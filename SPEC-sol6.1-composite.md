# Pyalamode: composite product specification

**Status:** Proposed composite for implementation planning  
**Date:** October 8, 2026; revised October 9, 2026  
**Product:** An opt-in functional subset of Python, static checker/compiler, and ordinary immutable value library  
**Scope:** XL ambition, delivered through a bounded core and separately gated extensions

This proposal follows the review in [SPEC-sol6.1-review.md](/Volumes/Projects/pyalamode/SPEC-sol6.1-review.md). Its base is `SPEC_sol6.1-with-prev.md`, with selected semantic rules and initial-release sequencing from `SPEC_sol6.1.md`, enforcement terminology from `SPEC_sol5.6.md`, and command and diagnostic ideas from `SPEC_fable5.1.md`.

It resolves competing choices rather than retaining every proposed feature. All APIs, rule codes, configuration fields, and commands below are proposed interfaces; this project does not yet implement them.

**Architecture decision:** Enforcement is primarily at check/build time. Accepted compatible-edition code runs on stock CPython, with ordinary library support for immutable values and optional guards at unchecked boundaries. The product requires no custom VM, mandatory specialized loader, runtime verification registry, or per-invocation certificate check.

## 1. Purpose and essential decisions

Pyalamode lets a Python team protect one calculation, then a larger functional core, without replacing its application framework or interpreter. Within participating code, bindings are initialized once, ordinary data is deeply immutable, and behavior depends on explicit stable inputs and characterized operations. An ordinary or explicitly effectful shell performs integration work.

The product must supply useful programming tools as well as restrictions: persistent updates, checked composition, records, closed alternatives, failure values, and intentional Python boundaries. A successful strict check must make a meaningful claim about supported behavior.

The governing decisions are:

1. **Compatible source preserves accepted Python expression semantics.** Mutable literals keep their Python meaning and are rejected from strict data code. They do not become persistent collections through a hidden transformation.
2. **Functions and modules are the adoption boundaries.** `@fun` and `# mode: fun` are the canonical declarations. Classes use explicit record or variant declarations. Inline block markers and mid-function toggles are outside this contract.
3. **Off, audit, and strict are different enforcement modes.** Audit is useful without establishing a functional guarantee. Strict checking/building rejects unknown operations and unsupported constructs. Runtime guards are a separate option, not the definition of strictness.
4. **Source evidence, external trust, effects, and failures remain separate.** A trusted pure operation is distinguishable from a checked pure operation. An effectful checked function is distinguishable from either.
5. **The first release is small enough to characterize completely.** It statically checks scalar calculation functions on one CPython minor. Modules, collections, interoperability, and richer inference expand that subset later.
6. **Ordinary Python integration is a durable part of the design.** Unchecked shells and adapters remain usable, but do not receive a strict certificate.
7. **Advanced features require new evidence.** Builders, concurrency, and syntax cannot weaken existing guarantees or become prerequisites for a useful core release.

The initial reference target is **CPython 3.13 on macOS and Linux**, using an explicitly published supported patch range. This is a scope choice, not a claim that 3.13 is the newest Python. A release must identify its tested patches. Other minors, free-threaded builds, alternative interpreters, and Windows support require their own compatibility gates.

## 2. Users and first experience

The primary user is an application developer moving business rules into a functional core. Maintainers review effects and trust, integration owners characterize external operations, and library authors publish checked exports. These are workflow roles without an account service.

A first-use example is ordinary Python:

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

The developer runs `pyalamode check` or `pyalamode build`, then executes the source or produced artifact with ordinary `python`. Reassigning `result`, introducing an unknown operation, or supplying an inadmissible argument from an analyzed caller fails static checking. A caller outside analysis must satisfy the public input contract; optional export guards can later validate supported inputs before the body. The first guide must demonstrate both a successful calculation and a rejected build-time violation.

For compatible source, `@fun` is a runtime identity marker: it returns the original function without registration, wrapping, or purity enforcement. A module directive or project policy can select code without even that marker-library dependency. Checking/building supplies the evidence, not decorator execution.

Adoption must not require a browser dashboard, new Python grammar, persistent collections, or organization policy before this example works.

## 3. The guarantee and its evidence

### 3.1 Behavior

For checked source, assuming its input and dependency contracts hold, a pure computation observes only explicit admitted inputs and stable approved dependencies. It does not change those inputs or perform observable external effects. On completion it returns admitted data or produces a characterized failure. It can diverge; resource exhaustion and process interruption are not eliminated.

The static guarantee is conditional on actual inputs having their admitted types and contents, callbacks satisfying their contracts, approved dependencies remaining unchanged, and unchecked code not mutating shared dependencies or violating ownership assumptions. Checked callers must establish these obligations statically or through a characterized conversion. Ordinary callers assume responsibility for them unless a selected boundary guard validates the relevant property. This is a strict language contract, not merely advice; it is not an unconditional claim about arbitrary Python callers.

The repeated-computation promise is defined over **contract-equivalent inputs**, under the same supported operation and runtime contracts. Equivalence includes the admitted type or variant tag, recursively equivalent payloads, and the order of ordered values. It is not defined by arbitrary Python `==`; cross-type scalar equality, allocation identity, and an unspecified iteration history cannot silently stand in for the complete input contract.

Records and collections publish their equivalence rules. Function arguments use callable contracts and stable captures rather than object-identity equality. Numeric types with NaN, signed zero, numerical contexts, or platform-sensitive behavior require a separate contract before admission.

This guarantee is relative to the characterized runtime and disclosed dependency assumptions. It is not security isolation from hostile Python, native code, or interpreter modification.

### 3.2 Independent dimensions

Every report and public export carries these dimensions:

| Dimension | Values and meaning |
| --- | --- |
| Enforcement | Off, audit, or strict at check/build time |
| Behavior | Pure, or a declared upper bound of characterized effects; unknown behavior has no certified bound |
| Source evidence | Checked participating source, opaque external implementation, or unchecked source |
| Trust | The complete relevant external assumptions, including transitive dependencies |
| Failure | Characterized failures, including expected result alternatives when applicable |
| Freshness | Current for the recorded source/build inputs, or stale and requiring rechecking before a new checked build |
| Boundary protection | Unguarded by default, or selected export/debug guards with stated validation coverage |

A strict export is admitted only when its implementation is checked or its operation is covered by an explicitly approved trusted contract, all relevant dependency conditions hold, and its effects fit the receiving policy. Checked source that calls a trusted integration remains **checked with external trust**. That trust propagates to callers and artifacts.

The core interpreter and product primitives are an explicitly identified trusted foundation in every claim. External integration trust is an additional list, denied by default until project policy approves specific entries. Checking a wrapper does not remove that list.

Invalid, unsupported, stale, or insufficiently characterized code is **unverified** for the claimed build. A cast, `Any`, a suppression, or a declaration reading “pure” cannot promote it. Known effects can be permitted; unknown behavior cannot be converted into known behavior by adding an effect name. Runtime violation of a disclosed precondition invalidates the claim for that execution; the default artifact is not required to detect the violation.

### 3.3 Unsafe integration

An uncharacterized operation may run in an ordinary Python adapter carrying an unsafe marker, scope, and rationale for reporting. This is an integration facility outside certified strict source.

A pure strict function cannot call that adapter. A checked effectful function also needs a characterized operation contract before making the call. The application may execute an ordinary adapter, snapshot or validate its output at an explicit boundary, and start a new strict computation on the resulting data. This certifies that computation, not the preceding adapter.

There is no unchecked hole inside an otherwise certified function and no generic `trust_me_pure` operation. Maintainers can approve an external contract; its assumption remains visible.

## 4. Editions and boundaries

### 4.1 Compatible edition

The initial edition is `python-v1`. It uses Python grammar and an external static checker. A checked build may copy compatible source into a normal artifact without transforming its bodies. It can generate explicitly selected boundary guards, but otherwise preserves the value types, evaluation order, and scope of admitted source expressions.

```python
# mode: fun
from pyalamode import Vector, fun

def plus_one(value: int) -> int:
    return value + 1

def revised(values: Vector[int]) -> Vector[int]:
    return values.appended(42)
```

The directive is in the module header, after any shebang, encoding declaration, and module docstring, before imports or other executable statements. A misplaced marker is an error. Module mode covers definitions and initialization expressions; functions are pure by default. After the effects milestone, an explicit effect declaration makes a function checked effectful code.

In an ordinary module, `@fun` covers one function, its nested definitions, captures, defaults, and dependencies. It does not certify the module's unrelated initialization. Only recognized declaration decorators and separately admitted decorator contracts are permitted on that function.

Package or project policy may require module mode without source markers. There is no `@unfun`, `with unfun:`, `with fun:`, or ordinary-comment region toggle in this edition. Extracting a local function with explicit inputs is the small-region alternative.

### 4.2 Optional syntax edition

A separately identified source format may later add `val` and immutable collection literals. It requires explicit translation before Python execution and edition-aware editor, formatting, source mapping, type feedback, and packaging support.

```text
# illustrative optional dialect; not ordinary Python
val prices = [10, 20, 30]
val revised = prices.updated_at(1, 25)
```

This changes authoring convenience, not purity or evidence requirements. A new source extension prevents ordinary-looking `.py` files from relying on a hidden loader to obtain different literal semantics. The compatible edition remains supported indefinitely.

Inline regions, pipeline punctuation, placeholders, and arbitrary macros are separate proposals. They are not implied by shipping `val`.

## 5. Static enforcement and runtime responsibilities

### 5.1 Check and build

`check` reads and analyzes source without importing application modules or evaluating user annotations, defaults, decorators, or conversion hooks. It constructs the required dependency and operation model statically. An unresolved construct remains unsupported or unknown. Strict checking fails; audit reports adoption obstacles.

`build` makes successful strict checking a prerequisite for producing a checked artifact. An invalid participating function, default, decorator, class body, annotation expression, or strict module initializer fails the build before application code executes. This is enforcement by a build gate, not interception of definition-time behavior inside an already running interpreter.

The compatible artifact is ordinary Python source/package content, with contracts and build evidence added as packaging support matures. It runs through normal Python commands and imports. There is no requirement to use a specialized loader, register functions, or validate a certificate on each invocation. The initial scalar checker can supply the full initial static contract before any export-guard feature exists.

`run` is an optional convenience command that checks the selected project and then launches stock Python. It supplies no stronger runtime protection than the same successful check followed by ordinary execution. Later dynamic loads do not receive automatic certification; strict source excludes dynamic imports, and unchecked shell behavior lies outside its claim.

Executing source without a successful current check establishes no checked claim, even if it contains `@fun` or a comment marker. Python may still execute it normally. The product's build and CI gates prevent invalid code from being accepted as checked; they do not prevent a developer from bypassing those gates.

### 5.2 Dependency assumptions and build freshness

Checking resolves the callable and constant bindings a function is allowed to use, including builtins and product primitives. Admission follows the analyzed target and exact supported behavior, never a familiar spelling alone. A normal Python global cannot serve as a constant merely because its current object is an integer. Strict imports and closed captures must refer to statically established stable bindings.

The checker rejects writes, monkey-patching, or unknown dispatch within analyzed code that would undermine those bindings. Effects and trust declarations must characterize dependencies used across the boundary. Unchecked mutation of a module attribute, callable, capture, or builtin after checking violates the execution assumptions; the default artifact does not police it. A protected runtime namespace or live dependency identity monitor is not required.

Verification fingerprints include relevant source or artifact bytes, edition, checker rules, target Python version, policy, dependency identities, operation contracts, and trust approvals. A relevant change invalidates cached results for subsequent checks/builds. A warm check may reuse only unaffected evidence.

Published evidence describes a particular build and dependency set. It is not a live certificate for a process whose environment has changed. Consumer checks and normal dependency locking can establish compatible build inputs; runtime tamper detection remains outside the default contract.

### 5.3 Ordinary library support and optional guards

Runtime support has narrowly defined jobs:

| Facility | Default responsibility |
| --- | --- |
| Scalar calculations and builtin immutable values | Stock Python operations; no functional enforcement runtime |
| Declaration markers | Identity/no-op declarations for ordinary Python compatibility |
| Persistent collections and records | Ordinary library implementations, immutable operations, and construction invariants |
| `freeze`/`thaw` and named adapters | Explicit conversion, supported-data validation, and independent snapshots/exports |
| Effect capabilities | Ordinary characterized library interfaces to external operations |
| Export/debug guards | Optional generated validation of stated boundary or data assumptions |

Library construction checks preserve the library's value invariants. They do not track local assignment, infer effects at runtime, or install a new execution environment. Static-only enforcement can initially use builtin immutable values; persistent structural sharing later needs library algorithms and storage, not a different interpreter.

After the boundary-support milestone, guard settings are `off` (default), `exports` (selected public exports), or `debug` (exports plus supported internal data assertions). Export guards can reject unsupported incoming types, nested mutable data, or invalid returned data at the relevant boundary. They do not automatically freeze arguments or prove a callback pure from its annotation. Callable admission still needs checked evidence or a characterized trusted contract.

Checked internal calls ordinarily need no wrappers or repeated deep validation. Debug assertions and public guards have published coverage and overhead. Neither can discover every hidden effect, establish arbitrary ownership, or protect every dependency from unchecked mutation. A guarded export's additional claim states exactly which invalid inputs it rejects; its purity still depends on the remaining disclosed assumptions.

### 5.4 Architectural alternatives

| Alternative | Position |
| --- | --- |
| Static checker, explicit immutable values, ordinary Python execution | Default compatible edition; least disruption and no generated bodies required |
| Source compiler lowering immutable literals or `val` to Python library operations | Viable optional edition; different source semantics, same stock Python runtime |
| Different VM, custom object model throughout Python, or universal execution guard | Excluded from the core; would need a separate demonstrated requirement |

Private mutable builtin containers could eventually be allowed through a sufficiently strong ownership/escape analysis. They are not necessary for the initial product and remain excluded from ordinary strict data code. Choosing explicit immutable values avoids making that analysis a first-release prerequisite.

## 6. The initial strict subset

Milestone 1 is deliberately narrower than the complete product:

| Area | Initial admitted behavior |
| --- | --- |
| Runtime | Published CPython 3.13 patch range, standard supported build, macOS/Linux |
| Scope | Top-level `@fun` functions, without nesting, closures, defaults, or additional decorators |
| Public contract | Explicit parameter and result annotations from a non-executed whitelist; obligations for ordinary callers |
| Values | Exact `NoneType`, `bool`, `int`, `str`, and `bytes`; no subclasses or arbitrary protocols |
| Statements | Simple local binding, `if`/`elif`/`else`, `return`, and `pass` |
| Expressions | Literals of admitted types, names, characterized unary and binary scalar operations, boolean conditions, comparisons, and conditional expressions |
| Calls | A published small whitelist, initially `abs`, `min`, `max`, and `len`, with exact admissible argument rules |
| Dependencies | Marker/runtime primitives and the approved builtin vocabulary; no ambient application globals |
| Excluded | Statement loops, comprehensions, imports in bodies, mutable containers, arbitrary calls, recursion, async/yield, reflection, user `raise`/`try`, record objects, and effects |

An overloaded operator is admitted only for its characterized operand types. Static contracts distinguish exact `bool` from exact `int`; an `int` annotation in this subset requires an exact integer rather than arbitrary subclass behavior. An analyzed call must establish that requirement, and an ordinary caller must satisfy it. Optional guards can later check it at entry. Builtins are resolved statically against approved behavior and supported signatures, conditional on the binding remaining unchanged during execution. Unsupported operand combinations fail static checking.

The initial operation whitelist is finite:

- Exact integers support unary `+`/`-`, binary `+`/`-`/`*`/`//`/`%`, and same-type comparisons. Floor division and remainder can produce characterized `ZeroDivisionError`. `/`, exponentiation, and additional numeric types wait for a later contract.
- Exact strings and bytes support same-type concatenation, equality, ordering, and `len`. Indexing, slicing, interpolation, formatting hooks, and methods wait for later admission.
- Exact booleans support `not`, boolean `and`/`or`, and equality. Initial branch conditions require a boolean result. Supported `is None` and `is not None` tests do not expose allocation identity.
- `abs` accepts one exact integer. `min` and `max` accept two or more scalar positional arguments of one supported exact type (`int`, `str`, or `bytes`); iterable, `key`, and `default` forms are excluded. `len` accepts one exact string or bytes value. No other builtin call is admitted initially.

Cross-type coercion and comparisons are excluded initially. Each later operation publishes its concrete input types, result type, behavior, and failure categories before joining the admitted vocabulary. Compiler-created temporary argument storage is trusted implementation machinery, not an escaping mutable source value.

Function discovery and annotations use supported source syntax, without `get_type_hints` or equivalent user-code evaluation. The ordinary caller's code is not claimed pure merely because it invokes a checked function.

This subset supplies useful arithmetic, comparisons, text combinations, and decision logic. It is a strict first release when the static checker covers its closed vocabulary, rejects invalid participating code, and gates checked builds. A runtime boundary validator, custom loader, or verification registry is not required. Audit remains a separate way to inspect noncompliant code without accepting it as checked.

## 7. Bindings and control flow as the subset expands

Ordinary assignment in strict source initializes a binding. Parameters are already initialized. Each reachable path that uses a name must establish it exactly once during its logical lifetime.

Mutually exclusive branches can supply one binding. A second assignment on a reachable path fails even if it supplies an equal value. An omitted initialization on a used path also fails. Earlier returns participate in that analysis.

The rules cover all admitted binding forms: destructuring, definitions, imports, patterns, and parameters. Duplicate targets, augmented assignment, explicit deletion, `global`, `nonlocal`, and assignment expressions fail. Writes to attributes or elements are separate mutation violations.

Nested functions may shadow names in actual nested scopes. An `if`, `match`, or ordinary `with` suite is not a new lexical scope. Captures must refer to stable immutable values and admitted callables. An analyzed later write to an enclosing cell blocks admission; an unchecked write violates the declared stable-capture precondition. No runtime closure-cell monitor is required.

Early collection algorithms use characterized transforms and folds. Later statement iteration can be admitted under an explicit restriction: targets and body-local bindings are initialized for each iteration, cannot overwrite preexisting surrounding bindings, cannot carry state across iterations, and cannot be used after the loop. The runtime retains Python's actual scope behavior; the checker prevents observation of that behavior outside the admitted lifetime.

A closure over a reused loop cell cannot escape its iteration. A checked factory that receives the iteration value as an explicit parameter can create a stable closure. This also applies to callbacks produced by comprehensions. Uncertain alias or escape behavior is rejected.

Ordinary `while` statements remain unsupported in the core edition. Recursion and immutable iteration helpers become available with explicit call contracts. This is a subset decision, not a claim that every terminating loop requires mutation.

Patterns operate only on admitted shapes and characterized dispatch. Failed attempts cannot supply observable captures; guards count toward exhaustiveness only when their coverage is established. Captures cannot overwrite an existing stable binding. The initial pattern subset avoids ambiguous partial-binding behavior and rejects capture reuse where successful initialization cannot be established.

Exception targets and interpreter cleanup need a distinct handler lifetime. Exception objects and traceback cells cannot escape into strict data or captured functions. They are not silently treated as ordinary immutable values.

## 8. Values, snapshots, and Python boundaries

### 8.1 Admitted values

After the initial release, the value domain expands to recursively immutable exact tuples, product collections, product records and variants, and admitted callable values with stable captures. Additional numeric and foreign record types require explicit contracts.

Immutability covers every reachable observable component and its admitted behavior. A tuple containing a list, a frozen record containing a mutable view, or an object whose getter reads changing state is inadmissible. Hashability, `Final`, `Sequence`, `Mapping`, and setter rejection alone are insufficient.

The product distinguishes stable data, callable contracts, temporary construction state, effect capabilities, and foreign data. A database connection, iterator cursor, coroutine, or builder is not an immutable record field. Callables cannot be serialized or used as identity-based collection keys merely because they are permitted as callbacks.

Allocation identity, frame inspection, weak-reference observations, address-based representation, and exposing process-randomized hashes are excluded from pure computations. `is None` and other explicitly supported singleton tests remain available.

### 8.2 Boundary conversions

`freeze` constructs a supported immutable snapshot in an ordinary shell or characterized effectful adapter. It is not a universally pure operation on arbitrary objects. `thaw` creates an independent mutable export at an integration boundary.

| Source | Snapshot result |
| --- | --- |
| Admitted stable data | Validated reuse where safe |
| Exact builtin list | Vector with recursively converted elements |
| Exact builtin tuple | Tuple with recursively converted elements |
| Exact builtin dictionary | OrderedMap by default, preserving meaningful insertion order |
| Exact builtin set/frozenset | Unordered Set with recursively admitted elements |
| Subclass, arbitrary object, live view, cycle, or capability | Explicit failure unless a named adapter provides a qualifying contract |

An unordered Map is constructed explicitly when order is irrelevant; converting an ordered dictionary to it is a visible choice. This avoids silently dropping meaningful source order.

Conversion retains no mutable alias into source storage. Repeated acyclic references are accepted without preserving object identity. Unsupported cycles and values fail with a nested path. Generic conversion does not invoke user-defined properties, iterators, constructors, hash methods, or restoration hooks; converted key types must have characterized hashing and equality.

The caller must provide exclusive access during snapshotting or a characterized synchronized snapshot adapter. The library cannot infer exclusive ownership of arbitrary Python objects or universally detect concurrent writes. Without that precondition, it offers no consistent-snapshot claim. Known instability is an explicit failure, not a partially certified result.

Ordinary code can continue mutating the original after conversion. The snapshot stays stable. `thaw` mutations likewise cannot affect the strict source. No automatic in-place freezing of existing aliases is promised.

## 9. Collections and functional algorithms

The core collection vocabulary is eager:

| Type | Representative operations and semantics |
| --- | --- |
| `Vector[T]` | `of`, index, slice, `appended`, `updated_at`, `concat`, `map`, `filter`, `fold` |
| `OrderedMap[K, V]` | `updated`, `without`, lookup, ordered entries and values; order participates in contract equivalence |
| `Map[K, V]` | Lookup, `updated`, `without`, merge, extensional comparison; no incidental ordered traversal |
| `Set[T]` | Membership, `added`, `without`, union, intersection, difference; unordered value semantics |

Update operations return new values and preserve every retained earlier version. Static construction/update contracts require admitted nested values; library constructors validate supported value invariants when accepting ordinary Python data. This is ordinary library behavior, not a per-call purity guard. Ignoring a known return-only update produces a diagnostic. The checker resolves operation contracts rather than categorically rejecting a method spelling.

Mutable literals, comprehensions producing mutable containers, and mutable constructors are rejected in strict data code. The tools suggest explicit immutable constructors and transformations. A later approved eager constructor may consume a confined generator expression over stable inputs; a general Python generator remains a stateful cursor and cannot escape as strict data.

Callback contracts propagate through every higher-order operation. For effect sets, the initial rule is set union: the operation's own characterized effects plus the callbacks' effects must fit the caller's declared bound. The system does not require arbitrary effect-row inference in its first useful release.

General `map`, `filter`, and `fold` operate on ordered inputs. Unordered maps and sets provide a finite characterized vocabulary of order-independent operations. A general callback or reducer is not presumed order-independent because it looks mathematical. To obtain an ordered result, select a supported total ordering or supply an OrderedMap/Vector whose order is part of its input value.

Canonical ordering defines tie behavior, comparison failure, and admitted key types. Formatting, serialization, diagnostics returned as values, and error selection obey the same rule. Internal storage hash order cannot leak through a pure result. Heterogeneous key domains with ambiguous equality or ordering are rejected until an explicit contract defines them.

The standard toolkit expands to eager folds, scans, grouping, composition, partial application, and result traversal. Recursion is permitted after checked call-graph support; termination and tail-call optimization are not promised. Captured arguments obey the same stable-value rules as closures.

Existing persistent implementations may provide storage. A product façade must characterize their exact operations, validate nested contents, restrict mutable export and evolver APIs, and document backend trust. Reuse is preferred when it satisfies these requirements; a library's immutable outer container is not by itself sufficient.

## 10. Records, variants, and failure

Records use explicit declarations:

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

Records have fixed typed fields, deep validation, stable defaults, pure field access, value comparison, pattern matching, and copy-with-changes. Hashing is available only under a characterized field and equivalence contract. Representations cannot expose storage order or invoke unknown methods.

The checker rejects uncharacterized record subclassing, dynamic attributes, descriptors, metaclasses, and replacement of behavioral class attributes. The record library enforces its documented construction and ordinary field-update restrictions. Unchecked alteration of behavioral definitions violates the dependency assumptions; universal runtime sealing is not promised. Methods, properties, defaults, constructors, and validators must satisfy their contracts. Existing dataclasses or named tuples can qualify through a compatibility contract; `frozen=True` alone is not certification.

Closed variants have a declared, stable case set and immutable payloads. `Option` and `Result` supply absence and success/error workflows. Validation combinators can accumulate independent immutable errors. Adding a variant case invalidates relevant exhaustiveness evidence.

A guarded case does not automatically cover its entire variant. An explicit wildcard can cover future cases when project policy permits it; adding a case does not necessarily break a deliberately exhaustive wildcard consumer. Projects can require explicit case handling for selected domain types.

Purity and totality remain separate. Characterized arithmetic failures can propagate without licensing I/O or changing state. Failure contracts list known categories; they are not a proof of every possible process failure. Early releases allow propagation of admitted builtin failures, while rejecting arbitrary user exception construction and handlers.

Later characterized handlers can inspect supported failure categories and immutable payloads or convert them into Result values. They cannot expose mutable exception dictionaries, tracebacks, frames, unknown cleanup, or arbitrary formatting hooks to pure code. Handling failure can discharge that failure requirement; it cannot erase effects already performed.

## 11. Effects and capabilities

The ordinary Python shell is sufficient for the initial product. A later checked shell declares effects as a finite upper bound and receives opaque capabilities for the operations that perform them.

The initial effect families are `IO`, `State`, `Clock`, `Random`, `Environment`, and, when concurrency is admitted, `Task`. Operation contracts can distinguish narrower permissions such as file reads and writes without creating a new language mechanism for each distinction. Failure remains a separate dimension. Unknown behavior remains unverified rather than an effect that authorizes arbitrary execution.

An effect declaration opts a function into checked effectful mode. It retains single assignment and immutable ordinary data. State changes occur through characterized capability operations, not arbitrary writes to domain records.

Every explicit and implicit operation participates: direct calls, operators, properties, truth testing, equality, hashing, formatting, iteration, matching, and context-manager entry and exit. Dynamic dispatch passes only when every admitted target fits the required contract. Unsupported dispatch fails closed.

Capabilities carry an allowed operation set and resource lifetime. They cannot be stored in pure records or returned as stable data. Only a later explicitly supported resource-transfer contract may move them between effectful scopes.

Pure callers cannot invoke effectful operations. Effectful callers can invoke pure functions. Test clocks and recorded service providers preserve the effect classification of their interfaces. Passing a timestamp as data can remove a clock dependency from a calculation; substituting a fake clock does not itself make a clock-using function pure.

There are no generic effect handlers or algebraic effect elimination in the core contract. Recorded replay identifies what was recorded and does not promise arbitrary network or process determinism.

## 12. Dependency contracts and distribution

An operation-level dependency declaration contains:

| Field | Obligation |
| --- | --- |
| Identity | Actual resolved operation, package/artifact identity, and applicable versions |
| Inputs and outputs | Admitted types, nested stability, callback contracts, and capabilities |
| Behavior | Effects, failures, implicit dispatch, and delayed execution |
| Aliases | Mutation of inputs, retained aliases, live views, and ownership preconditions |
| Initialization | Effects and evidence for module import or other required setup |
| Evidence | Checked implementation or explicit trusted assumption, with provenance |
| Review | Owner, rationale, policy approval, and any expiry |

Manifests may be product-shipped, dependency-shipped, or project-local. Dependency claims are evidence candidates, not automatic approvals. A project override can select a different trusted declaration with visible provenance; it cannot silently replace checked effects with an unsupported purity claim. Drafted entries remain unapproved and cannot satisfy strict admission.

A pure export does not establish pure import initialization. The ordinary shell may perform separately declared initialization before the pure export participates. Default, decorator, class-body, and annotation behavior are also distinct from later invocation behavior.

The product publishes a small characterized standard-operation set before expanding to more standard-library and third-party APIs. Mutable arrays, tables, sessions, and views need adapters or remain outside mode. Copying input and output can establish data isolation but cannot prove the wrapped operation has no hidden effects.

Published claims attach to strict exports, not indiscriminately to a whole distribution. A package can contain ordinary modules, checked pure exports, checked effectful exports, and operations relying on external trust. Consumers see those distinctions and may impose stricter trust policy than the author.

Built artifacts are ordinary Python distributions and include relevant fingerprints, contracts, original-source locations, dependency assumptions, and the selected guard configuration. Verification is reproducible for the same relevant inputs. Missing evidence or an incompatible dependency version prevents a consumer check/build from accepting an existing claim without rechecking. Normal Python import and invocation remain usable without a runtime certificate service. Packaging must distinguish a statically checked export from an export with additional boundary validation.

Explicit value encodings validate records, variants, ordering, numeric bounds, and schemas. Encoding admitted data can be pure; transporting bytes is effectful. Decoding never executes arbitrary constructors or object restoration hooks. Callables and live capabilities are excluded. Full pickle compatibility is not part of the contract.

## 13. Optional ownership and concurrency extensions

### 13.1 Confined builders

Builders are disabled by default and admitted only after ownership enforcement is demonstrated. Initial support uses one lexical construction callback, one fresh builder binding, characterized builder operations, no builder aliasing, and automatic one-way finalization. Unknown calls, closures retaining the builder, nested storage, and concurrent use are rejected.

The returned result must be stable data; construction failure cannot export partially mutable state. Runtime tokens invalidate unsupported reuse after finalization. A third-party evolver is not automatically a qualifying builder. Broader alias or ownership transfer requires a subsequent contract.

Private implementation mutation inside the trusted collection backend is part of that runtime contract. This is distinct from permitting arbitrary mutation in user strict source.

### 13.2 Explicit task orchestration

The core can be called from ordinary concurrent orchestration without claiming the shell is deterministic. A later characterized task facility passes stable messages and checked callable captures, preserves Task and external effects, and defines result order, cancellation, and failure propagation.

Builders, live views, and foreign mutable captures cannot cross that facility's task boundaries. Controlled scheduling has a bounded published test contract; arbitrary Python threads are not made deterministic. No automatic parallel speedup is promised.

Replayable lazy sequences, observable-cache-safe memoization, and expanded numerical semantics require separate extension proposals. Eager algorithms remain the default. Normal generators, coroutines, and mutable caches are not relabeled immutable because the extension might eventually support something related.

## 14. Commands, diagnostics, and local state

The command workflow is usable without an editor:

| Command | Purpose |
| --- | --- |
| `pyalamode check [paths]` | Strict static verification under selected project policy |
| `pyalamode check --audit [paths]` | Adoption findings without a strict guarantee |
| `pyalamode run <entry.py>` | Optional convenience: check, then launch stock Python without additional enforcement |
| `pyalamode explain <rule-or-symbol>` | Rule examples, value paths, effect paths, and evidence for admission |
| `pyalamode regions [paths]` | Participating functions/modules, mode, effects, trust, and current state |
| `pyalamode ready [paths]` | Candidate boundaries, blockers, and dependency-aware conversion order |
| `pyalamode convert <target> --preview` | Preview proposed source changes and remaining blockers |
| `pyalamode baseline` | Record reviewed audit findings, without certifying them |
| `pyalamode report` | Local human/structured report and change comparison |
| `pyalamode build` | Gate ordinary artifacts on strict checking; optionally generate selected guards or translate the syntax edition |

`check` uses status 0 when its selected gate passes, 1 for unsatisfied verification or policy, and 2 for tooling, resolution, or unsupported-target errors. Audit findings alone do not fail unless a chosen audit gate requires it. Tooling failures are never reported as clean checks. `build` and the optional `run` command stop after a failed gate. A user can invoke ordinary Python independently, but that does not establish a successful check.

Every diagnostic has a stable rule ID, source location, affected boundary, origin, reason, and valid remediation. Examples:

```text
PAL101: `total` is already initialized
  first binding: pricing.py:8
  second binding: pricing.py:11
  derive a new value or use a fold

PAL221: input contract is not established for customer.tags
  the supplied value may contain a builtin list
  create a supported immutable snapshot in the integration shell

PAL310: pure `quote` requires Clock
  quote -> campaign -> clock.now
  pass time as data or move the operation to a declared effectful boundary
```

Editor views share the engine and rule IDs. They show participating boundaries, inferred contracts, transitive trust, and effect origins. Fixes preview program changes. They never silently add permissions, trust, ignored errors, or changed failure behavior.

Migration conversion orders callees before callers and treats recursive components together. A rewrite is automatic only when its behavior preservation is established for the admitted case. Snapshot insertion, class conversion, ordering choices, and broad loop rewrites normally require a reviewed proposal.

Configuration lives in `pyproject.toml` under `tool.pyalamode`, using a versioned schema. The proposed minimum configuration is:

```toml
[tool.pyalamode]
schema = 1
edition = "python-v1"
runtime = "cpython-3.13"
boundary_guards = "off"
require_modules = ["core/**/*.py"]
external_trust = "deny"
builders = false
```

Policy can specify operation approvals, entry-point effect bounds, required exports, audit gates, and optional guards for selected public exports. Source declarations may tighten inherited policy but cannot silently weaken it. Target Python patch compatibility is determined by the published release matrix, rather than guessed from this minor-version field. Turning guards off does not weaken the static rules; it removes only the additional stated runtime validation.

Contract declarations, baselines, and policy remain project files. Baselines and saved reports live under `.pyalamode/`; disposable analysis caches are separate and loss of a cache cannot change a claim. External approvals record scope, reason, owner, and optional expiry. Local history can use normal source review rather than a separate approval service.

## 15. Migration and policy

Baseline identity includes the rule, logical boundary, and normalized violation context rather than only line number or total count. New findings fail a ratchet even when old findings were fixed in the same change. Moving debt does not make it disappear; ambiguous matching requires review rather than silent acceptance.

A baseline may accept audit debt. It cannot waive a strict correctness failure. Removing a marked boundary, reducing required coverage, expanding effects, adding trust, or permitting unsafe adapters appears separately in the change report. A lower finding count does not compensate for any of these changes.

Adoption reports publish their denominator: eligible and selected functions/modules, checked exports, external-trust dependencies, unresolved findings, and excluded source. They do not describe a few checked functions as proof that the whole project is functional.

A project can reject new findings, expired approvals, expanded entry-point effects, new trust assumptions, or lost strict coverage. Baseline and policy changes are explicit reviewable files. Suppression can reduce audit noise, but the underlying strict classification remains unverified.

## 16. Acceptance scenarios

Each expansion inherits earlier scenarios. Stages below refer to the roadmap; they are not claims of an existing implementation.

| ID | Stage | Scenario and required observation |
| --- | --- | --- |
| A01 | 1 | A valid scalar `@fun` calculation passes strict checking/building and runs under ordinary Python. |
| A02 | 1 | Reassignment or parameter `+=` fails and identifies the first binding. |
| A03 | 1 | Exclusive branches initialize a used name once; missing initialization or a second reachable initialization fails. |
| A04 | 1 | An analyzed caller supplying an `int` subclass or mutable value fails static checking; an unknown argument requires evidence rather than being assumed admissible. |
| A05 | 1 | Audit leaves ordinary behavior unchanged and reports no strict certificate. |
| A06 | 1 | Unknown calls, analyzed shadowing of approved builtins, and unsupported constructs fail the checked build. |
| A07 | 1 | Bad defaults/decorators on a participating function are diagnosed without evaluating them or producing a successful checked build. |
| A08 | 1 | Tooling failure or an unsupported target stops the check/build; a successful compatible artifact runs without a special loader or runtime registration. |
| A09 | 2 | Changing a scalar global binding or captured value blocks admission; a checked stable constant is permitted. |
| A10 | 2 | An analyzed callable replacement is rejected and a changed dependency invalidates affected build evidence; unchecked runtime replacement is documented as violating a precondition. |
| A11 | 3 | Vector and map updates preserve earlier versions and reject nested mutable members. |
| A12 | 3 | Unordered map/set history cannot affect an ordered result, formatting, or first-error selection. |
| A13 | 3 | An unknown or effectful callback does not become pure by passing through a collection operation. |
| A14 | 4 | A snapshot remains stable after nested original data changes; thawed data cannot mutate its source. |
| A15 | 4 | Unsupported hooks, cycles, live views, or missing snapshot preconditions do not produce a stable-value claim. |
| A16 | 4 | Static checks, supported conversion/constructor validation, and selected export guards identify nested mutable data; record replacement returns a new value. |
| A17 | 5 | A checked effectful function may use its characterized capabilities and fails on an undeclared effect. |
| A18 | 5 | Callback effects propagate; fake providers retain their effects; unknown operations are refused despite declarations. |
| A19 | 6 | Adding a closed variant case invalidates incomplete explicit consumers; guarded cases do not establish full coverage. |
| A20 | 6 | Handling a characterized failure does not erase other effects or expose mutable traceback state. |
| A21 | 7 | Pure exported behavior and effectful import initialization have separately visible contracts. |
| A22 | 8 | A trusted adapter remains in every caller's assumptions; approval is tied to the operation and installed dependency. |
| A23 | 8 | An unsafe adapter remains outside certification; validated output can start a new strict computation. |
| A24 | 9 | Editor and command diagnostics use the same rule and authored location; optional guard failures and translated-source diagnostics identify their authored boundary. |
| A25 | 10 | Moving old debt preserves identity; adding new debt fails even when the total count decreases. |
| A26 | 10 | Lost strict coverage, new trust, expanded effects, and expired approvals appear independently of debt count. |
| A27 | 11 | A consumed checked package imports normally and exposes its static contracts, transitive assumptions, and selected guard coverage without runtime certification services. |
| A28 | 11 | Source, policy, artifact, or relevant dependency changes invalidate affected evidence at subsequent check/build time. |
| A29 | 12 | A builder cannot be aliased, captured, leaked, used concurrently, or used after finalization. |
| A30 | 13 | Characterized tasks reject mutable captures and retain declared ordering, cancellation, and external effects. |
| A31 | 14 | The optional dialect preserves contracts and results of equivalent supported compatible-edition programs. |
| A32 | Relevant expansion | Custom operators, getters, formatters, matchers, iterators, and context managers cannot hide uncharacterized behavior. |
| A33 | 1 | A raw call using the identity `@fun` marker has ordinary Python behavior and acquires no checked evidence merely by executing the decorator. |
| A34 | 4 | A selected guarded export rejects supported invalid input types and nested mutability before its body; the same unguarded export instead publishes those requirements as caller obligations. |
| A35 | 4 | Checked internal calls have no mandatory generated wrappers or repeated deep validation; optional debug coverage and overhead are documented. |

The adversarial conformance suite must include aliases, exact-type subclasses, builtin shadowing, changing globals, escaping loop closures, initialization effects, failed/guarded matches, and stale contracts. Merely testing happy-path immutable APIs is insufficient.

## 17. Roadmap and release gates

The fourteen milestones express product increments, not equal effort or a promised calendar. Milestones 1–11 form the durable core. Milestones 12–14 are gated extensions. No later feature may weaken earlier contracts.

| Milestone | Delivered capability | Gate |
| --- | --- | --- |
| 1. Statically checked scalar functions | The closed subset, audit/check/build, approved operations, exact-type static contracts, identity markers, and useful explanations | Demonstrate A01–A08 and A33; ordinary execution requires no functional runtime gate |
| 2. Functional modules | Module opt-in, tuples, stable constants, checked call graphs, recursion, defaults, captures, and nested functions | Analyze initialization without executing it; make dependency assumptions explicit |
| 3. Persistent collections | Eager vectors, ordered maps, unordered maps/sets, updates, callback checks, and explicit traversal contracts | Resolve ordering and backend trust; publish update/retention costs |
| 4. Records and boundaries | Library records, replacements, recursive snapshots, fresh exports, qualifying record adapters, optional export/debug guards | Demonstrate nested validation and no retained mutable aliases; guards remain independent of static checking |
| 5. Checked effectful shells | Capability operations, finite effect propagation, higher-order bounds, resource lifetimes, controlled providers | Unknown operations still fail; providers cannot erase effects |
| 6. Domain alternatives and failure | Closed variants, Option, Result, validation, exhaustive matching, characterized failure handling | Guards, wildcards, and exception-state restrictions have precise behavior |
| 7. Standard-operation contracts | Useful text, numeric, parsing, encoding, filesystem, clock, and environment operations | Every admitted operation has versioned behavior and initialization evidence |
| 8. External integrations | Reviewed contracts, narrow adapters, approval policy, and dependency impact | At least two bounded integrations preserve trust, effects, and data isolation |
| 9. Editor experience | Shared diagnostics, inferred contracts, navigation, explanations, safe previews | A new Python user repairs representative violations from feedback |
| 10. Migration and team policy | Readiness, stable baselines, conversion previews, coverage gates, local history/reports | Added debt and policy weakening are detected independently |
| 11. Checked package distribution | Static export claims, installed-artifact evidence, consumer check/build policies, selected guard configuration, source locations | A separate consumer verifies the claim at check/build time and imports the package normally |
| 12. Confined construction | The narrow opt-in builder contract and useful bulk-construction costs | Escape and lifetime rules pass adversarial tests; ordinary data remains stable |
| 13. Characterized concurrency | Immutable task inputs/messages, effect-preserving task APIs, bounded test coordination | Scheduling/failure behavior is explicit; mutable captures fail |
| 14. Optional syntax | Identified dialect, `val`, immutable literal construction, source tooling, packaging | Measured authoring benefit and complete translation/debugging workflows |

Incremental checking and runtime/memory measurements begin with the core, rather than waiting for the final milestone. Targets name the workload, hardware, cold/warm state, and dependency fanout. There is no undefined “large project, under one second” universal requirement.

Before widening any supported operation set, publish its behavior contract, representative use case, adversarial counterexamples, supported environment, and performance implications. A failed gate narrows or defers that extension; it does not turn uncertainty into a warning-based guarantee.

## 18. Non-goals and remaining decisions

The core does not certify arbitrary dynamic Python, isolate hostile code, prove termination or domain correctness, replace a general-purpose type checker, transparently freeze mutable frameworks, automatically parallelize programs, or provide a hosted team platform. It does perform the type and callable analysis required for its admitted operations. A custom VM, mandatory specialized loader, protected process-wide namespace, and per-call certificate registry are also outside the default product.

Universal runtime rebinding or effect surveillance is outside scope. Optional audit instrumentation reports only its documented coverage. Selected boundary guards validate stated properties; they do not enforce the whole process environment, detect every unchecked dependency change, or prove unknown native behavior. Static contracts and ordinary library invariants remain useful when all optional guards are off.

The following decisions require engineering evidence without changing the product direction:

- Define the checker/build interface and exact static assumptions; demonstrate strict failure without evaluating source and normal execution of accepted output before milestone 1 ships.
- Specify optional guard generation, export selection, validation coverage, and overhead before milestone 4, independently of the static rules.
- Choose collection backends and publish their licensing, deep-value façade, trust, complexity, and retained-history costs before milestone 3.
- Define each expansion's exact callable, pattern, failure, and annotation syntax before admission; do not promise general inference before the useful finite rules work.
- Validate the most useful initial standard and external integrations with target users before expanding their contract catalog.
- Measure whether the optional syntax saves enough authoring effort to justify maintaining another source format.

Initial success means a Python developer can statically check a useful scalar function in roughly fifteen minutes, understand its assumptions, see reassignment and unknown behavior fail the build, and run accepted code under ordinary Python. Later success means a real application can retain an ordinary integration shell while publishing an inspectable, immutable, explicitly effectful functional core, with guard coverage chosen where it is useful. Time and usability targets are to be measured, not presented as established results.

## 19. Technical basis

This is a proposed contract, not a completed proof or implementation. The chosen restrictions follow Python's documented behavior: comments do not enforce execution, list displays construct lists, name assignment and object mutation are distinct, defaults and decorators have definition-time behavior, and loop targets retain ordinary Python binding semantics. Static rejection before a checked build and explicit boundary assumptions follow from those facts; they do not require a custom execution environment. [Python comments](https://docs.python.org/3.13/reference/lexical_analysis.html#comments), [list displays](https://docs.python.org/3/reference/expressions.html#list-displays), [execution model](https://docs.python.org/3/reference/executionmodel.html), [function and loop statements](https://docs.python.org/3.13/reference/compound_stmts.html).

Source inspection and optional translation are possible through Python's [AST facilities](https://docs.python.org/3.13/library/ast.html). They are mechanisms on which to build the restricted checker/compiler, not evidence that unrestricted Python can be certified automatically. Python does not itself enforce annotations, which is why an unguarded static claim states caller obligations and an optional export guard has a separate validation claim. [Python typing documentation](https://docs.python.org/3/library/typing.html).
