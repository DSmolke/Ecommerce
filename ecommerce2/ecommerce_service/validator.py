from enum import Enum
from typing import Final

from ecommerce2.common import matches_regex, ClientUnstandardizedData, ProductUnstandardizedData
from ecommerce2.ecommerce_service.model import Category
from ecommerce2.settings import ValidatorSettings


class BasicValidator:
    """ Implements all necessary methods that are strongly adapted to validate dicts used to represent certain objects in the service"""

    @staticmethod
    def validate_using_regex(key_name: str, expression: str, regex: str) -> list[str] | list:
        """
        Checks if expression matches regex.
        :param key_name: used to indicate name of expression that might cause errors
        :param expression: will be checked if matches regex
        :param regex: pattern that needs to be matched
        :return: empty list if data is fully valid, list of str if there are any issues with arguments
        """
        if not isinstance(key_name, str):
            raise TypeError(f"Invalid expression type: {type(key_name)}")
        errors = []
        try:
            if not matches_regex(expression, regex):
                errors.append(f'{key_name.title()} is not formatted correctly')
        except TypeError as e:
            errors.append(e.args[0])
        return errors

    @staticmethod
    def validate_integer_value(key_name: str, value: int, min_range: int, max_range: int | None = None) -> list[str]:
        """
        Checks if value matches provided range
        :param key_name: used to indicate name of value that might cause errors
        :param value: checked if matches provided range
        :param min_range: *
        :param max_range: *
        :return: empty list if data is fully valid, list of str if there are any issues with arguments
        """

        def _check_if_instance(name: str, v: int | str, type_: int | str) -> None:
            """ method based on isinstance() mechanism, but raises TypeError if type is incorrect """
            if not isinstance(v, type_):
                raise TypeError(f'{name.title()} has incorrect type')

        _check_if_instance('key_name', key_name, str)
        _check_if_instance('min_range', min_range, int)

        if max_range is not None:
            if min_range > max_range:
                raise ValueError('Range is not correct')
        errors = []
        if not isinstance(value, int):
            errors.append(f"Invalid expression type: {type(value)}")
        elif value < min_range:
            errors.append(f'{key_name.title()} is not valid')
        if max_range:
            if value > max_range:
                errors.append(f'{key_name.title()} is not valid')
        return errors

    @staticmethod
    def validate_name_existence(name: str, enumerator: Enum) -> list[str] | list:
        """ Checks if provided name is also name that exists in provided enumerator """
        if not isinstance(name, str):
            raise TypeError('Name has incorrect type')

        errors = []
        if name not in [e_name.name for e_name in enumerator]:
            errors.append(f'Category is not defined in {enumerator.__name__}')
        return errors


class ClientValidator(BasicValidator):
    """
        Validates client_data dict which is representing object that most likely is obtained by loading json file,
        and it's used to create from_dict() method of Client class.
        ClientValidator is subclass of BasicValidator, and it's strongly dependent on its methods.
    """

    NAME_REGEX: Final = ValidatorSettings.CLIENT_NAME_REGEX
    SURNAME_REGEX: Final = ValidatorSettings.CLIENT_SURNAME_REGEX
    BALANCE_REGEX: Final = ValidatorSettings.CLIENT_BALANCE_REGEX
    AGE_RANGE_MIN: Final = 18

    @staticmethod
    def validate_client_data(client_data: ClientUnstandardizedData) -> dict[str, list[str]]:
        """
        Validates client_data by collecting all errors information for each key that exists in it
        :param client_data: dict with keys: name, surname, age, balance
        :return: dict that contains name of an argument as a key and list with errors that might or might not occur
        """
        errors = {}
        if name_err := ClientValidator._validate_name(client_data['name']):
            errors['name'] = name_err
        if surname_err := ClientValidator._validate_name(client_data['surname']):
            errors['surname'] = surname_err
        if age_err := ClientValidator._validate_age(client_data['age']):
            errors['age'] = age_err
        if balance_err := ClientValidator._validate_balance(client_data['balance']):
            errors['balance'] = balance_err

        return errors

    @staticmethod
    def _validate_name(client_name: str) -> list[str]:
        return ClientValidator.validate_using_regex('name', client_name, ClientValidator.NAME_REGEX)

    @staticmethod
    def _validate_surname(client_surname: str) -> list[str]:
        return ClientValidator.validate_using_regex('surname', client_surname, ClientValidator.SURNAME_REGEX)

    @staticmethod
    def _validate_age(client_age: int) -> list[str]:
        return ClientValidator.validate_integer_value('age', client_age, ClientValidator.AGE_RANGE_MIN)

    @staticmethod
    def _validate_balance(client_balance: str) -> list[str]:
        return ClientValidator.validate_using_regex('balance', client_balance, ClientValidator.BALANCE_REGEX)


class ProductValidator(BasicValidator):
    """
        Validates product_data dict which is representing object that most likely is obtained by loading json file,
        and it's used to create from_dict() method of Product class.
        ProductValidator is subclass of BasicValidator, and it's strongly dependent on its methods.
    """
    NAME_REGEX: Final = ValidatorSettings.PRODUCT_NAME_REGEX
    CATEGORY_REGEX: Final = ValidatorSettings.PRODUCT_CATEGORY_REGEX
    PRICE_REGEX: Final = ValidatorSettings.PRODUCT_PRICE_REGEX

    @staticmethod
    def validate_product_data(product_data: ProductUnstandardizedData) -> dict[str, list[str]]:
        """
                Validates product_data by collecting all errors information for each key that exists in it
                :param product_data: dict with keys: name, category, price
                :return: dict that contains name of an argument as a key and list with errors that might or might not occur
                """
        errors = {}
        if name_err := ProductValidator._validate_name(product_data['name']):
            errors['name'] = name_err
        if category_err := ProductValidator._validate_category(product_data['category']):
            errors['category'] = category_err
        if price_err := ProductValidator._validate_price(product_data['price']):
            errors['price'] = price_err

        return errors

    @staticmethod
    def _validate_name(product_name: str) -> list[str]:
        return ProductValidator.validate_using_regex('name', product_name, ProductValidator.NAME_REGEX)

    @staticmethod
    def _validate_category(product_category: str) -> list[str]:
        if errors := ProductValidator.validate_using_regex('category', product_category,
                                                           ProductValidator.CATEGORY_REGEX):
            return errors
        return ProductValidator.validate_name_existence(product_category, Category)

    @staticmethod
    def _validate_price(product_price: str) -> list[str]:
        if errors := ProductValidator.validate_using_regex('price', product_price, ProductValidator.PRICE_REGEX):
            return errors
        return []
