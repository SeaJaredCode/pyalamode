# mode: fun
from pyalamode import fun

print("An invalid functional module initializer; checking never executes this.")


@fun
def identity(value: int) -> int:
    return value
