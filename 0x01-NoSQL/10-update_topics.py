#!/usr/bin/env python3
"""
function that changes all topics of a school document
based on the `name`
"""
from pymongo.collection import Collection
from typing import List


def update_topics(mongo_collection: Collection,
                  name: str, topics: List[str]) -> list:
    """
    Args:
        mongo_collection (Collection): _description_
        name (str): _description_
        topics (List[str]): _description_
    Returns:
        list: _description_
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
