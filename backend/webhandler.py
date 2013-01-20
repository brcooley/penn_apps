#!/usr/bin/env python
'''
take access_token ip
    return random location, pictures, flight info, hotel
take photo,
    return filepicker'd pictures
'''

import datetime
import json
import os
import random
import urllib
import threading

import pymongo
import requests
import web

import airport
import bookchooser
import fbscheduler
import flightsearch
import hotels
import imagemaker

urls = (
    '/vacationinfo', 'vacation_info',
    '/start',        'start',
    )

class vacation_info:
    def GET(self):
        return self.POST()
    def POST(self):
        access_token = web.input()['access_token']

        # Location and length of trip.
        location = rand_location() 
        length = random.randrange(3, 15)

        # Arguments for flights api.
        geo = airport.getGeoInfo(web.ctx.ip)
        city, state = geo['city'], geo['region_code']
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=length)
        try:
            flights = flightsearch.select_flight(
                city, location['name'], start_date, end_date),
        except Exception as e:
            print e
            flights = None

        try:
            hotel = hotels.select_hotel(location['name'])
        except Exception as e:
            print e
	
        hotel = {
            'name': 'An exclusive 5-star resort',
            'pic': 'http://images.theage.com.au/2010/04/26/1382672/Hotel_Generic-420x0.jpg'
            }

        try:
            book = bookchooser.select_book()
        except Exception as e:
            print e
            book = {
                'title': 'a good book',
                'photo': 'http://www.papierplume.com/media/catalog/product/cache/1/image/5e06319eda06f020e43594a9c230972d/m/o/modern-hard-bound-leather_2.jpg',
                }

        payload = {
            'location': [city, location['name']],
            'photos': location['photos'],
            'flights': flights,
            'hotels': hotel,
            'books': book,
            'length': length,
            'album_id': None,
            }

        conn = pymongo.MongoClient('localhost', 27017)
        try:
            db = conn.facation
            new_payload = payload.copy()
            new_payload['access_token'] = access_token
            db.vacations.insert(new_payload)
            #print 'inserted', new_payload
        finally:
            conn.close()

        # Headers and json return dictionary.
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps(payload)

class start:
    def POST(self):
        # expect access_token and fb_picture
        access_token = web.input()['access_token']
        fg_picture = web.input()['fg_picture']
        speed = web.input()['speed']
        #speed = True

        def generate_vacation():
            # Add this vacation to the db.
            conn = pymongo.MongoClient('localhost', 27017)
            try:
                db = conn.facation
                #new_token = extend_token(access_token)
                data = db.vacations.find_one({
                    'access_token': access_token,
                    })
                photos = db.locations.find_one({
                    'name': data['location'][1],
                    })['photos']
                if True:
                    photos = random.sample(photos, min(6, len(photos)))
                    composites = photos[:len(photos)/2]
                    plain = photos[len(photos)/2:]
                    if composites:
                        try:
                            composites = imagemaker.batchImages(
                                    fg_picture, composites)
                        except Exception as e:
                            print e
                    data['photos'] = {
                        'composite': composites,
                        'plain': plain,
                        }
                    data['speed'] = bool(speed)
                    #print data['photos']
            finally:
                conn.close()

            # Schedule all the facebook stuff here.
            fbscheduler.schedule_vacation(access_token, data)

        threading.Thread(target=generate_vacation).start()

        # Headers and json return dictionary.
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps({ })

def rand_location():
    conn = pymongo.MongoClient('localhost', 27017)
    try:
        db = conn.facation
        return random.choice(list(db.locations.find(
            {}, {'name': 1, 'photos': 1, '_id': 0})))
    finally:
        conn.close()


def extend_token(access_token):
    global app_id, app_secret
    url = ('https://graph.facebook.com/oauth/access_token?' + \
        'grant_type=fb_exchange_token&' \
        'client_id=%s&' \
        'client_secret=%s&' \
        'fb_exchange_token=%s') % (app_id, app_secret, access_token)
    t = requests.get(url).text
    #print t
    dct = dict(x.split('=') for x in t.split('&'))
    new_access_token = dct['access_token']
    # Update access_key everywhere in table
    #db.collections.update(
    #    { 'access_token': new_access_token },
    #    { 'access_token': access_token })
    return new_access_token
 

import ConfigParser
config = ConfigParser.RawConfigParser()
try:
    with open(os.path.expanduser('~/.facationd.conf')) as f:
        config.readfp(f)
    app_id = config.get('facationd', 'app_id')
    app_secret = config.get('facationd', 'app_secret')
    assert app_id and app_secret
except AssertionError:
    print 'config needs keys app_id and app_secret under [facationd]'
except IOError:
    print 'missing config file ~/.facationd.conf'
 

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
