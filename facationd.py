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

import multiprocessing.dummy as multiprocessing # Use threads.
import os
import sys
import time

import daemon
import facebook
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
    debug('reading jobs (although not really yet)')
    return []


def execute_job(access_token, *args):
    graph = facebook.GraphAPI(access_token)

    # put_wall_post: message, attachment={}, profile_id="me"
    if args[0] == 'put_wall_post':
        post_id =  graph.put_wall_post()['id']
        # maybe store it
        
    # put_photo: image, message=None, album_id=None
    elif args[0] == 'post_photo':
        album_id = None # get the album_id
        post_id = graph.put_photo('me', message, album_id)
        # maybe store it


def create_album(graph, name):
    return graph.put_object('me', 'albums', name=name)['id']


def main():
    pool = multiprocessing.Pool(processes=num_processes)
    while True:
        debug('reading and executing jobs asynchronously')
        pool.apply_async(execute_job, read_jobs())
        debug('sleeping %d seconds' % update_interval)
        time.sleep(update_interval)
        break


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
