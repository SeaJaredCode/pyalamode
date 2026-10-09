# M11 explicit stable value encoding: plan and observed engineering evidence

Status: implemented under root's explicit release of the accepted 290-line plan, SHA-256 `28b8f14ffc7eb8066810ae356795341a1bea30ec516c1eec0da78be7f1fbdb0a`. Final engineering gates passed on both supported platforms: 461-method suites, fresh installed walks and the independent original 78-case corpus. The one approved codec cost protocol completed on native then Linux; root independently reconciled its fixed wire grammar, receipts, counts and measurements. Plan and development provenance remain below, followed by final observations. Human usefulness is **UNMEASURED**, zero participants and attempts.

## Authority and inspected baseline

This bounded increment implements the final paragraph of composite specification §12, together with §3.1 equivalence, §6 exact scalar types, §8 stable data, §9 canonical unordered traversal, §10 closed records/variants and §11 implicit dispatch. It does not provide pickle compatibility, general object serialization, transport, a schema service or runtime purity certificates.

The inspected baseline is milestone 10 commit `9108a81`. Root's `/tmp/pyalamode-m10-root-freeze.json`, SHA-256 `20d293ccb4781b64fc16ada3eff48f4b5951c135d8eb8e6930a23f6fda5f98a5`, remains the inherited source gate. Its 401-method platform suites and installed consumer gates are historical verified prerequisites; this planning unit does not rerun them. The complete composite specification, README and orchestration ledger were read. No applicable `AGENTS.md` exists at this workspace or its ancestor paths.

Relevant implementation facts read from the unchanged sources:

- `collections.py` uses exact tuple storage, homogeneous exact scalar map keys/set members, type-sensitive recursive equality, ascending scalar canonical order and trusted `object.__new__` allocation. OrderedMap preserves first insertion slots. Map/Set constructors normally deduplicate and store canonical order, but a codec must independently reject malformed/duplicate forged storage instead of normalizing it silently.
- `records.py` admits fixed product classes by identity in `_RECORDS`; fields are typed fixed slots with `_pal_initialized`. Its `_annotation_schema` vocabulary is finite and never evaluates strings, but its ordinary namespace/string support is unnecessary for the codec and will not be called on arbitrary schema objects.
- `variants.py` stores exact closed families/cases in `_VARIANTS`/`_CASES`; user cases have fixed typed slots. Option/Result payload schemas are erased at runtime and therefore require an explicit complete schema at the codec call. Domains are namespaces, not constructors.
- `Failure` is an ordinary exact product record of two exact strings. A codec encodes that immutable value, never an exception, traceback or frame.
- The current checker parses annotation ASTs and distinguishes pure operation evidence, external trust, effects, invocation failures and separate initialization. Existing standard functions use positional-only finite signatures and detached catalog data. The primary worker owns extending that integration.

## Ownership and finite public API

The helper owns exactly these five implemented/prepared files:

1. New `pyalamode/encoding.py`: runtime codec and closed schema compilation/parser.
2. New `pyalamode/encoding_contracts.py`: detached versioned metadata only.
3. New `tests/m11_encoding.py`: focused runtime and primary-integrated static regressions.
4. New `benchmarks/m11_encoding.py`: the single shared codec cost controller described below.
5. This `Docs/evidence/m11-encoding.md`: settled behavior, implementation evidence and limitations.

The primary owns `__init__.py`, checker/model/project/CLI, reports/explain/freshness/writer integration, packaging/consumer workflows, public example and README. The independent reviewer owns literal conformance oracles. No helper edits central files, inherited tests, README, examples or other milestone evidence.

There are exactly two public operations, available as resolved `pyalamode` exports or from `pyalamode.encoding`:

```python
value_encode(value, schema, /) -> bytes
value_decode(data: bytes, schema, /) -> T
```

The schema is required, positional-only, and denotes the complete exact data schema `T`. There are no callbacks, custom serializers, factories, mutable options, runtime schema objects, schema inference, unions, subclass admission or automatic coercion. Runtime accepts only approved scalar/type identities and exact `types.GenericAlias` combinations of the existing data vocabulary. Runtime string/quoted schema arguments are rejected. `None` and `type(None)` denote the same None schema. `tuple[()]` denotes the empty fixed tuple. Existing complete `Option[T]`, `Result[T,E]`, `Some[T]`, `Nothing`, `Ok[T]` and `Err[E]` schemas remain distinct explicit roots.

Catalog interface agreed with primary:

```python
ENCODING_VERSION = "pyalamode.encoding-v1"
ENCODING_NAMES = frozenset({"value_encode", "value_decode"})
ENCODING_FOUNDATIONS = {...}  # module -> frozenset of actual native reads
operation_contract(name)     # detached dict or None
operation_catalog()         # detached list containing exactly the two operations
```

`operation_contract` accepts the public short name or `encoding.<name>` operation ID. Runtime identity is `pyalamode.encoding.<name>`. Metadata includes complete signatures, bounds, exact schema vocabulary, effect/failure/initialization/alias/dispatch/evidence/foundation contracts and ordinary invalid input categories. It contains no runtime application classes or callable objects.

## Static integration and evaluation order

Python retains normal left-to-right argument evaluation: resolve callable, evaluate value/data expression, evaluate explicit schema expression, enter the codec. No transform changes compatible source. The checker, without importing or evaluating application code, resolves argument two as a supported annotation AST under the actual lexical bindings and declaration availability at that location. Annotation spelling cannot acquire admission when a scalar, collection, record or domain name is shadowed or replaced.

Primary's finite integration obligations are:

- Exactly two non-starred positional arguments and no keywords. Unknown/spoofed callee identities fail as normal unknown operations.
- `value_encode` requires recursively established exact data of schema `T`, including bool/int distinction, correct nominal identity and complete Option/Result alternatives. It returns exact bytes.
- `value_decode` requires established exact bytes. On success its return is the exact selected schema `T`; malformed bytes do not establish any value.
- Argument two is a schema expression, not an admitted first-class value or callable. No `Callable`, Effectful, capability, builder, `Any`, ellipsis callable, arbitrary subscription, union, runtime string or unresolved nominal type can pass.
- Both operation IDs propagate product trust, schema declaration/source dependencies and transitive inherited collections/records/variants foundations. Exact source bytes of both new modules join product fingerprints and published installed identities. Known analyzed writers invalidate actual aliases/imports/catalog/helper/globals/class/native dependencies before strict admission; a spelling-only declaration never suffices.
- Invocation effects are empty. Known invocation failures are `ValueError` and conservative `RecursionError`; ordinary inadmissible inputs additionally raise `TypeError`. Existing `ValueError` handlers may discharge characterized codec failure without erasing trust or other effects. The general callable failure bound already includes these failures.
- Codec invocation is admitted in checked function bodies only for this increment, including checked effectful bodies. It is refused in functional initialization/defaults and has no automatic ordinary-annotation evidence rule. An ordinary shell can call the codec directly, while its later checked call still needs existing analyzed data evidence or a selected explicit guard.

No bytes transport is added. File, process, network or environment operations retain their own separately characterized effects and preconditions. Importing the codec performs trusted finite product imports/constant definitions only, with no application module lookup, registry import, external backend, I/O, environmental sampling or callback. Application package initialization remains separately reported.

## Schema admission and metadata read proof

Compilation never calls `eval`, `exec`, `get_type_hints`, string annotation parsing, import-by-name, an arbitrary class, `__class_getitem__`, a metaclass hook or a restoration function. Runtime schema expressions have already been evaluated by ordinary Python before the call; the codec does not evaluate them again. Checked source must establish that evaluating the selected expression is characterized.

Compilation examines only these cases, in this order:

1. Identity comparison against `None`, NoneType and exact scalar classes. It does not hash, compare using arbitrary `==`, format or read attributes of an unknown schema object.
2. Identity comparison through the trusted exact product record/domain/case catalogs, using tuple traversal. Unknown type objects/metaclasses do not become schemas because of nominal metadata or matching attributes. Type admission occurs before any class metadata read.
3. `type(schema) is GenericAlias`, followed by direct native reads of `__origin__`/`__args__` using `object.__getattribute__`. The origin is compared by identity against exact tuple, Vector/OrderedMap/Map/Set and Option/Result/payload-case classes before children are inspected. Arguments must be an exact tuple with the published arity; each child repeats this finite compilation. A foreign origin, union, string argument or unknown child fails without accessing its metadata.
4. For admitted nominal product identities only, read fixed catalog field/case tuples and native type metadata through the original builtin `type.__dict__` GetSetDescriptor/MemberDescriptor operations. The class dictionary, qualified-name slot, name slot and MRO are read directly through those native descriptors, bypassing even the characterized DomainType's custom metadata lookup. Qualified name is a native type slot and need not appear in the class dictionary. Module/slots metadata is taken from the native class dictionary; every value is tested for exact string/tuple shape before any string method or descriptor operation. A user descriptor placed under those names is never read through normal attribute dispatch. Exact string metadata length is checked before `split`, `isidentifier`, joining the nominal label or allocating descriptor bytes: module and qualified names each have at most 1,024 code points and their combined `module:qualified` identity has at most 1,024, including the colon; each field/case name has at most 128. Counts/depth/nodes are likewise bounded before expanding metadata. Field/case names are unique public identifiers. Identities are nonempty dotted Python identifier module and qualified-name components, separated by a single colon. Local `<locals>` identities are unsupported. No object is resolved from that text.

Record/case classes must have the generated exact `type` metaclass and `(class, object)` MRO. Their actual `__slots__` are exactly the fixed fields plus `_pal_initialized`. Every field and initialization slot must still be the native `types.MemberDescriptorType` with its exact expected `__objclass__` and name. Native class/MRO dictionaries must contain no custom `__del__`, so discarded partial decoded objects cannot invoke a foreign finalizer. A replaced field/getter/descriptor, missing slot, spoofed identity, unknown nominal class, forged annotation catalog attributes or subclass fails before user dispatch. Existing trusted catalogs are product implementation state, not user registration or certificates; unchecked replacement of product catalogs/native identities violates the disclosed dependency assumptions. An object with copied metadata cannot join them.

Collection storage descriptors are read from the exact trusted Vector/Set classes and the exact `_MapBase` owner, with the expected inherited MRO and native member descriptor checked. Descriptor operations are direct native `MemberDescriptorType.__get__`/`__set__`; normal instance `getattr`, property lookup, `__getattribute__`, iterator, representation, equality/hash or collection methods are never used on arbitrary inputs. Unknown values are rejected by `type`/identity before any storage read.

Schema compilation validates fixed record/variant catalog shapes recursively, including the entire closed domain case set. Duplicate selected nominal identities among admitted record/domain/attached-case catalog classes are refused, including repeated same-module/same-qualified record declarations, so distinct exact record types cannot acquire the same selected wire schema. Unsupported unrelated registered local class labels do not poison a supported selected schema: collision comparison reads only bounded exact native metadata and does not parse those unrelated labels. Selecting that local schema still fails its nominal spelling contract. The built-in untyped `_DATA` placeholder is never accepted as a selected user schema; Option/Result compilation substitutes the explicit generic payload schema. Schema cycles fail before recursion using active exact identities. Field defaults are neither read nor invoked for decoding; all fields are carried explicitly. Changing defaults alone preserves this wire schema but remains a relevant checked-distribution source freshness change.

Concrete inherited trust limit: `_VARIANTS` captures the original domain identity, but `_RECORDS` stores only actual class/fields/defaults. Without altering that existing declaration mechanism, the codec cannot recover an original record module:qualified name after an unchecked mutation to another unused valid label. Such a mutation violates the class/dependency integrity precondition; it is rejected when analyzed by the checker. Unknown classes with copied labels still fail identity admission, descriptor-shaped metadata fails before dispatch, and duplicate catalog labels fail. This is explicit conditional semantic parity, not a claim of universal runtime nominal tamper detection.

## Bounds and compatibility

All v1 limits are fixed constants, not caller-controlled configuration:

| Domain | Bound |
| --- | --- |
| Total encoded envelope / input bytes | 1,048,576 bytes (1 MiB), inclusive |
| Canonical schema section | 65,536 bytes, inclusive |
| Schema nodes | 1,024 nodes, inclusive; each appearance counts |
| Schema depth | Root depth 0; maximum 32 |
| Fields per record/case | 128 |
| Cases per closed domain | 128; domain is nonempty |
| Nominal `module:qualified` identity | 1,024 code points, including the colon; component metadata is bounded before splitting/joining |
| Field/case name | 128 code points; bounded before identifier parsing |
| Total value nodes | 16,384 nodes, inclusive; repeated references count again |
| Value depth | Root depth 0; maximum 32 |
| Tuple/vector/map/set length | 4,096 elements/entries, inclusive |
| Bytes atom | 262,144 bytes, inclusive |
| String atom | 65,536 Python code points, inclusive |
| Integer encoding domain | `-2**63 <= value <= 2**63-1`, exact int |

These are encoding-domain restrictions only. The broader core retains arbitrary exact integers and existing stable string semantics. Out-of-domain exact integers and finite-limit excess in supported data or exact supported schema metadata produce ValueError; there is no truncation, rounding or saturation. An unsupported schema object/origin/arity, non-exact or malformed metadata, non-native descriptor, invalid nominal/field/case spelling or duplicate nominal identity produces TypeError. Incoming malformed or excessive wire metadata always produces ValueError. Bool is a different tag/type and cannot satisfy int. Floats, Decimal, complex, NaN/context semantics and foreign numeric subclasses are excluded. All Python string code points, including U+0000, Unicode scalar values and lone surrogates, are preserved without normalization or encoding registry dispatch.

The target remains exact CPython 3.13.1 standard GIL on macOS arm64/Linux aarch64 with UTF-8/surrogateescape filesystem configuration. Format version 1 is fixed by the magic/version byte and is independent of allocation identities, hash seeds, native endian, process-randomized hashing and ambient decimal/codec limits. Only v1 is supported. There is no migration/default-field filling, schema alias, duck-typed compatibility or best-effort fallback.

## Exact v1 binary grammar

Numbers `U32` are four big-endian unsigned bytes and `U64` are eight big-endian unsigned bytes, implemented by characterized exact byte/integer shifts and arithmetic. No struct, JSON, pickle, dynamic codec or numeric formatter is used. `TEXT` is `U32(code_point_count)` followed by that many `U32(ord(character))` values; each point is in `0..0x10ffff`, including surrogates. `NAME` is TEXT restricted by the schema identifier rules.

```text
ENVELOPE = 50 41 4c 56 01   U32(schema_byte_length)   SCHEMA   VALUE
           P  A  L  V  v1
```

The schema section has exactly the declared length, exactly one root and no extra bytes. The envelope has exactly one root value and no trailing bytes. Schema and value parsers impose their own separate depth/node counters and size limits before allocating/traversing a declared count.

| Schema tag (hex) | Exact content after the one-byte tag |
| --- | --- |
| `00` None | empty |
| `01` bool | empty |
| `02` int | empty; v1 signed64 bound is fixed |
| `03` str | empty |
| `04` bytes | empty |
| `10` fixed tuple | U32(arity), that many child SCHEMA nodes |
| `11` homogeneous tuple | one child SCHEMA |
| `12` Vector | one child SCHEMA |
| `13` OrderedMap | scalar key SCHEMA, value SCHEMA |
| `14` Map | scalar key SCHEMA, value SCHEMA |
| `15` Set | scalar member SCHEMA |
| `20` record | NAME(module:qualified), U32(field_count), repeated NAME(field), SCHEMA |
| `21` domain | NAME(module:qualified), U32(case_count), repeated NAME(case), U32(field_count), repeated NAME(field), SCHEMA |
| `22` exact domain case | complete `21` domain SCHEMA, NAME(selected_case) |
| `23` Option | payload SCHEMA |
| `24` Result | success SCHEMA, error SCHEMA |
| `25` Some | payload SCHEMA |
| `26` Nothing | empty |
| `27` Ok | payload SCHEMA |
| `28` Err | error SCHEMA |

Record/domain identities use module:qualified names; NAME identity entries apply that grammar and the 1,024-code-point bound instead of the single-public-identifier field/case grammar and 128-code-point bound. The wire NAME count is checked before allocating code-point strings or splitting names. Fixed tuple arity has the 4,096 count limit. Map/set schemas only accept `00..04` key/member schemas. A `22` selected case must occur in its complete domain descriptor. Schema fields and cases retain declaration order and must be unique. Generic Option/Result use their fixed product identities, not mutable caller labels.

| Value tag (hex) | Exact content after the one-byte tag |
| --- | --- |
| `00` None | empty |
| `01` bool | one byte, exactly `00` False or `01` True |
| `02` int | U64 two's-complement signed representation |
| `03` str | TEXT |
| `04` bytes | U32(byte_count), exactly that many raw bytes |
| `10` tuple | U32(count), repeated VALUE; fixed/homogeneous choice is in selected schema |
| `12` Vector | U32(count), repeated VALUE |
| `13` OrderedMap | U32(entry_count), repeated VALUE(key), VALUE(value), insertion order |
| `14` Map | U32(entry_count), repeated VALUE(key), VALUE(value), canonical key order |
| `15` Set | U32(member_count), repeated scalar VALUE, canonical member order |
| `20` record | U32(field_count), field VALUEs in schema declaration order |
| `21` user domain case | U32(zero-based case_index), U32(field_count), field VALUEs in selected case order |
| `31` Some | one payload VALUE |
| `32` Nothing | empty |
| `33` Ok | one payload VALUE |
| `34` Err | one error VALUE |

Value tags are checked against the selected schema and closed alternative at each node. Record/case field count must match exactly. Values contain no field labels, so duplicate/unknown field names can only occur in the separately validated schema section. There is no implicit omission or default expansion. Case indexes outside the selected complete domain are refused. Unknown tag bytes never trigger a fallback.

Before value parsing, the incoming descriptor is parsed as bounded exact primitive metadata and validated for closed shape, counts, key domains, duplicate names and identifiers. Its canonical descriptor bytes must equal the selected runtime schema descriptor byte-for-byte. Unknown symbolic identities are a schema mismatch, never an import request. The decoder only uses the compiled selected schema's actual class references for allocation; it never trusts incoming type names as objects.

Hand-derived independent scalar golden envelopes (not observed candidate outputs):

```text
None / None:    50414c5601000000010000
False / bool:  50414c560100000001010100
True / bool:   50414c560100000001010101
0 / int:       50414c56010000000102020000000000000000
-1 / int:      50414c5601000000010202ffffffffffffffff
```

## Ordering, equivalence and deterministic failures

Within one accepted wire schema, `encode(a, T) == encode(b, T)` exactly when a and b are contract-equivalent under that schema and encoding domain. This includes exact scalar type, complete nominal schema/case tag, recursive payload equivalence and significant order. Different selected schemas are distinct envelope contracts even when sparse values happen to have the same payload (for example Nothing under different Option payload schemas).

Vector and tuple order, OrderedMap entry order and record/case field order are preserved. Unordered Map and Set encode with their published total homogeneous exact scalar order: None singleton, False before True, ascending integers, Python lexicographic code-point strings (including surrogates), lexicographic bytes. Empty key domains come from the explicit schema. Different construction histories/hash seeds cannot change valid bytes, diagnostics returned as exception messages or first semantic failure. No arbitrary key comparator/hash/equality runs.

The encoder checks unordered storage in deterministic phases: exact tuple/pair shape (generic storage path), all keys/members match the selected exact scalar domain (generic keys/members path), canonical native sort and duplicate refusal, then bounded scalar/payload traversal in canonical order. Malformed structural/type/duplicate storage does not disclose an incidental index. In Map payload errors, indexes are canonical traversal indexes. Ordered values use their explicit input order. Unordered duplicate storage is rejected, not collapsed; already constructed normal collections retain their normal value semantics.

The decoder's ordered wire parser selects the first left-to-right malformed condition under its fixed header/schema/value phases. Map/Set wire keys must be strictly ascending under the selected scalar domain; duplicate/noncanonical entries are refused instead of normalized. Malformed wire order is observable bytes supplied explicitly by the caller, never an undocumented hash history.

For any accepted `value` and selected T, `decode(encode(value,T),T)` has T's complete exact recursive schema and is contract-equivalent to value. For any accepted canonical envelope b, `encode(decode(b,T),T) == b`. No record/case allocation identity, repeated-reference identity or mutable alias is preserved. Every decoded collection/record/case has newly owned trusted storage; immutable scalar objects may be reused by stock Python. Callables, live capabilities, builders, mutable collections, arbitrary protocols, iterators/cursors and exceptions cannot become payloads.

## Trusted decoding allocation

The decoder parses and validates each child before allocating its parent. Only actual compiled exact product identities are eligible. For records/cases it uses `object.__new__(exact_class)` directly, writes each validated field with its checked native member descriptor's `__set__`, and writes `_pal_initialized=True` last. It never calls the class, its `__new__`, `__init__`, normal setattr, defaults, validators, `__setstate__`, reducers or restoration hooks. Partial objects on failure remain private and are not returned. Collection allocation similarly uses direct `object.__new__` and the validated native storage descriptor, retaining a new exact tuple of decoded children.

The output cannot be a fake record/case merely because the wire labels match. It is allocated from the consumer's passed, admitted class identity after full structural+nominal schema agreement. Producer and consumer ordinary package imports establish their local schema class objects independently. Checked consumer verification ties imported schemas/operations to actual installed producer bytes and dependency policy; runtime catalogs establish ordinary value structure only. No global certificate registration, class lookup service, import-on-decode or per-invocation distribution certificate check exists.

Symbolic identity plus complete recursive shape permits an ordinary producer/consumer pair using the same installed package namespace and schema to exchange these values even though class allocations differ between processes. A changed record field/type/order, domain case set/order/payload, generic parameter or nominal name refuses old bytes as schema mismatch. Distribution source/policy/artifact/dependency changes still invalidate consumer checked claims independently, even when the wire shape stays compatible.

## Failures and dependency contract

Invalid operations never return a partial value or partially valid byte envelope. Public exceptions use fixed plain path/reason strings without representing a rejected value/type, inspecting arbitrary exception payloads or invoking user formatting. TypeError describes ordinary inadmissible value/schema; ValueError describes supported-domain bounds or malformed bytes. Internal parser index/attribute failures are contained and translated into their fixed malformed condition. Resource exhaustion/interruption and the conservative inherited RecursionError remain outside any termination claim.

Required stable reason vocabulary, with deterministic nested paths, to be fixed in tests before observations:

| Category | Reason |
| --- | --- |
| TypeError | unsupported exact schema; unsupported schema origin/arity; malformed product schema metadata; unsupported nominal/field/case spelling; duplicate nominal identity; non-native product storage descriptor; custom product finalizer |
| TypeError | expected exact selected value type; malformed product storage; uninitialized product storage; cyclic data; keys/members require selected exact scalar domain; duplicate collection key/member |
| ValueError | integer outside signed64 encoding domain; string/bytes/container/node/depth/schema/envelope/nominal-name/field-name/case-name limit exceeded for exact supported data or schema |
| ValueError | truncated envelope/header/schema/value; unsupported magic/version/tag; invalid bool/code point/count; trailing schema/value bytes |
| ValueError | invalid schema identifier/shape/key domain; duplicate schema field/case; selected case absent; wire schema differs from selected schema |
| ValueError | value tag differs from selected schema; record/case field count mismatch; case index outside selected closed domain; duplicate/noncanonical map key or set member |

Paths begin `schema`, `value`, or `data`; fields append `.field_name`, ordered/canonical children append `[index]`, map pairs append `.entries[index].key`/`.value`. Unordered structural/domain/duplicate failures use the parent `.storage`/`.keys`/`.members` generic path. No key representation or allocation identity enters a path.

Direct native read inventory proposed for `ENCODING_FOUNDATIONS` (plus the complete inherited record/collection/domain dependency inventory owned by primary):

- `builtins`: type, object, tuple, list, set, dict, frozenset, len, range, enumerate, zip, any, all, sorted, id, ord, chr, str, bytes, int, bool, next, Ellipsis, TypeError, ValueError, AttributeError, RecursionError, `__build_class__`, `__import__`.
- `types`: GenericAlias, MemberDescriptorType, GetSetDescriptorType, MappingProxyType.
- Exact native operations: int comparisons/arithmetic/bit shifts/bit operations; str ordinal iteration/index/comparison/join/split/isidentifier/startswith; bytes index/slice/construction/comparison; tuple/list/set private storage/traversal/append/extend/add/remove; type.__getattribute__ for the builtin type dictionary; direct native type dictionary/qualified-name/name/MRO descriptors; object.__new__; GenericAlias native origin/args reads; mappingproxy exact lookup; MemberDescriptorType native name/objclass/get/set. Native type creation/decorators and existing schema declarations remain inherited initialization foundations.
- Product reads: exact collection identities and fixed descriptor owners; records `_RECORDS` fixed rows; variants `_VARIANTS`/`_CASES` fixed rows and Option/Result/case identities. If an existing helper is reused, its actual entire direct dependency closure joins this inventory; no broader helper is silently assumed pure.

Codec catalog/module/helper/class/globals writes are included in primary's analyzed writer closure. Existing foundation mutation rules still apply to all inherited data assumptions. Unchecked mutation of implementation/catalogs/classes/builtins after checking violates dependencies; this is stable-value validation under a characterized runtime, not security isolation from hostile interpreter modification.

## Concrete producer/consumer use

The primary will settle the actual example namespace and files; this exact useful shape is available for integration without expanding the operation catalog:

```python
from pyalamode import record, variant, case, Map, fun, value_encode, value_decode

@variant
class InvoiceStatus:
    @case
    class Ready:
        pass
    @case
    class Rejected:
        reason: str

@record
class Invoice:
    order_id: str
    total_cents: int
    labels: Map[str, str]
    status: InvoiceStatus

@fun
def invoice_packet(order_id: str, total_cents: int, labels: Map[str, str]) -> bytes:
    invoice = Invoice(order_id, total_cents, labels, InvoiceStatus.Ready())
    return value_encode(invoice, Invoice)

@fun
def read_invoice(packet: bytes) -> Invoice:
    return value_decode(packet, Invoice)
```

An installed producer publishes the checked `invoice_packet` export and schema declarations. A separate consumer imports that installed schema/export, checks its own `read_invoice` and business rule against current producer evidence, then imports/invokes normally. The ordinary demo passes bytes between them and prints exact retained values. Canonically equivalent label maps produce the same packet. A rejected invoice variant exercises closed tag/payload handling; changed schema/malformed packet/oversized integer refuse. Transport belongs to an ordinary shell or separately characterized IO operation. This demonstrates cents/order/labels/status data interchange; it does not claim measured target-user usefulness.

## Pre-observation adversarial test and measurement protocol

Before implementation observation, owned tests and reviewer literals will fix:

1. Hand-derived scalar golden bytes, signed64 min/max/outside values, False versus 0 rejection, all exact primitive subclasses and unknown protocols.
2. Every schema/value tag, empty/fixed/homogeneous tuple, parameterized empty collections, nested typed records, direct/family cases, Option/Result complete generic roots, Failure and ordered record/default payloads. Both roundtrip obligations are checked recursively by actual exact class/schema and order rather than arbitrary cross-type equality.
3. Map/Set opposite construction histories and at least three process hash seeds, int/string/surrogate/bytes order, OrderedMap/Vector order significance, duplicate/noncanonical malformed wire and forged unordered storage with multiple invalid values whose selected failure stays canonical.
4. Truncation at each scalar/container/header boundary, unknown tags/version/nominal identity, false counts, trailing data, invalid bool/code point, malformed/duplicate/unknown schema fields/cases, exact case closure mismatch, int/size/depth/node limits at and above bounds. Both encoder and decoder limits are exercised without huge unbounded input.
5. Hook sentinels for arbitrary constructors/`__new__`/getters/setters/metaclasses/`__class_getitem__`/reduce/setstate/iteration/hash/equality/formatters/codec registries. Unknown objects/metaclasses/alias origins/unions are rejected before reads; replacements of legitimate product descriptors fail with zero hook calls. Trusted decode with poisoned nominal `__init__`/`__new__`/setters records zero calls while allocating exact validated fields. No decoder dynamic import or namespace lookup occurs.
6. Forged initialized flags, missing slots, cycles, builtin mutable payloads, callable/capability/builder fields, shadowed schemas/callees, class/helper/native/globals writers, lexical unavailable schema expressions, no quoted schemas, no kwargs/starargs, exact decode result evidence and handled ValueError retains other effects/trust.
7. Actual separate installed producer/consumer with current artifact identities, altered relevant schema bytes/version/source evidence refusal and ordinary invocation without any certificate service. Root/primary own the complete package acceptance walk; helper observations remain focused and independently frozen.

The only shared codec cost protocol is `stable_invoice_encoding_v1`, owned by `benchmarks/m11_encoding.py`. It has **12 rows per platform**: two label counts **8 and 256**, times encode/decode, times actual installed **off/exports/debug** checked data exports. Each row performs **10 untimed warmups**, then **three intervals of 25 calls**: 36 intervals, 900 measured calls and 120 warmups per platform. The main and reviewer reference this same protocol; there is no second codec workload or separate guard-throughput protocol.

Each input is exactly one Invoice of the declared shape above, with nominal identities `checked_pricing.core:Invoice` and `checked_pricing.core:InvoiceStatus`, field order `order_id,total_cents,labels,status`, and domain case order `Ready,Rejected`. Value is `order_id="order-41"`, `total_cents=1299`, status `Ready()` and a canonical `Map[str,str]` containing exactly n labels: keys `"k000"` through `"k007"` or `"k255"`, paired with values `"v000"` through `"v007"` or `"v255"`. The size denotes n labels in that single map; it is not n nested maps or an n-squared value. The Rejected schema retains one exact `reason:str` field even though the measured value is Ready. All limits apply, and complete schema/value node/depth counts and wire byte sizes are published before interval release.

Decoder input bytes are generated only by a separately frozen finite hand-grammar oracle for this fixed Invoice shape, using independent literal tags/field/case names/nominal labels/ordering and exact U32/U64/code-point rules. Its complete source and resulting exact literals are authored and inspected before candidate observation; the measured encoder never generates its decoder oracle. This oracle handles only the fixed named payload, rather than becoming a second generic codec. Correctness outside intervals establishes that public encode equals the independent literal, public decode establishes the complete exact Invoice schema/value, and all guard modes retain the same semantics.

Root first approves exact source/controller/oracle/fixture inventories. Build, installation, first import, schema/input construction, literal-oracle construction, warmup, guard invocation counting, correctness, hashing and JSON writes stay outside intervals. The selected original or generated export is resolved once beforehand; each measured call includes its actual codec schema compilation, traversal, output construction, native validation and generated assertions. The loop retains only the final result and releases each previous result as the binding advances; no accumulating output list or per-call assertion enters the interval. Final-result correctness and byte/schema/type checks occur after each interval.

Each interval starts a fresh tracemalloc session and resets the peak outside its timer after all fixture/setup work. Start `perf_counter`, perform exactly 25 calls retaining only the last result, then stop `perf_counter`; read traced current/peak allocation and stop tracing afterward, before correctness/publication. Publish elapsed values/medians and peak traced delta with that initial fixture scope explicit. Runtime output/guard allocations, result disposal and tracing overhead are inside measured work; fixture/build/import/hash/assertion allocations are outside. Python-traced allocation is not RSS or complete native memory. No comparison subtracts tracing or guard overhead from the observed interval.

Freeze the exact controller, constants, independent oracles, full source/product maps, literal `.venv/bin/python` native executable and actual Linux interpreter/install provenance before observation. Record actual hardware/OS/runtime/flags/hash seed, original/generated guard modes and untimed assertion counts, plus before/after source maps. Do not run inherited suites/Docker setup concurrently with intervals or infer universal speed/space guarantees from these named conditions. At the original plan gate, this helper had run no candidate tests/codecs/wheels/benchmarks or timings; the later focused development observations are recorded below.

Implementation costs to disclose regardless of later measurements: schema compile/validation and full repeated structural descriptor generation occur per call (no mutable memoization cache); encoding/decoding traverses bounded complete values, copies wire/output storage, and uses O(n log n) canonical sorting for encoder map/set keys. Decoder Map/Set order checking compares adjacent keys, while decoder OrderedMap duplicate checking compares against prior exact scalar keys and can perform O(n²) comparisons at its fixed 4,096-entry bound. Catalog identity/collision checks additionally depend on the number of existing product declarations. Repeated references expand by value. The finite wire/schema/value limits bound those admitted traversals but do not prove constant cost, termination, process memory sufficiency or large-project throughput. The Invoice protocol uses Map and does not measure or extrapolate OrderedMap's duplicate-check cost.

## Historical plan gate

Root explicitly approved the reconciled helper, main and reviewer plans and released this five-file implementation. At that development gate, focused tests verified implementation intent only; final independent conformance/platform/installed-package/measurement observations awaited the later joint source and controller freeze. The final observations below supersede that held status. Inherited M1–10 gates remain separate historical provenance while new module identities are added for M11.

## Focused development evidence before final freeze

At this development cut, no whole suite, independent acceptance controller, installed-consumer acceptance or benchmark interval had been run by this helper. The benchmark had been authored with the fixed hand-grammar oracle and only syntax-compiled; neither its product setup nor its measured/unmeasured worker had been executed. Its expected independent schema length was 508 bytes and wire lengths were 918/11,334 at 8/256 labels, with schema nodes/depth 8/2 and value nodes/depth 21/2 or 517/2. These were hand-derived controller expectations, not candidate observations.

Actual focused commands on literal `/Volumes/Projects/pyalamode/.venv/bin/python`, from `/Volumes/Projects/pyalamode`:

| Command | Development observation |
| --- | --- |
| `PYTHONPATH=tests .venv/bin/python -m unittest m11_encoding.EncodingRuntime m11_encoding.EncodingCatalog -v` (first run) | 22 methods: 19 passed, 3 fixture errors. Patching/deleting a global test class's `__new__` perturbed CPython `tp_new` even after attribute restoration; later ordinary constructors failed. Original full tool output remains in conversation history. |
| Same command after disposable constructor-poison class/catalog isolation | 22 passed, status 0; raw `/tmp/pyalamode-m11-encoding-development-02.txt`. Runtime oracles were retained. |
| `.venv/bin/python -m py_compile pyalamode/encoding.py pyalamode/encoding_contracts.py tests/m11_encoding.py benchmarks/m11_encoding.py` | Status 0; syntax compilation only, no benchmark execution. |
| `PYTHONPATH=tests .venv/bin/python -m unittest m11_encoding -v` after native-domain metadata, nominal boundary, field/case/schema-byte controls and primary static integration | 27 passed, status 0; raw `/tmp/pyalamode-m11-encoding-development-03.txt`. |
| Same complete focused command after custom-finalizer refusal and zero-hook regression | 28 passed, status 0; raw `/tmp/pyalamode-m11-encoding-development-04.txt`. |

Source review corrections preceding those observations: unrelated legitimate local catalog records are ignored during selected nominal collision comparison; selected local labels remain unsupported. Direct builtin GetSetDescriptor/MemberDescriptor metadata reads bypass known-domain metaclass lookups. Schema nodes count appearances in the exact wire grammar: domain Choice with int/string fields counts 3; selecting its Number case counts the case wrapper plus complete domain plus both field schemas, 4; 128 empty domain cases still count one SCHEMA node, while the independent case-count bound applies. Native no-constructor probes use separate disposable test classes and restore original catalogs, so their intentionally unsupported monkey-patching cannot contaminate subsequent ordinary construction. Custom `__del__` is refused through native class/MRO dictionaries before allocation, retaining zero foreign cleanup hooks on malformed input; this rejects unsupported altered behavior and does not add a general runtime tamper monitor. These were focused engineering results and source intent; human usefulness was unmeasured and final release gates were held at that cut.

After root's complete source/controller review, the then-unrun benchmark worker was aligned with the package-owned mirrored wheel facade `checked_pricing._pyalamode_exports.core` for exports/debug modes, as emitted by `distribution.py`. Its isolated pip installation uses `--no-compile`, preserving source-only installation for relocated bytecode provenance checks. Independent literals, guard counts, correctness checks and interval scope were retained. These source-only revisions had not been executed at intent02, `/tmp/pyalamode-m11-encoding-intent-02.json`, SHA `f1792408528dc8f9af38eebec792e54bccf22dffb9809f12825689ea4449c1ed`; the earlier five-file intent SHA `3a2b46fff0a068f93aa9bfb18c1901c31193e6b9a8d1541ac0ee58ddeb0b1558` remains historical development evidence.

## Final frozen engineering observations

Root accepted the final central integration at main intent12, then froze the complete executable source and controllers in `/tmp/pyalamode-m11-root-freeze-10.json`, SHA `d8b5346e78b30c55e33fd47e986268f3bf3207d84df6a8782cd3969466d8fb2d`. This final evidence applies to those executable bytes. Only this evidence document changed afterward under the separate docs-only release; no codec, catalog, tests, benchmark, oracle or central source was changed for documentation.

| Gate | Actual final observation and receipt |
| --- | --- |
| Native complete source suite | 461 methods, status 0, 42.508 seconds; `/tmp/pyalamode-root-m11-native-suite-10.json`, SHA `1ed2422718c5603905218f7a9eeb1f0f6fe4e678413af3b1a6b0e4ee9e43992a` |
| Linux complete source suite | 461 methods, status 0, 239.186 seconds; `/tmp/pyalamode-root-m11-linux-suite-10.json`, SHA `08cd6e24226a42ae8fe92fd59c7c77f39e83c5f01f49a2331304e066e8269ce7` |
| Fresh installed producer/consumer acceptance | 40 commands and 121 assertions on each platform, both PASS; `/tmp/pyalamode-root-m11-native-walk-10.json`, SHA `402762126856696afb82aaa8ddb46bf7b72ecf5a20a868ebc75eb3288d5b9d04`, and `/tmp/pyalamode-root-m11-linux-walk-10.json`, SHA `e43b0f7f8f34b96f2b552472fbe563e322771be3dbfc7f73377919e87d46e3cd` |
| Independent original conformance corpus | All 78 fixed cases passed on each platform across eight platform/group runs; root reconciliation `/tmp/pyalamode-m11-root-peer-reconciliation-10.json`, SHA `d394b33722b3ab6e64783be0192c04b9d0003c721646a4fc2d47ab2c3ee446ae` |
| Approved codec measurement | Exactly 12 rows, 36 intervals, 900 measured calls and 120 warmups per platform; root reconciliation `/tmp/pyalamode-m11-root-codec-measurement-reconciliation-10.json`, SHA `76f20251091022a59ec41d0f0bc92adbe6a9a3c2944dab9025d7de7a5e309237` |

The independent corpus covers the fixed encoding E01–E18 cases as part of that original 78-case corpus, including malformed/bounded data, exact types, ordering, schema changes and constructor/descriptor hook controls. Root's installed walk also exercised fixed independent wire/business results in off/exports/debug packages and genuine dependency refusal without executing source during analysis. These finite engineering observations support the published operation contract under its stated runtime, stable class/catalog/native descriptor and ordinary input obligations. They do not certify arbitrary unchecked construction, private catalog mutation, hostile runtime changes, other Python builds or arbitrary schemas.

The separately approved distribution protocol completed 12 intervals per platform and stopped before codec intervals began. Root's `/tmp/pyalamode-m11-root-distribution-measurement-reconciliation-10.json`, SHA `fc8d0fed583eb285a8f3b5c18324ebac92e9bbe5b57d8c62066283b5b7726792`, is separate evidence; no distribution timing is combined with codec call cost. All heavy correctness runs and other measurement workers were stopped for the codec sequence.

## Observed codec measurements and retained raw evidence

The unchanged 370-line controller `/Volumes/Projects/pyalamode/benchmarks/m11_encoding.py`, SHA `c13096bc4da18ad243f942f4bb06969ff72a48579e67d6dc21c9908482c76051`, ran exactly `stable_invoice_encoding_v1`, native first and Linux second, without smoke/describe runs, additional rows, retries or repetitions. Both used the actual product wheel `/tmp/pyalamode-root-m11-product-10/wheels/pyalamode-0.1.0-py3-none-any.whl`, SHA `5812975300fc6a967a717b16872235b7032a7fdbe36e821e79d47f965c3e4dc2`, freshly installed with `--no-index --no-deps --no-compile`. Parent environments and the three mode-specific worker environments on each platform were outside the checkout. Each actual product installation matched all 23 Python package files and 22 foundations; each worker had no `.pth` files, while parent `.pth` inventories were empty dictionaries `{}`. No checkout `.pth` or source import path supplied the installed product.

Recorded controller command shapes were literal parent-venv Python, `-I`, the absolute controller path, `--measure --product-wheel ... --work-directory ... --output ...`. Native used `/tmp/pyalamode-m11-encoding-measurement-10/native-parent/bin/python`; its observed `sys.executable` used `/private/tmp/` for the same host path. Linux used `/tmp/pyalamode-m11-encoding-measurement-10/linux-parent/bin/python` with controller `/workspace/benchmarks/m11_encoding.py` in image `sha256:0771ed8526e7888cfc82c2154dc39d5113eeeb183c0ee1fd9466031489eaabae`, `--platform linux/arm64 --network none`, `/private/tmp:/tmp`, and the checkout mounted read-only at `/workspace`. Every interpreter invocation retained the literal venv path; resolved paths were observations only.

| Observed environment | Native | Linux |
| --- | --- | --- |
| Runtime | Exact CPython 3.13.1, standard GIL, `cpython-313`, empty ABI flags | Exact CPython 3.13.1, standard GIL, `cpython-313`, empty ABI flags |
| OS/architecture | macOS 26.6.2, arm64 | Linux 5.15.49-linuxkit, aarch64, glibc 2.36 |
| Build/compiler | Dec 3 2024; Clang 16.0.0 | Feb 4 2025; GCC 12.2.0 |
| Exposed logical CPUs | 10 | 5 |
| Filesystem | UTF-8 / surrogateescape | UTF-8 / surrogateescape |
| Measured worker flags | Isolated, no user site, ignore environment, optimize 0, UTF-8 mode 0 | Isolated, no user site, ignore environment, optimize 0, UTF-8 mode 0 |
| Hash/load/cache controls | Hash randomization enabled; no explicit hash seed; system load and OS caches uncontrolled | Hash randomization enabled; no explicit hash seed; system load and OS caches uncontrolled |

Linux's untimed parent reported UTF-8 mode 1; each actual measured installed worker reported mode 0, with the required UTF-8/surrogateescape filesystem configuration unchanged. Runtime and executable receipts retain that distinction. Native literal/base executable receipts both hashed to `d483cfdc272ddd1bfd8f6f595b65cdc2f00b8e503f0deab65b20e8faeb986132`; Linux literal/base executable receipts both hashed to `44a9ce6ed83ab1809449925790d0583e38f17b3ccd1671d9f55e15b576cb4f20`. These bounded executable observations are separate from the earlier distribution/integration five-file native dependency evidence and do not add a codec backend claim.

Root reconstructed the fixed wire independently with stdlib-only literal grammar. The schema was exactly 508 bytes, eight nodes and depth two. Actual 8-label and 256-label values had 21 and 517 nodes, depth two, and these identical native/Linux goldens:

| Labels | Envelope bytes | Independent literal SHA-256 |
| --- | ---: | --- |
| 8 | 918 | `0ed593777525c9dc11ba36888de5b5d5ce514031c85c7d61082f8990dc07c3bb` |
| 256 | 11,334 | `32183814d95799760741c3909430e78c14b7c9295a2ed889b03ee948eddd83d3` |

Every encode matched that independent literal byte-for-byte; every decode established the exact original Invoice/Ready class and complete field/map values. Untimed validation counts per selected invocation were exactly off **0**, exports **2**, debug **4**, for both operations and both sizes on both platforms. The temporary counting function and imported aliases were restored to the native validator before warmups and intervals. Generated assertions and native codec validation remained inside each measured call.

Each table entry is the median of its three 25-call intervals divided by 25, in milliseconds per call. Peak columns are median traced Python allocation deltas in bytes; native and Linux observed the same listed deltas. All actual interval elapsed/current/peak observations remain in the raw JSON.

| Mode | Labels | Native encode ms | Native decode ms | Linux encode ms | Linux decode ms | Encode peak bytes | Decode peak bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| off | 8 | 1.290048 | 1.543582 | 1.763440 | 2.193232 | 24,230 | 18,201 |
| off | 256 | 18.326082 | 20.220050 | 25.253950 | 29.736330 | 127,619 | 66,794 |
| exports | 8 | 1.495338 | 1.712177 | 2.068270 | 2.485032 | 26,830 | 20,697 |
| exports | 256 | 22.182465 | 25.937702 | 34.197318 | 34.115113 | 127,619 | 66,794 |
| debug | 8 | 1.718372 | 2.019755 | 2.323157 | 2.653708 | 29,430 | 23,193 |
| debug | 256 | 26.419150 | 27.851515 | 35.284153 | 40.321333 | 127,619 | 66,794 |

Tracing was fresh/reset before each timer; fixture/setup work was outside the traced interval scope. Timers included codec schema compilation, traversal, guards, output construction, disposal of preceding results and tracemalloc overhead; only the final result was retained. Current/peak reads and correctness checks followed the timer. These peaks are neither RSS nor total native allocation, and these elapsed values are the named traced workloads rather than an untraced throughput estimate. The two platform environments are separately observed conditions, with no controlled system-load or cache comparison.

Evidence directory `/tmp/pyalamode-m11-encoding-measurement-10` retains **34 recorded subprocess commands and 68 raw streams**: 24 nested controller setup/worker commands across both platforms, plus 10 outside parent setup/measurement/provenance commands. Raw streams were saved before return-code/oracle checks; all commands returned zero, with no failed or partial run hidden by a retry. Three worker JSON files per platform retain the complete independent wire literals and all intervals. Parent target-before/after receipts were byte-identical. Phase-before/cross/after receipts each preserved exact 114 source inputs, 23 package files, 22 foundations, 278 frozen controller inputs, the codec controller and product wheel. All five owned files matched intent02 during observation. The document's current final hash is recorded by the later docs-only intent rather than being represented as part of that earlier freeze.

| Retained receipt | SHA-256 |
| --- | --- |
| `/tmp/pyalamode-m11-encoding-measurement-10/native.json` | `8c2cf17bf395f180a7655b639448d5f317ba2afab4f02e82049788a089c20649` |
| `/tmp/pyalamode-m11-encoding-measurement-10/linux.json` | `c9e1e4746db88ac7d996f94174613fa5cc51c95150d41ef98402385ff16cd98a` |
| `/tmp/pyalamode-m11-encoding-measurement-10/reconciliation.json` (helper receipt/count/median reconstruction) | `ee3c7f41cc67311cb25b2e42aff2de97ae2aae8f5d0ea5717e187a647d8b799e` |
| `/tmp/pyalamode-m11-root-codec-measurement-reconciliation-10.json` (root independent wire/receipt/count/median reconstruction) | `76f20251091022a59ec41d0f0bc92adbe6a9a3c2944dab9025d7de7a5e309237` |

All measurement processes stopped before this docs-only update. Per-call schema/descriptor work, copies, canonical sort and declaration-catalog scans remain the costs described above. OrderedMap decoding still has bounded O(n²) duplicate comparisons; this Map-only Invoice workload does not measure that path. The numeric/size/depth/schema bounds and trusted allocation/class/catalog preconditions remain unchanged. No result establishes unrestricted serialization, termination, large-project throughput or target-user value. Human usefulness remains **UNMEASURED: zero participants, zero attempts**.
