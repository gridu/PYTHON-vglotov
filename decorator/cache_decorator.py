import time
import logging

from functools import wraps

CACHE = {}
logging.basicConfig(
    format='[%(asctime)s : %(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%I:%M:%S')
LOGGER = logging.getLogger()


def cache_usage(enable_logging=False):
    """Using dict as a cache for input values and function results"""

    def real_decorator(func):

        @wraps(func)
        def wrapper(arg):
            if arg in CACHE:
                if enable_logging:
                    LOGGER.info('Cache is used for arg %s in method: \'%s\'',
                                str(arg), func.__name__)
                return CACHE.get(arg)
            result = func(arg)
            CACHE[arg] = result
            if enable_logging:
                LOGGER.info('Cache is filled by new arg %s in method: \'%s\'',
                            str(arg), func.__name__)
            return result

        return wrapper

    return real_decorator


def timer(func):
    """Prints the runtime of the decorated function"""

    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        LOGGER.info(f'Finished method {func.__name__!r} in {run_time:.4f} secs')
        return value

    return wrapper_timer
