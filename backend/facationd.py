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
import StringIO
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
    return db.jobs.find(
        { 'timestamp': { '$lte': time.time()-5*3600 } },
        { '_id': 1, 'jobs_args': 1})


def execute_job(_id, job):
    global db
    access_token, action, args, kwargs = job
    graph = facebook.GraphAPI(access_token)
    if action == 'put_wall_post':
        func = graph.put_wall_post
    elif action == 'put_photo':
        # Retrieve the album_id and location for this vacation.
        result = db.vacations.find_one(
            { 'access_token': access_token },
            { 'location': 1, 'album_id': 1, '_id': 0 })
        location, album_id = result['location'], result['album_id']
        # Create the facebook album if it doesn't exists.
        if result['album_id'] is None:
            album_id = create_album('Awesome %s Photos!' % \
                    location.title())
            db.vacations.update(
                { 'access_token': access_token },
                { 'album_id': album_id })
        kwargs['album_id'] = album_id
        args[0] = StringIO.StringIO(requests.get(args[0]).text)
        func = graph.put_photo
    else:
        print 'action:', action
    # Apply the action and get the facebook id.
    func(*args, **kwargs)
    # Remove the job
    db.jobs.remove({ '_id': _id })


def create_album(graph, name):
    '''Create album on facebook and return its id.'''
    return graph.put_object('me', 'albums', name=name)['id']


db = None
def main():
    global db
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.facation
    try:
        #pool = multiprocessing.Pool(processes=num_processes)
        while True:
            debug('reading and executing jobs asynchronously')
            #debug('jobs: %s' % jobs)
            #pool.apply_async(execute_job, jobs)
            for job in read_jobs():
                debug('executing job: %s' % job)
                execute_job(job['_id'], job['jobs_args'])
            debug('sleeping %d seconds' % update_interval)
            time.sleep(update_interval)
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

