# Milestone 5: checked effectful shell conformance

Status: independent final frozen two-platform review complete; no remaining blocker observed in this bounded corpus. Authority: `SPEC-sol6.1-composite.md` §§3–5, 8–12, 14 and 16–18, especially §11 and A17–A18. Prerequisites: milestones 1–4 at `7c201ab`, with the M4 contract in [04-records.md](../milestones/04-records.md). The initial reference target is actual CPython 3.13.1 standard GIL on macOS and actual Linux `python:3.13.1-slim`.

This reviewer owns only this document. Product source, product tests, examples, runtime evidence, milestone handoff, orchestration ledger and Git operations belong to their assigned workers/root. No later milestone, schedule, CatWrangler workflow or delegation is part of this review.

The checked claim remains conditional on exact inputs, actual callable evidence, stable dependencies and the published resource ownership/lifetime preconditions. Static checking/building must not evaluate application modules, decorators, defaults, annotations or providers. An effect name authorizes only a characterized operation with a fitting finite bound; it cannot authorize unknown behavior. Runtime provider substitution preserves the interface's effects. Optional data guards remain distinct from effect, callback, lifetime and dependency obligations.

## Fixed adversarial plan

The exact literal sources will use the approved public syntax once the main builder freezes it. The following behavioral families and required outcomes were selected independently before that syntax was available.

| IDs | Adversarial family | Required observation |
| --- | --- | --- |
| D01–D12 | Pure default; each IO/State/Clock/Random/Environment bound; zero/multiple/redundant bounds; unknown/Task/dynamic declarations; marker aliases and definition order | Only the published finite declarations select checked effectful mode. Runtime markers preserve the identical function without registration. Invalid or unavailable declarations fail before application evaluation. Task remains deferred. |
| E01–E12 | Direct operation; direct checked calls; recursive graph; imported/assigned aliases; pure-to-effectful and effectful-to-pure composition; unused extra permissions | Every actual operation has an inspected versioned contract. Operation/callee effects union and fit the receiving declaration. Pure callers refuse effectful invocation. Failure bounds remain independent. |
| H01–H16 | Fixed higher-order contracts; collections map/filter/fold; nested closures; returned/conditional/aliased callback targets; broad callback bounds; pure callable annotation; unknown ordinary function | All admitted callback targets and their declared bounds propagate, including conditional branches and returned closures. Pure callable annotations never establish a provider/callback's behavior. Unknown callback behavior fails despite effect permissions. |
| P01–P14 | Exact real/test/recorded providers; data timestamp alternative; unsupported provider subclasses/proxies/arbitrary objects; hostile argument hooks; provider initialization | Fake and recorded providers retain interface effects. Provider operation inputs/results are exact supported data; foreign hooks cannot run during product validation. Setup/import claims are separate from later invocation; ordinary setup is disclosed as unchecked. |
| V01–V16 | Capability parameter; tuple/Vector/map/record/default/constant/returned data; local aliases; nested capture; returned callback; passing to pure function; resource transfer | Live capabilities cannot become admitted data or callable captures. Only the declared finite borrowing shape can use them. Unsupported return/store/capture/transfer escapes fail. Exact stable data remains admitted. |
| L01–L16 | Finite reader open/read/close; body failure; entry/read/cleanup failures; nested borrowing; alias/capture/return/store escape; use after close; unsupported context managers | Every admitted entry/exit/read is characterized. Resources close under normal and declared body-failure exits. Product-visible use after close fails within the finite lifetime contract. Unknown context managers and uncertain lifetime paths fail closed. |
| I01–I18 | Operator/truth/equality/hash/format/attribute/iteration/matching/context-manager implicit dispatch; arbitrary writes to domain values; unknown methods and callbacks under all effects | Each implicit dispatch is characterized or refused. Effect declarations provide no unknown-call or mutable-data hole. Supported state changes occur through the characterized state capability only. |
| N01–N10 | Sentinel decorators/defaults/annotations/module initialization/provider setup; malformed syntax/policy; audit and failed strict/build | Check/build never executes the literal application source. Failed gates publish no checked artifact; audit/failed/dependency-failed boundaries retain unverified evidence. |
| F01–F18 | Cold/warm evidence; changed callee source/effect declaration; operation/checker version; policy; actual product bytes; aliases writing capabilities and runtime foundations | A relevant change invalidates affected evidence and its consumers. Source/effects/failures/trust/initialization remain independent dimensions. Cache decoding cannot upgrade failed or audit evidence. |
| G01–G10 | Guards off/selected exports/debug; selected capability/Callable boundary; pure selected data consumer; unchecked provider/callback; internal composition | Static effect/lifetime rules apply with guards off. Unsupported capability/Callable guard schemas remain refused. Supported data guard coverage does not certify provider/callback effects or lifetime. Ordinary internal calls need no per-call certificate registry. |
| C01–C10 | Actual installed CLI check/build/explain/current JSON evidence; ordinary execution of accepted artifact; malformed/unknown CLI and target; snapshot stability | Execute actual M5 CLI commands and successfully built stock Python artifacts, inspect authored diagnostics and evidence, and confirm unchanged before/after source maps. Both platforms use actual supported interpreters. A separate report command remains M10. |

## Planned execution and decision rules

1. Read the main plan and published operation/lifetime contracts, inspect the implementation's declaration/type/call graph/callback propagation, runtime provider storage/dispatch, foundation gates, guard schemas and evidence/cache/build paths. Resolve positive public syntax once before generating a fixed literal source corpus.
2. Pass literal application strings to the source checker without importing/evaluating them; inspect expected status, diagnostic rule/origin/path and independent contract dimensions. Add targeted concrete regressions only when source inspection or probes expose a gap.
3. Run temporary multi-module projects through actual check/build/installed CLI commands, including cold/warm changes and source/policy/version/product-byte freshness transitions. Keep sentinel application effects absent through check/build. Execute only accepted artifacts intentionally afterward.
4. Run ordinary runtime provider/data/lifetime probes with exact-hook counters and retained data. Check normal reader cleanup, cleanup during declared body failures and use after close against the published finite contract. Do not claim control over Python pre-entry keyword binding or unsupported foreign hooks.
5. After the main/runtime workers freeze their owned source, record before/after current-source SHA-256 maps and run the bounded final corpus plus inherited/new suite on macOS and actual Docker Linux. Compare platform maps to each other and the current checkout. Report concrete blockers promptly with literal reproducer, command and observed result to the main worker/runtime helper/root.

A conservative refusal is acceptable when the milestone explicitly publishes that shape as unsupported. A falsely admitted unknown effect, callback, resource escape, data capability, implicit dispatch or stale claim blocks this milestone. Unsupported features are not warning-based certified behavior. A correct ordinary runtime result cannot repair a missing static contract.

## Interim findings and corrective retests

The following findings concern the changing implementation and were reported with concrete sources to the main worker/root. Their focused final retests pass.

- Root namespace syntax `import pyalamode as p; @p.effects(p.Clock)` initially failed token identity resolution. The corrected checker resolves the actual root marker/token identities and admits that positive control.
- Stock CPython binds `import pyalamode.effects as e` to the package's exported function after `__init__` exports that name. A minimal actual CPython 3.13.1 package probe confirmed the binding. The checker now models it as the identity marker and refuses nonexistent submodule namespace operations; `from pyalamode.effects import names` remains unambiguous.
- Runtime IO factories require explicit `allowed_ops`, and recorded providers have concrete `IndexError`/`KeyError` failures. The checker was aligned with those actual signatures, permissions, failure categories and transitive foundations. Known narrow IO remains conservatively unable to satisfy a bare checked IOCapability slot, including a read-only checked reader.
- A valid known writer was initially admitted: importing `_Borrow as manager`, assigning `manager.__enter__.__code__ = replacement.__code__`, and then using a checked `with borrow(cap)` scope. An ordinary replacement body could print undeclared IO during characterized entry. Final source checks refuse that exact code-object replacement, exit-method writes, assigned method aliases and lease-slot writes; warm consumer evidence is invalidated.
- Root identified ambient entropy/clock seeding in the initial secrets/random import chain. The runtime now implements live Random by direct `os.urandom` rejection sampling. Product catalog/class initialization performs no provider entropy/clock/environment/IO observation. The current failure and foundation inventories match that implementation.

All previously reported blockers are resolved on the frozen source below. No product/test/example/harness file was changed by this reviewer.

## Final frozen two-platform observations

macOS used actual CPython 3.13.1 standard GIL, Clang 16.0.0, arm64 macOS 26.6.2. Linux used actual `python:3.13.1-slim`, CPython 3.13.1 standard GIL, GCC 12.2.0, aarch64 LinuxKit 5.15.49/glibc 2.36, image digest `sha256:031ebf3cde9f3719d2db385233bcb18df5162038e9cda20e64e08f49f4b47a2f`. The Linux review copied the frozen package into temporary packaging storage, installed it with pip, compared all eleven installed package Python files with current source, and used its actual installed CLI. macOS used the existing installed `.venv/bin/pyalamode` CLI. Application source was never imported/evaluated by source/check/build probes; accepted artifacts were executed intentionally afterward through stock Python.

| Independent final gate | macOS | Actual Linux |
| --- | --- | --- |
| Literal source corpus | 175 cases; 36 expected admissions, 139 expected refusals; zero status/selection mismatches | Same |
| Ordinary provider/data/lifetime/IO probes | 142 assertions; zero foreign hooks | Same |
| Project, optional guard and nonexecution probes | 45 assertions | Same |
| Actual installed CLI/artifact walkthrough | 32 assertions | Same |
| Writer/cache/actual product-byte/version/policy probes | 93 assertions | Same |
| Full and partial warm callable-evidence probes | 20 assertions | Same |
| Complete product suite | 194 tests, 2.741 seconds | 194 tests, 9.394 seconds |
| Complete source/harness before-after gate | 35 SHA-256 entries unchanged | Same; map identical to macOS and current files |

The literal corpus below covers every finite operation, effect declaration identity/order/duplicate/unknown cases, direct/aliased/recursive calls, capability-bearing Effectful higher-order invocation, Vector map/filter/fold callback unions, branch and returned-callback unions, pure retention of effectful callable values, all capability data/alias/default/capture/result exclusions, logical scope/nested lifetime/early return, persistent-reader refusal, implicit operator/truth/equality/hash/format/iteration/matching dispatch, and actual public/private/stdlib foundation writers. Source strings are literal checker input, never evaluated application code. Failed strict boundaries carry unverified source evidence; none of the refused literal cases retains a successful checked source claim.

The 142 ordinary runtime assertions check identity declarations without metadata changes, all five exact provider classes, finite recorded results/exhaustion, Random bound validation without consumption, explicit environment defaults, live exact/range contracts, operation permissions, capability exclusion from Vector/snapshot/thaw/hash schemas, subclass/direct-construction/attribute/proxy refusals and exact-hook counters. Borrow tests cover normal exit, return behavior through built artifacts, body failure, child closure, ancestor invalidation of active descendants, repeated entry/exit and closed-view borrowing. Originals remain live while closed views refuse further operations. Real whole-path IO preserves UTF-8/newlines, rejects finite bad paths/symlinks/permissions and reports missing/encoding failures. Twenty repeated invalid UTF-8 reads and twenty surrogate writes leave the actual open-descriptor count unchanged on each platform. This verifies internal whole-path cleanup; it does not claim a persistent reader API or guaranteed success of an unavailable OS close.

The 45 project assertions keep ordinary factory setup distinct from checked invocation, refuse unknown shell annotations and closed/unsupported borrowed input evidence, preserve warm failed status, enforce entry effect policy and unknown-selector/family/Task/duplicate policy failures, and leave no artifact after a failed gate. Actual off/exports/debug artifacts execute normally. Selected capability and callback guard schemas fail closed. Debug builds may validate a capability function's exact int local/result while excluding its capability parameter, and selected pure data façades execute independently. Internal effect functions retain ordinary identity without mandatory wrappers. Default/decorator/annotation/strict-initializer sentinel writes remain absent through check/build; an ordinary initializer sentinel appears only after intentional import.

The 32 installed CLI assertions use check, build, audit, supported explain symbols and current JSON evidence, with no later-milestone report command. They inspect the selected denominator, declared/required effects, recorded failures, separate ordinary initialization evidence, unchanged off artifact bytes, stock execution, ordinary identity, undeclared unknown-operation refusal despite all five permissions, audit non-certification, failed publication and unsupported-target tooling status.

The 93 freshness assertions use eleven temporary writer layouts: public capability class/method, imported/assigned/module setter aliases, private borrow-method/assigned-method/lease storage, and actual clock/entropy/symlink foundations. Each begins clean cold/warm, changes a known writer, invalidates the affected consumer, refuses warm/fresh checks and subsequent warm/build publication. Private product aliases have a disclosed conservative whole-product exclusion; no minimal invalidation claim follows. Actual `effects.py`, `model.py` and `checker.py` byte edits, operation/checker label changes and policy changes are performed only in an independent temporary package copy and invalidate current consumer evidence. The checkout stays untouched.

The 20 callback cache assertions separately exercise a concrete Clock target returned under a broader Clock+State annotation, and a returned closure capturing a conditional Effectful callback. Cold, fully warm and partially warm analysis agree. Factory bodies are reused while consumer bodies are reanalyzed. Retained callback dependencies/trust remain visible, while uninvoked callback effects and operations stay separate from pure factory invocation. Actual subsequent invocation retains the tighter Clock requirement and the complete failure bound. This reconciles the current `effects-capabilities-5.1` exact target/bound/conditional/capture serialization with the independent effect and failure dimensions.

## Evidence dimensions and published limits

| Dimension | Inspected final claim |
| --- | --- |
| Enforcement/source | Strict checked participating functions and separately checked functional initialization; ordinary setup and unrelated initialization remain unchecked. Audit/failed/dependency-failed evidence is unverified. |
| Behavior | Finite declared upper bounds and actual required unions/origin paths; declared effectful targets remain effectful even when their current body performs no operation. Fake/recorded interfaces retain their family. |
| Trust | CPython/product foundations and finite actual transitive reads are visible. Retained concrete callable assumptions propagate separately from invocation. No external-integration approval or generic unknown-operation trust hole was added. |
| Failure | Concrete graph failures and conditional callable family failure bounds remain separate from effects. Recorded exhaustion/missing paths, valid IO/encoding/random failures and logical lifetime failure are characterized; invalid ordinary inputs are not admitted contracts. |
| Freshness | Actual source, policy, target, checker/operation version, analyzed writers and ten foundation-file bytes invalidate subsequent evidence/builds. Eleven complete package-file hashes, owned tests/examples/fixtures/benchmark and reviewer harness are independently frozen below. |
| Boundary | Off is the default; selected data exports/debug assertions publish finite coverage. Capability/Callable/Effectful boundary schemas remain unsupported, and guards do not establish effects, provider permission/lifetime, callback evidence or dependency integrity. |

The [M5 handoff](../milestones/05-effects.md), [runtime contract](../evidence/m05-runtime-contract.md) and [measurement report](../evidence/m05-runtime-measurements.md) match inspected source. Exact runtime IO permissions can be narrow, while analyzed bare IOCapability slots conservatively require both operations. Capability captures, data storage, transfer, persistent sessions/readers/cursors, concurrency, arbitrary implicit dispatch and general handlers remain unsupported. Logical borrowing supplies one-way view lifetime, not ownership, exclusivity, synchronization or OS-handle transfer. Root/path replacement races violate the explicitly stated IO precondition; path checks are not an atomic sandbox. IO writes are non-atomic and may leave truncated/partial content on failure.

Both [macOS measurement JSON](../evidence/m05-runtime-macos.json) and [Linux measurement JSON](../evidence/m05-runtime-linux.json) were independently reparsed against current files. Their ten product and four owned/support source hashes match each other and current bytes, with unchanged before/after maps. Each contains twenty rows, three trials per row, twenty-five measured checked calls per trial (sixty intervals/1,500 calls), plus 200 untimed warmup calls. Every correctness obligation passes; the actual normally imported off artifact contains seven checked functions and an Effectful clock-capability smoke returning 7. The fixture and generated artifact hashes agree across platforms.

Published bounds correctly include O(h²) lease identity/liveness scans, retained parent chains, O(n²) recorded duplicate setup, O(n) lookup/tuple writes plus scalar lengths, variable rejection sampling with expected fewer than two draws under independent uniform OS entropy, and filesystem/text work. The measurement report identifies included `tracemalloc`/Python-loop cost, excluded setup/build/import/warmup/correctness, traced allocation rather than RSS, uncontrolled load/filesystem caches, live nondeterministic observations, and repeated live rows with no size-varying parameter. It makes no universal latency, throughput, memory, determinism, termination or target-user usability claim.

No remaining blocker was observed in this bounded final review. Unchecked private tampering, violated path/lifetime/dependency assumptions, concurrent use and unsupported dynamic Python are outside the conditional claim. Root owns final Git staging, commit and sequencing. This reviewer changed only this conformance document in the repository, used temporary probe/package storage, and made no commit, schedule, CatWrangler call or delegation.

## Frozen current source SHA-256 map

The following complete map is identical in both final platform reports, their before/after snapshots and the current files. `reviewer:` entries identify temporary reviewer corpus/harness files; those are not product modules. The single map is published once because macOS and Linux are equal.

```json
{
  "benchmarks/m05_effects.py": "83b54c93ecc4240f340bcc88ba20b16f8a640306d49f784c26662cfe22bb22d3",
  "examples/effects/__init__.py": "976d6c1731a16ecf67980cfaddeed34d9f0182df1aeabb5a8e60720709a1f8b6",
  "examples/effects/core.py": "f18f5a58a03e37bb619319121deaf8a59a2ef5fc516142e342a433e23ded174c",
  "examples/effects/demo.py": "9f4d1340e900f8232461e59fcfa720f79b28a13fdc1dc168c7eb24c69dfe40dd",
  "pyalamode/__init__.py": "a945bad0b9c4cb6670fd6b35d11a23eea36b0848895c5bf95a682d49d804ed70",
  "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
  "pyalamode/boundaries.py": "9e6a903b36e0a8be24a55bb649957306252b21ee47ce5d1eaab7237640d3618a",
  "pyalamode/checker.py": "68e251a845f0e82f4b8d5ae66b31d29fd6682fa38b4c70f66f1f436353d1073d",
  "pyalamode/cli.py": "01b8930a041db1ac231273afb0eb81d2f119516b7f3c98af9969f9431bb4bf3c",
  "pyalamode/collections.py": "1fa0330adc28b33da902ea392a8227af29650672cfe64348324fe3577855dfdc",
  "pyalamode/effects.py": "31d3ee92aaf256fe92f29fa221941d6fac41115fb6c87e4b31503639776a9dfa",
  "pyalamode/guardgen.py": "b71356b99188e338e5e59d379d1687069067f9ea869abb2137cf0b66ebb44aa5",
  "pyalamode/model.py": "4d710be78aade0c89d16cf1049d35af33e11957b2c02822873541e986668332d",
  "pyalamode/project.py": "02360c7f727c9cd99ebfbfcf837c8d581597f77f3b45edc6e1bc07063b8f47ff",
  "pyalamode/records.py": "0f98108b894860244c410f5761f80f64a9ce9b212ebb587ab16f77ed69e3d8e9",
  "reviewer:callback_warm_probe.py": "96b86e4d4b943924b6ba250c18978e2cb8b283d4cafd2e5cde7fc4aa6a03fc6a",
  "reviewer:cli_probe.py": "1bb06d88781a4aa845b7bedbeccd6a4e2a799342973aa09d455abdce6e648437",
  "reviewer:final_probe.py": "26b8dd59978605cba4d3b44242a05cef623858235163d754fd6cf820fbaf278c",
  "reviewer:freshness_probe.py": "64357a448519a8ad4580f3be3b271c5a937a349066e4d9d2f77ea162ff90ae2e",
  "reviewer:literal-cases.json": "9326109f71eb36bf4dd944cea7685e0a1e7bba78cf4825a8511fb6470cd5395c",
  "reviewer:make_cases.py": "0b3244ec30ae791cd89f210a787291057309db6cb0039d3c31a5eeb51561ea44",
  "reviewer:project_probe.py": "1406ff2960fb91797732ecdb1141bc4035416bbb3c61766351f4ffc6c5450260",
  "reviewer:runtime_probe.py": "a53f9667fc585bb58592fca1383771ee345a2e820114ac7449ac6cfc67da128b",
  "reviewer:static_probe.py": "12d8da3f70312ba54c8e4790427e0e363509073115d9c6f822d33a4d46e22884",
  "tests/fixtures/m05/capability_escape.py": "8a7d3cc2af7452df06aa285aef88ecd910a9695c56baa4016be7e0faee849a79",
  "tests/fixtures/m05/undeclared.py": "af86b51c9d7d8fb60db6c7793c5f8a56e749cb73ac3c583550534cbac35ae471",
  "tests/fixtures/m05/unknown_operation.py": "faefe7fdeacb00163a72ba0e6241cdc0e313339b1eaf74c789bfc0c33a2a54f7",
  "tests/m01_scalar.py": "db119a7c5422292b7f13053f1dd3e7a43d5fb68eb3ec3c885269e548c3c228ce",
  "tests/m02_modules.py": "fdb5f94f7a03d122e82de1c32b7b5b7d4237e0fa0319ac78fe96a9ebce698a4b",
  "tests/m03_collections.py": "2ff03b8b771e6539f14ef528eaa245ab5fbf6a51ed60ed9f769dd82db79d403e",
  "tests/m03_runtime.py": "88db699167977af3934c85c793dc4f674e702f80f28a0dc19bba308ffd31551b",
  "tests/m04_records.py": "ff65472a4d5f478ecd745bd55d98e287025bc32c70836615683a5f3a71070e75",
  "tests/m04_runtime.py": "c3544a59356c91ab6bda4d41ffaf79658efa57bd5f74d214ea1ec5caea292c5a",
  "tests/m05_effects.py": "09ae107342ed62d29dfa929cc57be0a786d6b23dabec6a29a2b4897b0095d2ff",
  "tests/m05_runtime.py": "543a0ce687072a8527887bc79e20ef4308797b38cfb7ddf7d0e95056fccd1a21"
}
```

## Executed literal source corpus

`expected: 0` is strict admission; `expected: 1` is refusal. A `selected` field additionally checks that an alias declaration selects the required boundary rather than disappearing from the denominator. These are complete literal input strings passed to `analyze_source`, not evaluated Python application code.

```json
[
  {
    "id": "E01",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef probe(cap:IOCapability)->str:\n    return cap.read_text(\"a.txt\")\n",
    "note": ""
  },
  {
    "id": "E08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:IOCapability)->str:\n    return cap.read_text(\"a.txt\")\n",
    "note": ""
  },
  {
    "id": "E15",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:IOCapability)->str:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "E02",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef probe(cap:IOCapability)->None:\n    return cap.write_text(\"a.txt\",\"text\")\n",
    "note": ""
  },
  {
    "id": "E09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:IOCapability)->None:\n    return cap.write_text(\"a.txt\",\"text\")\n",
    "note": ""
  },
  {
    "id": "E16",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:IOCapability)->None:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "E03",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(State)\ndef probe(cap:StateCapability)->int:\n    return cap.get()\n",
    "note": ""
  },
  {
    "id": "E10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:StateCapability)->int:\n    return cap.get()\n",
    "note": ""
  },
  {
    "id": "E17",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:StateCapability)->int:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "E04",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(State)\ndef probe(cap:StateCapability)->None:\n    return cap.set(4)\n",
    "note": ""
  },
  {
    "id": "E11",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:StateCapability)->None:\n    return cap.set(4)\n",
    "note": ""
  },
  {
    "id": "E18",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:StateCapability)->None:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "E05",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "E12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "E19",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:ClockCapability)->int:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "E06",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability)->int:\n    return cap.below(4)\n",
    "note": ""
  },
  {
    "id": "E13",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:RandomCapability)->int:\n    return cap.below(4)\n",
    "note": ""
  },
  {
    "id": "E20",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:RandomCapability)->int:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "E07",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"KEY\",\"default\")\n",
    "note": ""
  },
  {
    "id": "E14",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"KEY\",\"default\")\n",
    "note": ""
  },
  {
    "id": "E21",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.unknown()\n",
    "note": ""
  },
  {
    "id": "D01",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\n@fun\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D02",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D03",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(\"Task\")\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(\"Other\")\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock,Clock)\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\n@effects(Clock)\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\n@fun\n@effects(Clock)\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(print(\"sentinel\"))\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(*[Clock])\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D11",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(value=Clock)\ndef probe(x:int)->int:\n    return x\n",
    "note": ""
  },
  {
    "id": "D12",
    "expected": 0,
    "source": "from pyalamode import effects as mark, Clock as family, ClockCapability\n@mark(family)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D13",
    "expected": 0,
    "source": "import pyalamode as p\n@p.effects(p.Clock)\ndef probe(cap:p.ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D14",
    "expected": 1,
    "source": "@effects(Clock)\ndef probe(x:int)->int:return x\nfrom pyalamode import effects,Clock\n",
    "note": ""
  },
  {
    "id": "D15",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nClock=\"IO\"\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D16",
    "expected": 0,
    "source": "# mode: fun\nfrom pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D17",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nmark=effects\n@mark(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": "Actual marker assignment alias must resolve or be explicitly refused; a zero-selection clean gate is not admission.",
    "selected": 1
  },
  {
    "id": "D18",
    "expected": 0,
    "source": "from pyalamode.effects import effects as mark,Clock,ClockCapability\n@mark(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "D19",
    "expected": 1,
    "source": "import pyalamode.effects as e\n@e.effects(e.Clock)\ndef probe(cap:e.ClockCapability)->int:return cap.now_ns()\n",
    "note": "Ordinary import alias binds exported effects function, not a submodule namespace."
  },
  {
    "id": "D20",
    "expected": 1,
    "source": "import pyalamode\n@pyalamode.effects.effects(pyalamode.effects.Clock)\ndef probe(x:int)->int:return x\n",
    "note": "Root package effects attribute is the declaration function."
  },
  {
    "id": "C01",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return leaf(cap)\n",
    "note": ""
  },
  {
    "id": "C02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\n@fun\ndef probe(cap:ClockCapability)->int:return leaf(cap)\n",
    "note": ""
  },
  {
    "id": "C03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(x:int)->int:return x\n@fun\ndef probe(x:int)->int:return leaf(x)\n",
    "note": ""
  },
  {
    "id": "C04",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef leaf(x:int)->int:return x+1\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return leaf(cap.now_ns())\n",
    "note": ""
  },
  {
    "id": "C05",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\nalias=leaf\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return alias(cap)\n",
    "note": ""
  },
  {
    "id": "C06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\nalias=leaf\n@effects(IO)\ndef probe(cap:ClockCapability)->int:return alias(cap)\n",
    "note": ""
  },
  {
    "id": "C07",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability,again:bool)->int:\n    if again:return probe(cap,False)\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "C08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(x:int)->int:return print(x)\n",
    "note": ""
  },
  {
    "id": "C09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(x:int)->int:return arbitrary(x)\n",
    "note": ""
  },
  {
    "id": "C10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\ndef ordinary(x:int)->int:return x\n@effects(IO,State,Clock,Random,Environment)\ndef probe(x:int)->int:return ordinary(x)\n",
    "note": ""
  },
  {
    "id": "H01",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\n@effects(Clock)\ndef apply(callback:Effectful[[ClockCapability],int,Clock],cap:ClockCapability)->int:return callback(cap)\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return apply(leaf,cap)\n",
    "note": ""
  },
  {
    "id": "H02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef apply(callback:Effectful[[ClockCapability],int,Clock],cap:ClockCapability)->int:return callback(cap)\ndef ordinary(cap:ClockCapability)->int:return cap.now_ns()\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return apply(ordinary,cap)\n",
    "note": ""
  },
  {
    "id": "H03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef probe(callback:Effectful[[int],int,Clock],x:int)->int:\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H04",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(callback:Effectful[[int],int,Clock],x:int)->int:\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef probe(callback:Effectful[[int],int,Clock],x:int)->int:\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(callback:Callable[[ClockCapability],int],cap:ClockCapability)->int:\n    return callback(cap)\n",
    "note": ""
  },
  {
    "id": "H07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(callback:Effectful[[ClockCapability],int,IO],cap:ClockCapability)->int:\n    return callback(cap)\n",
    "note": ""
  },
  {
    "id": "H08",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef leaf(x:int)->int:return x+1\n@effects(Clock)\ndef apply(callback:Effectful[[int],int,Clock],x:int)->int:return callback(x)\n@effects(Clock)\ndef probe(x:int)->int:return apply(leaf,x)\n",
    "note": ""
  },
  {
    "id": "H09",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@effects(Clock,Random)\ndef probe(which:bool,x:int)->int:\n    callback=first if which else second\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@effects(Clock)\ndef probe(which:bool,x:int)->int:\n    callback=first if which else second\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H11",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@effects(Clock,Random)\ndef probe(which:bool,x:int)->int:\n    if which:callback=first\n    else:callback=second\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@effects(Clock)\ndef probe(which:bool,x:int)->int:\n    if which:callback=first\n    else:callback=second\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H13",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(x:int)->int:return x\n@effects(Clock)\ndef probe(values:Vector[int])->Vector[int]:return values.map(leaf)\n",
    "note": ""
  },
  {
    "id": "H14",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(x:int)->int:return x\n@fun\ndef probe(values:Vector[int])->Vector[int]:return values.map(leaf)\n",
    "note": ""
  },
  {
    "id": "H15",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Environment)\ndef keep(x:int)->bool:return x>0\n@effects(Environment)\ndef probe(values:Vector[int])->Vector[int]:return values.filter(keep)\n",
    "note": ""
  },
  {
    "id": "H16",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(State)\ndef total(a:int,x:int)->int:return a+x\n@effects(State)\ndef probe(values:Vector[int])->int:return values.fold(total,0)\n",
    "note": ""
  },
  {
    "id": "H17",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(State)\ndef total(a:int,x:int)->int:return a+x\n@fun\ndef probe(values:Vector[int])->int:return values.fold(total,0)\n",
    "note": ""
  },
  {
    "id": "H18",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef maker(x:int)->Effectful[[int],int,Clock]:\n    @effects(Clock)\n    def callback(y:int)->int:return x+y\n    return callback\n@effects(Clock)\ndef probe(x:int)->int:\n    callback=maker(x)\n    return callback(2)\n",
    "note": ""
  },
  {
    "id": "H19",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef maker(x:int)->Effectful[[int],int,Clock]:\n    @effects(Clock)\n    def callback(y:int)->int:return x+y\n    return callback\n@fun\ndef probe(x:int)->int:\n    callback=maker(x)\n    return callback(2)\n",
    "note": ""
  },
  {
    "id": "H20",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(x:int)->int:return x\n@fun\ndef probe()->Callable[[int],int]:return leaf\n",
    "note": ""
  },
  {
    "id": "H21",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@fun\ndef pick(which:bool)->Effectful[[int],int,Clock,Random]:return first if which else second\n@effects(Clock,Random)\ndef probe(which:bool,x:int)->int:\n    callback=pick(which)\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H22",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@fun\ndef pick(which:bool)->Effectful[[int],int,Clock,Random]:return first if which else second\n@effects(Clock)\ndef probe(which:bool,x:int)->int:\n    callback=pick(which)\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H23",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@fun\ndef pick(which:bool)->Effectful[[int],int,Clock,Random]:return first if which else second\n@fun\ndef probe(which:bool,x:int)->int:\n    callback=pick(which)\n    return callback(x)\n",
    "note": ""
  },
  {
    "id": "H24",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef first(x:int)->int:return x\n@effects(Random)\ndef second(x:int)->int:return x+1\n@fun\ndef pick(which:bool)->Effectful[[int],int,Clock,Random]:return first if which else second\n@fun\ndef probe(which:bool)->Effectful[[int],int,Clock,Random]:return pick(which)\n",
    "note": ""
  },
  {
    "id": "V01",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->ClockCapability:\n    return cap\n",
    "note": ""
  },
  {
    "id": "V02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->tuple[ClockCapability]:\n    return (cap,)\n",
    "note": ""
  },
  {
    "id": "V03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->Vector[ClockCapability]:\n    return Vector.of(cap)\n",
    "note": ""
  },
  {
    "id": "V04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    alias=cap\n    return alias.now_ns()\n",
    "note": ""
  },
  {
    "id": "V05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    cap.value=1\n    return 1\n",
    "note": ""
  },
  {
    "id": "V06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    cap[0]=1\n    return 1\n",
    "note": ""
  },
  {
    "id": "V07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap+1\n",
    "note": ""
  },
  {
    "id": "V08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->bool:\n    return cap==cap\n",
    "note": ""
  },
  {
    "id": "V09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->bool:\n    return cap is cap\n",
    "note": ""
  },
  {
    "id": "V10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    if cap:return 1\n    return 0\n",
    "note": ""
  },
  {
    "id": "V11",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->str:\n    return str(cap)\n",
    "note": ""
  },
  {
    "id": "V12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->str:\n    return f\"{cap}\"\n",
    "note": ""
  },
  {
    "id": "V13",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return hash(cap)\n",
    "note": ""
  },
  {
    "id": "V14",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return len(cap)\n",
    "note": ""
  },
  {
    "id": "V15",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap.__class__\n",
    "note": ""
  },
  {
    "id": "V16",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap.__dict__\n",
    "note": ""
  },
  {
    "id": "V17",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@record\nclass Holder:\n    cap:ClockCapability\n",
    "note": ""
  },
  {
    "id": "V18",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    @effects(Clock)\n    def nested()->int:return cap.now_ns()\n    return nested()\n",
    "note": ""
  },
  {
    "id": "V19",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->Effectful[[],int,Clock]:\n    @effects(Clock)\n    def nested()->int:return cap.now_ns()\n    return nested\n",
    "note": ""
  },
  {
    "id": "V20",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    @effects(Clock)\n    def nested(view:ClockCapability=cap)->int:return view.now_ns()\n    return nested()\n",
    "note": ""
  },
  {
    "id": "V21",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@fun\ndef accept(x:tuple[int])->int:return x[0]\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return accept((cap,))\n",
    "note": ""
  },
  {
    "id": "L01",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        value=scoped.now_ns()\n    return value\n",
    "note": ""
  },
  {
    "id": "L02",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "L03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        value=scoped.now_ns()\n    return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "L04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->ClockCapability:\n    with borrow(cap) as scoped:\n        return scoped\n",
    "note": ""
  },
  {
    "id": "L05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        alias=scoped\n        return alias.now_ns()\n",
    "note": ""
  },
  {
    "id": "L06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        value=scoped.now_ns()\n    scoped=1\n    return scoped\n",
    "note": ""
  },
  {
    "id": "L07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with cap as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "L08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with arbitrary(cap) as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "L09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef probe(cap:IOCapability)->str:\n    with reading(cap,\"a.txt\") as reader:\n        return reader.read_text()\n",
    "note": ""
  },
  {
    "id": "L10",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        return leaf(scoped)\n",
    "note": ""
  },
  {
    "id": "L11",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        with borrow(scoped) as inner:\n            value=inner.now_ns()\n        return scoped.now_ns()+value\n",
    "note": ""
  },
  {
    "id": "L12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        with borrow(scoped) as inner:\n            value=inner.now_ns()\n        return inner.now_ns()+value\n",
    "note": ""
  },
  {
    "id": "L13",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    scoped=1\n    with borrow(cap) as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "L14",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        @effects(Clock)\n        def nested()->int:return scoped.now_ns()\n        return nested()\n",
    "note": ""
  },
  {
    "id": "L15",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    manager=borrow(cap)\n    return 1\n",
    "note": ""
  },
  {
    "id": "L16",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        if True:value=scoped.now_ns()\n    return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "I01",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability)->int:\n    return cap.below(True)\n",
    "note": ""
  },
  {
    "id": "I02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability)->int:\n    return cap.below(\"4\")\n",
    "note": ""
  },
  {
    "id": "I03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability)->int:\n    return cap.below(1,2)\n",
    "note": ""
  },
  {
    "id": "I04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability)->int:\n    return cap.below(bound=2)\n",
    "note": ""
  },
  {
    "id": "I05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability)->int:\n    return cap.below(*[2])\n",
    "note": ""
  },
  {
    "id": "I06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"KEY\")\n",
    "note": ""
  },
  {
    "id": "I07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"KEY\",1)\n",
    "note": ""
  },
  {
    "id": "I08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(name=\"KEY\",default=\"x\")\n",
    "note": ""
  },
  {
    "id": "I09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"KEY\",\"x\",3)\n",
    "note": ""
  },
  {
    "id": "I10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef probe(cap:IOCapability)->str:\n    return cap.read_text(1)\n",
    "note": ""
  },
  {
    "id": "I11",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef probe(cap:IOCapability)->None:\n    return cap.write_text(\"a\",1)\n",
    "note": ""
  },
  {
    "id": "I12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(State)\ndef probe(cap:StateCapability)->None:\n    return cap.set(True)\n",
    "note": ""
  },
  {
    "id": "I13",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns(1)\n",
    "note": ""
  },
  {
    "id": "I14",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    for value in cap:\n        return value\n    return 0\n",
    "note": ""
  },
  {
    "id": "I15",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    match cap:\n        case _:return 1\n",
    "note": ""
  },
  {
    "id": "I16",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO,State,Clock,Random,Environment)\ndef probe(x:int)->int:\n    values=[x]\n    return x\n",
    "note": ""
  },
  {
    "id": "N01",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(x:int=print(\"default\"))->int:return x\n",
    "note": ""
  },
  {
    "id": "N02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef probe(x:print(\"annotation\"))->int:return x\n",
    "note": ""
  },
  {
    "id": "N03",
    "expected": 1,
    "source": "# mode: fun\nfrom pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nvalue=print(\"initializer\")\n@effects(Clock)\ndef probe(x:int)->int:return x\n",
    "note": ""
  },
  {
    "id": "N04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import live_clock\n@effects(Clock)\ndef probe()->int:\n    cap=live_clock()\n    return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "N05",
    "expected": 1,
    "source": "# mode: fun\nfrom pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import live_clock\nCAP=live_clock()\n@effects(Clock)\ndef probe(x:int)->int:return x\n",
    "note": ""
  },
  {
    "id": "N06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import live_clock\n@effects(Clock)\ndef probe(cap:ClockCapability=live_clock())->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "P01",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=(\"read_text\",\"write_text\"))\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=(\"read_text\",))\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=(\"read_text\",))\n    return writer(cap)\n",
    "note": ""
  },
  {
    "id": "P04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io((),allowed_ops=(\"write_text\",))\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),))\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=(\"read_text\",\"write_text\",\"unknown\"))\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=(\"read_text\",\"read_text\"))\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=[\"read_text\",\"write_text\"])\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode import recorded_io\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell():\n    cap=recorded_io(((\"a\",\"text\"),),allowed_ops=(\"read_text\",\"write_text\"),extra=True)\n    return reader(cap)\n",
    "note": ""
  },
  {
    "id": "P10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(IO)\ndef reader(cap:IOCapability)->str:return cap.read_text(\"a\")\n@effects(IO)\ndef writer(cap:IOCapability)->None:return cap.write_text(\"a\",\"new\")\ndef shell(cap:IOCapability):return writer(cap)\n",
    "note": ""
  },
  {
    "id": "P11",
    "expected": 0,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\nfrom pyalamode import recorded_clock\ndef shell():\n    cap=recorded_clock((1,2))\n    return leaf(cap)\n",
    "note": ""
  },
  {
    "id": "P12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\n@effects(Clock)\ndef leaf(cap:ClockCapability)->int:return cap.now_ns()\nfrom pyalamode import recorded_clock\ndef shell():\n    cap=recorded_clock((1,2))\n    with borrow(cap) as scoped:pass\n    return leaf(scoped)\n",
    "note": ""
  },
  {
    "id": "B01",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport time\ntime.time_ns=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B02",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom time import time_ns as now\nnow.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B03",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport os\nos.urandom=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B04",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport os\nos.environ={}\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B05",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport builtins\nbuiltins.open=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B06",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport io\nio.open=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B07",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport _io\n_io.TextIOWrapper=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B08",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport posixpath\nposixpath.realpath=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B09",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nClockCapability.now_ns=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B10",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nalias=ClockCapability\nalias.now_ns=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B11",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nsetattr(ClockCapability,\"now_ns\",print)\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B12",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom builtins import setattr as put\nput(ClockCapability,\"now_ns\",print)\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B13",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport builtins as b\nb.setattr(ClockCapability,\"now_ns\",print)\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B14",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nput=setattr\nput(ClockCapability,\"now_ns\",print)\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B15",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom builtins import delattr as remove\nremove(ClockCapability,\"now_ns\")\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B16",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import ClockCapability as capclass\ncapclass.now_ns=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B17",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import effects as marker\nmarker.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B18",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nimport stat\nstat.S_ISLNK=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B19",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nClockCapability.now_ns.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B20",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _live as helper\nhelper.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B21",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _Borrow as manager\ndef replacement(self):\n    print(\"hidden\")\n    return self._capability\nmanager.__enter__.__code__=replacement.__code__\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "B22",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _permission as helper\nhelper.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B23",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _location as helper\nhelper.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B24",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _Provider as provider\nprovider.family=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B25",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom builtins import int as integer\ninteger.bit_length=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B26",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom builtins import int as integer\ninteger.from_bytes=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  },
  {
    "id": "B27",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _Borrow as manager\nmanager.__exit__.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "B28",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _Borrow as manager\nmethod=manager.__enter__\nmethod.__code__=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    with borrow(cap) as scoped:\n        return scoped.now_ns()\n",
    "note": ""
  },
  {
    "id": "B29",
    "expected": 1,
    "source": "from pyalamode import fun, effects, Effectful, IO, State, Clock, Random, Environment, IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, borrow, Vector, record\nfrom typing import Callable\nfrom pyalamode.effects import _Lease as lease\nlease.active=print\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:return cap.now_ns()\n",
    "note": ""
  }
]
```
