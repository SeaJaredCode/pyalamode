"""Checked calls, recursion, tuples, defaults and closed callable captures."""
# mode: fun

from collections.abc import Callable
from examples.modules.constants import DEFAULT_FACTOR, LABELS, SERVICE_FEE


def quote(cents: int, discount_cents: int = 0) -> int:
    remainder = cents - discount_cents
    if remainder < 0:
        subtotal = 0
    else:
        subtotal = remainder
    return subtotal + SERVICE_FEE


def make_multiplier(factor: int = DEFAULT_FACTOR) -> Callable[[int], int]:
    def multiply(value: int) -> int:
        return value * factor
    return multiply


def scaled(value: int) -> int:
    return make_multiplier()(value)


def countdown_total(value: int) -> int:
    if value <= 0:
        return 0
    return value + countdown_total(value - 1)


def label_count(labels: tuple[str, ...] = LABELS) -> int:
    return len(labels)
