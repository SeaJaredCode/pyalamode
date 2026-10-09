# M5 runtime measurements

The frozen harness builds the actual checked `m05_workload.py` artifact with boundary guards off, imports that generated artifact through ordinary Python, and measures its capability operations. Seven checked functions include State direct/borrow, Clock, Random, Environment, IO, and `Effectful[[ClockCapability], int, Clock]` callback lending. An untimed actual checked callback smoke returns 7 through the recorded clock. The artifact retains the original function source/code; no invocation wrapper, callable registry or special loader is involved.

Raw evidence: [macOS JSON](m05-runtime-macos.json), [Linux JSON](m05-runtime-linux.json). Each contains the environment, fixture/policy/artifact hashes, operation counts, source snapshots, and every elapsed/allocation interval. The [runtime contract](m05-runtime-contract.md) specifies exact providers, failures, logical lifetime, permission/path assumptions, transitive foundations and source costs. This is engineering evidence; target-user time/usability measurements remain unmeasured.

## Target, invocation and freshness

Native invocation was literal `.venv/bin/python benchmarks/m05_effects.py --output Docs/evidence/m05-runtime-macos.json`, using CPython 3.13.1, standard GIL build, on macOS 26.6.2 arm64, Apple M1 Pro, MacBookPro18,1, 10 reported logical CPUs and 16 GiB physical memory. The interpreter reports Clang 16.0.0 and build date December 3, 2024. Its executable field retains `/Volumes/Projects/pyalamode/.venv/bin/python`.

Linux used `docker run --rm --network none -e PYTHONPATH=/workspace -v /Volumes/Projects/pyalamode:/workspace:ro -w /workspace python:3.13.1-slim python benchmarks/m05_effects.py --output -`, saving JSON stdout to the owned evidence file. It reports CPython 3.13.1 standard GIL build, `/usr/local/bin/python`, GCC 12.2.0, aarch64 LinuxKit 5.15.49/glibc 2.36, 5 visible CPUs and approximately 8.23 GB visible memory. Reported cgroup CPU/memory maxima were unrestricted; these are container-visible observations, not reserved execution resources.

Native then Linux measurement jobs ran separately. Other system activity, OS scheduling, temperature and filesystem caches were uncontrolled. No CPU affinity, isolation or statistical-confidence study was performed. The bundled measurement helper reads hardware metadata and handles the tracing interval; its own source digest is included.

Both files record identical full ten-file product SHA256 maps and four owned/support source maps before and after each run. They also match the current files and each other. The product map includes `__init__.py`, `effects.py`, `collections.py`, `records.py`, `boundaries.py`, `guardgen.py`, `model.py`, `checker.py`, `project.py`, and `cli.py`. The owned/support map includes the runtime, runtime tests, M5 harness and reused M3 measurement helper. Root independently reparsed and reconciled both JSON files with current source; no product/runtime/test/harness source changed during or after measurements.

The frozen M5 identities are:

| File | SHA256 |
| --- | --- |
| `pyalamode/effects.py` | `31d3ee92aaf256fe92f29fa221941d6fac41115fb6c87e4b31503639776a9dfa` |
| `tests/m05_runtime.py` | `543a0ce687072a8527887bc79e20ef4308797b38cfb7ddf7d0e95056fccd1a21` |
| `benchmarks/m05_effects.py` | `83b54c93ecc4240f340bcc88ba20b16f8a640306d49f784c26662cfe22bb22d3` |

## Workloads and interval scope

Each platform has 20 conditions: ten provider/operation conditions at workload sizes 100 and 1000. Each has three raw trials of 25 calls, giving 60 measured intervals and 1,500 measured checked function calls per platform. Each row also runs ten untimed warmup calls on separate provider state, for 200 warmup calls per platform. Factory setup, recorded fixture generation, build/check, import, warmup, GC collection, correctness checks and JSON/hardware reporting are outside measured intervals. A fresh state/recorded cursor/provider is supplied for each trial.

Every interval includes `tracemalloc` overhead and the Python loop/function-call cost. Current/peak counts are Python traced allocations, including the returned value retained at interval end, not process RSS or all OS/filesystem buffers. Imports are warm and no check-cache timing is measured. Live IO repeatedly replaces/reads one temporary file using both allowed operations; no directory creation occurs in an interval. Filesystem page/metadata caches are uncontrolled. The first recorded IO write creates its single entry, with subsequent writes replacing it in the same trial.

| Condition | Workload-size meaning and operations per call |
| --- | --- |
| State direct | Integer increment 100/1000; two gets and one set |
| State borrow | Same gets/set through one fresh depth-one logical borrow, including enter/exit |
| Clock recorded | Recorded pool length 100/1000; one cursor read, first 25 values used |
| Clock live | One live `time.time_ns` read; repeated rows have no size-varying clock parameter |
| Random recorded | Bound 100/1000 and recorded sample bound minus one; one cursor read |
| Random live | Bound 100/1000; one operation, variable OS entropy rejection draws |
| Environment recorded | 100/1000 recorded entries with the selected key last; one linear lookup |
| Environment live | One fixed task-owned environment name lookup; repeated rows have no size-varying live lookup parameter |
| IO recorded | 100/1000-byte exact ASCII text; one write and read of a single recorded path |
| IO live | Same text bytes and path; one UTF-8 whole-file write/open/close and read/open/close |

Final results satisfy exact recorded values, cumulative State updates, Environment text and IO roundtrip text. Live Clock/Random are checked against their exact result/range contracts and are not asserted to repeat identical observations. The task-owned live environment value is set before timing and restored afterward. Recorded providers retain their State/Clock/Random/Environment/IO classifications; successful repeated results do not establish purity.

## Observed costs

The table reports the median of three measured interval times divided by 25 calls, in microseconds per call. It describes these exact traced workloads. Rows are heterogeneous and are not a speedup comparison between live and recorded providers.

| Condition | macOS n=100 | macOS n=1000 | Linux n=100 | Linux n=1000 |
| --- | ---: | ---: | ---: | ---: |
| State direct | 5.617 | 5.377 | 6.540 | 7.372 |
| State borrow | 26.478 | 27.435 | 34.545 | 34.832 |
| Clock recorded | 2.208 | 2.677 | 2.348 | 3.023 |
| Clock live | 2.172 | 2.103 | 2.385 | 2.777 |
| Random recorded | 2.435 | 2.423 | 2.603 | 2.508 |
| Random live | 5.568 | 7.033 | 4.965 | 7.695 |
| Environment recorded | 28.592 | 264.678 | 33.660 | 293.818 |
| Environment live | 2.722 | 2.740 | 2.848 | 2.770 |
| IO recorded | 16.938 | 17.358 | 19.500 | 19.293 |
| IO live | 158.807 | 155.355 | 127.902 | 138.335 |

Maximum traced peaks across the three n=1000 trials are:

| Condition | macOS bytes | Linux bytes |
| --- | ---: | ---: |
| State direct | 384 | 384 |
| State borrow | 968 | 968 |
| Clock recorded | 320 | 320 |
| Clock live | 292 | 292 |
| Random recorded | 320 | 320 |
| Random live | 367 | 367 |
| Environment recorded | 456 | 456 |
| Environment live | 304 | 304 |
| IO recorded | 1064 | 1064 |
| IO live | 11162 | 9936 |

Recorded Environment lookup visits entries linearly, matching the published source bound. The depth-one borrow adds exact metadata/liveness checks and a new context/view/lease; this workload does not measure arbitrarily deep retained scopes. Recorded IO reuses exact immutable text and copies one-entry metadata, while live IO allocates decoded results and performs filesystem work. Small traced intervals, three trials and external OS/load variability limit generalization; no universal latency, throughput, memory, termination or comparative performance claim follows.

## Verification and handoff

Owned runtime tests pass 27/27 on native macOS (0.007 seconds) and actual Linux Docker (0.004 seconds). They cover identity/annotation behavior, exact foreign-hook rejection, all live/recorded interfaces, permission scopes, malformed metadata, mutation/subclass rejection, stable-data exclusion, finite forged lease-cycle rejection, nested/ancestor/exception exit and one-way closure. Actual opened builtin streams are observed closed after success, invalid UTF-8 reads and surrogate encoding failures. Random tests force one rejection before success, verify the entropy-free singleton, exercise large bounds and propagate entropy failure. Setup/context tests remain ordinary runtime probes rather than source evaluation by check/build.

Root independently ran the complete frozen 194-test product suite on native macOS (3.259 seconds) and Linux (10.087 seconds), inspected the actual artifact callback smoke and all 20 raw rows, and independently verified full source-map freshness across both platforms. Independent static/runtime/project conformance and final milestone status are recorded separately by the reviewer/main/root. This helper hands back the owned runtime/tests/harness, exact dependency/failure contract and raw measurements; it makes no broader completion or usability claim.
