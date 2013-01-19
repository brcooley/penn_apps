# coding: utf-8
import json, requests, urllib

# dest is a string which contains a city name. It can also have country, state, etc.
# all dates MM/DD/YYYY
def pickHotel( dest, arrival, departure ):
    url = "http://api.ean.com/ean‑services/rs/hotel/v3/list"
    payload = {'minorRev':'20', 'apiKey':'j6xun3rbjn66vhzhvnm99twg', 'cid':'55505', 'numberOfResults':'1', 'minStarRating':'4', 'destinationString':dest, 'room1':'2', 'arrivalDate':arrival, 'departureDate':departure}
    #print url
    hotelInfo = requests.get(url, params=payload)
    print hotelInfo.url
    print hotelInfo
    #return hotelID


pickHotel("Boston", '01/27/2013', '01/29/2013')
