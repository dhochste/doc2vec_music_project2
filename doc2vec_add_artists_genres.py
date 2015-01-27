"""
Main program for  querying Google's freebase API, getting titles and genres,
and adding to the database.

David L. Hochstetler
1/26/15
"""

import json
import requests
import sys
import time
import doc2vec_methods as dm
import pandas as pd
import cPickle as pickle

from collections import defaultdict


if __name__ == '__main__':

	# Load the Freebase API info:
	with open('../doc2vec_music_project2/credentials.json') as credentials_file:
	    credentials = json.load(credentials_file)
	api_key = credentials['google_api']['api_key']
	service_url = 'https://www.googleapis.com/freebase/v1/mqlread'

	#Start with the smallest of the concated dfs

	# Load the original dfs
	directory_path = '../../Lemmatized_by_Sentence/processed_files/'
	fname = 'df_reviews_concat_4.pandas'
	print("Loading " + fname)
	df = dm.load_pickled_df(directory_path, fname)

	#Find the unique titles in the df







	# Loop through each df

	# load the dataframe

	# Find unique titles - keep title indices

	# iter through unique titles and query for artist, genre
		# If more than one - only choose the first?

	# add the artist and genre columns to the df

	# save the updated data frame


