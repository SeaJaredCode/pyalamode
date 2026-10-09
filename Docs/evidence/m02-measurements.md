# Milestone 2 measurements

The frozen M2 implementation passed five trials in each environment using
`benchmarks/m02_modules.py` and the named workload `branched_integer_rollup_v1`.
Each check selected 26 functional modules, published 208 checked function
contracts, and preserved 320 distinct direct cross-file checked call edges.
The generated application source was statically checked through `check_paths`;
it was never imported or executed.

Eight independent branches each contain three modules with eight functions per
module. Their shared foundation supplies eight checked functions and stable
scalar/tuple constants. An unrelated module supplies eight more functions.
The graph has 24 direct module import edges, a maximum checked call-chain length
of three edges, and at most two direct checked callees per function.

These are wall-time medians and median peak traced Python allocations. Hit/miss
counts were identical in all five trials on both platforms.

| Check state | macOS seconds | macOS peak bytes | Linux seconds | Linux peak bytes | File hits / misses |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cold | 0.676 | 3,339,628 | 0.880 | 3,289,102 | 0 / 26 |
| Warm, unchanged | 0.481 | 3,421,816 | 0.624 | 3,337,744 | 26 / 0 |
| Unrelated module edit | 0.484 | 3,460,563 | 0.628 | 3,380,014 | 25 / 1 |
| Branch leaf edit | 0.505 | 3,474,506 | 0.662 | 3,396,997 | 23 / 3 |

Every cold trial removed the complete analysis-cache directory. The warm check
followed immediately. Changing `unrelated.py`'s stable integer offset invalidated
only that file. Then changing the first function in
`branch_0000_level_0000.py` invalidated exactly branch 0's three-file import
closure; the unrelated edit remained present and its new evidence was reused.
Each invocation asserted the exact file hit/miss set, contract count, strict
success, and direct call graph. Checked contract counts include cached evidence;
the JSON also records contract counts in cache-miss files separately.

Both environments used standard, GIL-enabled CPython 3.13.1. The native host was
macOS 26.6.2 on an Apple M1 Pro, MacBookPro18,1, with 10 logical CPUs and 16 GiB
physical memory. Linux ran in the local ARM64 `python:3.13.1-slim` Docker image
with a read-only `/workspace` mount, `PYTHONPATH=/workspace`, and networking
disabled. The Linux guest reported five logical CPUs, 8,232,894,464 bytes of
physical memory, and Linux 5.15.49-linuxkit. Its exact image ID, repository
digest, and cgroup limits are saved in the Linux JSON.

The final platform runs were serialized on the same host; other system activity
was uncontrolled. Timing surrounds only `check_paths`, includes `tracemalloc`
overhead and disk-cache I/O, and excludes interpreter startup, checker imports,
fixture generation/edits, digest snapshots, result validation, and serialization.
Garbage collection ran before each interval. Cold refers to analysis-cache
state; the OS page cache was uncontrolled. Memory is Python allocation tracing
with the result retained, not RSS. Warm checks still read and fingerprint sources
and construct graph metadata. These results establish selective evidence reuse
for this bounded workload; they establish neither a universal latency target nor
application runtime performance.

The package source digest map was identical before and after each platform run,
matched the current frozen checkout, and matched across platforms. Both JSON
reports contain individual package/source/dependency digests, file fingerprints,
the complete normalized call graph, every trial, and unrounded summaries.
SHA-256 snapshots use sorted compact JSON for digest maps and call-edge lists:

| Snapshot | SHA-256 |
| --- | --- |
| Package source digest map | `43471d5bfd9674999e6365ff261d161d09572ebcb4fbfcc1ed7ee1582e061c0d` |
| Benchmark script bytes | `5d28d376907f3aa27810bf04a1d04b000fd26869568826e44b3e65d4765f790c` |
| Base workload source digest map | `eaac09a0d41cdd314be80663811638414a37a48fb6247e1613b3befc5cd6a727` |
| Unrelated edit source digest map | `7a8f4e659ac17ab39af189f937a5ba03993b89f5c1f17dcaed73d7e59372add5` |
| Leaf and unrelated edits source digest map | `348956df8b908102bc510bd8050c5951914b7860a103d6e5ff17e3754f8cbeef` |
| Direct checked call-edge list | `bd7835db9a1fe668c3c05236145105ab0e7fa65d8c80e3e39a479f25d8176f65` |

Raw evidence: [macOS](m02-benchmark-macos.json) and
[Linux](m02-benchmark-linux.json). Reproduce with the default five-trial workload:

```sh
.venv/bin/python benchmarks/m02_modules.py --output /tmp/m02-macos.json
docker run --rm --network none \
  --mount type=bind,src="$PWD",dst=/workspace,readonly \
  -e PYTHONPATH=/workspace -w /workspace python:3.13.1-slim \
  python benchmarks/m02_modules.py > /tmp/m02-linux.json
```
