"""Fixed deeply typed product records, using ordinary exact slot storage.

The registry describes values, not function purity. Unchecked replacement of
these definitions or forged private storage violates the dependency contract.
"""

import ast
import sys
from types import GenericAlias, ModuleType, GetSetDescriptorType, UnionType
from . import collections as _collections

__all__ = ["record", "replace"]

_MISSING = object()
_RECORDS = ()
_SCALARS = (("None", type(None)), ("bool", bool), ("int", int), ("str", str), ("bytes", bytes))


def _record_info(kind):
    # A dict keyed by arbitrary type objects could run a foreign metaclass hash.
    for entry in _RECORDS:
        if kind is entry[0]:
            return entry
    return None


def _record_values(value, info, path="record"):
    try:
        initialized = object.__getattribute__(value, "_pal_initialized")
    except AttributeError:
        _collections._invalid(path, "malformed record storage")
    if initialized is not True:
        _collections._invalid(path, "malformed record storage")
    values = []
    for name, _ in info[1]:
        try:
            values.append(object.__getattribute__(value, name))
        except AttributeError:
            _collections._invalid(path + "." + name, "malformed record storage")
    return tuple(values)


def _namespace(cls):
    if type(sys.modules) is not dict or any(type(name) is not str for name in sys.modules):
        _collections._invalid("record", "module namespace keys require exact strings")
    module = sys.modules.get(type.__getattribute__(cls, "__module__"))
    namespace = ModuleType.__getattribute__(module, "__dict__") if type(module) is ModuleType else {}
    if type(namespace) is not dict or any(type(name) is not str for name in namespace):
        _collections._invalid("record", "annotation namespace keys require exact strings")
    return namespace


def _annotation_schema(annotation, namespace=None):
    """Parse only the closed data vocabulary; never eval or get_type_hints."""
    for name, kind in _SCALARS:
        if annotation is kind or name == "None" and annotation is None:
            return name
    info = _record_info(annotation)
    if info is not None:
        return ("record", info[0], info[1])
    alternative = _sums._annotation_schema(annotation, namespace)
    if alternative is not None:
        return alternative
    if type(annotation) is GenericAlias:
        origin = object.__getattribute__(annotation, "__origin__")
        arguments = object.__getattribute__(annotation, "__args__")
        if origin is tuple:
            variadic = len(arguments) == 2 and arguments[1] is Ellipsis
            children = arguments[:1] if variadic else arguments
            return ("tuple", tuple(_annotation_schema(child, namespace) for child in children), variadic)
        for name, cls in (("Vector", _collections.Vector), ("OrderedMap", _collections.OrderedMap),
                          ("Map", _collections.Map), ("Set", _collections.Set)):
            if origin is cls:
                schema = (name, tuple(_annotation_schema(child, namespace) for child in arguments))
                _check_schema(schema)
                return schema
    if type(annotation) is UnionType:
        members = object.__getattribute__(annotation, "__args__")
        if type(members) is not tuple:
            _collections._invalid("annotation", "malformed union annotation")
        return _union_schema(tuple(_annotation_schema(member, namespace) for member in members))
    if type(annotation) is str:
        try:
            expression = ast.parse(annotation, mode="eval").body
        except SyntaxError:
            _collections._invalid("annotation", "unsupported record data annotation")
        return _annotation_node(expression, {} if namespace is None else namespace)
    _collections._invalid("annotation", "unsupported exact record data annotation")


def _annotation_node(node, namespace):
    if type(node) is ast.Constant and node.value is None:
        return "None"
    if type(node) is ast.BinOp and type(node.op) is ast.BitOr:
        return _union_schema((_annotation_node(node.left, namespace), _annotation_node(node.right, namespace)))
    if type(node) is ast.Name:
        # Builtin/collection names have meaning only if their actual binding is
        # absent or is the approved exact identity. Imported aliases are allowed.
        approved = {name: kind for name, kind in _SCALARS if name != "None"}
        approved.update({"tuple": tuple, "Vector": _collections.Vector, "Map": _collections.Map,
                         "OrderedMap": _collections.OrderedMap, "Set": _collections.Set})
        binding = namespace.get(node.id, approved.get(node.id, _MISSING))
        if node.id == "None":
            return "None"
        return _annotation_schema(binding, namespace)
    if type(node) is ast.Subscript:
        origin = _annotation_binding(node.value, namespace)
        parts = node.slice.elts if type(node.slice) is ast.Tuple else (node.slice,)
        variadic = len(parts) == 2 and type(parts[1]) is ast.Constant and parts[1].value is Ellipsis
        if origin is tuple:
            schema = ("tuple", tuple(_annotation_node(part, namespace) for part in (parts[:1] if variadic else parts)), variadic)
        else:
            name = next((name for name, cls in (("Vector", _collections.Vector), ("Map", _collections.Map),
                                               ("OrderedMap", _collections.OrderedMap), ("Set", _collections.Set)) if origin is cls), None)
            if name is None:
                name = _sums._annotation_origin(origin)
            if name is None:
                _collections._invalid("annotation", "unsupported record data annotation")
            schema = (name, tuple(_annotation_node(part, namespace) for part in parts))
        _check_schema(schema)
        return schema
    if type(node) is ast.Attribute:
        return _annotation_schema(_annotation_binding(node, namespace), namespace)
    _collections._invalid("annotation", "unsupported record data annotation")


def _annotation_binding(node, namespace):
    if type(node) is ast.Name:
        approved = {"tuple": tuple, "Vector": _collections.Vector, "Map": _collections.Map,
                    "OrderedMap": _collections.OrderedMap, "Set": _collections.Set}
        return namespace.get(node.id, approved.get(node.id, _MISSING))
    if type(node) is ast.Attribute:
        owner = _annotation_binding(node.value, namespace)
        if type(owner) is ModuleType:
            attributes = ModuleType.__getattribute__(owner, "__dict__")
            if type(attributes) is not dict or any(type(name) is not str for name in attributes):
                _collections._invalid("annotation", "module metadata names require exact strings")
            return attributes.get(node.attr, _MISSING)
        alternative = _sums._annotation_attribute(owner, node.attr)
        if alternative is not _MISSING:
            return alternative
    _collections._invalid("annotation", "unsupported record annotation namespace")


def _union_classes(schema):
    """Exact runtime classes occupied by one closed-union member schema."""
    if type(schema) is str:
        return tuple(kind for name, kind in _SCALARS if name == schema)
    if type(schema) is tuple and len(schema) == 3 and schema[0] in ("record", "case"):
        return (schema[1],)
    if type(schema) is tuple and len(schema) == 3 and schema[0] == "oneof" and type(schema[2]) is tuple:
        return tuple(entry[0] for entry in schema[2] if type(entry) is tuple and len(entry) == 2)
    _collections._invalid("schema", "union members are exact scalars, records, domains or cases")


def _union_key(schema):
    if type(schema) is str:
        return (0, next(index for index, (name, _) in enumerate(_SCALARS) if name == schema), "", 0)
    owner = schema[1]
    return (1, type.__getattribute__(owner, "__module__"), type.__getattribute__(owner, "__qualname__"), id(owner))


def _union_schema(members):
    """Flatten, deduplicate and order closed-union members; overlap is refused."""
    flat = []
    for member in members:
        if type(member) is tuple and member and member[0] == "union":
            if len(member) != 2 or type(member[1]) is not tuple:
                _collections._invalid("schema", "malformed union schema")
            children = member[1]
        else:
            children = (member,)
        for child in children:
            if not any(child == seen for seen in flat):
                flat.append(child)
    occupied = []
    for member in flat:
        for kind in _union_classes(member):
            if any(kind is seen for seen in occupied):
                _collections._invalid("schema", "union members overlap by exact runtime class")
            occupied.append(kind)
    if any(kind is bool for kind in occupied) and any(kind is int for kind in occupied):
        _collections._invalid("schema", "bool | int is refused because class patterns cannot separate them")
    if len(flat) == 1:
        return flat[0]
    return ("union", tuple(sorted(flat, key=_union_key)))


def _canonical(schema):
    """Order union members inside a checker-produced schema; shape is checked later."""
    if type(schema) is not tuple or not schema or type(schema[0]) is not str:
        return schema
    name = schema[0]
    if name == "union" and len(schema) == 2 and type(schema[1]) is tuple:
        return _union_schema(tuple(_canonical(child) for child in schema[1]))
    if name in ("record", "case") and len(schema) == 3 and type(schema[2]) is tuple:
        return (name, schema[1], tuple((field[0], _canonical(field[1])) if type(field) is tuple and len(field) == 2 else field
                                       for field in schema[2]))
    if name == "oneof" and len(schema) == 3 and type(schema[2]) is tuple:
        return (name, schema[1], tuple((entry[0], _canonical(("case", entry[0], entry[1]))[2])
                                       if type(entry) is tuple and len(entry) == 2 and type(entry[1]) is tuple else entry
                                       for entry in schema[2]))
    if len(schema) >= 2 and type(schema[1]) is tuple:
        return (name, tuple(_canonical(child) for child in schema[1]), *schema[2:])
    return schema


def _check_schema(schema):
    if type(schema) is str and any(schema == name for name, _ in _SCALARS):
        return
    if type(schema) is not tuple or not schema or type(schema[0]) is not str:
        _collections._invalid("schema", "unsupported exact data schema")
    name = schema[0]
    if name == "union":
        if len(schema) != 2 or type(schema[1]) is not tuple or len(schema[1]) < 2:
            _collections._invalid("schema", "malformed union schema")
        for child in schema[1]:
            if type(child) is tuple and child and child[0] == "union":
                _collections._invalid("schema", "union members are flat")
            _check_schema(child)
        if _union_schema(schema[1]) != schema:
            _collections._invalid("schema", "union schema is not canonical")
        return
    if _sums._check_schema(schema):
        return
    if name == "record":
        if len(schema) != 3:
            _collections._invalid("schema", "malformed record schema")
        info = _record_info(schema[1])
        if info is None or type(schema[2]) is not tuple:
            _collections._invalid("schema", "record schema requires an exact product record")
        for field in schema[2]:
            if type(field) is not tuple or len(field) != 2 or type(field[0]) is not str:
                _collections._invalid("schema", "malformed record fields")
            _check_schema(field[1])
        if schema[2] != info[1]:
            _collections._invalid("schema", "record schema differs from its fixed fields")
        return
    if name == "tuple":
        if len(schema) != 3 or type(schema[1]) is not tuple or type(schema[2]) is not bool or schema[2] and len(schema[1]) != 1:
            _collections._invalid("schema", "malformed tuple schema")
    elif name in ("Vector", "Set", "Map", "OrderedMap"):
        arity = 2 if name in ("Map", "OrderedMap") else 1
        if len(schema) != 2 or type(schema[1]) is not tuple or len(schema[1]) != arity:
            _collections._invalid("schema", "malformed collection schema")
        if name in ("Set", "Map", "OrderedMap") and not (type(schema[1][0]) is str and any(schema[1][0] == scalar for scalar, _ in _SCALARS)):
            _collections._invalid("schema", "keys/members require an exact scalar schema")
    else:
        _collections._invalid("schema", "unsupported exact data schema")
    for child in schema[1]:
        _check_schema(child)


def _validate_schema(value, schema, path="value", active=None):
    kind = type(value)
    if type(schema) is str:
        expected = next(kind for name, kind in _SCALARS if name == schema)
        if kind is not expected:
            _collections._invalid(path, "expected exact " + schema)
        return
    name = schema[0]
    if name == "union":
        for member in schema[1]:
            if any(kind is candidate for candidate in _union_classes(member)):
                _validate_schema(value, member, path, active)
                return
        _collections._invalid(path, "expected exact member of closed union")
    if name in ("oneof", "case", "Option", "Result", "Some", "Nothing", "Ok", "Err"):
        _sums._validate_schema(value, schema, path, active)
        return
    if name == "record":
        expected = schema[1]
    elif name == "tuple":
        expected = tuple
    else:
        expected = {"Vector": _collections.Vector, "Set": _collections.Set,
                    "Map": _collections.Map, "OrderedMap": _collections.OrderedMap}[name]
    if kind is not expected:
        _collections._invalid(path, "expected exact " + name)
    active = set() if active is None else active
    identity = id(value)
    if identity in active:
        _collections._invalid(path, "cyclic data is unsupported")
    active.add(identity)
    try:
        if name == "record":
            info = _record_info(kind)
            for (field, child), item in zip(info[1], _record_values(value, info, path)):
                _validate_schema(item, child, path + "." + field, active)
        elif name == "tuple":
            if not schema[2] and len(value) != len(schema[1]):
                _collections._invalid(path, "fixed tuple length differs from schema")
            for index, item in enumerate(value):
                child = schema[1][0] if schema[2] else schema[1][index]
                _validate_schema(item, child, f"{path}[{index}]", active)
        elif name in ("Vector", "Set"):
            items = _collections._storage(value, "_items", path)
            if name == "Set":
                _collections._validate_domain(items, path + ".members")
            for index, item in enumerate(items):
                _validate_schema(item, schema[1][0], f"{path}[{index}]", active)
        else:
            entries = _collections._storage(value, "_entries", path)
            for pair in entries:
                if type(pair) is not tuple or len(pair) != 2:
                    _collections._invalid(path, "malformed map entries")
            _collections._validate_domain(tuple(pair[0] for pair in entries), path + ".keys")
            traversal = entries if name == "OrderedMap" else _collections._canonical_pairs(entries)
            for key, item in traversal:
                _validate_schema(key, schema[1][0], path + ".key", active)
                _validate_schema(item, schema[1][1], path + ".entries[" + _collections._path_key(key) + "].value", active)
    finally:
        active.remove(identity)


def _validate_record(value, info, path, active):
    for (name, schema), item in zip(info[1], _record_values(value, info, path)):
        _validate_schema(item, schema, path + "." + name, active)


def _record_equal(left, right, info):
    return _collections._sequence_equal(_record_values(left, info), _record_values(right, info))


def _record_repr(value, info):
    name = type.__getattribute__(info[0], "__name__")
    return name + "(" + ", ".join(field + "=" + _collections._data_repr(item)
                                    for (field, _), item in zip(info[1], _record_values(value, info))) + ")"


def record(cls):
    """Replace a declaration-only class with a fixed deeply typed record class."""
    global _RECORDS
    if type(cls) is not type:
        _collections._invalid("record", "record declarations require exact type and no bases")
    bases = type.__getattribute__(cls, "__bases__")
    if len(bases) != 1 or bases[0] is not object:
        _collections._invalid("record", "record declarations require exact type and no bases")
    attributes = type.__getattribute__(cls, "__dict__")
    if any(type(name) is not str for name in attributes):
        _collections._invalid("record", "record metadata names require exact strings")
    if any(type(type.__getattribute__(cls, name)) is not str for name in ("__module__", "__qualname__", "__name__")):
        _collections._invalid("record", "record declaration identity requires exact string metadata")
    if attributes.get("__doc__") is not None and type(attributes.get("__doc__")) is not str:
        _collections._invalid("record", "record doc metadata requires an exact string")
    for name in ("__dict__", "__weakref__"):
        descriptor = attributes.get(name)
        if descriptor is not None and (type(descriptor) is not GetSetDescriptorType or descriptor.__objclass__ is not cls):
            _collections._invalid("record", "custom record descriptors are unsupported")
    annotations = attributes.get("__annotations__", {})
    if type(annotations) is not dict:
        _collections._invalid("record", "record annotations require exact dictionary metadata")
    namespace = _namespace(cls)
    fields = []
    defaults = []
    saw_default = False
    for name, annotation in annotations.items():
        if type(name) is not str or not name.isidentifier() or name.startswith("_"):
            _collections._invalid("record", "record fields require public identifiers")
        schema = _annotation_schema(annotation, namespace)
        _check_schema(schema)
        default = attributes.get(name, _MISSING)
        if default is not _MISSING:
            _validate_schema(default, schema, "default." + name)
            saw_default = True
        elif saw_default:
            _collections._invalid("record", "required fields cannot follow defaults")
        fields.append((name, schema))
        defaults.append(default)
    allowed = {"__module__", "__qualname__", "__doc__", "__annotations__", "__dict__", "__weakref__",
               "__firstlineno__", "__static_attributes__"}
    allowed.update(name for name, _ in fields)
    if any(name not in allowed for name in attributes):
        _collections._invalid("record", "record declarations contain only typed fields and stable defaults")
    fields, defaults = tuple(fields), tuple(defaults)

    def initialize(self, /, *args, **kwargs):
        try:
            object.__getattribute__(self, "_pal_initialized")
        except AttributeError:
            pass
        else:
            raise AttributeError("immutable record cannot be reinitialized")
        if len(args) > len(fields):
            _collections._invalid("record", "too many constructor arguments")
        if any(type(name) is not str for name in kwargs):
            _collections._invalid("record", "constructor field names require exact strings")
        if any(name not in tuple(field for field, _ in fields) for name in kwargs):
            _collections._invalid("record", "unknown constructor field")
        values = []
        for index, (name, schema) in enumerate(fields):
            if index < len(args):
                if name in kwargs:
                    _collections._invalid("record." + name, "field supplied twice")
                value = args[index]
            else:
                value = kwargs.get(name, defaults[index])
            if value is _MISSING:
                _collections._invalid("record." + name, "required field is missing")
            _validate_schema(value, schema, "record." + name)
            values.append(value)
        for name, _ in fields:
            try:
                object.__getattribute__(self, name)
            except AttributeError:
                continue
            raise AttributeError("immutable record cannot be reinitialized")
        for (name, _), value in zip(fields, values):
            object.__setattr__(self, name, value)
        object.__setattr__(self, "_pal_initialized", True)

    def reject_assignment(self, name, value):
        raise AttributeError("immutable record fields cannot be assigned")

    def reject_deletion(self, name):
        raise AttributeError("immutable record fields cannot be deleted")

    def reject_subclass(subclass, **kwargs):
        raise TypeError("product records cannot be subclassed")

    def equal(self, other):
        return type(self) is type(other) and _record_equal(self, other, _record_info(type(self)))

    def unequal(self, other):
        return not equal(self, other)

    def representation(self):
        return _record_repr(self, _record_info(type(self)))

    product = type(type.__getattribute__(cls, "__name__"), (object,), {
        "__module__": type.__getattribute__(cls, "__module__"), "__qualname__": type.__getattribute__(cls, "__qualname__"),
        "__doc__": attributes.get("__doc__"), "__slots__": tuple(name for name, _ in fields) + ("_pal_initialized",),
        "__match_args__": tuple(name for name, _ in fields), "__init__": initialize,
        "__setattr__": reject_assignment, "__delattr__": reject_deletion,
        "__init_subclass__": classmethod(reject_subclass), "__eq__": equal, "__ne__": unequal,
        "__repr__": representation, "__hash__": None,
    })
    _RECORDS += ((product, fields, defaults),)
    return product


def replace(value, /, **changes):
    """Return a new exact record with validated explicit field changes."""
    info = _record_info(type(value))
    if info is None:
        _collections._invalid("replace", "expected an exact product record")
    names = tuple(name for name, _ in info[1])
    if any(type(name) is not str for name in changes):
        _collections._invalid("replace", "replacement field names require exact strings")
    if any(name not in names for name in changes):
        _collections._invalid("replace", "unknown replacement field")
    _collections._validate(value)
    values = _record_values(value, info)
    return info[0](*(changes.get(name, item) for name, item in zip(names, values)))


# Imported after these definitions: collections imports records during its own
# initialization. Alternatives create only fixed classes/catalogs at import and
# consult completed collection functions only when ordinary data is used.
from . import sums as _sums
