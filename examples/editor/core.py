"""A small calculation core for diagnostics, hover and checked-call navigation."""
# mode: fun

from pyalamode import Vector


def discounted(cents: int, discount_cents: int) -> int:
    remainder = cents - discount_cents
    return max(0, remainder)


def quote(cents: int, discount_cents: int) -> int:
    subtotal = discounted(cents, discount_cents)
    total = subtotal + 200
    return total


def added(values: Vector[int], value: int) -> Vector[int]:
    revised = values.appended(value)
    return revised
