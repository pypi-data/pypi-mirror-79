# Hello Package

This is an example project demonstrating how to publish a Python package to PyPI.

## Installation

Run the followaing to install
```python
pip install hellopackage
```

## Usage

```python
from hello_package import hello_package

# Generate "Hello Package!"
say_hello()

# Generate "Hello, Python!"
say_hello("Python")
```

# Developing Hello Package

To install hellopackage, along waith tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```
