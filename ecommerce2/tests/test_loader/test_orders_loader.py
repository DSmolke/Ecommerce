from decimal import Decimal

import pytest

from ecommerce2.loader.orders_loader import OrdersLoader
from ecommerce2.ecommerce_service.model import Client, Category, Product
from ecommerce2.tests.fixtures import json_orders


class TestLoadOrders:
    def test_with_valid_orders(self, json_orders):
        assert OrdersLoader.load_from(json_orders) == {
            Client("A", "B", 18, Decimal("2000")): {
                Product("TV", Category.HOME, Decimal("2000")): 1,
                Product("FRIDGE", Category.HOME, Decimal("3000")): 1
            }
        }

    def test_with_invalid_orders(self, json_orders):
        json_orders[0]['client']['balance'] = 2000
        with pytest.raises(ValueError) as e:
            OrdersLoader.load_from(json_orders)
        assert e.value.args[0] == "Orders data is not correct. Cannot load it into Orders Service"
