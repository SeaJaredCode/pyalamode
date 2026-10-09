from pyalamode import fun


def ordinary_factory():
    offset = 1

    @fun
    def calculation(value: int) -> int:
        return value + offset

    def change():
        nonlocal offset
        offset = 2

    return calculation, change
