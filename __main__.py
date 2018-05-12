'''
Created on Feb 22, 2016

@author: Alex
'''
from scraper import scrape, write_to_db
from dbmgr import *

ENDPOINT = "https://api.douban.com/v2/book/search"

scrape(ENDPOINT)
# write_to_db()

