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
  - Evidence: Frozen93-test suite passesmacOS1.508s/Linux3.646s; independent113sourcecases,11projectlayouts,namespace/cache/backendbytefreshness and262runtimeassertions×3seeds clean; hugeint43focusedchecks/hookzero and8foundationwritergates clean. Ordinaryunchangedbuild/run and3negativebuildnooutputgates verified.36runtimeconditions/108intervals perplatform at100/1000/10000, actualretention/updatecosts andmatchingfinalsourceidentities published. Commitpending.
- [ ] 4. Records and boundaries
  - State: queued
  - Task: not started
  - Depends on: 3
  - Acceptance: A14–A16, A34–A35; independent snapshots/exports and selected guard coverage.
  - Evidence: pending
- [ ] 5. Checked effectful shells
  - State: queued
  - Task: not started
  - Depends on: 4
  - Acceptance: A17–A18; finite effects, capability lifetime, unknown-operation rejection and provider classification.
  - Evidence: pending
- [ ] 6. Domain alternatives and failure
  - State: queued
  - Task: not started
  - Depends on: 5
  - Acceptance: A19–A20; exhaustive alternatives, characterized handlers, immutable failure data.
  - Evidence: pending
- [ ] 7. Standard-operation contracts
  - State: queued
  - Task: not started
  - Depends on: 6
  - Acceptance: A21, A32; useful versioned operations with initialization, dispatch, effects/failure evidence.
  - Evidence: pending
- [ ] 8. External integrations
  - State: queued
  - Task: not started
  - Depends on: 7
  - Acceptance: A22–A23; two bounded integrations, reviewed dependency identity, transitive trust and isolation.
  - Evidence: pending
- [ ] 9. Editor experience
  - State: queued
  - Task: not started
  - Depends on: 8
  - Acceptance: A24 for compatible sources and generated guards; shared diagnostics, navigation, explanations and safe previews.
  - Evidence: pending
- [ ] 10. Migration and team policy
  - State: queued
  - Task: not started
  - Depends on: 8; independent of 9 when file ownership is disjoint
  - Acceptance: A25–A26; readiness, stable debt identity, conversion previews, coverage/effect/trust ratchets.
  - Evidence: pending
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
