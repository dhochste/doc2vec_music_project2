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


api_name = 'freebase'
api_version = 'v1'
with open('../doc2vec_music_project2/credentials.json') as credentials_file:
    credentials = json.load(credentials_file)
api_key = credentials['google_api']['api_key']

service_url = 'https://www.googleapis.com/freebase/v1/mqlread'

def do_query(music_album_titles):

	# Create a mql query
	query_names_genres = [{
		"type": "music/album",
		"artist": None,
		"name": music_album_titles,
		"genre": None
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

    results_dict = defaultdict(dict)
    for item in response[u'result']:
        g[item[u'name']] = {'Artist': item[u'artist'], 'Genre': item[u'genre']}

    return results_dict