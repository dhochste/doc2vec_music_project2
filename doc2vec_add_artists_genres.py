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
import freebase_api_query as faq
import pandas as pd
import cPickle as pickle
import os

from collections import defaultdict


if __name__ == '__main__':

	# Load the Freebase API info:
	with open('../doc2vec_music_project2/credentials.json') as credentials_file:
	    credentials = json.load(credentials_file)
	api_key = credentials['google_api']['api_key']
	service_url = 'https://www.googleapis.com/freebase/v1/mqlread'

	# Load the processed dfs
	directory_path = '../../Lemmatized_by_Sentence/processed_files/'

	# Loop through each df
	for fname in os.listdir(directory_path):
		path = os.path.join(directory_path, fname)
		# skip directories and files that aren't pickled pandas
		if os.path.isdir(path):
			continue
		elif os.path.splitext(path)[1] != ".pandas":
			continue
		
		print("Loading " + fname)
		df = dm.load_pickled_df(directory_path, fname)

		# Process the titles to remove extra [] and ()
		# i.e., (clean) or [vinyl]
		df['title'] = dm.remove_brackets(df['title'])

		#Find the unique titles in the df
		titles = pd.Series(df['title']).unique()

		# Remove the df from memory
		del df

		# iter through the unique titles and query for artist, genre
		t0 = time.time()
		title_artist_genre = []
		total_empty = 0
		total_none = 0
		count = 0
		err_log = []

		# deal with early stop from inital run
		if fname == 'df_reviews_concat_0.pandas':
			titles = titles[(1950+9973):]

		for title in titles:
			# avoid empty title at beginning
			if title == '':
				title_artist_genre.append(['','',''])
			else:
				response, err_flag = faq.do_query(title, service_url, api_key, 1)

				if err_flag:
					err_log.append([count, title])
					title_artist_genre.append([title,'',''])
					continue

				# print response

				if response is not None:
					cur_title,cur_artist, cur_genre, empty_flag = faq.get_artist_genre(response)
					title_artist_genre.append([cur_title,cur_artist,cur_genre])
					total_empty += empty_flag
				else:
					title_artist_genre.append([title,'',''])
					total_none += 1

			if count%1000 == 0:
				print("Iteration: {0}".format(count))
				print("Current number of emptys: {0}".format(total_empty))
				print("Current number of nones: {0}".format(total_none))

			count += 1
		
		t1 = time.time()
		print("Time for calling the freebase api was {0:.2f} seconds".format( t1-t0 ))

		print("The length of the titles list is {0}".format(len(titles)))	

		print("The length of the artists list is {0}".format(len(title_artist_genre)))

		print("The total number of empty artist/genre calls is {0}".format(total_empty))

		print("The total number of None responses to calls is {0}".format(total_none))

		# create new df with this unique info
		df_tag = pd.DataFrame(title_artist_genre, columns=['title','artist','genre'])

		# save the new data frame
		new_file = 'df_tag_' + os.path.splitext(path)[0][-1] + '.pandas'
		print("Pickling" + new_file)
		pickle.dump( df_tag, open( directory_path+new_file, "wb"))


	# Loop through each df
	# load the dataframe
	# Find unique titles - keep title indices
	# iter through unique titles and query for artist, genre
		# If more than one - only choose the first?
	# add the artist and genre columns to the df
	# save the updated data frame


