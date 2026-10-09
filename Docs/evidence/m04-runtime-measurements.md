# M4 runtime measurements

Final evidence is [macOS JSON](m04-runtime-macos.json), [Linux JSON](m04-runtime-linux.json), the [named harness](../../benchmarks/m04_boundaries.py), and the [runtime contract](m04-runtime-contract.md). Both runs completed against the final frozen product/test/harness sources, passed every generated-call-graph and snapshot/export correctness assertion, and recorded unchanged before/after source maps. An independent current-file comparison after both runs confirmed every recorded digest and equality of both platform maps. The product map contains all nine current sources, including records `0f98108b…`, boundaries `9e6a903b…`, collections `1fa0330a…`, checker `67cc0dda…`, guard generator `b71356b9…`, model `8c4d1967…`, project `ae6ab3a6…`, CLI `bbe5623a…`, and package exports `06bc60f8…`. Complete SHA-256 values are retained in JSON.

The named application fixture digest is `9b849eb0e48c566d43b13398aceb1649620542f9d6e94267fc88abd0c5e078b5`. Each platform builds actual off, exports and debug artifacts, preserving the same fixture source. Platform JSON records artifact-file hashes, exact policies and generated guard coverage. Generated diagnostic paths include the platform's temporary authored-source path, so generated artifact hashes are recorded separately rather than claimed identical across platforms. The harness digest is `be56c03b…`, and runtime-test digest `c3544a59…`; both match on both platforms and the final files.

## Workload and coverage gates

The checked public `entry(Vector[tuple[int,bool]])` performs eight direct calls to an unselected checked `leaf`, each returning its input unchanged. A selected export façade is used for exports/debug; off imports the original function. Untimed instrumentation confirms the façade's `__wrapped__` is the original function and records the authored paths of every deep assertion. Instrumentation aliases are restored to the original validator before timing.

| Actual artifact | Deep assertions per entry | Internal direct leaf calls | Interpretation |
| --- | --- | --- | --- |
| Off | 0 | 8 | No generated assertion or wrapper |
| Exports | 2 | 8 | One selected entry argument assertion and one return assertion; no leaf assertion |
| Debug | 28 | 8 | Two selected export assertions plus checked entry/leaf parameter, local-binding and return data assertions |

This demonstrates the claimed absence of mandatory internal guard validation in off/exports artifacts. Debug deliberately rechecks supported data at instrumented sites. It does not prove arbitrary hidden effects, ownership, callable purity or unchanged dependencies. Product constructor invariants remain ordinary library behavior independently of guard mode.

Snapshot fixtures are an exact insertion-ordered dict `{'items': n exact [int,bool] lists}`. `freeze(..., exclusive=True)` constructs a nested OrderedMap/Vector snapshot; mutation of the original after each measured interval is checked to leave the snapshot unchanged. `thaw` creates nested independent mutable containers; mutating an export is checked to leave the snapshot and another export unchanged.

Both platforms run n = 100 and 1,000, three trials per condition and 25 calls per trial: ten conditions, 30 measured intervals and 750 calls per platform. Timing includes conversion/deep assertions, temporary and result allocation, Python call/loop work, `perf_counter` and `tracemalloc` overhead. Builds/imports, fixture generation, instrumentation, correctness probes, environment/source hashing and JSON output occur outside measured intervals. Allocation peaks are traced Python allocation, not RSS; input fixtures exist before tracing. Results are retained as specified by the call loop (last result and the previous value while it is replaced).

The platform runs were launched concurrently. System load, scheduling and OS page-cache state were uncontrolled; no isolated-system, cold-cache, universal latency or speedup claim is made. The figures below are observations of these named traced workloads. Particularly, the tiny off workload returns existing data and has no substantive computation; its timing is sensitive to loop/timer resolution and does not estimate an application's normal workload.

## Observations

Values are median milliseconds per call across the three trials. Peaks are the maximum traced allocation during a complete 25-call trial.

| Condition | n=100 ms/call macOS / Linux | n=1,000 ms/call macOS / Linux | n=1,000 traced peak bytes macOS / Linux |
| --- | --- | --- | --- |
| Generated off | 0.000285 / 0.000252 | 0.000272 / 0.000233 | 112 / 112 |
| Generated exports | 3.590 / 5.094 | 37.744 / 47.601 | 2,135 / 2,031 |
| Generated debug | 48.836 / 65.175 | 505.766 / 673.360 | 2,131 / 2,027 |
| Nested mutable snapshot | 5.644 / 7.094 | 56.612 / 71.551 | 345,782 / 345,782 |
| Nested snapshot thaw | 1.744 / 2.174 | 17.809 / 22.103 | 196,104 / 196,104 |

Repeated deep debug assertions have substantial cost on this data-returning call graph. Exports bounds validation to the selected entry and its return; off performs none. Low assertion peaks reflect temporary validation stack/path objects, rather than copying the payload. Snapshot/export peaks include new nested containers. These measurements include `tracemalloc`, so they do not establish untraced production latency. Every individual elapsed time/current allocation/peak is retained in JSON, including both payload sizes.

macOS ran CPython 3.13.1, standard GIL build, Clang 16.0.0 on an Apple M1 Pro MacBookPro18,1, arm64, macOS 26.6.2, ten logical CPUs and 16 GiB physical memory. Linux ran `python:3.13.1-slim`, CPython 3.13.1 standard GIL build, GCC 12.2.0, aarch64 LinuxKit/glibc 2.36, five visible logical CPUs and 8,232,894,464 visible memory bytes. The container reported no cgroup memory/CPU maximum; its CPU brand was unavailable. Exact interpreter build/compiler/executable/platform details remain in JSON.

## Bounds and verification

The runtime contract publishes source-algorithm bounds separately from observations. Fixed record field access is O(1); construction/replacement/equality traverse their fixed fields and relevant data. Exact record identity recognition uses an O(R) tuple scan for R declarations. Snapshots copy repeated acyclic references by value; already converted descendants may be revalidated by containing product constructors, yielding O(Nh) recursive validation/copy work at depth h, plus existing homogeneous scalar sorts. Thaw validates before allocating fresh containers for each occurrence. Complete namespace-key scans contribute to declaration and adapter-qualification cost. Guard validation is proportional to schema and data visits; selected export boundaries do not force wrappers on direct internal calls.

The frozen M4 runtime suite passes 31 tests on both published platforms (macOS 0.006s; Linux 0.007s), including deeply typed records/defaults/replacements, public field/API parameter collisions, ownership omission, nested alias isolation, independent exports, cycles/live views/subclasses, foreign metadata/metaclass/namespace hook exclusion, qualifier replacements, erased generic disagreements and malformed storage. The full suite passed 149 tests on the local frozen tree; root owns the final combined two-platform release run and independent conformance ledger. Tests and benchmarks are engineering observations, not a proof of arbitrary Python behavior.

Reproduction uses the literal supported interpreter and container target:

```sh
.venv/bin/python -m unittest discover -s tests -p 'm04_runtime.py'
.venv/bin/python benchmarks/m04_boundaries.py --output Docs/evidence/m04-runtime-macos.json
docker run --rm -v /Volumes/Projects/pyalamode:/workspace -w /workspace python:3.13.1-slim python -m unittest discover -s tests -p 'm04_runtime.py'
docker run --rm -v /Volumes/Projects/pyalamode:/workspace -w /workspace python:3.13.1-slim python benchmarks/m04_boundaries.py --output Docs/evidence/m04-runtime-linux.json
```

No product/test/harness source was edited during or after the final measured runs. This helper made no commit or later-milestone change. Root owns release acceptance and staging.
