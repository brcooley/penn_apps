#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
#
# coverScrape.py
# @author Mike
# finds cover art for the books from nytimes best sellers

from bookart import BookArt
from bestsellers import BestSellers
import requests
import json
import pprint
import random

api_key = 'bc909254c6c2e7d4b9a73267f33d4cd8:10:67204552'
genre = 'combined-print-and-e-book-fiction'

def select_book():
    b = BestSellers(api_key)
    book_list = b.get_list(genre)
    # the only variable is WHICH_ENTRY, everything else should be
    # hardcoded ------>  book_list[WHICH ENTRY][u 'book_details'][0][u'title']

    #select the entry
    WHICH_ENTRY = random.randint(0,len(book_list)-1)
    title = book_list[WHICH_ENTRY][u'book_details'][0][u'title']

    WHICH_IMG = 0
    art = BookArt().get_art(title)

    # Try the first few images in case one 404s
    for i in range(5):
        # Process the JSON string.
        url = art[u'responseData'][u'results'][WHICH_IMG][u'url'] 
        # Make sure the image doesn't 404
        response = requests.get(url)
        if response.status_code == 200:
            break
    return {
        'title': title.title(),
        'photo': url,
        }
