"""Ordinary-shell snapshots, independent exports, and selected data assertions.

``exclusive=True`` is a caller assertion, not detected ownership or a lock.
No application annotation, constructor, iterator, property, or restoration hook
is evaluated while converting data. Named adapters have a finite qualifier.
"""

import collections as _stdlib_collections
import dataclasses as _dataclasses
from types import CodeType, FunctionType, GetSetDescriptorType
from . import collections as _collections
from . import records as _records

__all__ = ["freeze", "thaw", "dataclass_adapter", "namedtuple_adapter", "validate_data"]


def validate_data(value, schema, *, path="value"):
    """Validate checker-produced closed schema data and return the same value.

    This proves supported exact data shape only; it proves neither callback
    purity, exclusive ownership, nor unchanged dependencies.
    """
    if type(path) is not str:
        _collections._invalid("path", "expected exact string")
    schema = _records._canonical(schema)
    _records._check_schema(schema)
    _records._validate_schema(value, schema, path)
    return value


class _SnapshotAdapter:
    __slots__ = ("_source", "_target", "_kind", "_names", "_getter")

    def __setattr__(self, name, value):
        raise AttributeError("snapshot adapter metadata is immutable")

    def __delattr__(self, name):
        raise AttributeError("snapshot adapter metadata is immutable")

    def __init_subclass__(cls, **kwargs):
        raise TypeError("snapshot adapters cannot be subclassed")


def _adapter(source, target, kind, names, getter=None):
    value = object.__new__(_SnapshotAdapter)
    for name, item in (("_source", source), ("_target", target), ("_kind", kind), ("_names", names), ("_getter", getter)):
        object.__setattr__(value, name, item)
    return value


def _validate_adapter(adapter):
    try:
        source = object.__getattribute__(adapter, "_source")
        target = object.__getattribute__(adapter, "_target")
        kind = object.__getattribute__(adapter, "_kind")
        names = object.__getattribute__(adapter, "_names")
        getter = object.__getattribute__(adapter, "_getter")
    except AttributeError:
        _collections._invalid("adapter", "malformed snapshot adapter metadata")
    info = _records._record_info(target)
    if type(source) is not type or info is None or type(kind) is not str or kind not in ("dataclass", "namedtuple") or type(names) is not tuple or any(type(name) is not str for name in names) or names != tuple(name for name, _ in info[1]):
        _collections._invalid("adapter", "malformed snapshot adapter metadata")
    if kind == "dataclass" and (type(getter) is not GetSetDescriptorType or getter.__objclass__ is not source):
        _collections._invalid("adapter", "malformed dataclass storage descriptor")
    if kind == "namedtuple" and getter is not None:
        _collections._invalid("adapter", "malformed namedtuple storage descriptor")


def _source_metadata(source, target, base):
    if type(source) is not type:
        _collections._invalid("adapter", "source requires an exact ordinary class")
    bases = type.__getattribute__(source, "__bases__")
    if len(bases) != 1 or bases[0] is not base:
        _collections._invalid("adapter", "source has unsupported bases")
    target_info = _records._record_info(target)
    if target_info is None:
        _collections._invalid("adapter", "target requires an exact product record class")
    attributes = type.__getattribute__(source, "__dict__")
    if any(type(name) is not str for name in attributes):
        _collections._invalid("adapter", "metadata names require exact strings")
    if any(type(type.__getattribute__(source, name)) is not str for name in ("__name__", "__qualname__", "__module__")):
        _collections._invalid("adapter", "source identity requires exact string metadata")
    return attributes, tuple(name for name, _ in target_info[1])


def _code_token(code):
    if any(type(names) is not tuple or any(type(name) is not str for name in names) for names in
           (code.co_names, code.co_varnames, code.co_freevars, code.co_cellvars)):
        _collections._invalid("adapter", "generated code names require exact strings")
    constants = []
    for value in code.co_consts:
        if type(value) is CodeType:
            constants.append(_code_token(value))
        elif type(value) is frozenset and all(type(item) is str for item in value):
            constants.append(("generated field names", tuple(sorted(value))))
        elif value is None or any(type(value) is kind for kind in (bool, int, str, bytes, tuple)):
            _collections._validate(value, "adapter.code")
            constants.append(value)
        else:
            _collections._invalid("adapter", "unsupported generated-method constant")
    return (code.co_code, tuple(constants), code.co_names, code.co_varnames,
            code.co_freevars, code.co_cellvars, code.co_argcount, code.co_posonlyargcount,
            code.co_kwonlyargcount, code.co_flags, code.co_exceptiontable)


def _generated_method(actual, expected, source=None, reference=None):
    if type(actual) is staticmethod and type(expected) is staticmethod or type(actual) is classmethod and type(expected) is classmethod:
        actual, expected = object.__getattribute__(actual, "__func__"), object.__getattribute__(expected, "__func__")
    if type(actual) is not FunctionType or type(expected) is not FunctionType or _code_token(actual.__code__) != _code_token(expected.__code__):
        return False
    for namespace in (actual.__globals__, actual.__builtins__, expected.__globals__, expected.__builtins__):
        if type(namespace) is not dict or any(type(name) is not str for name in namespace):
            _collections._invalid("adapter", "generated-method namespace keys require exact strings")
    left_defaults, right_defaults = actual.__defaults__, expected.__defaults__
    if left_defaults is not None:
        _collections._validate(left_defaults, "adapter.defaults")
    if not _collections._equal(left_defaults, right_defaults):
        return False
    left_keywords, right_keywords = actual.__kwdefaults__, expected.__kwdefaults__
    if left_keywords is not None or right_keywords is not None:
        if type(left_keywords) is not dict or type(right_keywords) is not dict or any(type(name) is not str for name in left_keywords) or tuple(left_keywords) != tuple(right_keywords):
            return False
        for name in left_keywords:
            _collections._validate(left_keywords[name], "adapter.keyword_defaults")
            if not _collections._equal(left_keywords[name], right_keywords[name]):
                return False
    missing = _records._MISSING
    for name in expected.__code__.co_names:
        right = expected.__globals__.get(name, expected.__builtins__.get(name, missing))
        if right is missing:
            continue  # An attribute name, rather than a global/builtin read.
        left = actual.__globals__.get(name, actual.__builtins__.get(name, missing))
        if left is not right and not (left is source and right is reference):
            return False
    left_cells, right_cells = actual.__closure__ or (), expected.__closure__ or ()
    if len(left_cells) != len(right_cells):
        return False
    for left_cell, right_cell in zip(left_cells, right_cells):
        try:
            left, right = left_cell.cell_contents, right_cell.cell_contents
        except ValueError:
            return False
        if left is right or left is source and right is reference:
            continue
        if type(left) is FunctionType and type(right) is FunctionType:
            if not _generated_method(left, right, source, reference):
                return False
        elif (_collections._scalar_type(type(left)) or type(left) is tuple) and type(left) is type(right):
            _collections._validate(left, "adapter.closure")
            if not _collections._equal(left, right):
                return False
        elif type(left) is set and type(right) is set and len(left) == len(right) == 0:
            # Standard dataclass recursive repr owns an initially empty private
            # recursion set. This state is not read by snapshot conversion.
            continue
        else:
            return False
    return True


def dataclass_adapter(source, target):
    """Qualify a direct, ordinary generated dataclass for a concrete record.

    Supported: generated init/repr/equality, positional fields, stable defaults,
    optional standard frozen setters. Inheritance, slots, ordering, factories,
    keyword-only fields, custom methods/descriptors and metaclasses fail.
    """
    attributes, names = _source_metadata(source, target, object)
    getter = attributes.get("__dict__")
    if type(getter) is not GetSetDescriptorType or getter.__objclass__ is not source:
        _collections._invalid("adapter", "dataclass storage requires its ordinary generated descriptor")
    params = attributes.get("__dataclass_params__")
    fields = attributes.get("__dataclass_fields__")
    if type(params) is not _dataclasses._DataclassParams or type(fields) is not dict:
        _collections._invalid("adapter", "expected standard dataclass metadata")
    flags = {name: object.__getattribute__(params, name) for name in
             ("init", "repr", "eq", "order", "unsafe_hash", "frozen", "match_args", "kw_only", "slots", "weakref_slot")}
    if any(type(value) is not bool for value in flags.values()) or not all(flags[name] for name in ("init", "repr", "eq", "match_args")) or any(flags[name] for name in ("order", "unsafe_hash", "kw_only", "slots", "weakref_slot")):
        _collections._invalid("adapter", "unsupported dataclass declaration options")
    if any(type(name) is not str for name in fields) or tuple(fields) != names:
        _collections._invalid("adapter", "dataclass fields differ from target record")
    annotations = attributes.get("__annotations__")
    if type(annotations) is not dict or any(type(name) is not str for name in annotations) or tuple(annotations) != names:
        _collections._invalid("adapter", "dataclass annotations differ from target fields")
    declaration = []
    for name in names:
        field = fields[name]
        if type(field) is not _dataclasses.Field:
            _collections._invalid("adapter", "expected standard dataclass fields")
        if type(field.name) is not str or field.name != name or field._field_type is not _dataclasses._FIELD or field.default_factory is not _dataclasses.MISSING or field.init is not True or field.repr is not True or field.compare is not True or field.hash is not None or field.kw_only is not False:
            _collections._invalid("adapter", "unsupported dataclass field contract")
        if field.default is _dataclasses.MISSING:
            if name in attributes:
                _collections._invalid("adapter", "unexpected dataclass field descriptor")
            declaration.append((name, object))
        else:
            _collections._validate(field.default, "adapter.default." + name)
            if name not in attributes or not _collections._equal(attributes[name], field.default):
                _collections._invalid("adapter", "dataclass default was replaced")
            declaration.append((name, object, field.default))
    reference = _dataclasses.make_dataclass(type.__getattribute__(source, "__name__"), declaration,
                                          frozen=flags["frozen"], module=__name__,
                                          namespace={"__doc__": "Product adapter method reference."})
    reference_attributes = type.__getattribute__(reference, "__dict__")
    allowed = set(reference_attributes) | {"__firstlineno__", "__static_attributes__"}
    if any(name not in allowed for name in attributes):
        _collections._invalid("adapter", "custom dataclass behavior is unsupported")
    methods = ("__init__", "__repr__", "__eq__", "__replace__") + (("__setattr__", "__delattr__", "__hash__") if flags["frozen"] else ())
    if any(not _generated_method(attributes.get(name), reference_attributes.get(name), source, reference) for name in methods):
        _collections._invalid("adapter", "dataclass methods must match standard generated behavior")
    if not flags["frozen"] and attributes.get("__hash__", object()) is not None:
        _collections._invalid("adapter", "custom dataclass hash is unsupported")
    if type(attributes.get("__match_args__")) is not tuple or any(type(name) is not str for name in attributes["__match_args__"]) or attributes["__match_args__"] != names:
        _collections._invalid("adapter", "dataclass match fields were replaced")
    return _adapter(source, target, "dataclass", names, getter)


def namedtuple_adapter(source, target):
    """Qualify an exact standard namedtuple declaration for a concrete record."""
    attributes, names = _source_metadata(source, target, tuple)
    fields = attributes.get("_fields")
    defaults = attributes.get("_field_defaults")
    if type(fields) is not tuple or any(type(name) is not str for name in fields) or fields != names:
        _collections._invalid("adapter", "namedtuple fields differ from target record")
    if type(defaults) is not dict or any(type(name) is not str or name not in names for name in defaults):
        _collections._invalid("adapter", "unsupported namedtuple defaults")
    for name, value in defaults.items():
        _collections._validate(value, "adapter.default." + name)
    suffix = names[len(names) - len(defaults):] if defaults else ()
    if tuple(defaults) != suffix:
        _collections._invalid("adapter", "namedtuple defaults must be a trailing suffix")
    reference = _stdlib_collections.namedtuple(type.__getattribute__(source, "__name__"), names,
                                             defaults=tuple(defaults.values()) if defaults else None, module=__name__)
    reference_attributes = type.__getattribute__(reference, "__dict__")
    if any(name not in reference_attributes and name not in ("__annotations__", "__firstlineno__", "__static_attributes__") for name in attributes):
        _collections._invalid("adapter", "custom namedtuple behavior is unsupported")
    for name, expected in reference_attributes.items():
        if any(type(expected) is kind for kind in (FunctionType, staticmethod, classmethod)):
            if not _generated_method(attributes.get(name), expected, source, reference):
                _collections._invalid("adapter", "namedtuple methods must match standard generated behavior")
    for name in names:
        actual, expected = attributes.get(name), reference_attributes[name]
        if type(actual) is not type(expected):
            _collections._invalid("adapter", "custom namedtuple field getter is unsupported")
        reduction = actual.__reduce__()
        expected_reduction = expected.__reduce__()
        if type(reduction) is not tuple or len(reduction) != 2 or reduction[0] is not expected_reduction[0] or type(reduction[1]) is not tuple or len(reduction[1]) != 2 or type(reduction[1][0]) is not int or not (reduction[1][1] is None or type(reduction[1][1]) is str) or reduction[1] != expected_reduction[1]:
            _collections._invalid("adapter", "namedtuple field getter was replaced")
    slots = attributes.get("__slots__")
    matches = attributes.get("__match_args__")
    if type(slots) is not tuple or len(slots) != 0 or type(matches) is not tuple or any(type(name) is not str for name in matches) or matches != names:
        _collections._invalid("adapter", "namedtuple storage/match fields were replaced")
    return _adapter(source, target, "namedtuple", names)


def freeze(value, *, exclusive=False, adapter=None, schema=None):
    """Snapshot supported data under an explicit exclusive-access assertion.

    Mutable builtins and adapter sources require exact ``exclusive=True``.
    Repeated acyclic references are copied by value, without identity promises.
    Optional ``schema`` is a closed exact annotation, checked after conversion.
    """
    if type(exclusive) is not bool:
        _collections._invalid("exclusive", "expected exact bool ownership assertion")
    if adapter is not None and type(adapter) is not _SnapshotAdapter:
        _collections._invalid("adapter", "expected a named qualified snapshot adapter")
    if adapter is not None:
        _validate_adapter(adapter)
    output = _freeze(value, "value", set(), exclusive, adapter)
    if schema is not None:
        descriptor = _records._annotation_schema(schema)
        validate_data(output, descriptor)
    return output


def _freeze(value, path, active, exclusive, adapter):
    kind = type(value)
    if _collections._scalar_type(kind):
        return value
    if (_collections._collection_type(kind) or _records._record_info(kind) is not None
            or _records._sums._case_info(kind) is not None):
        _collections._validate(value, path)
        return value
    adapter_source = adapter is not None and kind is object.__getattribute__(adapter, "_source")
    if not any(kind is cls for cls in (list, tuple, dict, set, frozenset)) and not adapter_source:
        _collections._invalid(path, "unsupported snapshot source; no hooks, subclasses or live views")
    if (kind is list or kind is dict or kind is set or adapter_source) and not exclusive:
        _collections._invalid(path, "snapshot of mutable/adapter input requires exclusive=True caller assertion")
    identity = id(value)
    if identity in active:
        _collections._invalid(path, "cyclic snapshot source is unsupported")
    active.add(identity)
    try:
        if adapter_source:
            names = object.__getattribute__(adapter, "_names")
            if object.__getattribute__(adapter, "_kind") == "dataclass":
                try:
                    storage = object.__getattribute__(adapter, "_getter").__get__(value, kind)
                except AttributeError:
                    _collections._invalid(path, "malformed dataclass storage")
                if type(storage) is not dict or any(type(name) is not str for name in storage) or tuple(storage) != names:
                    _collections._invalid(path, "dataclass storage must contain only declared fields")
                values = tuple(storage[name] for name in names)
            else:
                if tuple.__len__(value) != len(names):
                    _collections._invalid(path, "malformed namedtuple storage")
                values = tuple(tuple.__getitem__(value, index) for index in range(len(names)))
            copied = tuple(_freeze(item, path + "." + name, active, exclusive, adapter) for name, item in zip(names, values))
            return object.__getattribute__(adapter, "_target")(*copied)
        if kind is list or kind is tuple:
            # A length check catches known size instability, but cannot detect
            # every same-size concurrent write. Ownership remains a precondition.
            size = len(value)
            copied = tuple(_freeze(item, f"{path}[{index}]", active, exclusive, adapter) for index, item in enumerate(value))
            if len(value) != size or len(copied) != size:
                _collections._invalid(path, "snapshot source changed size")
            return _collections.Vector.of(*copied) if kind is list else copied
        if kind is dict:
            size = len(value)
            try:
                entries = tuple(value.items())
            except RuntimeError:
                _collections._invalid(path, "snapshot source changed size")
            _collections._validate_domain(tuple(key for key, _ in entries), path + ".keys")
            copied = tuple((key, _freeze(item, path + ".entries[" + _collections._path_key(key) + "].value", active, exclusive, adapter)) for key, item in entries)
            if len(value) != size or len(entries) != size:
                _collections._invalid(path, "snapshot source changed size")
            return _collections.OrderedMap.of(*copied)
        size = len(value)
        try:
            items = tuple(value)
        except RuntimeError:
            _collections._invalid(path, "snapshot source changed size")
        _collections._validate_domain(items, path + ".members")
        if len(value) != size or len(items) != size:
            _collections._invalid(path, "snapshot source changed size")
        return _collections.Set.of(*items)
    finally:
        active.remove(identity)


def thaw(value):
    """Export admitted data into fresh nested list/dict/set storage.

    Product records export a field dictionary. Stable scalar leaves are reused;
    all container occurrences, including tuple occurrences, export independently.
    """
    _collections._validate(value)
    return _thaw(value)


def _thaw(value):
    kind = type(value)
    if _collections._scalar_type(kind):
        return value
    info = _records._record_info(kind)
    if info is not None:
        return {name: _thaw(item) for (name, _), item in zip(info[1], _records._record_values(value, info))}
    case_info = _records._sums._case_info(kind)
    if case_info is not None:
        return {"oneof": case_info[4], "case": case_info[5],
                "fields": {name: _thaw(item) for (name, _), item in
                           zip(case_info[1], _records._sums._case_values(value, case_info))}}
    if kind is tuple:
        return [_thaw(item) for item in value]
    if kind is _collections.Vector:
        return [_thaw(item) for item in _collections._storage(value, "_items", "value")]
    if kind is _collections.Set:
        return set(_collections._storage(value, "_items", "value"))
    return {key: _thaw(item) for key, item in _collections._storage(value, "_entries", "value")}
