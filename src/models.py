"""Module with two main classes (Product and Category)"""

import json
from typing import Any, Union

from src.base_models import BaseCategory, BaseProduct
from src.mixins import MixinConsoleLog


class Product(BaseProduct, MixinConsoleLog):
    """Class for making products"""

    __products_dict: dict = (
        dict()
    )  # Storage only for this project, in big online-shops this must be replaced with DB or smth else

    def __init__(self, name: str, description: str, price: Union[float, int], quantity: int):
        """Initialization method"""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        Product.__products_dict[name] = self
        MixinConsoleLog.__init__(self)

    def __str__(self) -> str:
        """Return string representation of product"""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self: "Product", other: "Product") -> float:
        """Return sum of product's price"""

        if self is other:
            raise AttributeError("Cannot add product to itself")

        elif type(other) != type(self):
            raise TypeError("Cannot add products from different classes")

        return self.__price * self.quantity + other.__price * other.quantity

    def __repr__(self) -> str:
        """Return string representation of product"""
        return f"{self.__class__.__name__}{self.name, self.description, self.__price, self.quantity}"

    @property
    def price(self) -> Union[float, int]:
        return self.__price

    @price.setter
    def price(self, value: Union[float, int]) -> None:
        if value <= 0:
            print("Price cannot be less than or equal to 0")
            pass
        elif self.__price > value:
            print("""Current product price is greater than the given price.
If you are sure you want to reset the price to lower one, enter 'y', enter any other key to pass""")
            try:
                user_input = input().lower().strip()
                if user_input == "y":
                    self.__price = value
            except Exception:
                pass
        else:
            self.__price = value

    @classmethod
    def new_product(cls, product_dict: dict) -> "Product":
        """Class method for creating a new product object from dictionary"""

        name = product_dict["name"]
        description = product_dict["description"]
        price = product_dict["price"]
        quantity = product_dict["quantity"]

        if name in cls.__products_dict:
            existing_product = cls.__products_dict[name]
            existing_product.quantity += quantity
            max_price = max(price, existing_product.price)
            existing_product.price = max_price
            return existing_product

        else:
            return cls(name, description, price, quantity)


class Category(BaseCategory):
    """Class for making categories"""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        """Initialization method"""
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self) -> str:
        """Return string representation of category"""

        return f"{self.name}, количество продуктов: {sum(prod.quantity for prod in self.__products)} шт."

    def add_product(self, product: Any) -> None:
        """Add product to category"""

        if not isinstance(product, Product) or not issubclass(type(product), Product):
            raise TypeError("Product must be of type Product or its subclass")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Getter for list of products in category"""

        products_string = ""

        for product in self.__products:
            products_string += f"{str(product)}\n"

        return products_string.strip()


class Order(BaseCategory):
    """Class for making orders"""

    order_counter = 0

    def __init__(self, name: str, quantity: int, price: float) -> None:
        """Initialization method"""
        self.name = name
        self.quantity = quantity
        self.price = price
        Order.order_counter += 1
        self.order_id = Order.order_counter

    def __str__(self) -> str:
        """Return string representation of order"""

        return "Order id: {}. Product name: {}. Quantity: {} Total price: {}.".format(
            self.order_id, self.name, self.quantity, self.price
        )


def init_from_json(json_file: str) -> list[Category]:
    """Initialization for objects from json file
    :param json_file: name of json file
    :return: all_products, all_categories — lists, access to products and categories is by using indices"""

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    all_categories = []

    for category in data:

        category_products = [Product.new_product(product) for product in category["products"]]
        category = Category(name=category["name"], description=category["description"], products=category_products)
        all_categories.append(category)

    return all_categories
