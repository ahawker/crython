"""
    crython/log
    ~~~~~~~~~~~

    Contains package logger.
"""

import logging


ROOT_LOGGER = None


def get_logger(name=None):
    global ROOT_LOGGER

    if ROOT_LOGGER is None:
        ROOT_LOGGER = logging.getLogger()

    return ROOT_LOGGER.getChild(name)
