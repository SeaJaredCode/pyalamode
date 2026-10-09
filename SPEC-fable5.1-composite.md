# Py à la Mode

**Status:** Composite product specification, assembled from four prior passes (see `SPEC-fable5.1-review.md` for provenance and the reasoning behind each decision)
**Scope:** XL, fourteen independently useful milestones
**Slug:** `pyalamode`
**Mode name:** `fun`
**Product:** A Python language mode and developer toolchain. No hosted service, no accounts. Everything the tool knows about a project lives in plain files checked into the repository.

> **Scope note.** The brief's web-application framing does not apply to this product. Its persistence requirement is satisfied by policy, baselines, manifests, and report snapshots living as files in the project so they survive machines, clones, and CI runs.

## Purpose

Py à la Mode adds an enforceable functional mode to ordinary Python. A developer marks a module or a function as `fun`, and inside that boundary three properties hold and are checked:

| Property | Promise | Insufficient substitute |
|---|---|---|
| Binding immutability | A name keeps its value for its whole binding lifetime. | A mutable object behind a constant name. |
| Value immutability | Nothing reachable from a value can observably change. | A frozen outer record containing a list. |
| Purity | A result depends only on explicit inputs and checked constants, with no external effects. | A function that never assigns but reads a clock or a changing global. |

Teams protect calculation and decision logic (pricing, parsing, rules, transformations, anything they test exhaustively or run in parallel) while keeping ordinary Python for application integration. Today that protection comes from discipline and review. Here it becomes a property of the code, checked by a tool, adopted one function at a time, and never requires leaving Python.

The product is a mode and a toolchain, not a claim that arbitrary Python can be made pure. Inside a strict boundary, violations block checking and execution. Outside it, Python is Python.

## Principles

1. **Functional by default inside the boundary.** Assignment is a binding. Functions are pure unless they declare effects.
2. **A successful check means something.** Unknown behavior fails closed in strict mode. No annotation, cast, suppression, or convention upgrades unknown to verified.
3. **Guarantees have a visible edge.** Checked, trusted, unsafe, and unchecked code never blur together, in diagnostics, reports, or published claims.
4. **Adoption is gradual.** One function can opt in without converting its callers or dependencies. Audit mode and baselines make migration debt visible without certifying it.
5. **Python familiarity is an asset.** The compatible edition is valid Python with unchanged literal semantics. New syntax arrives only in a separately identified edition that requires translation.
6. **Effects are capabilities, not sins.** Programs read files and call services. Those operations belong at named boundaries and remain callable from other effectful code.
7. **Diagnostics teach the model.** Every error names the rule, points at the origin and the violation, and offers a functional rewrite or a deliberate boundary.
8. **Escape hatches are explicit and counted.** Every one carries a reason and appears in reports as debt.

## Personas

| Persona | What they want |
|---|---|
| **Developer** | Write `fun` code daily, see violations as they type, apply the suggested functional rewrite. |
| **Adopting team / migrator** | Audit an existing codebase, convert it module by module with a readiness report and mechanical rewrites, never pretend unchecked code is safe. |
| **Library author** | Ship a manifest so downstream `fun` code can call the package without every call being unknown; earn a visible certification summary. |
| **Integration owner** | Wrap ordinary Python and external systems behind small, reviewed effectful or unsafe boundaries. |
| **Policy owner / maintainer** | Set strictness by path, govern escape hatches and trust, make CI hold the line while debt shrinks. |

These are workflow roles, not account types.

## User stories

1. As a developer, I put `# mode: fun` on my pricing module, run `pyalamode check`, and get every rebinding, mutation, and hidden effect listed with a one-line reason and the rewrite, so I can make the module pass in one sitting.
2. As a developer, I call `print` from a function that declared no `IO` effect and the checker stops me. I declare the effect, which propagates to every caller, or I move the printing to the rim of the program.
3. As a developer, I build records and collections, derive updated versions, match domain alternatives exhaustively, and the originals never change.
4. As a library author, I ship a manifest describing which operations are pure, which perform effects, and which mutate their arguments, and downstream `fun` code calls my package without the checker treating it as unknown.
5. As a migrator, I ask for a readiness report on a legacy package and get ranked blockers, a leaf-first conversion order, and a one-command mechanical rewrite for accumulator loops, in-place sorts, and attribute-bag classes.
6. As a policy owner, I require `core/` to be strict, forbid ignore directives there, record a baseline, and CI fails on any new violation while the baseline can only shrink.
7. As a maintainer reviewing a change, I see what became verified, what lost verification, which effects changed, and which new trust was introduced.

## The mode

### Opting in

Two primary boundaries, both valid Python:

```python
# mode: fun
```

placed in the module header (after shebang, encoding, and docstring; before any statement). It covers every definition and initialization expression in the module. A misplaced directive is an error, never a silent partial mode.

```python
from pyalamode import fun

@fun
def discounted_total(cents: int, discount_cents: int) -> int:
    discounted = cents - discount_cents
    return max(0, discounted)
```

covers the function, its nested functions, its defaults, its captures, and its dependency contracts. It does not certify the surrounding module. This is the recommended first adoption step.

Project policy can also declare whole paths strict so a tree needs no per-file marker.

Arbitrary comment-delimited or indentation-delimited blocks are not boundaries. Python blocks are not scopes, and a mid-function semantic change with no scope rules cannot be reviewed or checked. A constrained inline region, `with fun:`, is specified in milestone 14 with the rules that make it honest.

There is no `@unfun`. Carving an unchecked hole inside a strict module is an unsafe region (see Interop) and carries the same reason and reporting requirements.

### Enforcement levels

- **Off.** Ordinary Python. No functional claim.
- **Audit.** Ordinary runtime behavior continues. The checker reports what would stop a boundary from being strict, including the propagating `Unknown` effect for uncontracted calls. Findings can be baselined. Nothing in Audit is a guarantee.
- **Strict.** Violations are errors. The boundary cannot be run through supported execution, or published as checked code, until they are resolved or moved behind an explicit effectful or unsafe boundary.

There is no level at which a warning counts as proof of purity.

### Evidence is separate from purity

Every callable has a behavioral contract (pure, or a set of effects, plus a failure contract) and an evidence status:

| Evidence | Meaning |
|---|---|
| **Checked** | Supported source and all dependencies satisfy the checker. |
| **Trusted** | At least one dependency relies on a confirmed manifest entry or reviewed adapter rather than checked source. Propagates to callers. |
| **Unsafe** | Contains or depends on an unsafe region. Propagates to callers. |
| **Unchecked** | Outside any participating boundary. |

A function can be pure by trusted declaration. The product always shows the trust. A drafted (unconfirmed) manifest entry is `Unknown`, not `Trusted`.

### What the checker may not do

The checker never executes or imports application source to discover its behavior. Module initialization is part of the dependency contract; a pure export does not make importing its package effect-free. Supported execution checks the current source, edition, policy, and dependency contracts *before* strict initialization runs, because decorators and parameter defaults execute while Python defines a function, and no runtime wrapper can retroactively prevent an effect that already happened.

A stock interpreter ignores the comment marker. Running marked source through bare `python` is unchecked execution, and every command and document says so. Installing the runtime library does not change what any literal means.

## Bindings

### Assignment is a binding

```python
x = 42
x = 43        # PAL101 rebind
```

Inside a boundary, every name-binding form participates: assignment, destructuring, parameters, imports, function and class definitions, loop targets, pattern captures, exception targets, comprehension variables. Augmented assignment, `del`, `global`, `nonlocal`, and assignment expressions are rejected. Rebinding to an equal value is still a rebinding.

The rule is one initialization on every path that uses the name, not one textual assignment per file:

```python
if member:
    fee = 0
else:
    fee = 10
return fee       # allowed: every continuing path initializes fee exactly once
```

A path that reaches a use without initialization, or reaches a second initialization, fails with both locations named. Early returns are accounted for. A nested function may introduce a parameter with an outer name's spelling; it may capture an outer immutable binding; it may not change one.

### Loops

`for` is admitted from milestone 1 under one rule: the loop target and every name first bound in the body are fresh per iteration, cannot be read after the loop, cannot be loop-carried, and cannot reuse an already bound surrounding name. Accumulation uses `fold`, `scan`, comprehensions into an immutable constructor, or recursion. A closure that captures a loop binding cannot escape the iteration; a checked function factory with an explicit argument produces a stable capture.

This is a restriction on accepted Python, not a claim that Python loops gain scopes. The checker models the real binding behavior.

`while` is not admitted in the pure core, because a terminating `while` depends on a binding changing. Immutable iteration helpers (`iterate`, `unfold`, bounded recursion) cover the use cases. Unbounded recursion remains possible and acquires no termination guarantee.

### Destructuring and patterns

Destructuring initializes each target once and rejects repeated names in one target. Starred unpacking produces a `Vector`, not a list. Pattern captures follow branch rules and operate only on admitted records, variants, and immutable values. Exception targets are local to their handler; the exception object, its traceback, and its frames do not enter the value domain (see Failure).

## Values

### Admitted values

Pure code accepts: `None`, `bool`, `int`, `float`, `str`, `bytes`; recursively immutable tuples and frozensets of admitted values; the product's persistent collections; checked records and variants; and callables whose contract is Checked or visibly Trusted and whose captures are admitted values.

`Decimal` and other context-sensitive numerics are admitted only through a contract that makes the context an explicit input; the ambient context is a prohibited read. Floats carry the standard caveat that the guarantee covers equivalent results within a supported runtime, not bitwise identity across machines.

A built-in type's subclass does not inherit the built-in's evidence; it can override operations. Having `__hash__`, a `Final` annotation, or a `Sequence` interface is not evidence.

Every value is one of:

- **Stable data.** Reachable contents and observable operations satisfy the immutable contract.
- **Confined construction state.** A transient builder under ownership rules (milestone 12).
- **Effect capability.** An opaque handle whose operations require declared effects. Never ordinary data; a frozen holder containing a connection is not a record.
- **Foreign or unknown.** Must be frozen, adapted, or handled in an unsafe region before it is stable data.

### Deep immutability

```python
payload = ([],)      # PAL221: payload[0] is a mutable list
```

The checker reports the nested path, not the outer type, and inspects closure captures, record defaults, properties, and the behavior a value exposes, not only its fields. A read-only view over mutable storage (`MappingProxyType`, a memoryview, a live ORM row) is a view of changing state and is rejected as stable data.

Identity is not value. `id`, address-based representations, frame inspection, and weak references are excluded from the pure core. `is` is admitted only for supported singleton checks such as `value is None`.

### Literals in the compatible edition

`[]`, `{}`, and `{1}` keep their Python meaning everywhere. In strict code they are rejected (PAL230) with a quick fix to the immutable constructor:

```python
prices = Vector.of(10, 20, 30)
tags = Set.of("member", "trial")
customer = Map.of(name="Ada", points=10)
```

Comprehensions are admitted when they feed an immutable constructor eagerly and their source and callbacks are checked. The syntax edition (milestone 14) may give literals immutable meaning openly, because it already requires translation.

### Crossing the boundary

`freeze(value)` produces an independent, deeply immutable snapshot of supported ordinary data: lists become `Vector`, dicts become `Map` (or `OrderedMap` on request), sets become `Set`, frozen dataclasses and named tuples become records when their complete contract qualifies. The contract:

- No retained alias. Mutating the original afterwards cannot affect the snapshot.
- Already admitted values are reused without copying, with no promise about identity.
- Unsupported objects and cycles fail with the offending path. Cycles are modeled with immutable identifiers or a domain adapter.
- No user-defined properties, iteration hooks, or constructors run during generic conversion. That behavior needs a named adapter.
- Snapshotting concurrently changing data needs exclusive access or a synchronized snapshot adapter; otherwise the conversion refuses.

`freeze` is itself an operation on possibly changing state and belongs in the shell or in a declared-effect function, not in pure code.

`thaw(value)` hands ordinary code a fresh mutable copy. Mutating it does not affect the source. Mutable values cannot flow back into pure code without another `freeze`.

A value arriving at a strict function from ordinary code is **borrowed**. Checked entry points validate it at runtime: wrong type, nested mutability, unrecognized callable, or a built-in subclass fail before the body runs. A borrowed mutable value stored into a record, captured, or returned without `freeze` is a static error (PAL240 borrowed escape). The runtime does not try to make the caller's object read-only in place; that is not possible for a `list` already referenced elsewhere, and the product does not pretend otherwise.

## Collections

| Value | Operations |
|---|---|
| `Vector` | index, slice, `appended`, `set`, `concat`, `map`, `filter`, `fold`, `scan`, `sorted_by`, `group_by`, `partition`, `zip`, `window`, `chunk`, `flat_map`, `distinct`, `take`, `drop`, `take_while`, `first`, `last`, `find` |
| `Map` | lookup, `set`, `without`, `update_in` (nested path), `merge`, `map_values`, traversal under an explicit ordering contract |
| `OrderedMap` | `Map` operations with insertion order as part of the value |
| `Set` | membership, `with_`, `without`, union, intersection, difference, order-independent transforms |
| `Seq` | replayable lazy sequence over immutable inputs and checked callbacks for pipelines over large or unbounded data (milestone 12) |

Every update returns a new value; earlier versions and everything reachable from them stay stable. Structure is shared between versions so `appended` on a large vector is cheap; the user never manages the sharing. Ignoring the result of an update whose only purpose is the result is a diagnostic (PAL231), because it almost always reflects a mutable-collection habit.

Callbacks to `map`, `filter`, `fold`, and friends are checked like named calls. Passing a callback through a collection does not make it pure.

### Ordering

A `Vector`'s order and an `OrderedMap`'s entry order are part of the value. `Map` and `Set` have order-independent equality, and incidental insertion order or process-randomized hash order cannot reach an order-sensitive computation: traversal needs an explicit total order, or the consuming operation needs a verified order-independent result. A sort key that leaves ties needs a tie-break. Float reduction is not automatically order-independent. Internal hashing for storage is fine; exposing a randomized hash as a result is not pure.

### Iterators and generators

A consumable iterator has cursor state and is not an immutable collection. Private iterator machinery is confined to an approved eager constructor or terminal operation. A generator is admitted as a value only when it satisfies the replayable `Seq` contract; an ordinary generator returned as if it were a sequence is rejected (PAL233).

### Performance

Releases publish time and peak memory for repeated append, key update, nested update, `freeze` of representative inputs, and retained histories at stated sizes, and disclose any operation that copies a whole collection. Whether the implementation reuses an existing persistent-collection library or is written fresh is an engineering decision; a candidate must satisfy the deep-value, alias, callback, ordering, and performance contracts.

## Records and variants

```python
from pyalamode import record, variant, replace, Vector

@record
class Customer:
    name: str
    tags: Vector[str]

@fun
def tag(customer: Customer, label: str) -> Customer:
    return replace(customer, tags=customer.tags.appended(label))
```

A record has a fixed field set of admitted values; value equality; hashing when every field hashes; readable representation; destructuring and `match`; and `replace` returning a new instance, mirroring `dataclasses.replace`. Constructors, defaults, validation, methods, and computed properties obey the same purity rules as functions. Dynamic attributes, unreviewed descriptors, metaclass behavior, custom `__setattr__`, and post-construction mutation are not admitted because a decorator is present. Records are sealed against unverified subclassing.

Inside a strict module, `class` means record or variant. Identity-centered stateful classes belong behind effectful boundaries.

```python
@variant
class Shape:
    @record
    class Circle:
        radius: float
    @record
    class Rect:
        w: float
        h: float
```

A variant is a sealed set of records. `match` over a variant must be exhaustive; a missing case is an error (PAL410), and adding a case lights up every incomplete match in the project. Guards do not count as covering a case. An open external class hierarchy is never advertised as a variant.

`Option` (`Some`/`Nothing`) and `Result` (`Ok`/`Err`) ship as variants with `map`, `and_then`, `or_else`, `unwrap_or`, `to_option`, and a validation accumulator for independent errors. Existing frozen dataclasses and named tuples are accepted as records when their complete contents and behavior qualify; `frozen=True` alone is not sufficient.

### Value interchange

Supported values encode to and decode from bytes with their contracts validated. Encoding is pure; reading or writing the bytes is `IO`. Decoding never runs arbitrary constructors or restoration hooks. A changed record or variant contract produces an explicit compatibility result. Function values and capabilities are not data payloads.

## Purity and effects

### Pure computation

A pure function computes from explicit stable inputs and checked constants. It may allocate immutable values, call checked pure operations, branch, recur, match, and return a result or a declared failure.

It may not read a changing global, a mutable closure cell, ambient configuration, a clock, an unseeded random source, locale, numerical context, file, network, or process state. Reading mutable state without writing it is still a violation.

A global name in an ordinary module is not a stable constant because its current value is an integer: the *binding* can be reassigned elsewhere. Pass it as an argument or establish it as a checked constant. Checked constants from strict modules are permitted and pinned for the duration of a checked run.

Purity is independent of totality. A pure function may fail or never terminate. The product does not prove termination, resource sufficiency, or numerical correctness.

### Everything is a call

Operators, truth testing, iteration, comparison, hashing, formatting, attribute and property access, context-manager entry and exit, and pattern matching invoke methods. `a + b` is exactly as pure as the resolved `__add__`. A property that logs, an `__iter__` that reads a file, or a `__str__` of unknown implementation (PAL340) does not pass because its syntax looks harmless.

This requires the checker to know what a name refers to at each dispatch site. The product is not a replacement for the project's type checker and does not check argument and return types for their own sake. It does perform local inference, consume the project's type checker output when available, and resolve callees against manifests. Where the target cannot be resolved (`Any`, an unknown callable, dynamic dispatch with uncharacterized implementations), the operation is `Unknown`: an error in Strict, a tracked effect in Audit. Dynamic dispatch through a checked protocol is admitted when every implementation satisfies the contract.

A shadowed builtin resolves to what it actually is, not to its familiar spelling.

### Effects are declared capabilities

```python
from pyalamode import effects, IO, Clock

@effects(IO, Clock)
def report(prices: Vector[int], clock: Clock, out: IO) -> None:
    total = prices.fold(0, lambda acc, p: acc + p)
    out.write_line(f"{total} at {clock.now()}")
```

Effect families: `IO` (files, network, console), `State` (observation or change of mutable shared state), `Clock`, `Random`, `Env` (environment, process, locale), `Tasks` (task creation, scheduling, cancellation, coordination), and `Unsafe`. They are importable names, so a typo is an import error, not a silent string.

A declaration is a checked upper bound, not a waiver: an `@effects(IO)` function that reads the clock fails. Capabilities arrive as explicit parameters (or are constructed by the application shell) and are the only way to perform the effect; a function cannot reach `open` or `time.time` directly. Effects propagate: a caller of an effectful function declares or propagates its effects. Effectful code calls pure code freely. Pure code cannot call effectful code and suppress the evidence.

Effectful strict functions keep the binding and value rules. State changes happen through a `State` capability, not through assignment to domain values.

Higher-order functions carry their callbacks' effects. Effects do not disappear through lambdas, partial application, decorators, callable objects, protocols, or aliases. Mutually recursive functions keep their inferred or declared effects.

Constructing an immutable description of an effect is pure; executing it needs the capability. Time and configuration can be ordinary inputs; seeded randomness can be a pure transition returning a sample and a new state. Mock and recorded capabilities make tests deterministic without global patching, and the function still carries the effect it declared.

### Failure

Failure is a contract dimension separate from effects. A function's visible contract states its supported failure behavior. Expected domain failures use `Result`; a project can require value-based failure on selected public APIs. Declared recoverable exceptions can be raised and handled; `except` targets are local to the handler, and the exception instance, traceback, and frames do not enter the value domain. A supported exception converts to an immutable error value. Handling a failure does not erase effects already performed.

### Definition time

Decorator expressions, defaults, class bodies, and module-level statements run when Python defines things. In a strict module, module-level code may bind constants, define functions, records, and variants, and nothing else. Supported execution checks before any of that runs; `@fun` on one function in an ordinary module covers that function's defaults and decorators but says nothing about the module around it. Reports show import-time evidence separately from invocation evidence.

## Interop and manifests

### Manifests

A manifest describes one package to the checker: for each public operation, whether it is pure or which effects it performs, whether it mutates any argument or its receiver, whether it retains an alias to an argument, what it returns (stable or foreign), its failure behavior, and the version range the entry covers.

- The product ships built-in manifests for commonly used standard-library modules, so `math`, `itertools`, `functools`, `re`, `json` parsing, `datetime` arithmetic (with `now()` as `Clock`), string and number operations, and the like are usable on day one.
- A library author ships a manifest inside the package.
- A project adds manifests for third-party packages and can override any entry.
- Precedence: project override, then the package's own manifest, then built-in, then `Unknown`.
- `fun` code needs no manifest for itself; the checker derives its contracts.

Each entry is **confirmed** or **drafted**. `pyalamode manifest draft <package>` produces a draft from signatures and naming conventions with every guess marked drafted. A drafted entry is `Unknown` to Strict; a confirmed entry makes its callers `Trusted`, never `Checked`. Confirming is a reviewed act with an owner and a reason, recorded in the project. A standard-library package is not pure because one function is; a native extension is not safe because its signature is annotated.

Entries bind to versions. A dependency upgrade outside an entry's range invalidates it until reconfirmed, and every caller that relied on it is rechecked.

### Adapters

An adapter is a small, reviewed function that separates an effectful fetch from the pure transformation of its frozen result, declares its real effects, validates or freezes what it returns, and names the evidence it relies on. An adapter that retains a mutable alias or returns a stateful view cannot certify stable data. Copying arguments before and after an external call does not prove the call avoids clocks, files, or hidden callbacks.

### Unsafe regions

```python
with unsafe("legacy tax table is a module-global dict; adapter tracked in TAX-412"):
    rate = legacy_rates[region]
```

An unsafe region is bounded, carries a reason, propagates `Unsafe` to callers, and appears in every report. It cannot certify its result as stable data without a separate `freeze`. There is no `trust_me_pure`. Policy can forbid unsafe regions by path, require an owner, or cap their count.

### Unsupported dynamic behavior

Unchecked `eval`/`exec`, runtime code generation, reflective writes, monkey-patching, namespace mutation, mutable metaclass behavior, and uncharacterized native calls are rejected in strict code or placed in an unsafe region. Read-only reflection with a known result can be admitted. Dynamic imports and runtime replacement of verified dependencies need compatible evidence before participating.

## Supported execution

`pyalamode run` checks, then executes, with boundary enforcement:

- **Entry validation.** Every strict entry point validates values arriving from ordinary code before the body runs.
- **Freshness.** A cached verification is bound to the source, edition, policy, checker rules, and manifest versions that produced it. Any change invalidates it. Stale evidence refuses to run; it never degrades to an unchecked run.
- **Dependency pinning.** Checked constants and verified callables used by a strict region are pinned by identity at entry; a monkey-patched replacement observed at entry fails.
- **Effect audit** (development and test runs). I/O, clock, random, environment, and process primitives are instrumented to record any effect performed inside a function that did not declare it, with the stack and the manifest entry or absence that let it through. The audit lists every incident at the end of the run, and policy can make incidents fail the run. This is how manifest mistakes and surprising third-party behavior are caught.
- **Dynamic-construct guard.** Where the checker admitted a construct it could not fully resolve statically (a protocol dispatch, a checked reflection read), the runtime checks the actual target.

The guard reports its overhead. It is a development aid, not a sandbox, and it does not try to make foreign objects immutable in place.

## Tooling

### Commands

| Command | Does |
|---|---|
| `pyalamode check [paths]` | Verify strict regions; exit non-zero when policy is not satisfied. Terse CI mode and machine-readable mode. |
| `pyalamode run <program>` | Check, then execute with boundary enforcement and the effect audit. |
| `pyalamode explain <rule or location>` | Rule rationale with examples, or the binding, nested path, or call chain behind a specific diagnostic. |
| `pyalamode regions` | Every region with marker kind, extent, enforcement level, evidence status. |
| `pyalamode baseline` | Record current Audit findings as accepted debt. |
| `pyalamode manifest draft <package>` | Draft a manifest with every entry marked drafted. |
| `pyalamode ready <path>` | Readiness report: score, blockers by rule, uncontracted calls, leaf-first conversion order. |
| `pyalamode convert <target>` | Apply mechanical rewrites with a diff and confirmation; recheck; list what still needs a human. |
| `pyalamode report` | Coverage, effect inventory, boundary map, hotspots, debt, trust, trend; writes a self-contained page. |
| `pyalamode build` | Produce a checked distributable with verification claims, or translate syntax-edition source to inspectable Python. |

Checking a large project a second time after a one-file edit rechecks only what that edit can affect and finishes in well under a second (milestone 10).

### Diagnostics

Every diagnostic has a stable identifier and short name, severity, the boundary whose guarantee is at stake, the primary location, origin locations, a one-sentence functional explanation, and a remediation. Baselines key on identifiers and structural position, not line numbers.

```text
PAL101 rebind  core/pricing.py:42:5
  `total` is already bound at core/pricing.py:38
  In a fun region a name is bound once. To accumulate, fold:
      total = items.fold(0, lambda acc, line: acc + line.price)
  More: pyalamode explain rebind
```

```text
PAL221 mutable-nested  core/orders.py:17
  `Customer.tags[0]` contains a mutable list
  received from unchecked `load_customer`
  Create an independent snapshot at the boundary: freeze(load_customer(...))
```

```text
PAL310 undeclared-effect  core/quote.py:88
  pure function `quote` observes the clock
  quote -> campaign_for -> clock.now
  Pass the relevant time as data, or declare and propagate Clock.
```

```text
PAL340 unknown-dispatch  core/render.py:12
  the implementation of `value.__str__` is not resolved
  Formatting this value may run unchecked behavior.
  Use an admitted value or a confirmed manifest entry for its type.
```

Quick fixes distinguish safe mechanical rewrites (rename, loop to fold, in-place sort to `sorted_by`, attribute-bag class to record, add a missing `match` case stub, wrap a borrowed value in `freeze`, add a missing effect declaration) from meaning-changing ones (choose a traversal order, change failure behavior, accept a trust dependency), which preview and ask. No quick fix broadens permissions, suppresses a strict failure, or changes a public return type silently.

### Editor

One engine serves every editor through the standard diagnostics-and-actions mechanism. Inline diagnostics as you type with the same text as the CLI. Hover on a function shows its contract (pure or its effects, its failure contract, its evidence status). Hover on a value shows stable, borrowed, capability, or foreign. A "make this `fun`" action adds the marker and lists what breaks. Adding an effect shows affected callers; confirming a manifest entry shows the new trust assumption.

Tracebacks, coverage, navigation, and debugger stops refer to authored source, including for translated syntax-edition source.

### Policy

A checked-in policy file, owned by the policy owner:

- Enforcement level by path (`core/` strict, `scripts/` audit).
- Per-rule severity overrides by path.
- Public functions that require explicit type and effect contracts.
- Allowed effects at named entry points.
- Failure policy: where value-based failure is required.
- Whether unsafe regions are forbidden, owner-gated, or capped, by path.
- Whether ignore directives (`# fun: ignore[PAL101] reason`) are allowed, must carry a reason, or are forbidden, by path.
- Whether drafted manifest entries may be confirmed without a second reviewer.
- Whether the baseline may grow.

A file can tighten inherited policy and cannot weaken it. Every exception has a rule, an exact scope, a reason, an owner, and an optional expiry.

### Baseline and ratchet

`pyalamode baseline` records every current Audit finding by stable identity. Afterwards `check` reports only new findings, and the ratchet fails a run whose total exceeds the baseline. The baseline can be re-recorded only when the count went down; a policy owner can force it, and the force is recorded with who and why. Moving code cannot hide new debt, because identities are structural. Deleting a strict boundary, adding an unsafe region, or confirming a manifest entry appears in the change report even when the finding count drops.

### Reports

- **Coverage.** Share of functions and lines inside strict boundaries, by package, over time, with the denominator shown. Five easy functions do not make a project safe, and the report says so.
- **Effect inventory.** Functions grouped by effect; pure-to-effectful ratio; rim thickness (how far from entry points effects reach).
- **Boundary map.** Every boundary, the values that cross it, borrowed escapes, `freeze`/`thaw` sites.
- **Trust.** Every confirmed manifest entry and adapter in use, who confirmed it, which callers depend on it.
- **Debt.** Ignore directives, unsafe regions, drafted entries in use, expired exceptions, with reasons and owners.
- **Hotspots.** Ordinary-Python functions with the most mutation and ambient reads, ranked as conversion candidates.
- **Change review.** What became verified, what lost verification, which effects changed, which trust was added.
- **Trend.** Baseline count, coverage, debt, trust across snapshots.
- **Certification summary** for a library: manifest coverage of its public surface and the confirmed share.

Reports are files; snapshots live in the repository.

### Migration assistant

`pyalamode ready <path>` scores a tree, groups blockers by rule with counts, lists external calls with no confirmed entry, and proposes a conversion order that starts at call-graph leaves so each conversion is small and its callees are already strict.

`pyalamode convert <target>` applies the mechanical rewrites in bulk, shows the diff, waits for confirmation, writes only to the files it was pointed at, rechecks, and lists what still needs a human. Reversal is the project's version control.

## Packaging and claims

`pyalamode build` produces an ordinary Python artifact whose runtime behavior matches checked source, with a verification claim recording the edition, policy, checker rules, strict boundaries, failure and effect contracts of public entry points, and every trust and unsafe dependency with versions. Consumers inspect the claim, verify it against the installed artifact and dependency versions, and see Checked, Trusted, and Unsafe surfaces distinctly. A changed dependency version invalidates the affected claim until rechecked. A verified export does not imply the whole distribution was checked.

A published supported-interpreter matrix states what runs where. Unsupported syntax, runtime, or platform fails explicitly rather than degrading.

## Ownership and efficient construction

A transient builder (milestone 12) permits mutation nobody can observe: fresh state or a qualified immutable input, one owner, no retained input alias, no capture in an escaping closure, no sharing across tasks, one-way finalization into stable data that invalidates every builder alias. Escape through return, record field, closure, global, callback, unknown code, or task fails statically; use after finalization fails. Ownership cannot be asserted for a foreign object that may have aliases.

Builders are opt-in and separately reported. A project can forbid them. Persistent operations remain the default vocabulary.

## Concurrency

Immutable values cross task boundaries safely. Task creation, scheduling, cancellation, queues, and shared services are `Tasks` effects. `par_map` runs a pure function over a collection in parallel and requires a `Tasks` capability; a builder or foreign mutable object captured into a task fails. A controlled scheduler supports repeatable tests where the supported scheduler can promise it. The product does not model ordering between arbitrary threads, make external systems deterministic, or promise speedups.

## Testing

Pure tests use explicit immutable inputs and expected outputs. Property-test helpers generate record and variant instances from their declarations. Integration tests supply controlled `Clock`, `Random`, `IO`, and `State` capabilities. Passing a timestamp as data removes the `Clock` effect from a calculation; passing a fake clock does not change the declared effect. `memoize` is accepted only on functions the checker knows to be pure and whose cache state is unobservable; applying it to an effectful function is an error (PAL350).

## Inline regions and the syntax edition

### `with fun:` (milestone 14)

A constrained inline region inside an ordinary function, recognized by the checker, with `fun` a no-op context manager at runtime:

```python
def summarize(count: int, label: str) -> str:
    with fun:
        doubled = count * 2
        summary = f"{label}: {doubled}"
    return summary
```

Rules: the region ends at the dedent and creates no scope. Only stable, deeply immutable host bindings may be read, and the checker verifies their binding behavior in the host. Names first bound inside the region cannot reuse a host binding. Module globals are not readable directly. Closures created inside cannot escape; immutable computed values can. Code after the region gets no guarantee from it. When the host is too dynamic, the diagnostic offers extraction to a `@fun` function with explicit parameters.

### Syntax edition (milestone 14)

An opt-in dialect marked `# mode: fun+syntax`, valid only through `pyalamode build` and the editor integration:

```text
val prices = [10, 20, 30]
val active = customers |> filter(_.active) |> map(_.name)
```

`val` makes the binding visible; `[...]` and `{...}` produce the edition's immutable values; `|>` and `_` give pipelines and placeholder partial application. Same rules, same evidence, same diagnostics with the same identifiers pointing at authored source. The compatible edition remains fully supported indefinitely. The syntax edition ships only when editing, formatting, translation, debugging, packaging, and migration all work; novelty is not the bar.

## Information the product manages

- A **project** has an edition, a policy, participating boundaries, manifests and overrides, a baseline, and report snapshots. All in files.
- A **boundary** has a marker kind, an extent, an enforcement level, an evidence status, and the functions, records, and variants inside it.
- A **callable contract** has inputs, outputs, purity or effects, failure behavior, capture requirements, and evidence; callbacks relate contracts to higher-order operations.
- A **value contract** describes stable fields or elements, admitted behavior, variant cases, and construction constraints.
- A **manifest** covers one package at a version range and has entries, each confirmed or drafted, each with a source (built-in, shipped, override) and, if confirmed, an owner and reason.
- A **finding** relates a rule to an origin and a violation. A **baseline** is a set of accepted findings. An **exception** has rule, scope, reason, owner, expiry.
- A **guarded run** produces incidents: entry rejections, undeclared effects, pinning failures, each with a stack and region.
- A **verification claim** binds source or artifact, edition, policy, rules, and dependency evidence to the guarantees a release carries.
- A **snapshot** records coverage, inventory, debt, trust, and baseline count at a time; the trend is the sequence.

## Acceptance criteria

A person can confirm each by doing it.

**Boundaries and enforcement**

1. `# mode: fun` on a module with `x = 42` then `x = 43` fails `check` with PAL101 citing both lines; `run` does not enter the function. Removing the marker makes `check` pass with no output.
2. `@fun` on one function in an ordinary module checks that function, its defaults, and its decorators without changing the rest of the module.
3. The same finding in Audit leaves execution unchanged and is never displayed as a guarantee.
4. A strict function called from ordinary code with a list argument fails at entry before the body runs; passing `freeze(the_list)` succeeds.
5. `run` refuses stale evidence after a dependency, policy, or manifest change until `check` passes again.
6. Documentation and `run` output state that bare `python` on a marked file is unchecked execution.

**Bindings and values**

7. Two mutually exclusive branches each initializing `fee` pass; a path with no initialization or a second one fails with the path named.
8. `x += 1`, `del x`, `global`, `nonlocal`, an assignment expression, and a repeated name in one destructuring target each fail under the binding rule; `a, *rest = t` gives `rest` as a `Vector`.
9. A `for` loop whose body binds a fresh name per iteration passes; reading the loop target or a body-local after the loop fails; a closure capturing the loop target that escapes the iteration fails.
10. `([],)` fails with the path `[0]`; a record with a list field fails naming the field; a `MappingProxyType` argument is rejected as stable data.
11. `freeze` of a dict with a nested list yields a `Map`; mutating the original list afterwards leaves the snapshot unchanged; a cyclic input fails with the path.
12. `[1, 2, 3]` in strict code fails PAL230 and the quick fix produces `Vector.of(1, 2, 3)`; the same literal in an ordinary module is untouched.
13. `prices.appended(40)` with the result discarded produces PAL231.
14. Two equal `Map`s built in different orders fed to an order-sensitive fold without an explicit ordering fail; `OrderedMap` or `sorted_by` with a tie-break passes.

**Records, variants, failure**

15. A `match` over a three-case variant handling two cases fails PAL410 naming the missing case; adding the case clears it; adding a fourth case to the variant flags every incomplete match.
16. `replace(customer, tags=...)` returns a new record and leaves the original unchanged; a frozen dataclass whose fields all qualify is accepted as a record without rewriting.
17. A pure function that raises an undeclared exception fails its failure contract; one that returns `Result` passes; policy can require `Result` on a public API.

**Purity and effects**

18. A pure function that reaches `time.time()` three calls away fails PAL310 with the call chain; `explain` prints the chain.
19. Adding `@effects(IO)` to a helper causes every caller without `IO` to fail in turn; an `@effects(IO)` function that reads the clock fails.
20. A pure callback passed to `map` keeps the result pure; a logging callback makes the call require `IO`.
21. A custom `__add__`, property, `__iter__`, or `__str__` with an effect, or with no resolved implementation, does not pass as pure (PAL340).
22. A module-global `int` read from a `@fun` function in an ordinary module fails as an ambient read; a checked constant from a strict module passes.
23. A strict module with an effectful top-level statement fails before that statement runs under `run`; `check` never executes it.

**Interop and evidence**

24. A call to a package operation with no manifest entry fails in Strict and appears as a propagating `Unknown` effect in Audit; a drafted entry changes nothing; confirming the entry makes the caller pass with evidence `Trusted`, not `Checked`.
25. Upgrading the package outside the entry's version range invalidates it and rechecks every dependent region.
26. An unsafe region without a reason fails; with a reason it passes, propagates `Unsafe`, and appears in the report; policy can forbid it under `core/`.
27. An adapter that returns a live view over mutable storage cannot certify stable data.
28. A borrowed list stored into a record or returned without `freeze` fails PAL240.

**Supported execution**

29. Under `run`, a third-party call that performs I/O inside a function with no `IO` declaration appears in the effect audit with its stack and the manifest entry that admitted it; policy can fail the run.
30. A monkey-patched checked dependency observed at a strict entry point fails pinning.

**Policy, migration, review**

31. After `baseline` on a project with forty findings, `check` reports none; one new finding fails the run and names it; fixing five and re-recording succeeds; re-recording after adding one fails without the force flag, and a forced re-record is recorded.
32. A file that attempts to relax package policy fails; an expired exception fails; a newly confirmed manifest entry appears in the change report even when the finding count dropped.
33. `ready legacy/` lists blockers with counts and a conversion order whose first entry has no callees inside the tree.
34. `convert` on a class with only assigned attributes and an `__init__` produces a record, shows the diff, waits, and leaves the file unchanged on decline.
35. `report` shows coverage with denominator, effect inventory, boundary map, trust, debt, hotspots, and a trend with two points after two snapshots.
36. `check` run twice on a large project, the second time after a one-line change, finishes well under a second the second time.

**Editor, packaging, later milestones**

37. Typing `total += x` inside a region shows PAL101 within a second and the quick fix rewrites the enclosing loop to a fold.
38. A consumed package's verification claim lists Checked, Trusted, and Unsafe surfaces; a changed dependency forces rechecking before reuse.
39. A builder that escapes, retains an input alias, or is used after finalization fails; its finalized result is stable data.
40. A task that captures a builder fails; `par_map` without a `Tasks` capability fails; with one, results are deterministic for a pure function.
41. `memoize` on an `@effects(IO)` function fails PAL350.
42. A `with fun:` region that reads a host binding later reassigned in the host fails; one that reads stable host inputs and returns an immutable value passes.
43. `# mode: fun+syntax` source with `val` and `|>` is rejected by `check` untranslated; `build` produces inspectable Python whose contracts equal the compatible-edition equivalent, and a diagnostic in it points at the authored line.

## Non-goals

1. **Not a security sandbox.** Hostile source, native code, interpreter modification, and artifact tampering need a different product. The guarantee covers the supported workflow and exposes its trust conditions.
2. **Not certification of arbitrary Python.** Unknown behavior is rejected or made visibly unsafe. The checker does not guess.
3. **Not a replacement type checker.** It checks bindings, mutation, effects, failure, and exhaustiveness. It consumes type information for dispatch and does not check types for their own sake.
4. **Not whole-program enforcement.** Code outside a boundary is never checked, changed, or slowed.
5. **Not a new language in the compatible edition.** The compatible edition is a durable product. The syntax edition is optional and nothing depends on it.
6. **Not automatic parallelization, laziness, or termination proof.** `par_map` and `Seq` exist as explicit tools; nothing happens behind the developer's back.
7. **Not a transparent layer over mutable frameworks and data libraries.** Arrays, tables, sessions, and live views need adapters or stay outside.
8. **Not a replacement for tests or domain validation.** Functional contracts are not business correctness.
9. **Not a mandate for point-free style.** Named bindings, ordinary branching, declared exceptions, and an effectful shell are good code.
10. **Not zero overhead.** Costs are measured and published; disabling checks is never presented as keeping the guarantee.
11. **Not a hosted service.** Files, CLI, editor, CI.

## Assumptions and resolved ambiguities

1. **"Enforces" means a blocking contract within declared boundaries.** Rejected: an advisory linter whose marked regions execute anyway.
2. **"Functional programming" means practical, eager, typed functional Python.** Rejected: recreating Haskell's evaluation and inference.
3. **Ordinary assignment is `val` inside the mode; there is no `val` keyword in the compatible edition.** Rejected: a preprocessor-enforced `val` on day one. It survives as optional syntax.
4. **Literals keep Python's meaning in the compatible edition and are rejected in strict code.** Rejected: silently reinterpreting `[...]` as a persistent collection, because the result depends on whether a loader is active and that is the surprise the mode exists to remove.
5. **Functions and modules are the boundaries; a constrained `with fun:` arrives last; comment-delimited blocks never.** Rejected: blocks without scope rules.
6. **Unknown behavior fails closed in Strict and is a tracked, propagating effect in Audit.** Rejected: a default profile where "pure" means "pure except for unknown calls."
7. **Deep stability includes observation and aliases.** Rejected: setter suppression, frozen shells, and read-only views as proof.
8. **Trust is visible.** Confirmed manifest entries make callers Trusted, not Checked. Rejected: a wrapper or a cast that erases trust.
9. **The checker needs resolved types at dispatch sites and gets them from inference and the project's type checker.** Rejected: both "no type information needed" and "we build a type checker."
10. **`for` is admitted from the first milestone with per-iteration bindings; `while` is not in the pure core.** Rejected: deferring loops for most of the roadmap.
11. **Floats are admitted from the first milestone.** The guarantee already excludes cross-machine bitwise identity.
12. **The runtime validates at entry and audits effects; it does not make foreign objects immutable in place.** Rejected: boundary freezing of built-in containers, which CPython cannot do honestly.
13. **The target is modern Python with structural pattern matching.** Variants without exhaustive `match` are not worth shipping.
14. **Everything is local and in CI.** Rejected: a hosted dashboard.

## Feasibility

Python ignores comments; its tokenizer preserves them, so a tool can read a directive, but only the tool enforces it. Decorators and `with` statements are valid syntactic boundaries whose presence proves nothing by itself. `val x = 42` is not Python grammar and needs translation. The import system's finders and loaders make specialized loading possible, but a loader cannot establish purity and is an implementation option, not the promise. ([Lexical analysis](https://docs.python.org/3/reference/lexical_analysis.html), [tokenize](https://docs.python.org/3/library/tokenize.html), [ast](https://docs.python.org/3/library/ast.html), [import hooks](https://docs.python.org/3/reference/import.html#import-hooks).)

Assignment rebinds a name; it invokes no setter, so `__setattr__` tricks cannot stop `x = 43`. `typing.Final` is advice to a type checker and is not enforced at runtime, nor does it freeze the referent. ([Execution model](https://docs.python.org/3/reference/executionmodel.html#binding-of-names), [Final](https://docs.python.org/3/library/typing.html#typing.Final).)

Frozen dataclasses guard field assignment and are documented as *emulating* immutability; they do not freeze contents. `MappingProxyType` reflects changes to its backing mapping. Operators and attribute access call user code through special methods and descriptors. ([Frozen instances](https://docs.python.org/3/library/dataclasses.html#frozen-instances), [MappingProxyType](https://docs.python.org/3/library/types.html#types.MappingProxyType), [Special methods](https://docs.python.org/3/reference/datamodel.html#special-method-names).)

Decorators and defaults evaluate at definition time, so checking must precede strict initialization. ([Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).) Loop targets persist after the loop and closures capture bindings, not values. ([The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement).)

Persistent collections exist in the ecosystem (`immutables`, Pyrsistent), making reuse credible; the product still owns the nested-data, alias, callback, ordering, and performance contracts. PEP 638 (syntactic macros) is Draft and the product does not depend on it.

Conclusion: a checker over valid Python plus checked entry points plus explicit conversions is feasible and sufficient for the compatible edition. The syntax edition is a translation step on top. Nothing here requires Python to change.

## Roadmap

Each milestone is usable on its own. Later milestones widen admitted behavior without weakening already verified code.

1. **Strict functions and modules.** `# mode: fun` and `@fun`; single assignment with branch initialization; `for` with per-iteration bindings; scalars (including float), tuples, frozensets; checked constants; a characterized pure-operation surface for them; rejection of mutable literals, ambient reads, dynamic constructs, and unknown calls; entry validation; `check`, `run`, `explain`, `regions`; PAL identifiers. *Done when:* reassignment and a clock read fail with both locations; a compliant price calculation runs; a list argument is refused at entry.
2. **Persistent collections and boundaries.** `Vector`, `Map`, `OrderedMap`, `Set`; the returning-operation vocabulary; `freeze`/`thaw`; nested-path diagnostics; borrowed-escape rule; ordering rules; the discarded-update diagnostic. *Done when:* several versions derive from one vector, the foreign source of a snapshot is mutated, and every earlier strict value is unchanged.
3. **Records, variants, Option, Result.** `@record`, `replace`, `@variant`, exhaustive `match`, `Option`/`Result` with combinators, validation accumulator, acceptance of qualifying frozen dataclasses and named tuples, value interchange. *Done when:* a nested mutable field fails with its path and adding a variant case flags incomplete matches.
4. **Explicit effects and failure contracts.** `@effects`, capabilities as parameters, propagation through callbacks, failure as a contract dimension, controlled capabilities for tests. *Done when:* a reporting workflow combines a pure core with explicit `Clock` and `IO`, and an effectful callback fails inside a pure context.
5. **Standard-library manifests.** Built-in confirmed manifests for text, numbers, `re`, `json`, `datetime`, `itertools`, `functools`, paths, files, time, randomness, environment; initialization versus invocation evidence. *Done when:* a data-processing command freezes input, transforms purely, and writes output with every effect and trust visible.
6. **Third-party manifests and adapters.** Manifest format, package-shipped and project manifests, precedence and overrides, `manifest draft` with drafted/confirmed status, version binding and invalidation, adapters, the certification summary. *Done when:* one existing library operation is admitted with its trust visible to callers and a version bump invalidates it.
7. **Policy, baseline, ratchet.** Policy file with per-path levels and rules, unsafe-region and ignore-directive governance, exceptions with owner and expiry, `baseline` and the ratchet, CI output modes, change review report. *Done when:* an automated check rejects an expired exception, a new trust assumption, a file relaxing package policy, and a baseline growth.
8. **Supported execution.** `run` with freshness, dependency pinning, the effect audit with end-of-run report and policy gating, dynamic-construct guard, overhead reporting. *Done when:* an undeclared third-party I/O appears in the audit with its stack and the run can be made to fail on it.
9. **Editor and tests.** Inline diagnostics, contract and evidence hovers, quick fixes for every mechanical rewrite, "make this `fun`", consequence previews, property-test helpers, purity-gated `memoize`. *Done when:* a new Python developer resolves binding, nested-mutation, and effect errors from the editor and runs a deterministic integration test.
10. **Incremental checking and migration assistant.** Sub-second rechecks after small edits; `ready` with score, blockers, and leaf-first order; `convert` with diff, confirmation, and recheck. *Done when:* one legacy module is promoted following the suggested order and the second `check` on a large project finishes well under a second.
11. **Reports and verification claims.** `report` with coverage, inventory, boundary map, trust, debt, hotspots, trend, publishable page; `build` producing artifacts with verification claims; consumer-side claim inspection and freshness. *Done when:* a consumed package shows Checked, Trusted, and Unsafe surfaces and a changed dependency forces rechecking.
12. **Ownership, builders, lazy sequences, performance.** Transient builders with escape and finalization rules; replayable `Seq`; `Decimal` with explicit context and other numeric contracts; published cost behavior. *Done when:* a bulk transformation produces stable output and leaking a builder, reusing a finalized alias, or returning a bare generator fails.
13. **Concurrency.** `Tasks` capability, immutable messages across tasks, `par_map`, controlled scheduler for tests, rejection of shared transients and foreign mutable captures. *Done when:* a multi-task workflow exchanges stable values with cancellation and I/O visible, and sharing a builder is rejected.
14. **Inline regions and the syntax edition.** `with fun:` under its constraints; `# mode: fun+syntax` with `val`, immutable literals, `|>`, and `_`; translation through `build` with authored-source diagnostics; formatting, navigation, packaging, and migration support. *Done when:* the same program in both editions has equivalent contracts and results, a dialect error points at the authored line, and an inline region that reads a reassigned host binding fails.

## Success measures

Targets for validation, not results:

- A developer protects a useful pure function within fifteen minutes of starting the quick guide.
- Three quarters of introductory binding, mutable-value, and effect violations are fixed from the diagnostic alone.
- A team adopts one strict boundary without touching unrelated code.
- Every purity claim shows its evidence; every unsafe region and trust assumption is discoverable in one report.
- The regression suite covers indirect mutation, aliases, rebound globals, implicit dispatch, callback effects, definition-time effects, hash-order leakage, and stale evidence.
- Representative workloads have published cost behavior including `freeze` and retained versions.
- Library consumers enforce the same contract the author published.
- Change reports catch lost coverage and added trust, not only lower counts.

## Questions to validate before later milestones

1. Which immutable constructor spelling (`Vector.of(...)`, `vec(...)`, or another) is easiest to learn, and which update names best prevent ignored results?
2. Which effect distinctions help real applications without making public declarations unwieldy? Is `State` one family or several?
3. Which standard-library and third-party manifests make one strict module valuable in the target users' existing applications?
4. Should declared exceptions be first-class in the default failure policy, or an optional stricter profile once `Result` workflows are mature?
5. How much local type inference stays predictable before public annotations become the clearer experience?
6. What specific inline workflow cannot be expressed with a local `@fun` function, and does `with fun:` as constrained here serve it?
7. Does the syntax edition improve daily readability enough to justify its tooling and migration cost?
