from pyalamode import Vector, fun


@fun
def extend(values: Vector[int]) -> Vector[int]:
    values.appended(3)
    return values
