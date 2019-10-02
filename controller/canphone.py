#!python3

from canphone import CanController
import sys
import logging
import time
import signal


__logger = logging.getLogger("canphone")
__ctrl = CanController()


def on_term(signo, stack):
    __logger.info("Shutting down after receiving signal.")
    # stop controller
    __ctrl.stop()
    # kill main loop before quitting
    sys.exit(1)

def main():
    # configure logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    __logger.setLevel(logging.DEBUG)
    __logger.addHandler(ch)

    # start controller
    __ctrl.start()

    # register termination handlers
    signal.signal(signal.SIGINT, on_term)
    signal.signal(signal.SIGTERM, on_term)

    # simulate main loop
    time.sleep(500)

if __name__ == '__main__':
    sys.exit(main())
