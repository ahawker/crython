"""
    crython/field
    ~~~~~~~~~~~~~

    Contains functionality for representing an individual field within an expression.
"""
from __future__ import unicode_literals

import calendar
import collections
import functools
import re

from crython import compat


__all__ = ['CronField', 'second', 'minute', 'hour', 'day', 'month', 'weekday', 'year', 'partials']


#: Full day of week names e.g 'Monday', 'Tuesday', 'Wednesday'.
DAY_NAMES = dict((v.lower(), k) for k, v in enumerate(calendar.day_name))

#: Abbreviated day of week names e.g. 'Mon', 'Tue', 'Wed'.
DAY_ABBRS = dict((v.lower(), k) for k, v in enumerate(calendar.day_abbr))

#: Full month names e.g. 'January', 'February', 'March'.
MONTH_NAMES = dict((v.lower(), k) for k, v in enumerate(calendar.month_name))

#: Abbreviated month names e.g. 'Jan', 'Feb', 'Mar'.
MONTH_ABBRS = dict((v.lower(), k) for k, v in enumerate(calendar.month_abbr))

#: English words (full and abbreviated) for day of week & month names that are possible values.
PHRASES = dict((k.lower(), v)
               for d in (DAY_NAMES, DAY_ABBRS, MONTH_NAMES, MONTH_ABBRS)
               for (k, v) in compat.iteritems(d) if k)

#: Regex for detecting valid english words for day of week & month names.
PHRASES_REGEX = re.compile('|'.join(PHRASES.keys()).lstrip('|'), flags=re.IGNORECASE)

#: Regex for detecting "range" and "step" characters e.g. "1-10/2".
RANGE_REGEX = re.compile(r'[-/]', flags=re.IGNORECASE)

#: Default value for field that does not have one specified.
DEFAULT_VALUE = '*'

#: Name for the "second" field in an expression; first value.
SECOND_NAME = 'second'

#: Name for the "minute" field in an expression; second value.
MINUTE_NAME = 'minute'

#: Name for the "hour" field in an expression; third value.
HOUR_NAME = 'hour'

#: Name for the "day" field in an expression; fourth value.
DAY_NAME = 'day'

#: Name for the "month" field in an expression; fifth value.
MONTH_NAME = 'month'

#: Name for the "weekday" field in an expression; sixth value.
WEEKDAY_NAME = 'weekday'

#: Name for the "year" field in an expression; seventh value.
YEAR_NAME = 'year'

#: Collection of human readable names for all supported fields within a cron expression.
NAMES = (SECOND_NAME, MINUTE_NAME, HOUR_NAME, DAY_NAME, MONTH_NAME, WEEKDAY_NAME, YEAR_NAME)

#: Used to match all values within the bounds of a field.
ALL = '*'

#: Used when something in one of the two fields in which the character is allowed, but not the other.
NON_SPECIFIC = '?'

#: Used to specify multiple values.
VALUE_DELIMITER = ','

#: Used to specify a range of values.
RANGE_DELIMITER = '-'

#: Used to specify a step/increment to a range.
RANGE_STEP_DELIMITER = '/'

#: Used to specify the "last" of values.
#: This is only available for "day of week" and "day of month" fields.
LAST = 'L'

#: Used to specify the nearest weekday.
WEEKDAY = 'W'

#: Used to specifc the specific occurrence of a "day of month".
NTH = '#'

#: Set of all non-numeric special characters that are valid within a specific field.
ALL_SPECIALS = frozenset([ALL, NON_SPECIFIC, VALUE_DELIMITER, RANGE_DELIMITER,
                          RANGE_STEP_DELIMITER, LAST, WEEKDAY, NTH])


def _phrase_to_numeral(phrase, phrases=PHRASES, regex=PHRASES_REGEX):
    """
    Replace any full or abbreviated english dow/mon phrases (Jan, Monday, etc) from the field value
    with its respective integer value as a string.

    :param phrase: English word to convert to integer
    :param phrases: (Optional) Mapping of english word to integer value; Default: PHRASES
    :param regex: (Optional) Mapping of english word to integer value; Default: PHRASES_REGEX
    :return: String representation of integer value of the given english word
    """
    def _repl(match):
        return compat.str(phrases[match.group(0).lower()])

    return regex.sub(_repl, compat.str(phrase))


def _int_try_parse(value):
    """
    Attempt to convert the given string to an int. If it cannot be converted, the original string is returned.

    :param value: String to try and convert.
    :return: :class:`int` if conversion was successful; the original :class:`string` otherwise.
    """
    try:
        return compat.int(value)
    except (TypeError, ValueError):
        return value


def _check_and_parse_if_number(value):
    """
    Attempt to convert the given string to an int. Return a tuple pair containing the success of the conversion
    and the result as an integer or the original string if unable to convert.

    :param value: String to try and convert.
    :return: A two item tuple containing a boolean indicating the conversion success and the converted value.
    """
    value = _int_try_parse(value)
    return isinstance(value, compat.int), value


def _invalid_special_chars(value, valid_specials, all_specials=ALL_SPECIALS):
    """
    Get set of invalid special characters found within the given value.

    :param value: Value to check for invalid special characters.
    :param valid_specials: Set of special characters that are valid.
    :param all_specials: Set of all possible special characters that are valid.
    :return: Set of characters from the given value that are not valid.
    """
    return all_specials.difference(valid_specials).intersection(set(value))


class CronField(compat.object):
    """
    Represents an individual field of a cron expression.
    """

    @classmethod
    def new(cls, value, name, *args, **kwargs):
        """
        Create a new :class:`~crython.field.CronField` instance from the given value.

        :param value: Value to create field from.
        :param name: Name of the column this field represents within an expression.
        :param args: Additional positional args
        :param kwargs: Additional keyword args
        :return: A :class:`~crython.field.CronField`
        """
        if isinstance(value, compat.int):
            return cls.from_number(value, name, *args, **kwargs)
        if isinstance(value, compat.str):
            return cls.from_str(value, name, *args, **kwargs)
        if isinstance(value, collections.Iterable):
            return cls.from_iterable(value, name, *args, **kwargs)

        raise ValueError('Expected value of int, str, iterable type; got {0}'.format(type(value)))

    @classmethod
    def from_number(cls, value, name, min, max, specials, *args, **kwargs):
        """
        Create a new :class:`~crython.field.CronField` instance from the given numeric value.

        :param value: A :class:`~int` value.
        :param name: Name of the column this field represents within an expression.
        :param min: Lower bound for the value, inclusive
        :param max: Upper bound for the value, inclusive
        :param specials: Set of special characters valid for this field type
        :param args: Additional positional args
        :param kwargs: Additional keyword args
        :return: A :class:`~crython.field.CronField`
        """
        # Validate value within the given min/max bounds.
        if not min <= value <= max:
            raise ValueError('Value must be between {0} and {1}'.format(min, max))
        return cls(value, name, min, max, specials, *args, **kwargs)

    @classmethod
    def from_str(cls, value, name, min, max, specials, *args, **kwargs):
        """
        Create a new :class:`~crython.field.CronField` instance from the given string value.

        :param value: A :class:`~str` value.
        :param name: Name of the column this field represents within an expression.
        :param min: Lower bound for the value, inclusive
        :param max: Upper bound for the value, inclusive
        :param specials: Set of special characters valid for this field type
        :param args: Additional positional args
        :param kwargs: Additional keyword args
        :return: A :class:`~crython.field.CronField`
        """
        # Do allow creation of fields with special characters we don't have comparison logic for yet. # TODO - #11
        if value in [NON_SPECIFIC, LAST, WEEKDAY, NTH]:
            raise ValueError('Special character "{0}" is not yet supported'.format(value))

        # Replace english word representation for day of week and/or month names with their numeric value.
        value = _phrase_to_numeral(value)

        # Validate that the string value doesn't contain any special characters that aren't supported by the
        # the field "type".
        invalid_chars = _invalid_special_chars(value, specials)
        if invalid_chars:
            raise ValueError('Field contains invalid special characters: {0}'.format(','.join(invalid_chars)))

        return cls(_int_try_parse(value), name, min, max, specials, *args, **kwargs)

    @classmethod
    def from_iterable(cls, value, name, min, max, specials, *args, **kwargs):
        """
        Create a new :class:`~crython.field.CronField` instance from the given :class:`~collections.Iterable` value.

        :param value: A :class:`~collections.Iterable` value.
        :param name: Name of the column this field represents within an expression.
        :param min: Lower bound for the value, inclusive
        :param max: Upper bound for the value, inclusive
        :param specials: Set of special characters valid for this field type
        :param args: Additional positional args
        :param kwargs: Additional keyword args
        :return: A :class:`~crython.field.CronField`
        """
        return cls(sorted(value), name, min, max, specials, *args, **kwargs)

    def __init__(self, value, name, min, max, specials):
        self.value = value
        self.name = name
        self.min = min
        self.max = max
        self.specials = specials

    def __repr__(self):
        return '<{0}(name={1}, value={2}, min={3}, max={4})>'.format(self.__class__.__name__, self.name, self.value,
                                                                     self.min, self.max)

    def __str__(self):
        return compat.str(self.value)

    def __eq__(self, other):
        return self.value == other

    def __contains__(self, item):
        return self.matches(item)

    def matches(self, item):
        """
        Check to see if the given time is 'within' the "time" denoted by this individual field.

        ..todo:: Recomputing this isn't very efficient. Consider converting the field or expression to a `datetime`
        or `timedelta` instance.
        """
        if not isinstance(item, compat.int):
            raise ValueError('Expected comparison with item of type int; got {0}'.format(type(item)))

        if isinstance(self.value, compat.int):
            return self._matches_number(item)
        if isinstance(self.value, compat.str):
            return self._matches_str(item)
        if isinstance(self.value, collections.Iterable):
            return self._matches_iterable(item)

        raise RuntimeError('Unknown value type {0}'.format(type(self.value)))

    def _matches_number(self, item):
        """
        Check to see if the given time value matches that of the field.

        :param item: Numeric value to check against the field value.
        :return: :bool:`True` if they match; :bool:`False` otherwise.
        """
        return self.value == item

    def _matches_str(self, item):
        """
        Check to see if the given time value matches that of the field.

        :param item: String value to check against the field value.
        :return: :bool:`True` if they match; :bool:`False` otherwise.
        """
        match = False

        # Split the value into individual parts if we're dealing with a comma delimited list of values.
        # If there is no commas and nothing to split, this loop will only run one iteration with the
        # entire field value as its "part".
        for part in self.value.split(','):
            # Split on the range/step characters, e.g. "1-10/2".
            part = RANGE_REGEX.split(part)

            # If we just get a single character back, this means it wasn't a range/step definition. In that case
            # it's just a single character field that is some sort of special or a single number.
            if len(part) == 1:
                match |= self._matches_str_single_char_field(item, part[0])
                continue

            # If the length is greater than one, we've got a range definition (with optional step),
            # a numeric "last" field, and a few other possibilities to decipher.
            match |= self._matches_str_multi_char_field(item, *part)
            continue

        return match

    def _matches_str_single_char_field(self, item, value):
        """
        Check to see if this single character part of the field matches the given time value.

        :param item: Time value to check against the single character field value.
        :param value: Single character string value of the field value.
        :return: :bool:`True` if they match; :bool:`False` otherwise.
        """
        # If it's just a string representation of a number, convert it and perform that simple match check.
        # Note: Single numbers should be converted from str to int in :meth:`~crython.field.CronField.from_str`,
        # so these numbers _should_ only be when we're given a comma delimited list of them.
        is_number, numeric_value = _check_and_parse_if_number(value)
        if is_number:
            return numeric_value == item

        # If it's a wildcard special character (match all), just confirm it's within the min/max bounds
        # but otherwise it's _always_ a match.
        if value == ALL:
            return self.min <= item <= self.max

        # If it's a last special character (last of "day of month" or "day of week") or "?". TODO - #11
        if value in [NON_SPECIFIC, LAST]:
            raise RuntimeError('Special character {0} is not yet supported'.format(value))

        raise ValueError('Unknown match of field "{0}" with item "{1}"'.format(value, item))

    def _matches_str_multi_char_field(self, item, start, stop, step=1):
        """
        Check to see if this multi character part (broken into start, stop, and optional step)
        of the field matches the given time value.

        :param item: Time value to check against the multi character field value.
        :param start: First character string value of the part.
        :param stop: Second character string value of the part.
        :param step: (Optional) Third character string value of the part.
        :return: :bool:`True` if they match; :bool:`False` otherwise.
        """
        # If it's the "last" special character (last "day of month" or "day of week"). TODO - #11
        if stop == LAST:
            raise RuntimeError('Special character {0} is not yet supported'.format(stop))

        # If it's a wildcard special character (match all) as the range "start" value, e.g. "*/2", we want to
        # accept the entire value range of this field. Additionally for this case, there won't be a "stop" value, just
        # a "step". Ex: */2 -> 0-59/2
        if start == ALL:
            start, stop, step = self.min, self.max, stop

        # Check to see if the given item is within our range and a multiple of
        # the step/interval, if one was provided.
        start, stop, step = [compat.int(v) for v in (start, stop, step)]
        is_within_range = start <= item <= stop
        is_multiple_of_step = (not step or (item + start) % step == 0)

        return is_within_range and is_multiple_of_step

    def _matches_iterable(self, item):
        """
        Check to see if the given time value is within that of the field iterable.

        :param item: Value to check against field value for membership.
        :return: :bool:`True` if the field contains the target value; :bool:`False` otherwise.
        """
        return item in self.value


#: Partial for creating a :class:`~crython.CronField` that represents the "second".
second = functools.partial(CronField.new, name='second', min=0, max=59,
                           specials=frozenset([ALL, RANGE_DELIMITER,
                                               RANGE_STEP_DELIMITER, VALUE_DELIMITER]))

#: Partial for creating a :class:`~crython.CronField` that represents the "minute".
minute = functools.partial(CronField.new, name='minute', min=0, max=59,
                           specials=frozenset([ALL, RANGE_DELIMITER,
                                               RANGE_STEP_DELIMITER, VALUE_DELIMITER]))

#: Partial for creating a :class:`~crython.CronField` that represents the "hour".
hour = functools.partial(CronField.new, name='hour', min=0, max=23,
                         specials=frozenset([ALL, RANGE_DELIMITER,
                                             RANGE_STEP_DELIMITER, VALUE_DELIMITER]))

#: Partial for creating a :class:`~crython.CronField` that represents the "day of month".
day = functools.partial(CronField.new, name='day', min=1, max=31,
                        specials=frozenset([ALL, RANGE_DELIMITER,
                                            RANGE_STEP_DELIMITER, VALUE_DELIMITER,
                                            NON_SPECIFIC, LAST, WEEKDAY]))

#: Partial for creating a :class:`~crython.CronField` that represents the "day of month".
month = functools.partial(CronField.new, name='month', min=1, max=12,
                          specials=frozenset([ALL, RANGE_DELIMITER,
                                              RANGE_STEP_DELIMITER, VALUE_DELIMITER]))

#: Partial for creating a :class:`~crython.CronField` that represents the "day of week".
weekday = functools.partial(CronField.new, name='weekday', min=0, max=6,
                            specials=frozenset([ALL, RANGE_DELIMITER,
                                                RANGE_STEP_DELIMITER, VALUE_DELIMITER,
                                                NON_SPECIFIC, LAST, NTH]))

#: Partial for creating a :class:`~crython.CronField` that represents the "year".
year = functools.partial(CronField.new, name='year', min=1970, max=2099,
                         specials=frozenset([ALL, RANGE_DELIMITER,
                                             RANGE_STEP_DELIMITER, VALUE_DELIMITER,
                                             NON_SPECIFIC, LAST, NTH]))

#: Mapping of field name to the partial that create one of that field "type".
partials = compat.OrderedDict(zip(NAMES, (second, minute, hour, day, month, weekday, year)))
