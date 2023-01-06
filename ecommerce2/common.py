import re

from decimal import Decimal
from typing import Any
from typing import TypedDict

""" Module stores all objects commonly used in service"""


class ClientUnstandardizedData(TypedDict):
    """
    KEYS & TYPES:
    name: str, surname: str, age: int, balance: str
    """
    name: str
    surname: str
    age: int
    balance: str


class ProductUnstandardizedData(TypedDict):
    """
    KEYS & TYPES:
    name: str, category: str, price: str
    """
    name: str
    category: str
    price: str


def get_n_top_elements_of_most_common_list(elements: list[tuple[Any, Any]]) -> int:
    """
    This function purpose is to help with getting multiple values from Counters.
    Best example is when we have set of [1, 2, 3, 3]. We have 2 highest value, so we want to get list containing them
    :param elements: list that is what Counter.most_common() method returns. Example -> [(2,3), (3,3), (1,1)]
    :return: index of last value which is in most common group
    """
    if len(elements) == 0:
        raise IndexError("List is empty therefor index will be invalid")
    n = 1
    for i in range(1, len(elements)):
        if elements[i][1] == elements[i - 1][1]:
            n += 1
        else:
            return n
    return n

def first_elements_having_same_value(elements: list[int | float | Decimal]) -> list[int | float | Decimal]:
    """
    Can be used to extract the highest or the lowest occurrences of same value objects
    :param elements: list of elements sorted in ascending or descending order
    :return: list containing first few elements having same value
    """
    if isinstance(elements, list) is False:
        raise TypeError("Argument named 'elements' has invalid type")

    if not elements:
        return []
    desired_type = type(elements[0])
    if len(elements) != len([element for element in elements if isinstance(element, desired_type)]):
        raise TypeError("Elements list containing invalid type elements")
    if (l := len(elements)) == 1:
        return elements

    idx = 1
    for i in range(1, l):
        if elements[i] == elements[i - 1]:
            idx += 1
        else:
            return elements[:idx]
    return elements


def matches_regex(expression: str, regex: str) -> bool:
    """
    :param expression: valid string
    :param regex: valid string pattern
    :return: if expression matches pattern
    """
    if not isinstance(expression, str):
        raise TypeError(f"Invalid expression type: {type(expression)}")
    if not isinstance(regex, str):
        raise TypeError(f"Invalid regex type: {type(regex)}")
    return re.match(regex, expression)

def is_dict_structure_correct(data: dict, data_name: str, desired_keys: set[str]) -> bool:
    """
    Checks if data dict has same names of keys as desired_keys argument
    :param data: dict needs to be checked
    :param data_name: dict name
    :param desired_keys: keys that we expect to be in checked dict
    :return:
    """
    if not isinstance(data, dict):
        raise TypeError(f'Invalid {data_name} type')
    if data == {}:
        raise ValueError(f'{data_name} cannot be an empty dict')
    if desired_keys != set(data.keys()):
        raise KeyError(f'{data_name} is not valid due to different keys than desired')
    return True
