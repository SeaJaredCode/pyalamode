from pyalamode import fun


@fun
def broken(value: int) -> int:
    result = value + 1
    result = result + 1
    return result
