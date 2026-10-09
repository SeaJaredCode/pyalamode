# M6 frozen runtime measurements

Status: completed on the corrected root-approved source freeze. Both platforms were rerun sequentially after the family-dependency writer correction; the raw observations and source identities below are the current repeated trials.

Actual sequential native macOS and Docker Linux runs completed on the root-approved frozen product/test/example/harness snapshot. Each platform recorded **36 conditions, 108 intervals, 2,700 measured calls and 360 warmup calls**. All value/tag/order/retained-input assertions and the separate Effectful capability/failure smoke passed. These are named engineering measurements; human authoring benefit and general application speed remain unmeasured.

The actual 12-product-file and eight owned-source SHA maps are unchanged before/after each platform run, equal across platforms, and independently compared with current files. The raw observations are [macOS JSON](m06-runtime-macos.json) and [Linux JSON](m06-runtime-linux.json). No product, test or harness source changed after the freeze.

## Artifact and workload gates

[`benchmarks/m06_domains.py`](../../benchmarks/m06_domains.py) builds three real project artifacts from the same source text, with off, selected exports and debug policies. The off and exports originals retain identical authored bytes; debug copies contain the disclosed ordinary data assertions. Each artifact is imported normally from its output directory. Original function code paths refer to the built files, and generated export facades retain the originals in __wrapped__. Source check/build never imports these application fixtures. Actual execution occurs afterward in this measurement harness.

The authored fixture SHA is `bdf80f70efb10acc2739aaf19579f431e94a28fb2639116d6dafa8311477844a`. Artifact/policy hashes are recorded separately in both raw files; generated authored-path strings make some facade/debug bytes differ between platform temporary directories. A fourth actual off artifact passes an exact `Effectful[[ClockCapability], Result[int,Failure], Clock]` target through a logical borrow: a recorded timestamp returns Ok(7), and an empty recorded provider returns Err(Failure(IndexError,...)). It performs Clock regardless of successful conversion. This smoke is untimed and has no capability guard.

All three distinct source modules are preloaded before any timed interval, fixing catalog counts at **10 exact cases, three domains and one Failure record** across every mode. Import unloading does not remove data catalogs; the harness does not reset or forge product metadata. Untimed validator instrumentation counts actual deep assertions, then restores the validator and every imported alias before timing.

| Named condition | Exact work per call at workload size n | Off / exports / debug deep assertions |
| --- | --- | ---: |
| domain_construct | Construct fresh Batch.Ready over a preexisting Vector of n exact (int,bool) tuples and an int tag; validate complete payload | 0 / 3 / 6 |
| domain_match | Native full-case match over Batch.Ready carrying that Vector, return n | 0 / 2 / 4 |
| option_match | Native Some/Nothing match over Some carrying that Vector, return n | 0 / 2 / 4 |
| result_success | Compute len(payload)//1, return fresh Ok referencing the same deeply validated Vector | 0 / 3 / 7 |
| result_failure | Compute len(payload)//0, catch the actual ZeroDivisionError and copy its exact category into fresh immutable Failure/Err | 0 / 3 / 7 |
| validation_errors | Binary accumulate of two independently computed Err values, each carrying a distinct n-tuple Vector; retain both exact payload references in left-to-right Vector order | 0 / 3 / 6 |

Each mode/condition runs n=10 and n=100. Each row has ten untimed warmup calls followed by three independently traced intervals of 25 calls. Inputs/cases/providers are prepared outside intervals. The measured loop retains only its last result; disposal of earlier transient results is included. Validation retains both inputs without mutation and does not invoke callbacks or flatten errors.

## Scope and observed costs

Timing includes ordinary calls/loop, native match/arithmetic/exception behavior, library constructor/deep validation/allocation, selected generated assertions, perf_counter and tracemalloc overhead. GC collection precedes each interval. Build/import, fixture preparation, catalog setup, counter instrumentation, warmups, correctness probes, source/environment hashing and JSON writing are excluded. Memory is Python-traced allocation, not RSS; existing inputs/case bases preexist tracing. Imports are warm in one process. Source-check-cache startup/cold/warm/edit timings are not measured here. OS caches, system load and scheduling remain uncontrolled; runs are sequential between platforms, with no isolation from other host work. The shared environment/measure helper imports benchmark-only modules during setup; none is product invocation evidence.

At n=100, median milliseconds per call and maximum traced peaks are:

| Mode | Condition | ms/call macOS / Linux | peak bytes macOS / Linux |
| --- | --- | ---: | ---: |
| off | domain_construct | 1.930142 / 2.388532 | 4282 / 4282 |
| off | domain_match | 0.000745 / 0.000840 | 416 / 416 |
| off | option_match | 0.000668 / 0.000788 | 416 / 416 |
| off | result_success | 1.267657 / 1.493072 | 3772 / 3772 |
| off | result_failure | 0.079508 / 0.094965 | 4130 / 4130 |
| off | validation_errors | 7.538828 / 9.288220 | 5576 / 5576 |
| exports | domain_construct | 5.811983 / 7.115247 | 4713 / 4557 |
| exports | domain_match | 1.935213 / 2.392148 | 3175 / 3019 |
| exports | option_match | 1.902035 / 2.370465 | 3033 / 2877 |
| exports | result_success | 4.799720 / 6.207038 | 4520 / 4364 |
| exports | result_failure | 1.884397 / 2.492890 | 4474 / 4474 |
| exports | validation_errors | 14.182192 / 19.369765 | 6644 / 6436 |
| debug | domain_construct | 8.929672 / 12.143430 | 4695 / 4539 |
| debug | domain_match | 3.615677 / 5.044703 | 3157 / 3001 |
| debug | option_match | 3.841373 / 4.864690 | 3015 / 2859 |
| debug | result_success | 8.323897 / 11.386413 | 4502 / 4346 |
| debug | result_failure | 3.746490 / 5.216888 | 4668 / 4564 |
| debug | validation_errors | 21.399738 / 28.414288 | 6620 / 6412 |

Off native matching returns an exact int from existing data without deep revalidation, so those tiny intervals describe only the narrow dispatch fixture. Constructors still perform their ordinary library invariant validation when guards are off. The failure path does not traverse its Vector payload in off mode; selected argument guards traverse it in exports/debug. Error accumulation validates input/output error payloads repeatedly. These distinct workloads cannot establish a general speedup ratio. Optional debug assertions substantially increase recursive work, as their counted paths show.

macOS used CPython 3.13.1 standard GIL/Clang 16 on Apple M1 Pro MacBookPro18,1, arm64 macOS 26.6.2, ten logical CPUs and 16 GiB physical RAM. Linux used actual python:3.13.1-slim, CPython 3.13.1 standard GIL/GCC 12.2, aarch64 LinuxKit 5.15.49/glibc 2.36, five visible logical CPUs and 8,232,894,464 visible memory bytes; cgroup CPU/memory files reported 'max', with no finite maximum. CPU model text was unavailable inside the container, rather than inferred. Each JSON retains the literal executable, interpreter build and full platform details.

The [runtime contract](m06-runtime-contract.md) supplies source complexity, alias/dependency/initialization/failure and licensing limits. The exact slot/tuple backend adds no installed dependency or new license obligation. Frozen focused runtime tests passed **30/30** with actual native .venv/bin/python (0.003 seconds) and Docker Linux (0.007 seconds). Root owns the full-suite, independent review, CLI and release gates; these focused measurements do not replace them.

## Reproduction and source identities

```sh
.venv/bin/python benchmarks/m06_domains.py --sizes 10 100 --trials 3 --calls 25 --output Docs/evidence/m06-runtime-macos.json
docker run --rm --network none -v /Volumes/Projects/pyalamode:/workspace:ro -w /workspace -e PYTHONPATH=/workspace python:3.13.1-slim python benchmarks/m06_domains.py --sizes 10 100 --trials 3 --calls 25 --output - > Docs/evidence/m06-runtime-linux.json
.venv/bin/python -m unittest discover -s tests -p 'm06_runtime.py'
docker run --rm --network none -v /Volumes/Projects/pyalamode:/workspace:ro -w /workspace -e PYTHONPATH=/workspace python:3.13.1-slim python -m unittest discover -s tests -p 'm06_runtime.py'
```

The full foundation map contains twelve runtime/checker/CLI product files; the small __main__.py launcher is excluded from that map, so it is not a count of every installed package file. Eight owned sources cover five of those product files plus the runtime tests, M6 harness and shared measurement helper. Complete current/cross-platform identities are:

| Product foundation | SHA-256 |
| --- | --- |
| __init__.py | `073ee6f161b19df7bcf2dcdf148e45dec7872649f84e85e7d1c9508bc71b6cf6` |
| boundaries.py | `cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc` |
| checker.py | `f524a5db7c97bd0df889b709b5cc6101576cd10b9f8092fb68dada1aadfcd0f0` |
| cli.py | `315af58cde488384815bdb8968393c33eec5b0bc93917237c55dc103726d5ee5` |
| collections.py | `eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783` |
| effects.py | `31d3ee92aaf256fe92f29fa221941d6fac41115fb6c87e4b31503639776a9dfa` |
| failures.py | `221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be` |
| guardgen.py | `c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4` |
| model.py | `ea09503e2203feedc26e0efd4b602c3a4887d5e3bae1976e9ff70f56e342c90c` |
| project.py | `a9a35d1358fd3f4532222dc2c977ba0da07d7f444a6e1a70079dc8ab704d62d4` |
| records.py | `c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560` |
| variants.py | `02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d` |

| Owned source | SHA-256 |
| --- | --- |
| benchmarks/m03_collections.py | `f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141` |
| benchmarks/m06_domains.py | `7a192a8cfed4b29c22d990414d03a49ed6c525c428a2874684368d393d7275af` |
| pyalamode/boundaries.py | `cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc` |
| pyalamode/collections.py | `eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783` |
| pyalamode/failures.py | `221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be` |
| pyalamode/records.py | `c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560` |
| pyalamode/variants.py | `02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d` |
| tests/m06_runtime.py | `9f035ba5d1969839abd1452ebe38d09a400db3a35536bfb4dcf80d62ac7c59da` |
