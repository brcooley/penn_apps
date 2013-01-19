import json, requests, urllib
import csv
from math import radians, cos, sin, asin, sqrt

def getGeoInfo( ip ):
    url = "http://freegeoip.net/json/" + str(ip)
    result = requests.get(url)
    return result.json()

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


with open('airports.dat') as f:
    airports = (x.split('\t') for x in f.read().split('\n')[1:-1])
def nearest_airport(ip):
    global airports
    geo = getGeoInfo(ip)
    lat = float(geo['latitude'])
    lon = float(geo['longitude'])

    distances = \
        ((haversine(lat, lon, float(entry[2]), float(entry[3])), \
            entry)for entry in airports)
    min_distance, nearest_airport = min(distances, key=lambda x: x[0])
    return {
        'airport': nearest_airport,
        'distance': min_distance,
        }

