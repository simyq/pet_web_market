# Web market
Pet project. Work in progress. Current test coverage 99%.

## Content (main modules)

### [Main](main.py) — main module of the program

### [Src](src/) — directory for modules
- [Models](src/models.py) — contains main classes (Products, Categories) for building logic in web market 
- [Products](src/products.py) — Using the main Products class by building subclasses. Since this is just a pet project, there is no need to create many product classes.
### [Tests](tests/) — directory for tests
- [test_models](tests/test_models.py)
- [test_products](tests/test_products.py)
### [Data](data/) — directory for data files

## Installation:

### Prerequisites
- Python 3.13+
- Poetry 2.2+

All the required packages (linters and other dependencies) and environments are described in [pyproject.toml](pyproject.toml)  

1. Clone repository:
```
git clone https://github.com/simyq/pet_web_market
```
2. Install and activate virtual environment:
```
poetry install
poetry shell
```
3. Run main.py
```
python main.py
```