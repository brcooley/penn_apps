import json, requests, urllib
import csv
import math

def getGeoInfo( ip ):
    url = "http://freegeoip.net/json/" + str(ip)
    result = requests.get(url)
    return result.json()

def distance( x1 , y1 , x2 , y2 ):
   return  math.sqrt(math.abs((x1-x2)**2 + (y1-y2)**2))

def main():
    geo = getGeoInfo('158.130.102.99')
    lat = geo['latitude']
    lon = geo['longitude']
    print "lat:  "+ lat
    print 'long: ' + lon
    airports = csv.DictReader('airports.dat')
    #minDistance = min([distance(lat, lon, entry['LATITUDE'], entry['LONGITITUDE']) for entry in airports])
    #print "min distance: " +  minDistance

    distances = (distance(lat, lon, entry['LATITUDE'], \
            entry['LONGITUDE']) for entry in airports)
    min_distance = min(zip(distances, airports), key=lambda x: x[0])
    print 'min distance: ', min_distance


main()
