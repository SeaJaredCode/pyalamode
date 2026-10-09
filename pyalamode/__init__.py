"""Ordinary runtime declarations; execution does not establish checked evidence."""

from typing import Callable, TypeVar
from .collections import Map, OrderedMap, Set, Vector

__version__ = "0.1.0"
_F = TypeVar("_F", bound=Callable[..., object])


def fun(function: _F) -> _F:
    """Return the original function unchanged, without checking or registration."""
    return function


__all__ = ["fun", "Vector", "OrderedMap", "Map", "Set"]
