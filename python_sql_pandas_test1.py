
import os
import json

import pymysql as mdb
from pandas.io import sql


with open('credentials.json') as credentials_file:
	credentials = json.load(credentials_file)

passwd = credentials['mysql']['password']


conn = mdb.connect(host='localhost', 
	user = 'root', 
	passwd = passwd, 
	db = 'amazon_reviews_insight',
	autocommit = True)


sql_query = "SELECT * FROM test;"

result = sql.read_sql(sql_query, conn)
print result

conn.close()

