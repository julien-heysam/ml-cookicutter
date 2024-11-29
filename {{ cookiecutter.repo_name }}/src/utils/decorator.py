import logging
from time import time

logger = logging.getLogger(__name__)


def timer_func(func):
    def wrap_func(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__!r} executed in {(time() - start):.4f}s")
        return result

    return wrap_func


def async_timer_func(func):
    async def wrap_func(*args, **kwargs):
        start = time()
        result = await func(*args, **kwargs)
        logger.info(f"Function {func.__name__!r} executed in {(time() - start):.4f}s")
        return result

    return wrap_func


def async_logging(func):
    async def wrap_func(*args, **kwargs):
        start = time()
        logger.info(f"[Start] Function:{func.__name__!r}")
        result = await func(*args, **kwargs)
        logger.info(f"[End] Function:{func.__name__!r}, Execution time:{(time() - start):.4f}s")
        return result

    return wrap_func


def logging(func):
    def wrap_func(*args, **kwargs):
        start = time()
        logger.info(f"[Start] Function:{func.__name__!r}")
        result = func(*args, **kwargs)
        logger.info(f"[End] Function:{func.__name__!r}, Execution time:{(time() - start):.4f}s")
        return result

    return wrap_func
