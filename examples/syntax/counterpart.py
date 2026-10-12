# mode: fun
from pyalamode import Map, Set, Vector

fee: int = 2

def add_fee(value: int) -> int:
    return value + fee

def prices() -> Vector[int]:
    values: Vector[int] = Vector.of(10, 20, 30)
    return values.map(add_fee)

def labels() -> Map[str, int]:
    values: Map[str, int] = Map.of(("tea", 3), ("coffee", 5))
    return values

def unique() -> Set[int]:
    return Set.of(3, 1, 3)

def empty_prices() -> Vector[int]:
    values: Vector[int] = Vector[int].of()
    return values
