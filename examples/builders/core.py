from pyalamode import Vector, VectorBuilder, fun, vector_build

@fun
def positive(value: int) -> bool:
    return value > 0

@fun
def doubled(value: int) -> int:
    return value * 2

@fun
def assemble(first: Vector[int], second: Vector[int]) -> Vector[int]:
    def fill(out: VectorBuilder[int]) -> None:
        out.extend(first.filter(positive).map(doubled))
        out.append(-1)
        out.extend(second)
    return vector_build(fill)
