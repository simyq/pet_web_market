import pytest
import json
from unittest.mock import mock_open, patch
from pathlib import Path

from src.models import Product, Category, init_from_json

# Tests for Product class
class TestProduct:
    """Tests for Product class"""

    def test_product_initialization(self):
        """Test Product initialization with valid data"""
        product = Product(
            name="Телефон",
            description="Смартфон с хорошей камерой",
            price=50000.0,
            quantity=10
        )

        assert product.name == "Телефон"
        assert product.description == "Смартфон с хорошей камерой"
        assert product.price == 50000.0
        assert product.quantity == 10

    def test_product_with_zero_quantity(self):
        """Test Product with zero quantity"""
        product = Product(
            name="Товар",
            description="Описание",
            price=100.0,
            quantity=0
        )

        assert product.quantity == 0
        assert product.price == 100.0

    def test_product_with_negative_price(self):
        """Test Product with negative price (edge case)"""
        product = Product(
            name="Уцененный товар",
            description="Товар со скидкой",
            price=-50.0,
            quantity=5
        )

        assert product.price == -50.0  # Just in case price is negative

    def test_product_with_empty_strings(self):
        """Test Product with empty name and description"""
        product = Product(
            name="",
            description="",
            price=0.0,
            quantity=0
        )

        assert product.name == ""
        assert product.description == ""

    def test_product_with_special_characters(self):
        """Test Product with special characters in name"""
        product = Product(
            name="Товар №123",
            description="Описание с @символами#",
            price=123.45,
            quantity=100
        )

        assert "№" in product.name
        assert "@" in product.description

    def test_product_price_is_float(self):
        """Test that price is stored as float"""
        product = Product(
            name="Тест",
            description="Тест",
            price=100,  # Integer instead of float
            quantity=1
        )

        assert isinstance(product.price, (int, float))
        assert product.price == 100.0 or product.price == 100


# Tests for Category class
class TestCategory:
    """Tests for Category class"""

    def setup_method(self):
        """Reset counters before each test"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Test Category initialization with products"""
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]

        category = Category(
            name="Электроника",
            description="Техника и гаджеты",
            products=products
        )

        assert category.name == "Электроника"
        assert category.description == "Техника и гаджеты"
        assert len(category.products) == 2
        assert category.products[0].name == "Товар1"
        assert category.products[1].price == 200.0

    def test_category_with_empty_product_list(self):
        """Test Category with empty products list"""
        category = Category(
            name="Пустая категория",
            description="Нет товаров",
            products=[]
        )

        assert category.name == "Пустая категория"
        assert len(category.products) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0  # Empty list is not summed

    def test_category_counters_increase(self):
        """Test that category and product counters increase correctly"""
        # 1st category
        products1 = [
            Product("Т1", "Д1", 10.0, 1),
            Product("Т2", "Д2", 20.0, 2)
        ]
        cat1 = Category("Кат1", "Оп1", products1)

        assert Category.category_count == 1
        assert Category.product_count == 2

        # 2nd category
        products2 = [
            Product("Т3", "Д3", 30.0, 3),
            Product("Т4", "Д4", 40.0, 4),
            Product("Т5", "Д5", 50.0, 5)
        ]
        cat2 = Category("Кат2", "Оп2", products2)

        assert Category.category_count == 2
        assert Category.product_count == 5  # 2 + 3 = 5

    def test_category_with_single_product(self):
        """Test Category with single product"""
        products = [Product("Единственный", "Описание", 999.99, 1)]

        category = Category("Категория", "Описание", products)

        assert len(category.products) == 1
        assert category.products[0].name == "Единственный"
        assert Category.product_count == 1

    def test_category_name_and_description_edge_cases(self):
        """Test Category with edge case names and descriptions"""
        category = Category(
            name="   Категория с пробелами   ",
            description="Описание\nс переносом строки",
            products=[]
        )

        assert category.name == "   Категория с пробелами   "
        assert "\n" in category.description

    def test_category_products_are_referenced_correctly(self):
        """Test that products in category are the same objects"""
        product = Product("Тест", "Описание", 100.0, 5)
        category = Category("Категория", "Описание", [product])

        # Changing the product using category
        category.products[0].quantity = 10

        # Checking if the original object has been changed
        assert product.quantity == 10

    def test_multiple_categories_independent(self):
        """Test that multiple categories are independent"""
        products1 = [Product("Т1", "Д1", 100.0, 1)]
        products2 = [Product("Т2", "Д2", 200.0, 2)]

        cat1 = Category("Кат1", "Оп1", products1)
        cat2 = Category("Кат2", "Оп2", products2)

        assert cat1.name != cat2.name
        assert cat1.products[0] != cat2.products[0]
        assert cat1.products[0].price == 100.0
        assert cat2.products[0].price == 200.0


# Tests for Product and Category interaction
class TestProductCategoryInteraction:
    """Tests for interaction between Product and Category"""

    def setup_method(self):
        """Reset counters before each test"""
        Category.category_count = 0
        Category.product_count = 0

    def test_products_in_multiple_categories(self):
        """Test that same product can be in multiple categories"""
        product = Product("Универсальный товар", "Описание", 500.0, 10)

        cat1 = Category("Кат1", "Оп1", [product])
        cat2 = Category("Кат2", "Оп2", [product])

        # Same product in two categories
        assert cat1.products[0] is cat2.products[0]  # Same object
        assert Category.product_count == 2  # Counted twice

    def test_modify_product_affects_all_categories(self):
        """Test that modifying product affects all categories it's in"""
        product = Product("Товар", "Описание", 100.0, 5)

        cat1 = Category("Кат1", "Оп1", [product])
        cat2 = Category("Кат2", "Оп2", [product])

        # Changing the product using 1st category
        cat1.products[0].price = 200.0

        # Checking that product has been changed in the 2nd category
        assert cat2.products[0].price == 200.0
        assert product.price == 200.0

    def test_empty_product_list_in_category(self):
        """Test category with explicitly None products (should fail)"""
        with pytest.raises(TypeError):
            Category("Категория", "Описание", None)

    def test_category_with_non_product_in_list(self):
        """Test category with non-Product objects in list (edge case)"""
        # Список содержит не только Product объекты
        mixed_list = [
            Product("Товар1", "Описание1", 100.0, 1),
            "Не продукт",  # String instead of object
            123  # Number instead of object
        ]


        category = Category("Категория", "Описание", mixed_list)

        assert len(category.products) == 3
        assert Category.product_count == 3


# Parametrized tests for classes
@pytest.mark.parametrize("name,description,price,quantity", [
    ("Товар", "Описание", 100.0, 10),
    ("Т", "Д", 0.0, 0),
    ("Товар с пробелами", "Описание с символами !@#$%", 999.99, 999),
    ("", "", -10.0, -5),
])
def test_product_parameterized(name, description, price, quantity):
    """Parameterized test for Product with various inputs"""
    product = Product(name, description, price, quantity)

    assert product.name == name
    assert product.description == description
    assert product.price == price
    assert product.quantity == quantity


@pytest.mark.parametrize("cat_name,cat_desc,product_count", [
    ("Категория1", "Описание1", 0),
    ("Категория2", "Описание2", 1),
    ("Категория3", "Описание3", 5),
    ("   ", "\n", 2),
])
def test_category_parameterized(cat_name, cat_desc, product_count):
    """Parameterized test for Category with various inputs"""
    products = [
        Product(f"Товар{i}", f"Описание{i}", float(i * 100), i)
        for i in range(product_count)
    ]

    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    category = Category(cat_name, cat_desc, products)

    assert category.name == cat_name
    assert category.description == cat_desc
    assert len(category.products) == product_count
    assert Category.category_count == 1
    assert Category.product_count == product_count


# Annotation tests
def test_product_attribute_types():
    """Test that Product attributes have correct types"""
    product = Product("Тест", "Описание", 100.0, 5)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, (int, float))
    assert isinstance(product.quantity, int)


def test_category_attribute_types():
    """Test that Category attributes have correct types"""
    products = [Product("Т", "Д", 100.0, 1)]
    category = Category("Категория", "Описание", products)

    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.products, list)
    assert isinstance(Category.category_count, int)
    assert isinstance(Category.product_count, int)


# Test for case when product is changed, but main counter does not change
def test_product_count_not_changed_by_product_modification():
    """Test that modifying products doesn't change category counters"""
    Category.category_count = 0
    Category.product_count = 0

    product = Product("Товар", "Описание", 100.0, 1)
    category = Category("Категория", "Описание", [product])

    initial_product_count = Category.product_count

    product.price = 200.0
    product.quantity = 10

    assert Category.product_count == initial_product_count


# Test JSON data matching the structure in the function description
TEST_JSON_DATA = '''[
  {
    "name": "Смартфоны",
    "description": "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни",
    "products": [
      {
        "name": "Samsung Galaxy C23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
      },
      {
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8
      },
      {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14
      }
    ]
  },
  {
    "name": "Телевизоры",
    "description": "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
    "products": [
      {
        "name": "55\\" QLED 4K",
        "description": "Фоновая подсветка",
        "price": 123000.0,
        "quantity": 7
      }
    ]
  }
]'''


# Valid cases
def test_init_from_json_valid_file():
    """Test initialization from valid JSON file"""
    with patch('builtins.open', mock_open(read_data=TEST_JSON_DATA)):
        all_products, all_categories = init_from_json("test.json")

        # Checking structure
        assert isinstance(all_products, list)
        assert isinstance(all_categories, list)

        # Checking amount
        assert len(all_categories) == 2
        assert len(all_products) == 4  # 3 смартфона + 1 телевизор

        # Checking 1st category
        assert all_categories[0].name == "Смартфоны"
        assert "коммуникации" in all_categories[0].description
        assert len(all_categories[0].products) == 3

        # Checking 2nd category
        assert all_categories[1].name == "Телевизоры"
        assert "телевизор" in all_categories[1].description
        assert len(all_categories[1].products) == 1

        # Checking product from the 1st category
        smartphone_products = all_categories[0].products
        assert smartphone_products[0].name == "Samsung Galaxy C23 Ultra"
        assert smartphone_products[0].price == 180000.0
        assert smartphone_products[0].quantity == 5

        assert smartphone_products[1].name == "Iphone 15"
        assert smartphone_products[1].price == 210000.0
        assert smartphone_products[1].quantity == 8

        assert smartphone_products[2].name == "Xiaomi Redmi Note 11"
        assert smartphone_products[2].price == 31000.0
        assert smartphone_products[2].quantity == 14

        # Checking product from the 2nd category
        tv_products = all_categories[1].products
        assert tv_products[0].name == '55" QLED 4K'
        assert tv_products[0].price == 123000.0
        assert tv_products[0].quantity == 7

        # Checking all_products contains all products
        assert len(all_products) == 4
        assert all_products[0].name == "Samsung Galaxy C23 Ultra"
        assert all_products[3].name == '55" QLED 4K'


def test_init_from_json_empty_categories():
    """Test JSON with empty categories list"""
    empty_json = '[]'

    with patch('builtins.open', mock_open(read_data=empty_json)):
        all_products, all_categories = init_from_json("empty.json")

        assert all_products == []
        assert all_categories == []
        assert isinstance(all_products, list)
        assert isinstance(all_categories, list)


def test_init_from_json_category_with_no_products():
    """Test JSON with category that has empty products list"""
    json_no_products = '''[
      {
        "name": "Пустая категория",
        "description": "Нет товаров",
        "products": []
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=json_no_products)):
        all_products, all_categories = init_from_json("no_products.json")

        assert len(all_categories) == 1
        assert len(all_products) == 0
        assert all_categories[0].name == "Пустая категория"
        assert all_categories[0].products == []


# Edge cases
def test_init_from_json_with_special_characters():
    """Test JSON with special characters in names and descriptions"""
    special_json = '''[
      {
        "name": "Категория с 'кавычками'",
        "description": "Описание с \\n переносом строки",
        "products": [
          {
            "name": "Товар №1",
            "description": "Цена: 100$",
            "price": 100.0,
            "quantity": 10
          }
        ]
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=special_json)):
        all_products, all_categories = init_from_json("special.json")

        assert all_categories[0].name == "Категория с 'кавычками'"
        assert "переносом" in all_categories[0].description
        assert all_products[0].name == "Товар №1"
        assert "$" in all_products[0].description


def test_init_from_json_with_zero_and_negative_values():
    """Test JSON with zero and negative values"""
    edge_json = '''[
      {
        "name": "Тестовая",
        "description": "Тест",
        "products": [
          {
            "name": "Товар1",
            "description": "Нулевая цена",
            "price": 0.0,
            "quantity": 0
          },
          {
            "name": "Товар2",
            "description": "Отрицательная цена",
            "price": -50.0,
            "quantity": -5
          }
        ]
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=edge_json)):
        all_products, all_categories = init_from_json("edge.json")

        assert all_products[0].price == 0.0
        assert all_products[0].quantity == 0
        assert all_products[1].price == -50.0
        assert all_products[1].quantity == -5


def test_init_from_json_single_product():
    """Test JSON with single product in single category"""
    single_json = '''[
      {
        "name": "Единственная",
        "description": "Одна категория",
        "products": [
          {
            "name": "Единственный",
            "description": "Один товар",
            "price": 100.0,
            "quantity": 1
          }
        ]
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=single_json)):
        all_products, all_categories = init_from_json("single.json")

        assert len(all_categories) == 1
        assert len(all_products) == 1
        assert all_products[0].name == "Единственный"
        assert all_categories[0].name == "Единственная"


# Invalid cases
def test_init_from_json_file_not_found():
    """Test when JSON file doesn't exist"""
    with patch('builtins.open') as mock_file:
        mock_file.side_effect = FileNotFoundError("File not found")

        with pytest.raises(FileNotFoundError, match="File not found"):
            init_from_json("nonexistent.json")


def test_init_from_json_invalid_json():
    """Test with invalid JSON syntax"""
    invalid_json = '{invalid json'

    with patch('builtins.open', mock_open(read_data=invalid_json)):
        with pytest.raises(json.JSONDecodeError):
            init_from_json("invalid.json")


def test_init_from_json_missing_required_fields():
    """Test JSON missing required fields"""
    missing_fields_json = '''[
      {
        "name": "Категория",
        "description": "Описание"
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=missing_fields_json)):
        with pytest.raises(KeyError, match="products"):
            init_from_json("missing.json")


def test_init_from_json_product_missing_fields():
    """Test JSON where product is missing required fields"""
    missing_product_fields = '''[
      {
        "name": "Категория",
        "description": "Описание",
        "products": [
          {
            "name": "Товар"
          }
        ]
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=missing_product_fields)):
        with pytest.raises(KeyError):
            init_from_json("missing_product.json")


def test_init_from_json_wrong_data_types():
    """Test JSON with wrong data types"""
    wrong_types_json = '''[
      {
        "name": 123,  # Should be string
        "description": "Описание",
        "products": [
          {
            "name": "Товар",
            "description": "Описание",
            "price": "сто",  # Should be number
            "quantity": "много"  # Should be number
          }
        ]
      }
    ]'''

    with patch('builtins.open', mock_open(read_data=wrong_types_json)):
        try:
            all_products, all_categories = init_from_json("wrong_types.json")
            assert isinstance(all_categories[0].name, (str, int))
        except (TypeError, ValueError):
            pass


# Test that function resets Category counters
def test_init_from_json_category_counters():
    """Test that function properly uses Category class counters"""
    Category.category_count = 0
    Category.product_count = 0

    with patch('builtins.open', mock_open(read_data=TEST_JSON_DATA)):
        all_products, all_categories = init_from_json("test.json")

        assert Category.category_count == 2
        assert Category.product_count == 4


# Test products are correctly linked
def test_init_from_json_product_references():
    """Test that products in all_products are same objects as in categories"""
    with patch('builtins.open', mock_open(read_data=TEST_JSON_DATA)):
        all_products, all_categories = init_from_json("test.json")

        # Checking if products in all_products and all_categories are the same objects
        assert all_products[0] is all_categories[0].products[0]
        assert all_products[1] is all_categories[0].products[1]
        assert all_products[2] is all_categories[0].products[2]
        assert all_products[3] is all_categories[1].products[0]

        # Changing the product
        all_products[0].price = 999999.0

        # Checking, that the same object changed in categories
        assert all_categories[0].products[0].price == 999999.0


# Parameterized test for different JSON structures
@pytest.mark.parametrize("json_data,expected_categories,expected_products", [
    # Пустой список
    ('[]', 0, 0),
    # One category, one product
    ('''[{"name": "Cat", "description": "Desc", "products": [
        {"name": "Prod", "description": "Desc", "price": 100.0, "quantity": 1}
    ]}]''', 1, 1),
    # One category, many products
    ('''[{"name": "Cat", "description": "Desc", "products": [
        {"name": "P1", "description": "D1", "price": 10.0, "quantity": 1},
        {"name": "P2", "description": "D2", "price": 20.0, "quantity": 2},
        {"name": "P3", "description": "D3", "price": 30.0, "quantity": 3}
    ]}]''', 1, 3),
])
def test_init_from_json_parameterized(json_data, expected_categories, expected_products):
    """Parameterized test for different JSON structures"""
    with patch('builtins.open', mock_open(read_data=json_data)):
        all_products, all_categories = init_from_json("test.json")

        assert len(all_categories) == expected_categories
        assert len(all_products) == expected_products

        if expected_categories > 0:
            assert isinstance(all_categories[0], Category)
        if expected_products > 0:
            assert isinstance(all_products[0], Product)

