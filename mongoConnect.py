# -*- coding: utf-8 -*-
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
# or client = MongoClient('mongodb://localhost:27017/')


db = client['EvoDATABASE']
