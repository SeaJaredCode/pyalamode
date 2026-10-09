# pyalamode

> **Scope note.** The ask is a developer tool, not a web application: a language mode, a checker, a
> runtime library, and the surfaces around them. The brief's "self-contained web app served at `GET /`"
> constraint does not apply. Its persistence requirement is read as: everything the tool knows about a
> project (policy, baselines, manifests, report history) lives in plain files checked into the repository,
> so it survives machines, clones, and CI runs. XL scope fits the product: it has many distinct surfaces,
> four personas, and a deep domain (regions, bindings, effects, manifests, policy, migration).

## Purpose

pyalamode adds a **functional mode** to ordinary Python. A developer marks a file, a class, a function, or a
block as `fun`, and inside that region the rules change: every name is bound exactly once, nothing is
mutated, collections are persistent values, classes are immutable records or sealed variants, and functions
are pure unless they declare the effects they perform. The rules are enforced, not suggested: a checker
refuses violations before the code runs, and an optional guard catches at runtime what static analysis
cannot see.

The point is to give Python developers the one thing the language fights hardest: a region of code where
you can *know* a value will not change under you, and *know* a function does nothing but compute its
result. People reach for that guarantee when they write pricing engines, parsers, rules engines, data
transformations, and anything they need to test exhaustively or run in parallel. Today they get it by
discipline and code review. pyalamode makes it a property of the code, checked by a tool, adoptable one
function at a time, and never requires leaving Python: `fun` code is always valid Python that runs on a
stock interpreter.

## Personas

| Persona | What they want from pyalamode |
|---|---|
| **Developer** | Write `fun` code day to day, see violations as they type, fix them with the functional alternative the tool suggests. |
| **Library author** | Ship a package that `fun` code can call safely, by publishing an effect manifest alongside it, and earn a "fun-certified" mark. |
| **Policy owner** (team lead, maintainer) | Decide how strict the project is, which escape hatches are allowed, and make CI hold the line while legacy debt shrinks on a schedule. |
| **Migrator** | Convert an existing codebase one module at a time, with a readiness report that says what blocks conversion and mechanical rewrites for the boring parts. |

## User stories

1. As a **developer**, I put `# mode: fun` at the top of my pricing module and run the checker. It lists every
   place I rebound a name or mutated a collection, each with a one-line reason and the functional rewrite,
   so I can make the module provably pure in one sitting.
2. As a **developer**, I call `print` from a function that never declared an `io` effect, and the checker
   stops me. I either declare the effect, which propagates to every caller, or I move the printing to the
   edge of the program where effects belong.
3. As a **library author**, I ship an effect manifest inside my package describing which of my functions are
   pure, which perform I/O, and which mutate their arguments. Downstream `fun` code calls my library without
   the checker treating every call as unknown and unsafe.
4. As a **policy owner**, I set the project profile to `standard`, forbid local ignore directives in the
   `core/` tree, and record a baseline of existing violations. CI fails on any new violation while the
   baseline count can only go down.
5. As a **migrator**, I ask for a readiness report on a legacy module. I get a ranked list of blockers,
   a suggested conversion order starting at the leaves of the call graph, and a one-command mechanical
   rewrite for each accumulator loop, in-place sort, and mutable class.
6. As a **developer** running my test suite under the guard, a third-party function silently mutates a list
   my `fun` code was holding. The guard raises at the exact call, names the `fun` region that owns the
   value, and the test fails instead of corrupting state three calls later.

---

## The language: what `fun` means

This section defines the dialect. Everything here is valid Python syntax; the mode changes what is
*permitted*, not what parses.

### Declaring a region

A `fun` region is declared in one of four ways, from widest to narrowest:

| Marker | Covers |
|---|---|
| A directory pattern in the policy file (e.g. everything under `core/`) | Every file matched |
| `# mode: fun` as the first non-shebang comment line of a file | The whole file |
| `@fun` on a function or class | That definition and everything nested in it |
| `with fun:` | The statements in the block |

Regions nest. Ordinary Python may appear around and between regions; a file with no marker is untouched.
A region can be narrowed back with `@unfun` or `with unfun:` only when the policy profile permits it
(see Escape hatches).

### Bindings

Inside a region, **assignment is binding, and a name is bound once per scope.**

- `x = 42` binds `x`. A second `x = ...` in the same scope is a violation. So are `x += 1`, `del x`,
  `global`, `nonlocal`, and the walrus operator applied to a name that already exists.
- Shadowing in a nested scope (an inner function or comprehension) is allowed; the inner binding is a new
  name.
- `for` loops are allowed: the loop variable is a fresh binding on each iteration, and the body may not
  bind any name that is visible after the loop. Accumulation is done with `fold`, `scan`, or a
  comprehension, never with a counter.
- `while` loops are allowed in the `lenient` and `standard` profiles with a warning, and forbidden in
  `pure`, because a terminating `while` always depends on something changing.
- Tuple unpacking, conditional expressions, `match` captures, and comprehension variables all follow the
  same once-per-scope rule.

There is no `val` keyword. The region *is* the declaration. (See Assumptions for the rejected reading.)

### Values and collections

Every value that `fun` code constructs is immutable, and `fun` code never mutates any value, whoever
constructed it.

- Literal syntax keeps working. In a region, `[1, 2, 3]` is a persistent **Vector**, `{"a": 1}` is a
  persistent **Map**, `{1, 2}` is a persistent **Set**, and comprehensions produce the same. Under plain
  execution with no runtime installed they are ordinary Python objects that `fun` code is forbidden to
  change, so behaviour is identical either way.
- Every mutating operation is a violation: item and attribute assignment, `del` on an item or attribute,
  and the known mutating methods of the built-in types (`append`, `extend`, `insert`, `pop`, `remove`,
  `sort`, `reverse`, `clear`, `update`, `setdefault`, `add`, `discard`, and so on). The checker knows the
  full list for the built-ins and learns others from manifests.
- The persistent collections offer the full functional vocabulary as *returning* operations: `appended`,
  `without`, `updated`, `sorted_by`, `map`, `filter`, `fold`, `scan`, `group_by`, `partition`, `zip`,
  `window`, `chunk`, `flat_map`, `distinct`, `take`, `drop`, `take_while`, `first`, `last`, `find`, and
  friends. **Seq** is a lazy sequence for pipelines over large or infinite inputs.
- Converting at the boundary is explicit: `freeze(x)` deep-converts an ordinary Python value into
  persistent form, `thaw(x)` produces an ordinary mutable copy for handing to non-`fun` code that needs
  one.

### Records and variants

Inside a region, `class` means **record** or **variant**. Arbitrary stateful classes are not permitted.

- A **record** declares its fields with annotations. Instances are immutable, compared by value, hashable,
  and usable in `match`. Changing one means `replace(point, x=2.0)`, which returns a new instance.
  Records may define methods and computed properties; a method is simply a function whose first argument
  is a value.
- A **variant** is a sealed set of records sharing a base. `match` over a variant must be exhaustive; a
  missing case is a checker error, and adding a case to the variant makes every incomplete `match` in the
  project light up.
- The runtime ships **Option** (`Some`/`Nothing`) and **Result** (`Ok`/`Err`) as variants with the usual
  combinators (`map`, `and_then`, `or_else`, `unwrap_or`, `to_option`), so `None`-checking and exception
  juggling have a structured alternative.
- Existing frozen dataclasses and named tuples are accepted as records when used from a region.

### Functions and effects

**A function in a region is pure by default.** Purity means: its result depends only on its arguments, it
mutates nothing, and it performs no effect.

- Effects are named: `io` (files, network, console), `time`, `random`, `env` (environment, process state),
  `mutate` (changes an object it did not create), and `unknown` (calls something with no manifest entry).
  A function declares the effects it performs with a decorator, e.g. `@effects("io")`.
- Effects propagate. A function that calls an `io` function must itself declare `io`, or the checker
  reports an **undeclared effect** at the call site, naming the callee and the effect. Programs end up with
  a thin effectful rim and a pure core, which is the shape functional programs want anyway.
- What the checker knows about callees comes from **manifests** (next section). A call to something with
  no manifest entry is an `unknown` effect: a warning in `standard`, an error in `pure`, and it propagates
  like any other effect so the uncertainty is visible all the way up.
- Exceptions: `raise` and `try` are allowed in `lenient` and `standard`. The `pure` profile forbids them in
  favour of `Result`, except for re-raising inside an `@effects` function at the rim.
- Closures, lambdas, higher-order functions, default arguments, keyword arguments, and `async` functions
  are all fine. Because nothing rebinds, the classic late-binding closure trap cannot happen.

### Manifests: what the checker knows about other code

A **manifest** describes a package to the checker: for each public function and method, whether it is
pure, which effects it performs, and whether it mutates any of its arguments or its receiver.

- pyalamode ships a built-in manifest for the standard library's commonly used modules, so `fun` code can
  use `math`, `itertools`, `functools`, `re`, `json` (parsing side), `datetime` (constructors and
  arithmetic, with `now()` marked `time`), string and number operations, and so on, from day one.
- A **library author** ships a manifest inside their package. A **project** can add manifests for
  third-party packages and override any entry. Precedence is: project override, then the package's own
  manifest, then pyalamode's built-in manifest, then `unknown`.
- `fun` code needs no manifest for itself: the checker derives effect signatures of `fun` functions
  directly, and those signatures are what other `fun` code sees.
- A manifest can be **drafted** by the tool from a package's signatures and naming conventions, then
  confirmed by a human entry by entry. The draft marks every guess as unconfirmed so nobody mistakes a
  heuristic for a promise.

### Control flow and the rest

- `if`/`elif`/`else`, conditional expressions, `match`, comprehensions, generator expressions, `for` (as
  above), recursion, and early `return` are all allowed.
- `yield` is allowed; a generator in a region is a lazy `Seq` and is single-pass by nature, which the
  checker treats as a value that may be consumed once.
- `import` is allowed anywhere. Importing a non-`fun` module is fine; calling into it is governed by
  manifests.
- Module-level code in a `fun` file may bind constants, define functions and records, and nothing else.

### Boundaries: `fun` and ordinary Python side by side

Values cross the boundary in both directions, and the rules are about who may change what.

- **Into a region**: a value arriving from ordinary code is *borrowed*. `fun` code may read it and derive
  new values from it, but may not mutate it (same as any value). The hazard is the outside world mutating it
  later while `fun` code still holds it. The checker reports a **borrowed escape** when a borrowed mutable
  value is stored into a record or returned without being frozen. The guard (below) makes the hazard
  impossible at runtime by making the value read-only on entry.
- **Out of a region**: a persistent value handed to ordinary code behaves like a read-only version of the
  built-in it resembles. Ordinary code that needs to mutate it calls `thaw`. Attempting to mutate a
  persistent value from anywhere raises, with a message naming the region that produced it.
- A record or variant is a plain immutable object from the outside and can be passed anywhere.

### Escape hatches

Real codebases need them, and the policy owner decides which are available.

- A **local ignore directive** on a line (`# fun: ignore[rebind]`) suppresses one rule on that line. The
  policy can allow them, allow them but count them in reports, require a justification text, or forbid them
  by path.
- `@unfun` / `with unfun:` carve an ordinary-Python hole inside a region. Everything inside is unchecked;
  the hole's boundary is a region boundary and is reported as one.
- Both appear in reports as debt so they never become invisible.

---

## The experience, surface by surface

### The checker (command line)

The daily tool. Run `pyalamode check` at the project root (or on paths) and read the result.

- **Output** is one block per violation: location, rule name, a one-sentence reason, the functional
  alternative when there is a mechanical one, and a pointer to a longer explanation. Example shape:

  ```
  core/pricing.py:42:5  rebind   `total` is already bound on line 38.
      In a fun region a name is bound once. To accumulate, fold over the items:
          total = fold(items, 0, lambda acc, line: acc + line.price)
      More: pyalamode explain rebind
  ```

- `pyalamode explain <rule>` prints the rule's rationale, the profiles it applies in, and examples of the
  violation and the fix.
- `pyalamode regions` lists every region in the project with its marker type and extent, so a reader can
  see the shape of what is checked.
- Exit status reflects policy: errors fail, warnings do not, and the ratchet (see Policy) can fail a run
  that introduces new violations even when the rule is only a warning.
- Output has a terse mode for CI logs and a machine-readable mode for other tools.
- Incremental: on a large project, a second run after a one-file edit re-checks only what that edit can
  affect and finishes in well under a second for typical edits.

### The runtime library

The vocabulary `fun` code is written in: `Vector`, `Map`, `Set`, `Seq`, `Record`, `Variant`, `Option`,
`Result`, the `@fun`/`@effects` decorators, `replace`, `freeze`, `thaw`, and the functional toolkit (`pipe`,
`compose`, `curry`, `partial`, `fold`, `scan`, `unfold`, `iterate`, `memoize`, `par_map`).

- Installing the library is all a project needs to *run* `fun` code; the checker is for *verifying* it.
- Persistent collections share structure between versions, so `appended` on a million-element vector is
  cheap, and they print, compare, and convert like their built-in counterparts.
- `memoize` is accepted only on functions the checker knows to be pure; the checker refuses it elsewhere,
  because memoizing an effectful function is a bug.
- `par_map` runs a pure function over a collection in parallel with no caveats about shared state, which
  is the practical payoff of purity.

### The guard (runtime enforcement)

An optional runtime mode for development and tests, turned on by running the program or test suite through
`pyalamode run` or by an environment switch.

- **Boundary freezing**: values entering a region become read-only on entry; a mutation attempt from
  anywhere afterwards raises, naming the region and the call that attempted it.
- **Rebinding detection**: a region's bindings are watched; a rebinding that static analysis missed (for
  example via `exec` or reflection) raises.
- **Effect audit**: during a guarded run, every effect performed inside a function that did not declare it
  is recorded with its stack. At the end of the run the audit lists each undeclared effect, where it
  happened, and which manifest entry (or absence of one) let it through. Policy can make the audit fail the
  run. This is how manifest mistakes and unknown third-party behaviour get caught.
- The guard reports its own overhead so a team can decide where to enable it.

### The editor

pyalamode works inside common editors with the same engine the command line uses.

- Violations appear inline as you type, with the same message and suggested rewrite.
- Hovering a function shows its effect signature (pure, or the set it declares and the set the checker
  derived). Hovering a value shows whether it is `fun`-owned, borrowed, or ordinary.
- Quick fixes apply the mechanical rewrites: accumulator loop to `fold`, in-place `sort` to `sorted_by`,
  mutable class to record, add the missing effect declaration, wrap a borrowed value in `freeze`, add the
  missing `match` case with a stub.
- A "make this `fun`" action on a function adds the marker and lists what breaks, which is the smallest
  unit of migration.

### Policy

A policy file at the project root, checked in, owned by the policy owner.

- **Profile**: `lenient` (migration: most rules warn), `standard` (default: binding and mutation rules
  error, unknown calls warn, exceptions allowed), `pure` (everything errors, `while`/`raise`/`unknown`
  forbidden).
- **Per-rule settings** override the profile, and can be scoped by path so `core/` can be `pure` while
  `scripts/` is `lenient`.
- **Region declarations by path** so a tree is `fun` without a marker in every file.
- **Escape-hatch rules**: whether ignore directives are allowed, whether they need justification, where
  `unfun` is permitted.
- **Baseline and ratchet**: `pyalamode baseline` records every current violation. Afterwards, `check`
  reports only new ones, and the ratchet fails a run whose total exceeds the baseline. `baseline` can be
  re-recorded only when the count went down, unless a policy owner forces it, and the force is recorded.
- **Manifest sources**: which project-local manifests and overrides to load, and whether `unknown` effects
  are tolerated per path.

### Reports

`pyalamode report` prints a summary and writes a self-contained report page the team can open or publish
from CI.

- **Purity coverage**: share of functions, and of lines, inside `fun` regions, by package and over time.
- **Effect inventory**: every function grouped by effect, the pure-to-effectful ratio, and the
  "rim thickness" (how far from the entry points effects reach).
- **Boundary map**: every region boundary with the values that cross it and any borrowed escapes.
- **Mutation hotspots** outside regions: the ordinary-Python functions with the most mutation, ranked as
  candidates for conversion.
- **Debt**: ignore directives, `unfun` holes, and `unknown` effects, with their justifications and who added
  them when the project history can say.
- **Trend**: baseline count, coverage, and debt across recorded snapshots, so a lead can see the ratchet
  working.
- A certification summary a library author can publish: manifest coverage of their public surface and the
  share that is confirmed rather than drafted.

### The migration assistant

For the migrator, two commands.

- `pyalamode ready <path>` produces a **readiness report**: a score, blockers grouped by rule with counts,
  the external calls with no manifest, and a **suggested order** that starts with leaf functions nobody
  else depends on and works up the call graph, so each conversion is small and its callers are already
  `fun` by the time they are reached.
- `pyalamode convert <function-or-file>` applies the mechanical rewrites the quick fixes offer, in bulk,
  showing a diff and asking for confirmation before writing. It re-runs the checker on the result and
  reports what still needs a human. Every rewrite is reversible with the version control the project
  already uses; pyalamode never writes outside the files it was pointed at.

### The translator and the sugar dialect

For deployment targets that should need neither the checker nor the runtime, and for people who want
syntax Python does not have.

- `pyalamode translate <src> --out <dir>` emits plain Python with the runtime's required pieces vendored
  in, so the output runs anywhere a matching Python runs. Behaviour is identical to running the source
  with the library installed.
- The **sugar dialect** is an opt-in extension marked `# mode: fun+sugar` and only usable through the
  translator and the editor integration. It offers a pipeline operator (`items |> filter(_.active)
  |> map(_.price) |> sum`), the `_` placeholder for partial application, and an explicit `val` keyword
  for readers who want to see the binding. Sugar files are not valid Python until translated; that cost is
  why sugar is optional and last, and the plain dialect never requires it.

---

## What pyalamode keeps track of

Described conceptually. All of it lives in files in the project, except the editor's live state.

- A **project** has one **policy** (profile, rule settings by path, escape-hatch rules, manifest sources)
  and zero or one **baseline** (the recorded set of accepted violations, with the count and when it was
  recorded).
- A project contains many **regions**, each with a marker kind, an extent, and the **functions**,
  **records**, and **variants** defined inside it. A region can contain regions and `unfun` holes.
- Every function, inside or outside a region, has an **effect signature**: declared effects, derived
  effects, and whether it mutates arguments. For `fun` functions the checker derives it; for everything
  else it comes from a **manifest entry**.
- A **manifest** covers one package and has many entries; an entry is confirmed or drafted, and has a
  source (built-in, shipped with the package, or project override). Overrides win over shipped, shipped
  over built-in.
- A **check run** produces many **diagnostics** (location, rule, severity, message, suggested rewrite,
  whether it is in the baseline, whether an ignore directive covers it and with what justification).
- A **guarded run** produces **incidents**: boundary mutations, runtime rebindings, and undeclared effects,
  each with a stack and the region involved.
- A **report snapshot** records coverage, effect inventory, debt, and the baseline count at a point in
  time; the trend is the sequence of snapshots.
- A **variant** has many **cases**; a **match site** covers a subset of a variant's cases, and
  exhaustiveness is the comparison of the two.

---

## Acceptance criteria

A human can confirm each of these by doing it.

1. A file with `# mode: fun` that assigns the same name twice in one function fails `pyalamode check` with
   a `rebind` message that cites both lines and shows a `fold`-based rewrite when the second assignment is
   an accumulation.
2. The same file with the marker removed passes with no output.
3. In a region, `xs.append(1)` on a list, `d["k"] = 1` on a dict, and `obj.x = 1` on any object are each
   reported, and `xs.appended(1)`, `d.updated(k=1)`, and `replace(obj, x=1)` pass.
4. `[1, 2, 3]` written in a region runs correctly with only the runtime library installed and produces a
   value that raises on `.append` from ordinary code.
5. A `match` over a three-case variant that handles two cases is reported as non-exhaustive, naming the
   missing case; adding the case clears it.
6. A function in a region that calls `print` without `@effects("io")` is reported; adding the declaration
   clears it and causes every caller without `io` to be reported in turn.
7. Calling a function from a package with no manifest is a warning in `standard` and an error in `pure`;
   adding a project manifest entry marking it pure clears both.
8. Running a test suite under `pyalamode run` where a third-party function mutates a list that was passed
   into a region raises at that call with the region's name in the message.
9. After `pyalamode baseline` on a project with 40 violations, `check` reports none; introducing one new
   violation fails the run and names it; fixing five old ones and re-recording the baseline succeeds, and
   trying to re-record after adding one fails without the force flag.
10. In the editor, typing `total += x` inside a region shows the diagnostic within a second, and the quick
    fix rewrites the enclosing loop to a `fold`.
11. `pyalamode ready legacy/` lists blockers with counts and a conversion order whose first entry is a
    function with no callees inside the tree.
12. `pyalamode convert` on a class with only assigned attributes and an `__init__` produces a record,
    shows the diff, waits for confirmation, and leaves the file unchanged on decline.
13. `pyalamode report` opened in a browser shows coverage, effect inventory, boundary map, debt, and a
    trend with at least two points after two snapshots.
14. `pyalamode translate` output runs on a machine with no pyalamode installed and produces the same
    results as the source does with the runtime.
15. A `# mode: fun+sugar` file using `|>` is rejected by `check` without translation, and the translated
    output passes `check` and runs.
16. `memoize` applied to a function declaring `io` is rejected by the checker with a message saying why.
17. Running `check` twice on a large project, the second time after a one-line change, finishes well under
    a second on the second run.

---

## Non-goals

- **Not a new language, not a Python fork.** The plain dialect is always valid Python that runs on a stock
  interpreter with only a library installed. No preprocessor is ever required. The sugar dialect exists,
  but it is opt-in, isolated, and nothing in the product depends on it. Rationale: the moment `fun` code
  stops being Python, every debugger, coverage tool, formatter, and type checker breaks, and adoption dies.
- **Not a type checker.** pyalamode checks bindings, mutation, effects, and variant exhaustiveness. It does
  not infer or check argument and return types, and it is designed to run beside whatever type checker the
  project already uses rather than replace it. Rationale: type checking is a solved and separately owned
  problem, and coupling to it would make both tools worse.
- **Not whole-program enforcement.** Code outside a region is never checked, changed, or slowed. The
  guard only touches values crossing into regions. Rationale: gradual adoption is the entire strategy;
  a tool that judges the whole codebase on day one gets uninstalled on day two.
- **Not a security boundary.** The guard is a development aid for catching mistakes, not a sandbox for
  running untrusted code. Rationale: Python offers no cheap way to make that promise honestly.
- **Not a performance promise.** Persistent collections are competitive for the operations functional code
  uses most and slower than built-ins for some others, and the product reports rather than hides that.
  Rationale: correctness is the product; speed parity would dictate engineering choices that compromise it.
- **No modelling of concurrency ordering.** `async` functions can be `fun`, and `par_map` runs pure
  functions in parallel, but the effect system does not track scheduling, cancellation, or ordering between
  concurrent tasks. Rationale: it is a different product.
- **No automatic whole-codebase conversion.** The migration assistant proposes an order and applies
  mechanical rewrites one target at a time, with a diff and a confirmation. Rationale: the non-mechanical
  conversions are design decisions, and pretending otherwise produces code nobody understands.
- **No hosted service.** Reports are files; policy is a file; there is no account, server, or dashboard to
  log into. Rationale: the audience lives in repositories and CI, and a hosted tier is a separate decision.

---

## Assumptions

Each resolves an ambiguity in the ask; the rejected reading is named so it can be reinstated in one sentence.

1. **Assignment in a region is single binding; there is no `val` keyword.** Rejected: `val x = 42` syntax
   enforced by a preprocessor. The ask floated both; single-binding-by-region keeps the plain dialect
   valid Python, which is the foundation every other surface rests on. `val` survives as optional sugar.
2. **Literal collection syntax stays legal in regions and means the persistent collection.** Rejected:
   banning `[...]`, `{...}` and requiring `Vector(...)`. Banning literals makes `fun` code ugly for no
   safety gain, since the checker already forbids mutation.
3. **Functions are pure by default and declare effects; effects propagate to callers.** Rejected: "no I/O
   at all inside regions", which makes real programs impossible to write as `fun`; and "no effect tracking",
   which makes the word purity meaningless.
4. **Unknown calls are a warning in `standard` and an error in `pure`.** Rejected: error everywhere, which
   would block a first run on any project with a dependency. The built-in standard-library manifest keeps
   the warning count small from day one.
5. **Exceptions are allowed in `standard` and forbidden in `pure`.** Rejected: forbidding them everywhere,
   which would exclude most existing code from ever being `fun`.
6. **`class` in a region means record or variant.** Rejected: allowing arbitrary classes and trying to freeze
   them. Stateful classes are the heart of what the mode exists to exclude, and records cover the honest
   uses.
7. **The mode is named `fun` and the file marker is `# mode: fun`**, per the ask. Decorator and block
   markers are added so a region can be smaller than a file, since gradual adoption needs that granularity.
8. **The target is modern Python with structural pattern matching**, because variants without exhaustive
   `match` are not worth shipping. Older interpreters are out of scope.
9. **Everything runs locally and in CI.** Rejected: a hosted dashboard. See Non-goals.
10. **The editor integration is delivered through whatever standard mechanism common editors already
    support for diagnostics and quick fixes**, so one engine serves all editors. Rejected: a single-editor
    plugin.

---

## Roadmap

Thirteen milestones. Milestone 1 is a usable product on its own; every later milestone adds a capability to
something that already works.

1. **Regions and the binding rules.** The `check` command, the four region markers, single binding, the
   mutation rules against the built-in types, messages with reasons and rewrites, `explain`, `regions`.
   A developer can mark a module `fun` today and get a trustworthy list of everything that violates it.
2. **Persistent collections.** `Vector`, `Map`, `Set`, `Seq`, the returning-operation vocabulary, literal
   semantics in regions, `freeze`/`thaw`, the borrowed-escape rule, and checker awareness of the library's
   own API. `fun` code can now work with collections instead of avoiding them.
3. **Records, variants, Option and Result.** Immutable records with `replace`, sealed variants, exhaustive
   `match` checking, `Option`/`Result` with combinators, acceptance of frozen dataclasses and named tuples.
4. **Effects.** Pure-by-default functions, `@effects` declarations, propagation checking, the built-in
   standard-library manifest, the `unknown` effect, and the exception rules by profile.
5. **Manifests for other code.** The manifest format, package-shipped and project-local manifests with
   precedence, overrides, manifest drafting with confirmed/drafted marking, and the library author's
   certification summary.
6. **Policy, profiles, baseline and ratchet.** The policy file, `lenient`/`standard`/`pure`, per-rule and
   per-path settings, escape-hatch rules, ignore directives with justification, `baseline` and the ratchet,
   CI output modes.
7. **The guard.** `pyalamode run`, boundary freezing, runtime rebinding detection, the effect audit with its
   end-of-run report, and overhead reporting.
8. **Editor integration.** Live diagnostics, effect-signature and ownership hovers, quick fixes for every
   mechanical rewrite, the "make this `fun`" action.
9. **Incremental checking.** Sub-second re-checks after small edits on large projects, so the editor and
   CI stay fast as adoption grows.
10. **Migration assistant.** `ready` with readiness score, blockers, and leaf-first conversion order;
    `convert` with diff and confirmation and a post-conversion re-check.
11. **Reports and trend.** `report` with coverage, effect inventory, boundary map, mutation hotspots, debt,
    snapshots, and the trend view; the publishable report page.
12. **Functional toolkit.** `pipe`, `compose`, `curry`, `partial`, `unfold`, `iterate`, `memoize` (purity-
    gated), `par_map`, and property-test helpers that generate record and variant instances from their
    declarations.
13. **Translator and sugar dialect.** `translate` producing stand-alone plain Python, and the opt-in
    `fun+sugar` dialect with the pipeline operator, placeholder partial application, and `val`.
