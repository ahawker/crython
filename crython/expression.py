"""
    crython/expression
    ~~~~~~~~~~~~~~~~~~

    Contains functionality for representing a single cron expression.
"""
from __future__ import unicode_literals

from crython import compat, field, log


__all__ = ['CronExpression']


#: Number of fields for a single cron expression.
FIELD_COUNT = 7

#: Set of of field names based on the order of values in the tuple as returned by `time.struct_time`.
STRUCT_TIME_FIELDS = ('year', 'month', 'day', 'hour', 'minute', 'second', 'weekday')

#: Reserved keyword indicating a "reboot" expression. Reboot expressions should be executed once, immediately upon
#: startup.
REBOOT_KEYWORD = '@reboot'

#: Object indicating that the cron expression is a "@reboot". This means that there is no valid space-delimited
#: value to express it and that it should just be executed "immediately" after starting.
REBOOT_SENTINEL = compat.object()

#: Reserved keywords that map to a specific cron expression.
RESERVED_KEYWORDS = {
    '@yearly': '0 0 0 0 1 1 *',
    '@annually': '0 0 0 0 1 1 *',
    '@monthly': '0 0 0 0 1 * *',
    '@weekly': '0 0 0 0 * 0 *',
    '@daily': '0 0 0 * * * *',
    '@hourly': '0 0 * * * * *',
    '@minutely': '0 * * * * * *',
    '@secondly': '* * * * * * *'
}

#: Default expression string value.
DEFAULT_VALUE = ' '.join(field.DEFAULT_VALUE * FIELD_COUNT)


def _expression_str_to_dict(expression, expression_field_count=FIELD_COUNT, field_names=field.NAMES,
                            expression_keywords=RESERVED_KEYWORDS, reboot_sentinel=REBOOT_SENTINEL):
    """
    Convert the given cron expression in string form to a dict mapping each field to its value.

    :param expression: Cron expression string
    :param expression_field_count: (Optional) Expected number of fields in expression; Default: EXPRESSION_FIELD_COUNT
    :param field_names: (Optional) Collection of field names to use in the returned dict; Default: FIELD_NAMES
    :param expression_keywords: (Optional) Mapping of expression keywords; Default: EXPRESSION_RESERVED_KEYWORDS
    :param reboot_sentinel: (Optional) Object that indicates the expression is a reboot; Default: REBOOT_SENTINEL
    :return: Dict containing name -> value for all fields of the cron expression.
    """
    # If we were given the reboot keyword, return the sentinel object back as we don't have a valid cron expression
    # to represent this case.
    if expression is REBOOT_KEYWORD:
        return reboot_sentinel

    # If the expression is a keyword, convert it to its space-delimited format,
    # otherwise we assume it's already in that form.
    expression = expression_keywords.get(expression, expression)

    # Parse out each individual field value and check that we've got enough.
    values = expression.split()
    if len(values) != expression_field_count:
        raise ValueError('Expression contains {0} fields; expects {1}'.format(len(values), expression_field_count))

    return dict(zip(field_names, values))


def _fields_tuple_from_dict(fields, field_partials=field.partials, field_default=field.DEFAULT_VALUE):
    """
    Convert the given expression dict to an "ordered" tuple.

    The "order" of values within the tuple matches the field ordering of the expression e.g. "second" is first
     and "year" is last.

    :param fields: Dict containing field names -> values.
    :param field_partials: (Optional) Mapping of field names -> partials that create :class:`~crython.field.CronField`.
    :param field_default: (Optional) Default value of a field if one is not set.
    :return: An "ordered" tuple of :class:`~crython.field.CronField` instances.
    """
    return tuple(partial(fields.get(name, field_default)) for (name, partial) in compat.iteritems(field_partials))


class CronExpression(compat.object):
    """
    Represents an entire cron expression.

    An expression consists of seven, space delimited fields that represent the following values::

        +------------- second (0 - 59)
        | +------------- minute (0 - 59)
        | | +------------- hour (0 - 23)
        | | | +------------- day (1 - 31)
        | | | | +------------- month (1 - 12)
        | | | | | +------------- weekday (0 - 6) (Sunday to Saturday; 7 is also Sunday)
        | | | | | | +------------- year (1970 - 2099)
        | | | | | | |
        | | | | | | |
        * * * * * * *
    """

    @classmethod
    def new(cls, expression=None, **kwargs):
        """
        Create a :class:`~crython.expression.CronExpression` instance from the given expression string or field values.

        :param expression: (Optional) A string that can be converted to a cron expression.
        :param kwargs: (Optional) A dict that maps field names to values.
        :return: A :class:`~crython.expression.CronExpression` that represents the given string or field values.
        """
        return cls.from_str(expression) if expression else cls.from_kwargs(**kwargs)

    @classmethod
    def from_str(cls, expression, reboot_sentinel=REBOOT_SENTINEL):
        """
        Create a :class:`~crython.expression.CronExpression` instance from the given cron expression string.

        :param expression: A string that can be converted to a cron expression.
        :param reboot_sentinel: (Optional) Object that indicates the expression is a reboot; Default: REBOOT_SENTINEL
        :return: A :class:`~crython.expression.CronExpression` that represents the given string.
        """
        fields = _expression_str_to_dict(expression, reboot_sentinel=reboot_sentinel)
        return cls.reboot() if fields is reboot_sentinel else cls.from_kwargs(**fields)

    @classmethod
    def from_kwargs(cls, **kwargs):
        """
        Create a :class:`~crython.expression.CronExpression` instance from the given dict of field name -> field value.

        :param kwargs: A dict that maps field names to values.
        :return: A :class:`~crython.expression.CronExpression` that represents the given dict.
        """
        fields = _fields_tuple_from_dict(kwargs)
        return cls(*fields)

    @classmethod
    def reboot(cls):
        """
        Create a :class:`~crython.expression.CronExpression` instance that indicates it's a "reboot" expression.
        A "reboot" expression means that it should be executed during startup and as soon as possible.

        :return: A :class:`~crython.expression.CronExpression` that represents a "reboot".
        """
        return cls(*DEFAULT_VALUE.split(), reboot=True)

    def __init__(self, second, minute, hour, day, month, weekday, year, reboot=False, logger=None):
        self.second = second
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.weekday = weekday
        self.year = year
        self.reboot = reboot
        self.logger = logger or log.get_logger(__name__)

    def __repr__(self):
        return '<{0}({1})>'.format(self.__class__.__name__, compat.str(self))

    def __str__(self):
        if self.is_reboot:
            return REBOOT_KEYWORD
        return ' '.join(compat.str(f) for f in (self.second, self.minute, self.hour, self.day,
                                                self.month, self.weekday, self.year))

    @property
    def is_reboot(self):
        """
        Return `True` if this expression represents a reboot; `False` otherwise.
        """
        return self.reboot is True

    def matches(self, dt):
        """
        Check to see if the the given :class:`~datetime.datetime` instance "matches" this cron expression.

        :param dt: A :class:`~datetime.datetime` instance to compare against.
        :return: `True` if matches this expression; `False` otherwise.
        """
        def fields_lazy_eval(datetime_fields, expression_fields, field_names=field.NAMES):
            """
            Generator function that yields back individual field names and the "match" result of the
            :class:`~crython.field.CronField` with the :class:`~datetime.datetime` field value.

            :param datetime_fields: Mapping of field name to actual datetime value.
            :param expression_fields: Mapping of field name to cron field instance.
            :param field_names: Sequence of field names to use.
            :return: Generator that yields tuple pairs of field name and the match result.
            """
            for name in field_names:
                field = expression_fields[name]
                time = datetime_fields[name]
                match = expression_fields[name].matches(datetime_fields[name])
                match_str = 'matches' if match else 'does not match'
                self.logger.debug('Field "{0}:{1}" {2} value "{3}"'.format(name, field, match_str, time))
                yield match

        # Build mapping of field name -> value from the given :class:`~datetime.datetime` object and
        # field name -> :class:`~crython.field.CronField` on this expression instance that is used to
        # evaluate if the specific datetime value is a match.
        datetime_fields = dict(zip(STRUCT_TIME_FIELDS, dt.timetuple()[:FIELD_COUNT]))
        expression_fields = dict((name, self.__dict__[name]) for name in field.NAMES)

        return all(fields_lazy_eval(datetime_fields, expression_fields))
