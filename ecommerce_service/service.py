from collections import defaultdict, Counter
from dataclasses import dataclass
from decimal import Decimal
from typing import Hashable

from ecommerce2.ecommerce_service.model import Client, Product, Category
from ecommerce2.common import get_n_top_elements_of_most_common_list, first_elements_having_same_value


@dataclass(eq=False)
class OrdersService:
    """
    OrdersService works on dict named 'orders' containing Client as a key and dict as a value.
    Value dict has Product as a key and int representing quantity as a value
    """
    orders: dict[Client, dict[Product, int]]

    def client_with_biggest_spend(self) -> list[Client]:
        """
        :return: List of one or more Clients that have biggest spend in all clients pool
        """
        if self.orders == {}:
            return []

        def _count_total_spend(client_cart: dict[Product, int]) -> Decimal:
            total_spend = sum([product.cost_for_n(client_cart[product]) for product in client_cart])
            return total_spend if isinstance(total_spend, Decimal) else Decimal(total_spend)

        clients_and_total_spends = {}

        for client in self.orders:
            clients_and_total_spends[client] = _count_total_spend(self.orders[client])

        clients_and_total_spends_descending: list[tuple[Client, Decimal]] = sorted(clients_and_total_spends.items(),
                                                                                   key=lambda item: item[1],
                                                                                   reverse=True)
        idx = get_n_top_elements_of_most_common_list(clients_and_total_spends_descending)
        return [client_and_spend[0] for client_and_spend in clients_and_total_spends_descending[:idx]]

    def client_with_biggest_spend_in_category(self, category: Category) -> list[Client]:
        """
        :param category: to check available categories find ecommerce2.ecommerce_service.model.Category enum
        :return: List of one or more Clients that have biggest spend on products that match provided Category
        """
        if self.orders == {}:
            return []

        def _count_total_spend_in_category(client_cart: dict[Product, int]) -> Decimal:
            """
            Auxiliary function that counts total spend of client on products that have same category as in superior functions argument
            :param client_cart: value of orders dict for particular client
            :return: Total spend on products with certain category
            """
            total_spend = sum(
                [product.cost_for_n(client_cart[product]) for product in client_cart if product.category == category])
            return total_spend if isinstance(total_spend, Decimal) else Decimal(total_spend)

        clients_and_total_spends_in_category = {}

        for client in self.orders:
            clients_and_total_spends_in_category[client] = _count_total_spend_in_category(self.orders[client])

        clients_and_total_spends_in_category_descending: list[tuple[Client, Decimal]] = sorted(
            clients_and_total_spends_in_category.items(),
            key=lambda item: item[1],
            reverse=True)
        if clients_and_total_spends_in_category_descending[0][1] == Decimal('0'):
            return []
        idx = get_n_top_elements_of_most_common_list(clients_and_total_spends_in_category_descending)
        return [client_and_spend[0] for client_and_spend in clients_and_total_spends_in_category_descending[:idx]]

    def most_popular_categories_for_clients_ages(self) -> dict[int, list[Category]]:
        """
        Prepares list of one or more Categories are most popular for each age occurrence.
        Data is stored in dict where age is a key and a list of Categories is a value.
        """
        ages_with_categories = defaultdict(list)

        for client in self.orders.keys():
            ages_with_categories[client.age].extend([product.category for product in self.orders[client].keys()])

        ages_with_categories = dict(ages_with_categories)
        ages_with_top_categories = {}
        for age in ages_with_categories:
            ages_with_top_categories[age] = Counter(ages_with_categories[age]).most_common()
            idx = get_n_top_elements_of_most_common_list(ages_with_top_categories[age])
            ages_with_top_categories[age] = [pair[0] for pair in ages_with_top_categories[age][:idx]]

        return ages_with_top_categories

    def categories_stats(self) -> dict[Category, dict[str, Decimal | list[Product]]]:
        """ Creates statistical data on each Category that is currently used in orders. Value for each Category contains
            dict with three items: price mean, most expensive product and cheapest product. First is Decimal value, second
            and third are lists of one or more Product
        """
        if self.orders == {}:
            return {}

        category_with_products = defaultdict(set)
        for client in self.orders:
            for product in self.orders[client]:
                category_with_products[product.category].add(product)
        category_with_stats = {}

        for category in category_with_products:
            products = list(category_with_products[category])
            category_with_stats[category] = {
                    "price_mean": sum([product.price for product in products]) / len(products),
                    "most_expensive_product": first_elements_having_same_value(sorted(products, key=lambda p: p.price, reverse=True)),
                    "cheapest_product": first_elements_having_same_value(sorted(products, key=lambda p: p.price))
                }
        return dict(category_with_stats)

    def categories_with_biggest_clients(self) -> dict[Category, list[Client]]:
        """ Creates dict with Category as a key and list of one or more Clients that have the biggest quantity of bought
            products in that particular Category
        """
        def add_counter_as_value(container: dict, key_value: Hashable) -> None:
            container[key_value] = Counter()

        def update_container_with_client_cart_data(container: dict, key_value: Hashable) -> None:
            for product in self.orders[key_value]:
                container[product.category][key_value] += self.orders[key_value][product]

        def arrange_biggest_buyers_to_category(container: dict) -> None:
            for category in container:
                clients = container[category].most_common()
                if not clients:
                    container[category] = []
                    continue
                idx = get_n_top_elements_of_most_common_list(clients)

                container[category] = [client for client, _ in clients][:idx]

        categories_with_clients = {}

        for category_ in Category:
            add_counter_as_value(categories_with_clients, category_)

        for client in self.orders:
            update_container_with_client_cart_data(categories_with_clients, client)

        arrange_biggest_buyers_to_category(categories_with_clients)

        return categories_with_clients

    def clients_with_carts_value(self) -> dict[Client, Decimal]:
        """ Calculates total spend for each Client and returns dict with Client as a key and his total spend as a value"""
        container = {}
        for client in self.orders:
            container[client] = sum([product.cost_for_n(q) for product, q in self.orders[client].items()])

        return container

    def clients_balances_after_completing_orders(self) -> dict[Client, Decimal]:
        """ Calculates balance of each client if his cart would be processed. Dict with Client as a key,
            and balance subtracted from cart value
        """
        container = {}
        clients_with_spend = self.clients_with_carts_value()

        for client in self.orders:
            container[client] = client.balance_after_spending(clients_with_spend[client])

        return container
