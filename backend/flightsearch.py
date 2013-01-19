#!/usr/bin/env python
#
# flightsearch.py
# @author Mike
#
# scrapes hipmunk for flight information
#
# the storage container, 'itineraries', is a dictionary
# containing arrays of outgoing and return flights that 
# contain arrays of routes that contain arrays of legs 
# that contain dictionaries of leg flight information
# 
# when developing a heuristic for chooosing the flight,
# note that the outgoing and return itineraries are
# sorted by 'agony' score, with the low-agony, direct flights
# near the beginning and the high-agony, high-connection 
# flights are at the end

import datetime
import dateutil.parser
import pprint
import requests

OUTGOING = 0
RETURN = 1

def select_flight(from_, to, start_date, end_date):
    start_date = start_date.strftime('%b%d')
    end_date = end_date.strftime('%b%d')
    csrf = requests.get('http://www.hipmunk.com')
    search_strings = { 'i': '%s.%s,%s.%s' % \
            (from_, to, start_date, end_date)}
    headers = { 'X-Csrf-Token': csrf.headers['X-Csrf-Token'] }
    raw_data = requests.post('http://www.hipmunk.com/api/results', \
        data=search_strings, headers=headers)

    #splits flights into outgoing and returns
    outgoingFlights = raw_data.json()['routings'][OUTGOING]
    returnFlights = raw_data.json()['routings'][RETURN]

    return {'outgoing': getFlights(outgoingFlights[0]), \
        'return': getFlights(returnFlights[0])}
    
    #take the first flight?
    #-----------------------------------------------------#
    #T0D0: write code here with a heuristic that selects
    #an itinerary
    #-----------------------------------------------------#

def getFlights(route):
    routings = []
    flights = route['legs']
    trip = []
    for flight in flights:
        num = flight['marketing_num'][0] + ' ' + str(flight['marketing_num'][1])
        #print num
        origin = flight['from_code']
        #print origin
        dest = flight['to_code']
        #print dest
        depart = dateutil.parser.parse(flight['depart']).strftime('%m/%d/%y')
        #print depart
        arrive = dateutil.parser.parse(flight['arrive']).strftime('%m/%d/%y')
        #print arrive
        leg = {'flight': num, 'origin': origin, 'dest': dest, \
            'takeoff': depart, 'arrive': arrive}
        trip.append(leg)
    routings.append(trip)
    #print '\n'
    return routings

