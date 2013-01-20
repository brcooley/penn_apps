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
def select_hotel( dest, whichHotel=0):
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
    hotelSummary['pic'] = getHotelImages(hotelSummary['hotelId']) 
    if hotelSummary['pic'] != None:
        hotelSummary['pic'] = hotelSummary['pic'][0]
        return hotelSummary
    elif whichHotel == 4:
        hotelSumary['pic'] = 'http://imgur.com/dZxKhRP.jpg'
        return hotelSummary
    else:
        whichHotel += 1
        return select_hotel(dest, whichHotel)


def getHotelImages( hotelID ):
    url = 'http://api.ean.com/ean-services/rs/hotel/v3/roomImages'
    payload = {
        'apiKey': 'j6xun3rbjn66vhzhvnm99twg',
        'cid': '55505',
        'hotelId': hotelID
        }
    hotelInfo = requests.get(url, params=payload)
    junk = hotelInfo.json()
    if junk['HotelRoomImageResponse'].keys()[0] != 'RoomImages':
        return None
    return [i.values()[0] for i in \
        junk['HotelRoomImageResponse']['RoomImages']['RoomImage']]
    #return urlList


#pprint.pprint( select_hotel('Chicago') )
#print someHotel
#pprint.pprint( getHotelImages(someHotel['hotelId']))
