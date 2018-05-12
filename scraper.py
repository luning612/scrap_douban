# -*- coding: utf-8 -*-
'''
Created on Feb 22, 2016

@author: Alex
'''
import bs4
import requests
import sys
import json
from datetime import datetime
from dbmgr import insert_many
import random
import string

slug = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
output_path = "douban-books-"+ slug

books = []
current_time = lambda : str(datetime.now())

def process_tags(tags_complx):
    tags = []
    for tag in tags_complx:
        tags.append(tag["name"])
    return tags
def scrape(endpoint,**kwargs):
    # endpoint = kwargs.get("endpoint","api.douban.com/v2/book/search")
    
    global books
    #
    print("{0}\tstarted scraping".format(current_time()))
    #
    count = kwargs.get("count",100)
    num_iter = kwargs.get("num_iter",500)
    start_iter =kwargs.get("start_iter",199)
    tag=kwargs.get("tag","小说")
    #
    for itr in range(start_iter,num_iter):
        data={"count":count,"tag":tag,"start":count*itr}
        #try:
        json_response = requests.get(endpoint, data)
        response =json_response.json()
        #
        books = response["books"]
        if len(books)==0: break
        # print str(books)
        try:
            first_book_obj = books[0]["title"]
            first_book = json.dumps(first_book_obj).decode("unicode-escape")
            print (first_book)
        except KeyError:
            first_book = None
        print ("{0} |num_iter: {1}|# books: {2}".format(current_time(),str(itr)+" of "+str(num_iter),
                                                       len(books)))
        for book in books:
            useless_attr = ["binding","author_intro","series"]
            for attr in useless_attr:
                if attr in book: del (book[attr])
            book["rating"]["average"] = float(book["rating"]["average"])
            # book["price"] = float(book["price"][0:-1])
            book["tags"] = process_tags(book["tags"])
        #except ValueError as detail:
        #    print "ValueError in iter : {0}|{1}".format(str(itr), str(detail))
        #except:
        #    print "unexpected error"+ str(sys.exc_info())
        write_to_db()
        #write(output_path+"-"+str(itr)+".json")
        
    print("{0}\tended scraping".format(current_time()))
def write_to_db():
    global books
    if books:
        insert_many(books)
    books = []
def write(path):
    with open(path, 'wb') as f:
        f.write(json.dumps(books, sort_keys=True))
