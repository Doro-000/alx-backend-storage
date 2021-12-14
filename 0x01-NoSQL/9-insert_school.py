#!/usr/bin/env python3

"""
    Python function that inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
      implementation
    """
    insert_obj = mongo_collection.insert_one(kwargs)
    return insert_obj.inserted_id
