"""Compile-only finite .pya syntax and formatter; never executes authored code."""

import ast
import bisect
import io
import keyword
import re
import tokenize
import unicodedata
from dataclasses import dataclass

from . import source_maps as sm


@dataclass(frozen=True, slots=True)
class SyntaxIssue:
    rule: str
    category: str
    span: sm.ByteSpan
    reason: str
    line: int
    column: int
    end_line: int
    end_column: int


@dataclass(frozen=True, slots=True)
class ValBinding:
    keyword: sm.ByteSpan
    target: sm.ByteSpan
    statement: sm.ByteSpan


@dataclass(frozen=True, slots=True)
class PreparedSource:
    owner: sm.SourceOwner
    edition: str
    selected_edition: str
    authored_bytes: bytes
    authored_text: str
    scaffold_bytes: bytes
    scaffold_map: sm.SourceMap
    vals: tuple[ValBinding, ...]
    issues: tuple[SyntaxIssue, ...]


@dataclass(frozen=True, slots=True)
class PreparationResult:
    status: int
    issues: tuple[SyntaxIssue, ...]
    prepared: PreparedSource | None


@dataclass(frozen=True, slots=True)
class EmptyDisplayType:
    span: sm.ByteSpan
    family: str
    schema: str


@dataclass(frozen=True, slots=True)
class Translation:
    prepared: PreparedSource
    lowered_bytes: bytes
    lowered_map: sm.SourceMap
    used_collections: tuple[str, ...]
    empty_types: tuple[EmptyDisplayType, ...]


@dataclass(frozen=True, slots=True)
class TranslationResult:
    status: int
    issues: tuple[SyntaxIssue, ...]
    translation: Translation | None


@dataclass(frozen=True, slots=True)
class FormatEdit:
    span: sm.ByteSpan
    replacement: bytes


@dataclass(frozen=True, slots=True)
class FormatResult:
    status: int
    source_status: int
    issues: tuple[SyntaxIssue, ...]
    before: bytes
    after: bytes | None
    edits: tuple[FormatEdit, ...]
    source_map: sm.SourceMap | None


@dataclass(frozen=True, slots=True)
class _Token:
    kind: int
    text: str
    span: sm.ByteSpan


class _View:
    """Universal-newline token view with exact physical-byte endpoints."""
    def __init__(self, raw):
        self.geometry = sm._Geometry(raw)
        self.raw = raw
        self.lines = []
        self.offsets = []
        text = []
        for start, end in zip(self.geometry.starts, self.geometry.ends):
            line = raw[start:end].decode("utf-8")
            offsets = [start]
            cursor = start
            for char in line:
                cursor += len(char.encode("utf-8"))
                offsets.append(cursor)
            self.lines.append(line)
            self.offsets.append(offsets)
            text.append(line)
            if end < len(raw):
                text.append("\n")
        self.text = "".join(text)

    def at(self, row, column):
        if type(row) is not int or type(column) is not int or row < 1 or column < 0:
            sm._fail("invalid stock reporter coordinate")
        if row == len(self.lines) + 1 and column == 0:
            return len(self.raw)
        if row > len(self.lines) or column >= len(self.offsets[row - 1]):
            sm._fail("stock reporter coordinate is outside actual source")
        return self.offsets[row - 1][column]

    def tokens(self):
        result = []
        try:
            for token in tokenize.generate_tokens(io.StringIO(self.text).readline):
                if len(result) >= sm.MAX_TOKENS:
                    sm._fail("token count exceeds profile before stock parse")
                # tokenize's synthetic NEWLINE may extend beyond an unterminated line.
                start = self.at(*token.start)
                if token.type == tokenize.NEWLINE and token.string == "" and token.end[0] == token.start[0]:
                    end = start
                elif token.type in {tokenize.NEWLINE, tokenize.NL}:
                    end = self.geometry.starts[token.start[0]] if token.start[0] < len(self.lines) else len(self.raw)
                else:
                    end = self.at(*token.end)
                result.append(_Token(token.type, token.string, sm.ByteSpan(start, end)))
        except tokenize.TokenError as error:
            # API03's explicit EOF exception uses the actual source EOF point.
            # This one exact reason is evidenced for supported CPython3.13.1;
            # all other token failures preserve their stock reported location.
            point = len(self.raw) if error.args[0] == "unexpected EOF in multi-line statement" else self.at(*error.args[1])
            return None, _issue(self.raw, "PAL001", sm.ByteSpan(point, point), "stock tokenizer: " + error.args[0])
        except (IndentationError, SyntaxError) as error:
            return None, _reported_issue(self.raw, error, self)
        # The stock tokenizer may split combining identifier continuations into
        # ERRORTOKENs although the stock parser admits the complete identifier.
        # Merge only adjacent pieces whose complete spelling is an identifier.
        merged = []
        i = 0
        while i < len(result):
            token = result[i]
            if token.kind == tokenize.NAME:
                text, end, j = token.text, token.span.end, i + 1
                while j < len(result) and result[j].span.start == end and result[j].kind in {tokenize.NAME, tokenize.ERRORTOKEN}:
                    candidate = text + result[j].text
                    if not candidate.isidentifier():
                        break
                    text, end, j = candidate, result[j].span.end, j + 1
                merged.append(_Token(tokenize.NAME, text, sm.ByteSpan(token.span.start, end)))
                i = j
            else:
                merged.append(token)
                i += 1
        return tuple(merged), None


def _physical_position(raw, offset):
    """Malformed UTF8 issues disclose physical byte columns only."""
    starts, ends = [3 if raw.startswith(b"\xef\xbb\xbf") else 0], []
    i = starts[0]
    while i < len(raw):
        if raw[i] in (10, 13):
            ends.append(i)
            i += 2 if raw[i] == 13 and i + 1 < len(raw) and raw[i + 1] == 10 else 1
            starts.append(i)
        else:
            i += 1
    row = bisect.bisect_right(starts, offset) - 1
    if row < 0:
        return 1, 1
    return row + 1, offset - starts[row] + 1


def _issue(raw, rule, span, reason, *, malformed_encoding=False):
    if malformed_encoding:
        line, column = _physical_position(raw, span.start)
        end_line, end_column = _physical_position(raw, span.end)
    else:
        a, z = sm.position_at(raw, span.start), sm.position_at(raw, span.end)
        line, column, end_line, end_column = a.line, a.column, z.line, z.column
    return SyntaxIssue(rule, "tooling" if rule == "PAL001" else "semantic", span, reason,
                       line, column, end_line, end_column)


def _reported_issue(raw, error, view, provenance=None, authored=None):
    row, column = error.lineno, error.offset
    if row is None or column is None:
        sm._fail("stock parser did not supply an exact location")
    start = view.at(row, column - 1)
    if error.end_lineno is None or error.end_offset is None or error.end_offset < 1:
        end = start
    else:
        end = view.at(error.end_lineno, error.end_offset - 1)
    span = sm.ByteSpan(start, end)
    if provenance is not None:
        span = sm.map_range(provenance, span, source=authored, generated=raw).source_span
        raw = authored
    return _issue(raw, "PAL001", span, "stock parser: " + error.msg)


def _parse(raw, *, mode="exec"):
    """Stock parse first; finite node/plain-field bounds immediately afterward."""
    sm._bytes(raw)
    sm._token_bound(raw)
    try:
        tree = ast.parse(raw.decode("utf-8"), mode=mode, feature_version=(3, 13))
    except (ValueError, RecursionError) as error:
        raise sm.SourceMapError("stock parser refused bounded compile input") from error
    _bounded_tree(tree)
    return tree


def _bounded_tree(tree):
    stock = frozenset(value for value in vars(ast).values() if type(value) is type and issubclass(value, ast.AST))
    count, size, items, bits = 0, 0, 0, 0
    stack = [(tree, 0)]
    while stack:
        node, depth = stack.pop()
        if type(node) not in stock or depth > sm.MAX_AST_DEPTH:
            sm._fail("syntax AST class/depth exceeds profile")
        count += 1
        if count > sm.MAX_AST_NODES:
            sm._fail("syntax AST node count exceeds profile")
        for field, value in ast.iter_fields(node):
            values = value if type(value) is list else [value]
            items += 1 + len(values)
            if items > sm.MAX_FIELD_ITEMS:
                sm._fail("syntax AST field item count exceeds profile")
            for child in values:
                if type(child) in stock:
                    stack.append((child, depth + 1))
                elif type(child) is str:
                    try:
                        size += len(child.encode("utf-8"))
                    except UnicodeEncodeError as error:
                        raise sm.SourceMapError("syntax AST field is not UTF8") from error
                elif type(child) is bytes:
                    size += len(child)
                elif type(child) is int:
                    bits += child.bit_length()
                elif child is None or child is Ellipsis or type(child) in {bool, float, complex}:
                    pass
                else:
                    sm._fail("syntax AST field is not a stock plain value")
                if size > sm.MAX_FIELD_BYTES or bits > sm.MAX_INTEGER_BITS:
                    sm._fail("syntax AST plain field magnitude exceeds profile")
    return count


def _ast_span(node, raw, geometry=None):
    return sm._node_span(node, sm._Geometry(raw) if geometry is None else geometry)


class _Projection:
    """Invocation-local validated provenance index; no cross-input cache."""
    def __init__(self, value, source, generated):
        sm._validated(value, source, generated)
        self.value, self.geometry = value, sm._Geometry(generated)
        self.index = sm._HullIndex(value)
        self.anchors, self.gaps = [0], [0]
        prior = None
        for row in value.segments:
            self.anchors.append(self.anchors[-1] + int(row.kind != "copy"))
            self.gaps.append(self.gaps[-1] + int(prior is not None and prior.source_end != row.source_start))
            prior = row

    def range(self, span):
        self.geometry.span(span)
        if span.start == span.end:
            return sm._point(self.value, span.start, self.index.starts)
        first = bisect.bisect_right(self.index.starts, span.start) - 1
        last = bisect.bisect_left(self.index.starts, span.end) - 1
        hull = self.index.hull(span.start, span.end)
        exact = (self.anchors[last + 1] == self.anchors[first]
                 and self.gaps[last + 1] == self.gaps[first + 1]
                 and hull.end - hull.start == span.end - span.start)
        return sm.MappedRange(hull, exact, tuple(range(first, last + 1)))


def _issues(rows):
    result = {}
    for issue in rows:
        result[(issue.span.start, issue.span.end, issue.rule)] = issue
    return tuple(result[key] for key in sorted(result))


class _Builder:
    """Incremental byte/segment bounded splice builder, with exact source roles."""
    def __init__(self, raw, owner, translator, source, path, role):
        self.raw, self.owner, self.translator, self.source = raw, owner, translator, source
        self.path, self.role = path, role
        self.parts, self.rows, self.size = [], [], 0

    def add(self, payload, span, kind):
        sm._bytes(payload)
        if not payload:
            return
        if self.size + len(payload) > sm.MAX_GENERATED_BYTES:
            sm._fail("incremental syntax output exceeds profile")
        sm._append(self.rows, sm.MapSegment(self.size, self.size + len(payload), span.start, span.end, kind))
        self.parts.append(payload)
        self.size += len(payload)

    def copy(self, start, end):
        if start < end:
            self.add(self.raw[start:end], sm.ByteSpan(start, end), "copy")

    def anchor(self, payload, span):
        self.add(payload, span, "anchor")

    def finish(self):
        raw = b"".join(self.parts)
        identity = sm.source_identity(raw, path=self.path,
                                      edition=sm.EDITION if self.path.endswith(".pya") else "python-v1", role=self.role)
        value = sm.SourceMap(self.owner, self.translator, self.source, identity, tuple(self.rows))
        sm._validated(value, self.raw, raw)
        return raw, value


def _cookie(raw, view):
    # Same first/second physical-line and encoding-name recognition as tokenize.
    cookie = re.compile(r"^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)", re.ASCII)
    blank = re.compile(r"^[ \t\f]*(?:[#\r\n]|$)")
    for index in range(min(2, len(view.lines))):
        if index == 1 and not blank.match(view.lines[0]):
            break
        match = cookie.match(view.lines[index])
        if match:
            name = match.group(1)
            normalized = name[:12].lower().replace("_", "-")
            accepted = normalized == "utf-8" or normalized.startswith("utf-8-")
            if not accepted:
                span = sm.ByteSpan(view.at(index + 1, match.start(1)), view.at(index + 1, match.end(1)))
                return _issue(raw, "PAL001", span, "only the stock UTF8 cookie profile is supported")
            break
    return None


_TRIVIA = {tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.NL, tokenize.ENCODING}
_AUGMENTED = {"+=", "-=", "*=", "/=", "//=", "%=", "**=", "@=", "|=", "&=", "^=", "<<=", ">>="}


def _val_headers(raw, view, tokens):
    candidates, issues = [], []
    for i, token in enumerate(tokens):
        if token.kind != tokenize.NAME or token.text != "val":
            continue
        j = i + 1
        while j < len(tokens) and tokens[j].kind in _TRIVIA:
            j += 1
        if j == len(tokens):
            continue
        target = tokens[j]
        # Ordinary valid identifier uses are reserved semantic identities.
        if target.kind not in {tokenize.NAME} and target.text not in {"(", "["}:
            continue
        if target.kind == tokenize.NAME and target.text in {"in", "as", "if", "else"}:
            continue
        prefix = raw[view.geometry.starts[view.geometry.position(token.span.start).line - 1]:token.span.start]
        if target.kind != tokenize.NAME and prefix.strip(b" \t\f"):
            # A call or function identifier such as def val(...) is ordinary
            # parseable Python and receives the complete NAME collision issue.
            continue
        if prefix.strip(b" \t\f"):
            issues.append(_issue(raw, "PAL001", token.span, "val declaration must start a physical statement line"))
            continue
        if target.kind != tokenize.NAME or keyword.iskeyword(unicodedata.normalize("NFKC", target.text)):
            issues.append(_issue(raw, "PAL001", target.span, "val target must be one nonkeyword name"))
            continue
        cursor, depth, equals, end_token = j + 1, 0, None, None
        annotation = False
        bad = None
        while cursor < len(tokens):
            part = tokens[cursor]
            if part.kind in {tokenize.NEWLINE, tokenize.ENDMARKER}:
                end_token = part
                break
            if part.kind in _TRIVIA:
                cursor += 1
                continue
            if depth == 0:
                if part.text == ";":
                    bad = token.span
                    break
                if equals is None:
                    if cursor == j + 1 and part.text == ":":
                        annotation = True
                    elif part.text == "=":
                        equals = cursor
                    elif part.text in _AUGMENTED or not annotation:
                        bad = part.span
                        break
            if part.text in {"(", "[", "{"}:
                depth += 1
            elif part.text in {")", "]", "}"}:
                depth -= 1
            cursor += 1
        header_end = tokens[equals].span.end if equals is not None else (end_token.span.start if end_token else len(raw))
        slash = raw.find(b"\\", token.span.end, header_end)
        if slash >= 0:
            # Only a gap outside annotation tokens is an explicit header escape.
            if not any(part.span.start <= slash < part.span.end for part in tokens[j:equals if equals is not None else cursor]):
                bad = sm.ByteSpan(slash, slash + 1)
        if bad is not None:
            issues.append(_issue(raw, "PAL001", bad, "malformed val declaration header"))
            continue
        significant = [part for part in tokens[(equals + 1 if equals is not None else cursor):cursor] if part.kind not in _TRIVIA]
        if equals is None or not significant:
            point = end_token.span.start if end_token else len(raw)
            issues.append(_issue(raw, "PAL001", sm.ByteSpan(point, point), "val requires an initializer"))
            continue
        separator = raw[token.span.end:target.span.start]
        if not separator or any(byte not in (32, 9) for byte in separator):
            issues.append(_issue(raw, "PAL001", token.span, "val separator must be horizontal whitespace"))
            continue
        candidates.append((token, target))
    if issues:
        return None, min(issues, key=lambda item: item.span.start)
    return tuple(candidates), None


def _copy_without(raw, cuts, owner, translator):
    source = sm.source_identity(raw, path=owner.authored_path, edition=sm.EDITION, role="authored")
    builder = _Builder(raw, owner, translator, source, owner.runtime_path, "scaffold")
    cursor = 0
    for span in cuts:
        builder.copy(cursor, span.start)
        cursor = span.end
    builder.copy(cursor, len(raw))
    return builder.finish()


def prepare_source(raw, owner, *, edition, translator):
    sm._bytes(raw, sm.MAX_AUTHORED_BYTES)
    sm._owner(owner)
    sm._translator(translator)
    sm._text(edition)
    if not owner.authored_path.endswith(".pya") or edition not in {sm.EDITION, "python-v1"}:
        sm._fail("syntax requires a .pya owner and a known edition")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        issue = _issue(raw, "PAL001", sm.ByteSpan(error.start, error.end), "authored source is not strict UTF8",
                       malformed_encoding=True)
        return PreparationResult(2, (issue,), None)
    if raw.startswith(b"\xef\xbb\xbf"):
        text = text[1:]
    view = _View(raw)
    problem = _cookie(raw, view)
    if problem is not None:
        return PreparationResult(2, (problem,), None)
    tokens, problem = view.tokens()
    if problem is not None:
        return PreparationResult(2, (problem,), None)
    candidates, problem = _val_headers(raw, view, tokens)
    if problem is not None:
        return PreparationResult(2, (problem,), None)
    cuts = [sm.ByteSpan(0, 3)] if view.geometry.bom else []
    cuts.extend(sm.ByteSpan(token.span.start, target.span.start) for token, target in candidates)
    scaffold, provenance = _copy_without(raw, sorted(cuts, key=lambda span: span.start), owner, translator)
    try:
        tree = _parse(scaffold)
    except SyntaxError as error:
        problem = _reported_issue(scaffold, error, _View(scaffold), provenance, raw)
        return PreparationResult(2, (problem,), None)
    projection = _Projection(provenance, raw, scaffold)
    direct_class, statements, strings = set(), {}, []
    stack = [tree]
    while stack:
        node = stack.pop()
        if type(node) is ast.ClassDef:
            direct_class.update(id(child) for child in node.body)
        if type(node) in {ast.Assign, ast.AnnAssign}:
            targets = node.targets if type(node) is ast.Assign else [node.target]
            if targets and type(targets[0]) is ast.Name:
                span = _ast_span(targets[0], scaffold, projection.geometry)
                original = projection.range(span)
                statements[(original.source_span.start, original.source_span.end)] = node
        if type(node) is ast.JoinedStr:
            strings.append(projection.range(_ast_span(node, scaffold, projection.geometry)).source_span)
        stack.extend(ast.iter_child_nodes(node))
    vals = []
    for token, target in candidates:
        node = statements.get((target.span.start, target.span.end))
        if node is None:
            sm._fail("admitted val target has no exact stock statement")
        if type(node) is ast.Assign and len(node.targets) != 1:
            second = projection.range(_ast_span(node.targets[1], scaffold, projection.geometry)).source_span
            following = projection.range(_ast_span(node.targets[2] if len(node.targets) > 2 else node.value, scaffold, projection.geometry)).source_span
            separators = [part for part in tokens if part.kind == tokenize.OP and part.text == "="
                          and second.end <= part.span.start < following.start]
            if len(separators) != 1:
                sm._fail("chained val has no unique actual second assignment separator")
            return PreparationResult(2, (_issue(raw, "PAL001", separators[0].span, "val cannot chain assignment targets"),), None)
        if id(node) in direct_class:
            return PreparationResult(2, (_issue(raw, "PAL001", token.span, "val cannot declare a direct class field"),), None)
        stop = projection.range(_ast_span(node, scaffold, projection.geometry)).source_span.end
        vals.append(ValBinding(token.span, target.span, sm.ByteSpan(token.span.start, stop)))
    semantic = []
    if edition != sm.EDITION:
        semantic.append(_issue(raw, "PAL390", sm.ByteSpan(view.geometry.bom, view.geometry.bom), "experimental syntax edition is disabled"))
    declarations = {row.keyword for row in vals}
    for token in tokens:
        if token.kind != tokenize.NAME or token.span in declarations or any(span.start <= token.span.start < span.end for span in strings):
            continue
        normalized = unicodedata.normalize("NFKC", token.text)
        if normalized == "val" or normalized.startswith("_pyalamode_syntax_"):
            semantic.append(_issue(raw, "PAL392", token.span, "reserved syntax identifier identity"))
    issues = _issues(semantic)
    prepared = PreparedSource(owner, sm.EDITION, edition, raw, text, scaffold, provenance, tuple(vals), issues)
    return PreparationResult(1 if issues else 0, issues, prepared)


def _prepared(value):
    if type(value) is not PreparedSource:
        sm._fail("expected exact PreparedSource")
    sm._text(value.edition)
    sm._text(value.selected_edition)
    sm._text(value.authored_text, sm.MAX_AUTHORED_BYTES)
    sm._bytes(value.authored_bytes, sm.MAX_AUTHORED_BYTES)
    sm._bytes(value.scaffold_bytes)
    if type(value.vals) is not tuple or type(value.issues) is not tuple:
        sm._fail("prepared rows must be exact tuples")
    geometry = sm._Geometry(value.authored_bytes)
    for row in value.vals:
        if type(row) is not ValBinding:
            sm._fail("expected exact ValBinding")
        for span in (row.keyword, row.target, row.statement):
            geometry.span(span)
    for row in value.issues:
        if type(row) is not SyntaxIssue:
            sm._fail("expected exact SyntaxIssue")
        for field in (row.rule, row.category, row.reason):
            sm._text(field)
        geometry.span(row.span)
        for coordinate in (row.line, row.column, row.end_line, row.end_column):
            sm._integer(coordinate, minimum=1)
    sm._validated(value.scaffold_map, value.authored_bytes, value.scaffold_bytes)
    rebuilt = prepare_source(value.authored_bytes, value.owner, edition=value.selected_edition, translator=value.scaffold_map.translator)
    if rebuilt.prepared is None or rebuilt.prepared != value:
        sm._fail("PreparedSource is not the actual fresh authored derivation")
    return value


def _value_displays(tree):
    """Traverse runtime value fields; syntax-only contexts and strings stay opaque."""
    found = []
    pending = [tree]
    while pending:
        node = pending.pop()
        if isinstance(node, ast.pattern) or isinstance(node, ast.expr) and getattr(node, "ctx", None) is not None and type(node.ctx) is ast.Store:
            continue
        if type(node) in {ast.Constant, ast.JoinedStr}:
            continue
        if type(node) in {ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp}:
            found.append(node)
            continue
        if type(node) in {ast.List, ast.Dict, ast.Set}:
            found.append(node)
            if (type(node) is ast.Dict and any(key is None for key in node.keys)
                    or type(node) in {ast.List, ast.Set} and any(type(child) is ast.Starred for child in node.elts)):
                continue
        for field, value in ast.iter_fields(node):
            if field in {"annotation", "returns", "type_params", "pattern"}:
                continue
            children = value if type(value) is list else [value]
            pending.extend(child for child in children if isinstance(child, ast.AST))
    return found


def _direct_empty(tree, raw, projection):
    direct = {}
    for node in ast.walk(tree):
        if type(node) is ast.AnnAssign and type(node.target) is ast.Name and type(node.value) in {ast.List, ast.Dict}:
            if node.value.elts if type(node.value) is ast.List else node.value.keys:
                continue
            span = projection.range(_ast_span(node.value, raw, projection.geometry))
            if span.exact:
                direct[span.source_span] = node
    return direct


def _contexts(rows, direct, authored):
    if type(rows) is not tuple or len(rows) > sm.MAX_AST_NODES:
        sm._fail("empty context rows must be a bounded exact tuple")
    result = {}
    geometry = sm._Geometry(authored)
    for row in rows:
        if type(row) is not EmptyDisplayType:
            sm._fail("expected exact EmptyDisplayType")
        geometry.span(row.span)
        sm._text(row.family)
        sm._text(row.schema, sm.MAX_AUTHORED_BYTES)
        family = "Vector" if row.span in direct and type(direct[row.span].value) is ast.List else "Map"
        if row.family not in {"Vector", "Map"} or row.family != family or row.span not in direct or row.span in result or not row.schema:
            sm._fail("empty context is duplicate, stale, wrong-family or not a direct annotated initializer")
        # Canonical schema is a nonempty inherited resolved collection shape,
        # never an evaluated type or a claim that its names are available.
        if not row.schema.startswith(row.family + "[") or not row.schema.endswith("]"):
            sm._fail("empty context canonical family/schema mismatch")
        try:
            schema = _parse(row.schema.encode("utf-8"), mode="eval").body
        except SyntaxError as error:
            raise sm.SourceMapError("empty context schema is not a closed collection expression") from error
        if (type(schema) is not ast.Subscript or type(schema.value) is not ast.Name or schema.value.id != row.family
                or (len(schema.slice.elts) if type(schema.slice) is ast.Tuple else 1) != (1 if row.family == "Vector" else 2)):
            sm._fail("empty context canonical schema arity differs")
        if not _canonical_argument_shape(schema.slice):
            sm._fail("empty context canonical schema arguments are outside the finite data vocabulary")
        result[row.span] = row
    return result


_ARG_CLASSES = {ast.Name, ast.Attribute, ast.Subscript, ast.Tuple, ast.Load, ast.Constant}


def _canonical_argument_shape(node):
    pending = [(node, False)]
    while pending:
        child, record_identity = pending.pop()
        if type(child) not in _ARG_CLASSES:
            return False
        if type(child) is ast.Constant:
            if child.value is None or child.value is Ellipsis:
                continue
            if not record_identity or type(child.value) is not str or not child.value:
                return False
            continue
        if type(child) is ast.Subscript:
            record = type(child.value) is ast.Name and child.value.id in {"Record", "OneOf", "Case"}
            pending.append((child.value, False))
            pending.append((child.slice, record))
        else:
            pending.extend((value, False) for value in ast.iter_child_nodes(child))
    return True


def _argument_shape(node):
    pending = [node]
    while pending:
        child = pending.pop()
        if type(child) not in _ARG_CLASSES:
            return False
        if type(child) is ast.Constant and child.value is not None and child.value is not Ellipsis:
            return False
        pending.extend(ast.iter_child_nodes(child))
    return True


def _annotation_arguments(node, row, raw, geometry):
    annotation = node.annotation
    quoted = type(annotation) is ast.Constant and type(annotation.value) is str
    if quoted:
        try:
            parsed = _parse(annotation.value.encode("utf-8"), mode="eval")
        except (SyntaxError, UnicodeEncodeError):
            return None
        annotation = parsed.body
    if type(annotation) is not ast.Subscript:
        return None
    arguments = annotation.slice.elts if type(annotation.slice) is ast.Tuple else [annotation.slice]
    if len(arguments) != (1 if row.family == "Vector" else 2) or not all(_argument_shape(argument) for argument in arguments):
        return None
    if quoted:
        try:
            rendered = ast.unparse(annotation.slice).encode("utf-8")
        except (ValueError, TypeError, RecursionError, UnicodeEncodeError) as error:
            raise sm.SourceMapError("stock annotation unparse refused") from error
        sm._bytes(rendered)
        # Unparse a tuple slice as its argument list, not a tuple wrapper.
        if type(annotation.slice) is ast.Tuple:
            rendered = rendered[1:-1] if rendered.startswith(b"(") and rendered.endswith(b")") else rendered
        if not _equal_ast(annotation.slice, _parse(rendered, mode="eval").body):
            sm._fail("stock annotation rendering changed structural argument topology")
        return rendered, _ast_span(node.annotation, raw, geometry), "anchor"
    span = _ast_span(annotation.slice, raw, geometry)
    return raw[span.start:span.end], span, "copy"


def _newline(raw):
    match = re.search(b"\r\n|\r|\n", raw)
    return match.group() if match else b"\n"


def _import_point(tree, raw):
    body = tree.body
    i = 0
    if body and type(body[0]) is ast.Expr and type(body[0].value) is ast.Constant and type(body[0].value.value) is str:
        i += 1
    while i < len(body) and type(body[i]) is ast.ImportFrom and body[i].module == "__future__":
        i += 1
    if i == len(body):
        return len(raw)
    node = body[i]
    line = min([node.lineno] + [decorator.lineno for decorator in getattr(node, "decorator_list", [])])
    return sm._Geometry(raw).starts[line - 1]


def _punctuation(tokens, node_span, text, starts):
    first = bisect.bisect_left(starts, node_span.start)
    last = bisect.bisect_left(starts, node_span.end)
    return [token for token in tokens[first:last] if token.kind == tokenize.OP and token.text == text
            and node_span.start <= token.span.start and token.span.end <= node_span.end]


def _expected_lowered(tree, nodes, arguments, used):
    """Independent stock-AST splice oracle: children once and original order."""
    selected = {id(node): family for span, node, family, origin in nodes}
    def visit(node):
        if (isinstance(node, ast.pattern) or type(node) in {ast.Constant, ast.JoinedStr}
                or isinstance(node, ast.expr) and type(getattr(node, "ctx", None)) is ast.Store):
            return node
        for field, value in ast.iter_fields(node):
            if field in {"annotation", "returns", "type_params", "pattern"}:
                continue
            if isinstance(value, ast.AST):
                setattr(node, field, visit(value))
            elif type(value) is list:
                setattr(node, field, [visit(child) if isinstance(child, ast.AST) else child for child in value])
        family = selected.get(id(node))
        if family is None:
            return node
        root = ast.Name(id="_pyalamode_syntax_" + family, ctx=ast.Load())
        if id(node) in arguments:
            root = ast.Subscript(value=root, slice=_parse(arguments[id(node)][0], mode="eval").body, ctx=ast.Load())
        children = ([ast.Tuple(elts=[key, value], ctx=ast.Load()) for key, value in zip(node.keys, node.values)]
                    if type(node) is ast.Dict else node.elts)
        return ast.Call(func=ast.Attribute(value=root, attr="of", ctx=ast.Load()), args=children, keywords=[])
    expected = visit(tree)
    index = 0
    if expected.body and type(expected.body[0]) is ast.Expr and type(expected.body[0].value) is ast.Constant and type(expected.body[0].value.value) is str:
        index += 1
    while index < len(expected.body) and type(expected.body[index]) is ast.ImportFrom and expected.body[index].module == "__future__":
        index += 1
    expected.body[index:index] = [ast.ImportFrom(module="pyalamode", names=[ast.alias(name=family, asname="_pyalamode_syntax_" + family)], level=0)
                                for family in used]
    return expected


def lower_source(prepared, *, empty_types=()):
    prepared = _prepared(prepared)
    raw, authored = prepared.scaffold_bytes, prepared.authored_bytes
    tree = _parse(raw)
    tokens, problem = _View(raw).tokens()
    if problem is not None:
        sm._fail("fresh scaffold tokenization differs from preparation")
    projection = _Projection(prepared.scaffold_map, authored, raw)
    token_starts = [token.span.start for token in tokens]
    direct = _direct_empty(tree, raw, projection)
    contexts = _contexts(empty_types, direct, authored)
    displays = _value_displays(tree)
    nodes, semantic, used, arguments = [], list(prepared.issues), set(), {}
    for node in displays:
        span = _ast_span(node, raw, projection.geometry)
        origin = projection.range(span).source_span
        unsupported = (type(node) in {ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp}
                       or type(node) is ast.Dict and any(key is None for key in node.keys)
                       or type(node) in {ast.List, ast.Set} and any(type(child) is ast.Starred for child in node.elts))
        if unsupported:
            semantic.append(_issue(authored, "PAL391", origin, "unsupported runtime display grammar"))
            continue
        family = {ast.List: "Vector", ast.Dict: "Map", ast.Set: "Set"}[type(node)]
        empty = not (node.keys if type(node) is ast.Dict else node.elts)
        if empty:
            row = contexts.get(origin)
            parsed_arguments = _annotation_arguments(direct[origin], row, raw, projection.geometry) if row is not None else None
            if parsed_arguments is None:
                semantic.append(_issue(authored, "PAL391", origin, "empty display requires an available supported direct collection annotation"))
                continue
            arguments[id(node)] = parsed_arguments
        used.add(family)
        nodes.append((span, node, family, origin))
    issues = _issues(semantic)
    if issues:
        return TranslationResult(1, issues, None)
    used = tuple(family for family in ("Vector", "Map", "Set") if family in used)
    point = _import_point(tree, raw)
    source = prepared.scaffold_map.generated
    builder = _Builder(raw, prepared.owner, prepared.scaffold_map.translator, source, prepared.owner.runtime_path, "lowered")
    # All edits are finite nonoverlapping punctuation/copy insertions. Nested
    # display punctuation has distinct locations, and children remain copied.
    events = []
    sequence = 0
    def replacement(start, end, pieces):
        nonlocal sequence
        events.append((start, end, sequence, pieces))
        sequence += 1
    for span, node, family, origin in nodes:
        opening, closing = span.start, span.end - 1
        if raw[opening:opening + 1] not in {b"[", b"{"} or raw[closing:span.end] not in {b"]", b"}"}:
            sm._fail("stock display does not retain its exact delimiters")
        alias = ("_pyalamode_syntax_" + family).encode("ascii")
        if id(node) in arguments:
            payload, argument_span, kind = arguments[id(node)]
            replacement(opening, opening + 1, [(alias + b"[", span, "anchor"),
                                              (payload, argument_span, kind), (b"].of(", span, "anchor")])
        else:
            replacement(opening, opening + 1, [(alias + b".of(", span, "anchor")])
        replacement(closing, span.end, [(b")", span, "anchor")])
        if type(node) is ast.Dict:
            for key, value in zip(node.keys, node.values):
                key_span, value_span = _ast_span(key, raw, projection.geometry), _ast_span(value, raw, projection.geometry)
                pair = sm.ByteSpan(key_span.start, value_span.end)
                colons = [token for token in _punctuation(tokens, sm.ByteSpan(key_span.end, value_span.start), ":", token_starts)
                          if key_span.end <= token.span.start < value_span.start]
                if len(colons) != 1:
                    sm._fail("dictionary pair has no unique exact separator")
                replacement(key_span.start, key_span.start, [(b"(", pair, "anchor")])
                replacement(colons[0].span.start, colons[0].span.end, [(b",", pair, "anchor")])
                replacement(value_span.end, value_span.end, [(b")", pair, "anchor")])
    if used:
        line_end = _newline(raw)
        payload = b"".join(("from pyalamode import " + family + " as _pyalamode_syntax_" + family).encode("ascii") + line_end for family in used)
        if point and raw[point - 1:point] not in {b"\r", b"\n"}:
            payload = line_end + payload
        replacement(point, point, [(payload, sm.ByteSpan(0, point), "anchor")])
    # At a shared endpoint closing inner syntax precedes closing pair syntax;
    # pair opening precedes display opening. Sequence derives literal traversal.
    def order(event):
        start, end, seq, pieces = event
        insert = start == end
        close_pair = insert and pieces[0][0] == b")"
        return start, 0 if close_pair else 1 if insert else 2, seq
    events.sort(key=order)
    cursor = 0
    for start, end, seq, pieces in events:
        if start < cursor:
            sm._fail("constructor splice ranges overlap")
        builder.copy(cursor, start)
        for payload, anchor, kind in pieces:
            builder.add(payload, anchor, kind)
        cursor = end
    builder.copy(cursor, len(raw))
    lowered, intermediate = builder.finish()
    try:
        lowered_tree = _parse(lowered)
    except SyntaxError as error:
        raise sm.SourceMapError("finite constructor splice is not stock Python") from error
    # Compare all stock fields, including child order and typed arguments.
    # Neither generated constructor nor imported product is ever invoked.
    expected = _expected_lowered(tree, nodes, arguments, used)
    if not _equal_ast(expected, lowered_tree):
        sm._fail("finite constructor transformation shape differs")
    provenance = sm.compose_maps(prepared.scaffold_map, intermediate, source=authored, intermediate=raw, generated=lowered)
    return TranslationResult(0, (), Translation(prepared, lowered, provenance, used, empty_types))


def translate_source(raw, owner, *, edition, translator, empty_types=()):
    result = prepare_source(raw, owner, edition=edition, translator=translator)
    if result.prepared is None:
        return TranslationResult(result.status, result.issues, None)
    return lower_source(result.prepared, empty_types=empty_types)


def _format_edits(prepared):
    raw = prepared.authored_bytes
    tokens, problem = _View(raw).tokens()
    if problem is not None:
        sm._fail("fresh formatting tokens differ from preparation")
    protected = [token.span for token in tokens if token.kind in {tokenize.STRING, tokenize.COMMENT}]
    tree = _parse(prepared.scaffold_bytes)
    projection = _Projection(prepared.scaffold_map, raw, prepared.scaffold_bytes)
    for node in ast.walk(tree):
        if type(node) is ast.JoinedStr:
            protected.append(projection.range(_ast_span(node, prepared.scaffold_bytes, projection.geometry)).source_span)
    protected.sort(key=lambda span: span.start)
    edits = []
    for row in prepared.vals:
        span = sm.ByteSpan(row.keyword.end, row.target.start)
        if raw[span.start:span.end] != b" ":
            edits.append(FormatEdit(span, b" "))
    geometry = sm._Geometry(raw)
    for start, end in zip(geometry.starts, geometry.ends):
        stop = end
        while stop > start and raw[stop - 1] in (32, 9):
            stop -= 1
        if stop == end:
            continue
        if any(span.start < end and stop < span.end for span in protected):
            continue
        # Whitespace-only lines may shrink; nonblank indentation stays copied.
        edits.append(FormatEdit(sm.ByteSpan(stop, end), b""))
    if not raw.endswith((b"\n", b"\r")):
        edits.append(FormatEdit(sm.ByteSpan(len(raw), len(raw)), _newline(raw)))
    edits.sort(key=lambda row: (row.span.start, row.span.end))
    for previous, current in zip(edits, edits[1:]):
        if previous.span.end > current.span.start:
            sm._fail("formatter edits overlap")
    return tuple(edits)


def _apply_format(prepared, edits):
    raw = prepared.authored_bytes
    builder = _Builder(raw, prepared.owner, prepared.scaffold_map.translator,
                       prepared.scaffold_map.source, prepared.owner.authored_path, "formatted")
    cursor = 0
    for edit in edits:
        builder.copy(cursor, edit.span.start)
        builder.anchor(edit.replacement, edit.span)
        cursor = edit.span.end
    builder.copy(cursor, len(raw))
    return builder.finish()


def _equal_ast(left, right):
    # Compile-generated stock trees only; bounded nodes/plain fields precede this.
    pending = [(left, right)]
    while pending:
        a, b = pending.pop()
        if type(a) is not type(b):
            return False
        if isinstance(a, ast.AST):
            pending.extend((getattr(a, name), getattr(b, name)) for name in a._fields)
        elif type(a) is list:
            if len(a) != len(b):
                return False
            pending.extend(zip(a, b))
        elif a != b:
            return False
    return True


def format_source(raw, owner, *, edition, translator, empty_types=()):
    original = prepare_source(raw, owner, edition=edition, translator=translator)
    if original.prepared is None:
        return FormatResult(2, 2, original.issues, raw, None, (), None)
    checked = lower_source(original.prepared, empty_types=empty_types)
    if checked.status:
        return FormatResult(2, checked.status, checked.issues, raw, None, (), None)
    edits = _format_edits(original.prepared)
    after, provenance = _apply_format(original.prepared, edits)
    rows = []
    for row in empty_types:
        ranges = sm.generated_ranges(provenance, row.span, source=raw, generated=after)
        if len(ranges) != 1:
            sm._fail("formatted empty initializer does not survive once")
        mapped = sm.map_range(provenance, ranges[0], source=raw, generated=after)
        if not mapped.exact or mapped.source_span != row.span:
            sm._fail("formatted empty initializer is not a proportional copy")
        rows.append(EmptyDisplayType(ranges[0], row.family, row.schema))
    formatted = prepare_source(after, owner, edition=edition, translator=translator)
    if formatted.status or formatted.prepared is None:
        sm._fail("safe formatter changed preparation status")
    lowered = lower_source(formatted.prepared, empty_types=tuple(rows))
    if lowered.status or lowered.translation is None:
        sm._fail("safe formatter changed translation status")
    if (not _equal_ast(_parse(original.prepared.scaffold_bytes), _parse(formatted.prepared.scaffold_bytes))
            or not _equal_ast(_parse(checked.translation.lowered_bytes), _parse(lowered.translation.lowered_bytes))):
        sm._fail("formatter changed stock AST/constructor structure")
    if _format_edits(formatted.prepared):
        sm._fail("formatter is not byte idempotent")
    return FormatResult(1 if edits else 0, 0, (), raw, after, edits, provenance)
