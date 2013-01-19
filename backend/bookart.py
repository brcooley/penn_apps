# bookart.py
# @author Mike
# helper class for coverScrape.py to find cover art for
# nytimes best sellers

import requests
import json

class BookArt:

    __API_DOMAIN = 'http://ajax.googleapis.com'
    __API_ENDPOINT_ROOT = '/ajax/services/search/images?'
    __API_VERSION = 'v=1.0'
    __API_QUERY = '&q='

    def __init__(self):
        pass

    def get_api_url(self):
        return self.__API_DOMAIN + \
                self.__API_ENDPOINT_ROOT + \
                self.__API_VERSION + \
		self.__API_QUERY

    def append_title(self, url, title):
        urlEnd = ''
        tArray = title.split()
        for token in tArray:
            urlEnd += token + '%20' 
        urlEnd + 'cover%20art'
        final_url = url + urlEnd + 'book%20cover%20'
        return final_url

    def get_art(self, title):
        url = self.get_api_url()
        final_url = self.append_title(url, title)

        r = requests.get(final_url)

        j = json.loads(r.content)
        return j
