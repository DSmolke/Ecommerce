import json
import pytest

from typing import Final

from ecomerceapp.common.validator import matches_regex
from ecomerceapp.ecomerce_service.model import Order
from ecomerceapp.ecomerce_service.loader import load_json_file, load_orders


class TestJsonLoader:
    CORRECT_FILE_NAME: Final = r'test_file.json'
    INCORRECT_FILE_NAME: Final = 'xyz.json'
    INCORRECT_FILE_TYPE: Final = r'test_file.txt'

    @pytest.mark.xfail(reason="If pytest runs from ecomerceapp instead of ecomerceapp/tests, there will be error")
    def test_loader_with_correct_path(self):
        assert load_json_file(self.CORRECT_FILE_NAME) == [1, 2, 3]

    def test_loader_with_incorrect_path(self):
        with pytest.raises(FileNotFoundError) as e:
            load_json_file(self.INCORRECT_FILE_NAME)
        assert 'File does not exist' == e.value.args[0]

    @pytest.mark.xfail(reason="If pytest runs from ecomerceapp instead of ecomerceapp/tests, there will be error")
    def test_loader_with_incorrect_file_type(self):
        with pytest.raises(json.decoder.JSONDecodeError) as e:
            load_json_file(self.INCORRECT_FILE_TYPE)
        assert e.type == json.decoder.JSONDecodeError


class TestOrdersLoader:
    correct_data = [
        {
            "customer": {
                "name": "DAMIAN",
                "surname": "SMOLCZYNSKI",
                "age": 18,
                "email": "d.smolczynski@o2.pl"
            },
            "product": {
                "name": "TV",
                "price": "20.00",
                "category": "A"
            },
            "quantity": 2,
            "order_date": "2022-11-20T00:00:00+00:00"
        },
        {
            "customer": {
                "name": "MARIA",
                "surname": "SMOLKE",
                "age": 18,
                "email": "d.smolczynski1@o2.pl"
            },
            "product": {
                "name": "CAR",
                "price": "200.00",
                "category": "A"
            },
            "quantity": 3,
            "order_date": "2022-12-20T00:00:00+00:00"
        }
    ]

    incorrect_data = [{}, {}]
    incorrect_data_type = 'Order1, Order2'

    def test_orders_loader_with_correct_data(self):
        assert load_orders(self.correct_data) == [Order.from_dict(self.correct_data[0]),
                                                  Order.from_dict(self.correct_data[1])]

    def test_orders_loader_with_incorrect_data(self):
        assert load_orders(self.incorrect_data) == []

    def test_orders_loader_with_incorrect_data_type(self):
        with pytest.raises(AttributeError) as e:
            load_orders(self.incorrect_data_type)

        assert matches_regex(r"^.*object has no attribute 'keys'", e.value.args[0])
