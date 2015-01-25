"""
Main function to load, re-organize, and save all of the Amazon album reviews dataframes.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/22/15
"""

import doc2vec_methods as dm
import pandas as pd
import cPickle as pickle
import time
from doc2vec_classes import LabeledReviewSentence
import gensim, logging 		# For Doc2Vec
import os



# # Pickle and save the adjust df
# new_file = 'df_reviews_' +str(i) +'.pandas'
# print("Saving pickled dataframe as " + new_file)
# new_file_path = directory_path + new_file
# pickle.dump( df, open( new_file_path, "wb"))

if __name__ == '__main__':
	# Set the path to the pickled file
	directory_path = '../../Lemmatized_by_Sentence/'
	# Loop through each df, convert to desired format, and pickle the new df

	file_path_base = 'amazon_music_random_lemmatized_'
	file_path_end = '.pandas'
	number_dfs = 22

	for i in range(number_dfs):
		t0 = time.time()
		# Load the original dfs
		# print("Loading original dataframe {0}".format(t1-t0))
		file_path = file_path_base + str(i) + file_path_end
		print("Loading " + file_path)
		df = dm.load_pickled_df(directory_path, file_path)

		# Adjust the df
		print("Processing dataframe")
		df.drop_duplicates(subset = df.columns[:-1],inplace=True)
		df = dm.df_column_reduce(df)
		df = dm.df_title_format(df)

		# Concat the dataframe with each new df loaded
		print("Adding df to df_all with concat")
		if i == 0:
			df_all = df.copy()

		else:
			df_all = pd.concat([df_all, df])

		t1 = time.time()
		print("Time iteration {0} was {1:.2f} seconds".format( i, (t1-t0) ))

	# Pickle and save the new, compiled df
	new_file = 'df_reviews_all.pandas'
	print("Saving pickled dataframe as " + new_file)
	new_file_path = directory_path + new_file
	t0 = time.time()
	pickle.dump( df_all, open( new_file_path, "wb"))
	t1 = time.time()
	print("Time to save pickled all was {0:.2f}".format(t1-t0))

	# Create and save the gensime Doc2Vec model
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	reviews = LabeledReviewSentence(df_all)

	num_workers = 4 # 4 on my macbook pro, may need to adjust for running on AWS
	t0 = time.time()
	model = gensim.models.Doc2Vec(reviews, workers=num_workers)
	t1 = time.time()
	print("Time to run Doc2Vec to generate model was {0:.2f}".format(t1-t0))

	# Save the model
	model_directory = '../doc2vec_models/'
	model_filename = 'model_all_01.doc2vec'
	t0 = time.time()
	model.save(model_directory+model_filename)
	t1 = time.time()
	print("Time to save Doc2Vec model was {0:.2f}".format(t1-t0))
	