

def model_music(input_string):
	# Load the model
	model_directory = '../doc2vec_models/'
	model_filename = 'model_01.doc2vec'
	model = Doc2Vec.load(model_directory+model_filename)

	# Look at results

	positive_terms = ['hard','rock']
	negative_terms = []
	results = model.most_similar_cosmul(positive= positive_terms, 
		negative=negative_terms, topn=10)

	return results