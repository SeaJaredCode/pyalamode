# Pyalamode

Pyalamode checks a functional core in ordinary Python. The current M11 increment supports scalar functions, functional modules, recursive tuples, eager persistent collections, fixed typed records, persistent replacements, explicit shell snapshots and fresh exports, finite dataclass/namedtuple adapters, optional generated data guards, finite checked effectful shells with opaque capabilities, closed `@oneof` sums and closed unions, Option/Result values, ordered validation accumulation, exhaustive finite patterns, characterized failure handlers, and a bounded standard toolkit for text, integers, UTF-8/hex, eager scan/grouping, composition, partial application and Result traversal, reviewed exact installed external operations, local editor diagnostics and repair previews, adoption queues, reviewed audit baselines and independent team policy gates, checked source-wheel distribution with fresh consumer verification, and stable exact value encoding. Checked callbacks, stable constants, recursion, captures, and defaults retain their existing contracts. Accepted code runs through normal Python imports and commands. Checking parses application source without importing it or evaluating its hooks.

The supported check/build target is **CPython 3.13.1, standard GIL build, on macOS arm64 or Linux aarch64**, with native filesystem encoding `utf-8` and errors `surrogateescape` (`cpython-3.13.1`). Reports/cache inputs record the observed encoding, error mode and UTF-8 mode. Other native filesystem configurations, patches/minors, free-threaded builds, interpreters, and platforms fail the target gate. Ordinary live IO/environment setup checks the same filesystem condition. Installation under another Python 3.13 patch does not establish compatibility.

## Install and run

```sh
python3.13 --version
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
pyalamode check examples/scalar.py
python examples/scalar.py
pyalamode check examples/modules --no-cache
python -m examples.modules.demo
pyalamode check examples/collections --no-cache
python -m examples.collections.demo
pyalamode check examples/records --no-cache
python -m examples.records.demo
pyalamode check examples/effects --no-cache
python -m examples.effects.demo
pyalamode check examples/domains --no-cache
python -m examples.domains.demo
pyalamode check examples/standard --no-cache
python -m examples.standard.demo
pyalamode check examples/editor --no-cache
python -m examples.editor.demo
```

The scalar example prints `1300` and `0`. The module example prints `1500`, `6`, `6`, and `2`. Its checked core uses stable imports, defaults, a closure, a recursive calculation, and tuple inputs; its ordinary demo prints those results without receiving a purity claim.

One function can opt in with the runtime identity marker:

```python
from pyalamode import fun

@fun
def discounted_total(cents: int, discount_cents: int) -> int:
    remainder = cents - discount_cents
    if remainder < 0:
        result = 0
    else:
        result = remainder
    return result
```

A module can opt in without importing that marker:

```python
"""Calculation core."""
# mode: fun

SERVICE_FEE = 200

def quote(cents: int, discount_cents: int = 0) -> int:
    return cents - discount_cents + SERVICE_FEE
```

The directive occurs once after any shebang, encoding declaration, and module docstring, before executable statements. A misplaced directive or region toggle fails. Module mode selects functions, nested definitions, and initialization. In an ordinary module, `@fun` selects that function and its nested definitions, defaults, annotations, captures, and dependencies; unrelated initialization stays unchecked.

Projects can require module mode without source markers:

```toml
[tool.pyalamode]
schema = 1
require_modules = ["core/**/*.py"]
```

Patterns are project-relative, case-sensitive glob patterns; `**/` may match zero directories. Absolute paths, parent traversal, and non-string patterns fail policy validation. Required mode also applies to discovered local dependencies matching the policy. Guard policy is described below; other accepted fields retain their closed defaults.

## Exact contracts

Every parameter and result has an explicit supported annotation. Analyzed calls establish the actual value and callable contracts; ordinary annotations alone cannot establish exact runtime inputs.

| Contract | Admitted syntax and meaning |
| --- | --- |
| Scalars | Exact `int`, `bool`, `str`, `bytes`, `None`; stable `types.NoneType` imports; supported quoted annotations |
| Tuples | Fixed `tuple[int, str]`, homogeneous `tuple[int, ...]`, empty `tuple[()]`; recursive exact immutable data, excluding subclasses and callable payloads |
| Callables | Stable `typing` or `collections.abc` `Callable[[int, str], int]`; fixed positional pure invocation. Product `Effectful[[ClockCapability], int, Clock]` adds a finite effect upper bound and exact capability slots. Actual target/capture evidence is required. |
| Capabilities | Exact `IOCapability`, `StateCapability`, `ClockCapability`, `RandomCapability`, `EnvironmentCapability`; borrowed invocation inputs in matching effectful functions, excluded from stable data/returns/defaults/captures/aliases |
| Collections | Stable `pyalamode` imports of `Vector[T]`, `OrderedMap[K, V]`, `Map[K, V]`, and `Set[T]`; recursively admitted data; map keys and Set elements use one exact scalar domain |
| Sum types | Closed tagged `@oneof` domains with nested `@case` payloads (`@variant` is a deprecated alias); closed unions `A \| B` of `None`, `bool`, `int`, `str`, `bytes`, records, domains and cases, discriminated by exact class (`case int(n):`); `Option[T]` (`Some`, `Nothing`) and `Result[T,E]` (`Ok`, `Err`); finite exhaustive exact class patterns. See [the sum-types design](Docs/design/sum-types.md). |
| Failure data | Exact immutable `Failure(category: str, message: str)`; `failure_value` converts a supported opaque actual handler exception token to fixed immutable data |
| Records | Exact `@record` declarations with fixed public typed fields and stable defaults; recursive admitted data, pure slot reads, exact type-sensitive equality and `replace` |

Callable parameters express a required input contract. They do not turn an unknown function, lambda, protocol, or ordinary annotated parameter into checked pure evidence. Checked callers supply resolved checked functions or pass a callable already established by their own input contract. Callable annotations allow nested callable inputs/results, but exclude `Any`, ellipsis signatures, variadics, and keyword-only callback shapes. Optional positional defaults and positional-only parameters are compatible when the complete fixed positional call fits. Direct checked calls also support normal positional-only, positional-or-keyword, keyword-only, and default arguments.

A generic pure admitted callable has the finite invocation failure upper bound **`IndexError`, `KeyError`, `ValueError`, `ZeroDivisionError`, and `RecursionError`**, the current closed operation universe. Conditional pure callback invocation propagates that bound. Effectful conditional callbacks add the finite operation failure categories of their declared families, including `RuntimeError`, `OSError` and `UnicodeError` where relevant. Concrete direct targets retain their characterized transitive failures. Reports disclose concrete callback defaults, captures, returned targets, and collection operation identities when established. Recursively nested library validation and equality have a separate conservative `RecursionError` bound.

Stable constants require a single characterized source initialization and no analyzed replacement. Upper-case spelling, `Final`, hashability, a current integer object, and an annotation do not establish stability. A nested function can capture admitted immutable values and checked callables. Changing cells fail, and every required cell must be initialized before a closure is invoked or escapes. Recursion is admitted without a termination claim.

## Supported source

The scalar operations remain integer unary `+`/`-`, integer `+`/`-`/`*`/`//`/`%`, same-type integer/string/bytes comparisons, string/bytes concatenation, boolean `not`/`and`/`or`/equality, right-hand literal `is None`/`is not None`, and conditional expressions. Approved builtin signatures are `abs(int)`, `len(str|bytes|admitted_tuple|product_collection)`, and two-or-more homogeneous positional `min`/`max` over exact `int`, `str`, or `bytes`. Division and remainder disclose `ZeroDivisionError`.

Statements include one-name initialization, annotated initialization, `if`/`elif`/`else`, `return`, `pass`, docstrings, checked nested function definitions, exhaustive finite `match`, and characterized `try`/`except` handlers. Each reachable binding initializes once. Exclusive branches may initialize the same name; missing initialization and reachable reinitialization fail. Imports are module-level dependencies.

Module initializers and defaults use closed stable data expressions, earlier stable bindings, approved builtin calls, and checked callable references. **Calling application functions in initialization/default expressions is excluded**, even if their invocation contract is checked. Annotation expressions are parsed from the finite whitelist. Functions admit the resolved identity `fun` and finite identity `effects` declarations; fixed record classes admit the library declaration `record`. Imports, decorators, annotations and defaults must be available when Python evaluates them. Initialization and definition-time default failures are reported separately from invocation failures.

Local imports resolve from the project root with package-before-module precedence and required package initializers. A strict module imports only characterized foundations or functional local modules. Cyclic direct from-imports and eager cyclic namespace reads in initialization/defaults/non-postponed annotations fail `PAL241`; module imports with deferred function references remain supported. This is a finite conservative availability gate. An ordinary module may perform unchecked initialization before using checked exports. Unresolved external APIs receive no trusted admission. A local file named `pyalamode`, `typing`, `types`, or `collections` cannot acquire foundation behavior through its spelling.

Fixed tuples support in-range literal integer indexing and literal slicing; homogeneous tuples support exact integer indexes and slices. Tuple/collection/record equality requires matching recursive exact data schemas. Map/Set membership uses characterized scalar lookup. Loops, comprehensions, destructuring, arbitrary classes/methods, general patterns, mutable strict data, reflection, generators, async, arbitrary exception construction/raise/handlers, external trust approvals, arbitrary effectful operations and Task remain excluded. Dynamic ordinary dispatch stays the ordinary caller's responsibility. The checker is conservative about unknown aliases, ordinary control flow, and cells outside a checked enclosing scope.

## Closed alternatives and failure values

```python
from pyalamode import oneof, case, fun, Result, Ok, Err, Failure, failure_value

@oneof
class Lookup:
    @case
    class Found:
        value: int
    @case
    class Missing:
        pass

@fun
def read(value: Lookup) -> int:
    match value:
        case Lookup.Found(value=number):
            return number
        case Lookup.Missing():
            return 0

@fun
def quotient(number: int, divisor: int) -> Result[int, Failure]:
    try:
        return Ok(number // divisor)
    except ZeroDivisionError as caught:
        return Err(failure_value(caught))
```

A domain has one or more public nested `@case` declarations with fixed immutable data fields and stable trailing defaults. Construct `Lookup.Found(3)` or `Lookup.Missing()`; the domain is a closed namespace. Cases have no methods, bases, custom constructors, descriptors, or arbitrary match hooks. Field schemas refer to already available data declarations; outer/self/sibling/forward case references are refused. Unchecked changes to case behavior still violate dependency assumptions.

`Option[int]` contains `Some(value)` or `Nothing()`. `Result[int,str]` contains `Ok(value)` or `Err(error)`. Inspect them with `case Some(value=n)`, `case Nothing()`, `case Ok(value=n)`, or `case Err(error=e)`. `accumulate(left,right)` accepts exactly two positional established `Result[T,E]` and `Result[U,E]` schemas and returns `Result[tuple[T,U],Vector[E]]`: successes produce a pair; independent errors appear in left-to-right argument order. Explicit Result parameter/binding annotations supply missing success/error schemas; two sparse `Ok` constructors alone do not establish the full accumulation contract.

An unguarded full case pattern covers its whole tag only when its payload patterns are irrefutable. A nested single case of a multi-case payload domain constrains that outer case. Constrained patterns and guarded patterns cannot bind named captures, because failed attempts may leave partial bindings. Capture-free exact bool guards supply coverage only when statically literal `True`. All declared cases need full coverage, or an explicit final `_` can deliberately cover present and future cases. Adding a case rejects incomplete explicit consumers and keeps a deliberate wildcard valid. Projects can require explicit cases with `explicit_cases = ["core:Lookup"]` under `[tool.pyalamode]`.

Handlers admit unchanged builtin `ZeroDivisionError`, `IndexError`, `KeyError`, `ValueError`, `RecursionError`, `RuntimeError`, `OSError`, and `UnicodeError` categories, including direct tuple selection. `RuntimeError` covers `RecursionError`; `ValueError` covers `UnicodeError`; overlapping handlers are refused. Broad/bare/user handlers, `else`/`finally`, exception construction, and `raise` stay outside the catalog. An `as` target remains an actual mutable Python exception, opaque in checked code and deleted after the handler. Only direct `failure_value(caught)` converts it to immutable category/message data, using exact supported builtin identities and fixed messages without reading payloads, dictionary, traceback, frames, or formatters. Targets cannot alias/capture/escape, overwrite a potentially initialized try binding, or be reused after cleanup.

Catching a characterized failure reduces the failure contract at that operation/call site. It retains every performed effect, operation and dependency assumption. Handler-body failures remain visible outside that handler's mask; warm cache evidence preserves masks per call occurrence. Snapshot validation and optional guards support nested variants; `thaw` emits fresh `{"variant": "module:Domain", "case": "CaseName", "fields": {...}}` envelopes, with fixed `pyalamode:Option`/`pyalamode:Result` identities. See [the M6 contract](Docs/milestones/06-domains.md) and [the domain example](examples/domains/domain.py).

## Checked effectful shells

A declaration names a finite upper bound. Every admitted operation remains characterized, including callback invocation. Unknown calls and implicit dispatch fail even when all five effects are declared.

```python
from pyalamode import effects, Effectful, Clock, ClockCapability, borrow

@effects(Clock)
def read_clock(clock: ClockCapability) -> int:
    return clock.now_ns()

@effects(Clock)
def invoke(reader: Effectful[[ClockCapability], int, Clock], clock: ClockCapability) -> int:
    with borrow(clock) as scoped:
        return reader(scoped)
```

`@effects` selects the function, alone or alongside one `@fun`; both declarations preserve the identical function without registration, wrappers or metadata mutation. Pure callers cannot invoke a declared effectful function. `Callable` has an empty effect bound; `Effectful` permits a concrete target with a smaller bound and unions every conditional alternative. Capability callback arguments are explicit borrowed slots; a callback cannot capture a live capability. Vector map/filter/fold preserve ordered execution and union callback bounds; their capture restriction remains the same.

The exact interfaces are `IOCapability.read_text(path)`/`write_text(path,text)`, `StateCapability.get()`/`set(int)`, `ClockCapability.now_ns()`, `RandomCapability.below(int)` and `EnvironmentCapability.get(name,default)`. IO reads/writes whole UTF-8 files, closes internally on completion/failure, and uses explicit rooted relative paths. `borrow` is a logical lease whose view expires on every exit, including return or body failure. Persistent readers, sessions, arbitrary context managers and resource transfer remain unsupported.

Provider setup is ordinary Python: `recorded_clock((123,))`, `state(0)`, `recorded_random((3,))`, `recorded_environment((("NAME","demo"),))`, and `recorded_io((), allowed_ops=("read_text","write_text"))` provide controlled inputs. `live_clock()`, `live_random()`, `live_environment()` and `live_io(root, allowed_ops=("read_text","write_text"))` access their live interfaces. Controlled providers retain their effects. Provider constructors are refused inside checked functions, defaults and functional module initializers. Recorded exhaustion raises `IndexError`; recorded IO missing reads raise `KeyError`; invalid bounds/path/name raise `ValueError`. Failures remain separate from effects.

A capability slot conservatively requires the **full interface operation set** and a live invocation lifetime. The checker does not infer minimal callee permissions: a known read-only IO provider cannot satisfy any checked IOCapability slot, including a reader. Ordinary narrower providers remain usable under their runtime permission checks. Known closed/unknown shell capability operations invalidate analyzed lending evidence; ordinary annotations establish no actual provider type. Capabilities cannot be stored in tuples/collections/records, defaults, global constants, alias bindings, captured cells or returned stable values. Ordinary callers still owe exact interfaces, permissions, lifetime, dependency integrity and IO path consistency. The rooted IO contract is not a security sandbox.

Entry policy can restrict exact selected functions:

```toml
[tool.pyalamode.effect_bounds]
"core:invoke" = ["Clock"]
"core:pure_total" = []
```

The declared bound cannot exceed policy; required effects must fit the declaration. Reports retain declared/required effects, origin paths, separate invocation and definition failures, concrete callable argument/reference dependencies, and exact returned/captured callback evidence across warm checks. An uninvoked effectful callable value retains its assumptions without adding invocation effects. Guards validate supported data only and refuse callback/capability exports; debug can assert data alongside unguarded capability inputs.

Use public names through `from pyalamode import ...` or `from pyalamode.effects import ...`. The exported `effects` function shares its helper submodule name: ordinary `import pyalamode.effects as e` binds that function, so `@e(Clock)` works, while `e.effects`/`e.ClockCapability` namespace syntax is refused. See the [M5 handoff](Docs/milestones/05-effects.md) and [runtime contract](Docs/evidence/m05-runtime-contract.md) for the finite catalog, failures, dependency/cleanup assumptions and costs.

## Eager persistent collections

```python
from pyalamode import Vector, fun

@fun
def total(values: Vector[int], adjustment: int) -> int:
    def adjusted(value: int) -> int:
        return value + adjustment
    def add(accumulator: int, value: int) -> int:
        return accumulator + value
    return values.map(adjusted).fold(add, 0)

original = Vector.of(10, 20)
revised = original.appended(30)
print(original)               # Vector.of(10, 20)
print(total(revised, 5))       # 75
```

Construction uses explicit positional items: `Vector.of(1, 2)`, `OrderedMap.of(("a", 1))`, `Map.of(("a", 1))`, and `Set.of("a", "b")`. Typed empty values use `Vector[int].of()` or `Map[str, int].of()`. Constructors and updates validate deep immutable-data invariants; ordinary runtime generic arguments are erased, so complete parameterized schemas remain static and ordinary-caller obligations. `Vector[int].of(True)` is refused by the checker even though its ordinary runtime value contains stable data. Builtin mutable containers, arbitrary iterators, and callable data members are excluded from strict values; explicit shell snapshots can produce admitted data.

Vectors provide index/slice, `appended`, `updated_at`, `concat`, and eager `map`, `filter`, and `fold(callback, initial)`. Maps provide lookup, `get(key, default)`, `contains`, `updated`, `without`, and right-wins `merge`. OrderedMap provides `entries()`, `keys()`, and `values()` in insertion order. Map provides `ordered_entries()`, `ordered_keys()`, and `ordered_values()` in canonical scalar-key order. Sets provide `contains`, `added`, `without`, `union`, `intersection`, `difference`, and canonical `ordered_values()`. Ignoring a known persistent update fails `PAL250`; bind or return its new value.

Map/Set key domains are exact `None`, `bool`, `int`, `str`, or `bytes`, with one domain per static schema. Their canonical order is singleton None, False before True, ascending integers, and lexicographic strings/bytes. Equivalent unordered values have the same ordered traversal and runtime representation across construction histories and hash seeds. Arbitrary unordered iteration or callbacks are refused; select a canonical Vector before a transform or fold. Vector/OrderedMap order is part of equivalence. Product equality compares exact types recursively, including distinct bool/int payloads. Strict formatting, hashing, and general iteration remain excluded.

The backend reuses stock CPython tuple storage with no added package dependency or vendored backend code. Updates copy O(n) references, and keeping k similarly sized versions can retain O(kn) references; nested value validation adds traversal work. Construction and map merge sort scalar keys, with an O(n log n) comparison bound. This is an eager, useful copying implementation; it does not promise structural-sharing update costs. The [M3 report](Docs/milestones/03-collections.md) publishes every admitted signature, failure/equivalence/order contract, licensing/trust boundary, and measured workload costs.

## Records and explicit boundaries

```python
from pyalamode import Vector, fun, record, replace

@record
class Customer:
    name: str
    tags: Vector[str]

@fun
def tag_customer(customer: Customer, tag: str) -> Customer:
    tags = customer.tags.appended(tag)
    return replace(customer, tags=tags)
```

Records validate complete recursive field schemas, accept positional/keyword fields and stable trailing defaults, preserve earlier values through replacement, and reject ordinary field mutation, reinitialization and subclassing. Public fields named `self` or `value` are supported; constructor/replacement receivers are positional-only. Methods, custom constructors/validators, descriptors, callable fields, bases/metaclasses, private fields, and forward/recursive record declarations have no M4 contract. Finite exact record patterns support fresh irrefutable captures; guarded or potentially failed partial capture patterns are refused. Records are unhashable. Record-only checked builds are supported, and evidence separates the checked declaration from the trusted product implementation.

In an ordinary shell, `freeze(raw, exclusive=True, schema=Vector[int])` recursively converts exact list/tuple/dict/set/frozenset input to Vector/tuple/OrderedMap/Set and validates the selected result schema. An explicit schema on a simple stable ordinary assignment establishes data for a subsequent analyzed checked call. `exclusive=True` asserts caller-held exclusive access during snapshotting; it does not detect ownership or acquire a lock. Missing mutable-source preconditions, cycles, subclasses, foreign hooks, and live views fail. Repeated acyclic references are copied by value. `thaw(snapshot)` creates independent fresh nested lists/dictionaries/sets; record exports are field dictionaries. Neither operation is admitted inside pure checked functions, defaults or functional initialization.

`dataclass_adapter(Source, Customer)` or `namedtuple_adapter(Source, Customer)` can qualify a finite exact generated source class for `freeze(source, exclusive=True, adapter=adapter, schema=Customer)`. Source field order/storage/generated behavior and stable defaults must qualify; custom getters/constructors/methods, factories and subclasses fail. The target is a concrete product record with exact nested schema validation. `frozen=True` alone certifies neither behavior nor nested data. The [record demo](examples/records/demo.py) shows source mutation after snapshotting and export mutation without changing retained records.

## Bounded standard operations

```python
from pyalamode import Vector, fun, text_split, integer_parse_decimal, vector_scan

@fun
def parse_item(text: str) -> int:
    return integer_parse_decimal(text)

@fun
def add(total: int, value: int) -> int:
    return total + value

@fun
def running_prices(text: str) -> Vector[int]:
    values = text_split(text, ",").map(parse_item)
    return vector_scan(values, add, 0)
```

`pyalamode.standard-v1` publishes exact positional-only contracts for twelve text/integer/encoding operations and five eager helpers. Decimal conversion admits `[+-]?[0-9]{1,4096}` and canonical output, using manual arithmetic independent of CPython's ambient decimal formatting limit. UTF-8 uses manual exact conversion and builtin Unicode failures; registered codecs/error handlers cannot run. Hex decoding accepts even ASCII pairs without whitespace. No float/context, general formatter, dynamic codec, JSON, pickle or foreign restoration is admitted.

Scans include the initial accumulator; grouping preserves first-key and within-group input order; Result traversal stops at the first Err. `compose(outer, inner)` supports fixed unary callbacks; `partial_first(binary_callback, stable_first_argument)` returns a fixed unary callback. Construction invokes neither callback, while later invocation preserves actual targets, captures, effects, failures and trust. Bound arguments must be stable data; an unbound wrapper input can be data or an exact capability slot. Callable values remain outside data containers and selected data guards.

Existing rooted whole-file IO, Clock and Environment interfaces have versioned entries in the same report catalog. Live IO uses binary read/write plus manual UTF-8, closes on failure, and preserves newlines. A write opens/truncates before encoding, so encoding/OS failure can leave truncated or partial output. Roots, relative paths and environment names reject surrogate code points before native conversion. Filesystem stability/permission and lifetime preconditions remain explicit. Controlled providers retain effects. Recognized ordinary provider setup has separate per-file observations; a pure export does not certify surrounding import initialization, and strict modules refuse imports with ordinary setup.

The [standard workflow](examples/standard/core.py) and [ordinary demo](examples/standard/demo.py) cover parsing to Result/Failure, running totals, grouping, adjusted values, UTF-8/hex and separately effectful providers. `pyalamode explain compose`, `integer_parse_decimal`, `utf8_decode` and `IOCapability.read_text` describe their contracts. Structured check/build reports include `standard_catalog`, used `operation_contracts`, recursive callable evidence and `setup_observations`. [The M7 contract](Docs/milestones/07-standard.md) and [runtime inventory](Docs/evidence/m07-runtime-contract.md) publish signatures, ordering, failures, aliases, initialization and costs. Target-user usefulness remains **UNMEASURED**; the representative tasks and measurement protocol do not imply completed user validation.

## Reviewed external operations

```python
from pyalamode import fun
from pyalamode.integrations import base64_encode, base64_decode, sha256_digest

@fun
def attachment(data: bytes) -> tuple[bytes, bytes]:
    encoded = base64_encode(data)
    restored = base64_decode(encoded)
    return encoded, sha256_digest(restored)
```

`pyalamode.integrations-v1` has three bounded exact-bytes operations backed by the actual installed CPython 3.13.1 native `binascii` and `_sha2` artifacts. Encode and hash accept at most 1MiB. Decode accepts at most 1,398,104 encoded bytes and requires canonical padded Base64, including zero unused pad bits; malformed/noncanonical/oversized data raises `ValueError`. SHA-256 returns 32 raw bytes through private HACL state. Native backend behavior remains an explicit external assumption. Ordinary adapter import has separately reported IO/loader setup; a checked pure export does not certify that setup.

External operations are denied by default. `pyalamode explain integrations --json` shows detached candidate contracts and actual path/version/byte identities without importing the adapters or backends. `python -m examples.integrations.review_policy` prints a denied local review proposal. After reviewing those identities, each explicit `[[tool.pyalamode.integration_approvals]]` table supplies `operation`, `contract_sha256`, `dependency_sha256`, nonempty `owner`, `rationale`, `provenance` and optional UTC `expires_at`; `external_trust = "approved"` selects current reviewed approvals. No command writes or silently approves policy. The [M8 contract](Docs/milestones/08-integrations.md) describes the complete closed schema and optional conservative JSON overrides. Drafts, stale identities and expired approvals cannot satisfy strict admission.

Checked wrappers retain complete operation/approval identities through callers, returned/composed/captured callbacks, eager collection helpers and failure handlers. Check and build rediscover actual dependency bytes and expiry on warm runs and before artifact publication. The supported discovery layout is `sys.base_prefix/lib/python3.13/lib-dynload`, with the built-in `_imp` ABI suffix, a macOS framework `Python` core or Linux `lib/libpython3.13.so.1.0` core. Missing/custom layouts refuse. Discovery executes no sysconfig imports/getters, selected config-data source, annotations, defaults or dependency import hooks. The disk snapshot assumes ordinary unchanged importers and loaded/backend bindings at execution; analyzed native/private/global/importer writers fail closed.

An ordinary `@unsafe(scope="...", rationale="...")` adapter carries visible unchecked scope/rationale and remains outside checked calls even when all effects are declared. Its isolated output may start a new checked computation after explicit `freeze(raw, exclusive=True, schema=Vector[int])`; that snapshot establishes data evidence under the exclusive-access precondition. Copying does not certify the earlier adapter behavior. The [attachment workflow](examples/integrations/core.py) and [ordinary unsafe-output demo](examples/integrations/demo.py) show both boundaries. Target-user usefulness remains **UNMEASURED**.

## Optional guards

```toml
[tool.pyalamode]
boundary_guards = "exports"
guarded_exports = ["examples.records.core:tag_customer"]
```

Build then provides the guarded public alias `pyalamode_exports.examples.records.core:tag_customer`, imported normally with `from pyalamode_exports.examples.records.core import tag_customer`. It validates exact supported arguments before the original body and returned data afterward. Original-module functions remain unwrapped and unguarded in exports mode; checked internal calls use those originals. Guards are off by default and do not freeze inputs, prove effects/ownership/callback purity, or monitor dependency tampering. Selected Callable, Effectful and live capability boundaries are refused. Unknown, ambiguous, duplicate and conflicting selections fail.

`boundary_guards = "debug"` additionally inserts supported exact data assertions at selected function parameters, local bindings and returns in copied source. Reports list coverage; callable evidence obligations remain. Debug assertions add repeated traversal and ordinary import/allocation overhead. The [M4 handoff](Docs/milestones/04-records.md) and [runtime contract](Docs/evidence/m04-runtime-contract.md) publish guard behavior, costs, snapshot preconditions, adapter limits and evidence.

## Local editor

The [local VS Code client](editors/vscode/README.md) uses the same full-project engine as check/build. Install Pyalamode into the supported interpreter's environment, then set `pyalamode.pythonPath` in User settings to its absolute path, such as `/Volumes/Projects/pyalamode/.venv/bin/python`, and open one trusted local workspace. The client preserves that virtual environment path and launches with Python isolation (`-I`) without a shell, so workspace packages and `PYTHONPATH` cannot replace the server at interpreter startup. Install the finite local VSIX using the client guide, or use its extension development command; no Marketplace service is needed.

Problems display shared rule IDs, authored ranges and first bindings. Hover and **Pyalamode: Inspect Project Contracts** show participating boundaries, exact/inferred data and callable contracts, declared/required effects and origins, transitive trust, separate failures/initialization and guard coverage. Definitions/references cover participating declarations and actual checked-call edges; unsupported targets have no guessed destination. **Explain Rule or Operation** accepts rule/catalog names or an exact `module:qualified.function` authored selector. The same selector works with `pyalamode explain core:quote --root /path/to/project`.

Open files supply full-text versioned overlays, including dependency buffers. The server refreshes policy, source/import resolution, analyzed writers and current external identities/expiry at each observation. Reports distinguish unsaved overlay evidence from disk evidence; closing restores disk analysis. This server performs fresh body analysis and makes no incremental-body-reuse claim. Changed product bytes require restarting the loaded server. Tooling/stale failures keep both project and file-level claims unverified.

An eligible code action opens a read-only before/after diff with its source version, full input snapshot, checked candidate and limits. A finite straight-line reassignment preview keeps the second assignment's old-value RHS and renames subsequent reads. A discarded persistent-update preview binds the new value while retaining the original return; choose intentionally how the calculation should use it. Source and policy bytes stay unchanged until you make an edit. No preview adds effects, approvals, ignored errors, conversions or handlers. Closures, branches, aliases, callbacks, capabilities and other unsupported changes receive explanations without a fabricated safe rewrite.

**Open Authored Guard Boundary** validates a local built artifact's actual selected source/facade hashes, coverage and current source/policy/dependency fingerprint, then opens the original compatible declaration or supported debug assertion. It neither runs the artifact nor treats an arbitrary exception string as evidence. The stdio server is also available directly:

```sh
/absolute/environment/bin/python -I -m pyalamode.editor --stdio --root /absolute/project
```

This command requires Pyalamode installed in that environment and speaks bounded LSP-style JSON-RPC frames on stdin/stdout. The installed console command `pyalamode editor --stdio --root /absolute/project` is also available under ordinary Python startup assumptions; it does not add interpreter isolation. The [M9 handoff](Docs/milestones/09-editor.md) specifies supported methods, UTF-16 ranges, producer coordinate metadata, provenance, freshness and preview limits. Copy [the editor core](examples/editor/core.py) into an isolated project and use [the repair cases](examples/editor/repair-cases.txt) for a feedback walkthrough. The ordinary demo prints `1300`, `Vector.of(1, 2)` and `Vector.of(1, 2, 3)`. Target-user editor repair usefulness and authoring time remain **UNMEASURED**, with zero participants/attempts; translated-source navigation remains the M14 gate.

## Migration and team policy

Migration views observe the full project, including dependencies and ordinary analyzed writers. Path arguments filter the displayed regions and adoption queue; eligible module/function counts still describe every captured source file and declaration. Ordinary async, methods and unsafe adapters remain visible without a checked claim. Readiness groups actual direct and retained callable edges, orders prerequisites before callers, and keeps recursive components together. Its candidate contracts are hypothetical analysis evidence; checked prerequisites require current strict source proof on disk.

```sh
pyalamode baseline --root /path/to/project --owner "maintainer" --rationale "reviewed current debt"
pyalamode regions --root /path/to/project
pyalamode ready --root /path/to/project
pyalamode convert function:core:total --preview --root /path/to/project
pyalamode convert module:core --preview --root /path/to/project
pyalamode report --root /path/to/project --save --json
```

Conversion only proposes a finite module marker, an already available identity `@fun` marker, or an inherited conservative reassignment/persistent-update repair. The complete overlay is checked again by the actual engine with current policy and history. No command applies an edit or inserts imports, effects, approvals or suppressions. Existing source and policy files remain available for your review. Follow [the isolated migration walkthrough](examples/migration/README.md) for an existing-debt repair and ordinary function adoption.

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

Each gate is independent and defaults to false. Exact current required exports must already be selected and verified. Historical gates require a valid local reference; first-baseline capture bypasses that missing history only. A baseline can record current non-tooling source or policy debt with command status 0 and an unverified receipt, preserving the strict/current-policy statuses and events. It never waives a source, export or expiry failure. Audit returns 0 for unchanged reviewed findings when current requirements and chosen ratchets pass; introducing a new finding fails even when other debt was fixed. Identical repeated contexts carry explicit occurrence counts; ambiguous identity requires review.

`baseline --replace` requires an explicit owner/rationale and valid predecessor. Baseline history is immutable and records any validated relocation lineage. `report --compare .pyalamode/history/ID.json` compares an explicit local reference. `report --save` keeps the report command's actual status: a failing report is 1 although its successful write receipt is 0. JSON write commands return `{report, written}`. Saved records remain historical evidence; observations and publication refresh current source/writers, policy, product, installed external identities, UTC expiry and reference bytes. Approval-failure visibility follows actual required operations and preserves the inherited audit behavior; unused denied catalog entries are not source failures.

`.pyalamode` records are excluded from source, alongside `.git`, `.venv`, `__pycache__`, build/dist, caches and egg-info directories. The reserved `.pyalamode-build-` directory prefix excludes temporary product staging. A user-owned output subtree outside those exclusions becomes source at the next observation. Only baseline and report-save commands write migration records. Other migration views are read-only. [The M10 handoff](Docs/milestones/10-migration.md) and [record contract](Docs/evidence/m10-policy.md) define exact identity, status and IO limits. Migration usefulness remains **UNMEASURED**, with zero participants/attempts.

## Check, build, and inspect

```sh
pyalamode check examples/modules --json
pyalamode build examples/modules --output build/modules-first-use
python -m examples.modules.demo
pyalamode check --audit tests/fixtures/m02/changing_capture.py
pyalamode explain PAL240
pyalamode explain tuple
pyalamode explain Callable
pyalamode explain Vector
pyalamode explain PAL250
```

A build freshly checks selected source and resolved local dependencies, copies unchanged Python bytes in off/exports mode, optionally generates the selected façade/debug assertions, and writes `pyalamode-evidence.json` in a fresh output directory. To run a copied example, enter that directory and run `python -m examples.records.demo` with the installed Pyalamode library available. Builds require a participating function, record/variant declaration or functional module, reject existing outputs, and publish no artifact after a failed gate, generated-source compile error or freshness check. Checked package distribution and separate consumer verification use the finite wheel workflow below.

Strict failures return status 1. Tooling, syntax, policy, and unsupported-target errors return 2. Audit findings alone return 0, label evidence unverified, and leave ordinary behavior unchanged. An empty ordinary selection may pass `check` but supplies no participating function or module claim. The same commands are available as `python -m pyalamode`.

At runtime, `fun(function)` returns that identical function object. It does not wrap, register, guard, or create check evidence. Ordinary callers satisfy exact recursive data/callback contracts and leave dependencies/captures unchanged; selected generated aliases add only their stated data coverage. Unchecked monkey-patching violates the execution precondition; no live dependency monitor is installed. Resource exhaustion, interruption, interpreter tampering, and arbitrary dynamic Python are outside the guarantee.

Disposable `.pyalamode-cache` entries include source bytes, target, policy, product identities, transitive local import bytes, resolution identities, and relevant analyzed binding replacements. An unchanged warm check reuses body evidence. A dependency edit invalidates its import closure; unrelated modules can retain hits. Adding an ordinary writer that replaces a referenced callable or foundation binding also invalidates affected evidence. Import closures are conservative: unused local imports and unrelated edits within an imported file can invalidate callers. Missing or corrupt cache entries trigger fresh checking. Builds bypass the cache and recheck source/dependency bytes and policy before publication.

## Verification and handoff

```sh
python -m unittest discover -s tests -p 'm*.py' -v
python benchmarks/m01_scalar.py --output /tmp/pyalamode-m01.json
```

The M7 suite adds exact standard signatures/identities, nested composition/partial evidence, eager ordering, conditional Unicode failures, per-occurrence wrapper validation masks, cold/full/partial cache equality, separate ordinary setup/import evidence, shared native/helper/globals writer refusals, supported filesystem configuration and real off/exports/debug workflows. The M6 suite adds case-set freshness and explicit-case policy, full/guarded/nested pattern coverage, opaque exception cleanup/collision gates, per-call failure masks preserving effects, ordered immutable error accumulation, supported variant guards and nonexecuting ordinary builds. The M5 suite adds finite operation/declared/required effect unions, concrete and conditional higher-order capability slots, data/alias/capture/lifetime escape refusals, controlled providers, whole-path IO cleanup, permission gates, partial warm callable evidence, and current source/policy/product/writer fingerprints. The M4 suite inherits the earlier adversarial guarantees and adds fixed record/schema/definition evidence, nested record validation, retained replacements, exclusive snapshot assertions, foreign hook/metadata refusal, fresh by-value exports, finite adapter qualification, selected guard entry/return coverage, internal-call isolation, debug coverage, circular initialization refusal and runtime-byte/policy/writer freshness. See [the M4 handoff](Docs/milestones/04-records.md), [the M3 handoff](Docs/milestones/03-collections.md), [the M2 handoff](Docs/milestones/02-modules.md), and [the composite specification](SPEC-sol6.1-composite.md). Human authoring-time and usability claims remain unmeasured.

## Checked installed packages and stable encoding

An explicit `[tool.pyalamode.distribution]` table selects initialized flat-layout Python packages and actual public strict exports. `pyalamode build --wheel --root PRODUCER --output FRESH/checked_pricing-1.0.0-py3-none-any.whl --json` publishes an ordinary source wheel with static export contracts, original authored bytes, artifact hashes, separately characterized initialization and optional guard coverage. It reads metadata as data and never invokes a build backend or application import. Supported source/metadata layouts and input sizes are finite; ambiguous owners, namespaces, shadows and source/cache corruption refuse.

A separate consumer installs the wheel normally, declares `[[tool.pyalamode.checked_dependencies]]` with exact `schema=1`, name/version/packages, then uses ordinary `check` and `build`. The checker reanalyzes installed authored sources, all relevant writers and transitive callers under the consumer's own current policy and exact native-operation approvals. Producer approval supplies provenance. Installed functions keep separate dependency coverage and authored locations; they do not enlarge the consumer's local coverage denominator. Missing or well-formed stale/incompatible evidence is PAL370/1; unpublished or refused source is PAL371/1; a valid late change is PAL372/1 with no artifact. Malformed ownership/metadata/cache/read inputs are tooling2 and cannot become baseline records. See [the separate producer/consumer example](examples/distribution/README.md) and [the distribution contract](Docs/evidence/m11-distribution.md).

Wheel guards use package-owned aliases such as `checked_pricing._pyalamode_exports.core:quote`. Tree builds retain their documented alias namespace. Stock Python imports and calls accepted code without a certificate lookup or registration service. The caller preserves checked source/product/native dependencies and exact data/callback/lifetime obligations between the gate and execution. Relevant caches may be absent; present opt0/1/2 CPython caches must match bounded current compiler output. Static checking compiles source only and never unmarshals supplied bytecode. Concurrent unchecked replacement after the gate violates the existing runtime precondition.

`value_encode(value, schema)` and `value_decode(data, schema)` provide versioned stable bytes for exact scalars, recursive persistent collections, records, `@oneof` domains, closed unions, Option/Result and payload cases. A checked body passes a resolved exact schema expression in argument two; strings, runtime schema values, callable/capability payloads and codec calls in initialization/defaults are refused. The format preserves signed64 ints, bool distinction, every Python string including surrogates, declaration order and canonical Map/Set order. Bounds are 1MiB wire, depth32, 16,384 nodes and 4096 container entries. Decode allocates only admitted exact nominal identities through trusted native storage, with no arbitrary constructors or restoration hooks. Invalid schema/input fails TypeError; malformed/oversized/noncanonical supported values fail ValueError, with conservative RecursionError. [The encoding contract](Docs/evidence/m11-encoding.md) defines the exact grammar, limits and costs.

Current migration states use closed schema2/current22 product identities. Genuine M10 schema1/exact19 records remain validated historical provenance with their original IDs and lineage; reading them cannot certify current inputs. Frozen M11 engineering verification passed 461 methods on each supported target, fresh installed consumer gates and all 78 independent fixed cases; the two bounded distribution/encoding measurement protocols are complete. [The M11 evidence](Docs/evidence/m11-distribution.md) records actual costs, repairs and scope. Human onboarding, editor/integration repair, authoring time and dialect usefulness remain **UNMEASURED**, with zero participants/attempts.
