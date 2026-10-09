"""Sum-type stages 0-1: the @oneof spelling and closed unions discriminated by exact class."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pyalamode.checker import analyze_source
from pyalamode.project import check_paths, build_paths

IMPORTS = 'from pyalamode import fun, oneof, case, record, Option, Some, Nothing\n'
DECLARATIONS = '''@record
class Point:
    x: int
    y: int | None
@oneof
class Shape:
    @case
    class Circle:
        r: int
    @case
    class Dot:
        pass
'''
SCALAR = '''@fun
def describe(v: int | str | None) -> int:
    match v:
        case int(n): return n
        case str(): return 1
        case None: return 0
'''
MIXED = '''@fun
def area(v: Shape | Point | None) -> int:
    match v:
        case Shape.Circle(r): return r
        case Shape.Dot(): return 0
        case Point(x=x): return x
        case None: return -1
'''


class OneOf(unittest.TestCase):
    def test_variant_spelling_is_gone(self):
        import pyalamode
        self.assertIn('oneof', pyalamode.__all__)
        self.assertNotIn('variant', pyalamode.__all__)
        self.assertFalse(hasattr(pyalamode, 'variant'))
        result = analyze_source('from pyalamode import fun, case\nfrom pyalamode import variant\n@variant\nclass Lookup:\n    @case\n    class Found:\n        value: int\n@fun\ndef f(v: Lookup) -> int:\n    return 1\n', path='lookup.py')
        self.assertIn('PAL130', [d.rule for d in result.diagnostics])

    def test_checker_admits_oneof_and_module_attribute_spelling(self):
        for prefix, decorator in [(IMPORTS, '@oneof'), ('import pyalamode\nfrom pyalamode import fun, case\n', '@pyalamode.oneof')]:
            source = prefix + decorator + '\nclass Lookup:\n    @case\n    class Found:\n        value: int\n    @case\n    class Missing:\n        pass\n@fun\ndef f(v: Lookup) -> int:\n    match v:\n        case Lookup.Found(n): return n\n        case Lookup.Missing(): return 0\n'
            result = analyze_source(source, path='lookup.py')
            self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
            self.assertEqual(len(result.oneofs), 1)

    def test_rebound_oneof_is_not_a_domain_declaration(self):
        source = IMPORTS + 'oneof = record\n@oneof\nclass Lookup:\n    @case\n    class Found:\n        value: int\n'
        self.assertFalse(analyze_source(source, path='lookup.py').verified)

    def test_explain_topics(self):
        from pyalamode.cli import explain_symbol
        self.assertIn('@oneof', str(explain_symbol('oneof')))
        self.assertIn('bool | int', str(explain_symbol('union')))


class ClosedUnions(unittest.TestCase):
    def checked(self, source, **kwargs):
        result = analyze_source(IMPORTS + DECLARATIONS + source, path='unions.py', **kwargs)
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def rejected(self, source, rule=None, **kwargs):
        result = analyze_source(IMPORTS + DECLARATIONS + source, path='unions.py', **kwargs)
        self.assertFalse(result.verified, source)
        if rule:
            self.assertIn(rule, [d.rule for d in result.diagnostics], '\n'.join(d.format() for d in result.diagnostics))
        return result

    def test_scalar_record_domain_and_none_members_match_exhaustively(self):
        result = self.checked(SCALAR + MIXED)
        rows = {c.name: c for c in result.contracts}
        self.assertEqual(rows['describe'].parameters['v'], 'None | int | str')
        self.assertEqual(rows['describe'].patterns[0]['case_set'], ['None', 'int', 'str'])
        self.assertEqual(rows['area'].patterns[0]['case_set'],
                         ["Case['unions:Shape:Circle']", "Case['unions:Shape:Dot']", 'None', "Record['unions:Point']"])
        self.assertFalse(rows['area'].patterns[0]['wildcard'])

    def test_values_flow_into_and_out_of_unions(self):
        self.checked(SCALAR + '''@fun
def ret(flag: bool) -> int | None:
    if flag:
        return 1
    return None
@fun
def merged(flag: bool) -> int:
    x = 1 if flag else None
    match x:
        case int(n): return n
        case None: return 0
@fun
def reordered(v: int | None) -> None | int:
    return v
@fun
def widen(v: Shape.Circle | Shape.Dot) -> Shape:
    return v
@fun
def call() -> int:
    return describe(None) + describe(3) + describe("x")
@fun
def stored(v: int | None) -> Point:
    return Point(1, v)
@fun
def optional(v: Option[int | None]) -> int:
    match v:
        case Some(inner):
            match inner:
                case int(n): return n
                case None: return 0
        case Nothing(): return -1
@fun
def quoted(v: "bytes | None") -> int:
    match v:
        case bytes(): return 1
        case None: return 0
''')

    def test_boolean_members_use_singletons_or_bool_class(self):
        self.checked('@fun\ndef f(v: bool | str) -> int:\n    match v:\n        case True: return 1\n        case False: return 0\n        case str(): return 2\n')
        self.checked('@fun\ndef f(v: bool | None) -> int:\n    match v:\n        case bool(b): return 1\n        case None: return 0\n')
        self.rejected('@fun\ndef f(v: bool | None) -> int:\n    match v:\n        case True: return 1\n        case None: return 0\n', 'PAL330')

    def test_canonical_normalization(self):
        result = self.checked('@fun\ndef f(a: int | None, b: None | int, c: int | int, d: int | (str | None)) -> int:\n    return c\n')
        parameters = result.contracts[0].parameters
        self.assertEqual(parameters['a'], parameters['b'])
        self.assertEqual(parameters['c'], 'int')
        self.assertEqual(parameters['d'], 'None | int | str')

    def test_refused_members(self):
        for annotation in ['bool | int', 'Shape | Shape.Circle', 'int | list[int]', 'int | Option[int]', 'int | tuple[int]',
                           'int | float', 'Union[int, str]', 'Optional[int]']:
            with self.subTest(annotation=annotation):
                self.rejected('@fun\ndef f(v: ' + annotation + ') -> int:\n    return 1\n', 'PAL130')
        result = self.rejected('@fun\ndef f(v: bool | int) -> int:\n    return 1\n', 'PAL130')
        self.assertIn('bool | int', result.diagnostics[0].reason)
        self.rejected('@record\nclass Bad:\n    v: int | Shape.Dot | Shape.Dot | Shape\n', 'PAL130')

    def test_union_values_support_no_implicit_operations(self):
        self.rejected('@fun\ndef f(v: int | None) -> int:\n    return v + 1\n', 'PAL210')
        self.rejected('@fun\ndef f(v: int | None) -> int:\n    return v\n', 'PAL211')
        self.rejected('@fun\ndef g(n: int) -> int:\n    return n\n@fun\ndef f(v: int | str) -> int:\n    return g(v)\n', 'PAL221')
        self.checked('@fun\ndef f(v: Shape) -> Shape.Circle | Shape.Dot | None:\n    return v\n')

    def test_coverage_policy_guards_and_literals(self):
        self.rejected(SCALAR.replace('        case str(): return 1\n', ''), 'PAL330')
        self.rejected(MIXED.replace('        case Shape.Dot(): return 0\n', ''), 'PAL330')
        wildcard = '@fun\ndef f(v: Shape | None) -> int:\n    match v:\n        case None: return 0\n        case _: return 1\n'
        self.checked(wildcard)
        self.rejected(wildcard, 'PAL330', policy={'explicit_cases': ['unions:Shape']})
        self.checked(wildcard, policy={'explicit_cases': ['other:Shape']})
        for case in ['case int(0): return 0', 'case 0: return 0', 'case int() if False: return 0']:
            with self.subTest(case=case):
                self.rejected(SCALAR.replace('case int(n): return n', case), 'PAL330')
        self.checked(SCALAR.replace('case int(n): return n', 'case int() if True: return 0'))
        self.checked(SCALAR.replace('case int(n): return n', 'case 0: return 0\n        case int(n): return n'))

    def test_class_patterns_require_union_members(self):
        self.rejected(SCALAR.replace('case str(): return 1', 'case bytes(): return 1'), 'PAL330')
        self.rejected('@fun\ndef f(v: int | None) -> int:\n    match v:\n        case Point(): return 1\n        case _: return 0\n', 'PAL330')
        self.rejected('@fun\ndef f(v: int | None) -> int:\n    match v:\n        case int(x=n): return n\n        case _: return 0\n', 'PAL330')
        self.rejected('@fun\ndef f(v: int | None, int: int) -> int:\n    match v:\n        case int(): return 1\n        case None: return 0\n')
        self.rejected('int = str\n@fun\ndef f(v: str | None) -> int:\n    match v:\n        case int(): return 1\n        case None: return 0\n')

    def test_narrowing_inside_payload_does_not_exhaust_it(self):
        self.rejected('@fun\ndef f(p: Point) -> int:\n    match p:\n        case Point(y=None): return 0\n        case Point(y=int(n)): return n\n', 'PAL330')
        self.checked('@fun\ndef f(p: Point) -> int:\n    match p:\n        case Point(y=None): return 0\n        case _: return 1\n')
        self.checked('@fun\ndef f(p: Point) -> int:\n    match p:\n        case Point(y=y):\n            match y:\n                case int(n): return n\n                case None: return 0\n')


class UnionProjects(unittest.TestCase):
    def test_member_case_addition_invalidates_incomplete_union_consumers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'shapes.py').write_text('# mode: fun\n' + IMPORTS + DECLARATIONS)
            (root / 'consumer.py').write_text('# mode: fun\nfrom shapes import Shape, Point\n' + MIXED.replace('@fun\n', ''))
            (root / 'tolerant.py').write_text('# mode: fun\nfrom shapes import Shape\ndef f(v: Shape | None) -> int:\n    match v:\n        case None: return 0\n        case _: return 1\n')
            cold = check_paths([root / 'consumer.py', root / 'tolerant.py'], root=root)
            self.assertEqual(cold.status, 0)
            warm = check_paths([root / 'consumer.py', root / 'tolerant.py'], root=root)
            self.assertTrue(all(r.cache_hit for r in warm.results))
            def contracts(run):
                return {c.name + r.path: c.__dict__ for r in run.results for c in r.contracts}
            self.assertEqual(contracts(cold), contracts(warm))
            (root / 'shapes.py').write_text((root / 'shapes.py').read_text() + '    @case\n    class Square:\n        side: int\n')
            changed = check_paths([root / 'consumer.py', root / 'tolerant.py'], root=root)
            failing = {Path(r.path).name for r in changed.results if r.diagnostics}
            self.assertEqual(failing, {'consumer.py'})

    def test_build_off_exports_debug_real_runs(self):
        source = IMPORTS + DECLARATIONS + SCALAR + MIXED
        for mode in ['off', 'exports', 'debug']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / 'unions.py').write_text(source)
                if mode != 'off':
                    (root / 'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="' + mode + '"\nguarded_exports=["unions:describe", "unions:area"]\n')
                output = root / 'out'
                result = build_paths([root / 'unions.py'], root=root, output=output)
                self.assertEqual(result.status, 0, [d.reason for d in result.tooling] + [d.reason for r in result.results for d in r.diagnostics])
                module = 'unions' if mode == 'off' else 'pyalamode_exports.unions'
                script = ('from unions import Shape, Point\nfrom ' + module + ' import describe, area\n'
                          'assert (describe(4), describe("x"), describe(None)) == (4, 1, 0)\n'
                          'assert (area(Shape.Circle(3)), area(Shape.Dot()), area(Point(5, None)), area(None)) == (3, 0, 5, -1)\n')
                env = {**os.environ, 'PYTHONPATH': str(output) + os.pathsep + str(Path(__file__).resolve().parents[1])}
                run = subprocess.run([sys.executable, '-c', script], cwd=output, env=env, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                if mode != 'off':
                    for bad in ['describe(True)', 'describe(b"x")', 'area(7)']:
                        failed = subprocess.run([sys.executable, '-c', 'from ' + module + ' import describe, area\n' + bad], cwd=output, env=env, capture_output=True, text=True)
                        self.assertNotEqual(failed.returncode, 0, bad)
                        self.assertIn('unions:', failed.stderr)


class UnionRuntime(unittest.TestCase):
    def test_record_and_case_fields_validate_exact_members(self):
        from pyalamode import record, oneof, case

        @record
        class Pair:
            left: int | None
            right: 'str | bytes' = 'a'

        @oneof
        class Slot:
            @case
            class Filled:
                value: Pair | None

        self.assertEqual(Pair(None).left, None)
        self.assertEqual(Slot.Filled(Pair(1, b'z')).value.right, b'z')
        for bad in [lambda: Pair('x'), lambda: Pair(True), lambda: Pair(1, 2), lambda: Slot.Filled(3)]:
            with self.assertRaises(TypeError):
                bad()

    def test_overlap_and_bool_int_are_refused(self):
        from pyalamode import record, oneof, case

        @oneof
        class Slot:
            @case
            class Empty:
                pass
        for annotation in [bool | int, Slot | Slot.Empty]:
            with self.assertRaises(TypeError):
                record(type('Bad', (), {'__annotations__': {'v': annotation}, '__module__': __name__, '__qualname__': 'Bad'}))

    def test_validate_data_accepts_any_member_order(self):
        from pyalamode import record
        from pyalamode.boundaries import validate_data

        @record
        class Holder:
            value: int | None
        for members in [("int", "None"), ("None", "int")]:
            schema = ('union', (('record', Holder, (('value', ('union', members)),)), 'str'))
            self.assertEqual(validate_data(Holder(None), schema).value, None)
            self.assertEqual(validate_data('x', schema), 'x')
            with self.assertRaises(TypeError):
                validate_data(3, schema)



from pyalamode import record as _record, oneof as _oneof, case as _case


@_record
class EncodedLeft:
    value: int | None


@_record
class EncodedRight:
    value: int


@_oneof
class EncodedSlot:
    @_case
    class Filled:
        n: int

    @_case
    class Empty:
        pass


class UnionEncoding(unittest.TestCase):
    def test_round_trip_member_index_and_order_independence(self):
        from pyalamode import value_encode, value_decode, Vector
        Left, Right, Slot = EncodedLeft, EncodedRight, EncodedSlot
        schema = Left | Right | Slot | None
        for value in [Left(1), Left(None), Right(2), Slot.Filled(3), Slot.Empty(), None]:
            decoded = value_decode(value_encode(value, schema), schema)
            self.assertIs(type(decoded), type(value))
            self.assertEqual(decoded, value)
        # Two record members share the record wire tag; the member index separates them.
        self.assertNotEqual(value_encode(Left(2), Left | Right)[-14:], value_encode(Right(2), Left | Right)[-14:])
        self.assertEqual(value_encode(1, int | None), value_encode(1, None | int))
        self.assertEqual(value_decode(value_encode(Vector.of(1, None), Vector[int | None]), Vector[int | None]), Vector.of(1, None))

    def test_refusals(self):
        from pyalamode import value_encode, value_decode
        for value in [True, 'x', 1.5]:
            with self.assertRaises(TypeError):
                value_encode(value, int | None)
        with self.assertRaises(TypeError):
            value_encode(1, bool | int)
        with self.assertRaises(ValueError):
            value_decode(value_encode(1, int | None), int | str)
        corrupted = bytearray(value_encode(None, int | None))
        corrupted[-2] = 9
        with self.assertRaises(ValueError):
            value_decode(bytes(corrupted), int | None)

    def test_checked_codec_accepts_union_schemas(self):
        source = IMPORTS + 'from pyalamode import value_encode, value_decode\n@fun\ndef wire(v: int | None) -> bytes:\n    return value_encode(v, int | None)\n@fun\ndef back(b: bytes) -> int | None:\n    return value_decode(b, None | int)\n'
        result = analyze_source(source, path='codec.py')
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        bad = analyze_source(source.replace('value_encode(v, int | None)', 'value_encode(v, int | str)'), path='codec.py')
        self.assertFalse(bad.verified)


if __name__ == '__main__':
    unittest.main()
