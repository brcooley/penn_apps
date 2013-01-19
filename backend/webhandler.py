#!/usr/bin/env python
'''
take access_token ip
    return random location, pictures, flight info, hotel
take photo,
    return filepicker'd pictures
'''

import json
import os
import random
import urllib

import pymongo
import requests
import web

import airport
import flickrsearch

urls = (
    '/vacationinfo', 'vacation_info',
    )

class vacation_info:
    def GET(self):
        print web.input()
        return self.POST()
    def POST(self):
        print web.data()
        location = choose_location() 
        ip_address = web.ctx.ip
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps({
            'location': location,
            'photos': list(flickrsearch.iter_results(location)),
            'flights': {
                'nearest': airport.nearest_airport(ip_address),
                },
            'hotels': None,
            'books': None,
            })

def choose_location():
    return random.choice((
        'Hawaii',
        'New York City',
        'Prague',
        'Bankok',
        'Williamsburg',
        ))

def extend_token(access_token):
    url = ('https://graph.facebook.com/oauth/access_token?' + \
        'grant_type=fb_exchange_token&' \
        'client_id=%s&' \
        'client_secret=%s&' \
        'fb_exchange_token=%s') % (app_id, app_secret, access_token)
    dct = dict(x.split('=') for x in requests.get(url).text.split('&'))
    new_access_token = dct['access_token']
    # Update all tables to reflect the new access token.
    conn = pymongo.MongoClient('localhost', 27017) 
    db = conn.facation
    db.collections.update(
        { 'access_token': new_access_token },
        { 'access_token': access_token })
    conn.close()
    return new_access_token
 

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()