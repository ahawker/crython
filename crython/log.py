"""
    crython/log
    ~~~~~~~~~~~

    Contains package logger.
"""
# pylint: disable=global-statement
import logging

ROOT_LOGGER = None


def get_logger(name=None):
    """
    Get a logger instance relative to the crython package.
    """
    global ROOT_LOGGER

    if ROOT_LOGGER is None:
        ROOT_LOGGER = logging.getLogger()

    name = '.'.join((ROOT_LOGGER.name, name)) if name else None
    return logging.getLogger(name)
