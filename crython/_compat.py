"""
    crython/_compat
    ~~~~~~~~~~~~~~~

    Contains backwards and forwards compatibility across python versions.
"""


try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


__all__ = ['OrderedDict']
