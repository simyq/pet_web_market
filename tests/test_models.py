import json
from unittest.mock import mock_open, patch

import pytest

from src.models import Category, Order, Product, init_from_json


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
        assert len(category.products) == 67


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

        assert len(category.products) == 40
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


# Tests for Product and Category interaction
class TestProductCategoryInteraction:
    """Tests for interaction between Product and Category"""

    def setup_method(self):
        """Reset counters before each test"""
        Category.category_count = 0
        Category.product_count = 0


    def test_empty_product_list_in_category(self):
        """Test category with explicitly None products (should fail)"""
        with pytest.raises(TypeError):
            Category("Категория", "Описание", None)


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
    assert isinstance(category.products, str)
    assert isinstance(Category.category_count, int)
    assert isinstance(Category.product_count, int)
    assert category.name in str(category)


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
        all_categories = init_from_json("test.json")

        # Checking structure
        assert isinstance(all_categories, list)
        # Checking amount
        assert len(all_categories) == 2
        # # Checking 1st category
        assert "коммуникации" in all_categories[0].description
        assert len(all_categories[0].products) == 145
        # # Checking 2nd category
        assert "телевизор" in all_categories[1].description
        assert len(all_categories[1].products) == 41



def test_init_from_json_empty_categories():
    """Test JSON with empty categories list"""
    empty_json = '[]'

    with patch('builtins.open', mock_open(read_data=empty_json)):
        all_categories = init_from_json("empty.json")

        assert all_categories == []
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
        all_categories = init_from_json("no_products.json")

        assert len(all_categories) == 1
        assert all_categories[0].name == "Пустая категория"
        assert all_categories[0].products == ""


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
        all_categories = init_from_json("special.json")

        assert all_categories[0].name == "Категория с 'кавычками'"
        assert "переносом" in all_categories[0].description


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
        all_categories = init_from_json("single.json")

        assert len(all_categories) == 1
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
            all_categories = init_from_json("wrong_types.json")
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


# Parameterized test for different JSON structures
@pytest.mark.parametrize("json_data,expected_categories", [
    # Empty list
    ('[]', 0),
    # One category, one product
    ('''[{"name": "Cat", "description": "Desc", "products": [
        {"name": "Prod", "description": "Desc", "price": 100.0, "quantity": 1}
    ]}]''', 1),
    # One category, many products
    ('''[{"name": "Cat", "description": "Desc", "products": [
        {"name": "P1", "description": "D1", "price": 10.0, "quantity": 1},
        {"name": "P2", "description": "D2", "price": 20.0, "quantity": 2},
        {"name": "P3", "description": "D3", "price": 30.0, "quantity": 3}
    ]}]''', 1),
])
def test_init_from_json_parameterized(json_data, expected_categories):
    """Parameterized test for different JSON structures"""
    with patch('builtins.open', mock_open(read_data=json_data)):
        all_categories = init_from_json("test.json")

        assert len(all_categories) == expected_categories

        if expected_categories > 0:
            assert isinstance(all_categories[0], Category)


@pytest.fixture(autouse=True)
def reset_products_dict():
    """Reset the products dictionary before each test"""
    Product._Product__products_dict.clear()
    yield


# Tests for price getter
class TestPriceGetter:
    """Tests for price getter property"""

    def test_price_getter_valid(self):
        """Valid case: get price after initialization"""
        product = Product("Test", "Description", 100.0, 5)
        assert product.price == 100.0

    def test_price_getter_after_set(self):
        """Valid case: get price after setting new value"""
        product = Product("Test", "Description", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    @pytest.mark.parametrize("initial_price", [
        0.01,  # Min positive
        999999.99,  # Big num
        50,  # Integer
    ])
    def test_price_getter_parameterized(self, initial_price):
        """Parameterized test for different price values"""
        product = Product("Test", "Description", initial_price, 5)
        assert product.price == initial_price


# Tests for price setter
class TestPriceSetter:
    """Tests for price setter"""

    @pytest.mark.parametrize("initial_price,new_price", [
        (100.0, 150.0),  # Price increase
        (50.0, 75.5),  # Increase with float
        (200, 300),  # Integer
    ])
    def test_price_setter_increase_valid(self, initial_price, new_price, capsys):
        """Valid case: increase price"""
        product = Product("Test", "Description", initial_price, 5)
        product.price = new_price
        assert product.price == new_price
        captured = capsys.readouterr()
        assert captured.out == f"Product('Test', 'Description', {initial_price}, 5)\n"

    @pytest.mark.parametrize("initial_price,new_price", [
        (100.0, 50.0),  # Price decrease without message
        (200.0, 150.0),  # Price decrease
        (75.5, 70.0),  # Light decrease
    ])
    def test_price_setter_decrease_without_confirmation(self, initial_price, new_price, capsys):
        """Invalid case: decrease price without 'y' confirmation"""
        product = Product("Test", "Description", initial_price, 5)

        with patch('builtins.input', return_value='n'):
            product.price = new_price

        assert product.price == initial_price  # No price change

        captured = capsys.readouterr()
        assert "greater than the given price" in captured.out

    @pytest.mark.parametrize("initial_price,new_price,user_input", [
        (100.0, 50.0, 'y'),  # Eng "y"
        (200.0, 150.0, 'Y'),  # Capital "Y"
        (75.5, 70.0, '  y  '),  # With spaces
    ])
    def test_price_setter_decrease_with_confirmation(self, initial_price, new_price, user_input, capsys):
        """Valid case: decrease price with 'y' confirmation"""
        product = Product("Test", "Description", initial_price, 5)

        with patch('builtins.input', return_value=user_input):
            product.price = new_price

        assert product.price == new_price  # Price has been changed

        captured = capsys.readouterr()
        assert "greater than the given price" in captured.out

    @pytest.mark.parametrize("new_price", [
        0,  # Zero
        -1,  # Negative
        -100.5,  # Negative float
    ])
    def test_price_setter_non_positive(self, new_price, capsys):
        """Edge case: setting price <= 0"""
        product = Product("Test", "Description", 100.0, 5)
        product.price = new_price

        assert product.price == 100.0  # No price change

        captured = capsys.readouterr()
        assert "Price cannot be less than or equal to 0" in captured.out

    def test_price_setter_input_exception_handling(self, capsys):
        """Edge case: input() raises exception during confirmation"""
        product = Product("Test", "Description", 100.0, 5)

        with patch('builtins.input', side_effect=Exception("Input error")):
            product.price = 50.0

        assert product.price == 100.0  # No price change

        captured = capsys.readouterr()
        assert "greater than the given price" in captured.out


# Tests for new_product method
class TestNewProductMethod:
    """Tests for new_product class method"""

    def test_new_product_valid_new(self):
        """Valid case: create new product that doesn't exist"""
        product_dict = {
            'name': 'New Product',
            'description': 'Brand new product',
            'price': 150.0,
            'quantity': 10
        }

        product = Product.new_product(product_dict)

        assert isinstance(product, Product)
        assert product.name == 'New Product'
        assert product.description == 'Brand new product'
        assert product.price == 150.0
        assert product.quantity == 10

    def test_new_product_existing_product_update(self):
        """Valid case: update existing product"""
        # Creating the first product
        initial_dict = {
            'name': 'Existing Product',
            'description': 'Original description',
            'price': 100.0,
            'quantity': 5
        }
        first_product = Product.new_product(initial_dict)

        # Updating with new data
        update_dict = {
            'name': 'Existing Product',
            'description': 'Updated description (ignored)',
            'price': 80.0,
            'quantity': 3
        }
        updated_product = Product.new_product(update_dict)

        # Checking if this is the same object (before and after updating)
        assert updated_product is first_product

        # Checking new data
        assert updated_product.quantity == 8  # 5 + 3
        assert updated_product.price == 100.0  # max(100, 80) = 100
        # No description changes
        assert updated_product.description == 'Original description'

    def test_new_product_existing_with_higher_price(self):
        """Valid case: update existing product with higher price"""
        initial_dict = {
            'name': 'Product',
            'description': 'Desc',
            'price': 100.0,
            'quantity': 5
        }
        first_product = Product.new_product(initial_dict)

        update_dict = {
            'name': 'Product',
            'description': 'New',
            'price': 150.0,  # Выше
            'quantity': 3
        }
        updated_product = Product.new_product(update_dict)

        assert updated_product is first_product
        assert updated_product.quantity == 8
        assert updated_product.price == 150.0  # max(100, 150) = 150

    @pytest.mark.parametrize("missing_field", [
        'name',
        'description',
        'price',
        'quantity'
    ])
    def test_new_product_missing_fields(self, missing_field):
        """Invalid case: missing required fields in dictionary"""
        product_dict = {
            'name': 'Test',
            'description': 'Test Description',
            'price': 100.0,
            'quantity': 5
        }

        # KeyError Exception raise
        with pytest.raises(KeyError):
            for missing_field in ("name", "description", "price", "quantity"):
                del product_dict[missing_field]
                Product.new_product(product_dict)



    def test_new_product_empty_dict(self):
        """Edge case: empty dictionary"""
        with pytest.raises(KeyError):
            Product.new_product({})


    def test_new_product_multiple_updates(self):
        """Edge case: multiple updates to same product"""
        # 1st product
        product1 = Product.new_product({
            'name': 'Multi',
            'description': 'Original',
            'price': 100.0,
            'quantity': 10
        })

        # A bunch of updates
        updates = [
            {'price': 150.0, 'quantity': 5},  # Higher price
            {'price': 120.0, 'quantity': 3},  # Lower price (must be ignored)
            {'price': 200.0, 'quantity': 2},  # Higher price
        ]

        for update in updates:
            update_dict = {
                'name': 'Multi',
                'description': 'New',
                'price': update['price'],
                'quantity': update['quantity']
            }
            Product.new_product(update_dict)

        # Checking final data
        assert product1.quantity == 20  # 10 + 5 + 3 + 2
        assert product1.price == 200.0  # Max price

    def test_new_product_different_products_same_name(self):
        """Edge case: products with same name are considered same"""
        product1 = Product.new_product({
            'name': 'Same Name',
            'description': 'First',
            'price': 100.0,
            'quantity': 5
        })

        product2 = Product.new_product({
            'name': 'Same Name',
            'description': 'Second (ignored)',
            'price': 200.0,
            'quantity': 10
        })

        # Must be the same obj
        assert product2 is product1
        assert product1.quantity == 15
        assert product1.price == 200.0
        assert product1.description == 'First'  # No description change

    @pytest.mark.parametrize("initial_price,initial_qty,new_price,new_qty,expected_price,expected_qty", [
        (100.0, 5, 150.0, 3, 150.0, 8),  # New price is higher
        (200.0, 5, 150.0, 3, 200.0, 8),  # New price is lower
        (100.0, 0, 150.0, 5, 150.0, 5),  # Start value is 0
        (100.0, 5, 100.0, 10, 100.0, 15),  # Equal price
    ])
    def test_new_product_parameterized(self, initial_price, initial_qty, new_price, new_qty, expected_price,
                                       expected_qty):
        """Parameterized test for different update scenarios"""
        initial_dict = {
            'name': 'Param Product',
            'description': 'Test',
            'price': initial_price,
            'quantity': initial_qty
        }
        product = Product.new_product(initial_dict)

        update_dict = {
            'name': 'Param Product',
            'description': 'Updated',
            'price': new_price,
            'quantity': new_qty
        }
        result = Product.new_product(update_dict)

        assert result is product
        assert result.price == expected_price
        assert result.quantity == expected_qty

    def test_new_product_preserves_private_dict(self):
        """Test that __products_dict is updated correctly"""

        product1 = Product.new_product({
            'name': 'Product 1',
            'description': 'Desc 1',
            'price': 100.0,
            'quantity': 5
        })

        product2 = Product.new_product({
            'name': 'Product 2',
            'description': 'Desc 2',
            'price': 200.0,
            'quantity': 10
        })

        # Updating existent product
        Product.new_product({
            'name': 'Product 1',
            'description': 'New',
            'price': 150.0,
            'quantity': 3
        })

        # Check using private dict
        products_dict = Product._Product__products_dict
        assert len(products_dict) == 2
        assert products_dict['Product 1'] is product1
        assert products_dict['Product 2'] is product2
        assert products_dict['Product 1'].quantity == 8
        assert products_dict['Product 1'].price == 150.0


# Tests for add_product from Category class
class TestCategoryAddProduct:

    @pytest.mark.parametrize(
        "product_name, description, product_price, product_quantity, expected_count",
        [
            ("Test Product", "Description 1", 100.0, 5, 1),
            ("Another Product", "Description 1", 250.50, 10, 1),
            ("Cheap Product", "Description 1", 0.99, 100, 1),
        ],
        ids=["standard_product", "medium_price_product", "low_price_product"]
    )
    def test_add_product_increases_product_count(
            self,
            product_name,
            description,
            product_price,
            product_quantity,
            expected_count,
            empty_category
    ):
        """Check for counter increase"""
        initial_count = Category.product_count
        product = Product(product_name, description, product_price, product_quantity)
        empty_category.add_product(product)

        assert Category.product_count == initial_count + expected_count

    @pytest.mark.parametrize(
        "products_to_add, product_names",
        [
            (1, ["Product 1"]),
            (2, ["Product 1", "Product 2"]),
            (3, ["Product A", "Product B", "Product C"]),
        ],
        ids=["one_product", "two_products", "three_products"]
    )
    def test_add_product_products_accessible_in_getter(
            self,
            products_to_add,
            product_names,
            empty_category
    ):
        """Check for accessibility in getter"""
        products = []
        for name in product_names[:products_to_add]:
            product = Product(name, "description", 100.0, 5)
            products.append(product)
            empty_category.add_product(product)

        products_str = empty_category.products

        for i, product_name in enumerate(product_names[:products_to_add]):
            assert product_name in products_str


# Tests for products-getter from Category class
class TestCategoryProductsGetter:

    @pytest.mark.parametrize(
        "products_data, expected_strings",
        [
            (
                    [("Laptop", "Laptop", 1000.0, 5)],
                    'Laptop, 1000.0 руб. Остаток: 5 шт.'
            ),
            (
                    [("Mouse", "Mouse", 25.50, 10), ("Keyboard", "Keyboard", 75.0, 3)],
                    'Mouse, 25.5 руб. Остаток: 10 шт.\nKeyboard, 75.0 руб. Остаток: 3 шт.'
            ),
            (
                    [("Phone", "Phone", 500.0, 0), ("Case", "Case", 15.0, 20)],
                    'Phone, 500.0 руб. Остаток: 0 шт.\nCase, 15.0 руб. Остаток: 20 шт.'
            ),
        ],
        ids=["single_product", "two_products", "with_zero_stock"]
    )
    def test_products_getter_returns_formatted_strings(
            self,
            products_data,
            expected_strings
    ):
        """Test for string formatting in getter"""
        products = []
        for name, description, price, qty in products_data:
            products.append(Product(name, description, price, qty))
        category = Category("Test Category", "Test Description", products)

        result = category.products

        assert result == expected_strings


    @pytest.mark.parametrize(
        "products_data, index, expected_substring",
        [
            ([("Laptop", "Laptop", 1000.0, 5)], 0, "Laptop"),
            ([("Mouse", "Mouse", 25.50, 10), ("Keyboard", "Keyboard", 75.0, 3)], 1, "Keyboard"),
            ([("A", "A", 1.0, 1), ("B", "B", 2.0, 2), ("C", "C", 3.0, 3)], 2, "C"),
        ],
        ids=["first_product", "second_product", "third_product"]
    )
    def test_products_getter_contains_product_info(
            self,
            products_data,
            index,
            expected_substring
    ):
        """Check for correct substring of product info"""
        products = []
        for name, description, price, qty in products_data:
            products.append(Product(name, description, price, qty))
        category = Category("Test Category", "Test Description", products)

        result = category.products

        assert expected_substring in result


@pytest.fixture
def empty_category():
    """empty category fixture"""
    return Category("Test Category", "Test Description", [])


@pytest.fixture
def category_with_products():
    """Fixture for category with existing products"""
    products = [
        Product("Product 1", "Description 1", 100.0, 5),
        Product("Product 2", "Description 2", 200.0, 10),
        Product("Product 3", "Description 3", 300.0, 15)
    ]
    return Category("Test Category", "Test Description", products)


class TestProductAddMethod:
    """Tests for __add__ method of Product class"""

    def test_add_products_valid(self):
        """Valid case: sum of two products with positive quantities and prices"""
        product1 = Product("Product 1", "Description 1", 100.0, 5)
        product2 = Product("Product 2", "Description 2", 200.0, 3)

        result = product1 + product2

        assert result == 1100.0
        assert isinstance(result, float)

    def test_add_products_with_zero_quantity(self):
        """Edge case: one product has zero quantity"""
        product1 = Product("Product 1", "Description 1", 100.0, 0)
        product2 = Product("Product 2", "Description 2", 200.0, 3)

        result = product1 + product2

        assert result == 600.0

    def test_add_products_with_zero_price(self):
        """Edge case: one product has zero price"""
        product1 = Product("Product 1", "Description 1", 0.0, 5)
        product2 = Product("Product 2", "Description 2", 200.0, 3)

        result = product1 + product2

        assert result == 600.0

    def test_add_products_with_negative_values(self):
        """Invalid/Edge case: products with negative prices or quantities"""
        product1 = Product("Product 1", "Description 1", -100.0, 5)
        product2 = Product("Product 2", "Description 2", 200.0, 3)

        result = product1 + product2

        assert result == 100.0

    def test_add_products_with_float_values(self):
        """Valid case: products with float prices and quantities"""
        product1 = Product("Product 1", "Description 1", 99.99, 2)
        product2 = Product("Product 2", "Description 2", 149.99, 3)

        result = product1 + product2

        assert result == 649.95

    def test_add_product_with_itself(self):
        """Edge case: adding product to itself"""
        product = Product("Product", "Description", 100.0, 5)

        with pytest.raises(AttributeError):
            result = product + product

    def test_add_products_wrong_type_invalid(self):
        """Invalid case: adding Product with non-Product type"""
        product = Product("Product", "Description", 100.0, 5)

        with pytest.raises(TypeError):
            result = product + 100

        with pytest.raises(TypeError):
            result = product + "string"

        with pytest.raises(TypeError):
            result = product + None


class TestProductStrMethod:
    """Tests for __str__ method of Product class"""

    def test_str_product_valid(self):
        """Valid case: product string representation"""
        product = Product("Product 1", "Description 1", 100.0, 5)
        result = str(product)
        assert result == f"Product 1, 100.0 руб. Остаток: 5 шт."

    def test_str_product_edge(self):
        """Edge case: product string representation"""

        product = Product(None, None, None, None)
        assert str(product) == 'None, None руб. Остаток: None шт.'

    def test_str_product_invalid(self):
        """Invalid case: product string representation"""
        with pytest.raises(TypeError):
            product = Product("Description 1", 100.0, 5)


class TestProductReprMethod:
    """Tests for __repr__ method of Product class"""

    def test_repr_product_valid(self):
        """Valid case: product string representation"""
        product = Product("Product 1", "Description 1", 100.0, 5)
        result = repr(product)
        assert result == "Product('Product 1', 'Description 1', 100.0, 5)"

    def test_repr_product_edge(self):
        """Edge case: product string representation"""

        product = Product(None, None, None, None)
        assert repr(product) == 'Product(None, None, None, None)'

    def test_repr_product_invalid(self):
        """Invalid case: product string representation"""
        with pytest.raises(TypeError):
            product = Product("Description 1", 100.0, 5)


class TestCategoryStrMethod:
    """Tests for __str__ method of Category class"""

    def test_str_category_valid(self):
        """Valid case: category string representation"""

        category = Category("Test Category", "Test Description", [])
        result = str(category)
        assert result == 'Test Category, количество продуктов: 0 шт.'

    def test_str_category_edge(self):
        """Edge case: category string representation"""

        category = Category(None, "Test Description", [])
        result = str(category)
        assert result == 'None, количество продуктов: 0 шт.'

    def test_str_category_invalid(self):
        """Invalid case: category string representation"""

        with pytest.raises(TypeError):
            category = Category("Test Description", 100.0, 5)


class TestOrder:
    """Tests for Order class"""

    # Valid cases
    def test_order_initialization(self):
        """Test that Order initializes correctly with all attributes"""
        order = Order("Test Product", 5, 1000.0)

        assert order.name == "Test Product"
        assert order.quantity == 5
        assert order.price == 1000.0
        assert order.order_id == 1  # First order gets ID 1

    def test_order_str_representation(self):
        """Test __str__ method of Order"""
        order = Order("Laptop", 3, 150000.0)
        expected = f"Order id: 2. Product name: Laptop. Quantity: 3 Total price: 150000.0."
        assert str(order) == expected

    def test_order_multiple_instances_increment_id(self):
        """Test that order_id increments with each new order"""
        order3 = Order("Product 3", 2, 100.0)
        order4 = Order("Product 4", 1, 50.0)
        order5 = Order("Product 5", 5, 200.0)

        assert order3.order_id == 3
        assert order4.order_id == 4
        assert order5.order_id == 5

    def test_order_with_different_data_types(self):
        """Test Order with various data types"""
        order = Order("123", 10, 99.99)

        assert order.name == "123"
        assert order.quantity == 10
        assert order.price == 99.99

    # Edge cases
    def test_order_with_zero_quantity(self):
        """Test Order with zero quantity"""
        order = Order("Zero Product", 0, 100.0)

        assert order.quantity == 0
        assert order.price == 100.0

    def test_order_with_zero_price(self):
        """Test Order with zero price"""
        order = Order("Free Product", 10, 0.0)

        assert order.quantity == 10
        assert order.price == 0.0

    def test_order_with_negative_quantity(self):
        """Test Order with negative quantity (edge case)"""
        order = Order("Negative", -5, 100.0)

        assert order.quantity == -5
        assert order.price == 100.0

    def test_order_with_negative_price(self):
        """Test Order with negative price (edge case)"""
        order = Order("Discounted", 10, -50.0)

        assert order.quantity == 10
        assert order.price == -50.0

    def test_order_with_empty_string_name(self):
        """Test Order with empty string as name"""
        order = Order("", 5, 100.0)

        assert order.name == ""
        assert order.quantity == 5
        assert order.price == 100.0

    def test_order_with_special_characters_in_name(self):
        """Test Order with special characters in name"""
        order = Order("Product №123!@#", 5, 100.0)

        assert order.name == "Product №123!@#"
        assert order.quantity == 5

    def test_order_with_float_quantity(self):
        """Test Order with float quantity (edge case)"""
        order = Order("Float Quantity", 5.5, 100.0)

        assert order.quantity == 5.5
        assert order.price == 100.0


    # Invalid cases
    def test_order_missing_required_arguments(self):
        """Test that missing required arguments raise TypeError"""
        with pytest.raises(TypeError):
            Order("Test")  # Missing quantity and price

    def test_order_with_none_name(self):
        """Test Order with None as name"""
        order = Order(None, 5, 100.0)

        assert order.name is None
        assert order.quantity == 5
        assert order.price == 100.0

    def test_order_with_string_price(self):
        """Test Order with string price (should work but may cause issues)"""
        order = Order("Test", 5, "100.0")

        assert order.price == "100.0"  # No type conversion
        assert order.quantity == 5

    @pytest.mark.parametrize("name,quantity,price", [
        ("", 0, 0),
        (" ", 0, 0),
        ("Test", 1, 1.0),
        ("Test", 100, 1000.0),
        ("Test", 999999, 999999.99),
    ])
    def test_order_parameterized(self, name, quantity, price):
        """Parameterized test for Order with various valid inputs"""
        order = Order(name, quantity, price)

        assert order.name == name
        assert order.quantity == quantity
        assert order.price == price
