# M10 independent migration and team-policy conformance

**Status:** fixed expectations and five bounded frozen fresh-installed groups PASS on native macOS and Linux. Initial fixture failures, the root-approved one-line correction and raw final observations are retained below. No workload interval or human usefulness claim is made. Root owns final milestone acceptance and Git. This reviewer owns only this document and bounded probes under `/tmp/pyalamode-m10-review`.

Authority read: complete `SPEC-sol6.1-composite.md`, README, acceptance matrix, orchestration ledger, M1–M9 milestone handoffs, current project/model/CLI contracts and relevant source graph, resolution, writer, invocation, approval and editor-preview implementation. Main proposal: `Docs/milestones/10-migration.md`; helper proposal: `Docs/evidence/m10-policy.md`. The user authorized local parallel work and excluded CatWrangler, remote writes, deployments and scheduling. Those explicit limits take precedence over the orchestrate skill's top-level-session/CatWrangler workflow. No applicable AGENTS.md was found in workspace ancestors.

M8 `ec580b0` is independently verified. Root has accepted and committed M9 as `dfe408f`, after verification against `/tmp/pyalamode-m09-root-freeze.json`, SHA-256 `57575e0779f28f5b4bf7b961756027fefc34ac9be1a36de48f8050ffbefeeb01`. Product/test/example/client/README files remain read-only to this reviewer. Root has released bounded main and helper implementation after joint schema/API reconciliation. Independent candidate observation still requires a later root-declared freeze.

M10 adds observation, adoption proposals and local team gates, with no new admitted Python behavior. Historical M1–M9 contracts remain authoritative for unchanged data/runtime/operation semantics; this document does not reprint or rerun their complete unrelated corpora. Human migration usefulness and authoring effort remain **UNMEASURED**, participants 0 and attempts 0.

## Fixed status and claim axes

The axes below are independent. A successful recording command is not a strict check. A passing debt ratchet is not source certification. Tooling and unsupported targets are never clean reports.

| Observation | Command result | Required evidence |
| --- | --- | --- |
| Reviewed baseline records current PAL101 audit debt | Recording status 0, `verified=false` | Saved `state.strict_status=1`, current findings and coverage; subsequent strict check/build 1, no artifact. |
| Baseline records current required-export or used/unused expiry policy debt | Recording status 0, `verified=false` | Preserve current policy/report status 1 and all events, plus source strict status. Normal check/build continues to enforce current failures. |
| `report --save` stores a failing strict source/policy report | Command keeps report status 1 | Outer JSON is exactly `{report,written}`; the closed report retains failure/events while successful write receipt is status0/verifiedfalse. Baseline uses the same wrapper but returns recording status0. |
| First baseline with enabled historical ratchets but no active reference | Recording may succeed | Bypass only recursive missing-historical-reference evaluation. Still capture actual current source/coverage/effects/trust/expiry/unsafe/current policy evidence. No certified source claim results. |
| Explicit replacement requests missing/corrupt predecessor | Status 2, no write | Preserve active/history/report bytes and any prior artifact. Never treat replacement as first recording. |
| Audit with existing reviewed source debt and satisfied enabled policy | Status 0, `verified=false` | Findings remain; checked behavior/effect claims remain unverified. |
| Audit with distinct new finding or enabled independent change gate | Status 1, `verified=false` | New debt/policy event remains visible even if old debt decreases. |
| Current strict source failure, whether baselined or suppressed for presentation | Strict check/build 1 | No artifact and no strict waiver. |
| Current required external approval missing/stale/draft/denied/expired | Existing strict source status 1/PAL350, approval-failure event | Audit with no selected gate retains inherited findings-only status 0/unverified; the report preserves the underlying strict classification. This category adds no gate. |
| Malformed policy/reference, stale capture, unsupported runtime/filesystem target, unsafe local-record IO | Status 2 | No durable write, checked artifact, source evaluation or clean ratchet. |

Main-owned final freshness validation is required immediately before durable publication: reread source and resolution inventory, policy, product, actual integration bytes/approval UTC expiry and predecessor/reference receipts. Detached state alone cannot establish a fresh write. The helper owns no application/project/checker/editor import. Saved state is historical evidence and never skips current analysis.

The root-approved comparison categories now include explicit **`approval_failures`**. This current-state category is independent of historical debt/trust differences and uses actual currently selected direct/invoked/retained operation requirements, preserving their engine status/rule/evidence. Used expiry may appear here and in `expired_approvals`; expiry examines configured unused approvals too. Default-denied unused catalog rows are not failures. Removing an unused approval is tightening; removing a required approval remains a current engine refusal. No new audit gate, trust permission or purity claim is introduced.

## Normalized context literals fixed before candidate observation

Finding identity uses rule, logical boundary and normalized violation context, with origin included. Line/column/end ranges, first-binding coordinates, absolute root and human reason/remediation text are review metadata, not identity. The context is the smallest containing `ast.stmt`; when the engine emits over a whole declaration that declaration is the context. Module diagnostics use a logical module boundary. Missing source/context and duplicate physical declarations with one logical identity require review, not a guessed position or text match. PAL001/PAL002 are tooling evidence and cannot become baseline debt.

The normalizer is fixed to `ast.dump(node, annotate_fields=True, include_attributes=False, show_empty=False)` on the supported CPython 3.13.1. The literal dumps below were checked only by a stdlib-only isolated AST generator; that is not an M10 candidate observation. The generator and detached JSON are `/tmp/pyalamode-m10-review/context_literals.py` and `context-literals.json`.

```python
CONTEXT_LITERALS = {
    "C101": ("PAL101", "static source", "value = value + 1\n",
        "Assign(targets=[Name(id='value', ctx=Store())], value=BinOp(left=Name(id='value', ctx=Load()), op=Add(), right=Constant(value=1)))"),
    "C221": ("PAL221", "static source", "return leaf(True)\n",
        "Return(value=Call(func=Name(id='leaf', ctx=Load()), args=[Constant(value=True)]))"),
    "C230": ("PAL230", "static source", "return unknown(value)\n",
        "Return(value=Call(func=Name(id='unknown', ctx=Load()), args=[Name(id='value', ctx=Load())]))"),
    "C241": ("PAL241", "static source", "import os\n",
        "Import(names=[alias(name='os')])"),
    "C250": ("PAL250", "persistent return-only operation", "values.appended(1)\n",
        "Expr(value=Call(func=Attribute(value=Name(id='values', ctx=Load()), attr='appended', ctx=Load()), args=[Constant(value=1)]))"),
    "C310": ("PAL310", "project effect policy",
        "@effects(Clock)\ndef now(clock: ClockCapability) -> int:\n    return clock.now_ns()\n",
        "FunctionDef(name='now', args=arguments(args=[arg(arg='clock', annotation=Name(id='ClockCapability', ctx=Load()))]), body=[Return(value=Call(func=Attribute(value=Name(id='clock', ctx=Load()), attr='now_ns', ctx=Load())))], decorator_list=[Call(func=Name(id='effects', ctx=Load()), args=[Name(id='Clock', ctx=Load())])], returns=Name(id='int', ctx=Load()))"),
    "C350": ("PAL350", "external operation policy", "return sha256_digest(data)\n",
        "Return(value=Call(func=Name(id='sha256_digest', ctx=Load()), args=[Name(id='data', ctx=Load())]))"),
}
```

C101 belongs to the second assignment, C221 to the containing return although a diagnostic may begin on `True`, C230/C350 to the return, C241 to module initialization, C250 to the expression statement, and declaration-emitted C310 to the full function including decorator/annotations/body. The contexts are intentionally conservative syntax evidence; changing the statement's constant/callee/argument/declaration is not semantic-equivalence matching. A second diagnostic on the same statement with a different rule/origin is a distinct identity group.

Finding rows are **groups** with current `identity_key`, immutable `birth_identity` hashed to `id`, `count` and current `locations`. Initial capture uses birth=current identity. A unique relocation retains birth/id in comparison and explicitly reviewed replacement. Occurrences have no inferred positional identity.

| Identity transition | Fixed PAL101 projection |
| --- | --- |
| One old occurrence, one current occurrence; only blank lines/comments/indentation/newline encoding changes | retained 1, resolved 0, new 0; same group ID, updated locations. |
| One old occurrence duplicated identically within its same boundary | retained 1, new 1; count 1→2; enabled new-debt gate 1. |
| Two old identical occurrences, one current occurrence | retained 1, resolved 1, new 0; no claim which positional occurrence disappeared. |
| Two old duplicate occurrences reordered or separated by unrelated statements | retain multiplicity; no new debt from coordinates/order alone. |
| Same statement/rule but different origin or enclosing logical boundary | Distinct current identity; never silently retained by statement text alone. |
| Unique `core:f`→`moved:f`, same kind/name/parameter-result syntax/violation context | Retain prior birth/id and count; show both paths. Moving debt does not resolve it. |
| Multiple old/current `f` candidates with the same relocation evidence | Ambiguous event, no guessed retained pairing; enabled identity ratchet 1. |
| Rename or move with changed contract/context | Lost/new or ambiguous as supported by exact evidence; never guessed retained. |
| Source unavailable, context point outside all eligible statements, incompatible identity version | Review/tooling classification explicitly visible; never clean ratchet or automatic resolved debt. |

## Independent debt and coverage cases

All command inputs are isolated full projects. Reports preserve every comparison category even if a gate is disabled. The fixed table asserts meaningful category membership and counts where defined, not implementation-specific list order.

| ID | Fixture/transition | Fixed result |
| --- | --- | --- |
| D01 | Baseline three independent PAL101 groups `a`, `b`, `c`; fix `a` and `b`, add same violation to new `d` | PAL101 retained 1/resolved 2/new 1; total 3→2; audit new-debt ratchet 1. Strict build 1/no artifact. |
| D02 | Insert blank lines/comments before old PAL101 in `f` | Same debt ID and new=0; audit ratchet 0; strict 1/no artifact. |
| D03 | Uniquely move entire decorated `f` with unchanged signature/violation from `core.py` to `moved.py` | Retained old ID; report records old/current paths, new=0. Ordinary reviewed move does not erase debt. |
| D04 | Baseline two `f` debt boundaries; move both to two new modules with identical signatures/contexts | Ambiguous pairing, no fabricated location mapping; enabled identity ratchet 1. Explicit replacement can record reviewed current groups without certifying them. |
| D05 | Add identical second discarded `values.appended(1)` to one selected function | PAL250 count 1→2, new occurrence 1. Lower unrelated totals cannot offset it. |
| D06 | Change `unknown(value)` to `other(value)` | New normalized PAL230 context. Familiar unsupported spelling does not inherit old debt. |
| D07 | Preserve violation statement but move it from `f` into nested `f.inner` | Logical boundary changes; absent unique same-qualified-name relocation, new/lost or explicit ambiguity. |
| D08 | Add two diagnostic categories on one statement | Both rule/origin groups survive; no deduplication by line only. |
| D09 | Remove `@fun` from formerly passing `core:total` | Lost function/export strict coverage; selected denominator drops visibly; enabled coverage gate 1 despite findings 0. |
| D10 | Remove a valid functional-module header while keeping ordinary functions | Lost module initialization and selected-function/export coverage separately visible. |
| D11 | Remove a `require_modules` pattern which selected valid module mode | Structural policy weakening plus lost current coverage when applicable; gate 1 independently. |
| D12 | Keep marker but introduce actual ordinary writer `core.total.__code__ = ...` in another file; CLI displays only core | Full-project gate observes writer, lost verified coverage and source refusal. Partial presentation cannot hide it. |
| D13 | Formerly strict export acquires source/dependency PAL240/PAL241 | Lost checked coverage although selected counts remain unchanged. |
| D14 | Move a passing strict function uniquely with same name/signature/normalized body | Coverage follows unique authored relocation; debt and coverage matching remain separately evidenced. |
| D15 | `required_exports=["core:total"]`, target absent, ordinary, private/nested, duplicate selected definition or source-unverified | Current coverage failure 1 for absent/ordinary/unverified; malformed/private/nested selector or ambiguous target tooling 2. No build artifact. |
| D16 | Remove a required export entry without changing source | Policy weakening independently visible even if that function remains voluntarily checked. |
| D17 | Add a required export/current module requirement or narrow effect bound | Added requirement alone is not weakening; current source must still satisfy it. |
| D18 | Deleted source file or new outside/symlink-resolved dependency | No silent disappearance from a required current target/reference; explicit loss or tooling2 before outside read. |
| D19 | PAL101 statement contains U+2028 inside an ordinary string literal on physical line4 | Source line slicing recognizes only CR/LF/CRLF, matching CPython coordinates. U+2028 stays in the same string/statement; exact normalized Assign context remains available, never mislocated/unavailable from str.splitlines(). |

Duplicate physical package/module files retain the inherited M9 actual-resolution rules. Required-export selection must not invent a successful target from whichever file was traversed last. A canonical imported package has its actual schema; genuinely ambiguous authored selection refuses 2. Duplicate logical debt declarations require review. Guard selection retains its independent inherited duplicate-module refusal.

## Independent effect, trust, expiry, unsafe and policy cases

Use actual temporary reviewed native operation/dependency identities only after future source freeze. No production approval is written. Synthetic helper-state fixtures may pin deterministic UTC event comparison without impersonating actual installed-operation conformance.

| ID | Change | Fixed event/gate |
| --- | --- | --- |
| P01 | Pure valid boundary becomes `@effects(Clock)` with an unchanged return | Expanded declared effects even when required effects remain empty; enabled gate 1. |
| P02 | Already Clock-declared boundary starts calling `clock.now_ns()` | Expanded required effects with actual origin; bound need not change. |
| P03 | Higher-order/eager callback adds Clock; fake/recorded provider used | Propagated required/declaration union is retained, effects gate 1; provider substitution never erases classification. |
| P04 | Retain an effectful callable without invoking it | Callable assumptions retained; no invented invocation effect. If only retained assumptions changed, report that actual dimension. |
| P05 | Add approved SHA operation through direct wrapper/caller | Actual transitive new trust includes operation/contract/dependency/approval identity; enabled gate 1. |
| P06 | Return/capture/compose/partially bind approved external wrapper without invoking it | Latent trust propagates to every relevant boundary; no false invocation effect/failure claim. |
| P07 | Catch known ValueError around new trusted operation | Failure masking cannot hide new trust/effects. |
| P08 | Add one unused approval or widen `external_trust` | Policy event visible; no claim existing boundaries consumed that operation. |
| P09 | Same operation changes approved contract/dependency identity | New/changed trust identity independently visible; familiar operation name alone cannot retain unchanged assumption. |
| P10 | Used approval expires while source/policy/cache are unchanged | Current PAL350 strict1 plus expiry event/gate1; no artifact. |
| P11 | Unused configured approval expires | Independent expiry event/gate1; no fabricated source call/PAL350 consumer. |
| P12 | Approval reaches exact UTC expiry instant | Expired, never still current at equality. Baseline replacement cannot waive current expiry. |
| P13 | Shorten expiry, change owner/rationale/provenance or remove unused approval | All approval changes visible; weakening classification follows exact finite policy contract, never inferred consumed trust. |
| P14 | Add ordinary `@unsafe(scope="legacy", rationale="reviewed shell")` | Unsafe weakening event even if no selected call/debt; gate1 when enabled. |
| P15 | Change unsafe scope or rationale | Review-required unsafe event; new declaration is not automatically safer from prose. |
| P16 | Pure/all-effects checked function calls unsafe adapter | Inherited strict source refusal, never baseline-waived. Snapshot output starts only a separate new checked computation. |
| P17 | Remove/narrow migration gate, redirect baseline, or explicitly replace baseline | Reviewable policy/reference change; weakened protection appears separately from accepted findings. |
| P18 | Remove/narrow required explicit-case policy | Structural policy weakening; wildcard/exhaustiveness follows inherited source rules. |
| P19 | Remove/widen `effect_bounds` entry | Policy weakening even if observed current required effects happen to be unchanged. |
| P20 | Change existing module glob string | Conservative review-required policy weakening unless byte-identical or a recognized added requirement; no arbitrary glob implication claim. |
| P21 | Exports/debug guard selection reduced or guards off | Lost additional boundary protection/policy event; no invented loss of static correctness when source still passes. |
| P22 | Fix all audit debt while independently removing marker, expanding effects, adding trust and expiring unused approval | All four independent changes survive findings total→0; enabled gates1. |
| P23 | Currently required SHA wrapper lacks approval, with no reference | `approval_failures` contains actual operation, required boundary/path/via and existing PAL350 strict1 evidence; historical categories are unobserved. Unused denied Base64 catalog entries absent from this category. |
| P24 | Actual required direct/transitive/retained operation approval is independently stale, draft, denied, expired or unresolved | Current approval-failure row preserves exact actual admission and engine status/rule. Unresolved installed identity keeps its source/tooling classification; no fabricated digest or clean current state. |
| P25 | Remove a previously approved unused operation | No approval-failure or consumed new-trust event; removal is tightening. Actual configured table/input change remains visible. |
| P26 | Remove approval for operation retained only through returned/composed checked wrapper | Actual retained requirement survives; current approval failure/PAL350 source refusal cannot disappear from lower invocation/finding counts. |
| P27 | Used approval expires | One actual requirement may appear in both current approval failures and configured expiry. Neither category erases the other or creates duplicate fictitious source calls. |
| P28 | Ordinary audit observes required PAL350 source debt with all optional team gates disabled | Findings-only command0, verifiedfalse, strict_status1 and current approval failure visible; strict check/build1/noartifact. |
| P29 | Ordinary unsafe adapter changes only its body `return 1`→`return 2`; scope/rationale and selector are byte-identical | Actual boundary definition_sha256 changes; independent unsafe-weakening event and enabled gate1. Scope/rationale equality cannot hide changed unchecked behavior. No checked-adapter claim. |
| P30 | Same configured manifest path changes the actual contract of an unused operation, e.g. empty effects become Clock | Actual current contract identity/policy-input change yields independent review-required policy-weakening event and enabled gate1, plus inputs_changed. No consumed new-trust/approval-failure event or fabricated source consumer. Unchanged manifest path string cannot erase changed contract protection. |

## Fixed denominators and readiness graph

The denominator fixture has exactly four eligible physical Python modules: empty `__init__.py`, `core.py`, `plain.py`, `strict.py`. `core.py` declares a public selected record `Customer`, a public selected variant `Choice` with two cases, selected `@fun total` containing selected `plus`, selected `@effects(Clock) now`, ordinary `ordinary`, async `deferred`, ordinary `Service.method`, and unsafe ordinary `raw`. `plain.py` has ordinary `unused`; `strict.py` has a valid header and selected `double`. All signatures/bodies use inherited admitted syntax, except excluded ordinary shapes remain unchecked.

Required published counts: eligible modules 4, selected/checked modules 1; eligible functions 9, selected/checked functions 4; selected records 1, variants 1. Public checked top-level exports are `core:total`, `core:now`, `strict:double`, `core:Customer`, `core:Choice`: 5. Nested plus is a checked function but not a public top-level export. Case declarations do not inflate function count. Ordinary/async/method/unsafe definitions remain in eligible inventory with explicit off/excluded/blocker status; they do not acquire contracts by annotation. The project denominator stays identical when presentation selects only `plain.py`; displayed counts and project counts remain distinct.

Root fixes the empty project-root `__init__.py` as a physical eligible module with internal `kind="module"`, `selector="module:"`, `qualified_name=""` and `path="__init__.py"`. It receives no invented named export namespace. Readiness/conversion exposes its missing named target as an explicit blocker; public authored selectors cannot silently reinterpret the empty identity as a named module.

Excluded source locations are published with reasons: `.git`, `.venv`, `__pycache__`, `build`, `dist`, `.pyalamode-cache`, `.pyalamode` and `*.egg-info`. Place a Python poison file in each excluded directory; no body analysis or current checked claim for these files. Exclusion does not silently mean checked. No whole-project functional percentage is inferred from the selected numerator.

The readiness fixture uses ordinary top-level exact-int functions with a stable existing `from pyalamode import fun`, plus independently already-checked prerequisite `checked`. Actual edges are fixed:

```text
leaf -> no candidate
middle -> leaf
outer -> middle
left -> right
right -> left
uses_cycle -> left
factory -> leaf              # retained returned Callable, not invoked here
uses_alias -> leaf           # stable actual import alias from dependency
uses_checked -> checked     # already checked prerequisite
shadow(leaf: Callable[[int],int]) -> conditional obligation; no concrete leaf edge
unknown -> unresolved call; blocker, no fabricated edge
```

| ID | Required readiness/preview observation |
| --- | --- |
| R01 | Tarjan output groups `{leaf}`, `{middle}`, `{outer}`, `{left,right}`, `{uses_cycle}` exactly once; dependency partial order leaf before middle before outer and cycle before uses_cycle. Independent groups may have any documented stable tie order. |
| R02 | Retained factory/import-alias dependencies order actual leaf before consumers; shared spelling/parameter shadow cannot invent an edge. Direct and retained edges remain separately labeled. |
| R03 | `{left,right}` is one necessary recursive adoption component; exact member request previews both markers atomically or explicit component blocker, never a falsely checked single member. |
| R04 | `outer` before leaf/middle disk adoption | Reviewable remaining predecessor blockers; no claim of ready strict conversion from hypothetical predecessor success. |
| R05 | Valid target with already checked prerequisites | Existing resolved marker inserted at available declaration, unchanged body/defaults/annotations/import initialization; full-project candidate gate and dimensions reported. |
| R06 | Missing/late/shadowed/replaced marker import, unsupported additional decorator/default, class method/async/generic/duplicate target | Manual-review blocker or selector tooling2; never add an import or guess stable marker identity. |
| R07 | Module adoption | Comment after shebang, encoding and module docstring, before executable source. Preserve LF/CRLF and source bytes elsewhere; analyze all initialization and selected definitions. |
| R08 | Module has ordinary effectful setup/unsafe adapter/native adapter import | Show initialization blocker; no fabricated functional module claim because one export is pure. |
| R09 | Exact `function:module:qname`, `module:name`; source module literally named `module` | Kind prefix disambiguates. Unknown/malformed/ambiguous selector2. No apply command; missing `--preview` parsing2. |
| R10 | Straight-line second-binding repair | Preserve old-value RHS; rename only second target and later lexical reads to a fresh name. Full-project strict candidate passes; existing trust/effect/failure/operation dimensions unchanged. |
| R11 | Discarded persistent update repair | Bind original expression once to fresh local; original return stays unchanged, retained old/new value choice visibly remains for human. |
| R12 | Closure, branch, alias, callback/capability, third rebinding, snapshot/class/order/loop/effect/trust/handler/suppression change | Bounded no-edit/manual-review result. M9 conservative preview restrictions remain inherited. |
| R13 | Unrelated project error, failed policy ratchet or changed untargeted dependency/reference during preview | No successful full-project conversion claim; blockers/status/freshness explicit. No source/policy/baseline/report write. |

Finite literal repair references are `result=value; result=result+1; return result`, expected ordinary result `value+1`, and `values.appended(1); return values`, expected original Vector returned. A preexisting `result_2` forces another fresh name. Runtime equivalence checks happen only after future root approval/freeze in separately identified ordinary subprocesses; static evidence never executes these sources.

## Local records, malformed files and race cases

Closed canonical JSON must reject duplicate keys, NaN/Infinity, booleans standing in for integer schema/count/status, unexpected fields, incompatible versions, forged content IDs and unreasonable recursive/size inputs with bounded tooling2. Sorted-key compact canonical bytes determine IDs; pretty indent/newline is the published representation. Semantic array order is retained; unordered inventories are documented and deterministically sorted. Record `id` excludes only itself when hashing, so changed owner/rationale/state/previous pointer invalidates the ID.

| ID | Record/protocol sequence | Fixed result |
| --- | --- | --- |
| L01 | First valid baseline | Active and `.pyalamode/history/<id>.json` contain the same exact reviewed envelope; UTC created time, owner/rationale and `previous_id=null`; explicit written paths/ID output. |
| L02 | Baseline again without `--replace` | Tooling2/no overwrite. With reviewed replacement, new ID/history plus `previous_id=old`; old history preserved byte-for-byte. |
| L03 | Equivalent baseline content serialized with different key order/whitespace | Hash canonical content; parsing format alone cannot corrupt identity. Ordered source/case/parameter content cannot be arbitrarily sorted away. |
| L04 | Existing history ID contains different content; active predecessor ID/state corrupt | Tooling2; never overwrite collision or trust corruption. |
| L05 | `report` without `--save`, `regions`, `ready`, `convert --preview`, check/build | No active/history/report writes. Check cache changes remain separately disposable. |
| L06 | `report --save` | Explicit content-addressed report only; no baseline/latest cursor change. Save same ID reuses verified exact content, not different content. |
| L07 | Explicit comparison missing; true historical gate without baseline; malformed configured reference | Tooling2 for normal observation; no fallback to empty historical clean state. First baseline exception is only fixed bootstrap above. |
| L08 | References absolute/outside `.pyalamode`, `..`, backslashes/escape, symlinked record/directory/history/report/temp component | Refuse before outside content read or write; status2. Audit-hook probe must observe zero outside opens. |
| L09 | Change selected source, add/remove source/import winner/writer, policy, product, actual dependency or expiry between capture and write | Freshness2/no durable publication; original active/history/report preserved. |
| L10 | Change/delete predecessor/reference between validation and publication | Receipt mismatch2; no artifact or active replacement using unchecked predecessor. |
| L11 | Unwritable `.pyalamode`, invalid owner/rationale, failing atomic replacement | Status2; no best-effort successful recording. Stage cleanup and original active preservation observed. |
| L12 | Required reference changes after successful build check but during guard generation/staging | Freshness2/no published artifact; prior artifact untouched. |
| L13 | Delete/corrupt/unwriteable `.pyalamode-cache` | Fresh analysis, same source/debt/coverage/policy classification. Never regenerate or lose baseline/history from cache failure. |
| L14 | Delete `.pyalamode/baseline.json` while warm source cache remains | Required team gate tooling2. Body hit cannot stand in for review state. |
| L15 | Root relocation/copy to another absolute directory | Logical debt/coverage match where authored relative/module identities are unchanged; observed source/product/native provenance refreshed, never old absolute IO authority. |
| L16 | Report without reference and with no historical gate | Historical comparisons explicitly unobserved; current expiry/unsafe/denominator visible, no invented retained/resolved history. |
| L17 | Used native SHA approval is current during strict check/build copy, then reaches exact UTC expiry after guard generation and before publication | Earlier saved raw source_status0 must update to actual late strict source_status1; PAL350/integration-freshness evidence, build status1, no artifact and staging cleaned. No PAL001 downgrade or new audit gate. Root identified this source-status risk before independent candidate observation. |
| L18 | Valid project builds successfully to `root/accepted`, with a temporary `.pyalamode-build-*` directory under the root during final full-project recapture | Build0, actual compatible artifact and stage cleanup. Only the reserved internal staging prefix is excluded with published reason; explicit staged-source display target refuses2. Published `accepted/*.py` remains eligible, never hidden as arbitrary user output. |
| L19 | After actual guard generation, change source/reference or introduce a new ordinary writer before publication | Complete final source/inventory/resolution/reference freshness refuses2/no new artifact; prior artifact bytes remain unchanged. Existing late used approval expiry keeps L17's strict1 classification. |
| L20 | Controlled temporary write/fsync failure before stage-context yield, or controlled active directory-fsync/readback failure after replacement | Tooling2, temporary files cleaned, previous active bytes or initial absence restored; complete orphan history is the sole permitted residue. Rollback first verifies active is the record this writer published. A noncooperative replacement keeps its own bytes; never blindly overwrite a new writer to pretend prior-state preservation. |
| L21 | Validly hashed predecessor/child envelopes claim retained old `A:f`/`B:f` IDs through ambiguous identical relocation to `C:f`/`D:f` | Reference load2 even when IDs, compatible context/counts/paths and hash chain are individually correct. Loader must compare verified predecessor against child with births reset to current and establish actual unique retention. Explicit reviewed replacement from a valid predecessor may instead persist fresh C/D births/IDs with no guessed retained lineage. |
| L22 | Genuine strict report has state.strict_status1; forged closed report sets status0/verifiedfalse and recomputes valid saved-envelope ID | Direct save and valid-digest load refuse2. Closed report status is at least max(strict,current,gates); there is no report audit-mode waiver. Genuine report1 saves with receipt0; baseline outer recording0 retains nested report1. Check --audit remains command0/unverified with nested migration report strict1. |
| L23 | Keep valid default baseline, configure missing `.pyalamode/reviews/team.json` with current source/required-export debt, then capture/duplicate/replace | First custom recording0 with strict1/current1/events/previousnull; default bytes unchanged. Repeated initial capture2/no overwrite; explicit replacement follows custom predecessor/history. Active writer destinations under `.pyalamode/history` or `.pyalamode/reports` refuse2 before publication. |

Migration TOML is exactly schema1 and relative baseline plus seven exact booleans: reject new findings, lost strict coverage, new trust, expanded effects, expired approvals, unsafe weakening and policy weakening. Unknown key, unsupported schema, duplicate/malformed selector/reference and wrong boolean/list types are2. Gate false keeps its report events visible. Root approves PAL360–PAL367 policy findings and current required-export events as distinct from underlying source debt; they do not recursively become new-debt groups. Existing source PAL350 remains its genuine source debt group as well as an independent current approval-failure observation.

## Exact helper-schema review supplements

The helper's additive state shape is fixed: `current_policy_status`, `current_policy_events={required_exports,expired_approvals,approval_failures}` and `required_operations`. Required-operation rows are exactly `{operation,required_by,contract_sha256,dependency_sha256,admission,engine_status,engine_rule,evidence}`; `required_by` rows are `{boundary,path,line,via}`, with `via=direct|invoked|retained`. `evidence` is exactly `{kind,value}`: kind `external-assumption` carries the closed inherited 12-key compact row; kind `integration-input` carries the closed 5-key `{contract_sha256,dependency_sha256,admission,approval,identity_error}` row. An untyped full catalog payload refuses2. Null digests require actual unresolved engine evidence. Familiar AST call spelling cannot create a requirement.

Root approves actual required-operation origin capture through a private `FunctionInfo.external_operation_sites` map, recorded by the existing actual `_integration_call` before approval refusal. The fresh strict-state walk follows real direct-call and retained-callable edges with finite `(target,via)` visitation. Own operations are direct; actual invocation paths are invoked; any retained path is retained. Reassignment, parameter shadows, unrelated same-spelling source/native functions and arbitrary denied catalog entries cannot create fake sites. Direct native primitive first-class callbacks remain deferred.

Boundary rows additionally publish selection reasons, actual public/required export flags and effect origins. Guard coverage is exactly `{mode,selected_export,debug,data_assertions}`; selection/debug/assertion rows retain their closed inherited schemas. Invocation/definition/initialization failures remain distinct. Finding groups carry `review_required`, and unavailable context is never accepted baseline debt. Public current-capture normalization forces `birth_identity` equal to the current identity. A historical differing birth/current identity is accepted only through validated envelope/predecessor lineage; baseline replacement derives inherited births internally from unique comparison matches. Arbitrary caller-provided historical birth IDs cannot promote a current capture.

`load_reference` returns exact `{record,state,receipt}` with reference receipt `{path,id,sha256}`. Finding comparison event before/after wrappers are exactly `{finding,count,path}`: complete finding group, independent occurrence delta and project-relative path. The baseline envelope adds explicit sorted lineage rows `{id,previous_identity_key,current_identity_key,previous_path,current_path,count}`. Saved reports use `{schema,kind,id,created_at,report}`. Write receipts explicitly separate `status=0,verified=false,state_strict_status,current_policy_status` from the stored source/current-policy result. Baseline and `report --save` CLI output is exactly `{report,written}`; unsaved report remains the plain closed report. CLI must show current events as well as recording receipt axes.

Finite supported record limits are independently testable refusal boundaries: 16MiB encoded record, JSON depth64/nodes500000, identity/location/review strings16384 code points, AST dump1MiB, sources16384, boundary/finding groups65536, locations262144, approval/unsafe rows4096 and predecessor depth128. Exact-at-limit supported input remains subject to all other rules; one-over-limit returns bounded tooling2, never a silently truncated report. Unexpected callback return, including `False`, is an error; success is exactly `None`.

Immutable history and active publication are two atomic operations, with live callback/receipt checks before each. Failure between them may leave a complete unreferenced new history record while preserving the prior active baseline and returning2. This is the only permitted newly created durable residue after that failure; no earlier record is overwritten. Record/directory symlinks and multi-link record ownership refuse before reads/writes. A failed active publication is not a successful replacement.

## Bounded post-freeze verification proposal

No candidate observations are authorized at this plan gate. After joint approval, implementation and a later root-declared source freeze, use these focused controllers under `/tmp/pyalamode-m10-review`:

Prepared `cli_controller.py` is UNEXECUTED. Its fixed sequence covers baseline-debt recording versus strict check/build, coordinate/cache stability, unique moved-debt lineage through replacement, lower-count independent new debt, failing `report --save` versus successful write receipt, corrupt explicit predecessor refusal, successful build beneath the root/reserved staging exclusion and source/policy byte preservation. It requires an explicit execution flag, fresh isolated work directory and root freeze identifier. Construction syntax checks use only stdlib AST parsing, never candidate import or calls.

Prepared `late_build_probe.py` is also UNEXECUTED. L17 uses each environment's actual SHA contract/dependency identity, a deterministic before/equal-expiry UTC snapshot and a guard-generation phase hook. It asserts a passing initial strict source status0, then the actual final integration-freshness PAL350 source/build status1 and no published artifact. The phase hook changes clock input only; it does not inject a diagnostic, result status or private freshness exception. It adds no measured elapsed interval.

`extra_literal_probes.json` pins D19/P29/P30 before correction observation: Unicode statement/range/AST (physical line4, UTF-8 columns5→21), unchanged unsafe scope/rationale with body-only change, and unchanged manifest path with widened unused contract. D19 coordinates/dump are checked with stdlib AST only. These fixed literals remain UNEXECUTED against the candidate.

Prepared `record_io_controller.py` exercises L20–L23 using real installed strict captures and main-owned live callbacks, bounded OS-failure hooks and genuine/forged content-addressed envelopes. `race_build_controller.py` changes actual source/reference/writer inputs at real guard generation for L19. The fresh-wheel wrapper checks frozen repository, all installed package/product bytes and controller maps before/cross/after; isolated provenance records actual sys.path and exactly one physical product. All remain UNEXECUTED until root authorizes the joint freeze.

`structural_controller.py` observes only the fixed four-module denominator, named SCC graph, seven contexts/D19 and existing P29/P30/A26 transitions. A26 pins source0→source0 actual approved SHA trust/gate1, source0→source0 declared+required Clock expansion/gate1, and unused current approval expiry with source0/current-policy1/gate1 but no consumer/PAL350/new trust. Identities are generated from each actual environment at execution; no elapsed workload interval is collected. The source/root freeze is `/tmp/pyalamode-m10-root-freeze.json`, SHA-256 `20d293ccb4781b64fc16ada3eff48f4b5951c135d8eb8e6930a23f6fda5f98a5`; peer controllers require their separate root-reviewed immutable intent before observation.

Before candidate observation, root source review corrected fixture metadata to the published M8 authority: native SHA/Base64 contracts declare empty effects, and `External` is not an exported effect family. A26 therefore uses `@fun` bytes identity→approved SHA wrapper with empty declared/required effects before and after; P30 pins empty→Clock effects in the unused manifest. The independent new-trust and policy-weakening gate1 outcomes are unchanged.

The first authorized native/Linux installed runs passed the CLI group and denominator fixture, then stopped at the readiness fixture's strict0 assertion. Actual PAL102/PAL221 diagnostics at ordinary `uses_checked(value) -> checked(value)` correctly refused to infer exact int input from its unchecked parameter annotation. Root approved changing only this call to `checked(1)`, preserving the authored edge, checked prerequisite and all strict0/graph expectations. Initial failed raw observations and post-failure source/product/controller maps are retained. Product freeze99 inputs and the source suites are unchanged; corrected candidate execution awaits a refreshed peer intent and root authorization.

1. Pure normalizer/multiset/unique-move controller over the seven fixed context literals and grouped state rows; exact counts, lineage, ambiguity, independent events and malformed closed schemas. The verifier fixes inputs/answers before importing the future helper.
2. Native installed-CLI isolated projects for D/P/R/L cases: actual command exit/report projection, exact denominator/SCC partial order, baseline/history hashes, read-only before/after source/policy/record maps, ordinary retained-data execution for only admitted artifacts and no-output failed builds. No cache-hit timing proves claims.
3. Fresh installed Linux wheel outside the checkout on exact CPython3.13.1 standard GIL UTF-8/surrogateescape, offline `python:3.13.1-slim`; compare all installed package bytes with the final checkout/freeze map and run only the bounded M10 controllers. Actual native operation approvals are generated per fixture from each environment's current identities. Platform-native paths/binaries remain separate provenance.
4. Nonexecution/pre-read controllers with authored default/decorator/annotation/import/setup/unsafe sentinels, excluded-source poison, sysconfig/startup poison and outside symlink audit hooks. Migration CLI commands use installed console scripts under explicitly disclosed ordinary Python startup assumptions; editor wire keeps the literal installed-environment executable and `-I -m pyalamode.editor`. No command claims console startup isolation it does not provide.
5. Current check/build/editor integration transitions: disk→warm→deleted/corrupt cache; partial display/full-project gate; required-export/current expiry; overlay marker removal or new writer; fresh policy/reference races. Editor receives the same policy diagnostic/status and unsaved provenance without applying edits or stale successful file claims.

Root owns one complete inherited/current suite on native macOS and actual Linux after freeze; this reviewer reuses its authoritative M1–M9 results and need not repeat full suites absent a new source change/failure. Final evidence maps cover all current product files, M10 tests/examples/controllers and exact root freeze packet before/after; no invented counters or partial hashes substitute for those inputs.

The proposed untimed cost inventory is one four-module denominator fixture and one named readiness graph: report actual source bytes/functions/modules, selected/checked/export/excluded denominator, resolved direct/retained edge count, SCC count, finding-group/occurrence count and enabled gates, with cold/current-warm cache-hit observations. It makes no universal latency claim. Any elapsed/memory workload intervals require a separate protocol and explicit root authorization after freeze; none is run here.

Main/helper schema/API/errors, audit/approval axes, origin metadata, final live callback, selectors and publication wrappers are jointly reconciled; root has released implementation. Remaining gates are the later joint freeze and bounded independent evidence. M9 prerequisite is satisfied at `dfe408f`. Fixed outcomes cannot be changed to fit a candidate. A concrete additional concern is documented before correction observation. Human usefulness remains UNMEASURED.

## Final independent engineering evidence

Root authorized both corrected runs against unchanged source freeze `/tmp/pyalamode-m10-root-freeze.json`, SHA-256 `20d293ccb4781b64fc16ada3eff48f4b5951c135d8eb8e6930a23f6fda5f98a5`, and peer intent-v2 SHA-256 `f76ca01ab24f0e5f0298efaab8171cf5d18c3e7045f44978c9276534eff9f17a` / prepared-v2 SHA-256 `0b458b28b47c3a7caed80cb8d3c1f535810ae2fbbf2df220b1f94c919973e5ce`. The original intent/prepared packets and failed native/Linux attempts remain unchanged. The only observed correction was ordinary caller `checked(value)`→`checked(1)`; it supplies established exact input without changing the authored edge, source0 requirement or checked prerequisite. There was no product correction or source freeze change.

Both final fresh installed environments passed all five bounded groups. Each built its own wheel offline from an outside-checkout copy of the frozen99 input files using build-only setuptools75.8.0, installed it with no index/dependencies in a clean consumer venv, and ran from outside the checkout. Linux used network-none `python:3.13.1-slim`, actual image ID `sha256:0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae`, read-only source/controllers and an explicit peer path map. All20 ZIP package members and all20 installed package bytes matched the freeze; the19 product-identity members matched separately. Wheel container hashes differ with platform/archive metadata; package bytes agree.

Actual isolated provenance at every checkpoint records CPython3.13.1, standard GIL, UTF-8/surrogateescape, the full sys.path and loaded product paths, and exactly one physical resolving product outside the checkout. macOS reports darwin/Clang16 and Linux linux/GCC12.2; both report `isolated=1`, `gil_disabled=0`, `utf8_mode=0`. Ordinary console startup assumptions are explicitly recorded. No fixture application module, annotation/default or decorator is evaluated by static capture.

Before, after each of the five groups, and after all groups, both drivers reconciled complete99-source,3-root-controller,10-peer-controller,20-installed-package and19-product SHA maps. The raw records retain each map and provenance independently. The reviewer reused root401-test source suites and62-check/23-command root walks on both platforms; no full inherited suite or performance workload was repeated. Raw engine JSON includes incidental engine elapsed fields, which are not workload measurements or performance acceptance. Human usefulness remains **UNMEASURED**, zero participants and attempts.

| Fixed group | Native macOS | Fresh installed Linux | Literal result |
| --- | --- | --- | --- |
| CLI | PASS,19 console commands | PASS,19 console commands | Baseline recording0/report1/unverified; strict/build1 with debt; audit0 until new-debt gate1; moved identity preserved; lower3→2 debt still new1; report-save exit1/receipt0; corrupt predecessor2; root build0 and staging display2. |
| Structural | PASS,15 named observations | PASS,15 named observations | Four-module/9-function/5-export denominator, actual SCC order/retained edges/checked disk prerequisite,7 literal AST contexts+D19, body-only unsafe gate1, same-path unused manifest gate1, actual approved SHA trust gate1, Clock expansion gate1, unused expiry source0/current-policy1/gate1. |
| Record IO | PASS,7 console commands and7 bounded helper refusals | PASS,7 console commands and7 bounded helper refusals | Genuine report1 writes0; valid-digest forged report and ambiguous retained lineage refuse; actual staged-fsync cleanup; post-active restoration and concurrent-writer preservation; configured custom baseline capture/replacement and reserved destinations. |
| Late used expiry | PASS | PASS | Actual guard generation changes only deterministic UTC input: initial source/check0, exact-expiry PAL350 source/build1, no tooling2, output or artifact, source/policy/product bytes preserved. |
| Publication races | PASS,3 actual transitions | PASS,3 actual transitions | Actual guard generation followed by source/reference/new-writer change gives tooling2/no new artifact; complete earlier successful artifact maps stay identical. |

The untimed denominator inventory is4 eligible modules/9 eligible functions,1 selected/checked module,4 selected/checked functions,5 checked exports,1 selected record,1 selected variant,9 excluded directories and794 authored Python bytes. Cold checks report4 cache misses; current warm checks report4 cache hits. The named readiness graph contains10 SCCs,7 direct and12 retained edges, with11 ordinary candidates exactly once. Unknown target remains an explicit hypothetical blocker (`candidate_status=1`); it does not become checked evidence. This finite inventory makes no universal cost or latency claim.

### Raw evidence index

Terminal index [`evidence-index.json`](/tmp/pyalamode-m10-review/evidence-index.json), 460134 bytes, SHA-256 `cf5e66ed4abe1baccc165f866ba297f5ff187321deeda252fdab589d6d92eec0`, retains51 expected/observed literal projections per platform, all26 actual console argv/exit pairs per platform, all raw stdout/stderr hashes, wheel members/byte lengths, every source/controller/product checkpoint, installed provenance, fixture JSON record hashes, initial failed-attempt hashes and the authoritative root summary. Each raw JSON includes unabridged producer output; these hashes cover its exact bytes.

| Raw record | Bytes | SHA-256 |
| --- | ---: | --- |
| [linux-installed-v2/wrapper](/private/tmp/pyalamode-m10-review/runs/linux-installed-v2/observations.json) | 200223 | `573548b76344566557d9ef2286e8a47bf03fab692a49967202d61da590fa01e3` |
| [linux-installed-v2/cli_controller](/private/tmp/pyalamode-m10-review/runs/linux-installed-v2/cli_controller/observations.json) | 1405144 | `9ca949ce825b2cf819d1cc2842c75a77d77b1c4938fe87951fc0e9d87332305f` |
| [linux-installed-v2/late_build_probe](/private/tmp/pyalamode-m10-review/runs/linux-installed-v2/late_build_probe/observations.json) | 212646 | `ae046b4268425eb82bb8d15f78fbb82d1694147f8ea61c2a28802338129c2a94` |
| [linux-installed-v2/race_build_controller](/private/tmp/pyalamode-m10-review/runs/linux-installed-v2/race_build_controller/observations.json) | 646992 | `680cdd4a521e68bbe9ceeb1ebd1e7a93f0983433b2dec18d18ef043bbdaba628` |
| [linux-installed-v2/record_io_controller](/private/tmp/pyalamode-m10-review/runs/linux-installed-v2/record_io_controller/observations.json) | 153198 | `9589e25dc78775217603c75d904d9331a15f05d0e8f47dc51c9d9a76aa6ccb47` |
| [linux-installed-v2/structural_controller](/private/tmp/pyalamode-m10-review/runs/linux-installed-v2/structural_controller/observations.json) | 487449 | `e404923c187f761ffded368fb44132b81fa7018c25bb3653a55a5c301d0c0029` |
| [native-installed-v2/wrapper](/private/tmp/pyalamode-m10-review/runs/native-installed-v2/observations.json) | 216911 | `e453b23056c30383854e4bd755a63933f8e8852051c2963c37dc1c371823092c` |
| [native-installed-v2/cli_controller](/private/tmp/pyalamode-m10-review/runs/native-installed-v2/cli_controller/observations.json) | 1418017 | `8c27cc8aee25467f7a1d6b04c39a6c0f842fbc49afb45e458137c3e573d6d7d8` |
| [native-installed-v2/late_build_probe](/private/tmp/pyalamode-m10-review/runs/native-installed-v2/late_build_probe/observations.json) | 216414 | `a902e9c23b86c2b955fc6c3aad5bdd09dc24287bddac85bcf631e54c9c7487b1` |
| [native-installed-v2/race_build_controller](/private/tmp/pyalamode-m10-review/runs/native-installed-v2/race_build_controller/observations.json) | 654213 | `50dc71e513cb913240bdb142b4921e5bd3de61a7e048aa1dfa14368ec68792ba` |
| [native-installed-v2/record_io_controller](/private/tmp/pyalamode-m10-review/runs/native-installed-v2/record_io_controller/observations.json) | 154923 | `e390cab7b50f3c39ac0d423c3642252a9b42720164e085271573e3dbc096acd8` |
| [native-installed-v2/structural_controller](/private/tmp/pyalamode-m10-review/runs/native-installed-v2/structural_controller/observations.json) | 496722 | `fef94b937dc3674c9bffb05d8a0d376149980749ba2c34175eae2a6f8d7ef747` |

Native own-wheel SHA-256 `635155a39641e561ad3eecaaba14b83279d4ffa7bc9d566e20ff9c9ccfad2c9a`; Linux own-wheel SHA-256 `b43e7ba9bfe321a09d789615c0a81b2ad2643109af38815eb80da71b0404ad7c`. Complete ZIP member and installed-byte maps are in each wrapper and the terminal index.

Publication authority documents may append final evidence as approved by root; frozen source and protocol maps remain unchanged. The final engineering result is bounded to these named cases and actual target environments. Root owns final acceptance/commit; no human adoption or universal arbitrary-Python correctness claim is inferred.

### Complete final frozen controller and literal texts

These are the complete exact ten protocol inputs pinned by peer intent-v2. Hashes cover the bytes on disk, including final newline. Text publication below does not execute a controller. The initial structural controller SHA was `d6c5a56d94180901607a71351c219f875abe8d8296bd2fb80c39a14c7d010950`; reversing only the approved `checked(1)`→`checked(value)` delta reproduces that initial SHA. All other protocol inputs retain their original SHA.

#### cli_controller.py

Path: `/private/tmp/pyalamode-m10-review/cli_controller.py`
Bytes: 13539; SHA-256: `bbf2fd1d4256da2b894c5ffa372b30bf716599b724c8e974b2a5d2f45ed3b0ad`.

````python
"""Fixed M10 native/installed-CLI controls; construction is not candidate evidence.

Execute only after root's joint source freeze, using the literal installed console
script. Console startup has ordinary Python assumptions. This controller never
imports pyalamode, uses no timings, and writes only beneath its fresh work root.
Root separately verifies the complete installed product/freeze byte inventory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def envelope(record: dict) -> None:
    expected = digest(canonical({key: value for key, value in record.items()
                                 if key != "id"}))
    assert record["id"] == expected, "record ID must cover all non-ID fields"


def debt(name: str, *, passing: bool = False) -> str:
    body = "    return value + 1\n" if passing else (
        "    result = value\n    result = result + 1\n    return result\n")
    return f"@fun\ndef {name}(value: int) -> int:\n" + body + "\n"


def unit(*definitions: str, prefix: str = "") -> str:
    return prefix + "from pyalamode import fun\n\n" + "".join(definitions)


def pal_counts(report: dict) -> dict[str, int]:
    counts = {}
    for category, side in (("retained_findings", "after"),
                           ("resolved_findings", "before"),
                           ("new_findings", "after")):
        counts[category] = sum(
            row[side]["count"] for row in report["comparison"][category]
            if row[side] is not None and row[side]["finding"]["rule"] == "PAL101")
    return counts


def record_map(root: Path) -> dict[str, str]:
    directory = root / ".pyalamode"
    return ({str(path.relative_to(root)): digest(path.read_bytes())
             for path in sorted(directory.rglob("*")) if path.is_file()}
            if directory.exists() else {})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--freeze-sha256")
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED: explicit root freeze authorization required")
        return 0
    assert args.candidate and args.work_root and args.freeze_sha256
    assert sys.version_info[:3] == (3, 13, 1), "controller target must be exact"
    assert not sysconfig.get_config_var("Py_GIL_DISABLED"), "standard-GIL target required"
    assert sys.getfilesystemencoding() == "utf-8"
    assert sys.getfilesystemencodeerrors() == "surrogateescape"
    assert len(args.freeze_sha256) == 64
    assert all(c in "0123456789abcdef" for c in args.freeze_sha256)
    assert args.candidate.is_absolute(), "literal installed console path required"
    candidate = args.candidate.resolve(strict=True)
    work = args.work_root.resolve()
    assert not work.exists(), "controller requires a fresh isolated directory"
    work.mkdir(parents=True)
    project = work / "project"
    project.mkdir()
    observations = []
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)

    def cli(command: str, *arguments: str, expected: int) -> dict:
        source_before = {str(path.relative_to(project)): digest(path.read_bytes())
                         for path in sorted(project.rglob("*.py"))}
        source_before["pyproject.toml"] = digest((project / "pyproject.toml").read_bytes())
        argv = [str(candidate), command, *arguments, "--root", str(project), "--json"]
        result = subprocess.run(argv, cwd=project, env=environment,
                                capture_output=True, text=True, timeout=45)
        observation = {"argv": argv, "expected_status": expected,
                       "status": result.returncode, "stdout": result.stdout,
                       "stderr": result.stderr}
        observations.append(observation)
        assert result.returncode == expected, observation
        source_after = {str(path.relative_to(project)): digest(path.read_bytes())
                        for path in sorted(project.rglob("*.py"))}
        source_after["pyproject.toml"] = digest((project / "pyproject.toml").read_bytes())
        assert all(source_after.get(path) == value for path, value in source_before.items()), (
            "CLI observation must preserve authored source/policy bytes")
        new_sources = set(source_after) - set(source_before)
        if new_sources:
            assert command == "build" and expected == 0 and "--output" in arguments
            output = Path(arguments[arguments.index("--output") + 1]).resolve()
            assert all((project / path).resolve().is_relative_to(output) for path in new_sources), (
                "only successful build may publish source copies beneath requested output")
        value = json.loads(result.stdout)
        assert isinstance(value, dict)
        return value

    def baseline(*extra: str) -> dict:
        result = cli("baseline", "--owner", "independent fixed review",
                     "--rationale", "record debt without strict waiver", *extra,
                     expected=0)
        assert set(result) == {"report", "written"}
        assert result["written"]["status"] == 0
        assert result["written"]["verified"] is False
        assert result["written"]["state_strict_status"] == 1
        assert result["report"]["status"] == 1
        assert result["report"]["verified"] is False
        assert result["report"]["state"]["strict_status"] == 1
        active = json.loads((project / ".pyalamode/baseline.json").read_text())
        envelope(active)
        history = project / ".pyalamode/history" / (active["id"] + ".json")
        assert history.read_bytes() == (project / ".pyalamode/baseline.json").read_bytes()
        return active

    try:
        (project / "pyproject.toml").write_text(
            '[tool.pyalamode.migration]\nschema = 1\n'
            'baseline = ".pyalamode/baseline.json"\nreject_new_findings = true\n')
        (project / "core.py").write_text(unit(debt("a"), debt("b"), debt("c")))
        original = baseline()
        assert original["previous_id"] is None
        originals = [row for row in original["state"]["findings"]
                     if row["rule"] == "PAL101"]
        assert len(originals) == 3 and sum(row["count"] for row in originals) == 3
        old_ids = {row["logical_boundary"]["selector"]: row["id"] for row in originals}
        records = record_map(project)
        initial = cli("report", expected=1)
        assert pal_counts(initial) == {"retained_findings": 3,
                                       "resolved_findings": 0, "new_findings": 0}
        cli("check", "--audit", expected=0)
        cli("check", expected=1)
        cli("build", "--output", str(project / "artifact"), expected=1)
        assert not (project / "artifact").exists()
        assert record_map(project) == records, "observation must not publish state"

        # D02/L13: coordinate changes and lost cache cannot create or erase debt.
        (project / "core.py").write_text(unit(debt("a"), debt("b"), debt("c"),
                                             prefix="# coordinate-only change\n\n"))
        shifted = cli("report", expected=1)
        assert pal_counts(shifted) == pal_counts(initial)
        assert {row["after"]["finding"]["id"]
                for row in shifted["comparison"]["retained_findings"]
                if row["after"]["finding"]["rule"] == "PAL101"} == set(old_ids.values())
        cli("check", "--audit", expected=0)
        shutil.rmtree(project / ".pyalamode-cache", ignore_errors=True)
        without_cache = cli("report", expected=1)
        assert pal_counts(without_cache) == pal_counts(initial)

        # D03/L02: unique relocation retains original ID through reviewed replacement.
        (project / "core.py").write_text(unit(debt("b"), debt("c")))
        (project / "moved.py").write_text(unit(debt("a")))
        moved = cli("report", expected=1)
        assert pal_counts(moved) == pal_counts(initial)
        moved_a = [row for row in moved["comparison"]["retained_findings"]
                   if row["after"]["finding"]["logical_boundary"]["selector"] == "moved:a"
                   and row["after"]["finding"]["rule"] == "PAL101"]
        assert len(moved_a) == 1
        assert moved_a[0]["after"]["finding"]["id"] == old_ids["core:a"]
        assert moved_a[0]["before"]["path"] == "core.py"
        assert moved_a[0]["after"]["path"] == "moved.py"
        replacement = baseline("--replace")
        assert replacement["previous_id"] == original["id"]
        assert any(row["id"] == old_ids["core:a"] and row["previous_path"] == "core.py"
                   and row["current_path"] == "moved.py" for row in replacement["lineage"])
        historical = project / ".pyalamode/history" / (original["id"] + ".json")
        assert json.loads(historical.read_text()) == original

        # D01: lower debt total independently contains new debt and rejects audit.
        (project / "moved.py").write_text(unit(debt("a", passing=True)))
        (project / "core.py").write_text(unit(debt("b", passing=True), debt("c"), debt("d")))
        lower = cli("report", expected=1)
        assert pal_counts(lower) == {"retained_findings": 1,
                                     "resolved_findings": 2, "new_findings": 1}
        cli("check", "--audit", expected=1)
        cli("check", expected=1)
        cli("build", "--output", str(project / "artifact"), expected=1)
        assert not (project / "artifact").exists()
        before_save = record_map(project)
        saved = cli("report", "--save", expected=1)
        assert set(saved) == {"report", "written"}
        assert saved["report"]["status"] == 1 and saved["report"]["verified"] is False
        assert saved["written"]["status"] == 0 and saved["written"]["verified"] is False
        after_save = record_map(project)
        assert all(after_save[path] == value for path, value in before_save.items())
        assert len(set(after_save) - set(before_save)) == 1
        report_path = project / saved["written"]["path"]
        report_record = json.loads(report_path.read_text())
        envelope(report_record)
        assert report_record["report"] == saved["report"]

        # L04: explicit corrupt predecessor refuses instead of first-capture fallback.
        active_path = project / ".pyalamode/baseline.json"
        active_path.write_bytes(b'{"schema":1,"kind":"corrupt"}\n')
        corrupt = record_map(project)
        cli("baseline", "--owner", "independent fixed review", "--rationale", "refuse",
            "--replace", expected=2)
        assert record_map(project) == corrupt

        # L18: successful output beneath root must not turn private staging into source.
        project = work / "build-success"
        project.mkdir()
        (project / "pyproject.toml").write_text("[tool.pyalamode]\n")
        (project / "core.py").write_text(unit(debt("total", passing=True)))
        accepted = project / "accepted"
        built = cli("build", "--output", str(accepted), expected=0)
        assert built["status"] == 0 and built["verified"] is True
        assert (accepted / "core.py").read_bytes() == (project / "core.py").read_bytes()
        assert (accepted / "pyalamode-evidence.json").is_file()
        assert not list(project.glob(".pyalamode-build-*")), "successful staging must be cleaned"
        # Published output is ordinary eligible source; a reserved stage is explicit exclusion.
        staging = project / ".pyalamode-build-fixed"
        staging.mkdir()
        (staging / "poison.py").write_text('raise RuntimeError("reserved staging poison")\n')
        inventory = cli("regions", expected=0)
        assert inventory["state"]["coverage"]["eligible_modules"] == 2
        assert any(row["path"].startswith(".pyalamode-build-fixed")
                   and row["reason"] == "reserved product build staging"
                   for row in inventory["state"]["scope"]["exclusions"])
        cli("regions", str(staging / "poison.py"), expected=2)
        outcome = "PASS"
    except Exception as error:
        outcome = "FAIL"
        observations.append({"controller_error": repr(error)})
        raise
    finally:
        evidence = {"schema": 1, "kind": "m10-fixed-cli-observations",
                    "outcome": outcome, "root_freeze_sha256": args.freeze_sha256,
                    "candidate_entrypoint_sha256": digest(candidate.read_bytes()),
                    "controller_sha256": digest(Path(__file__).read_bytes()),
                    "ordinary_console_startup_assumptions": True,
                    "human_measurement": {"status": "UNMEASURED", "participants": 0,
                                          "attempts": 0}, "observations": observations}
        (work / "observations.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": outcome, "evidence": str(work / "observations.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

#### context-literals.json

Path: `/private/tmp/pyalamode-m10-review/context-literals.json`
Bytes: 1540; SHA-256: `4ffff5e5da67e7eff5439e40348f7b69d5bc3b2e7873b945164f52ddcca49f26`.

````json
{
  "C101": {
    "ast": "Assign(targets=[Name(id='value', ctx=Store())], value=BinOp(left=Name(id='value', ctx=Load()), op=Add(), right=Constant(value=1)))",
    "origin": "static source",
    "rule": "PAL101"
  },
  "C221": {
    "ast": "Return(value=Call(func=Name(id='leaf', ctx=Load()), args=[Constant(value=True)]))",
    "origin": "static source",
    "rule": "PAL221"
  },
  "C230": {
    "ast": "Return(value=Call(func=Name(id='unknown', ctx=Load()), args=[Name(id='value', ctx=Load())]))",
    "origin": "static source",
    "rule": "PAL230"
  },
  "C241": {
    "ast": "Import(names=[alias(name='os')])",
    "origin": "static source",
    "rule": "PAL241"
  },
  "C250": {
    "ast": "Expr(value=Call(func=Attribute(value=Name(id='values', ctx=Load()), attr='appended', ctx=Load()), args=[Constant(value=1)]))",
    "origin": "persistent return-only operation",
    "rule": "PAL250"
  },
  "C310": {
    "ast": "FunctionDef(name='now', args=arguments(args=[arg(arg='clock', annotation=Name(id='ClockCapability', ctx=Load()))]), body=[Return(value=Call(func=Attribute(value=Name(id='clock', ctx=Load()), attr='now_ns', ctx=Load())))], decorator_list=[Call(func=Name(id='effects', ctx=Load()), args=[Name(id='Clock', ctx=Load())])], returns=Name(id='int', ctx=Load()))",
    "origin": "project effect policy",
    "rule": "PAL310"
  },
  "C350": {
    "ast": "Return(value=Call(func=Name(id='sha256_digest', ctx=Load()), args=[Name(id='data', ctx=Load())]))",
    "origin": "external operation policy",
    "rule": "PAL350"
  }
}
````

#### context_literals.py

Path: `/private/tmp/pyalamode-m10-review/context_literals.py`
Bytes: 1000; SHA-256: `ed7c40a6be69ff914455b64f8a056ba5e65613ad1ccd8ac28153b283c22a0efd`.

````python
"""Plan-only CPython AST literals; never imports or invokes the candidate."""
import ast
import json

CASES = {
    "C101": ("PAL101", "static source", "value = value + 1\n"),
    "C221": ("PAL221", "static source", "return leaf(True)\n"),
    "C230": ("PAL230", "static source", "return unknown(value)\n"),
    "C241": ("PAL241", "static source", "import os\n"),
    "C250": ("PAL250", "persistent return-only operation", "values.appended(1)\n"),
    "C310": ("PAL310", "project effect policy", "@effects(Clock)\ndef now(clock: ClockCapability) -> int:\n    return clock.now_ns()\n"),
    "C350": ("PAL350", "external operation policy", "return sha256_digest(data)\n"),
}

print(json.dumps({name: {"rule": rule, "origin": origin,
                         "ast": ast.dump(ast.parse(text).body[0], annotate_fields=True,
                                         include_attributes=False, show_empty=False)}
                  for name, (rule, origin, text) in CASES.items()}, indent=2, sort_keys=True))
````

#### extra_literal_probes.json

Path: `/private/tmp/pyalamode-m10-review/extra_literal_probes.json`
Bytes: 6839; SHA-256: `ebc0d6348455a98cd97faec683448bf33129b189362f73e1ce26722e03a0dcc8`.

````json
{
  "schema": 1,
  "kind": "m10-independent-extra-literals",
  "status": "UNEXECUTED",
  "cases": {
    "D19": {
      "source": "@fun\ndef f(value: str) -> str:\n    result = value\n    result = \"a\u2028b\"\n    return result\n",
      "logical_boundary": {"kind": "function", "selector": "core:f", "qualified_name": "f"},
      "rule": "PAL101",
      "origin": "static source",
      "diagnostic_range": {"line": 4, "column": 5, "end_line": 4, "end_column": 21, "column_encoding": "utf-8-bytes"},
      "expected_context": {"kind": "ast-statement", "ast": "Assign(targets=[Name(id='result', ctx=Store())], value=Constant(value='a\\u2028b'))"},
      "expected_physical_lines": 5,
      "note": "Pure context fixture; decorator spelling is parsed and never evaluated. End byte offset includes all three UTF-8 bytes of U+2028 and is end-exclusive."
    },
    "P29": {
      "before_source": "from pyalamode import unsafe\n@unsafe(scope=\"legacy\", rationale=\"reviewed shell\")\ndef raw() -> int:\n    return 1\n",
      "current_source": "from pyalamode import unsafe\n@unsafe(scope=\"legacy\", rationale=\"reviewed shell\")\ndef raw() -> int:\n    return 2\n",
      "selector": "core:raw",
      "unchanged": ["selector", "scope", "rationale", "signature"],
      "changed": ["definition_sha256"],
      "expected": {"unsafe_weakening_nonempty": true, "reject_unsafe_weakening_status": 1, "source_strict_status": 0, "checked_adapter": false}
    },
    "P30": {
      "configured_manifest_paths_before": ["contracts.json"],
      "configured_manifest_paths_current": ["contracts.json"],
      "source": "from pyalamode import fun\n@fun\ndef identity(value: int) -> int:\n    return value\n",
      "unused_operation": "pyalamode.integrations.base64_encode",
      "before_effects": [],
      "current_effects": ["Clock"],
      "contract_sha256_changes": true,
      "expected": {"policy_weakening_nonempty": true, "inputs_changed_nonempty": true, "reject_policy_weakening_status": 1, "source_strict_status": 0, "new_trust_count": 0, "approval_failures_count": 0},
      "identity_rule": "Build each temporary reviewed manifest from that frozen environment's actual product candidate contract identity; no reused or invented native digest."
    },
    "A26": {
      "trust": {"selector": "core:digest", "before": "@fun exact bytes identity", "current": "same empty effect bound; approved actual sha256_digest invocation", "declared_effects_before": [], "declared_effects_current": [], "required_effects_before": [], "required_effects_current": [], "source_status_before": 0, "source_status_current": 0, "new_trust_nonempty": true, "reject_new_trust_status": 1},
      "effects": {"selector": "core:f", "before": "pure exact int identity", "current": "@effects(Clock) exact ClockCapability.now_ns", "source_status_before": 0, "source_status_current": 0, "declared_expansion": ["Clock"], "required_expansion": ["Clock"], "reject_expanded_effects_status": 1},
      "unused_expiry": {"before_expiry": "2099-01-01T00:00:00Z", "current_expiry": "2000-01-01T00:00:00Z", "source_status_before": 0, "source_status_current": 0, "current_policy_status": 1, "reject_expired_approvals_status": 1, "new_trust_count": 0, "approval_failures_count": 0, "source_PAL350_count": 0},
      "identity_rule": "Use actual per-environment SHA contract/dependency identities in each temporary project; no invented approval or source consumer."
    },
    "L22": {
      "strict_status": 1,
      "forged_report_status": 0,
      "forged_verified": false,
      "all_envelope_content_ids_recomputed_correctly": true,
      "expected_direct_save_status": 2,
      "expected_reference_load_status": 2,
      "genuine": {"report_status": 1, "write_receipt_status": 0},
      "audit": {"command_status": 0, "verified": false, "nested_report_strict_status": 1},
      "required_rule": "Closed report status >= max(state.strict_status,state.current_policy_status,gates.status); no report audit mode exists."
    },
    "L23": {
      "active": ".pyalamode/reviews/team.json",
      "default": ".pyalamode/baseline.json",
      "first": {"recording_status": 0, "strict_status": 1, "current_policy_status": 1, "previous_id": null, "default_bytes_unchanged": true},
      "duplicate_initial_status": 2,
      "replacement_follows_custom_predecessor": true,
      "reserved_writer_destinations": [".pyalamode/history/active.json", ".pyalamode/reports/active.json"],
      "reserved_writer_status": 2
    },
    "L21": {
      "old_boundaries": ["A:f", "B:f"],
      "current_boundaries": ["C:f", "D:f"],
      "shared_evidence": {"kind": "function", "qualified_name": "f", "same_signature": true, "rule": "PAL101", "context": "C101", "origin": "static source", "count_per_group": 1},
      "forged_lineage": [
        {"old": "A:f", "current": "C:f", "inherits_old_birth_id": true},
        {"old": "B:f", "current": "D:f", "inherits_old_birth_id": true}
      ],
      "all_envelope_content_ids_recomputed_correctly": true,
      "expected_forged_reference_load_status": 2,
      "required_validation": "Reset child groups to fresh current birth identities; actual compare against verified predecessor must prove each retained pairing unique.",
      "reviewed_replacement_from_valid_predecessor": {"recording_status": 0, "verified": false, "fresh_current_births": true, "guessed_retained_lineage": false}
    },
    "L20": {
      "cases": [
        {"controlled_failure": "temporary write or fsync before stage context yield", "expected_status": 2, "temporary_files_cleaned": true},
        {"controlled_failure": "active directory fsync or readback after this writer replaces active", "expected_status": 2, "previous_active_or_absence_restored": true},
        {"controlled_failure": "postreplace error plus noncooperative new active writer", "expected_status": 2, "concurrent_writer_bytes_preserved": true, "blind_rollback": false}
      ],
      "allowed_residue": "one complete unreferenced history envelope; no earlier record overwritten",
      "ownership_rule": "Before rollback, verify active inode/content belongs to this publication, with descriptor-local cooperative lock still held."
    },
    "L19": {
      "hook": "after actual guard generation, before final artifact publication",
      "cases": [
        {"change": "selected source bytes", "expected_build_status": 2},
        {"change": "valid required baseline/reference receipt bytes", "expected_build_status": 2},
        {"change": "new ordinary writer file assigning core.total.__code__", "expected_build_status": 2}
      ],
      "expected": {"new_artifact": false, "prior_artifact_bytes_unchanged": true, "stage_cleaned": true},
      "exception": "Actual used approval crossing UTC expiry is L17/source strict1, not tooling2. No diagnostics/status/exceptions are injected."
    }
  }
}
````

#### installed_provenance.py

Path: `/private/tmp/pyalamode-m10-review/installed_provenance.py`
Bytes: 2686; SHA-256: `0cb9999bb4e6bf18ae33c5cf0e153678fcda9429fa740613281f524cc5150d68`.

````python
"""UNEXECUTED isolated installed-product provenance; no application module import."""
import argparse
import importlib
from importlib.machinery import PathFinder
import json
from pathlib import Path
import sys
import sysconfig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout-root", type=Path, required=True)
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED")
        return 0
    assert sys.flags.isolated and sys.version_info[:3] == (3, 13, 1)
    assert not sysconfig.get_config_var("Py_GIL_DISABLED")
    assert sys.getfilesystemencoding() == "utf-8" and sys.getfilesystemencodeerrors() == "surrogateescape"
    checkout = args.checkout_root.resolve()
    package = importlib.import_module("pyalamode")
    model = importlib.import_module("pyalamode.model")
    product = Path(package.__file__).resolve().parent
    assert not product.is_relative_to(checkout)
    for filename in model.foundation_identities():
        if filename != "__init__.py":
            importlib.import_module("pyalamode." + filename.removesuffix(".py"))
    loaded = {name: str(Path(module.__file__).resolve()) for name, module in sys.modules.items()
              if (name == "pyalamode" or name.startswith("pyalamode.")) and getattr(module, "__file__", None)}
    assert all(Path(path).is_relative_to(product) for path in loaded.values())
    roots = set()
    for entry in sys.path:
        if entry:
            assert not Path(entry).resolve().is_relative_to(checkout)
            spec = PathFinder.find_spec("pyalamode", [entry])
            if spec and spec.origin:
                roots.add(str(Path(spec.origin).resolve().parent))
    assert roots == {str(product)}, "exactly one physical product must resolve"
    print(json.dumps({"product_root": str(product), "loaded_files": loaded,
        "resolved_product_roots": sorted(roots), "sys_path": sys.path,
        "product_artifacts": model.foundation_identities(),
        "runtime": {"version": sys.version, "executable": sys.executable,
                    "base_prefix": sys.base_prefix, "prefix": sys.prefix,
                    "platform": sys.platform, "isolated": sys.flags.isolated,
                    "filesystem_encoding": sys.getfilesystemencoding(),
                    "filesystem_errors": sys.getfilesystemencodeerrors(),
                    "utf8_mode": sys.flags.utf8_mode, "gil_disabled": sysconfig.get_config_var("Py_GIL_DISABLED")}},
        indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

#### late_build_probe.py

Path: `/private/tmp/pyalamode-m10-review/late_build_probe.py`
Bytes: 8098; SHA-256: `6fc6a3e7b7f4d3f61dbca436232d5ab91bdabcdff0150c086acf1b23f693f2ea`.

````python
"""UNEXECUTED L17 fixed post-guard UTC-expiry probe; root freeze required.

The isolated installed-environment Python runs this file with -I after root has
verified installed bytes. This imports the candidate only behind an explicit
execution flag. It obtains actual native identities and changes observation UTC
after actual guard generation. It never injects a diagnostic/status/exception.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import importlib
import json
from pathlib import Path
import sys
import sysconfig


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--installed-product-root", type=Path)
    parser.add_argument("--freeze-sha256")
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED: explicit root freeze authorization required")
        return 0
    assert args.work_root and args.installed_product_root and args.freeze_sha256
    assert sys.version_info[:3] == (3, 13, 1)
    assert not sysconfig.get_config_var("Py_GIL_DISABLED")
    assert sys.getfilesystemencoding() == "utf-8"
    assert sys.getfilesystemencodeerrors() == "surrogateescape"
    assert len(args.freeze_sha256) == 64
    assert all(c in "0123456789abcdef" for c in args.freeze_sha256)
    work = args.work_root.resolve()
    assert not work.exists(), "fresh isolated work directory required"
    work.mkdir(parents=True)
    root = work / "project"
    root.mkdir()
    project = importlib.import_module("pyalamode.project")
    contracts = importlib.import_module("pyalamode.integration_contracts")
    guards = importlib.import_module("pyalamode.guardgen")
    model = importlib.import_module("pyalamode.model")
    assert Path(project.__file__).resolve().parent == args.installed_product_root.resolve()
    before = datetime(2035, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    expiry = datetime(2035, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
    identity = contracts.integration_snapshot({}, root, now=before)
    operation = "pyalamode.integrations.sha256_digest"
    actual = identity["inputs"][operation]
    assert not identity["errors"] and actual["dependency_sha256"] is not None
    policy = (
        '[tool.pyalamode]\nexternal_trust = "approved"\n'
        'boundary_guards = "exports"\nguarded_exports = ["core:digest"]\n\n'
        '[[tool.pyalamode.integration_approvals]]\n'
        f'operation = "{operation}"\n'
        f'contract_sha256 = "{actual["contract_sha256"]}"\n'
        f'dependency_sha256 = "{actual["dependency_sha256"]}"\n'
        'owner = "independent bounded review"\n'
        'rationale = "current only until exact post-guard UTC expiry"\n'
        'provenance = "actual environment identity; temporary fixture"\n'
        'expires_at = "2035-01-01T00:00:01Z"\n')
    (root / "pyproject.toml").write_text(policy)
    source = root / "core.py"
    source.write_text('from pyalamode import fun\n'
                      'from pyalamode.integrations import sha256_digest\n'
                      '@fun\ndef digest(data: bytes) -> bytes:\n'
                      '    return sha256_digest(data)\n')
    original_source = source.read_bytes()
    product_before = model.foundation_identities()
    source_before = {"core.py": hashlib.sha256(original_source).hexdigest(),
                     "pyproject.toml": hashlib.sha256(policy.encode()).hexdigest()}
    real_snapshot = project.integration_snapshot
    real_facades = guards.generate_facades
    phase = {"expired": False, "facade_calls": 0}
    snapshots = []

    def phase_snapshot(policy, root):
        value = real_snapshot(policy, root, now=expiry if phase["expired"] else before)
        snapshots.append({"phase": "equal-expiry" if phase["expired"] else "before-expiry",
                          "admission": value["inputs"][operation]["admission"],
                          "actual_input": value["inputs"][operation]})
        return value

    def post_guard(*args, **kwargs):
        value = real_facades(*args, **kwargs)
        phase["facade_calls"] += 1
        phase["expired"] = True
        return value

    observations = {"schema": 1, "kind": "m10-fixed-late-build-observation",
                    "root_freeze_sha256": args.freeze_sha256,
                    "controller_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "actual_contract_sha256": actual["contract_sha256"],
                    "actual_dependency_sha256": actual["dependency_sha256"],
                    "before_utc": before.isoformat(), "expiry_utc": expiry.isoformat(),
                    "clock_change_only": True, "snapshots": snapshots,
                    "product_before": product_before, "source_before": source_before,
                    "human_measurement": {"status": "UNMEASURED", "participants": 0,
                                          "attempts": 0}}
    destination = root / "artifact"
    project.integration_snapshot = phase_snapshot
    guards.generate_facades = post_guard
    try:
        initial = project.check_paths([str(source)], root=str(root), cache=False)
        observations["initial_source_status"] = initial.source_status
        observations["initial_status"] = initial.status
        observations["initial_raw"] = initial.to_dict()
        assert initial.status == 0 and initial.source_status == 0
        directories_before = {path.name for path in root.iterdir()
                              if path.is_dir() and path.name != ".pyalamode-cache"}
        result = project.build_paths([str(source)], root=str(root), output=str(destination))
        observations["late_status"] = result.status
        observations["late_source_status"] = result.source_status
        observations["diagnostics"] = [asdict(row) for file in result.results
                                        for row in file.diagnostics]
        observations["tooling"] = [asdict(row) for row in result.tooling]
        observations["artifact_exists"] = destination.exists()
        observations["output"] = result.output
        observations["facade_calls"] = phase["facade_calls"]
        observations["late_raw"] = result.to_dict()
        observations["product_after"] = model.foundation_identities()
        observations["source_after"] = {
            "core.py": hashlib.sha256(source.read_bytes()).hexdigest(),
            "pyproject.toml": hashlib.sha256((root / "pyproject.toml").read_bytes()).hexdigest()}
        directories_after = {path.name for path in root.iterdir()
                             if path.is_dir() and path.name != ".pyalamode-cache"}
        assert phase["facade_calls"] == 1
        assert result.status == 1 and result.source_status == 1
        assert any(row["rule"] == "PAL350" and row["origin"] == "integration freshness"
                   for row in observations["diagnostics"])
        assert not observations["tooling"]
        assert not destination.exists() and result.output is None
        assert directories_after == directories_before, "failed staging must be cleaned"
        assert observations["product_after"] == product_before
        assert observations["source_after"] == source_before
        assert source.read_bytes() == original_source
        assert (root / "pyproject.toml").read_text() == policy
        assert snapshots[-1]["admission"] == "expired"
        observations["outcome"] = "PASS"
    except Exception as error:
        observations["outcome"] = "FAIL"
        observations["controller_error"] = repr(error)
        raise
    finally:
        project.integration_snapshot = real_snapshot
        guards.generate_facades = real_facades
        (work / "observations.json").write_text(json.dumps(observations, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": "PASS", "evidence": str(work / "observations.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

#### race_build_controller.py

Path: `/private/tmp/pyalamode-m10-review/race_build_controller.py`
Bytes: 5803; SHA-256: `5a3d92474a67d8361d4bb37229745bc3862e7ba3f67b04719e439624763c2189`.

````python
"""UNEXECUTED L19 actual post-guard source/reference/writer changes; no injected status."""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--installed-product-root", type=Path)
    parser.add_argument("--freeze-sha256")
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED: root freeze authorization required")
        return 0
    assert args.work_root and args.installed_product_root and args.freeze_sha256
    work = args.work_root.resolve()
    assert not work.exists()
    work.mkdir(parents=True)
    project = importlib.import_module("pyalamode.project")
    views = importlib.import_module("pyalamode.migration_views")
    helper = importlib.import_module("pyalamode.migration")
    guards = importlib.import_module("pyalamode.guardgen")
    model = importlib.import_module("pyalamode.model")
    assert Path(project.__file__).resolve().parent == args.installed_product_root.resolve()
    product_before = model.foundation_identities()
    log = []
    real_facades = guards.generate_facades
    try:
        for mode in ("source", "reference", "writer"):
            base = work / mode
            base.mkdir()
            root = base / "project"
            root.mkdir()
            source = root / "core.py"
            source.write_text('from pyalamode import fun\n@fun\ndef total(value: int) -> int:\n    return value + 1\n')
            (root / "pyproject.toml").write_text('[tool.pyalamode]\nboundary_guards = "exports"\n'
                'guarded_exports = ["core:total"]\n[tool.pyalamode.migration]\nschema = 1\n'
                'baseline = ".pyalamode/baseline.json"\nreject_new_findings = true\n')
            snapshot, state, report, _ = views.observe(root, bootstrap=True)
            assert state["strict_status"] == 0 and report["status"] == 0
            receipt = helper.write_baseline(root, state, owner="fixed race review", rationale="initial passing capture",
                        prepublish=views.make_prepublish(snapshot, state, []))
            active = root / receipt["path"]
            source_before = hashlib.sha256(source.read_bytes()).hexdigest()
            reference_before = hashlib.sha256(active.read_bytes()).hexdigest()
            prior = base / "prior-artifact"
            earlier = project.build_paths([str(source)], root=str(root), output=str(prior))
            assert earlier.status == 0 and earlier.verified and prior.exists()
            prior_map = {p.relative_to(prior).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in prior.rglob("*") if p.is_file()}
            assert "pyalamode-evidence.json" in prior_map
            calls = []

            def post_guard(*parameters, **keywords):
                result = real_facades(*parameters, **keywords)
                calls.append(mode)
                if mode == "source":
                    source.write_text(source.read_text().replace("return value + 1", "return value + 2"))
                elif mode == "reference":
                    active.write_bytes(active.read_bytes() + b" ")  # same canonical ID, different exact receipt
                else:
                    (root / "writer.py").write_text('import core\ncore.total.__code__ = (lambda value: value).__code__\n')
                return result

            guards.generate_facades = post_guard
            destination = root / "accepted"
            result = project.build_paths([str(source)], root=str(root), output=str(destination))
            guards.generate_facades = real_facades
            row = {"case": "L19 " + mode, "guard_calls": calls, "raw": result.to_dict(),
                   "source_before": source_before, "source_after": hashlib.sha256(source.read_bytes()).hexdigest(),
                   "reference_before": reference_before, "reference_after": hashlib.sha256(active.read_bytes()).hexdigest(),
                   "artifact_exists": destination.exists(), "prior_raw": earlier.to_dict(),
                   "prior_before": prior_map,
                   "prior_after": {p.relative_to(prior).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in prior.rglob("*") if p.is_file()},
                   "current_source_map": {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                          for p in root.rglob("*.py")}, "product_after": model.foundation_identities()}
            log.append(row)
            assert calls == [mode]
            assert result.status == 2 and result.output is None and not destination.exists()
            assert not list(root.glob(".pyalamode-build-*"))
            assert row["prior_after"] == prior_map
            assert row["product_after"] == product_before
        outcome = "PASS"
    except Exception as error:
        outcome = "FAIL"
        log.append({"controller_error": repr(error)})
        raise
    finally:
        guards.generate_facades = real_facades
        (work / "observations.json").write_text(json.dumps({"schema": 1, "kind": "m10-fixed-build-races",
            "root_freeze_sha256": args.freeze_sha256, "outcome": outcome, "product_before": product_before,
            "observations": log, "human_measurement": {"status": "UNMEASURED", "participants": 0, "attempts": 0}},
            indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": outcome, "evidence": str(work / "observations.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

#### record_io_controller.py

Path: `/private/tmp/pyalamode-m10-review/record_io_controller.py`
Bytes: 13435; SHA-256: `7be48341f6bbeb0d31e08c94a2c5f8215d5cd7e51e94937ac12971bead40d082`.

````python
"""UNEXECUTED fixed L20-L23 installed record controls; execute after root freeze."""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from unittest.mock import patch


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode()


def addressed(record):
    record["id"] = hashlib.sha256(canonical({k: v for k, v in record.items() if k != "id"})).hexdigest()
    return record


def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted((root / ".pyalamode").rglob("*")) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--installed-product-root", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--freeze-sha256")
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED: root freeze authorization required")
        return 0
    assert args.work_root and args.installed_product_root and args.candidate and args.freeze_sha256
    work = args.work_root.resolve()
    assert not work.exists()
    work.mkdir(parents=True)
    helper = importlib.import_module("pyalamode.migration")
    views = importlib.import_module("pyalamode.migration_views")
    assert Path(helper.__file__).resolve().parent == args.installed_product_root.resolve()
    log = []
    body = ('from pyalamode import fun\n@fun\ndef f(value: int) -> int:\n'
            '    result = value\n    result = result + 1\n    return result\n')

    def project(name, *, policy=None):
        root = work / name
        root.mkdir()
        (root / "core.py").write_text(body)
        (root / "pyproject.toml").write_text(policy or (
            '[tool.pyalamode.migration]\nschema = 1\n'
            'baseline = ".pyalamode/baseline.json"\n'))
        return root

    def capture(root):
        snapshot, state, report, reference = views.observe(root, bootstrap=True)
        assert state["strict_status"] == 1 and report["status"] == 1
        return state, report, views.make_prepublish(snapshot, state, [])

    def refused(label, call):
        try:
            call()
        except helper.MigrationError as error:
            assert len(str(error)) <= 1024
            log.append({"case": label, "expected_tooling_status": 2, "error": str(error)})
        else:
            raise AssertionError(label + " must refuse")

    def cli(root, command, *extra, expected):
        argv = [str(args.candidate), command, *extra, "--root", str(root), "--json"]
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        environment.pop("PYTHONHOME", None)
        result = subprocess.run(argv, cwd=root, env=environment, capture_output=True,
                                text=True, timeout=45)
        log.append({"argv": argv, "status": result.returncode, "expected": expected,
                    "stdout": result.stdout, "stderr": result.stderr})
        assert result.returncode == expected
        return json.loads(result.stdout)

    def write(root, state, callback, **options):
        return helper.write_baseline(root, state, owner="independent fixed review",
                                     rationale="debt is not a strict waiver",
                                     prepublish=callback, **options)

    try:
        root = project("report-axes")
        state, report, callback = capture(root)
        receipt = write(root, state, callback)
        assert receipt["status"] == 0 and receipt["verified"] is False
        genuine = helper.save_report(root, report, prepublish=callback)
        assert genuine["status"] == 0 and genuine["state_strict_status"] == 1
        loaded = helper.load_reference(root, genuine["path"])
        assert loaded["record"]["report"]["status"] == 1
        audit = cli(root, "check", "--audit", expected=0)
        assert audit["status"] == 0 and audit["verified"] is False
        assert audit["migration"]["status"] == 1
        assert audit["migration"]["state"]["strict_status"] == 1
        forged = copy.deepcopy(report)
        forged["status"] = 0
        forged["verified"] = False
        prior = files(root)
        refused("L22 direct save", lambda: helper.save_report(root, forged, prepublish=callback))
        assert files(root) == prior
        bad = addressed({"schema": 1, "kind": "pyalamode-saved-report",
                         "created_at": "2035-01-01T00:00:00Z", "report": forged})
        bad_path = ".pyalamode/reports/" + bad["id"] + ".json"
        (root / bad_path).write_text(json.dumps(bad, indent=2, sort_keys=True) + "\n")
        refused("L22 valid-digest load", lambda: helper.load_reference(root, bad_path))
        cli(root, "report", "--compare", bad_path, expected=2)

        # Controlled fsync failures exercise real OS publication, not injected result statuses.
        for mode in ("temporary", "initial-active", "replace-active", "new-writer"):
            root = project("fsync-" + mode)
            state, _, callback = capture(root)
            active = root / ".pyalamode/baseline.json"
            if mode in {"replace-active", "new-writer"}:
                write(root, state, callback)
            old = active.read_bytes() if active.exists() else None
            before = files(root)
            original_fsync = helper.os.fsync
            original_replace = helper.os.replace
            injected = {"count": 0, "concurrent": None, "phase": None, "stage": None}

            def fail(fd):
                descriptor = os.fstat(fd)
                regular = stat.S_ISREG(descriptor.st_mode)
                stages = [path for path in (root / ".pyalamode").rglob(".migration-*.tmp")
                          if (path.stat(follow_symlinks=False).st_dev,
                              path.stat(follow_symlinks=False).st_ino) == (descriptor.st_dev, descriptor.st_ino)]
                changed = active.exists() and active.read_bytes() != old
                matches = (regular and bool(stages)) if mode == "temporary" else (not regular and changed)
                if matches and injected["count"] == 0:
                    injected["count"] += 1
                    injected["phase"] = "pre-yield staged file fsync" if mode == "temporary" else "post-active directory fsync"
                    injected["stage"] = stages[0].relative_to(root).as_posix() if stages else None
                    if mode == "new-writer":
                        concurrent = json.loads(active.read_text())
                        concurrent["owner"] = "independent concurrent writer"
                        addressed(concurrent)
                        raw = (json.dumps(concurrent, indent=2, sort_keys=True) + "\n").encode()
                        (root / ".pyalamode/history" / (concurrent["id"] + ".json")).write_bytes(raw)
                        temporary = active.with_name("concurrent-publication.tmp")
                        temporary.write_bytes(raw)
                        original_replace(temporary, active)
                        injected["concurrent"] = raw
                    raise OSError("fixed controlled " + mode + " fsync failure")
                return original_fsync(fd)

            with patch.object(helper.os, "fsync", side_effect=fail):
                refused("L20 " + mode, lambda: write(root, state, callback,
                        replace=mode in {"replace-active", "new-writer"}))
            assert injected["count"] == 1, "failure hook must reach its intended publication phase"
            if mode == "new-writer":
                assert active.read_bytes() == injected["concurrent"]
            elif old is None:
                assert not active.exists()
            else:
                assert active.read_bytes() == old
            after = files(root)
            assert all(after.get(path) == raw for path, raw in before.items()
                       if mode != "new-writer" or path != ".pyalamode/baseline.json")
            added = set(after) - set(before)
            assert all(path.startswith(".pyalamode/history/") and path.endswith(".json")
                       for path in added), "no temporary/lock residue"
            assert len(added) <= (2 if mode == "new-writer" else 1)
            for path in added:
                record = json.loads(after[path])
                assert addressed(copy.deepcopy(record))["id"] == record["id"]
            log.append({"case": "L20 " + mode, "added": sorted(added), "prior_preserved": mode != "new-writer",
                        "hook_phase": injected["phase"], "hook_stage": injected["stage"]})

        root = project("lineage")
        (root / "core.py").unlink()
        for name in ("A", "B"):
            (root / (name + ".py")).write_text(body)
        old_state, _, callback = capture(root)
        old_receipt = write(root, old_state, callback)
        old_record = helper.load_reference(root, old_receipt["path"])["record"]
        for name in ("A", "B"):
            (root / (name + ".py")).unlink()
        for name in ("C", "D"):
            (root / (name + ".py")).write_text(body)
        current, _, callback = capture(root)
        current_ids = {f["id"] for f in current["findings"]}
        new_receipt = write(root, current, callback, replace=True)
        child = helper.load_reference(root, new_receipt["path"])["record"]
        assert {f["id"] for f in child["state"]["findings"]} == current_ids
        assert not child["lineage"], "reviewed ambiguous move resets to fresh births"
        forged_child = copy.deepcopy(child)
        forged_child["lineage"] = []
        old_groups = {f["logical_boundary"]["selector"]: f for f in old_record["state"]["findings"]}
        assert len(old_groups) == 2 and len(forged_child["state"]["findings"]) == 2
        for finding in forged_child["state"]["findings"]:
            selector = finding["logical_boundary"]["selector"]
            old_group = old_groups[{"C:f": "A:f", "D:f": "B:f"}[selector]]
            finding["id"], finding["birth_identity"] = old_group["id"], old_group["birth_identity"]
            forged_child["lineage"].append({"id": old_group["id"],
                "previous_identity_key": old_group["identity_key"], "current_identity_key": finding["identity_key"],
                "previous_path": old_group["locations"][0]["path"], "current_path": finding["locations"][0]["path"], "count": 1})
        forged_child["lineage"].sort(key=lambda row: row["id"])
        addressed(forged_child)
        forged_path = ".pyalamode/history/" + forged_child["id"] + ".json"
        (root / forged_path).write_text(json.dumps(forged_child, indent=2, sort_keys=True) + "\n")
        refused("L21 forged ambiguous retained IDs", lambda: helper.load_reference(root, forged_path))

        root = project("custom-active")
        state, _, callback = capture(root)
        write(root, state, callback)
        default = (root / ".pyalamode/baseline.json").read_bytes()
        (root / "pyproject.toml").write_text('[tool.pyalamode]\nrequired_exports = ["core:missing"]\n'
            '[tool.pyalamode.migration]\nschema = 1\nbaseline = ".pyalamode/reviews/team.json"\nreject_new_findings = true\n')
        result = cli(root, "baseline", "--owner", "custom review", "--rationale", "preserve current debt", expected=0)
        assert result["written"]["path"] == ".pyalamode/reviews/team.json"
        assert result["written"]["state_strict_status"] == 1 and result["written"]["current_policy_status"] == 1
        assert result["report"]["state"]["current_policy_events"]["required_exports"]
        assert result["written"]["previous_id"] is None
        custom_id = result["written"]["id"]
        before = files(root)
        cli(root, "baseline", "--owner", "custom review", "--rationale", "duplicate", expected=2)
        assert files(root) == before
        replacement = cli(root, "baseline", "--owner", "custom review", "--rationale", "replacement", "--replace", expected=0)
        assert replacement["written"]["previous_id"] == custom_id
        assert (root / ".pyalamode/baseline.json").read_bytes() == default
        for reserved in ("history", "reports"):
            (root / "pyproject.toml").write_text('[tool.pyalamode.migration]\nschema = 1\nbaseline = ".pyalamode/' + reserved + '/active.json"\n')
            before = files(root)
            cli(root, "baseline", "--owner", "reserved", "--rationale", "refuse", expected=2)
            assert files(root) == before
        outcome = "PASS"
    except Exception as error:
        outcome = "FAIL"
        log.append({"controller_error": repr(error)})
        raise
    finally:
        (work / "observations.json").write_text(json.dumps({"schema": 1, "kind": "m10-record-io-controls",
            "outcome": outcome, "root_freeze_sha256": args.freeze_sha256, "observations": log,
            "human_measurement": {"status": "UNMEASURED", "participants": 0, "attempts": 0}}, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": outcome, "evidence": str(work / "observations.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

#### structural_controller.py

Path: `/private/tmp/pyalamode-m10-review/structural_controller.py`
Bytes: 18300; SHA-256: `a88bd7501f7477f1443b2285d60b18758174417a4ce4373c25f18e5531bd545e`.

````python
"""UNEXECUTED bounded fixed denominators/SCC/context/independent-policy controls."""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import importlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--installed-product-root", type=Path)
    parser.add_argument("--freeze-sha256")
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED: root freeze authorization required")
        return 0
    assert args.work_root and args.installed_product_root and args.freeze_sha256
    work = args.work_root.resolve()
    assert not work.exists()
    work.mkdir(parents=True)
    own = Path(__file__).resolve().parent
    views = importlib.import_module("pyalamode.migration_views")
    helper = importlib.import_module("pyalamode.migration")
    project = importlib.import_module("pyalamode.project")
    contracts = importlib.import_module("pyalamode.integration_contracts")
    assert Path(views.__file__).resolve().parent == args.installed_product_root.resolve()
    log = []

    def root(name, source, policy="[tool.pyalamode]\n"):
        directory = work / name
        directory.mkdir()
        (directory / "core.py").write_text(source)
        (directory / "pyproject.toml").write_text(policy)
        return directory

    def observation(directory, paths=None):
        snapshot, state, report, _ = views.observe(directory, paths=paths, bootstrap=True)
        assert state["strict_status"] == 0
        return snapshot, state, report

    try:
        core = '''from pyalamode import fun, record, variant, case, effects, Clock, ClockCapability, unsafe
@record
class Customer:
    name: str
@variant
class Choice:
    @case
    class Yes:
        value: int
    @case
    class No:
        pass
@fun
def total(value: int) -> int:
    def plus(amount: int) -> int:
        return amount + 1
    return plus(value)
@effects(Clock)
def now(clock: ClockCapability) -> int:
    return clock.now_ns()
def ordinary(value: int) -> int:
    return value
async def deferred(value: int) -> int:
    return value
class Service:
    def method(self) -> int:
        return 0
@unsafe(scope="legacy", rationale="reviewed shell")
def raw() -> int:
    return 1
'''
        directory = root("denominator", core)
        (directory / "__init__.py").write_bytes(b"")
        (directory / "plain.py").write_text("def unused(value: int) -> int:\n    return value\n")
        (directory / "strict.py").write_text("# mode: fun\ndef double(value: int) -> int:\n    return value * 2\n")
        for name in (".git", ".venv", "__pycache__", "build", "dist", ".pyalamode-cache",
                     ".pyalamode", "fixture.egg-info", ".pyalamode-build-fixed"):
            (directory / name).mkdir()
            (directory / name / "poison.py").write_text("this is invalid Python !!!\n")
        snapshot, state, report = observation(directory, [str(directory / "plain.py")])
        expected = {"eligible_modules": 4, "selected_modules": 1, "checked_modules": 1,
                    "eligible_functions": 9, "selected_functions": 4, "checked_functions": 4,
                    "checked_exports": 5, "selected_records": 1, "selected_variants": 1}
        assert state["coverage"] == expected
        assert state["scope"]["displayed_paths"] == ["plain.py"]
        assert len(state["scope"]["selected_paths"]) == 4
        empty = [row for row in state["boundaries"] if row["kind"] == "module" and row["path"] == "__init__.py"]
        assert len(empty) == 1 and empty[0]["selector"] == "module:" and empty[0]["qualified_name"] == ""
        assert not empty[0]["public_export"]
        cold = project.check_paths(root=str(directory), cache=True)
        warm = project.check_paths(root=str(directory), cache=True)
        assert cold.status == 0 and warm.status == 0
        log.append({"case": "denominators", "raw": views.regions_view(snapshot, state),
                    "cache_cold": cold.to_dict(), "cache_warm": warm.to_dict(),
                    "untimed_inventory": {**expected, "source_bytes": sum((directory / p).stat().st_size for p in state["scope"]["selected_paths"]),
                                          "exclusions": len(state["scope"]["exclusions"]), "human_measurement": "UNMEASURED"}})

        queue = '''from typing import Callable
from pyalamode import fun
from dep import leaf as actual_leaf
def middle(value: int) -> int: return actual_leaf(value)
def outer(value: int) -> int: return middle(value)
def left(value: int) -> int: return right(value)
def right(value: int) -> int: return left(value)
def uses_cycle(value: int) -> int: return left(value)
def factory() -> Callable[[int], int]: return actual_leaf
def uses_alias(value: int) -> int: return actual_leaf(value)
@fun
def checked(value: int) -> int: return value + 1
def uses_checked(value: int) -> int: return checked(1)
def shadow(leaf: Callable[[int], int], value: int) -> int: return leaf(value)
def unknown(value: int) -> int: return missing(value)
'''
        directory = root("readiness", queue)
        (directory / "dep.py").write_text("from pyalamode import fun\ndef leaf(value: int) -> int:\n    return value\n")
        snapshot, state, _ = observation(directory)
        ready = views.ready_view(snapshot, state)
        groups = ready["groups"]
        members = [member for group in groups for member in group["members"]]
        expected_members = {"dep:leaf", *("core:" + name for name in ("middle", "outer", "left", "right", "uses_cycle", "factory", "uses_alias", "uses_checked", "shadow", "unknown"))}
        assert set(members) == expected_members and len(members) == len(set(members))
        index = {member: i for i, group in enumerate(groups) for member in group["members"]}
        assert index["dep:leaf"] < index["core:middle"] < index["core:outer"]
        assert index["core:left"] == index["core:right"] < index["core:uses_cycle"]
        cycle = groups[index["core:left"]]
        assert cycle["recursive"] and set(cycle["members"]) == {"core:left", "core:right"}
        edge = {(row["caller"].rsplit("::", 1)[1], row["callee"].rsplit("::", 1)[1], row["kind"]) for row in ready["edges"]}
        assert ("factory", "leaf", "retained") in edge and ("factory", "leaf", "direct") not in edge
        assert not any(caller == "shadow" and callee == "leaf" for caller, callee, _ in edge)
        assert any(name.endswith("::checked") for name in groups[index["core:uses_checked"]]["checked_prerequisites"])
        assert groups[index["core:unknown"]]["blockers"]
        for group in groups:
            for contract in group["contracts"]:
                assert contract["source_evidence"].startswith("hypothetical candidate analysis:")
                assert "analysis" in contract["freshness"]
        log.append({"case": "readiness", "raw": ready,
                    "untimed_inventory": {"scc_groups": len(groups), "edges": len(ready["edges"]),
                                          "direct_edges": sum(row["kind"] == "direct" for row in ready["edges"]),
                                          "retained_edges": sum(row["kind"] == "retained" for row in ready["edges"])}})

        tree = ast.parse((own / "context_literals.py").read_text())
        literals = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                        and any(isinstance(target, ast.Name) and target.id == "CASES" for target in node.targets))
        expected_contexts = json.loads((own / "context-literals.json").read_text())
        template = next(row for row in state["boundaries"] if row["kind"] == "function")
        for name, (rule, origin, minimal) in literals.items():
            module = name == "C241"
            declaration = name == "C310"
            source = minimal if module or declaration else "def f() -> int:\n" + "".join("    " + line + "\n" for line in minimal.splitlines())
            parsed = ast.parse(source)
            node = parsed.body[0] if module or declaration else parsed.body[0].body[0]
            boundary = copy.deepcopy(template)
            boundary.update({"kind": "module" if module else "function", "selector": "module:core" if module else "core:" + ("now" if declaration else "f"),
                             "qualified_name": "core" if module else ("now" if declaration else "f"), "path": "core.py"})
            owner = parsed.body[0]
            boundary["location"] = {"path": "core.py", "line": owner.lineno, "column": owner.col_offset + 1,
                                    "end_line": owner.end_lineno, "end_column": owner.end_col_offset + 1,
                                    "column_encoding": "utf-8-bytes"}
            diagnostic = {"rule": rule, "path": "core.py", "line": node.lineno, "column": node.col_offset + 1,
                          "end_line": node.end_lineno, "end_column": node.end_col_offset + 1, "column_encoding": "utf-8-bytes",
                          "boundary": "<module>" if module else boundary["qualified_name"], "origin": origin,
                          "reason": "fixed literal", "remediation": "review", "first_binding": None}
            result = helper.finding_context(source, diagnostic, boundary)
            assert result == {"kind": "ast-statement", "ast": expected_contexts[name]["ast"]}
            log.append({"case": name, "context": result})
        extra = json.loads((own / "extra_literal_probes.json").read_text())["cases"]
        unicode = extra["D19"]
        boundary.update({"kind": "function", "selector": "core:f", "qualified_name": "f"})
        owner = ast.parse(unicode["source"]).body[0]
        boundary["location"] = {"path": "core.py", "line": owner.lineno, "column": owner.col_offset + 1,
                                "end_line": owner.end_lineno, "end_column": owner.end_col_offset + 1,
                                "column_encoding": "utf-8-bytes"}
        diagnostic.update(unicode["diagnostic_range"], rule="PAL101", boundary="f", origin="static source")
        assert helper.finding_context(unicode["source"], diagnostic, boundary) == unicode["expected_context"]
        log.append({"case": "D19", "context": unicode["expected_context"]})

        directory = root("unsafe-body", extra["P29"]["before_source"], '[tool.pyalamode.migration]\nschema=1\nreject_unsafe_weakening=true\n')
        _, before, _ = observation(directory)
        (directory / "core.py").write_text(extra["P29"]["current_source"])
        _, current, _ = observation(directory)
        comparison = helper.compare_states(before, current)
        gates = helper.evaluate_gates(comparison, current["policy"]["migration"])
        assert comparison["unsafe_weakening"] and gates["status"] == 1
        log.append({"case": "P29", "comparison": comparison, "gates": gates})

        directory = root("unused-manifest", extra["P30"]["source"], '[tool.pyalamode]\nintegration_manifests=["contracts.json"]\n'
                         '[tool.pyalamode.migration]\nschema=1\nreject_policy_weakening=true\n')
        catalog = contracts.integration_snapshot({}, directory)
        candidate = next(row for row in catalog["catalog"] if row["identity"] == extra["P30"]["unused_operation"])
        manifest = {"schema": 1, "operation": candidate["identity"], "status": "reviewed", "base_contract_sha256": candidate["contract_sha256"],
                    "effects": candidate["effects"], "failures": candidate["failures"], "owner": "independent temporary review",
                    "rationale": "same-path unused conservative contract", "provenance": "actual product candidate identity"}
        (directory / "contracts.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        _, before, _ = observation(directory)
        manifest["effects"] = sorted(set(manifest["effects"]) | {"Clock"})
        (directory / "contracts.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        _, current, _ = observation(directory)
        comparison = helper.compare_states(before, current)
        gates = helper.evaluate_gates(comparison, current["policy"]["migration"])
        assert comparison["policy_weakening"] and comparison["inputs_changed"] and gates["status"] == 1
        assert not comparison["new_trust"] and not comparison["approval_failures"]
        log.append({"case": "P30", "comparison": comparison, "gates": gates, "actual_manifest": manifest})

        def actual_sha_policy(directory, gate, expiry=None):
            snapshot = contracts.integration_snapshot({}, directory)
            native = next(row for row in snapshot["catalog"] if row["identity"] == "pyalamode.integrations.sha256_digest")
            assert not snapshot["errors"] and native["dependency_sha256"] is not None
            policy = ('[tool.pyalamode]\nexternal_trust="approved"\n[tool.pyalamode.migration]\nschema=1\n'
                      + gate + '=true\n[[tool.pyalamode.integration_approvals]]\n'
                      + 'operation="pyalamode.integrations.sha256_digest"\n'
                      + 'contract_sha256=' + json.dumps(native["contract_sha256"]) + '\n'
                      + 'dependency_sha256=' + json.dumps(native["dependency_sha256"]) + '\n'
                      + 'owner="independent temporary review"\nrationale="actual environment native identity"\n'
                      + 'provenance="fixed A26 temporary fixture"\n')
            if expiry:
                policy += 'expires_at=' + json.dumps(expiry) + '\n'
            return policy, native

        # P05/A26: approved real native trust remains an independent gate with no source debt.
        before_source = ('from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n'
                         '@fun\ndef digest(data: bytes) -> bytes:\n    return data\n')
        directory = root("new-native-trust", before_source)
        policy, native = actual_sha_policy(directory, "reject_new_trust")
        (directory / "pyproject.toml").write_text(policy)
        _, before, _ = observation(directory)
        (directory / "core.py").write_text(before_source.replace("return data", "return sha256_digest(data)"))
        _, current, _ = observation(directory)
        comparison = helper.compare_states(before, current)
        gates = helper.evaluate_gates(comparison, current["policy"]["migration"])
        assert not before["findings"] and not current["findings"]
        assert all(row["effect_bound"] == [] and row["required_effects"] == []
                   for captured in (before, current) for row in captured["boundaries"]
                   if row["selector"] == "core:digest")
        assert comparison["new_trust"] and gates["status"] == 1
        assert current["required_operations"] and not comparison["approval_failures"]
        log.append({"case": "A26 native trust", "before": before, "current": current,
                    "comparison": comparison, "gates": gates, "actual_identity": native})

        # P02/A26: same authored selector changes declared and actual Clock dimensions.
        directory = root("expanded-clock", 'from pyalamode import fun, effects, Clock, ClockCapability\n'
                         '@fun\ndef f(value: int) -> int:\n    return value\n',
                         '[tool.pyalamode.migration]\nschema=1\nreject_expanded_effects=true\n')
        _, before, _ = observation(directory)
        (directory / "core.py").write_text('from pyalamode import fun, effects, Clock, ClockCapability\n'
                                           '@effects(Clock)\ndef f(clock: ClockCapability) -> int:\n    return clock.now_ns()\n')
        _, current, _ = observation(directory)
        comparison = helper.compare_states(before, current)
        gates = helper.evaluate_gates(comparison, current["policy"]["migration"])
        boundary = next(row for row in current["boundaries"] if row["selector"] == "core:f")
        assert boundary["effect_bound"] == ["Clock"] and boundary["required_effects"] == ["Clock"]
        assert not before["findings"] and not current["findings"]
        assert comparison["expanded_effects"] and gates["status"] == 1
        log.append({"case": "A26 declared/required Clock", "before": before, "current": current,
                    "comparison": comparison, "gates": gates})

        # P11/A26: unused configured expiry fails current policy without a fabricated consumer.
        directory = root("unused-expiry", extra["P30"]["source"])
        policy, native = actual_sha_policy(directory, "reject_expired_approvals", "2099-01-01T00:00:00Z")
        (directory / "pyproject.toml").write_text(policy)
        _, before, _ = observation(directory)
        (directory / "pyproject.toml").write_text(policy.replace("2099-01-01", "2000-01-01"))
        _, current, _ = observation(directory)
        comparison = helper.compare_states(before, current)
        gates = helper.evaluate_gates(comparison, current["policy"]["migration"])
        assert current["current_policy_status"] == 1 and comparison["expired_approvals"] and gates["status"] == 1
        assert not current["required_operations"] and not comparison["new_trust"] and not comparison["approval_failures"]
        assert not any(row["rule"] == "PAL350" for row in current["findings"])
        log.append({"case": "A26 unused expiry", "before": before, "current": current,
                    "comparison": comparison, "gates": gates, "actual_identity": native})
        outcome = "PASS"
    except Exception as error:
        outcome = "FAIL"
        log.append({"controller_error": repr(error)})
        raise
    finally:
        (work / "observations.json").write_text(json.dumps({"schema": 1, "kind": "m10-fixed-structural-controls",
            "root_freeze_sha256": args.freeze_sha256, "outcome": outcome, "observations": log,
            "human_measurement": {"status": "UNMEASURED", "participants": 0, "attempts": 0}}, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": outcome, "evidence": str(work / "observations.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

#### wheel_controller.py

Path: `/private/tmp/pyalamode-m10-review/wheel_controller.py`
Bytes: 8407; SHA-256: `c5e5128be5b9e024ddc96728bef4a1009c9800e0241f4b34b97b461b25b61a32`.

````python
"""UNEXECUTED bounded fresh-wheel driver; offline native/Linux, root freeze required."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", type=Path)
    parser.add_argument("--checkout-root", type=Path)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--build-backend-target", type=Path)
    parser.add_argument("--review-intent", type=Path)
    parser.add_argument("--path-map", type=Path)
    parser.add_argument("--execute-frozen-candidate", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen_candidate:
        print("UNEXECUTED: root freeze authorization required")
        return 0
    assert args.freeze and args.checkout_root and args.work_root and args.build_backend_target and args.review_intent
    freeze_bytes = args.freeze.read_bytes()
    frozen = json.loads(freeze_bytes)
    freeze_sha = hashlib.sha256(freeze_bytes).hexdigest()
    review_bytes = args.review_intent.read_bytes()
    review = json.loads(review_bytes)
    review_sha = hashlib.sha256(review_bytes).hexdigest()
    assert review["source_freeze"]["sha256"] == freeze_sha
    checkout = args.checkout_root.resolve()
    work = args.work_root.resolve()
    assert not work.exists() and not work.is_relative_to(checkout)
    work.mkdir(parents=True)
    remaps = json.loads(args.path_map.read_text()) if args.path_map else {}
    assert isinstance(remaps, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in remaps.items())
    own = Path(__file__).resolve().parent
    raw, phases = [], []
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)
    environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"

    def remap(value):
        path = Path(value)
        for prefix, replacement in sorted(remaps.items(), key=lambda item: -len(item[0])):
            if path.is_relative_to(prefix):
                return Path(replacement) / path.relative_to(prefix)
        return path

    def frozen_maps():
        assert sha(args.freeze) == freeze_sha and sha(args.review_intent) == review_sha
        source = {relative: sha(checkout / relative) for relative in frozen["inputs"]}
        controllers = {original: sha(remap(original)) for original in frozen["controllers"]}
        peer = {original: sha(remap(original)) for original in review["controllers"]}
        assert source == frozen["inputs"] and controllers == frozen["controllers"] and peer == review["controllers"]
        tops = {Path(relative).parts[0] for relative in frozen["inputs"] if len(Path(relative).parts) > 1}
        ignored = {"__pycache__", "node_modules", ".pyalamode-cache", ".pytest_cache", ".DS_Store"}
        discovered = {relative for relative in frozen["inputs"] if len(Path(relative).parts) == 1}
        for top in tops:
            discovered.update(path.relative_to(checkout).as_posix() for path in (checkout / top).rglob("*")
                              if path.is_file() and not any(part in ignored for part in path.relative_to(checkout).parts))
        assert discovered == set(frozen["inputs"]), "frozen source inventory changed"
        return {"source": source, "root_controllers": controllers, "review_controllers": peer}

    def run(argv, *, cwd=None, env=None):
        result = subprocess.run([str(item) for item in argv], cwd=cwd or work,
                                env=env or environment, capture_output=True, text=True, timeout=180)
        raw.append({"argv": [str(item) for item in argv], "cwd": str(cwd or work),
                    "status": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        assert result.returncode == 0, raw[-1]
        return result.stdout

    try:
        initial = frozen_maps()
        distribution = work / "distribution-source"
        distribution.mkdir()
        for relative in frozen["inputs"]:
            destination = distribution / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checkout / relative, destination)
        assert "pyproject.toml" in frozen["inputs"]
        wheels = work / "wheels"
        wheels.mkdir()
        packaging_environment = dict(environment)
        packaging_environment["PYTHONPATH"] = str(args.build_backend_target.resolve())
        run([sys.executable, "-m", "pip", "wheel", "--no-index", "--no-deps", "--no-build-isolation",
             distribution, "-w", wheels], cwd=distribution, env=packaging_environment)
        wheel_paths = list(wheels.glob("*.whl"))
        assert len(wheel_paths) == 1
        wheel = wheel_paths[0]
        with zipfile.ZipFile(wheel) as archive:
            wheel_map = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist() if not name.endswith("/")}
        package_members = {Path(name).name: value for name, value in wheel_map.items() if name.startswith("pyalamode/")}
        assert len(package_members) == len([name for name in wheel_map if name.startswith("pyalamode/")])
        assert package_members == frozen["package_files"]
        venv = work / "consumer-venv"
        run([sys.executable, "-I", "-m", "venv", venv])
        python = venv / "bin/python"
        run([python, "-I", "-m", "pip", "install", "--no-index", "--no-deps", wheel])
        cli = venv / "bin/pyalamode"

        def phase(label):
            maps = frozen_maps()
            provenance = json.loads(run([python, "-I", own / "installed_provenance.py", "--checkout-root", checkout,
                                         "--execute-frozen-candidate"]))
            product = Path(provenance["product_root"])
            maps["package"] = {name: sha(product / name) for name in frozen["package_files"]}
            maps["product"] = {name: sha(product / name) for name in frozen["product_artifacts"]}
            assert maps["package"] == frozen["package_files"] and maps["product"] == frozen["product_artifacts"]
            assert provenance["product_artifacts"] == frozen["product_artifacts"]
            phases.append({"phase": label, "maps": maps, "provenance": provenance})
            return product

        product = phase("before")
        for script in ("cli_controller.py", "structural_controller.py", "record_io_controller.py",
                       "late_build_probe.py", "race_build_controller.py"):
            arguments = [python, "-I", own / script, "--work-root", work / script.removesuffix(".py"),
                         "--freeze-sha256", freeze_sha, "--execute-frozen-candidate"]
            if script in {"cli_controller.py", "record_io_controller.py"}:
                arguments.extend(["--candidate", cli])
            if script != "cli_controller.py":
                arguments.extend(["--installed-product-root", product])
            run(arguments)
            phase("cross:" + script)
        phase("after")
        assert frozen_maps() == initial
        outcome = "PASS"
    except Exception as error:
        outcome = "FAIL"
        raw.append({"controller_error": repr(error)})
        raise
    finally:
        evidence = {"schema": 1, "kind": "m10-fresh-wheel-controls", "outcome": outcome,
                    "root_freeze_sha256": freeze_sha, "raw": raw, "phases": phases,
                    "review_controller_intent_sha256": review_sha,
                    "ordinary_console_startup_assumptions": True,
                    "packaging_only_pythonpath": str(args.build_backend_target),
                    "human_measurement": {"status": "UNMEASURED", "participants": 0, "attempts": 0}}
        if "wheel" in locals() and "wheel_map" in locals():
            evidence.update({"wheel": str(wheel), "wheel_sha256": sha(wheel), "wheel_members": wheel_map})
        evidence["raw_artifact_hashes"] = {p.relative_to(work).as_posix(): sha(p) for p in work.rglob("observations.json")}
        (work / "observations.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": outcome, "evidence": str(work / "observations.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````
