# Dependencies:
#
# --python facebook sdk
# $ git clone git://github.com/pythonforfacebook/facebook-sdk.git
# $ cd facebook-sdk
# $ python setup.py install
#
# --pymongo
# $ easy_install pymongo

import facebook
import pymongo

# Retrieve this from db, should probably be received
# from the clientside Facebook Login javascript API
access_token = None

graph = facebook.GraphAPI(access_token)
print graph.get_object('me')
