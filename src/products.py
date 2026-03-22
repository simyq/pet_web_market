from typing import Union

from src.models import Product


class Smartphone(Product):
    """Class for creating smartphones goods"""

    def __init__(
        self,
        name: str,
        description: str,
        price: Union[float, int],
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Class for creating lawn grass goods"""

    def __init__(
        self,
        name: str,
        description: str,
        price: Union[float, int],
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
