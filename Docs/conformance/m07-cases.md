# M7 independent conformance review

Status: the independent frozen-source M7 conformance matrix passed on native macOS and an actual freshly installed Linux wheel. All 532 fixed source outcomes agree, both complete suites pass 286 tests, and helper measurements have been independently reconciled. Root retains the release decision. Target-user usefulness and authoring benefit remain **UNMEASURED**.

Authority read in full: `SPEC-sol6.1-composite.md` (545 lines), particularly §§3–5, 7–12, 16–18, A21 and A32. The inherited engineering baseline is M1–M6 commit `48b56a9`, CPython 3.13.1 standard GIL on native macOS arm64 and actual Linux Docker. Review ownership is only this file; probes and fixtures are created outside the checkout. Main and runtime workers own implementation. Root owns catalog approval, admission, source freeze, ledger, Git and the release decision.

## Fixed adversarial plan

This plan is published before checking the forthcoming M7 vocabulary. Once root approves the operation catalog, each row is instantiated as exact literal source/input, assigned a fixed admit/refuse/result/effect/failure expectation and hashed before readiness. Expected outcomes will not be changed merely to match observations; corrections, narrowed scope and reruns remain visible. Every newly admitted operation must first have its exact signature/types, runtime/version identity, callback/capture behavior, ordering/ties/error selection, aliases, failures, dependencies, initialization evidence, supported environment, representative use case, adversarial counterexamples and named performance implications published.

| Plan IDs | Fixed independent obligation |
| --- | --- |
| S01–S12 | Every catalog operation: exact supported source target; alias; module-qualified form only if catalogued; supported and unsupported arity/keywords/types; ordinary stock-Python result and characterized failures; no arbitrary protocol dispatch. |
| T01–T12 | Text/bytes and any numeric conversion: exact subclasses, bool/int distinction, custom operators/truth/equality/hash/getters/iteration/formatting; empty/edge/Unicode/negative/large values; integer digit-limit and codec/locale/context assumptions. Unlisted methods, codecs, numeric forms and arbitrary error handlers refuse. |
| P01–P10 | Parsing/encoding: finite explicit schema, malformed input, bounds, canonical output/order and first-error behavior; no constructors/restoration hooks, object aliases, callables/capabilities, ambient codecs or locale dependence concealed as pure. |
| F01–F12 | Filesystem/clock/environment: pure lexical processing versus capability calls; exact input and output; all declared effect families retained through direct, helper, callback and handled-failure paths; fake providers retain classification; setup and import initialization evidence/policy separately visible. |
| H01–H20 | Eager fold/scan/group/result traversal: Vector/ordered inputs only; deterministic left-to-right callback calls, accumulator/result schema, empty input, first failure, tie/group order and independent accumulated errors; unsupported unordered/general iterable/generator routes refuse. Concrete, conditional, returned and captured callbacks carry actual effect/failure/trust/capture bounds. |
| C01–C20 | Composition/partial application: actual target and all latent calls remain in evidence; argument/return/capture contracts, arity and invocation order; captured data stable and exact; unknown/capability/effectful captures, wrong signature, conditional alternatives, nested returned calls and handled failures cannot disappear. Callable annotations alone do not prove purity. |
| W01–W16 | Analyzed replacement of every public/private new product operation, transitive helper and native dependency through direct/from/module aliases, class writers and writer helpers; spelling alone never admits a replaced operation. Actual foundation/native inventories and source bytes participate in freshness. |
| I01–I12 | Import, default, decorator, annotation, class-local-default and initializer sentinels remain unevaluated by check/build; pure invocation and effectful required setup appear separately in reports and policy decisions. Inherited class-local/default and generated-name collision regressions remain checked. |
| K01–K12 | Cache clear/cold/full-warm/partial checks agree on strict admission and report effects/failures/dependencies/targets; relevant source, operation bytes, native identity/environment and policy changes invalidate relevant claims. Cache loss cannot change admission. |
| B01–B12 | Actual CLI check/audit/build/run and source execution: unsuccessful gates produce no artifact and no application side effects; off artifacts preserve exact source bytes; exports/debug guard coverage rejects supported invalid data before body and preserves ordinary valid results without callback/capability purity claims. |
| R01–R12 | Independent runtime constructor/hook/alias/order/failure tests and direct measurements inspect implementation and helper evidence after source freeze; supported exact inputs do not invoke unknown hooks; old versions and fresh exports retain invariants. |
| X01–X08 | Exact supported native and actual Linux CPython 3.13.1 standard GIL focused/full suites plus literal corpus, CLI and nonexecution probes; Linux fresh installed wheel inventory includes every actual installed product Python file and launcher. This is M7 operation verification, not an M11 consumer-distribution claim. |

The final report will publish complete literal sources and layouts, harness text, exact expected/observed outcomes, assertion and recorded-row counts separate from subprocess counts, environment and command provenance, named full source/current/cross/before/after identity maps, actual installed-byte equality and inspected helper evidence identities. `git diff --check` does not cover an untracked document; this file will receive an explicit whitespace inspection or staged-equivalent check. No unsupported Windows, free-threaded, alternative-runtime, later external-trust approval, editor, package-consumer, builder, Task or dialect claim will be inferred.

## Target-user measurement protocol

Before any usefulness claim, recruit application developers who routinely parse small data, transform ordered values and isolate filesystem/clock/environment work. Give each the published catalog and an ordinary Python fixture, record prior Python experience, then time a successful checked core, repair of one exact-type violation, callback effect failure and one setup/invocation policy distinction. Record completion/abandonment, repairs, diagnostic comprehension, ordinary execution and catalog coverage. Report sample size and tasks individually. No recruited users or completed observations exist in this review.

## Readiness and evidence

Completed: catalog approval preceded exact literal instantiation; expectations were fixed before observation; root explicitly authorized the joint source freeze before final native/Linux and measured intervals. The final bounded observations, identities and remaining scope limits appear below. Earlier preapproval and interim findings are retained as provenance.

Root supplied a preapproval native CPython 3.13.1 counterexample: registering a custom `codecs.register_error("strict", handler)` changes `_codecs.utf_8_encode("\ud800", "strict")` and `_codecs.utf_8_decode(b"\xff", "strict")` into replacement success and invokes that handler. A low-level codec entry point therefore does not itself establish independence from Python's error-handler registry. T/P's fixed ambient-handler obligation will be instantiated as an isolated-process registration sentinel across malformed encode/decode and valid boundary code points. Approved UTF-8 behavior must retain its published UnicodeError failures and valid results without that sentinel firing; the proposed codec mechanism is not yet approved.

Root also reproduced the same registry dispatch through inherited live IO: an invalid UTF-8 file read and a surrogate text write both returned custom replacements and invoked the changed handler. The joint approval must characterize that route too. The fixed isolated probe includes live read/write malformed data, zero registry hits, CRLF and BOM preservation, cleanup, permissions and the documented write ordering (open/truncate before encoding failure), independently of retained IO effect evidence. Historical M5/M6 passes do not discharge this newly concrete counterexample.

## Frozen M7 literal source corpus

Root approved the joint catalog and runtime contract before this instantiation. The complete M7 corpus below is fixed before any admission observation: 269 cases, 108 expected admits and 161 expected refusals; SHA-256 `288563ab1d86d55480b70d657cad25f8fe43360cad3aa9ecc24126f331225b88`. The inherited 236 exact M6 sources are additionally replayed; its pure conditional callback expectations F41/F42 add UnicodeError according to the approved M7 envelope, while the ValueError handler continues to discharge UnicodeError. Combined expected counts are 505 rows, 181 admits and 324 refusals. Case count is distinct from runtime assertions and subprocesses.

```json
[
  {
    "id": "S01a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text,separator)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S01b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split as operation\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return operation(text,separator)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S01c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text,separator)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S01d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return standard.text_split(text,separator)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S01e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(value:Vector[str]=text_split(\"a,b\",\",\"))->Vector[str]:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S01f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\nvalue=text_split(\"a,b\",\",\")\ndef probe()->Vector[str]:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S01g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split()\n",
    "expected": 1
  },
  {
    "id": "S01h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text,separator,0)\n",
    "expected": 1
  },
  {
    "id": "S01i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text=text)\n",
    "expected": 1
  },
  {
    "id": "S01j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(*(\"a,b\",\",\",))\n",
    "expected": 1
  },
  {
    "id": "S01k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(1,separator)\n",
    "expected": 1
  },
  {
    "id": "S01l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\ntext_split=unknown\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text,separator)\n",
    "expected": 1
  },
  {
    "id": "S01m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\nAlias=text_split\nAlias.__code__=unknown\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text,separator)\n",
    "expected": 1
  },
  {
    "id": "S01n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_split\n@fun\ndef probe(text:str,separator:str)->Vector[str]:\n    return text_split(text,separator)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'),',')\n",
    "expected": 1
  },
  {
    "id": "S02a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(parts,separator)\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S02b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join as operation\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return operation(parts,separator)\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S02c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(parts,separator)\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S02d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return standard.text_join(parts,separator)\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S02e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(value:str=text_join(Vector.of(\"a\",\"b\"),\",\"))->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S02f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\nvalue=text_join(Vector.of(\"a\",\"b\"),\",\")\ndef probe()->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S02g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join()\n",
    "expected": 1
  },
  {
    "id": "S02h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(parts,separator,0)\n",
    "expected": 1
  },
  {
    "id": "S02i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(parts=parts)\n",
    "expected": 1
  },
  {
    "id": "S02j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(*(Vector.of(\"a\",\"b\"),\",\",))\n",
    "expected": 1
  },
  {
    "id": "S02k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join((),separator)\n",
    "expected": 1
  },
  {
    "id": "S02l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\ntext_join=unknown\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(parts,separator)\n",
    "expected": 1
  },
  {
    "id": "S02m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_join\nAlias=text_join\nAlias.__code__=unknown\n@fun\ndef probe(parts:Vector[str],separator:str)->str:\n    return text_join(parts,separator)\n",
    "expected": 1
  },
  {
    "id": "S03a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text,old,new)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S03b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace as operation\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return operation(text,old,new)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S03c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text,old,new)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S03d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return standard.text_replace(text,old,new)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S03e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(value:str=text_replace(\"aaa\",\"aa\",\"b\"))->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S03f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\nvalue=text_replace(\"aaa\",\"aa\",\"b\")\ndef probe()->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S03g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace()\n",
    "expected": 1
  },
  {
    "id": "S03h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text,old,new,0)\n",
    "expected": 1
  },
  {
    "id": "S03i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text=text)\n",
    "expected": 1
  },
  {
    "id": "S03j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(*(\"aaa\",\"aa\",\"b\",))\n",
    "expected": 1
  },
  {
    "id": "S03k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(1,old,new)\n",
    "expected": 1
  },
  {
    "id": "S03l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\ntext_replace=unknown\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text,old,new)\n",
    "expected": 1
  },
  {
    "id": "S03m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\nAlias=text_replace\nAlias.__code__=unknown\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text,old,new)\n",
    "expected": 1
  },
  {
    "id": "S03n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_replace\n@fun\ndef probe(text:str,old:str,new:str)->str:\n    return text_replace(text,old,new)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'),'aa','b')\n",
    "expected": 1
  },
  {
    "id": "S04a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text,prefix)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S04b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith as operation\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return operation(text,prefix)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S04c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text,prefix)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S04d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return standard.text_startswith(text,prefix)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S04e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(value:bool=text_startswith(\"ab\",\"a\"))->bool:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S04f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\nvalue=text_startswith(\"ab\",\"a\")\ndef probe()->bool:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S04g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith()\n",
    "expected": 1
  },
  {
    "id": "S04h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text,prefix,0)\n",
    "expected": 1
  },
  {
    "id": "S04i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text=text)\n",
    "expected": 1
  },
  {
    "id": "S04j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(*(\"ab\",\"a\",))\n",
    "expected": 1
  },
  {
    "id": "S04k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(1,prefix)\n",
    "expected": 1
  },
  {
    "id": "S04l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\ntext_startswith=unknown\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text,prefix)\n",
    "expected": 1
  },
  {
    "id": "S04m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\nAlias=text_startswith\nAlias.__code__=unknown\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text,prefix)\n",
    "expected": 1
  },
  {
    "id": "S04n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_startswith\n@fun\ndef probe(text:str,prefix:str)->bool:\n    return text_startswith(text,prefix)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'),'a')\n",
    "expected": 1
  },
  {
    "id": "S05a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text,start,stop)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S05b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice as operation\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return operation(text,start,stop)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S05c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text,start,stop)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S05d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return standard.text_slice(text,start,stop)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S05e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(value:str=text_slice(\"abc\",0,2))->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S05f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\nvalue=text_slice(\"abc\",0,2)\ndef probe()->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S05g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice()\n",
    "expected": 1
  },
  {
    "id": "S05h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text,start,stop,0)\n",
    "expected": 1
  },
  {
    "id": "S05i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text=text)\n",
    "expected": 1
  },
  {
    "id": "S05j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(*(\"abc\",0,2,))\n",
    "expected": 1
  },
  {
    "id": "S05k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(1,start,stop)\n",
    "expected": 1
  },
  {
    "id": "S05l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\ntext_slice=unknown\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text,start,stop)\n",
    "expected": 1
  },
  {
    "id": "S05m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\nAlias=text_slice\nAlias.__code__=unknown\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text,start,stop)\n",
    "expected": 1
  },
  {
    "id": "S05n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import text_slice\n@fun\ndef probe(text:str,start:int,stop:int)->str:\n    return text_slice(text,start,stop)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'),0,2)\n",
    "expected": 1
  },
  {
    "id": "S06a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value,lower,upper)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S06b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp as operation\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return operation(value,lower,upper)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S06c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value,lower,upper)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S06d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return standard.integer_clamp(value,lower,upper)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S06e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int=integer_clamp(2,0,3))->int:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S06f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\nvalue=integer_clamp(2,0,3)\ndef probe()->int:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S06g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp()\n",
    "expected": 1
  },
  {
    "id": "S06h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value,lower,upper,0)\n",
    "expected": 1
  },
  {
    "id": "S06i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value=value)\n",
    "expected": 1
  },
  {
    "id": "S06j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(*(2,0,3,))\n",
    "expected": 1
  },
  {
    "id": "S06k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(True,lower,upper)\n",
    "expected": 1
  },
  {
    "id": "S06l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\ninteger_clamp=unknown\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value,lower,upper)\n",
    "expected": 1
  },
  {
    "id": "S06m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\nAlias=integer_clamp\nAlias.__code__=unknown\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value,lower,upper)\n",
    "expected": 1
  },
  {
    "id": "S06n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_clamp\n@fun\ndef probe(value:int,lower:int,upper:int)->int:\n    return integer_clamp(value,lower,upper)\nclass Derived(int):\n    pass\nprobe(Derived(123),0,3)\n",
    "expected": 1
  },
  {
    "id": "S07a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S07b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal as operation\n@fun\ndef probe(text:str)->int:\n    return operation(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S07c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S07d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str)->int:\n    return standard.integer_parse_decimal(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S07e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(value:int=integer_parse_decimal(\"123\"))->int:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S07f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\nvalue=integer_parse_decimal(\"123\")\ndef probe()->int:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S07g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal()\n",
    "expected": 1
  },
  {
    "id": "S07h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text,0)\n",
    "expected": 1
  },
  {
    "id": "S07i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text=text)\n",
    "expected": 1
  },
  {
    "id": "S07j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(*(\"123\",))\n",
    "expected": 1
  },
  {
    "id": "S07k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(1)\n",
    "expected": 1
  },
  {
    "id": "S07l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\ninteger_parse_decimal=unknown\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n",
    "expected": 1
  },
  {
    "id": "S07m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\nAlias=integer_parse_decimal\nAlias.__code__=unknown\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n",
    "expected": 1
  },
  {
    "id": "S07n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_parse_decimal\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'))\n",
    "expected": 1
  },
  {
    "id": "S08a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S08b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal as operation\n@fun\ndef probe(value:int)->str:\n    return operation(value)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S08c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S08d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(value:int)->str:\n    return standard.integer_format_decimal(value)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S08e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:str=integer_format_decimal(123))->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S08f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\nvalue=integer_format_decimal(123)\ndef probe()->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S08g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal()\n",
    "expected": 1
  },
  {
    "id": "S08h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value,0)\n",
    "expected": 1
  },
  {
    "id": "S08i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value=value)\n",
    "expected": 1
  },
  {
    "id": "S08j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(*(123,))\n",
    "expected": 1
  },
  {
    "id": "S08k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(True)\n",
    "expected": 1
  },
  {
    "id": "S08l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\ninteger_format_decimal=unknown\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value)\n",
    "expected": 1
  },
  {
    "id": "S08m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\nAlias=integer_format_decimal\nAlias.__code__=unknown\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value)\n",
    "expected": 1
  },
  {
    "id": "S08n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import integer_format_decimal\n@fun\ndef probe(value:int)->str:\n    return integer_format_decimal(value)\nclass Derived(int):\n    pass\nprobe(Derived(123))\n",
    "expected": 1
  },
  {
    "id": "S09a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S09b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode as operation\n@fun\ndef probe(text:str)->bytes:\n    return operation(text)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S09c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S09d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str)->bytes:\n    return standard.utf8_encode(text)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S09e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(value:bytes=utf8_encode(\"Ada\"))->bytes:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S09f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\nvalue=utf8_encode(\"Ada\")\ndef probe()->bytes:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S09g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode()\n",
    "expected": 1
  },
  {
    "id": "S09h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text,0)\n",
    "expected": 1
  },
  {
    "id": "S09i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text=text)\n",
    "expected": 1
  },
  {
    "id": "S09j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(*(\"Ada\",))\n",
    "expected": 1
  },
  {
    "id": "S09k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(1)\n",
    "expected": 1
  },
  {
    "id": "S09l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\nutf8_encode=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "S09m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\nAlias=utf8_encode\nAlias.__code__=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "S09n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_encode\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'))\n",
    "expected": 1
  },
  {
    "id": "S10a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S10b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode as operation\n@fun\ndef probe(data:bytes)->str:\n    return operation(data)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S10c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S10d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(data:bytes)->str:\n    return standard.utf8_decode(data)\n",
    "expected": 0,
    "failures": [
      "UnicodeError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S10e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(value:str=utf8_decode(b\"Ada\"))->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S10f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\nvalue=utf8_decode(b\"Ada\")\ndef probe()->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S10g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode()\n",
    "expected": 1
  },
  {
    "id": "S10h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data,0)\n",
    "expected": 1
  },
  {
    "id": "S10i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data=data)\n",
    "expected": 1
  },
  {
    "id": "S10j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(*(b\"Ada\",))\n",
    "expected": 1
  },
  {
    "id": "S10k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(1)\n",
    "expected": 1
  },
  {
    "id": "S10l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\nutf8_decode=unknown\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data)\n",
    "expected": 1
  },
  {
    "id": "S10m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\nAlias=utf8_decode\nAlias.__code__=unknown\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data)\n",
    "expected": 1
  },
  {
    "id": "S10n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import utf8_decode\n@fun\ndef probe(data:bytes)->str:\n    return utf8_decode(data)\nclass Derived(bytes):\n    pass\nprobe(Derived(b'Ada'))\n",
    "expected": 1
  },
  {
    "id": "S11a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S11b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode as operation\n@fun\ndef probe(data:bytes)->str:\n    return operation(data)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S11c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S11d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(data:bytes)->str:\n    return standard.hex_encode(data)\n",
    "expected": 0,
    "failures": [],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S11e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(value:str=hex_encode(b\"Ada\"))->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S11f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\nvalue=hex_encode(b\"Ada\")\ndef probe()->str:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S11g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode()\n",
    "expected": 1
  },
  {
    "id": "S11h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data,0)\n",
    "expected": 1
  },
  {
    "id": "S11i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data=data)\n",
    "expected": 1
  },
  {
    "id": "S11j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(*(b\"Ada\",))\n",
    "expected": 1
  },
  {
    "id": "S11k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(1)\n",
    "expected": 1
  },
  {
    "id": "S11l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\nhex_encode=unknown\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data)\n",
    "expected": 1
  },
  {
    "id": "S11m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\nAlias=hex_encode\nAlias.__code__=unknown\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data)\n",
    "expected": 1
  },
  {
    "id": "S11n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_encode\n@fun\ndef probe(data:bytes)->str:\n    return hex_encode(data)\nclass Derived(bytes):\n    pass\nprobe(Derived(b'Ada'))\n",
    "expected": 1
  },
  {
    "id": "S12a",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S12b",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode as operation\n@fun\ndef probe(text:str)->bytes:\n    return operation(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S12c",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode.standard import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S12d",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pyalamode.standard as standard\n@fun\ndef probe(text:str)->bytes:\n    return standard.hex_decode(text)\n",
    "expected": 0,
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "effect_bound": []
  },
  {
    "id": "S12e",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(value:bytes=hex_decode(\"416461\"))->bytes:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S12f",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\nvalue=hex_decode(\"416461\")\ndef probe()->bytes:\n    return value\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "S12g",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode()\n",
    "expected": 1
  },
  {
    "id": "S12h",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text,0)\n",
    "expected": 1
  },
  {
    "id": "S12i",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text=text)\n",
    "expected": 1
  },
  {
    "id": "S12j",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(*(\"416461\",))\n",
    "expected": 1
  },
  {
    "id": "S12k",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(1)\n",
    "expected": 1
  },
  {
    "id": "S12l",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\nhex_decode=unknown\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text)\n",
    "expected": 1
  },
  {
    "id": "S12m",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\nAlias=hex_decode\nAlias.__code__=unknown\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text)\n",
    "expected": 1
  },
  {
    "id": "S12n",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import hex_decode\n@fun\ndef probe(text:str)->bytes:\n    return hex_decode(text)\nclass Derived(str):\n    pass\nprobe(Derived('Ada'))\n",
    "expected": 1
  },
  {
    "id": "H01",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,add,0)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H02",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,parity)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H03",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,good)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H04",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->int:\n    return values.fold(add,0)\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  },
  {
    "id": "H01-unordered",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Set[int])->Vector[int]:\n    return vector_scan(values,add,0)\n",
    "expected": 1
  },
  {
    "id": "H01-iterable",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:tuple[int,...])->Vector[int]:\n    return vector_scan(values,add,0)\n",
    "expected": 1
  },
  {
    "id": "H01-unknown",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,unknown,0)\n",
    "expected": 1
  },
  {
    "id": "H01-lambda",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,lambda a,b:a+b,0)\n",
    "expected": 1
  },
  {
    "id": "H01-mutable",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,add,[])\n",
    "expected": 1
  },
  {
    "id": "H01-arity",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,add)\n",
    "expected": 1
  },
  {
    "id": "H01-keyword",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,add,initial=0)\n",
    "expected": 1
  },
  {
    "id": "H01-init",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef add(a:int,b:int)->int:\n    return a+b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,add,0)\nvalue=probe(Vector.of(1))\n",
    "expected": 1
  },
  {
    "id": "H02-unordered",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Set[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,parity)\n",
    "expected": 1
  },
  {
    "id": "H02-iterable",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:tuple[int,...])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,parity)\n",
    "expected": 1
  },
  {
    "id": "H02-unknown",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,unknown)\n",
    "expected": 1
  },
  {
    "id": "H02-lambda",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,lambda x:x)\n",
    "expected": 1
  },
  {
    "id": "H02-mutable",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return [x]\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,parity)\n",
    "expected": 1
  },
  {
    "id": "H02-arity",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,parity,0)\n",
    "expected": 1
  },
  {
    "id": "H02-keyword",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,callback=parity)\n",
    "expected": 1
  },
  {
    "id": "H02-init",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef parity(x:int)->int:\n    return x%2\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,parity)\nvalue=probe(Vector.of(1))\n",
    "expected": 1
  },
  {
    "id": "H03-unordered",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Set[int])->Result[Vector[int],str]:\n    return result_traverse(values,good)\n",
    "expected": 1
  },
  {
    "id": "H03-iterable",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:tuple[int,...])->Result[Vector[int],str]:\n    return result_traverse(values,good)\n",
    "expected": 1
  },
  {
    "id": "H03-unknown",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,unknown)\n",
    "expected": 1
  },
  {
    "id": "H03-lambda",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,lambda x:Ok(x))\n",
    "expected": 1
  },
  {
    "id": "H03-mutable",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok([x])\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,good)\n",
    "expected": 1
  },
  {
    "id": "H03-arity",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values)\n",
    "expected": 1
  },
  {
    "id": "H03-keyword",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,callback=good)\n",
    "expected": 1
  },
  {
    "id": "H03-init",
    "source": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef good(x:int)->Result[int,str]:\n    if x<0:\n        return Err(\"negative\")\n    return Ok(x+1)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,good)\nvalue=probe(Vector.of(1))\n",
    "expected": 1
  },
  {
    "id": "H05-str",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef key(x:int)->str:\n    return \"x\"\n@fun\ndef probe(values:Vector[int])->OrderedMap[str,Vector[int]]:\n    return vector_group_by(values,key)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H05-bool",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef key(x:int)->bool:\n    return x<0\n@fun\ndef probe(values:Vector[int])->OrderedMap[bool,Vector[int]]:\n    return vector_group_by(values,key)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H05-bytes",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef key(x:int)->bytes:\n    return b\"x\"\n@fun\ndef probe(values:Vector[int])->OrderedMap[bytes,Vector[int]]:\n    return vector_group_by(values,key)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H05-None",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef key(x:int)->None:\n    return None\n@fun\ndef probe(values:Vector[int])->OrderedMap[None,Vector[int]]:\n    return vector_group_by(values,key)\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "H06",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef key(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(values,key)\n",
    "expected": 1
  },
  {
    "id": "H07",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef step(a:int,b:int)->str:\n    return \"x\"\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return vector_scan(values,step,0)\n",
    "expected": 1
  },
  {
    "id": "H08",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef bad(x:int)->Option[int]:\n    return Some(x)\n@fun\ndef probe(values:Vector[int])->Result[Vector[int],str]:\n    return result_traverse(values,bad)\n",
    "expected": 1
  },
  {
    "id": "H09",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef probe(values:Vector[int],op:Callable[[int,int],int])->Vector[int]:\n    try:\n        return vector_scan(values,op,0)\n    except ValueError:\n        return Vector.of(0)\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "IndexError",
      "KeyError",
      "RecursionError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "H10",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef probe(values:Vector[str],op:Callable[[str],Result[int,str]])->Result[Vector[int],str]:\n    try:\n        return result_traverse(values,op)\n    except UnicodeError:\n        return Err(\"unicode\")\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "IndexError",
      "KeyError",
      "RecursionError",
      "ValueError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C01",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    return compose(double,plus)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C02",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe()->Callable[[int],int]:\n    return compose(double,plus)\n",
    "expected": 0,
    "latent": true,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C03",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    return partial_first(divide,10)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C04",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe()->Callable[[int],int]:\n    return partial_first(divide,10)\n",
    "expected": 0,
    "latent": true,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C05",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    try:\n        return partial_first(divide,10)(x)\n    except ZeroDivisionError:\n        return 0\n",
    "expected": 0,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C06",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    op=partial_first(divide,10)\n    first=op(x)\n    try:\n        return op(first)\n    except ZeroDivisionError:\n        return 0\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C07",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return values.map(compose(double,plus))\n",
    "expected": 0,
    "required_effects": []
  },
  {
    "id": "C08",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(values:Vector[int])->Vector[int]:\n    return values.map(partial_first(divide,10))\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C09",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int,flag:bool)->int:\n    op=compose(double,plus) if flag else partial_first(divide,10)\n    return op(x)\n",
    "expected": 0,
    "required_effects": [],
    "contains": {
      "failures": [
        "ZeroDivisionError"
      ]
    }
  },
  {
    "id": "C10",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    return compose(compose(double,plus),plus)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C11",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef maker(op:Callable[[int],int])->Callable[[int],int]:\n    return compose(double,op)\n@fun\ndef probe(x:int)->int:\n    return maker(plus)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C12",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef maker(op:Callable[[int,int],int])->Callable[[int],int]:\n    return partial_first(op,10)\n@fun\ndef probe(x:int)->int:\n    return maker(divide)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C13",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(op:Callable[[int],int],x:int)->int:\n    try:\n        return compose(double,op)(x)\n    except ValueError:\n        return 0\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "IndexError",
      "KeyError",
      "RecursionError",
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C14",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(flag:bool)->Callable[[int],int]:\n    return compose(double,plus) if flag else partial_first(divide,10)\n",
    "expected": 0,
    "latent": true,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C15",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef maker(bound:int)->Callable[[int],int]:\n    return partial_first(divide,bound)\n@fun\ndef probe(x:int)->int:\n    return maker(10)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": [
      "ZeroDivisionError"
    ]
  },
  {
    "id": "C16",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    fixed=3\n    def add(y:int)->int:\n        return y+fixed\n    return compose(double,add)(x)\n",
    "expected": 0,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "C-negative-01",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return compose(double,plus,plus)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-02",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return compose(outer=double,inner=plus)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-03",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return compose(double,unknown)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-04",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return partial_first(divide,[])(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-05",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return partial_first(divide,plus)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-06",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return partial_first(divide,state(1))(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-07",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return partial_first(divide)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-08",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return compose(divide,plus)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-09",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\nfrom pyalamode import state\n@fun\ndef probe(x:int)->int:\n    return compose(double,plus)(\"x\")\n",
    "expected": 1
  },
  {
    "id": "C-negative-mutable-capture",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef double(x:int)->int:\n    return x*2\n@fun\ndef divide(a:int,b:int)->int:\n    return a//b\n@fun\ndef probe(x:int)->int:\n    changing=[]\n    def inner(y:int)->int:\n        return changing[0]+y\n    return compose(double,inner)(x)\n",
    "expected": 1
  },
  {
    "id": "C-negative-capcapture",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    def inner(x:int)->int:\n        return cap.now_ns()+x\n    return compose(inner,inner)(1)\n",
    "expected": 1
  },
  {
    "id": "E01",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\n@effects(Clock)\ndef timed(bound:int,cap:ClockCapability)->int:\n    return cap.now_ns()//bound\n@fun\ndef probe()->Effectful[[ClockCapability],int,Clock]:\n    return compose(plus,now)\n",
    "expected": 0,
    "latent": true,
    "required_effects": [],
    "failures": []
  },
  {
    "id": "E02",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\n@effects(Clock)\ndef timed(bound:int,cap:ClockCapability)->int:\n    return cap.now_ns()//bound\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return compose(plus,now)(cap)\n",
    "expected": 0,
    "required_effects": [
      "Clock"
    ],
    "effect_bound": [
      "Clock"
    ],
    "failures": [
      "IndexError",
      "OSError",
      "RuntimeError"
    ]
  },
  {
    "id": "E03",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\n@effects(Clock)\ndef timed(bound:int,cap:ClockCapability)->int:\n    return cap.now_ns()//bound\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    try:\n        return partial_first(timed,0)(cap)\n    except (RuntimeError,OSError,IndexError,ZeroDivisionError):\n        return 0\n",
    "expected": 0,
    "required_effects": [
      "Clock"
    ],
    "effect_bound": [
      "Clock"
    ],
    "failures": []
  },
  {
    "id": "E04",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\n@effects(Clock)\ndef timed(bound:int,cap:ClockCapability)->int:\n    return cap.now_ns()//bound\n@fun\ndef probe(cap:ClockCapability)->int:\n    return compose(plus,now)(cap)\n",
    "expected": 1
  },
  {
    "id": "E05",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\n@effects(Clock)\ndef timed(bound:int,cap:ClockCapability)->int:\n    return cap.now_ns()//bound\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->Callable[[int],int]:\n    return partial_first(timed,cap)\n",
    "expected": 1
  },
  {
    "id": "E06",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\n@effects(Clock)\ndef timed(bound:int,cap:ClockCapability)->int:\n    return cap.now_ns()//bound\n@fun\ndef maker(op:Effectful[[ClockCapability],int,Clock,IO])->Effectful[[ClockCapability],int,Clock,IO]:\n    return compose(plus,op)\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return maker(now)(cap)\n",
    "expected": 0,
    "required_effects": [
      "Clock"
    ],
    "effect_bound": [
      "Clock"
    ],
    "failures": [
      "IndexError",
      "OSError",
      "RuntimeError"
    ]
  },
  {
    "id": "F-IO",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(IO)\ndef probe(cap:IOCapability)->str:\n    return cap.read_text(\"input\")\n",
    "expected": 0,
    "required_effects": [
      "IO"
    ],
    "effect_bound": [
      "IO"
    ],
    "failures": [
      "KeyError",
      "OSError",
      "RuntimeError",
      "UnicodeError",
      "ValueError"
    ]
  },
  {
    "id": "F-IO-handled",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(IO)\ndef probe(cap:IOCapability)->str:\n    try:\n        return cap.read_text(\"input\")\n    except (OSError,RuntimeError,ValueError,IndexError,KeyError):\n        return \"failure\"\n",
    "expected": 0,
    "required_effects": [
      "IO"
    ],
    "effect_bound": [
      "IO"
    ],
    "failures": []
  },
  {
    "id": "F-IO-pure",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef probe(cap:IOCapability)->str:\n    return cap.read_text(\"input\")\n",
    "expected": 1
  },
  {
    "id": "F-Clock",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "expected": 0,
    "required_effects": [
      "Clock"
    ],
    "effect_bound": [
      "Clock"
    ],
    "failures": [
      "IndexError",
      "OSError",
      "RuntimeError"
    ]
  },
  {
    "id": "F-Clock-handled",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    try:\n        return cap.now_ns()\n    except (OSError,RuntimeError,ValueError,IndexError,KeyError):\n        return 0\n",
    "expected": 0,
    "required_effects": [
      "Clock"
    ],
    "effect_bound": [
      "Clock"
    ],
    "failures": []
  },
  {
    "id": "F-Clock-pure",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef probe(cap:ClockCapability)->int:\n    return cap.now_ns()\n",
    "expected": 1
  },
  {
    "id": "F-Environment",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"MODE\",\"off\")\n",
    "expected": 0,
    "required_effects": [
      "Environment"
    ],
    "effect_bound": [
      "Environment"
    ],
    "failures": [
      "OSError",
      "RuntimeError",
      "UnicodeError",
      "ValueError"
    ]
  },
  {
    "id": "F-Environment-handled",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\n@effects(Environment)\ndef probe(cap:EnvironmentCapability)->str:\n    try:\n        return cap.get(\"MODE\",\"off\")\n    except (OSError,RuntimeError,ValueError,IndexError,KeyError):\n        return \"failure\"\n",
    "expected": 0,
    "required_effects": [
      "Environment"
    ],
    "effect_bound": [
      "Environment"
    ],
    "failures": []
  },
  {
    "id": "F-Environment-pure",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\n@fun\ndef probe(cap:EnvironmentCapability)->str:\n    return cap.get(\"MODE\",\"off\")\n",
    "expected": 1
  },
  {
    "id": "N01",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport json\n@fun\ndef probe()->int:\n    return json.loads(\"{}\")\n",
    "expected": 1
  },
  {
    "id": "N02",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport pickle\n@fun\ndef probe()->int:\n    return pickle.loads(b\"x\")\n",
    "expected": 1
  },
  {
    "id": "N03",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport codecs\n@fun\ndef probe()->str:\n    return codecs.decode(b\"x\",\"utf-8\")\n",
    "expected": 1
  },
  {
    "id": "N04",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport locale\n@fun\ndef probe()->int:\n    return locale.atoi(\"12\")\n",
    "expected": 1
  },
  {
    "id": "N05",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport os\n@fun\ndef probe()->str:\n    return os.getenv(\"MODE\")\n",
    "expected": 1
  },
  {
    "id": "N06",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nimport time\n@fun\ndef probe()->int:\n    return time.time_ns()\n",
    "expected": 1
  },
  {
    "id": "N07",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom functools import partial\n@fun\ndef probe()->int:\n    return partial(abs,1)()\n",
    "expected": 1
  },
  {
    "id": "N08",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->str:\n    return \"x\".format()\n",
    "expected": 1
  },
  {
    "id": "N09",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->bytes:\n    return \"x\".encode(\"utf-8\")\n",
    "expected": 1
  },
  {
    "id": "N10",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->str:\n    return b\"x\".decode(\"utf-8\")\n",
    "expected": 1
  },
  {
    "id": "N11",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->int:\n    return int(\"12\")\n",
    "expected": 1
  },
  {
    "id": "N12",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->str:\n    return str(12)\n",
    "expected": 1
  },
  {
    "id": "N13",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->int:\n    return sum(Vector.of(1,2))\n",
    "expected": 1
  },
  {
    "id": "N14",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\n\n@fun\ndef probe()->Vector[int]:\n    return sorted(Vector.of(1,2))\n",
    "expected": 1
  },
  {
    "id": "W01",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nfrom pyalamode.standard import _exact as helper\nhelper.__code__=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W02",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nimport pyalamode.standard as std\nstd.__dict__[\"utf8_decode\"]=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W03",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nimport pyalamode as pal\nAlias=pal.standard\nAlias.__dict__.update({\"integer_parse_decimal\":unknown})\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W04",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nfrom pyalamode import utf8_encode as operation\nfrom builtins import setattr as change\nchange(operation,\"__code__\",unknown)\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W05",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nimport builtins\nbuiltins.ord=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W06",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nfrom builtins import chr as helper\nhelper.__code__=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W07",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nimport builtins\nbuiltins.UnicodeDecodeError=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W08",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nfrom pyalamode.collections import _validate as helper\nhelper.__code__=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  },
  {
    "id": "W09",
    "source": "from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\nfrom typing import Callable\nfrom pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\nfrom pyalamode.variants import _validate_case as helper\nhelper.__code__=unknown\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
    "expected": 1
  }
]
```

## Frozen supplemental intermediate-validation literals

Six additional literals instantiate the fixed callback/failure plan after code inspection identified that compose validates intermediate B as well as R. The expected RecursionError for nonscalar B, and its discharge by a RuntimeError handler, follow the inherited validation contract and are fixed before observing these inputs. The initial 269 source corpus and its digest are unchanged. Supplemental SHA-256 `cd9032e387ba18e9def9c6d8f5ba8039d2807e0c40991c7b22795f8488144aa2`.

```json
[
  {
    "id": "V01",
    "source": "from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\nfrom typing import Callable\n@fun\ndef one(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef size(values:Vector[int])->int:\n    return len(values)\n@fun\ndef nonempty(values:Vector[int])->bool:\n    return len(values)>0\n@fun\ndef probe(x:int)->int:\n    return compose(size,one)(x)\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": []
  },
  {
    "id": "V02",
    "source": "from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\nfrom typing import Callable\n@fun\ndef one(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef size(values:Vector[int])->int:\n    return len(values)\n@fun\ndef nonempty(values:Vector[int])->bool:\n    return len(values)>0\n@fun\ndef probe(x:Vector[int])->Vector[int]:\n    return x.map(compose(size,one))\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": []
  },
  {
    "id": "V03",
    "source": "from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\nfrom typing import Callable\n@fun\ndef one(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef size(values:Vector[int])->int:\n    return len(values)\n@fun\ndef nonempty(values:Vector[int])->bool:\n    return len(values)>0\n@fun\ndef probe(x:Vector[int])->Vector[int]:\n    return x.filter(compose(nonempty,one))\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": []
  },
  {
    "id": "V04",
    "source": "from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\nfrom typing import Callable\n@fun\ndef one(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef size(values:Vector[int])->int:\n    return len(values)\n@fun\ndef nonempty(values:Vector[int])->bool:\n    return len(values)>0\n@fun\ndef probe(x:Vector[int])->OrderedMap[int,Vector[int]]:\n    return vector_group_by(x,compose(size,one))\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": []
  },
  {
    "id": "V05",
    "source": "from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\nfrom typing import Callable\n@fun\ndef one(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef size(values:Vector[int])->int:\n    return len(values)\n@fun\ndef nonempty(values:Vector[int])->bool:\n    return len(values)>0\n@fun\ndef maker()->Callable[[int],int]:\n    return compose(size,one)\n@fun\ndef probe(x:int)->int:\n    return maker()(x)\n",
    "expected": 0,
    "failures": [
      "RecursionError"
    ],
    "required_effects": []
  },
  {
    "id": "V06",
    "source": "from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\nfrom typing import Callable\n@fun\ndef one(x:int)->Vector[int]:\n    return Vector.of(x)\n@fun\ndef size(values:Vector[int])->int:\n    return len(values)\n@fun\ndef nonempty(values:Vector[int])->bool:\n    return len(values)>0\n@fun\ndef probe(x:int)->int:\n    try:\n        return compose(size,one)(x)\n    except RuntimeError:\n        return 0\n",
    "expected": 0,
    "failures": [],
    "required_effects": []
  }
]
```

## Approved OS environment narrowing and additional refusal

The root-approved native target now requires UTF-8 filesystem encoding and surrogateescape filesystem errors. CPython patch/platform alone was insufficient: an actual network-disabled Docker 3.13.1 process under LC_ALL=C, PYTHONUTF8=0 and PYTHONCOERCECLOCALE=0 reported ASCII filesystem encoding; a replaced surrogateescape handler then converted the valid scalar name café into replacement bytes. The checker/build must refuse that target with tooling status 2, and ordinary live IO/environment provider setup must fail RuntimeError before native encoding. Roots, relative paths and environment names exclude every surrogate code point before native conversion. Native environment decoding of malformed stored bytes remains a separately characterized operation: FF, encoded surrogate bytes and every byte 80–FF are observed as native DC escapes with zero changed-handler calls. Manual standard UTF-8 remains independent of both registries. These conditions are tested in isolated subprocesses and are not a claim about unsupported startup environments.

Root clarified partial_first B as stable data or an exact capability; arbitrary Callable B is outside this catalog. The one additional refusal literal is frozen separately, leaving the earlier digests unchanged; SHA-256 `dc7db1d9179338435d2cd5ac8ebc53c2910f367e9509ba2153fcccf028ef3328`. Combined sources now total 512: 187 expected admits and 325 expected refusals.

```json
[
  {
    "id": "V07",
    "source": "from pyalamode import fun,partial_first\nfrom typing import Callable\n@fun\ndef apply(bound:int,op:Callable[[int],int])->int:\n    return op(bound)\n@fun\ndef plus(x:int)->int:\n    return x+1\n@fun\ndef probe()->int:\n    return partial_first(apply,3)(plus)\n",
    "expected": 1
  }
]
```

## Frozen literal layouts

The 42 exact M7 project/CLI/nonexecution layouts were instantiated from the approved catalog before readiness; SHA-256 `07673e4ec850fb1e4b374639df564eb002fdee9e65a5fe027a21e1db3c835ef2`. Paths created by the drivers are temporary execution locations; every source string and transition is listed here.

```json
[
  {
    "id": "wrapper returned handled partial warm",
    "files": {
      "leaf.py": "# mode: fun\ndef plus(x:int)->int:\n    return x+1\ndef divide(a:int,b:int)->int:\n    return a//b\n",
      "factory.py": "# mode: fun\nfrom typing import Callable\nfrom pyalamode import compose,partial_first\nfrom leaf import plus,divide\ndef maker()->Callable[[int],int]:\n    return compose(plus,partial_first(divide,10))\n",
      "consumer.py": "# mode: fun\nfrom factory import maker\ndef probe(x:int)->int:\n    try:\n        return maker()(x)\n    except ZeroDivisionError:\n        return 0\n"
    },
    "expected": 0,
    "transition": {
      "consumer.py": "# mode: fun\nfrom factory import maker\ndef probe(x:int)->int:\n    try:\n        return maker()(x)\n    except ZeroDivisionError:\n        return 0\n\n# independent consumer edit\n"
    },
    "failures": [],
    "effects": []
  },
  {
    "id": "wrapper returned unhandled partial warm",
    "files": {
      "leaf.py": "# mode: fun\ndef plus(x:int)->int:\n    return x+1\ndef divide(a:int,b:int)->int:\n    return a//b\n",
      "factory.py": "# mode: fun\nfrom typing import Callable\nfrom pyalamode import compose,partial_first\nfrom leaf import plus,divide\ndef maker()->Callable[[int],int]:\n    return compose(plus,partial_first(divide,10))\n",
      "consumer.py": "# mode: fun\nfrom factory import maker\ndef probe(x:int)->int:\n    return maker()(x)\n"
    },
    "expected": 0,
    "transition": {
      "consumer.py": "# mode: fun\nfrom factory import maker\ndef probe(x:int)->int:\n    return maker()(x)\n\n# independent consumer edit\n"
    },
    "failures": [
      "ZeroDivisionError"
    ],
    "effects": []
  },
  {
    "id": "factory parameter concrete specialization partial warm",
    "files": {
      "leaf.py": "# mode: fun\ndef plus(x:int)->int:\n    return x+1\ndef divide(a:int,b:int)->int:\n    return a//b\n",
      "factory.py": "# mode: fun\nfrom typing import Callable\nfrom pyalamode import compose,partial_first\nfrom leaf import plus,divide\ndef maker(op:Callable[[int,int],int])->Callable[[int],int]:\n    return compose(plus,partial_first(op,10))\n",
      "consumer.py": "# mode: fun\nfrom factory import maker\nfrom leaf import divide\ndef probe(x:int)->int:\n    try:\n        return maker(divide)(x)\n    except ZeroDivisionError:\n        return 0\n"
    },
    "expected": 0,
    "transition": {
      "consumer.py": "# mode: fun\nfrom factory import maker\nfrom leaf import divide\ndef probe(x:int)->int:\n    try:\n        return maker(divide)(x)\n    except ZeroDivisionError:\n        return 0\n\n# independent consumer edit\n"
    },
    "failures": [],
    "effects": []
  },
  {
    "id": "factory tighter concrete effects partial warm",
    "files": {
      "leaf.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\ndef plus(x:int)->int:\n    return x+1\n",
      "factory.py": "# mode: fun\nfrom pyalamode import compose,Effectful,Clock,IO,ClockCapability\nfrom leaf import plus\ndef maker(op:Effectful[[ClockCapability],int,Clock,IO])->Effectful[[ClockCapability],int,Clock,IO]:\n    return compose(plus,op)\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\nfrom leaf import now\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    try:\n        return maker(now)(cap)\n    except RuntimeError:\n        return 0\n"
    },
    "expected": 0,
    "transition": {
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\nfrom leaf import now\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    try:\n        return maker(now)(cap)\n    except RuntimeError:\n        return 0\n\n# independent consumer edit\n"
    },
    "failures": [
      "IndexError",
      "OSError"
    ],
    "effects": [
      "Clock"
    ]
  },
  {
    "id": "writer public operation method",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "from pyalamode import utf8_encode as operation\noperation.__code__=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer public operation assigned alias",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "from pyalamode import utf8_encode\nAlias=utf8_encode\nAlias.__defaults__=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer private exact helper",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "from pyalamode.standard import _exact as helper\nhelper.__code__=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer private standard module dictionary",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import pyalamode.standard as standard\nstandard.__dict__[\"_exact\"]=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer package standard attribute",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import pyalamode as product\nproduct.standard.utf8_encode=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer stdlib Unicode error identity",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.UnicodeEncodeError=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer native ord direct",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.ord=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer native chr alias module",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins as native\nAlias=native\nAlias.chr=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer private collection helper",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "from pyalamode.collections import _validate as helper\nhelper.__code__=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer private variants helper",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "from pyalamode.variants import _validate_case as helper\nhelper.__code__=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer writer setattr alias",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "from pyalamode import utf8_encode\nfrom builtins import setattr as write\nwrite(utf8_encode,\"__code__\",unknown)\n"
    },
    "changed_expected": 1
  },
  {
    "id": "writer writer module dictionary update",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import pyalamode.standard as standard\nstandard.__dict__.update({\"utf8_encode\":unknown})\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation type",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.type=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation int",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.int=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation str",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.str=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation bytes",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.bytes=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation len",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.len=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation ord",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.ord=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation chr",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.chr=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation enumerate",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.enumerate=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation range",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.range=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation tuple",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.tuple=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation list",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.list=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation object",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.object=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation TypeError",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.TypeError=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation ValueError",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.ValueError=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation UnicodeEncodeError",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.UnicodeEncodeError=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "native foundation UnicodeDecodeError",
    "files": {
      "core.py": "from pyalamode import fun,utf8_encode,integer_parse_decimal\n@fun\ndef probe(text:str)->bytes:\n    return utf8_encode(text)\n",
      "writer.py": "pass\n"
    },
    "expected": 0,
    "transition": {
      "writer.py": "import builtins\nbuiltins.UnicodeDecodeError=unknown\n"
    },
    "changed_expected": 1
  },
  {
    "id": "separate ordinary setup and pure invocation",
    "files": {
      "setup.py": "from pyalamode import fun,integer_parse_decimal,live_io,live_clock,live_environment,recorded_clock,recorded_environment\nfrom pathlib import Path\ndef mark():\n    Path(\"sentinel\").write_text(\"executed\")\n    return 0\nmark()\nfiles=live_io(\".\",allowed_ops=(\"read_text\",\"write_text\"))\nclock=live_clock()\nsettings=live_environment()\nrecorded=recorded_clock((3,4))\nrecorded_settings=recorded_environment(((\"MODE\",\"test\"),))\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n"
    },
    "expected": 0,
    "setup_observations": true
  },
  {
    "id": "strict import refuses ordinary setup",
    "files": {
      "setup.py": "from pyalamode import fun,integer_parse_decimal,live_io,live_clock,live_environment,recorded_clock,recorded_environment\nfrom pathlib import Path\ndef mark():\n    Path(\"sentinel\").write_text(\"executed\")\n    return 0\nmark()\nfiles=live_io(\".\",allowed_ops=(\"read_text\",\"write_text\"))\nclock=live_clock()\nsettings=live_environment()\nrecorded=recorded_clock((3,4))\nrecorded_settings=recorded_environment(((\"MODE\",\"test\"),))\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n",
      "consumer.py": "# mode: fun\nfrom setup import probe\ndef calculation()->int:\n    return probe(\"12\")\n"
    },
    "expected": 1
  },
  {
    "id": "guard off",
    "files": {
      "core.py": "from pyalamode import fun,text_split,integer_parse_decimal,Vector,Result,Failure,Ok,Err,result_traverse,failure_value\n@fun\ndef parse(text:str)->Result[int,Failure]:\n    try:\n        return Ok(integer_parse_decimal(text))\n    except ValueError as caught:\n        return Err(failure_value(caught))\n@fun\ndef probe(text:str)->Result[Vector[int],Failure]:\n    return result_traverse(text_split(text,\",\"),parse)\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"off\"\n"
    },
    "expected": 0,
    "mode": "off"
  },
  {
    "id": "guard exports",
    "files": {
      "core.py": "from pyalamode import fun,text_split,integer_parse_decimal,Vector,Result,Failure,Ok,Err,result_traverse,failure_value\n@fun\ndef parse(text:str)->Result[int,Failure]:\n    try:\n        return Ok(integer_parse_decimal(text))\n    except ValueError as caught:\n        return Err(failure_value(caught))\n@fun\ndef probe(text:str)->Result[Vector[int],Failure]:\n    return result_traverse(text_split(text,\",\"),parse)\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"exports\"\nguarded_exports=[\"core:probe\"]\n"
    },
    "expected": 0,
    "mode": "exports"
  },
  {
    "id": "guard debug",
    "files": {
      "core.py": "from pyalamode import fun,text_split,integer_parse_decimal,Vector,Result,Failure,Ok,Err,result_traverse,failure_value\n@fun\ndef parse(text:str)->Result[int,Failure]:\n    try:\n        return Ok(integer_parse_decimal(text))\n    except ValueError as caught:\n        return Err(failure_value(caught))\n@fun\ndef probe(text:str)->Result[Vector[int],Failure]:\n    return result_traverse(text_split(text,\",\"),parse)\n",
      "pyproject.toml": "[tool.pyalamode]\nboundary_guards=\"debug\"\nguarded_exports=[\"core:probe\"]\n"
    },
    "expected": 0,
    "mode": "debug"
  },
  {
    "id": "nonexecution default",
    "files": {
      "core.py": "from pyalamode import fun,integer_parse_decimal,vector_scan,Vector\nfrom pathlib import Path\ndef mark(*args):\n    Path(\"sentinel\").write_text(\"executed\")\n    return \"1\"\n@fun\ndef probe(text:str=mark())->int:\n    return integer_parse_decimal(text)\n"
    },
    "expected": 1,
    "sentinel": true
  },
  {
    "id": "nonexecution annotation",
    "files": {
      "core.py": "from pyalamode import fun,integer_parse_decimal,vector_scan,Vector\nfrom pathlib import Path\ndef mark(*args):\n    Path(\"sentinel\").write_text(\"executed\")\n    return \"1\"\n@fun\ndef probe(text:mark())->int:\n    return 1\n"
    },
    "expected": 1,
    "sentinel": true
  },
  {
    "id": "nonexecution initializer",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,integer_parse_decimal,vector_scan,Vector\nfrom pathlib import Path\ndef mark(*args):\n    Path(\"sentinel\").write_text(\"executed\")\n    return \"1\"\nvalue=mark()\ndef probe()->int:\n    return 1\n"
    },
    "expected": 1,
    "sentinel": true
  },
  {
    "id": "nonexecution callback",
    "files": {
      "core.py": "from pyalamode import fun,integer_parse_decimal,vector_scan,Vector\nfrom pathlib import Path\ndef mark(*args):\n    Path(\"sentinel\").write_text(\"executed\")\n    return \"1\"\n@fun\ndef probe(x:Vector[int])->Vector[int]:\n    return vector_scan(x,mark,0)\n"
    },
    "expected": 1,
    "sentinel": true
  },
  {
    "id": "entry effect policy refuses wrapper",
    "files": {
      "leaf.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\n@effects(Clock)\ndef now(cap:ClockCapability)->int:\n    return cap.now_ns()\ndef plus(x:int)->int:\n    return x+1\n",
      "factory.py": "# mode: fun\nfrom pyalamode import compose,Effectful,Clock,IO,ClockCapability\nfrom leaf import plus\ndef maker(op:Effectful[[ClockCapability],int,Clock,IO])->Effectful[[ClockCapability],int,Clock,IO]:\n    return compose(plus,op)\n",
      "consumer.py": "# mode: fun\nfrom pyalamode import effects,Clock,ClockCapability\nfrom factory import maker\nfrom leaf import now\n@effects(Clock)\ndef probe(cap:ClockCapability)->int:\n    try:\n        return maker(now)(cap)\n    except RuntimeError:\n        return 0\n",
      "pyproject.toml": "[tool.pyalamode.effect_bounds]\n\"consumer:probe\"=[]\n"
    },
    "expected": 1
  }
]
```

## Complete inherited literal sources

These 236 M6 source bytes and initial expectations are unchanged. The static harness below applies only the expressly approved UnicodeError envelope updates to F41/F42, without editing historical source bytes or admission/refusal outcomes. Inherited project callback envelope expectations receive the same approved update.

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

## Complete frozen reproduction harness

All executable reviewer inputs below are outside the checkout at `/tmp/pyalamode-m07-review.ey3fnwr8`. They cover the complete 512 source rows, 42 new and 48 inherited literal project/CLI/nonexecution layouts, actual library and artifact execution, 15 installed product Python files, changed product bytes, native conditions and full suites. Source fixture digests remain unchanged. The earlier interim harness assumption that debug originals must be unguarded was corrected before this freeze: exports originals remain unguarded, while debug originals intentionally receive supported data assertions. Optional CLI run is explicitly unsupported (status 2); actual accepted artifacts execute through stock Python. Source checking is never evaluated user code.

Harness SHA-256 map:

```json
{
  "cli_probe.py": "251cc975f42f3b3c678021fa4cd8afea1e8a1474a00aee8c4495c484518fed0e",
  "environment_probe.py": "2b16da1d5c5bdc1132c00e2a92b4c3c1aca27c5cc49edf5f1c610b750ad99b49",
  "final_probe.py": "a2b5d0e566036ee8a8ab7c8cd05195e9bde7f12595a4b8810e68166523c853b3",
  "freshness_probe.py": "1b7155a377fe27d92541996044e26a2cfc5e5780c65397c626d44501292eeb30",
  "m06_cli_probe.py": "be44b9bf2d611fa580c5d88045c373f78ef4671246dff7fab85abc9e5180799a",
  "m06_freshness_probe.py": "e981fdee013e9c2140bbf619004723eec5d3fdf11706753b64552d27dd8e6d39",
  "m06_nonexecution_probe.py": "d8fd3094bf9e6daa5eeefa6bd19f9ef581ddc1b35e858973fc49fa110d509ef4",
  "m06_project_probe.py": "e9dd75392a8198925edf7641dce3a9178abfb132048ac80c1e20a75f4cad854e",
  "m06_runtime_probe.py": "c8eef2d0cb8f4d486cddaa0f7b940b4e5f17b4518541159cb531c559cd989e8b",
  "make_cases.py": "d3de5400f1d0238e4a46e66f2a699920cb4f62afdbba90683569a27f43d6b5c6",
  "make_layouts.py": "bd1e4e48627d32ea034aab2e987b5ebe87cab955587487edbb6bb01e9e61c78e",
  "make_supplement.py": "efc84afdb89e1b5aa35af783dc36d245f0a8d7c622111e2786cbe18e4f5573f6",
  "project_probe.py": "ada8aeb6267f3986e073e8b5ac161e524ee7c6be6e867de01b35e39c2f41e3df",
  "runtime_probe.py": "77516e940c97ef1f7fcf2c1184e26d7c68eeb12c24748557160e8c282c3c9dd7",
  "static_probe.py": "cad6bcc229d545b1be64a29a352a62c2e6e41982bc6233dc61c53e751a43ad75"
}
```

Complete harness file contents:

```json
{
  "cli_probe.py": "import json,os,subprocess,sys,tempfile\nfrom pathlib import Path\nOUT=Path(__file__).parent;checks=0;rows=[]\nlayouts=json.loads((OUT/'literal-layouts.json').read_text())\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\ndef call(root,label,args,status):\n ran=subprocess.run([sys.executable,'-m','pyalamode',*args],cwd=root,capture_output=True,text=True)\n check(ran.returncode==status,label+' status '+str(ran.returncode)+' '+ran.stderr)\n rows.append(dict(label=label,args=args,status=ran.returncode,stdout=ran.stdout,stderr=ran.stderr))\n return json.loads(ran.stdout) if '--json' in args else None\ndef write(root,files):\n for name,source in files.items():(root/name).write_text(source)\nfor layout in layouts:\n if layout.get('mode') or layout.get('sentinel') or layout.get('setup_observations') or layout['id']=='strict import refuses ordinary setup':\n  with tempfile.TemporaryDirectory(prefix='m07-cli-') as d:\n   root=Path(d);write(root,layout['files']);label=layout['id'];status=layout['expected']\n   checked=call(root,label+' check',['check','--root',str(root),'--no-cache','--json'],status)\n   check(checked['verified']==(status==0),label+' verification dimension');check(not (root/'sentinel').exists(),label+' check sentinel absent')\n   audited=call(root,label+' audit',['check','--root',str(root),'--audit','--no-cache','--json'],0)\n   check(not audited['verified'],label+' audit no certificate')\n   built=call(root,label+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],status)\n   check((root/'artifact').exists()==(status==0),label+' no failed artifact');check(not (root/'sentinel').exists(),label+' build sentinel absent')\n   if not status:\n    env=dict(os.environ);env['PYTHONPATH']=str(root/'artifact')+os.pathsep+env.get('PYTHONPATH','')\n    if layout.get('mode'):\n     mode=layout['mode'];source=layout['files']['core.py']\n     if mode=='off':check((root/'artifact/core.py').read_text()==source,'off source bytes unchanged')\n     code='import core\\nfrom pyalamode import Ok,Err,Vector,Failure\\nassert core.probe(\"1,2,-3\")==Ok(Vector.of(1,2,-3))\\nassert core.probe(\"1,bad,3\")==Err(Failure(\"ValueError\",\"invalid value\"))\\nassert core.probe.__dict__=={}\\n'\n     if mode!='off':\n      code+='from pyalamode_exports.core import probe\\nassert probe.__wrapped__ is core.probe\\nassert probe(\"1,2\")==Ok(Vector.of(1,2))\\nclass Text(str):pass\\ntry:probe(Text(\"1\"))\\nexcept TypeError as error:assert \"core:probe\" in str(error) and \"core.py:\" in str(error) and \"argument text\" in str(error)\\nelse:raise AssertionError(\"guard subtype admitted\")\\n'\n      if mode=='exports':check(all(b['original_protection']=='unguarded' for b in built['guarded_exports']),mode+' independent guard dimension')\n      else:check(bool(built['debug_coverage']),mode+' published finite internal assertion coverage')\n    else:code='import setup\\nassert setup.probe(\"12\")==12\\n'\n    ran=subprocess.run([sys.executable,'-c',code],cwd=root,env=env,capture_output=True,text=True)\n    check(ran.returncode==0,label+' stock artifact invocation '+ran.stderr)\n    rows.append(dict(label=label+' stock execution',status=ran.returncode,stdout=ran.stdout,stderr=ran.stderr,literal_source=code))\n    if layout.get('setup_observations'):check((root/'sentinel').read_text()=='executed','ordinary setup executes only on import')\nnegative=json.loads((OUT/'literal-cases.json').read_text())\nfor id in ('S01g','S09k','H01-unordered','C-negative-06','E04','N03','W01'):\n with tempfile.TemporaryDirectory(prefix='m07-cli-negative-') as d:\n  root=Path(d);case=next(c for c in negative if c['id']==id);(root/'bad.py').write_text(case['source'])\n  call(root,id+' check',['check','--root',str(root),'--json'],1)\n  call(root,id+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],1)\n  check(not (root/'artifact').exists(),id+' no failed artifact')\nwith tempfile.TemporaryDirectory(prefix='m07-explain-') as d:\n root=Path(d);(root/'core.py').write_text('from pyalamode import fun\\n@fun\\ndef probe(x:int)->int:\\n    return x+1\\n')\n for symbol in ('text_split','integer_parse_decimal','utf8_encode','vector_scan','vector_group_by','compose','partial_first','result_traverse','Vector.fold','IOCapability.read_text','ClockCapability.now_ns','EnvironmentCapability.get'):\n  call(root,'explain '+symbol,['explain',symbol],0)\n (root/'entry.py').write_text('from core import probe\\nprint(probe(3))\\n')\n ran=subprocess.run([sys.executable,'-m','pyalamode','run',str(root/'entry.py'),'--root',str(root)],cwd=root,capture_output=True,text=True)\n check(ran.returncode==2,'optional run is outside current CLI vocabulary '+ran.stderr)\n rows.append(dict(label='unsupported optional run command',status=ran.returncode,stdout=ran.stdout,stderr=ran.stderr))\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'cli-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,recorded_rows=len(rows))))\n",
  "environment_probe.py": "import json,os,subprocess,sys\nfrom pathlib import Path\nOUT=Path(__file__).parent\ncode=r'''import codecs,json,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode import live_io,live_environment,utf8_encode\nfrom pyalamode.project import check_paths,build_paths\nhits=[]\ndef changed(error):\n hits.append(type(error).__name__)\n return (b'replacement',error.end)\ncodecs.register_error('surrogateescape',changed)\nchecks=0\nwith tempfile.TemporaryDirectory(prefix='m07-ascii-target-') as d:\n root=Path(d);(root/'core.py').write_text('from pyalamode import fun\\n@fun\\ndef probe(x:int)->int:\\n    return x+1\\n')\n encoding=sys.getfilesystemencoding();errors=sys.getfilesystemencodeerrors()\n if encoding=='ascii':\n  checked=check_paths(root=root);assert checked.status==2 and not checked.verified;checks+=1\n  assert any('filesystem' in item.reason.lower() for item in checked.tooling);checks+=1\n  built=build_paths(root=root,output=root/'artifact');assert built.status==2 and not (root/'artifact').exists();checks+=1\n  for call in (lambda:live_io(d,allowed_ops=('read_text',)),live_environment):\n   try:call()\n   except RuntimeError:checks+=1\n   else:raise AssertionError('unsupported ASCII provider admitted')\n assert utf8_encode('caf\\u00e9')==b'caf\\xc3\\xa9';checks+=1\n assert hits==[];checks+=1\nprint(json.dumps({'assertions':checks,'encoding':encoding,'errors':errors,'utf8_mode':sys.flags.utf8_mode,'handler_hits':hits,'ascii_target_refused':encoding=='ascii','ascii_provider_setup_refused':encoding=='ascii'}))\n'''\nenv=dict(os.environ);env.update(LC_ALL='C',PYTHONUTF8='0',PYTHONCOERCECLOCALE='0')\nran=subprocess.run([sys.executable,'-c',code],env=env,capture_output=True,text=True)\nif ran.returncode:raise AssertionError(ran.stderr)\nrow=json.loads(ran.stdout)\nif sys.platform=='linux':assert row['encoding']=='ascii' and row['ascii_target_refused'] and row['ascii_provider_setup_refused']\nelse:assert row['encoding']=='utf-8'\nreport=dict(subprocesses=1,assertions=1+row['assertions'],row=row,command=[sys.executable,'-c',code],environment_overrides={'LC_ALL':'C','PYTHONUTF8':'0','PYTHONCOERCECLOCALE':'0'},stdout=ran.stdout,stderr=ran.stderr)\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'environment-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(assertions=report['assertions'],subprocesses=1,encoding=row['encoding'],ascii_target_refused=row['ascii_target_refused'],handler_hits=row['handler_hits'])))\n",
  "final_probe.py": "import hashlib,json,platform,re,subprocess,sys,sysconfig,time\nfrom pathlib import Path\nimport pyalamode\nOUT=Path(__file__).parent;ROOT=Path(sys.argv[1]);NAME=sys.argv[2]\ndef digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()\ndef source_map():\n    paths=[ROOT/'pyproject.toml',ROOT/'README.md']\n    for area in ('pyalamode','tests','examples','benchmarks'):paths.extend((ROOT/area).rglob('*.py'))\n    result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths)) if '__pycache__' not in p.parts}\n    for p in sorted(OUT.glob('*.py')):result['reviewer:'+p.name]=digest(p)\n    for p in (OUT/'literal-cases.json',OUT/'m06-literal-cases.json',OUT/'literal-layouts.json',OUT/'supplemental-cases.json',OUT/'narrowing-cases.json'):result['reviewer:'+p.name]=digest(p)\n    return result\ndef installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}\nbefore=source_map();installed_before=installed_map()\nassert len(installed_before)==15\nassert all(before[k]==v for k,v in installed_before.items())\nresults=[]\nfor script in ('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','freshness_probe.py','m06_runtime_probe.py','m06_project_probe.py','m06_cli_probe.py','m06_nonexecution_probe.py','m06_freshness_probe.py','environment_probe.py'):\n    target=NAME+'-'+script.removesuffix('_probe.py')+'.json'\n    started=time.perf_counter();ran=subprocess.run([sys.executable,str(OUT/script),target],cwd=OUT,capture_output=True,text=True)\n    row=dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=target);results.append(row)\n    if ran.returncode:print(json.dumps(row));raise SystemExit(ran.returncode)\nstarted=time.perf_counter();ran=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','m*.py'],cwd=OUT,capture_output=True,text=True)\nsuite=dict(status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr)\nif ran.returncode:print(json.dumps(suite));raise SystemExit(ran.returncode)\nmatch=re.search(r'Ran (\\d+) tests in ([\\d.]+)s',ran.stderr);assert match\nsuite.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)))\nafter=source_map();installed_after=installed_map();assert before==after;assert installed_before==installed_after\nreport=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),py_gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),filesystem_encoding=sys.getfilesystemencoding(),filesystem_errors=sys.getfilesystemencodeerrors(),utf8_mode=sys.flags.utf8_mode,package_path=pyalamode.__file__),results=results,suite=suite,source_before=before,source_after=after,installed_product_before=installed_before,installed_product_after=installed_after,source_unchanged=True,installed_source_equal=True)\n(OUT/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(name=NAME,suite=suite['tests'],focused=[r['stdout'].strip() for r in results],source_files=len(before),installed_product_files=len(installed_before),unchanged=True)))\n",
  "freshness_probe.py": "import json,os,shutil,subprocess,sys,tempfile\nfrom pathlib import Path\nimport pyalamode\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\nsource='from pyalamode import fun,compose,partial_first\\n@fun\\ndef plus(x:int)->int:\\n    return x+1\\n@fun\\ndef divide(a:int,b:int)->int:\\n    return a//b\\n@fun\\ndef probe(x:int)->int:\\n    return compose(plus,partial_first(divide,10))(x)\\n'\nscript='''import json\nfrom pyalamode.project import check_paths\nfrom pyalamode.model import foundation_identities\nresult=check_paths(root=PROJECT)\nprint(json.dumps({'status':result.status,'hits':[f.cache_hit for f in result.results],'identities':foundation_identities(),'contracts':[c.__dict__ for f in result.results for c in f.contracts]}))\n'''\nwith tempfile.TemporaryDirectory(prefix='m07-product-copy-') as d:\n root=Path(d);project=root/'project';project.mkdir();(project/'core.py').write_text(source)\n shutil.copytree(Path(pyalamode.__file__).parent,root/'product/pyalamode',ignore=shutil.ignore_patterns('__pycache__'))\n env=dict(os.environ);env['PYTHONPATH']=str(root/'product')+os.pathsep+env.get('PYTHONPATH','')\n def observe(label,hits):\n  ran=subprocess.run([sys.executable,'-c',script.replace('PROJECT',repr(str(project)))],cwd=root,env=env,capture_output=True,text=True)\n  check(ran.returncode==0,label+' process '+ran.stderr);value=json.loads(ran.stdout);check(value['status']==0,label+' admission');check(value['hits']==hits,label+' exact cache state');rows.append(dict(label=label,**value));return value\n old=observe('copy cold',[False]);warm=observe('copy full warm',[True]);check(old['contracts']==warm['contracts'],'exact copy warm evidence')\n check(len(old['identities'])==14,'all fourteen product foundations')\n for filename in ('standard.py','standard_contracts.py','effects.py','checker.py','model.py'):\n  p=root/'product/pyalamode'/filename;p.write_bytes(p.read_bytes()+b'\\n# independent relevant operation freshness input\\n')\n  changed=observe(filename+' byte changed',[False]);check(changed['identities'][filename]!=warm['identities'][filename],filename+' actual byte changed');warm=observe(filename+' changed warm',[True])\n (project/'pyproject.toml').write_text('[tool.pyalamode]\\nrequire_modules=[\"core.py\"]\\n')\n observe('policy changed',[False]);observe('policy changed warm',[True]);check(not (project/'artifact').exists(),'cache only no artifact')\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'freshness-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_source=source,literal_driver=script),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,subprocesses=len(rows))))\n",
  "m06_cli_probe.py": "import hashlib,json,os,subprocess,sys,tempfile\nfrom pathlib import Path\n\nOUT=Path(__file__).parent\nchecks=0;rows=[];layouts=[]\ndef check(condition,label):\n    global checks\n    checks+=1\n    if not condition:raise AssertionError(label)\ndef call(root,label,args,status,json_output=False):\n    result=subprocess.run([sys.executable,'-m','pyalamode',*args],cwd=root,capture_output=True,text=True)\n    check(result.returncode==status,label+' status '+str(result.returncode)+' '+result.stderr)\n    payload=json.loads(result.stdout) if json_output else None\n    rows.append(dict(label=label,args=args,status=result.returncode,stdout=result.stdout,stderr=result.stderr))\n    return payload\nsource='''from pyalamode import fun,variant,case,Option,Some,Nothing,Result,Ok,Err,accumulate,Vector,Failure,failure_value\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value:Vector[int]\n    @case\n    class Missing:\n        pass\n@fun\ndef probe(x:Lookup)->int:\n    match x:\n        case Lookup.Found(value=values):\n            return len(values)\n        case Lookup.Missing():\n            return 0\n@fun\ndef optional(x:Option[int])->int:\n    match x:\n        case Some(value=number):\n            return number\n        case Nothing():\n            return 0\n@fun\ndef validate(x:int,label:str)->Result[int,str]:\n    if x<0:\n        return Err(label)\n    return Ok(x)\n@fun\ndef pair(left:int,right:int)->Result[tuple[int,int],Vector[str]]:\n    return accumulate(validate(left,\"left\"),validate(right,\"right\"))\n@fun\ndef quotient(x:int)->Result[int,Failure]:\n    try:\n        return Ok(10//x)\n    except ZeroDivisionError as caught:\n        return Err(failure_value(caught))\n'''\nordinary='''import json\nimport core\nfrom pyalamode import Vector,Some,Nothing,Err,Failure\nassert core.probe(core.Lookup.Found(Vector.of(1,2)))==2\nassert core.probe(core.Lookup.Missing())==0\nassert core.optional(Some(7))==7 and core.optional(Nothing())==0\nassert core.pair(-1,-2)==Err(Vector.of(\"left\",\"right\"))\nassert core.quotient(0)==Err(Failure(\"ZeroDivisionError\",\"division by zero\"))\nassert core.probe.__dict__=={} and core.quotient.__dict__=={}\nprint(json.dumps({\"ordinary\":True,\"errors\":[\"left\",\"right\"]}))\n'''\nguarded='''import json,core\nfrom pyalamode import Vector,Some,Nothing,Ok,Err,Failure\nfrom pyalamode_exports.core import probe,optional,quotient\nassert probe.__wrapped__ is core.probe\nassert optional.__wrapped__ is core.optional\nassert probe(core.Lookup.Found(Vector.of(1,2)))==2\nassert optional(Some(7))==7 and optional(Nothing())==0\nassert quotient(0)==Err(Failure(\"ZeroDivisionError\",\"division by zero\"))\nerrors=[]\nfor function,bad in ((probe,Some(1)),(optional,Some(True))):\n    try:function(bad)\n    except TypeError as error:errors.append(str(error))\n    else:raise AssertionError(\"invalid argument admitted\")\nassert \"argument x\" in errors[0] and \"core:probe\" in errors[0]\nassert \"argument x\" in errors[1] and \"core:optional\" in errors[1]\nassert \"core.py:\" in errors[0] and \"core.py:\" in errors[1]\nprint(json.dumps({\"guarded\":True,\"authored_paths\":True}))\n'''\n\nfor mode in ('off','exports','debug'):\n    with tempfile.TemporaryDirectory(prefix='m06-cli-'+mode+'-') as d:\n        root=Path(d);(root/'core.py').write_text(source)\n        policy='[tool.pyalamode]\\nboundary_guards=\"'+mode+'\"\\n'\n        if mode!='off':policy+='guarded_exports=[\"core:probe\",\"core:optional\",\"core:quotient\"]\\n'\n        (root/'pyproject.toml').write_text(policy)\n        layouts.append(dict(id='CLI '+mode,files={'core.py':source,'pyproject.toml':policy},expected=0))\n        checked=call(root,mode+' check',['check','--root',str(root),'--json','--no-cache'],0,True)\n        check(checked['coverage']['selected_functions']==5,mode+' denominator')\n        check(checked['verified'],mode+' strict evidence')\n        built=call(root,mode+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],0,True)\n        artifact=root/'artifact'\n        if mode=='off':check((artifact/'core.py').read_text()==source,'off exact source bytes')\n        evidence=json.loads((artifact/'pyalamode-evidence.json').read_text())\n        check(evidence['boundary_guards']==mode,mode+' artifact guard evidence')\n        check(evidence['artifact_kind'].startswith('local compatible source'),'ordinary local artifact claim')\n        environment=dict(os.environ)\n        environment['PYTHONPATH']=str(artifact)+os.pathsep+environment.get('PYTHONPATH','')\n        code=ordinary if mode=='off' else guarded\n        ran=subprocess.run([sys.executable,'-c',code],cwd=root,env=environment,capture_output=True,text=True)\n        check(ran.returncode==0,mode+' stock artifact execution '+ran.stderr)\n        check(json.loads(ran.stdout).get('ordinary' if mode=='off' else 'guarded'),mode+' execution output')\n        rows.append(dict(label=mode+' ordinary artifact',status=ran.returncode,stdout=ran.stdout,stderr=ran.stderr,\n                         artifact_files=evidence['artifact_files']))\n        if mode=='exports':check(all(c['original_protection']=='unguarded' for c in evidence['guarded_exports']),'exports original remains unguarded')\n        if mode=='debug':check(bool(evidence['debug_coverage']),'debug finite coverage')\n\ncollision=source.split('@fun\\ndef optional')[0].replace('value=values','value=_pyalamode_guard_validate').replace('return len(values)','return 1')\nfor mode in ('off','debug'):\n    with tempfile.TemporaryDirectory(prefix='m06-capture-prefix-') as d:\n        root=Path(d);(root/'core.py').write_text(collision)\n        policy='[tool.pyalamode]\\nboundary_guards=\"'+mode+'\"\\n';(root/'pyproject.toml').write_text(policy)\n        layouts.append(dict(id='unused capture prefix '+mode,files={'core.py':collision,'pyproject.toml':policy},expected=0))\n        call(root,mode+' prefix build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],0,True)\n        environment=dict(os.environ);environment['PYTHONPATH']=str(root/'artifact')+os.pathsep+environment.get('PYTHONPATH','')\n        ran=subprocess.run([sys.executable,'-c','import core\\nfrom pyalamode import Vector\\nassert core.probe(core.Lookup.Found(Vector.of(1)))==1\\n'],cwd=root,env=environment,capture_output=True,text=True)\n        check(ran.returncode==0,mode+' unused capture generated name collision '+ran.stderr)\n\nnegative=json.loads((OUT/'m06-literal-cases.json').read_text())\nfor id in ('P02','P05','P42','F23','F49u','N08'):\n    case=next(c for c in negative if c['id']==id)\n    with tempfile.TemporaryDirectory(prefix='m06-negative-cli-') as d:\n        root=Path(d);(root/'bad.py').write_text(case['source'])\n        payload=call(root,id+' check',['check','--root',str(root),'--json','--no-cache'],1,True)\n        check(not payload['verified'],id+' no certificate')\n        call(root,id+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],1,True)\n        check(not (root/'artifact').exists(),id+' no artifact')\n        audited=call(root,id+' audit',['check','--root',str(root),'--audit','--json','--no-cache'],0,True)\n        check(not audited['verified'],id+' audit unverified')\n\nwith tempfile.TemporaryDirectory(prefix='m06-explain-') as d:\n    root=Path(d);(root/'core.py').write_text(source)\n    for symbol in ('variant','Option','Result','accumulate','failure_value','PAL330','PAL340'):\n        call(root,'explain '+symbol,['explain',symbol],0)\n    unsupported=call(root,'unsupported target',['check','--root',str(root),'--target','cpython-3.14.0','--json'],2,True)\n    check(not unsupported['verified'],'unsupported target no verification')\n\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'cli-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_layouts=layouts),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,commands=len(rows),layouts=len(layouts))))\n",
  "m06_freshness_probe.py": "import hashlib,json,os,shutil,subprocess,sys,tempfile\nfrom pathlib import Path\nimport pyalamode\n\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n    global checks\n    checks+=1\n    if not value:raise AssertionError(label)\nsource='from pyalamode import fun,Option,Some\\n@fun\\ndef probe(x:int)->Option[int]:\\n    return Some(x)\\n'\nscript='''import json\nfrom pyalamode.project import check_paths\nfrom pyalamode.model import foundation_identities\nresult=check_paths(root=PROJECT)\nprint(json.dumps({\"status\":result.status,\"hits\":[r.cache_hit for r in result.results],\"identities\":foundation_identities(),\"contract\":result.results[0].contracts[0].__dict__}))\n'''\nwith tempfile.TemporaryDirectory(prefix='m06-copy-freshness-') as d:\n    root=Path(d);product=root/'product';project=root/'project';project.mkdir();(project/'core.py').write_text(source)\n    shutil.copytree(Path(pyalamode.__file__).parent,product/'pyalamode',ignore=shutil.ignore_patterns('__pycache__'))\n    environment=dict(os.environ);environment['PYTHONPATH']=str(product)+os.pathsep+environment.get('PYTHONPATH','')\n    def observe(label,expected_hits):\n        ran=subprocess.run([sys.executable,'-c',script.replace('PROJECT',repr(str(project)))],cwd=root,env=environment,capture_output=True,text=True)\n        check(ran.returncode==0,label+' process '+ran.stderr)\n        result=json.loads(ran.stdout);check(result['status']==0,label+' valid gate');check(result['hits']==expected_hits,label+' cache condition')\n        rows.append(dict(label=label,**result));return result\n    original=observe('copy cold',[False]);warm=observe('copy warm',[True])\n    check(original['contract']==warm['contract'],'copy exact warm evidence')\n    for filename in ('variants.py','failures.py','model.py','checker.py'):\n        target=product/'pyalamode'/filename\n        target.write_bytes(target.read_bytes()+b'\\n# independent relevant byte freshness probe\\n')\n        changed=observe(filename+' changed bytes',[False])\n        check(changed['identities'][filename]!=warm['identities'][filename],filename+' concrete bytes differ')\n        warm=observe(filename+' changed warm',[True])\n    (project/'pyproject.toml').write_text('[tool.pyalamode]\\nrequire_modules=[\"core.py\"]\\n')\n    observe('changed policy',[False]);observe('changed policy warm',[True])\n    check(not (project/'artifact').exists(),'cache checks do not publish artifacts')\n\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'freshness-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_source=source),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,transitions=len(rows))))\n",
  "m06_nonexecution_probe.py": "import json,os,subprocess,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\n\nOUT=Path(__file__).parent;checks=0;rows=[];layouts=[]\ndef check(value,label):\n    global checks\n    checks+=1\n    if not value:raise AssertionError(label)\nbase='from pyalamode import fun,variant,case,record,Option,Some,Nothing\\nfrom pathlib import Path\\ndef mark(*args):\\n    Path(MARKER).write_text(\"evaluated\")\\n    return 3\\n'\nfixtures=(\n ('annotation','@fun\\ndef probe(x:mark())->int:\\n    return 1\\n'),\n ('default','@fun\\ndef probe(x:int=mark())->int:\\n    return x\\n'),\n ('decorator','@mark\\n@fun\\ndef probe(x:int)->int:\\n    return x\\n'),\n ('variant decorator','@mark\\n@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int\\n'),\n ('case decorator','@variant\\nclass Domain:\\n    @mark\\n    @case\\n    class Value:\\n        value:int\\n'),\n ('case annotation','@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:mark()\\n'),\n ('case default','@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int=mark()\\n'),\n ('case body','@variant\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int\\n        hidden=mark()\\n'),\n ('variant factory','@variant(mark())\\nclass Domain:\\n    @case\\n    class Value:\\n        value:int\\n'),\n ('pattern getter','class Foreign:\\n    @property\\n    def value(self):\\n        return mark()\\n@fun\\ndef probe(x:Option[int])->int:\\n    match x:\\n        case Foreign(value=number):\\n            return number\\n        case _:\\n            return 0\\n'),\n ('pattern guard','@fun\\ndef probe(x:Option[int])->int:\\n    match x:\\n        case Some() if mark():\\n            return 1\\n        case _:\\n            return 0\\n'),\n ('handler category','@fun\\ndef probe(x:int)->int:\\n    try:\\n        return 10//x\\n    except mark():\\n        return 0\\n'),\n ('handler body','@fun\\ndef probe(x:int)->int:\\n    try:\\n        return 10//x\\n    except ZeroDivisionError:\\n        return mark()\\n'),\n ('unknown class subscription','class Foreign:\\n    @classmethod\\n    def __class_getitem__(cls,arg):\\n        return mark()\\n@fun\\ndef probe(x:Foreign[int])->int:\\n    return 0\\n'),\n)\nfor label,fragment in fixtures:\n    with tempfile.TemporaryDirectory(prefix='m06-sentinel-') as d:\n        root=Path(d);marker=root/'sentinel';source=base.replace('MARKER',repr(str(marker)))+fragment\n        (root/'core.py').write_text(source);layouts.append(dict(id=label,files={'core.py':source},expected=1))\n        checked=check_paths(root=root,cache=False)\n        check(checked.status==1,label+' check refusal');check(not marker.exists(),label+' check nonexecution')\n        built=build_paths(root=root,output=root/'artifact')\n        check(built.status==1,label+' build refusal');check(not marker.exists(),label+' build nonexecution')\n        check(not (root/'artifact').exists(),label+' no artifact')\n        rows.append(dict(label=label,check_status=checked.status,build_status=built.status,sentinel_exists=marker.exists()))\n\nwith tempfile.TemporaryDirectory(prefix='m06-unchecked-init-') as d:\n    root=Path(d);marker=root/'sentinel'\n    source=base.replace('MARKER',repr(str(marker)))+'mark()\\n@fun\\ndef probe(x:int)->int:\\n    return x+1\\n'\n    (root/'core.py').write_text(source);layouts.append(dict(id='separate ordinary initialization',files={'core.py':source},expected=0))\n    checked=check_paths(root=root,cache=False)\n    check(checked.status==0,'separate invocation checks');check(not marker.exists(),'ordinary initializer not executed by check')\n    check(checked.results[0].initialization_evidence=='unchecked ordinary module initialization','separate initialization evidence')\n    built=build_paths(root=root,output=root/'artifact')\n    check(built.status==0,'ordinary initializer copied');check(not marker.exists(),'ordinary initializer not executed by build')\n    check((root/'artifact/core.py').read_text()==source,'unchanged ordinary source')\n    env=dict(os.environ);env['PYTHONPATH']=str(root/'artifact')+os.pathsep+env.get('PYTHONPATH','')\n    ran=subprocess.run([sys.executable,'-c','import core\\nassert core.probe(1)==2\\n'],cwd=root,env=env,capture_output=True,text=True)\n    check(ran.returncode==0,'stock ordinary initializer runs '+ran.stderr)\n    check(marker.read_text()=='evaluated','initialization occurs only on ordinary import')\n    rows.append(dict(label='separate ordinary initialization',check_status=checked.status,build_status=built.status,ordinary_status=ran.returncode))\n\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'nonexecution-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_layouts=layouts),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,sentinels=len(fixtures),layouts=len(layouts))))\n",
  "m06_project_probe.py": "import hashlib,json,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\n\nOUT=Path(__file__).parent\nchecks=0;rows=[];layouts=[]\ndef check(condition,label):\n    global checks\n    checks+=1\n    if not condition:raise AssertionError(label)\ndef write(root,files):\n    for name,source in files.items():\n        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source)\ndef contract(result,name):\n    return next(c for f in result.results for c in f.contracts if c.name==name)\ndef gate(root,label,expected,cache=True):\n    result=check_paths(root=root,cache=cache)\n    check(result.status==expected,label+' status '+str(result.status))\n    rows.append(dict(label=label,status=result.status,cache_hits={Path(f.path).name:f.cache_hit for f in result.results},\n                     diagnostics=[d.__dict__ for d in [*result.tooling,*[d for f in result.results for d in f.diagnostics]]],\n                     contracts={c.name:c.__dict__ for f in result.results for c in f.contracts}))\n    return result\n\ndomain='# mode: fun\\nfrom pyalamode import variant,case\\n@variant\\nclass Lookup:\\n    @case\\n    class Found:\\n        value:int\\n    @case\\n    class Missing:\\n        pass\\n'\nexplicit='# mode: fun\\nfrom domain import Lookup\\ndef probe(x:Lookup)->int:\\n    match x:\\n        case Lookup.Found(value=number):\\n            return number\\n        case Lookup.Missing():\\n            return 0\\n'\nwildcard='# mode: fun\\nfrom domain import Lookup\\ndef probe(x:Lookup)->int:\\n    match x:\\n        case Lookup.Found(value=number):\\n            return number\\n        case _:\\n            return 0\\n'\nadded=domain+'    @case\\n    class Pending:\\n        code:str\\n'\nfor label,consumer,after in (('explicit',explicit,1),('wildcard',wildcard,0)):\n    with tempfile.TemporaryDirectory(prefix='m06-'+label+'-') as d:\n        root=Path(d);files={'domain.py':domain,'consumer.py':consumer};write(root,files)\n        layouts.append(dict(id='case-add-'+label,files=files,transition={'domain.py':added},expected=[0,0,after]))\n        first=gate(root,label+' cold',0);warm=gate(root,label+' warm',0)\n        check(all(f.cache_hit for f in warm.results),label+' fully warm')\n        before=contract(first,'probe')\n        write(root,{'domain.py':added});changed=gate(root,label+' case addition',after)\n        check(not next(f for f in changed.results if Path(f.path).name=='consumer.py').cache_hit,label+' consumer invalidated')\n        if not after:\n            check(before.patterns[0]['wildcard'] and contract(changed,'probe').patterns[0]['wildcard'],'deliberate wildcard evidence')\n            check(before.patterns[0]['case_fingerprint']!=contract(changed,'probe').patterns[0]['case_fingerprint'],'case fingerprint changed')\n        failed=build_paths(root=root,output=root/'artifact')\n        check(failed.status==after,label+' subsequent build gate')\n        check((root/'artifact').exists()==(not after),label+' artifact publication')\n\npolicies=(\n ('explicit wildcard','explicit_cases=[\"domain:Lookup\"]',wildcard,1),\n ('explicit complete','explicit_cases=[\"domain:Lookup\"]',explicit,0),\n ('unknown selector','explicit_cases=[\"domain:Unknown\"]',explicit,2),\n ('wrong type','explicit_cases=3',explicit,2),\n ('unknown module','explicit_cases=[\"unknown:Lookup\"]',explicit,2),\n ('malformed selector','explicit_cases=[\"domain.Lookup\"]',explicit,2),\n ('duplicate selector','explicit_cases=[\"domain:Lookup\",\"domain:Lookup\"]',explicit,2),\n)\nfor label,policy,consumer,status in policies:\n    with tempfile.TemporaryDirectory(prefix='m06-policy-') as d:\n        root=Path(d);files={'domain.py':domain,'consumer.py':consumer,'pyproject.toml':'[tool.pyalamode]\\n'+policy+'\\n'}\n        layouts.append(dict(id=label,files=files,expected=status));write(root,files)\n        gate(root,label,status);built=build_paths(root=root,output=root/'artifact')\n        check(built.status==status,label+' build status')\n        check((root/'artifact').exists()==(not status),label+' build output')\n\nleaf='# mode: fun\\ndef divide(x:int)->int:\\n    return 10//x\\n'\nfactory='# mode: fun\\nfrom typing import Callable\\nfrom leaf import divide\\ndef maker()->Callable[[int],int]:\\n    def handled(x:int)->int:\\n        try:\\n            return divide(x)\\n        except ZeroDivisionError:\\n            return 0\\n    return handled\\n'\nconsumer='# mode: fun\\nfrom factory import maker\\ndef invoke(x:int)->int:\\n    return maker()(x)\\n'\nwith tempfile.TemporaryDirectory(prefix='m06-handler-warm-') as d:\n    root=Path(d);files={'leaf.py':leaf,'factory.py':factory,'consumer.py':consumer};write(root,files)\n    layouts.append(dict(id='returned handler partial warm',files=files,transition={'consumer.py':consumer+'\\n# independent consumer edit\\n'},expected=[0,0,0]))\n    cold=gate(root,'returned handler cold',0);warm=gate(root,'returned handler warm',0)\n    check(all(f.cache_hit for f in warm.results),'handler full body reuse')\n    for result in (cold,warm):\n        check(contract(result,'invoke').failures==[],'handled returned target does not leak division failure')\n        check(contract(result,'maker').required_effects==[],'reference factory has no invocation effects')\n        check(bool(contract(result,'maker').return_callable_targets),'known returned handler target retained')\n        check(bool(contract(result,'maker.handled').failure_edges),'handler call edge serialized')\n    write(root,{'consumer.py':consumer+'\\n# independent consumer edit\\n'})\n    partial=gate(root,'returned handler partial warm',0)\n    hits={Path(f.path).name:f.cache_hit for f in partial.results}\n    check(hits['factory.py'] and hits['leaf.py'] and not hits['consumer.py'],'actual partial factory body reuse')\n    for name in ('maker','maker.handled','invoke'):\n        check(contract(cold,name).__dict__==contract(partial,name).__dict__,'partial exact evidence '+name)\n\nclockleaf='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\n@effects(Clock)\\ndef timed(cap:ClockCapability,x:int)->int:\\n    try:\\n        return cap.now_ns()//x\\n    except ZeroDivisionError:\\n        return 0\\n'\nclockfactory='# mode: fun\\nfrom pyalamode import Effectful,Clock,State,ClockCapability\\nfrom leaf import timed\\ndef maker()->Effectful[[ClockCapability,int],int,Clock,State]:\\n    return timed\\n'\nclockconsumer='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\nfrom factory import maker\\n@effects(Clock)\\ndef invoke(cap:ClockCapability,x:int)->int:\\n    return maker()(cap,x)\\n'\nwith tempfile.TemporaryDirectory(prefix='m06-clock-warm-') as d:\n    root=Path(d);files={'leaf.py':clockleaf,'factory.py':clockfactory,'consumer.py':clockconsumer};write(root,files)\n    layouts.append(dict(id='tighter concrete handled clock partial warm',files=files,transition={'consumer.py':clockconsumer+'\\n# independent edit\\n'},expected=[0,0,0]))\n    cold=gate(root,'tighter handled clock cold',0);warm=gate(root,'tighter handled clock warm',0)\n    for result in (cold,warm):\n        c=contract(result,'invoke')\n        check(c.required_effects==['Clock'],'actual tighter target effect')\n        check(c.failures==['IndexError','OSError','RuntimeError'],'masked target failures independent from effects')\n        check(contract(result,'maker').required_effects==[],'retained clock target not invoked by maker')\n        check(contract(result,'maker').trust==c.trust,'retained complete target trust')\n    write(root,{'consumer.py':clockconsumer+'\\n# independent edit\\n'})\n    partial=gate(root,'tighter handled clock partial warm',0)\n    hits={Path(f.path).name:f.cache_hit for f in partial.results}\n    check(hits['factory.py'] and hits['leaf.py'] and not hits['consumer.py'],'actual clock partial reuse')\n    for name in ('timed','maker','invoke'):\n        check(contract(cold,name).__dict__==contract(partial,name).__dict__,'clock partial exact evidence '+name)\n\ncapturing_factory='# mode: fun\\nfrom pyalamode import effects,Effectful,Clock,ClockCapability\\ndef maker(op:Effectful[[ClockCapability,int],int,Clock])->Effectful[[ClockCapability,int],int,Clock]:\\n    @effects(Clock)\\n    def handled(cap:ClockCapability,x:int)->int:\\n        try:\\n            return op(cap,x)\\n        except RuntimeError:\\n            return 0\\n    return handled\\n'\ncapturing_consumer='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\nfrom factory import maker\\nfrom leaf import timed\\n@effects(Clock)\\ndef invoke(cap:ClockCapability,x:int)->int:\\n    return maker(timed)(cap,x)\\n'\nvariant_leaf='# mode: fun\\nfrom pyalamode import Option,Some\\ndef present(x:int)->Option[int]:\\n    return Some(x)\\n'\nvariant_factory='# mode: fun\\nfrom pyalamode import Option\\nfrom typing import Callable\\nfrom leaf import present\\ndef maker()->Callable[[int],Option[int]]:\\n    return present\\n'\nvariant_consumer='# mode: fun\\nfrom pyalamode import Vector,Option\\nfrom factory import maker\\ndef invoke(values:Vector[int])->Vector[Option[int]]:\\n    return values.map(maker())\\n'\nfor label,files,expected_failures,expected_effects in (\n ('conditional captured handler',{'leaf.py':clockleaf,'factory.py':capturing_factory,'consumer.py':capturing_consumer},['IndexError','KeyError','OSError','UnicodeError','ValueError','ZeroDivisionError'],['Clock']),\n ('retained variant callable',{'leaf.py':variant_leaf,'factory.py':variant_factory,'consumer.py':variant_consumer},['RecursionError'],[]),\n):\n    with tempfile.TemporaryDirectory(prefix='m06-partial-') as d:\n        root=Path(d);write(root,files)\n        edited=files['consumer.py']+'\\n# independent body reuse probe\\n'\n        layouts.append(dict(id=label,files=files,transition={'consumer.py':edited},expected=[0,0,0]))\n        cold=gate(root,label+' cold',0);warm=gate(root,label+' warm',0)\n        check(all(f.cache_hit for f in warm.results),label+' full reuse')\n        for result in (cold,warm):\n            check(contract(result,'invoke').failures==expected_failures,label+' callback failure upper bound')\n            check(contract(result,'invoke').required_effects==expected_effects,label+' invocation bound')\n            check(contract(result,'maker').required_effects==[],label+' uninvoked factory bound')\n            check(set(contract(result,'maker').trust)<=set(contract(result,'invoke').trust),label+' complete retained trust')\n            if label=='conditional captured handler':\n                evidence=contract(result,'maker.handled').callable_capture_evidence['op']\n                check(evidence['conditional'] and evidence['effect_bound']==['Clock'],label+' conditional capture evidence')\n            else:\n                check(any('domains-v1' in trust for trust in contract(result,'maker').trust),label+' retained variant foundation')\n        write(root,{'consumer.py':edited});partial=gate(root,label+' partial warm',0)\n        hits={Path(f.path).name:f.cache_hit for f in partial.results}\n        check(hits['leaf.py'] and hits['factory.py'] and not hits['consumer.py'],label+' actual partial reuse')\n        for name in ('maker','invoke'):\n            check(contract(cold,name).__dict__==contract(partial,name).__dict__,label+' exact serialized evidence '+name)\n\nwriters=(\n ('case class method','from domain import Lookup\\nLookup.Found.__init__.__code__=unknown\\n'),\n ('case imported assigned alias','from domain import Lookup\\nAlias=Lookup.Found\\nAlias.__match_args__=()\\n'),\n ('case setter alias','from domain import Lookup\\nfrom builtins import setattr as write\\nwrite(Lookup.Found,\"__match_args__\",())\\n'),\n ('private variant helper','from pyalamode.variants import _case_info as helper\\nhelper.__code__=unknown\\n'),\n ('private variant metaclass method','from pyalamode.variants import _DomainType\\n_DomainType.__setattr__.__code__=unknown\\n'),\n ('private failure helper','from pyalamode.failures import failure_value as helper\\nhelper.__code__=unknown\\n'),\n ('failure record method','from pyalamode import Failure\\nFailure.__init__.__code__=unknown\\n'),\n ('failure builtin native identity','import builtins\\nbuiltins.ZeroDivisionError=Exception\\n'),\n ('variant GenericAlias identity','import types\\ntypes.GenericAlias=unknown\\n'),\n ('variant descriptor foundation','import types\\ntypes.GetSetDescriptorType=unknown\\n'),\n ('Option contained Some writer','from pyalamode import Some\\nSome.__setattr__=unknown\\n'),\n ('Option contained Nothing alias','from pyalamode.variants import Nothing as Alias\\nAlias.__eq__.__code__=unknown\\n'),\n ('Option nested Vector writer','from pyalamode import Some\\nSome.__setattr__=unknown\\n'),\n ('Result contained Ok writer','from pyalamode import Ok\\nOk.__setattr__=unknown\\n'),\n ('Result nested tuple Err writer','from pyalamode.variants import Err as Alias\\nAlias.__init__.__code__=unknown\\n'),\n)\nfor label,writer in writers:\n    with tempfile.TemporaryDirectory(prefix='m06-writer-') as d:\n        selected_consumer=('# mode: fun\\nfrom pyalamode import Result,Ok,Err,Failure,failure_value\\ndef probe(x:int)->Result[int,Failure]:\\n    try:\\n        return Ok(10//x)\\n    except ZeroDivisionError as caught:\\n        return Err(failure_value(caught))\\n') if 'failure' in label else explicit\n        if label.startswith(('Option','Result')):\n            schema='Vector[Option[int]]' if 'Vector' in label else 'tuple[Result[int,str]]' if 'tuple' in label else 'Option[int]' if label.startswith('Option') else 'Result[int,str]'\n            selected_consumer='# mode: fun\\nfrom pyalamode import Vector,Option,Result\\ndef probe(x:'+schema+')->'+schema+':\\n    return x\\n'\n        root=Path(d);files={'domain.py':domain,'consumer.py':selected_consumer,'writer.py':'pass\\n'};write(root,files)\n        layouts.append(dict(id=label,files=files,transition={'writer.py':writer},expected=[0,0,1]))\n        gate(root,label+' cold',0);warm=gate(root,label+' warm',0)\n        check(all(f.cache_hit for f in warm.results),label+' warm original')\n        write(root,{'writer.py':writer});changed=gate(root,label+' changed writer',1)\n        affected=next(f for f in changed.results if Path(f.path).name=='consumer.py')\n        check(not affected.cache_hit or (not affected.verified and all('unverified' in c.source_evidence for c in affected.contracts)),label+' consumer evidence invalidated')\n        fresh=gate(root,label+' fresh writer',1,cache=False)\n        built=build_paths(root=root,output=root/'artifact')\n        check(built.status==1 and not (root/'artifact').exists(),label+' no artifact')\n\nresult=dict(assertions=checks,rows=rows,literal_layouts=layouts)\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'project-observations.json')).write_text(json.dumps(result,indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,layouts=len(layouts),checks=len(rows))))\n",
  "m06_runtime_probe.py": "import json,sys\nfrom pathlib import Path\nfrom pyalamode import (variant,case,record,Vector,Map,OrderedMap,Set,Option,Some,Nothing,\n                      Result,Ok,Err,accumulate,Failure,failure_value,freeze,thaw,state)\nfrom pyalamode.boundaries import validate_data\nfrom pyalamode.records import _annotation_schema\n\nchecks=0\ndef check(value,label):\n    global checks\n    checks+=1\n    if not value:\n        raise AssertionError(label)\ndef raises(kind,operation,label):\n    global checks\n    checks+=1\n    try:\n        operation()\n    except kind:\n        return\n    raise AssertionError(label)\n\n@record\nclass Payload:\n    number:int\n    labels:Vector[str]\n\n@variant\nclass Lookup:\n    @case\n    class Found:\n        item:Payload\n    @case\n    class Missing:\n        pass\n\n@variant\nclass Pair:\n    @case\n    class Data:\n        left:Option[int]\n        right:Result[Vector[int],str]\n\nfirst=Lookup.Found(Payload(7,Vector.of('a','b')))\nsame=Lookup.Found(Payload(7,Vector.of('a','b')))\ndifferent=Lookup.Found(Payload(8,Vector.of('a','b')))\ncheck(first==same,'nested case equivalence')\ncheck(first!=different,'nested case payload difference')\ncheck(first!=Lookup.Missing(),'tag distinction')\ncheck(Some(True)!=Some(1),'bool int Option distinction')\ncheck(Ok(True)!=Ok(1),'bool int Result distinction')\ncheck(Some(1)!=Ok(1),'domain distinction')\ncheck(Nothing()==Nothing(),'absence equivalence')\ncheck(Lookup.Missing()==Lookup.Missing(),'zero case equivalence')\ncheck(Vector.of(first)==Vector.of(same),'collection nested variants')\ncheck(OrderedMap.of(('x',first))==OrderedMap.of(('x',same)),'ordered map nested variants')\ncheck(Map.of(('x',first))==Map.of(('x',same)),'map nested variants')\ncheck(Pair.Data(Some(1),Ok(Vector.of(2)))==Pair.Data(Some(1),Ok(Vector.of(2))),'generic fields')\ncheck(repr(first)==repr(same),'stable equivalent repr')\ncheck(repr(first).index('number=7')<repr(first).index('labels='),'declaration order in repr')\nraises(AttributeError,lambda:setattr(first,'item',Payload(9,Vector.of())),'case assignment')\nraises(AttributeError,lambda:delattr(first,'item'),'case deletion')\nraises(AttributeError,lambda:first.__init__(Payload(9,Vector.of())),'case reinitialization')\nraises(TypeError,lambda:hash(first),'case unhashable')\nraises(TypeError,lambda:Lookup(),'domain not constructible')\nraises(TypeError,lambda:type('Derived',(Lookup.Found,),{}),'case subclass')\nraises(TypeError,lambda:type('DerivedDomain',(Lookup,),{}),'domain subclass')\nraises(TypeError,lambda:Lookup.Found(),'required payload')\nraises(TypeError,lambda:Lookup.Found(first.item,item=first.item),'duplicate payload')\nraises(TypeError,lambda:Lookup.Found(unknown=first.item),'unknown payload')\nraises(TypeError,lambda:Lookup.Missing(1),'no payload excess')\nraises(TypeError,lambda:Lookup.Found([1]),'mutable case payload')\nraises(TypeError,lambda:Some([1]),'mutable option payload')\nraises(TypeError,lambda:Ok({'x':1}),'mutable success payload')\nraises(TypeError,lambda:Err(([],)),'nested mutable error payload')\nraises(TypeError,lambda:Some(lambda:1),'callable payload')\nraises(TypeError,lambda:Some(state(1)),'capability payload')\nraises(TypeError,lambda:Ok(ValueError('raw')),'raw exception payload')\nclass Integer(int):\n    pass\nraises(TypeError,lambda:Some(Integer(1)),'scalar subclass payload')\nraises(TypeError,lambda:Vector.of([first]),'mutable collection wrapping case')\nraises(TypeError,lambda:Set.of(first),'variant key excluded')\nraises(TypeError,lambda:Map.of((first,1)),'variant map key excluded')\n\nhooks=[]\nclass ForeignMeta(type):\n    def __hash__(self):\n        hooks.append('metahash');return 0\n    def __eq__(self,other):\n        hooks.append('metaeq');return False\n    def __getattribute__(self,name):\n        hooks.append('metaget');return super().__getattribute__(name)\nclass Foreign(metaclass=ForeignMeta):\n    def __getattribute__(self,name):\n        hooks.append('get');return object.__getattribute__(self,name)\n    def __iter__(self):\n        hooks.append('iter');return iter(())\n    def __hash__(self):\n        hooks.append('hash');return 0\n    def __eq__(self,other):\n        hooks.append('eq');return False\n    def __repr__(self):\n        hooks.append('repr');return 'foreign'\n    def __str__(self):\n        hooks.append('str');return 'foreign'\nforeign=Foreign();hooks.clear()\nfor label,operation in (\n ('Some',lambda:Some(foreign)),('Ok',lambda:Ok(foreign)),('Err',lambda:Err(foreign)),\n ('case',lambda:Lookup.Found(foreign)),('Vector',lambda:Vector.of(foreign)),\n ('freeze',lambda:freeze(foreign,exclusive=True)),('thaw',lambda:thaw(foreign)),\n ('failure',lambda:failure_value(foreign)),\n):\n    raises(TypeError,operation,'hook-zero '+label)\n    check(hooks==[],'zero hooks '+label)\ncheck(first!=foreign,'product foreign inequality')\ncheck(hooks==[],'zero equality hooks')\n\nfor value,annotation in ((first,Lookup),(first,Lookup.Found),(Some(1),Option[int]),\n                         (Nothing(),Option[int]),(Ok(1),Result[int,str]),\n                         (Err('bad'),Result[int,str]),(Some(1),Some[int]),\n                         (Ok(1),Ok[int]),(Err('bad'),Err[str])):\n    schema=_annotation_schema(annotation)\n    check(validate_data(value,schema) is value,'schema validate '+str(annotation))\nraises(TypeError,lambda:validate_data(Some(True),_annotation_schema(Option[int])),'exact generic Option schema')\nraises(TypeError,lambda:validate_data(Err(1),_annotation_schema(Result[int,str])),'exact generic error schema')\nraises(TypeError,lambda:validate_data(Ok(True),_annotation_schema(Result[int,str])),'exact generic success schema')\nraises(TypeError,lambda:validate_data(first,_annotation_schema(Option[int])),'wrong domain schema')\nraises(TypeError,lambda:validate_data(Some(foreign),_annotation_schema(Option[int])),'foreign schema hook zero')\ncheck(hooks==[],'schema hooks remain zero')\n\nfor left,right,result in ((Ok(1),Ok('r'),Ok((1,'r'))),(Err('l'),Ok(2),Err(Vector.of('l'))),\n                          (Ok(1),Err('r'),Err(Vector.of('r'))),(Err('l'),Err('r'),Err(Vector.of('l','r')))):\n    check(accumulate(left,right)==result,'ordered binary validation')\norder=[]\ndef supplied(label,value):\n    order.append(label);return value\ncombined=accumulate(supplied('left',Err('one')),supplied('right',Err('two')))\ncheck(order==['left','right'],'argument order')\ncheck(combined==Err(Vector.of('one','two')),'two independent errors')\nraises(TypeError,lambda:accumulate(Some(1),Ok(2)),'unknown accumulation input')\nraises(TypeError,lambda:accumulate(foreign,Ok(2)),'foreign accumulation input')\ncheck(hooks==[],'accumulation hook zero')\n\ncheck(freeze(first) is first,'admitted case snapshot reuse')\nsnapshot=freeze([first,first],exclusive=True,schema=Vector[Lookup])\ncheck(snapshot==Vector.of(first,first),'mutable outer independent snapshot')\nexport=thaw(first);other=thaw(first)\ncheck(export=={'variant':'__main__:Lookup','case':'Found','fields':{'item':{'number':7,'labels':['a','b']}}},'domain export envelope')\nexport['fields']['item']['labels'].append('changed')\ncheck(other['fields']['item']['labels']==['a','b'],'fresh repeated export')\ncheck(first.item.labels==Vector.of('a','b'),'export cannot change variant')\ncopies=thaw(snapshot)\ncopies[0]['fields']['item']['labels'].append('only first')\ncheck(copies[1]['fields']['item']['labels']==['a','b'],'fresh repeated occurrence')\ncheck(thaw(Some(Vector.of(1)))=={'variant':'pyalamode:Option','case':'Some','fields':{'value':[1]}},'builtin Option export')\ncheck(thaw(Nothing())=={'variant':'pyalamode:Option','case':'Nothing','fields':{}},'builtin absence export')\ncheck(thaw(Err(Vector.of('a','b')))=={'variant':'pyalamode:Result','case':'Err','fields':{'error':['a','b']}},'builtin Result export')\n\nfixed={ZeroDivisionError:'division by zero',IndexError:'index out of range',KeyError:'key not found',\n       ValueError:'invalid value',RecursionError:'recursion limit reached',RuntimeError:'runtime operation failed',\n       OSError:'operating system operation failed',UnicodeError:'unicode operation failed'}\nfor kind,message in fixed.items():\n    exception=kind(foreign)\n    exception.extra=foreign\n    converted=failure_value(exception)\n    check(type(converted) is Failure,'exact Failure')\n    check(converted.category==kind.__name__,'exact native category')\n    check(converted.message==message,'fixed native message')\n    check(failure_value(exception)==converted,'repeat equivalent failure')\n    check(failure_value(exception) is not converted,'fresh failure value')\n    check(thaw(converted)=={'category':kind.__name__,'message':message},'Failure fresh record export')\n    check(hooks==[],'no exception args formatting')\nfor kind in (BlockingIOError,ChildProcessError,ConnectionError,BrokenPipeError,ConnectionAbortedError,\n             ConnectionRefusedError,ConnectionResetError,FileExistsError,FileNotFoundError,InterruptedError,\n             IsADirectoryError,NotADirectoryError,PermissionError,ProcessLookupError,TimeoutError):\n    converted=failure_value(kind())\n    check(converted.category=='OSError','finite OS exact subtype')\n    check(converted.message==fixed[OSError],'finite OS fixed message')\nfor exception in (UnicodeDecodeError('utf-8',b'\\xff',0,1,'unknown'),\n                  UnicodeEncodeError('utf-8','x',0,1,'unknown'),UnicodeTranslateError('x',0,1,'unknown')):\n    converted=failure_value(exception)\n    check(converted.category=='UnicodeError','finite Unicode exact subtype')\n    check(converted.message==fixed[UnicodeError],'finite Unicode fixed message')\nclass CustomFailure(ValueError):\n    def __str__(self):hooks.append('exceptionstr');return 'bad'\n    def __repr__(self):hooks.append('exceptionrepr');return 'bad'\n    def __getattribute__(self,name):hooks.append('exceptionget');return object.__getattribute__(self,name)\nfor exception in (CustomFailure(),Exception(),BaseException(),TypeError(),StopIteration()):\n    raises(TypeError,lambda:failure_value(exception),'unsupported exception universe')\n    check(hooks==[],'unsupported exception no hooks')\nfailure=Failure('arbitrary','data')\nraises(AttributeError,lambda:setattr(failure,'category','changed'),'immutable failure fields')\nraises(TypeError,lambda:Failure(True,'bad'),'exact failure strings')\ncheck(hooks==[],'final hook zero')\n\ntarget=Path(__file__).parent/(sys.argv[1] if len(sys.argv)>1 else 'runtime-observations.json')\ntarget.write_text(json.dumps(dict(assertions=checks,hook_calls=hooks),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,hook_calls=hooks)))\n",
  "make_cases.py": "import ast,hashlib,json\nfrom pathlib import Path\nOUT=Path(__file__).parent;cases=[]\nbase='from pyalamode import fun,Vector,OrderedMap,Map,Set,Result,Ok,Err,Option,Some,Nothing,Failure,failure_value,effects,Effectful,IO,Clock,Environment,IOCapability,ClockCapability,EnvironmentCapability,borrow\\nfrom typing import Callable\\n'\nops=(\n ('text_split','text:str,separator:str','Vector[str]','text,separator','\"a,b\",\",\"','str','[\"ValueError\"]'),\n ('text_join','parts:Vector[str],separator:str','str','parts,separator','Vector.of(\"a\",\"b\"),\",\"','Vector[str]','[\"RecursionError\"]'),\n ('text_replace','text:str,old:str,new:str','str','text,old,new','\"aaa\",\"aa\",\"b\"','str','[]'),\n ('text_startswith','text:str,prefix:str','bool','text,prefix','\"ab\",\"a\"','str','[]'),\n ('text_slice','text:str,start:int,stop:int','str','text,start,stop','\"abc\",0,2','str','[]'),\n ('integer_clamp','value:int,lower:int,upper:int','int','value,lower,upper','2,0,3','int','[\"ValueError\"]'),\n ('integer_parse_decimal','text:str','int','text','\"123\"','str','[\"ValueError\"]'),\n ('integer_format_decimal','value:int','str','value','123','int','[\"ValueError\"]'),\n ('utf8_encode','text:str','bytes','text','\"Ada\"','str','[\"UnicodeError\"]'),\n ('utf8_decode','data:bytes','str','data','b\"Ada\"','bytes','[\"UnicodeError\"]'),\n ('hex_encode','data:bytes','str','data','b\"Ada\"','bytes','[]'),\n ('hex_decode','text:str','bytes','text','\"416461\"','str','[\"ValueError\"]'),\n)\ndef add(id,source,status=0,**fields):cases.append(dict(id=id,source=source,expected=status,**fields))\nfor i,(name,params,result,args,literals,first,failures) in enumerate(ops,1):\n imp=base+'from pyalamode import '+name+'\\n'\n source=imp+'@fun\\ndef probe('+params+')->'+result+':\\n    return '+name+'('+args+')\\n'\n common=dict(failures=json.loads(failures),required_effects=[],effect_bound=[])\n add(f'S{i:02}a',source,**common)\n add(f'S{i:02}b',source.replace('import '+name,'import '+name+' as operation').replace('return '+name+'(','return operation('),**common)\n add(f'S{i:02}c',source.replace('from pyalamode import '+name,'from pyalamode.standard import '+name),**common)\n add(f'S{i:02}d',source.replace('from pyalamode import '+name,'import pyalamode.standard as standard').replace('return '+name+'(','return standard.'+name+'('),**common)\n add(f'S{i:02}e',imp+'@fun\\ndef probe(value:'+result+'='+name+'('+literals+'))->'+result+':\\n    return value\\n',failures=[],required_effects=[])\n add(f'S{i:02}f','# mode: fun\\n'+imp+'value='+name+'('+literals+')\\ndef probe()->'+result+':\\n    return value\\n',failures=[],required_effects=[])\n add(f'S{i:02}g',source.replace(name+'('+args+')',name+'()'),1)\n add(f'S{i:02}h',source.replace(name+'('+args+')',name+'('+args+',0)'),1)\n keyword=params.split(':')[0]\n add(f'S{i:02}i',source.replace(name+'('+args+')',name+'('+keyword+'='+args.split(',')[0]+')'),1)\n add(f'S{i:02}j',source.replace(name+'('+args+')',name+'(*('+literals+',))'),1)\n wrong='True' if first=='int' else '1' if first in {'str','bytes'} else '()'\n firstarg=args.split(',')[0];wrongargs=','.join([wrong,*args.split(',')[1:]])\n add(f'S{i:02}k',source.replace(name+'('+args+')',name+'('+wrongargs+')'),1)\n add(f'S{i:02}l',imp+name+'=unknown\\n@fun\\ndef probe('+params+')->'+result+':\\n    return '+name+'('+args+')\\n',1)\n add(f'S{i:02}m',imp+'Alias='+name+'\\nAlias.__code__=unknown\\n@fun\\ndef probe('+params+')->'+result+':\\n    return '+name+'('+args+')\\n',1)\n if first in {'str','bytes','int'}:\n  actual=repr('Ada') if first=='str' else repr(b'Ada') if first=='bytes' else '123'\n  literal_args=[ast.unparse(arg) for arg in ast.parse('_('+literals+')').body[0].value.args]\n  add(f'S{i:02}n',source+'class Derived('+first+'):\\n    pass\\nprobe('+','.join(['Derived('+actual+')',*literal_args[1:]])+')\\n',1)\n\nhigher=base+'from pyalamode import vector_scan,vector_group_by,compose,partial_first,result_traverse,utf8_encode,utf8_decode,text_split,integer_parse_decimal\\n'\nadd('H01',higher+'@fun\\ndef add(a:int,b:int)->int:\\n    return a+b\\n@fun\\ndef probe(values:Vector[int])->Vector[int]:\\n    return vector_scan(values,add,0)\\n',required_effects=[])\nadd('H02',higher+'@fun\\ndef parity(x:int)->int:\\n    return x%2\\n@fun\\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\\n    return vector_group_by(values,parity)\\n',required_effects=[])\nadd('H03',higher+'@fun\\ndef good(x:int)->Result[int,str]:\\n    if x<0:\\n        return Err(\"negative\")\\n    return Ok(x+1)\\n@fun\\ndef probe(values:Vector[int])->Result[Vector[int],str]:\\n    return result_traverse(values,good)\\n',required_effects=[])\nadd('H04',higher+'@fun\\ndef add(a:int,b:int)->int:\\n    return a+b\\n@fun\\ndef probe(values:Vector[int])->int:\\n    return values.fold(add,0)\\n',failures=[],required_effects=[])\nfor id,source in list((c['id'],c['source']) for c in cases if c['id'] in {'H01','H02','H03'}):\n add(id+'-unordered',source.replace('values:Vector[int]','values:Set[int]'),1)\n add(id+'-iterable',source.replace('values:Vector[int]','values:tuple[int,...]'),1)\n add(id+'-unknown',source.replace(',add,',',unknown,').replace(',parity)',',unknown)').replace(',good)',',unknown)'),1)\n add(id+'-lambda',source.replace(',add,',',lambda a,b:a+b,').replace(',parity)',',lambda x:x)').replace(',good)',',lambda x:Ok(x))'),1)\n add(id+'-mutable',source.replace('vector_scan(values,add,0)','vector_scan(values,add,[])').replace('return x%2','return [x]').replace('return Ok(x+1)','return Ok([x])'),1)\n add(id+'-arity',source.replace('vector_scan(values,add,0)','vector_scan(values,add)').replace('vector_group_by(values,parity)','vector_group_by(values,parity,0)').replace('result_traverse(values,good)','result_traverse(values)'),1)\n add(id+'-keyword',source.replace('vector_scan(values,add,0)','vector_scan(values,add,initial=0)').replace('vector_group_by(values,parity)','vector_group_by(values,callback=parity)').replace('result_traverse(values,good)','result_traverse(values,callback=good)'),1)\n add(id+'-init','# mode: fun\\n'+source+'value=probe(Vector.of(1))\\n',1)\nfor keykind,key in (('str','\"x\"'),('bool','x<0'),('bytes','b\"x\"'),('None','None')):\n add('H05-'+keykind,higher+'@fun\\ndef key(x:int)->'+keykind+':\\n    return '+key+'\\n@fun\\ndef probe(values:Vector[int])->OrderedMap['+keykind+',Vector[int]]:\\n    return vector_group_by(values,key)\\n',required_effects=[])\nadd('H06',higher+'@fun\\ndef key(x:int)->Vector[int]:\\n    return Vector.of(x)\\n@fun\\ndef probe(values:Vector[int])->OrderedMap[int,Vector[int]]:\\n    return vector_group_by(values,key)\\n',1)\nadd('H07',higher+'@fun\\ndef step(a:int,b:int)->str:\\n    return \"x\"\\n@fun\\ndef probe(values:Vector[int])->Vector[int]:\\n    return vector_scan(values,step,0)\\n',1)\nadd('H08',higher+'@fun\\ndef bad(x:int)->Option[int]:\\n    return Some(x)\\n@fun\\ndef probe(values:Vector[int])->Result[Vector[int],str]:\\n    return result_traverse(values,bad)\\n',1)\nadd('H09',higher+'@fun\\ndef probe(values:Vector[int],op:Callable[[int,int],int])->Vector[int]:\\n    try:\\n        return vector_scan(values,op,0)\\n    except ValueError:\\n        return Vector.of(0)\\n',required_effects=[],failures=['IndexError','KeyError','RecursionError','ZeroDivisionError'])\nadd('H10',higher+'@fun\\ndef probe(values:Vector[str],op:Callable[[str],Result[int,str]])->Result[Vector[int],str]:\\n    try:\\n        return result_traverse(values,op)\\n    except UnicodeError:\\n        return Err(\"unicode\")\\n',required_effects=[],failures=['IndexError','KeyError','RecursionError','ValueError','ZeroDivisionError'])\n\npure=higher+'@fun\\ndef plus(x:int)->int:\\n    return x+1\\n@fun\\ndef double(x:int)->int:\\n    return x*2\\n@fun\\ndef divide(a:int,b:int)->int:\\n    return a//b\\n'\nadd('C01',pure+'@fun\\ndef probe(x:int)->int:\\n    return compose(double,plus)(x)\\n',required_effects=[],failures=[])\nadd('C02',pure+'@fun\\ndef probe()->Callable[[int],int]:\\n    return compose(double,plus)\\n',latent=True,required_effects=[],failures=[])\nadd('C03',pure+'@fun\\ndef probe(x:int)->int:\\n    return partial_first(divide,10)(x)\\n',required_effects=[],failures=['ZeroDivisionError'])\nadd('C04',pure+'@fun\\ndef probe()->Callable[[int],int]:\\n    return partial_first(divide,10)\\n',latent=True,required_effects=[],failures=[])\nadd('C05',pure+'@fun\\ndef probe(x:int)->int:\\n    try:\\n        return partial_first(divide,10)(x)\\n    except ZeroDivisionError:\\n        return 0\\n',required_effects=[],failures=[])\nadd('C06',pure+'@fun\\ndef probe(x:int)->int:\\n    op=partial_first(divide,10)\\n    first=op(x)\\n    try:\\n        return op(first)\\n    except ZeroDivisionError:\\n        return 0\\n',required_effects=[],failures=['ZeroDivisionError'])\nadd('C07',pure+'@fun\\ndef probe(values:Vector[int])->Vector[int]:\\n    return values.map(compose(double,plus))\\n',required_effects=[])\nadd('C08',pure+'@fun\\ndef probe(values:Vector[int])->Vector[int]:\\n    return values.map(partial_first(divide,10))\\n',required_effects=[],failures=['ZeroDivisionError'])\nadd('C09',pure+'@fun\\ndef probe(x:int,flag:bool)->int:\\n    op=compose(double,plus) if flag else partial_first(divide,10)\\n    return op(x)\\n',required_effects=[],contains={'failures':['ZeroDivisionError']})\nadd('C10',pure+'@fun\\ndef probe(x:int)->int:\\n    return compose(compose(double,plus),plus)(x)\\n',required_effects=[],failures=[])\nadd('C11',pure+'@fun\\ndef maker(op:Callable[[int],int])->Callable[[int],int]:\\n    return compose(double,op)\\n@fun\\ndef probe(x:int)->int:\\n    return maker(plus)(x)\\n',required_effects=[],failures=[])\nadd('C12',pure+'@fun\\ndef maker(op:Callable[[int,int],int])->Callable[[int],int]:\\n    return partial_first(op,10)\\n@fun\\ndef probe(x:int)->int:\\n    return maker(divide)(x)\\n',required_effects=[],failures=['ZeroDivisionError'])\nadd('C13',pure+'@fun\\ndef probe(op:Callable[[int],int],x:int)->int:\\n    try:\\n        return compose(double,op)(x)\\n    except ValueError:\\n        return 0\\n',required_effects=[],failures=['IndexError','KeyError','RecursionError','ZeroDivisionError'])\nadd('C14',pure+'@fun\\ndef probe(flag:bool)->Callable[[int],int]:\\n    return compose(double,plus) if flag else partial_first(divide,10)\\n',latent=True,required_effects=[],failures=[])\nadd('C15',pure+'@fun\\ndef maker(bound:int)->Callable[[int],int]:\\n    return partial_first(divide,bound)\\n@fun\\ndef probe(x:int)->int:\\n    return maker(10)(x)\\n',required_effects=[],failures=['ZeroDivisionError'])\nadd('C16',pure+'@fun\\ndef probe(x:int)->int:\\n    fixed=3\\n    def add(y:int)->int:\\n        return y+fixed\\n    return compose(double,add)(x)\\n',required_effects=[],failures=[])\nfor i,body in enumerate(('compose(double,plus,plus)(x)','compose(outer=double,inner=plus)(x)','compose(double,unknown)(x)','partial_first(divide,[])(x)','partial_first(divide,plus)(x)','partial_first(divide,state(1))(x)','partial_first(divide)(x)','compose(divide,plus)(x)','compose(double,plus)(\"x\")'),1):\n add(f'C-negative-{i:02}',pure+'from pyalamode import state\\n@fun\\ndef probe(x:int)->int:\\n    return '+body+'\\n',1)\nadd('C-negative-mutable-capture',pure+'@fun\\ndef probe(x:int)->int:\\n    changing=[]\\n    def inner(y:int)->int:\\n        return changing[0]+y\\n    return compose(double,inner)(x)\\n',1)\nadd('C-negative-capcapture',higher+'@fun\\n@effects(Clock)\\ndef probe(cap:ClockCapability)->int:\\n    def inner(x:int)->int:\\n        return cap.now_ns()+x\\n    return compose(inner,inner)(1)\\n',1)\n\nclock=higher+'@fun\\n@effects(Clock)\\ndef now(cap:ClockCapability)->int:\\n    return cap.now_ns()\\n@fun\\ndef plus(x:int)->int:\\n    return x+1\\n@fun\\n@effects(Clock)\\ndef timed(bound:int,cap:ClockCapability)->int:\\n    return cap.now_ns()//bound\\n'\nadd('E01',clock+'@fun\\ndef probe()->Effectful[[ClockCapability],int,Clock]:\\n    return compose(plus,now)\\n',latent=True,required_effects=[],failures=[])\nadd('E02',clock+'@fun\\n@effects(Clock)\\ndef probe(cap:ClockCapability)->int:\\n    return compose(plus,now)(cap)\\n',required_effects=['Clock'],effect_bound=['Clock'],failures=['IndexError','OSError','RuntimeError'])\nadd('E03',clock+'@fun\\n@effects(Clock)\\ndef probe(cap:ClockCapability)->int:\\n    try:\\n        return partial_first(timed,0)(cap)\\n    except (RuntimeError,OSError,IndexError,ZeroDivisionError):\\n        return 0\\n',required_effects=['Clock'],effect_bound=['Clock'],failures=[])\nadd('E04',clock+'@fun\\ndef probe(cap:ClockCapability)->int:\\n    return compose(plus,now)(cap)\\n',1)\nadd('E05',clock+'@fun\\n@effects(Clock)\\ndef probe(cap:ClockCapability)->Callable[[int],int]:\\n    return partial_first(timed,cap)\\n',1)\nadd('E06',clock+'@fun\\ndef maker(op:Effectful[[ClockCapability],int,Clock,IO])->Effectful[[ClockCapability],int,Clock,IO]:\\n    return compose(plus,op)\\n@fun\\n@effects(Clock)\\ndef probe(cap:ClockCapability)->int:\\n    return maker(now)(cap)\\n',required_effects=['Clock'],effect_bound=['Clock'],failures=['IndexError','OSError','RuntimeError'])\nfor family,cap,call,ret,failures in (('IO','IOCapability','cap.read_text(\"input\")','str',['KeyError','OSError','RuntimeError','UnicodeError','ValueError']),('Clock','ClockCapability','cap.now_ns()','int',['IndexError','OSError','RuntimeError']),('Environment','EnvironmentCapability','cap.get(\"MODE\",\"off\")','str',['OSError','RuntimeError','UnicodeError','ValueError'])):\n add('F-'+family,higher+'@fun\\n@effects('+family+')\\ndef probe(cap:'+cap+')->'+ret+':\\n    return '+call+'\\n',required_effects=[family],effect_bound=[family],failures=failures)\n add('F-'+family+'-handled',higher+'@fun\\n@effects('+family+')\\ndef probe(cap:'+cap+')->'+ret+':\\n    try:\\n        return '+call+'\\n    except (OSError,RuntimeError,ValueError,IndexError,KeyError):\\n        return '+('0' if ret=='int' else '\"failure\"')+'\\n',required_effects=[family],effect_bound=[family],failures=[])\n add('F-'+family+'-pure',higher+'@fun\\ndef probe(cap:'+cap+')->'+ret+':\\n    return '+call+'\\n',1)\n\n# Closed vocabulary refuses arbitrary standard-library dispatch and native hooks.\nfor i,(imp,expr,result) in enumerate((('import json','json.loads(\"{}\")','int'),('import pickle','pickle.loads(b\"x\")','int'),('import codecs','codecs.decode(b\"x\",\"utf-8\")','str'),('import locale','locale.atoi(\"12\")','int'),('import os','os.getenv(\"MODE\")','str'),('import time','time.time_ns()','int'),('from functools import partial','partial(abs,1)()','int'),('','\"x\".format()','str'),('','\"x\".encode(\"utf-8\")','bytes'),('','b\"x\".decode(\"utf-8\")','str'),('','int(\"12\")','int'),('','str(12)','str'),('','sum(Vector.of(1,2))','int'),('','sorted(Vector.of(1,2))','Vector[int]')),1):\n add(f'N{i:02}',base+imp+'\\n@fun\\ndef probe()->'+result+':\\n    return '+expr+'\\n',1)\n\n# Private/native writer routes must invalidate public operation consumers.\nfor i,writer in enumerate(('from pyalamode.standard import _exact as helper\\nhelper.__code__=unknown\\n','import pyalamode.standard as std\\nstd.__dict__[\"utf8_decode\"]=unknown\\n','import pyalamode as pal\\nAlias=pal.standard\\nAlias.__dict__.update({\"integer_parse_decimal\":unknown})\\n','from pyalamode import utf8_encode as operation\\nfrom builtins import setattr as change\\nchange(operation,\"__code__\",unknown)\\n','import builtins\\nbuiltins.ord=unknown\\n','from builtins import chr as helper\\nhelper.__code__=unknown\\n','import builtins\\nbuiltins.UnicodeDecodeError=unknown\\n','from pyalamode.collections import _validate as helper\\nhelper.__code__=unknown\\n','from pyalamode.variants import _validate_case as helper\\nhelper.__code__=unknown\\n'),1):\n add(f'W{i:02}',higher+writer+'@fun\\ndef probe(text:str)->bytes:\\n    return utf8_encode(text)\\n',1)\n\nassert len({c['id'] for c in cases})==len(cases)\npath=OUT/'literal-cases.json';path.write_text(json.dumps(cases,indent=2)+'\\n')\nprint(json.dumps(dict(cases=len(cases),admit=sum(c['expected']==0 for c in cases),refuse=sum(c['expected']==1 for c in cases),sha256=hashlib.sha256(path.read_bytes()).hexdigest())))\n",
  "make_layouts.py": "import hashlib,json\nfrom pathlib import Path\nOUT=Path(__file__).parent;layouts=[]\ndef add(id,files,**fields):layouts.append(dict(id=id,files=files,**fields))\nleaf='# mode: fun\\ndef plus(x:int)->int:\\n    return x+1\\ndef divide(a:int,b:int)->int:\\n    return a//b\\n'\nfactory='# mode: fun\\nfrom typing import Callable\\nfrom pyalamode import compose,partial_first\\nfrom leaf import plus,divide\\ndef maker()->Callable[[int],int]:\\n    return compose(plus,partial_first(divide,10))\\n'\nconsumer='# mode: fun\\nfrom factory import maker\\ndef probe(x:int)->int:\\n    try:\\n        return maker()(x)\\n    except ZeroDivisionError:\\n        return 0\\n'\nadd('wrapper returned handled partial warm',{'leaf.py':leaf,'factory.py':factory,'consumer.py':consumer},expected=0,transition={'consumer.py':consumer+'\\n# independent consumer edit\\n'},failures=[],effects=[])\nconsumer2=consumer.replace('    try:\\n        return maker()(x)\\n    except ZeroDivisionError:\\n        return 0','    return maker()(x)')\nadd('wrapper returned unhandled partial warm',{'leaf.py':leaf,'factory.py':factory,'consumer.py':consumer2},expected=0,transition={'consumer.py':consumer2+'\\n# independent consumer edit\\n'},failures=['ZeroDivisionError'],effects=[])\nfactory2='# mode: fun\\nfrom typing import Callable\\nfrom pyalamode import compose,partial_first\\nfrom leaf import plus,divide\\ndef maker(op:Callable[[int,int],int])->Callable[[int],int]:\\n    return compose(plus,partial_first(op,10))\\n'\nconsumer3='# mode: fun\\nfrom factory import maker\\nfrom leaf import divide\\ndef probe(x:int)->int:\\n    try:\\n        return maker(divide)(x)\\n    except ZeroDivisionError:\\n        return 0\\n'\nadd('factory parameter concrete specialization partial warm',{'leaf.py':leaf,'factory.py':factory2,'consumer.py':consumer3},expected=0,transition={'consumer.py':consumer3+'\\n# independent consumer edit\\n'},failures=[],effects=[])\nclockleaf='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\n@effects(Clock)\\ndef now(cap:ClockCapability)->int:\\n    return cap.now_ns()\\ndef plus(x:int)->int:\\n    return x+1\\n'\nclockfactory='# mode: fun\\nfrom pyalamode import compose,Effectful,Clock,IO,ClockCapability\\nfrom leaf import plus\\ndef maker(op:Effectful[[ClockCapability],int,Clock,IO])->Effectful[[ClockCapability],int,Clock,IO]:\\n    return compose(plus,op)\\n'\nclockconsumer='# mode: fun\\nfrom pyalamode import effects,Clock,ClockCapability\\nfrom factory import maker\\nfrom leaf import now\\n@effects(Clock)\\ndef probe(cap:ClockCapability)->int:\\n    try:\\n        return maker(now)(cap)\\n    except RuntimeError:\\n        return 0\\n'\nadd('factory tighter concrete effects partial warm',{'leaf.py':clockleaf,'factory.py':clockfactory,'consumer.py':clockconsumer},expected=0,transition={'consumer.py':clockconsumer+'\\n# independent consumer edit\\n'},failures=['IndexError','OSError'],effects=['Clock'])\nscalar='from pyalamode import fun,utf8_encode,integer_parse_decimal\\n@fun\\ndef probe(text:str)->bytes:\\n    return utf8_encode(text)\\n'\nwriters=(\n ('public operation method','from pyalamode import utf8_encode as operation\\noperation.__code__=unknown\\n'),\n ('public operation assigned alias','from pyalamode import utf8_encode\\nAlias=utf8_encode\\nAlias.__defaults__=unknown\\n'),\n ('private exact helper','from pyalamode.standard import _exact as helper\\nhelper.__code__=unknown\\n'),\n ('private standard module dictionary','import pyalamode.standard as standard\\nstandard.__dict__[\"_exact\"]=unknown\\n'),\n ('package standard attribute','import pyalamode as product\\nproduct.standard.utf8_encode=unknown\\n'),\n ('stdlib Unicode error identity','import builtins\\nbuiltins.UnicodeEncodeError=unknown\\n'),\n ('native ord direct','import builtins\\nbuiltins.ord=unknown\\n'),\n ('native chr alias module','import builtins as native\\nAlias=native\\nAlias.chr=unknown\\n'),\n ('private collection helper','from pyalamode.collections import _validate as helper\\nhelper.__code__=unknown\\n'),\n ('private variants helper','from pyalamode.variants import _validate_case as helper\\nhelper.__code__=unknown\\n'),\n ('writer setattr alias','from pyalamode import utf8_encode\\nfrom builtins import setattr as write\\nwrite(utf8_encode,\"__code__\",unknown)\\n'),\n ('writer module dictionary update','import pyalamode.standard as standard\\nstandard.__dict__.update({\"utf8_encode\":unknown})\\n'),\n)\nfor id,writer in writers:add('writer '+id,{'core.py':scalar,'writer.py':'pass\\n'},expected=0,transition={'writer.py':writer},changed_expected=1)\nfor name in ('type','int','str','bytes','len','ord','chr','enumerate','range','tuple','list','object','TypeError','ValueError','UnicodeEncodeError','UnicodeDecodeError'):\n add('native foundation '+name,{'core.py':scalar,'writer.py':'pass\\n'},expected=0,transition={'writer.py':'import builtins\\nbuiltins.'+name+'=unknown\\n'},changed_expected=1)\nsetup='''from pyalamode import fun,integer_parse_decimal,live_io,live_clock,live_environment,recorded_clock,recorded_environment\nfrom pathlib import Path\ndef mark():\n    Path(\"sentinel\").write_text(\"executed\")\n    return 0\nmark()\nfiles=live_io(\".\",allowed_ops=(\"read_text\",\"write_text\"))\nclock=live_clock()\nsettings=live_environment()\nrecorded=recorded_clock((3,4))\nrecorded_settings=recorded_environment(((\"MODE\",\"test\"),))\n@fun\ndef probe(text:str)->int:\n    return integer_parse_decimal(text)\n'''\nadd('separate ordinary setup and pure invocation',{'setup.py':setup},expected=0,setup_observations=True)\nadd('strict import refuses ordinary setup',{'setup.py':setup,'consumer.py':'# mode: fun\\nfrom setup import probe\\ndef calculation()->int:\\n    return probe(\"12\")\\n'},expected=1)\nfor mode in ('off','exports','debug'):\n policy='[tool.pyalamode]\\nboundary_guards=\"'+mode+'\"\\n'\n if mode!='off':policy+='guarded_exports=[\"core:probe\"]\\n'\n add('guard '+mode,{'core.py':'from pyalamode import fun,text_split,integer_parse_decimal,Vector,Result,Failure,Ok,Err,result_traverse,failure_value\\n@fun\\ndef parse(text:str)->Result[int,Failure]:\\n    try:\\n        return Ok(integer_parse_decimal(text))\\n    except ValueError as caught:\\n        return Err(failure_value(caught))\\n@fun\\ndef probe(text:str)->Result[Vector[int],Failure]:\\n    return result_traverse(text_split(text,\",\"),parse)\\n','pyproject.toml':policy},expected=0,mode=mode)\nfor label,fragment in (\n ('default','@fun\\ndef probe(text:str=mark())->int:\\n    return integer_parse_decimal(text)\\n'),\n ('annotation','@fun\\ndef probe(text:mark())->int:\\n    return 1\\n'),\n ('initializer','# mode: fun\\nvalue=mark()\\ndef probe()->int:\\n    return 1\\n'),\n ('callback','@fun\\ndef probe(x:Vector[int])->Vector[int]:\\n    return vector_scan(x,mark,0)\\n'),\n):\n source='from pyalamode import fun,integer_parse_decimal,vector_scan,Vector\\nfrom pathlib import Path\\ndef mark(*args):\\n    Path(\"sentinel\").write_text(\"executed\")\\n    return \"1\"\\n'+fragment\n if label=='initializer':source=source.replace('# mode: fun\\n','');source='# mode: fun\\n'+source\n add('nonexecution '+label,{'core.py':source},expected=1,sentinel=True)\nadd('entry effect policy refuses wrapper',{'leaf.py':clockleaf,'factory.py':clockfactory,'consumer.py':clockconsumer,'pyproject.toml':'[tool.pyalamode.effect_bounds]\\n\"consumer:probe\"=[]\\n'},expected=1)\npath=OUT/'literal-layouts.json';path.write_text(json.dumps(layouts,indent=2)+'\\n')\nprint(json.dumps(dict(layouts=len(layouts),sha256=hashlib.sha256(path.read_bytes()).hexdigest())))\n",
  "make_supplement.py": "import hashlib,json\nfrom pathlib import Path\nOUT=Path(__file__).parent\nbase='from pyalamode import fun,Vector,OrderedMap,compose,vector_group_by\\nfrom typing import Callable\\n@fun\\ndef one(x:int)->Vector[int]:\\n    return Vector.of(x)\\n@fun\\ndef size(values:Vector[int])->int:\\n    return len(values)\\n@fun\\ndef nonempty(values:Vector[int])->bool:\\n    return len(values)>0\\n'\nbodies={\n 'V01':'@fun\\ndef probe(x:int)->int:\\n    return compose(size,one)(x)\\n',\n 'V02':'@fun\\ndef probe(x:Vector[int])->Vector[int]:\\n    return x.map(compose(size,one))\\n',\n 'V03':'@fun\\ndef probe(x:Vector[int])->Vector[int]:\\n    return x.filter(compose(nonempty,one))\\n',\n 'V04':'@fun\\ndef probe(x:Vector[int])->OrderedMap[int,Vector[int]]:\\n    return vector_group_by(x,compose(size,one))\\n',\n 'V05':'@fun\\ndef maker()->Callable[[int],int]:\\n    return compose(size,one)\\n@fun\\ndef probe(x:int)->int:\\n    return maker()(x)\\n',\n 'V06':'@fun\\ndef probe(x:int)->int:\\n    try:\\n        return compose(size,one)(x)\\n    except RuntimeError:\\n        return 0\\n',\n}\ncases=[dict(id=id,source=base+body,expected=0,failures=[] if id=='V06' else ['RecursionError'],required_effects=[]) for id,body in bodies.items()]\np=OUT/'supplemental-cases.json';p.write_text(json.dumps(cases,indent=2)+'\\n');print(json.dumps(dict(cases=len(cases),sha256=hashlib.sha256(p.read_bytes()).hexdigest())))\n",
  "project_probe.py": "import json,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\nOUT=Path(__file__).parent;checks=0;rows=[]\nlayouts=json.loads((OUT/'literal-layouts.json').read_text())\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\ndef write(root,files):\n for name,source in files.items():\n  path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source)\ndef contracts(result):return {c.name:c for f in result.results for c in f.contracts}\ndef observe(root,label,expected,cache=True):\n try:result=check_paths(root=root,cache=cache)\n except Exception:\n  print(json.dumps({\"failed_label\":label,\"literal_files\":{p.name:p.read_text() for p in root.glob(\"*.py\")}}));raise\n report=result.to_dict();check(report['standard_operation_version']=='pyalamode.standard-v1',label+' versioned standard catalog');check(len(report['standard_catalog'])==22,label+' finite catalog denominator')\n check(result.status==expected,label+' status '+str(result.status)+' '+str([d.reason for f in result.results for d in f.diagnostics]))\n rows.append(dict(label=label,status=result.status,hits={Path(f.path).name:f.cache_hit for f in result.results},report=result.to_dict()))\n return result\nfor layout in layouts:\n with tempfile.TemporaryDirectory(prefix='m07-project-') as d:\n  root=Path(d);write(root,layout['files']);label=layout['id'];status=layout['expected']\n  cold=observe(root,label+' cold',status,False)\n  check(not (root/'sentinel').exists(),label+' check nonexecution')\n  populated=observe(root,label+' cache clear',status);warm=observe(root,label+' full warm',status)\n  check(all(f.cache_hit for f in warm.results),label+' full warm all files')\n  if not status:\n   check({k:v.__dict__ for k,v in contracts(cold).items()}=={k:v.__dict__ for k,v in contracts(warm).items()},label+' cold/full-warm exact contracts')\n  if 'failures' in layout:\n   for result in (cold,warm):\n    c=contracts(result)['probe'];check(c.failures==layout['failures'],label+' exact failures');check(c.required_effects==layout['effects'],label+' actual invocation effects')\n    maker=contracts(result)['maker'];check(maker.required_effects==[],label+' latent factory effects');check(bool(maker.return_callable_evidence),label+' retained wrapper evidence')\n  if 'transition' in layout:\n   write(root,layout['transition']);changed_status=layout.get('changed_expected',status)\n   changed=observe(root,label+' partial/changed warm',changed_status)\n   fresh=observe(root,label+' changed fresh',changed_status,False)\n   check({k:v.__dict__ for k,v in contracts(changed).items()}=={k:v.__dict__ for k,v in contracts(fresh).items()},label+' partial/fresh evidence agreement')\n   if 'failures' in layout:\n    hits={Path(f.path).name:f.cache_hit for f in changed.results}\n    check(hits['leaf.py'] and hits['factory.py'] and not hits['consumer.py'],label+' actual partial reused dependencies')\n    c=contracts(changed)['probe'];check(c.failures==layout['failures'],label+' partial exact failures');check(c.required_effects==layout['effects'],label+' partial exact effects')\n    check({k:v.__dict__ for k,v in contracts(cold).items()}=={k:v.__dict__ for k,v in contracts(changed).items()},label+' cold/partial exact contracts')\n   status=changed_status\n  built=build_paths(root=root,output=root/'artifact')\n  check(built.status==status,label+' build gate '+str(built.status));check((root/'artifact').exists()==(status==0),label+' artifact iff verified');check(not (root/'sentinel').exists(),label+' build nonexecution')\n  if layout.get('setup_observations'):\n   f=next(f for f in cold.results if Path(f.path).name=='setup.py')\n   check(f.initialization_evidence=='unchecked ordinary module initialization',label+' separately unchecked initialization')\n   check(contracts(cold)['probe'].behavior=='pure',label+' separately pure invocation')\n   setup=getattr(f,'setup_observations',None)\n   check(bool(setup),label+' visible characterized setup observations')\n   check(any('live_io' in json.dumps(r) and 'IO' in json.dumps(r) for r in setup),label+' IO root setup identity/effect')\n   check(any('live_clock' in json.dumps(r) for r in setup),label+' clock allocation setup identity')\n   check(any('live_environment' in json.dumps(r) for r in setup),label+' environment allocation setup identity')\nreport=dict(assertions=checks,rows=rows,layouts=len(layouts))\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'project-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,checks=len(rows),layouts=len(layouts))))\n",
  "runtime_probe.py": "import json,subprocess,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode import *\nfrom pyalamode import standard as std\nOUT=Path(__file__).parent;checks=0;rows=[];hooks=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\ndef raises(kind,call,label):\n global checks\n checks+=1\n try:call()\n except kind:return\n raise AssertionError(label)\n\n# Exact results and boundary grammar are fixed independently of implementation.\nfor text,sep,want in (('',',',Vector.of('')),(',a,,',',',Vector.of('','a','','')),('a::b::','::',Vector.of('a','b','')),('e\\u0301|\\U0001f63a','|',Vector.of('e\\u0301','\\U0001f63a'))):check(text_split(text,sep)==want,'split '+repr(text))\nraises(ValueError,lambda:text_split('x',''),'empty separator')\ncheck(text_join(Vector.of('a','','b'),'|')=='a||b','join order');check(text_join(Vector.of(),'|')=='','empty join')\ncheck(text_replace('aaa','aa','b')=='ba','nonoverlap replace');check(text_replace('ab','','X')=='XaXbX','empty replace boundaries')\ncheck(text_startswith('x',''),'empty prefix');check(not text_startswith('ab','b'),'prefix false')\ncheck(text_slice('a\\U0001f63ab',1,2)=='\\U0001f63a','codepoint slice');check(text_slice('abc',-20,20)=='abc','clamped slice');check(text_slice('abc',3,1)=='','reversed slice')\nfor value,lo,hi,want in ((4,1,3,3),(-5,1,3,1),(2,1,3,2),(0,0,0,0),(10**100,0,10**99,10**99)):check(integer_clamp(value,lo,hi)==want,'clamp')\nraises(ValueError,lambda:integer_clamp(1,3,2),'invalid clamp bound')\nfor text,want in (('0',0),('-0',0),('+00012',12),('-123',-123),('9'*4096,10**4096-1)):\n check(integer_parse_decimal(text)==want,'bounded parse');check(integer_parse_decimal(integer_format_decimal(want))==want,'decimal roundtrip')\nfor text in ('','+','-',' 1','1 ','1_0','1.0','\\u0661','\\uff11','0x10','++1','1\\n','0'*4097):raises(ValueError,lambda text=text:integer_parse_decimal(text),'refused decimal grammar')\nraises(ValueError,lambda:integer_format_decimal(10**4096),'decimal format bound')\nlimit=sys.get_int_max_str_digits();sys.set_int_max_str_digits(640)\ntry:\n check(integer_format_decimal(10**4095)=='1'+'0'*4095,'format independent ambient digit limit')\n check(integer_parse_decimal('9'*4096)==10**4096-1,'parse independent ambient digit limit')\nfinally:sys.set_int_max_str_digits(limit)\nfor text in ('','\\x00','ASCII','\\ufeffa','e\\u0301','\\x7f','\\x80','\\u07ff','\\u0800','\\ud7ff','\\ue000','\\uffff','\\U00010000','\\U0010ffff'):\n expected=text.encode('utf-8');check(utf8_encode(text)==expected,'valid encode boundary');check(utf8_decode(expected)==text,'valid decode boundary')\nfor cp in [((i*7919)%0x110000) for i in range(256)]:\n if 0xd800<=cp<=0xdfff:continue\n text=chr(cp);raw=text.encode('utf-8');check(utf8_encode(text)==raw,'sample encode');check(utf8_decode(raw)==text,'sample decode')\nfor text in ('\\ud800','\\udfff','a\\ud800b','\\ud800\\udc00'):raises(UnicodeError,lambda text=text:utf8_encode(text),'surrogate encode refusal')\nfor raw in (b'\\x80',b'\\xc0\\x80',b'\\xc1\\xbf',b'\\xc2',b'\\xc2A',b'\\xe0\\x80\\x80',b'\\xed\\xa0\\x80',b'\\xf0\\x80\\x80\\x80',b'\\xf4\\x90\\x80\\x80',b'\\xf5\\x80\\x80\\x80',b'\\xff',b'abc\\xe2\\x82'):\n raises(UnicodeError,lambda raw=raw:utf8_decode(raw),'invalid UTF8 refusal')\nfor raw in (b'',b'\\x00',bytes(range(256)),b'\\xff\\x80A'):\n check(hex_encode(raw)==raw.hex(),'lowercase hex');check(hex_decode(raw.hex().upper())==raw,'hex roundtrip')\nfor text in ('0','abc',' 00','00 ','0g','\\uff10\\uff10','00\\n'):raises(ValueError,lambda text=text:hex_decode(text),'strict hex grammar')\n\nclass Foreign:\n def __getattribute__(self,name):hooks.append('getter');return object.__getattribute__(self,name)\n def __iter__(self):hooks.append('iterator');return iter(())\n def __str__(self):hooks.append('str');return 'foreign'\n def __repr__(self):hooks.append('repr');return 'foreign'\n def __hash__(self):hooks.append('hash');return 0\n def __eq__(self,other):hooks.append('equal');return False\n def __call__(self,*args):hooks.append('call');return 1\nclass Text(str):\n def __getattribute__(self,name):hooks.append('text-getter');return super().__getattribute__(name)\n def __str__(self):hooks.append('text-str');return 'foreign'\nclass Number(int):\n def __index__(self):hooks.append('index');return 1\n def __add__(self,value):hooks.append('add');return 1\nclass Binary(bytes):\n def hex(self,*args):hooks.append('hex');return ''\nforeign=Foreign();hooks.clear()\nfor label,call in (\n ('split subtype',lambda:text_split(Text('a'),'a')),('join nested subtype',lambda:text_join(Vector.of(1),',')),\n ('slice bool',lambda:text_slice('a',True,1)),('clamp subtype',lambda:integer_clamp(Number(1),0,2)),\n ('parse foreign',lambda:integer_parse_decimal(foreign)),('format foreign',lambda:integer_format_decimal(foreign)),\n ('UTF8 text subtype',lambda:utf8_encode(Text('a'))),('UTF8 bytes subtype',lambda:utf8_decode(Binary(b'a'))),\n ('hex foreign',lambda:hex_encode(foreign)),('hex subtype',lambda:hex_decode(Text('00'))),\n ('scan callback object',lambda:vector_scan(Vector.of(1),foreign,0)),('scan input iterator',lambda:vector_scan(foreign,lambda a,b:a+b,0)),\n ('group callback object',lambda:vector_group_by(Vector.of(1),foreign)),('compose callback object',lambda:compose(foreign,lambda x:x)),\n ('partial bound capability',lambda:partial_first(lambda a,b:b,state(1))),('partial bound callable',lambda:partial_first(lambda a,b:b,lambda:1)),\n ('traverse callback object',lambda:result_traverse(Vector.of(1),foreign)),('traverse input iterable',lambda:result_traverse((1,),lambda x:Ok(x))),\n):\n raises(TypeError,call,'exact validation '+label);check(hooks==[],'hook zero '+label)\n\norder=[]\ndef add(a,b):order.append(('scan',a,b));return a+b\nold=Vector.of(1,2,3);scanned=vector_scan(old,add,10)\ncheck(scanned==Vector.of(10,11,13,16),'scan includes initial');check(order==[('scan',10,1),('scan',11,2),('scan',13,3)],'scan callback order');check(old==Vector.of(1,2,3),'scan preserves input')\norder.clear();check(vector_scan(Vector.of(),add,7)==Vector.of(7),'empty scan');check(order==[],'empty scan no callback')\ndef group(x):order.append(x);return x%3\nitems=Vector.of(5,2,4,3,1,8);grouped=vector_group_by(items,group)\ncheck(order==[5,2,4,3,1,8],'group once input order');check(grouped.entries()==Vector.of((2,Vector.of(5,2,8)),(1,Vector.of(4,1)),(0,Vector.of(3))),'first encounter group order')\ncheck(vector_group_by(Vector.of(),group)==OrderedMap(),'empty groups')\norder.clear()\ndef inner(x):order.append('inner');return x+1\ndef outer(x):order.append('outer');return x*2\nwrapped=compose(outer,inner);check(order==[],'compose construction latent');check(wrapped(3)==8,'compose result');check(order==['inner','outer'],'compose order')\norder.clear()\ndef divide(a,b):order.append((a,b));return a//b\nbound=partial_first(divide,10);check(order==[],'partial construction latent');check(bound(2)==5,'partial argument order');check(order==[(10,2)],'partial once')\norder.clear()\ndef fail(x):order.append('failure');return 1//0\nraises(ZeroDivisionError,lambda:compose(outer,fail)(3),'composition first raised failure');check(order==['failure'],'outer skipped after inner failure')\norder.clear()\ndef choose(x):\n order.append(x)\n return Err('bad:'+str(x)) if x==2 else Ok(x*10)\ncheck(result_traverse(Vector.of(1,2,3),choose)==Err('bad:2'),'first result error');check(order==[1,2],'traversal failfast')\norder.clear();check(result_traverse(Vector.of(),choose)==Ok(Vector.of()),'empty traverse');check(order==[],'empty traverse no callback')\ncheck(result_traverse(Vector.of(1,3),choose)==Ok(Vector.of(10,30)),'all successes ordered')\nfor call,label in ((lambda:vector_scan(Vector.of(1),lambda a,b:foreign,0),'scan foreign output'),(lambda:vector_group_by(Vector.of(1),lambda x:foreign),'group foreign key'),(lambda:compose(lambda x:foreign,lambda x:x)(1),'compose foreign output'),(lambda:partial_first(lambda a,b:foreign,1)(2),'partial foreign output'),(lambda:result_traverse(Vector.of(1),lambda x:foreign),'traverse foreign case')):\n raises(TypeError,call,label);check(hooks==[],label+' no output hooks')\nraises(TypeError,lambda:vector_group_by(Vector.of(1,2),lambda x:True if x==1 else 1),'heterogeneous exact group domains')\n\n# Isolated registry mutation must not leak to any other test or report.\nregistry=r'''import codecs,json,tempfile\nfrom pathlib import Path\nfrom pyalamode import utf8_encode,utf8_decode,live_io\nhits=[]\ndef changed(error):\n hits.append(type(error).__name__)\n return (b'replacement' if isinstance(error,UnicodeEncodeError) else 'replacement',error.end)\ncodecs.register_error('strict',changed)\ncodecs.register_error('surrogateescape',changed)\nchecks=0\ndef refuses(call):\n global checks\n checks+=1\n try:call()\n except UnicodeError:return\n raise AssertionError('custom strict registry replaced required failure')\nfor text in ('\\ud800','a\\udfff','\\ud800\\udc00'):refuses(lambda text=text:utf8_encode(text))\nfor raw in (b'\\xff',b'\\xc0\\x80',b'\\xed\\xa0\\x80',b'\\xf4\\x90\\x80\\x80',b'\\xe2\\x82'):refuses(lambda raw=raw:utf8_decode(raw))\nassert utf8_encode('\\ufeff\\x00\\U0010ffff')==b'\\xef\\xbb\\xbf\\x00\\xf4\\x8f\\xbf\\xbf';checks+=1\nassert utf8_decode(b'\\xef\\xbb\\xbf\\r\\na\\r')=='\\ufeff\\r\\na\\r';checks+=1\nwith tempfile.TemporaryDirectory(prefix='m07-registry-') as d:\n root=Path(d);cap=live_io(d,allowed_ops=('read_text','write_text'))\n (root/'invalid').write_bytes(b'\\xff');refuses(lambda:cap.read_text('invalid'))\n (root/'target').write_bytes(b'old');refuses(lambda:cap.write_text('target','\\ud800'))\n assert (root/'target').read_bytes()==b'';checks+=1\n # Failure cleanup permits another write to the same rooted target.\n cap.write_text('target','\\ufeff\\r\\na\\r');assert (root/'target').read_bytes()==b'\\xef\\xbb\\xbf\\r\\na\\r';checks+=1\n assert cap.read_text('target')=='\\ufeff\\r\\na\\r';checks+=1\n for bad in ('\\ud800','\\udc80','a\\udfff'):\n  for call in (lambda bad=bad:cap.read_text(bad),lambda bad=bad:cap.write_text(bad,'text'),lambda bad=bad:live_io(str(root)+'/'+bad,allowed_ops=('read_text',)),lambda bad=bad:__import__('pyalamode').live_environment().get(bad,'default')):\n   checks+=1\n   try:call()\n   except ValueError:pass\n   else:raise AssertionError('non-scalar Unicode OS input admitted')\n cap.write_text('caf\\u00e9','valid');assert cap.read_text('caf\\u00e9')=='valid';checks+=1\n assert __import__('pyalamode').live_environment().get('M07_CAF\\u00c9_MISSING','default')=='default';checks+=1\n import os\n key=b'M07_REVIEW_INVALID_NATIVE_VALUE'\n prior=os.environb.get(key)\n try:\n  for raw,want in ((b'\\xff','\\udcff'),(b'\\xed\\xa0\\x80','\\udced\\udca0\\udc80'),(bytes(range(0x80,0x100)),''.join(chr(0xdc00+n) for n in range(0x80,0x100)))):\n   os.environb[key]=raw\n   assert __import__('pyalamode').live_environment().get(key.decode('ascii'),'default')==want;checks+=1\n finally:\n  if prior is None:os.environb.pop(key,None)\n  else:os.environb[key]=prior\nassert hits==[];checks+=1\nprint(json.dumps({'assertions':checks,'handler_hits':hits,'write_truncated_before_encoding_failure':True,'whole_path_cleanup':True}))\n'''\nran=subprocess.run([sys.executable,'-c',registry],capture_output=True,text=True)\ncheck(ran.returncode==0,'registry isolated sentinel '+ran.stderr)\nrows.append(dict(label='codec registry and IO',status=ran.returncode,stdout=ran.stdout,stderr=ran.stderr,literal_source=registry))\nreport=dict(assertions=checks,hook_calls=hooks,subprocesses=rows)\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'runtime-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,hook_calls=hooks,subprocesses=len(rows),isolated_assertions=json.loads(ran.stdout)['assertions'])))\n",
  "static_probe.py": "import hashlib,json,sys\nfrom pathlib import Path\nfrom pyalamode.checker import analyze_source\nOUT=Path(__file__).parent\nrows=[]\nfor corpus in ('m06-literal-cases.json','literal-cases.json','supplemental-cases.json','narrowing-cases.json'):\n    cases=json.loads((OUT/corpus).read_text())\n    for original in cases:\n        case=dict(original)\n        if corpus.startswith('m06-'):\n            case['id']='M6-'+case['id']\n            if original['id'] in {'F41','F42'}:\n                case['failures']=sorted(set(case['failures'])|{'UnicodeError'})\n        result=analyze_source(case['source'],path='<m07_'+case['id']+'>')\n        contracts={c.name:c for c in result.contracts}\n        probe=contracts.get(case.get('boundary','probe'))\n        problems=[]\n        if result.status!=case['expected']:problems.append('status')\n        if case.get('selected') is not None and result.selected_functions<case['selected']:problems.append('selection')\n        if not result.status and probe:\n            for key in ('failures','required_effects','effect_bound'):\n                if key in case and sorted(case[key])!=getattr(probe,key):problems.append(key)\n            for key,required in case.get('contains',{}).items():\n                if not set(required)<=set(getattr(probe,key)):problems.append('contains '+key)\n            if case.get('latent'):\n                if probe.required_effects:problems.append('latent effects')\n                if not probe.return_callable_evidence:problems.append('latent evidence')\n        rows.append(dict(id=case['id'],expected=case['expected'],observed=result.status,selected=result.selected_functions,problems=problems,\n                         diagnostics=[d.__dict__ for d in result.diagnostics],contracts={name:c.__dict__ for name,c in contracts.items()}))\nreport=dict(corpus_sha256={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ('m06-literal-cases.json','literal-cases.json','supplemental-cases.json','narrowing-cases.json')},rows=rows,unexpected=[r for r in rows if r['problems']])\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'static-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(cases=len(rows),unexpected=[dict(id=r['id'],problems=r['problems'],expected=r['expected'],observed=r['observed'],diagnostics=[d['reason'] for d in r['diagnostics']]) for r in report['unexpected']])))\nraise SystemExit(bool(report['unexpected']))\n"
}
```

## Additional fixed shared-global writer refusals before source freeze

The main worker found a concrete shared-module-global write before source freeze: a standard function exposes its module dictionary through `__globals__`. The original 512 expected outcomes stay fixed. Root requested this independent addition before probing its correction. Sixteen literal cases below all require refusal, including an operation consumer distinct from the function used to obtain the shared dictionary, direct and aliased subscript/method writers, public/private functions and nested builtin dictionaries. The writer corpus SHA-256 is `88b147ee859e74e5a1e469cc855a7c200dd0db2d75a2498bd3586ba5d1886e2b`; the complete static corpus is now 528 rows: 187 admits and 341 refusals. This changes no original source byte or expected result.

```json
[
  {
    "id": "V08",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd.text_replace.__globals__['str']=print\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public direct subscript invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V09",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std.text_replace.__globals__\ng['str']=print\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public aliased subscript invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V10",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd.text_replace.__globals__.update(str=print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public direct update invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V11",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std.text_replace.__globals__\ng.update(str=print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public aliased update invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V12",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd.text_replace.__globals__.__setitem__('str',print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public direct setitem invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V13",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std.text_replace.__globals__\ng.__setitem__('str',print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public aliased setitem invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V14",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd._exact.__globals__['str']=print\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private direct subscript invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V15",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std._exact.__globals__\ng['str']=print\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private aliased subscript invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V16",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd._exact.__globals__.update(str=print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private direct update invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V17",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std._exact.__globals__\ng.update(str=print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private aliased update invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V18",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd.text_replace.__globals__['__builtins__']['str']=print\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public nested builtins subscript invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V19",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std.text_replace.__globals__['__builtins__']\ng['str']=print\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public nested builtins alias invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V20",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd._exact.__globals__['__builtins__'].update(str=print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private nested builtins update invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V21",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\ng=std._exact.__globals__['__builtins__']\ng.update(str=print)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private nested builtins alias update invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V22",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd.text_replace.__globals__.pop('str',None)\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "public dictionary pop invalidates shared standard module/native foundation, including a distinct consumer"
  },
  {
    "id": "V23",
    "source": "import pyalamode.standard as std\nfrom pyalamode import fun,text_startswith\nstd._exact.__globals__.clear()\n@fun\ndef probe(text:str)->bool:\n    return text_startswith(text,\"a\")\n",
    "expected": 1,
    "selected": 1,
    "note": "private dictionary clear invalidates shared standard module/native foundation, including a distinct consumer"
  }
]
```

The static and final harnesses add this corpus to their input inventory. Revised complete executable harness map and changed/new full file contents are fixed below before running these new cases. The historical initial manifest remains above as provenance.

```json
{
  "cli_probe.py": "251cc975f42f3b3c678021fa4cd8afea1e8a1474a00aee8c4495c484518fed0e",
  "environment_probe.py": "2b16da1d5c5bdc1132c00e2a92b4c3c1aca27c5cc49edf5f1c610b750ad99b49",
  "final_probe.py": "de9f683cf11d0fd1aabca927ad6ed44c8d4a6100d8f8ebcfa3b3dd7bfee68e20",
  "freshness_probe.py": "1b7155a377fe27d92541996044e26a2cfc5e5780c65397c626d44501292eeb30",
  "m06_cli_probe.py": "be44b9bf2d611fa580c5d88045c373f78ef4671246dff7fab85abc9e5180799a",
  "m06_freshness_probe.py": "e981fdee013e9c2140bbf619004723eec5d3fdf11706753b64552d27dd8e6d39",
  "m06_nonexecution_probe.py": "d8fd3094bf9e6daa5eeefa6bd19f9ef581ddc1b35e858973fc49fa110d509ef4",
  "m06_project_probe.py": "e9dd75392a8198925edf7641dce3a9178abfb132048ac80c1e20a75f4cad854e",
  "m06_runtime_probe.py": "c8eef2d0cb8f4d486cddaa0f7b940b4e5f17b4518541159cb531c559cd989e8b",
  "make_cases.py": "d3de5400f1d0238e4a46e66f2a699920cb4f62afdbba90683569a27f43d6b5c6",
  "make_layouts.py": "bd1e4e48627d32ea034aab2e987b5ebe87cab955587487edbb6bb01e9e61c78e",
  "make_supplement.py": "efc84afdb89e1b5aa35af783dc36d245f0a8d7c622111e2786cbe18e4f5573f6",
  "make_writers.py": "2ea5a876c4f8ac3680ffe0ab272427d10ec26c6e76e4ee8fd932b6a678ac6c52",
  "project_probe.py": "ada8aeb6267f3986e073e8b5ac161e524ee7c6be6e867de01b35e39c2f41e3df",
  "runtime_probe.py": "77516e940c97ef1f7fcf2c1184e26d7c68eeb12c24748557160e8c282c3c9dd7",
  "static_probe.py": "506eba4603d03e3ab8ec8dce19bae74c81dccc3fa740698b7fcb52eebceec99d"
}
```

```json
{
  "static_probe.py": "import hashlib,json,sys\nfrom pathlib import Path\nfrom pyalamode.checker import analyze_source\nOUT=Path(__file__).parent\nrows=[]\nfor corpus in ('m06-literal-cases.json','literal-cases.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json'):\n    cases=json.loads((OUT/corpus).read_text())\n    for original in cases:\n        case=dict(original)\n        if corpus.startswith('m06-'):\n            case['id']='M6-'+case['id']\n            if original['id'] in {'F41','F42'}:\n                case['failures']=sorted(set(case['failures'])|{'UnicodeError'})\n        result=analyze_source(case['source'],path='<m07_'+case['id']+'>')\n        contracts={c.name:c for c in result.contracts}\n        probe=contracts.get(case.get('boundary','probe'))\n        problems=[]\n        if result.status!=case['expected']:problems.append('status')\n        if case.get('selected') is not None and result.selected_functions<case['selected']:problems.append('selection')\n        if not result.status and probe:\n            for key in ('failures','required_effects','effect_bound'):\n                if key in case and sorted(case[key])!=getattr(probe,key):problems.append(key)\n            for key,required in case.get('contains',{}).items():\n                if not set(required)<=set(getattr(probe,key)):problems.append('contains '+key)\n            if case.get('latent'):\n                if probe.required_effects:problems.append('latent effects')\n                if not probe.return_callable_evidence:problems.append('latent evidence')\n        rows.append(dict(id=case['id'],expected=case['expected'],observed=result.status,selected=result.selected_functions,problems=problems,\n                         diagnostics=[d.__dict__ for d in result.diagnostics],contracts={name:c.__dict__ for name,c in contracts.items()}))\nreport=dict(corpus_sha256={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ('m06-literal-cases.json','literal-cases.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json')},rows=rows,unexpected=[r for r in rows if r['problems']])\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'static-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(cases=len(rows),unexpected=[dict(id=r['id'],problems=r['problems'],expected=r['expected'],observed=r['observed'],diagnostics=[d['reason'] for d in r['diagnostics']]) for r in report['unexpected']])))\nraise SystemExit(bool(report['unexpected']))\n",
  "final_probe.py": "import hashlib,json,platform,re,subprocess,sys,sysconfig,time\nfrom pathlib import Path\nimport pyalamode\nOUT=Path(__file__).parent;ROOT=Path(sys.argv[1]);NAME=sys.argv[2]\ndef digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()\ndef source_map():\n    paths=[ROOT/'pyproject.toml',ROOT/'README.md']\n    for area in ('pyalamode','tests','examples','benchmarks'):paths.extend((ROOT/area).rglob('*.py'))\n    result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths)) if '__pycache__' not in p.parts}\n    for p in sorted(OUT.glob('*.py')):result['reviewer:'+p.name]=digest(p)\n    for p in (OUT/'literal-cases.json',OUT/'m06-literal-cases.json',OUT/'literal-layouts.json',OUT/'supplemental-cases.json',OUT/'narrowing-cases.json',OUT/'writer-cases.json'):result['reviewer:'+p.name]=digest(p)\n    return result\ndef installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}\nbefore=source_map();installed_before=installed_map()\nassert len(installed_before)==15\nassert all(before[k]==v for k,v in installed_before.items())\nresults=[]\nfor script in ('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','freshness_probe.py','m06_runtime_probe.py','m06_project_probe.py','m06_cli_probe.py','m06_nonexecution_probe.py','m06_freshness_probe.py','environment_probe.py'):\n    target=NAME+'-'+script.removesuffix('_probe.py')+'.json'\n    started=time.perf_counter();ran=subprocess.run([sys.executable,str(OUT/script),target],cwd=OUT,capture_output=True,text=True)\n    row=dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=target);results.append(row)\n    if ran.returncode:print(json.dumps(row));raise SystemExit(ran.returncode)\nstarted=time.perf_counter();ran=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','m*.py'],cwd=OUT,capture_output=True,text=True)\nsuite=dict(status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr)\nif ran.returncode:print(json.dumps(suite));raise SystemExit(ran.returncode)\nmatch=re.search(r'Ran (\\d+) tests in ([\\d.]+)s',ran.stderr);assert match\nsuite.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)))\nafter=source_map();installed_after=installed_map();assert before==after;assert installed_before==installed_after\nreport=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),py_gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),filesystem_encoding=sys.getfilesystemencoding(),filesystem_errors=sys.getfilesystemencodeerrors(),utf8_mode=sys.flags.utf8_mode,package_path=pyalamode.__file__),results=results,suite=suite,source_before=before,source_after=after,installed_product_before=installed_before,installed_product_after=installed_after,source_unchanged=True,installed_source_equal=True)\n(OUT/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(name=NAME,suite=suite['tests'],focused=[r['stdout'].strip() for r in results],source_files=len(before),installed_product_files=len(installed_before),unchanged=True)))\n",
  "make_writers.py": "import hashlib,json\nfrom pathlib import Path\nout=Path(__file__).parent\nheader='import pyalamode.standard as std\\nfrom pyalamode import fun,text_startswith\\n'\nbody='@fun\\ndef probe(text:str)->bool:\\n    return text_startswith(text,\"a\")\\n'\nwriters=[\n('public direct subscript',\"std.text_replace.__globals__['str']=print\\n\"),\n('public aliased subscript',\"g=std.text_replace.__globals__\\ng['str']=print\\n\"),\n('public direct update',\"std.text_replace.__globals__.update(str=print)\\n\"),\n('public aliased update',\"g=std.text_replace.__globals__\\ng.update(str=print)\\n\"),\n('public direct setitem',\"std.text_replace.__globals__.__setitem__('str',print)\\n\"),\n('public aliased setitem',\"g=std.text_replace.__globals__\\ng.__setitem__('str',print)\\n\"),\n('private direct subscript',\"std._exact.__globals__['str']=print\\n\"),\n('private aliased subscript',\"g=std._exact.__globals__\\ng['str']=print\\n\"),\n('private direct update',\"std._exact.__globals__.update(str=print)\\n\"),\n('private aliased update',\"g=std._exact.__globals__\\ng.update(str=print)\\n\"),\n('public nested builtins subscript',\"std.text_replace.__globals__['__builtins__']['str']=print\\n\"),\n('public nested builtins alias',\"g=std.text_replace.__globals__['__builtins__']\\ng['str']=print\\n\"),\n('private nested builtins update',\"std._exact.__globals__['__builtins__'].update(str=print)\\n\"),\n('private nested builtins alias update',\"g=std._exact.__globals__['__builtins__']\\ng.update(str=print)\\n\"),\n('public dictionary pop',\"std.text_replace.__globals__.pop('str',None)\\n\"),\n('private dictionary clear',\"std._exact.__globals__.clear()\\n\"),\n]\ncases=[dict(id='V'+str(8+i).zfill(2),source=header+writer+body,expected=1,selected=1,note=note+' invalidates shared standard module/native foundation, including a distinct consumer') for i,(note,writer) in enumerate(writers)]\np=out/'writer-cases.json';p.write_text(json.dumps(cases,indent=2)+'\\n');print(json.dumps(dict(cases=len(cases),admits=0,refusals=len(cases),sha256=hashlib.sha256(p.read_bytes()).hexdigest())))\n"
}
```

## Fixed inherited sibling-global writer regression

Root requested four inherited local-function `__globals__` cases before observing the correction. All four require refusal; a checked anchor function supplies the defining module dictionary, while a sibling checked function reads the replaced constant or builtin. This is the inherited known-writer gate, with no catalog expansion. The original 528 outcomes remain fixed. The complete static corpus is now 532 rows: 187 admits and 345 refusals. New literal SHA-256 `d1099a5c22faa49d08b65cb2eaf9d4bdc004cbd664c49d7d0ef83c1f870b53f3`.

```json
[
  {
    "id": "V24",
    "source": "from pyalamode import fun\nBIAS=1\n@fun\ndef anchor(value:int)->int:\n    return value\n@fun\ndef probe(value:int)->int:\n    return value+BIAS\nanchor.__globals__['BIAS']=print\n",
    "expected": 1,
    "selected": 2,
    "note": "sibling constant direct invalidates defining local module and sibling dependency"
  },
  {
    "id": "V25",
    "source": "from pyalamode import fun\nBIAS=1\n@fun\ndef anchor(value:int)->int:\n    return value\n@fun\ndef probe(value:int)->int:\n    return value+BIAS\ng=anchor.__globals__\ng['BIAS']=print\n",
    "expected": 1,
    "selected": 2,
    "note": "sibling constant alias invalidates defining local module and sibling dependency"
  },
  {
    "id": "V26",
    "source": "from pyalamode import fun\nBIAS=1\n@fun\ndef anchor(value:int)->int:\n    return value\n@fun\ndef probe(value:int)->int:\n    return abs(value)\nanchor.__globals__['abs']=print\n",
    "expected": 1,
    "selected": 2,
    "note": "sibling builtin direct invalidates defining local module and sibling dependency"
  },
  {
    "id": "V27",
    "source": "from pyalamode import fun\nBIAS=1\n@fun\ndef anchor(value:int)->int:\n    return value\n@fun\ndef probe(value:str)->int:\n    return len(value)\ng=anchor.__globals__\ng['len']=print\n",
    "expected": 1,
    "selected": 2,
    "note": "sibling builtin alias invalidates defining local module and sibling dependency"
  }
]
```

Final complete executable harness map and changed/new full file contents, fixed before these new observations:

```json
{
  "cli_probe.py": "251cc975f42f3b3c678021fa4cd8afea1e8a1474a00aee8c4495c484518fed0e",
  "environment_probe.py": "2b16da1d5c5bdc1132c00e2a92b4c3c1aca27c5cc49edf5f1c610b750ad99b49",
  "final_probe.py": "9a67f08324f1edd298406f750b7f53be37651a058d7b71a1b68b7bb0925ae369",
  "freshness_probe.py": "1b7155a377fe27d92541996044e26a2cfc5e5780c65397c626d44501292eeb30",
  "m06_cli_probe.py": "be44b9bf2d611fa580c5d88045c373f78ef4671246dff7fab85abc9e5180799a",
  "m06_freshness_probe.py": "e981fdee013e9c2140bbf619004723eec5d3fdf11706753b64552d27dd8e6d39",
  "m06_nonexecution_probe.py": "d8fd3094bf9e6daa5eeefa6bd19f9ef581ddc1b35e858973fc49fa110d509ef4",
  "m06_project_probe.py": "e9dd75392a8198925edf7641dce3a9178abfb132048ac80c1e20a75f4cad854e",
  "m06_runtime_probe.py": "c8eef2d0cb8f4d486cddaa0f7b940b4e5f17b4518541159cb531c559cd989e8b",
  "make_cases.py": "d3de5400f1d0238e4a46e66f2a699920cb4f62afdbba90683569a27f43d6b5c6",
  "make_layouts.py": "bd1e4e48627d32ea034aab2e987b5ebe87cab955587487edbb6bb01e9e61c78e",
  "make_local_writers.py": "57ebee5191e62d22f3efb1c0e809857034d55d9c2f408d65901af9fd5fcf38cc",
  "make_supplement.py": "efc84afdb89e1b5aa35af783dc36d245f0a8d7c622111e2786cbe18e4f5573f6",
  "make_writers.py": "2ea5a876c4f8ac3680ffe0ab272427d10ec26c6e76e4ee8fd932b6a678ac6c52",
  "project_probe.py": "ada8aeb6267f3986e073e8b5ac161e524ee7c6be6e867de01b35e39c2f41e3df",
  "runtime_probe.py": "77516e940c97ef1f7fcf2c1184e26d7c68eeb12c24748557160e8c282c3c9dd7",
  "static_probe.py": "e9caa86870cdfe0aed171e70734ad98ce27a0aacb9e3f458151833450012777b"
}
```

```json
{
  "static_probe.py": "import hashlib,json,sys\nfrom pathlib import Path\nfrom pyalamode.checker import analyze_source\nOUT=Path(__file__).parent\nrows=[]\nfor corpus in ('m06-literal-cases.json','literal-cases.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json','local-writer-cases.json'):\n    cases=json.loads((OUT/corpus).read_text())\n    for original in cases:\n        case=dict(original)\n        if corpus.startswith('m06-'):\n            case['id']='M6-'+case['id']\n            if original['id'] in {'F41','F42'}:\n                case['failures']=sorted(set(case['failures'])|{'UnicodeError'})\n        result=analyze_source(case['source'],path='<m07_'+case['id']+'>')\n        contracts={c.name:c for c in result.contracts}\n        probe=contracts.get(case.get('boundary','probe'))\n        problems=[]\n        if result.status!=case['expected']:problems.append('status')\n        if case.get('selected') is not None and result.selected_functions<case['selected']:problems.append('selection')\n        if not result.status and probe:\n            for key in ('failures','required_effects','effect_bound'):\n                if key in case and sorted(case[key])!=getattr(probe,key):problems.append(key)\n            for key,required in case.get('contains',{}).items():\n                if not set(required)<=set(getattr(probe,key)):problems.append('contains '+key)\n            if case.get('latent'):\n                if probe.required_effects:problems.append('latent effects')\n                if not probe.return_callable_evidence:problems.append('latent evidence')\n        rows.append(dict(id=case['id'],expected=case['expected'],observed=result.status,selected=result.selected_functions,problems=problems,\n                         diagnostics=[d.__dict__ for d in result.diagnostics],contracts={name:c.__dict__ for name,c in contracts.items()}))\nreport=dict(corpus_sha256={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ('m06-literal-cases.json','literal-cases.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json','local-writer-cases.json')},rows=rows,unexpected=[r for r in rows if r['problems']])\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'static-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(cases=len(rows),unexpected=[dict(id=r['id'],problems=r['problems'],expected=r['expected'],observed=r['observed'],diagnostics=[d['reason'] for d in r['diagnostics']]) for r in report['unexpected']])))\nraise SystemExit(bool(report['unexpected']))\n",
  "final_probe.py": "import hashlib,json,platform,re,subprocess,sys,sysconfig,time\nfrom pathlib import Path\nimport pyalamode\nOUT=Path(__file__).parent;ROOT=Path(sys.argv[1]);NAME=sys.argv[2]\ndef digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()\ndef source_map():\n    paths=[ROOT/'pyproject.toml',ROOT/'README.md']\n    for area in ('pyalamode','tests','examples','benchmarks'):paths.extend((ROOT/area).rglob('*.py'))\n    result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths)) if '__pycache__' not in p.parts}\n    for p in sorted(OUT.glob('*.py')):result['reviewer:'+p.name]=digest(p)\n    for p in (OUT/'literal-cases.json',OUT/'m06-literal-cases.json',OUT/'literal-layouts.json',OUT/'supplemental-cases.json',OUT/'narrowing-cases.json',OUT/'writer-cases.json',OUT/'local-writer-cases.json'):result['reviewer:'+p.name]=digest(p)\n    return result\ndef installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}\nbefore=source_map();installed_before=installed_map()\nassert len(installed_before)==15\nassert all(before[k]==v for k,v in installed_before.items())\nresults=[]\nfor script in ('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','freshness_probe.py','m06_runtime_probe.py','m06_project_probe.py','m06_cli_probe.py','m06_nonexecution_probe.py','m06_freshness_probe.py','environment_probe.py'):\n    target=NAME+'-'+script.removesuffix('_probe.py')+'.json'\n    started=time.perf_counter();ran=subprocess.run([sys.executable,str(OUT/script),target],cwd=OUT,capture_output=True,text=True)\n    row=dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=target);results.append(row)\n    if ran.returncode:print(json.dumps(row));raise SystemExit(ran.returncode)\nstarted=time.perf_counter();ran=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','m*.py'],cwd=OUT,capture_output=True,text=True)\nsuite=dict(status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr)\nif ran.returncode:print(json.dumps(suite));raise SystemExit(ran.returncode)\nmatch=re.search(r'Ran (\\d+) tests in ([\\d.]+)s',ran.stderr);assert match\nsuite.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)))\nafter=source_map();installed_after=installed_map();assert before==after;assert installed_before==installed_after\nreport=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),py_gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),filesystem_encoding=sys.getfilesystemencoding(),filesystem_errors=sys.getfilesystemencodeerrors(),utf8_mode=sys.flags.utf8_mode,package_path=pyalamode.__file__),results=results,suite=suite,source_before=before,source_after=after,installed_product_before=installed_before,installed_product_after=installed_after,source_unchanged=True,installed_source_equal=True)\n(OUT/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps(dict(name=NAME,suite=suite['tests'],focused=[r['stdout'].strip() for r in results],source_files=len(before),installed_product_files=len(installed_before),unchanged=True)))\n",
  "make_local_writers.py": "import hashlib,json\nfrom pathlib import Path\nout=Path(__file__).parent\nprefix='from pyalamode import fun\\nBIAS=1\\n@fun\\ndef anchor(value:int)->int:\\n    return value\\n'\ncases=[]\nfor i,(note,writer,body) in enumerate((\n ('sibling constant direct',\"anchor.__globals__['BIAS']=print\\n\",'@fun\\ndef probe(value:int)->int:\\n    return value+BIAS\\n'),\n ('sibling constant alias',\"g=anchor.__globals__\\ng['BIAS']=print\\n\",'@fun\\ndef probe(value:int)->int:\\n    return value+BIAS\\n'),\n ('sibling builtin direct',\"anchor.__globals__['abs']=print\\n\",'@fun\\ndef probe(value:int)->int:\\n    return abs(value)\\n'),\n ('sibling builtin alias',\"g=anchor.__globals__\\ng['len']=print\\n\",'@fun\\ndef probe(value:str)->int:\\n    return len(value)\\n'),\n)):\n cases.append(dict(id='V'+str(24+i),source=prefix+body+writer,expected=1,selected=2,note=note+' invalidates defining local module and sibling dependency'))\np=out/'local-writer-cases.json';p.write_text(json.dumps(cases,indent=2)+'\\n')\nfor name in ('static_probe.py','final_probe.py'):\n p=out/name;s=p.read_text();s=s.replace(\"'writer-cases.json'\", \"'writer-cases.json','local-writer-cases.json'\") if name=='static_probe.py' else s.replace(\"OUT/'writer-cases.json'\", \"OUT/'writer-cases.json',OUT/'local-writer-cases.json'\")\n p.write_text(s)\nmanifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.py'))}\n(out/'harness-freeze-3.json').write_text(json.dumps(manifest,indent=2)+'\\n')\nsha=hashlib.sha256((out/'local-writer-cases.json').read_bytes()).hexdigest()\nwith Path('/Volumes/Projects/pyalamode/Docs/conformance/m07-cases.md').open('a') as f:\n f.write('\\n## Fixed inherited sibling-global writer regression\\n\\nRoot requested four inherited local-function `__globals__` cases before observing the correction. All four require refusal; a checked anchor function supplies the defining module dictionary, while a sibling checked function reads the replaced constant or builtin. This is the inherited known-writer gate, with no catalog expansion. The original 528 outcomes remain fixed. The complete static corpus is now 532 rows: 187 admits and 345 refusals. New literal SHA-256 `'+sha+'`.\\n\\n```json\\n'+(out/'local-writer-cases.json').read_text()+'```\\n\\nFinal complete executable harness map and changed/new full file contents, fixed before these new observations:\\n\\n```json\\n'+json.dumps(manifest,indent=2)+'\\n```\\n\\n```json\\n'+json.dumps({n:(out/n).read_text() for n in ('static_probe.py','final_probe.py','make_local_writers.py')},indent=2)+'\\n```\\n')\nprint(json.dumps(dict(cases=len(cases),sha256=sha,manifest_sha256=hashlib.sha256((out/'harness-freeze-3.json').read_bytes()).hexdigest(),executables=len(manifest))))\n"
}
```

## Observed corrections before final source freeze

The fixed cases found and preserved the following corrections; these are concrete observations, not changes to admit/refuse expectations. The native low-level UTF-8 and inherited text-IO registry counterexamples preceded catalog approval and led to manual conversion. Later actual Linux ASCII startup exposed a valid non-ASCII OS-name route through the changed surrogateescape handler; root narrowed the supported target to UTF-8 filesystem encoding with surrogateescape error mode and required provider setup to refuse other configurations before native access. All surrogate code units in roots, resolved roots, relative paths and environment names now refuse before OS conversion. Native environment values retain documented CPython decoding semantics; isolated invalid-byte controls are checked separately.

A cold refused default expression with unknown capture crashed during full-warm restoration when its unknown type was reparsed; main restored unknown evidence directly, and the fixed 42-layout corpus retains cold/populated/full-warm/partial refusal and a zero execution sentinel. Composition's intermediate stable-data validation can raise RecursionError even when the final return type is scalar; main added recursive intermediate/nested wrapper validation failures at every invocation occurrence. The six additional literal admits retain that failure, with the RuntimeError handler case discharging it according to Python's exception hierarchy. `text_split` has no recursive validation route: its published failure metadata was reconciled to ValueError, while text_join retains validation RecursionError. Partial application's second argument is limited to supported stable data or an exact capability; the fixed Callable-second-argument case refuses.

The first shared-global supplement found four incorrectly admitted nested builtin dictionary writers V18–V21 under checker SHA-256 `1b1318cd0cde0c3f4df22f2348552ccb999b76a2ecf82664d552d1f8be01c002`; the remaining 12 new writer refusals agreed. Before correction, the inherited sibling-global supplement additionally found incorrectly admitted V24–V27. Root independently observed the same propagation gap. Main changed reference identity to the defining module for function globals and propagates that owner through dictionary extraction and nested subscripts, so writers taint the shared defining module. Root's independent interim replay observed all 532 fixed outcomes agree. Final acceptance still requires the frozen-source installed native/Linux runs below.

## Final frozen-source independent results

Root explicitly froze the corrected implementation before these runs. The main freeze packet `/tmp/pyalamode-m07-main-freeze.json` SHA-256 is `6caecbcc6b6d554faf8cac897f8fb2afd44aadf1c89b75089a7a609f154ce6e8`; checker SHA-256 is `2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd`. No fixed expectation was weakened. All 532 rows pass on both platforms: 187 admits and 345 refusals. The complete native/Linux static rows, including contracts and diagnostics, are equal. This is a bounded conformance observation for the published catalog. Root retains the release decision.

| Independent gate | Native result | Fresh installed Linux result | Count interpretation |
| --- | --- | --- | --- |
| Complete inherited/current suite | 286 tests, pass; 6.316 s | 286 tests, pass; 19.003 s | Test methods; suite time is not a workload benchmark |
| Fixed static corpus | 532 exact outcomes, no discrepancy | Same | 187 admits / 345 refusals; all exact M6 sources retained |
| New runtime | 684 assertions plus 33 isolated child checks; zero hooks | Same | One registry/IO/OS-name child; exact types, callbacks, ordering and failures |
| New project/cache/layout | 902 assertions, 190 recorded checks, 42 layouts | Same | In-process API cold/populate/full-warm/partial/build transitions |
| New CLI/artifact | 114 assertions, 58 recorded rows | Same | Actual CLI and stock-Python execution rows |
| New byte/policy freshness | 50 assertions, 14 subprocesses | Same | Copied actual product/source/policy mutations |
| Inherited runtime | 192 assertions, zero hooks | Same | Existing data/domain contracts on M7 bytes |
| Inherited project | 207 assertions, 85 checks, 28 layouts | Same | Approved conditional envelope update explicit above |
| Inherited CLI | 76 assertions, 37 rows, five layouts | Same | Actual inherited commands/artifact gates |
| Inherited nonexecution | 78 assertions, 14 sentinels, 15 layouts | Same | Check/build never execute authored initializer/default/decorator/annotation code |
| Inherited freshness | 42 assertions, 12 subprocesses | Same | Inherited byte identities invalidate appropriately |
| Alternate native startup | Three assertions; remains UTF-8 | Eight assertions; actual ASCII startup refused | One child per platform; Linux tooling status 2/no artifact and both live providers RuntimeError before OS access; zero registry hooks |

Focused assertion totals are 2,381 native and 2,386 Linux including the 33 isolated child checks. Static rows and suite test methods are separate counts. Each final driver starts eleven focused subprocesses and one suite subprocess; recorded project/CLI rows are not interchangeable with subprocess counts. The 42 new layouts and inherited 28 project/five CLI/15 nonexecution layouts are distinct inventories, completely published in the frozen harness.

Native invocation: `.venv/bin/python /tmp/pyalamode-m07-review.ey3fnwr8/final_probe.py /Volumes/Projects/pyalamode native`. Its spelling preserves the editable environment. Frozen pyproject, README and 15 product Python files were copied into `/tmp/pyalamode-m07-review.ey3fnwr8/package-source`. The first `pip wheel --no-index --no-deps --no-build-isolation` attempt reported missing setuptools in the existing editable environment. The existing declared build dependency was then resolved outside the checkout with `.venv/bin/python -m pip wheel --no-deps --wheel-dir /tmp/pyalamode-m07-review.ey3fnwr8/wheels /tmp/pyalamode-m07-review.ey3fnwr8/package-source`; it succeeded without changing any reviewed source. The new wheel is 117,899 bytes, SHA-256 `195b8444a4e24ff1a53e2e9c985fabb80ab73840710c709863dc1a7d5f4d706e`.

Actual Linux invocation: `docker run --rm --network none -v /Volumes/Projects/pyalamode:/workspace:ro -v /tmp/pyalamode-m07-review.ey3fnwr8:/review -w /review -e PYTHONPATH=/review/installed python:3.13.1-slim sh -c 'python -m pip install --no-index --no-deps --target /review/installed /review/wheels/pyalamode-0.1.0-py3-none-any.whl && python /review/final_probe.py /workspace linux'`. The fresh wheel installs before product import. Both full suites use the actual interpreter plus `-m unittest discover -s CHECKOUT_ROOT/tests -p m*.py`. Both are exact CPython 3.13.1 standard GIL with UTF-8 filesystem encoding and surrogateescape errors; native UTF-8 mode is zero, Linux one. This verifies M7 operations on an actual installed product without making an M11 consumer-distribution claim.

Successful off artifacts retain authored source bytes. Exports enforce supported argument/return data checks and leave originals unguarded; debug publishes finite supported data assertions. Neither mode certifies unknown callbacks or capabilities. Rejected check/build creates no artifact and executes no authored code. Optional CLI run remains unsupported (status 2); accepted artifacts execute via stock Python. Provider setup is independently visible and unchecked, with ordinary initialization policy/environment obligations separate from invocation evidence. Handled failures retain effects/trust/dependencies. Callable annotation or marker alone never establishes admission.

Final driver metadata and outputs (maps published once below):

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
      "filesystem_encoding": "utf-8",
      "filesystem_errors": "surrogateescape",
      "utf8_mode": 0,
      "package_path": "/Volumes/Projects/pyalamode/pyalamode/__init__.py"
    },
    "results": [
      {
        "script": "static_probe.py",
        "status": 0,
        "elapsed_seconds": 1.1026315421331674,
        "stdout": "{\"cases\": 532, \"unexpected\": []}\n",
        "stderr": "",
        "output": "native-static.json"
      },
      {
        "script": "runtime_probe.py",
        "status": 0,
        "elapsed_seconds": 0.12648679106496274,
        "stdout": "{\"assertions\": 684, \"hook_calls\": [], \"subprocesses\": 1, \"isolated_assertions\": 33}\n",
        "stderr": "",
        "output": "native-runtime.json"
      },
      {
        "script": "project_probe.py",
        "status": 0,
        "elapsed_seconds": 1.983091042144224,
        "stdout": "{\"assertions\": 902, \"checks\": 190, \"layouts\": 42}\n",
        "stderr": "",
        "output": "native-project.json"
      },
      {
        "script": "cli_probe.py",
        "status": 0,
        "elapsed_seconds": 4.440129332942888,
        "stdout": "{\"assertions\": 114, \"recorded_rows\": 58}\n",
        "stderr": "",
        "output": "native-cli.json"
      },
      {
        "script": "freshness_probe.py",
        "status": 0,
        "elapsed_seconds": 1.2336610001511872,
        "stdout": "{\"assertions\": 50, \"subprocesses\": 14}\n",
        "stderr": "",
        "output": "native-freshness.json"
      },
      {
        "script": "m06_runtime_probe.py",
        "status": 0,
        "elapsed_seconds": 0.04760758299380541,
        "stdout": "{\"assertions\": 192, \"hook_calls\": []}\n",
        "stderr": "",
        "output": "native-m06_runtime.json"
      },
      {
        "script": "m06_project_probe.py",
        "status": 0,
        "elapsed_seconds": 0.877538374857977,
        "stdout": "{\"assertions\": 207, \"layouts\": 28, \"checks\": 85}\n",
        "stderr": "",
        "output": "native-m06_project.json"
      },
      {
        "script": "m06_cli_probe.py",
        "status": 0,
        "elapsed_seconds": 2.856406166916713,
        "stdout": "{\"assertions\": 76, \"commands\": 37, \"layouts\": 5}\n",
        "stderr": "",
        "output": "native-m06_cli.json"
      },
      {
        "script": "m06_nonexecution_probe.py",
        "status": 0,
        "elapsed_seconds": 0.2860673328395933,
        "stdout": "{\"assertions\": 78, \"sentinels\": 14, \"layouts\": 15}\n",
        "stderr": "",
        "output": "native-m06_nonexecution.json"
      },
      {
        "script": "m06_freshness_probe.py",
        "status": 0,
        "elapsed_seconds": 1.1550586668308824,
        "stdout": "{\"assertions\": 42, \"transitions\": 12}\n",
        "stderr": "",
        "output": "native-m06_freshness.json"
      },
      {
        "script": "environment_probe.py",
        "status": 0,
        "elapsed_seconds": 0.11229066597297788,
        "stdout": "{\"assertions\": 3, \"subprocesses\": 1, \"encoding\": \"utf-8\", \"ascii_target_refused\": false, \"handler_hits\": []}\n",
        "stderr": "",
        "output": "native-environment.json"
      }
    ],
    "suite": {
      "status": 0,
      "elapsed_seconds": 6.445055874995887,
      "stdout": "",
      "stderr": "..............................................................................................................................................................................................................................................................................................\n----------------------------------------------------------------------\nRan 286 tests in 6.316s\n\nOK\n",
      "tests": 286,
      "reported_seconds": 6.316
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
      "filesystem_encoding": "utf-8",
      "filesystem_errors": "surrogateescape",
      "utf8_mode": 1,
      "package_path": "/review/installed/pyalamode/__init__.py"
    },
    "results": [
      {
        "script": "static_probe.py",
        "status": 0,
        "elapsed_seconds": 5.476948919000279,
        "stdout": "{\"cases\": 532, \"unexpected\": []}\n",
        "stderr": "",
        "output": "linux-static.json"
      },
      {
        "script": "runtime_probe.py",
        "status": 0,
        "elapsed_seconds": 0.11980774999938149,
        "stdout": "{\"assertions\": 684, \"hook_calls\": [], \"subprocesses\": 1, \"isolated_assertions\": 33}\n",
        "stderr": "",
        "output": "linux-runtime.json"
      },
      {
        "script": "project_probe.py",
        "status": 0,
        "elapsed_seconds": 9.72493817099894,
        "stdout": "{\"assertions\": 902, \"checks\": 190, \"layouts\": 42}\n",
        "stderr": "",
        "output": "linux-project.json"
      },
      {
        "script": "cli_probe.py",
        "status": 0,
        "elapsed_seconds": 5.024606585000583,
        "stdout": "{\"assertions\": 114, \"recorded_rows\": 58}\n",
        "stderr": "",
        "output": "linux-cli.json"
      },
      {
        "script": "freshness_probe.py",
        "status": 0,
        "elapsed_seconds": 0.9669357500006299,
        "stdout": "{\"assertions\": 50, \"subprocesses\": 14}\n",
        "stderr": "",
        "output": "linux-freshness.json"
      },
      {
        "script": "m06_runtime_probe.py",
        "status": 0,
        "elapsed_seconds": 0.0462054170002375,
        "stdout": "{\"assertions\": 192, \"hook_calls\": []}\n",
        "stderr": "",
        "output": "linux-m06_runtime.json"
      },
      {
        "script": "m06_project_probe.py",
        "status": 0,
        "elapsed_seconds": 4.532252917999358,
        "stdout": "{\"assertions\": 207, \"layouts\": 28, \"checks\": 85}\n",
        "stderr": "",
        "output": "linux-m06_project.json"
      },
      {
        "script": "m06_cli_probe.py",
        "status": 0,
        "elapsed_seconds": 3.5860481269992306,
        "stdout": "{\"assertions\": 76, \"commands\": 37, \"layouts\": 5}\n",
        "stderr": "",
        "output": "linux-m06_cli.json"
      },
      {
        "script": "m06_nonexecution_probe.py",
        "status": 0,
        "elapsed_seconds": 0.5853630010005872,
        "stdout": "{\"assertions\": 78, \"sentinels\": 14, \"layouts\": 15}\n",
        "stderr": "",
        "output": "linux-m06_nonexecution.json"
      },
      {
        "script": "m06_freshness_probe.py",
        "status": 0,
        "elapsed_seconds": 0.928137875000175,
        "stdout": "{\"assertions\": 42, \"transitions\": 12}\n",
        "stderr": "",
        "output": "linux-m06_freshness.json"
      },
      {
        "script": "environment_probe.py",
        "status": 0,
        "elapsed_seconds": 0.08833908300039184,
        "stdout": "{\"assertions\": 8, \"subprocesses\": 1, \"encoding\": \"ascii\", \"ascii_target_refused\": true, \"handler_hits\": []}\n",
        "stderr": "",
        "output": "linux-environment.json"
      }
    ],
    "suite": {
      "status": 0,
      "elapsed_seconds": 19.220599759000834,
      "stdout": "",
      "stderr": "..............................................................................................................................................................................................................................................................................................\n----------------------------------------------------------------------\nRan 286 tests in 19.003s\n\nOK\n",
      "tests": 286,
      "reported_seconds": 19.003
    },
    "source_unchanged": true,
    "installed_source_equal": true
  }
}
```

Exact frozen-input and final raw-output digests:

```json
{
  "inputs": {
    "literal-cases.json": "288563ab1d86d55480b70d657cad25f8fe43360cad3aa9ecc24126f331225b88",
    "m06-literal-cases.json": "15cc3949409763e122db23262cf1c7a842821a9145d63286434c0daace4721bd",
    "literal-layouts.json": "07673e4ec850fb1e4b374639df564eb002fdee9e65a5fe027a21e1db3c835ef2",
    "supplemental-cases.json": "cd9032e387ba18e9def9c6d8f5ba8039d2807e0c40991c7b22795f8488144aa2",
    "narrowing-cases.json": "dc7db1d9179338435d2cd5ac8ebc53c2910f367e9509ba2153fcccf028ef3328",
    "writer-cases.json": "88b147ee859e74e5a1e469cc855a7c200dd0db2d75a2498bd3586ba5d1886e2b",
    "local-writer-cases.json": "d1099a5c22faa49d08b65cb2eaf9d4bdc004cbd664c49d7d0ef83c1f870b53f3",
    "harness-freeze.json": "bcfa5f32e7fe87b895141cfba992cc195585ee79effb8af89dfdd551f23813b6",
    "harness-freeze-2.json": "65836639871105283c5099a9dd4065b91814a0e7f26f037808c89274b432b75a",
    "harness-freeze-3.json": "bd974f39699278d77ab0da17e64edc5052bf3dd28a494ba2f0a681ecf6b718ee"
  },
  "outputs": {
    "native-cli.json": "eaf2f327ea02867da9f36032e30d667e35eb2d25edf0465636ea2080d5411243",
    "native-environment.json": "733f671928d8f6081e1fe8020cb91b752d56768d66f231a32917cc21d845c251",
    "native-final.json": "b11da06e15b059bab437fbb828badfc9f56f54f5fd1c8572729a258a96f73d19",
    "native-freshness.json": "ce047a1412a420216a4b136c8287d5537afcceaf65d92c2a6e13a3bf8f1fa333",
    "native-m06_cli.json": "1b62bc0d4e5c61ff50ae2822387ac28307756ad791eca711eccbe46bc6fa766e",
    "native-m06_freshness.json": "43d65ce18949fb53f51a7d7389b247d1d29ed0888b4e7f31f502a369d4437cbe",
    "native-m06_nonexecution.json": "4633b73bab03db1545a6ef61f20898d9feb8dd93ab99bcb12b0416799dddc1bc",
    "native-m06_project.json": "92bf7f65b2a4528191022cce4b9576ad2037d15ad637d6a47845beb038abe467",
    "native-m06_runtime.json": "169ab77e5ed30b06aa211e4a7850f5d40d391d8c888ca60af89dac660b6f66ce",
    "native-project.json": "237e4b0b91c5fdc52134aa454345fbef24965a6c628bb6daa743a6a4d147d951",
    "native-runtime.json": "19786871efd8c627af149e6187e0011fbde121e13dcdea78c6367c014e76004e",
    "native-static.json": "a403a4194a17a29c8423c1c389de1dbcb0fd3e057089d8f191236db502df9914",
    "linux-cli.json": "e407acbb97f78d50d5db5bfbeaabd4422d5b8f800533251087492af69dcc5c5e",
    "linux-environment.json": "f5b358b20942ffb004abdc039ffaf15948a32d619cb5d3033136ac0a3005317f",
    "linux-final.json": "bb1a3df2c45eb06ea64c0d97f4acedc95d580a795c596a04ce397322e7ad92a6",
    "linux-freshness.json": "752dbb77fc201e2fa9d15f1306befbba7c4129b1b5cfcdfcd22ac8c445f3f0c3",
    "linux-m06_cli.json": "7cacca1ca9a38e67b91fe779f4506009628810daef0b13d9fb8393e11f04206e",
    "linux-m06_freshness.json": "08538d05182fd0defd3d4ed5f288350ce70e67d38c9799bab10ea7917baa9dab",
    "linux-m06_nonexecution.json": "0a9e4e5a1e91966ac24bee1c04ecf6622e951e977d9fda98878d136242ffc273",
    "linux-m06_project.json": "b4c8bfdaec8aaabb5ec96c2548097bc546647fdd8d250bfb7c7711e878783cd7",
    "linux-m06_runtime.json": "169ab77e5ed30b06aa211e4a7850f5d40d391d8c888ca60af89dac660b6f66ce",
    "linux-project.json": "61131ffcbbe6a272b68bd3fa98f95a008fb96412476ac9c398fd6109bb0a4905",
    "linux-runtime.json": "19786871efd8c627af149e6187e0011fbde121e13dcdea78c6367c014e76004e",
    "linux-static.json": "a403a4194a17a29c8423c1c389de1dbcb0fd3e057089d8f191236db502df9914",
    "measurement-inspection.json": "af8a0b587077bf42b8cc7a14f66500774bda7fa5b293e4700d8b522142efded4"
  }
}
```

## Complete final source/current/cross/before-after identities

All 92 entries below are identical in native-before, native-after, Linux-before and Linux-after and were rehashed against current checkout/reviewer bytes. Every package/test/fixture/example/benchmark Python file, pyproject and README, all 17 executable reviewer files and seven exact corpus/layout inputs are included. `reviewer:` names resolve in the outside-checkout directory above. Documents/raw outputs are referenced separately to avoid circular self-hashes. Fourteen product foundation identities exclude `__main__.py`; the actual installed inventory includes that launcher as the fifteenth package Python file.

```json
{
  "README.md": "8185b5dda4d698404e9bfd6a58226a2efa84b2f7a64848c134f5bcf6206efcc6",
  "benchmarks/m01_scalar.py": "c84afa054ee636c9a9bdcf001894043b26b81ffd1adb96398c1fae89056a6132",
  "benchmarks/m02_modules.py": "5d28d376907f3aa27810bf04a1d04b000fd26869568826e44b3e65d4765f790c",
  "benchmarks/m03_collections.py": "f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141",
  "benchmarks/m04_boundaries.py": "be56c03b4bd1845baf5cd1e37071e8dce94a0e0430780d45bcf8d4a88b1ffef5",
  "benchmarks/m05_effects.py": "83b54c93ecc4240f340bcc88ba20b16f8a640306d49f784c26662cfe22bb22d3",
  "benchmarks/m06_domains.py": "7a192a8cfed4b29c22d990414d03a49ed6c525c428a2874684368d393d7275af",
  "benchmarks/m07_standard.py": "a5386cbd9e38000b3d00912073429288405a614405b5f50e2ea971218c41ad86",
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
  "examples/standard/core.py": "1ff9c394b8c832cb45f6e34953230539e147942de32edc73d064cf45b6b36992",
  "examples/standard/demo.py": "600bc2cb16d69c4924a1764da58307025da73fe47a55b5a5b536c51c4b0dd444",
  "pyalamode/__init__.py": "477ccce4a90dab58f949e8b1f0dc0ca1c59bc7d257114c520fcb2f7c2a1d8ab2",
  "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
  "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
  "pyalamode/checker.py": "2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd",
  "pyalamode/cli.py": "688d5d299094c50e292efa7dc0729735d45a58f91e3dd4881ef2873a7e2c54f4",
  "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
  "pyalamode/effects.py": "1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d",
  "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
  "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
  "pyalamode/model.py": "269edb7fa4e716ad15634a362cca688f649b253337ed1d59487fc0d18724ab7a",
  "pyalamode/project.py": "d8fc1d3768c67d7408a9fc3d9765ab1b98c643f6c16239496db197e0c4a21be1",
  "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
  "pyalamode/standard.py": "b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9",
  "pyalamode/standard_contracts.py": "cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a",
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
  "tests/m07_runtime.py": "75d1a0ccffbf1f109190596ec881efb8e213643f641caf6fb3b5ec04c4bf5133",
  "tests/m07_standard.py": "b3e2a3cfc3396b30eb0e404ae435daf6737d3eb386e5d4b0bf33de223525f7d2",
  "reviewer:cli_probe.py": "251cc975f42f3b3c678021fa4cd8afea1e8a1474a00aee8c4495c484518fed0e",
  "reviewer:environment_probe.py": "2b16da1d5c5bdc1132c00e2a92b4c3c1aca27c5cc49edf5f1c610b750ad99b49",
  "reviewer:final_probe.py": "9a67f08324f1edd298406f750b7f53be37651a058d7b71a1b68b7bb0925ae369",
  "reviewer:freshness_probe.py": "1b7155a377fe27d92541996044e26a2cfc5e5780c65397c626d44501292eeb30",
  "reviewer:m06_cli_probe.py": "be44b9bf2d611fa580c5d88045c373f78ef4671246dff7fab85abc9e5180799a",
  "reviewer:m06_freshness_probe.py": "e981fdee013e9c2140bbf619004723eec5d3fdf11706753b64552d27dd8e6d39",
  "reviewer:m06_nonexecution_probe.py": "d8fd3094bf9e6daa5eeefa6bd19f9ef581ddc1b35e858973fc49fa110d509ef4",
  "reviewer:m06_project_probe.py": "e9dd75392a8198925edf7641dce3a9178abfb132048ac80c1e20a75f4cad854e",
  "reviewer:m06_runtime_probe.py": "c8eef2d0cb8f4d486cddaa0f7b940b4e5f17b4518541159cb531c559cd989e8b",
  "reviewer:make_cases.py": "d3de5400f1d0238e4a46e66f2a699920cb4f62afdbba90683569a27f43d6b5c6",
  "reviewer:make_layouts.py": "bd1e4e48627d32ea034aab2e987b5ebe87cab955587487edbb6bb01e9e61c78e",
  "reviewer:make_local_writers.py": "57ebee5191e62d22f3efb1c0e809857034d55d9c2f408d65901af9fd5fcf38cc",
  "reviewer:make_supplement.py": "efc84afdb89e1b5aa35af783dc36d245f0a8d7c622111e2786cbe18e4f5573f6",
  "reviewer:make_writers.py": "2ea5a876c4f8ac3680ffe0ab272427d10ec26c6e76e4ee8fd932b6a678ac6c52",
  "reviewer:project_probe.py": "ada8aeb6267f3986e073e8b5ac161e524ee7c6be6e867de01b35e39c2f41e3df",
  "reviewer:runtime_probe.py": "77516e940c97ef1f7fcf2c1184e26d7c68eeb12c24748557160e8c282c3c9dd7",
  "reviewer:static_probe.py": "e9caa86870cdfe0aed171e70734ad98ce27a0aacb9e3f458151833450012777b",
  "reviewer:literal-cases.json": "288563ab1d86d55480b70d657cad25f8fe43360cad3aa9ecc24126f331225b88",
  "reviewer:m06-literal-cases.json": "15cc3949409763e122db23262cf1c7a842821a9145d63286434c0daace4721bd",
  "reviewer:literal-layouts.json": "07673e4ec850fb1e4b374639df564eb002fdee9e65a5fe027a21e1db3c835ef2",
  "reviewer:supplemental-cases.json": "cd9032e387ba18e9def9c6d8f5ba8039d2807e0c40991c7b22795f8488144aa2",
  "reviewer:narrowing-cases.json": "dc7db1d9179338435d2cd5ac8ebc53c2910f367e9509ba2153fcccf028ef3328",
  "reviewer:writer-cases.json": "88b147ee859e74e5a1e469cc855a7c200dd0db2d75a2498bd3586ba5d1886e2b",
  "reviewer:local-writer-cases.json": "d1099a5c22faa49d08b65cb2eaf9d4bdc004cbd664c49d7d0ef83c1f870b53f3"
}
```

Complete actual imported package map, equal in all four before/after/platform observations and equal to current checkout bytes:

```json
{
  "pyalamode/__init__.py": "477ccce4a90dab58f949e8b1f0dc0ca1c59bc7d257114c520fcb2f7c2a1d8ab2",
  "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
  "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
  "pyalamode/checker.py": "2c53c9158e8a693c52e607c832ff21066bb70456a0726863501b006fb13ba2fd",
  "pyalamode/cli.py": "688d5d299094c50e292efa7dc0729735d45a58f91e3dd4881ef2873a7e2c54f4",
  "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
  "pyalamode/effects.py": "1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d",
  "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
  "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
  "pyalamode/model.py": "269edb7fa4e716ad15634a362cca688f649b253337ed1d59487fc0d18724ab7a",
  "pyalamode/project.py": "d8fc1d3768c67d7408a9fc3d9765ab1b98c643f6c16239496db197e0c4a21be1",
  "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
  "pyalamode/standard.py": "b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9",
  "pyalamode/standard_contracts.py": "cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a",
  "pyalamode/variants.py": "02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d"
}
```

Historical pre-M7 initial source map, separate from frozen current identity:

```json
{
  "pyalamode/effects.py": "31d3ee92aaf256fe92f29fa221941d6fac41115fb6c87e4b31503639776a9dfa",
  "pyalamode/variants.py": "02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d",
  "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
  "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
  "pyalamode/__init__.py": "073ee6f161b19df7bcf2dcdf148e45dec7872649f84e85e7d1c9508bc71b6cf6",
  "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
  "pyalamode/model.py": "ea09503e2203feedc26e0efd4b602c3a4887d5e3bae1976e9ff70f56e342c90c",
  "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
  "pyalamode/cli.py": "315af58cde488384815bdb8968393c33eec5b0bc93917237c55dc103726d5ee5",
  "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
  "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
  "pyalamode/checker.py": "f524a5db7c97bd0df889b709b5cc6101576cd10b9f8092fb68dada1aadfcd0f0",
  "pyalamode/project.py": "a9a35d1358fd3f4532222dc2c977ba0da07d7f444a6e1a70079dc8ab704d62d4",
  "tests/m04_records.py": "ff65472a4d5f478ecd745bd55d98e287025bc32c70836615683a5f3a71070e75",
  "tests/m04_runtime.py": "c3544a59356c91ab6bda4d41ffaf79658efa57bd5f74d214ea1ec5caea292c5a",
  "tests/m03_runtime.py": "88db699167977af3934c85c793dc4f674e702f80f28a0dc19bba308ffd31551b",
  "tests/m06_domains.py": "76dd88436fa1efabcd3b30c53e68c8f6e3fd70d811cf5900b08f852965335187",
  "tests/m01_scalar.py": "db119a7c5422292b7f13053f1dd3e7a43d5fb68eb3ec3c885269e548c3c228ce",
  "tests/m02_modules.py": "fdb5f94f7a03d122e82de1c32b7b5b7d4237e0fa0319ac78fe96a9ebce698a4b",
  "tests/m06_runtime.py": "9f035ba5d1969839abd1452ebe38d09a400db3a35536bfb4dcf80d62ac7c59da",
  "tests/m05_runtime.py": "543a0ce687072a8527887bc79e20ef4308797b38cfb7ddf7d0e95056fccd1a21",
  "tests/m03_collections.py": "2ff03b8b771e6539f14ef528eaa245ab5fbf6a51ed60ed9f769dd82db79d403e",
  "tests/m05_effects.py": "09ae107342ed62d29dfa929cc57be0a786d6b23dabec6a29a2b4897b0095d2ff",
  "tests/fixtures/m01/invalid_reassignment.py": "9fd746a84247b3bf809537318a6b5202844eefe1a181cd6d9546bfef8f77f7cf",
  "tests/fixtures/m04/missing_snapshot_precondition.py": "4bf2d9a4fa9355670cbd5934d644fd741c486ec64c400a3e74a0458e9cec3258",
  "tests/fixtures/m04/nested_record_mutable.py": "3a6621d963a0f840fd7448f17f27c3a1fdc62c07342e93945d13d36202115d8a",
  "tests/fixtures/m04/unsupported_getter.py": "0c7bccb953b884150127246521e9902431e3e60aaf4d55e795c84fda750b1e78",
  "tests/fixtures/m03/effectful_callback.py": "c50377aa374a12a3f30d7e4b3855d87d65a30773b3a59059b159b5d46d07950b",
  "tests/fixtures/m03/nested_mutable.py": "2a6d3ad7a043f9e9b504ab334d5e9c2c96d0c520660ec6bf8fe0ab1f62855943",
  "tests/fixtures/m03/ignored_update.py": "61273bf75865d171b57b0e1e36a6a26b03b4ba4493a5ab4f8de1d3160f93eadf",
  "tests/fixtures/m02/changing_capture.py": "371fd5f6c50b65c425056fe6b3e9c1efa7a69acc8f4cf9c5a484790263c21ceb",
  "tests/fixtures/m02/effectful_initializer.py": "32535add5e080ad8e1f3a21338271ceca42a8df81a10d4389d0b5313e5a25965",
  "tests/fixtures/m02/nested_mutable_tuple.py": "262a0801f7a8651137edaa00014ca55367650ece9d7bf948596eca30e266fbc1",
  "tests/fixtures/m05/unknown_operation.py": "faefe7fdeacb00163a72ba0e6241cdc0e313339b1eaf74c789bfc0c33a2a54f7",
  "tests/fixtures/m05/capability_escape.py": "8a7d3cc2af7452df06aa285aef88ecd910a9695c56baa4016be7e0faee849a79",
  "tests/fixtures/m05/undeclared.py": "af86b51c9d7d8fb60db6c7793c5f8a56e749cb73ac3c583550534cbac35ae471",
  "examples/scalar.py": "0507c266d4bff0287693b9a6ec8b7f3db8da265aee6eecbde50ccc855fa90a6a",
  "examples/pricing.py": "e94c9435d25f4f11658a583e4dd287f149717b2d470970d362d2cc09555ea7f0",
  "examples/records/__init__.py": "0def8ab59c34cd9fd81bb1c5ceb3c534209245af8616add6e597215812611d9e",
  "examples/records/core.py": "f13caca1f361bae7a58d7bca0d10e41ceac79f03ba4826a7ed9d70b7fffdfcc2",
  "examples/records/demo.py": "a0e0e6456ad3aa38adaeb8b538886b8ff46965f7026eb34eb10daace76e16f18",
  "examples/domains/domain.py": "3aea9061e61670529e9ceb9bdea477c8af359ab1d96ddf60596f18cd0bc0ac12",
  "examples/domains/demo.py": "130c85d8e2790cd049f0c60adc07a644ef3f63c9a295735ebde4d43ca728474d",
  "examples/modules/constants.py": "74d9245e93fbe88a079e3fc74ca865648475f21edea90696388b4981abdc7813",
  "examples/modules/__init__.py": "76f92b53e625d8faf18131c3c6f2cd841fd35f5b1b61a2dd969e2c99b7ca5936",
  "examples/modules/calculations.py": "aab5a0781bad61a88ece1f3140385cbbf75c3fb4db9bb1c2ecb86eb6ea699eba",
  "examples/modules/demo.py": "8bdd18276448d091ecedb396bedc7d0cbc9ac1e079b7dfc21c1f92c7b145a556",
  "examples/effects/__init__.py": "976d6c1731a16ecf67980cfaddeed34d9f0182df1aeabb5a8e60720709a1f8b6",
  "examples/effects/core.py": "f18f5a58a03e37bb619319121deaf8a59a2ef5fc516142e342a433e23ded174c",
  "examples/effects/demo.py": "9f4d1340e900f8232461e59fcfa720f79b28a13fdc1dc168c7eb24c69dfe40dd",
  "examples/collections/__init__.py": "4bb3c9c16ae4b554d4fa71a406310b1807033b61c7ec2ced586f0616e7eb2418",
  "examples/collections/core.py": "f9b05387462f4ae1009df83fe8d407b07d4767e3d567e307a14ec09185ca61db",
  "examples/collections/demo.py": "039cc3ca4b04c72ecced2276037a4182866a16c18f10c26d0d2cf8389fb2fa98",
  "benchmarks/m04_boundaries.py": "be56c03b4bd1845baf5cd1e37071e8dce94a0e0430780d45bcf8d4a88b1ffef5",
  "benchmarks/m06_domains.py": "7a192a8cfed4b29c22d990414d03a49ed6c525c428a2874684368d393d7275af",
  "benchmarks/m01_scalar.py": "c84afa054ee636c9a9bdcf001894043b26b81ffd1adb96398c1fae89056a6132",
  "benchmarks/m02_modules.py": "5d28d376907f3aa27810bf04a1d04b000fd26869568826e44b3e65d4765f790c",
  "benchmarks/m03_collections.py": "f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141",
  "benchmarks/m05_effects.py": "83b54c93ecc4240f340bcc88ba20b16f8a640306d49f784c26662cfe22bb22d3"
}
```

## Complete observed fixed outcomes

Every exact expected status and both observed statuses appear below. Admitted contracts retain observed types, failures/effects, trust, captures, target/dependency evidence, latent wrappers and handlers; refused rows retain diagnostics. All discrepancy lists are empty. The hashed full raw contract reports retain further operation-catalog and occurrence-edge fields. Every literal source appears in the complete corpus sections above.

```json
[
  {
    "id": "M6-N01",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "a completing path falls through with None instead of the declared result"
      },
      {
        "rule": "PAL110",
        "reason": "Raise is outside the scalar statement vocabulary"
      }
    ]
  },
  {
    "id": "M6-N02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-N03",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-N04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `repr` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-N05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `str` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-N06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-N07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "a completing path falls through with None instead of the declared result"
      },
      {
        "rule": "PAL320",
        "reason": "only with borrow(exact local capability) as fresh_name has a characterized context lifetime"
      }
    ]
  },
  {
    "id": "M6-N08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown_operation` is not a statically established stable dependency"
      },
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-N09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "handler can reinitialize partially completed try bindings: value"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "`error` is not initialized on every continuing path"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL201",
        "reason": "indexing requires an admitted exact Vector/map/tuple contract"
      }
    ]
  },
  {
    "id": "M6-N10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 3,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL201",
        "reason": "indexing requires an admitted exact Vector/map/tuple contract"
      },
      {
        "rule": "PAL240",
        "reason": "captured binding `error` is not established as stable and initialized"
      }
    ]
  },
  {
    "id": "M6-V01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Variant['<m07_M6-V01>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Variant['<m07_M6-V02>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Variant['<m07_M6-V03>:Lookup']",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Case['<m07_M6-V04>:Lookup:Found']"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.field"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V05>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      }
    ]
  },
  {
    "id": "M6-V06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V06>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "M6-V07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V07>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      }
    ]
  },
  {
    "id": "M6-V08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V08>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case construction requires its exact fixed field signature"
      }
    ]
  },
  {
    "id": "M6-V09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V09>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case constructor has an unknown or duplicate field"
      }
    ]
  },
  {
    "id": "M6-V10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V10>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case constructor has an unknown or duplicate field"
      }
    ]
  },
  {
    "id": "M6-V11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V11>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case construction requires its exact fixed field signature"
      }
    ]
  },
  {
    "id": "M6-V12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V12>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "M6-V13",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Variant['<m07_M6-V13>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct",
          "Vector.of"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V14",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Variant['<m07_M6-V14>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct",
          "Vector.of"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V15",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Variant['<m07_M6-V15>:Lookup']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      },
      {
        "rule": "PAL221",
        "reason": "collection elements must establish one recursively admitted exact data schema; empty of requires explicit type arguments"
      }
    ]
  },
  {
    "id": "M6-V16",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V17",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V18",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL310",
        "reason": "capability parameter `clock` requires declared Clock"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V19",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Variant['<m07_M6-V19>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V20",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Variant['<m07_M6-V20>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V21",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Variant['<m07_M6-V21>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V22",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL221",
        "reason": "case default does not establish its exact field schema"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V23",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "domains require only @variant, nested fixed @case declarations and no bases/metaclass/generic behavior"
      }
    ]
  },
  {
    "id": "M6-V24",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "cases require only @case, fixed typed data fields, no class behavior"
      }
    ]
  },
  {
    "id": "M6-V25",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "case payloads require public typed data fields and stable trailing defaults"
      }
    ]
  },
  {
    "id": "M6-V26",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "case payloads require public typed data fields and stable trailing defaults"
      }
    ]
  },
  {
    "id": "M6-V27",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "cases require only @case, fixed typed data fields, no class behavior"
      }
    ]
  },
  {
    "id": "M6-V28",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "domains require only @variant, nested fixed @case declarations and no bases/metaclass/generic behavior"
      }
    ]
  },
  {
    "id": "M6-V29",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "domain case name has another declaration"
      }
    ]
  },
  {
    "id": "M6-V30",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "a closed domain must declare at least one case"
      },
      {
        "rule": "PAL120",
        "reason": "a closed domain contains only public nested @case declarations"
      }
    ]
  },
  {
    "id": "M6-V31",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "case payloads require public typed data fields and stable trailing defaults"
      }
    ]
  },
  {
    "id": "M6-V32",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "domains require only @variant, nested fixed @case declarations and no bases/metaclass/generic behavior"
      }
    ]
  },
  {
    "id": "M6-V33",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "case payloads require public typed data fields and stable trailing defaults"
      }
    ]
  },
  {
    "id": "M6-V34",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "domain namespace or case behavior has an analyzed replacement"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V35",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "case behavior has an analyzed replacement"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V36",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "case behavior has an analyzed replacement"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V37",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "case behavior has an analyzed replacement"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V38",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "domain namespace or case behavior has an analyzed replacement"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V39",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "case behavior has an analyzed replacement"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      },
      {
        "rule": "PAL240",
        "reason": "binding `Lookup` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-V40",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Variant['<m07_M6-V40>:Outer']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V41",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Variant['<m07_M6-V41>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode records-v1: exact fixed fields, deep schema validation and type-sensitive value equivalence",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Record.construct",
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-V42",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `id` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-O01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Option[int]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Some.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Option[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Nothing.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Vector[int]"
        },
        "returns": "Option[Vector[int]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Some.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Result[int, str]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Ok.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O05",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "e": "str"
        },
        "returns": "Result[int, str]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Err.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found Some[bool]"
      }
    ]
  },
  {
    "id": "M6-O07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[int, str]; found Ok[str]"
      }
    ]
  },
  {
    "id": "M6-O08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[int, str]; found Err[int]"
      }
    ]
  },
  {
    "id": "M6-O09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      }
    ]
  },
  {
    "id": "M6-O10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case construction requires its exact fixed field signature"
      }
    ]
  },
  {
    "id": "M6-O11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case construction requires its exact fixed field signature"
      }
    ]
  },
  {
    "id": "M6-O12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case constructor has an unknown or duplicate field"
      }
    ]
  },
  {
    "id": "M6-O13",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "indexing requires an admitted exact Vector/map/tuple contract"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "M6-O14",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[int, str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "indexing requires an admitted exact Vector/map/tuple contract"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "M6-O15",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Option[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "M6-O16",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-O17",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-O18",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-O19",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "a": "Option[int]",
          "b": "Option[int]"
        },
        "returns": "bool",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Option.equivalent"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O20",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "a": "Result[int, str]",
          "b": "Result[int, str]"
        },
        "returns": "bool",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Result.equivalent"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O21",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL210",
        "reason": "collection/tuple equality requires the same recursively exact data schema; arbitrary ordering is excluded"
      }
    ]
  },
  {
    "id": "M6-O22",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "a": "Result[int, str]",
          "b": "Result[str, str]"
        },
        "returns": "Result[tuple[int, str], Vector[str]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Result.accumulate"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O23",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires two established Result[T,E] schemas with identical E; annotate checked inputs or bindings"
      }
    ]
  },
  {
    "id": "M6-O24",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires two established Result[T,E] schemas with identical E; annotate checked inputs or bindings"
      }
    ]
  },
  {
    "id": "M6-O25",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires two established Result[T,E] schemas with identical E; annotate checked inputs or bindings"
      }
    ]
  },
  {
    "id": "M6-O26",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires exactly two Result values with the same exact error schema"
      }
    ]
  },
  {
    "id": "M6-O27",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires exactly two Result values with the same exact error schema"
      }
    ]
  },
  {
    "id": "M6-O28",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires exactly two Result values with the same exact error schema"
      }
    ]
  },
  {
    "id": "M6-O29",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires two established Result[T,E] schemas with identical E; annotate checked inputs or bindings"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-O30",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Option[Option[int]]"
        },
        "returns": "Option[Option[int]]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O31",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Result[Option[int], Vector[str]]"
        },
        "returns": "Result[Option[int], Vector[str]]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-O32",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      }
    ]
  },
  {
    "id": "M6-P01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P01>:Lookup']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P02>:Lookup:Missing']"
      }
    ]
  },
  {
    "id": "M6-P03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P03>:Lookup']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P04>:Lookup']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P05>:Lookup:Found']"
      }
    ]
  },
  {
    "id": "M6-P06",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P06>:Lookup']",
          "flag": "bool"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P07",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P07>:Lookup']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P08>:Lookup:Found']"
      }
    ]
  },
  {
    "id": "M6-P09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "failed partial/guarded patterns cannot establish fresh capture initialization"
      }
    ]
  },
  {
    "id": "M6-P10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "pattern capture `number` overwrites an initialized binding"
      }
    ]
  },
  {
    "id": "M6-P11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "pattern capture `number` overwrites an initialized binding"
      }
    ]
  },
  {
    "id": "M6-P12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P12>:Lookup:Found']"
      }
    ]
  },
  {
    "id": "M6-P13",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P13>:Lookup']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P14",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "`selected` is not initialized on every continuing path"
      }
    ]
  },
  {
    "id": "M6-P15",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P15>:Lookup']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P16",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "`number` is not initialized on every continuing path"
      }
    ]
  },
  {
    "id": "M6-P17",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "failed partial/guarded patterns cannot establish fresh capture initialization"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P18",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "class pattern contains an unknown or duplicate payload field"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P19",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "class pattern contains an unknown or duplicate payload field"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P20",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "class pattern exceeds its fixed payload signature"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P21",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "class pattern requires a resolved unchanged exact product case/record compatible with the subject"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P22",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P22>:Lookup:Found'], Case['<m07_M6-P22>:Lookup:Missing']"
      },
      {
        "rule": "PAL330",
        "reason": "pattern has no characterized finite dispatch/binding contract"
      }
    ]
  },
  {
    "id": "M6-P23",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "pattern has no characterized finite dispatch/binding contract"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P24",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "pattern has no characterized finite dispatch/binding contract"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-P25",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL210",
        "reason": "pattern guard requires exact bool"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown_guard` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-P26",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Option[int]"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P27",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Nothing"
      }
    ]
  },
  {
    "id": "M6-P28",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Result[int, str]"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P29",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Err"
      }
    ]
  },
  {
    "id": "M6-P30",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "bool"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P31",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: False"
      }
    ]
  },
  {
    "id": "M6-P32",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: False, True"
      },
      {
        "rule": "PAL330",
        "reason": "literal pattern requires an exact same-type scalar payload"
      },
      {
        "rule": "PAL330",
        "reason": "literal pattern requires an exact same-type scalar payload"
      }
    ]
  },
  {
    "id": "M6-P33",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "None"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P34",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "a completing path falls through with None instead of the declared result"
      },
      {
        "rule": "PAL330",
        "reason": "match requires one established closed domain/case, exact record, bool or None schema"
      }
    ]
  },
  {
    "id": "M6-P35",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Record['<m07_M6-P35>:Payload']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode records-v1: exact fixed fields, deep schema validation and type-sensitive value equivalence",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P36",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Record['<m07_M6-P36>:Payload']"
      }
    ]
  },
  {
    "id": "M6-P37",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "failed partial/guarded patterns cannot establish fresh capture initialization"
      }
    ]
  },
  {
    "id": "M6-P38",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "a pattern capture name appears twice"
      }
    ]
  },
  {
    "id": "M6-P39",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P39>:Pair']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-P40",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P40>:Lookup:Found'], Case['<m07_M6-P40>:Lookup:Missing']"
      },
      {
        "rule": "PAL330",
        "reason": "class pattern requires a resolved unchanged exact product case/record compatible with the subject"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `number` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL330",
        "reason": "class pattern requires a resolved unchanged exact product case/record compatible with the subject"
      }
    ]
  },
  {
    "id": "M6-P41",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "pattern has no characterized finite dispatch/binding contract"
      },
      {
        "rule": "PAL330",
        "reason": "root named capture is outside explicit finite dispatch; use class patterns or explicit _"
      }
    ]
  },
  {
    "id": "M6-P42",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P42>:Outer:Value']"
      },
      {
        "rule": "PAL330",
        "reason": "failed partial/guarded patterns cannot establish fresh capture initialization"
      }
    ]
  },
  {
    "id": "M6-P43",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "failed partial/guarded patterns cannot establish fresh capture initialization"
      }
    ]
  },
  {
    "id": "M6-P44",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL330",
        "reason": "match is not exhaustive; missing full case coverage: Case['<m07_M6-P44>:Outer:Value']"
      }
    ]
  },
  {
    "id": "M6-P45",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Variant['<m07_M6-P45>:Outer']"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Pattern.dispatch"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-F01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "IndexError"
            ],
            "discharged": [
              "IndexError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ValueError"
            ],
            "discharged": [
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F07",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Result[int, Record['pyalamode:Failure']]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode records-v1: exact fixed fields, deep schema validation and type-sensitive value equivalence",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Err.construct",
          "Failure.convert",
          "Ok.construct"
        ],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": "caught",
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F08",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "str",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Failure.convert",
          "Failure.field"
        ],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ValueError"
            ],
            "discharged": [
              "UnicodeError",
              "ValueError"
            ],
            "target": "caught",
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F09",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "str",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Failure.convert",
          "Failure.field"
        ],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ValueError"
            ],
            "discharged": [
              "UnicodeError",
              "ValueError"
            ],
            "target": "caught",
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL110",
        "reason": "TryStar is outside the scalar statement vocabulary"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `result` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-F12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "a completing path falls through with None instead of the declared result"
      },
      {
        "rule": "PAL340",
        "reason": "checked try supports known category handlers, without else/finally or arbitrary cleanup"
      }
    ]
  },
  {
    "id": "M6-F13",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "a completing path falls through with None instead of the declared result"
      },
      {
        "rule": "PAL340",
        "reason": "checked try supports known category handlers, without else/finally or arbitrary cleanup"
      }
    ]
  },
  {
    "id": "M6-F14",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories overlap in the characterized builtin hierarchy"
      }
    ]
  },
  {
    "id": "M6-F15",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories overlap in the characterized builtin hierarchy"
      }
    ]
  },
  {
    "id": "M6-F16",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories overlap in the characterized builtin hierarchy"
      }
    ]
  },
  {
    "id": "M6-F17",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ZeroDivisionError",
              "IndexError"
            ],
            "discharged": [
              "IndexError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F18",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "exception cleanup target must be fresh and cannot overwrite a stable binding"
      }
    ]
  },
  {
    "id": "M6-F19",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "handler can reinitialize partially completed try bindings: value"
      }
    ]
  },
  {
    "id": "M6-F20",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "local `value` is not initialized or shadows an approved operation"
      }
    ]
  },
  {
    "id": "M6-F21",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "`caught` is not initialized on every continuing path"
      }
    ]
  },
  {
    "id": "M6-F22",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "opaque exception cleanup targets cannot be initialized or aliased as stable bindings"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL102",
        "reason": "`caught` is not initialized on every continuing path"
      }
    ]
  },
  {
    "id": "M6-F23",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F24",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F25",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F26",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F27",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `str` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-F28",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `repr` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-F29",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "tuple contents must be recursively admitted immutable data; capabilities/callables/modules are not tuple data"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F30",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F31",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "failure_value requires one direct live opaque handler exception token"
      }
    ]
  },
  {
    "id": "M6-F32",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `getattr` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-F33",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      },
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "failure_value requires one direct live opaque handler exception token"
      }
    ]
  },
  {
    "id": "M6-F34",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Callable[[], Record['pyalamode:Failure']]; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      },
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "failure_value requires one direct live opaque handler exception token"
      }
    ]
  },
  {
    "id": "M6-F35",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "failure_value requires one direct live opaque handler exception token"
      }
    ]
  },
  {
    "id": "M6-F36",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "failure_value requires one direct live opaque handler exception token"
      }
    ]
  },
  {
    "id": "M6-F37",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Record['pyalamode:Failure']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode records-v1: exact fixed fields, deep schema validation and type-sensitive value equivalence",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Failure.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-F38",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `category` requires its exact recursively admitted immutable data schema"
      }
    ]
  },
  {
    "id": "M6-F39",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F40",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          },
          {
            "line": 10,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F41",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "op": "Callable[[int], int]",
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "KeyError",
          "RecursionError",
          "UnicodeError",
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F42",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "op": "Callable[[int], int]",
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "KeyError",
          "UnicodeError",
          "ValueError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "RuntimeError"
            ],
            "discharged": [
              "RecursionError",
              "RuntimeError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F43",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "op": "Callable[[int], int]",
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "KeyError",
          "RecursionError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 7,
            "categories": [
              "ValueError"
            ],
            "discharged": [
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F44",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "divide": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F44>::divide"
        ],
        "callable_dependencies": [
          "<m07_M6-F44>::divide"
        ],
        "operations": [],
        "handlers": [
          {
            "line": 10,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F45",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "divide": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F45>::divide"
        ],
        "callable_dependencies": [
          "<m07_M6-F45>::divide"
        ],
        "operations": [],
        "handlers": [
          {
            "line": 11,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F46",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "divide": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F46>::divide"
        ],
        "callable_dependencies": [
          "<m07_M6-F46>::divide"
        ],
        "operations": [],
        "handlers": [
          {
            "line": 10,
            "categories": [
              "IndexError"
            ],
            "discharged": [
              "IndexError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F47",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "divide": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F47>::divide"
        ],
        "callable_dependencies": [
          "<m07_M6-F47>::divide"
        ],
        "operations": [],
        "handlers": [
          {
            "line": 10,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F48",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "divide": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F48>::divide"
        ],
        "callable_dependencies": [
          "<m07_M6-F48>::divide"
        ],
        "operations": [],
        "handlers": [
          {
            "line": 10,
            "categories": [
              "ZeroDivisionError",
              "RuntimeError"
            ],
            "discharged": [
              "RecursionError",
              "RuntimeError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F49",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "ClockCapability",
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "IndexError",
              "RuntimeError",
              "OSError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "IndexError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F49u",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Clock"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Clock"
      }
    ]
  },
  {
    "id": "M6-F50",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "StateCapability",
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "State"
        ],
        "effect_bound": [
          "State"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "StateCapability.set"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "RuntimeError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "RecursionError",
              "RuntimeError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F50u",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared State"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared State"
      }
    ]
  },
  {
    "id": "M6-F51",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "IOCapability",
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [
          "IO"
        ],
        "effect_bound": [
          "IO"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "IOCapability.read_text"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "OSError",
              "UnicodeError",
              "RuntimeError",
              "KeyError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "KeyError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "UnicodeError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F51u",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared IO"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared IO"
      }
    ]
  },
  {
    "id": "M6-F52",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "RandomCapability",
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "Random"
        ],
        "effect_bound": [
          "Random"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "RandomCapability.below"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "ValueError",
              "RuntimeError",
              "OSError",
              "IndexError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "IndexError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "UnicodeError",
              "ValueError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F52u",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Random"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Random"
      }
    ]
  },
  {
    "id": "M6-F53",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "EnvironmentCapability",
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "Environment"
        ],
        "effect_bound": [
          "Environment"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "EnvironmentCapability.get"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "ValueError",
              "RuntimeError",
              "OSError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "OSError",
              "RecursionError",
              "RuntimeError",
              "UnicodeError",
              "ValueError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F53u",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Environment"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Environment"
      }
    ]
  },
  {
    "id": "M6-F54",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F55",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F56",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported"
      }
    ]
  },
  {
    "id": "M6-F57",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F58",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "ClockCapability",
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns",
          "borrow.enter_exit"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "RuntimeError",
              "OSError",
              "IndexError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "IndexError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F59",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL340",
        "reason": "opaque exception cleanup targets cannot be initialized or aliased as stable bindings"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL340",
        "reason": "actual handler exceptions are opaque; only direct failure_value conversion is admitted"
      }
    ]
  },
  {
    "id": "M6-F60",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Record['pyalamode:Failure']; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "failure_value requires one direct live opaque handler exception token"
      }
    ]
  },
  {
    "id": "M6-H01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "op": "Callable[[int], Result[int, str]]",
          "x": "int"
        },
        "returns": "Result[tuple[int, int], Vector[str]]",
        "failures": [
          "IndexError",
          "KeyError",
          "RecursionError",
          "UnicodeError",
          "ValueError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Result.accumulate"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-H02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      },
      {
        "rule": "PAL211",
        "reason": "return requires Result[tuple[int, int], Vector[str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "accumulate requires two established Result[T,E] schemas with identical E; annotate checked inputs or bindings"
      }
    ]
  },
  {
    "id": "M6-H03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "validate": {
        "parameters": {
          "x": "int"
        },
        "returns": "Result[int, str]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Err.construct",
          "Ok.construct"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "Result[tuple[int, int], Vector[str]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-H03>::validate"
        ],
        "callable_dependencies": [
          "<m07_M6-H03>::validate"
        ],
        "operations": [
          "Err.construct",
          "Ok.construct",
          "Result.accumulate"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-H04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "validate": {
        "parameters": {
          "cap": "ClockCapability",
          "x": "int"
        },
        "returns": "Result[int, str]",
        "failures": [
          "IndexError",
          "OSError",
          "RecursionError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns",
          "Ok.construct"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "cap": "ClockCapability",
          "x": "int"
        },
        "returns": "Result[tuple[int, int], Vector[str]]",
        "failures": [
          "IndexError",
          "OSError",
          "RecursionError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-H04>::validate"
        ],
        "callable_dependencies": [
          "<m07_M6-H04>::validate"
        ],
        "operations": [
          "ClockCapability.now_ns",
          "Ok.construct",
          "Result.accumulate"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-H05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Clock"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Clock"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Clock"
      }
    ]
  },
  {
    "id": "M6-H06",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "validate": {
        "parameters": {
          "x": "int"
        },
        "returns": "Result[int, str]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Err.construct",
          "Ok.construct"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "Vector[Result[int, str]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-H06>::validate"
        ],
        "callable_dependencies": [
          "<m07_M6-H06>::validate"
        ],
        "operations": [
          "Err.construct",
          "Ok.construct",
          "Vector.map"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-H07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[Result[int, str]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "Vector.map requires a checked bounded fixed callback with admitted result"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "M6-F61",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "dual": {
        "parameters": {
          "values": "Vector[int]",
          "index": "int",
          "denominator": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.index"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]",
          "index": "int",
          "denominator": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F61>::dual"
        ],
        "callable_dependencies": [
          "<m07_M6-F61>::dual"
        ],
        "operations": [
          "Vector.index"
        ],
        "handlers": [
          {
            "line": 10,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          },
          {
            "line": 14,
            "categories": [
              "IndexError"
            ],
            "discharged": [
              "IndexError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F62",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "dual": {
        "parameters": {
          "values": "Vector[int]",
          "index": "int",
          "denominator": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.index"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]",
          "index": "int",
          "denominator": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F62>::dual"
        ],
        "callable_dependencies": [
          "<m07_M6-F62>::dual"
        ],
        "operations": [
          "Vector.index"
        ],
        "handlers": [
          {
            "line": 11,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          },
          {
            "line": 13,
            "categories": [
              "IndexError"
            ],
            "discharged": [
              "IndexError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F63",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "dual": {
        "parameters": {
          "values": "Vector[int]",
          "index": "int",
          "denominator": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.index"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]",
          "index": "int",
          "denominator": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_M6-F63>::dual"
        ],
        "callable_dependencies": [
          "<m07_M6-F63>::dual"
        ],
        "operations": [
          "Vector.index"
        ],
        "handlers": [
          {
            "line": 10,
            "categories": [
              "IndexError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "IndexError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "M6-F64",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL101",
        "reason": "exception target can overwrite a partially initialized try binding"
      }
    ]
  },
  {
    "id": "M6-D01",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D03",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D09",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "x": "Record['<m07_M6-D09>:Payload']"
        },
        "returns": "Variant['<m07_M6-D09>:Lookup']",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode records-v1: exact fixed fields, deep schema validation and type-sensitive value equivalence",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Variant.construct"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "M6-D10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "nested case decorator is shadowed by an earlier outer class binding"
      }
    ]
  },
  {
    "id": "M6-D11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL221",
        "reason": "record default `int` does not establish None"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL221",
        "reason": "record default `value` does not establish None"
      }
    ]
  },
  {
    "id": "M6-D12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL221",
        "reason": "case default does not establish its exact field schema"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL221",
        "reason": "case default does not establish its exact field schema"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D13",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 0,
    "problems": [],
    "contracts": {}
  },
  {
    "id": "M6-D14",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 0,
    "problems": [],
    "contracts": {}
  },
  {
    "id": "M6-D15",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL221",
        "reason": "record default `int` does not establish None"
      }
    ]
  },
  {
    "id": "M6-D16",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL221",
        "reason": "case default does not establish its exact field schema"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      }
    ]
  },
  {
    "id": "M6-D17",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL221",
        "reason": "record default `value` does not establish int"
      }
    ]
  },
  {
    "id": "M6-D18",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL221",
        "reason": "case default does not establish its exact field schema"
      }
    ]
  },
  {
    "id": "M6-D19",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 0,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL221",
        "reason": "record default `value` does not establish int"
      }
    ]
  },
  {
    "id": "M6-D20",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 0,
    "problems": [],
    "contracts": {}
  },
  {
    "id": "M6-D21",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 0,
    "problems": [],
    "contracts": {}
  },
  {
    "id": "M6-D22",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 0,
    "problems": [],
    "contracts": {}
  },
  {
    "id": "M6-W01",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W03",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "M6-W09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL130",
        "reason": "case fields require previously available recursively admitted data"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL130",
        "reason": "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars"
      },
      {
        "rule": "PAL211",
        "reason": "return requires None; found unknown/unsupported value"
      }
    ]
  },
  {
    "id": "S01a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "separator": "str"
        },
        "returns": "Vector[str]",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_split"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S01b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "separator": "str"
        },
        "returns": "Vector[str]",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_split"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S01c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "separator": "str"
        },
        "returns": "Vector[str]",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_split"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S01d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "separator": "str"
        },
        "returns": "Vector[str]",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_split"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S01e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "Vector[str]"
        },
        "returns": "Vector[str]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_split"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S01f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "Vector[str]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_split"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S01g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_split requires exact ('str', 'str')"
      }
    ]
  },
  {
    "id": "S01h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_split requires exact ('str', 'str')"
      }
    ]
  },
  {
    "id": "S01i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S01j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S01k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_split requires exact ('str', 'str')"
      }
    ]
  },
  {
    "id": "S01l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_split` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S01m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_split` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S01n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S02a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "parts": "Vector[str]",
          "separator": "str"
        },
        "returns": "str",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_join"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S02b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "parts": "Vector[str]",
          "separator": "str"
        },
        "returns": "str",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_join"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S02c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "parts": "Vector[str]",
          "separator": "str"
        },
        "returns": "str",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_join"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S02d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "parts": "Vector[str]",
          "separator": "str"
        },
        "returns": "str",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_join"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S02e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of",
          "standard.text_join"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S02f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of",
          "standard.text_join"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S02g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_join requires exact ('Vector[str]', 'str')"
      }
    ]
  },
  {
    "id": "S02h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_join requires exact ('Vector[str]', 'str')"
      }
    ]
  },
  {
    "id": "S02i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S02j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S02k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_join requires exact ('Vector[str]', 'str')"
      }
    ]
  },
  {
    "id": "S02l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_join` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S02m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_join` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S03a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "old": "str",
          "new": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_replace"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S03b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "old": "str",
          "new": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_replace"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S03c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "old": "str",
          "new": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_replace"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S03d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "old": "str",
          "new": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_replace"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S03e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_replace"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S03f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_replace"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S03g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_replace requires exact ('str', 'str', 'str')"
      }
    ]
  },
  {
    "id": "S03h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_replace requires exact ('str', 'str', 'str')"
      }
    ]
  },
  {
    "id": "S03i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S03j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S03k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_replace requires exact ('str', 'str', 'str')"
      }
    ]
  },
  {
    "id": "S03l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_replace` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S03m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_replace` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S03n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S04a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "prefix": "str"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_startswith"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S04b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "prefix": "str"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_startswith"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S04c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "prefix": "str"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_startswith"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S04d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "prefix": "str"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_startswith"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S04e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "bool"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_startswith"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S04f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_startswith"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S04g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_startswith requires exact ('str', 'str')"
      }
    ]
  },
  {
    "id": "S04h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_startswith requires exact ('str', 'str')"
      }
    ]
  },
  {
    "id": "S04i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S04j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S04k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_startswith requires exact ('str', 'str')"
      }
    ]
  },
  {
    "id": "S04l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S04m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S04n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S05a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "start": "int",
          "stop": "int"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_slice"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S05b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "start": "int",
          "stop": "int"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_slice"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S05c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "start": "int",
          "stop": "int"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_slice"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S05d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str",
          "start": "int",
          "stop": "int"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_slice"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S05e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_slice"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S05f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.text_slice"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S05g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_slice requires exact ('str', 'int', 'int')"
      }
    ]
  },
  {
    "id": "S05h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_slice requires exact ('str', 'int', 'int')"
      }
    ]
  },
  {
    "id": "S05i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S05j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S05k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "text_slice requires exact ('str', 'int', 'int')"
      }
    ]
  },
  {
    "id": "S05l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_slice` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S05m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_slice` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S05n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S06a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int",
          "lower": "int",
          "upper": "int"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_clamp"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S06b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int",
          "lower": "int",
          "upper": "int"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_clamp"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S06c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int",
          "lower": "int",
          "upper": "int"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_clamp"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S06d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int",
          "lower": "int",
          "upper": "int"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_clamp"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S06e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_clamp"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S06f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_clamp"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S06g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_clamp requires exact ('int', 'int', 'int')"
      }
    ]
  },
  {
    "id": "S06h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_clamp requires exact ('int', 'int', 'int')"
      }
    ]
  },
  {
    "id": "S06i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S06j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S06k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_clamp requires exact ('int', 'int', 'int')"
      }
    ]
  },
  {
    "id": "S06l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `integer_clamp` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S06m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `integer_clamp` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S06n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `value` of `probe` requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S07a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_parse_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S07b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_parse_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S07c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_parse_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S07d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "int",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_parse_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S07e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_parse_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S07f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_parse_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S07g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_parse_decimal requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S07h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_parse_decimal requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S07i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S07j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S07k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_parse_decimal requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S07l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `integer_parse_decimal` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S07m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `integer_parse_decimal` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S07n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S08a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int"
        },
        "returns": "str",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_format_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S08b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int"
        },
        "returns": "str",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_format_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S08c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int"
        },
        "returns": "str",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_format_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S08d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "int"
        },
        "returns": "str",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_format_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S08e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_format_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S08f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.integer_format_decimal"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S08g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_format_decimal requires exact ('int',)"
      }
    ]
  },
  {
    "id": "S08h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_format_decimal requires exact ('int',)"
      }
    ]
  },
  {
    "id": "S08i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S08j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S08k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "integer_format_decimal requires exact ('int',)"
      }
    ]
  },
  {
    "id": "S08l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `integer_format_decimal` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S08m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `integer_format_decimal` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S08n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `value` of `probe` requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S09a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S09b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S09c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S09d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S09e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "bytes"
        },
        "returns": "bytes",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S09f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "bytes",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S09g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "utf8_encode requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S09h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "utf8_encode requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S09i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S09j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S09k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "utf8_encode requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S09l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S09m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S09n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S10a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S10b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S10c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S10d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [
          "UnicodeError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S10e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S10f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.utf8_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S10g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "utf8_decode requires exact ('bytes',)"
      }
    ]
  },
  {
    "id": "S10h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "utf8_decode requires exact ('bytes',)"
      }
    ]
  },
  {
    "id": "S10i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S10j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S10k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "utf8_decode requires exact ('bytes',)"
      }
    ]
  },
  {
    "id": "S10l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_decode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S10m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_decode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S10n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `data` of `probe` requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S11a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S11b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S11c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S11d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "data": "bytes"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S11e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "str"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S11f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_encode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S11g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "hex_encode requires exact ('bytes',)"
      }
    ]
  },
  {
    "id": "S11h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "hex_encode requires exact ('bytes',)"
      }
    ]
  },
  {
    "id": "S11i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S11j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S11k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "hex_encode requires exact ('bytes',)"
      }
    ]
  },
  {
    "id": "S11l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `hex_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S11m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `hex_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S11n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `data` of `probe` requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "S12a",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S12b",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S12c",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S12d",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "text": "str"
        },
        "returns": "bytes",
        "failures": [
          "ValueError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S12e",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "value": "bytes"
        },
        "returns": "bytes",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S12f",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {},
        "returns": "bytes",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.hex_decode"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "S12g",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "hex_decode requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S12h",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "hex_decode requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S12i",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S12j",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "S12k",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "hex_decode requires exact ('str',)"
      }
    ]
  },
  {
    "id": "S12l",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `hex_decode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S12m",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `hex_decode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "S12n",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL102",
        "reason": "local `Derived` is not initialized or shadows an approved operation"
      },
      {
        "rule": "PAL221",
        "reason": "argument `text` of `probe` requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "H01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "add": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "Vector[int]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H01>::add"
        ],
        "callable_dependencies": [
          "<m07_H01>::add"
        ],
        "operations": [
          "standard.vector_scan"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "parity": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "OrderedMap[int, Vector[int]]",
        "failures": [
          "RecursionError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H02>::parity"
        ],
        "callable_dependencies": [
          "<m07_H02>::parity"
        ],
        "operations": [
          "standard.vector_group_by"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "good": {
        "parameters": {
          "x": "int"
        },
        "returns": "Result[int, str]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Err.construct",
          "Ok.construct"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "Result[Vector[int], str]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H03>::good"
        ],
        "callable_dependencies": [
          "<m07_H03>::good"
        ],
        "operations": [
          "Err.construct",
          "Ok.construct",
          "standard.result_traverse"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "add": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H04>::add"
        ],
        "callable_dependencies": [
          "<m07_H04>::add"
        ],
        "operations": [
          "Vector.fold"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H01-unordered",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan requires exact ordered Vector and resolved checked callback"
      }
    ]
  },
  {
    "id": "H01-iterable",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan requires exact ordered Vector and resolved checked callback"
      }
    ]
  },
  {
    "id": "H01-unknown",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan requires exact ordered Vector and resolved checked callback"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "H01-lambda",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan requires exact ordered Vector and resolved checked callback"
      },
      {
        "rule": "PAL201",
        "reason": "Lambda is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "H01-mutable",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan requires (Vector[T], (A,T)->A, exact admitted A initial)"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "H01-arity",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan has the published fixed eager Vector signature"
      }
    ]
  },
  {
    "id": "H01-keyword",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "H01-init",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL230",
        "reason": "definition-time values use closed stable data expressions and approved builtins; checked application invocation is confined to function bodies"
      }
    ]
  },
  {
    "id": "H02-unordered",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_group_by requires exact ordered Vector and resolved checked callback"
      }
    ]
  },
  {
    "id": "H02-iterable",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_group_by requires exact ordered Vector and resolved checked callback"
      }
    ]
  },
  {
    "id": "H02-unknown",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_group_by requires exact ordered Vector and resolved checked callback"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "H02-lambda",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_group_by requires exact ordered Vector and resolved checked callback"
      },
      {
        "rule": "PAL201",
        "reason": "Lambda is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "H02-mutable",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "H02-arity",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_group_by has the published fixed eager Vector signature"
      }
    ]
  },
  {
    "id": "H02-keyword",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "H02-init",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL230",
        "reason": "definition-time values use closed stable data expressions and approved builtins; checked application invocation is confined to function bodies"
      }
    ]
  },
  {
    "id": "H03-unordered",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "result_traverse requires exact ordered Vector and resolved checked callback"
      }
    ]
  },
  {
    "id": "H03-iterable",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "result_traverse requires exact ordered Vector and resolved checked callback"
      }
    ]
  },
  {
    "id": "H03-unknown",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "result_traverse requires exact ordered Vector and resolved checked callback"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "H03-lambda",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "result_traverse requires exact ordered Vector and resolved checked callback"
      },
      {
        "rule": "PAL201",
        "reason": "Lambda is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "H03-mutable",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[int, str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "case field `value` requires its exact recursively admitted immutable data schema"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "H03-arity",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "result_traverse has the published fixed eager Vector signature"
      }
    ]
  },
  {
    "id": "H03-keyword",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      }
    ]
  },
  {
    "id": "H03-init",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL230",
        "reason": "definition-time values use closed stable data expressions and approved builtins; checked application invocation is confined to function bodies"
      }
    ]
  },
  {
    "id": "H05-str",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "key": {
        "parameters": {
          "x": "int"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "OrderedMap[str, Vector[int]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H05-str>::key"
        ],
        "callable_dependencies": [
          "<m07_H05-str>::key"
        ],
        "operations": [
          "standard.vector_group_by"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H05-bool",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "key": {
        "parameters": {
          "x": "int"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "OrderedMap[bool, Vector[int]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H05-bool>::key"
        ],
        "callable_dependencies": [
          "<m07_H05-bool>::key"
        ],
        "operations": [
          "standard.vector_group_by"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H05-bytes",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "key": {
        "parameters": {
          "x": "int"
        },
        "returns": "bytes",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "OrderedMap[bytes, Vector[int]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H05-bytes>::key"
        ],
        "callable_dependencies": [
          "<m07_H05-bytes>::key"
        ],
        "operations": [
          "standard.vector_group_by"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H05-None",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 2,
    "problems": [],
    "contracts": {
      "key": {
        "parameters": {
          "x": "int"
        },
        "returns": "None",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "OrderedMap[None, Vector[int]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_H05-None>::key"
        ],
        "callable_dependencies": [
          "<m07_H05-None>::key"
        ],
        "operations": [
          "standard.vector_group_by"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "H06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires OrderedMap[int, Vector[int]]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_group_by requires T->K with one exact scalar key schema"
      }
    ]
  },
  {
    "id": "H07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "vector_scan requires (Vector[T], (A,T)->A, exact admitted A initial)"
      },
      {
        "rule": "PAL221",
        "reason": "collection callback requires resolved bounded Callable[[int, int], int] with stable captures"
      }
    ]
  },
  {
    "id": "H08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Result[Vector[int], str]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "result_traverse requires T->Result[U,E] with admitted U/E schemas"
      }
    ]
  },
  {
    "id": "H09",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "values": "Vector[int]",
          "op": "Callable[[int, int], int]"
        },
        "returns": "Vector[int]",
        "failures": [
          "IndexError",
          "KeyError",
          "RecursionError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of",
          "standard.vector_scan"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "ValueError"
            ],
            "discharged": [
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "H10",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "values": "Vector[str]",
          "op": "Callable[[str], Result[int, str]]"
        },
        "returns": "Result[Vector[int], str]",
        "failures": [
          "IndexError",
          "KeyError",
          "RecursionError",
          "ValueError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Err.construct",
          "standard.result_traverse"
        ],
        "handlers": [
          {
            "line": 8,
            "categories": [
              "UnicodeError"
            ],
            "discharged": [
              "UnicodeError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "C01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C01>::double",
          "<m07_C01>::plus"
        ],
        "callable_dependencies": [
          "<m07_C01>::double",
          "<m07_C01>::plus"
        ],
        "operations": [
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {},
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_C02>::double",
          "<m07_C02>::plus"
        ],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [
            "<m07_C02>::double",
            "<m07_C02>::plus"
          ],
          "captures": [],
          "conditional": false,
          "effect_bound": [],
          "wrapper": "compose",
          "components": [
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C02>::double"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            },
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C02>::plus"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_C02>::double",
          "<m07_C02>::plus"
        ],
        "operations": [
          "standard.compose"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C03>::divide"
        ],
        "callable_dependencies": [
          "<m07_C03>::divide"
        ],
        "operations": [
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {},
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_C04>::divide"
        ],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [
            "<m07_C04>::divide"
          ],
          "captures": [],
          "conditional": false,
          "effect_bound": [],
          "wrapper": "partial_first",
          "components": [
            {
              "parameters": [
                "int",
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C04>::divide"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [
            [
              "int",
              "Constant(value=10)"
            ]
          ],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_C04>::divide"
        ],
        "operations": [
          "standard.partial_first"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C05",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C05>::divide"
        ],
        "callable_dependencies": [
          "<m07_C05>::divide"
        ],
        "operations": [
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": [
          {
            "line": 17,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "C06",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C06>::divide"
        ],
        "callable_dependencies": [
          "<m07_C06>::divide"
        ],
        "operations": [
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": [
          {
            "line": 19,
            "categories": [
              "ZeroDivisionError"
            ],
            "discharged": [
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "C07",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C07>::double",
          "<m07_C07>::plus"
        ],
        "callable_dependencies": [
          "<m07_C07>::double",
          "<m07_C07>::plus"
        ],
        "operations": [
          "Vector.map",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C08",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "Vector[int]",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C08>::divide"
        ],
        "callable_dependencies": [
          "<m07_C08>::divide"
        ],
        "operations": [
          "Vector.map",
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C09",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int",
          "flag": "bool"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C09>::divide",
          "<m07_C09>::double",
          "<m07_C09>::plus"
        ],
        "callable_dependencies": [
          "<m07_C09>::divide",
          "<m07_C09>::double",
          "<m07_C09>::plus"
        ],
        "operations": [
          "standard.compose",
          "standard.compose.invoke",
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C10",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C10>::double",
          "<m07_C10>::plus"
        ],
        "callable_dependencies": [
          "<m07_C10>::double",
          "<m07_C10>::plus"
        ],
        "operations": [
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C11",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 5,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "maker": {
        "parameters": {
          "op": "Callable[[int], int]"
        },
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_C11>::double"
        ],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [
            "<m07_C11>::double"
          ],
          "captures": [],
          "conditional": true,
          "effect_bound": [],
          "wrapper": "compose",
          "components": [
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C11>::double"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            },
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [],
              "captures": [],
              "conditional": true,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": "<m07_C11>::maker:op",
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_C11>::double"
        ],
        "operations": [
          "standard.compose"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C11>::double",
          "<m07_C11>::maker",
          "<m07_C11>::plus"
        ],
        "callable_dependencies": [
          "<m07_C11>::double",
          "<m07_C11>::maker",
          "<m07_C11>::plus"
        ],
        "operations": [
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C12",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 5,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "maker": {
        "parameters": {
          "op": "Callable[[int, int], int]"
        },
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [],
          "captures": [],
          "conditional": true,
          "effect_bound": [],
          "wrapper": "partial_first",
          "components": [
            {
              "parameters": [
                "int",
                "int"
              ],
              "returns": "int",
              "targets": [],
              "captures": [],
              "conditional": true,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": "<m07_C12>::maker:op",
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [
            [
              "int",
              "Constant(value=10)"
            ]
          ],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "standard.partial_first"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C12>::divide",
          "<m07_C12>::maker"
        ],
        "callable_dependencies": [
          "<m07_C12>::divide",
          "<m07_C12>::maker"
        ],
        "operations": [
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C13",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "op": "Callable[[int], int]",
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "KeyError",
          "RecursionError",
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C13>::double"
        ],
        "callable_dependencies": [
          "<m07_C13>::double"
        ],
        "operations": [
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": [
          {
            "line": 17,
            "categories": [
              "ValueError"
            ],
            "discharged": [
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "C14",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "flag": "bool"
        },
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_C14>::divide",
          "<m07_C14>::double",
          "<m07_C14>::plus"
        ],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [
            "<m07_C14>::divide",
            "<m07_C14>::double",
            "<m07_C14>::plus"
          ],
          "captures": [],
          "conditional": false,
          "effect_bound": [],
          "wrapper": "choice",
          "components": [
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C14>::double",
                "<m07_C14>::plus"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": "compose",
              "components": [
                {
                  "parameters": [
                    "int"
                  ],
                  "returns": "int",
                  "targets": [
                    "<m07_C14>::double"
                  ],
                  "captures": [],
                  "conditional": false,
                  "effect_bound": [],
                  "wrapper": null,
                  "components": [],
                  "bound_arguments": [],
                  "obligation": null,
                  "captured_callbacks": []
                },
                {
                  "parameters": [
                    "int"
                  ],
                  "returns": "int",
                  "targets": [
                    "<m07_C14>::plus"
                  ],
                  "captures": [],
                  "conditional": false,
                  "effect_bound": [],
                  "wrapper": null,
                  "components": [],
                  "bound_arguments": [],
                  "obligation": null,
                  "captured_callbacks": []
                }
              ],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            },
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C14>::divide"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": "partial_first",
              "components": [
                {
                  "parameters": [
                    "int",
                    "int"
                  ],
                  "returns": "int",
                  "targets": [
                    "<m07_C14>::divide"
                  ],
                  "captures": [],
                  "conditional": false,
                  "effect_bound": [],
                  "wrapper": null,
                  "components": [],
                  "bound_arguments": [],
                  "obligation": null,
                  "captured_callbacks": []
                }
              ],
              "bound_arguments": [
                [
                  "int",
                  "Constant(value=10)"
                ]
              ],
              "obligation": null,
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_C14>::divide",
          "<m07_C14>::double",
          "<m07_C14>::plus"
        ],
        "operations": [
          "standard.compose",
          "standard.partial_first"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C15",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 5,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "maker": {
        "parameters": {
          "bound": "int"
        },
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_C15>::divide"
        ],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [
            "<m07_C15>::divide"
          ],
          "captures": [],
          "conditional": false,
          "effect_bound": [],
          "wrapper": "partial_first",
          "components": [
            {
              "parameters": [
                "int",
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_C15>::divide"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [
            [
              "int",
              "Name(id='bound', ctx=Load())"
            ]
          ],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_C15>::divide"
        ],
        "operations": [
          "standard.partial_first"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C15>::divide",
          "<m07_C15>::maker"
        ],
        "callable_dependencies": [
          "<m07_C15>::divide",
          "<m07_C15>::maker"
        ],
        "operations": [
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C16",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 5,
    "problems": [],
    "contracts": {
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "double": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "divide": {
        "parameters": {
          "a": "int",
          "b": "int"
        },
        "returns": "int",
        "failures": [
          "ZeroDivisionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe.add": {
        "parameters": {
          "y": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {
          "fixed": "int"
        },
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_C16>::double",
          "<m07_C16>::probe.add"
        ],
        "callable_dependencies": [
          "<m07_C16>::double",
          "<m07_C16>::probe.add"
        ],
        "operations": [
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "C-negative-01",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "compose requires exactly two arguments"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "C-negative-02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "standard operations require exactly their published positional-only signature"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "C-negative-03",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "compose requires actual resolved callable/capture evidence"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `unknown` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "C-negative-04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "partial_first requires (A,B)->R with admitted data A/R and exact stable bound A; capabilities/callables cannot be bound"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      }
    ]
  },
  {
    "id": "C-negative-05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "partial_first requires (A,B)->R with admitted data A/R and exact stable bound A; capabilities/callables cannot be bound"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "C-negative-06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "partial_first requires (A,B)->R with admitted data A/R and exact stable bound A; capabilities/callables cannot be bound"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL230",
        "reason": "provider construction is ordinary unchecked setup, distinct from checked capability invocation"
      }
    ]
  },
  {
    "id": "C-negative-07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "partial_first requires exactly two arguments"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "C-negative-08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "compose requires unary outer B->R and inner A->B, admitted data B/R, and data or exact capability input A"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "C-negative-09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL221",
        "reason": "wrapper argument requires exact int"
      }
    ]
  },
  {
    "id": "C-negative-mutable-capture",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 5,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL201",
        "reason": "List is outside the scalar expression vocabulary"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "indexing requires an admitted exact Vector/map/tuple contract"
      },
      {
        "rule": "PAL210",
        "reason": "Add is uncharacterized for unknown/unsupported value and int"
      },
      {
        "rule": "PAL240",
        "reason": "captured binding `changing` is not established as stable and initialized"
      }
    ]
  },
  {
    "id": "C-negative-capcapture",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL210",
        "reason": "Add is uncharacterized for unknown/unsupported value and int"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL320",
        "reason": "capability `cap` cannot be captured by a callable"
      },
      {
        "rule": "PAL320",
        "reason": "capability `cap` cannot be captured by a callable"
      }
    ]
  },
  {
    "id": "E01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "now": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "timed": {
        "parameters": {
          "bound": "int",
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError",
          "ZeroDivisionError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {},
        "returns": "Effectful[[ClockCapability], int, Clock]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_E01>::now",
          "<m07_E01>::plus"
        ],
        "return_callable_evidence": {
          "parameters": [
            "ClockCapability"
          ],
          "returns": "int",
          "targets": [
            "<m07_E01>::now",
            "<m07_E01>::plus"
          ],
          "captures": [],
          "conditional": false,
          "effect_bound": [
            "Clock"
          ],
          "wrapper": "compose",
          "components": [
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_E01>::plus"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            },
            {
              "parameters": [
                "ClockCapability"
              ],
              "returns": "int",
              "targets": [
                "<m07_E01>::now"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [
                "Clock"
              ],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_E01>::now",
          "<m07_E01>::plus"
        ],
        "operations": [
          "standard.compose"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "E02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "now": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "timed": {
        "parameters": {
          "bound": "int",
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError",
          "ZeroDivisionError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_E02>::now",
          "<m07_E02>::plus"
        ],
        "callable_dependencies": [
          "<m07_E02>::now",
          "<m07_E02>::plus"
        ],
        "operations": [
          "ClockCapability.now_ns",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "E03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "now": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "timed": {
        "parameters": {
          "bound": "int",
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError",
          "ZeroDivisionError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_E03>::timed"
        ],
        "callable_dependencies": [
          "<m07_E03>::timed"
        ],
        "operations": [
          "ClockCapability.now_ns",
          "standard.partial_first",
          "standard.partial_first.invoke"
        ],
        "handlers": [
          {
            "line": 20,
            "categories": [
              "RuntimeError",
              "OSError",
              "IndexError",
              "ZeroDivisionError"
            ],
            "discharged": [
              "IndexError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "ZeroDivisionError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "E04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Clock"
      },
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "collection callback requires resolved bounded Callable[[ClockCapability], int] with stable captures"
      },
      {
        "rule": "PAL221",
        "reason": "wrapper invocation requires its exact characterized callable contract"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Clock"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Clock"
      }
    ]
  },
  {
    "id": "E05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 4,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Callable[[int], int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "partial_first requires (A,B)->R with admitted data A/R and exact stable bound A; capabilities/callables cannot be bound"
      }
    ]
  },
  {
    "id": "E06",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 5,
    "problems": [],
    "contracts": {
      "now": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "plus": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [],
        "handlers": []
      },
      "timed": {
        "parameters": {
          "bound": "int",
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError",
          "ZeroDivisionError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      },
      "maker": {
        "parameters": {
          "op": "Effectful[[ClockCapability], int, Clock, IO]"
        },
        "returns": "Effectful[[ClockCapability], int, Clock, IO]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_E06>::plus"
        ],
        "return_callable_evidence": {
          "parameters": [
            "ClockCapability"
          ],
          "returns": "int",
          "targets": [
            "<m07_E06>::plus"
          ],
          "captures": [],
          "conditional": true,
          "effect_bound": [
            "Clock",
            "IO"
          ],
          "wrapper": "compose",
          "components": [
            {
              "parameters": [
                "int"
              ],
              "returns": "int",
              "targets": [
                "<m07_E06>::plus"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            },
            {
              "parameters": [
                "ClockCapability"
              ],
              "returns": "int",
              "targets": [],
              "captures": [],
              "conditional": true,
              "effect_bound": [
                "Clock",
                "IO"
              ],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": "<m07_E06>::maker:op",
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_E06>::plus"
        ],
        "operations": [
          "standard.compose"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_E06>::maker",
          "<m07_E06>::now",
          "<m07_E06>::plus"
        ],
        "callable_dependencies": [
          "<m07_E06>::maker",
          "<m07_E06>::now",
          "<m07_E06>::plus"
        ],
        "operations": [
          "ClockCapability.now_ns",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "F-IO",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "IOCapability"
        },
        "returns": "str",
        "failures": [
          "KeyError",
          "OSError",
          "RuntimeError",
          "UnicodeError",
          "ValueError"
        ],
        "required_effects": [
          "IO"
        ],
        "effect_bound": [
          "IO"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "IOCapability.read_text"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "F-IO-handled",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "IOCapability"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [
          "IO"
        ],
        "effect_bound": [
          "IO"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "IOCapability.read_text"
        ],
        "handlers": [
          {
            "line": 9,
            "categories": [
              "OSError",
              "RuntimeError",
              "ValueError",
              "IndexError",
              "KeyError"
            ],
            "discharged": [
              "IndexError",
              "KeyError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "F-IO-pure",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared IO"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared IO"
      }
    ]
  },
  {
    "id": "F-Clock",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [
          "IndexError",
          "OSError",
          "RuntimeError"
        ],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "F-Clock-handled",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "ClockCapability"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [
          "Clock"
        ],
        "effect_bound": [
          "Clock"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "ClockCapability.now_ns"
        ],
        "handlers": [
          {
            "line": 9,
            "categories": [
              "OSError",
              "RuntimeError",
              "ValueError",
              "IndexError",
              "KeyError"
            ],
            "discharged": [
              "IndexError",
              "KeyError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "F-Clock-pure",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Clock"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Clock"
      }
    ]
  },
  {
    "id": "F-Environment",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "EnvironmentCapability"
        },
        "returns": "str",
        "failures": [
          "OSError",
          "RuntimeError",
          "UnicodeError",
          "ValueError"
        ],
        "required_effects": [
          "Environment"
        ],
        "effect_bound": [
          "Environment"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "EnvironmentCapability.get"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "F-Environment-handled",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 1,
    "problems": [],
    "contracts": {
      "probe": {
        "parameters": {
          "cap": "EnvironmentCapability"
        },
        "returns": "str",
        "failures": [],
        "required_effects": [
          "Environment"
        ],
        "effect_bound": [
          "Environment"
        ],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "EnvironmentCapability.get"
        ],
        "handlers": [
          {
            "line": 9,
            "categories": [
              "OSError",
              "RuntimeError",
              "ValueError",
              "IndexError",
              "KeyError"
            ],
            "discharged": [
              "IndexError",
              "KeyError",
              "OSError",
              "RecursionError",
              "RuntimeError",
              "UnicodeError",
              "ValueError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "F-Environment-pure",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL310",
        "reason": "capability parameter `cap` requires declared Environment"
      },
      {
        "rule": "PAL310",
        "reason": "boundary requires undeclared Environment"
      }
    ]
  },
  {
    "id": "N01",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N03",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `partial` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "N08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL201",
        "reason": "attribute access is admitted only for statically resolved module dependencies"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "N11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `int` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "N12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires str; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `str` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "N13",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `sum` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "N14",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires Vector[int]; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `sorted` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W01",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W02",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W03",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W04",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W05",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W06",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL120",
        "reason": "only one unchanged @fun and one finite @effects declaration are supported"
      },
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "W09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bytes; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `utf8_encode` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V01",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "one": {
        "parameters": {
          "x": "int"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of"
        ],
        "handlers": []
      },
      "size": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "nonempty": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_V01>::one",
          "<m07_V01>::size"
        ],
        "callable_dependencies": [
          "<m07_V01>::one",
          "<m07_V01>::size"
        ],
        "operations": [
          "Vector.len",
          "Vector.of",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "V02",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "one": {
        "parameters": {
          "x": "int"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of"
        ],
        "handlers": []
      },
      "size": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "nonempty": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "Vector[int]"
        },
        "returns": "Vector[int]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_V02>::one",
          "<m07_V02>::size"
        ],
        "callable_dependencies": [
          "<m07_V02>::one",
          "<m07_V02>::size"
        ],
        "operations": [
          "Vector.len",
          "Vector.map",
          "Vector.of",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "V03",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "one": {
        "parameters": {
          "x": "int"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of"
        ],
        "handlers": []
      },
      "size": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "nonempty": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "Vector[int]"
        },
        "returns": "Vector[int]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_V03>::nonempty",
          "<m07_V03>::one"
        ],
        "callable_dependencies": [
          "<m07_V03>::nonempty",
          "<m07_V03>::one"
        ],
        "operations": [
          "Vector.filter",
          "Vector.len",
          "Vector.of",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "V04",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "one": {
        "parameters": {
          "x": "int"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of"
        ],
        "handlers": []
      },
      "size": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "nonempty": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "Vector[int]"
        },
        "returns": "OrderedMap[int, Vector[int]]",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_V04>::one",
          "<m07_V04>::size"
        ],
        "callable_dependencies": [
          "<m07_V04>::one",
          "<m07_V04>::size"
        ],
        "operations": [
          "Vector.len",
          "Vector.of",
          "standard.compose",
          "standard.compose.invoke",
          "standard.vector_group_by"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "V05",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 5,
    "problems": [],
    "contracts": {
      "one": {
        "parameters": {
          "x": "int"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of"
        ],
        "handlers": []
      },
      "size": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "nonempty": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "maker": {
        "parameters": {},
        "returns": "Callable[[int], int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [
          "<m07_V05>::one",
          "<m07_V05>::size"
        ],
        "return_callable_evidence": {
          "parameters": [
            "int"
          ],
          "returns": "int",
          "targets": [
            "<m07_V05>::one",
            "<m07_V05>::size"
          ],
          "captures": [],
          "conditional": false,
          "effect_bound": [],
          "wrapper": "compose",
          "components": [
            {
              "parameters": [
                "Vector[int]"
              ],
              "returns": "int",
              "targets": [
                "<m07_V05>::size"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            },
            {
              "parameters": [
                "int"
              ],
              "returns": "Vector[int]",
              "targets": [
                "<m07_V05>::one"
              ],
              "captures": [],
              "conditional": false,
              "effect_bound": [],
              "wrapper": null,
              "components": [],
              "bound_arguments": [],
              "obligation": null,
              "captured_callbacks": []
            }
          ],
          "bound_arguments": [],
          "obligation": null,
          "captured_callbacks": []
        },
        "invoked_targets": [],
        "callable_dependencies": [
          "<m07_V05>::one",
          "<m07_V05>::size"
        ],
        "operations": [
          "standard.compose"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [
          "RecursionError"
        ],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_V05>::maker",
          "<m07_V05>::one",
          "<m07_V05>::size"
        ],
        "callable_dependencies": [
          "<m07_V05>::maker",
          "<m07_V05>::one",
          "<m07_V05>::size"
        ],
        "operations": [
          "Vector.len",
          "Vector.of",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": []
      }
    }
  },
  {
    "id": "V06",
    "expected": 0,
    "native_observed": 0,
    "linux_observed": 0,
    "selected": 4,
    "problems": [],
    "contracts": {
      "one": {
        "parameters": {
          "x": "int"
        },
        "returns": "Vector[int]",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.of"
        ],
        "handlers": []
      },
      "size": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "nonempty": {
        "parameters": {
          "values": "Vector[int]"
        },
        "returns": "bool",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode.fun identity marker"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [],
        "callable_dependencies": [],
        "operations": [
          "Vector.len"
        ],
        "handlers": []
      },
      "probe": {
        "parameters": {
          "x": "int"
        },
        "returns": "int",
        "failures": [],
        "required_effects": [],
        "effect_bound": [],
        "trust": [
          "CPython 3.13.1 standard scalar, tuple, function and annotation operations",
          "pyalamode collections-v1: exact deep-data fa\u00e7ade, CPython tuple-copy storage and canonical scalar ordering",
          "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion",
          "pyalamode.fun identity marker",
          "pyalamode.standard-v1: finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
        ],
        "captures": {},
        "callable_targets": {},
        "return_callable_targets": [],
        "return_callable_evidence": null,
        "invoked_targets": [
          "<m07_V06>::one",
          "<m07_V06>::size"
        ],
        "callable_dependencies": [
          "<m07_V06>::one",
          "<m07_V06>::size"
        ],
        "operations": [
          "Vector.len",
          "Vector.of",
          "standard.compose",
          "standard.compose.invoke"
        ],
        "handlers": [
          {
            "line": 16,
            "categories": [
              "RuntimeError"
            ],
            "discharged": [
              "RecursionError",
              "RuntimeError"
            ],
            "target": null,
            "target_semantics": "opaque actual Python exception, deleted on every handler exit"
          }
        ]
      }
    }
  },
  {
    "id": "V07",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 3,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires int; found unknown/unsupported value"
      },
      {
        "rule": "PAL221",
        "reason": "partial_first requires (A,B)->R with admitted data A/R and exact stable bound A; capabilities/callables cannot be bound"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      }
    ]
  },
  {
    "id": "V08",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V09",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V10",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V11",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V12",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V13",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V14",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V15",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V16",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V17",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V18",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V19",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V20",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V21",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V22",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V23",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 1,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL211",
        "reason": "return requires bool; found unknown/unsupported value"
      },
      {
        "rule": "PAL230",
        "reason": "call target is not a resolved checked callable or characterized builtin"
      },
      {
        "rule": "PAL240",
        "reason": "binding `text_startswith` is not a statically established stable dependency"
      }
    ]
  },
  {
    "id": "V24",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "checked callable `anchor` has an analyzed attribute/behavior replacement"
      },
      {
        "rule": "PAL240",
        "reason": "checked callable `probe` has an analyzed attribute/behavior replacement"
      }
    ]
  },
  {
    "id": "V25",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "checked callable `anchor` has an analyzed attribute/behavior replacement"
      },
      {
        "rule": "PAL240",
        "reason": "checked callable `probe` has an analyzed attribute/behavior replacement"
      }
    ]
  },
  {
    "id": "V26",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "checked callable `anchor` has an analyzed attribute/behavior replacement"
      },
      {
        "rule": "PAL240",
        "reason": "checked callable `probe` has an analyzed attribute/behavior replacement"
      }
    ]
  },
  {
    "id": "V27",
    "expected": 1,
    "native_observed": 1,
    "linux_observed": 1,
    "selected": 2,
    "problems": [],
    "diagnostics": [
      {
        "rule": "PAL240",
        "reason": "checked callable `anchor` has an analyzed attribute/behavior replacement"
      },
      {
        "rule": "PAL240",
        "reason": "checked callable `probe` has an analyzed attribute/behavior replacement"
      }
    ]
  }
]
```

## Independent final helper measurement inspection

The reviewer read the entire 430-line new harness and exact shared `_measure`, then parsed both actual packets and recomputed every median elapsed/per-call time and maximum traced peak. Each has exactly six named conditions at n=10/100 in off/exports/debug: 36 rows, 108 traced intervals, 2,700 measured calls and 360 untimed warmups. All correctness flags pass. Untimed counts agree: off zero; exports two; debug text_decimal 48/408, encoding_roundtrip 4/4, scan 34/304, grouping 24/204, composition 54/504, traversal_first_error 16/106. Thirteen checked workload functions, six selected exports and 13 debug coverage entries agree with artifact evidence. The record/case/domain catalog is fixed before intervals.

Build/import/input/instrumentation/warmups/verification/hash/JSON are excluded. Invocation loops, native/library/generated data checks, transient disposal and tracemalloc overhead are included; GC precedes intervals and only the last result is retained. These are warm-process Python-traced allocation/time observations, not RSS or cold source-check/cache/import/build/setup measurements. OS caches, scheduling and load are uncontrolled. They justify no general speedup/latency threshold or human usefulness claim.

Both packets retain exact 14-foundation/15-package/five-owned-input maps equal before/after, across platforms and to current independent source entries. Separate untimed effect/setup smoke records three unchecked ordinary setup rows, actual IO/Clock/Environment and a pure export. Four acquired streams close on every success/failure; malformed read/surrogate-write fail with zero strict/surrogateescape callbacks; opening/truncation precedes encoding failure; CRLF/BOM/non-BMP roundtrip; permissions and surrogate OS names refuse. Native environment invalid-byte decoding is independently controlled in the isolated runtime probe.

Inspection summary:

```json
{
  "rows": [
    {
      "platform": "macos",
      "rows": 36,
      "intervals": 108,
      "measured_calls": 2700,
      "warmup_calls": 360,
      "foundations": 14,
      "package_sources": 15,
      "owned_sources": 5,
      "unchanged": true,
      "guard_counts_recomputed": true,
      "medians_recomputed": true,
      "all_correctness": true,
      "setup_observations": 3,
      "native_streams": 4,
      "handler_hits": 0,
      "sha256": "d213178c571f99d4db77bcb68e70328f1a3a8c1ff062283b5a8a231b56c8d02c"
    },
    {
      "platform": "linux",
      "rows": 36,
      "intervals": 108,
      "measured_calls": 2700,
      "warmup_calls": 360,
      "foundations": 14,
      "package_sources": 15,
      "owned_sources": 5,
      "unchanged": true,
      "guard_counts_recomputed": true,
      "medians_recomputed": true,
      "all_correctness": true,
      "setup_observations": 3,
      "native_streams": 4,
      "handler_hits": 0,
      "sha256": "542fd0c6c82becff4aefdeab99405d9407a1c8d14c99978c628da584d3fa20f8"
    }
  ],
  "current_review_source_equal": true,
  "cross_platform_source_equal": true,
  "source_unchanged": true,
  "measured_operations_only": true,
  "notes": "Instrumented callback/data assertion counts are untimed; measured intervals are warm steady process Python traced allocation/time, not RSS or cold import/build/cache/setup timings. System load and OS caches uncontrolled. No usefulness or universal performance threshold claim."
}
```

## Final references and terminal review boundary

Main and runtime workers completed authorized documentation-only handoffs after source freeze. The final current reference digests below replace their pre-freeze status-document identities; product/test/example/harness and all raw measurement/reviewer input bytes remain unchanged. The reviewer additionally parsed all 36 displayed helper result rows and verified every six-decimal ms/call value, peak-byte value and generated assertion count against both raw packets. Inputs, fixed catalogs and earlier interval outputs predate tracing, so measured peaks do not claim total retained memory or memory-retention behavior. The complete literal sources and all 17 executable harness texts were parsed from this document and matched the frozen outside-checkout inputs.

```json
{
  "SPEC-sol6.1-composite.md": "3d8f845b5b3739418062caa44db5ba51b95bc99823425bde3b4aff6cebaaee48",
  "Docs/milestones/06-domains.md": "7005da2fbc9c36f4f595ac07a17cf96e393f4ab8ecfb5c4f78d9e291af7ec065",
  "Docs/evidence/m06-runtime-contract.md": "9c1292ce605d1d98718a8db33e068be0866c68498f4c20a41e4b0953e64c0e2a",
  "Docs/conformance/m06-cases.md": "bec9bb9e7bf4a55bc13276c46c8817be2fe1e6afd5de17d872bd36ab29fd8cb3",
  "Docs/milestones/07-standard.md": "8648f0e989756f03f260d4e8673f1b098f4b1673dfa2bb11d3fc659b3a5cfb7a",
  "Docs/evidence/m07-runtime-contract.md": "4e0615c40a0bf69cc91f2b81ad08e77332a258007ac48456c53d70ae84632df2",
  "Docs/evidence/m07-runtime-measurements.md": "bbd4a2a6d50e63411f076f32bfe3bcd055b255c5108eab23b598cf4d6d46a7cf",
  "Docs/evidence/m07-runtime-macos.json": "d213178c571f99d4db77bcb68e70328f1a3a8c1ff062283b5a8a231b56c8d02c",
  "Docs/evidence/m07-runtime-linux.json": "542fd0c6c82becff4aefdeab99405d9407a1c8d14c99978c628da584d3fa20f8",
  "README.md": "8185b5dda4d698404e9bfd6a58226a2efa84b2f7a64848c134f5bcf6206efcc6",
  "pyproject.toml": "7b993e35b0c738d99b2ab823c05f4599b73655ddfb48fe3af06fe5f8b378ebeb"
}
```

Explicit final document validation parsed every JSON block, recovered all seven exact corpus/layout inputs and all 17 complete executable sources, confirmed 532 unique expected/observed rows and found no trailing whitespace or tab characters. The tracked-tree `git diff --check` also passed; because this document was untracked during review, the separate text whitespace inspection is the evidence for this file. All 92 current source inputs and all 15 actual installed Python files were rehashed and remain equal to both platform before/after maps.

No concrete soundness discrepancy remains in this fixed bounded matrix. The approved runtime configuration and caller/setup/effect/failure/trust obligations continue to limit admission; arbitrary Python, Windows, free-threaded builds, alternative runtimes and later milestone scopes are not covered. Target-user usefulness and authoring time remain UNMEASURED; the prepared protocol requires actual participants before any such claim. Root owns release acceptance, the ledger and Git. This independent unit is complete and ends supervised work; no additional product/test/example/README/ledger files were edited by the reviewer and no reviewer commit was made.
