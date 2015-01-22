"""
Contains classes used with Doc2Vec

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/20/15

Much thanks to Matt P. and Ben E. for the dataframe and Doc2Vec help!
"""

import numpy as np
import pandas as pd
import numexpr as ne 		# Used by pandas.query method
import sys
import re
import gensim, logging 		# For Doc2Vec


class LabeledReviewSentence(object):
    def __init__(self, dataframe):
        self.df = dataframe
        
    def __iter__(self):
        
        for index,row in self.df.iterrows():
            title = row['title']
            sentence = row['tokenize']
            yield gensim.models.doc2vec.LabeledSentence(words=sentence, labels=[title])

