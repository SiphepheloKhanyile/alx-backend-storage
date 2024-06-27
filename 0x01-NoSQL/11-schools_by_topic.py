#!/usr/bin/env python3
"""
Module: Task 11.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Args:
        mongo_collection (_type_): _description_
        topic (_type_): _description_
    Returns:
        list : _description_
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
