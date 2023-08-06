"""" String utilities. """

import sys


def s__(obj):
    """
    Converts an object to str format.
    :rtype: str
    """

    if isinstance(obj, str):
        return obj
    v = sys.version_info[0]
    if v == 2:
        if isinstance(obj, unicode):
            return obj.encode('utf-8')
    elif v == 3:
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
    return str(obj)


def b__(obj):
    """
    Converts an object to bytes format.
    :rtype: bytes
    """

    v = sys.version_info[0]
    if v == 2:
        return s__(obj)

    if isinstance(obj, bytes):
        return obj
    if not isinstance(obj, str):
        obj = str(obj)
    return obj.encode('utf-8')
