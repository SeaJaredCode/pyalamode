"""Closed compile-only UTF-8 source provenance; no source execution or file I/O."""

import ast
import bisect
import hashlib
import heapq
import io
import json
import keyword
import math
import tokenize
import types
import typing
import unicodedata
from dataclasses import dataclass

EDITION = "pyalamode-v1-experimental"
TRANSLATOR_VERSION = "pyalamode.syntax-v1"
MAP_SCHEMA = 1
MAP_KIND = "pyalamode-source-map"
COORDINATES = "utf-8-bytes"
MAX_AUTHORED_BYTES = 1048576
MAX_GENERATED_BYTES = 8388608
MAX_TOKENS = 100000
MAX_AST_NODES = 100000
MAX_AST_DEPTH = 256
MAX_SEGMENTS = 200000
MAX_MAP_BYTES = 33554432
MAX_FIELD_BYTES = 8388608
MAX_FIELD_ITEMS = 400000
MAX_INTEGER_BITS = 8388608
MAX_ORIGINS = 100001
MAX_PATH_ELEMENTS = 512


class SourceMapError(ValueError):
    """Malformed compile input or provenance; never semantic source evidence."""


@dataclass(frozen=True, slots=True)
class ByteSpan:
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class SourceOwner:
    authored_path: str
    runtime_path: str
    module: str


@dataclass(frozen=True, slots=True)
class TranslatorIdentity:
    version: str
    files: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class SourceIdentity:
    path: str
    edition: str
    role: str
    sha256: str
    byte_count: int


@dataclass(frozen=True, slots=True)
class MapSegment:
    generated_start: int
    generated_end: int
    source_start: int
    source_end: int
    kind: str


@dataclass(frozen=True, slots=True)
class SourceMap:
    owner: SourceOwner
    translator: TranslatorIdentity
    source: SourceIdentity
    generated: SourceIdentity
    segments: tuple[MapSegment, ...]


@dataclass(frozen=True, slots=True)
class SourcePosition:
    line: int
    column: int
    byte_offset: int
    utf16_column: int


@dataclass(frozen=True, slots=True)
class MappedRange:
    source_span: ByteSpan
    exact: bool
    segments: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class NodeOrigin:
    span: ByteSpan
    kind: str


@dataclass(frozen=True, slots=True)
class AstDerivation:
    generated_bytes: bytes
    source_map: SourceMap
    node_count: int


def _fail(reason):
    raise SourceMapError(reason)


def _integer(value, minimum=0, maximum=MAX_GENERATED_BYTES):
    if type(value) is not int or not minimum <= value <= maximum:
        _fail("expected bounded exact integer")
    return value


def _text(value, maximum=4096):
    if type(value) is not str:
        _fail("expected exact text")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        _fail("text is not UTF-8")
    if size > maximum:
        _fail("text exceeds bound")
    return value


def _bytes(value, maximum=MAX_GENERATED_BYTES):
    if type(value) is not bytes or len(value) > maximum:
        _fail("expected bounded exact bytes")
    return value


def _digest(value):
    if type(value) is not str or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        _fail("expected lowercase SHA256")
    return value


def _path(value):
    _text(value)
    if (not value or value.startswith("/") or ":" in value or "\\" in value
            or any(ord(c) < 32 or ord(c) == 127 for c in value)
            or any(part in {"", ".", ".."} for part in value.split("/"))
            or not value.endswith((".py", ".pya"))):
        _fail("expected closed relative Python source path")
    return value


def _owner(value):
    if type(value) is not SourceOwner:
        _fail("expected exact SourceOwner")
    _path(value.authored_path)
    _path(value.runtime_path)
    expected = value.authored_path[:-4] + ".py" if value.authored_path.endswith(".pya") else value.authored_path
    if value.runtime_path != expected:
        _fail("runtime path must retain authored stem")
    _text(value.module)
    if (not value.module or unicodedata.normalize("NFKC", value.module) != value.module
            or any(not part.isidentifier() or keyword.iskeyword(part) for part in value.module.split("."))):
        _fail("expected explicit canonical importable module")
    return value


def _translator(value):
    if type(value) is not TranslatorIdentity:
        _fail("expected exact translator identity")
    _text(value.version)
    if value.version != TRANSLATOR_VERSION or type(value.files) is not tuple:
        _fail("expected exact translator identity")
    if len(value.files) != 2:
        _fail("translator requires exactly two source bodies")
    for row, name in zip(value.files, ("source_maps.py", "syntax.py")):
        if type(row) is not tuple or len(row) != 2:
            _fail("translator file names/order are closed")
        _text(row[0])
        if row[0] != name:
            _fail("translator file names/order are closed")
        _digest(row[1])
    return value


def _identity(value):
    if type(value) is not SourceIdentity:
        _fail("expected exact source identity")
    _path(value.path)
    _text(value.role)
    _text(value.edition)
    if value.role not in {"authored", "scaffold", "lowered", "debug", "facade", "formatted"}:
        _fail("unknown source role")
    if value.edition not in {"python-v1", EDITION}:
        _fail("unknown source edition")
    expected = EDITION if value.path.endswith(".pya") else "python-v1"
    if value.edition != expected or value.role not in {"authored", "formatted"} and value.path.endswith(".pya"):
        _fail("role/path/edition mismatch")
    _digest(value.sha256)
    _integer(value.byte_count, maximum=MAX_AUTHORED_BYTES if value.role == "authored" else MAX_GENERATED_BYTES)
    return value


def _roles(value):
    _owner(value.owner)
    _translator(value.translator)
    _identity(value.source)
    _identity(value.generated)
    pairs = {("authored", role) for role in ("scaffold", "lowered", "debug", "facade", "formatted")}
    pairs.update({("scaffold", "lowered"), ("lowered", "debug"), ("lowered", "facade")})
    if (value.source.role, value.generated.role) not in pairs:
        _fail("unsupported source/generated role pair")
    for identity in (value.source, value.generated):
        if identity.role in {"authored", "formatted"} and identity.path != value.owner.authored_path:
            _fail("authored path does not match owner")
        if identity.role in {"scaffold", "lowered"} and identity.path != value.owner.runtime_path:
            _fail("runtime path does not match owner")


class _Geometry:
    def __init__(self, raw):
        _bytes(raw)
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise SourceMapError("source is not strict UTF-8") from error
        self.raw = raw
        self.bom = 3 if raw.startswith(b"\xef\xbb\xbf") else 0
        self.starts = [self.bom]
        self.ends = []
        self.boundaries = {0, self.bom}
        offset = self.bom
        for char in raw[self.bom:].decode("utf-8"):
            offset += len(char.encode("utf-8"))
            self.boundaries.add(offset)
        i = self.bom
        while i < len(raw):
            if raw[i] in (10, 13):
                self.ends.append(i)
                if raw[i] == 13 and i + 1 < len(raw) and raw[i + 1] == 10:
                    self.boundaries.discard(i + 1)
                    i += 2
                else:
                    i += 1
                self.starts.append(i)
            else:
                i += 1
        self.ends.append(len(raw))

    def offset(self, offset):
        _integer(offset, maximum=len(self.raw))
        if offset not in self.boundaries:
            _fail("coordinate is inside a scalar, BOM or CRLF")
        return offset

    def span(self, value):
        if type(value) is not ByteSpan:
            _fail("expected exact ByteSpan")
        self.offset(value.start)
        self.offset(value.end)
        if value.start > value.end:
            _fail("reversed byte range")
        return value

    def position(self, offset):
        self.offset(offset)
        if offset == 0 and self.bom:
            return SourcePosition(1, 1, 0, 0)
        row = bisect.bisect_right(self.starts, offset) - 1
        start = self.starts[row]
        if offset > self.ends[row]:
            _fail("coordinate is inside a line terminator")
        prefix = self.raw[start:offset].decode("utf-8")
        return SourcePosition(row + 1, offset - start + 1, offset, len(prefix.encode("utf-16-le")) // 2)

    def at(self, line, column, encoding):
        _integer(line, minimum=1, maximum=len(self.starts))
        start, end = self.starts[line - 1], self.ends[line - 1]
        if encoding == "utf-8-bytes":
            _integer(column, minimum=1, maximum=end - start + 1)
            return self.offset(start + column - 1)
        if encoding != "utf-16":
            _fail("unknown coordinate encoding")
        _integer(column, maximum=2 * (end - start))
        offset, units = start, 0
        for char in self.raw[start:end].decode("utf-8"):
            if units == column:
                return offset
            units += 2 if ord(char) > 65535 else 1
            offset += len(char.encode("utf-8"))
        if units == column:
            return end
        _fail("coordinate is inside a surrogate or outside line")


def source_identity(raw, *, path, edition, role):
    _path(path)
    _text(edition)
    _text(role)
    _bytes(raw, MAX_AUTHORED_BYTES if role == "authored" else MAX_GENERATED_BYTES)
    _Geometry(raw)
    return _identity(SourceIdentity(path, edition, role, hashlib.sha256(raw).hexdigest(), len(raw)))


def position_at(raw, offset):
    return _Geometry(raw).position(offset)


def offset_at(raw, line, column, *, encoding=COORDINATES):
    _text(encoding)
    return _Geometry(raw).at(line, column, encoding)


def _shape(value):
    if type(value) is not SourceMap:
        _fail("expected exact SourceMap")
    _roles(value)
    if type(value.segments) is not tuple or len(value.segments) > MAX_SEGMENTS:
        _fail("segment count/type exceeds profile")
    end = 0
    for segment in value.segments:
        if type(segment) is not MapSegment:
            _fail("expected exact closed segment")
        _text(segment.kind)
        if segment.kind not in {"copy", "anchor"}:
            _fail("expected exact closed segment")
        for item in (segment.generated_start, segment.generated_end):
            _integer(item, maximum=value.generated.byte_count)
        for item in (segment.source_start, segment.source_end):
            _integer(item, maximum=value.source.byte_count)
        if segment.generated_start != end or segment.generated_end <= end or segment.source_end < segment.source_start:
            _fail("segment coverage or range is invalid")
        if segment.kind == "copy" and segment.generated_end - segment.generated_start != segment.source_end - segment.source_start:
            _fail("copy lengths differ")
        end = segment.generated_end
    if end != value.generated.byte_count:
        _fail("generated coverage is incomplete")
    return value


def _validated(value, source, generated):
    _shape(value)
    sg, gg = _Geometry(source), _Geometry(generated)
    if (len(source) != value.source.byte_count or hashlib.sha256(source).hexdigest() != value.source.sha256
            or len(generated) != value.generated.byte_count or hashlib.sha256(generated).hexdigest() != value.generated.sha256):
        _fail("actual bytes differ from descriptors")
    for segment in value.segments:
        sg.span(ByteSpan(segment.source_start, segment.source_end))
        gg.span(ByteSpan(segment.generated_start, segment.generated_end))
        if segment.kind == "copy" and source[segment.source_start:segment.source_end] != generated[segment.generated_start:segment.generated_end]:
            _fail("copy bytes differ")
    return value


def identity_map(raw, *, owner, translator, source, generated):
    _bytes(raw)
    value = SourceMap(owner, translator, source, generated,
                      (MapSegment(0, len(raw), 0, len(raw), "copy"),) if raw else ())
    return _validated(value, raw, raw)


def _keys(value, keys):
    if type(value) is not dict or len(value) != len(keys) or any(type(key) is not str for key in value) or set(value) != set(keys):
        _fail("wire object has nonclosed keys/types")
    return value


def map_to_dict(value):
    _shape(value)
    # Every closed segment has five fixed keys, four integers of at most seven
    # digits and copy/anchor. 160 bytes is a conservative compact-JSON bound.
    # The fixed header's bounded paths/module/identities need at most 96KiB,
    # including UTF8 and escaping. Check before detachment or serialization.
    if 160 * len(value.segments) + 98304 > MAX_MAP_BYTES:
        _fail("bounded serialized map size exceeds profile")
    def identity(item):
        return {name: getattr(item, name) for name in ("path", "edition", "role", "sha256", "byte_count")}
    wire = {"schema": MAP_SCHEMA, "kind": MAP_KIND,
            "owner": {name: getattr(value.owner, name) for name in ("authored_path", "runtime_path", "module")},
            "translator": {"version": value.translator.version, "files": dict(value.translator.files)},
            "source": identity(value.source), "generated": identity(value.generated),
            "coordinate_encoding": COORDINATES,
            "segments": [{name: getattr(segment, name) for name in ("generated_start", "generated_end", "source_start", "source_end", "kind")}
                         for segment in value.segments]}
    if len(json.dumps(wire, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")) + 1 > MAX_MAP_BYTES:
        _fail("serialized map exceeds bound")
    return wire


def validate_map(value, *, source, generated, owner, translator, source_identity, generated_identity):
    _keys(value, ("schema", "kind", "owner", "translator", "source", "generated", "coordinate_encoding", "segments"))
    _text(value["kind"])
    _text(value["coordinate_encoding"])
    if type(value["schema"]) is not int or value["schema"] != MAP_SCHEMA or value["kind"] != MAP_KIND or value["coordinate_encoding"] != COORDINATES:
        _fail("unknown map schema/kind/coordinates")
    o = _keys(value["owner"], ("authored_path", "runtime_path", "module"))
    t = _keys(value["translator"], ("version", "files"))
    files = _keys(t["files"], ("source_maps.py", "syntax.py"))
    def identity(row):
        _keys(row, ("path", "edition", "role", "sha256", "byte_count"))
        return SourceIdentity(**row)
    rows = value["segments"]
    if type(rows) is not list or len(rows) > MAX_SEGMENTS:
        _fail("wire segment list exceeds bound")
    segments = []
    for row in rows:
        _keys(row, ("generated_start", "generated_end", "source_start", "source_end", "kind"))
        segments.append(MapSegment(**row))
    parsed = SourceMap(SourceOwner(**o), TranslatorIdentity(t["version"], tuple((name, files[name]) for name in ("source_maps.py", "syntax.py"))),
                       identity(value["source"]), identity(value["generated"]), tuple(segments))
    _owner(owner)
    _translator(translator)
    _identity(source_identity)
    _identity(generated_identity)
    _shape(parsed)
    if (parsed.owner != owner or parsed.translator != translator or parsed.source != source_identity or parsed.generated != generated_identity):
        _fail("map differs from independently owned identities")
    _validated(parsed, source, generated)
    map_to_dict(parsed)
    return parsed


def _point(value, point, starts=None):
    if point == value.generated.byte_count:
        last = value.segments[-1] if value.segments else None
        exact = (not last and not value.source.byte_count or last is not None and last.kind == "copy" and last.source_end == value.source.byte_count)
        return MappedRange(ByteSpan(value.source.byte_count, value.source.byte_count), bool(exact), ())
    if starts is None:
        starts = [s.generated_start for s in value.segments]
    index = bisect.bisect_right(starts, point) - 1
    segment = value.segments[index]
    if segment.kind == "anchor":
        return MappedRange(ByteSpan(segment.source_start, segment.source_end), False, (index,))
    offset = segment.source_start + point - segment.generated_start
    return MappedRange(ByteSpan(offset, offset), True, (index,))


def map_range(value, span, *, source, generated):
    _validated(value, source, generated)
    _Geometry(generated).span(span)
    if span.start == span.end:
        return _point(value, span.start)
    starts = [s.generated_start for s in value.segments]
    index = bisect.bisect_right(starts, span.start) - 1
    contributions, indices = [], []
    while index < len(value.segments):
        segment = value.segments[index]
        if segment.generated_start >= span.end:
            break
        lo, hi = max(span.start, segment.generated_start), min(span.end, segment.generated_end)
        if lo < hi:
            if segment.kind == "copy":
                a = segment.source_start + lo - segment.generated_start
                z = segment.source_start + hi - segment.generated_start
            else:
                a, z = segment.source_start, segment.source_end
            contributions.append((a, z, segment.kind))
            indices.append(index)
        index += 1
    lo = min(row[0] for row in contributions)
    hi = max(row[1] for row in contributions)
    exact = (all(row[2] == "copy" for row in contributions)
             and all(a[1] == b[0] for a, b in zip(contributions, contributions[1:]))
             and hi - lo == span.end - span.start)
    return MappedRange(ByteSpan(lo, hi), exact, tuple(indices))


def generated_ranges(value, span, *, source, generated):
    _validated(value, source, generated)
    _Geometry(source).span(span)
    result = []
    for segment in value.segments:
        if span.start == span.end:
            point = span.start
            if segment.kind == "copy" and segment.source_start <= point < segment.source_end:
                g = segment.generated_start + point - segment.source_start
                result.append(ByteSpan(g, g))
            elif segment.kind == "anchor" and (segment.source_start <= point < segment.source_end or segment.source_start == segment.source_end == point):
                result.append(ByteSpan(segment.generated_start, segment.generated_end))
        else:
            lo, hi = max(span.start, segment.source_start), min(span.end, segment.source_end)
            if lo < hi:
                if segment.kind == "copy":
                    result.append(ByteSpan(segment.generated_start + lo - segment.source_start,
                                           segment.generated_start + hi - segment.source_start))
                else:
                    result.append(ByteSpan(segment.generated_start, segment.generated_end))
    if span.start == span.end == value.source.byte_count:
        result.append(ByteSpan(value.generated.byte_count, value.generated.byte_count))
    result.sort(key=lambda row: (row.start, row.end))
    merged = []
    for row in result:
        if merged and row.start <= merged[-1].end:
            merged[-1] = ByteSpan(merged[-1].start, max(merged[-1].end, row.end))
        else:
            merged.append(row)
    return tuple(merged)


def _append(rows, item):
    if rows:
        old = rows[-1]
        if old.generated_end == item.generated_start and old.kind == item.kind:
            if old.kind == "copy" and old.source_end == item.source_start:
                rows[-1] = MapSegment(old.generated_start, item.generated_end, old.source_start, item.source_end, "copy")
                return
            if old.kind == "anchor" and (old.source_start, old.source_end) == (item.source_start, item.source_end):
                rows[-1] = MapSegment(old.generated_start, item.generated_end, old.source_start, old.source_end, "anchor")
                return
    if len(rows) >= MAX_SEGMENTS:
        _fail("generated segment count exceeds bound")
    rows.append(item)


class _HullIndex:
    def __init__(self, value):
        self.value = value
        self.starts = [row.generated_start for row in value.segments]
        self.size = 1
        while self.size < len(value.segments):
            self.size *= 2
        self.low = [MAX_GENERATED_BYTES + 1] * (2 * self.size)
        self.high = [-1] * (2 * self.size)
        for i, row in enumerate(value.segments):
            self.low[self.size + i], self.high[self.size + i] = row.source_start, row.source_end
        for i in range(self.size - 1, 0, -1):
            self.low[i] = min(self.low[2 * i], self.low[2 * i + 1])
            self.high[i] = max(self.high[2 * i], self.high[2 * i + 1])

    def middle(self, left, right):
        lo, hi = MAX_GENERATED_BYTES + 1, -1
        left, right = left + self.size, right + self.size
        while left < right:
            if left % 2:
                lo, hi = min(lo, self.low[left]), max(hi, self.high[left])
                left += 1
            if right % 2:
                right -= 1
                lo, hi = min(lo, self.low[right]), max(hi, self.high[right])
            left //= 2
            right //= 2
        return lo, hi

    def hull(self, start, end):
        if start == end:
            return _point(self.value, start, self.starts).source_span
        first = bisect.bisect_right(self.starts, start) - 1
        last = bisect.bisect_left(self.starts, end) - 1
        pieces = []
        for i in {first, last}:
            row = self.value.segments[i]
            if row.kind == "copy":
                pieces.append((row.source_start + max(start, row.generated_start) - row.generated_start,
                               row.source_start + min(end, row.generated_end) - row.generated_start))
            else:
                pieces.append((row.source_start, row.source_end))
        if first + 1 < last:
            pieces.append(self.middle(first + 1, last))
        return ByteSpan(min(p[0] for p in pieces), max(p[1] for p in pieces))


def compose_maps(inner, outer, *, source, intermediate, generated):
    _validated(inner, source, intermediate)
    _validated(outer, intermediate, generated)
    if inner.owner != outer.owner or inner.translator != outer.translator or inner.generated != outer.source:
        _fail("composition requires identical actual intermediate ownership/identity")
    index = _HullIndex(inner)
    result = []
    for row in outer.segments:
        if row.kind == "anchor":
            span = index.hull(row.source_start, row.source_end)
            _append(result, MapSegment(row.generated_start, row.generated_end, span.start, span.end, "anchor"))
            continue
        i = bisect.bisect_right(index.starts, row.source_start) - 1
        point = row.source_start
        while point < row.source_end:
            prior = inner.segments[i]
            stop = min(row.source_end, prior.generated_end)
            gstart = row.generated_start + point - row.source_start
            gend = row.generated_start + stop - row.source_start
            if prior.kind == "copy":
                a = prior.source_start + point - prior.generated_start
                z = prior.source_start + stop - prior.generated_start
            else:
                a, z = prior.source_start, prior.source_end
            _append(result, MapSegment(gstart, gend, a, z, prior.kind))
            point, i = stop, i + 1
    value = SourceMap(inner.owner, inner.translator, inner.source, outer.generated, tuple(result))
    return _validated(value, source, generated)


_NODE_NAMES = """Module FunctionDef ClassDef Return Assign AnnAssign If With Match Try Assert Import ImportFrom Expr Pass
BoolOp BinOp UnaryOp IfExp Compare Call Constant Attribute Subscript Name List Tuple Slice ExceptHandler arguments arg keyword alias withitem match_case
MatchValue MatchSingleton MatchSequence MatchMapping MatchClass MatchStar MatchAs MatchOr Load Store
And Or Add Sub Mult MatMult Div Mod Pow LShift RShift BitOr BitXor BitAnd FloorDiv Invert Not UAdd USub
Eq NotEq Lt LtE Gt GtE Is IsNot In NotIn""".split()
_NODE_TYPES = frozenset(getattr(ast, name) for name in _NODE_NAMES)


def _field_shape(value, expected):
    origin = typing.get_origin(expected)
    if origin in {types.UnionType, typing.Union}:
        return any(_field_shape(value, choice) for choice in typing.get_args(expected))
    if origin is list:
        if type(value) is not list or len(value) > MAX_FIELD_ITEMS:
            return False
        child = typing.get_args(expected)[0]
        return all(_field_shape(item, child) for item in value)
    if expected is object:
        return value is None or value is Ellipsis or type(value) in {str, bytes, int, bool, float, complex}
    if expected is type(None):
        return value is None
    if expected in {str, int, bool, bytes}:
        return type(value) is expected
    if type(expected) is type and issubclass(expected, ast.AST):
        return type(value) in _NODE_TYPES and isinstance(value, expected)
    return False


def _ast_nodes(tree):
    if type(tree) is not ast.Module:
        _fail("derivation requires exact Module")
    stack = [(tree, (), 0, ())]
    nodes, field_bytes, field_items, integer_bits = [], 0, 0, 0
    while stack:
        node, path, depth, ancestors = stack.pop()
        if type(node) not in _NODE_TYPES or depth > MAX_AST_DEPTH or id(node) in ancestors:
            _fail("unsupported AST class/depth/cycle")
        nodes.append((path, node, depth))
        if len(nodes) > MAX_AST_NODES:
            _fail("AST node count exceeds bound")
        for name, item in vars(node).items():
            if name not in node._fields and name not in node._attributes:
                if not name.startswith("_pyalamode_") or type(item) is not NodeOrigin:
                    _fail("unknown AST field/provenance")
        for name in node._attributes:
            if hasattr(node, name):
                item = getattr(node, name)
                if item is None and name in {"end_lineno", "end_col_offset"}:
                    continue
                _integer(item, minimum=1 if name in {"lineno", "end_lineno"} else 0)
        if hasattr(node, "lineno") != hasattr(node, "col_offset"):
            _fail("incomplete stock start location")
        if getattr(node, "end_lineno", None) is not None and getattr(node, "end_col_offset", None) is None:
            _fail("incomplete stock end location")
        for name in node._fields:
            if not hasattr(node, name):
                _fail("missing stock AST field")
            value = getattr(node, name)
            if name not in type(node)._field_types or not _field_shape(value, type(node)._field_types[name]):
                _fail("malformed finite stock AST field layout")
            values = value if type(value) is list else [value]
            field_items += 1 + len(values)
            if field_items > MAX_FIELD_ITEMS:
                _fail("AST field item count exceeds bound")
            for i, item in enumerate(values):
                childpath = path + (name, i) if type(value) is list else path + (name,)
                if type(item) in _NODE_TYPES:
                    stack.append((item, childpath, depth + 1, ancestors + (id(node),)))
                elif isinstance(item, ast.AST):
                    _fail("foreign or unsupported AST node")
                elif type(item) in {str, bytes}:
                    try:
                        field_bytes += len(item.encode("utf-8") if type(item) is str else item)
                    except UnicodeEncodeError as error:
                        raise SourceMapError("AST text is not UTF-8") from error
                elif type(item) is int:
                    integer_bits += item.bit_length()
                elif item is None or item is Ellipsis or type(item) is bool:
                    pass
                elif type(item) is float and math.isfinite(item):
                    pass
                elif type(item) is complex and math.isfinite(item.real) and math.isfinite(item.imag):
                    pass
                else:
                    _fail("foreign or unsupported AST field payload")
                if field_bytes > MAX_FIELD_BYTES or integer_bits > MAX_INTEGER_BITS:
                    _fail("AST plain-field magnitude exceeds bound")
    return nodes


def _node_span(node, geometry):
    if type(node) is ast.Module:
        return ByteSpan(0, len(geometry.raw))
    if not hasattr(node, "lineno") or not hasattr(node, "end_lineno") or node.end_lineno is None:
        return None
    return ByteSpan(geometry.at(node.lineno, node.col_offset + 1, COORDINATES),
                    geometry.at(node.end_lineno, node.end_col_offset + 1, COORDINATES))


def _field_equal(a, b):
    pending = [(a, b)]
    while pending:
        left, right = pending.pop()
        if type(left) is not type(right):
            return False
        if type(left) in _NODE_TYPES:
            pending.extend((getattr(left, field), getattr(right, field)) for field in left._fields)
        elif type(left) is list:
            if len(left) != len(right):
                return False
            pending.extend(zip(left, right))
        elif left != right:
            return False
    return True


def _token_bound(raw):
    text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    count = 0
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            count += 1
            if count > MAX_TOKENS:
                _fail("generated token count exceeds profile before stock reparse")
    except (tokenize.TokenError, IndentationError, SyntaxError) as error:
        raise SourceMapError("stock unparse produced malformed tokens") from error


def derive_ast(source, tree, origins, *, owner, translator, source_identity, generated_path, generated_role):
    _bytes(source)
    geometry = _Geometry(source)
    _owner(owner)
    _translator(translator)
    _identity(source_identity)
    if len(source) != source_identity.byte_count or hashlib.sha256(source).hexdigest() != source_identity.sha256:
        _fail("derivation source identity is stale")
    _text(generated_role)
    if generated_role not in {"debug", "facade"}:
        _fail("derivation generated role must be debug/facade")
    _path(generated_path)
    if type(origins) is not dict or len(origins) > MAX_ORIGINS:
        _fail("origin table exceeds profile")
    nodes = _ast_nodes(tree)
    actual = {path: node for path, node, depth in nodes}
    for path, origin in origins.items():
        if type(path) is not tuple or len(path) > MAX_PATH_ELEMENTS:
            _fail("invalid origin path")
        if any(type(part) not in {str, int} or type(part) is int and part < 0 for part in path) or path not in actual:
            _fail("origin path is not an actual AST node")
        if type(origin) is not NodeOrigin:
            _fail("invalid exact NodeOrigin")
        _text(origin.kind)
        if origin.kind not in {"copy", "anchor"}:
            _fail("invalid exact NodeOrigin")
        geometry.span(origin.span)
        if origin.kind == "copy":
            span = _node_span(actual[path], geometry)
            if span is not None and span != origin.span:
                _fail("copy origin differs from actual source node position")
    inherited = {}
    for path, node, depth in sorted(nodes, key=lambda item: len(item[0])):
        positioned = isinstance(node, (ast.stmt, ast.expr, ast.arg, ast.alias, ast.keyword, ast.ExceptHandler, ast.pattern)) or type(node) is ast.Module
        if positioned and path not in origins:
            _fail("missing explicit positioned-node origin")
        if path in origins:
            inherited[path] = origins[path]
        else:
            parent = path[:-1] if type(path[-1]) is str else path[:-2]
            if parent not in inherited:
                _fail("missing containing origin")
            inherited[path] = inherited[parent]
    try:
        text = ast.unparse(tree) + "\n"
        generated = text.encode("utf-8")
    except (ValueError, TypeError, AttributeError, AssertionError, IndexError, RecursionError, UnicodeEncodeError) as error:
        raise SourceMapError("stock unparse refused bounded AST") from error
    _bytes(generated)
    _token_bound(generated)
    try:
        reparsed = ast.parse(text, feature_version=(3, 13))
    except (SyntaxError, ValueError, RecursionError) as error:
        raise SourceMapError("stock unparse produced malformed Python") from error
    reparsed_nodes = _ast_nodes(reparsed)
    if not _field_equal(tree, reparsed):
        _fail("stock unparse changed AST field topology/value")
    generated_geometry = _Geometry(generated)
    events, candidates = [], []
    for path, node, depth in reparsed_nodes:
        span = _node_span(node, generated_geometry)
        if span is None or span.start == span.end:
            continue
        origin = inherited[path]
        copied = (origin.kind == "copy" and generated[span.start:span.end] == source[origin.span.start:origin.span.end])
        index = len(candidates)
        candidates.append((span, origin.span, copied, depth))
        events.append((span.start, 1, index))
        events.append((span.end, 0, index))
    events.sort()
    active, heap, result = set(), [], []
    point, i = 0, 0
    while i < len(events):
        stop = events[i][0]
        while heap and heap[0][2] not in active:
            heapq.heappop(heap)
        if point < stop:
            if not heap:
                _fail("structural origins leave generated gap")
            span, original, copied, depth = candidates[heap[0][2]]
            a = original.start + point - span.start if copied else original.start
            z = original.start + stop - span.start if copied else original.end
            _append(result, MapSegment(point, stop, a, z, "copy" if copied else "anchor"))
        while i < len(events) and events[i][0] == stop:
            _, begin, index = events[i]
            if begin:
                active.add(index)
                heapq.heappush(heap, (-candidates[index][3], -int(candidates[index][2]), index))
            else:
                active.discard(index)
            i += 1
        point = stop
    if point != len(generated):
        _fail("structural generated coverage is incomplete")
    identity = _identity(SourceIdentity(generated_path, "python-v1", generated_role,
                                        hashlib.sha256(generated).hexdigest(), len(generated)))
    value = SourceMap(owner, translator, source_identity, identity, tuple(result))
    _validated(value, source, generated)
    return AstDerivation(generated, value, len(nodes))
