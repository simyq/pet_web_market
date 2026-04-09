"""Abstract classes for models"""

from abc import ABC, abstractmethod
from typing import Union


class BaseProduct(ABC):
    """Abstract base class for products"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: Union[float, int], quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: object) -> float:
        pass

    @property
    @abstractmethod
    def price(self) -> Union[float, int]:
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_dict: dict) -> object:
        pass


class BaseCategory(ABC):
    """Abstract base class for categories ad orders"""

    @abstractmethod
    def __init__(self, name: str, *args: list) -> None:
        self.name = name
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class ZeroQuantityAddError(ValueError):
    """Raised when a quantity is zero"""

    def __init__(self, quantity) -> None:
        """Raised when a quantity is zero"""
        self.quantity = quantity

        if quantity != 0:
            print("Товар добавлен")
            pass
        else:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
