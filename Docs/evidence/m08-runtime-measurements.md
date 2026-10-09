# M8 bounded integration support measurements

Status: completed on the corrected root-approved joint source freeze after heavy acceptance verification finished. Actual native macOS and networking-disabled Docker Linux runs completed sequentially, with all correctness and assertion-count gates passing. No product, test, example or harness source changed. Target-user usefulness, authoring time and approval-review effort are **UNMEASURED**.

The [runtime contract](m08-runtime-contract.md) and [main catalog](../milestones/08-integrations.md) publish the exact contracts before admission. [`benchmarks/m08_integrations.py`](../../benchmarks/m08_integrations.py) builds four individually checked functions in an ordinary module that imports the external adapters. Three temporary policies explicitly approve all three exact current operation/dependency identities for this root-authorized benchmark fixture only. This generates no production approval and bypasses no policy gate. Each build records full external assumptions, ordinary adapter-import setup with IO and explicitly unchecked surrounding initialization. Backend setup/import and approval preparation precede every measured invocation.

| Named workload | Exact work at payload size n |
| --- | --- |
| encode | One adapter Base64 encode, one fixed native binascii encode; input n exact bytes, output `4*ceil(n/3)` canonical bytes. |
| decode | One adapter canonical decode, one strict native decode and one native canonical re-encode/equality check; encoded input `4*ceil(n/3)` bytes, output n bytes. |
| digest | One fresh private `_sha2` HACL state, SHA256 constructor/update and one fixed 32-byte digest result; n input bytes. |
| transport_digest | One checked function encodes n bytes, canonically decodes that result and digests decoded bytes; two native Base64 encodes including canonical verification, one native decode and one private SHA256 state/digest; return an ordered exact `(encoded:bytes, digest:bytes)` tuple. |

Payloads contain the deterministic repeated byte sequence 0–255, truncated to 32 or 4,096 bytes. At these sizes canonical encodings have 44 or 5,464 bytes. No random input, text codec or general backend selection is involved. Empty data, noncanonical pad-bit refusal, fixed ValueError without native context/cause and guarded mutable-input refusal are separate untimed actual-artifact correctness gates.

Every original off/export fixture has byte-identical authored source. Debug artifacts contain only the separately selected generated assertions. Artifact imports occur normally after successful static build; check/build do not evaluate their application initialization. The selected export facade is checked to wrap the original function in the actual generated artifact, and each original function's code filename is checked against that artifact path. Reports retain the exact operation approvals, installed native/adapter/interpreter identities, policy and artifact hashes, guard coverage and invocation-versus-setup evidence.

Untimed instruments on the corrected frozen artifacts observed and independently enforce these deep-assertion API call counts for both payload sizes:

| Guard mode | encode | decode | digest | transport_digest |
| --- | ---: | ---: | ---: | ---: |
| off | 0 | 0 | 0 | 0 |
| selected exports | 2 | 2 | 2 | 2 |
| debug | 4 | 4 | 4 | 6 |

Counts name calls to the characterized data validator, not recursive payload nodes or native buffer checks. The actual measured conditions are counted untimed before intervals; all original/imported validator aliases are restored afterward. Optional assertions do not approve an external backend or monitor its identity. Exact runtime adapter validation remains ordinary library behavior in every mode.

The approved protocol has four workloads, two payload sizes and three modes: 24 rows per platform. Each row has ten untimed warmups and three separately traced intervals of 25 calls: 72 intervals, 1,800 measured calls and 240 warmups. Native macOS and actual Docker `python:3.13.1-slim` Linux run sequentially with networking disabled for the Docker process, using exact CPython 3.13.1 standard GIL UTF-8/surrogateescape targets. No interval starts before root's explicit joint product/test/example/harness source freeze.

Build, ordinary application/native-backend import, input creation, fixture approval generation, assertion instrumentation/counting, warmups, correctness checks, environment/source/dependency hashing and JSON writing are outside intervals. Actual adapter/backend invocation loops, optional assertions, transient disposal and tracemalloc overhead are inside. GC collection precedes each interval; only the last result is retained. Allocation is Python-traced peak/current memory rather than RSS, and native HACL allocations may not be represented in tracemalloc. Process/backends/imports are warm; no source-check-cache timing is included. OS caches, system load and scheduling remain uncontrolled. These observations establish no universal latency, security timing or speedup claim.

Raw packets record actual hardware/interpreter/filesystem provenance, each independently traced interval and correctness gate, actual assertion counts and exact generated artifacts. Complete before/after maps cover all sixteen current product foundations, all seventeen package Python files including the launcher and four owned runtime/test/harness/support inputs. Both actual native artifacts, adapter bytes, executable/core and their per-operation contract/dependency identities are included separately. Cross-platform product/test/harness source bytes must match current files; native backend binaries and installed paths intentionally differ by target and must each match the corresponding approved installed identity. Relevant source/dependency bytes must stay unchanged before/after every run. Every platform-local dependency snapshot was independently regenerated after its run; five unique native/adapter/interpreter files were rehashed and all artifact catalog/caller identities matched those current snapshots. No human validation has been performed.

## Frozen observed results

Each raw packet contains **24 rows, 72 independently traced intervals, 1,800 measured calls and 240 warmup calls**, exactly matching the approved protocol. All 24 condition/size/mode combinations are present once per target. The [native JSON](m08-runtime-macos.json) and [Linux JSON](m08-runtime-linux.json) retain every interval, environment, fixture/policy/artifact hash, operation approval, full external assumption, separate setup observation and complete source/dependency map. All three actual artifacts retain their checked calculation contracts and independently reported ordinary import setup. Empty, noncanonical and guarded mutable-input controls passed outside intervals.

Native used CPython 3.13.1/Clang 16.0.0 on Apple M1 Pro arm64, MacBookPro18,1, 10 logical CPUs and 17,179,869,184 bytes physical memory, macOS 26.6.2. Docker used CPython 3.13.1/GCC 12.2.0 on aarch64 Linux 5.15.49-linuxkit/glibc 2.36, five visible logical CPUs and 8,232,894,464 visible memory bytes, with networking disabled. The container exposed no CPU model string; CPU/memory cgroup maxima report max. Both are standard GIL builds. Native UTF-8 mode is 0 and Linux is 1; both use utf-8 filesystem encoding and surrogateescape errors. The targets have distinct installed native binaries and executable/core bytes.

Per-call medians below divide the median of three elapsed intervals by 25 calls. Peak bytes are the maximum traced peak among those three observations. These warm-process support costs do not establish a general speedup, cross-platform speed comparison, production latency or security timing guarantee.

| Mode | Workload | Input payload bytes | ms/call macOS / Linux | Peak traced bytes macOS / Linux | Generated assertions/call |
| --- | --- | ---: | ---: | ---: | ---: |
| off | encode | 32 | 0.000625 / 0.000570 | 218 / 218 | 0 |
| off | encode | 4096 | 0.006297 / 0.004093 | 13788 / 13788 | 0 |
| off | decode | 32 | 0.001002 / 0.001172 | 271 / 271 | 0 |
| off | decode | 4096 | 0.017737 / 0.012647 | 16549 / 16549 | 0 |
| off | digest | 32 | 0.000952 / 0.001073 | 242 / 242 | 0 |
| off | digest | 4096 | 0.013107 / 0.014230 | 242 / 242 | 0 |
| off | transport_digest | 32 | 0.002482 / 0.002655 | 573 / 573 | 0 |
| off | transport_digest | 4096 | 0.036557 / 0.030443 | 23591 / 23591 | 0 |
| exports | encode | 32 | 0.005923 / 0.007043 | 730 / 730 | 2 |
| exports | encode | 4096 | 0.011650 / 0.010447 | 13836 / 13836 | 2 |
| exports | decode | 32 | 0.006405 / 0.007485 | 706 / 706 | 2 |
| exports | decode | 4096 | 0.022668 / 0.018930 | 16597 / 16597 | 2 |
| exports | digest | 32 | 0.006317 / 0.007435 | 706 / 706 | 2 |
| exports | digest | 4096 | 0.018502 / 0.020652 | 706 / 706 | 2 |
| exports | transport_digest | 32 | 0.026433 / 0.033177 | 1664 / 1612 | 2 |
| exports | transport_digest | 4096 | 0.060892 / 0.061128 | 23695 / 23695 | 2 |
| debug | encode | 32 | 0.011142 / 0.013690 | 730 / 730 | 4 |
| debug | encode | 4096 | 0.016918 / 0.017108 | 13836 / 13836 | 4 |
| debug | decode | 32 | 0.011582 / 0.014272 | 706 / 706 | 4 |
| debug | decode | 4096 | 0.028017 / 0.025778 | 16597 / 16597 | 4 |
| debug | digest | 32 | 0.011587 / 0.014223 | 706 / 706 | 4 |
| debug | digest | 4096 | 0.023760 / 0.027388 | 706 / 706 | 4 |
| debug | transport_digest | 32 | 0.054275 / 0.069412 | 1702 / 1650 | 6 |
| debug | transport_digest | 4096 | 0.088550 / 0.098662 | 23695 / 23695 | 6 |

The exact generated-assertion counts were instrumented untimed for both sizes, then every validator alias was restored before intervals. Off executes zero generated assertions; selected exports executes two; debug executes four for encode/decode/digest and six for the combined checked tuple result. Adapter exact-type/size checks, canonical re-encode verification and native validation remain present with guards off and are separate from those counts.

Root independently passed the final complete 320-method suites native in 15.369 seconds and Linux in 50.641 seconds. The reviewer passed fresh-installed complete suites native in 14.168 seconds and Linux in 33.891 seconds, plus 18 focused verification groups, 708 fixed literal source/policy cases and 57 runtime inputs/unsafe artifact gates per target. The twelve owned runtime methods are included in those suites: they cover every single-byte canonical Base64/pad-bit family, exact size bounds, native Error constructor and compatible-base effects, no foreign hooks before rejection, prior output isolation, actual native known answers and registered strict/surrogateescape zero-call controls. Suite elapsed times are verification observations, not these workload timings. [Independent conformance evidence](../conformance/m08-cases.md).

## Complete current source identity maps

Every entry below is equal before/after each platform run, equal across platforms and independently rehashed against current files. Root's corrected 37-input freeze packet SHA-256 is `18fc42d5f4d76160a1a74edf39882f044024847888ef2774d85cc77daa566712`. Product foundations include the static-only integration_contracts.py and ordinary-only integrations.py; the full package map also includes the launcher. No code/test/example/harness source was changed during or after these measurements.

### Product foundations (16)

| Source | SHA-256 |
| --- | --- |
| `__init__.py` | `c695ea8253ae3fa75e978d5b1d68e2f7a0a54ab41323849e096fffa5998a6bab` |
| `boundaries.py` | `cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc` |
| `checker.py` | `65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5` |
| `cli.py` | `a72e1c2d17a68c94060bd06e3b16225894ec1a35bca8d88b89f63ff7e749f744` |
| `collections.py` | `eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783` |
| `effects.py` | `1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d` |
| `failures.py` | `221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be` |
| `guardgen.py` | `c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4` |
| `integration_contracts.py` | `f9f2d0d0e77f8505c8839f561212b76d9f4e757f2edde89687ded9030b614567` |
| `integrations.py` | `3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e` |
| `model.py` | `3c13736b6230365ac5a4ad36ab3e639ef24c1e74b65e6163cf5dcae1556b7513` |
| `project.py` | `ee8b098b29fdf0f3fc414b275a5f9b1faf4ef6d09cf07015be9eb1f1cd3a1b81` |
| `records.py` | `c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560` |
| `standard.py` | `b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9` |
| `standard_contracts.py` | `cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a` |
| `variants.py` | `02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d` |

### Full package Python sources (17)

| Source | SHA-256 |
| --- | --- |
| `pyalamode/__init__.py` | `c695ea8253ae3fa75e978d5b1d68e2f7a0a54ab41323849e096fffa5998a6bab` |
| `pyalamode/__main__.py` | `935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d` |
| `pyalamode/boundaries.py` | `cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc` |
| `pyalamode/checker.py` | `65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5` |
| `pyalamode/cli.py` | `a72e1c2d17a68c94060bd06e3b16225894ec1a35bca8d88b89f63ff7e749f744` |
| `pyalamode/collections.py` | `eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783` |
| `pyalamode/effects.py` | `1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d` |
| `pyalamode/failures.py` | `221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be` |
| `pyalamode/guardgen.py` | `c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4` |
| `pyalamode/integration_contracts.py` | `f9f2d0d0e77f8505c8839f561212b76d9f4e757f2edde89687ded9030b614567` |
| `pyalamode/integrations.py` | `3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e` |
| `pyalamode/model.py` | `3c13736b6230365ac5a4ad36ab3e639ef24c1e74b65e6163cf5dcae1556b7513` |
| `pyalamode/project.py` | `ee8b098b29fdf0f3fc414b275a5f9b1faf4ef6d09cf07015be9eb1f1cd3a1b81` |
| `pyalamode/records.py` | `c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560` |
| `pyalamode/standard.py` | `b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9` |
| `pyalamode/standard_contracts.py` | `cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a` |
| `pyalamode/variants.py` | `02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d` |

### Owned and shared measurement inputs (4)

| Source | SHA-256 |
| --- | --- |
| `benchmarks/m03_collections.py` | `f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141` |
| `benchmarks/m08_integrations.py` | `e5189e5b6b50af43bcca10714549214afe5bdc47704d42775e15df7fe6b497dd` |
| `pyalamode/integrations.py` | `3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e` |
| `tests/m08_runtime.py` | `38ad79083ff06804f5cd6ba39c6ac4fe708c3cccc799422946df42789a871b1c` |

### Platform-local installed dependency identities

Each operation includes the shared adapter plus both native extensions, interpreter core/executable, canonical base prefix, ABI flags, native extension suffix inventory, exact CPython build/version/platform/cache tag and invoked backend. All three complete identities were regenerated after each run and every unique referenced file rehashed on that target. Every built artifact catalog and caller assumption matched these identities. Paths and binary bytes intentionally differ across targets, so fixture approvals are platform-local. Native loader/libc or libSystem and binascii-linked zlib remain separately disclosed setup trust; hashing these files does not prove backend purity.

| Operation | Effective contract SHA-256 | Dependency SHA-256 macOS / Linux |
| --- | --- | --- |
| `pyalamode.integrations.base64_decode` | `61f5fa1bf491475c9d242d6cd7a14f90f98aabd5ae71f17bc18fbc7d27695585` | `dd8062d7174d2f557651b998fe5121d344ca3d1d92f5cddf8d8abc3f6684ea37` / `5b440d6d7ebdefe854da3dd35f7db6f6abdffb246e43d3739e20c68d71d8c8f6` |
| `pyalamode.integrations.base64_encode` | `10ae6750641e50bc12334ca52eaf1c6ff9328b477e06cace8993f94ce7dc1d60` | `ed3e4d190077f0955f25fd7f0d7ae0a34e1e8131b1a620a00626c5db47b43d0b` / `16315c0a418d8709c99bba54c81c3c5ae64582ae124506dfbc6ae12a2e11a949` |
| `pyalamode.integrations.sha256_digest` | `58b9b3376483918e16f5078332d5de4fc7fd4b6053173a0d9de960bb4548ec6c` | `3497e592446052a8e3561b38bd793b9f697995c239d2a4dc605c99353496d243` / `a54b3eb4beba11fd2c7db17a5881a2cd45332b2c1b5e437ea4e8a7c78d630033` |

### Actual macos installed file bytes (5)

| Artifact | Actual resolved path | SHA-256 |
| --- | --- | --- |
| adapter | `/Volumes/Projects/pyalamode/pyalamode/integrations.py` | `3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e` |
| interpreter core | `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Python` | `424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d` |
| interpreter executable | `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/bin/python3.13` | `d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132` |
| _sha2 | `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/_sha2.cpython-313-darwin.so` | `b6bfcfe427f23d6705e084795ce320e9cf7c59c5df26250e7430a31b5c12ba62` |
| binascii | `/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/binascii.cpython-313-darwin.so` | `428c1263cf9326aae8e9913b9898852ce1ca0f5f3736148638af01eeb0ebaaca` |

### Actual linux installed file bytes (5)

| Artifact | Actual resolved path | SHA-256 |
| --- | --- | --- |
| adapter | `/workspace/pyalamode/integrations.py` | `3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e` |
| interpreter core | `/usr/local/lib/libpython3.13.so.1.0` | `654a735558be10deedd50bc06bded72d1de1f217fb25296c8ba66df7f45a918f` |
| interpreter executable | `/usr/local/bin/python3.13` | `44a9ce6ed83ab1809449925790d0583e38f17b3ccd1671d9f55e15b576cb4f20` |
| _sha2 | `/usr/local/lib/python3.13/lib-dynload/_sha2.cpython-313-aarch64-linux-gnu.so` | `8fc33c42e000fa6063b560e3d86d9889e5b48298690c80428624a44298bcfec3` |
| binascii | `/usr/local/lib/python3.13/lib-dynload/binascii.cpython-313-aarch64-linux-gnu.so` | `e86dd0645c3cec4bab67bbd9d2e0e44dc029d6501c3d71734743c4ccc5137680` |

### Raw packet identities

| Packet | SHA-256 |
| --- | --- |
| `Docs/evidence/m08-runtime-macos.json` | `c33abdcd12a9771e41410c09497e9eb58a28bb00c8d9d68352ca23bc89374ea5` |
| `Docs/evidence/m08-runtime-linux.json` | `066587849daee869c75507fa7a9ca5755343cdda148e0ead5d1385ea8317a329` |

Root independently reconciled the raw summaries and source/dependency maps. The reviewer completed 842 explicit reconciliation checks, including all raw row/interval/call/warmup counts, actual validator counts, interval summaries, catalog/caller/approval identities, separate setup, complete source maps and native/core/executable bytes against independent installed conformance. [Independent final review](../conformance/m08-cases.md).

All runtime/test/harness sources remain frozen. Named support costs and artifact correctness are observed engineering evidence; target-user completion, errors, authoring time, approval-review effort and usefulness remain unperformed and **UNMEASURED**. Root owns final acceptance and Git.
