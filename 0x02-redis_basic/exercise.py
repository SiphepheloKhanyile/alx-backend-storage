#!/usr/bin/env python3
"""
store an instance of the Redis client
"""
import uuid
from typing import Union, Optional, Callable
import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for counting calls.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for storing history.
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


class Cache:
    """
    Creates instance of Redis Client
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Args:
            data (typing.Any): data to be stored
        Returns:
            str: generated random key string
        """
        uuid_string: str = str(uuid.uuid4())
        self._redis.set(uuid_string, data)
        return uuid_string

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        """
        Args:
            key (str): The key associated with the data.
            fn (Optional[Callable]): A callable function to transform the
            retrieved data.
        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        value = self._redis.get(key)
        if fn and value is not None:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """
        Get a string from the cache.

        Args:
            key (str): The key associated with the string.

        Returns:
            str: The retrieved string.
        """
        value = self._redis.get(key)
        return value.decode('utf-8') if value else ""

    def get_int(self, key: str) -> int:
        """
        Get an integer from the cache.

        Args:
            key (str): The key associated with the integer.

        Returns:
            int: The retrieved integer.
        """
        value = self._redis.get(key)
        try:
            return int(value.decode('utf-8')) if value else 0
        except ValueError:
            return 0


def replay(method: Callable) -> None:
    """
    Replay the history of a function.

    Args:
        method (Callable): The function to be replayed.

    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name)
    if calls:
        calls = calls.decode("utf-8")
        print("{} was called {} times:".format(name, calls))
        inputs = cache.lrange(name + ":inputs", 0, -1)
        outputs = cache.lrange(name + ":outputs", 0, -1)
        for i, o in zip(inputs, outputs):
            print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                         o.decode('utf-8')))
    else:
        print("{} has not been called yet.".format(name))
