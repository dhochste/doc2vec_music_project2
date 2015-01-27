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
		"artist": [],
		"name": album_title,
		"genre": [],
		"limit": limit
		}]

	opts = {"query": json.dumps(query_names_genres), "key": api_key}
	r = requests.get(service_url, params=opts)
	response = r.json()

	if u'error' in response:
		print 'Request failed. Return: '
		print response
		sys.exit(1)

	return response

def get_artist_genre(response):
	""""
	Get the artist, title, and genre from the response
	"""
	if response[u'result'] == []:
		artist = []
		title = []
		genre_list = []
		empty_flag = 1
	else:
		title = response[u'result'][0][u'name'].encode('UTF8')
		if response[u'result'][0][u'artist'] != []:
			artist = response[u'result'][0][u'artist'][0].encode('UTF8')
		else:
			artist = []
		if response[u'result'][0][u'genre'] != []:
			genre_list = response[u'result'][0][u'genre']
			genre_list =[genre.encode('UTF8') for genre in genre_list]
		else:
			genre_list = []
		empty_flag = 0

	return title, artist, genre_list, empty_flag


