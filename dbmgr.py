'''
Created on Feb 22, 2016

@author: Alex
'''
from pymongo import MongoClient

try:
    client = MongoClient("mongodb://ec2-54-169-84-199.ap-southeast-1.compute.amazonaws.com:27017")
    print("testing connection...")
    print (client.database_names())
    db = client.douban
    print ("connected")
    
except ValueError as detail:
    print ("Error when connecting to db"+str(detail))

def insert_many(to_insert):
    try:
        result = db.books.insert_many(to_insert)
    except Exception as e:
        insert_many(to_insert)
        print (e)
#         for item in to_insert:
#             db.books.insert(item)
    



