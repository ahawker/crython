"""
    crython/log
    ~~~~~~~~~~~

    Contains package logger.
"""
# pylint: disable=global-statement
import logging

ROOT_LOGGER = logging.getLogger(__package__)


def get_logger(name=None):
    """
    Get a logger instance relative to the crython package.
    """
    return ROOT_LOGGER.getChild(name)
