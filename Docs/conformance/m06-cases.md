# Milestone 6: independent domain and failure conformance

Status: independent review passed on the corrected root-approved M6 source freeze. Both actual platforms pass all 236 literal cases, 595 focused assertions and 242 full-suite tests; no known conformance blocker remains. The original adversarial plan below was published before implementation or approved syntax, and its prospective protocol is retained as historical review scope. Authority: `SPEC-sol6.1-composite.md`, read in full, especially §§3–5, 7–12, 16–18, A19–A20/A32 and roadmap milestone 6. Prerequisite: verified M5 commit `f6ea4c1`, with 194 tests observed by root on actual native macOS and Linux CPython 3.13.1 standard GIL builds.

This reviewer owns only this document. Product source/tests/examples, runtime contracts/measurements, milestone handoff and Git belong to their assigned workers/root. Temporary reviewer corpus, harness and package copies live outside the checkout. The review does not invoke CatWrangler, create chats, schedule work, commit, delegate or admit later milestones.

The claim remains conditional on admitted exact recursive inputs, actual callback target/capture evidence, unchanged dependencies and disclosed lifetime/ownership assumptions. Constructors preserve ordinary immutable-value invariants. Optional export/debug guards have a separate finite coverage claim. Check/build must never import or evaluate application modules, annotations, defaults, decorators, class bodies, patterns, handlers or conversion hooks. Ordinary import initialization remains separate from invocation behavior.

## Fixed plan and decision rules

The following semantic inputs and adversarial families are fixed independently before the API is ready. Literal positive sources will be instantiated only from the syntax catalog approved by root. The final document will publish every exact executed source as literal JSON, expected/observed outcomes, literal project layouts where needed, complete source maps and bounded evidence. Cases will not be weakened to match an implementation. A deliberately narrow published refusal is acceptable for an unsupported form; a false strict claim is a blocker.

| IDs | Fixed family and semantic inputs | Required outcome |
| --- | --- | --- |
| V01–V12 | Closed zero-payload and int-payload alternatives; imported/assigned/module aliases; wrong arity/field/type; stable defaults; nested tuple/Vector/record/variant payloads; mutable/capability/callable/subclass payloads | Exact declared tags and recursively immutable payloads only. Actual declaration identity and definition availability govern admission. Mutable/capability/callable data never qualify. |
| V13–V24 | Variant declaration bases/metaclass/method/property/descriptor/custom constructor; changing case set, tag and payload definitions; direct/aliased class/method/helper writers | Unknown behavior fails. Product runtime identities and finite transitive foundation reads remain current. No name-only trust or reflection loophole. |
| O01–O12 | Option absence/presence with exact int and nested data; Result success/error with independent schemas; mismatched generic payloads; ambiguous empty constructors; constructor/case equivalence | All constructor schemas, tags, equality and ordered nested contents are precise. bool does not satisfy exact int. Ordinary erased generic metadata cannot establish checked data. |
| O13–O20 | Validation over ordered inputs `(3, -1, -2, 4)` with independent errors; empty/single/multiple errors; callback unknown/effectful/concrete/captured/returned alternatives | Error accumulation preserves explicit input order and immutable errors. Callback bounds, failures, actual targets, stable captures and complete trust remain visible; unknown targets fail. |
| P01–P12 | Complete explicit cases; incomplete explicit cases; duplicate cases; false/true/data guards; guarded-only coverage; explicit wildcard; nested partial shape | A19: guards do not imply full-case coverage unless coverage is established. A complete wildcard follows the published project policy. Exhaustiveness evidence uses current declared cases. |
| P13–P24 | Capture of an already initialized parameter/local; capture repeated across cases; failed nested pattern with partial capture; guard-failed capture read; post-match read; branch merge/early return | Single assignment and definite initialization apply to Python's real scope. Failed patterns cannot supply observable partial bindings. Captures do not overwrite stable bindings. |
| P25–P36 | Unknown matcher/getter/descriptor/metaclass/value pattern; class/marker/builtin shadow; alias resolution; unsupported OR/as/star/sequence/mapping patterns; side-effecting guard | Every implicit dispatch is characterized. Unsupported syntax or unknown behavior fails before execution. No familiar spelling acquires trusted behavior. |
| F01–F12 | Direct arithmetic failure; category-specific handling; unrelated-category handler; multiple categories; nested checked call; handler guard; conditional callback; recursive call | Only covered characterized failures are discharged. Unknown/conditional callback failures remain conservative. Recursive and nested graph evidence stays precise and cannot erase a reachable category. |
| F13–F24 | Clock then division; State update then failure; IO operation and cleanup failure; nested handler failure; fallback operation failure; failure return as immutable Result data | A20: handling failures never removes already performed or declared IO/State/Clock/Random/Environment effects. Handler, guard and cleanup operations contribute their own effects/failures. |
| F25–F40 | Failure category and supported immutable fields; raw exception return/store/capture; exception `__dict__`, `__traceback__`, frames, args, repr/str hooks; target reused/read after handler/cleanup | Supported payloads are exact immutable data. Raw exception state never becomes data, callback capture or returned evidence. Exception-target binding follows its distinct cleanup lifetime. |
| F41–F48 | User raise/custom exception; general/bare except; arbitrary context manager; unknown cleanup; handler annotation/default/decorator/class/pattern sentinel | Unknown behavior remains refused despite effect declarations or apparent handling. Check/build evaluates none of the source sentinels. |
| G01–G12 | Off, selected exports and debug with nested variants/Option/Result; malformed erased payload; exact subclass; capability/callback schema; record match temporary names | Supported guards reject invalid recursive data before body entry, preserve authored boundary/path, and publish coverage. Off artifacts remain ordinary unchanged source. Guards never infer callback purity or effect/lifetime evidence. |
| C01–C12 | Case addition under cold/full-warm/partial-warm checks; removed/renamed case; wildcard under permissive policy and explicit-case policy; policy malformed/unknown selector | Relevant evidence/builds invalidate. Incomplete explicit consumers refuse after addition. Deliberate future-case wildcard semantics are preserved when policy permits; explicit policy remains enforced. Unknown selectors/policy fail tooling/refusal. |
| C13–C24 | Retained/captured/returned handler or variant callback; tighter concrete target under broader annotation; conditional alternatives; provider lending; unrelated consumer edit | Exact target, conditional status, effects, failures, captures, dependencies, retained operations and full trust survive cache serialization and partial body reuse. Reference trust remains separate from invocation effects. |
| W01–W16 | Public/private imported class/helper/method aliases; `__code__`, `setattr`, `delattr`, class dictionary; builtin/stdlib transitive foundation writers; actual runtime source bytes | Known writers invalidate relevant cold/warm consumers and builds. Implicit runtime dependency inventories reflect actual source. Label-preserving product byte changes cannot preserve stale evidence. |
| X01–X12 | Actual installed check/build/explain/audit JSON; checked denominator; unknown operation despite all effects; negative builds; unsupported target; separate import initialization | Status and evidence remain compatible with M1–M5. Audit/failed evidence is unverified. Failed publication leaves no artifact. Accepted artifacts execute under stock Python, with no loader or per-call registry. |

## Literal negative seeds fixed before API approval

These complete source strings are selected now. Their strict expected outcome is refusal; the new syntax catalog cannot license reflection, raw exception data, user raises, unknown calls or source evaluation. Diagnostic details will be recorded after implementation. They are analyzed as source text rather than executed application code.

```json
[
  {"id":"N01","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    raise ValueError(\"user\")\n"},
  {"id":"N02","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except Exception as error:\n        return error.__dict__\n"},
  {"id":"N03","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as error:\n        return error.__traceback__\n"},
  {"id":"N04","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->str:\n    try:\n        return \"ok\"\n    except ValueError as error:\n        return repr(error)\n"},
  {"id":"N05","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->str:\n    try:\n        return \"ok\"\n    except ValueError as error:\n        return str(error)\n"},
  {"id":"N06","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as error:\n        return error\n"},
  {"id":"N07","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    with unknown_context():\n        return x\n"},
  {"id":"N08","expected":1,"source":"from pyalamode import effects,IO,State,Clock,Random,Environment\n@effects(IO,State,Clock,Random,Environment)\ndef probe(x:int)->int:\n    try:\n        return unknown_operation(x)\n    except Exception:\n        return 0\n"},
  {"id":"N09","expected":1,"source":"from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        value=10//x\n    except ZeroDivisionError as error:\n        value=0\n    return error.args[0]\n"},
  {"id":"N10","expected":1,"source":"from pyalamode import fun\nfrom typing import Callable\n@fun\ndef probe(x:int)->Callable[[],int]:\n    try:\n        value=10//x\n    except ZeroDivisionError as error:\n        def retained()->int:\n            return error.args[0]\n        return retained\n    def constant()->int:\n        return value\n    return constant\n"}
]
```

## Independent execution protocol

Before final runs, the reviewer will inspect the approved catalog, relevant implementation and runtime dependency inventory. Complete literal sources and project layouts will be frozen in temporary storage; each source records expected status and required evidence. Unsupported alternatives stay explicit. Any unexpected strict admission is reported to the responsible builder/root with the literal repro, expected/observed result and current source identities.

Focused static/runtime/project/guard/cache/CLI assertions will run through the literal native `.venv/bin/python` and actual Docker `python:3.13.1-slim` with networking disabled, `PYTHONPATH=/workspace` where needed, and a current package/CLI installed when feasible. The full inherited-plus-M6 suite uses `unittest discover -s tests -p 'm*.py'`. Root independently performs its final suite/gates; this reviewer does not repeat every interim implementation run.

Runtime checks cover exact tag/payload equivalence, nested invariants, zero foreign-hook dispatch, construction/update immutability, deep stable-data snapshots and independent fresh thaw output, callback order/bounds, failure-data construction, supported guards and no runtime verification registry. Ordinary Python call-binding dispatch outside product entry remains a separately disclosed limitation where applicable. Capabilities, callables and exception objects are never admissible nested data.

Project checks cover real source graphs, import/definition availability, unchanged compatible builds, module initialization separated from invocation, authored guard paths, failed no-artifact builds, foundation writers, policy selection and cold/full-warm/partial-warm evidence. Mutating runtime product bytes for freshness probes is confined to an independent temporary package copy. No checkout product/test/example file is modified by the reviewer.

Final evidence will include every installed product Python file (including the launcher), relevant existing/new tests, examples, fixtures, benchmark/support files and reviewer harness/corpus hashes. Each platform must preserve before/after source maps; final cross-platform maps and current checkout bytes must agree. Runtime measurement correctness, current identities, actual operation costs and limitations will be independently inspected from helper evidence. Human authoring/usability and unclaimed target/platform results remain unmeasured.

## Final observations and bounded acceptance

All final runs used the corrected freeze after the contained-case writer correction. Earlier candidate results are historical. Native CPython 3.13.1 used the literal `.venv/bin/python` and its editable installed package; actual Docker `python:3.13.1-slim` used a newly built current wheel installed with `--no-index --no-deps --target /review/installed`, networking disabled and checkout mounted read-only. Every imported package Python file was compared with checkout bytes. The Linux package path was `/review/installed/pyalamode/__init__.py`; it did not import the checkout package. Both interpreters report standard GIL builds, with `Py_GIL_DISABLED=0` and the GIL enabled. Checker label: `domains-failures-6.0`; target remains CPython 3.13.1.

| Final gate, on each platform | Actual result |
| --- | --- |
| Complete source corpus | 236 unique cases: 73 admissions, 163 refusals; zero status, denominator or specified evidence mismatches |
| Runtime values and hooks | 192 assertions; zero foreign/metaclass/exception hooks |
| Source graphs, policies, callbacks and caches | 207 assertions, 28 literal project layouts, 85 recorded project checks plus failed-build/no-artifact checks |
| Actual CLI and ordinary artifacts | 76 assertions; 34 actual check/build/explain/audit CLI subprocesses and five stock-Python artifact executions, including two generated-name collision controls |
| No source execution | 78 assertions; 14 negative sentinels and one separate initialization control; every check/build leaves sentinel absent |
| Copied product byte/policy freshness | 42 assertions across 12 fresh-process transitions; mutations confined to a temporary package copy |
| Focused assertion total | 595 per platform; corpus gate is additional |
| Full inherited-plus-M6 suite | 242 tests pass: 194 inherited, 18 M6 static/project tests, 30 M6 runtime tests |
| Full source map | All 70 named inputs equal before/after, across platforms, and current checkout/harness bytes |
| Imported installed package | All 13 Python files equal before/after, across platforms and current checkout, including `__main__.py` |

The native full suite reported 3.871 seconds; Linux reported 13.905 seconds. These suite durations are observations, not comparative performance claims. Six focused drivers returned status 0 on each platform. Accepted off artifacts preserve authored source bytes and ordinary identity functions; selected export facades retain originals through `__wrapped__`; debug artifacts execute successfully. Actual guards reject wrong tags and recursively wrong Option payloads with authored `core.py` paths and argument/boundary names. Negative strict checks/builds return 1 and publish no artifact. Audit returns 0 with `verified=false`; unsupported target returns 2 with no verification. Tooling policy selectors distinguish invalid policy (2) from a valid explicit-case policy rejecting a wildcard (1).

The graph probes retain per-occurrence failure masks: the same callee handled at one call and unhandled at another keeps the reachable failure; masks from different categories cannot union away every occurrence. Covered RuntimeError includes RecursionError and covered ValueError includes UnicodeError. Conditional/captured/returned callbacks retain actual targets, full trust, conservative failures and invocation operations through full-warm and partial-warm serialization. A concrete Clock callback under a broader Clock/State annotation keeps its actual Clock behavior and concrete operation failures. A pure factory retaining a callable keeps its reference trust while remaining separate from invocation effects. Case addition invalidates an incomplete explicit consumer; a permitted deliberate wildcard preserves its authored future-case behavior. Relevant writer changes invalidate the successful claim and block guarded publication. Some private-foundation changes permit reuse of a conditionally checked consumer body (`cache_hit=true`) while failed dependencies make that consumer unverified; this is evidence invalidation, not a claim that every body must miss or that invalidation is minimal.

The runtime probes cover exact tag-sensitive/bool-sensitive equivalence, constructors and ordered match fields, immutable writes/reinitialization/subclass refusal, nested records/collections/cases, all 26 exact native exception conversion identities, fixed fresh Failure records, wrong generic payloads, left-to-right independent binary errors, zero callback/conversion hooks, data-only captures, freeze reuse and separately fresh nested thaw envelopes. Capabilities, callables, raw exceptions and foreign subclasses fail data validation. No exception args/dictionary/traceback/frames/formatting/getter is read by conversion. The exception target remains an opaque real Python exception solely inside its handler and cannot escape cleanup, become a capture or be reused as an initialized local. Handler and fallback failures remain in evidence, and performed Clock/IO/State/Random/Environment effects are never discharged by failure handling.

Fourteen authored sentinels cover function annotations/defaults/decorators, variant/case decorators and bodies, case annotations/defaults, a called variant factory, unknown pattern getter, guard, handler category/body and unknown class subscription. Checking and building execute none. The separate ordinary-initialization source checks/builds without execution and discloses unchecked initialization; a later separate stock-Python import creates its marker and calls the admitted scalar function successfully. This keeps module setup separate from invocation certification.

## Findings resolved before the final freeze

| Literal or probe | Earlier observed problem | Current result |
| --- | --- | --- |
| V28 called `@variant()` | Declaration silently disappeared from the selected denominator, status 0 | Resolved called marker opts in, noncanonical factory syntax refuses; standalone resolved `@case` also refuses |
| P42–P44 nested constrained case patterns | Multi-case nested payload was treated as irrefutable outer-case coverage, permitting a missing-result path | All refuse; P45 capture-free constraint followed by deliberate `_` admits |
| Private `_DomainType.__setattr__.__code__` writer | Tooling raised UnboundLocalError while resolving a private method reference | Clean strict refusal, dependent consumer unverified, failed build publishes nothing |
| Unused capture `_pyalamode_guard_validate` | Accepted debug artifact shadowed the generated validator and raised UnboundLocalError on valid entry | Capture/handler/global/nonlocal names participate in generated-name inventory; off/debug artifacts execute |
| D10–D22 declaration timing and class-local defaults | Earlier or current stored field defaults could shadow native annotation bindings; a same-named local default could incorrectly use a global | Ordinary AnnAssign value-before-annotation and class-suite binding order enforced; quoted/future annotations use the characterized module parser; matching positive controls admit |
| W01–W09 parent-family/nested schemas | Some/Nothing/Ok/Err behavioral writers could leave an identity-only Option/Result or nested family schema certified | Contained exact cases invalidate parent/nested schemas through public/submodule aliases; cold/full-warm checks and selected guarded builds refuse |

The original 210-case publication is unchanged: removing the 26 identified additions from the final corpus reconstructs its exact original JSON bytes/hash. A review expectation was corrected for **new, unpublished** D15/D16 controls before final publication: quoting only a later annotation does not fix `int:int=3`, because CPython stores the current default before evaluating that field's own nonpostponed annotation. Their expected result is refusal; D21/D22 quote both annotations and provide the corresponding positive controls. No original expected refusal was relaxed to accommodate an implementation, and none of the resolved false admissions remains on the final frozen source.

## Limits and actual runtime foundations

This acceptance is the published finite M6 slice. Binary positional accumulation combines two established full Result schemas with the same error schema and preserves eager Python argument order; it is not a general callback traversal or error-flattening API. Sparse constructor literals do not independently establish both Result parameters. Self/sibling/forward field references unavailable at ordinary declaration time remain refused. Matching omits OR/as/sequence/mapping/star syntax, guarded named captures and constrained named partial captures. Capture-free guards establish coverage only where the catalog proves it, currently literal True. `try` omits else/finally, broad/bare/custom handlers, user raise and arbitrary context managers. Unknown operations stay unverified even with every current effect declared. Task remains deferred.

Failure conversion accepts only the published 26 exact native identities. Ordinary except uses native subtype matching, but custom subclasses/foreign exceptions are outside the admitted builtin operation/input universe and fail conversion. Resource exhaustion, interruption and divergence are outside the finite failure bound; RecursionError remains a conservative recursive bound. General exception formatting/state inspection is unsupported. Fixed category/message data is not a complete serialization of an exception.

Source/identity evidence assumes unchanged checked dependencies, exact recursive input schemas, stable callable captures and the inherited explicit capability operation/lifetime contract. Native reflection, custom keyword binding before function entry, hostile unchecked mutation and raw exception state do not gain certification. Optional guards prove finite exact data/tag schemas only; off is default, export originals remain unguarded, and no callback/effect/lifetime registry is added. Capability/Effectful slots require complete interfaces and stable actual target evidence and remain outside data guards. Ordinary CPython can consult str-subclass keyword hashes/equality while binding `**kwargs` before a constructor enters; the runtime contract characterizes this inherited entry boundary. No free-threaded, other interpreter/version/platform or human authoring benefit claim is made, and no M10 report is required or inferred.

Independent source inspection reconciled actual variant/failure dependencies with the [runtime inventory](../evidence/m06-runtime-contract.md): product fixed closures/catalogs/metaclass/helpers; native exact `type`/`object`, slots/class creation/MATCH_CLASS and fixed `__match_args__`; named builtin tuple/dict/list/set/str traversal/construction and scalar operations; GenericAlias/GetSetDescriptorType; all 26 exact native exception identities; inherited collection/record/boundary validation, equivalence, snapshots and finite non-evaluating ast annotation parser including ast.parse/compile-with-PyCF_ONLY_AST, sys.modules/ModuleType. Public and private helper/class/method/native foundation writers are conditioned by the actual dependency gates. This remains the original tuple/slot backend with no external installed backend or license addition; stock CPython/stdlib retains its existing license. Declaration setup is ordinary module initialization and excluded from pure invocation claims.

The independent review parsed both current [runtime raw JSON files](../evidence/m06-runtime-macos.json) and [Linux raw JSON](../evidence/m06-runtime-linux.json), verified every row's correctness flag, all three observations per row, actual assertion counts, and before/after/current/cross-platform 12-product-plus-eight-owned maps against the full map below. Each platform has 36 rows, 108 intervals, 2,700 measured calls plus 360 warmups at n=10/100. Actual generated assertion counts are off 0; exports 2 or 3; debug 4, 6 or 7 according to the named workload. Separate untimed Effectful/borrowed Clock smoke returns Ok(7) or Err(IndexError data) and retains Clock. The [measurement report](../evidence/m06-runtime-measurements.md) discloses warm imports, setup excluded, GC before intervals, native/library/generated assertion work included, traced Python allocations rather than RSS, no allocation-retention inference, and uncontrolled OS/scheduling. Native matching, recursive construction and error accumulation are distinct work; the timings establish no general speedup. Source complexity includes tuple-catalog scans, recursive validation, constructor field membership and fresh thaw allocation; bounds are not constant-time claims for arbitrary payload size.

## Final complete literal source corpus

The approved-catalog initial 210 sources (67 admissions/143 refusals) were frozen before the first implementation probe, including root's F64 collision seed. Initial corpus SHA-256: `8e77bd98a56dd1b582e665cc588dd6513661d30ad8fe9bb2ce5b4a6fcc911088`. The exact 26 additions are P42–P45, D10–D22 and W01–W09. Final **236 unique sources** have **73 admissions/163 refusals**. Every expected status matches both final platforms. `selected` is the minimum denominator; `failures`, `required_effects` and `effect_bound` assert exact successful evidence when present. Sources are checked as text, never imported. The next JSON block is the entire final `literal-cases.json` contents, serialized with indent=2 and a terminal newline. Its SHA-256 is **`15cc3949409763e122db23262cf1c7a842821a9145d63286434c0daace4721bd`**.

```json
[
  {
    "id": "N01",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    raise ValueError(\"user\")\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N02",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except Exception as error:\n        return error.__dict__\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N03",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as error:\n        return error.__traceback__\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N04",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->str:\n    try:\n        return \"ok\"\n    except ValueError as error:\n        return repr(error)\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N05",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->str:\n    try:\n        return \"ok\"\n    except ValueError as error:\n        return str(error)\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N06",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as error:\n        return error\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N07",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    with unknown_context():\n        return x\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N08",
    "expected": 1,
    "source": "from pyalamode import effects,IO,State,Clock,Random,Environment\n@effects(IO,State,Clock,Random,Environment)\ndef probe(x:int)->int:\n    try:\n        return unknown_operation(x)\n    except Exception:\n        return 0\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N09",
    "expected": 1,
    "source": "from pyalamode import fun\n@fun\ndef probe(x:int)->int:\n    try:\n        value=10//x\n    except ZeroDivisionError as error:\n        value=0\n    return error.args[0]\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "N10",
    "expected": 1,
    "source": "from pyalamode import fun\nfrom typing import Callable\n@fun\ndef probe(x:int)->Callable[[],int]:\n    try:\n        value=10//x\n    except ZeroDivisionError as error:\n        def retained()->int:\n            return error.args[0]\n        return retained\n    def constant()->int:\n        return value\n    return constant\n",
    "note": "Fixed pre-approval universal negative"
  },
  {
    "id": "V01",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:int)->Lookup:\n    return Lookup.Found(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V02",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:int)->Lookup:\n    return Lookup.Found(value=x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V03",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Missing()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V04",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup.Found)->int:\n    return x.value\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V05",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(True)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V06",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found([1])\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V07",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V08",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1,2)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V09",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1,value=2)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V10",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(unknown=1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V11",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Missing(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V12",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V13",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:tuple[int,Vector[str]]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found((1,Vector[str].of(\"a\")))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V14",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[tuple[int,str]]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(Vector[tuple[int,str]].of((1,\"a\")))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V15",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(Vector[int].of(True))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V16",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:list[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found([1])\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V17",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Callable[[],int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(probe)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V18",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:ClockCapability\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(clock:ClockCapability)->Lookup:\n    return Lookup.Found(clock)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V19",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nAlias=Lookup\n@fun\ndef probe(x:int)->Lookup:\n    return Alias.Found(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V20",
    "expected": 0,
    "source": "from pyalamode import variant as closed,case as alternative,fun as checked\n@closed\nclass Lookup:\n    @alternative\n    class Found:\n        value:int\n    @alternative\n    class Missing:\n        pass\n@checked\ndef probe(x:int)->Lookup:\n    return Lookup.Found(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V21",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int=3\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V22",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int=[3]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe()->Lookup:\n    return Lookup.Found()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V23",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup(object):\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V24",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found(object):\n        value:int\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V25",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n        def changed(self):\n            return 1\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V26",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n        @property\n        def hidden(self):\n            return 1\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V27",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case()\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V28",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant()\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V29",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Found:\n        pass\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V30",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Empty:\n    pass\n",
    "note": ""
  },
  {
    "id": "V31",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        _value:int\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V32",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup(metaclass=Unknown):\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V33",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n        def __init__(self,value):\n            self.value=value\n    @case\n    class Missing:\n        pass\n",
    "note": ""
  },
  {
    "id": "V34",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nLookup.Found=Lookup.Missing\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V35",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nLookup.Found.__match_args__=(\"unknown\",)\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V36",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nAlias=Lookup.Found\nAlias.__init__.__code__=unknown\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V37",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nfrom builtins import setattr as write\nwrite(Lookup.Found,\"__match_args__\",())\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V38",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nfrom builtins import delattr as erase\nerase(Lookup,\"Found\")\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V39",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\nLookup.Found.__dict__[\"__init__\"]=unknown\n@fun\ndef probe()->Lookup:\n    return Lookup.Found(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V40",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@variant\nclass Outer:\n    @case\n    class Value:\n        item:Lookup\n@fun\ndef probe(x:int)->Outer:\n    return Outer.Value(Lookup.Found(x))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V41",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Payload:\n    number:int\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Payload\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:int)->Lookup:\n    return Lookup.Found(Payload(x))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "V42",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    return id(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O01",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Option[int]:\n    return Some(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O02",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Nothing()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O03",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Vector[int])->Option[Vector[int]]:\n    return Some(value=x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O04",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Result[int,str]:\n    return Ok(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O05",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(e:str)->Result[int,str]:\n    return Err(error=e)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O06",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Some(True)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O07",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Result[int,str]:\n    return Ok(\"wrong\")\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O08",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Result[int,str]:\n    return Err(3)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O09",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Some()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O10",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Nothing(1)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O11",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Some(1,2)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O12",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Some(1,value=2)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O13",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Option[int]()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O14",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Result[int,str]:\n    return Result[int,str]()\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O15",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Option[int]:\n    return Some([1])\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O16",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[ClockCapability])->int:\n    return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O17",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[int,Callable[[],int]])->int:\n    return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O18",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[list[int]])->int:\n    return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O19",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Option[int],b:Option[int])->bool:\n    return a==b\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O20",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str],b:Result[int,str])->bool:\n    return a!=b\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O21",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Option[int],b:Option[bool])->bool:\n    return a==b\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O22",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str],b:Result[str,str])->Result[tuple[int,str],Vector[str]]:\n    return accumulate(a,b)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O23",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Result[tuple[int,int],Vector[str]]:\n    return accumulate(Ok(1),Ok(2))\n",
    "note": "No established complete Result input schemas",
    "selected": 1
  },
  {
    "id": "O24",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Result[tuple[int,int],Vector[str]]:\n    return accumulate(Err(\"left\"),Err(\"right\"))\n",
    "note": "No established complete Result input schemas",
    "selected": 1
  },
  {
    "id": "O25",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str],b:Result[int,int])->Result[tuple[int,int],Vector[str]]:\n    return accumulate(a,b)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O26",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str])->Result[tuple[int,int],Vector[str]]:\n    return accumulate(a)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O27",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str])->Result[tuple[int,int],Vector[str]]:\n    return accumulate(a,a,a)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O28",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str])->Result[tuple[int,int],Vector[str]]:\n    return accumulate(left=a,right=a)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O29",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(a:Result[int,str])->Result[tuple[int,int],Vector[str]]:\n    return accumulate(a,unknown(a))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O30",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[Option[int]])->Option[Option[int]]:\n    return x\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O31",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[Option[int],Vector[str]])->Result[Option[int],Vector[str]]:\n    return x\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "O32",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[int,str])->str:\n    return x.error\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P01",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P02",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P03",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P04",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found():\n            return 1\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P05",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup,flag:bool)->int:\n    match x:\n        case Lookup.Found() if flag:\n            return 1\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P06",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup,flag:bool)->int:\n    match x:\n        case Lookup.Found() if flag:\n            return 1\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P07",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found() if True:\n            return 1\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P08",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found() if False:\n            return 1\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P09",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number) if True:\n            return number\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P10",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup,number:int)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P11",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    number=4\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P12",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=0):\n            return 1\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P13",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=0):\n            return 1\n        case Lookup.Found():\n            return 2\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P14",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            selected=number\n        case Lookup.Missing():\n            pass\n    return selected\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P15",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            selected=number\n        case Lookup.Missing():\n            selected=0\n    return selected\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P16",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            pass\n        case Lookup.Missing():\n            pass\n    return number\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P17",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number) if number>0:\n            return number\n        case _:\n            return number\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P18",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(unknown=number):\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P19",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(number,value=other):\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P20",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(number,other):\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P21",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Unknown(value=number):\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P22",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found()|Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P23",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case [number]:\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P24",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case {\"value\":number}:\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P25",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found() if unknown_guard():\n            return 1\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P26",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n        case Nothing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P27",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P28",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[int,str])->int:\n    match x:\n        case Ok(value=number):\n            return number\n        case Err(error=problem):\n            return len(problem)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P29",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[int,str])->int:\n    match x:\n        case Ok(value=number):\n            return number\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P30",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:bool)->int:\n    match x:\n        case True:\n            return 1\n        case False:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P31",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:bool)->int:\n    match x:\n        case True:\n            return 1\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P32",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:bool)->int:\n    match x:\n        case 1:\n            return 1\n        case 0:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P33",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:None)->int:\n    match x:\n        case None:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P34",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    match x:\n        case 1:\n            return 1\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P35",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Payload:\n    number:int\n@fun\ndef probe(x:Payload)->int:\n    match x:\n        case Payload(number=n):\n            return n\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P36",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Payload:\n    number:int\n@fun\ndef probe(x:Payload)->int:\n    match x:\n        case Payload(number=0):\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P37",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Pair:\n    @case\n    class Data:\n        first:int\n        second:int\n@fun\ndef probe(x:Pair)->int:\n    match x:\n        case Pair.Data(first=number,second=0):\n            return number\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P38",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Pair:\n    @case\n    class Data:\n        first:int\n        second:int\n@fun\ndef probe(x:Pair)->int:\n    match x:\n        case Pair.Data(first=number,second=number):\n            return number\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P39",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Pair:\n    @case\n    class Data:\n        first:int\n        second:int\n@fun\ndef probe(x:Pair)->int:\n    match x:\n        case Pair.Data(first=number,second=other):\n            return number+other\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P40",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup,Lookup:int)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P41",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found() as whole:\n            return 1\n        case _:\n            return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "P42",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@variant\nclass Outer:\n    @case\n    class Value:\n        item:Lookup\n@fun\ndef probe(x:Outer)->int:\n    match x:\n        case Outer.Value(item=Lookup.Found(value=number)):\n            return number\n",
    "note": "Nested class pattern narrows a multi-case payload and cannot fully cover the outer case",
    "selected": 1
  },
  {
    "id": "P43",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@variant\nclass Outer:\n    @case\n    class Value:\n        item:Lookup\n@fun\ndef probe(x:Outer)->int:\n    match x:\n        case Outer.Value(item=Lookup.Found(value=number)):\n            return number\n        case _:\n            return 0\n",
    "note": "A nested constrained payload pattern cannot expose named captures",
    "selected": 1
  },
  {
    "id": "P44",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@variant\nclass Outer:\n    @case\n    class Value:\n        item:Lookup\n@fun\ndef probe(x:Outer)->int:\n    match x:\n        case Outer.Value(item=Lookup.Found()):\n            return 1\n",
    "note": "Capture-free nested constrained payload is not full outer-case coverage",
    "selected": 1
  },
  {
    "id": "P45",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n@variant\nclass Outer:\n    @case\n    class Value:\n        item:Lookup\n@fun\ndef probe(x:Outer)->int:\n    match x:\n        case Outer.Value(item=Lookup.Found()):\n            return 1\n        case _:\n            return 0\n",
    "note": "Capture-free constrained nested pattern is usable with deliberate final wildcard",
    "selected": 1
  },
  {
    "id": "F01",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F02",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except IndexError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F03",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ValueError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F04",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except Exception:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F05",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except BaseException:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F06",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except UnknownError:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F07",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        failure=failure_value(caught)\n        return Err(failure)\n",
    "note": "",
    "selected": 1,
    "failures": [
      "RecursionError"
    ]
  },
  {
    "id": "F08",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->str:\n    try:\n        return \"ok\"\n    except ValueError as caught:\n        return failure_value(caught).category\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F09",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->str:\n    try:\n        return \"ok\"\n    except ValueError as caught:\n        failure=failure_value(caught)\n        return failure.message\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F10",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F11",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except* ZeroDivisionError:\n        result=0\n    return result\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F12",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        value=10//x\n    except ZeroDivisionError:\n        return 0\n    else:\n        return value\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F13",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    finally:\n        pass\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F14",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except (ValueError,UnicodeError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F15",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except (RuntimeError,RecursionError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F16",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError:\n        return 0\n    except ZeroDivisionError:\n        return 1\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F17",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except (ZeroDivisionError,IndexError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F18",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int,caught:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as caught:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F19",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        value=10//x\n    except ZeroDivisionError:\n        value=0\n    return value\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F20",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        value=10//x\n    except ZeroDivisionError:\n        return value\n    return value\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F21",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as caught:\n        pass\n    return caught\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F22",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as caught:\n        pass\n    caught=1\n    return caught\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F23",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return caught\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F24",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return caught.args\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F25",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return caught.__dict__\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F26",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return caught.__traceback__\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F27",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return str(caught)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F28",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return repr(caught)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F29",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return (caught,)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F30",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return Some(caught)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F31",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return failure_value((caught,))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F32",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        return getattr(caught,\"args\")\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F33",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        alias=caught\n        return failure_value(alias)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F34",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Callable[[],Failure]:\n    try:\n        return unknown()\n    except ValueError as caught:\n        def retained()->Failure:\n            return failure_value(caught)\n        return retained\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F35",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    return failure_value(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F36",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Failure:\n    return failure_value(ValueError(\"x\"))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F37",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Failure:\n    return Failure(category=\"ValueError\",message=\"data only\")\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F38",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe()->Failure:\n    return Failure(category=True,message=\"bad\")\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F39",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError:\n        return 1//x\n",
    "note": "",
    "selected": 1,
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F40",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        try:\n            return 10//x\n        except ZeroDivisionError:\n            return 1//x\n    except ZeroDivisionError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F41",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(op:Callable[[int],int],x:int)->int:\n    try:\n        return op(x)\n    except ZeroDivisionError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "IndexError",
      "KeyError",
      "RecursionError",
      "ValueError"
    ]
  },
  {
    "id": "F42",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(op:Callable[[int],int],x:int)->int:\n    try:\n        return op(x)\n    except RuntimeError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "IndexError",
      "KeyError",
      "ValueError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F43",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(op:Callable[[int],int],x:int)->int:\n    try:\n        return op(x)\n    except ValueError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "IndexError",
      "KeyError",
      "RecursionError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F44",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef divide(x:int)->int:\n    return 10//x\n@fun\ndef probe(x:int)->int:\n    try:\n        return divide(x)\n    except ZeroDivisionError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F45",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef divide(x:int)->int:\n    return 10//x\n@fun\ndef probe(x:int)->int:\n    first=divide(x)\n    try:\n        return divide(first)\n    except ZeroDivisionError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F46",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef divide(x:int)->int:\n    return 10//x\n@fun\ndef probe(x:int)->int:\n    try:\n        return divide(x)\n    except IndexError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F47",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef divide(x:int)->int:\n    return 10//x\n@fun\ndef probe(x:int)->int:\n    try:\n        return divide(x)\n    except ZeroDivisionError:\n        return divide(x)\n",
    "note": "",
    "selected": 1,
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F48",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef divide(x:int)->int:\n    return 10//x\n@fun\ndef probe(x:int)->int:\n    try:\n        return divide(x)\n    except (ZeroDivisionError,RuntimeError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F49",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability,x:int)->int:\n    try:\n        stamp=cap.now_ns()\n        return 10//x\n    except (IndexError,RuntimeError,OSError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "required_effects": [
      "Clock"
    ],
    "effect_bound": [
      "Clock"
    ]
  },
  {
    "id": "F49u",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(cap:ClockCapability,x:int)->int:\n    try:\n        stamp=cap.now_ns()\n        return 10//x\n    except (IndexError,RuntimeError,OSError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F50",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(State)\ndef probe(cap:StateCapability,x:int)->int:\n    try:\n        cap.set(3)\n        return 10//x\n    except (RuntimeError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "required_effects": [
      "State"
    ],
    "effect_bound": [
      "State"
    ]
  },
  {
    "id": "F50u",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(cap:StateCapability,x:int)->int:\n    try:\n        cap.set(3)\n        return 10//x\n    except (RuntimeError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F51",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(IO)\ndef probe(cap:IOCapability,x:int)->int:\n    try:\n        text=cap.read_text(\"x.txt\")\n        return 10//x\n    except (OSError,UnicodeError,RuntimeError,KeyError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "required_effects": [
      "IO"
    ],
    "effect_bound": [
      "IO"
    ]
  },
  {
    "id": "F51u",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(cap:IOCapability,x:int)->int:\n    try:\n        text=cap.read_text(\"x.txt\")\n        return 10//x\n    except (OSError,UnicodeError,RuntimeError,KeyError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F52",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(Random)\ndef probe(cap:RandomCapability,x:int)->int:\n    try:\n        number=cap.below(3)\n        return 10//x\n    except (ValueError,RuntimeError,OSError,IndexError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "required_effects": [
      "Random"
    ],
    "effect_bound": [
      "Random"
    ]
  },
  {
    "id": "F52u",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(cap:RandomCapability,x:int)->int:\n    try:\n        number=cap.below(3)\n        return 10//x\n    except (ValueError,RuntimeError,OSError,IndexError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F53",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(Environment)\ndef probe(cap:EnvironmentCapability,x:int)->int:\n    try:\n        text=cap.get(\"MODE\",\"\")\n        return 10//x\n    except (ValueError,RuntimeError,OSError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "required_effects": [
      "Environment"
    ],
    "effect_bound": [
      "Environment"
    ]
  },
  {
    "id": "F53u",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(cap:EnvironmentCapability,x:int)->int:\n    try:\n        text=cap.get(\"MODE\",\"\")\n        return 10//x\n    except (ValueError,RuntimeError,OSError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F54",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int,ValueError:int)->int:\n    try:\n        return x\n    except ValueError:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F55",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nValueError=int\n@fun\ndef probe(x:int)->int:\n    try:\n        return x\n    except ValueError:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F56",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport builtins\nbuiltins.ZeroDivisionError=Exception\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError:\n        return 0\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F57",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom builtins import ZeroDivisionError as DivFailure\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except DivFailure:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F58",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(Clock)\ndef probe(cap:ClockCapability,x:int)->int:\n    try:\n        with borrow(cap) as scoped:\n            return scoped.now_ns()//x\n    except (RuntimeError,OSError,IndexError,ZeroDivisionError):\n        return 0\n",
    "note": "",
    "selected": 1,
    "required_effects": [
      "Clock"
    ],
    "failures": []
  },
  {
    "id": "F59",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError as caught:\n        caught=1\n        return caught\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F60",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Failure:\n    try:\n        return Failure(\"x\",\"y\")\n    except ValueError as caught:\n        def capture()->Failure:\n            return Failure(\"x\",\"y\")\n        return failure_value(caught)\n    return failure_value(caught)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "H01",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(op:Callable[[int],Result[int,str]],x:int)->Result[tuple[int,int],Vector[str]]:\n    left=op(x)\n    right=op(x+1)\n    return accumulate(left,right)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "H02",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->Result[tuple[int,int],Vector[str]]:\n    left=unknown(x)\n    return accumulate(left,Ok(x))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "H03",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef validate(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x)\n@fun\ndef probe(x:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(x),validate(x+1))\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "H04",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(Clock)\ndef validate(cap:ClockCapability,x:int)->Result[int,str]:\n    stamp=cap.now_ns()\n    return Ok(x+stamp)\n@effects(Clock)\ndef probe(cap:ClockCapability,x:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(cap,x),validate(cap,x+1))\n",
    "note": "",
    "selected": 2,
    "required_effects": [
      "Clock"
    ]
  },
  {
    "id": "H05",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@effects(Clock)\ndef validate(cap:ClockCapability,x:int)->Result[int,str]:\n    stamp=cap.now_ns()\n    return Ok(x+stamp)\n@fun\ndef probe(cap:ClockCapability,x:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(cap,x),validate(cap,x+1))\n",
    "note": "",
    "selected": 2
  },
  {
    "id": "H06",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef validate(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x)\n@fun\ndef probe(values:Vector[int])->Vector[Result[int,str]]:\n    return values.map(validate)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "H07",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(values:Vector[int])->Vector[Result[int,str]]:\n    return values.map(unknown)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "F61",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef dual(values:Vector[int],index:int,denominator:int)->int:\n    return values[index]//denominator\n@fun\ndef probe(values:Vector[int],index:int,denominator:int)->int:\n    try:\n        first=dual(values,index,denominator)\n    except ZeroDivisionError:\n        return 0\n    try:\n        return dual(values,index,first)\n    except IndexError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": [
      "IndexError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F62",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef dual(values:Vector[int],index:int,denominator:int)->int:\n    return values[index]//denominator\n@fun\ndef probe(values:Vector[int],index:int,denominator:int)->int:\n    try:\n        try:\n            return dual(values,index,denominator)\n        except ZeroDivisionError:\n            return 0\n    except IndexError:\n        return 0\n",
    "note": "",
    "selected": 1,
    "failures": []
  },
  {
    "id": "F63",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef dual(values:Vector[int],index:int,denominator:int)->int:\n    return values[index]//denominator\n@fun\ndef probe(values:Vector[int],index:int,denominator:int)->int:\n    try:\n        return dual(values,index,denominator)\n    except (IndexError,ZeroDivisionError):\n        return dual(values,index,denominator)\n",
    "note": "",
    "selected": 1,
    "failures": [
      "IndexError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "F64",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:int)->int:\n    try:\n        caught=3\n        return 10//x\n    except ZeroDivisionError as caught:\n        return 0\n",
    "note": "Exception target must not overwrite any potential try-body binding",
    "selected": 1
  },
  {
    "id": "D01",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Lookup.Missing\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D02",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Lookup.Found\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D03",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:\"Lookup.Missing\"\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D04",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:\"Found\"\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D05",
    "expected": 1,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Lookup.Missing\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D06",
    "expected": 1,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Lookup.Found\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D07",
    "expected": 1,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Found\n    @case\n    class Missing:\n        pass\n",
    "note": "Domain binding unavailable while nested case decorator executes"
  },
  {
    "id": "D08",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Later\n    @case\n    class Missing:\n        pass\n@record\nclass Later:\n    value:int\n",
    "note": "Forward external record unavailable at ordinary declaration execution"
  },
  {
    "id": "D09",
    "expected": 0,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Payload:\n    number:int\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Payload\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Payload)->Lookup:\n    return Lookup.Found(x)\n",
    "note": "",
    "selected": 1
  },
  {
    "id": "D10",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class case:\n        pass\n    @case\n    class Missing:\n        pass\n",
    "note": "Earlier outer class case binding shadows the later decorator"
  },
  {
    "id": "D11",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Pair:\n    int:int=3\n    value:int=4\n",
    "note": "Actual class-local default shadows a later nonpostponed annotation"
  },
  {
    "id": "D12",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Pair:\n        int:int=3\n        value:int=4\n",
    "note": "Actual case-local default shadows a later nonpostponed annotation"
  },
  {
    "id": "D13",
    "expected": 0,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Pair:\n    int:int=3\n    value:int=4\n",
    "note": "Closed postponed parser resolves annotation from module namespace"
  },
  {
    "id": "D14",
    "expected": 0,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Pair:\n        int:int=3\n        value:int=4\n",
    "note": "Closed postponed parser resolves case annotation from module namespace"
  },
  {
    "id": "D15",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Pair:\n    int:int=3\n    value:\"int\"=4\n",
    "note": "Current field default is stored before its own nonpostponed annotation; quoting only the later field does not repair it"
  },
  {
    "id": "D16",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Pair:\n        int:int=3\n        value:\"int\"=4\n",
    "note": "Current case field default is stored before its own nonpostponed annotation"
  },
  {
    "id": "D17",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nTOKEN=4\n@record\nclass Pair:\n    TOKEN:bool=True\n    value:int=TOKEN\n",
    "note": "Class-local default must not silently resolve same-named global"
  },
  {
    "id": "D18",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nTOKEN=4\n@variant\nclass Lookup:\n    @case\n    class Pair:\n        TOKEN:bool=True\n        value:int=TOKEN\n",
    "note": "Case-local default must not silently resolve same-named global"
  },
  {
    "id": "D19",
    "expected": 1,
    "source": "from __future__ import annotations\nfrom pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nTOKEN=4\n@record\nclass Pair:\n    TOKEN:bool=True\n    value:int=TOKEN\n",
    "note": "Postponement does not change ordinary default lookup"
  },
  {
    "id": "D20",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class int:\n        pass\n    @case\n    class Found:\n        value:int\n",
    "note": "Outer class locals do not enclose the nested case class annotation lookup"
  },
  {
    "id": "D21",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Pair:\n    int:\"int\"=3\n    value:\"int\"=4\n",
    "note": "Both closed quoted annotations resolve from module namespace"
  },
  {
    "id": "D22",
    "expected": 0,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Lookup:\n    @case\n    class Pair:\n        int:\"int\"=3\n        value:\"int\"=4\n",
    "note": "Both closed quoted case annotations resolve from module namespace"
  },
  {
    "id": "W01",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[int])->Option[int]:\n    return x\nSome.__setattr__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W02",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[int])->Option[int]:\n    return x\nNothing.__eq__.__code__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W03",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[int,str])->Result[int,str]:\n    return x\nOk.__setattr__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W04",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Result[int,str])->Result[int,str]:\n    return x\nErr.__init__.__code__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W05",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Vector[Option[int]])->Vector[Option[int]]:\n    return x\nSome.__setattr__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W06",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:tuple[Result[int,str]])->tuple[Result[int,str]]:\n    return x\nOk.__setattr__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W07",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@fun\ndef probe(x:Option[int])->Option[int]:\n    return x\nfrom pyalamode.variants import Some as Alias\nAlias.__setattr__=unknown\n",
    "note": "Parent family and nested admitted schemas depend on every contained exact case definition",
    "selected": 1
  },
  {
    "id": "W08",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@record\nclass Payload:\n    option:Option[int]\n@fun\ndef probe(x:Payload)->Payload:\n    return x\nSome.__setattr__=unknown\n",
    "note": "Record field parent-family dependency",
    "selected": 1
  },
  {
    "id": "W09",
    "expected": 1,
    "source": "from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n@variant\nclass Domain:\n    @case\n    class Payload:\n        option:Option[int]\n@fun\ndef probe(x:Domain)->Domain:\n    return x\nSome.__setattr__=unknown\n",
    "note": "Variant field parent-family dependency",
    "selected": 1
  }
]
```

## Complete literal status observations

The precise evidence predicates in the source corpus passed as well as these statuses/denominators. Rules are the native observed diagnostic set; platform path strings and timings do not affect the status claim.

```json
[
  {
    "id": "N01",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL110",
      "PAL211"
    ]
  },
  {
    "id": "N02",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "N03",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "N04",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "N05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "N06",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "N07",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL320"
    ]
  },
  {
    "id": "N08",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240",
      "PAL340"
    ]
  },
  {
    "id": "N09",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL101",
      "PAL102",
      "PAL201",
      "PAL211"
    ]
  },
  {
    "id": "N10",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 3,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL240"
    ]
  },
  {
    "id": "V01",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V02",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V03",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V04",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V06",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V07",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V08",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V09",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V10",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V11",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V12",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230"
    ]
  },
  {
    "id": "V13",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V14",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V15",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "V16",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V17",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V18",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240",
      "PAL310"
    ]
  },
  {
    "id": "V19",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V20",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V21",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V22",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL221",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V23",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V24",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V25",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V26",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V27",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V28",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V29",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL101"
    ]
  },
  {
    "id": "V30",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V31",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V32",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V33",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "V34",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V35",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V36",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V37",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V38",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V39",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL201",
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "V40",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V41",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "V42",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "O01",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O02",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O03",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O04",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O05",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O06",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211"
    ]
  },
  {
    "id": "O07",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211"
    ]
  },
  {
    "id": "O08",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211"
    ]
  },
  {
    "id": "O09",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O10",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O11",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O12",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O13",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL230"
    ]
  },
  {
    "id": "O14",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL230"
    ]
  },
  {
    "id": "O15",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O16",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "O17",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "O18",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "O19",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O20",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O21",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL210",
      "PAL211"
    ]
  },
  {
    "id": "O22",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O23",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O24",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O25",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O26",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O27",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O28",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "O29",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "O30",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O31",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "O32",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211"
    ]
  },
  {
    "id": "P01",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P02",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P03",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P04",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P06",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P07",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P08",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P09",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P10",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL101"
    ]
  },
  {
    "id": "P11",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL101"
    ]
  },
  {
    "id": "P12",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P13",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P14",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211"
    ]
  },
  {
    "id": "P15",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P16",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211"
    ]
  },
  {
    "id": "P17",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P18",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P19",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P20",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P21",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P22",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P23",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P24",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P25",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL210",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "P26",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P27",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P28",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P29",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P30",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P31",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P32",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P33",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P34",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P35",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P36",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P37",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P38",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P39",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "P40",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL330"
    ]
  },
  {
    "id": "P41",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P42",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P43",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P44",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL330"
    ]
  },
  {
    "id": "P45",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F01",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F02",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F03",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F04",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F06",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F07",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F08",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F09",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F10",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F11",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL110",
      "PAL211"
    ]
  },
  {
    "id": "F12",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F13",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F14",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F15",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F16",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F17",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F18",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL101"
    ]
  },
  {
    "id": "F19",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL101"
    ]
  },
  {
    "id": "F20",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211"
    ]
  },
  {
    "id": "F21",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211"
    ]
  },
  {
    "id": "F22",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL102",
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F23",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F24",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F25",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F26",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL201",
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F27",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "F28",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "F29",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL340"
    ]
  },
  {
    "id": "F30",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL340"
    ]
  },
  {
    "id": "F31",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "F32",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "F33",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL340"
    ]
  },
  {
    "id": "F34",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 2,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "F35",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "F36",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "F37",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F38",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "F39",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F40",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F41",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F42",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F43",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F44",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F45",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F46",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F47",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F48",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F49",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F49u",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL310"
    ]
  },
  {
    "id": "F50",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F50u",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL310"
    ]
  },
  {
    "id": "F51",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F51u",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL310"
    ]
  },
  {
    "id": "F52",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F52u",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL310"
    ]
  },
  {
    "id": "F53",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F53u",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL310"
    ]
  },
  {
    "id": "F54",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F55",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F56",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL340"
    ]
  },
  {
    "id": "F57",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F58",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "F59",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL340"
    ]
  },
  {
    "id": "F60",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 2,
    "rules": [
      "PAL211",
      "PAL221"
    ]
  },
  {
    "id": "H01",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "H02",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL230",
      "PAL240"
    ]
  },
  {
    "id": "H03",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "H04",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "H05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 2,
    "rules": [
      "PAL310"
    ]
  },
  {
    "id": "H06",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "H07",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL211",
      "PAL221",
      "PAL240"
    ]
  },
  {
    "id": "F61",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F62",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F63",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 2,
    "rules": []
  },
  {
    "id": "F64",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL101"
    ]
  },
  {
    "id": "D01",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D02",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D03",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D04",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D06",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D07",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D08",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130"
    ]
  },
  {
    "id": "D09",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 1,
    "rules": []
  },
  {
    "id": "D10",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL120"
    ]
  },
  {
    "id": "D11",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130",
      "PAL221"
    ]
  },
  {
    "id": "D12",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130",
      "PAL221"
    ]
  },
  {
    "id": "D13",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 0,
    "rules": []
  },
  {
    "id": "D14",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 0,
    "rules": []
  },
  {
    "id": "D15",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130",
      "PAL221"
    ]
  },
  {
    "id": "D16",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL130",
      "PAL221"
    ]
  },
  {
    "id": "D17",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL221"
    ]
  },
  {
    "id": "D18",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL221"
    ]
  },
  {
    "id": "D19",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 0,
    "rules": [
      "PAL221"
    ]
  },
  {
    "id": "D20",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 0,
    "rules": []
  },
  {
    "id": "D21",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 0,
    "rules": []
  },
  {
    "id": "D22",
    "expected": 0,
    "native": 0,
    "linux": 0,
    "selected": 0,
    "rules": []
  },
  {
    "id": "W01",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W02",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W03",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W04",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W05",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W06",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W07",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W08",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  },
  {
    "id": "W09",
    "expected": 1,
    "native": 1,
    "linux": 1,
    "selected": 1,
    "rules": [
      "PAL130",
      "PAL211"
    ]
  }
]
```

## Complete literal project layouts

These 28 projects include every policy and writer source and each source transition. Sequence expectations mean cold, full warm, then the named transition; writer projects additionally recheck fresh source and attempt a guarded build, which must leave no artifact. Callback partial-warm projects change only their consumer as recorded. The separate complete driver below contains every asserted evidence field and build step.

```json
[
  {
    "id": "case-add-explicit",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n"
    },
    "transition": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n    @case\n    class Pending:\n        code:str\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "case-add-wildcard",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case _:\n            return 0\n"
    },
    "transition": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n    @case\n    class Pending:\n        code:str\n"
    },
    "expected": [
      0,
      0,
      0
    ]
  },
  {
    "id": "explicit wildcard",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case _:\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=[\"domain:Lookup\"]\n"
    },
    "expected": 1
  },
  {
    "id": "explicit complete",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=[\"domain:Lookup\"]\n"
    },
    "expected": 0
  },
  {
    "id": "unknown selector",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=[\"domain:Unknown\"]\n"
    },
    "expected": 2
  },
  {
    "id": "wrong type",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=3\n"
    },
    "expected": 2
  },
  {
    "id": "unknown module",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=[\"unknown:Lookup\"]\n"
    },
    "expected": 2
  },
  {
    "id": "malformed selector",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=[\"domain.Lookup\"]\n"
    },
    "expected": 2
  },
  {
    "id": "duplicate selector",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nexplicit_cases=[\"domain:Lookup\",\"domain:Lookup\"]\n"
    },
    "expected": 2
  },
  {
    "id": "returned handler partial warm",
    "files": {
      "leaf.py": "# mode: fun\ndef divide(x:int)->int:\n    return 10//x\n",
      "factory.py": "# mode: fun\nfrom typing import Callable\nfrom leaf import divide\ndef maker()->Callable[[int],int]:\n    def handled(x:int)->int:\n        try:\n            return divide(x)\n        except ZeroDivisionError:\n            return 0\n    return handled\n",
      "consumer.py": "# mode: fun\nfrom factory import maker\ndef invoke(x:int)->int:\n    return maker()(x)\n"
    },
    "transition": {
      "consumer.py": "# mode: fun\nfrom factory import maker\ndef invoke(x:int)->int:\n    return maker()(x)\n\n# independent consumer edit\n"
    },
    "expected": [
      0,
      0,
      0
    ]
  },
  {
    "id": "tighter concrete handled clock partial warm",
    "files": {
      "leaf.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\n@effects(Clock)\ndef timed(cap:ClockCapability,x:int)->int:\n    try:\n        return cap.now_ns()//x\n    except ZeroDivisionError:\n        return 0\n",
      "factory.py": "# mode: fun\nfrom pyalamode import Effectful,Clock,State,ClockCapability\nfrom leaf import timed\ndef maker()->Effectful[[ClockCapability,int],int,Clock,State]:\n    return timed\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\n@effects(Clock)\ndef invoke(cap:ClockCapability,x:int)->int:\n    return maker()(cap,x)\n"
    },
    "transition": {
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\n@effects(Clock)\ndef invoke(cap:ClockCapability,x:int)->int:\n    return maker()(cap,x)\n\n# independent edit\n"
    },
    "expected": [
      0,
      0,
      0
    ]
  },
  {
    "id": "conditional captured handler",
    "files": {
      "leaf.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\n@effects(Clock)\ndef timed(cap:ClockCapability,x:int)->int:\n    try:\n        return cap.now_ns()//x\n    except ZeroDivisionError:\n        return 0\n",
      "factory.py": "# mode: fun\nfrom pyalamode import effects,Effectful,Clock,ClockCapability\ndef maker(op:Effectful[[ClockCapability,int],int,Clock])->Effectful[[ClockCapability,int],int,Clock]:\n    @effects(Clock)\n    def handled(cap:ClockCapability,x:int)->int:\n        try:\n            return op(cap,x)\n        except RuntimeError:\n            return 0\n    return handled\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\nfrom leaf import timed\n@effects(Clock)\ndef invoke(cap:ClockCapability,x:int)->int:\n    return maker(timed)(cap,x)\n"
    },
    "transition": {
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\nfrom leaf import timed\n@effects(Clock)\ndef invoke(cap:ClockCapability,x:int)->int:\n    return maker(timed)(cap,x)\n\n# independent body reuse probe\n"
    },
    "expected": [
      0,
      0,
      0
    ]
  },
  {
    "id": "retained variant callable",
    "files": {
      "leaf.py": "# mode: fun\nfrom pyalamode import Option,Some\ndef present(x:int)->Option[int]:\n    return Some(x)\n",
      "factory.py": "# mode: fun\nfrom pyalamode import Option\nfrom typing import Callable\nfrom leaf import present\ndef maker()->Callable[[int],Option[int]]:\n    return present\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option\nfrom factory import maker\ndef invoke(values:Vector[int])->Vector[Option[int]]:\n    return values.map(maker())\n"
    },
    "transition": {
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option\nfrom factory import maker\ndef invoke(values:Vector[int])->Vector[Option[int]]:\n    return values.map(maker())\n\n# independent body reuse probe\n"
    },
    "expected": [
      0,
      0,
      0
    ]
  },
  {
    "id": "case class method",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from domain import Lookup\nLookup.Found.__init__.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "case imported assigned alias",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from domain import Lookup\nAlias=Lookup.Found\nAlias.__match_args__=()\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "case setter alias",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from domain import Lookup\nfrom builtins import setattr as write\nwrite(Lookup.Found,\"__match_args__\",())\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "private variant helper",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode.variants import _case_info as helper\nhelper.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "private variant metaclass method",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode.variants import _DomainType\n_DomainType.__setattr__.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "private failure helper",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Result,Ok,Err,Failure,failure_value\ndef probe(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode.failures import failure_value as helper\nhelper.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "failure record method",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Result,Ok,Err,Failure,failure_value\ndef probe(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode import Failure\nFailure.__init__.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "failure builtin native identity",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Result,Ok,Err,Failure,failure_value\ndef probe(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "import builtins\nbuiltins.ZeroDivisionError=Exception\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "variant GenericAlias identity",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "import types\ntypes.GenericAlias=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "variant descriptor foundation",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom domain import Lookup\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=number):\n            return number\n        case Lookup.Missing():\n            return 0\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "import types\ntypes.GetSetDescriptorType=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "Option contained Some writer",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option,Result\ndef probe(x:Option[int])->Option[int]:\n    return x\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode import Some\nSome.__setattr__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "Option contained Nothing alias",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option,Result\ndef probe(x:Option[int])->Option[int]:\n    return x\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode.variants import Nothing as Alias\nAlias.__eq__.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "Option nested Vector writer",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option,Result\ndef probe(x:Vector[Option[int]])->Vector[Option[int]]:\n    return x\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode import Some\nSome.__setattr__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "Result contained Ok writer",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option,Result\ndef probe(x:Result[int,str])->Result[int,str]:\n    return x\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode import Ok\nOk.__setattr__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  },
  {
    "id": "Result nested tuple Err writer",
    "files": {
      "domain.py": "# mode: fun\nfrom pyalamode import variant,case\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:int\n    @case\n    class Missing:\n        pass\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import Vector,Option,Result\ndef probe(x:tuple[Result[int,str]])->tuple[Result[int,str]]:\n    return x\n",
      "writer.py": "pass\n"
    },
    "transition": {
      "writer.py": "from pyalamode.variants import Err as Alias\nAlias.__init__.__code__=unknown\n"
    },
    "expected": [
      0,
      0,
      1
    ]
  }
]
```

## Complete literal CLI/artifact layouts

Five positive layouts exercise off/exports/debug and generated-name controls. Six negative CLI layouts use P02/P05/P42/F23/F49u/N08 directly from the complete corpus. Explain covers variant, Option, Result, accumulate, failure_value, PAL330 and PAL340. The 37 recorded CLI rows consist of 34 actual CLI commands and three ordinary artifact executions; two further prefix-control artifact subprocesses are separately asserted by the driver.

```json
[
  {
    "id": "CLI off",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=values):\n            return len(values)\n        case Lookup.Missing():\n            return 0\n@fun\ndef optional(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n        case Nothing():\n            return 0\n@fun\ndef validate(x:int,label:str)->Result[int,str]:\n    if x<0:\n        return Err(label)\n    return Ok(x)\n@fun\ndef pair(left:int,right:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(left,\"left\"),validate(right,\"right\"))\n@fun\ndef quotient(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"off\"\n"
    },
    "expected": 0
  },
  {
    "id": "CLI exports",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=values):\n            return len(values)\n        case Lookup.Missing():\n            return 0\n@fun\ndef optional(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n        case Nothing():\n            return 0\n@fun\ndef validate(x:int,label:str)->Result[int,str]:\n    if x<0:\n        return Err(label)\n    return Ok(x)\n@fun\ndef pair(left:int,right:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(left,\"left\"),validate(right,\"right\"))\n@fun\ndef quotient(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"exports\"\nguarded_exports=[\"core:probe\",\"core:optional\",\"core:quotient\"]\n"
    },
    "expected": 0
  },
  {
    "id": "CLI debug",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=values):\n            return len(values)\n        case Lookup.Missing():\n            return 0\n@fun\ndef optional(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n        case Nothing():\n            return 0\n@fun\ndef validate(x:int,label:str)->Result[int,str]:\n    if x<0:\n        return Err(label)\n    return Ok(x)\n@fun\ndef pair(left:int,right:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(left,\"left\"),validate(right,\"right\"))\n@fun\ndef quotient(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"debug\"\nguarded_exports=[\"core:probe\",\"core:optional\",\"core:quotient\"]\n"
    },
    "expected": 0
  },
  {
    "id": "unused capture prefix off",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=_pyalamode_guard_validate):\n            return 1\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"off\"\n"
    },
    "expected": 0
  },
  {
    "id": "unused capture prefix debug",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=_pyalamode_guard_validate):\n            return 1\n        case Lookup.Missing():\n            return 0\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"debug\"\n"
    },
    "expected": 0
  }
]
```

## Complete literal no-execution layouts

These are the actual 15 native authored layouts. Linux executes the same templates with distinct actual temporary absolute sentinel paths; every other source form and assertion is identical. The marker paths below are authored data, not checker-generated actions. The final driver generates fresh directories rather than requiring these removed temporary directories to exist.

```json
[
  {
    "id": "annotation",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-8c39oxrv/sentinel').write_text(\"evaluated\")\n    return 3\n@fun\ndef probe(x:mark())->int:\n    return 1\n"
    },
    "expected": 1
  },
  {
    "id": "default",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-5tbr4jrw/sentinel').write_text(\"evaluated\")\n    return 3\n@fun\ndef probe(x:int=mark())->int:\n    return x\n"
    },
    "expected": 1
  },
  {
    "id": "decorator",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-2eq7tvfb/sentinel').write_text(\"evaluated\")\n    return 3\n@mark\n@fun\ndef probe(x:int)->int:\n    return x\n"
    },
    "expected": 1
  },
  {
    "id": "variant decorator",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-x5znb58x/sentinel').write_text(\"evaluated\")\n    return 3\n@mark\n@variant\nclass Domain:\n    @case\n    class Value:\n        value:int\n"
    },
    "expected": 1
  },
  {
    "id": "case decorator",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-1gsl_9vp/sentinel').write_text(\"evaluated\")\n    return 3\n@variant\nclass Domain:\n    @mark\n    @case\n    class Value:\n        value:int\n"
    },
    "expected": 1
  },
  {
    "id": "case annotation",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-ai2bz8vv/sentinel').write_text(\"evaluated\")\n    return 3\n@variant\nclass Domain:\n    @case\n    class Value:\n        value:mark()\n"
    },
    "expected": 1
  },
  {
    "id": "case default",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-elbnx9b0/sentinel').write_text(\"evaluated\")\n    return 3\n@variant\nclass Domain:\n    @case\n    class Value:\n        value:int=mark()\n"
    },
    "expected": 1
  },
  {
    "id": "case body",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-1zg8oxwe/sentinel').write_text(\"evaluated\")\n    return 3\n@variant\nclass Domain:\n    @case\n    class Value:\n        value:int\n        hidden=mark()\n"
    },
    "expected": 1
  },
  {
    "id": "variant factory",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-3sce3yiw/sentinel').write_text(\"evaluated\")\n    return 3\n@variant(mark())\nclass Domain:\n    @case\n    class Value:\n        value:int\n"
    },
    "expected": 1
  },
  {
    "id": "pattern getter",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-u2b6d4u5/sentinel').write_text(\"evaluated\")\n    return 3\nclass Foreign:\n    @property\n    def value(self):\n        return mark()\n@fun\ndef probe(x:Option[int])->int:\n    match x:\n        case Foreign(value=number):\n            return number\n        case _:\n            return 0\n"
    },
    "expected": 1
  },
  {
    "id": "pattern guard",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-snl4t327/sentinel').write_text(\"evaluated\")\n    return 3\n@fun\ndef probe(x:Option[int])->int:\n    match x:\n        case Some() if mark():\n            return 1\n        case _:\n            return 0\n"
    },
    "expected": 1
  },
  {
    "id": "handler category",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-fem36tce/sentinel').write_text(\"evaluated\")\n    return 3\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except mark():\n        return 0\n"
    },
    "expected": 1
  },
  {
    "id": "handler body",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-27x0dv98/sentinel').write_text(\"evaluated\")\n    return 3\n@fun\ndef probe(x:int)->int:\n    try:\n        return 10//x\n    except ZeroDivisionError:\n        return mark()\n"
    },
    "expected": 1
  },
  {
    "id": "unknown class subscription",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-sentinel-x7sntxjp/sentinel').write_text(\"evaluated\")\n    return 3\nclass Foreign:\n    @classmethod\n    def __class_getitem__(cls,arg):\n        return mark()\n@fun\ndef probe(x:Foreign[int])->int:\n    return 0\n"
    },
    "expected": 1
  },
  {
    "id": "separate ordinary initialization",
    "files": {
      "core.py": "from pyalamode import fun,variant,case,record,Option,Some,Nothing\nfrom pathlib import Path\ndef mark(*args):\n    Path('/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m06-unchecked-init-u76jbefj/sentinel').write_text(\"evaluated\")\n    return 3\nmark()\n@fun\ndef probe(x:int)->int:\n    return x+1\n"
    },
    "expected": 0
  }
]
```

## Copied-package freshness source

The complete input below is run from a separate current package copy. Labels/comments are changed in variants.py, failures.py, model.py and checker.py one at a time; each changed byte identity causes a cold result followed by a warm hit. A policy change also causes a cold result followed by a warm hit. All 12 observations retain the same successful exact contract except their current source identities. The checkout is never mutated.

```json
{
  "source": "from pyalamode import fun,Option,Some\n@fun\ndef probe(x:int)->Option[int]:\n    return Some(x)\n"
}
```

## Complete frozen reviewer drivers

The following eight exact Python texts are the final reviewer inputs, retained here so reproduction does not depend on temporary files. Recreate them together with the complete corpus in a separate review directory. `final_probe.py CHECKOUT_ROOT PLATFORM_NAME` runs the six probes and full suite through its actual interpreter, records each output JSON and captures the 70-entry map. The corpus generator is retained for provenance; final reproduction can use the published corpus directly. These scripts are reviewer artifacts, not product tests or certified application code.

```json
{
  "cli_probe.py": "import hashlib,json,os,subprocess,sys,tempfile\nfrom pathlib import Path\n\nOUT=Path(__file__).parent\nchecks=0;rows=[];layouts=[]\ndef check(condition,label):\n    global checks\n    checks+=1\n    if not condition:raise AssertionError(label)\ndef call(root,label,args,status,json_output=False):\n    result=subprocess.run([sys.executable,'-m','pyalamode',*args],cwd=root,capture_output=True,text=True)\n    check(result.returncode==status,label+' status '+str(result.returncode)+' '+result.stderr)\n    payload=json.loads(result.stdout) if json_output else None\n    rows.append(dict(label=label,args=args,status=result.returncode,stdout=result.stdout,stderr=result.stderr))\n    return payload\nsource='''from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=values):\n            return len(values)\n        case Lookup.Missing():\n            return 0\n@fun\ndef optional(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n        case Nothing():\n            return 0\n@fun\ndef validate(x:int,label:str)->Result[int,str]:\n    if x<0:\n        return Err(label)\n    return Ok(x)\n@fun\ndef pair(left:int,right:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(left,\"left\"),validate(right,\"right\"))\n@fun\ndef quotient(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n'''\nordinary='''import json\nimport core\nfrom pyalamode import Vector,Some,Nothing,Err,Failure\nassert core.probe(core.Lookup.Found(Vector.of(1,2)))==2\nassert core.probe(core.Lookup.Missing())==0\nassert core.optional(Some(7))==7 and core.optional(Nothing())==0\nassert core.pair(-1,-2)==Err(Vector.of(\"left\",\"right\"))\nassert core.quotient(0)==Err(Failure(\"ZeroDivisionError\",\"division by zero\"))\nassert core.probe.__dict__=={} and core.quotient.__dict__=={}\nprint(json.dumps({\"ordinary\":True,\"errors\":[\"left\",\"right\"]}))\n'''\nguarded='''import json,core\nfrom pyalamode import Vector,Some,Nothing,Ok,Err,Failure\nfrom pyalamode_exports.core import probe,optional,quotient\nassert probe.__wrapped__ is core.probe\nassert optional.__wrapped__ is core.optional\nassert probe(core.Lookup.Found(Vector.of(1,2)))==2\nassert optional(Some(7))==7 and optional(Nothing())==0\nassert quotient(0)==Err(Failure(\"ZeroDivisionError\",\"division by zero\"))\nerrors=[]\nfor function,bad in ((probe,Some(1)),(optional,Some(True))):\n    try:function(bad)\n    except TypeError as error:errors.append(str(error))\n    else:raise AssertionError(\"invalid argument admitted\")\nassert \"argument x\" in errors[0] and \"core:probe\" in errors[0]\nassert \"argument x\" in errors[1] and \"core:optional\" in errors[1]\nassert \"core.py:\" in errors[0] and \"core.py:\" in errors[1]\nprint(json.dumps({\"guarded\":True,\"authored_paths\":True}))\n'''\n\nfor mode in ('off','exports','debug'):\n    with tempfile.TemporaryDirectory(prefix='m06-cli-'+mode+'-') as d:\n        root=Path(d);(root/'core.py').write_text(source)\n        policy='[tool.pyalamode]\\nboundary_guards=\"'+mode+'\"\\n'\n        if mode!='off':policy+='guarded_exports=[\"core:probe\",\"core:optional\",\"core:quotient\"]\\n'\n        (root/'pyproject.toml').write_text(policy)\n        layouts.append(dict(id='CLI '+mode,files={'core.py':source,'pyproject.toml':policy},expected=0))\n        checked=call(root,mode+' check',['check','--root',str(root),'--json','--no-cache'],0,True)\n        check(checked['coverage']['selected_functions']==5,mode+' denominator')\n        check(checked['verified'],mode+' strict evidence')\n        built=call(root,mode+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],0,True)\n        artifact=root/'artifact'\n        if mode=='off':check((artifact/'core.py').read_text()==source,'off exact source bytes')\n        evidence=json.loads((artifact/'pyalamode-evidence.json').read_text())\n        check(evidence['boundary_guards']==mode,mode+' artifact guard evidence')\n        check(evidence['artifact_kind'].startswith('local compatible source'),'ordinary local artifact claim')\n        environment=dict(os.environ)\n        environment['PYTHONPATH']=str(artifact)+os.pathsep+environment.get('PYTHONPATH','')\n        code=ordinary if mode=='off' else guarded\n        ran=subprocess.run([sys.executable,'-c',code],cwd=root,env=environment,capture_output=True,text=True)\n        check(ran.returncode==0,mode+' stock artifact execution '+ran.stderr)\n        check(json.loads(ran.stdout).get('ordinary' if mode=='off' else 'guarded'),mode+' execution output')\n        rows.append(dict(label=mode+' ordinary artifact',status=ran.returncode,stdout=ran.stdout,stderr=ran.stderr,\n                         artifact_files=evidence['artifact_files']))\n        if mode=='exports':check(all(c['original_protection']=='unguarded' for c in evidence['guarded_exports']),'exports original remains unguarded')\n        if mode=='debug':check(bool(evidence['debug_coverage']),'debug finite coverage')\n\ncollision=source.split('@fun\\ndef optional')[0].replace('value=values','value=_pyalamode_guard_validate').replace('return len(values)','return 1')\nfor mode in ('off','debug'):\n    with tempfile.TemporaryDirectory(prefix='m06-capture-prefix-') as d:\n        root=Path(d);(root/'core.py').write_text(collision)\n        policy='[tool.pyalamode]\\nboundary_guards=\"'+mode+'\"\\n';(root/'pyproject.toml').write_text(policy)\n        layouts.append(dict(id='unused capture prefix '+mode,files={'core.py':collision,'pyproject.toml':policy},expected=0))\n        call(root,mode+' prefix build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],0,True)\n        environment=dict(os.environ);environment['PYTHONPATH']=str(root/'artifact')+os.pathsep+environment.get('PYTHONPATH','')\n        ran=subprocess.run([sys.executable,'-c','import core\\nfrom pyalamode import Vector\\nassert core.probe(core.Lookup.Found(Vector.of(1)))==1\\n'],cwd=root,env=environment,capture_output=True,text=True)\n        check(ran.returncode==0,mode+' unused capture generated name collision '+ran.stderr)\n\nnegative=json.loads((OUT/'literal-cases.json').read_text())\nfor id in ('P02','P05','P42','F23','F49u','N08'):\n    case=next(c for c in negative if c['id']==id)\n    with tempfile.TemporaryDirectory(prefix='m06-negative-cli-') as d:\n        root=Path(d);(root/'bad.py').write_text(case['source'])\n        payload=call(root,id+' check',['check','--root',str(root),'--json','--no-cache'],1,True)\n        check(not payload['verified'],id+' no certificate')\n        call(root,id+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],1,True)\n        check(not (root/'artifact').exists(),id+' no artifact')\n        audited=call(root,id+' audit',['check','--root',str(root),'--audit','--json','--no-cache'],0,True)\n        check(not audited['verified'],id+' audit unverified')\n\nwith tempfile.TemporaryDirectory(prefix='m06-explain-') as d:\n    root=Path(d);(root/'core.py').write_text(source)\n    for symbol in ('variant','Option','Result','accumulate','failure_value','PAL330','PAL340'):\n        call(root,'explain '+symbol,['explain',symbol],0)\n    unsupported=call(root,'unsupported target',['check','--root',str(root),'--target','cpython-3.14.0','--json'],2,True)\n    check(not unsupported['verified'],'unsupported target no verification')\n\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'cli-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_layouts=layouts),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,commands=len(rows),layouts=len(layouts))))\n",
  "final_probe.py": "import hashlib,json,os,platform,re,subprocess,sys,sysconfig,time\nfrom pathlib import Path\nimport pyalamode\n\nREVIEW=Path(__file__).parent\nROOT=Path(sys.argv[1])\nNAME=sys.argv[2]\ndef digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()\ndef checkout_map():\n    paths=[ROOT/'pyproject.toml',ROOT/'README.md']\n    for directory in ('pyalamode','tests','examples'):\n        paths.extend((ROOT/directory).rglob('*.py'))\n    paths.extend((ROOT/'benchmarks').glob('m0*.py'))\n    result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths))}\n    for path in sorted(REVIEW.glob('*.py')):\n        result['reviewer:'+path.name]=digest(path)\n    result['reviewer:literal-cases.json']=digest(REVIEW/'literal-cases.json')\n    return result\ndef installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}\nbefore=checkout_map();installed_before=installed_map()\nassert len(installed_before)==13\nassert all(before[key]==value for key,value in installed_before.items())\nresults=[]\nfor script in ('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','nonexecution_probe.py','freshness_probe.py'):\n    output=NAME+'-'+script.replace('_probe.py','')+'.json'\n    started=time.perf_counter()\n    ran=subprocess.run([sys.executable,str(REVIEW/script),output],cwd=REVIEW,capture_output=True,text=True)\n    results.append(dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=output))\n    if ran.returncode:\n        print(json.dumps(results[-1]));raise SystemExit(ran.returncode)\nstarted=time.perf_counter()\nsuite=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','m*.py'],cwd=REVIEW,capture_output=True,text=True)\nsuite_result=dict(status=suite.returncode,elapsed_seconds=time.perf_counter()-started,stdout=suite.stdout,stderr=suite.stderr)\nif suite.returncode:print(json.dumps(suite_result));raise SystemExit(suite.returncode)\nmatch=re.search(r'Ran (\\d+) tests in ([\\d.]+)s',suite.stderr)\nassert match\nsuite_result.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)))\nafter=checkout_map();installed_after=installed_map()\nassert before==after\nassert installed_before==installed_after\nreport=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),py_gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),package_path=pyalamode.__file__),\n            results=results,suite=suite_result,source_before=before,source_after=after,\n            installed_product_before=installed_before,installed_product_after=installed_after,\n            source_unchanged=True,installed_source_equal=True)\n(REVIEW/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(name=NAME,suite=suite_result['tests'],suite_seconds=suite_result['reported_seconds'],focused=[r['stdout'].strip() for r in results],source_files=len(before),installed_product_files=len(installed_before),unchanged=True)))\n",
  "freshness_probe.py": "import hashlib,json,os,shutil,subprocess,sys,tempfile\nfrom pathlib import Path\nimport pyalamode\n\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n    global checks\n    checks+=1\n    if not value:raise AssertionError(label)\nsource='from pyalamode import fun,Option,Some\\n@fun\\ndef probe(x:int)->Option[int]:\\n    return Some(x)\\n'\nscript='''import json\nfrom pyalamode.project import check_paths\nfrom pyalamode.model import foundation_identities\nresult=check_paths(root=PROJECT)\nprint(json.dumps({\"status\":result.status,\"hits\":[r.cache_hit for r in result.results],\"identities\":foundation_identities(),\"contract\":result.results[0].contracts[0].__dict__}))\n'''\nwith tempfile.TemporaryDirectory(prefix='m06-copy-freshness-') as d:\n    root=Path(d);product=root/'product';project=root/'project';project.mkdir();(project/'core.py').write_text(source)\n    shutil.copytree(Path(pyalamode.__file__).parent,product/'pyalamode',ignore=shutil.ignore_patterns('__pycache__'))\n    environment=dict(os.environ);environment['PYTHONPATH']=str(product)+os.pathsep+environment.get('PYTHONPATH','')\n    def observe(label,expected_hits):\n        ran=subprocess.run([sys.executable,'-c',script.replace('PROJECT',repr(str(project)))],cwd=root,env=environment,capture_output=True,text=True)\n        check(ran.returncode==0,label+' process '+ran.stderr)\n        result=json.loads(ran.stdout);check(result['status']==0,label+' valid gate');check(result['hits']==expected_hits,label+' cache condition')\n        rows.append(dict(label=label,**result));return result\n    original=observe('copy cold',[False]);warm=observe('copy warm',[True])\n    check(original['contract']==warm['contract'],'copy exact warm evidence')\n    for filename in ('variants.py','failures.py','model.py','checker.py'):\n        target=product/'pyalamode'/filename\n        target.write_bytes(target.read_bytes()+b'\\n# independent relevant byte freshness probe\\n')\n        changed=observe(filename+' changed bytes',[False])\n        check(changed['identities'][filename]!=warm['identities'][filename],filename+' concrete bytes differ')\n        warm=observe(filename+' changed warm',[True])\n    (project/'pyproject.toml').write_text('[tool.pyalamode]\\nrequire_modules=[\"core.py\"]\\n')\n    observe('changed policy',[False]);observe('changed policy warm',[True])\n    check(not (project/'artifact').exists(),'cache checks do not publish artifacts')\n\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'freshness-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_source=source),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,transitions=len(rows))))\n",
  "make_cases.py": "import json\nfrom pathlib import Path\n\nROOT = Path('/Volumes/Projects/pyalamode')\nOUT = Path(__file__).parent\nBASE = ('from pyalamode import fun,variant,case,record,Vector,Map,OrderedMap,Set,'\n        'Option,Some,Nothing,Result,Ok,Err,accumulate,Failure,failure_value,'\n        'effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,'\n        'StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow\\n'\n        'from typing import Callable\\n')\nDOMAIN = '@variant\\nclass Lookup:\\n    @case\\n    class Found:\\n        value:int\\n    @case\\n    class Missing:\\n        pass\\n'\nCASES = []\ndef add(name, expected, source, note='', **evidence):\n    CASES.append(dict(id=name, expected=expected, source=source, note=note, **evidence))\ndef body(name, expected, params, result, code, note='', prefix='', **evidence):\n    add(name, expected, BASE+prefix+'@fun\\ndef probe('+params+')->'+result+':\\n'+code, note, selected=1, **evidence)\ndef domain(name, expected, params, result, code, note='', **evidence):\n    body(name, expected, params, result, code, note, DOMAIN, **evidence)\n\ndoc=(ROOT/'Docs/conformance/m06-cases.md').read_text()\nseed=doc.split('```json\\n',1)[1].split('\\n```',1)[0]\nCASES.extend(json.loads(seed))\nfor entry in CASES:\n    entry['note']='Fixed pre-approval universal negative'\n\ndomain('V01',0,'x:int','Lookup','    return Lookup.Found(x)\\n')\ndomain('V02',0,'x:int','Lookup','    return Lookup.Found(value=x)\\n')\ndomain('V03',0,'','Lookup','    return Lookup.Missing()\\n')\ndomain('V04',0,'x:Lookup.Found','int','    return x.value\\n')\ndomain('V05',1,'','Lookup','    return Lookup.Found(True)\\n')\ndomain('V06',1,'','Lookup','    return Lookup.Found([1])\\n')\ndomain('V07',1,'','Lookup','    return Lookup.Found()\\n')\ndomain('V08',1,'','Lookup','    return Lookup.Found(1,2)\\n')\ndomain('V09',1,'','Lookup','    return Lookup.Found(1,value=2)\\n')\ndomain('V10',1,'','Lookup','    return Lookup.Found(unknown=1)\\n')\ndomain('V11',1,'','Lookup','    return Lookup.Missing(1)\\n')\ndomain('V12',1,'','Lookup','    return Lookup()\\n')\nfor name,field,expr,expected in (\n ('V13','tuple[int,Vector[str]]','(1,Vector[str].of(\"a\"))',0),\n ('V14','Vector[tuple[int,str]]','Vector[tuple[int,str]].of((1,\"a\"))',0),\n ('V15','Vector[int]','Vector[int].of(True)',1),\n ('V16','list[int]','[1]',1),\n ('V17','Callable[[],int]','probe',1),\n ('V18','ClockCapability','clock',1),\n):\n    dec=DOMAIN.replace('value:int','value:'+field)\n    params='clock:ClockCapability' if name=='V18' else ''\n    body(name,expected,params,'Lookup','    return Lookup.Found('+expr+')\\n',prefix=dec)\nadd('V19',0,BASE+DOMAIN+'Alias=Lookup\\n@fun\\ndef probe(x:int)->Lookup:\\n    return Alias.Found(x)\\n',selected=1)\nadd('V20',0,'from pyalamode import variant as closed,case as alternative,fun as checked\\n@closed\\nclass Lookup:\\n    @alternative\\n    class Found:\\n        value:int\\n    @alternative\\n    class Missing:\\n        pass\\n@checked\\ndef probe(x:int)->Lookup:\\n    return Lookup.Found(x)\\n',selected=1)\nadd('V21',0,BASE+DOMAIN.replace('value:int','value:int=3')+'@fun\\ndef probe()->Lookup:\\n    return Lookup.Found()\\n',selected=1)\nadd('V22',1,BASE+DOMAIN.replace('value:int','value:int=[3]')+'@fun\\ndef probe()->Lookup:\\n    return Lookup.Found()\\n',selected=1)\nfor name,decl in (\n ('V23',DOMAIN.replace('class Lookup:','class Lookup(object):')),\n ('V24',DOMAIN.replace('class Found:','class Found(object):')),\n ('V25',DOMAIN.replace('value:int','value:int\\n        def changed(self):\\n            return 1')),\n ('V26',DOMAIN.replace('value:int','value:int\\n        @property\\n        def hidden(self):\\n            return 1')),\n ('V27',DOMAIN.replace('@case\\n    class Found:','@case()\\n    class Found:')),\n ('V28',DOMAIN.replace('@variant\\n','@variant()\\n')),\n ('V29',DOMAIN.replace('class Found:\\n        value:int','class Found:\\n        value:int\\n    @case\\n    class Found:\\n        pass')),\n ('V30','@variant\\nclass Empty:\\n    pass\\n'),\n ('V31',DOMAIN.replace('value:int','_value:int')),\n ('V32',DOMAIN.replace('class Lookup:','class Lookup(metaclass=Unknown):')),\n ('V33',DOMAIN.replace('value:int','value:int\\n        def __init__(self,value):\\n            self.value=value')),\n):\n    add(name,1,BASE+decl)\nfor name,writer in (\n ('V34','Lookup.Found=Lookup.Missing'),\n ('V35','Lookup.Found.__match_args__=(\"unknown\",)'),\n ('V36','Alias=Lookup.Found\\nAlias.__init__.__code__=unknown'),\n ('V37','from builtins import setattr as write\\nwrite(Lookup.Found,\"__match_args__\",())'),\n ('V38','from builtins import delattr as erase\\nerase(Lookup,\"Found\")'),\n ('V39','Lookup.Found.__dict__[\"__init__\"]=unknown'),\n):\n    add(name,1,BASE+DOMAIN+writer+'\\n@fun\\ndef probe()->Lookup:\\n    return Lookup.Found(1)\\n',selected=1)\nbody('V40',0,'x:int','Outer','    return Outer.Value(Lookup.Found(x))\\n',prefix=DOMAIN+'@variant\\nclass Outer:\\n    @case\\n    class Value:\\n        item:Lookup\\n')\nbody('V41',0,'x:int','Lookup','    return Lookup.Found(Payload(x))\\n',prefix='@record\\nclass Payload:\\n    number:int\\n'+DOMAIN.replace('value:int','value:Payload'))\nbody('V42',1,'x:Lookup','int','    return id(x)\\n',prefix=DOMAIN)\n\nbody('O01',0,'x:int','Option[int]','    return Some(x)\\n')\nbody('O02',0,'','Option[int]','    return Nothing()\\n')\nbody('O03',0,'x:Vector[int]','Option[Vector[int]]','    return Some(value=x)\\n')\nbody('O04',0,'x:int','Result[int,str]','    return Ok(x)\\n')\nbody('O05',0,'e:str','Result[int,str]','    return Err(error=e)\\n')\nbody('O06',1,'','Option[int]','    return Some(True)\\n')\nbody('O07',1,'','Result[int,str]','    return Ok(\"wrong\")\\n')\nbody('O08',1,'','Result[int,str]','    return Err(3)\\n')\nbody('O09',1,'','Option[int]','    return Some()\\n')\nbody('O10',1,'','Option[int]','    return Nothing(1)\\n')\nbody('O11',1,'','Option[int]','    return Some(1,2)\\n')\nbody('O12',1,'','Option[int]','    return Some(1,value=2)\\n')\nbody('O13',1,'','Option[int]','    return Option[int]()\\n')\nbody('O14',1,'','Result[int,str]','    return Result[int,str]()\\n')\nbody('O15',1,'','Option[int]','    return Some([1])\\n')\nbody('O16',1,'x:Option[ClockCapability]','int','    return 0\\n')\nbody('O17',1,'x:Result[int,Callable[[],int]]','int','    return 0\\n')\nbody('O18',1,'x:Option[list[int]]','int','    return 0\\n')\nbody('O19',0,'a:Option[int],b:Option[int]','bool','    return a==b\\n')\nbody('O20',0,'a:Result[int,str],b:Result[int,str]','bool','    return a!=b\\n')\nbody('O21',1,'a:Option[int],b:Option[bool]','bool','    return a==b\\n')\nbody('O22',0,'a:Result[int,str],b:Result[str,str]','Result[tuple[int,str],Vector[str]]','    return accumulate(a,b)\\n')\nbody('O23',1,'','Result[tuple[int,int],Vector[str]]','    return accumulate(Ok(1),Ok(2))\\n','No established complete Result input schemas')\nbody('O24',1,'','Result[tuple[int,int],Vector[str]]','    return accumulate(Err(\"left\"),Err(\"right\"))\\n','No established complete Result input schemas')\nbody('O25',1,'a:Result[int,str],b:Result[int,int]','Result[tuple[int,int],Vector[str]]','    return accumulate(a,b)\\n')\nbody('O26',1,'a:Result[int,str]','Result[tuple[int,int],Vector[str]]','    return accumulate(a)\\n')\nbody('O27',1,'a:Result[int,str]','Result[tuple[int,int],Vector[str]]','    return accumulate(a,a,a)\\n')\nbody('O28',1,'a:Result[int,str]','Result[tuple[int,int],Vector[str]]','    return accumulate(left=a,right=a)\\n')\nbody('O29',1,'a:Result[int,str]','Result[tuple[int,int],Vector[str]]','    return accumulate(a,unknown(a))\\n')\nbody('O30',0,'x:Option[Option[int]]','Option[Option[int]]','    return x\\n')\nbody('O31',0,'x:Result[Option[int],Vector[str]]','Result[Option[int],Vector[str]]','    return x\\n')\nbody('O32',1,'x:Result[int,str]','str','    return x.error\\n')\n\nFULL='    match x:\\n        case Lookup.Found(value=number):\\n            return number\\n        case Lookup.Missing():\\n            return 0\\n'\ndomain('P01',0,'x:Lookup','int',FULL)\ndomain('P02',1,'x:Lookup','int',FULL.split('        case Lookup.Missing():')[0])\ndomain('P03',0,'x:Lookup','int','    match x:\\n        case Lookup.Found(number):\\n            return number\\n        case Lookup.Missing():\\n            return 0\\n')\ndomain('P04',0,'x:Lookup','int','    match x:\\n        case Lookup.Found():\\n            return 1\\n        case _:\\n            return 0\\n')\ndomain('P05',1,'x:Lookup,flag:bool','int','    match x:\\n        case Lookup.Found() if flag:\\n            return 1\\n        case Lookup.Missing():\\n            return 0\\n')\ndomain('P06',0,'x:Lookup,flag:bool','int','    match x:\\n        case Lookup.Found() if flag:\\n            return 1\\n        case _:\\n            return 0\\n')\ndomain('P07',0,'x:Lookup','int','    match x:\\n        case Lookup.Found() if True:\\n            return 1\\n        case Lookup.Missing():\\n            return 0\\n')\ndomain('P08',1,'x:Lookup','int','    match x:\\n        case Lookup.Found() if False:\\n            return 1\\n        case Lookup.Missing():\\n            return 0\\n')\ndomain('P09',1,'x:Lookup','int',FULL.replace('value=number):','value=number) if True:'))\ndomain('P10',1,'x:Lookup,number:int','int',FULL)\ndomain('P11',1,'x:Lookup','int','    number=4\\n'+FULL)\ndomain('P12',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(value=0):\\n            return 1\\n        case Lookup.Missing():\\n            return 0\\n')\ndomain('P13',0,'x:Lookup','int','    match x:\\n        case Lookup.Found(value=0):\\n            return 1\\n        case Lookup.Found():\\n            return 2\\n        case Lookup.Missing():\\n            return 0\\n')\ndomain('P14',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(value=number):\\n            selected=number\\n        case Lookup.Missing():\\n            pass\\n    return selected\\n')\ndomain('P15',0,'x:Lookup','int','    match x:\\n        case Lookup.Found(value=number):\\n            selected=number\\n        case Lookup.Missing():\\n            selected=0\\n    return selected\\n')\ndomain('P16',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(value=number):\\n            pass\\n        case Lookup.Missing():\\n            pass\\n    return number\\n')\ndomain('P17',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(value=number) if number>0:\\n            return number\\n        case _:\\n            return number\\n')\ndomain('P18',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(unknown=number):\\n            return number\\n        case _:\\n            return 0\\n')\ndomain('P19',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(number,value=other):\\n            return number\\n        case _:\\n            return 0\\n')\ndomain('P20',1,'x:Lookup','int','    match x:\\n        case Lookup.Found(number,other):\\n            return number\\n        case _:\\n            return 0\\n')\ndomain('P21',1,'x:Lookup','int','    match x:\\n        case Unknown(value=number):\\n            return number\\n        case _:\\n            return 0\\n')\ndomain('P22',1,'x:Lookup','int','    match x:\\n        case Lookup.Found()|Lookup.Missing():\\n            return 0\\n')\ndomain('P23',1,'x:Lookup','int','    match x:\\n        case [number]:\\n            return number\\n        case _:\\n            return 0\\n')\ndomain('P24',1,'x:Lookup','int','    match x:\\n        case {\"value\":number}:\\n            return number\\n        case _:\\n            return 0\\n')\ndomain('P25',1,'x:Lookup','int','    match x:\\n        case Lookup.Found() if unknown_guard():\\n            return 1\\n        case _:\\n            return 0\\n')\nbody('P26',0,'x:Option[int]','int','    match x:\\n        case Some(value=number):\\n            return number\\n        case Nothing():\\n            return 0\\n')\nbody('P27',1,'x:Option[int]','int','    match x:\\n        case Some(value=number):\\n            return number\\n')\nbody('P28',0,'x:Result[int,str]','int','    match x:\\n        case Ok(value=number):\\n            return number\\n        case Err(error=problem):\\n            return len(problem)\\n')\nbody('P29',1,'x:Result[int,str]','int','    match x:\\n        case Ok(value=number):\\n            return number\\n')\nbody('P30',0,'x:bool','int','    match x:\\n        case True:\\n            return 1\\n        case False:\\n            return 0\\n')\nbody('P31',1,'x:bool','int','    match x:\\n        case True:\\n            return 1\\n')\nbody('P32',1,'x:bool','int','    match x:\\n        case 1:\\n            return 1\\n        case 0:\\n            return 0\\n')\nbody('P33',0,'x:None','int','    match x:\\n        case None:\\n            return 0\\n')\nbody('P34',1,'x:int','int','    match x:\\n        case 1:\\n            return 1\\n        case _:\\n            return 0\\n')\nbody('P35',0,'x:Payload','int','    match x:\\n        case Payload(number=n):\\n            return n\\n',prefix='@record\\nclass Payload:\\n    number:int\\n')\nbody('P36',1,'x:Payload','int','    match x:\\n        case Payload(number=0):\\n            return 0\\n',prefix='@record\\nclass Payload:\\n    number:int\\n')\ntwo='@variant\\nclass Pair:\\n    @case\\n    class Data:\\n        first:int\\n        second:int\\n'\nbody('P37',1,'x:Pair','int','    match x:\\n        case Pair.Data(first=number,second=0):\\n            return number\\n        case _:\\n            return 0\\n',prefix=two)\nbody('P38',1,'x:Pair','int','    match x:\\n        case Pair.Data(first=number,second=number):\\n            return number\\n',prefix=two)\nbody('P39',0,'x:Pair','int','    match x:\\n        case Pair.Data(first=number,second=other):\\n            return number+other\\n',prefix=two)\ndomain('P40',1,'x:Lookup,Lookup:int','int',FULL)\ndomain('P41',1,'x:Lookup','int','    match x:\\n        case Lookup.Found() as whole:\\n            return 1\\n        case _:\\n            return 0\\n')\nnested=DOMAIN+'@variant\\nclass Outer:\\n    @case\\n    class Value:\\n        item:Lookup\\n'\nbody('P42',1,'x:Outer','int','    match x:\\n        case Outer.Value(item=Lookup.Found(value=number)):\\n            return number\\n',prefix=nested,note='Nested class pattern narrows a multi-case payload and cannot fully cover the outer case')\nbody('P43',1,'x:Outer','int','    match x:\\n        case Outer.Value(item=Lookup.Found(value=number)):\\n            return number\\n        case _:\\n            return 0\\n',prefix=nested,note='A nested constrained payload pattern cannot expose named captures')\nbody('P44',1,'x:Outer','int','    match x:\\n        case Outer.Value(item=Lookup.Found()):\\n            return 1\\n',prefix=nested,note='Capture-free nested constrained payload is not full outer-case coverage')\nbody('P45',0,'x:Outer','int','    match x:\\n        case Outer.Value(item=Lookup.Found()):\\n            return 1\\n        case _:\\n            return 0\\n',prefix=nested,note='Capture-free constrained nested pattern is usable with deliberate final wildcard')\n\nfor name,category,expected,failures in (\n ('F01','ZeroDivisionError',0,[]),('F02','IndexError',0,['ZeroDivisionError']),\n ('F03','ValueError',0,['ZeroDivisionError']),('F04','Exception',1,None),\n ('F05','BaseException',1,None),('F06','UnknownError',1,None),\n):\n    body(name,expected,'x:int','int','    try:\\n        return 10//x\\n    except '+category+':\\n        return 0\\n',**({'failures':failures} if failures is not None else {}))\nbody('F07',0,'x:int','Result[int,Failure]','    try:\\n        return Ok(10//x)\\n    except ZeroDivisionError as caught:\\n        failure=failure_value(caught)\\n        return Err(failure)\\n',failures=['RecursionError'])\nbody('F08',0,'x:int','str','    try:\\n        return \"ok\"\\n    except ValueError as caught:\\n        return failure_value(caught).category\\n')\nbody('F09',0,'x:int','str','    try:\\n        return \"ok\"\\n    except ValueError as caught:\\n        failure=failure_value(caught)\\n        return failure.message\\n')\nbody('F10',1,'x:int','int','    try:\\n        return 10//x\\n    except:\\n        return 0\\n')\nbody('F11',1,'x:int','int','    try:\\n        return 10//x\\n    except* ZeroDivisionError:\\n        result=0\\n    return result\\n')\nbody('F12',1,'x:int','int','    try:\\n        value=10//x\\n    except ZeroDivisionError:\\n        return 0\\n    else:\\n        return value\\n')\nbody('F13',1,'x:int','int','    try:\\n        return 10//x\\n    finally:\\n        pass\\n')\nbody('F14',1,'x:int','int','    try:\\n        return 10//x\\n    except (ValueError,UnicodeError):\\n        return 0\\n')\nbody('F15',1,'x:int','int','    try:\\n        return 10//x\\n    except (RuntimeError,RecursionError):\\n        return 0\\n')\nbody('F16',1,'x:int','int','    try:\\n        return 10//x\\n    except ZeroDivisionError:\\n        return 0\\n    except ZeroDivisionError:\\n        return 1\\n')\nbody('F17',0,'x:int','int','    try:\\n        return 10//x\\n    except (ZeroDivisionError,IndexError):\\n        return 0\\n',failures=[])\nbody('F18',1,'x:int,caught:int','int','    try:\\n        return 10//x\\n    except ZeroDivisionError as caught:\\n        return 0\\n')\nbody('F19',1,'x:int','int','    try:\\n        value=10//x\\n    except ZeroDivisionError:\\n        value=0\\n    return value\\n')\nbody('F20',1,'x:int','int','    try:\\n        value=10//x\\n    except ZeroDivisionError:\\n        return value\\n    return value\\n')\nbody('F21',1,'x:int','int','    try:\\n        return 10//x\\n    except ZeroDivisionError as caught:\\n        pass\\n    return caught\\n')\nbody('F22',1,'x:int','int','    try:\\n        return 10//x\\n    except ZeroDivisionError as caught:\\n        pass\\n    caught=1\\n    return caught\\n')\nfor name,expr in (\n ('F23','caught'),('F24','caught.args'),('F25','caught.__dict__'),\n ('F26','caught.__traceback__'),('F27','str(caught)'),('F28','repr(caught)'),\n ('F29','(caught,)'),('F30','Some(caught)'),('F31','failure_value((caught,))'),\n ('F32','getattr(caught,\"args\")'),\n):\n    body(name,1,'x:int','Failure','    try:\\n        return Failure(\"x\",\"y\")\\n    except ValueError as caught:\\n        return '+expr+'\\n')\nbody('F33',1,'x:int','Failure','    try:\\n        return Failure(\"x\",\"y\")\\n    except ValueError as caught:\\n        alias=caught\\n        return failure_value(alias)\\n')\nbody('F34',1,'x:int','Callable[[],Failure]','    try:\\n        return unknown()\\n    except ValueError as caught:\\n        def retained()->Failure:\\n            return failure_value(caught)\\n        return retained\\n')\nbody('F35',1,'x:int','Failure','    return failure_value(x)\\n')\nbody('F36',1,'','Failure','    return failure_value(ValueError(\"x\"))\\n')\nbody('F37',0,'','Failure','    return Failure(category=\"ValueError\",message=\"data only\")\\n')\nbody('F38',1,'','Failure','    return Failure(category=True,message=\"bad\")\\n')\nbody('F39',0,'x:int','int','    try:\\n        return 10//x\\n    except ZeroDivisionError:\\n        return 1//x\\n',failures=['ZeroDivisionError'])\nbody('F40',0,'x:int','int','    try:\\n        try:\\n            return 10//x\\n        except ZeroDivisionError:\\n            return 1//x\\n    except ZeroDivisionError:\\n        return 0\\n',failures=[])\nbody('F41',0,'op:Callable[[int],int],x:int','int','    try:\\n        return op(x)\\n    except ZeroDivisionError:\\n        return 0\\n',failures=['IndexError','KeyError','RecursionError','ValueError'])\nbody('F42',0,'op:Callable[[int],int],x:int','int','    try:\\n        return op(x)\\n    except RuntimeError:\\n        return 0\\n',failures=['IndexError','KeyError','ValueError','ZeroDivisionError'])\nbody('F43',0,'op:Callable[[int],int],x:int','int','    try:\\n        return op(x)\\n    except ValueError:\\n        return 0\\n',failures=['IndexError','KeyError','RecursionError','ZeroDivisionError'])\nleaf='@fun\\ndef divide(x:int)->int:\\n    return 10//x\\n'\nbody('F44',0,'x:int','int','    try:\\n        return divide(x)\\n    except ZeroDivisionError:\\n        return 0\\n',prefix=leaf,failures=[])\nbody('F45',0,'x:int','int','    first=divide(x)\\n    try:\\n        return divide(first)\\n    except ZeroDivisionError:\\n        return 0\\n',prefix=leaf,failures=['ZeroDivisionError'])\nbody('F46',0,'x:int','int','    try:\\n        return divide(x)\\n    except IndexError:\\n        return 0\\n',prefix=leaf,failures=['ZeroDivisionError'])\nbody('F47',0,'x:int','int','    try:\\n        return divide(x)\\n    except ZeroDivisionError:\\n        return divide(x)\\n',prefix=leaf,failures=['ZeroDivisionError'])\nbody('F48',0,'x:int','int','    try:\\n        return divide(x)\\n    except (ZeroDivisionError,RuntimeError):\\n        return 0\\n',prefix=leaf,failures=[])\nfor name,family,capability,statement,categories in (\n ('F49','Clock','ClockCapability','stamp=cap.now_ns()','(IndexError,RuntimeError,OSError,ZeroDivisionError)'),\n ('F50','State','StateCapability','cap.set(3)','(RuntimeError,ZeroDivisionError)'),\n ('F51','IO','IOCapability','text=cap.read_text(\"x.txt\")','(OSError,UnicodeError,RuntimeError,KeyError,ZeroDivisionError)'),\n ('F52','Random','RandomCapability','number=cap.below(3)','(ValueError,RuntimeError,OSError,IndexError,ZeroDivisionError)'),\n ('F53','Environment','EnvironmentCapability','text=cap.get(\"MODE\",\"\")','(ValueError,RuntimeError,OSError,ZeroDivisionError)'),\n):\n    source=BASE+'@effects('+family+')\\ndef probe(cap:'+capability+',x:int)->int:\\n    try:\\n        '+statement+'\\n        return 10//x\\n    except '+categories+':\\n        return 0\\n'\n    add(name,0,source,selected=1,required_effects=[family],effect_bound=[family])\n    add(name+'u',1,source.replace('@effects('+family+')','@fun'),selected=1)\nbody('F54',1,'x:int,ValueError:int','int','    try:\\n        return x\\n    except ValueError:\\n        return 0\\n')\nadd('F55',1,BASE+'ValueError=int\\n@fun\\ndef probe(x:int)->int:\\n    try:\\n        return x\\n    except ValueError:\\n        return 0\\n',selected=1)\nadd('F56',1,BASE+'import builtins\\nbuiltins.ZeroDivisionError=Exception\\n@fun\\ndef probe(x:int)->int:\\n    try:\\n        return 10//x\\n    except ZeroDivisionError:\\n        return 0\\n',selected=1)\nadd('F57',0,BASE+'from builtins import ZeroDivisionError as DivFailure\\n@fun\\ndef probe(x:int)->int:\\n    try:\\n        return 10//x\\n    except DivFailure:\\n        return 0\\n',selected=1,failures=[])\nbody('F58',0,'x:int','int','    try:\\n        with borrow(cap) as scoped:\\n            return scoped.now_ns()//x\\n    except (RuntimeError,OSError,IndexError,ZeroDivisionError):\\n        return 0\\n',prefix='')\nCASES[-1]['source']=CASES[-1]['source'].replace('@fun\\ndef probe(x:int)','@effects(Clock)\\ndef probe(cap:ClockCapability,x:int)')\nCASES[-1]['required_effects']=['Clock']\nCASES[-1]['failures']=[]\nbody('F59',1,'x:int','int','    try:\\n        return 10//x\\n    except ZeroDivisionError as caught:\\n        caught=1\\n        return caught\\n')\nbody('F60',1,'x:int','Failure','    try:\\n        return Failure(\"x\",\"y\")\\n    except ValueError as caught:\\n        def capture()->Failure:\\n            return Failure(\"x\",\"y\")\\n        return failure_value(caught)\\n    return failure_value(caught)\\n')\n\nbody('H01',0,'op:Callable[[int],Result[int,str]],x:int','Result[tuple[int,int],Vector[str]]','    left=op(x)\\n    right=op(x+1)\\n    return accumulate(left,right)\\n')\nbody('H02',1,'x:int','Result[tuple[int,int],Vector[str]]','    left=unknown(x)\\n    return accumulate(left,Ok(x))\\n')\npure='@fun\\ndef validate(x:int)->Result[int,str]:\\n    if x<0:\\n        return Err(\"negative\")\\n    return Ok(x)\\n'\nbody('H03',0,'x:int','Result[tuple[int,int],Vector[str]]','    return accumulate(validate(x),validate(x+1))\\n',prefix=pure)\neffect='@effects(Clock)\\ndef validate(cap:ClockCapability,x:int)->Result[int,str]:\\n    stamp=cap.now_ns()\\n    return Ok(x+stamp)\\n'\nadd('H04',0,BASE+effect+'@effects(Clock)\\ndef probe(cap:ClockCapability,x:int)->Result[tuple[int,int],Vector[str]]:\\n    return accumulate(validate(cap,x),validate(cap,x+1))\\n',selected=2,required_effects=['Clock'])\nadd('H05',1,BASE+effect+'@fun\\ndef probe(cap:ClockCapability,x:int)->Result[tuple[int,int],Vector[str]]:\\n    return accumulate(validate(cap,x),validate(cap,x+1))\\n',selected=2)\nbody('H06',0,'values:Vector[int]','Vector[Result[int,str]]','    return values.map(validate)\\n',prefix=pure)\nbody('H07',1,'values:Vector[int]','Vector[Result[int,str]]','    return values.map(unknown)\\n')\n\ndual='@fun\\ndef dual(values:Vector[int],index:int,denominator:int)->int:\\n    return values[index]//denominator\\n'\nbody('F61',0,'values:Vector[int],index:int,denominator:int','int','    try:\\n        first=dual(values,index,denominator)\\n    except ZeroDivisionError:\\n        return 0\\n    try:\\n        return dual(values,index,first)\\n    except IndexError:\\n        return 0\\n',prefix=dual,failures=['IndexError','ZeroDivisionError'])\nbody('F62',0,'values:Vector[int],index:int,denominator:int','int','    try:\\n        try:\\n            return dual(values,index,denominator)\\n        except ZeroDivisionError:\\n            return 0\\n    except IndexError:\\n        return 0\\n',prefix=dual,failures=[])\nbody('F63',0,'values:Vector[int],index:int,denominator:int','int','    try:\\n        return dual(values,index,denominator)\\n    except (IndexError,ZeroDivisionError):\\n        return dual(values,index,denominator)\\n',prefix=dual,failures=['IndexError','ZeroDivisionError'])\nbody('F64',1,'x:int','int','    try:\\n        caught=3\\n        return 10//x\\n    except ZeroDivisionError as caught:\\n        return 0\\n','Exception target must not overwrite any potential try-body binding')\nfor name,annotation,future in (\n ('D01','Lookup.Missing',''),('D02','Lookup.Found',''),\n ('D03','\"Lookup.Missing\"',''),('D04','\"Found\"',''),\n ('D05','Lookup.Missing','from __future__ import annotations\\n'),\n ('D06','Lookup.Found','from __future__ import annotations\\n'),\n ('D07','Found','from __future__ import annotations\\n'),\n):\n    add(name,1,future+BASE+DOMAIN.replace('value:int','value:'+annotation),'Domain binding unavailable while nested case decorator executes')\nadd('D08',1,BASE+'@variant\\nclass Lookup:\\n    @case\\n    class Found:\\n        value:Later\\n    @case\\n    class Missing:\\n        pass\\n@record\\nclass Later:\\n    value:int\\n','Forward external record unavailable at ordinary declaration execution')\nadd('D09',0,'from __future__ import annotations\\n'+BASE+'@record\\nclass Payload:\\n    number:int\\n'+DOMAIN.replace('value:int','value:Payload')+'@fun\\ndef probe(x:Payload)->Lookup:\\n    return Lookup.Found(x)\\n',selected=1)\nadd('D10',1,BASE+'@variant\\nclass Lookup:\\n    @case\\n    class case:\\n        pass\\n    @case\\n    class Missing:\\n        pass\\n','Earlier outer class case binding shadows the later decorator')\nadd('D11',1,BASE+'@record\\nclass Pair:\\n    int:int=3\\n    value:int=4\\n','Actual class-local default shadows a later nonpostponed annotation')\nadd('D12',1,BASE+'@variant\\nclass Lookup:\\n    @case\\n    class Pair:\\n        int:int=3\\n        value:int=4\\n','Actual case-local default shadows a later nonpostponed annotation')\nadd('D13',0,'from __future__ import annotations\\n'+BASE+'@record\\nclass Pair:\\n    int:int=3\\n    value:int=4\\n','Closed postponed parser resolves annotation from module namespace')\nadd('D14',0,'from __future__ import annotations\\n'+BASE+'@variant\\nclass Lookup:\\n    @case\\n    class Pair:\\n        int:int=3\\n        value:int=4\\n','Closed postponed parser resolves case annotation from module namespace')\nadd('D15',1,BASE+'@record\\nclass Pair:\\n    int:int=3\\n    value:\"int\"=4\\n','Current field default is stored before its own nonpostponed annotation; quoting only the later field does not repair it')\nadd('D16',1,BASE+'@variant\\nclass Lookup:\\n    @case\\n    class Pair:\\n        int:int=3\\n        value:\"int\"=4\\n','Current case field default is stored before its own nonpostponed annotation')\nadd('D17',1,BASE+'TOKEN=4\\n@record\\nclass Pair:\\n    TOKEN:bool=True\\n    value:int=TOKEN\\n','Class-local default must not silently resolve same-named global')\nadd('D18',1,BASE+'TOKEN=4\\n@variant\\nclass Lookup:\\n    @case\\n    class Pair:\\n        TOKEN:bool=True\\n        value:int=TOKEN\\n','Case-local default must not silently resolve same-named global')\nadd('D19',1,'from __future__ import annotations\\n'+BASE+'TOKEN=4\\n@record\\nclass Pair:\\n    TOKEN:bool=True\\n    value:int=TOKEN\\n','Postponement does not change ordinary default lookup')\nadd('D20',0,BASE+'@variant\\nclass Lookup:\\n    @case\\n    class int:\\n        pass\\n    @case\\n    class Found:\\n        value:int\\n','Outer class locals do not enclose the nested case class annotation lookup')\nadd('D21',0,BASE+'@record\\nclass Pair:\\n    int:\"int\"=3\\n    value:\"int\"=4\\n','Both closed quoted annotations resolve from module namespace')\nadd('D22',0,BASE+'@variant\\nclass Lookup:\\n    @case\\n    class Pair:\\n        int:\"int\"=3\\n        value:\"int\"=4\\n','Both closed quoted case annotations resolve from module namespace')\nfor name,schema,writer in (\n ('W01','Option[int]','Some.__setattr__=unknown'),\n ('W02','Option[int]','Nothing.__eq__.__code__=unknown'),\n ('W03','Result[int,str]','Ok.__setattr__=unknown'),\n ('W04','Result[int,str]','Err.__init__.__code__=unknown'),\n ('W05','Vector[Option[int]]','Some.__setattr__=unknown'),\n ('W06','tuple[Result[int,str]]','Ok.__setattr__=unknown'),\n ('W07','Option[int]','from pyalamode.variants import Some as Alias\\nAlias.__setattr__=unknown'),\n):\n    add(name,1,BASE+'@fun\\ndef probe(x:'+schema+')->'+schema+':\\n    return x\\n'+writer+'\\n','Parent family and nested admitted schemas depend on every contained exact case definition',selected=1)\nadd('W08',1,BASE+'@record\\nclass Payload:\\n    option:Option[int]\\n@fun\\ndef probe(x:Payload)->Payload:\\n    return x\\nSome.__setattr__=unknown\\n','Record field parent-family dependency',selected=1)\nadd('W09',1,BASE+'@variant\\nclass Domain:\\n    @case\\n    class Payload:\\n        option:Option[int]\\n@fun\\ndef probe(x:Domain)->Domain:\\n    return x\\nSome.__setattr__=unknown\\n','Variant field parent-family dependency',selected=1)\n\n(OUT/'literal-cases.json').write_text(json.dumps(CASES,indent=2)+'\\n')\nprint(json.dumps(dict(cases=len(CASES),admit=sum(c['expected']==0 for c in CASES),refuse=sum(c['expected']==1 for c in CASES))))\n",
  "nonexecution_probe.py": "import json,os,subprocess,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\n\nOUT=Path(__file__).parent;checks=0;rows=[];layouts=[]\ndef check(value,label):\n    global checks\n    checks+=1\n    if not value:raise AssertionError(label)\nbase='from pyalamode import fun,variant,case,record,Option,Some,Nothing\\nfrom pathlib import Path\\ndef mark(*args):\\n    Path(MARKER).write_text(\"evaluated\")\\n    return 3\\n'\nfixtures=(\n ('annotation','@fun\\ndef probe(x:mark())->int:\\n    return 1\\n'),\n ('default','@fun\\ndef probe(x:int=mark())->int:\\n    return x\\n'),\n ('decorator','@mark\\n@fun\\ndef probe(x:int)->int:\\n    return x\\n'),\n ('variant decorator','@mark\\n@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int\\n'),\n ('case decorator','@variant\\nclass Domain:\\n    @mark\\n    @case\\n    class Value:\\n        value:int\\n'),\n ('case annotation','@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:mark()\\n'),\n ('case default','@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int=mark()\\n'),\n ('case body','@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int\\n        hidden=mark()\\n'),\n ('variant factory','@variant(mark())\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int\\n'),\n ('pattern getter','class Foreign:\\n    @property\\n    def value(self):\\n        return mark()\\n@fun\\ndef probe(x:Option[int])->int:\\n    match x:\\n        case Foreign(value=number):\\n            return number\\n        case _:\\n            return 0\\n'),\n ('pattern guard','@fun\\ndef probe(x:Option[int])->int:\\n    match x:\\n        case Some() if mark():\\n            return 1\\n        case _:\\n            return 0\\n'),\n ('handler category','@fun\\ndef probe(x:int)->int:\\n    try:\\n        return 10//x\\n    except mark():\\n        return 0\\n'),\n ('handler body','@fun\\ndef probe(x:int)->int:\\n    try:\\n        return 10//x\\n    except ZeroDivisionError:\\n        return mark()\\n'),\n ('unknown class subscription','class Foreign:\\n    @classmethod\\n    def __class_getitem__(cls,arg):\\n        return mark()\\n@fun\\ndef probe(x:Foreign[int])->int:\\n    return 0\\n'),\n)\nfor label,fragment in fixtures:\n    with tempfile.TemporaryDirectory(prefix='m06-sentinel-') as d:\n        root=Path(d);marker=root/'sentinel';source=base.replace('MARKER',repr(str(marker)))+fragment\n        (root/'core.py').write_text(source);layouts.append(dict(id=label,files={'core.py':source},expected=1))\n        checked=check_paths(root=root,cache=False)\n        check(checked.status==1,label+' check refusal');check(not marker.exists(),label+' check nonexecution')\n        built=build_paths(root=root,output=root/'artifact')\n        check(built.status==1,label+' build refusal');check(not marker.exists(),label+' build nonexecution')\n        check(not (root/'artifact').exists(),label+' no artifact')\n        rows.append(dict(label=label,check_status=checked.status,build_status=built.status,sentinel_exists=marker.exists()))\n\nwith tempfile.TemporaryDirectory(prefix='m06-unchecked-init-') as d:\n    root=Path(d);marker=root/'sentinel'\n    source=base.replace('MARKER',repr(str(marker)))+'mark()\\n@fun\\ndef probe(x:int)->int:\\n    return x+1\\n'\n    (root/'core.py').write_text(source);layouts.append(dict(id='separate ordinary initialization',files={'core.py':source},expected=0))\n    checked=check_paths(root=root,cache=False)\n    check(checked.status==0,'separate invocation checks');check(not marker.exists(),'ordinary initializer not executed by check')\n    check(checked.results[0].initialization_evidence=='unchecked ordinary module initialization','separate initialization evidence')\n    built=build_paths(root=root,output=root/'artifact')\n    check(built.status==0,'ordinary initializer copied');check(not marker.exists(),'ordinary initializer not executed by build')\n    check((root/'artifact/core.py').read_text()==source,'unchanged ordinary source')\n    env=dict(os.environ);env['PYTHONPATH']=str(root/'artifact')+os.pathsep+env.get('PYTHONPATH','')\n    ran=subprocess.run([sys.executable,'-c','import core\\nassert core.probe(1)==2\\n'],cwd=root,env=env,capture_output=True,text=True)\n    check(ran.returncode==0,'stock ordinary initializer runs '+ran.stderr)\n    check(marker.read_text()=='evaluated','initialization occurs only on ordinary import')\n    rows.append(dict(label='separate ordinary initialization',check_status=checked.status,build_status=built.status,ordinary_status=ran.returncode))\n\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'nonexecution-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_layouts=layouts),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,sentinels=len(fixtures),layouts=len(layouts))))\n",
  "project_probe.py": "import hashlib,json,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\n\nOUT=Path(__file__).parent\nchecks=0;rows=[];layouts=[]\ndef check(condition,label):\n    global checks\n    checks+=1\n    if not condition:raise AssertionError(label)\ndef write(root,files):\n    for name,source in files.items():\n        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source)\ndef contract(result,name):\n    return next(c for f in result.results for c in f.contracts if c.name==name)\ndef gate(root,label,expected,cache=True):\n    result=check_paths(root=root,cache=cache)\n    check(result.status==expected,label+' status '+str(result.status))\n    rows.append(dict(label=label,status=result.status,cache_hits={Path(f.path).name:f.cache_hit for f in result.results},\n                     diagnostics=[d.__dict__ for d in [*result.tooling,*[d for f in result.results for d in f.diagnostics]]],\n                     contracts={c.name:c.__dict__ for f in result.results for c in f.contracts}))\n    return result\n\ndomain='# mode: fun\\nfrom pyalamode import variant,case\\n@variant\\nclass Lookup:\\n    @case\\n    class Found:\\n        value:int\\n    @case\\n    class Missing:\\n        pass\\n'\nexplicit='# mode: fun\\nfrom domain import Lookup\\ndef probe(x:Lookup)->int:\\n    match x:\\n        case Lookup.Found(value=number):\\n            return number\\n        case Lookup.Missing():\\n            return 0\\n'\nwildcard='# mode: fun\\nfrom domain import Lookup\\ndef probe(x:Lookup)->int:\\n    match x:\\n        case Lookup.Found(value=number):\\n            return number\\n        case _:\\n            return 0\\n'\nadded=domain+'    @case\\n    class Pending:\\n        code:str\\n'\nfor label,consumer,after in (('explicit',explicit,1),('wildcard',wildcard,0)):\n    with tempfile.TemporaryDirectory(prefix='m06-'+label+'-') as d:\n        root=Path(d);files={'domain.py':domain,'consumer.py':consumer};write(root,files)\n        layouts.append(dict(id='case-add-'+label,files=files,transition={'domain.py':added},expected=[0,0,after]))\n        first=gate(root,label+' cold',0);warm=gate(root,label+' warm',0)\n        check(all(f.cache_hit for f in warm.results),label+' fully warm')\n        before=contract(first,'probe')\n        write(root,{'domain.py':added});changed=gate(root,label+' case addition',after)\n        check(not next(f for f in changed.results if Path(f.path).name=='consumer.py').cache_hit,label+' consumer invalidated')\n        if not after:\n            check(before.patterns[0]['wildcard'] and contract(changed,'probe').patterns[0]['wildcard'],'deliberate wildcard evidence')\n            check(before.patterns[0]['case_fingerprint']!=contract(changed,'probe').patterns[0]['case_fingerprint'],'case fingerprint changed')\n        failed=build_paths(root=root,output=root/'artifact')\n        check(failed.status==after,label+' subsequent build gate')\n        check((root/'artifact').exists()==(not after),label+' artifact publication')\n\npolicies=(\n ('explicit wildcard','explicit_cases=[\"domain:Lookup\"]',wildcard,1),\n ('explicit complete','explicit_cases=[\"domain:Lookup\"]',explicit,0),\n ('unknown selector','explicit_cases=[\"domain:Unknown\"]',explicit,2),\n ('wrong type','explicit_cases=3',explicit,2),\n ('unknown module','explicit_cases=[\"unknown:Lookup\"]',explicit,2),\n ('malformed selector','explicit_cases=[\"domain.Lookup\"]',explicit,2),\n ('duplicate selector','explicit_cases=[\"domain:Lookup\",\"domain:Lookup\"]',explicit,2),\n)\nfor label,policy,consumer,status in policies:\n    with tempfile.TemporaryDirectory(prefix='m06-policy-') as d:\n        root=Path(d);files={'domain.py':domain,'consumer.py':consumer,'pyproject.toml':'[tool.pyalamode]\\n'+policy+'\\n'}\n        layouts.append(dict(id=label,files=files,expected=status));write(root,files)\n        gate(root,label,status);built=build_paths(root=root,output=root/'artifact')\n        check(built.status==status,label+' build status')\n        check((root/'artifact').exists()==(not status),label+' build output')\n\nleaf='# mode: fun\\ndef divide(x:int)->int:\\n    return 10//x\\n'\nfactory='# mode: fun\\nfrom typing import Callable\\nfrom leaf import divide\\ndef maker()->Callable[[int],int]:\\n    def handled(x:int)->int:\\n        try:\\n            return divide(x)\\n        except ZeroDivisionError:\\n            return 0\\n    return handled\\n'\nconsumer='# mode: fun\\nfrom factory import maker\\ndef invoke(x:int)->int:\\n    return maker()(x)\\n'\nwith tempfile.TemporaryDirectory(prefix='m06-handler-warm-') as d:\n    root=Path(d);files={'leaf.py':leaf,'factory.py':factory,'consumer.py':consumer};write(root,files)\n    layouts.append(dict(id='returned handler partial warm',files=files,transition={'consumer.py':consumer+'\\n# independent consumer edit\\n'},expected=[0,0,0]))\n    cold=gate(root,'returned handler cold',0);warm=gate(root,'returned handler warm',0)\n    check(all(f.cache_hit for f in warm.results),'handler full body reuse')\n    for result in (cold,warm):\n        check(contract(result,'invoke').failures==[],'handled returned target does not leak division failure')\n        check(contract(result,'maker').required_effects==[],'reference factory has no invocation effects')\n        check(bool(contract(result,'maker').return_callable_targets),'known returned handler target retained')\n        check(bool(contract(result,'maker.handled').failure_edges),'handler call edge serialized')\n    write(root,{'consumer.py':consumer+'\\n# independent consumer edit\\n'})\n    partial=gate(root,'returned handler partial warm',0)\n    hits={Path(f.path).name:f.cache_hit for f in partial.results}\n    check(hits['factory.py'] and hits['leaf.py'] and not hits['consumer.py'],'actual partial factory body reuse')\n    for name in ('maker','maker.handled','invoke'):\n        check(contract(cold,name).__dict__==contract(partial,name).__dict__,'partial exact evidence '+name)\n\nclockleaf='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\n@effects(Clock)\\ndef timed(cap:ClockCapability,x:int)->int:\\n    try:\\n        return cap.now_ns()//x\\n    except ZeroDivisionError:\\n        return 0\\n'\nclockfactory='# mode: fun\\nfrom pyalamode import Effectful,Clock,State,ClockCapability\\nfrom leaf import timed\\ndef maker()->Effectful[[ClockCapability,int],int,Clock,State]:\\n    return timed\\n'\nclockconsumer='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\nfrom factory import maker\\n@effects(Clock)\\ndef invoke(cap:ClockCapability,x:int)->int:\\n    return maker()(cap,x)\\n'\nwith tempfile.TemporaryDirectory(prefix='m06-clock-warm-') as d:\n    root=Path(d);files={'leaf.py':clockleaf,'factory.py':clockfactory,'consumer.py':clockconsumer};write(root,files)\n    layouts.append(dict(id='tighter concrete handled clock partial warm',files=files,transition={'consumer.py':clockconsumer+'\\n# independent edit\\n'},expected=[0,0,0]))\n    cold=gate(root,'tighter handled clock cold',0);warm=gate(root,'tighter handled clock warm',0)\n    for result in (cold,warm):\n        c=contract(result,'invoke')\n        check(c.required_effects==['Clock'],'actual tighter target effect')\n        check(c.failures==['IndexError','OSError','RuntimeError'],'masked target failures independent from effects')\n        check(contract(result,'maker').required_effects==[],'retained clock target not invoked by maker')\n        check(contract(result,'maker').trust==c.trust,'retained complete target trust')\n    write(root,{'consumer.py':clockconsumer+'\\n# independent edit\\n'})\n    partial=gate(root,'tighter handled clock partial warm',0)\n    hits={Path(f.path).name:f.cache_hit for f in partial.results}\n    check(hits['factory.py'] and hits['leaf.py'] and not hits['consumer.py'],'actual clock partial reuse')\n    for name in ('timed','maker','invoke'):\n        check(contract(cold,name).__dict__==contract(partial,name).__dict__,'clock partial exact evidence '+name)\n\ncapturing_factory='# mode: fun\\nfrom pyalamode import effects,Effectful,Clock,ClockCapability\\ndef maker(op:Effectful[[ClockCapability,int],int,Clock])->Effectful[[ClockCapability,int],int,Clock]:\\n    @effects(Clock)\\n    def handled(cap:ClockCapability,x:int)->int:\\n        try:\\n            return op(cap,x)\\n        except RuntimeError:\\n            return 0\\n    return handled\\n'\ncapturing_consumer='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\nfrom factory import maker\\nfrom leaf import timed\\n@effects(Clock)\\ndef invoke(cap:ClockCapability,x:int)->int:\\n    return maker(timed)(cap,x)\\n'\nvariant_leaf='# mode: fun\\nfrom pyalamode import Option,Some\\ndef present(x:int)->Option[int]:\\n    return Some(x)\\n'\nvariant_factory='# mode: fun\\nfrom pyalamode import Option\\nfrom typing import Callable\\nfrom leaf import present\\ndef maker()->Callable[[int],Option[int]]:\\n    return present\\n'\nvariant_consumer='# mode: fun\\nfrom pyalamode import Vector,Option\\nfrom factory import maker\\ndef invoke(values:Vector[int])->Vector[Option[int]]:\\n    return values.map(maker())\\n'\nfor label,files,expected_failures,expected_effects in (\n ('conditional captured handler',{'leaf.py':clockleaf,'factory.py':capturing_factory,'consumer.py':capturing_consumer},['IndexError','KeyError','OSError','ValueError','ZeroDivisionError'],['Clock']),\n ('retained variant callable',{'leaf.py':variant_leaf,'factory.py':variant_factory,'consumer.py':variant_consumer},['RecursionError'],[]),\n):\n    with tempfile.TemporaryDirectory(prefix='m06-partial-') as d:\n        root=Path(d);write(root,files)\n        edited=files['consumer.py']+'\\n# independent body reuse probe\\n'\n        layouts.append(dict(id=label,files=files,transition={'consumer.py':edited},expected=[0,0,0]))\n        cold=gate(root,label+' cold',0);warm=gate(root,label+' warm',0)\n        check(all(f.cache_hit for f in warm.results),label+' full reuse')\n        for result in (cold,warm):\n            check(contract(result,'invoke').failures==expected_failures,label+' callback failure upper bound')\n            check(contract(result,'invoke').required_effects==expected_effects,label+' invocation bound')\n            check(contract(result,'maker').required_effects==[],label+' uninvoked factory bound')\n            check(set(contract(result,'maker').trust)<=set(contract(result,'invoke').trust),label+' complete retained trust')\n            if label=='conditional captured handler':\n                evidence=contract(result,'maker.handled').callable_capture_evidence['op']\n                check(evidence['conditional'] and evidence['effect_bound']==['Clock'],label+' conditional capture evidence')\n            else:\n                check(any('domains-v1' in trust for trust in contract(result,'maker').trust),label+' retained variant foundation')\n        write(root,{'consumer.py':edited});partial=gate(root,label+' partial warm',0)\n        hits={Path(f.path).name:f.cache_hit for f in partial.results}\n        check(hits['leaf.py'] and hits['factory.py'] and not hits['consumer.py'],label+' actual partial reuse')\n        for name in ('maker','invoke'):\n            check(contract(cold,name).__dict__==contract(partial,name).__dict__,label+' exact serialized evidence '+name)\n\nwriters=(\n ('case class method','from domain import Lookup\\nLookup.Found.__init__.__code__=unknown\\n'),\n ('case imported assigned alias','from domain import Lookup\\nAlias=Lookup.Found\\nAlias.__match_args__=()\\n'),\n ('case setter alias','from domain import Lookup\\nfrom builtins import setattr as write\\nwrite(Lookup.Found,\"__match_args__\",())\\n'),\n ('private variant helper','from pyalamode.variants import _case_info as helper\\nhelper.__code__=unknown\\n'),\n ('private variant metaclass method','from pyalamode.variants import _DomainType\\n_DomainType.__setattr__.__code__=unknown\\n'),\n ('private failure helper','from pyalamode.failures import failure_value as helper\\nhelper.__code__=unknown\\n'),\n ('failure record method','from pyalamode import Failure\\nFailure.__init__.__code__=unknown\\n'),\n ('failure builtin native identity','import builtins\\nbuiltins.ZeroDivisionError=Exception\\n'),\n ('variant GenericAlias identity','import types\\ntypes.GenericAlias=unknown\\n'),\n ('variant descriptor foundation','import types\\ntypes.GetSetDescriptorType=unknown\\n'),\n ('Option contained Some writer','from pyalamode import Some\\nSome.__setattr__=unknown\\n'),\n ('Option contained Nothing alias','from pyalamode.variants import Nothing as Alias\\nAlias.__eq__.__code__=unknown\\n'),\n ('Option nested Vector writer','from pyalamode import Some\\nSome.__setattr__=unknown\\n'),\n ('Result contained Ok writer','from pyalamode import Ok\\nOk.__setattr__=unknown\\n'),\n ('Result nested tuple Err writer','from pyalamode.variants import Err as Alias\\nAlias.__init__.__code__=unknown\\n'),\n)\nfor label,writer in writers:\n    with tempfile.TemporaryDirectory(prefix='m06-writer-') as d:\n        selected_consumer=('# mode: fun\\nfrom pyalamode import Result,Ok,Err,Failure,failure_value\\ndef probe(x:int)->Result[int,Failure]:\\n    try:\\n        return Ok(10//x)\\n    except ZeroDivisionError as caught:\\n        return Err(failure_value(caught))\\n') if 'failure' in label else explicit\n        if label.startswith(('Option','Result')):\n            schema='Vector[Option[int]]' if 'Vector' in label else 'tuple[Result[int,str]]' if 'tuple' in label else 'Option[int]' if label.startswith('Option') else 'Result[int,str]'\n            selected_consumer='# mode: fun\\nfrom pyalamode import Vector,Option,Result\\ndef probe(x:'+schema+')->'+schema+':\\n    return x\\n'\n        root=Path(d);files={'domain.py':domain,'consumer.py':selected_consumer,'writer.py':'pass\\n'};write(root,files)\n        layouts.append(dict(id=label,files=files,transition={'writer.py':writer},expected=[0,0,1]))\n        gate(root,label+' cold',0);warm=gate(root,label+' warm',0)\n        check(all(f.cache_hit for f in warm.results),label+' warm original')\n        write(root,{'writer.py':writer});changed=gate(root,label+' changed writer',1)\n        affected=next(f for f in changed.results if Path(f.path).name=='consumer.py')\n        check(not affected.cache_hit or (not affected.verified and all('unverified' in c.source_evidence for c in affected.contracts)),label+' consumer evidence invalidated')\n        fresh=gate(root,label+' fresh writer',1,cache=False)\n        built=build_paths(root=root,output=root/'artifact')\n        check(built.status==1 and not (root/'artifact').exists(),label+' no artifact')\n\nresult=dict(assertions=checks,rows=rows,literal_layouts=layouts)\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'project-observations.json')).write_text(json.dumps(result,indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,layouts=len(layouts),checks=len(rows))))\n",
  "runtime_probe.py": "import json,sys\nfrom pathlib import Path\nfrom pyalamode import (variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,\n                      Result,Ok,Err,accumulate,Failure,failure_value,freeze,thaw,state)\nfrom pyalamode.boundaries import validate_data\nfrom pyalamode.records import _annotation_schema\n\nchecks=0\ndef check(value,label):\n    global checks\n    checks+=1\n    if not value:\n        raise AssertionError(label)\ndef raises(kind,operation,label):\n    global checks\n    checks+=1\n    try:\n        operation()\n    except kind:\n        return\n    raise AssertionError(label)\n\n@record\nclass Payload:\n    number:int\n    labels:Vector[str]\n\n@variant\nclass Lookup:\n    @case\n    class Found:\n        item:Payload\n    @case\n    class Missing:\n        pass\n\n@variant\nclass Pair:\n    @case\n    class Data:\n        left:Option[int]\n        right:Result[Vector[int],str]\n\nfirst=Lookup.Found(Payload(7,Vector.of('a','b')))\nsame=Lookup.Found(Payload(7,Vector.of('a','b')))\ndifferent=Lookup.Found(Payload(8,Vector.of('a','b')))\ncheck(first==same,'nested case equivalence')\ncheck(first!=different,'nested case payload difference')\ncheck(first!=Lookup.Missing(),'tag distinction')\ncheck(Some(True)!=Some(1),'bool int Option distinction')\ncheck(Ok(True)!=Ok(1),'bool int Result distinction')\ncheck(Some(1)!=Ok(1),'domain distinction')\ncheck(Nothing()==Nothing(),'absence equivalence')\ncheck(Lookup.Missing()==Lookup.Missing(),'zero case equivalence')\ncheck(Vector.of(first)==Vector.of(same),'collection nested variants')\ncheck(OrderedMap.of(('x',first))==OrderedMap.of(('x',same)),'ordered map nested variants')\ncheck(Map.of(('x',first))==Map.of(('x',same)),'map nested variants')\ncheck(Pair.Data(Some(1),Ok(Vector.of(2)))==Pair.Data(Some(1),Ok(Vector.of(2))),'generic fields')\ncheck(repr(first)==repr(same),'stable equivalent repr')\ncheck(repr(first).index('number=7')<repr(first).index('labels='),'declaration order in repr')\nraises(AttributeError,lambda:setattr(first,'item',Payload(9,Vector.of())),'case assignment')\nraises(AttributeError,lambda:delattr(first,'item'),'case deletion')\nraises(AttributeError,lambda:first.__init__(Payload(9,Vector.of())),'case reinitialization')\nraises(TypeError,lambda:hash(first),'case unhashable')\nraises(TypeError,lambda:Lookup(),'domain not constructible')\nraises(TypeError,lambda:type('Derived',(Lookup.Found,),{}),'case subclass')\nraises(TypeError,lambda:type('DerivedDomain',(Lookup,),{}),'domain subclass')\nraises(TypeError,lambda:Lookup.Found(),'required payload')\nraises(TypeError,lambda:Lookup.Found(first.item,item=first.item),'duplicate payload')\nraises(TypeError,lambda:Lookup.Found(unknown=first.item),'unknown payload')\nraises(TypeError,lambda:Lookup.Missing(1),'no payload excess')\nraises(TypeError,lambda:Lookup.Found([1]),'mutable case payload')\nraises(TypeError,lambda:Some([1]),'mutable option payload')\nraises(TypeError,lambda:Ok({'x':1}),'mutable success payload')\nraises(TypeError,lambda:Err(([],)),'nested mutable error payload')\nraises(TypeError,lambda:Some(lambda:1),'callable payload')\nraises(TypeError,lambda:Some(state(1)),'capability payload')\nraises(TypeError,lambda:Ok(ValueError('raw')),'raw exception payload')\nclass Integer(int):\n    pass\nraises(TypeError,lambda:Some(Integer(1)),'scalar subclass payload')\nraises(TypeError,lambda:Vector.of([first]),'mutable collection wrapping case')\nraises(TypeError,lambda:Set.of(first),'variant key excluded')\nraises(TypeError,lambda:Map.of((first,1)),'variant map key excluded')\n\nhooks=[]\nclass ForeignMeta(type):\n    def __hash__(self):\n        hooks.append('metahash');return 0\n    def __eq__(self,other):\n        hooks.append('metaeq');return False\n    def __getattribute__(self,name):\n        hooks.append('metaget');return super().__getattribute__(name)\nclass Foreign(metaclass=ForeignMeta):\n    def __getattribute__(self,name):\n        hooks.append('get');return object.__getattribute__(self,name)\n    def __iter__(self):\n        hooks.append('iter');return iter(())\n    def __hash__(self):\n        hooks.append('hash');return 0\n    def __eq__(self,other):\n        hooks.append('eq');return False\n    def __repr__(self):\n        hooks.append('repr');return 'foreign'\n    def __str__(self):\n        hooks.append('str');return 'foreign'\nforeign=Foreign();hooks.clear()\nfor label,operation in (\n ('Some',lambda:Some(foreign)),('Ok',lambda:Ok(foreign)),('Err',lambda:Err(foreign)),\n ('case',lambda:Lookup.Found(foreign)),('Vector',lambda:Vector.of(foreign)),\n ('freeze',lambda:freeze(foreign,exclusive=True)),('thaw',lambda:thaw(foreign)),\n ('failure',lambda:failure_value(foreign)),\n):\n    raises(TypeError,operation,'hook-zero '+label)\n    check(hooks==[],'zero hooks '+label)\ncheck(first!=foreign,'product foreign inequality')\ncheck(hooks==[],'zero equality hooks')\n\nfor value,annotation in ((first,Lookup),(first,Lookup.Found),(Some(1),Option[int]),\n                         (Nothing(),Option[int]),(Ok(1),Result[int,str]),\n                         (Err('bad'),Result[int,str]),(Some(1),Some[int]),\n                         (Ok(1),Ok[int]),(Err('bad'),Err[str])):\n    schema=_annotation_schema(annotation)\n    check(validate_data(value,schema) is value,'schema validate '+str(annotation))\nraises(TypeError,lambda:validate_data(Some(True),_annotation_schema(Option[int])),'exact generic Option schema')\nraises(TypeError,lambda:validate_data(Err(1),_annotation_schema(Result[int,str])),'exact generic error schema')\nraises(TypeError,lambda:validate_data(Ok(True),_annotation_schema(Result[int,str])),'exact generic success schema')\nraises(TypeError,lambda:validate_data(first,_annotation_schema(Option[int])),'wrong domain schema')\nraises(TypeError,lambda:validate_data(Some(foreign),_annotation_schema(Option[int])),'foreign schema hook zero')\ncheck(hooks==[],'schema hooks remain zero')\n\nfor left,right,result in ((Ok(1),Ok('r'),Ok((1,'r'))),(Err('l'),Ok(2),Err(Vector.of('l'))),\n                          (Ok(1),Err('r'),Err(Vector.of('r'))),(Err('l'),Err('r'),Err(Vector.of('l','r')))):\n    check(accumulate(left,right)==result,'ordered binary validation')\norder=[]\ndef supplied(label,value):\n    order.append(label);return value\ncombined=accumulate(supplied('left',Err('one')),supplied('right',Err('two')))\ncheck(order==['left','right'],'argument order')\ncheck(combined==Err(Vector.of('one','two')),'two independent errors')\nraises(TypeError,lambda:accumulate(Some(1),Ok(2)),'unknown accumulation input')\nraises(TypeError,lambda:accumulate(foreign,Ok(2)),'foreign accumulation input')\ncheck(hooks==[],'accumulation hook zero')\n\ncheck(freeze(first) is first,'admitted case snapshot reuse')\nsnapshot=freeze([first,first],exclusive=True,schema=Vector[Lookup])\ncheck(snapshot==Vector.of(first,first),'mutable outer independent snapshot')\nexport=thaw(first);other=thaw(first)\ncheck(export=={'variant':'__main__:Lookup','case':'Found','fields':{'item':{'number':7,'labels':['a','b']}}},'domain export envelope')\nexport['fields']['item']['labels'].append('changed')\ncheck(other['fields']['item']['labels']==['a','b'],'fresh repeated export')\ncheck(first.item.labels==Vector.of('a','b'),'export cannot change variant')\ncopies=thaw(snapshot)\ncopies[0]['fields']['item']['labels'].append('only first')\ncheck(copies[1]['fields']['item']['labels']==['a','b'],'fresh repeated occurrence')\ncheck(thaw(Some(Vector.of(1)))=={'variant':'pyalamode:Option','case':'Some','fields':{'value':[1]}},'builtin Option export')\ncheck(thaw(Nothing())=={'variant':'pyalamode:Option','case':'Nothing','fields':{}},'builtin absence export')\ncheck(thaw(Err(Vector.of('a','b')))=={'variant':'pyalamode:Result','case':'Err','fields':{'error':['a','b']}},'builtin Result export')\n\nfixed={ZeroDivisionError:'division by zero',IndexError:'index out of range',KeyError:'key not found',\n       ValueError:'invalid value',RecursionError:'recursion limit reached',RuntimeError:'runtime operation failed',\n       OSError:'operating system operation failed',UnicodeError:'unicode operation failed'}\nfor kind,message in fixed.items():\n    exception=kind(foreign)\n    exception.extra=foreign\n    converted=failure_value(exception)\n    check(type(converted) is Failure,'exact Failure')\n    check(converted.category==kind.__name__,'exact native category')\n    check(converted.message==message,'fixed native message')\n    check(failure_value(exception)==converted,'repeat equivalent failure')\n    check(failure_value(exception) is not converted,'fresh failure value')\n    check(thaw(converted)=={'category':kind.__name__,'message':message},'Failure fresh record export')\n    check(hooks==[],'no exception args formatting')\nfor kind in (BlockingIOError,ChildProcessError,ConnectionError,BrokenPipeError,ConnectionAbortedError,\n             ConnectionRefusedError,ConnectionResetError,FileExistsError,FileNotFoundError,InterruptedError,\n             IsADirectoryError,NotADirectoryError,PermissionError,ProcessLookupError,TimeoutError):\n    converted=failure_value(kind())\n    check(converted.category=='OSError','finite OS exact subtype')\n    check(converted.message==fixed[OSError],'finite OS fixed message')\nfor exception in (UnicodeDecodeError('utf-8',b'\\xff',0,1,'unknown'),\n                  UnicodeEncodeError('utf-8','x',0,1,'unknown'),UnicodeTranslateError('x',0,1,'unknown')):\n    converted=failure_value(exception)\n    check(converted.category=='UnicodeError','finite Unicode exact subtype')\n    check(converted.message==fixed[UnicodeError],'finite Unicode fixed message')\nclass CustomFailure(ValueError):\n    def __str__(self):hooks.append('exceptionstr');return 'bad'\n    def __repr__(self):hooks.append('exceptionrepr');return 'bad'\n    def __getattribute__(self,name):hooks.append('exceptionget');return object.__getattribute__(self,name)\nfor exception in (CustomFailure(),Exception(),BaseException(),TypeError(),StopIteration()):\n    raises(TypeError,lambda:failure_value(exception),'unsupported exception universe')\n    check(hooks==[],'unsupported exception no hooks')\nfailure=Failure('arbitrary','data')\nraises(AttributeError,lambda:setattr(failure,'category','changed'),'immutable failure fields')\nraises(TypeError,lambda:Failure(True,'bad'),'exact failure strings')\ncheck(hooks==[],'final hook zero')\n\ntarget=Path(__file__).parent/(sys.argv[1] if len(sys.argv)>1 else 'runtime-observations.json')\ntarget.write_text(json.dumps(dict(assertions=checks,hook_calls=hooks),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,hook_calls=hooks)))\n",
  "static_probe.py": "import hashlib,json,sys\nfrom pathlib import Path\nfrom pyalamode.checker import analyze_source\n\ndirectory=Path(__file__).parent\ncases=json.loads((directory/'literal-cases.json').read_text())\nrows=[]\nfor case in cases:\n    result=analyze_source(case['source'],path='<m06_'+case['id']+'>')\n    probe=next((c for c in result.contracts if c.name=='probe'),None)\n    problems=[]\n    if result.status!=case['expected']:\n        problems.append('status')\n    if case.get('selected') is not None and result.selected_functions<case['selected']:\n        problems.append('selection')\n    if not result.status and probe:\n        for key in ('failures','required_effects','effect_bound'):\n            if key in case and sorted(case[key])!=getattr(probe,key):\n                problems.append(key)\n    rows.append(dict(id=case['id'],expected=case['expected'],observed=result.status,\n                     selected=result.selected_functions,problems=problems,\n                     diagnostics=[d.__dict__ for d in result.diagnostics],\n                     contract=probe.__dict__ if probe else None))\nreport=dict(corpus_sha256=hashlib.sha256((directory/'literal-cases.json').read_bytes()).hexdigest(),\n            rows=rows,unexpected=[r for r in rows if r['problems']])\ntarget=directory/(sys.argv[1] if len(sys.argv)>1 else 'static-observations.json')\ntarget.write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(cases=len(rows),unexpected=[dict(id=r['id'],problems=r['problems'],expected=r['expected'],observed=r['observed'],diagnostics=[d['reason'] for d in r['diagnostics']]) for r in report['unexpected']])))\nraise SystemExit(bool(report['unexpected']))\n"
}
```

## Actual reproduction and platform reports

Native final invocation was `.venv/bin/python /tmp/pyalamode-m06-review.RcjEJM/final_probe.py /Volumes/Projects/pyalamode native`. Linux built a wheel from a temporary copy of current pyproject/README/product sources; wheel SHA-256 is `02fe2b45f5d684cd58595834c2ded881ca0ce2ed75a350fff3c98df653bc587a` (104,742 bytes). Actual installation ran `python -m pip install --no-index --no-deps --target /review/installed /review/wheels/pyalamode-0.1.0-py3-none-any.whl` before the final harness, in `python:3.13.1-slim` with `--network none`, read-only `/workspace` checkout, `/review` mounted temporary reviewer directory, working directory `/review` and `PYTHONPATH=/review/installed`. Actual Linux invocation was `python /review/final_probe.py /workspace linux`. The full suite command in each driver is the actual interpreter plus `-m unittest discover -s CHECKOUT_ROOT/tests -p m*.py`. The original wheel install is successful; isolated wheel build dependency setup occurred outside the checkout before the container run.

Temporary full raw evidence remains at `/tmp/pyalamode-m06-review.RcjEJM/{native,linux}-{final,static,runtime,project,cli,nonexecution,freshness}.json` for root inspection. These reports below retain actual environments, subprocess outputs and suite output; the shared full maps follow separately.

```json
{
  "native": {
    "name": "native",
    "environment": {
      "python": "3.13.1 (main, Dec  3 2024, 17:59:52) [Clang 16.0.0 (clang-1600.0.26.4)]",
      "executable": "/Volumes/Projects/pyalamode/.venv/bin/python",
      "platform": "macOS-26.6.2-arm64-arm-64bit-Mach-O",
      "machine": "arm64",
      "gil_enabled": true,
      "py_gil_disabled": 0,
      "package_path": "/Volumes/Projects/pyalamode/pyalamode/__init__.py"
    },
    "results": [
      {
        "script": "static_probe.py",
        "status": 0,
        "elapsed_seconds": 0.5190834591630846,
        "stdout": "{\"cases\": 236, \"unexpected\": []}\n",
        "stderr": "",
        "output": "native-static.json"
      },
      {
        "script": "runtime_probe.py",
        "status": 0,
        "elapsed_seconds": 0.03895604191347957,
        "stdout": "{\"assertions\": 192, \"hook_calls\": []}\n",
        "stderr": "",
        "output": "native-runtime.json"
      },
      {
        "script": "project_probe.py",
        "status": 0,
        "elapsed_seconds": 0.7775072089862078,
        "stdout": "{\"assertions\": 207, \"layouts\": 28, \"checks\": 85}\n",
        "stderr": "",
        "output": "native-project.json"
      },
      {
        "script": "cli_probe.py",
        "status": 0,
        "elapsed_seconds": 2.4340655421838164,
        "stdout": "{\"assertions\": 76, \"commands\": 37, \"layouts\": 5}\n",
        "stderr": "",
        "output": "native-cli.json"
      },
      {
        "script": "nonexecution_probe.py",
        "status": 0,
        "elapsed_seconds": 0.19500724994577467,
        "stdout": "{\"assertions\": 78, \"sentinels\": 14, \"layouts\": 15}\n",
        "stderr": "",
        "output": "native-nonexecution.json"
      },
      {
        "script": "freshness_probe.py",
        "status": 0,
        "elapsed_seconds": 0.907973333960399,
        "stdout": "{\"assertions\": 42, \"transitions\": 12}\n",
        "stderr": "",
        "output": "native-freshness.json"
      }
    ],
    "suite": {
      "status": 0,
      "elapsed_seconds": 3.9943612080533057,
      "stdout": "",
      "stderr": "..................................................................................................................................................................................................................................................\n----------------------------------------------------------------------\nRan 242 tests in 3.871s\n\nOK\n",
      "tests": 242,
      "reported_seconds": 3.871
    },
    "source_unchanged": true,
    "installed_source_equal": true
  },
  "linux": {
    "name": "linux",
    "environment": {
      "python": "3.13.1 (main, Feb  4 2025, 12:52:11) [GCC 12.2.0]",
      "executable": "/usr/local/bin/python",
      "platform": "Linux-5.15.49-linuxkit-aarch64-with-glibc2.36",
      "machine": "aarch64",
      "gil_enabled": true,
      "py_gil_disabled": 0,
      "package_path": "/review/installed/pyalamode/__init__.py"
    },
    "results": [
      {
        "script": "static_probe.py",
        "status": 0,
        "elapsed_seconds": 2.3730137509992346,
        "stdout": "{\"cases\": 236, \"unexpected\": []}\n",
        "stderr": "",
        "output": "linux-static.json"
      },
      {
        "script": "runtime_probe.py",
        "status": 0,
        "elapsed_seconds": 0.05091133400128456,
        "stdout": "{\"assertions\": 192, \"hook_calls\": []}\n",
        "stderr": "",
        "output": "linux-runtime.json"
      },
      {
        "script": "project_probe.py",
        "status": 0,
        "elapsed_seconds": 3.7489784179997514,
        "stdout": "{\"assertions\": 207, \"layouts\": 28, \"checks\": 85}\n",
        "stderr": "",
        "output": "linux-project.json"
      },
      {
        "script": "cli_probe.py",
        "status": 0,
        "elapsed_seconds": 3.037270543001796,
        "stdout": "{\"assertions\": 76, \"commands\": 37, \"layouts\": 5}\n",
        "stderr": "",
        "output": "linux-cli.json"
      },
      {
        "script": "nonexecution_probe.py",
        "status": 0,
        "elapsed_seconds": 0.5220876250004949,
        "stdout": "{\"assertions\": 78, \"sentinels\": 14, \"layouts\": 15}\n",
        "stderr": "",
        "output": "linux-nonexecution.json"
      },
      {
        "script": "freshness_probe.py",
        "status": 0,
        "elapsed_seconds": 0.7868744580009661,
        "stdout": "{\"assertions\": 42, \"transitions\": 12}\n",
        "stderr": "",
        "output": "linux-freshness.json"
      }
    ],
    "suite": {
      "status": 0,
      "elapsed_seconds": 14.102808006000487,
      "stdout": "",
      "stderr": "..................................................................................................................................................................................................................................................\n----------------------------------------------------------------------\nRan 242 tests in 13.905s\n\nOK\n",
      "tests": 242,
      "reported_seconds": 13.905
    },
    "source_unchanged": true,
    "installed_source_equal": true
  }
}
```

## Complete current cross-platform source identity map

All 70 entries below are identical in native-before, native-after, Linux-before and Linux-after maps and have been rehashed against current checkout/reviewer files. The `reviewer:` prefix denotes the reconstructed outside-checkout directory. Checkout entries include every package Python file, all tests and fixtures, all examples, all M1–M6 benchmark harnesses and shared helper, pyproject and README. Inline literal fixtures are inputs of the hashed drivers and separately published above. This output document is excluded to avoid a circular digest. Installed package maps independently contain the 13 `pyalamode/` Python entries below, including launcher; both imported installed copies equal these checkout bytes. Helper runtime maps contain 12 foundations and eight owned inputs, independently reconciled with these entries.

```json
{
  "README.md": "aa0813f5b9bfa320f3bb5d64137b0b78db26d4cf1515664ed4cb42f4ac347fc5",
  "benchmarks/m01_scalar.py": "c84afa054ee636c9a9bdcf001894043b26b81ffd1adb96398c1fae89056a6132",
  "benchmarks/m02_modules.py": "5d28d376907f3aa27810bf04a1d04b000fd26869568826e44b3e65d4765f790c",
  "benchmarks/m03_collections.py": "f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141",
  "benchmarks/m04_boundaries.py": "be56c03b4bd1845baf5cd1e37071e8dce94a0e0430780d45bcf8d4a88b1ffef5",
  "benchmarks/m05_effects.py": "83b54c93ecc4240f340bcc88ba20b16f8a640306d49f784c26662cfe22bb22d3",
  "benchmarks/m06_domains.py": "7a192a8cfed4b29c22d990414d03a49ed6c525c428a2874684368d393d7275af",
  "examples/collections/__init__.py": "4bb3c9c16ae4b554d4fa71a406310b1807033b61c7ec2ced586f0616e7eb2418",
  "examples/collections/core.py": "f9b05387462f4ae1009df83fe8d407b07d4767e3d567e307a14ec09185ca61db",
  "examples/collections/demo.py": "039cc3ca4b04c72ecced2276037a4182866a16c18f10c26d0d2cf8389fb2fa98",
  "examples/domains/demo.py": "130c85d8e2790cd049f0c60adc07a644ef3f63c9a295735ebde4d43ca728474d",
  "examples/domains/domain.py": "3aea9061e61670529e9ceb9bdea477c8af359ab1d96ddf60596f18cd0bc0ac12",
  "examples/effects/__init__.py": "976d6c1731a16ecf67980cfaddeed34d9f0182df1aeabb5a8e60720709a1f8b6",
  "examples/effects/core.py": "f18f5a58a03e37bb619319121deaf8a59a2ef5fc516142e342a433e23ded174c",
  "examples/effects/demo.py": "9f4d1340e900f8232461e59fcfa720f79b28a13fdc1dc168c7eb24c69dfe40dd",
  "examples/modules/__init__.py": "76f92b53e625d8faf18131c3c6f2cd841fd35f5b1b61a2dd969e2c99b7ca5936",
  "examples/modules/calculations.py": "aab5a0781bad61a88ece1f3140385cbbf75c3fb4db9bb1c2ecb86eb6ea699eba",
  "examples/modules/constants.py": "74d9245e93fbe88a079e3fc74ca865648475f21edea90696388b4981abdc7813",
  "examples/modules/demo.py": "8bdd18276448d091ecedb396bedc7d0cbc9ac1e079b7dfc21c1f92c7b145a556",
  "examples/pricing.py": "e94c9435d25f4f11658a583e4dd287f149717b2d470970d362d2cc09555ea7f0",
  "examples/records/__init__.py": "0def8ab59c34cd9fd81bb1c5ceb3c534209245af8616add6e597215812611d9e",
  "examples/records/core.py": "f13caca1f361bae7a58d7bca0d10e41ceac79f03ba4826a7ed9d70b7fffdfcc2",
  "examples/records/demo.py": "a0e0e6456ad3aa38adaeb8b538886b8ff46965f7026eb34eb10daace76e16f18",
  "examples/scalar.py": "0507c266d4bff0287693b9a6ec8b7f3db8da265aee6eecbde50ccc855fa90a6a",
  "pyalamode/__init__.py": "073ee6f161b19df7bcf2dcdf148e45dec7872649f84e85e7d1c9508bc71b6cf6",
  "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
  "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
  "pyalamode/checker.py": "f524a5db7c97bd0df889b709b5cc6101576cd10b9f8092fb68dada1aadfcd0f0",
  "pyalamode/cli.py": "315af58cde488384815bdb8968393c33eec5b0bc93917237c55dc103726d5ee5",
  "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
  "pyalamode/effects.py": "31d3ee92aaf256fe92f29fa221941d6fac41115fb6c87e4b31503639776a9dfa",
  "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
  "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
  "pyalamode/model.py": "ea09503e2203feedc26e0efd4b602c3a4887d5e3bae1976e9ff70f56e342c90c",
  "pyalamode/project.py": "a9a35d1358fd3f4532222dc2c977ba0da07d7f444a6e1a70079dc8ab704d62d4",
  "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
  "pyalamode/variants.py": "02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d",
  "pyproject.toml": "7b993e35b0c738d99b2ab823c05f4599b73655ddfb48fe3af06fe5f8b378ebeb",
  "tests/fixtures/m01/invalid_reassignment.py": "9fd746a84247b3bf809537318a6b5202844eefe1a181cd6d9546bfef8f77f7cf",
  "tests/fixtures/m02/changing_capture.py": "371fd5f6c50b65c425056fe6b3e9c1efa7a69acc8f4cf9c5a484790263c21ceb",
  "tests/fixtures/m02/effectful_initializer.py": "32535add5e080ad8e1f3a21338271ceca42a8df81a10d4389d0b5313e5a25965",
  "tests/fixtures/m02/nested_mutable_tuple.py": "262a0801f7a8651137edaa00014ca55367650ece9d7bf948596eca30e266fbc1",
  "tests/fixtures/m03/effectful_callback.py": "c50377aa374a12a3f30d7e4b3855d87d65a30773b3a59059b159b5d46d07950b",
  "tests/fixtures/m03/ignored_update.py": "61273bf75865d171b57b0e1e36a6a26b03b4ba4493a5ab4f8de1d3160f93eadf",
  "tests/fixtures/m03/nested_mutable.py": "2a6d3ad7a043f9e9b504ab334d5e9c2c96d0c520660ec6bf8fe0ab1f62855943",
  "tests/fixtures/m04/missing_snapshot_precondition.py": "4bf2d9a4fa9355670cbd5934d644fd741c486ec64c400a3e74a0458e9cec3258",
  "tests/fixtures/m04/nested_record_mutable.py": "3a6621d963a0f840fd7448f17f27c3a1fdc62c07342e93945d13d36202115d8a",
  "tests/fixtures/m04/unsupported_getter.py": "0c7bccb953b884150127246521e9902431e3e60aaf4d55e795c84fda750b1e78",
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
  "tests/m05_runtime.py": "543a0ce687072a8527887bc79e20ef4308797b38cfb7ddf7d0e95056fccd1a21",
  "tests/m06_domains.py": "76dd88436fa1efabcd3b30c53e68c8f6e3fd70d811cf5900b08f852965335187",
  "tests/m06_runtime.py": "9f035ba5d1969839abd1452ebe38d09a400db3a35536bfb4dcf80d62ac7c59da",
  "reviewer:cli_probe.py": "318a19f6a1c8dba3bee98651d6157b39e44c7b5cf4f8879dab8060953d12cbc5",
  "reviewer:final_probe.py": "e9e737110a6f2ddd5799f972f5936637bf07dcc13ab77218a82385c82f34384c",
  "reviewer:freshness_probe.py": "e981fdee013e9c2140bbf619004723eec5d3fdf11706753b64552d27dd8e6d39",
  "reviewer:make_cases.py": "6cb4d20fc7537bde89d721ea2e4ba37e96938bcb8c08761baa1af11636386550",
  "reviewer:nonexecution_probe.py": "d8fd3094bf9e6daa5eeefa6bd19f9ef581ddc1b35e858973fc49fa110d509ef4",
  "reviewer:project_probe.py": "5d345502f4b3b8c7d9b8e0019cbf90ebe27efa101e0ee369d018a5151104974f",
  "reviewer:runtime_probe.py": "c8eef2d0cb8f4d486cddaa0f7b940b4e5f17b4518541159cb531c559cd989e8b",
  "reviewer:static_probe.py": "a9f6eeb50728a547761217ac23b62a8f984a1614d5e6af506fad68f17e3c4d63",
  "reviewer:literal-cases.json": "15cc3949409763e122db23262cf1c7a842821a9145d63286434c0daace4721bd"
}
```

## Current authority and inspected evidence identities

These are current hashes of separately read authority/handoffs and final inspected evidence, rather than a claim those documents were all frozen before every earlier implementation probe. The full executable input before/after claim is the 70-entry map above.

```json
{
  "SPEC-sol6.1-composite.md": "3d8f845b5b3739418062caa44db5ba51b95bc99823425bde3b4aff6cebaaee48",
  "Docs/milestones/01-scalar.md": "5f4532c826880868dae9f6af65eba45ea9d343f8fb95b8732e0e27d63ba17c4d",
  "Docs/milestones/02-modules.md": "fb370d6447b18e2913f3e4f1f40e0018f893ae30e621a9ef3e3b0826156c3775",
  "Docs/milestones/03-collections.md": "10d74df5d6b38b49d31d60e3159a581d990e9e6e2783f36c257e46d3c2083cff",
  "Docs/milestones/04-records.md": "a8034077f244a5badb52d770f7b432b20c794f59047e34bfba955bc817391634",
  "Docs/milestones/05-effects.md": "d26a2c31a0f72ae40c88b18526cdd6dde1bbc2fdbf107e76cce4b4048ec862e4",
  "Docs/milestones/06-domains.md": "7005da2fbc9c36f4f595ac07a17cf96e393f4ab8ecfb5c4f78d9e291af7ec065",
  "Docs/evidence/m06-runtime-contract.md": "9c1292ce605d1d98718a8db33e068be0866c68498f4c20a41e4b0953e64c0e2a",
  "Docs/evidence/m06-runtime-measurements.md": "4dc925318769e68dc6713bb492d1ccc21187dd4e331058865f4f800e984c3d67",
  "Docs/evidence/m06-runtime-macos.json": "dab2c31906ec972c5f37e75957dcd81b3a3c13fbc27257f4b694e6ef959873bd",
  "Docs/evidence/m06-runtime-linux.json": "5c5dc7585d86e4ffdc4201729cf1d4eba73ae879a71e347b4165e5809864809a"
}
```
