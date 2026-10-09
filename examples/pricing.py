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
    print(discounted_total(1500, 200))
