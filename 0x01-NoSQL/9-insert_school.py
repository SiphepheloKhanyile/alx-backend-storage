#!/usr/bin/env python3
"""
function that inserts a new document in a collection
based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Args:
        mongo_collection (Collection):
    Returns:
        list
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
