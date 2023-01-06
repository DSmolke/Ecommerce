from decimal import Decimal
from ecommerce2.ecommerce_service.model import Category

# TODO To mi się nie podoba
from ecommerce2.tests.fixtures import basic_orders_service, client_1, client_2, client_3, product_1, product_2, \
    product_3, empty_orders_service, orders_service_with_two_clients_having_same_age, client_2_ghost, home_product1, \
    home_product2, home_product3, electronics_product1, electronics_product2, electronics_product3, \
    category_stats_orders_service, rtv_product1, kitchen_product1


class TestOrdersService:
    class TestClientWithBiggestSpend:
        def test_when_one_client_with_top_spend(self, basic_orders_service, client_1):
            assert basic_orders_service.client_with_biggest_spend() == [client_1]

        def test_when_two_clients_with_top_spend(self, basic_orders_service, client_1, client_2):
            basic_orders_service.orders[client_2] = basic_orders_service.orders[client_1]

            assert basic_orders_service.client_with_biggest_spend() == [client_1, client_2]

        def test_when_service_has_no_orders(self, empty_orders_service):
            assert empty_orders_service.client_with_biggest_spend() == []

    class TestClientWithBiggestSpendInCategory:

        def test_when_one_client_with_top_spend_in_category(self, basic_orders_service, client_1):
            assert basic_orders_service.client_with_biggest_spend_in_category(Category.HOME) == [client_1]

        def test_when_two_clients_with_top_spend_in_category(self, basic_orders_service, client_1, client_2, product_2):
            basic_orders_service.orders[client_2][product_2] = 2
            assert basic_orders_service.client_with_biggest_spend_in_category(Category.HOME) == [client_1, client_2]

        def test_when_no_product_of_category_in_service(self, basic_orders_service):
            assert basic_orders_service.client_with_biggest_spend_in_category(Category.RTV) == []

        def test_when_service_has_no_orders(self, empty_orders_service):
            assert empty_orders_service.client_with_biggest_spend_in_category(Category.HOME) == []

    class TestMostPopularCategoriesForClientsAges:
        def test_when_three_clients_have_unique_age(self, basic_orders_service):
            assert basic_orders_service.most_popular_categories_for_clients_ages() == {
                18: [Category.ELECTRONICS, Category.HOME],
                24: [Category.HOME],
                22: [Category.AGD]
            }

        def test_when_two_clients_have_same_age_but_different_categories(self,
                                                                         orders_service_with_two_clients_having_same_age):
            assert orders_service_with_two_clients_having_same_age.most_popular_categories_for_clients_ages() == {
                18: [Category.ELECTRONICS, Category.HOME]
            }

        def test_when_empty_service(self, empty_orders_service):
            assert empty_orders_service.most_popular_categories_for_clients_ages() == {}

    class TestCategoriesStats:
        def test_with_one_product_for_category(self, basic_orders_service, product_1, product_2, product_3):
            assert basic_orders_service.categories_stats() == {
                Category.ELECTRONICS: {
                    "price_mean": Decimal('1200'),
                    "most_expensive_product": [product_1],
                    "cheapest_product": [product_1]
                },
                Category.HOME: {
                    "price_mean": Decimal('3200'),
                    "most_expensive_product": [product_2],
                    "cheapest_product": [product_2]
                },
                Category.AGD: {
                    "price_mean": Decimal('2000'),
                    "most_expensive_product": [product_3],
                    "cheapest_product": [product_3]
                }
            }

        def test_with_at_least_three_products_for_category(self, category_stats_orders_service, home_product1,
                                                           home_product3, electronics_product1, electronics_product3):
            assert category_stats_orders_service.categories_stats() == {
                Category.HOME: {
                    "price_mean": Decimal('2'),
                    "most_expensive_product": [home_product3],
                    "cheapest_product": [home_product1]
                },
                Category.ELECTRONICS: {
                    "price_mean": Decimal('5'),
                    "most_expensive_product": [electronics_product3],
                    "cheapest_product": [electronics_product1]
                }
            }

        def test_with_empty_orders(self, empty_orders_service):
            assert empty_orders_service.categories_stats() == {}

    class TestCategoriesWithBiggestClients:
        def test_when_not_all_categories_have_clients(self, basic_orders_service, client_1, client_2, client_3):
            assert basic_orders_service.categories_with_biggest_clients() == {
                Category.HOME: [client_1],
                Category.ELECTRONICS: [client_1],
                Category.KITCHEN: [],
                Category.RTV: [],
                Category.AGD: [client_3]
            }

        def test_when_all_categories_have_client(self, basic_orders_service, client_1, client_2,
                                                 client_3, rtv_product1, kitchen_product1):
            basic_orders_service.orders[client_1][rtv_product1] = 1
            basic_orders_service.orders[client_1][kitchen_product1] = 1

            assert basic_orders_service.categories_with_biggest_clients() == {
                Category.HOME: [client_1],
                Category.ELECTRONICS: [client_1],
                Category.KITCHEN: [client_1],
                Category.RTV: [client_1],
                Category.AGD: [client_3]
            }

        def test_when_more_than_one_client_in_category(self, basic_orders_service, client_1, client_2, product_1):
            basic_orders_service.orders[client_2][product_1] = 1
            assert basic_orders_service.categories_with_biggest_clients()[Category.ELECTRONICS] == [client_1, client_2]

    class TestClientsWithCartsValue:
        def test_with_clients_having_one_product_with_single_quantity(self, basic_orders_service, product_2, client_1,
                                                                      client_2, client_3):
            del basic_orders_service.orders[client_1][product_2]

            assert basic_orders_service.clients_with_carts_value() == {
                client_1: Decimal("1200"),
                client_2: Decimal("3200"),
                client_3: Decimal("2000")
            }

        def test_with_clients_having_multiple_products_with_multiple_quantities(self, basic_orders_service, client_1,
                                                                                client_2, client_3):
            assert basic_orders_service.clients_with_carts_value() == {
                client_1: Decimal('7600'),
                client_2: Decimal('3200'),
                client_3: Decimal('2000')
            }

        def test_with_empty_service(self, empty_orders_service):
            assert empty_orders_service.clients_with_carts_value() == {}

    class TestClientsBalancesAfterCompletingOrders:
        def test_for_populated_service(self, basic_orders_service, client_1, client_2, client_3):
            assert basic_orders_service.clients_balances_after_completing_orders() == {
                client_1: Decimal("-5600"),
                client_2: Decimal("18800"),
                client_3: Decimal("0")
            }

        def test_for_empty_service(self, empty_orders_service):
            assert empty_orders_service.clients_balances_after_completing_orders() == {}
