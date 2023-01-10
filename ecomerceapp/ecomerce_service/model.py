import pytz

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import Any, Self, ClassVar

from ecomerceapp.settings import AppData


@dataclass(frozen=True)
class Customer:
    """
    Customer stores name, surname, age, and email of service user. It provides service with few functionalities needed.
    """
    name: str
    surname: str
    age: int
    email: str

    def is_older_than(self, n: int) -> bool:
        """ n has to be an integer"""
        if isinstance(n, int):
            return self.age > n
        raise TypeError('Incorrect value type for n')

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """ Creates Customer instance. No data should not be provided without previous validation"""
        return cls(data['name'], data['surname'], data['age'], data['email'])


class Category(Enum):
    """ available names: A B C """
    A, B, C = [auto() for _ in range(3)]


@dataclass(frozen=True)
class Product:
    """ Product stores name, price, and category of service product. It provides service with few functionalities needed. """
    name: str
    price: Decimal
    category: Category

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """ Creates Product instance. No data should not be provided without previous validation"""
        price = Decimal(data['price'])
        category = Category[data['category']]
        return cls(data['name'], price, category)


@dataclass(frozen=True)
class Order:
    """ Order stores category, product, quantity, and order_date of service order. It provides service with few functionalities needed. """

    DISCOUNT_RATE_FOR_DATE: ClassVar = AppData.DISCOUNT_RATE_FOR_DATE
    DISCOUNT_RATE_FOR_CUSTOMER_AGE: ClassVar = AppData.DISCOUNT_RATE_FOR_CUSTOMER_AGE
    DISCOUNT_AGE_CAP: ClassVar = AppData.DISCOUNT_AGE_CAP

    customer: Customer
    product: Product
    quantity: int
    order_date: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.customer, Customer):
            raise ValueError('customer is not Customer instance')
        if not isinstance(self.product, Product):
            raise ValueError('product is not Product instance')

    def get_total_price(self) -> Decimal:
        """ Calculates total value of an order"""
        return self.quantity * self.product.price

    def is_order_in_date_range(self, start_date: datetime, end_date: datetime) -> bool:
        """ Checks if order was made in provided range of time """
        return start_date <= self.order_date <= end_date

    def is_quantity_equal_to(self, n: int) -> bool:
        """
        Checks if order quantity equals n
        :param n: comparison number
        :return: True or False
        """
        return self.quantity == n

    def is_customer_older_than(self, n: int = DISCOUNT_AGE_CAP) -> bool:
        """
            Checks if customer is older than 'n'- an integer provided as an argument.
            In case of 'n' absence in parameters, method will use DISCOUNT_AGE_CAP form Order namespace
        """
        return self.customer.is_older_than(n)

    def get_value_after_discount(self) -> Decimal:
        """ Calculates value of order after applied discount. If customer is younger than 25 years he will get
            x% of discount according to DISCOUNT_RATE_FOR_CUSTOMER_AGE rate, if not then order will be checked if it's
            made within 2 days. If yes then he will get y% of discount according to DISCOUNT_RATE_FOR_DATE rate
        """
        if not self.is_customer_older_than(25):
            return self.get_total_price() * self.DISCOUNT_RATE_FOR_CUSTOMER_AGE
        if self.is_order_in_date_range(today := datetime.now(tz=pytz.timezone("UTC")),
                                       today.replace(day=today.day + 2)):
            return self.get_total_price() * self.DISCOUNT_RATE_FOR_DATE
        return self.get_total_price()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """ Creates Order instance. No data should not be provided without previous validation"""
        return cls(
            Customer.from_dict(data['customer']),
            Product.from_dict(data['product']),
            data['quantity'],
            datetime.fromisoformat(data['order_date'])
        )
