#!/usr/bin/env python3
""" returns all students sorted by average score """

from pymongo import MongoClient


def top_students(mongo_collection):
    """ main function """
    aggre = [
        { "$unwind" : '$topics' },
        ]
    main = [x for x in mongo_collection.aggregate(aggre)]
    print(main)
