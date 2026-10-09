# Milestone 10 — migration and team policy

**Status:** engineering gates and final publication reconciliation observed; main handoff complete for the forthcoming root-owned Git milestone. Frozen native/Linux source suites, root command walks and corrected peer fresh-installed groups pass. No Git commit is claimed yet.
**Authority:** complete `SPEC-sol6.1-composite.md`, README, `Docs/orchestrations/pyalamode.md`, `Docs/evidence/m10-policy.md`, `Docs/conformance/m10-cases.md` and the explicitly invoked orchestrate skill. The user's local parallel-agent authorization and exclusion of CatWrangler/remote/scheduling override that skill's session workflow. No applicable `AGENTS.md` was found.
**Prerequisite:** M1–M9 are verified and committed; M9 is `dfe408f`. Root approved the complete 255-line main plan (SHA-256 `d588bd7e8af6d1cbff3000ea49ced8a61fec09fd08ddb2a772eb774962c7c310`) together with helper/reviewer contracts and released the bounded implementation. The final M9 packet is `/tmp/pyalamode-m09-root-freeze.json`, SHA-256 `57575e0779f28f5b4bf7b961756027fefc34ac9be1a36de48f8050ffbefeeb01`.
**Human usefulness:** UNMEASURED, zero participants, attempts or observations.

M10 supplies local adoption queues, finite conversion proposals, reviewed debt and independent team gates. It adds no admitted Python operation, effect, value, automatic source edit, trust permission, runtime certificate, remote service or CatWrangler dependency. Static observation does not import application modules or evaluate annotations, defaults, decorators or hooks. The target remains exactly CPython 3.13.1 standard GIL on macOS/Linux with UTF-8 filesystem encoding and surrogateescape errors; unsupported targets are status 2.

## 1. Fixed decisions and ownership

- All commands capture the full project, including current dependencies, resolution winners and ordinary analyzed writers. Path arguments filter presentation and candidate queues, never the policy denominator.
- Baseline/report capture and readiness/candidate work use fresh bodies (`cache=False`). Normal checks retain ordinary body-cache reuse. With neither required exports nor migration policy, ordinary check adds no second analysis or durable write. Cache payloads contain source evidence, never historical gate decisions.
- A baseline may record any non-tooling current source/audit/current-policy debt with recording status 0 and `verified=false`. It preserves underlying strict and current-policy statuses/events and never waives their normal check/build failures.
- First-baseline bootstrap bypasses only recursive historical-reference evaluation and missing-active-reference failure. Its active path is the safely validated normalized `policy.migration.baseline`, defaulting to `.pyalamode/baseline.json`; the same configured path controls record, load, predecessor and active publication. An existing unrelated default record does not prevent first capture at a missing configured custom path. Source, required-export, effect, external, guard and current expiry requirements remain observable. Existing active records require explicit replacement with a valid predecessor.
- PAL360–PAL367 and current required-export events are policy evidence, excluded from underlying finding groups. Policy events cannot recursively become new audit debt.
- A saved state is historical review evidence. Every observation and final publication refreshes actual source/inventory/resolution/writers, policy, product, integration identities, UTC expiry and reference identities.
- Only explicit `baseline` and `report --save` publish migration files. Other commands are read-only apart from separately disposable check caches. `run` remains optional and deferred.

Implementation ownership is disjoint:

| Worker | Owned files | Responsibility |
| --- | --- | --- |
| Main `/root/m10_build` | `pyalamode/migration_views.py`, `tests/m10_migration.py`, `examples/migration/**`, central `cli.py`, `project.py`, `model.py`, finite analysis-selection/origin metadata in `checker.py`, README and this document | Authoritative capture/denominators, regions/readiness/conversion, CLI and check/build/editor integration. |
| Helper `/root/m10_policy` | `pyalamode/migration.py`, `tests/m10_policy.py`, **`Docs/evidence/m10-policy.md`** | Pure context/normalization/matching/gates, closed records and explicit local IO. |
| Reviewer `/root/m10_review` | `Docs/conformance/m10-cases.md`, bounded controllers outside checkout | Fix expectations before candidate observations; independently inspect actual frozen commands and evidence. No product edits. |
| Root | Orchestration ledger, approval/freeze/final verification/commit | Release and verify the increment. |

No editor/server or client source changes are planned. Main projects deduplicated policy diagnostics into the existing editor diagnostic feed after preserving raw source evidence. The two inherited M9 previews are reused through `EditorSession` in-process; changing a shared editor API requires root review first. Product-byte identity inventory changes explicitly from 17 to 19 for the two new modules; operation admission does not change.

## 2. Exact APIs and status axes

Helper API, fully detached except root and the required callback:

```python
class MigrationError(ValueError):
    pass

finding_context(source: str, diagnostic: dict, boundary: dict) -> dict
normalize_state(state: dict) -> dict
compare_states(reference: dict | None, current: dict) -> dict
evaluate_gates(comparison: dict, policy: dict) -> dict
load_reference(root: Path, relative: str) -> dict
write_baseline(root: Path, state: dict, *, owner: str, rationale: str,
               replace: bool = False, prepublish: Callable[[], None]) -> dict
save_report(root: Path, report: dict, *, prepublish: Callable[[], None]) -> dict
```

Pure calls mutate no caller data and perform no IO. `finding_context` parses captured text only. `normalize_state` is **current-capture only**, forcing birth=current; mismatched supplied births refuse. Private helper validators accept persisted retained births only after `load_reference` validates envelope/predecessor/lineage. Replacement derives retained births internally from validated comparison; arbitrary current dictionaries cannot promote old IDs. `load_reference` returns exactly `{record,state,receipt}`; receipt is `{path,id,sha256}`, SHA over actual reference bytes. Helper errors are bounded to 1,024 characters and main maps them to tooling 2. Callback success is exactly `None`; false/other values refuse.

Main APIs in `migration_views.py`:

```python
capture_state(snapshot: ProjectSnapshot, policy: dict, inventory: dict) -> dict
observe(root, paths=None, *, target=TARGET, compare=None,
        bootstrap=False) -> tuple[ProjectSnapshot, dict, dict, dict | None]
make_report(snapshot: ProjectSnapshot, state: dict, reference=None,
            *, bootstrap=False) -> dict
regions_view(snapshot: ProjectSnapshot, state: dict) -> dict
ready_view(snapshot: ProjectSnapshot, state: dict) -> dict
convert_preview(snapshot: ProjectSnapshot, state: dict, target: str) -> dict
make_prepublish(snapshot: ProjectSnapshot, state: dict,
                reference_receipts: list[dict]) -> Callable[[], None]
```

`capture_state` requires an actual full-project **non-audit** snapshot; it does not infer checked proof from audit contracts. Inventory is captured from the same root/source set and contains displayed paths/exclusion rows; state normalization is helper-owned. `observe` returns the current strict snapshot, normalized state, report and validated reference. `check_snapshot` and `check_paths` gain private `_candidate_selection=None` and `_migration_history=True` arguments. `_migration_history=False` disables only historical reference/comparison recursion; all current source/policy enforcement remains. Snapshot inputs/hash explicitly include `analysis={candidate_selection,migration_history}`. Readiness publishes the separate candidate snapshot/analysis; conversion publishes its actual overlay snapshot/inputs/freshness. Candidate selection is analysis-only, cannot be TOML-serialized, cached or selected by build. Public build always enforces current/history gates.

`ProjectResult` gains detached `migration`, `policy_diagnostics`, and saved raw `source_status`; current and historical policy statuses remain separate. Command status is `max(actual command source_status, current_policy_status, historical_gate_status)`, with tooling 2 dominant. For `check --audit`, inherited audit source status remains 0 for non-tooling PAL350/PAL101 debt; the separately captured `state.strict_status=1` never becomes a new audit gate. `approval_failures` is independent visible engine evidence, not a new gate. Current policy status includes actual required-export failure and **enabled** current expiry enforcement; it does not blanket-upgrade source PAL350 to an audit policy failure. Audit is always unverified.

Save raw source status and strict boundary evidence before projecting policy diagnostics into existing result-file/editor diagnostics; cache writes precede projection. `to_dict` publishes both axes and the distinct policy list. Deduplicate projections by full diagnostic identity. Status still accounts for late non-policy source refusals; used expiry at build publication updates saved source status to1 and preserves PAL350/no artifact. A current valid function can retain checked source proof while project policy status is 1 and project `verified=false`. Policy failures that invalidate a boundary's actual source/input scope cannot preserve its proof. Editor sees policy diagnostics/status and unsaved provenance through its existing engine feed; no per-file policy success is fabricated.

## 3. Closed state schema and finite bounds

Canonical hashes use `json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=True, allow_nan=False).encode("utf-8")`. Published JSON is indented with trailing newline. Reject duplicate keys, unknown fields, bool-as-int, floats/NaN/Infinity, malformed/unsupported versions, corrupt IDs and oversized/deep input. Set inventories are sorted/deduplicated only where declared; ordered parameters/source cases and occurrence counts retain order/meaning.

Root-approved bounds: encoded record 16 MiB, depth 64, JSON nodes 500,000, identity/location/review text 16,384 code points, AST dump 1 MiB, sources 16,384, boundaries/finding groups 65,536, finding locations 262,144, approval/unsafe rows 4,096, predecessor chain 128. Limit failure is tooling 2, never a truncated passing claim.

Exact normalized state keys:

```text
schema=1; kind="pyalamode-migration-state"; identity_version="migration-identity-v1"
target; runtime_environment; edition; checker; operation_contract; snapshot; freshness; strict_status
current_policy_status; current_policy_events; required_operations
inputs={sources,policy_sha256,product_artifacts,integration_inputs}
scope={project_root,selected_paths,displayed_paths,exclusions}
coverage={eligible_modules,selected_modules,checked_modules,
          eligible_functions,selected_functions,checked_functions,
          checked_exports,selected_records,selected_variants}
boundaries; findings; policy; approvals; unsafe_adapters
```

`strict_status` is current underlying strict source/tooling 0/1/2 independent of historical/current policy and audit exit. `current_policy_status` is current nonhistorical policy 0/1/2. Freshness is exactly `current disk snapshot`, `current overlay snapshot; unsaved`, or `stale; recheck required`. Durable IO refuses tooling 2, stale and overlay states. `target`, edition, checker and operation strings are actual inherited identifiers. `runtime_environment` is exactly `{filesystem_encoding,filesystem_errors,utf8_mode}`, with supported encoding/error strings and exact int0/1 mode. No elapsed_seconds float enters migration state.

`sources` maps project-relative POSIX path to `{sha256,origin,version,disk_sha256}`: disk has version null; overlays keep actual nonnegative versions and disk hashes. `policy_sha256` is actual digest or null. `product_artifacts` maps all 19 actual installed filenames to digests. `integration_inputs` retains exact engine `{contract_sha256,dependency_sha256,admission,approval,identity_error}` rows keyed by canonical operation. Absolute native artifact paths are evidence provenance, never local record authority. All source selections/dependencies remain project-local; outside resolution refuses before read.

Scope selected_paths is the full captured physical source set; displayed_paths is its requested presentation subset. Exclusions are `{path,reason}` rows sorted by path/reason. Root path is informational and excluded from logical identity. Every input hash is fresh provenance; saved hashes never authorize evidence reuse.

Policy row has exactly `{require_modules,effect_bounds,explicit_cases,external_trust,integration_manifests,integration_approvals,required_exports,boundary_guards,guarded_exports,migration}`, with normalized closed defaults. Approvals are configured current engine approval rows, not denied catalog entries. Unsafe rows are the closed `{boundary,path,line,scope,rationale,valid_declaration,source_evidence,behavior,output_boundary}` shape: main converts the inherited name to its exact authored boundary selector and makes path project-relative; other engine evidence is retained. Closed inherited nested integration/external/native/approval and guard validators are fixed in the helper plan; main supplies those engine rows unchanged.

`current_policy_events` is exactly `{required_exports,expired_approvals,approval_failures}`, each a detached event list. Each event is `{boundary,before,after,reason,location}`. Required-export failure has before null, after exactly `{selector,engine_status:1,engine_rule:"PAL361",source_evidence}`, boundary `{kind:"function",selector,qualified_name}`, reason `current-required-export-{absent|unselected|unverified}` and policy location. Failed current required exports remain here and are projected into comparison `lost_strict_coverage` even without a reference. Historical coverage gates remain unobserved without history; current export status is independently enforced.

## 4. Exact denominators and boundary rows

Eligible modules count every captured physical Python file, including empty `__init__.py` and ordinary modules. Selected modules have actual source header or project module requirement; checked modules have actual successful strict initialization evidence. Physical same-name package/module files remain individually visible even though engine import namespace chooses the canonical package. No source is counted as checked merely because it was excluded.

Eligible functions count every authored `FunctionDef`/`AsyncFunctionDef`, including nested functions, methods, async and unsafe ordinary adapters. Selected functions are actual engine-selected definitions, including inherited nested/module selection; checked functions require current strict source proof. Unsupported ordinary async/methods remain eligible with mode off and explicit readiness blockers, never silently disappear from the denominator. Record/variant cases do not inflate function counts. Selected records/variants are actual declaration rows. Checked exports count canonical public top-level checked functions/records/variant domains; nested functions/cases, noncanonical shadows and the empty root namespace are not public exports.

The fixed four-module fixture is exactly: eligible modules 4, selected/checked modules 1; eligible functions 9, selected/checked functions 4; selected records 1 and variants 1; checked exports 5 (`core:total`, `core:now`, `strict:double`, `core:Customer`, `core:Choice`). Selecting only plain.py for display leaves these project counts unchanged. `.git`, `.venv`, `__pycache__`, build, dist, `.pyalamode-cache`, **`.pyalamode`**, `*.egg-info`, and the reserved **`.pyalamode-build-` directory prefix** are named exclusions; poison source there has no body analysis. Product staging is excluded with the published reason `reserved product build staging`; arbitrary user-owned output subtrees remain visible at the next observation. Explicit excluded migration display selections refuse2 before capture. Team initial selected/transitive reads and snapshot/migration-build/preview rereads check actual root ownership before reading; the shared policy parser also refuses outside-root policy resolution for ordinary commands.

Exact boundary row:

```text
id,kind,selector,path,qualified_name,signature,definition_sha256,
selected,selection_reasons,strict_checked,public_export,required_export,
mode,source_evidence,effect_bound,required_effects,effect_origins,
external_assumptions,failures,guard_coverage,location
```

Kinds are `function|module|record|variant`. Module selector is `module:<actual module name>`; module qualified_name is that name and signature null. Root `__init__.py` has selector **`module:`**, qualified_name **empty string**, and physical path provenance; it counts as a module without an invented importable namespace. Function/record/variant authored selectors are `<actual module>:<qualified name>` with no kind prefix; function qualified_name is lexical (e.g. total.plus), declaration qualified_name is its top-level name. Root declarations therefore have `:<name>` selectors for inventory only. Exact conversion selectors add a kind prefix separately.

`id` hashes `{identity_version,kind,selector,path}`. It is physical reporting identity; logical matching excludes path. Duplicate same-file declaration rows may repeat this physical ID and are preserved with their locations, never coalesced into a declaration. Helper detects duplicate logical declarations, emits intrinsic ambiguity even without findings, and refuses baselining them. Current authored conversion selector remains ambiguous if multiple physical definitions match.

`signature` is a position-free `ast.dump` of actual arguments/result/type parameters for a function, or actual ordered fields/defaults/cases for a declaration; it is never evaluated. `definition_sha256` hashes canonical position-free full declaration AST (module uses its module AST). Selection reasons are sorted literals `source_fun`, `source_effects`, `module_marker`, `required_module`, `enclosing_selection`; readiness adds hypothetical provenance to its own view, never to current state. Mode is `strict` for actual selected strict capture, `off` otherwise. `strict_checked` comes from actual unmodified engine evidence before project-policy projection, never from mode alone.

Effect bound/required effects are sorted finite family sets; effect_origins preserves actual engine family-to-origin-list map. External assumptions retain exact transitive inherited rows separately from foundation trust. Failures are `{invocation,definition,initialization}` sorted category lists. Guard coverage is `{mode,selected_export,debug,data_assertions}` with actual selected/export/debug/data rows; selecting a guard is not claiming it was generated. Location is `{path,line,column,end_line,end_column,column_encoding}`; positive 1-based starts, nullable ends, inherited encoding. Modules use line1/column1 with nullable ends.

`required_exports` accepts unique exact public top-level **function** selectors `module:function` only (nonempty dotted identifier module, one public identifier function). It uses `snapshot.graph.modules[module]` to select the actual canonical imported namespace. A noncanonical physical shadow does not win by traversal order. Missing canonical module/function, ordinary/unverified target => current PAL361 status1. Malformed/private/nested selector, duplicate selected declarations in the canonical namespace or incompatible/ambiguous target => tooling2. Existing nominal shadow PAL241 and guard duplicate-module refusals remain unchanged. Required exports select a requirement, never force checking or add callback/capability guards.

## 5. Grouped finding identity and context

Exact finding row:

```text
id,identity_key,birth_identity,rule,boundary_id,logical_boundary,
signature,context_sha256,context,origin,count,locations,review_required
```

Logical boundary is `{kind,selector,qualified_name}`; signature is boundary signature. Context is `{kind:"ast-statement",ast:TEXT}` or `{kind:"unavailable",reason:TEXT}`. Location rows are `{path,line,column,end_line,end_column,column_encoding,first_binding,reason,remediation}`; inherited first_binding is string|null, never an invented coordinate object. Count is positive and equals location multiplicity. Sort locations for review; never pair occurrences by their positions. PAL001/PAL002 and PAL360–367 are excluded from debt groups.

Context uses the smallest AST statement containing the **full** diagnostic range inside its authoritative owning boundary. Producer encoding is respected, including AST UTF-8-byte end-exclusive positions and token/syntax conventions. Function declaration ranges start at FunctionDef.lineno; its normalized dump includes decorators/defaults/annotations/body. Module diagnostics use the explicit module boundary. Missing source, unresolved/tied boundary/context or out-of-range points are review-required; line/reason alone is no identity. `ast.dump(...,annotate_fields=True,include_attributes=False,show_empty=False)` on exact CPython3.13.1 is pinned to the reviewer/helper's seven literal PAL101/221/230/241/250/310/350 dumps.

```text
context_sha256 = sha256(canonical(context))
current_identity = {identity_version,rule,logical_boundary,signature,context_sha256,origin}
identity_key = sha256(canonical(current_identity))
birth_identity = original current_identity
id = sha256(canonical(birth_identity))
```

Initial capture forces birth=current. Exact groups retain min(old_count,new_count), with positive count deltas independently new/resolved. old1/current2 => retained1/new1; old2/current1 => retained1/resolved1; old2/current2 => retained2 only. Identical repeated contexts are counted debt, not inherently ambiguous. No physical duplicate occurrence receives an ordinal ID.

Only a unique disappearing/appearing old/current group match with unchanged kind, qualified name, signature, rule, context and origin establishes relocation. Comparison carries prior birth/ID and before/after paths; reviewed replacement inherits it through validated lineage. Fresh current state still uses its current birth. Multiple plausible partners, duplicate logical declarations, unavailable context and incompatible identities are ambiguity; never guessed retention or clean resolution. Explicit reviewed replacement can reset historical ambiguity to current fresh identities, but intrinsically ambiguous current identities refuse2. General semantic equivalence, rename inference and positional guesses are out of scope.

Coverage matching is independent: exact logical boundary first, then unique same-kind/name/signature/body relocation. Selection/marker/module/required/public coverage changes remain visible even if findings decrease or prior selected source was unverified.

## 6. Required operations and independent comparisons

Main extracts required external operations from **actual current selected** engine functions, operation sets, contracts and external assumptions. The private `FunctionInfo.external_operation_sites` maps `integrations.<name>` to authored call-line sets, populated at the existing actual `_integration_call` **after** stable adapter/native dependency-replacement checks and **before** admission/PAL350 refusal. Actual PAL240 replacement refusals do not fabricate a required operation or approval diagnostic. Existing `info.operations` timing/admission semantics remain unchanged; new sites change observation metadata only. Native primitives as first-class callbacks remain deferred; real latent checked wrappers retain their body operation assumptions.

For each current selected owning boundary, main walks actual `info.calls` and `callable_dependencies` using finite `(target,via)` visited states. Own direct sites are `direct`; paths containing only invocation are `invoked`; any retained callable path is `retained`. Emit sorted unique `{boundary,path,line,via}` requirements with source path/line at the actual operation site and boundary at the affected owning logical selector. Cycles terminate; unknown/conditional callback obligations create no concrete edge. No familiar-spelling AST scan, diagnostic reason parsing, catalog enumeration or guessed operation manufactures a requirement.

Exact required operation row:

```text
{operation,required_by,contract_sha256,dependency_sha256,
 admission,engine_status,engine_rule,evidence}
```

Operation is canonical catalog identity; required_by is the sorted requirement array above. Evidence is closed discriminated `{kind:"external-assumption"|"integration-input",value:<exact inherited row>}`. Main currently supplies actual external-assumption rows from the engine; the helper also accepts the closed integration-input alternative. Digest null is permitted only for authoritative unresolved identity. Approved sites have rule null/status0; actual nonapproved admission at that recorded branch has PAL350/status1. Tooling2 captures refuse before constructing a non-tooling state. Do not infer rules from prose or turn catalog default denial into a source requirement.

Comparison has exact metadata `schema=1`, `kind="pyalamode-migration-comparison"`, `reference_observed` and lists:

```text
retained_findings,resolved_findings,new_findings,ambiguous_findings,
lost_strict_coverage,new_trust,expanded_effects,expired_approvals,approval_failures,
unsafe_weakening,policy_weakening,inputs_changed
```

All events are `{boundary,before,after,reason,location}`, boundary logical identity|null, category-specific detached before/after rows|null. Finding before/after wrappers are exactly `{finding:<complete group>,count:<retained/new/resolved occurrence delta>,path:<project-relative path>}`; they retain lineage evidence without choosing positional occurrence subsets. Categories are independent and may overlap; no lower total offsets an event. Null reference gives unobserved historical categories while current required-export/expiry/approval events remain visible.

- New trust compares actual transitive operation+contract+dependency identities; latent callables retain trust without adding invocation effects. An unused new approval is a policy event only.
- Expanded effects compares declared bounds and actual required sets separately with engine origins. A new effectful boundary has an entry event.
- Expired approvals examines **all currently configured** approvals at fresh UTC `now >= expires_at`, including unused. Used expiry preserves PAL350 source refusal and may also appear in approval_failures; unused expiry invents no source call.
- Approval failures contains only required actual direct/invoked/retained operations with admission `missing|stale|draft|denied|expired|unresolved`. After row is the exact required-operation row; before is prior matching requirement|null; reason `required-operation-approval-not-current`. This visibility is not a new permission, gate or audit failure.
- Unsafe weakening includes new/changed ordinary unsafe declarations, scope/rationale/body changes and unknown scope implication. A unique unchanged relocation is retained; adapters remain outside checked calls.
- Policy weakening includes removed exports/explicit cases/module requirements, changed globs conservatively review-required, widened/removed effect bound, deny→approved trust, added/widened approval/manifest, weakened migration gate/reference, and reduced guards. Add-only requirements and **removed unused approvals** are tightening. Losing a used approval remains current source/approval evidence.
- Inputs changed reports all current source/inventory/resolution/policy/product/integration identities separately; it does not substitute for approval-failure events.

## 7. Gates, reports and durable IO

Closed migration TOML has exactly schema1, relative baseline and seven exact booleans; omitted gates default false:

```toml
[tool.pyalamode]
required_exports = ["core:total"]

[tool.pyalamode.migration]
schema = 1
baseline = ".pyalamode/baseline.json"
reject_new_findings = true
reject_lost_strict_coverage = true
reject_new_trust = true
reject_expanded_effects = true
reject_expired_approvals = true
reject_unsafe_weakening = true
reject_policy_weakening = true
```

Bad fields/types/selectors/paths/schema and missing/corrupt requested reference are tooling2. Historical true gates (all except current expiry) require valid history outside explicit baseline bootstrap. `evaluate_gates` returns `{status,diagnostics,decisions}`; decision `{gate,enabled,observed,passed,event_count}`, passed null for unobserved history. Diagnostics `{rule,boundary,reason,location}` use PAL360 debt, PAL361 coverage, PAL362 trust, PAL363 effects, PAL364 expiry, PAL365 unsafe, PAL366 ambiguity and PAL367 policy weakening. Identity ambiguity fails enabled debt/coverage identity ratchets. Approval failures preserve engine evidence without changing gate status. Gate false retains events.

Report document is exactly `{schema:1,kind:"pyalamode-migration-report",state,reference_id,comparison,gates,status,verified,claim_scope,human_measurement}`; human measurement exactly `{status:"UNMEASURED",participants:0,attempts:0}`. Report/regions/readiness use a current strict observation status, candidate previews add their own status; baseline recording has its separate receipt axis. No report upgrades audit/history or an unsatisfied source/current/history gate to verified.

Baseline envelope is `{schema:1,kind:"pyalamode-audit-baseline",id,created_at,owner,rationale,previous_id,state,lineage}`. Lineage is sorted `{id,previous_identity_key,current_identity_key,previous_path,current_path,count}` for retained groups. Saved-report envelope is `{schema:1,kind:"pyalamode-saved-report",id,created_at,report}`. Envelope ID hashes canonical contents excluding only itself. Owner/rationale are explicit nonempty strings; created_at is valid UTC `YYYY-MM-DDTHH:MM:SSZ`. Initial previous_id is null; replacement records the actual active predecessor. Forged/missing lineage or history refuses.

Write receipt is exactly `{schema:1,kind:"pyalamode-migration-write-receipt",record_kind,id,path,history_path,previous_id,status:0,verified:false,state_strict_status,current_policy_status}`. Saved-report history_path/previous_id are null. CLI baseline/report-save outer JSON is exactly `{report,written}`; the nested report retains its closed schema and events. Baseline command uses recording0; `report --save` preserves the actual report command status (e.g. strict debt1) while its nested successful write receipt is0; saving cannot turn a failing report into command0. Active baseline destination is normalized `state.policy.migration.baseline`; immutable history remains `.pyalamode/history/ID.json` for both default/custom active paths. Reports are `.pyalamode/reports/ID.json` without a latest cursor.

Active baseline writing refuses the reserved `.pyalamode/history/**` and `.pyalamode/reports/**` namespaces before transaction or directory creation. Those immutable paths remain valid comparison reads; the reference schema is unchanged.

Helper enforces descriptor-relative `O_NOFOLLOW` safe reads/writes, ordinary directories/regular singly linked records, bounded reads with inode/type/size checks, and project-local `.pyalamode` ownership before content access. Refuse absolute/traversal/backslash/empty-dot component references and symlinks, unsafe temp/history/report components and unsupported safe-open environments. Baseline active/history contain the same reviewed envelope; same-ID existing content must be canonically equal, never overwritten with different contents. Historical references may be validated baseline or saved report; original byte receipts remain exact freshness authority.

Stage exclusive same-directory files, flush/fsync and verify. Immediately before immutable history/report publication, required **main** prepublish rereads actual full source inventory/resolution/writers, source/policy/product/native bytes and UTC approval states; helper then rechecks reference/predecessor receipts and descriptor ownership, atomically publishes without clobber. Immediately before active baseline replacement repeat both checks, requiring old active receipt unchanged or still absent initially; atomic replacement plus directory fsync and final ID readback. Cooperative baseline writers hold an exclusive descriptor-local transaction lock before predecessor capture through completion; stale/occupied locks refuse2. Two publications are not a transaction: failure after history publication may leave one complete unreferenced history envelope, preserves old active and returns2, never successful replacement. Clean temporary files on failure; existing records remain unchanged.

Main's callback runs a fresh strict current capture with historical recursion disabled, compares complete captured/live inputs and status/event/expiry evidence, and raises MigrationError on any change; no detached freshness string suffices. It validates reference receipts as well as helper's final check. Expiry crossing during recording refuses2 without publication; debt already expired at capture can be recorded0 with preserved statuses/events. Build repeats complete current/reference freshness immediately before artifact publication; used expiry preserves inherited strict1/no artifact, other changed inputs/reference are tooling2. Current ordinary writers outside copied presentation remain in freshness inventory.

## 8. Readiness and finite conversion

```sh
pyalamode regions [paths] --root PROJECT [--json]
pyalamode ready [paths] --root PROJECT [--json]
pyalamode convert EXACT_TARGET --preview --root PROJECT [--json]
pyalamode baseline --root PROJECT --owner TEXT --rationale TEXT [--replace] [--json]
pyalamode report [paths] --root PROJECT [--compare .pyalamode/baseline.json] [--save] [--json]
```

All accept inherited --target. Conversion function selector is `function:module:qualified.function`; module selector is `module:module.name`. Exact authored conversion target requires one physical matching boundary; duplicate physical matches refuse2 even where engine canonical import selection is known. Unknown/malformed/ambiguous targets return2. Missing --preview is parser2; no apply exists. Empty root-module namespace is inventory/readiness-visible with an explicit no-named-conversion-target blocker, not an invented selector. Baseline always observes all source; report defaults to active baseline if present, explicit missing comparison never becomes empty history.

Regions publishes independent current selection/mode/source/effects/trust/failures/freshness/guards and authored findings; ordinary functions remain off in the denominator. Views retain full state and distinct display rows/counts.

Private candidate selector is closed `{functions:[physical path::qualified-name identities],modules:[physical paths]}` derived from current unique AST declarations. Hypothetical function selection changes discovery and only bypasses the requirement that an otherwise undecorated top-level function already have an opt-in marker. It retains real additional decorator/default/annotation/resolution/writer/call/effect/external/guard/current policy checks and selects nested definitions by existing inheritance. Module hypothetical selection analyzes all actual initialization/definitions without inserting a comment. It neither resolves real marker availability nor creates current checked proof. Root/source paths and selector membership are validated before analysis.

Readiness analyzes all supported ordinary top-level candidates together using this private selector to discover **actual** engine direct invoked and retained callable edges and recursion. Unsupported async/method/generic/duplicate shapes remain blockers/inventory. Conditional callable parameters and unknown dispatch have obligations/blockers, no synthetic callee edge. Only actual current-disk `strict_checked` prerequisites are labeled checked; unverified selected callees retain edges and explicit blockers. Tarjan components appear once with callees before callers, deterministic authored-selector tie order; recursive component members stay together. Each group shows current/hypothetical selection, actual direct/retained edges, checked prerequisites, predecessor blockers, diagnostics/current policy/trust/effect requirements and preview availability. Its contract source_evidence begins `hypothetical candidate analysis:` and freshness explicitly says analysis-only. Local hypothetical success does not mean whole current project passed or predecessors exist on disk.

Finite source proposals are canonical module-header comment; available resolved identity @fun marker for one function/necessary recursive component; inherited straight-line second-binding rename; inherited discarded persistent-update binding. Function adoption needs an actual already available stable import alias/module reference resolving to `pyalamode.fun` before every target declaration, with no analyzed marker/import/writer replacement. Missing/late/shadowed/replaced imports, extra unsupported decorators/defaults or unsafe adapters yield manual blockers, never an inserted import. Recursive members receive actual markers together; predecessor components must already be admitted on disk.

Proposals are in-memory full-text overlays, preserving bodies/defaults/annotations/import initialization and LF/CRLF placement. Module comment follows shebang/encoding/docstring before executable statements. Unsupported encodings/edits refuse a fabricated proposal. After generation, rerun the actual strict current engine **without hypothetical selection** on the complete overlay, including current/history policy. That recheck establishes actual marker availability and declaration evaluation order. Report exact target/component, before/after source, unified diff, snapshot/source identities, candidate diagnostics/policy gates, retained dimensions and limits. Retain untargeted input identities and existing participating effects/trust/failures/operations. Status1/blockers can accompany an adoption proposal; successful conversion requires the whole candidate gate. CLI previews also publish the current report: no-edit/no-candidate results preserve its failure status; actual repair/adoption overlays use their own current/history engine result and may improve the original source status. M9 repair reuse retains its stricter whole-project-passing requirement. Snapshot/class/order/loop/effect/trust/handler/suppression or snapshot insertion remains manual review. No preview changes source, policy or durable records.

## 9. Acceptance and implementation sequence

Reviewer fixed `Docs/conformance/m10-cases.md` before candidate observations; helper literal context dumps and pure count answers are shared authority. In particular: moved debt retains prior ID only with unique lineage; lower-total new debt and duplicate multiplicity fail; duplicate/unknown contexts require review; selection/required export/effect/trust/expiry/unsafe changes remain independent; used expiry overlaps source and approval/expiry evidence while unused denial is no failure; audit0/source-strict1 stays explicit; canonical package export and duplicate authored conversion are separate; first bootstrap preserves current requirements; races publish no stale active/artifact and may leave only a complete orphan history.

- [x] Root approves this reconciled API/schema/ownership plan and releases M10 writes.
- [x] Helper implements detached normalization/matching/gates/closed IO; main implements strict capture, exact inventory/boundary/context/operation extraction, project/model hooks and regions.
- [x] Main implements finite hypothetical selection and SCC readiness, actual overlay conversion/retained dimensions, public commands and isolated migration example/README walkthrough.
- [x] Integrate full-project current/historical policy into check/build/editor diagnostic feed, audit axis, warm bodies, overlays, reference/input/expiry final freshness and explicit product inventory17→19.
- [x] Run meaningful focused owned checks after implementation authorization. Independent fixed conformance remains below; no whole suites or timed observations before root's later freeze.
- [x] Root freezes all product/test/example/controller bytes and runs one authoritative inherited/current suite on actual native macOS and Linux. Both pass401 methods, including current22 main-owned and30 helper-owned methods. Source-suite isolated children use one canonical physical source product; separate installed consumers use the outside wheel with exact byte maps.
- [x] Reviewer runs bounded current M10 commands/cases/nonexecution/pre-read/cache/overlay/build/publication controls against freeze; corrected fresh-installed native/Linux groups pass and actual maps/status/raw projections are independently reconciled by root. Inherited M1–M9 source gates remain applicable because product bytes are unchanged.
- [x] Complete final publication of the approved **untimed structural** cost inventory and controller/raw index. Named denominator/readiness/cache observations and all ten complete published controller/literal inputs are reconciled. No elapsed/memory intervals or universal latency/user benefit claim.
- [x] Reconcile final exact schemas/limits/documentation and return the complete main handoff to root for the forthcoming milestone commit. Human usefulness remains UNMEASURED0; Git itself remains root-owned.

## 10. Main implementation handoff

The main implementation preserves the approved detached helper contract. Current capture uses fresh actual strict analysis and records raw source/current-policy axes; inherited audit exit remains separate. The shared editor receives deduplicated policy diagnostics and unsaved provenance without editor/client source changes. Current default-denied unused native catalog entries create no approval failure; actual direct/invoked/retained sites are explicit. Policy events are excluded from finding debt. Build publication refreshes all current source/writers and exact history receipts, including accepted root output staging, and preserves used-expiry source1 rather than downgrading it to a tooling error.

Focused verification uses the installed `.venv` CPython3.13.1 and actual checkout package path. `.venv/bin/python -m unittest tests.m10_migration` passes all **21** owned checks. They cover recording0/source1/report-save1, inherited audit0/new-debt1, exact 4/9/5 denominators under partial display, current required exports, checked source proof under unrelated policy1, actual direct/retained approvals and earlier PAL240 refusal, unused configured expiry, marker loss/replacement, canonical package versus ambiguous authored conversion, unsaved editor projection, build reference changes, actual prerequisite/cycle/retained edges without shadow-name guesses, candidate provenance, no-edit historical failure, unverified prerequisites, module CRLF/shebang/docstring placement, inherited straight-line repair, late ordinary writers, excluded/outside reads, outside symlink replacement before reread, successful reserved-stage builds and actual late used expiry. Nine targeted inherited checks pass: M9 outside-read, overlays, both repair paths and current external expiry; M8 warm rich external evidence and post-analysis expiry; M7 recursive warm descriptors plus the real console off/exports/debug workflow. A mistaken test-selector invocation was corrected before the successful checks; it changed no test expectation. The inherited M7 product identity count is the sole authorized assertion update17→19. Isolated `python -I` resolves the same canonical checkout product package as the focused source tests.

Root's final source review identified hardcoded default-active paths in CLI bootstrap detection and helper recording. The bounded correction uses safely validated configured active paths for bootstrap and normalized state policy for record/load/predecessor/publication. The additional 22nd main method `.venv/bin/python -m unittest tests.m10_migration.MigrationCase.test_custom_active_baseline_bootstrap_and_replacement_keep_default` passes against stable corrected helper bytes: a valid default old record remains unchanged, first missing custom capture records0 with strict1/current1/current-export events and previous_id null, a repeated initial custom capture refuses2 without overwrite, and explicit replacement follows the custom predecessor. The 21-test main run and nine inherited checks above preceded this correction; they were not broadly rerun. Helper reports 30 focused tests passing, including custom nested paths and writer-only immutable-namespace refusal. Final full/frozen verification remains root-owned.

The isolated example is an intentionally failing checked total plus one ordinary function. Its focused test records existing debt, previews and manually applies the finite repair in a temporary project, saves a passing report, previews and manually adopts the ordinary function, then observes no remaining ordinary candidate. The published example itself remains unchanged. The example and README make no measured human benefit claim.

Root owns the joint freeze, full native/Linux suite, independently installed command/conformance/artifact observations, approved untimed structural cost inventory and Git milestone. Main stops editing product/test/example/README bytes after the freeze except for a concrete root-authorized correction. Root and corrected peer engineering results and final publication reconciliation below are observed evidence; the Git milestone is forthcoming and root-owned. No elapsed-cost interval, human adoption benefit, remote/CatWrangler action, scheduling, new chat or Git commit is claimed by this worker.

## 11. Observed root engineering gates

Root source packet `/tmp/pyalamode-m10-root-freeze.json`, SHA-256 `20d293ccb4781b64fc16ada3eff48f4b5951c135d8eb8e6930a23f6fda5f98a5`, binds99 complete source/test/example/editor/benchmark/README/spec inputs,20 package files,19 foundation byte identities and three root controllers. The corrected custom-active implementation is included: main22 methods and helper30 methods. Evolving final evidence prose is excluded from those99 source identities; this doc-only update does not change the frozen source or the pre-freeze intent.

The actual root raw index `/tmp/pyalamode-root-m10-evidence/root-summary.json`, SHA-256 `9f93ebeaf509f9ab24f695471110c1560eb9061fdcf8927250eba15b0bb4bdaa`, records the following results. Its nine raw-file digests match the files read for this handoff. Both suite records have exit0 and identical before/after maps equal to all99 frozen inputs.

| Root observation | Native macOS arm64 | Linux aarch64 |
| --- | --- | --- |
| Full inherited/current source suite | 401 methods, exit0, OK | 401 methods, exit0, OK |
| Unittest-reported suite duration | 21.499 seconds | 80.526 seconds |
| Fixed real-console root walk | 62 assertions across23 commands, passed | 62 assertions across23 commands, passed |

The durations are verification-harness records, not migration latency or human authoring-cost measurements. The supported interpreter remains exact CPython3.13.1 standard GIL with UTF-8 filesystem encoding and surrogateescape errors. Native source evidence records UTF-8 mode0; Linux source evidence records mode1. Source suites and installed consumers are separate single-physical-product environments: native uses the editable checkout product in `.venv`, Linux source uses canonical `/workspace` via its source setup, and the fresh Linux consumer uses `/selected/lib/python3.13/site-packages/pyalamode` with no checkout on sys.path. Neither source suite mixes its physical source package with the outside installed wheel.

The outside-copy wheel is `/tmp/pyalamode-root-m10-evidence/wheels/pyalamode-0.1.0-py3-none-any.whl`, SHA-256 `dc04c689b6d44d73aa6f3d2206407f4addf33a3725a62662c8a9230166a92798`. Its20 package-file map and the fresh Linux installed map exactly equal the frozen package map. Root's native console walk exercises the native source environment; root's Linux console walk exercises the separate fresh installed consumer. Corrected peer verification below is the separate fresh installed native/Linux gate.

The fixed root walks observe baseline command0 with unverified receipt and stored strict1, unchanged reviewed audit0, strict check/build1 with no artifact, line-shift finding retention, lower-total independently new/resolved debt and audit ratchet1, read views preserving source/records, and report-save command1 with receipt0 and unchanged baseline. They also observe successful ordinary artifact execution, independent marker-loss coverage, current required-export1/no new artifact while retaining a prior artifact, reviewed replacement0 that cannot waive the export requirement, nonexecution of application setup/default sentinels, and unsupported target2 with no saved report. These are actual command projections, not inferred gate claims.

Root separately read and froze ten peer controller/literal inputs. Initial peer intent SHA-256 `e348c9c5b7190caafcf2cc6df22febacff8779f3c0bcc30ab9b1e3ea9766064a` was superseded by the corrected v2 intent below, retaining the same product/source freeze. All human measurement remains exactly **UNMEASURED**, participants0 and attempts0. No suite, timing or candidate command was rerun for these doc-only handoff updates.

## 12. Corrected peer acceptance and structural observations

The first fresh installed runs passed CLI and denominator controls, then the ordinary readiness fixture `uses_checked(value) -> checked(value)` correctly produced PAL102/PAL221: its unchecked parameter annotation could not establish an exact int argument. Root authorized the single fixture-call correction to `checked(1)`. It preserves the actual prerequisite edge and strict0/graph expectation using a characterized literal input; it does not weaken checker admission. Initial failed raw records remain preserved. Product, tests, examples and README are unchanged, so the401-method source suite gates remain valid.

Corrected peer v2 intent `/tmp/pyalamode-m10-review/freeze-intent-v2.json`, SHA-256 `f76ca01ab24f0e5f0298efaab8171cf5d18c3e7045f44978c9276534eff9f17a`, binds ten complete peer controller/literal inputs to the root source freeze. All five bounded groups pass in both fresh installed native and Linux consumers. The authoritative root reconciliation is `/tmp/pyalamode-root-m10-evidence/peer-reconciliation.json`, SHA-256 `d743f28141dd896bd98e0d2dff511f9f09fc16f06ac1f9c05798dc44f6dd1501`; its controller `/tmp/pyalamode_m10_reconcile.py` checks actual raw hashes, current wheel contents, installed files, status projections and phase maps without product execution.

Each platform records seven before/cross/after phases with exact99 source,3 root controller,10 peer controller,20 package and19 foundation maps. Installed provenance resolves one product root, all19 loaded product files remain within it, and no checkout/workspace source appears on sys.path. Peer native wheel SHA-256 is `635155a39641e561ad3eecaaba14b83279d4ffa7bc9d566e20ff9c9ccfad2c9a`; peer Linux wheel SHA-256 is `b43e7ba9bfe321a09d789615c0a81b2ad2643109af38815eb80da71b0404ad7c`. Each wheel's complete20 Python-file map and its fresh installed consumer map equal the frozen package map.

Per platform, the peer observes26 real console commands (19 CLI and7 record-IO),15 structural rows,18 record-IO rows and3 build races. Root reconciles literal exits, independent unsafe-body/unused-manifest/new-trust/effect/unused-expiry categories, actual record errors and preserved ownership, and each tooling2 race with no new artifact and a genuinely successful prior artifact unchanged. The late-expiry group starts with strict check/source status0, changes only the UTC clock at facade generation, and reaches actual PAL350 source/build status1 with no artifact; it does not inject a diagnostic or synthetic refusal. Root independently rehashes five actual native identity files on each platform. Actual native dependency digests are macOS `092176aeea2377cdf71314afaed761a6b62c53aa59504f7585d775b55bf1f06a` and Linux `430ed7dacb60115b707ce7d84cab3254735c7cfdc93858ae9237ceddb88bdf4f`.

Both platforms agree on the named untimed inventories:

| Observation | Reconciled value |
| --- | --- |
| Denominator source bytes | 794 |
| Eligible / selected / checked modules | 4 / 1 / 1 |
| Eligible / selected / checked functions | 9 / 4 / 4 |
| Checked public exports | 5 |
| Selected records / variants | 1 / 1 |
| Published exclusions | 9 |
| Readiness SCC groups | 10 |
| Actual direct / retained edges | 7 / 12, total19 |
| Cold body-cache hits | false for all4 captured files |
| Current warm body-cache hits | true for all4 captured files |

The cold/current-warm reports each retain `analyzed_call_sites=2`; that is stored descriptor evidence, not two newly analyzed body calls on a cache hit. These are bounded structural observations of the named fixtures, with no elapsed/memory interval or universal project-cost/authoring benefit claim. Final peer controller-text/raw-index publication and root reconciliation of that publication are observed below. All engineering gates described here are observed; human usefulness remains **UNMEASURED**, participants0 and attempts0.

## 13. Final publication closure

Peer's final `/tmp/pyalamode-m10-review/evidence-index.json` has outcome PASS and SHA-256 `cf5e66ed4abe1baccc165f866ba297f5ff187321deeda252fdab589d6d92eec0`. Complete published `Docs/conformance/m10-cases.md` has SHA-256 `164dba12d0169d6e7e5691962bd9af39eea8bb4a2d872bb7e2e3df673f4c0150`. Root's final `/tmp/pyalamode_m10_publication.py` reconciliation passes131 actual raw-file SHA/byte records,102 expected/observed projections,52 actual console commands and10 exact complete published controller/literal inputs. It compares actual stdout/stderr digests and exits against raw commands, verifies wheel members and publication receipts, and requires each published controller body to equal its frozen current file. Bounded helper exceptions retain their actual exception classification; independently exercised CLI errors supply numeric exit2 where a CLI is used. The independent concurrent writer remains preserved after the controlled rollback refusal.

Final structural publication, exact schema/evidence reconciliation and the main handoff are complete for root's forthcoming milestone commit. Product/test/example/README/source-intent bytes remain unchanged, and no suite, timing or candidate command was rerun to close this document. Root owns the remaining Git action; this handoff does not claim that it has already occurred. Human usefulness remains **UNMEASURED**, participants0 and attempts0.
