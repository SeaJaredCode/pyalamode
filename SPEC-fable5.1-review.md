# Review of the four pyalamode specifications

**Reviewer:** Claude Fable 5.1, 2026-10-08
**Inputs:** `SPEC_sol5.6.md`, `SPEC_sol6.1.md`, `SPEC_sol6.1-with-prev.md`, `SPEC_fable5.1.md`
**Criteria:** feasibility (can the stated promises be kept on CPython), consistency (does the document contradict itself), completeness (does it cover the product end to end with testable acceptance criteria)

One disclosure up front: `SPEC_fable5.1.md` was written by the same model lineage as this review. I evaluated it on the same terms as the others, and it does not win.

## Verdict

**Vote: `SPEC_sol6.1-with-prev.md`** is the best single document. It is the most feasible, the most internally consistent, and the most complete on the semantics that make the product's central promise true. It is already a synthesis of `sol5.6` and `sol6.1`, and it shows.

**A composite is better than any single spec**, and I have written one as `SPEC-fable5.1-composite.md`. The reason is that the four documents split cleanly into two camps that are each strong where the other is weak:

- `sol6.1` and `sol6.1-with-prev` get the **guarantee** right: fail closed, keep Python's literal semantics, separate purity from evidence, check definition-time behavior, treat implicit calls as calls. They are weaker on **tooling concreteness** and have usability gaps in their roadmaps (no `for` loops until milestone 11 in one, no floats until milestone 12 in the other).
- `fable5.1` gets the **developer experience** right: manifests with precedence and drafted/confirmed status, a baseline ratchet with precise rules, a leaf-first migration assistant, incremental checking, concrete reports. It is weaker on the **guarantee**: it reinterprets collection literals while claiming stock-interpreter equivalence, lets unknown calls through as warnings in the default profile, promises a runtime guard it cannot build, and declares itself "not a type checker" while depending on type information.
- `sol5.6` is a good, concise earlier draft that `sol6.1-with-prev` supersedes on nearly every axis.

The composite takes the semantic spine of `sol6.1-with-prev`, fixes its two roadmap gaps, and grafts on the tooling design from `fable5.1` after correcting the four guarantee problems above.

## Scorecard

| | sol5.6 | sol6.1 | sol6.1-with-prev | fable5.1 |
|---|---|---|---|---|
| Feasibility | Good, one loader-dependent claim | Very high, two over-claims | Very high | Medium, four over-claims in core promises |
| Consistency | Medium-high, one self-questioned decision | High | High | Medium, four internal tensions |
| Completeness: semantics | Medium | Very high | Very high | Medium |
| Completeness: tooling and DX | Medium | Medium | Medium-high | Very high |
| Acceptance criteria | Prose bullets, adequate | 28-row scenario table, excellent | 35 numbered, testable | 17 numbered, most concretely testable |
| Milestone 1 usefulness | Good | Marginal (scalars only, closed op set) | Good | Good |
| Roadmap usability gaps | Collections and records bundled in M2 | Floats at M12, effects at M7 | `for` loops at M11 | None, but several milestones rest on infeasible claims |
| Feasibility analysis with sources | Yes | Yes, with code examples | Yes, best of the four | None |
| Overall | 3rd | 2nd | **1st** | 4th on guarantee, 1st on DX |

## Where the four agree

The agreement is substantial and should be treated as settled for the composite:

1. The first edition is valid Python syntax. `val x = 42` is deferred to an opt-in syntax edition that requires translation. All four reject it for the compatible edition, for the same reason: it duplicates a rule the mode already enforces and breaks every Python tool.
2. Ordinary assignment inside the mode is a single binding. Augmented assignment, `del`, `global`, and `nonlocal` are rejected. Mutually exclusive branches may each initialize a name once.
3. Immutability is transitive. A frozen outer record containing a list is not immutable. Diagnostics report the nested path.
4. Functions are pure by default inside the mode and declare effects; effects propagate to callers and through callbacks.
5. Module directive plus function decorator are the opt-in surfaces. Arbitrary comment-delimited blocks are rejected because Python blocks are not scopes.
6. Audit or lenient mode exists for migration and never confers a guarantee. Baselines record debt without certifying it.
7. Interop is explicit and granular. Unsafe regions carry a reason and appear in reports.
8. No hosted service, no accounts. Everything lives in files in the repository.
9. Not a security sandbox. Not a termination prover. Not automatic parallelization.

## Where they disagree, and which side is right

### 1. Do collection literals change meaning inside the mode?

- `sol5.6` (line 147, 411) and `fable5.1` (line 101-105): yes, `[1, 2, 3]` in a strict region is a persistent Vector.
- `sol6.1` (line 69, 235) and `sol6.1-with-prev` (line 15, 269): no, `[]` stays a list and is rejected in pure code; use an explicit constructor.

**The no side is right for the compatible edition.** Reinterpreting a literal requires an import hook or source transform to be active at load time. `fable5.1` says on line 24-25 that `fun` code "runs on a stock interpreter" and on line 103-105 that "behaviour is identical either way," but acceptance criterion 4 (line 376-377) requires that the literal "produces a value that raises on `.append` from ordinary code" with only the runtime installed. Those cannot all be true: with the hook active, ordinary code receiving the value cannot mutate it; without the hook, it can. That is a behavior difference, and it is exactly the class of hidden-mechanism surprise `sol6.1` warns about on line 63. `sol5.6` half-acknowledges the problem by listing its own decision as open question 1 (line 498). The syntax edition can change literal semantics openly, since it already requires translation.

### 2. What happens on a call with no contract?

- `fable5.1` (line 146-147, 449-451): a warning in the default `standard` profile, an error only in `pure`.
- The other three: fail closed in strict mode, always.

**Fail closed is right.** `fable5.1` says on line 138 that a function in a region "performs no effect," then on line 146 lets an `unknown` call through as a warning. In the default profile, "pure" therefore means "pure except for calls we know nothing about," which is the convention-based state of affairs the product exists to replace. `fable5.1`'s adoption argument (line 449-451: erroring everywhere "would block a first run on any project with a dependency") is real, but the other specs already solve it with Audit mode plus baselines, which keeps Strict meaning strict. The good idea buried in `fable5.1`'s approach is worth keeping: `unknown` should be a *tracked, propagating* effect in Audit mode so the uncertainty is visible all the way up the call graph. The composite does that.

### 3. How much can a runtime guard do?

- `fable5.1` (line 247-260): values entering a region "become read-only on entry"; a region's bindings are "watched" for rebinding via `exec` or reflection; an effect audit records undeclared effects.
- `sol6.1` (line 59, 206-210, 497) and `sol6.1-with-prev` (line 153-155, 361-363): runtime validates inputs at checked entry points and rejects unsupported values; it does not make arbitrary objects immutable.

**The narrow reading is right.** CPython offers no way to make an existing `list` read-only in place while ordinary code still holds the same reference. `fable5.1`'s own non-goal on line 420-421 concedes that "Python offers no cheap way to make that promise honestly," then acceptance criterion 8 (line 384-385) promises it anyway. The feasible version is: checked entry points reject mutable or unrecognized inputs unless the caller passes them through `freeze`, which produces an independent snapshot; after that, third-party mutation of the original is irrelevant. The effect audit (monkeypatching I/O primitives in a dev run to record undeclared effects) is feasible and valuable as an audit tool for catching manifest mistakes. The composite keeps that and drops in-place freezing.

### 4. Does the checker need type information?

- `fable5.1` (line 413-416): "Not a type checker," runs beside whatever type checker the project uses.
- `sol6.1` (line 55, 297, 453) and `sol6.1-with-prev` (line 345-347, 662): dispatch-sensitive checks need resolved callee identity; `Any` or an unresolved callable fails closed.

**The rigorous side is right, and `fable5.1` is inconsistent here.** `fable5.1` detects mutation by "the known mutating methods of the built-in types" (line 106-109) and resolves callees against manifests (line 146). Both require knowing what `xs` in `xs.append(1)` actually is. A method-name match is a heuristic, and `sol6.1-with-prev` line 175 is right that the product "must not rely on regex checks." Neither `sol6.1` spec addresses `__add__`, properties, iterators, `__str__`, or context-manager protocol with effects as a side issue; they treat implicit calls as calls (`sol6.1-with-prev` line 345, acceptance 19; `sol6.1` acceptance row "A custom `__add__`..."). `fable5.1` never mentions implicit calls. The honest position, which the composite takes, is: the product is not a replacement for mypy or pyright, but it does need resolved types at dispatch sites, which it gets from local inference and from the project's type checker's output, and an unresolved target fails closed in Strict.

### 5. Loops

- `sol6.1-with-prev` (line 193, 619-623): statement loops are excluded from the initial strict subset and arrive in milestone 11.
- `sol6.1` (line 169-170): `for` admitted from the start with per-iteration bindings; `while` unsupported in the pure core.
- `fable5.1` (line 87-91): `for` admitted; `while` warns in standard, forbidden in pure.
- `sol5.6` (line 114, 234): `for` admitted when no mutable accumulator escapes.

**Admit `for` in milestone 1.** The rule is simple and all three other specs state it the same way: loop target and body-local names are fresh per iteration, cannot be read after the loop, and cannot be loop-carried. Deferring that for ten milestones is `sol6.1-with-prev`'s one real usability mistake and sits badly with its own "Python familiarity" principle. `while` is correctly excluded from the pure core by `sol6.1` and `fable5.1`: a terminating `while` depends on a binding changing.

### 6. Floats and numerics

`sol6.1` line 179 starts the scalar set at `None`, bool, int, str, bytes, and defers "other numeric types" to milestone 12 (line 488). Its own examples price everything in cents (line 83), which suggests the authors noticed. The other three admit floats implicitly. **Admit float in milestone 1.** The guarantee already excludes cross-machine bitwise identity (`sol6.1` line 41), so there is no soundness reason to wait. `Decimal` is the interesting case because it reads an ambient context; `sol6.1-with-prev` line 313 correctly lists "implicit numerical context" as a prohibited read, so `Decimal` needs an explicit-context contract.

### 7. Inline regions

- `fable5.1` (line 73, 453): `with fun:` is a first-class region marker from milestone 1, with no scope rules stated.
- `sol6.1` (line 114-130, 489): `with fun:` is a limited inline region with explicit constraints (no new scope, only stable immutable host inputs admitted, names cannot reuse a host binding, closures cannot escape, no direct module-global reads) delivered in milestone 13.
- `sol6.1-with-prev` (line 501, 641) and `sol5.6` (line 88): out of the XL scope entirely.

**`sol6.1`'s treatment is right.** `fable5.1` says "a name is bound once per scope" (line 81) but a `with` block is not a scope, so a name bound before the block and again inside it is undefined behavior in that spec. `sol6.1` wrote the constraints that make the block honest. Since the original ask apparently mentioned inline blocks, the composite keeps the `sol6.1` version as a late milestone rather than dropping it.

### 8. Effect declaration form

`fable5.1` uses strings (`@effects("io")`); `sol5.6` and `sol6.1-with-prev` use importable names (`@effects(IO, Clock)`). Importable names win: a typo in a string is silent, a typo in a name is an import error. `fable5.1`'s `mutate` effect (changes an object it did not create) is a useful addition the others express as a manifest field; the composite keeps it as a manifest field rather than a declarable effect, since strict code should never declare it.

### 9. Failure and exceptions

`fable5.1` toggles `raise`/`try` by profile. `sol6.1-with-prev` (line 349-355) treats failure as a separate contract dimension from effects, prefers `Result`, lets policy require value-based failure on selected public APIs, and notes that handling a failure does not erase effects already performed. `sol6.1` adds that exception instances, tracebacks, and cleanup behavior must not leak into the value domain. **The contract-dimension model is right** and subsumes the profile toggle.

## Per-spec findings

### SPEC_sol5.6.md

The most readable of the four and the one with the crispest principles list (line 13-22) and information architecture (six areas, line 44-68). Its three-level enforcement (Off/Audit/Strict, line 90-96) and four trust states (line 240-245) are the vocabulary the later specs refined.

Problems:
- Principle 4 (line 18, "valid Python syntax wherever it can") is in tension with line 147 and assumption 5 (line 411), which give literals new runtime meaning. Open question 1 (line 498) then asks whether to do that at all. A spec should not list its own core decision as open.
- Milestone 2 (line 432-434) bundles persistent collections, transitive record immutability, copy-with-changes, equality, and pattern matching into one increment. The other specs split this into two.
- No named conversion functions, no command vocabulary, no concrete collection API. "Explicit conversion" (line 163) is left unnamed.
- Milestone 14 (line 480-482, "ecosystem governance") is the least concrete milestone in any of the four documents.
- Does not address definition-time effects (decorator and default evaluation), implicit calls through dunder methods, ordering of unordered collections, or stale verification. All four of those appear in the `sol6.1` pair.

It is a solid draft, and nearly every good thing in it survives into `sol6.1-with-prev`.

### SPEC_sol6.1.md

The most rigorous on soundness. Its best contributions, none of which appear in `fable5.1`:
- The checker must not execute or import unverified source to learn its behavior (line 65, acceptance row on line 467).
- Verification and purity are separate; an effectful operation can be verified against its declared effects (line 51).
- Unordered collections cannot leak insertion or hash order into order-sensitive computation; ties need a tie-breaking contract; float reduction is not automatically order-independent (line 239-245). This is the only spec that gets reproducibility of map iteration right.
- An `int` annotation does not admit a subclass with effectful arithmetic (line 206).
- Cached verification is invalidated by any change to code, rules, policy, or dependency contracts (line 420).
- `with fun:` with real constraints (line 114-130).
- The 28-row acceptance table (line 438-467) is the best acceptance artifact in the set.

Problems:
- Milestone 1 (line 477) is "checked scalar functions" with "a small closed vocabulary of pure operations." The spec claims it stands alone, but a function that can only use a closed set of scalar operations is a demo, not a protected pricing module. Compare `sol6.1-with-prev` milestone 1, which includes tuples, checked constants, and module opt-in.
- Floats arrive in milestone 12 (line 179, 488). See disagreement 6.
- Effects arrive in milestone 7 (line 483). The functional-core-with-ordinary-shell pattern on line 316-320 does cover the gap, so this is a sequencing preference rather than an error, but six milestones without `@effects` is long.
- Line 183: verified function values "are not ordinary Python function objects that users may inspect or modify." CPython cannot enforce that. The achievable claim is that the checker rejects inspection or modification inside verified regions and the runtime pins identity at entry.
- Line 305: the product "preserves the approved dependency or rejects the changed environment." Detecting a monkey-patched dependency at runtime is feasible only by identity checks at checked entry points, which the spec does not say.
- Diagnostics (line 374-392) have no stable rule identifiers. Both `sol5.6` and `sol6.1-with-prev` have `PAL###` IDs, and `fable5.1` has rule names; a baseline needs stable identities (`sol6.1-with-prev` line 452).
- Dense and repetitive. Several paragraphs restate "an annotation is not evidence" in slightly different words.

### SPEC_sol6.1-with-prev.md

The winner. It carries forward everything right about `sol6.1` and adds the readability and vocabulary of `sol5.6`. Distinctive contributions:
- The authoring-form table (line 75-83) is the clearest statement in any of the four about what each Python surface can and cannot express, and why `val` needs translation.
- The definition-time analysis (line 357-363): decorators and defaults run while Python defines the function, so a runtime wrapper cannot retroactively prevent effects that already happened. This is correct and important, and only this spec states it.
- The observation (line 315) that an integer global is immutable while its *binding* can be reassigned elsewhere, so a global is not a stable constant merely because its current value is an int.
- Citing `immutables` and Pyrsistent as credible reuse (line 95) while keeping selection as engineering work.
- Four-state evidence (Checked/Trusted/Unsafe/Unchecked, line 138-143) is the cleanest formulation across the set.
- Effects in milestone 4 (line 577), earlier than `sol6.1`.
- 35 numbered acceptance criteria (line 505-555), each checkable.

Problems:
- `for` loops are excluded until milestone 11 (line 193, 619-623). See disagreement 5. This is the one change the composite makes to its core.
- Inline regions are removed from XL scope entirely (line 501, 641). The composite restores `sol6.1`'s constrained version as a late milestone.
- The relationship between `@effects(IO, Clock)` and the `clock, output` parameters in the example (line 328-333) is not stated. Are capabilities always explicit parameters? The composite says yes.
- Collection naming is slightly inconsistent: `seq(...)` constructor but `ImmutableSeq[str]` type (line 257, 287). `sol6.1`'s `Vector`/`Map`/`Set`/`OrderedMap` is cleaner.
- Starred unpacking is rejected because it produces a list (line 189) without offering the obvious alternative, which is to have `*rest` produce a Vector.
- Length. At 689 lines it could lose a fifth without losing content.

### SPEC_fable5.1.md

The best developer-experience document and the weakest on the guarantee. What it contributes that none of the others has in usable form:
- **Manifests** (line 153-168): per-package, per-operation declarations of purity, effects, and argument mutation; precedence project override > shipped > built-in > unknown; a drafting tool whose output is marked unconfirmed entry by entry; a certification summary for library authors. This is the concrete form of what the other specs call "reviewed contracts" and "adapters," and it is better than any of their descriptions.
- **Baseline and ratchet mechanics** (line 287-289): `baseline` can be re-recorded only when the count went down unless a policy owner forces it, and the force is recorded. Acceptance criterion 9 makes this testable.
- **Migration assistant** (line 311-322): `ready` produces a score, blockers by rule, uncontracted external calls, and a leaf-first conversion order; `convert` applies mechanical rewrites with a diff and confirmation. Acceptance criteria 11 and 12.
- **Reports** (line 293-309): purity coverage, effect inventory with "rim thickness," boundary map, mutation hotspots as conversion candidates, debt with justifications, trend across snapshots.
- **Incremental checking** as a milestone (line 230-231, 493-494) with a testable target (acceptance 17).
- Purity-gated `memoize` (line 242-243, acceptance 16), `par_map` as the practical payoff of purity, property-test helpers generated from record declarations (line 500-501).
- The borrowed-escape rule (line 184-188): a borrowed mutable value stored into a record or returned without freezing is a checker error. Good, and static.
- Acceptance criteria that read like test cases (line 370-403).

Problems, in order of severity:
1. **Literal reinterpretation versus stock-interpreter equivalence** (line 24-25, 103-105, 239, 376-377). See disagreement 1. Unresolvable as written.
2. **Guard boundary freezing** (line 252-253, 384-385) is infeasible for built-in containers already referenced by ordinary code. See disagreement 3. The spec's own non-goal (line 420-421) says as much.
3. **Unknown calls warn in the default profile** (line 146-147), contradicting pure-by-default (line 138). See disagreement 2.
4. **"Not a type checker"** (line 413-416) versus mutation detection by method name (line 106-109) and manifest callee resolution (line 146). See disagreement 4. The spec never mentions implicit calls through operators, properties, or protocols, which the `sol6.1` pair treat as central.
5. `with fun:` has no scope rules (line 73, 81). A name bound before the block and inside it is undefined.
6. `yield` in a region produces a "single-pass" value "consumed once" (line 173-175) with no enforcement story. `sol6.1` line 303 and 340 correctly treat generators as stateful unless they satisfy a replayable contract.
7. No treatment of definition-time effects, ordering of unordered collections, trust visibility in results (a call through a confirmed manifest entry should make the caller visibly Trusted, not Checked), or freshness of cached verification.
8. No feasibility analysis or citations. The other three each ground their design in Python's documented behavior.

The scope note (line 3-8) is useful context the others lack: it records that the brief had web-app constraints and how they were reinterpreted.

## What the composite does

`SPEC-fable5.1-composite.md` is a full specification, not a diff. Its decisions, with sources:

| Decision | Taken from | Change made |
|---|---|---|
| Three properties (binding, value, purity) and four-state evidence | sol6.1-with-prev | none |
| Off/Audit/Strict enforcement | sol5.6, sol6.1-with-prev | `unknown` becomes a tracked, propagating effect in Audit (fable5.1's idea, relocated) |
| Compatible edition keeps literal semantics; mutable literals rejected in strict code | sol6.1, sol6.1-with-prev | add a quick fix that rewrites `[...]` to `Vector.of(...)` |
| `for` loops with per-iteration bindings | sol6.1, fable5.1 | admitted in milestone 1, not 11 |
| `while` excluded from pure core | sol6.1, fable5.1 | none |
| Floats admitted from milestone 1; Decimal needs explicit context | sol5.6, sol6.1-with-prev | stated explicitly |
| Checker never executes source; definition-time checking | sol6.1, sol6.1-with-prev | none |
| Implicit calls are calls; unresolved dispatch fails closed | sol6.1, sol6.1-with-prev | none |
| Type information: not a replacement type checker, but consumes one | fable5.1 non-goal, sol6.1 assumption | reconciled |
| Ordering and hash-randomization rules | sol6.1 | none |
| Freshness invalidation of cached verification | sol6.1 | none |
| `Vector`, `Map`, `Set`, `OrderedMap`, `freeze`, `thaw` | sol6.1, fable5.1 | `replace(record, **changes)` as a free function, mirroring dataclasses |
| Records and sealed variants; `Option`/`Result` with combinators; exhaustive match | all four | fable5.1's combinator list |
| Effects as importable names; capabilities as explicit parameters | sol5.6, sol6.1-with-prev | parameter relationship stated |
| Failure as a separate contract dimension | sol6.1-with-prev | none |
| Manifests: precedence, drafted/confirmed, drafting tool, certification summary | fable5.1 | drafted entries are Unknown in Strict; confirmed entries make callers Trusted, not Checked |
| Borrowed-escape rule | fable5.1 | kept as a static check; in-place freezing dropped |
| Guard: entry validation, effect audit, dynamic-construct rebinding detection | fable5.1 scope, sol6.1 limits | boundary freezing removed |
| Policy, baseline, ratchet rules | fable5.1 mechanics, sol6.1-with-prev policy dimensions | profiles replaced by Audit/Strict plus per-path rule settings |
| Migration assistant (`ready`, `convert`) | fable5.1 | none |
| Reports | fable5.1 | add verification claims and trust changes from sol6.1-with-prev |
| Incremental checking milestone | fable5.1 | none |
| `with fun:` with constraints, late milestone | sol6.1 | none |
| Syntax edition with `val`, pipeline, placeholder, immutable literals | fable5.1, sol6.1-with-prev | none |
| Transient builders with ownership rules | sol5.6, sol6.1, sol6.1-with-prev | none |
| Concurrency as explicit effects; `par_map` lives here | sol6.1-with-prev, fable5.1 | `par_map` requires a Tasks capability |
| Feasibility section with sources | sol6.1-with-prev | condensed |
| Acceptance criteria as numbered scenarios | sol6.1 table, fable5.1 concreteness | merged |

## If you do not want a composite

Adopt `SPEC_sol6.1-with-prev.md` and make three edits: move `for` loops with the per-iteration rule into milestone 1; restore `sol6.1`'s constrained `with fun:` region in milestone 14 alongside the syntax edition; and replace the "Third-party adapters" milestone's prose with `fable5.1`'s manifest design (lines 153-168, 483-485) and its baseline ratchet rules (lines 287-289). That gets you most of the composite's value in about forty lines of change.
