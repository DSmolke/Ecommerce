from decimal import Decimal

import pytest
from ecommerce2.ecommerce_service.model import Client, Product, Category
from ecommerce2.tests.fixtures import client1_data, client_1, product1_data, product_1


class TestClient:
    class TestBalanceAfterSpending:
        def test_with_value_lower_than_balance(self, client_1):
            assert client_1.balance_after_spending(Decimal('1999.9')) == Decimal('0.1')

        def test_with_same_value_as_balance(self, client_1):
            assert client_1.balance_after_spending(Decimal('2000')) == Decimal('0')

        def test_with_value_grater_than_balance(self, client_1):
            assert client_1.balance_after_spending(Decimal('2000.1')) == Decimal('-0.1')

        @pytest.mark.parametrize(('spent_value',), [
            (1,),
            (1.1,),
            ('1',),
            ((1,),),
            ([1],),
            ({1},),
            ({1: 1},)
        ])
        def test_with_incorrect_spent_value_type(self, spent_value):
            basic_client = Client('A', 'B', 18, Decimal('1'))
            with pytest.raises(TypeError) as e:
                basic_client.balance_after_spending(spent_value)
            assert e.value.args[0] == "Invalid spent_value type"

    class TestFromDict:

        def test_for_all_values_valid(self, client1_data, client_1):
            assert Client.from_dict(client1_data) == client_1

        """ Other cases, where client data is incorrect by type, being empty or wrong key 
            structure will be validated by ecommerce2.common.is_dict_structure_correct
        """

        @pytest.mark.parametrize(('client_data', ), [
            ({}, ),
            ((), ),
            ({'name': 1})
        ])
        def test_when_incorrect_data_is_provided(self, client_data):
            with pytest.raises(ValueError) as e:
                Client.from_dict(client_data)
            assert e.value.args[0] == "Invalid structure of client_data"


class TestProduct:
    class TestFromDict:
        def test_for_all_values_valid(self, product1_data, product_1):
            assert Product.from_dict(product1_data) == product_1

        """ Other cases, where client data is incorrect by type, being empty or wrong key 
                    structure will be validated by ecommerce2.common.is_dict_structure_correct
                """

        @pytest.mark.parametrize(('product_data',), [
            ({},),
            ((),),
            ({'name': 1})
        ])
        def test_when_incorrect_data_is_provided(self, product_data):
            with pytest.raises(ValueError) as e:
                Product.from_dict(product_data)
            assert e.value.args[0] == "Invalid structure of product_data"

    class TestCostForN:
        def test_if_returned_value_is_decimal(self, product_1):
            assert isinstance(product_1.cost_for_n(2), Decimal)

        def test_when_n_is_valid(self, product_1):
            assert product_1.cost_for_n(2) == Decimal('2400')

        def test_when_n_is_0(self, product_1):
            assert product_1.cost_for_n(0) == Decimal('0')

        def test_when_n_lower_than_0(self, product_1):
            with pytest.raises(ValueError) as e:
                product_1.cost_for_n(-1)
            assert e.value.args[0] == 'n value cannot be lower than 0'

        @pytest.mark.parametrize(
            ("n",),
            [
                ([],),
                (set(()),),
                ((),),
                (1.1,),
                ('ABC',),
                (Decimal('1'),)
            ]
        )
        def test_when_n_has_invalid_type(self, n):
            with pytest.raises(TypeError) as e:
                Product('IPHONE 7', Category.ELECTRONICS, Decimal('2000')).cost_for_n(n)
            assert e.value.args[0] == 'Invalid n value type'
