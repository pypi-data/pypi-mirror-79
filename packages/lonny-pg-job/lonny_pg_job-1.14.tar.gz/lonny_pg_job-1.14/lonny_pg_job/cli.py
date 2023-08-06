from argparse import ArgumentParser
from logging import getLogger, StreamHandler
from time import sleep
from importlib import import_module
from os import getenv
import sys
from lonny_proc import Manager, Context
from signal import signal, SIGINT, SIGTERM

parser = ArgumentParser()
parser.add_argument("worker")
parser.add_argument("--workers", type = int, default = 1)
parser.add_argument("--sleep", type = float, default = 1.0)

def _exit(_sig, _frame):
    exit()

def run():
    logger = getLogger()
    logger.addHandler(StreamHandler())
    logger.setLevel(getenv("LOG_LEVEL", "INFO"))

    sys.path.insert(0, "")
    args = parser.parse_args()
    worker_module, worker_ref = args.worker.split(":")
    worker = import_module(worker_module).__getattribute__(worker_ref)

    signal(SIGINT, _exit)
    signal(SIGTERM, _exit)

    def _target():
        while Context.alive:
            while worker.run_next():
                pass
            sleep(args.sleep)

    with Manager() as mgr:
        for _ in range(args.workers):
            mgr.add(_target)
        while True:
            mgr.tick()
            sleep(args.sleep)

if __name__ == "__main__":
    run()