#!/usr/bin/env python
# nybest.py
# @author Mike
# queries nytimes api and asks for a best seller; currently uses
# the first listing from the query

from bestsellers import BestSellers
import pprint
import simplejson

api_key = 'bc909254c6c2e7d4b9a73267f33d4cd8:10:67204552'
#genre = 'hardcover-fiction'
genre = 'combined-print-and-e-book-fiction'

b = BestSellers(api_key)
book_list = b.get_list(genre)
# the only variable is WHICH_ENTRY, everything else should be
# hardcoded ------>  book_list[WHICH ENTRY][u 'book_details'][0][u'title']

print len(book_list)
#print book_list[WHICH_ENTRY][u'book_details'][0][u'title']
for book in book_list:
   print book[u'book_details'][0][u'title']

