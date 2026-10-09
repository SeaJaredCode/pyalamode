"""Ordinary shell; normal execution creates no checked claim."""
from pyalamode import Vector
from .core import quote, added

print(quote(1500, 400))
original = Vector.of(1, 2)
print(original)
print(added(original, 3))
