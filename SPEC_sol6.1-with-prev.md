# Py à la Mode functional Python product specification

**Status:** Proposed product specification  
**Scope:** XL with fourteen independently useful milestones  
**Working name:** Py à la Mode  
**Slug:** `pyalamode`  
**Product:** A Python language mode and developer toolchain

## Purpose and product direction

Py à la Mode lets Python developers place a real functional contract around selected code: names cannot be rebound, ordinary data cannot be mutated through any supported alias, and a function cannot conceal input, output, state, or another external effect. Teams can protect their calculation and decision logic while retaining ordinary Python for application integration.

Start with a checked subset of valid Python, explicit immutable values, and blocking enforcement. Expand into a complete language product with persistent collections, immutable records, higher-order effect contracts, dependency adapters, migration tools, editor support, packaging, and team policy. Offer syntax additions as a separate, opt-in source edition once the underlying guarantees work.

The compatible edition preserves Python's runtime meaning for accepted expressions. In particular, `[]` continues to mean a mutable list and does not secretly become another type. Strict code must use an immutable alternative. The syntax edition may explicitly provide different literal semantics; it must identify itself and require the product's compilation workflow.

The valuable distinction is between three separate properties:

| Property | Promise | Insufficient substitute |
| --- | --- | --- |
| Binding immutability | A name keeps its assigned value within its binding lifetime. | A mutable object behind a constant name. |
| Value immutability | The data reachable from a value cannot observably change. | A frozen outer record containing a list. |
| Purity | Computation depends on explicit inputs and stable constants, with no external effects. | A function that does not assign but reads a clock or a changing global. |

This is a language product, so its syntax, semantic rules, diagnostics, and execution guarantees are user-facing requirements. Implementation mechanisms remain open. It does not need a hosted application or a cloud account.

## Intended users

- **Python developer:** Wants safer domain logic, useful feedback, and familiar Python syntax.
- **Adopting team:** Needs gradual migration without converting an entire application at once.
- **Library author:** Wants to publish immutable values and callable contracts consumers can rely on.
- **Integration owner:** Maintains reviewed boundaries around ordinary Python and external systems.
- **Project maintainer:** Controls strict coverage, permitted effects, dependency trust, and exceptions.

These are workflow roles. The local product does not require user accounts or an authorization server. Any approval requirements come from a project's chosen policy.

## User stories

1. As a developer, I can mark one function or module as functional and receive blocking feedback when it rebinds a name, observes changing data, mutates a value, or calls an unapproved operation.
2. As a developer, I can build records and collections, derive updated versions, match domain alternatives, and compose transformations while the original values remain unchanged.
3. As an application author, I can keep pure logic separate from explicitly effectful integration and see how effects propagate through callbacks and dependencies.
4. As an adopting team, I can audit existing code, save migration debt, and increase strict coverage without presenting unchecked code as verified.
5. As a library author or integration owner, I can publish narrow contracts and adapters that identify checked behavior, external trust, and unsafe behavior separately.
6. As a maintainer, I can review changes to guarantees, trust, and exceptions, enforce policy in automated checks, and understand exactly what a released artifact claims.

## Developer experience and information architecture

The everyday entry points are the command line and editor. All views use the same contract vocabulary and diagnostic identities.

| Area | What the developer sees and can do |
| --- | --- |
| Project overview | See strict boundaries, current failures, dependency trust, and changes since the saved baseline. |
| Check | Check a function, file, package, or project; navigate from a violation to its cause and suggested rewrite. |
| Explain | Inspect a name's binding, a nested mutable value, an operation's effective contract, or the call path that introduces an effect. |
| Run and test | Execute verified code, detect stale verification, inspect original source locations, and test integrations with controlled inputs. |
| Values and contracts | Browse accepted data types, immutable operations, public functions, effect requirements, and failure contracts. |
| Dependencies | Inspect reviewed operations, adapters, unchecked calls, version changes, and the evidence behind trust. |
| Migration | Find candidate pure regions, compare findings against a baseline, preview safe rewrites, and promote boundaries. |
| Policy and history | Inspect inherited rules, exceptions, owners, expiry, coverage changes, and published verification claims. |

A new developer starts with a calculation function, sees its first violation, applies a functional rewrite, checks it, and runs it. Advanced policy and syntax features do not interrupt this first experience.

Project policy, dependency declarations, baselines, and exception history survive tool restarts and travel with the project. Temporary analysis results are disposable; losing them cannot change a guarantee.

## What Python already permits

### Names and values

Python names refer to objects. Assignment binds or rebinds a name; it does not invoke a setter on that object. Consequently, disabling `__setattr__` cannot prevent local `x = 43` after `x = 42`. The product must reject that rebinding through its checked language rules. [Python execution model](https://docs.python.org/3/reference/executionmodel.html#binding-of-names).

`typing.Final` already expresses a no-reassignment intention to type checkers, but Python does not enforce it at runtime. It also does not make the referenced object's contents immutable. Py à la Mode can recognize this vocabulary without treating it as the complete contract. [Python Final documentation](https://docs.python.org/3/library/typing.html#typing.Final).

### Inline declarations and new syntax

| Authoring form | What it can express | Product position |
| --- | --- | --- |
| Module comment | An external tool can interpret a directive; Python ignores it. | Primary file-level opt-in. |
| Function decorator | A declaration in valid Python syntax at a real function boundary. | Primary small adoption boundary. |
| Type annotation | A contract for a checker, without changing assignment semantics. | Public types and callable contracts. |
| `with` block | A runtime context boundary using valid Python syntax. | Useful for resources; insufficient by itself for lexical `val` semantics. |
| String containing a DSL | A separate language embedded as data. | Poor fit for normal Python editing and debugging. |
| AST or source transformation | A tool can inspect and transform accepted Python syntax. | Optional mechanism, rather than a requirement of the compatible edition. |
| `val x = 42` | Grammar ordinary Python does not accept. | Separate syntax edition requiring translation before normal Python execution. |

Python's tokenizer exposes comments, its syntax-tree facilities support inspection and transformation, and its import system supports custom loading. These provide possible extension points; they do not give an ordinary library permission to introduce arbitrary grammar. The tokenizer is documented for syntactically valid Python, so it should not be assumed to be a general parser for a new dialect. [Python tokenizer](https://docs.python.org/3/library/tokenize.html), [Python AST facilities](https://docs.python.org/3/library/ast.html), [Python import system](https://docs.python.org/3/reference/import.html).

Python has a syntactic-macro proposal, PEP 638, whose published status is Draft. The product must work independently of that proposal being adopted. [PEP 638](https://peps.python.org/pep-0638/).

### Records and collections

Python supplies tuple-like records and frozen data classes. Frozen data classes reject normal field assignment, but their contents are not automatically transitively immutable. Their documentation describes frozen instances as emulating immutability. These are useful adoption surfaces, subject to checking fields and behavior. [Python data classes](https://docs.python.org/3/library/dataclasses.html#frozen-instances).

Read-only interfaces also need care. A mapping proxy reflects changes to its backing mapping, so it is a view of changing state rather than a stable functional value. [Python mapping proxies](https://docs.python.org/3/library/types.html#types.MappingProxyType).

Persistent collections already exist in the Python ecosystem. The `immutables` project supplies a mapping with operations returning new mappings; Pyrsistent supplies vectors, maps, sets, records, and conversion facilities. This makes reuse a credible option. The product still needs its own rules for nested data, aliases, callback effects, and trusted operations; selecting an implementation is subsequent engineering work. [immutables project](https://github.com/MagicStack/immutables), [Pyrsistent documentation](https://pyrsistent.readthedocs.io/en/latest/intro.html).

## Mode boundaries and verification claims

### Opting in

The proposed module directive is:

```python
# mode: fun
```

It appears in the module header. A project or package can also require the mode through policy. A misplaced directive produces an error; it cannot silently change semantics halfway through a function.

In a mixed Python module, the proposed function declaration is:

```python
from pyalamode import fun

@fun
def discounted_price(price: int, discount: int) -> int:
    net = price - discount
    return net
```

All names and commands in examples describe the proposed product vocabulary, not an existing implementation.

Module opt-in covers functions and supported initialization in that module. Function opt-in covers the callable, its defaults, captured values, and dependencies; it does not certify the surrounding module. An effect declaration opts a callable into checked effectful mode when used in a mixed module.

Ordinary code remains ordinary outside these boundaries. Crossing a boundary is explicit and checked according to the receiving contract.

### Enforcement modes

- **Off:** Ordinary Python execution with no functional claim.
- **Audit:** Reports obstacles to adoption while retaining ordinary runtime behavior. Findings can be baselined.
- **Strict:** Unsupported or violating code fails verification and blocks supported execution or publication as verified code.

Audit debt and diagnostic suppressions never turn an invalid strict function into a verified pure function.

### Separate purity from evidence

A function has a behavioral contract and an evidence status. These are separate dimensions.

| Evidence status | Meaning |
| --- | --- |
| Checked | The supported source and its dependencies satisfy the checker rules. |
| Trusted | A specific external operation relies on an approved declaration or runtime implementation. |
| Unsafe | The behavior is insufficiently characterized and requires an explicit unsafe boundary. |
| Unchecked | The code lies outside the participating boundary. |

A callable can be pure according to a trusted declaration, but the product must show that external trust. A wrapper does not improve evidence automatically: it is checked only to the extent that its implementation, conversions, and dependencies are checked.

### Execution contract

Strict verification is a blocking build and execution contract, rather than a style preference. A developer must be able to require it in local commands, tests, automation, and packaging.

Supported execution checks the current source, active edition, policy, and relevant dependency contracts before the strict boundary executes. Changed or missing evidence requires rechecking or causes refusal. Invalid strict initialization must be rejected before it performs its prohibited effects.

A Python interpreter ignores a comment marker. Executing raw source through an unmanaged `python` command carries no certification. The product clearly distinguishes this case from supported execution. Where its runtime entry points are used, they refuse unsupported or stale contracts and validate values received from ordinary Python.

These checks protect supported program behavior. They do not establish isolation from hostile native code, deliberate reflection, artifact tampering, or monkey-patching of the execution environment. The runtime and approved external contracts are a visible part of the trust boundary.

## Binding rules

### Assignment is val by default

Within a strict scope, ordinary assignment introduces a binding:

```python
x = 42
y = x + 1
```

The following fails:

```python
x = 42
x = 43
```

Parameters are already bound. Augmented assignment, deletion, `global`, and `nonlocal` writes fail. Imports, function declarations, pattern captures, and other name-binding forms also participate; the rule cannot be bypassed by choosing another spelling of a write.

A name may be initialized on mutually exclusive paths if each continuing path reaches its first assignment exactly once:

```python
if member:
    fee = 0
else:
    fee = 10
return fee
```

If a continuing path reaches `return fee` without initialization, or reaches a second assignment to `fee`, checking fails. Earlier returns are accounted for. Reusing a name in a distinct nested function scope is allowed; changing a captured binding is not.

Assignments to fields and collection elements are value mutation, not a new binding, and fail separately. Destructuring creates bindings only for immutable received values. Starred unpacking that would introduce a mutable Python list is rejected in the compatible edition.

### Iteration and scope

The first usable release favors expressions, recursion, eager transformations, folds, and comprehensions consumed immediately into approved immutable results. Ordinary statement loops that repeatedly bind the same name are excluded from that initial strict subset.

The XL product supports checked iteration with an explicit per-iteration rule: loop targets and body-local names cannot be manually rebound, accessed as accumulated state, or used after the loop. They cannot reuse an already bound surrounding name. A closure capturing a changing loop binding cannot escape that iteration; developers use a checked function factory with explicit arguments when a snapshot is needed.

This is a restriction on accepted Python, not an assertion that Python loops acquire new lexical scopes. Python loop targets persist after iteration, and closures must be checked against the actual binding behavior. [Python for statements](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement).

Pattern captures cannot overwrite existing bindings and are usable only on paths that establish them. Exception targets remain local to the handler in accepted strict code; escaping exception objects, traceback state, or closures over a cleared target is rejected or requires an effectful adapter. Assignment expressions are excluded from strict source initially.

## Immutable values and alias safety

### Admitted values

Pure code accepts known immutable scalars, recursively immutable tuples, approved immutable collections, checked records and alternatives, and callables with verified or visibly trusted contracts and stable captures.

Built-in immutable values are accepted through their known behavior. An arbitrary subclass does not inherit that evidence automatically because it can override operations. Merely having a hash, a `Final` annotation, a `Sequence` interface, or a `Mapping` interface is insufficient.

Every value is understood as one of:

- **Stable data:** Its reachable data and observable operations satisfy the immutable contract.
- **Confined construction state:** A temporary builder admitted only under ownership rules.
- **Effect capability:** An opaque handle whose operations explicitly require effects.
- **Foreign or unknown data:** It must be adapted, validated, or handled in an unsafe region before being treated as stable data.

Capabilities and builders are not ordinary immutable data. A frozen holder containing a database connection does not qualify as a pure record.

### Deep immutability

An immutable outer structure does not make its members immutable:

```python
payload = ([],)  # rejected: the tuple contains a mutable list
```

The checker identifies the nested path, not just the outer type. It checks closure captures, record defaults, custom properties, and behavior exposed by a value as well as obvious fields.

No cast, annotation, alias, or suppression can turn foreign data into checked stable data. Public strict entry points validate supported incoming values from ordinary Python before executing the body. Mutable or unrecognized data fails, or crosses a separately declared conversion boundary.

### Conversion and snapshots

Converting foreign mutable data creates an independent immutable snapshot. Mutating the original later must not change that snapshot. A shallow wrapper or read-only view does not satisfy this requirement.

Snapshotting is itself an operation on potentially changing state. Its effect and evidence depend on the source: reading a mutable object, invoking its iterator, or accessing a custom property cannot be universally labeled pure. Those operations belong in a checked effectful or visibly trusted adapter.

Conversion handles supported nested values and shared references without retaining mutable aliases. Cyclic foreign graphs fail with an explanatory path in the initial product; developers model cycles through immutable identifiers or supply a reviewed domain adapter. Arbitrary objects are never frozen merely by disabling their setters.

Concurrent changes to a source require an adapter that provides a consistent snapshot or an explicit failure. Ordinary copying does not promise an atomic snapshot of shared state.

Converting back to mutable Python data produces independent mutable values at an integration boundary. Changes to them do not affect the strict input. Mutable values cannot flow back into pure code without another checked conversion.

## Immutable collections

The full product supplies sequence, map, and set values with persistent updates. A persistent update returns a new logical collection while leaving earlier versions unchanged; it should avoid copying the entire collection for each small update where the collection's documented behavior permits sharing.

The developer can:

- Construct collections from stable data and checked transformations.
- Read, index, slice, iterate, match, and compare values using documented value semantics.
- Add, replace, remove, concatenate, union, intersect, map, filter, fold, group, and traverse.
- Update a nested path with a new value and retain the original graph.
- Distinguish ordered collections from collections without an ordering promise.

Proposed examples:

```python
from pyalamode import seq, mapping

prices = seq(10, 20, 30)
revised_prices = prices.set(1, 25)
total = revised_prices.fold(0, lambda subtotal, price: subtotal + price)

customer = mapping(name="Ada", points=10)
revised_customer = customer.set("points", 11)
```

An apparent mutator name is not categorically forbidden: the actual operation contract decides whether it returns a new value or changes its receiver. Ignoring a returned update produces useful feedback when the operation is known to have no other purpose.

The compatible edition rejects mutable list, dictionary, and set values in pure code, including mutable comprehensions and mutable constructors. It offers explicit immutable construction and safe rewrites. Python literal types, indexing, and calling behavior remain unchanged for accepted code.

Eager collection transformations are the default. A consumable iterator has changing cursor state; it is not silently treated as a reusable immutable collection. Private iterator machinery can be confined to an approved construction or terminal operation. The XL product also offers reusable transformation recipes with checked captures and callbacks; consumption timing and effects remain visible.

Operations that rely on ordering require ordered inputs or an explicit ordering step. Purity does not imply that an unordered collection gains reproducible ordering across processes.

## Records and domain modeling

### Immutable records

The proposed record declaration is:

```python
from pyalamode import record, seq, ImmutableSeq

@record
class Customer:
    name: str
    tags: ImmutableSeq[str]

customer = Customer("Ada", seq("member"))
revised_customer = customer.with_(name="Grace")
```

A record has a fixed field set and stable field values. It supports construction, value comparison, field access, destructuring, pattern matching, and copy with changes. It is hashable when its value components and comparison contract support hashing.

Constructors, defaults, validation, methods, and computed properties obey the same effect rules as functions. Mutable inheritance, dynamic attributes, unreviewed descriptors, and custom hooks cannot smuggle changing state into a record. Identity comparisons and identity-derived values cannot substitute for domain equality in pure code.

Existing frozen data classes and named tuples can be recognized when their complete contracts qualify. The developer need not rewrite an already suitable domain model solely to use a different decorator.

### Alternatives and expected failure

The full product supports closed alternatives, optional values, success or failure results, and validation that can accumulate independent errors. Variant values are deeply immutable.

A developer can match a closed alternative exhaustively. Adding a case causes incomplete consumers to fail checking. Guards do not falsely count as covering a whole case, and an unrestricted external Python class hierarchy is not advertised as a closed set.

Expected absence and domain rejection use explicit values. This remains a practical Python product: recursion, eager evaluation, named bindings, and straightforward branching are welcome; pervasive currying or point-free style is not required.

## Purity and effects

### Pure computation

A pure function computes from explicit stable inputs and checked constants. It can allocate immutable outputs, call checked pure operations, branch, recur, and produce a deterministic result or supported failure for those inputs.

It cannot read a changing global, mutable closure cell, ambient configuration, clock, unseeded random source, locale, implicit numerical context, file, network, or process state. Even reading mutable state without modifying it violates this contract.

Free values in a strict function inside an ordinary module are especially important: an integer object can be immutable while its global binding is reassigned elsewhere. Such a global is not accepted as a stable constant merely because its current value is an integer. Pass it as an argument or establish it through a checked constant boundary.

Purity is independent of totality. A function can be pure and still fail or never terminate. The product reports modeled failure separately and makes no claim to prove termination, resource sufficiency, numerical correctness, or equivalence across different Python runtimes.

### Effects are explicit permissions

Initial effect families cover input/output, state observation and change, time, randomness, environment and process interaction, task coordination, and unsafe execution. Projects can inspect and restrict them without inventing a new annotation for every operation.

The proposed declaration is:

```python
from pyalamode import effects, IO, Clock

@effects(IO, Clock)
def report(prices: tuple[int, ...], clock, output):
    total = sum(prices)
    instant = clock.now()
    output.write(total, instant)
```

An effect declaration is a checked upper bound on behavior. It is not a waiver for unknown calls. Capabilities identify where the effect comes from and can be passed explicitly to integration code. Pure functions cannot operate on stateful handles, even when their holders are frozen.

Effectful strict functions retain the binding and ordinary-data immutability rules. State changes happen through declared capability operations, rather than unrestricted field assignment to arbitrary domain values.

An effectful caller can call pure functions. A pure caller cannot call an effectful function and suppress the evidence. Handling a failure does not erase I/O or state changes already performed.

### Higher-order functions and hidden calls

An operation that receives a callback carries the callback's effects. A transformation with a pure callback can be pure; the same transformation with a callback that logs requires output permission. Effects cannot disappear through lambdas, partial application, decorators, callable objects, protocols, or aliases.

Checking includes implicit calls: operators, truth testing, iteration, comparison, hashing, formatting, property access, context-manager entry and exit, and matching operations. For example, `a + b` is only as pure as the admitted operation for those values. A custom `__add__` that writes a file is not pure arithmetic.

Dynamic dispatch is allowed when every admitted implementation satisfies the contract. Unknown dispatch fails closed. Recursion and mutually recursive functions retain their inferred or declared effects.

### Failures

Failure behavior is a separate contract dimension. Known recoverable exceptions can be declared and handled; `Result` values provide a clearer default for expected domain failures. A project can require value-based failure on selected public APIs.

Exception handling does not grant access to mutable exception internals or ambient traceback state from pure code. Such inspection requires a characterized adapter. Exhaustive result matching is available without implying exhaustive knowledge of every Python exception.

The tool does not claim to eliminate memory exhaustion, interpreter interruption, or every possible runtime failure. A pure label is never presented as a promise that the function always returns successfully.

### Imports and definition time

Module initialization, callable invocation, and delayed execution have distinct contracts. A pure callable in an external package can still come from a package whose import performs effects. Reports show that initialization evidence separately.

Supported strict execution checks module bodies, defaults, decorator evaluation, class bodies, and supported annotation behavior. A decorator alone cannot retroactively prevent effects that occurred while Python was defining the function: decorator expressions and parameter defaults are evaluated during definition. The product therefore requires checking before relevant strict initialization, rather than claiming that a runtime wrapper is sufficient. [Python function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).

Runtime contract discovery cannot execute arbitrary annotations or user hooks merely to establish safety. Unsupported definition-time behavior fails closed or remains at an explicit integration boundary.

## Interoperability with ordinary Python

### Narrow boundaries

Ordinary Python callers can pass supported stable values to exported strict functions. Boundary validation catches wrong types, nested mutability, and unrecognized callables before the body starts. Ordinary code does not receive a blanket functional certificate by calling one strict function.

Foreign operations are approved individually. A standard-library package is not wholly pure because one function is; a native extension is not safe because its signature is annotated.

An adapter specifies inputs, outputs, conversion behavior, effects, failure, and the evidence it relies on. It can separate an effectful fetch from the subsequent pure transformation of an immutable snapshot. If an operation retains a mutable alias, invokes an uncontrolled callback, or returns a stateful view, that behavior remains visible.

### Unsafe behavior

An unsafe region is bounded, carries a reason, and remains discoverable in reports. It propagates an unsafe requirement to callers. It cannot certify its returned data as immutable without a separately qualified conversion.

The product supplies no generic `trust_me_pure` or cast that erases unknown effects. A maintainer can approve an external contract, but the result remains visibly dependent on trust. Diagnostic suppression cannot promote that evidence to checked.

### Unsupported dynamic behavior

Unchecked `eval` or `exec`, runtime code generation, arbitrary reflection, monkey-patching, mutable metaclass behavior, writes through object hooks, and uncharacterized native calls are rejected within checked source or assigned to an unsafe boundary.

Dynamic imports and runtime replacement of verified dependencies require compatible evidence before they participate. Mutable global caches, implicit random state, and ambient numerical settings are not accepted by convention. Hidden implementation caches are permitted only in a visibly trusted implementation whose cache state is unobservable under the supported contract.

## Ownership and efficient construction

The XL product permits private mutation when no caller or alias can observe it. This is a controlled construction feature, not a general permission to mutate strict values.

A transient builder starts with fresh state or a qualified immutable input. The checker prevents escape through returns, records, closures, globals, callbacks, unknown code, or concurrently running tasks. Finalization yields stable data and invalidates all usable builder aliases. Using a finalized builder fails.

Ownership transfer cannot be asserted for arbitrary foreign Python objects when aliases may still exist. Such data requires a snapshot or a reviewed ownership boundary. A failed construction cannot leak a partially mutable result.

Developers see documented cost behavior for persistent updates, bulk construction, and nested changes. Representative examples demonstrate that updating many values does not automatically require copying an entire graph for every edit. Claims include conversion costs and retention of prior versions.

The product prioritizes stable semantics over a promise of zero overhead. Performance exceptions must remain visible boundaries; disabling checks is not represented as retaining the same guarantee.

## Testing and concurrency

Pure tests use explicit immutable inputs and expected outputs. Integration tests supply controlled capabilities for clocks, randomness, services, and state; they do not rely on global monkey-patching to establish purity.

A deterministic test provider helps reproduce outcomes, but its function still has the effect contract of the capability it uses. Passing a timestamp as data removes the clock effect from a calculation; substituting a fake clock does not change that calculation's declared capabilities automatically.

Immutable messages and snapshots can cross task boundaries without data mutation. Creating tasks, scheduling, cancellation, queues, and shared services remain explicit effects. Capturing a builder or foreign mutable object in a task fails.

Controlled scheduling supports repeatable tests where the supported scheduler can make that promise. The product does not claim that arbitrary threads or external networks become deterministic. Automatic parallel execution is outside this scope.

## Diagnostics and editor behavior

Every diagnostic has a stable identity, a primary source location, the active boundary, a concise explanation, and relevant origin locations. The explanation can trace nested data or a chain of calls instead of showing only the final failing expression.

Examples:

```text
PAL101: `count` is already bound
  introduced at totals.py:8
  assigned again at totals.py:11
  derive a new binding or express accumulation as a fold
```

```text
PAL221: `Customer.tags[0]` contains mutable data
  received from unchecked `load_customer`
  create an independent immutable snapshot at the integration boundary
```

```text
PAL310: `quote` observes the clock
  quote -> campaign -> clock.now
  pass the relevant time as data, or declare the Clock effect
```

```text
PAL340: the implementation of `value.__str__` is unknown
  formatting this value may execute unchecked behavior
  use an admitted immutable value or a reviewed formatting adapter
```

Editor actions show the consequences of changing a contract. Adding an effect displays affected callers; choosing a trusted contract displays the new trust assumption. Quick fixes never silently broaden permissions, suppress a strict failure, or change a public return type.

Tracebacks, navigation, coverage, and debugger stops refer to authored source. Diagnostics from source translation carry the same rule identities as the compatible edition. An explain view can answer both “why did this fail?” and “what evidence makes this pass?”

## Migration and team policy

### Migration workflow

Audit mode inventories mutation, changing inputs, implicit effects, unsupported operations, and dependency uncertainty without changing execution. It identifies useful pure regions and their blockers rather than treating a clean-looking syntax fragment as proven safe.

The developer saves a baseline, selects a boundary, previews necessary conversions, and promotes it only after strict checking passes. Bulk rewrites are previewed, reversible, and preserve the intended runtime behavior; uncertain changes are suggestions.

Baselines use stable finding identities rather than raw line numbers. Moving existing debt cannot conceal new debt. Deleting a strict boundary, changing its edition, introducing unsafe code, or adding trusted declarations appears in the change report even when the error count decreases.

### Maintainer policy

A project can require strict boundaries, public type and effect contracts, permitted effects at entry points, approved dependency evidence, and limits on unsafe behavior. A file can tighten inherited policy and cannot silently weaken it.

Exceptions identify the rule, exact scope, reason, owner, and optional expiry. The product distinguishes migration debt, an explicit effect allowance, a trust declaration, and an unsafe exception; those choices have different implications.

Policy checks can prevent expanded effects, expired exceptions, newly trusted operations, lost strict coverage, or baseline growth. Public compatibility reports flag changes to effects, failure, accepted input mutability, returned value stability, and closed alternatives, even when the ordinary Python signature remains similar.

History is useful in code review and offline. It does not require sending source code to a hosted service.

## Conceptual information managed

- A **project** has an edition, policy, participating boundaries, and saved migration evidence.
- A **boundary** includes bindings, values, callable contracts, and dependencies on other boundaries.
- A **callable** has input and output requirements, effects, failure behavior, capture requirements, and evidence. Callbacks relate these contracts to higher-order operations.
- A **value contract** describes stable fields or elements, admitted behavior, alternatives, and any construction constraints.
- A **dependency operation** can have reviewed declarations and adapters tied to particular versions. Multiple projects can consume the same contract with different trust policy.
- A **finding** relates a violated rule to its origin and consequence. A baseline records accepted migration findings without certifying them.
- An **exception** has scope, rationale, ownership, and history, and may expire.
- A **verification claim** relates source, edition, policy, dependency evidence, and the guarantees a particular released artifact actually carries.

These relationships support search by function, effect, rule, dependency, owner, and trust status; filtering; bulk migration review; change reports; and history.

## Packaging and compatibility

Developers publish ordinary Python applications and libraries with clear participating entry points and functional-contract evidence. Consumers can distinguish checked logic, trusted operations, effectful integration, and unsafe dependencies.

A verification claim binds to the relevant source or released artifact, edition, policy, checker rules, runtime requirements, and dependency evidence. A contract for one dependency version is not silently applied to another version. Incompatible changes require review or rechecking.

Supported distribution retains source locations and boundary validation. Shipping a generated Python artifact does not make a raw comment executable, nor does it make unchecked callers or hostile code pure.

The product publishes a supported Python-version and execution-environment matrix. Unsupported syntax, runtime behavior, or platforms fail explicitly instead of falling back to weaker guarantees. Public declarations can remain compatible across ordinary annotation tools without assuming that those tools implement functional effects.

## Optional syntax edition

The XL roadmap includes an opt-in dialect once the compatible edition has established the contract. It can make immutable authoring less verbose:

```python
# illustrative dialect source, not ordinary Python
val prices = [10, 20, 30]
val revised = prices.set(1, 25)
```

In that edition, `val` introduces the same binding contract and collection literals produce the edition's immutable values. It uses the same purity, evidence, and effect rules; syntax cannot bypass them.

Dialect source identifies itself before normal Python execution, translates through supported commands, and has formatting, navigation, diagnostics, source mapping, packaging, and edition-aware type feedback. It never relies on users remembering that an ordinary-looking file must be run with a hidden transformation.

Arbitrary comment-delimited regions remain excluded. The smallest stable boundary is a function. A true inline lexical-block form is a separate extension proposal and must define inputs, outputs, capture, scope, and escape behavior before release; a `with` marker is not presented as having those semantics automatically.

The dialect's launch criterion is useful authoring improvements with complete tooling, rather than novelty alone. Projects can remain on the compatible edition indefinitely.

## Acceptance criteria

### Boundaries and enforcement

1. A developer can protect and run a useful arithmetic or decision function in the first release without a cloud account or new Python grammar.
2. Adding a supported module directive or function declaration makes reassignment a blocking error; the error identifies both assignments.
3. The same finding in audit mode leaves ordinary execution unchanged and is not displayed as a strict guarantee.
4. A strict function fails before its body runs when an ordinary caller supplies unsupported mutable data.
5. Supported execution rejects stale evidence and invalid strict initialization before that initialization performs the prohibited operation.
6. An unmanaged raw-source run is visibly outside certification; the documentation and run commands do not imply that Python enforces comment markers.

### Bindings and values

7. Mutually exclusive first assignments pass when every continuing path defines the name; a second assignment or missing assignment fails.
8. Parameters, imports, destructuring, captures, and alternate binding forms cannot bypass the rule.
9. A tuple or frozen record containing a nested mutable value fails with the nested path.
10. A read-only view of mutable foreign state is rejected as stable data.
11. A converted snapshot remains unchanged after the original nested source is mutated.
12. Unsupported cycles or inconsistent snapshot sources produce an explicit conversion failure rather than a false immutable label.
13. Collection and record updates return new values while earlier values remain observably unchanged.
14. A closure cannot leak a changing loop binding; a function factory receiving the value explicitly can produce a stable capture.

### Purity and effects

15. Reading time, randomness, changing global data, or ambient process state from pure code fails even through multiple calls.
16. The explain view identifies the originating effect and the path to the pure caller.
17. An effect declaration permits characterized effects but still rejects an unknown operation.
18. An effectful callback propagates effects through a higher-order operation.
19. A custom operator, property, formatter, matcher, or iterator with effects cannot pass as a pure implicit operation.
20. Handling a failure does not erase other effects; purity is not confused with totality.
21. Default and decorator evaluation cannot perform unchecked effects during supported strict initialization.
22. A pure operation from a package with effectful import initialization displays both contracts accurately.

### Interoperability and evidence

23. A reviewed contract applies to a specific operation and dependency version, not an entire package by association.
24. Every external trust assumption and unsafe region is visible in reports and in released claims.
25. An adapter that retains a mutable alias fails to return certified stable data.
26. A cast or diagnostic suppression cannot promote unknown behavior to checked purity.
27. The consumer of a published library can inspect effects, stable-value requirements, failure, and evidence before using a strict entry point.

### Full product workflows

28. Adding a closed alternative breaks incomplete consumers with a useful exhaustiveness diagnostic.
29. A transient cannot escape or be used after finalization through any supported alias.
30. Task creation rejects a captured mutable builder and preserves explicit scheduling and external effects.
31. Migration reports detect added debt and lost strict coverage even when source lines move.
32. A maintainer can prevent policy weakening, expanded unsafe use, and expired exceptions through the same local and automated checks.
33. Editor feedback, execution failures, and translated-source diagnostics point to authored locations.
34. Equivalent supported operations in the compatible and syntax editions carry equivalent functional contracts and results.
35. A developer can move one function into strict mode while unrelated ordinary Python remains usable through declared boundaries.

## XL roadmap

### Milestone 1 Strict functions and modules

A developer protects useful scalar and recursively immutable tuple calculations with module or function opt-in, immutable bindings, checked constants, a small characterized pure-operation surface, source-linked diagnostics, boundary validation, and supported check and run workflows. Unknown behavior fails closed. Audit feedback can explain violations without certification.

**Observable completion:** Reassignment and ambient reads fail; a compliant price calculation runs; a mutable argument is refused before invocation. This milestone works independently of every later feature.

### Milestone 2 Immutable collections

Developers construct immutable sequences, maps, and sets; use persistent updates and eager map, filter, and fold operations; inspect nested mutability; and convert supported foreign data at a visible boundary. Collection contracts state ordering and failure behavior.

**Observable completion:** Derive multiple collection versions, mutate the foreign source of a snapshot, and confirm every earlier strict value remains unchanged.

### Milestone 3 Records and immutable object behavior

Developers declare records, validate fields and defaults, copy with changes, match records, and admit qualifying existing Python record types. Checked methods and properties cannot hide mutation or implicit effects.

**Observable completion:** A nested mutable field fails with its path; a compliant customer record supports matching and immutable revision.

### Milestone 4 Effects and application integration

Applications use checked effectful entry points, explicit capabilities, effect propagation, higher-order contracts, modeled failure, and origin explanations. Strict ordinary data remains immutable in effectful code.

**Observable completion:** A reporting workflow combines a pure calculation with explicit clock and output capabilities; an effectful callback fails when passed into a pure context.

### Milestone 5 Domain alternatives and failure workflows

Developers model closed alternatives, optional values, results, exhaustive matches, and validation that accumulates errors. Projects can specify failure policy without treating every pure computation as total.

**Observable completion:** Adding a domain variant identifies incomplete matches; a validation workflow returns immutable success or error values.

### Milestone 6 Standard Python operation contracts

Developers use a useful reviewed surface for text, numbers, serialization, paths, files, time, randomness, and environment interactions. Contracts cover implicit dispatch and distinguish initialization from invocation.

**Observable completion:** A data-processing command converts external input, performs pure transformation, and writes output with fully visible effects and trust.

### Milestone 7 Third-party adapters and dependency evidence

Integration owners characterize narrow foreign operations, publish reusable adapters, manage version-specific trust, and explain callbacks, retained aliases, and unknown native behavior. Library authors publish equivalent contracts for downstream use.

**Observable completion:** Two representative external integrations expose stable values and accurate effects; changing a dependency invalidates incompatible evidence.

### Milestone 8 Editor explanations and tests

Developers receive live feedback, safe rewrite previews, contract and effect navigation, original-source debugging, and test support with controlled capabilities. Changing a public contract shows consequences for callers.

**Observable completion:** A new Python developer resolves binding, nested mutation, and effect errors from the editor, then runs a deterministic integration test.

### Milestone 9 Existing project migration

Teams inventory an ordinary codebase, select candidate regions, save a stable baseline, preview bulk rewrites, and increase strict coverage one boundary at a time. Reports distinguish eliminated debt from weakened enforcement.

**Observable completion:** Promote one module in an existing application and reject added debt even after files or lines move.

### Milestone 10 Project policy and change history

Maintainers require strict coverage, constrain entry-point effects, govern trust and unsafe exceptions, manage ownership and expiry, and review functional compatibility. Policy inheritance and all weakening are visible.

**Observable completion:** An automated check rejects an expired exception, a new trust assumption, and a file that attempts to relax package policy.

### Milestone 11 Ownership and efficient construction

Developers use confined transient builders, safe per-iteration bindings, reusable transformation recipes, and documented performance guidance. Escape and alias rules preserve the stable-data contract.

**Observable completion:** A bulk transformation produces immutable output; leaking a builder, reusing a finalized alias, or leaking a changing loop capture fails.

### Milestone 12 Concurrent functional workflows

Applications send immutable messages between tasks, use declared scheduling and coordination capabilities, and test supported coordination with controlled scheduling. Shared foreign data remains at explicit boundaries.

**Observable completion:** A multi-task workflow exchanges stable values and exposes cancellation and I/O effects; sharing a transient is rejected.

### Milestone 13 Distribution and ecosystem contracts

Authors package applications and libraries with usable entry points, verification evidence, source locations, a compatibility matrix, and contribution rules for reviewed external contracts. Consumers inspect guarantees and detect incompatible releases.

**Observable completion:** An independently consumed package preserves boundary validation and published effects; altered dependency evidence requires review or rechecking.

### Milestone 14 Optional syntax edition

Developers can choose concise `val` declarations and immutable literal forms in an explicitly identified dialect with complete editing, translation, debugging, packaging, and migration support. The compatible edition remains fully supported.

**Observable completion:** The same representative functional program in both editions has equivalent contracts and behavior, and errors in the dialect point to authored syntax. Arbitrary inline block syntax requires a subsequent, separately specified extension.

## Non-goals

1. **Security isolation from hostile Python or native code.** Functional contracts apply within supported execution and declared trust. A hostile-code sandbox requires a different threat model and execution environment.
2. **Certification of arbitrary dynamic Python.** Unknown behavior is rejected or made visibly unsafe; the checker does not guess and call that proof.
3. **Transparent compatibility with mutable application frameworks and data libraries.** These can remain in ordinary Python or receive reviewed adapters. Their identity and mutation semantics cannot simply be relabeled functional.
4. **A new general-purpose language or mandatory syntax migration.** The compatible edition is a durable product. The dialect adds authoring conveniences without requiring replacement of the Python ecosystem.
5. **Automatic parallelization, pervasive laziness, or proof of termination.** Those are separate execution or verification commitments. Purity and immutable data do not establish them automatically.
6. **Automatic elimination of domain bugs or runtime failure.** Functional checking complements tests and validation; it does not prove numerical correctness, resource sufficiency, or business requirements.
7. **Arbitrary mid-function comment toggles.** They do not supply lexical scope or reliable escape rules. Functions and modules provide the initial boundaries.
8. **A required hosted dashboard, account system, or organization service.** Editor and local reports provide the complete initial experience, policy, and history.

## Assumptions and resolved ambiguities

- **Enforcement means a blocking contract.** The rejected interpretation is advisory lint that can be bypassed while retaining the same verified label.
- **Practical functional programming means stable data, explicit effects, and composition.** The rejected interpretation is recreating Haskell evaluation and inference wholesale.
- **Compatible Python semantics are valuable.** The initial edition rejects mutable literals rather than silently transforming their types. A dialect can change literal semantics openly.
- **Ordinary assignment is val inside strict code.** A new keyword adds readability rather than the core safety guarantee and belongs in the optional edition.
- **Functions are the smallest initial adoption unit.** Arbitrary inline comment blocks are deferred because their scope and escape behavior remain underspecified.
- **Deep stability includes observation and aliases.** Setter restrictions, frozen outer shells, and read-only interfaces alone are insufficient.
- **Type information is necessary where behavior depends on dispatch.** Local inference is useful; public boundary annotations and characterized protocols are preferable to guessing. `Any` or an unresolved callable does not count as evidence.
- **External contracts are unavoidable and must remain visible.** Runtime primitives, native implementations, and foreign packages are trusted to explicitly characterized extents rather than included in a universal proof claim.
- **Ordinary Python remains available for integration.** Its use must have visible boundaries; forcing a whole application into pure code is not required.
- **The XL scope is an ambition, not the first release.** Fourteen increments cover a complete product; milestone 1 supplies a useful enforceable subset on its own.

## Product success measures

The following are targets for validation, not established results:

- A Python developer can protect a useful pure function within fifteen minutes of starting the quick guide.
- Most introductory binding, mutable-value, and effect violations can be resolved from the diagnostic and its rewrite example.
- A team can adopt one strict boundary without converting unrelated application code.
- Every claim of purity shows its scope and external evidence; every unsafe escape is discoverable.
- The regression suite includes indirect mutation, mutable aliases, changing global bindings, implicit dispatch, callback effects, initialization effects, and stale dependency contracts.
- Representative transformation workloads have published cost behavior, including conversion and retained-version costs, so adoption decisions use measured tradeoffs.
- Library consumers can inspect and enforce the same public contract that the author published.
- Migration and change reports detect lost coverage and added trust, rather than rewarding only a lower diagnostic count.

## Questions to validate before later releases

These questions refine later capabilities without blocking the initial product:

1. Which immutable construction vocabulary is easiest for Python users to learn, and which update names prevent accidentally ignoring returned values?
2. Which effect distinctions help users reason about real applications without making public declarations unwieldy?
3. Which standard and third-party integrations make one strict module valuable in the target users' existing applications?
4. How much loop support is useful once eager transformations and ownership-safe builders are available?
5. Does the syntax edition improve daily readability enough to justify its tooling and migration cost?
6. What specific inline-block workflow cannot be expressed clearly with a local strict function, and what scope and escape contract would that workflow need?
