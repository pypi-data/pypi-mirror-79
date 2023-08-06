# -*- coding: utf-8 -*-

import io
import json
import functools
import inspect
from typing import Union, Any, Dict, Optional, Tuple, Type, Callable

from .pretty import prettify


Function = Callable[..., Any]


async def to_bytesio(obj: Union[str, bytes, Dict[str, Any]], skipkeys: bool = False, ensure_ascii: bool = True,
                     check_circular: bool = True, allow_nan: bool = True, encoder: Optional[Type[json.JSONEncoder]] = None, indent: int = 4,
                     separators: Optional[Tuple[str, str]] = None, sort_keys: bool = False, silent: bool = False) -> io.BytesIO:
    """Prettify json-like object and convert it to io.BytesIO object.

    If ``silent`` is true then exception won't be raised and just returns none.

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
    instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the return value can contain non-ASCII
    characters if they appear in strings contained in ``obj``. Otherwise, all
    such characters are escaped in JSON strings.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
    strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If specified, ``separators`` should be an ``(item_separator, key_separator)``
    tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
    ``(',', ': ')`` otherwise.  To get the most compact JSON representation,
    you should specify ``(',', ':')`` to eliminate whitespace.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *sort_keys* is true (default: ``False``), then the output of
    dictionaries will be sorted by key.

    To use a custom ``JSONEncoder`` specify it with the kwarg ``encoder``.
    """

    try:
        if isinstance(obj, (bytes, bytearray)):
            return io.BytesIO(await prettify(obj, silent=silent))

        elif isinstance(obj, (dict, str)):
            return io.BytesIO((await prettify(obj, silent=silent)).encode('utf-8'))

        else:
            raise TypeError("Input must be str, dict, bytes or bytearray not %s" % type(obj))
    except:
        if not silent:
            raise


def jbytesio(skipkeys: bool = False, ensure_ascii: bool = True, check_circular: bool = True,
             allow_nan: bool = True, encoder: Optional[Type[json.JSONEncoder]] = None, indent: int = 4,
             separators: Optional[Tuple[str, str]] = None, sort_keys: bool = False, silent: bool = False):
    """Decorator that wraps the function `to_bytesio`.
    Accepts every kwarg of `to_bytesio` or `prettify`.
    """

    def outer(func: Function) -> Function:

        @functools.wraps(func)
        async def inner(*args, **kwargs):

            if inspect.iscoroutinefunction(func):
                res = await func(*args, **kwargs)
            else:
                res = func(*args, **kwargs)

            return await to_bytesio(res, silent=silent, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                                    allow_nan=allow_nan, encoder=encoder, indent=indent, separators=separators, sort_keys=sort_keys)
        return inner
    return outer
