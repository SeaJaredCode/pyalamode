# Py à la Mode

**Status:** Product specification  
**Scope:** XL  
**Slug:** `pyalamode`

## Purpose

Py à la Mode is an enforceable functional-programming mode for Python. It lets teams write code that still looks and interoperates like Python while gaining a meaningful contract: bindings do not change, owned values are immutable, pure functions cannot quietly perform effects, and unsafe Python interactions are visible at explicit boundaries. It is for Python developers who want functional safety and composability without moving an entire application or ecosystem to another language.

The product is deliberately a **mode and toolchain**, not a claim that unrestricted Python can be made pure. Code opts into a checked functional subset at project, package, module, or function boundaries. Inside those boundaries, violations stop checking and execution rather than appearing as advisory style warnings. Outside them, ordinary Python remains ordinary Python.

## Product principles

1. **Functional by default inside the boundary.** Assignment introduces a binding; it does not create a mutable slot. Functions are pure unless their permitted effects are declared.
2. **Guarantees must have a visible edge.** Checked code, trusted declarations, effectful code, and unchecked Python must never blur into one another.
3. **Adoption must be gradual.** One function or module can opt in without converting its callers, dependencies, or entire repository.
4. **Python familiarity is an asset.** The first edition uses valid Python syntax wherever it can. Novel syntax must earn its migration and tooling cost by enabling semantics that ordinary Python syntax cannot express clearly.
5. **Immutability is deeper than frozen attributes.** The product distinguishes an immutable binding from an immutable value and rejects a mutable value hidden inside an otherwise frozen record.
6. **Effects are capabilities, not moral failures.** Programs must read files, call services, use clocks, and update durable state. Those operations belong at named boundaries and remain callable from other effectful code.
7. **Diagnostics teach the model.** Every error explains the violated rule, points to the mutation or effect source, and offers a functional rewrite or a deliberate boundary.
8. **Escape hatches are explicit and auditable.** Real Python ecosystems require them, but every escape carries a reason and remains discoverable in reports.

## Personas and roles

- **Functional application developer:** writes domain logic in strict modules and wants fast, local feedback about mutation, impurity, and unsafe calls.
- **Adopting Python developer:** starts with an existing imperative codebase, uses audit mode, and moves selected functions or modules into strict mode over time.
- **Library author:** publishes immutable types and trustworthy purity/effect contracts that strict consumers can use without falling back to unchecked interop.
- **Team maintainer:** sets project policy, approves exceptions, prevents regressions in continuous integration, and tracks adoption and unsafe surface area.
- **Interop maintainer:** wraps ordinary Python or third-party packages behind small, reviewed effectful or unsafe boundaries.
- **Tooling contributor:** extends knowledge about Python and third-party APIs while preserving the meaning of the core guarantees.

## User stories

1. As an application developer, I can mark a module or function as strict functional code and have reassignment, mutation, undeclared effects, and unsafe dynamic behavior rejected before it runs.
2. As a developer, I can use immutable records and familiar collection expressions, transform them without mutation, and pattern-match over domain values.
3. As an adopting team, I can audit an ordinary Python project, establish a baseline, and tighten one boundary at a time without pretending that unchecked code is already safe.
4. As a library author, I can publish machine-checkable contracts describing which public operations are pure, effectful, immutable, or unsafe.
5. As a maintainer, I can see why an effect reaches a function, where unchecked Python enters the program, and whether a change expands the project's functional-risk surface.
6. As a Python user, I can package, test, debug, and deploy checked code with useful source locations and intentional conversions at ordinary-Python boundaries.

## Product shape and information architecture

Py à la Mode presents one coherent tool with six primary areas:

### Check

The everyday experience. A developer checks a file, package, or project and sees errors grouped by binding, value mutability, effects, control flow, and interop. A successful strict check is a claim about the whole declared boundary, not merely a clean lint report.

### Run and test

Checked modules and applications can be run only after their active strict boundaries pass. Test output and tracebacks point to the author's source. Pure tests can assert that a callable remains effect-free; effectful tests can provide controlled capabilities such as a clock or file access.

### Explain

For any diagnostic or function, the developer can inspect a human-readable explanation: the binding's definition and later write, the mutable value's path, the call chain by which an effect arrived, or the boundary that made a value unsafe.

### Migrate

An audit view ranks mutation sites, implicit effects, dynamic features, mutable dependencies, and candidate pure regions. Teams can save a baseline, prevent new violations, and promote individual functions, modules, or packages to strict mode.

### Dependencies and trust

A dependency view distinguishes strict libraries, libraries with reviewed contracts, libraries used through explicit adapters, and wholly unchecked dependencies. Trust decisions have an owner, scope, rationale, and history.

### Policy and reports

Project maintainers can define which boundaries must be strict, which effects are allowed at designated entry points, whether unsafe exceptions require approval, and whether the build may expand its baseline. Reports show adoption, effect surface, unsafe surface, exception age, and changes over time.

## The mode model

### Scope

The canonical module declaration is a top-of-file directive:

```python
# pyalamode: strict
```

Strictness can also be selected for a package or project through project policy. In an otherwise ordinary Python module, a valid-Python decorator marks a function as a strict island:

```python
@pure
def total(prices):
    return sum(prices)
```

Arbitrary comment-delimited or indentation-delimited **blocks are not part of the initial product**. Python blocks do not create ordinary lexical scopes, and invisible mid-function semantic changes would make review and control-flow analysis harder. The smallest adoption boundary is therefore a function; the most common is a module.

### Enforcement levels

- **Off:** ordinary Python behavior; no functional claim.
- **Audit:** ordinary Python behavior continues, but the product reports what would prevent a boundary from becoming strict. Findings can be baselined but are not called guarantees.
- **Strict:** violations are errors. The boundary cannot be run or published as checked code until they are resolved or moved behind an explicit effectful/unsafe boundary.

There is no mode in which warnings are silently treated as proof of purity.

### Binding rule: ordinary assignment is `val`

The first language edition does **not** add `val x = 42`. In strict code:

```python
x = 42
```

introduces an immutable binding. A second assignment, augmented assignment, deletion, `global` write, or `nonlocal` write is an error. Function parameters, pattern variables, exception variables, and comprehension variables are also bindings.

This gives the desired meaning without making files invalid to Python's parser. Diagnostics use the term **binding**, so the difference from an ordinary mutable Python name is explicit.

Control flow follows single-assignment semantics:

- A name may be supplied once by mutually exclusive branches when every continuing path supplies it.
- Pattern and exception bindings are local to their branch.
- A loop target is a fresh per-iteration binding and is not a mutable accumulator or an exported post-loop value.
- Closures may capture immutable values but may not mutate captured state.
- Assignment expressions are rejected in strict code because their rebinding and scope behavior obscure the contract.

Examples:

```python
# allowed: one resulting binding, supplied on both paths
if score >= 90:
    grade = "A"
else:
    grade = "B"

# rejected: rebinding
count = 0
count += 1
```

### Value rule: immutable means transitively immutable

An immutable binding alone is insufficient: `items = []` is a stable name pointing at a mutable object. Strict mode therefore classifies values as:

- **Immutable:** the value and all reachable owned values cannot be changed.
- **Locally owned transient:** mutation is temporarily permitted inside a confined construction operation, but the value cannot escape until frozen.
- **Effectful state:** mutation is intentional and accessible only through an explicitly declared state capability.
- **Foreign/unknown:** no immutability claim is available; the value must be frozen, adapted, or handled behind an unsafe boundary.

The checker reports the full path to hidden mutability, such as `Order.customer.preferences.tags`, rather than merely calling the outer record unsafe.

## Core language experience

### Immutable collections

Inside strict mode, collection literals and comprehensions create immutable collection values with familiar iteration, membership, indexing, slicing, equality, and pattern behavior.

The standard family is conceptually:

- **Sequence:** ordered values with efficient append-like and indexed-update operations that return new sequences.
- **Map:** key/value associations whose add, replace, and remove operations return new maps.
- **Set:** unique values whose union, intersection, add, and remove operations return new sets.
- **Record collection views:** lazy or reusable transformations where retaining a full intermediate collection is unnecessary.

Operations never mutate the receiver:

```python
updated = users.set(user_id, revised_user)
visible = users.values().filter(is_active).map(display_name)
```

Literal behavior is consistent within a strict boundary, including nested literals and comprehensions. Crossing into ordinary Python requires an explicit conversion when an API expects a mutable built-in collection. Values returning from unchecked Python are foreign/unknown until validated or frozen.

A confined transient builder supports performance-sensitive bulk construction. The builder cannot be returned, captured, stored globally, or passed to unknown code; only its frozen result may leave the construction scope.

### Records and domain values

Python already has tuple-like records and frozen data classes, but those provide at most shallow, cooperative immutability. Py à la Mode owns a stronger **record** contract:

```python
@record
class Customer:
    id: CustomerId
    name: str
    tags: Set[str]
```

A record:

- has fields fixed at construction;
- accepts only immutable field values;
- supports value equality, hashing when all fields support it, destructuring, and pattern matching;
- provides a copy-with-changes operation that returns a new record;
- cannot acquire attributes dynamically;
- cannot hide mutable state behind a property, descriptor, or custom attribute hook.

The domain model also includes tagged alternatives for closed choices, plus `Option`, `Result`, and validation values for expected absence and failure. Exhaustive matching reports an error when a known case is omitted.

Ordinary classes remain available outside strict mode. Inside strict mode they are accepted only when they satisfy the immutable record/protocol contract; identity-centered mutable objects belong behind effectful boundaries.

### Pure functions

Functions in a strict module are pure by default. A pure function:

- derives its observable result only from its arguments and immutable constants;
- does not mutate arguments, captured values, globals, or foreign objects;
- calls only pure functions;
- does not read time, randomness, environment, process state, files, network, or other implicit inputs;
- does not perform output or durable state changes;
- cannot use dynamic execution or reflection that defeats analysis.

Pure functions may allocate immutable values, perform deterministic computation, recurse, pattern-match, and construct a `Result` describing an expected failure. Whether unexpected exceptions are permitted is separately visible in the function's contract; a function cannot conceal a known failure path behind an undocumented raise.

### Effects and capabilities

Effectful behavior is declared at function boundaries and propagated through callers. Initial effect families include:

- input/output;
- mutable state;
- clock and scheduling;
- randomness;
- environment and process interaction;
- concurrency and task coordination;
- raised failure;
- unchecked/unsafe Python.

An application entry point can declare the capabilities it needs:

```python
@effects(IO, Clock)
def main(args):
    ...
```

Pure code cannot call `main` or any function requiring those capabilities. Effectful code can call pure code freely. The product shows the shortest call path that introduced each effect and can distinguish an effect deliberately handled inside a boundary from one propagated to the caller.

Effects are part of a public callable's contract. Higher-order functions preserve the effects of callbacks instead of becoming implicitly unsafe. Tests can supply controlled capabilities, enabling deterministic clocks, randomness, and external responses without introducing mutable globals.

### Functional control flow

The product embraces existing expressions, comprehensions, iteration, functions, closures, and structural pattern matching. It adds library-level composition, pipelines, immutable updates, folds, and result traversal without requiring symbolic syntax in the first edition.

Imperative loops are allowed when each iteration is independent and no mutable accumulator escapes. Accumulation uses folds, comprehensions, recursion where appropriate, or a confined transient builder. `break` and early return remain available when they do not violate definite binding or resource/effect rules.

Expected domain failures use explicit values. Exceptions remain available for genuinely exceptional failures, but their presence is visible in the callable contract and exhaustive handling can be required by project policy.

### Imports and ordinary Python interop

Every imported value has one of four trust states:

1. **Checked:** produced by code verified under a compatible strict contract.
2. **Declared:** described by a reviewed external contract.
3. **Adapted:** accessed through a small wrapper that validates values and declares effects.
4. **Unsafe:** used without a trustworthy contract and therefore propagates an unsafe effect.

The standard Python library is presented through reviewed contracts that distinguish pure operations from I/O, state, time, randomness, and unknown behavior. Third-party libraries can publish equivalent contracts independently of their implementation language.

An unsafe escape hatch requires a bounded scope and rationale. It cannot assert that a mutable result is immutable; it can only move responsibility to a visible boundary, optionally followed by validation or freezing. Project policy may reject unsafe code, require named approval, or cap its growth.

### Dynamic Python features

Strict mode rejects or confines features that make the guarantees unknowable, including arbitrary `exec`/`eval`, monkey-patching, writes through reflection, mutable metaclass behavior, unreviewed descriptors, module-global mutation, and unknown native-extension behavior.

Read-only reflection may be accepted when its result and effect are known. Dynamic dispatch through checked protocols is supported. The aim is not to remove Python's expressiveness but to make loss of reasoning explicit.

## Source, compatibility, and editions

### Initial compatible edition

The initial edition is valid Python source plus declarations the tool recognizes. It includes the strict directive, recognized decorators, ordinary assignment-as-binding, immutable literal semantics within strict boundaries, records, effects, contracts, and explicit interop conversions.

This edition is the default because a comment can select external checking while decorators and assignments remain parseable by ordinary Python tools. Python itself ignores a mode comment, so the guarantee exists only when project commands, test execution, packaging, and continuous integration invoke Py à la Mode.

### Future syntax edition

A later source edition may add syntax such as `val`, pipeline forms, concise tagged alternatives, or explicit effect rows. Such files require preprocessing or a dedicated parser before Python can read them. New syntax ships only when user research shows that it materially improves clarity or expressiveness and when formatting, editor, traceback, packaging, and migration experiences are ready at the same time.

`val` alone does not meet that bar: strict assignment already has the same product meaning.

### Produced artifacts

Users can produce ordinary deployable Python artifacts whose runtime behavior matches checked source. Source locations, stack traces, coverage, and debugging refer back to authored code. Artifact metadata records the language edition, strict boundaries, contract versions, and unchecked dependencies so consumers can verify the claim they are receiving.

Running a generated artifact outside the product does not turn it into a security sandbox. The functional guarantee applies to the checked source and declared dependency boundary from which the artifact was produced.

## Project policy and team workflow

A project can define:

- the active language edition and supported Python versions;
- which packages, modules, and functions must be strict;
- public functions that require explicit type and effect contracts;
- allowed effects at named entry points;
- rules for exceptions and partial functions;
- approved dependency contracts and adapters;
- whether unsafe scopes are prohibited, time-limited, or approval-gated;
- whether audit findings may grow beyond the saved baseline;
- compatibility expectations for published functional contracts.

Policy inheritance is visible: a file can tighten project rules but cannot silently weaken them. Every suppression has a rule identifier, a narrow scope, a rationale, and optionally an owner and expiry. Reports distinguish active exceptions from unresolved accidental violations.

## Diagnostics and developer experience

Every diagnostic includes:

- a stable rule identifier and severity;
- the strict boundary whose guarantee would be broken;
- the primary source location and the relevant origin, such as the first binding or imported contract;
- a concise explanation in functional terms;
- one or more valid remediations: return a new value, use a persistent operation, declare an effect, adapt a dependency, freeze/validate a value, or narrow an unsafe scope;
- an explain view for multi-step effect and mutability paths.

Representative messages:

```text
PAL101 binding `count` is assigned more than once
  first bound here: totals.py:8
  written again here: totals.py:11
  return the next count from the expression or fold the sequence
```

```text
PAL221 `Customer.tags` is not transitively immutable
  `tags` receives `list[str]` from unchecked function `load_tags`
  freeze the result, adapt `load_tags`, or move this operation to an unsafe boundary
```

```text
PAL310 pure function `price_quote` performs the Clock effect
  price_quote -> current_campaign -> now
  pass time as a value or declare and propagate Clock
```

Editor feedback, command-line output, continuous-integration annotations, and machine-readable reports all use the same rule identities and explanations.

## Conceptual data managed by the product

Py à la Mode manages no user business data. It maintains a model of a codebase:

- **Projects and boundaries:** which projects, packages, modules, and functions participate in audit or strict mode.
- **Bindings and values:** where names originate, where writes occur, and whether reachable values are immutable, transient, stateful, or foreign.
- **Callable contracts:** inputs, outputs, purity, effects, failure behavior, and generic/higher-order relationships.
- **Type and record contracts:** immutable fields, tagged alternatives, protocols, and exhaustive match sets.
- **Dependency trust:** checked packages, reviewed declarations, adapters, unsafe imports, owners, and rationales.
- **Diagnostics and baselines:** current violations, accepted migration debt, suppressions, approvals, and changes over time.
- **Build claims:** the source edition, policy, contracts, and dependency evidence associated with a published artifact.
- **History:** when strictness, policy, dependency trust, effects, or unsafe surface changed and who approved exceptions.

## Acceptance criteria

### Opt-in and enforcement

- A developer can add the strict module directive to a valid module, check it, and run it when it complies.
- Reassigning a local, deleting it, mutating a captured value, writing a global, or modifying a function argument produces a blocking diagnostic with both origin and write locations.
- The same code in audit mode continues to use ordinary Python behavior and is never labeled as verified strict code.
- A `@pure` function inside an ordinary module receives the same purity checks as a pure function in a strict module without changing the rest of the module's semantics.

### Immutable values

- Collection literals, nested collections, and comprehensions inside strict mode cannot be changed in place.
- Each standard collection update returns a new value while leaving the original observably unchanged.
- A record containing a mutable or unknown nested value is rejected with the path to that value.
- Record updates create new records, support pattern matching, and cannot add or replace fields in place.
- A transient builder cannot escape its construction scope, and its frozen result behaves as an immutable value.

### Purity and effects

- A pure function that reads time, randomness, environment, a file, a network response, or mutable global state fails checking even when the operation is several calls away.
- The explain view shows a concrete call path from the pure function to the originating effect.
- Declaring an effect makes it part of the function contract and requires callers either to handle or propagate it.
- Passing an effectful callback to a higher-order function does not erase the callback's effects.
- Controlled clock and randomness capabilities make repeated tests deterministic without global patching.

### Interop and trust

- Importing a checked functional library preserves its published purity and immutability guarantees.
- Calling an ordinary uncontracted dependency from pure code is rejected rather than assumed safe.
- A reviewed declaration or adapter can make specific dependency operations available with their actual effects, without blessing the entire dependency.
- Every unsafe scope appears in a project report with its location and rationale, and policy can prevent new unsafe usage.
- Converting an immutable collection for a mutable Python API is explicit, and a mutable value returning from that API is not silently considered immutable.

### Migration and team policy

- An existing Python project can produce an audit report without changing runtime behavior.
- A team can save current findings as a baseline and fail later checks only when the mutation, effect, or unsafe surface grows.
- A function, then a module, then a package can be promoted to strict mode while surrounding code remains ordinary Python through explicit boundaries.
- A maintainer can identify expired suppressions, newly trusted dependencies, expanded effects, and reduced strict coverage from one change report.
- Policy applied by a project or package cannot be silently weakened by a source file.

### Packaging and debugging

- A compliant project can produce and consume a normal Python artifact while retaining its strict-contract metadata.
- Failures, tracebacks, coverage, and debugger locations point to authored strict source rather than opaque generated code.
- Rechecking the same source, policy, and dependency contracts produces the same functional claims.
- A consumer can tell whether an artifact is fully checked, partly adapted, or contains unsafe boundaries.

### Human usability

- A Python developer unfamiliar with formal effect systems can resolve the introductory reassignment, mutable collection, and undeclared I/O examples from the diagnostics and quick-start material alone.
- A developer can explain, from the reports, where the application's effects enter and where unchecked Python is allowed.
- A new project can gain value from milestone 1 without adopting records, persistent collections, or the later ecosystem features.

## Non-goals

1. **Not a security sandbox.** The mode improves program reasoning; it does not defend against hostile source, hostile native code, deliberate artifact tampering, or unrestricted reflection outside the checked boundary.
2. **Not proof that arbitrary Python is pure.** Dynamic or uncontracted behavior is rejected or marked unsafe. The product will not claim soundness by guessing.
3. **Not a new general-purpose language in the first edition.** The initial experience is a functional subset and semantic mode for Python. Novel syntax is deferred until it solves demonstrated usability problems across the whole toolchain.
4. **Not automatic parallelization, lazy evaluation, or distributed execution.** Immutability may make those systems easier to build, but changing evaluation or execution strategy would be a separate product.
5. **Not a transparent compatibility layer for mutation-dependent libraries.** Interop is intentional; code that relies on object identity, callbacks with hidden state, monkey-patching, or in-place updates may require an adapter or remain outside strict mode.
6. **Not a replacement for all testing or domain validation.** The checker enforces functional contracts, not business correctness, performance targets, numerical validity, authorization, or external-system behavior.
7. **Not a mandate for point-free or academically pure style.** Readable named bindings, ordinary control flow, exceptions where declared, and effectful application shells are valid.
8. **Not a promise of zero runtime overhead.** The product prioritizes clear guarantees and predictable interop; performance is measured and improved without weakening the contract.

## Assumptions and resolved ambiguities

1. **“Functional programming” means practical, eager, typed functional Python.** The product prioritizes immutability, pure logic, explicit effects, algebraic domain values, and composition. It rejects the reading “recreate Haskell semantics inside Python,” including mandatory laziness and pervasive currying.
2. **“Enforces” means blocking verification within declared boundaries.** It does not mean warnings, naming conventions, or runtime setter tricks alone. It also does not mean policing code that never opted in.
3. **The canonical scope is a file, with functions as the smallest island.** Arbitrary inline blocks are rejected for the first edition because their invisible scope and Python's existing name rules would make the guarantee hard to understand.
4. **Ordinary assignment declares an immutable binding in strict mode.** A new `val` token is rejected initially because it would require a separate parser while duplicating a rule the mode already knows.
5. **CPython ecosystem interoperability matters more than byte-for-byte ordinary-Python semantics inside strict scopes.** In particular, collection literals may yield immutable values and loop/pattern bindings have stricter scope rules. The rejected reading is “a linter only, with no semantic difference at runtime.”
6. **Static checking provides the primary guarantee; runtime guards defend boundaries.** A runtime-only approach cannot reliably catch hidden effects or mutation before code executes, while a purely static claim cannot validate every foreign object.
7. **Immutability is transitive for owned values.** A frozen outer shell around a mutable list is not considered an immutable record. The rejected reading is “disabling attribute setters is enough.”
8. **Effects are explicit and allowed.** The application shell may perform I/O and state changes; the rejected reading is “all useful code must be globally pure.”
9. **Type annotations are encouraged at public strict boundaries but not required on every local.** The product infers what it can and asks for declarations where ambiguity would weaken a public contract.
10. **The product begins as a local developer and team tool.** A centralized hosted service may visualize reports later, but no cloud account is required to obtain or enforce the functional guarantee.

## Feasibility stance

The concept is feasible, with one hard boundary: Python does not treat arbitrary comments as syntax and rejects unknown grammar such as `val x = 42` before an ordinary library can run. A comment like `# pyalamode: strict` can select behavior only because an external checker/runner recognizes it. Decorators provide valid-Python function-level declarations. Python's documented syntax tree and compilation facilities support analysis and transformations, and its import system is extensible enough to load specially handled modules; neither fact makes unrestricted Python statically knowable. [Python lexical analysis](https://docs.python.org/3/reference/lexical_analysis.html), [AST facilities](https://docs.python.org/3/library/ast.html), [Python import system](https://docs.python.org/3/reference/import.html).

Likewise, existing “frozen” records are a useful interoperability surface but not the final guarantee: Python's own data-class documentation describes frozen instances as an emulation and notes that truly immutable Python objects are not generally provided. Py à la Mode therefore needs its own transitive immutability contract rather than equating `frozen=True` with functional safety. [Python data classes](https://docs.python.org/3/library/dataclasses.html#frozen-instances).

The product should therefore begin with a source-compatible checked subset plus controlled runtime values and explicit interop. It may later offer a preprocessed syntax edition, but it should never confuse syntactic novelty with enforceable semantics.

## XL roadmap

### Milestone 1 — Strict functional modules

A developer can mark a module or function as strict, check it, and run it. The product enforces single-assignment bindings, bans obvious mutation and dynamic escape routes, treats functions as pure by default, reports source-linked violations, and supports a small useful pure-Python subset. This milestone stands alone: a team can immediately protect calculation, transformation, and decision modules.

### Milestone 2 — Immutable collections and records

Strict code gains immutable collection literals and comprehensions, persistent update operations, transitive record immutability, copy-with-changes, value equality, and structural pattern matching. Explicit conversions let these values cross ordinary Python APIs without mislabeling mutable returns.

### Milestone 3 — Effects and application shells

Functions can declare I/O, state, clock, randomness, environment, raised failure, and unsafe effects. Effects propagate through call chains and higher-order functions, while explain output shows their origin. Applications can keep a pure core and a clearly effectful entry point.

### Milestone 4 — Results, alternatives, and exhaustive workflows

Domain modeling gains tagged alternatives, `Option`, `Result`, validation accumulation, exhaustive matching, and visible failure contracts. Developers can express expected failure without mutation or invisible exception paths.

### Milestone 5 — Safe Python standard-library interop

Developers receive reviewed contracts and functional adapters for high-value standard capabilities, including pure computation, iteration, text/data transformation, files, time, randomness, processes, and concurrency. Each operation carries its actual mutability and effect contract.

### Milestone 6 — Third-party dependency boundaries

Projects can review and consume external contracts, build narrow adapters, freeze or validate foreign values, and track unsafe dependencies. Library authors can publish functional contracts that downstream projects verify and version independently.

### Milestone 7 — Project policy and continuous enforcement

Teams can require strictness by package, constrain effects at entry points, govern unsafe exceptions, prevent baseline growth, and compare functional-contract changes during review. Reports provide adoption, effect, mutation, trust, and exception history.

### Milestone 8 — Editor, debugger, and test experience

Developers receive immediate diagnostics, safe quick fixes, effect and mutability explanations, source-accurate debugging, and testing support for pure functions and controlled capabilities. The experience is consistent across local editing, commands, and automated checks.

### Milestone 9 — Existing-code migration

Audit mode inventories a normal Python codebase, identifies promising pure regions, establishes baselines, and guides function-by-function and module-by-module conversion. Progress metrics reward reduced mutation and unsafe surface without misrepresenting audited code as strict.

### Milestone 10 — Packaging and checked-library distribution

Applications and libraries can publish ordinary Python artifacts with source mappings and verifiable functional-contract metadata. Consumers can distinguish fully checked, declared, adapted, and unsafe surfaces and detect incompatible contract changes.

### Milestone 11 — Ownership, transients, and performance confidence

Confined transient construction and ownership rules support efficient bulk transformations without observable mutation. Developers can inspect structural sharing and performance guidance, and the product prevents a transient or mutable foreign alias from escaping as an immutable value.

### Milestone 12 — Concurrency and deterministic coordination

Immutable values move safely across tasks, while task creation, cancellation, scheduling, queues, and shared state remain explicit effects. Controlled schedulers and clocks support deterministic tests, and unsafe shared-memory patterns are rejected inside strict boundaries.

### Milestone 13 — Extensible contracts and language editions

Tooling contributors can extend reviewed API knowledge without weakening core guarantees. The product establishes compatibility rules for contracts and language editions, then pilots only those syntax additions—potentially concise values, pipelines, or tagged alternatives—that prove clearer than source-compatible forms.

### Milestone 14 — Operational maturity and ecosystem governance

The product adds long-term contract compatibility reporting, exception expiry workflows, organization-level policy distribution, reproducible verification claims, ecosystem quality criteria, and a stable contribution/review process for trusted contracts. Teams can adopt it as durable engineering policy rather than a local experiment.

## Product success measures

- A new user can protect a useful pure module in under fifteen minutes.
- At least three quarters of introductory violations are fixed from the primary diagnostic without opening separate documentation.
- Existing projects can adopt one strict boundary without converting unrelated modules.
- Strict builds have zero unreported mutation or effect paths in the supported language surface.
- Teams can keep or reduce unsafe surface over time and can identify every exception owner and rationale.
- Functional libraries retain their contract when packaged and consumed by another project.
- Performance on representative immutable transformations is predictable enough that teams do not need to abandon strict mode for routine workloads.

## Open product questions for validation

These do not block the initial direction, but user research should settle them before their milestones ship:

1. Should strict collection literals preserve Python's exact display and equality conventions, or visibly identify functional collection types to reduce boundary surprises?
2. Which effect families are most understandable to ordinary Python users without collapsing everything into “I/O” or overwhelming them with taxonomy?
3. Should declared exceptions be a first-class effect in the default policy, or an optional stricter profile after `Result` workflows are available?
4. How much local type inference can remain predictable before public annotations become the clearer experience?
5. Which standard-library and third-party packages provide the smallest adapter set that makes the product useful for real applications?
6. What evidence would justify a syntax edition, and which proposed syntax solves a semantic problem rather than expressing a stylistic preference?
