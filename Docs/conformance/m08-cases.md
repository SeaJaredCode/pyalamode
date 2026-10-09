# M8 independent conformance review

Status: the fixed adversarial plan and literal expectations preceded admission. Corrected frozen source passes independent installed conformance on macOS and Linux: 320 test methods, 708 literal source/policy cases and 57 fixed runtime inputs per target. Frozen support-cost observations are independently reconciled, with scope and exact provenance below. Human integration usefulness and authoring benefit are **UNMEASURED**.

Authority read in full: `SPEC-sol6.1-composite.md` (545 lines), especially §§3–5, 8–12, 14–18, A22, A23, A32 and all inherited gates. Prerequisite: independently verified M1–M7 at `4531a3e`, CPython 3.13.1 standard GIL on macOS and actual Linux, native filesystem UTF-8/surrogateescape. This reviewer owns only this file and ephemeral probes outside the checkout. Root approves the finite catalog, coordinates source freeze, accepts the milestone and owns Git. Main/runtime workers own product, tests, examples, contracts and measurements. M9–M14 are non-goals.

## Fixed adversarial plan

The plan below is fixed before admission. After root approves the exact finite catalog, instantiate complete literal sources, project layouts, policies, actual installed identities, runtime inputs and expected observations; hash them before observing readiness. Expected results remain fixed when a bug appears. Publish any focused supplement before observing its correction. A narrowed operation requires explicit root approval and visible provenance rather than changing expectations to fit output.

| Plan IDs | Independent obligation fixed before admission |
| --- | --- |
| E01–E12 | At least two real bounded integrations, each with actual operation, installed version and artifact identity; exact inputs/results, effects, failures, delayed execution, aliases, ownership, resource lifetime, initialization, owner, rationale, provenance and expiry. Read actual native/transitive implementation dependencies, backend selection, mutable caches/registries/error handlers and implicit operators/getters/iterators/formatters/constructors/restoration. Exact output, copying and a “pure” declaration never establish purity. |
| A01–A18 | Denied by default; draft, absent, expired, wrong-operation, wrong-version and wrong-artifact approvals cannot admit. Explicit approved entries admit only the named operation and artifact. Project override provenance stays visible and cannot erase known effects or unchecked implementation. Invalid/ambiguous/duplicate/unbounded policy fails with tooling status; policy and approvals are reviewable project files. |
| N01–N12 | Metadata and installed identity discovery must read bytes statically without application or dependency import execution. Module/default/decorator/annotation/class/backend-discovery sentinels remain zero in check, audit, build, explanation and metadata discovery. A pure export never certifies unchecked import/setup. Strict module initialization and ordinary setup observations remain separate. |
| T01–T20 | External trust appears in every relevant direct, indirect, conditional, returned, captured, composed and partially bound callable, eager map/filter/fold/scan/group/traverse, data operation and characterized handler. Construction retains latent assumptions without inventing invocation effects. Every conditional target is retained; failure masks remove only the handled failure at that occurrence. |
| F01–F12 | Effects, known failures, resource/lifetime/mutation/alias conditions and initialization remain independent fields. Approved effectful operations retain their effects through fake providers, callbacks and handled failures. Unknown behavior stays unverified even under every effect family. Error selection/order and invalid ordinary input behavior obey the approved finite contract. |
| W01–W20 | Aliased/shadowed operations, native/backend/private helpers, shared defining-function globals, nested builtins dictionaries, class writers and writer functions cannot acquire admission by spelling. Actual dependency inventories include imported function globals and transitive helpers. An analyzed writer invalidates affected evidence under cold/full/partial-warm checks. |
| U01–U12 | Unsafe ordinary adapters publish explicit marker/scope/rationale and remain unchecked. Pure and checked effectful functions cannot call an uncharacterized adapter. Validated isolated output can start a new strict computation; retained source aliases may subsequently mutate without changing the new core input. Unsupported hooks, subclasses, cycles, views, missing exclusive snapshot preconditions and mutable nested data fail without invoking them. No certification of prior shell behavior is inferred. |
| K01–K16 | Cold/no-cache/full-warm/partial-warm checks preserve status and detached effects/failures/trust/callback/setup evidence. Real installed bytes/version changes, absent backend, expired approval, source/policy/catalog/product changes and copied-product changes invalidate affected current evidence. Unrelated selected modules may retain cache hits. Corrupt/deleted caches cannot change admission. |
| B01–B14 | Actual CLI strict/audit/build/explain plus ordinary stock-Python artifact execution. Failed gate returns 1 or tooling 2 as appropriate and creates no artifact/sentinel. Accepted off artifacts retain source bytes. Exports/debug guards retain their stated exact data coverage and reject invalid data before body, with no runtime registry/loader claim. Optional `run` is currently unsupported and creates no artifact. |
| R01–R16 | Real approved runtime outputs, empty/boundary/invalid values, result equivalence, no retained mutable aliases, actual failure categories, effect and setup controls, unsupported hook dispatch and resource cleanup on success/failure. External backend/environment assumptions are tested through isolated subprocesses without modifying the checkout or shared installation. |
| X01–X10 | Native and actual networking-disabled Docker `python:3.13.1-slim`: focused and complete suites, inherited literal corpus, fresh installed product and meaningful real backend probes, complete current/cross/before-after identity maps, actual installed product bytes and actual approved backend bytes/version. Count test methods, literal cases, assertions, recorded rows and subprocesses separately. |
| P01–P08 | Read the entire named workload/guard-cost harness only after explicit joint root source freeze. Recompute published row summaries, correctness/assertion controls and source identities from raw platform packets. Runtime costs do not establish user benefit; no unsupported platform/runtime/performance or package-consumer guarantee is inferred. |

Final evidence will retain reproducible complete fixture/layout/policy/input and executable harness text, exact fixed expectations, raw outcomes and actual digests. Inherited M7 literal and harness records may be referenced by their frozen named identity rather than duplicated. Compact outcomes must agree with raw fields. This file receives an explicit whitespace check because an untracked document is outside `git diff --check` coverage.

## Target-user protocol

Recruit application Python developers who own a real integration shell. Give them the two approved catalog operations, an ordinary unsafe adapter fixture and the published guide. Record Python/integration experience; time approval of an exact installed operation, repair of an expired/wrong-artifact policy, interpretation of transitive trust, and conversion of mutable unsafe output into a new strict calculation. Record completion, errors, diagnostic comprehension, ordinary artifact execution, perceived usefulness and reasons for avoiding the catalog. Publish participant count and each task separately. No participant observations exist; usefulness remains **UNMEASURED**.

## Readiness boundary

Awaiting root-approved catalog and policy, then literal/source/input freeze. No new operation is independently accepted by this document yet.

## Independent preapproval native inspection

The proposed two backends were independently inspected before admission. Exact v3.13.1 C and generated call-binding sources were downloaded outside the checkout; this was source inspection, not application or dependency import. Native Base64 strict decoding does not enforce canonical unused pad bits, so the proposed re-encode equality is necessary. Decode failures construct the module-state `binascii.Error` heap exception class; its constructor/behavioral dictionary and aliases belong in writer/dependency assumptions. Exact-byte prevalidation excludes foreign buffer dispatch. [CPython binascii source](https://github.com/python/cpython/blob/v3.13.1/Modules/binascii.c).

The chosen `_sha2` constructor creates private HACL state, updates from the exact buffer, returns the native hash object only internally, and its digest method produces bytes before deallocation frees state. Its SHA256 native type is immutable and cannot be subclassed; the selected path has no OpenSSL/provider selection. Module initialization creates all four SHA2 native types, separately from invocation. [CPython SHA2 source](https://github.com/python/cpython/blob/v3.13.1/Modules/sha2module.c).

Static native artifact inspection used `sysconfig.get_config_var("DESTSHARED")`, filenames and byte reads, without importing either backend. `otool -L` reports `binascii` linked to `/usr/lib/libz.1.dylib` and `/usr/lib/libSystem.B.dylib`, `_sha2` to libSystem only. Linked-loader foundations remain disclosed; Base64 does not use the CRC/zlib algorithms. These are actual macOS observations, with Linux inspection still pending.

| Independent source/artifact input | SHA-256 |
| --- | --- |
| v3.13.1 `Modules/binascii.c` | `6279cb34617ca0a744d6824828a5972fc247bf2db2061e74321e4796ae21b909` |
| v3.13.1 `Modules/sha2module.c` | `24c7bf64cf100334ff823024096f94cd0233c7c766d68bc4bbd576700fbfe1c8` |
| v3.13.1 `Modules/clinic/binascii.c.h` | `9e6231dac474014d2e3ea48001982ec7b3ce69113e437635ab534ece85281316` |
| v3.13.1 `Modules/clinic/sha2module.c.h` | `db592dab2478863f8c7964570e8c0c785fd9802617fc3104cdf2418afdb145f9` |
| v3.13.1 `Modules/_hacl/Hacl_Hash_SHA2.c` | `30638efb75c8b185bb09c3df6977e3f3c5d21a1e696218cf7ade6bc4d5201b31` |
| Actual macOS `binascii.cpython-313-darwin.so` | `428c1263cf9326aae8e9913b9898852ce1ca0f5f3736148638af01eeb0ebaaca` |
| Actual macOS `_sha2.cpython-313-darwin.so` | `b6bfcfe427f23d6705e084795ce320e9cf7c59c5df26250e7430a31b5c12ba62` |

The native directory is `/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload`; actual resolved dependency paths and all final before/after identities will be captured again during readiness verification. These inspected input hashes are provenance, not approval or current product readiness.

## Root-approved fixed literal inputs

The root's installed-console probe identified an extensionless launcher file falsely treated as an importable `pyalamode` package shadow. Before this reviewer observes the correction, a focused console supplement is fixed: use exact source/layout case `E01-direct`, its exact current reviewed approval, and run `[str(Path(sys.executable).parent / "pyalamode"), "check", "--root", str(root), "--json", "--no-cache"]` from outside the source project. Expected status is 0, verified selected wrapper with its exact Base64 assumption, no sentinel, and no extensionless launcher shadow. This is a separate real-console subprocess count, not a new source case.

The inherited M7 CLI harness runs some `python -c` commands from the original-source project while prepending its artifact through PYTHONPATH. That path precedence can select original source, so those rows cannot establish copied-artifact execution. Root's independent M7 artifact gates ran with cwd equal to output and remain separate acceptance evidence. Every new M8 stock-artifact run will use cwd equal to its generated artifact and assert the actual module `__file__` is inside that output. Inherited fixed outcomes remain unchanged.

Root approved the exact two-backend/three-operation catalog and schema/API before this freeze. The M8 source/layout corpus is fixed before any implementation admission observation: 176 cases, 37 admits, 119 strict refusals and 20 tooling refusals; SHA-256 `4a83d211d8b72fc8cf175bf5323042000933e300efd20416da7e14dc51fc5b74`. The independent known-answer/boundary runtime corpus is 57 cases (27 completing results, 30 ValueError failures). Its exact digest is recorded below. All sources/layouts and expected dimensions are complete; platform-local approval digests are instantiated from nonexecuting installed discovery before each observation, with explicit reviewer owner/rationale/provenance and fixed 2999 UTC expiry. This is test approval of the fixed reviewed contract, never a production approval workflow. Inherited 532 M7 source cases and their frozen harness text are replayed from the existing M7 record.

Case controls: approval_operations names exact reviewed entries; omitted policy_mode is approved; approval_mutation is a literal field change/removal (None); nonexpiring removes expiry; override writes exact reviewed/draft JSON; invalid policies retain their fixed tooling2 expectation. Trust expectations apply to the named probe boundary (total for the unsafe shell case), without certifying prior shell behavior. Expected known failures/effects/initialization and external setup remain independent.

m08-literal-cases.json SHA-256 `4a83d211d8b72fc8cf175bf5323042000933e300efd20416da7e14dc51fc5b74`.

```json
[
  {
    "id": "E01-direct",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E01-alias",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode as adapter\n@fun\ndef probe(data:bytes)->bytes:\n    return adapter(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E01-namespace",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations as adapter\n@fun\ndef probe(data:bytes)->bytes:\n    return adapter.base64_encode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E01-package",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations\n@fun\ndef probe(data:bytes)->bytes:\n    return pyalamode.integrations.base64_encode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E01-empty",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-extra",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data,data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-keyword",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data=data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-star",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(*(data,))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-int",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(1)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-bool",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(True)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-text",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(\"abc\")\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-tuple",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode((data,))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-vector",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(Vector.of(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-mutable",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(bytearray(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-view",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(memoryview(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-return-schema",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->int:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-subclass",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\nclass Derived(bytes):\n    pass\nprobe(Derived(b\"abc\"))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-default",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes=base64_encode(b\"abc\"))->bytes:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-initializer",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\nvalue=base64_encode(b\"abc\")\ndef probe()->bytes:\n    return value\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-strict-import",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\ndef probe(data:bytes)->bytes:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-direct-callback",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(values:Vector[bytes])->Vector[bytes]:\n    return values.map(base64_encode)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-shadow",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\nbase64_encode=unknown\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E01-deny",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "policy_mode": "deny"
  },
  {
    "id": "E01-missing",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": []
  },
  {
    "id": "E01-wrong-contract",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "contract_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "E01-wrong-dependency",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "dependency_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "E01-expired",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "expires_at": "2000-01-01T00:00:00Z"
    }
  },
  {
    "id": "E01-nonexpiring",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "failures": [
      "ValueError"
    ],
    "approval_remove_expiry": true
  },
  {
    "id": "E02-direct",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E02-alias",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode as adapter\n@fun\ndef probe(data:bytes)->bytes:\n    return adapter(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E02-namespace",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations as adapter\n@fun\ndef probe(data:bytes)->bytes:\n    return adapter.base64_decode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E02-package",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations\n@fun\ndef probe(data:bytes)->bytes:\n    return pyalamode.integrations.base64_decode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E02-empty",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-extra",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data,data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-keyword",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data=data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-star",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(*(data,))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-int",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(1)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-bool",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(True)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-text",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(\"abc\")\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-tuple",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode((data,))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-vector",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(Vector.of(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-mutable",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(bytearray(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-view",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(memoryview(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-return-schema",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->int:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-subclass",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\nclass Derived(bytes):\n    pass\nprobe(Derived(b\"abc\"))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-default",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes=base64_decode(b\"abc\"))->bytes:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-initializer",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\nvalue=base64_decode(b\"abc\")\ndef probe()->bytes:\n    return value\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-strict-import",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\ndef probe(data:bytes)->bytes:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-direct-callback",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(values:Vector[bytes])->Vector[bytes]:\n    return values.map(base64_decode)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-shadow",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\nbase64_decode=unknown\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E02-deny",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "policy_mode": "deny"
  },
  {
    "id": "E02-missing",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": []
  },
  {
    "id": "E02-wrong-contract",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_decode",
      "contract_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "E02-wrong-dependency",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_decode",
      "dependency_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "E02-expired",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_decode",
      "expires_at": "2000-01-01T00:00:00Z"
    }
  },
  {
    "id": "E02-nonexpiring",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "failures": [
      "ValueError"
    ],
    "approval_remove_expiry": true
  },
  {
    "id": "E03-direct",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E03-alias",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest as adapter\n@fun\ndef probe(data:bytes)->bytes:\n    return adapter(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E03-namespace",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations as adapter\n@fun\ndef probe(data:bytes)->bytes:\n    return adapter.sha256_digest(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E03-package",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations\n@fun\ndef probe(data:bytes)->bytes:\n    return pyalamode.integrations.sha256_digest(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "failures": [
      "ValueError"
    ],
    "required_effects": [],
    "initializer": "unchecked ordinary module initialization",
    "external_setup": true
  },
  {
    "id": "E03-empty",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-extra",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data,data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-keyword",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data=data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-star",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(*(data,))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-int",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(1)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-bool",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(True)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-text",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(\"abc\")\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-tuple",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest((data,))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-vector",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(Vector.of(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-mutable",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(bytearray(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-view",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(memoryview(data))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-return-schema",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->int:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-subclass",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\nclass Derived(bytes):\n    pass\nprobe(Derived(b\"abc\"))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-default",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes=sha256_digest(b\"abc\"))->bytes:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-initializer",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\nvalue=sha256_digest(b\"abc\")\ndef probe()->bytes:\n    return value\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-strict-import",
    "files": {
      "core.py": "# mode: fun\nfrom pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\ndef probe(data:bytes)->bytes:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-direct-callback",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(values:Vector[bytes])->Vector[bytes]:\n    return values.map(sha256_digest)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-shadow",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\nsha256_digest=unknown\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "E03-deny",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "policy_mode": "deny"
  },
  {
    "id": "E03-missing",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": []
  },
  {
    "id": "E03-wrong-contract",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.sha256_digest",
      "contract_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "E03-wrong-dependency",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.sha256_digest",
      "dependency_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "E03-expired",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.sha256_digest",
      "expires_at": "2000-01-01T00:00:00Z"
    }
  },
  {
    "id": "E03-nonexpiring",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "failures": [
      "ValueError"
    ],
    "approval_remove_expiry": true
  },
  {
    "id": "T-direct",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return encode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-conditional",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes,flag:bool)->bytes:\n    selected=encode if flag else digest\n    return selected(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-returned",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef choose(flag:bool)->Callable[[bytes],bytes]:\n    return encode if flag else digest\n@fun\ndef probe(data:bytes,flag:bool)->bytes:\n    selected=choose(flag)\n    return selected(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-captured",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    selected=encode\n    def retained(value:bytes)->bytes:\n        return selected(value)\n    return retained(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-composed",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return compose(digest,compose(decode,encode))(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-latent-composed",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe()->Callable[[bytes],bytes]:\n    return compose(digest,compose(decode,encode))\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": []
  },
  {
    "id": "T-latent-returned",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(flag:bool)->Callable[[bytes],bytes]:\n    return encode if flag else digest\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": []
  },
  {
    "id": "T-partial",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef salted(prefix:bytes,data:bytes)->bytes:\n    return digest(prefix+data)\n@fun\ndef probe(data:bytes)->bytes:\n    return partial_first(salted,b\"salt\")(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-latent-partial",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef salted(prefix:bytes,data:bytes)->bytes:\n    return digest(prefix+data)\n@fun\ndef probe()->Callable[[bytes],bytes]:\n    return partial_first(salted,b\"salt\")\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": []
  },
  {
    "id": "T-eager-map",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(values:Vector[bytes])->Vector[bytes]:\n    return values.map(compose(digest,encode))\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures_contains": [
      "ValueError"
    ]
  },
  {
    "id": "T-eager-filter",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef valid(data:bytes)->bool:\n    return encode(data)==b\"\"\n@fun\ndef probe(values:Vector[bytes])->Vector[bytes]:\n    return values.filter(valid)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "required_effects": [],
    "failures_contains": [
      "ValueError"
    ]
  },
  {
    "id": "T-eager-fold",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef combine(acc:bytes,data:bytes)->bytes:\n    return digest(acc+data)\n@fun\ndef probe(values:Vector[bytes])->bytes:\n    return values.fold(combine,b\"\")\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures_contains": [
      "ValueError"
    ]
  },
  {
    "id": "T-eager-scan",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef combine(acc:bytes,data:bytes)->bytes:\n    return digest(acc+data)\n@fun\ndef probe(values:Vector[bytes])->Vector[bytes]:\n    return vector_scan(values,combine,b\"\")\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures_contains": [
      "ValueError"
    ]
  },
  {
    "id": "T-eager-group",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(values:Vector[bytes])->OrderedMap[bytes,Vector[bytes]]:\n    return vector_group_by(values,digest)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures_contains": [
      "ValueError"
    ]
  },
  {
    "id": "T-eager-traverse",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef parse(data:bytes)->Result[bytes,Failure]:\n    try:\n        return Ok(decode(data))\n    except ValueError as caught:\n        return Err(failure_value(caught))\n@fun\ndef probe(values:Vector[bytes])->Result[Vector[bytes],Failure]:\n    return result_traverse(values,parse)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "required_effects": []
  },
  {
    "id": "T-handler",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    try:\n        return decode(data)\n    except ValueError:\n        return b\"invalid\"\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "required_effects": [],
    "failures": []
  },
  {
    "id": "T-handler-occurrences",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    try:\n        first=decode(data)\n    except ValueError:\n        return b\"invalid\"\n    return encode(first)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "T-generic-factory",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef retain(callback:Callable[[bytes],bytes])->Callable[[bytes],bytes]:\n    def held(data:bytes)->bytes:\n        return callback(data)\n    return held\n@fun\ndef probe(data:bytes)->bytes:\n    selected=retain(encode)\n    return selected(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode"
    ],
    "required_effects": [],
    "failures_contains": [
      "ValueError"
    ]
  },
  {
    "id": "T-latent-captured",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe()->Callable[[bytes],bytes]:\n    selected=compose(digest,encode)\n    def held(data:bytes)->bytes:\n        return selected(data)\n    return held\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "trust_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.sha256_digest"
    ],
    "required_effects": [],
    "failures": []
  },
  {
    "id": "F-native-binascii-encode",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\n@fun\ndef probe(data:bytes)->bytes:\n    return binascii.b2a_base64(data,newline=False)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "F-native-binascii-decode",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\n@fun\ndef probe(data:bytes)->bytes:\n    return binascii.a2b_base64(data,strict_mode=True)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "F-native-sha2",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport _sha2\n@fun\ndef probe(data:bytes)->bytes:\n    return _sha2.sha256(data,usedforsecurity=False).digest()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "F-native-private",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import _exact_bytes\n@fun\ndef probe(data:bytes)->bytes:\n    return _exact_bytes(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "F-native-hashlib",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport hashlib\n@fun\ndef probe(data:bytes)->bytes:\n    return hashlib.sha256(data).digest()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-member",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations as adapter\nadapter.base64_decode=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-private",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations as adapter\nadapter._exact_bytes=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-bound",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport pyalamode.integrations as adapter\nadapter._MAX_BYTES=0\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-code",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode as alias\nalias.__code__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-globals",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\nbase64_encode.__globals__[\"_sha2\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-globals-alias",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\nnamespace=base64_encode.__globals__\nnamespace[\"_MAX_BYTES\"]=0\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-builtins",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\nbase64_encode.__globals__[\"__builtins__\"][\"len\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-builtins-alias",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\nnamespace=base64_encode.__globals__[\"__builtins__\"]\nnamespace[\"bytes\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-adapter-helper-globals",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import _exact_bytes\n_exact_bytes.__globals__[\"_binascii\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-encode",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\nbinascii.b2a_base64=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-decode",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom binascii import a2b_base64 as native\nnative.__dict__.update({\"replacement\":unknown})\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-sha",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport _sha2\n_sha2.sha256=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-digest",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport _sha2\n_sha2.SHA256Type.digest=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-binding",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\nbinascii.Error=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-init",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\nbinascii.Error.__init__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-new",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom binascii import Error as E\nE.__new__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-bases",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom binascii import Error as E\nE.__bases__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-dict",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom binascii import Error as E\nnamespace=E.__dict__\nnamespace.update({\"__init__\":unknown})\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-mro",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\nbase=binascii.Error.__mro__[1]\nbase.__init__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-base-dict",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport binascii\nnamespace=binascii.Error.__bases__[0].__dict__\nnamespace.update({\"__new__\":unknown})\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-native-error-writer-helper",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom binascii import Error as E\ndef replace_error():\n    E.__init__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-sysmodules-native",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport sys\nsys.modules[\"binascii\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-sysmodules-native-alias",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom sys import modules as table\ntable[\"_sha2\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-sysmodules-adapter",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport sys\nsys.modules[\"pyalamode.integrations\"]=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-metapath-writer",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport sys\nsys.meta_path.append(unknown)\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-pathhooks-writer",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom sys import path_hooks as hooks\nhooks.append(unknown)\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-builtin-len",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport builtins\nbuiltins.len=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "W-builtin-valueerror",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nimport builtins\nbuiltins.ValueError.__init__=unknown\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef encode(data:bytes)->bytes:\n    return base64_encode(data)\n@fun\ndef decode(data:bytes)->bytes:\n    return base64_decode(data)\n@fun\ndef digest(data:bytes)->bytes:\n    return sha256_digest(data)\n@fun\ndef probe(data:bytes)->bytes:\n    return digest(decode(encode(data)))\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-explicit-new-core",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"vendor rows\",rationale=\"ordinary mutable integration\")\ndef vendor():\n    return [1,2]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\nraw=vendor()\nsnapshot=freeze(raw,exclusive=True,schema=Vector[int])\nresult=total(snapshot)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "boundary": "total",
    "trust_operations": [],
    "required_effects": [],
    "unsafe_count": 1
  },
  {
    "id": "U-direct",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"vendor rows\",rationale=\"ordinary mutable integration\")\ndef vendor():\n    return [1,2]\n@fun\ndef probe()->Vector[int]:\n    return vendor()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-effectful",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"vendor rows\",rationale=\"ordinary mutable integration\")\ndef vendor():\n    return [1,2]\n@effects(IO,State,Clock,Random,Environment)\ndef probe()->Vector[int]:\n    return vendor()\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-marked",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"vendor rows\",rationale=\"ordinary mutable integration\")\ndef vendor():\n    return [1,2]\n@fun\n@unsafe(scope=\"core\",rationale=\"unchecked\")\ndef probe(data:int)->int:\n    return data\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-no-exclusive",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"vendor rows\",rationale=\"ordinary mutable integration\")\ndef vendor():\n    return [1,2]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\nraw=vendor()\nsnapshot=freeze(raw,schema=Vector[int])\nresult=total(snapshot)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-no-schema",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"vendor rows\",rationale=\"ordinary mutable integration\")\ndef vendor():\n    return [1,2]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\nraw=vendor()\nsnapshot=freeze(raw,exclusive=True)\nresult=total(snapshot)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-marker-empty-scope",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"\",rationale=\"reason\")\ndef vendor():\n    return [1]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-marker-empty-rationale",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=\"scope\",rationale=\"\")\ndef vendor():\n    return [1]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-marker-positional",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(\"scope\",\"reason\")\ndef vendor():\n    return [1]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "U-marker-unknown",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\n@unsafe(scope=unknown,rationale=\"reason\")\ndef vendor():\n    return [1]\n@fun\ndef total(values:Vector[int])->int:\n    def add(acc:int,value:int)->int:\n        return acc+value\n    return values.fold(add,0)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ]
  },
  {
    "id": "A-invalid-unknown-operation",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "vendor.fake"
    }
  },
  {
    "id": "A-invalid-missing-owner",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "owner": null
    }
  },
  {
    "id": "A-invalid-empty-rationale",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "rationale": ""
    }
  },
  {
    "id": "A-invalid-unknown-field",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "extra": "unsupported"
    }
  },
  {
    "id": "A-invalid-bad-expiry",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "expires_at": "2099-01-01"
    }
  },
  {
    "id": "A-invalid-offset-expiry",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "expires_at": "2099-01-01T00:00:00+00:00"
    }
  },
  {
    "id": "A-invalid-uppercase-digest",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "dependency_sha256": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    }
  },
  {
    "id": "A-invalid-short-digest",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode",
      "contract_sha256": "0"
    }
  },
  {
    "id": "A-invalid-duplicate",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode"
    },
    "duplicate_approval": true
  },
  {
    "id": "A-invalid-unknown-policy",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode"
    },
    "policy_extra": {
      "trust_me_pure": true
    }
  },
  {
    "id": "A-invalid-bad-mode",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "approval_mutation": {
      "operation": "pyalamode.integrations.base64_encode"
    },
    "policy_mode": "allow"
  },
  {
    "id": "A-override-reviewed",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [],
      "failures": [
        "ValueError"
      ]
    },
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "required_effects": [],
    "failures": [
      "ValueError"
    ]
  },
  {
    "id": "A-override-draft",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "draft",
      "effects": [],
      "failures": [
        "ValueError"
      ]
    }
  },
  {
    "id": "A-override-effect-undeclared",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [
        "Clock"
      ],
      "failures": [
        "ValueError"
      ]
    }
  },
  {
    "id": "A-override-effect-declared",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@effects(Clock)\ndef probe(data:bytes)->bytes:\n    try:\n        return base64_decode(data)\n    except ValueError:\n        return b\"bad\"\n"
    },
    "expected": 0,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [
        "Clock"
      ],
      "failures": [
        "ValueError"
      ]
    },
    "trust_operations": [
      "pyalamode.integrations.base64_decode"
    ],
    "required_effects": [
      "Clock"
    ],
    "failures": []
  },
  {
    "id": "A-override-unknown-effect",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [
        "Network"
      ],
      "failures": [
        "ValueError"
      ]
    }
  },
  {
    "id": "A-override-remove-failure",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [],
      "failures": []
    }
  },
  {
    "id": "A-override-wrong-base",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [],
      "failures": [
        "ValueError"
      ],
      "base_contract_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  },
  {
    "id": "A-override-unknown-field",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [],
      "failures": [
        "ValueError"
      ],
      "signature": "other"
    }
  },
  {
    "id": "A-override-missing-owner",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_decode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_decode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "override": {
      "operation": "pyalamode.integrations.base64_decode",
      "status": "reviewed",
      "effects": [],
      "failures": [
        "ValueError"
      ],
      "owner": ""
    }
  },
  {
    "id": "N-backend-module",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n",
      "binascii.py": "from pathlib import Path\nPath(\"sentinel\").write_text(\"backend imported\")\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "nonexecuting": true
  },
  {
    "id": "N-backend-package",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n",
      "_sha2/__init__.py": "from pathlib import Path\nPath(\"sentinel\").write_text(\"backend package imported\")\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "nonexecuting": true
  },
  {
    "id": "N-adapter-package",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n",
      "pyalamode/__init__.py": "from pathlib import Path\nPath(\"sentinel\").write_text(\"product package imported\")\n",
      "pyalamode/integrations.py": "from pathlib import Path\nPath(\"sentinel\").write_text(\"adapter imported\")\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "nonexecuting": true
  },
  {
    "id": "N-app-default",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pathlib import Path\ndef sentry():\n    Path(\"sentinel\").write_text(\"executed\")\n    return 1\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes=sentry())->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "nonexecuting": true
  },
  {
    "id": "N-app-decorator",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pathlib import Path\ndef sentry():\n    Path(\"sentinel\").write_text(\"executed\")\n    return 1\nfrom pyalamode.integrations import base64_encode\n@fun\n@sentry()\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "nonexecuting": true
  },
  {
    "id": "N-app-annotation",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pathlib import Path\ndef sentry():\n    Path(\"sentinel\").write_text(\"executed\")\n    return 1\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:sentry())->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 1,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "nonexecuting": true
  },
  {
    "id": "A-manifest-absolute",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "manifest_paths": [
      "/tmp/override.json"
    ]
  },
  {
    "id": "A-manifest-parent",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "manifest_paths": [
      "../override.json"
    ]
  },
  {
    "id": "A-manifest-duplicate",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "manifest_paths": [
      "override.json",
      "override.json"
    ]
  },
  {
    "id": "A-manifest-missing",
    "files": {
      "core.py": "from pyalamode import fun,Vector,OrderedMap,Result,Ok,Err,Failure,failure_value,compose,partial_first,vector_scan,vector_group_by,result_traverse,effects,Effectful,Clock,IO,State,Random,Environment,freeze,unsafe\nfrom typing import Callable\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n"
    },
    "expected": 2,
    "approval_operations": [
      "pyalamode.integrations.base64_encode",
      "pyalamode.integrations.base64_decode",
      "pyalamode.integrations.sha256_digest"
    ],
    "manifest_paths": [
      "absent.json"
    ]
  }
]
```

m08-runtime-inputs.json SHA-256 `60434fd49760244f261621521e757eedc6461544996b746b750a21edc742c0f8`.

```json
[
  {
    "id": "R-encode-",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": ""
    },
    "expected": {
      "hex": ""
    },
    "failure": null
  },
  {
    "id": "R-decode-",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": ""
    },
    "expected": {
      "hex": ""
    },
    "failure": null
  },
  {
    "id": "R-encode-66",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "66"
    },
    "expected": {
      "hex": "5a673d3d"
    },
    "failure": null
  },
  {
    "id": "R-decode-66",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a673d3d"
    },
    "expected": {
      "hex": "66"
    },
    "failure": null
  },
  {
    "id": "R-encode-666f",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "666f"
    },
    "expected": {
      "hex": "5a6d383d"
    },
    "failure": null
  },
  {
    "id": "R-decode-666f",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a6d383d"
    },
    "expected": {
      "hex": "666f"
    },
    "failure": null
  },
  {
    "id": "R-encode-666f6f",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "666f6f"
    },
    "expected": {
      "hex": "5a6d3976"
    },
    "failure": null
  },
  {
    "id": "R-decode-666f6f",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a6d3976"
    },
    "expected": {
      "hex": "666f6f"
    },
    "failure": null
  },
  {
    "id": "R-encode-666f6f62",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "666f6f62"
    },
    "expected": {
      "hex": "5a6d397659673d3d"
    },
    "failure": null
  },
  {
    "id": "R-decode-666f6f62",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a6d397659673d3d"
    },
    "expected": {
      "hex": "666f6f62"
    },
    "failure": null
  },
  {
    "id": "R-encode-666f6f6261",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "666f6f6261"
    },
    "expected": {
      "hex": "5a6d3976596d453d"
    },
    "failure": null
  },
  {
    "id": "R-decode-666f6f6261",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a6d3976596d453d"
    },
    "expected": {
      "hex": "666f6f6261"
    },
    "failure": null
  },
  {
    "id": "R-encode-666f6f626172",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "666f6f626172"
    },
    "expected": {
      "hex": "5a6d3976596d4679"
    },
    "failure": null
  },
  {
    "id": "R-decode-666f6f626172",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a6d3976596d4679"
    },
    "expected": {
      "hex": "666f6f626172"
    },
    "failure": null
  },
  {
    "id": "R-encode-00",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "00"
    },
    "expected": {
      "hex": "41413d3d"
    },
    "failure": null
  },
  {
    "id": "R-decode-00",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41413d3d"
    },
    "expected": {
      "hex": "00"
    },
    "failure": null
  },
  {
    "id": "R-encode-ff",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "ff"
    },
    "expected": {
      "hex": "2f773d3d"
    },
    "failure": null
  },
  {
    "id": "R-decode-ff",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "2f773d3d"
    },
    "expected": {
      "hex": "ff"
    },
    "failure": null
  },
  {
    "id": "R-encode-ffff",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "ffff"
    },
    "expected": {
      "hex": "2f2f383d"
    },
    "failure": null
  },
  {
    "id": "R-decode-ffff",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "2f2f383d"
    },
    "expected": {
      "hex": "ffff"
    },
    "failure": null
  },
  {
    "id": "R-encode-000000",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "hex": "000000"
    },
    "expected": {
      "hex": "41414141"
    },
    "failure": null
  },
  {
    "id": "R-decode-000000",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41414141"
    },
    "expected": {
      "hex": "000000"
    },
    "failure": null
  },
  {
    "id": "R-malformed-3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-3d3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "3d3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-3d3d3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "3d3d3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-4141",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "4141"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-414141",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "414141"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-413d3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "413d3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41413d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41413d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41413d3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41413d3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-414141413d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "414141413d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-414141413d3d3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "414141413d3d3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41413d3d41",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41413d3d41"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41413d3d0a",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41413d3d0a"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-2041413d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "2041413d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41413d3d20",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41413d3d20"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-4141003d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "4141003d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-2d773d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "2d773d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-5f773d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5f773d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-ff414141",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "ff414141"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-5a683d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a683d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-5a6d393d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a6d393d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-41423d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "41423d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-4141423d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "4141423d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-5a673d5a",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a673d5a"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-malformed-5a673d3d3d",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "hex": "5a673d3d3d"
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-encode-boundary",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "repeat_hex": "61",
      "count": 1048576
    },
    "expected": {
      "chunks": [
        {
          "repeat_hex": "59574668",
          "count": 349525
        },
        {
          "hex": "59513d3d"
        }
      ]
    },
    "failure": null
  },
  {
    "id": "R-decode-boundary",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "chunks": [
        {
          "repeat_hex": "59574668",
          "count": 349525
        },
        {
          "hex": "59513d3d"
        }
      ]
    },
    "expected": {
      "repeat_hex": "61",
      "count": 1048576
    },
    "failure": null
  },
  {
    "id": "R-encode-overflow",
    "operation": "pyalamode.integrations.base64_encode",
    "input": {
      "repeat_hex": "61",
      "count": 1048577
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-decode-output-overflow",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "chunks": [
        {
          "repeat_hex": "59574668",
          "count": 349525
        },
        {
          "hex": "5957453d"
        }
      ]
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-decode-input-overflow",
    "operation": "pyalamode.integrations.base64_decode",
    "input": {
      "repeat_hex": "59574668",
      "count": 349526
    },
    "expected": null,
    "failure": "ValueError"
  },
  {
    "id": "R-sha-empty",
    "operation": "pyalamode.integrations.sha256_digest",
    "input": {
      "hex": ""
    },
    "expected": {
      "hex": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "failure": null
  },
  {
    "id": "R-sha-abc",
    "operation": "pyalamode.integrations.sha256_digest",
    "input": {
      "hex": "616263"
    },
    "expected": {
      "hex": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    },
    "failure": null
  },
  {
    "id": "R-sha-million-a",
    "operation": "pyalamode.integrations.sha256_digest",
    "input": {
      "repeat_hex": "61",
      "count": 1000000
    },
    "expected": {
      "hex": "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
    },
    "failure": null
  },
  {
    "id": "R-sha-overflow",
    "operation": "pyalamode.integrations.sha256_digest",
    "input": {
      "repeat_hex": "61",
      "count": 1048577
    },
    "expected": null,
    "failure": "ValueError"
  }
]
```

## Fixed sysconfig-discovery nonexecution supplement

Before this reviewer observes the repair, root approved a scope correction: the supported layout now discovers real native files directly and uses no sysconfig import/getter. Inactive sysconfig name/path/platform selectors and sysconfig/default-data shadows therefore do not alter identity and need not be refused. The initial investigation assumed target2/no-identity; root explicitly replaced that assumption before this reviewer ran any supplement with zero execution plus ordinary denied/current-approved classification from fixed actual installed paths. Missing/unsupported actual layout/version still fails closed. This correction does not weaken the fixed no-execution requirement and is not a response to a reviewer result.

The complete revised supplement uses explicit selector, explicit path, both overrides, default-name PYTHONPATH shadow and default-name project shadow, plus a sysconfig.py module sentinel and unused host-platform selector. Each fresh metadata subprocess must discover real denied identities, instantiate an explicit exact fixture approval, then report approved identities without importing the adapter/backend/config hook. Fresh real console check/audit/build/explain must return 0, preserve the audit distinction, execute zero hooks, and build only the approved artifact. Clean metadata remains denied. These 26 subprocesses are separate from source-case and runtime-input counts.

Harness SHA-256 `841bf69e26811207e21fa9b54dacf7b1f54ce43d625db2dbfe52cacbd43ee9ee`.

```python
import json,os,subprocess,sys,tempfile
from pathlib import Path
from m08_common import sha
OUT=Path(__file__).parent;checks=0;rows=[]
def check(value,label):
 global checks
 checks+=1
 if not value:raise AssertionError(label)
name=f'_sysconfigdata_{sys.abiflags}_{sys.platform}_{getattr(sys.implementation,"_multiarch","")}'
metadata_source='''import json,sys
from pathlib import Path
from pyalamode.integration_contracts import integration_snapshot,operation_contract
from m08_common import prepare
assert operation_contract('base64_encode')['identity']=='pyalamode.integrations.base64_encode'
snapshot=integration_snapshot(root=PROJECT)
assert not Path(SENTINEL).exists()
assert not any(snapshot['inputs'][operation]['admission']=='approved' for operation in snapshot['inputs'])
assert all(row['installed_identity'] and row['admission']=='denied' for row in snapshot['catalog'])
policy,initial=prepare(Path(PROJECT),{'id':'ignored config selectors','files':{'core.py':Path(PROJECT,'core.py').read_text()}})
approved=integration_snapshot(policy,root=PROJECT)
assert all(row['admission']=='approved' and row['installed_identity'] for row in approved['catalog'])
assert not {'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys()
print(json.dumps({'snapshot':snapshot,'approved_snapshot':approved,'backend_modules':sorted({'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys())}))
'''
for profile in ('explicit-name','explicit-path','explicit-both','default-pythonpath-shadow','default-project-shadow'):
 with tempfile.TemporaryDirectory(prefix='m08-config-nonexecution-') as directory:
  root=Path(directory);shadow=root/'shadow';shadow.mkdir();project=root/'project';project.mkdir();sentinel=root/'sentinel'
  (project/'core.py').write_text('from pyalamode import fun\nfrom pyalamode.integrations import base64_encode\n@fun\ndef probe(data:bytes)->bytes:\n    return base64_encode(data)\n')
  hook='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("config imported")\nbuild_time_vars={}\n'
  env=dict(os.environ);env.pop('_PYTHON_SYSCONFIGDATA_NAME',None);env.pop('_PYTHON_SYSCONFIGDATA_PATH',None)
  if profile in ('explicit-name','explicit-both'):
   (shadow/'m08_config_hook.py').write_text(hook);env['_PYTHON_SYSCONFIGDATA_NAME']='m08_config_hook'
  if profile in ('explicit-path','explicit-both'):
   (shadow/(name+'.py')).write_text(hook);env['_PYTHON_SYSCONFIGDATA_PATH']=str(shadow)
  if profile=='default-pythonpath-shadow':(shadow/(name+'.py')).write_text(hook)
  if profile=='default-project-shadow':(project/(name+'.py')).write_text(hook)
  (shadow/'sysconfig.py').write_text(hook)
  env['_PYTHON_HOST_PLATFORM']='m08-unused-host-platform'
  env['PYTHONPATH']=str(shadow)+os.pathsep+str(OUT)+os.pathsep+env.get('PYTHONPATH','')
  cwd=project if profile=='default-project-shadow' else OUT
  source=metadata_source.replace('PROJECT',repr(str(project))).replace('SENTINEL',repr(str(sentinel)))
  ran=subprocess.run([sys.executable,'-c',source],cwd=cwd,env=env,capture_output=True,text=True)
  check(ran.returncode==0,profile+' safe metadata '+ran.stderr);check(not sentinel.exists(),profile+' metadata sentinel zero')
  rows.append({'profile':profile,'action':'metadata','status':ran.returncode,'source':source,'environment_changes':{k:env.get(k) for k in ('_PYTHON_SYSCONFIGDATA_NAME','_PYTHON_SYSCONFIGDATA_PATH','PYTHONPATH')},'hook_source':hook,'hook_filename':name+'.py' if profile!='explicit-name' else 'm08_config_hook.py','stdout':ran.stdout,'stderr':ran.stderr})
  for action,args in [('check',['check','--root',str(project),'--no-cache','--json']),('audit',['check','--root',str(project),'--audit','--no-cache','--json']),('build',['build','--root',str(project),'--output',str(project/'artifact'),'--json']),('explain',['explain','base64_encode'])]:
   ran=subprocess.run([str(Path(sys.executable).parent/'pyalamode'),*args],cwd=cwd,env=env,capture_output=True,text=True)
   check(ran.returncode==0,profile+' '+action+' unused config selectors safely ignored '+ran.stderr);check(not sentinel.exists(),profile+' '+action+' sentinel zero');check((project/'artifact').exists()==(action in {'build','explain'}),profile+' '+action+' correct artifact publication')
   rows.append({'profile':profile,'action':action,'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr})
# Successful clean metadata identity discovery also imports none of the actual
# backend/application modules. It does not create an approval.
clean=r'''import json,sys
from pyalamode.integration_contracts import integration_snapshot
before=set(sys.modules)
snapshot=integration_snapshot()
assert not snapshot['errors']
assert all(row['installed_identity'] and row['admission']=='denied' for row in snapshot['catalog'])
assert not {'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys()
print(json.dumps({'catalog':snapshot['catalog'],'backend_modules':sorted({'pyalamode.integrations','binascii','_sha2'} & (set(sys.modules)-before))}))
'''
ran=subprocess.run([sys.executable,'-c',clean],cwd=OUT,capture_output=True,text=True)
check(ran.returncode==0,'clean nonexecuting real installed discovery '+ran.stderr);rows.append({'profile':'clean','action':'metadata','status':ran.returncode,'source':clean,'stdout':ran.stdout,'stderr':ran.stderr})
report={'inputs':{'m08_nonexecution_probe.py':sha(__file__)},'assertions':checks,'rows':rows,'default_config_name':name,'clean_literal_source':clean}
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-nonexecution-observations.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows)}))
```

## Complete fixed executable harnesses before readiness

The source, runtime, project/cache/expiry, actual CLI/artifact/console and real copied-interpreter/product/native-identity probes below were completed and syntax-checked before this reviewer observed readiness. They create only outside-checkout fixtures. Exact inherited inventory reconciliation: the M7 freshness harness assertion `len(old["identities"]) == 14` becomes 16 for the two actual new product files, with its label updated; behavior and literal source expectations remain fixed. Final installed inventories count 17 Python files rather than the predecessor 15. The complete revised freshness text is included here. Restoring exactly earlier dependency bytes may legitimately reuse an earlier current cache entry; it is not required to be a miss.

```json
{
  "m08_common.py": "import hashlib,json\nfrom pathlib import Path\nCANON=['pyalamode.integrations.'+n for n in ('base64_encode','base64_decode','sha256_digest')]\nOWNER='M8 independent reviewer'\ndef sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()\ndef digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()\ndef write_files(root,files):\n for name,source in files.items():\n  path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source)\ndef toml(value):\n if type(value) is str:return json.dumps(value)\n if type(value) is bool:return 'true' if value else 'false'\n if type(value) is int:return str(value)\n if type(value) is list:return '['+','.join(toml(x) for x in value)+']'\n raise TypeError(type(value))\ndef policy_text(policy):\n lines=['[tool.pyalamode]']\n for key,value in policy.items():\n  if key not in ('integration_approvals','effect_bounds'):lines.append(key+'='+toml(value))\n if policy.get('effect_bounds'):\n  lines.append('[tool.pyalamode.effect_bounds]')\n  for key,value in policy['effect_bounds'].items():lines.append(toml(key)+'='+toml(value))\n for approval in policy.get('integration_approvals',[]):\n  lines.append('[[tool.pyalamode.integration_approvals]]')\n  lines.extend(key+'='+toml(value) for key,value in approval.items())\n return '\\n'.join(lines)+'\\n'\ndef prepare(root,case):\n from pyalamode.integration_contracts import operation_contract,integration_snapshot\n write_files(root,case['files'])\n policy={'schema':1,'external_trust':case.get('policy_mode','approved')}\n if case.get('mode'):\n  policy.update(boundary_guards=case['mode'])\n  if case['mode']!='off':policy['guarded_exports']=['core:probe']\n if case.get('override'):\n  options=dict(case['override']);operation=options['operation'];base=operation_contract(operation)\n  row={'schema':1,'operation':operation,'status':'reviewed','base_contract_sha256':digest(base),'effects':[],'failures':['ValueError'],'owner':'M8 manifest reviewer','rationale':'fixed conservative review fixture','provenance':'Docs/conformance/m08-cases.md override fixture',**options}\n  (root/'override.json').write_text(json.dumps(row,indent=2)+'\\n');policy['integration_manifests']=['override.json']\n if 'manifest_paths' in case:policy['integration_manifests']=case['manifest_paths']\n snapshot=integration_snapshot(policy,root=root)\n catalog={row['identity']:row for row in snapshot['catalog']}\n policy['integration_approvals']=[]\n for operation in case.get('approval_operations',CANON):\n  row=catalog[operation]\n  policy['integration_approvals'].append({'operation':operation,'contract_sha256':row['contract_sha256'],'dependency_sha256':row['dependency_sha256'] or '0'*64,'owner':OWNER,'rationale':'fixed independently reviewed M8 conformance contract','provenance':'Docs/conformance/m08-cases.md literal '+case['id'],'expires_at':'2999-01-01T00:00:00Z'})\n mutation=case.get('approval_mutation')\n if mutation:\n  target=mutation.get('operation',CANON[0]);entry=next((a for a in policy['integration_approvals'] if a['operation']==target),policy['integration_approvals'][0])\n  for key,value in mutation.items():\n   if value is None:entry.pop(key,None)\n   else:entry[key]=value\n if case.get('approval_remove_expiry'):\n  for entry in policy['integration_approvals']:entry.pop('expires_at',None)\n if case.get('duplicate_approval'):policy['integration_approvals'].append(dict(policy['integration_approvals'][0]))\n policy.update(case.get('policy_extra',{}))\n (root/'pyproject.toml').write_text(policy_text(policy))\n return policy,snapshot\n\ndef reduced(result):\n return {'status':result.status,'verified':result.verified,'tooling':[d.__dict__ for d in result.tooling],'files':[{'path':Path(f.path).name,'status':f.status,'verified':f.verified,'cache_hit':f.cache_hit,'fingerprint':f.fingerprint,'initialization_evidence':f.initialization_evidence,'initialization_failures':f.initialization_failures,'diagnostics':[d.__dict__ for d in f.diagnostics],'setup_observations':f.setup_observations,'unsafe_adapters':f.unsafe_adapters,'integration_inputs':f.integration_inputs,'contracts':[c.__dict__ for c in f.contracts]} for f in result.results]}\n",
  "m08_static_probe.py": "import json,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.project import check_paths\nfrom m08_common import prepare,reduced,sha,OWNER\nOUT=Path(__file__).parent;rows=[];checks=0\ndef check(value,label,problems):\n global checks\n checks+=1\n if not value:problems.append(label)\nfor case in json.loads((OUT/'m08-literal-cases.json').read_text()):\n with tempfile.TemporaryDirectory(prefix='m08-literal-') as directory:\n  root=Path(directory);policy,snapshot=prepare(root,case)\n  result=check_paths(root=root,cache=False);problems=[]\n  check(result.status==case['expected'],'status',problems)\n  check(result.verified==(case['expected']==0),'verified dimension',problems)\n  check(not (root/'sentinel').exists(),'nonexecuting sentinel',problems)\n  file=next((f for f in result.results if Path(f.path).name=='core.py'),None)\n  contract=next((c for c in file.contracts if c.name==case.get('boundary','probe')),None) if file else None\n  if not case['expected']:\n   check(contract is not None,'selected boundary',problems)\n   if contract:\n    for field in ('failures','required_effects'):\n     if field in case:check(sorted(case[field])==getattr(contract,field),field,problems)\n    if 'failures_contains' in case:check(set(case['failures_contains'])<=set(contract.failures),'known failure retained',problems)\n    assumptions=contract.external_assumptions\n    check(set(case.get('trust_operations',[]))=={a['identity'] for a in assumptions},'complete exact external trust',problems)\n    for assumption in assumptions:\n     operation=assumption['identity'];approval=next(a for a in policy['integration_approvals'] if a['operation']==operation)\n     check(assumption['contract_sha256']==approval['contract_sha256'] and assumption['dependency_sha256']==approval['dependency_sha256'],'exact operation/artifact approval',problems)\n     check(assumption['approval']==approval and approval['owner']==OWNER,'visible review/expiry/provenance',problems)\n     check(assumption['admission']=='approved','current approval',problems)\n     check(assumption['installed_identity']['version']=='3.13.1','actual installed version',problems)\n     check(assumption['initialization']['effects']==['IO'],'setup separate from pure invocation',problems)\n     check('opaque' in assumption['source_evidence'],'opaque source evidence',problems)\n    if 'initializer' in case:check(file.initialization_evidence==case['initializer'],'unchecked ordinary initialization',problems)\n    if case.get('external_setup'):check(any(s['identity']=='pyalamode.integrations import' and s['effects']==['IO'] and s['phase']=='ordinary external import setup' for s in file.setup_observations),'visible external setup',problems)\n   if 'unsafe_count' in case:check(len(file.unsafe_adapters)==case['unsafe_count'],'unsafe declaration remains ordinary',problems)\n  rows.append({'id':case['id'],'expected':case['expected'],'observed':result.status,'problems':problems,'policy':policy,'discovery_before':snapshot,'report':reduced(result)})\nreport={'inputs':{'m08-literal-cases.json':sha(OUT/'m08-literal-cases.json'),'m08_static_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py')},'assertions':checks,'rows':rows,'unexpected':[{'id':r['id'],'problems':r['problems'],'diagnostics':[d['reason'] for f in r['report']['files'] for d in f['diagnostics']]} for r in rows if r['problems']]}\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-static-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'cases':len(rows),'assertions':checks,'unexpected':report['unexpected']}))\nraise SystemExit(bool(report['unexpected']))\n",
  "m08_runtime_probe.py": "import codecs,hashlib,json,subprocess,sys,tempfile\nfrom pathlib import Path\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\nfrom pyalamode import Vector,freeze,thaw,fun,unsafe\nfrom m08_common import sha\nOUT=Path(__file__).parent;checks=0;rows=[];hooks=[]\ndef sha_bytes(raw):return hashlib.sha256(raw).hexdigest()\nOPERATIONS={'pyalamode.integrations.base64_encode':base64_encode,'pyalamode.integrations.base64_decode':base64_decode,'pyalamode.integrations.sha256_digest':sha256_digest}\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\ndef data(row):\n if 'hex' in row:return bytes.fromhex(row['hex'])\n if 'repeat_hex' in row:return bytes.fromhex(row['repeat_hex'])*row['count']\n return b''.join(data(part) for part in row['chunks'])\nfor case in json.loads((OUT/'m08-runtime-inputs.json').read_text()):\n operation=OPERATIONS[case['operation']];raw=data(case['input']);failure=None\n try:observed=operation(raw)\n except Exception as error:\n  failure=type(error).__name__;observed=None\n  check(type(error) is ValueError,case['id']+' exact failure class')\n  check(error.__context__ is None and error.__cause__ is None,case['id']+' no native exception state')\n check(failure==case['failure'],case['id']+' failure classification')\n if failure is None:check(type(observed) is bytes and observed==data(case['expected']),case['id']+' exact known answer')\n rows.append({'id':case['id'],'failure':failure,'input_length':len(raw),'input_sha256':sha_bytes(raw),'output_length':len(observed) if observed is not None else None,'output_sha256':sha_bytes(observed) if observed is not None else None})\nclass Foreign:\n def __getattribute__(self,name):hooks.append('getter');return object.__getattribute__(self,name)\n def __iter__(self):hooks.append('iter');return iter(())\n def __str__(self):hooks.append('str');return 'foreign'\n def __repr__(self):hooks.append('repr');return 'foreign'\n def __bytes__(self):hooks.append('bytes');return b''\n def __len__(self):hooks.append('len');return 0\n def __bool__(self):hooks.append('bool');return False\n def __index__(self):hooks.append('index');return 0\n def __eq__(self,other):hooks.append('eq');return True\n def __hash__(self):hooks.append('hash');return 0\n def __reduce__(self):hooks.append('reduce');return (bytes,())\nclass Binary(bytes):\n def __getattribute__(self,name):hooks.append('subclass getter');return super().__getattribute__(name)\n def __len__(self):hooks.append('subclass len');return 0\n def __eq__(self,other):hooks.append('subclass eq');return True\ninvalid=[None,True,1,'',(),[],{},bytearray(b'abc'),memoryview(b'abc'),Foreign(),Binary(b'abc'),lambda:b'abc',Vector.of(b'abc')]\nhooks.clear()\nfor name,operation in OPERATIONS.items():\n for i,value in enumerate(invalid):\n  try:operation(value)\n  except TypeError as error:check(type(error) is TypeError,name+' invalid exact failure')\n  else:raise AssertionError(name+' invalid admitted '+str(i))\n  check(hooks==[],name+' invalid no foreign hooks')\n for label,call in [('missing',lambda operation=operation:operation()),('extra',lambda operation=operation:operation(b'',b'')),('keyword',lambda operation=operation:operation(data=b''))]:\n  try:call()\n  except TypeError:check(True,name+' '+label)\n  else:raise AssertionError(name+' unsupported signature '+label)\nraw=[1,2];alias=raw\n@unsafe(scope='mutable vendor rows',rationale='ordinary adapter fixture')\ndef vendor():return raw\n@fun\ndef total(values):return values[0]+values[1]\ncheck(unsafe(scope='identity',rationale='identity marker')(vendor) is vendor,'unsafe identity marker returns same function')\ncheck(fun(total) is total and total.__dict__=={},'ordinary fun marker adds no evidence/registration')\nsnapshot=freeze(vendor(),exclusive=True,schema=Vector[int]);alias[0]=99\ncheck(snapshot==Vector.of(1,2) and total(snapshot)==3,'new calculation uses isolated validated snapshot')\nexport=thaw(snapshot);export[1]=77;check(snapshot==Vector.of(1,2),'fresh export preserves new core input')\nfor raw,kwargs in [([1],{'schema':Vector[int]}),([[1]],{'exclusive':True,'schema':Vector[int]}),(Binary(b'abc'),{'exclusive':True})]:\n try:freeze(raw,**kwargs)\n except (TypeError,ValueError):check(True,'invalid snapshot refuses')\n else:raise AssertionError('invalid snapshot admitted')\ncheck(hooks==[],'boundary conversions reject hooks')\n# Deliberately violate mutable native Error dependencies in isolated ordinary\n# processes. This demonstrates the assumption; it creates no checked claim.\nconstructor_probe=r'''import binascii,json\nfrom pyalamode.integrations import base64_decode\nhits=[]\noriginal=binascii.Error.__init__\ndef changed(self,*args):\n hits.append('init');original(self,*args)\nbinascii.Error.__init__=changed\ntry:base64_decode(b'!')\nexcept ValueError as error:\n assert type(error) is ValueError and error.__context__ is None and error.__cause__ is None\nelse:raise AssertionError('malformed decode admitted')\nassert hits==['init']\nprint(json.dumps({'hits':hits,'failure':'ValueError','context':None,'cause':None}))\n'''\nbases_probe=r'''import binascii,json\nfrom pyalamode.integrations import base64_decode\nhits=[]\nclass ChangedBase(ValueError):\n __slots__=()\n def __init__(self,*args):hits.append('base init');ValueError.__init__(self,*args)\nbinascii.Error.__bases__=(ChangedBase,)\ntry:base64_decode(b'!')\nexcept ValueError as error:\n assert type(error) is ValueError and error.__context__ is None and error.__cause__ is None\nelse:raise AssertionError('malformed decode admitted')\nassert hits==['base init']\nprint(json.dumps({'hits':hits,'failure':'ValueError','context':None,'cause':None}))\n'''\nregistry_probe=r'''import codecs,hashlib,json\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\nhits=[]\ndef changed(error):hits.append('codec');return ('replacement',error.end)\ncodecs.register_error('strict',changed)\ncodecs.register_error('surrogateescape',changed)\nhashlib.sha256=lambda value:hits.append('hashlib')\nassert base64_encode(b'abc')==b'YWJj'\nassert base64_decode(b'YWJj')==b'abc'\nassert sha256_digest(b'abc').hex()=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'\ntry:base64_decode(b'!')\nexcept ValueError:pass\nelse:raise AssertionError('invalid decode admitted')\nassert hits==[]\nprint(json.dumps({'hooks':hits,'checks':4}))\n'''\nprocesses=[]\nfor label,source in [('native mutable Error constructor',constructor_probe),('native mutable Error compatible base',bases_probe),('unselected codec/hashlib registry independence',registry_probe)]:\n ran=subprocess.run([sys.executable,'-c',source],cwd=OUT,capture_output=True,text=True)\n check(ran.returncode==0,label+' isolated process '+ran.stderr);processes.append({'label':label,'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'source':source})\nreport={'inputs':{'m08-runtime-inputs.json':sha(OUT/'m08-runtime-inputs.json'),'m08_runtime_probe.py':sha(__file__)},'assertions':checks,'literal_rows':rows,'isolated_processes':processes,'hooks':hooks,'unsafe_core_result':3}\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-runtime-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'literal_rows':len(rows),'assertions':checks,'subprocesses':len(processes),'hooks':hooks}))\n",
  "m08_project_probe.py": "import copy,json,time,sys,tempfile\nfrom datetime import datetime,timezone,timedelta\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\nfrom pyalamode.integration_contracts import integration_snapshot\nfrom m08_common import prepare,policy_text,reduced,sha,CANON\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\ndef observe(root,label,status,cache=True):\n result=check_paths(root=root,cache=cache);check(result.status==status,label+' status '+str(result.status));check(not (root/'sentinel').exists(),label+' sentinel absent')\n rows.append({'label':label,'report':reduced(result)});return result\nfiles={'adapter.py':'from pyalamode import fun\\nfrom pyalamode.integrations import base64_encode,sha256_digest\\n@fun\\ndef encode(data:bytes)->bytes:\\n    return base64_encode(data)\\n@fun\\ndef digest(data:bytes)->bytes:\\n    return sha256_digest(data)\\n','core.py':'from pyalamode import fun,compose\\nfrom adapter import encode,digest\\n@fun\\ndef probe(data:bytes)->bytes:\\n    return compose(digest,encode)(data)\\n','plain.py':'from pyalamode import fun\\n@fun\\ndef plain(value:int)->int:\\n    return value+1\\n'}\nwith tempfile.TemporaryDirectory(prefix='m08-project-') as directory:\n root=Path(directory);policy,discovery=prepare(root,{'id':'project closure','files':files})\n cold=observe(root,'cold',0);warm=observe(root,'full warm',0)\n check(all(f.cache_hit for f in warm.results),'full warm actual hits')\n check([c.__dict__ for f in cold.results for c in f.contracts]==[c.__dict__ for f in warm.results for c in f.contracts],'cold/warm exact detached contracts')\n probe=next(c for f in warm.results for c in f.contracts if c.name=='probe')\n check({a['identity'] for a in probe.external_assumptions}=={CANON[0],CANON[2]},'cross-module composed trust')\n (root/'plain.py').write_text(files['plain.py'].replace('value+1','value+2'))\n partial=observe(root,'partial unrelated source edit',0)\n check({Path(f.path).name:f.cache_hit for f in partial.results}=={'adapter.py':True,'core.py':True,'plain.py':False},'partial exact unaffected evidence')\n no_cache=observe(root,'no cache same source',0,False)\n check([c.__dict__ for f in partial.results for c in f.contracts]==[c.__dict__ for f in no_cache.results for c in f.contracts],'partial/no-cache evidence equality')\n # Actual expiration without changing policy bytes: do not infer expiry from a\n # mere changed-policy cache miss. Wait outside all measurement intervals.\n expiry=(datetime.now(timezone.utc)+timedelta(seconds=3)).replace(microsecond=0)\n for approval in policy['integration_approvals']:approval['expires_at']=expiry.strftime('%Y-%m-%dT%H:%M:%SZ')\n (root/'pyproject.toml').write_text(policy_text(policy))\n expiring=observe(root,'approved before real UTC expiry',0);observe(root,'approved full warm before expiry',0)\n before_policy=sha(root/'pyproject.toml')\n delay=(expiry-datetime.now(timezone.utc)).total_seconds()\n if delay>0:time.sleep(delay+0.02)\n expired=observe(root,'same bytes actual expired warm',1)\n check(sha(root/'pyproject.toml')==before_policy,'expiry invalidation with identical policy bytes')\n check(any(not f.cache_hit for f in expired.results if Path(f.path).name in {'adapter.py','core.py'}),'expired relevant body cannot reuse approval hit')\n observe(root,'expired full warm refusal',1);observe(root,'expired no-cache refusal',1,False)\n (root/'plain.py').write_text(files['plain.py'].replace('value+1','value+3'))\n observe(root,'expired partial warm refusal',1)\n built=build_paths(root=root,output=root/'artifact');check(built.status==1 and not (root/'artifact').exists(),'expired build has no artifact')\n rows.append({'label':'expired build','report':reduced(built)})\n # Exact override manifest byte/provenance invalidation is distinct from expiry.\n override_case={'id':'manifest freshness','files':{'core.py':'from pyalamode import effects,Clock\\nfrom pyalamode.integrations import base64_decode\\n@effects(Clock)\\ndef probe(data:bytes)->bytes:\\n    try:\\n        return base64_decode(data)\\n    except ValueError:\\n        return b\"bad\"\\n'},'override':{'operation':CANON[1],'status':'reviewed','effects':['Clock'],'failures':['ValueError']}}\nwith tempfile.TemporaryDirectory(prefix='m08-manifest-') as directory:\n root=Path(directory);policy,snapshot=prepare(root,override_case)\n observe(root,'reviewed conservative override cold',0);warm=observe(root,'reviewed override warm',0)\n contract=next(c for f in warm.results for c in f.contracts if c.name=='probe')\n check(contract.required_effects==['Clock'] and contract.failures==[],'handled failure retains performed conservative Clock effect')\n check(contract.external_assumptions[0]['failures']==['ValueError'] and contract.external_assumptions[0]['effects']==['Clock'],'catalog failure/effect dimensions stay visible despite handler')\n original=(root/'override.json').read_text();(root/'override.json').write_text(original+'\\n')\n observe(root,'actual override bytes changed stale',1);observe(root,'stale manifest no-cache',1,False)\n built=build_paths(root=root,output=root/'artifact');check(built.status==1 and not (root/'artifact').exists(),'stale manifest build no artifact')\n # Explicit reapproval of the changed manifest remains a visible new approval.\n snapshot=integration_snapshot(policy,root=root);new=next(r for r in snapshot['catalog'] if r['identity']==CANON[1])\n entry=next(a for a in policy['integration_approvals'] if a['operation']==CANON[1]);old_digest=entry['contract_sha256'];entry['contract_sha256']=new['contract_sha256']\n check(old_digest!=entry['contract_sha256'],'actual manifest bytes participate in contract identity')\n (root/'pyproject.toml').write_text(policy_text(policy));observe(root,'explicit changed override reapproval',0)\nreport={'inputs':{'m08_project_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py')},'assertions':checks,'literal_layout':files,'literal_override_layout':override_case,'rows':rows}\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-project-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'assertions':checks,'recorded_rows':len(rows),'expiry_delay_seconds':delay}))\n",
  "m08_cli_probe.py": "import json,os,subprocess,sys,tempfile\nfrom pathlib import Path\nfrom m08_common import prepare,sha,CANON\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\ndef call(root,label,args,status,console=False):\n executable=[str(Path(sys.executable).parent/'pyalamode')] if console else [sys.executable,'-m','pyalamode']\n ran=subprocess.run([*executable,*args],cwd=root,capture_output=True,text=True)\n check(ran.returncode==status,label+' status '+str(ran.returncode)+' '+ran.stderr)\n rows.append({'label':label,'command':[*executable,*args],'cwd':str(root),'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr})\n return json.loads(ran.stdout) if '--json' in args else None\nsource='from pyalamode import fun\\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\\n@fun\\ndef probe(data:bytes)->tuple[bytes,bytes]:\\n    encoded=base64_encode(data)\\n    restored=base64_decode(encoded)\\n    return encoded,sha256_digest(restored)\\n'\nstock_source=r'''import json\nfrom pathlib import Path\nimport core\nfrom pyalamode import unsafe,fun\nartifact=Path.cwd().resolve()\nassert Path(core.__file__).resolve().is_relative_to(artifact)\nexpected=(b'YWJj',bytes.fromhex('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'))\nassert core.probe(b'abc')==expected\nassert core.probe.__dict__=={}\nassert fun(core.probe) is core.probe\nchecks=4\nmode=MODE\nif mode!='off':\n from pyalamode_exports.core import probe\n assert probe.__wrapped__ is core.probe\n assert probe(b'abc')==expected\n checks+=2\n original=core.probe.__code__\n def body(data):\n  Path('body-sentinel').write_text('entered')\n  return (b'',b'')\n core.probe.__code__=body.__code__\n class Binary(bytes):pass\n for value in (Binary(b'abc'),bytearray(b'abc'),memoryview(b'abc'),True):\n  try:probe(value)\n  except TypeError as error:\n   assert 'core:probe' in str(error) and 'core.py:' in str(error) and 'argument data' in str(error)\n  else:raise AssertionError('invalid selected export admitted')\n  assert not Path('body-sentinel').exists()\n  checks+=2\n core.probe.__code__=original\n if mode=='debug':\n  try:core.probe(Binary(b'abc'))\n  except TypeError as error:assert 'argument data' in str(error)\n  else:raise AssertionError('debug original entry admitted subtype')\n  checks+=1\nprint(json.dumps({'assertions':checks,'module_file':core.__file__,'artifact':str(artifact),'mode':mode,'result_hex':[x.hex() for x in expected]}))\n'''\nfor mode in ('off','exports','debug'):\n with tempfile.TemporaryDirectory(prefix='m08-cli-artifact-') as directory:\n  root=Path(directory);policy,snapshot=prepare(root,{'id':'CLI '+mode,'files':{'core.py':source},'mode':mode})\n  checked=call(root,mode+' strict check',['check','--root',str(root),'--no-cache','--json'],0)\n  check(checked['verified'],mode+' strict verified dimension')\n  audited=call(root,mode+' audit',['check','--root',str(root),'--audit','--no-cache','--json'],0)\n  check(not audited['verified'],mode+' audit no strict certificate')\n  artifact=root/'artifact';built=call(root,mode+' build',['build','--root',str(root),'--output',str(artifact),'--json'],0)\n  evidence=json.loads((artifact/'pyalamode-evidence.json').read_text())\n  check(built['verified'] and built['boundary_guards']==mode,mode+' build guard dimension')\n  check(len(evidence['files'][0]['contracts'][0]['external_assumptions'])==3,mode+' artifact keeps all three exact assumptions')\n  if mode in ('off','exports'):check((artifact/'core.py').read_text()==source,mode+' copied source bytes identical')\n  env=dict(os.environ);env['PYTHONPATH']=str(artifact)+os.pathsep+env.get('PYTHONPATH','')\n  script=stock_source.replace('MODE',repr(mode));ran=subprocess.run([sys.executable,'-c',script],cwd=artifact,env=env,capture_output=True,text=True)\n  check(ran.returncode==0,mode+' actual stock artifact execution '+ran.stderr)\n  value=json.loads(ran.stdout);check(Path(value['module_file']).resolve().is_relative_to(artifact),mode+' actual module file inside output')\n  rows.append({'label':mode+' actual stock execution','command':[sys.executable,'-c',script],'cwd':str(artifact),'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'artifact_product':evidence.get('product_artifacts'),'assertions':value['assertions']})\ncases={row['id']:row for row in json.loads((OUT/'m08-literal-cases.json').read_text())}\nnegative_ids=('E01-deny','E01-missing','E01-wrong-contract','E01-wrong-dependency','E01-expired','A-override-draft','A-override-effect-undeclared','W-native-error-init','W-adapter-globals','W-sysmodules-native','U-direct','U-effectful','U-marked','N-backend-module','N-app-default','N-app-decorator','N-app-annotation','A-invalid-bad-expiry','A-manifest-parent')\nfor id in negative_ids:\n case=cases[id]\n with tempfile.TemporaryDirectory(prefix='m08-cli-refusal-') as directory:\n  root=Path(directory);prepare(root,case);status=case['expected']\n  call(root,id+' check',['check','--root',str(root),'--json'],status)\n  call(root,id+' audit',['check','--root',str(root),'--audit','--json'],2 if status==2 else 0)\n  call(root,id+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],status)\n  check(not (root/'artifact').exists(),id+' failed gate has no artifact');check(not (root/'sentinel').exists(),id+' no application/dependency execution')\nwith tempfile.TemporaryDirectory(prefix='m08-real-console-') as directory:\n root=Path(directory);prepare(root,cases['E01-direct'])\n value=call(OUT,'real installed console entrypoint',['check','--root',str(root),'--json','--no-cache'],0,True)\n check(value['verified'],'console entrypoint verifies actual selected source')\n check(any(c['external_assumptions'][0]['identity']==CANON[0] for f in value['files'] for c in f['contracts'] if c['name']=='probe'),'console actual Base64 assumption visible')\n check(not (root/'sentinel').exists(),'console no sentinel')\n for symbol in ('base64_encode','base64_decode','sha256_digest','unsafe','PAL350','PAL351'):\n  call(OUT,'explain '+symbol,['explain',symbol],0)\n entry=root/'entry.py';entry.write_text('from core import probe\\nprint(probe(b\"abc\"))\\n')\n ran=subprocess.run([sys.executable,'-m','pyalamode','run',str(entry),'--root',str(root)],cwd=OUT,capture_output=True,text=True)\n check(ran.returncode==2,'optional run remains unsupported');check(not (root/'artifact').exists(),'unsupported run creates no artifact')\n rows.append({'label':'optional run unsupported','status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr})\nreport={'inputs':{'m08_cli_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py'),'m08-literal-cases.json':sha(OUT/'m08-literal-cases.json')},'assertions':checks,'rows':rows,'literal_artifact_source':source,'literal_stock_source':stock_source,'negative_ids':negative_ids}\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-cli-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows)}))\n",
  "m08_identity_probe.py": "import json,os,shutil,subprocess,sys,tempfile,time\nfrom pathlib import Path\nimport pyalamode\nfrom m08_common import sha\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\n# Actual interpreter/home/native/product copies; shared installations are never\n# edited. Copied core bytes stay identical to the actual loaded core foundation.\nsource=r'''import json,sys\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\nfrom pyalamode.integration_contracts import integration_snapshot\nfrom pyalamode.model import foundation_identities\nroot=Path(PROJECT)\nresult=build_paths(root=root,output=root/'artifact') if BUILD else check_paths(root=root,cache=CACHE)\nprint(json.dumps({'status':result.status,'verified':result.verified,'hits':{Path(f.path).name:f.cache_hit for f in result.results},'snapshot':integration_snapshot(root=root),'product':foundation_identities(),'contracts':[c.__dict__ for f in result.results for c in f.contracts],'artifact_exists':(root/'artifact').exists(),'tooling':[d.__dict__ for d in result.tooling],'diagnostics':[d.__dict__ for f in result.results for d in f.diagnostics],'native_loaded':sorted({'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys())}))\n'''\napproval_source=r'''import json\nfrom pathlib import Path\nfrom m08_common import prepare\nroot=Path(PROJECT)\npolicy,snapshot=prepare(root,{'id':'real copied installed identity','files':{'core.py':root.joinpath('core.py').read_text()}})\nprint(json.dumps({'policy':policy,'snapshot':snapshot}))\n'''\nruntime_source=r'''import json\nfrom pathlib import Path\nimport binascii,_sha2\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\nassert Path(binascii.__file__).resolve().is_relative_to(Path(HOME))\nassert Path(_sha2.__file__).resolve().is_relative_to(Path(HOME))\nassert base64_encode(b'abc')==b'YWJj'\nassert base64_decode(b'YWJj')==b'abc'\nassert sha256_digest(b'abc').hex()=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'\nprint(json.dumps({'binascii_file':binascii.__file__,'sha2_file':_sha2.__file__,'checks':5}))\n'''\nfixture='from pyalamode import fun\\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\\n@fun\\ndef probe(data:bytes)->bytes:\\n    return sha256_digest(base64_decode(base64_encode(data)))\\n'\nwith tempfile.TemporaryDirectory(prefix='m08-real-runtime-copy-') as directory:\n root=Path(directory);home=root/'runtime';stdlib=home/'lib/python3.13';stdlib.parent.mkdir(parents=True)\n shutil.copytree(Path(sys.base_prefix)/'lib/python3.13',stdlib,ignore=shutil.ignore_patterns('site-packages','__pycache__'))\n (home/'bin').mkdir();interpreter=home/'bin/python';shutil.copy2(Path(sys.executable).resolve(),interpreter)\n core_original=Path(sys.base_prefix)/('Python' if sys.platform=='darwin' else 'lib/libpython3.13.so.1.0')\n core_copy=home/('Python' if sys.platform=='darwin' else 'lib/libpython3.13.so.1.0');shutil.copy2(core_original,core_copy)\n shutil.copytree(Path(pyalamode.__file__).parent,root/'product/pyalamode',ignore=shutil.ignore_patterns('__pycache__'))\n project=root/'project';project.mkdir();(project/'core.py').write_text(fixture)\n env=dict(os.environ);env['PYTHONHOME']=str(home);env['PYTHONPATH']=str(root/'product')+os.pathsep+str(OUT)\n for key in ('_PYTHON_SYSCONFIGDATA_NAME','_PYTHON_SYSCONFIGDATA_PATH','_PYTHON_HOST_PLATFORM'):env.pop(key,None)\n def call(label,program,status=0):\n  ran=subprocess.run([str(interpreter),'-S','-c',program],cwd=OUT,env=env,capture_output=True,text=True)\n  check(ran.returncode==status,label+' copied actual interpreter process '+ran.stderr)\n  value=json.loads(ran.stdout) if ran.returncode==0 else None\n  rows.append({'label':label,'process_status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'source':program,'value':value});return value\n def approve(label):return call(label,approval_source.replace('PROJECT',repr(str(project))))\n def observe(label,status,hits=None,cache=True,build=False):\n  program=source.replace('PROJECT',repr(str(project))).replace('BUILD',repr(build)).replace('CACHE',repr(cache));value=call(label,program)\n  check(value['status']==status,label+' exact check/build status '+str(value['status']))\n  if hits is not None:check(value['hits']=={'core.py':hits},label+' exact cache hit')\n  check(not value['native_loaded'],label+' no backend/adaptor execution during discovery/check/build')\n  if status:check(not value['artifact_exists'],label+' failed gate no artifact')\n  return value\n approved=approve('copied home explicit real installed approval')\n baseline=observe('copied home approved cold',0,False);warm=observe('copied home approved full warm',0,True)\n check(baseline['contracts']==warm['contracts'],'copied home cold/warm exact external trust')\n identity=approved['snapshot']['catalog'][0]['installed_identity'];native={name:Path(value['path']) for name,value in identity['native_artifacts'].items()}\n check(all(path.is_relative_to(home) for path in native.values()),'fixed discovery resolves actual copied native artifacts')\n check(identity['interpreter_executable']['path']==str(interpreter.resolve()) and identity['interpreter_core']['path']==str(core_copy.resolve()),'copied executable/core identities are explicit')\n original_native={name:{'path':str(path),'sha256':sha(path)} for name,path in native.items()}\n shared_native={name:{'path':str(Path(sys.base_prefix)/'lib/python3.13/lib-dynload'/path.name),'sha256':sha(Path(sys.base_prefix)/'lib/python3.13/lib-dynload'/path.name)} for name,path in native.items()}\n for name,path in native.items():\n  original=path.read_bytes();path.write_bytes(original+b'\\nM8 independent harmless artifact byte change\\n')\n  check(sha(path)!=original_native[name]['sha256'],name+' real installed bytes changed')\n  changed=observe(name+' changed artifact stale warm',1,False)\n  observe(name+' changed artifact stale full warm',1,True)\n  observe(name+' changed artifact stale no-cache',1,False,False)\n  observe(name+' changed artifact rejected build',1,None,False,True)\n  refreshed=approve(name+' explicit changed-artifact reapproval')\n  accepted=observe(name+' changed-artifact reapproved cold',0,False);observe(name+' changed-artifact reapproved warm',0,True)\n  check(accepted['contracts'][0]['external_assumptions'][0]['dependency_sha256']!=baseline['contracts'][0]['external_assumptions'][0]['dependency_sha256'],name+' actual new identity propagated transitively')\n  call(name+' actual changed native artifact invocation',runtime_source.replace('HOME',repr(str(home))))\n  path.write_bytes(original);approve(name+' explicit restored original reapproval');baseline=observe(name+' restored artifact current',0)\n # Missing supported installed file cannot return a valid-looking identity.\n missing=native['binascii'];saved=missing.with_name(missing.name+'.saved');missing.rename(saved)\n observe('real supported native artifact missing',1,False);observe('missing artifact no-cache',1,False,False);observe('missing artifact rejected build',1,None,False,True)\n saved.rename(missing);approve('restored missing artifact explicit current approval');observe('restored missing artifact accepts',0)\n # Relevant product bytes invalidate cached source evidence independently of the\n # external approval. Adapter bytes additionally change the approved dependency.\n product=root/'product/pyalamode'\n for filename in ('checker.py','model.py','project.py','integration_contracts.py'):\n  path=product/filename;old=sha(path);path.write_bytes(path.read_bytes()+b'\\n# independent M8 copied-product freshness input\\n')\n  changed=observe(filename+' actual product byte change',0,False);check(changed['product'][filename]!=old,filename+' actual product identity changed');observe(filename+' changed product warm',0,True)\n path=product/'integrations.py';old=sha(path);path.write_bytes(path.read_bytes()+b'\\n# independent changed adapter artifact\\n')\n changed=observe('adapter actual bytes stale approval',1,False);check(changed['product']['integrations.py']!=old,'adapter bytes alter actual product identity')\n observe('adapter stale rejected build',1,None,False,True);approve('adapter explicit current reapproval');observe('adapter current reapproved',0,False)\n # Cross-publication expiry: initial approval must pass, then current UTC crosses\n # before publication. The isolated delay is product-control instrumentation.\n crossing=r'''import json,time\nfrom datetime import datetime,timezone,timedelta\nfrom pathlib import Path\nimport pyalamode.project as project_api\nfrom m08_common import prepare,policy_text\nroot=Path(PROJECT)\npolicy,snapshot=prepare(root,{'id':'crossing expiry','files':{'core.py':root.joinpath('core.py').read_text()}})\nexpiry=(datetime.now(timezone.utc)+timedelta(seconds=2)).replace(microsecond=0)\nfor entry in policy['integration_approvals']:entry['expires_at']=expiry.strftime('%Y-%m-%dT%H:%M:%SZ')\nroot.joinpath('pyproject.toml').write_text(policy_text(policy))\noriginal=project_api._guard_plan\ncalls=[]\ndef delayed(*args,**kwargs):\n calls.append('initial admitted plan');original(*args,**kwargs);time.sleep(2.1)\nproject_api._guard_plan=delayed\ntry:result=project_api.build_paths(root=root,output=root/'artifact')\nfinally:project_api._guard_plan=original\nassert calls and result.status==1 and not root.joinpath('artifact').exists()\nprint(json.dumps({'status':result.status,'artifact_exists':False,'expired':datetime.now(timezone.utc)>=expiry,'calls':calls,'contracts':[c.__dict__ for f in result.results for c in f.contracts]}))\n'''\n call('actual UTC approval crosses before publication',crossing.replace('PROJECT',repr(str(project))))\n report={'inputs':{'m08_identity_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py')},'assertions':checks,'rows':rows,'original_native':original_native,'copied_interpreter_sha256':sha(interpreter),'copied_core_sha256':sha(core_copy),'original_interpreter_sha256':sha(Path(sys.executable).resolve()),'original_core_sha256':sha(core_original),'shared_native':shared_native,'shared_installation_unchanged':all(sha(Path(v['path']))==v['sha256'] for v in shared_native.values()),'literal_fixture':fixture,'literal_observation_source':source,'literal_approval_source':approval_source,'literal_runtime_source':runtime_source}\n check(report['copied_interpreter_sha256']==report['original_interpreter_sha256'] and report['copied_core_sha256']==report['original_core_sha256'],'real copied interpreter/core equal original foundations')\n # No copied path escapes this TemporaryDirectory; report retains all observed\n # actual digests and paths after the isolated checkout is removed.\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-identity-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows)}))\n",
  "freshness_probe.py": "import json,os,shutil,subprocess,sys,tempfile\nfrom pathlib import Path\nimport pyalamode\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\nsource='from pyalamode import fun,compose,partial_first\\n@fun\\ndef plus(x:int)->int:\\n    return x+1\\n@fun\\ndef divide(a:int,b:int)->int:\\n    return a//b\\n@fun\\ndef probe(x:int)->int:\\n    return compose(plus,partial_first(divide,10))(x)\\n'\nscript='''import json\nfrom pyalamode.project import check_paths\nfrom pyalamode.model import foundation_identities\nresult=check_paths(root=PROJECT)\nprint(json.dumps({'status':result.status,'hits':[f.cache_hit for f in result.results],'identities':foundation_identities(),'contracts':[c.__dict__ for f in result.results for c in f.contracts]}))\n'''\nwith tempfile.TemporaryDirectory(prefix='m07-product-copy-') as d:\n root=Path(d);project=root/'project';project.mkdir();(project/'core.py').write_text(source)\n shutil.copytree(Path(pyalamode.__file__).parent,root/'product/pyalamode',ignore=shutil.ignore_patterns('__pycache__'))\n env=dict(os.environ);env['PYTHONPATH']=str(root/'product')+os.pathsep+env.get('PYTHONPATH','')\n def observe(label,hits):\n  ran=subprocess.run([sys.executable,'-c',script.replace('PROJECT',repr(str(project)))],cwd=root,env=env,capture_output=True,text=True)\n  check(ran.returncode==0,label+' process '+ran.stderr);value=json.loads(ran.stdout);check(value['status']==0,label+' admission');check(value['hits']==hits,label+' exact cache state');rows.append(dict(label=label,**value));return value\n old=observe('copy cold',[False]);warm=observe('copy full warm',[True]);check(old['contracts']==warm['contracts'],'exact copy warm evidence')\n check(len(old['identities'])==16,'all sixteen M8 product foundations')\n for filename in ('standard.py','standard_contracts.py','effects.py','checker.py','model.py'):\n  p=root/'product/pyalamode'/filename;p.write_bytes(p.read_bytes()+b'\\n# independent relevant operation freshness input\\n')\n  changed=observe(filename+' byte changed',[False]);check(changed['identities'][filename]!=warm['identities'][filename],filename+' actual byte changed');warm=observe(filename+' changed warm',[True])\n (project/'pyproject.toml').write_text('[tool.pyalamode]\\nrequire_modules=[\"core.py\"]\\n')\n observe('policy changed',[False]);observe('policy changed warm',[True]);check(not (project/'artifact').exists(),'cache only no artifact')\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'freshness-observations.json')).write_text(json.dumps(dict(assertions=checks,rows=rows,literal_source=source,literal_driver=script),indent=2)+'\\n')\nprint(json.dumps(dict(assertions=checks,subprocesses=len(rows))))\n"
}
```

## Interim diagnostic harness correction

The fixed 176 source outcomes, 57 runtime inputs and 26 configuration subprocess expectations passed unchanged on the interim native candidate. The actual CLI probe stopped at its outer path assertion: stock execution already verified its module file inside `Path.cwd().resolve()`, while the parent compared that resolved `/private/var/...` module path against unresolved macOS `/var/...` artifact paths. Both sides now use `resolve()`; the same strict artifact-provenance expectation remains. This is a reviewer harness correction, not a product correction or weakened expected outcome. The complete corrected CLI harness is fixed below before its rerun; original text and failing interim trace remain reproducible above.

Corrected CLI SHA-256 `11a04f0676d95d07d4ff66caaa473090da2e68cc802d17ece0af8f6acfc0dbdd`.

```python
import json,os,subprocess,sys,tempfile
from pathlib import Path
from m08_common import prepare,sha,CANON
OUT=Path(__file__).parent;checks=0;rows=[]
def check(value,label):
 global checks
 checks+=1
 if not value:raise AssertionError(label)
def call(root,label,args,status,console=False):
 executable=[str(Path(sys.executable).parent/'pyalamode')] if console else [sys.executable,'-m','pyalamode']
 ran=subprocess.run([*executable,*args],cwd=root,capture_output=True,text=True)
 check(ran.returncode==status,label+' status '+str(ran.returncode)+' '+ran.stderr)
 rows.append({'label':label,'command':[*executable,*args],'cwd':str(root),'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr})
 return json.loads(ran.stdout) if '--json' in args else None
source='from pyalamode import fun\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef probe(data:bytes)->tuple[bytes,bytes]:\n    encoded=base64_encode(data)\n    restored=base64_decode(encoded)\n    return encoded,sha256_digest(restored)\n'
stock_source=r'''import json
from pathlib import Path
import core
from pyalamode import unsafe,fun
artifact=Path.cwd().resolve()
assert Path(core.__file__).resolve().is_relative_to(artifact)
expected=(b'YWJj',bytes.fromhex('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'))
assert core.probe(b'abc')==expected
assert core.probe.__dict__=={}
assert fun(core.probe) is core.probe
checks=4
mode=MODE
if mode!='off':
 from pyalamode_exports.core import probe
 assert probe.__wrapped__ is core.probe
 assert probe(b'abc')==expected
 checks+=2
 original=core.probe.__code__
 def body(data):
  Path('body-sentinel').write_text('entered')
  return (b'',b'')
 core.probe.__code__=body.__code__
 class Binary(bytes):pass
 for value in (Binary(b'abc'),bytearray(b'abc'),memoryview(b'abc'),True):
  try:probe(value)
  except TypeError as error:
   assert 'core:probe' in str(error) and 'core.py:' in str(error) and 'argument data' in str(error)
  else:raise AssertionError('invalid selected export admitted')
  assert not Path('body-sentinel').exists()
  checks+=2
 core.probe.__code__=original
 if mode=='debug':
  try:core.probe(Binary(b'abc'))
  except TypeError as error:assert 'argument data' in str(error)
  else:raise AssertionError('debug original entry admitted subtype')
  checks+=1
print(json.dumps({'assertions':checks,'module_file':core.__file__,'artifact':str(artifact),'mode':mode,'result_hex':[x.hex() for x in expected]}))
'''
for mode in ('off','exports','debug'):
 with tempfile.TemporaryDirectory(prefix='m08-cli-artifact-') as directory:
  root=Path(directory);policy,snapshot=prepare(root,{'id':'CLI '+mode,'files':{'core.py':source},'mode':mode})
  checked=call(root,mode+' strict check',['check','--root',str(root),'--no-cache','--json'],0)
  check(checked['verified'],mode+' strict verified dimension')
  audited=call(root,mode+' audit',['check','--root',str(root),'--audit','--no-cache','--json'],0)
  check(not audited['verified'],mode+' audit no strict certificate')
  artifact=root/'artifact';built=call(root,mode+' build',['build','--root',str(root),'--output',str(artifact),'--json'],0)
  evidence=json.loads((artifact/'pyalamode-evidence.json').read_text())
  check(built['verified'] and built['boundary_guards']==mode,mode+' build guard dimension')
  check(len(evidence['files'][0]['contracts'][0]['external_assumptions'])==3,mode+' artifact keeps all three exact assumptions')
  if mode in ('off','exports'):check((artifact/'core.py').read_text()==source,mode+' copied source bytes identical')
  env=dict(os.environ);env['PYTHONPATH']=str(artifact)+os.pathsep+env.get('PYTHONPATH','')
  script=stock_source.replace('MODE',repr(mode));ran=subprocess.run([sys.executable,'-c',script],cwd=artifact,env=env,capture_output=True,text=True)
  check(ran.returncode==0,mode+' actual stock artifact execution '+ran.stderr)
  value=json.loads(ran.stdout);check(Path(value['module_file']).resolve().is_relative_to(artifact.resolve()),mode+' actual module file inside output')
  rows.append({'label':mode+' actual stock execution','command':[sys.executable,'-c',script],'cwd':str(artifact),'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'artifact_product':evidence.get('product_artifacts'),'assertions':value['assertions']})
cases={row['id']:row for row in json.loads((OUT/'m08-literal-cases.json').read_text())}
negative_ids=('E01-deny','E01-missing','E01-wrong-contract','E01-wrong-dependency','E01-expired','A-override-draft','A-override-effect-undeclared','W-native-error-init','W-adapter-globals','W-sysmodules-native','U-direct','U-effectful','U-marked','N-backend-module','N-app-default','N-app-decorator','N-app-annotation','A-invalid-bad-expiry','A-manifest-parent')
for id in negative_ids:
 case=cases[id]
 with tempfile.TemporaryDirectory(prefix='m08-cli-refusal-') as directory:
  root=Path(directory);prepare(root,case);status=case['expected']
  call(root,id+' check',['check','--root',str(root),'--json'],status)
  call(root,id+' audit',['check','--root',str(root),'--audit','--json'],2 if status==2 else 0)
  call(root,id+' build',['build','--root',str(root),'--output',str(root/'artifact'),'--json'],status)
  check(not (root/'artifact').exists(),id+' failed gate has no artifact');check(not (root/'sentinel').exists(),id+' no application/dependency execution')
with tempfile.TemporaryDirectory(prefix='m08-real-console-') as directory:
 root=Path(directory);prepare(root,cases['E01-direct'])
 value=call(OUT,'real installed console entrypoint',['check','--root',str(root),'--json','--no-cache'],0,True)
 check(value['verified'],'console entrypoint verifies actual selected source')
 check(any(c['external_assumptions'][0]['identity']==CANON[0] for f in value['files'] for c in f['contracts'] if c['name']=='probe'),'console actual Base64 assumption visible')
 check(not (root/'sentinel').exists(),'console no sentinel')
 for symbol in ('base64_encode','base64_decode','sha256_digest','unsafe','PAL350','PAL351'):
  call(OUT,'explain '+symbol,['explain',symbol],0)
 entry=root/'entry.py';entry.write_text('from core import probe\nprint(probe(b"abc"))\n')
 ran=subprocess.run([sys.executable,'-m','pyalamode','run',str(entry),'--root',str(root)],cwd=OUT,capture_output=True,text=True)
 check(ran.returncode==2,'optional run remains unsupported');check(not (root/'artifact').exists(),'unsupported run creates no artifact')
 rows.append({'label':'optional run unsupported','status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr})
report={'inputs':{'m08_cli_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py'),'m08-literal-cases.json':sha(OUT/'m08-literal-cases.json')},'assertions':checks,'rows':rows,'literal_artifact_source':source,'literal_stock_source':stock_source,'negative_ids':negative_ids}
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-cli-observations.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows)}))
```

The isolated copied-runtime probe encountered the same macOS `/var` symlink at its two copy-path provenance assertions. Both now canonicalize the copied home too; exact bytes, actual native execution from the copied home and all freshness/refusal expectations remain fixed. No artifact/approval outcome was changed. Complete corrected identity harness SHA-256 `68c4cfd1102688ac5e4bef21d7af8012410c526839225d8bac51b88d5b569a49` is fixed here before rerun.

```python
import json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
import pyalamode
from m08_common import sha
OUT=Path(__file__).parent;checks=0;rows=[]
def check(value,label):
 global checks
 checks+=1
 if not value:raise AssertionError(label)
# Actual interpreter/home/native/product copies; shared installations are never
# edited. Copied core bytes stay identical to the actual loaded core foundation.
source=r'''import json,sys
from pathlib import Path
from pyalamode.project import check_paths,build_paths
from pyalamode.integration_contracts import integration_snapshot
from pyalamode.model import foundation_identities
root=Path(PROJECT)
result=build_paths(root=root,output=root/'artifact') if BUILD else check_paths(root=root,cache=CACHE)
print(json.dumps({'status':result.status,'verified':result.verified,'hits':{Path(f.path).name:f.cache_hit for f in result.results},'snapshot':integration_snapshot(root=root),'product':foundation_identities(),'contracts':[c.__dict__ for f in result.results for c in f.contracts],'artifact_exists':(root/'artifact').exists(),'tooling':[d.__dict__ for d in result.tooling],'diagnostics':[d.__dict__ for f in result.results for d in f.diagnostics],'native_loaded':sorted({'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys())}))
'''
approval_source=r'''import json
from pathlib import Path
from m08_common import prepare
root=Path(PROJECT)
policy,snapshot=prepare(root,{'id':'real copied installed identity','files':{'core.py':root.joinpath('core.py').read_text()}})
print(json.dumps({'policy':policy,'snapshot':snapshot}))
'''
runtime_source=r'''import json
from pathlib import Path
import binascii,_sha2
from pyalamode.integrations import base64_encode,base64_decode,sha256_digest
assert Path(binascii.__file__).resolve().is_relative_to(Path(HOME).resolve())
assert Path(_sha2.__file__).resolve().is_relative_to(Path(HOME).resolve())
assert base64_encode(b'abc')==b'YWJj'
assert base64_decode(b'YWJj')==b'abc'
assert sha256_digest(b'abc').hex()=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
print(json.dumps({'binascii_file':binascii.__file__,'sha2_file':_sha2.__file__,'checks':5}))
'''
fixture='from pyalamode import fun\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\n@fun\ndef probe(data:bytes)->bytes:\n    return sha256_digest(base64_decode(base64_encode(data)))\n'
with tempfile.TemporaryDirectory(prefix='m08-real-runtime-copy-') as directory:
 root=Path(directory);home=root/'runtime';stdlib=home/'lib/python3.13';stdlib.parent.mkdir(parents=True)
 shutil.copytree(Path(sys.base_prefix)/'lib/python3.13',stdlib,ignore=shutil.ignore_patterns('site-packages','__pycache__'))
 (home/'bin').mkdir();interpreter=home/'bin/python';shutil.copy2(Path(sys.executable).resolve(),interpreter)
 core_original=Path(sys.base_prefix)/('Python' if sys.platform=='darwin' else 'lib/libpython3.13.so.1.0')
 core_copy=home/('Python' if sys.platform=='darwin' else 'lib/libpython3.13.so.1.0');shutil.copy2(core_original,core_copy)
 shutil.copytree(Path(pyalamode.__file__).parent,root/'product/pyalamode',ignore=shutil.ignore_patterns('__pycache__'))
 project=root/'project';project.mkdir();(project/'core.py').write_text(fixture)
 env=dict(os.environ);env['PYTHONHOME']=str(home);env['PYTHONPATH']=str(root/'product')+os.pathsep+str(OUT)
 for key in ('_PYTHON_SYSCONFIGDATA_NAME','_PYTHON_SYSCONFIGDATA_PATH','_PYTHON_HOST_PLATFORM'):env.pop(key,None)
 def call(label,program,status=0):
  ran=subprocess.run([str(interpreter),'-S','-c',program],cwd=OUT,env=env,capture_output=True,text=True)
  check(ran.returncode==status,label+' copied actual interpreter process '+ran.stderr)
  value=json.loads(ran.stdout) if ran.returncode==0 else None
  rows.append({'label':label,'process_status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'source':program,'value':value});return value
 def approve(label):return call(label,approval_source.replace('PROJECT',repr(str(project))))
 def observe(label,status,hits=None,cache=True,build=False):
  program=source.replace('PROJECT',repr(str(project))).replace('BUILD',repr(build)).replace('CACHE',repr(cache));value=call(label,program)
  check(value['status']==status,label+' exact check/build status '+str(value['status']))
  if hits is not None:check(value['hits']=={'core.py':hits},label+' exact cache hit')
  check(not value['native_loaded'],label+' no backend/adaptor execution during discovery/check/build')
  if status:check(not value['artifact_exists'],label+' failed gate no artifact')
  return value
 approved=approve('copied home explicit real installed approval')
 baseline=observe('copied home approved cold',0,False);warm=observe('copied home approved full warm',0,True)
 check(baseline['contracts']==warm['contracts'],'copied home cold/warm exact external trust')
 identity=approved['snapshot']['catalog'][0]['installed_identity'];native={name:Path(value['path']) for name,value in identity['native_artifacts'].items()}
 check(all(path.is_relative_to(home.resolve()) for path in native.values()),'fixed discovery resolves actual copied native artifacts')
 check(identity['interpreter_executable']['path']==str(interpreter.resolve()) and identity['interpreter_core']['path']==str(core_copy.resolve()),'copied executable/core identities are explicit')
 original_native={name:{'path':str(path),'sha256':sha(path)} for name,path in native.items()}
 shared_native={name:{'path':str(Path(sys.base_prefix)/'lib/python3.13/lib-dynload'/path.name),'sha256':sha(Path(sys.base_prefix)/'lib/python3.13/lib-dynload'/path.name)} for name,path in native.items()}
 for name,path in native.items():
  original=path.read_bytes();path.write_bytes(original+b'\nM8 independent harmless artifact byte change\n')
  check(sha(path)!=original_native[name]['sha256'],name+' real installed bytes changed')
  changed=observe(name+' changed artifact stale warm',1,False)
  observe(name+' changed artifact stale full warm',1,True)
  observe(name+' changed artifact stale no-cache',1,False,False)
  observe(name+' changed artifact rejected build',1,None,False,True)
  refreshed=approve(name+' explicit changed-artifact reapproval')
  accepted=observe(name+' changed-artifact reapproved cold',0,False);observe(name+' changed-artifact reapproved warm',0,True)
  check(accepted['contracts'][0]['external_assumptions'][0]['dependency_sha256']!=baseline['contracts'][0]['external_assumptions'][0]['dependency_sha256'],name+' actual new identity propagated transitively')
  call(name+' actual changed native artifact invocation',runtime_source.replace('HOME',repr(str(home))))
  path.write_bytes(original);approve(name+' explicit restored original reapproval');baseline=observe(name+' restored artifact current',0)
 # Missing supported installed file cannot return a valid-looking identity.
 missing=native['binascii'];saved=missing.with_name(missing.name+'.saved');missing.rename(saved)
 observe('real supported native artifact missing',1,False);observe('missing artifact no-cache',1,False,False);observe('missing artifact rejected build',1,None,False,True)
 saved.rename(missing);approve('restored missing artifact explicit current approval');observe('restored missing artifact accepts',0)
 # Relevant product bytes invalidate cached source evidence independently of the
 # external approval. Adapter bytes additionally change the approved dependency.
 product=root/'product/pyalamode'
 for filename in ('checker.py','model.py','project.py','integration_contracts.py'):
  path=product/filename;old=sha(path);path.write_bytes(path.read_bytes()+b'\n# independent M8 copied-product freshness input\n')
  changed=observe(filename+' actual product byte change',0,False);check(changed['product'][filename]!=old,filename+' actual product identity changed');observe(filename+' changed product warm',0,True)
 path=product/'integrations.py';old=sha(path);path.write_bytes(path.read_bytes()+b'\n# independent changed adapter artifact\n')
 changed=observe('adapter actual bytes stale approval',1,False);check(changed['product']['integrations.py']!=old,'adapter bytes alter actual product identity')
 observe('adapter stale rejected build',1,None,False,True);approve('adapter explicit current reapproval');observe('adapter current reapproved',0,False)
 # Cross-publication expiry: initial approval must pass, then current UTC crosses
 # before publication. The isolated delay is product-control instrumentation.
 crossing=r'''import json,time
from datetime import datetime,timezone,timedelta
from pathlib import Path
import pyalamode.project as project_api
from m08_common import prepare,policy_text
root=Path(PROJECT)
policy,snapshot=prepare(root,{'id':'crossing expiry','files':{'core.py':root.joinpath('core.py').read_text()}})
expiry=(datetime.now(timezone.utc)+timedelta(seconds=2)).replace(microsecond=0)
for entry in policy['integration_approvals']:entry['expires_at']=expiry.strftime('%Y-%m-%dT%H:%M:%SZ')
root.joinpath('pyproject.toml').write_text(policy_text(policy))
original=project_api._guard_plan
calls=[]
def delayed(*args,**kwargs):
 calls.append('initial admitted plan');original(*args,**kwargs);time.sleep(2.1)
project_api._guard_plan=delayed
try:result=project_api.build_paths(root=root,output=root/'artifact')
finally:project_api._guard_plan=original
assert calls and result.status==1 and not root.joinpath('artifact').exists()
print(json.dumps({'status':result.status,'artifact_exists':False,'expired':datetime.now(timezone.utc)>=expiry,'calls':calls,'contracts':[c.__dict__ for f in result.results for c in f.contracts]}))
'''
 call('actual UTC approval crosses before publication',crossing.replace('PROJECT',repr(str(project))))
 report={'inputs':{'m08_identity_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py')},'assertions':checks,'rows':rows,'original_native':original_native,'copied_interpreter_sha256':sha(interpreter),'copied_core_sha256':sha(core_copy),'original_interpreter_sha256':sha(Path(sys.executable).resolve()),'original_core_sha256':sha(core_original),'shared_native':shared_native,'shared_installation_unchanged':all(sha(Path(v['path']))==v['sha256'] for v in shared_native.values()),'literal_fixture':fixture,'literal_observation_source':source,'literal_approval_source':approval_source,'literal_runtime_source':runtime_source}
 check(report['copied_interpreter_sha256']==report['original_interpreter_sha256'] and report['copied_core_sha256']==report['original_core_sha256'],'real copied interpreter/core equal original foundations')
 # No copied path escapes this TemporaryDirectory; report retains all observed
 # actual digests and paths after the isolated checkout is removed.
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-identity-observations.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows)}))
```

## Fixed real unsupported installed-version probe

The actual separately installed Homebrew CPython 3.12 executable is probed without changing sys.version or shared bytes: metadata must return no supported installed identity/dependency digest, and check/build must return target2/no artifact. This native-only three-process scope supplies actual version-change evidence; an absent alternate interpreter on Linux creates no version-result claim. Source expectation is fixed before its first observation, after the product source freeze.

Harness SHA-256 `240ea4e25b85dfd036f3d4f0556588176208587a757956ed7811abb33507b49a`.

```python
import json,os,subprocess,sys,tempfile
from pathlib import Path
import pyalamode
from m08_common import sha
OUT=Path(__file__).parent;rows=[];checks=0
# Native actual Homebrew CPython 3.12 is an installed unsupported runtime, not a
# monkeypatched sys.version identity. It is not installed on the Docker target.
alternative=Path('/opt/homebrew/opt/python@3.12/bin/python3.12')
source=r'''import json,sys
from pyalamode.integration_contracts import integration_snapshot
snapshot=integration_snapshot()
assert all(row['installed_identity'] is None and row['dependency_sha256'] is None for row in snapshot['catalog'])
assert not {'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys()
print(json.dumps({'python':sys.version,'cache_tag':sys.implementation.cache_tag,'snapshot':snapshot}))
'''
if alternative.exists():
 with tempfile.TemporaryDirectory(prefix='m08-real-version-') as directory:
  root=Path(directory);(root/'core.py').write_text('from pyalamode import fun\n@fun\ndef probe(value:int)->int:\n    return value+1\n')
  env=dict(os.environ);env['PYTHONPATH']=str(Path(pyalamode.__file__).parent.parent)
  for label,args,status in [('actual unsupported installed version metadata',['-c',source],0),('actual unsupported installed version check',['-m','pyalamode','check','--root',str(root),'--json'],2),('actual unsupported installed version build',['-m','pyalamode','build','--root',str(root),'--output',str(root/'artifact'),'--json'],2)]:
   ran=subprocess.run([str(alternative),'-S',*args],cwd=OUT,env=env,capture_output=True,text=True);checks+=2
   if ran.returncode!=status or (root/'artifact').exists():raise AssertionError(label+' '+str(ran.returncode)+' '+ran.stderr)
   rows.append({'label':label,'command':[str(alternative),'-S',*args],'expected':status,'observed':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr})
report={'inputs':{'m08_version_probe.py':sha(__file__)},'scope':'actual native macOS installed CPython 3.12 only' if alternative.exists() else 'alternate installed interpreter unavailable; no version-result claim','assertions':checks,'rows':rows,'literal_metadata_source':source}
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-version-observations.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows),'scope':report['scope']}))
```

## Corrected joint freeze and final controller

The first joint candidate failed the unchanged inherited M2 positive `calculations.add(plus(x))` on both platforms: the ordinary checked function name `add` was mistaken for a mutating method. Root reopened only the checker and focused regression; corrected joint freeze SHA-256 is `18fc42d5f4d76160a1a74edf39882f044024847888ef2774d85cc77daa566712`. The corrected checker SHA-256 is `65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5`. Literal expectations remain unchanged. Historical observations from the earlier checker are diagnostic only.

The isolated identity harness counted its last equality assertion after constructing the raw report, giving 153 stdout assertions versus 152 in the raw field. Before final reruns, only the raw counter assignment is corrected; the same 153 assertions and all behavior expectations remain. The executable final controller requires a fresh wheel outside the checkout, exactly 17 installed package files equal to current source, the corrected freeze map, all focused harnesses, and the complete 320-method suite. It records full before/after source, harness, installed product, and real backend identity maps.

Current harness hashes:

```json
{
  "m08_final_probe.py": "5d330f09a64599ad62224b4eee100dba37d5d093c821427a6583ca253f10fb9f",
  "m08_identity_probe.py": "07be7351a293f59cdfbcfcd38ee82edfdaaec3a83606d943ef6996124fd93492"
}
```

Complete current replacement identity harness and final controller (these supersede earlier harness text by filename):

```json
{
  "m08_final_probe.py": "import hashlib,json,platform,re,subprocess,sys,time\nfrom pathlib import Path\nimport pyalamode\nfrom pyalamode.integration_contracts import integration_snapshot\nOUT=Path(__file__).parent;ROOT=Path(sys.argv[1]);NAME=sys.argv[2]\ndef digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()\ndef source_map():\n paths=[ROOT/'pyproject.toml',ROOT/'README.md']\n for area in ('pyalamode','tests','examples','benchmarks'):paths.extend((ROOT/area).rglob('*.py'))\n result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths)) if '__pycache__' not in p.parts}\n for p in sorted(OUT.glob('*.py')):result['reviewer:'+p.name]=digest(p)\n for name in ('literal-cases.json','m06-literal-cases.json','literal-layouts.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json','local-writer-cases.json','m08-literal-cases.json','m08-runtime-inputs.json','corrected-root-freeze.json'):result['reviewer:'+name]=digest(OUT/name)\n return result\ndef installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}\nbefore=source_map();installed_before=installed_map();freeze=json.loads((OUT/'corrected-root-freeze.json').read_text())\nassert len(installed_before)==17\nassert all(before[k]==v for k,v in installed_before.items())\nassert all(before[k]==v for k,v in freeze['paths'].items())\nassert not Path(pyalamode.__file__).resolve().is_relative_to(ROOT.resolve()),'must use freshly installed wheel outside checkout'\ninstalled_snapshot_before=integration_snapshot()\nassert not {'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys()\nresults=[]\nscripts=('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','freshness_probe.py','m06_runtime_probe.py','m06_project_probe.py','m06_cli_probe.py','m06_nonexecution_probe.py','m06_freshness_probe.py','environment_probe.py','m08_static_probe.py','m08_runtime_probe.py','m08_project_probe.py','m08_cli_probe.py','m08_nonexecution_probe.py','m08_identity_probe.py','m08_version_probe.py')\nfor script in scripts:\n target=NAME+'-'+script.removesuffix('_probe.py')+'.json';started=time.perf_counter()\n ran=subprocess.run([sys.executable,str(OUT/script),target],cwd=OUT,capture_output=True,text=True)\n row=dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=target);results.append(row)\n (OUT/(NAME+'-progress.json')).write_text(json.dumps(results,indent=2)+'\\n')\n print(json.dumps({'script':script,'status':ran.returncode,'elapsed_seconds':row['elapsed_seconds'],'summary':ran.stdout.strip()}),flush=True)\n if ran.returncode:print(ran.stderr,flush=True);raise SystemExit(ran.returncode)\nstarted=time.perf_counter()\nran=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','m*.py'],cwd=OUT,capture_output=True,text=True)\nsuite=dict(status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr)\nif ran.returncode:print(json.dumps(suite));raise SystemExit(ran.returncode)\nmatch=re.search(r'Ran (\\d+) tests in ([\\d.]+)s',ran.stderr);assert match\nsuite.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)));assert suite['tests']==320\nafter=source_map();installed_after=installed_map();installed_snapshot_after=integration_snapshot()\nassert before==after;assert installed_before==installed_after;assert installed_snapshot_before==installed_snapshot_after\nreport=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,base_prefix=sys.base_prefix,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),abiflags=sys.abiflags,filesystem_encoding=sys.getfilesystemencoding(),filesystem_errors=sys.getfilesystemencodeerrors(),utf8_mode=sys.flags.utf8_mode,package_path=pyalamode.__file__),results=results,suite=suite,source_before=before,source_after=after,installed_product_before=installed_before,installed_product_after=installed_after,installed_snapshot_before=installed_snapshot_before,installed_snapshot_after=installed_snapshot_after,source_unchanged=True,installed_source_equal=True,corrected_freeze_sha256=digest(OUT/'corrected-root-freeze.json'))\n(OUT/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'name':NAME,'suite':suite['tests'],'suite_seconds':suite['reported_seconds'],'focused_scripts':len(results),'source_files':len(before),'installed_product_files':len(installed_before),'unchanged':True}),flush=True)\n",
  "m08_identity_probe.py": "import json,os,shutil,subprocess,sys,tempfile,time\nfrom pathlib import Path\nimport pyalamode\nfrom m08_common import sha\nOUT=Path(__file__).parent;checks=0;rows=[]\ndef check(value,label):\n global checks\n checks+=1\n if not value:raise AssertionError(label)\n# Actual interpreter/home/native/product copies; shared installations are never\n# edited. Copied core bytes stay identical to the actual loaded core foundation.\nsource=r'''import json,sys\nfrom pathlib import Path\nfrom pyalamode.project import check_paths,build_paths\nfrom pyalamode.integration_contracts import integration_snapshot\nfrom pyalamode.model import foundation_identities\nroot=Path(PROJECT)\nresult=build_paths(root=root,output=root/'artifact') if BUILD else check_paths(root=root,cache=CACHE)\nprint(json.dumps({'status':result.status,'verified':result.verified,'hits':{Path(f.path).name:f.cache_hit for f in result.results},'snapshot':integration_snapshot(root=root),'product':foundation_identities(),'contracts':[c.__dict__ for f in result.results for c in f.contracts],'artifact_exists':(root/'artifact').exists(),'tooling':[d.__dict__ for d in result.tooling],'diagnostics':[d.__dict__ for f in result.results for d in f.diagnostics],'native_loaded':sorted({'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys())}))\n'''\napproval_source=r'''import json\nfrom pathlib import Path\nfrom m08_common import prepare\nroot=Path(PROJECT)\npolicy,snapshot=prepare(root,{'id':'real copied installed identity','files':{'core.py':root.joinpath('core.py').read_text()}})\nprint(json.dumps({'policy':policy,'snapshot':snapshot}))\n'''\nruntime_source=r'''import json\nfrom pathlib import Path\nimport binascii,_sha2\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\nassert Path(binascii.__file__).resolve().is_relative_to(Path(HOME).resolve())\nassert Path(_sha2.__file__).resolve().is_relative_to(Path(HOME).resolve())\nassert base64_encode(b'abc')==b'YWJj'\nassert base64_decode(b'YWJj')==b'abc'\nassert sha256_digest(b'abc').hex()=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'\nprint(json.dumps({'binascii_file':binascii.__file__,'sha2_file':_sha2.__file__,'checks':5}))\n'''\nfixture='from pyalamode import fun\\nfrom pyalamode.integrations import base64_encode,base64_decode,sha256_digest\\n@fun\\ndef probe(data:bytes)->bytes:\\n    return sha256_digest(base64_decode(base64_encode(data)))\\n'\nwith tempfile.TemporaryDirectory(prefix='m08-real-runtime-copy-') as directory:\n root=Path(directory);home=root/'runtime';stdlib=home/'lib/python3.13';stdlib.parent.mkdir(parents=True)\n shutil.copytree(Path(sys.base_prefix)/'lib/python3.13',stdlib,ignore=shutil.ignore_patterns('site-packages','__pycache__'))\n (home/'bin').mkdir();interpreter=home/'bin/python';shutil.copy2(Path(sys.executable).resolve(),interpreter)\n core_original=Path(sys.base_prefix)/('Python' if sys.platform=='darwin' else 'lib/libpython3.13.so.1.0')\n core_copy=home/('Python' if sys.platform=='darwin' else 'lib/libpython3.13.so.1.0');shutil.copy2(core_original,core_copy)\n shutil.copytree(Path(pyalamode.__file__).parent,root/'product/pyalamode',ignore=shutil.ignore_patterns('__pycache__'))\n project=root/'project';project.mkdir();(project/'core.py').write_text(fixture)\n env=dict(os.environ);env['PYTHONHOME']=str(home);env['PYTHONPATH']=str(root/'product')+os.pathsep+str(OUT)\n for key in ('_PYTHON_SYSCONFIGDATA_NAME','_PYTHON_SYSCONFIGDATA_PATH','_PYTHON_HOST_PLATFORM'):env.pop(key,None)\n def call(label,program,status=0):\n  ran=subprocess.run([str(interpreter),'-S','-c',program],cwd=OUT,env=env,capture_output=True,text=True)\n  check(ran.returncode==status,label+' copied actual interpreter process '+ran.stderr)\n  value=json.loads(ran.stdout) if ran.returncode==0 else None\n  rows.append({'label':label,'process_status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'source':program,'value':value});return value\n def approve(label):return call(label,approval_source.replace('PROJECT',repr(str(project))))\n def observe(label,status,hits=None,cache=True,build=False):\n  program=source.replace('PROJECT',repr(str(project))).replace('BUILD',repr(build)).replace('CACHE',repr(cache));value=call(label,program)\n  check(value['status']==status,label+' exact check/build status '+str(value['status']))\n  if hits is not None:check(value['hits']=={'core.py':hits},label+' exact cache hit')\n  check(not value['native_loaded'],label+' no backend/adaptor execution during discovery/check/build')\n  if status:check(not value['artifact_exists'],label+' failed gate no artifact')\n  return value\n approved=approve('copied home explicit real installed approval')\n baseline=observe('copied home approved cold',0,False);warm=observe('copied home approved full warm',0,True)\n check(baseline['contracts']==warm['contracts'],'copied home cold/warm exact external trust')\n identity=approved['snapshot']['catalog'][0]['installed_identity'];native={name:Path(value['path']) for name,value in identity['native_artifacts'].items()}\n check(all(path.is_relative_to(home.resolve()) for path in native.values()),'fixed discovery resolves actual copied native artifacts')\n check(identity['interpreter_executable']['path']==str(interpreter.resolve()) and identity['interpreter_core']['path']==str(core_copy.resolve()),'copied executable/core identities are explicit')\n original_native={name:{'path':str(path),'sha256':sha(path)} for name,path in native.items()}\n shared_native={name:{'path':str(Path(sys.base_prefix)/'lib/python3.13/lib-dynload'/path.name),'sha256':sha(Path(sys.base_prefix)/'lib/python3.13/lib-dynload'/path.name)} for name,path in native.items()}\n for name,path in native.items():\n  original=path.read_bytes();path.write_bytes(original+b'\\nM8 independent harmless artifact byte change\\n')\n  check(sha(path)!=original_native[name]['sha256'],name+' real installed bytes changed')\n  changed=observe(name+' changed artifact stale warm',1,False)\n  observe(name+' changed artifact stale full warm',1,True)\n  observe(name+' changed artifact stale no-cache',1,False,False)\n  observe(name+' changed artifact rejected build',1,None,False,True)\n  refreshed=approve(name+' explicit changed-artifact reapproval')\n  accepted=observe(name+' changed-artifact reapproved cold',0,False);observe(name+' changed-artifact reapproved warm',0,True)\n  check(accepted['contracts'][0]['external_assumptions'][0]['dependency_sha256']!=baseline['contracts'][0]['external_assumptions'][0]['dependency_sha256'],name+' actual new identity propagated transitively')\n  call(name+' actual changed native artifact invocation',runtime_source.replace('HOME',repr(str(home))))\n  path.write_bytes(original);approve(name+' explicit restored original reapproval');baseline=observe(name+' restored artifact current',0)\n # Missing supported installed file cannot return a valid-looking identity.\n missing=native['binascii'];saved=missing.with_name(missing.name+'.saved');missing.rename(saved)\n observe('real supported native artifact missing',1,False);observe('missing artifact no-cache',1,False,False);observe('missing artifact rejected build',1,None,False,True)\n saved.rename(missing);approve('restored missing artifact explicit current approval');observe('restored missing artifact accepts',0)\n # Relevant product bytes invalidate cached source evidence independently of the\n # external approval. Adapter bytes additionally change the approved dependency.\n product=root/'product/pyalamode'\n for filename in ('checker.py','model.py','project.py','integration_contracts.py'):\n  path=product/filename;old=sha(path);path.write_bytes(path.read_bytes()+b'\\n# independent M8 copied-product freshness input\\n')\n  changed=observe(filename+' actual product byte change',0,False);check(changed['product'][filename]!=old,filename+' actual product identity changed');observe(filename+' changed product warm',0,True)\n path=product/'integrations.py';old=sha(path);path.write_bytes(path.read_bytes()+b'\\n# independent changed adapter artifact\\n')\n changed=observe('adapter actual bytes stale approval',1,False);check(changed['product']['integrations.py']!=old,'adapter bytes alter actual product identity')\n observe('adapter stale rejected build',1,None,False,True);approve('adapter explicit current reapproval');observe('adapter current reapproved',0,False)\n # Cross-publication expiry: initial approval must pass, then current UTC crosses\n # before publication. The isolated delay is product-control instrumentation.\n crossing=r'''import json,time\nfrom datetime import datetime,timezone,timedelta\nfrom pathlib import Path\nimport pyalamode.project as project_api\nfrom m08_common import prepare,policy_text\nroot=Path(PROJECT)\npolicy,snapshot=prepare(root,{'id':'crossing expiry','files':{'core.py':root.joinpath('core.py').read_text()}})\nexpiry=(datetime.now(timezone.utc)+timedelta(seconds=2)).replace(microsecond=0)\nfor entry in policy['integration_approvals']:entry['expires_at']=expiry.strftime('%Y-%m-%dT%H:%M:%SZ')\nroot.joinpath('pyproject.toml').write_text(policy_text(policy))\noriginal=project_api._guard_plan\ncalls=[]\ndef delayed(*args,**kwargs):\n calls.append('initial admitted plan');original(*args,**kwargs);time.sleep(2.1)\nproject_api._guard_plan=delayed\ntry:result=project_api.build_paths(root=root,output=root/'artifact')\nfinally:project_api._guard_plan=original\nassert calls and result.status==1 and not root.joinpath('artifact').exists()\nprint(json.dumps({'status':result.status,'artifact_exists':False,'expired':datetime.now(timezone.utc)>=expiry,'calls':calls,'contracts':[c.__dict__ for f in result.results for c in f.contracts]}))\n'''\n call('actual UTC approval crosses before publication',crossing.replace('PROJECT',repr(str(project))))\n report={'inputs':{'m08_identity_probe.py':sha(__file__),'m08_common.py':sha(OUT/'m08_common.py')},'assertions':checks,'rows':rows,'original_native':original_native,'copied_interpreter_sha256':sha(interpreter),'copied_core_sha256':sha(core_copy),'original_interpreter_sha256':sha(Path(sys.executable).resolve()),'original_core_sha256':sha(core_original),'shared_native':shared_native,'shared_installation_unchanged':all(sha(Path(v['path']))==v['sha256'] for v in shared_native.values()),'literal_fixture':fixture,'literal_observation_source':source,'literal_approval_source':approval_source,'literal_runtime_source':runtime_source}\n check(report['copied_interpreter_sha256']==report['original_interpreter_sha256'] and report['copied_core_sha256']==report['original_core_sha256'],'real copied interpreter/core equal original foundations')\n # No copied path escapes this TemporaryDirectory; report retains all observed\n # actual digests and paths after the isolated checkout is removed.\nreport['assertions']=checks\n(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-identity-observations.json')).write_text(json.dumps(report,indent=2)+'\\n')\nprint(json.dumps({'assertions':checks,'recorded_rows':len(rows),'subprocesses':len(rows)}))\n"
}
```

## Installed-suite source-location correction

All 18 focused harnesses passed on both fresh installed targets. The first complete-suite launch used original checkout test paths; a new test derives its child PYTHONPATH from `__file__.parents[1]`, injecting the source package beside the installed package. Nonexecuting discovery correctly reported that second package candidate unresolved, causing two sentinel subtest assertions to fail. The unchanged tests and examples are now copied into a separate fixture location containing no product package, with every copied Python file checked against the original before and after execution. This correction preserves every test expectation and ensures the suite exercises the installed wheel. The current complete controller supersedes prior controller text. SHA-256 `61792b79baca7755c42c5c023ef0d22c5b48c665fc15a41c2956366d8f8d2b47`.

```python
import hashlib,json,platform,re,subprocess,sys,time
from pathlib import Path
import pyalamode
from pyalamode.integration_contracts import integration_snapshot
OUT=Path(__file__).parent;ROOT=Path(sys.argv[1]);NAME=sys.argv[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source_map():
 paths=[ROOT/'pyproject.toml',ROOT/'README.md']
 for area in ('pyalamode','tests','examples','benchmarks'):paths.extend((ROOT/area).rglob('*.py'))
 result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths)) if '__pycache__' not in p.parts}
 for p in sorted(OUT.glob('*.py')):result['reviewer:'+p.name]=digest(p)
 for name in ('literal-cases.json','m06-literal-cases.json','literal-layouts.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json','local-writer-cases.json','m08-literal-cases.json','m08-runtime-inputs.json','corrected-root-freeze.json'):result['reviewer:'+name]=digest(OUT/name)
 return result
def installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}
def suite_fixture_map():
 return {('tests' if p.is_relative_to(OUT/'suite-tests') else 'examples')+'/'+p.relative_to(OUT/'suite-tests' if p.is_relative_to(OUT/'suite-tests') else OUT/'examples').as_posix():digest(p) for area in ('suite-tests','examples') for p in sorted((OUT/area).rglob('*.py')) if '__pycache__' not in p.parts}
before=source_map();installed_before=installed_map();freeze=json.loads((OUT/'corrected-root-freeze.json').read_text())
fixture_before=suite_fixture_map();assert fixture_before and all(before[k]==v for k,v in fixture_before.items())
assert len(installed_before)==17
assert all(before[k]==v for k,v in installed_before.items())
assert all(before[k]==v for k,v in freeze['paths'].items())
assert not Path(pyalamode.__file__).resolve().is_relative_to(ROOT.resolve()),'must use freshly installed wheel outside checkout'
installed_snapshot_before=integration_snapshot()
assert not {'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys()
results=[]
scripts=('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','freshness_probe.py','m06_runtime_probe.py','m06_project_probe.py','m06_cli_probe.py','m06_nonexecution_probe.py','m06_freshness_probe.py','environment_probe.py','m08_static_probe.py','m08_runtime_probe.py','m08_project_probe.py','m08_cli_probe.py','m08_nonexecution_probe.py','m08_identity_probe.py','m08_version_probe.py')
for script in scripts:
 target=NAME+'-'+script.removesuffix('_probe.py')+'.json';started=time.perf_counter()
 ran=subprocess.run([sys.executable,str(OUT/script),target],cwd=OUT,capture_output=True,text=True)
 row=dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=target);results.append(row)
 (OUT/(NAME+'-progress.json')).write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({'script':script,'status':ran.returncode,'elapsed_seconds':row['elapsed_seconds'],'summary':ran.stdout.strip()}),flush=True)
 if ran.returncode:print(ran.stderr,flush=True);raise SystemExit(ran.returncode)
started=time.perf_counter()
ran=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(OUT/'suite-tests'),'-p','m*.py'],cwd=OUT,capture_output=True,text=True)
suite=dict(status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr)
if ran.returncode:print(json.dumps(suite));raise SystemExit(ran.returncode)
match=re.search(r'Ran (\d+) tests in ([\d.]+)s',ran.stderr);assert match
suite.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)));assert suite['tests']==320
after=source_map();installed_after=installed_map();installed_snapshot_after=integration_snapshot()
fixture_after=suite_fixture_map();assert fixture_before==fixture_after
assert before==after;assert installed_before==installed_after;assert installed_snapshot_before==installed_snapshot_after
report=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,base_prefix=sys.base_prefix,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),abiflags=sys.abiflags,filesystem_encoding=sys.getfilesystemencoding(),filesystem_errors=sys.getfilesystemencodeerrors(),utf8_mode=sys.flags.utf8_mode,package_path=pyalamode.__file__),results=results,suite=suite,source_before=before,source_after=after,installed_product_before=installed_before,installed_product_after=installed_after,installed_snapshot_before=installed_snapshot_before,installed_snapshot_after=installed_snapshot_after,suite_fixture_before=fixture_before,suite_fixture_after=fixture_after,source_unchanged=True,installed_source_equal=True,corrected_freeze_sha256=digest(OUT/'corrected-root-freeze.json'))
(OUT/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'name':NAME,'suite':suite['tests'],'suite_seconds':suite['reported_seconds'],'focused_scripts':len(results),'source_files':len(before),'installed_product_files':len(installed_before),'unchanged':True}),flush=True)
```

## Fixed actual unsafe-output artifact supplement

Before observing this supplement, all three guard modes must build the unchanged U-explicit-new-core source, keep prior unsafe behavior and initialization unchecked, publish no external trust for the new pure total, and execute the actual generated module from artifact cwd. Mutating the old raw list must leave the validated Vector and total 3 unchanged. The six actual console/stock subprocesses also retain cwd, sys.path, exact imported installed product and console provenance. This is a separate focused artifact assertion, not extra source admission or a change to the fixed 176 cases. Harness SHA-256 `1666a8ba01e0b2565dd2189bb0963a867bc7002544806abcc1b9d4155462d05d`.

```python
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
import pyalamode
OUT=Path(__file__).resolve().parents[1];rows=[];checks=0
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def check(value,label):
 global checks
 checks+=1
 if not value:raise AssertionError(label)
case=next(c for c in json.loads((OUT/'m08-literal-cases.json').read_text()) if c['id']=='U-explicit-new-core')
source=case['files']['core.py']
stock=r'''import json,sys
from pathlib import Path
import core,pyalamode
from pyalamode import unsafe,Vector
assert Path(core.__file__).resolve().is_relative_to(Path.cwd().resolve())
assert core.result==3 and type(core.snapshot) is Vector
core.raw.append(9)
assert list(core.snapshot)==[1,2] and core.total(core.snapshot)==3
assert core.vendor.__dict__=={} and unsafe(scope='ordinary',rationale='identity')(core.vendor) is core.vendor
if MODE!='off':
 from pyalamode_exports.core import total
 assert total.__wrapped__ is core.total and total(core.snapshot)==3
print(json.dumps({'module_file':core.__file__,'product_file':pyalamode.__file__,'cwd':str(Path.cwd()),'sys_path':sys.path,'result':core.result,'snapshot':list(core.snapshot),'mutated_raw':core.raw,'mode':MODE}))
'''
console=Path(sys.executable).parent/'pyalamode'
check(console.is_file(),'actual installed console exists')
check(Path(pyalamode.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()),'product belongs to installed environment')
for mode in ('off','exports','debug'):
 with tempfile.TemporaryDirectory(prefix='m08-unsafe-artifact-') as directory:
  root=Path(directory);(root/'core.py').write_text(source)
  policy='[tool.pyalamode]\nboundary_guards='+json.dumps(mode)+'\n'
  if mode!='off':policy+='guarded_exports=["core:total"]\n'
  (root/'pyproject.toml').write_text(policy);artifact=root/'artifact'
  args=[str(console),'build','--root',str(root),'--output',str(artifact),'--json']
  ran=subprocess.run(args,cwd=OUT,capture_output=True,text=True);check(ran.returncode==0,mode+' actual console build '+ran.stderr)
  value=json.loads(ran.stdout);file=next(f for f in value['files'] if Path(f['path']).name=='core.py');contract=next(c for c in file['contracts'] if c['name']=='total')
  check(value['verified'] and not contract['external_assumptions'] and not contract['required_effects'],mode+' new isolated calculation only')
  check(file['initialization_evidence']=='unchecked ordinary module initialization',mode+' prior ordinary behavior stays unchecked')
  check(len(file['unsafe_adapters'])==1 and file['unsafe_adapters'][0]['source_evidence']=='unchecked ordinary unsafe adapter',mode+' unsafe declaration visible')
  evidence=json.loads((artifact/'pyalamode-evidence.json').read_text());check(evidence['files'][0]['unsafe_adapters']==file['unsafe_adapters'],mode+' artifact retains unsafe provenance')
  if mode!='debug':check((artifact/'core.py').read_text()==source,mode+' unchanged copied source')
  rows.append({'label':mode+' actual console build','command':args,'cwd':str(OUT),'status':ran.returncode,'stdout':ran.stdout,'stderr':ran.stderr,'artifact_files':evidence['artifact_files']})
  env=dict(os.environ);env['PYTHONPATH']=str(artifact);program=stock.replace('MODE',repr(mode))
  run=subprocess.run([sys.executable,'-c',program],cwd=artifact,env=env,capture_output=True,text=True)
  check(run.returncode==0,mode+' actual unsafe shell output isolation '+run.stderr)
  observed=json.loads(run.stdout);check(Path(observed['module_file']).resolve().is_relative_to(artifact.resolve()),mode+' actual generated artifact imported')
  rows.append({'label':mode+' actual stock artifact','command':[sys.executable,'-c',program],'cwd':str(artifact),'status':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
report={'inputs':{'m08_unsafe_artifact.py':sha(__file__),'m08-literal-cases.json':sha(OUT/'m08-literal-cases.json')},'assertions':checks,'subprocesses':len(rows),'rows':rows,'literal_source':source,'literal_stock_source':stock,'installed_provenance':{'cwd':str(Path.cwd()),'sys_path':sys.path,'prefix':sys.prefix,'executable':sys.executable,'product_file':pyalamode.__file__,'console_path':str(console),'console_sha256':sha(console),'package':{'pyalamode/'+p.name:sha(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}}}
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'm08-unsafe-artifact.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assertions':checks,'rows':len(rows),'subprocesses':len(rows)}))
```

The relocated suite also retains the literal `tests/fixtures` directory name: the first relocation used `suite-tests`, so two unchanged M1 tests could not open their authored `tests/fixtures/m01/invalid_reassignment.py` path. Both platform traces showed only this missing reviewer fixture path; the sysconfig sentinel tests now passed. Renaming the copied directory to `tests` preserves all source and fixture bytes and expected outcomes. Current controller SHA-256 `fd416963843e7f8896d321dede47e35d46db9c2521c3d7d275ef4f5a89e5110b`; complete text follows.

```python
import hashlib,json,platform,re,subprocess,sys,time
from pathlib import Path
import pyalamode
from pyalamode.integration_contracts import integration_snapshot
OUT=Path(__file__).parent;ROOT=Path(sys.argv[1]);NAME=sys.argv[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source_map():
 paths=[ROOT/'pyproject.toml',ROOT/'README.md']
 for area in ('pyalamode','tests','examples','benchmarks'):paths.extend((ROOT/area).rglob('*.py'))
 result={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(set(paths)) if '__pycache__' not in p.parts}
 for p in sorted(OUT.glob('*.py')):result['reviewer:'+p.name]=digest(p)
 for name in ('literal-cases.json','m06-literal-cases.json','literal-layouts.json','supplemental-cases.json','narrowing-cases.json','writer-cases.json','local-writer-cases.json','m08-literal-cases.json','m08-runtime-inputs.json','corrected-root-freeze.json'):result['reviewer:'+name]=digest(OUT/name)
 return result
def installed_map():return {'pyalamode/'+p.name:digest(p) for p in sorted(Path(pyalamode.__file__).parent.glob('*.py'))}
def suite_fixture_map():
 return {('tests' if p.is_relative_to(OUT/'tests') else 'examples')+'/'+p.relative_to(OUT/'tests' if p.is_relative_to(OUT/'tests') else OUT/'examples').as_posix():digest(p) for area in ('tests','examples') for p in sorted((OUT/area).rglob('*.py')) if '__pycache__' not in p.parts}
before=source_map();installed_before=installed_map();freeze=json.loads((OUT/'corrected-root-freeze.json').read_text())
fixture_before=suite_fixture_map();assert fixture_before and all(before[k]==v for k,v in fixture_before.items())
assert len(installed_before)==17
assert all(before[k]==v for k,v in installed_before.items())
assert all(before[k]==v for k,v in freeze['paths'].items())
assert not Path(pyalamode.__file__).resolve().is_relative_to(ROOT.resolve()),'must use freshly installed wheel outside checkout'
installed_snapshot_before=integration_snapshot()
assert not {'pyalamode.integrations','binascii','_sha2'} & sys.modules.keys()
results=[]
scripts=('static_probe.py','runtime_probe.py','project_probe.py','cli_probe.py','freshness_probe.py','m06_runtime_probe.py','m06_project_probe.py','m06_cli_probe.py','m06_nonexecution_probe.py','m06_freshness_probe.py','environment_probe.py','m08_static_probe.py','m08_runtime_probe.py','m08_project_probe.py','m08_cli_probe.py','m08_nonexecution_probe.py','m08_identity_probe.py','m08_version_probe.py')
for script in scripts:
 target=NAME+'-'+script.removesuffix('_probe.py')+'.json';started=time.perf_counter()
 ran=subprocess.run([sys.executable,str(OUT/script),target],cwd=OUT,capture_output=True,text=True)
 row=dict(script=script,status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr,output=target);results.append(row)
 (OUT/(NAME+'-progress.json')).write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({'script':script,'status':ran.returncode,'elapsed_seconds':row['elapsed_seconds'],'summary':ran.stdout.strip()}),flush=True)
 if ran.returncode:print(ran.stderr,flush=True);raise SystemExit(ran.returncode)
started=time.perf_counter()
ran=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(OUT/'tests'),'-p','m*.py'],cwd=OUT,capture_output=True,text=True)
suite=dict(status=ran.returncode,elapsed_seconds=time.perf_counter()-started,stdout=ran.stdout,stderr=ran.stderr)
if ran.returncode:print(json.dumps(suite));raise SystemExit(ran.returncode)
match=re.search(r'Ran (\d+) tests in ([\d.]+)s',ran.stderr);assert match
suite.update(tests=int(match.group(1)),reported_seconds=float(match.group(2)));assert suite['tests']==320
after=source_map();installed_after=installed_map();installed_snapshot_after=integration_snapshot()
fixture_after=suite_fixture_map();assert fixture_before==fixture_after
assert before==after;assert installed_before==installed_after;assert installed_snapshot_before==installed_snapshot_after
report=dict(name=NAME,environment=dict(python=sys.version,executable=sys.executable,base_prefix=sys.base_prefix,platform=platform.platform(),machine=platform.machine(),gil_enabled=sys._is_gil_enabled(),abiflags=sys.abiflags,filesystem_encoding=sys.getfilesystemencoding(),filesystem_errors=sys.getfilesystemencodeerrors(),utf8_mode=sys.flags.utf8_mode,package_path=pyalamode.__file__),results=results,suite=suite,source_before=before,source_after=after,installed_product_before=installed_before,installed_product_after=installed_after,installed_snapshot_before=installed_snapshot_before,installed_snapshot_after=installed_snapshot_after,suite_fixture_before=fixture_before,suite_fixture_after=fixture_after,source_unchanged=True,installed_source_equal=True,corrected_freeze_sha256=digest(OUT/'corrected-root-freeze.json'))
(OUT/(NAME+'-final.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'name':NAME,'suite':suite['tests'],'suite_seconds':suite['reported_seconds'],'focused_scripts':len(results),'source_files':len(before),'installed_product_files':len(installed_before),'unchanged':True}),flush=True)
```

## Terminal independent observations

The corrected frozen candidate passes independent conformance on actual CPython 3.13.1 standard GIL macOS and networking-disabled Linux, using the same fresh installed wheel. The 320 test methods pass in 14.168 seconds and 33.891 seconds respectively. Both targets also pass all 18 focused harnesses, 532 inherited plus 176 new fixed source/policy cases (708 total), and 57 fixed runtime input rows (27 results and 30 ValueError cases). The new source corpus has 37 admissions, 119 strict refusals and 20 tooling failures. Invalid ordinary representations are separate from the 57 exact-bytes runtime rows.

These counts describe different units. Test methods are counted from the suite and AST, source cases from frozen literal entries, runtime rows from their input file, and the following counts from each harness's explicit parent check counter. They do not count every Python assertion executed inside child processes or unittest methods. Stock native-integration child programs separately report 4/14/15 assertions for off/exports/debug.

| M8 focused harness | Counted parent checks, macOS / Linux | Recorded rows | Child subprocesses, macOS / Linux |
| --- | ---: | ---: | ---: |
| Source/policy literals | 972 / 972 | 176 | 0 / 0 |
| Known results, failures, invalid representations, hooks | 242 / 242 | 57 fixed runtime rows | 3 / 3 |
| Cross-module, cache, override and real UTC expiry | 42 / 42 | 16 | 0 / 0 |
| CLI/check/build/audit/explain and actual guarded artifacts | 136 / 136 | 77 | 77 / 77 |
| Fresh metadata/configuration nonexecution | 71 / 71 | 26 | 26 / 26 |
| Copied actual runtime/backend/product identities | 153 / 153 | 41 | 41 / 41 |
| Actual separately installed CPython 3.12.8 refusal | 6 / 0 | 3 / 0 | 3 / 0 |
| Actual unsafe-output/new-computation artifacts | 25 / 25 | 6 | 6 / 6 |

The new M8 parent counters sum to 1,647 on macOS and 1,641 on Linux; its explicit child counts sum to 156 and 153. The complete controller launches 18 harness processes and one suite process per target; inherited harness children and unittest children are not folded into the new-M8 child subtotal. The final source maps contain 114 relevant source/harness/input identities, the installed package contains exactly 17 Python files, and the relocated tests/examples contain 49 Python fixtures. Each map equals current source and its before/after counterpart, and shared source/package/fixture maps equal across platforms. Installed dependency identities differ by actual platform, paths, interpreter build and native bytes; each approval is local and explicit. The original shared native installation remains byte-for-byte unchanged after isolated mutation probes.

Actual appended bytes to each copied native extension invalidate formerly approved cold/full-warm/no-cache and build evidence. Failed builds publish no artifact. Explicit approval of the changed bytes restores admission and actual changed native modules execute the fixed known results from their copied paths. Missing native bytes produce unresolved/no digest and refusal. Real copied checker/model/project/catalog changes invalidate source cache evidence; changed adapter bytes additionally invalidate external approval. Real UTC expiry refuses warm/partial/no-cache/build, including a crossing after an initially admitted guard plan. Full trust remains through checked wrappers and failure handling, while effects, known failures, ordinary setup and unchecked unsafe behavior remain separate.

Application/default/decorator/annotation/backend/product-shadow/configuration sentinels execute zero times during check/build/explain/discovery. Inactive sysconfig selectors and module shadows safely leave fixed-path identities and normal denial/approval classification intact. Actual unsupported CPython 3.12.8 returns no supported identity and check/build target status 2; Linux has no alternate installed interpreter, so no alternate-version observation is claimed there. Native Error constructor/base mutation controls demonstrate the underlying prior effects, while analyzed writer cases refuse. The unsafe supplement executes an ordinary vendor shell and then a new pure total; later mutation of raw data preserves the isolated Vector and total 3. It verifies actual generated `core.__file__` from artifact cwd for every mode.

There is no product blocker in this fixed corpus. Frozen runtime support-cost measurements are reviewed separately below when supplied by the helper. Human integration usefulness, authoring time and review effort remain **UNMEASURED** under the published target-user protocol. Root owns milestone acceptance and Git.

The complete raw outputs are in `/tmp/pyalamode-m08-review`, with hashes and reduced published fields below. Original and corrected fixture/harness texts above make the observations reproducible; historical failing candidates and reviewer path/count corrections do not change the fixed expectations. The fresh wheel SHA-256 is `2dfabb006196b2e16b955225934621cd89a2324b5fdad2aae8515ec259e51833`, rebuilt from the corrected source copy and installed without network/dependencies on Linux. The Docker image is `python:3.13.1-slim` ID `sha256:0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae`. The finished reviewer container was removed after all observations.

Published complete before/after-equivalent source/package/fixture maps, actual current backend identities, local operation digests, fixed transition outcomes, installed provenance and raw-output hashes (shared maps occur once; complete rich contracts stay in the raw focused outputs):

```json
{
  "corrected_freeze_sha256": "18fc42d5f4d76160a1a74edf39882f044024847888ef2774d85cc77daa566712",
  "wheel_sha256": "2dfabb006196b2e16b955225934621cd89a2324b5fdad2aae8515ec259e51833",
  "docker_image_id": "sha256:0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae",
  "test_methods": 320,
  "literal_sources": {
    "inherited": 532,
    "m08": 176,
    "m08_admit": 37,
    "m08_strict_refusal": 119,
    "m08_tooling": 20
  },
  "runtime_literal_inputs": {
    "rows": 57,
    "results": 27,
    "ValueError": 30
  },
  "source_map": {
    "README.md": "5438e9d196333965153549fb5bb6af7368cbe48d1d99e5466f3cd3b757dae452",
    "benchmarks/m01_scalar.py": "c84afa054ee636c9a9bdcf001894043b26b81ffd1adb96398c1fae89056a6132",
    "benchmarks/m02_modules.py": "5d28d376907f3aa27810bf04a1d04b000fd26869568826e44b3e65d4765f790c",
    "benchmarks/m03_collections.py": "f77088969476fe4657ae61fb78b80f1494c28b9d86ba79be1d90ddd49066b141",
    "benchmarks/m04_boundaries.py": "be56c03b4bd1845baf5cd1e37071e8dce94a0e0430780d45bcf8d4a88b1ffef5",
    "benchmarks/m05_effects.py": "83b54c93ecc4240f340bcc88ba20b16f8a640306d49f784c26662cfe22bb22d3",
    "benchmarks/m06_domains.py": "7a192a8cfed4b29c22d990414d03a49ed6c525c428a2874684368d393d7275af",
    "benchmarks/m07_standard.py": "a5386cbd9e38000b3d00912073429288405a614405b5f50e2ea971218c41ad86",
    "benchmarks/m08_integrations.py": "e5189e5b6b50af43bcca10714549214afe5bdc47704d42775e15df7fe6b497dd",
    "examples/collections/__init__.py": "4bb3c9c16ae4b554d4fa71a406310b1807033b61c7ec2ced586f0616e7eb2418",
    "examples/collections/core.py": "f9b05387462f4ae1009df83fe8d407b07d4767e3d567e307a14ec09185ca61db",
    "examples/collections/demo.py": "039cc3ca4b04c72ecced2276037a4182866a16c18f10c26d0d2cf8389fb2fa98",
    "examples/domains/demo.py": "130c85d8e2790cd049f0c60adc07a644ef3f63c9a295735ebde4d43ca728474d",
    "examples/domains/domain.py": "3aea9061e61670529e9ceb9bdea477c8af359ab1d96ddf60596f18cd0bc0ac12",
    "examples/effects/__init__.py": "976d6c1731a16ecf67980cfaddeed34d9f0182df1aeabb5a8e60720709a1f8b6",
    "examples/effects/core.py": "f18f5a58a03e37bb619319121deaf8a59a2ef5fc516142e342a433e23ded174c",
    "examples/effects/demo.py": "9f4d1340e900f8232461e59fcfa720f79b28a13fdc1dc168c7eb24c69dfe40dd",
    "examples/integrations/core.py": "520b36577f72b03e640e2a91a68801287ada5f98249c1bb5a15d3da55bba2ec1",
    "examples/integrations/demo.py": "4de78341e953a3fbd6bade6e04011d7b30d9c472a4f76de35851aa3482910d50",
    "examples/integrations/review_policy.py": "48b39595bc531f610d37755663a59313f6a0688679305b709037c41f17e750ca",
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
    "pyalamode/__init__.py": "c695ea8253ae3fa75e978d5b1d68e2f7a0a54ab41323849e096fffa5998a6bab",
    "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
    "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
    "pyalamode/checker.py": "65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5",
    "pyalamode/cli.py": "a72e1c2d17a68c94060bd06e3b16225894ec1a35bca8d88b89f63ff7e749f744",
    "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
    "pyalamode/effects.py": "1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d",
    "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
    "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
    "pyalamode/integration_contracts.py": "f9f2d0d0e77f8505c8839f561212b76d9f4e757f2edde89687ded9030b614567",
    "pyalamode/integrations.py": "3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e",
    "pyalamode/model.py": "3c13736b6230365ac5a4ad36ab3e639ef24c1e74b65e6163cf5dcae1556b7513",
    "pyalamode/project.py": "ee8b098b29fdf0f3fc414b275a5f9b1faf4ef6d09cf07015be9eb1f1cd3a1b81",
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
    "tests/m07_standard.py": "3469d350d5aaf2beac2e61f84e3aca7cbd7ba449c0c196e12fb0f4ff401265b5",
    "tests/m08_integrations.py": "f80818e30eff9789f5cdca7d8fab039a6371c51a8245505797208bc35c31ba5f",
    "tests/m08_runtime.py": "38ad79083ff06804f5cd6ba39c6ac4fe708c3cccc799422946df42789a871b1c",
    "reviewer:cli_probe.py": "251cc975f42f3b3c678021fa4cd8afea1e8a1474a00aee8c4495c484518fed0e",
    "reviewer:environment_probe.py": "2b16da1d5c5bdc1132c00e2a92b4c3c1aca27c5cc49edf5f1c610b750ad99b49",
    "reviewer:final_probe.py": "9a67f08324f1edd298406f750b7f53be37651a058d7b71a1b68b7bb0925ae369",
    "reviewer:freshness_probe.py": "eb899484a5630a667ffd58e67b9a6c71725df31995e8ca75b486961046c14660",
    "reviewer:m06_cli_probe.py": "be44b9bf2d611fa580c5d88045c373f78ef4671246dff7fab85abc9e5180799a",
    "reviewer:m06_freshness_probe.py": "e981fdee013e9c2140bbf619004723eec5d3fdf11706753b64552d27dd8e6d39",
    "reviewer:m06_nonexecution_probe.py": "d8fd3094bf9e6daa5eeefa6bd19f9ef581ddc1b35e858973fc49fa110d509ef4",
    "reviewer:m06_project_probe.py": "e9dd75392a8198925edf7641dce3a9178abfb132048ac80c1e20a75f4cad854e",
    "reviewer:m06_runtime_probe.py": "c8eef2d0cb8f4d486cddaa0f7b940b4e5f17b4518541159cb531c559cd989e8b",
    "reviewer:m08_cli_probe.py": "11a04f0676d95d07d4ff66caaa473090da2e68cc802d17ece0af8f6acfc0dbdd",
    "reviewer:m08_common.py": "6df32e2488e0a9ce5b704d898e56a0e0d0d986632f8be5fdaf76a5e0212db54e",
    "reviewer:m08_final_probe.py": "fd416963843e7f8896d321dede47e35d46db9c2521c3d7d275ef4f5a89e5110b",
    "reviewer:m08_identity_probe.py": "07be7351a293f59cdfbcfcd38ee82edfdaaec3a83606d943ef6996124fd93492",
    "reviewer:m08_nonexecution_probe.py": "841bf69e26811207e21fa9b54dacf7b1f54ce43d625db2dbfe52cacbd43ee9ee",
    "reviewer:m08_project_probe.py": "3e8186bef397d0baad2e8d0a34b306a65af74a80fab225c780ad43b73623caee",
    "reviewer:m08_runtime_probe.py": "fe8bb92e152d594ab96f8263ba5f9ef474993e29852b64e51a2cc14e5d1239fd",
    "reviewer:m08_static_probe.py": "84e7e2a17db6e15a939b7aea98b53e26b5d57a33f6c2feb33141a988d20b9777",
    "reviewer:m08_version_probe.py": "240ea4e25b85dfd036f3d4f0556588176208587a757956ed7811abb33507b49a",
    "reviewer:make_cases.py": "d3de5400f1d0238e4a46e66f2a699920cb4f62afdbba90683569a27f43d6b5c6",
    "reviewer:make_layouts.py": "bd1e4e48627d32ea034aab2e987b5ebe87cab955587487edbb6bb01e9e61c78e",
    "reviewer:make_local_writers.py": "57ebee5191e62d22f3efb1c0e809857034d55d9c2f408d65901af9fd5fcf38cc",
    "reviewer:make_m08_cases.py": "faeba7fcf43bac57a0bd622a21c87a6f1d335ab26060be88d171fe55e4958f0c",
    "reviewer:make_m08_runtime_inputs.py": "436efea76be71e6393660d882f52fd903bd76d71c75e3a7a02608ccc212e5daf",
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
    "reviewer:local-writer-cases.json": "d1099a5c22faa49d08b65cb2eaf9d4bdc004cbd664c49d7d0ef83c1f870b53f3",
    "reviewer:m08-literal-cases.json": "4a83d211d8b72fc8cf175bf5323042000933e300efd20416da7e14dc51fc5b74",
    "reviewer:m08-runtime-inputs.json": "60434fd49760244f261621521e757eedc6461544996b746b750a21edc742c0f8",
    "reviewer:corrected-root-freeze.json": "18fc42d5f4d76160a1a74edf39882f044024847888ef2774d85cc77daa566712"
  },
  "installed_product_map": {
    "pyalamode/__init__.py": "c695ea8253ae3fa75e978d5b1d68e2f7a0a54ab41323849e096fffa5998a6bab",
    "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
    "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
    "pyalamode/checker.py": "65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5",
    "pyalamode/cli.py": "a72e1c2d17a68c94060bd06e3b16225894ec1a35bca8d88b89f63ff7e749f744",
    "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
    "pyalamode/effects.py": "1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d",
    "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
    "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
    "pyalamode/integration_contracts.py": "f9f2d0d0e77f8505c8839f561212b76d9f4e757f2edde89687ded9030b614567",
    "pyalamode/integrations.py": "3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e",
    "pyalamode/model.py": "3c13736b6230365ac5a4ad36ab3e639ef24c1e74b65e6163cf5dcae1556b7513",
    "pyalamode/project.py": "ee8b098b29fdf0f3fc414b275a5f9b1faf4ef6d09cf07015be9eb1f1cd3a1b81",
    "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
    "pyalamode/standard.py": "b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9",
    "pyalamode/standard_contracts.py": "cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a",
    "pyalamode/variants.py": "02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d"
  },
  "copied_test_example_map": {
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
    "tests/m07_standard.py": "3469d350d5aaf2beac2e61f84e3aca7cbd7ba449c0c196e12fb0f4ff401265b5",
    "tests/m08_integrations.py": "f80818e30eff9789f5cdca7d8fab039a6371c51a8245505797208bc35c31ba5f",
    "tests/m08_runtime.py": "38ad79083ff06804f5cd6ba39c6ac4fe708c3cccc799422946df42789a871b1c",
    "examples/collections/__init__.py": "4bb3c9c16ae4b554d4fa71a406310b1807033b61c7ec2ced586f0616e7eb2418",
    "examples/collections/core.py": "f9b05387462f4ae1009df83fe8d407b07d4767e3d567e307a14ec09185ca61db",
    "examples/collections/demo.py": "039cc3ca4b04c72ecced2276037a4182866a16c18f10c26d0d2cf8389fb2fa98",
    "examples/domains/demo.py": "130c85d8e2790cd049f0c60adc07a644ef3f63c9a295735ebde4d43ca728474d",
    "examples/domains/domain.py": "3aea9061e61670529e9ceb9bdea477c8af359ab1d96ddf60596f18cd0bc0ac12",
    "examples/effects/__init__.py": "976d6c1731a16ecf67980cfaddeed34d9f0182df1aeabb5a8e60720709a1f8b6",
    "examples/effects/core.py": "f18f5a58a03e37bb619319121deaf8a59a2ef5fc516142e342a433e23ded174c",
    "examples/effects/demo.py": "9f4d1340e900f8232461e59fcfa720f79b28a13fdc1dc168c7eb24c69dfe40dd",
    "examples/integrations/core.py": "520b36577f72b03e640e2a91a68801287ada5f98249c1bb5a15d3da55bba2ec1",
    "examples/integrations/demo.py": "4de78341e953a3fbd6bade6e04011d7b30d9c472a4f76de35851aa3482910d50",
    "examples/integrations/review_policy.py": "48b39595bc531f610d37755663a59313f6a0688679305b709037c41f17e750ca",
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
    "examples/standard/demo.py": "600bc2cb16d69c4924a1764da58307025da73fe47a55b5a5b536c51c4b0dd444"
  },
  "cross_platform_maps_equal": true,
  "raw_manifest": {
    "corrected-root-freeze.json": "18fc42d5f4d76160a1a74edf39882f044024847888ef2774d85cc77daa566712",
    "linux-final-unsafe.json": "4620435bdefd1c3c16b1daf78177e7b7615b465f6e19ce874a41f29674a6cdb4",
    "linux-terminal-cli.json": "65f839631cd060acf84221c2db3cc00acbefdfbe37f7e9bec1c4325168009d39",
    "linux-terminal-environment.json": "f5b358b20942ffb004abdc039ffaf15948a32d619cb5d3033136ac0a3005317f",
    "linux-terminal-final.json": "8c3d0236f8ac4662c72a6896f04e5896a47aa75e93cc46ec76c72361efeb4103",
    "linux-terminal-freshness.json": "196509bfd0cd4bc26c25e998cc61f141c68aede6060471a213761e1e0066da46",
    "linux-terminal-m06_cli.json": "a0423f6551697491a24ab908030cf31d93e6ada348c3c1f0be9c161f63f49e97",
    "linux-terminal-m06_freshness.json": "d2c6ba15ef95807c8161d1432a6b687da637de54cdc4273720a669702860835c",
    "linux-terminal-m06_nonexecution.json": "87c3efb49c233af84d75394d697f8033ffeebe612f322d8f17d8a82ffbcdbc73",
    "linux-terminal-m06_project.json": "158d3815cceac4933156a96d132df85446ccea8a896117f1c5622bb0532d7b5f",
    "linux-terminal-m06_runtime.json": "169ab77e5ed30b06aa211e4a7850f5d40d391d8c888ca60af89dac660b6f66ce",
    "linux-terminal-m08_cli.json": "4317dd82999df1aeb828db6a0935eeb3db3f3e97d57b0dfb625617920ee33fc1",
    "linux-terminal-m08_identity.json": "6871f8ffb1c539437b3676a8c64b24ecb9e3f956c64c914b441e532ac68d92f7",
    "linux-terminal-m08_nonexecution.json": "2cd66f50a17d5396d0705a0f0ff107578dd838101a32ac7d1b2ba2acb5aa8eda",
    "linux-terminal-m08_project.json": "b319bdf4bc74f0f75673e0eff5b1d40e6b0300f19b6461a927c800e8a169efcc",
    "linux-terminal-m08_runtime.json": "d1969251dd0ebd5a2c4cf2caa39809c12c6840fe7289f0f38e298a5d0e2560f0",
    "linux-terminal-m08_static.json": "4a2e2c2e2b7893d4c400a56ba6b481bc054437699f2ad4dec97e178cd1847f57",
    "linux-terminal-m08_version.json": "b277d29326f6ea76c9cd62280565617251c7d419c53aef483d19ec94eb271263",
    "linux-terminal-progress.json": "8192397c971343f53ae5b1e25706de85c1236ae5a2651a267035d3b457d7d1b1",
    "linux-terminal-project.json": "fca4e5187988f19506820426dee6c835bbfff9949dd1eea5b5b492a752066c93",
    "linux-terminal-runtime.json": "19786871efd8c627af149e6187e0011fbde121e13dcdea78c6367c014e76004e",
    "linux-terminal-static.json": "5cd0d0df79db3416ef427e8a46ace3191f08fb340ebefb01c1811e85cef884b9",
    "native-final-unsafe.json": "d241c4967ab1a472e2176f7e5623266cdd193307e243600606f87cf920d6fa41",
    "native-terminal-cli.json": "a77569618a9a461c499fc732424abba015a4ae17b37953915bdc3ba959fa9d56",
    "native-terminal-environment.json": "a63cc5b715839cb95f9f0e328373a66c8ad7ecbc0ea689b216fdffadc204d150",
    "native-terminal-final.json": "cd3304befbd50c34f82a235699e8fada1d24258593faa11c6d93aec5c7d42c86",
    "native-terminal-freshness.json": "5702a2aed837c12862ffb4e54afd08ea78aa63ead9235568d64dccab7d383133",
    "native-terminal-m06_cli.json": "2161442753155ac2f064c9ffa53f4ee2b4ed058be0c42cb8e108aca6fa6c1c78",
    "native-terminal-m06_freshness.json": "640d423aa0a28d52fc2078928b9b1222d376c8e4206a2fd028ba74a43b35b77b",
    "native-terminal-m06_nonexecution.json": "07c4a2098cde591e8808fbb76e4aa8fb58e5d1e5d739828c953df420ef9c61dd",
    "native-terminal-m06_project.json": "c4127f1c0014465cde2d50473f62ba8fba1346ce6128cb5b502abe33b4d2fce0",
    "native-terminal-m06_runtime.json": "169ab77e5ed30b06aa211e4a7850f5d40d391d8c888ca60af89dac660b6f66ce",
    "native-terminal-m08_cli.json": "a11ef2727e1e0f6bdafff8c6f54c86736f2fdf97cb35e524590e59fc0fb805b6",
    "native-terminal-m08_identity.json": "7bdf5292a4058d889f80366341e14de129098c08e91a5a94f8de964a6796de1a",
    "native-terminal-m08_nonexecution.json": "dcd554065f33a0b1caa07bcc3188c0ebdee1f4fe7143aa7a93c9292a74a474a6",
    "native-terminal-m08_project.json": "1476d3991ff398f67cf1e870fa0fb7258955a7b6a93684749e817237fcad6599",
    "native-terminal-m08_runtime.json": "d1969251dd0ebd5a2c4cf2caa39809c12c6840fe7289f0f38e298a5d0e2560f0",
    "native-terminal-m08_static.json": "2bcf6121c21a591237f2c81201a8e6da664c480f9fba2e1dab86380c19d491e9",
    "native-terminal-m08_version.json": "8737aa354d7f2733b78a9a8fe300d2a7aec12edf9050484ccc23f9f82401fe11",
    "native-terminal-progress.json": "34c688c54338b488b97b6c23e6e18786139ebcc61044e69632ef218c59b8943b",
    "native-terminal-project.json": "594a98ddd16601fb550ab429ce0534d8ac0dd5c6d927648462a3d8e3e83014cd",
    "native-terminal-runtime.json": "19786871efd8c627af149e6187e0011fbde121e13dcdea78c6367c014e76004e",
    "native-terminal-static.json": "5cd0d0df79db3416ef427e8a46ace3191f08fb340ebefb01c1811e85cef884b9",
    "package-build-inputs.json": "b9c7b28552d2d84c3e41bd91b4951fd60f3a11ef5de050c7fddddb31b0313e62",
    "wheels/pyalamode-0.1.0-py3-none-any.whl": "2dfabb006196b2e16b955225934621cd89a2324b5fdad2aae8515ec259e51833"
  },
  "authority_spec_sha256": "3d8f845b5b3739418062caa44db5ba51b95bc99823425bde3b4aff6cebaaee48",
  "targets": {
    "native": {
      "environment": {
        "python": "3.13.1 (main, Dec  3 2024, 17:59:52) [Clang 16.0.0 (clang-1600.0.26.4)]",
        "executable": "/private/tmp/pyalamode-m08-review/native-venv/bin/python",
        "base_prefix": "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13",
        "platform": "macOS-26.6.2-arm64-arm-64bit-Mach-O",
        "machine": "arm64",
        "gil_enabled": true,
        "abiflags": "",
        "filesystem_encoding": "utf-8",
        "filesystem_errors": "surrogateescape",
        "utf8_mode": 0,
        "package_path": "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages/pyalamode/__init__.py"
      },
      "suite": {
        "status": 0,
        "methods": 320,
        "seconds": 14.168
      },
      "before_after_equal": true,
      "installed_shared_identity": {
        "distribution": "CPython-stdlib",
        "version": "3.13.1",
        "build": "3.13.1 (main, Dec  3 2024, 17:59:52) [Clang 16.0.0 (clang-1600.0.26.4)]",
        "cache_tag": "cpython-313",
        "platform": "darwin",
        "base_prefix": "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13",
        "abiflags": "",
        "extension_suffixes": [
          ".cpython-313-darwin.so",
          ".abi3.so",
          ".so"
        ],
        "native_artifacts": {
          "binascii": {
            "path": "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/binascii.cpython-313-darwin.so",
            "sha256": "428c1263cf9326aae8e9913b9898852ce1ca0f5f3736148638af01eeb0ebaaca"
          },
          "_sha2": {
            "path": "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/_sha2.cpython-313-darwin.so",
            "sha256": "b6bfcfe427f23d6705e084795ce320e9cf7c59c5df26250e7430a31b5c12ba62"
          }
        },
        "adapter_artifact": {
          "path": "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages/pyalamode/integrations.py",
          "sha256": "3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e"
        },
        "interpreter_executable": {
          "path": "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/bin/python3.13",
          "sha256": "d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132"
        },
        "interpreter_core": {
          "path": "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Python",
          "sha256": "424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d"
        },
        "resolution": "fixed sys.base_prefix/lib/python3.13/lib-dynload and builtin _imp extension suffix; no sysconfig getters/config-data imports or environment selectors; visible filesystem shadows refused; ordinary importer/module bindings must remain unchanged at execution",
        "native_setup_trust": "platform loader/libc or libSystem and binascii linked zlib remain disclosed foundation assumptions; selected invocation does not use zlib",
        "operation": "pyalamode.integrations.base64_decode",
        "invocation_backend": "binascii",
        "native_operations": [
          "binascii.a2b_base64(data,strict_mode=True)",
          "binascii.Error exact construction",
          "binascii.b2a_base64(decoded,newline=False)"
        ]
      },
      "operation_digests": [
        {
          "identity": "pyalamode.integrations.base64_decode",
          "contract_sha256": "61f5fa1bf491475c9d242d6cd7a14f90f98aabd5ae71f17bc18fbc7d27695585",
          "dependency_sha256": "34cef3376fd4d0bf734618e525af2388bb8dffa0e6c2710b8f7993a600a735c0",
          "admission": "denied"
        },
        {
          "identity": "pyalamode.integrations.base64_encode",
          "contract_sha256": "10ae6750641e50bc12334ca52eaf1c6ff9328b477e06cace8993f94ce7dc1d60",
          "dependency_sha256": "7d379d788795b9faf52d0e98c920ff10c75382727ab85ed3caf9fb8ef6d2c482",
          "admission": "denied"
        },
        {
          "identity": "pyalamode.integrations.sha256_digest",
          "contract_sha256": "58b9b3376483918e16f5078332d5de4fc7fd4b6053173a0d9de960bb4548ec6c",
          "dependency_sha256": "6e897db0d9862f7e42f80de18986e5f5f915a63cbc22cbd875818453dbdba36d",
          "admission": "denied"
        }
      ],
      "isolated_copies": {
        "original_native": {
          "binascii": {
            "path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-real-runtime-copy-7_dx7s_0/runtime/lib/python3.13/lib-dynload/binascii.cpython-313-darwin.so",
            "sha256": "428c1263cf9326aae8e9913b9898852ce1ca0f5f3736148638af01eeb0ebaaca"
          },
          "_sha2": {
            "path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-real-runtime-copy-7_dx7s_0/runtime/lib/python3.13/lib-dynload/_sha2.cpython-313-darwin.so",
            "sha256": "b6bfcfe427f23d6705e084795ce320e9cf7c59c5df26250e7430a31b5c12ba62"
          }
        },
        "shared_native": {
          "binascii": {
            "path": "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/binascii.cpython-313-darwin.so",
            "sha256": "428c1263cf9326aae8e9913b9898852ce1ca0f5f3736148638af01eeb0ebaaca"
          },
          "_sha2": {
            "path": "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/_sha2.cpython-313-darwin.so",
            "sha256": "b6bfcfe427f23d6705e084795ce320e9cf7c59c5df26250e7430a31b5c12ba62"
          }
        },
        "shared_installation_unchanged": true,
        "copied_interpreter_sha256": "d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132",
        "copied_core_sha256": "424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d",
        "original_interpreter_sha256": "d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132",
        "original_core_sha256": "424ea839329aebfcb02bc4a832e0ac377d9ad07d192d9d0efe4dd50dbefc7e1d"
      },
      "unsafe_artifact": {
        "assertions": 25,
        "subprocesses": 6,
        "provenance": {
          "cwd": "/private/tmp/pyalamode-m08-review",
          "sys_path": [
            "/private/tmp/pyalamode-m08-review/supplements",
            "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
            "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
            "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
            "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages"
          ],
          "prefix": "/private/tmp/pyalamode-m08-review/native-venv",
          "executable": "/private/tmp/pyalamode-m08-review/native-venv/bin/python",
          "product_file": "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages/pyalamode/__init__.py",
          "console_path": "/private/tmp/pyalamode-m08-review/native-venv/bin/pyalamode",
          "console_sha256": "00dae0301180a3f5b2cd312c8a53797ae645757efc8cdbb1ce4edfa2f0d4f76f",
          "package": {
            "pyalamode/__init__.py": "c695ea8253ae3fa75e978d5b1d68e2f7a0a54ab41323849e096fffa5998a6bab",
            "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
            "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
            "pyalamode/checker.py": "65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5",
            "pyalamode/cli.py": "a72e1c2d17a68c94060bd06e3b16225894ec1a35bca8d88b89f63ff7e749f744",
            "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
            "pyalamode/effects.py": "1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d",
            "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
            "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
            "pyalamode/integration_contracts.py": "f9f2d0d0e77f8505c8839f561212b76d9f4e757f2edde89687ded9030b614567",
            "pyalamode/integrations.py": "3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e",
            "pyalamode/model.py": "3c13736b6230365ac5a4ad36ab3e639ef24c1e74b65e6163cf5dcae1556b7513",
            "pyalamode/project.py": "ee8b098b29fdf0f3fc414b275a5f9b1faf4ef6d09cf07015be9eb1f1cd3a1b81",
            "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
            "pyalamode/standard.py": "b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9",
            "pyalamode/standard_contracts.py": "cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a",
            "pyalamode/variants.py": "02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d"
          }
        },
        "stock_results": [
          {
            "module_file": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-evakn7uz/artifact/core.py",
            "product_file": "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages/pyalamode/__init__.py",
            "cwd": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-evakn7uz/artifact",
            "sys_path": [
              "",
              "/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-evakn7uz/artifact",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
              "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages"
            ],
            "result": 3,
            "snapshot": [
              1,
              2
            ],
            "mutated_raw": [
              1,
              2,
              9
            ],
            "mode": "off"
          },
          {
            "module_file": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-8ffklppc/artifact/core.py",
            "product_file": "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages/pyalamode/__init__.py",
            "cwd": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-8ffklppc/artifact",
            "sys_path": [
              "",
              "/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-8ffklppc/artifact",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
              "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages"
            ],
            "result": 3,
            "snapshot": [
              1,
              2
            ],
            "mutated_raw": [
              1,
              2,
              9
            ],
            "mode": "exports"
          },
          {
            "module_file": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-kocrt7ov/artifact/core.py",
            "product_file": "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages/pyalamode/__init__.py",
            "cwd": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-kocrt7ov/artifact",
            "sys_path": [
              "",
              "/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m08-unsafe-artifact-kocrt7ov/artifact",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
              "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
              "/private/tmp/pyalamode-m08-review/native-venv/lib/python3.13/site-packages"
            ],
            "result": 3,
            "snapshot": [
              1,
              2
            ],
            "mutated_raw": [
              1,
              2,
              9
            ],
            "mode": "debug"
          }
        ]
      },
      "focused": [
        {
          "script": "static_probe.py",
          "status": 0,
          "summary": {
            "cases": 532,
            "unexpected": []
          }
        },
        {
          "script": "runtime_probe.py",
          "status": 0,
          "summary": {
            "assertions": 684,
            "hook_calls": [],
            "subprocesses": 1,
            "isolated_assertions": 33
          }
        },
        {
          "script": "project_probe.py",
          "status": 0,
          "summary": {
            "assertions": 902,
            "checks": 190,
            "layouts": 42
          }
        },
        {
          "script": "cli_probe.py",
          "status": 0,
          "summary": {
            "assertions": 114,
            "recorded_rows": 58
          }
        },
        {
          "script": "freshness_probe.py",
          "status": 0,
          "summary": {
            "assertions": 50,
            "subprocesses": 14
          }
        },
        {
          "script": "m06_runtime_probe.py",
          "status": 0,
          "summary": {
            "assertions": 192,
            "hook_calls": []
          }
        },
        {
          "script": "m06_project_probe.py",
          "status": 0,
          "summary": {
            "assertions": 207,
            "layouts": 28,
            "checks": 85
          }
        },
        {
          "script": "m06_cli_probe.py",
          "status": 0,
          "summary": {
            "assertions": 76,
            "commands": 37,
            "layouts": 5
          }
        },
        {
          "script": "m06_nonexecution_probe.py",
          "status": 0,
          "summary": {
            "assertions": 78,
            "sentinels": 14,
            "layouts": 15
          }
        },
        {
          "script": "m06_freshness_probe.py",
          "status": 0,
          "summary": {
            "assertions": 42,
            "transitions": 12
          }
        },
        {
          "script": "environment_probe.py",
          "status": 0,
          "summary": {
            "assertions": 3,
            "subprocesses": 1,
            "encoding": "utf-8",
            "ascii_target_refused": false,
            "handler_hits": []
          }
        },
        {
          "script": "m08_static_probe.py",
          "status": 0,
          "summary": {
            "cases": 176,
            "assertions": 972,
            "unexpected": []
          }
        },
        {
          "script": "m08_runtime_probe.py",
          "status": 0,
          "summary": {
            "literal_rows": 57,
            "assertions": 242,
            "subprocesses": 3,
            "hooks": []
          }
        },
        {
          "script": "m08_project_probe.py",
          "status": 0,
          "summary": {
            "assertions": 42,
            "recorded_rows": 16,
            "expiry_delay_seconds": 2.431599
          }
        },
        {
          "script": "m08_cli_probe.py",
          "status": 0,
          "summary": {
            "assertions": 136,
            "recorded_rows": 77,
            "subprocesses": 77
          }
        },
        {
          "script": "m08_nonexecution_probe.py",
          "status": 0,
          "summary": {
            "assertions": 71,
            "recorded_rows": 26,
            "subprocesses": 26
          }
        },
        {
          "script": "m08_identity_probe.py",
          "status": 0,
          "summary": {
            "assertions": 153,
            "recorded_rows": 41,
            "subprocesses": 41
          }
        },
        {
          "script": "m08_version_probe.py",
          "status": 0,
          "summary": {
            "assertions": 6,
            "recorded_rows": 3,
            "subprocesses": 3,
            "scope": "actual native macOS installed CPython 3.12 only"
          }
        }
      ],
      "installed_identity_transitions": [
        {
          "label": "copied home explicit real installed approval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "copied home approved cold",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "copied home approved full warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact stale warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact stale full warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact stale no-cache",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii explicit changed-artifact reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "binascii changed-artifact reapproved cold",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed-artifact reapproved warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "binascii actual changed native artifact invocation",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "binascii explicit restored original reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "binascii restored artifact current",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact stale warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact stale full warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact stale no-cache",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 explicit changed-artifact reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "_sha2 changed-artifact reapproved cold",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed-artifact reapproved warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 actual changed native artifact invocation",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "_sha2 explicit restored original reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "_sha2 restored artifact current",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "real supported native artifact missing",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "missing artifact no-cache",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "missing artifact rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "restored missing artifact explicit current approval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "restored missing artifact accepts",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "checker.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "checker.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "model.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "model.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "project.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "project.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "integration_contracts.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "integration_contracts.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "adapter actual bytes stale approval",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "adapter stale rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "adapter explicit current reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "adapter current reapproved",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "actual UTC approval crosses before publication",
          "process_status": 0,
          "status": 1,
          "hits": null,
          "artifact_exists": false
        }
      ],
      "representative_actual_identity_digests": {
        "copied home approved cold": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "f5fe86361585dace7c142c5028f20418799bf6db30a6871b8405606cd1356c81",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "e821a95e80c81edf5836c9ec3a76d83bcc1e394b8cfa5943fc43afe62ab1de12",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "649ca3134cf94782b893c89a4533f947a00f361bacb569b28827d7589688434c",
            "admission": "denied"
          }
        ],
        "binascii changed artifact stale warm": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "4048e713162e742f059286299301210fc51bb4c61110ff1c8d58d0eb6e611c53",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "1b7b5ff13675bbb273d37fe5f34983f0530ae14bfb7d95d545d8d7a9b8383087",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "881c21c2c86863ac789693e1d1e89a5144266b057d0390cc4ea65fa9da642bcc",
            "admission": "denied"
          }
        ],
        "binascii changed-artifact reapproved cold": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "4048e713162e742f059286299301210fc51bb4c61110ff1c8d58d0eb6e611c53",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "1b7b5ff13675bbb273d37fe5f34983f0530ae14bfb7d95d545d8d7a9b8383087",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "881c21c2c86863ac789693e1d1e89a5144266b057d0390cc4ea65fa9da642bcc",
            "admission": "denied"
          }
        ],
        "_sha2 changed artifact stale warm": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "73478708935488e94e3c1eb5a6942e372cbbec7e50309371042707f301efe677",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "d13647a9feac612b45a6d4b295e8b42f83ca33c2c7ee46ef9e2ca30b59921089",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "ae1b0b14a11f54a3a02ece84815e3c8dd409f4a206f367aba8a5c9d983ec0aa7",
            "admission": "denied"
          }
        ],
        "_sha2 changed-artifact reapproved cold": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "73478708935488e94e3c1eb5a6942e372cbbec7e50309371042707f301efe677",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "d13647a9feac612b45a6d4b295e8b42f83ca33c2c7ee46ef9e2ca30b59921089",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "ae1b0b14a11f54a3a02ece84815e3c8dd409f4a206f367aba8a5c9d983ec0aa7",
            "admission": "denied"
          }
        ],
        "real supported native artifact missing": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": null,
            "admission": "unresolved"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": null,
            "admission": "unresolved"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": null,
            "admission": "unresolved"
          }
        ],
        "adapter actual bytes stale approval": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "1889ee5c020aea71b44e560d72019f196a62e4ff16bdd96d83a82b3e2c89a336",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "b525d5c59be4a8dc6a0e817b5cad75f8896b6f35b9d3985b29ffaf7cec4ba487",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "71fc66b17900a1a8863b61aeb7a42516873ab50f2d7445b9b0560c24cf7c89e0",
            "admission": "denied"
          }
        ],
        "adapter current reapproved": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "1889ee5c020aea71b44e560d72019f196a62e4ff16bdd96d83a82b3e2c89a336",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "b525d5c59be4a8dc6a0e817b5cad75f8896b6f35b9d3985b29ffaf7cec4ba487",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "71fc66b17900a1a8863b61aeb7a42516873ab50f2d7445b9b0560c24cf7c89e0",
            "admission": "denied"
          }
        ]
      }
    },
    "linux": {
      "environment": {
        "python": "3.13.1 (main, Feb  4 2025, 12:52:11) [GCC 12.2.0]",
        "executable": "/usr/local/bin/python",
        "base_prefix": "/usr/local",
        "platform": "Linux-5.15.49-linuxkit-aarch64-with-glibc2.36",
        "machine": "aarch64",
        "gil_enabled": true,
        "abiflags": "",
        "filesystem_encoding": "utf-8",
        "filesystem_errors": "surrogateescape",
        "utf8_mode": 1,
        "package_path": "/usr/local/lib/python3.13/site-packages/pyalamode/__init__.py"
      },
      "suite": {
        "status": 0,
        "methods": 320,
        "seconds": 33.891
      },
      "before_after_equal": true,
      "installed_shared_identity": {
        "distribution": "CPython-stdlib",
        "version": "3.13.1",
        "build": "3.13.1 (main, Feb  4 2025, 12:52:11) [GCC 12.2.0]",
        "cache_tag": "cpython-313",
        "platform": "linux",
        "base_prefix": "/usr/local",
        "abiflags": "",
        "extension_suffixes": [
          ".cpython-313-aarch64-linux-gnu.so",
          ".abi3.so",
          ".so"
        ],
        "native_artifacts": {
          "binascii": {
            "path": "/usr/local/lib/python3.13/lib-dynload/binascii.cpython-313-aarch64-linux-gnu.so",
            "sha256": "e86dd0645c3cec4bab67bbd9d2e0e44dc029d6501c3d71734743c4ccc5137680"
          },
          "_sha2": {
            "path": "/usr/local/lib/python3.13/lib-dynload/_sha2.cpython-313-aarch64-linux-gnu.so",
            "sha256": "8fc33c42e000fa6063b560e3d86d9889e5b48298690c80428624a44298bcfec3"
          }
        },
        "adapter_artifact": {
          "path": "/usr/local/lib/python3.13/site-packages/pyalamode/integrations.py",
          "sha256": "3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e"
        },
        "interpreter_executable": {
          "path": "/usr/local/bin/python3.13",
          "sha256": "44a9ce6ed83ab1809449925790d0583e38f17b3ccd1671d9f55e15b576cb4f20"
        },
        "interpreter_core": {
          "path": "/usr/local/lib/libpython3.13.so.1.0",
          "sha256": "654a735558be10deedd50bc06bded72d1de1f217fb25296c8ba66df7f45a918f"
        },
        "resolution": "fixed sys.base_prefix/lib/python3.13/lib-dynload and builtin _imp extension suffix; no sysconfig getters/config-data imports or environment selectors; visible filesystem shadows refused; ordinary importer/module bindings must remain unchanged at execution",
        "native_setup_trust": "platform loader/libc or libSystem and binascii linked zlib remain disclosed foundation assumptions; selected invocation does not use zlib",
        "operation": "pyalamode.integrations.base64_decode",
        "invocation_backend": "binascii",
        "native_operations": [
          "binascii.a2b_base64(data,strict_mode=True)",
          "binascii.Error exact construction",
          "binascii.b2a_base64(decoded,newline=False)"
        ]
      },
      "operation_digests": [
        {
          "identity": "pyalamode.integrations.base64_decode",
          "contract_sha256": "61f5fa1bf491475c9d242d6cd7a14f90f98aabd5ae71f17bc18fbc7d27695585",
          "dependency_sha256": "be938eb8221d5b0bde5827b4f87dcceb08088ee30be2a3554aba1dcf4ecf2cba",
          "admission": "denied"
        },
        {
          "identity": "pyalamode.integrations.base64_encode",
          "contract_sha256": "10ae6750641e50bc12334ca52eaf1c6ff9328b477e06cace8993f94ce7dc1d60",
          "dependency_sha256": "cb6f117ca3f9e1b829cbf4e9abf915afbf385f26e613f390af71675c878f50a3",
          "admission": "denied"
        },
        {
          "identity": "pyalamode.integrations.sha256_digest",
          "contract_sha256": "58b9b3376483918e16f5078332d5de4fc7fd4b6053173a0d9de960bb4548ec6c",
          "dependency_sha256": "0289cf23283f56c9ec937b3021b75b8647f9a08814e7d4567c74dc862d6d4360",
          "admission": "denied"
        }
      ],
      "isolated_copies": {
        "original_native": {
          "binascii": {
            "path": "/tmp/m08-real-runtime-copy-ohyq_udz/runtime/lib/python3.13/lib-dynload/binascii.cpython-313-aarch64-linux-gnu.so",
            "sha256": "e86dd0645c3cec4bab67bbd9d2e0e44dc029d6501c3d71734743c4ccc5137680"
          },
          "_sha2": {
            "path": "/tmp/m08-real-runtime-copy-ohyq_udz/runtime/lib/python3.13/lib-dynload/_sha2.cpython-313-aarch64-linux-gnu.so",
            "sha256": "8fc33c42e000fa6063b560e3d86d9889e5b48298690c80428624a44298bcfec3"
          }
        },
        "shared_native": {
          "binascii": {
            "path": "/usr/local/lib/python3.13/lib-dynload/binascii.cpython-313-aarch64-linux-gnu.so",
            "sha256": "e86dd0645c3cec4bab67bbd9d2e0e44dc029d6501c3d71734743c4ccc5137680"
          },
          "_sha2": {
            "path": "/usr/local/lib/python3.13/lib-dynload/_sha2.cpython-313-aarch64-linux-gnu.so",
            "sha256": "8fc33c42e000fa6063b560e3d86d9889e5b48298690c80428624a44298bcfec3"
          }
        },
        "shared_installation_unchanged": true,
        "copied_interpreter_sha256": "44a9ce6ed83ab1809449925790d0583e38f17b3ccd1671d9f55e15b576cb4f20",
        "copied_core_sha256": "654a735558be10deedd50bc06bded72d1de1f217fb25296c8ba66df7f45a918f",
        "original_interpreter_sha256": "44a9ce6ed83ab1809449925790d0583e38f17b3ccd1671d9f55e15b576cb4f20",
        "original_core_sha256": "654a735558be10deedd50bc06bded72d1de1f217fb25296c8ba66df7f45a918f"
      },
      "unsafe_artifact": {
        "assertions": 25,
        "subprocesses": 6,
        "provenance": {
          "cwd": "/review",
          "sys_path": [
            "/review/supplements",
            "/usr/local/lib/python313.zip",
            "/usr/local/lib/python3.13",
            "/usr/local/lib/python3.13/lib-dynload",
            "/usr/local/lib/python3.13/site-packages"
          ],
          "prefix": "/usr/local",
          "executable": "/usr/local/bin/python",
          "product_file": "/usr/local/lib/python3.13/site-packages/pyalamode/__init__.py",
          "console_path": "/usr/local/bin/pyalamode",
          "console_sha256": "c7d5b20b81520d481fbca54356439df8faa96d4a0579b059ff1a4883fd247725",
          "package": {
            "pyalamode/__init__.py": "c695ea8253ae3fa75e978d5b1d68e2f7a0a54ab41323849e096fffa5998a6bab",
            "pyalamode/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
            "pyalamode/boundaries.py": "cdab5e012d4c9b2d93e3ef84bbb136a51e21dc5458b18abffc632de29d4944fc",
            "pyalamode/checker.py": "65147068ec0aa7201cac7badbeb891d7ed2e7cae190914900be8f21132427cd5",
            "pyalamode/cli.py": "a72e1c2d17a68c94060bd06e3b16225894ec1a35bca8d88b89f63ff7e749f744",
            "pyalamode/collections.py": "eeff0db49d3f199e10135d61e15927027a5e52ee4d829487e794f5110ce1d783",
            "pyalamode/effects.py": "1c98e00efa431021404981d1d83bede669512bf76de1a8dcb909298509fd6a7d",
            "pyalamode/failures.py": "221e010072e3832f3750d804593c0fbed68065e5f087d1f3eeedda0204ff82be",
            "pyalamode/guardgen.py": "c9a7e8d01924c5711c9021a6523b6bb79872ef7ea836daa2bcc5d992027693a4",
            "pyalamode/integration_contracts.py": "f9f2d0d0e77f8505c8839f561212b76d9f4e757f2edde89687ded9030b614567",
            "pyalamode/integrations.py": "3a200d54ca83cf9e4ebacb0a012dbc04e86e8df9e281595844338af50462e09e",
            "pyalamode/model.py": "3c13736b6230365ac5a4ad36ab3e639ef24c1e74b65e6163cf5dcae1556b7513",
            "pyalamode/project.py": "ee8b098b29fdf0f3fc414b275a5f9b1faf4ef6d09cf07015be9eb1f1cd3a1b81",
            "pyalamode/records.py": "c607c9c057390e64e27292a495849cb7765598d3b4cbec5c60d70be0ea0da560",
            "pyalamode/standard.py": "b75e815758abc614f931fff56380f3376c6ea89db2425c9b51943dca9538eba9",
            "pyalamode/standard_contracts.py": "cb57ccaf910e52beb4c61c105e7b1031aab22c75a46ec02c9982c049c40cae3a",
            "pyalamode/variants.py": "02aeb566887188eb3c9a3b82b5cbdc07016bac53923235d4087069fc41df2c1d"
          }
        },
        "stock_results": [
          {
            "module_file": "/tmp/m08-unsafe-artifact-vn8ykahe/artifact/core.py",
            "product_file": "/usr/local/lib/python3.13/site-packages/pyalamode/__init__.py",
            "cwd": "/tmp/m08-unsafe-artifact-vn8ykahe/artifact",
            "sys_path": [
              "",
              "/tmp/m08-unsafe-artifact-vn8ykahe/artifact",
              "/usr/local/lib/python313.zip",
              "/usr/local/lib/python3.13",
              "/usr/local/lib/python3.13/lib-dynload",
              "/usr/local/lib/python3.13/site-packages"
            ],
            "result": 3,
            "snapshot": [
              1,
              2
            ],
            "mutated_raw": [
              1,
              2,
              9
            ],
            "mode": "off"
          },
          {
            "module_file": "/tmp/m08-unsafe-artifact-ur3bgken/artifact/core.py",
            "product_file": "/usr/local/lib/python3.13/site-packages/pyalamode/__init__.py",
            "cwd": "/tmp/m08-unsafe-artifact-ur3bgken/artifact",
            "sys_path": [
              "",
              "/tmp/m08-unsafe-artifact-ur3bgken/artifact",
              "/usr/local/lib/python313.zip",
              "/usr/local/lib/python3.13",
              "/usr/local/lib/python3.13/lib-dynload",
              "/usr/local/lib/python3.13/site-packages"
            ],
            "result": 3,
            "snapshot": [
              1,
              2
            ],
            "mutated_raw": [
              1,
              2,
              9
            ],
            "mode": "exports"
          },
          {
            "module_file": "/tmp/m08-unsafe-artifact-xhmp7tsh/artifact/core.py",
            "product_file": "/usr/local/lib/python3.13/site-packages/pyalamode/__init__.py",
            "cwd": "/tmp/m08-unsafe-artifact-xhmp7tsh/artifact",
            "sys_path": [
              "",
              "/tmp/m08-unsafe-artifact-xhmp7tsh/artifact",
              "/usr/local/lib/python313.zip",
              "/usr/local/lib/python3.13",
              "/usr/local/lib/python3.13/lib-dynload",
              "/usr/local/lib/python3.13/site-packages"
            ],
            "result": 3,
            "snapshot": [
              1,
              2
            ],
            "mutated_raw": [
              1,
              2,
              9
            ],
            "mode": "debug"
          }
        ]
      },
      "focused": [
        {
          "script": "static_probe.py",
          "status": 0,
          "summary": {
            "cases": 532,
            "unexpected": []
          }
        },
        {
          "script": "runtime_probe.py",
          "status": 0,
          "summary": {
            "assertions": 684,
            "hook_calls": [],
            "subprocesses": 1,
            "isolated_assertions": 33
          }
        },
        {
          "script": "project_probe.py",
          "status": 0,
          "summary": {
            "assertions": 902,
            "checks": 190,
            "layouts": 42
          }
        },
        {
          "script": "cli_probe.py",
          "status": 0,
          "summary": {
            "assertions": 114,
            "recorded_rows": 58
          }
        },
        {
          "script": "freshness_probe.py",
          "status": 0,
          "summary": {
            "assertions": 50,
            "subprocesses": 14
          }
        },
        {
          "script": "m06_runtime_probe.py",
          "status": 0,
          "summary": {
            "assertions": 192,
            "hook_calls": []
          }
        },
        {
          "script": "m06_project_probe.py",
          "status": 0,
          "summary": {
            "assertions": 207,
            "layouts": 28,
            "checks": 85
          }
        },
        {
          "script": "m06_cli_probe.py",
          "status": 0,
          "summary": {
            "assertions": 76,
            "commands": 37,
            "layouts": 5
          }
        },
        {
          "script": "m06_nonexecution_probe.py",
          "status": 0,
          "summary": {
            "assertions": 78,
            "sentinels": 14,
            "layouts": 15
          }
        },
        {
          "script": "m06_freshness_probe.py",
          "status": 0,
          "summary": {
            "assertions": 42,
            "transitions": 12
          }
        },
        {
          "script": "environment_probe.py",
          "status": 0,
          "summary": {
            "assertions": 8,
            "subprocesses": 1,
            "encoding": "ascii",
            "ascii_target_refused": true,
            "handler_hits": []
          }
        },
        {
          "script": "m08_static_probe.py",
          "status": 0,
          "summary": {
            "cases": 176,
            "assertions": 972,
            "unexpected": []
          }
        },
        {
          "script": "m08_runtime_probe.py",
          "status": 0,
          "summary": {
            "literal_rows": 57,
            "assertions": 242,
            "subprocesses": 3,
            "hooks": []
          }
        },
        {
          "script": "m08_project_probe.py",
          "status": 0,
          "summary": {
            "assertions": 42,
            "recorded_rows": 16,
            "expiry_delay_seconds": 2.467353
          }
        },
        {
          "script": "m08_cli_probe.py",
          "status": 0,
          "summary": {
            "assertions": 136,
            "recorded_rows": 77,
            "subprocesses": 77
          }
        },
        {
          "script": "m08_nonexecution_probe.py",
          "status": 0,
          "summary": {
            "assertions": 71,
            "recorded_rows": 26,
            "subprocesses": 26
          }
        },
        {
          "script": "m08_identity_probe.py",
          "status": 0,
          "summary": {
            "assertions": 153,
            "recorded_rows": 41,
            "subprocesses": 41
          }
        },
        {
          "script": "m08_version_probe.py",
          "status": 0,
          "summary": {
            "assertions": 0,
            "recorded_rows": 0,
            "subprocesses": 0,
            "scope": "alternate installed interpreter unavailable; no version-result claim"
          }
        }
      ],
      "installed_identity_transitions": [
        {
          "label": "copied home explicit real installed approval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "copied home approved cold",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "copied home approved full warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact stale warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact stale full warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact stale no-cache",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed artifact rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii explicit changed-artifact reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "binascii changed-artifact reapproved cold",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "binascii changed-artifact reapproved warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "binascii actual changed native artifact invocation",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "binascii explicit restored original reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "binascii restored artifact current",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact stale warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact stale full warm",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact stale no-cache",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed artifact rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 explicit changed-artifact reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "_sha2 changed-artifact reapproved cold",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 changed-artifact reapproved warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "_sha2 actual changed native artifact invocation",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "_sha2 explicit restored original reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "_sha2 restored artifact current",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "real supported native artifact missing",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "missing artifact no-cache",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "missing artifact rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "restored missing artifact explicit current approval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "restored missing artifact accepts",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "checker.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "checker.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "model.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "model.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "project.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "project.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "integration_contracts.py actual product byte change",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "integration_contracts.py changed product warm",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": true
          },
          "artifact_exists": false
        },
        {
          "label": "adapter actual bytes stale approval",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "adapter stale rejected build",
          "process_status": 0,
          "status": 1,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "adapter explicit current reapproval",
          "process_status": 0,
          "status": null,
          "hits": null,
          "artifact_exists": null
        },
        {
          "label": "adapter current reapproved",
          "process_status": 0,
          "status": 0,
          "hits": {
            "core.py": false
          },
          "artifact_exists": false
        },
        {
          "label": "actual UTC approval crosses before publication",
          "process_status": 0,
          "status": 1,
          "hits": null,
          "artifact_exists": false
        }
      ],
      "representative_actual_identity_digests": {
        "copied home approved cold": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "48e12264a9fc14304459ab7d950a7b8414d9a2d998db6cd4c3d6845272af6d75",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "5169c76fba420414780154317b887a3c978678d92319dc9d135b3af7baacede9",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "70b171d9b43f95f5ba7937db7097f6a2b15bd6290e13663fae299196fbb366db",
            "admission": "denied"
          }
        ],
        "binascii changed artifact stale warm": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "27e68eee05153f9d2db64629b22047d4a89af91012de0cf5dbd9884da4315efe",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "c5bc812d96c9f6e088b281a5e7a5407aacba0ba8a333441b3245d513de3461be",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "79e9bae8f5e40719fc7df2e5d852a5853bd65706960c09e055e5abca84fd4443",
            "admission": "denied"
          }
        ],
        "binascii changed-artifact reapproved cold": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "27e68eee05153f9d2db64629b22047d4a89af91012de0cf5dbd9884da4315efe",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "c5bc812d96c9f6e088b281a5e7a5407aacba0ba8a333441b3245d513de3461be",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "79e9bae8f5e40719fc7df2e5d852a5853bd65706960c09e055e5abca84fd4443",
            "admission": "denied"
          }
        ],
        "_sha2 changed artifact stale warm": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "c26950405bbe133b9778441e9e649a4a47dc30ef2694f2819a5bea338c8df36c",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "80b9ab92e6dfc450d32b08dfa2ab4698ace76c22f8899b95c5fc68556a37a6d8",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "91ab17b5562f36470ce70d244cc81aa970a6df40cf6ba234d33f6f7f8d6739ed",
            "admission": "denied"
          }
        ],
        "_sha2 changed-artifact reapproved cold": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "c26950405bbe133b9778441e9e649a4a47dc30ef2694f2819a5bea338c8df36c",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "80b9ab92e6dfc450d32b08dfa2ab4698ace76c22f8899b95c5fc68556a37a6d8",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "91ab17b5562f36470ce70d244cc81aa970a6df40cf6ba234d33f6f7f8d6739ed",
            "admission": "denied"
          }
        ],
        "real supported native artifact missing": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": null,
            "admission": "unresolved"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": null,
            "admission": "unresolved"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": null,
            "admission": "unresolved"
          }
        ],
        "adapter actual bytes stale approval": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "6c14c00c7170807616b9d951db68668c10a40ea44be15a267f9072f44319f27e",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "9e7f003ab595da057a4f9481da7210b08798efba9ecc531e9a600623118e32bf",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "7cb82c966d1f07c5d63d5d52b181e5cfd571011cce20ff720838ddbfb23b26ca",
            "admission": "denied"
          }
        ],
        "adapter current reapproved": [
          {
            "identity": "pyalamode.integrations.base64_decode",
            "dependency_sha256": "6c14c00c7170807616b9d951db68668c10a40ea44be15a267f9072f44319f27e",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.base64_encode",
            "dependency_sha256": "9e7f003ab595da057a4f9481da7210b08798efba9ecc531e9a600623118e32bf",
            "admission": "denied"
          },
          {
            "identity": "pyalamode.integrations.sha256_digest",
            "dependency_sha256": "7cb82c966d1f07c5d63d5d52b181e5cfd571011cce20ff720838ddbfb23b26ca",
            "admission": "denied"
          }
        ]
      }
    }
  }
}
```

## Independent support-cost reconciliation

The root-approved frozen harness and shared `_measure` interval were inspected in full before reconciling helper observations. The two current raw files are [macOS measurements](../evidence/m08-runtime-macos.json) (SHA-256 `c33abdcd12a9771e41410c09497e9eb58a28bb00c8d9d68352ca23bc89374ea5`) and [Linux measurements](../evidence/m08-runtime-linux.json) (SHA-256 `066587849daee869c75507fa7a9ca5755343cdda148e0ead5d1385ea8317a329`). Each has exactly 24 unique workload/mode/size rows, 72 intervals of 25 calls, 1,800 measured calls and 240 warmups. All expected output and instrumented guard conditions passed. Off has zero deep-validator calls; exports has two; debug has four for each single-operation workload and six for transport/digest, at both sizes. These are call counts for the instrumented validator, separately from assertion counters and unittest methods.

The independent reconciliation performs 842 counted checks of exact inventories, current/cross/before-after 16 product/17 package/4 owned maps, actual local native/artifact/interpreter identities, every checked artifact contract/approval/catalog digest and trust record, separate ordinary setup, unique workloads, measured counts, finite interval values and exact median calculations. Backend/core/executable byte records equal the separate fresh-installed conformance observations; the adapter paths differ between source and installed runs but their exact bytes agree. All operation assumptions remain opaque and all three actual artifacts retain unchecked surrounding initialization plus separate IO loader setup. The sole-purpose temporary fixture approvals identify their owner, rationale and provenance and confer no production approval.

The table shows medians per call in microseconds, and Python-traced peak bytes per interval, rounded to four significant figures for time. Every triple is off / exports / debug. Complete interval fields remain in the raw files.

| Workload | Payload bytes | macOS microseconds/call | macOS traced peak bytes | Linux microseconds/call | Linux traced peak bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| encode | 32 | 0.625 / 5.923 / 11.14 | 218 / 730 / 730 | 0.57 / 7.043 / 13.69 | 218 / 730 / 730 |
| encode | 4096 | 6.297 / 11.65 / 16.92 | 13788 / 13836 / 13836 | 4.093 / 10.45 / 17.11 | 13788 / 13836 / 13836 |
| decode | 32 | 1.002 / 6.405 / 11.58 | 271 / 706 / 706 | 1.172 / 7.485 / 14.27 | 271 / 706 / 706 |
| decode | 4096 | 17.74 / 22.67 / 28.02 | 16549 / 16597 / 16597 | 12.65 / 18.93 / 25.78 | 16549 / 16597 / 16597 |
| digest | 32 | 0.9517 / 6.317 / 11.59 | 242 / 706 / 706 | 1.073 / 7.435 / 14.22 | 242 / 706 / 706 |
| digest | 4096 | 13.11 / 18.5 / 23.76 | 242 / 706 / 706 | 14.23 / 20.65 / 27.39 | 242 / 706 / 706 |
| transport_digest | 32 | 2.482 / 26.43 / 54.27 | 573 / 1664 / 1702 | 2.655 / 33.18 / 69.41 | 573 / 1612 / 1650 |
| transport_digest | 4096 | 36.56 / 60.89 / 88.55 | 23591 / 23695 / 23695 | 30.44 / 61.13 / 98.66 | 23591 / 23695 / 23695 |

Setup, input generation, approvals, actual artifact build/import, guard instrumentation, warmup, result correctness checks, source hashing and JSON output occur outside intervals. Invocation, generated boundary assertions, looping, transient result disposal and tracemalloc occur inside; collection runs before each interval. Only the last result is retained. Traced memory is not RSS and may omit native HACL allocations. The process/backends are warm, OS caches and system load are uncontrolled; hardware and container resource fields are in the raw records. These limited observations support the catalog's engineering cost discussion and do not establish universal performance, application latency or human benefit. Human usefulness, authoring/review time and participant outcomes remain **UNMEASURED**.

Reconciliation output `/tmp/pyalamode-m08-review/measurement-reconciliation.json` SHA-256 `4ef466910acbea1bad7f5749b49f57502d85b490da5baa17a536d0a36c9446fc`; complete executable reconciliation harness SHA-256 `5a3af000a3ffe5973aa173c355cc1d9bf44197b015d54fd854d429c70c7f1a9d`:

```python
import hashlib,json,math,statistics,sys
from pathlib import Path
from pyalamode.integration_contracts import operation_contract
ROOT=Path(sys.argv[1]);OUT=Path(__file__).resolve().parents[1];checks=0
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def check(value,label):
 global checks
 checks+=1
 if not value:raise AssertionError(label)
records={};frozen=json.loads((OUT/'corrected-root-freeze.json').read_text())['paths']
conditions=('encode','decode','digest','transport_digest');modes=('off','exports','debug');sizes=(32,4096)
for platform in ('macos','linux'):
 path=ROOT/('Docs/evidence/m08-runtime-'+platform+'.json');raw=json.loads(path.read_text());before=raw['source_identity_before'];after=raw['source_identity_after']
 check(raw['schema']=='pyalamode-m08-measurements-v1','schema')
 check(before==after,platform+' complete before/after identity')
 check(raw['workload_sizes']==list(sizes) and raw['trials']==3 and raw['calls_per_trial']==25,platform+' exact approved bounds')
 check(len(before['product_artifacts'])==16 and len(before['full_package_sources'])==17 and len(before['owned_sources'])==4,platform+' exact source inventories')
 for name,value in before['full_package_sources'].items():check(sha(ROOT/name)==value==frozen[name],platform+' current frozen package '+name)
 for name,value in before['product_artifacts'].items():check(sha(ROOT/'pyalamode'/name)==value,platform+' current foundation '+name)
 for name,value in before['owned_sources'].items():check(sha(ROOT/name)==value==frozen[name],platform+' current owned source '+name)
 expected={(mode,condition,size) for mode in modes for condition in conditions for size in sizes}
 check({(r['mode'],r['condition'],r['size']) for r in raw['measurements']}==expected and len(raw['measurements'])==24,platform+' exact unique 24 conditions')
 check([a['mode'] for a in raw['built_artifacts']]==list(modes),platform+' actual three modes')
 dependencies=before['installed_dependencies'];check(len(dependencies)==3,platform+' exact installed operation records')
 independent=json.loads((OUT/(('native' if platform=='macos' else 'linux')+'-terminal-final.json')).read_text())['installed_snapshot_before']['catalog'][0]['installed_identity']
 for operation,record in dependencies.items():
  identity=record['identity'];check(record['dependency_sha256']==digest(identity),platform+' actual dependency digest '+operation)
  check(record['contract_sha256']==digest(operation_contract(operation)),platform+' actual candidate digest '+operation)
  check(identity['version']=='3.13.1' and identity['platform']==('darwin' if platform=='macos' else 'linux'),platform+' actual version/platform')
  for key in ('native_artifacts','interpreter_core','interpreter_executable'):check(identity[key]==independent[key],platform+' independent actual foundation '+key)
  check(identity['adapter_artifact']['sha256']==independent['adapter_artifact']['sha256']==frozen['pyalamode/integrations.py'],platform+' same actual adapter bytes')
  if platform=='macos':
   for artifact in [*identity['native_artifacts'].values(),identity['adapter_artifact'],identity['interpreter_core'],identity['interpreter_executable']]:check(sha(artifact['path'])==artifact['sha256'],'macos current installed bytes')
 for artifact in raw['built_artifacts']:
  mode=artifact['mode'];catalog={x['identity']:x for x in artifact['integration_catalog']};approvals={x['operation']:x for x in artifact['integration_approvals']}
  check(len(catalog)==len(approvals)==3,platform+' actual catalog/approval closure')
  check(len(artifact['contracts'])==4 and len(artifact['file_initialization'])==1,platform+' actual checked boundaries/setup')
  setup=artifact['file_initialization'][0];check(not setup['module_mode'] and setup['initialization_evidence']=='unchecked ordinary module initialization',platform+' ordinary setup remains unchecked')
  check(any(x['identity']=='pyalamode.integrations import' and x['effects']==['IO'] and x['failures']==['ImportError','OSError'] for x in setup['setup_observations']),platform+' separate native setup effects/failures')
  if mode!='debug':check(artifact['actual_off_or_exports_original_source_unchanged'] and artifact['artifact_files_sha256'][artifact['module']+'.py']==artifact['fixture_sha256'],platform+' actual copied source identity')
  check(len(artifact['guarded_exports'])==(0 if mode=='off' else 4),platform+' selected export coverage')
  for contract in artifact['contracts']:
   expected_operations={'pyalamode.integrations.base64_encode'} if contract['name']=='encode_payload' else {'pyalamode.integrations.base64_decode'} if contract['name']=='decode_payload' else {'pyalamode.integrations.sha256_digest'} if contract['name']=='content_digest' else set(dependencies)
   check({x['identity'] for x in contract['external_assumptions']}==expected_operations,platform+' transitive benchmark trust '+contract['name'])
   check(contract['required_effects']==[] and contract['failures']==['ValueError'],platform+' separate invocation effect/failure')
   for assumption in contract['external_assumptions']:
    op=assumption['identity'];record=dependencies[op];approval=approvals[op]
    check(assumption['installed_identity']==record['identity']==catalog[op]['installed_identity'],platform+' actual contract/catalog/dependency identity')
    check(assumption['dependency_sha256']==record['dependency_sha256']==approval['dependency_sha256'] and assumption['contract_sha256']==record['contract_sha256']==approval['contract_sha256'],platform+' exact reviewed digest closure')
    check(assumption['admission']==catalog[op]['admission']==approval['status']=='approved',platform+' current benchmark approval')
    check(assumption['approval']['owner']=='root-authorized M8 benchmark fixture' and 'not a production approval' in assumption['approval']['rationale'] and assumption['approval']['provenance']=='Docs/evidence/m08-runtime-contract.md approved protocol',platform+' visible finite fixture approval')
    check(assumption['initialization']['effects']==['IO'] and 'opaque' in assumption['source_evidence'],platform+' opaque native trust/setup preserved')
 rows=[]
 for row in raw['measurements']:
  mode,condition,size=row['mode'],row['condition'],row['size'];expected_count=0 if mode=='off' else 2 if mode=='exports' else 6 if condition=='transport_digest' else 4
  guard=row['actual_guard_calls_per_invocation'];artifact=next(a for a in raw['built_artifacts'] if a['mode']==mode)
  check(guard==artifact['instrumented_guard_calls'][condition][str(size)],platform+' actual measured guard condition')
  check(guard['deep_assertion_calls_per_invocation']==len(guard['paths'])==expected_count,platform+' exact guard count')
  check(row['warmup_calls']==10 and row['correctness_passed'] and len(row['observations'])==3,platform+' exact calls/correctness/trials')
  check(row['workload']['payload_bytes']==size and row['workload']['encoded_bytes']==4*((size+2)//3),platform+' actual payload/encoded work')
  for observation in row['observations']:check(math.isfinite(observation['elapsed_seconds']) and observation['elapsed_seconds']>0 and 0<=observation['traced_current_bytes']<=observation['traced_peak_bytes'],platform+' finite measured time/traced allocations')
  check(row['median_seconds_per_call']==statistics.median(o['elapsed_seconds'] for o in row['observations'])/25,platform+' independent exact time median')
  check(row['median_traced_peak_bytes']==statistics.median(o['traced_peak_bytes'] for o in row['observations']),platform+' independent exact allocation median')
  rows.append({'mode':mode,'condition':condition,'size':size,'guard_calls':expected_count,'median_microseconds_per_call':row['median_seconds_per_call']*1e6,'median_traced_peak_bytes':row['median_traced_peak_bytes']})
 records[platform]={'raw_sha256':sha(path),'environment':raw['environment'],'rows':rows,'source_identity_before':before,'source_identity_after':after,'intervals':sum(len(r['observations']) for r in raw['measurements']),'measured_calls':sum(len(r['observations'])*25 for r in raw['measurements']),'warmups':sum(r['warmup_calls'] for r in raw['measurements']),'scope':raw['measurement_scope']}
for key in ('product_artifacts','full_package_sources','owned_sources'):check(records['macos']['source_identity_before'][key]==records['linux']['source_identity_before'][key],'cross-platform current '+key)
report={'assertions':checks,'harness_sha256':sha(__file__),'records':records,'unexpected':[]}
(OUT/'measurement-reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assertions':checks,'per_platform_rows':24,'per_platform_intervals':72,'per_platform_calls':1800,'per_platform_warmups':240,'unexpected':[]}))
```
