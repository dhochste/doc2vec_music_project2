"""
Contains classes used with Doc2Vec

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/20/15

Much thanks to Matt P. and Ben E. for the dataframe and Doc2Vec help!
"""

import numpy as np
import pandas as pd
import numexpr as ne 		# Used by pandas.query method
import sys
import re
import gensim, logging 		# For Doc2Vec



class LabeledTitleReview(object):
    def __init__(self, dataframe):
        self.df = dataframe
        
    def __iter__(self):
        
        for index,row in self.df.iterrows():
            title = row['title'].replace(' ','_')
            review = row['tokenized']
            yield gensim.models.doc2vec.LabeledSentence(words=review, labels=[title])


class LabeledArtistReview(object):
    def __init__(self, dataframe):
        self.df = dataframe
        
    def __iter__(self):
        
        for index,row in self.df.iterrows():
            artist = row['artist'].replace(' ','_')
            review = row['tokenized']
            yield gensim.models.doc2vec.LabeledSentence(words=review, labels=[artist])


class LabeledTitleArtistReview(object):
    def __init__(self, dataframe):
        self.df = dataframe
        
    def __iter__(self):
        
        for index,row in self.df.iterrows():
            title = row['title'].replace(' ','_')
            artist = row['artist'].replace(' ','_')
            review = row['tokenized']
            yield gensim.models.doc2vec.LabeledSentence(words=review, labels=[title, artist])


class LabeledAllReview(object):
    def __init__(self, dataframe):
        self.df = dataframe
        
    def __iter__(self):
        
        for index,row in self.df.iterrows():
            title = row['title'].replace(' ','_')
            artist = row['artist'].replace(' ','_')
            genre = [v.replace(' ','_') for v in row['genre']]
            review = row['tokenized']
            yield gensim.models.doc2vec.LabeledSentence(words=review, labels=[title, artist].extend(genre))



# # create a function to return a list of tuples: (beer name, similarity score)
# # an extension of the doc2vec most_similar_n method
# def most_similar_artists(positive_terms=[], negative_terms=[], artist_list=[], music_genre_lookup={}, doc2Vec_model = None):
#     """
#     Returns a list of tuples: (artist, similarity score) given pos and
#     neg imput vocab, list of all artists, and an artist-genre dict.
#     Uses a trained doc2vec_model as input
#     """
#     # populate the search terms with latent styles 
#     positive_latent = populate_latent_styles(positive_terms, beer_style_lookup)
#     negative_latent = populate_latent_styles(negative_terms, beer_style_lookup)
#     all_search_terms = positive_latent + negative_latent
#     print all_search_terms
#     # find the array of distances for all terms
#     distances = doc2Vec_model.most_similar(positive=positive_latent, negative=negative_latent, topn=None)
#     # sort array and convert to indices, rather than raw values (which are returned)
#     best_distance_indices = np.argsort(distances)[::-1]
#     # build a dict of artists with assosciated distances
#     artists = []
#     for dist_index in best_distance_indices:
#         vocab_word = doc2Vec_model.index2word[dist_index] 
#         # if the word is an artist, and not one we searched for
#         if vocab_word in artist_list and vocab_word not in all_search_terms: 
#             artists.append((vocab_word, float(distances[dist_index]))) # assign the score to the entry
#     return artists


"""
# Try a new class that call a mysql database
import os
import json
import pymysql as mdb
from pandas.io import sql

with open('credentials.json') as credentials_file:
	credentials = json.load(credentials_file)
passwd = credentials['mysql']['password']

conn = mdb.connect(host='localhost', user = 'root', passwd = passwd, db = 'amazon_reviews_insight', autocommit = True)

class LabeledReviewSentenceSQL(object):
	def __init__(self, dataframe):
		self.df = dataframe

	def __iter__(self):


# sql_query = "SELECT * FROM test;"

# result = sql.read_sql(sql_query, conn)
# print result
"""

