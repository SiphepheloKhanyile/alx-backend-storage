#!/usr/bin/env python3
"""
store an instance of the Redis client
"""
import uuid
import typing
import redis


class Cache:
    """
    Creates instance of Redis Client
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: typing.Any) -> str:
        """
        Args:
            data (typing.Any): data to be stored
        Returns:
            str: generated random key string
        """
        uuid_string: str = str(uuid.uuid4())
        self._redis.set(uuid_string, data)
        return uuid_string
