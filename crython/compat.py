"""
    crython/compat
    ~~~~~~~~~~~~~~~

    Contains backwards and forwards compatibility across python versions.
"""

import six

try:
    import __builtin__ as builtins
except ImportError:
    import builtins

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


int = builtins.int
iteritems = six.iteritems
map = six.moves.map
object = builtins.object
range = six.moves.range
str = str if six.PY3 else unicode
zip = six.moves.zip


__all__ = []
