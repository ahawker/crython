"""
    test_expression
    ~~~~~~~~~~~~~~~

    Tests for the :mod:`~crython.expression` module.
"""
from __future__ import unicode_literals

import pytest

from crython import compat, expression, field


@pytest.fixture(scope='module', params=expression.RESERVED_KEYWORDS.items())
def reserved_keywords(request):
    """
    Fixture that yields two-item pairs containing the name of a reserved keyword and
    its corresponding space-delimited value.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    dict(second=-1),
    dict(second=60),
    dict(minute=-1),
    dict(minute=60),
    dict(hour=-1),
    dict(hour=24),
    dict(day=0),
    dict(day=32),
    dict(month=0),
    dict(month=13),
    dict(weekday=-1),
    dict(weekday=8),
    dict(year=0),
    dict(year=1969),
    dict(year=2100)
])
def invalid_expression_kwargs(request):
    """
    Fixture that yields mappings that are invalid sets of kwargs for creating a new
    :class:`~crython.expression.CronExpression` instance.
    """
    return request.param


def test_expression_str_to_dict_returns_reboot_sentinel():
    """
    Assert that :func:`~crython.expression._expression_str_to_dict` returns
    :object:`~crython.expression.REBOOT_SENTINEL` when given :str:`~crython.expression.REBOOT_KEYWORD`.
    """
    assert expression._expression_str_to_dict(expression.REBOOT_KEYWORD) == expression.REBOOT_SENTINEL


def test_expression_str_to_dict_raises_on_invalid_length_expression(invalid_length_expression_str):
    """
    Assert that :func:`~crython.expression._expression_str_to_dict` raises a :class:`~ValueError` when given
    an expression string that doesn't match the expected length.
    """
    with pytest.raises(ValueError):
        expression._expression_str_to_dict(invalid_length_expression_str)


def test_expression_str_to_dict_returns_well_formed_dict_on_valid_str(valid_expression_str):
    """
    Assert that :func:`~crython.expression._expression_str_to_dict` returns a well-formed dictionary when
    given a valid expression string.
    """
    fields = expression._expression_str_to_dict(valid_expression_str)
    assert len(fields) == expression.FIELD_COUNT


def test_fields_tuple_from_dict_uses_defaults_on_empty_dict():
    """
    Assert that :func:`~crython.expression._fields_tuple_from_dict` uses all default field values
    when given an empty dict.
    """
    fields = expression._fields_tuple_from_dict({}, field_default='$')
    assert all(f == '$' for f in fields)


def test_fields_tuple_from_dict_uses_given_field_partials():
    """
    Assert that :func:`~crython.expression._fields_tuple_from_dict` uses the given field_partials dict
    when building the return connection.
    """
    fields = expression._fields_tuple_from_dict({}, field_partials={})
    assert len(fields) == 0


def test_fields_tuple_from_dict_returns_cron_field_instances():
    """
    Assert that :func:`~crython.expression._fields_tuple_from_dict` contains
    :class:`~crython.field.CronField` instances.
    """
    fields = expression._fields_tuple_from_dict({})
    assert all(isinstance(f, field.CronField) for f in fields)


def test_cron_expression_new_with_no_params_returns_default():
    """
    Assert that :meth:`~crython.expression.CronExpression.new` returns a :class:`~crython.expression.CronExpression`
    of the default expression value when not given any parameters.
    """
    expr = expression.CronExpression.new()
    assert compat.str(expr) == expression.DEFAULT_VALUE


def test_cron_expression_new_handles_reboot():
    """
    Assert that :meth:`~crython.expression.CronExpression.new` returns a :class:`~crython.expression.CronExpression`
    that evaluates to a reboot expression when given the keyword.
    """
    expr = expression.CronExpression.new(expression.REBOOT_KEYWORD)
    assert expr.is_reboot is True


def test_cron_expression_from_reboot_returns_proper_expression():
    """
    Assert that :meth:`~crython.expression.CronExpression.new` returns a :class:`~crython.expression.CronExpression`
    that evaluates to a reboot expression.
    """
    expr = expression.CronExpression.from_reboot()
    assert expr.is_reboot is True


def test_cron_expression_new_handles_reserved_keywords(reserved_keywords):
    """
    Assert that :meth:`~crython.expression.CronExpression.new` returns a :class:`~crython.expression.CronExpression`
    that maps to the correct space-delimited value for a given reserved keyword.
    """
    keyword, value = reserved_keywords
    expr = expression.CronExpression.new(keyword)
    assert compat.str(expr) == expression.RESERVED_KEYWORDS[keyword]


def test_cron_expression_from_str_uses_given_reboot_sentinel():
    """
    Assert that :meth:`~crython.expression.CronExpression.new` returns a :class:`~crython.expression.CronExpression`
    that evaluates to a reboot expression when given a custom sentinel.
    """
    sentinel = compat.object()
    expr = expression.CronExpression.from_str(expression.REBOOT_KEYWORD, reboot_sentinel=sentinel)
    assert expr.is_reboot is True


def test_cron_expression_from_kwargs_raises_on_oob_value(invalid_expression_kwargs):
    """
    Assert that :meth:`~crython.expression.CronExpression.from_kwargs` raises a :class:`~ValueError`
    exception when given
    """
    with pytest.raises(ValueError):
        expression.CronExpression.from_kwargs(**invalid_expression_kwargs)
