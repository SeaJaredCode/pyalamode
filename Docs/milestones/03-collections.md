# Milestone 3: eager persistent collections

Status: implementation and handoff documentation complete; product code, tests, and examples frozen for orchestrator-owned final verification. Final macOS/Linux runtime measurements are published. Authority: `SPEC-sol6.1-composite.md`, read in full, especially §§3–9, 12–14 and 16–18; prerequisites: scalar commit `7d694e0` and module commit `ca3db3f`. The increment implements A11–A13 and the new relevant A32 dispatch gates, while retaining M1/M2 selection, modes, namespace/capture/default assumptions, freshness, and ordinary-build behavior. No CatWrangler, deployment, schedule, records, conversions, guards, effects, variants, general loops/generators, builders, concurrency, or dialect was added.

## Backend, licensing, and trust decision

The storage backend is the existing stock CPython 3.13.1 exact builtin tuple implementation. `pyalamode/collections.py` is original product façade code; it uses ordinary temporary private lists/sets while constructing immutable tuple storage. No external package dependency, vendored persistent-library source, or copied CPython implementation was introduced. Thus there is no new third-party package approval or license to carry in `pyproject.toml`. Python's software is governed by the [PSF License Version 2 and accompanying incorporated-software notices](https://docs.python.org/3.13/license.html). The supported interpreter installation supplies that software and its notices; this local source build neither vendors nor redistributes it.

Reusing a tuple backend resolves the present licensing/trust decision with a deliberately bounded performance tradeoff: every changed version copies its outer storage. The claim is persistence with stable retained versions, not a trie/HAMT structural-sharing cost claim. More sophisticated storage can replace the private backend later only after preserving these exact value/ordering/invariant contracts and supplying its own license/trust/cost evidence.

The trusted foundation includes CPython scalar/tuple/function/GenericAlias operations and the shipped product façade, including recursive validator, typed equality, canonical scalar ordering, and private construction mutation. It is distinct from source-checked application callbacks. Reports record `collections-v1` trust and concrete/transitive operation identities; `foundation_identities()` hashes `collections.py` along with the other installed product sources. Check/cache/build fingerprints include those bytes and operation version `scalar-tuple-call-collection-ops-3`. Checked artifacts remain unchanged ordinary application source plus evidence, with the ordinary installed product package available at execution.

Analyzed public class/method/constructor changes, GenericAlias routes, module/class aliases, method behavior replacements, and concrete internal backend routes invalidate admission. Known backend helper/base changes such as `_validate`, `_Frozen.__eq__`, or `_MapBase.of` conservatively invalidate the product foundation. Replacement identities participate in warm-cache context. Unchecked runtime monkey-patching, forged private storage, interpreter replacement, and application code outside the analyzed source graph remain violations of disclosed dependency/invariant assumptions. This is not hostile-Python isolation or complete dynamic alias inference.

The finite transitive backend foundation inventory is `builtins.type`, `any`, `all`, `id`, `set`, `enumerate`, `tuple`, `len`, `sorted`, `repr`, `hex`, `zip`, `iter`, `next`, `object`, `getattr`, `bool`, `int`, `str`, `bytes`, `classmethod`, `TypeError`, `AttributeError`, `IndexError`, `KeyError`, `ValueError`, `__build_class__`, and `__import__`, plus `types.FunctionType` and `types.GenericAlias`. It covers actual explicit/implicit backend reads, declaration, and import setup. A private list literal uses a Python opcode and does not read an ambient `builtins.list` binding. Known dependency writers through direct/module aliases, dictionary setters, recognized setter calls, imported helper aliases, and selected ordinary writer source invalidate the four collection class contracts and record dependency origins in warm-cache keys. Unrelated scalar bodies retain their existing individual foundation gates. This inventory is a dependency condition, not admission for application calls to these names.

## Exact schemas and ordinary runtime invariants

The new finite annotations are `Vector[T]`, `OrderedMap[K, V]`, `Map[K, V]`, and `Set[T]`, from stable resolved `pyalamode` imports or module aliases. `T`/`V` recursively contain exact None/bool/int/str/bytes, fixed/homogeneous tuples, and these four exact product classes. Callable members are excluded. Map keys and Set elements have one exact scalar domain: None, bool, int, str, or bytes. Recursive `Any`, protocols, subclasses, collection-valued keys, heterogeneous key/element domains, general type variables/unions, and callable data do not qualify.

All static parameterized constructors validate their complete nested schema. Ordinary runtime type subscription uses standard `types.GenericAlias`; its type arguments are erased metadata. For example, `Vector[int].of(True)` is statically rejected but ordinary execution produces a stable Vector containing bool. Runtime constructors preserve deep immutable-data invariants and map-key/Set-element scalar homogeneity; they do not infer the complete parameterized schema. Vector/map values can therefore contain heterogeneous stable data in ordinary unchecked use. Their use as a checked `Vector[T]` or `Map[K,V]` requires the stated exact schema.

The façade validates exact admitted types before traversing them and never calls foreign `__iter__`, `__hash__`, `__eq__`, `__index__`, property, formatter, or conversion hooks. Invalid nested data raises `TypeError` with an immutable-data path. That is an ordinary invariant violation, outside valid checked input/callback-result contracts. Generic validation does not freeze mutable values. No mutable exports/evolvers exist. All public classes reject ordinary attribute reassignment/deletion, reinitialization, and subclassing. Private exact tuples contain no retained mutable alias. Construction/update validation belongs to the value library, not a wrapper placed around every checked application call.

## Complete admitted operation vocabulary

In this table, `T`, `V`, `R`, and `A` are recursively admitted data schemas; `K` and Set's `S` are exact homogeneous scalar domains. All method arguments are explicit positional arguments, with no keywords, star expansion, arbitrary iterables, callbacks-by-protocol, or method aliases. `C` means the same exact concrete collection class and recursive schema. Every operation is pure under its value/dependency/callback preconditions, with no effects. Resource exhaustion and process interruption are outside the finite failure contract.

| Operation | Exact input and result signature | Characterized invocation failures |
| --- | --- | --- |
| `Vector.of` | `Vector.of(T, ...) -> Vector[T]`; nonempty data infer one schema; `Vector[T].of(T, ...)` supplies it, including zero arguments | Recursive nested-member validation: conservative `RecursionError` |
| `OrderedMap.of`, `Map.of` | `C.of(tuple[K,V], ...) -> C[K,V]`; nonempty exact pairs infer schemas; `C[K,V].of(...)` also admits zero pairs | Recursive nested-value validation: conservative `RecursionError` |
| `Set.of` | `Set.of(S, ...) -> Set[S]`; typed `Set[S].of(...)` admits zero arguments | None under valid scalar-domain contract |
| `v[i]` | `Vector[T], exact int -> T`; negative indexes use ordinary Python normalization | `IndexError` |
| `v[start:stop:step]` | `Vector[T], exact int/None bounds -> Vector[T]`; default/negative/clipped bounds follow stock tuple slicing | `ValueError` for zero step |
| `v.appended` | `Vector[T].appended(T) -> Vector[T]` | Nested new member: conservative `RecursionError` |
| `v.updated_at` | `Vector[T].updated_at(exact int, T) -> Vector[T]` | `IndexError`; nested new member: conservative `RecursionError` |
| `v.concat` | `Vector[T].concat(Vector[T]) -> Vector[T]` | Nested member validation: conservative `RecursionError` |
| `v.map` | `Vector[T].map(checked pure Callable[[T],R]) -> Vector[R]` | Callback failure bound; nested returned-data validation: conservative `RecursionError` |
| `v.filter` | `Vector[T].filter(checked pure Callable[[T],bool]) -> Vector[T]` | Callback failure bound |
| `v.fold` | `Vector[T].fold(checked pure Callable[[A,T],A], admitted A initial) -> A` | Callback failure bound; nested initial/accumulator validation: conservative `RecursionError` |
| `m[key]` | `C[K,V], K -> V` for C = OrderedMap or Map | `KeyError` when absent |
| `m.get` | `C[K,V].get(K, V default) -> V`; default is required and evaluated/validated ordinarily even if key exists | Nested default validation: conservative `RecursionError` |
| `m.contains`, `key in m`, `key not in m` | `C[K,V], K -> bool` | None |
| `m.updated` | `C[K,V].updated(K,V) -> C[K,V]` | Nested new value: conservative `RecursionError` |
| `m.without` | `C[K,V].without(K) -> C[K,V]`; missing key is a no-op | None |
| `m.merge` | `C[K,V].merge(C[K,V]) -> C[K,V]`; right values win | Nested-value validation: conservative `RecursionError` |
| OrderedMap traversals | `.entries() -> Vector[tuple[K,V]]`, `.keys() -> Vector[K]`, `.values() -> Vector[V]` | None |
| Map canonical traversals | `.ordered_entries() -> Vector[tuple[K,V]]`, `.ordered_keys() -> Vector[K]`, `.ordered_values() -> Vector[V]` | None |
| Set membership | `Set[S].contains(S) -> bool`; `S in Set[S]` / `S not in Set[S] -> bool` | None |
| Set persistent changes | `.added(S) -> Set[S]`, `.without(S) -> Set[S]`; duplicates/absent removals are no-ops | None |
| Set algebra | `.union(Set[S])`, `.intersection(Set[S])`, `.difference(Set[S]) -> Set[S]` | None |
| Set canonical traversal | `.ordered_values() -> Vector[S]` | None |
| Collection size | `len(C) -> exact int`, all four classes | None |
| Collection equality | Same recursively exact schema `C == C` / `C != C -> bool`; recursively typed value equivalence | Nested payload equality: conservative `RecursionError` |
| Tuple indexing | Fixed tuple: in-range literal exact int -> selected member schema. Homogeneous `tuple[T,...]`: exact int -> T | Conservative `IndexError` upper bound; fixed out-of-range indexes are rejected before admission |
| Tuple slicing | Fixed tuple: literal int/None bounds, nonzero step -> exact sliced fixed tuple schema. Homogeneous `tuple[T,...]`: int/None bounds -> same tuple schema | Conservative `ValueError` upper bound; fixed zero-step slices are rejected |
| Tuple equality | Matching recursively exact tuple schemas `==` / `!= -> bool`; stock Python tuple comparison on exact admitted elements | Nested payload equality: conservative `RecursionError` |

The recursive library failure bound applies when the relevant member/value/result/accumulator schema is a tuple or collection, separately from application recursion. Scalar-only constructor/update callbacks retain precise scalar failure bounds. The complete conditional callable invocation upper bound is now `{IndexError, KeyError, ValueError, ZeroDivisionError, RecursionError}`. Concrete targets contribute their actual characterized transitive failures; a conditional alternative cannot be erased merely because another alternative has a concrete target.

`map` invokes once per input item from index zero upward; `filter` preserves relative order and requires an exact bool decision; `fold` passes `(accumulator, item)` left to right and returns the initial value on an empty Vector. The first callback failure stops the operation at that ordered index. Known checked targets/captures/defaults/returned callable metadata remain intact and flow into call/dependency/failure evidence. A passed conditional `Callable` input is a caller obligation, not evidence about an arbitrary actual function. Runtime higher-order methods accept exact Python functions and validate data results/bool decisions; they cannot prove purity, captures, or complete signatures. Unknown/ordinary effectful targets, lambda expressions, keyword-only callback targets, and uncharacterized callable objects fail strict admission.

Known ignored return-only updates report `PAL250` with operation identity, source location, persistent-operation origin, and a bind/return remediation. Ordinary data constructors with arbitrary iterable arguments, raw `Vector()`/`Map()` empty calls in strict source, ordinary iterator objects, bound-method aliases, mutation, tuple/collection ordering comparisons, hashing, formatting/repr calls, and unordered general `map`/`filter`/`fold`/iteration remain unsupported. Runtime ordinary `Vector` iteration is ordered convenience for an unchecked shell; maps and Set explicitly reject general iteration. Tuple index/slice/equality is the finite expansion needed to consume map entry Vectors; no destructuring/statement loop extension was implied.

## Ordering, equivalence, and first-error contracts

Vector element order and OrderedMap entry order participate in contract equivalence. OrderedMap replacement retains the existing slot; a new key appends. Duplicate constructor keys use the last value while retaining the first insertion slot. Removal deletes that slot, so later reinsertion appends. Merge applies right-wins values while keeping left slots and appending new right keys in right order.

Map equivalence is typed extensional key/value equivalence; Set equivalence is typed extensional membership. Canonical internal tuple storage prevents incidental hash/history order from leaking. Scalar total order is singleton None, False before True, ascending exact integers, and lexicographic exact str/bytes. Domains cannot mix, so bool/int cross-equality, heterogeneous ties, NaN, and custom comparators are excluded. Duplicate keys/members collapse by exact-type scalar equality. No process hash is exposed or used for storage ordering.

All four product classes implement deterministic runtime representations using exact scalar/builtin tuple/product formatting only; product equality recursively distinguishes bool and int even in payloads. Foreign values compare false through product-side equality without invoking foreign hooks. Strict `repr`, `str`, interpolation, arbitrary serialization/formatter hooks, and arbitrary unordered traversal remain excluded. Ordinary public repr retains CPython scalar formatting failures, including `ValueError` when an exact integer exceeds the configured decimal-digit conversion limit. Internal validation paths separately use a deterministic hexadecimal fallback for such keys, so valid huge-int map construction/nested validation/merge do not acquire a hidden formatting failure. Ordered outputs from Map/Set arise only through the named canonical traversal methods. Transforming/folding the resulting Vector preserves that canonical first-failure order. Runtime Map validation visits supported value paths in canonical key order; OrderedMap visits insertion order. Invalid keys/mixed domains/mutable data are outside the admitted input equivalence relation, so constructor rejection of unsupported inputs is not a certified unordered computation over those inputs.

## Actual cost contract

The following upper bounds describe final source algorithms, treating scalar comparison and reference operations as unit cost. Arbitrary integer bit lengths/text lengths add comparison/representation cost. `n`/`m` are outer collection sizes, `r` is produced output length, and `D` is recursive value-validation/equality work, including repeated visits, nested canonical sorts, and constructed diagnostic-path lengths. Callback time and accumulator growth are additional. Constants and runtime allocation behavior are measurements, not universal guarantees.

| Work | Time bound | Additional live/retained outer storage |
| --- | --- | --- |
| Vector `.of` | O(n + D) | O(n) references |
| Vector index / len | O(1) | O(1) |
| Vector slice | O(r) | O(r) references; unchanged full slices may reuse tuple storage |
| Vector `.appended` / `.updated_at` | O(n + Dnew) | O(n) references per changed version |
| Vector `.concat` | O(n + m + Dother) | O(n + m) references |
| Vector map/filter | O(n + callback work + returned-data validation for map) | O(r), plus temporary output references |
| Vector fold | O(n + callback work + repeated initial/accumulator validation) | O(1) outer accumulator binding; result/retained callback allocations depend on callback |
| Map/OrderedMap `.of` | O(n log n + Dvalues); scalar-key sorts and linear duplicate collapse | O(n) entries plus temporary sort/index references |
| Map/OrderedMap lookup/get/contains | O(n), plus get's default validation | O(1) |
| Map/OrderedMap updated/without | O(n + Dnew for update) | O(n) changed outer entry references; no-op removal may reuse receiver |
| Map/OrderedMap merge | O((n+m) log(n+m) + Dvalues), including validated constructor reuse | O(n+m) entries and temporary references |
| Map/OrderedMap entries traversal | O(1) wrapper over existing exact tuple | O(1) wrapper; entry tuple shared immutably |
| Map/OrderedMap keys/values traversal | O(n) | O(n) references |
| Set `.of` | O(n log n), scalar sorting and linear duplicate collapse | O(n) references |
| Set contains/added/without | O(n) | O(n) changed storage; no-op may reuse receiver |
| Set union/intersection/difference | O(n+m), validated scalar-domain merge | O(n+m) maximum result/temporary references |
| Set `.ordered_values` | O(1) wrapper over existing canonical tuple | O(1) wrapper |
| Collection equality | O(n + recursively compared payloads); short-circuits unequal lengths/values | Recursive stack proportional to schema depth |
| Runtime repr | O(rendered output + recursively visited data), scalar formatting cost additional | Output text and recursive stack |
| Retaining k similarly n-sized changed versions | Update-dependent time above | O(kn) outer references; immutable unchanged element/pair objects shared; append history sizes sum and can be quadratic in k |

These bounds do not include a HAMT/logarithmic update claim. Release measurements are owned by the runtime helper in [`benchmarks/m03_collections.py`](../../benchmarks/m03_collections.py), [`m03-runtime-macos.json`](../evidence/m03-runtime-macos.json), [`m03-runtime-linux.json`](../evidence/m03-runtime-linux.json), and the [measurement report](../evidence/m03-runtime-measurements.md). Both final runs record the same current product/source snapshot, including checker `7791b1ae…`, model `6f0cbbc5…`, and runtime `c0a4738a…`, with unchanged before/after source gates and independent current-file comparison.

Each platform ran three trials for each of 36 conditions (108 measured intervals), at n = 100, 1,000, and 10,000. Inputs use seed-17 shuffled exact integers without duplicates. Update conditions perform 32 distinct existing-slot revisions at fixed size n; Set performs a removal plus addition per revision, for 64 calls. Latest-only retention keeps base and latest values; history retention keeps the base plus all 32 revisions. All construction and retained-history content assertions passed. Timings include operation validation/copying/allocation/loop and `tracemalloc` overhead, and exclude startup/import, input/base construction, content checks, environment hashing, and JSON output. Memory is traced Python allocation, not RSS; bases/fixtures are allocated before tracing. OS page-cache state is uncontrolled.

At n = 10,000, observed median milliseconds and maximum traced allocation peaks were:

| Collection | Construction ms macOS / Linux | 32 latest-only revisions ms macOS / Linux | 32 retained revisions ms macOS / Linux | Construction / latest / retained peak bytes, both platforms |
| --- | --- | --- | --- | --- |
| Vector | 17.287 / 22.998 | 1.439 / 1.645 | 1.399 / 2.729 | 160,896 / 241,516 / 2,644,228 |
| OrderedMap | 48.975 / 63.678 | 31.356 / 42.373 | 32.873 / 42.815 | 2,618,092 / 244,220 / 2,646,932 |
| Map | 61.337 / 62.830 | 32.781 / 42.474 | 32.859 / 43.014 | 2,698,132 / 244,220 / 2,646,932 |
| Set | 12.264 / 14.093 | 110.562 / 125.217 | 110.012 / 127.815 | 325,616 / 241,588 / 2,644,300 |

macOS ran CPython 3.13.1 standard GIL on an Apple M1 Pro MacBookPro18,1, arm64, macOS 26.6.2, 10 logical CPUs and 16 GiB physical memory. Linux ran CPython 3.13.1 standard GIL in an aarch64 LinuxKit/glibc 2.36 container with five visible logical CPUs, about 8.23 GB visible memory, and no cgroup CPU/memory maximum reported. The JSON files retain exact interpreter build/compiler/container/environment details and every observation. These workloads demonstrate retained-history costs and correct values under the recorded conditions; they do not establish universal performance or an authoring/usability improvement.

## Verification and downstream handoff

Local final code-freeze verification used CPython 3.13.1, standard GIL build, macOS arm64. The combined M1/M2/M3 suite passed **93 tests**, including 19 static/build M3 tests and 24 runtime M3 tests. Root owns the final two-platform run, independent conformance digest, ledger, and commit. These are engineering/adversarial observations, not a proof of all Python behavior or a user study.

```sh
.venv/bin/python -m unittest discover -s tests -p 'm0*.py'
.venv/bin/python -m pyalamode check examples/collections --no-cache
.venv/bin/python -m examples.collections.demo
.venv/bin/python -m pyalamode explain Vector
.venv/bin/python -m pyalamode explain PAL250
```

The collection example checks eight functions (including nested callbacks) in one functional module. Ordinary execution prints the retained original `Vector.of(10, 20)`, adjusted `Vector.of(15, 25, 35)`, total `60`, canonical amounts `Vector.of(130, 200)`, revised insertion-ordered prices, and canonical selected labels. Tests reject nested builtin mutable members, exact-type disagreements, custom dispatch/index/iteration/formatter/hash routes, unknown/effectful callback targets, ignored updates, unknown generic schemas, class/backend behavior writers, finite transitive foundation writers, and non-characterized initializer callback invocation. They retain old versions, compare canonical histories, characterize callback/deep-validation failures, exercise exact map entry tuple operations, cover unrestricted exact huge-int map keys without hidden decimal-formatting failure, verify runtime-byte/writer cache invalidation, and preserve unchanged ordinary builds with no application source execution during checking.

`TypeSpec` now serializes the four recursive generic collection schemas and cache decoding restores them. `Value` retains exact data/callable separation; collections do not contain callable evidence. `FunctionInfo.operations` and serialized `FunctionContract.operations` preserve and propagate concrete admitted operation identities through calls and warm caches. `FunctionalAnalyzer._data_schema`, `matches`, and `_schema_matches` are the closed recursive admission points; `_collection_callback` consumes actual callable evidence and never an annotation-only purity assertion; `_collection_operation` records invocation failures/operation identity. Source replacement discovery now precedes signature admission while all checked signatures still precede body checking for recursion. These are internal extension interfaces, not a generic public registry.

M4 should extend the same closed data-schema/value-admission hooks with exact product records, snapshots, fresh exports, and selected boundary assertions; it must preserve erased generic obligations, mutable-alias exclusion, callback evidence, canonical unordered traversal, and runtime-byte freshness. Failure-universe expansions must update conditional call contracts and cache/version identity without erasing concrete targets/captures. No foundation record/conversion/guard/effect stub was added in this unit.

Owned files: `pyalamode/__init__.py`, `pyalamode/checker.py`, `pyalamode/model.py`, `pyalamode/cli.py`, `tests/m03_collections.py`, `tests/fixtures/m03/*.py`, `examples/collections/*.py`, `README.md`, and this report. Root-dispatched runtime helper owns `pyalamode/collections.py`, `tests/m03_runtime.py`, `benchmarks/m03_collections.py`, and `Docs/evidence/m03-runtime-*`. Independent reviewer owns `Docs/conformance/m03-cases.md`. This worker did not alter specifications, prior reports, orchestrator ledger/conformance/evidence files, or make commits. Root owns final staging, verification, commit, and release decision.
