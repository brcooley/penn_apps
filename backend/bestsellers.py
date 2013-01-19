# bestsellers.py
# @author Mike
# class for  best sellers queries of the nytimes api

import requests
import json


class BestSellers:

    __API_DOMAIN = 'http://api.nytimes.com'
    __API_ENDPOINT_ROOT = '/svc/books'
    __API_VERSION = '/v2'
    __API_ENDPOINT_LIST = '/lists'
    __API_ENDPOINT_LIST_NAMES = '/lists/names'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_api_url(self, api_endpoint):
        return self.__API_DOMAIN            \
                + self.__API_ENDPOINT_ROOT    \
                + self.__API_VERSION        \
                + api_endpoint

    def append_api_key(self, url):
        return url + '?&api-key=' + self.api_key

    def get_list_names(self):
        url = self.get_api_url(self.__API_ENDPOINT_LIST_NAMES)
        final_url = self.append_api_key(url)

        r = requests.get(final_url)

        j = json.loads(r.content)
        return j[u'results']

    def get_list(self, list_name):
        url = self.get_api_url(self.__API_ENDPOINT_LIST) + '/' + list_name
        final_url = self.append_api_key(url)
	#print final_url

        r = requests.get(final_url)

        j = json.loads(r.content)
        return j[u'results']

