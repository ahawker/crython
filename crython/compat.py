"""
    crython/compat
    ~~~~~~~~~~~~~~~

    Contains backwards and forwards compatibility across python versions.
"""
# pylint: disable=redefined-builtin, invalid-name, undefined-variable
import sys

import six

try:
    import __builtin__ as builtins
except ImportError:
    import builtins

try:
    from collections import OrderedDict  # pylint: disable=unused-import
except ImportError:
    from ordereddict import OrderedDict


def is_version(major, minor):
    """
    Check to see if current python interpreter is given major/minor version.
    """
    version = sys.version_info
    return version[0] == major and version[1] == minor


py27 = is_version(2, 7)
py34 = is_version(3, 4)
py35 = is_version(3, 5)
py36 = is_version(3, 6)

int = builtins.int
iteritems = six.iteritems
map = six.moves.map
object = builtins.object
range = six.moves.range
str = str if six.PY3 else unicode
zip = six.moves.zip

int_types = six.integer_types
str_types = six.string_types


__all__ = []
