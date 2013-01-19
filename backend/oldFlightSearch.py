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

import pprint
import requests
import pprint
import dateutil.parser

OUTGOING = 0
RETURN = 1

def main():
	csrf = requests.get('http://www.hipmunk.com')
	search_strings = { 'i': 'Philidelphia.Denver,Jan26.Feb2' }
	#search_strings = { 'i': 'Philidelphia+PA.Chicago,Jan26.Feb2' }
	headers = { 'X-Csrf-Token': csrf.headers['X-Csrf-Token'] }
	raw_data = requests.post('http://www.hipmunk.com/api/results', \
	    data=search_strings, headers=headers)
	#pprint.pprint(raw_data.json()['routings'])

	#splits flights into outgoing and returns
	outgoingFlights = raw_data.json()['routings'][OUTGOING]
	returnFlights = raw_data.json()['routings'][RETURN]

	itineraries = {'outgoing': getFlights(outgoingFlights), \
	    'return': getFlights(returnFlights)}
	#pprint.pprint(itineraries)
	
	#take the first flight?
	#-----------------------------------------------------#
	#T0D0: write code here with a heuristic that selects
	#an itinerary
	#-----------------------------------------------------#
	print 1


def getFlights(routes):
	routings = []
	for route in routes:
	  flights = route['legs']
	  trip = []
	  for flight in flights:
	    num = flight['marketing_num'][0] + ' ' + str(flight['marketing_num'][1])
	    #print num
	    origin = flight['from_code']
	    #print origin
	    dest = flight['to_code']
	    #print dest
	    depart = dateutil.parser.parse(flight['depart'])
	    #print depart
	    arrive = dateutil.parser.parse(flight['arrive'])
	    #print arrive
	    leg = {'flight': num, 'origin': origin, 'dest': dest, \
		'takeoff': depart, 'arrive': arrive}
	    trip.append(leg)
	  routings.append(trip)
	  #print '\n'
	return routings

main()
