"""
Main function to load, re-organize, and save all of the Amazon album reviews dataframes.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/22/15
"""

import doc2vec_methods as dm
import cPickle as pickle




def main():
	# Set the path to the pickled file
	directory_path = '../../Lemmatized_by_Sentence/'
	# Loop through each df, convert to desired format, and pickle the new df

	file_path_base = 'amazon_music_random_lemmatized_'
	file_path_end = '.pandas'
	number_dfs = 22
	for i in range(number_dfs):
		# Load the original dfs
		file_path = file_path_base + str(i) + file_path_end
		df = dm.load_pickled_df(directory_path, file_path)

		# Adjust the df
		df = dm.df_column_reduce(df)
		df = dm.df_title_format(df)
		df = dm.df_review_collapse(df)

		# Pickle and save the adjust df
		pickle.dump( df, open( file_path, "wb"))

if __name__ == '__main__':
	main()