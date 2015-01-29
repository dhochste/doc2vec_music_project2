"""
Contains functions for performing Doc2Vec on loaded database (dataframe or csv)

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/28/15

Thanks to Ben E for the Doc2Vec help!
"""

import numpy as np
import pandas as pd
import numexpr as ne 		# Used by pandas.query method
import sys
import re
import gensim, logging 		# For Doc2Vec
import math
import string


def create_artist_list(df):
	"""
	Extract list of artists from the dataframe with column 'artist'
	"""
	artist_list = []
	for index,row in df.iterrows():
	    artist = row['artist'].replace(' ','_')
	    if artist not in artist_list:
	        artist_list.append(artist)

	return artist_list


def create_genre_lookup(df):
	"""
	Create a dict of artist - list of genre classifications
	"""
	genre_lookup = {}
	for index,row in df.iterrows():
	    artist = row['artist'].replace(' ','_')
	    if row['genre'] != []:
	        if artist not in genre_lookup.keys():
	            genre_lookup[artist] = [v.replace(' ','_') for v in row['genre']]
	        else:
	            # add any new genre terms
	            new_set = set([v.replace(' ','_') for v in row['genre']])
	            genre_lookup[artist] = list(set(genre_lookup[artist]).union(new_set))
	return genre_lookup


def populate_artist_genres(artist_list, genre_lookup_dict): 
	""""
	Populate a list of artists with any genres that define them
	"""
    populated_list = []
    for artist in artist_list:
        if artist in music_genre_dict.keys():
        	populated_list.append(artist)
            populated_list.extend(music_genre_dict[artist]) # add the latent style into the search terms
        else:
            populated_list.append(artist)
    return populated_list


def most_similar_artists_w_genre(positive_terms=[], negative_terms=[], 
	artist_list=[], music_genre_lookup={}, doc2Vec_model = None,d2v_topn):
    """
    Returns a list of tuples: (artist, similarity score) given pos and
    neg input vocab, list of all artists, and an artist-genre dict.
    Uses a trained doc2vec_model as input.
    Based on similar method developed by Ben Everson. Thanks, Ben!
    """
    # populate the search terms with latent styles 
    positive_latent = populate_artist_genres(positive_terms, music_genre_lookup)
    negative_latent = populate_artist_genres(negative_terms, music_genre_lookup)
    all_search_terms = positive_latent + negative_latent
    print all_search_terms
    # find the array of distances for all terms
    distances = doc2Vec_model.most_similar(positive=positive_latent, negative=negative_latent, 
    	topn=d2v_topn)
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


def most_similar_artists_(positive_terms=[], negative_terms=[], 
	artist_list=[], doc2Vec_model = None, d2v_topn = 100):
    """
    Returns a list of tuples: (artist, similarity score) given pos and neg 
    input vocab and a list of all artists. Uses a trained doc2vec_model as input.
    Based on similar method developed by Ben Everson. Thanks, Ben!
    """
    all_search_terms = positive_terms+negative_terms
    # find the array of distances for all terms
    distances = doc2Vec_model.most_similar(positive=positive_terms, negative=negative_terms,
    	topn=d2v_topn)
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





