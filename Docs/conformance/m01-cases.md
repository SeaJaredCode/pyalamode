# Milestone 1 independent conformance inventory

Source of requirements: `SPEC-sol6.1-composite.md`, especially §§3–7, 14, 16–18. This inventory is an independent review artifact, not evidence that the cases have passed. Requirement fixtures use only the proposed `fun`, `check`, `check --audit`, `build`, and `explain` interfaces. No output-directory option, manifest schema, result API, or new rule number is proposed. The final observation section also names the implementation's existing internal analysis entry point for reproducibility.

Run each source fixture independently unless a case explicitly describes a mutation sequence. Select the fixture with `pyalamode check [paths]`; use the implementation's documented project selection for `pyalamode build`. Expected verification failures use status 1. Tooling, resolution, and unsupported-target failures use status 2. Audit findings alone use status 0 absent an explicit audit gate. A diagnostic must include a stable rule ID, source location, affected boundary, origin, reason, and valid remediation (§14); `PAL101` is the specification's existing example for repeated initialization, not a complete proposed rule catalog.

“Pass” means acceptance under a published supported environment and current inputs. An accepted unguarded function still requires exact admitted inputs and unchanged approved bindings at execution. Nothing here requires runtime purity enforcement, automatic conversion, a special loader, or a per-call registry.

## Distinguish the three analysis questions

1. A participating function must satisfy the closed scalar vocabulary.
2. An ordinary caller included in analysis must establish the checked callee's input contract. The caller does **not** thereby become pure, single-assignment, or certified as a whole.
3. An ordinary caller outside analysis assumes the published obligations. Until milestone 4 optional guards, an invalid raw call may execute ordinary Python behavior. Its execution has no valid strict claim.

Checks must analyze syntax without importing the application or executing its annotations, defaults, decorators, class bodies, or initializer expressions. Unrelated ordinary module initialization need not be pure; a checked function's actual dependencies must nevertheless be established. This distinction is essential to A04, A06, A07, and A33.

## A01: successful scalar checking, building, and ordinary execution

### A01.1 — reference calculation

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

assert discounted_total(1000, 250) == 750
assert discounted_total(100, 250) == 0
```

Expected: strict check and checked build pass; the compatible artifact runs through ordinary Python and produces those results. The branches initialize `result` once on every path reaching its use. The analyzed calls establish exact integer inputs. Evidence names the function, scalar contracts, current build inputs, trusted foundation, and unguarded caller obligations (§§2–6; A01).

### A01.2 — effects and rebinding in an ordinary caller

```python
from pyalamode import fun

@fun
def plus_one(value: int) -> int:
    return value + 1

def application_shell() -> None:
    value = 4
    print("ordinary shell")
    value = 5
    answer = plus_one(value)
    print(answer)

application_shell()
```

Expected: `plus_one` is accepted and its analyzed call has exact integer evidence. The shell's `print` and ordinary rebinding do not become purity violations in `plus_one` and must not cause an invented whole-module purity claim. A checker may need finite ordinary-caller type flow here; milestone 1 cannot defer *all* caller analysis to milestone 2 (§6; A04). If the implementation cannot establish the call's argument, it must diagnose that missing evidence rather than certify the call by assumption.

### A01.3 — ordinary module initialization is not executed by analysis

```python
from pyalamode import fun

raise RuntimeError("application imported during static analysis")

@fun
def add(left: int, right: int) -> int:
    return left + right
```

Expected: static analysis never raises the application error. The unrelated ordinary initializer receives no purity certificate. A check can certify the function body and disclose the ordinary initialization assumption; it cannot claim that importing the complete fixture succeeds. A successful checked build is not permission to report this artifact as an executable-success test (§§4.1, 5.1, 12). This case separates static non-execution from the A01.1 execution witness.

## A02: initialized bindings cannot be initialized again

### A02.1 — equal values still count as a second assignment

```python
from pyalamode import fun

@fun
def same_value(value: int) -> int:
    result = value
    result = value
    return result
```

Expected: fail at the second assignment and identify the first binding. Equality does not rescue a second reachable initialization (§7; A02).

### A02.2 — parameter initialization and augmented assignment

```python
from pyalamode import fun

@fun
def increment(value: int) -> int:
    value += 1
    return value
```

Expected: fail; the parameter is already initialized and augmented assignment is expressly prohibited. Its first binding location is the parameter declaration (§7; A02).

### A02.3 — local augmented assignment

```python
from pyalamode import fun

@fun
def increment_local(value: int) -> int:
    result = value
    result += 1
    return result
```

Expected: fail, with the original local initialization identified. An implementation must not special-case only parameter `+=` (§7).

## A03: joins and early returns

### A03.1 — exclusive nested branches

```python
from pyalamode import fun

@fun
def select(first: bool, second: bool) -> int:
    if first:
        value = 1
    elif second:
        value = 2
    else:
        value = 3
    return value
```

Expected: pass. These are mutually exclusive initializations in one Python lexical scope, not three scopes (§7; A03).

### A03.2 — a missing reaching initialization

```python
from pyalamode import fun

@fun
def missing(flag: bool) -> int:
    if flag:
        value = 1
    return value
```

Expected: fail at the use or join with the missing `flag == False` initialization explained. No implicit `None` or assumed truthy path may fill it (§7; A03).

### A03.3 — may-initialized is insufficient for another assignment

```python
from pyalamode import fun

@fun
def second_on_one_path(flag: bool) -> int:
    if flag:
        value = 1
    value = 2
    return value
```

Expected: fail because the `flag == True` path reaches a second initialization. A join needs both definite-initialization information and possible earlier binding origins (§7; A03).

### A03.4 — early return removes its path from the join

```python
from pyalamode import fun

@fun
def early(flag: bool) -> int:
    if flag:
        value = 1
        return value
    value = 2
    return value
```

Expected: pass. The first initialization cannot reach the second; merely unioning all assignments in both branches gives a false failure (§7; A03).

### A03.5 — an early return rescues the other path's initialization

```python
from pyalamode import fun

@fun
def surviving_path(flag: bool) -> int:
    if flag:
        return 0
    else:
        value = 1
    return value
```

Expected: pass. Every path reaching the final use initialized `value`, even though not every entry path did (§7; A03).

### A03.6 — returns do not erase a live second assignment

```python
from pyalamode import fun

@fun
def still_second(flag: bool) -> int:
    value = 0
    if flag:
        return value
    value = 1
    return value
```

Expected: fail. The surviving path reaches both bindings (§7; A03).

### A03.7 — return contract includes fallthrough

```python
from pyalamode import fun

@fun
def falls_through(flag: bool) -> int:
    if flag:
        return 1
    pass
```

Expected: fail; the other path returns Python `None`, which does not establish the exact integer result contract. The implementation must account for implicit return behavior while preserving ordinary Python semantics (§§3.1, 6).

### A03.8 — distinct branch result types

```python
from pyalamode import fun

@fun
def mixed(flag: bool) -> int:
    if flag:
        value = 1
    else:
        value = True
    return value
```

Expected: fail. Single initialization is satisfied, but the joined result is not always exact `int`. Exact `bool` must not collapse into the Python subclass relation to `int` (§6).

## A04: exact input contracts in analyzed callers

### A04.1 — exact booleans and integers are different

```python
from pyalamode import fun

@fun
def integer(value: int) -> int:
    return value + 1

@fun
def boolean(value: bool) -> bool:
    return not value

integer(True)
boolean(1)
```

Expected: both analyzed calls fail. Python's `isinstance(True, int)` relationship and cross-type equality are not the admitted contract (§§3.1, 6; A04).

### A04.2 — an integer subclass can hide overloaded behavior

```python
from pyalamode import fun

@fun
def integer(value: int) -> int:
    return value + 1

class HostileInt(int):
    def __add__(self, other):
        raise RuntimeError("subclass behavior executed")

integer(HostileInt(1))
```

Expected: fail at the analyzed call without constructing `HostileInt` or invoking its operator. The ordinary class is not itself required to be pure; its result is not an exact integer (§6; A04). Equivalent exact-type rejection applies to subclasses of `str` and `bytes`.

### A04.3 — mutable arguments and unknown shell inputs

```python
from pyalamode import fun

@fun
def length(value: str) -> int:
    return len(value)

length(["mutable"])

def shell(value):
    print("ordinary behavior")
    return length(value)
```

Expected: the mutable argument fails, and the unknown argument requires input evidence. The `print` is ordinary shell behavior, not a purity violation attributed to `length`. The selected gate must not silently assume every ordinary caller argument satisfies the annotation (§§3.1, 6; A04).

### A04.4 — indirect aliases retain the callee obligation

```python
from pyalamode import fun

@fun
def integer(value: int) -> int:
    return value + 1

alias = integer
alias(True)
```

Expected: the analyzed alias call fails. A recognizable callee alias cannot erase exact-input obligations. If a caller's indirect target cannot be established, the checker reports missing callable/input evidence instead of treating the call as validated (§§3.1, 5.2; A04).

### A04.5 — annotations on ordinary callers are not exact-type proofs

```python
from pyalamode import fun

@fun
def integer(value: int) -> int:
    return value + 1

def shell(value: int) -> int:
    return integer(value)
```

Expected: a conventional ordinary Python annotation alone is insufficient to prove this call always supplies an exact integer. The implementation must describe how it establishes the ordinary caller's obligation, or issue a missing-evidence finding. The shell annotation has not independently acquired the stricter checked-input meaning (§§3.1, 6; A04).

## A05: audit is observation, not certification

```python
from pyalamode import fun

@fun
def invalid(value: int) -> int:
    value = value + 1
    print("ordinary execution remains ordinary")
    return value

assert invalid(2) == 3
```

Expected: strict checking fails; `check --audit` reports both adoption blockers but grants no strict certificate. Audit findings alone do not fail the audit command absent an audit gate. Running the raw source separately prints the text and returns 3; an audit must not alter the source, replace the function, install enforcement, or turn findings into accepted strict evidence. A later build of the same invalid source still fails (§§3.2, 5.1, 14; A05).

Audit output must make the selected boundary and excluded ordinary source understandable. It must not report the project as functional merely because one different function passed. A baseline or suppression cannot turn this body into a strict checked export (§15).

## A06: resolve actual operations and declaration markers

### A06.1 — direct builtin shadowing

```python
from pyalamode import fun

def abs(value):
    print("shadowed builtin")
    return value

@fun
def magnitude(value: int) -> int:
    return abs(value)
```

Expected: fail. The name resolves to ordinary application behavior rather than the approved builtin contract (§§5.2, 6; A06).

### A06.2 — local shadowing and an earlier syntactic local binding

```python
from pyalamode import fun

@fun
def parameter_shadow(abs: int, value: int) -> int:
    return abs(value)

@fun
def local_shadow(value: int) -> int:
    result = abs(value)
    abs = 1
    return result
```

Expected: both fail. A parameter is not an approved callable. Python's function-wide local binding analysis makes the second `abs` local even before its assignment; spelling-based builtin resolution would incorrectly accept an ordinary `UnboundLocalError` path (§§5.2, 6–7; A06).

### A06.3 — marker import aliases and qualified markers

```python
from pyalamode import fun as checked
import pyalamode as pal

@checked
def first(value: int) -> int:
    return value + 1

@pal.fun
def second(value: int) -> int:
    return value - 1
```

Expected: actual marker aliases are discovered as participating functions, or the implementation explicitly reports unsupported declaration syntax. It must never produce a silently clean result with these boundaries omitted. Admission follows the resolved marker target, not the literal spelling `fun`. The release should publish which source alias forms it recognizes (§§4.1, 5.2, 6; adversarial-suite requirement).

### A06.4 — a familiar marker spelling with a different target

```python
def fun(function):
    return function

@fun
def ordinary(value: int) -> int:
    value = value + 1
    return value
```

Expected: the function receives no strict certificate merely because its decorator is spelled `fun`. The ordinary decorator and body remain ordinary Python. Report source selection accurately. Do not certify the function as a product marker, and do not invent automatic whole-module opt-in (§§4.1, 5.2; A33).

### A06.5 — rebinding a real marker alias

```python
from pyalamode import fun as checked

checked = lambda function: function

@checked
def replaced(value: int) -> int:
    value = value + 1
    return value
```

Expected: the decorator target is no longer the imported marker; no strict certificate may be attached to `replaced`. A declaration-resolution/rebinding diagnostic is preferable where the implementation recognizes the attempted participating declaration. A clean result must explicitly leave the boundary unselected, not claim successful verification of it (§§4.1, 5.2).

### A06.6 — a builtin alias is not automatically a stable application global

```python
from pyalamode import fun

magnitude = abs

@fun
def value(number: int) -> int:
    return magnitude(number)
```

Expected: fail in the initial subset unless the published primitive-alias syntax statically resolves and admits this exact binding. Milestone 1 excludes ambient application globals; ordinary assignment is not enough to publish a stable constant. Merely observing that its current value is the builtin is insufficient (§§5.2, 6; stable application bindings arrive in milestone 2).

### A06.7 — builtin attribute aliases and indirect monkey-patching

```python
import builtins as library
from pyalamode import fun

alias = library
alias.abs = lambda value: value + 1

@fun
def magnitude(value: int) -> int:
    return abs(value)
```

Expected: fail: the analyzed alias writes the approved builtin dependency. The checker does not need to classify all ordinary shell behavior as pure to reject this known dependency invalidation. No application code is run (§5.2; A06).

### A06.8 — writes through a namespace operation

```python
from pyalamode import fun

namespace = globals()
namespace["abs"] = lambda value: value + 1

@fun
def magnitude(value: int) -> int:
    return abs(value)
```

Expected: dependency admission fails or is explicitly unresolved; a read-only ordinary initializer scan must not treat the familiar `abs` spelling as established after a recognized namespace mutation. The arbitrary ordinary shell is not certified, and the unresolved dependency may not receive a guessed approved target (§5.2; A06).

### A06.9 — unknown calls and deferred checked call graphs

```python
from pyalamode import fun

@fun
def first(value: int) -> int:
    return value + 1

@fun
def second(value: int) -> int:
    return first(value)
```

Expected: fail in milestone 1, where only the initial builtin whitelist is admitted. A locally well-typed callee is not sufficient to silently introduce milestone 2 checked call graphs. Recursion is likewise excluded (§6; roadmap milestone 2).

### A06.10 — unsupported constructs remain unsupported

```python
from pyalamode import fun

@fun
def loop(value: int) -> int:
    for item in [value]:
        pass
    return value

@fun
def hidden(value: int) -> int:
    def nested() -> int:
        return value
    return value

@fun
def mutate(value: int) -> int:
    values = [value]
    values[0] = value
    return value
```

Expected: fail for statement iteration, nesting/capture, mutable construction, and element mutation. Related negative fixtures must cover `while`, comprehensions, imports in bodies, tuples, arbitrary attribute access, methods, indexing, formatting, assignment expressions, `global`, `nonlocal`, `del`, `raise`, `try`, async/yield, and reflection. Tuples are deferred despite being builtin immutable outer containers; later admission needs recursively stable members (§§6–8).

## A07: do not execute rejected definition-time behavior

### A07.1 — malicious annotation expression

```python
from pyalamode import fun

def poison():
    raise RuntimeError("annotation evaluated")

@fun
def annotated(value: poison()) -> int:
    return 1
```

Expected: diagnose unsupported annotation syntax without calling `poison`, importing the fixture, or using `get_type_hints`. Build fails. Subscript/attribute/call expressions outside the published annotation whitelist fail for the same reason (§§5.1, 6; A07).

### A07.2 — malicious default and a harmless default

```python
from pyalamode import fun

def poison():
    raise RuntimeError("default evaluated")

@fun
def bad_default(value: int = poison()) -> int:
    return value

@fun
def scalar_default(value: int = 1) -> int:
    return value
```

Expected: both functions fail because all defaults are excluded initially. `poison` is never evaluated. A literal default cannot be silently admitted just because A07 mentions “bad” defaults; defaults belong to milestone 2 (§6; A07).

### A07.3 — additional decorators and decorator factories

```python
from pyalamode import fun

def poison(function):
    raise RuntimeError("decorator evaluated")

def factory():
    raise RuntimeError("decorator factory evaluated")

@fun
@poison
def inner(value: int) -> int:
    return value

@factory()
@fun
def outer(value: int) -> int:
    return value
```

Expected: both participating declarations fail without invoking either decorator or factory. Discovery must scan the complete decorator list, including when `@fun` is not outermost. Extra decorators are excluded regardless of their claimed annotation or apparent identity behavior (§§4.1, 5.1, 6; A07).

For all non-execution fixtures, an external harness can place a sentinel write in `poison` and assert the sentinel is absent after check, audit, and failed build. Place the sentinel outside the build destination; assert application stdout/stderr is also absent. Only the external harness creates fixtures or checks filesystem state; static analysis itself must never execute these functions. Source errors may be reported, but arbitrary application exceptions must not become the check result.

## A08: error classes, build gates, and current evidence

### A08.1 — unsupported environment

Use the A01.1 fixture under an interpreter minor, build flavor, platform, or patch outside the published supported matrix.

Expected: status 2 and an unsupported-target/tooling explanation; no successful checked artifact/evidence for this attempted build. A generic `cpython-3.13` string does not substitute for a tested patch range. The release must name the supported patches and standard build assumptions before claiming the milestone gate (§§1, 6, 14; A08).

### A08.2 — parsing, resolution, and tooling failures

```python
from pyalamode import fun

@fun
def broken(value: int) -> int
    return value
```

Expected: parse/tooling failure cannot be reported as a clean check or an empty certified selection. Similarly, missing/unreadable source inputs, unreadable required policy, missing marker resolution, internal analyzer failure, and interrupted analysis cannot become a successful strict check. Use the published classification consistently; resolution/tooling failures are status 2 (§14; A08).

### A08.3 — a failed build must not publish a new checked artifact

Start with A01.1 and build it successfully. Change its participating body to A02.1 and build again.

Expected: the second build fails before application execution and produces no successful artifact/claim for the changed source. A previous successful artifact may be retained, but must remain visibly tied to the previous inputs; its evidence must not be refreshed, relabeled, or passed off as the failed build's result. Also test a fresh empty output destination: a failed first build must not leave a consumable output represented as checked. Partial temporary files are not successful artifacts (§§5.1–5.2, 14; A08).

### A08.4 — current evidence cannot be bypassed by a warm result

Start with A01.1; check/build once; change the source to A06.1; check/build again using the same cache/state.

Expected: the changed relevant source invalidates the previous success and the second gate fails. Repeat separately with a relevant policy change, a supported-target change, and a checker/operation-contract change if the implementation caches results. Fingerprints include source/artifact bytes, edition, rules, Python target, policy, dependency identities/contracts, and trust approvals when applicable. Losing a disposable cache cannot change the claim (§5.2).

### A08.5 — artifact equivalence and absence of a functional loader

Build A01.1 and inspect the compatible source and public evidence. Run the artifact with ordinary supported Python using its ordinary declared package dependency.

Expected: admitted bodies preserve Python expression semantics and results. No custom loader, function registration, runtime certificate service, generated mandatory validation wrapper, or per-invocation evidence check is required. A normal import dependency for the identity marker is permitted. `build` does not execute the application merely to establish correctness (§§4.1, 5.1–5.4; A08).

## A33: the marker is a runtime identity, not enforcement

```python
from pyalamode import fun

def ordinary(value: int) -> int:
    value += 1
    return value

marked = fun(ordinary)
assert marked is ordinary
assert marked(2) == 3

@fun
def unchecked(value: int) -> int:
    value += 1
    return value

assert unchecked(2) == 3
```

Expected when executed as raw ordinary Python: identity assertions and ordinary reassignment behavior succeed; no registry, wrapper, or purity enforcement is installed. Running this file does not create checked evidence. When checked/build-selected, `unchecked` fails; audit only reports the violation. An application should not need an initialized checker service to import and use the marker (§§2, 5.1, 5.3; A33).

Also execute a raw unguarded checked-shaped function with an `int` subclass or `True`. The marker must retain ordinary Python dispatch; it need not reject those values at runtime. Report their exact-input violation as an execution precondition failure, not a product promise of runtime interception (§§3.1, 6; A04/A33). Similarly, ordinary unchecked rebinding of `builtins.abs` after a successful check violates a dependency precondition; it is not evidence that a mandatory live monitor is missing (§5.2).

## Closed scalar vocabulary: additional positive and negative fixtures

Each row describes a separate participating function with explicit parameter/result annotations. Use the indicated expression as its body; an accepted operation's results must match ordinary Python under the recorded runtime. For rejected expressions, do not execute user hooks to infer their behavior.

| Parameters and result | Body/expression | Expected and rationale |
| --- | --- | --- |
| `left: int, right: int -> int` | `return +left - -right` | Pass; characterized integer unary signs and subtraction. |
| `left: int, right: int -> int` | `return left * right` | Pass; exact integer multiplication. |
| `left: int, right: int -> int` | `return left // right` | Pass; ordinary floor division, characterized `ZeroDivisionError` when `right == 0`. |
| `left: int, right: int -> int` | `return left % right` | Pass; ordinary remainder and characterized zero failure. Include negative operands to distinguish floor semantics from truncation. |
| `left: int, right: int -> bool` | `return left < right` | Pass; same-type comparison. Include all admitted comparison forms. |
| `left: str, right: str -> str` | `return left + right` | Pass; same-type concatenation. |
| `left: bytes, right: bytes -> bytes` | `return left + right` | Pass; same-type concatenation. |
| `left: str, right: str -> bool` | `return left <= right` | Pass; characterized same-type ordering. |
| `left: bytes, right: bytes -> bool` | `return left == right` | Pass; same-type equality. |
| `left: bool, right: bool -> bool` | `return not left or (left and right)` | Pass; exact Boolean operations with Python evaluation order. |
| `flag: bool, left: int, right: int -> int` | `return left if flag else right` | Pass; Boolean condition and a same-type scalar join. |
| `value: int -> int` | `return abs(value)` | Pass; exactly one exact integer argument. |
| `left: int, right: int, third: int -> int` | `return min(left, right, third)` | Pass; supported same-type positional arity. Also test `max`. |
| `left: str, right: str -> str` | `return max(left, right)` | Pass; supported exact string arguments. Also test bytes. |
| `value: str -> int` | `return len(value)` | Pass; exact string length. Also test bytes. |
| `value: int -> int` | `return value / 2` | Fail; `/` and its float result are excluded. |
| `value: int -> int` | `return value ** 2` | Fail; exponentiation is not initially characterized. |
| `value: bool -> int` | `return value + 1` | Fail; Boolean arithmetic is not integer arithmetic. |
| `value: int -> bool` | `return value == True` | Fail; cross-type comparison. |
| `value: str -> bool` | `return value == b"x"` | Fail; cross-type comparison. |
| `value: int -> int` | `if value: return 1` followed by `return 0` | Fail; branch condition must be Boolean, with no general truth protocol. |
| `value: str -> str` | `return value and "fallback"` | Fail; initial Boolean operations require Boolean operands. |
| `value: str -> str` | `return value[0]` | Fail; indexing is deferred. |
| `value: str -> str` | `return value[:]` | Fail; slicing is deferred. |
| `value: str -> str` | `return value.upper()` | Fail; methods are deferred despite familiar spelling. |
| `value: int -> str` | `return f"{value}"` | Fail; interpolation/formatting needs later operation contracts. |
| `value: int -> int` | `return len(value)` | Fail; unsupported exact operand type. |
| `value: bool -> int` | `return abs(value)` | Fail; `abs` requires exact integer. |
| `value: int -> int` | `return abs(value, value)` | Fail; unsupported arity. |
| `value: int -> int` | `return abs(value=value)` | Fail unless the published signature explicitly admits this form; Python's builtin signature is part of the actual approved contract. |
| `value: str -> str` | `return min(value)` | Fail; iterable form is excluded. |
| `value: str -> str` | `return max(value, default="")` | Fail; `default` form is excluded. |
| `left: int, right: int -> int` | `return min(left, right, key=abs)` | Fail; `key` form is excluded, even for a familiar builtin. |
| `left: int, right: str -> int` | `return min(left, right)` | Fail; heterogeneous arguments are excluded. |
| `value: int -> int` | `return int(value)` | Fail; no other builtin call is initially admitted. |
| `value: int -> bool` | `return value is 1` | Fail; allocation identity is not an admitted observation. |
| `value: int -> int` | `return 1.0` | Fail; floats are outside the initial value domain. |
| `value: int -> int` | `return (value,)` | Fail; tuples arrive in milestone 2. |

`NoneType` needs a published non-executed annotation spelling. A standard source form to settle explicitly is `@fun def absent() -> None: return None`; expected value behavior is exact `NoneType`, and `return None is None` has a Boolean result. The inventory does not invent a new `NoneType` import API. Test permitted `is None`/`is not None` separately from arbitrary `is`, and do not infer that every cross-type equality is allowed (§§6, 8.1).

For the annotation whitelist, test missing parameter annotations, a missing result annotation, `Any`, a user alias assigned to `int`, an ordinary subclass annotation, and a non-whitelisted string expression. All require explicit supported source resolution or rejection; neither evaluation nor a general type checker's ordinary subtype rules can supply the stricter scalar contract. Forward/string annotations and positional/keyword parameter forms must be listed in the release's syntax contract rather than accidentally accepted by AST convenience (§6; §18).

## Freshness and roadmap gates

The roadmap's sequencing is coherent if later milestones expand the contract without postponing the following foundations:

- **Milestone 1 caller evidence:** A04 already includes ordinary analyzed callers, subclass rejection, aliases, mutable arguments, and unknown inputs. Milestone 2 may introduce calls *from strict bodies* to checked application callees and recursion; it cannot be the first implementation of A04.
- **Milestone 1 environment and vocabulary publication:** the CPython patch matrix, non-executed annotation/declaration syntax, exact signatures, supported argument forms, scalar failures, diagnostic explanations, and ordinary caller obligations are release prerequisites (§§1, 6, 14, 18). A successful test under one local interpreter does not establish the promised matrix.
- **Freshness starts with the first reusable evidence:** §5.2 applies as soon as any cache, report, or checked artifact is emitted. A10 expands application dependency replacement at milestone 2; A28 adds separately consumed installed-artifact evidence at milestone 11. Neither allows stale milestone 1 success to survive changed source, policy, target, or builtin contracts.
- **Milestone 2 initialization and captures:** modules/defaults/nesting may be admitted only after their initialization, stable bindings, and captures are statically modeled. Preserve the A03 early-return rules and account for writes through aliases. Escaping reused loop cells remain rejected until an explicit later lifetime contract exists (§7).
- **Milestone 3 callback and backend assumptions:** collection callbacks need checked pure contracts even before milestone 5 permits characterized effects. Persistent backend identity, trust, ordering, and nested-value validation are prerequisites of collection admission, not details deferred to external-integration or packaging milestones (§9). Unordered history may not pick a first error or ordered result.
- **Milestone 4 snapshot ownership:** `freeze` can first be used by ordinary shells, so checked effectful shells in milestone 5 are not a dependency. Publish exclusive-access/synchronized-snapshot preconditions and reject unknown hooks, live views, and cycles. Optional guards are independently stated additional validation; they never repair missing static callable evidence (§§5.3, 8.2; A34/A35).
- **Milestones 5–8 operation evidence:** effects cannot authorize unknown calls. Import/initialization behavior must be characterized for every operation when it is first admitted, including earlier product/backend operations; milestone 7 expands the standard catalog rather than introducing that obligation for the first time (§§11–12).
- **Milestone 9 useful diagnostics:** editor integration may arrive later, but command rule IDs, first bindings, authored locations, remediation, and usable explanations are milestone 1 capabilities (§14; roadmap milestone 1).
- **A24 sequencing:** A24 places translated-source diagnostics in stage 9 while the optional source format and translator arrive in milestone 14. Preserve the complete requirement by checking compatible-source/editor/guard diagnostics at milestone 9 and the translated-source authored mapping at milestone 14. This is a genuine split gate; it is not a reason to make milestone 9 wait for optional syntax.
- **Milestone 10 policy:** audit baselines never waive strict failures. A smaller finding count must not hide a removed boundary, expanded effects, or new trust (§15).
- **Milestone 11 distribution:** consumer rechecking and installed-artifact contracts add a stronger distribution gate. Normal import and default unguarded execution still require no runtime registry; stale or missing evidence blocks consumer certification, not ordinary Python import (§12).
- **Milestones 12–14 extensions:** builders need escape/lifetime evidence and one-way runtime finalization tokens; concurrency needs preserved effects and explicit ordering/failure behavior; optional syntax needs source mapping and semantic equivalence. None can weaken scalar, caller, or freshness guarantees (§§13, 17).

Observable missing preconditions should be reported as such, not called architectural defects: an unpublished target range, unresolved annotation syntax, unavailable caller evidence, or unspecified build output/evidence selection blocks the relevant acceptance witness. The specification already directs these decisions to be settled before admission (§18). This review adds no requirement for a runtime boundary guard, universal shell analysis, hostile-code isolation, or runtime mutation surveillance.

## Observed implementation probes, October 9, 2026

These are intermediate observations while the builder is still editing, not final release results. Each was passed as source text to the existing internal `pyalamode.checker.analyze_source(source, path=...)` entry point; application source was not executed. This entry point does not itself establish the CLI's supported-interpreter gate. Unless otherwise stated, the observed result was **status 0, `verified=True`, no diagnostics**. The expected gate is a verification failure for the identified unresolved contract. Line citations below refer to the checker snapshot inspected during the probes and may move when corrected.

### P01 — relevant module aliases are not tracked through writes

```python
import builtins as library
from pyalamode import fun
alias = library
alias.abs = lambda value: value + 1
@fun
def magnitude(value: int) -> int:
    return abs(value)
```

Observed: admitted, one selected function. Attribute writes were collected at `pyalamode/checker.py:166`, but approved builtin modules at line 422 recognized only direct import bindings. `alias` was never related to `library`. This is an explicit source mutation of a relevant dependency, not a request to certify every ordinary shell effect (§5.2; A06.7).

### P02 — a recognized global namespace write can change admission

```python
from pyalamode import fun
namespace = globals()
namespace["abs"] = lambda value: value + 1
@fun
def magnitude(value: int) -> int:
    return abs(value)
```

Observed: admitted, one selected function. The literal key identifies the relevant global binding that overrides the approved builtin. This is a bounded recognizable mutation; arbitrary unknown ordinary calls remain governed by disclosed execution preconditions, rather than an invented whole-shell purity gate (§5.2; A06.8).

An input-evidence variant was also admitted with one analyzed call:

```python
from pyalamode import fun
@fun
def selected(value: int) -> int:
    return value + 1
value = 1
namespace = globals()
namespace["value"] = "wrong"
selected(value)
```

The caller's exact-integer evidence is stale after the explicit namespace write. The retained environment at `pyalamode/checker.py:475` must not prove this call admissible (A04).

### P03 — annotation target replacement is missed

```python
import builtins
from pyalamode import fun
builtins.int = str
@fun
def increment(value: int) -> int:
    return value + 1
```

Observed: admitted with an exact-int parameter contract. Annotation resolution at `pyalamode/checker.py:131` checked ordinary name writes but not replacement of the builtin type binding. Actual source target resolution is required without evaluating the annotation (§§5.2, 6).

### P04 — an imported or qualified marker can have been replaced

```python
import pyalamode
pyalamode.fun = lambda function: function
from pyalamode import fun
@fun
def increment(value: int) -> int:
    return value + 1
```

Observed: admitted. Marker validity at `pyalamode/checker.py:121` considered the Name import stable without incorporating the source write to the imported module's marker attribute.

The alias form was also admitted:

```python
import pyalamode as pal
alias = pal
alias.fun = lambda function: function
@pal.fun
def increment(value: int) -> int:
    return value + 1
```

Expected: do not guess that either decorator is the unchanged approved marker; report resolution/rebinding or explicitly withhold selection/evidence. The latter alternative must be visible, not a successful certificate for the function (§§4.1, 5.2).

### P05 — an earlier callable alias receives the later definition's contract

```python
from pyalamode import fun
@fun
def selected(value: int) -> int:
    return value + 1
alias = selected
@fun
def selected(value: str) -> str:
    return value + "!"
alias("wrong for actual target")
```

Observed: admitted, two selected functions, one analyzed call. The actual alias retains the integer function. The contract dictionary was overwritten by name, and ordinary aliases at `pyalamode/checker.py:433` pointed to the final string contract; `_call_inputs` at line 498 only guarded direct calls whose spelling equaled the contract name. The call therefore passed with a known inadmissible argument (A04; §5.2).

Removing the alias and final call also produced two same-name current checked contracts without a finding. Evidence must distinguish actual exposed bindings or reject their analyzed replacement; duplicate logical names must not let a caller choose a contract for a different function object.

### P06 — further explicit binding forms need dependency resolution

```python
from pyalamode import fun
match (lambda value: value + 1):
    case abs:
        pass
@fun
def magnitude(value: int) -> int:
    return abs(value)
```

Observed: admitted. `_written_names` at `pyalamode/checker.py:63` did not collect `MatchAs`, `MatchStar`, and `MatchMapping` string-valued capture fields. Patterns remain excluded in strict bodies, but an ordinary shell's explicit capture can still replace a dependency used by a checked body (§§5.2, 7).

Both additional bounded writes were also admitted:

```python
from pyalamode import fun
def patch():
    import builtins as library
    library.abs = lambda value: value + 1
patch()
@fun
def magnitude(value: int) -> int:
    return abs(value)
```

```python
import builtins
from pyalamode import fun
setattr(builtins, "abs", lambda value: value + 1)
@fun
def magnitude(value: int) -> int:
    return abs(value)
```

The first requires respecting the local import's actual module target; the second uses an explicit literal relevant attribute. Neither requires executing `patch`, the lambda, or `setattr` during analysis (§5.2).

### P07 — analyzed calls are skipped in definition expressions and match suites

Use this common preamble with each suffix independently:

```python
from pyalamode import fun
@fun
def integer(value: int) -> int:
    return value + 1
```

```python
class Shell(integer(True)):
    pass
```

```python
def shell(value: integer(True)):
    pass
```

```python
match True:
    case True:
        integer(True)
```

Observed for each complete fixture: admitted, **zero** analyzed call sites. Ordinary-caller traversal at `pyalamode/checker.py:461` skipped class bases, function annotations, and match-case bodies. These direct calls have known wrong input types and are present in selected source; their effects do not need certification, but their callee obligations still need checking without executing definition expressions (A04; §§5.1, 6).

### Correct observations and a corrected intermediate issue

- A03.4's early-return example passed with no diagnostics. A03.3's reachable second initialization failed with `PAL101` at the second assignment and the first binding identified; downstream missing/result findings were also emitted.
- A07.2's malicious default was rejected with `PAL120`; the poison function was not executed.
- A04.5's ordinary annotated caller failed with `PAL221` for unknown exact-input evidence. The checker correctly did not treat an ordinary `int` annotation as proof of exact integer values.
- A prior false failure from recursively inspecting an ordinary `if` suite before establishing its local bindings was corrected during the review. A fixture with `if flag: value = 1; return selected(value)` subsequently passed with exactly one analyzed call.

### Retest after dependency and caller corrections

The complete P01–P07 direct-source regression set was rerun after the builder signaled readiness. All previously admitted relevant-binding changes and missed direct caller obligations now produce **status 1, `verified=False`**. Marker replacement produces `PAL120`, annotation target replacement produces `PAL130`, dependency/duplicate-export changes produce `PAL240`, and invalid direct callers produce `PAL221`. Both no-call duplicate definitions and the retained-earlier-alias counterexample are rejected. The correct early-return and branch-local exact-input examples continue to pass, and an unrelated qualified `.fun` decorator leaves zero selected functions.

Source/primitive freshness now includes the implementation's `foundation_identities()` product artifact digests in its fingerprints. The earlier constant-only dependency concern is corrected in the inspected implementation. Read-only CLI observations also passed: the existing pricing example checked successfully with one inspected caller and unguarded evidence; the invalid reassignment fixture audited with status 0/`verified=False` and first-binding evidence; an unsupported requested target returned status 2. These results do not themselves establish Linux execution, the artifact/build tests, or measured user onboarding.

### P08 — lambda defaults must use the enclosing scope

```python
from pyalamode import fun
@fun
def integer(value: int) -> int:
    return value + 1
shell = lambda integer=integer(True): integer
```

Observed after the P01–P07 corrections: **status 0, `verified=True`, zero inspected calls**. The lambda's parameter shadows `integer` in its body, but not in its default expression. The default contains a direct call to the checked export with exact `bool`, which must fail the exact-integer obligation without evaluating it (A04; §§5.1, 6). A control using `lambda value=integer(True): value` correctly fails with `PAL221` and one inspected call. This residual is within direct same-file caller coverage, rather than a demand for arbitrary indirect-dispatch analysis.

Two smaller scope observations remain to distinguish from that false admission: an entirely unrelated ordinary decorator named `fun` without any `pyalamode` import is still selected by spelling, and an ordinary `*integer` parameter is not treated as a shadowing local when resolving `integer(True)`. Both are false positives in ordinary shells; they do not establish missing purity enforcement. Chained aliases such as `first = second = integer; first(True)` were not inspected; either support that finite form or explicitly list it outside the initial caller vocabulary and retain the caller obligation. Do not silently describe an uninspected call as validated.

Retest P08 and any changed caller resolution before claiming milestone acceptance. Preserve explicit limitations for caller forms outside the published finite coverage.

### P09 — unreachable code still has a closed expression vocabulary

```python
from pyalamode import fun
@fun
def calculation() -> int:
    return 1
    value = unknown_operation()
```

```python
from pyalamode import fun
@fun
def calculation() -> int:
    if False:
        value = []
    return 1
```

Observed: both admitted with status 0/`verified=True`. `_dead_surface` checks statement classes but not unsupported expressions nested in an admitted assignment. These examples have no reachable hidden effect; the finding is the narrower closed-vocabulary/build-gate obligation, not a claim that they produce impure execution. Unless deliberately specified as an extension, mutable literals and unknown calls remain excluded in participating source (§6; A06). Reject unsupported expression surface while preserving §7's reachability-sensitive binding rule; an unreachable equal-value reassignment must not be confused with this unsupported-expression case.

The independent finite scalar matrix passed **17 accepted expressions and 22 rejected expressions**, covering exact integer/Boolean/string/bytes/None values, scalar operations, builtin arity/type/signature rules, and deferred numeric/container/format/index/method forms. Fixture function names were kept distinct from builtin operation names so the positive builtin tests did not accidentally introduce real shadowing.

### Final independent regression result

After the last caller/dead-source corrections, **25 independent regression fixtures produced their expected results, with zero unexpected admissions or rejections**. This set reran every P01–P07 dependency/caller counterexample, P08 and P09, chained aliases, ordinary parameter/variadic shadowing, unrelated markers, branch-local exact calls, early returns, and an unreachable equal-value binding.

P08 now fails with `PAL221` and exactly one inspected call. P09's unknown call fails with `PAL230`; its mutable literal fails with `PAL201`. A chained alias call with a Boolean input now fails with `PAL221` and one inspected call. An ordinary variadic parameter correctly shadows the checked global function, and an unrelated ordinary decorator named `fun` now leaves zero selected functions. The early-return, branch-local exact-input, and unreachable admitted-binding controls pass.

No residual strict false admission remains among the exercised fixtures. These are finite conformance results, not an assertion of all-Python caller coverage. Artifact/cache/platform tests and target-user usability evidence remain separate gates owned by the full acceptance workflow.
