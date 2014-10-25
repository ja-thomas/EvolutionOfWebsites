# -*- coding: utf-8 -*-
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
# or client = MongoClient('mongodb://localhost:27017/')

# you connect to the database you created with "use mydb"
db = client['EvoDATABASE']

# you connect to the collection you created with "db.testData.insert("something)"
pagesHTML_collection = db['pagesHTML']

dummy = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}


def SaveToDatabase(pageObject):
    pagesHTML_collection.insert(pageObject)
