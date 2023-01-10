import enum
import re

from decimal import Decimal
from enum import Enum

from typing import Any, Callable


# ENUM
def is_enum_name(enum_: Enum, name: str) -> bool:
    """
    :param enum_: enum object that will be checked
    :param name: name that we are anticipating is an enum element name
    :return: bool checking if name is part of enum
    """
    if not isinstance(enum_, enum.EnumType):
        raise TypeError("Object is not an Enum")
    if not isinstance(name, str):
        raise TypeError("Name is not a string")
    return name in [element.name for element in enum_]

# NUMERIC VALUES
def is_unstandardized_decimal_grater_or_equal_to(compare_value: Decimal, value: str) -> bool:
    """
    checks if value is greater or equal to compare value
    :param compare_value: can be decimal
    :param value: can also be a decimal
    :return: value >= compare_value
    """
    if not isinstance(compare_value, Decimal):
        raise TypeError('Compare value has invalid type')
    if not isinstance(value, str):
        raise TypeError('Value argument has invalid type')
    if not matches_regex(r'^\d+\.?\d*$', value):
        raise ValueError('Value argument has invalid formatting')

    return Decimal(value) >= compare_value

def is_integer_grater_equal_to(compare_value: int, value: int) -> bool:
    """ Both compare_value and value have to be integer """
    if not isinstance(compare_value, int):
        raise TypeError('Compare value has invalid type')
    if not isinstance(value, int):
        raise TypeError('Value argument has invalid type')
    return value >= compare_value

# STRING VALUES
def matches_regex(regex: str, expression: str) -> bool:
    """
    :param regex: valid r-string that determine desired pattern
    :param expression: valid str expression
    :return: if expression matches regex
    """
    if not isinstance(expression, str):
        raise TypeError('Expression should be string')
    if re.match(regex, expression):
        return True
    return False


def is_default_isoformat(expression: str) -> bool:
    """
    checks if expression is valid isoformat string
    :param expression: any string
    :return: expression match isoformat regex
    """
    if not isinstance(expression, str):
        raise TypeError('Expression should be string')
    return True if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$', expression) else False

# DICT
def are_keys_in_dict(data_keys: set, data: dict[str, Any]) -> bool:
    return data_keys == set(data.keys())


def validate_dict_structure(validator_and_params_in_order: tuple[tuple[Callable[[Any], bool], tuple[Any]]]):
    """
    Method checks if all provided validations are successful. If there is no match it returns False, and there is
    no further investigation which validation failed
    :param validator_and_params_in_order: Tuple that contains pairs of validator, and it's params
    :return: if all validations are successful
    """
    return all([validator(*params) for validator, params in validator_and_params_in_order])
