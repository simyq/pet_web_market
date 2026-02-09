"""Module with two main classes (Product and Category)"""

import json
from typing import Union


class Product:
    """Class for making products"""

    def __init__(self, name: str, description: str, price: Union[float, int], quantity: int):
        """Initialization method"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Class for making categories"""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        """Initialization method"""
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def init_from_json(json_file: str) -> tuple[list[Product], list[Category]]:
    """Initialization for objects from json file
    :param json_file: name of json file
    :return: all_products, all_categories — lists, access to products and categories is by using indices"""

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    all_products = []
    all_categories = []

    for category in data:
        category_products = []

        for product in category["products"]:

            product = Product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                quantity=product["quantity"],
            )

            category_products.append(product)
            all_products.append(product)

        category = Category(name=category["name"], description=category["description"], products=category_products)

        all_categories.append(category)

    return all_products, all_categories
