"""A checked scalar core invoked by an ordinary Python shell."""

from pyalamode import fun


@fun
def discounted_total(cents: int, discount_cents: int) -> int:
    remainder = cents - discount_cents
    if remainder < 0:
        result = 0
    else:
        result = remainder
    return result


if __name__ == "__main__":
    # Exact scalar literals establish these same-file input contracts statically.
    # Printing is ordinary shell behavior outside the checked function.
    print(discounted_total(1500, 200))
    print(discounted_total(100, 200))
