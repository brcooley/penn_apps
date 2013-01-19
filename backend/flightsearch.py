#!/usr/bin/env python

import requests
import pprint

def main():
	csrf = requests.get('http://www.hipmunk.com')
	search_strings = { 'i': 'Philidelphia+PA.Denver+CO,Jan26.Feb2' }
	#search_strings = { 'i': 'Philidelphia+PA.Chicago,Jan26.Feb2' }
	headers = { 'X-Csrf-Token': csrf.headers['X-Csrf-Token'] }
	raw_data = requests.post('http://www.hipmunk.com/api/results', \
	    data=search_strings, headers=headers)
	#pprint.pprint(raw_data.json()['routings'])
	routes = raw_data.json()['routings'][0]
	#pprint.pprint(routes)
	for route in routes:
	  flights = route['legs']
	  for flight in flights:
	    print flight['marketing_num'][0] + ' ' + str(flight['marketing_num'][1])
	    print flight['from_code']
	    print flight['to_code']
	    print flight['depart']
	    print flight['arrive']
	  print '\n'

main()
