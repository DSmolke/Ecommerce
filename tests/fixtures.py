import pytest

from enum import Enum
from decimal import Decimal

from ecommerce2.ecommerce_service.model import Client, Product, Category
from ecommerce2.ecommerce_service.service import OrdersService

"""
Package contains fixtures used for all tests
"""

# -----------------------------------------------
# CLIENT
# -----------------------------------------------
@pytest.fixture
def client1_data():
    """ { "name": "ANDREW", "surname": "JOHNS", "age": 18, "balance": "2000.00"} """
    return {
        "name": "ANDREW",
        "surname": "JOHNS",
        "age": 18,
        "balance": "2000.00"
    }

@pytest.fixture
def invalid_client_data():
    """ { "name": 1, "surname": 1, "age": '1', "balance": 1} """
    return {
        'name': 1,
        'surname': 1,
        'age': '1',
        'balance': 1
    }


@pytest.fixture
def client_1():
    """ Client('ANDREW', 'JOHNS', 18, Decimal('2000.00')) """
    return Client('ANDREW', 'JOHNS', 18, Decimal('2000.00'))


@pytest.fixture
def client_2():
    """ Client('JACK', 'SPARROW', 24, Decimal('22000.00')) """
    return Client('JACK', 'SPARROW', 24, Decimal('22000.00'))


@pytest.fixture
def client_3():
    """ Client('JULIA', 'SMITH', 22, Decimal('2000.00')) """
    return Client('JULIA', 'SMITH', 22, Decimal('2000.00'))

@pytest.fixture
def client_2_ghost():
    """ Client('JACK', 'SPARROW', 18, Decimal('22000.00')) """
    return Client('JACK', 'SPARROW', 18, Decimal('22000.00'))

# -----------------------------------------------
# PRODUCT
# -----------------------------------------------

@pytest.fixture
def product_1():
    """ Product("TV", Category.ELECTRONICS, Decimal("1200")) """
    return Product("TV", Category.ELECTRONICS, Decimal("1200"))


@pytest.fixture
def product_2():
    """ Product("SOFA", Category.HOME, Decimal("3200")) """
    return Product("SOFA", Category.HOME, Decimal("3200"))

@pytest.fixture
def product_3():
    """ Product("DISHWASHER", Category.AGD, Decimal("2000")) """
    return Product("DISHWASHER", Category.AGD, Decimal("2000"))

@pytest.fixture
def home_product1():
    """ Product("A", Category.HOME, Decimal('1')) """
    return Product("A", Category.HOME, Decimal('1'))

@pytest.fixture
def home_product2():
    """ Product("B", Category.HOME, Decimal('2')) """
    return Product("B", Category.HOME, Decimal('2'))

@pytest.fixture
def home_product3():
    """ Product("C", Category.HOME, Decimal('3')) """
    return Product("C", Category.HOME, Decimal('3'))

@pytest.fixture
def electronics_product1():
    """ Product("A", Category.ELECTRONICS, Decimal('4')) """
    return Product("A", Category.ELECTRONICS, Decimal('4'))

@pytest.fixture
def electronics_product2():
    """ Product("B", Category.ELECTRONICS, Decimal('5')) """
    return Product("B", Category.ELECTRONICS, Decimal('5'))

@pytest.fixture
def electronics_product3():
    """ Product("C", Category.ELECTRONICS, Decimal('6')) """
    return Product("C", Category.ELECTRONICS, Decimal('6'))

@pytest.fixture
def rtv_product1():
    """ Product("A", Category.RTV, Decimal('7')) """
    return Product("A", Category.RTV, Decimal('7'))

@pytest.fixture
def kitchen_product1():
    """ Product("A", Category.KITCHEN, Decimal('8')) """
    return Product("A", Category.KITCHEN, Decimal('8'))

@pytest.fixture
def product1_data():
    """ { "name": "TV", "category": "ELECTRONICS","price": "1200" } """
    return {
        "name": "TV",
        "category": "ELECTRONICS",
        "price": "1200"
    }

@pytest.fixture
def invalid_product_data():
    """ { "name": 1, "category": 1, "price": 1 } """
    return {
        'name': 1,
        'category': 1,
        'price': 1
    }
# -----------------------------------------------
# ORDERS SERVICE
# -----------------------------------------------
@pytest.fixture
def basic_orders_service(client_1, client_2, client_3, product_1, product_2, product_3):
    return OrdersService({
        client_1: {
            product_1: 1,
            product_2: 2
        },
        client_2: {
            product_2: 1
        },
        client_3: {
            product_3: 1
        }
    })

@pytest.fixture
def empty_orders_service():
    return OrdersService({})

@pytest.fixture
def orders_service_with_two_clients_having_same_age(client_1, client_2_ghost, product_1, product_2):
    return OrdersService({
        client_1: {product_1: 1},
        client_2_ghost: {product_2: 1}
    })

@pytest.fixture
def category_stats_orders_service(client_1, client_2, home_product1, home_product2, home_product3, electronics_product1, electronics_product2, electronics_product3):
    return OrdersService({
        client_1: {home_product1, electronics_product1, home_product2},
        client_2_ghost: {electronics_product1, home_product3, electronics_product3}
    })


# --------------------------------------
# MODELS DATA
# --------------------------------------
@pytest.fixture
def product_name():
    """ "DISHWASHER" """
    return "DISHWASHER"

@pytest.fixture
def product_category():
    """ "HOME" """
    return "HOME"

@pytest.fixture
def not_defined_product_category():
    """ "Z" """
    return "Z"

@pytest.fixture
def product_price():
    """ "200.00" """
    return "200.00"

@pytest.fixture
def basic_enum():
    """ Enum('B', 'B') """
    return Enum('B', 'B')
# -----------------------------------------------
# ORDER DATA
# -----------------------------------------------
@pytest.fixture
def json_orders():
    return [
        {
            "client": {
                "name": "A",
                "surname": "B",
                "age": 18,
                "balance": "2000"
            },
            "client_orders": [
                {"name": "TV", "category":  "HOME", "price": "2000"},
                {"name": "FRIDGE", "category": "HOME", "price": "3000"}
            ]
        }
    ]
