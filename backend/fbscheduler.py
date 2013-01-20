#!/usr/bin/env python
#fbscheduler.py
# @author Mike
#
# schedules automated fb activity for delayed execution,
# talk to peter about how it works
#

import time
import random
from datetime import datetime, timedelta

import pymongo
import pprint
import random
from generateStatus import *

api_key = '415779275173477'
ORIGIN = 0
DEST = 1

def schedule_vacation(access_token, data):
    '''Mike and Nathan look at _schedule_vacation instead!'''
    conn = pymongo.MongoClient('localhost', 27017)
    try:
        _schedule_vacation(conn.facation, access_token, data)
    finally:
        conn.close()


def _schedule_vacation(db, access_token, data):
    '''
    Schedule jobs to be executed by the Facebook API.

    Examples: (see https://github.com/pythonforfacebook/facebook-sdk/blob/master/facebook.py 
    for functions and arguments and/or ask Peter for help! :D)

    # Post a status at 7pm on Jan 23
    timestamp = datetime(2013, 1, 23, 19)
    schedule_job(db, access_token, timestamp, 'put_wall_post', 'Hello, world!')

    # Post a picture at in 3 days and 7 hours from now
    timestamp = datetime.now() + timedelta(days=3, hours=7)
    schedule_job(db, access_token, timestamp, 'put_photo', url, 'Caption!')
    '''

    #url = 'http://farm5.staticflickr.com/4108/5055725881_d3f62c280d_b.jpg'

    #timestamp = datetime(2013, 1, 19, 21, 40)
    #status = generateFirstStatus(data)
    #schedule_job(db, access_token, timestamp, 'put_wall_post', status)

    #db_out = list(db.locations.find({'name': dest}))

    #pic_list = db_out[0][u'photos']
    #url = random.choice(pic_list)
    #print url
    #schedule_job(db, access_token, timestamp, 'put_photo', url, \
	#'Look at me, here in ' + dest + '!')
    dest = data['location'][DEST]
    stat1 = generateFirstStatus(dest)
    stat2 = generateMiddleStatus(dest)
    stat3 = generateEndStatus(dest)
    #fire them all off at once
    timestamp1 = timestamp2 = timestamp3 = datetime(2013, 1, 20, 0, 0)
    if data['speed'] == False:
        timestamp1 = datetime(2013, 1, 20, 0, 0)
        timestamp2 = datetime(2013, 1, 25, 0, 0)
        timestamp3 = datetime(2013, 1, 29, 0, 0)
    schedule_job(db, access_token, timestamp1, 'put_wall_post', stat1)
    schedule_job(db, access_token, timestamp2, 'put_wall_post', stat2)
    #empty pics
    for image in data['photos']['plain']:
        schedule_job(db, access_token, timestamp2, 'put_photo', image, '')
    for image in data['photos']['composite']:
        schedule_job(db, access_token, timestamp2, 'put_photo', image, generateImageTag(dest))
    schedule_job(db, access_token, timestamp3, 'put_wall_post', stat3)
    

def schedule_job(db, access_token, timestamp, token, *args, **kwargs):
    db.jobs.insert({
        'timestamp': time.mktime(timestamp.utctimetuple()),
        'jobs_args': [access_token, token, args, kwargs],
        })

