"""Module with two main classes (Product and Category)"""

import json
from typing import Union


class Product:
    """Class for making products"""

    __products_dict = dict()  # Storage only for this project, in big online-shops this must be replaced with DB or smth else


    def __init__(self, name: str, description: str, price: Union[float, int], quantity: int):
        """Initialization method"""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        Product.__products_dict[name] = self


    @property
    def price(self):
        return self.__price


    @price.setter
    def price(self, value):
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
    def new_product(cls, product_dict: dict):
        """Class method for creating a new product object from dictionary"""

        name = product_dict.get('name')
        description = product_dict.get('description')
        price = product_dict.get('price')
        quantity = product_dict.get('quantity')

        if name in cls.__products_dict:
            existing_product = cls.__products_dict[name]
            existing_product.quantity += quantity
            max_price = max(price, existing_product.price)
            existing_product.price = max_price
            return existing_product

        else:
            return cls(name, description, price, quantity)


class Category:
    """Class for making categories"""

    category_count = 0
    product_count = 0


    def __init__(self, name: str, description: str, products: list[Product]):
        """Initialization method"""
        self.name = name
        self.description = description
        self.__products = products
        # self.__products_dict = {p.name: p for p in products} # Storage only for this project, in big online-shops this string must be replaced with DB or smth else

        Category.category_count += 1
        Category.product_count += len(products)


    def add_product(self, product: Product):
        """Add product to category"""

        self.__products.append(product)
        Category.product_count += 1


    @property
    def products(self) -> str:
        """Getter for list of products in category"""

        products_string = ""
        for product in self.__products:
            products_string += f"{product.name}, {product.price} RUB, Stock: {product.quantity}.\n"

        return products_string.strip()


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




# prod1 = Product("prod1", "descr1", 1, 100)
# prod2 = Product("prod2", "descr2", 2, 200)
#
# cat = Category("cat", "descr", [prod1])
#
# print(cat)
# print(cat.name)
#
# cat.add_product(prod2)
#
# print(cat)
# print(cat.products)
