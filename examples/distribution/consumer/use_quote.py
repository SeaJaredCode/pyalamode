from pyalamode import fun
from checked_pricing.core import quote

@fun
def total(quantity: int) -> int:
    return quote(quantity)
