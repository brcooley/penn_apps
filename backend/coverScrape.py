#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
#
# coverScrape.py
# @author Mike
# finds cover art for the books from nytimes best sellers

from bookart import BookArt
from bestsellers import BestSellers
import requests
import simplejson
import pprint
import random

api_key = 'bc909254c6c2e7d4b9a73267f33d4cd8:10:67204552'
#genre = 'hardcover-fiction'
genre = 'combined-print-and-e-book-fiction'

b = BestSellers(api_key)
book_list = b.get_list(genre)
# the only variable is WHICH_ENTRY, everything else should be
# hardcoded ------>  book_list[WHICH ENTRY][u 'book_details'][0][u'title']

#print book_list[WHICH_ENTRY][u'book_details'][0][u'title']
for book in book_list:
   print book[u'book_details'][0][u'title']

#select the entry
WHICH_ENTRY = random.randint(0,len(book_list)-1)
print WHICH_ENTRY
title = book_list[WHICH_ENTRY][u'book_details'][0][u'title']

ba = BookArt()

art = ba.get_art(title)

#url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
#             'v=1.0&q=barack%20obama&userip=INSERT-USER-IP')
WHICH_IMG = 0

#r = requests.get(url)
#j = simplejson.loads(r.content)

# Process the JSON string.
print art[u'responseData'][u'results'][WHICH_IMG][u'url'] 
#pprint.pprint(results[0][u 'responseData'])
