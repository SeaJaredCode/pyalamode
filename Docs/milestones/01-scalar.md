# Milestone 1: statically checked scalar functions

Status: implementation complete; macOS tests, independent Linux acceptance run, independent adversarial review, guide verification, and named measurements passed. The orchestrator owns the final suite rerun and commit. Authority: `SPEC-sol6.1-composite.md` sections 1–6, 14, 16–18. No later capability is admitted by this increment.

## Delivered interfaces

- `pyalamode.fun(function)` returns the identical function. It neither registers nor wraps, inspects annotations, validates values, or creates check evidence.
- `pyalamode.checker.analyze_source(text, path="<source>", audit=False, policy=None)` supplies static text analysis; it does not certify the calling interpreter. `analyze_file` decodes Python source without executing it.
- `pyalamode.project.check_paths(paths=None, root=None, audit=False, target="cpython-3.13.1", cache=True)` checks source under the explicit runtime/policy gate. `build_paths(..., output=None)` freshly checks and atomically publishes an unchanged compatible source tree with `pyalamode-evidence.json`.
- `Diagnostic`, `FunctionContract`, `CheckResult`, and `ProjectResult` supply structured reports. Diagnostics carry stable rule, authored location, affected boundary, origin, reason, valid remediation, and first binding when relevant. JSON export claims separate enforcement, pure behavior, checked source evidence, foundation trust, characterized failures, freshness, unguarded boundary protection, and ordinary caller obligations.
- CLI: `pyalamode check [paths] [--audit] [--json] [--no-cache] [--root DIR] [--target cpython-3.13.1]`; `pyalamode build [paths] [--output FRESH_DIR] [--json] [--root DIR] [--target ...]`; `pyalamode explain PAL101` or `abs|min|max|len|fun`.

Strict status is 0 for a passing selected gate, 1 for unsatisfied verification, and 2 for tooling, policy, path, syntax, or unsupported-target failures. Audit findings alone return 0 and publish no strict claim; tooling errors remain 2. A passing gate with no participating exports explicitly publishes zero coverage. Build requires at least one selected export. Existing output directories are preserved and rejected; no failed gate emits a new checked artifact.

## Closed contracts and decisions

Top-level functions opt in using exactly one statically resolved `from pyalamode import fun` marker (including import aliases), or `import pyalamode as alias; @alias.fun`. Marker binding replacements, known module-attribute replacements through direct aliases/setters/namespaces, duplicate export definitions, additional decorators, defaults, nesting, async, variadics, and generic function declarations fail. An unrelated `object.fun` spelling does not opt ordinary code in.

Parameter/result annotations are exact `int`, `bool`, `str`, `bytes`, `None`, corresponding quoted strings, or a stable `from types import NoneType` import. Annotations are parsed rather than evaluated; user hooks, `Any`, unions, generics, custom classes, subclasses, and known shadowed/replaced type bindings fail.

Bindings use simple assignment or annotated initialization to one local name. A branch merge tracks both possible and definite initialization and all exact result alternatives. Exclusive branches may initialize once; second reachable initialization and missing initialization on a used path fail. Early returns remove terminated paths. Constant exact boolean branches are pruned. The checker deliberately does not solve correlations between separate conditions. `if` requires exact boolean conditions. `return`, `pass`, and ordinary function docstrings are supported. Excluded statement constructs stay excluded in dead source; provably unreachable admitted assignments do not create rebinding failures.

The operation catalog is exactly the authority's scalar catalog: integer unary `+`/`-`, integer `+`/`-`/`*`/`//`/`%`, same-type integer/string/bytes comparisons, string/bytes concatenation, boolean `not`/`and`/`or`/equality, right-hand literal `is None`/`is not None`, conditional expressions, `abs(int)`, `len(str|bytes)`, and two-or-more homogeneous exact integer/string/bytes positional `min`/`max`. There is no cross-type coercion, indexing, float, interpolation, user operators, protocols, mutable literal, ambient application constant, or checked-to-checked call support. `//` and `%` disclose `ZeroDivisionError`; resource exhaustion and interruption remain outside characterized failure claims.

Builtins resolve against actual analyzed lexical/module binding models. Local and module shadowing, global statements, match captures, direct/aliased `builtins` attribute writes, dictionary writes, recognized setters, and direct/aliased globals namespace writes cannot preserve approved binding evidence. Unchecked modifications outside these recognized static writes violate the published dependency precondition; there is no process monitor or protected namespace.

## Ordinary caller inspection scope

Ordinary shell source remains unchecked and receives no purity claim. Within each selected source file, the checker inspects calls whose direct lexical target resolves to a same-file selected export, plus stable direct same-scope name aliases of such an export. It covers executable expression sites in ordinary statements, branch/match/handler bodies, function defaults/decorators/annotations, class bases/decorators/keywords, lambdas, and comprehensions. Parameter, lambda, comprehension, and sibling-scope shadowing cannot turn a different callable into that export.

An exact literal, closed supported scalar expression, or one prior local/module scalar initialization without analyzed reassignment can establish an inspected argument. Ordinary parameter annotations do not prove exact inputs, and subclass construction, mutable values, unknown expressions, unpacking, missing/excess/duplicate arguments, and incompatible keyword forms fail `PAL221`. This inspection does not establish contracts for arbitrary dynamic aliases, objects storing functions, imported exports from other files, or ordinary higher-order dispatch. Those ordinary callers retain the unguarded export's explicit exact-type and stable-dependency obligations. Checked call graphs and cross-module resolution are milestone 2 work.

## Freshness and artifacts

Fingerprint inputs include original source bytes, authored path, edition, checker/operation versions, target, analysis mode, platform, accepted policy, dependency identities, and digests of the installed `fun`, checker, model, project/build, and CLI source artifacts. Source and policy edits invalidate subsequent checks; changed product implementation bytes also invalidate them even if version labels remain unchanged.

The disposable `.pyalamode-cache` is content addressed, checksum validated, and split by audit/strict mode. Missing, corrupted, unwritable, or deleted cache content triggers fresh analysis without changing the gate. It is local acceleration evidence, not an authenticated distribution format. Builds bypass the cache, analyze one captured byte snapshot, compare bytes again before copying, recheck policy, stage output privately, and publish only after every selected gate passes. Source/build evidence describes those artifact bytes and conditional dependencies; it is not a live execution certificate.

The artifact is a local ordinary source tree. Source bytes, value types, evaluation order, and body scopes are preserved. Artifact fingerprints and caller obligations are inspectable JSON. Distribution/installed-consumer claims, export guards, runtime revalidation, module initialization certification, and package claim discovery are deliberately not implemented.

## Verification and acceptance mapping

Local environment: macOS Darwin arm64, CPython 3.13.1 standard build at `/opt/homebrew/bin/python3.13`. Only that patch was run locally. The orchestrator also ran CPython 3.13.1 on Linux aarch64 in `python:3.13.1-slim`: the expanded 24-test snapshot passed on macOS in 1.022 seconds and Linux in 1.421 seconds. The final class-global dependency-write regression passed locally after that snapshot; the orchestrator performs the final frozen-tree rerun before committing. Other patches/minors, Windows, alternative interpreters, and free-threaded builds fail the runtime gate.

Commands run successfully:

```sh
/opt/homebrew/bin/python3.13 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest discover -s tests -p 'm01*.py' -v
.venv/bin/pyalamode check examples/pricing.py --no-cache
.venv/bin/pyalamode check --audit tests/fixtures/m01/invalid_reassignment.py
.venv/bin/pyalamode explain PAL101
git diff --check
```

The final suite runs 24 tests (0.749 seconds in the final local virtual-environment run), with parameterized adversarial subcases. A01 checks the example, unchanged build bytes, evidence dimensions, and execution via ordinary Python. A02 checks reassignment/augmented assignment and first locations. A03 checks exclusive branches, missing initialization, reachable reinitialization, literal branch pruning, and early returns. A04 rejects exact-int subclasses, booleans as integers, mutable values, unknown annotated shell parameters, alias arguments, and malformed call signatures. A05 ensures audit does not claim verification. A06 exercises unknown operators/calls/constructs and builtin shadows. A07 checks defaults/decorators/annotation hooks without source execution. A08 checks tooling/target statuses and no build output after failure. A33 checks marker identity, ordinary mutation, and unguarded subclass execution.

Additional regressions cover marker/builtin/type alias replacement, function/class globals writes, match captures, local builtins imports, sibling lexical callable aliases, class/default/annotation/match/lambda/comprehension call sites, stale source/policy/product artifacts, malformed/deleted cache, cache-independent build failures, atomic freshness rejection, and retained prior artifacts. Dead source still checks declaration, statement, expression, operand, and call contracts, while dead admitted assignments avoid false reachable-reinitialization findings. Independent review observed all 25 regression probes at expected statuses, plus 17 admitted and 22 excluded scalar expression cases without unexpected results; its source cases and observations are retained in `Docs/conformance/m01-cases.md`. The guide helper verified 14 commands and retained records in `Docs/evidence/m01-guide-verification.json`.

These results establish observed conformance for the bounded fixtures and static rules, rather than a proof about arbitrary dynamic Python. All checked behavior remains conditional on the published exact input and unchanged-dependency obligations.

## Performance and handoff

The helper's `benchmarks/m01_scalar.py` workload was run after the final implementation edits using `.venv/bin/python benchmarks/m01_scalar.py --output Docs/milestones/01-scalar-measurements-macos.json`. Full evidence is retained in [01-scalar-measurements-macos.json](01-scalar-measurements-macos.json). On an Apple M1 Pro MacBookPro18,1 (10 logical CPUs, 16 GiB RAM), CPython 3.13.1, it checked 32 generated files, eight selected functions each, 256 ordinary same-file calls, 70,176 source bytes, and 2,656 source lines. Checked function/cross-file dependency fanout is zero; each export has one inspected ordinary caller and one approved `max` operation. Five repetitions yielded:

| Named condition | Median elapsed seconds | Maximum traced Python allocation peak |
| --- | ---: | ---: |
| Cold analysis cache, checker already imported | 0.669538542 | 1,226,184 bytes |
| Warm unchanged sources, 32 cache hits | 0.035513458 | 662,343 bytes |
| One source-file edit, 31 hits/one miss | 0.055648708 | 657,756 bytes |

Measurements include `tracemalloc` overhead, cache reads/writes, and re-fingerprinting every file; imports, interpreter startup, fixture creation, JSON serialization, and application execution are outside the interval. OS page-cache state is uncontrolled. Memory figures are traced Python allocations rather than RSS. This demonstrates per-file incremental reuse for the named workload and makes no universal latency or later transitive-call-graph claim.

Independent Linux measurements of the same workload are retained in `Docs/evidence/m01-benchmark-linux.json`: CPython 3.13.1, Linux 5.15.49-linuxkit aarch64 container, five trials, cold median 1.083078542 seconds, warm 0.123151583 seconds, and one-file edit 0.1462 seconds. All expected per-file cold/warm/edit hit/miss checks passed. That JSON discloses the container, source snapshot, allocation peaks, and measurement conditions; it is a separate platform measurement rather than a native macOS/Linux comparison.

Implementation handoff files: `pyalamode/{__init__,__main__,model,checker,project,cli}.py`, `pyproject.toml`, `.gitignore`, `examples/pricing.py`, `tests/m01_scalar.py`, and `tests/fixtures/m01/invalid_reassignment.py`. README, the scalar guide example, and benchmark workload belong to the documentation/measurement helper. No commits were made by this worker; the orchestrator owns the ledger and commit.
