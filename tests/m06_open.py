"""Sum-type stage 3: open @oneof(open=True) domains with distribution-scoped @case(of=...)."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pyalamode import oneof, case, record, value_encode, value_decode
from pyalamode.checker import analyze_source, analyze_sources
from pyalamode.project import check_paths, build_paths
import m11_distribution as _m11

IMPORTS = 'from pyalamode import fun, oneof, case, record\n'
DOMAIN = '''@oneof(open=True)
class Shape:
    @case
    class Circle:
        r: int
'''
EXTENSION = '''@case(of=Shape)
class Square:
    side: int
'''
FULL = '''@fun
def size(s: Shape) -> int:
    match s:
        case Shape.Circle(r): return r
        case Square(side): return side
'''


def _rejected(test, result, rule):
    test.assertFalse(result.verified)
    test.assertIn(rule, [d.rule for d in result.diagnostics], '\n'.join(d.format() for d in result.diagnostics))


class OpenDeclarations(unittest.TestCase):
    def test_extension_in_same_module_and_exhaustive_coverage(self):
        result = analyze_source(IMPORTS + DOMAIN + EXTENSION + FULL, path='shapes.py')
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        row = result.oneofs[0]
        self.assertTrue(row['open'])
        self.assertEqual(list(row['cases']), ['Circle', 'Square'])
        self.assertEqual(row['cases']['Square'], {**row['cases']['Square'], 'extension': True, 'qualname': 'Square', 'module': 'shapes'})
        self.assertEqual(result.contracts[0].patterns[0]['case_set'], ["Case['shapes:Shape:Circle']", "Case['shapes:Shape:Square']"])
        _rejected(self, analyze_source(IMPORTS + DOMAIN + EXTENSION + FULL.replace('        case Square(side): return side\n', ''), path='shapes.py'), 'PAL330')
        wildcard = IMPORTS + DOMAIN + EXTENSION + '@fun\ndef f(s: Shape) -> int:\n    match s:\n        case Shape.Circle(r): return r\n        case _: return 0\n'
        self.assertTrue(analyze_source(wildcard, path='shapes.py').verified)
        _rejected(self, analyze_source(wildcard, path='shapes.py', policy={'explicit_cases': ['shapes:Shape']}), 'PAL330')

    def test_open_domain_may_start_empty(self):
        source = IMPORTS + '@oneof(open=True)\nclass Event:\n    pass\n@case(of=Event)\nclass Started:\n    at: int\n@fun\ndef f(e: Event) -> int:\n    match e:\n        case Started(at): return at\n'
        self.assertTrue(analyze_source(source, path='events.py').verified)
        _rejected(self, analyze_source(IMPORTS + '@oneof\nclass Event:\n    pass\n', path='events.py'), 'PAL120')

    def test_refused_declarations(self):
        closed = IMPORTS + '@oneof\nclass Shape:\n    @case\n    class Circle:\n        r: int\n' + EXTENSION
        _rejected(self, analyze_source(closed, path='shapes.py'), 'PAL120')
        _rejected(self, analyze_source(IMPORTS + '@case\nclass Loose:\n    n: int\n', path='shapes.py'), 'PAL120')
        _rejected(self, analyze_source(IMPORTS + DOMAIN + '@case(of=Shape)\nclass Circle:\n    pass\n', path='shapes.py'), 'PAL101')
        for spelling in ['@oneof(open=False)', '@oneof(open=1)', '@oneof()']:
            with self.subTest(spelling=spelling):
                _rejected(self, analyze_source(IMPORTS + DOMAIN.replace('@oneof(open=True)', spelling), path='shapes.py'), 'PAL120')
        _rejected(self, analyze_source(IMPORTS + DOMAIN + '@case(of=Shape)\nclass Bad:\n    side: int\n    def area(self): return 1\n', path='shapes.py'), 'PAL120')

    def test_extension_is_not_a_domain_attribute(self):
        source = IMPORTS + DOMAIN + EXTENSION + '@fun\ndef f() -> Shape:\n    return Shape.Square(1)\n'
        self.assertFalse(analyze_source(source, path='shapes.py').verified)
        source = IMPORTS + DOMAIN + EXTENSION + '@fun\ndef f(s: Shape.Square) -> int:\n    return 1\n'
        _rejected(self, analyze_source(source, path='shapes.py'), 'PAL130')

    def test_cross_module_extension_inside_one_project(self):
        sources = {'/p/shapes.py': IMPORTS + DOMAIN, '/p/more.py': IMPORTS + 'from shapes import Shape\n' + EXTENSION,
                   '/p/use.py': IMPORTS + 'from shapes import Shape\nfrom more import Square\n' + FULL}
        results = analyze_sources(sources, root='/p')
        self.assertTrue(all(r.verified for r in results.values()), [d.format() for r in results.values() for d in r.diagnostics])


class OpenProjects(unittest.TestCase):
    def test_census_finds_unimported_extensions_and_invalidates_caches(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'shapes.py').write_text('# mode: fun\n' + IMPORTS + DOMAIN)
            (root / 'use.py').write_text('# mode: fun\n' + IMPORTS + 'from shapes import Shape\ndef f(s: Shape) -> int:\n    match s:\n        case Shape.Circle(r): return r\n')
            self.assertEqual(check_paths([root / 'use.py'], root=root).status, 0)
            self.assertTrue(all(r.cache_hit for r in check_paths([root / 'use.py'], root=root).results))
            # A new module nobody imports still contributes a case to the open domain.
            (root / 'more.py').write_text('# mode: fun\n' + IMPORTS + 'from shapes import Shape\n' + EXTENSION)
            changed = check_paths([root / 'use.py'], root=root)
            self.assertEqual(changed.status, 1)
            self.assertIn('Square', ' '.join(d.reason for r in changed.results for d in r.diagnostics))
            (root / 'use.py').write_text('# mode: fun\n' + IMPORTS + 'from shapes import Shape\ndef f(s: Shape) -> int:\n    match s:\n        case Shape.Circle(r): return r\n        case _: return 0\n')
            self.assertEqual(check_paths([root / 'use.py'], root=root).status, 0)

    def test_guarded_builds_import_extension_modules(self):
        for mode in ['off', 'exports', 'debug']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / 'shapes.py').write_text(IMPORTS + DOMAIN)
                (root / 'more.py').write_text(IMPORTS + 'from shapes import Shape\n' + EXTENSION)
                (root / 'use.py').write_text(IMPORTS + 'from shapes import Shape\nfrom more import Square\n' + FULL)
                if mode != 'off':
                    (root / 'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="' + mode + '"\nguarded_exports=["use:size"]\n')
                output = root / 'out'
                result = build_paths([root / 'use.py'], root=root, output=output)
                self.assertEqual(result.status, 0, [d.reason for d in result.tooling] + [d.reason for r in result.results for d in r.diagnostics])
                module = 'use' if mode == 'off' else 'pyalamode_exports.use'
                env = {**os.environ, 'PYTHONPATH': str(output) + os.pathsep + str(Path(__file__).resolve().parents[1])}
                script = 'from shapes import Shape\nfrom more import Square\nfrom ' + module + ' import size\nassert (size(Shape.Circle(2)), size(Square(5))) == (2, 5)\n'
                run = subprocess.run([sys.executable, '-c', script], cwd=output, env=env, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                if mode != 'off':
                    bad = subprocess.run([sys.executable, '-c', 'from ' + module + ' import size\nsize(3)'], cwd=output, env=env, capture_output=True, text=True)
                    self.assertNotEqual(bad.returncode, 0)


class OpenDistribution(unittest.TestCase):
    setUp = _m11.DistributionTests.setUp
    tearDown = _m11.DistributionTests.tearDown
    wheel = _m11.DistributionTests.wheel
    check = _m11.DistributionTests.check

    def publish(self):
        (self.producer / 'checked_pricing/core.py').write_text('# mode: fun\nfrom pyalamode import oneof, case\n' + DOMAIN + '@case(of=Shape)\nclass Square:\n    side: int\ndef quote(value:int)->int:\n    return value+2\n')
        policy = _m11.POLICY.replace('exports=["checked_pricing.core:quote"]', 'exports=["checked_pricing.core:quote","checked_pricing.core:Shape","checked_pricing.core:Square"]')
        (self.producer / 'pyproject.toml').write_text(policy)
        self.wheel()

    def use(self, body):
        (self.consumer / 'use.py').write_text('from pyalamode import fun, case\nfrom checked_pricing.core import Shape, Square\n' + body)
        return self.check()

    def test_consumers_need_a_wildcard_and_cannot_extend(self):
        self.publish()
        exhaustive = '@fun\ndef f(s: Shape) -> int:\n    match s:\n        case Shape.Circle(r): return r\n        case Square(side): return side\n'
        refused = self.use(exhaustive)
        self.assertEqual(refused.status, 1)
        self.assertIn('another checked distribution', ' '.join(d.reason for r in refused.results for d in r.diagnostics))
        self.assertEqual(self.use(exhaustive.replace('        case Square(side): return side\n', '        case _: return 0\n')).status, 0)
        union = '@fun\ndef f(s: Shape | None) -> int:\n    match s:\n        case Shape(): return 1\n        case None: return 0\n'
        self.assertEqual(self.use(union).status, 0)
        extended = self.use('@case(of=Shape)\nclass Mine:\n    n: int\n')
        self.assertEqual(extended.status, 1)
        self.assertIn('own checked distribution', ' '.join(d.reason for r in extended.results for d in r.diagnostics))


@oneof(open=True)
class EncodedShape:
    @case
    class Circle:
        r: int


@case(of=EncodedShape)
class EncodedSquare:
    side: int


@record
class EncodedHolder:
    shape: EncodedShape | None


class OpenRuntime(unittest.TestCase):
    def test_catalog_isinstance_and_encoding(self):
        from pyalamode import sums
        names = [sums._pending_info(kind)[5] for kind, _ in sums._oneof_info(EncodedShape)[2]]
        self.assertEqual(names, ['Circle', 'EncodedSquare'])
        self.assertTrue(isinstance(EncodedSquare(1), EncodedShape))
        self.assertFalse(hasattr(EncodedShape, 'EncodedSquare'))
        for value in [EncodedShape.Circle(1), EncodedSquare(2)]:
            self.assertEqual(value_decode(value_encode(value, EncodedShape), EncodedShape), value)
        self.assertEqual(EncodedHolder(EncodedSquare(3)).shape, EncodedSquare(3))

    def test_runtime_refusals(self):
        with self.assertRaises(TypeError):
            case(of=EncodedShape)(type('Circle', (), {'__module__': __name__, '__qualname__': 'Circle'}))
        closed = oneof(type('Closed', (), {'__module__': __name__, '__qualname__': 'Closed', 'Only': case(type('Only', (), {'__module__': __name__, '__qualname__': 'Closed.Only'}))}))
        with self.assertRaises(TypeError):
            case(of=closed)
        with self.assertRaises(TypeError):
            oneof(open=1)
        with self.assertRaises(TypeError):
            case(type('Bad', (), {'__module__': __name__, '__qualname__': 'Bad'}), of=EncodedShape)


if __name__ == '__main__':
    unittest.main()
