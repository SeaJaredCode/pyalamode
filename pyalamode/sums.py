"""Closed tagged sums (@oneof/@case), Option and Result: exact slot classes and native patterns.

The identity catalogs describe data, not callable purity. Generic arguments are
schemas erased by constructors; unchanged definitions remain caller obligations.
"""

from types import GenericAlias, GetSetDescriptorType
from . import collections as _collections
from . import records as _records

__all__ = ["oneof", "case", "Option", "Some", "Nothing", "Result", "Ok", "Err", "accumulate"]

_CASES = ()
_ONEOFS = ()
# Open domains, by identity; their extension cases come from other declarations.
_OPEN = ()
_DATA = object()


def _case_info(kind):
    for entry in _CASES:
        if kind is entry[0] and entry[3] is not None:
            return entry
    return None


def _pending_info(kind):
    for entry in _CASES:
        if kind is entry[0]:
            return entry
    return None


def _oneof_info(kind):
    for entry in _ONEOFS:
        if kind is entry[0]:
            return entry
    return None


def _case_values(value, info, path="case"):
    try:
        initialized = object.__getattribute__(value, "_pal_initialized")
    except AttributeError:
        _collections._invalid(path, "malformed case storage")
    if initialized is not True:
        _collections._invalid(path, "malformed case storage")
    values = []
    for name, _ in info[1]:
        try:
            values.append(object.__getattribute__(value, name))
        except AttributeError:
            _collections._invalid(path + "." + name, "malformed case storage")
    return tuple(values)


def _validate_case(value, info, path, active):
    for (name, schema), item in zip(info[1], _case_values(value, info, path)):
        if schema is _DATA:
            _collections._validate(item, path + "." + name, active)
        else:
            _records._validate_schema(item, schema, path + "." + name, active)


def _case_equal(left, right, info):
    return _collections._sequence_equal(_case_values(left, info), _case_values(right, info))


def _case_repr(value, info):
    return info[5] + "(" + ", ".join(name + "=" + _collections._data_repr(item)
                                    for (name, _), item in zip(info[1], _case_values(value, info))) + ")"


def _make_case(name, module, qualified, doc, fields, defaults, family=None, identity=None):
    global _CASES

    def initialize(self, /, *args, **kwargs):
        info = _case_info(type(self))
        if info is None:
            _collections._invalid("case", "case must belong to its closed domain")
        try:
            object.__getattribute__(self, "_pal_initialized")
        except AttributeError:
            pass
        else:
            raise AttributeError("immutable case cannot be reinitialized")
        names = tuple(field for field, _ in fields)
        if len(args) > len(fields):
            _collections._invalid("case", "too many constructor arguments")
        if any(type(field) is not str for field in kwargs):
            _collections._invalid("case", "constructor field names require exact strings")
        if any(field not in names for field in kwargs):
            _collections._invalid("case", "unknown constructor field")
        values = []
        for index, (field, schema) in enumerate(fields):
            if index < len(args):
                if field in kwargs:
                    _collections._invalid("case." + field, "field supplied twice")
                value = args[index]
            else:
                value = kwargs.get(field, defaults[index])
            if value is _records._MISSING:
                _collections._invalid("case." + field, "required field is missing")
            if schema is _DATA:
                _collections._validate(value, "case." + field)
            else:
                _records._validate_schema(value, schema, "case." + field)
            values.append(value)
        for field in names:
            try:
                object.__getattribute__(self, field)
            except AttributeError:
                continue
            raise AttributeError("immutable case cannot be reinitialized")
        for (field, _), value in zip(fields, values):
            object.__setattr__(self, field, value)
        object.__setattr__(self, "_pal_initialized", True)

    def reject_assignment(self, name, value):
        raise AttributeError("immutable case fields cannot be assigned")

    def reject_deletion(self, name):
        raise AttributeError("immutable case fields cannot be deleted")

    def reject_subclass(subclass, **kwargs):
        raise TypeError("product cases cannot be subclassed")

    def equal(self, other):
        info = _case_info(type(self))
        if info is None:
            _collections._invalid("case", "case must belong to its closed domain")
        return type(self) is type(other) and _case_equal(self, other, info)

    def unequal(self, other):
        return not equal(self, other)

    def representation(self):
        info = _case_info(type(self))
        if info is None:
            _collections._invalid("case", "case must belong to its closed domain")
        return _case_repr(self, info)

    def subscribe(cls, arguments):
        if cls is Some or cls is Ok or cls is Err:
            values = arguments if type(arguments) is tuple else (arguments,)
            if len(values) != 1:
                _collections._invalid("annotation", "payload case requires one data schema")
            _records._annotation_schema(values[0])
            return GenericAlias(cls, values)
        _collections._invalid("annotation", "case generic subscription is unsupported")

    product = type(name, (object,), {
        "__module__": module, "__qualname__": qualified, "__doc__": doc,
        "__slots__": tuple(field for field, _ in fields) + ("_pal_initialized",),
        "__match_args__": tuple(field for field, _ in fields), "__init__": initialize,
        "__setattr__": reject_assignment, "__delattr__": reject_deletion,
        "__init_subclass__": classmethod(reject_subclass), "__eq__": equal, "__ne__": unequal,
        "__repr__": representation, "__hash__": None, "__class_getitem__": classmethod(subscribe),
    })
    _CASES += ((product, fields, defaults, family, identity, name),)
    return product


def _declaration(cls, path):
    if type(cls) is not type:
        _collections._invalid(path, "declaration requires exact type and no bases")
    bases = type.__getattribute__(cls, "__bases__")
    if len(bases) != 1 or bases[0] is not object:
        _collections._invalid(path, "declaration requires exact type and no bases")
    attributes = type.__getattribute__(cls, "__dict__")
    if any(type(name) is not str for name in attributes):
        _collections._invalid(path, "metadata names require exact strings")
    if any(type(type.__getattribute__(cls, name)) is not str for name in ("__module__", "__qualname__", "__name__")):
        _collections._invalid(path, "declaration identity requires exact string metadata")
    if attributes.get("__doc__") is not None and type(attributes.get("__doc__")) is not str:
        _collections._invalid(path, "doc metadata requires an exact string")
    for name in ("__dict__", "__weakref__"):
        descriptor = attributes.get(name)
        if descriptor is not None and (type(descriptor) is not GetSetDescriptorType or descriptor.__objclass__ is not cls):
            _collections._invalid(path, "custom descriptors are unsupported")
    return attributes


def _is_open(kind):
    return any(kind is entry for entry in _OPEN)


def case(cls=None, /, *, of=None):
    """Create a fixed case declaration.

    Nested @case declarations are closed by their containing @oneof. A
    top-level @case(of=Domain) adds a case to an open domain.
    """
    if cls is None:
        if of is None or not _is_open(of):
            _collections._invalid("case", "of= requires an open @oneof(open=True) domain")
        return lambda declaration: _extend(declaration, of)
    if of is not None:
        _collections._invalid("case", "use @case(of=Domain) as a decorator factory")
    return _case(cls)


def _case(cls):
    attributes = _declaration(cls, "case")
    annotations = attributes.get("__annotations__", {})
    if type(annotations) is not dict:
        _collections._invalid("case", "annotations require exact dictionary metadata")
    namespace = _records._namespace(cls)
    fields, defaults = [], []
    saw_default = False
    for name, annotation in annotations.items():
        if type(name) is not str or not name.isidentifier() or name.startswith("_"):
            _collections._invalid("case", "fields require public identifiers")
        schema = _records._annotation_schema(annotation, namespace)
        _records._check_schema(schema)
        default = attributes.get(name, _records._MISSING)
        if default is not _records._MISSING:
            _records._validate_schema(default, schema, "default." + name)
            saw_default = True
        elif saw_default:
            _collections._invalid("case", "required fields cannot follow defaults")
        fields.append((name, schema))
        defaults.append(default)
    allowed = {"__module__", "__qualname__", "__doc__", "__annotations__", "__dict__", "__weakref__",
               "__firstlineno__", "__static_attributes__"}
    allowed.update(name for name, _ in fields)
    if any(name not in allowed for name in attributes):
        _collections._invalid("case", "declarations contain only typed fields and stable defaults")
    return _make_case(type.__getattribute__(cls, "__name__"), type.__getattribute__(cls, "__module__"),
                      type.__getattribute__(cls, "__qualname__"), attributes.get("__doc__"), tuple(fields), tuple(defaults))


class _DomainType(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError("closed domain is a namespace, not a value constructor")

    def __setattr__(cls, name, value):
        raise AttributeError("closed domain namespace cannot be assigned")

    def __delattr__(cls, name):
        raise AttributeError("closed domain namespace cannot be deleted")

    def __instancecheck__(cls, instance):
        # Native `case Domain():` matches exactly the domain's own case classes.
        info = _oneof_info(cls)
        kind = type(instance)
        return info is not None and any(kind is case for case, _ in info[2])


def _extend(cls, domain):
    """Attach a top-level extension case to an open domain, in canonical order."""
    global _CASES, _ONEOFS
    info = _oneof_info(domain)
    product = _case(cls)
    entry = _pending_info(product)
    qualified = type.__getattribute__(product, "__qualname__")
    if info is None or qualified != entry[5]:
        _collections._invalid("case", "extension cases are top-level declarations of an open domain")
    if any(_pending_info(kind)[5] == entry[5] for kind, _ in info[2]):
        _collections._invalid("case", "open domain already has a case with this name")
    _CASES = tuple((kind, fields, defaults, domain, info[1], name) if kind is product else row
                   for row in _CASES for kind, fields, defaults, family, old_identity, name in (row,))
    domain_module = type.__getattribute__(domain, "__module__")
    domain_qualified = type.__getattribute__(domain, "__qualname__")

    def nested(kind):
        return (type.__getattribute__(kind, "__module__") == domain_module
                and type.__getattribute__(kind, "__qualname__").startswith(domain_qualified + "."))

    def key(item):
        return (type.__getattribute__(item[0], "__module__"), type.__getattribute__(item[0], "__qualname__"))
    cases = info[2] + ((product, entry[1]),)
    ordered = tuple(item for item in cases if nested(item[0])) + tuple(sorted((item for item in cases if not nested(item[0])), key=key))
    _ONEOFS = tuple((kind, identity, ordered) if kind is domain else row
                    for row in _ONEOFS for kind, identity, _ in (row,))
    return product


def oneof(cls=None, /, *, open=False):
    """Seal a declaration-only namespace with its nested case set.

    @oneof is closed. @oneof(open=True) also accepts top-level
    @case(of=Domain) declarations; matches outside the defining
    distribution must then end with a wildcard.
    """
    if type(open) is not bool:
        _collections._invalid("oneof", "open requires an exact bool")
    if cls is None:
        return lambda declaration: _seal(declaration, open)
    return _seal(cls, open)


def _seal(cls, is_open):
    global _CASES, _ONEOFS, _OPEN
    attributes = _declaration(cls, "oneof")
    cases = []
    allowed = {"__module__", "__qualname__", "__doc__", "__dict__", "__weakref__",
               "__firstlineno__", "__static_attributes__"}
    module = type.__getattribute__(cls, "__module__")
    qualified = type.__getattribute__(cls, "__qualname__")
    for name, value in attributes.items():
        if name in allowed:
            continue
        if not name.isidentifier() or name.startswith("_"):
            _collections._invalid("oneof", "cases require public identifiers")
        info = _pending_info(value)
        if info is None or info[3] is not None:
            _collections._invalid("oneof", "domain contains only unattached exact case declarations")
        if type.__getattribute__(value, "__module__") != module or type.__getattribute__(value, "__qualname__") != qualified + "." + name or info[5] != name:
            _collections._invalid("oneof", "case must be declared inside its domain under its own name")
        cases.append((value, info[1]))
    if not cases and not is_open:
        _collections._invalid("oneof", "domain requires at least one case")

    def reject_subclass(subclass, **kwargs):
        raise TypeError("closed domains cannot be subclassed")

    namespace = {"__module__": module, "__qualname__": qualified, "__doc__": attributes.get("__doc__"),
                 "__slots__": (), "__init_subclass__": classmethod(reject_subclass)}
    namespace.update((type.__getattribute__(kind, "__name__"), kind) for kind, _ in cases)
    product = _DomainType(type.__getattribute__(cls, "__name__"), (object,), namespace)
    identity = module + ":" + qualified
    _CASES = tuple((kind, fields, defaults, product, identity, name)
                   if any(kind is candidate for candidate, _ in cases) else entry
                   for entry in _CASES for kind, fields, defaults, family, old_identity, name in (entry,))
    _ONEOFS += ((product, identity, tuple(cases)),)
    if is_open:
        _OPEN += (product,)
    return product


class Option:
    """Annotation-only absence family; construct Some or Nothing values."""
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        raise TypeError("construct Some or Nothing, not Option")

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Option is an exact closed schema family")

    @classmethod
    def __class_getitem__(cls, arguments):
        values = arguments if type(arguments) is tuple else (arguments,)
        if len(values) != 1:
            _collections._invalid("annotation", "Option requires one data schema")
        _records._annotation_schema(values[0])
        return GenericAlias(cls, values)


class Result:
    """Annotation-only success/error family; construct Ok or Err values."""
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        raise TypeError("construct Ok or Err, not Result")

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Result is an exact closed schema family")

    @classmethod
    def __class_getitem__(cls, arguments):
        if type(arguments) is not tuple or len(arguments) != 2:
            _collections._invalid("annotation", "Result requires two data schemas")
        for child in arguments:
            _records._annotation_schema(child)
        return GenericAlias(cls, arguments)


Some = _make_case("Some", "pyalamode", "Some", "A present immutable value.", (("value", _DATA),), (_records._MISSING,), Option, "pyalamode:Option")
Nothing = _make_case("Nothing", "pyalamode", "Nothing", "An absent value.", (), (), Option, "pyalamode:Option")
Ok = _make_case("Ok", "pyalamode", "Ok", "An immutable successful value.", (("value", _DATA),), (_records._MISSING,), Result, "pyalamode:Result")
Err = _make_case("Err", "pyalamode", "Err", "An immutable error value.", (("error", _DATA),), (_records._MISSING,), Result, "pyalamode:Result")


def _schema_origins():
    return (("Option", Option), ("Result", Result), ("Some", Some), ("Nothing", Nothing), ("Ok", Ok), ("Err", Err))


def _annotation_schema(annotation, namespace):
    info = _oneof_info(annotation)
    if info is not None:
        return ("oneof", info[0], info[2])
    info = _case_info(annotation)
    if info is not None and info[3] is not Option and info[3] is not Result:
        return ("case", info[0], info[1])
    if annotation is Nothing:
        return ("Nothing", ())
    if type(annotation) is GenericAlias:
        origin = object.__getattribute__(annotation, "__origin__")
        for name, cls in _schema_origins():
            if origin is cls:
                arguments = object.__getattribute__(annotation, "__args__")
                schema = (name, tuple(_records._annotation_schema(child, namespace) for child in arguments))
                _check_schema(schema)
                return schema
    return None


def _annotation_origin(origin):
    return next((name for name, cls in _schema_origins() if origin is cls), None)


def _annotation_attribute(owner, name):
    info = _oneof_info(owner)
    if info is not None:
        return next((kind for kind, _ in info[2] if type.__getattribute__(kind, "__name__") == name), _records._MISSING)
    return _records._MISSING


def _check_fields(fields):
    if type(fields) is not tuple:
        _collections._invalid("schema", "case fields require exact tuple metadata")
    for field in fields:
        if type(field) is not tuple or len(field) != 2 or type(field[0]) is not str:
            _collections._invalid("schema", "malformed case fields")
        _records._check_schema(field[1])


def _check_schema(schema):
    name = schema[0]
    if name == "oneof":
        if len(schema) != 3 or type(schema[2]) is not tuple:
            _collections._invalid("schema", "malformed oneof schema")
        info = _oneof_info(schema[1])
        if info is None:
            _collections._invalid("schema", "expected exact declared domain")
        for entry in schema[2]:
            if type(entry) is not tuple or len(entry) != 2:
                _collections._invalid("schema", "malformed domain cases")
            case_info = _case_info(entry[0])
            if case_info is None or case_info[3] is not info[0]:
                _collections._invalid("schema", "case belongs to another domain")
            _check_fields(entry[1])
        if schema[2] != info[2]:
            _collections._invalid("schema", "oneof differs from its closed case set")
        return True
    if name == "case":
        if len(schema) != 3:
            _collections._invalid("schema", "malformed case schema")
        info = _case_info(schema[1])
        if info is None or info[3] is Option or info[3] is Result:
            _collections._invalid("schema", "expected exact declared case")
        _check_fields(schema[2])
        if schema[2] != info[1]:
            _collections._invalid("schema", "case differs from its fixed fields")
        return True
    if name in ("Option", "Result", "Some", "Nothing", "Ok", "Err"):
        arity = 2 if name == "Result" else 0 if name == "Nothing" else 1
        if len(schema) != 2 or type(schema[1]) is not tuple or len(schema[1]) != arity:
            _collections._invalid("schema", "malformed alternative schema")
        for child in schema[1]:
            _records._check_schema(child)
        return True
    return False


def _validate_schema(value, schema, path, active):
    kind = type(value)
    info = _case_info(kind)
    name = schema[0]
    if info is None:
        _collections._invalid(path, "expected exact " + name)
    if name == "oneof":
        if info[3] is not schema[1]:
            _collections._invalid(path, "expected exact declared domain case")
        fields = info[1]
    elif name == "case":
        if kind is not schema[1]:
            _collections._invalid(path, "expected exact declared case")
        fields = info[1]
    elif name == "Option":
        if kind is not Some and kind is not Nothing:
            _collections._invalid(path, "expected exact Option case")
        fields = (("value", schema[1][0]),) if kind is Some else ()
    elif name == "Result":
        if kind is not Ok and kind is not Err:
            _collections._invalid(path, "expected exact Result case")
        fields = (("value", schema[1][0]),) if kind is Ok else (("error", schema[1][1]),)
    else:
        expected = next(cls for token, cls in _schema_origins() if token == name)
        if kind is not expected:
            _collections._invalid(path, "expected exact " + name)
        fields = () if kind is Nothing else ((info[1][0][0], schema[1][0]),)
    active = set() if active is None else active
    identity = id(value)
    if identity in active:
        _collections._invalid(path, "cyclic data is unsupported")
    active.add(identity)
    try:
        for (field, child), item in zip(fields, _case_values(value, info, path)):
            _records._validate_schema(item, child, path + "." + field, active)
    finally:
        active.remove(identity)


def accumulate(left, right):
    """Combine two independently computed exact Results, retaining error order."""
    if not (type(left) is Ok or type(left) is Err) or not (type(right) is Ok or type(right) is Err):
        _collections._invalid("accumulate", "expected two exact Result cases")
    _collections._validate(left, "left")
    _collections._validate(right, "right")
    if type(left) is Ok and type(right) is Ok:
        return Ok((_case_values(left, _case_info(Ok))[0], _case_values(right, _case_info(Ok))[0]))
    errors = tuple(_case_values(value, _case_info(Err))[0] for value in (left, right) if type(value) is Err)
    return Err(_collections.Vector.of(*errors))
