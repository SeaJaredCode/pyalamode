import itertools
import random
import sys
import unittest
from types import GenericAlias

from pyalamode.collections import Vector, OrderedMap, Map, Set


class Hooks:
    calls = []

    def __getattribute__(self, name):
        if name != 'calls':
            Hooks.calls.append(('attribute', name))
        return object.__getattribute__(self, name)

    def __iter__(self):
        Hooks.calls.append('iteration')
        raise AssertionError('foreign iteration')

    def __repr__(self):
        Hooks.calls.append('representation')
        raise AssertionError('foreign representation')

    def __eq__(self, other):
        Hooks.calls.append('equality')
        raise AssertionError('foreign equality')

    def __hash__(self):
        Hooks.calls.append('hash')
        raise AssertionError('foreign hash')

    def __call__(self, *arguments):
        Hooks.calls.append('call')
        raise AssertionError('foreign call')


class HostileMeta(type):
    def __eq__(cls, other):
        Hooks.calls.append('metaclass equality')
        raise AssertionError('metaclass equality')

    def __getattribute__(cls, name):
        Hooks.calls.append(('metaclass attribute', name))
        return type.__getattribute__(cls, name)


class MetaForeign(metaclass=HostileMeta):
    pass


class RuntimeCollections(unittest.TestCase):
    def setUp(self):
        Hooks.calls.clear()

    def test_generic_alias_is_erased_without_weaker_value_invariants(self):
        self.assertIs(type(Vector[int]), GenericAlias)
        self.assertIs(type(Vector[int].of(1)), Vector)
        self.assertIs(type(Map[str, int].of(('a', 1))), Map)
        self.assertEqual(Vector[str].of(1), Vector.of(1))
        self.assertEqual(Map[str, int].of(('a', 'runtime schemas are erased')), Map.of(('a', 'runtime schemas are erased')))
        with self.assertRaises(TypeError):
            Vector[int].of([])

    def test_empty_constructors_and_no_arbitrary_iterable_constructors(self):
        for cls in [Vector, OrderedMap, Map, Set]:
            self.assertEqual(len(cls()), 0)
            self.assertEqual(cls(), cls.of())
            with self.assertRaises(TypeError):
                cls(Hooks())
        for cls in [OrderedMap, Map]:
            for pair in [[1, 2], (1,), (1, 2, 3), Hooks()]:
                with self.assertRaisesRegex(TypeError, 'pairs'):
                    cls.of(pair)
        self.assertEqual(Hooks.calls, [])

    def test_recursively_admitted_values_and_repeated_references(self):
        inner = Map.of(('x', Vector.of(1, (True, None, b'b'))))
        value = Vector.of((inner, inner), Set.of('a', 'b'), OrderedMap.of((1, (2, 3))))
        self.assertEqual(value[0][0], inner)
        self.assertEqual(value[0][1], inner)
        self.assertEqual(value[1], Set.of('b', 'a'))
        self.assertEqual(len(value), 3)

    def test_nested_mutability_subclasses_and_foreign_hooks_rejected(self):
        class IntChild(int):
            def __repr__(self):
                Hooks.calls.append('int repr')
                raise AssertionError()
        class TupleChild(tuple):
            def __iter__(self):
                Hooks.calls.append('tuple iteration')
                raise AssertionError()
        for bad in [[], {}, set(), bytearray(b'a'), iter((1,)), Hooks(), MetaForeign(), IntChild(1), TupleChild((1,)), lambda: 1]:
            for construct in [lambda v: Vector.of((1, (v,))), lambda v: Map.of(('a', (v,))), lambda v: OrderedMap.of(('a', v))]:
                with self.assertRaises(TypeError):
                    construct(bad)
            with self.assertRaises(TypeError):
                Set.of(bad)
        self.assertEqual(Hooks.calls, [])

    def test_stable_nested_path_and_no_foreign_repr(self):
        with self.assertRaisesRegex(TypeError, r'items\[0\]\[1\]\[0\]'):
            Vector.of((1, (Hooks(),)))
        with self.assertRaisesRegex(TypeError, r"entries\['a'\].value\[1\]"):
            Map.of(('a', (1, Hooks())))
        self.assertEqual(Hooks.calls, [])

    def test_large_integer_keys_do_not_add_decimal_formatting_failure(self):
        previous_limit = sys.get_int_max_str_digits()
        sys.set_int_max_str_digits(sys.int_info.default_max_str_digits)
        try:
            huge = 10 ** 5000
            with self.assertRaises(ValueError):
                repr(huge)
            for cls in [Map, OrderedMap]:
                original = cls.of((huge, 1), (-huge, 2))
                nested = Vector.of(cls[int, int].of().updated(huge, 3))
                self.assertEqual(original[huge], 1)
                self.assertEqual(original[-huge], 2)
                self.assertEqual(nested[0][huge], 3)
                merged = original.merge(cls.of((huge, 4)))
                self.assertEqual(merged[huge], 4)
                self.assertEqual(original[huge], 1)
                self.assertEqual(original.get(huge, nested), 1)
                self.assertIs(original.get(huge + 1, nested), nested)
                for key in [huge, -huge]:
                    with self.assertRaises(TypeError) as error:
                        cls.of((key, (1, Hooks())))
                    self.assertEqual(str(error.exception),
                                     "entries[" + hex(key) + "].value[1]: expected exact recursively immutable data")
                # Public representation retains ordinary Python formatting.
                with self.assertRaises(ValueError):
                    repr(original)
            self.assertEqual(Hooks.calls, [])
        finally:
            sys.set_int_max_str_digits(previous_limit)

    def test_cycle_and_malformed_forged_storage_rejected_without_hooks(self):
        forged = object.__new__(Vector)
        with self.assertRaisesRegex(TypeError, 'malformed'):
            Vector.of(forged)
        object.__setattr__(forged, '_items', (forged,))
        with self.assertRaisesRegex(TypeError, 'cyclic'):
            Vector.of(forged)
        object.__setattr__(forged, '_items', (Hooks(),))
        with self.assertRaises(TypeError):
            Vector.of(forged)
        self.assertEqual(Hooks.calls, [])

    def test_frozen_slots_final_classes_no_hash_or_mutable_export(self):
        for value in [Vector.of(1), OrderedMap.of((1, 2)), Map.of((1, 2)), Set.of(1)]:
            with self.assertRaises(AttributeError):
                value.extra = []
            with self.assertRaises(AttributeError):
                del value.extra
            with self.assertRaises(AttributeError):
                value.__init__()
            with self.assertRaises(TypeError):
                vars(value)
            with self.assertRaises(TypeError):
                hash(value)
            with self.assertRaises(TypeError):
                type('Child', (type(value),), {})
        self.assertEqual(Vector.of(1), Vector.of(1))

    def test_Vector_updates_and_retained_versions(self):
        original = Vector.of(1, 2, 3)
        appended = original.appended(4)
        revised = original.updated_at(-1, 9)
        combined = revised.concat(Vector.of(10, 11))
        self.assertEqual(original, Vector.of(1, 2, 3))
        self.assertEqual(appended, Vector.of(1, 2, 3, 4))
        self.assertEqual(revised, Vector.of(1, 2, 9))
        self.assertEqual(combined, Vector.of(1, 2, 9, 10, 11))
        with self.assertRaises(TypeError):
            original.appended([4])
        with self.assertRaises(TypeError):
            original.concat((4,))

    def test_Vector_exact_index_slice_and_failure_categories(self):
        value = Vector.of(0, 1, 2, 3)
        self.assertEqual(value[-1], 3)
        self.assertEqual(value[1:4:2], Vector.of(1, 3))
        self.assertEqual(value[::-1], Vector.of(3, 2, 1, 0))
        self.assertEqual(value[10:100], Vector.of())
        for index in [True, 1.0, Hooks()]:
            with self.assertRaises(TypeError):
                value[index]
            with self.assertRaises(TypeError):
                value.updated_at(index, 1)
        for index in [4, -5]:
            with self.assertRaises(IndexError):
                value[index]
            with self.assertRaises(IndexError):
                value.updated_at(index, 1)
        for index in [slice(True, None), slice(None, False), slice(None, None, True), slice(Hooks(), 2)]:
            with self.assertRaises(TypeError):
                value[index]
        with self.assertRaises(ValueError):
            value[::0]
        self.assertEqual(Hooks.calls, [])

    def test_eager_map_filter_fold_and_callback_order(self):
        value = Vector.of(1, 2, 3)
        visited = []
        def add(value):
            visited.append(value)
            return value + 1
        self.assertEqual(value.map(add), Vector.of(2, 3, 4))
        self.assertEqual(visited, [1, 2, 3])
        self.assertEqual(value.filter(lambda x: x != 2), Vector.of(1, 3))
        self.assertEqual(value.fold(lambda total, x: total + x, 0), 6)
        self.assertEqual(Vector.of().fold(lambda a, b: 0, 'initial'), 'initial')
        self.assertEqual(value, Vector.of(1, 2, 3))

    def test_runtime_callbacks_have_no_purity_registry_or_signature_introspection(self):
        effects = []
        def ordinary(value):
            effects.append(value)
            return value
        self.assertEqual(Vector.of(1).map(ordinary), Vector.of(1))
        self.assertEqual(effects, [1])
        for callback in [Hooks(), abs, ordinary.__call__]:
            for run in [lambda cb: Vector.of().map(cb), lambda cb: Vector.of().filter(cb), lambda cb: Vector.of().fold(cb, 0)]:
                with self.assertRaises(TypeError):
                    run(callback)
        self.assertEqual(Hooks.calls, [])
        with self.assertRaises(TypeError):
            Vector.of(1).map(lambda left, right: left + right)

    def test_callback_results_predicates_and_each_accumulator_validated(self):
        value = Vector.of(1, 2, 3)
        with self.assertRaisesRegex(TypeError, r'map.result\[0\]'):
            value.map(lambda x: (Hooks(),))
        with self.assertRaisesRegex(TypeError, r'filter.result\[0\]'):
            value.filter(lambda x: 1)
        with self.assertRaisesRegex(TypeError, r'fold.accumulator\[1\]'):
            value.fold(lambda a, x: [] if x == 2 else a + x, 0)
        with self.assertRaisesRegex(TypeError, 'initial'):
            Vector.of().fold(lambda a, x: a, [])
        self.assertEqual(Hooks.calls, [])
        with self.assertRaises(ZeroDivisionError):
            Vector.of(0).map(lambda x: 1 // x)

    def test_OrderedMap_duplicate_slots_merge_and_persistence(self):
        first = OrderedMap.of(('b', 2), ('a', 1), ('b', 3))
        revised = first.updated('a', 4).updated('c', 5)
        merged = first.merge(OrderedMap.of(('d', 6), ('b', 7)))
        self.assertEqual(first.entries(), Vector.of(('b', 3), ('a', 1)))
        self.assertEqual(revised.entries(), Vector.of(('b', 3), ('a', 4), ('c', 5)))
        self.assertEqual(merged.entries(), Vector.of(('b', 7), ('a', 1), ('d', 6)))
        self.assertEqual(first.keys(), Vector.of('b', 'a'))
        self.assertEqual(first.values(), Vector.of(3, 1))
        self.assertIs(first.without('missing'), first)
        self.assertEqual(first.without('b'), OrderedMap.of(('a', 1)))
        self.assertNotEqual(first, OrderedMap.of(('a', 1), ('b', 3)))

    def test_Map_extensional_equivalence_canonical_results_and_persistence(self):
        first = Map.of(('b', 2), ('a', 1), ('b', 3))
        second = Map.of(('a', 1), ('b', 3))
        self.assertEqual(first, second)
        self.assertEqual(first.ordered_entries(), Vector.of(('a', 1), ('b', 3)))
        self.assertEqual(first.ordered_keys(), Vector.of('a', 'b'))
        self.assertEqual(first.ordered_values(), Vector.of(1, 3))
        self.assertEqual(repr(first), repr(second))
        self.assertEqual(first.merge(Map.of(('b', 4), ('c', 5))), Map.of(('c', 5), ('a', 1), ('b', 4)))
        self.assertEqual(first, second)
        self.assertIs(first.without('missing'), first)
        self.assertEqual(first.updated('c', 5).without('a'), Map.of(('c', 5), ('b', 3)))

    def test_map_lookups_membership_defaults_and_exact_domains(self):
        for cls in [OrderedMap, Map]:
            value = cls.of((1, 'a'))
            self.assertEqual(value[1], 'a')
            self.assertTrue(value.contains(1))
            self.assertTrue(1 in value)
            self.assertFalse(2 in value)
            self.assertEqual(value.get(1, 'default'), 'a')
            self.assertEqual(value.get(2, 'default'), 'default')
            with self.assertRaises(KeyError):
                value[2]
            for operation in [lambda: value[True], lambda: value.contains(True), lambda: value.updated(True, 'b'), lambda: value.without(True), lambda: value.get(True, 'default')]:
                with self.assertRaises(TypeError):
                    operation()
            with self.assertRaises(TypeError):
                value.get(1, [])
            with self.assertRaises(TypeError):
                value.merge((Map if cls is OrderedMap else OrderedMap).of((1, 'a')))
            with self.assertRaises(TypeError):
                cls.of((True, 1), (1, 2))
            self.assertEqual(cls.of((None, 1), (None, 2))[None], 2)
            self.assertEqual(cls.of().updated(True, 1), cls.of((True, 1)))

    def test_exact_scalar_canonical_order_in_all_supported_domains(self):
        domains = [(None,), (True, False), (3, -2, 0), ('z', 'a', 'å'), (b'z', b'a', b'\x00')]
        for domain in domains:
            expected = tuple(domain) if domain == (None,) else tuple(sorted(domain))
            self.assertEqual(Set.of(*domain).ordered_values(), Vector.of(*expected))
            self.assertEqual(Map.of(*((key, 1) for key in domain)).ordered_keys(), Vector.of(*expected))
        for bad in [(True, 1), (1, 'a'), (None, False), ('a', b'a')]:
            with self.assertRaises(TypeError):
                Set.of(*bad)
            with self.assertRaises(TypeError):
                Map.of(*((key, 1) for key in bad))

    def test_unordered_values_block_iteration_including_sequence_fallback(self):
        for value in [Map.of((0, 'a'), (1, 'b')), Set.of(1, 2)]:
            with self.assertRaises(TypeError):
                iter(value)
            with self.assertRaises(TypeError):
                list(value)
            with self.assertRaises(TypeError):
                tuple(value)
        self.assertEqual(tuple(Vector.of(1, 2)), (1, 2))

    def test_Set_operations_membership_and_retention(self):
        first = Set.of(3, 1, 3)
        second = Set.of(2, 3)
        self.assertEqual(first, Set.of(1, 3))
        self.assertEqual(first.ordered_values(), Vector.of(1, 3))
        self.assertEqual(first.added(2), Set.of(1, 2, 3))
        self.assertEqual(first.without(3), Set.of(1))
        self.assertEqual(first.union(second), Set.of(1, 2, 3))
        self.assertEqual(first.intersection(second), Set.of(3))
        self.assertEqual(first.difference(second), Set.of(1))
        self.assertTrue(1 in first)
        self.assertFalse(2 in first)
        self.assertIs(first.added(1), first)
        self.assertIs(first.without(2), first)
        self.assertEqual(first, Set.of(1, 3))
        for operation in [lambda: first.added(True), lambda: first.without(True), lambda: first.contains(True), lambda: first.union(Set.of(True)), lambda: first.intersection(Vector.of(1))]:
            with self.assertRaises(TypeError):
                operation()

    def test_recursive_exact_typed_equality_and_foreign_false_without_hooks(self):
        for left, right in [(Vector.of(True), Vector.of(1)), (Vector.of((True,)), Vector.of((1,))), (Map.of(('a', True)), Map.of(('a', 1))), (OrderedMap.of(('a', Vector.of(True))), OrderedMap.of(('a', Vector.of(1)))), (Set.of(True), Set.of(1)), (Map.of((1, 2)), OrderedMap.of((1, 2)))]:
            self.assertFalse(left == right)
            self.assertTrue(left != right)
        for value in [Vector.of(1), Map.of((1, 2)), OrderedMap.of((1, 2)), Set.of(1)]:
            self.assertFalse(value == Hooks())
            self.assertFalse(value == MetaForeign())
        self.assertEqual(Hooks.calls, [])

    def test_map_constructor_nested_error_selection_uses_canonical_keys(self):
        errors = []
        for pairs in [[('b', (Hooks(),)), ('a', (Hooks(),))], [('a', (Hooks(),)), ('b', (Hooks(),))]]:
            with self.assertRaises(TypeError) as caught:
                Map.of(*pairs)
            errors.append(str(caught.exception))
        self.assertEqual(errors[0], errors[1])
        self.assertIn("entries['a'].value[0]", errors[0])
        self.assertEqual(Hooks.calls, [])

    def test_three_seed_histories_preserve_unordered_outputs_and_repr(self):
        expected_map = Map.of(*((key, (key,)) for key in range(15)))
        expected_set = Set.of(*range(15))
        for seed in [7, 19, 101]:
            keys = list(range(15))
            random.Random(seed).shuffle(keys)
            mapping, members = Map.of(), Set.of()
            versions = []
            for key in keys:
                versions.append((mapping, members, len(mapping)))
                mapping = mapping.updated(key, (key,))
                members = members.added(key)
            self.assertEqual(mapping, expected_map)
            self.assertEqual(members, expected_set)
            self.assertEqual(mapping.ordered_entries(), expected_map.ordered_entries())
            self.assertEqual(members.ordered_values(), expected_set.ordered_values())
            self.assertEqual(repr(mapping), repr(expected_map))
            self.assertEqual(repr(members), repr(expected_set))
            for old_map, old_set, size in versions:
                self.assertEqual(len(old_map), size)
                self.assertEqual(len(old_set), size)

    def test_set_binary_algorithms_match_exact_scalar_reference(self):
        for left in [(), (1,), (1, 3), (1, 2, 4)]:
            for right in [(), (2,), (1, 4), (0, 1, 2, 3)]:
                a, b = Set.of(*left), Set.of(*right)
                self.assertEqual(a.union(b), Set.of(*sorted(set(left) | set(right))))
                self.assertEqual(a.intersection(b), Set.of(*sorted(set(left) & set(right))))
                self.assertEqual(a.difference(b), Set.of(*sorted(set(left) - set(right))))

    def test_ordinary_three_domain_permutations_are_extensional(self):
        for values in [(False, True), (None,), ('a', 'b', 'c')]:
            first_set, first_map = Set.of(*values), Map.of(*((key, 1) for key in values))
            for permutation in itertools.permutations(values):
                self.assertEqual(Set.of(*permutation), first_set)
                self.assertEqual(Map.of(*((key, 1) for key in permutation)), first_map)
                self.assertEqual(repr(Set.of(*permutation)), repr(first_set))
                self.assertEqual(repr(Map.of(*((key, 1) for key in permutation))), repr(first_map))


if __name__ == '__main__':
    unittest.main()
