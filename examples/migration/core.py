"""Copy this file into an isolated project for the migration walkthrough."""
from pyalamode import fun


@fun
def total(price: int, quantity: int) -> int:
    result = price * quantity
    result = result + 100
    return result


def doubled(value: int) -> int:
    return value * 2
