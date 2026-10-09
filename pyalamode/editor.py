"""Bounded local LSP editor views over the shared static project engine.

This module never imports application source, applies edits, writes approvals or
executes built artifacts. All protocol ranges are zero-based UTF-16.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import asdict
import difflib
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from .model import CHECKER_VERSION, TARGET, diagnostic, foundation_identities
from .project import check_snapshot

MAX_BODY = 8 * 1024 * 1024
MAX_HEADER = 8 * 1024


class ProtocolError(Exception):
    def __init__(self, message, code=-32602):
        super().__init__(message)
        self.code = code


def uri_path(uri, root, *, python=False, directory=False):
    if type(uri) is not str or re.search(r"%(?![0-9A-Fa-f]{2})", uri):
        raise ProtocolError("expected a valid local file URI")
    try:
        parsed = urlsplit(uri)
    except ValueError:
        raise ProtocolError("malformed local file URI") from None
    if parsed.scheme != "file" or parsed.netloc or parsed.query or parsed.fragment:
        raise ProtocolError("only local file URIs without authority/query/fragment are supported")
    try:
        decoded = unquote(parsed.path, encoding="utf-8", errors="strict")
        if "\x00" in decoded or not decoded.startswith("/"):
            raise ValueError
        path = Path(decoded).resolve()
    except (UnicodeError, ValueError, OSError):
        raise ProtocolError("invalid local file URI path") from None
    if not path.is_relative_to(root) or (directory and not path.is_dir()) or (not directory and not path.is_file()):
        raise ProtocolError("URI must resolve to existing content within this workspace")
    if python and path.suffix != ".py":
        raise ProtocolError("document must be an existing Python file")
    return path


def _lines(text):
    # splitlines also splits Unicode separators which Python source positions do
    # not count as newline. Preserve LF/CRLF/lone-CR physical source coordinates.
    return re.split(r"\r\n|\r|\n", text)


def position(text, line, column, encoding="utf-8-bytes"):
    """Convert one-based producer coordinates to a bounded UTF-16 position."""
    lines = _lines(text)
    number = max(0, min((line or 1) - 1, len(lines) - 1))
    value = lines[number]
    count = max(0, (column or 1) - 1)
    if encoding == "utf-8-bytes":
        prefix = value.encode("utf-8")[:count].decode("utf-8", errors="ignore")
    else:
        prefix = value[:count]
    return {"line": number, "character": len(prefix.encode("utf-16-le")) // 2}


def node_range(text, node):
    return {"start": position(text, node.lineno, node.col_offset + 1),
            "end": position(text, node.end_lineno, node.end_col_offset + 1)}


def _offset(text, point):
    if type(point) is not dict or set(point) != {"line", "character"} or any(type(point[k]) is not int or point[k] < 0 for k in point):
        raise ProtocolError("positions require nonnegative integer line/character")
    lines = _lines(text)
    line, character = point["line"], point["character"]
    if line >= len(lines):
        raise ProtocolError("position line is outside document")
    value = lines[line]
    parts = re.split(r"(\r\n|\r|\n)", text)
    start = sum(len(part) for part in parts[:line * 2])
    units = 0
    for index, char in enumerate(value):
        if units == character:
            return start + index
        units += 2 if ord(char) > 0xFFFF else 1
    if units != character:
        raise ProtocolError("position character is outside document or splits a surrogate pair")
    return start + len(value)


def _contains(range_, point):
    value = (point["line"], point["character"])
    return (range_["start"]["line"], range_["start"]["character"]) <= value < (range_["end"]["line"], range_["end"]["character"])


def _selection(text, node):
    line = _lines(text)[node.lineno - 1]
    match = re.search(r"\b(?:def|class)\s+([^\s(:]+)", line)
    if not match:
        return node_range(text, node)
    return {"start": position(text, node.lineno, match.start(1) + 1, "unicode-codepoints"),
            "end": position(text, node.lineno, match.end(1) + 1, "unicode-codepoints")}


def _definitions(text):
    try:
        tree = ast.parse(text, feature_version=(3, 13))
    except (SyntaxError, ValueError):
        return {}, None
    nodes = {}
    def visit(body, prefix=""):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                name = prefix + node.name
                nodes[name] = node
                visit(node.body, name + ".")
    visit(tree.body)
    return nodes, tree


class EditorSession:
    """Serialized document state; every observation refreshes the shared engine."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise ProtocolError("root must be an existing project directory")
        self.documents = {}
        self.initialized = False
        self.shutdown = False
        self.exited = False
        self.audit = False
        self.current = None
        self.notifications = []
        self.published = set()
        self.diagnostics = []
        self.regions = []
        self.nodes = {}
        self.startup_products = foundation_identities()

    def drain_notifications(self):
        items, self.notifications = self.notifications, []
        return items

    def refresh(self):
        self.current = check_snapshot([self.root], root=self.root, audit=self.audit, cache=False, overlays=self.documents)
        if self.current.inputs["product_artifacts"] != self.startup_products:
            self.current.freshness = "stale; recheck required"
            self.current.result.tooling.append(diagnostic("PAL001", str(self.root), "server product bytes changed after startup; restart required", origin="editor loaded implementation"))
            for file in self.current.result.results:
                file.diagnostics.append(diagnostic("PAL001", file.path, "server product bytes changed after startup; restart required", origin="editor loaded implementation"))
                for declaration in [*file.records, *file.variants]:
                    declaration["source_evidence"] = "unverified: loaded server implementation changed"
                for contract in file.contracts:
                    contract.source_evidence = "unverified: loaded server implementation changed"
                    contract.freshness = "stale; restart required"
                    contract.behavior = "unverified behavior; no certified effect bound"
        self.nodes = {path: _definitions(text)[0] for path, text in self.current.sources.items()}
        self.regions = []
        for file in self.current.result.results:
            text = self.current.sources.get(file.path, "")
            for contract in file.contracts:
                node = self.nodes.get(file.path, {}).get(contract.name)
                if node:
                    self.regions.append({"uri": Path(file.path).as_uri(), "range": node_range(text, node),
                                         "selectionRange": _selection(text, node), "name": contract.name,
                                         "kind": "function", "mode": file.mode, "contract": asdict(contract)})
            for kind, declarations in (("record", file.records), ("variant", file.variants), ("unsafe", file.unsafe_adapters)):
                for declaration in declarations:
                    node = self.nodes.get(file.path, {}).get(declaration["name"])
                    if node:
                        self.regions.append({"uri": Path(file.path).as_uri(), "range": node_range(text, node),
                                             "selectionRange": _selection(text, node), "name": declaration["name"],
                                             "kind": kind, "mode": "off" if kind == "unsafe" else file.mode,
                                             "contract": dict(declaration)})
        raw = [*self.current.result.tooling, *(item for file in self.current.result.results for item in file.diagnostics)]
        self.diagnostics = []
        grouped = {}
        for index, item in enumerate(raw):
            path = Path(item.path).resolve()
            # A malformed project cannot give the client an outside-file read.
            if not path.is_relative_to(self.root):
                continue
            text = self.current.sources.get(str(path), "")
            range_ = {"start": position(text, item.line, item.column, item.column_encoding),
                      "end": position(text, item.end_line or item.line, item.end_column or item.column, item.column_encoding)}
            data = {"boundary": item.boundary, "origin": item.origin, "reason": item.reason,
                    "remediation": item.remediation, "authored": {key: getattr(item, key) for key in ("path", "line", "column", "end_line", "end_column", "column_encoding")},
                    "snapshot": self.current.snapshot, "version": self.documents.get(str(path), {}).get("version"),
                    "diagnosticIndex": index}
            lsp_diagnostic = {"range": range_, "severity": 2 if self.audit and item.rule not in {"PAL001", "PAL002"} else 1,
                          "code": item.rule, "source": "pyalamode", "message": item.reason + "\n" + item.remediation, "data": data}
            if item.first_binding:
                first_path, first_line = item.first_binding.rsplit(":", 1)
                first = Path(first_path).resolve()
                if first.is_relative_to(self.root):
                    first_text = self.current.sources.get(str(first), "")
                    start = position(first_text, int(first_line), 1)
                    lsp_diagnostic["relatedInformation"] = [{"location": {"uri": first.as_uri(), "range": {"start": start, "end": start}}, "message": "first binding: " + item.first_binding}]
            uri = path.as_uri()
            self.diagnostics.append({"uri": uri, **lsp_diagnostic})
            grouped.setdefault(uri, []).append(lsp_diagnostic)
        uris = set(grouped) | self.published | {Path(path).as_uri() for path in self.documents}
        for uri in sorted(uris):
            payload = {"uri": uri, "diagnostics": grouped.get(uri, [])}
            version = self.documents.get(str(Path(unquote(urlsplit(uri).path)).resolve()), {}).get("version")
            if version is not None:
                payload["version"] = version
            self.notifications.append({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics", "params": payload})
        self.published = set(grouped) | {Path(path).as_uri() for path in self.documents}
        return self.current

    def _document(self, params):
        document = params.get("textDocument")
        if type(document) is not dict:
            raise ProtocolError("textDocument is required")
        path = uri_path(document.get("uri"), self.root, python=True)
        return str(path), document

    def _point(self, params):
        path, _ = self._document(params)
        text = self.current.sources.get(path)
        if text is None:
            raise ProtocolError("document is unavailable in this project snapshot")
        point = params.get("position")
        _offset(text, point)
        return path, text, point

    def _region_at(self, path, point):
        found = [row for row in self.regions if row["uri"] == Path(path).as_uri() and _contains(row["range"], point)]
        return min(found, key=lambda row: (row["range"]["end"]["line"] - row["range"]["start"]["line"], -row["range"]["start"]["line"])) if found else None

    def _edges(self):
        edges = []
        for file in self.current.result.results:
            text = self.current.sources.get(file.path, "")
            _, tree = _definitions(text)
            if tree is None:
                continue
            calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
            for contract in file.contracts:
                for edge in contract.failure_edges:
                    matching = [node for node in calls if node.lineno == edge["line"] and node.col_offset + 1 == edge["column"]]
                    for call in matching:
                        edges.append((file.path, node_range(text, call.func), edge["target"]))
        return edges

    def _target_location(self, target):
        if "::" not in target:
            return None
        path, name = target.rsplit("::", 1)
        node = self.nodes.get(path, {}).get(name)
        if node is None or not Path(path).is_relative_to(self.root):
            return None
        return {"uri": Path(path).as_uri(), "range": _selection(self.current.sources[path], node)}

    def _targets(self, path, point):
        targets = {target for file, range_, target in self._edges() if file == path and _contains(range_, point)}
        for region in self.regions:
            if region["kind"] == "function" and region["uri"] == Path(path).as_uri() and _contains(region["selectionRange"], point):
                targets.add(path + "::" + region["name"])
        return targets

    def handle(self, method, params=None):
        params = {} if params is None else params
        if type(params) is not dict:
            raise ProtocolError("params must be an object")
        if method == "exit":
            self.exited = True
            return None
        if method == "initialize":
            if self.initialized or self.shutdown:
                raise ProtocolError("server is already initialized")
            root_uri = params.get("rootUri")
            if root_uri is None or uri_path(root_uri, self.root, directory=True) != self.root:
                raise ProtocolError("initialize rootUri must match launch root")
            self.initialized = True
            return {"capabilities": {"positionEncoding": "utf-16", "textDocumentSync": {"openClose": True, "change": 1, "save": {"includeText": False}},
                    "hoverProvider": True, "definitionProvider": True, "referencesProvider": True,
                    "documentSymbolProvider": True, "codeActionProvider": True,
                    "experimental": {"pyalamode": {"schema": 1, "target": TARGET, "pythonExecutable": sys.executable,
                        "pythonVersion": list(sys.version_info[:3]), "platform": sys.platform, "root": str(self.root),
                        "filesystemEncoding": sys.getfilesystemencoding(), "filesystemErrors": sys.getfilesystemencodeerrors()}}},
                    "serverInfo": {"name": "pyalamode", "version": CHECKER_VERSION}}
        if not self.initialized:
            raise ProtocolError("server must be initialized", -32002)
        if method == "shutdown":
            self.shutdown = True
            return None
        if self.shutdown:
            raise ProtocolError("server is shut down", -32600)
        if method == "$/cancelRequest":
            return None
        if method in {"textDocument/didOpen", "textDocument/didChange", "textDocument/didClose", "textDocument/didSave"}:
            path, document = self._document(params)
            if method == "textDocument/didClose":
                if path not in self.documents:
                    raise ProtocolError("document is not open")
                del self.documents[path]
            elif method == "textDocument/didSave":
                if path not in self.documents or "text" in params:
                    raise ProtocolError("save requires an open document and no replacement text")
            else:
                version = document.get("version")
                if type(version) is not int or version < 0:
                    raise ProtocolError("document version must be a nonnegative integer")
                if method == "textDocument/didOpen":
                    if path in self.documents or document.get("languageId") != "python":
                        raise ProtocolError("open requires a new Python document")
                    text = document.get("text")
                else:
                    if path not in self.documents or version <= self.documents[path]["version"]:
                        raise ProtocolError("change requires an open document and increasing version")
                    changes = params.get("contentChanges")
                    if type(changes) is not list or len(changes) != 1 or type(changes[0]) is not dict or set(changes[0]) != {"text"}:
                        raise ProtocolError("one full-text replacement is required")
                    text = changes[0]["text"]
                if type(text) is not str or len(text.encode("utf-8")) > MAX_BODY:
                    raise ProtocolError("document text must be bounded decoded UTF-8")
                self.documents[path] = {"text": text, "version": version}
            self.refresh()
            return None
        known = {"initialized", "pyalamode/project", "pyalamode/explain", "pyalamode/preview", "pyalamode/guardLocation",
                 "textDocument/hover", "textDocument/definition", "textDocument/references", "textDocument/documentSymbol", "textDocument/codeAction"}
        if method not in known:
            raise ProtocolError("unsupported method: " + method, -32601)
        if method == "pyalamode/project" and "audit" in params:
            if type(params["audit"]) is not bool:
                raise ProtocolError("audit must be boolean")
            self.audit = params["audit"]
        self.refresh()
        if method == "initialized":
            return None
        if method == "pyalamode/project":
            return {"schema": 1, "snapshot": self.current.snapshot, "freshness": self.current.freshness,
                    "inputs": self.current.inputs, "report": self.current.result.to_dict(),
                    "documents": [{"uri": Path(path).as_uri(), "version": entry["version"]} for path, entry in sorted(self.documents.items())],
                    "regions": self.regions, "diagnostics": self.diagnostics}
        if method == "pyalamode/explain":
            from .cli import explain_symbol
            if type(params.get("symbol")) is not str:
                raise ProtocolError("symbol must be text")
            return explain_symbol(params["symbol"], root=self.root, snapshot=self.current)
        if method == "pyalamode/preview":
            return self.preview(params)
        if method == "pyalamode/guardLocation":
            return self.guard_location(params)
        if method == "textDocument/documentSymbol":
            path, _ = self._document(params)
            return [{"name": row["name"], "detail": row["mode"] + ": " + str((row["contract"] or {}).get("source_evidence", "")),
                     "kind": 12 if row["kind"] in {"function", "unsafe"} else 5,
                     "range": row["range"], "selectionRange": row["selectionRange"]}
                    for row in self.regions if row["uri"] == Path(path).as_uri()]
        if method == "textDocument/codeAction":
            path, _ = self._document(params)
            text = self.current.sources.get(path, "")
            range_ = params.get("range")
            if type(range_) is not dict or set(range_) != {"start", "end"}:
                raise ProtocolError("code action range is required")
            start, end = _offset(text, range_["start"]), _offset(text, range_["end"])
            if end < start:
                raise ProtocolError("range end precedes start")
            version = self.documents.get(path, {}).get("version")
            if version is None:
                return []
            actions = []
            for item in self.diagnostics:
                if item["uri"] != Path(path).as_uri() or item["code"] not in {"PAL101", "PAL250"}:
                    continue
                point = _offset(text, item["range"]["start"])
                if not start <= point <= end:
                    continue
                request = {"uri": item["uri"], "version": version, "snapshot": self.current.snapshot,
                           "diagnosticIndex": item["data"]["diagnosticIndex"]}
                try:
                    preview = self.preview(request)
                except ProtocolError:
                    continue
                actions.append({"title": "Preview " + preview["title"], "command": "pyalamode.preview", "arguments": [request]})
            return actions
        path, text, point = self._point(params)
        if method == "textDocument/hover":
            row = self._region_at(path, point)
            if row is None:
                return None
            contract = row["contract"] or {}
            file = next((file for file in self.current.result.results if file.path == path), None)
            payload = {"boundary": row["name"], "mode": row["mode"], "freshness": self.current.freshness,
                       "contract": contract, "initialization": file.initialization_evidence if file else "unavailable",
                       "setup": file.setup_observations if file else [], "guards": self.current.result.guarded_exports,
                       "debug_coverage": self.current.result.debug_coverage}
            return {"contents": {"kind": "markdown", "value": "Pyalamode authored boundary `" + row["name"] + "`\n\n```json\n" + json.dumps(payload, indent=2, sort_keys=True) + "\n```"}, "range": row["range"]}
        targets = self._targets(path, point)
        if method == "textDocument/definition":
            locations = [self._target_location(target) for target in sorted(targets)]
        else:
            if type(params.get("context")) is not dict or type(params["context"].get("includeDeclaration")) is not bool:
                raise ProtocolError("references context.includeDeclaration is required")
            locations = [{"uri": Path(file).as_uri(), "range": range_} for file, range_, target in self._edges() if target in targets]
            if params["context"]["includeDeclaration"]:
                locations.extend(self._target_location(target) for target in sorted(targets))
        return list({json.dumps(location, sort_keys=True): location for location in locations if location}.values())

    def preview(self, params):
        path = str(uri_path(params.get("uri"), self.root, python=True))
        entry = self.documents.get(path)
        if (entry is None or type(params.get("version")) is not int or params["version"] != entry["version"]
                or params.get("snapshot") != self.current.snapshot or self.current.freshness.startswith("stale")):
            raise ProtocolError("preview is stale or document is not open", -32801)
        index = params.get("diagnosticIndex")
        if type(index) is not int:
            raise ProtocolError("diagnosticIndex must be an integer")
        item = next((item for item in self.diagnostics if item["uri"] == Path(path).as_uri() and item["data"]["diagnosticIndex"] == index), None)
        if item is None or item["code"] not in {"PAL101", "PAL250"}:
            raise ProtocolError("no supported safe preview for this diagnostic")
        text = entry["text"]
        nodes, tree = _definitions(text)
        node = nodes.get(item["data"]["boundary"])
        if not isinstance(node, ast.FunctionDef):
            raise ProtocolError("preview requires a participating function")
        contract = next((row["contract"] for row in self.regions if row["uri"] == Path(path).as_uri() and row["name"] == item["data"]["boundary"]), None)
        forbidden = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda, ast.If, ast.For, ast.AsyncFor,
                     ast.While, ast.Try, ast.With, ast.AsyncWith, ast.Match, ast.Import, ast.ImportFrom, ast.Global,
                     ast.Nonlocal, ast.NamedExpr, ast.Delete, ast.AugAssign, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        if any(isinstance(child, forbidden) for statement in node.body for child in ast.walk(statement)):
            raise ProtocolError("preview refuses captures, nested scopes, control flow and dynamic bindings")
        if not contract or any(contract.get(key) for key in ("captures", "callable_targets", "callable_defaults", "return_callable_targets", "capability_parameters", "callable_arguments", "callable_dependencies")):
            raise ProtocolError("preview requires closed stable data without callbacks/capabilities/captures")
        if any("Callable[" in kind or "Effectful[" in kind or "Capability" in kind for kind in [*contract["parameters"].values(), contract["returns"] or ""]):
            raise ProtocolError("preview requires a data-only contract")
        boundary_items = [other for other in self.diagnostics if other["uri"] == item["uri"] and other["data"]["boundary"] == item["data"]["boundary"]]
        if len(boundary_items) != 1:
            raise ProtocolError("preview requires exactly one supported boundary finding")
        names = {child.id for child in ast.walk(node) if isinstance(child, ast.Name)} | {arg.arg for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)}
        def fresh(base):
            candidate, suffix = base, 2
            while candidate in names:
                candidate = base + "_" + str(suffix)
                suffix += 1
            return candidate
        line = item["data"]["authored"]["line"]
        edits = []
        if item["code"] == "PAL250":
            statement = next((statement for statement in node.body if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and statement.lineno == line), None)
            if statement is None:
                raise ProtocolError("preview requires a direct discarded persistent update")
            start = position(text, statement.lineno, statement.col_offset + 1)
            edits = [{"range": {"start": start, "end": start}, "newText": fresh("updated_value") + " = "}]
            title = "retain the persistent update in a fresh binding"
            limits = "The original return remains unchanged. The new value is unused until you intentionally choose how to use it; this preview does not update the receiver or change failures."
        else:
            if not node.body or not isinstance(node.body[-1], ast.Return) or sum(isinstance(statement, ast.Return) for statement in node.body) != 1:
                raise ProtocolError("SSA preview requires one final return")
            for statement in node.body:
                if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant) and type(statement.value.value) is str:
                    continue
                if not isinstance(statement, (ast.Assign, ast.AnnAssign, ast.Return, ast.Pass)):
                    raise ProtocolError("SSA preview only supports straight-line data statements")
                targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target] if isinstance(statement, ast.AnnAssign) else []
                if targets and (len(targets) != 1 or not isinstance(targets[0], ast.Name)):
                    raise ProtocolError("SSA preview requires one simple local target")
            second = next((statement for statement in node.body if isinstance(statement, ast.Assign) and statement.lineno == line), None)
            if second is None or len(second.targets) != 1 or not isinstance(second.targets[0], ast.Name):
                raise ProtocolError("SSA preview requires a second simple assignment")
            name = second.targets[0].id
            parameter_names = {arg.arg for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)}
            assignments = [statement for statement in node.body if isinstance(statement, (ast.Assign, ast.AnnAssign)) and any(isinstance(target, ast.Name) and target.id == name for target in (statement.targets if isinstance(statement, ast.Assign) else [statement.target]))]
            if name in parameter_names or len(assignments) != 2 or assignments[-1] is not second:
                raise ProtocolError("SSA preview requires exactly two non-parameter local bindings")
            annotations = [child.annotation for child in ast.walk(node) if isinstance(child, ast.AnnAssign)]
            if any(isinstance(child, ast.Name) and child.id == name for annotation in annotations for child in ast.walk(annotation)):
                raise ProtocolError("SSA preview refuses same-name annotation dependencies")
            # Alias copies are outside this deliberately closed rename contract.
            if any(isinstance(statement, (ast.Assign, ast.AnnAssign)) and isinstance(statement.value, ast.Name) and statement.value.id == name for statement in node.body):
                raise ProtocolError("SSA preview refuses alias assignments")
            renamed = fresh(name + "_2")
            changed = [second.targets[0]]
            for statement in node.body[node.body.index(second) + 1:]:
                changed.extend(child for child in ast.walk(statement) if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load) and child.id == name)
            edits = [{"range": node_range(text, child), "newText": renamed} for child in changed]
            title = "split the second local binding and subsequent reads"
            limits = "Exactly two straight-line data bindings; the second RHS still reads the first value. Captures, branches, aliases, callbacks and dynamic names are refused. Supported caller/dependency assumptions remain."
        after = text
        for edit in sorted(edits, key=lambda edit: _offset(text, edit["range"]["start"]), reverse=True):
            start, end = _offset(text, edit["range"]["start"]), _offset(text, edit["range"]["end"])
            after = after[:start] + edit["newText"] + after[end:]
        overlays = {**self.documents, path: {"text": after, "version": entry["version"]}}
        candidate = check_snapshot([self.root], root=self.root, overlays=overlays, cache=False)
        if candidate.result.status or candidate.freshness.startswith("stale"):
            raise ProtocolError("candidate does not pass the complete current strict project gate")
        new_contract = next((asdict(contract_) for file in candidate.result.results for contract_ in file.contracts if file.path == path and contract_.name == contract["name"]), None)
        retained = ("trust", "external_assumptions", "failures", "definition_failures", "effect_bound", "required_effects", "operations", "operation_contracts")
        if new_contract is None or any(new_contract[key] != contract[key] for key in retained):
            raise ProtocolError("candidate changes retained trust/effect/failure/operation dimensions")
        if candidate.inputs["policy_sha256"] != self.current.inputs["policy_sha256"] or candidate.inputs["product_artifacts"] != self.current.inputs["product_artifacts"] or candidate.inputs["integration_inputs"] != self.current.inputs["integration_inputs"]:
            raise ProtocolError("preview inputs changed during candidate checking", -32801)
        original_sources = {source: dict(row) for source, row in self.current.inputs["sources"].items()}
        candidate_sources = {source: dict(row) for source, row in candidate.inputs["sources"].items()}
        if path in original_sources and path in candidate_sources:
            original_sources[path].pop("sha256")
            candidate_sources[path].pop("sha256")
        if original_sources != candidate_sources:
            raise ProtocolError("preview source/dependency inputs changed during candidate checking", -32801)
        return {"title": title, "uri": Path(path).as_uri(), "version": entry["version"], "snapshot": self.current.snapshot,
                "before": text, "after": after, "diff": "".join(difflib.unified_diff(text.splitlines(keepends=True), after.splitlines(keepends=True), fromfile=path, tofile=path + " (preview)")),
                "edits": edits, "status": candidate.result.status,
                "remainingDiagnostics": [asdict(item) for file in candidate.result.results for item in file.diagnostics], "limits": limits}

    def guard_location(self, params):
        artifact = uri_path(params.get("artifactUri"), self.root, directory=True)
        evidence_path = artifact / "pyalamode-evidence.json"
        if not evidence_path.is_file() or not evidence_path.resolve().is_relative_to(artifact):
            raise ProtocolError("artifact has no local evidence")
        try:
            if evidence_path.stat().st_size > MAX_BODY:
                raise ProtocolError("artifact evidence exceeds the bounded local payload")
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            if type(evidence) is not dict:
                raise ProtocolError("artifact evidence must be an object")
            if evidence.get("verified") is not True or evidence.get("status") != 0:
                raise ProtocolError("artifact has no successful strict gate")
            inventory = evidence.get("artifact_files")
            if type(inventory) is not dict or not inventory or any(type(relative) is not str or type(digest) is not str or not re.fullmatch("[0-9a-f]{64}", digest) for relative, digest in inventory.items()):
                raise ProtocolError("artifact requires a nonempty exact byte inventory")
            for relative, digest in inventory.items():
                path = (artifact / relative).resolve()
                if not path.is_relative_to(artifact) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    raise ProtocolError("artifact bytes are stale or modified", -32801)
            selected = next((row for row in evidence["guarded_exports"] if row["public_boundary"] == params.get("publicBoundary") and row["generated"]), None)
            if selected is None:
                raise ProtocolError("public boundary has no generated guard coverage")
            expected = next((row for row in self.current.result.guarded_exports if row["public_boundary"] == params.get("publicBoundary")), None)
            if (expected is None or selected != {**expected, "generated": True}
                    or evidence.get("boundary_guards") != self.current.result.boundary_guards):
                raise ProtocolError("artifact guard coverage does not match the current selected plan")
            phase = params.get("phase")
            name = params.get("name")
            if phase not in {"argument", "return", "local"} or (name is not None and type(name) is not str):
                raise ProtocolError("unsupported guard phase/name")
            module, boundary = selected["original_boundary"].split(":", 1)
            from .checker import _module_name
            file = next((file for file in self.current.result.results if _module_name(file.path, self.root) == module), None)
            old_file = next((old for old in evidence["files"] if file and old["path"] == file.path), None)
            contract = next((contract for contract in file.contracts if contract.name == boundary), None) if file else None
            if (contract is None or old_file is None or self.current.result.status or self.current.freshness.startswith("stale")
                    or old_file["fingerprint"] != file.fingerprint or evidence["product_artifacts"] != self.current.inputs["product_artifacts"]):
                raise ProtocolError("authored source/policy/dependency evidence is stale", -32801)
            source_relative = Path(file.path).relative_to(self.root).as_posix()
            facade_relative = "pyalamode_exports/" + source_relative
            required = {source_relative, facade_relative, "pyalamode_exports/__init__.py"}
            if not required <= set(inventory):
                raise ProtocolError("artifact inventory omits the authored source or selected facade")
            from .guardgen import debug_source, facade_source, record_schemas
            records = record_schemas(self.current.result.results)
            text = self.current.sources[file.path]
            expected_source = debug_source(text, file, records).encode() if evidence["boundary_guards"] == "debug" else Path(file.path).read_bytes()
            selected_contracts = [next(contract_ for contract_ in file.contracts if contract_.name == row["original_boundary"].split(":", 1)[1]) for row in self.current.result.guarded_exports if row["original_boundary"].split(":", 1)[0] == module]
            expected_facade = facade_source(text, module, selected_contracts, records).encode()
            if (inventory[source_relative] != hashlib.sha256(expected_source).hexdigest()
                    or inventory[facade_relative] != hashlib.sha256(expected_facade).hexdigest()):
                raise ProtocolError("artifact selected source/facade bytes differ from current guard generation", -32801)
            line = contract.line
            if phase == "argument":
                if name not in selected["parameters"]:
                    raise ProtocolError("argument is outside generated guard coverage")
            elif phase == "return":
                if name is not None:
                    raise ProtocolError("return phase has no name")
                if params.get("authoredLine") is not None:
                    if evidence["boundary_guards"] != "debug":
                        raise ProtocolError("export return navigates to authored declaration")
                    requested = params["authoredLine"]
                    node = self.nodes[file.path][boundary]
                    if type(requested) is not int or not any(isinstance(child, ast.Return) and child.lineno == requested for child in ast.walk(node)):
                        raise ProtocolError("return line is outside authored coverage")
                    line = requested
            else:
                coverage = next((row for row in evidence["debug_coverage"] if row["path"] == file.path and row["name"] == boundary and row["generated"]), None)
                expected_coverage = next((row for row in self.current.result.debug_coverage if row["path"] == file.path and row["name"] == boundary), None)
                if expected_coverage is None or coverage != {**expected_coverage, "generated": True}:
                    raise ProtocolError("artifact debug coverage differs from the current selected plan")
                assertion = next((row for row in coverage["locals"] if row["name"] == name and row["line"] == params.get("authoredLine")), None) if coverage else None
                if assertion is None:
                    raise ProtocolError("local assertion is outside debug guard coverage")
                line = assertion["line"]
            text = self.current.sources[file.path]
            start = position(text, line, 1)
            end = position(text, line, len(_lines(text)[line - 1]) + 1, "unicode-codepoints")
            return {"location": {"uri": Path(file.path).as_uri(), "range": {"start": start, "end": end}},
                    "boundary": selected["original_boundary"], "phase": phase, "name": name,
                    "freshness": self.current.freshness, "snapshot": self.current.snapshot, "coverage": selected["coverage"]}
        except ProtocolError:
            raise
        except (OSError, UnicodeError, ValueError, KeyError, TypeError, StopIteration):
            raise ProtocolError("unsupported or malformed artifact evidence") from None


def _frame(value):
    body = json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n\r\n" + body


def _read_frame(stream):
    headers, length, total = {}, None, 0
    while True:
        line = stream.readline(MAX_HEADER + 1)
        if not line:
            if not total:
                return None
            raise EOFError("truncated header")
        total += len(line)
        if total > MAX_HEADER or not line.endswith(b"\r\n"):
            raise ProtocolError("malformed or oversized framing header", -32700)
        if line == b"\r\n":
            break
        try:
            key, value = line[:-2].decode("ascii").split(":", 1)
        except (UnicodeError, ValueError):
            raise ProtocolError("framing headers must be ASCII name/value pairs", -32700) from None
        key, value = key.lower(), value.strip()
        if key in headers:
            raise ProtocolError("duplicate framing header", -32700)
        headers[key] = value
    value = headers.get("content-length", "")
    if not value.isascii() or not value.isdecimal() or len(value) > 9 or not 0 < int(value) <= MAX_BODY:
        raise ProtocolError("invalid or oversized Content-Length", -32700)
    length = int(value)
    chunks, remaining = [], length
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError("truncated body")
        chunks.append(chunk)
        remaining -= len(chunk)
    body = b"".join(chunks)
    content = headers.get("content-type", "application/vscode-jsonrpc; charset=utf-8").lower()
    if "charset=" in content and content.split("charset=", 1)[1].strip() not in {"utf-8", "utf8"}:
        return ProtocolError("only UTF-8 Content-Type is supported", -32700)
    try:
        def reject_constant(value):
            raise ValueError("non-JSON constant: " + value)
        return json.loads(body.decode("utf-8"), parse_constant=reject_constant)
    except (UnicodeError, ValueError, RecursionError):
        return ProtocolError("invalid UTF-8 JSON body", -32700)


def serve(*, root, input_stream=None, output_stream=None):
    stream = input_stream or sys.stdin.buffer
    output = output_stream or sys.stdout.buffer
    try:
        session = EditorSession(root)
    except ProtocolError as error:
        print(str(error), file=sys.stderr)
        return 2
    def send(value):
        output.write(_frame(value))
        output.flush()
    while not session.exited:
        try:
            message = _read_frame(stream)
        except EOFError:
            return 2
        except ProtocolError as error:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": error.code, "message": str(error)}})
            return 2
        if message is None:
            break
        if isinstance(message, ProtocolError):
            send({"jsonrpc": "2.0", "id": None, "error": {"code": message.code, "message": str(message)}})
            continue
        identity = message.get("id") if type(message) is dict else None
        request = type(message) is dict and "id" in message
        valid_id = type(identity) in {str, int} or identity is None
        envelope = type(message) is dict and message.get("jsonrpc") == "2.0" and type(message.get("method")) is str and (not request or valid_id)
        notification = envelope and not request
        try:
            if not envelope:
                raise ProtocolError("invalid JSON-RPC request", -32600)
            result = session.handle(message["method"], message.get("params"))
            if request:
                send({"jsonrpc": "2.0", "id": identity, "result": result})
        except (ProtocolError, OSError, UnicodeError, ValueError, RecursionError) as error:
            code = error.code if isinstance(error, ProtocolError) else -32603
            if not notification:
                send({"jsonrpc": "2.0", "id": identity if envelope and valid_id else None, "error": {"code": code, "message": str(error)[:1000]}})
            else:
                send({"jsonrpc": "2.0", "method": "window/logMessage", "params": {"type": 1, "message": str(error)[:1000]}})
        for notification in session.drain_notifications():
            send(notification)
    return 0 if session.shutdown else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pyalamode local static editor server")
    parser.add_argument("--stdio", action="store_true", required=True)
    parser.add_argument("--root", required=True)
    args = parser.parse_args(argv)
    return serve(root=args.root)


if __name__ == "__main__":
    raise SystemExit(main())
