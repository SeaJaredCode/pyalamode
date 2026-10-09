# Pyalamode: review of the four specifications

**Date:** October 8, 2026; revised October 9, 2026  
**Assessment:** Feasibility, internal consistency, and completeness of the proposed product contract.

**Revision:** The composite now uses strict static checking/building with ordinary CPython execution. A runtime gate is not required for a strict static contract; optional boundary guards provide a separately stated validation guarantee. This changes the recommended execution architecture, while retaining the ranking of the original four documents.

## Recommendation

**My vote is `SPEC_sol6.1-with-prev.md`.** It is the best overall foundation: it preserves accepted Python semantics, gives purity a credible enforcement boundary, treats external trust honestly, and declines to make inline blocks part of the core promise. It also catches important problems involving loop captures, definition-time effects, mutable aliases, and migration baselines.

**A selective composite is better than adopting any of the four unchanged.** Use that specification's direction and scope discipline; add `SPEC_sol6.1.md`'s stronger treatment of ordering, observable identity, verification freshness, and a scalar-function first milestone. Preserve the approachable commands and diagnostic style from `SPEC_fable5.1.md`, and the separation of audit from strict enforcement articulated well in `SPEC_sol5.6.md`.

The resulting proposal is [SPEC-sol6.1-composite.md](/Volumes/Projects/pyalamode/SPEC-sol6.1-composite.md). It is a replacement product contract, with explicit decisions, a bounded initial language, and release gates. Its default enforcement happens at check/build time; accepted code runs on stock CPython with ordinary immutable-library support and optional boundary guards. It does not combine all four feature lists or inherit their runtime-enforcement commitments unchanged.

If selecting exactly one existing document is preferable, select **`SPEC_sol6.1-with-prev.md`**, then resolve the execution, trust, and ordering questions below before implementation.

## Comparison

The ranking evaluates what each document actually promises. A shorter implementation obtained by quietly weakening those promises does not count as feasibility. Completeness means resolving consequential product decisions, rather than mentioning the most features. These are qualitative judgments, not measured engineering estimates.

| Rank | Specification | Feasibility | Consistency | Completeness | Assessment |
| --- | --- | --- | --- | --- | --- |
| 1 | [SPEC_sol6.1-with-prev.md](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md) | Best overall; still substantial language engineering | Strongest scope and Python-semantics discipline | Strong product and team workflows; several engineering contracts remain open | Best base |
| 2 | [SPEC_sol6.1.md](/Volumes/Projects/pyalamode/SPEC_sol6.1.md) | Strong initial subset; heavier eventual commitments | Strong central guarantee; loop and inline-region edges need tightening | Most complete treatment of value observations, ordering, and freshness | Best source of semantic additions |
| 3 | [SPEC_sol5.6.md](/Volumes/Projects/pyalamode/SPEC_sol5.6.md) | Plausible if treated as a compiler-assisted semantic edition | Good principles; transformation and evidence details remain ambiguous | Broad product coverage; fewer operationally precise rules | Good direction, needs a firmer language contract |
| 4 | [SPEC_fable5.1.md](/Volumes/Projects/pyalamode/SPEC_fable5.1.md) | Attractive checker/runtime portions; several guarantees cannot be delivered as described | Material contradictions between literal semantics, execution, and runtime protection | Clearest everyday interface; weakest account of difficult semantics | Salvage the experience, not the guarantee model |

The top two are close. The standalone 6.1 document wins on several individual semantic topics. The `with-prev` document wins overall because it avoids extra execution models and is clearer about the difference between restricting accepted Python and changing Python's scope behavior.

## 1. SPEC_sol6.1-with-prev.md

### Why it wins

Its most valuable decision appears immediately: accepted compatible-edition expressions keep their Python meaning, and mutable literals are rejected rather than relabeled. That removes the need to make a hidden compiler responsible for ordinary collection syntax. Its [boundary and execution model](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md:97) also distinguishes unmanaged Python execution from supported strict execution without pretending a comment enforces anything.

It handles several traps the other drafts miss or describe less accurately:

- Its [iteration rules](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md:191) explicitly acknowledge Python's actual loop binding behavior and forbid escaping closures over changing loop bindings.
- Its [snapshot rules](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md:230) treat reading foreign mutable data as a boundary operation, including inconsistent concurrent snapshots.
- Its [definition-time section](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md:357) recognizes that a decorator cannot undo effects from defaults or other evaluation that already happened.
- Its [migration policy](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md:446) tracks finding identity, lost strict coverage, and new trust, rather than only declining diagnostic counts.
- Its [syntax edition](/Volumes/Projects/pyalamode/SPEC_sol6.1-with-prev.md:487) leaves inline lexical regions to a separate proposal. That is sensible scope control.

The document also gives useful attention to fake capabilities retaining their effects, guarded patterns not establishing exhaustiveness, and private mutation being a separate ownership feature. These distinctions make acceptance criteria more credible.

### What still needs resolution

**Evidence propagation needs one precise rule.** The checked/trusted/unsafe/unchecked table is useful, but a checked wrapper can depend on trusted behavior. The public result should show both facts: checked source, with these transitive trust assumptions. Otherwise “checked” can conceal the trust underneath it. The standalone 6.1 draft makes caller propagation more explicit.

**Unsafe execution must not become an alternate route to a strict certificate.** The document permits unsafe requirements to propagate, while strict execution blocks unsupported behavior. Define whether such a function is runnable integration code, a verified effectful function, or unverified. My choice is to keep uncharacterized adapters outside certified strict code. A project may run an ordinary shell around strict exports, but the shell receives no functional certificate.

**Ordering needs a stronger observational contract.** Saying order-dependent operations require ordered inputs is correct, but leaves implicit iteration, formatting, encoding, error selection, and folds underspecified. Borrow the standalone 6.1 rules, while using a narrow supported operation set instead of asking the checker to prove arbitrary reducers commutative.

**The initial milestone is still crowded.** Function and module adoption, tuples, constants, capture analysis, and execution freshness are all included at once. Split the first function-only release from module linking and richer values. The scalar first milestone in standalone 6.1 is a better starting point.

**Several later features are independent projects.** Ownership-safe transients, deterministic scheduling, artifact evidence, and a dialect each deserve gates. Calling fourteen milestones independently useful does not establish that their dependencies or effort are small.

These are refinements to a coherent foundation, rather than reasons to abandon it.

## 2. SPEC_sol6.1.md

### Its strongest contributions

The [guarantee section](/Volumes/Projects/pyalamode/SPEC_sol6.1.md:28) separates bindings, values, pure computations, effects, and evidence clearly. It also makes trusted integrations propagate to callers and rejects casts, ignores, and `Any` as substitutes for evidence.

Its [value-domain rules](/Volumes/Projects/pyalamode/SPEC_sol6.1.md:177) are the strongest of the four. Exact-type checks, immutable function captures, identity restrictions, hook-free conversion, cyclic-graph rejection, and no automatic argument conversion all close real holes. Its [ordering and equality rules](/Volumes/Projects/pyalamode/SPEC_sol6.1.md:239) identify a less obvious problem: equal unordered values can otherwise produce different ordered results. Its [freshness requirements](/Volumes/Projects/pyalamode/SPEC_sol6.1.md:416) make cached verification depend on code, policy, rules, and dependency evidence.

It also gives the best first-release shape: [checked scalar functions](/Volumes/Projects/pyalamode/SPEC_sol6.1.md:477), before modules, collections, external integrations, or syntax. This is the most credible way to prove the central idea cheaply.

### Why it is second

**Inline regions expand the proof boundary substantially.** The [inline example](/Volumes/Projects/pyalamode/SPEC_sol6.1.md:114) is more careful than Fable's block marker, and limited inline regions are possible in principle. The remaining rules still require analysis of the ordinary host: captures, earlier writes, later writes, host callbacks, repeated entry, and escaping results. In particular, “closures created in this region cannot escape” does not cover a closure created earlier in ordinary code that already captures a host cell. The meaning of output bindings after the block also needs a clear lifetime: does later ordinary reassignment invalidate a binding claim or simply end the block's claim? Extracting a strict function avoids this complexity.

**The `for` rule describes fresh logical bindings without explicitly closing the escaping-capture hole.** Python reuses its actual loop binding. A runtime-compatible restriction must reject an escaping closure over that cell or deliberately translate the scope. `with-prev` states this directly. This is an omission to repair, not evidence that every allowed loop is unsound.

**Order-independent operations need a tractable admission rule.** “Verified order-independent result” could imply proving algebraic properties of arbitrary callbacks, especially with failures and floating-point arithmetic. Initially permit specific characterized unordered operations and require explicit ordering for general traversal.

**The observable-equivalence promise needs a defined value relation.** Python `==` is insufficient by itself: `True == 1`, while `str(True)` and `str(1)` differ. Later float support must address signed zero and NaN. State equivalence in terms of the admitted type and value contract, not any pair of objects Python happens to compare equal.

**Milestone 12 bundles too much risk.** Replayable lazy values, ownership, additional numeric contracts, concurrency, and memoization each introduce different obligations. Move them behind separate extension gates. They should not delay a useful strict core.

The default refusal of external trust is defensible. It does mean the useful initial operation set and trusted runtime must be identified clearly; “no external trust” cannot mean no trust in Python or the collection implementation.

## 3. SPEC_sol5.6.md

### What works

This draft establishes the right broad product: a local toolchain, gradual adoption, distinct off/audit/strict states, deeply immutable data, effects through callbacks, and granular interoperability. Its [principles](/Volumes/Projects/pyalamode/SPEC_sol5.6.md:13) remain good design criteria. Rejecting arbitrary initial block regions is also a sound choice.

It acknowledges that comments require external tooling and that frozen records alone are insufficient. It makes readable Python control flow and an effectful application shell legitimate, rather than confusing functional programming with forbidding useful programs.

### What makes it less ready

**Its compatible edition is syntactically compatible, not runtime-semantics compatible.** [Immutable literal semantics](/Volumes/Projects/pyalamode/SPEC_sol5.6.md:145) and [fresh loop/branch bindings](/Volumes/Projects/pyalamode/SPEC_sol5.6.md:110) require transformations or equivalent restrictions. The draft consciously permits this in assumption 5, so it is not the same contradiction as Fable's library-only claim. However, the transformation pipeline, raw-source behavior, tooling expectations, and scope rules must become explicit product requirements. An AST-based implementation is plausible; it is a larger first product.

**Its evidence categories mix mechanism with assurance.** “Adapted” says how an operation is exposed, not whether its implementation and dependency assumptions are checked. A reviewed adapter can still invoke opaque code. Report adaptation separately from checked source and accepted trust.

**Effect handling is too loosely described.** The promise to distinguish an effect handled inside a boundary from one propagated needs semantics. Catching an exception can handle a failure; writing to a file cannot be made pure by “handling” it afterwards. Capabilities and controlled providers do not erase the effect either.

**Several essential assurances are implicit.** Definition-time effects, stable global bindings, native-operation trust, actual callable resolution, and stale verification need the precision present in the 6.1 drafts.

**The roadmap postpones functionality that earlier milestones already need.** Confined builders appear in core collection behavior, but ownership is milestone 11. Either exclude builders until that milestone or specify an earlier safe subset. The same discipline is needed for interop validation used before mature dependency contracts.

This is a good strategic specification. It needs more language and execution decisions before it is a good implementation basis.

## 4. SPEC_fable5.1.md

### What is worth retaining

This is the easiest draft to imagine using. `check`, `explain`, `regions`, `ready`, conversion previews, readable diagnostics, and local reports form an approachable workflow. Returning-operation names such as `appended` and `updated` communicate immutable updates better than an API that initially resembles a familiar mutator. Manifest drafts being visibly unconfirmed is a useful precaution.

Its concrete acceptance examples are also helpful. Preserve that style while changing the semantics those examples test.

### Blocking problems

**Literal semantics contradict the execution promise.** The [collection section](/Volumes/Projects/pyalamode/SPEC_fable5.1.md:102) says `[1, 2, 3]` produces a persistent vector, then says ordinary lists under plain execution behave identically. Acceptance criterion 4 requires the literal to reject external `.append` with only the library installed. The [runtime section](/Volumes/Projects/pyalamode/SPEC_fable5.1.md:240) and non-goals say no preprocessor is required. Ordinary Python list displays construct lists; installing a library does not change that operation. A custom loader or compilation step could change it, but that would require a different execution contract. The two behaviors are observably different. [Python list displays](https://docs.python.org/3/reference/expressions.html#list-displays).

**Read-only borrowing does not stop mutation through an existing alias.** The [boundary and guard promises](/Volumes/Projects/pyalamode/SPEC_fable5.1.md:184) say entry protection makes outside mutation impossible and reports the offending call. A read-only view cannot freeze another alias to an ordinary list or dictionary. A copied snapshot protects the computation, but allows the original to keep changing and therefore has different semantics. Python explicitly documents mapping proxies as reflecting backing changes. [MappingProxyType](https://docs.python.org/3/library/types.html#types.MappingProxyType).

**The runtime effect audit is overpromised.** Recording every undeclared effect in arbitrary third-party code is a universal observation claim. It would need coverage for ordinary state reads, implicit dispatch, and native behavior, not merely interception of familiar I/O. Audit hooks are a limited observation mechanism, and Python warns against treating them as a sandbox. The document's own non-security caveat does not establish the advertised complete effect coverage. Use bounded instrumentation for diagnostics and static refusal or explicit trust for guarantees. [Python audit hooks](https://docs.python.org/3/library/sys.html#sys.addaudithook).

**Unknown calls may pass the default profile while the product claims purity.** The [standard profile](/Volumes/Projects/pyalamode/SPEC_fable5.1.md:277) warns on unknown calls. That can be a useful migration mode, but its successful exit cannot confer a verified pure label. Split audit from strict.

**Single assignment does not automatically eliminate loop closure late binding.** The draft admits loops and says the trap cannot happen because nothing rebinds. Python does reassign the loop target on successive iterations. Reject escaping captures or provide explicit snapshot semantics. [Python's loop closure explanation](https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result).

**Avoiding type and operation analysis is incompatible with the guarantee.** The [type-checker non-goal](/Volumes/Projects/pyalamode/SPEC_fable5.1.md:413) can sensibly mean “do not replace a general-purpose type checker.” It cannot mean avoiding the type and callable-resolution information needed to distinguish builtin arithmetic from an effectful `__add__`, or immutable updates from similarly named mutators. A method-name blacklist is insufficient. [Python operator dispatch](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types).

There are additional, smaller issues: mutually exclusive initialization is not defined clearly; ordinary frozen records are accepted too broadly; the count-based baseline description can allow replacing old debt with new debt; and “a terminating while always depends on something changing” is false (`while True: return 1` terminates without a changing condition). Loop exclusions can be useful subset decisions without that justification.

The migration explanation also reverses part of the call-graph story: leaf functions have no relevant callees, rather than necessarily no callers. Convert callees before callers; group mutually recursive functions when necessary.

## Shared gaps to resolve before implementation

All four documents describe substantial language tooling. The AST, import machinery, and persistent data structures make a restricted implementation plausible; they do not themselves provide an effect checker, ownership analysis, or stable dependency environment. Existing [immutables](https://github.com/MagicStack/immutables) and [Pyrsistent](https://pyrsistent.readthedocs.io/en/latest/intro.html) are reuse candidates, not complete functional guarantees. These are engineering conclusions from the documented facilities, not measured feasibility results.

| Open contract | Required decision | Composite resolution |
| --- | --- | --- |
| What exactly ships first? | Accepted grammar, runtime, scalar types, operations, and unsupported behavior | A closed scalar-function subset on one CPython minor, then separately gated expansion |
| How does checking precede initialization? | Build-time rejection versus runtime interception, including defaults and decorators | Source-only analysis rejects invalid checked builds without evaluating definitions; raw Python execution is not intercepted |
| What makes dependencies stable? | Live globals, callable identity, monkey-patching, and cache freshness | Reject undermining writes in analyzed code; disclose unchanged-dependency assumptions and fingerprint build inputs |
| What does trust mean downstream? | Source evidence versus transitive assumptions | Both are retained; trusted callers are never shown as having no external assumptions |
| Can an unsafe effect make strict code run? | Separate permitted orchestration from certifiable source | Unknown adapters stay outside certified strict exports |
| What counts as equal input? | Type, order, identity, numeric edge cases, and callable behavior | Contract-defined equivalence; no universal claim based on Python `==` |
| Can any immutable-container implementation qualify? | Nested validation, callbacks, exports, equality, and mutability escape APIs | A sealed product façade with a characterized backend |
| How is adoption measured? | Baseline identity, coverage denominator, changed trust, and deleted regions | Set comparison plus separate coverage and contract-change checks |
| How much runtime is needed? | Custom execution environment versus ordinary libraries and selected validation | Stock CPython; explicit immutable values; optional export/debug guards; no mandatory runtime registry |

A particularly important architectural distinction is **a strict static contract versus protection from invalid unchecked callers**. Build-time errors can enforce the former without a runtime gate. Its guarantees hold when actual inputs and dependencies satisfy the declared contracts. Optional boundary validators can add specific protection against invalid ordinary callers, but are not what makes static checking strict. Audit differs by allowing noncompliant code without accepting it as checked. The earlier claim that a checker without a runtime gate must be audit-only was too strong.

## Compile-time enforcement and runtime choice

The better default is a static checker/compiler targeting ordinary Python execution. These are three separate decisions: when rules are enforced, what interpreter executes accepted code, and how immutable values are represented. Combining them unnecessarily makes the product resemble a specialized runtime.

| Architecture | Benefit | Cost or condition | Recommendation |
| --- | --- | --- | --- |
| Static checker, compatible Python source, explicit immutable values | Minimal execution disruption; errors block checked builds; existing interpreter and import workflow | Inputs, callbacks, and dependencies must satisfy disclosed contracts | Default |
| Source compiler lowering functional syntax to ordinary Python/library calls | Can offer immutable literals and `val` without a new VM | Separate source semantics, parser/tooling, source mapping, and library dependency | Viable optional edition |
| Generated guards at selected unchecked exports | Reject supported invalid inputs before the body; useful at integration boundaries | Validation coverage and overhead; does not prove arbitrary callback behavior or monitor all dependencies | Optional additional protection |
| Custom VM, mandatory protected loader, live certification registry | Could enforce additional execution assumptions | Much larger compatibility and implementation burden | Exclude from the core absent a specific demonstrated need |

Immutable collections still need algorithms and storage, and snapshots still copy or validate data at runtime. These can be ordinary Python libraries. They do not require a different interpreter, mandatory function wrappers, or a universal effect watcher. A first scalar-only release can use builtin immutable values and an identity declaration marker.

The conditional guarantee is substantive: checked source uses only characterized operations, preserves binding/value rules, and stays within declared effects, assuming its actual inputs and dependencies conform. It does not establish that unchecked Python will obey those assumptions. Python annotations do not enforce actual argument types; selecting an export guard adds explicit validation for supported boundary values. [Python typing documentation](https://docs.python.org/3/library/typing.html).

Checking and build fingerprints remain useful for source and dependency changes. They do not detect every subsequent monkey-patch inside a running process, and the revised composite no longer promises that. Likewise, diagnosing a bad default before a successful build is achievable without importing the module; preventing someone from independently running invalid raw source would be a stronger, separately chosen execution policy.

The composite therefore drops mandatory runtime registration, protected dependency namespaces, and per-call freshness checks. It retains explicit conversions, ordinary immutable-value library invariants, optional selected guards, and build-time evidence. Checked internal calls ordinarily need no repeated validation. A future ownership analysis could admit private mutable builtin containers, but its complexity should not delay the initial static subset.

## What the composite takes and leaves

| Source | Retain | Decline or revise |
| --- | --- | --- |
| `SPEC_sol6.1-with-prev.md` | Compatible semantics; functions/modules; loop capture restrictions; initialization contracts; granular adapters; honest baselines | Ambiguous evidence labels; unsafe propagation without a precise certification rule; crowded first milestone |
| `SPEC_sol6.1.md` | Scalar first release; exact-type validation; ordering and identity rules; hook-free snapshots; explicit freshness and package claims | Inline regions as a committed feature; generic proofs of unordered reductions; one milestone for many advanced execution features |
| `SPEC_sol5.6.md` | Off/audit/strict distinction; gradual adoption; capabilities; domain values; teaching diagnostics | Transformed literal and scope semantics in the compatible edition; adaptation as an evidence status |
| `SPEC_fable5.1.md` | Clear commands; returning-update vocabulary; region inventory; readiness and preview workflows; unconfirmed manifest drafts | Library-only literal rewriting; global alias freezing; universal runtime effect audit; warning-based purity; count-only ratchets |

The composite keeps the XL ambition while making its essential path explicit. Strict static checks and ordinary execution come first. Eager functional values, ordinary-shell interoperability, records, effects, reviewed dependencies, editor support, migration, and published contracts form the core. Boundary guards are an independent option. Builders, concurrency support, and optional syntax require additional gates. Replayable laziness, observable-cache reasoning, and inline blocks become separate extension proposals rather than conditions for delivering the useful product.

## Validation and confidence

I read all four specifications. The project currently contains specifications rather than an implementation, so this assessment is not a benchmark, a formal soundness proof, or an estimate based on existing checker code. The originating brief is not present; where drafts disagree, I have evaluated the product contracts they actually state rather than inventing an unstated requirement for a particular marker or feature.

I checked the central Python claims against primary documentation and ran small probes under the available **CPython 3.13.1**. They confirmed:

- A frozen dataclass can contain a list that still mutates.
- A read-only mapping proxy reflects a mutation through its backing dictionary.
- Escaping loop closures all observed the final loop value in the probe.
- Equal dictionaries constructed in different orders traversed differently.
- A default expression executed before the decorator was applied.
- An `int` subclass passed `isinstance(value, int)` and executed custom arithmetic.

These probes establish the relevant Python counterexamples, not whether a future Pyalamode implementation will reject them. Definition evaluation and loop binding are documented in [Python's compound statements](https://docs.python.org/3/reference/compound_stmts.html); the frozen-record behavior is documented in [dataclasses](https://docs.python.org/3/library/dataclasses.html#frozen-instances); dictionary equality and iteration are documented in [mapping types](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict).

**Decision:** adopt the revised composite as the next design basis. If keeping a single original is important, use `SPEC_sol6.1-with-prev.md`, while revisiting its runtime-enforcement requirements. Establish the bounded strict static contract and build gate on stock Python before investing in broader inference, syntax, or advanced ownership features.
