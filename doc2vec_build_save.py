"""
Main function to implement Doc2Vec on entire set of Amazon music album reviews
stored in dataframes.

Load, re-organize, and concatenate all of the Amazon album reviews dataframes.

Build a Doc2Vec model using the entire dataframe set.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/22/15
"""

import doc2vec_methods as dm
import cPickle as pickle
import pandas as pd
from doc2vec_classes import LabeledReviewSentence
import pdb					# For debugging
import re
import gensim, logging 		# For Doc2Vec
import time 				# For timing


if __name__ == '__main__':
	# Set the path to the pickled file
	directory_path = '../../Lemmatized_by_Sentence/'
	# Loop through each df, convert to desired format, and pickle the new df

	# load pickled df: Hard-coded formatted file.
	df_all = dm.load_pickled_df(directory_path,'df_reviews_01.pandas')

	# Run Doc2Vec on the dataset of reviews
	# Not sure what this does...
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	reviews = LabeledReviewSentence(df_all)

	# pdb.set_trace()
	
	# Instantiate the doc2vec model
	# Want to know how long this training takes
	# Need to look into adjustable parameters...
	""" FROM RADIM REHUREK TUTORIAL -- LOOK INTO THIS LATER (Also see gensim site)
	model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate (OR ADJUST)
	model.build_vocab(reviews)
	for epoch in range(10): #adjust number of epochs (more = better??)
		model.train(reviews)
    	model.alpha -= 0.002  # decrease the learning rate
    	model.min_alpha = model.alpha  # fix the learning rate, no decay

	"""

	num_workers = 4 # 4 on my macbook pro, may need to adjust for running on AWS
	t0 = time.time()
	model = gensim.models.Doc2Vec(reviews, workers=num_workers)
	t1 = time.time()
	time_model_gen_all_reviews = t1-t0
	print("Time to run Doc2Vec to generate model using all reviews was {0}".format(t1-t0))

	# Save the model
	model_directory = '../doc2vec_models/'
	model_filename = 'model_01.doc2vec'
	model.save(model_directory+model_filename)
