#!/usr/bin/env python3

"""
    function that changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
      implementation
    """
    insert_obj = mongo_collection.update(
        {"name": name}, {"$set": {"topics": topics}})
    return insert_obj.inserted_id
