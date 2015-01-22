"""
This file contains functions for scraping data from Amazon product pages.
Geared for Amazon albums.

Part of Project for Insight Data Science - Silicon Valley 2015a

David L. Hochstetler
1/21/15

"""

import re
import pandas as pd
from bs4 import BeautifulSoup
import urllib2
import contextlib
import requests


def amazon_urls_from_df(df):
	"""
	Load df. Expecting to have a productId column. Return a
	series with Amazon urls
	"""
	url_base = 'http://www.amazon.com/dp/'
	urls_col = df['productId'].map(lambda x: url_base + x )

	return urls_col


def amazon_title_genres_df(urls_col):
	"""
	Scrape the title, genre, subgenre, and subsubgenre from Amazon
	products at the urls in the given series. Create a df with those
	columns.
	"""

	df_title_genres = pd.DataFrame(columns = ['artist','genre',
		'subgenre','subsubgenre'])

	curr_url = urls_col[0]
	i = 0
	for url in urls_col:
		print("In amazon_title_genres_df - iter {0}".format(i))
		if i==0 or url != curr_url:
			tags_list = amazon_scrape_title_genres(url)
			# df_title_genres = pd.concat([df_title_genres,tags_list],axis=0)
			df_title_genres.loc[i] = tags_list
			curr_url == url
		elif url == curr_url:
			# df_title_genres = pd.concat([df_title_genres,tags_list],axis=0)
			df_title_genres.loc[i] = tags_list
		i+=1

	return df_title_genres


def amazon_scrape_title_genres(url):
	"""
	Scrape the title, genre, subgenre, and subsubgenre from Amazon
	products at the url given. Return these as a list.
	"""
	
	# with contextlib.closing(urllib2.urlopen(url)) as page:
	with contextlib.closing(requests.get(url)) as page:
		# soup = BeautifulSoup(page.read())
		soup = BeautifulSoup(page.text)

		titles = str(soup.title.string).split(" ")
    	title = titles[1][:-1]
    	genres_div = soup.find("div", {"id": "wayfinding-breadcrumbs_feature_div"})
    	# Get all 4 entries, but only want the last 3
    	# try:
    	if genres_div is not None: 
    		i= 0
    		genres = []
    		for genre_tag in genres_div.find_all("a",{"class": "a-link-normal a-color-tertiary"}):
    			if i>0:
    				tag = str(genre_tag.getText())
    				match = re.search(r'([\w]+[\s\w]*)\n', tag)
    				genres = genres + [ match.group(1) ]
				i+=1
			tags_list = [title] + genres
			print("Scraping Worked!")
		# except: #AttributeError, Argument:
		else:
			# print "AttributeError in amazon_scrape_title_genres. Will have empty row, ", Argument
			print("Problem with amazon_scrape_title_genres for iteration {0}".format(i))
	    	tags_list = ['','','','']

        # tags_list = [title, genres[0], genres[1], genres[2]] 

    	return tags_list



##
# Load series of Amazon product urls
# Loop through each page to
	# if url is same as previous, use previous values
	# else
	# open the page
	# read the page w/ bs4
	# get title
	# get genres

# From

#Put all the df files into a csv file

#Create a class to iterate over the complete csv.