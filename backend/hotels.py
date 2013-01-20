#!/usr/bin/env python
# @author Mike
#
# hotels.py
#

import json
import requests
import urllib
import pprint

# dest is a string which contains a city name.
# It can also have country, state, etc.
# all dates MM/DD/YYYY -- where do the dates go???
def pick_hotel( dest, whichHotel=0):
    url = 'http://api.ean.com/ean-services/rs/hotel/v3/list'
    payload = {
        'apiKey': 'j6xun3rbjn66vhzhvnm99twg',
        'cid': '55505',
        'destinationString': dest,
        'minStarRating': '4.0'
        }
    hotelInfo = requests.get(url, params=payload)

    #need to limit what info is being passed up
    hotelSummary = hotelInfo.json() \
        ['HotelListResponse']['HotelList']['HotelSummary'][whichHotel]
    return hotelSummary


def getHotelImages( hotelID ):
    url = 'http://api.ean.com/ean-services/rs/hotel/v3/roomImages'
    payload = {
        'apiKey': 'j6xun3rbjn66vhzhvnm99twg',
        'cid': '55505',
        'hotelId': hotelID
        }
    hotelInfo = requests.get(url, params=payload)
    junk = hotelInfo.json()
    return [i.values()[0] for i in \
        junk['HotelRoomImageResponse']['RoomImages']['RoomImage']]
    return urlList


#someHotel = pickHotel('Boston')
#print someHotel
#print getHotelImages(someHotel['hotelId'])
