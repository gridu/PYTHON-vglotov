import time
import logging

cache = {}
logging.basicConfig(
    format='[%(asctime)s:%(levelname)s] %(message)s',
    level=logging.DEBUG,
    datefmt='%I:%M:%S')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def cache_usage(enable_logging=False):
    """Using dict as a cache for input values and function results"""

    def real_decorator(f):

        def wrapper(arg):
            if arg in cache:
                if enable_logging:
                    LOGGER.warning('Cache is used for arg ' + str(arg))
                return cache.get(arg)
            result = f(arg)
            cache[arg] = result
            if enable_logging:
                LOGGER.warning('Cache is filled by new arg: ' + str(arg))
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
        LOGGER.warning(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer
