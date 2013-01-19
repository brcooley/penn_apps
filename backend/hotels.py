import json, requests, urllib

# dest is a string which contains a city name. It can also have country, state, etc.
# all dates MM/DD/YYYY
def pickHotel( dest, arrival, departure, whichHotel=0):
    url = 'http://api.ean.com/ean-services/rs/hotel/v3/list'
    payload = {'apiKey':'j6xun3rbjn66vhzhvnm99twg', 'cid':'55505', 'destinationString':dest , 'minStarRating':'4', }
    #print url
    hotelInfo = requests.get(url, params=payload)
    print hotelInfo.url
    hotelSummary = hotelInfo.json()['HotelListResponse']['HotelList']['HotelSummary'][whichHotel]
    
    return hotelID


pickHotel("Boston", '01/27/2013', '01/29/2013')
