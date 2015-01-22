"""
Main function to implement Doc2Vec.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/20/15

Much thanks to Matt P. and Ben E. for the dataframe and Doc2Vec help!
"""

import doc2vec_methods as dm
import scraping_methods as scrape
from doc2vec_classes import LabeledReviewSentence
import pdb					# For debugging
import sys
import re
import gensim, logging 		# For Doc2Vec
import time 				# For timing


if __name__ == '__main__':
	# Set the path to the pickled file
	directory_path = '../../Lemmatized_by_Sentence/'
	file_path = 'amazon_music_random_lemmatized_0.pandas'

	t0 = time.time()
	df_full = dm.load_pickled_df(directory_path, file_path)
	t1 = time.time()
	print("Time to run load_pickled_df was {0}".format(t1-t0))

	# Smaller to help with debugging (1000,10000,100000)
	df = df_full[:10000].copy(deep=True)

	# Get the df into desired format
	# NOTE: This assumes set/hard-coded columns and column names in each df
	t0 = time.time()
	df = dm.df_column_reduce(df)
	t1 = time.time()
	print("Time to run df_column_reducer was {0}".format(t1-t0))

	t0 = time.time()
	df = dm.df_title_format(df)
	t1 = time.time()
	print("Time to run df_title_format was {0}".format(t1-t0))

	# pdb.set_trace()

	t0 = time.time()
	df = dm.df_review_collapse(df)
	t1 = time.time()
	print("Time to run df_review_collapse was {0}".format(t1-t0))

	# Run Doc2Vec on the dataset of reviews
	# Not sure what this does...
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	reviews = LabeledReviewSentence(df)

	# pdb.set_trace()
	
	# Instantiate the doc2vec model
	# Want to know how long this training takes
	# Need to look into adjustable parameters...
	# --> SEE gensim site
	num_workers = 4 # 4 on my macbook pro, may need to adjust for running on AWS
	t0 = time.time()
	model = gensim.models.Doc2Vec(reviews, workers=num_workers)
	t1 = time.time()
	print("Time to run Doc2Vec to generate model was {0}".format(t1-t0))

	# Look at results
	positive_terms = ['hard','rock']
	negative_terms = []
	print model.most_similar_cosmul(positive= positive_terms, 
		negative=negative_terms, topn=10)

	# Check out only titles:
	title_scores = dm.most_similar_titles(df,positive_terms,negative_terms,model)








