import sys

major = sys.version_info.major
if major == 2:
    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    numeric_types = (int, long)

elif major == 3:
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int)

else:
    raise ImportError

