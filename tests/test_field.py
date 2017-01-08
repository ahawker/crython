"""
    test_field
    ~~~~~~~~~~

    Tests for the :mod:`~crython.field` module.
"""
from __future__ import unicode_literals

import pytest

from crython import compat, field


@pytest.fixture(scope='module', params=field.partials.values())
def field_partial(request):
    """
    Fixture that yields back partials for creating :class:`~crython.field.CronField` instances.
    """
    return request.param


@pytest.fixture(scope='module')
def default_field(field_partial):
    """
    Fixture that yields back the creation of all partials using the default field value.
    """
    return field_partial(field.DEFAULT_VALUE)


@pytest.fixture(scope='module', params=compat.range(0, 59))
def second_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "second" field.
    """
    return request.param


@pytest.fixture(scope='module')
def second_field_valid_numeral(second_valid_numeral):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    with a valid numeral.
    """
    return field.second(second_valid_numeral)


@pytest.fixture(scope='module')
def second_field_valid_numeral_as_str(second_valid_numeral):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    with a valid numeral as a string.
    """
    return field.second(compat.str(second_valid_numeral))


@pytest.fixture(scope='module', params=[
    (0, 3),
    (0, 10),
    (0, 58),
    (5, 11),
    (14, 35),
    (30, 59)
])
def second_valid_range(request):
    """
    Fixture that yields a list of values that represent a range of numbers within the bounds
    of the "second" field.
    """
    return compat.range(*request.param)


@pytest.fixture(scope='module', params=[
    (10, 30, 8),
    (20, 30, 2),
    (0, 59, 2),
    (0, 59, 5)
])
def second_valid_range_with_step(request):
    """
    Fixture that yields a list of values that represent a range of numbers with a step that are within
    the bounds of the "second" field.
    """
    return compat.range(*request.param)


@pytest.fixture(scope='module')
def second_field_valid_range(second_valid_range):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    by a valid range of numbers.
    """
    return field.second(second_valid_range)


@pytest.fixture(scope='module')
def second_field_valid_range_with_step(second_valid_range_with_step):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    by a valid range of numbers with a step.
    """
    return field.second(second_valid_range_with_step)


@pytest.fixture(scope='module')
def second_valid_range_str(second_valid_range):
    """
    Fixture that yields a string representation of a range within the bounds
    of the "second" field.
    """
    start, stop = second_valid_range[0], second_valid_range[-1]
    return '{0}-{1}'.format(start, stop)


@pytest.fixture(scope='module')
def second_field_valid_range_str(second_valid_range_str):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    by a valid range string.
    """
    return field.second(second_valid_range_str)


@pytest.fixture(scope='module')
def second_valid_range_with_step_str(second_valid_range_with_step):
    """
    Fixture that yields a string representation of a range, with step value, within the bounds
    of the "second" field.
    """
    start, stop = second_valid_range_with_step[0], second_valid_range_with_step[-1]
    step = second_valid_range_with_step[1] - second_valid_range_with_step[0]
    return '{0}-{1}/{2}'.format(start, stop, step)


@pytest.fixture(scope='module')
def second_field_valid_range_with_step_str(second_valid_range_with_step_str):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    by a valid range string with a step value.
    """
    return field.second(second_valid_range_with_step_str)


@pytest.fixture(scope='module', params=[
    1,
    2,
    3,
    5,
    6,
    10
])
def second_field_all_match_range_with_step_str(request):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    by a valid "all matches" range string with a step value.
    """
    return field.second('*/{0}'.format(request.param))


@pytest.fixture(scope='module', params=[
    [0, 1, 2],
    [0, 1, 2, 3],
    [0, 1, 2, 4],
    [0, 1, 2, 5, 10],
    [0, 1, 2, 5, 10, 30],
    [0, 1, 2, 5, 10, 30, 45],
    [0, 1, 2, 5, 10, 30, 45, 51],
    [0, 1, 2, 5, 10, 30, 45, 51, 54],
    [0, 1, 2, 5, 10, 30, 45, 51, 54, 59],
])
def second_valid_list(request):
    """
    Fixture that yields back valid lists of numbers that can be used to specify multiple matching
    values for the "second" field.
    """
    return request.param


@pytest.fixture(scope='module')
def second_field_valid_list(second_valid_list):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    with a valid list of numerals.
    """
    return field.second(second_valid_list)


@pytest.fixture(scope='module')
def second_field_valid_list_csv_str(second_valid_list):
    """
    Fixture that yields back a :class:`~crython.field.CronField` for the "second" field created
    with a valid list of numerals formatted as a comma separated string.
    """
    return field.second(','.join(map(str, second_valid_list)))


@pytest.fixture(scope='module', params=compat.range(0, 59))
def minute_field_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "second" field.
    """
    return request.param


@pytest.fixture(scope='module', params=compat.range(0, 23))
def hour_field_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "hour" field.
    """
    return request.param


@pytest.fixture(scope='module', params=compat.range(1, 31))
def day_field_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "hour" field.
    """
    return request.param


@pytest.fixture(scope='module', params=compat.range(1, 12))
def month_field_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "hour" field.
    """
    return request.param


@pytest.fixture(scope='module', params=compat.range(0, 6))
def weekday_field_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "hour" field.
    """
    return request.param


@pytest.fixture(scope='module', params=compat.range(1970, 2099))
def year_field_valid_numeral(request):
    """
    Fixture that yields back all valid numerals (inclusive) for the "hour" field.
    """
    return request.param


def _field_matches_lower_bound_inclusive(field):
    """
    Return :bool:`True` if the given field matches its minimum bound value.
    """
    below = field.matches(field.min - 1)
    exact = field.matches(field.min)
    above = field.matches(field.min + 1)
    return below is False and exact is True and above is True


def _field_matches_upper_bound_inclusive(field):
    """
    Return :bool:`True` if the given field matches its maximum bound value.
    """
    below = field.matches(field.max - 1)
    exact = field.matches(field.max)
    above = field.matches(field.max + 1)
    return below is True and exact is True and above is False


def _field_matches_single_value_within_bounds(field, value):
    """
    Return :bool:`True` if the given field _only_ matches the given value. This will check that the given
    value matches and that no other values within the expected min/max bounds do.
    """
    exact = field.matches(value)
    others_within_bounds = (field.matches(v) for v in compat.range(field.min, field.max) if v != value)
    return exact is True and not any(others_within_bounds)


def _field_matches_multiple_values_within_bounds(field, values):
    """
    Return :bool:`True` if the given field _only_ matches against a collection of specified values. This will check
    that the given values match and that no other values within the expected min/max bounds do.
    """
    exact = (field.matches(v) for v in values)
    others_within_bounds = (field.matches(v) for v in compat.range(field.min, field.max) if v not in values)
    return all(exact) and not any(others_within_bounds)


def _field_matches_multiple_values_as_csv_within_bounds(field, values):
    """
    Return :bool:`True` if the given field _only_ matches against a collection of values specified as a
    comma delimited string.
    """
    return _field_matches_multiple_values_within_bounds(field, values.split(','))


def test_default_field_matches_lower_bound_inclusive(default_field):
    """
    Assert that all fields with the default value match their lower bound inclusively.
    """
    assert _field_matches_lower_bound_inclusive(default_field)


def test_default_field_matches_upper_bound_inclusive(default_field):
    """
    Assert that all fields with the default value match their upper bound inclusively.
    """
    assert _field_matches_upper_bound_inclusive(default_field)


def test_default_second_field_matches_all_numeral_values(second_valid_numeral):
    """
    Assert that the "second" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.second(field.DEFAULT_VALUE).matches(second_valid_numeral)


def test_numeral_second_field_only_matches_itself(second_field_valid_numeral):
    """
    Assert that the "second" field created from a single numeral _only_ matches that one value
    and none others within the bounds.
    """
    assert _field_matches_single_value_within_bounds(second_field_valid_numeral, second_field_valid_numeral.value)


def test_numeral_str_second_field_only_matches_itself(second_field_valid_numeral_as_str):
    """
    Assert that the "second" field created from a single numeral formatted as a str _only_ matches that one value
    and none others within the bounds.
    """
    assert _field_matches_single_value_within_bounds(second_field_valid_numeral_as_str,
                                                     second_field_valid_numeral_as_str.value)


def test_list_second_field_only_matches_itself(second_field_valid_list):
    """
    Assert that the "second" field created from a list of numerals _only_ matches those values
    and none other within the bounds.
    """
    assert _field_matches_multiple_values_within_bounds(second_field_valid_list, second_field_valid_list.value)


@pytest.mark.xfail(reason='TODO - #10')
def test_csv_str_second_field_matches_only_matches_itself(second_field_valid_list_csv_str):
    """
    Assert that the "second" field created from a comma separated string of numerals _only_ matches those values
    and none other within the bounds.
    """
    assert _field_matches_multiple_values_as_csv_within_bounds(second_field_valid_list_csv_str,
                                                               second_field_valid_list_csv_str.value)


def test_range_second_field_only_matches_members(second_field_valid_range):
    """
    Assert that the "second" field created from a range of numbers _only_ matches themselves and none
    other within the bounds.
    """
    assert _field_matches_multiple_values_within_bounds(second_field_valid_range, second_field_valid_range.value)


def test_range_with_step_second_field_only_matches_members(second_field_valid_range_with_step):
    """
    Assert that the "second" field created from a range with a step _only_ matches themselves and none
    other within the bounds.
    """
    assert _field_matches_multiple_values_within_bounds(second_field_valid_range_with_step,
                                                        second_field_valid_range_with_step.value)


def test_range_str_second_field_only_matches_members(second_field_valid_range_str, second_valid_range):
    """
    Assert that the "second" field created from a range string _only_ matches items within the range itself
    and none other within the bounds.
    """
    assert _field_matches_multiple_values_within_bounds(second_field_valid_range_str, second_valid_range)


@pytest.mark.xfail(reason='TODO - #13')
def test_range_str_with_step_second_field_only_matches_members(second_field_valid_range_with_step_str,
                                                               second_valid_range_with_step):
    """
    Assert that the "second" field created from a range string with a step value _only_ matches items
    within the range itself that are multiples of the step and none other within the bounds.
    """
    assert _field_matches_multiple_values_within_bounds(second_field_valid_range_with_step_str,
                                                        second_valid_range_with_step)


def test_range_wildcard_str_second_field_matches_all_members_within_bounds(second_field_all_match_range_with_step_str):
    """
    Assert that the "second" field created from a "all match" range string with a step value _only_
    matches items within the range itself that are multiples of the step and none other within the bounds.
    """
    start, stop = second_field_all_match_range_with_step_str.min, second_field_all_match_range_with_step_str.max
    step = compat.int(second_field_all_match_range_with_step_str.value.split('/')[-1])
    assert _field_matches_multiple_values_within_bounds(second_field_all_match_range_with_step_str,
                                                        compat.range(start, stop, step))


def test_default_minute_field_matches_all_numeral_values(minute_field_valid_numeral):
    """
    Assert that the "minute" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.minute(field.DEFAULT_VALUE).matches(minute_field_valid_numeral)


def test_default_hour_field_matches_all_numeral_values(hour_field_valid_numeral):
    """
    Assert that the "hour" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.hour(field.DEFAULT_VALUE).matches(hour_field_valid_numeral)


def test_default_day_field_matches_all_numeral_values(day_field_valid_numeral):
    """
    Assert that the "day" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.day(field.DEFAULT_VALUE).matches(day_field_valid_numeral)


def test_default_month_field_matches_all_numeral_values(month_field_valid_numeral):
    """
    Assert that the "month" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.month(field.DEFAULT_VALUE).matches(month_field_valid_numeral)


def test_default_weekday_field_matches_all_numeral_values(weekday_field_valid_numeral):
    """
    Assert that the "weekday" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.weekday(field.DEFAULT_VALUE).matches(weekday_field_valid_numeral)


def test_default_year_field_matches_all_numeral_values(year_field_valid_numeral):
    """
    Assert that the "year" field with the default value matches all numeral values within
    bounds inclusively.
    """
    assert field.year(field.DEFAULT_VALUE).matches(year_field_valid_numeral)
