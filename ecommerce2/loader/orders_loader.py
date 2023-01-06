from collections import defaultdict
from dataclasses import dataclass

from ecommerce2.ecommerce_service.model import Client, Product
from ecommerce2.ecommerce_service.validator import ClientValidator, ProductValidator


@dataclass
class OrdersLoader:
    """ Class that holds namespace for method that is specifically designed to load orders into OrdersService"""
    @staticmethod
    def load_from(orders_data: list[dict[str, dict | list[dict]]]) -> dict[Client, dict[Product, int]]:
        """

        :param orders_data: List of dicts that are most likely loaded from json file. As a result of it, data types are limited by JSON
                            Therefor any transformations that are necessary are processed in from_dict() methods of Client and Product
        :return:
        """
        try:
            for data in orders_data:
                err1 = ClientValidator.validate_client_data(data['client'])
                err2 = [True for order in data['client_orders'] if ProductValidator.validate_product_data(order)]
                if err1 or err2:
                    raise TypeError(f'Invalid data')
        except TypeError:
            raise ValueError("Orders data is not correct. Cannot load it into Orders Service")
        else:
            orders = {}
            for client_order in orders_data:
                client = Client.from_dict(client_order['client'])
                cl_orders = [Product.from_dict(data) for data in client_order['client_orders']]
                cl_orders_default = defaultdict(int)
                for order in cl_orders:
                    cl_orders_default[order] += 1
                orders[client] = dict(cl_orders_default)

            return orders
