"""Checked collection calculations with persistent versions and explicit order."""
# mode: fun

from pyalamode import Map, OrderedMap, Set, Vector

START = Vector.of(10, 20)


def adjusted(values: Vector[int], delta: int) -> Vector[int]:
    def increase(value: int) -> int:
        return value + delta
    return values.map(increase)


def sum_values(values: Vector[int]) -> int:
    def add(total: int, value: int) -> int:
        return total + value
    return values.fold(add, 0)


def amounts_by_key(prices: Map[str, int]) -> Vector[int]:
    def amount(entry: tuple[str, int]) -> int:
        return entry[1]
    return prices.ordered_entries().map(amount)


def revise(prices: OrderedMap[str, int]) -> OrderedMap[str, int]:
    return prices.updated("apples", 130).updated("pears", 200)


def selected(labels: Set[str]) -> Vector[str]:
    return labels.added("pears").difference(Set.of("bananas")).ordered_values()
