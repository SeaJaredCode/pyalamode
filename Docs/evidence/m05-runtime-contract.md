# M5 ordinary runtime contract

The new runtime is original product code in `pyalamode/effects.py`. It adds no installed dependency, vendored implementation, callable-certification registry, mandatory function wrapper, or special loader. Stock CPython 3.13.1 and its standard-library/OS bindings supply the disclosed foundations under their existing licenses. Setup factories are ordinary shell operations. A successful static source check never evaluates application definitions or providers.

## Declarations and annotations

`effects(*families)` requires one or more unique exact strings from `IO`, `State`, `Clock`, `Random`, and `Environment`. The exported tokens are those fixed strings; Task and unknown names fail. The returned declaration returns its argument identically, with no metadata changes, registration or wrapping. It supplies no runtime callable evidence. The checker establishes participating source and actual effect requirements separately.

`Effectful[[T1, ...], R, Clock, ...]` is an annotation-only exact `types.GenericAlias`. It copies its exact parameter list into an immutable tuple and uses a finite closed data/Callable/Effectful schema parser without `eval`, `get_type_hints`, application type subscriptions or foreign class hooks. Exact capability parameter slots require the corresponding family; capabilities cannot occur in nested ordinary data, pure Callable slots, or results. Nested fixed Callable and Effectful schemas are supported. Future annotations retain ordinary Python string behavior; the product does not evaluate arbitrary annotation strings to establish callback evidence. An annotation alone never certifies an ordinary function's effects or captures.

## Exact providers and catalog

All providers have an exact opaque family class with no instance dictionary. Direct construction, subclassing, ordinary attribute writes/deletes, and hashing fail. Public repr identifies only the family. There is no application-provided callback, getter, storage implementation or context-manager protocol. Factory payloads are recursively exact closed tuples/integers/strings, validated before comparisons, membership or traversal. Subclasses and malformed metadata fail without foreign hooks. Reflection or unchecked replacement of private/product/foundation definitions violates the dependency assumptions; these properties do not isolate hostile Python.

| Ordinary factory | Exact setup contract | Operations |
| --- | --- | --- |
| `live_io(root, *, allowed_ops)` | Existing root directory as exact str; explicit unique nonempty tuple subset of `('read_text', 'write_text')` | Rooted UTF-8 whole-file read/replacement |
| `recorded_io(entries, *, allowed_ops)` | Exact tuple of unique `(relative_path_str, text_str)` tuples; same explicit permissions | In-memory read/replacement of recorded text |
| `state(initial)` | Exact int, including negative values | `get() -> int`; `set(int) -> None` |
| `live_clock()` / `recorded_clock(values)` | Live OS clock / exact tuple of int timestamps | `now_ns() -> int` |
| `live_random()` / `recorded_random(values)` | Live OS entropy / exact tuple of int samples | `below(positive_exact_int) -> int` in `[0, bound)` |
| `live_environment()` / `recorded_environment(entries)` | Live process environment / exact tuple of unique `(name_str, value_str)` tuples | `get(name_str, default_str) -> str` |

Recorded clock/random reads consume one item on success and raise `IndexError` at exhaustion. A recorded random value outside the requested bound raises `ValueError` without consuming it. Recorded IO reads raise `KeyError` for missing paths; writes update or add one entry. Environment lookup uses the explicit default when missing; names must be nonempty without `=` or NUL. No recorded provider changes its interface effect classification, even for repeated identical observations or singleton random bounds.

Live randomness implements rejection sampling directly from `os.urandom`: for `bound > 1`, take `k = (bound - 1).bit_length()`, mask a sampled byte sequence to k bits, and retry values at least bound. Uniform independent OS bytes make each k-bit value uniform; accepting the first value below bound gives a uniform result over `[0,bound)`. Acceptance probability is greater than one half, so expected draws are below two under that assumption. There is no fixed retry count or universal termination/timing guarantee. `bound == 1` returns zero without reading entropy and still has the Random interface effect. The product no longer imports secrets/random, avoiding their module-global entropy/clock initialization. OS entropy integrity and availability remain trusted assumptions.

All capabilities are excluded from existing record/collection/snapshot/thaw/data-guard schemas. Static source additionally excludes capability aliases, defaults, global constants, captures and stable returns. Ordinary Python may retain multiple references to a root provider; the runtime does not infer unique ownership. Checked invocation/callback slots lend exact family capabilities for their call duration. Current analyzed IO caller matching conservatively requires both public IO operations for any IOCapability slot; known narrower providers remain usable in the ordinary shell but do not establish that full checked interface contract.

## Rooted IO and logical borrowing

Paths are exact nonempty strings with nonempty slash-separated components, excluding absolute paths, `.`, `..`, NUL and backslash. Setup canonicalizes the root with `realpath` and requires an existing directory; root symlinks may resolve during setup. Each later operation checks every path component with `lstat` and refuses any symlink before opening. Missing components are left for the ordinary open operation to report; the library does not create directories. UTF-8 strict decoding/encoding and `newline=''` preserve text newline characters. Write truncates/replaces one file, is not atomic and can leave partial or truncated content on failure.

The runtime opens each file inside a builtin context manager and reads/writes/closes within that operation, including body-failure cleanup. It never exposes a persistent stream, reader, session, cursor or OS resource-transfer API. Read/write failures can propagate `OSError` or `UnicodeError`; denied permissions and symlink components use `PermissionError`. Tests observe actual opened streams closed after successful IO and malformed UTF-8 read/surrogate-write failures. If open fails before returning a stream there is no acquired stream to release. External OS close failures follow CPython's ordinary cleanup behavior; the product does not guarantee success of an unavailable underlying resource release.

Path checks and opening are separate system calls. Callers must preserve the canonical root and path components against replacement/symlink races for the duration of each operation, supply allowed permissions and a supported filesystem, and preserve product/stdlib/OS dependency bindings. Those assertions are not detected ownership, an atomic no-follow filesystem operation, or a security sandbox. Process environment mutation, filesystem content, clock values and entropy remain external effects.

`with borrow(capability) as scoped:` creates a single-use logical lease and a fresh exact same-family view over the same provider state, permission set and recorded cursor. Normal/exceptional exit permanently closes its view. Nested leases reference their parent, so closing an ancestor invalidates active descendants; closing a child leaves its parent live. The original root remains live. The context returns false from `__exit__`, preserving body exceptions, and rejects reentry/repeated exit/use after close. This is logical interface lifetime, not exclusive access, OS-handle ownership or transfer. Concurrent use/synchronization is not characterized. Private lease-cycle forgery is refused finitely rather than traversed indefinitely.

## Failures and trust inventory

Under valid interface inputs and dependency/lifetime assumptions, State operations have no additional domain failure; recorded Clock/Random can raise `IndexError`; Random invalid bounds/samples use `ValueError`, and live entropy can raise `OSError`; Environment encoding can raise `UnicodeError`; IO has `KeyError` for missing recorded paths and `OSError`/`UnicodeError` for live operations. Setup uses `TypeError` for unsupported exact types and `ValueError` for invalid values/duplicates/permissions/path/name, plus filesystem `OSError` (including `NotADirectoryError`). Invalid/malformed ordinary inputs fail `TypeError`, and closed/reused logical leases fail `RuntimeError`; these do not make invalid calls satisfy the interface contract. Resource exhaustion, interruption and divergence remain separate from finite domain failures.

Actual new reads in the runtime include builtin `type`, `str`, `int`, `tuple`, `list`, `len`, `enumerate`, `any`, `next`, `object`, `classmethod`, `open`, the named builtin failure classes, and class/import machinery. Annotation handling reads `types.GenericAlias`, `typing._CallableGenericAlias`, `collections.abc._CallableGenericAlias`/`Callable` and existing closed `records._annotation_schema` foundations. The exact native int `bit_length`/`from_bytes` operations supply live random integer decoding.

IO additionally reads `os.path.join`/`realpath`/`isdir`, `os.lstat`, and `stat.S_ISLNK`; their CPython POSIX transitive definitions read `os.fspath`, `os.getcwd`/`getcwdb`, `os.readlink`, `os.stat`, `posixpath._get_sep` and `genericpath._check_arg_types`/`isdir`, `stat.S_IFMT`/`S_IFLNK`/`S_ISDIR`/`S_IFDIR`, builtin `isinstance`/`bytes`/`OSError`/`BytesWarning`, and ordinary exact string/list/dict operations. The false `strict` branch of root realpath does not call its errno error formatting path. Native `open` produces CPython TextIOWrapper context/read/write/close and UTF-8 codec behavior. Random reads `os.urandom`; Clock reads `time.time_ns`. Environment reads `os.environ`, its `_Environ`/Mapping get/item and stored encode/decode/data machinery, with builtin `isinstance`/`str`/`KeyError`. The OS environment mapping captures filesystem encoding at interpreter initialization; `sys.getfilesystemencoding` is a setup dependency rather than a read at every lookup.

`EFFECT_FOUNDATIONS` in the checker records the concrete finite writer gate. Whole known runtime/product-helper module mutations may conservatively invalidate the entire relevant effect foundation; this does not admit source calls to those names or claim minimal cache invalidation. Standard interpreter/library initialization is trusted separately from checked application initializer source. Product module imports create catalog/classes only; no capability factory, entropy/clock/environment observation or IO operation is run by `effects.py` initialization.

## Source costs

Let h be a logical lease depth, n recorded name/value entries, b the live random bound bit width, p path components, and t UTF-8 text size. Costs include exact scalar lengths/bit widths and ordinary allocation/OS latency.

| Work | Source work and storage |
| --- | --- |
| State/clock/cursor operation | Fixed metadata checks plus O(h²) identity-only lease-cycle/liveness scan; recorded cursor lookup O(1); one private provider/cursor |
| Borrow enter/use/exit | Entry/use liveness checks O(h²); fresh O(1) view+lease; exit O(1); retained nested views hold parent chains |
| Recorded IO/environment setup | O(n²) duplicate-name comparisons plus validation/copy of exact tuple metadata |
| Recorded IO/environment lookup | O(n) pair/name validation and search plus scalar comparison lengths |
| Recorded IO write | O(n) search and O(n) tuple replacement/copy; earlier ordinary root aliases observe the shared provider update |
| Live random | Expected fewer than two entropy reads under uniform independent bytes, O(b) integer/byte work per draw and O(b) temporary storage; variable retries |
| Live IO | O(p) path system calls plus open/read/write/close and O(t) UTF-8 data; external filesystem cost uncontrolled |
| Live environment | Exact name/default validation plus OS mapping/encoding lookup; external process environment dependence |
| Runtime Effectful schema | Finite recursive schema traversal using the existing record identity-only metadata scans; canonical immutable parameter tuple |

These are source bounds, not latency guarantees or target-user measurements. Actual generated-artifact trials, allocation scope, hardware, full product/owned source identities and verification counts are published in the separate measurement report after product freeze.
