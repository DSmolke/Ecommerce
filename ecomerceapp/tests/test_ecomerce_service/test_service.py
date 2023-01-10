from decimal import Decimal

import pytest
import pytz
from datetime import datetime

from ecomerceapp.ecomerce_service.model import Product, Category, Order, Customer
from ecomerceapp.ecomerce_service.service import OrdersService
# TODO adult_customer is used as fixture
from .test_models import adult_customer


@pytest.fixture
def order1():
    return Order(Customer('ADAM', 'SMITH', 33, 'adam@gmail.com'), Product('TV', Decimal('3000'), Category.A), 1,
                 datetime(2022, 11, 11, 0, 0, 0, 0, pytz.timezone('UTC')))


@pytest.fixture
def order2():
    return Order(Customer('ELENA', 'BRACE', 25, 'elena@gmail.com'), Product('FRIDGE', Decimal('1500'), Category.B), 2,
                 datetime(2022, 12, 11, 0, 0, 0, 0, pytz.timezone('UTC')))


@pytest.fixture
def order3():
    return Order(Customer('GABRIEL', 'WILLIAMS', 18, 'gabriel@gmail.com'),
                 Product('TOSTER', Decimal('150'), Category.C),
                 3, datetime(2023, 1, 11, 0, 0, 0, 0, pytz.timezone('UTC')))


@pytest.fixture
def order_service_with_distinct_valued_orders(order1, order2, order3):
    return OrdersService([order1, order2, order3])


class TestOrdersService:
    def test_add_order_from_dict(self):
        orders_service = OrdersService([])
        orders_service.add_order_from_dict({
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
        })
        assert len(orders_service.orders) == 1

    def test_get_average_product_price_when_within_range(self, order_service_with_distinct_valued_orders):
        date_min = datetime(2022, 11, 11, 0, 0, 0, 0, pytz.timezone('UTC'))
        date_max = datetime(2023, 1, 11, 0, 0, 0, 0, pytz.timezone('UTC'))
        assert order_service_with_distinct_valued_orders.get_average_product_price_in_date_range(date_min,
                                                                                                 date_max) == Decimal(
            '1075')

    def test_get_average_product_price_when_out_of_range(self, order_service_with_distinct_valued_orders):
        date_min = datetime(2010, 11, 11, 0, 0, 0, 0, pytz.timezone('UTC'))
        date_max = datetime(2010, 1, 11, 0, 0, 0, 0, pytz.timezone('UTC'))
        with pytest.raises(ZeroDivisionError) as e:
            order_service_with_distinct_valued_orders.get_average_product_price_in_date_range(date_min, date_max)
        assert e.value.args[0] == 'product_count equals 0 therefore it cannot be valid divisor'

    def test_get_most_expensive_products_per_category(self, order_service_with_distinct_valued_orders):
        # price is slightly higher and should be in result dict
        flag_order = Order(Customer('ADAM', 'SMITHY', 33, 'adamy@gmail.com'),
                           Product('TV_FLAG', Decimal('3000.1'), Category.A), 1,
                           datetime(2022, 11, 11, 0, 0, 0, 0, pytz.timezone('UTC')))
        redundant_price_order = Order(Customer('GABRIELE', 'WILLIAMS', 18, 'gabriele@gmail.com'),
                                      Product('MONSTER', Decimal('150'), Category.C),
                                      3, datetime(2023, 1, 11, 0, 0, 0, 0, pytz.timezone('UTC')))
        service = order_service_with_distinct_valued_orders
        service.orders.append(flag_order)
        service.orders.append(redundant_price_order)
        assert service.get_most_expensive_products_per_category() == {
            Category.A: [flag_order.product],
            Category.B: [service.orders[1].product],
            Category.C: [service.orders[2].product, redundant_price_order.product]
        }

    def test_get_customers_summary(self, order_service_with_distinct_valued_orders, order1, order2, order3):
        assert order_service_with_distinct_valued_orders.get_customers_orders_summary() == {
            order1.customer: [{'product': order1.product, 'quantity': order1.quantity}],
            order2.customer: [{'product': order2.product, 'quantity': order2.quantity}],
            order3.customer: [{'product': order3.product, 'quantity': order3.quantity}]
        }

    def test_get_date_with_most_orders_made(self, order_service_with_distinct_valued_orders, order1, order2, order3):
        assert order_service_with_distinct_valued_orders.get_date_with_most_orders_made() == [
            order1.order_date, order2.order_date, order3.order_date
        ]

    def test_get_date_with_least_orders_made(self, order_service_with_distinct_valued_orders, order1, order2, order3):
        assert set(order_service_with_distinct_valued_orders.get_date_with_least_orders_made()) == {
            order1.order_date, order2.order_date, order3.order_date
        }

    def test_get_client_with_most_valuable_cart(self, order_service_with_distinct_valued_orders, order1, order2):
        assert order_service_with_distinct_valued_orders.get_client_with_most_valuable_cart() == [
            order1.customer, order2.customer]

    def test_get_orders_value_after_discounts(self, order_service_with_distinct_valued_orders):
        assert order_service_with_distinct_valued_orders.get_orders_value_after_discounts() == Decimal('6346.5')

    def test_get_clients_num_that_ordered_at_least_n_products_per_transaction(self, order_service_with_distinct_valued_orders, order1):
        assert order_service_with_distinct_valued_orders.get_clients_num_that_ordered_at_least_n_products_per_transaction(1) == 1

    def test_get_most_popular_category(self, order_service_with_distinct_valued_orders):
        assert order_service_with_distinct_valued_orders.get_most_popular_category() == [
            Category.A, Category.B, Category.C
        ]

    def test_get_months_with_quantity_of_ordered_products(self, order_service_with_distinct_valued_orders):
        assert order_service_with_distinct_valued_orders.get_months_with_quantity_of_ordered_products() == {
            11: 1,
            12: 2,
            1: 3
        }

    def test_get_most_popular_categories_for_months_that_orders_occurred(self, order_service_with_distinct_valued_orders):
        assert order_service_with_distinct_valued_orders.get_most_popular_categories_for_months_that_orders_occurred() == {
            11: [Category.A],
            12: [Category.B],
            1: [Category.C]
        }
