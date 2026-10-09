"""Exact immutable collections using a dependency-free tuple backend.

Updates copy O(n) tuple storage. Keeping k n-sized versions can retain O(kn)
references. Runtime generic arguments are erased. Higher-order operations accept
exact Python functions; checked purity/signature/capture evidence is the ordinary
caller's obligation, rather than a runtime registry or per-call purity guard.
"""

from types import FunctionType, GenericAlias

__all__ = ["Vector", "OrderedMap", "Map", "Set"]

_SCALAR_TYPES = (type(None), bool, int, str, bytes)


def _scalar_type(kind):
    return any(kind is admitted for admitted in _SCALAR_TYPES)


def _collection_type(kind):
    return any(kind is admitted for admitted in _COLLECTION_TYPES)


def _invalid(path, reason="expected exact recursively immutable data"):
    # Never inspect or represent an inadmissible object's type or value.
    raise TypeError(f"{path}: {reason}")


def _storage(value, name, path):
    try:
        data = object.__getattribute__(value, name)
    except AttributeError:
        _invalid(path, "malformed collection storage")
    if type(data) is not tuple:
        _invalid(path, "malformed collection storage")
    return data


def _validate(value, path="value", active=None):
    """Closed structural validation, without foreign hooks or mutable aliases."""
    kind = type(value)
    if _scalar_type(kind):
        return
    if kind is not tuple and not _collection_type(kind):
        _invalid(path)
    active = set() if active is None else active
    identity = id(value)
    if identity in active:
        _invalid(path, "cyclic data is unsupported")
    active.add(identity)
    try:
        if kind is tuple:
            for index, item in enumerate(value):
                _validate(item, f"{path}[{index}]", active)
        elif kind is Vector:
            for index, item in enumerate(_storage(value, "_items", path)):
                _validate(item, f"{path}[{index}]", active)
        elif kind is Set:
            _validate_domain(_storage(value, "_items", path), path + ".members")
        else:
            entries = _storage(value, "_entries", path)
            for entry in entries:
                if type(entry) is not tuple or len(entry) != 2:
                    _invalid(path, "malformed map entries")
            _validate_domain(tuple(entry[0] for entry in entries), path + ".keys")
            # A Map's value/error traversal has its canonical scalar-key order.
            traversal = entries if kind is OrderedMap else _canonical_pairs(entries)
            for key, item in traversal:
                _validate(item, path + ".entries[" + _path_key(key) + "].value", active)
    finally:
        active.remove(identity)


def _validate_key(key, path):
    if not _scalar_type(type(key)):
        _invalid(path, "keys/members require exact None, bool, int, str or bytes")


def _validate_domain(keys, path):
    domain = None
    for key in keys:
        _validate_key(key, path)
        if domain is None:
            domain = type(key)
        elif type(key) is not domain:
            _invalid(path, "keys/members must share one exact scalar domain")
    return domain


def _domain(items):
    return type(items[0]) if items else None


def _check_key(key, domain, path="key"):
    _validate_key(key, path)
    if domain is not None and type(key) is not domain:
        _invalid(path, "key/member differs from the collection's exact scalar domain")


def _key_equal(left, right):
    return type(left) is type(right) and left == right


def _canonical_keys(items):
    # All keys are already validated homogeneous exact scalars. None is singleton.
    return tuple(items) if not items or type(items[0]) is type(None) else tuple(sorted(items))


def _canonical_pairs(entries):
    return tuple(entries) if not entries or type(entries[0][0]) is type(None) else tuple(sorted(entries, key=lambda pair: pair[0]))


def _equal(left, right):
    kind = type(left)
    if kind is not type(right):
        return False
    if _scalar_type(kind):
        return left == right
    if kind is tuple:
        return _sequence_equal(left, right)
    if kind is Vector or kind is Set:
        return _sequence_equal(_storage(left, "_items", "left"), _storage(right, "_items", "right"))
    if kind is OrderedMap or kind is Map:
        return _sequence_equal(_storage(left, "_entries", "left"), _storage(right, "_entries", "right"))
    return False


def _sequence_equal(left, right):
    return len(left) == len(right) and all(_equal(a, b) for a, b in zip(left, right))


def _data_repr(value):
    kind = type(value)
    if _scalar_type(kind):
        return repr(value)
    if kind is tuple:
        body = ", ".join(_data_repr(item) for item in value)
        return "(" + body + ("," if len(value) == 1 else "") + ")"
    if _collection_type(kind):
        return kind.__repr__(value)
    _invalid("representation")


def _path_key(key):
    # Exact int decimal formatting has a CPython digit limit. Diagnostic paths
    # must not add that failure to otherwise valid collection operations.
    if type(key) is int:
        try:
            return repr(key)
        except ValueError:
            return hex(key)
    return _data_repr(key)


def _function(callback, path="callback"):
    if type(callback) is not FunctionType:
        _invalid(path, "expected an exact Python function; purity, signature and stable captures are caller obligations")


def _index(index):
    if type(index) is not int:
        _invalid("index", "expected exact int, excluding bool and subclasses")


def _new(cls, attribute, storage):
    value = object.__new__(cls)
    object.__setattr__(value, attribute, storage)
    return value


def _empty(value, attribute):
    try:
        object.__getattribute__(value, attribute)
    except AttributeError:
        object.__setattr__(value, attribute, ())
        return
    raise AttributeError("immutable collection cannot be reinitialized")


class _Frozen:
    __slots__ = ()
    __hash__ = None

    def __setattr__(self, name, value):
        raise AttributeError("immutable collection attributes cannot be assigned")

    def __delattr__(self, name):
        raise AttributeError("immutable collection attributes cannot be deleted")

    @classmethod
    def __class_getitem__(cls, arguments):
        return GenericAlias(cls, arguments)

    def __eq__(self, other):
        return _equal(self, other)

    def __ne__(self, other):
        return not _equal(self, other)


class Vector(_Frozen):
    """Ordered exact stable values; generic element schemas are statically checked."""
    __slots__ = ("_items",)

    def __init__(self):
        _empty(self, "_items")

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Vector is an exact closed collection class")

    @classmethod
    def of(cls, *items):
        for index, value in enumerate(items):
            _validate(value, f"items[{index}]")
        return _new(cls, "_items", items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        # Ordinary ordered traversal only; the checker does not admit general loops.
        return iter(self._items)

    def __getitem__(self, index):
        if type(index) is slice:
            for name in ("start", "stop", "step"):
                bound = getattr(index, name)
                if bound is not None and type(bound) is not int:
                    _invalid("slice." + name, "expected exact int or None")
            return _new(Vector, "_items", self._items[index])
        _index(index)
        return self._items[index]

    def appended(self, value):
        _validate(value)
        return _new(Vector, "_items", self._items + (value,))

    def updated_at(self, index, value):
        _index(index)
        size = len(self._items)
        normalized = index + size if index < 0 else index
        if normalized < 0 or normalized >= size:
            raise IndexError("Vector index out of range")
        _validate(value)
        return _new(Vector, "_items", self._items[:normalized] + (value,) + self._items[normalized + 1:])

    def concat(self, other):
        if type(other) is not Vector:
            _invalid("other", "expected exact Vector")
        _validate(other, "other")
        return _new(Vector, "_items", self._items + other._items)

    def map(self, callback):
        _function(callback)
        output = []
        for index, value in enumerate(self._items):
            result = callback(value)
            _validate(result, f"map.result[{index}]")
            output.append(result)
        return _new(Vector, "_items", tuple(output))

    def filter(self, predicate):
        _function(predicate, "predicate")
        output = []
        for index, value in enumerate(self._items):
            decision = predicate(value)
            if type(decision) is not bool:
                _invalid(f"filter.result[{index}]", "predicate must return exact bool")
            if decision:
                output.append(value)
        return _new(Vector, "_items", tuple(output))

    def fold(self, callback, initial):
        _function(callback)
        _validate(initial, "initial")
        accumulator = initial
        for index, value in enumerate(self._items):
            accumulator = callback(accumulator, value)
            _validate(accumulator, f"fold.accumulator[{index}]")
        return accumulator

    def __repr__(self):
        return "Vector.of(" + ", ".join(_data_repr(value) for value in self._items) + ")"


class _MapBase(_Frozen):
    __slots__ = ("_entries",)

    def __init__(self):
        _empty(self, "_entries")

    @classmethod
    def of(cls, *pairs):
        for pair in pairs:
            if type(pair) is not tuple or len(pair) != 2:
                _invalid("pairs", "expected exact two-element tuple pairs")
        _validate_domain(tuple(pair[0] for pair in pairs), "keys")
        traversal = pairs if cls is OrderedMap else _canonical_pairs(pairs)
        for key, value in traversal:
            _validate(value, "entries[" + _path_key(key) + "].value")
        indexed = tuple((key, value, index) for index, (key, value) in enumerate(pairs))
        ordered = indexed if not indexed or type(indexed[0][0]) is type(None) else sorted(indexed, key=lambda row: row[0])
        entries = []
        for key, value, index in ordered:
            if entries and _key_equal(entries[-1][0], key):
                entries[-1] = (key, value, entries[-1][2])
            else:
                entries.append((key, value, index))
        if cls is OrderedMap:
            entries.sort(key=lambda row: row[2])
        stored = tuple((key, value) for key, value, _ in entries)
        return _new(cls, "_entries", stored)

    def __len__(self):
        return len(self._entries)

    def __iter__(self):
        raise TypeError("map iteration is unsupported; use an explicit characterized Vector traversal")

    def _lookup(self, key):
        _check_key(key, type(self._entries[0][0]) if self._entries else None)
        return next((index for index, pair in enumerate(self._entries) if _key_equal(pair[0], key)), None)

    def __getitem__(self, key):
        index = self._lookup(key)
        if index is None:
            raise KeyError(key)
        return self._entries[index][1]

    def contains(self, key):
        return self._lookup(key) is not None

    def __contains__(self, key):
        return self.contains(key)

    def get(self, key, default):
        _validate(default, "default")
        index = self._lookup(key)
        return default if index is None else self._entries[index][1]

    def updated(self, key, value):
        index = self._lookup(key)
        _validate(value)
        if index is None:
            if type(self) is OrderedMap:
                entries = self._entries + ((key, value),)
            else:
                position = next((i for i, pair in enumerate(self._entries) if key < pair[0]), len(self._entries))
                entries = self._entries[:position] + ((key, value),) + self._entries[position:]
        else:
            entries = self._entries[:index] + ((key, value),) + self._entries[index + 1:]
        return _new(type(self), "_entries", entries)

    def without(self, key):
        index = self._lookup(key)
        if index is None:
            return self
        return _new(type(self), "_entries", self._entries[:index] + self._entries[index + 1:])

    def merge(self, other):
        if type(other) is not type(self):
            _invalid("other", "merge requires the same exact concrete map class")
        _validate(other, "other")
        _validate_domain(tuple(pair[0] for pair in self._entries + other._entries), "keys")
        # Construction applies right-wins duplicate values and preserves OrderedMap slots.
        return type(self).of(*(self._entries + other._entries))

    def __repr__(self):
        name = "OrderedMap" if type(self) is OrderedMap else "Map"
        return name + ".of(" + ", ".join(_data_repr(pair) for pair in self._entries) + ")"


class OrderedMap(_MapBase):
    """First insertion slots are significant; replacement keeps the existing slot."""
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        raise TypeError("OrderedMap is an exact closed collection class")

    def entries(self):
        return _new(Vector, "_items", self._entries)

    def keys(self):
        return _new(Vector, "_items", tuple(pair[0] for pair in self._entries))

    def values(self):
        return _new(Vector, "_items", tuple(pair[1] for pair in self._entries))


class Map(_MapBase):
    """Unordered value semantics with explicit canonical scalar-key traversal."""
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Map is an exact closed collection class")

    def ordered_entries(self):
        return _new(Vector, "_items", self._entries)

    def ordered_keys(self):
        return _new(Vector, "_items", tuple(pair[0] for pair in self._entries))

    def ordered_values(self):
        return _new(Vector, "_items", tuple(pair[1] for pair in self._entries))


class Set(_Frozen):
    """Homogeneous exact scalar members; only canonical ordered export is exposed."""
    __slots__ = ("_items",)

    def __init__(self):
        _empty(self, "_items")

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Set is an exact closed collection class")

    @classmethod
    def of(cls, *items):
        _validate_domain(items, "members")
        output = []
        for item in _canonical_keys(items):
            if not output or not _key_equal(output[-1], item):
                output.append(item)
        return _new(cls, "_items", tuple(output))

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        raise TypeError("unordered Set iteration is unsupported; use ordered_values()")

    def contains(self, value):
        _check_key(value, _domain(self._items), "member")
        return any(_key_equal(item, value) for item in self._items)

    def __contains__(self, value):
        return self.contains(value)

    def added(self, value):
        if self.contains(value):
            return self
        position = next((i for i, item in enumerate(self._items) if value < item), len(self._items))
        return _new(Set, "_items", self._items[:position] + (value,) + self._items[position:])

    def without(self, value):
        if not self.contains(value):
            return self
        return _new(Set, "_items", tuple(item for item in self._items if not _key_equal(item, value)))

    def _other(self, other):
        if type(other) is not Set:
            _invalid("other", "expected exact Set")
        _validate(other, "other")
        _validate_domain(self._items + other._items, "members")

    def union(self, other):
        self._other(other)
        return _new(Set, "_items", self._combined(other, "union"))

    def intersection(self, other):
        self._other(other)
        return _new(Set, "_items", self._combined(other, "intersection"))

    def difference(self, other):
        self._other(other)
        return _new(Set, "_items", self._combined(other, "difference"))

    def _combined(self, other, operation):
        left, right, output = 0, 0, []
        while left < len(self._items) and right < len(other._items):
            a, b = self._items[left], other._items[right]
            if _key_equal(a, b):
                if operation != "difference":
                    output.append(a)
                left += 1
                right += 1
            elif a < b:
                if operation != "intersection":
                    output.append(a)
                left += 1
            else:
                if operation == "union":
                    output.append(b)
                right += 1
        if operation != "intersection":
            output.extend(self._items[left:])
        if operation == "union":
            output.extend(other._items[right:])
        return tuple(output)

    def ordered_values(self):
        return _new(Vector, "_items", self._items)

    def __repr__(self):
        return "Set.of(" + ", ".join(_data_repr(value) for value in self._items) + ")"


_COLLECTION_TYPES = (Vector, OrderedMap, Map, Set)
