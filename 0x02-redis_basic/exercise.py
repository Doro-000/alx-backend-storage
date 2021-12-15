#!/usr/bin/env python3
"""
Writing strings to Redis
"""

import redis
from uuid import uuid4
from typing import Callable, Union
from functools import wraps


class Cache:
    """
    Cache class to handle caching using redis
    """

    def __init__(self):
        """
        Initialization
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        """
        decorator to count how many times a function has been called
        """
        @wraps(method)
        def incr(self, *args, **kwargs):
            """
            increments the count
            """
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
        return incr

    def call_history(method: Callable) -> Callable:
        """
        decorator to store input and output history of a method
        """
        @wraps(method)
        def store_history(self, *args, **kwargs):
            """
            stores input and output to redis
            """
            self._redis.rpush(method.__qualname__ + ":inputs", str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(method.__qualname__ + ":outputs", str(result))
            return result
        return store_history

    @call_history
    @count_calls
    def store(self, data: Union[int, float, bytes, str]) -> str:
        """
        stores data in redis using a random key and data as value
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """
        Get value of key from redis, fn to convert the return to desired type
        """
        val = self._redis.get(key)
        if fn:
            return fn(val)
        return val

    def get_str(self, key: str):
        """
        Get value of key from redis, return the value as a string
        """
        def strFunc(byteObj): return byteObj.decode("utf-8")
        return self.get(key, strFunc)

    def get_int(self, key: str):
        """
        Get value of key from redis, return the value as an int
        """
        return self.get(key, int)


def replay(function: callable):
    """
    replays the call history of a function
    """
    my_redis = redis.Redis()
    input_key = function.__qualname__ + ":inputs"
    output_key = function.__qualname__ + ":outputs"
    inputs = my_redis.lrange(input_key, 0, -1)
    outputs = my_redis.lrange(output_key, 0, -1)
    print(
        "{} was called {} times:".format(
            function.__qualname__,
            my_redis.llen(input_key)))
    for op in zip(inputs, outputs):
        print("function.__qualname__({}) -> {}".format(op[0], op[1]))