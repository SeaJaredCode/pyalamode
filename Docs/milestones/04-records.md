# Milestone 4: records and explicit boundaries

Status: implementation, frozen two-platform engineering verification and handoff documentation complete; product/test/example source remains frozen for root-owned final acceptance and Git staging. Authority: `SPEC-sol6.1-composite.md`, especially §§3–5, 8–10, 14 and 16–18; prerequisite M3 commit `1675e94`. This increment implements A14–A16 and A34–A35, relevant A32 dispatch gates, and preserves earlier scalar/module/collection guarantees. Root owns the ledger, Git staging and release decision. No effects, variants, static patterns, general loops, generators, builders, concurrency, dialect, package-consumer verifier, schedule or CatWrangler workflow was added.

## Concrete public contract

The normal package exports `record`, `replace`, `freeze`, `thaw`, `dataclass_adapter` and `namedtuple_adapter` alongside existing `fun` and collections. `fun` still returns the identical function without checking, wrapping or registration. Records/conversions are ordinary product library implementations. Guards are optional generated ordinary Python, selected independently of the static rules.

```python
from pyalamode import Vector, fun, record, replace

@record
class Customer:
    name: str
    tags: Vector[str]

@fun
def tag_customer(customer: Customer, tag: str) -> Customer:
    tags = customer.tags.appended(tag)
    return replace(customer, tags=tags)
```

`@record` selects a top-level fixed declaration even in an ordinary module; record-only checked builds work. It accepts public typed data fields and stable trailing defaults. Required fields precede defaults. Constructor arguments may be positional or explicit keywords. `replace(record, /, **changes)` accepts one exact receiver and explicit known field keywords, validates old/new data, and returns a new record. Receivers are positional-only so public fields named `self` and `value` work. Ignored replacements fail PAL250. Field reads and same-exact-record-type equality are characterized; scalar/record distinctions and recursive contents participate in equivalence, and declaration field order determines record traversal. Static `is None` remains the existing singleton operation; allocation identity is excluded.

The checker rejects record bases/metaclasses/type parameters, multiple decorators, dynamic/private fields, descriptors, methods/properties, custom constructors/validators, callable fields, mutable or mismatched defaults, and analyzed replacement of class/behavioral definitions. This finite M4 record shape deliberately refuses forward/recursive record schemas, including nested tuple/collection forms and postponed strings. Imports/aliases, the record marker, annotations and defaults must be available at their Python evaluation point. Function recursion remains supported separately. Runtime `__match_args__` enables ordinary Python record patterns; static matching belongs to M6.

The library creates exact slot classes and validates complete recursive field schemas. Assignment/deletion/reinitialization/subclassing are refused, and instances have no mutable dictionary. Records are unhashable. Representation uses only supported scalar/tuple/collection/record vocabulary; strict formatting/representation remain unsupported, and ordinary repr retains CPython's configured exact-int decimal-formatting `ValueError`. The library data metadata is an identity-only immutable tuple of record classes/field schemas/defaults. It supplies construction invariants, never function-purity evidence or runtime certification.

## Explicit snapshots and independent exports

`freeze(value, *, exclusive=False, adapter=None, schema=None)` is an ordinary-shell boundary. Exact list becomes Vector; exact tuple becomes tuple; exact dict becomes OrderedMap preserving insertion order; exact set/frozenset becomes Set. Map keys and set members retain the M3 homogeneous exact scalar domain. Admitted stable data can be deeply validated and reused. Unordered Map construction remains an explicit visible choice.

Every recursively reached mutable builtin or named adapter source requires exact `exclusive=True`. This is the caller's assertion of exclusive access throughout snapshotting, not detected ownership or an acquired lock. Missing/false assertions fail before a mutable input is traversed. Observed size/iteration instability fails, but same-size concurrent writes cannot be universally detected. Violation of the assertion supplies no consistent-snapshot claim. No synchronized route is offered without a characterized synchronization contract.

Conversion accepts repeated acyclic references by value and does not preserve object identity. It retains no mutable alias into source storage. Cycles, subclasses, arbitrary objects, live views, cursors/capabilities, foreign constructors/getters/iterators/hash/equality/formatter/restoration hooks and unsupported keys/members fail with a nested path. Supported input checks occur before foreign metadata lookup. A named adapter can qualify a narrow foreign storage shape; it does not create a generic foreign-object hole.

`schema=Vector[int]`, an exact product record class, or another closed schema validates the completed result. The checker recognizes a simple stable ordinary assignment of the form `snapshot = freeze(raw, exclusive=True, schema=Vector[int])` as exact output data for a subsequent analyzed checked call. Shell parameter annotations do not establish data, local shadowing cannot establish a foundation schema, unknown mutable input requires the explicit assertion, and omitted schemas for unknown input remain unknown. Stable admitted source expressions can establish their existing schema. The analyzed shell/provider and mutable read are still unchecked. Invalid conversion can fail before reaching the checked computation.

`freeze`, `thaw` and adapter factories have no M4 pure strict-body/default/functional-initializer call contract. A pure computation starts after the explicit ordinary boundary. `thaw(admitted)` deeply validates then allocates a fresh list for tuple/Vector, dict for Map/OrderedMap, set for Set, and field dict for records. Every container occurrence and repeated export is independent; scalar leaves may reuse exact immutable values. Mutating an exported nested container cannot mutate the strict source or another fresh export.

## Finite named record adapters

`dataclass_adapter(ExactSourceClass, ExactTargetRecord)` and `namedtuple_adapter(ExactSourceClass, ExactTargetRecord)` return immutable named adapter metadata. `freeze(source, exclusive=True, adapter=adapter, schema=TargetRecord)` copies supported fields and constructs the exact target with complete nested validation. The source class itself never becomes admitted strict data. `frozen=True`, a hash method or a setter restriction alone provides no compatibility evidence.

The direct dataclass shape uses exact ordinary generated dictionary storage, target field order, generated constructor/repr/equality/match behavior, stable defaults and optional standard frozen setters/hash. Inheritance, slots, factories, keyword-only fields, ordering, post-init/custom methods, constructors and descriptors fail. Namedtuple qualification requires a direct standard generated tuple class, target field order, exact generated methods/getter indices/match metadata, empty slots and stable suffix defaults. It excludes arbitrary subclasses/custom namedtuple behavior.

The qualifier compares actual generated method code, defaults, globals/builtins and closures with a trusted installed-stdlib reference generated from exact field names/object metadata/stable defaults. Foreign dictionary keys and code-name metadata are checked before lookup. The reference uses a constant docstring and `inspect.get_annotations(..., eval_str=False)` only on product-generated metadata. Standard reference generators may execute their own generated source; application annotations, defaults factories, constructors, properties and restoration hooks are not evaluated by checking or qualifying. Physical source storage is read through retained exact builtin descriptors/tuple operations, then field contents are recursively snapshotted. Later unchecked mutation violates the stated source/product dependency assumptions; no live identity monitor is installed.

The [runtime contract](../evidence/m04-runtime-contract.md) publishes the exact qualifier and Python call-stage limit: CPython may dispatch string-subclass keyword-key hashing/equality while binding `**kwargs` before product code starts. Product validation rejects such keys before further foreign dispatch; it does not claim to control Python's earlier call-binding step.

## Guard selection, generation and coverage

```toml
[tool.pyalamode]
boundary_guards = "exports"
guarded_exports = ["core:quote", "domain.customer:tag_customer"]
```

`boundary_guards` is `off` by default, `exports`, or `debug`. `guarded_exports` lists exact selected top-level public `module:function` boundaries. Unknown/misspelled names, duplicate selections, invalid nested/private names, ambiguous module identities, generated namespace conflicts and off-with-selections fail tooling policy. Exports mode requires at least one explicit selection; debug can assert supported selected data without a public selection.

The build generates an ordinarily importable mirror façade under `pyalamode_exports`, for example `from pyalamode_exports.domain.customer import tag_customer`. Evidence names this façade as the selected guarded public boundary and separately names the original unguarded function. In exports mode original application bytes remain unchanged and original function identity remains available through the façade's `__wrapped__`. Original internal calls keep calling the originals with no generated wrappers or repeated deep validation. The generated façade preserves positional-only/keyword-only/default behavior and uses actual original default objects at ordinary import time; the build never evaluates defaults/annotations. Selected parameter/result Callables fail the finite M4 guard gate rather than acquiring annotation-only purity evidence.

Generated schemas are closed scalar strings and ordinary tuples for fixed/homogeneous tuples, collections and exact record classes/field schemas. Guards never evaluate user annotations, coerce/freeze inputs, or invoke foreign getters/iterators/hash/equality/formatters. They validate recursively exact argument schemas before body entry and returned data afterward, identify authored file/boundary/value paths, and reject nested mutation, subclasses, bool-as-int and wrong erased generic contents. These are additional data checks. They do not prove effects/callback purity/capture stability/ownership, prevent all unchecked tampering, or certify shell behavior.

Debug mode additionally inserts supported data assertions at selected function parameters, local data bindings and explicit returns in copied source. Callable assertions are excluded and the caller's evidence obligations remain. Generated temporary/import/record-alias names avoid source parameter/local/import collisions. Own record class references use aliases after their original declarations, so executing the copied module as `__main__` does not import/initialize it twice. Imported record aliases resolve at assertion-bearing function invocation, preserving module import order and safe deferred module cycles. Reports enumerate supported parameter/local/return coverage. Debug can repeat deep traversal and adds import/temporary allocation overhead; it is optional.

Generated debug/facade Python is compiled without execution before publication. Syntax/type/schema/generation failures are tooling errors and leave no artifact. Builds also reread source, policy and installed product bytes after generation and fail atomically on relevant change. No specialized loader, VM, namespace monitor or per-invocation certificate lookup is needed.

## Static evidence, freshness and initialization availability

Record evidence separately carries enforcement, behavior, source evidence, trusted implementation, trust list, failure dimensions, freshness, boundary protection and caller obligations. A successful record declaration is source checked; generated product record methods remain trusted library implementation. Definition/default failures are separate from valid construction/replacement's conservative `RecursionError` bound. Invalid ordinary field data/signatures can raise `TypeError`, and rejected mutation/reinitialization can raise `AttributeError`; those are outside admitted data contracts. Audit/failed/dependency-failed declarations are unverified and publish no successful checked claim. Optional function guards remain distinct from unconditional library constructor invariants.

Checked function operation evidence records `Record.construct`, `Record.field`, `Record.replace` and `Record.equivalent`, and propagates concrete/transitive dependencies and failure bounds. Records expand closed recursive data admission without admitting Callable payloads, unordered traversal, arbitrary dispatch or mutable data. Existing generic collection obligations/callback evidence and canonical error/order contracts remain intact. Constructor/replacement validation failure for invalid ordinary input does not expand a pure checked callable's valid-input failure universe; M4's new valid recursive operations use the already characterized `RecursionError` bound.

The checker rejects known direct/module/imported/assigned-alias setter/deleter/class dictionary writer routes to record/function/collection behavioral definitions. New record/boundary foundations include exact type/slot/code/module identities, runtime annotation parsing, installed standard dataclass/namedtuple reference generation and their finite transitive dependencies. `RECORD_FOUNDATIONS` is a dependency inventory, not application-call admission. Record/boundary helper-module writes conservatively invalidate their data families. The inherited collection helper-module wildcard gate can also invalidate unrelated scalar marker claims; this whole-product conservative exclusion is distinct from individual builtin/stdlib dependency gates, which preserve unrelated scalar behavior/cache hits. Import closures and body cache reuse remain conservative; minimal invalidation is not promised.

Relevant source, policy, checker/operation versions, foundations, selection settings, dependency/writer identities and installed product byte hashes participate in cache/build freshness. New `records.py`, `boundaries.py` and `guardgen.py` hashes are included alongside the existing product files. Warm decoding restores record metadata and recursively serialized record schemas, and never upgrades audit or failed evidence. Original-source hashes and generated-artifact hashes are recorded separately.

Review exposed an inherited initialization gap: a complete static function graph could accept cyclic from-imports whose stock Python import fails on a partially initialized definition. M4 adds a finite fail-closed gate. Cyclic direct from-imports and eager cyclic namespace reads in constants/defaults/record fields/non-postponed function annotations fail PAL241 with an initialization-cycle origin. Pure namespace module imports with deferred body references or postponed/string function annotations remain supported. The gate is conservative; it does not establish all possible Python import behavior. Rejected initialization/dependency evidence is unverified, including subsequent warm checks/builds.

## Costs, measurement and verification

The [runtime contract](../evidence/m04-runtime-contract.md) publishes algorithm/storage bounds, dependency assumptions, licensing and retained-value behavior. Record construction/replacement retains O(f) outer slots for f fields, with old/new deep validation. Field reads are O(1). Record metadata lookup scans R known classes by identity, adding O(R) per relevant visit; metadata declaration copies growing tuples. Snapshot copying is by occurrence with no identity deduplication; nested constructors can revalidate descendants, yielding O(Nh) work plus scalar key/member sorting for N occurrences and depth h. Thaw validates and allocates independently by occurrence. No tree-sharing update, universal latency or ownership-detection claim is made.

The [benchmark](../../benchmarks/m04_boundaries.py) builds real off/exports/debug artifacts. Its selected entry makes eight direct checked leaf calls over a Vector of exact `(int, bool)` tuple payloads. Untimed instrumentation observes 0/2/28 deep assertion calls for off/exports/debug. Exports has no leaf entry guards; debug adds the documented parameter/local/result sites. Instrumentation is removed before timing. Separate nested list/dict workloads verify snapshot isolation and fresh thaw exports. Timings include validation/conversion/allocation/calls/loops and `tracemalloc` overhead; exclude build/import/fixtures/counting/correctness probes/environment hashing/JSON writing. Memory is traced Python allocation, not RSS; OS page cache is uncontrolled. Platform JSON must retain before/after unchanged product/runtime/test/harness snapshots and current byte comparison. Human authoring-time/usability targets remain unmeasured.

Final evidence is the [measurement report](../evidence/m04-runtime-measurements.md), [macOS JSON](../evidence/m04-runtime-macos.json) and [Linux JSON](../evidence/m04-runtime-linux.json). Each platform passed ten conditions at n = 100 and 1,000, with three trials and 25 calls per trial (30 measured intervals/750 calls per platform). Both unchanged-before/after maps match each other and all nine current product files plus owned runtime/test/harness files. Generated artifact hashes are recorded separately because authored temporary paths differ across platforms. Runs were concurrent with uncontrolled system load/scheduling/page-cache state; these are named traced-workload observations. The off workload returns existing data and its tiny timing does not estimate normal application cost. Record/adapter costs above are algorithm bounds, not measured record-construction latency.

At n = 1,000, median milliseconds per call and maximum traced peaks were:

| Condition | ms/call macOS / Linux | peak bytes macOS / Linux |
| --- | --- | --- |
| Actual generated off | 0.000272 / 0.000233 | 112 / 112 |
| Actual generated exports | 37.744 / 47.601 | 2,135 / 2,031 |
| Actual generated debug | 505.766 / 673.360 | 2,131 / 2,027 |
| Nested mutable snapshot | 56.612 / 71.551 | 345,782 / 345,782 |
| Independent nested thaw | 17.809 / 22.103 | 196,104 / 196,104 |

Debug's repeated deep assertions have substantial cost in this data-returning call graph; exports bounds checks to the selected entry/result, and off does none. Low assertion peaks represent temporary validation stack/path objects; conversion/export peaks include newly allocated nested containers. `tracemalloc` is included, so these figures do not establish untraced production latency. The JSON retains each observation and exact environment. macOS used CPython 3.13.1 standard GIL/Clang 16 on Apple M1 Pro arm64, ten logical CPUs and 16 GiB memory, macOS 26.6.2. Linux used actual `python:3.13.1-slim`, CPython 3.13.1 standard GIL/GCC 12.2, aarch64 LinuxKit/glibc 2.36, five visible logical CPUs and about 8.23 GB visible memory, with no reported cgroup maximum. There is no universal performance or authoring-speed claim.

Frozen local verification on CPython 3.13.1 standard GIL macOS arm64 passed **149 tests**: 93 inherited, 25 new static/build and 31 new runtime. Root independently ran the same frozen suite on macOS (2.491 seconds) and actual Linux (7.591 seconds), both 149/149. `git diff --check` passed. The record example strictly checks two functions, one record declaration and one functional module; ordinary execution prints an unchanged original Customer, a new tagged Customer, count 2, and independently mutated export. Root's 39 independent gates covered nested Cart/Line records, collection folds/replacement, analyzed snapshot callers, self/value fields, alias-writer/late-marker negatives, actual installed CLI off/exports/debug builds and ordinary execution, internal function identity, malformed nested before-body rejection without hooks, three failed builds with no artifact, and record demo isolation. Source snapshots were unchanged. The independent reviewer owns the additional literal/project/runtime/guard corpus observations in [M4 conformance](../conformance/m04-cases.md). These observations do not prove arbitrary dynamic Python behavior or human usability.

```sh
.venv/bin/python -m unittest discover -s tests -p 'm0*.py'
.venv/bin/python -m pyalamode check examples/records --no-cache
.venv/bin/python -m examples.records.demo
.venv/bin/python -m pyalamode explain record
.venv/bin/python -m pyalamode explain freeze
.venv/bin/python -m pyalamode explain guards
.venv/bin/python -m pyalamode check tests/fixtures/m04/nested_record_mutable.py --no-cache
```

## Ownership and downstream handoff

This worker owns `pyalamode/__init__.py`, `checker.py`, `model.py`, `project.py`, `guardgen.py`, `cli.py`, `tests/m04_records.py`, `tests/fixtures/m04/*.py`, `examples/records/*.py`, README and this report. The root-dispatched runtime helper owns `records.py`, `boundaries.py`, collection record hooks, `tests/m04_runtime.py`, `benchmarks/m04_boundaries.py` and `Docs/evidence/m04-runtime-*`. The independent reviewer owns `Docs/conformance/m04-cases.md`. No commits, ledger edits, schedules, deployments, skills or CatWrangler actions were performed by this worker.

M5 should extend behavior/effect/capability evidence and the finite failure universe deliberately. It must preserve identity `fun`, exact record/collection data separation, ordinary boundary source evidence, snapshot ownership assumptions, fresh exports, callback target/capture obligations and optional guard coverage. A declaration/effect name cannot turn an unknown operation into a characterized conversion. Guards still protect only selected supported data assumptions. M6 owns static record/variant matching and failure handling; M4's runtime `__match_args__` supplies no exhaustiveness evidence. M11 owns package distribution/consumer checking, including guarded façade contract consumption; this artifact is a local compatible source tree with recorded evidence.
