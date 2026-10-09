# Pyalamode

Pyalamode checks a functional core in ordinary Python. The current M4 increment supports scalar functions, functional modules, recursive tuples, eager persistent collections, fixed typed records, persistent replacements, explicit shell snapshots and fresh exports, finite dataclass/namedtuple adapters, and optional generated data guards. Checked callbacks, stable constants, recursion, captures, and defaults retain their existing contracts. Accepted code runs through normal Python imports and commands. Checking parses application source without importing it or evaluating its hooks.

The supported check/build target is **CPython 3.13.1, standard GIL build, on macOS or Linux** (`cpython-3.13.1`). Other patches/minors, free-threaded builds, interpreters, and platforms fail the target gate. Installation under another Python 3.13 patch does not establish compatibility.

## Install and run

```sh
python3.13 --version
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
pyalamode check examples/scalar.py
python examples/scalar.py
pyalamode check examples/modules --no-cache
python -m examples.modules.demo
pyalamode check examples/collections --no-cache
python -m examples.collections.demo
pyalamode check examples/records --no-cache
python -m examples.records.demo
```

The scalar example prints `1300` and `0`. The module example prints `1500`, `6`, `6`, and `2`. Its checked core uses stable imports, defaults, a closure, a recursive calculation, and tuple inputs; its ordinary demo prints those results without receiving a purity claim.

One function can opt in with the runtime identity marker:

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
```

A module can opt in without importing that marker:

```python
"""Calculation core."""
# mode: fun

SERVICE_FEE = 200

def quote(cents: int, discount_cents: int = 0) -> int:
    return cents - discount_cents + SERVICE_FEE
```

The directive occurs once after any shebang, encoding declaration, and module docstring, before executable statements. A misplaced directive or region toggle fails. Module mode selects functions, nested definitions, and initialization. In an ordinary module, `@fun` selects that function and its nested definitions, defaults, annotations, captures, and dependencies; unrelated initialization stays unchecked.

Projects can require module mode without source markers:

```toml
[tool.pyalamode]
schema = 1
require_modules = ["core/**/*.py"]
```

Patterns are project-relative, case-sensitive glob patterns; `**/` may match zero directories. Absolute paths, parent traversal, and non-string patterns fail policy validation. Required mode also applies to discovered local dependencies matching the policy. Guard policy is described below; other accepted fields retain their closed defaults.

## Exact contracts

Every parameter and result has an explicit supported annotation. Analyzed calls establish the actual value and callable contracts; ordinary annotations alone cannot establish exact runtime inputs.

| Contract | Admitted syntax and meaning |
| --- | --- |
| Scalars | Exact `int`, `bool`, `str`, `bytes`, `None`; stable `types.NoneType` imports; supported quoted annotations |
| Tuples | Fixed `tuple[int, str]`, homogeneous `tuple[int, ...]`, empty `tuple[()]`; recursive exact immutable data, excluding subclasses and callable payloads |
| Callables | Stable `typing` or `collections.abc` `Callable[[int, str], int]`; fixed positional pure invocation with exact admitted inputs/result and stable captures |
| Collections | Stable `pyalamode` imports of `Vector[T]`, `OrderedMap[K, V]`, `Map[K, V]`, and `Set[T]`; recursively admitted data; map keys and Set elements use one exact scalar domain |
| Records | Exact `@record` declarations with fixed public typed fields and stable defaults; recursive admitted data, pure slot reads, exact type-sensitive equality and `replace` |

Callable parameters express a required input contract. They do not turn an unknown function, lambda, protocol, or ordinary annotated parameter into checked pure evidence. Checked callers supply resolved checked functions or pass a callable already established by their own input contract. Callable annotations allow nested callable inputs/results, but exclude `Any`, ellipsis signatures, variadics, and keyword-only callback shapes. Optional positional defaults and positional-only parameters are compatible when the complete fixed positional call fits. Direct checked calls also support normal positional-only, positional-or-keyword, keyword-only, and default arguments.

A generic admitted callable has the finite invocation failure upper bound **`IndexError`, `KeyError`, `ValueError`, `ZeroDivisionError`, and `RecursionError`**, the current closed operation universe. Conditional callback invocation propagates that bound. Concrete direct targets retain their characterized transitive failures. Reports disclose concrete callback defaults, captures, returned targets, and collection operation identities when established. Recursively nested library validation and equality have a separate conservative `RecursionError` bound.

Stable constants require a single characterized source initialization and no analyzed replacement. Upper-case spelling, `Final`, hashability, a current integer object, and an annotation do not establish stability. A nested function can capture admitted immutable values and checked callables. Changing cells fail, and every required cell must be initialized before a closure is invoked or escapes. Recursion is admitted without a termination claim.

## Supported source

The scalar operations remain integer unary `+`/`-`, integer `+`/`-`/`*`/`//`/`%`, same-type integer/string/bytes comparisons, string/bytes concatenation, boolean `not`/`and`/`or`/equality, right-hand literal `is None`/`is not None`, and conditional expressions. Approved builtin signatures are `abs(int)`, `len(str|bytes|admitted_tuple|product_collection)`, and two-or-more homogeneous positional `min`/`max` over exact `int`, `str`, or `bytes`. Division and remainder disclose `ZeroDivisionError`.

Statements include one-name initialization, annotated initialization, `if`/`elif`/`else`, `return`, `pass`, docstrings, and checked nested function definitions. Each reachable binding initializes once. Exclusive branches may initialize the same name; missing initialization and reachable reinitialization fail. Imports are module-level dependencies.

Module initializers and defaults use closed stable data expressions, earlier stable bindings, approved builtin calls, and checked callable references. **Calling application functions in initialization/default expressions is excluded**, even if their invocation contract is checked. Annotation expressions are parsed from the finite whitelist. Functions admit the resolved identity `fun`; fixed record classes admit the library declaration `record`. Imports, decorators, annotations and defaults must be available when Python evaluates them. Initialization and definition-time default failures are reported separately from invocation failures.

Local imports resolve from the project root with package-before-module precedence and required package initializers. A strict module imports only characterized foundations or functional local modules. Cyclic direct from-imports and eager cyclic namespace reads in initialization/defaults/non-postponed annotations fail `PAL241`; module imports with deferred function references remain supported. This is a finite conservative availability gate. An ordinary module may perform unchecked initialization before using checked exports. Unresolved external APIs receive no trusted admission. A local file named `pyalamode`, `typing`, `types`, or `collections` cannot acquire foundation behavior through its spelling.

Fixed tuples support in-range literal integer indexing and literal slicing; homogeneous tuples support exact integer indexes and slices. Tuple/collection/record equality requires matching recursive exact data schemas. Map/Set membership uses characterized scalar lookup. Loops, comprehensions, destructuring, arbitrary classes/methods, static patterns, mutable strict data, reflection, generators, async, user exceptions/handlers, external trust approvals, and effects remain excluded. Dynamic ordinary dispatch stays the ordinary caller's responsibility. The checker is conservative about unknown aliases, ordinary control flow, and cells outside a checked enclosing scope.

## Eager persistent collections

```python
from pyalamode import Vector, fun

@fun
def total(values: Vector[int], adjustment: int) -> int:
    def adjusted(value: int) -> int:
        return value + adjustment
    def add(accumulator: int, value: int) -> int:
        return accumulator + value
    return values.map(adjusted).fold(add, 0)

original = Vector.of(10, 20)
revised = original.appended(30)
print(original)               # Vector.of(10, 20)
print(total(revised, 5))       # 75
```

Construction uses explicit positional items: `Vector.of(1, 2)`, `OrderedMap.of(("a", 1))`, `Map.of(("a", 1))`, and `Set.of("a", "b")`. Typed empty values use `Vector[int].of()` or `Map[str, int].of()`. Constructors and updates validate deep immutable-data invariants; ordinary runtime generic arguments are erased, so complete parameterized schemas remain static and ordinary-caller obligations. `Vector[int].of(True)` is refused by the checker even though its ordinary runtime value contains stable data. Builtin mutable containers, arbitrary iterators, and callable data members are excluded from strict values; explicit shell snapshots can produce admitted data.

Vectors provide index/slice, `appended`, `updated_at`, `concat`, and eager `map`, `filter`, and `fold(callback, initial)`. Maps provide lookup, `get(key, default)`, `contains`, `updated`, `without`, and right-wins `merge`. OrderedMap provides `entries()`, `keys()`, and `values()` in insertion order. Map provides `ordered_entries()`, `ordered_keys()`, and `ordered_values()` in canonical scalar-key order. Sets provide `contains`, `added`, `without`, `union`, `intersection`, `difference`, and canonical `ordered_values()`. Ignoring a known persistent update fails `PAL250`; bind or return its new value.

Map/Set key domains are exact `None`, `bool`, `int`, `str`, or `bytes`, with one domain per static schema. Their canonical order is singleton None, False before True, ascending integers, and lexicographic strings/bytes. Equivalent unordered values have the same ordered traversal and runtime representation across construction histories and hash seeds. Arbitrary unordered iteration or callbacks are refused; select a canonical Vector before a transform or fold. Vector/OrderedMap order is part of equivalence. Product equality compares exact types recursively, including distinct bool/int payloads. Strict formatting, hashing, and general iteration remain excluded.

The backend reuses stock CPython tuple storage with no added package dependency or vendored backend code. Updates copy O(n) references, and keeping k similarly sized versions can retain O(kn) references; nested value validation adds traversal work. Construction and map merge sort scalar keys, with an O(n log n) comparison bound. This is an eager, useful copying implementation; it does not promise structural-sharing update costs. The [M3 report](Docs/milestones/03-collections.md) publishes every admitted signature, failure/equivalence/order contract, licensing/trust boundary, and measured workload costs.

## Records and explicit boundaries

```python
from pyalamode import Vector, fun, record, replace

@record
class Customer:
    name: str
    tags: Vector[str]

@fun
def tag_customer(customer: Customer, tag: str) -> Customer:
    tags = customer.tags.appended(tag)
    return replace(customer, tags=tags)
```

Records validate complete recursive field schemas, accept positional/keyword fields and stable trailing defaults, preserve earlier values through replacement, and reject ordinary field mutation, reinitialization and subclassing. Public fields named `self` or `value` are supported; constructor/replacement receivers are positional-only. Methods, custom constructors/validators, descriptors, callable fields, bases/metaclasses, private fields, and forward/recursive record declarations have no M4 contract. Runtime ordinary Python patterns use `__match_args__`; static patterns arrive later. Records are unhashable. Record-only checked builds are supported, and evidence separates the checked declaration from the trusted product implementation.

In an ordinary shell, `freeze(raw, exclusive=True, schema=Vector[int])` recursively converts exact list/tuple/dict/set/frozenset input to Vector/tuple/OrderedMap/Set and validates the selected result schema. An explicit schema on a simple stable ordinary assignment establishes data for a subsequent analyzed checked call. `exclusive=True` asserts caller-held exclusive access during snapshotting; it does not detect ownership or acquire a lock. Missing mutable-source preconditions, cycles, subclasses, foreign hooks, and live views fail. Repeated acyclic references are copied by value. `thaw(snapshot)` creates independent fresh nested lists/dictionaries/sets; record exports are field dictionaries. Neither operation is admitted inside pure checked functions, defaults or functional initialization.

`dataclass_adapter(Source, Customer)` or `namedtuple_adapter(Source, Customer)` can qualify a finite exact generated source class for `freeze(source, exclusive=True, adapter=adapter, schema=Customer)`. Source field order/storage/generated behavior and stable defaults must qualify; custom getters/constructors/methods, factories and subclasses fail. The target is a concrete product record with exact nested schema validation. `frozen=True` alone certifies neither behavior nor nested data. The [record demo](examples/records/demo.py) shows source mutation after snapshotting and export mutation without changing retained records.

## Optional guards

```toml
[tool.pyalamode]
boundary_guards = "exports"
guarded_exports = ["examples.records.core:tag_customer"]
```

Build then provides the guarded public alias `pyalamode_exports.examples.records.core:tag_customer`, imported normally with `from pyalamode_exports.examples.records.core import tag_customer`. It validates exact supported arguments before the original body and returned data afterward. Original-module functions remain unwrapped and unguarded in exports mode; checked internal calls use those originals. Guards are off by default and do not freeze inputs, prove effects/ownership/callback purity, or monitor dependency tampering. M4 refuses selected Callable boundaries. Unknown, ambiguous, duplicate and conflicting selections fail.

`boundary_guards = "debug"` additionally inserts supported exact data assertions at selected function parameters, local bindings and returns in copied source. Reports list coverage; callable evidence obligations remain. Debug assertions add repeated traversal and ordinary import/allocation overhead. The [M4 handoff](Docs/milestones/04-records.md) and [runtime contract](Docs/evidence/m04-runtime-contract.md) publish guard behavior, costs, snapshot preconditions, adapter limits and evidence.

## Check, build, and inspect

```sh
pyalamode check examples/modules --json
pyalamode build examples/modules --output build/modules-first-use
python -m examples.modules.demo
pyalamode check --audit tests/fixtures/m02/changing_capture.py
pyalamode explain PAL240
pyalamode explain tuple
pyalamode explain Callable
pyalamode explain Vector
pyalamode explain PAL250
```

A build freshly checks selected source and resolved local dependencies, copies unchanged Python bytes in off/exports mode, optionally generates the selected façade/debug assertions, and writes `pyalamode-evidence.json` in a fresh output directory. To run a copied example, enter that directory and run `python -m examples.records.demo` with the installed Pyalamode library available. Builds require a participating function, record declaration or functional module, reject existing outputs, and publish no artifact after a failed gate, generated-source compile error or freshness check. Package distribution and consumer verification are later milestones.

Strict failures return status 1. Tooling, syntax, policy, and unsupported-target errors return 2. Audit findings alone return 0, label evidence unverified, and leave ordinary behavior unchanged. An empty ordinary selection may pass `check` but supplies no participating function or module claim. The same commands are available as `python -m pyalamode`.

At runtime, `fun(function)` returns that identical function object. It does not wrap, register, guard, or create check evidence. Ordinary callers satisfy exact recursive data/callback contracts and leave dependencies/captures unchanged; selected generated aliases add only their stated data coverage. Unchecked monkey-patching violates the execution precondition; no live dependency monitor is installed. Resource exhaustion, interruption, interpreter tampering, and arbitrary dynamic Python are outside the guarantee.

Disposable `.pyalamode-cache` entries include source bytes, target, policy, product identities, transitive local import bytes, resolution identities, and relevant analyzed binding replacements. An unchanged warm check reuses body evidence. A dependency edit invalidates its import closure; unrelated modules can retain hits. Adding an ordinary writer that replaces a referenced callable or foundation binding also invalidates affected evidence. Import closures are conservative: unused local imports and unrelated edits within an imported file can invalidate callers. Missing or corrupt cache entries trigger fresh checking. Builds bypass the cache and recheck source/dependency bytes and policy before publication.

## Verification and handoff

```sh
python -m unittest discover -s tests -p 'm0*.py' -v
python benchmarks/m01_scalar.py --output /tmp/pyalamode-m01.json
```

The M4 suite inherits the earlier adversarial guarantees and adds fixed record/schema/definition evidence, nested record validation, retained replacements, exclusive snapshot assertions, foreign hook/metadata refusal, fresh by-value exports, finite adapter qualification, selected guard entry/return coverage, internal-call isolation, debug coverage, circular initialization refusal and runtime-byte/policy/writer freshness. See [the M4 handoff](Docs/milestones/04-records.md), [the M3 handoff](Docs/milestones/03-collections.md), [the M2 handoff](Docs/milestones/02-modules.md), and [the composite specification](SPEC-sol6.1-composite.md). Human authoring-time and usability claims remain unmeasured.
