from pyalamode import Vector, fun


def log(value: int) -> int:
    print(value)
    return value


@fun
def invalid(values: Vector[int]) -> Vector[int]:
    return values.map(log)
