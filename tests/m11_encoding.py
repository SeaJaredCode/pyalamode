"""Fixed finite codec oracles and focused exact-type/no-hook regressions."""

import codecs
import json
import os
from pathlib import Path
import subprocess
import sys
from types import GenericAlias, MemberDescriptorType
import unittest
from unittest.mock import patch

from pyalamode import record, variant, case, Vector, OrderedMap, Map, Set, Option, Some, Nothing, Result, Ok, Err, Failure
from pyalamode import records, variants, collections
from pyalamode.encoding import value_encode, value_decode
from pyalamode import encoding
from pyalamode.encoding_contracts import ENCODING_NAMES, ENCODING_VERSION, operation_contract, operation_catalog


@variant
class Choice:
    @case
    class Number:
        number: int
    @case
    class Text:
        text: str


@record
class Sample:
    name: str
    amount: int
    labels: Map[str, str]
    choice: Choice


@record
class Defaulted:
    value: int = 9


def u32(value):
    return bytes(((value >> 24) & 255, (value >> 16) & 255, (value >> 8) & 255, value & 255))


def text(value):
    return u32(len(value)) + b"".join(u32(ord(character)) for character in value)


def envelope(schema, value):
    return b"PALV\x01" + u32(len(schema)) + schema + value


def integer(value):
    bits = value if value >= 0 else value + 2 ** 64
    return b"\x02" + bytes((bits >> shift) & 255 for shift in range(56, -1, -8))


def forged(kind, name, values):
    value = object.__new__(kind)
    owner = collections._MapBase if kind is Map or kind is OrderedMap else kind
    descriptor = type.__getattribute__(owner, "__dict__")[name]
    MemberDescriptorType.__set__(descriptor, value, values)
    return value


class EncodingRuntime(unittest.TestCase):
    def roundtrip(self, value, schema):
        packet = value_encode(value, schema)
        result = value_decode(packet, schema)
        self.assertIs(type(result), type(value))
        self.assertEqual(result, value)
        self.assertEqual(value_encode(result, schema), packet)
        return result

    def test_independent_scalar_golden_bytes_and_exact_integer_endpoints(self):
        goldens = ((None, None, "50414c5601000000010000"),
                   (False, bool, "50414c560100000001010100"),
                   (True, bool, "50414c560100000001010101"),
                   (0, int, "50414c56010000000102020000000000000000"),
                   (-1, int, "50414c5601000000010202ffffffffffffffff"))
        for value, schema, hexadecimal in goldens:
            literal = bytes.fromhex(hexadecimal)
            self.assertEqual(value_encode(value, schema), literal)
            self.assertIs(type(value_decode(literal, schema)), type(value))
            self.assertEqual(value_decode(literal, schema), value)
        for number in (-(2 ** 63), 2 ** 63 - 1):
            literal = envelope(b"\x02", integer(number))
            self.assertEqual(value_encode(number, int), literal)
            self.assertEqual(value_decode(literal, int), number)
        for number in (-(2 ** 63) - 1, 2 ** 63, 10 ** 5000):
            with self.assertRaisesRegex(ValueError, "signed64"):
                value_encode(number, int)
        with self.assertRaises(TypeError):
            value_encode(True, int)
        with self.assertRaises(TypeError):
            value_encode(0, bool)

    def test_codepoint_strings_and_raw_bytes_independent_literals(self):
        value = "\x00\ufeff\U0001f600\ud800\udc80\udfff"
        literal = envelope(b"\x03", b"\x03" + text(value))
        self.assertEqual(value_encode(value, str), literal)
        self.assertEqual(value_decode(literal, str), value)
        data = b"\x00\x7f\x80\xff"
        literal = envelope(b"\x04", b"\x04" + u32(4) + data)
        self.assertEqual(value_encode(data, bytes), literal)
        self.assertEqual(value_decode(literal, bytes), data)

    def test_ordered_container_tags_and_empty_exact_schemas(self):
        rows = (((), tuple[()], b"\x10" + u32(0)),
                ((3, "x"), tuple[int, str], b"\x10" + u32(2) + b"\x02\x03"),
                ((3, 4), tuple[int, ...], b"\x11\x02"),
                (Vector.of(3), Vector[int], b"\x12\x02"),
                (OrderedMap.of(("b", 1), ("a", 2)), OrderedMap[str, int], b"\x13\x03\x02"),
                (Map[str, int].of(), Map[str, int], b"\x14\x03\x02"),
                (Set[str].of(), Set[str], b"\x15\x03"))
        for value, schema, descriptor in rows:
            packet = value_encode(value, schema)
            self.assertEqual(packet[9:9 + len(descriptor)], descriptor)
            self.roundtrip(value, schema)
        left = OrderedMap.of(("a", 1), ("b", 2))
        right = OrderedMap.of(("b", 2), ("a", 1))
        self.assertNotEqual(value_encode(left, OrderedMap[str, int]), value_encode(right, OrderedMap[str, int]))
        self.assertNotEqual(value_encode(Vector.of(1, 2), Vector[int]), value_encode(Vector.of(2, 1), Vector[int]))

    def test_every_alternative_schema_and_value_tag(self):
        rows = ((Some(7), Option[int], b"\x23\x02", b"\x31" + integer(7)),
                (Nothing(), Option[int], b"\x23\x02", b"\x32"),
                (Ok(7), Result[int, str], b"\x24\x02\x03", b"\x33" + integer(7)),
                (Err("bad"), Result[int, str], b"\x24\x02\x03", b"\x34\x03" + text("bad")),
                (Some(7), Some[int], b"\x25\x02", b"\x31" + integer(7)),
                (Nothing(), Nothing, b"\x26", b"\x32"),
                (Ok(7), Ok[int], b"\x27\x02", b"\x33" + integer(7)),
                (Err("bad"), Err[str], b"\x28\x03", b"\x34\x03" + text("bad")))
        for value, schema, descriptor, body in rows:
            literal = envelope(descriptor, body)
            self.assertEqual(value_encode(value, schema), literal)
            self.assertEqual(value_decode(literal, schema), value)
        with self.assertRaises(TypeError):
            value_encode(Some(True), Option[int])
        with self.assertRaisesRegex(ValueError, "wire schema differs"):
            value_decode(envelope(b"\x23\x03", b"\x32"), Option[int])

    def test_record_domain_and_exact_case_schema_literals(self):
        identity = __name__ + ":Choice"
        domain = (b"\x21" + text(identity) + u32(2)
                  + text("Number") + u32(1) + text("number") + b"\x02"
                  + text("Text") + u32(1) + text("text") + b"\x03")
        number = b"\x21" + u32(0) + u32(1) + integer(7)
        self.assertEqual(value_encode(Choice.Number(7), Choice), envelope(domain, number))
        exact_case = b"\x22" + domain + text("Number")
        self.assertEqual(value_encode(Choice.Number(7), Choice.Number), envelope(exact_case, number))
        self.assertEqual(value_decode(envelope(domain, number), Choice), Choice.Number(7))
        with self.assertRaisesRegex(ValueError, "case index differs"):
            value_decode(envelope(exact_case, b"\x21" + u32(1) + u32(1) + b"\x03" + text("x")), Choice.Number)
        descriptor = b"\x20" + text(__name__ + ":Defaulted") + u32(1) + text("value") + b"\x02"
        self.assertEqual(value_encode(Defaulted(), Defaulted), envelope(descriptor, b"\x20" + u32(1) + integer(9)))
        self.roundtrip(Failure("ValueError", "invalid value"), Failure)
        sample = Sample("order", 1299, Map.of(("b", "B"), ("a", "A")), Choice.Text("ready"))
        result = self.roundtrip(sample, Sample)
        self.assertIs(type(result.labels), Map)
        self.assertIs(type(result.choice), Choice.Text)
        self.assertIsNot(result, sample)
        self.assertIsNot(result.labels, sample.labels)

    def test_schema_node_depth_count_is_wire_appearance_count(self):
        compiler = encoding._Compiler()
        compiler.annotation(Choice)
        self.assertEqual(compiler.budget.count, 3)  # domain + int + str
        compiler = encoding._Compiler()
        compiler.annotation(Choice.Number)
        self.assertEqual(compiler.budget.count, 4)  # exact-case + complete domain + int + str
        schema, value = int, 1
        for _ in range(32):
            schema, value = tuple[schema], (value,)
        self.roundtrip(value, schema)
        with self.assertRaisesRegex(ValueError, "depth"):
            value_encode((value,), tuple[schema])
        compiler = encoding._Compiler()
        compiler.annotation(tuple[tuple[int, str], tuple[int, str]])
        self.assertEqual(compiler.budget.count, 7)
        self.roundtrip(tuple(range(1023)), tuple[(int,) * 1023])
        with self.assertRaisesRegex(ValueError, "schema node"):
            value_encode(tuple(range(1024)), tuple[(int,) * 1024])

    def test_atom_container_value_node_and_envelope_bounds(self):
        self.roundtrip("x" * 65536, str)
        self.roundtrip(b"x" * 262144, bytes)
        self.roundtrip(Vector.of(*(0 for _ in range(4096))), Vector[int])
        for value, schema in (("x" * 65537, str), (b"x" * 262145, bytes), (tuple(range(4097)), tuple[int, ...])):
            with self.assertRaisesRegex(ValueError, "limit exceeded"):
                value_encode(value, schema)
        values = tuple((0, 0, 0) for _ in range(4095))
        self.roundtrip(values, tuple[tuple[int, int, int], ...])  # 1 + 4095 * 4 == 16381
        with self.assertRaisesRegex(ValueError, "value node"):
            value_encode(values + ((0, 0, 0),), tuple[tuple[int, int, int], ...])
        with self.assertRaisesRegex(ValueError, "envelope"):
            value_encode((b"x" * 262144,) * 4, tuple[bytes, ...])
        with self.assertRaisesRegex(ValueError, "envelope"):
            value_decode(b"x" * 1048577, int)

    def test_maps_sets_canonical_order_and_bool_int_domains(self):
        domains = ((None, (None,)), (bool, (True, False)), (int, (2, -1, 0)),
                   (str, ("\udfff", "\ud800", "a", "\x00")), (bytes, (b"\xff", b"a", b"\x00")))
        for schema, members in domains:
            left, right = Set.of(*members), Set.of(*reversed(members))
            self.assertEqual(value_encode(left, Set[schema]), value_encode(right, Set[schema]))
            self.roundtrip(left, Set[schema])
            left = Map.of(*((member, index) for index, member in enumerate(members)))
            right = Map.of(*reversed(tuple((member, index) for index, member in enumerate(members))))
            self.assertEqual(value_encode(left, Map[schema, int]), value_encode(right, Map[schema, int]))
            self.roundtrip(left, Map[schema, int])
        with self.assertRaises(TypeError):
            value_encode(Map.of((True, "x")), Map[int, str])
        with self.assertRaises(TypeError):
            value_encode(Set.of(1), Set[bool])

    def test_unordered_forged_storage_selects_canonical_first_failure(self):
        for entries in ((("z", True), ("a", "bad")), (("a", "bad"), ("z", True))):
            with self.assertRaisesRegex(TypeError, r"value.entries\[0\].value: expected exact"):
                value_encode(forged(Map, "_entries", entries), Map[str, int])
        for entries in (((True, 1), (0, 2)), ((0, 2), (True, 1))):
            with self.assertRaisesRegex(TypeError, "value.keys:"):
                value_encode(forged(Map, "_entries", entries), Map[int, int])
        with self.assertRaisesRegex(TypeError, "duplicate collection"):
            value_encode(forged(Map, "_entries", (("a", 1), ("a", 2))), Map[str, int])
        with self.assertRaisesRegex(TypeError, "duplicate collection"):
            value_encode(forged(Set, "_items", (1, 1)), Set[int])
        with self.assertRaisesRegex(TypeError, "storage"):
            value_encode(forged(Map, "_entries", (1, ("a", 1))), Map[str, int])

    def test_noncanonical_duplicate_map_set_and_ordered_map_wire(self):
        for keys in ((2, 1), (1, 1)):
            body = b"\x14" + u32(2) + b"".join(integer(key) + integer(0) for key in keys)
            with self.assertRaisesRegex(ValueError, "duplicate/noncanonical map"):
                value_decode(envelope(b"\x14\x02\x02", body), Map[int, int])
            body = b"\x15" + u32(2) + b"".join(integer(key) for key in keys)
            with self.assertRaisesRegex(ValueError, "duplicate/noncanonical set"):
                value_decode(envelope(b"\x15\x02", body), Set[int])
        body = b"\x13" + u32(2) + integer(2) + integer(0) + integer(1) + integer(0)
        result = value_decode(envelope(b"\x13\x02\x02", body), OrderedMap[int, int])
        self.assertEqual(result.entries(), Vector.of((2, 0), (1, 0)))
        with self.assertRaisesRegex(ValueError, "duplicate/noncanonical map"):
            value_decode(envelope(b"\x13\x02\x02", b"\x13" + u32(2) + (integer(1) + integer(0)) * 2), OrderedMap[int, int])

    def test_truncation_every_boundary_unknown_tags_bool_points_and_trailing(self):
        literal = envelope(b"\x10" + u32(2) + b"\x02\x03", b"\x10" + u32(2) + integer(3) + b"\x03" + text("x"))
        for end in range(len(literal)):
            with self.assertRaises(ValueError):
                value_decode(literal[:end], tuple[int, str])
        malformed = ((b"PALV\x02" + literal[5:], tuple[int, str]),
                     (envelope(b"\xff", b"\x00"), None),
                     (envelope(b"\x01", b"\x01\x02"), bool),
                     (envelope(b"\x03", b"\x03" + u32(1) + u32(0x110000)), str),
                     (envelope(b"\x02\x00", integer(1)), int),
                     (envelope(b"\x02", integer(1) + b"\x00"), int),
                     (envelope(b"\x02", b"\x00"), int))
        for packet, schema in malformed:
            with self.assertRaises(ValueError):
                value_decode(packet, schema)

    def test_unknown_duplicate_invalid_schema_names_and_closed_cases(self):
        duplicate = b"\x20" + text("somewhere:Record") + u32(2) + (text("value") + b"\x02") * 2
        with self.assertRaisesRegex(ValueError, "duplicate schema field"):
            value_decode(envelope(duplicate, b"\x00"), Defaulted)
        duplicate = b"\x21" + text("somewhere:Domain") + u32(2) + (text("One") + u32(0)) * 2
        with self.assertRaisesRegex(ValueError, "duplicate schema case"):
            value_decode(envelope(duplicate, b"\x00"), Choice)
        for descriptor in (b"\x20" + text("unknown:Record") + u32(0),
                           b"\x20" + text("bad:<locals>.Record") + u32(0),
                           b"\x15\x12\x02", b"\x21" + text("m:Domain") + u32(0)):
            with self.assertRaises(ValueError):
                value_decode(envelope(descriptor, b"\x00"), Defaulted)
        descriptor = (b"\x21" + text(__name__ + ":Choice") + u32(2)
                      + text("Number") + u32(1) + text("number") + b"\x02"
                      + text("Text") + u32(1) + text("text") + b"\x03")
        with self.assertRaisesRegex(ValueError, "case index outside"):
            value_decode(envelope(descriptor, b"\x21" + u32(2) + u32(0)), Choice)

    def test_unknown_schema_alias_origins_and_exact_subclasses_have_zero_hooks(self):
        hits = []
        class ForeignMeta(type):
            def __getattribute__(self, name):
                hits.append(name)
                return super().__getattribute__(name)
            def __hash__(self):
                hits.append("hash")
                return 1
            def __eq__(self, other):
                hits.append("eq")
                return True
        class Foreign(metaclass=ForeignMeta):
            pass
        class Hook:
            def __getattribute__(self, name):
                hits.append(name)
                raise AssertionError("foreign read")
            def __repr__(self):
                hits.append("repr")
                raise AssertionError("foreign repr")
        schemas = (Foreign, Hook(), GenericAlias(Foreign, int), int | str, "int", tuple["int"], Vector["int"])
        hits.clear()
        for schema in schemas:
            with self.assertRaises(TypeError):
                value_encode(1, schema)
        self.assertEqual(hits, [])
        for kind, value in ((int, 1), (str, "x"), (bytes, b"x"), (tuple, (1,))):
            subtype = type("Subclass", (kind,), {})
            schema = tuple[int] if kind is tuple else kind
            with self.assertRaises(TypeError):
                value_encode(subtype(value), schema)
        with self.assertRaises(TypeError):
            value_decode(bytearray(envelope(b"\x02", integer(1))), int)

    def test_no_user_constructors_setters_restoration_or_instance_getters_on_decode(self):
        hits = []
        def hook(*args, **kwargs):
            hits.append("hook")
            raise AssertionError("user dispatch")
        # Changing/deleting __new__ can alter CPython tp_new even after the
        # attribute is restored. Discard these distinct test classes/catalog
        # rows; do not poison later ordinary constructors in the suite.
        before = records._RECORDS, variants._CASES, variants._VARIANTS
        try:
            kind = record(type("PoisonRecord", (object,), {
                "__module__": "m11_hook_fixture", "__annotations__": {"value": int}}))
            packet = value_encode(kind(7), kind)
            with patch.object(kind, "__new__", hook, create=True), patch.object(kind, "__init__", hook), \
                    patch.object(kind, "__setattr__", hook), patch.object(kind, "__getattribute__", hook), \
                    patch.object(kind, "__setstate__", hook, create=True), patch.object(kind, "__reduce__", hook):
                result = value_decode(packet, kind)
                descriptor = type.__getattribute__(kind, "__dict__")["value"]
                self.assertEqual(MemberDescriptorType.__get__(descriptor, result, kind), 7)
            number = case(type("Number", (object,), {"__module__": "m11_hook_fixture",
                                                     "__qualname__": "PoisonDomain.Number", "__annotations__": {"value": int}}))
            domain = variant(type("PoisonDomain", (object,), {"__module__": "m11_hook_fixture", "Number": number}))
            packet = value_encode(number(7), domain)
            with patch.object(number, "__init__", hook), patch.object(number, "__new__", hook, create=True):
                result = value_decode(packet, domain)
            self.assertIs(type(result), number)
            self.assertEqual(hits, [])
        finally:
            records._RECORDS, variants._CASES, variants._VARIANTS = before

    def test_foreign_replaced_storage_and_metadata_descriptors_refuse_before_hooks(self):
        packet = value_encode(Defaulted(7), Defaulted)
        hits = []
        def hook(*args):
            hits.append("getter")
            raise AssertionError("descriptor ran")
        with patch.object(Defaulted, "value", property(hook)):
            with self.assertRaisesRegex(TypeError, "non-native"):
                value_decode(packet, Defaulted)
        with patch.object(Defaulted, "__module__", property(hook)):
            with self.assertRaisesRegex(TypeError, "metadata"):
                value_decode(packet, Defaulted)
        with patch.object(Vector, "_items", property(hook)):
            with self.assertRaisesRegex(TypeError, "non-native"):
                value_decode(envelope(b"\x12\x02", b"\x12" + u32(0)), Vector[int])
        self.assertEqual(hits, [])

    def test_known_domain_metaclass_lookup_is_bypassed_by_native_metadata_reads(self):
        value = Choice.Number(7)
        packet = value_encode(value, Choice)
        hits = []
        def hook(*args):
            hits.append("metaclass")
            raise AssertionError("metaclass lookup ran")
        with patch.object(variants._DomainType, "__getattribute__", hook):
            self.assertEqual(value_encode(value, Choice), packet)
            result = value_decode(packet, Choice)
        self.assertIs(type(result), type(value))
        self.assertEqual(hits, [])

    def test_foreign_finalizers_refuse_before_partial_decode_allocation(self):
        packet = value_encode(Defaulted(7), Defaulted)
        hits = []
        def hook(*args):
            hits.append("finalizer")
        with patch.object(Defaulted, "__del__", hook, create=True):
            with self.assertRaisesRegex(TypeError, "finalizers"):
                value_decode(packet[:-1], Defaulted)
        with patch.object(collections._Frozen, "__del__", hook, create=True):
            with self.assertRaisesRegex(TypeError, "finalizers"):
                value_decode(envelope(b"\x12\x02", b"\x12" + u32(0)), Vector[int])
        self.assertEqual(hits, [])

    def test_uninitialized_missing_cycle_mutable_callable_capability_storage(self):
        with self.assertRaisesRegex(TypeError, "uninitialized"):
            value_encode(object.__new__(Defaulted), Defaulted)
        malformed = object.__new__(Defaulted)
        object.__setattr__(malformed, "_pal_initialized", True)
        with self.assertRaisesRegex(TypeError, "storage"):
            value_encode(malformed, Defaulted)
        cycle = forged(Vector, "_items", ())
        MemberDescriptorType.__set__(type.__getattribute__(Vector, "__dict__")["_items"], cycle, (cycle,))
        with self.assertRaisesRegex(TypeError, "cyclic"):
            value_encode(cycle, Vector[Vector[int]])
        for member in ([], {}, lambda: None, object()):
            with self.assertRaises(TypeError):
                value_encode(forged(Vector, "_items", (member,)), Vector[int])

    def test_unrelated_legitimate_local_record_does_not_poison_selected_schema(self):
        @record
        class Local:
            number: int
        with self.assertRaisesRegex(TypeError, "spelling"):
            value_encode(Local(1), Local)
        self.roundtrip(Defaulted(7), Defaulted)

    def test_duplicate_admitted_nominal_identity_refuses_selected_schema(self):
        before = records._RECORDS
        try:
            duplicate = record(type("Defaulted", (object,), {
                "__module__": __name__, "__qualname__": "Defaulted", "__annotations__": {"value": int}}))
            with self.assertRaisesRegex(TypeError, "duplicate nominal"):
                value_encode(Defaulted(7), Defaulted)
            with self.assertRaisesRegex(TypeError, "duplicate nominal"):
                value_encode(duplicate(7), duplicate)
        finally:
            records._RECORDS = before

    def test_nominal_and_field_name_bounds_before_metadata_expansion(self):
        # Normal generated exact records; explicit oversized schema metadata is
        # ValueError, while unsupported spelling/descriptor shape is TypeError.
        with patch.object(Defaulted, "__module__", "m" * 1024):
            with self.assertRaisesRegex(ValueError, "nominal-name"):
                value_encode(Defaulted(7), Defaulted)
        with patch.object(Defaulted, "__module__", "m" * (1023 - len("Defaulted"))):
            self.roundtrip(Defaulted(7), Defaulted)
        before = records._RECORDS
        try:
            long_name = "f" * 129
            kind = record(type("LongField", (object,), {"__module__": __name__, "__annotations__": {long_name: int}}))
            with self.assertRaisesRegex(ValueError, "field-name/case-name"):
                value_encode(kind(7), kind)
        finally:
            records._RECORDS = before
        with self.assertRaisesRegex(ValueError, "schema name"):
            value_decode(envelope(b"\x20" + u32(1025), b"\x00"), Defaulted)

    def test_record_field_closed_case_count_and_schema_bytes_bounds(self):
        before = records._RECORDS, variants._CASES, variants._VARIANTS
        try:
            def generated_record(count, width=4):
                names = tuple("f" + str(index).rjust(3, "0") + "x" * (width - 4) for index in range(count))
                kind = record(type("Fields" + str(count) + "Width" + str(width), (object,), {
                    "__module__": "m11_count_fixture", "__annotations__": dict((name, int) for name in names)}))
                return kind, kind(*(0 for _ in names))
            kind, value = generated_record(128)
            self.roundtrip(value, kind)
            kind, value = generated_record(129)
            with self.assertRaisesRegex(ValueError, "schema field count"):
                value_encode(value, kind)
            kind, value = generated_record(128, 128)
            with self.assertRaisesRegex(ValueError, "schema bytes"):
                value_encode(value, kind)
            for count in (128, 129):
                domain_name = "Cases" + str(count)
                attributes = {"__module__": "m11_count_fixture"}
                for index in range(count):
                    name = "C" + str(index)
                    attributes[name] = case(type(name, (object,), {"__module__": "m11_count_fixture",
                                                                "__qualname__": domain_name + "." + name}))
                domain = variant(type(domain_name, (object,), attributes))
                value = attributes["C0"]()
                if count == 128:
                    self.roundtrip(value, domain)
                    compiler = encoding._Compiler()
                    compiler.annotation(domain)
                    self.assertEqual(compiler.budget.count, 1)
                else:
                    with self.assertRaisesRegex(ValueError, "schema case count"):
                        value_encode(value, domain)
        finally:
            records._RECORDS, variants._CASES, variants._VARIANTS = before

    def test_codec_registry_is_never_consulted(self):
        hits = []
        def hook(error):
            hits.append("codec")
            raise AssertionError("codec handler ran")
        previous = codecs.lookup_error("strict")
        codecs.register_error("strict", hook)
        try:
            self.roundtrip("\ud800\udc80", str)
        finally:
            codecs.register_error("strict", previous)
        self.assertEqual(hits, [])

    def test_process_hash_seeds_have_identical_valid_bytes_and_first_failure(self):
        script = '''import json
from pyalamode import Map,Set
from pyalamode.encoding import value_encode
from pyalamode import collections
values=set(("z","a","m"))
mapping=Map.of(*((key,key) for key in values))
print(json.dumps([value_encode(mapping,Map[str,str]).hex(),value_encode(Set.of(*values),Set[str]).hex()]))
'''
        outputs = []
        for seed in ("1", "2", "8675309"):
            environment = dict(os.environ, PYTHONHASHSEED=seed)
            result = subprocess.run([sys.executable, "-c", script], env=environment, cwd=Path(__file__).resolve().parents[1],
                                    capture_output=True, text=True, check=True)
            outputs.append(json.loads(result.stdout))
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[1], outputs[2])


class EncodingCatalog(unittest.TestCase):
    def test_exact_two_operations_detached_metadata_and_failure_effect_axes(self):
        self.assertEqual(ENCODING_VERSION, "pyalamode.encoding-v1")
        self.assertEqual(ENCODING_NAMES, {"value_encode", "value_decode"})
        catalog = operation_catalog()
        self.assertEqual({row["identity"] for row in catalog}, {"pyalamode.encoding.value_encode", "pyalamode.encoding.value_decode"})
        for row in catalog:
            self.assertEqual(row["effects"], [])
            self.assertEqual(row["failures"], ["ValueError", "RecursionError"])
            self.assertEqual(row["ordinary_invalid_inputs"], ["TypeError"])
            json.dumps(row)
        catalog[0]["bounds"]["wire_bytes"] = 0
        catalog[0]["foundations"].clear()
        self.assertEqual(operation_catalog()[0]["bounds"]["wire_bytes"], 1048576)
        self.assertTrue(operation_catalog()[0]["foundations"])
        self.assertIsNone(operation_contract("unknown"))
        self.assertEqual(operation_contract("encoding.value_decode"), operation_contract("value_decode"))


class EncodingStatic(unittest.TestCase):
    def analyze(self, source):
        from pyalamode.checker import analyze_source
        return analyze_source(source, "codec.py")

    def test_pure_body_exact_schema_result_and_handled_failure(self):
        source = '''from pyalamode import fun,record,Map,value_encode,value_decode,Result,Ok,Err,Failure,failure_value
@record
class Invoice:
    amount:int
    labels:Map[str,str]
@fun
def send(value:Invoice)->bytes:return value_encode(value,Invoice)
@fun
def receive(data:bytes)->Invoice:return value_decode(data,Invoice)
@fun
def handled(data:bytes)->Result[Invoice,Failure]:
    try:
        return Ok(value_decode(data,Invoice))
    except ValueError as caught:
        return Err(failure_value(caught))
'''
        result = self.analyze(source)
        self.assertTrue(result.verified, [item.format() for item in result.diagnostics])
        contracts = {item.name: item for item in result.contracts}
        self.assertIn("encoding.value_encode", contracts["send"].operations)
        self.assertIn("encoding.value_decode", contracts["receive"].operations)
        self.assertIn("ValueError", contracts["receive"].failures)
        self.assertNotIn("ValueError", contracts["handled"].failures)
        self.assertIn("RecursionError", contracts["handled"].failures)

    def test_static_bad_types_schemas_keywords_defaults_and_initialization_refuse(self):
        prefix = "from pyalamode import fun,Vector,value_encode,value_decode\n"
        for expression in ('value_encode(True,int)', 'value_encode(1,"int")', 'value_encode(1,int|str)',
                           'value_decode(1,int)', 'value_encode(1,schema=int)', 'value_decode(b"",Vector)',
                           'value_encode(1,int,2)', 'value_decode(b"",int,2)'):
            result = self.analyze(prefix + "@fun\ndef bad()->int:return " + expression + "\n")
            self.assertFalse(result.verified, expression)
        for source in (prefix + '@fun\ndef bad(x:bytes=value_encode(1,int))->bytes:return x\n',
                       '# mode: fun\n' + prefix + 'PACKET=value_encode(1,int)\n'):
            self.assertFalse(self.analyze(source).verified)

    def test_schema_and_codec_foundation_writer_refusal(self):
        prefix = "from pyalamode import fun,record,value_encode\n@record\nclass R:\n    number:int\n"
        for writer in ('R.__module__="elsewhere"', 'R.number=property(print)',
                       'import pyalamode.encoding as e\ne._encode=print',
                       'import types\ntypes.GetSetDescriptorType=print'):
            result = self.analyze(prefix + writer + '\n@fun\ndef f(r:R)->bytes:return value_encode(r,R)\n')
            self.assertFalse(result.verified, writer)


if __name__ == "__main__":
    unittest.main()
