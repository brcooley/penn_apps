import urllib

import pymongo
import requests
import web

urls = (
    '/extend_token', 'extend_token',
    )

class extend_token:
    def GET(self, access_token):
        print access_token
        return
        url = ('https://graph.facebook.com/oauth/access_token?' + \
            'grant_type=fb_exchange_token&' \
            'client_id=%s&' \
            'client_secret=%s&' \
            'fb_exchange_token=%s') % (app_id, app_secret, access_token)
        dct = dict(x.split('=') for x in requests.get(url).text.split('&'))
        new_access_token = dct['access_token']
        # Update all tables to reflect the new access token.
        conn = pymongo.MongoClient('localhost', 27017) 
        db = conn.facation
        db.collections.update(
            { 'access_token': new_access_token },
            { 'access_token': access_token })
        conn.close()
        return new_access_token


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()


