# M7 frozen standard runtime measurements

Status: completed on the corrected root-approved joint source freeze. Actual native macOS and Docker Linux runs completed sequentially with no product, test or harness edits. Both platforms passed every workload and separate effect/setup smoke. Human usefulness, authoring time and general application speed remain UNMEASURED.

Each platform recorded **36 rows, 108 independently traced intervals, 2,700 measured calls and 360 warmup calls**: six named paths at n=10/100, three guard modes, three trials of 25 calls and ten warmups per row. Actual 14-foundation, all-15-package-file (including launcher), and five owned-input maps are unchanged before/after, equal across platforms and independently rehashed against current files. The raw [native JSON](m07-runtime-macos.json) and [Linux JSON](m07-runtime-linux.json) retain every observation, environment, authored fixture/policy/artifact identity, actual guard count and source map.

The [runtime contract](m07-runtime-contract.md) and [main catalog](../milestones/07-standard.md) publish exact behavior/dependencies. [`benchmarks/m07_standard.py`](../../benchmarks/m07_standard.py) builds actual ordinary artifacts. Off and exports original source bytes are unchanged; debug copies contain the selected generated data assertions. Each original function code filename points at its built file, and export facades retain their originals through __wrapped__. Checking/building never imports the application fixtures; ordinary imports/execution occur afterward. Generated temporary absolute paths make some facade/debug/smoke artifact hashes differ between platforms; those identities are separately recorded.

## Actual named work

| Named workload | Exact work at size n |
| --- | --- |
| text_decimal | n semicolon-separated ASCII integer items; native replace/split, two eager Vector maps for bounded parse and clamp/format, then ordered join |
| encoding_roundtrip | n Unicode code points containing two/four-byte code points, CR/LF and BOM; manual UTF-8 encode, hex encode/decode and manual UTF-8 decode |
| scan | n ordered integers, n binary addition callbacks and n+1 accumulator outputs including initial zero |
| grouping | n ordered integers grouped by modulo seven; n callbacks, min(n,7) first-seen groups, original within-group order and retained immutable references |
| composition | one binary partial with stable bound two and one unary composition constructed per call; eager map invokes inner/outer n times each with intermediate/final validation |
| traversal_first_error | n ordered inputs, first negative at index floor(n/2); floor(n/2)+1 callbacks, first Err returned, later callbacks skipped, earlier successful values discarded |

Traversal success and empty inputs are separate correctness gates. An additional untimed off artifact declares IO/Clock/Environment functions alongside ordinary rooted/recorded provider initialization and a pure export. Execution passed CRLF/BOM/non-BMP roundtrip, malformed read/surrogate-write failures, zero registered strict/surrogateescape callback calls, surrogate OS-name refusal, every acquired stream closed, encoding-failure truncation, explicit permission denial, recorded timestamp 7/configuration test and pure text behavior. Actual static evidence records three ordinary provider setup calls and explicitly unchecked surrounding initialization. Supported startup provenance is filesystem encoding utf-8 and errors surrogateescape. This supplies setup/invocation evidence without certifying surrounding ordinary initialization.

## Measurement scope and observed costs

All three distinct modules preload before intervals, keeping the inherited catalog fixed at four cases, zero registered user domains and one Failure record. The builtin Option/Result family schemas are fixed separately from the user-domain catalog. Inputs, build/import, guard instrumentation, warmups, correctness, source/environment hashing and JSON writing are excluded. Invocation loops, native/library/generated assertions, transient disposal and perf_counter/tracemalloc overhead are included. GC collection precedes each interval. Only the last interval result is retained; memory is Python-traced allocation rather than RSS, and preexisting inputs/catalogs/earlier interval results predate tracing. No allocation-retention claim follows from these peaks. Process/import state is warm; source-check-cache timings are not measured. OS caches, scheduling and load are uncontrolled, and independent review activity may overlap.

Native used CPython 3.13.1/Clang 16.0.0 on Apple M1 Pro arm64, MacBookPro18,1, 10 logical CPUs and 17,179,869,184 bytes physical memory, macOS 26.6.2. Docker used CPython 3.13.1/GCC 12.2.0 on aarch64 Linux 5.15.49-linuxkit/glibc 2.36, five visible logical CPUs and 8,232,894,464 bytes visible memory, with network disabled. The container did not expose a CPU model string; memory/cpu cgroup maxima report max. Both are standard GIL builds. Native UTF-8 mode is 0 and Linux is 1; both report utf-8 filesystem encoding/surrogateescape errors. Exact interpreter/build/executable fields are in raw JSON.

Per-call medians below divide each row median elapsed interval by its 25 calls. Peaks are the maximum traced bytes among the three row observations. Distinct operation paths and optional repeated assertions do not establish a general speedup, cross-platform speed comparison or application latency promise.

| Mode | Workload | n | ms/call macOS / Linux | peak traced bytes macOS / Linux | Generated assertions/call |
| --- | --- | ---: | ---: | ---: | ---: |
| off | text_decimal | 10 | 0.098697 / 0.131222 | 1817 / 1817 | 0 |
| off | text_decimal | 100 | 0.883092 / 1.222700 | 12258 / 12258 | 0 |
| off | encoding_roundtrip | 10 | 0.041048 / 0.057132 | 959 / 959 | 0 |
| off | encoding_roundtrip | 100 | 0.349640 / 0.498912 | 4845 / 4845 | 0 |
| off | scan | 10 | 0.050457 / 0.070943 | 1458 / 1458 | 0 |
| off | scan | 100 | 0.427622 / 0.610913 | 7856 / 7856 | 0 |
| off | grouping | 10 | 0.067878 / 0.094007 | 6352 / 6352 | 0 |
| off | grouping | 100 | 0.473443 / 0.682793 | 8464 / 8464 | 0 |
| off | composition | 10 | 0.054548 / 0.076558 | 1918 / 1918 | 0 |
| off | composition | 100 | 0.500613 / 0.720398 | 3504 / 3504 | 0 |
| off | traversal_first_error | 10 | 0.261082 / 0.370898 | 9099 / 9099 | 0 |
| off | traversal_first_error | 100 | 2.171735 / 3.047198 | 63451 / 63451 | 0 |
| exports | text_decimal | 10 | 0.098978 / 0.136100 | 1817 / 1817 | 2 |
| exports | text_decimal | 100 | 0.891863 / 1.258695 | 12258 / 12258 | 2 |
| exports | encoding_roundtrip | 10 | 0.046205 / 0.062983 | 960 / 960 | 2 |
| exports | encoding_roundtrip | 100 | 0.354888 / 0.499805 | 4845 / 4845 | 2 |
| exports | scan | 10 | 0.187267 / 0.278355 | 1897 / 1845 | 2 |
| exports | scan | 100 | 1.571400 / 2.357542 | 8266 / 8214 | 2 |
| exports | grouping | 10 | 0.329330 / 0.492785 | 9919 / 9815 | 2 |
| exports | grouping | 100 | 1.745097 / 2.510512 | 11360 / 11256 | 2 |
| exports | composition | 10 | 0.185923 / 0.268158 | 2102 / 2102 | 2 |
| exports | composition | 100 | 1.707807 / 2.417898 | 3688 / 3688 | 2 |
| exports | traversal_first_error | 10 | 0.370245 / 0.503812 | 9312 / 9275 | 2 |
| exports | traversal_first_error | 100 | 2.917005 / 3.956003 | 63627 / 63627 | 2 |
| debug | text_decimal | 10 | 0.430213 / 0.574825 | 2205 / 2153 | 48 |
| debug | text_decimal | 100 | 3.626733 / 5.187838 | 12646 / 12594 | 408 |
| debug | encoding_roundtrip | 10 | 0.051713 / 0.072110 | 960 / 960 | 4 |
| debug | encoding_roundtrip | 100 | 0.360865 / 0.495212 | 4845 / 4845 | 4 |
| debug | scan | 10 | 0.404858 / 0.576955 | 1891 / 1839 | 34 |
| debug | scan | 100 | 3.467587 / 4.962898 | 8260 / 8208 | 304 |
| debug | grouping | 10 | 0.642073 / 0.929868 | 12307 / 12203 | 24 |
| debug | grouping | 100 | 3.509993 / 5.082897 | 13748 / 13644 | 204 |
| debug | composition | 10 | 0.451765 / 0.665505 | 2452 / 2400 | 54 |
| debug | composition | 100 | 4.106565 / 5.871810 | 3893 / 3841 | 504 |
| debug | traversal_first_error | 10 | 0.580420 / 0.836318 | 9447 / 9395 | 16 |
| debug | traversal_first_error | 100 | 4.545583 / 6.568802 | 63799 / 63747 | 106 |

Generated assertions were counted untimed at each exact condition/size, then the validator and every imported alias were restored before timing. Off has zero generated assertions and exports two throughout. Debug counts at n=10/100 are text 48/408, encoding 4/4, scan 34/304, grouping 24/204, composition 54/504 and traversal 16/106. Callback data assertions account for size-dependent debug counts. Ordinary library constructor/intermediate/result validation remains present with guards off and is not counted as a generated assertion.

Root independently observed the final 286-test suite passing native in 6.350 seconds and Linux in 20.501 seconds, plus 26 actual installed CLI/artifact/negative-build/setup/effect/explanation gates. The unchanged runtime unit contributes 25 meaningful tests, including the full 65,536 two-byte UTF-8 universe, longer constraints/surrogate spans, 4096-digit native-limit independence, exact foreign refusals, retained data, callback/first-error order, OS-name sentinels and alternate ASCII Linux startup. Suite elapsed times are verification observations, not workload benchmarks.

## Complete current source identity maps

All entries below were identical before/after each platform, across platforms and current bytes. Product foundations include the static-only standard_contracts.py catalog; the independent full package map additionally includes __main__.py. Owned inputs overlap package entries where noted and separately include runtime tests/harness/shared measurement helper. The corrected frozen checker SHA is `2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd`.

### Product foundations (14)

| Source | SHA-256 |
| --- | --- |
| `__init__.py` | `477ccce4a90dab58f949e8b1f0dc0ca1c59bc7d257114c520fcb2f7c2a1d8ab2` |
| `boundaries.py` | `cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc` |
| `checker.py` | `2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd` |
| `cli.py` | `688d5d299094c50e292efa7dc0729735d45a58f91e3dd4881ef2873a7e2c54f4` |
| `collections.py` | `eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783` |
| `effects.py` | `1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d` |
| `failures.py` | `221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be` |
| `guardgen.py` | `c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4` |
| `model.py` | `269edb7fa4e716ad15634a362cca688f649b253337ed1d59487fc0d18724ab7a` |
| `project.py` | `d8fc1d3768c67d7408a9fc3d9765ab1b98c643f6c16239496db197e0c4a21be1` |
| `records.py` | `c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560` |
| `standard.py` | `b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9` |
| `standard_contracts.py` | `cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a` |
| `variants.py` | `02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d` |

### Full package Python sources (15)

| Source | SHA-256 |
| --- | --- |
| `pyalamode/__init__.py` | `477ccce4a90dab58f949e8b1f0dc0ca1c59bc7d257114c520fcb2f7c2a1d8ab2` |
| `pyalamode/__main__.py` | `935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d` |
| `pyalamode/boundaries.py` | `cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc` |
| `pyalamode/checker.py` | `2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd` |
| `pyalamode/cli.py` | `688d5d299094c50e292efa7dc0729735d45a58f91e3dd4881ef2873a7e2c54f4` |
| `pyalamode/collections.py` | `eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783` |
| `pyalamode/effects.py` | `1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d` |
| `pyalamode/failures.py` | `221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be` |
| `pyalamode/guardgen.py` | `c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4` |
| `pyalamode/model.py` | `269edb7fa4e716ad15634a362cca688f649b253337ed1d59487fc0d18724ab7a` |
| `pyalamode/project.py` | `d8fc1d3768c67d7408a9fc3d9765ab1b98c643f6c16239496db197e0c4a21be1` |
| `pyalamode/records.py` | `c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560` |
| `pyalamode/standard.py` | `b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9` |
| `pyalamode/standard_contracts.py` | `cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a` |
| `pyalamode/variants.py` | `02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d` |

### Owned measurement inputs (5)

| Source | SHA-256 |
| --- | --- |
| `benchmarks/m03_collections.py` | `f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141` |
| `benchmarks/m07_standard.py` | `a5386cbd9e38000b3d00912073429288405a614405b5f50e2ea971218c41ad86` |
| `pyalamode/effects.py` | `1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d` |
| `pyalamode/standard.py` | `b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9` |
| `tests/m07_runtime.py` | `75d1a0ccffbf1f109190596ec881efb8e213643f641caf6fb3b5ec04c4bf5133` |

### Raw result identities

| Packet | SHA-256 |
| --- | --- |
| `Docs/evidence/m07-runtime-macos.json` | `d213178c571f99d4db77bcb68e70328f1a3a8c1ff062283b5a8a231b56c8d02c` |
| `Docs/evidence/m07-runtime-linux.json` | `542fd0c6c82becff4aefdeab99405d9407a1c8d14c99978c628da584d3fa20f8` |

No product/test/harness source changed after freeze. Named support costs and all correctness/source-identity gates are measured engineering evidence; target-user completion, errors, authoring time and usefulness remain unperformed and UNMEASURED. Root owns final acceptance and Git.
