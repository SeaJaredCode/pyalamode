# Milestone 5: checked effectful shells

Status: implementation and frozen two-platform engineering verification complete; product/test/example source remains frozen for root-owned final acceptance and Git staging. Authority: `SPEC-sol6.1-composite.md`, especially §§3–5, 9, 11 and A17–A18/A32; prerequisite M4 commit `7c201ab`. Root owns final verification, ledger and Git. This catalog precedes static admission.

The compatible API adds identity `@effects(IO, State, Clock, Random, Environment)` declarations. Each effect token is an ordinary fixed string. An effect declaration selects checked source, alone, alongside `@fun`, or inside module mode; each family occurs at most once. The function keeps single assignment and immutable ordinary data. `fun` and effects declarations return the identical function, without registration, wrapping, metadata mutation or invocation enforcement. Task remains reserved for M13 and is refused. An effect declaration never admits an unknown operation.

Pure `Callable[[T,...],R]` retains its existing contract. `Effectful[[T,...],R,Clock,...]` names a fixed positional callable upper bound. Exact capability parameter slots are supported only when the corresponding family is included. The operation's own effects and every concrete/conditional callback upper bound are united. A pure caller cannot invoke a declared effectful function even if its body currently performs no operation. Concrete target bounds may tighten receiving callback bounds; annotations alone never establish actual callable evidence for analyzed callers. Capabilities cannot be callable captures.

## Finite capability operations

| Exact opaque interface | Allowed operation/signature | Effect | Result |
| --- | --- | --- | --- |
| IOCapability | read_text(exact relative path str) | IO | exact str, UTF-8 whole-file read |
| IOCapability | write_text(exact relative path str, exact text str) | IO | None, UTF-8 whole-file replacement |
| StateCapability | get(); set(exact int) | State | exact int; None |
| ClockCapability | now_ns() | Clock | exact int nanoseconds |
| RandomCapability | below(exact int bound) | Random | exact int in [0,bound); nonpositive bounds fail |
| EnvironmentCapability | get(exact name str, exact default str) | Environment | exact str |

Provider construction remains ordinary unchecked setup. Named live and recorded providers retain the same interface effects. Recorded providers characterize finite recorded inputs and exhaustion, not arbitrary process/network determinism. Direct builtin/stdlib operations, callback hooks, implicit dispatch and provider constructors inside strict invocation/default/initialization remain unsupported. State is a private exact integer cell, not admission for arbitrary mutable application objects. Library snapshot adapters retain their ordinary-shell classification.

IO uses rooted relative paths and internally opens, reads/writes and closes each file, including body-failure cleanup. Its runtime contract publishes allowed operation scopes, path and symlink assumptions, and failure categories. It is not a security sandbox. `with borrow(capability) as scoped:` is one finite characterized context manager for a logical lease; it invalidates the borrowed view at exit and does not expose or claim a persistent OS reader. Persistent readers, sessions, arbitrary context managers and resource-transfer syntax are unsupported.

Capability parameters are invocation borrows. Explicit calls to checked functions and fixed Effectful callbacks may lend a capability to an exact corresponding parameter, for the duration of that call. Live capabilities cannot appear in ordinary data, defaults, global constants, returned stable values, aliases or captured cells. Scoped names cannot be used outside their borrow suite or overwritten by subsequent bindings; nested borrowing is finite. Ordinary callers must supply the exact supported live interface, allowed operations and lifetime, and preserve the provider/runtime dependencies. Selected export guards refuse capability and callback schemas; debug assertions cover supported data only.

Project `effect_bounds` maps exact `module:function` selections to finite effect-family lists. A source declaration cannot exceed that entry bound, and actual required effects must fit the declaration. Effects, trust, failures, source initialization and freshness are separate report dimensions. Unknown effects, Task, unknown selectors and malformed policy remain refusal/tooling failures. Source check/build never imports or evaluates application code.

## Implementation, evidence and limits

Frozen tests, independent review and actual generated-artifact measurements are complete as recorded below. Main worker owns checker/model/project/CLI/package exports, static tests/examples/README and this report. Runtime helper owns new `effects.py`, runtime tests, benchmark and runtime contract/measurement evidence. Independent reviewer owns conformance observations. Runtime operation costs and retained state were published before freeze; actual target-user measurements remain unmeasured.

## Frozen static implementation and evidence

Main product/test/example source is frozen for root-owned final acceptance. The complete frozen suite passes **194 tests** (149 inherited, 18 new static/build and 27 new runtime). `git diff --check` passes. Final independent corpus, two-platform suite, artifact walkthrough and runtime measurements are recorded below from unchanged-source runs. Actual target-user outcomes remain unmeasured.

The checker is `effects-capabilities-5.1` with operation contract `scalar-tuple-call-collection-record-boundary-effect-ops-5`. It records `effect_bound`, `required_effects` and per-family origin paths. Concrete invocation edges use `invoked_targets`; supplied/retained callable targets use separate `callable_dependencies`, `callable_arguments` and `callable_operations`. Retaining or returning an effectful callable can remain pure when it is not invoked, while its target/dependency/trust assumptions stay visible. These reference operations describe relevant callable vocabulary, not specialized generic invocation. Concrete and conditional captured/returned callable evidence retains target identities, exact bound, conditional failure status and capture metadata across partial warm dependency reuse. Callable type merges canonicalize finite effect unions, preventing a warm cache from losing a conditional alternative or widening a known returned target to its annotated bound.

The finite graph unions callee declared bounds even when a callee's observed required set is smaller. Direct operations and callback invocation require the receiving declaration; source declarations also fit selected project `effect_bounds`. Unknown target/operation/schema stays unverified. Recursive graph failure propagation remains distinct from effect propagation. Audit, failed source and failed dependency evidence publish no certified behavior bound. Ordinary module initialization stays unchecked; functional module source initialization stays a separately checked dimension. Product setup imports establish trusted catalog/classes, not provider operation results; live random uses direct `os.urandom` rejection sampling and does not import a module that seeds random state at product import.

The ten product foundation Python files, including `effects.py`, participate in fingerprint/build freshness. The small `__main__.py` launcher is separately covered by the full independent source snapshot; it is not one of these ten foundation identities. Source, policy, target, operation/checker identities and analyzed binding writers remain included. Finite `EFFECT_FOUNDATIONS` inventories actual implicit runtime dependencies without licensing calls to those names. Public class/method and private helper/class/method aliases preserve mutation identity through code, setter/deleter and class-dictionary routes. Private effect helper imports may reach existing record/collection machinery; their behavioral replacements conservatively invalidate the whole product. Record/boundary helper replacements also invalidate relevant effect foundations. This conservative scope is disclosed and does not promise minimal cache invalidation.

An analyzed capability value carries interface, allowed operations, provider origin and lifetime evidence. Bare capability slots require the full interface operation set, including both IO read/write operations; minimal callee permissions are not inferred. Known narrowed/closed/unknown shell operations cannot establish that slot. IO factories require the explicit keyword `allowed_ops=("read_text","write_text")` (either order); ordinary narrower subsets are usable only under their ordinary runtime permissions. Unknown ordinary annotations establish no actual capability. Uncharacterized shell use conservatively invalidates existing provider aliases before later checked lending. This is static finite evidence, not a live runtime registry.

Use `from pyalamode import names` or `from pyalamode.effects import names`. Stock Python binds `import pyalamode.effects as e` to the package's exported identity function. The checker supports that actual marker binding as `@e(Clock)` and refuses nonexistent namespace behavior such as `e.effects` or `e.ClockCapability`.

## Failures, cleanup and costs

| Family/operation | Conservative valid-operation failure vocabulary |
| --- | --- |
| IO read/write interface | OSError (including permissions/symlinks), UnicodeError, ValueError, RuntimeError; recorded reads also KeyError |
| State get/set | RuntimeError for invalidated logical lease |
| Clock now_ns | IndexError at recorded exhaustion; RuntimeError lifetime; conservative OSError |
| Random below | ValueError for bound/recorded sample, IndexError at recorded exhaustion, OSError entropy, RuntimeError lifetime |
| Environment get | ValueError name, UnicodeError encoding, RuntimeError lifetime; conservative OSError |
| Borrow entry/exit | RuntimeError invalid/reused/expired lease |
| Conditional callable | Inherited pure IndexError/KeyError/ValueError/ZeroDivisionError/RecursionError union relevant declared family failure vocabularies |

Unsupported ordinary exact types use TypeError and lie outside admitted input contracts. Definition/default/setup failures remain separately disclosed. Borrow exits preserve body exceptions; whole-path IO uses actual builtin open/context/read-or-write/close cleanup and can propagate ordinary close errors. Writes are non-atomic and may leave partial/truncated content after failure. Logical borrowing does not promise OS stream ownership, exclusivity or synchronization. Persistent reader/session transfer, arbitrary dispatch, handlers, Task and later milestones remain unsupported.

The [runtime contract](../evidence/m05-runtime-contract.md) publishes source costs and storage. Logical liveness/cycle checks are O(h²) for lease depth h, with O(1) fresh view/lease and parent-chain retention. Recorded name/value setup is O(n²) duplicate checking; lookup/write is O(n) plus scalar lengths, and writes copy tuples. Live IO includes path-component system calls and UTF-8 text work; external filesystem latency is uncontrolled. Live random uses expected fewer than two rejection-sampling draws under independent uniform OS entropy, with no fixed retry/termination bound. These are algorithm/storage statements, not measured production latency.

## Commands and handoff

```sh
.venv/bin/python -m unittest discover -s tests -p 'm0*.py'
.venv/bin/python -m pyalamode check examples/effects --no-cache
.venv/bin/python -m examples.effects.demo
.venv/bin/python -m pyalamode explain effects
.venv/bin/python -m pyalamode explain Effectful
.venv/bin/python -m pyalamode explain borrow
.venv/bin/python -m pyalamode explain capabilities
.venv/bin/python -m pyalamode check tests/fixtures/m05/undeclared.py --no-cache
```

The effects example selects seven functions and two functional modules. Its ordinary demo prints `(1000000, 0) (1000100, 1) 100 3 run demo`, showing recorded clock progression, explicit higher-order capability lending, scoped borrowing, state update and retained Random/Environment/IO interfaces. Setup and final shell output remain ordinary unchecked work.

M6 can extend the characterized failure vocabulary/handling and closed alternatives without erasing effects or exporting exception/traceback state. M7 can expand operation/initialization contracts deliberately; M8 can consume retained concrete callback assumptions as external operation trust is introduced. Existing snapshot conversions remain ordinary-shell operations; declaring an effect does not admit mutable inputs or arbitrary conversions. Selected guards still protect only supported data assumptions. No later milestone, ledger edit, commit, schedule, CatWrangler workflow or additional delegation was performed by this main worker.

## Final verification and measured engineering costs

The independent [M5 conformance report](../conformance/m05-cases.md) passed **175 literal source cases and 332 focused assertions on each platform**: 142 runtime, 45 project/guard/sentinel, 32 actual CLI, 93 freshness and 20 cold/full-warm/partial-warm callback assertions. It independently passed the complete 194-test suite on macOS in 2.741 seconds and actual installed-package Linux in 9.394 seconds. Its complete 35-entry product/test/example/fixture/benchmark/reviewer source maps match before/after, cross-platform and current source. Earlier review gaps in namespace binding, capability tuple data, private nested helper method writers and exact warm callback evidence were resolved at source before the final freeze; there is no remaining blocker.

Root independently passed the same frozen **194 tests** on native CPython 3.13.1 macOS (3.259 seconds) and actual `python:3.13.1-slim` Linux (10.087 seconds). Its installed CLI walkthrough checks/builds/executes all five capability families, explicit higher-order capability slots and scoped borrowing; the unchanged off artifact runs through ordinary Python, with no specialized loader or callback/purity registry. Rooted IO reads/writes, state progression and recorded clock/random/environment behavior passed. Each shipped negative example fails with status 1 and no artifact: undeclared capability effect, nested capability data escape and unknown operation despite declared effects. A restrictive entry effect policy also fails before publication. Six finite explanation commands passed, and source snapshots remained unchanged.

The runtime helper's [measurement report](../evidence/m05-runtime-measurements.md), [macOS JSON](../evidence/m05-runtime-macos.json) and [Linux JSON](../evidence/m05-runtime-linux.json) cover ten conditions at sizes 100 and 1,000, three trials and 25 calls per trial: **20 rows, 60 measured intervals and 1,500 measured calls per platform**, plus 200 excluded warmup calls. All correctness obligations passed. Actual off builds/imports preserve function code/identity; an explicit Effectful ClockCapability callback smoke returns 7. All ten product foundation identities and four owned runtime/test/harness identities match before/after, cross-platform and current source, independently checked by root. Artifact identities remain separate from source/foundation maps and environment paths.

Representative n = 1,000 median microseconds per call and maximum traced peaks are:

| Condition | µs/call macOS / Linux | peak bytes macOS / Linux |
| --- | --- | --- |
| State two gets/one set | 5.377 / 7.372 | 384 / 384 |
| Same State work in one borrow | 27.435 / 34.832 | 968 / 968 |
| Live Random below 1,000 | 7.033 / 7.695 | 367 / 367 |
| Recorded Environment, selected last of 1,000 entries | 264.678 / 293.818 | 456 / 456 |
| Live IO write/read 1,000 UTF-8 bytes | 155.355 / 138.335 | 11,162 / 9,936 |

These heterogeneous intervals include Python call loops, provider operation/validation/allocation and `tracemalloc`; they exclude builds/imports/setup/warmups/correctness/JSON work. Peaks are traced Python allocation, not RSS. Live results, system load, scheduling and OS/filesystem caches are uncontrolled. Sizes have condition-specific meanings, and live Clock/Environment operations have no size parameter. The observations do not estimate untraced application latency, universal speed, deterministic live behavior or target-user authoring costs. Full per-condition observations and limitations remain in the linked runtime report.

Both platforms use actual CPython 3.13.1 standard GIL builds. macOS ran Apple M1 Pro arm64, ten logical CPUs, 16 GiB memory, macOS 26.6.2 and Clang 16. Linux ran actual `python:3.13.1-slim`, aarch64 LinuxKit/glibc 2.36 and GCC 12.2, five visible logical CPUs and about 8.23 GB visible memory, with no reported cgroup maximum. No product/test/example/harness source changed after the agreed measurement freeze. Documentation reconciliation is separate from that source evidence. Root owns the final ledger, Git and release decision.
