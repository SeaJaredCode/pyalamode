# Pyalamode XL Product Specification

**Status:** Proposed product contract. **Scope:** XL, with 14 shippable milestones. **Date:** October 8, 2026.

Pyalamode is an opt-in functional mode for Python. It lets developers keep ordinary Python for application orchestration while putting business rules, transformations, and other computations inside regions where bindings cannot be reassigned, values cannot be observably mutated, and effects cannot occur implicitly. Its central promise is that a successful verification means something stronger than adherence to a coding style.

The product starts as a restricted subset of ordinary Python with a checker, checked execution, and immutable value tools. The complete XL product adds records and variants, persistent collections, explicit effects, interoperability contracts, editor support, migration reports, package verification, and an optional syntax extension. These are developer-facing capabilities; a hosted service or web application is unnecessary.

## Product purpose

Python makes useful functional patterns possible, but a team currently has to preserve them through convention. A function may look pure while reading mutable configuration, invoking a callback that writes to a database, or receiving a supposedly frozen record containing a mutable list. Pyalamode makes those dependencies visible and rejects the ones the developer has not explicitly authorized.

The primary use case is a functional core inside an existing Python application. A developer should be able to adopt one calculation first and gradually expand the verified portion of the project. A fully functional module is a supported destination, rather than a prerequisite for getting started.

The product must help users write useful programs within its rules. Prohibiting assignment without supplying immutable updates, folds, error values, and practical boundaries would produce a restriction tool rather than a programming mode.

## People and user stories

The main personas are the application developer writing computations, the reviewer maintaining project guarantees, the integration maintainer exposing existing Python libraries, and the package author publishing reusable functional code. These are responsibilities in the developer workflow, not new account types.

1. **As an application developer,** I can mark one function as functional and receive an explanation of every reassignment, mutable dependency, or hidden effect that prevents it from passing.
2. **As a developer maintaining business rules,** I can express updates to collections and records as new values, confident that earlier values and nested contents remain unchanged.
3. **As a developer integrating legacy code,** I can convert ordinary Python data at a named boundary and see what was copied, rejected, or accepted under a trusted contract.
4. **As a reviewer,** I can see why a function is verified, which dependencies it relies on, and whether a change introduces an effect or additional trust.
5. **As an integration maintainer,** I can describe a library operation's inputs, outputs, effects, and ownership requirements without declaring an entire package pure.
6. **As a package author,** I can distribute functions whose guarantees are checked against the actual package and dependency versions used by consumers.

## The guarantee

Four concepts must remain distinct throughout the product:

| Concept | What the developer can rely on |
| --- | --- |
| Single-assignment binding | A name receives its value once during its logical lifetime. |
| Deeply immutable value | No observable part of the reachable value can change through an admitted operation or retained mutable alias. |
| Pure computation | Its observable result depends only on explicit immutable inputs and verified immutable dependencies; it performs no observable effects. |
| Explicit effect | Interaction with changing state or the outside world appears in the operation's contract and requires a declared capability. |

A **verified pure function**, when it finishes, returns an admitted immutable value or produces a failure described by its failure contract. Repeating it with equal explicit inputs in the same supported runtime environment produces equivalent observable outcomes. It cannot modify its inputs, shared state, or the outside world through an admitted operation.

This promise is conditional on the published language subset, checked entry points, admitted dependencies, and trusted runtime. It does not include termination, identical floating-point behavior across machines, identical memory use, or resistance to a hostile interpreter. Those conditions are part of the contract, not reasons to turn every unsupported case into a warning.

### Verification states

Every opted-in region has one of three visible states:

- **Verified:** Its source and dependencies satisfy the supported rules, apart from the disclosed core runtime that all programs depend on.
- **Relies on trusted integration:** An explicitly approved external contract supplies a guarantee that Pyalamode has not established from that dependency's implementation. This status propagates to callers.
- **Unverified:** A rule fails, a relevant dependency is unknown, or the construct is unsupported. Strict execution rejects the region.

An effectful operation can be verified against its declared effects, but it must never be presented as pure. Verification and purity are separate pieces of information.

The default strict policy admits verified code and the disclosed core runtime. Trusted external integrations and private mutable builders require explicit project opt-in. Neither option can authorize an unverified region.

Annotations are claims to check. `Any`, an ignored diagnostic, a cast, an unknown callback, or an unrecognized decorator must not turn an unknown operation into a verified one. If the product cannot establish a guarantee, it explains the obstacle and keeps the region unverified.

### Where enforcement applies

The checker rejects invalid code before checked execution. Checked entry points validate ordinary Python inputs before allowing them into the functional core. Immutable value operations and boundary checks supply runtime protection where static knowledge is insufficient.

Running the checker in advisory mode helps migration; it does not confer a guarantee. The checked runner, a verified package entry point, or a required project check is how a developer opts into enforcement. A required project check prevents invalid changes from passing that project's gate; it does not intercept arbitrary Python processes.

Plain Python ignores a comment directive. A user who runs marked source through an unchecked interpreter has bypassed the mode. The product must make the distinction visible in commands, documentation, and reports. It must not claim that installing a package changes all Python execution.

Checking source must not execute that source or import unverified application modules merely to discover their behavior. Imports and module initialization are part of the dependency contract; a pure function exported by a package does not establish that importing the package is effect-free.

## Language profiles and entering the mode

The initial **Python profile** accepts ordinary Python grammar and restricts its permitted behavior. It does not reinterpret Python list or dictionary literals as different collection types. Accepted code retains its ordinary value semantics under the checked environment.

The later **Extended profile** offers explicitly opted-in syntax. It accepts `val` as an explicit single-assignment declaration and `fun:` as an inline region marker, with the same functional rules as the Python profile. Extended source is visibly identified as a dialect, produces inspectable ordinary Python, and requires the product's tools. Both profiles share one semantic contract.

All names and command spellings below describe the proposed user interface; they do not refer to an implemented package.

### A whole module

```python
# mode: fun
from pyalamode import record, Vector

@record
class Line:
    unit_cents: int
    quantity: int

def line_total(line: Line) -> int:
    amount = line.unit_cents * line.quantity
    return amount

def invoice_total(lines: Vector[Line]) -> int:
    amounts = lines.map(line_total)
    return amounts.fold(0, lambda total, amount: total + amount)
```

The directive belongs in the module header, after an optional shebang, encoding declaration, and module docstring, before imports or other statements. It applies to all module definitions and initialization expressions. Function bodies, defaults, record declarations, and dependencies are checked; a header must not provide cover for an effectful top-level expression.

There is no mid-file toggle back to ordinary Python. File-wide functional modules use declared effectful operations for their shell behavior or place the shell in another module.

### A single function in an ordinary module

```python
from pyalamode import fun

@fun
def discounted_total(cents: int, discount_cents: int) -> int:
    discounted = cents - discount_cents
    return max(0, discounted)
```

The declaration covers the whole function, its nested functions, and its dependency and capture contracts. Defaults, annotations, and additional decorators are checked as part of creating and exporting it. Applying a marker to an existing function is not proof of purity.

This is the recommended first adoption path. It gives Python an existing syntactic boundary and avoids ambiguity over where a comment-controlled region ends.

### An inline region in an ordinary function

The XL Python profile supports `with fun:` for a limited inline region. It is a marker recognized by the product, not a context manager that can make arbitrary Python pure at runtime.

```python
def summarize(count: int, label: str) -> str:
    with fun:
        doubled = count * 2
        summary = label + ": " + str(doubled)
    return summary
```

The region ends at the matching dedent. It follows ordinary Python's enclosing scope rules; it does not create a new lexical scope. The checker admits only stable, deeply immutable host inputs and checks their bindings in the enclosing function. Repeated or uncertain writes to those input bindings are rejected. Direct reads of ordinary module globals are not admitted. Closures created in this limited inline region cannot escape into the ordinary host; returning immutable computed values is allowed.

Names first initialized inside the region cannot reuse an existing host binding. Ordinary code after the region can consume its immutable results. Any guarantee about that later code requires its own opt-in; it cannot retroactively alter the value already produced by the region.

When a host function is too dynamic for these conditions, the diagnostic offers extraction into a marked function with explicit parameters. The product does not silently add scopes or capture mutable configuration.

### Explicit declarations in the Extended profile

```text
val amount = line.unit_cents * line.quantity
```

Within functional mode, ordinary `amount = ...` already means single assignment. `val` makes intent visible without adding a second, weaker flavor of value. It is invalid in stock Python and belongs only in the explicitly selected Extended profile.

In that profile, `fun:` is shorthand for the same limited region contract as `with fun:`. It does not introduce different scoping, a mutable `var` escape, or a second purity system.

## Bindings and control flow

Python names do not have general-purpose setters that can be disabled. Pyalamode therefore defines and checks binding rules; object attribute setters are a separate concern. Python's own binding operations include parameters, assignments, imports, loop targets, pattern captures, and several other constructs. [Python execution model](https://docs.python.org/3/reference/executionmodel.html#binding-of-names).

The functional rules apply to every admitted binding form, including function and record names. Parameters are already initialized when a function starts. Reassigning a name to the same value still violates single assignment. Deleting a binding is also prohibited.

The rule is **one initialization on every reachable path that uses the name**, rather than one textual assignment anywhere in a file. Mutually exclusive branches may initialize the same logical binding:

```python
@fun
def magnitude(x: int) -> int:
    if x < 0:
        result = -x
    else:
        result = x
    return result
```

The developer sees an error if one branch omits initialization or a path initializes an already initialized name. A condition reading unknown external state remains invalid even when both branches satisfy the assignment rule.

The complete control-flow contract is:

- Destructuring initializes each target once and rejects repeated names in one target.
- Augmented assignment is rejected, including on an immutable scalar. It is a rebinding operation and can also invoke mutation on other types.
- Ordinary `global` and `nonlocal` declarations are rejected in functional regions. Verified immutable module constants remain available under the dependency rules.
- A nested function may introduce a new parameter with the same spelling as an outer name. Reusing a name inside an `if` or ordinary `with` statement does not create a new scope.
- Comprehension binders are fresh for each iteration and cannot supply an escaping mutable iterator.
- An admitted `for` loop treats its target and body-local bindings as fresh per iteration. Reading them after the loop is rejected, as are loop-carried assignments. Each body must satisfy the ordinary purity rules. Collection folds and explicit state transitions provide accumulation.
- Ordinary `while` loops that depend on changing a binding are unsupported in the pure core. Immutable iteration helpers provide a supported alternative; unbounded recursion remains possible and does not acquire a termination guarantee.
- Pattern captures follow branch initialization rules. Patterns must operate on admitted records and variants, rather than invoke unknown access behavior.
- Assignment expressions are excluded from both profiles in this XL scope. An explicit initialization statement gives the developer the same useful binding without expression-level assignment. The checker reports the unsupported construct precisely.
- Resource context managers and exception handlers are admitted only with checked operation and failure contracts. The inline `fun` marker is not blanket authorization for arbitrary context managers.

The product must explain the logical lifetime of a name whenever ordinary Python would permit rebinding it. It must not rely on regex checks for repeated assignment spellings.

## The value domain

An admitted value is defined by its behavior and reachable contents, not by a convenient annotation. The initial domain consists of exact supported scalar types, deeply immutable tuples and frozen sets, product collections, product records and variants, and verified functions with immutable captures. The supported scalar set starts with `None`, booleans, integers, strings, and bytes; other numeric types enter through explicit supported contracts.

For ordinary data, deep immutability is recursive. A tuple containing a list is not admitted. A record containing an ordinary dictionary is not admitted. A container that exposes no mutator can still be inadmissible if an external alias can change its contents.

Verified function values have a separate code-and-capture contract. They are not ordinary Python function objects that users may inspect or modify. Their approved behavior and captured values must remain stable for the checked run.

Application computations observe values rather than allocation identity. `id`, address-dependent representations, frame inspection, and weak-reference observations are excluded from the pure core. Identity comparisons are admitted only for supported singleton checks such as `value is None`. Function values cannot acquire ordinary object-identity equality or hashing merely because they are admitted as callbacks.

### Converting ordinary Python data

A boundary conversion called `freeze` creates an immutable snapshot of explicitly supported ordinary data. It is used in the ordinary or declared-effect shell before passing data into a pure function.

The conversion contract requires:

- Recursive conversion of supported mutable containers, with a reported mapping from source types to value types. Lists become vectors; dictionaries become maps unless the caller explicitly requests an ordered map.
- No retained mutable alias into the original object graph. Changing a nested original list after conversion cannot affect the snapshot.
- Reuse of already admitted immutable values where safe, without promising identity or a particular amount of copying.
- Rejection of unsupported objects and cycles with a path to the offending value. Repeated acyclic references are allowed; preserving their object identity is unnecessary.
- No execution of arbitrary user-defined properties, iteration methods, conversion hooks, or constructors during generic conversion. Such behavior requires a named integration contract.
- Explicit errors for a read-only view over mutable backing storage, rather than treating read-only access as proof of stability.

Snapshotting a concurrently changing source is not automatically safe. The boundary requires exclusive access, a supported synchronized snapshot operation, or another explicit ownership contract during conversion. If those conditions cannot be satisfied, the product refuses the guarantee. Reading mutable external data and synchronizing access belong to the effect shell.

Ordinary Python can receive a fresh mutable export through a separate `thaw` conversion. Mutating that export does not affect its immutable source. Exporting live aliases into internal storage is prohibited.

### Inputs and returned values

Checked entry points validate inputs at runtime when source analysis cannot establish their actual values. An `int` annotation alone must not admit a user-defined subclass whose arithmetic has effects. Subclasses and custom types need their own supported behavior contract.

There is no automatic conversion of an arbitrary argument just because the callee is marked functional. The caller deliberately snapshots or constructs the required value, and the boundary explains what is required.

Returned values are also checked. A function cannot pass verification and then return a mutable list through an unrecognized helper, an unchecked variant field, or a callback. Nested values obey the same rule as top-level values.

## Collections

The product supplies an immutable collection vocabulary that supports normal application work:

| Value | Developer operations |
| --- | --- |
| Vector | Index, slice, append a value, replace an element, concatenate, map, filter, and fold. |
| Map | Look up a key, associate or remove an entry, transform values, merge, and traverse under an explicit ordering contract. |
| Set | Membership, add or remove a value, union, intersection, difference, and order-independent transforms. |
| Ordered map | Preserve entry order when that order is part of the application value. |
| Tuple | Use fixed-size heterogeneous values and ordinary destructuring. |

Every update returns a new immutable value. Earlier versions and all values reachable from them stay stable. The implementation may share immutable structure between versions, but the user never manages that sharing.

```python
@fun
def extend(values: Vector[int]) -> Vector[int]:
    longer = values.append(42)
    return longer
```

Here `append` returns a vector. Discarding the result of an immutable update is a diagnostic because it commonly reflects an assumption about Python's mutable collection behavior.

Mutable list, dictionary, and set literals are rejected in the pure core. The product suggests an explicit immutable constructor; it does not quietly change the meaning of the literal. A comprehension can feed an approved eager value constructor when its source and callback are verified and its internal iterator cannot escape.

Callbacks to map, filter, sorting, grouping, and folds are checked just like named calls. Merely passing a callback through an immutable collection does not make it pure.

### Ordering and equality

A vector's order is part of its value. An ordered map's entry order is also part of its equality contract. Ordinary maps and sets have order-independent value equality.

To preserve the rule that equal inputs produce equivalent results, an unordered collection cannot expose incidental insertion order or randomized hash order to an order-sensitive computation. Its traversal either uses an explicit supported total order or an operation with a verified order-independent result. A sorting key that leaves ambiguous ties needs a tie-breaking contract. Floating-point reduction does not automatically qualify as order-independent.

Hashing used internally for storage is allowed under the collection contract. Exposing a process-randomized hash as an application result is not classified as a pure operation.

### Performance and construction

Repeated immutable updates must be practical for ordinary workloads. Releases report time and peak memory for repeated append, key updates, nested updates, and retained histories at published data sizes. The product must disclose operations that copy an entire collection or retain substantial old structure.

The XL product includes an optional scoped builder for bulk construction. This is explicitly private construction, with an ownership rule: fresh state, one owner, no retained input alias, no sharing, no captured builder in an escaping callback, and one-way finalization into an immutable result. An attempted escape or use after finalization fails. It cannot expose mutation of an existing functional value.

This feature permits controlled internal mutation when it cannot be observed outside construction. It is opt-in and separately reported; developers can select a source profile that prohibits even this form. Persistent value operations remain the default vocabulary.

Whether the underlying collection machinery is reused or written is an implementation choice. Any candidate must satisfy the deep-value, alias, callback, ordering, and performance contracts. An existing immutable container alone is not sufficient evidence.

## Records and variants

Records give developers a concise way to model application data without mutable object behavior. Fields are typed immutable values, constructors validate them, and updates return a new record.

```python
@record
class Customer:
    name: str
    tags: Vector[str]

@fun
def tag_customer(customer: Customer, tag: str) -> Customer:
    updated_tags = customer.tags.append(tag)
    return customer.replace(tags=updated_tags)
```

The product record contract includes value equality, safe hashing when all fields support it, readable representations, checked defaults, pure field validation, pattern matching, and immutable replacement. A field getter, equality method, hash method, or representation cannot run an unknown effect.

Records are sealed against unverified subclass behavior. Class attributes that affect record behavior are stable dependencies, not a place to hide mutable state. Arbitrary descriptors, metaclasses, custom constructors, setters, and post-construction mutation are not admitted merely because a class carries a marker.

Ordinary frozen dataclasses and named tuples can be accepted through a checked compatibility contract when their complete behavior and contents qualify. Freezing an instance is not sufficient by itself.

The XL value model also includes sealed variants, an optional value, and a result value. These support states such as `Found(value)` and `Missing`, or `Ok(value)` and `Err(error)`, without sentinel conventions or hidden exceptions. Every payload is immutable. Pattern coverage for a sealed variant is checked; adding a case identifies consumers whose handling has become incomplete.

### Value interchange

Developers can encode supported data values and decode them back with their collection, record, and variant contracts validated. Encoding is a pure value transformation; reading or writing the encoded bytes is an effect. Supported encodings define their ordering and numeric limits explicitly. Function values and live capabilities are not portable data payloads.

Decoding cannot execute arbitrary Python constructors or object restoration hooks. A changed record or variant contract produces an explicit validation or compatibility result. Restored values satisfy the same deep-immutability rules as values constructed in code.

## Purity and dependency checking

A function's contract includes everything it can observe or invoke, not just assignments in its body. Calls, captures, defaults, decorators, annotations, operators, attribute access, iteration, matching, and callbacks all participate.

The product must reject or require a supported contract for these cases:

| Dependency or operation | Functional treatment |
| --- | --- |
| Mutable module configuration | Pass an explicit immutable snapshot as input. |
| Closure over a mutable binding or object | Reject the capture; offer explicit parameters or an immutable capture. |
| Unknown callable or dynamic dispatch | Reject unless every possible admitted target satisfies the required contract. |
| Attribute or property getter | Admit a checked record field or verified getter; otherwise behavior is unknown. |
| Arithmetic, comparison, indexing, truth testing, or iteration on a custom type | Check the actual operation contract. Familiar syntax is not evidence of purity. |
| Mutable default argument or default factory | Reject. A safe default must be an immutable value or a checked pure constructor. |
| `eval`, `exec`, reflective writes, namespace mutation, or runtime code replacement | Reject inside verified regions. |
| File access, logging, network calls, clocks, environment reads, or shared random generators | Require a declared effect outside the pure core. |
| Iterator, generator, coroutine, or resource handle | Treat as a stateful or effectful value unless it has a specific supported contract. |

Immutable constants from verified modules are permitted. The approved value or callable used by a checked computation must remain stable throughout that computation. Changing a normal Python module attribute must not silently change a verified dependency; the product preserves the approved dependency or rejects the changed environment and requires rechecking.

Imports cannot be treated as pure solely because a desired exported symbol is pure. Module initialization, dependency versions, and approved exports all need an explicit basis for admission. Unknown imported source does not become verified because it is in the standard library or a popular package.

The checker infers contracts where it has enough information. Exported functions, records, variants, higher-order operations, and integration boundaries expose understandable contracts so consumers and reviewers can see their dependencies. If inference is insufficient, the diagnostic identifies the missing information rather than requesting arbitrary annotation ceremony.

## Effects and application orchestration

Useful programs read files, communicate, and update state. Pyalamode supports an explicit functional core with an ordinary or declared-effect shell. Pure functions consume values supplied by that shell and return new values or descriptions of work to perform.

```python
raw_lines = read_invoice()          # Ordinary Python shell
lines = freeze(raw_lines)           # Explicit snapshot boundary
total = invoice_total(lines)        # Checked pure computation
write_total(total)                  # Ordinary Python shell
```

For applications that want stronger shell contracts, the XL product offers effect declarations such as filesystem reads, filesystem writes, network access, clock reads, environment reads, and logging. An operation may use only its declared effects and the capabilities supplied for them. Calling it propagates the effect requirement to the caller; a pure function cannot conceal the call.

Declared-effect code retains immutable application values and single-assignment bindings. Resource handles and capabilities have explicit lifetimes and permitted operations; they are not ordinary record payloads. Existing unrestricted orchestration can remain outside mode rather than pretending to satisfy these rules.

Constructing an immutable description of an effect can be pure. Executing it requires the appropriate effectful operation. Adding a string such as `"pure"` to an effect description never authorizes execution inside a pure function.

Time and configuration can be ordinary explicit input values. Seeded randomness can be represented as a checked transition that returns both a sample and a new immutable random state. An explicit seed does not authorize access to a shared mutable random generator.

Mock or recorded capabilities support testing and replay. Replay claims specify which inputs and effects were recorded; they do not imply that arbitrary external systems are reproducible.

## Failure and advanced computation

Purity is separate from totality. A pure expression may fail, for example on division by zero. A function's visible contract indicates potential supported failures. Domain failures should be modeled as immutable result values when callers are expected to handle them.

The product does not require proving that every program terminates or that every integer is nonzero. It does require that handling a failure does not smuggle mutable exception instances, traceback frames, or unknown cleanup behavior into the value domain. A supported exception can be converted to a checked immutable error value.

Functional folds, scans, grouping, composition, partial application, immutable state transitions, and recursion make ordinary algorithms possible. Captured arguments in partial applications obey the same immutability rule as other closures. Built-in helpers have published callback and failure contracts.

The XL product supports replayable lazy sequences as a separate value abstraction. They must retain immutable inputs and verified callbacks, produce equivalent results on repeated traversal, and make unbounded consumption visible. A normal Python generator is not automatically replayable.

Running pure computations concurrently is supported through explicit orchestration. Result order and failure handling are defined, and admitted values can be shared safely. The product does not promise that every workload gets faster or automatically gains parallel execution.

Memoization is admissible only under a published observational contract: immutable inputs and outputs, no mutable cached aliases, and no caller-visible cache state inside a pure computation. A function cannot depend on hit counts, eviction, or timing while retaining a pure classification.

## Interoperability and trusted integrations

Interoperability is deliberately explicit and granular. An integration describes one operation or family of operations: accepted values, returned values, effects, potential failures, alias behavior, initialization behavior, and the versions to which that description applies.

An integration may be verified from supported source or accepted as trusted after review. The latter remains visible in every dependent guarantee. Declaring an operation trusted does not make its effects disappear.

Copying mutable arguments can protect inputs from modification, but it does not prove that an external function avoids global state, clocks, files, or hidden callbacks. A wrapper around arbitrary Python cannot become verified pure simply by copying before and after the call.

The first integrations should cover useful, bounded cases: standard data conversion, supported numeric operations, parsing into immutable values, and explicit filesystem or network boundaries. Libraries organized around mutable arrays, tables, sessions, or live views require an ownership or snapshot contract; they are not transparently admitted as immutable values.

Integration maintainers can inspect who uses a contract, record the reason for accepting trust, and see which callers need rechecking when an operation or version changes. Contracts expire or become invalid when their stated version or behavior conditions no longer hold. Local review policy determines whether a project permits trusted integrations at all.

## The developer experience

The product's information architecture has six primary surfaces: source authoring, diagnostics, dependency explanation, value and effect reference, project migration, and project policy. These appear through local commands, editor integrations, and readable reports. They do not require a browser dashboard.

### First use

A developer marks one function, runs a check, sees whether it qualifies, and runs it through a checked entry point. Installation must not require replacing their Python interpreter or converting the whole project. Unsupported language or interpreter versions produce an actionable message before execution.

The first successful example must demonstrate a guarantee, including a rejected reassignment and a rejected inappropriate input. A collection of annotations that lets the same invalid function run unchecked is not an adequate onboarding experience.

### Authoring and diagnostics

Editors show where the mode is active and whether a region is pure, effectful, trusted, or unverified. A developer can inspect inferred value types, effect requirements, captures, and admitted dependencies. The initial command workflow remains usable without an editor integration.

Diagnostics identify the source location, the relevant first binding or boundary, the violated guarantee, and a practical repair. For example:

```text
Binding reassigned: total
  First initialized in the preceding statement.
  Functional bindings have one initialization per logical lifetime.
  Create a new binding or use a fold for accumulation.
```

```text
Mutable input at customer.tags[2]
  A list is reachable inside the supplied record.
  Create an immutable snapshot before calling tag_customer.
```

```text
Hidden effect: filesystem write
  invoice_total -> format_line -> save_debug_output
  A pure function cannot call this operation.
  Return the data to the effect shell or declare an effectful operation.
```

Suggested fixes distinguish between a safe mechanical change and a change in program meaning. Renaming a variable can be automatic when safe. Converting a shared mutable object into a snapshot, choosing a traversal order, or changing failure behavior requires the developer to review the proposed result. Bulk fixes preview their changes before application.

### Local commands

The proposed command vocabulary is:

- `pyalamode check`: Verify selected regions and fail the command when the chosen policy is not satisfied.
- `pyalamode run`: Check before executing a supported program and enforce its boundaries.
- `pyalamode explain`: Show the dependency and effect chain behind a classification or diagnostic.
- `pyalamode report`: Summarize adoption, failures, trust dependencies, and change impact.
- `pyalamode build`: Produce a checked distributable or, for Extended source, inspectable ordinary Python with original-source diagnostics.

Structured output supports editor and project automation integrations. Human-readable output remains the default. Errors in checking, dependency resolution, or verification freshness do not turn into a successful exit or an automatic unchecked run.

### Project adoption and review

A project inventory identifies marked regions, candidates for extraction, mutation sites, effect sites, unknown dependencies, and existing integrations. Search and filters let a developer find a rule, type, effect, dependency, or owner. Findings are grouped by the change that would unblock useful work, rather than only by raw warning count.

Advisory migration can establish a baseline of existing findings. Project policy can require that new marked regions pass, prevent new trust dependencies, and gradually reduce the baseline. A baselined violation remains unverified. The report shows the denominator and scope behind any adoption percentage; checking five easy functions does not mean the project is functionally safe.

A review report answers four questions: what became verified, what lost verification, what effects changed, and what new trust was introduced. Saved reports and contract decisions remain available across restarts. Project teams can keep them with their normal source review history; the product does not require a separate identity or approval system.

### Reusable packages and freshness

Package authors can publish visible function, value, effect, and integration contracts. Consumers verify that those contracts match the installed source or artifact and the relevant dependency versions.

A cached verification is tied to the code, language rules, project policy, and relevant dependency and integration contracts that produced it. Changing any relevant input invalidates it. A package upgrade, monkey-patched dependency, or revised trusted contract cannot retain an old green classification silently.

Consumers can inspect the package's public functional surface and the extent of its trust. A verified export does not imply that every module, import initializer, or application in the distribution has been checked.

## Information the product manages

The core things are a project, its opted-in regions, its value definitions, and its operation contracts. A region references values, operations, and other regions. Those references determine its effects and verification state. A public export is a region or value definition offered to consumers under a stated contract.

An integration connects an external operation and version range to a contract and its review history. A project policy determines which states and effects are permitted at its gates. A verification result records the region, its relevant dependencies, the applicable policy, and the reasons for its classification. A diagnostic connects a failed rule to source locations and the dependency chain that caused it.

A migration baseline records known unresolved findings without changing their classification. Reports compare verification results and baselines over time. Builders and resource capabilities have lifetimes during execution; they are not persistent application data.

These relationships must be inspectable by developers and reviewers. Their storage format and internal organization are implementation choices.

## Product acceptance criteria

The complete XL release must satisfy the following observable criteria. Examples concern the proposed language contract, not an existing implementation.

| Scenario | What a developer observes |
| --- | --- |
| A marked function sets `x = 42`, then `x = 43` | Checking fails at the second assignment and identifies the first. Checked execution does not enter the invalid function. |
| A parameter is reassigned, including with `+=` | It fails the same binding rule as a local name. |
| Two mutually exclusive branches each initialize `result` | The function passes if every path that uses `result` initializes it once and all operations qualify. |
| One branch leaves a used name uninitialized | Checking fails with the missing path identified. |
| `values[0] = item`, `record.field = item`, or a mutating helper is used | Checking fails or identifies the unsatisfied ownership contract. Aliases do not hide the write. |
| A tuple or frozen record contains a mutable nested list | Entry validation rejects it and reports the nested path. |
| An ordinary dictionary is frozen, then its original nested list changes | The immutable snapshot does not change. |
| A read-only view refers to mutable backing storage | It is rejected or explicitly snapshotted under a supported boundary contract. |
| A persistent vector is appended to and a record is replaced | New values contain the changes; previous values and nested contents remain unchanged. |
| The result of an immutable update is ignored | The editor or checker explains that the operation returns a new value. |
| A pure function reads changing global configuration | It fails and suggests an explicit immutable input. A verified immutable constant is permitted. |
| An unknown callback is passed to `map` | Verification fails until its behavior contract is established. An annotation alone does not satisfy this. |
| A custom `__add__`, property, iterator, or comparison performs an effect | The apparently harmless expression does not pass as pure. |
| A builtin is shadowed by a different callable | Admission follows the resolved callable, not its familiar spelling. |
| A helper starts logging or writing a file | Its pure callers lose verification, with the dependency path shown. |
| A declared-effect operation uses an undeclared effect | Checking fails at the call or operation requiring it. |
| An external operation is accepted under a reviewed purity contract | Dependent regions visibly rely on trusted integration; they do not receive the fully verified classification. |
| Two equal maps with different construction histories enter an order-sensitive traversal | Incidental history cannot change a verified result; explicit ordering or an ordered-map value is required. |
| A sealed variant gains a case | Consumers without complete handling are identified. |
| A builder escapes, retains a mutable alias, or is used after finalization | The ownership or lifetime violation is rejected. |
| A normal generator is returned as though it were an immutable sequence | It is rejected; a supported replayable value is required. |
| A pure computation uses `id` or allocation identity to distinguish equal values | It is rejected; a supported singleton check remains permitted. |
| A supported record value is encoded and decoded | Its value and type contract are preserved, and invalid or outdated payloads produce an explicit failure. |
| A marked region uses an ignored diagnostic, a cast, or `Any` to hide an unknown operation | It remains unverified. |
| Extended source containing `val` is built | The generated Python is inspectable, diagnostics point to original source, and its functional guarantees match the Python profile. |
| A relevant dependency, policy, or integration version changes | Existing affected verification is invalidated before reuse. |
| An ordinary interpreter runs a file containing only the comment marker | Documentation and tools describe this as unchecked execution, with no claim that the comment changes Python itself. |
| The checker examines a module with effectful top-level code | Examination does not execute that code. Checked execution rejects or requires a declared initialization boundary. |

Successful checks are reproducible for unchanged supported inputs and environments. Reports distinguish source evidence, runtime boundary validation, and accepted external trust. Performance, unsupported constructs, and compatibility limits are published for each release.

## The 14 milestone roadmap

Each milestone delivers a usable increment. Later milestones expand the admitted language and workflow without weakening the guarantee of already verified code.

| Milestone | Delivered capability | A user can confirm completion by |
| --- | --- | --- |
| 1. Checked scalar functions | Function opt-in, single assignment, exact scalar input validation, a small closed vocabulary of pure operations, branch initialization, useful diagnostics, and checked execution. Unknown behavior is rejected. | Marking and running a useful scalar calculation, then seeing reassignment and an inappropriate input rejected. |
| 2. Functional modules and dependencies | File-wide mode, immutable constants, supported pure initialization, checked function-to-function calls, immutable captures, defaults, and dependency explanations. | Composing a small module and seeing a mutable capture or hidden effect in a helper block its callers. |
| 3. Persistent collection values | Vectors, maps, sets, ordered maps, immutable updates, basic higher-order transforms, callback checking, and published equality and ordering rules. | Retaining an earlier value through several updates and confirming it has not changed. |
| 4. Ordinary Python boundaries | Recursive snapshots, fresh mutable exports, nested diagnostics, boundary input and result validation, and alias and ownership checks for conversion. | Passing legacy data into a functional calculation, mutating the original, and seeing the result's snapshot stay stable. |
| 5. Records and variants | Checked records, immutable replacement, optional and result values, sealed variants, pure validation, and exhaustive pattern handling. | Modeling a real domain state and seeing a nested mutable field or missing variant case rejected. |
| 6. Practical functional algorithms | Richer folds, scans, grouping, composition, partial application, checked failure handling, and supported control flow without loop-carried mutation. | Expressing a collection transformation and a state transition without dropping into unrestricted Python. |
| 7. Explicit effects | Named effect requirements, capabilities, resource lifetimes, effect propagation, value descriptions of work, and test or replay capabilities. | Running an application with a verified core and declared shell, then seeing an undeclared effect rejected. |
| 8. Reviewed external integrations | Operation-level contracts, version conditions, trust classification, integration impact views, and a useful initial set of bounded integrations. | Admitting one existing library operation while keeping its trust or effects visible to callers. |
| 9. Editor authoring and reference | Active-mode indicators, inline diagnostics, inferred contracts, dependency navigation, safe fix previews, and a searchable language and value reference. | Repairing a failed guarantee from the editor and inspecting why the corrected region qualifies. |
| 10. Project migration and review | Project inventory, searchable findings, honest adoption reports, baselines, project policy, bulk fix previews, and change-impact reports. | Adopting another functional region while tracking unresolved work and preventing a new trust dependency under project policy. |
| 11. Verified package distribution | Public contracts, checked exports, installed-artifact and dependency verification, freshness invalidation, and consumer-visible guarantee reports. | Consuming a package and seeing a changed dependency force rechecking before reuse. |
| 12. Larger functional computations | Replayable lazy values, private scoped builders, supported additional numeric contracts, explicit concurrent orchestration, and optional observational memoization. | Processing a larger workload while observing stable earlier values and rejection of builder or iterator escape. |
| 13. Inline regions and optional syntax | Restricted inline regions in ordinary Python, equivalent Extended `fun:` and `val` forms, inspectable generated Python, and original-source diagnostics. | Extracting a pure calculation inline, then expressing the same contract with optional syntax and obtaining equivalent results. |
| 14. Release compatibility and assurance | A published supported-interpreter matrix, cross-platform package workflows, complete language conformance examples, performance and memory reports, upgrade guidance, and a stable guarantee reference. | Reproducing the published acceptance scenarios and identifying the guarantees, costs, and limits of the installed release. |

The early releases deliberately admit less behavior. Missing language support is a visible limitation, never an excuse to accept unchecked code under a pure label. Milestone 1 stands alone; the optional syntax release is not a prerequisite for useful enforcement.

## Non goals

- **A security sandbox for hostile code.** Native extensions, interpreter modification, or deliberately invasive unchecked code require a different isolation product. Pyalamode protects the stated supported workflow and exposes its trust conditions.
- **Automatic purification of arbitrary Python.** Copying every object and suppressing setters cannot establish unknown effects or stable behavior. Unsupported constructs require a different expression or an explicit contract.
- **Proof that every program terminates or succeeds.** The product checks mutation, dependencies, effects, and supported failure contracts. Universal termination and arithmetic proofs would turn it into a different language and proof system.
- **An unrestricted macro system or arbitrary embedded DSLs.** The optional syntax adds a small functional vocabulary. General metaprogramming would greatly expand the semantics that users and verification must trust.
- **Immediate compatibility with every package and interpreter.** Support is published and bounded. Mutable scientific objects, live sessions, and alternative runtimes need dedicated contracts rather than a blanket promise.
- **A hosted team platform or mandatory web UI.** Editor, command, package, and review workflows satisfy the intended users. Accounts, hosted analytics, and centralized administrative roles are outside this product.
- **Automatic parallel speedups or native compilation.** Safer sharing and explicit concurrent orchestration are included. Faster execution for every algorithm or a replacement numerical compiler is not promised.

## Assumptions and decisions

1. **The main goal is enforceable behavior within an adopted workflow.** This proposal rejects the weaker reading of a stylistic linter that reports mutation but lets marked regions execute anyway.
2. **Adoption should be incremental.** An ordinary Python application can contain a functional core. A mandatory functional rewrite of the whole program is not the initial model.
3. **Bindings are single assignment by default inside mode.** Explicit `val` is optional syntax, rather than something required to make each binding safe. Rebinding to another immutable value still fails.
4. **Immutable shared values are useful.** The product prohibits changing or implicitly observed shared state, while permitting verified immutable constants. It does not ban all sharing.
5. **Private construction may be useful in the XL product.** A separately selectable scoped-builder facility allows internal mutation under enforced ownership. Projects seeking no mutation in user source can disable it.
6. **Ordinary Python syntax comes first.** The first functional boundaries are functions and modules. Arbitrary inline regions and new syntax wait until their scope and boundary rules can be enforced.
7. **Trust must remain visible.** Practical interoperability includes reviewed external contracts, but relying on one changes the reported guarantee. Unknown behavior never defaults to purity.
8. **A restricted sound subset is acceptable.** A correct Python program may be rejected because the product cannot establish its behavior. The product owes the developer an explanation and a practical alternative.
9. **The product is local developer tooling.** The XL scope is expressed through language and workflow depth, rather than through unrelated hosted application features.

These choices define the proposed product. Implementation work should not begin by silently substituting a weaker guarantee or widening an exception into a general escape hatch.

## Python feasibility and existing facilities

### What is available without new grammar

Python comments are ignored by its syntax, while its source tokenizer can preserve them. A dedicated tool can therefore recognize a mode comment, but stock Python will not enforce it. Decorators and `with` statements offer existing syntactic boundaries; their presence alone cannot change the rules for assignment or prove a body pure. [Python comments](https://docs.python.org/3/reference/lexical_analysis.html#comments), [Python tokenizer](https://docs.python.org/3/library/tokenize.html), [Python scopes](https://docs.python.org/3/reference/executionmodel.html#resolution-of-names).

**Product conclusion:** use existing grammar for the first release and establish enforceable semantics before adding syntax. A checker is necessary, checked execution and boundaries complete the guarantee, and optional source translation later supplies `val`. These solve different parts of the same product need.

The import system is extensible through finders, loaders, and import hooks. That makes specialized loading feasible, but it does not establish purity or cover every way a script can be executed. It is one possible implementation mechanism rather than a feature on which the product promise rests. [Python import hooks](https://docs.python.org/3/reference/import.html#import-hooks).

### Why Final is insufficient

`Final` tells a type checker that a name should not be reassigned; it does not make the referred-to object immutable. Python's documentation also states that these properties are not checked at runtime. [Typing qualifier specification](https://typing.python.org/en/latest/spec/qualifiers.html#final), [Python Final documentation](https://docs.python.org/3/library/typing.html#typing.Final).

```python
from typing import Final

items: Final = []
items.append(42)  # Final alone does not prohibit this.
```

**Product conclusion:** existing annotations may contribute information, but they do not supply the deep-value, effect, or checked-entry contracts.

### What records already support

Python's frozen dataclasses generate assignment and deletion guards. That is useful record machinery, but it does not recursively freeze field contents or establish that every method and field access is pure. The dataclass documentation describes this as emulated immutability. [Frozen dataclass instances](https://docs.python.org/3/library/dataclasses.html#frozen-instances).

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    values: list[int]

box = Box([])
box.values.append(42)  # The field binding is frozen; the list is mutable.
```

**Product conclusion:** reuse familiar record ergonomics, while checking the reachable value graph and admitted behavior. The required product is stronger than a blanket frozen-class decorator.

### Why read only does not mean stable

Python's `MappingProxyType` is a read-only view that reflects changes to its underlying mapping. It therefore cannot independently supply an immutable snapshot. [MappingProxyType documentation](https://docs.python.org/3/library/types.html#types.MappingProxyType).

Operators and attribute access can also invoke user-defined methods or descriptors. Their familiar syntax does not imply that they are effect-free. [Python special methods](https://docs.python.org/3/reference/datamodel.html#special-method-names), [Python descriptors](https://docs.python.org/3/reference/datamodel.html#invoking-descriptors).

**Product conclusion:** the checker must know the admitted operation and actual value contract. Removing obvious setters or listing a few forbidden method names cannot establish functional behavior.
