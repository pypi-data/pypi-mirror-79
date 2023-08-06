"""
This module contains the methods for the ``openxc-dump`` command line program.

`main` is executed when ``openxc-dump`` is run, and all other callables in this
module are internal only.
"""


import argparse
import time
import logging
import sys

from openxc.formats.json import JsonFormatter
from .common import device_options, configure_logging, select_device

import functools
print = functools.partial(print, flush=True)

def receive(message, **kwargs):
    message['timestamp'] = time.time()
    print((JsonFormatter.serialize(message)))


def parse_options():
    parser = argparse.ArgumentParser(
            description="View a raw OpenXC data stream",
            parents=[device_options()])

    arguments = parser.parse_args()
    return arguments


def main():
    try:
        configure_logging(logging.DEBUG)
        arguments = parse_options()
        source_class, source_kwargs = select_device(arguments)
        source = source_class(callback=receive, **source_kwargs)
        source.start()
        # TODO test this, I'd prefer it to the sleep loop
        while(True):
            source.join(0.1)
    except KeyboardInterrupt:
        sys.exit(0)
