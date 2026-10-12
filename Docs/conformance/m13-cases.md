# M13 independent characterized-task acceptance plan

Status: PREPARATION ONLY. No candidate check, build, install, runtime, controller,
QA, suite or benchmark has run for this review. No application/product module
has been imported during preparation. Standard-library reads, AST parsing,
literal generation, byte copying and hashing establish preparation identities
only. Source/plan review and a separate root execution release remain required.

Owner `/root/m13_review` owns this new document and
`/tmp/pyalamode-m13-review` only. Root owns product source review, target setup,
all Docker/container operations, release, evidence publication and Git commits.
The guide, worksheet, README additions, M14 plan and incidental files are outside
this review's ownership. No external chat, CatWrangler or automation is involved.

Authority is `SPEC-sol6.1-composite.md` §13.2, A30 and roadmap13, retaining
A01–A29/A32–A35. M12 prerequisite is committed `d58ccbd`: independent root
acceptance of 506 methods, 40 installed commands/121 assertions and 148 fixed
cases on native CPython3.13.1 standard GIL/macOS arm64 and actual copied-input
Linux aarch64. Those are historical prerequisite observations, not M13 results.
No applicable workspace, ancestor or nested AGENTS.md was found.

Human participants, attempts, authoring-time and usefulness observations are
all zero. This correctness plan creates no benchmark condition, timed loop or
performance claim. Arbitrary Python thread scheduling remains nondeterministic;
the finite live and controlled contracts below concern only their specified
task facility. No automatic parallel speedup is promised.

## Genuine prerequisite retention before central changes

Before any M13 version change, standard-library preparation copied the actual
24 product files and parsed the literal M12 model labels. The immutable receipt
is `/tmp/pyalamode-m13-review/authentic-m12/profile.json` (11378 bytes, SHA256
`8f4e2032dd7054642862a6334737cc10b371d11d43d7e02aa10d0e3bcd27eb4f`). It records
checker `confined-builders-12.0`, operation contract
`scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-builder-ops-12`,
edition `python-v1`, target `cpython-3.13.1` and the authentic 24 file hashes.
It imports no product code and creates no new certificate.

Byte-exact original H03-clean, H03-weakening and H07 M12 source, policy,
baseline/history/report, original command/raw streams and root final receipts
are retained under `/tmp/pyalamode-m13-review/history`. H07 preserves genuine
strict source debt; H03 preserves genuine successful schema3/product24 and the
separate policy gate. H01/H02 retain the original schema2/product22 M11 and
schema1/product19 M10 predecessor closures. No historical ID, birth, count,
root, timestamp, policy, version or digest has been edited.

Original M12 wheel2 copies have these exact identities:

| Guard mode | Bytes | SHA256 |
| --- | ---: | --- |
| off | 27026 | cde07e24c8335ce48f187a5107c306190550a1d4a5b3b7d87e05a452cfa26649 |
| exports | 29308 | ee2afee4e8b60d437e31d3a13c456e2bdc26340930262ca99563a781b3d0bcf6 |
| debug | 31439 | efd98e19b59a6dcd91cd98cfff9701c263ed7e8f54891610a6e0d19795dde316 |

All originate in accepted
`/tmp/pyalamode-m12-review/runs/native-08/distribution-history/wheels`.
The genuine M11 wheel1 is 67958 bytes, SHA256
`272be9de20f15a186905c288fe0609b3a74f8d2a0aaa8c89c61deff58e1d118e`;
its original M11 path/copy receipt is retained separately. The cumulative
original-to-copy receipt is `history/receipt-map-02.json` (37689 bytes, SHA256
`f8eb32f913e24981ce797e452a4f4a744bb36d5a0367a99f6f03e38313514b5e`), retaining
the first map unchanged. Root must review these originals before accepting
new finite historical validators. Inventing schema3 or relabeling old source
does not create historical provenance.

## Frozen joint API and acceptance dependencies

Root approval remains pending. The exact ordinary factories are
`live_tasks(workers, /, *, max_tasks=256)` (exact ints1..4 and1..256) and
`controlled_tasks(order, /, *, cancel_after=None)` (exact tuple permutation of
0..n-1, n0..256; cutoff None or exact int0..n). Bool/subclasses/foreign shapes
raise TypeError; invalid bounds/permutations/cardinality raise ValueError.
`task_map(tasks, callback, messages, /)` and
`task_map_with(tasks, capability, callback, messages, /)` return exact Vector.
Every callback alternative/capture/wrapper requires actual checked evidence;
T/R must be recursive stable data. The explicit capability is one exact
pre-M13 IO/State/Clock/Random/Environment capability, excluding Task. Runtime
FunctionType/data validation establishes no static capture/purity certificate.

Task plus every callback declared/required/external effect stays visible even
for a controlled provider or declaration-only fake Clock callback. Task markers
remain recognized when `tasks` is omitted/false; actual invocation is refused
at its Call with PAL382. Nonbool tasks policy is PAL001, process2/tooling2. Inherited
PAL221/230/240/310/320/381 remain source refusals at their literal authored sites.
No PAL390/PAL391 is allocated by this packet. Current proposed labels are
checker `characterized-tasks-13.0`, operation
`scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-builder-task-ops-13`,
package27/foundation26, migration4 and wheel3. Authentic M12 state3/24+wheel2,
M11 state2/22+wheel1 and M10 state1/19 retain exact old provenance; compatibility
never reissues old evidence as current.

Controlled callbacks run serially on the owner thread in the exact schedule;
results remain input ordered. Cutoff<n raises RuntimeError after that successful
prefix with no partial result; cutoff=n including empty0 succeeds. First
scheduled callback/result failure wins unchanged before a later cutoff. Live1
runs serially on its caller; live2..4 use bounded input-index waves, within-wave
scheduling nondeterministic, and select the lowest input-index callback/result
error in the first failing wave after normal joins. Later waves are omitted.
Provider busy reentry/foreign owner/expired lease/revocation raise RuntimeError;
sequential reuse works after successful cleanup. Explicit-capability live calls
require workers1 before callbacks; every invocation has a fresh same-thread
borrow, including result validation, whose descendants expire on each exit.

Coordinator start/join BaseException has first-object priority over callback
failures. Every attempted nonzero-ident handle receives an initial join, then
failed joins receive at most one retry after all initial joins. Successful
cleanup restores idle; unresolved retry permanently revokes the provider.
Repeated signals/native OS failure can prevent complete joins or termination.
No universal all-exit guarantee or worker preemption is claimed. Root must
review the final native implementation and retain the focused runtime helper's
start-before/after-native-start and join-interruption/retry/revocation controls
as a separate acceptance prerequisite; this finite reviewer matrix adds no
unapproved private seam or simulated OS claim.

Supported execution assumes no application audit/trace/profile/monitoring hooks
introducing unknown behavior. The actual native start emits an audit event;
checked direct/aliased sys.addaudithook registrations invalidate the task
foundation/cache at the task call (N33/N34/F06). No runtime hidden-hook registry
absence inference is used. Unknown threading remains ordinary nondeterminism;
no automatic speedup or human authoring benefit is asserted.

The frozen revised runtime plan is `api/runtime-plan-02.md`; its catalog is
`api/task-contract-literals.json` SHA256
`8e10e3c5919a2ab1620db97a68bec899085592dcb682e824778bf62b6e4c4270`.
The exact30 operation keys and8 setup keys plus task_scopes operation/line/end_line,
message/result/callback schemas, actual sorted callback targets, nullable
capability and shared ordering/cancellation/failure/lifetime strings are pinned
there. Revision01 is preserved separately, unchanged. Producer callback targets
must resolve under actual producer source; fresh dependency targets resolve
under actual installed source. Only their disclosed module/tail relation is
normalized, while every other task scope field remains exact.

## Fixed execution and preservation contract

The four held groups use separate fresh outside venvs and an installed frozen
wheel, --no-index/--no-deps, literal CPython3.13.1 standard GIL/macOS arm64 and
then root-owned actual copied-input Linux aarch64. Root supplies a disclosed finite frozen source copy that excludes old evidence
archives; its complete path set is rediscovered for every child. Every loaded
product module must resolve under installedproduct; checkout/PYTHONPATH/PYTHONHOME/.pth leaks
are refused. The full small child environment is explicit: os.defpath PATH,
C locale, PYTHONUTF8=1, UTF-8 stdio, owned TMPDIR, pip no-index/no-config.
No inherited credential-bearing environment is copied.

`planned-execution.json` is the closed symbolic complete argv/cwd/status plan;
only root-reviewed physical paths expand. Each command is bounded60seconds.
Before assertion/parsing, commands.json retains actual argv/cwd/environment,
status/engine failure and original stdout/stderr bytes. Complete before/after
input maps are rediscovered each command, retained once by content SHA, with
phase maps and explicit argument/project/cache/native/installed identities.
Owned mutations restore bytes/modes/mtime in finally. Every failed run stays
in its separate outside tree; no earlier failure is overwritten or projected
away. Controller/library/script bytes and literal maps remain frozen.

Positive source uses check0/build0 then fixed ordinary stock invocation;
negative strict source uses1/unverified/no fresh artifact. Malformed metadata
and provenance use2/PAL001; malformed tasks source policy uses2/PAL001.
Dependency input status, source status, completeness, verification, current
policy, historical gate, command/write statuses and owned findings remain
separate axes. H05 ordinary SDK catches MigrationError with process0 and no
publication; it makes no invented CLI PAL001 assertion. H03 contains two fixed
separate projects for tasks-enable policy and pure-to-Task effect expansion.

No controller, candidate, product import, suite, runtime, install, benchmark or
QA execution is released. Standard-library authoring/AST parsing/hash receipts
are preparation only. Root must review the complete packet and final source,
then issue a release pinning case/controller/source/product/wheel identities.
The final independent result needs every finite group on both targets and root
reconciliation of inherited suites/focused native fault controls. Human and
timing observations remain0. STOP pending root review.

## Independently fixed finite literals

The complete case corpus is `cases.json`, SHA256 `475d229e8dc751175427f627c05ffdf38e3972b47f3476d49c327ea9b7e6f039`. Counts: distribution-history 16, guard-freshness 10, runtime 24, source 51; total 101. The original 101-case corpus was authored before observation; N24/G02 expectations were corrected after retained native02 observations against inherited authority, and the D01 controller path was corrected separately, as disclosed in `/tmp/pyalamode-m13-review-correction-plan-01/correction-receipt.json` and `/tmp/pyalamode-m13-review-correction-plan-01/observed-history.json`. The N27 expectation was corrected after retained native03 observations against the callback-site source authority, as disclosed in `/tmp/pyalamode-m13-review-n27-correction-plan-01/correction-receipt.json` and `/tmp/pyalamode-m13-review-n27-correction-plan-01/observed-history.json`. Status values for runtime IDs are ordinary process statuses and their verified axis is null.

### source

| ID | Authored purpose | Exact expected fields |
| --- | --- | --- |
| P01 | empty controlled map | `{"diagnostic":null,"ordinary_stdout":"[]\n","projection":{"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P02 | permuted schedule retains input result order | `{"diagnostic":null,"ordinary_stdout":"[6,10,14]\n","projection":{"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P03 | recursive stable message and result data | `{"diagnostic":null,"ordinary_stdout":"[[[5,3],4],[[11,7],8]]\n","projection":{"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P04 | nested checked callback stable scalar and Vector captures | `{"diagnostic":null,"ordinary_stdout":"[21,23]\n","projection":{"callback":"make.cb","captures":{"extra":"Vector[int]","offset":"int"},"effect_bound":["Task"],"failures_include":["IndexError"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P05 | checked callback alias retains actual target | `{"diagnostic":null,"ordinary_stdout":"[6]\n","projection":{"callback_targets":["cb"],"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P06 | conditional checked alternatives retain complete target union | `{"diagnostic":null,"ordinary_stdout":"[4,6]\n","projection":{"callback_targets":["cb","other"],"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P07 | returned checked closure specializes stable capture evidence | `{"diagnostic":null,"ordinary_stdout":"[10,12]\n","projection":{"callback_targets":["factory.cb"],"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P08 | positional-only fixed callback | `{"diagnostic":null,"ordinary_stdout":"[6]\n","projection":{"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P09 | declaration-only callback effect is never erased by fake scheduling | `{"diagnostic":null,"ordinary_stdout":"[6,10]\n","projection":{"effect_bound":["Clock","Task"],"required_effects":["Clock","Task"]},"status":0,"verified":true}` |
| P10 | callback failure handler retains Task and removes handled category | `{"diagnostic":null,"ordinary_stdout":"[]\n","projection":{"effect_bound":["Task"],"failures_excludes":["ZeroDivisionError"],"handlers_include":["ZeroDivisionError"],"required_effects":["Task"]},"status":0,"verified":true}` |
| P11 | explicit Clock same-thread invocation borrow | `{"diagnostic":null,"ordinary_stdout":"[32,28]\n","projection":{"capability":"ClockCapability","effect_bound":["Clock","Task"],"required_effects":["Clock","Task"]},"status":0,"verified":true}` |
| P12 | explicit State same-thread invocation borrow | `{"diagnostic":null,"ordinary_stdout":"[18,15]\n","projection":{"capability":"StateCapability","effect_bound":["State","Task"],"required_effects":["State","Task"]},"status":0,"verified":true}` |
| P13 | explicit IO same-thread invocation borrow | `{"diagnostic":null,"ordinary_stdout":"[\"valuea\",\"valueb\"]\n","projection":{"capability":"IOCapability","effect_bound":["IO","Task"],"required_effects":["IO","Task"]},"status":0,"verified":true}` |
| P14 | explicit Random same-thread invocation borrow | `{"diagnostic":null,"ordinary_stdout":"[10,7]\n","projection":{"capability":"RandomCapability","effect_bound":["Random","Task"],"required_effects":["Random","Task"]},"status":0,"verified":true}` |
| P15 | explicit Environment same-thread invocation borrow | `{"diagnostic":null,"ordinary_stdout":"[\"valuea\",\"valueb\"]\n","projection":{"capability":"EnvironmentCapability","effect_bound":["Environment","Task"],"required_effects":["Environment","Task"]},"status":0,"verified":true}` |
| P16 | nested incoming borrow preserves lifetime and external effect | `{"diagnostic":null,"ordinary_stdout":"[26,34]\n","projection":{"borrow_scopes":1,"capability":"ClockCapability","effect_bound":["Clock","Task"],"required_effects":["Clock","Task"]},"status":0,"verified":true}` |
| N01 | tasks default off | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL382"},"projection":{},"status":1,"verified":false}` |
| N02 | tasks explicitly false | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL382"},"projection":{},"status":1,"verified":false}` |
| N03 | malformed string policy is tooling | `{"diagnostic":{"column":1,"column_encoding":"utf-8-bytes","line":1,"path":"pyproject.toml","rule":"PAL001"},"projection":{},"status":2,"verified":false}` |
| N04 | pure parent cannot erase Task | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL310"},"projection":{},"status":1,"verified":false}` |
| N05 | undeclared callback effect union refused | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL310"},"projection":{},"status":1,"verified":false}` |
| N06 | ordinary unknown callback has no checked evidence | `{"diagnostic":{"column":27,"column_encoding":"utf-8-bytes","line":6,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N07 | mutable global capture refused | `{"diagnostic":{"column":14,"column_encoding":"utf-8-bytes","line":5,"path":"core.py","rule":"PAL240"},"projection":{},"status":1,"verified":false}` |
| N08 | changing scalar dependency capture refused | `{"diagnostic":{"column":14,"column_encoding":"utf-8-bytes","line":5,"path":"core.py","rule":"PAL240"},"projection":{},"status":1,"verified":false}` |
| N09 | external capability capture cannot cross task | `{"diagnostic":{"column":18,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL320"},"projection":{},"status":1,"verified":false}` |
| N10 | task capability capture cannot cross task | `{"diagnostic":{"column":25,"column_encoding":"utf-8-bytes","line":6,"path":"core.py","rule":"PAL320"},"projection":{},"status":1,"verified":false}` |
| N11 | callback input type mismatch | `{"diagnostic":{"column":27,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N12 | callback extra keyword-only/default parameter refused | `{"diagnostic":{"column":27,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N13 | callback wrong data result schema refused | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL211"},"projection":{},"status":1,"verified":false}` |
| N14 | mutable callback annotation refused | `{"diagnostic":{"column":10,"column_encoding":"utf-8-bytes","line":3,"path":"core.py","rule":"PAL130"},"projection":{},"status":1,"verified":false}` |
| N15 | mutable task messages refused | `{"diagnostic":{"column":30,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL201"},"projection":{},"status":1,"verified":false}` |
| N16 | tuple is not exact Vector messages | `{"diagnostic":{"column":30,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N17 | task keyword signature refused | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N18 | task result cannot be silently ignored | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL250"},"projection":{},"status":1,"verified":false}` |
| N19 | unknown Task operation remains refused despite declaration | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL230"},"projection":{},"status":1,"verified":false}` |
| N20 | Task capability alias refused | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL320"},"projection":{},"status":1,"verified":false}` |
| N21 | Task capability cannot be stable tuple data | `{"diagnostic":{"column":14,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N22 | provider construction in checked body remains ordinary setup | `{"diagnostic":{"column":9,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL230"},"projection":{},"status":1,"verified":false}` |
| N23 | Task capability return refused | `{"diagnostic":{"column":52,"column_encoding":"utf-8-bytes","line":6,"path":"core.py","rule":"PAL320"},"projection":{},"status":1,"verified":false}` |
| N24 | task capability cannot be serialized message | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":5,"path":"core.py","rule":"PAL130"},"projection":{},"status":1,"verified":false}` |
| N25 | builder captured by task callback refused | `{"diagnostic":{"column":9,"column_encoding":"utf-8-bytes","line":6,"path":"core.py","rule":"PAL381"},"projection":{},"status":1,"verified":false}` |
| N26 | Task is excluded from explicit external capability slot | `{"diagnostic":{"column":32,"column_encoding":"utf-8-bytes","line":7,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N27 | explicit external capability/callback mismatch refused | `{"diagnostic":{"column":36,"column_encoding":"utf-8-bytes","line":8,"path":"core.py","rule":"PAL221"},"projection":{},"status":1,"verified":false}` |
| N28 | callback unknown print stays refused with Task and IO | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":4,"path":"core.py","rule":"PAL230"},"projection":{},"status":1,"verified":false}` |
| N29 | async callback never relabeled checked | `{"diagnostic":{"column":1,"column_encoding":"utf-8-bytes","line":3,"path":"core.py","rule":"PAL120"},"projection":{},"status":1,"verified":false}` |
| N30 | generator callback remains stateful cursor | `{"diagnostic":{"column":5,"column_encoding":"utf-8-bytes","line":4,"path":"core.py","rule":"PAL201"},"projection":{},"status":1,"verified":false}` |
| N31 | source task method replacement invalidates actual identity | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":9,"path":"core.py","rule":"PAL240"},"projection":{},"status":1,"verified":false}` |
| N32 | source native thread writer invalidates task evidence | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":9,"path":"core.py","rule":"PAL240"},"projection":{},"status":1,"verified":false}` |
| N33 | analyzed native audit hook registration invalidates task boundary | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":11,"path":"core.py","rule":"PAL240"},"projection":{},"status":1,"verified":false}` |
| N34 | analyzed audit registration alias preserves invalidation | `{"diagnostic":{"column":12,"column_encoding":"utf-8-bytes","line":12,"path":"core.py","rule":"PAL240"},"projection":{},"status":1,"verified":false}` |
| P17 | Task invocation borrow closes only its view | `{"diagnostic":null,"ordinary_stdout":"[6]\n","projection":{"borrow_scopes":1,"effect_bound":["Task"],"required_effects":["Task"]},"status":0,"verified":true}` |

Held command count 122; exact process status vector `[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0]`. Full argv/cwd and named mutation sequence remain in planned-execution.json and the held source drivers.

### runtime

| ID | Authored purpose | Exact expected fields |
| --- | --- | --- |
| R01 | fixed ordinary runtime R01 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"result":[]},"verified":null}` |
| R02 | fixed ordinary runtime R02 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[7,3,5],"result":[6,10,14]},"verified":null}` |
| R03 | fixed ordinary runtime R03 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[],"error":"RuntimeError","reuse_error":"RuntimeError"},"verified":null}` |
| R04 | fixed ordinary runtime R04 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[7,3],"error":"RuntimeError"},"verified":null}` |
| R05 | fixed ordinary runtime R05 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[7,3,5],"result":[6,10,14]},"verified":null}` |
| R06 | fixed ordinary runtime R06 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"empty_zero_cutoff":[]},"verified":null}` |
| R07 | fixed ordinary runtime R07 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[7,5],"error":"ValueError","identical":true},"verified":null}` |
| R08 | fixed ordinary runtime R08 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"nested":["RuntimeError"],"result":[3],"reused_result":[10]},"verified":null}` |
| R09 | fixed ordinary runtime R09 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"other_thread":["RuntimeError"],"owner_result":[6]},"verified":null}` |
| R10 | fixed ordinary runtime R10 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"original_value":18,"result":[18,15],"retained_errors":["RuntimeError","RuntimeError","RuntimeError","RuntimeError"]},"verified":null}` |
| R11 | fixed ordinary runtime R11 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"error":"ValueError","identical":true,"original_value":7,"retained_error":"RuntimeError"},"verified":null}` |
| R12 | fixed ordinary runtime R12 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[],"error":"ValueError"},"verified":null}` |
| R13 | fixed ordinary runtime R13 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"errors":["TypeError","TypeError","TypeError","ValueError"]},"verified":null}` |
| R14 | fixed ordinary runtime R14 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[],"error":"TypeError"},"verified":null}` |
| R15 | fixed ordinary runtime R15 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"calls":[5],"error":"TypeError"},"verified":null}` |
| R16 | fixed ordinary runtime R16 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"callback_error":"TypeError","hook_calls":0,"message_error":"TypeError"},"verified":null}` |
| R17 | fixed ordinary runtime R17 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"errors":["TypeError","ValueError","ValueError","TypeError","ValueError","TypeError","TypeError","ValueError","ValueError","TypeError","ValueError","ValueError"]},"verified":null}` |
| R18 | fixed ordinary runtime R18 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"assign":"AttributeError","construct":"TypeError","delete":"AttributeError","subclass":"TypeError"},"verified":null}` |
| R19 | fixed ordinary runtime R19 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"original":[3,5,7,11,13],"result":[6,10,14,22,26]},"verified":null}` |
| R20 | fixed ordinary runtime R20 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"error":"ValueError","finished":[true,true],"identical_low":true,"started":[0,1]},"verified":null}` |
| R21 | fixed ordinary runtime R21 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"error":"TypeError","started":[0,1]},"verified":null}` |
| R22 | fixed ordinary runtime R22 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"preflight_errors":["ValueError","ValueError","TypeError"]},"verified":null}` |
| R23 | fixed ordinary runtime R23 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"expired_error":"RuntimeError","loan_result":[6],"original_result":[10],"wrong_thread_exit":["RuntimeError"]},"verified":null}` |
| R24 | fixed ordinary runtime R24 | `{"diagnostic":null,"projection":{},"status":0,"stdout_projection":{"ordinary_mutable_capture":[3],"ordinary_result":[4],"static_evidence_from_execution":false},"verified":null}` |

Held command count 4; exact process status vector `[0,0,0,0]`. Full argv/cwd and named mutation sequence remain in planned-execution.json and the held source drivers.

### guard-freshness

| ID | Authored purpose | Exact expected fields |
| --- | --- | --- |
| G01 | guarded stable-message boundary type outcomes | `{"diagnostic":null,"projection":{"debug_bool":"TypeError","exports_bool":"TypeError","exports_nested_mutable":"TypeError","off_unknown_error":"ZeroDivisionError"},"status":0,"verified":true}` |
| G02 | capability parameter remains unguarded invocation obligation | `{"diagnostic":null,"projection":{"build_status":2,"check_status":2,"output":null,"rule":"PAL001","source_diagnostics":[],"source_status":2},"status":2,"verified":false}` |
| F01 | warm callback source change invalidates affected names only | `{"diagnostic":null,"projection":{"changed_result":"[9,15]","changed_status":0,"cold_status":0,"restored_status":0,"unrelated_semantics_equal":true,"warm_status":0},"status":0,"verified":true}` |
| F02 | policy Task denial invalidates source evidence | `{"diagnostic":null,"projection":{"after":1,"artifact_preserved":true,"before":0,"restored":0,"rule":"PAL382"},"status":1,"verified":false}` |
| F03 | callback dependency becomes mutable; no source certificate reuse | `{"diagnostic":null,"projection":{"before":0,"changed":1,"restored":0,"rule":"PAL240"},"status":1,"verified":false}` |
| F04 | installed task implementation change invalidates cache | `{"diagnostic":null,"projection":{"before":0,"cache_reused_changed":false,"changed":0,"identity_changed":true,"restored":0},"status":0,"verified":true}` |
| F06 | audit-hook registration alias invalidates affected task cache | `{"diagnostic":null,"projection":{"after":1,"before":0,"restored":0,"rule":"PAL240","unrelated_semantics_equal":true},"status":1,"verified":false}` |
| E01 | approved external callback retains trust and IO plus Task union | `{"diagnostic":null,"projection":{"admission":"approved","effect_bound":["IO","Task"],"external_effects":["IO"],"external_identity":"pyalamode.integrations.base64_encode","required_effects":["IO","Task"],"result":["YQ==","Yg=="]},"status":0,"verified":true}` |
| E02 | consumer external denial refuses otherwise current task export | `{"diagnostic":null,"projection":{"complete":true,"exports":[],"input_status":0,"rule":"PAL371","source_status":1,"upstream":"PAL350","verified":false},"status":1,"verified":false}` |
| F05 | source callback actual-callee replacement propagates refusal | `{"diagnostic":null,"projection":{"after":1,"before":0,"restored":0,"rule":"PAL221"},"status":1,"verified":false}` |

Held command count 49; exact process status vector `[0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1]`. Full argv/cwd and named mutation sequence remain in planned-execution.json and the held source drivers.

### distribution-history

| ID | Authored purpose | Exact expected fields |
| --- | --- | --- |
| D01 | fresh current wheel3 ordinary import and task contract | `{"diagnostic":null,"projection":{"complete":true,"foundation":26,"guards":["off","exports","debug"],"input_status":0,"ordinary_result":[6,10,14],"schema":3,"source_status":0,"verified":true},"status":0,"verified":true}` |
| D02 | consumer tasks denial remains source refusal all guard modes | `{"diagnostic":null,"projection":{"complete":true,"exports":[],"input_status":0,"rule":"PAL371","source_status":1,"upstream":"PAL382","verified":false},"status":1,"verified":false}` |
| D03 | malformed consumer tasks policy is tooling | `{"diagnostic":null,"projection":{"output":null,"rule":"PAL001"},"status":2,"verified":false}` |
| D04 | genuine M12 wheel2 and M11 wheel1 valid incompatible | `{"diagnostic":null,"projection":{"complete":true,"exports":[],"input_status":1,"rule":"PAL370","source_status":null,"verified":false},"status":1,"verified":false}` |
| D05 | coherent checksum unknown task operation fails closed | `{"diagnostic":null,"projection":{"complete":false,"exports":[],"input_status":2,"rule":"PAL001","source_status":null},"status":2,"verified":false}` |
| D06 | coherent checksum forged task lifetime/order fails closed | `{"diagnostic":null,"projection":{"complete":false,"exports":[],"input_status":2,"rule":"PAL001","source_status":null},"status":2,"verified":false}` |
| D07 | hybrid current wheel old24 inventory fails closed | `{"diagnostic":null,"projection":{"complete":false,"exports":[],"input_status":2,"rule":"PAL001","source_status":null},"status":2,"verified":false}` |
| D08 | consumer source writer remains actual source refusal | `{"diagnostic":null,"projection":{"complete":true,"exports":[],"input_status":0,"rule":"PAL371","source_status":1,"upstream":"PAL240"},"status":1,"verified":false}` |
| D09 | installed authored task source tamper fails closed | `{"diagnostic":null,"projection":{"complete":true,"exports":[],"input_status":1,"rule":"PAL370","source_status":null},"status":1,"verified":false}` |
| D10 | unused unavailable dependency cannot invent owned debt | `{"diagnostic":null,"projection":{"baseline_write_status":0,"build_status":1,"output":null,"owned_findings":0,"written_verified":false},"status":1,"verified":false}` |
| H01 | genuine M12schema3/product24 debt history retained | `{"diagnostic":null,"projection":{"current_foundation":26,"current_schema":4,"historical_foundation":24,"historical_schema":3,"history_ids_unchanged":true,"raw_unchanged":true},"status":1,"verified":false}` |
| H02 | genuine M11schema2 and M10schema1 retain exact lineage | `{"diagnostic":null,"projection":{"current_schema":4,"historical_foundations":[22,19],"historical_schemas":[2,1],"history_ids_unchanged":true,"raw_unchanged":true},"status":1,"verified":false}` |
| H03 | tasks enablement and expanded Task are independent gates | `{"diagnostic":null,"projection":{"baseline_command":0,"baseline_source":1,"baseline_write":0,"current_policy":0,"current_schema":4,"current_source":0,"historical_policy":1,"reason":"tasks-enabled","rules":["PAL367","PAL363"]},"status":1,"verified":false}` |
| H04 | counterfeit old provenance is tooling and never durable debt | `{"diagnostic":null,"projection":{"hybrid_inventory":2,"rule":"PAL001","saved":false,"unknown_labels":2,"unknown_task_row_in_old":2},"status":2,"verified":false}` |
| H05 | current malformed live writer callback fails closed | `{"diagnostic":null,"projection":{"callback_calls":1,"original_state_unchanged":true,"saved":false,"writer_error":"MigrationError"},"status":0,"verified":true}` |
| H06 | current Task source debt saved without certification | `{"diagnostic":null,"projection":{"baseline_command":0,"baseline_source":1,"baseline_write":0,"build_status":1,"output":null,"report_command":1,"report_write":0,"written_verified":false},"status":1,"verified":false}` |

Held command count 83; exact process status vector `[0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,0,0,0,0,0,0,0,0,1,1,2,2,0,0,0,0,0,0,0,0,1,1,2,2,0,0,0,0,1,1,0,0,0,0,1,1,2,2,2,2,2,2,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,2,2,2,2,2,2,0,1,1,0,0]`. Full argv/cwd and named mutation sequence remain in planned-execution.json and the held source drivers.

## Published authored source literals

These are the exact UTF-8/newline source and policies for all51 static cases. The outside cases.json additionally fixes the stock call expressions and their expected bytes, without importing these sources.

<details><summary>P01 — empty controlled map</summary>

`P01/core.py` SHA256 `ce3d7c138ed7cfe4a3f8f8dbc9549d4653f2833107a7b0021e0cd2503bc27313`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`P01/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P02 — permuted schedule retains input result order</summary>

`P02/core.py` SHA256 `ce3d7c138ed7cfe4a3f8f8dbc9549d4653f2833107a7b0021e0cd2503bc27313`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`P02/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P03 — recursive stable message and result data</summary>

`P03/core.py` SHA256 `64e595dd4947aff4583852a75e8115e0e1f236e6251ebe94e7bcbd87636e92ef`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:tuple[int,Vector[int]])->tuple[Vector[int],int]:
    return (x[1].appended(x[0]),x[0]+1)
@effects(Task)
def make(tasks:TaskCapability,values:Vector[tuple[int,Vector[int]]])->Vector[tuple[Vector[int],int]]:
    return task_map(tasks,cb,values)
```

`P03/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P04 — nested checked callback stable scalar and Vector captures</summary>

`P04/core.py` SHA256 `17bbf200de9f630fcab9975ebf4a4e0cea84c4fcd2856f38ff05da9734914b2f`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int],offset:int,extra:Vector[int])->Vector[int]:
    def cb(x:int)->int:
        return x+offset+extra[0]
    return task_map(tasks,cb,values)
```

`P04/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P05 — checked callback alias retains actual target</summary>

`P05/core.py` SHA256 `8616f5b00e5b0b71de95a056d01bb176ff3b06807d5210ec73857c9d04c1b414`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    alias=cb
    return task_map(tasks,alias,values)
```

`P05/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P06 — conditional checked alternatives retain complete target union</summary>

`P06/core.py` SHA256 `def33a2f7bddc0b908f916d8668ba9965813abbc696647500f5d96c9b2ec90e1`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@fun
def other(x:int)->int:
    return x+1
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int],choose:bool)->Vector[int]:
    chosen=cb if choose else other
    return task_map(tasks,chosen,values)
```

`P06/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P07 — returned checked closure specializes stable capture evidence</summary>

`P07/core.py` SHA256 `61cf9eed1c6c4305e2a3098e281dc16673cc99f7495cd0f8da1df0d98c89bbcc`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from typing import Callable
@fun
def factory(offset:int)->Callable[[int],int]:
    def cb(x:int)->int:
        return x+offset
    return cb
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int],offset:int)->Vector[int]:
    return task_map(tasks,factory(offset),values)
```

`P07/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P08 — positional-only fixed callback</summary>

`P08/core.py` SHA256 `11b10731eaa9189ad35d7f26a6ac0ea377ace09b47c77db6b2dca71caa55f2c7`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int,/)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`P08/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P09 — declaration-only callback effect is never erased by fake scheduling</summary>

`P09/core.py` SHA256 `e37c98239907b1aa74d44e9bce64cd9e814ce70768dea7ef32dbf58d84a13eb1`

```python
from pyalamode import Clock,fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@effects(Clock)
def cb(x:int)->int:
    return x*2
@effects(Task,Clock)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`P09/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P10 — callback failure handler retains Task and removes handled category</summary>

`P10/core.py` SHA256 `b70bcdedeb876bc185f67b242e899ee9d6dfd82dbc3d75e2075e9c1527893913`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return 12//x
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    try:
        return task_map(tasks,cb,values)
    except ZeroDivisionError:
        return Vector[int].of()
```

`P10/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P11 — explicit Clock same-thread invocation borrow</summary>

`P11/core.py` SHA256 `7baac7f3ad46cce8c4c73d1e56c0389facc531081b44f3064fbaf84ffa11a4ea`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import Clock,ClockCapability,recorded_clock
@effects(Clock)
def cb(cap:ClockCapability,x:int)->int:
    return cap.now_ns()+x
@effects(Task,Clock)
def make(tasks:TaskCapability,cap:ClockCapability,values:Vector[int])->Vector[int]:
    return task_map_with(tasks,cap,cb,values)
```

`P11/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P12 — explicit State same-thread invocation borrow</summary>

`P12/core.py` SHA256 `5bd7c3c234e30023b3997c3e901fd80dc909e0b6e70f3802eb094a3a9e961eea`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import State,StateCapability,state
@effects(State)
def cb(cap:StateCapability,x:int)->int:
    value=cap.get()
    cap.set(value+x)
    return value+x
@effects(Task,State)
def make(tasks:TaskCapability,cap:StateCapability,values:Vector[int])->Vector[int]:
    return task_map_with(tasks,cap,cb,values)
```

`P12/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P13 — explicit IO same-thread invocation borrow</summary>

`P13/core.py` SHA256 `e08dd33a9e8f0cdf5380595650e51942cc7b4f938444550c98622e0d5af72596`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import IO,IOCapability,recorded_io
@effects(IO)
def cb(cap:IOCapability,x:str)->str:
    return cap.read_text("x")+x
@effects(Task,IO)
def make(tasks:TaskCapability,cap:IOCapability,values:Vector[str])->Vector[str]:
    return task_map_with(tasks,cap,cb,values)
```

`P13/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P14 — explicit Random same-thread invocation borrow</summary>

`P14/core.py` SHA256 `94a90c170536683a40cb40d9658ef88d220d9f8b7b981ec4ebd51d41df182d51`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import Random,RandomCapability,recorded_random
@effects(Random)
def cb(cap:RandomCapability,x:int)->int:
    return cap.below(10)+x
@effects(Task,Random)
def make(tasks:TaskCapability,cap:RandomCapability,values:Vector[int])->Vector[int]:
    return task_map_with(tasks,cap,cb,values)
```

`P14/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P15 — explicit Environment same-thread invocation borrow</summary>

`P15/core.py` SHA256 `e4053493deae25d5f6f099fd66b1716c42b07deace989e055282ef76b627927e`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import Environment,EnvironmentCapability,recorded_environment
@effects(Environment)
def cb(cap:EnvironmentCapability,x:str)->str:
    return cap.get("NAME","")+x
@effects(Task,Environment)
def make(tasks:TaskCapability,cap:EnvironmentCapability,values:Vector[str])->Vector[str]:
    return task_map_with(tasks,cap,cb,values)
```

`P15/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P16 — nested incoming borrow preserves lifetime and external effect</summary>

`P16/core.py` SHA256 `460f9989adec4aa0536ef88c9fec453e23acdb45366653ee72c6696c260417b0`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import borrow,Clock,ClockCapability,recorded_clock
@effects(Clock)
def cb(cap:ClockCapability,x:int)->int:
    return cap.now_ns()+x
@effects(Task,Clock)
def make(tasks:TaskCapability,cap:ClockCapability,values:Vector[int])->Vector[int]:
    with borrow(cap) as loan:
        return task_map_with(tasks,loan,cb,values)
```

`P16/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N01 — tasks default off</summary>

`N01/core.py` SHA256 `ce3d7c138ed7cfe4a3f8f8dbc9549d4653f2833107a7b0021e0cd2503bc27313`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N01/pyproject.toml` SHA256 `835b258e67c0b07b897da969db6948a71461257872ee2700382907f147693046`

```toml
[tool.pyalamode]
```

</details>

<details><summary>N02 — tasks explicitly false</summary>

`N02/core.py` SHA256 `ce3d7c138ed7cfe4a3f8f8dbc9549d4653f2833107a7b0021e0cd2503bc27313`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N02/pyproject.toml` SHA256 `1b871e9889cc3e61b1f70e301737b926996e480b088295d56738434af7007f39`

```toml
[tool.pyalamode]
tasks = false
```

</details>

<details><summary>N03 — malformed string policy is tooling</summary>

`N03/core.py` SHA256 `ce3d7c138ed7cfe4a3f8f8dbc9549d4653f2833107a7b0021e0cd2503bc27313`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N03/pyproject.toml` SHA256 `610c53186a0f1772c370973124d9b0cc365d96d4cc04d031a5d31ff510843be2`

```toml
[tool.pyalamode]
tasks = "true"
```

</details>

<details><summary>N04 — pure parent cannot erase Task</summary>

`N04/core.py` SHA256 `b66ba310fcbc8eb6d2bd02c097e54a5214880ae01ade51314cb5af7e777e4b87`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@fun
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N04/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N05 — undeclared callback effect union refused</summary>

`N05/core.py` SHA256 `43dc1688ba59f61f9c32240f287a0702b2d1ee783af911891e3544fc1030cb94`

```python
from pyalamode import Clock,fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@effects(Clock)
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N05/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N06 — ordinary unknown callback has no checked evidence</summary>

`N06/core.py` SHA256 `e7f17b9b6c2f2f20045ed8d6ba7b3ad477e072212e853e9e808488d6c332dd73`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N06/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N07 — mutable global capture refused</summary>

`N07/core.py` SHA256 `92f787be2d3e2b18dc5c518762774b704d8d72b2abaf0607da9460c2ec8a11c7`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
BAD=[1]
@fun
def cb(x:int)->int:
    return x+BAD[0]
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N07/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N08 — changing scalar dependency capture refused</summary>

`N08/core.py` SHA256 `2d21da99960f1b51357c5112bf7bf1ce8c92735008e129132f595ea7ee340316`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
OFFSET=1
@fun
def cb(x:int)->int:
    return x+OFFSET
OFFSET=2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N08/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N09 — external capability capture cannot cross task</summary>

`N09/core.py` SHA256 `38ed5833a4622ffd11c5ec77731078b795e8940e16969ec77a7c7703a1eb3109`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import Clock,ClockCapability
@effects(Task,Clock)
def make(tasks:TaskCapability,cap:ClockCapability,values:Vector[int])->Vector[int]:
    @effects(Clock)
    def cb(x:int)->int:
        return x+cap.now_ns()
    return task_map(tasks,cb,values)
```

`N09/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N10 — task capability capture cannot cross task</summary>

`N10/core.py` SHA256 `994a421859fca22773dedf886eb5decd29b58b4547fe1d38fcdde9237d3fb032`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    @effects(Task)
    def cb(x:int)->int:
        return task_map(tasks,cb,Vector.of(x))[0]
    return task_map(tasks,cb,values)
```

`N10/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N11 — callback input type mismatch</summary>

`N11/core.py` SHA256 `178d1e7aa560bb8e58e2b7900cc29f3f6e0d7f32c11c600e95d568484d77aba3`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:bool)->int:
    return 1
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N11/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N12 — callback extra keyword-only/default parameter refused</summary>

`N12/core.py` SHA256 `6a5bb070f2b10f6f340db4d347e75dd0cc34a9f135204cfad82e262fa255024b`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int,*,extra:int=0)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N12/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N13 — callback wrong data result schema refused</summary>

`N13/core.py` SHA256 `3776e316400e9e624f82f5a310bd503784a0ce577ddb46e0f3222066ab86eea2`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->bool:
    return True
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N13/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N14 — mutable callback annotation refused</summary>

`N14/core.py` SHA256 `f9e084fc620c2c0f0e91df0c07d6d486a33f8a2187e436a71872d00be2b39a77`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:list[int])->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N14/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N15 — mutable task messages refused</summary>

`N15/core.py` SHA256 `7b438bf73d893c4289fce6ef3f1aa96d53b9d8a54b0de783b2e34b49488476e7`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,[1])
```

`N15/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N16 — tuple is not exact Vector messages</summary>

`N16/core.py` SHA256 `d1a01125e877f61ddec1c0b7fb53ca84c878efe8b2e9670f24069730fd76709a`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,(1,))
```

`N16/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N17 — task keyword signature refused</summary>

`N17/core.py` SHA256 `3c6bbc16767c352908f181d39c0c2c4ef67595857ba0c7b9363eb538281cd710`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,messages=values)
```

`N17/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N18 — task result cannot be silently ignored</summary>

`N18/core.py` SHA256 `7abc9d5c624fed08339b0836c9f047c0344ae4ed07cdc5266cb027a4b5e49287`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    task_map(tasks,cb,values)
    return values
```

`N18/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N19 — unknown Task operation remains refused despite declaration</summary>

`N19/core.py` SHA256 `5037559ccce376d6fef06efc844f36c5da0347e53b58cd920099f6d6aa0e24f1`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    tasks.unknown()
    return values
```

`N19/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N20 — Task capability alias refused</summary>

`N20/core.py` SHA256 `a97ab18588e1dd815475a4ddc0d6a13757e707c7ef89b4c091b316cd5c306629`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    alias=tasks
    return task_map(alias,cb,values)
```

`N20/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N21 — Task capability cannot be stable tuple data</summary>

`N21/core.py` SHA256 `e11c4d6ae7c4d76dc6e07dfac6c226556c0a7983d397ad83a1a4bb08df155be5`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    retained=(tasks,)
    return values
```

`N21/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N22 — provider construction in checked body remains ordinary setup</summary>

`N22/core.py` SHA256 `0ae21db3bcbb6159af436bc8b0ea05cedf54dbed312c1c311f9d314616f787a3`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    cap=controlled_tasks((0,))
    return task_map(cap,cb,values)
```

`N22/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N23 — Task capability return refused</summary>

`N23/core.py` SHA256 `aefba22804e52360cc7f8e4fb032e48ea6eb389c19256fdf4ecd0bcf7e78f5ff`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->TaskCapability:
    return tasks
```

`N23/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N24 — task capability cannot be serialized message</summary>

`N24/core.py` SHA256 `85409e51bcfbbb630d90f38c4d1ee32bea7edd4b0b8aeb5add5c2e59da5ee0cf`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import record
@record
class Bad:
    cap:TaskCapability
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N24/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N25 — builder captured by task callback refused</summary>

`N25/core.py` SHA256 `b606306b86546274ef8d71dc9ebb7a9beb86c63247bd7ad2b28a0cf0dd3e06a9`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import VectorBuilder,vector_build
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    def fill(b:VectorBuilder[int])->None:
        def cb(x:int)->int:
            b.append(x)
            return x
        task_map(tasks,cb,values)
    return vector_build(fill)
```

`N25/pyproject.toml` SHA256 `c1d196dc1294eb3065019ed0b0f0b32418b26a17c5f071591321902399bce547`

```toml
[tool.pyalamode]
tasks = true
builders = true
```

</details>

<details><summary>N26 — Task is excluded from explicit external capability slot</summary>

`N26/core.py` SHA256 `faf51b212f9cfdcb1f15a477fa3f35b709e5fb90102829a99d185c6a6b7d0868`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@effects(Task)
def cb(cap:TaskCapability,x:int)->int:
    return x
@effects(Task)
def make(tasks:TaskCapability,other:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map_with(tasks,other,cb,values)
```

`N26/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N27 — explicit external capability/callback mismatch refused</summary>

`N27/core.py` SHA256 `033b0bb832fdb800286fa53482077629721714e4c44188441c7cf927e0ad2031`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
from pyalamode import StateCapability,State,Clock,ClockCapability,recorded_clock
@effects(Clock)
def cb(cap:ClockCapability,x:int)->int:
    return cap.now_ns()+x
@effects(Task,Clock,State)
def make(tasks:TaskCapability,cap:StateCapability,values:Vector[int])->Vector[int]:
    return task_map_with(tasks,cap,cb,values)
```

`N27/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N28 — callback unknown print stays refused with Task and IO</summary>

`N28/core.py` SHA256 `6c857c5c6aeff5682c453a9a5762c3e7dad7fccd55b43fa241673ab925863841`

```python
from pyalamode import IO,fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@effects(IO)
def cb(x:int)->int:
    print(x)
    return x
@effects(Task,IO)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N28/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N29 — async callback never relabeled checked</summary>

`N29/core.py` SHA256 `eb565a70b30db5520ab5a87bcdb4f518a7a16432a68353a268d3af8886bde9e2`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
async def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N29/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N30 — generator callback remains stateful cursor</summary>

`N30/core.py` SHA256 `1d72726f009c4e0cff443353e6b31a8153375c092f756ab3b51c6c85b20d666c`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    yield x
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N30/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N31 — source task method replacement invalidates actual identity</summary>

`N31/core.py` SHA256 `94da70a91b9ed6b29791ba9812f9072e4fd1ae1140bf8e176f4009390cf7263e`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
import pyalamode.tasks as implementation
implementation.task_map=print
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N31/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N32 — source native thread writer invalidates task evidence</summary>

`N32/core.py` SHA256 `8702177475bb10b13a8b3c6f0e616b2addd59441ad6fc13a04ba54f27187c42c`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
import _thread
_thread.start_joinable_thread=print
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N32/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N33 — analyzed native audit hook registration invalidates task boundary</summary>

`N33/core.py` SHA256 `bf20616852284e2569716e932d8127b1c4ba38449f448dd767e4668834d5a7a2`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
import sys
def hook(event,args):
    return None
sys.addaudithook(hook)
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N33/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>N34 — analyzed audit registration alias preserves invalidation</summary>

`N34/core.py` SHA256 `52de8dac6827b6c32fda41824a604751e6808f39f6866d1069b9ce823b26ecee`

```python
from pyalamode import fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
import sys
def hook(event,args):
    return None
register=sys.addaudithook
register(hook)
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    return task_map(tasks,cb,values)
```

`N34/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

<details><summary>P17 — Task invocation borrow closes only its view</summary>

`P17/core.py` SHA256 `e7f38d590d154913e13bef80af934d08322baa58858812eb7d3b944913a30f55`

```python
from pyalamode import borrow,fun, effects, Task, TaskCapability, Vector, task_map, task_map_with, controlled_tasks, live_tasks
@fun
def cb(x:int)->int:
    return x*2
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    with borrow(tasks) as scoped:
        return task_map(scoped,cb,values)
```

`P17/pyproject.toml` SHA256 `27716806856361e4576ab5da64e5a30c512641fd8eca877b66715ba95220838c`

```toml
[tool.pyalamode]
tasks = true
```

</details>

