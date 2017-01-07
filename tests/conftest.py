"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""

import pytest


@pytest.fixture(scope='module', params=[
    '0 0 0 0 1 1 *',
    '0 0 0 0 1 1 *',
    '0 0 0 0 1 * *',
    '0 0 0 0 * 0 *',
    '0 0 0 * * * *',
    '0 0 * * * * *',
    '0 * * * * * *',
    '* * * * * * *'
])
def valid_expression_str(request):
    """
    Fixture that yields valid cron expression strings.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    '*',
    '* *',
    '* * *',
    '* * * *',
    '* * * * *',
    '* * * * * *',
    '* * * * * * * *',
    '* * * * * * * * *',
    '* * * * * * * * * *',
    '* * * * * * * * * * *',
])
def invalid_length_expression_str(request):
    """
    Fixture that yields cron expression strings that are not the correct length.
    """
    return request.param



