import pytest

from typing import Any

@pytest.fixture
def valid_customer_data() -> dict[str, int]:
    """ { "name": "D", "surname": "S", "age": 18, "email": "d.smolczynski1@gmail.pl" }"""
    return {
        "name": "D",
        "surname": "S",
        "age": 18,
        "email": "d.smolczynski1@gmail.pl"
    }


@pytest.fixture(params=[
    {"name": "Da", "surname": "S", "age": 18, "email": "d.smolczynski1@gmail.com"},
    {"name": "D", "surname": "Sm", "age": 18, "email": "d.smolczynski1@gmail.com"},
    {"name": "D", "surname": "S", "age": 17, "email": "d.smolczynski1@gmail.com"},
    {"name": "D", "surname": "S", "age": 18, "email": "d.smolczynski1gmail.com"}
])
def invalid_customer_data(request) -> dict[str, str | int]:
    """ {"name": "Da", "surname": "S", "age": 18, "email": "d.smolczynski1@gmail.com"} x4 where every dict has one wrong value"""
    return request.param


@pytest.fixture(params=[
    {"A": 1},
    {}
])
def invalid_structured_data(request) -> dict:
    """ {"A": 1} | {}"""
    return request.param


@pytest.fixture
def valid_product_data():
    """ { "name": "A", "price": '1.00', "category": "A"} """
    return {
        "name": "A",
        "price": '1.00',
        "category": "A"
    }


@pytest.fixture(params=[
    {"name": "Aa", "price": '1.00', "category": "A"},
    {"name": "A", "price": '1$', "category": "A"},
    {"name": "A", "price": '1.00', "category": "Aa"},
])
def invalid_product_data(request):
    return request.param


@pytest.fixture
def valid_order_data(valid_product_data, valid_customer_data) -> dict[str, Any]:
    return {
        "customer": valid_customer_data,
        "product": valid_product_data,
        "quantity": 1,
        "order_date": "2022-12-20T00:00:00+00:00"
    }


@pytest.fixture
def invalid_order_data() -> dict[str, Any]:
    return {
        "customer": 1,
        "product": 1,
        "quantity": 1,
        "order_date": 1
    }


@pytest.fixture(params=[
    {"A": 1},
    {}
])
def invalid_structured_data(request) -> dict:
    """ {"A": 1} | {}"""
    return request.param
