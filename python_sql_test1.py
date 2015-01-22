
import os
import json

import pymysql as mdb

with open('credentials.json') as credentials_file:
	credentials = json.load(credentials_file)

passwd = credentials['mysql']['password']


conn = mdb.connect(host='localhost', 
	user = 'root', 
	passwd = passwd, 
	db = 'amazon_reviews_insight',
	autocommit = True)

cur =conn.cursor()


sql_command = "SELECT * FROM test;"

cur.execute(sql_command)
result =cur.fetchall()
print result[0][1]

cur.close()
conn.close()

