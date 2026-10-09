# Pyalamode

Pyalamode checks a small functional core in ordinary Python. Milestone 1 provides an installable local library, a static scalar checker, an audit mode, and a checked build that copies accepted Python source. Accepted code runs with normal Python commands and imports.

The supported check/build target is **CPython 3.13.1, standard GIL build, on macOS or Linux** (`cpython-3.13.1`). Other patch versions, free-threaded builds, other interpreters, and Windows fail the target gate. Installing the package under another Python 3.13 patch does not establish target compatibility.

## Install and try it

From this checkout, use a `python3.13` executable whose `--version` reports `Python 3.13.1`:

```sh
python3.13 --version
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
pyalamode check examples/scalar.py
python examples/scalar.py
```

The strict check passes with one selected function and two inspected ordinary same-file calls. Execution prints:

```text
1300
0
```

The calculation in [examples/scalar.py](examples/scalar.py) is ordinary Python:

```python
from pyalamode import fun

@fun
def discounted_total(cents: int, discount_cents: int) -> int:
    remainder = cents - discount_cents
    if remainder < 0:
        result = 0
    else:
        result = remainder
    return result
```

Each continuing branch initializes `result` once. The example's ordinary shell calls it with exact integer literals, then prints the results. Printing and unrelated module initialization receive no purity claim.

Build into a fresh output directory, then execute the copied file:

```sh
pyalamode build examples/scalar.py --output build/scalar-first-use
python build/scalar-first-use/examples/scalar.py
```

The build freshly checks source and writes ordinary `.py` files plus `pyalamode-evidence.json`. It requires at least one participating function and refuses an existing output directory. Choose a new directory for another build. This is a local source artifact; checked package distribution and consumer verification are planned milestones.

The same command interface is available as `python -m pyalamode`.

## See a rejected change

Save this as `bad_scalar.py`:

```python
from pyalamode import fun

@fun
def bad_total(cents: int) -> int:
    total = cents
    total = total + 1
    return total
```

```sh
pyalamode check bad_scalar.py
pyalamode build bad_scalar.py --output build/rejected-scalar
pyalamode explain PAL101
```

Both strict commands fail with `PAL101`, including the first binding's location, and the build produces no artifact. Derive a new name instead of assigning `total` again.

Unknown operations also fail. For example, replacing the function body with `return round(cents)` produces `PAL230`: `round` is outside M1's approved call vocabulary. A call to another `@fun` function inside a selected function is also outside M1; checked call graphs are planned for milestone 2.

To inspect findings without establishing strict evidence:

```sh
pyalamode check --audit bad_scalar.py
pyalamode check --audit --json bad_scalar.py
pyalamode explain PAL230
pyalamode explain abs
pyalamode explain fun
```

Audit reports violations and labels its contracts unverified. Findings alone return status 0 in audit mode. Strict verification failures return 1; tooling, syntax, policy, and unsupported-target failures return 2. Audit still fails for tooling errors. The checker parses application source without importing it or executing annotations, defaults, or decorators.

## What M1 checks

Selected code consists of top-level functions with one statically resolved `@fun` marker, explicit scalar parameter/result annotations, and no defaults, nesting, or other decorators. The marker may be imported from `pyalamode`; exact types are `int`, `bool`, `str`, `bytes`, and `None` (or `NoneType` imported from `types`). An `int` contract excludes `bool` and all `int` subclasses.

| Area | Supported vocabulary |
| --- | --- |
| Statements | Simple local assignments, `if`/`elif`/`else`, `return`, `pass` |
| Integers | Unary `+`/`-`; binary `+`, `-`, `*`, `//`, `%`; same-type comparisons |
| Strings and bytes | Same-type concatenation, equality and ordering |
| Booleans | `not`, `and`, `or`, equality; exact boolean branch conditions |
| Other expressions | Scalar literals and names, conditional expressions, supported `is None`/`is not None` tests |
| Calls | `abs(int)`; `len(str_or_bytes)`; `min`/`max` with two or more positional arguments of one exact `int`, `str`, or `bytes` type |

Floor division and remainder disclose `ZeroDivisionError`. M1 rejects loops, comprehensions, mutable containers, imports inside selected functions, application globals, arbitrary calls, methods, recursion, exceptions written by the user, async code, and unsupported operators. It also rejects analyzed replacement of approved bindings. No configuration is required for this subset. `# mode: fun` and policy-selected modules belong to the planned functional-modules milestone.

## Caller obligations and evidence

A successful strict gate covers the selected scalar functions and inspected direct same-file calls. It does not certify ordinary shell behavior or unrelated module initialization. An empty selection can pass `check`, but establishes no participating export claim; `build` rejects an empty selection.

An ordinary caller must supply the exact declared scalar types. Unknown inputs at an inspected same-file call produce `PAL221`; an ordinary parameter annotation alone does not establish an exact runtime input. Calls from other files and dynamic dispatch remain the caller's responsibility. Public contracts and caller obligations appear in `check --json` and build evidence.

The behavior claim assumes approved builtin, marker, annotation, and function bindings remain unchanged during execution. An unchecked caller that monkey-patches those dependencies or passes a subclass violates that claim's preconditions. The trusted foundation is CPython 3.13.1's supported scalar operations and the Pyalamode marker; arbitrary external operations are excluded. Resource exhaustion and interruption are outside the characterized failures. The checker does not prove termination or business-rule correctness.

At runtime, `fun(function)` returns that same function object. It does not wrap, register, validate arguments, enforce purity, or create checked evidence. Running a file containing `@fun` is ordinary Python execution; a successful current check/build supplies the static evidence. Boundary guards are planned for milestone 4.

Checks store disposable per-file analysis in `.pyalamode-cache/`. The cache includes source bytes, path, policy, checker/operation identities, and target/dependency identities. An unchanged warm check can reuse evidence; editing a file invalidates that file's entry. `check --no-cache` freshly analyzes every selected file, and builds always freshly analyze. Evidence describes the recorded inputs, rather than monitoring a running process.

## Local commands and measurements

```sh
pyalamode check examples/scalar.py --json
pyalamode check examples/scalar.py --no-cache
pyalamode check examples/scalar.py --root . --target cpython-3.13.1
python -m unittest discover -s tests -p 'm01*.py'
python benchmarks/m01_scalar.py --output /tmp/pyalamode-m01-scalar.json
```

The dependency-free benchmark generates a temporary scalar workload, checks an empty cache, repeats with unchanged sources, then edits one file. It verifies every file's expected cache behavior and records timings and Python allocations from `tracemalloc`. Its JSON includes workload size, dependency fanout, Python/build details, OS, hardware, conditions, and per-file cache hits. Run it on the exact supported interpreter; compare measurements only with their recorded conditions. These results do not establish a universal performance target.

The planned roadmap adds functional modules and checked call graphs, persistent collections, records and boundary guards, characterized effects and integrations, editor/migration tools, and checked package distribution. Those capabilities are not supplied by M1. See [the composite specification](SPEC-sol6.1-composite.md) for proposed later milestones.
