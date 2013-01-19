#!/usr/bin/env python

import pymongo

import flickrsearch

if __name__ == '__main__':
    conn = pymongo.MongoClient('localhost', 27017)
    try:
        db = conn.facation
        loc_name = raw_input('Enter location name: ').title()
        if db.locations.find_one({'name':loc_name}) is not None:
            print 'Location already in db'
            import sys
            sys.exit()
        print 'Searching flickr...'
        photos = list(flickrsearch.iter_results(loc_name.lower()))
        if raw_input('Found %d photos. Add to db? y/n ' \
                % len(photos)).startswith('y'):
            db.locations.insert({
                'name': loc_name,
                'photos': photos,
                })
            print 'Added location:', loc_name
        else:
            print 'No location added.'
    finally:
        conn.close()
