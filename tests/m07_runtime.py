"""Ordinary M7 runtime semantics, hooks, retention and rooted IO regressions."""

import builtins
import codecs
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import FunctionType
import unittest
from unittest.mock import patch

from pyalamode import (Vector, OrderedMap, Map, Set, Ok, Err, Some, record,
                       recorded_clock, live_io, borrow)
from pyalamode.effects import live_environment, recorded_environment, recorded_io
from pyalamode import standard as library


HOOKS = []


class Foreign:
    def __getattribute__(self, name):
        HOOKS.append("getattribute")
        return object.__getattribute__(self, name)

    def __iter__(self):
        HOOKS.append("iter")
        return iter(())

    def __str__(self):
        HOOKS.append("str")
        return "foreign"

    def __repr__(self):
        HOOKS.append("repr")
        return "foreign"

    def __eq__(self, other):
        HOOKS.append("eq")
        return False

    def __hash__(self):
        HOOKS.append("hash")
        return 0

    def __index__(self):
        HOOKS.append("index")
        return 0

    def __call__(self, *args):
        HOOKS.append("call")
        return 0


class TextSubclass(str):
    def split(self, *args):
        HOOKS.append("split")
        return []

    def encode(self, *args):
        HOOKS.append("encode")
        return b""


class IntegerSubclass(int):
    def __mod__(self, other):
        HOOKS.append("mod")
        return 0


class BytesSubclass(bytes):
    def decode(self, *args):
        HOOKS.append("decode")
        return ""


@record
class Item:
    category: str
    labels: Vector[str]


class StandardRuntimeTests(unittest.TestCase):
    def setUp(self):
        HOOKS.clear()

    def tearDown(self):
        self.assertEqual(HOOKS, [])

    def test_text_operations_empty_unicode_and_native_boundaries(self):
        self.assertEqual(library.text_split("a,,b,", ","), Vector.of("a", "", "b", ""))
        self.assertEqual(library.text_split("", "::"), Vector.of(""))
        self.assertEqual(library.text_join(Vector.of("a", "é", ""), "::"), "a::é::")
        self.assertEqual(library.text_join(Vector(), "nonempty"), "")
        self.assertEqual(library.text_replace("banana", "ana", "X"), "bXna")
        self.assertEqual(library.text_replace("é𐀀", "", "|"), "|é|𐀀|")
        self.assertTrue(library.text_startswith("é", ""))
        self.assertFalse(library.text_startswith("a", "aa"))
        self.assertEqual(library.text_slice("aé𐀀z", -3, 100), "é𐀀z")
        self.assertEqual(library.text_slice("abc", 10**100, -10**100), "")
        with self.assertRaises(ValueError):
            library.text_split("a", "")

    def test_scalar_foreign_and_subclass_inputs_never_dispatch_hooks(self):
        foreign = Foreign()
        cases = (
            (library.text_split, (foreign, ",")),
            (library.text_split, (TextSubclass("a"), ",")),
            (library.text_join, (foreign, ",")),
            (library.text_join, (Vector.of(1), ",")),
            (library.text_replace, ("a", foreign, "b")),
            (library.text_startswith, ("a", foreign)),
            (library.text_slice, ("a", foreign, 1)),
            (library.text_slice, ("a", True, 1)),
            (library.integer_clamp, (True, 0, 1)),
            (library.integer_clamp, (IntegerSubclass(2), 0, 1)),
            (library.integer_parse_decimal, (TextSubclass("1"),)),
            (library.integer_format_decimal, (foreign,)),
            (library.utf8_encode, (TextSubclass("a"),)),
            (library.utf8_decode, (BytesSubclass(b"a"),)),
            (library.hex_encode, (foreign,)),
            (library.hex_decode, (TextSubclass("aa"),)),
        )
        for operation, arguments in cases:
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(TypeError):
                    operation(*arguments)
                self.assertEqual(HOOKS, [])

    def test_every_entry_point_is_positional_only(self):
        for name in library.__all__:
            function = getattr(library, name)
            parameter = function.__code__.co_varnames[0]
            with self.subTest(name=name), self.assertRaises(TypeError):
                function(**{parameter: None})

    def test_clamp_inclusive_extreme_values_and_reversed_bounds(self):
        huge = 10**6000
        self.assertEqual(library.integer_clamp(-huge, -10, 10), -10)
        self.assertEqual(library.integer_clamp(huge, -10, 10), 10)
        self.assertEqual(library.integer_clamp(7, 7, 7), 7)
        with self.assertRaises(ValueError):
            library.integer_clamp(0, 2, 1)

    def test_decimal_ascii_grammar_and_canonical_format(self):
        for text, value in (("0", 0), ("+000", 0), ("-0", 0), ("00012", 12), ("-123", -123)):
            with self.subTest(text=text):
                self.assertEqual(library.integer_parse_decimal(text), value)
                self.assertEqual(library.integer_format_decimal(value), str(value))
        for invalid in ("", "+", "-", " 1", "1 ", "1_0", "١", "１２", "1\n", "--1", "0x10", "1.0"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                library.integer_parse_decimal(invalid)

    def test_decimal_digit_limit_independent_of_mutable_native_limit(self):
        previous = sys.get_int_max_str_digits()
        try:
            for native_limit in (640, 0, 4300):
                sys.set_int_max_str_digits(native_limit)
                text = "9" * 4096
                number = library.integer_parse_decimal(text)
                self.assertEqual(library.integer_format_decimal(number), text)
                self.assertEqual(library.integer_format_decimal(-number), "-" + text)
                self.assertEqual(library.integer_parse_decimal("0" * 4096), 0)
                with self.assertRaises(ValueError):
                    library.integer_parse_decimal("0" * 4097)
                with self.assertRaises(ValueError):
                    library.integer_format_decimal(10**4096)
        finally:
            sys.set_int_max_str_digits(previous)

    def test_utf8_all_width_boundaries_match_native_and_retain_bom(self):
        points = (0, 0x7F, 0x80, 0x7FF, 0x800, 0xD7FF, 0xE000, 0xFFFF,
                  0x10000, 0x10FFFF, 0xFEFF, 0x1F642)
        text = "".join(chr(point) for point in points)
        encoded = text.encode("utf-8")
        self.assertEqual(library.utf8_encode(text), encoded)
        self.assertEqual(library.utf8_decode(encoded), text)
        self.assertEqual(library.utf8_encode(""), b"")
        self.assertEqual(library.utf8_decode(b""), "")
        self.assertEqual(library.utf8_decode(b"\xef\xbb\xbf"), "\ufeff")

    def test_utf8_two_byte_universe_matches_native_first_error(self):
        for left, right in itertools.product(range(256), repeat=2):
            data = bytes((left, right))
            try:
                expected = data.decode("utf-8")
            except UnicodeDecodeError as expected_error:
                with self.assertRaises(UnicodeDecodeError) as caught:
                    library.utf8_decode(data)
                actual = caught.exception
                self.assertEqual((actual.start, actual.end, actual.reason),
                                 (expected_error.start, expected_error.end, expected_error.reason))
            else:
                self.assertEqual(library.utf8_decode(data), expected)

    def test_utf8_malformed_long_sequences_match_native_positions(self):
        inputs = (b"\xe0\x80\x80", b"\xed\xa0\x80", b"\xf0\x80\x80\x80",
                  b"\xf4\x90\x80\x80", b"\xf5\x80\x80\x80", b"\xe1\x80",
                  b"\xf0\x90\x80", b"x\xe1\x80y", b"\xf1\x80\x80x")
        for data in inputs:
            with self.subTest(data=data):
                with self.assertRaises(UnicodeDecodeError) as expected:
                    data.decode("utf-8")
                with self.assertRaises(UnicodeDecodeError) as actual:
                    library.utf8_decode(data)
                self.assertEqual((actual.exception.start, actual.exception.end, actual.exception.reason),
                                 (expected.exception.start, expected.exception.end, expected.exception.reason))
        for text in ("\ud800", "a\ud800\udfffz", "\udfff\ud800", "é\ud800𐀀"):
            with self.subTest(text=ascii(text)):
                with self.assertRaises(UnicodeEncodeError) as expected:
                    text.encode("utf-8")
                with self.assertRaises(UnicodeEncodeError) as actual:
                    library.utf8_encode(text)
                self.assertEqual((actual.exception.start, actual.exception.end, actual.exception.reason),
                                 (expected.exception.start, expected.exception.end, expected.exception.reason))

    def test_utf8_never_dispatches_replaced_strict_error_handler(self):
        previous = codecs.lookup_error("strict")
        calls = []
        def replacement(error):
            calls.append(type(error).__name__)
            return ("replacement", error.end)
        codecs.register_error("strict", replacement)
        try:
            self.assertEqual(library.utf8_encode("é𐀀"), b"\xc3\xa9\xf0\x90\x80\x80")
            self.assertEqual(library.utf8_decode(b"\xc3\xa9"), "é")
            with self.assertRaises(UnicodeEncodeError):
                library.utf8_encode("\ud800")
            with self.assertRaises(UnicodeDecodeError):
                library.utf8_decode(b"\xff")
            self.assertEqual(calls, [])
        finally:
            codecs.register_error("strict", previous)

    def test_hex_all_bytes_case_empty_and_invalid_grammar(self):
        data = bytes(range(256))
        expected = data.hex()
        self.assertEqual(library.hex_encode(data), expected)
        self.assertEqual(library.hex_decode(expected.upper()), data)
        self.assertEqual(library.hex_decode(""), b"")
        for invalid in ("a", "aa bb", "aa\n", "ＡＡ", "0g", "é0", "-1"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                library.hex_decode(invalid)

    def test_scan_order_empty_and_retained_accumulators(self):
        values = Vector.of(1, 2, 3)
        initial = Vector.of(10)
        visits = []
        def append(accumulator, value):
            visits.append(value)
            return accumulator.appended(value)
        scanned = library.vector_scan(values, append, initial)
        self.assertEqual(visits, [1, 2, 3])
        self.assertEqual(scanned, Vector.of(Vector.of(10), Vector.of(10, 1), Vector.of(10, 1, 2), Vector.of(10, 1, 2, 3)))
        self.assertIs(scanned[0], initial)
        self.assertEqual(initial, Vector.of(10))
        self.assertEqual(values, Vector.of(1, 2, 3))
        self.assertEqual(library.vector_scan(Vector(), append, initial), Vector.of(initial))
        self.assertEqual(visits, [1, 2, 3])

    def test_scan_stops_on_raised_failure_and_mutable_output(self):
        visits = []
        def fail(accumulator, value):
            visits.append(value)
            return accumulator // value
        with self.assertRaises(ZeroDivisionError):
            library.vector_scan(Vector.of(2, 0, 5), fail, 10)
        self.assertEqual(visits, [2, 0])
        with self.assertRaises(TypeError):
            library.vector_scan(Vector.of(1), lambda accumulator, value: [], 0)

    def test_grouping_first_key_and_stable_nested_payload_order(self):
        a = Item("second", Vector.of("a"))
        b = Item("first", Vector.of("b"))
        c = Item("second", Vector.of("c"))
        values = Vector.of(a, b, c)
        visits = []
        def category(value):
            visits.append(value)
            return value.category
        groups = library.vector_group_by(values, category)
        self.assertIs(type(groups), OrderedMap)
        self.assertEqual(groups.keys(), Vector.of("second", "first"))
        self.assertEqual(groups["second"], Vector.of(a, c))
        self.assertIs(groups["second"][0], a)
        self.assertEqual(visits, [a, b, c])
        self.assertEqual(values, Vector.of(a, b, c))
        self.assertEqual(library.vector_group_by(Vector(), category), OrderedMap())
        self.assertEqual(visits, [a, b, c])

    def test_grouping_key_domains_bool_int_and_foreign(self):
        for key in (None, True, 7, "a", b"a"):
            with self.subTest(domain=type(key).__name__):
                groups = library.vector_group_by(Vector.of(1, 2), lambda value: key)
                self.assertEqual(groups.keys(), Vector.of(key))
                self.assertEqual(groups[key], Vector.of(1, 2))
        with self.assertRaises(TypeError):
            library.vector_group_by(Vector.of(0, 1), lambda value: False if value == 0 else 1)
        for key in (Foreign(), IntegerSubclass(1), (1,), Vector.of(1)):
            with self.assertRaises(TypeError):
                library.vector_group_by(Vector.of(1), lambda value: key)

    def test_composition_calls_in_order_and_skips_outer_on_failure(self):
        visits = []
        def inner(value):
            visits.append("inner")
            return 10 // value
        def outer(value):
            visits.append("outer")
            return value + 1
        callback = library.compose(outer, inner)
        self.assertIs(type(callback), FunctionType)
        self.assertEqual(callback.__dict__, {})
        self.assertEqual(visits, [])
        self.assertEqual(callback(2), 6)
        self.assertEqual(visits, ["inner", "outer"])
        visits.clear()
        with self.assertRaises(ZeroDivisionError):
            callback(0)
        self.assertEqual(visits, ["inner"])
        with self.assertRaises(TypeError):
            library.compose(outer, lambda value: [])(1)
        with self.assertRaises(TypeError):
            library.compose(lambda value: [], inner)(1)
        with self.assertRaises(TypeError):
            library.compose(outer, lambda value: recorded_clock((1,)))(1)

    def test_partial_first_retains_stable_data_without_constructing_calls(self):
        bound = Item("rate", Vector.of("original"))
        visits = []
        def apply(item, value):
            visits.append(value)
            return (item, value + 1)
        callback = library.partial_first(apply, bound)
        self.assertIs(type(callback), FunctionType)
        self.assertEqual(callback.__dict__, {})
        self.assertEqual(visits, [])
        result = callback(2)
        self.assertIs(result[0], bound)
        self.assertEqual(result[1], 3)
        self.assertEqual(visits, [2])
        for invalid in ([], Foreign(), recorded_clock((1,)), lambda value: value):
            with self.assertRaises(TypeError):
                library.partial_first(apply, invalid)
        with self.assertRaises(TypeError):
            library.partial_first(lambda left, right: [], bound)(1)

    def test_wrappers_pass_capability_parameter_without_retaining_it(self):
        clock = recorded_clock((7, 8))
        callback = library.compose(lambda value: value + 1, lambda capability: capability.now_ns())
        partial = library.partial_first(lambda bound, capability: bound + capability.now_ns(), 2)
        with borrow(clock) as scoped:
            self.assertEqual(callback(scoped), 8)
            self.assertEqual(partial(scoped), 10)
        with self.assertRaises(RuntimeError):
            callback(scoped)
        self.assertFalse(any(cell.cell_contents is clock or cell.cell_contents is scoped for cell in callback.__closure__))
        self.assertFalse(any(cell.cell_contents is clock or cell.cell_contents is scoped for cell in partial.__closure__))

    def test_traverse_first_error_identity_order_skip_and_success(self):
        visits = []
        error = Err(Some(Vector.of("first")))
        def validate(value):
            visits.append(value)
            return error if value == 2 else Ok(value + 1)
        self.assertIs(library.result_traverse(Vector.of(1, 2, 3), validate), error)
        self.assertEqual(visits, [1, 2])
        visits.clear()
        self.assertEqual(library.result_traverse(Vector.of(1, 3), validate), Ok(Vector.of(2, 4)))
        self.assertEqual(visits, [1, 3])
        self.assertEqual(library.result_traverse(Vector(), validate), Ok(Vector()))
        self.assertEqual(visits, [1, 3])

    def test_traverse_raised_failure_and_invalid_results_stop_immediately(self):
        visits = []
        def divide(value):
            visits.append(value)
            return Ok(10 // value)
        with self.assertRaises(ZeroDivisionError):
            library.result_traverse(Vector.of(2, 0, 5), divide)
        self.assertEqual(visits, [2, 0])
        for result in (1, Some(1), Foreign()):
            with self.assertRaises(TypeError):
                library.result_traverse(Vector.of(1), lambda value: result)

    def test_toolkit_refuses_unordered_inputs_and_foreign_callbacks(self):
        for values in ([], (1,), Set(), Set.of(1), Map(), Map.of((1, 2)), Foreign()):
            for operation, arguments in ((library.vector_scan, (values, lambda a, x: a, 0)),
                                         (library.vector_group_by, (values, lambda x: x)),
                                         (library.result_traverse, (values, lambda x: Ok(x)))):
                with self.assertRaises(TypeError):
                    operation(*arguments)
        callback = Foreign()
        for operation, arguments in ((library.vector_scan, (Vector.of(1), callback, 0)),
                                     (library.vector_group_by, (Vector.of(1), callback)),
                                     (library.result_traverse, (Vector.of(1), callback)),
                                     (library.compose, (callback, lambda x: x)),
                                     (library.compose, (lambda x: x, callback)),
                                     (library.partial_first, (callback, 0))):
            with self.assertRaises(TypeError):
                operation(*arguments)

    def test_invalid_nested_vector_is_checked_before_callback(self):
        forged = object.__new__(Vector)
        object.__setattr__(forged, "_items", (Foreign(),))
        visits = []
        def callback(value):
            visits.append(value)
            return Ok(value)
        with self.assertRaises(TypeError):
            library.result_traverse(forged, callback)
        self.assertEqual(visits, [])

    def test_rooted_io_manual_utf8_registry_zero_newlines_cleanup_and_truncation(self):
        previous = codecs.lookup_error("strict")
        handler_calls = []
        streams = []
        native_open = builtins.open
        def track(*args, **kwargs):
            stream = native_open(*args, **kwargs)
            streams.append(stream)
            return stream
        def replacement(error):
            handler_calls.append(type(error).__name__)
            return ("replacement", error.end)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad").write_bytes(b"\xff")
            (root / "truncate").write_bytes(b"existing contents")
            provider = live_io(directory, allowed_ops=("read_text", "write_text"))
            codecs.register_error("strict", replacement)
            try:
                with patch("builtins.open", track):
                    text = "\ufeffé\r\nline\rnext\n\x00𐀀"
                    provider.write_text("text", text)
                    self.assertEqual(provider.read_text("text"), text)
                    with self.assertRaises(UnicodeDecodeError):
                        provider.read_text("bad")
                    with self.assertRaises(UnicodeEncodeError):
                        provider.write_text("truncate", "\ud800")
                self.assertEqual((root / "truncate").read_bytes(), b"")
                self.assertEqual(handler_calls, [])
                self.assertEqual(len(streams), 4)
                self.assertTrue(all(stream.closed for stream in streams))
                self.assertEqual([stream.mode for stream in streams], ["wb", "rb", "rb", "wb"])
            finally:
                codecs.register_error("strict", previous)
            read_only = live_io(directory, allowed_ops=("read_text",))
            with self.assertRaises(PermissionError):
                read_only.write_text("text", "changed")

    def test_os_roots_paths_and_environment_names_reject_surrogates_before_hooks(self):
        previous = codecs.lookup_error("surrogateescape")
        events = []
        def replacement(error):
            events.append(type(error).__name__)
            return ("replacement", error.end)
        with tempfile.TemporaryDirectory() as directory:
            provider = live_io(directory, allowed_ops=("read_text", "write_text"))
            environment = live_environment()
            codecs.register_error("surrogateescape", replacement)
            try:
                for surrogate in ("\ud800", "\udfff", "\udc80", "\udcff"):
                    with self.subTest(point=ascii(surrogate)):
                        with self.assertRaises(ValueError), patch("os.path.realpath", side_effect=AssertionError("root OS call")):
                            live_io(directory + surrogate, allowed_ops=("read_text",))
                        with self.assertRaises(ValueError), patch("os.lstat", side_effect=AssertionError("path OS call")):
                            provider.read_text(surrogate)
                        with self.assertRaises(ValueError), patch("os.lstat", side_effect=AssertionError("path OS call")):
                            provider.write_text(surrogate, "text")
                        with self.assertRaises(ValueError), patch.object(os.environ, "get", side_effect=AssertionError("environment read")):
                            environment.get(surrogate, "default")
                        with self.assertRaises(ValueError):
                            recorded_environment(((surrogate, "value"),))
                        with self.assertRaises(ValueError):
                            recorded_io(((surrogate, "value"),), allowed_ops=("read_text",))
                provider.write_text("café𐀀", "valid")
                self.assertEqual(provider.read_text("café𐀀"), "valid")
                with patch.dict(os.environ, {"PYALAMODE_É_𐀀": "value"}):
                    self.assertEqual(environment.get("PYALAMODE_É_𐀀", "default"), "value")
                self.assertEqual(events, [])
            finally:
                codecs.register_error("surrogateescape", previous)
            with patch("os.path.realpath", return_value=directory + "\udc80"), self.assertRaises(ValueError):
                live_io(directory, allowed_ops=("read_text",))

    def test_live_provider_setup_refuses_unsupported_filesystem_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            for encoding, errors in (("ascii", "surrogateescape"), ("utf-8", "strict")):
                with patch("sys.getfilesystemencoding", return_value=encoding), patch("sys.getfilesystemencodeerrors", return_value=errors):
                    with self.assertRaises(RuntimeError), patch("os.path.realpath", side_effect=AssertionError("OS setup")):
                        live_io(directory, allowed_ops=("read_text",))
                    with self.assertRaises(RuntimeError):
                        live_environment()
        script = '''import json,sys,tempfile
from pyalamode import live_io,live_environment
with tempfile.TemporaryDirectory() as directory:
    outcomes=[]
    for create in (lambda:live_io(directory,allowed_ops=("read_text",)),live_environment):
        try:create()
        except RuntimeError:outcomes.append("unsupported")
        else:outcomes.append("supported")
print(json.dumps({"encoding":sys.getfilesystemencoding(),"errors":sys.getfilesystemencodeerrors(),"outcomes":outcomes}))
'''
        child_environment = dict(os.environ, PYTHONUTF8="0", PYTHONCOERCECLOCALE="0", LC_ALL="C", LANG="C")
        child = subprocess.run([sys.executable, "-c", script], env=child_environment, capture_output=True, text=True)
        self.assertEqual(child.returncode, 0, child.stderr)
        result = json.loads(child.stdout)
        expected = "supported" if result["encoding"] == "utf-8" and result["errors"] == "surrogateescape" else "unsupported"
        self.assertEqual(result["outcomes"], [expected, expected])
        if sys.platform == "linux":
            self.assertEqual(result["encoding"], "ascii")
            self.assertEqual(result["outcomes"], ["unsupported", "unsupported"])


if __name__ == "__main__":
    unittest.main()
