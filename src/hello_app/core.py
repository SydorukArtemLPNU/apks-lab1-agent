"""Pure functions of the application (no side effects)."""
from __future__ import annotations


def greet(name: str = "World") -> str:
    """Return a greeting for ``name``."""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Return the sum of ``a`` and ``b``."""
    return a + b
