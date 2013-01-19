# bookart.py
# @author Mike
# helper class for coverScrape.py to find cover art for
# nytimes best sellers

import requests
import simplejson

class BookArt:

  __API_DOMAIN = 'http://ajax.googleapis.com'
  __API_ENDPOINT_ROOT = '/ajax/services/search/images?'
  __API_VERSION = 'v=1.0'

  def __init__(self):

    def get_api_url(self):
      return self.__API_DOMAIN            \
	  + self.__API_ENDPOINT_ROOT    \
	  + self.__API_VERSION        

    def append_title(self, url, title):
      urlEnd
      tArray = title.split()
      for token in tArray:
	urlEnd += token + '%20' 
      urlEnd + 'cover%20art'
      final_url = url + urlEnd
      return final_url

    def get_art(self, title):
        url = self.get_api_url()
        final_url = self.append_title(url, title)

        r = requests.get(final_url)

        j = simplejson.loads(r.content)
        return j
