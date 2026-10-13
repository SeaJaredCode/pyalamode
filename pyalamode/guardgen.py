"""Generate optional ordinary-Python boundary facades and finite debug assertions.

This module reads parsed source and checker-owned schemas only. It never imports
application modules or evaluates annotations/defaults while building.
"""

import ast
import copy
from pathlib import Path

from .checker import SCALARS, _contract_type, _module_name


def record_schemas(results):
    schemas = {record["schema"]: record for result in results for record in result.records}
    schemas["Record['pyalamode:Failure']"] = {"name": "Failure", "fields": {"category": "str", "message": "str"}}
    for result in results:
        for oneof in result.oneofs:
            schemas[oneof["schema"]] = oneof
            for name, case in oneof["cases"].items():
                schemas[case["schema"]] = {**case, "name": oneof["name"] + "." + name}
    return schemas


def supported_schema(text, records, seen=()):
    try:
        schema = _contract_type(text)
    except (SyntaxError, ValueError, TypeError):
        return False
    if schema.name in SCALARS:
        return True
    if schema.name == "union":
        return all(supported_schema(str(member), records, seen) for member in schema.arguments)
    if schema.name.startswith("oneof:"):
        if text in seen or text not in records:
            return False
        return all(supported_schema(case["schema"], records, (*seen, text)) for case in records[text]["cases"].values())
    if schema.name.startswith(("record:", "case:")):
        if text in seen or text not in records:
            return False
        return all(supported_schema(t, records, (*seen, text)) for t in records[text]["fields"].values())
    return schema.name in {"tuple", "Vector", "Map", "OrderedMap", "Set", "Option", "Result", "Some", "Nothing", "Ok", "Err"} and all(supported_schema(str(t), records, seen) for t in schema.arguments)


class Schemas:
    def __init__(self, records, prefix, local_records=None):
        self.records, self.prefix, self.modules = records, prefix, {}
        self.local_records = local_records or {}

    def module(self, name):
        if not name or any(not part.isidentifier() for part in name.split(".")):
            raise ValueError("guarded modules must have ordinary importable names")
        if name not in self.modules:
            self.modules[name] = self.prefix + "module" + str(len(self.modules))
        return self.modules[name]

    def code(self, text):
        schema = _contract_type(text)
        if schema.name in SCALARS:
            return repr(schema.name)
        children = "(" + ", ".join(self.code(str(t)) for t in schema.arguments) + ("," if len(schema.arguments) == 1 else "") + ")"
        if schema.name == "union":
            return "('union', " + children + ")"
        if schema.name == "tuple":
            return "('tuple', " + children + ", " + repr(schema.variadic) + ")"
        if schema.name.startswith("oneof:"):
            module, name = schema.name[len("oneof:"):].rsplit(":", 1)
            reference = self.local_records.get(text) or self.module(module) + "." + name
            cases = []
            for case_name, case in self.records[text]["cases"].items():
                fields = "(" + ", ".join("(" + repr(field) + ", " + self.code(kind) + ")" for field, kind in case["fields"].items()) + ("," if len(case["fields"]) == 1 else "") + ")"
                cases.append("(" + self.case_reference(case["schema"], case) + ", " + fields + ")")
            return "('oneof', " + reference + ", (" + ", ".join(cases) + ("," if len(cases) == 1 else "") + "))"
        if schema.name.startswith("case:"):
            reference = self.case_reference(text, self.records[text])
            fields = "(" + ", ".join("(" + repr(field) + ", " + self.code(kind) + ")" for field, kind in self.records[text]["fields"].items()) + ("," if len(self.records[text]["fields"]) == 1 else "") + ")"
            return "('case', " + reference + ", " + fields + ")"
        if schema.name.startswith("record:"):
            module, name = schema.name[len("record:"):].rsplit(":", 1)
            record = self.records[text]
            fields = "(" + ", ".join("(" + repr(field) + ", " + self.code(kind) + ")" for field, kind in record["fields"].items()) + ("," if len(record["fields"]) == 1 else "") + ")"
            reference = self.local_records.get(text) or self.module(module) + "." + name
            return "('record', " + reference + ", " + fields + ")"
        if schema.name in {"Vector", "Map", "OrderedMap", "Set", "Option", "Result", "Some", "Nothing", "Ok", "Err"}:
            return "(" + repr(schema.name) + ", " + children + ")"
        raise ValueError("guard schemas require supported exact data, not Callable evidence")

    def case_reference(self, text, case):
        """Nested cases are domain attributes; open-domain extension cases are module attributes."""
        if text in self.local_records:
            return self.local_records[text]
        if "module" in case and "qualname" in case:
            return self.module(case["module"]) + "." + case["qualname"]
        module, domain, name = _contract_type(text).name[len("case:"):].rsplit(":", 2)
        return self.module(module) + "." + domain + "." + name

    def imports(self):
        return ["import " + name + " as " + alias for name, alias in self.modules.items()]


def _prefix(tree):
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    names.update(n.arg for n in ast.walk(tree) if isinstance(n, ast.arg))
    names.update(n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.MatchAs, ast.MatchStar, ast.ExceptHandler)) and node.name:
            names.add(node.name)
        if isinstance(node, ast.MatchMapping) and node.rest:
            names.add(node.rest)
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            names.update(node.names)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update(alias.asname or (alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name) for alias in node.names)
    prefix = "_pyalamode_guard_"
    while any(name.startswith(prefix) for name in names):
        prefix += "x_"
    return prefix


def facade_source(source, module, contracts, records):
    tree = ast.parse(source)
    prefix = _prefix(tree)
    schemas = Schemas(records, prefix)
    original_module = schemas.module(module)
    validate = prefix + "validate"
    lines = []
    for index, contract in enumerate(contracts):
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == contract.name)
        original = prefix + "original" + str(index)
        args = copy.deepcopy(function.args)
        for arg in args.posonlyargs + args.args + args.kwonlyargs:
            arg.annotation = None
        # A @tailrec driver takes *arguments; its declared defaults live on the wrapped body.
        source_function = original + (".__wrapped__" if contract.tail_recursive else "")
        args.defaults = [ast.parse(source_function + ".__defaults__[" + str(i) + "]", mode="eval").body for i in range(len(args.defaults))]
        args.kw_defaults = [ast.parse(source_function + ".__kwdefaults__[" + repr(arg.arg) + "]", mode="eval").body if default is not None else None for arg, default in zip(args.kwonlyargs, args.kw_defaults)]
        signature = ast.FunctionDef(name=contract.name, args=args, body=[ast.Pass()], decorator_list=[])
        signature = ast.unparse(ast.fix_missing_locations(signature)).split("\n", 1)[0]
        lines += [original + " = " + original_module + "." + contract.name, signature]
        for name, kind in contract.parameters.items():
            lines.append("    " + validate + "(" + name + ", " + schemas.code(kind) + ", path=" + repr(module + ":" + contract.name + " argument " + name + " (" + contract.path + ":" + str(contract.line) + ")") + ")")
        positional = [arg.arg for arg in args.posonlyargs + args.args]
        keywords = [arg.arg + "=" + arg.arg for arg in args.kwonlyargs]
        returned = prefix + "result"
        lines.append("    " + returned + " = " + original + "(" + ", ".join(positional + keywords) + ")")
        lines.append("    " + validate + "(" + returned + ", " + schemas.code(contract.returns) + ", path=" + repr(module + ":" + contract.name + " return (" + contract.path + ":" + str(contract.line) + ")") + ")")
        lines.append("    return " + returned)
        lines += [contract.name + ".__wrapped__ = " + original, contract.name + ".__annotations__ = " + original + ".__annotations__.copy()", ""]
    return "\n".join(["\"\"\"Selected guarded public boundaries; original modules remain unguarded.\"\"\"", "from pyalamode.boundaries import validate_data as " + validate, *schemas.imports(), "", *lines]) + "\n"


def debug_source(source, result, records, *, _derivation=None):
    tree = ast.parse(source)
    provenance = _original_origins(source.encode("utf-8"), tree) if _derivation else None
    prefix = _prefix(tree)
    declarations = [*result.records, *result.oneofs]
    local_records = {record["schema"]: prefix + "record" + str(index) for index, record in enumerate(declarations)}
    for oneof in result.oneofs:
        for name, case in oneof["cases"].items():
            if not case.get("extension"):
                local_records[case["schema"]] = local_records[oneof["schema"]] + "." + name
    schemas = Schemas(records, prefix, local_records)
    validate = prefix + "validate"
    contracts = {contract.name: contract for contract in result.contracts}

    def assertion(name, kind, path, authored):
        call = ast.parse(validate + "(" + name + ", " + schemas.code(kind) + ", path=" + repr(path) + ")").body[0]
        return ast.copy_location(call, authored)

    def visit(body, qualified="", contract=None):
        output = []
        for node in body:
            if isinstance(node, ast.FunctionDef):
                name = qualified + node.name
                selected = contracts.get(name)
                node.body = visit(node.body, name + ".", selected)
                if selected:
                    entries = [assertion(arg, kind, selected.path + ":" + str(selected.line) + " " + selected.name + " argument " + arg, node) for arg, kind in selected.parameters.items() if supported_schema(kind, records)]
                    insertion = 1 if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and type(node.body[0].value.value) is str else 0
                    node.body[insertion:insertion] = entries
                output.append(node)
                continue
            # A @tailrec tail call returns the trampoline's private continuation;
            # the driver's final value is the real result, so only plain returns are asserted.
            tail_call = contract is not None and contract.tail_recursive and any(
                isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == contract.name.rsplit(".", 1)[-1] for n in ast.walk(node))
            if isinstance(node, ast.Return) and contract and supported_schema(contract.returns, records) and not tail_call:
                temporary = prefix + "return_" + str(node.lineno)
                output.append(ast.copy_location(ast.Assign(targets=[ast.Name(id=temporary, ctx=ast.Store())], value=node.value or ast.Constant(value=None)), node))
                output.append(assertion(temporary, contract.returns, contract.path + ":" + str(node.lineno) + " " + contract.name + " return", node))
                output.append(ast.copy_location(ast.Return(value=ast.Name(id=temporary, ctx=ast.Load())), node))
                continue
            for field in ("body", "orelse", "finalbody"):
                nested = getattr(node, field, None)
                if isinstance(nested, list):
                    setattr(node, field, visit(nested, qualified, contract))
            for handler in getattr(node, "handlers", []):
                handler.body = visit(handler.body, qualified, contract)
            for case in getattr(node, "cases", []):
                case.body = visit(case.body, qualified, contract)
            output.append(node)
            if contract and isinstance(node, (ast.Assign, ast.AnnAssign)):
                for item in contract.data_assertions:
                    if item["line"] == node.lineno and supported_schema(item["schema"], records):
                        output.append(assertion(item["name"], item["schema"], contract.path + ":" + str(node.lineno) + " " + contract.name + " local " + item["name"], node))
        return output

    tree.body = visit(tree.body)
    aliased = []
    for node in tree.body:
        aliased.append(node)
        if isinstance(node, ast.ClassDef):
            for record in declarations:
                if record["name"] == node.name:
                    aliased.append(ast.copy_location(ast.Assign(targets=[ast.Name(id=local_records[record["schema"]], ctx=ast.Store())], value=ast.Name(id=node.name, ctx=ast.Load())), node))
    tree.body = aliased
    # Imported record dependencies are already characterized source dependencies.
    # Resolve aliases when an asserted function is invoked, preserving ordinary
    # module initializer order and avoiding a second import of script __main__.
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and any(isinstance(child, ast.Name) and child.id == validate for child in ast.walk(node)):
            insertion = 1 if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and type(node.body[0].value.value) is str else 0
            node.body[insertion:insertion] = [ast.parse(line).body[0] for line in schemas.imports()]
    imports = [ast.parse("from pyalamode.boundaries import validate_data as " + validate).body[0]]
    insertion = 1 if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and type(tree.body[0].value.value) is str else 0
    while insertion < len(tree.body) and isinstance(tree.body[insertion], ast.ImportFrom) and tree.body[insertion].module == "__future__":
        insertion += 1
    tree.body[insertion:insertion] = imports
    tree = ast.fix_missing_locations(tree)
    if _derivation:
        return _derive(source.encode("utf-8"), tree, provenance, **_derivation)
    return ast.unparse(tree) + "\n"


def _original_origins(raw, tree):
    from . import source_maps as sm
    origins = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            origins[node] = sm.NodeOrigin(sm.ByteSpan(0, len(raw)), "anchor")
        elif getattr(node, "end_lineno", None) is not None:
            origins[node] = sm.NodeOrigin(sm.ByteSpan(
                sm.offset_at(raw, node.lineno, node.col_offset + 1),
                sm.offset_at(raw, node.end_lineno, node.end_col_offset + 1)), "copy")
    return origins


def _derive(raw, tree, original, *, owner, translator, identity, path, role):
    """Assign actual structural node origins before stock unparse/reparse."""
    from . import source_maps as sm
    rows = {}
    def visit(node, path_, inherited):
        origin = original.get(node)
        if origin is None:
            if isinstance(node, ast.stmt) and getattr(node, "end_lineno", None) is not None:
                try:
                    origin = sm.NodeOrigin(sm.ByteSpan(sm.offset_at(raw, node.lineno, node.col_offset + 1),
                        sm.offset_at(raw, node.end_lineno, node.end_col_offset + 1)), "anchor")
                except sm.SourceMapError:
                    origin = inherited
            else: origin = inherited
        rows[path_] = origin
        for name, value in ast.iter_fields(node):
            if isinstance(value, ast.AST): visit(value, path_ + (name,), origin)
            elif type(value) is list:
                for index, child in enumerate(value):
                    if isinstance(child, ast.AST): visit(child, path_ + (name, index), origin)
    visit(tree, (), sm.NodeOrigin(sm.ByteSpan(0, len(raw)), "anchor"))
    return sm.derive_ast(raw, tree, rows, owner=owner, translator=translator,
        source_identity=identity, generated_path=path, generated_role=role)


def debug_derivation(unit, result, records, path=None):
    from .checker import translator_identity
    from . import source_maps as sm
    return debug_source(unit.normalized_text, result, records, _derivation={"owner": unit.owner,
        "translator": translator_identity(), "identity": unit.source_map.generated,
        "path": path or unit.owner.runtime_path, "role": "debug"})


def facade_derivation(unit, module, contracts, records, path):
    """Build a compiler-owned facade AST; every synthetic node is anchored."""
    from .checker import translator_identity
    from . import source_maps as sm
    raw = unit.normalized_bytes
    original_tree = ast.parse(raw, feature_version=(3, 13))
    prefix = _prefix(original_tree)
    schemas = Schemas(records, prefix)
    original_module = schemas.module(module)
    validate = prefix + "validate"
    body, origins = [], {}
    anchor = sm.NodeOrigin(sm.ByteSpan(0, 0), "anchor")
    def add(statement, origin):
        for node in ast.walk(statement): origins[node] = origin
        body.append(statement)
    for index, contract in enumerate(contracts):
        function = next(node for node in original_tree.body if isinstance(node, ast.FunctionDef) and node.name == contract.name)
        span = sm.ByteSpan(sm.offset_at(raw, function.lineno, function.col_offset + 1),
            sm.offset_at(raw, function.end_lineno, function.end_col_offset + 1))
        origin = sm.NodeOrigin(span, "anchor")
        original = prefix + "original" + str(index)
        args = copy.deepcopy(function.args)
        for arg in args.posonlyargs + args.args + args.kwonlyargs: arg.annotation = None
        args.defaults = [ast.parse(original + ".__defaults__[" + str(i) + "]", mode="eval").body for i in range(len(args.defaults))]
        args.kw_defaults = [ast.parse(original + ".__kwdefaults__[" + repr(arg.arg) + "]", mode="eval").body if default is not None else None for arg, default in zip(args.kwonlyargs, args.kw_defaults)]
        add(ast.parse(original + " = " + original_module + "." + contract.name).body[0], origin)
        statements = [ast.parse(validate + "(" + name + ", " + schemas.code(kind) + ", path=" + repr(module + ":" + contract.name + " argument " + name + " (" + contract.path + ":" + str(contract.line) + ")") + ")").body[0] for name, kind in contract.parameters.items()]
        returned = prefix + "result"
        call = ast.Call(func=ast.Name(id=original, ctx=ast.Load()), args=[ast.Name(id=arg.arg, ctx=ast.Load()) for arg in args.posonlyargs + args.args], keywords=[ast.keyword(arg=arg.arg, value=ast.Name(id=arg.arg, ctx=ast.Load())) for arg in args.kwonlyargs])
        statements += [ast.Assign(targets=[ast.Name(id=returned, ctx=ast.Store())], value=call),
            ast.parse(validate + "(" + returned + ", " + schemas.code(contract.returns) + ", path=" + repr(module + ":" + contract.name + " return (" + contract.path + ":" + str(contract.line) + ")") + ")").body[0],
            ast.Return(value=ast.Name(id=returned, ctx=ast.Load()))]
        add(ast.FunctionDef(name=contract.name, args=args, body=statements, decorator_list=[], returns=None, type_comment=None, type_params=[]), origin)
        for line in (contract.name + ".__wrapped__ = " + original, contract.name + ".__annotations__ = " + original + ".__annotations__.copy()"):
            add(ast.parse(line).body[0], origin)
    header = ast.parse('"""Selected guarded public boundaries; original modules remain unguarded."""\nfrom pyalamode.boundaries import validate_data as ' + validate + "\n" + "\n".join(schemas.imports())).body
    for node in header:
        for child in ast.walk(node): origins[child] = anchor
    tree = ast.fix_missing_locations(ast.Module(body=header + body, type_ignores=[]))
    origins[tree] = anchor
    return _derive(raw, tree, origins, owner=unit.owner, translator=translator_identity(),
        identity=unit.source_map.generated, path=path, role="facade")


def generate_facades(staging, results, root, selections, sources, *, units=None, syntax_modules=None):
    records = record_schemas(results)
    grouped = {}
    for selection in selections:
        module, name = selection.split(":", 1)
        result = next(r for r in results if _module_name(r.path, root) == module)
        grouped.setdefault(module, (result, []))[1].append(next(c for c in result.contracts if c.name == name))
    artifacts = {}
    if not grouped:
        return artifacts
    package = staging / "pyalamode_exports"
    package.mkdir()
    (package / "__init__.py").write_text('"""Explicit selected guarded public boundaries. Original modules remain unguarded."""\n')
    for module, (result, contracts) in grouped.items():
        parts = module.split(".")
        relative = Path(*parts) / "__init__.py" if Path(result.path).name in {"__init__.py", "__init__.pya"} else Path(*parts).with_suffix(".py")
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        parent = target.parent
        while parent != package:
            initializer = parent / "__init__.py"
            if not initializer.exists():
                initializer.write_text('"""Selected guarded boundary namespace."""\n')
            parent = parent.parent
        unit = (units or {}).get(result.path)
        if unit and unit.source_map:
            from .checker import map_bytes
            from . import source_maps as sm
            derivation = facade_derivation(unit, module, contracts, records, target.relative_to(staging).as_posix())
            mapping = sm.compose_maps(unit.source_map, derivation.source_map, source=unit.authored_bytes,
                intermediate=unit.normalized_bytes, generated=derivation.generated_bytes)
            target.write_bytes(derivation.generated_bytes)
            map_path = ".pyalamode/maps/" + target.relative_to(staging).as_posix() + ".map.json"
            map_target = staging / map_path
            map_target.parent.mkdir(parents=True, exist_ok=True)
            raw = map_bytes(mapping)
            map_target.write_bytes(raw)
            artifacts[map_path] = raw
            syntax_modules[module]["facades"].append({"path": target.relative_to(staging).as_posix(),
                "map_path": map_path, "map_sha256": __import__("hashlib").sha256(raw).hexdigest()})
        else:
            target.write_text(facade_source(sources[result.path], module, contracts, records))
    for path in package.rglob("*.py"):
        artifacts[path.relative_to(staging).as_posix()] = path.read_bytes()
    return artifacts
