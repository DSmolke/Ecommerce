from enum import Enum
from decimal import Decimal

import pytest

from ecommerce2.ecommerce_service.validator import BasicValidator, ClientValidator, ProductValidator
from ecommerce2.tests.fixtures import invalid_client_data, client1_data, product_name, product_category, product_price, \
    not_defined_product_category, basic_enum, product1_data, invalid_product_data


class TestBasicValidator:
    class TestValidateUsingRegex:
        def test_with_correct_arguments(self):
            assert BasicValidator.validate_using_regex('name', 'ADA', r'^[A-Z]+$') == []

        def test_with_expression_not_matching_regex(self):
            assert BasicValidator.validate_using_regex('name', '123', r'^[A-Z]+$') == [
                'Name is not formatted correctly']

        @pytest.mark.parametrize(('key_name', 'expression', 'regex'), [
            ('ABC', 1, r'1'),
            ('ABC', 'ABC', 123),

        ])
        def test_with_invalid_type(self, key_name, expression, regex):
            assert BasicValidator.validate_using_regex(key_name, expression, regex) == \
                   ["Invalid expression type: <class 'int'>"] or ["Invalid regex type: <class 'int'>"]

        def test_for_invalid_key_name_type(self):
            with pytest.raises(TypeError) as e:
                assert BasicValidator.validate_using_regex(123, '1', r'1')
            assert e.value.args[0] == "Invalid expression type: <class 'int'>"

    class TestValidateIntegerValue:
        def test_for_correct_arguments(self):
            assert BasicValidator.validate_integer_value('age', 1, 1, 2) == []

        def test_for_value_not_in_range(self):
            assert BasicValidator.validate_integer_value('age', 1, 2, 3) == ['Age is not valid']

        def test_for_incorrect_range(self):
            with pytest.raises(ValueError) as e:
                BasicValidator.validate_integer_value('age', 1, 2, 1)
            assert e.value.args[0] == 'Range is not correct'

    class TestValidateNameExistence:
        def test_for_correct_arguments(self, basic_enum: Enum):
            assert BasicValidator.validate_name_existence('B', basic_enum) == []

        def test_for_incorrect_name(self, basic_enum: Enum):
            assert BasicValidator.validate_name_existence('Z', basic_enum) == [f'Category is not defined in B']

        def test_for_incorrect_name_type(self, basic_enum: Enum):
            with pytest.raises(TypeError) as e:
                BasicValidator.validate_name_existence(1, basic_enum)
            assert e.value.args[0] == 'Name has incorrect type'


class TestClientValidator:
    class TestValidateClientData:
        def test_with_valid_data(self, client1_data):
            assert ClientValidator.validate_client_data(client1_data) == {}

        def test_when_all_errors_occur(self, invalid_client_data):
            """ All values have incorrect types"""
            assert ClientValidator.validate_client_data(invalid_client_data) == {
                'name': [f"Invalid expression type: {type(1)}"],
                'surname': [f"Invalid expression type: {type(1)}"],
                'age': [f"Invalid expression type: {type('1')}"],
                'balance': [f"Invalid expression type: {type(1)}"],
            }

    class TestValidateClientName:
        def test_with_valid_name(self):
            assert ClientValidator._validate_name("ADA") == []

        def test_with_invalid_name(self):
            assert ClientValidator._validate_name('Ada') == ['Name is not formatted correctly']

        def test_with_invalid_name_type(self):
            invalid_name = 123
            assert ClientValidator._validate_name(invalid_name) == [f"Invalid expression type: {type(invalid_name)}"]

    class TestValidateClientSurname:

        @pytest.mark.parametrize(('surname',), [
            ("SMITH",),
            ("SMITH-JONES",),
            ("S",),
        ])
        def test_with_valid_surname(self, surname):
            assert ClientValidator._validate_surname(surname) == []

        @pytest.mark.parametrize(('invalid_surname',), [
            ("Smith",),
            ("SMITH-Jones",),
            ("s",),
            ("sol0",),
        ])
        def test_with_invalid_surname(self, invalid_surname):
            assert ClientValidator._validate_surname(invalid_surname) == ['Surname is not formatted correctly']

        @pytest.mark.parametrize(('invalid_surname',), [
            (1,),
            (1.1,),
            (Decimal('1.2'),),
            (("solo",),),
        ])
        def test_with_invalid_surname_type(self, invalid_surname):
            assert ClientValidator._validate_surname(invalid_surname) == [
                f"Invalid expression type: {type(invalid_surname)}"]

    class TestValidateClientAge:
        def test_with_valid_age(self):
            assert ClientValidator._validate_age(18) == []

        def test_with_invalid_age(self):
            assert ClientValidator._validate_age(17) == ['Age is not valid']

        @pytest.mark.parametrize(('invalid_age',), [
            (18.1,),
            (Decimal("18"),),
            ("18",),
            ((18,),),
            ([18, ],),
        ])
        def test_with_invalid_age_type(self, invalid_age) -> None:
            assert ClientValidator._validate_age(invalid_age) == [f"Invalid expression type: {type(invalid_age)}"]

    class TestValidateClientBalance:

        def test_with_valid_value(self):
            assert ClientValidator._validate_balance('200.00') == []

        @pytest.mark.parametrize(('invalid_balance',), [
            (1,),
            ([1, ],),
            ((1,),),
        ])
        def test_with_invalid_type(self, invalid_balance):
            assert ClientValidator._validate_balance(invalid_balance) == [
                f"Invalid expression type: {type(invalid_balance)}"]


class TestProductValidator:
    class TestValidateProductData:
        def test_with_valid_data(self, product1_data):
            assert ProductValidator.validate_product_data(product1_data) == {}

        def test_when_all_errors_occur(self, invalid_product_data):
            """ All values have incorrect types"""
            assert ProductValidator.validate_product_data(invalid_product_data) == {
                'name': [f"Invalid expression type: {type(1)}"],
                'category': [f"Invalid expression type: {type(1)}"],
                'price': [f"Invalid expression type: {type(1)}"],
            }

    class TestValidateProductName:
        def test_with_correct_value(self, product_name):
            assert ProductValidator._validate_name(product_name) == []

        def test_with_invalid_name(self):
            assert ProductValidator._validate_name('Dishwasher') == ['Name is not formatted correctly']

        @pytest.mark.parametrize(('invalid_name',), [
            (1,),
            ([1, ],),
            ((1,),),
        ])
        def test_with_invalid_name_type(self, invalid_name):
            assert ProductValidator._validate_name(invalid_name) == [f"Invalid expression type: {type(invalid_name)}"]

    class TestValidateProductCategory:
        def test_with_correct_value(self, product_category):
            assert ProductValidator._validate_category(product_category) == []

        def test_with_invalid_category(self):
            assert ProductValidator._validate_category('1') == ['Category is not formatted correctly']

        def test_with_not_defined_category(self, not_defined_product_category):
            assert ProductValidator._validate_category(not_defined_product_category) == [
                'Category is not defined in Category']

        @pytest.mark.parametrize(('invalid_category',), [
            (1,),
            ([1, ],),
            ((1,),),
        ])
        def test_with_invalid_name_type(self, invalid_category):
            assert ProductValidator._validate_name(invalid_category) == [
                f"Invalid expression type: {type(invalid_category)}"]

    class TestValidatePrice:
        def test_with_correct_price(self, product_price):
            assert ProductValidator._validate_price(product_price) == []

        def test_with_invalid_price(self):
            assert ProductValidator._validate_price('-1.00') == ['Price is not formatted correctly']

        @pytest.mark.parametrize(('invalid_price',), [
            (1,),
            ([1, ],),
            ((1,),),
        ])
        def test_with_invalid_name_type(self, invalid_price):
            assert ProductValidator._validate_price(invalid_price) == [
                f"Invalid expression type: {type(invalid_price)}"]
