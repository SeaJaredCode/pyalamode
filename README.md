# Pyalamode

Pyalamode checks a functional core in ordinary Python. The current M2 increment supports scalar functions, functional modules, recursively immutable tuples, stable source constants, checked calls and recursion, nested functions, stable captures, and controlled defaults. Accepted code runs through normal Python imports and commands. Checking parses application source without importing it or evaluating its hooks.

The supported check/build target is **CPython 3.13.1, standard GIL build, on macOS or Linux** (`cpython-3.13.1`). Other patches/minors, free-threaded builds, interpreters, and platforms fail the target gate. Installation under another Python 3.13 patch does not establish compatibility.

## Install and run

```sh
python3.13 --version
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
pyalamode check examples/scalar.py
python examples/scalar.py
pyalamode check examples/modules --no-cache
python -m examples.modules.demo
```

The scalar example prints `1300` and `0`. The module example prints `1500`, `6`, `6`, and `2`. Its checked core uses stable imports, defaults, a closure, a recursive calculation, and tuple inputs; its ordinary demo prints those results without receiving a purity claim.

One function can opt in with the runtime identity marker:

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

A module can opt in without importing that marker:

```python
"""Calculation core."""
# mode: fun

SERVICE_FEE = 200

def quote(cents: int, discount_cents: int = 0) -> int:
    return cents - discount_cents + SERVICE_FEE
```

The directive occurs once after any shebang, encoding declaration, and module docstring, before executable statements. A misplaced directive or region toggle fails. Module mode selects functions, nested definitions, and initialization. In an ordinary module, `@fun` selects that function and its nested definitions, defaults, annotations, captures, and dependencies; unrelated initialization stays unchecked.

Projects can require module mode without source markers:

```toml
[tool.pyalamode]
schema = 1
require_modules = ["core/**/*.py"]
```

Patterns are project-relative, case-sensitive glob patterns; `**/` may match zero directories. Absolute paths, parent traversal, and non-string patterns fail policy validation. Required mode also applies to discovered local dependencies matching the policy. Other accepted configuration values remain the closed defaults documented in the specification.

## Exact contracts

Every parameter and result has an explicit supported annotation. Analyzed calls establish the actual value and callable contracts; ordinary annotations alone cannot establish exact runtime inputs.

| Contract | Admitted syntax and meaning |
| --- | --- |
| Scalars | Exact `int`, `bool`, `str`, `bytes`, `None`; stable `types.NoneType` imports; supported quoted annotations |
| Tuples | Fixed `tuple[int, str]`, homogeneous `tuple[int, ...]`, empty `tuple[()]`; recursive exact immutable data, excluding subclasses and callable payloads |
| Callables | Stable `typing` or `collections.abc` `Callable[[int, str], int]`; fixed positional pure invocation with exact admitted inputs/result and stable captures |

Callable parameters express a required input contract. They do not turn an unknown function, lambda, protocol, or ordinary annotated parameter into checked pure evidence. Checked callers supply resolved checked functions or pass a callable already established by their own input contract. Callable annotations allow nested callable inputs/results, but exclude `Any`, ellipsis signatures, variadics, and keyword-only callback shapes. Optional positional defaults and positional-only parameters are compatible when the complete fixed positional call fits. Direct checked calls also support normal positional-only, positional-or-keyword, keyword-only, and default arguments.

A generic admitted callable has the finite invocation failure upper bound **`ZeroDivisionError` and `RecursionError`**, the current closed operation universe. Conditional callback invocation propagates that bound. Concrete direct targets retain their characterized transitive failures. Reports disclose concrete callback defaults, captures, and returned targets when established.

Stable constants require a single characterized source initialization and no analyzed replacement. Upper-case spelling, `Final`, hashability, a current integer object, and an annotation do not establish stability. A nested function can capture admitted immutable values and checked callables. Changing cells fail, and every required cell must be initialized before a closure is invoked or escapes. Recursion is admitted without a termination claim.

## Supported source

The scalar operations remain integer unary `+`/`-`, integer `+`/`-`/`*`/`//`/`%`, same-type integer/string/bytes comparisons, string/bytes concatenation, boolean `not`/`and`/`or`/equality, right-hand literal `is None`/`is not None`, and conditional expressions. Approved builtin signatures are `abs(int)`, `len(str|bytes|admitted_tuple)`, and two-or-more homogeneous positional `min`/`max` over exact `int`, `str`, or `bytes`. Division and remainder disclose `ZeroDivisionError`.

Statements include one-name initialization, annotated initialization, `if`/`elif`/`else`, `return`, `pass`, docstrings, and checked nested function definitions. Each reachable binding initializes once. Exclusive branches may initialize the same name; missing initialization and reachable reinitialization fail. Imports are module-level dependencies.

Module initializers and defaults use closed stable data expressions, earlier stable bindings, approved builtin calls, and checked callable references. **Calling application functions in initialization/default expressions is excluded in this increment**, even if their invocation contract is checked. Annotation expressions are parsed from the finite whitelist, and the only supported decorator is the resolved identity `fun`. Initialization failures and definition-time default failures are reported separately from function invocation failures.

Local imports resolve from the project root with package-before-module precedence and required package initializers. A strict module imports only characterized foundations or functional local modules. An ordinary module may separately perform unchecked initialization before using checked exports. Unresolved external APIs receive no trusted admission. A local file named `pyalamode`, `typing`, `types`, or `collections` cannot acquire foundation behavior through its spelling.

Loops, comprehensions, destructuring, tuple indexing/slicing/comparison, classes/records, mutable containers, arbitrary methods, reflection, generators, async, user exceptions/handlers, persistent collections, external trust approvals, and effects remain excluded. Dynamic ordinary dispatch stays the ordinary caller's responsibility. The checker is conservative about unknown aliases, ordinary control flow, and cells outside a checked enclosing scope.

## Check, build, and inspect

```sh
pyalamode check examples/modules --json
pyalamode build examples/modules --output build/modules-first-use
python -m examples.modules.demo
pyalamode check --audit tests/fixtures/m02/changing_capture.py
pyalamode explain PAL240
pyalamode explain tuple
pyalamode explain Callable
```

A build freshly checks the selected source and its resolved local dependencies, copies unchanged Python bytes into a fresh output directory, and writes `pyalamode-evidence.json`. To run that copied module example, enter the output directory and run `python -m examples.modules.demo` with the installed Pyalamode library available. Builds require a participating function or functional module, reject existing outputs, and publish no artifact after a failed gate or freshness check. Package distribution and consumer verification are later milestones.

Strict failures return status 1. Tooling, syntax, policy, and unsupported-target errors return 2. Audit findings alone return 0, label evidence unverified, and leave ordinary behavior unchanged. An empty ordinary selection may pass `check` but supplies no participating function or module claim. The same commands are available as `python -m pyalamode`.

At runtime, `fun(function)` returns that identical function object. It does not wrap, register, guard, or create check evidence. Ordinary callers must provide exact recursively admitted inputs and checked callable contracts, and leave resolved dependencies/captures unchanged. Unchecked monkey-patching violates the execution precondition; no runtime dependency monitor or argument guard is installed. Resource exhaustion, interruption, interpreter tampering, and arbitrary dynamic Python are outside the guarantee.

Disposable `.pyalamode-cache` entries include source bytes, target, policy, product identities, transitive local import bytes, resolution identities, and relevant analyzed binding replacements. An unchanged warm check reuses body evidence. A dependency edit invalidates its import closure; unrelated modules can retain hits. Adding an ordinary writer that replaces a referenced callable or foundation binding also invalidates affected evidence. Import closures are conservative: unused local imports and unrelated edits within an imported file can invalidate callers. Missing or corrupt cache entries trigger fresh checking. Builds bypass the cache and recheck source/dependency bytes and policy before publication.

## Verification and handoff

```sh
python -m unittest discover -s tests -p 'm0*.py' -v
python benchmarks/m01_scalar.py --output /tmp/pyalamode-m01.json
```

The M2 suite inherits M1's adversarial guarantees and covers module selection, recursive tuple contents, closure timing, defaults/annotation hooks, callable shapes/failures, source resolution, analyzed replacements, affected-file gate failure, normal artifacts, and selective cache freshness. See [the M2 handoff](Docs/milestones/02-modules.md) for concrete interfaces and limits, and [the composite specification](SPEC-sol6.1-composite.md) for later milestones.
