# Orchestration: Pyalamode local build

**Status**: active
**Designer**: none
**Scope source**: Implement SPEC-sol6.1-composite.md locally, using the reviewed fourteen-milestone order, parallel subagents for independent work, and a commit after each verified milestone.
**Watcher**: none
**Watch until**: none

## Completion criteria

- Installable local checker/library and compatible artifacts implement the in-scope specification.
- Each milestone has independently inspected code, passing relevant acceptance/adversarial tests, documentation, and a recorded commit.
- Core milestones 1–11 are usable without optional extensions, runtime certification services, or CatWrangler.
- Extensions 12–14 retain separate gates; unsupported behavior fails closed and limitations remain explicit.
- Full local suite, command walkthrough, and separate-package consumer verification pass. Platform claims identify actual tested environments.

## Work queue

- [x] 1. Statically checked scalar functions
  - State: complete
  - Task: /root/m01_scalar
  - Depends on: none
  - Acceptance: A01–A08, A33; closed scalar vocabulary; no user-code evaluation; successful ordinary execution.
  - Evidence: Final frozen tree independently passed 24 tests on macOS (0.966s) and Linux (1.347s); 25 independent probes and 17 accepted/22 rejected expressions; 14 guide commands; installed CLI build/run/rejected-build walkthrough; named macOS/Linux benchmark JSON. Code commit: 7d694e0.
- [x] 2. Functional modules
  - State: complete
  - Task: /root/m02_modules
  - Depends on: 1
  - Acceptance: A09–A10; initialization, stable constants/captures/defaults, checked graphs and recursion.
  - Evidence: Frozen50-test suite passed macOS1.292s/Linux2.329s; independent83 source cases,20 project layouts,6 warm transitions clean; actual warm body-analysis skip verified; CLI ordinary build/run and negative no-output gates. Named26-file/208-function/320-edge measurements recorded separately. Commit ca3db3f.
- [x] 3. Persistent collections
  - State: complete
  - Task: /root/m03_collections
  - Depends on: 2
  - Acceptance: A11–A13; nested invariants, retained versions, traversal/callback safety, published costs/trust.
  - Evidence: Frozen93-test suite passesmacOS1.508s/Linux3.646s; independent113sourcecases,11projectlayouts,namespace/cache/backendbytefreshness and262runtimeassertions×3seeds clean; hugeint43focusedchecks/hookzero and8foundationwritergates clean. Ordinaryunchangedbuild/run and3negativebuildnooutputgates verified.36runtimeconditions/108intervals perplatform at100/1000/10000, actualretention/updatecosts andmatchingfinalsourceidentities published. Commit1675e94.
- [x] 4. Records and boundaries
  - State: complete
  - Task: /root/m04_records; runtime helper /root/m04_runtime; independent reviewer /root/m04_review
  - Depends on: 3
  - Acceptance: A14–A16, A34–A35; independent snapshots/exports and selected guard coverage.
  - Evidence: Frozen149-test suite passes macOS2.491s/Linux7.591s; root39 CLI/ordinary execution/failed-build gates and3 shipped negative fixture no-output builds clean. Independent93 literal sources,99 runtime assertions,49 guard assertions and42 project layouts/168 assertions pass on both actual platforms with unchanged/cross-platform source maps. Actual generated guard counts0/2/28 over8 direct internal leaf calls;10 runtime conditions/30 intervals/750 calls per platform and all9 current product digests independently inspected. Final conformance/handoff/cost documentation inspected. Commit7c201ab.
- [x] 5. Checked effectful shells
  - State: complete
  - Task: /root/m05_effects; runtime helper /root/m04_records; independent reviewer /root/m05_review
  - Depends on: 4
  - Acceptance: A17–A18; finite effects, capability lifetime, unknown-operation rejection and provider classification.
  - Evidence: Frozen194 suite passes native3.259s/Linux10.087s. Root installed-CLI all-five-family unchanged-artifact execution, explicit capability HOF/borrow and failed-build gates pass; three shipped negatives each1/nooutput. Root independently reran all175 published literal cases (36admit/139refuse) and reconciled26 checkout hashes. Reviewer332focused assertions perplatform plus194suite and35-entry source maps pass; actual Linux package/CLI installed. Runtime20rows/60intervals/1500calls perplatform, ten product/four support identities current/crossplatform/beforeafter identical. Contracts, final conformance, README and costs inspected; Commitf6ea4c1.
- [x] 6. Domain alternatives and failure
  - State: complete
  - Task: /root/m06_domains; runtime helper /root/m05_effects; independent reviewer /root/m06_review
  - Depends on: 5
  - Acceptance: A19–A20; exhaustive alternatives, characterized handlers, immutable failure data.
  - Evidence: Corrected frozen242 suite passes rootnative4.775s/Linux14.739s; root23 installed-CLI/native artifact/guard/failed-build/explain gates pass. Root independently reran236 published literal sources (73admit/163refuse) and reconciled70 source identities plus11 current references. Reviewer595 focused assertions/platform and actual installedLinuxwheel13-file inventory pass; full source maps unchanged/current/crossplatform. Runtime36rows108intervals2700calls+360warmups/platform at10/100,12product+8owned maps independently inspected. Final contracts, conformance and costs inspected; commit48b56a9.
- [x] 7. Standard-operation contracts
  - State: complete
  - Task: /root/m07_standard; runtime helper /root/m06_domains; independent reviewer /root/m07_review
  - Depends on: 6
  - Acceptance: A21, A32; useful versioned operations with initialization, dispatch, effects/failure evidence.
  - Evidence: Frozen 286-test suite passes root native 6.350s/Linux 20.501s; root 26 installed-CLI/artifact/setup/effect/failed-build/explain gates pass. Independent 532 fixed sources (187 admits/345 refusals), 2,381 native/2,386 Linux focused assertions and fresh installed Linux wheel pass. Root reconciled all 92 current/cross/before-after inputs, 15 installed files, 17 complete published harnesses, all published outcomes/contracts and 11 references. Runtime 36 rows/108 intervals/2,700 calls plus 360 warmups per platform, 14/15/5 current identity maps, medians/peaks and zero registry hooks reconciled. Final handoff/contracts/conformance/costs inspected; commit4531a3e.
- [x] 8. External integrations
  - State: complete
  - Task: /root/m08_integrations; runtime helper /root/m07_standard; independent reviewer /root/m08_review
  - Depends on: 7
  - Acceptance: A22–A23; two bounded integrations, reviewed dependency identity, transitive trust and isolation.
  - Evidence: Corrected 37-input freeze passes root 320-test suites native 15.369s/Linux 50.641s, eight installed-console/artifact gates and four fresh metadata nonexecution commands. Independent fresh installed wheel passes 320 methods, 708 fixed source/policy cases, 57 runtime rows and 18 focused groups per platform. Root reconciled 114 source, 17 installed product and 49 copied fixture identities, 11 complete published current harnesses, all 45 raw output hashes and published status/counter summaries. Real installed binary mutation/expiry/unsafe artifact gates pass. Measurements: 24 rows/72 intervals/1,800 calls plus 240 warmups per platform, exact guards/medians/peaks and current 16/17/4 maps reconciled; three dependency identities and five real installed files independently rehashed per platform. Final handoff/contracts/conformance/costs inspected; human usefulness remains UNMEASURED. Commit ec580b0.
- [x] 9. Editor experience
  - State: engineering complete; human repair gate unmeasured
  - Task: /root/m09_editor; client helper /root/m08_integrations; independent reviewer /root/m09_review
  - Depends on: 8
  - Acceptance: A24 for compatible sources and generated guards; shared diagnostics, navigation, explanations and safe previews.
  - Evidence: Frozen91 checkout inputs/18 package files/5 complete reviewer controllers remain current. Root349 suites pass native15.680s/Linux61.842s, five installed-console/isolated-wire/stock-guard aggregate gates per platform. Independent fresh installed native/Linux wheel each passes349 methods and2408 fixed checks/15groups; root reconciles212 raw identities, complete controllers,87 source/controller/18 installed/62 copied fixture maps, and67 observed nonisolated suite processes per platform with all loaded product paths installed. Actual Node10, trusted/restricted VS Code hosts and finite VSIX install/readback pass with91/18/8 before/after/current maps. Exact local VSIX preserved under dist/editors/. Source/harness corrections and startup/site prerequisites explicit. Human repair remains UNMEASURED0; translated A24 remains milestone14. Committed dfe408f.
- [x] 10. Migration and team policy
  - State: engineering complete; root commit forthcoming
  - Task: /root/m10_build; policy helper /root/m10_policy; independent reviewer /root/m10_review
  - Depends on: 8; independent of 9 when file ownership is disjoint
  - Acceptance: A25–A26; readiness, stable debt identity, conversion previews, coverage/effect/trust ratchets.
  - Evidence: Unchanged99-input freeze passes401-method suites native21.499s/Linux80.526s and root62assertion23command walks each. Fresh independent installed native/Linux fivegroups each pass26actualconsolecommands15structural18IOrows3buildraces/actualUTCexpiry. Root reconciles7phase99source/3root/10peer/20package/19product maps,131raw SHA/byte records102projections52actualcommands10exactpublishedprotocoltexts and5actualnativeidentityfiles/platform. Named794byte4module9function5export9exclusion denominator and10SCC19edge7direct12retained inventory published. Peerindex cf5e66ed..., rootfinalacceptance96aca49e...; original fixture refusal/correction preserved. Human0UNMEASURED; local milestone commit forthcoming.
- [ ] 11. Checked package distribution
  - State: queued
  - Task: not started
  - Depends on: 9, 10
  - Acceptance: A27–A28; separate consumer checks installed artifact evidence and imports normally.
  - Evidence: pending
- [ ] 12. Confined construction
  - State: queued
  - Task: not started
  - Depends on: 11
  - Acceptance: A29; disabled by default, confinement/finalization adversarial tests and useful measured costs.
  - Evidence: pending
- [ ] 13. Characterized concurrency
  - State: queued
  - Task: not started
  - Depends on: 12
  - Acceptance: A30; stable messages/captures, effect/failure propagation, ordering and cancellation tests.
  - Evidence: pending
- [ ] 14. Optional syntax
  - State: queued
  - Task: not started
  - Depends on: 11; independent of 12–13 when file ownership is disjoint
  - Acceptance: A31 and translated-source part of A24; explicit dialect translation, equivalence, editor/source maps and packaging.
  - Evidence: pending

## Shared context

- Authority: /Volumes/Projects/pyalamode/SPEC-sol6.1-composite.md.
- Repository starts with specifications only; initial specification commit: e0e36ab.
- Local available interpreter: CPython 3.13.1 on macOS. Linux compatibility requires actual evidence before claiming it tested.
- Workers use fresh, curated subagent contexts as explicitly requested by the user. No CatWrangler sessions, services, tickets or credentials are involved.
- Orchestrator owns this ledger, milestone verification, commits and run sequencing; workers own implementation in their assigned files and do not commit or schedule monitoring.
- Every worker records decisions, public handoffs and limitations in local milestone documentation so subsequent workers can inspect the actual implementation.

## Decisions and blockers

- A24’s translated-source requirement cannot be observed before milestone 14 supplies translation. Verify compatible-source/editor/guard coverage at milestone 9 and retain the translated-source portion as an outstanding gate until milestone 14. This changes verification timing, not product scope.
- Strict dependency milestones start only after prerequisite verification. Independent conformance/review/documentation work may proceed in parallel; concurrent writers have disjoint file ownership.
- M4 plan reviewed: exact fixed-field product records; named qualifying dataclass/namedtuple snapshot adapters to concrete record schemas; explicit exclusive-access assertion for mutable snapshots; fresh exports; optional selected `pyalamode_exports` facades and documented debug assertions. Guard selection must fail on unknown/duplicate targets. Ordinary original-module and checked internal calls retain their unguarded contracts. Runtime helper owns records/boundaries/collection hooks; checker/build worker owns remaining product files; reviewer owns conformance documentation only.
- M4 review corrections include annotation/default availability, resolved setter aliases, the new runtime dependency inventory, and exact adapter getter/default/constructor qualifiers. Root found an inherited checked circular `from` import admitted despite predictable partial initialization; approved a finite SCC rejection gate while retaining deferred module-import recursion. Product-module helper writes retain conservative wildcard exclusions; specific standard-foundation writers keep their individual gates. No claim of minimal symbol-level invalidation is made.

## Supporting workers

- /root/conformance_review: independent milestone-1 adversarial cases; owns Docs/conformance/m01-cases.md.
- /root/acceptance_inventory: complete; Docs/conformance/acceptance-matrix.md independently inspected; all14 milestone gates and35 acceptance scenarios retained.

- Linux verification environment: local Docker, python:3.13.1-slim, image digest sha256:031ebf3cde9f3719d2db385233bcb18df5162038e9cda20e64e08f49f4b47a2f. Milestone 1 same-patch suite passed; later milestone suites are independently rerun.

- /root/m01_guide_benchmark: owns README.md, examples/scalar.py and benchmarks/m01_scalar.py; independent first-use and named cold/warm measurement support.

## Verified milestones

- 1: CPython 3.13.1 standard macOS arm64 and Linux aarch64 local Docker suite: 24/24. Root CLI walkthrough emitted 1300 and rejected a PAL101 build with no artifact. Docs/milestones/01-scalar.md is the public handoff. Linux image digest recorded above. Human onboarding-time target remains unmeasured.

- /root/m02_review: independent module/capture/call-graph/freshness cases; owns Docs/conformance/m02-cases.md.
- Milestone 1 committed as 7d694e0; final staged whitespace check passed; tracked working tree was clean before milestone 2 dispatch.

- /root/m02_measurements: owns benchmarks/m02_modules.py and Docs/evidence/m02-*; named call-graph/cache measurements await frozen implementation.
- Milestone 2 callable rule: finite positional Callable contracts require pure invocation and stable captures; conditional callback calls carry the closed current failure upper bound {ZeroDivisionError, RecursionError}; concrete targets retain precise failures.
- Milestone 2 review corrections include lexical definition order/cell stability, actual foundation and package resolution, initializer failure separation, transitive rejection, and relevant analyzed writer context in cache identity. Final retest pending.

- Milestone 2 pre-freeze root verification: combined50 tests pass macOS1.210s/Linux2.292s. Installed CLI checks4 module-example files/6 functions/7 caller sites, builds unchanged compatible source, and ordinary execution emits1500,6,6,2. Three invalid capture/initializer/nested-data builds each return1 and publish no artifact. Final frozen tests/reviewer/measurements still pending.

- Milestone 2 app code/tests/examples frozen by worker; final combined50-test suite passed macOS1.292s and Linux2.329s. README and Docs/milestones/02-modules.md inspected. Independent conformance and final named measurements running against frozen sources.

- Milestone 2 measurements: branched_integer_rollup_v1,26 modules/208 functions/320 direct call edges,5 trials per platform. Medians macOS cold/warm/unrelated/leaf0.675846/0.481166/0.483994/0.505263s; Linux0.879751/0.623652/0.627578/0.662288s. Hits/misses0/26,26/0,25/1,23/3 on every trial. Both package snapshots match frozen checkout. Docs/evidence/m02-measurements.md publishes conditions/limits.

- Milestone 2 committed ca3db3f; staged whitespace clean and working tree clean before M3 dispatch.
- /root/m03_review owns Docs/conformance/m03-cases.md; implementation/review run in parallel only after M2 verification.

- M3 approved engineering plan: tuple-backed Vector/OrderedMap; canonically ordered homogeneous exactscalar Map/Set; O(n) copying updates and O(kn) full retained history, no externalbackend. Conditional callable failure bound expands to ZeroDivisionError/RecursionError/IndexError/KeyError/ValueError. No unordered general callbacks/traversal.
- Runtimehelper dispatch: fresh agent hit threadlimit, so completed /root/m02_modules reused with new curated disjoint unit: pyalamode/collections.py,tests/m03_runtime.py,benchmarks/m03_collections.py,Docs/evidence/m03-runtime-*. MainM3builder owns all checker/static/export/docs files; reviewer owns only conformance. No CatWrangler identity propagation.

- M3 pre-freeze root combined89-test suite passes macOS1.397s/Linux3.051s. Independent interim110source cases,11project layouts,6namespace/cache transitions clean. Runtime membership mismatch fixed with __contains__, 23runtime tests cover hooks/metaclass/cycles/forgedstorage/retention/order/callbackdata. Finalsourcefreeze/conformance/performance pending.

- M3 combinedproduct/tests/examples frozen. Root90-test finalsuite passesmacOS1.490s/Linux3.131s. Independentruntime262assertions/process at seeds1,2,8675309 identicaloutput. Nested-schema validation/equality RecursionError boundedseparately, meaningfulregression included. Conformancefinal/backendbytefreshness and100/1000/10000runtime measurements pending.

- M3 final4diagnostic-remediationstrings corrected (no behavior change); revisedmodeldigest6f0cbbc5837c3054f65bb1c3b8d4f6b0c5ce85a39506037790fdcc3af65fa184, renewedfreeze. Root90-test suite passesmacOS1.388s/Linux3.084s. Finalfocusedconformanceannotation willrecordnewmodeldigest; benchmarkonlybeforeafterhash/hardware refinement rerunsmeasurementsagainstupdatedsnapshot.
- M3rootCLI example:3sourcefiles/8functions/20calls, successfulfreshunchangedsourcebuild, ordinaryexecutionoutputpreservesoriginalVector andcanonicalMap/Set results.

- M3actualpostfreezefinding: validexactint key10**5000 caused hiddenValueError fromeagerdecimaldiagnosticpathformatting inMap/OrderedMapconstructors andnestedvalidation. Approved ONLYruntimeinternaldiagnostickeyformatter hex fallback (publicrepr/strictformatting scope unchanged) andfocusedtests; runtimefreeze reopened. Earliermeasurements preservedhistoricallyuntilfinalrerun. No checkerfailureuniversechange required.

- M3transitivefoundationfix: finiteactualbackendbuiltin/types inventory, knownanalyzedwritersinvalidatecollectionclasses+warmcontext; unrelatedscalarstridentity retainsproof/cache. Latestchecker7791b1ae028218413af16d02f956bb434f6cb8e7b073d4369ad6ba1b83683539, runtimec0a4738ae85c1048b44c160a19f2d425c2872a5b601dcd352989903ad4102ab6. Combined93-tests passmacOS1.508s/Linux3.646s. Finalfocusedconformance andfinalmetrics againsttheseidentities running.

- M3allworkerterminalreadiness inspected; Docs/milestones/03-collections.md andDocs/evidence/m03-runtime-measurements.md complete. Finalsrc/productidentities matchbothrawplatformmeasurements; sourceunchangedgatespass.

- M5 plan approved: finite source effect bounds, actual declared/conditional callback unions, explicit capability parameter lending and fixed Effectful signatures; whole-path rooted IO cleanup plus logical lexical borrow views, without persistent readers or capability captures. Live and recorded providers keep identical effect families. Strict unknown operations remain refusal. Fresh runtime helper dispatch hit client agent thread limit; completed M4 main task reused with a curated, disjoint runtime-only unit. Root owns gates and commits.

- M5 interim root verification:191 tests pass native2.873s after runtime26 added; earlier165 pass native3.270s/Linux9.398s. Actual installed CLI all-five-family check/build preserves source; stock Python artifact returns ('Ada','input',107,4), rooted IO writes saved:input and state advances4→5. Explicit capability-slot HOF and borrow pass. Three failed builds (undeclared IO, expired view, unknown operation) and narrowed entry policy each refuse/no artifact; six explain commands pass. Final frozen two-platform review/measurements pending.
- M5 review fixes: unused nested capability tuple refused; correct nested TOML effect-bound table; actual effects-function/submodule name collision modeled; imported private borrow-class method writers rejected. Ambient secrets/random import setup removed in favor of a finite direct OS-entropy operation; recorded provider classifications remain unchanged.

- M5 final gate observed against frozen checker5.1/runtime31d3ee92: all workers terminal, named final conformance corpus rerun by root, full source maps and actual generated-artifact measurements reconciled. Human measurements remain unmeasured; full-interface capability permission restriction, no captures/data/transfer, rooted IO TOCTOU assumptions and logical lease limits are published. No required engineering gate remains for M5.

- M5 committed f6ea4c1; staged whitespace passed and clean tree observed before M6 dispatch. Fresh M6 main/reviewer tasks are planning only. Runtime fresh dispatch and former runtime revival hit client thread limit, so terminal M5 main is reused with curated disjoint runtime-only ownership. M6 exact variant/pattern/handler catalog must be reviewed before code admission; ordinary exception targets must retain actual Python values with explicit immutable conversion and a distinct cleanup lifetime.

- M6 plan approved: nested closed variant/case declarations; typed Option/Result, binary ordered error accumulation; finite irrefutable class/record patterns with constrained and guarded captures refused; explicit-cases wildcard policy and case-set freshness. Ordinary builtin-category try handlers retain actual opaque handler-local exception targets and explicitly convert to immutable fixed-message Failure; cleanup targets cannot escape/rebind. Handler masks retain effects/trust/operations and respect RuntimeError/RecursionError and ValueError/UnicodeError hierarchies. Runtime schema/recursive fresh tagged exports agreed; main and helper file ownership disjoint.

- M6 interim root verification:234 native tests pass3.336s; actual admitted Lookup/Result source executes unchanged, returns correct closed cases and immutable failures. Root verified per-occurrence handled/unhandled calls and Clock effect retention. Independent review found nested constrained payload coverage, private-helper writer crashes and generated debug-prefix collisions; focused regressions/fixes are in progress. Root found inherited record/new-case class-local defaults shadowing annotation/default names; correction remains a pre-freeze gate. Final two-platform tests, corpus/source maps, installed CLI workflows and runtime measurements remain pending.

- M6 first frozen candidate:241 tests passed rootnative4.366s/Linux13.169s, root23 installed-CLI/native execution/guard/failed-build/explain gates passed. Freeze reopened for a concrete family-dependency gap: analyzed Some/Ok behavior writers did not invalidate Option/Result identity-only or nested-schema consumers. Focused correction approved; earlier final outputs/measurements are historical until the corrected tree is frozen and verified again. No dependent milestone has started.

- M6 corrected final gate observed: all three workers terminal; independent complete236-source corpus,70-source map/11references and raw36-row observations rerun/reconciled by root. Nested constrained coverage, generated-name collisions, private helper writer crash, real class-suite lookup and contained-case family dependencies have meaningful regressions. Actual source remains unchanged across final tests/artifact execution/measurements. Exact supported builtin handlers, positional binary accumulation and guard/caller limits are published; human measurements remain unmeasured. No required M6 engineering gate remains.

- M6 committed48b56a9 after staged whitespace check; clean checkout observed beforeM7dispatch. Fresh M7main/reviewer plan-only tasks started. Freshruntime helper hit client threadlimit, so terminalM6main reused with a curated runtime-only disjoint unit; prior static ownership ended. Joint finite standard-operation and callable toolkit catalog must be published/reviewed before new admission. Native decimal digit-limit dependence, UTF8/hex dispatch, latent composed/partial callbacks and setup/invocation separation are explicit review gates.

- M7 joint catalog approved before implementation:12 fixed positional text/int/manual-decimal/manual-UTF8/hex façades and5 eager scan/group/compose/partial/Result-traversal functions plus cataloged inherited fold/IO/Clock/Environment. Wrapper construction retains dependencies/trust/captures without invoking callbacks; invocation retains exact target/failure/effect evidence and masks through cache. Root actual3.13.1 probes found mutable registered strict handlers in low-level UTF8 and inherited live IO; resolved before admission by manualUTF8 and minimal rooted binaryIO hooks preserving permissions/lease/cleanup and truncation-before-encoding-failure behavior. Unknown native hooks remain refusal; setup observations leave surrounding ordinary initialization unchecked. Runtime workload proposal approved10/100×sixconditions×threeguardmodes, actual intervals require finalsourcefreeze. Human usefulness remains unmeasured.

- M7 pre-freeze native probes also demonstrated registered surrogateescape callbacks in live root/path/environment-name encoding, including Unicode scalar names under actual ASCII Linux startup. The supported runtime now explicitly requires UTF-8 filesystem encoding with surrogateescape error mode, enforced by check/build and live-provider setup and recorded in provenance. Caller-supplied OS names and resolved roots reject surrogate code points before native conversion. Existing native UTF-8 environment-value decoding retains its characterized DC-escape behavior: invalid-byte controls executed no replacement handler. Main/helper own focused implementation and reviewer owns isolated registry/startup regressions; final freeze remains pending.

- M7 final pre-freeze review found known function `__globals__` writes were not consistently invalidating sibling consumers. Main owns the focused defining-module correction, including dictionary aliases/mutators, nested builtins and local checked-function shared globals. Reviewer froze supplementary refusal literals before observing the correction; all earlier admission expectations remain fixed. Runtime/helper files are frozen, and no timed intervals or dependent milestone starts are authorized until the corrected joint tree passes its final gates.

- M7 final gate observed: all three workers terminal. Corrected checker `2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd` and all product/test/example/harness bytes remain frozen across final suites, stock artifact execution, fresh installed Linux review and measurements. Ordinary initialization remains distinct from pure invocation; latent wrapper targets/effects/failures and shared globals writer gates are preserved. Supported filesystem configuration, narrowed OS-name domain and characterized native environment decoding are explicit. Human usefulness remains UNMEASURED. No required M7 engineering gate remains.

- M7 committed4531a3e after staged whitespace inspection and clean checkout verification. Fresh M8 main/reviewer dispatched at plan-first gate; fresh runtime dispatch hit client thread limit, so completed M7 main reused with new curated runtime-only ownership and previous static ownership ended. At least two real bounded integrations, actual installed artifact/version identity, visible operation approvals/transitive assumptions and separate ordinary setup/unsafe isolation must be jointly reviewed before new admission.

- M8 joint plans approved after complete main/runtime/reviewer records and pinned CPython source review. Three exact-bytes positional-only operations use actual binascii canonical Base64 and fixed _sha2 HACL SHA-256, with 1MiB payload bounds, fixed ValueError translation, separate ordinary import setup and explicit operation/contract/installed-artifact approvals. binascii.Error construction/base/dictionary behavior is in the writer closure. Safe discovery executes no dependency or metadata hook; every warm check/build refreshes identity and expiry. Direct primitive first-class callbacks remain deferred; checked wrappers retain assumptions. Measurement protocol approved: four workloads, two sizes, three guards, 24 rows/72 intervals/1,800 calls plus 240 warmups per platform; intervals require a later explicit joint freeze. Human validation remains UNMEASURED.

- M8 pre-freeze root walkthrough passed eight aggregate installed-console gates in /tmp/pyalamode_root_m08.py: three guard-mode cold/warm/build/stock-artifact executions, latent composition/map trust, handled failure retains assumptions, unsafe snapshot starts a pure total, denied/missing/stale/expired check/build refusals with no artifact, and checked unsafe-call refusal. Root found and main corrected a displaced standard composition branch and an extensionless console-script false package shadow. Inherited M7 foundation inventory assertion is explicitly reconciled 14→16 for the two new modules; no source/behavior expectation changed. Reviewer fixed 176 source/policy expectations and 57 runtime answers before admission observations. Runtime helper freeze intent and protocol inspected; joint final freeze remains pending.

- M8 actual pre-freeze metadata execution finding: sysconfig getters can import a PYTHONPATH module selected by _PYTHON_SYSCONFIGDATA_NAME; helper observed a sentinel run during discovery despite unresolved identities. Main owns focused safe configuration/target discovery repair; reviewer independently checks related selectors and default configuration shadows. No new operation behavior is authorized by this repair. Final freeze/measurement/acceptance are held until nonexecution is established.

- M8 first joint freeze reconciled 37 source inputs (17 package files), packet SHA3f4362023be4d26ee92761c10dc9ce43474f3b7882db32b4c9648322f52d0754. Root frozen acceptance/metadata walks passed, but full suites319 native15.531s/Linux51.714s both found one inherited M2 valid module-alias call falsely tainted as a writer. The new mutator-spelling inventory included `add`, incorrectly classifying actual checked `calculations.add(plus(x))`. Main resumed for a focused actual-callee distinction and regression, preserving original M2 expectation and native/escaped writer refusal. Runtime/test/measurement sources remain frozen; intervals held until corrected re-freeze.

- M8 corrected freeze reconciled exactly checker.py/tests/m08_integrations.py changes, retaining the other 35 inputs. Packet SHA18fc42d5f4d76160a1a74edf39882f044024847888ef2774d85cc77daa566712; checker65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5. Root full320 suites PASS native15.369s/Linux50.641s, final8 installed-console/stock-artifact gates and4 fresh metadata-nonevaluation commands PASS. All37 input hashes remain current. Helper untimed corrected artifacts PASS off/exports/debug both platforms, with16/17/4 unchanged/cross-equal maps and expected0/2/4(simple)/6(combined) validator calls. Reviewer fresh corrected-wheel/native+installedLinux conformance and frozen intervals remain outstanding; no repeated whole-suite tests are needed absent another source change.

- M8 final gate observed: all workers terminal; root reconciled final publication against fixed literal inputs, raw outputs and actual current installed bytes. Source freeze remains unchanged. Explicit native approval, ordinary setup separation, safe fixed-layout discovery and unsafe snapshot isolation retain their published finite contracts. Fresh installed verification and all authorized intervals are complete; no required M8 engineering gate remains. Human integration usefulness and approval effort remain UNMEASURED.

- M8 committed ec580b0 after staged whitespace checks; clean checkout observed before M9 dispatch. Fresh M9 main/reviewer are at plan-first gates; completed M8 main reused for disjoint editor client ownership. Shared server/client schema, authored locations, safe previews and freshness/nonexecution must be jointly reviewed before implementation. M10 may overlap only after disjoint file ownership is established.

- M9 joint plans approved: shared full-project read-only disk/overlay snapshot, current policy/resolution/writer/approval inputs, producer-aware AST/token/syntax positions converted to UTF16, finite LSP3.17 stdio and actual direct checked-edge navigation. Two preview-only finite data-flow repairs retain semantics/effects/trust/failures and never apply edits. Current-artifact/checked-source guard locations remain static. Disjoint local VS Code CommonJS client uses Node builtins and isolated real host/VSIX install verification. Product inventory16→17 reviewed; central CLI/project/model/checker files locked until M9 release. Human repair remains UNMEASURED.

- M9 early source review corrections are worker-owned: malformed client error must settle its pending promise; editor policy/selected/transitive symlink paths are refused before read; shared external explanation reuses scoped snapshot; long-lived product changes require restart and no successful per-file stale claim; guard evidence requires actual selected hashed source/facade and current coverage; malformed envelope/ID/JSON and finite parser recursion failures retain bounded correct wire behavior. Reviewer fixes literals before observing corrections. Client interim actual Node transport tests and isolated VSIX install pass; actual host asynchronous diagnostics require a bounded wait in the test. Final freeze and final suite/client/conformance remain pending.

- M9 interim development345-method suite passes15.359s; actual trusted VS Code1.139.1 host (embedded Node24.20.0, external Node23.5.0 separate) passes real Problems/navigation/diff/guard workflow. Restricted host correctly grants no child execution; development module activation differs from initial harness assumption and will be disclosed. Review fixed lone-CR/Unicode-separator expectations before observing correction; valid CR source tokenizer crash repaired via universal physical-line reading without transforming source bytes. Settled independent2086-check run found one actual same-name package/module index bug: _local_path prefers package but SourceGraph.modules selection depended on traversal order. Root approved narrow actual-resolved index selection plus inherited/warm-overlay/stock-import regression; original expectation remains fixed. Final freeze held.

- M9 module-index correction exposed a concrete nominal-type collision: selected shadow module `Item(payload:int)` overwrote actual imported package `Item(payload:str)`. Root approved canonical package record/variant/case indexes, retained per-path declaration reporting, and PAL241 refusal of conflicting shadow nominal declarations. Function-only duplicate physical files keep their fixed admission expectation. Reviewer fixes both payload directions before observing correction. Client local-desktop/remote-host gate is settled; final joint freeze remains held until the type-index repair passes.

- M9 nominal repair passes28 main methods plus69 relevant inherited methods; source intent accepted, final observations not started. Helper then observed actual workspace `pyalamode/__init__.py` execution during plain interpreter module startup before checker entry. Root approved exact isolated client launch with literal configured venv executable and `-I -m pyalamode.editor`, installed-environment provenance and independent workspace/startup-poison sentinel regressions. Client/main documentation and controller launch expectations must settle before joint freeze. Ordinary Python startup assumptions remain explicit for manually invoked console commands.

- M9 corrected joint freeze independently reconciles main/client intent maps: packetSHA57575e0779f28f5b4bf7b961756027fefc34ac9be1a36de48f8050ffbefeeb01,91 checkout inputs/18 package files/5 complete review controllers plus root real-wire harness. Root native349-method suite PASS15.680s and five actual installed-console/isolated-wire/ordinary-guard-artifact gates PASS; all frozen inputs remain unchanged. Fresh wheelSHA1c58ae17c01e8fcb29976cca8252b4e0e9adbd871f4722e1bf46f88aa938e6a3 built from exact frozen outside copy; Linux source suite installs it offline for isolated children. Final installed reviewer and actual host/package evidence remain outstanding. M10 fresh main is planning only in its new milestone document; all frozen source ownership remains locked.

- M9 final engineering gate observed: all implementation/reviewer workers terminal, complete published controllers match actual frozen bytes and terminal projections match all212 current raw identities. Root Linux first harness mixed checkout and installed physical product copies, producing correct identity refusal; corrected single canonical source setup passes349 tests61.842s, separate actual installed CLI/isolated-wire/stock-artifact walk passes five gates. Fresh installed reviewer passes349 native18.448s/Linux45.824s and2408 checks/15groups each;67 nonisolated process records per platform independently rehashed with all706 loaded product paths within the selected installed package. Four actual client/host/package packet hashes, exact source maps and usable VSIXSHA61057976468834b063ed81d03077e8b4ad2a9699620018e3747870a6b084cafb reconciled. Human repair remains UNMEASURED0 and translated A24 remains14; no engineering blocker remains for9.

- M10 joint planning started in new documents only. Root settles stable finding groups with occurrence counts and explicit birth-identity lineage; unique relocation retains prior IDs without positional guessing. Baseline recording success is distinct from source/current-policy status and never certifies or waives failures. A first baseline can bootstrap historical reference gates while preserving current source/policy events; normal strict checks/builds still refuse current failures. Atomic baseline/report writes require a main-owned live freshness validator before publication. Exact helper/main/reviewer APIs, row schemas and literal cases remain at plan review; no M10 source mutations authorized yet.

- M9 committed dfe408f after final staged whitespace verification. Its engineering source gate is released; M10 source mutation remains separately withheld until joint plan approval. Fresh main m10_build assumes the prior terminal planner's document; helper/reviewer retain disjoint plan ownership. Root fixes independent current approval_failures events, including actually required missing/stale/draft/denied/expired/unresolved approvals, while expired_approvals includes configured unused expiry. Migration PAL360–367 events do not become recursively ratcheted underlying source-debt groups.

- M10 detached helper released from the complete 228-line policy contract SHAf696cd1cd1c50b78a6f1874e6eb223e7a268e5dbc1270d78419b3c4de0b8eb91 and fixed reviewer literals. Root approves exact nested evidence schemas, finite JSON/IO limits, actual audit versus strict-state axes, verified predecessor lineage, descriptor-local cooperative baseline lock, live callback and explicit two-publication orphan-history semantics. Module selectors are module: plus actual namespace, including the empty root __init__ namespace without an invented public import identity. Main reconciliation is finishing; independent candidate observations wait for a later joint freeze.

- M10 complete joint main plan SHAd588bd7e8af6d1cbff3000ea49ced8a61fec09fd08ddb2a772eb774962c7c310 read and approved against helper SHAf696cd1c... and fixed reviewer SHAc9389e85.... Main/helper now implement disjoint files in parallel. Actual strict capture remains distinct from inherited audit exit; required export uses canonical namespace, conversion exact authored identity; private actual external-site metadata and finite dependency traversal supply required operations without spelling guesses. Report save preserves its current failing command status with a separate successful recording receipt. Root fixed command controller SHA7dd240b7f16a962be44ace389bdd5acf53444e734af377cb08701f7c1fd1fe6a prepared without candidate observation. Editor files remain unchanged; explicit foundation count17→19 is the only authorized inherited assertion update. Full suites/final reviewer observations/timed intervals remain held until a later source freeze.

- M10 early source review fixes retain original expectations: late build PAL350 must update the saved source/status axis; team policy ownership is enforced before initial source/dependency reads; physical AST lines exclude Unicode separators; body-only unsafe changes and same-path unused manifest contract changes have independent events; category-specific persisted rows remain closed and consistent. Reviewer fixes dedicated cases before correction observation. Root approves a disclosed reserved .pyalamode-build- internal staging-directory exclusion for full prepublication inventory, without hiding arbitrary output subtrees. Root command controller's pre-observation schema extraction now uses settled outer report/written receipts and a direct-root accepted output to cover actual staging ownership.

- M10 final source review additionally requires no-edit conversion to preserve historical failure, hypothetical contracts to disclose analysis-only selection, and prerequisites to have actual disk checked proof. Verified lineage is recomputed against predecessor/current birth-reset capture; valid digests cannot authorize ambiguous relocation. Temporary pre-yield failures clean up and controlled post-replace failures restore prior active bytes only while publication ownership remains unchanged. Closed saved report status cannot waive strict source failure; audit remains a separate command axis. Helper focused28 and main focused21 plus nine inherited checks passed before the later configured-path correction; those are implementation evidence, not final platform acceptance.

- M10 root found both active baseline bootstrap and writer destination hardcoded to the default despite a supported configured reference. Main/helper jointly use the normalized configured active path for first/replacement/predecessor/receipt, preserving an existing independent default baseline. Reserved history/reports namespaces remain immutable: writer destinations there refuse2 before publication; explicit historical reads remain supported. Helper focused30 passes after the correction; root final freeze/whole suites/installed independent observations remain held until current intent maps and prepared controllers settle. No dependent milestone has started.

- M10 final source intents independently reconcile main12/helper3 files and actual19 foundation artifacts. Root source packet `/tmp/pyalamode-m10-root-freeze.json` SHA20d293ccb4781b64fc16ada3eff48f4b5951c135d8eb8e6930a23f6fda5f98a5 pins99 complete code/test/example/editor/benchmark/README/spec inputs,20 package modules and three root controllers; exact inventory comparison catches additions/removals as well as byte changes. Root native/Linux full suites and fixed real-console command walk are released against that freeze. To overlap preparation safely, peer installed-review controllers/literals remain separately held until root reads their complete texts and freezes their final intent against these same source inputs. Evolving final evidence prose is excluded from source identity. No dependent milestone has started.

- M10 root source gates pass401 methods on native21.499s/Linux80.526s; fixed real-console walks pass62 assertions/23 commands each, including source1/baseline0/audit0/report-save1, new debt despite lower total, coverage loss, failed build no output, successful ordinary artifact execution and nonexecution sentinels. Exact99 source inventory and bytes remain unchanged. Root's outside-copy wheel SHAdc04c689b6d44d73aa6f3d2206407f4addf33a3725a62662c8a9230166a92798 has all20 frozen package files; separate fresh Linux installed environment matches every file and has no checkout on sys.path. Native editable-source suite, Linux canonical-source suite and fresh installed Linux walk stay separate physical-product environments. Final independent bounded installed review and approved untimed structural inventory remain outstanding; no full-suite repetition is required absent new source changes or findings.

- M10 independently read and rehashed all ten peer controller/literal inputs. Peer intent SHAe348c9c5b7190caafcf2cc6df22febacff8779f3c0bcc30ab9b1e3ea9766064a and preparation SHAc7ad2da2b4046b42efb217f73469c292c48385f996ba343d48547c0f143e94a1 bind unchanged root source freeze20d293cc.... Five bounded fresh installed native/Linux groups are authorized. Before candidate observation, source review corrected a fixture that mistakenly treated external trust as an External effect: actual native invocation effects remain empty and trust is separate; the semantic trust gate expectation stays1. A prior-artifact preservation probe now uses a genuine successful build, and temporary-file failure injection targets the actual staging inode. No product bytes changed, so existing401-method source gates remain applicable. Human migration usefulness remains UNMEASURED0.

- M10 first peer installed runs pass CLI and denominator controls, then correctly refuse an ordinary uses_checked(value) call with PAL102/PAL221 because ordinary annotations do not establish exact argument evidence. The readiness fixture incorrectly expected that selected prerequisite to remain checked. Root read actual raw diagnostic SHAf4c9cc9dacf5780eb4ee9506436998c97e4cf2eb073a2466e1dc24648e2efc26 and inherited source semantics; only fixture call checked(1) is authorized for preparation, preserving actual dependency edge, strict0 and checked-prerequisite oracles. Initial failed raw runs remain preserved. Corrected controller execution waits for a new peer intent review; product freeze99/401 source gates unchanged.

- M10 corrected peer controller intent-v2 SHAf76ca01ab24f0e5f0298efaab8171cf5d18c3e7045f44978c9276534eff9f17a and preparation SHA0b458b28b47c3a7caed80cb8d3c1f535810ae2fbbf2df220b1f94c919973e5ce independently reconcile exact single-line checked(1) delta, retaining all fixed strict0/actual dependency/checked-prerequisite expectations. Fresh installed native/Linux five-group runs PASS. Root independently inspects actual19CLI+7recordIO commands,15structural rows18IO rows3actualbuild races/lateUTCexpiry projections, all7before/cross/after99source/3root/10peer/20package/19product maps, actual current wheels and installed files. Root rehashes all5 actual native/interpreter/adapter files each platform. Structural inventory794bytes4modules9functions5checkedexports9exclusions; readiness10SCCgroups19edges7direct12retained; all4cold cache flags false/all4warm true. Root peer reconciliation SHAd743f28141dd896bd98e0d2dff511f9f09fc16f06ac1f9c05798dc44f6dd1501 records those gates; complete published controllers/finalindex/docs remain outstanding before commit. Human0UNMEASURED.

- M10 final published controller/literal bytes independently reconstruct all10 pinned inputs;131 actual raw SHA/byte records and102 literal projections/52 actual console command records reconcile with observed producer outputs and installed maps. Independent concurrent-writer publication remains present after safe rollback refusal. Final root acceptance `/tmp/pyalamode-root-m10-evidence/final-acceptance.json` SHA96aca49e065944ce52a809e26e608806f4aa2a2fab9f87568e4a2629053b4d34 closes engineering gates. Main/helper final docs inspected; root Git milestone is next. Human release observations remain UNMEASURED0.
