from pyalamode import Vector, freeze, fun


@fun
def count(values: Vector[int]) -> int:
    return len(values)


def shell(raw):
    snapshot = freeze(raw, schema=Vector[int])
    return count(snapshot)
