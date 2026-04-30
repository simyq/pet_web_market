"""Module with tests for products.py"""

import pytest

from src.products import LawnGrass, Smartphone


class TestSmartphones:
    """Tests for Smartphone class"""

    @pytest.fixture
    def smartphone1(self):
        """Fixture for first smartphone"""
        return Smartphone(
            name="Samsung Galaxy S23 Ultra",
            description="256GB, Серый цвет, 200MP камера",
            price=180000.0,
            quantity=5,
            efficiency=95.5,
            model="S23 Ultra",
            memory=256,
            color="Серый"
        )

    @pytest.fixture
    def smartphone2(self):
        """Fixture for second smartphone"""
        return Smartphone(
            name="Iphone 15",
            description="512GB, Gray space",
            price=210000.0,
            quantity=8,
            efficiency=98.2,
            model="15",
            memory=512,
            color="Gray space"
        )

    @pytest.fixture
    def smartphone3(self):
        """Fixture for third smartphone"""
        return Smartphone(
            name="Xiaomi Redmi Note 11",
            description="1024GB, Синий",
            price=31000.0,
            quantity=14,
            efficiency=90.3,
            model="Note 11",
            memory=1024,
            color="Синий"
        )

    # Valid cases
    def test_smartphone_initialization(self, smartphone1):
        """Test that Smartphone initializes correctly with all attributes"""
        assert smartphone1.name == "Samsung Galaxy S23 Ultra"
        assert smartphone1.description == "256GB, Серый цвет, 200MP камера"
        assert smartphone1.price == 180000.0
        assert smartphone1.quantity == 5
        assert smartphone1.efficiency == 95.5
        assert smartphone1.model == "S23 Ultra"
        assert smartphone1.memory == 256
        assert smartphone1.color == "Серый"

    def test_smartphone_inherits_from_product(self, smartphone1):
        """Test that Smartphone inherits from Product class"""
        assert isinstance(smartphone1, Smartphone)
        assert hasattr(smartphone1, 'name')
        assert hasattr(smartphone1, 'description')
        assert hasattr(smartphone1, 'price')
        assert hasattr(smartphone1, 'quantity')

    def test_smartphone_price_access(self, smartphone3):
        """Test that price property works correctly"""
        assert smartphone3.price == 31000.0

    def test_smartphone_efficiency_access(self, smartphone2):
        """Test that efficiency attribute is accessible"""
        assert smartphone2.efficiency == 98.2

    def test_smartphone_str_representation(self, smartphone1):
        """Test string representation of smartphone"""
        expected = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
        assert str(smartphone1) == expected

    def test_smartphone_addition(self, smartphone1, smartphone2):
        """Test adding two smartphones"""
        # smartphone1 total: 180000 * 5 = 900000
        # smartphone2 total: 210000 * 8 = 1680000
        # Total: 2580000
        result = smartphone1 + smartphone2
        assert result == 2580000.0

    # Edge cases
    def test_smartphone_with_minimal_values(self):
        """Test Smartphone with minimal valid values"""
        phone = Smartphone(
            name="A",
            description="Minimal",
            price=0.01,
            quantity=1,
            efficiency=0.1,
            model="M",
            memory=1,
            color="C"
        )
        assert phone.name == "A"
        assert phone.price == 0.01
        assert phone.quantity == 1
        assert phone.efficiency == 0.1

    def test_smartphone_with_large_values(self):
        """Test Smartphone with large values"""
        phone = Smartphone(
            name="Large Phone",
            description="Very large",
            price=999999.99,
            quantity=1000000,
            efficiency=100.0,
            model="XL",
            memory=1024,
            color="Black"
        )
        assert phone.price == 999999.99
        assert phone.quantity == 1000000

    def test_smartphone_zero_quantity(self):
        """Test Smartphone with zero quantity"""
        with pytest.raises(ValueError) as e:
            phone = Smartphone(
            name="Out of stock",
            description="No stock",
            price=100.0,
            quantity=0,
            efficiency=95.0,
            model="Zero",
            memory=128,
            color="Red"
        )
            assert "Товар с нулевым количеством не может быть добавлен" in e

    def test_smartphone_add_itself(self, smartphone1):
        """Test that adding smartphone to itself raises AttributeError"""
        with pytest.raises(AttributeError, match="Cannot add product to itself"):
            smartphone1 + smartphone1

    # Invalid cases
    def test_smartphone_missing_required_attributes(self):
        """Test that missing required attributes raise TypeError"""
        with pytest.raises(TypeError):
            Smartphone(
                name="Test",
                description="Test",
                price=100.0,
                quantity=5,
                # Missing efficiency, model, memory, color
            )

    def test_smartphone_with_negative_price(self, capsys):
        """Test Smartphone with negative price (should print warning)"""
        phone = Smartphone(
            name="Test",
            description="Test",
            price=-100.0,
            quantity=5,
            efficiency=95.0,
            model="Test",
            memory=128,
            color="Blue"
        )
        captured = capsys.readouterr()
        # Price can be set to negative, but setter should warn
        assert phone.price == -100.0

    def test_smartphone_with_negative_quantity(self):
        """Test Smartphone with negative quantity"""
        phone = Smartphone(
            name="Test",
            description="Test",
            price=100.0,
            quantity=-5,
            efficiency=95.0,
            model="Test",
            memory=128,
            color="Blue"
        )
        assert phone.quantity == -5

    def test_smartphone_wrong_efficiency_type(self):
        """Test Smartphone with string efficiency (should work)"""
        phone = Smartphone(
            name="Test",
            description="Test",
            price=100.0,
            quantity=5,
            efficiency="95.5",  # String instead of float
            model="Test",
            memory=128,
            color="Blue"
        )
        assert phone.efficiency == "95.5"

    @pytest.mark.parametrize("name,price,quantity,efficiency,model,memory,color", [
        ("", 100.0, 5, 95.0, "M", 128, "C"),  # Empty name
        ("Test", -50.0, 5, 95.0, "M", 128, "C"),  # Negative price
        ("Test", 100.0, -10, 95.0, "M", 128, "C"),  # Negative quantity
        ("Test", 100.0, 5, -10.0, "M", 128, "C"),  # Negative efficiency
        ("Test", 100.0, 5, 95.0, "", 128, "C"),  # Empty model
        ("Test", 100.0, 5, 95.0, "M", -5, "C"),  # Negative memory
        ("Test", 100.0, 5, 95.0, "M", 128, ""),  # Empty color
    ])
    def test_smartphone_parameterized_edge_cases(self, name, price, quantity, efficiency, model, memory, color):
        """Parameterized test for smartphone edge cases"""
        phone = Smartphone(name, "Description", price, quantity, efficiency, model, memory, color)
        assert phone.name == name
        assert phone.price == price
        assert phone.quantity == quantity


class TestLawnGrass:
    """Tests for LawnGrass class"""

    @pytest.fixture
    def grass1(self):
        """Fixture for first lawn grass"""
        return LawnGrass(
            name="Газонная трава",
            description="Элитная трава для газона",
            price=500.0,
            quantity=20,
            country="Россия",
            germination_period="7 дней",
            color="Зеленый"
        )

    @pytest.fixture
    def grass2(self):
        """Fixture for second lawn grass"""
        return LawnGrass(
            name="Газонная трава 2",
            description="Выносливая трава",
            price=450.0,
            quantity=15,
            country="США",
            germination_period="5 дней",
            color="Темно-зеленый"
        )

    # Valid cases
    def test_lawn_grass_initialization(self, grass1):
        """Test that LawnGrass initializes correctly with all attributes"""
        assert grass1.name == "Газонная трава"
        assert grass1.description == "Элитная трава для газона"
        assert grass1.price == 500.0
        assert grass1.quantity == 20
        assert grass1.country == "Россия"
        assert grass1.germination_period == "7 дней"
        assert grass1.color == "Зеленый"

    def test_lawn_grass_inherits_from_product(self, grass1):
        """Test that LawnGrass inherits from Product class"""
        assert isinstance(grass1, LawnGrass)
        assert hasattr(grass1, 'name')
        assert hasattr(grass1, 'description')
        assert hasattr(grass1, 'price')
        assert hasattr(grass1, 'quantity')

    def test_lawn_grass_country_access(self, grass1):
        """Test that country attribute is accessible"""
        assert grass1.country == "Россия"

    def test_lawn_grass_color_access(self, grass2):
        """Test that color attribute is accessible"""
        assert grass2.color == "Темно-зеленый"

    def test_lawn_grass_germination_period_access(self, grass1):
        """Test that germination_period attribute is accessible"""
        assert grass1.germination_period == "7 дней"

    def test_lawn_grass_str_representation(self, grass1):
        """Test string representation of lawn grass"""
        expected = "Газонная трава, 500.0 руб. Остаток: 20 шт."
        assert str(grass1) == expected

    def test_lawn_grass_addition(self, grass1, grass2):
        """Test adding two lawn grasses"""
        # grass1 total: 500 * 20 = 10000
        # grass2 total: 450 * 15 = 6750
        # Total: 16750
        result = grass1 + grass2
        assert result == 16750.0

    def test_lawn_grass_addition_commutative(self, grass1, grass2):
        """Test that addition is commutative"""
        result1 = grass1 + grass2
        result2 = grass2 + grass1
        assert result1 == result2 == 16750.0

    # Edge cases
    def test_lawn_grass_with_minimal_values(self):
        """Test LawnGrass with minimal valid values"""
        grass = LawnGrass(
            name="G",
            description="Min",
            price=0.01,
            quantity=1,
            country="A",
            germination_period="1",
            color="C"
        )
        assert grass.name == "G"
        assert grass.price == 0.01
        assert grass.quantity == 1
        assert grass.country == "A"

    def test_lawn_grass_zero_quantity(self):
        """Test LawnGrass with zero quantity"""
        with pytest.raises(ValueError) as e:
            grass = LawnGrass(
            name="Out of stock",
            description="No stock",
            price=100.0,
            quantity=0,
            country="Russia",
            germination_period="7 days",
            color="Green"
        )
            assert "Товар с нулевым количеством не может быть добавлен" in e

    def test_lawn_grass_add_itself(self, grass1):
        """Test that adding lawn grass to itself raises AttributeError"""
        with pytest.raises(AttributeError, match="Cannot add product to itself"):
            grass1 + grass1

    # Invalid cases
    def test_lawn_grass_missing_required_attributes(self):
        """Test that missing required attributes raise TypeError"""
        with pytest.raises(TypeError):
            LawnGrass(
                name="Test",
                description="Test",
                price=100.0,
                quantity=5,
                # Missing country, germination_period, color
            )

    def test_lawn_grass_with_negative_price(self, capsys):
        """Test LawnGrass with negative price (should print warning)"""
        grass = LawnGrass(
            name="Test",
            description="Test",
            price=-100.0,
            quantity=5,
            country="Russia",
            germination_period="7 days",
            color="Green"
        )
        captured = capsys.readouterr()
        # Price can be set to negative, but setter should warn
        assert grass.price == -100.0

    def test_lawn_grass_with_negative_quantity(self):
        """Test LawnGrass with negative quantity"""
        grass = LawnGrass(
            name="Test",
            description="Test",
            price=100.0,
            quantity=-5,
            country="Russia",
            germination_period="7 days",
            color="Green"
        )
        assert grass.quantity == -5

    @pytest.mark.parametrize("name,price,quantity,country,germination_period,color", [
        ("", 100.0, 5, "R", "7d", "G"),  # Empty name
        ("Test", -50.0, 5, "R", "7d", "G"),  # Negative price
        ("Test", 100.0, -10, "R", "7d", "G"),  # Negative quantity
        ("Test", 100.0, 5, "", "7d", "G"),  # Empty country
        ("Test", 100.0, 5, "R", "", "G"),  # Empty germination period
        ("Test", 100.0, 5, "R", "7d", ""),  # Empty color
    ])
    def test_lawn_grass_parameterized_edge_cases(self, name, price, quantity, country, germination_period, color):
        """Parameterized test for lawn grass edge cases"""
        grass = LawnGrass(name, "Description", price, quantity, country, germination_period, color)
        assert grass.name == name
        assert grass.price == price
        assert grass.quantity == quantity

# Tests for cross-class addition (should fail)
class TestCrossClassAddition:
    """Tests for adding different product types"""

    @pytest.fixture
    def smartphone(self):
        return Smartphone(
            name="Phone",
            description="Test",
            price=100.0,
            quantity=5,
            efficiency=95.0,
            model="M",
            memory=128,
            color="Black"
        )

    @pytest.fixture
    def lawn_grass(self):
        return LawnGrass(
            name="Grass",
            description="Test",
            price=50.0,
            quantity=10,
            country="Russia",
            germination_period="7 days",
            color="Green"
        )

    def test_smartphone_plus_lawn_grass_raises_error(self, smartphone, lawn_grass):
        """Test that adding Smartphone and LawnGrass raises TypeError"""
        with pytest.raises(TypeError, match="Cannot add products from different classes"):
            smartphone + lawn_grass

    def test_lawn_grass_plus_smartphone_raises_error(self, smartphone, lawn_grass):
        """Test that adding LawnGrass and Smartphone raises TypeError"""
        with pytest.raises(TypeError, match="Cannot add products from different classes"):
            lawn_grass + smartphone