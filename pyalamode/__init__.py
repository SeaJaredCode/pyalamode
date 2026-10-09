"""Ordinary runtime declarations; execution does not establish checked evidence."""

from typing import Callable, TypeVar
from .collections import Map, OrderedMap, Set, Vector
from .records import record, replace
from .variants import oneof, variant, case, Option, Some, Nothing, Result, Ok, Err, accumulate
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


def unsafe(*, scope: str, rationale: str):
    """Declare an ordinary unchecked adapter without wrapping or registration."""
    if type(scope) is not str or not scope.strip() or type(rationale) is not str or not rationale.strip():
        raise TypeError("unsafe scope and rationale require nonempty exact strings")
    def declaration(function):
        return function
    return declaration


__all__ = ["oneof", "variant", "case", "Option", "Some", "Nothing", "Result", "Ok", "Err", "accumulate", "Failure", "failure_value", "fun", "unsafe", "Vector", "OrderedMap", "Map", "Set", "record", "replace", "freeze", "thaw", "dataclass_adapter", "namedtuple_adapter", "effects", "Effectful", "IO", "State", "Clock", "Random", "Environment",
           "text_split", "text_join", "text_replace", "text_startswith", "text_slice",
           "integer_clamp", "integer_parse_decimal", "integer_format_decimal", "utf8_encode", "utf8_decode", "hex_encode", "hex_decode", "vector_scan", "vector_group_by", "compose", "partial_first", "result_traverse",
           "IOCapability", "StateCapability", "ClockCapability", "RandomCapability", "EnvironmentCapability",
           "borrow", "live_io", "recorded_io", "state", "live_clock", "recorded_clock", "live_random",
           "recorded_random", "live_environment", "recorded_environment"]
