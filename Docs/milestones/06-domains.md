# Milestone 6: domain alternatives and characterized failure

Status: M6 engineering complete on the corrected frozen source. Independent native and installed Linux wheel verification, root gates and frozen-source measurements passed; human usability remains unmeasured. Authority: `SPEC-sol6.1-composite.md` §§3–5, 7–12, 16–18, especially A19–A20 and relevant A32. Prerequisite: independently verified milestones 1–5, M5 commit `f6ea4c1`. Root owns approval, ledger, source freeze, independent verification, release decision and Git.

## Published finite syntax before admission

All syntax is ordinary CPython 3.13.1. The checker parses source without importing or evaluating application code. No translation, registration, exception rewrite or special loader establishes the static claim.

```python
from pyalamode import variant, case, fun, Option, Some, Nothing
from pyalamode import Result, Ok, Err, accumulate, Failure, failure_value, Vector

@variant
class Lookup:
    @case
    class Found:
        value: int

    @case
    class Missing:
        pass

@fun
def describe(value: Lookup) -> int:
    match value:
        case Lookup.Found(value=number):
            return number
        case Lookup.Missing():
            return 0

@fun
def optional(value: Option[int]) -> int:
    match value:
        case Some(value=number):
            return number
        case Nothing():
            return 0

@fun
def quotient(number: int, denominator: int) -> Result[int, Failure]:
    try:
        return Ok(number // denominator)
    except ZeroDivisionError as caught:
        failure = failure_value(caught)
        return Err(failure)

@fun
def validate_pair(left: Result[int, str], right: Result[str, str]) -> Result[tuple[int, str], Vector[str]]:
    return accumulate(left, right)
```

Domain classes are top-level `@variant` declarations whose body contains only optional docstrings and one or more uniquely named public nested `@case` classes. Cases contain the M4 fixed public typed data fields and stable trailing defaults, or `pass` for no payload. Domain/case bases, metaclasses, type parameters, extra decorators, methods, descriptors, custom constructors/validators and behavioral attributes are refused. Schemas must be available before the outer domain begins evaluation; outer/self/sibling/forward case references are refused, and earlier outer-case bindings cannot shadow later case decorators. Nested cases are immutable exact slot data; the domain itself is an immutable closed namespace, not an instantiable superclass. Case construction uses `Lookup.Found(...)` with the record fixed positional/explicit-keyword signature. Annotations use `Lookup`, or a particular `Lookup.Found` where an exact case input is intended. `replace` stays a record operation; variant payload updates reconstruct a case.

Record/case class suites follow ordinary CPython evaluation: defaults evaluate against earlier class-local defaults and bind before their own nonpostponed annotations. Such bindings cannot silently acquire a builtin/type meaning. Explicit string/future annotations use the product's separate module namespace parser; defaults still use class-local values. Outer-domain case bindings do not become inner-case field locals.

`Option[T]` has the complete case set `Some(value: T)` and `Nothing()`. `Result[T, E]` has `Ok(value: T)` and `Err(error: E)`. Their type arguments must be recursively admitted data; capabilities and callable payloads are excluded. Constructors are `Some(value)`, `Nothing()`, `Ok(value)`, `Err(error)` with fixed positional or named payload fields. The exact constructor case is tracked; matching a case value against its containing Option/Result/domain annotation requires its known payload schema. No implicit coercion or annotation-driven constructor execution occurs. Option/Result generic aliases provide schemas, not generic application inference.

`accumulate(left, right)` accepts exactly two positional established Result schemas with identical error schema E, evaluates its ordinary arguments in Python order, and returns `Result[tuple[T, U], Vector[E]]`. Two successes produce the pair; one or two errors produce an immutable Vector in left-to-right argument order. It does not short circuit independent input computations. Its implementation operates only on exact product Result cases and validates payloads; arbitrary iterable/error hooks are excluded. Repeated binary accumulation of already accumulated errors changes E to Vector[E] visibly; flattening, builders, loops and arbitrary variadic signatures are outside this increment.

`Failure` is exact immutable data with fields `category: str` and `message: str`. `failure_value(caught)` accepts only an opaque live handler-bound exception token in checked code. Runtime conversion recognizes only the published exact builtin exception classes (including the finite OS subclasses listed in the runtime catalog), maps them to a supported failure category, and returns a fixed category-specific message; it does not read exception dictionaries, traceback, frames, custom attributes, arbitrary `args` or formatting hooks. Ordinary invalid exceptions fail explicitly. Direct `Failure(category, message)` construction is admitted only as ordinary immutable data construction, with exact strings; it does not manufacture a characterized raised exception or validate an actual occurrence.

## Pattern, binding and coverage contract

Checked `match` operates on an established closed domain/Option/Result case schema, an exact record, or an exact scalar finite singleton domain (`bool` and `None`). Class patterns resolve to unchanged characterized exact product cases or records. Positional patterns follow declaration field order; explicit field-keyword patterns must be unique and known. Supported nested payload patterns are fresh captures, `_`, exact scalar literals/singletons and characterized record/case class patterns. A full-case pattern has only irrefutable captures/wildcards or exact irrefutable record/single-case patterns in every inspected field; a nested particular case of a multi-case domain/Option/Result constrains the outer case rather than exhausting its payload; omission of a field is irrefutable for that field. Literal or nested constrained payload patterns do not cover an entire outer case. Sequence, mapping, star, OR and arbitrary value patterns are refused in M6.

Every pattern capture must be fresh on its reachable path. Class/payload patterns whose attempts can partially bind before failing are refused when they contain named captures; this avoids depending on unspecified failed partial bindings. Captures in guarded cases are refused because a false guard can leave them initialized before a later case. Guarded capture-free cases may use exact bool guards, are analyzed for operations/effects/failures, and supply no coverage unless the guard is statically literal `True`. Guard coverage never follows from merely spelling a supported case.

An explicit final `_` covers every remaining present and future case when project policy permits it. Without a wildcard every declared case must have a full-case unguarded pattern (or literal-True guard), regardless of whether branches return. An exact record subject requires an irrefutable record or wildcard branch. Exhaustiveness is reported as explicit case evidence plus the stable case-set fingerprint, or deliberate wildcard evidence. Adding a case changes dependency/cache freshness and rejects an incomplete explicit consumer; a deliberate wildcard consumer remains admitted. Project policy `explicit_cases = ["module:Domain", ...]` requires selected source-declared domains to have explicit full-case coverage and refuses wildcard consumers of those domains. Policy selectors must resolve to a checked top-level domain.

`match` does not create a lexical scope. Successful branch captures and body assignments merge by the existing once-binding/definite-initialization rules; a name absent from a continuing branch cannot be used afterward. Returning branches do not contribute a continuing environment. Checked nested functions may capture only existing stable admitted data and callable evidence, subject to enclosing writes; pattern captures do not license mutable or capability capture.

## Handler, failure and effect contract

Checked handlers are ordinary `try` bodies followed by one or more `except KnownCategory` or `except (KnownCategory, ...)`, optionally `as fresh_name`. M6 supports the characterized categories `ZeroDivisionError`, `IndexError`, `KeyError`, `ValueError`, `RecursionError`, `RuntimeError`, `OSError`, and `UnicodeError`, resolved to unchanged builtins. A ValueError handler also discharges the supported UnicodeError category, and RuntimeError discharges RecursionError, matching builtin inheritance. Category overlaps are rejected, including UnicodeError/ValueError and RecursionError/RuntimeError overlap; broad Exception/BaseException, bare except, user classes, arbitrary exception construction/raise, `except*`, `else`, and `finally` have no M6 contract.

The `as` target remains the real mutable Python exception at runtime. Statically it is an opaque handler-local token, admitted only as the direct argument of `failure_value`. Assignment aliases, attributes, subscripting, returned values, payload construction, callable capture, arbitrary calls and formatting of that token are refused. The target must not already be initialized. Python deletes it after every handler exit; the checker marks it unavailable afterward and rejects later rebinding of that cleanup name. This cleanup slot is distinct from a normal stable binding and never creates immutable exception evidence.

Handler entry uses only the environment established before the try. Names initialized inside the try may already exist at an exceptional exit, so handlers cannot initialize a name written anywhere in the try body. Handler-body stable names may be initialized in mutually exclusive handlers and merge with the successful body only where every continuing path establishes them. Try-local names are not assumed available on a failure path. The conservative rule is published rather than inferring arbitrary exceptional control-flow positions.

Every performed operation retains its known failures unless its occurrence is enclosed by a supported matching handler. Direct operations and conditional callback failure upper bounds record that mask. Concrete checked calls retain per-invocation handled-category masks separately from target/dependency evidence; graph closure adds the callee's unhandled failures, preserves its operations and trust, and always retains its required/declared effects. Handler-body failures are outside that handler's own mask but inside any enclosing try. Recursive graph failures follow the same edge rules. Cache serialization restores these exact masks, explicit case evidence, immutable schema identities and concrete callback targets on warm and partial checks. No broad-except spelling alone proves safe handling.

Handled pure arithmetic failure propagates no effect permission. A caught IO/Clock/Random/State/Environment operation still requires its family. Failure conversion does not erase performed effects. Borrow entry/exit and logical capability lifetime remain the M5 contract; an exception token cannot expose capabilities or mutable cleanup state.

## Runtime, boundaries, freshness and evidence

The runtime worker owns new `variants.py`/`failures.py` and minimal records/collections/boundaries hooks. The main worker owns exports, checker/model/project/CLI/guard generation and static fixtures. Both use one immutable identity-only metadata catalog for exact domain cases and recursive schemas. Runtime constructors reject nested mutable data, exact-type subclasses, proxies, callables/capabilities, cycles and foreign hooks before consulting arbitrary metadata. Cases are unhashable, have exact type-sensitive value equivalence and deterministic declaration-order representation using the existing approved data vocabulary; strict formatting remains unsupported.

Snapshots deeply validate admitted variants and can reuse them; fresh exports use the exact ordinary dict envelope `{"variant": domain_identity, "case": case_name, "fields": field_dict}`: domain_identity is the declaring module plus `:` plus its qualified domain name (builtin domains use `pyalamode:Option` and `pyalamode:Result`); field_dict follows declaration order and contains recursively fresh exports. Failure exports follow the existing record dict field contract. No arbitrary restoration hooks or implicit case decoding are added. Generated off/exports/debug modes admit these supported variant/Option/Result/Failure data schemas while continuing to refuse Callable/Effectful/capability boundaries. Guard failure points identify authored boundary locations and validate exact tags and nested payloads. Guard generation never imports application code while checking/building.

Source/domain schemas carry stable case-set and ordered field-schema fingerprints. Current product-file fingerprints expand to include actual variant/failure implementation bytes and characterize their actual builtin/dependency inventory; analyzed source aliases/helper writers/class replacements cannot hide behavioral mutation. Exact source evidence, library trust, failures, effects, caller obligations, initialization and optional boundary protection remain separate report dimensions. Domain-only builds work without a selected function. Ordinary unchecked initialization and source/library rebinding remain explicit obligations.

Acceptance evidence will include positive closed-domain, Option/Result and two-error accumulation workflows; retained versions and nested record payloads; negative guarded/partial capture, incomplete/exact-policy wildcard, subclass/proxy/helper writer and exception reflection/escape cases; native and Linux warm case addition and partial callback/handler graph checks; immutable conversion/export/guards; source nonexecution sentinels; actual off/exports/debug CLI build/run and failed-gate no-output checks. Full existing tests plus M6 run on actual native `.venv/bin/python` and Docker `python:3.13.1-slim` with networking disabled. Frozen-source timing/memory costs compare ordinary library behavior and optional guards. Human authoring benefit remains unmeasured.

No loops, generators, async, general Python pattern dispatch, standard functional operations, external trust, editor, package consumer, builders, Task, dialect, schedules or CatWrangler workflow are introduced. Root explicitly approved this published plan before application implementation. Product, test and example source remains frozen after the contained-case dependency correction and completed independent final gates and measurements.


## Implemented engineering gates and handoff

Main-worker changes are `pyalamode/{__init__,checker,model,project,cli,guardgen}.py`, `tests/m06_domains.py`, `examples/domains/{domain,demo}.py`, this milestone contract and README. Runtime-helper changes are `pyalamode/{variants,failures}.py` plus minimal records/collections/boundaries hooks, `tests/m06_runtime.py`, `benchmarks/m06_domains.py` and the runtime contract/evidence. Independent review owns `Docs/conformance/m06-cases.md`. Root owns the orchestration ledger and Git. No worker committed changes.

The checker version is `domains-failures-6.0`, operation contract `scalar-tuple-call-collection-record-boundary-effect-domain-failure-ops-6`. Exact product fingerprints now cover twelve actual files: `__init__.py`, `variants.py`, `failures.py`, `effects.py`, `collections.py`, `records.py`, `boundaries.py`, `guardgen.py`, `model.py`, `checker.py`, `project.py`, and `cli.py`; the independently frozen installed inventory additionally covers `__main__.py`. `FunctionContract` adds `direct_failures`, per-occurrence `failure_edges`, `patterns` and `handlers`; `CheckResult` adds `variants`. Project coverage reports `selected_variants` separately from functions/records. Cache restoration retains direct failures and rebuilds transitive failure closure through occurrence masks, keeping effect/dependency/trust evidence separate.

The 18 main M6 regression tests include complete declared cases and nested records, Option/Result workflows, full-schema binary accumulation, constrained/guarded/wildcard coverage, bool/None finite patterns, class/field/default availability and actual class-suite evaluation, opaque failure conversion, cleanup/partial-try collisions, per-occurrence/nested handler masks and retained Clock effects, inherited builtin overlap, case-addition/partial warm checks, class/private foundation writers, private-public foundation aliases, generated-prefix collision protection, contained builtin case/family identity and nested schema invalidation across three public/private writer routes and cold/warm/guard gates, nonexecution and real off/exports/debug artifacts. Parameterized subcases supply adversarial breadth; test count is not the case count. The runtime helper adds 30 tests to the inherited 194-test suite, for 242 total tests.

Independent review identified and retained corrections for called `@variant()` disappearing from coverage, nested full-case patterns falsely exhausting multi-case payloads, a private helper writer reference tooling crash, unused pattern/handler name collisions with generated guard names, inherited record/new-case class-local initializer/annotation lookup, and parent Option/Result schemas retaining invalid contained case assumptions. Each correction has a meaningful implementation regression. Human usability and authoring time remain unmeasured.

The ordinary domain example checks four functions, one record, one closed variant and one functional initializer, then prints `Ada`, `Ada`, `Ok(value=4)`, an immutable ZeroDivisionError Result, two left-to-right validation errors, and `Ok(value=(12, 'Ada'))` through stock Python. `pyalamode explain variant`, `case`, `Option`, `Result`, `accumulate`, `Failure`, `failure_value`, `handlers` and `match` describe the closed catalog. Source checking/building does not evaluate example declarations or shell hooks.

The final two-platform suite outputs, independent literal/project/actual CLI counts, exact source snapshots and named measured costs below establish the completed engineering handoff. Root retains the release decision and Git work.


Current refrozen engineering suite: actual native `.venv/bin/python -m unittest discover -s tests -p 'm*.py' -q` passed all 242 tests in 4.631 seconds; actual `docker run --rm --network none -e PYTHONPATH=/workspace -v /Volumes/Projects/pyalamode:/workspace:ro -w /workspace python:3.13.1-slim python -m unittest discover -s tests -p 'm*.py' -q` passed all 242 tests in 14.355 seconds. Both are CPython 3.13.1 standard builds on the supported platforms. Compilation of owned Python files and `git diff --check` also passed. These elapsed suite times are observed verification costs, not workload benchmarks or cross-platform speed comparisons.

The final correction ties Option schemas to unchanged Some/Nothing behavior and Result schemas to unchanged Ok/Err behavior, including recursively nested records, cases, tuples and collections and consumers that only return their input. Source writer aliases from exported names or the installed variants submodule retain canonical foundation identities in cache context. The unaffected builtin family can remain admitted when a precise public case writer changes only the other family. Private product helper/catalog writes may still invalidate the whole product vocabulary conservatively.

Independent review passed all 236 literal sources (73 admitted, 163 refused), 595 focused assertions and all 242 tests on both native CPython 3.13.1 and an actual installed Linux wheel. The focused gates include 207 project assertions across 28 layouts/85 check/build gates, 192 runtime assertions with zero foreign hooks, 76 actual CLI assertions covering 34 CLI invocations and five stock-Python artifact executions (37 recorded rows plus two separately asserted artifact subprocesses), 78 assertions over fourteen nonexecution sentinels and a separate initialization control, and 42 copied-product freshness assertions over twelve isolated transitions. All 70 reviewed input identities remain unchanged before/after, equal across platforms and equal to current checkout bytes; all thirteen imported product Python files match the checkout. The fixed literal corpus SHA-256 is `15cc3949409763e122db23262cf1c7a842821a9145d63286434c0daace4721bd`; the complete independent cases and evidence are in [the conformance report](../conformance/m06-cases.md). Root independently reran the corrected refrozen candidate: all 242 tests passed on native CPython 3.13.1 in 4.775 seconds and Linux CPython 3.13.1 in 14.739 seconds. Root's 23 installed CLI/execution/negative-build/explanation gates also passed, covering all M6 workflows in three guard modes, unchanged off/export source, retained Clock effects with known-failure conversion, two invalid guarded inputs, six rejected builds with no artifact/source execution, and documented explain targets.

The runtime helper completed repeated measurements of the approved sizes 10 and 100 across off/exports/debug modes on the corrected frozen product: 36 rows, 108 timed intervals and 2,700 measured operation calls plus 360 warmups per platform. Root independently parsed all rows and compared all twelve product and eight owned-source SHA maps: they are current, unchanged before/after each run and equal across platforms. Correctness and the separate Clock/Effectful/borrow failure-conversion smoke passed. The source scopes and complete identity tables are in [the measurement report](../evidence/m06-runtime-measurements.md), with raw [native JSON](../evidence/m06-runtime-macos.json) and [Linux JSON](../evidence/m06-runtime-linux.json).

At n=100, constructing a typed domain payload had off-mode median 1.930142 ms/call on native macOS and 2.388532 ms/call on Linux. Converting the actual zero-division failure to immutable Failure/Err had off medians 0.079508/0.094965 ms/call. Binary two-error accumulation over two n-tuple Vector payloads had off medians 7.538828/9.288220 ms/call, exports 14.182192/19.369765, and debug 21.399738/28.414288. These rows include perf_counter/tracemalloc and loop/disposal work, retain only the last result, and exclude setup/build/import/counter/warmup/correctness work. Memory is traced Python allocation, not RSS. Distinct operation paths and optional repeated deep assertions do not establish a general speedup or general application latency claim; OS caches/system load are uncontrolled. Human authoring benefit remains unmeasured.

The fixed measurement catalog has ten exact cases, three domains and one Failure record. Counted deep assertions are off 0 for every condition; exports 3/2/2/3/3/3 and debug 6/4/4/7/7/6 for construct/domain-match/option-match/success/failure/accumulation respectively. Constructor validation remains ordinary library behavior with guards off; matching existing data has no mandatory repeated deep guard. The [runtime contract](../evidence/m06-runtime-contract.md) separately publishes exact categories, wires, aliases, native/class/module foundations, setup behavior, asymptotic storage/lookup/validation costs and licensing assumptions. Focused runtime tests passed 30/30 on native 0.003 seconds and Linux 0.007 seconds. M6 implementation, engineering verification and measurement handoff are complete. Root retains final acceptance and commit ownership; human authoring benefit and usability remain unmeasured.
