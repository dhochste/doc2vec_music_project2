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



"""
# Try a new class that call a mysql database
import os
import json
import pymysql as mdb
from pandas.io import sql

with open('credentials.json') as credentials_file:
	credentials = json.load(credentials_file)
passwd = credentials['mysql']['password']

conn = mdb.connect(host='localhost', user = 'root', passwd = passwd, db = 'amazon_reviews_insight', autocommit = True)

class LabeledReviewSentenceSQL(object):
	def __init__(self, dataframe):
		self.df = dataframe

	def __iter__(self):


# sql_query = "SELECT * FROM test;"

# result = sql.read_sql(sql_query, conn)
# print result
"""

