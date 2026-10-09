"""The ordinary shell prints results; it receives no checked purity claim."""

from pyalamode import Map, OrderedMap, Set
from .core import START, adjusted, amounts_by_key, revise, selected, sum_values

new = START.appended(30)
print(START)
print(adjusted(new, 5))
print(sum_values(new))
print(amounts_by_key(Map.of(("pears", 200), ("apples", 130))))
print(revise(OrderedMap.of(("bananas", 80), ("apples", 100))))
print(selected(Set.of("bananas", "apples")))
