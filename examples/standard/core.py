"""Bounded data workflows; provider setup belongs to the ordinary demo."""
# mode: fun
from pyalamode import (fun, Vector, OrderedMap, Result, Ok, Err, Failure, failure_value,
                      text_split, text_join, integer_parse_decimal, integer_format_decimal,
                      utf8_encode, utf8_decode, hex_encode, hex_decode, vector_scan,
                      vector_group_by, compose, partial_first, result_traverse,
                      effects, IO, IOCapability, Clock, ClockCapability,
                      Environment, EnvironmentCapability)


@fun
def parse_price(text: str) -> Result[int, Failure]:
    try:
        return Ok(integer_parse_decimal(text))
    except ValueError as caught:
        return Err(failure_value(caught))


@fun
def prices(text: str) -> Result[Vector[int], Failure]:
    pieces = text_split(text, ",")
    return result_traverse(pieces, parse_price)


@fun
def add(total: int, item: int) -> int:
    return total + item


@fun
def running_totals(values: Vector[int]) -> Vector[int]:
    return vector_scan(values, add, 0)


@fun
def parity(value: int) -> int:
    return value % 2


@fun
def groups(values: Vector[int]) -> OrderedMap[int, Vector[int]]:
    return vector_group_by(values, parity)


@fun
def multiply(rate: int, value: int) -> int:
    return rate * value


@fun
def increment(value: int) -> int:
    return value + 1


@fun
def adjusted(values: Vector[int], rate: int) -> Vector[int]:
    scaled = partial_first(multiply, rate)
    action = compose(increment, scaled)
    return values.map(action)


@fun
def wire(text: str) -> str:
    return hex_encode(utf8_encode(text))


@fun
def unwire(text: str) -> str:
    return utf8_decode(hex_decode(text))


@fun
def show(values: Vector[int]) -> str:
    pieces = values.map(integer_text)
    return text_join(pieces, ",")


@fun
def integer_text(value: int) -> str:
    return integer_format_decimal(value)


@effects(IO)
def read_prices(files: IOCapability, path: str) -> Result[Vector[int], Failure]:
    text = files.read_text(path)
    return prices(text)


@effects(Clock)
def timestamp(clock: ClockCapability) -> int:
    return clock.now_ns()


@effects(Environment)
def configuration(environment: EnvironmentCapability, name: str) -> str:
    return environment.get(name, "missing")
