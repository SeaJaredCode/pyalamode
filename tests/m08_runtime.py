"""Actual external adapter semantics, isolation, hook and setup obligations."""

import binascii
import codecs
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from pyalamode import recorded_clock
from pyalamode import integrations as library


HOOKS = []
ALPHABET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


class Foreign:
    def __getattribute__(self, name):
        HOOKS.append("getattribute")
        return object.__getattribute__(self, name)

    def __buffer__(self, flags):
        HOOKS.append("buffer")
        return memoryview(b"foreign")

    def __iter__(self):
        HOOKS.append("iter")
        return iter(())

    def __bytes__(self):
        HOOKS.append("bytes")
        return b"foreign"

    def __len__(self):
        HOOKS.append("len")
        return 0

    def __str__(self):
        HOOKS.append("str")
        return "foreign"

    def __repr__(self):
        HOOKS.append("repr")
        return "foreign"

    def __eq__(self, other):
        HOOKS.append("eq")
        return False

    def __call__(self, *args):
        HOOKS.append("call")
        return b"foreign"


class BytesSubclass(bytes):
    def __len__(self):
        HOOKS.append("subclass-len")
        return 0

    def __buffer__(self, flags):
        HOOKS.append("subclass-buffer")
        return memoryview(b"foreign")

    def __bytes__(self):
        HOOKS.append("subclass-bytes")
        return b"foreign"

    def __eq__(self, other):
        HOOKS.append("subclass-eq")
        return True


class IntegrationRuntimeTests(unittest.TestCase):
    def setUp(self):
        HOOKS.clear()

    def tearDown(self):
        self.assertEqual(HOOKS, [])

    def isolated(self, source):
        process = subprocess.run([sys.executable, "-c", source], capture_output=True,
                                 text=True, cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(process.returncode, 0, process.stderr)
        return json.loads(process.stdout)

    def test_base64_known_answers_and_all_byte_order(self):
        vectors = ((b"", b""), (b"f", b"Zg=="), (b"fo", b"Zm8="),
                   (b"foo", b"Zm9v"), (b"foob", b"Zm9vYg=="),
                   (b"fooba", b"Zm9vYmE="), (b"foobar", b"Zm9vYmFy"))
        for data, encoded in vectors:
            with self.subTest(data=data):
                self.assertEqual(library.base64_encode(data), encoded)
                self.assertEqual(library.base64_decode(encoded), data)
                self.assertIs(type(library.base64_encode(data)), bytes)
                self.assertIs(type(library.base64_decode(encoded)), bytes)
        payload = bytes(range(256)) * 17 + b"\0\xff\r\n"
        encoded = library.base64_encode(payload)
        self.assertNotIn(b"\n", encoded)
        self.assertEqual(len(encoded), 4 * ((len(payload) + 2) // 3))
        self.assertEqual(library.base64_decode(encoded), payload)

    def test_sha256_known_answers_block_and_gil_boundaries(self):
        vectors = (
            (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
            (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
            (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
             "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
        )
        for data, digest in vectors:
            result = library.sha256_digest(data)
            self.assertIs(type(result), bytes)
            self.assertEqual(len(result), 32)
            self.assertEqual(result.hex(), digest)
        for size in (31, 32, 55, 56, 63, 64, 65, 127, 128, 129, 2047, 2048, 2049, 4096):
            payload = (bytes(range(256)) * ((size + 255) // 256))[:size]
            self.assertEqual(library.sha256_digest(payload), hashlib.sha256(payload).digest())

    def test_nonzero_padding_bits_are_refused_for_every_single_byte(self):
        # Native strict mode admits these unused-bit alternatives; our canonical
        # contract deliberately refuses them rather than silently normalizing.
        for value in range(256):
            canonical = library.base64_encode(bytes((value,)))
            index = ALPHABET.index(canonical[1])
            self.assertEqual(index & 15, 0)
            for low_bits in range(1, 16):
                noncanonical = canonical[:1] + bytes((ALPHABET[index + low_bits],)) + b"=="
                self.assertEqual(binascii.a2b_base64(noncanonical, strict_mode=True), bytes((value,)))
                with self.assertRaisesRegex(ValueError, "^invalid canonical base64$"):
                    library.base64_decode(noncanonical)
        for noncanonical in (b"Zm9=", b"Zm+=", b"Zm/="):
            with self.assertRaises(ValueError):
                library.base64_decode(noncanonical)

    def test_malformed_grammar_raises_fixed_error_without_native_context(self):
        malformed = (b"=", b"====", b"A", b"AA", b"AAA", b"Zg=", b"Zg===",
                     b"Zm9v=", b"Zg==Zg==", b"Zg==\0", b"AA\n==", b"Z g==",
                     b"Zg==\r\n", b"-w==", b"_w==", b"\xff", b"\0", b"!", b"AA=A")
        for value in malformed:
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as caught:
                    library.base64_decode(value)
                error = caught.exception
                self.assertIs(type(error), ValueError)
                self.assertEqual(error.args, ("invalid canonical base64",))
                self.assertIsNone(error.__context__)
                self.assertIsNone(error.__cause__)

    def test_published_input_and_decoded_output_size_bounds(self):
        maximum = b"x" * 1_048_576
        encoded = library.base64_encode(maximum)
        self.assertEqual(len(encoded), 1_398_104)
        self.assertEqual(library.base64_decode(encoded), maximum)
        self.assertEqual(library.sha256_digest(maximum), hashlib.sha256(maximum).digest())
        # A one-byte-too-large decoded payload still has the permitted encoded
        # length, so the independent decoded-output bound is essential.
        encoded_overflow = binascii.b2a_base64(maximum + b"x", newline=False)
        self.assertEqual(len(encoded_overflow), 1_398_104)
        with self.assertRaisesRegex(ValueError, "^decoded data exceeds"):
            library.base64_decode(encoded_overflow)
        with patch.object(library._binascii, "b2a_base64", side_effect=AssertionError("backend ran")), \
             patch.object(library._binascii, "a2b_base64", side_effect=AssertionError("backend ran")), \
             patch.object(library._sha2, "sha256", side_effect=AssertionError("backend ran")):
            for operation in (library.base64_encode, library.sha256_digest):
                with self.assertRaises(ValueError):
                    operation(maximum + b"x")
            with self.assertRaises(ValueError):
                library.base64_decode(b"A" * 1_398_105)

    def test_exact_input_refusal_precedes_all_foreign_hooks_and_backend_calls(self):
        mutable = bytearray(b"YWJj")
        capability = recorded_clock((7,))
        values = (Foreign(), BytesSubclass(b"YWJj"), mutable, memoryview(mutable),
                  memoryview(mutable).toreadonly(), "YWJj", (b"YWJj",), [b"YWJj"],
                  {"data": b"YWJj"}, 0, True, None, lambda: b"YWJj", capability)
        with patch.object(library._binascii, "b2a_base64", side_effect=AssertionError("backend ran")), \
             patch.object(library._binascii, "a2b_base64", side_effect=AssertionError("backend ran")), \
             patch.object(library._sha2, "sha256", side_effect=AssertionError("backend ran")):
            for operation in (library.base64_encode, library.base64_decode, library.sha256_digest):
                for value in values:
                    with self.subTest(operation=operation.__name__, kind=type(value).__name__):
                        with self.assertRaises(TypeError):
                            operation(value)
                        self.assertEqual(HOOKS, [])
        self.assertEqual(capability.now_ns(), 7)

    def test_exact_positional_only_public_signatures(self):
        for name in library.__all__:
            function = getattr(library, name)
            parameters = list(inspect.signature(function).parameters.values())
            self.assertEqual(len(parameters), 1)
            self.assertEqual(parameters[0].kind, inspect.Parameter.POSITIONAL_ONLY)
            with self.assertRaises(TypeError):
                function(data=b"")
            with self.assertRaises(TypeError):
                function(b"", b"")

    def test_retained_outputs_and_ordinary_source_snapshot_are_isolated(self):
        source = bytearray(range(256))
        snapshot = bytes(source)
        encoded = library.base64_encode(snapshot)
        decoded = library.base64_decode(encoded)
        digest = library.sha256_digest(snapshot)
        source[:] = b"changed"
        for value in (b"different", b"", b"\xff\0"):
            library.base64_decode(library.base64_encode(value))
            library.sha256_digest(value)
        self.assertEqual(snapshot, bytes(range(256)))
        self.assertEqual(decoded, snapshot)
        self.assertEqual(encoded, binascii.b2a_base64(snapshot, newline=False))
        self.assertEqual(digest, hashlib.sha256(snapshot).digest())
        self.assertIs(type(decoded), bytes)

    def test_no_codec_registry_or_hashlib_dispatch(self):
        previous = {name: codecs.lookup_error(name) for name in ("strict", "surrogateescape")}
        calls = []
        def replacement(error):
            calls.append("error-handler")
            return ("replacement", error.end)
        for name in previous:
            codecs.register_error(name, replacement)
        try:
            with patch("codecs.lookup", side_effect=AssertionError("codec lookup")), \
                 patch("hashlib.new", side_effect=AssertionError("algorithm dispatch")), \
                 patch("hashlib.sha256", side_effect=AssertionError("hashlib dispatch")):
                payload = b"\0\xff\xc0\xed\xa0\x80"
                self.assertEqual(library.base64_decode(library.base64_encode(payload)), payload)
                self.assertEqual(library.sha256_digest(b"abc").hex(),
                                 "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
                with self.assertRaises(ValueError):
                    library.base64_decode(b"\xff")
            self.assertEqual(calls, [])
        finally:
            for name, handler in previous.items():
                codecs.register_error(name, handler)

    def test_root_import_does_not_load_external_adapters_and_setup_is_observable(self):
        observed = self.isolated('''import json,sys
requests=[]
class Finder:
    def find_spec(self,name,path=None,target=None):
        if name in {"pyalamode.integrations","binascii","_sha2"}: requests.append(name)
        return None
sys.meta_path.insert(0,Finder())
import pyalamode
root_requests=list(requests)
assert not root_requests
assert all(name not in sys.modules for name in ("pyalamode.integrations","binascii","_sha2"))
from pyalamode import integrations
setup_requests=list(requests)
requests.clear()
assert integrations.base64_decode(integrations.base64_encode(b"abc"))==b"abc"
assert len(integrations.sha256_digest(b"abc"))==32
print(json.dumps(dict(root_requests=root_requests,setup_requests=setup_requests,invocation_requests=requests)))
''')
        self.assertEqual(observed["root_requests"], [])
        self.assertEqual(set(observed["setup_requests"]), {"pyalamode.integrations", "binascii", "_sha2"})
        self.assertEqual(observed["invocation_requests"], [])

    def test_mutable_native_error_constructor_and_bases_are_real_trust_preconditions(self):
        observed = self.isolated('''import binascii,json
from pyalamode.integrations import base64_decode
hits=[]
def changed(self,*args):
    hits.append("Error.__init__")
    ValueError.__init__(self,*args)
binascii.Error.__init__=changed
try:
    base64_decode(b"!")
except ValueError as error:
    assert type(error) is ValueError
    assert error.__context__ is None and error.__cause__ is None
    print(json.dumps(dict(hits=hits,args=error.args)))
''')
        self.assertEqual(observed, {"hits": ["Error.__init__"], "args": ["invalid canonical base64"]})
        inherited = self.isolated('''import binascii,json
from pyalamode.integrations import base64_decode
hits=[]
class ChangedBase(ValueError):
    __slots__=()
    def __init__(self,*args):
        hits.append("Error base constructor")
        super().__init__(*args)
binascii.Error.__bases__=(ChangedBase,)
try:
    base64_decode(b"!")
except ValueError as error:
    assert type(error) is ValueError
    assert error.__context__ is None and error.__cause__ is None
    print(json.dumps(dict(hits=hits,args=error.args)))
''')
        self.assertEqual(inherited, {"hits": ["Error base constructor"], "args": ["invalid canonical base64"]})

    def test_exact_output_does_not_prove_rebound_backend_pure(self):
        calls = []
        original = library._binascii.b2a_base64
        def changed(data, *, newline):
            calls.append("observable changed backend")
            return original(data, newline=newline)
        with patch.object(library._binascii, "b2a_base64", changed):
            result = library.base64_encode(b"abc")
        self.assertIs(type(result), bytes)
        self.assertEqual(result, b"YWJj")
        self.assertEqual(calls, ["observable changed backend"])
        # Ordinary use has no approval service or live rebinding monitor. Static
        # writer/approval gates and the unchanged dependency assumption supply
        # the checked claim; data validation alone cannot replace them.


if __name__ == "__main__":
    unittest.main()
