from functools import wraps
from pickle import dumps, loads
from base64 import b64decode, b64encode
from .logger import logger

class Job:
    def __init__(self, worker, fn, *, slug, qkwargs):
        self._worker = worker
        self._slug = slug
        self._fn = fn
        self._qkwargs = qkwargs

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

    def schedule(self, *args, **kwargs):
        pickled = dumps([self._slug, args, kwargs])
        encoded = b64encode(pickled).decode("utf-8")
        self._worker._queue.put(encoded, ** self._qkwargs)
        full_args = [str(x) for x in args]
        full_args.extend(f"{k}={v}" for k,v in kwargs.items())
        arg_str = ",".join(full_args)
        logger.info(f"Job: {self._slug} enqueued with args: ({arg_str}).")

class Worker:
    def __init__(self, queue, scheduler):
        self._queue = queue
        self._scheduler = scheduler
        self._jobs = dict()
        self._on_error = list()

    def on_error(self, fn):
        self._on_error.append(fn)
        return fn

    def job(self, *, slug = None, interval = None, ** qkwargs):
        def wrapper(fn):
            final_slug = ":".join([fn.__module__, fn.__name__]) if slug is None else slug
            job = wraps(fn)(Job(self, fn, slug = final_slug, qkwargs = qkwargs))
            self._jobs[final_slug] = job
            if interval is not None:
                self._scheduler.schedule(job.schedule, slug = final_slug, interval = interval)
            return job
        return wrapper

    def tick(self):
        while self._scheduler.run_next():
            pass

    def run_next(self):
        payload, id = self._queue.get()
        if id is None:
            return False
        decoded = b64decode(payload)
        slug, args, kwargs = loads(decoded)
        full_args = [str(x) for x in args]
        full_args.extend(f"{k}={v}" for k,v in kwargs.items())
        arg_str = ",".join(full_args)
        logger.info(f"Job: {slug} starting with args: ({arg_str}).")
        try:
            self._jobs[slug](*args, **kwargs)
            logger.info(f"Job: {slug} completed successfully.")
            self._queue.consume(id)
        except Exception as err:
            for hdlr in self._on_error:
                hdlr(slug, args, kwargs, err)
            logger.error(f"Job: {slug} failed.")
            logger.exception(err)
        return True