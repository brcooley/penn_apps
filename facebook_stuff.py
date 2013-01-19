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

import os
import sys

import daemon
import facebook
import pymongo


'''
# Retrieve this from db, should probably be received
# from the clientside Facebook Login javascript API
access_token = None

graph = facebook.GraphAPI(access_token)
print graph.get_object('me')
'''

pidfile_path = '/var/run/pennapps.pid'


def read_pidfile():
    with open(pidfile_path) as pidfile:
        return int(pidfile.read())


def write_pidfile():
    with open(pidfile_path, 'w+') as pidfile:
        pidfile.write('%d\n' % os.getpid())


def main():
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
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
            print 'Running as PID %d.' % read_pidfile()
        else:
            print 'Not running.'
    else:
        print 'Usage: %s [start|status]' % sys.argv[0]

