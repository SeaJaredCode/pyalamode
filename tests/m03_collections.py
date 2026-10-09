"""Static and build gates for the finite collection contracts, without source imports."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.checker import CALLABLE_FAILURES, COLLECTION_FOUNDATIONS, analyze_source
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths, check_paths


PREFIX = 'from pyalamode import fun, Vector, OrderedMap, Map, Set\nfrom typing import Callable\n'


class CollectionsStatic(unittest.TestCase):
    def good(self, text):
        result = analyze_source(text, 'sample.py')
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def bad(self, text, rule=None):
        result = analyze_source(text, 'sample.py')
        self.assertFalse(result.verified, text)
        if rule:
            self.assertIn(rule, {d.rule for d in result.diagnostics})
        return result

    def test_finite_annotations_and_constructors(self):
        for kind, expression in [('Vector[int]', 'Vector.of(1, 2)'), ('Vector[Vector[int]]', 'Vector.of(Vector.of(1))'),
                                 ('OrderedMap[str, tuple[int, ...]]', 'OrderedMap.of(("a", (1, 2)))'),
                                 ('Map[str, Vector[int]]', 'Map.of(("a", Vector.of(1)))'), ('Set[bytes]', 'Set.of(b"a", b"b")')]:
            with self.subTest(kind=kind):
                self.good(PREFIX + f'@fun\ndef f() -> {kind}:return {expression}\n')
                self.good(PREFIX + f'@fun\ndef f() -> {kind}:return {kind}.of()\n')
        for annotation in ['Vector', 'Vector[Any]', 'Vector[Callable[[int],int]]', 'Set[tuple[int]]',
                           'Map[Vector[int],int]', 'OrderedMap[int,Callable[[int],int]]', 'Map[int]', 'Set[int,str]']:
            with self.subTest(annotation=annotation):
                self.bad(PREFIX + f'@fun\ndef f(x: {annotation}) -> int:return 1\n', 'PAL130')

    def test_complete_constructor_schema_and_deep_mutability_rejected(self):
        for expression in ['Vector[int].of(True)', 'Vector.of(1, True)', 'Vector.of((1, [2]))',
                           'Vector[Vector[int]].of(Vector.of("x"))', 'Map[int,int].of((True,1))',
                           'Map.of((1,1),(True,2))', 'Map.of((1,[2]))', 'Set.of((1,2))', 'Vector.of()']:
            with self.subTest(expression=expression):
                self.bad(PREFIX + f'@fun\ndef f() -> int:\n    item = {expression}\n    return 1\n')

    def test_vector_representative_operations_and_callbacks(self):
        result = self.good(PREFIX + '''@fun
def plus(x: int) -> int:return x + 1
@fun
def positive(x: int) -> bool:return x > 0
@fun
def add(a: int, x: int) -> int:return a + x
@fun
def f(v: Vector[int]) -> int:
    a = v.appended(3)
    b = a.updated_at(-1, 4)
    c = b.concat(Vector.of(5))
    d = c[1:]
    e = d.map(plus).filter(positive)
    return e.fold(add, 0) + e[0] + len(e)
''')
        f = next(c for c in result.contracts if c.name == 'f')
        self.assertEqual(f.failures, ['IndexError', 'ValueError'])
        self.assertIn('Vector.map', f.operations)
        self.assertIn('sample.py::plus', f.dependencies)
        self.assertTrue(any('collections-v1' in trust for trust in f.trust))

    def test_maps_sets_traversal_and_membership(self):
        self.good(PREFIX + '''@fun
def f(m: Map[str,int], o: OrderedMap[str,int], s: Set[str]) -> int:
    a = m.updated("z", 3).without("a").merge(Map.of(("b", 2)))
    b = o.updated("z", 4).without("a").merge(OrderedMap.of(("c", 5)))
    c = s.added("z").without("a").union(Set.of("b")).intersection(Set.of("b", "z")).difference(Set.of("x"))
    return a.get("missing", 0) + a.ordered_values()[0] + b.values()[0] + len(a.ordered_entries()) + len(a.ordered_keys()) + len(b.entries()) + len(b.keys()) + len(c.ordered_values()) + (1 if "z" in a and "z" not in c else 0)
''')
        for receiver, operation in [('m', 'values()'), ('m', 'entries()'), ('m', 'map(cb)'), ('s', 'map(cb)'), ('s', 'fold(cb,0)')]:
            self.bad(PREFIX + f'@fun\ndef f(m: Map[int,int], s: Set[int], cb: Callable[[int],int]) -> int:\n    unknown = {receiver}.{operation}\n    return 1\n', 'PAL221')

    def test_tuple_entries_are_usable_under_bounded_contracts(self):
        self.good(PREFIX + '''@fun
def amount(pair: tuple[str,int]) -> int:return pair[1]
@fun
def f(m: Map[str,int]) -> Vector[int]:return m.ordered_entries().map(amount)
@fun
def g(t: tuple[int,...], i: int) -> tuple[int,...]:return t[i:]
@fun
def h(t: tuple[int,str]) -> tuple[str]:return t[1:]
''')
        for expression in ['t[True]', 't[i]', 't[i:]', 't[10]', 't[::0]']:
            self.bad(PREFIX + f'@fun\ndef f(t: tuple[int,str], i: int) -> int:\n    value = {expression}\n    return 1\n', 'PAL210')

    def test_exact_dispatch_rejects_bool_indexes_and_unknown_hooks(self):
        for expression in ['v[True]', 'v[False:]', 'v.updated_at(True,1)', 'v.appended(True)', 'v.concat(Set.of(1))',
                           'm.get(True,1)', 'm.updated(1,True)', 's.added(True)', 'True in s', 'v.__getitem__(0)',
                           'v.append(1)', 'iter(v)', 'hash(s)', 'str(m)', 'repr(s)', 'f"{m}"', 'v < v']:
            with self.subTest(expression=expression):
                self.bad(PREFIX + f'@fun\ndef f(v: Vector[int], m: Map[int,int], s: Set[int]) -> int:\n    item = {expression}\n    return 1\n')

    def test_deep_schema_equality_and_order_domain(self):
        self.good(PREFIX + '@fun\ndef f(v: Vector[int], m: Map[str,int], s: Set[bool], t: tuple[int,str]) -> bool:return v == v and m != m and s == s and t == t\n')
        self.bad(PREFIX + '@fun\ndef f(a: Vector[int], b: Vector[bool]) -> bool:return a == b\n', 'PAL210')
        self.bad(PREFIX + '@fun\ndef f(a: Map[int,int], b: OrderedMap[int,int]) -> bool:return a == b\n', 'PAL210')
        self.good(PREFIX + '@fun\ndef f(a: Vector[int]) -> bool:return a is None\n')

    def test_A13_unknown_effectful_callback_shapes_never_promoted(self):
        for method, signature in [('map', 'Callable[[int],int]'), ('filter', 'Callable[[int],bool]'), ('fold', 'Callable[[int,int],int]')]:
            suffix = ',0' if method == 'fold' else ''
            text = PREFIX + f'@fun\ndef apply(v: Vector[int], cb: {signature}) -> int:\n    result = v.{method}(cb{suffix})\n    return 1\n'
            self.good(text)
            self.bad(text + 'def unknown(x):return x\napply(Vector.of(1), unknown)\n', 'PAL221')
            self.bad(text + 'def effectful(x):\n    print(x)\n    return x\napply(Vector.of(1), effectful)\n', 'PAL221')
        for definition in ['def cb(x: int, *, y: int=0) -> int:return x', 'def cb(x: bool) -> int:return 1',
                           'def cb(x: int) -> bool:return True']:
            self.bad(PREFIX + '@fun\n' + definition + '\n@fun\ndef f(v: Vector[int]) -> Vector[int]:return v.map(cb)\n')

    def test_callbacks_preserve_capture_and_actual_failures(self):
        result = self.good(PREFIX + '''@fun
def f(v: Vector[int], source: Map[int,int]) -> Vector[int]:
    def lookup(key: int) -> int:return source[key]
    return v.map(lookup)
''')
        contracts = {c.name: c for c in result.contracts}
        self.assertEqual(contracts['f'].failures, ['KeyError'])
        self.assertEqual(contracts['f.lookup'].captures, {'source': 'Map[int, int]'})
        self.assertIn('sample.py::f.lookup', contracts['f'].dependencies)
        result = self.good(PREFIX + '@fun\ndef f(v: Vector[int], cb: Callable[[int],int]) -> Vector[int]:return v.map(cb)\n')
        self.assertEqual(set(result.contracts[0].failures), set(CALLABLE_FAILURES))

    def test_mixed_concrete_conditional_callback_failure_universe(self):
        result = self.good(PREFIX + '''@fun
def identity(x: int) -> int:return x
@fun
def f(flag: bool, cb: Callable[[int],int], x: int) -> int:
    selected = identity if flag else cb
    return selected(x)
''')
        self.assertEqual(set(result.contracts[-1].failures), set(CALLABLE_FAILURES))

    def test_recursive_library_validation_failure_bound_is_separate(self):
        result = self.good(PREFIX + '''@fun
def box(x: int) -> tuple[int]:return (x,)
@fun
def prepend(a: tuple[int,...], x: int) -> tuple[int,...]:return a
@fun
def nested(v: Vector[tuple[int]], m: Map[int,tuple[int]], x: tuple[int], source: Vector[int]) -> Vector[tuple[int]]:
    a = v.appended(x).updated_at(0,x).concat(v)
    b = m.updated(1,x).merge(m).get(1,x)
    equal = a == v
    mapped = source.map(box)
    folded = source.fold(prepend, (1,))
    return mapped
@fun
def scalar(v: Vector[int]) -> Vector[int]:return v.appended(1)
''')
        contracts = {c.name: c for c in result.contracts}
        self.assertIn('RecursionError', contracts['nested'].failures)
        self.assertEqual(contracts['scalar'].failures, [])
        self.assertEqual(contracts['box'].failures, [])

    def test_collection_operations_remain_unavailable_in_initializer_callbacks(self):
        self.good('# mode: fun\n' + PREFIX + 'V = Vector.of(1,2)\nM = Map.of(("a",V))\ndef f(v: Vector[int]=V) -> int:return len(v)\n')
        self.bad('# mode: fun\n' + PREFIX + 'def cb(x: int) -> int:return x\nV = Vector.of(1).map(cb)\n', 'PAL221')
        self.bad(PREFIX + '@fun\ndef cb(x: int) -> int:return x\n@fun\ndef f(v: Vector[int]=Vector.of(1).map(cb)) -> int:return len(v)\n', 'PAL221')

    def test_return_only_updates_diagnosed_from_resolved_receiver(self):
        for annotation, statement in [('Vector[int]', 'v.appended(1)'), ('Vector[int]', 'v.updated_at(0,1)'),
                                      ('Map[int,int]', 'v.updated(1,1)'), ('Map[int,int]', 'v.without(1)'),
                                      ('Set[int]', 'v.added(1)'), ('Set[int]', 'v.union(Set.of(1))')]:
            result = self.bad(PREFIX + f'@fun\ndef f(v: {annotation}) -> int:\n    {statement}\n    return 1\n', 'PAL250')
            ignored = next(d for d in result.diagnostics if d.rule == 'PAL250')
            self.assertEqual(ignored.origin, 'persistent return-only operation')
            self.assertIn('new collection', ignored.remediation)

    def test_namespace_identity_class_and_method_replacements(self):
        writers = ['Vector.appended = print', 'alias = Vector\nalias.of = print', 'Vector[int].of = print',
                   'Vector.of.__code__ = print', 'import pyalamode as p\np.Vector.appended = print',
                   'from pyalamode.collections import Vector as backend\nbackend.appended = print',
                   'import pyalamode.collections as backend\nbackend.Vector.appended = print',
                   'import pyalamode.collections as backend\nbackend._validate = print',
                   'import pyalamode.collections as backend\nbackend._Frozen.__eq__ = print',
                   'from pyalamode.collections import _MapBase as base\nbase.of = print']
        for writer in writers:
            with self.subTest(writer=writer):
                self.bad(PREFIX + '@fun\ndef f(v: Vector[int]) -> Vector[int]:return v.appended(1)\n' + writer + '\n')
        self.bad(PREFIX + 'def Vector():return 1\n@fun\ndef f() -> int:\n    v = Vector.of(1)\n    return 1\n')

    def test_actual_backend_foundation_writers_cannot_inject_dispatch(self):
        core = 'from pyalamode import Map,fun\n@fun\ndef f(key:int) -> Map[int,int]:return Map.of((key,1))\n'
        for module, names in COLLECTION_FOUNDATIONS.items():
            for name in names:
                with self.subTest(module=module, name=name):
                    self.bad(core + f'import {module} as foundation\nfoundation.{name} = print\n')
        for writer in ['import builtins as b\nalias=b\nalias.repr=print',
                       'import builtins as b\nb.__dict__["type"]=print',
                       'import builtins as b\nsetattr(b,"hex",print)',
                       'import builtins as b\ndef ordinary_writer():\n    b.repr=print']:
            self.bad(core + writer + '\n')
        self.good('from pyalamode import fun\nimport builtins\n@fun\ndef scalar(x:str) -> str:return x\nbuiltins.repr=print\n')


class CollectionsProject(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / 'core.py'
        self.source.write_text('# mode: fun\nfrom pyalamode import Vector\ndef revise(v: Vector[int]) -> Vector[int]:return v.appended(1)\n')

    def tearDown(self):
        self.temp.cleanup()

    def test_cache_runtime_bytes_and_class_replacement_context(self):
        cold = check_paths([self.source], root=self.root)
        self.assertEqual(cold.status, 0)
        self.assertTrue(check_paths([self.source], root=self.root).results[0].cache_hit)
        changed = {**foundation_identities(), 'collections.py': 'changed-runtime-bytes'}
        with patch('pyalamode.checker.foundation_identities', return_value=changed):
            self.assertFalse(check_paths([self.source], root=self.root).results[0].cache_hit)
        (self.root / 'writer.py').write_text('from pyalamode import Vector\nVector.appended = print\n')
        result = check_paths([self.root], root=self.root)
        self.assertEqual(result.status, 1)
        core = next(r for r in result.results if Path(r.path).name == 'core.py')
        self.assertFalse(core.cache_hit)

    def test_build_preserves_source_and_discloses_runtime_contract(self):
        output = self.root / 'artifact'
        result = build_paths([self.source], root=self.root, output=output)
        self.assertEqual(result.status, 0, [d.format() for r in result.results for d in r.diagnostics])
        self.assertEqual((output / 'core.py').read_bytes(), self.source.read_bytes())
        evidence = json.loads((output / 'pyalamode-evidence.json').read_text())
        self.assertIn('collections.py', evidence['product_artifacts'])
        self.assertIn('Vector.appended', evidence['files'][0]['contracts'][0]['operations'])

    def test_backend_namespace_writer_only_changes_invalidate_warm_evidence(self):
        for writer in ['import builtins\nbuiltins.repr=print\n', 'import builtins as b\na=b\na.hex=print\n',
                       'import builtins as b\ndef ordinary_writer():\n    b.repr=print\n',
                       'import types as t\nt.FunctionType=print\n']:
            with self.subTest(writer=writer), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'core.py').write_text('from pyalamode import Map,fun\n@fun\ndef f(key:int) -> Map[int,int]:return Map.of((key,1))\n')
                (root / 'scalar.py').write_text('from pyalamode import fun\n@fun\ndef identity(x:str) -> str:return x\n')
                self.assertEqual(check_paths([root], root=root).status, 0)
                self.assertTrue(all(r.cache_hit for r in check_paths([root], root=root).results))
                (root / 'writer.py').write_text(writer)
                cached = check_paths([root], root=root)
                fresh = check_paths([root], root=root, cache=False)
                self.assertEqual(cached.status, 1)
                self.assertEqual(fresh.status, 1)
                core = next(r for r in cached.results if Path(r.path).name == 'core.py')
                scalar = next(r for r in cached.results if Path(r.path).name == 'scalar.py')
                self.assertFalse(core.cache_hit)
                self.assertTrue(any('collection dependency' in identity for identity in core.binding_context))
                self.assertTrue(scalar.verified)
                self.assertTrue(scalar.cache_hit)

    def test_invalid_deep_value_stops_build_without_executing_hooks(self):
        sentinel = self.root / 'sentinel'
        self.source.write_text('from pathlib import Path\n' + PREFIX + f'Path({str(sentinel)!r}).write_text("executed")\n@fun\ndef f() -> Vector[int]:return Vector.of([1])\n')
        output = self.root / 'invalid'
        self.assertEqual(build_paths([self.source], root=self.root, output=output).status, 1)
        self.assertFalse(output.exists())
        self.assertFalse(sentinel.exists())


if __name__ == '__main__':
    unittest.main()
