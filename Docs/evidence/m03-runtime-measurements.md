# M3 runtime collections and measured tuple backend

## Runtime contract

`Vector`, `OrderedMap`, `Map`, and `Set` are exact final classes with frozen slots and exact builtin tuple storage. No external collection library, mutable export, evolver, hash lookup, or runtime purity registry is used. Empty ordinary constructors are supported; data constructors are `Vector.of(*items)`, `Set.of(*items)`, and map `.of(*exact_two_element_tuple_pairs)`. Runtime `GenericAlias` arguments are erased; `Vector[str].of(1)` remains an ordinary valid runtime construction. The checker establishes a generic schema separately.

Construction and newly supplied payloads recursively validate exact `None`, `bool`, `int`, `str`, `bytes`, tuples, and these four collection classes. Mutable values, subclasses, custom objects, and callables are rejected without executing foreign attribute, iteration, equality, hashing, or representation hooks. Diagnostic paths are deterministic for their characterized traversal. Exact integer keys whose decimal representation exceeds CPython's digit limit use hexadecimal only in internal diagnostic paths. Public representation retains ordinary scalar formatting and can raise `ValueError` for such integers; strict formatting is outside this milestone.

Map keys and Set members share one homogeneous exact scalar domain. `bool` and `int` remain distinct, including within nested equality. `None` is a single value; canonical order is `False < True`, numeric integer order, or lexicographic string/bytes order. Map and Set store canonical order, so equivalence, explicit outputs, and representation do not depend on insertion permutation or hash seed. Vector and OrderedMap order is part of equivalence. Duplicate map keys use the last value; OrderedMap keeps the first insertion slot. Merge uses right-hand values and left-hand slots followed by new right-hand keys.

The ordered traversals are methods returning Vector: OrderedMap `entries()`, `keys()`, `values()`; Map `ordered_entries()`, `ordered_keys()`, `ordered_values()`; Set `ordered_values()`. Map and Set membership syntax delegates to `contains`; map/set iteration explicitly raises `TypeError`, including Python's sequence fallback. Ordinary Vector iteration is supported. Vector indexing uses exact integers or slices whose bounds are exact integers/None; bool indices are rejected. Out-of-range indexing raises `IndexError`, absent map indexing raises `KeyError`, and a zero slice step raises `ValueError`. Map `get(key, default)` requires a recursively valid default, and absent `without` is a no-op.

Vector `map(callback)`, `filter(predicate)`, and `fold(callback, initial)` are eager in vector order. Runtime callbacks must be exact Python functions. Their purity, signature, failure bounds, and stable captures are caller obligations established by source checking for strict callers. Ordinary runtime calls execute those functions normally, including any effects or exceptions. Map results, each fold accumulator, and the initial accumulator are recursively validated; predicate results must be exact bool. There are no unordered callbacks. Recursive validation/equality can raise `RecursionError` at the interpreter's finite recursion limit.

These invariants cover values made and operated on through the characterized API. Deliberate `object.__setattr__` or class/module replacement is outside that invariant and trust contract. Constructor rejection of malformed forged storage is tested; the library is not a security boundary against arbitrary interpreter tampering. No equivalence claim is made for first errors on inadmissible constructor data whose keys/pairs themselves violate the preconditions.

## Cost accounting

Here `n` and `m` count top-level elements/entries. `D` denotes recursively traversed payload occurrences and their validation work, including nested canonical sorting and constructed diagnostic-path lengths. Repeated references are traversed repeatedly rather than globally memoized. Arbitrary integer magnitude, string/bytes comparison and representation lengths, and nested payload costs add to the scalar-unit bounds below.

| Operation | Tuple backend cost under valid scalar-unit preconditions |
| --- | --- |
| `len`, Vector scalar indexing | O(1) |
| Vector construction | O(n + D) validation and tuple storage |
| Vector slice selecting k items | O(k) tuple references |
| Vector append / indexed update | O(n + D_new); tuple copying preserves the old version |
| Vector concat | O(n + m + D_other), including recursive validation of the other vector |
| Map / OrderedMap / Set construction | O(n log n + D) general sorting/grouping bound; ordered inputs and tiny bool/None domains can cost less |
| Map lookup / contains / get; Set contains | O(n) scalar comparisons; get also validates its default |
| Map / OrderedMap updated / without; Set added / without | O(n + D_new) scans and tuple copying; absent removal and duplicate Set addition can reuse the same object |
| Map / OrderedMap merge | O((n + m) log(n + m) + D), with domain validation and sorted/grouped construction; no repeated quadratic duplicate-key scan |
| Set union / intersection / difference | O(n + m) domain validation, canonical two-pointer traversal, and output allocation |
| Map/OrderedMap entry-vector export; Set ordered-value export | O(1) wrapper sharing the immutable storage tuple |
| Map/OrderedMap key/value-vector export | O(n) tuple references |
| Vector map / filter | O(n) traversal plus callback costs and, for map, recursive result validation |
| Vector fold | O(n) callbacks plus initial and every accumulator validation; growing accumulators can make total validation quadratic |
| Equality / representation | Recursive payload/comparison/emitted-text costs, with order-sensitive or canonical equivalence as above |

Single updates copy tuple references rather than every immutable payload. This shares payloads, but does not use a tree/trie backend with logarithmic path updates. Retaining `k` versions of size `n` can retain O(kn) references. Retaining successively appended versions includes the growing tuple sizes. These are complete cost qualifications, not an O(n) time claim for every operation or a universal latency guarantee.

## Verification and protocol

The owned runtime suite has 24 tests, passing on CPython 3.13.1 standard GIL builds on both macOS and Linux (0.004 seconds each). It covers retained versions of all four classes, exact domain/order/equality, recursive mutation rejection and hostile hooks, indexing/slicing failures, callback output/accumulator validation, ordinary callback obligations, frozen slots/reinitialization, iteration fallback, canonical error traversal, and large integer diagnostic paths. The independent reviewer reran 262 assertions per seed for seeds 1, 2, and 8675309 on the final runtime/checker bytes, with identical output SHA256 `65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942`. It also passed 43 focused huge-int assertions, observed zero foreign hook calls, and reproduced the three original decimal-formatting failures using the preceding backend in a temporary copy. Its [conformance artifact](../conformance/m03-cases.md) records the bounded observations. Passing these finite probes is evidence for the published contract, not proof over all Python programs.

The named harness is [benchmarks/m03_collections.py](../../benchmarks/m03_collections.py). Defaults are sizes 100/1000/10000, three trials per condition, and 32 revisions per update condition, for 36 conditions and 108 measured intervals per platform. Constructor inputs are seed-17 shuffled exact integers without duplicates; map payloads are int-to-int. Vector updates replace an existing index, maps replace an existing key, and a Set revision removes an existing member then adds a fresh integer. Thus Set has **64 actual runtime update calls** for 32 revisions; the other classes have 32.

The latest-only condition retains the base and final version. The history condition retains the base plus all 32 revisions. Correctness checks inspect every revised cell/member in every retained version outside measurement. Timings include actual runtime validation, scans/copies/allocations, loop, timer, and tracemalloc overhead. Imports/startup, input generation, update-base construction, correctness checks, environment/hash collection, and JSON writing are excluded. GC collection occurs before each interval; OS page-cache state is uncontrolled. Tracemalloc reports Python allocations during the interval, not process RSS; existing inputs/update bases are outside that accounting.

Every final run compares SHA256 maps before and after all measured intervals for the owned runtime/test/harness and the complete `model.foundation_identities()` product artifacts. A mismatch aborts without writing new evidence. Platform timing runs are serialized on the shared host. Historical runs before a product correction are replaced only after the renewed source freeze.

## Final measured snapshot, 2026-10-09

Both final runs passed all retained-value assertions and the before/after source gate. A separate post-run comparison confirmed that both JSON maps match the current owned sources and complete product foundation. The complete three-trial observations for **all three sizes** are in [macOS JSON](m03-runtime-macos.json) and [Linux JSON](m03-runtime-linux.json).

The native run used CPython 3.13.1, Clang 16.0.0, standard GIL, macOS 26.6.2 arm64, an Apple M1 Pro MacBookPro18,1, 10 logical CPUs, and 17,179,869,184 physical-memory bytes (16 GiB). The Linux run used CPython 3.13.1, GCC 12.2.0, standard GIL, aarch64 Linux 5.15.49-linuxkit/glibc 2.36 in Docker on that same host. The Docker VM exposed five logical CPUs and 8,232,894,464 memory bytes; `memory.max` was `max`, and `cpu.max` was `max 100000`. CPU branding was unavailable inside the container. The measured image was `python:3.13.1-slim`, image ID `sha256:0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae`.

The table shows n=10000, median elapsed **seconds per complete condition**, and maximum traced peak bytes across its three trials. Update timings cover 32 revisions, with 64 actual Set calls. Peaks happened to agree exactly between these platform observations; timings and allocations should not be extrapolated to other payloads, machines, concurrency, interpreter builds, or uncontended environments. The shared host was not an isolated performance laboratory, and tracemalloc overhead is included.

| Collection | Condition | macOS median seconds | Linux median seconds | Maximum traced peak bytes, each platform |
| --- | --- | ---: | ---: | ---: |
| Vector | construction | 0.017287 | 0.022998 | 160896 |
| Vector | updates_latest | 0.001439 | 0.001645 | 241516 |
| Vector | updates_retained | 0.001399 | 0.002729 | 2644228 |
| OrderedMap | construction | 0.048975 | 0.063678 | 2618092 |
| OrderedMap | updates_latest | 0.031356 | 0.042373 | 244220 |
| OrderedMap | updates_retained | 0.032873 | 0.042815 | 2646932 |
| Map | construction | 0.061337 | 0.062830 | 2698132 |
| Map | updates_latest | 0.032781 | 0.042474 | 244220 |
| Map | updates_retained | 0.032859 | 0.043014 | 2646932 |
| Set | construction | 0.012264 | 0.014093 | 325616 |
| Set | updates_latest | 0.110562 | 0.125217 | 241588 |
| Set | updates_retained | 0.110012 | 0.127815 | 2644300 |

The larger traced allocation peaks for retained histories are consistent with retaining their outer tuple references. They do not measure process RSS or establish a cross-platform speed ranking. Construction sorting/grouping, repeated linear key/member scans, deep payload validation, and callback costs retain the qualifications above.

Reproduction commands, run serially from the repository root:

```sh
.venv/bin/python -m unittest discover -s tests -p 'm03_runtime.py' -v
docker run --rm --volume /Volumes/Projects/pyalamode:/workspace --workdir /workspace python:3.13.1-slim python -m unittest discover -s tests -p 'm03_runtime.py' -v
.venv/bin/python benchmarks/m03_collections.py --output Docs/evidence/m03-runtime-macos.json
docker run --rm --volume /Volumes/Projects/pyalamode:/workspace --workdir /workspace python:3.13.1-slim python benchmarks/m03_collections.py --output Docs/evidence/m03-runtime-linux.json
```

Owned source SHA256 identities:

| Path | SHA256 |
| --- | --- |
| pyalamode/collections.py | `c0a4738ae85c1048b44c160a19f2d425c2872a5b601dcd352989903ad4102ab6` |
| tests/m03_runtime.py | `88db699167977af3934c85c793dc4f674e702f80f28a0dc19bba308ffd31551b` |
| benchmarks/m03_collections.py | `f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141` |

The full product map in both JSONs additionally records checker `7791b1ae028218413af16d02f956bb434f6cb8e7b073d4369ad6ba1b83683539`, model `6f0cbbc5837c3054f65bb1c3b8d4f6b0c5ce85a39506037790fdcc3af65fa184`, and the installed __init__/project/CLI source identities. Documentation changes do not change those product artifacts. This helper owns the runtime, runtime tests, named benchmark, and these three evidence files; it makes no commits. Root owns final combined verification, staging, commit, and the milestone decision.
