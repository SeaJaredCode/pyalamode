"""Finite ordinary effect declarations and opaque capability providers.

Declarations are identity markers, never callable evidence. Provider setup is
ordinary shell work. Borrowing is a logical lease, not an OS handle transfer or
security boundary; filesystem consistency and dependency integrity remain
caller preconditions.
"""

import os
import stat
import time
import typing
import collections.abc
import sys
import _thread
from types import GenericAlias
from . import records as _records
from . import standard as _standard

IO = "IO"
State = "State"
Clock = "Clock"
Random = "Random"
Environment = "Environment"
Task = "Task"
_FAMILIES = (IO, State, Clock, Random, Environment, Task)

__all__ = ["effects", "Effectful", "IO", "State", "Clock", "Random", "Environment", "Task",
           "IOCapability", "StateCapability", "ClockCapability", "RandomCapability", "EnvironmentCapability", "TaskCapability",
           "borrow", "live_io", "recorded_io", "state", "live_clock", "recorded_clock",
           "live_random", "recorded_random", "live_environment", "recorded_environment"]


def _invalid(path, reason):
    raise TypeError(path + ": " + reason)


def _exact(value, kind, path):
    if type(value) is not kind:
        _invalid(path, "unsupported exact input type")


def _scalar_text(value, path):
    _exact(value, str, path)
    for character in value:
        if 0xD800 <= ord(character) <= 0xDFFF:
            raise ValueError(path + " requires Unicode scalar values without surrogates")
    return value


def _filesystem_runtime():
    if sys.getfilesystemencoding() != "utf-8" or sys.getfilesystemencodeerrors() != "surrogateescape":
        raise RuntimeError("live providers require utf-8 filesystem encoding with surrogateescape errors")


def _families(values):
    _exact(values, tuple, "effects")
    if not values:
        _invalid("effects", "at least one effect family is required")
    for index, value in enumerate(values):
        _exact(value, str, "effects[" + str(index) + "]")
        if value not in _FAMILIES:
            _invalid("effects", "unknown or reserved effect family")
        if value in values[:index]:
            _invalid("effects", "duplicate effect family")
    return values


def effects(*families):
    """Return an identity declaration; no wrapping, registry or metadata write."""
    _families(families)

    def declare(function):
        return function
    return declare


class _Provider:
    __slots__ = ("family", "mode", "data", "index", "root", "allowed")


class _Lease:
    __slots__ = ("active", "parent")


class _Capability:
    __slots__ = ("_provider", "_lease")
    __hash__ = None

    def __init__(self, *args, **kwargs):
        _invalid("capability", "use an ordinary named provider factory")

    def __setattr__(self, name, value):
        raise AttributeError("opaque capability attributes cannot be assigned")

    def __delattr__(self, name):
        raise AttributeError("opaque capability attributes cannot be deleted")

    def __repr__(self):
        for family, kind in _CAPABILITIES:
            if type(self) is kind:
                return family + "Capability(<opaque>)"
        return "Capability(<unsupported>)"


class IOCapability(_Capability):
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        _invalid("IOCapability", "exact capability subclasses are unsupported")

    def read_text(self, path):
        provider = _live(self, IO)
        path = _relative(path)
        _permission(provider, "read_text")
        if provider.mode == "recorded":
            for name, text in _stored_pairs(provider.data):
                if name == path:
                    return text
            raise KeyError(path)
        location = _location(provider, path)
        with open(location, "rb") as stream:
            return _standard.utf8_decode(stream.read())

    def write_text(self, path, text):
        provider = _live(self, IO)
        path = _relative(path)
        _exact(text, str, "text")
        _permission(provider, "write_text")
        if provider.mode == "recorded":
            entries = provider.data
            for index, (name, _) in enumerate(_stored_pairs(entries)):
                if name == path:
                    object.__setattr__(provider, "data", entries[:index] + ((path, text),) + entries[index + 1:])
                    return None
            object.__setattr__(provider, "data", entries + ((path, text),))
            return None
        location = _location(provider, path)
        with open(location, "wb") as stream:
            stream.write(_standard.utf8_encode(text))
        return None


class StateCapability(_Capability):
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        _invalid("StateCapability", "exact capability subclasses are unsupported")

    def get(self):
        value = _live(self, State).data
        _exact(value, int, "state value")
        return value

    def set(self, value):
        provider = _live(self, State)
        _exact(value, int, "value")
        object.__setattr__(provider, "data", value)
        return None


class ClockCapability(_Capability):
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        _invalid("ClockCapability", "exact capability subclasses are unsupported")

    def now_ns(self):
        provider = _live(self, Clock)
        if provider.mode == "recorded":
            value = _peek(provider)
            object.__setattr__(provider, "index", provider.index + 1)
            return value
        return time.time_ns()


class RandomCapability(_Capability):
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        _invalid("RandomCapability", "exact capability subclasses are unsupported")

    def below(self, bound):
        provider = _live(self, Random)
        _exact(bound, int, "bound")
        if bound <= 0:
            raise ValueError("random bound must be positive")
        if provider.mode == "recorded":
            value = _peek(provider)
            if value < 0 or value >= bound:
                raise ValueError("recorded random value is outside the requested bound")
            object.__setattr__(provider, "index", provider.index + 1)
            return value
        bits = (bound - 1).bit_length()
        if not bits:
            return 0
        width = (bits + 7) // 8
        while True:
            value = int.from_bytes(os.urandom(width)) & ((1 << bits) - 1)
            if value < bound:
                return value


class EnvironmentCapability(_Capability):
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        _invalid("EnvironmentCapability", "exact capability subclasses are unsupported")

    def get(self, name, default):
        provider = _live(self, Environment)
        name = _environment_name(name)
        _exact(default, str, "default")
        if provider.mode == "recorded":
            for key, value in _stored_pairs(provider.data):
                if key == name:
                    return value
            return default
        return os.environ.get(name, default)


class TaskCapability(_Capability):
    """Opaque owner-thread provider for the finite top-level task operations."""
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        _invalid("TaskCapability", "exact capability subclasses are unsupported")


_CAPABILITIES = ((IO, IOCapability), (State, StateCapability), (Clock, ClockCapability),
                 (Random, RandomCapability), (Environment, EnvironmentCapability), (Task, TaskCapability))


def _capability_family(kind):
    for family, admitted in _CAPABILITIES:
        if kind is admitted:
            return family
    return None


def _new(family, mode, data=None, *, root=None, allowed=()):
    provider = object.__new__(_Provider)
    for name, value in (("family", family), ("mode", mode), ("data", data), ("index", 0), ("root", root), ("allowed", allowed)):
        object.__setattr__(provider, name, value)
    kind = next(kind for name, kind in _CAPABILITIES if family == name)
    return _view(kind, provider, None)


def _view(kind, provider, lease):
    capability = object.__new__(kind)
    object.__setattr__(capability, "_provider", provider)
    object.__setattr__(capability, "_lease", lease)
    return capability


def _task_metadata(provider):
    """Check only exact private Task configuration, including revoked status."""
    data, mode, index = provider.data, provider.mode, provider.index
    if type(data) is not tuple or len(data) != 5:
        _invalid("capability", "malformed task configuration")
    workers, maximum, order, cutoff, owner = data
    if type(workers) is not int or type(maximum) is not int or type(owner) is not int:
        _invalid("capability", "malformed task configuration")
    if owner <= 0 or index not in (0, 1, 2):
        _invalid("capability", "invalid task metadata")
    if mode == "live":
        if not 1 <= workers <= 4 or not 1 <= maximum <= 256 or order is not None or cutoff is not None:
            _invalid("capability", "invalid live task configuration")
    elif mode == "controlled":
        if workers != 1 or type(order) is not tuple or len(order) > 256 or maximum != len(order):
            _invalid("capability", "invalid controlled task configuration")
        for position, value in enumerate(order):
            if type(value) is not int or not 0 <= value < len(order) or value in order[:position]:
                _invalid("capability", "invalid controlled task order")
        if cutoff is not None and (type(cutoff) is not int or not 0 <= cutoff <= len(order)):
            _invalid("capability", "invalid controlled task cutoff")
    else:
        _invalid("capability", "invalid task provider mode")
    return owner


def _task_owner(provider):
    if _task_metadata(provider) != _thread.get_ident():
        raise RuntimeError("tasks: provider belongs to a different thread")


def _live(capability, family=None):
    actual = _capability_family(type(capability))
    if actual is None or family is not None and actual != family:
        _invalid("capability", "expected the exact corresponding capability interface")
    try:
        provider = object.__getattribute__(capability, "_provider")
        lease = object.__getattribute__(capability, "_lease")
    except AttributeError:
        _invalid("capability", "malformed capability storage")
    if type(provider) is not _Provider:
        _invalid("capability", "malformed provider storage")
    try:
        mode, stored_family, index = provider.mode, provider.family, provider.index
        data, root, allowed = provider.data, provider.root, provider.allowed
    except AttributeError:
        _invalid("capability", "incomplete provider storage")
    _exact(stored_family, str, "provider family")
    _exact(mode, str, "provider mode")
    _exact(index, int, "provider index")
    if stored_family != actual or index < 0 or mode not in (("cell",) if actual == State else ("live", "controlled") if actual == Task else ("live", "recorded")):
        _invalid("capability", "invalid provider metadata")
    if actual == Task:
        _task_metadata(provider)
    elif actual == State:
        _exact(data, int, "state value")
    elif mode == "recorded":
        _exact(data, tuple, "recorded provider data")
    elif data is not None:
        _invalid("capability", "unexpected live provider data")
    if actual == IO:
        _allowed(allowed)
        if mode == "live":
            _scalar_text(root, "IO root")
    elif type(allowed) is not tuple or allowed or root is not None:
        _invalid("capability", "unexpected provider metadata")
    visited = ()
    while lease is not None:
        if type(lease) is not _Lease:
            _invalid("capability", "malformed lease storage")
        if any(lease is previous for previous in visited):
            _invalid("capability", "cyclic lease storage")
        visited += (lease,)
        try:
            active, parent = lease.active, lease.parent
        except AttributeError:
            _invalid("capability", "incomplete lease storage")
        if active is not True:
            raise RuntimeError("borrowed capability view is closed")
        lease = parent
    if actual == Task:
        _task_owner(provider)
        if index == 1:
            raise RuntimeError("tasks: provider already has an active call")
        if index == 2:
            raise RuntimeError("tasks: provider is permanently revoked")
    return provider


class _Borrow:
    __slots__ = ("_capability", "_lease", "_status")

    def __setattr__(self, name, value):
        raise AttributeError("borrow metadata cannot be assigned")

    def __delattr__(self, name):
        raise AttributeError("borrow metadata cannot be deleted")

    def __init_subclass__(cls, **kwargs):
        _invalid("borrow", "borrow context subclasses are unsupported")

    def __enter__(self):
        if _context_status(self) != "fresh":
            raise RuntimeError("borrow context is single-use")
        provider = _live(self._capability)
        lease = object.__new__(_Lease)
        object.__setattr__(lease, "active", True)
        object.__setattr__(lease, "parent", object.__getattribute__(self._capability, "_lease"))
        object.__setattr__(self, "_lease", lease)
        object.__setattr__(self, "_status", "entered")
        return _view(type(self._capability), provider, lease)

    def __exit__(self, exception_type, exception, traceback):
        if _context_status(self) != "entered":
            raise RuntimeError("borrow context has no active entry")
        if type(self._lease) is not _Lease:
            _invalid("borrow", "malformed context lease")
        if type(self._capability) is TaskCapability:
            # Body/coordinator failure may revoke the provider. Exit checks
            # ownership without requiring idle/nonrevoked status, preserving it.
            _task_owner(object.__getattribute__(self._capability, "_provider"))
        object.__setattr__(self._lease, "active", False)
        object.__setattr__(self, "_status", "closed")
        return False


def _context_status(context):
    if type(context) is not _Borrow:
        _invalid("borrow", "expected exact borrow context")
    try:
        status = context._status
    except AttributeError:
        _invalid("borrow", "incomplete context storage")
    _exact(status, str, "borrow status")
    if status not in ("fresh", "entered", "closed"):
        _invalid("borrow", "invalid context status")
    return status


def borrow(capability):
    """Single-use logical lease. Exit invalidates its view and dependent views."""
    _live(capability)
    context = object.__new__(_Borrow)
    object.__setattr__(context, "_capability", capability)
    object.__setattr__(context, "_lease", None)
    object.__setattr__(context, "_status", "fresh")
    return context


def _peek(provider):
    if provider.index >= len(provider.data):
        raise IndexError("recorded provider is exhausted")
    value = provider.data[provider.index]
    _exact(value, int, "recorded provider value")
    return value


def _integers(values, path):
    _exact(values, tuple, path)
    for index, value in enumerate(values):
        _exact(value, int, path + "[" + str(index) + "]")
    return values


def _environment_name(name):
    _scalar_text(name, "name")
    if not name or "=" in name or "\x00" in name:
        raise ValueError("environment name must be nonempty without '=' or NUL")
    return name


def _relative(path):
    _scalar_text(path, "path")
    if not path or "\x00" in path or "\\" in path or any(part in {"", ".", ".."} for part in path.split("/")):
        raise ValueError("path must contain nonempty relative components without dot/dotdot, backslash or NUL")
    return path


def _pairs(entries, path, names):
    _exact(entries, tuple, path)
    output = []
    for index, pair in enumerate(entries):
        if type(pair) is not tuple or len(pair) != 2:
            _invalid(path + "[" + str(index) + "]", "expected an exact name/value pair tuple")
        key, value = pair
        key = names(key)
        _exact(value, str, path + ".value")
        if any(key == existing for existing, _ in output):
            raise ValueError("recorded provider names must be unique")
        output.append((key, value))
    return tuple(output)


def _stored_pairs(entries):
    for pair in entries:
        if type(pair) is not tuple or len(pair) != 2:
            _invalid("recorded provider", "malformed name/value pair")
        name, value = pair
        _exact(name, str, "recorded provider name")
        _exact(value, str, "recorded provider value")
        yield name, value


def _allowed(allowed):
    _exact(allowed, tuple, "allowed_ops")
    if not allowed:
        raise ValueError("allowed_ops must explicitly allow at least one IO operation")
    for index, operation in enumerate(allowed):
        _exact(operation, str, "allowed_ops[" + str(index) + "]")
        if operation not in ("read_text", "write_text") or operation in allowed[:index]:
            raise ValueError("allowed_ops requires unique read_text/write_text operation names")
    return allowed


def _permission(provider, operation):
    if operation not in provider.allowed:
        raise PermissionError("IO operation is outside provider allowed_ops")


def _location(provider, relative):
    current = provider.root
    for part in relative.split("/"):
        current = os.path.join(current, part)
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(metadata.st_mode):
            raise PermissionError("symlink path components are outside the IO provider contract")
    return current


def live_io(root, *, allowed_ops):
    """Rooted whole-file UTF-8 operations; symlink/TOCTOU limits are explicit."""
    _scalar_text(root, "root")
    _filesystem_runtime()
    allowed = _allowed(allowed_ops)
    if not root or "\x00" in root:
        raise ValueError("root must be a nonempty filesystem path without NUL")
    canonical = os.path.realpath(root)
    _scalar_text(canonical, "canonical root")
    if not os.path.isdir(canonical):
        raise NotADirectoryError("IO root must name an existing directory")
    return _new(IO, "live", root=canonical, allowed=allowed)


def recorded_io(entries, *, allowed_ops):
    return _new(IO, "recorded", _pairs(entries, "entries", _relative), allowed=_allowed(allowed_ops))


def state(initial):
    _exact(initial, int, "initial")
    return _new(State, "cell", initial)


def live_clock():
    return _new(Clock, "live")


def recorded_clock(values):
    return _new(Clock, "recorded", _integers(values, "values"))


def live_random():
    return _new(Random, "live")


def recorded_random(values):
    return _new(Random, "recorded", _integers(values, "values"))


def live_environment():
    _filesystem_runtime()
    return _new(Environment, "live")


def recorded_environment(entries):
    return _new(Environment, "recorded", _pairs(entries, "entries", _environment_name))


def _annotation(annotation, families, *, parameter=False):
    family = _capability_family(annotation)
    if family is not None:
        if not parameter or family not in families:
            _invalid("Effectful", "capability parameter requires its corresponding effect family; capabilities cannot be results")
        return
    if type(annotation) is GenericAlias and object.__getattribute__(annotation, "__origin__") is Effectful:
        arguments = object.__getattribute__(annotation, "__args__")
        _effectful_arguments(arguments)
        return
    if type(annotation) is typing._CallableGenericAlias or type(annotation) is collections.abc._CallableGenericAlias:
        origin = object.__getattribute__(annotation, "__origin__")
        arguments = object.__getattribute__(annotation, "__args__")
        if origin is not collections.abc.Callable or type(arguments) is not tuple or not arguments or any(value is Ellipsis for value in arguments):
            _invalid("Effectful", "Callable requires a fixed positional schema")
        for child in arguments:
            _annotation(child, (), parameter=False)
        return
    _records._annotation_schema(annotation)


def _effectful_arguments(arguments):
    if type(arguments) is not tuple or len(arguments) < 3 or type(arguments[0]) is not tuple:
        _invalid("Effectful", "expected fixed parameters, result and at least one effect family")
    families = _families(arguments[2:])
    for parameter in arguments[0]:
        _annotation(parameter, families, parameter=True)
    _annotation(arguments[1], families)


class Effectful:
    """Finite runtime annotation; actual callable purity/effects need evidence."""
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        _invalid("Effectful", "annotation-only class")

    def __init_subclass__(cls, **kwargs):
        _invalid("Effectful", "annotation subclasses are unsupported")

    @classmethod
    def __class_getitem__(cls, arguments):
        if cls is not Effectful or type(arguments) is not tuple or len(arguments) < 3 or type(arguments[0]) is not list:
            _invalid("Effectful", "use Effectful[[fixed parameter types], result, family, ...]")
        canonical = (tuple(arguments[0]), *arguments[1:])
        _effectful_arguments(canonical)
        return GenericAlias(cls, canonical)
