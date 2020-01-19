import time
import logging

cache = {}
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def cache_usage(func):
    """Using dict as a cache for input values and function results"""

    def wrapper(arg):
        if arg in cache.keys():
            LOGGER.warning('Cache is used for arg ' + str(arg))
            return cache[arg]
        cache[arg] = func(arg)
        LOGGER.warning('Cache is filled by new arg: ' + str(arg))
        return cache[arg]

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
