
from hello_package import hello_package


def test_hello_package_no_params():
    assert hello_package() == "Hello, Package!"


def test_hello_package_with_params():
    assert hello_package("Dinkan") == "Hello, Dinkan"


