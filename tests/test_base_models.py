from abc import ABC
from typing import Union

import pytest

from src.base_models import BaseCategory, BaseProduct


class TestBaseProduct:
    """Tests for BaseProduct abstract class"""

    class ConcreteProduct(BaseProduct):
        """Concrete implementation of BaseProduct for testing"""

        def __init__(self, name: str, description: str, price: Union[float, int], quantity: int) -> None:
            self.name = name
            self.description = description
            self._price = price
            self.quantity = quantity

        def __str__(self) -> str:
            return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

        def __repr__(self) -> str:
            return f"ConcreteProduct('{self.name}', '{self.description}', {self._price}, {self.quantity})"

        def __add__(self, other: object) -> float:
            if not isinstance(other, BaseProduct):
                raise TypeError("Cannot add non-product")
            return self._price * self.quantity + other._price * other.quantity

        @property
        def price(self) -> Union[float, int]:
            return self._price

        @classmethod
        def new_product(cls, product_dict: dict) -> object:
            return cls(
                product_dict["name"],
                product_dict["description"],
                product_dict["price"],
                product_dict["quantity"]
            )

    # Valid cases
    def test_base_product_is_abstract(self):
        """Test that BaseProduct cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseProduct("Test", "Description", 100.0, 5)

    def test_concrete_product_implements_all_methods(self):
        """Test that concrete implementation works correctly"""
        product = self.ConcreteProduct("Test", "Description", 100.0, 5)

        assert product.name == "Test"
        assert product.description == "Description"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_concrete_product_str_method(self):
        """Test __str__ method implementation"""
        product = self.ConcreteProduct("Test", "Description", 100.0, 5)
        expected = "Test, 100.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_concrete_product_repr_method(self):
        """Test __repr__ method implementation"""
        product = self.ConcreteProduct("Test", "Description", 100.0, 5)
        expected = "ConcreteProduct('Test', 'Description', 100.0, 5)"
        assert repr(product) == expected

    def test_concrete_product_add_method(self):
        """Test __add__ method implementation"""
        product1 = self.ConcreteProduct("P1", "D1", 100.0, 5)
        product2 = self.ConcreteProduct("P2", "D2", 200.0, 3)

        result = product1 + product2
        assert result == 1100.0

    def test_concrete_product_new_product_classmethod(self):
        """Test new_product classmethod"""
        product_dict = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 150.0,
            "quantity": 10
        }

        product = self.ConcreteProduct.new_product(product_dict)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 150.0
        assert product.quantity == 10

    # Edge cases
    def test_base_product_abstract_methods_exist(self):
        """Test that BaseProduct defines all required abstract methods"""
        abstract_methods = [
            '__init__',
            '__str__',
            '__repr__',
            '__add__',
            'price',
            'new_product'
        ]

        for method in abstract_methods:
            assert hasattr(BaseProduct, method)
            assert getattr(BaseProduct, method).__isabstractmethod__

    def test_concrete_product_with_zero_values(self):
        """Test concrete product with zero values"""
        product = self.ConcreteProduct("Zero", "Description", 0.0, 0)

        assert product.price == 0.0
        assert product.quantity == 0

    def test_concrete_product_with_negative_values(self):
        """Test concrete product with negative values"""
        product = self.ConcreteProduct("Negative", "Description", -100.0, -5)

        assert product.price == -100.0
        assert product.quantity == -5

    def test_concrete_product_price_property_getter(self):
        """Test that price property works as getter"""
        product = self.ConcreteProduct("Test", "Description", 100.0, 5)

        # Should access private attribute via property
        assert product.price == 100.0

    # Invalid cases
    def test_base_product_missing_methods(self):
        """Test that class missing abstract methods cannot be instantiated"""

        class IncompleteProduct(BaseProduct):
            def __init__(self, name, description, price, quantity):
                self.name = name
                # Missing other abstract methods

        with pytest.raises(TypeError):
            IncompleteProduct("Test", "Desc", 100.0, 5)

    def test_concrete_product_add_non_product(self):
        """Test __add__ with non-product object raises error"""
        product = self.ConcreteProduct("Test", "Description", 100.0, 5)

        with pytest.raises(TypeError, match="Cannot add non-product"):
            product + 100

    def test_new_product_missing_dict_keys(self):
        """Test new_product with missing dictionary keys"""
        incomplete_dict = {
            "name": "Test",
            "price": 100.0
            # Missing description and quantity
        }

        with pytest.raises(KeyError):
            self.ConcreteProduct.new_product(incomplete_dict)


class TestBaseCategory:
    """Tests for BaseCategory abstract class"""

    class ConcreteCategory(BaseCategory):
        """Concrete implementation of BaseCategory for testing"""

        def __init__(self, name, *args) -> None:
            self.name = name
            self.products = list(args)

        def __str__(self) -> str:
            return f"Категория: {self.name}, товаров: {len(self.products)}"

        def add_product(self, product) -> None:
            """Additional method for testing"""
            self.products.append(product)

    # Valid cases
    def test_base_category_is_abstract(self):
        """Test that BaseCategory cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseCategory("Test")

    def test_concrete_category_implements_methods(self):
        """Test that concrete implementation works correctly"""
        category = self.ConcreteCategory("Electronics")

        assert category.name == "Electronics"
        assert category.products == []

    def test_concrete_category_with_args(self):
        """Test concrete category with additional arguments"""
        product1 = {"name": "Phone", "price": 100}
        product2 = {"name": "Laptop", "price": 1000}

        category = self.ConcreteCategory("Electronics", product1, product2)

        assert category.name == "Electronics"
        assert len(category.products) == 2
        assert category.products[0] == product1
        assert category.products[1] == product2

    def test_concrete_category_str_method(self):
        """Test __str__ method implementation"""
        category = self.ConcreteCategory("Books", "Book1", "Book2", "Book3")
        expected = "Категория: Books, товаров: 3"
        assert str(category) == expected

    # Edge cases
    def test_base_category_abstract_methods_exist(self):
        """Test that BaseCategory defines all required abstract methods"""
        abstract_methods = ['__init__', '__str__']

        for method in abstract_methods:
            assert hasattr(BaseCategory, method)
            assert getattr(BaseCategory, method).__isabstractmethod__

    def test_concrete_category_with_empty_name(self):
        """Test concrete category with empty name"""
        category = self.ConcreteCategory("")

        assert category.name == ""
        assert category.products == []

    def test_concrete_category_with_no_args(self):
        """Test concrete category with no additional arguments"""
        category = self.ConcreteCategory("Empty")

        assert category.name == "Empty"
        assert len(category.products) == 0

    # Invalid cases
    def test_base_category_missing_methods(self):
        """Test that class missing abstract methods cannot be instantiated"""

        class IncompleteCategory(BaseCategory):
            def __init__(self, name):
                self.name = name
                # Missing __str__ method

        with pytest.raises(TypeError):
            IncompleteCategory("Test")

    def test_concrete_category_name_type_validation(self):
        """Test that name can be any type (no validation in abstract class)"""
        # Abstract class doesn't enforce type, so this should work
        category = self.ConcreteCategory(123)

        assert category.name == 123

    def test_concrete_category_with_none_name(self):
        """Test concrete category with None as name"""
        category = self.ConcreteCategory(None)

        assert category.name is None
        assert category.products == []


class TestBaseProductInheritance:
    """Tests for inheritance from BaseProduct"""

    def test_concrete_product_inherits_from_base(self):
        """Test that concrete product inherits from BaseProduct"""

        class MyProduct(TestBaseProduct.ConcreteProduct):
            pass

        assert issubclass(MyProduct, BaseProduct)

        product = MyProduct("Test", "Desc", 100.0, 5)
        assert isinstance(product, BaseProduct)

    def test_concrete_category_inherits_from_base(self):
        """Test that concrete category inherits from BaseCategory"""

        class MyCategory(TestBaseCategory.ConcreteCategory):
            pass

        assert issubclass(MyCategory, BaseCategory)

        category = MyCategory("Test")
        assert isinstance(category, BaseCategory)