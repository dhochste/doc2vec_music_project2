"""
Querying Google's Freebase API

David L. Hochestetler
1/26/15

"""

import json
import requests
import sys
import time
from collections import defaultdict


def do_query(album_title, service_url, api_key, limit = 1):
	"""
	Query the using api_key for the artist and genre corresponding to an album 
	title. This was created for freebase api.
	"""

	# Create a mql query
	query_names_genres = [{
		"type": "/music/album",
		"artist": None,
		"name": album_title,
		"genre": []
		"limit": limit
	}]

    opts = {
        "query": json.dumps(query_names_genres),
        "key": api_key     
    }

    r = requests.get(service_url, params=opts)
    response = r.json()

    if u'error' in response:
        print 'Request failed. Return: ',
        print response
        sys.exit(1)

    return response

    # results_dict = defaultdict(dict)
    # for item in response[u'result']:
    #     results_dict[item[u'name']] = {'Artist': item[u'artist'], 'Genre': item[u'genre']}

    # return results_dict

def dict_get_artist_genre(response):

	artist = response[u'result'][0][u'artist'].encode('UTF8')
	title = response[u'result'][0][u'name'].encode('UTF8')
	genre_list = response[u'result'][0][u'genre']
	genre_list =[x.encode('UTF8') for x in genre_list]

	return title, artist, genre_list


