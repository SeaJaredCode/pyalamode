"""Bounded explicit value bytes with closed schemas and native slot allocation.

This is ordinary trusted value support, not a callable certificate registry.
Classes, catalogs and native dependencies must remain unchanged. No incoming
type label resolves an object; decode uses only the explicitly selected schema.
"""

from types import GenericAlias, MemberDescriptorType, GetSetDescriptorType, MappingProxyType
from . import collections as _collections
from . import records as _records
from . import variants as _variants

__all__ = ["value_encode", "value_decode"]

MAX_WIRE_BYTES = 1_048_576
MAX_SCHEMA_BYTES = 65_536
MAX_SCHEMA_NODES = 1_024
MAX_VALUE_NODES = 16_384
MAX_DEPTH = 32
MAX_ITEMS = 4_096
MAX_FIELDS = 128
MAX_CASES = 128
MAX_BYTES = 262_144
MAX_STRING = 65_536
MAX_IDENTITY = 1_024
MAX_NAME = 128
MIN_INTEGER = -(2 ** 63)
MAX_INTEGER = 2 ** 63 - 1
_MAGIC = b"PALV\x01"
_SCALARS = ((0, type(None)), (1, bool), (2, int), (3, str), (4, bytes))
_COLLECTIONS = ((0x12, _collections.Vector), (0x13, _collections.OrderedMap),
                (0x14, _collections.Map), (0x15, _collections.Set))
_MISSING = object()
_TYPE_ATTRIBUTES = type.__getattribute__(type, "__dict__")


def _type_error(path, reason):
    raise TypeError(path + ": " + reason)


def _value_error(path, reason):
    raise ValueError(path + ": " + reason)


def _limit(value, maximum, path, label):
    if value > maximum:
        _value_error(path, label + " limit exceeded")


def _name(value, identity=False, wire=False):
    fail = _value_error if wire else _type_error
    if type(value) is not str:
        fail("schema", "malformed product schema metadata")
    _limit(len(value), MAX_IDENTITY if identity else MAX_NAME, "schema",
           "nominal-name" if identity else "field-name/case-name")
    if identity:
        parts = str.split(value, ":")
        valid = len(parts) == 2 and all(parts)
        if valid:
            valid = all(part and str.isidentifier(part)
                        for section in parts for part in str.split(section, "."))
    else:
        valid = bool(value) and not value.startswith("_") and str.isidentifier(value)
    if not valid:
        fail("schema", "unsupported nominal/field/case spelling")
    return value


def _native_type_read(kind, name):
    # Direct builtin descriptors bypass even characterized DomainType metadata
    # lookup. An unrelated/foreign schema never reaches this helper.
    descriptor = _TYPE_ATTRIBUTES[name]
    if type(descriptor) is GetSetDescriptorType:
        return GetSetDescriptorType.__get__(descriptor, kind, type(kind))
    if type(descriptor) is MemberDescriptorType:
        return MemberDescriptorType.__get__(descriptor, kind, type(kind))
    _type_error("schema", "non-native product metadata descriptor")


def _class_dict(kind):
    attributes = _native_type_read(kind, "__dict__")
    if type(attributes) is not MappingProxyType:
        _type_error("schema", "malformed product schema metadata")
    return attributes


def _identity(kind, unrelated=False):
    attributes = _class_dict(kind)
    module = attributes.get("__module__", _MISSING)
    # Qualname is the native type slot, not necessarily a mappingproxy key.
    # Only an admitted exact type/trusted domain metaclass reaches this read.
    qualified = _native_type_read(kind, "__qualname__")
    if type(module) is not str or type(qualified) is not str:
        if unrelated:
            return None
        _type_error("schema", "malformed product schema metadata")
    if unrelated:
        if len(module) + 1 + len(qualified) > MAX_IDENTITY:
            return None
        # Collision equality needs no spelling parsing of unrelated entries.
        return module + ":" + qualified
    _limit(len(module), MAX_IDENTITY, "schema", "nominal-name")
    _limit(len(qualified), MAX_IDENTITY, "schema", "nominal-name")
    _limit(len(module) + 1 + len(qualified), MAX_IDENTITY, "schema", "nominal-name")
    return _name(module + ":" + qualified, identity=True)


def _descriptor(owner, name):
    descriptor = _class_dict(owner).get(name, _MISSING)
    if (type(descriptor) is not MemberDescriptorType
            or object.__getattribute__(descriptor, "__objclass__") is not owner
            or object.__getattribute__(descriptor, "__name__") != name):
        _type_error("schema", "non-native product storage descriptor")
    return descriptor


def _field_shape(fields):
    if type(fields) is not tuple:
        _type_error("schema", "malformed product schema metadata")
    _limit(len(fields), MAX_FIELDS, "schema", "schema field count")
    names = []
    for field in fields:
        if type(field) is not tuple or len(field) != 2:
            _type_error("schema", "malformed product schema metadata")
        name = _name(field[0])
        if name in names:
            _type_error("schema", "malformed product schema metadata")
        names.append(name)
    return tuple(names)


def _field_descriptors(kind, fields):
    # Actual class identity is admitted before this function is called.
    if type(kind) is not type:
        _type_error("schema", "malformed product schema metadata")
    mro = _native_type_read(kind, "__mro__")
    if len(mro) != 2 or mro[0] is not kind or mro[1] is not object:
        _type_error("schema", "malformed product schema metadata")
    names = _field_shape(fields)
    attributes = _class_dict(kind)
    if "__del__" in attributes:
        _type_error("schema", "custom product finalizers are unsupported")
    slots = attributes.get("__slots__", _MISSING)
    if (type(slots) is not tuple or any(type(name) is not str for name in slots)
            or slots != names + ("_pal_initialized",)):
        _type_error("schema", "malformed product schema metadata")
    return tuple(_descriptor(kind, name) for name in names) + (_descriptor(kind, "_pal_initialized"),)


def _collection_descriptor(kind):
    if kind is _collections.Vector or kind is _collections.Set:
        expected = (kind, _collections._Frozen, object)
        owner, name = kind, "_items"
    else:
        expected = (kind, _collections._MapBase, _collections._Frozen, object)
        owner, name = _collections._MapBase, "_entries"
    mro = _native_type_read(kind, "__mro__")
    if len(mro) != len(expected) or any(a is not b for a, b in zip(mro, expected)):
        _type_error("schema", "malformed product schema metadata")
    if any("__del__" in _class_dict(base) for base in expected):
        _type_error("schema", "custom product finalizers are unsupported")
    return _descriptor(owner, name)


class _Node:
    __slots__ = ("tag", "kind", "children", "identity", "fields", "cases", "selected", "descriptors")

    def __init__(self, tag, kind=None, children=(), identity=None, fields=(), cases=(), selected=None, descriptors=()):
        self.tag, self.kind, self.children = tag, kind, children
        self.identity, self.fields, self.cases = identity, fields, cases
        self.selected, self.descriptors = selected, descriptors


class _Case:
    __slots__ = ("kind", "name", "fields", "descriptors")

    def __init__(self, kind, name, fields, descriptors):
        self.kind, self.name, self.fields, self.descriptors = kind, name, fields, descriptors


class _Budget:
    __slots__ = ("maximum", "count", "label", "active")

    def __init__(self, maximum, label):
        self.maximum, self.count, self.label, self.active = maximum, 0, label, set()

    def node(self, depth):
        _limit(depth, MAX_DEPTH, self.label, self.label + " depth")
        self.count += 1
        _limit(self.count, self.maximum, self.label, self.label + " node")


class _Compiler:
    __slots__ = ("records", "domains", "cases", "budget", "labels")

    def __init__(self):
        self.records, self.domains, self.cases = _records._RECORDS, _variants._VARIANTS, _variants._CASES
        for rows, arity in ((self.records, 3), (self.domains, 3), (self.cases, 6)):
            if type(rows) is not tuple or any(type(row) is not tuple or len(row) != arity for row in rows):
                _type_error("schema", "malformed product schema metadata")
        self.budget, self.labels = _Budget(MAX_SCHEMA_NODES, "schema"), None

    def find(self, rows, kind):
        for row in rows:
            if kind is row[0]:
                return row
        return None

    def nominal(self, kind):
        # Only registered exact product classes reach metadata reads. Avoid
        # class hashing/equality, including foreign metaclass implementations.
        identity = _identity(kind)
        if self.labels is None:
            labels = []
            for row in self.records:
                if type(row[0]) is not type:
                    _type_error("schema", "malformed product schema metadata")
                label = _identity(row[0], unrelated=True)
                if label is not None:
                    labels.append((label, row[0]))
            for row in self.domains:
                if type(row[0]) is not _variants._DomainType or type(row[1]) is not str:
                    _type_error("schema", "malformed product schema metadata")
                original = _identity(row[0], unrelated=True)
                if original is not None:
                    labels.append((original, row[0]))
            for row in self.cases:
                if row[3] is None:
                    continue
                if type(row[0]) is not type:
                    _type_error("schema", "malformed product schema metadata")
                label = _identity(row[0], unrelated=True)
                if label is not None:
                    labels.append((label, row[0]))
            self.labels = tuple(labels)
        for label, other in self.labels:
            if label == identity and other is not kind:
                _type_error("schema", "duplicate nominal identity")
        return identity

    def fields(self, fields, depth):
        _field_shape(fields)
        return tuple((name, self.internal(schema, depth + 1)) for name, schema in fields)

    def record(self, info, depth):
        identity = id(info[0])
        if identity in self.budget.active:
            _type_error("schema", "cyclic product schema metadata")
        self.budget.active.add(identity)
        try:
            descriptors = _field_descriptors(info[0], info[1])
            return _Node(0x20, info[0], identity=self.nominal(info[0]),
                         fields=self.fields(info[1], depth), descriptors=descriptors)
        finally:
            self.budget.active.remove(identity)

    def domain(self, info, depth):
        kind, original, entries = info
        if type(kind) is not _variants._DomainType or type(entries) is not tuple or not entries:
            _type_error("schema", "malformed product schema metadata")
        _limit(len(entries), MAX_CASES, "schema", "schema case count")
        identity = self.nominal(kind)
        if type(original) is not str or identity != original:
            _type_error("schema", "malformed product schema metadata")
        active_identity = id(kind)
        if active_identity in self.budget.active:
            _type_error("schema", "cyclic product schema metadata")
        self.budget.active.add(active_identity)
        try:
            cases, names = [], []
            for entry in entries:
                if type(entry) is not tuple or len(entry) != 2:
                    _type_error("schema", "malformed product schema metadata")
                case = self.find(self.cases, entry[0])
                if case is None or case[3] is not kind or entry[1] is not case[1]:
                    _type_error("schema", "malformed product schema metadata")
                descriptors = _field_descriptors(case[0], case[1])
                name = _name(case[5])
                if name in names or self.nominal(case[0]) != identity + "." + name:
                    _type_error("schema", "malformed product schema metadata")
                names.append(name)
                cases.append(_Case(case[0], name, self.fields(case[1], depth), descriptors))
            return _Node(0x21, kind, identity=identity, cases=tuple(cases))
        finally:
            self.budget.active.remove(active_identity)

    def builtin_case(self, kind, fields):
        info = self.find(self.cases, kind)
        expected_name = next(name for cls, name in ((_variants.Some, "Some"), (_variants.Nothing, "Nothing"),
                                                   (_variants.Ok, "Ok"), (_variants.Err, "Err")) if cls is kind)
        family = _variants.Option if kind is _variants.Some or kind is _variants.Nothing else _variants.Result
        if info is None or info[3] is not family or type(info[5]) is not str or info[5] != expected_name:
            _type_error("schema", "malformed product schema metadata")
        descriptors = _field_descriptors(kind, info[1])
        names = _field_shape(info[1])
        if names != tuple(name for name, _ in fields) or self.nominal(kind) != "pyalamode:" + expected_name:
            _type_error("schema", "malformed product schema metadata")
        return _Case(kind, expected_name, fields, descriptors)

    def alternative(self, tag, children):
        cases = []
        if tag in (0x23, 0x25):
            cases.append(self.builtin_case(_variants.Some, (("value", children[0]),)))
        if tag in (0x23, 0x26):
            cases.append(self.builtin_case(_variants.Nothing, ()))
        if tag in (0x24, 0x27):
            cases.append(self.builtin_case(_variants.Ok, (("value", children[0]),)))
        if tag in (0x24, 0x28):
            cases.append(self.builtin_case(_variants.Err, (("error", children[1] if tag == 0x24 else children[0]),)))
        return _Node(tag, children=children, cases=tuple(cases))

    def annotation(self, annotation, depth=0):
        self.budget.node(depth)
        for tag, kind in _SCALARS:
            if annotation is kind or tag == 0 and annotation is None:
                return _Node(tag, kind)
        info = self.find(self.records, annotation)
        if info is not None:
            return self.record(info, depth)
        info = self.find(self.domains, annotation)
        if info is not None:
            return self.domain(info, depth)
        info = self.find(self.cases, annotation)
        if info is not None and info[3] is not None:
            if annotation is _variants.Nothing:
                return self.alternative(0x26, ())
            if info[3] is not _variants.Option and info[3] is not _variants.Result:
                domain = self.annotation(info[3], depth + 1)
                selected = next((index for index, case in enumerate(domain.cases) if case.kind is annotation), None)
                if selected is None:
                    _type_error("schema", "malformed product schema metadata")
                return _Node(0x22, annotation, children=(domain,), selected=selected)
        if type(annotation) is not GenericAlias:
            _type_error("schema", "unsupported exact schema")
        origin = object.__getattribute__(annotation, "__origin__")
        arguments = object.__getattribute__(annotation, "__args__")
        if type(arguments) is not tuple:
            _type_error("schema", "unsupported schema origin/arity")
        if origin is tuple:
            variadic = len(arguments) == 2 and arguments[1] is Ellipsis
            if variadic:
                children = (self.annotation(arguments[0], depth + 1),)
            else:
                _limit(len(arguments), MAX_ITEMS, "schema", "schema tuple count")
                children = tuple(self.annotation(child, depth + 1) for child in arguments)
            return _Node(0x11 if variadic else 0x10, tuple, children)
        for tag, kind in _COLLECTIONS:
            if origin is kind:
                arity = 2 if tag in (0x13, 0x14) else 1
                if len(arguments) != arity:
                    _type_error("schema", "unsupported schema origin/arity")
                children = tuple(self.annotation(child, depth + 1) for child in arguments)
                if tag in (0x13, 0x14, 0x15) and children[0].tag > 4:
                    _type_error("schema", "unsupported schema key domain")
                return _Node(tag, kind, children, descriptors=(_collection_descriptor(kind),))
        for tag, kind, arity in ((0x23, _variants.Option, 1), (0x24, _variants.Result, 2),
                                  (0x25, _variants.Some, 1), (0x27, _variants.Ok, 1), (0x28, _variants.Err, 1)):
            if origin is kind:
                if len(arguments) != arity:
                    _type_error("schema", "unsupported schema origin/arity")
                return self.alternative(tag, tuple(self.annotation(child, depth + 1) for child in arguments))
        _type_error("schema", "unsupported schema origin/arity")

    def internal(self, schema, depth):
        # These are fixed declaration schemas, not caller-supplied descriptors.
        self.budget.node(depth)
        if type(schema) is str:
            for name, (tag, kind) in zip(("None", "bool", "int", "str", "bytes"), _SCALARS):
                if schema == name:
                    return _Node(tag, kind)
            _type_error("schema", "malformed product schema metadata")
        if type(schema) is not tuple or not schema or type(schema[0]) is not str:
            _type_error("schema", "malformed product schema metadata")
        name = schema[0]
        if name == "record" and len(schema) == 3:
            info = self.find(self.records, schema[1])
            if info is None or schema[2] is not info[1]:
                _type_error("schema", "malformed product schema metadata")
            return self.record(info, depth)
        if name == "variant" and len(schema) == 3:
            info = self.find(self.domains, schema[1])
            if info is None or schema[2] is not info[2]:
                _type_error("schema", "malformed product schema metadata")
            return self.domain(info, depth)
        if name == "case" and len(schema) == 3:
            info = self.find(self.cases, schema[1])
            if info is None or schema[2] is not info[1] or info[3] is None:
                _type_error("schema", "malformed product schema metadata")
            domain = self.annotation(info[3], depth + 1)
            selected = next((index for index, case in enumerate(domain.cases) if case.kind is schema[1]), None)
            if selected is None:
                _type_error("schema", "malformed product schema metadata")
            return _Node(0x22, schema[1], children=(domain,), selected=selected)
        if name == "tuple" and len(schema) == 3 and type(schema[1]) is tuple and type(schema[2]) is bool:
            if schema[2] and len(schema[1]) != 1:
                _type_error("schema", "malformed product schema metadata")
            _limit(len(schema[1]), MAX_ITEMS, "schema", "schema tuple count")
            return _Node(0x11 if schema[2] else 0x10, tuple,
                         tuple(self.internal(child, depth + 1) for child in schema[1]))
        if len(schema) == 2 and type(schema[1]) is tuple:
            for tag, kind in _COLLECTIONS:
                if name == _native_type_read(kind, "__name__"):
                    arity = 2 if tag in (0x13, 0x14) else 1
                    if len(schema[1]) != arity:
                        _type_error("schema", "malformed product schema metadata")
                    children = tuple(self.internal(child, depth + 1) for child in schema[1])
                    if tag in (0x13, 0x14, 0x15) and children[0].tag > 4:
                        _type_error("schema", "unsupported schema key domain")
                    return _Node(tag, kind, children, descriptors=(_collection_descriptor(kind),))
            for token, tag, arity in (("Option", 0x23, 1), ("Result", 0x24, 2), ("Some", 0x25, 1),
                                      ("Nothing", 0x26, 0), ("Ok", 0x27, 1), ("Err", 0x28, 1)):
                if name == token and len(schema[1]) == arity:
                    return self.alternative(tag, tuple(self.internal(child, depth + 1) for child in schema[1]))
        _type_error("schema", "malformed product schema metadata")


class _Writer:
    __slots__ = ("items", "maximum", "label")

    def __init__(self, maximum, label):
        self.items, self.maximum, self.label = [], maximum, label

    def byte(self, value):
        _limit(len(self.items) + 1, self.maximum, self.label, self.label + " bytes")
        self.items.append(value)

    def raw(self, values):
        _limit(len(self.items) + len(values), self.maximum, self.label, self.label + " bytes")
        self.items.extend(values)

    def number(self, value, width=4):
        for shift in range((width - 1) * 8, -1, -8):
            self.byte((value >> shift) & 255)

    def text(self, value, maximum, path):
        _limit(len(value), maximum, path, "string" if maximum == MAX_STRING else "schema name")
        _limit(len(self.items) + 4 + 4 * len(value), self.maximum, self.label, self.label + " bytes")
        self.number(len(value))
        for character in value:
            self.number(ord(character))

    def result(self):
        return bytes(self.items)


def _write_schema(node, writer):
    writer.byte(node.tag)
    if node.tag <= 4 or node.tag == 0x26:
        return
    if node.tag == 0x20:
        writer.text(node.identity, MAX_IDENTITY, "schema")
        writer.number(len(node.fields))
        for name, child in node.fields:
            writer.text(name, MAX_NAME, "schema")
            _write_schema(child, writer)
    elif node.tag == 0x21:
        writer.text(node.identity, MAX_IDENTITY, "schema")
        writer.number(len(node.cases))
        for case in node.cases:
            writer.text(case.name, MAX_NAME, "schema")
            writer.number(len(case.fields))
            for name, child in case.fields:
                writer.text(name, MAX_NAME, "schema")
                _write_schema(child, writer)
    elif node.tag == 0x22:
        _write_schema(node.children[0], writer)
        writer.text(node.children[0].cases[node.selected].name, MAX_NAME, "schema")
    else:
        if node.tag == 0x10:
            writer.number(len(node.children))
        for child in node.children:
            _write_schema(child, writer)


def _compile(schema):
    compiler = _Compiler()
    node = compiler.annotation(schema)
    writer = _Writer(MAX_SCHEMA_BYTES, "schema")
    _write_schema(node, writer)
    return node, writer.result()


def _read_storage(value, descriptor, path):
    try:
        data = MemberDescriptorType.__get__(descriptor, value, type(value))
    except AttributeError:
        _type_error(path, "malformed product storage")
    if type(data) is not tuple:
        _type_error(path, "malformed product storage")
    return data


def _read_fields(value, item, path):
    try:
        initialized = MemberDescriptorType.__get__(item.descriptors[-1], value, item.kind)
    except AttributeError:
        _type_error(path, "uninitialized product storage")
    if initialized is not True:
        _type_error(path, "uninitialized product storage")
    values = []
    for (name, _), descriptor in zip(item.fields, item.descriptors):
        try:
            values.append(MemberDescriptorType.__get__(descriptor, value, item.kind))
        except AttributeError:
            _type_error(path + "." + name, "malformed product storage")
    return tuple(values)


def _canonical(items, key_schema, path, pairs=False):
    # Structural/type/duplicate phases disclose no unordered incidental index.
    if pairs and any(type(pair) is not tuple or len(pair) != 2 for pair in items):
        _type_error(path + ".storage", "malformed product storage")
    keys = tuple(pair[0] for pair in items) if pairs else items
    if any(type(key) is not key_schema.kind for key in keys):
        _type_error(path + (".keys" if pairs else ".members"), "keys/members require selected exact scalar domain")
    ordered = items if key_schema.tag == 0 else tuple(sorted(items, key=lambda pair: pair[0])) if pairs else tuple(sorted(items))
    ordered_keys = tuple(pair[0] for pair in ordered) if pairs else ordered
    if any(left == right for left, right in zip(ordered_keys, ordered_keys[1:])):
        _type_error(path + (".keys" if pairs else ".members"), "duplicate collection key/member")
    return ordered


def _encode(value, node, writer, budget, depth, path):
    budget.node(depth)
    tag = node.tag
    if tag <= 4:
        if type(value) is not node.kind:
            _type_error(path, "expected exact selected value type")
        writer.byte(tag)
        if tag == 1:
            writer.byte(1 if value else 0)
        elif tag == 2:
            if value < MIN_INTEGER or value > MAX_INTEGER:
                _value_error(path, "integer outside signed64 encoding domain")
            writer.number(value if value >= 0 else value + 2 ** 64, 8)
        elif tag == 3:
            writer.text(value, MAX_STRING, path)
        elif tag == 4:
            _limit(len(value), MAX_BYTES, path, "bytes")
            writer.number(len(value))
            writer.raw(value)
        return
    if tag in (0x21, 0x22) or tag >= 0x23:
        cases = node.children[0].cases if tag == 0x22 else node.cases
        selected = next((index for index, case in enumerate(cases) if type(value) is case.kind), None)
        if selected is None or tag == 0x22 and selected != node.selected:
            _type_error(path, "expected exact selected value type")
        item = cases[selected]
    else:
        if type(value) is not node.kind:
            _type_error(path, "expected exact selected value type")
        item = node
    identity = id(value)
    if identity in budget.active:
        _type_error(path, "cyclic data")
    budget.active.add(identity)
    try:
        if tag in (0x20, 0x21, 0x22) or tag >= 0x23:
            values = _read_fields(value, item, path)
            if tag == 0x20:
                writer.byte(0x20)
                writer.number(len(values))
            elif tag in (0x21, 0x22):
                writer.byte(0x21)
                writer.number(selected)
                writer.number(len(values))
            else:
                wire_tag = next(wire for kind, wire in ((_variants.Some, 0x31), (_variants.Nothing, 0x32),
                                                        (_variants.Ok, 0x33), (_variants.Err, 0x34)) if item.kind is kind)
                writer.byte(wire_tag)
            for (name, child), member in zip(item.fields, values):
                _encode(member, child, writer, budget, depth + 1, path + "." + name)
        elif tag in (0x10, 0x11, 0x12, 0x15):
            values = value if tag in (0x10, 0x11) else _read_storage(value, node.descriptors[0], path + ".storage")
            _limit(len(values), MAX_ITEMS, path, "container")
            if tag == 0x10 and len(values) != len(node.children):
                _type_error(path, "fixed tuple length differs from schema")
            if tag == 0x15:
                values = _canonical(values, node.children[0], path)
            writer.byte(0x10 if tag == 0x11 else tag)
            writer.number(len(values))
            for index, member in enumerate(values):
                child = node.children[index] if tag == 0x10 else node.children[0]
                _encode(member, child, writer, budget, depth + 1, path + "[" + str(index) + "]")
        else:
            entries = _read_storage(value, node.descriptors[0], path + ".storage")
            _limit(len(entries), MAX_ITEMS, path, "container")
            canonical = _canonical(entries, node.children[0], path, pairs=True)
            traversal = entries if tag == 0x13 else canonical
            writer.byte(tag)
            writer.number(len(traversal))
            for index, (key, member) in enumerate(traversal):
                location = path + ".entries[" + str(index) + "]"
                _encode(key, node.children[0], writer, budget, depth + 1, location + ".key")
                _encode(member, node.children[1], writer, budget, depth + 1, location + ".value")
    finally:
        budget.active.remove(identity)


class _Reader:
    __slots__ = ("data", "index", "end", "label")

    def __init__(self, data, start=0, end=None, label="data"):
        self.data, self.index, self.end, self.label = data, start, len(data) if end is None else end, label

    def byte(self):
        if self.index >= self.end:
            _value_error(self.label, "truncated " + self.label)
        value = self.data[self.index]
        self.index += 1
        return value

    def number(self, width=4):
        if width > self.end - self.index:
            _value_error(self.label, "truncated " + self.label)
        value = 0
        for _ in range(width):
            value = (value << 8) | self.byte()
        return value

    def raw(self, count):
        if count > self.end - self.index:
            _value_error(self.label, "truncated " + self.label)
        result = self.data[self.index:self.index + count]
        self.index += count
        return result

    def text(self, maximum, path):
        count = self.number()
        _limit(count, maximum, path, "string" if maximum == MAX_STRING else "schema name")
        if count * 4 > self.end - self.index:
            _value_error(self.label, "truncated " + self.label)
        characters = []
        for _ in range(count):
            point = self.number()
            if point > 0x10ffff:
                _value_error(path, "invalid code point")
            characters.append(chr(point))
        return str.join("", characters)


def _parse_fields(reader, budget, depth):
    count = reader.number()
    _limit(count, MAX_FIELDS, "schema", "schema field count")
    names, fields = set(), []
    for _ in range(count):
        name = _name(reader.text(MAX_NAME, "schema"), wire=True)
        if name in names:
            _value_error("schema", "duplicate schema field")
        names.add(name)
        fields.append((name, _parse_schema(reader, budget, depth + 1)))
    return tuple(fields)


def _parse_schema(reader, budget, depth=0):
    budget.node(depth)
    tag = reader.byte()
    if tag <= 4 or tag == 0x26:
        return (tag,)
    if tag == 0x10:
        count = reader.number()
        _limit(count, MAX_ITEMS, "schema", "schema tuple count")
        return (tag, tuple(_parse_schema(reader, budget, depth + 1) for _ in range(count)))
    if tag in (0x11, 0x12, 0x13, 0x14, 0x15, 0x23, 0x24, 0x25, 0x27, 0x28):
        count = 2 if tag in (0x13, 0x14, 0x24) else 1
        children = tuple(_parse_schema(reader, budget, depth + 1) for _ in range(count))
        if tag in (0x13, 0x14, 0x15) and children[0][0] > 4:
            _value_error("schema", "invalid schema key domain")
        return (tag, children)
    if tag == 0x20:
        identity = _name(reader.text(MAX_IDENTITY, "schema"), identity=True, wire=True)
        return (tag, identity, _parse_fields(reader, budget, depth))
    if tag == 0x21:
        identity = _name(reader.text(MAX_IDENTITY, "schema"), identity=True, wire=True)
        count = reader.number()
        _limit(count, MAX_CASES, "schema", "schema case count")
        if count == 0:
            _value_error("schema", "invalid schema case count")
        names, cases = set(), []
        for _ in range(count):
            name = _name(reader.text(MAX_NAME, "schema"), wire=True)
            if name in names:
                _value_error("schema", "duplicate schema case")
            names.add(name)
            cases.append((name, _parse_fields(reader, budget, depth)))
        return (tag, identity, tuple(cases))
    if tag == 0x22:
        domain = _parse_schema(reader, budget, depth + 1)
        if domain[0] != 0x21:
            _value_error("schema", "invalid exact-case schema")
        selected = _name(reader.text(MAX_NAME, "schema"), wire=True)
        if not any(selected == name for name, _ in domain[2]):
            _value_error("schema", "selected case absent")
        return (tag, domain, selected)
    _value_error("schema", "unsupported schema tag")


def _allocate_fields(item, values):
    value = object.__new__(item.kind)
    for descriptor, member in zip(item.descriptors, values):
        MemberDescriptorType.__set__(descriptor, value, member)
    MemberDescriptorType.__set__(item.descriptors[-1], value, True)
    return value


def _allocate_collection(node, values):
    value = object.__new__(node.kind)
    MemberDescriptorType.__set__(node.descriptors[0], value, values)
    return value


def _decode(node, reader, budget, depth, path):
    budget.node(depth)
    tag = reader.byte()
    expected = 0x10 if node.tag == 0x11 else 0x21 if node.tag == 0x22 else node.tag
    if node.tag >= 0x23:
        kind = next((kind for wire, kind in ((0x31, _variants.Some), (0x32, _variants.Nothing),
                                            (0x33, _variants.Ok), (0x34, _variants.Err)) if tag == wire), None)
        item = next((case for case in node.cases if case.kind is kind), None)
        if item is None:
            _value_error(path, "value tag differs from selected schema")
        return _allocate_fields(item, tuple(_decode(child, reader, budget, depth + 1, path + "." + name)
                                            for name, child in item.fields))
    if tag != expected:
        _value_error(path, "value tag differs from selected schema")
    if tag <= 4:
        if tag == 0:
            return None
        if tag == 1:
            value = reader.byte()
            if value > 1:
                _value_error(path, "invalid bool")
            return value == 1
        if tag == 2:
            value = reader.number(8)
            return value if value < 2 ** 63 else value - 2 ** 64
        if tag == 3:
            return reader.text(MAX_STRING, path)
        count = reader.number()
        _limit(count, MAX_BYTES, path, "bytes")
        return reader.raw(count)
    if tag in (0x20, 0x21):
        if tag == 0x21:
            domain = node.children[0] if node.tag == 0x22 else node
            selected = reader.number()
            if selected >= len(domain.cases):
                _value_error(path, "case index outside selected closed domain")
            if node.tag == 0x22 and selected != node.selected:
                _value_error(path, "case index differs from selected schema")
            item = domain.cases[selected]
        else:
            item = node
        count = reader.number()
        if count != len(item.fields):
            _value_error(path, "record/case field count mismatch")
        values = tuple(_decode(child, reader, budget, depth + 1, path + "." + name) for name, child in item.fields)
        return _allocate_fields(item, values)
    count = reader.number()
    _limit(count, MAX_ITEMS, path, "container")
    if tag in (0x10, 0x12, 0x15):
        if node.tag == 0x10 and count != len(node.children):
            _value_error(path, "fixed tuple length differs from schema")
        values = []
        for index in range(count):
            child = node.children[index] if node.tag == 0x10 else node.children[0]
            member = _decode(child, reader, budget, depth + 1, path + "[" + str(index) + "]")
            if tag == 0x15 and values and (member == values[-1] or child.tag == 0 or member < values[-1]):
                _value_error(path, "duplicate/noncanonical set member")
            values.append(member)
        values = tuple(values)
        return values if tag == 0x10 else _allocate_collection(node, values)
    entries, sorted_keys = [], []
    for index in range(count):
        location = path + ".entries[" + str(index) + "]"
        key = _decode(node.children[0], reader, budget, depth + 1, location + ".key")
        if tag == 0x14 and entries:
            previous = entries[-1][0]
            if key == previous or node.children[0].tag == 0 or key < previous:
                _value_error(path, "duplicate/noncanonical map key")
        if tag == 0x13:
            if any(key == previous for previous in sorted_keys):
                _value_error(path, "duplicate/noncanonical map key")
            sorted_keys.append(key)
        member = _decode(node.children[1], reader, budget, depth + 1, location + ".value")
        entries.append((key, member))
    return _allocate_collection(node, tuple(entries))


def value_encode(value, schema, /):
    """Encode exact selected stable data; signed64 and finite v1 limits apply."""
    node, descriptor = _compile(schema)
    writer = _Writer(MAX_WIRE_BYTES, "envelope")
    writer.raw(_MAGIC)
    writer.number(len(descriptor))
    writer.raw(descriptor)
    _encode(value, node, writer, _Budget(MAX_VALUE_NODES, "value"), 0, "value")
    return writer.result()


def value_decode(data, schema, /):
    """Decode canonical v1 bytes without imports, constructors or restoration."""
    if type(data) is not bytes:
        _type_error("data", "expected exact selected value type")
    _limit(len(data), MAX_WIRE_BYTES, "data", "envelope")
    node, descriptor = _compile(schema)
    reader = _Reader(data)
    if reader.raw(len(_MAGIC)) != _MAGIC:
        _value_error("data", "unsupported magic/version")
    count = reader.number()
    _limit(count, MAX_SCHEMA_BYTES, "schema", "schema bytes")
    if count > reader.end - reader.index:
        _value_error("schema", "truncated schema")
    start = reader.index
    schema_reader = _Reader(data, start, start + count, "schema")
    _parse_schema(schema_reader, _Budget(MAX_SCHEMA_NODES, "schema"))
    if schema_reader.index != schema_reader.end:
        _value_error("schema", "trailing schema bytes")
    if reader.raw(count) != descriptor:
        _value_error("schema", "wire schema differs from selected schema")
    reader.label = "value"
    value = _decode(node, reader, _Budget(MAX_VALUE_NODES, "value"), 0, "value")
    if reader.index != reader.end:
        _value_error("data", "trailing value bytes")
    return value
