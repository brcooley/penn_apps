#!/usr/bin/env python
#
# destScrape.py
#
# @author Mike
#
# uses http://stuvel.eu/flickrapi to scrape images from flickr using
# flickr.photos.search function, documentation for which is
# http://www.flickr.com/services/api/flickr.photos.search.html 
#
# most of the code in this example comes from
# http://spanring.eu/blog/2010/02/25/python-flickr-api-geo-search-example/
#-------------------------------------------------------------------------------------
# http://farm9.staticflickr.com/8516/8391840883_1cd60e55d8_b.jpg  <<<< Chicago pic
# http://farm9.staticflickr.com/8187/8392484980_0d409f2ea2_b.jpg  <<<< Chicao pic 2

# secret = 95940c26dc30095f

import flickrapi

api_key = '005b8c46e4020bd2639342676d41cfcc'

flickr = flickrapi.FlickrAPI(api_key)
#photos = flickr.photos_search(tags='boston', lat='42.355056', lon='-71.065503', radius='5')
#photos = flickr.photos_search(has_geo='true', geo_context=1, \
#      extras='original_format',text='chicago')
photos = flickr.photos_search(has_geo='true', text='chicago, il')

for photo in photos[0]:
       #print photo.attrib['title']
       #photoLoc = flickr.photos_geo_getLocation(photo_id=photo.attrib['id'])
       #print photoLoc[0][0].attrib['latitude']
       #print photoLoc[0][0].attrib['longitude']
       photoSizes = flickr.photos_getSizes(photo_id=photo.attrib['id'])

       # try to print largest possible, catch IndexError if we go too big
       try: 
	  print photoSizes[0][9].attrib['source']
       except IndexError:
	  pass
