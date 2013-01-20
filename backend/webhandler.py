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
        print web.input()
        #access_token = web.input()['access_token']

        # Location and length of trip.
        location = rand_location() 
        length = random.randrange(3, 15)

        # Arguments for flights api.
        geo = airport.getGeoInfo(web.ctx.ip)
        city, state = geo['city'], geo['region_code']
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=length)

        # Headers and json return dictionary.
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps({
            'location': location['name'],
            'photos': location['photos'][:10],
            'flights': flightsearch.select_flight(
                city, location['name'], start_date, end_date),
            'hotels': hotels.select_hotel(location['name']),
            'books': bookchooser.select_book(),
            'length': length,
            })

class start:
    def POST(self):
        # expect access_token and location
        locals().update(web.input())

        # Add this vacation to the db.
        conn = pymongo.MongoClient('localhost', 27017)
        try:
            db = conn.facation
            db.vacations.insert({
                'access_token': access_token,
                'location': location,
                'album_id': None
                })
        finally:
            db.close()

        # Schedule all the facebook stuff here!!!!!!!!!
        fbscheduler.schedule_vacation(access_token, location)

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


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
