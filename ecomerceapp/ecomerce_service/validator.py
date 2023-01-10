from decimal import Decimal
from typing import Any

from ecomerceapp.common.validator import matches_regex, is_unstandardized_decimal_grater_or_equal_to, \
    is_default_isoformat, is_enum_name, is_integer_grater_equal_to, are_keys_in_dict, validate_dict_structure
from ecomerceapp.ecomerce_service.model import Category
from ecomerceapp.settings import AppData

class ServiceDataValidator:
    @staticmethod
    def is_customer_data_valid(customer_data: dict[str, Any]) -> bool:
        """
        Method checks if unstandardized data needed for creation of order object is valid for transformation by from_dict methods
        :param customer_data: Data where Decimal, Enum names, and Datetime are represented by a str
        :return: if data is valid
        """
        customer_keys_in_order = ('name', 'surname', 'age', 'email')
        if are_keys_in_dict(set(customer_keys_in_order), customer_data):
            keys_iterator = iter(customer_keys_in_order)
            return validate_dict_structure(
                validator_and_params_in_order=(
                    (matches_regex, (r'^[A-Z]+( ?[A-Z]+)*$', customer_data[next(keys_iterator)])),
                    (matches_regex, (r'^[A-Z]+( ?[A-Z]+)*$', customer_data[next(keys_iterator)])),
                    (is_integer_grater_equal_to, (AppData.MINIMAL_CUSTOMER_AGE, customer_data[next(keys_iterator)])),
                    (matches_regex, (r'^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$', customer_data[next(keys_iterator)])),
                )
            )
        return False

    @staticmethod
    def is_product_data_valid(product_data: dict[str, Any]) -> bool:
        """
        Method checks if unstandardized data needed for creation of product object is valid for transformation by from_dict methods
        :param product_data: Data where Decimal, Enum names, and Datetime are represented by a str
        :return: if data is valid
        """
        product_keys_in_order = ('name', 'price', 'category')
        if are_keys_in_dict(set(product_keys_in_order), product_data):
            try:
                keys_iterator = iter(product_keys_in_order)
                return validate_dict_structure(
                    validator_and_params_in_order=(
                        (matches_regex, (r'^[A-Z]+( ?[A-Z]+)*$', product_data[next(keys_iterator)])),
                        (is_unstandardized_decimal_grater_or_equal_to, (Decimal('0'), product_data[next(keys_iterator)])),
                        (is_enum_name, (Category, product_data[next(keys_iterator)]))
                    )
                )
            except ValueError:
                return False
        return False

    @staticmethod
    def validate_order_data(order_data: dict[str, Any]) -> bool:
        """
        Method checks if unstandardized data needed for creation of order object is valid for transformation by from_dict methods
        :param order_data: Data where Decimal, Enum names, and Datetime are represented by a str
        :return: if data is valid
        """
        order_keys_in_order = ('customer', 'product', 'quantity', 'order_date')
        if are_keys_in_dict(set(order_keys_in_order), order_data):
            keys_iterator = iter(order_keys_in_order)
            return validate_dict_structure(
                validator_and_params_in_order=(
                    (ServiceDataValidator.is_customer_data_valid, (order_data[next(keys_iterator)],)),
                    (ServiceDataValidator.is_product_data_valid, (order_data[next(keys_iterator)],)),
                    (is_integer_grater_equal_to, (0, order_data[next(keys_iterator)])),
                    (is_default_isoformat, (order_data[next(keys_iterator)],)),
                )
            )
        return False
