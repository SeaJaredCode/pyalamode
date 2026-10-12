# Design: additional sum types and the `oneof` spelling

Status: stages 0 to 3 implemented on branch `sum-types`, which has merged main through M13 (`0016394`).
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
| 0 | `oneof` becomes the canonical decorator, with a transitional `variant` alias | M6 | Implemented, then superseded by stage 2 |
| 1 | Closed unions in annotations, values, matches, records, cases, guards and value encoding | M6, M11 | Implemented on `sum-types` |
| 2 | Full rename to `oneof`; the `variant` spelling is gone | M11 | Implemented on `sum-types` |
| 3 | Open tagged `@oneof(open=True)` with distribution-scoped `@case(of=Domain)` | M11, stage 2 | Implemented on `sum-types` |

Stage order follows the original design note. Closed unions stand alone, unlock `int | None`, and exercise the multi-member value representation. Open tagged work touches registry and policy, so it reviews separately. Stage 2 waits for M11 because the uncommitted M11 tree edits the same checker lines and adds new files (`encoding.py`, `distribution.py`) that name `variant`.

## Stage 0: `oneof`

`sum` collides with the builtin, and `alt` reads as branching in FP vocabulary. `oneof` is the canonical spelling. Stage 0 introduced it alongside a transitional `variant` alias. Stage 2 removed the alias.

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
  - `case Domain():` for a domain whose cases are all union members. It covers every current and future case of that domain, like a wildcard scoped to it, so `explicit_cases` refuses it for selected domains. It takes no payload patterns. The runtime makes it native: the domain metaclass's `__instancecheck__` is true exactly for the domain's own case classes. On a plain domain subject it is refused; use `_`;
  - `case Member(...) as name:` binds the narrowed member schema (`int`, the record, the case or the whole domain). The usual rule applies: a capture needs a full, unguarded pattern;
  - literal patterns, which are always partial;
  - a final `_`.
- Expected coverage is the set of exact runtime classes: each scalar (`bool` contributes `True` and `False`), each record, each case, and every case of each member domain. `bool()` covers both booleans.
- A class pattern on a union-typed payload field never makes that field irrefutable. Capture patterns bind the full union schema.
- `explicit_cases` policy applies to closed unions as it does to domains. A wildcard is refused when any member domain is selected by the policy.
- Pattern evidence records the union schema, the class-level case set, coverage, and a fingerprint over the member list plus each member domain's case-set fingerprint. Adding a case to a member domain therefore changes freshness and rejects incomplete explicit consumers.
- Serialized contracts use the canonical `A | B` text. The cache decoder parses it without evaluating user code.

- Payload narrowing follows the existing M6 rule. `case Point(y=None):` constrains the `Point` case and never exhausts it, so a full `Point` consumer captures `y` and matches it separately, or ends with `_`.
- Or-patterns and bare root captures (`case x:`) stay unsupported on union subjects, as on domains.
- `int | None` and `Option[int]` never unify in either direction. `Option` is tagged and nests; a union is a flat class set.

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
- Verification at `268d916`: the full suite (505 tests) passes natively on CPython 3.13.1 macOS arm64, and in Docker `python:3.13.1-slim` (CPython 3.13.1, Linux aarch64) with networking disabled. The Linux run uses `git archive HEAD` copied into the container and a `.pth` file so subprocess tests import the package, since the M9 editor test starts `python -m pyalamode.editor` in a fresh process.

## Stage 2: rename

The project has no users yet, so the rename is complete rather than aliased.

- `@variant` no longer exists. `pyalamode.oneof` is the only spelling, and the runtime module is `pyalamode/sums.py`. A module named `oneof.py` would be shadowed by the `oneof` function on the package.
- Checker identities use `oneof:module:Name`, serialized contract text uses `OneOf['module:Name']`, and value kinds use `oneof_class:`.
- Result and report fields are `oneofs` and `selected_oneofs`. Migration boundary kinds and editor symbols use `oneof`.
- The fresh export envelope is `{"oneof": domain_identity, "case": name, "fields": {...}}`.
- `CHECKER_VERSION` is `sums-unions-11.1` and `OPERATION_VERSION` ends in `-union-ops-11.1`. Baselines from earlier builds are refused as unrecognized provenance, which is correct with no users.
- Genuine M10 history stays readable as provenance. The legacy reader accepts its `variant` boundary kind, its `selected_variants` coverage key and its `variants.py` product inventory, and nothing else uses those spellings.
- Historical milestone, evidence and conformance documents keep `@variant`, because they record what was built and measured at the time.

## Stage 3: open tagged sums

### Declaration

```python
# shapes.py
@oneof(open=True)
class Shape:
    @case
    class Circle:
        radius: int

# squares.py, same project or distribution
from shapes import Shape

@case(of=Shape)
class Square:
    side: int
```

- `@oneof(open=True)` is the only open spelling. `@oneof(open=False)`, `@oneof()` and non-literal values are refused; a closed domain is plain `@oneof`. An open domain may start with no nested cases (`pass`).
- `@case(of=Domain)` is a top-level class with the same payload rules as a nested case. `Domain` must resolve to an unchanged open domain. Case names are unique across the whole domain.
- Extension cases are module attributes, not domain attributes. `Shape.Square` is refused statically and absent at runtime; code imports `Square` from its module.
- A case declared outside the domain's own checked distribution is refused (PAL120). For a project check, the project is one distribution; an installed checked dependency is another.

### Census and freshness

Exhaustiveness inside the distribution is only sound if the checker sees every contributed case, including cases in modules nobody imports.

- When any loaded source declares `@oneof(open=...)`, source loading parses (never imports) every project module under the root, using the same exclusions as project discovery, and loads each one that declares `@case(of=...)`.
- Every module that defines or imports an open domain depends, for cache keys, on all extension modules and their import closures. Adding or editing an extension anywhere in the project therefore re-analyzes those consumers.
- The domain fingerprint covers all cases with their declaring modules, plus the open flag.

### Coverage

- Inside the defining distribution, coverage is exhaustive over the full collected case set, and `explicit_cases` applies as for closed domains.
- In any other distribution, a match over an open domain must end with `_`. Inside a union, `case Domain():` also covers that member, because it matches future cases at runtime too. `explicit_cases` cannot select another distribution's open domain.

### Runtime, guards, encoding and distribution

- The runtime catalog orders cases as nested cases in declaration order, then extension cases by `(module, qualname)`. The checker uses the same order, so generated guard schemas compare equal.
- Guard code references extension cases through their own module, which imports that module and registers the case before validation.
- Encoding keeps PALV1. An extension case's nominal identity is its own `module:Name`. The schema descriptor lists the cases loaded in the process, so encoder and decoder must have imported the same extension modules; otherwise decoding refuses with "wire schema differs from selected schema".
- Wheel evidence: domain rows carry `open`, and each case row carries `module`, `qualname` and `extension`. Extension cases are a new export kind, `case`, listed in `exports` by their own `module:Name` and verified against the consumer's re-derivation like records and domains.

### Not in the first cut

- Cases contributed by consumer packages to a dependency's open domain.
- Open unions.
- Census for single-source APIs (`analyze_source`, `analyze_sources`). Their census is exactly the sources passed in.

## Merge notes for the orchestrator

### Merge of M12 and M13 (`0016394`)

Done on `sum-types` with the procedure below. `--resolve` settled 19 of 26 regions. The rest, and the follow-ups, were:

- `__all__` keeps M13's names with `oneof` and `tailrec`; `FunctionContract` and `FunctionInfo` keep M12/M13 fields and `tail_recursive`/`tailrec`; M13's module-mode import allowance gains `tailrec`; the extension-case exclusion moved into M12's `_attribute_value`; the contract-relation key line keeps the `case` export kind.
- `migration.py`: `PRODUCTS = (M12_PRODUCTS - {"variants.py"}) | {"sums.py", "tasks.py", "task_contracts.py"}`. M13 marks all M10-M12 states with one `historical` flag, and all of them spell `variant`, so the legacy spelling conditions key off `historical`.
- `_FACADE_PUBLIC_BINDINGS` adds `MARKERS`; M12's count assertion goes from 72 to 73. M12's simulated M11 wheel test renames `sums.py` to `variants.py` and drops `tail_recursive`. M12's product child-module list names `sums`.
- Versions: `CHECKER_VERSION = "characterized-tasks-sums-13.1"`, `OPERATION_VERSION` ends `-builder-task-union-ops-13.1`; M13's version test follows. The rename tool no longer rewrites versions, and its legacy-line protection covers `historical`.
- Result: 596 tests pass on macOS.

The `sum-types` branch started at `9108a81`, merged M11 (`c668439`), and then added the rename, open sums and `@tailrec`. M12 is in progress in the main working tree. It was rehearsed against a snapshot of that tree in a scratch clone: after the steps below, the combined tree passed all 550 tests on macOS, and the snapshot alone passed its 506.

### Procedure (after M12 commits)

1. On `sum-types`: `git -c merge.conflictStyle=diff3 merge main`.
2. `python tools/rename_oneof.py --resolve`. This settles every conflict region where one side only renamed the base. In the rehearsal it cleared 25 of 32 hunks.
3. Resolve the remaining regions by hand. In the rehearsal they were:
   - `pyalamode/__init__.py` `__all__`: M12's list with `oneof` and `tailrec`.
   - `pyalamode/model.py`: keep M12's new `FunctionContract` fields and `tail_recursive`.
   - `pyalamode/checker.py`: keep both new `FunctionInfo` fields; add `"tailrec"` to M12's module-mode import allowance; take M12's extracted `_attribute_value(...)` call and apply the extension-case exclusion inside that new method.
   - `pyalamode/project.py`: M12's contract-relation key line plus the `case` export kind branch.
   - `pyalamode/migration.py`: `PRODUCTS = (M11_PRODUCTS - {"variants.py"}) | {"sums.py", "builders.py", "builder_contracts.py"}`, with `M11_PRODUCTS` left historical.
4. `python tools/rename_oneof.py`. M12-only code merges in with the old spelling outside conflict regions; this renames it. The tool is idempotent on branch code and never renames the historical `variants.py`.
5. Apply the M12-specific follow-ups the tool cannot decide:
   - M12 reads M11 history through a `historical` flag. M11 history also spells `variant`, `selected_variants` and `variants.py`, so every legacy-spelling condition in `migration.py` becomes `legacy or historical`.
   - `_FACADE_PUBLIC_BINDINGS` gains the markers: `... | MARKERS | {"unsafe"}`. M12's count assertion for it goes from 66 to 67.
   - Quoted `"variants"` in M12 code can be a module name (becomes `"sums"`) or a result field (becomes `"oneofs"`). The tool picks `oneofs`; review module-name lists, as in M12's product child-module test.
   - M12's simulated M11 wheel test must rename the `sums.py` artifact key to `variants.py` and drop `tail_recursive` from the contract, since genuine M11 evidence has neither.
6. Run the full suite, then the Linux container suite.

Version strings will conflict if M12 bumps them too; take the later milestone's numbering and keep the `sums-unions` and `union-ops` markers.
