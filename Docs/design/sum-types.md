# Design: additional sum types and the `oneof` spelling

Status: stages 0 and 1 implemented on branch `sum-types`, merged with M11 (`c668439`) including union encoding; stages 2 and 3 queued.
Authority: amends `SPEC-sol6.1-composite.md` §10 (records, variants and failure) and the M6 contract in `Docs/milestones/06-domains.md`. Open unions remain out of scope.

## Three designations

Each form has its own discriminator and its own proof story. They are not interchangeable spellings.

| Designation | Syntax | Discriminated by | Exhaustive match | Adding a member |
|---|---|---|---|---|
| Closed tagged | `@oneof` with nested `@case` (today's `@variant`) | Constructor tag | Always | Rejects every incomplete explicit consumer |
| Closed union | `A \| B` in annotations | Exact runtime class of the value | Yes, through class patterns such as `case int(n):` | Rejects every incomplete explicit consumer |
| Open tagged | `@oneof(open=True)`, with `@case` declarations in other modules of the same distribution | Constructor tag | Only inside the defining distribution; elsewhere a final `_` is mandatory | Local incomplete consumers fail; external consumers already have `_` |

Open unions (structural "anything with this class" sets) stay unsupported. `Option` and `Result` stay tagged and are never sugar for unions.

## Stages

| Stage | Scope | Depends on | State |
|---|---|---|---|
| 0 | `oneof` becomes the canonical decorator; `variant` stays an identical transitional alias | M6 | Implemented on `sum-types` |
| 1 | Closed unions in annotations, values, matches, records, cases, guards and value encoding | M6, M11 | Implemented on `sum-types` |
| 2 | Full internal rename: identifiers, explain topics, docs, messages, export envelope key, removal of the `variant` alias | M11 committed | Queued |
| 3 | Open tagged `@oneof(open=True)` with a distribution-scoped case registry | M11 committed, stage 2 | Queued |

Stage order follows the original design note. Closed unions stand alone, unlock `int | None`, and exercise the multi-member value representation. Open tagged work touches registry and policy, so it reviews separately. Stage 2 waits for M11 because the uncommitted M11 tree edits the same checker lines and adds new files (`encoding.py`, `distribution.py`) that name `variant`.

## Stage 0: `oneof`

`sum` collides with the builtin, and `alt` reads as branching in FP vocabulary. `oneof` is the canonical spelling.

- `pyalamode.oneof` is the decorator. `pyalamode.variant` is the same object during the transition, so runtime identity, case registration and export envelopes are unchanged.
- The checker admits both names wherever it admitted `variant`, through the same unchanged-foundation checks. Rebinding either name invalidates the domain vocabulary exactly as before.
- `pyalamode explain oneof` describes the declaration. `explain variant` remains.
- Stage 2 removes the alias, renames internal identifiers and decides the export envelope key. The `{"variant": ...}` envelope key is a wire format and changes only with an explicit M11 encoding decision.

## Stage 1: closed unions

### Member rules

- Allowed members: `None`, `bool`, `int`, `str`, `bytes`, `@record` classes, `@oneof` domains and their `@case` classes.
- Excluded: tuples, collections (generic arguments are erased at runtime), `Option`/`Result` and their cases, `Callable`/`Effectful`, capabilities. These remain refused with PAL130.
- Members must be pairwise distinguishable by exact runtime class. A domain and one of its own cases overlap, so `Shape | Shape.Circle` is refused.
- `bool | int` is refused. Python class patterns use `isinstance`, so `case int():` matches `True`, and literal `1` equals `True`. Exact-class discrimination cannot be expressed safely with native patterns for that pair.
- Unions are set-theoretic. Nested unions flatten, duplicates collapse, and members sort canonically, so `None | int` and `int | None` are one schema. A union that collapses to one member is that member.
- Only the `|` operator is admitted. `typing.Union` and `typing.Optional` are not part of the closed vocabulary.
- String and postponed annotations use the same parser.

### Static behavior

- A union annotation is one canonical schema such as `None | int`. Values of that schema support no operations except matching, passing, returning and storing where a compatible schema is expected. Arithmetic on `int | None` fails closed with PAL210.
- A value fits a union when each of its possible exact types fits some member. A union fits another schema when every member fits it, so `Shape.Circle | Shape.Square` fits `Shape`. A domain value fits a union that lists each of its cases, so `Shape` fits `Shape.Circle | Shape.Square | None`.
- Branch merges that already produce several exact types (for example `1` on one path and `None` on another) are matchable when they normalize to a valid union.
- `match` on a union subject accepts:
  - `case None:`, `case True:`, `case False:`;
  - `case int():`, `case int(n):`, and the same for `bool`, `str`, `bytes`, where the single positional pattern applies to the subject itself;
  - record class patterns and `Domain.Case(...)` patterns, with the existing payload rules;
  - literal patterns, which are always partial;
  - a final `_`.
- Expected coverage is the set of exact runtime classes: each scalar (`bool` contributes `True` and `False`), each record, each case, and every case of each member domain. `bool()` covers both booleans.
- A class pattern on a union-typed payload field never makes that field irrefutable. Capture patterns bind the full union schema.
- `explicit_cases` policy applies to closed unions as it does to domains. A wildcard is refused when any member domain is selected by the policy.
- Pattern evidence records the union schema, the class-level case set, coverage, and a fingerprint over the member list plus each member domain's case-set fingerprint. Adding a case to a member domain therefore changes freshness and rejects incomplete explicit consumers.
- Serialized contracts use the canonical `A | B` text. The cache decoder parses it without evaluating user code.

- Payload narrowing follows the existing M6 rule. `case Point(y=None):` constrains the `Point` case and never exhausts it, so a full `Point` consumer captures `y` and matches it separately, or ends with `_`.
- Or-patterns, `as` patterns and root captures stay unsupported on union subjects, as on domains.

### Runtime and guards

- Records and cases evaluate annotations at class creation, so `int | None` arrives as `types.UnionType`. The runtime schema parser accepts `types.UnionType` and string `A | B` annotations, applies the same member rules, and produces `("union", members)`.
- Validation selects the unique member whose exact class matches the value, then validates against that member. No member means an explicit invalid-data failure.
- Generated facades and debug assertions encode union schemas the same way.

### Encoding

- PALV1 gains schema tag `0x29`: a member count followed by the member schemas in canonical order. Members are scalars, records (`0x20`), domains (`0x21`) or cases (`0x22`).
- A union value is `0x29`, a 4-byte member index, then the member's ordinary encoding. The index is required: two record members both encode as `0x20` with fields only, because nominal identity lives in the schema descriptor, not in the value bytes.
- `int | None` and `None | int` produce identical bytes, because the encoder reuses the runtime's canonical member order.
- Decoding refuses an index outside the member list and any wire schema that differs from the selected one.
- `ENCODING_VERSION` stays `pyalamode.encoding-v1`. The tag is an addition: existing bytes are unchanged, and a product without union support fails closed on `0x29` with "unsupported schema tag". Distribution compatibility already pins exact product file hashes.
- Checked `value_encode(v, int | None)` and `value_decode(b, None | int)` use the ordinary annotation parser.

### Deferred within stage 1

- **Named aliases.** A stable module-level alias such as `Shape = Circle | Square` (or `type Shape = ...`) is not admitted yet. When added, the alias identity `module:Alias` becomes the `explicit_cases` selector for that union.
- **Flow narrowing.** `if x is None:` does not narrow. `match` is the only discriminator.

### Implementation and verification on `sum-types`

- Checker: `TypeSpec("union", members)` with canonical text `A | B`; annotation parsing, member normalization, schema matching, cache decoding, union pattern routing, scalar class patterns, union match subjects and policy in `pyalamode/checker.py`.
- Runtime: `types.UnionType` and string union annotations, member validation and order canonicalization in `pyalamode/records.py`; `validate_data` canonicalizes checker schemas in `pyalamode/boundaries.py`; guard schema code in `pyalamode/guardgen.py`.
- Explain topics `oneof` and `union` in `pyalamode/cli.py`. Example in `examples/unions/shapes.py`.
- Tests: `tests/m06_unions.py` adds 18 tests covering the alias, positive flows, refused members, refused operations, coverage, policy, literals, shadowed builtins, payload narrowing, warm-cache freshness after a member domain gains a case, real off/exports/debug builds with rejected guarded inputs, and runtime validation. Two earlier whitelist tests now use still-refused unions (`int | float`, `bool | int`, `tuple[int | list[int]]`) instead of `int | None`.
- The full suite (419 tests) passes natively on CPython 3.13.1 macOS. One Linux `python:3.13.1-slim` run reported 1 failure in 419 tests before its details could be captured; the rerun was blocked by a Docker Desktop file-sharing hang. Linux verification is outstanding, and that failure is unidentified.

## Stage 2: full rename (after M11)

1. Rename runtime and checker internals (`variants.py` to `oneof.py` or kept as a module name, `VariantInfo`, `variant:` schema prefixes, `Variant[...]` serialized text, `selected_variants` report keys, `explain` topics, diagnostics and documentation).
2. Decide whether the export envelope key moves from `"variant"` to `"oneof"`. That changes the M11 value encoding and its evidence, so it needs its own decision and a reader for the old key if any artifacts already exist.
3. Remove the `variant` alias once no example, test or fixture uses it.
4. Bump `CHECKER_VERSION` and `OPERATION_VERSION`, since serialized contract text changes.

## Stage 3: open tagged (after M11)

- Declaration: `@oneof(open=True)` with nested cases as today, plus top-level `@case(of=Domain)` declarations in other modules.
- Cases from a consumer package are refused in the first cut. Only modules owned by the same checked distribution may add cases. This keeps M11 producer evidence sound without cross-package invalidation machinery.
- The case registry collects cases across the distribution's modules. The domain fingerprint covers the full collected set.
- Coverage: inside the defining distribution, explicit coverage works as for closed domains. Outside it, a final `_` is mandatory regardless of policy, and `explicit_cases` cannot select the domain.
- Encoding: case identity is the declaring `module:Domain.Case`, which is already stable across the distribution.

## Version strings

`CHECKER_VERSION` and `OPERATION_VERSION` are not bumped on this branch. M10 baseline loading requires them to equal the current values, so a bump makes every M11-era reviewed baseline unsupported unless it is registered as legacy. Cache, evidence and distribution freshness do not depend on the bump, because they hash the exact product file bytes. Whether to bump, and how to treat existing baselines, is an orchestrator decision.

## Merge notes for the orchestrator

- The `sum-types` branch started at `9108a81` and has merged M11 (`c668439`). Merge conflicts were three one-line edits in `pyalamode/__init__.py` and the checker's domain discovery.
- One M11 test listed `int | str` among encoder schemas that must be refused. It now uses `Foreign | int`, `int | float` and `bool | int`, which remain refused without foreign hooks.
- Add a ledger entry to `Docs/orchestrations/pyalamode.md` for each stage. The ledger was left untouched here because the M11 session is editing it.
