#!/usr/bin/env python

import pprint
import requests

def main():
	csrf = requests.get('http://www.hipmunk.com')
	search_strings = { 'i': 'Philidelphia+PA.Denver+CO,Jan26.Feb2' }
	headers = { 'X-Csrf-Token': csrf.headers['X-Csrf-Token'] }
	raw_data = requests.post('http://www.hipmunk.com/api/results', data=search_strings, headers=headers)
	pprint.pprint(raw_data.json()['routings'])

main()
