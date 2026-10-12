"""Ordinary-runtime effect declarations, finite providers and logical leases."""

import builtins
import importlib
import os
from pathlib import Path
import tempfile
import typing
import unittest
from unittest.mock import patch
from types import GenericAlias

from pyalamode.effects import (
    effects, Effectful, IO, State, Clock, Random, Environment,
    IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability,
    borrow, live_io, recorded_io, state, live_clock, recorded_clock,
    live_random, recorded_random, live_environment, recorded_environment,
)
from pyalamode import Vector, record, freeze, thaw
from pyalamode.boundaries import validate_data

runtime = importlib.import_module("pyalamode.effects")
FULL_IO = ("read_text", "write_text")


class Hooks:
    calls = []

    def __iter__(self):
        self.calls.append("iter")
        return iter(())

    def __hash__(self):
        self.calls.append("hash")
        return 1

    def __eq__(self, other):
        self.calls.append("eq")
        return False

    def __repr__(self):
        self.calls.append("repr")
        return "foreign"


class StringHooks(str):
    def __hash__(self):
        Hooks.calls.append("stringhash")
        return str.__hash__(self)

    def __eq__(self, other):
        Hooks.calls.append("stringeq")
        return str.__eq__(self, other)

    def __str__(self):
        Hooks.calls.append("stringstr")
        return str.__str__(self)


class TupleHooks(tuple):
    def __iter__(self):
        Hooks.calls.append("tupleiter")
        return tuple.__iter__(self)


class MetaHooks(type):
    def __eq__(self, other):
        Hooks.calls.append("metaeq")
        return False

    def __hash__(self):
        Hooks.calls.append("metahash")
        return 1

    def __getattribute__(self, name):
        Hooks.calls.append("metaget")
        return type.__getattribute__(self, name)


class Foreign(metaclass=MetaHooks):
    pass


@record
class Count:
    value: int


class M05Runtime(unittest.TestCase):
    def setUp(self):
        Hooks.calls.clear()

    def test_declaration_identity_and_metadata_unchanged(self):
        captured = object()

        def function(value=3):
            return captured, value

        function.flag = "existing"
        before = (function.__code__, function.__closure__, function.__defaults__, dict(function.__dict__))
        self.assertIs(effects(IO, State, Clock, Random, Environment)(function), function)
        self.assertEqual(before, (function.__code__, function.__closure__, function.__defaults__, function.__dict__))
        self.assertIs(effects(Clock)(captured), captured)

    def test_declaration_family_exact_first(self):
        for families in ((), ("Future",), ("Unknown",), (Clock, Clock), (Hooks(),), (StringHooks(Clock),)):
            with self.subTest(families=tuple(type(value).__name__ for value in families)):
                with self.assertRaises(TypeError):
                    effects(*families)
        self.assertEqual(Hooks.calls, [])

    def test_effectful_fixed_alias_and_schema_copy(self):
        parameters = [ClockCapability, Vector[int], Count, tuple[str, ...]]
        annotation = Effectful[parameters, int, Clock]
        self.assertIs(type(annotation), GenericAlias)
        self.assertIs(annotation.__origin__, Effectful)
        self.assertEqual(annotation.__args__, (tuple(parameters), int, Clock))
        parameters.append(str)
        self.assertEqual(len(annotation.__args__[0]), 4)
        self.assertIs(Effectful[[], None, State].__origin__, Effectful)
        self.assertIs(Effectful[[typing.Callable[[int], int]], int, Clock].__origin__, Effectful)
        self.assertIs(Effectful[[Effectful[[StateCapability], int, State]], int, Clock].__origin__, Effectful)

    def test_effectful_rejects_unknown_types_hooks_and_capability_escape(self):
        bad = (lambda: Effectful[[ClockCapability], int, State],
               lambda: Effectful[[int], ClockCapability, Clock],
               lambda: Effectful[[tuple[ClockCapability]], int, Clock],
               lambda: Effectful[[typing.Callable[[ClockCapability], int]], int, Clock],
               lambda: Effectful[[typing.Callable[..., int]], int, Clock],
               lambda: Effectful[[Hooks()], int, Clock],
               lambda: Effectful[[Foreign], int, Clock],
               lambda: Effectful[[int], int, StringHooks(Clock)],
               lambda: Effectful[[int], int, "Future"],
               lambda: Effectful[(int,), int, Clock],
               lambda: Effectful[[int], int],
               lambda: Effectful())
        for function in bad:
            with self.assertRaises(TypeError):
                function()
        self.assertEqual(Hooks.calls, [])
        with self.assertRaises(TypeError):
            class Child(Effectful):
                pass

    def test_capability_exact_classes_opaque_mutation_and_subclasses(self):
        providers = (recorded_io((), allowed_ops=FULL_IO), state(1), recorded_clock(()),
                     recorded_random(()), recorded_environment(()))
        classes = (IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability)
        for provider, kind in zip(providers, classes):
            self.assertIs(type(provider), kind)
            with self.assertRaises(TypeError):
                kind()
            with self.assertRaises(TypeError):
                type("Child", (kind,), {})
            with self.assertRaises(AttributeError):
                provider._provider = Hooks()
            with self.assertRaises(AttributeError):
                del provider._lease
            with self.assertRaises(TypeError):
                hash(provider)
            self.assertFalse(hasattr(provider, "__dict__"))
            self.assertIn("<opaque>", repr(provider))

    def test_state_exact_integer_private_cell(self):
        first, second = state(2), state(2)
        self.assertEqual(first.get(), 2)
        self.assertIsNone(first.set(5))
        self.assertEqual(first.get(), 5)
        self.assertEqual(second.get(), 2)
        for value in (True, "2", Hooks(), Foreign()):
            with self.assertRaises(TypeError):
                state(value)
            with self.assertRaises(TypeError):
                first.set(value)
        self.assertEqual(Hooks.calls, [])

    def test_clock_live_recorded_and_exhaustion(self):
        provider = recorded_clock((10, -3, 10))
        self.assertEqual([provider.now_ns() for _ in range(3)], [10, -3, 10])
        with self.assertRaises(IndexError):
            provider.now_ns()
        self.assertIs(type(live_clock().now_ns()), int)
        self.assertEqual(recorded_clock((10,)).now_ns(), 10)

    def test_random_recorded_bounds_and_nonconsuming_failure(self):
        provider = recorded_random((3, 0))
        with self.assertRaises(ValueError):
            provider.below(3)
        self.assertEqual(provider.below(4), 3)
        for bound in (0, -2):
            with self.assertRaises(ValueError):
                provider.below(bound)
        for bound in (True, "4", Hooks()):
            with self.assertRaises(TypeError):
                provider.below(bound)
        self.assertEqual(provider.below(1), 0)
        with self.assertRaises(IndexError):
            provider.below(5)
        self.assertEqual(Hooks.calls, [])

    def test_random_live_rejection_sampling_and_singleton(self):
        provider = live_random()
        with patch.object(runtime.os, "urandom", side_effect=[b"\x03", b"\x02"]) as entropy:
            self.assertEqual(provider.below(3), 2)
            self.assertEqual(entropy.call_args_list[0].args, (1,))
            self.assertEqual(entropy.call_count, 2)
        with patch.object(runtime.os, "urandom", side_effect=AssertionError("singleton sampled")):
            self.assertEqual(provider.below(1), 0)
        for bound in (2, 3, 257, 2**80 + 1):
            for _ in range(10):
                value = provider.below(bound)
                self.assertIs(type(value), int)
                self.assertTrue(0 <= value < bound)
        with patch.object(runtime.os, "urandom", side_effect=OSError("entropy unavailable")):
            with self.assertRaises(OSError):
                provider.below(3)

    def test_recorded_integer_inputs_exact_before_hooks(self):
        for factory in (recorded_clock, recorded_random):
            for values in (Hooks(), [1], TupleHooks((1,)), (True,), (Hooks(),)):
                with self.assertRaises(TypeError):
                    factory(values)
        self.assertEqual(Hooks.calls, [])

    def test_environment_live_recorded_names_defaults(self):
        provider = recorded_environment((("PYALAMODE_M05_RUNTIME", "recorded"),))
        self.assertEqual(provider.get("PYALAMODE_M05_RUNTIME", "absent"), "recorded")
        self.assertEqual(provider.get("PYALAMODE_M05_MISSING", "absent"), "absent")
        with patch.dict(os.environ, {"PYALAMODE_M05_RUNTIME": "live"}):
            self.assertEqual(live_environment().get("PYALAMODE_M05_RUNTIME", "absent"), "live")
        for name in ("", "a=b", "a\x00b"):
            with self.assertRaises(ValueError):
                provider.get(name, "default")
        for name, default in ((StringHooks("n"), "d"), ("n", StringHooks("d")), (Hooks(), "d"), ("n", Hooks())):
            with self.assertRaises(TypeError):
                provider.get(name, default)
        self.assertEqual(Hooks.calls, [])

    def test_recorded_pair_input_exact_unique_and_hook_free(self):
        for factory in (recorded_environment, lambda data: recorded_io(data, allowed_ops=FULL_IO)):
            for entries in (Hooks(), TupleHooks(()), [()], (Hooks(),), (["n", "v"],), (("n",),),
                            ((StringHooks("n"), "v"),), (("n", StringHooks("v")),), (("n", Hooks()),)):
                with self.assertRaises(TypeError):
                    factory(entries)
            with self.assertRaises(ValueError):
                factory((("n", "a"), ("n", "b")))
        self.assertEqual(Hooks.calls, [])

    def test_recorded_io_shared_updates_missing_and_permissions(self):
        provider = recorded_io((("a.txt", "one"),), allowed_ops=FULL_IO)
        self.assertEqual(provider.read_text("a.txt"), "one")
        self.assertIsNone(provider.write_text("a.txt", "two"))
        self.assertEqual(provider.read_text("a.txt"), "two")
        provider.write_text("nested/new.txt", "new")
        self.assertEqual(provider.read_text("nested/new.txt"), "new")
        with self.assertRaises(KeyError):
            provider.read_text("missing")
        read_only = recorded_io((("a", "v"),), allowed_ops=("read_text",))
        self.assertEqual(read_only.read_text("a"), "v")
        with self.assertRaises(PermissionError):
            read_only.write_text("a", "x")
        write_only = recorded_io((), allowed_ops=("write_text",))
        write_only.write_text("a", "x")
        with self.assertRaises(PermissionError):
            write_only.read_text("a")

    def test_io_allowed_operations_required_exact_and_unique(self):
        with tempfile.TemporaryDirectory() as directory:
            factories = (lambda ops: live_io(directory, allowed_ops=ops), lambda ops: recorded_io((), allowed_ops=ops))
            for factory in factories:
                for ops in (Hooks(), ["read_text"], TupleHooks(("read_text",)), (Hooks(),), (StringHooks("read_text"),)):
                    with self.assertRaises(TypeError):
                        factory(ops)
                for ops in ((), ("read_text", "read_text"), ("other",)):
                    with self.assertRaises(ValueError):
                        factory(ops)
            with self.assertRaises(TypeError):
                live_io(directory)
            with self.assertRaises(TypeError):
                recorded_io(())
        self.assertEqual(Hooks.calls, [])

    def test_live_io_utf8_newlines_nested_and_root_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "nested").mkdir()
            provider = live_io(directory, allowed_ops=FULL_IO)
            text = "héllo\r\nworld\n"
            provider.write_text("nested/value.txt", text)
            self.assertEqual(provider.read_text("nested/value.txt"), text)
            self.assertEqual(Path(directory, "nested/value.txt").read_bytes(), text.encode("utf-8"))
            with self.assertRaises(FileNotFoundError):
                provider.read_text("missing")
            with self.assertRaises(FileNotFoundError):
                provider.write_text("absent/child", "x")
            with self.assertRaises(NotADirectoryError):
                live_io(str(Path(directory, "missing")), allowed_ops=FULL_IO)
            with self.assertRaises(NotADirectoryError):
                live_io(str(Path(directory, "nested/value.txt")), allowed_ops=FULL_IO)
        for root in (Hooks(), StringHooks("."), Path(".")):
            with self.assertRaises(TypeError):
                live_io(root, allowed_ops=FULL_IO)
        for root in ("", "\x00"):
            with self.assertRaises(ValueError):
                live_io(root, allowed_ops=FULL_IO)
        self.assertEqual(Hooks.calls, [])

    def test_io_relative_paths_hook_free_and_symlink_refusal(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            Path(outside, "secret").write_text("outside")
            Path(directory, "link").symlink_to(outside, target_is_directory=True)
            Path(directory, "file-link").symlink_to(Path(outside, "secret"))
            for provider in (live_io(directory, allowed_ops=FULL_IO), recorded_io((), allowed_ops=FULL_IO)):
                for path in ("", "/absolute", "../secret", "a/../b", ".", "a//b", "a/", "a\\b", "a\x00b"):
                    with self.assertRaises(ValueError):
                        provider.read_text(path)
                    with self.assertRaises(ValueError):
                        provider.write_text(path, "x")
                for path in (Hooks(), StringHooks("name")):
                    with self.assertRaises(TypeError):
                        provider.read_text(path)
                with self.assertRaises(TypeError):
                    provider.write_text("name", StringHooks("x"))
            provider = live_io(directory, allowed_ops=FULL_IO)
            for path in ("link/secret", "file-link"):
                with self.assertRaises(PermissionError):
                    provider.read_text(path)
                with self.assertRaises(PermissionError):
                    provider.write_text(path, "overwrite")
            self.assertEqual(Path(outside, "secret").read_text(), "outside")
        self.assertEqual(Hooks.calls, [])

    def test_live_io_actual_opened_stream_closed_on_success_and_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            provider = live_io(directory, allowed_ops=FULL_IO)
            opened = []

            def observe(*args, **kwargs):
                stream = builtins.open(*args, **kwargs)
                opened.append(stream)
                return stream

            with patch.object(runtime, "open", side_effect=observe, create=True):
                provider.write_text("normal", "ok")
                self.assertEqual(provider.read_text("normal"), "ok")
                Path(directory, "invalid").write_bytes(b"\xff")
                with self.assertRaises(UnicodeDecodeError):
                    provider.read_text("invalid")
                with self.assertRaises(UnicodeEncodeError):
                    provider.write_text("invalid-write", "\ud800")
            self.assertEqual(len(opened), 4)
            self.assertTrue(all(stream.closed for stream in opened))

    def test_live_io_denied_permission_never_opens(self):
        with tempfile.TemporaryDirectory() as directory:
            provider = live_io(directory, allowed_ops=("read_text",))
            with patch.object(runtime, "open", side_effect=AssertionError("opened"), create=True):
                with self.assertRaises(PermissionError):
                    provider.write_text("denied", "x")

    def test_borrow_view_shares_state_and_closes_one_way(self):
        original = state(1)
        context = borrow(original)
        with context as view:
            self.assertIs(type(view), StateCapability)
            self.assertIsNot(view, original)
            view.set(4)
            self.assertEqual(original.get(), 4)
        self.assertEqual(original.get(), 4)
        for operation in (view.get, lambda: view.set(5), lambda: borrow(view), context.__enter__,
                          lambda: context.__exit__(None, None, None)):
            with self.assertRaises(RuntimeError):
                operation()
        with self.assertRaises(AttributeError):
            context._status = "fresh"
        with self.assertRaises(AttributeError):
            del context._lease

    def test_borrow_nested_child_closure_and_original_liveness(self):
        original = state(5)
        with borrow(original) as outer:
            with borrow(outer) as inner:
                inner.set(8)
            with self.assertRaises(RuntimeError):
                inner.get()
            self.assertEqual(outer.get(), 8)
        with self.assertRaises(RuntimeError):
            outer.get()
        self.assertEqual(original.get(), 8)

    def test_borrow_ancestor_exit_closes_active_descendant(self):
        original = state(1)
        parent = borrow(original)
        outer = parent.__enter__()
        child = borrow(outer)
        inner = child.__enter__()
        parent.__exit__(None, None, None)
        with self.assertRaises(RuntimeError):
            inner.get()
        self.assertFalse(child.__exit__(None, None, None))
        self.assertEqual(original.get(), 1)

    def test_borrow_exception_cleanup_and_preentry_misuse(self):
        original = state(1)
        failure = LookupError("body failed")
        with self.assertRaises(LookupError) as raised:
            with borrow(original) as view:
                raise failure
        self.assertIs(raised.exception, failure)
        with self.assertRaises(RuntimeError):
            view.get()
        self.assertEqual(original.get(), 1)
        context = borrow(original)
        with self.assertRaises(RuntimeError):
            context.__exit__(None, None, None)
        with context as view:
            self.assertEqual(view.get(), 1)
        for value in (Hooks(), Foreign(), 1):
            with self.assertRaises(TypeError):
                borrow(value)
        self.assertEqual(Hooks.calls, [])

    def test_borrow_preserves_all_provider_interfaces_and_permissions(self):
        providers = (recorded_io((("n", "v"),), allowed_ops=("read_text",)),
                     recorded_clock((7, 9)), recorded_random((2, 1)), recorded_environment((("N", "V"),)))
        for provider in providers:
            with borrow(provider) as view:
                self.assertIs(type(view), type(provider))
                if type(provider) is IOCapability:
                    self.assertEqual(view.read_text("n"), "v")
                    with self.assertRaises(PermissionError):
                        view.write_text("n", "x")
                elif type(provider) is ClockCapability:
                    self.assertEqual(view.now_ns(), 7)
                elif type(provider) is RandomCapability:
                    self.assertEqual(view.below(3), 2)
                else:
                    self.assertEqual(view.get("N", "default"), "V")
            with self.assertRaises(RuntimeError):
                borrow(view)
        self.assertEqual(providers[1].now_ns(), 9)
        self.assertEqual(providers[2].below(3), 1)

    def test_capabilities_rejected_by_stable_data_boundaries(self):
        providers = (state(1), recorded_clock(()), recorded_random(()), recorded_environment(()),
                     recorded_io((), allowed_ops=FULL_IO))
        for provider in providers:
            for operation in (lambda: Vector.of(provider), lambda: Count(provider),
                              lambda: freeze(provider, exclusive=True), lambda: thaw(provider),
                              lambda: validate_data(provider, int)):
                with self.assertRaises(TypeError):
                    operation()

    def test_malformed_exact_capability_metadata_rejects_before_hooks(self):
        for kind in (IOCapability, StateCapability, ClockCapability, RandomCapability, EnvironmentCapability):
            malformed = object.__new__(kind)
            with self.assertRaises(TypeError):
                borrow(malformed)
        provider = state(1)
        object.__setattr__(provider, "_provider", Hooks())
        with self.assertRaises(TypeError):
            provider.get()
        provider = state(1)
        object.__setattr__(provider._provider, "mode", Hooks())
        with self.assertRaises(TypeError):
            provider.get()
        provider = recorded_environment((("N", "V"),))
        object.__setattr__(provider._provider, "data", ((StringHooks("N"), "V"),))
        with self.assertRaises(TypeError):
            provider.get("N", "default")
        provider = recorded_clock((1,))
        object.__setattr__(provider._provider, "data", (Hooks(),))
        with self.assertRaises(TypeError):
            provider.now_ns()
        self.assertEqual(Hooks.calls, [])

    def test_forged_lease_cycle_rejects_finitely(self):
        context = borrow(state(1))
        view = context.__enter__()
        object.__setattr__(view._lease, "parent", view._lease)
        with self.assertRaises(TypeError):
            view.get()
        context.__exit__(None, None, None)

    def test_malformed_context_exact_metadata_before_hooks(self):
        context = borrow(state(1))
        object.__setattr__(context, "_status", StringHooks("fresh"))
        with self.assertRaises(TypeError):
            context.__enter__()
        with self.assertRaises(TypeError):
            context.__exit__(None, None, None)
        context = object.__new__(runtime._Borrow)
        with self.assertRaises(TypeError):
            context.__enter__()
        context = borrow(state(1))
        view = context.__enter__()
        object.__setattr__(context, "_lease", Hooks())
        with self.assertRaises(TypeError):
            context.__exit__(None, None, None)
        object.__setattr__(view._lease, "parent", object.__new__(runtime._Lease))
        with self.assertRaises(TypeError):
            view.get()
        self.assertEqual(Hooks.calls, [])


if __name__ == "__main__":
    unittest.main()
