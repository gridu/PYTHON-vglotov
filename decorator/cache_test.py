import inspect

from cache_decorator import timer, cache_usage, cache


# @timer
# @cache_usage
def factorial(n):
    if n < 2:
        return 1
    return factorial(n - 1) * n


factorial(4)
factorial(2)
factorial(4)
factorial(2)
