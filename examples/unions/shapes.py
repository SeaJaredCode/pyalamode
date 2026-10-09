"""Closed tagged sums (@oneof) and closed unions (A | B) side by side."""
from pyalamode import fun, oneof, case, record


@record
class Point:
    x: int
    y: int


@oneof
class Shape:
    @case
    class Circle:
        radius: int

    @case
    class Square:
        side: int


@fun
def size(value: Shape | Point | int | None) -> int:
    match value:
        case Shape.Circle(radius=r):
            return r * 2
        case Shape.Square(side=s):
            return s
        case Point(x=x, y=y):
            return x + y
        case int(n):
            return n
        case None:
            return 0


@fun
def first_positive(a: int, b: int) -> int | None:
    if a > 0:
        return a
    if b > 0:
        return b
    return None


if __name__ == "__main__":
    print(size(Shape.Circle(3)), size(Shape.Square(4)), size(Point(1, 2)), size(7), size(None))
    print(first_positive(-1, 5), first_positive(-1, -2))
