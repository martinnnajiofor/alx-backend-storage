#!/usr/bin/env python3
""" 11-schools_by_topic.py"""
from pymongo import MongoClient
def schools_by_topic(mongo_collection, topic):
    """function that returns the list of school having a specific topic"""
    query = { "topics": topic }
    schoolst = mongo_collection.find(query)
    return schoolst 
