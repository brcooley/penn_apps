#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# scrape.py
# @author Mike
# uses http://stuvel.eu/flickrapi to scrape images from flickr using
# flickr.photos.search function, documentation for which is
# http://www.flickr.com/services/api/flickr.photos.search.html 

import flickrapi

api_key = '005b8c46e4020bd2639342676d41cfcc'

flickr = flickrapi.FlickrAPI(api_key)
#photos = flickr.photos_search(tags='boston', lat='42.355056', lon='-71.065503', radius='5')
photos = flickr.photos_search(has_geo='true', text='london,UK')

for photo in photos[0]:
       print photo.attrib['title']
       photoLoc = flickr.photos_geo_getLocation(photo_id=photo.attrib['id'])
       print photoLoc[0][0].attrib['latitude']
       print photoLoc[0][0].attrib['longitude']
       photoSizes = flickr.photos_getSizes(photo_id=photo.attrib['id'])
       print photoSizes[0][1].attrib['source']
