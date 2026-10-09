# Milestone 4 independent conformance corpus

Status: final frozen-code independent conformance review complete; no remaining blocker observed in this bounded corpus. Authority: `SPEC-sol6.1-composite.md`, especially §§3–5, 8, 10 and 16–18, prerequisite collection commit `1675e94`, and `Docs/milestones/03-collections.md`. This reviewer owns only this document. Product code, committed tests, other documentation, final platform acceptance and commits belong to the implementation workers/orchestrator.

## Admission and evidence rules

The M4 gates are A14–A16 and A34–A35, with the applicable A32 dispatch and A24 authored-location constraints. Static source is passed as text to the checker or written to isolated temporary projects. Check/build must not import or execute that source, including record declarations, decorators, annotations, defaults, adapters or guard generation. Runtime probes intentionally execute separate ordinary library examples and successfully built artifacts only. Every accepted source case must establish exact recursive schemas; every negative case must be refused rather than accepted with an erased obligation.

The default compatible artifact must remain ordinary Python with optional guards off. Records and conversion invariants belong to the ordinary library. Selected boundary guards add an explicit data-validation claim; callbacks retain an external purity/capture obligation, unchecked dependency mutation remains outside the claim, and guard generation must not become a per-call verification service. Conservative unsupported behavior is acceptable when published; false admission, retained mutable aliases, hook execution during generic conversion, missing preconditions accompanied by a stable-snapshot claim, or silent guard selection failures are blockers.

Public API spellings and precise qualifying adapter forms will be reconciled with the worker's approved engineering plan before running positive cases. This does not relax the fixed behavioral outcomes below.

## Fixed adversarial plan

| IDs | Independent case family | Required outcome |
| --- | --- | --- |
| R01–R06 | Exact scalar, nested tuple/collection/record fields; construction, access, equality and copy-with-changes | Accept supported declarations and operations. Parameter/result and replacement schemas remain exact, including bool/int separation. Earlier records stay equivalent to their original values. |
| R07–R12 | Mutable field annotation/value/default; nested `Any`; callback/live capability field; same-name ordinary class | Reject strict declarations/callers. Ordinary constructor and replacement reject reachable unsupported data with a nested field path. |
| R13–R18 | Stable defaults and imported/nested record schemas; declaration/default failure; field ordering, duplicate/unknown/missing changes | Admit only the published supported default syntax and exact schemas. Preserve dependency and characterized failure evidence. Invalid operations fail explicitly. |
| R19–R28 | User property/descriptor/getter, custom constructor/validator, inherited fields, subclass, metaclass, dynamic annotations, decorator alias and field/method alias | No uncharacterized behavioral dispatch admitted. Ordinary validation determines exact type before traversing and does not call foreign hooks. Qualified aliases resolve actual declarations rather than spellings. |
| R29–R34 | Direct/aliased/imported/setter/namespace writes to class fields and behavior; class replacement; generated storage tampering | Known analyzed writes invalidate affected declarations and callers, cold and warm. Runtime private-forgery/unchecked monkey-patching limitations are disclosed without a hostile-Python guarantee. |
| A01–A08 | Qualifying exact dataclass and named-tuple adapters, nested field access and validation | Admit only explicit qualifying compatibility contracts. Merely `frozen=True`, a tuple shape, or a familiar decorator spelling is insufficient. |
| A09–A16 | Adapter inherited methods/metaclass/descriptors/custom construction/post-init/default factory/foreign field hooks | Refuse uncharacterized adapters or fail ordinary registration before unsupported behavior executes. Adapter dependencies and ownership preconditions remain visible. |
| F01–F08 | Exact list/dict/tuple/set/frozenset snapshots, stable data reuse, nested mixed supported shapes, meaningful dict insertion order | Produce the published immutable result types, with homogeneous exact scalar keys/elements. Original nested mutations cannot change any retained result. |
| F09–F16 | Repeated acyclic references; source aliases retained before and after conversion; two independent thaws and repeated exports | Snapshot may discard identity. Every thawed mutable node is independent of source and earlier exports; mutation of one exported alias cannot affect source or another export. |
| F17–F24 | Direct/indirect list/dict cycles; mutable value inside a tuple/record/collection; dict views, mapping proxies, generators, iterators and capabilities | Cycles and unsupported generic values fail with a nested path; no stable-value result is claimed. Generic conversion never delegates to their traversal or restoration hooks. |
| F25–F32 | Exact-type subclasses, hostile equality/hash/iteration/attribute/metaclass hooks, unsupported keys and nested foreign objects | Reject before foreign hooks execute. Counter logs stay empty. Validation paths avoid incidental decimal formatting failures for huge exact int keys. |
| F33–F38 | Omitted/false/malformed exclusive-access precondition; supported synchronized adapter; known instability | No consistent-snapshot claim without the declared qualifying precondition. Synchronization is an explicit characterized contract, not guessed from arbitrary object behavior. Known instability fails explicitly. |
| G01–G06 | Default `off`; opt-in `exports` and `debug`; selected public names, imported/nested names, invalid/empty selection, policy/schema errors | Off is independent of strict acceptance and preserves ordinary execution. Selections are deterministic, validated statically, and reflected in artifact/export evidence. Invalid configuration fails before publication. |
| G07–G14 | Selected scalar/tuple/collection/record parameter subclass and nested mutable/forged inputs; signature/default/positional/keyword calls | Selected export rejects supported invalid input before its body with authored boundary/path. Exact valid inputs preserve ordinary source semantics and failures. |
| G15–G20 | Invalid returned data; callback object/function and conditional callback obligations; guard does not freeze/convert input | Returned data is checked where covered. Data validation cannot certify arbitrary callback purity/captures or automatically promote mutable input. Callable coverage/remaining obligation is explicit. |
| G21–G26 | Checked internal composition, recursion, aliases/captures, exports calls to unselected internals, debug assertions | Exports mode leaves checked internal calls without mandatory wrappers/repeated deep validation. Debug instruments only published supported sites and reports its separate coverage. |
| G27–G32 | Guarded fresh/warm builds, changed source/policy/selection/runtime foundation bytes, sentinel source effects | Relevant changes invalidate evidence; failed builds publish no checked artifact. Neither check nor guarded build evaluates source. Normal imports require no loader or registry. |
| E01–E08 | Export report dimensions, source maps, trust/assumptions/failures, conversion/record/guard costs and actual environment | Evidence distinguishes static claim from additional boundary coverage and reports authored source locations. Published costs include recursive work, repeated deep validation where selected, retained history and fresh export allocation. Both macOS and actual Linux use CPython 3.13.1. |

## Planned execution

1. Inspect the approved engineering plan, shipped record/conversion/guard modules, checker declaration/type/operation analysis, project selection/build machinery and model evidence. Resolve public positive syntax once before generating the literal fixed source corpus.
2. Run independent source cases with `.venv/bin/python` and inspect admission, diagnostic rules/locations, operation and dependency/failure dimensions. Run temporary multi-module writer/alias/default and warm-cache transitions through actual project check/build APIs.
3. Run ordinary runtime invariants using exact-hook counters, nested mutations, retained replacements, repeated acyclic references, cycles/views and independently mutated thaws. Execute selected successfully built guard artifacts to observe before-body rejection and supported debug coverage.
4. Review the final frozen product/tests/examples and inspect current source identities against runtime evidence. Repeat the bounded probes on actual `docker ... python:3.13.1-slim` Linux, recording the actual interpreter/platform/image. Report concrete blockers with source/command/outcome to the main builder and orchestrator.

The plan above was fixed before implementation. The final observations below supersede its interim status; literal source IDs identify executed cases, while the planning table describes behavioral families.

## Interim implementation review

These historical observations concern a changing implementation. All concrete blockers below received focused corrective retests on the final frozen sources and are no longer outstanding.

- The first independent literal source corpus contains 75 cases. All expected statuses matched in the first run through `analyze_source`; candidate application source was never evaluated. Additional forward/self/mutually nested record annotation cases were refused after the builder's definition-order refinement.
- A malformed record declaration's `__module__` metadata triggered a foreign `__hash__` before rejection. The exact reproducer used an ordinary exact-type class with `x: int`, replaced its module string with an object whose hash appends to a log, and called `record(cls)`: the first implementation raised `KeyError` with `['hash']`. The corrected final metadata probe raises TypeError before namespace lookup with zero hooks.
- Known record behavior writes through imported, module-qualified and assigned `setattr`/`delattr` aliases were initially admitted. For example, `from builtins import setattr as put; put(Point, '__eq__', print)` followed by a checked `p == p` was status 0. The final project corpus retests these families for checked functions, collection classes/methods, record and collection helpers, with cold/warm and scalar controls.
- Known writes to actual record runtime foundations were initially admitted: `builtins.type`, `builtins.object`, `sys.modules`, and `pyalamode.records` helpers/registry/exports. The final finite record/conversion/guard foundation and cache probes refuse these writes and leave no artifact.
- Guard generator review found missing import alias names in its generated-name collision inventory, and identified own-module schema imports as a possible duplicate-initialization route when a debug artifact is executed as a script. The final debug artifact avoids alias collisions and prints its ordinary script initialization sentinel exactly once.

All issues were sent with concrete source or code locations to the main builder/runtime helper and orchestrator. A later decorator-availability probe exposed a marker imported after its class declaration. The builder fixed marker/alias/default timing, added record-only build support, and renewed the freeze. The final corpus includes late-import/alias refusals and the positive earlier-alias control.

## Final frozen observations

The final product, tests and examples were independently inspected after the renewed freeze. `.venv/bin/python` was actual CPython 3.13.1 standard GIL on macOS arm64. Linux used actual `python:3.13.1-slim`, CPython 3.13.1 standard GIL, aarch64 LinuxKit/glibc 2.36, image digest `sha256:031ebf3cde9f3719d2db385233bcb18df5162038e9cda20e64e08f49f4b47a2f`. Both complete runs recorded identical before/after product/test/example/harness hashes, identical cross-platform maps, and a subsequent match to current files. No application source was imported or evaluated by the source/check/build probes.

| Independent final gate | macOS | Actual Linux |
| --- | --- | --- |
| Fixed literal source corpus | 93 cases; zero status mismatches or checker exceptions | Same |
| Ordinary runtime probes | 99 assertions | Same |
| Optional guard build/execution walkthrough | 49 assertions | Same |
| Multi-module/warm-cache/debug project corpus | 42 layouts; 168 assertions | Same |
| Combined product suite | 149 tests, 2.166 seconds | 149 tests, 6.909 seconds |
| Before/after source gate | Unchanged | Unchanged |

The literal source corpus has 22 expected admissions and 71 expected refusals. It covers complete nested record/collection schemas, stable defaults, exact constructor/replacement signatures, field access/equivalence, actual aliases, unknown/mutable/callable fields, foreign behavior, analyzed class writes, recursive/late annotations, and late decorator imports/aliases. All statuses matched on both platforms. The application text below was passed to `analyze_source` and never executed.

The 99 runtime assertions cover retained replacements, scalar/generic/schema exactness, ordinary mutation/reinitialization/subclass rejection, nested source mutation isolation, repeated acyclic reference copying, independent mutable nodes within/across thaws, scalar/product reuse, ordering/canonical domains, ownership omission/false/malformed assertions, cycle/view/subclass/capability refusal, forged nested data refusal, huge-int paths, positive dataclass/namedtuple snapshots, and qualifying factory/property/getter-index/default/global failures. Foreign ordinary/metaclass/metadata/namespace hook logs stay empty during validation/conversion. Colliding generated-function and annotation namespace keys are refused before lookup; those regressions are separate from Python's documented pre-entry keyword binding.

The 49 guard assertions build actual off/exports/debug artifacts. A sentinel written by ordinary initialization is absent after check/build and exists only after intentional ordinary import. Off and exports preserve original source bytes; off generates no façade. Selected façades reject exact-type/nested errors before a body whose valid execution raises characterized ZeroDivisionError. Valid failures/defaults/positional-only/keyword-only calls retain their behavior. Returned invalid data is rejected by the generated return validator; that coverage probe substitutes an unchecked body after import and demonstrates validation coverage, not purity under violated dependency assumptions. Missing/wrong/duplicate/nested selections and off-with-selection fail without an artifact. Selected Callable boundaries are refused; data validation does not prove callback purity. Failures identify authored file/function/nested data paths.

The project matrix uses six targets: record `Point.__eq__`, checked `probe.__code__`, `Vector.of` class behavior, `Vector.of.__code__`, `pyalamode.collections._validate`, and `pyalamode.records._record_values`. Each is tested through five routes: imported setter, builtin module setter, assigned setter, imported deleter, and a branch containing a builtin setter alias. Each of 30 layouts starts clean cold/warm, changes an ordinary writer, invalidates affected cache evidence, refuses warm/fresh checks and refuses build without publication. Public record/function/collection and record-helper routes retain an unrelated scalar's valid evidence/cache/fingerprint. Collection helper-module routes retain the approved conservative `pyalamode.*.<behavior>` gate: the scalar marker claim is also refused and misses cache. This is a documented product-wide exclusion, not a false admission or minimal-invalidation claim.

Seven layouts refuse actual record/guard foundations before publication: builtins type/object, sys.modules, record registry, boundary validator/module binding and types.ModuleType. Other layouts refuse cyclic early from-imports while admitting and ordinarily executing safe deferred module recursion; preserve unused import aliases and exactly one own-record script initialization in debug; and count two deep validations around an exports façade versus nine in a separate debug graph with two checked internal leaf calls and one local binding. Emitted exports source leaves direct internal calls untouched; timing alone was not used to infer that property.

A separate native record-only control builds/imports a valid explicit declaration, refuses an invalid mutable-field declaration without output, and inspects independent record evidence dimensions. A dependency-failed record layout reports unverified source evidence and no successful freshness claim. Root-owned suite/CLI observations provide additional release evidence and remain independent of this reviewer corpus.

## Contract and measurement reconciliation

The [M4 handoff](../milestones/04-records.md) and [runtime contract](../evidence/m04-runtime-contract.md) match inspected code: exact fixed product records; shell-only snapshots/exports; exact ownership assertion for every mutable/adapter source; narrow named adapters into concrete product records; explicit `pyalamode_exports` façades; unchanged checked internal calls in off/exports; and documented debug parameter/local/return assertions. Callbacks retain caller evidence obligations; foreign source classes never become strict record data. Runtime field patterns are ordinary Python support; static patterns remain M6. A synchronized adapter needs a separately characterized contract. The implemented assertion neither acquires synchronization nor detects arbitrary ownership/concurrency violations.

Both [macOS JSON](../evidence/m04-runtime-macos.json) and [Linux JSON](../evidence/m04-runtime-linux.json) were read and independently compared with current files. All nine published product fingerprints, runtime-test and benchmark-harness fingerprints match each other and the frozen checkout. Both record unchanged before/after gates, ten conditions × three measured intervals and all correctness obligations passing. The [measurement report](../evidence/m04-runtime-measurements.md) accurately identifies 0/2/28 assertions over eight direct checked leaves, payload sizes 100/1,000, 25 calls/trial, actual interpreter/hardware, included tracemalloc overhead and uncontrolled concurrent load/page-cache conditions. Its tiny off workload returns existing data; it makes no general latency or speedup claim.

Source bounds account for deep/repeated validation, O(R) identity registry searches, growing metadata tuples, possible O(Nh) snapshot descendant revisits, fresh container allocation per thaw occurrence and complete namespace scans during declaration/adapter qualification. Substantial measured debug overhead is openly reported. Library invariants remain independent of optional function guards. No admitted snapshot retains a mutable source alias in these probes.

No remaining blocker was observed in this bounded review. Unchecked monkey-patching, forged private metadata, concurrent ownership violations, process/resource failure and unsupported dynamic Python remain outside the conditional claim. Root owns final staging, commit and later sequencing. This reviewer edited only this document and made no commit, schedule, CatWrangler call or delegation.

## Frozen product SHA-256 map

```json
{
  "pyalamode/__init__.py": "06bc60f8d805fd4e0a82fe953b1490ca3396dd2b2510f5592829c84d974446cb",
  "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
  "pyalamode/boundaries.py": "9e6a903b36e0a8be24a55bb649957306252b21ee47ce5d1eaab7237640d3618a",
  "pyalamode/checker.py": "67cc0dda7a951ffb0660dda1aacec52dbe05e2de48958042e8627ea82a7dd37d",
  "pyalamode/cli.py": "bbe5623ac60aab89c4056b22d412f82a8f4f4ce5544c1c463c036fa639b700e2",
  "pyalamode/collections.py": "1fa0330adc28b33da902ea392a8227af29650672cfe64348324fe3577855dfdc",
  "pyalamode/guardgen.py": "b71356b99188e338e5e59d379d1687069067f9ea869abb2137cf0b66ebb44aa5",
  "pyalamode/model.py": "8c4d1967ccbbef323ff3b0768d16e1092b4a03e77dca669bea7fd879c44b349d",
  "pyalamode/project.py": "ae6ab3a64b7103360818116bef14555f713d36af4887d4eecf1e972fc22ec94d",
  "pyalamode/records.py": "0f98108b894860244c410f5761f80f64a9ce9b212ebb587ab16f77ed69e3d8e9"
}
```

## Executed literal source corpus

`expected: 0` means admitted strict source; `expected: 1` means refused. This JSON is literal input, not evaluated application code.

```json
[
  {
    "id": "R01",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1, Vector.of(2,3))\n",
    "note": ""
  },
  {
    "id": "R02",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R03",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Vector[int]:\n    return p.tags\n",
    "note": ""
  },
  {
    "id": "R04",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, x=2)\n",
    "note": ""
  },
  {
    "id": "R05",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, tags=p.tags.appended(4))\n",
    "note": ""
  },
  {
    "id": "R06",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(a: Point, b: Point) -> bool:\n    return a == b\n",
    "note": ""
  },
  {
    "id": "R07",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Vector[Point]:\n    return Vector.of(p)\n",
    "note": ""
  },
  {
    "id": "R08",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Map[str,Point]:\n    return Map.of((\"a\",p))\n",
    "note": ""
  },
  {
    "id": "R09",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> OrderedMap[str,Point]:\n    return OrderedMap.of((\"a\",p))\n",
    "note": ""
  },
  {
    "id": "R10",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: tuple[Point,int]) -> Point:\n    return p[0]\n",
    "note": ""
  },
  {
    "id": "R11",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> tuple[Point]:\n    return (p,)\n",
    "note": ""
  },
  {
    "id": "R12",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return Point(x=p.x, tags=p.tags)\n",
    "note": ""
  },
  {
    "id": "R13",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int = 1\n    tags: Vector[int] = Vector[int].of()\n@fun\ndef probe() -> Point:\n    return Point()\n",
    "note": ""
  },
  {
    "id": "R14",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Inner:\n    x: int\n@record\nclass Point:\n    inner: Inner\n    values: tuple[Vector[int],str]\n@fun\ndef probe() -> Point:\n    return Point(Inner(1), (Vector.of(2),\"ok\"))\n",
    "note": ""
  },
  {
    "id": "R15",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Inner:\n    x: int\n@record\nclass Point:\n    inner: Inner\n    values: tuple[Vector[int],str]\n@fun\ndef probe(p: Point) -> int:\n    return p.inner.x\n",
    "note": ""
  },
  {
    "id": "R16",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Inner:\n    x: int\n@record\nclass Point:\n    inner: Inner\n    values: tuple[Vector[int],str]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, inner=Inner(2))\n",
    "note": ""
  },
  {
    "id": "R17",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p)\n",
    "note": ""
  },
  {
    "id": "R18",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1, tags=Vector.of(2))\n",
    "note": ""
  },
  {
    "id": "R19",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(True,Vector.of(2))\n",
    "note": ""
  },
  {
    "id": "R20",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1,Vector.of(True))\n",
    "note": ""
  },
  {
    "id": "R21",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1,[2])\n",
    "note": ""
  },
  {
    "id": "R22",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1,(2,))\n",
    "note": ""
  },
  {
    "id": "R23",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1)\n",
    "note": ""
  },
  {
    "id": "R24",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1,Vector.of(2),3)\n",
    "note": ""
  },
  {
    "id": "R25",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(x=1,tags=Vector.of(2),missing=3)\n",
    "note": ""
  },
  {
    "id": "R26",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe() -> Point:\n    return Point(1,x=1,tags=Vector.of(2))\n",
    "note": ""
  },
  {
    "id": "R27",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, x=True)\n",
    "note": ""
  },
  {
    "id": "R28",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, tags=[2])\n",
    "note": ""
  },
  {
    "id": "R29",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, missing=3)\n",
    "note": ""
  },
  {
    "id": "R30",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, tags=Vector.of(\"x\"))\n",
    "note": ""
  },
  {
    "id": "R31",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, 1)\n",
    "note": ""
  },
  {
    "id": "R32",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return p.missing\n",
    "note": ""
  },
  {
    "id": "R33",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return p.__dict__\n",
    "note": ""
  },
  {
    "id": "R34",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return p.__class__\n",
    "note": ""
  },
  {
    "id": "R35",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return p.x < p\n",
    "note": ""
  },
  {
    "id": "R36",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return p is p\n",
    "note": ""
  },
  {
    "id": "R37",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return hash(p)\n",
    "note": ""
  },
  {
    "id": "R38",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return repr(p)\n",
    "note": ""
  },
  {
    "id": "R39",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return str(p)\n",
    "note": ""
  },
  {
    "id": "R40",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    return f\"{p}\"\n",
    "note": ""
  },
  {
    "id": "R41",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(p: Point) -> Point:\n    replace(p,x=2)\n    return p\n",
    "note": ""
  },
  {
    "id": "R42",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom typing import Any, Callable\n@record\nclass Point:\n    x: list[int]\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R43",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom typing import Any, Callable\n@record\nclass Point:\n    x: tuple[int,list[int]]\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R44",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom typing import Any, Callable\n@record\nclass Point:\n    x: Vector[list[int]]\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R45",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom typing import Any, Callable\n@record\nclass Point:\n    x: object\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R46",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom typing import Any, Callable\n@record\nclass Point:\n    x: Any\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R47",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom typing import Any, Callable\n@record\nclass Point:\n    x: Callable[[int],int]\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R48",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\ndef side_effect():\n    print(\"effect\")\n    return 1\n@record\nclass Point:\n    x: int = [1]\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R49",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\ndef side_effect():\n    print(\"effect\")\n    return 1\n@record\nclass Point:\n    x: int = Vector.of([1])\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R50",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\ndef side_effect():\n    print(\"effect\")\n    return 1\n@record\nclass Point:\n    x: int = True\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R51",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\ndef side_effect():\n    print(\"effect\")\n    return 1\n@record\nclass Point:\n    x: int = side_effect()\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R52",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    @property\n    def x(self): return 1\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R53",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    def __getattribute__(self,name): return 1\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R54",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    def __init__(self,x): self.x=x\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R55",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    def __eq__(self,other): return True\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R56",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    def method(self): return 1\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R57",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    __slots__ = (\"x\",)\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R58",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x = 1\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R59",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    x: int\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R60",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nclass Base: pass\n@record\nclass Point(Base):\n    x: int\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R61",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nclass Meta(type): pass\n@record\nclass Point(metaclass=Meta):\n    x: int\n@fun\ndef probe(p: Point) -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "R62",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nclass Child(Point): pass\n@fun\ndef probe(p: Child) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R63",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\n@record\nclass Other:\n    x: int\n    tags: Vector[int]\n@fun\ndef probe(a: Point, b: Other) -> bool:\n    return a == b\n",
    "note": ""
  },
  {
    "id": "R64",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nclass Point:\n    x: int\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p, x=2)\n",
    "note": ""
  },
  {
    "id": "R65",
    "expected": 0,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R66",
    "expected": 0,
    "source": "import pyalamode as pal\nfrom pyalamode import fun\n@pal.record\nclass Point:\n    x: int\n@pal.fun\ndef identity(x:int)->int:return x\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R67",
    "expected": 0,
    "source": "from pyalamode import fun, record as rec, replace as copy\n@rec\nclass Point:\n    x: int\n@fun\ndef probe(p: Point) -> Point:\n    return copy(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R68",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nPoint.x=2\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R69",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nPoint.__eq__=print\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R70",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nalias=Point\nalias.x=2\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R71",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nsetattr(Point,\"x\",2)\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R72",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nPoint.__dict__[\"x\"]=2\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "R73",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nPoint=object\n@fun\ndef probe(p: Point) -> int:\n    return p.x\n",
    "note": ""
  },
  {
    "id": "F01",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom pyalamode import freeze\n@fun\ndef probe(x: int) -> int:\n    return freeze(x, exclusive=True)\n",
    "note": ""
  },
  {
    "id": "F02",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\nfrom pyalamode import thaw\n@fun\ndef probe(x: Vector[int]) -> int:\n    return thaw(x)\n",
    "note": ""
  },
  {
    "id": "R74",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass First:\n    child: Later\n@record\nclass Later:\n    x:int\n@fun\ndef probe(p:First)->int:return p.child.x\n",
    "note": ""
  },
  {
    "id": "R75",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass First:\n    child: Vector[Later]\n@record\nclass Later:\n    x:int\n@fun\ndef probe(p:First)->int:return len(p.child)\n",
    "note": ""
  },
  {
    "id": "R76",
    "expected": 1,
    "source": "from __future__ import annotations\nfrom pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass First:\n    child: Vector[First]\n@fun\ndef probe(p:First)->int:return len(p.child)\n",
    "note": ""
  },
  {
    "id": "R77",
    "expected": 1,
    "source": "from __future__ import annotations\nfrom pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass First:\n    child: Vector[Later]\n@record\nclass Later:\n    child: tuple[First]\n@fun\ndef probe(p:First)->int:return len(p.child)\n",
    "note": ""
  },
  {
    "id": "R78",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nfrom builtins import setattr as put\nput(Point,\"__eq__\",print)\n@fun\ndef probe(p: Point) -> bool:\n    return p==p\n",
    "note": ""
  },
  {
    "id": "R79",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport builtins as b\nb.setattr(Point,\"__eq__\",print)\n@fun\ndef probe(p: Point) -> bool:\n    return p==p\n",
    "note": ""
  },
  {
    "id": "R80",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nput=setattr\nput(Point,\"__eq__\",print)\n@fun\ndef probe(p: Point) -> bool:\n    return p==p\n",
    "note": ""
  },
  {
    "id": "R81",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nfrom builtins import delattr as remove\nremove(Point,\"__eq__\")\n@fun\ndef probe(p: Point) -> bool:\n    return p==p\n",
    "note": ""
  },
  {
    "id": "R82",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport builtins\nbuiltins.type=print\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R83",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport builtins\nbuiltins.object=print\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R84",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport sys\nsys.modules={}\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R85",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport pyalamode.records as r\nr._record_values=print\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R86",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport pyalamode.records as r\nr._RECORDS=()\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R87",
    "expected": 1,
    "source": "from pyalamode import fun, record, replace, Vector, OrderedMap, Map, Set\n@record\nclass Point:\n    x: int\n    tags: Vector[int]\nimport pyalamode.records as r\nr.replace=print\n@fun\ndef probe(p: Point) -> Point:\n    return replace(p,x=2)\n",
    "note": ""
  },
  {
    "id": "R88",
    "expected": 1,
    "source": "@record\nclass P:\n x:int\nfrom pyalamode import record,fun\n@fun\ndef f(p:P)->int:return p.x\n",
    "note": ""
  },
  {
    "id": "R89",
    "expected": 1,
    "source": "@pal.record\nclass P:\n x:int\nimport pyalamode as pal\nfrom pyalamode import fun\n@fun\ndef f(p:P)->int:return p.x\n",
    "note": ""
  },
  {
    "id": "R90",
    "expected": 1,
    "source": "@declaration\nclass P:\n x:int\nfrom pyalamode import fun,record\ndeclaration=record\n@fun\ndef f(p:P)->int:return p.x\n",
    "note": ""
  },
  {
    "id": "R91",
    "expected": 0,
    "source": "from pyalamode import fun,record\ndeclaration=record\n@declaration\nclass P:\n x:int\n@fun\ndef f(p:P)->int:return p.x\n",
    "note": ""
  }
]
```
