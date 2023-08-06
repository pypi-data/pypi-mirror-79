from functools import wraps
from pickle import dumps, loads
from base64 import b64decode, b64encode
from .logger import logger

class Job:
    def __init__(self, worker, slug, fn):
        self._worker = worker
        self._slug = slug
        self._fn = fn

    def __call__(self, *args, **kwargs):
        return self._worker._put_job(self._slug, args, kwargs)

    def now(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

class Worker:
    def __init__(self, queue):
        self._queue = queue
        self._jobs = dict()

    def _get_job(self):
        payload = self._queue.get()
        if payload is None:
            return None
        decoded = b64decode(payload)
        return loads(decoded)

    def _put_job(self, slug, args, kwargs):
        pickled = dumps([slug, args, kwargs])
        encoded = b64encode(pickled).decode("utf-8")
        self._queue.put(encoded)

    def job(self, slug = None):
        def wrapper(fn):
            final_slug = ":".join([fn.__module__, fn.__name__]) if slug is None else slug
            self._jobs[final_slug] = fn
            return wraps(fn)(Job(self, final_slug, fn))
        return wrapper

    def __call__(self):
        next_job = self._get_job()
        if next_job is None:
            return False
        slug, args, kwargs = next_job
        if slug not in self._jobs:
            logger.warn(f"Function: {slug} is not defined.")
            return True
        full_args = list()
        full_args.extend(str(x) for x in args)
        full_args.extend(f"{k}={v}" for k,v in kwargs.items())
        args_str = ",".join(full_args)
        try:
            logger.info(f"Function: {slug} is starting with arguments: {args_str}")
            self._jobs[slug](*args, **kwargs)
            logger.info(f"Function: {slug} completed successfully.")
        except Exception as err:
            logger.error(f"Function: {slug} failed to complete")
            logger.exception(err)
        return True