#!/usr/bin/env python3
"""
function that inserts a new document in a collection
based on kwargs
"""
from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs):
    """
    Args:
        mongo_collection (Collection): _description_
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
