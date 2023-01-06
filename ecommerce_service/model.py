from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from typing import Self, Any

from ecommerce2.common import is_dict_structure_correct


@dataclass(frozen=True)
class Client:
    """ Product class used for creating products that are needed in OrdersService"""
    name: str
    surname: str
    age: int
    balance: Decimal

    def __hash__(self):
        """ Client has to be a key for OrdersService dict"""
        return hash((self.name, self.surname))

    def balance_after_spending(self, spent_value: Decimal) -> Decimal:
        """ Calculates the balance that will occur after spending certain ammount of money"""
        if not isinstance(spent_value, Decimal):
            raise TypeError("Invalid spent_value type")
        return self.balance - spent_value

    @classmethod
    def from_dict(cls, client_data: dict[str, Any]) -> Self:
        """ Creates an instance of Client using provided dict containing parameters needed
            There is assumption in business logic that client_data is validated before getting into new instance
            so any argument types will be able to create new instance
        """
        try:
            is_dict_structure_correct(client_data, 'client_data', {'name', 'surname', 'age', 'balance'})

        except (ValueError, KeyError, TypeError):
            raise ValueError("Invalid structure of client_data")
        client_data['balance'] = Decimal(client_data['balance'])
        return cls(**client_data)


class Category(Enum):
    """ Enumerator for Product categories currently available in service"""
    HOME, ELECTRONICS, KITCHEN, RTV, AGD = (auto() for _ in range(5))


@dataclass(frozen=True)
class Product:
    """ Product class used for creating products that are needed in OrdersService"""
    name: str
    category: Category
    price: Decimal

    def cost_for_n(self, quantity: int) -> Decimal:
        """Calculates cost of provided quantity of product"""
        if isinstance(quantity, int) is False:
            raise TypeError('Invalid n value type')
        if quantity < 0:
            raise ValueError('n value cannot be lower than 0')
        return self.price * quantity

    @classmethod
    def from_dict(cls, product_data: dict[str, Any]) -> Self:
        """ Creates an instance of Product using provided dict containing parameters needed.
            There is assumption in business logic that product_data is validated before getting into new instance
            so any dict with valid keys will be able to create new instance.
        """
        try:
            is_dict_structure_correct(product_data, 'product_data', {'name', 'category', 'price'})

        except (ValueError, KeyError, TypeError):
            raise ValueError("Invalid structure of product_data")

        product_data['category'] = Category[product_data['category']]
        product_data['price'] = Decimal(product_data['price'])
        return cls(**product_data)
