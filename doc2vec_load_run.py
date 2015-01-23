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
from doc2vec_classes import LabeledReviewSentence
import pdb					# For debugging
import re
import gensim, logging 		# For Doc2Vec
import time 				# For timing


if __name__ == '__main__':

	# Load the model
	model_directory = '../doc2vec_models/'
	model_filename = 'model_01.doc2vec'
	model = gensim.models.Doc2Vec.load(model_directory+model_filename)

	# Look at results
	positive_terms = ['hard','rock']
	negative_terms = []
	print model.most_similar_cosmul(positive= positive_terms, 
		negative=negative_terms, topn=10)

	# Run Doc2Vec on the dataset of reviews
	# Not sure what this does...
	# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
