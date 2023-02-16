#!/usr/bin/env python3
"""Python function that inserts a new document in a collection based on kwargs"""
from pymongo import MongoClient
def insert_school(mongo_collection, **kwargs):
    """function that inserts a new document in a collection"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    result = mongo_collection.insert_one(kwargs)
    return result.