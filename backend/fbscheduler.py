import time
from datetime import *

import pymongo

def schedule_vacation(access_token, location):
    '''Mike and Nathan look at _schedule_vacation instead!'''
    conn = pymongo.MongoClient('localhost', 27017)
    try:
        _schedule_vacation(db.facation, access_token, location)
    finally:
        conn.close()


def schedule_vacation(db, access_token, location):
    '''
    Schedule jobs to be executed by the Facebook API.

    Examples: (see https://github.com/pythonforfacebook/facebook-sdk/blob/master/facebook.py for functions and arguments and/or ask Peter for help! :D)

    # Post a status at 7pm on Jan 23
    timestamp = datetime(2013, 1, 23, 19)
    schedule_job(db, access_token, timestamp, 'Hello, world!')

    # Post a picture at in 3 days and 7 hours from now
    timestamp = datetime.now() + timedelta(days=3, hours=7)
    schedule_job(db, access_token, timestamp, 'put_photo', url, 'Caption!')
    '''
    pass


def schedule_job(db, access_token, timestamp, token, *args, **kwargs):
    db.jobs.insert({
        'timestamp': time.mktime(timestamp.timetuple()),
        'jobs_args': [access_token, token, args, kwargs],
        })

