"""
Run the model on the entire data set.

David L. Hochstetler

"""


from doc2vec_classes import LabeledReviewSentence
import doc2vec_methods as dm
import doc2vec_model_methods as dmm
import pandas as pd
import cPickle as pickle
import time
import gensim, logging 		# For Doc2Vec
import os
import sys
import pdb

if __name__ == '__main__':

	# Load the massive df
	dir_path = '../doc2vec_models/'
	file_name = 'df_all_concat_4.pandsa'

	t0 = time.time()
	df = dm.load_pickled_df(df_path, file_name)
	t1 = time.time()
	print("Time to load pickled: {0:.2f}".format(t1-t0))

	# Set up iterators for the model

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	# reviews_title = LabeledTitleReview(df)
	reviews_artist = LabeledArtistReview(df)
	reviews_title_artist = LabeledTitleArtistReview(df)
	reviews_all = LabeledAllReview(df)

	# Build the model
	num_workers = 4
	
	pdb.set_trace()
	# model_title = gensim.models.Doc2Vec(reviews_title, workers=num_workers, 
	# 	alpha=0.025, min_alpha=0.025)

	t0 = time.time()
	model_artist = gensim.models.Doc2Vec(reviews_artist, workers=num_workers, 
		alpha=0.025, min_alpha=0.025)
	t1 = time.time()
	print("Time to run Doc2Vec to generate artist model was {0:.2f}".format(t1-t0))

	pdb.set_trace()

	t0 = time.time()
	model_artist.save(dir_path +'doc2vec_model_artist.doc2vec')
	t1 = time.time()
	print("Time to save: {0:.2f}".format(t1-t0))

	pdb.set_trace()

	t0 = time.time()
	model_title_artist = gensim.models.Doc2Vec(reviews_title_artist, workers=num_workers, 
		alpha=0.025, min_alpha=0.025)
	t1 = time.time()
	print("Time to run Doc2Vec to generate artist model was {0:.2f}".format(t1-t0))

	t0 = time.time()
	model_title_artist.save(dir_path +'doc2vec_model_title_artist.doc2vec')
	t1 = time.time()
	print("Time to save: {0:.2f}".format(t1-t0))

	t0 = time.time()
	model_all = gensim.models.Doc2Vec(reviews_all, workers=num_workers, 
		alpha=0.025, min_alpha=0.025)
	t1 = time.time()
	print("Time to run Doc2Vec to generate artist model was {0:.2f}".format(t1-t0))

	t0 = time.time()
	model_title_artist.save(dir_path +'doc2vec_model_title_artist.doc2vec')
	t1 = time.time()
	print("Time to save: {0:.2f}".format(t1-t0))












