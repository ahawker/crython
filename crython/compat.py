"""
    crython/compat
    ~~~~~~~~~~~~~~~

    Contains backwards and forwards compatibility across python versions.
"""

import six
import sys

try:
    import __builtin__ as builtins
except ImportError:
    import builtins

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def is_version(major, minor):
    version = sys.version_info
    return version[0] == major and version[1] == minor


py26 = is_version(2, 6)
py27 = is_version(2, 7)
py33 = is_version(3, 3)
py34 = is_version(3, 4)
py35 = is_version(3, 5)

int = builtins.int
iteritems = six.iteritems
map = six.moves.map
object = builtins.object
range = six.moves.range
str = str if six.PY3 else unicode
zip = six.moves.zip


__all__ = []
