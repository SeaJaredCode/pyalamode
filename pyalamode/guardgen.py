"""Generate optional ordinary-Python boundary facades and finite debug assertions.

This module reads parsed source and checker-owned schemas only. It never imports
application modules or evaluates annotations/defaults while building.
"""

import ast
import copy
from pathlib import Path

from .checker import SCALARS, _contract_type, _module_name


def record_schemas(results):
    return {record["schema"]: record for result in results for record in result.records}


def supported_schema(text, records, seen=()):
    try:
        schema = _contract_type(text)
    except (SyntaxError, ValueError, TypeError):
        return False
    if schema.name in SCALARS:
        return True
    if schema.name.startswith("record:"):
        if text in seen or text not in records:
            return False
        return all(supported_schema(t, records, (*seen, text)) for t in records[text]["fields"].values())
    return schema.name in {"tuple", "Vector", "Map", "OrderedMap", "Set"} and all(supported_schema(str(t), records, seen) for t in schema.arguments)


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
        if schema.name == "tuple":
            return "('tuple', " + children + ", " + repr(schema.variadic) + ")"
        if schema.name.startswith("record:"):
            module, name = schema.name[len("record:"):].rsplit(":", 1)
            record = self.records[text]
            fields = "(" + ", ".join("(" + repr(field) + ", " + self.code(kind) + ")" for field, kind in record["fields"].items()) + ("," if len(record["fields"]) == 1 else "") + ")"
            reference = self.local_records.get(text) or self.module(module) + "." + name
            return "('record', " + reference + ", " + fields + ")"
        if schema.name in {"Vector", "Map", "OrderedMap", "Set"}:
            return "(" + repr(schema.name) + ", " + children + ")"
        raise ValueError("guard schemas require supported exact data, not Callable evidence")

    def imports(self):
        return ["import " + name + " as " + alias for name, alias in self.modules.items()]


def _prefix(tree):
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    names.update(n.arg for n in ast.walk(tree) if isinstance(n, ast.arg))
    names.update(n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)))
    for node in ast.walk(tree):
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
        args.defaults = [ast.parse(original + ".__defaults__[" + str(i) + "]", mode="eval").body for i in range(len(args.defaults))]
        args.kw_defaults = [ast.parse(original + ".__kwdefaults__[" + repr(arg.arg) + "]", mode="eval").body if default is not None else None for arg, default in zip(args.kwonlyargs, args.kw_defaults)]
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


def debug_source(source, result, records):
    tree = ast.parse(source)
    prefix = _prefix(tree)
    local_records = {record["schema"]: prefix + "record" + str(index) for index, record in enumerate(result.records)}
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
            if isinstance(node, ast.Return) and contract and supported_schema(contract.returns, records):
                temporary = prefix + "return_" + str(node.lineno)
                output.append(ast.copy_location(ast.Assign(targets=[ast.Name(id=temporary, ctx=ast.Store())], value=node.value or ast.Constant(value=None)), node))
                output.append(assertion(temporary, contract.returns, contract.path + ":" + str(node.lineno) + " " + contract.name + " return", node))
                output.append(ast.copy_location(ast.Return(value=ast.Name(id=temporary, ctx=ast.Load())), node))
                continue
            for field in ("body", "orelse", "finalbody"):
                nested = getattr(node, field, None)
                if isinstance(nested, list):
                    setattr(node, field, visit(nested, qualified, contract))
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
            for record in result.records:
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
    return ast.unparse(ast.fix_missing_locations(tree)) + "\n"


def generate_facades(staging, results, root, selections, sources):
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
        relative = Path(*parts) / "__init__.py" if Path(result.path).name == "__init__.py" else Path(*parts).with_suffix(".py")
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        parent = target.parent
        while parent != package:
            initializer = parent / "__init__.py"
            if not initializer.exists():
                initializer.write_text('"""Selected guarded boundary namespace."""\n')
            parent = parent.parent
        target.write_text(facade_source(sources[result.path], module, contracts, records))
    for path in package.rglob("*.py"):
        artifacts[path.relative_to(staging).as_posix()] = path.read_bytes()
    return artifacts
