"""Focused ordinary runtime invariants; source confinement belongs to checking."""

import _thread
import json
import threading
import unittest
from types import GenericAlias

from pyalamode import fun, record, Some, Nothing, Ok, Err
from pyalamode import collections as collection_runtime
from pyalamode.boundaries import validate_data
from pyalamode.collections import Vector, Map, OrderedMap, Set
from pyalamode.builders import VectorBuilder, vector_build
from pyalamode.builder_contracts import (
    BUILDER_VERSION, BUILDERS_NAMES, BUILDERS_FOUNDATIONS, operation_catalog, operation_contract,
)
from pyalamode.encoding import value_encode


@record
class RuntimeItem:
    label: str
    values: Vector[int]


class Hooks:
    calls = []

    def __getattribute__(self, name):
        Hooks.calls.append("attribute")
        return object.__getattribute__(self, name)

    def __call__(self, *arguments):
        Hooks.calls.append("call")
        raise AssertionError("foreign call")

    def __iter__(self):
        Hooks.calls.append("iteration")
        raise AssertionError("foreign iteration")

    def __repr__(self):
        Hooks.calls.append("representation")
        raise AssertionError("foreign representation")

    def __eq__(self, other):
        Hooks.calls.append("equality")
        raise AssertionError("foreign equality")

    def __hash__(self):
        Hooks.calls.append("hash")
        raise AssertionError("foreign hash")


class HostileMeta(type):
    def __getattribute__(cls, name):
        Hooks.calls.append("metaclass attribute")
        raise AssertionError("foreign metaclass attribute")

    def __eq__(cls, other):
        Hooks.calls.append("metaclass equality")
        raise AssertionError("foreign metaclass equality")


class Foreign(metaclass=HostileMeta):
    pass


class Abort(BaseException):
    pass


def stored(vector):
    assert type(vector) is Vector
    data = object.__getattribute__(vector, "_items")
    assert type(data) is tuple
    return data


class RuntimeBuilders(unittest.TestCase):
    def setUp(self):
        Hooks.calls.clear()

    def expired(self, builder):
        for call in (lambda: builder.append(19), lambda: builder.extend(Vector.of(19))):
            with self.assertRaisesRegex(RuntimeError, "^builder: construction is no longer active$"):
                call()
        self.assertIs(object.__getattribute__(builder, "_active"), False)
        self.assertIsNone(object.__getattribute__(builder, "_items"))

    def test_empty_and_prefix_completion(self):
        self.assertEqual(stored(vector_build(lambda builder: None)), ())
        def fill(builder):
            builder.append(3)
            return None
        self.assertEqual(stored(vector_build(fill)), (3,))

    def test_append_extend_order_and_callback_once(self):
        events = []
        def fill(builder):
            events.append("callback")
            self.assertIsNone(builder.append(3))
            events.append("append")
            self.assertIsNone(builder.extend(Vector.of(5, 7)))
            events.append("extend")
            builder.append(11)
        result = vector_build(fill)
        events.append("returned")
        self.assertEqual(events, ["callback", "append", "extend", "returned"])
        self.assertEqual(stored(result), (3, 5, 7, 11))

    def test_useful_ordered_map_filter_assembly(self):
        source = Vector.of(-2, 0, 3, 4)
        def fill(builder):
            builder.append(0)
            builder.extend(source.map(lambda value: value * 2).filter(lambda value: value > 0))
            builder.append(-1)
        self.assertEqual(stored(vector_build(fill)), (0, 6, 8, -1))
        self.assertEqual(stored(source), (-2, 0, 3, 4))

    def test_nested_values_and_retained_versions(self):
        old = Vector.of((3, Vector.of(5)))
        item = RuntimeItem("saved", Vector.of(7))
        nested = (item, Some(old), Nothing(), Ok(item), Err("error"),
                  Map.of(("b", old), ("a", item)), OrderedMap.of((2, old), (1, item)), Set.of(11, 7))
        def fill(builder):
            builder.extend(old)
            builder.append(nested)
            builder.append(nested)
        result = vector_build(fill)
        revised = result.appended(17)
        self.assertEqual(stored(old)[0][0], 3)
        self.assertEqual(stored(result)[0][0], 3)
        self.assertIs(stored(result)[1], nested)
        self.assertIs(stored(result)[2], nested)
        self.assertEqual(len(stored(result)), 3)
        self.assertEqual(len(stored(revised)), 4)
        self.assertEqual(stored(item.values), (7,))

    def test_staging_list_is_cleared_and_not_final_storage(self):
        held, lists = [], []
        def fill(builder):
            held.append(builder)
            lists.append(object.__getattribute__(builder, "_items"))
            builder.append(3)
        result = vector_build(fill)
        self.assertEqual(lists, [[]])
        lists[0].append(99)  # deliberate raw alias cannot mutate published tuple
        self.assertEqual(stored(result), (3,))
        self.expired(held[0])

    def test_expired_builder_and_bound_methods_after_success(self):
        held, methods = [], []
        def fill(builder):
            held.append(builder)
            methods.extend((builder.append, builder.extend))
            builder.append(3)
        self.assertEqual(stored(vector_build(fill)), (3,))
        self.expired(held[0])
        for method, argument in zip(methods, (7, Vector.of(7))):
            with self.assertRaises(RuntimeError):
                method(argument)

    def test_every_failure_revokes_preserving_exception_identity(self):
        for error in (ZeroDivisionError("fixed"), Abort("fixed"), KeyboardInterrupt(), SystemExit(7)):
            held = []
            def fail(builder):
                held.append(builder)
                builder.append(3)
                raise error
            with self.assertRaises(type(error)) as caught:
                vector_build(fail)
            self.assertIs(caught.exception, error)
            self.expired(held[0])

    def test_invalid_callback_returns_revoke(self):
        for returned in (False, 0, (), Vector.of(3), Hooks()):
            held = []
            def fill(builder):
                held.append(builder)
                builder.append(3)
                return returned
            with self.assertRaisesRegex(TypeError, "^callback: construction callback must return exact None$"):
                vector_build(fill)
            self.expired(held[0])
        held = []
        def return_builder(builder):
            held.append(builder)
            return builder
        with self.assertRaises(TypeError):
            vector_build(return_builder)
        self.expired(held[0])
        self.assertEqual(Hooks.calls, [])

    def test_callback_types_refuse_without_hooks(self):
        def fill(builder):
            pass
        for callback in (Hooks(), Foreign(), abs, fill.__call__):
            with self.assertRaisesRegex(TypeError, "^callback: expected an exact Python function"):
                vector_build(callback)
        self.assertEqual(Hooks.calls, [])

    def test_no_annotation_defaults_capture_or_purity_introspection(self):
        events = []
        def ordinary(builder, default=Hooks()):
            events.append("ordinary side effect")
            builder.append(47)
        ordinary.__annotations__ = {"builder": Hooks(), "return": Hooks()}
        self.assertIs(fun(ordinary), ordinary)
        self.assertEqual(stored(vector_build(ordinary)), (47,))
        self.assertEqual(events, ["ordinary side effect"])
        self.assertEqual(Hooks.calls, [])

    def test_wrong_function_signature_and_keywords_refuse(self):
        with self.assertRaises(TypeError):
            vector_build(lambda: None)
        with self.assertRaises(TypeError):
            vector_build(callback=lambda builder: None)
        def fill(builder):
            with self.assertRaises(TypeError):
                builder.append(value=3)
            with self.assertRaises(TypeError):
                builder.extend(values=Vector.of(3))
            builder.append(5)
        self.assertEqual(stored(vector_build(fill)), (5,))

    def test_generic_erasure_and_selected_data_validation(self):
        alias = VectorBuilder[int]
        self.assertIs(type(alias), GenericAlias)
        self.assertIs(alias.__origin__, VectorBuilder)
        def erased(builder: VectorBuilder[int]) -> None:
            builder.append("stable but wrong T")
        value = vector_build(erased)
        self.assertEqual(stored(value), ("stable but wrong T",))
        with self.assertRaises(TypeError):
            validate_data(value, ("Vector", ("int",)))

    def test_public_constructor_subclass_attributes_hash_and_dict_refuse(self):
        for constructor in (VectorBuilder, VectorBuilder[int]):
            with self.assertRaisesRegex(TypeError, "^VectorBuilder: use vector_build; direct construction is unsupported$"):
                constructor()
        with self.assertRaisesRegex(TypeError, "^VectorBuilder: exact construction subclasses are unsupported$"):
            type("Child", (VectorBuilder,), {})
        def fill(builder):
            with self.assertRaisesRegex(AttributeError, "cannot be assigned$"):
                builder.extra = 3
            with self.assertRaisesRegex(AttributeError, "cannot be deleted$"):
                del builder._items
            with self.assertRaises(TypeError):
                vars(builder)
            with self.assertRaises(TypeError):
                hash(builder)
        self.assertEqual(stored(vector_build(fill)), ())

    def test_nested_mutables_subclasses_and_foreign_data_refuse_no_hooks(self):
        class IntChild(int):
            pass
        class TupleChild(tuple):
            def __iter__(self):
                Hooks.calls.append("subclass iteration")
                raise AssertionError()
        for bad in ([], {}, set(), bytearray(b"x"), iter((3,)), lambda: 3, Hooks(), Foreign(),
                    IntChild(3), TupleChild((3,))):
            held = []
            def fill(builder):
                held.append(builder)
                builder.append((Vector.of(3), bad))
            with self.assertRaisesRegex(TypeError, r"^append.value\[1\]"):
                vector_build(fill)
            self.expired(held[0])
        self.assertEqual(Hooks.calls, [])

    def test_live_ownership_callable_and_codec_exclusion(self):
        def fill(builder):
            for bad in (builder, builder.append, lambda: 3):
                with self.assertRaises(TypeError):
                    builder.append((bad,))
            with self.assertRaises(TypeError):
                value_encode(builder, VectorBuilder[int])
            builder.append(3)
        self.assertEqual(stored(vector_build(fill)), (3,))

    def test_extend_exactness_and_no_partial_mutation(self):
        forged = object.__new__(Vector)
        object.__setattr__(forged, "_items", (7, (Hooks(),)))
        def fill(builder):
            builder.append(3)
            for bad in (Hooks(), (5,), [5], forged):
                with self.assertRaises(TypeError):
                    builder.extend(bad)
                self.assertEqual(object.__getattribute__(builder, "_items"), [3])
            builder.append(11)
        self.assertEqual(stored(vector_build(fill)), (3, 11))
        self.assertEqual(Hooks.calls, [])

    def test_cyclic_and_malformed_product_storage_refuse(self):
        missing = object.__new__(Vector)
        cycle = object.__new__(Vector)
        object.__setattr__(cycle, "_items", (cycle,))
        for bad in (missing, cycle):
            def fill(builder):
                builder.append(bad)
            with self.assertRaises(TypeError):
                vector_build(fill)

    def test_canonical_nested_error_selection(self):
        messages = []
        for pairs in ((("b", (Hooks(),)), ("a", (Hooks(),))), (("a", (Hooks(),)), ("b", (Hooks(),)))):
            forged = object.__new__(Map)
            object.__setattr__(forged, "_entries", pairs)
            with self.assertRaises(TypeError) as caught:
                vector_build(lambda builder: builder.append(forged))
            messages.append(str(caught.exception))
        self.assertEqual(messages, ["append.value.entries['a'].value[0]: expected exact recursively immutable data"] * 2)
        self.assertEqual(Hooks.calls, [])

    def test_invalid_receiver_token_and_storage_refuse(self):
        with self.assertRaisesRegex(TypeError, "^builder: expected exact VectorBuilder$"):
            VectorBuilder.append(Hooks(), 3)
        forged = object.__new__(VectorBuilder)
        with self.assertRaisesRegex(TypeError, "^builder: malformed construction token$"):
            forged.append(3)
        for active, owner, busy in ((1, _thread.get_ident(), False), (True, True, False), (True, _thread.get_ident(), 0)):
            object.__setattr__(forged, "_active", active)
            object.__setattr__(forged, "_owner", owner)
            object.__setattr__(forged, "_busy", busy)
            with self.assertRaisesRegex(TypeError, "^builder: malformed construction token$"):
                forged.append(3)
        object.__setattr__(forged, "_active", True)
        object.__setattr__(forged, "_owner", _thread.get_ident())
        object.__setattr__(forged, "_busy", False)
        for storage in (None, (), Hooks()):
            object.__setattr__(forged, "_items", storage)
            with self.assertRaisesRegex(TypeError, "^builder: malformed construction storage$"):
                forged.append(3)
        self.assertEqual(Hooks.calls, [])

    def test_wrong_thread_refuses_before_validation_owner_can_continue(self):
        errors, live_threads = [], []
        original = collection_runtime._validate
        validations = []
        def validation(value, path="value", active=None):
            validations.append(path)
            return original(value, path, active)
        def fill(builder):
            def worker():
                for call in (lambda: builder.append(Hooks()), lambda: builder.extend(Hooks())):
                    try:
                        call()
                    except RuntimeError as error:
                        errors.append(str(error))
            thread = threading.Thread(target=worker)
            live_threads.append(thread)
            thread.start()
            thread.join(5)
            self.assertFalse(thread.is_alive(), "bounded worker did not join")
            self.assertEqual(validations, [])
            builder.append(37)
        try:
            collection_runtime._validate = validation
            result = vector_build(fill)
        finally:
            collection_runtime._validate = original
            for thread in live_threads:
                thread.join(5)
        self.assertEqual(errors, ["builder: construction belongs to its creating thread"] * 2)
        self.assertEqual(stored(result), (37,))
        self.assertEqual(Hooks.calls, [])

    def test_busy_guard_in_explicit_validator_seam_and_restoration(self):
        original = collection_runtime._validate
        held, messages = [], []
        def validation(value, path="value", active=None):
            if path == "append.value":
                for call in (lambda: held[0].append(53), lambda: held[0].extend(Vector.of(53))):
                    try:
                        call()
                    except RuntimeError as error:
                        messages.append(str(error))
            return original(value, path, active)
        def fill(builder):
            held.append(builder)
            builder.append(59)
        try:
            collection_runtime._validate = validation
            result = vector_build(fill)
        finally:
            collection_runtime._validate = original
        self.assertEqual(stored(result), (59,))
        self.assertEqual(messages, ["builder: operation is already active"] * 2)
        self.assertIs(collection_runtime._validate, original)
        self.expired(held[0])

    def test_final_validation_failure_revokes_before_publication(self):
        original = collection_runtime._validate
        held = []
        error = ValueError("fixed-finalization-failure")
        def validation(value, path="value", active=None):
            if path == "result":
                with self.assertRaises(RuntimeError):
                    held[0].append(67)
                raise error
            return original(value, path, active)
        def fill(builder):
            held.append(builder)
            builder.append(61)
        try:
            collection_runtime._validate = validation
            with self.assertRaises(ValueError) as caught:
                vector_build(fill)
        finally:
            collection_runtime._validate = original
        self.assertIs(caught.exception, error)
        self.expired(held[0])

    def test_final_validation_refuses_private_injected_mutable_contents(self):
        held = []
        def fill(builder):
            held.append(builder)
            builder.append(3)
            object.__getattribute__(builder, "_items").append([])
        with self.assertRaisesRegex(TypeError, r"^result\[1\]"):
            vector_build(fill)
        self.expired(held[0])

    def test_recursive_validation_failure_revokes(self):
        deep = 3
        for _ in range(2000):
            deep = (deep,)
        held = []
        def fill(builder):
            held.append(builder)
            builder.append(deep)
        with self.assertRaises(RecursionError):
            vector_build(fill)
        self.expired(held[0])

    def test_ordinary_repeated_and_nested_calls_get_fresh_tokens(self):
        builders = []
        def fill(builder):
            builders.append(builder)
            builder.append(41)
        first, second = vector_build(fill), vector_build(fill)
        self.assertIsNot(first, second)
        self.assertIsNot(builders[0], builders[1])
        self.assertEqual(stored(first), (41,))
        self.assertEqual(stored(second), (41,))
        def outer(builder):
            builder.append(vector_build(lambda inner: inner.append(43)))
        self.assertEqual(stored(stored(vector_build(outer))[0]), (43,))
        for builder in builders:
            self.expired(builder)

    def test_catalog_three_defining_rows_and_finite_aliases(self):
        self.assertEqual(BUILDER_VERSION, "pyalamode.builders-v1")
        self.assertEqual(BUILDERS_NAMES, frozenset({"vector_build", "VectorBuilder"}))
        rows = operation_catalog()
        names = ("vector_build", "VectorBuilder.append", "VectorBuilder.extend")
        self.assertEqual([row["identity"] for row in rows], ["pyalamode.builders." + name for name in names])
        for name, row in zip(names, rows):
            for alias in (name, "builders." + name, "pyalamode.builders." + name):
                self.assertEqual(operation_contract(alias), row)
            self.assertEqual(row["effects"], [])
            self.assertEqual(row["version"], BUILDER_VERSION)
        for unknown in (Hooks(), Foreign(), "VectorBuilder", "pyalamode.vector_build", "append", "builders.unknown"):
            self.assertIsNone(operation_contract(unknown))
        json.dumps(rows, allow_nan=False)
        self.assertEqual(Hooks.calls, [])

    def test_catalog_rows_are_detached_and_native_thread_closure_visible(self):
        row = operation_contract("vector_build")
        row["effects"].append("State")
        row["callback"]["effects"].append("IO")
        row["initialization"]["effects"].append("Environment")
        self.assertEqual(operation_contract("vector_build")["effects"], [])
        self.assertEqual(operation_contract("vector_build")["callback"]["effects"], [])
        self.assertEqual(operation_contract("vector_build")["initialization"]["effects"], [])
        self.assertEqual(BUILDERS_FOUNDATIONS["_thread"], frozenset({"get_ident"}))
        self.assertIn("types.FunctionType exact callback admission", operation_contract("vector_build")["foundations"])


if __name__ == "__main__":
    unittest.main()
