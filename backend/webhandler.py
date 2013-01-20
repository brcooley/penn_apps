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

import pymongo
import requests
import web

import airport
import bookchooser
import fbscheduler
import flightsearch
import hotels

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
        flights = flightsearch.select_flight(
            city, location['name'], start_date, end_date),

        hotel = hotels.select_hotel(location['name'])
        book = bookchooser.select_book()

        blebleble = {
            'location': location['name'],
            'photos': location['photos'][:10],
            'flights': flights,
            'hotels': hotel,
            'books': book,
            'length': length,
            }

        conn = pymongo.MongoClient('localhost', 27017)
        try:
            db = conn.facation
            asdf = blebleble.copy()
            asdf.update({'access_token':access_token})
            db.vacations.insert(asdf)
        finally:
            conn.close()

        # Headers and json return dictionary.
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps(blebleble)

class start:
    def POST(self):
        # expect access_token and fb_picture
        locals().update(web.input())

        # Add this vacation to the db.
        conn = pymongo.MongoClient('localhost', 27017)
        try:
            db = conn.facation
            new_token = extend_token(access_token)
            db.vacations.update({
                'access_token': access_token, 
                }, {
                'access_token': new_token,
                'album_id': None
                })
            data = db.vacations.find({
                'access_token': new_token,
                })
        finally:
            db.close()

        # Schedule all the facebook stuff here!!!!!!!!!
        fbscheduler.schedule_vacation(access_token, data)

        # Headers and json return dictionary.
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps({
            })

def rand_location():
    conn = pymongo.MongoClient('localhost', 27017)
    try:
        db = conn.facation
        return random.choice(list(db.locations.find(
            {}, {'name': 1, 'photos': 1, '_id': 0})))
    finally:
        conn.close()


def extend_token(access_token):
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
 



if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
