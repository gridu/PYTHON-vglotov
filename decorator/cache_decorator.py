import time
import logging

cache = {}
LOGGER = logging.getLogger()


def cache_usage(func, enable_logging=False):
    """Using dict as a cache for input values and function results"""

    def wrapper(arg):
        if arg in cache.keys():
            if enable_logging:
                LOGGER.info('Cache is used')
            return cache.get(arg)
        result = func(arg)
        cache[arg] = result
        if not enable_logging:
            LOGGER.info('Values are added to cache')
        return result

    return wrapper


def timer(func):
    """Prints the runtime of the decorated function"""

    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer
