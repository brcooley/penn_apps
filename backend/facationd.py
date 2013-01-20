#!/usr/bin/env python

# Dependencies:
#
# --python facebook sdk
# $ git clone git://github.com/pythonforfacebook/facebook-sdk.git
# $ cd facebook-sdk
# $ python setup.py install
#
# --pymongo
# $ easy_install pymongo
#
# --python daemon
# install it from here: http://pypi.python.org/pypi/python-daemon/

import ConfigParser
import multiprocessing.dummy as multiprocessing # Use threads.
import os
import sys
import time
import urllib

import daemon
import facebook
import requests
import pymongo


pidfile_path = '/var/run/pennapps.pid'
update_interval = 60
num_processes = 4


debug = True
def debug(mesg):
    if debug:
        print 'debug: ' + mesg


def read_pidfile():
    with open(pidfile_path) as pidfile:
        return int(pidfile.read())


def write_pidfile():
    with open(pidfile_path, 'w+') as pidfile:
        pidfile.write('%d\n' % os.getpid())


def read_jobs():
    '''Read jobs that are ready to be executed.'''
    global db
    return list(db.jobs.find(
        { 'timestamp': { '$lte': time.time() } },
        { '_id': 0, 'job_args': 1}))


def execute_job(job):
    global db
    access_token, action, args, kwargs = job
    graph = facebook.GraphAPI(access_token)
    if action == 'put_wall_post':
        func = graph.put_wall_post
        id_key = 'id'
    elif action == 'put_photo':
        # Retrieve the album_id and location for this vacation.
        location, album_id = db.vacations.find_one(
            { 'access_token': access_token },
            { 'location': 1, 'album_id': 1, '_id': 0 })
        # Create the facebook album if it doesn't exists.
        if album_id is None:
            album_id = create_album('Awesome %s Photos!' % \
                    location.title())
            db.vacations.update(
                { 'access_token': access_token },
                { 'album_id': album_id })
        kwargs['album_id'] = album_id
        func = graph.put_photo
        id_key = 'post_id'
    # Apply the action and get the facebook id.
    action_id = func(*args, **kwargs)[id_key]


def create_album(graph, name):
    '''Create album on facebook and return its id.'''
    return graph.put_object('me', 'albums', name=name)['id']


db = None
def main():
    global db
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.facation
    try:
        pool = multiprocessing.Pool(processes=num_processes)
        while True:
            debug('reading and executing jobs asynchronously')
            jobs = read_jobs()
            debug('jobs: %s' % jobs)
            pool.apply_async(execute_job, jobs)
            debug('sleeping %d seconds' % update_interval)
            time.sleep(update_interval)
            break
    finally:
        conn.close()

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
    usage = 'Usage: %s [test|start|status]' % sys.argv[0]
    if len(sys.argv) < 2:
        print usage
    elif sys.argv[1] == 'test':
        main()
    elif sys.argv[1] == 'start':
        # Tests if you have write access to pidfile_path
        write_pidfile()
        with daemon.DaemonContext():
            write_pidfile()
            try:
                main()
            except:
                os.unlink(pidfile_path)
    elif sys.argv[1] == 'status':
        if os.path.exists(pidfile_path):
            print 'Daemon is running as PID %d.' % read_pidfile()
        else:
            print 'Daemon is not running.'
    else:
        print usage

