import json, requests, urllib

def getGeoInfo( ip ):
    url = "http://freegeoip.net/json/" + str(ip)
    result = requests.get(url)
    return result.json()



def main():
    geo = getGeoInfo('158.130.102.99')
    print "lat:  "+ geo['latitude']
    print 'long: ' + geo['longitude']


main()
