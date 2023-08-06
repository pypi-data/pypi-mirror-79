from argparse import ArgumentParser
from logging import getLogger, StreamHandler
from time import sleep
from importlib import import_module
from os import getenv
import sys
from signal import signal, SIGINT, SIGTERM

parser = ArgumentParser()
parser.add_argument("scheduler")
parser.add_argument("--sleep", type = float, default = 1.0)

_alive = True
def _exit(_sig, _frame):
    global _alive
    _alive = False

def run():
    logger = getLogger()
    logger.addHandler(StreamHandler())
    logger.setLevel(getenv("LOG_LEVEL", "INFO"))

    sys.path.insert(0, "")
    args = parser.parse_args()
    scheduler_module, scheduler_ref = args.scheduler.split(":")
    scheduler = import_module(scheduler_module).__getattribute__(scheduler_ref)

    signal(SIGINT, _exit)
    signal(SIGTERM, _exit)

    while True:
        if not _alive:
            break
        elif scheduler.run_next():
            pass
        else:
            sleep(args.sleep)

if __name__ == "__main__":
    run()