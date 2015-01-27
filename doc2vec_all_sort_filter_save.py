"""
Main function to load, process, sort and save all of the Amazon album reviews dataframes.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/22/15
"""

import doc2vec_methods as dm
import pandas as pd
import cPickle as pickle
import time
# from doc2vec_classes import LabeledReviewSentence
# import gensim, logging 		# For Doc2Vec
import os
# import sys
# import csv


# # Pickle and save the adjust df
# new_file = 'df_reviews_' +str(i) +'.pandas'
# print("Saving pickled dataframe as " + new_file)
# new_file_path = directory_path + new_file
# pickle.dump( df, open( new_file_path, "wb"))

if __name__ == '__main__':
	# Set the path to the pickled files
	directory_path = '../../Lemmatized_by_Sentence/'
	new_dir_path = directory_path + 'processed_files/'
	file_path_csv = new_dir_path + 'df_reviews_all.csv'


	# Loop through each df, convert to desired format, and pickle the new df
	i = 0
	concat_count = 0
	for fname in os.listdir(directory_path):
		path = os.path.join(directory_path, fname)
		# skip directories and files that aren't pickled pandas
		if os.path.isdir(path):
			continue
		elif os.path.splitext(path)[1] != ".pandas":
			continue


		t0 = time.time()
		# Load the original dfs
		print("Loading " + fname)
		df = dm.load_pickled_df(directory_path, fname)

		# Get rid of row duplicates, unnecessary columns, and 
		print("Processing dataframe")
		df.drop_duplicates(subset = df.columns[:-1],inplace=True)
		df = dm.df_column_reduce(df)
		# df = dm.df_title_format(df) # For now, let's leave the titles as is (for artist api purposes)

		# Group by title in order to filter out titles with less than 2 reviews
		print("Filtering dataframe")
		df = dm.df_filter_by_num_reviews(df, 3)

		# Add df to csv file
		print("Writing to csv file")
		if i == 0:
			df.to_csv(path_or_buf = file_path_csv, header=True, index=False)
		else:
			df.to_csv(path_or_buf = file_path_csv, mode='a', header=False, index=False)

		# Concat the dataframe for up to 5 times, then create a new dataframe
		if i%5 == 0:
			print("Creating a new df_concat")
			df_concat = df.copy()
		elif i%5 == 4:
			print("Concatenating df and pickling df")
			df_concat = pd.concat([df_concat, df])

			new_file = 'df_reviews_concat_' + str(concat_count) + '.pandas'
			pickle.dump( df_concat, open( new_dir_path+new_file, "wb"))
			concat_count += 1
			del df_concat
		else:
			print("Concatenating df")
			df_concat = pd.concat([df_concat, df])

		del df

		t1 = time.time()
		print("Time for iteration {0} was {1:.2f} seconds".format( i, (t1-t0) ))
		i+=1
	

