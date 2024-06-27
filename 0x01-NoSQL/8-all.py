#!/usr/bin/env python3
"""
function that lists all documents in a collection
"""
from pymongo import collection


def list_all(mongo_collection: collection.Collection):
    """
    Args:
        mongo_collection (collection.Collection):
    Returns:
        list
    """
    return [doc for doc in mongo_collection.find()]
