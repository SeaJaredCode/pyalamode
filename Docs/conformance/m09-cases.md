# M9 independent editor conformance plan and observations

Status: **FINAL FROZEN INDEPENDENT M9 CONFORMANCE PASSED; ROOT ACCEPTANCE RESERVED**. Authority: the complete `SPEC-sol6.1-composite.md`, current public checker/model/project APIs, README, M1–M8 milestone contracts and acceptance matrix, read on 2026-10-09. Prerequisite: root reports independent M1–M8 acceptance at `ec580b0`. Root owns release acceptance, source freezes, Git and scheduling. This reviewer owns only this file; executable probes, fixtures, installed environments and raw records live outside the checkout under `/tmp/pyalamode-m09-review`. No application-source execution is permitted while gathering static editor evidence.

This plan fixes expected behaviors before admission observation. Concrete session/transport requests and complete executable bounded harness text will be appended once the two peer schemas exist and root approves them, before calling the candidate. A bug does not change a fixed expected outcome. Any genuinely new semantic supplement is fixed here before a correction or probe. Main's plan is `Docs/milestones/09-editor.md`; client plan is `Docs/evidence/m09-client.md`.

## Fixed acceptance inventory

| ID | Fixed observation and expectation |
| --- | --- |
| E01 | Same captured compatible source gives identical shared-engine and editor rule, authored range, affected boundary, origin, reason, remediation and first binding. Strict invalid source remains status 1/unverified; audit remains adoption evidence without certification; off cannot publish a strict claim. Empty selection explicitly has zero coverage. |
| E02 | UTF-8 AST byte columns convert to editor UTF-16 units exactly, including BMP non-ASCII identifiers, astral characters before a diagnostic/navigation token, CRLF, final lines without newline and multiline nodes. LSP ranges are zero-based and end-exclusive. Authored command columns are converted according to the published command contract, never confused with byte columns. |
| E03 | Current unsaved document text/version overrides its disk text while open. Increasing versions replace evidence; duplicate/decreasing versions cannot masquerade as current. Save/close/reopen uses its documented source without discarding other open overlays. A failed new revision never retains an old successful claim. |
| E04 | Definition/references/call origins follow resolved source identity, import aliases, lexical captures and actual shadowing. Two same-spelling local functions or parameters in distinct scopes remain distinct. Unsupported dynamic targets get no fabricated destination. URI/source ownership prevents requests outside the workspace or symlink escapes from being read or edited under this workspace's authority. |
| E05 | Participating boundary information/hover includes exact inputs/results, enforcement, behavior, checked/opaque/unchecked source evidence, transitive trust, failures, freshness and selected guard coverage. Effects retain origin paths through direct and higher-order calls. Ordinary setup/unsafe adapter evidence remains separately unchecked. |
| E06 | Rule explanation exposes valid finite remediation and symbol explanation uses the current resolved contract/dependency/effect/trust evidence. Unknown rules/symbols are explicitly unsupported, rather than an invented clean symbol. |
| E07 | At least one useful finite fix preview contains explicit text edits, current document version and preconditions. It leaves bytes unchanged until a user/client elects to apply. It cannot silently add effects, approvals, ignored errors, conversions, an exception handler, marker removal or changed failure behavior. Unsupported fixes return a bounded explanation/no edits. Stale revisions invalidate old previews. |
| E08 | Real selected exports/debug guard failures navigate to the original authored compatible file/boundary and appropriate value path. Nested mutable/type mismatch rejection occurs before body entry; output failure identifies return coverage. Off remains ordinary Python with its existing caller obligations. No certificate/registry service participates in invocation. |
| E09 | Tooling/encoding/syntax/resolution/policy and unsupported-target errors are distinct from a clean editor view. External approval UTC expiry, current policy/source/import-resolution/analyzed writer/product bytes and integration identity changes invalidate subsequent observations even when source text/version is unchanged. No stale success survives a failed refresh. |
| E10 | If stdio JSON-RPC/LSP is chosen, exercise actual Content-Length framing, initialize/initialized/shutdown/exit, notifications, workspace-root handling, Unicode lengths, malformed JSON/headers/params, unknown methods and response/error IDs. Offered cancellation/update semantics must match the published contract; unopened text reads and cross-workspace URIs cannot silently escape ownership. |
| E11 | Run the actual selected editor client against the actual wire server. Record client implementation, interpreter, process arguments, transport and literal requests/responses; a direct engine-only call cannot establish client provenance. Static default/decorator/annotation/import/metadata sentinels must remain absent. |
| E12 | Final current source map covers all product Python files, current M9 tests/examples/client/harness inputs and the root freeze packet, before/after each complete native and actual Linux gate. Run the final complete inherited/current suite once against the frozen source, plus focused bounded probes. Reuse authoritative named M1–M8 corpora for unchanged guarantees; do not reprint or re-execute huge unrelated historic corpora. |

## Fixed literal source fixtures

The complete following texts are part of the expectation, independent of implementation. The executable harness will retain these exact texts and emit their SHA-256. File paths are isolated project-relative files chosen by the harness. CRLF is an explicit byte transformation of U01, not the textual backslash spelling. U01 also runs with the last newline removed.

```python
LITERALS = {
    "U01": "# mode: fun\n\ndef café(値: int) -> int:\n    café = 値\n    café = 2\n    return café\n",
    "U02": "# mode: fun\n\ndef f(値: int) -> int:\n    return (\n        値 +\n        missing(値)\n    )\n",
    "U03": "# mode: fun\n\ndef f(値: int) -> int:\n    pair = ('😀', missing(値))\n    return 値\n",
    "S01": "# mode: fun\n\ndef leaf(value: int) -> int:\n    return value + 1\n\ndef outer(value: int) -> int:\n    def leaf(value: int) -> int:\n        return value + 2\n    return leaf(value)\n\ndef another(leaf: int) -> int:\n    return leaf\n\ndef caller(value: int) -> int:\n    return leaf(value)\n",
    "S02": "# mode: fun\nfrom dependency import leaf as café\n\ndef caller(値: int) -> int:\n    return café(値)\n",
    "S03": "# mode: fun\n\ndef leaf(value: int) -> int:\n    return value + 1\n",
    "C01": "from pyalamode import effects, Clock, ClockCapability\n\n@effects(Clock)\ndef leaf(clock: ClockCapability) -> int:\n    return clock.now_ns()\n\n@effects(Clock)\ndef caller(clock: ClockCapability) -> int:\n    return leaf(clock)\n",
    "T01": "from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n\n@fun\ndef digest(data: bytes) -> bytes:\n    return sha256_digest(data)\n\n@fun\ndef caller(data: bytes) -> bytes:\n    return digest(data)\n",
    "F01": "# mode: fun\nfrom pyalamode import Vector\n\ndef grow(values: Vector[int]) -> Vector[int]:\n    values.appended(1)\n    return values\n",
    "F02": "# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = value + 1\n    return result\n",
    "F03": "# mode: fun\nfrom pyalamode import ClockCapability\n\ndef f(clock: ClockCapability) -> int:\n    return clock.now_ns()\n",
    "G01": "# mode: fun\nfrom pyalamode import Vector, record\n\n@record\nclass Payload:\n    values: Vector[int]\n\ndef echo(payload: Payload) -> Payload:\n    return payload\n",
}
```

Fixed primary outcomes: U01 strict refusal `PAL101` at second `café` binding, first binding line 4; U02/U03 strict refusal `PAL230` at `missing`; S01/S02+S03/C01/G01 strict admission; T01 denied by default `PAL350`, then admitted only under explicit exact current fixture approval; F01 strict `PAL250`, F02 strict `PAL101`, F03 strict effect/capability refusal (its precise complete rule set remains inherited checker evidence). Audit versions of every refused fixture expose findings and no certified contract. No U/F fixture receives fabricated pure source evidence.

Literal zero-based UTF-16 end-exclusive token ranges to assert before invoking the candidate:

| Fixture/token | Range | Original AST UTF-8 byte range where applicable |
| --- | --- | --- |
| U01 second café | `(4,4)–(4,8)` | `(4,4)–(4,9)` |
| U01 first café binding | `(3,4)–(3,8)` | `(3,4)–(3,9)` |
| U01 parameter 値 | `(2,9)–(2,10)` | `(2,10)–(2,13)` |
| U02 missing | `(5,8)–(5,15)` | same |
| U03 missing following astral string | `(3,18)–(3,25)` | `(3,20)–(3,27)` |
| S01 outer's nested leaf call | `(8,11)–(8,15)` | same |
| S01 top-level leaf call | `(14,11)–(14,15)` | same |
| S02 café call | `(4,11)–(4,15)` | `(4,11)–(4,16)` |
| S03 leaf declaration | `(2,4)–(2,8)` | same |
| F01 discarded update expression | `(4,4)–(4,22)` | same |

Diagnostic ranges may cover the full offending AST expression when the peer contract says so; the token ranges above separately fix location conversion/navigation expectations. Exact full diagnostic ranges and wire payloads will be supplemented from the declared schema before observation, without changing the source/token expectations.

## Fixed state, freshness and malicious-input sequences

1. Open clean S03 at version 1; replace its unsaved body with `return missing(value)` at version 2; query diagnostics/contract; send duplicate version 2 and stale version 1; restore exact clean S03 at version 3; close and query documented disk state. Current failure must supersede successful evidence and old versions must never supersede 3.
2. Open S02 and dependency S03; modify the dependency overlay to `return missing(value)`; inspect both caller/dependency; restore it; add an analyzed ordinary writer replacing leaf; remove writer; change import resolution by adding a same-name package; remove it. Current loaded graph/source identities and resulting contract/diagnostics must track each input.
3. For T01, use a fixture owner/rationale/provenance and exact current operation/backend digests, no production approval. Observe current success, then actual UTC expiry with unchanged text/policy, stale policy, malformed policy and denied policy. Each subsequent query must refresh classification. Change product bytes only in an isolated copied installed package, never checkout source.
4. Request previews for F01/F02/F03/T01 and syntax-invalid text; preserve disk and overlays before/after; inspect every edit for forbidden policy/trust/effect/ignore/handler/conversion changes. If F01 offers a finite bind-new-value preview, assert remaining blockers and preview text visibly retain old return semantics unless the user explicitly chooses a changed program. Request the old preview after a version edit and expect explicit staleness.
5. Read/query `file:///outside.py`, `file://remotehost/path.py`, encoded traversal, unsupported URI schemes, symlink escape, malformed percent encoding, bogus ranges/version fields, paths to directories and non-UTF8 bytes. No arbitrary outside content/writes or clean certified view may result.
6. Real wire: split a header/body across writes; concatenate two framed requests; include astral source text whose UTF-8 byte count differs from code points; send unknown method, missing params, bad numeric positions/versions, invalid JSON and bad Content-Length; exercise every advertised lifecycle/cancellation behavior. Responses preserve request IDs, remain framed and errors do not contaminate later valid requests according to the fixed peer transport policy.
7. Sentinel sources use ordinary top-level filesystem writes plus annotated/default/decorator expressions and local import metadata side effects. Snapshot document/client/CLI operations must not create any sentinel. Ordinary artifact execution is a separate explicit stage and cannot be confused with the static no-execution stage.

## Evidence and unresolved gates

## Fixed safe-preview semantic supplement, before implementation

The client/helper proposal mentions a straight-line SSA rename and ignored-update fresh binding. This supplement fixes the additional eligibility tests before candidate observation. A safe preview may be intentionally reviewable instead of automatic, but its remaining blockers and semantic implications must be visible. For SSA the pre-repair ordinary Python reference result and a successfully checked repaired artifact must agree for admitted test inputs. Preserving text spelling alone does not establish this.

```python
PREVIEW_LITERALS = {
    "P01": "# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n",
    "P02": "# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    def captured() -> int:\n        return result\n    result = value + 1\n    return captured()\n",
    "P03": "# mode: fun\n\ndef f(value: int, choose: bool) -> int:\n    result = value\n    if choose:\n        result = result + 1\n    return result\n",
    "P04": "# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    def inner(result: int) -> int:\n        return result + 2\n    return inner(result)\n",
    "P05": "# mode: fun\n\ndef f(value: int) -> int:\n    result_new = value + 9\n    result = value\n    result = result + 1\n    return result + result_new\n",
    "P06": "# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    result = result + 2\n    return result\n",
    "P07": "# mode: fun\n\ndef f(value: int) -> int:\n    result_2 = value + 9\n    result = value\n    result = result + 1\n    return result + result_2\n",
}
```

P01 may preview a finite new target/later-use name, keeping its RHS's old `result` reference; ordinary expected result is `value+1`. P02/P03 require no edits because capture/control-flow rewriting is outside the proposed straight-line eligibility. P04 may refuse conservatively; if offered, only the actual later outer reference changes, never inner parameter/body references; expected result is `value+3`. P05 requires a genuinely fresh name with no collision and expected result `2*value+10`. P06 may refuse conservatively; if offered it must rename all three logical versions consistently, preserve expected result `value+3` and visibly report any remaining `PAL101`. None may remove opt-in, add trust/effects/ignores or alter exception/failure behavior. F01's fresh binding must not silently replace `return values` with `return new_values`; the original ordinary return remains the original Vector. A preview that binds and leaves the old return supplies a clear remaining semantic-choice explanation. No preview applies itself.

P07 supplements P05 before its first observation with an explicit `result_2` collision matching the concrete proposed SSA suffix. Its required finite preview must choose a fresh different name and preserve `2*value+10`; P05's original literal and expected result remain unchanged.

## Fixed producer-coordinate supplement, before implementation

Root identified the inherited producer distinction before implementation: AST offsets are UTF-8 bytes, tokenizer offsets are code points, and current syntax/tooling diagnostics can omit the precise syntax offset entirely. Legacy command starts must be retained; an absent span cannot be treated as an AST byte span. These additional literal sources and expectations are fixed before observation:

```python
COORDINATE_LITERALS = {
    "U04": "é = 1; # mode: fun\n",
    "U05": "'😀'; # mode: fun\n",
    "U06": "def café(値: int) -> int:\n    return 値 +\n",
    "U07": "from pyalamode import fun\r\r@fun\rdef café(値: int) -> int:\r    café = 値\r    café = 2\r    return café\r",
    "U08": "# mode: fun\n\ndef f(値: int) -> int:\n    pair = ('😀\u2028', missing(値))\n    return 値\n",
}
```

U04 PAL121 authored line 1, legacy code-point column 8, LSP comment start `(0,7)`; U05 PAL121 authored line 1, legacy code-point column 6, LSP comment start `(0,6)`. U06 remains tooling status 2/PAL001 on line 2 with its preserved legacy column 1 and explicit imprecise fallback. If the candidate adds genuine syntax span metadata without changing the old start, its newly precise location must be separately producer-correct; it cannot quietly convert a code-point column as bytes.

U07 uses accepted decorated compatible Python with lone CR physical newlines: `PAL101` at `(5,4)–(5,12)`, first binding on zero-based line4. U08 places U+2028 inside a string on one physical source line: `PAL230` at `(3,19)–(3,29)`. Source-only inspection identified the lone-CR mapping concern before any candidate calls; Python physical LF/CRLF/CR line semantics and Unicode string separators remain distinct.

## Fixed protocol request supplement, before observation

The read main schema proposes JSON-RPC2/LSP3.17 on stdin/stdout, exact configured interpreter argv, 8MiB maximum body and serialized analysis. The following request inventory is fixed before invoking any candidate. The harness substitutes only current fixture roots/URIs/snapshots/versions and serializes UTF-8 `ensure_ascii=False`; Content-Length equals those exact bytes. All ordinary requests have `jsonrpc:"2.0"` and unique exact integer IDs; notifications omit IDs.

| Request | Literal method/params and expected result |
| --- | --- |
| W01 | `initialize`, `{rootUri:root.as_uri(),capabilities:{}}`; advertised `positionEncoding:"utf-16"`, full sync change 1, named server and the actual claimed providers. |
| W02 | `initialized`, `{}`; no response. `pyalamode/project`, `{}`; schema1, current snapshot/inputs/report/regions/diagnostics, status matching CLI on disk. |
| W03 | `textDocument/didOpen`, `{textDocument:{uri,languageId:"python",version:1,text:S03}}`; versioned diagnostics. `didChange`, `{textDocument:{uri,version:2},contentChanges:[{text:badS03}]}`; current bad overlay. Duplicate2/decreasing1, bool version and incremental change with `range` refuse. |
| W04 | `textDocument/hover|definition|references`, `{textDocument:{uri},position:{line:8,character:12}}` for S01's nested call; definition only nested `outer.leaf`, references only that established identity; top-level call at line14 character12 resolves top-level leaf. Add references context `{includeDeclaration:true|false}` and check the actual supported declaration inclusion. |
| W05 | `textDocument/documentSymbol`, `{textDocument:{uri}}`; participating authored names/ranges only, nested scopes distinct. Parameter/shadow reference query on S01 line11 character12 returns no fabricated definition. |
| W06 | `pyalamode/explain`, `{symbol:"PAL101"}` and `{symbol:"core:caller"}`; rule and current exact symbol evidence. Main clarified the `module:qualified.function` selector before first candidate calls; unqualified authored `caller` and unknown strings stay explicit unsupported. |
| W07 | `textDocument/codeAction`, `{textDocument:{uri},range:{start:{line:4,character:0},end:{line:4,character:30}},context:{diagnostics:[]}}`; only explicit Preview Commands with exact preview params, never source writes/workspace applyEdit. |
| W08 | `pyalamode/preview`, `{uri,version:1,snapshot:currentSnapshot,diagnosticIndex:matchingIndex}`; full before/after/diff/edits/status/remainingDiagnostics/limits. Version/snapshot/index mismatch errors. Fixed P/F semantic inventory governs eligibility. |
| W09 | `pyalamode/guardLocation`, `{artifactUri,publicBoundary:"pyalamode_exports.core:echo",phase:"argument",name:"payload"}`; exact original declaration location on current real exports/debug evidence. Return/local phases require real published coverage. Tampered/current-input-mismatched/unguarded evidence errors. |
| W10 | `textDocument/didSave`, `{textDocument:{uri}}`, `didClose`, `{textDocument:{uri}}`; documented current overlay/disk transitions and clear diagnostics for removed findings. Other open dependency overlay is preserved. |
| W11 | Unknown request method; malformed top-level JSON type; wrong/missing params; negative/bool/fractional/out-of-bounds positions; unauthorized/remote/invalid URI; root mismatch; null/nonboolean audit; bogus diagnostic index/snapshot. Each errors explicitly, preserving request ID where valid, without reading outside content or retaining a clean successful claim. Boolean audit false/true remains valid. |
| W12 | Valid request split across 3 writes; two frames concatenated; astral source body; malformed complete JSON then valid project request. Recoverable complete-frame errors leave later requests usable. Oversize, negative/nonnumeric/duplicate Content-Length, malformed headers and truncated EOF follow the documented bounded rejection/end behavior. Stdout is framed protocol only. |
| W13 | `$/cancelRequest`, `{id:priorId}` notification; no fabricated cancellation promise/response. `shutdown`, `{}`; then work request fails; `exit` notification ends process. Before initialize and duplicate initialize obey published lifecycle errors. |

The direct API comparison uses exactly `project.check_snapshot(paths=None,root=fixtureRoot,audit=False,target=TARGET,cache=True,overlays={str(existingPath):{"text":text,"version":1}})`. Expected captured `sources`, `inputs` origins/versions/disk SHA, current freshness and SHA snapshot are independent of UI payload formatting. Project-wide ordinary writer discovery and current policy/approval inputs remain essential. Main's finite navigation deliberately excludes parameter/capture-variable destinations; this does not weaken the no-fabricated-resolution expectation in E04.

At plan publication, final frozen conformance was **UNVERIFIED**. The final frozen observations below supersede that pending state. Main/client schemas and root approval were obtained before candidate calls; historical interim observations are recorded below. Final records retain complete bounded new harness/fixture text, raw digests/projections, actual native/Linux interpreter/platform and installed source inventories, suite statuses, transport/client provenance and same source maps before/after. Historic M1–M8 records remain named authority for unchanged admission/runtime contracts. A24's translated-source portion remains M14's gate.

Human editor repair/usability benefit is **UNMEASURED**, with zero participants/attempts. Proposed unperformed task protocol: recruit new Python users; provide the fixed rebinding, ignored update and unknown/effect-call fixtures; measure correct repair, incorrect semantic/trust/effect changes, attempts, time and interpretation of caller obligations; publish the denominator and failures. Automated protocol conformance cannot establish human benefit.

## Pre-read ownership supplement, fixed before candidate calls

Root source review identified that status2 after reading outside content is insufficient. The independent supplement fixes actual selected-source, transitive-module, package-directory and policy symlink refusals before reads. A CPython audit hook records every attempted open resolved to the isolated outside fixture. Each direct full-project snapshot must return tooling/unverified, expose no outside source and make zero outside-content opens. This preserves E04 and the ordinary CLI contract. No candidate was invoked before this supplement.

## File-claim and input-race supplement, fixed before candidate calls

Root identified aggregate-only staleness as insufficient. Loaded-product and captured source/policy/overlay-disk races must leave every serialized file claim unverified as well as the aggregate and contracts. The deterministic race controller changes only isolated authored fixture bytes after the real SourceGraph analysis and before snapshot publication; it executes no application hook. This preserves E03/E09.

## Selected-guard evidence supplement, fixed before candidate calls

Root source review identified self-declared generated coverage with an empty byte inventory as insufficient. Fixed real artifact tamper variants now include empty inventory, missing selected source, missing selected facade and parameter coverage changed from the actual current guard plan. Each must refuse guard navigation; restoring complete original evidence restores the original contract. This preserves E08/E09 without adding M11 consumer certification.

## Exact malformed-envelope supplement, fixed before candidate calls

Raw UTF-8 bodies `{}`, `[]`, boolean/object request IDs, and otherwise shaped requests containing literal `NaN` or `Infinity` are invalid JSON-RPC/JSON. They require a framed error with null ID, without being relabeled valid notifications or reflecting invalid IDs. Each complete-frame rejection is followed by a valid project request that must remain usable. Proper notifications still receive no response. Root identified this producer distinction during source review; expectations are fixed before correction observation.

## External explanation ownership supplement, fixed before candidate calls

The outside-policy audit also covers actual `EditorSession.handle("pyalamode/explain",{"symbol":"integrations"})` and `sha256_digest` after initialize. Both reuse the refused scoped snapshot, remain status2, and make zero outside-content opens. A second unscoped policy read during explanation cannot bypass the first correct ownership refusal. The ordinary CLI policy contract remains unchanged.

## Reviewer-only extraction repair before candidate invocation

The first controller launch stopped before importing/calling the product: naive Markdown fence extraction encountered the controller's own embedded fence spelling and raised SyntaxError. Fence extraction now matches line-anchored Markdown blocks. Literal texts and all expected outcomes are unchanged; this is a controller repair, not candidate evidence.

## Historical first interim feedback and reviewer fixture repair

The first actual mutable-source probe made 1,951 parent checks. Coordinate/engine agreement (including CR/Unicode separators), resolved navigation, finite previews, malformed wire/ownership, static nonexecution, isolated loaded-product restart, captured-input races and lifecycle groups passed. Editor/client source changed during this run, so its source-map failure is expected historical feedback, not final evidence. Two state/expiry assertions are being rerun on settled product bytes. The guard fixture forged an uninitialized record and correctly failed before body entry with malformed outer storage; it did not reach the intended nested member. The fixture now constructs a valid record and only replaces its nested Vector with wrong exact bool content. The fixed nested-path/before-body expectation remains unchanged. Every process transcript is now saved even if a group raises. No candidate expectation was weakened. Raw first packet: `/tmp/pyalamode-m09-review/interim-native-probe.json`.

## Concrete settled resolution finding and fixed correction supplement

The settled interim packet passed twelve groups and unchanged maps with 2,086 parent checks. Its one remaining failure is concrete: adding `dependency/__init__.py` alongside selected/open `dependency.py` discovers both but S02's call/definition still resolves to dependency.py. Wire request11 returns that wrong module destination. Actual Python and the inherited package-before-module contract require the initializer. Main/root were notified; the fixed expectation is preserved. Before correction observation, the same layout is extended with exact initializer text `# mode: fun\n\ndef leaf(value: int) -> str:\n    return "package"\n`; S02's declared int return must fail PAL211 in alias.py and leave its file unverified, rather than using the same-spelling module's int contract. This tests admission implications in addition to navigation.

The independent actual exported JavaScript client meanwhile passed 16 checks over 40 recorded wire messages in a native real process, preserving the literal `.venv/bin/python` argv; its interim packet is `/tmp/pyalamode-m09-review/interim-client.json`. This is transport provenance, not human repair or final frozen evidence.

## Fixed canonical nominal-schema supplement, before correction observation

Root authorized canonical package/module record, variant and case indexes while retaining every per-file declaration and refusing conflicting secondary declarations with PAL241. The following exact fixtures extend the already-fixed function-only duplicate module/package case. Both physical files are discovered, and dependency.py is explicitly selected/open with version1. The initializer must supply the imported payload schema despite the secondary open file. No corrected candidate has been observed for these expectations.

```python
NOMINAL_LITERALS = {
    "R01": "# mode: fun\nfrom pyalamode import record\n\n@record\nclass Item:\n    payload: int\n",
    "R02": "# mode: fun\nfrom pyalamode import record\n\n@record\nclass Item:\n    payload: str\n",
    "R03": "# mode: fun\nfrom dependency import Item\n\ndef payload(item: Item) -> str:\n    return item.payload\n",
    "R04": "# mode: fun\nfrom dependency import Item\n\ndef payload(item: Item) -> int:\n    return item.payload\n",
    "V01": "# mode: fun\nfrom pyalamode import variant, case\n\n@variant\nclass Item:\n    @case\n    class Value:\n        payload: int\n",
    "V02": "# mode: fun\nfrom pyalamode import variant, case\n\n@variant\nclass Item:\n    @case\n    class Value:\n        payload: str\n",
    "V03": "# mode: fun\nfrom dependency import Item\n\ndef payload(item: Item.Value) -> str:\n    return item.payload\n",
    "V04": "# mode: fun\nfrom dependency import Item\n\ndef payload(item: Item.Value) -> int:\n    return item.payload\n",
}
```

R01/V01 are dependency.py; R02/V02 are dependency/__init__.py; R03/V03 begin as alias.py. Positive caller diagnostics must contain no PAL211: the current canonical field is str. The project remains status1 because the conflicting secondary declaration has PAL241 and its file/declaration is unverified. Its per-file int schema remains visible, while the initializer's str schema is separately retained. Opening alias.py with R04/V04 must add PAL211 in that file and leave it unverified: the source cannot use the secondary int spelling to pass. Snapshot identity changes with the actual revision. These expectations preserve existing runtime/admission scope; no ambiguous nominal import is certified.

## Installed-suite relocation correction, before final observation

Root's controller source review found that discovering checkout tests directly would make inherited child commands set PYTHONPATH to the checkout via their test file location. This is the already-characterized M8 harness issue. The final reviewer controller now copies the unchanged tests, examples and required client/packager fixtures outside checkout, records every copied byte, and discovers OUT/tests with PYTHONPATH=OUT. OUT contains no pyalamode package. Actual parent and suite-child imports must resolve to the selected installed wheel; checkout product paths in child sys.path fail. The outside sitecustomize logger observes existing sys.modules at process exit without importing product or authored application source. Its complete record includes interpreter, argv, current directory, Python search path and every loaded pyalamode module path. Child processes that intentionally import no product remain visible. Inherited semantic expectations are unchanged; root's checkout source suite remains a separate run. This correction and logger text are fixed before final execution.

## Fixed installed-bootstrap isolation supplement, before repair observation

The client helper observed an authored workspace pyalamode/__init__.py execute before the checker through the original nonisolated module launch, with a sentinel written before valid metadata arrived. This is a concrete defect, retained in `/tmp/pyalamode-m09-client-bootstrap-probe.json`; the final independent corrected observations are recorded below. Root authorized the exact selected installed interpreter launch `<literal absolute Python> -I -m pyalamode.editor --stdio --root <canonical root>`. This replaces the original nonisolated launch expectation based on the observed defect; existing admission/runtime contracts and request schemas remain unchanged. Source-mode PYTHONPATH launch does not establish installed isolated provenance.

```python
BOOTSTRAP_LITERALS = {
    "B01": "from pathlib import Path\n(Path(__file__).parents[1] / 'bootstrap-package-sentinel').write_text('executed')\n",
    "B02": "from pathlib import Path\nPath(__file__).with_name('bootstrap-site-sentinel').write_text('executed')\n",
    "B03": "from pathlib import Path\nPath(__file__).with_name('bootstrap-user-sentinel').write_text('executed')\n",
    "B04": "from pathlib import Path\nPath(__file__).with_name('bootstrap-startup-sentinel').write_text('executed')\n",
}
```

Three independent real installed-server sessions fix workspace pyalamode shadow alone, external PYTHONPATH/PYTHONHOME/PYTHONSTARTUP poisoning alone, and their combination. B01 is each shadow initializer; B02/B03 are external sitecustomize/usercustomize files; B04 is the explicitly selected PYTHONSTARTUP file. Every initialize must retain the selected interpreter, exact isolated argv and actual installed product-byte snapshot. All package/site/user/startup sentinels must remain absent before and after actual project checking. Each poisoned workspace also runs the literal selected Python `-I -c` identity subprocess, retains actual package __file__/sys.path and requires the selected installed package with neither authored root nor poisoning directory in the search path. The actual editor wire then separately proves initialize/snapshot byte provenance and absent sentinels. The actual exported JavaScript Client independently gets workspace/package plus external startup poisoning with exact isolated arguments and absent sentinels. The loaded-product lifetime case now copies exact installed product bytes into a separate freshly created interpreter site-packages directory, runs that interpreter with -I, changes only its editor.py and observes stale/restart followed by a fresh restart. No checkout product or authored source is executed during static evidence collection. The suite-child provenance logger remains a deliberately nonisolated harness-only observer of inherited commands; isolated `-I` children ignore OUT/PYTHONPATH and that logger, so its records are not claimed to cover them. The actual poisoned `-I -c` identity subprocess and real wire/byte records separately establish isolated installed launch provenance.

## Complete bounded executable supplement, fixed before candidate calls

Literal expectations remain fixed, except the explicitly evidenced bootstrap launch repair above. The complete current controllers include documented reviewer repairs, P07 collision, canonical nominal-schema and installed-bootstrap supplements fixed before their first observation, and installed-suite relocation before final execution. Final installed-wheel/suite controller remains held until root joint freeze. prepare.py creates the wheel from an exact outside-checkout copy and verifies root freeze inputs before/after; neither packaging preparation nor tests edit checkout source.

`/tmp/pyalamode-m09-review/probe.py` SHA-256 `2eb3d624b83e1aae190c7fe3b99f4a593b9736fd413356ddb680cddf0bbfd62e`:

```python
import argparse, ast, datetime, hashlib, json, os, pathlib, re, select, shutil, subprocess, sys, tempfile, time, traceback
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(__file__).resolve().parent
NAME = sys.argv[2]
checks = 0
failures = []
records = []

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def check(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)

def source_map():
    paths = [ROOT/'pyproject.toml', ROOT/'README.md']
    for area in ('pyalamode', 'tests', 'examples', 'editors'):
        paths.extend(p for p in (ROOT/area).rglob('*') if p.is_file() and p.suffix in ('.py','.js','.cjs','.json','.md','.txt') and '__pycache__' not in p.parts)
    result = {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))}
    for p in sorted(OUT.glob('*.py')):
        result['reviewer:'+p.name] = sha(p)
    for p in sorted(OUT.glob('*.js')):
        result['reviewer:'+p.name] = sha(p)
    return result

def group(name, action):
    start = checks
    try:
        detail = action()
        records.append({'name':name,'checks':checks-start,'passed':True,'detail':detail})
    except Exception as error:
        failures.append({'name':name,'error':repr(error),'traceback':traceback.format_exc()})
        records.append({'name':name,'checks':checks-start,'passed':False})

text = (ROOT/'Docs/conformance/m09-cases.md').read_text()
literals = {}
for block in re.findall(r'(?ms)^```python\n(.*?)^```\s*$',text):
    tree = ast.parse(block)
    for node in tree.body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id.endswith('LITERALS'):
            literals.update(ast.literal_eval(node.value))
fixture_identity = {name:hashlib.sha256(value.encode()).hexdigest() for name,value in literals.items()}

class RPCError(Exception):
    def __init__(self,packet):
        self.packet=packet
        super().__init__(repr(packet))

class Wire:
    def __init__(self,root,env=None,python=None):
        self.root=Path(root).resolve();self.id=0;self.buffer=b'';self.packets=[];self.requests=[]
        self.python=str(python or sys.executable);self.argv=[self.python,'-I','-m','pyalamode.editor','--stdio','--root',str(self.root)]
        self.process=subprocess.Popen(self.argv,cwd=self.root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    def send(self,method,params=None,notification=False,parts=False):
        packet={'jsonrpc':'2.0','method':method,'params':{} if params is None else params}
        if not notification:
            self.id+=1;packet['id']=self.id
        raw=json.dumps(packet,ensure_ascii=False,separators=(',',':')).encode()
        frame=('Content-Length: '+str(len(raw))+'\r\n\r\n').encode()+raw
        self.requests.append(packet)
        if parts:
            for chunk in (frame[:7],frame[7:26],frame[26:]):
                self.process.stdin.write(chunk);self.process.stdin.flush()
        else:
            self.process.stdin.write(frame);self.process.stdin.flush()
        return packet.get('id')
    def read(self,timeout=30):
        deadline=time.monotonic()+timeout
        while True:
            marker=self.buffer.find(b'\r\n\r\n')
            if marker>=0:
                head=self.buffer[:marker].decode('ascii');rows=head.split('\r\n')
                lengths=[r.split(':',1)[1].strip() for r in rows if r.lower().startswith('content-length:')]
                check(len(lengths)==1,'stdout exact framing length')
                length=int(lengths[0]);check(0<=length<=8*1024*1024,'stdout bounded body')
                if len(self.buffer)>=marker+4+length:
                    raw=self.buffer[marker+4:marker+4+length];self.buffer=self.buffer[marker+4+length:]
                    packet=json.loads(raw.decode('utf-8'));check(packet.get('jsonrpc')=='2.0','stdout JSONRPC2')
                    self.packets.append(packet);return packet
            remaining=deadline-time.monotonic()
            if remaining<=0:raise TimeoutError('wire reply timeout')
            readable,_,_=select.select([self.process.stdout],[],[],remaining)
            if not readable:raise TimeoutError('wire read timeout')
            raw=os.read(self.process.stdout.fileno(),65536)
            if not raw:raise EOFError('server ended before framed reply')
            self.buffer+=raw
    def receive(self,request_id):
        while True:
            packet=self.read()
            if packet.get('id')==request_id:
                check(('result' in packet)^('error' in packet),'one result/error')
                if 'error' in packet:raise RPCError(packet)
                return packet['result']
            check('method' in packet and 'id' not in packet,'only notifications before response')
    def request(self,method,params=None,parts=False):
        return self.receive(self.send(method,params,parts=parts))
    def error(self,method,params=None):
        try:self.request(method,params)
        except RPCError as e:return e.packet
        raise AssertionError('expected explicit RPC error: '+method)
    def initialize(self):
        result=self.request('initialize',{'rootUri':self.root.as_uri(),'capabilities':{}},parts=True)
        caps=result['capabilities'];check(caps['positionEncoding']=='utf-16','explicit UTF16')
        check(caps['textDocumentSync']=={'openClose':True,'change':1,'save':{'includeText':False}},'exact full-text sync')
        provenance=caps['experimental']['pyalamode'];check(provenance['schema']==1 and provenance['target']=='cpython-3.13.1','target provenance')
        check(provenance['pythonVersion']==[3,13,1] and provenance['root']==str(self.root),'actual version/root provenance')
        check(provenance['filesystemEncoding']=='utf-8' and provenance['filesystemErrors']=='surrogateescape','filesystem provenance')
        check(Path(provenance['pythonExecutable']).resolve()==Path(self.python).resolve(),'actual interpreter provenance')
        self.send('initialized',{},notification=True);return result
    def project(self,audit=False):return self.request('pyalamode/project',{'audit':audit})
    def open(self,path,text,version=1):
        self.send('textDocument/didOpen',{'textDocument':{'uri':Path(path).as_uri(),'languageId':'python','version':version,'text':text}},notification=True)
        return self.project()
    def change(self,path,text,version):
        self.send('textDocument/didChange',{'textDocument':{'uri':Path(path).as_uri(),'version':version},'contentChanges':[{'text':text}]},notification=True)
        return self.project()
    def stop(self):
        try:
            if self.process.poll() is None:
                self.request('shutdown',{});self.send('exit',{},notification=True)
                self.process.stdin.close();self.process.wait(timeout=5)
        finally:
            if self.process.poll() is None:self.process.kill();self.process.wait(timeout=5)
        record={'argv':self.argv,'requests':self.requests,'packets':self.packets,'status':self.process.returncode,'stderr':self.process.stderr.read().decode(errors='replace')}
        (OUT/(NAME+'-wire-'+self.root.name+'-'+str(self.process.pid)+'.json')).write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
        return record

def fixture(name,files):
    path=OUT/(NAME+'-'+name)
    if path.exists():shutil.rmtree(path)
    path.mkdir()
    for relative,value in files.items():
        target=path/relative;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(value.encode('utf-8'))
    return path

def file_rows(project):return project['report']['files']
def contracts(project):return [c for f in file_rows(project) for c in f['contracts']]
def codes(project):return {d['code'] for d in project['diagnostics']}
def position(path,line,character):return {'textDocument':{'uri':Path(path).as_uri()},'position':{'line':line,'character':character}}
def primary(project,code):return next(d for d in project['diagnostics'] if d['code']==code)

before=source_map()
import pyalamode
from pyalamode.project import check_paths,check_snapshot,build_paths
from pyalamode.integration_contracts import integration_snapshot
installed_before={'pyalamode/'+p.name:sha(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}

def coordinates():
    detail=[]
    for name,rule,start,end in [('U01','PAL101',(4,4),(4,12)),('U02','PAL230',(5,8),(5,18)),('U03','PAL230',(3,18),(3,28)),('U04','PAL121',(0,7),None),('U05','PAL121',(0,6),None),('U06','PAL001',(1,0),None),('U07','PAL101',(5,4),(5,12)),('U08','PAL230',(3,19),(3,29))]:
        variants=[literals[name]]
        if name=='U01':variants += [literals[name].replace('\n','\r\n'),literals[name].rstrip('\n')]
        for index,source in enumerate(variants):
            root=fixture(name+str(index),{'core.py':source});path=root/'core.py';wire=Wire(root)
            try:
                wire.initialize();project=wire.project();engine=check_paths(root=root,cache=False).to_dict()
                check(project['report']['status']==engine['status']==(2 if name=='U06' else 1),'same gate status '+name)
                diag=primary(project,rule);check(diag['range']['start']=={'line':start[0],'character':start[1]},'authored start '+name)
                if end:check(diag['range']['end']=={'line':end[0],'character':end[1]},'exact AST end '+name)
                raw=next(d for f in engine['files'] for d in f['diagnostics'] if d['rule']==rule) if engine['files'] else next(d for d in engine['tooling'] if d['rule']==rule)
                for field in ('path','line','column','end_line','end_column','column_encoding'):
                    check(diag['data']['authored'][field]==raw[field],'shared authored '+name+field)
                for field in ('boundary','origin','reason','remediation'):check(diag['data'][field]==raw[field],'shared '+name+field)
                check(diag['message']==raw['reason']+'\n'+raw['remediation'],'same useful message')
                check(not project['report']['verified'],'invalid never certified')
                if name=='U01':check(diag['relatedInformation'][0]['location']['range']['start']['line']==3,'first binding authored')
                if name=='U07':check(diag['relatedInformation'][0]['location']['range']['start']['line']==4,'lone CR first binding authored')
                audit=wire.project(True);check(audit['report']['status']==(2 if name=='U06' else 0) and not audit['report']['verified'],'audit/tooling distinction')
                detail.append({'fixture':name,'variant':index,'status':engine['status'],'diagnostic':diag,'wire':wire.stop()})
            finally:
                if wire.process.poll() is None:wire.stop()
    return detail
group('coordinates-shared-engine',coordinates)

def navigation():
    root=fixture('navigation',{'core.py':literals['S01'],'dependency.py':literals['S03'],'alias.py':literals['S02']});wire=Wire(root)
    try:
        wire.initialize();project=wire.project();check(project['report']['status']==0,'admitted navigation project')
        for filename,line,char,targetline in [('core.py',8,12,6),('core.py',14,12,2),('alias.py',4,12,2)]:
            result=wire.request('textDocument/definition',position(root/filename,line,char));check(len(result)==1,'one concrete definition')
            expected=root/('dependency.py' if filename=='alias.py' else 'core.py')
            check(result[0]['uri']==expected.as_uri() and result[0]['range']['start']['line']==targetline,'actual resolved lexical/import identity')
        check(wire.request('textDocument/definition',position(root/'core.py',11,12))==[],'shadowed parameter no guessed definition')
        for line,count in [(8,2),(14,2)]:
            params={**position(root/'core.py',line,12),'context':{'includeDeclaration':True}}
            refs=wire.request('textDocument/references',params);check(len(refs)==count,'separate actual reference inventories')
            params['context']['includeDeclaration']=False
            check(len(wire.request('textDocument/references',params))==count-1,'includeDeclaration respected')
        symbols=wire.request('textDocument/documentSymbol',{'textDocument':{'uri':(root/'core.py').as_uri()}})
        check(bool(symbols),'useful participating symbols')
        hover=wire.request('textDocument/hover',position(root/'core.py',14,12));check(hover and 'contents' in hover,'contract hover exists')
        explanation=wire.request('pyalamode/explain',{'symbol':'core:outer'});check(explanation['contract'] is not None,'current exact symbol contract')
        ambiguous=wire.request('pyalamode/explain',{'symbol':'caller'});check(ambiguous['status']!=0 and ambiguous['contract'] is None,'unqualified symbol deliberately unsupported')
        rule=wire.request('pyalamode/explain',{'symbol':'PAL101'});check('remediation' in rule['text'].lower() or 'initial' in rule['text'].lower(),'rule explanation useful')
        unsupported=wire.request('pyalamode/explain',{'symbol':'no_such_symbol'});check(unsupported['status']!=0 and unsupported['contract'] is None,'unknown explicit unsupported')
        return {'project':project,'wire':wire.stop()}
    finally:
        if wire.process.poll() is None:wire.stop()
group('resolved-navigation',navigation)

def states():
    root=fixture('states',{'dependency.py':literals['S03'],'alias.py':literals['S02']});path=root/'dependency.py';wire=Wire(root);disk=path.read_bytes()
    bad=literals['S03'].replace('value + 1','missing(value)')
    try:
        wire.initialize();clean=wire.open(path,literals['S03']);check(clean['report']['status']==0,'open clean')
        broken=wire.change(path,bad,2);check(broken['report']['status']==1 and 'PAL230' in codes(broken),'unsaved failure supersedes clean')
        check(broken['inputs']['sources'][str(path)]['origin']=='overlay' and broken['inputs']['sources'][str(path)]['version']==2,'explicit overlay provenance')
        for version in (2,1,True):
            rejected=wire.change(path,literals['S03'],version);check(rejected['report']['status']==1 and rejected['inputs']['sources'][str(path)]['version']==2,'stale/invalid version cannot replace buffer')
        fixed=wire.change(path,literals['S03'],3);check(fixed['report']['status']==0 and fixed['snapshot']!=broken['snapshot'],'fresh valid revision')
        check(path.read_bytes()==disk,'wire never writes source')
        direct=check_snapshot(root=root,overlays={str(path):{'text':bad,'version':4}},cache=False)
        check(direct.result.status==1 and direct.sources[str(path)]==bad,'direct snapshot full overlay pipeline')
        check(path.read_bytes()==disk,'direct snapshot never writes source')
        (root/'writer.py').write_text('from dependency import leaf\nleaf.__code__ = None\n')
        written=wire.project();check(written['report']['status']==1 and 'PAL240' in codes(written),'current root writer invalidates evidence')
        (root/'writer.py').unlink();check(wire.project()['report']['status']==0,'removed writer restores fresh evidence')
        package=root/'dependency';package.mkdir();(package/'__init__.py').write_text(literals['S03'].replace('value + 1','value + 2'))
        changed=wire.project();check(changed['snapshot']!=fixed['snapshot'],'package precedence changes snapshot')
        definition=wire.request('textDocument/definition',position(root/'alias.py',4,12));check(definition[0]['uri']==(package/'__init__.py').as_uri(),'current package precedence navigation')
        (package/'__init__.py').write_text('# mode: fun\n\ndef leaf(value: int) -> str:\n    return "package"\n')
        incompatible=wire.project();check(incompatible['report']['status']==1 and 'PAL211' in codes(incompatible),'actual package signature invalidates caller return contract')
        alias_file=next(f for f in file_rows(incompatible) if f['path']==str(root/'alias.py'))
        check(not alias_file['verified'] and any(d['rule']=='PAL211' for d in alias_file['diagnostics']),'actual package contract, not same-spelling module contract')
        shutil.rmtree(package)
        wire.send('textDocument/didClose',{'textDocument':{'uri':path.as_uri()}},notification=True)
        closed=wire.project();check(closed['report']['status']==0 and closed['inputs']['sources'][str(path)]['origin']=='disk','close restores disk evidence')
        (root/'pyproject.toml').write_text('[tool.pyalamode]\nschema = 999\n')
        tooling=wire.project();check(tooling['report']['status']==2 and not tooling['report']['verified'],'bad policy visible tooling')
        check(tooling['report']['tooling'] and 'PAL001' in codes(tooling),'policy diagnostics never clean view')
        return {'broken':broken,'closed':closed,'tooling':tooling,'wire':wire.stop()}
    finally:
        if wire.process.poll() is None:wire.stop()
group('overlay-writer-policy-resolution',states)

def nominal_resolution():
    detail=[]
    for kind,prefix in (('record','R'),('variant','V')):
        root=fixture('nominal-'+kind,{'dependency.py':literals[prefix+'01'],'dependency/__init__.py':literals[prefix+'02'],'alias.py':literals[prefix+'03']})
        shadow=root/'dependency.py';package=root/'dependency/__init__.py';caller=root/'alias.py';wire=Wire(root)
        try:
            wire.initialize();positive=wire.open(shadow,literals[prefix+'01'])
            shadow_file=next(f for f in file_rows(positive) if f['path']==str(shadow))
            package_file=next(f for f in file_rows(positive) if f['path']==str(package))
            caller_file=next(f for f in file_rows(positive) if f['path']==str(caller))
            check(positive['report']['status']==1,'conflicting '+kind+' shadow is not clean')
            check(any(d['rule']=='PAL241' for d in shadow_file['diagnostics']) and not shadow_file['verified'],'conflicting shadow '+kind+' declaration fails closed')
            check(not any(d['rule']=='PAL211' for d in caller_file['diagnostics']),'canonical package str '+kind+' field drives positive caller')
            field_key='records' if kind=='record' else 'variants'
            canonical=next(row for row in package_file[field_key] if row['name']=='Item')
            secondary=next(row for row in shadow_file[field_key] if row['name']=='Item')
            canonical_fields=canonical['fields'] if kind=='record' else canonical['cases']['Value']['fields']
            secondary_fields=secondary['fields'] if kind=='record' else secondary['cases']['Value']['fields']
            check(canonical_fields=={'payload':'str'},'canonical package '+kind+' schema retained')
            check(secondary_fields=={'payload':'int'} and 'unverified' in secondary['source_evidence'],'secondary per-file '+kind+' schema retained without successful claim')
            check(positive['inputs']['sources'][str(shadow)]['origin']=='overlay','selected/open secondary '+kind+' buffer participates')
            inverted=wire.open(caller,literals[prefix+'04'])
            inverted_file=next(f for f in file_rows(inverted) if f['path']==str(caller))
            check(inverted['report']['status']==1 and any(d['rule']=='PAL211' for d in inverted_file['diagnostics']) and not inverted_file['verified'],'inverted int '+kind+' caller cannot reuse shadow schema')
            check(inverted['snapshot']!=positive['snapshot'],'current '+kind+' caller revision changes source identity')
            detail.append({'kind':kind,'positive':positive,'inverted':inverted,'wire':wire.stop()})
        finally:
            if wire.process.poll() is None:wire.stop()
    return detail
group('canonical-record-variant-case-resolution',nominal_resolution)

def previews():
    detail=[]
    for name in ('P01','P02','P03','P04','P05','P06','P07','F01','F03','T01'):
        root=fixture('preview-'+name,{'core.py':literals[name]});path=root/'core.py';wire=Wire(root);original=path.read_bytes()
        try:
            wire.initialize();project=wire.open(path,literals[name]);desired='PAL250' if name=='F01' else 'PAL101' if name.startswith('P') else next(iter(codes(project)))
            diag=primary(project,desired);params={'uri':path.as_uri(),'version':1,'snapshot':project['snapshot'],'diagnosticIndex':diag['data']['diagnosticIndex']}
            try:preview=wire.request('pyalamode/preview',params)
            except RPCError as error:
                check(name in ('P02','P03','P04','P06','F03','T01'),'required finite preview must exist '+name)
                preview={'error':error.packet}
            else:
                check(name not in ('P02','P03','F03','T01'),'ineligible must refuse '+name)
                check(preview['before']==literals[name] and preview['uri']==path.as_uri() and preview['version']==1,'exact source/version preview')
                check(preview['snapshot']==project['snapshot'] and preview['edits'] and preview['diff'],'reviewable fixed snapshot/edits')
                after=preview['after'];check(after!=preview['before'],'useful actual program change')
                check(all(word not in after for word in ('# type: ignore','@effects','integration_approvals','except ')),'no silent permissions/ignore/failure rewrite')
                if name=='F01':check('return values' in after and preview['limits'],'original immutable return semantics disclosed')
                candidate=check_snapshot(root=root,overlays={str(path):{'text':after,'version':2}},cache=False)
                check(candidate.result.status==0,'preview strict full candidate gate')
                if name.startswith('P'):
                    namespace={};exec(compile(literals[name],str(path),'exec'),namespace);repair={};exec(compile(after,str(path),'exec'),repair)
                    for value in (-10,0,7):check(namespace['f'](value)==repair['f'](value),'ordinary dataflow preserved '+name)
            check(path.read_bytes()==original,'preview never writes source')
            new=wire.change(path,literals[name]+'\n',2);wire.error('pyalamode/preview',params)
            check(new['inputs']['sources'][str(path)]['version']==2,'stale preview requested only after actual new version')
            detail.append({'fixture':name,'preview':preview,'wire':wire.stop()})
        finally:
            if wire.process.poll() is None:wire.stop()
    return detail
group('finite-review-only-previews',previews)

def security():
    root=fixture('security',{'core.py':literals['S03']});outside=fixture('outside',{'secret.py':'secret = "not-for-this-root"\n'});wire=Wire(root)
    try:
        wire.initialize();wire.project()
        (root/'escape.py').symlink_to(outside/'secret.py')
        for uri in ((outside/'secret.py').as_uri(),'file://remotehost'+str(root/'core.py'),'https://example.com/core.py',(root/'escape.py').as_uri(),'file://'+str(root/'core.py')+'%GG'):
            wire.error('textDocument/hover',{'textDocument':{'uri':uri},'position':{'line':0,'character':0}})
        (root/'escape.py').unlink()
        for bad in ({'line':-1,'character':0},{'line':True,'character':0},{'line':0,'character':0.5},{'line':999,'character':0},{'line':0,'character':999}):
            wire.error('textDocument/hover',{'textDocument':{'uri':(root/'core.py').as_uri()},'position':bad})
        for method,params in [('noSuchMethod',{}),('pyalamode/project',{'audit':None}),('pyalamode/project',{'audit':'strict'}),('pyalamode/explain',{}),('textDocument/hover',{})]:wire.error(method,params)
        policy=wire.project();check(policy['report']['status']==0,'protocol rejection cannot poison current clean project')
        wire.process.stdin.write(b'Content-Length: 1\r\n\r\n{');wire.process.stdin.flush()
        bad=wire.read();check('error' in bad,'complete invalid JSON explicit error')
        check(wire.project()['report']['status']==0,'recoverable malformed JSON leaves useful process')
        for raw in (b'{}',b'[]',b'{"jsonrpc":"2.0","id":true,"method":"pyalamode/project","params":{}}',b'{"jsonrpc":"2.0","id":{},"method":"pyalamode/project","params":{}}',b'{"jsonrpc":"2.0","id":19,"method":"pyalamode/project","params":{"audit":NaN}}',b'{"jsonrpc":"2.0","id":20,"method":"pyalamode/project","params":{"audit":Infinity}}'):
            wire.process.stdin.write(('Content-Length: '+str(len(raw))+'\r\n\r\n').encode()+raw);wire.process.stdin.flush()
            rejected=wire.read();check('error' in rejected and rejected.get('id') is None,'invalid envelope/id/nonJSON number explicit null-ID error')
            check(wire.project()['report']['status']==0,'complete invalid envelope cannot poison later project')
        ids=[wire.send('pyalamode/project',{}),wire.send('pyalamode/explain',{'symbol':'PAL101'})]
        check(wire.receive(ids[0])['report']['status']==0 and wire.receive(ids[1])['symbol']=='PAL101','concatenated frames independent replies')
        wire.send('$/cancelRequest',{'id':9999},notification=True);check(wire.project()['report']['status']==0,'ignored cancellation documented')
        return wire.stop()
    finally:
        if wire.process.poll() is None:wire.stop()
group('wire-security-and-malformed',security)

def preread_ownership():
    outside=fixture('ownership-outside',{'secret.py':literals['S03'],'policy.toml':'[tool.pyalamode]\nschema=1\n','pkg/__init__.py':literals['S03']})
    observed=[];active={'root':None}
    def audit(event,args):
        if event=='open' and active['root'] is not None and isinstance(args[0],(str,bytes)):
            try:resolved=Path(os.fsdecode(args[0])).resolve()
            except (ValueError,OSError):return
            if resolved.is_relative_to(outside):observed.append({'path':str(resolved),'mode':repr(args[1])})
    sys.addaudithook(audit)
    detail=[]
    for kind in ('selected','dependency','package','policy'):
        files={'alias.py':literals['S02']} if kind in ('dependency','package') else {'core.py':literals['S03']}
        root=fixture('ownership-'+kind,files)
        if kind=='selected':(root/'escaped.py').symlink_to(outside/'secret.py')
        elif kind=='dependency':(root/'dependency.py').symlink_to(outside/'secret.py')
        elif kind=='package':(root/'dependency').symlink_to(outside/'pkg',target_is_directory=True)
        else:(root/'pyproject.toml').symlink_to(outside/'policy.toml')
        before_count=len(observed);active['root']=root
        explanations=[]
        try:
            snapshot=check_snapshot(root=root,cache=False)
            if kind=='policy':
                from pyalamode.editor import EditorSession
                session=EditorSession(root);session.handle('initialize',{'rootUri':root.as_uri(),'capabilities':{}})
                for symbol in ('integrations','sha256_digest'):
                    answer=session.handle('pyalamode/explain',{'symbol':symbol});check(answer['status']==2,'custom explain retains refused outside policy')
                    explanations.append(answer)
        finally:active['root']=None
        check(snapshot.result.status==2 and not snapshot.result.verified,'outside symlink explicit ownership error '+kind)
        check(len(observed)==before_count,'outside content never opened before refusal '+kind)
        check(all(Path(path).is_relative_to(root) for path in snapshot.sources),'outside source never exposed '+kind)
        detail.append({'kind':kind,'result':snapshot.result.to_dict(),'explanations':explanations,'outside_opens':observed[before_count:]})
    return detail
group('actual-pre-read-source-policy-symlink-ownership',preread_ownership)

def effects_trust():
    root=fixture('effects',{'core.py':literals['C01']});wire=Wire(root)
    try:
        wire.initialize();project=wire.project();check(project['report']['status']==0,'characterized effects admitted')
        caller=next(c for c in contracts(project) if c['name']=='caller')
        check(caller['required_effects']==['Clock'] and caller['effect_origins']['Clock'],'transitive actual effect origins')
        check(caller['source_evidence']=='checked participating source' and caller['failures'],'separate checked effect failures')
        effect_record={'project':project,'wire':wire.stop()}
    finally:
        if wire.process.poll() is None:wire.stop()
    root=fixture('trust',{'core.py':literals['T01']});wire=Wire(root)
    try:
        wire.initialize();denied=wire.project();check(denied['report']['status']==1 and 'PAL350' in codes(denied),'default external trust denied')
        snapshot=integration_snapshot(root=root);row=next(r for r in snapshot['catalog'] if r['identity']=='pyalamode.integrations.sha256_digest')
        expires=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=5)
        fields={'operation':row['identity'],'contract_sha256':row['contract_sha256'],'dependency_sha256':row['dependency_sha256'],'owner':'root-authorized independent M9 fixture','rationale':'bounded conformance fixture, not a production approval','provenance':'Docs/conformance/m09-cases.md fixed E09','expires_at':expires.strftime('%Y-%m-%dT%H:%M:%SZ')}
        (root/'pyproject.toml').write_text('[tool.pyalamode]\nschema=1\nexternal_trust="approved"\n\n[[tool.pyalamode.integration_approvals]]\n'+''.join(k+'='+json.dumps(v)+'\n' for k,v in fields.items()))
        approved=wire.project();check(approved['report']['status']==0,'exact current fixture approval')
        caller=next(c for c in contracts(approved) if c['name']=='caller')
        check(len(caller['external_assumptions'])==1 and caller['external_assumptions'][0]['admission']=='approved','transitive trust stays visible')
        check('opaque' in caller['external_assumptions'][0]['source_evidence'] and caller['required_effects']==[],'opaque trust separate from checked pure invocation')
        check(next(f for f in file_rows(approved) if f['path']==str(root/'core.py'))['initialization_evidence']=='unchecked ordinary module initialization','ordinary setup stays unchecked')
        while datetime.datetime.now(datetime.timezone.utc)<expires:time.sleep(.2)
        expired=wire.project();check(expired['report']['status']==1 and 'PAL350' in codes(expired) and expired['snapshot']!=approved['snapshot'],'actual UTC expiry invalidates unchanged source/policy')
        return {'effects':effect_record,'approved':approved,'expired':expired,'fixture_approval':fields,'wire':wire.stop()}
    finally:
        if wire.process.poll() is None:wire.stop()
group('actual-effects-trust-UTC-expiry',effects_trust)

def nonexecution():
    root=fixture('nonexecution',{'dependency.py':"from pathlib import Path\nPath('import-sentinel').write_text('executed')\nfrom pyalamode import fun\n@fun\ndef leaf(value:int)->int:\n    return value\n",'core.py':"from pathlib import Path\nfrom pyalamode import fun\nfrom dependency import leaf\nPath('module-sentinel').write_text('executed')\n\ndef hook():\n    Path('hook-sentinel').write_text('executed')\n    return int\n\n@fun\n@hook()\ndef bad(value: hook() = hook()) -> int:\n    return 1\n\n@fun\ndef caller(value:int)->int:\n    return leaf(value)\n"});wire=Wire(root)
    try:
        wire.initialize();project=wire.project();check(project['report']['status']==1,'invalid declarations remain rejected')
        wire.request('pyalamode/explain',{'symbol':'PAL120'});wire.request('textDocument/documentSymbol',{'textDocument':{'uri':(root/'core.py').as_uri()}})
        check(not any(p.name.endswith('sentinel') for p in root.iterdir()),'no app imports/defaults/decorators/annotations executed')
        return {'project':project,'wire':wire.stop()}
    finally:
        if wire.process.poll() is None:wire.stop()
group('static-source-hook-nonexecution',nonexecution)

def bootstrap_isolation():
    detail=[]
    for mode in ('workspace-shadow','startup-poison','combined'):
        files={'core.py':literals['S03']}
        if mode!='startup-poison':files['pyalamode/__init__.py']=literals['B01']
        root=fixture('bootstrap-'+mode,files)
        poison=fixture('bootstrap-poison-'+mode,{'pyalamode/__init__.py':literals['B01'],'sitecustomize.py':literals['B02'],'usercustomize.py':literals['B03'],'startup.py':literals['B04']})
        env={**os.environ}
        if mode!='workspace-shadow':env.update(PYTHONPATH=str(poison),PYTHONHOME=str(poison),PYTHONSTARTUP=str(poison/'startup.py'))
        identity_argv=[sys.executable,'-I','-c','import json,pyalamode,sys;print(json.dumps({"package":pyalamode.__file__,"executable":sys.executable,"sys_path":sys.path}))']
        identity_run=subprocess.run(identity_argv,cwd=root,env=env,capture_output=True,text=True)
        check(identity_run.returncode==0,'actual isolated package identity subprocess succeeds despite startup poisoning')
        identity=json.loads(identity_run.stdout)
        check(Path(identity['package']).resolve()==Path(pyalamode.__file__).resolve(),'actual isolated child imports selected installed package')
        check(not any(Path(entry).resolve() in (root,poison) for entry in identity['sys_path'] if entry),'isolated child excludes authored startup paths')
        check(not list(root.rglob('*sentinel')) and not list(poison.rglob('*sentinel')),'isolated identity subprocess executes no authored hooks')
        wire=Wire(root,env)
        try:
            initialize=wire.initialize();project=wire.project()
            check(wire.argv==[sys.executable,'-I','-m','pyalamode.editor','--stdio','--root',str(root)],'literal isolated installed interpreter launch')
            check(all(sha(Path(pyalamode.__file__).parent/name)==value for name,value in project['inputs']['product_artifacts'].items()),'bootstrap snapshot identifies actual installed product bytes')
            check(not list(root.rglob('*sentinel')) and not list(poison.rglob('*sentinel')),'workspace and startup hooks never executed before checking')
            detail.append({'mode':mode,'initialize':initialize,'project':project,'isolated_identity':{'argv':identity_argv,'status':identity_run.returncode,'stdout':identity_run.stdout,'stderr':identity_run.stderr,'observed':identity},'poison_environment':{key:env[key] for key in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP') if mode!='workspace-shadow'},'wire':wire.stop()})
        finally:
            if wire.process.poll() is None:wire.stop()
    return detail
group('actual-installed-bootstrap-isolation',bootstrap_isolation)

def product_lifetime():
    root=fixture('product-lifetime',{'core.py':literals['S03']})
    copied=OUT/(NAME+'-copied-package')
    if copied.exists():shutil.rmtree(copied)
    made=subprocess.run([sys.executable,'-I','-m','venv','--without-pip','--copies',str(copied)],capture_output=True,text=True)
    check(made.returncode==0,'isolated installed-product interpreter created')
    isolated_python=copied/'bin/python'
    located=subprocess.run([str(isolated_python),'-I','-c','import sysconfig;print(sysconfig.get_path("purelib"))'],capture_output=True,text=True)
    check(located.returncode==0,'isolated interpreter site-packages resolved')
    isolated_package=Path(located.stdout.strip())/'pyalamode'
    shutil.copytree(Path(pyalamode.__file__).parent,isolated_package,ignore=shutil.ignore_patterns('__pycache__'))
    check({p.name:sha(p) for p in isolated_package.glob('*.py')}=={p.name:sha(p) for p in Path(pyalamode.__file__).parent.glob('*.py')},'isolated installed product copy is exact')
    wire=Wire(root,python=isolated_python)
    try:
        wire.initialize();original=wire.project();check(original['report']['status']==0,'actual copied installation current initially')
        artifact=isolated_package/'editor.py';artifact.write_bytes(artifact.read_bytes()+b'\n# independent isolated product-byte mutation\n')
        changed=wire.project();check(changed['report']['status']==2 and not changed['report']['verified'],'loaded old implementation cannot certify changed disk product')
        check('stale' in changed['freshness'].lower() or 'restart' in json.dumps(changed).lower(),'loaded product mismatch explicitly stale/restart')
        check(all(not f['verified'] for f in file_rows(changed)),'stale loaded product leaves no successful file claim')
        check(all('unverified' in c['source_evidence'] for c in contracts(changed)),'stale loaded product leaves no checked source contract')
        first=wire.stop();wire=Wire(root,python=isolated_python);wire.initialize();fresh=wire.project()
        check(fresh['report']['status']==0 and fresh['snapshot']!=original['snapshot'],'new actual process checks current copied bytes')
        target=check_snapshot(root=root,target='cpython-3.13.9');check(target.result.status==2 and not target.result.verified,'unsupported target distinct tooling')
        return {'isolated_interpreter':str(isolated_python),'isolated_package':str(isolated_package),'original':original,'stale':changed,'fresh':fresh,'before_wire':first,'after_wire':wire.stop()}
    finally:
        if wire.process.poll() is None:wire.stop()
group('actual-loaded-product-bytes-and-restart',product_lifetime)

def captured_races():
    from unittest.mock import patch
    from pyalamode.checker import SourceGraph
    detail=[]
    for kind in ('source','policy','overlay-disk'):
        root=fixture('race-'+kind,{'core.py':literals['S03']});path=root/'core.py'
        original=SourceGraph.analyze
        def changed(graph,*args,**kwargs):
            result=original(graph,*args,**kwargs)
            if kind=='policy':(root/'pyproject.toml').write_text('[tool.pyalamode]\nschema=999\n')
            else:path.write_text(literals['S03']+'\n# changed after captured graph analysis\n')
            return result
        overlays={str(path):{'text':literals['S03'],'version':1}} if kind=='overlay-disk' else None
        with patch.object(SourceGraph,'analyze',changed):snapshot=check_snapshot(root=root,cache=False,overlays=overlays)
        value=snapshot.result.to_dict()
        check(value['status']==2 and not value['verified'] and 'stale' in snapshot.freshness,'captured input race is stale tooling '+kind)
        check(all(not f['verified'] for f in value['files']),'race leaves no successful file claim '+kind)
        check(all('unverified' in c['source_evidence'] for f in value['files'] for c in f['contracts']),'race leaves no checked source contract '+kind)
        detail.append({'kind':kind,'freshness':snapshot.freshness,'report':value})
    return detail
group('captured-current-input-races-and-file-claims',captured_races)

def malformed_lifecycle():
    root=fixture('lifecycle',{'core.py':literals['S03']});wire=Wire(root)
    detail=[]
    try:
        wire.error('pyalamode/project',{});wire.error('initialize',{'rootUri':OUT.as_uri(),'capabilities':{}})
        wire.initialize();wire.error('initialize',{'rootUri':root.as_uri(),'capabilities':{}})
        wire.request('shutdown',{});wire.error('pyalamode/project',{})
        wire.send('exit',{},notification=True);wire.process.stdin.close();wire.process.wait(timeout=5)
        check(wire.process.returncode is not None,'explicit shutdown/exit complete')
        detail.append({'requests':wire.requests,'packets':wire.packets,'status':wire.process.returncode})
    finally:
        if wire.process.poll() is None:wire.process.kill();wire.process.wait(timeout=5)
    for raw in (b'Content-Length: -1\r\n\r\n',b'Content-Length: nope\r\n\r\n',b'Content-Length: 1\r\nContent-Length: 1\r\n\r\n{}',b'Content-Length: 8388609\r\n\r\n',b'X'*9000+b'\r\n\r\n',b'Content-Length: 2\r\n\r\n\xff\xff',b'Content-Length: 10\r\n\r\n{'):
        process=subprocess.Popen([sys.executable,'-I','-m','pyalamode.editor','--stdio','--root',str(root)],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=process.communicate(raw,timeout=5)
        check(process.returncode is not None,'malformed/truncated wire bounded EOF termination')
        check(not stdout or stdout.startswith(b'Content-Length:'),'malformed wire stdout remains framed')
        detail.append({'input_hex':raw.hex(),'status':process.returncode,'stdout_hex':stdout.hex(),'stderr':stderr.decode(errors='replace')})
    return detail
group('actual-malformed-framing-and-lifecycle',malformed_lifecycle)

def guards():
    detail=[]
    for mode in ('off','exports','debug'):
        root=fixture('guard-'+mode,{'core.py':literals['G01']});path=root/'core.py'
        policy='[tool.pyalamode]\nschema=1\nboundary_guards='+json.dumps(mode)+'\n'
        if mode!='off':policy+='guarded_exports=["core:echo"]\n'
        (root/'pyproject.toml').write_text(policy);artifact=root/'build'/'artifact'
        built=build_paths(root=root,output=artifact);check(built.status==0,'real guard artifact '+mode)
        if mode in ('off','exports'):check((artifact/'core.py').read_bytes()==path.read_bytes(),'ordinary compatible original byte copy')
        wire=Wire(root)
        try:
            wire.initialize();project=wire.project();params={'artifactUri':artifact.as_uri(),'publicBoundary':'pyalamode_exports.core:echo','phase':'argument','name':'payload'}
            if mode=='off':wire.error('pyalamode/guardLocation',params)
            else:
                location=wire.request('pyalamode/guardLocation',params)
                check(location['location']['uri']==path.as_uri() and location['location']['range']['start']['line']==7,'real argument guard authored boundary')
                returned=wire.request('pyalamode/guardLocation',{'artifactUri':artifact.as_uri(),'publicBoundary':'pyalamode_exports.core:echo','phase':'return'})
                check(returned['location']['uri']==path.as_uri(),'real return guard authored source')
                run=subprocess.run([sys.executable,'-c',"import json,sys;from core import Payload;from pyalamode import Vector;from pyalamode_exports.core import echo;p=Payload(Vector.of(1));object.__setattr__(p,'values',Vector.of(True));calls=[];code=echo.__wrapped__.__code__;sys.settrace(lambda f,e,a: calls.append(e) if e=='call' and f.f_code is code else None)\ntry:echo(p)\nexcept TypeError as e:print(json.dumps({'error':str(e),'body_calls':len(calls)}))\nelse:raise AssertionError('invalid nested guard input passed')"],cwd=artifact,capture_output=True,text=True)
                check(run.returncode==0,'actual stock artifact nested guard failure')
                observed=json.loads(run.stdout);check(observed['body_calls']==0 and 'values' in observed['error'] and str(path) in observed['error'],'nested authored failure before body')
                changed=wire.open(path,literals['G01']+'\n');wire.error('pyalamode/guardLocation',params)
                wire.send('textDocument/didClose',{'textDocument':{'uri':path.as_uri()}},notification=True);wire.project()
                original=(artifact/'core.py').read_bytes();(artifact/'core.py').write_bytes(original+b'\n')
                wire.error('pyalamode/guardLocation',params);(artifact/'core.py').write_bytes(original)
                evidence_path=artifact/'pyalamode-evidence.json';evidence_original=evidence_path.read_bytes();evidence=json.loads(evidence_original)
                for kind in ('empty-inventory','missing-source','missing-facade','altered-coverage'):
                    altered=json.loads(evidence_original)
                    if kind=='empty-inventory':altered['artifact_files']={}
                    elif kind=='missing-source':altered['artifact_files'].pop('core.py')
                    elif kind=='missing-facade':altered['artifact_files'].pop('pyalamode_exports/core.py')
                    else:altered['guarded_exports'][0]['parameters']={'payload':'int'}
                    evidence_path.write_text(json.dumps(altered));wire.error('pyalamode/guardLocation',params);evidence_path.write_bytes(evidence_original)
            detail.append({'mode':mode,'artifact_files':json.loads((artifact/'pyalamode-evidence.json').read_text())['artifact_files'],'wire':wire.stop()})
        finally:
            if wire.process.poll() is None:wire.stop()
    return detail
group('actual-guard-authored-boundary',guards)

after=source_map()
installed_after={'pyalamode/'+p.name:sha(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}
group('input-identity',lambda:(check(before==after,'complete current source map unchanged'),check(installed_before==installed_after,'installed package map unchanged'),check(all(before[k]==v for k,v in installed_before.items()),'all imported package bytes equal checkout')))
report={'name':NAME,'checks':checks,'harness_sha256':sha(__file__),'fixture_sha256':fixture_identity,'environment':{'python':sys.version,'executable':sys.executable,'platform':sys.platform,'package':pyalamode.__file__,'filesystem_encoding':sys.getfilesystemencoding(),'filesystem_errors':sys.getfilesystemencodeerrors(),'gil':sys._is_gil_enabled()},'source_before':before,'source_after':after,'installed_before':installed_before,'installed_after':installed_after,'records':records,'unexpected':failures}
target=OUT/(NAME+'-probe.json');target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'name':NAME,'checks':checks,'groups':[(r['name'],r['passed']) for r in records],'unexpected':failures,'output':str(target)},ensure_ascii=False))
sys.exit(bool(failures))
```

`/tmp/pyalamode-m09-review/client.js` SHA-256 `8fc508d2226dcd176172f5f47d000dd499bf650684d4522bfbc46957dff6daf8`:

```javascript
'use strict';
const fs=require('node:fs'), path=require('node:path'), assert=require('node:assert/strict'), crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {execFileSync}=require('node:child_process');
const repo=process.argv[2], python=process.argv[3], root=process.argv[4], output=process.argv[5];
const {Client}=require(path.join(repo,'editors/vscode/transport.js'));
const before=crypto.createHash('sha256').update(fs.readFileSync(path.join(repo,'editors/vscode/transport.js'))).digest('hex');
fs.mkdirSync(root,{recursive:true});
const file=path.join(root,'core.py'), uri=pathToFileURL(file).href;
const bad='# mode: fun\n\ndef café(値: int) -> int:\n    café = 値\n    café = 2\n    return café\n';
const ssa='# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n';
fs.writeFileSync(file,bad);
const poison=path.join(root,'startup-poison');fs.mkdirSync(path.join(root,'pyalamode'),{recursive:true});fs.mkdirSync(path.join(poison,'pyalamode'),{recursive:true});
const packageHook='from pathlib import Path\n(Path(__file__).parents[1] / "bootstrap-package-sentinel").write_text("executed")\n';
const siteHook='from pathlib import Path\nPath(__file__).with_name("bootstrap-site-sentinel").write_text("executed")\n';
fs.writeFileSync(path.join(root,'pyalamode/__init__.py'),packageHook);fs.writeFileSync(path.join(poison,'pyalamode/__init__.py'),packageHook);fs.writeFileSync(path.join(poison,'sitecustomize.py'),siteHook);
process.env.PYTHONPATH=poison;process.env.PYTHONHOME=poison;process.env.PYTHONSTARTUP=path.join(poison,'sitecustomize.py');
const packagePath=execFileSync(python,['-I','-c','import pyalamode;print(pyalamode.__file__)'],{cwd:root,env:process.env,encoding:'utf8'}).trim();
const wire=[], logs=[], failures=[];const client=new Client(python,root);
client.on('wire',packet=>wire.push(packet));client.on('log',line=>logs.push(line));client.on('failure',e=>failures.push(String(e)));
let checks=0;function check(value,label){checks++;assert.ok(value,label);}
(async()=>{
  try {
    const initialize=await client.initialize();check(client.python===python,'literal configured launch executable preserved');
    check(!fs.existsSync(path.join(root,'bootstrap-package-sentinel'))&&!fs.existsSync(path.join(poison,'bootstrap-package-sentinel'))&&!fs.existsSync(path.join(poison,'bootstrap-site-sentinel')),'actual client isolated bootstrap hooks remain absent');
    check(JSON.stringify(client.args)===JSON.stringify(['-I','-m','pyalamode.editor','--stdio','--root',root]),'exact no-shell args');
    let project=await client.request('pyalamode/project',{});
    check(!packagePath.startsWith(root+path.sep)&&Object.entries(project.inputs.product_artifacts).every(([name,value])=>crypto.createHash('sha256').update(fs.readFileSync(path.join(path.dirname(packagePath),name))).digest('hex')===value),'actual isolated installed package identity matches server snapshot');
    check(project.report.status===1&&!project.report.verified,'actual client invalid shared gate');
    let diagnostic=project.diagnostics.find(d=>d.code==='PAL101');check(JSON.stringify(diagnostic.range)===JSON.stringify({start:{line:4,character:4},end:{line:4,character:12}}),'actual multibyte UTF16 range');
    client.notify('textDocument/didOpen',{textDocument:{uri,languageId:'python',version:1,text:ssa}});
    project=await client.request('pyalamode/project',{});diagnostic=project.diagnostics.find(d=>d.code==='PAL101');
    check(project.freshness.includes('unsaved')&&project.inputs.sources[file].version===1,'actual unsaved provenance');
    const params={uri,version:1,snapshot:project.snapshot,diagnosticIndex:diagnostic.data.diagnosticIndex};
    const preview=await client.request('pyalamode/preview',params);check(preview.before===ssa&&preview.after!==ssa&&preview.edits.length>0,'actual reviewable preview');
    check(fs.readFileSync(file,'utf8')===bad,'actual client/server no source write');
    client.notify('textDocument/didChange',{textDocument:{uri,version:2},contentChanges:[{text:preview.after}]});
    const corrected=await client.request('pyalamode/project',{});check(corrected.report.status===0&&corrected.inputs.sources[file].version===2,'current repaired overlay accepted');
    await assert.rejects(client.request('pyalamode/preview',params));checks++;
    const hover=await client.request('textDocument/hover',{textDocument:{uri},position:{line:2,character:5}});check(hover&&hover.contents,'actual client contract hover');
    const rule=await client.request('pyalamode/explain',{symbol:'PAL101'});check(rule.symbol==='PAL101'&&rule.text,'actual shared explanation');
    client.notify('textDocument/didClose',{textDocument:{uri}});const closed=await client.request('pyalamode/project',{});
    check(closed.report.status===1&&closed.inputs.sources[file].origin==='disk','close current disk rather than old good overlay');
    await assert.rejects(client.request('textDocument/hover',{textDocument:{uri:pathToFileURL(path.dirname(root)+'/outside.py').href},position:{line:0,character:0}}));checks++;
    check(failures.length===0,'RPC errors remain distinct from terminal transport failure');
    await client.stop();check(client.dead&&client.pending.size===0,'bounded shutdown settles actual client');
    const after=crypto.createHash('sha256').update(fs.readFileSync(path.join(repo,'editors/vscode/transport.js'))).digest('hex');check(before===after,'actual selected client bytes unchanged');
    fs.writeFileSync(output,JSON.stringify({checks,environment:{node:process.version,platform:process.platform,execPath:process.execPath},provenance:client.provenance,bootstrap:{poison,packagePath,identity_argv:[python,'-I','-c','import pyalamode;print(pyalamode.__file__)'],pythonstartup:process.env.PYTHONSTARTUP,pythonpath:process.env.PYTHONPATH,pythonhome:process.env.PYTHONHOME,package_hook_sha256:crypto.createHash('sha256').update(packageHook).digest('hex'),site_hook_sha256:crypto.createHash('sha256').update(siteHook).digest('hex')},transport_before:before,transport_after:after,initialize,project,preview,corrected,closed,wire,logs,failures},null,2)+'\n');
    process.stdout.write(JSON.stringify({checks,wire_messages:wire.length,output})+'\n');
  } catch(error) {await client.stop();fs.writeFileSync(output,JSON.stringify({checks,error:String(error),stack:error.stack,wire,logs,failures},null,2)+'\n');throw error;}
})().catch(error=>{process.stderr.write(String(error)+'\n');process.exitCode=1;});
```

`/tmp/pyalamode-m09-review/final.py` SHA-256 `336f7b3a6e6d401b71873595d48b0a36cf39bc7042a9c587cbcf9c283f27d6d9`:

```python
import hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve();NAME=sys.argv[2];FREEZE=Path(sys.argv[3]);NODE=sys.argv[4] if len(sys.argv)>4 else ''
OUT=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def source_map():
    paths=[ROOT/'pyproject.toml',ROOT/'README.md']
    for area in ('pyalamode','tests','examples','editors'):
        paths.extend(p for p in (ROOT/area).rglob('*') if p.is_file() and p.suffix in ('.py','.js','.cjs','.json','.md','.txt') and '__pycache__' not in p.parts)
    result={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))}
    for suffix in ('*.py','*.js'):
        for p in OUT.glob(suffix):result['reviewer:'+p.name]=sha(p)
    return result
before=source_map();frozen=json.loads(FREEZE.read_text())
for relative,value in frozen['paths'].items():
    if sha(ROOT/relative)!=value:raise AssertionError('root frozen input differs: '+relative)
import pyalamode
installed_before={'pyalamode/'+p.name:sha(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}
if not all(before[k]==v for k,v in installed_before.items()):raise AssertionError('actual installed wheel differs')
fixture_map={}
for area in ('tests','examples','editors'):
    target=OUT/area
    if target.exists():shutil.rmtree(target)
    target.mkdir()
    for source in sorted((ROOT/area).rglob('*')):
        if not source.is_file() or '__pycache__' in source.parts or source.suffix not in ('.py','.js','.cjs','.json','.md','.txt'):continue
        relative=source.relative_to(ROOT);copy=OUT/relative;copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,copy)
        fixture_map[relative.as_posix()]=sha(copy)
        if sha(source)!=fixture_map[relative.as_posix()]:raise AssertionError('copied fixture differs '+str(relative))
if (OUT/'pyalamode').exists():raise AssertionError('outside harness must not contain a product source package')
def run(argv,child_logs=None):
    env={**os.environ,'PYTHONPATH':str(OUT)}
    if child_logs is not None:
        child_logs.mkdir();env['PYALAMODE_REVIEW_CHILD_LOG_DIR']=str(child_logs)
    else:env.pop('PYALAMODE_REVIEW_CHILD_LOG_DIR',None)
    started=time.perf_counter();ran=subprocess.run(argv,cwd=OUT,capture_output=True,text=True,env=env)
    return {'argv':argv,'status':ran.returncode,'elapsed_seconds':time.perf_counter()-started,'stdout':ran.stdout,'stderr':ran.stderr,'pythonpath':env['PYTHONPATH'],'child_log_directory':str(child_logs) if child_logs else None}
probe=run([sys.executable,str(OUT/'probe.py'),str(ROOT),NAME])
if probe['status']:
    (OUT/(NAME+'-final-incomplete.json')).write_text(json.dumps({'probe':probe},indent=2)+'\n')
    print(probe['stdout']);print(probe['stderr']);raise SystemExit(probe['status'])
child_logs=OUT/(NAME+'-suite-processes')
if child_logs.exists():shutil.rmtree(child_logs)
suite=run([sys.executable,'-m','unittest','discover','-s',str(OUT/'tests'),'-p','m*.py','-q'],child_logs)
processes=[{'record_file':p.name,'sha256':sha(p),**json.loads(p.read_text())} for p in sorted(child_logs.glob('*.json'))]
if not processes:raise AssertionError('installed-suite process provenance missing')
installed_root=Path(pyalamode.__file__).parent.resolve()
for process in processes:
    if any(Path(entry).resolve()==ROOT for entry in process['sys_path'] if entry):raise AssertionError('suite process includes checkout product root')
    for module,path in process['package_modules'].items():
        if path and not Path(path).resolve().is_relative_to(installed_root):raise AssertionError('suite process imports noninstalled product: '+module+' '+path)
if not any(process['package_modules'] for process in processes if process['argv'][0]=='-c'):raise AssertionError('actual installed child package imports missing')
for relative,value in fixture_map.items():
    if sha(OUT/relative)!=value:raise AssertionError('copied fixture changed '+relative)
match=re.search(r'Ran (\d+) tests in ([\d.]+)s',suite['stderr'])
if not match:raise AssertionError('complete suite method summary missing')
suite['tests']=int(match.group(1));suite['reported_seconds']=float(match.group(2))
client=None
if NODE:
    client_root=OUT/(NAME+'-actual-js-client')
    if client_root.exists():shutil.rmtree(client_root)
    client=run([NODE,str(OUT/'client.js'),str(ROOT),sys.executable,str(client_root),str(OUT/(NAME+'-client.json'))])
after=source_map();installed_after={'pyalamode/'+p.name:sha(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}
if before!=after or installed_before!=installed_after:raise AssertionError('final source or installed bytes changed')
for relative,value in frozen['paths'].items():
    if sha(ROOT/relative)!=value:raise AssertionError('final root frozen input differs: '+relative)
probe_path=OUT/(NAME+'-probe.json');focused=json.loads(probe_path.read_text())
if focused['unexpected']:raise AssertionError('final focused unexpected outcomes')
report={'name':NAME,'environment':{'python':sys.version,'executable':sys.executable,'platform':sys.platform,'package':pyalamode.__file__,'filesystem_encoding':sys.getfilesystemencoding(),'filesystem_errors':sys.getfilesystemencodeerrors(),'gil_enabled':sys._is_gil_enabled()},'freeze_path':str(FREEZE),'freeze_sha256':sha(FREEZE),'freeze_inputs':frozen['paths'],'source_before':before,'source_after':after,'installed_before':installed_before,'installed_after':installed_after,'copied_fixtures':fixture_map,'suite_processes':processes,'process_logger_sha256':sha(OUT/'sitecustomize.py'),'probe':probe,'focused_sha256':sha(probe_path),'focused_checks':focused['checks'],'focused_groups':[(r['name'],r['checks'],r['passed']) for r in focused['records']],'suite':suite,'client':client,'client_sha256':sha(OUT/(NAME+'-client.json')) if client else None,'harness_sha256':sha(__file__)}
target=OUT/(NAME+'-final.json');target.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'name':NAME,'focused_checks':focused['checks'],'suite_tests':suite['tests'],'suite_status':suite['status'],'client_status':client['status'] if client else None,'source_entries':len(before),'installed_files':len(installed_before),'copied_fixtures':len(fixture_map),'unchanged':True,'output':str(target)}))
sys.exit(bool(suite['status'] or (client and client['status'])))
```

`/tmp/pyalamode-m09-review/prepare.py` SHA-256 `337183d5b1c0087ee758bc7395658a1781be3df107c251d8546edbe0daa74fe1`:

```python
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve();FREEZE=Path(sys.argv[2]);OUT=Path(__file__).resolve().parent
frozen=json.loads(FREEZE.read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
for relative,value in frozen['paths'].items():
    if sha(ROOT/relative)!=value:raise AssertionError('root freeze mismatch before wheel preparation '+relative)
source=OUT/'distribution-source'
if source.exists():shutil.rmtree(source)
source.mkdir()
for name in ('pyproject.toml','README.md'):shutil.copy2(ROOT/name,source/name)
shutil.copytree(ROOT/'pyalamode',source/'pyalamode',ignore=shutil.ignore_patterns('__pycache__'))
copied={'pyalamode/'+p.name:sha(p) for p in sorted((source/'pyalamode').glob('*.py'))}
for relative,value in copied.items():
    if sha(ROOT/relative)!=value:raise AssertionError('copied package differs '+relative)
wheels=OUT/'wheels';wheels.mkdir(exist_ok=True)
argv=[str(ROOT/'.venv/bin/python'),'-m','pip','wheel','--no-index','--no-deps','--no-build-isolation',str(source),'-w',str(wheels)]
ran=subprocess.run(argv,cwd=OUT,capture_output=True,text=True)
if ran.returncode:print(ran.stdout);print(ran.stderr);raise SystemExit(ran.returncode)
wheel=next(wheels.glob('pyalamode-*.whl'))
for relative,value in frozen['paths'].items():
    if sha(ROOT/relative)!=value:raise AssertionError('root freeze mismatch after wheel preparation '+relative)
(OUT/'wheel-preparation.json').write_text(json.dumps({'argv':argv,'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'wheel':str(wheel),'wheel_sha256':sha(wheel),'copied_package':copied,'freeze_sha256':sha(FREEZE),'harness_sha256':sha(__file__)},indent=2)+'\n')
print(json.dumps({'wheel':str(wheel),'wheel_sha256':sha(wheel),'package_files':len(copied),'unchanged':True}))
```

`/tmp/pyalamode-m09-review/sitecustomize.py` SHA-256 `d1a57d52a86827bc2dc952b3cdb5bc4ed850a1f6cd3b45fc01552f63430c22a2`:

```python
"""Outside-checkout installed-suite process provenance only; no product imports."""
import atexit,json,os,sys
from pathlib import Path
_log_directory=os.environ.get("PYALAMODE_REVIEW_CHILD_LOG_DIR")
if _log_directory:
    def _record_review_process():
        modules={name:getattr(module,"__file__",None) for name,module in tuple(sys.modules.items()) if name=="pyalamode" or name.startswith("pyalamode.")}
        Path(_log_directory,str(os.getpid())+".json").write_text(json.dumps({"pid":os.getpid(),"executable":sys.executable,"argv":sys.argv,"cwd":os.getcwd(),"pythonpath":os.environ.get("PYTHONPATH"),"sys_path":sys.path,"package_modules":modules},sort_keys=True)+"\n")
    atexit.register(_record_review_process)
```

## Final frozen installed observations

Root authorized the joint freeze `/tmp/pyalamode-m09-root-freeze.json` (SHA-256 `57575e0779f28f5b4bf7b961756027fefc34ac9be1a36de48f8050ffbefeeb01`) before these runs. No product, test, example, client or published controller changed afterward. Independent review passed on a fresh native installed wheel and a fresh networking-disabled Linux installed wheel. Root retains release/acceptance authority. No correction remains open in this review.

The exact wheel is `/private/tmp/pyalamode-m09-review/wheels/pyalamode-0.1.0-py3-none-any.whl`, SHA-256 `1c58ae17c01e8fcb29976cca8252b4e0e9adbd871f4722e1bf46f88aa938e6a3`. Initial packaging stopped before candidate observation because the root interpreter lacked the declared setuptools backend. The unchanged preparation controller was rerun with build-only setuptools75.8.0 in an outside-checkout target directory through packaging PYTHONPATH. Product/controller inputs remained frozen; no application source was imported by this packaging step. `wheel-preparation.json` preserves its complete command/output and exact eighteen-file copy map. Native and Linux offline installs used this same wheel.

| Actual target | Focused assertions | Full inherited/current suite | Installed/copy identity |
| --- | ---: | --- | --- |
| Native macOS, CPython3.13.1, Clang16.0.0, standard GIL | 2,408; fifteen groups; zero unexpected | 349 methods, status0, reported18.448s | Eighteen site-packages product files, sixty-two relocated unchanged fixtures; all unchanged |
| Networking-disabled python:3.13.1-slim Linux, CPython3.13.1, GCC12.2.0, standard GIL | 2,408; same fifteen groups; zero unexpected | 349 methods, status0, reported45.824s | Same eighteen installed product bytes and sixty-two fixture bytes; all unchanged |

Counts are bounded controller assertions, including framing/envelope checks, and suite methods; they are not human repair attempts or independent empirical task-success samples. Timings describe these single correctness runs and support no performance claim. Native product imports were `/private/tmp/pyalamode-m09-review/native-venv/lib/python3.13/site-packages/pyalamode/__init__.py`; Linux imports were `/selected/lib/python3.13/site-packages/pyalamode/__init__.py`. Both reported UTF-8/surrogateescape filesystem behavior and CPython3.13.1 standard GIL.

Both final controllers verified all ninety-one root-frozen checkout inputs before/after and retained the independent eighty-seven-entry current source/controller map before/after. The independent maps are identical across platforms, canonical-map SHA-256 `95a8966582977063596c48522a91fcb436eca911eadfcb3d911c0bcc753b7609`. Installed package and copied fixture maps also match across platforms. Whole-suite discovery used relocated tests under OUT with no OUT/pyalamode product package. Sixty-seven actual nonisolated process records per platform include sixty-five product-importing processes; every observed product module remained within the selected installed site-packages path and none included the checkout root in sys.path. Isolated -I children ignore that logger: their provenance is independently established by the poisoned-workspace `-I -c` identity subprocesses, literal server/client argv, actual initialize metadata and current product-byte snapshot, with zero bootstrap sentinels.

| Fixed group, both targets passed | Assertions per target |
| --- | ---: |
| `coordinates-shared-engine` | 537 |
| `resolved-navigation` | 94 |
| `overlay-writer-policy-resolution` | 231 |
| `canonical-record-variant-case-resolution` | 124 |
| `finite-review-only-previews` | 680 |
| `wire-security-and-malformed` | 206 |
| `actual-pre-read-source-policy-symlink-ownership` | 14 |
| `actual-effects-trust-UTC-expiry` | 77 |
| `static-source-hook-nonexecution` | 46 |
| `actual-installed-bootstrap-isolation` | 81 |
| `actual-loaded-product-bytes-and-restart` | 64 |
| `captured-current-input-races-and-file-claims` | 9 |
| `actual-malformed-framing-and-lifecycle` | 45 |
| `actual-guard-authored-boundary` | 197 |
| `input-identity` | 3 |

The package-first call destination and changed str-return initializer now resolve correctly. Record/variant/case positive callers use the canonical str field; conflicting selected/open secondary int declarations retain their own per-file schema and fail PAL241, and inverted int callers fail PAL211. No nominal ambiguity obtains a successful source claim. Precise producer-specific UTF-8-byte/code-point conversion, UTF-16 navigation, CRLF/loneCR/non-ASCII/multiline/astral positions pass. Actual unsaved/versioned states, removed writers, changed policy/import inputs, expiry and race findings supersede previous successful evidence and invalidate aggregate, file and contract claims where required.

All preview expectations pass, including old-binding RHS semantics and generated-name collisions. Candidate previews remain finite, strict-project checked, read-only, and preserve the fixed effect/trust/failure/operation dimensions; the ignored update exposes its unused new value and retained original return. Reference/repaired finite fixture execution and selected generated-artifact runtime checks are explicitly separate ordinary execution probes after successful static checks. Static source/import/default/decorator/annotation/metadata and bootstrap sentinels remain absent. Ownership audits record zero outside source/policy opens, including external explanation reuse. Actual generated exports/debug nested guard failures occur before body entry and navigate to the authored boundary; off/missing/tampered/stale/coverage-forged inventories refuse. Malformed real-wire requests, current URI/file ownership, lifecycle and errors remain distinct from clean diagnostics. Ordinary generated artifacts remain Python; no certificate service, new runtime admission or M11/M14 consumer claim is introduced.

The independent actual exported JavaScript Client passed eighteen assertions over forty real wire messages using external Nodev23.5.0 and the selected fresh native installed interpreter with exact `-I -m pyalamode.editor --stdio --root <canonicalRoot>` arguments. Its poisoned workspace/startup environment resolves the same installed package and snapshot bytes; all bootstrap sentinels are absent. This proves actual client/server protocol behavior. Peer frozen Code-host API evidence below separately establishes real editor integration; Linux wire conformance does not claim a Linux GUI run. Human editor repair/usefulness remains **UNMEASURED**, zero participants/attempts.

The complete original bootstrap defect record is retained at `/tmp/pyalamode-m09-client-bootstrap-probe.json`, SHA-256 `d77167eb3480669e846906788bebae760b6b5091e889e5123825d4476b2ba3fb`: original args begin `-m` and `sentinel=true`. The final repair uses -I and does not erase this observed failure. Reviewer extraction/guard-fixture/suite-relocation corrections and earlier mutable-source outcomes remain separately disclosed above.

## Final raw outcome identities

`/tmp/pyalamode-m09-review/terminal-summary.json` SHA-256 `9fbb67b05b04153cfa70cb2bd49d7c349bb24b20204c6fbf0560035d8a9acc42` retains literal preparation/install/native/Docker commands, actual platform/interpreter/client provenance, group outcomes, full-suite stdout/stderr/status projections, map digests and a complete SHA-256/byte inventory of 212 bounded reviewer raw final wire/process/summary records, plus the four peer packet digests and actual editor/client provenance. Complete source/copy/installed maps, all literal requests/responses and source versions remain in the raw final packets; no successful evidence is reused for different inputs.

| Raw packet | SHA-256 |
| --- | --- |
| `/tmp/pyalamode-m09-review/native-frozen-final.json` | `d8c38ee66ecb8d97133aa617e53431355a2a95d595c2cda102e7e086e1712aed` |
| `/tmp/pyalamode-m09-review/native-frozen-probe.json` | `cc591dec86cba8c46f1c44332666ddf616299266f820abe2c5087fdb06b6194d` |
| `/tmp/pyalamode-m09-review/native-frozen-client.json` | `0f675547713a876e6ba7f3a41a167c5eae6ec973de53d2179062af28d12a3d26` |
| `/tmp/pyalamode-m09-review/linux-run/linux-frozen-final.json` | `93f1ecc6750407207bb6f8a2b1fe6e48f440cea3d3d3e50d435b5ca1a11ee255` |
| `/tmp/pyalamode-m09-review/linux-run/linux-frozen-probe.json` | `ebd69f8bd750e609f006939582ec79532cce11939fe4f70898d7fbf24c315729` |
| `/tmp/pyalamode-m09-review/wheel-preparation.json` | `bb5d0286742a38537268aedd1c5f1adbc9fb48e15f27b678c11606b53b5af94e` |

## Frozen peer editor/client provenance reconciliation

This reviewer read and verified the actual peer packet digests and current source maps against the same root freeze. [Client evidence](../evidence/m09-client.md) retains the complete literal host/test/package controllers and original failed development attempts. Frozen `m09-client-node.json` SHA-256 `45ae918019dd98ab1be3668f38438ef2dae68a4b95ec71c15f3f51b8de176ed8` records ten Node methods passed, zero failed/skipped, actual full wire trust/effect/nonexecution workflows and isolated bootstrap sentinels. Frozen `m09-client-package.json` SHA-256 `e4d5ffe7b5d419aa17b7d8d4ce2efc3f2f7c8e04c1331ca830117e584f0e60f0` records the deterministic VSIX, actual isolated install/list/readback of five installed files, byte-equal authored JavaScript/README and exact parsed authored manifest after only the explicitly characterized installer __metadata addition/formatting. Raw ZIP/source/installed hashes and metadata remain visible.

Frozen `m09-client-host.json` SHA-256 `f826f707b550c528ae8f649ff9c8a376ba2ef57c6ed446f70aebddbeb9de5a5d` records actual local VS Code1.139.1, embedded Nodev24.20.0, UIKind1/remoteName=null, actual Problems/hover/symbol/definition/reference/code-action/read-only diff/current edit/selected guard APIs, precise Unicode range and three false bootstrap sentinels. Its actual selected Python args include -I and its before/after/current ninety-one-input maps equal the root freeze. The initial frozen host process startup hit macOS IPC socket-length limits before a test ran; a fresh shorter isolated /tmp path ran successfully without source changes. Frozen `m09-client-restricted.json` SHA-256 `6af79523066bc2b16a0ff248195a40eea5df1ae99f125b0309a8c1855719f331` records actual trusted=false, extensionActive=true, childSentinel=false and actual_api=true, with the same before/after/current ninety-one-input maps equal to the freeze. The Development Host can activate the development module while restricted; the checked gate is no configured tool child and explicit ensure() refusal, with sentinel absence before/after. This records actual restricted-workspace behavior and claims neither an inactive module nor a Linux/remote GUI run.

Final current-map reconciliation rechecked all ninety-one root-frozen inputs, every one of the five published reviewer controllers, both installed/copy/source maps and all four peer before/after/current source maps. No unresolved M9 conformance finding remains. This review stops at the gate; root owns milestone acceptance and subsequent work. Human repair/usefulness remains **UNMEASURED** with zero participants/attempts.
