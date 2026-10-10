"""Finite ordinary Vector construction with one-way callback lifetime tokens.

Source confinement and callback purity are static/caller obligations. Runtime
generic arguments are erased. Private reflection or mutation of product/native
dependencies violates the ownership contract; this is not security isolation.
"""

import _thread
from types import GenericAlias
from . import collections as _collections

__all__ = ["VectorBuilder", "vector_build"]


def _live(builder):
    if type(builder) is not VectorBuilder:
        _collections._invalid("builder", "expected exact VectorBuilder")
    try:
        active = object.__getattribute__(builder, "_active")
        owner = object.__getattribute__(builder, "_owner")
        busy = object.__getattribute__(builder, "_busy")
    except AttributeError:
        _collections._invalid("builder", "malformed construction token")
    if type(active) is not bool or type(owner) is not int or type(busy) is not bool:
        _collections._invalid("builder", "malformed construction token")
    if not active:
        raise RuntimeError("builder: construction is no longer active")
    if owner != _thread.get_ident():
        raise RuntimeError("builder: construction belongs to its creating thread")
    if busy:
        raise RuntimeError("builder: operation is already active")
    try:
        items = object.__getattribute__(builder, "_items")
    except AttributeError:
        _collections._invalid("builder", "malformed construction storage")
    if type(items) is not list:
        _collections._invalid("builder", "malformed construction storage")
    return items


def _close(builder):
    # Revocation precedes every read/clear of the staging payload. Discarded
    # valid contents have no foreign finalizer under the dependency contract.
    object.__setattr__(builder, "_active", False)
    object.__setattr__(builder, "_busy", False)
    try:
        try:
            items = object.__getattribute__(builder, "_items")
        except AttributeError:
            items = None
        if type(items) is list:
            items.clear()
    finally:
        object.__setattr__(builder, "_items", None)


class VectorBuilder:
    """Exact confined callback parameter; never stable data or a public factory."""
    __slots__ = ("_active", "_owner", "_busy", "_items")
    __hash__ = None

    def __init__(self, *args, **kwargs):
        _collections._invalid("VectorBuilder", "use vector_build; direct construction is unsupported")

    def __init_subclass__(cls, **kwargs):
        _collections._invalid("VectorBuilder", "exact construction subclasses are unsupported")

    def __setattr__(self, name, value):
        raise AttributeError("opaque builder attributes cannot be assigned")

    def __delattr__(self, name):
        raise AttributeError("opaque builder attributes cannot be deleted")

    @classmethod
    def __class_getitem__(cls, arguments):
        return GenericAlias(cls, arguments)

    def append(self, value, /):
        items = _live(self)
        object.__setattr__(self, "_busy", True)
        try:
            _collections._validate(value, "append.value")
            items.append(value)
        finally:
            object.__setattr__(self, "_busy", False)

    def extend(self, values, /):
        items = _live(self)
        object.__setattr__(self, "_busy", True)
        try:
            if type(values) is not _collections.Vector:
                _collections._invalid("extend.values", "expected exact Vector")
            _collections._validate(values, "extend.values")
            source = _collections._storage(values, "_items", "extend.values")
            items.extend(source)
        finally:
            object.__setattr__(self, "_busy", False)


def vector_build(callback, /):
    """Invoke an exact function once; publish one stable Vector after cleanup.

    This does not inspect annotations or establish callback purity/confinement.
    Each ordinary invocation gets fresh storage, with no function registry.
    """
    _collections._function(callback)
    builder = object.__new__(VectorBuilder)
    object.__setattr__(builder, "_active", True)
    object.__setattr__(builder, "_owner", _thread.get_ident())
    object.__setattr__(builder, "_busy", False)
    object.__setattr__(builder, "_items", [])
    try:
        returned = callback(builder)
        if returned is not None:
            _collections._invalid("callback", "construction callback must return exact None")
        items = _live(builder)
        object.__setattr__(builder, "_busy", True)
        result = _collections._new(_collections.Vector, "_items", tuple(items))
        _collections._validate(result, "result")
    finally:
        _close(builder)
    return result
