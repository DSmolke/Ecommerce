import unittest
from decimal import Decimal
from datetime import datetime
import pytz


import pytest

from ecomerceapp.ecomerce_service.model import Customer, Product, Category, Order


# CUSTOMER

@pytest.fixture
def adult_customer() -> Customer:
    return Customer('ADAM', 'SMITH', 18, 'adam.smith@email.com')


class TestCustomerIsOlderThan:
    customer = Customer('ADAM', 'SMITH', 18, 'adam.smith@email.com')
    lower_value = 10
    same_value = 18
    greater_value = 21
    incorrect_type_value = '20'

    def test_is_older_than_with_lower_value(self, adult_customer):
        assert adult_customer.is_older_than(17)

    def test_is_older_than_with_same_value(self, adult_customer):
        assert adult_customer.is_older_than(18) is False

    def test_is_older_than_with_greater_value(self, adult_customer):
        assert adult_customer.is_older_than(19) is False

    def test_is_older_than_with_incorrect_type_value(self):
        with pytest.raises(TypeError) as e:
            self.customer.is_older_than(self.incorrect_type_value)
        assert 'Incorrect value type for n' == e.value.args[0]


class TestCustomerFromDict:
    def test_from_dict_with_correct_data(self):
        assert Customer.from_dict({
            "name": "MARIA",
            "surname": "SMOLKE",
            "age": 18,
            "email": "smolke@gmail.com"
        }) == Customer("MARIA", "SMOLKE", 18, 'smolke@gmail.com')


# PRODUCT

class TestProductFromDict:

    def test_from_dict_with_correct_data(self):
        assert Product.from_dict({"name": "CAR", "price": "200.00", "category": "A"}) == Product("CAR",
                                                                                                 Decimal("200.00"),
                                                                                                 Category.A)


# ORDER

# for datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))
@pytest.fixture(params=[
    (datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 21, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2022, 11, 19, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 21, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2022, 12, 19, 0, 0, 0, 1, pytz.timezone('UTC')), datetime(2022, 12, 21, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2021, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2023, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))),
])
def correct_date_ranges(request):
    return request.param

# for datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))
@pytest.fixture(params=[
    (datetime(2022, 12, 21, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 22, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2022, 12, 19, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 19, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2022, 12, 21, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 25, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2022, 12, 20, 0, 0, 0, 1, pytz.timezone('UTC')), datetime(2022, 12, 21, 0, 0, 0, 1, pytz.timezone('UTC'))),
    (datetime(2023, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2023, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))),
    (datetime(2023, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC')), datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))),
])
def incorrect_date_ranges(request):
    return request.param


class TestOrder:
    valid_customer = Customer("MARIA", 'SMOLKE', 18, 'smolke@gmail.com')
    valid_product = Product('CAR', Decimal('200.00'), Category.A)
    valid_quantity = 3
    valid_order_date = datetime(2022, 12, 20, 0, 0, 0, 0, pytz.timezone('UTC'))
    valid_order = Order(valid_customer, valid_product, valid_quantity, valid_order_date)

    def test_from_dict_with_correct_data(self):
        assert Order.from_dict({
            "customer": {
                "name": "MARIA",
                "surname": "SMOLKE",
                "age": 18,
                "email": "smolke@gmail.com"
            },
            "product": {
                "name": "CAR",
                "price": "200.00",
                "category": "A"
            },
            "quantity": 3,
            "order_date": "2022-12-20T00:00:00+00:00"
        }) == self.valid_order

    def test_get_total_price(self):
        assert self.valid_order.get_total_price() == Decimal('200.00') * 3

    def test_is_order_in_date_range_with_correct_range(self, correct_date_ranges):
        assert self.valid_order.is_order_in_date_range(*correct_date_ranges)

    def test_is_order_in_date_range_with_incorrect_range(self, incorrect_date_ranges):
        assert not self.valid_order.is_order_in_date_range(*incorrect_date_ranges)

    def test_is_quantity_equal_to_with_equal_value(self):
        assert self.valid_order.is_quantity_equal_to(3)

    def test_is_quantity_equal_to_with_not_equal_value(self):
        assert not self.valid_order.is_quantity_equal_to(4)

    def test_get_value_after_discount_for_condition_not_matched(self):
        order = Order(Customer("TESTER", "TEST", 26, 'test@gmail.com'), self.valid_product, self.valid_quantity, datetime(2000, 1, 1, 1, 1, 1, 1, pytz.timezone('UTC')))
        # TODO CZY DA SIĘ JAKOŚ MOCKOWAĆ KLASY Z DEKORATOREM DATACLASS(FROZEN=TRUE)
        assert order.get_value_after_discount() == Decimal('600')

    def test_get_value_after_discount_for_customer_age_matched(self):
        correct_value = (Decimal('600') * Decimal('0.97'))
        assert self.valid_order.get_value_after_discount() == correct_value

    def test_get_value_after_discount_for_customer_with_date_matched(self):
        order = Order(Customer("TESTER", "TEST", 26, 'test@gmail.com'), self.valid_product, self.valid_quantity, datetime.now(tz=pytz.timezone("UTC")))
        assert order.get_value_after_discount() == (Decimal('600') * Decimal('0.98'))

    def test_get_value_after_discount_for_both_condition_matched(self):
        order = Order(self.valid_customer, self.valid_product, self.valid_quantity, datetime.now(tz=pytz.timezone('UTC')))
        assert order.get_value_after_discount() == (Decimal('600') * Decimal('0.97'))

    def test_creation_of_order_with_invalid_customer(self):
        with pytest.raises(ValueError) as e:
            Order('Customer', self.valid_product, self.valid_quantity, self.valid_order_date)
        assert 'customer is not Customer instance', e.value.args[0]

    def test_creation_of_order_with_invalid_product(self):
        with pytest.raises(ValueError) as e:
            Order(self.valid_customer, 'Product', self.valid_quantity, self.valid_order_date)
        assert 'product is not Product instance' == e.value.args[0]

