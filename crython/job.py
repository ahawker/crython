"""
    crython/job
    ~~~~~~~~~~~

    Contains functionality for defining functions that should be executed.
"""
from __future__ import unicode_literals

import functools

from crython import expression, field, tab


def job(*args, **kwargs):
    """
    Decorate functions to execute them in the background at a scheduled time.

    :param args: Positional args to pass to the decorated function.
    :param kwargs: Keyword args that contain job configuration and values to be passed to the decorated function.
    """
    # Pop out known kwargs that are `crython` specific.
    crontab = kwargs.pop('tab', tab.default_tab)
    ctx = kwargs.pop('ctx', tab.DEFAULT_EXECUTION_CONTEXT)
    on_success = kwargs.pop('on_success', lambda context: None)
    on_failure = kwargs.pop('on_failure', lambda context: None)
    expr = kwargs.pop('expr', None)
    fields = dict((k, kwargs.pop(k)) for k in kwargs.keys() if k in field.NAMES)

    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            try:
                return on_success(func(*args, **kwargs))
            except Exception as e:
                return on_failure(e)

        # Attach metadata to the decorated function that is consumed by the :class:`~crython.tab.CronTab`
        # instance it's registered with.
        wrapper.cron_expression = expression.CronExpression.new(expr, **fields)
        wrapper.ctx = ctx
        wrapper.name = func.__name__

        # Register our decorated function with the specified crontab for execution.
        crontab.register(wrapper.name, wrapper)

        return wrapper
    return decorator
