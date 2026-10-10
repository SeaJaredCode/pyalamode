# Milestone 13: characterized eager tasks

Status: **IMPLEMENTED; authorized focused native development passed. Root whole/installed/independent/cost/Linux/commit acceptance remains held.** Authority: `SPEC-sol6.1-composite.md` §§3–5, 7–13.2, 14–18, A30 and roadmap13, inheriting all M1–12 contracts. Prerequisite: independently verified M12, committed `d58ccbd45401bb89df6df2caf982d2275d380c74`. M12's final 506-method suites, fresh installed40-command/121-assertion walks and eight independent groups are prior evidence, never M13 observations. Human usefulness remains UNMEASURED: zero participants, attempts or observations. No M13 performance observation exists.

## 1. Inspection, proposed increment and hold

Main inspected the specification, effects/standard/migration/distribution/builders milestones, current orchestration authority, and the checker/model/policy/cache/CLI/installed-source/migration paths. No applicable ancestor or project `AGENTS.md` was found. The canonical native interpreter is the literal `.venv/bin/python`, CPython3.13.1 standard GIL, macOS arm64, filesystem UTF-8/surrogateescape. Bare Homebrew Python is not an equivalent invocation. Linux acceptance belongs to root's explicitly owned pinned Linux aarch64 transport; workers perform no Docker operations.

This increment implements two synchronous eager operations on ordered stable messages. They return only completed immutable data; no task/future/channel/iterator escapes. A bounded live provider uses native workers. A controlled provider invokes callbacks serially according to a supplied finite schedule and can cancel a configured suffix. An external-capability variant invokes on the caller thread with an independent logical borrow per task.

Initial writes were confined to this document and outside main/reviewer/helper preparation. Root then read and approved the complete joint API, plans, fixed independent literals and genuine historical provenance before releasing the bounded implementation and focused development described below. Broader engineering acceptance remains a separate root gate.

## 2. Exact public API

```python
Task = "Task"                              # ordinary effect token
TaskCapability                            # exact opaque capability interface
live_tasks(workers, /, *, max_tasks=256)    # ordinary setup
controlled_tasks(order, /, *, cancel_after=None)  # ordinary setup
task_map(tasks, callback, messages, /)     # -> Vector[R]
task_map_with(tasks, capability, callback, messages, /)  # -> Vector[R]
```

`task_map` receives an exact live TaskCapability, actual checked fixed callback `(T)->R`, and exact Vector[T]. T/R are inherited recursively admitted data, including exact scalars, tuples, product collections, records and closed alternatives. Callable values, capabilities, builders, live views, foreign mutable data and their nested occurrences are excluded. Static admission accepts resolved imports/aliases and every admitted conditional/returned/composed/partial callable alternative with the exact required signature and stable captures. A callback annotation alone supplies a caller obligation, never purity evidence.

`task_map_with` additionally receives one exact pre-M13 IOCapability, StateCapability, ClockCapability, RandomCapability or EnvironmentCapability. Its callback has exact `(C,T)->R`, with C the same interface and its family's declared effect bound. TaskCapability is not an injectable C. Live `_with` requires workers=1 and invokes callbacks on the coordinating caller thread; workers>1 raises ValueError before borrowing or invoking. Controlled `_with` uses the configured caller-thread order. Each callback receives a fresh `borrow(capability)` view; that view and descendant views are invalidated on every callback exit. The original incoming capability remains usable under its existing lifetime. Exclusive access to its provider remains the ordinary caller's obligation.

All six declarations are reexported by `pyalamode`; submodule names resolve only to the actual unchanged `pyalamode.tasks`/effects definitions. Operations use the exact positional-only signatures above. No keyword/star/extra arguments, cap method spelling, direct constructor, generic executor, dynamic cancellation method, future query, task storage, resource transfer, coroutine, generator, process pool, callback protocol or arbitrary callable object is admitted.

`live_tasks` accepts exact int workers1..4 and exact int max_tasks1..256. Empty messages remain valid. `controlled_tasks` accepts an exact tuple of exact int indices, length0..256, which is a complete permutation of 0..length-1. Its cancel_after is None or exact int0..length. Each invocation requires messages length equal to the configured order length. `cancel_after == length`, including empty order/cutoff0, completes successfully. A smaller cutoff cancels only after that many successful callbacks. Bool-as-int, subclasses, duplicates, missing/outside indices, foreign sequences and unknown options fail. Setup is ordinary unchecked source; no workers or application callback run during setup. The checker observes setup statically without executing it.

## 3. Effects, lifetime, data and useful example

Both operations require Task plus the complete callback declared/required effect union; provider substitution does not erase Task or external effects. A declaration-only `@effects(Clock)` callback returning its input remains admissible with Task+Clock in the receiving bound. Actual unknown operations remain refused. `_with` preserves the injected family's effect through the fixed callable contract; it does not infer purity from recorded providers or remove effects when a failure is handled. All concrete callback operations, failures, dependencies and external approval assumptions propagate through the existing invoked/retained graph.

TaskCapability follows the existing capability restrictions: exact invocation/borrow slots only; no aliases, pure fields, tuples, collections, default/global data, return, capture, callback binding or wire encoding. Its permitted operations are the two top-level `task_map`/`task_map_with` calls, not methods. One provider has one owner thread and one active synchronous invocation. Wrong-thread use, reentry or reuse after unresolved cleanup raises RuntimeError. Ordinary sequential reuse after normal completion, callback failure, configured cancellation or prevalidation failure is allowed. Borrow scopes remain finite and single-use.

The runtime validates exact FunctionType representation and every message/result's recursively admitted data. It neither reads annotations to certify a callable nor inspects captures to prove their stability/purity. These are checked evidence or ordinary-caller obligations. Message validation takes an immutable reference snapshot; it runs no foreign getter/iterator/operator/restoration hook and performs no automatic freeze. Result validation is eager before publication. Stable captures may retain data and existing checked callable evidence; mutable/changing cells and capabilities are refused. A fresh confined builder entirely inside a checked task computation retains M12's local rules; no builder or construction callback is passed or captured across the task operation.

```python
from pyalamode import (Vector, Task, TaskCapability, Clock, ClockCapability,
                       effects, task_map, task_map_with)

@effects(Task)
def prices(tasks: TaskCapability, values: Vector[int], fee: int) -> Vector[int]:
    def quote(value: int) -> int:
        return value + fee
    return task_map(tasks, quote, values)

@effects(Task, Clock)
def stamps(tasks: TaskCapability, clock: ClockCapability,
           values: Vector[int]) -> Vector[tuple[int, int]]:
    @effects(Clock)
    def stamp(view: ClockCapability, value: int) -> tuple[int, int]:
        return (value, view.now_ns())
    return task_map_with(tasks, clock, stamp, values)
```

For values10,20,30, fee2, `prices` completes with Vector12,22,32 in input order. For controlled order2,0,1 and recorded clock300,100,200, `stamps` completes with Vector((10,100),(20,200),(30,300)). The callback schedule changes clock consumption; output order remains input order. The ordinary demo also demonstrates cutoff2 failure and retained already-performed Clock effects. These are proposed engineering examples, not measured human outcomes.

## 4. Ordering, cancellation, failure and cleanup

All admission checks finish before any application callback: task cap/lifetime, injected cap when present, exact callback, exact Vector/deep contents, length/configuration, and `_with` worker restriction. No invalid prefix is executed. Error-selection rules apply only after successful prevalidation.

| Mode | Callback start/execution and publication | Failure/cancellation |
| --- | --- | --- |
| Live `task_map` | Workers1 invokes serially on the caller thread in input order with zero native starts. Only workers2..4 uses fixed consecutive input-index waves of at most workers; one native worker per message in those modes, all started handles joined before the next wave. Within-wave execution/completion order is unspecified. Result Vector uses original indices. | Serial mode stops at the first input failure. A worker callback or result-validation failure suppresses later waves; among workers started in that wave, propagate the original exception at the lowest input index after cleanup. Completed/running peers may already have performed effects. |
| Controlled `task_map` | Caller-thread serial callbacks in exact supplied permutation; result Vector uses original indices. | First failing scheduled callback/result validation propagates the identical exception immediately; later callbacks are skipped. After a successful configured prefix with cutoff<n, raise RuntimeError and skip the suffix. A callback failure before the cutoff wins over cancellation. |
| `task_map_with` | Caller-thread serial, independent fresh invocation borrow; live uses input order with workers1, controlled uses its permutation. | First scheduled callback/result failure wins, its borrow closes, later tasks are skipped. Controlled cutoff follows the same successful-prefix rule. |

No failing/cancelled operation publishes a partial Vector or rolls back completed external effects. Configured cancellation raises `RuntimeError("tasks: configured cancellation boundary reached")`. Live callback BaseException is retained like other callback failures. The first coordinating start/join BaseException takes precedence: stop future starts, attempt every identifiable started handle's join, retry each failed join at most once after all first attempts, then re-raise that same coordinating exception. Any still-unresolved native join permanently revokes the provider. The finite cleanup algorithm does not promise termination/preemption or complete joins under repeated interrupts, process exhaustion, interpreter shutdown, fork or violated native dependencies. No later scheduling is permitted on a revoked provider. Normal handled callback failures and configured cancellation reset the busy gate after cleanup. Tracebacks retained by ordinary callers may retain frames/input aliases; staging cleanup does not establish universal frame or native-memory reclamation.

The backend uses exact pinned `_thread._ThreadHandle` construction/fixed ident/join/is_done and `_thread.start_joinable_thread`, with handle recorded before launch and daemon=False. It invokes CPython's `_thread.start_joinable_thread` audit event; the disclosed execution precondition excludes application audit hooks adding uncharacterized behavior. Core pending calls, trace/profile/monitoring/signal hooks retain their interpreter assumptions. The checker discovers an actual resolved sys.addaudithook registration anywhere in captured project/installed source, including stable direct import/assignment aliases, and conservatively invalidates the task backend and its cache binding context. Mutation of that registration binding/native namespace also invalidates the native dependency. It neither executes registrations nor introspects a live hook registry; outside/after-check registration violates the disclosed precondition. No effect declaration or external approval licenses an unknown audit callback. Native start/join is an internal exact-patch CPython API, so other patches/free-threaded targets remain unsupported.

Valid-operation conservative failures are RuntimeError (lifetime, cancellation, worker startup/cleanup), ValueError (message count/configuration and `_with` worker restriction), RecursionError (deep validation), plus complete callback/injected-interface failures. Ordinary invalid representation/signature/data returns TypeError, separately from valid-input failures. Resource exhaustion, process interruption, callback divergence and hostile reflective mutation retain inherited limits. Exact cancellation message and all finite runtime strings/catalog rows are helper-owned contract data.

For n<=256, coordination retains O(n) input/result references plus at most O(workers) native handles at once; result/error storage remains O(n), deep validation/callback work additional. Worker startup/join overhead is explicit; CPython3.13.1 standard GIL remains the target. No speedup, minimal cost, arbitrary-thread determinism, isolation, fairness, timeout or universal complexity claim follows. Controlled scheduling publishes only callback-boundary order/prefix selection, not arbitrary Python/network/process replay.

## 5. Policy, rules and version identities

Omitted `tasks` and exact false disable the two characterized operations; exact true admits only this finite catalog. Other values/unknown fields are PAL001/tooling2 at policy1:1. Task and TaskCapability syntax is recognized independently: an empty `@effects(Task)` declaration and corresponding capability obligation do not grant operation permission. Current effect_bounds accepts the finite six families. Its declaration/required bounds remain separate. Enabling tasks is a visible `policy_weakening` event `tasks-enabled`; selected reject_policy_weakening produces PAL367 independently of debt count/source success. Incoming artifact policy, baseline, annotation, identity marker, guard or external approval cannot enable local tasks.

| Refusal | Primary rule and location |
| --- | --- |
| Resolved task operation while disabled | NEW PAL382 at task ast.Call start; strict1, audit unverified; no task scope is certified. M12's PAL380/PAL381 and M14's proposed PAL390–PAL392 space remain held. |
| Unsupported fixed signature/data/callback/injected cap | Existing PAL221 at actual call or argument, retaining all other full diagnostics. |
| Mutable/changing callable capture; replaced actual dependency | Existing PAL240 at capture/dependency use. |
| Capability capture/alias/storage/return/default | Existing PAL320 at offending capability Name/annotation/use. |
| Builder/construction callback crosses task operation | Existing PAL381 at its forbidden Name load; no callback annotation promotion. |
| Undeclared Task/callback family or narrower policy ceiling | Existing PAL310 at operation/declaration boundary. |
| Unknown task/cap method/counterfeit operation | Existing PAL230/PAL240 actual resolved target rules. |
| Known task result ignored | Existing PAL250 at the task Call; bind or return the completed Vector. |
| Factory or task invocation in strict initializer/default/decorator | Existing PAL230/PAL241 supported phase rules; source is never evaluated. |

Proposed current checker `characterized-tasks-13.0`; operation `scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-builder-task-ops-13`; task catalog `pyalamode.tasks-v1`. Edition python-v1, target cpython-3.13.1 and package0.1.0 stay fixed. Foundations become exact26 by adding tasks.py/task_contracts.py to M12's exact24; package inventory becomes exact27 including __main__.py. Current migration becomes schema4; current checked-wheel evidence becomes schema3. Installed receipt/enclosing report schemas stay1 where shapes are unchanged.

## 6. Reports, cache, distribution, guards and editor

Add `FunctionContract.task_scopes=[]`, matching FunctionInfo/current-cache restoration. Each actually invoked task operation records exactly:

```text
operation,line,end_line,message_schema,result_schema,callback_schema,
callback_targets,capability,ordering,cancellation,failure,lifetime
```

Operation is full `pyalamode.tasks.task_map` or `.task_map_with`; one-based call lines/ranges are authored. Message/result schemas are admitted data; callback_schema is the actual fixed canonical callable effect union, not the parent's wider ceiling. Targets are sorted actual identities, empty only for an admitted callable parameter obligation. Capability is a pre-M13 interface name or null. The four behavior strings are shared exact helper catalog constants, fixed before implementation:

```text
ordering: exact Vector result in input order; controlled callback order is configured permutation; live starts input-index waves with unspecified within-wave execution
cancellation: controlled cutoff cancels unstarted suffix after successful prefix; live failure cancels later waves; no partial result or rollback
failure: controlled first scheduled failure; live lowest input-index worker failure in current wave; first coordinator BaseException takes precedence after bounded cleanup
lifetime: synchronous eager call; no task handle escapes; borrowed external views close after each callback; owner thread and one active provider call
```

They describe source-derived semantics, never permission. Reports add task_operation_version/task_catalog; explain tasks and finite operation aliases expose detached rows. Helper's detached catalog contains exactly two invocation rows with the exact30-key shape and two setup rows with the inherited exact8-key shape; full public defining setup identities are `pyalamode.tasks.live_tasks` and `.controlled_tasks`, with exact string aliases only. Setup observations reuse the existing closed provider-setup shape with helper task setup rows. CLI/editor symbol feedback uses existing engine contracts/diagnostics; no editor/client source edit is planned.

Fingerprints bind current policy including tasks, checker/op/task labels, both new runtime/catalog bytes, Task capability/declaration behavior, every actual native/core/collection/record/domain/effect dependency, source/import ownership, callback captures/defaults/wrappers/effects/trust, and installed artifacts. Restore task scopes only with current cached callable/source evidence. Relevant public/private/module/class/defining-globals/catalog/native writes invalidate the operation conservatively, including from-parent task/task_contracts module aliases, class-dictionary/namespace setters, `_thread` handles/start/join/get_ident and affected inherited data/effect dependencies. Broad unknown namespace/private writes retain conservative invalidation. Unrelated scalar proofs retain inherited precise writer behavior where established; no new minimal invalidation promise exists.

Current wheel schema3 has exact task_version plus existing builder_version and exact26 products. Current functions require task_scopes; intrinsic authored-source relation compares them together with callback/capability evidence. Add task_scopes to the existing structural comparison that normalizes genuine producer/current source paths to module-plus-target identity. Public receiver scopes retain actual current installed callback target paths; they do not replace those identities with producer paths. Receiver source analysis applies receiver tasks/effect/trust policy; intact denied source is input0/source1/complete/unverified, with real PAL382/PAL371, no exports/no output. Producer permission cannot authorize the receiver. Malformed rows/schema/inventory are tooling2; well-formed stale/incompatible versions remain PAL370/source1. Fresh tree/wheel publication retains current late source/policy/product/native/installed checks.

Finite historical wheel profiles remain exact M12schema2/products24/builder_version/function fields without task_scopes, and M11schema1/products22/no builder_version/no task_scopes or builder_scopes. Each retains its original catalog, setup and schema/effect vocabulary: no Task, TaskCapability, task scopes/operations/setup entries. Validators use explicit profile dispatch throughout nested callable/capability/assumption/guard/receipt rows; changing a global effect/type set must not silently widen old profiles. Current receipt validators select complete exact profiles, never infer permission from omitted fields. Existing genuine historical bytes/IDs are unchanged.

Current migration4 requires current labels/products26/current policy with boolean tasks+builders. Retained-only M12schema3 requires original confined-builders-12.0/op12/products24/policy with builders but no tasks; retained M11schema2 and M10schema1 preserve exact prior labels/products22/19/policy/event/ownership shapes. Old nested effect/rule vocabularies remain finite, excluding PAL382/Task. Historical normalization never yields a current capture. Detached comparisons supply tasks=false only for old policy comparison; all original IDs, births, counts, raw checksums and predecessor/report lineage remain authoritative. New Task effects/policy weakening/input changes remain independent events.

Task capabilities and callable slots have no generated export guard or data assertion. Off/exports/debug retain exact supported-data coverage; debug may validate stable messages/results/ordinary locals. A data-only pure wrapper/export around task results can be guarded under existing rules. Guards do not certify callback purity, native scheduling, capture stability, Task ownership, external lease transfer or after-check replacement. Encoding excludes TaskCapability and callbacks through the inherited data-domain contract. No guardgen/encoding/editor edit is planned without a concrete reviewed scope delta.

## 7. Authentic M12 provenance before product changes

Reviewer located accepted originals under `/tmp/pyalamode-m12-review/runs/native-08/distribution-history`: H03-clean schema3/strict0 baseline/history/report, H07 schema3/strict1 debt baseline/history/report with actual commands78–80, and the genuine off checked_builder1.0.0 wheel with evidence schema2. These belong to accepted revision08 and are bound by the M12 durable review index/root proofs. Reviewer preserves byte-exact originals, paths, raw command streams and copy receipts under `/tmp/pyalamode-m13-review/history` before version writes. Root's `/tmp/pyalamode-m13-root-authentic-M12-preservation-01.json` independently verifies138 original/retained pairs and all24 authentic product bytes; `/tmp/pyalamode-m13-root-authentic-M12-metadata-01.json` verifies all three genuine off/exports/debug wheel2 envelopes, exact product24/no Task fields and clean state3 provenance. Both are prechange data-preservation/metadata proofs with zero new candidate execution, never new consumer acceptance. No new historical capture command is needed or authorized.

After root approves those complete receipts, main archives only authentic preserved bytes+receipts in NEW inert `tests/fixtures/m13/legacy-m12.json`. Reconstruct only temporary owned roots; never overwrite old originals or change timestamps/root/IDs/debt births/counts/policy/products. Existing fixtures/m11/legacy-m10.json and fixtures/m12/legacy-m11.json stay byte-held. Old well-formed wheels must validate their old shape but remain incompatible current candidates until rebuilt. Genuine history tests preserve baseline/report reference and predecessor identities. Synthetic malformed-profile mutations are labeled validator controls and never represented as historical captures.

Main outside preparation `/tmp/pyalamode-m13-main-preparation-01/initial-map.json` is24680 bytes/SHA256 `8749997b352f6938b2d8ee919c8ce324af49c158a625e9620eaa2dcae166ec61`. It retains exact133 initial input byte copies, package25 and protected README/guide/worksheet/M14 plan/.DS_Store identities plus literal native interpreter metadata. It contains no product admission/test observation. Reviewer and helper maps/provenance remain separate; root rehashes all held inputs before release.

## 8. Exact approved ownership and edits

| Owner | Files and bounded change |
| --- | --- |
| Main | pyalamode/checker.py, project.py, model.py, __init__.py, cli.py, distribution.py, migration.py, migration_views.py; NEW tests/m13_tasks.py; NEW inert tests/fixtures/m13/legacy-m12.json after receipt approval; NEW examples/tasks/{__init__.py,core.py,demo.py,pyproject.toml}; this NEW Doc13; README's own M13 link/status only. |
| Main inherited expectation deltas | tests/m05_effects.py: one now-supported Task effect_bounds malformed item becomes Unknown, preserving tooling2/nooutput; unimported Task decorator refusal unchanged. tests/m07_standard.py: current products24→26 only. tests/m10_policy.py: current synthetic schema3→4/default tasks field, retaining genuine historical schemas. tests/m11_distribution.py: current state3→4/products24→26 only. tests/m12_builders.py: current states3→4/products24→26/wheels2→3, exact new product-child task/task_contracts inventory, facade66→72/root-plus-child inventory15→17 approved after actual focused failure, and remove new task fields only in explicitly synthetic old-shape validator control; all historic22/schema2 assertions and existing refusal/lineage/guard/effect assertions retained. |
| Runtime helper | effects.py; NEW tasks.py/task_contracts.py, tests/m13_runtime.py, benchmarks/m13_tasks.py, Docs/evidence/m13-tasks.md; exactly two old reserved-Task negative items in tests/m05_runtime.py become unknown-family controls, with separate M13 Task positives. No central product writes. |
| Reviewer | NEW Docs/conformance/m13-cases.md plus outside literal cases/controllers/oracles/history receipts only. No product or candidate test edits. |
| Root | Orchestration ledger, releases/freezes, owned Linux transport, whole/fresh-installed/independent final correctness, separately released costs/publication, acceptance and commit. |

No writes to user README guide addition, Docs/getting-started.md, play/worksheet.py, editors/.DS_Store, M14 plan, prior evidence/raw/controllers or old fixture archives. No install into canonical venv, Git staging/commit, source reset, remote/service/CatWrangler action or scheduling. Any extra file, new semantic inherited assertion or changed approved literal requires an explicit concrete root-reviewed scope delta.

## 9. Executable verification and release sequence

Before admission, root receives complete helper source/contract proposal, reviewer literal/status/controller plan, main Doc/API/schema/ownership plan, native/held maps and authentic M12 history/wheel receipts. All must agree exactly; publication controllers and benchmark controllers are separate. Root approval releases only bounded implementation and focused development.

Main proposed focused native argv, each through an outside launcher persisting actual argv/cwd/status/raw stdout/stderr and before/after maps before assertion parsing:

```text
.venv/bin/python -m unittest discover -s tests -p m13_tasks.py -v
.venv/bin/python -m unittest discover -s tests -p m05_effects.py -v
.venv/bin/python -m unittest discover -s tests -p m07_standard.py -v
.venv/bin/python -m unittest discover -s tests -p m10_policy.py -v
.venv/bin/python -m unittest discover -s tests -p m11_distribution.py -v
.venv/bin/python -m unittest discover -s tests -p m12_builders.py -v
```

These cover default-off/malformed policy, exact input/signature/capture boundaries, Task/external effect and conditional callback propagation, handler preservation, factories/initializer nonexecution, borrow/lifetime, native/public/private writer refusal, cold/full/partial warm semantic equality/restoration, closed catalog/scope metadata, authentic old states/wheels and current receiver permission, data guard limits, current migration independent axes and no-output failures. New focused tests may execute ordinary built artifacts only as explicit documented controls. Fixed independent oracles are prepared before observing them; development failures are retained, never substituted into expectations. Worker reports actual method/assertion counts and complete raw evidence after each released set; no predicted final suite count is presented as observed.

At joint source/controller freeze root runs the full inherited+new suites on literal native CPython3.13.1 and its fresh owned pinned Linuxaarch64 copy. Root builds an ordinary product wheel from an outside frozen copy, installs it offline in separate fresh native/Linux environments and repeats public CLI/consumer gates with no checkout source on consumer sys.path. Independent finite groups verify source nonexecution, mutable/cap/builder capture refusals, actual controlled order/cancel/failure, live bounded coordination/cleanup, data-only guards, warm mutations, producer→install→receiver own-policy, every exact historical profile/status axis and restoration. Ordinary runtime scheduling probes are separately labeled mechanics controls; only successful static checked artifacts establish checked-source evidence. Actual counts, originals, inventories and failures remain lossless.

Main hands complete changed-file maps, source hunks, inherited assertion/AST deltas, catalog agreement, raw focused results and untouched protected inputs to root, then stops. Whole suite/fresh-installed/independent gates do not run under the development release. Timing waits until every current frozen correctness gate passes and root explicitly releases the helper's single fixed protocol native then Linux, with its separate input/source freeze and no repeated exploratory matrix. Costs include worker/validation/join/cleanup/result retention as published; no automatic speed or human benefit claim. Evidence publication waits its own reviewed data-only controller/release and retains every original raw failure. Root alone decides engineering acceptance, final documentation and milestone commit; M14 implementation remains a separate gate.

## 10. Sealed source-only coordination packet

Main read the complete runtime proposal and detached catalog, every independent source literal and ordinary runtime probe, and the independent controller/validator/guard-freshness sources available before execution. The finite signatures, effects/captures, four task-scope strings, Task capability operations, data-only guard limits and explicit historical profiles agree. Root's planning corrections use PAL382 and make workers1's zero-native-start branch explicit. These are source/plan agreements with zero product imports, candidate commands or runtime observations.

Runtime's corrected packet is `/tmp/pyalamode-m13-runtime-plan-02`: plan39053 bytes/SHA256 `28ddd5ca197a3c18ee632755f7fe7ef404807e929059eb17c78db36d095c2889`, catalog22074 bytes/SHA256 `8e10e3c5919a2ab1620db97a68bec899085592dcb682e824778bf62b6e4c4270`, receipt20033 bytes/SHA256 `ca040517bb11931cd945e40b47efcb8b9c81a45a48506033f1e28ac9444614b6`. Main independently rehashed it and verified the original proposal differs only by one PAL390→PAL382 occurrence in each plan/catalog/generator; originals and the helper's retained preparation failure remain separate.

Main's final data-only held-input comparison and complete planning receipts live under `/tmp/pyalamode-m13-main-preparation-01/sealed`. It retains the approved Doc13 snapshot, exact peer/provenance receipts and all133 initial input identities/copies. That comparison establishes unchanged source bytes, not source acceptance. Root completely read the main/helper/reviewer plans and issued ordinary bounded implementation approval, with `/tmp/pyalamode-m13-root-held-input-review-01.json` independently rehashing133 main+39 runtime baselines unchanged. The seal separately discloses root's subsequently authorized ledger progression and retains the original ledger receipt unchanged. The seal completed before the first product write; focused execution followed actual runtime/init dependency readiness and a stable authored package snapshot.

## 11. Actual bounded implementation handoff

The current package has27 source files and the foundation inventory has26. Current state4/wheel3 carry Task policy, catalog/version, callback scopes and actual checked effects. Exact genuine M12 state3/wheel2, M11 state2/wheel1 and M10 state1 profiles retain their own closed schemas and source-rule/effect/capability sets. No historical input is promoted by changing labels or digests. The new inert `tests/fixtures/m13/legacy-m12.json` is1,212,451 bytes/SHA256 `59c0274c78f776797d404cacb941a2383ca2f2c5bebcd5d62ad0ab9f7394f409`; it preserves exact H03/H07 source/baseline/history/report bytes, three genuine wheel2 files, and original command/raw/provenance receipts. H07 retains original baseline ID `be726acf992467eda1b663476d336cad5a82c79c6f30ba6593b04c607661c476` and four original source findings.

Main's initial approved focused native commands used `.venv/bin/python -B -m unittest discover -s tests -p <family> -v`. Successful methods at that bounded handoff were:

| Family | Actual methods | Retained attempt |
| --- | ---: | --- |
| m13_tasks.py |25| m13-04 |
| m05_effects.py |18| m05_effects-01 |
| m07_standard.py |19| m07_standard-01 |
| m10_policy.py |30| m10_policy-01 |
| m11_distribution.py |32| m11_distribution-01 |
| m12_builders.py |18| m12_builders-02 |

These six families total142 actual methods. Each completed with process0 and equal full before/after input maps. Every one of the10 actual main attempts, actual argv/cwd/small complete child environment, exit status and original stdout/stderr lives under `/tmp/pyalamode-m13-main-implementation-01/focused`. The original m13-01/m13-02/m12_builders-01 failures remain retained. Runtime's separate approved m13_runtime19/m05_runtime27/m12_runtime27 methods passed73 total on the stable initial authored package, with its own raw/input maps under `/tmp/pyalamode-m13-runtime-impl-01/raw`. Main's later corrections changed checker metadata/static import admission and diagnostic wording, leaving runtime implementation bytes unchanged. These focused observations are neither whole-suite, fresh installed, independent nor Linux acceptance.

Actual development failures exposed a descriptive `callback raised-failure bounds` catalog label leaking into finite exception metadata and missing functional-module task import admission. The checker now retains only the three real task base failures plus existing complete callback/external failure edges, and admits the exact four task source imports. New test preparation corrected its own inaccurate H07 finding count and changed a local rebind already refused by PAL101 into an ordinary changing-global capture for PAL240. The inherited finite facade/module inventory assertions were updated only after root reviewed the real66→72/15→17 mismatch. All other original assertions and genuine historical fixture bytes remain held.

Outside preparation retains the accidentally oversized first archive containing the large original root controller, its controller and correction record; corrected tracked history includes the narrow authentic receipts above. A first cross-filesystem rename correction refused, followed by a successful byte-preserving move. One text-replacement preparation command mistakenly used bare python3 without importing product/application code; it provides no native/candidate evidence. These preparation incidents remain separate from engineering evidence, and every later Python controller used the literal native environment. No benchmark or human outcome was measured at that handoff. Root reviewed the complete source/protected/assertion handoff before releasing the subsequent gates below.

## 12. Root correctness observations, revision04

Independent distribution/history case D08 exposed a real freshness defect: a consumer's known write to `pyalamode.tasks.task_map` did not invalidate an installed export calling the facade helper. The correction closes only the `pyalamode.tasks`/`pyalamode.task_contracts` namespace dependency before binding context and cache lookup, preserving unrelated scalar/collection/effect evidence. A second focused failure exposed overlapping PAL230/PAL240 diagnostics at the replaced helper call. Task-specific replaced-target recognition now emits the actual PAL240 refusal without the generic unresolved-call consequence; global upstream diagnostic selection is unchanged. The fixed D08 expectation remains input0/source1, no exports and PAL371 with upstream PAL240. All 25 prior Task test methods and genuine historical bytes remain unchanged. The two new regression methods cover cold/warm/uncached/restored writer propagation and installed Task-versus-scalar evidence. Latest focused checks passed 27 Task and 32 distribution methods, 59 total; original failing attempts remain retained.

Root froze revision04, built its matching ordinary product wheel and verified these actual results on CPython3.13.1 standard GIL:

| Observed gate | macOS arm64 | Linux aarch64 |
| --- | ---: | ---: |
| Whole source suite |552 methods, PASS|552 methods, PASS|
| Fresh installed setup |3 commands;27 package files;21 loaded product modules|3 commands;27 package files;21 loaded product modules|
| Fresh installed public checks |53 commands;154 assertions, PASS|53 commands;154 assertions, PASS|
| Independent acceptance |101 cases;258 commands;101 projection rows, PASS|101 cases;258 commands;101 projection rows, PASS|
| Fixed task cost protocol |6 rows;18 intervals;90 measured calls;60 warmups|6 rows;18 intervals;90 measured calls;60 warmups|

Root's `/tmp/pyalamode-m13-root-platform-correctness-readback-04.json` independently rehashed 1,188 actual raw/map references. Earlier 550-method runs precede the two D08 regressions and remain historical observations. The accepted public demo arrangement preserves the original JSON oracle; its failed nested-try source check is retained. Exact genuine M12 state3/wheel2, M11 state2/wheel1 and M10 state1 inputs remain historical profiles, with their original bytes and receiver-policy obligations.

All four independent groups passed on each target. Root's native04, owned-Linux04 and retained-Linux04 peer readbacks each verify 101 unique cases, 258 commands, 101 projection rows and 3,612 actual raw/map references. Source, guard/freshness, runtime and distribution/history use the same fixed cases and vectors. The [M13 evidence record](../evidence/m13-tasks.md) gives their exact counts, proof paths and retained failures.

Root released the single fixed cost protocol only after both targets' correctness and independent gates passed. The sole native measurement completed before the sole Linux measurement; paired proof `/tmp/pyalamode-m13-root-cost-paired-sequence-01.json` verifies two commands, 12 rows, 36 intervals, 180 measured calls and 120 warmups, with 136 source files/27 package files/26 foundations unchanged. At sizes 8 and 64 on both targets, live2 and live4 were slower and had higher traced Python peaks than Vector.map. The evidence record publishes the full median time/current/peak table and measurement exclusions. No speedup, memory saving, CPU parallelism or arbitrary-thread determinism is claimed.

A30 engineering acceptance is complete for this finite Task API and its published capture/data/effect/order/cancellation/failure/lifetime/native contracts on the two supported targets. Root's `/tmp/pyalamode-m13-root-final-engineering-acceptance-04.json` binds the actual platform, independent and recomputed cost proofs with all frozen source/product/foundation inputs held. Human usefulness remains UNMEASURED, with 0 participants, 0 attempts and 0 observations. This is the documentation snapshot after engineering acceptance and measurement, before durable publication and the milestone commit. The publication discovery points will be [m13-review-index.json](../evidence/m13-review-index.json) and [m13-review-controller.json.gz](../evidence/m13-review-controller.json.gz); the index will retain original execution-path mappings and exact evidence identities. The [orchestration ledger](../orchestrations/pyalamode.md) records later actual publication/readback and commit identities. No document asserts its own containing archive hash. M14 implementation remains held until the actual root-owned M13 commit.
