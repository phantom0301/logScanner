#! /usr/bin/env python
# coding: utf-8
"""
函数性能测试
"""

import time
from functools import wraps

def per_mon(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s seconds" %str(t1-t0))
        return result
    return function_timer

