"""Ordinary runtime declarations; execution does not establish checked evidence."""

from sys import _getframe
from types import FunctionType
from typing import Callable, TypeVar
from .collections import Map, OrderedMap, Set, Vector
from .records import record, replace
from .sums import oneof, case, Option, Some, Nothing, Result, Ok, Err, accumulate
from .encoding import value_encode, value_decode
from .failures import Failure, failure_value
from .boundaries import dataclass_adapter, freeze, namedtuple_adapter, thaw
from .standard import (text_split, text_join, text_replace, text_startswith, text_slice,
                       integer_clamp, integer_parse_decimal, integer_format_decimal,
                       utf8_encode, utf8_decode, hex_encode, hex_decode, vector_scan,
                       vector_group_by, compose, partial_first, result_traverse)
from .effects import (effects, Effectful, IO, State, Clock, Random, Environment,
                      IOCapability, StateCapability, ClockCapability, RandomCapability,
                      EnvironmentCapability, borrow, live_io, recorded_io, state,
                      live_clock, recorded_clock, live_random, recorded_random,
                      live_environment, recorded_environment)

__version__ = "0.1.0"
_F = TypeVar("_F", bound=Callable[..., object])


def fun(function: _F) -> _F:
    """Return the original function unchanged, without checking or registration."""
    return function


class _TailCall:
    """Private request from a function body to rebind its parameters and continue."""
    __slots__ = ("arguments",)

    def __init__(self, arguments):
        self.arguments = arguments


def tailrec(function: _F) -> _F:
    """Run a self-tail-recursive function in constant stack depth.

    Unlike @fun, this is a wrapper. Calls from anywhere else run a driver
    loop. A call made directly by the function's own body frame is a tail
    call: it returns a private continuation that the driver unpacks. The
    checker proves that every such call is in tail position (PAL122), so
    plain Python and built artifacts behave identically.
    """
    if type(function) is not FunctionType:
        raise TypeError("tailrec decorates an ordinary function")
    body = function.__code__

    def driver(*arguments, **keywords):
        if _getframe(1).f_code is body:
            if keywords:
                raise TypeError("tail calls pass positional arguments only")
            return _TailCall(arguments)
        result = function(*arguments, **keywords)
        while type(result) is _TailCall:
            result = function(*result.arguments)
        return result

    for name in ("__module__", "__name__", "__qualname__", "__doc__"):
        setattr(driver, name, getattr(function, name))
    driver.__annotations__ = dict(function.__annotations__)
    driver.__wrapped__ = function
    return driver


def unsafe(*, scope: str, rationale: str):
    """Declare an ordinary unchecked adapter without wrapping or registration."""
    if type(scope) is not str or not scope.strip() or type(rationale) is not str or not rationale.strip():
        raise TypeError("unsafe scope and rationale require nonempty exact strings")
    def declaration(function):
        return function
    return declaration


__all__ = ["value_encode", "value_decode", "oneof", "case", "Option", "Some", "Nothing", "Result", "Ok", "Err", "accumulate", "Failure", "failure_value", "fun", "tailrec", "unsafe", "Vector", "OrderedMap", "Map", "Set", "record", "replace", "freeze", "thaw", "dataclass_adapter", "namedtuple_adapter", "effects", "Effectful", "IO", "State", "Clock", "Random", "Environment",
           "text_split", "text_join", "text_replace", "text_startswith", "text_slice",
           "integer_clamp", "integer_parse_decimal", "integer_format_decimal", "utf8_encode", "utf8_decode", "hex_encode", "hex_decode", "vector_scan", "vector_group_by", "compose", "partial_first", "result_traverse",
           "IOCapability", "StateCapability", "ClockCapability", "RandomCapability", "EnvironmentCapability",
           "borrow", "live_io", "recorded_io", "state", "live_clock", "recorded_clock", "live_random",
           "recorded_random", "live_environment", "recorded_environment"]
