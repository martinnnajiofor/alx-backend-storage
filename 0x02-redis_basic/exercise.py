#!/usr/bin/env python3
""" Redis Basic
"""
import redis
from typing import Union, Callable, List, Optional
import uuid
import sys
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ In this exercise we will create a get method that take a key string argument and an optional Callable argument named fn. This callable will be used to convert the data back to the desired format. """
    key = method.__qualname__

    @wraps(method)
    def counter_wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return counter_wrapper


def call_history(method: Callable) -> Callable:
    """ In this task, we will define a call_history decorator to store the history of inputs and outputs for a particular function. Everytime the original function will be called, we will add its input parameters to one list in redis, and store its output into another list."""
    input_list_key = method.__qualname__ + ":inputs"
    output_list_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def set_history(self, *args, **kwargs):
        self._redis.rpush(input_list_key, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(output_list_key, str(res))
        return res

    return set_history

""" In this tasks, we will implement a replay function to display the history of calls of a particular function"""
def replay(method: Callable) -> None:
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print(f"{key} was called {count} times:")
    in_list = redis.lrange(inputs, 0, -1)
    out_list = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(in_list, out_list))
    for a, b in redis_zipped:
        attr, result = a.decode("utf-8"), b.decode("utf-8")
        print(f"{key}(*{attr}) -> {result}")


class Cache:
    """ Cache class
    """
    def __init__(self):
        """ Instantiate Redis """
        self._redis = redis.Redis(host="localhost", port=6379)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store any type of data in Redis """
        key = str(uuid.uuid4())
        self._redis[key] = data
        return key

    def get(self, key: str, fn: Optional[Callable] = None) ->\
            Union[str, bytes, int, float]:
        """ Get value in db, convert data back to desired format """
        return fn(self._redis.get(key)) if fn else self._redis.get(key)

    def get_str(self, b: bytes) -> str:
        """ Convert bytes to str """
        return b.decode('utf-8')

    def get_int(self, b: bytes) -> int:
        """ Convert bytes to int """
        return int.from_bytes(b, sys.byteorder)

    def get_list(self, k: str) -> List:
        """ Convert bytes from store to list """
        return self._redis.lrange(k, 0, -1)
