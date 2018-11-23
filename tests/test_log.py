"""
    test_log
    ~~~~~~~~

    Tests for the :mod:`~crython.log` module.
"""
from crython import log


def test_root_logger_uses_package_name():
    """
    Assert that the root logger uses the package name.
    """
    assert log.ROOT_LOGGER.name == 'crython'


def test_child_logger_name_path_starts_with_package_name():
    """
    Assert that child logs use the package name as the root value of the name path.
    """
    child = log.get_logger('foo')
    assert child.name == 'crython.foo'
