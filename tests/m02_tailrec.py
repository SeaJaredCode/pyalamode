"""@tailrec: proven self tail calls (PAL122) run on a constant-depth trampoline."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pyalamode import tailrec, effects, Clock, ClockCapability, recorded_clock
from pyalamode.checker import analyze_source
from pyalamode.project import build_paths
import m11_distribution as _m11

PREFIX = 'from pyalamode import fun, tailrec, effects, Clock, ClockCapability, borrow, oneof, case\n'
TOTAL = '''@tailrec
def total(value: int, acc: int = 0) -> int:
    if value <= 0:
        return acc
    return total(value - 1, acc + value)
'''


def rules(source):
    result = analyze_source(PREFIX + source, path='rec.py')
    return result, sorted({d.rule for d in result.diagnostics})


class TailShape(unittest.TestCase):
    def accepted(self, source):
        result, found = rules(source)
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def refused(self, source, rule='PAL122'):
        result, found = rules(source)
        self.assertFalse(result.verified, source)
        self.assertIn(rule, found, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def test_accepted_shapes_and_contract(self):
        result = self.accepted(TOTAL + '@fun\ndef use() -> int:\n    return total(10)\n')
        contracts = {c.name: c for c in result.contracts}
        self.assertTrue(contracts['total'].tail_recursive)
        self.assertFalse(contracts['use'].tail_recursive)
        # A proven self tail call never deepens the stack.
        self.assertNotIn('RecursionError', contracts['total'].failures)
        self.assertNotIn('RecursionError', contracts['use'].failures)
        plain = analyze_source(PREFIX + TOTAL.replace('@tailrec', '@fun'), path='rec.py')
        self.assertIn('RecursionError', plain.contracts[0].failures)
        self.accepted('@tailrec\ndef f(n: int, acc: int) -> int:\n    return acc if n <= 0 else f(n - 1, acc + 1)\n')
        self.accepted('@tailrec\ndef f(n: int, acc: int) -> int:\n    if n == 0:\n        return acc\n    elif n == 1:\n        return f(0, acc + 1)\n    else:\n        return f(n - 2, acc + 2)\n')
        self.accepted('@oneof\nclass Step:\n    @case\n    class More:\n        n: int\n    @case\n    class Done:\n        pass\n'
                      '@tailrec\ndef f(s: Step, acc: int) -> int:\n    match s:\n        case Step.More(n):\n            return f(Step.Done() if n <= 1 else Step.More(n - 1), acc + n)\n        case Step.Done():\n            return acc\n')
        self.accepted('import pyalamode\n@pyalamode.tailrec\ndef f(n: int) -> int:\n    return 0 if n <= 0 else f(n - 1)\n')
        self.accepted('@tailrec\ndef no_recursion(n: int) -> int:\n    return n + 1\n')

    def test_effects_compose_in_either_order(self):
        for decorators in ['@tailrec\n@effects(Clock)\n', '@effects(Clock)\n@tailrec\n']:
            with self.subTest(decorators=decorators):
                self.accepted(decorators + 'def f(c: ClockCapability, n: int) -> int:\n    return n if n <= 0 else f(c, n - 1)\n')

    def test_refused_shapes(self):
        cases = {
            'operand of an operation': '    return 1 + total(value - 1, acc)',
            'keyword arguments': '    return total(value - 1, acc=acc + value)',
            'missing argument': '    return total()',
            'too many arguments': '    return total(value, acc, 1)',
            'starred arguments': '    return total(*(value - 1, acc))',
            'local alias': '    again = total\n    return again(value - 1, acc + value)',
            'callback': '    return apply(total, value - 1)',
            'inside try': '    try:\n        return total(value - 1, acc + value)\n    except ZeroDivisionError:\n        return acc',
            'assigned first': '    nxt = total(value - 1, acc + value)\n    return nxt',
        }
        helper = '@fun\ndef apply(f: Callable[[int, int], int], n: int) -> int:\n    return f(n, 0)\n'
        for label, body in cases.items():
            with self.subTest(label):
                source = TOTAL.replace('    return total(value - 1, acc + value)', body)
                if label == 'callback':
                    source = 'from typing import Callable\n' + helper + source
                self.refused(source)

    def test_refused_borrow_closures_mutual_and_signatures(self):
        self.refused('@tailrec\n@effects(Clock)\ndef f(c: ClockCapability, n: int) -> int:\n    with borrow(c) as b:\n        return n if n <= 0 else f(b, n - 1)\n')
        self.refused('@tailrec\ndef f(n: int) -> int:\n    def inner() -> int:\n        return n\n    return 0 if n <= 0 else f(n - 1)\n')
        self.refused('@tailrec\ndef a(n: int) -> int:\n    return 0 if n <= 0 else b(n - 1)\n@fun\ndef b(n: int) -> int:\n    return a(n)\n')
        self.refused('@tailrec\ndef f(n: int, *, step: int = 1) -> int:\n    return 0 if n <= 0 else f(n - step)\n')
        self.refused('@tailrec\ndef f(f: int) -> int:\n    return f\n')
        self.refused('@tailrec\n@fun\ndef f(n: int) -> int:\n    return n\n', 'PAL120')

    def test_rebound_frame_access_invalidates_the_marker(self):
        self.refused('import sys\nsys._getframe = None\n' + TOTAL, 'PAL120')


@tailrec
def countdown_total(value: int, total: int = 0) -> int:
    if value <= 0:
        return total
    return countdown_total(value - 1, total + value)


@tailrec
@effects(Clock)
def stamps(clock: ClockCapability, count: int, last: int) -> int:
    return last if count <= 0 else stamps(clock, count - 1, clock.now_ns())


def _call_back(callback, value):
    return callback(value)


@tailrec
def through_callback(value: int) -> int:
    # Unchecked ordinary code: a re-entrant call from another frame is a full call.
    return value if value <= 0 else _call_back(through_callback, value - 1)


class Trampoline(unittest.TestCase):
    def test_constant_depth_far_beyond_the_recursion_limit(self):
        self.assertLess(sys.getrecursionlimit(), 100_000)
        self.assertEqual(countdown_total(100_000), 5_000_050_000)
        self.assertEqual(countdown_total(3, 10), 16)
        self.assertEqual(countdown_total(value=4), 10)

    def test_effects_and_metadata(self):
        self.assertEqual(stamps(recorded_clock((1, 2, 3)), 3, 0), 3)
        self.assertEqual(countdown_total.__name__, 'countdown_total')
        self.assertEqual(countdown_total.__annotations__, {'value': int, 'total': int, 'return': int})
        with self.assertRaises(TypeError):
            tailrec(len)

    def test_reentry_from_another_frame_is_an_ordinary_call(self):
        self.assertEqual(through_callback(50), 0)

    def test_failures_point_at_the_body(self):
        @tailrec
        def divide(n: int, d: int) -> int:
            return n // d if d == 0 else divide(n, d - 1)
        try:
            divide(10, 3)
        except ZeroDivisionError as error:
            frames = [frame.name for frame in __import__('traceback').extract_tb(error.__traceback__)]
        else:
            self.fail('expected ZeroDivisionError')
        self.assertEqual(frames[-1], 'divide')
        self.assertLess(len(frames), 5)


class TailrecProjects(unittest.TestCase):
    def test_build_off_exports_debug_real_runs(self):
        for mode in ['off', 'exports', 'debug']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / 'rec.py').write_text(PREFIX + TOTAL)
                if mode != 'off':
                    (root / 'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="' + mode + '"\nguarded_exports=["rec:total"]\n')
                output = root / 'out'
                result = build_paths([root / 'rec.py'], root=root, output=output)
                self.assertEqual(result.status, 0, [d.reason for d in result.tooling] + [d.reason for r in result.results for d in r.diagnostics])
                module = 'rec' if mode == 'off' else 'pyalamode_exports.rec'
                env = {**os.environ, 'PYTHONPATH': str(output) + os.pathsep + str(Path(__file__).resolve().parents[1])}
                run = subprocess.run([sys.executable, '-c', 'from ' + module + ' import total\nassert total(50000) == 1250025000\n'], cwd=output, env=env, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                if mode != 'off':
                    bad = subprocess.run([sys.executable, '-c', 'from ' + module + ' import total\ntotal(True)'], cwd=output, env=env, capture_output=True, text=True)
                    self.assertNotEqual(bad.returncode, 0)


class TailrecDistribution(unittest.TestCase):
    setUp = _m11.DistributionTests.setUp
    tearDown = _m11.DistributionTests.tearDown
    wheel = _m11.DistributionTests.wheel
    check = _m11.DistributionTests.check

    def test_exported_tailrec_function_is_used_by_a_consumer(self):
        (self.producer / 'checked_pricing/core.py').write_text('from pyalamode import fun, tailrec\n' + TOTAL + '@fun\ndef quote(value:int)->int:\n    return total(value)\n')
        self.wheel()
        result = self.check()
        self.assertEqual(result.status, 0, [d.format() for r in result.results for d in r.diagnostics])
        exported = next(e for e in result.checked_dependencies[0]['exports'] if e['selector'] == 'checked_pricing.core:quote')
        self.assertNotIn('RecursionError', exported['contract']['failures'])
        # The consumer runs the installed wheel's trampoline far past the recursion limit.
        script = 'import sys\nsys.path[:0] = [' + repr(str(self.site)) + ', ' + repr(str(self.consumer)) + ']\nfrom use import total\nassert total(30000) == 450015000\n'
        run = subprocess.run([sys.executable, '-c', script], env={**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1])}, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)


if __name__ == '__main__':
    unittest.main()
