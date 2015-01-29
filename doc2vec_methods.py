"""
This file contains functions for loading Amazon Music Reviews dataframes
and performing Doc2Vec on the reviews.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/20/15

Much thanks to Matt P. and Ben E. for the dataframe and Doc2Vec help!
"""


import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import numexpr as ne 		# Used by pandas.query method
import sys
import re
import gensim, logging 		# For Doc2Vec
import cPickle as pickle 	# Used for pickling/unpickling files
import math
import string


def load_pickled_df(directory_path, file_path):
    """
    Load the df from pickled pandas dataframe
    """

    file_0 = directory_path+file_path

    with open(file_0, 'rb') as pickle_file:
        df = pickle.load(pickle_file)

    return df


def df_filter_by_num_reviews(df,filter_num = 3):
	"""
	Filter out reviews with less than filter_num of reviews for an album
	"""

	# Sort by titlename
	df.sort(['title'], inplace=True)

	# Add a column of 1s, this will be used later to eliminate titles with only one song
	df['num_titles'] = pd.Series(np.ones((len(df)),dtype=np.int), index=df.index)

	# group by title
	df_titlegroup = df.groupby(['title'])
	# sum the number of titles
	temp = df_titlegroup[['num_titles']].transform(sum).sort('num_titles')
	# order by number of titles
	df = df.ix[ df_titlegroup[['num_titles']].transform(sum).sort('num_titles').index]
	# Keep and sort the titles with enough reviews
	df_filter = df[temp['num_titles']>=filter_num]
	df_filter.sort(['title'], inplace=True)
	# Drop the extra column
	df_filter.drop(['num_titles'],axis=1,inplace=True)

	return df_filter


def remove_brackets(list_of_strs):
	""""
	Removes anything in [ ] or ( ) at the end of a string.
	"""
	new_list =[]

	for string in list_of_strs:
		match = re.search(r'([^\[\(\)\]])*',string)

		if match is not None:
			new_string = match.group(0)
			if new_string == '' or new_string[-1] != ' ':
				new_list.append(match.group(0))
			elif new_string[-1] == ' ':
				new_list.append(match.group(0)[:-1])
				
		else:
			print "Warning: Unexpected non-match in remove_brackets()"
			print string

	return new_list

"""
Several small functions for text cleaning in dataframes
"""
def convert_list_str(x):
    if x == '[]':
        x = ''
    elif isinstance(x, list):
    	if x == []:
    		x = ''
    	else:
    		print("Warning: Unexpected List")
    return x

def convert_nan_str(x):
    if isinstance(x,float):
        if math.isnan(x):
            x = ''
    return x

def convert_nan_list(x):
    if x == np.nan:
        x = []
    return x

def convert_strlist_list(string_list):
    if isinstance(string_list, list):
        string_list = string_list
    elif string_list == '[]':
        string_list = []
    elif  isinstance(string_list, float):
        if math.isnan(string_list):
            string_list = []
    else:
        string_list = string.split(string_list[1:-1],", ")
        string_list = [v.replace("'", "") for v in string_list]
    return string_list


def df_column_reduce(df):
	"""
	Keep only relevant columns. Using hard-coded column names from Amazon database
	"""
	df = df.drop(['product/price','review/helpfulness','review/score','review/profileName',
		'review/summary','review/time','review/userId'],
		axis=1, inPlace=False)

	df.columns = ['productId','title','tokenized']

	return df


def df_title_format(df):
	"""
	Replace spaces with underscores
	"""
	df['title'].map(lambda title: title.replace(' ','_'))

	return df

def df_review_collapse(df):
	"""
	Apply aggregation so there is only 1 row per review (append the tokenize column 
	for previous multiple lines of df for a single review)
	"""

	review_rows_list = []
	working_row = []

	for i,row in df.iterrows():
		if i == 0:
			working_row = row
		
		else:
			if row[0] == working_row[0]: # same review, add tokenized sentence
				working_row[-1].extend(row[-1])

			else: # new review
				review_rows_list.append(working_row)
				working_row = row

	review_rows_list.append(working_row) #add the last working_row compilation
	df_reviews = pd.DataFrame(review_rows_list, columns=df.columns)

	""" OLD STUFF - TOO SLOW!!!
	df = df.groupby(list(df.columns[:-1])).agg({'tokenize':'sum'})
	df.reset_index(inplace=True)
	"""
	return df_reviews


def most_similar_artists(positive_terms=[], negative_terms=[], artist_list=[], music_genre_lookup={}, doc2Vec_model = None):
    """
    Returns a list of tuples: (artist, similarity score) given pos and
    neg imput vocab, list of all artists, and an artist-genre dict.
    Uses a trained doc2vec_model as input.
    Based on similar method developed by Ben Everson. Thanks, Ben!
    """
    # populate the search terms with latent styles 
    positive_latent = populate_latent_styles(positive_terms, music_genre_lookup)
    negative_latent = populate_latent_styles(negative_terms, music_genre_lookup)
    all_search_terms = positive_latent + negative_latent
    print all_search_terms
    # find the array of distances for all terms
    distances = doc2Vec_model.most_similar(positive=positive_latent, negative=negative_latent, topn=None)
    # sort array and convert to indices, rather than raw values (which are returned)
    best_distance_indices = np.argsort(distances)[::-1]
    # build a dict of artists with assosciated distances
    artists = []
    for dist_index in best_distance_indices:
        vocab_word = doc2Vec_model.index2word[dist_index] 
        # if the word is an artist, and not one we searched for
        if vocab_word in artist_list and vocab_word not in all_search_terms: 
            artists.append((vocab_word, float(distances[dist_index]))) # assign the score to the entry
    return artists





