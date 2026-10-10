from pyalamode import Vector
from .core import assemble

if __name__ == "__main__":
    first = Vector.of(-2, 3, 4)
    second = Vector.of(8, 9)
    print(assemble(first, second))
