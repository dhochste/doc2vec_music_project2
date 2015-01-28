"""
Load each df chunk for amazon reviews (df_am) and for freebase data (df_fb)

David L. Hochstetler
1/28/15
"""

import doc2vec_methods as dm
import pandas as pd
import numpy as np
import time
import cPickle as pickle
import os
import re

import gensim, logging
from random import shuffle

import string
from nltk import sent_tokenize
from collections import defaultdict
# don't quite understand this config
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


if __name__ == '__main__':

	# Load the processed dfs
	directory_path = '../../Lemmatized_by_Sentence/processed_files/'
	new_dir_path = '../doc2vec_methods/'

	# Loop through each df
	##### TEMP #####
	# for fname in os.listdir(directory_path):
	for i in range(1):

		# Load df_am and df_fb
		fname_am = 'df_reviews_concat_' + str(i) +'.pandas'
		fname_fb = 'df_tag_' + str(i) +'.pd'

		print("Loading " + fname_am + " and " + fname_fb)
		df_am = dm.load_pickled_df(directory_path, fname_am)
		df_fb = dm.load_pickled_df(directory_path, fname_fb)

		# Remove the productId column, which isn't used
		df_am = df_am.drop(['productId'], axis=1, inPlace=False)

		# Remove [] and () from end of title names
		df_am['title'] = remove_brackets(df_am['title'])

		# drop duplicate rows (empty) and then get rid of row 0 which is empty
		df_fb.drop_duplicates('title',inplace=True)
		df_fb = df_fb[1:]

		# Merge the two dataframes
		df_merge = pd.merge(df_am, df_fb, how='left', left_on='title', right_on='title')
		del df_am
		del df_fb

		# Get rid of freebase api call artifacts
		df_merge['artist'] = df_merge['artist'].apply(convert_list_str)
		df_merge['artist'] = df_merge['artist'].apply(dm.convert_nan_str)
		df_merge['genre'] = df_merge['genre'].apply(dm.convert_strlist_list)

		# Final form: re-order columns
		df_merge = df_merge[ ['artist', 'title', 'genre', 'tokenized'] ]

		# Concat and save
		if i==0:
			print("Creating a new df_all")
			df_all = df_merge.copy()
		else:
			print("Concatenating df_all")
			df_all = pd.concat([df_all, df_merge])

			new_file = 'df_all_concat_' + str(i) + '.pandas'
			pickle.dump( df_concat, open( new_dir_path+new_file, "wb"))

		del df_merge
		print("Iteration {0}: pickling df_all".format(i))




