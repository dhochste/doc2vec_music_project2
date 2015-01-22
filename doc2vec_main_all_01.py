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



if __name__ == '__main__':
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

		# Concat (add on) the dataframe
		if i == 0:
			df_all = df.copy(deep=True)
		else:
			df_all = pd.concat([df_all, df])

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
	model_filename = 'model_all_01.doc2vec'
	model.save(model_directory+model_filename)
