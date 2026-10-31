from hello_app.core import add, greet


def test_BasicAddition() -> None:
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_greet_default() -> None:
    assert greet() == "Hello, World!"


def test_greet_name() -> None:
    assert greet("Lab") == "Hello, Lab!"
