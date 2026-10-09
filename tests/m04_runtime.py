"""Adversarial ordinary-runtime records, snapshots and exact data guards."""

from __future__ import annotations

import collections
import dataclasses
import unittest
from types import FunctionType

from pyalamode.collections import Vector, Map, OrderedMap, Set
from pyalamode.records import record, replace
from pyalamode.boundaries import freeze, thaw, validate_data, dataclass_adapter, namedtuple_adapter
from pyalamode import boundaries


@record
class Customer:
    name: str
    tags: Vector[str]
    enabled: bool = True


@record
class Batch:
    customer: Customer
    counts: tuple[int, ...]


@record
class NumberPair:
    a: int
    b: int


class Hooks:
    calls = []

    def __iter__(self):
        self.calls.append("iter")
        return iter(())

    def __hash__(self):
        self.calls.append("hash")
        return 9

    def __eq__(self, other):
        self.calls.append("eq")
        return False

    def __repr__(self):
        self.calls.append("repr")
        return "foreign"


class HookMeta(type):
    def __hash__(self):
        Hooks.calls.append("metahash")
        return 7

    def __eq__(self, other):
        Hooks.calls.append("metaeq")
        return False

    def __getattribute__(self, name):
        Hooks.calls.append("metaget")
        return super().__getattribute__(name)


class Foreign(metaclass=HookMeta):
    pass


class StringHooks(str):
    def __hash__(self):
        Hooks.calls.append("stringhash")
        return str.__hash__(self)

    def __eq__(self, other):
        Hooks.calls.append("stringeq")
        return str.__eq__(self, other)


class M04Runtime(unittest.TestCase):
    def setUp(self):
        Hooks.calls.clear()

    def customer(self):
        return Customer("Ada", Vector.of("one"))

    def test_record_fixed_fields_defaults_equality_repr(self):
        first = self.customer()
        self.assertEqual(first.name, "Ada")
        self.assertTrue(first.enabled)
        self.assertEqual(first, Customer(tags=Vector.of("one"), name="Ada"))
        self.assertEqual(repr(first), "Customer(name='Ada', tags=Vector.of('one'), enabled=True)")
        self.assertFalse(first == Hooks())
        self.assertFalse(first == Foreign())
        self.assertEqual(Hooks.calls, [])

    def test_record_deep_exact_fields_and_nested_paths(self):
        for args in [("Ada", ["one"]), ("Ada", Vector.of(1)), ("Ada", Vector.of("one"), 1)]:
            with self.assertRaises(TypeError) as caught:
                Customer(*args)
            self.assertIn("record.", str(caught.exception))
        with self.assertRaises(TypeError) as caught:
            Batch(self.customer(), (True,))
        self.assertIn("counts[0]", str(caught.exception))
        self.assertEqual(Batch(self.customer(), (1, 2)).counts, (1, 2))

    def test_record_mutation_reinitialization_subclassing_and_hash_blocked(self):
        value = self.customer()
        for operation in [lambda: setattr(value, "name", "Grace"), lambda: delattr(value, "name"),
                          lambda: setattr(value, "extra", 1), lambda: value.__init__("x", Vector.of()), lambda: hash(value)]:
            with self.assertRaises((AttributeError, TypeError)):
                operation()
        with self.assertRaises(TypeError):
            type("Child", (Customer,), {})
        self.assertFalse(hasattr(value, "__dict__"))

    def test_zero_field_record_reinitialization_and_malformed_storage(self):
        @record
        class Empty:
            pass
        value = Empty()
        with self.assertRaises(AttributeError):
            value.__init__()
        with self.assertRaises(TypeError):
            freeze(object.__new__(Empty))

    def test_replace_preserves_prior_versions_and_exact_schema(self):
        first = self.customer()
        second = replace(first, tags=first.tags.appended("two"))
        self.assertIs(type(second), Customer)
        self.assertEqual(first.tags, Vector.of("one"))
        self.assertEqual(second.tags, Vector.of("one", "two"))
        self.assertIsNot(first, replace(first))
        for operation in [lambda: replace(first, missing=1), lambda: replace(first, tags=Vector.of(1)), lambda: replace(Hooks(), name="x")]:
            with self.assertRaises(TypeError):
                operation()
        self.assertEqual(Hooks.calls, [])

    def test_record_typed_equality_inside_collections(self):
        @record
        class Flag:
            value: bool
        @record
        class Count:
            value: int
        self.assertNotEqual(Flag(True), Count(1))
        self.assertEqual(Vector.of(self.customer()), Vector.of(self.customer()))
        self.assertEqual(Map.of(("c", self.customer())), Map.of(("c", self.customer())))
        self.assertIn("Customer(", repr(Vector.of(self.customer())))

    def test_record_rejects_declaration_behavior_and_reserved_fields(self):
        for namespace in [{"__annotations__": {"_storage": int}}, {"__annotations__": {"__dict__": int}},
                          {"__annotations__": {"x": int}, "__init__": lambda self: None},
                          {"__annotations__": {"x": int}, "x": property(lambda self: 1)},
                          {"__annotations__": {"x": int}, "method": lambda self: 1},
                          {"__annotations__": {"x": int}, "__dict__": property(lambda self: {})}]:
            namespace["__module__"] = __name__
            with self.assertRaises(TypeError):
                record(type("Bad", (), namespace))
        with self.assertRaises(TypeError):
            record(Foreign)
        with self.assertRaises(TypeError):
            record(type("Derived", (Foreign,), {"__annotations__": {"x": int}}))
        self.assertEqual(Hooks.calls, [])

    def test_record_rejects_unsupported_defaults_and_annotation_calls(self):
        for annotation, default in [(int, True), (Vector[int], Vector.of(True)), (int, Hooks()),
                                    ("Hooks()", 1), ("__import__('os').getcwd()", 1), (list[int], [])]:
            namespace = {"__module__": __name__, "__annotations__": {"x": annotation}, "x": default}
            with self.assertRaises(TypeError):
                record(type("Bad", (), namespace))
        self.assertEqual(Hooks.calls, [])

    def test_record_metadata_exactness_before_hash_or_namespace_access(self):
        for metadata in [Hooks(), StringHooks(__name__)]:
            declaration = type("Bad", (), {"__module__": metadata, "__annotations__": {"x": int}})
            Hooks.calls.clear()
            with self.assertRaises(TypeError):
                record(declaration)
            self.assertEqual(Hooks.calls, [])
        key = StringHooks("x")
        annotations = {key: int}
        declaration = type("Bad", (), {"__module__": __name__, "__annotations__": annotations})
        Hooks.calls.clear()
        with self.assertRaises(TypeError):
            record(declaration)
        self.assertEqual(Hooks.calls, [])

    def test_constructor_and_replace_reject_string_subclass_keyword_keys(self):
        kwargs = {StringHooks("name"): "Ada", "tags": Vector.of()}
        changes = {StringHooks("name"): "Grace"}
        class Plain:
            def __init__(self, /, *args, **kwargs):
                pass
        def plain_replace(value, /, **changes):
            pass
        # CPython binds **kwargs before entering a function and itself consults
        # str-subclass keys. The validator must add no foreign calls afterward.
        Hooks.calls.clear()
        Plain(**kwargs)
        plain_replace(self.customer(), **changes)
        binding_calls = list(Hooks.calls)
        Hooks.calls.clear()
        with self.assertRaises(TypeError):
            Customer(**kwargs)
        with self.assertRaises(TypeError):
            replace(self.customer(), **changes)
        self.assertEqual(Hooks.calls, binding_calls)

    def test_public_self_and_value_fields_do_not_collide_with_api_parameters(self):
        @record
        class PublicNames:
            self: int
            value: int
        value = PublicNames(self=1, value=2)
        self.assertEqual(value.self, 1)
        self.assertEqual(replace(value, self=3, value=4), PublicNames(3, 4))
        self.assertEqual(value.value, 2)

    def test_freeze_nested_alias_isolation_and_dictionary_order(self):
        shared = [1, {"inner": [2]}]
        source = {"b": shared, "a": shared}
        result = freeze(source, exclusive=True)
        self.assertEqual(result.keys(), Vector.of("b", "a"))
        source["c"] = 4
        shared[0] = 9
        shared[1]["inner"].append(3)
        expected = Vector.of(1, OrderedMap.of(("inner", Vector.of(2))))
        self.assertEqual(result["a"], expected)
        self.assertEqual(result["b"], expected)
        self.assertIsNot(result["a"], result["b"])

    def test_freeze_tuple_and_stable_reuse_without_mutable_precondition(self):
        for value in [None, True, 1, "a", b"a", self.customer(), Vector.of(self.customer())]:
            self.assertIs(freeze(value), value)
        self.assertEqual(freeze((1, [2]), exclusive=True), (1, Vector.of(2)))
        self.assertEqual(freeze((1, (2,))), (1, (2,)))
        with self.assertRaises(TypeError) as caught:
            freeze((1, [2]))
        self.assertIn("value[1]", str(caught.exception))

    def test_missing_or_nonexact_exclusive_assertion_fails(self):
        for value in [[1], {"a": 1}, {1}]:
            for exclusive in [False, 1, Hooks()]:
                with self.assertRaises(TypeError):
                    freeze(value, exclusive=exclusive)
        self.assertEqual(Hooks.calls, [])

    def test_freeze_cycles_report_nested_path_and_shared_acyclic_is_allowed(self):
        value = []
        value.append(value)
        with self.assertRaises(TypeError) as caught:
            freeze(value, exclusive=True)
        self.assertIn("value[0]", str(caught.exception))
        dictionary = {}
        dictionary["self"] = dictionary
        with self.assertRaises(TypeError) as caught:
            freeze(dictionary, exclusive=True)
        self.assertIn("entries['self']", str(caught.exception))
        shared = [1]
        self.assertEqual(freeze([shared, shared], exclusive=True), Vector.of(Vector.of(1), Vector.of(1)))

    def test_freeze_foreign_values_subclasses_views_no_hooks(self):
        class ListSubclass(list):
            def __iter__(self):
                Hooks.calls.append("subiter")
                return super().__iter__()
        dictionary = {"a": 1}
        for value in [Hooks(), Foreign(), ListSubclass([1]), dictionary.keys(), dictionary.values(), dictionary.items(), iter((1,))]:
            with self.assertRaises(TypeError):
                freeze(value, exclusive=True)
        self.assertEqual(Hooks.calls, [])

    def test_freeze_key_and_set_domains_reject_hooks_and_bool_int_mix(self):
        foreign_key = Hooks()
        source = {foreign_key: 1}
        foreign_set = {foreign_key}
        Hooks.calls.clear()
        for value in [source, foreign_set, {(1, 2)}, {1, "a"}, {False, "a"}]:
            with self.assertRaises(TypeError):
                freeze(value, exclusive=True)
        self.assertEqual(Hooks.calls, [])
        self.assertEqual(freeze(frozenset({3, 1})), Set.of(1, 3))

    def test_freeze_schema_validates_parameterized_data_after_conversion(self):
        self.assertEqual(freeze([1, 2], exclusive=True, schema=Vector[int]), Vector.of(1, 2))
        self.assertEqual(freeze(self.customer(), schema=Customer), self.customer())
        for value, schema in [([True], Vector[int]), ({"a": [True]}, OrderedMap[str, Vector[int]])]:
            with self.assertRaises(TypeError):
                freeze(value, exclusive=True, schema=schema)

    def test_thaw_all_container_occurrences_are_fresh_mutable_exports(self):
        shared = Vector.of(1)
        source = Vector.of(shared, shared, (shared,), Map.of(("a", shared)), Set.of(1, 2))
        output = thaw(source)
        self.assertIsInstance(output, list)
        self.assertIsInstance(output[2], list)
        self.assertIsInstance(output[3], dict)
        self.assertIsInstance(output[4], set)
        output[0].append(9)
        output[2][0][0] = 7
        output[3]["a"].clear()
        output[4].add(3)
        self.assertEqual(output[1], [1])
        self.assertEqual(source[0], Vector.of(1))
        self.assertEqual(source[3]["a"], Vector.of(1))
        self.assertEqual(source[4], Set.of(1, 2))
        self.assertIsNot(output, thaw(source))

    def test_thaw_records_export_independent_field_dictionary(self):
        source = Batch(self.customer(), (1, 2))
        first, second = thaw(source), thaw(source)
        first["customer"]["tags"].append("two")
        first["counts"][0] = 8
        self.assertEqual(second["customer"]["tags"], ["one"])
        self.assertEqual(source.customer.tags, Vector.of("one"))
        self.assertEqual(source.counts, (1, 2))

    def test_dataclass_adapter_concrete_target_and_alias_isolation(self):
        @dataclasses.dataclass(frozen=True)
        class Source:
            name: str
            tags: object
            enabled: bool = True
        adapter = dataclass_adapter(Source, Customer)
        tags = ["one"]
        source = Source("Ada", tags)
        with self.assertRaises(TypeError):
            freeze(source, adapter=adapter)
        result = freeze(source, adapter=adapter, exclusive=True, schema=Customer)
        self.assertIs(type(result), Customer)
        tags.append("two")
        self.assertEqual(result.tags, Vector.of("one"))
        with self.assertRaises(AttributeError):
            adapter._target = NumberPair

    def test_mutable_standard_dataclass_adapter_is_also_explicit_snapshot(self):
        @dataclasses.dataclass
        class Source:
            a: int
            b: int
        adapter = dataclass_adapter(Source, NumberPair)
        source = Source(1, 2)
        result = freeze(source, adapter=adapter, exclusive=True)
        source.a = 8
        self.assertEqual(result, NumberPair(1, 2))

    def test_namedtuple_adapter_concrete_target_and_getter_replacement_rejected(self):
        Source = collections.namedtuple("Source", "a b")
        adapter = namedtuple_adapter(Source, NumberPair)
        result = freeze(Source(1, 2), adapter=adapter, exclusive=True)
        self.assertIs(type(result), NumberPair)
        self.assertEqual(result, NumberPair(1, 2))
        Source.b = Source.a
        with self.assertRaises(TypeError):
            namedtuple_adapter(Source, NumberPair)

    def test_adapter_custom_methods_ctors_descriptors_factories_subclasses_fail(self):
        @dataclasses.dataclass
        class MethodSource:
            a: int
            b: int
            def method(self):
                return 1
        @dataclasses.dataclass
        class FactorySource:
            a: int
            b: object = dataclasses.field(default_factory=list)
        @dataclasses.dataclass(init=False)
        class ConstructorSource:
            a: int
            b: int
            def __init__(self):
                Hooks.calls.append("ctor")
        Source = collections.namedtuple("Source", "a b")
        class Derived(Source):
            pass
        for value, adapter_function in [(MethodSource, dataclass_adapter), (FactorySource, dataclass_adapter),
                                        (ConstructorSource, dataclass_adapter), (Derived, namedtuple_adapter),
                                        (Foreign, dataclass_adapter)]:
            with self.assertRaises(TypeError):
                adapter_function(value, NumberPair)
        self.assertEqual(Hooks.calls, [])

    def test_adapter_replaced_generated_defaults_globals_closures_fail(self):
        @dataclasses.dataclass
        class Data:
            a: int = 1
            b: int = 2
        Data.__init__.__defaults__ = (3, 4)
        with self.assertRaises(TypeError):
            dataclass_adapter(Data, NumberPair)
        Source = collections.namedtuple("Source", "a b")
        Source.__new__.__globals__["_tuple_new"] = lambda cls, args: tuple.__new__(cls, (5, 6))
        with self.assertRaises(TypeError):
            namedtuple_adapter(Source, NumberPair)

    def test_adapter_foreign_generated_namespace_keys_fail_before_lookup_hooks(self):
        Source = collections.namedtuple("Source", "a b")
        namespace = dict(Source.__new__.__globals__)
        constructor = namespace.pop("_tuple_new")
        namespace[StringHooks("_tuple_new")] = constructor
        Source.__new__ = staticmethod(FunctionType(Source.__new__.__code__, namespace))
        Hooks.calls.clear()
        with self.assertRaises(TypeError):
            namedtuple_adapter(Source, NumberPair)
        self.assertEqual(Hooks.calls, [])

    def test_adapters_reject_unknown_target_arbitrary_objects_and_invalid_values(self):
        Source = collections.namedtuple("Source", "a b")
        for target in [object, Foreign, Hooks()]:
            with self.assertRaises(TypeError):
                namedtuple_adapter(Source, target)
        adapter = namedtuple_adapter(Source, NumberPair)
        for value in [Source(True, 2), Source(1, []), Hooks()]:
            with self.assertRaises(TypeError):
                freeze(value, adapter=adapter, exclusive=True)
        self.assertEqual(Hooks.calls, [])
        with self.assertRaises(TypeError):
            freeze(Source(1, 2), adapter=object.__new__(boundaries._SnapshotAdapter), exclusive=True)

    def test_guard_full_recursive_exact_schema_and_typed_record(self):
        schema = ("OrderedMap", ("str", ("Vector", (("tuple", ("int", "bool"), False),))))
        good = OrderedMap.of(("a", Vector.of((1, True))))
        self.assertIs(validate_data(good, schema), good)
        with self.assertRaises(TypeError) as caught:
            validate_data(OrderedMap.of(("a", Vector.of((True, True)))), schema, path="entry.payload")
        self.assertIn("entry.payload.entries['a'].value[0][0]", str(caught.exception))
        record_schema = ("record", Customer, (("name", "str"), ("tags", ("Vector", ("str",))), ("enabled", "bool")))
        self.assertIs(validate_data(self.customer(), record_schema).enabled, True)

    def test_guard_rejects_erased_wrong_generics_and_foreign_metaclasses(self):
        for value, schema in [(Vector[int].of(True), ("Vector", ("int",))), (Hooks(), "int"),
                              (Foreign(), ("Vector", ("int",))), ([1], ("Vector", ("int",)))]:
            with self.assertRaises(TypeError):
                validate_data(value, schema)
        self.assertEqual(Hooks.calls, [])

    def test_guard_schema_is_data_not_application_annotation_evaluation(self):
        for schema in [Hooks(), Foreign, "Hooks()", ("Callable", ("int",)),
                       ("record", Foreign, ()), ("Map", (("Vector", ("int",)), "int")),
                       ("tuple", ("int",), Hooks())]:
            with self.assertRaises(TypeError):
                validate_data(1, schema)
        self.assertEqual(Hooks.calls, [])

    def test_malformed_and_cyclic_private_storage_is_rejected_without_hooks(self):
        forged = object.__new__(Vector)
        object.__setattr__(forged, "_items", [Hooks()])
        for function in [freeze, thaw, lambda value: validate_data(value, ("Vector", ("int",)))]:
            with self.assertRaises(TypeError):
                function(forged)
        cyclic = object.__new__(Vector)
        object.__setattr__(cyclic, "_items", (cyclic,))
        with self.assertRaises(TypeError):
            freeze(cyclic)
        malformed = object.__new__(Customer)
        with self.assertRaises(TypeError):
            validate_data(malformed, ("record", Customer, (("name", "str"), ("tags", ("Vector", ("str",))), ("enabled", "bool"))))
        self.assertEqual(Hooks.calls, [])


if __name__ == "__main__":
    unittest.main()
