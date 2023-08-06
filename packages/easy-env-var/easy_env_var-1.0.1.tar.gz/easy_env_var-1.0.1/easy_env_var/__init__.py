import json
from decimal import Decimal
from os import environ
from typing import Any, Optional, Union

PARSE_MAP = {
    list: json.loads,
    dict: json.loads,
    int: json.loads,
    float: json.loads,
    str: str,
    Decimal: Decimal,
    bool: lambda value: json.loads(value.lower()),
}
ParseableTypes = Union[tuple(PARSE_MAP)]

empty = object()


def env(
    name: str, *, expected_type: ParseableTypes = str, default: Optional[Any] = empty
) -> ParseableTypes:
    f"""
    Returns the environment variable for the given `name` after parsing it to
    the `expected_type`.

    If a environment variable does not exist the `default` value is returned if
    provided. If no `default` is provided it raises KeyError.

    :param name: str
        The name of the environment variable
    :param expected_type: {ParseableTypes}
        The data type the environment variable should be parse to.
    :param default: Any
        The default value to use in case the environment variable doesn't exist.
        This value is not parsed.
    :return: {ParseableTypes}
        The parsed environment variable or the default value if not found.
    :raises:
        KeyError:
    """
    parser = PARSE_MAP[expected_type]
    try:
        value = environ[name]
    except KeyError:
        if default is empty:
            raise
        return default
    else:
        return parser(value)
