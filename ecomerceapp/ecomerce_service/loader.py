import json
import logging

from typing import Any

from ecomerceapp.ecomerce_service.model import Order
from ecomerceapp.ecomerce_service.validator import ServiceDataValidator


logger = logging.getLogger(__name__)


def load_json_file(filepath: str) -> dict | list:
    """
    It opens connection with json file, and returns an object represented in that file
    :param filepath: example filepath: 'ecommerceapp/files/file.json'
    :return: object that is stored in json file
    """
    try:
        with open(filepath) as jf:
            logger.info(f'File {filepath} was successfully loaded')
            return json.load(jf)
    except FileNotFoundError as e:
        raise FileNotFoundError('File does not exist')


def load_orders(data: list[dict[str, Any]]) -> list['Order']:
    """
    It has a purpose of loading data of orders that were loaded from json file
    :param data: list of dicts with keys - Order object argument names, values - raw values of those arguments, for example: Decimal values are represented by string values
    :return: list of Order objects
    """
    orders = [Order.from_dict(order_data) for order_data in data if ServiceDataValidator.validate_order_data(order_data)]

    # ternary operator
    if (l1 := len(orders)) == (l2 := len(data)):
        logger.info(f'All json objects were loaded successfully')
    else:
        logger.warning(f"{l2 - l1} json objects weren't loaded correctly")
    return orders
