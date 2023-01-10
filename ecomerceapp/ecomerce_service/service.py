import logging

from collections import defaultdict, Counter
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from ecomerceapp.common.utils import get_n_top_elements_of_most_common_list
from ecomerceapp.ecomerce_service.model import Order, Category, Product, Customer


logger = logging.getLogger(__name__)


@dataclass
class OrdersService:
    """ OrdersService job is to manage orders pool. It has to provide certain data about orders itself according to business logic"""
    orders: list[Order]

    def __post_init__(self):
        logger.info("Orders service was initialized successfully")

    def add_order_from_dict(self, order_data: dict[str, Any]) -> None:
        """ Ads single order from unstandardized data dict to orders pool"""
        self.orders.append(Order.from_dict(order_data))

    def get_average_product_price_in_date_range(self, start_date: datetime, end_date: datetime) -> Decimal | None:
        """
        Method takes date range as an arguments and calculate average product price that was ordered in that period.
        :param start_date: datetime argument
        :param end_date: datetime argument
        :return: average product price or None if there was no sales in that period
        """
        valid_orders = [order for order in self.orders if order.is_order_in_date_range(start_date, end_date)]
        products_count = Decimal(sum([order.quantity for order in valid_orders]))
        if products_count == 0:
            raise ZeroDivisionError('product_count equals 0 therefore it cannot be valid divisor')
        products_value = sum([order.get_total_price() for order in valid_orders])

        return products_value / products_count

    def get_most_expensive_products_per_category(self) -> dict[Category, list[Product]]:
        """ :return: dict that has a category as a key and list of most expensive products per category as a value
        """

        def get_many_products_if_same_price(products: list[Product]) -> list[Product]:
            """
            Auxiliary function that returns list of one element if there is one most common element or list of n elements
            if there is n most common elements
            :param products: elements that have same category
            :return: list of n elements with highiest price
            """

            def is_price_higher_than_next_product(i: int):
                """
                checks if product that is next in the list is also to product with top price
                :param i:
                :return: True when i is first or last in list or if product under this index has same price as previous one
                         False if price is different
                """
                if i == 0:
                    return True
                if i == len(products):
                    return True
                return True if products[i - 1].price == products[i].price else False

            return [products[i] for i in range(len(products)) if is_price_higher_than_next_product(i)]

        category_and_products = defaultdict(list)

        for order in self.orders:
            category_and_products[order.product.category].append(order.product)

        for category in category_and_products:
            category_and_products[category] = get_many_products_if_same_price(
                sorted(category_and_products[category], reverse=True, key=lambda product: product.price))

        return dict(category_and_products)

    def get_customers_orders_summary(self) -> dict[Customer, list[dict[str, Any]]]:
        """
        method that have to return summary of customers with all of their ordered products
        :return: dict where key is a customer and value is a list of
        """
        customer_and_products = defaultdict(list)

        for order in self.orders:
            customer_and_products[order.customer].append(
                {"product": order.product, "quantity": order.quantity})

        return dict(customer_and_products)

    def get_date_with_most_orders_made(self) -> list[datetime]:
        """
        Method returns list of n dates that are busiest in therms of orders made
        :return: list of n datetime objects
        """

        dates_with_quantities: list = Counter([order.order_date for order in self.orders]).most_common()
        return [date for date, _ in
                dates_with_quantities[:get_n_top_elements_of_most_common_list(dates_with_quantities)]]

    def get_date_with_least_orders_made(self) -> list[datetime]:
        """
        Method returns list of n dates that are the least busy in therms of orders made
        :return: list of datetime objects
        """
        dates_with_quantities: list = Counter([order.order_date for order in self.orders]).most_common()
        dates_with_quantities.reverse()
        return [date for date, _ in
                dates_with_quantities[:get_n_top_elements_of_most_common_list(dates_with_quantities)]]

    def get_client_with_most_valuable_cart(self) -> list[Customer]:
        """
        Method returns list of n clients that have most valuable carts(orders)
        :return: list of Customer objects
        """
        counter = Counter()
        for order in self.orders:
            counter[order.customer] += order.get_total_price()
        counter = counter.most_common()
        return [customer for customer, _ in counter[:get_n_top_elements_of_most_common_list(counter)]]

    def get_orders_value_after_discounts(self) -> Decimal:
        """
        Method calculates value of all orders with discounts applied.
        Rules of discounts:
            - order that is made by a customer that is 25 years old or younger receives 3% discount
            - order that is made in two days time from today gets 2% discount
        :return: total orders value after discount
        """
        return sum([order.get_value_after_discount() for order in self.orders])

    def get_clients_num_that_ordered_at_least_n_products_per_transaction(self, n: int) -> int:
        """
        Method has to check how many clients ordered at least n products per transaction
        :param n: minimal quantity per order
        :return: number of customers that matched
        """
        client_and_orders = defaultdict(list)

        for order in self.orders:
            client_and_orders[order.customer].append(order)

        valid_clients = 0
        for client in client_and_orders:
            if len(client_and_orders[client]) == len(
                    [order for order in client_and_orders[client] if order.is_quantity_equal_to(n)]):
                valid_clients += 1

        return valid_clients

    def get_most_popular_category(self) -> list[Category]:
        """
        Method has to return list of n Category objects that where most popular in all orders
        :return: list of Category objects
        """

        counter = Counter([order.product.category for order in self.orders]).most_common()

        return [category for category, _ in counter[:get_n_top_elements_of_most_common_list(counter)]]

    def get_months_with_quantity_of_ordered_products(self) -> dict[int, int]:
        """
        Method returns dict with numeric representation of month as a key and sum of quantities that occurred in orders in that month
        :return: dict with number from 1 to 12 as a key and integer as a value
        """
        months_with_products_quantities = defaultdict(int)

        for order in self.orders:
            months_with_products_quantities[order.order_date.month] += order.quantity

        return dict(sorted(months_with_products_quantities.items(), key=lambda m_q: m_q[1], reverse=True))

    def get_most_popular_categories_for_months_that_orders_occurred(self) -> dict[int, Category]:
        """ Method returns dict where key is month that is represented by a integer ranges from 1 to 12, value is list of
            one or more Categories that where the most popular for month that order has occurred
        """
        months_with_categories = defaultdict(list)

        for order in self.orders:
            months_with_categories[order.order_date.month].append(order.product.category)

        final_month_with_category = {}
        for month in months_with_categories:
            final_month_with_category[month] = Counter(months_with_categories[month]).most_common()
            idx = get_n_top_elements_of_most_common_list(final_month_with_category[month])
            final_month_with_category[month] = [category for category, _ in final_month_with_category[month]][:idx]
        return final_month_with_category
