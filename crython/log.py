"""
    crython/log
    ~~~~~~~~~~~

    Contains package logger.
"""

import logging

from crython import compat


ROOT_LOGGER = None


if compat.py26:
    logging._loggerClass.getChild = lambda s, name: '{0}.{1}'.format(s.name, name)


def get_logger(name=None):
    global ROOT_LOGGER

    if ROOT_LOGGER is None:
        ROOT_LOGGER = logging.getLogger()

    name = '.'.join((ROOT_LOGGER.name, name)) if name else None
    return logging.getLogger(name)
