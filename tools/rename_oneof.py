"""Apply the variant -> oneof rename to a pre-rename tree, reproducibly.

Run from a repository root whose `pyalamode/variants.py` still exists, then
commit the result before merging the `sum-types` branch. Lines this tool
rewrites then match the branch, so the merge only conflicts where the same
line also carries real semantic changes on both sides.

    python tools/rename_oneof.py            # rewrite in place
    python tools/rename_oneof.py --check    # list files that would change
    python tools/rename_oneof.py --resolve  # after `git -c merge.conflictStyle=diff3 merge`

`--resolve` settles a conflict region automatically only when one side is
exactly the rename of the base, i.e. that side did nothing but rename those
lines. The result is the other side with the rename applied. Every other
region is left for review.

Genuine M10 history keeps its spelling: migration's legacy product inventory
still names variants.py, and the legacy reader accepts the `variant` boundary
kind and `selected_variants` coverage key.
"""

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
TREES = ("pyalamode", "tests", "benchmarks", "examples")

# Exact edits applied before the generic identifier mapping, in order.
LITERAL = {
    "pyalamode/checker.py": [
        ('DOMAIN_PRIMITIVES = frozenset({"variant", "case",',
         'DOMAIN_DECORATORS = frozenset({"oneof"})\nDOMAIN_PRIMITIVES = frozenset({"oneof", "case",'),
        ('{"variant"}) for d in node.decorator_list', 'DOMAIN_DECORATORS) for d in node.decorator_list'),
        ('self._primitive_identity(node.decorator_list[0], {"variant"})', 'self._primitive_identity(node.decorator_list[0], DOMAIN_DECORATORS)'),
        ('"variants" if name in DOMAIN_PRIMITIVES else None)', '"sums" if name in DOMAIN_PRIMITIVES else None)'),
        ('"boundaries", "variants", "failures", "standard"', '"boundaries", "sums", "failures", "standard"'),
        ('"pyalamode.variants": "variants.py"', '"pyalamode.sums": "sums.py"'),
        ('inside a closed @variant domain', 'inside a closed @oneof domain'),
    ],
    "pyalamode/model.py": [('"standard_contracts.py", "variants.py",', '"standard_contracts.py", "sums.py",')],
    "pyalamode/__init__.py": [("from .variants import variant, case,", "from .sums import oneof, case,")],
    "pyalamode/migration.py": [
        ('\nPRODUCTS = LEGACY_PRODUCTS | {', '\nPRODUCTS = (LEGACY_PRODUCTS - {"variants.py"}) | {"sums.py", '),
        ('''def _logical(value):
    _shape(value, {"kind", "selector", "qualified_name"})
    if value["kind"] not in {"module", "function", "record", "variant"}:''',
         '''def _logical(value, legacy=False):
    _shape(value, {"kind", "selector", "qualified_name"})
    # Genuine M10 history spells closed sums "variant"; current files use "oneof".
    if value["kind"] not in {"module", "function", "record", "variant" if legacy else "oneof"}:'''),
        ('selected_records selected_variants".split()))', 'selected_records".split()) | {"selected_variants" if legacy else "selected_oneofs"})'),
        ('''                    "selected_variants": sum(b["kind"] == "variant" and b["selected"] for b in rows)}
        if value["coverage"] != expected''',
         '''                    ("selected_variants" if legacy else "selected_oneofs"): sum(b["kind"] == ("variant" if legacy else "oneof") and b["selected"] for b in rows)}
        if value["coverage"] != expected'''),
        ('        _logical(logical)\n', '        _logical(logical, legacy=legacy)\n'),
        ('        _logical(row["logical_boundary"])\n', '        _logical(row["logical_boundary"], legacy=legacy)\n'),
        ('        _logical(birth["logical_boundary"])\n', '        _logical(birth["logical_boundary"], legacy=legacy)\n'),
    ],
    "benchmarks/m06_domains.py": [('"pyalamode/variants.py"', '"pyalamode/sums.py"')],
}
# Module imports of the runtime catalog in tests and benchmarks.
MODULE_IMPORTS = [("import records, variants, collections", "import records, sums, collections"),
                  ("import boundaries, variants, records", "import boundaries, sums, records"),
                  ("import boundaries, records, variants", "import boundaries, records, sums"),
                  ("variants._", "sums._")]
# Generic identifier mapping, applied in order on every Python file and the README.
PAIRS = [(r"pyalamode\.variants\b", "pyalamode.sums"), (r"from \. import variants as _variants", "from . import sums as _sums"),
         (r"from \.variants import", "from .sums import"), (r"from pyalamode import variants\b", "from pyalamode import sums"),
         (r"\b_variants\b", "_sums"), (r"\b_VARIANTS\b", "_ONEOFS"), (r"\b_variant_info\b", "_oneof_info"), (r"\bvariant_info\b", "oneof_info"),
         (r"\bVariantInfo\b", "OneOfInfo"), (r"\breplaced_variants\b", "replaced_oneofs"), (r"\bselected_variants\b", "selected_oneofs"),
         (r"\bvariant_class\b", "oneof_class"), (r"\bvariant_declarations\b", "oneof_declarations"), (r"\bprepare_variant\b", "prepare_oneof"),
         (r"\bdiscover_variants\b", "discover_oneofs"), (r"\bVariant\b", "OneOf"), (r"\bvariants\b", "oneofs"), (r"\bvariant\b", "oneof"),
         (r"_variant_", "_oneof_"), (r"_variant\b", "_oneof"), (r"\bvariant_", "oneof_")]
# Lines that must keep historical spelling after the generic mapping.
PROTECTED = {"pyalamode/migration.py": [r"^LEGACY_PRODUCTS = ", r'"variants\.py"', r"Genuine M10", r"selected_variants\" if ", r"\"variant\" if "]}
# Branch-native files mention `variant` only to prove it is gone.
SKIP = {"tests/m06_unions.py", "tests/m06_open.py", "tests/m02_tailrec.py"}

def rewrite(path, text):
    relative = path.relative_to(ROOT).as_posix()
    if relative in SKIP:
        return text
    for old, new in LITERAL.get(relative, []):
        text = text.replace(old, new)
    if relative.startswith(("tests/", "benchmarks/")):
        for old, new in MODULE_IMPORTS:
            text = text.replace(old, new)
    protected = PROTECTED.get(relative, [])
    lines = []
    for line in text.split("\n"):
        if not any(re.search(pattern, line) for pattern in protected):
            # Current inventories were rewritten by LITERAL above; any remaining
            # variants.py names a genuinely shipped historical product file.
            line = line.replace("variants.py", "\0historical\0")
            for pattern, replacement in PAIRS:
                line = re.sub(pattern, replacement, line)
            line = line.replace("\0historical\0", "variants.py")
        lines.append(line)
    # Version strings are a merge decision, not a mechanical rename.
    return "\n".join(lines)


def main(check=False):
    source = ROOT / "pyalamode/variants.py"
    if source.exists() and not check:
        subprocess.run(["git", "mv", str(source), str(ROOT / "pyalamode/sums.py")], check=True)
    files = [p for tree in TREES for p in (ROOT / tree).rglob("*.py") if ".pyalamode-cache" not in p.parts] + [ROOT / "README.md"]
    changed = []
    for path in files:
        original = path.read_text()
        updated = rewrite(path, original)
        if updated != original:
            changed.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_text(updated)
    print("\n".join(changed))
    return 0


def resolve():
    """Settle diff3 conflict regions whose branch side is a pure rename of the base."""
    files = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, text=True, check=True).stdout.split()
    pattern = re.compile(r"<<<<<<< [^\n]*\n(.*?)\|\|\|\|\|\|\| [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)
    remaining = {}
    for name in files:
        path = ROOT / name
        text = path.read_text()

        def settle(match):
            ours, base, theirs = match.groups()
            renamed = rewrite(path, base)
            # Whichever side only renamed the base yields to the other side, renamed.
            if renamed == ours:
                return rewrite(path, theirs)
            if renamed == theirs:
                return rewrite(path, ours)
            return match.group(0)
        text = pattern.sub(settle, text)
        path.write_text(text)
        left = text.count("<<<<<<< ")
        if left:
            remaining[name] = left
        else:
            subprocess.run(["git", "add", name], check=True)
    for name, count in remaining.items():
        print(name + ": " + str(count) + " region(s) need review")
    return 1 if remaining else 0


if __name__ == "__main__":
    arguments = sys.argv[1:]
    sys.exit(resolve() if "--resolve" in arguments else main(check="--check" in arguments))
