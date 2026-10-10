# M12 confined Vector construction: runtime contract and cost evidence

Status: revision08 engineering correctness and fixed runtime cost gates PASSED,
2026-10-09. Both targets passed 506 whole methods,40 fresh installed commands/
121 assertions and 148 independent cases. The fixed workload found the builder
slower with a higher traced peak at both sizes on both platforms. No speedup or
memory saving was observed. The extension remains experimental and default-off;
human usefulness and authoring-time benefit remain UNMEASURED, zero participants/
attempts. Root's final receipts and the post-measurement documentation authority
appear in the final section.

The original opening status was IMPLEMENTED FOR ROOT SOURCE REVIEW on 2026-10-09;
it recorded 27 focused runtime methods as development evidence and held broader
gates/measurements. All sections from Authority through Actual controller
correction and standard-library preparation below preserve the historical plan
and worker handoffs. Their pending/held statements describe those past gates;
only the explicitly identified final receipts establish later current status.
The complete original opening and document bytes remain in the sealed before map.

## Authority, baseline and actual inspected paths

Authority is `SPEC-sol6.1-composite.md` §13.1, A29 and roadmap12, with the inherited
§§3–12 contracts for conditional source evidence, exact deeply immutable data,
once bindings, callbacks, ordering, failures, effects, initialization and Python
boundaries. The full relevant specification was read. Applicable workspace,
ancestor and nested `AGENTS.md` searches found none.

M11 is committed at `c668439`. Its inherited acceptance is 461 methods on each
supported native macOS arm64/Linux aarch64 target, fresh installed normal
producer/consumer walks of 40 commands/121 assertions per target and the original
78-case independent corpus on both. These are prerequisites supplied by root and
the concrete M11 handoffs, not M12 reruns. See
`Docs/milestones/11-distribution.md`, `Docs/evidence/m11-distribution.md` and
`Docs/evidence/m11-encoding.md` for their exact frozen inputs and limitations.

Actual unchanged paths inspected include `collections.py` in full and relevant
`records.py`, `variants.py`, `boundaries.py`, `effects.py`, `encoding.py`,
`guardgen.py`, `checker.py`, `project.py`, `model.py`, `distribution.py`,
`migration.py`, `__init__.py`, `standard_contracts.py`, `encoding_contracts.py`
and earlier cost controllers. The resulting implementation constraints are:

- Exact Vector uses private tuple storage. `appended`/`concat` copy references,
  preserve retained versions and validate nested data. Recursive validation
  accepts exact admitted scalars, tuples, product collections and registered
  records/cases, with cycle refusal, bool/int distinction and no foreign hooks
  under unchanged product definitions/catalogs/native dependencies.
- Generic T is statically established and erased at runtime. Ordinary runtime
  data validation cannot infer `Vector[int]` from an unexamined annotation.
- Ordered Vector/tuple/OrderedMap payload traversal preserves explicit order;
  Map/Set use inherited homogeneous exact scalar canonical order for nested
  validation and failure selection. No new unordered construction is proposed.
- The checker already separates data, checked callable evidence and opaque
  capability lifetimes. Its general source loop/generator/task vocabulary stays
  closed. `@fun` remains an identity marker, never a runtime certificate.
- Detached catalogs join source fingerprints, reports and closed wheel
  validators; producer metadata is provenance. Current combined consumer source
  analysis alone establishes current permission, effects and trust. Private
  intrinsic schema reconstruction has no consumer-admission authority.

The supported execution target is literal `.venv/bin/python`, CPython 3.13.1
standard GIL, native UTF8/surrogateescape, macOS arm64 or Linux aarch64. Linux
observations, when released, use pinned image
`0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae`.

## Ownership and finite API agreed with main

Runtime worker owns exactly five files after root release:

1. NEW `pyalamode/builders.py`: ordinary confined runtime.
2. NEW `pyalamode/builder_contracts.py`: detached versioned metadata only.
3. NEW `tests/m12_runtime.py`: focused runtime/invariant adversaries.
4. NEW `benchmarks/m12_builders.py`: the ONE shared cost controller below.
5. This `Docs/evidence/m12-builders.md`: plan, actual later evidence and limits.

Main owns checker/model/project/public-export/necessary CLI/migration/distribution
integration, `tests/m12_builders.py`, `Docs/milestones/12-builders.md`, README and
examples. Reviewer owns `Docs/conformance/m12-cases.md` and outside observers.
Root owns the ledger, freezes, verification/measurement release and Git. This
worker edits no central file or existing collection hunk. User
`Docs/getting-started.md`, `play/worksheet.py`, README getting-started content and
incidental editor/`.DS_Store` files stay outside this ownership.

The public names resolve from `pyalamode` or `pyalamode.builders`:

```python
vector_build(callback, /) -> Vector[T]
VectorBuilder[T]                 # confined callback annotation, never data
VectorBuilder.append(value, /) -> None
VectorBuilder.extend(values: Vector[T], /) -> None
```

There are no public constructor, finalizer, read/query/index operation, seed,
mutable export, ownership transfer, evolver, generator consumer, context manager,
task operation or general mutable-container permission. Annotation subscription
produces an ordinary exact `GenericAlias`; the checker admits exactly one data
schema T in the designated callback parameter slot. Ordinary generic arguments
have the same erasure limits as the existing collections. Runtime does not parse
strings, inspect annotations, call `get_type_hints` or evaluate schemas.

A useful admitted authoring shape is finite bulk assembly from existing ordered
operations, retaining the existing no-general-loops rule:

```python
from pyalamode import Vector, VectorBuilder, fun, vector_build

@fun
def framed_positive_doubles(values: Vector[int]) -> Vector[int]:
    def twice(value: int) -> int:
        return value * 2

    def positive(value: int) -> bool:
        return value > 0

    def populate(builder: VectorBuilder[int]) -> None:
        builder.append(0)
        builder.extend(values.map(twice).filter(positive))
        builder.append(-1)
        return None

    return vector_build(populate)
```

For values `(-2, 0, 3, 4)`, the independent literal result is `(0, 6, 8, -1)`.
No callback return value supplies the Vector. Early `return None` finalizes the
accepted prefix; empty callback completion produces an empty exact Vector.

## Static agreement and effects/failure boundary

Builders are default OFF: omitted `builders` or exact `false` preserves earlier
source admission. Exact `builders = true` enables only this finite contract.
Other types/values are tooling refusals. Runtime availability does not read policy
or require a runtime check/build service; ordinary calls acquire no source claim.

One direct nested undecorated `def` in the same active checked parent is consumed
once through a direct Name argument to `vector_build`. The definition dominates
that call. It has exactly one fresh positional-only or positional-or-keyword
parameter `VectorBuilder[T]`, no default/varargs/keyword-only/type parameters and
explicit `-> None`. T must be existing stable data, recursively excluding builder,
Callable, Effectful and capabilities. No other builder signature is admitted.

The construction callback is pure in this initial increment. Its stable ordinary
captures and separately checked helper callbacks retain existing obligations.
Pure characterized data calls are permitted. Effect declarations/capabilities,
unknown operations, nested construction and nested definitions inside that
callback are refused. Inherited if/match/characterized try and fresh ordinary
bindings retain their existing rules; no loop, comprehension or generator rule
is added. Each builder Name occurrence is a direct receiver of admitted
`append`/`extend`, with established exact T or Vector[T], respectively. Calls are
statement operations returning None, with normal once-binding enforcement.

The builder and its methods cannot be aliased, reassigned, captured, returned,
stored in nested data/defaults/globals, passed to any other call, used for truth,
comparison/formatting/reflection, invoked directly as a callback, reused at a
second construction site or used concurrently. A checked outer effectful caller
may perform its already-characterized operations before/after construction; the
construction callback itself remains pure. Its failures do not erase prior
effects or existing external trust.

Private list/token mutation is trusted implementation machinery with empty
observable effects. It does not grant user `State` or `Task`. The runtime's own
valid-input failure bound is conservative `RecursionError` from nested validation
plus actual callback raised-failure bounds. Ordinary malformed arguments/returns
produce TypeError; expired/busy/wrong-thread tokens produce RuntimeError. Those
ordinary precondition failures are distinguished from valid strict source's
failure graph. Termination, allocation success and process interruption are not
proved. Callback failures propagate unchanged after invalidation.

## Runtime algorithm, exact refusal and lifetime

`vector_build` admits only exact `types.FunctionType` through the inherited
finite function admission helper, without attribute/annotation/default/capture
inspection. It allocates one exact VectorBuilder with private fixed slots, a
fresh active token, owner `_thread.get_ident()` and private exact list. It invokes
the callback once with that builder. Ordinary reuse of the same Python callback
in a separate call constructs a fresh independent builder; no permanent function
registry or certificate lookup exists. Ordinary nested independent constructions
are likewise outside the strict lexical contract but do not share tokens.

Public direct construction and subclassing refuse. Ordinary attribute writes and
deletes refuse. No mutable storage is part of the public interface. Deliberate
private slot/reflection/native mutation is outside the unchanged-runtime and
ownership preconditions; the runtime is not hostile-process isolation.

Each append/extend checks in this exact order: exact receiver, complete exact
token shape, active token, current owner thread, non-busy operation, exact private
list storage, then argument admission/validation. Foreign values are refused
before representation, equality/hash, iterator, property or arbitrary conversion.
A retained bound method checks its original builder token anew on each call.
Wrong-thread calls cannot read, validate or change the payload. A private busy
flag surrounds validation plus list mutation and is reset in a method `finally`.

- `append` validates `append.value` completely before adding one reference.
- `extend` first requires exact Vector, validates `extend.values` completely,
  reads its exact tuple through the inherited finite storage helper, then extends
  the staging list. An invalid nested Vector cannot partially extend staging.
- Normal callback completion must be exact None. After that check, validate the
  token again, copy private list references to one exact tuple, allocate one
  exact Vector through inherited `_new`, and validate the final result at
  `result` in explicit element order before publication.
- An enclosing `finally` runs on every exit, including TypeError, characterized
  callback failure, KeyboardInterrupt/SystemExit and failure during finalization.
  It marks inactive BEFORE clearing/dropping staging storage. The result is
  returned only after this cleanup. Failure returns no partial Vector or mutable
  payload; an ordinary illegally retained builder is expired on either exit.

Required public reason literals to author in tests before candidate observation:

| Failure | Fixed reason/message |
| --- | --- |
| TypeError | `VectorBuilder: use vector_build; direct construction is unsupported` |
| TypeError | `VectorBuilder: exact construction subclasses are unsupported` |
| TypeError | `builder: expected exact VectorBuilder` |
| TypeError | `builder: malformed construction token` |
| TypeError | `builder: malformed construction storage` |
| TypeError | inherited exact-function `callback` admission reason |
| TypeError | `callback: construction callback must return exact None` |
| TypeError | `extend.values: expected exact Vector` |
| RuntimeError | `builder: construction is no longer active` |
| RuntimeError | `builder: construction belongs to its creating thread` |
| RuntimeError | `builder: operation is already active` |
| AttributeError | `opaque builder attributes cannot be assigned` / `opaque builder attributes cannot be deleted` |

Nested failures retain inherited closed validation's path/reason vocabulary,
including cyclic/malformed product storage, exact scalar domains and canonical
Map traversal. No rejected value/type is represented. Within one call, statement
order selects the first failed operation; within append/extend/final validation,
the existing ordered/canonical rules select the first failed nested component.
Callback raised failures precede later finalization; wrong return precedes final
output validation. No partial result becomes a stable-value claim.

The immutable result retains stable nested values by reference and owns a new
outer tuple; it retains no staging-list alias. Every prior Vector/record/domain
value remains unchanged. Repeated references are permitted by value, with no
identity guarantee. Deep final validation is construction invariant enforcement,
not purity/capture/alias inference. Selected export/debug data guards may validate
the finished Vector[T] through existing schemas; they never accept the live
builder or certify its callback. Codec schemas/payloads still exclude builders,
callables and live ownership even when wrapped in another container.

## Detached published operation rows and integration instructions

`builder_contracts.py` exposes only detached serializable metadata:

```python
BUILDER_VERSION = "pyalamode.builders-v1"
BUILDERS_NAMES = frozenset({"vector_build", "VectorBuilder"})
BUILDERS_FOUNDATIONS = {...}  # closed actual native-read inventory
operation_contract(name)     # detached dict or None
operation_catalog()         # detached list of exactly three rows
```

Nonexact str and unknown names return None without hooks. Accepted spellings are
the full defining identity and these static shorthands:

| Defining identity | Static shorthand | Signature/valid effects/failures |
| --- | --- | --- |
| `pyalamode.builders.vector_build` | `builders.vector_build`, `vector_build` | `(VectorBuilder[T]->None, /)->Vector[T]`; effects []; RecursionError + callback failure bounds |
| `pyalamode.builders.VectorBuilder.append` | `VectorBuilder.append`, `builders.VectorBuilder.append` | `(T, /)->None`; effects []; RecursionError |
| `pyalamode.builders.VectorBuilder.extend` | `VectorBuilder.extend`, `builders.VectorBuilder.extend` | `(Vector[T], /)->None`; effects []; RecursionError |

`operation_contract("VectorBuilder")` is None: the annotation name is not a
constructor operation. Each detached row publishes version, exact target,
signature/inputs/output, explicit order and callback cardinality, effects,
valid failure bounds, ordinary invalid-input categories, no-alias/lifetime and
finalization contract, no-hook dispatch, initialization, evidence, foundations,
ownership preconditions, generic erasure, complexity and limits. It has no
application type or callable object and no runtime registry.

Direct trusted native inventory: builtins type/object/tuple/list/bool/int/str/
classmethod/sorted/frozenset/TypeError/RuntimeError/AttributeError plus native import/class
initialization; types GenericAlias/FunctionType; `_thread.get_ident`; exact
list append/extend/clear, tuple copy/traversal, object new/getattribute/setattr,
fixed-slot native descriptors and exact int/bool comparison. Product closure
includes `collections.Vector`, `_function`, `_validate`, `_storage`, `_new` and
their complete existing collection/record/domain foundations. Final implementation
must publish actual reads, remove unused proposed reads and include every helper
dependency; this native inventory grants no application calls by spelling.

Initialization has empty effects/failures: trusted finite imports, definitions
and detached constants only; no application lookup/callback, thread sampling,
environment/filesystem observation or external backend during import. Thread
owner sampling occurs only in private invocation/lifetime bookkeeping. Ordinary
application module initialization remains separately unchecked.

Main integrates actual public identities and analyzed writers for new modules,
helpers/classes/methods/globals/catalogs/native reads and inherited dependencies,
not just public spelling. Source fingerprints and installed evidence add exactly
`builders.py` and `builder_contracts.py`: foundation24, package25. Current checker
is `confined-builders-12.0`, operations
`scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-builder-ops-12`.

Parent FunctionContract adds exact `builder_scopes` rows:
`{callback,parameter,element_schema,line,end_line,callback_line,callback_end_line,lifetime,operations,finalization}`.
Lifetime is `fresh callback invocation; invalidated on every exit; no alias,
retention or transfer`; operations are `["append", "extend"]`; finalization is
`automatic exact Vector result after None; construction failure publishes no result`.
This is source-derived reported proof, never an admission switch or producer
claim granting consumer permission. Builders remain non-data and public export
builder parameters/results are refused. Closed validators compare exact detached
rows, complete scopes and source-derived relationships under current policy.

Current migration state is schema3 with exact current checker/op/inventory24.
Historical recognized tuples remain distinct: genuine M11 schema2,
`checked-distribution-11.0`,
`scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-ops-11`,
exact22; genuine M10 schema1, `migration-team-policy-10.0`,
`scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-ops-8`,
exact19. Raw original IDs/bytes/provenance remain immutable history. Recognized
valid old installed product evidence is stale/source refusal1 under current
inputs; unknown/extra/missing malformed inventory or rows are tooling2.

The main/runtime/reviewer wheel agreement is current evidence schema2, existing
kind, producer prior exact fields plus `builder_version = "pyalamode.builders-v1"`,
exact foundation24 and the new closed FunctionContract shape with builder_scopes.
Historical M11 wheel schema1 has exact22, no builder_version and the original
closed contract shape without scopes. It is parsed as bounded provenance, then
refused as incompatible/PAL3701 until rebuilt. To preserve original M11F20,
otherwise valid known22/schema1 producer profiles with different version labels
or hashes remain valid-but-incompatible1; the wheel parser does not require the
historical migration tuple's literal11 labels. Current schema2/exact24 with valid
different producer version labels/hashes similarly remains incompatible1. Unknown
schema/profile combinations, extra/missing/unknown product names and hybrid
old/new contract rows are malformed2. Migration historical state admission still
requires its exact genuine schema/checker/op/inventory tuple above. No producer
profile promotes a current consumer claim or supplies its builders permission.

## Fixed adversarial verification obligations before observation

Focused runtime test literals will cover empty/prefix/append/extend and the useful
example's exact order; mixed append/extend order and fresh calls; nested exact
tuples/collections/records/Option/Result and earlier retained versions; erased T
versus selected guard validation; exact function refusal without callable-object
hooks or annotation evaluation; positional signatures and callback count one.

Refusal cases include mutable nested fields, arbitrary protocol/subclass/metaclass
objects, cyclic/malformed product storage, callables/capabilities/live builders in
all data positions, non-Vector extend, invalid callback return including builder,
tuple and Vector, direct constructor/subclass/attribute mutation, malformed token
or storage without formatting hooks. Failed extend leaves previously staged valid
data unchanged until the enclosing failure cleanup, and no final result escapes.

Ordinary adversaries retain a builder AND a bound append/extend method, then try
them after success, after callback failure and after invalid return; all expire.
Raise ZeroDivisionError and an exact sentinel BaseException, preserving actual
exception identity while invalidating first. A raw callback starts/joins a thread
which attempts append/extend while the owner callback is active; exact RuntimeError
appears before value validation, owner operations still succeed, and no thread is
left running. This tests token affinity on the supported standard GIL runtime,
without granting checked threads or scheduling determinism.

Valid exact validation has no user callback hook that can reenter a method. A
focused ordinary unit seam temporarily injects a validator that attempts the same
builder method while busy, to establish the private busy guard and restore the
unchanged helper afterward. This observation is explicitly a seam test, not a
claim that arbitrary unchecked dependency replacement remains certified. Callback
recursion/new builders and permanent callback reuse are distinguished from
unsupported same-token reentry; no hidden global registry is introduced.

Main/reviewer fix independent static/admission oracles for default-off, true-only
configuration, direct lexical domination/one-use and every alias/capture/store/
default/return/method-retention/unknown-call/concurrent/generator/task attack;
pure callback/effect bounds and failure handlers; once-binding paths; callee,
annotation, catalog/helper/class/native and installed consumer writers; warm
freshness and no import/annotation/default execution; selected data guards and
finished result encoding; old/current exact migration and wheel provenance.
Current consumer false policy refuses intact builder producer source with1, not
false current proof or malformed2. Literal expected results/statuses are fixed
before candidate observations. Root releases inherited/platform/installed gates
only after joint source/controller freeze; this worker does not rerun them early.

## Complexity, retention, memory and trust limits

Let n be the completed Vector length and D the total recursive validation work,
counting repeated appearances and inherited canonical Map sorting/catalog scans.
Append has amortized O(1) private reference staging plus its nested validation;
extend has O(m) reference staging plus full nested validation of m input elements;
finalization has O(n) tuple copy, O(n) staging cleanup and one full result
validation. Overall runtime is O(n + D + callback work), with inherited unordered
validation possibly O(k log k) and catalog lookup/depth costs. There are no new
constant-time, structural-sharing, termination or resource guarantees.

The runtime retains O(n) staging references and O(n) final tuple references during
publication, plus recursive validation temporaries and callback allocations.
Nested admitted values may be shared; no copying of their stable internals is
required. Completed builders retain no staging list/items. There is one final
outer tuple and no public intermediate version. Keeping k independently completed
n-sized results can still retain O(kn) references. Existing persistent updates
remain O(n) tuple-copy operations and preserve all retained earlier versions.
No backend replacement or existing collection behavior changes.

No additional value/cardinality/string/integer quota is imposed: existing
collections and callback source constraints apply; recursive depth may fail with
RecursionError. This is a finite API and lexical ownership contract, not a bound
on user computation or process memory. Supported exact no-hook invariants depend
on unchanged classes/catalogs/helper/native bindings and absence of unchecked
storage/dependency mutation. Token guards cover supported ordinary lifetime,
thread and construction invariants. They do not establish callback purity,
prevent arbitrary reflection/native tampering or monitor closure cells.

## ONE useful cost protocol: bulk_vector_assembly_v1

Only `benchmarks/m12_builders.py` owns this shared protocol. Fixed sizes are total
**64 and 4096 exact int elements** in exactly **64 preconstructed nonempty ordered
Vector[int] chunks**, with **1 or 64 consecutive elements per chunk**, respectively.
Chunk j contains `j * (n // 64)` through `(j + 1) * (n // 64) - 1`. Chunks are held
in an exact `Vector[Vector[int]]`; each final result has n+1 items, the ascending
integers 0..n-1 followed by exact -1. All input/oracle construction is untimed.

Exactly two conditions per size, hence **4 rows per platform**:

1. `builder_extend64`: one ordinary call to the checked function, lexical callback
   definition/allocation, vector_build token/list allocation, exactly64 literal
   `builder.extend(chunks[j])` statements in increasing j, `builder.append(-1)`,
   exact None completion, ingress/final validation, tuple publication and cleanup.
2. `persistent_concat64`: one call to the checked function containing the single
   left-associated chained expression `Vector[int].of().concat(chunks[0])` through
   `.concat(chunks[63]).appended(-1)`. No once-bound intermediate local is retained;
   each consumed intermediate receiver can be released as the next result takes
   its place. Each exact chunk index and inherited validation/copy is inside work.

The fixed fixture is generated from literal64 only BEFORE freeze and is strictly
checked with builders=true and guards=off. Its source contains no admitted loop
or general builder transfer. The baseline contains no accumulating result list,
fold's additional repeated accumulator validation or 64 retained local versions.
Both conditions retain the same source chunks throughout, no intermediate history
and only the final completed result of the timed loop. There is no additional
append/update/guard/retained-history/installed-throughput cost matrix.

Each row has **10 untimed warmups**, then **3 intervals of 25 calls**: per platform,
12 intervals,300 measured calls,40 warmups. Separately, exactly **4 untimed pre-row
correctness invocations** execute one named condition at each size, and exactly
**1 untimed builder call** creates the retained completed-version setup. These
five invocations are recorded individually outside warmup/measurement counts;
later retained-version assertions invoke no additional builder. No extra interval
or condition is introduced. Each interval uses a fresh tracemalloc
session/reset peak outside the timer after setup. Time with perf_counter around
the25 calls, replacing the previous result and retaining only the last. Stop timer,
read traced current/peak, stop tracing, then check correctness and write evidence.
Tracing overhead, callable/token/staging/validation/allocation/disposal and last
result retention are inside measured work; import/check/build/install/fixture/
input/oracle creation, warmup, hashes/assertions/raw evidence writing are outside.
Preexisting stable chunks are outside the traced allocation baseline. Peak delta
is traced Python allocation for the entire interval, not per-call RSS/native
memory. Report every interval, median per call and current/peak baseline/deltas.

Independent correctness does not call candidate builder, persistent constructor,
equality or codec to generate expected output. Before candidate execution, fix
plain tuple oracle `tuple(range(n)) + (-1,)` and per-chunk plain tuple literals in
the outside controller. Untimed checks require exact Vector, exact tuple storage,
exact n+1 length and exact int at every position matching that oracle; verify all
original chunk storage is unchanged. Separately retain an existing source Vector
and an earlier completed Vector across ordinary later construction/update and
verify unchanged contents, outside intervals. No candidate-observed value becomes
an oracle and no checker/cache timing enters this runtime protocol.

Root approves exact source/controller/fixture/oracle maps before observations and
releases correctness before intervals. Record actual `.venv/bin/python` and Linux
interpreter/runtime/native identities, OS/hardware/flags/hash seed, explicit
guard=off, source/product/controller hashes before/after and exact counts. This
runtime protocol imports **one canonical frozen SOURCE copy** at ROOT/pyalamode;
fresh installed-wheel correctness is a separate acceptance gate. The loaded
exact24 foundation modules must all resolve to that same physical package, whose
exact25 Python files are hashed. Capture the complete package/native/core/sys.path
environment before and again in finally; require exact equality, including on a
failed candidate interval before any acceptance. A failed after-observation is
recorded and refuses acceptance. Resolve the required actual Python core through
LIBDIR/LDLIBRARY or, on Darwin only, the finite PYTHONFRAMEWORKPREFIX/LDLIBRARY
alternative; record its configured/actual/resolved path, size and SHA256. There
is no conditional core omission. Hash both generated fixture source and the exact
frozen POLICY bytes before/after and require byte equality. Run accepted native
then pinned Linux sequentially,
with no inherited suites/Docker setup/correctness controllers during intervals.
At the original plan gate, no candidate measurement or correctness run had occurred.
Three samples characterize these named conditions and shared host load; no
universal speedup, isolated-hardware throughput or cross-platform claim follows.
Human usefulness/authoring time remains UNMEASURED, zero participants/attempts.

## Historical preparation handoff and release

Main and runtime agreed the exact API, pure-only lexical callback, no-new-loops
scope, final revalidation/cleanup, ordinary-only misuse categories, catalog
identities/version, exact current/historical inventories and ONE cost protocol.
Reviewer receives these literal contracts to fix adversaries. The main-owned
closed wheel shape above preserves bounded historical provenance and the original
M11F20 valid-but-incompatible case. At that preparation gate, tests, source edits
and measurements were held. Root subsequently released only the bounded five-file
implementation and focused development tests; broader gates and intervals remain
held. Any further plan amendment requires explicit reconciliation and a new hash.

## Actual bounded implementation and focused development handoff

The five owned files are implemented/prepared. `builders.py` reads inherited
helpers through `_collections`; no copied validation alias or function registry
is introduced. Slots are `_active`, `_owner`, `_busy`, `_items`. Exact token checks
precede payload admission; methods and finalization hold busy; callback exact
None is required; final recursive result validation precedes finally cleanup.
Cleanup revokes first, clears exact staging storage and drops the builder's list
reference on every supported exit. Direct construction/subclass/attribute/hash/
dict access refuses. Runtime annotation subscription is erased GenericAlias only.
The source adds no existing-collection change, configurable quota, backend or
capability/effect permission.

`builder_contracts.py` publishes exactly three detached rows with all nine finite
spelling aliases above. Every call returns new nested metadata lists/dicts.
BUILDERS_FOUNDATIONS contains builtins type, object, tuple, list, bool, int, str,
classmethod, sorted, frozenset, TypeError, RuntimeError, AttributeError,
`__build_class__`, `__import__`; types GenericAlias and inherited FunctionType;
`_thread.get_ident`. Actual closure includes list append/extend/clear, tuple copy,
fixed slots through object native access, exact token comparisons and inherited
collections `_function`, `_invalid`, `_validate`, `_storage`, `_new`, Vector,
records/cases/registries and their entire existing native/product foundations.
Sorted/frozenset/str additionally describe detached catalog initialization/name
handling; FunctionType is the reused exact callback admission dependency.

The ONLY development execution was:

```text
/Volumes/Projects/pyalamode/.venv/bin/python -m unittest discover -s tests -p m12_runtime.py -v
```

It passed27 focused methods, exit0, on native CPython3.13.1. Raw receipt is
`/tmp/pyalamode-m12-runtime-development/001/result.json`, SHA256
`39a6dc9bde131a9cc1bd3311dad34489843c965644bba384f2c1e175fcf7344e`.
`stdout.bin` is empty, SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
`stderr.bin` is3846 bytes, SHA256
`50e02516aa60a7cb48183afda01c11f82406a5c7c6c428e98f474d9269a2fee8`.
Exact argv and before/after source maps are retained alongside those files; no
captured source changed during the run. There were zero failed candidate runs and
no reruns. This is focused development evidence only, with no frozen platform,
independent148-case, installed-wheel or inheritance acceptance assertion.

The methods cover useful ordered assembly, exact nested data/retained versions,
erased T versus selected data validation, every supported exit's invalidation,
bound methods, constructor/subclass/token/storage/no-hook refusal, exact None,
callback count and annotation/default noninspection, wrong-thread-before-validation,
canonical nested errors, callback/data/codec ownership exclusion and detached
catalog rows. Busy/finalization validation injections are explicitly ordinary
seams restored in finally; no continued certification of replaced dependencies
is inferred. One ordinary raw staging alias test establishes final tuple isolation,
while preserving the explicit private-reflection precondition.

The first controller, SHA256
`f7c53dab7fb7c47c7fd5a46c831cc3da10cdf4bcdf8eaed689898dbfbedfd2eb`,
was handed off without any execution. Its full source and receipt remain frozen
in `/tmp/pyalamode-m12-runtime-handoff-01/`; original handoff JSON SHA256 is
`b110c50d7a04a70b29e308bd8088bfc9184c9d4a230ba39da7a5faf7185b4f03`.
Root then released a correction confined to this controller and evidence document,
followed by standard-library describe/AST/oracle preparation only. The runtime,
catalog and 27-method test files stay byte-identical, with no test rerun. It exposes
`--describe` for standard-library fixed-source/plain-oracle preparation only and
`--measure` for the approved exact four-row protocol. Measure requires a closed
root release JSON containing exactly schema1, protocol bulk_vector_assembly_v1,
`m12_builder_measurements_authorized=true`, controller_sha256, fixture_sha256,
absolute frozen source_files map and current24 product_artifacts map. Hash/target
gates precede product/candidate imports. The controller pins the canonical frozen
SOURCE root for ordinary imports, refuses any product module from another physical
package or unexpected module inventory, records actual package25/native interpreter/
required core/environment identities before/after, and strictly checks its fixed
guards-off fixture outside intervals. The finite exact24 foundation is imported
before the before-map so normal lazy checker imports cannot change that inventory;
the25th file __main__.py is hashed as a launch entry and never imported here.
Its source/oracles and release schema are reviewable without importing product
code. Setup is not an additional installed acceptance observer or cost condition.

If later released, each actual interval is persisted before correctness checks;
failed or interrupted runs retain partial JSON and after-source/product/environment
maps plus fixture source/policy hashes and exact-byte checks. The controller
computes actual row/interval/call/warmup/pre-row/retention totals and requires
4/12/300/40/4/1. The chained persistent expression holds no named intermediate
versions; explicit stable inputs and only the last completed result are retained.
No candidate fixture check, independent observer, full suite, new installed
acceptance or cost measurement has run in this worker handoff. Root reviews the
corrected full source/controller/document and raw preparation receipt before
joint freeze or broader release.

## Actual controller correction and standard-library preparation

Root's confined correction changed only `benchmarks/m12_builders.py` and this
document. The corrected controller is366 lines/22517 bytes, SHA256
`fe5d09a6b3b9cae51736155072ca96a319b60409dff9bd8647796c7143e6d48f`.
The unchanged runtime/catalog/tests retain respectively SHA256
`3ce7424371755ca79b5f234a09bb1a733e855a47072c3a6aca93ce3f4b316548`,
`44449e402c8920fcc4a5979583f5c14d75f5d78ade00a471d5184f3ad8a7168c`,
`0c6be6a6db8cdf11c6e04676418a39a22db70a3190210498af5ef8a5e0fdb081`.
The former controller and document are also retained at
`/tmp/pyalamode-m12-runtime-controller-f7c53dab.py` and
`/tmp/pyalamode-m12-runtime-evidence-ec254f44.md`; no historical receipt was
overwritten. Complete corrected-source and historical-to-current diffs accompany
the second handoff. This document's receipt paragraph was appended after the
preparation run; the raw before/after document maps from that run remain intact.

The one authorized preparation command was:

```text
.venv/bin/python benchmarks/m12_builders.py --describe
```

It exited0 with empty stderr. Raw argv/before/after/stdout/stderr and independent
standard-library AST/oracle preparation are retained under
`/tmp/pyalamode-m12-runtime-preparation/001/`. Result JSON is4229 bytes, SHA256
`8eeaedd3e739b1b9420e6126a9fad67449e0cf6c529defcb0a5af24128cfd9c5`;
stdout is131095 bytes, SHA256
`87f17d75880bb4a94e15531ab516b6c6edce901fc54a800d6a6f7e557052a005`;
stderr is0 bytes, SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The five source maps before/after were equal. There were zero failed preparation
attempts, candidate product imports, fixture checks, candidate invocations, test
reruns or measured intervals in this preparation. No target-gate or measurement
branch was executed.

Preparation fixed the75-line/3812-byte fixture source, SHA256
`0d174fe7f96002a41f78278d678ac9fbd7e21bbad3861be239485ab14a1aa7e6`,
the4-line/62-byte exact policy, SHA256
`2288fced08da39d55dea287290be62d0388d6f54ea3e5cf85937a33b9cff1313`,
and107853-byte plain JSON oracles, SHA256
`d402a9681c6622cb747ec58bd9d02bc597f8502a8bff349577615e947de2dc19`.
AST inspection established the64 ordered literal extends, one append(-1), exact
None completion and direct construction return; the baseline is one return
expression with64 ordered concat calls and appended(-1), with no source loop or
intermediate local. Plain literal oracles independently have64 chunks with1/64
integers each and65/4097 result items. All four owned Python files parsed without
execution, all top-level controller imports belong to the standard library, and
the preparation process contained no pyalamode module. These are source/oracle
preparation observations, not candidate correctness or measurement acceptance.

The standard-library native core observation resolved the finite Darwin fallback
`PYTHONFRAMEWORKPREFIX/LDLIBRARY` to
`/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/Python`,
actual resolved file
`/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Python`,
5079728 bytes, SHA256
`424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d`.
The failed LIBDIR/LDLIBRARY candidate and all three sysconfig literals are recorded
in `stdlib-preparation.json`. Linux resolution remains held for root's released
platform work. This worker stops at corrected-source handoff; measurements and
broader correctness gates require root's later joint freeze/release.


## Fixed cost fixture empty-seed amendment — outside preparation only

Root authorized a bounded preparation amendment to the initial persistent seed:
`Vector()` becomes the existing admitted `Vector[int].of()`. The direct bare empty
constructor is unsupported in this strict fixture. The typed empty of operation
establishes the existing exact int Vector schema without widening constructor,
static API, builder, loop, callback, data, ownership or policy admission.

The proposed sole-controller change is exactly the fixture_source expression's
initial literal. Its proposed full source remains366 lines/22525
bytes,SHA256 `84c28bf5009714d48cd3e5e0ec457186ec8a62b70ed6d60c0c211a9425e36bc6`. The proposed generated fixture changes
only its persistent return expression's initial empty seed; it remains75 lines,
now3820 bytes,SHA256 `bbf3f8f53d591f007ae48d779dd27c3681faf5a6b038b26d186e7e7f5f961317`. The exact62-byte
policy and its SHA256
`2288fced08da39d55dea287290be62d0388d6f54ea3e5cf85937a33b9cff1313`
remain unchanged. Controller/release fixture identities change only as this exact
source dependency consequence. Original366-line/22517-byte controller
`fe5d09a6b3b9cae51736155072ca96a319b60409dff9bd8647796c7143e6d48f`
and75-line/3812-byte fixture
`0d174fe7f96002a41f78278d678ac9fbd7e21bbad3861be239485ab14a1aa7e6`
remain preserved historical inputs.

The intended `bulk_vector_assembly_v1` measurement conditions remain exactly
`builder_extend64` and `persistent_concat64`: total64/4096 exact ints in64 prepared
ordered chunks; builder64 direct extends plus one append(-1); persistent one
left-associated64-concat chain from `Vector[int].of()` plus one appended(-1).
Input/oracle/result order, result lengths65/4097, retained stable chunks, released
consumed intermediate receivers and only the last completed timed result are
unchanged. There are still4 rows/platform,10 warmups/row (40 total),three25-call
intervals/row (12 intervals/300 measured calls),four untimed pre-row correctness
calls and one untimed retained-builder setup. Every timer/tracemalloc baseline,
current/peak/delta, cleanup/disposal, validation, excluded setup/assertion/hash/
evidence-write and platform/native/core/source/package/foundation identity rule
remains unchanged. There is no new cost condition or better-of repetition.

Original native cost01 is an interrupted attempt before any interval, preserved
separately: launcher status-15 after root-reported142.415s in the
untimed strict fixture check; stdout/stderr both empty. Root SIGTERM stopped only
verified owned PID9049. Original partial JSON has0 measurement rows and0
intervals, no completed untimed fixture-check receipt and no observed finally
map. It supplies no runtime cost value or completed frozen-input acceptance.
Linux cost was unlaunched. These are original attempt outcomes, not measurements
of the proposed amended fixture.

Preserved cost01 root release is
`/tmp/pyalamode-m12-root-native-cost-release-01.json`,SHA256
`af2827c36bbf2146c12d90b6b11b255dc49c83bd967746e2d08ac6cee51e64fa`; actual launcher journal is
`/tmp/pyalamode-m12-root-native-cost-launch-01/command.json`,SHA256
`428049f4b46a204075b070f3a9b720c2720f286948b176bca038d4dc54943d95`; root stop receipt is
`/tmp/pyalamode-m12-root-native-cost-stop-01.json`,SHA256
`81af93c37d65976da0ad40591e2488560c6d2a6c5c13691d29d16fa8fba6e013`. Original partial is
`/tmp/pyalamode-m12-root-native-cost-work-01/partial.json`,
234066 bytes,SHA256
`d4a61d370d3de62e3ee71695ba6fd64bd063260f71642f4d799869160e3093a5`. Its actual raw streams, original
fixture/policy and every receipt byte are copied unchanged in the outside packet.
The absent cost01 final result/finally maps remain absent; no fabricated terminal
state is substituted for the original partial status.

This is full-source/protocol preparation only. No amended controller/fixture
branch, product import, strict check, describe, test, timing, Docker, publisher,
Git or live document action has run. Root reviews the exact full diffs and any
separate checker-performance correction, establishes a fresh immutable matching
freeze/release and decides whether to run the fixed protocol. Later actual data
must retain the interrupted cost01 receipt, every attempt and any unresolved
hold. No run, pass, cost improvement or user benefit is predicted here. Human
usefulness remains UNMEASURED: zero participants/attempts.

## Final revision08 frozen correctness and runtime cost evidence — 2026-10-09

Revision08 engineering correctness and the sole fixed runtime cost protocol
completed on native macOS arm64 and pinned Linux aarch64. The complete engineering
acceptance is [pyalamode-m12-root-final-acceptance-review-08.json](/tmp/pyalamode-m12-root-final-acceptance-review-08.json), 2164 bytes, SHA256 `1810c99f9cd9d66730d5e572ba1458589bfba6b81c63baf33f9e5b7fd5772323`. It records `passed=true`, while its milestone
completion field is false at this gate because final documentation, evidence
publication and commit remain root-owned follow-up work. The post-measurement
documentation authorization below permits only the reviewed document delta.
No failed correctness or fixed-cost acceptance gate remains in these revision08
receipts. Earlier failed/held attempts remain historical and are preserved.

Revision08 contains the bounded call-local callee sharing and graph-wide
diagnostic stamp for remote emissions. Its 506-method denominator is observed on
both targets. Earlier 504/revision05 suite and installed passes and 148/revision07
independent passes belong to their own frozen bytes; final acceptance here uses
revision08 receipts.

### Final acceptance receipts and preserved earlier outcomes

| Gate | Native macOS arm64 | Pinned Linux aarch64 | Retained reconciliation |
| --- | --- | --- | --- |
| Whole-source suite | 506 methods; passed; 52.764s | 506 methods; passed; 54.933s | [pyalamode-m12-root-correctness-review-08.json](/tmp/pyalamode-m12-root-correctness-review-08.json), 1990 bytes, SHA256 `263527a5fc17b4928aad6d9ebab37101876b4c5e10991faff9404d223fe11748` |
| Fresh installed producer/consumer gates | 40 commands/121 assertions; passed | 40 commands/121 assertions; passed | [pyalamode-m12-root-native-reconciliation-08.json](/tmp/pyalamode-m12-root-native-reconciliation-08.json), 10194 bytes, SHA256 `d8ae15365c1069ee542108d741ddcc3f38848160c301295f83c42e89e48f6160`; [root-proof.json](/tmp/pyalamode-m12-retained-linux-08/root-proof.json), 9570 bytes, SHA256 `514189ef37e9cc378aa62b98085e55187a1f23f40a6bfe1d95394d1bbcce2032` |
| Independent fixed corpus | 148 cases/4 groups; passed | 148 cases/4 groups; passed | [pyalamode-m12-root-peer-native08-complete-review.json](/tmp/pyalamode-m12-root-peer-native08-complete-review.json), 3974 bytes, SHA256 `47d7a09019aef154cea86f9938fcaca68f0fddfec64a108360072cfb83f9d42c`; [peer-complete-proof.json](/tmp/pyalamode-m12-retained-linux-08/peer-complete-proof.json), 3431 bytes, SHA256 `608b407712bb4721cd930e6d60c2de043b9173b47cfab55ed6964f531d51fa41` |

Each independent platform proof records 327 child commands, 654 raw streams and 152
projection rows, retaining diagnostic/contract/current-policy/gate/history and
output-preservation projections. Group denominators are static 94 cases/209
commands, runtime 20/4, guard-freshness 13/30 and distribution-history 21/84; all eight
groups passed. Native exact phase maps/raw records remain at
`/tmp/pyalamode-m12-review/runs/native-08`; Linux's retained four groups remain
under `/tmp/pyalamode-m12-retained-linux-08/peer-runs`. Their source, controller and
installed before/after equalities are bound by the final correctness receipt and
[pyalamode-m12-root-retained-linux08-review.json](/tmp/pyalamode-m12-root-retained-linux08-review.json), 1554 bytes, SHA256 `1d49695928f3769945bd1c100e679bd7baed9755286ac91a181c63755526058a`. The 08 review release is [pyalamode-m12-root-review-release-08.json](/tmp/pyalamode-m12-root-review-release-08.json), 40765 bytes, SHA256 `30baec333ed0744facb98f8fb61715ef5d75422fdd5a4bd8b6ac8bf6f497b035`; its
correctness authorization excludes timing. The fixed measurement releases below
separately authorize runtime timing.

Historical outcomes remain distinct from acceptance of these final bytes:

| Historical gate | Preserved outcome | Retained evidence |
| --- | --- | --- |
| Original runtime development | 27 focused native methods passed; zero failed runtime candidate attempts or reruns in that worker release. This finite worker claim does not count later cost attempts. | Unchanged development/controller preparation receipts in the historical body above. |
| Revision05 whole/installed and revision07 independent | Whole 504 passed native 54.227s/Linux 56.908s; fresh 40/121 on each. All eight 07 independent groups passed 148 cases/327 commands per target. | [pyalamode-m12-root-final-correctness-review.json](/tmp/pyalamode-m12-root-final-correctness-review.json), 2841 bytes, SHA256 `50da231cefe631c5714365d8336c8c0804c862f97dc192b23283d429dccb4e52` |
| Native cost01 / unlaunched Linux cost | Root stopped owned native PID9049 after 142.415s in untimed checking; launcher -15, 0 rows/0 intervals. No final result or completed finally/check observations. Linux cost01 never launched. | [pyalamode-m12-root-native-cost-stop-01.json](/tmp/pyalamode-m12-root-native-cost-stop-01.json), 1008 bytes, SHA256 `81af93c37d65976da0ad40591e2488560c6d2a6c5c13691d29d16fa8fba6e013`; [command.json](/tmp/pyalamode-m12-root-native-cost-launch-01/command.json), 950 bytes, SHA256 `428049f4b46a204075b070f3a9b720c2720f286948b176bca038d4dc54943d95`; original release/partial/raw preserved above. |
| Freeze01 F04 | Warm checking incorrectly admitted ordinary builders._collections=None; acceptance stopped. Partial 231 commands/462 raw streams/122 projections remain original outcomes. | [pyalamode-m12-root-peer-native-partial-review-01.json](/tmp/pyalamode-m12-root-peer-native-partial-review-01.json), 3676 bytes, SHA256 `2091efb275859778183bc3a17743f50a018a3ef75ec6989f89f0ba5df0bee4cb` |
| F04 correction run039 | Seven cache-miss subtests failed in one method because a reused project had already refused bodies. Fresh per-shape projects corrected test setup; original failure streams remain. | [focused-outcomes.json](/tmp/pyalamode-m12-main-handoff-02/focused-outcomes.json), 10158 bytes, SHA256 `368f7c4cd97c2a316346dd3740345e7280bf791d2872d6f4b5345dc2ca9e35fe` |
| H03 controller hold/correction | One expected object current_policy_status 1→0 and explicit enabled_historical_policy_status 1; current 0/gate 1/history 1. Earlier bootstrap=False/saved=True/write=False repair unchanged. Other 147 objects/all 327 vectors unchanged. | [handoff.json](/tmp/pyalamode-m12-h03-axis-correction-01/handoff.json), 4882 bytes, SHA256 `4ab4a12c77e46290b5e875b051cb062f68a09b3e45c4d5b01e01843fcc7f0a39`; [complete-application.diff](/tmp/pyalamode-m12-h03-axis-correction-01/complete-application.diff), 11183 bytes, SHA256 `481d041ecfcaf772cab1c1351d921bb0c54ed72219f2e209b7e3f471d54d763d`; [pyalamode-m12-root-h03-axis-final-review.json](/tmp/pyalamode-m12-root-h03-axis-final-review.json), 539 bytes, SHA256 `de9d7f2705d0cfc071b0661db48d235adf9e4d0f15b3acbefef48f957e4fa786` |

The native cost01 interruption supplies no runtime value. The revision08 runs
below are the accepted corrected-protocol measurements; the historical attempt
is retained rather than compared or selected for a better outcome. No additional
timed row, interval, repetition or condition supplies the reported medians. Human
usefulness and authoring-time benefit remain **UNMEASURED: zero participants/
attempts**.

### Revision08 observed freeze and final identities

M11 prerequisite commit is `c668439`. Final checker SHA256 is
`53c3346dc653af3df7fae30ada826b926e40d49bfa0acb83372f3ec9fae7c1c1`; `tests/m12_builders.py` SHA256 is
`599277f0af7800165edcf1213d0d30e045cfc5878bf3e484e96a0e02ce2a0c3b`. Runtime remains
`pyalamode.builders-v1`; checker is `confined-builders-12.0`, operations
`scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-builder-ops-12`.

| Frozen input | Observed denominator/identity | Retained map/receipt |
| --- | --- | --- |
| Review primary/authority source | 124 primary+3 authority=127; distinct from full inventory | [pyalamode-m12-root-source-map-08.json](/tmp/pyalamode-m12-root-source-map-08.json), 18711 bytes, SHA256 `e1b3fa7b05c1c92da5332a16beaa801d13b68083d663cbb886f126cea3ff0151`; freeze [pyalamode-m12-root-freeze-08.json](/tmp/pyalamode-m12-root-freeze-08.json), 63493 bytes, SHA256 `588cf67dcfc164ef1c40dc330cb87ec98305611283a6f8fc2b4f76c0d2ffe640` |
| Complete copied/measured source inventory | 205 entries, used in both cost source_before/source_after maps | [pyalamode-m12-root-source-inventory-08.json](/tmp/pyalamode-m12-root-source-inventory-08.json), 39700 bytes, SHA256 `8021cac7f04c96df62c26826fbc8ee4e587bc942e65d5ceca5ee6b8ca34c1b18` |
| Physical package | 25 Python files, including launch-only __main__.py | [pyalamode-m12-root-product-map-08.json](/tmp/pyalamode-m12-root-product-map-08.json), 3361 bytes, SHA256 `599473398d5af8fca1c0453d7baaa13365b20351f1266d1acf576d00fca395ae`; both environment.full_package_bytes maps |
| Loaded foundation | 24 exact modules from one canonical physical source package | Freeze product_artifacts plus both result product_before/product_after and environment.loaded_product_sources maps |
| Sole cost controller | 366 lines/22525 bytes; SHA256 84c28bf5009714d48cd3e5e0ec457186ec8a62b70ed6d60c0c211a9425e36bc6 | [m12_builders.py](/Volumes/Projects/pyalamode/benchmarks/m12_builders.py), 22525 bytes, SHA256 `84c28bf5009714d48cd3e5e0ec457186ec8a62b70ed6d60c0c211a9425e36bc6` |
| Fixed fixture source | 75 lines/3820 bytes; SHA256 bbf3f8f53d591f007ae48d779dd27c3681faf5a6b038b26d186e7e7f5f961317 | Exact bulk_core.py bytes, before/after identities and description.fixture.source in both results |
| Fixed policy | 4 lines/62 bytes; SHA256 2288fced08da39d55dea287290be62d0388d6f54ea3e5cf85937a33b9cff1313 | Exact [tool.pyalamode] schema 1/builders=true/boundary_guards="off" bytes in each work/fixture/pyproject.toml and result description |
| Independent literal tuple oracles | Original preparation JSON 107853 bytes; SHA256 d402a9681c6622cb747ec58bd9d02bc597f8502a8bff349577615e947de2dc19 | Literal tuple(range(N))+(-1,) and all 64 chunks fixed before execution; complete description.oracles in both results |
| Independent case/controller identities | 148-case manifest and 215 active controller inputs including map self-file | [cases.json](/tmp/pyalamode-m12-review/cases.json), 95167 bytes, SHA256 `fc005f094b9321abe6a05539f60d70941f6c002fd87621293c15f715d79afa84`; [controller-source-map.json](/tmp/pyalamode-m12-review/controller-source-map.json), 44465 bytes, SHA256 `efe1fbd0a44293e549d48205f8d3bd07bcb1283f741c099ec223089b4de629f9`; [planned-execution.json](/tmp/pyalamode-m12-review/planned-execution.json), 174194 bytes, SHA256 `f6b97ccae52db635f4c262e19acdb46a0d26d3f6cce0858ad2937389a511617c` |
| Fresh installed wheel | 235013 bytes; same frozen product used for separate installed correctness | [pyalamode-0.1.0-py3-none-any.whl](/tmp/pyalamode-root-m12-product-08/wheels/pyalamode-0.1.0-py3-none-any.whl), 235013 bytes, SHA256 `7efcea3f6ec0886c56446c9dcf8d73026ef451f34225ed56c4983933b2371ab7` |

Freeze08 pins the active publisher source SHA256
`97753e2de26b798a8cbebfaacff129121238a5151a6b267cfedbe46de11b2be8` and its
SOURCE-PLAN SHA256
`f19ebf79f6115a6dd1078d66e524ad448af34af2dc54ea79e6f04d653ed5e75e`.
That source pin is not publication execution authorization. The source review
map and full copied inventory retain their observed pre-documentation hashes;
this later evidence prose does not replace those frozen bytes or maps.

### Actual fixed-protocol releases, launchers and retention

Both closed schema 1 releases explicitly authorize
`m12_builder_measurements_authorized=true` for `bulk_vector_assembly_v1`, pin the
same controller/fixture/policy, 205 absolute source_files and 24 product_artifacts.
Hash/target gates preceded imports. Runtime timing imported one canonical frozen
SOURCE package; fresh installed correctness remained a separate physical product
and is not a throughput condition.

| Receipt/observation | Native macOS arm64 | Pinned Linux aarch64 |
| --- | --- | --- |
| Release | [pyalamode-m12-root-native-cost-release-08.json](/tmp/pyalamode-m12-root-native-cost-release-08.json), 29771 bytes, SHA256 `3ac720325977b6464a6ad1a7f54026f30da389de06dc3789c1471aafee9cd7f9` | [release.json](/tmp/pyalamode-m12-retained-linux-08/cost/release.json), 26286 bytes, SHA256 `201de7d8bcd6e9640922bbd76eaff3ab25a1cf9c7973e876de56029dfeff420a` |
| Actual launcher journal | [command.json](/tmp/pyalamode-m12-root-native-cost-launch-08/command.json), 948 bytes, SHA256 `8ce6d9124f8f00212103e000674ee5c03ff20172e80e63ebe3375c0ccb1d57a7` | [commands.json](/tmp/pyalamode-m12-root-linux-cost-launch-08/commands.json), 2939 bytes, SHA256 `a3cda76a99bc24a6799d4c7892e3f8c64a3cf901aeb362de60d4f8e789497f13`; [result.json](/tmp/pyalamode-m12-root-linux-cost-launch-08/result.json), 234 bytes, SHA256 `eef79a41cfaad27f9bd4bb7cd6d6678bc1e136cdb6f897aca0e0f84465e5dcf4` |
| Exit/controller status | exit 0; completed | candidate index 1 exit 0; completed; both container guards exit 0 |
| Complete raw result | [pyalamode-m12-root-native-cost-result-08.json](/tmp/pyalamode-m12-root-native-cost-result-08.json), 282860 bytes, SHA256 `f3dac6336d511f610ffc234e4057eecdc5fcb97282bc44349bee9157bdc46a6a` | [result.json](/tmp/pyalamode-m12-retained-linux-08/cost/result.json), 265824 bytes, SHA256 `0dd1403209599fc0c5ad561a8ca2f37ae83e7727f8154ee761ee3ede315b38b1` |
| Root cost reconciliation | [pyalamode-m12-root-native-cost-reconciliation-08.json](/tmp/pyalamode-m12-root-native-cost-reconciliation-08.json), 2608 bytes, SHA256 `9c291776d54221d8e0a9bb370dca52f6b9f5632d6247ba20a16065bf0734d5a8` | [root-proof.json](/tmp/pyalamode-m12-retained-linux-08/cost/root-proof.json), 2198 bytes, SHA256 `5f276131581ac492c46e8cc2811d86271d45e443b33ad5dbd47b49f72b13aae2` |
| Untimed strict fixture check | status 0; `/tmp/pyalamode-m12-root-native-cost-work-08/fixture-check.json`,145093 bytes, SHA256 `4ddbf69b476bdd64e309b14e299e3bd6e42f147f6c17d844716cbd844fe43134` | status 0; retained `/tmp/pyalamode-m12-retained-linux-08/cost/work/fixture-check.json`,143998 bytes, SHA256 `8ab52b8cdf078e454683e8a958a03c99ad72c0bb300a8daffffeda32792202b6` |
| Rows/intervals/measured calls/warmups | 4/12/300/40 | 4/12/300/40 |
| Untimed pre-row/retained builder calls | 4/1, all verified | 4/1, all verified |
| Source/product/environment before-after | 205/24/environment exact equality; frozen_inputs_equal=true | 205/24/environment exact equality; frozen_inputs_equal=true |
| Fixture source/policy exact bytes | Both equal before/after; exact fixed hashes above | Both equal before/after; exact fixed hashes above |
| Partial/final retention | work/partial.json equals final result bytes; cost01 remains original interrupted attempt | retained cost/work/partial.json equals final result bytes; no Linux cost01 launch |

Paired acceptance is [pyalamode-m12-root-cost-paired-reconciliation-08.json](/tmp/pyalamode-m12-root-cost-paired-reconciliation-08.json), 3725 bytes, SHA256 `1e4cc5c4a478b5c94766c28c8646b18a85e4843d3705da1bdd4b3331bb6248d8`. It records 24 intervals/600 measured calls
across both platforms, with 40 warmups, four pre-row correctness calls and one
retained-version setup call per platform. Complete work directories retain
fixture/policy, strict-check cache, fixture-check and partial bytes.

Linux original in-container paths remain unchanged inside the copied JSON:
`/tmp/pyalamode-m12-root-linux-cost-result-08.json`,
`/tmp/pyalamode-m12-root-linux-cost-release-08.json`,
`/tmp/pyalamode-m12-root-linux-cost-reconciliation-08.json` and
`/tmp/pyalamode-m12-root-linux-cost-work-08` map respectively to retained
`cost/result.json`, `cost/release.json`, `cost/root-proof.json` and `cost/work`
under `/tmp/pyalamode-m12-retained-linux-08`. The complete original path/byte
inventory is [original-output-inventory.json](/tmp/pyalamode-m12-retained-linux-08/cost/original-output-inventory.json), 1867 bytes, SHA256 `1e40cc8c9054344adb90ac21d7b181ece7587c28647b0fca5b5a1dc92a8caa5e`; paired reconciliation binds these
lossless retained copies to the actual Linux result and release.

Native actual launch ran from `2026-10-09T23:43:07.111698+00:00` to
`2026-10-09T23:43:10.986585+00:00`. Linux's candidate index 1 ran later, from
`2026-10-09T23:46:49.177512+00:00` to `2026-10-09T23:46:54.159513+00:00`. Root released
native then Linux with setup/correctness/other candidate work stopped during the
measurement intervals. The exact argv are retained below, as data:

```json
[
  "/Volumes/Projects/pyalamode/.venv/bin/python",
  "-I",
  "-B",
  "/Volumes/Projects/pyalamode/benchmarks/m12_builders.py",
  "--measure",
  "--release",
  "/tmp/pyalamode-m12-root-native-cost-release-08.json",
  "--work-directory",
  "/tmp/pyalamode-m12-root-native-cost-work-08",
  "--output",
  "/tmp/pyalamode-m12-root-native-cost-result-08.json"
]
```

```json
[
  "docker",
  "--host",
  "unix:///Users/jared/Library/Containers/com.docker.docker/Data/docker.raw.sock",
  "container",
  "exec",
  "d813b9372e8b20f288954da11c801633beeddf21727506501959e34b8f7a49d9",
  "/usr/local/bin/python3",
  "-I",
  "-B",
  "/workspace/benchmarks/m12_builders.py",
  "--measure",
  "--release",
  "/tmp/pyalamode-m12-root-linux-cost-release-08.json",
  "--work-directory",
  "/tmp/pyalamode-m12-root-linux-cost-work-08",
  "--output",
  "/tmp/pyalamode-m12-root-linux-cost-result-08.json"
]
```

The native stdout/stderr and Linux candidate `1.stdout.bin`/`1.stderr.bin` are
each 0 bytes, SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Linux launcher contains exactly three commands: container guard, candidate exec,
container guard. Both guards' stdout is 7896 bytes, SHA256
`e141648666f11a08207c43a2bf2dac602572d0660b56711107fb18dc8458decf`, with empty
stderr. Container identity is
`d813b9372e8b20f288954da11c801633beeddf21727506501959e34b8f7a49d9`, image
`sha256:0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae`,
no mounts and network mode none. Copy/reconcile guards remain separate from the
single candidate launch and do not add measured calls. No additional timed
repetition is included. Every interval was persisted before its oracle checks;
the interrupted cost01 partial and absent final observations remain preserved.

### Observed supported environments

| Identity | Native macOS arm64 | Pinned Linux aarch64 |
| --- | --- | --- |
| Literal executable | `/Volumes/Projects/pyalamode/.venv/bin/python` | `/usr/local/bin/python3` |
| Observed resolved/base executable | `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/bin/python3.13`; base same path | resolved `/usr/local/bin/python3.13`; base `/usr/local/bin/python3` |
| Python version | `3.13.1 (main, Dec  3 2024, 17:59:52) [Clang 16.0.0 (clang-1600.0.26.4)]` | `3.13.1 (main, Feb  4 2025, 12:52:11) [GCC 12.2.0]` |
| Build/compiler/cache tag/ABI/GIL | ["main", "Dec  3 2024 17:59:52"]; Clang 16.0.0 (clang-1600.0.26.4); cpython-313; ABI empty; GIL true | ["main", "Feb  4 2025 12:52:11"]; GCC 12.2.0; cpython-313; ABI empty; GIL true |
| OS/machine/processor/logical CPUs | macOS-26.6.2-arm64-arm-64bit-Mach-O; arm64/arm;10 | Linux-5.15.49-linuxkit-aarch64-with-glibc2.36; aarch64/empty processor;5 |
| Filesystem encoding/errors; UTF8 mode; hash-seed environment | utf-8/surrogateescape;0; null | utf-8/surrogateescape;1; null |
| Prefix/base prefix | `/Volumes/Projects/pyalamode/.venv`; `/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13` | `/usr/local`; `/usr/local` |
| Canonical imported source package | `/Volumes/Projects/pyalamode/pyalamode` | `/workspace/pyalamode` |
| System load / OS caches controlled | false / false | false / false |
| Complete environment maps | [pyalamode-m12-root-native-cost-result-08.json](/tmp/pyalamode-m12-root-native-cost-result-08.json), 282860 bytes, SHA256 `f3dac6336d511f610ffc234e4057eecdc5fcb97282bc44349bee9157bdc46a6a` environment_before/environment_after | [result.json](/tmp/pyalamode-m12-retained-linux-08/cost/result.json), 265824 bytes, SHA256 `0dd1403209599fc0c5ad561a8ca2f37ae83e7727f8154ee761ee3ede315b38b1` environment_before/environment_after |

Both targets observed exact CPython 3.13.1 with the standard GIL and canonical
physical package identities 25 files/24 loaded foundations. Executable resolution
is observation only; byte identity uses the literal required files. All measured
environment_before/environment_after fields compare equal, including flags,
sys.path, full package, loaded foundation and native Python core identities.

**Native interpreter/core files:**

| Literal identity path | Bytes | SHA256 |
| --- | --- | --- |
| `/Volumes/Projects/pyalamode/.venv/bin/python` | 52640 | `d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132` |
| `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/bin/python3.13` | 52640 | `d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132` |
| `/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/Python` | 5079728 | `424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d` |

Core observed path `/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/Python` resolves to `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Python`;
resolution `PYTHONFRAMEWORKPREFIX/LDLIBRARY`. Exact finite core-resolution inputs and
candidates, flags and sys.path are retained here (including the Linux duplicate
/workspace entry):

```json
{
  "python_core": {
    "LDLIBRARY": "Python.framework/Versions/3.13/Python",
    "LIBDIR": "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib",
    "PYTHONFRAMEWORKPREFIX": "/opt/homebrew/opt/python@3.13/Frameworks",
    "bytes": 5079728,
    "candidate_paths": [
      "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib/Python.framework/Versions/3.13/Python",
      "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/Python"
    ],
    "path": "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/Python",
    "resolution": "PYTHONFRAMEWORKPREFIX/LDLIBRARY",
    "resolved_path": "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Python",
    "sha256": "424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d"
  },
  "sys_flags": "sys.flags(debug=0, inspect=0, interactive=0, optimize=0, dont_write_bytecode=1, no_user_site=1, no_site=0, ignore_environment=1, verbose=0, bytes_warning=0, quiet=0, hash_randomization=1, isolated=1, dev_mode=False, utf8_mode=0, warn_default_encoding=0, safe_path=True, int_max_str_digits=4300)",
  "sys_path": [
    "/Volumes/Projects/pyalamode",
    "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
    "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
    "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
    "/Volumes/Projects/pyalamode/.venv/lib/python3.13/site-packages"
  ]
}
```

**Linux interpreter/core files:**

| Literal identity path | Bytes | SHA256 |
| --- | --- | --- |
| `/usr/local/bin/python3` | 67600 | `44a9ce6ed83ab1809449925790d0583e38f17b3ccd1671d9f55e15b576cb4f20` |
| `/usr/local/lib/libpython3.13.so` | 5175584 | `654a735558be10deedd50bc06bded72d1de1f217fb25296c8ba66df7f45a918f` |

Core observed path `/usr/local/lib/libpython3.13.so` resolves to `/usr/local/lib/libpython3.13.so.1.0`;
resolution `LIBDIR/LDLIBRARY`. Exact finite core-resolution inputs and
candidates, flags and sys.path are retained here (including the Linux duplicate
/workspace entry):

```json
{
  "python_core": {
    "LDLIBRARY": "libpython3.13.so",
    "LIBDIR": "/usr/local/lib",
    "PYTHONFRAMEWORKPREFIX": "",
    "bytes": 5175584,
    "candidate_paths": [
      "/usr/local/lib/libpython3.13.so"
    ],
    "path": "/usr/local/lib/libpython3.13.so",
    "resolution": "LIBDIR/LDLIBRARY",
    "resolved_path": "/usr/local/lib/libpython3.13.so.1.0",
    "sha256": "654a735558be10deedd50bc06bded72d1de1f217fb25296c8ba66df7f45a918f"
  },
  "sys_flags": "sys.flags(debug=0, inspect=0, interactive=0, optimize=0, dont_write_bytecode=1, no_user_site=1, no_site=0, ignore_environment=1, verbose=0, bytes_warning=0, quiet=0, hash_randomization=1, isolated=1, dev_mode=False, utf8_mode=1, warn_default_encoding=0, safe_path=True, int_max_str_digits=4300)",
  "sys_path": [
    "/workspace",
    "/usr/local/lib/python313.zip",
    "/usr/local/lib/python3.13",
    "/usr/local/lib/python3.13/lib-dynload",
    "/usr/local/lib/python3.13/site-packages",
    "/workspace"
  ]
}
```

Core resolution tries LIBDIR/LDLIBRARY, with the Darwin
PYTHONFRAMEWORKPREFIX/LDLIBRARY alternative. Native's first candidate does not
exist; its actual framework core is required and hashed. Root rehashes all three
native interpreter/core identity entries and both Linux entries. Successful
finally observations establish the complete source/product/environment equality;
an absent or failed observation would not establish acceptance. Shared
host/container load and OS caches were uncontrolled.

### Fixed workload and timing/memory scope

The four rows per platform are 64 and 4096 exact int input elements split into 64
preconstructed nonempty ordered exact Vector[int] chunks, respectively 1 and 64
integers/chunk. The same stable chunks remain held. Each result is ascending 0..N-1
followed by exact -1, giving 65 or 4097 items. `builder_extend64` defines one lexical
callback, executes 64 direct ordered extends and one append, requires exact None,
then publishes one exact immutable Vector with lifetime cleanup.
`persistent_concat64` starts with the admitted exact empty `Vector[int].of()`
and uses one left-associated 64-concat expression followed by appended(-1);
consumed intermediates can be released and no named intermediate history is held. The fixture introduces no general strict loop or builder transfer.

Each row has 10 untimed warmups and three 25-call timed intervals. Observed counts
are 4 rows/12 intervals/300 measured calls/40 warmups per platform, plus four
individually recorded untimed pre-row correctness calls and one untimed builder
call for retained-version setup. Exact Vector/tuple/int schema, output order,
original chunks and retained source/completed/later versions are checked outside
intervals against the independent plain tuple oracles. Runtime data invariants
and recursive validation during construction remain inside the measured work.

Each interval starts a fresh tracemalloc session and resets its peak before the
perf_counter timer. Included work is callback/closure/annotation allocation,
fresh token/list, native and product indexing, ingress validation, staging/copy,
final full validation, invalidation/list cleanup, persistent validation/copy,
prior-result disposal, last-result retention and loop/timer/tracing overhead.
Setup, imports, fixture/policy/check/build/install/input/oracle creation, warmups,
assertions, hashing and evidence writes are excluded. Current/peak are read after
the timer; tracing stops before oracle checks. Preexisting stable chunks are
untraced. Current/peak and their baseline deltas describe the whole 25-call interval.
They are Python traced allocation, **not per-call memory, RSS or native total**.

### All raw intervals — Native macOS arm64

Each row is one actual 25-call interval. Seconds preserve raw JSON precision;
allocation columns are bytes for that complete traced interval.

| Input N | Condition | Sample | Elapsed seconds | Baseline | Current | Peak | Current delta | Peak delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 64 | `builder_extend64` | 1 | 0.021736915921792388 | 0 | 600 | 3099 | 600 | 3099 |
| 64 | `builder_extend64` | 2 | 0.021082749823108315 | 0 | 600 | 3099 | 600 | 3099 |
| 64 | `builder_extend64` | 3 | 0.02135449997149408 | 0 | 600 | 3099 | 600 | 3099 |
| 64 | `persistent_concat64` | 1 | 0.01450216700322926 | 0 | 600 | 2097 | 600 | 2097 |
| 64 | `persistent_concat64` | 2 | 0.014745499938726425 | 0 | 600 | 2097 | 600 | 2097 |
| 64 | `persistent_concat64` | 3 | 0.014401959022507071 | 0 | 600 | 2097 | 600 | 2097 |
| 4096 | `builder_extend64` | 1 | 0.7064479170367122 | 0 | 32856 | 103929 | 32856 | 103929 |
| 4096 | `builder_extend64` | 2 | 0.7037116249557585 | 0 | 32856 | 103929 | 32856 | 103929 |
| 4096 | `builder_extend64` | 3 | 0.746563500026241 | 0 | 32856 | 103929 | 32856 | 103929 |
| 4096 | `persistent_concat64` | 1 | 0.32801724993623793 | 0 | 32856 | 98600 | 32856 | 98600 |
| 4096 | `persistent_concat64` | 2 | 0.32398262503556907 | 0 | 32856 | 98600 | 32856 | 98600 |
| 4096 | `persistent_concat64` | 3 | 0.3246222920715809 | 0 | 32856 | 98600 | 32856 | 98600 |

### All raw intervals — Pinned Linux aarch64

Each row is one actual 25-call interval. Seconds preserve raw JSON precision;
allocation columns are bytes for that complete traced interval.

| Input N | Condition | Sample | Elapsed seconds | Baseline | Current | Peak | Current delta | Peak delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 64 | `builder_extend64` | 1 | 0.028421750001143664 | 0 | 600 | 3099 | 600 | 3099 |
| 64 | `builder_extend64` | 2 | 0.027653708995785564 | 0 | 600 | 3099 | 600 | 3099 |
| 64 | `builder_extend64` | 3 | 0.027377082995371893 | 0 | 600 | 3099 | 600 | 3099 |
| 64 | `persistent_concat64` | 1 | 0.01873329198861029 | 0 | 600 | 2097 | 600 | 2097 |
| 64 | `persistent_concat64` | 2 | 0.01860300000407733 | 0 | 600 | 2097 | 600 | 2097 |
| 64 | `persistent_concat64` | 3 | 0.01891349999641534 | 0 | 600 | 2097 | 600 | 2097 |
| 4096 | `builder_extend64` | 1 | 0.9426519590051612 | 0 | 32856 | 103929 | 32856 | 103929 |
| 4096 | `builder_extend64` | 2 | 0.9124208759894827 | 0 | 32856 | 103929 | 32856 | 103929 |
| 4096 | `builder_extend64` | 3 | 0.9141103330039186 | 0 | 32856 | 103929 | 32856 | 103929 |
| 4096 | `persistent_concat64` | 1 | 0.4226260419964092 | 0 | 32856 | 98600 | 32856 | 98600 |
| 4096 | `persistent_concat64` | 2 | 0.4185802499996498 | 0 | 32856 | 98600 | 32856 | 98600 |
| 4096 | `persistent_concat64` | 3 | 0.4227144589967793 | 0 | 32856 | 98600 | 32856 | 98600 |

### Row medians and bounded interpretation

Median seconds/call is the median of three elapsed/25 observations. Median peak
delta remains the whole-interval allocation measure. Every controller row field
below matches its three retained raw samples; none is rounded or substituted.

| Platform | Input N | Condition | Median seconds/call | Median interval peak delta bytes |
| --- | --- | --- | --- | --- |
| Native | 64 | `builder_extend64` | 0.0008541799988597632 | 3099 |
| Native | 64 | `persistent_concat64` | 0.0005800866801291704 | 2097 |
| Native | 4096 | `builder_extend64` | 0.028257916681468487 | 103929 |
| Native | 4096 | `persistent_concat64` | 0.012984891682863235 | 98600 |
| Linux | 64 | `builder_extend64` | 0.0011061483598314226 | 3099 |
| Linux | 64 | `persistent_concat64` | 0.0007493316795444116 | 2097 |
| Linux | 4096 | `builder_extend64` | 0.036564413320156745 | 103929 |
| Linux | 4096 | `persistent_concat64` | 0.016905041679856368 | 98600 |

The builder was slower than persistent_concat64 at both 64 and 4096 inputs on
both platforms. Its traced peak was also higher in all four comparisons: 3099
versus 2097 bytes at 64 and 103929 versus 98600 bytes at 4096 on each platform.
Current traced allocation was equal between conditions, 600 or 32856 bytes
respectively. These runs observed **no speedup and no memory saving** for the
builder. The fixed comparison remains meaningful even though its direction
opposes a hoped-for benefit; no universal builder benefit follows.

These observations characterize only this finite bulk workload, fixed retention,
recursive validation and recorded environments. They do not establish universal
throughput, isolated hardware behavior, a different persistent backend, general
ownership transfer or concurrency benefit. Callback calculations, recursive
depth and resource use retain inherited limits; there is no termination,
allocation-success or process-memory guarantee. Tracemalloc is Python allocation
instrumentation with overhead included, not RSS or all native allocations.
Load and caches were uncontrolled.

Private token/list mutation remains a disclosed trusted implementation
foundation. The exact immutable result has a new outer tuple with stable nested
references; source chunks and independently retained completed versions stay
stable. Tokens invalidate on supported exits and reject expired/busy/wrong-thread
use before payload access. Static confinement/pure callback/once-binding/current
dependency evidence remains separate from runtime FunctionType admission, data
validation and selected guards. Thread affinity does not prove deterministic
scheduling or hostile-process isolation; unchanged classes/catalogs/native/
helper/storage bindings remain preconditions. This extension adds no general
strict loop, task, builder alias, mutable data or owner-transfer permission.
It remains **experimental and default-off**. Human usefulness and authoring-time
benefit remain **UNMEASURED: zero participants/attempts**.

Root's actual post-measurement DOCUMENTATION AUTHORIZATION intent packet is
[pyalamode-m12-root-final-doc-authorization-08.json](/tmp/pyalamode-m12-root-final-doc-authorization-08.json), 1924 bytes, SHA256 `fa754caf0cd3b6ae55f6e8e4182f60bbefdb21c6fa5b76d135a3209f4654a41b`. It records before-target hashes, approved scope and
actual acceptance/cost/freeze references after measurements and before the filled
document. Its after_document_hashes field assigns actual after-document receipts
to a separate root application receipt. This document cites the prior intent
packet, avoiding a self-referential after-hash cycle. Application and publication are recorded in separate root receipts. The
engineering gate above does not establish their completion. Root records actual
after-document receipts after reviewing and applying the exact delta.
Measured source maps keep the documentation hashes observed during execution;
later prose changes do not rewrite original freezes, raw intervals, controller
oracles, historical failures, partial results or finally maps.
