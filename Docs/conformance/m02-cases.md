# Milestone 2 independent conformance inventory

Authority: the full `SPEC-sol6.1-composite.md`, especially lines 116–120 (module/function boundary), 140–158 (non-execution, resolution and freshness), 222–234 (bindings and cells), 244–250 (deep tuples/callables), 294 (recursion), 346–366 (initialization and operation evidence), 469–470 (A09–A10), 497 (adversarial cases), and 506 (M2 gate); concrete inherited contract: `Docs/milestones/01-scalar.md`. This artifact records finite fixtures and exact observations, not a proof about arbitrary Python, measured user experience, or a waiver of unknown behavior.

Review status: final frozen-code bounded verification complete. No remaining observed blocking conformance issue; the final summary at the end supersedes the provisional snapshots, which are retained for exact correction history.

Reviewer ownership is this file only. Application source, tests, specifications, other documentation, and implementation are read-only. Tests below use actual `pyalamode.checker.analyze_source` and `pyalamode.project.check_paths`/`build_paths` APIs when the implementation is ready. Project probes use isolated temporary roots. No application fixture is imported during checking.

Expected strict status: 0 accepted, 1 unsatisfied verification, 2 tooling/resolution/runtime-target failure. Audit findings return 0 but no strict claim. Default exports stay unguarded: exact admitted inputs, stable captures, callable contracts and unchanged dependencies are execution preconditions. An unchecked runtime replacement may violate those preconditions without a runtime rejection. An analyzed replacement must prevent strict admission. An ordinary initializer is not certified merely because a function it defines is checked.

## Finite source inventory

Each block is an independent source unless a project layout or mutation sequence is stated. `fun` is the actual imported identity marker. Tuple/callable annotation fixtures will be aligned with the implementation's published finite syntax before execution; an unsupported syntax must fail closed rather than acquire an inferred contract.

### Header placement and boundary selection

H01, expected 0: canonical header after shebang, encoding and module docstring; no marker-library import required.

```python
#!/usr/bin/env python3
# coding: utf-8
"""Header documentation."""
# mode: fun
OFFSET = 2
def offset(value: int) -> int:
    return value + OFFSET
```

H02, expected 1: marker before an existing module docstring (the contract requires it after that docstring).

```python
# mode: fun
"""Header documentation."""
def identity(value: int) -> int:
    return value
```

H03, expected 1: marker after an import. H04, expected 1: marker inside a function. Neither is a supported region toggle.

```python
from pyalamode import fun
# mode: fun
def identity(value: int) -> int:
    return value
```

```python
def ordinary(value):
    # mode: fun
    return value
```

H05, expected 0 with **zero participating coverage**: a comment-looking line in a string is not a directive. H06 is the analogous ordinary assignment string case.

```python
"""# mode: fun"""
def ordinary(value):
    print(value)
```

```python
description = "# mode: fun"
def ordinary(value):
    print(value)
```

H07, expected 1: duplicated/conflicting directive; acceptance must not turn a later directive into a policy override.

```python
# mode: fun
# mode: off
def identity(value: int) -> int:
    return value
```

### Non-execution and initialization

I01, expected 0: unrelated ordinary initialization is outside the invocation claim and never executes during static analysis.

```python
from pyalamode import fun
raise RuntimeError("ordinary initializer executed")
@fun
def identity(value: int) -> int:
    return value
```

I02, expected 1: the same initializer in module mode must fail before execution.

```python
# mode: fun
raise RuntimeError("participating initializer executed")
def identity(value: int) -> int:
    return value
```

I03, expected 1: unknown initializer call. I04, expected 1: mutable initializer even if an unrelated function is scalar.

```python
# mode: fun
VALUE = open("CHECK_MUST_NOT_CREATE_THIS", "w")
def identity(value: int) -> int:
    return value
```

```python
# mode: fun
VALUES = (1, [])
def identity(value: int) -> int:
    return value
```

I05–I07, expected 1 without invoking any sentinel: participating default, extra decorator and annotation expression respectively. Checker/build must not evaluate definition-time expressions.

```python
from pyalamode import fun
@fun
def bad(value: int = open("DEFAULT_MUST_NOT_CREATE", "w")) -> int:
    return value
```

```python
from pyalamode import fun
@open("DECORATOR_MUST_NOT_CREATE", "w")
@fun
def bad(value: int) -> int:
    return value
```

```python
from pyalamode import fun
@fun
def bad(value: open("ANNOTATION_MUST_NOT_CREATE", "w")) -> int:
    return value
```

I08, expected refusal: participating `import unknown_dependency` cannot establish import/setup evidence by its spelling. I09, project case: strict `core.py` imports a pure checked export from ordinary `dependency.py` whose initializer calls `print`; the import initialization must either have an explicitly admitted setup contract or fail. A pure invocation claim alone cannot certify it. The same export reached from an ordinary module may have an invocation claim only, with ordinary initialization disclosed.

### A09 stable data, aliases and cells

C01, expected 0: module-mode scalar/recursive exact-tuple constants are statically established and used by a checked function.

```python
# mode: fun
BASE = 7
PAIR = (BASE, ("ok", b"ok", None))
def base(value: int) -> int:
    return value + BASE
```

C02, expected 0 under the worker's published finite rule: an ordinary global qualifies only through one statically characterized deeply immutable initialization and absence of every analyzed writer/replacement. Its present runtime object, uppercase spelling, or `Final` annotation is not evidence by itself. C04 tests the analyzed-writer counterexample.

```python
from pyalamode import fun
VALUE = 7
@fun
def read() -> int:
    return VALUE
```

C03–C05, expected 1: repeated constant initialization, an ordinary `global` writer, and a mutable member reachable through a tuple respectively.

```python
# mode: fun
VALUE = 7
VALUE = 7
def read() -> int:
    return VALUE
```

```python
from pyalamode import fun
VALUE = 7
def mutate() -> None:
    global VALUE
    VALUE = 8
@fun
def read() -> int:
    return VALUE
```

```python
# mode: fun
VALUE = (1, (2, []))
def read() -> int:
    return 1
```

C06, expected 0: stable enclosing local captured by a nested function. C07, expected 1: a later write to that enclosing cell. C08, expected 1: ordinary nonlocal writer to a captured cell. Nested lexical shadowing itself is not rebinding of the outer name.

```python
from pyalamode import fun
@fun
def outer(value: int) -> int:
    offset = 3
    def inner(item: int) -> int:
        return item + offset
    return inner(value)
```

```python
from pyalamode import fun
@fun
def outer(value: int) -> int:
    offset = 3
    def inner(item: int) -> int:
        return item + offset
    offset = 4
    return inner(value)
```

```python
from pyalamode import fun
def factory():
    offset = 3
    @fun
    def inner(item: int) -> int:
        return item + offset
    def mutate():
        nonlocal offset
        offset = 4
    return inner, mutate
```

C09, expected 1: escaping reused loop cell or comprehension-produced callback is unsupported, even if its annotation says callable. C10, expected 1: mutable capture. C11, expected 0 under published callable syntax: a checked factory returns a nested callable capturing an explicit exact scalar parameter; caller obligations include capture stability.

### A10 callable identity and call graph

F01, expected 0: checked same-module call, stable direct alias and exact scalar input.

```python
from pyalamode import fun
@fun
def plus_one(value: int) -> int:
    return value + 1
alias = plus_one
@fun
def compute(value: int) -> int:
    return alias(value)
```

F02, expected 1: replacement after alias establishment invalidates the alias's target evidence.

```python
from pyalamode import fun
@fun
def plus_one(value: int) -> int:
    return value + 1
alias = plus_one
alias = print
@fun
def compute(value: int) -> int:
    return alias(value)
```

F03, expected 1: direct callable replacement. F04, expected 1: imported callable replacement through a module alias or recognized setter/namespace alias. F05, expected 1: a checked caller targets an ordinary uncharacterized helper. F06, expected 1: an unknown/ordinary callable cannot become pure by passing through a checked wrapper or a `Callable` annotation.

```python
from pyalamode import fun
def ordinary(value: int) -> int:
    print(value)
    return value
@fun
def compute(value: int) -> int:
    return ordinary(value)
```

F07, expected 0: mutual recursion as one checked component, exact argument and result contracts; divergence is permitted and termination is not claimed.

```python
# mode: fun
def even(value: int) -> bool:
    if value == 0:
        return True
    return odd(value - 1)
def odd(value: int) -> bool:
    if value == 0:
        return False
    return even(value - 1)
```

F08, expected 1: change one member of that component to call `print`; every strict caller/component must lose admission. F09, expected 1: recursive callee receives `bool` for exact `int`. F10, expected refusal: default value or nested definition requires a callable that is not yet initialized at the actual Python definition time; invocation-time recursive availability does not establish definition-time availability.

### Signatures, defaults, tuples and callable values

S01, expected 0: admitted scalar/tuple defaults follow ordinary Python evaluation order, are exact/deeply stable, and omitted arguments use their published types. S02, expected 1: `int` default is `True`. S03, expected 1: tuple default contains a mutable member. S04, expected 1: a default calls an unknown function or references an unstable binding. S05, expected 1: an admitted default is assigned twice or a nested definition overwrites an initialized parameter/local.

S06–S10, expected 1: missing required argument, excess argument, duplicate positional/keyword argument, keyword for a positional-only parameter, and positional argument for a keyword-only parameter. S11, expected 0: valid positional-only and keyword-only/default call. S12, expected 1: unpacking bypass (`callee(*(1,))`, `callee(**{})`) until a characterized signature rule exists. S13, expected 1: exact tuple has a mutable member or a subclass/unknown element. S14, expected 1: tuple allocation identity/protocol dispatch remains uncharacterized. S15, expected 1: returned callable captures `list` or a replaced callable. S16, expected 0 under the published callable syntax: checked callable default/capture with compatible parameter/result types. S17, expected 1: callable signature mismatch. S18, expected 1: annotations/`Any`/a cast cannot promote unknown callable evidence.

## Project and freshness sequences

P01: isolated `core.py` selected by `[tool.pyalamode].require_modules = ["core.py"]` without a source marker passes with module coverage; adding unknown initializer behavior makes strict check/build fail. P02: a source `mode: off`/ordinary directive cannot weaken that required module policy. P03: a string containing a directive cannot supply policy coverage. P04: unresolved imports/tooling retain failure status and cannot appear as clean zero coverage.

D01 uses participating `leaf.py` (stable `VALUE`, checked `leaf`), `middle.py` (checked import/call of `leaf`) and `root.py` (checked import/call of `middle`), plus independent participating `unrelated.py`. Cold check must establish all contracts. Warm unchanged check may reuse all evidence. Edit `leaf.py` to a different valid constant: `leaf`, `middle` and `root` fingerprints/results must change or be re-established; unrelated evidence may be reused. Then edit leaf to an uncharacterized call/rebinding: subsequent check and build must fail with no newly published artifact. Prior artifact is retained, with evidence tied to its old bytes. Relevant source/dependency identities/operation contracts, target, policy and product bytes are all part of freshness (§5.2). Cache deletion/corruption must not change admission.

D02: edit only `unrelated.py`; leaf/middle/root evidence should remain reusable. D03: change policy so required module coverage changes; affected evidence must be invalidated. D04: alter a transitive ordinary-import initializer from admitted pure setup to unknown/effectful setup; importing participating modules cannot retain their previous initialization claim. D05: make one member of a recursive cross-file component invalid; all component/dependent exports become unverified. D06: build captures/checks one source snapshot and refuses a relevant dependency mutation before publication.

## Observation ledger

Initial inventory prepared against baseline commit `7d694e0`. M2 implementation was not yet ready, so the inventory above contains expectations, **not passed tests**. Final observations will preserve API, fixture source/status, runtime, implementation snapshot and causal implementation line references. False admissions take priority over unsupported-case false positives. Whole-suite macOS/Linux acceptance is owned by the orchestrator.

### Interim read-only API pass (implementation still in progress)

Observed on macOS, CPython 3.13.1, using `.venv/bin/python -B` and actual `analyze_source(case["source"], path="/virtual/m02/" + case["id"] + ".py")`. Checker bytes at the start of this pass had SHA-256 `712b2e263bff0d9cb88edfd7d1f940520c5ef6413efff69ec2ad7293871327e7`. All 77 concrete single-source fixtures were invoked; 67 matched numeric expectations, five invalid fixtures were admitted, three invalid fixtures raised an internal exception, and two proposed positive fixtures were rejected. These are provisional implementation observations, not final gate results. No sentinel application file was created by this invocation.

| Fixture | Expected | Actual | Exact observation |
| --- | --- | --- | --- |
| C08 | 1 | 0 | No diagnostics; `factory.inner` published `checked participating source`, capturing `offset: int`, despite the sibling ordinary `nonlocal offset` writer |
| L06 | 1 | 0 | No diagnostics; `outer.inner` published checked source while its `int` annotation resolves to the ordinary outer parameter |
| L07 | 1 | 0 | No diagnostics; `outer.inner` published checked source and captured `int: int` despite using that ordinary local as its annotation target |
| O05 | 1 | 0 | No diagnostics; `outer.first` captured a predeclared `second` and was called before the `second` definition executes |
| O07 | 1 | 0 | No diagnostics; `outer.first` escaped with predeclared `second` even though the early return prevents its definition from executing |
| L01–L03 | 1 | no result | Each raised `KeyError: '<unknown>'`; no `CheckResult` or diagnostic status was returned |
| B02 | 0 | 1 | `PAL102` and `PAL221` at source line 9: known checked `identity` callback was treated as an uninitialized local |
| O04 | 0 | 1 | `PAL230` at source line 5: application invocation in initializers is excluded by the new closed initializer rule; this is a finite-subset restriction to publish, not a false admission |

At this snapshot the causal source paths were `pyalamode/checker.py`: `_annotation` lines 1046–1048 reads lexical shadow names only when the active function has a checked `FunctionInfo.parent`, losing ordinary-enclosing bindings (L06/L07); `_ordinary_capture_env` lines 1174–1187 checks a single parent initialization without finding nested ordinary nonlocal cell writes (C08); `function` lines 1245–1248 installs stable syntactic sibling definitions into captures before proving their cell initialization at a call/escape (O05/O07). `FunctionInfo.value` lines 689–692 indexes the type table for `"<unknown>"` parameter types (L01–L03). Sources and line references are tied to the stated interim bytes and may move during correction.

Positive observations: F07/O06 valid mutual/sibling recursion passed; F08 invalid recursive body failed and both contracts were unverified; R01 passed and both the recursive function and its caller listed `RecursionError` and `ZeroDivisionError`. The finite pass did not execute those potentially divergent functions. Exact source inputs are retained below. All findings were sent to the worker and orchestrator for correction and final retest.

### Interim source-graph and identity passes

Actual `analyze_sources` with each concrete virtual project layout and its policy produced the expected aggregate status for the first 12 projects (checker SHA-256 `3f2acd5bc82ea2a1bbc28baf880dc43095ceb7cab17a321bff0505d12799f15f`). I09 rejected strict import of ordinary effectful setup; I10 accepted invocation only and reported `unchecked ordinary module initialization` on both ordinary modules; G01 resolved the leaf/middle/core graph; G03 listed `ZeroDivisionError` on both transitive callers. G02's invalid leaf failed, and transitive contract strings were downgraded, but middle/core individual results incorrectly remained status 0/verified true with checked initializer strings. At that snapshot `SourceGraph.analyze` lines 853–857 changed only contract text; `CheckResult.verified`/`status` in `model.py` lines 95–103 use diagnostics. The worker subsequently added dependency diagnostics; final structured-state retest remains required.

The seven foundation/package project probes used checker SHA-256 `4016a16962cc81d0570b5088a251d49d08f095dc9d3ebff58a34bdfae9b7e5d3`. Exact outcomes:

| Fixture | Expected | Actual | Observation |
| --- | --- | --- | --- |
| K01 | 1 | 0 | Effectful local `pyalamode.py` decorator accepted as trusted identity marker; app export checked/verified |
| K02 | 1 | 0 | Effectful local `pyalamode/__init__.py` decorator accepted as trusted identity marker; app export checked/verified |
| K03 | 1 | 0 | Local `typing.py` user `Callable.__class_getitem__` hook treated as the foundation annotation contract |
| K04 | 1 | 0 | Local `types.py` binds `NoneType = list`; app still receives exact `None` contract and checked source evidence |
| K05 | 1 | 0 | Local `collections` initializer calls `print` and local `abc.Callable` has a user annotation hook; app still claims checked pure initialization and a checked callable contract |
| K07 | 1 | 1 | Ordinary package initializer is refused by strict importer (`PAL241`, app line 2) |
| K08 | 1 | 1 | Invalid participating package initializer is refused; app has dependency-gate `PAL240`, while its initializer string still said checked pure initialization |

At those bytes, `FunctionalAnalyzer._marker_valid` (`checker.py` lines 1090–1100, also base lines 156–164) checks source bindings/writes but does not distinguish an actual project-local `pyalamode` implementation from the installed foundation. `_type_identity` lines 1064–1067 and 1073–1083 admits standard annotation targets by module spelling, and `_check_import` lines 1268–1273 skips foundation initialization by spelling before inspecting source-graph identities. These concrete false admissions were sent to the worker and orchestrator; they cannot be waived as unchecked runtime replacement, because the conflicting dependency source is already present in the analyzed graph.

### Correction pass before code freeze

Actual single-source retest at checker SHA-256 `6699166a8312ed064df4c3325ac5a225343375ba02a05156889a8b076ed4abda`: **83/83 numeric statuses matched**, with no exceptions. C08/L06/L07/O05/O07 now refuse admission; L01–L03 return diagnostic results; B02 accepts the resolved checked callback. B05 reports `RecursionError` and `ZeroDivisionError` on conditional `apply`, `caller`, and `default`; `returned` resolves the concrete `divide` target and lists precise `ZeroDivisionError`. I11 publishes `initialization_failures = ["ZeroDivisionError"]`, independently of `identity.failures = []`.

O04's numeric expectation is now 1 to reflect the published closed subset: checked application calls are confined to function bodies, while initialization/default expressions use closed stable data and approved builtins. The interim rejection remains recorded above; the test is retained to ensure that unsupported application initialization never obtains a clean initializer claim. This correction pass does not replace the final frozen-code project/cache/build retest.

## Concrete single-source probe data

The following JSON is the exact source input for the finite API probes. It also concretizes the shorthand signature/capture cases above. `L01`–`L05` test lexical definition-time binding; `O01`–`O04` distinguish default/initializer order from invocation-time predeclarations; `R01` requires `ZeroDivisionError` to propagate through the recursive component and caller; `T01`–`T05` and `B01`–`B04` exercise recursive tuple contents and actual callable evidence. The initial 71-source data omits C02; it is separately probed after publication of the static stable-ordinary-initializer rule above.

```json
[
  {
    "id": "H01",
    "expected": 0,
    "source": "#!/usr/bin/env python3\n# coding: utf-8\n\"\"\"Header documentation.\"\"\"\n# mode: fun\nOFFSET = 2\ndef offset(value: int) -> int:\n    return value + OFFSET\n"
  },
  {
    "id": "H02",
    "expected": 1,
    "source": "# mode: fun\n\"\"\"Header documentation.\"\"\"\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "H03",
    "expected": 1,
    "source": "from pyalamode import fun\n# mode: fun\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "H04",
    "expected": 1,
    "source": "def ordinary(value):\n    # mode: fun\n    return value\n"
  },
  {
    "id": "H05",
    "expected": 0,
    "source": "\"\"\"# mode: fun\"\"\"\ndef ordinary(value):\n    print(value)\n"
  },
  {
    "id": "H06",
    "expected": 0,
    "source": "description = \"# mode: fun\"\ndef ordinary(value):\n    print(value)\n"
  },
  {
    "id": "H07",
    "expected": 1,
    "source": "# mode: fun\n# mode: off\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "I01",
    "expected": 0,
    "source": "from pyalamode import fun\nraise RuntimeError(\"ordinary initializer executed\")\n@fun\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "I02",
    "expected": 1,
    "source": "# mode: fun\nraise RuntimeError(\"participating initializer executed\")\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "I03",
    "expected": 1,
    "source": "# mode: fun\nVALUE = open(\"CHECK_MUST_NOT_CREATE_THIS\", \"w\")\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "I04",
    "expected": 1,
    "source": "# mode: fun\nVALUES = (1, [])\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "I05",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef bad(value: int = open(\"DEFAULT_MUST_NOT_CREATE\", \"w\")) -> int:\n    return value\n"
  },
  {
    "id": "I06",
    "expected": 1,
    "source": "from pyalamode import fun\n@open(\"DECORATOR_MUST_NOT_CREATE\", \"w\")\n@fun\ndef bad(value: int) -> int:\n    return value\n"
  },
  {
    "id": "I07",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef bad(value: open(\"ANNOTATION_MUST_NOT_CREATE\", \"w\")) -> int:\n    return value\n"
  },
  {
    "id": "I08",
    "expected": 1,
    "source": "# mode: fun\nimport unknown_dependency\ndef identity(value: int) -> int:\n    return value\n"
  },
  {
    "id": "C01",
    "expected": 0,
    "source": "# mode: fun\nBASE = 7\nPAIR = (BASE, (\"ok\", b\"ok\", None))\ndef base(value: int) -> int:\n    return value + BASE\n"
  },
  {
    "id": "C03",
    "expected": 1,
    "source": "# mode: fun\nVALUE = 7\nVALUE = 7\ndef read() -> int:\n    return VALUE\n"
  },
  {
    "id": "C04",
    "expected": 1,
    "source": "from pyalamode import fun\nVALUE = 7\ndef mutate() -> None:\n    global VALUE\n    VALUE = 8\n@fun\ndef read() -> int:\n    return VALUE\n"
  },
  {
    "id": "C05",
    "expected": 1,
    "source": "# mode: fun\nVALUE = (1, (2, []))\ndef read() -> int:\n    return 1\n"
  },
  {
    "id": "C06",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    offset = 3\n    def inner(item: int) -> int:\n        return item + offset\n    return inner(value)\n"
  },
  {
    "id": "C07",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    offset = 3\n    def inner(item: int) -> int:\n        return item + offset\n    offset = 4\n    return inner(value)\n"
  },
  {
    "id": "C08",
    "expected": 1,
    "source": "from pyalamode import fun\ndef factory():\n    offset = 3\n    @fun\n    def inner(item: int) -> int:\n        return item + offset\n    def mutate():\n        nonlocal offset\n        offset = 4\n    return inner, mutate\n"
  },
  {
    "id": "C09",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef factory(values: tuple[int, ...]) -> tuple[Callable[[], int], ...]:\n    return tuple(lambda: value for value in values)\n"
  },
  {
    "id": "C10",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    offset = []\n    def inner(item: int) -> int:\n        return item + len(offset)\n    return inner(value)\n"
  },
  {
    "id": "C11",
    "expected": 0,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef factory(value: int) -> Callable[[int], int]:\n    def add(item: int) -> int:\n        return item + value\n    return add\n"
  },
  {
    "id": "F01",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef plus_one(value: int) -> int:\n    return value + 1\nalias = plus_one\n@fun\ndef compute(value: int) -> int:\n    return alias(value)\n"
  },
  {
    "id": "F02",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef plus_one(value: int) -> int:\n    return value + 1\nalias = plus_one\nalias = print\n@fun\ndef compute(value: int) -> int:\n    return alias(value)\n"
  },
  {
    "id": "F03",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef plus_one(value: int) -> int:\n    return value + 1\nplus_one = print\n@fun\ndef compute(value: int) -> int:\n    return plus_one(value)\n"
  },
  {
    "id": "F05",
    "expected": 1,
    "source": "from pyalamode import fun\ndef ordinary(value: int) -> int:\n    print(value)\n    return value\n@fun\ndef compute(value: int) -> int:\n    return ordinary(value)\n"
  },
  {
    "id": "F06",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\ndef ordinary(value: int) -> int:\n    print(value)\n    return value\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n@fun\ndef compute(value: int) -> int:\n    return apply(ordinary, value)\n"
  },
  {
    "id": "F07",
    "expected": 0,
    "source": "# mode: fun\ndef even(value: int) -> bool:\n    if value == 0:\n        return True\n    return odd(value - 1)\ndef odd(value: int) -> bool:\n    if value == 0:\n        return False\n    return even(value - 1)\n"
  },
  {
    "id": "F08",
    "expected": 1,
    "source": "# mode: fun\ndef even(value: int) -> bool:\n    if value == 0:\n        return True\n    return odd(value - 1)\ndef odd(value: int) -> bool:\n    print(value)\n    return even(value - 1)\n"
  },
  {
    "id": "F09",
    "expected": 1,
    "source": "# mode: fun\ndef recursive(value: int) -> int:\n    if value == 0:\n        return 0\n    return recursive(True)\n"
  },
  {
    "id": "F10",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    def inner(item: int = later(1)) -> int:\n        return item\n    def later(item: int) -> int:\n        return item + 1\n    return inner(value)\n"
  },
  {
    "id": "S01",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef default(value: int = 3, suffix: tuple[str, bytes] = (\"ok\", b\"ok\")) -> int:\n    return value\n@fun\ndef use() -> int:\n    return default()\n"
  },
  {
    "id": "S02",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef default(value: int = True) -> int:\n    return value\n"
  },
  {
    "id": "S03",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef default(value: tuple[int, tuple[str, ...]] = (1, [\"ok\"])) -> int:\n    return 1\n"
  },
  {
    "id": "S04",
    "expected": 1,
    "source": "from pyalamode import fun\ndef unknown():\n    return 1\n@fun\ndef default(value: int = unknown()) -> int:\n    return value\n"
  },
  {
    "id": "S05",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(inner: int) -> int:\n    def inner(value: int) -> int:\n        return value\n    return 1\n"
  },
  {
    "id": "S06",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: int) -> int:\n    return value\n@fun\ndef caller() -> int:\n    return callee()\n"
  },
  {
    "id": "S07",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: int) -> int:\n    return value\n@fun\ndef caller() -> int:\n    return callee(1, 2)\n"
  },
  {
    "id": "S08",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: int) -> int:\n    return value\n@fun\ndef caller() -> int:\n    return callee(1, value=2)\n"
  },
  {
    "id": "S09",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: int, /) -> int:\n    return value\n@fun\ndef caller() -> int:\n    return callee(value=1)\n"
  },
  {
    "id": "S10",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(*, value: int) -> int:\n    return value\n@fun\ndef caller() -> int:\n    return callee(1)\n"
  },
  {
    "id": "S11",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: int, /, *, extra: int = 2) -> int:\n    return value + extra\n@fun\ndef caller() -> int:\n    return callee(1, extra=3)\n"
  },
  {
    "id": "S12",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: int) -> int:\n    return value\n@fun\ndef caller() -> int:\n    return callee(*(1,))\n"
  },
  {
    "id": "S13",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: tuple[int, tuple[str, ...]]) -> int:\n    return 1\n@fun\ndef caller() -> int:\n    return callee((1, (\"ok\", [])))\n"
  },
  {
    "id": "S14",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef same(left: tuple[int, ...], right: tuple[int, ...]) -> bool:\n    return left is right\n"
  },
  {
    "id": "S15",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef factory() -> Callable[[int], int]:\n    values = []\n    def inner(value: int) -> int:\n        return value + len(values)\n    return inner\n"
  },
  {
    "id": "S16",
    "expected": 0,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef identity(value: int) -> int:\n    return value\n@fun\ndef apply(value: int, cb: Callable[[int], int] = identity) -> int:\n    return cb(value)\n"
  },
  {
    "id": "S17",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef identity(value: str) -> str:\n    return value\n@fun\ndef apply(value: int, cb: Callable[[int], int] = identity) -> int:\n    return cb(value)\n"
  },
  {
    "id": "S18",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable, Any\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\ndef ordinary(cb: Callable[[int], int]) -> int:\n    return apply(cb, 1)\n"
  },
  {
    "id": "L01",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(int: int) -> int:\n    def inner(value: int) -> int:\n        return value\n    return inner(int)\n"
  },
  {
    "id": "L02",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    int = 1\n    def inner(item: int) -> int:\n        return item\n    return inner(value)\n"
  },
  {
    "id": "L03",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    def inner(item: int) -> int:\n        return item\n    int = 1\n    return inner(value)\n"
  },
  {
    "id": "L04",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    def inner(item: int = offset) -> int:\n        return item\n    offset = 1\n    return inner(value)\n"
  },
  {
    "id": "L05",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    offset = 1\n    def inner(item: int = offset) -> int:\n        return item\n    return inner()\n"
  },
  {
    "id": "O01",
    "expected": 1,
    "source": "# mode: fun\nfrom typing import Callable\ndef f(cb: Callable[[int], int] = f) -> int:\n    return cb(1)\n"
  },
  {
    "id": "O02",
    "expected": 1,
    "source": "# mode: fun\ndef f(value: int = LATER) -> int:\n    return value\nLATER = 1\n"
  },
  {
    "id": "O03",
    "expected": 1,
    "source": "# mode: fun\ndef f() -> int:\n    return LATER\nEARLY = f()\nLATER = 1\n"
  },
  {
    "id": "O04",
    "expected": 1,
    "source": "# mode: fun\ndef f() -> int:\n    return LATER\nLATER = 1\nAFTER = f()\n"
  },
  {
    "id": "R01",
    "expected": 0,
    "source": "# mode: fun\ndef recursive(value: int) -> int:\n    if value == 0:\n        return 1 // value\n    return recursive(value - 1)\ndef caller(value: int) -> int:\n    return recursive(value)\n"
  },
  {
    "id": "T01",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef identity(value: tuple[int, tuple[str, bytes], None]) -> tuple[int, tuple[str, bytes], None]:\n    return value\n"
  },
  {
    "id": "T02",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef identity(value: tuple[int, ...]) -> tuple[int, ...]:\n    return value\n@fun\ndef empty() -> tuple[()]:\n    return ()\n"
  },
  {
    "id": "T03",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: tuple[int, ...]) -> int:\n    return 1\ncallee((True,))\n"
  },
  {
    "id": "T04",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: tuple[int, ...]) -> int:\n    return 1\nclass Evil(int):\n    pass\ncallee((Evil(1),))\n"
  },
  {
    "id": "T05",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef callee(value: tuple[int, ...]) -> int:\n    return 1\nclass Evil(tuple):\n    pass\ncallee(Evil((1,)))\n"
  },
  {
    "id": "B01",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\napply(print, 1)\n"
  },
  {
    "id": "B02",
    "expected": 0,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef identity(value: int) -> int:\n    return value\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\napply(identity, 1)\n"
  },
  {
    "id": "B03",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\ndef ordinary(cb: Callable[[int], int]) -> int:\n    return apply(cb, 1)\n"
  },
  {
    "id": "B04",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef bad(value: int) -> int:\n    print(value)\n    return value\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n@fun\ndef caller(value: int) -> int:\n    return apply(bad, value)\n"
  }
]
```

## Concrete project probe data

These exact layouts drive the project API probes. `I10` may accept only an invocation claim while its ordinary import initialization remains explicitly unchecked; its expected 0 does not certify importing the dependency. `G03` must list `ZeroDivisionError` on both transitive callers. `G01`/`G02` also supply the initial/failing source snapshots for D01.

```json
[
  {
    "id": "P01",
    "expected": 0,
    "files": {
      "pyproject.toml": "[tool.pyalamode]\nschema=1\nrequire_modules=[\"core.py\"]\n",
      "core.py": "VALUE = 3\ndef identity(value: int) -> int:\n    return value + VALUE\n"
    }
  },
  {
    "id": "P01-invalid",
    "expected": 1,
    "files": {
      "pyproject.toml": "[tool.pyalamode]\nschema=1\nrequire_modules=[\"core.py\"]\n",
      "core.py": "print(\"unknown initializer\")\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "P02",
    "expected": 1,
    "files": {
      "pyproject.toml": "[tool.pyalamode]\nschema=1\nrequire_modules=[\"core.py\"]\n",
      "core.py": "# mode: off\nprint(\"weakening\")\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "P03",
    "expected": 1,
    "files": {
      "pyproject.toml": "[tool.pyalamode]\nschema=1\nrequire_modules=[\"core.py\"]\n",
      "core.py": "\"\"\"# mode: fun\"\"\"\nprint(\"policy still applies\")\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "I09",
    "expected": 1,
    "files": {
      "dependency.py": "from pyalamode import fun\nprint(\"ordinary setup\")\n@fun\ndef identity(value: int) -> int:\n    return value\n",
      "core.py": "# mode: fun\nfrom dependency import identity\ndef caller(value: int) -> int:\n    return identity(value)\n"
    }
  },
  {
    "id": "I10",
    "expected": 0,
    "files": {
      "dependency.py": "from pyalamode import fun\nprint(\"ordinary setup\")\n@fun\ndef identity(value: int) -> int:\n    return value\n",
      "core.py": "from pyalamode import fun\nfrom dependency import identity\n@fun\ndef caller(value: int) -> int:\n    return identity(value)\n"
    }
  },
  {
    "id": "F04-attribute",
    "expected": 1,
    "files": {
      "leaf.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "core.py": "from pyalamode import fun\nimport leaf as module\nalias = module\nalias.identity = print\n@fun\ndef caller(value: int) -> int:\n    return module.identity(value)\n"
    }
  },
  {
    "id": "F04-setter",
    "expected": 1,
    "files": {
      "leaf.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "core.py": "from pyalamode import fun\nimport leaf as module\nalias = module\nsetattr(alias, \"identity\", print)\n@fun\ndef caller(value: int) -> int:\n    return module.identity(value)\n"
    }
  },
  {
    "id": "F04-in-writer",
    "expected": 1,
    "files": {
      "leaf.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "core.py": "from pyalamode import fun\nimport leaf as module\nalias = module\ndef mutate():\n    alias.identity = print\n@fun\ndef caller(value: int) -> int:\n    return module.identity(value)\n"
    }
  },
  {
    "id": "G01",
    "expected": 0,
    "files": {
      "leaf.py": "# mode: fun\nVALUE = 1\ndef leaf(value: int) -> int:\n    return value + VALUE\n",
      "middle.py": "# mode: fun\nfrom leaf import leaf\ndef middle(value: int) -> int:\n    return leaf(value)\n",
      "core.py": "# mode: fun\nfrom middle import middle\ndef caller(value: int) -> int:\n    return middle(value)\n",
      "unrelated.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "G02",
    "expected": 1,
    "files": {
      "leaf.py": "# mode: fun\nVALUE = 1\ndef leaf(value: int) -> int:\n    print(\"invalid leaf\")\n    return value + VALUE\n",
      "middle.py": "# mode: fun\nfrom leaf import leaf\ndef middle(value: int) -> int:\n    return leaf(value)\n",
      "core.py": "# mode: fun\nfrom middle import middle\ndef caller(value: int) -> int:\n    return middle(value)\n",
      "unrelated.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "G03",
    "expected": 0,
    "files": {
      "leaf.py": "# mode: fun\ndef leaf(value: int) -> int:\n    return 1 // value\n",
      "middle.py": "# mode: fun\nfrom leaf import leaf\ndef middle(value: int) -> int:\n    return leaf(value)\n",
      "core.py": "# mode: fun\nfrom middle import middle\ndef caller(value: int) -> int:\n    return middle(value)\n"
    }
  }
]
```

## Additional lexical and sibling-cell probes

`L06`/`L07` require ordinary enclosing annotation bindings to be resolved at their actual lexical definition site. `O05`/`O07` test nested sibling predeclarations before a closure cell is initialized or after an early return; `O06` is the valid after-definition counterpart. The presence of a later syntactic declaration does not establish a cell value at an earlier call or escape. C02 executes the ordinary stable-constant decision.

```json
[
  {
    "id": "L06",
    "expected": 1,
    "source": "from pyalamode import fun\ndef outer(int):\n    @fun\n    def inner(value: int) -> int:\n        return value\n    return inner\n"
  },
  {
    "id": "L07",
    "expected": 1,
    "source": "from pyalamode import fun\ndef outer():\n    int = 1\n    @fun\n    def inner(value: int) -> int:\n        return value\n    return inner\n"
  },
  {
    "id": "O05",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    def first(item: int) -> int:\n        return second(item)\n    early = first(value)\n    def second(item: int) -> int:\n        return item\n    return early\n"
  },
  {
    "id": "O06",
    "expected": 0,
    "source": "from pyalamode import fun\n@fun\ndef outer(value: int) -> int:\n    def first(item: int) -> int:\n        return second(item)\n    def second(item: int) -> int:\n        return item\n    return first(value)\n"
  },
  {
    "id": "O07",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef outer() -> Callable[[int], int]:\n    def first(item: int) -> int:\n        return second(item)\n    return first\n    def second(item: int) -> int:\n        return item\n"
  },
  {
    "id": "C02",
    "expected": 0,
    "source": "from pyalamode import fun\nVALUE = 7\n@fun\ndef read() -> int:\n    return VALUE\n"
  }
]
```

## Foundation identity and package initialization probes

`K01`–`K05` are local modules/packages that shadow familiar product or standard-library spellings. Their actual implementations and setup do not match the installed trusted foundation; imports/annotations/decorators must resolve identities before admission. `builtins` is not included as a filesystem shadow because normal Python import gives the builtin module priority. The project's actual installed product package is an accepted foundation identity and requires a separate positive check of existing repo examples, not a fabricated shadow. `K07`/`K08` require package initializers as well as submodule source to participate in dependency and initializer evidence.

```json
[
  {
    "id": "K01",
    "expected": 1,
    "files": {
      "pyalamode.py": "def fun(function):\n    print(\"local decorator effect\")\n    return function\n",
      "app.py": "from pyalamode import fun\n@fun\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "K02",
    "expected": 1,
    "files": {
      "pyalamode/__init__.py": "def fun(function):\n    print(\"local package decorator effect\")\n    return function\n",
      "app.py": "from pyalamode import fun\n@fun\ndef identity(value: int) -> int:\n    return value\n"
    }
  },
  {
    "id": "K03",
    "expected": 1,
    "files": {
      "typing.py": "class Callable:\n    def __class_getitem__(cls, item):\n        print(\"annotation hook\")\n        return object\n",
      "app.py": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n"
    }
  },
  {
    "id": "K04",
    "expected": 1,
    "files": {
      "types.py": "NoneType = list\n",
      "app.py": "from pyalamode import fun\nfrom types import NoneType\n@fun\ndef identity(value: NoneType) -> NoneType:\n    return value\n"
    }
  },
  {
    "id": "K05",
    "expected": 1,
    "files": {
      "collections/__init__.py": "print(\"local collections initializer\")\n",
      "collections/abc.py": "class Callable:\n    def __class_getitem__(cls, item):\n        print(\"annotation hook\")\n        return object\n",
      "app.py": "# mode: fun\nfrom collections.abc import Callable\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n"
    }
  },
  {
    "id": "K07",
    "expected": 1,
    "files": {
      "pkg/__init__.py": "print(\"ordinary package initializer\")\n",
      "pkg/core.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "app.py": "# mode: fun\nfrom pkg.core import identity\ndef caller(value: int) -> int:\n    return identity(value)\n"
    }
  },
  {
    "id": "K08",
    "expected": 1,
    "files": {
      "pkg/__init__.py": "# mode: fun\nVALUES = []\n",
      "pkg/core.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "app.py": "# mode: fun\nfrom pkg.core import identity\ndef caller(value: int) -> int:\n    return identity(value)\n"
    }
  }
]
```

## Higher-order failure propagation probe

B05 is expected to pass with a complete characterized failure bound: `caller`, `default` and `returned` can invoke `divide` and therefore must disclose `ZeroDivisionError` (or a conservative published callable failure bound containing it). A pure invocation annotation cannot erase actual callback behavior. The ordinary caller's exact-input/stable-callback obligation does not remove admitted division failure from these implementations.

```json
[
  {
    "id": "B05",
    "expected": 0,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef divide(value: int) -> int:\n    return 1 // value\n@fun\ndef apply(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n@fun\ndef caller(value: int) -> int:\n    return apply(divide, value)\n@fun\ndef default(value: int, cb: Callable[[int], int] = divide) -> int:\n    return cb(value)\n@fun\ndef factory() -> Callable[[int], int]:\n    return divide\n@fun\ndef returned(value: int) -> int:\n    return factory()(value)\n"
  }
]
```

Actual interim `analyze_source` on CPython 3.13.1 with checker SHA-256 `64f913325cc095f94cb122a884df97465bc426eba996c2d89d4bb105df673c12` returned status 0 and no diagnostics. Contracts: `divide.failures = ["ZeroDivisionError"]`; `apply`, `caller`, `default`, `factory`, and `returned` all had `failures = []`. `caller.dependencies` named only `apply`; `returned.dependencies` named only `factory`; the callable default recorded its signature but no target. This is incomplete admitted failure evidence for concrete known callback paths. Worker/orchestrator notified; final retest required.




## Callable shape and initializer failure probes

B06–B08 reject a required keyword-only argument hidden by a fixed positional callable return/default/assignment. B09 is the compatible positional-only counterpart. I11 may pass only with characterized initialization failure (`ZeroDivisionError`) disclosed separately from `identity` invocation. Initializer admission is not a promise that importing every accepted module completes successfully.

```json
[
  {
    "id": "B06",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef target(value: int, *, extra: int) -> int:\n    return value + extra\n@fun\ndef factory() -> Callable[[int], int]:\n    return target\n@fun\ndef caller(value: int) -> int:\n    return factory()(value)\n"
  },
  {
    "id": "B07",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef target(value: int, *, extra: int) -> int:\n    return value + extra\n@fun\ndef apply(value: int, cb: Callable[[int], int] = target) -> int:\n    return cb(value)\n"
  },
  {
    "id": "B08",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef target(value: int, *, extra: int) -> int:\n    return value + extra\n@fun\ndef caller(value: int) -> int:\n    callback: Callable[[int], int] = target\n    return callback(value)\n"
  },
  {
    "id": "B09",
    "expected": 0,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef target(value: int, /) -> int:\n    return value\n@fun\ndef apply(value: int, cb: Callable[[int], int] = target) -> int:\n    return cb(value)\n"
  },
  {
    "id": "I11",
    "expected": 0,
    "source": "# mode: fun\nVALUE = 1 // 0\ndef identity(value: int) -> int:\n    return value\n"
  }
]
```

Interim I11 observation (checker SHA-256 `93628a875273d3e7270dc94b2d54219d5d01eb0ec61c17881383e8dbcd3ecba5`): status 0/verified true, checked pure initializer string, `identity.failures = []`, and no initializer failure field in `to_dict()`. This is an initialization disclosure gap; it is not a request to add `ZeroDivisionError` to the unrelated identity invocation contract. Worker/orchestrator notified; final retest required.

## Warm-cache resolution and writer-context transitions

For each exact layout below, call actual `check_paths(root=root)` twice (cold and unchanged warm), write `added_files` without modifying `files`, then call both cached and `cache=False` checks on the same current root. The baseline must pass, and the changed cached/fresh gates must agree on refusal. Sources are never imported. Removing the added files and deleting/corrupting cache cannot change admission. These are relevant resolution/writer changes, despite the new ordinary module being outside the caller's original import closure.

```json
[
  {
    "id": "W01-module-writer",
    "expected": 0,
    "expected_after_addition": 1,
    "files": {
      "leaf.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "core.py": "# mode: fun\nfrom leaf import identity\ndef caller(value: int) -> int:\n    return identity(value)\n"
    },
    "added_files": {
      "writer.py": "import leaf\nleaf.identity = print\n"
    }
  },
  {
    "id": "W02-builtin-writer",
    "expected": 0,
    "expected_after_addition": 1,
    "files": {
      "core.py": "# mode: fun\ndef caller(value: int) -> int:\n    return abs(value)\n"
    },
    "added_files": {
      "writer.py": "import builtins\nbuiltins.abs = print\n"
    }
  },
  {
    "id": "W03-marker-writer",
    "expected": 0,
    "expected_after_addition": 1,
    "files": {
      "core.py": "from pyalamode import fun\n@fun\ndef caller(value: int) -> int:\n    return value\n"
    },
    "added_files": {
      "writer.py": "import pyalamode\npyalamode.fun = print\n"
    }
  },
  {
    "id": "W04-annotation-writer",
    "expected": 0,
    "expected_after_addition": 1,
    "files": {
      "core.py": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef caller(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n"
    },
    "added_files": {
      "writer.py": "import typing\ntyping.Callable = print\n"
    }
  },
  {
    "id": "W05-marker-resolution",
    "expected": 0,
    "expected_after_addition": 1,
    "files": {
      "core.py": "from pyalamode import fun\n@fun\ndef caller(value: int) -> int:\n    return value\n"
    },
    "added_files": {
      "pyalamode.py": "def fun(function):\n    print(\"shadow decorator\")\n    return function\n"
    }
  },
  {
    "id": "W06-annotation-resolution",
    "expected": 0,
    "expected_after_addition": 1,
    "files": {
      "core.py": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef caller(cb: Callable[[int], int], value: int) -> int:\n    return cb(value)\n"
    },
    "added_files": {
      "typing.py": "class Callable:\n    def __class_getitem__(cls, item):\n        print(\"shadow annotation\")\n        return object\n"
    }
  }
]
```

Interim actual `check_paths` outcomes, CPython 3.13.1, checker SHA-256 `6ba7d965c0e42fe8a2cecc3d98009ac63b43e5642977882d221d32b8a96da7ea`, project SHA-256 `c2ef72705112af3f1b46c76ab3ba51473de0cc8d3606934f177e405bc2cf1b91`: W01–W04 each yielded cold 0, warm 0, changed-cached **0**, changed-fresh **1**. Every changed cached `core.py` had `cache_hit = true` and no diagnostics. W01's `leaf.py` also hit. Fresh W01/W02 reported unknown target/stable-binding failures; fresh W03 reported invalid marker (`PAL120`); fresh W04 reported unknown annotation (`PAL130`) and callback-target failure. Thus cache availability changed strict admission for already-analyzed replacements. Causal code at that snapshot: `project.py` lines 184–186 keys only source bytes/import dependency closure, with `_source_dependencies` lines 209–223 reading import ASTs; `SourceGraph.analyze` (`checker.py` lines 802–816 at the earlier graph snapshot) skips bodies for cached files, so newly collected whole-graph replacement facts do not invalidate the reused result. Worker/orchestrator notified. W05/W06 are added for final resolution-transition retest.

## Ordinary Python import-priority probe

K09 must be run through actual `check_paths`/`analyze_file`, selecting only `app.py`, not by giving `analyze_sources` an artificial graph containing both candidates. The normal Python path finder resolves a same-name regular package before its `.py` module. `PathFinder.find_spec("dep", [str(root)])` is a non-executing resolution witness.

```json
[
  {
    "id": "K09-package-priority",
    "expected": 1,
    "selected_paths": [
      "app.py"
    ],
    "files": {
      "dep.py": "# mode: fun\ndef identity(value: int) -> int:\n    return value\n",
      "dep/__init__.py": "from pyalamode import fun\nprint(\"package initializer\")\n@fun\ndef identity(value: int) -> int:\n    return value\n",
      "app.py": "# mode: fun\nfrom dep import identity\ndef caller(value: int) -> int:\n    return identity(value)\n"
    }
  }
]
```

Interim actual observation: checker SHA-256 `5717df661c77a26b333f5a4a30d62284b0194e18195bcf63c479c4a67b01500a`, project SHA-256 `c2ef72705112af3f1b46c76ab3ba51473de0cc8d3606934f177e405bc2cf1b91`; CPython path finder selected `dep/__init__.py`, whereas `check_paths([root / "app.py"], root=root, cache=False)` returned status 0, loaded only `app.py` and `dep.py`, and reported checked pure initialization for both. The app dependency digest named only `dep.py`. Causal source: `_local_path` (`checker.py`, initially lines 734–742) tries `base.with_suffix(".py")` before `base / "__init__.py"`. This is a static false admission of effectful package setup and a dependency-identity mismatch, not unchecked runtime tampering. Worker/orchestrator notified; final retest required.

## Final frozen-code verification

**Outcome: no remaining actual false admission or checker exception was observed in this recorded bounded corpus.** Every previously reported admission/claim/cache issue above was corrected and retested. These results concern finite source rules and explicit dependency/input assumptions; they do not establish whole-Python soundness or user-study results. Full-suite macOS/Linux acceptance and commit remain orchestrator-owned.

Runtime: CPython 3.13.1 standard build, macOS 26.6.2 arm64. The source snapshot stayed unchanged through the final corpus and freshness runs. Frozen product SHA-256 values:

| Product artifact | SHA-256 |
| --- | --- |
| __init__.py | `203297da7fc44ded8fb1bf8179350ceb772cb1a1b6ddb6b29ed54ad80e619aaf` |
| checker.py | `107ea0fd7833d32e639d49ba4bd566dc99c82aea328c3c0836b959bc3fe4f62f` |
| model.py | `3539b23fd75ec8640e01e9a06c3083464d0b01facdefa62d133ac02f19cd1cfc` |
| project.py | `b983e1ce25bd99ddb97fce4ddffe20f571c2eb70af01aa17ea41709fd0ac8d41` |
| cli.py | `65288b5167680a5be3f4f418035a101538ccb921fd58cc56f04dc3f94cb71d89` |

Actual final APIs: `analyze_source`, `check_paths(..., root=..., cache=False)` for isolated project layouts, ordinary cached `check_paths` for transitions, and fresh `build_paths`. Application project sources were never imported by checking. K09 selected only `app.py`; a non-executing CPython `PathFinder.find_spec` confirmed the analyzed package initializer is the normal import target.

| Recorded checks | Final observation |
| --- | --- |
| 83 single-source fixtures | 83 expected statuses; no exceptions |
| 20 actual project layouts | 20 expected statuses, including all local foundation shadows and K09 package priority refusal |
| Six warm writer/resolution additions | Every cold/warm baseline passed; changed cached and fresh gates both returned 1; the affected caller lost its cache hit |
| G02 invalid transitive source | Middle/core results status 1, verified false, invocation and initialization evidence unverified |
| Recursive/cross-file/callback failure evidence | Required failure categories propagate; B05 known returned target remains precise `ZeroDivisionError` |
| I11 initializer division | Initialization separately lists `ZeroDivisionError`; independent identity invocation has no such failure |
| Audit and unguarded exports | Audit has no strict claim; accepted contracts remain unguarded with caller obligations |
| Static non-execution | No check/default/decorator/annotation sentinel file exists |
| Actual installed marker positive | Existing `examples/pricing.py` passes with one selected export and no diagnostics |

Cache body analysis was instrumented by temporarily wrapping the actual `FunctionalAnalyzer.function` method at runtime, recording source/qualified name entries, without changing implementation or test files. Indexing/signature preparation still runs; those operations are not counted as body analysis. The G01 four-file workload produced:

| Condition | Status | Actual function-body entries | Evidence reuse |
| --- | --- | ---: | --- |
| Cold | 0 | 4 | No hits |
| Unchanged warm | 0 | 0 | Four hits |
| Valid leaf edit | 0 | 3 | Leaf/middle/core fingerprints changed; unrelated fingerprint and hit retained |
| Unrelated edit | 0 | 1 | Leaf/middle/core retain three hits |
| Invalid leaf edit | 1 | 3 | All affected files unverified; unrelated hit retained |
| Successful/invalid build | 0 / 1 | 4 / 4 | Builds bypass body cache |
| Corrupted/deleted cache with invalid leaf | 1 / 1 | 4 / 4 | Same refusal after fresh analysis |
| Policy edit | 0 | 4 | Policy change invalidates prior keys |
| B05 unchanged warm | 0 | 0 | Concrete returned callback retains precise division failure; default retains the published conditional bound |

A successful G01 build copied all four source files byte-for-byte. Running its ordinary artifact with the same stock interpreter (`import core; print(core.caller(2))`) returned status 0 and printed `4`. The subsequent invalid dependency prevented a new output, and the prior artifact's complete file digests stayed unchanged. A controlled dependency edit immediately after the fresh check and before copying caused build status 2, no new output, and preserved the prior artifact. Removing/corrupting disposable cache never changed admission.

Final causal interfaces inspected: package-before-module resolution is now `checker.py` lines 680–693; the actual installed product initializer is identified at lines 696–697; cached source bodies skip `run` at lines 886–888 while concrete capture/return metadata is reconstructed at lines 869–885; project keys include transitive bytes and binding context at `project.py` lines 185–190. The original defective snapshot line citations are retained above as historical observations, not findings against these final bytes.
