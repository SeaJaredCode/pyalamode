from pyalamode import Vector, fun


@fun
def invalid() -> Vector[tuple[int, int]]:
    return Vector.of((1, [2]))
