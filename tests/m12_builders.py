"""Focused development controls for confined source and retained provenance.

Application fixtures are read and compiled by check/build, never imported here.
Runtime lifetime controls belong to m12_runtime.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from pyalamode.project import build_paths, check_paths, load_policy
from pyalamode import distribution as d, migration as m
from pyalamode.migration_views import observe
from pyalamode.builder_contracts import operation_catalog


SOURCE = '''from pyalamode import Vector, VectorBuilder, fun, vector_build
@fun
def assemble(values: Vector[int]) -> Vector[int]:
    def fill(out: VectorBuilder[int]) -> None:
        out.extend(values)
        out.append(-1)
    return vector_build(fill)
'''

D06_SOURCE = '''from pyalamode import fun, Vector, VectorBuilder, vector_build
@fun
def double(x:int)->int:
    return x*2
@fun
def large(x:int)->bool:
    return x>5
@fun
def make(source:Vector[int])->Vector[int]:
    def fill(b:VectorBuilder[int])->None:
        b.extend(source.map(double).filter(large))
        b.append(17)
    return vector_build(fill)
'''


class BuilderSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'core.py'
        self.source.write_text(SOURCE)
        self.policy = self.root / 'pyproject.toml'
        self.policy.write_text('[tool.pyalamode]\nbuilders=true\n')

    def tearDown(self):
        self.temp.cleanup()

    def check(self, **kwargs):
        return check_paths([self.root], root=self.root, **kwargs)

    def rules(self, result):
        return [x.rule for file in result.results for x in file.diagnostics]

    def contract(self, result, name='assemble'):
        return next(c for file in result.results for c in file.contracts if c.name == name)

    def test_fixed64_method_chain_and_source_contract_refusals(self):
        # Original stopped cost source is inert; the finite checker never admits
        # bare Vector(). The typed control uses only the existing empty of API.
        original = '''# mode: fun
from pyalamode import Vector, VectorBuilder, vector_build

def builder_assembly(chunks: Vector[Vector[int]]) -> Vector[int]:
    def populate(builder: VectorBuilder[int]) -> None:
        builder.extend(chunks[0])
        builder.extend(chunks[1])
        builder.extend(chunks[2])
        builder.extend(chunks[3])
        builder.extend(chunks[4])
        builder.extend(chunks[5])
        builder.extend(chunks[6])
        builder.extend(chunks[7])
        builder.extend(chunks[8])
        builder.extend(chunks[9])
        builder.extend(chunks[10])
        builder.extend(chunks[11])
        builder.extend(chunks[12])
        builder.extend(chunks[13])
        builder.extend(chunks[14])
        builder.extend(chunks[15])
        builder.extend(chunks[16])
        builder.extend(chunks[17])
        builder.extend(chunks[18])
        builder.extend(chunks[19])
        builder.extend(chunks[20])
        builder.extend(chunks[21])
        builder.extend(chunks[22])
        builder.extend(chunks[23])
        builder.extend(chunks[24])
        builder.extend(chunks[25])
        builder.extend(chunks[26])
        builder.extend(chunks[27])
        builder.extend(chunks[28])
        builder.extend(chunks[29])
        builder.extend(chunks[30])
        builder.extend(chunks[31])
        builder.extend(chunks[32])
        builder.extend(chunks[33])
        builder.extend(chunks[34])
        builder.extend(chunks[35])
        builder.extend(chunks[36])
        builder.extend(chunks[37])
        builder.extend(chunks[38])
        builder.extend(chunks[39])
        builder.extend(chunks[40])
        builder.extend(chunks[41])
        builder.extend(chunks[42])
        builder.extend(chunks[43])
        builder.extend(chunks[44])
        builder.extend(chunks[45])
        builder.extend(chunks[46])
        builder.extend(chunks[47])
        builder.extend(chunks[48])
        builder.extend(chunks[49])
        builder.extend(chunks[50])
        builder.extend(chunks[51])
        builder.extend(chunks[52])
        builder.extend(chunks[53])
        builder.extend(chunks[54])
        builder.extend(chunks[55])
        builder.extend(chunks[56])
        builder.extend(chunks[57])
        builder.extend(chunks[58])
        builder.extend(chunks[59])
        builder.extend(chunks[60])
        builder.extend(chunks[61])
        builder.extend(chunks[62])
        builder.extend(chunks[63])
        builder.append(-1)
        return None
    return vector_build(populate)

def persistent_assembly(chunks: Vector[Vector[int]]) -> Vector[int]:
    return Vector().concat(chunks[0]).concat(chunks[1]).concat(chunks[2]).concat(chunks[3]).concat(chunks[4]).concat(chunks[5]).concat(chunks[6]).concat(chunks[7]).concat(chunks[8]).concat(chunks[9]).concat(chunks[10]).concat(chunks[11]).concat(chunks[12]).concat(chunks[13]).concat(chunks[14]).concat(chunks[15]).concat(chunks[16]).concat(chunks[17]).concat(chunks[18]).concat(chunks[19]).concat(chunks[20]).concat(chunks[21]).concat(chunks[22]).concat(chunks[23]).concat(chunks[24]).concat(chunks[25]).concat(chunks[26]).concat(chunks[27]).concat(chunks[28]).concat(chunks[29]).concat(chunks[30]).concat(chunks[31]).concat(chunks[32]).concat(chunks[33]).concat(chunks[34]).concat(chunks[35]).concat(chunks[36]).concat(chunks[37]).concat(chunks[38]).concat(chunks[39]).concat(chunks[40]).concat(chunks[41]).concat(chunks[42]).concat(chunks[43]).concat(chunks[44]).concat(chunks[45]).concat(chunks[46]).concat(chunks[47]).concat(chunks[48]).concat(chunks[49]).concat(chunks[50]).concat(chunks[51]).concat(chunks[52]).concat(chunks[53]).concat(chunks[54]).concat(chunks[55]).concat(chunks[56]).concat(chunks[57]).concat(chunks[58]).concat(chunks[59]).concat(chunks[60]).concat(chunks[61]).concat(chunks[62]).concat(chunks[63]).appended(-1)
'''
        policy = '[tool.pyalamode]\nschema=1\nbuilders=true\nboundary_guards="off"\n'
        self.assertEqual(len(original.encode()), 3812)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(),
                         '0d174fe7f96002a41f78278d678ac9fbd7e21bbad3861be239485ab14a1aa7e6')
        self.assertEqual(len(policy.encode()), 62)
        self.assertEqual(hashlib.sha256(policy.encode()).hexdigest(),
                         '2288fced08da39d55dea287290be62d0388d6f54ea3e5cf85937a33b9cff1313')
        typed = original.replace('return Vector().concat', 'return Vector[int].of().concat')

        def project(label, source):
            case = self.root / label
            case.mkdir()
            path = case / 'bulk_core.py'
            path.write_text(source)
            (case / 'pyproject.toml').write_text(policy)
            return case, path

        def parity(case, status):
            cold = check_paths([case], root=case)
            warm = check_paths([case], root=case)
            fresh = check_paths([case], root=case, cache=False)
            for result in (cold, warm, fresh):
                self.assertEqual(result.status, status, result.to_dict())
                self.assertEqual(result.verified, status == 0)
            self.assertTrue(all(file.cache_hit for file in warm.results))
            self.assertEqual(cold.results[0].diagnostics, warm.results[0].diagnostics)
            self.assertEqual(cold.results[0].diagnostics, fresh.results[0].diagnostics)
            self.assertEqual(cold.results[0].contracts, warm.results[0].contracts)
            self.assertEqual(cold.results[0].contracts, fresh.results[0].contracts)
            return cold

        def no_output(case, label):
            output = self.root / ('output-' + label)
            result = build_paths([case], root=case, output=output)
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertIsNone(result.output)
            self.assertFalse(output.exists())

        case, path = project('original-fixed64', original)
        rejected = parity(case, 1)
        self.assertTrue(any(row.rule == 'PAL230' and (row.line, row.column) == (75, 12)
                            for row in rejected.results[0].diagnostics), rejected.to_dict())
        no_output(case, 'original-fixed64')
        self.assertEqual(path.read_text(), original)

        case, path = project('typed-fixed64', typed)
        accepted = parity(case, 0)
        builder = self.contract(accepted, 'builder_assembly')
        persistent = self.contract(accepted, 'persistent_assembly')
        for contract in (builder, persistent):
            self.assertEqual(contract.returns, 'Vector[int]')
            self.assertEqual(contract.required_effects, [])
            self.assertIn('IndexError', contract.failures)
            self.assertTrue(contract.source_evidence.startswith('checked'))
            self.assertTrue(any('collections-v' in item for item in contract.trust))
        self.assertIn('RecursionError', builder.failures)
        self.assertEqual(len(builder.builder_scopes), 1)
        self.assertEqual(builder.builder_scopes[0]['callback'], 'builder_assembly.populate')
        self.assertEqual(builder.builder_scopes[0]['operations'], ['append', 'extend'])
        self.assertEqual(persistent.builder_scopes, [])
        self.assertTrue({'Vector.of', 'Vector.concat', 'Vector.appended', 'Vector.index'} <= set(persistent.operations))
        sentinel = case / 'executed'
        (case / 'shell.py').write_text('from pathlib import Path\nPath(' + repr(str(sentinel)) + ').write_text("executed")\n')
        built = build_paths([case], root=case, output=self.root / 'output-typed')
        self.assertEqual(built.status, 0, built.to_dict())
        self.assertFalse(sentinel.exists())
        self.assertEqual(path.read_text(), typed)
        self.assertEqual((case / 'pyproject.toml').read_text(), policy)

        case, _ = project('bool-fixed64', typed.replace('chunks: Vector[Vector[int]]', 'chunks: Vector[Vector[bool]]'))
        mismatch = parity(case, 1)
        self.assertIn('PAL221', self.rules(mismatch))
        self.assertTrue(any(row.rule == 'PAL221' and row.line == 75 for row in mismatch.results[0].diagnostics), mismatch.to_dict())
        no_output(case, 'bool-fixed64')

        case, _ = project('unknown-fixed64', typed.replace('return Vector[int].of().concat', 'return missing().concat'))
        missing = parity(case, 1)
        self.assertTrue(any(row.rule == 'PAL240' and (row.line, row.column) == (75, 12)
                            for row in missing.results[0].diagnostics), missing.to_dict())
        no_output(case, 'unknown-fixed64')
        case, _ = project('unknown-short', '# mode: fun\nfrom pyalamode import Vector\ndef unknown() -> Vector[int]:\n    return missing().concat(Vector.of(1))\n')
        short = parity(case, 1)
        projection = {(row.rule, row.line, row.column, row.end_line, row.end_column)
                      for row in short.results[0].diagnostics}
        self.assertIn(('PAL240', 4, 12, 4, 19), projection)
        self.assertIn(('PAL230', 4, 12, 4, 21), projection)
        no_output(case, 'unknown-short')

        # A real replacement remains a refusal, and does not invalidate an
        # independent scalar marker when the analyzed writer is introduced.
        case, path = project('writer-fixed64', original)
        scalar = case / 'valid.py'
        scalar.write_text('from pyalamode import fun\n@fun\ndef scalar(value:int)->int:return value+1\n')
        clean = check_paths([case], root=case)
        check_paths([case], root=case)
        original_scalar = next(file.contracts for file in clean.results if file.path == str(scalar))
        writer = case / 'writer.py'
        writer.write_text('import pyalamode as owner\nowner.Vector = None\n')
        refused = check_paths([case], root=case)
        fresh = check_paths([case], root=case, cache=False)
        for result in (refused, fresh):
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertFalse(result.verified)
            core = next(file for file in result.results if file.path == str(path))
            self.assertFalse(core.cache_hit)
            self.assertTrue(any(row.rule == 'PAL240' and (row.line, row.column) == (75, 12)
                                for row in core.diagnostics), result.to_dict())
        self.assertEqual(next(file.diagnostics for file in refused.results if file.path == str(path)),
                         next(file.diagnostics for file in fresh.results if file.path == str(path)))
        unchanged = next(file for file in refused.results if file.path == str(scalar))
        self.assertTrue(unchanged.cache_hit)
        self.assertEqual(unchanged.contracts, original_scalar)
        self.assertEqual(unchanged.diagnostics, [])
        no_output(case, 'writer-fixed64')
        writer.unlink()
        restored = check_paths([case], root=case)
        self.assertEqual(restored.status, 1, restored.to_dict())  # original bare constructor still refuses
        self.assertEqual(next(file.contracts for file in restored.results if file.path == str(path)),
                         next(file.contracts for file in clean.results if file.path == str(path)))
        self.assertEqual(path.read_text(), original)

    def test_chained_receiver_preserves_capture_failure_effect_and_actual_callee(self):
        def project(label, source):
            case = self.root / label
            case.mkdir()
            path = case / 'core.py'
            path.write_text(source)
            (case / 'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
            return case, path

        def checked(case, status):
            cold = check_paths([case], root=case)
            warm = check_paths([case], root=case)
            fresh = check_paths([case], root=case, cache=False)
            for result in (cold, warm, fresh):
                self.assertEqual(result.status, status, result.to_dict())
                self.assertEqual(result.verified, status == 0)
            self.assertTrue(all(file.cache_hit for file in warm.results))
            for left, right in zip(cold.results, fresh.results):
                self.assertEqual(left.diagnostics, right.diagnostics)
                self.assertEqual(left.contracts, right.contracts)
            return cold

        def no_output(case, label):
            output = self.root / ('rejected-' + label)
            result = build_paths([case], root=case, output=output)
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertIsNone(result.output)
            self.assertFalse(output.exists())

        capture_source = '''from pyalamode import fun, Vector
@fun
def assemble(seed:int, chunks:Vector[Vector[int]])->Vector[int]:
    def initial()->Vector[int]:
        return Vector.of(10//seed)
    return initial().concat(chunks[0]).appended(17)
'''
        case, path = project('captured-chain', capture_source)
        captured = checked(case, 0)
        initial = self.contract(captured, 'assemble.initial')
        outer = self.contract(captured, 'assemble')
        self.assertEqual(initial.captures, {'seed': 'int'})
        self.assertIn('ZeroDivisionError', initial.failures)
        self.assertIn('ZeroDivisionError', outer.failures)
        self.assertIn('IndexError', outer.failures)
        self.assertEqual(outer.required_effects, [])
        self.assertEqual(outer.returns, 'Vector[int]')
        self.assertTrue(any(edge['target'].endswith('::assemble.initial') for edge in outer.failure_edges))
        self.assertTrue(any(str(path) in dependency for dependency in outer.dependencies))

        handled_source = capture_source.replace('    return initial().concat(chunks[0]).appended(17)\n',
            '    try:\n        return initial().concat(chunks[0]).appended(17)\n    except ZeroDivisionError:\n        return Vector.of(0)\n')
        case, _ = project('handled-chain', handled_source)
        handled = checked(case, 0)
        outer = self.contract(handled, 'assemble')
        self.assertNotIn('ZeroDivisionError', outer.failures)
        self.assertIn('IndexError', outer.failures)
        self.assertTrue(any('ZeroDivisionError' in edge['handled'] for edge in outer.failure_edges
                            if edge['target'].endswith('::assemble.initial')))

        partial_source = capture_source.replace('def assemble(seed:int, chunks:Vector[Vector[int]])',
                                               'def assemble(flag:bool, chunks:Vector[Vector[int]])').replace(
            '    def initial()', '    if flag:\n        seed=2\n    def initial()')
        case, _ = project('partial-capture-chain', partial_source)
        partial = checked(case, 1)
        self.assertIn('PAL240', self.rules(partial))
        no_output(case, 'partial-capture')

        effect_source = '''from pyalamode import fun, effects, Effectful, Clock, Vector
@fun
def pure(run:Effectful[[int],Vector[int],Clock], value:int)->Vector[int]:
    return run(value).concat(Vector.of(1)).appended(17)
@effects(Clock)
def allowed(run:Effectful[[int],Vector[int],Clock], value:int)->Vector[int]:
    return run(value).concat(Vector.of(1)).appended(17)
'''
        case, _ = project('pure-effect-chain', effect_source)
        impure = checked(case, 1)
        self.assertEqual([(row.line, row.column) for file in impure.results for row in file.diagnostics
                          if row.rule == 'PAL310'], [(4, 12)])
        bad = self.contract(impure, 'pure')
        allowed = self.contract(impure, 'allowed')
        for contract in (bad, allowed):
            self.assertEqual(contract.required_effects, ['Clock'])
            self.assertTrue({'IndexError', 'KeyError', 'ValueError', 'UnicodeError', 'ZeroDivisionError', 'RecursionError'} <= set(contract.failures))
            self.assertTrue(contract.caller_obligations)
        self.assertEqual(allowed.effect_bound, ['Clock'])
        no_output(case, 'pure-effect')
        case, _ = project('allowed-effect-chain', effect_source.replace(
            '@fun\ndef pure(run:Effectful[[int],Vector[int],Clock], value:int)->Vector[int]:\n    return run(value).concat(Vector.of(1)).appended(17)\n', ''))
        allowed_result = checked(case, 0)
        self.assertEqual(self.contract(allowed_result, 'allowed').required_effects, ['Clock'])
        self.assertEqual(self.contract(allowed_result, 'allowed').effect_bound, ['Clock'])

        case, path = project('actual-module-chain', 'from pyalamode import fun\nimport calc as owner\n@fun\ndef apply(value:int)->int:return owner.concat(value)\n')
        dependency = case / 'calc.py'
        dependency.write_text('# mode: fun\ndef concat(value:int)->int:return value+1\n')
        scalar = case / 'valid.py'
        scalar.write_text('from pyalamode import fun\n@fun\ndef scalar(value:int)->int:return value+2\n')
        actual = checked(case, 0)
        apply = self.contract(actual, 'apply')
        self.assertTrue(any(edge['target'] == str(dependency) + '::concat' for edge in apply.failure_edges))
        self.assertNotIn('Vector.concat', apply.operations)
        self.assertIn(str(dependency), apply.dependencies)
        writer = case / 'writer.py'
        writer.write_text('import calc as owner\nowner.concat = None\n')
        refused = check_paths([case], root=case)
        fresh = check_paths([case], root=case, cache=False)
        for result in (refused, fresh):
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertFalse(result.verified)
            self.assertTrue(any(row.rule == 'PAL240' and (row.line, row.column) == (4, 34)
                                for file in result.results if file.path == str(path) for row in file.diagnostics), result.to_dict())
        self.assertEqual(next(file.contracts for file in refused.results if file.path == str(scalar)),
                         next(file.contracts for file in actual.results if file.path == str(scalar)))
        self.assertTrue(next(file.cache_hit for file in refused.results if file.path == str(scalar)))
        no_output(case, 'actual-module')
        writer.unlink()
        restored = checked(case, 0)
        self.assertEqual(self.contract(restored, 'apply'), apply)

        case, _ = project('record-field-chain', 'from pyalamode import fun, record, Vector\n@record\nclass Box:\n    values:Vector[int]\n@fun\ndef read(box:Box)->Vector[int]:\n    return box.values.concat(Vector.of(1)).appended(2)\n')
        field = checked(case, 0)
        self.assertTrue({'Record.field', 'Vector.concat', 'Vector.of', 'Vector.appended'} <= set(self.contract(field, 'read').operations))
        self.assertEqual(self.contract(field, 'read').required_effects, [])

        case, _ = project('shadowed-source-member', 'from pyalamode import fun\nimport calc as owner\n@fun\ndef apply(owner:int, value:int)->int:return owner.concat(value)\n')
        (case / 'calc.py').write_text('# mode: fun\ndef concat(value:int)->int:return value+1\n')
        shadow = checked(case, 1)
        self.assertTrue(any(row.rule == 'PAL201' and row.line == 4 for file in shadow.results for row in file.diagnostics), shadow.to_dict())
        self.assertNotIn('Vector.concat', self.contract(shadow, 'apply').operations)
        no_output(case, 'shadowed-source-member')

        malformed = 'from pyalamode import fun, Vector, value_decode\n@fun\ndef invalid(raw:bytes)->Vector[int]:\n    return value_decode(raw, Vector[Unknown]).concat(Vector.of(1))\n'
        case, _ = project('malformed-quiet-schema', malformed)
        schema_refusal = checked(case, 1)
        self.assertTrue(any(row.rule == 'PAL130' and (row.line, row.column, row.end_line, row.end_column) == (4, 30, 4, 45)
                            for file in schema_refusal.results for row in file.diagnostics), schema_refusal.to_dict())
        no_output(case, 'malformed-quiet-schema')

        # Imported ordinary constants resolve in their own source analyzer.
        # Schema diagnostics there must remain real dependency diagnostics.
        delegated_caller = ('from pyalamode import fun, Vector\n'
                            'from constants import BAD\n@fun\n'
                            'def apply(xs:Vector[int])->Vector[int]:\n'
                            '    return BAD.concat(xs)\n')
        malformed_constant = ('from pyalamode import Vector, Clock\n'
                              'BAD = Vector[Clock].of()\n')
        valid_constant = malformed_constant.replace('Vector[Clock].of()', 'Vector.of(1)')

        def remote_refusal(result, caller, dependency):
            core = next(file for file in result.results if file.path == str(caller))
            remote = next(file for file in result.results if file.path == str(dependency))
            self.assertTrue(any(row.rule == 'PAL130' and
                                (row.line, row.column, row.end_line, row.end_column) == (2, 7, 2, 20)
                                for row in remote.diagnostics), result.to_dict())
            self.assertFalse(any(row.rule == 'PAL130' for row in core.diagnostics))
            self.assertTrue(any(row.rule == 'PAL240' and row.origin == 'dependency gate'
                                for row in core.diagnostics), result.to_dict())
            contract = self.contract(result, 'apply')
            self.assertEqual(contract.returns, 'Vector[int]')  # declared schema, no checked claim
            self.assertFalse(contract.source_evidence.startswith('checked'))
            self.assertNotIn('Vector.concat', contract.operations)
            self.assertEqual(contract.failures, [])
            self.assertEqual(contract.required_effects, [])
            self.assertIn(str(dependency), contract.dependencies)

        case, caller = project('delegated-malformed-constant', delegated_caller)
        dependency = case / 'constants.py'
        dependency.write_text(malformed_constant)
        delegated = checked(case, 1)
        remote_refusal(delegated, caller, dependency)
        no_output(case, 'delegated-malformed-constant')
        self.assertEqual(caller.read_text(), delegated_caller)
        self.assertEqual(dependency.read_text(), malformed_constant)
        self.assertEqual((case / 'pyproject.toml').read_text(), '[tool.pyalamode]\nbuilders=true\n')

        case, caller = project('delegated-constant-restoration', delegated_caller)
        dependency = case / 'constants.py'
        dependency.write_text(valid_constant)
        scalar = case / 'valid.py'
        scalar.write_text('from pyalamode import fun\n@fun\ndef scalar(value:int)->int:return value+3\n')
        clean = checked(case, 0)
        original_contract = self.contract(clean, 'apply')
        self.assertEqual(original_contract.returns, 'Vector[int]')
        self.assertIn('Vector.concat', original_contract.operations)
        self.assertIn(str(dependency), original_contract.dependencies)
        self.assertEqual(original_contract.required_effects, [])
        original_scalar = next(file.contracts for file in clean.results if file.path == str(scalar))
        sentinel = case / 'executed'
        (case / 'shell.py').write_text('from pathlib import Path\nPath(' + repr(str(sentinel)) + ').write_text("executed")\n')
        built = build_paths([case], root=case, output=self.root / 'delegated-valid-output')
        self.assertEqual(built.status, 0, built.to_dict())
        self.assertFalse(sentinel.exists())
        dependency.write_text(malformed_constant)
        changed = check_paths([case], root=case)
        self.assertEqual(changed.status, 1, changed.to_dict())
        self.assertFalse(changed.verified)
        remote_refusal(changed, caller, dependency)
        self.assertFalse(next(file.cache_hit for file in changed.results if file.path == str(caller)))
        unchanged = next(file for file in changed.results if file.path == str(scalar))
        self.assertTrue(unchanged.cache_hit)
        self.assertEqual(unchanged.contracts, original_scalar)
        self.assertEqual(unchanged.diagnostics, [])
        repeated = (check_paths([case], root=case), check_paths([case], root=case),
                    check_paths([case], root=case, cache=False))
        for result in repeated:
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertFalse(result.verified)
            remote_refusal(result, caller, dependency)
        self.assertTrue(all(file.cache_hit for file in repeated[1].results))
        # Cached finish sorts an existing dependency-gate diagnostic; a fresh
        # gate appends it afterward. Preserve every field and duplicate while
        # comparing this inherited ordering distinction only for this control.
        for cold_file, warm_file, fresh_file in zip(*(result.results for result in repeated)):
            self.assertEqual(cold_file.path, warm_file.path)
            self.assertEqual(cold_file.path, fresh_file.path)
            self.assertCountEqual(cold_file.diagnostics, warm_file.diagnostics)
            self.assertCountEqual(cold_file.diagnostics, fresh_file.diagnostics)
            self.assertEqual(cold_file.contracts, warm_file.contracts)
            self.assertEqual(cold_file.contracts, fresh_file.contracts)
        no_output(case, 'delegated-constant-change')
        dependency.write_text(valid_constant)
        restored = checked(case, 0)
        self.assertEqual(self.contract(restored, 'apply'), original_contract)
        self.assertEqual(caller.read_text(), delegated_caller)
        self.assertEqual(dependency.read_text(), valid_constant)
        self.assertEqual((case / 'pyproject.toml').read_text(), '[tool.pyalamode]\nbuilders=true\n')
        self.assertFalse(sentinel.exists())

    def test_cold_warm_and_no_cache_exact_contract(self):
        cold = self.check()
        warm = self.check()
        fresh = self.check(cache=False)
        self.assertEqual(cold.status, 0, cold.to_dict())
        self.assertEqual(warm.status, 0, warm.to_dict())
        self.assertTrue(all(file.cache_hit for file in warm.results))
        for result in (cold, warm, fresh):
            parent = self.contract(result)
            scope = parent.builder_scopes
            self.assertEqual(len(scope), 1)
            self.assertEqual(scope[0], {'callback':'assemble.fill','parameter':'out','element_schema':'int',
                'line':7,'end_line':7,'callback_line':4,'callback_end_line':6,
                'lifetime':'fresh callback invocation; invalidated on every exit; no alias, retention or transfer',
                'operations':['append','extend'],
                'finalization':'automatic exact Vector result after None; construction failure publishes no result'})
            self.assertEqual(parent.required_effects, [])
            self.assertIn('RecursionError', parent.failures)
            self.assertEqual({r['identity'] for r in parent.operation_contracts}, {r['identity'] for r in operation_catalog()})
        self.assertEqual(self.contract(cold), self.contract(warm))
        self.assertEqual(self.contract(cold), self.contract(fresh))
        self.source.write_text(SOURCE.replace('from pyalamode import Vector, VectorBuilder, fun, vector_build','from pyalamode import Vector, fun\nimport pyalamode.builders').replace('out: VectorBuilder[int]','out: pyalamode.builders.VectorBuilder[int]').replace('return vector_build(fill)','return pyalamode.builders.vector_build(fill)'))
        namespace=self.check(cache=False)
        self.assertEqual(namespace.status,0,namespace.to_dict())

    def test_default_off_and_exact_policy(self):
        for text in ('', '[tool.pyalamode]\nbuilders=false\n'):
            self.policy.write_text(text)
            result = self.check(cache=False)
            self.assertEqual(result.status, 1)
            self.assertIn('PAL380', self.rules(result))
            self.assertNotIn('PAL130', self.rules(result))
            built = build_paths([self.root], root=self.root, output=self.root/'refused')
            self.assertEqual(built.status, 1)
            self.assertIsNone(built.output)
            self.assertFalse((self.root/'refused').exists())
        for value in ('1', '"true"', '[]', '{}'):
            self.policy.write_text('[tool.pyalamode]\nbuilders='+value+'\n')
            result = self.check(cache=False)
            self.assertEqual(result.status, 2)
            self.assertEqual([r.rule for r in result.tooling], ['PAL001'])

    def test_escape_and_carrier_once_proof(self):
        mutations = {
            'alias':'        other = out\n',
            'method':'        saved = out.append\n',
            'return':'        return out\n',
            'container':'        saved = Vector.of(out)\n',
            'lambda':'        saved = lambda: out\n',
            'unknown':'        unknown(out)\n',
            'store':'        box.value = out\n',
            'subscript':'        box[0] = out\n',
            'query':'        out.size()\n',
        }
        for label, body in mutations.items():
            with self.subTest(label=label):
                self.source.write_text(SOURCE.replace('        out.append(-1)\n', body))
                result = self.check(cache=False)
                self.assertEqual(result.status, 1)
                self.assertIn('PAL381', self.rules(result))
        for body in ('    saved = fill\n    return vector_build(fill)\n',
                     '    first = vector_build(fill)\n    return vector_build(fill)\n',
                     '    fill(1)\n    return vector_build(fill)\n'):
            self.source.write_text(SOURCE.replace('    return vector_build(fill)\n', body))
            self.assertIn('PAL381', self.rules(self.check(cache=False)))

    def test_shapes_schema_rebinding_and_none_return(self):
        controls = [
            (SOURCE.replace('out.append(-1)', 'out.append(True)'), 'PAL221'),
            (SOURCE.replace('out.extend(values)', 'out.extend((1, 2))'), 'PAL221'),
            (SOURCE.replace('out.append(-1)', 'out.append(value=1)'), 'PAL221'),
            (SOURCE.replace('out.append(-1)', 'out = 1'), 'PAL101'),
            (SOURCE.replace('out.append(-1)', 'return 1'), 'PAL381'),
            (SOURCE.replace('def fill(', 'async def fill('), 'PAL381'),
            (SOURCE.replace('out: VectorBuilder[int]', 'out'), 'PAL381'),
            (SOURCE.replace('out: VectorBuilder[int]', '*out: VectorBuilder[int]'), 'PAL381'),
            (SOURCE.replace('    def fill(', '    @fun\n    def fill('), 'PAL381'),
            (SOURCE.replace('out: VectorBuilder[int]', 'out: VectorBuilder[int], other: int'), 'PAL381'),
            (SOURCE.replace('out.append(-1)', 'yield 1'), 'PAL201'),
            (SOURCE.replace('out.append(-1)', 'for value in values:\n            out.append(value)'), 'PAL110'),
            (SOURCE.replace('return vector_build(fill)', 'vector_build(fill)'), 'PAL250'),
        ]
        for source, rule in controls:
            with self.subTest(source=source, rule=rule):
                self.source.write_text(source)
                result = self.check(cache=False)
                self.assertEqual(result.status, 1)
                self.assertIn(rule, self.rules(result))

        conditional=SOURCE.replace('    def fill(out: VectorBuilder[int]) -> None:\n        out.extend(values)\n        out.append(-1)\n', '    if True:\n        def fill(out: VectorBuilder[int]) -> None:\n            out.extend(values)\n            out.append(-1)\n')
        self.source.write_text(conditional)
        self.assertIn('PAL381',self.rules(self.check(cache=False)))
        for source in (SOURCE.replace('out: VectorBuilder[int]', 'out'), SOURCE.replace('out: VectorBuilder[int]', '*out: VectorBuilder[int]')):
            self.source.write_text(source)
            result=self.check(cache=False)
            self.assertTrue(any(row.rule=='PAL381' and (row.line,row.column)==(4,5) for file in result.results for row in file.diagnostics),result.to_dict())

    def test_pure_callback_effectful_parent_and_failure_graph(self):
        self.source.write_text('''from pyalamode import Vector, VectorBuilder, ClockCapability, Clock, effects, vector_build
@effects(Clock)
def assemble(clock: ClockCapability, value: int) -> Vector[int]:
    now = clock.now_ns()
    def fill(out: VectorBuilder[int]) -> None:
        out.append(value // 2)
    return vector_build(fill)
''')
        result = self.check(cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual(self.contract(result).required_effects, ['Clock'])
        self.assertIn('ZeroDivisionError', self.contract(result).failures)
        self.policy.write_text('[tool.pyalamode]\nbuilders=true\n[tool.pyalamode.effect_bounds]\n"core:assemble.fill"=["Clock"]\n')
        bounded=self.check(cache=False)
        self.assertEqual(bounded.status,0,bounded.to_dict())
        self.assertEqual(self.contract(bounded,'assemble.fill').effect_bound,[])
        original=self.source.read_text()
        self.source.write_text('from pyalamode import Vector, VectorBuilder, Effectful, Clock, effects, vector_build\n@effects(Clock)\ndef assemble(run:Effectful[[int],int,Clock], value:int)->Vector[int]:\n    def fill(out:VectorBuilder[int])->None:\n        out.append(run(value))\n    return vector_build(fill)\n')
        policy_refusal=self.check(cache=False)
        self.assertEqual(policy_refusal.status,1,policy_refusal.to_dict())
        self.assertIn('PAL310',self.rules(policy_refusal))
        self.source.write_text(original)
        self.policy.write_text('[tool.pyalamode]\nbuilders=true\n')
        self.source.write_text(self.source.read_text().replace('out.append(value // 2)', 'out.append(clock.now_ns())'))
        refused = self.check(cache=False)
        self.assertEqual(refused.status, 1)
        self.assertIn('PAL320', self.rules(refused))

    def test_current_writer_invalidates_warm_builder_dependency(self):
        self.assertEqual(self.check().status, 0)
        self.assertTrue(all(f.cache_hit for f in self.check().results))
        (self.root/'ordinary.py').write_text('import _thread\n_thread.get_ident = lambda: 1\n')
        refused = self.check()
        self.assertEqual(refused.status, 1, refused.to_dict())
        self.assertFalse(next(f for f in refused.results if f.path == str(self.source)).cache_hit)

    def test_parent_product_module_writer_cold_warm_refusal_and_restoration(self):
        writers = [
            ('exact', 'from pyalamode import builders\nbuilders._collections = None\n', 'builders', 'module:pyalamode.builders'),
            ('renamed', 'from pyalamode import builders as owner\nowner._collections=None\n', 'owner', 'module:pyalamode.builders'),
            ('assignment', 'from pyalamode import builders\nowner=builders\nowner._collections=None\n', 'owner', 'module:pyalamode.builders'),
            ('dotted', 'import pyalamode.builders as owner\nowner._collections=None\n', 'owner', 'module:pyalamode.builders'),
            ('parent', 'import pyalamode as pal\npal.builders._collections=None\n', 'pal.builders', 'module:pyalamode.builders'),
            ('dictionary', 'from pyalamode import builders as owner\nnamespace=owner.__dict__\nnamespace["_collections"]=None\n', 'namespace', 'module:pyalamode.builders'),
            ('setattr', 'from pyalamode import builders as owner\nsetattr(owner,"_collections",None)\n', 'owner', 'module:pyalamode.builders'),
            ('catalog', 'from pyalamode import builder_contracts as meta\nmeta.operation_contract=None\n', 'meta', 'module:pyalamode.builder_contracts'),
            ('helper', 'from pyalamode.builders import _collections as backend\nbackend._validate=None\n', 'backend', 'module:pyalamode.builders'),
            ('class', 'from pyalamode import builders\ncls=builders.VectorBuilder\ncls.append=None\n', 'cls', 'foundation:pyalamode:VectorBuilder'),
        ]
        for label, source, owner, expected in writers:
            with self.subTest(label=label):
                # Each shape starts from a clean proof, not a previously cached
                # refusal with an equivalent behavioral replacement context.
                case = self.root/label
                case.mkdir()
                core_path = case/'core.py'
                core_path.write_text(SOURCE)
                (case/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
                independent = case/'independent.py'
                independent.write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value + 1\n')
                def check(**kwargs):
                    return check_paths([case], root=case, **kwargs)
                cold, warm, fresh = check(), check(), check(cache=False)
                for result in (cold, warm, fresh):
                    self.assertEqual(result.status, 0, result.to_dict())
                    self.assertEqual(self.contract(result), self.contract(cold))
                self.assertTrue(all(file.cache_hit for file in warm.results))
                original_contracts = next(file.contracts for file in cold.results if file.path == str(core_path))
                writer = case/'writer.py'
                writer.write_text(source)
                capture = {}
                try:
                    refused = check(_capture=capture)
                    no_cache = check(cache=False)
                    graph = capture['graph']
                    self.assertEqual(graph.reference(graph.analyzers[str(writer)], ast.parse(owner, mode='eval').body), expected)
                    self.assertIn(('pyalamode', 'VectorBuilder'), graph.replaced_foundations)
                    for result in (refused, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertFalse(result.verified)
                        core = next(file for file in result.results if file.path == str(core_path))
                        self.assertFalse(core.cache_hit)
                        self.assertTrue(core.binding_context)
                        self.assertFalse(self.contract(result).source_evidence.startswith('checked'))
                        if label != 'class':
                            self.assertIn(('pyalamode', 'vector_build'), graph.replaced_foundations)
                            self.assertTrue(any(row.rule == 'PAL240' and (row.line, row.column) == (7, 12) for row in core.diagnostics), result.to_dict())
                    self.assertEqual(next(file.diagnostics for file in refused.results if file.path == str(core_path)), next(file.diagnostics for file in no_cache.results if file.path == str(core_path)))
                    self.assertEqual(next(file.contracts for file in refused.results if file.path == str(core_path)), next(file.contracts for file in no_cache.results if file.path == str(core_path)))
                    scalar = next(file for file in refused.results if file.path == str(independent))
                    self.assertTrue(scalar.cache_hit)
                    self.assertEqual(scalar.diagnostics, [])
                    self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
                    self.assertEqual(scalar.contracts, next(file.contracts for file in cold.results if file.path == str(independent)))
                    if label != 'class':
                        output = case/('refused-'+label)
                        built = build_paths([case], root=case, output=output)
                        self.assertEqual(built.status, 1, built.to_dict())
                        self.assertIsNone(built.output)
                        self.assertFalse(output.exists())
                    self.assertEqual(writer.read_text(), source)
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                self.assertEqual(next(file.contracts for file in restored.results if file.path == str(core_path)), original_contracts)
                self.assertTrue(all(file.cache_hit for file in check().results))
        self.assertEqual(self.source.read_text(), SOURCE)

    def test_parent_product_module_reference_inventory_and_parent_precedence(self):
        from pyalamode.checker import SourceGraph
        children = ('collections', 'records', 'boundaries', 'sums', 'failures', 'standard', 'standard_contracts',
                    'encoding', 'encoding_contracts', 'builders', 'builder_contracts', 'tasks', 'task_contracts', 'integrations', 'integration_contracts')
        reference_root = self.root/'references'
        reference_root.mkdir()
        reader = reference_root/'reader.py'
        text = ''.join('from pyalamode import '+name+'\nfrom pyalamode import '+name+' as renamed_'+name+'\n' for name in children)
        text += 'import pyalamode as pal\nfrom pyalamode import effects as decorator\nfrom pyalamode import unknown_child\n'
        reader.write_text(text)
        graph = SourceGraph({str(reader): text}, reference_root, False, {'builders': True})
        analyzer = graph.analyzers[str(reader)]
        for name in children:
            for expression in (name, 'renamed_'+name, 'pal.'+name):
                self.assertEqual(graph.reference(analyzer, ast.parse(expression, mode='eval').body), 'module:pyalamode.'+name)
        self.assertEqual(graph.reference(analyzer, ast.Name(id='decorator')), 'foundation:pyalamode:effects')
        self.assertEqual(graph.reference(analyzer, ast.parse('pal.effects', mode='eval').body), 'foundation:pyalamode:effects')
        self.assertEqual(graph.reference(analyzer, ast.Name(id='unknown_child')), 'foundation:pyalamode:unknown_child')
        self.assertNotIn(('pyalamode', 'vector_build'), graph.replaced_foundations)
        parent_sources = (
            ('function', '# mode: fun\ndef builders(value:int)->int:\n    return value\n'),
            ('scalar', 'builders = 1\n'),
            ('name-write', 'del builders\n'),
            ('wildcard-write', 'globals()[name] = None\n'),
            ('empty-override', '# ordinary local parent override\n'),
        )
        for label, parent_source in parent_sources:
            with self.subTest(parent=label):
                local = reference_root/label
                package = local/'pyalamode'
                package.mkdir(parents=True)
                parent = package/'__init__.py'
                child = package/'builders.py'
                shadow = local/'pyalamode.py'
                use = local/'reader.py'
                source_map = {str(parent): parent_source, str(child): '# mode: fun\ndef token(value:int)->int:return value\n',
                              str(shadow): '# mode: fun\ndef builders(value:int)->int:return value + 1\n',
                              str(use): 'from pyalamode import builders as found\nimport pyalamode as pal\n'}
                for path, source in source_map.items():
                    Path(path).write_text(source)
                local_graph = SourceGraph(source_map, local, False, {'builders': True})
                local_analyzer = local_graph.analyzers[str(use)]
                self.assertEqual(local_graph.modules['pyalamode'].path, str(parent))
                self.assertFalse(local_analyzer._foundation_available('pyalamode.builders'))
                self.assertIsNone(local_graph._product_child_reference(local_analyzer, 'pyalamode', 'builders'))
                expected = str(parent)+'::builders' if label == 'function' else 'module:pyalamode.builders' if label == 'empty-override' else None
                self.assertEqual(local_graph.reference(local_analyzer, ast.Name(id='found')), expected)
                self.assertEqual(local_graph.reference(local_analyzer, ast.parse('pal.builders', mode='eval').body), expected)
                if label == 'empty-override':
                    self.assertEqual(local_graph.modules['pyalamode.builders'].path, str(child))

    def test_facade_binding_replacement_keeps_unrelated_marker_proof(self):
        from pyalamode.checker import (SourceGraph, _FACADE_PUBLIC_BINDINGS, _PRODUCT_CHILD_MODULES,
                                      _product_source, _BUILTINS_WRITER_BINDINGS, COLLECTION_FOUNDATIONS)
        root_module = ast.parse((Path(__file__).resolve().parents[1]/'pyalamode/__init__.py').read_text())
        published = next(node.value for node in root_module.body if isinstance(node, ast.Assign)
                         and any(isinstance(target, ast.Name) and target.id == '__all__' for target in node.targets))
        self.assertEqual(_FACADE_PUBLIC_BINDINGS, frozenset(ast.literal_eval(published)))
        self.assertEqual(len(_FACADE_PUBLIC_BINDINGS), 73)
        product_directory = Path(__file__).resolve().parents[1]/'pyalamode'
        product_names = {'pyalamode': '__init__.py', 'pyalamode.effects': 'effects.py',
                         **{'pyalamode.'+name:name+'.py' for name in _PRODUCT_CHILD_MODULES}}
        self.assertEqual(len(product_names), 19)
        for module, filename in product_names.items():
            canonical = product_directory/filename
            self.assertTrue(_product_source(module, canonical))
            copied = self.root/('copy-'+filename)
            copied.write_bytes(canonical.read_bytes())
            self.assertFalse(_product_source(module, copied))
            copied.write_text('# mode: fun\ndef f(value:int)->int:return value\n')
            self.assertFalse(_product_source(module, copied))
        self.assertFalse(_product_source('pyalamode.checker', product_directory/'checker.py'))
        for name in sorted(_FACADE_PUBLIC_BINDINGS):
            text = 'import pyalamode as pal\npal.'+name+' = None\n'
            path = self.root/'inventory.py'
            graph = SourceGraph({str(path): text}, self.root, False, {'builders': True})
            self.assertIn(('pyalamode', name), graph.replaced_foundations)
            self.assertNotIn(('pyalamode', '*'), graph.replaced_foundations)

        writers = (
            ('exact', 'import pyalamode as pal\npal.vector_build = lambda callback: None\n'),
            ('plain', 'import pyalamode\npyalamode.vector_build = None\n'),
            ('alias', 'import pyalamode as pal\nowner = pal\nowner.vector_build = None\n'),
            ('typed', 'import pyalamode as pal\npal.vector_build: int = 1\n'),
            ('augmented', 'import pyalamode as pal\npal.vector_build += 1\n'),
            ('deleted', 'import pyalamode as pal\ndel pal.vector_build\n'),
            ('callable', 'from pyalamode import vector_build as factory\nfactory.__code__ = None\n'),
        )
        for label, writer_source in writers:
            with self.subTest(writer=label):
                case = self.root/('facade-'+label)
                case.mkdir()
                core = case/'core.py'
                core.write_text(D06_SOURCE)
                independent = case/'independent.py'
                independent.write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value+1\n')
                local = case/'local.py'
                local.write_text('from pyalamode import fun\n@fun\ndef double(value:int)->int:\n    return value*2\n@fun\ndef alias(value:int)->int:\n    vector_build = double\n    return vector_build(value)\n')
                (case/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
                def check(**kwargs):
                    return check_paths([case], root=case, **kwargs)
                cold, warm, fresh = check(), check(), check(cache=False)
                for result in (cold, warm, fresh):
                    self.assertEqual(result.status, 0, result.to_dict())
                    self.assertEqual(next(file.contracts for file in result.results if file.path == str(core)),
                                     next(file.contracts for file in cold.results if file.path == str(core)))
                self.assertTrue(all(file.cache_hit for file in warm.results))
                writer = case/'writer.py'
                writer.write_text(writer_source)
                capture = {}
                try:
                    refused = check(_capture=capture)
                    refused_warm, no_cache = check(), check(cache=False)
                    graph = capture['graph']
                    self.assertIn(('pyalamode', 'vector_build'), graph.replaced_foundations)
                    for name in ('*', 'fun', 'Vector'):
                        self.assertNotIn(('pyalamode', name), graph.replaced_foundations)
                    affected = next(file for file in refused.results if file.path == str(core))
                    self.assertFalse(affected.cache_hit)
                    self.assertTrue(affected.binding_context)
                    for result in (refused, refused_warm, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertFalse(result.verified)
                        file = next(file for file in result.results if file.path == str(core))
                        self.assertFalse(next(c for c in file.contracts if c.name == 'make').source_evidence.startswith('checked'))
                        self.assertEqual(file.diagnostics, affected.diagnostics)
                        self.assertEqual(file.contracts, affected.contracts)
                        self.assertNotIn('PAL120', [row.rule for row in file.diagnostics])
                        self.assertNotIn('PAL130', [row.rule for row in file.diagnostics])
                        target = [row.rule for row in file.diagnostics if (row.line, row.column) == (13, 12)]
                        self.assertIn('PAL240', target)
                        self.assertNotIn('PAL230', target)
                        primary = next(row for row in file.diagnostics if row.rule != 'PAL211')
                        self.assertEqual((primary.rule, primary.line, primary.column), ('PAL240', 13, 12))
                        for path in (independent, local):
                            scalar = next(file for file in result.results if file.path == str(path))
                            self.assertEqual(scalar.diagnostics, [])
                            self.assertTrue(all(c.source_evidence.startswith('checked') for c in scalar.contracts))
                            self.assertEqual(scalar.contracts, next(file.contracts for file in cold.results if file.path == str(path)))
                    self.assertTrue(next(file for file in refused.results if file.path == str(independent)).cache_hit)
                    self.assertTrue(next(file for file in refused_warm.results if file.path == str(core)).cache_hit)
                    output = case/'refused-output'
                    built = build_paths([case], root=case, output=output)
                    self.assertEqual(built.status, 1, built.to_dict())
                    self.assertIsNone(built.output)
                    self.assertFalse(output.exists())
                    self.assertEqual(writer.read_text(), writer_source)
                    self.assertEqual(core.read_text(), D06_SOURCE)
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                self.assertEqual(next(file.contracts for file in restored.results if file.path == str(core)),
                                 next(file.contracts for file in cold.results if file.path == str(core)))
                self.assertTrue(all(file.cache_hit for file in check().results))

        # These normalized namespace references cannot become precise facade
        # module objects, even when their spelling contains a public binding.
        conservative = (
            'import pyalamode as pal\nsetattr(pal,"vector_build",None)\n',
            'import pyalamode as pal\nsetattr(pal,name,None)\n',
            'import pyalamode as pal\npal._helper=None\n',
            'import pyalamode as pal\npal.builders=None\n',
            'import pyalamode as pal\nnamespace=pal.__dict__\nnamespace["vector_build"]=None\n',
            'from pyalamode import fun\nnamespace=fun.__globals__\nnamespace.vector_build=None\n',
            'import pyalamode as pal\npal.__dict__.clear()\n',
            'import pyalamode as pal\nowner=pal\nowner=object()\nowner.vector_build=None\n',
            'import pyalamode as pal\ndef write(pal):\n    pal.vector_build=None\n',
            'import pyalamode as pal\npal.__dict__["vector_build"]=None\n',
            'import pyalamode as pal\nowner=pal\nnamespace=owner.__dict__\nnamespace["vector_build"]=None\n',
            'import pyalamode as pal\nnamespace=pal.__dict__\nnamespace[key]=None\n',
            'import pyalamode as pal\nnamespace=pal.__dict__\nnamespace.update({"vector_build":None})\n',
        )
        for index, text in enumerate(conservative):
            with self.subTest(conservative=text):
                path = self.root/'conservative.py'
                graph = SourceGraph({str(path): text}, self.root, False, {'builders': True})
                self.assertIn(('pyalamode', '*'), graph.replaced_foundations)
                namespace_nodes = [node for node in ast.walk(graph.analyzers[str(path)].tree)
                                   if isinstance(node, ast.Attribute) and node.attr == '__dict__']
                for node in namespace_nodes:
                    self.assertEqual(graph.reference(graph.analyzers[str(path)], node), 'module:pyalamode')
                case = self.root/('conservative-'+str(index))
                case.mkdir()
                (case/'core.py').write_text(D06_SOURCE)
                (case/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
                def check(**kwargs):
                    return check_paths([case], root=case, **kwargs)
                accepted = check()
                self.assertEqual(accepted.status, 0, accepted.to_dict())
                self.assertTrue(all(file.cache_hit for file in check().results))
                writer = case/'writer.py'
                writer.write_text(text)
                try:
                    refused, no_cache = check(), check(cache=False)
                    affected = next(file for file in refused.results if file.path == str(case/'core.py'))
                    self.assertFalse(affected.cache_hit)
                    self.assertTrue(affected.binding_context)
                    for result in (refused, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertFalse(result.verified)
                        self.assertFalse(next(c for file in result.results for c in file.contracts if c.name == 'make').source_evidence.startswith('checked'))
                    self.assertEqual(affected.diagnostics, next(file.diagnostics for file in no_cache.results if file.path == affected.path))
                    output = case/'refused-output'
                    built = build_paths([case], root=case, output=output)
                    self.assertEqual(built.status, 1, built.to_dict())
                    self.assertIsNone(built.output)
                    self.assertFalse(output.exists())
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                self.assertEqual(restored.results[0].contracts, accepted.results[0].contracts)
                self.assertTrue(all(file.cache_hit for file in check().results))

        # A namespace identity must reach both actual captured callees and
        # native foundations even when no native source analyzer exists.
        source_cases = (
            ('captured', 'checked_dep.core', {'checked_dep/__init__.py':'# mode: fun\n',
                'checked_dep/core.py':'# mode: fun\ndef f(value:int)->int:\n    return value+1\n'}),
            ('shadow-root', 'pyalamode', {'pyalamode.py':'# mode: fun\ndef f(value:int)->int:\n    return value+1\n'}),
            ('shadow-child', 'pyalamode.builders', {'pyalamode/__init__.py':'# mode: fun\n',
                'pyalamode/builders.py':'# mode: fun\ndef f(value:int)->int:\n    return value+1\n'}),
            ('shadow-effects', 'pyalamode.effects', {'pyalamode/__init__.py':'# mode: fun\n',
                'pyalamode/effects.py':'# mode: fun\ndef f(value:int)->int:\n    return value+1\n'}),
        )
        for label, module, source_map in source_cases:
            mutations = ('namespace=owner.__dict__\nnamespace["f"]=None\n',
                         'owner.__dict__.clear()\n', 'owner.f=None\n')
            for index, mutation in enumerate(mutations):
                with self.subTest(namespace=label, mutation=index):
                    case = self.root/(label+'-'+str(index))
                    case.mkdir()
                    for name, source in source_map.items():
                        path = case/name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(source)
                    use = case/'use.py'
                    use.write_text('# mode: fun\nimport '+module+' as owner\ndef use(value:int)->int:\n    return owner.f(value)\n')
                    independent = case/'independent.py'
                    independent.write_text('# mode: fun\ndef independent(value:int)->int:\n    return value+1\n')
                    def check(**kwargs):
                        return check_paths([case], root=case, **kwargs)
                    cold, warm = check(), check()
                    self.assertEqual(cold.status, 0, cold.to_dict())
                    self.assertTrue(all(file.cache_hit for file in warm.results))
                    writer = case/'writer.py'
                    writer.write_text('import '+module+' as owner\n'+mutation)
                    capture = {}
                    try:
                        refused, no_cache = check(_capture=capture), check(cache=False)
                        graph = capture['graph']
                        analyzer = graph.analyzers[str(writer)]
                        self.assertEqual(graph.reference(analyzer, ast.Name(id='owner')), 'module:'+module)
                        if index < 2:
                            self.assertEqual(graph.reference(analyzer, ast.parse('owner.__dict__', mode='eval').body), 'module:'+module)
                        defined = graph.modules[module]
                        self.assertIn(defined.path+'::f', graph.replaced_functions)
                        self.assertIn((module, '*'), graph.replaced_foundations)
                        if label != 'captured':
                            self.assertFalse(analyzer._foundation_available(module))
                            self.assertIs(graph._captured_source_target(module), defined)
                        for result in (refused, no_cache):
                            self.assertEqual(result.status, 1, result.to_dict())
                            self.assertFalse(result.verified)
                            caller = next(file for file in result.results if file.path == str(use))
                            self.assertTrue(any(row.rule == 'PAL240' for row in caller.diagnostics), result.to_dict())
                            self.assertFalse(caller.contracts[0].source_evidence.startswith('checked'))
                            scalar = next(file for file in result.results if file.path == str(independent))
                            self.assertEqual(scalar.diagnostics, [])
                            self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
                        caller = next(file for file in refused.results if file.path == str(use))
                        self.assertFalse(caller.cache_hit)
                        self.assertTrue(caller.binding_context)
                        self.assertTrue(next(file for file in refused.results if file.path == str(independent)).cache_hit)
                        self.assertEqual(caller.diagnostics, next(file.diagnostics for file in no_cache.results if file.path == str(use)))
                        output = case/'refused-output'
                        built = build_paths([case], root=case, output=output)
                        self.assertEqual(built.status, 1, built.to_dict())
                        self.assertIsNone(built.output)
                        self.assertFalse(output.exists())
                    finally:
                        writer.unlink()
                    restored = check()
                    self.assertEqual(restored.status, 0, restored.to_dict())
                    for file in restored.results:
                        self.assertEqual(file.contracts, next(old.contracts for old in cold.results if old.path == file.path))
                    self.assertTrue(all(file.cache_hit for file in check().results))

        for index, mutation in enumerate(('namespace=owner.__dict__\nnamespace["GenericAlias"]=None\n', 'owner.__dict__.clear()\n')):
            with self.subTest(native=index):
                case = self.root/('native-namespace-'+str(index))
                case.mkdir()
                core = case/'core.py'
                core.write_text(D06_SOURCE)
                independent = case/'independent.py'
                independent.write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value+1\n')
                (case/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
                def check(**kwargs):
                    return check_paths([case], root=case, **kwargs)
                cold = check()
                self.assertEqual(cold.status, 0, cold.to_dict())
                self.assertTrue(all(file.cache_hit for file in check().results))
                writer = case/'writer.py'
                writer.write_text('import types as owner\n'+mutation)
                capture = {}
                try:
                    refused, no_cache = check(_capture=capture), check(cache=False)
                    graph = capture['graph']
                    self.assertNotIn('types', graph.modules)
                    self.assertEqual(graph._module_writer_targets('types'), [])
                    self.assertEqual(graph.reference(graph.analyzers[str(writer)], ast.parse('owner.__dict__', mode='eval').body), 'module:types')
                    self.assertIn(('types', '*'), graph.replaced_foundations)
                    for result in (refused, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertFalse(result.verified)
                        self.assertFalse(next(c for file in result.results for c in file.contracts if c.name == 'make').source_evidence.startswith('checked'))
                        scalar = next(file for file in result.results if file.path == str(independent))
                        self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
                        self.assertEqual(scalar.diagnostics, [])
                    affected = next(file for file in refused.results if file.path == str(core))
                    self.assertFalse(affected.cache_hit)
                    self.assertTrue(affected.binding_context)
                    self.assertTrue(next(file for file in refused.results if file.path == str(independent)).cache_hit)
                    output = case/'refused-output'
                    built = build_paths([case], root=case, output=output)
                    self.assertEqual(built.status, 1, built.to_dict())
                    self.assertIsNone(built.output)
                    self.assertFalse(output.exists())
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                self.assertEqual(next(file.contracts for file in restored.results if file.path == str(core)),
                                 next(file.contracts for file in cold.results if file.path == str(core)))
                self.assertTrue(all(file.cache_hit for file in check().results))

        # Direct known builtin binding writes invalidate their native readers,
        # while an unrelated str annotation retains its original warm proof.
        self.assertTrue({'repr', 'hex'} <= COLLECTION_FOUNDATIONS['builtins'])
        self.assertTrue({'repr', 'hex'} <= _BUILTINS_WRITER_BINDINGS)
        builtin_writers = (
            ('plain', 'repr', 'import builtins\nbuiltins.repr=print\n'),
            ('alias', 'hex', 'import builtins as b\na=b\na.hex=print\n'),
            ('captured', 'repr', 'import builtins as b\ndef ordinary_writer():\n    b.repr=print\n'),
            ('typed', 'repr', 'import builtins as b\nb.repr:int=1\n'),
            ('augmented', 'hex', 'import builtins as b\nb.hex+=1\n'),
            ('deleted', 'repr', 'import builtins as b\ndel b.repr\n'),
        )
        for label, binding, writer_source in builtin_writers:
            with self.subTest(builtin_binding=label):
                case = self.root/('builtin-binding-'+label)
                case.mkdir()
                core = case/'core.py'
                core.write_text(D06_SOURCE)
                independent = case/'independent.py'
                scalar_source = 'from pyalamode import fun\n@fun\ndef identity(value:str)->str:\n    return value\n'
                independent.write_text(scalar_source)
                (case/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
                def check(**kwargs):
                    return check_paths([case], root=case, **kwargs)
                cold, warm, fresh = check(), check(), check(cache=False)
                for result in (cold, warm, fresh):
                    self.assertEqual(result.status, 0, result.to_dict())
                    for path in (core, independent):
                        self.assertEqual(next(file.contracts for file in result.results if file.path == str(path)),
                                         next(file.contracts for file in cold.results if file.path == str(path)))
                self.assertTrue(all(file.cache_hit for file in warm.results))
                writer = case/'writer.py'
                writer.write_text(writer_source)
                capture = {}
                try:
                    refused = check(_capture=capture)
                    refused_warm, no_cache = check(), check(cache=False)
                    graph = capture['graph']
                    self.assertIn(('builtins', binding), graph.replaced_foundations)
                    self.assertNotIn(('builtins', '*'), graph.replaced_foundations)
                    self.assertNotIn(('builtins', 'str'), graph.replaced_foundations)
                    self.assertIn('builtins.'+binding, graph.collection_dependency_replacements)
                    self.assertIn('builtins.'+binding, graph.builder_dependency_replacements)
                    analyzer = graph.analyzers[str(writer)]
                    target = next(node for node in ast.walk(analyzer.tree)
                                  if isinstance(node, ast.Attribute) and node.attr == binding)
                    self.assertTrue(graph._stable_module_object(analyzer, target.value, 'builtins'))
                    affected = next(file for file in refused.results if file.path == str(core))
                    self.assertFalse(affected.cache_hit)
                    self.assertTrue(affected.binding_context)
                    for result in (refused, refused_warm, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertFalse(result.verified)
                        file = next(file for file in result.results if file.path == str(core))
                        self.assertFalse(next(c for c in file.contracts if c.name == 'make').source_evidence.startswith('checked'))
                        self.assertEqual(file.diagnostics, affected.diagnostics)
                        self.assertEqual(file.contracts, affected.contracts)
                        scalar = next(file for file in result.results if file.path == str(independent))
                        self.assertTrue(scalar.verified)
                        self.assertEqual(scalar.diagnostics, [])
                        self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
                        self.assertEqual(scalar.contracts, next(file.contracts for file in cold.results if file.path == str(independent)))
                    self.assertTrue(next(file for file in refused.results if file.path == str(independent)).cache_hit)
                    self.assertTrue(next(file for file in refused_warm.results if file.path == str(core)).cache_hit)
                    output = case/'refused-output'
                    built = build_paths([case], root=case, output=output)
                    self.assertEqual(built.status, 1, built.to_dict())
                    self.assertIsNone(built.output)
                    self.assertFalse(output.exists())
                    self.assertEqual(writer.read_text(), writer_source)
                    self.assertEqual(core.read_text(), D06_SOURCE)
                    self.assertEqual(independent.read_text(), scalar_source)
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                for path in (core, independent):
                    self.assertEqual(next(file.contracts for file in restored.results if file.path == str(path)),
                                     next(file.contracts for file in cold.results if file.path == str(path)))
                self.assertTrue(all(file.cache_hit for file in check().results))

        builtin_namespaces = (
            ('alias-item', 'import builtins as owner\nnamespace=owner.__dict__\nnamespace["repr"]=None\n', 'namespace'),
            ('clear', 'import builtins as owner\nowner.__dict__.clear()\n', '__dict__'),
            ('dynamic-item', 'import builtins as owner\nnamespace=owner.__dict__\nnamespace[key]=None\n', 'namespace'),
            ('update', 'import builtins as owner\nnamespace=owner.__dict__\nnamespace.update({"repr":None})\n', 'namespace'),
            ('setattr', 'import builtins as owner\nsetattr(owner,"repr",None)\n', None),
            ('dynamic-setattr', 'import builtins as owner\nsetattr(owner,name,None)\n', None),
            ('private', 'import builtins as owner\nowner._helper=None\n', None),
            ('uncatalog', 'import builtins as owner\nowner.not_a_known_native_binding=None\n', None),
            ('rebound', 'import builtins as b\nowner=b\nowner=object()\nowner.repr=None\n', 'owner'),
            ('parameter', 'import builtins as owner\ndef write(owner):\n    owner.repr=None\n', 'owner'),
        )
        for label, writer_source, uncertain in builtin_namespaces:
            with self.subTest(builtin_namespace=label):
                case = self.root/('builtin-namespace-'+label)
                case.mkdir()
                core = case/'core.py'
                core.write_text(D06_SOURCE)
                independent = case/'independent.py'
                independent.write_text('from pyalamode import fun\n@fun\ndef identity(value:str)->str:\n    return value\n')
                (case/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
                def check(**kwargs):
                    return check_paths([case], root=case, **kwargs)
                cold, warm = check(), check()
                self.assertEqual(cold.status, 0, cold.to_dict())
                self.assertTrue(all(file.cache_hit for file in warm.results))
                writer = case/'writer.py'
                writer.write_text(writer_source)
                capture = {}
                try:
                    refused = check(_capture=capture)
                    refused_warm, no_cache = check(), check(cache=False)
                    graph = capture['graph']
                    self.assertIn(('builtins', '*'), graph.replaced_foundations)
                    analyzer = graph.analyzers[str(writer)]
                    if uncertain == '__dict__':
                        proof_node = next(node for node in ast.walk(analyzer.tree)
                                          if isinstance(node, ast.Attribute) and node.attr == '__dict__')
                    elif uncertain is not None:
                        proof_node = next(node for node in ast.walk(analyzer.tree)
                                          if isinstance(node, ast.Name) and node.id == uncertain and isinstance(node.ctx, ast.Load))
                    if uncertain is not None:
                        self.assertFalse(graph._stable_module_object(analyzer, proof_node, 'builtins'))
                    affected = next(file for file in refused.results if file.path == str(core))
                    self.assertFalse(affected.cache_hit)
                    self.assertTrue(affected.binding_context)
                    for result in (refused, refused_warm, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertFalse(result.verified)
                        file = next(file for file in result.results if file.path == str(core))
                        self.assertFalse(next(c for c in file.contracts if c.name == 'make').source_evidence.startswith('checked'))
                        self.assertEqual(file.diagnostics, affected.diagnostics)
                        scalar = next(file for file in result.results if file.path == str(independent))
                        self.assertFalse(scalar.verified)
                        self.assertFalse(scalar.contracts[0].source_evidence.startswith('checked'))
                    self.assertTrue(next(file for file in refused_warm.results if file.path == str(core)).cache_hit)
                    output = case/'refused-output'
                    built = build_paths([case], root=case, output=output)
                    self.assertEqual(built.status, 1, built.to_dict())
                    self.assertIsNone(built.output)
                    self.assertFalse(output.exists())
                    self.assertEqual(writer.read_text(), writer_source)
                    self.assertEqual(core.read_text(), D06_SOURCE)
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                for path in (core, independent):
                    self.assertEqual(next(file.contracts for file in restored.results if file.path == str(path)),
                                     next(file.contracts for file in cold.results if file.path == str(path)))
                self.assertTrue(all(file.cache_hit for file in check().results))

        builtin_shadow = self.root/'builtin-source-shadow'
        builtin_shadow.mkdir()
        defined = builtin_shadow/'builtins.py'
        defined.write_text('# mode: fun\ndef repr()->None:\n    return None\n')
        use = builtin_shadow/'use.py'
        use.write_text('# mode: fun\nimport builtins as owner\ndef use()->None:\n    return owner.repr()\n')
        independent = builtin_shadow/'independent.py'
        independent.write_text('# mode: fun\ndef independent()->None:\n    return None\n')
        cold = check_paths([builtin_shadow], root=builtin_shadow)
        self.assertEqual(cold.status, 0, cold.to_dict())
        self.assertTrue(all(file.cache_hit for file in check_paths([builtin_shadow], root=builtin_shadow).results))
        writer = builtin_shadow/'writer.py'
        writer.write_text('import builtins as owner\nowner.repr=None\n')
        capture = {}
        try:
            refused = check_paths([builtin_shadow], root=builtin_shadow, _capture=capture)
            no_cache = check_paths([builtin_shadow], root=builtin_shadow, cache=False)
            graph = capture['graph']
            analyzer = graph.analyzers[str(writer)]
            self.assertIs(graph._captured_source_target('builtins'), graph.modules['builtins'])
            self.assertFalse(analyzer._foundation_available('builtins'))
            target = next(node for node in ast.walk(analyzer.tree) if isinstance(node, ast.Attribute) and node.attr == 'repr')
            self.assertFalse(graph._stable_module_object(analyzer, target.value, 'builtins'))
            self.assertIn(str(defined)+'::repr', graph.replaced_functions)
            self.assertIn(('builtins', '*'), graph.replaced_foundations)
            self.assertNotIn(('builtins', 'repr'), graph.replaced_foundations)
            for result in (refused, no_cache):
                self.assertEqual(result.status, 1, result.to_dict())
                self.assertFalse(result.verified)
                caller = next(file for file in result.results if file.path == str(use))
                self.assertTrue(any(row.rule == 'PAL240' for row in caller.diagnostics), result.to_dict())
                self.assertFalse(caller.contracts[0].source_evidence.startswith('checked'))
            output = builtin_shadow/'refused-output'
            built = build_paths([builtin_shadow], root=builtin_shadow, output=output)
            self.assertEqual(built.status, 1, built.to_dict())
            self.assertIsNone(built.output)
            self.assertFalse(output.exists())
            self.assertEqual(writer.read_text(), 'import builtins as owner\nowner.repr=None\n')
        finally:
            writer.unlink()
        restored = check_paths([builtin_shadow], root=builtin_shadow)
        self.assertEqual(restored.status, 0, restored.to_dict())
        for file in restored.results:
            self.assertEqual(file.contracts, next(old.contracts for old in cold.results if old.path == file.path))
        self.assertTrue(all(file.cache_hit for file in check_paths([builtin_shadow], root=builtin_shadow).results))

        function_case = self.root/'function-dictionary'
        function_case.mkdir()
        defined = function_case/'defined.py'
        defined.write_text('# mode: fun\ndef f(value:int)->int:\n    return value+1\n')
        use = function_case/'use.py'
        use.write_text('# mode: fun\nfrom defined import f\ndef use(value:int)->int:\n    return f(value)\n')
        independent = function_case/'independent.py'
        independent.write_text('# mode: fun\ndef independent(value:int)->int:\n    return value+1\n')
        cold = check_paths([function_case], root=function_case)
        self.assertEqual(cold.status, 0, cold.to_dict())
        self.assertTrue(all(file.cache_hit for file in check_paths([function_case], root=function_case).results))
        writer = function_case/'writer.py'
        writer.write_text('from defined import f\nnamespace=f.__dict__\nnamespace["tag"]=None\n')
        capture = {}
        try:
            refused = check_paths([function_case], root=function_case, _capture=capture)
            self.assertEqual(refused.status, 1, refused.to_dict())
            graph = capture['graph']
            self.assertEqual(graph.reference(graph.analyzers[str(writer)], ast.Name(id='namespace')), str(defined)+'::f')
            self.assertIn(str(defined)+'::f', graph.replaced_functions)
            self.assertNotIn(('pyalamode', '*'), graph.replaced_foundations)
            scalar = next(file for file in refused.results if file.path == str(independent))
            self.assertTrue(scalar.cache_hit)
            self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
            output = function_case/'refused-output'
            built = build_paths([function_case], root=function_case, output=output)
            self.assertEqual(built.status, 1, built.to_dict())
            self.assertIsNone(built.output)
            self.assertFalse(output.exists())
        finally:
            writer.unlink()
        restored = check_paths([function_case], root=function_case)
        self.assertEqual(restored.status, 0, restored.to_dict())
        self.assertEqual(next(file.contracts for file in restored.results if file.path == str(use)),
                         next(file.contracts for file in cold.results if file.path == str(use)))
        self.assertTrue(all(file.cache_hit for file in check_paths([function_case], root=function_case).results))
        unknown_path = self.root/'unknown-namespace.py'
        unknown_source = 'namespace=getattr(unknown,"__dict__")\nnamespace["f"]=None\n'
        unknown_graph = SourceGraph({str(unknown_path):unknown_source}, self.root, False, {})
        self.assertIsNone(unknown_graph.reference(unknown_graph.analyzers[str(unknown_path)], ast.Name(id='namespace')))
        controls = self.root/'controls'
        controls.mkdir()
        core = controls/'core.py'
        core.write_text('from pyalamode import fun, vector_build\n@fun\ndef unknown(vector_build:int)->int:\n    return vector_build(1)\n')
        (controls/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n')
        writer = controls/'writer.py'
        writer.write_text(writers[0][1])
        refused = check_paths([controls], root=controls, cache=False)
        file = next(file for file in refused.results if file.path == str(core))
        self.assertIn('PAL230', [row.rule for row in file.diagnostics if row.line == 4])
        self.assertNotIn('PAL240', [row.rule for row in file.diagnostics if row.line == 4])
        writer.write_text('import pyalamode as pal\npal.fun=None\n')
        self.assertIn('PAL120', [row.rule for file in check_paths([controls], root=controls, cache=False).results for row in file.diagnostics])
        (controls/'pyalamode.py').write_text('def fun(value):return value\n')
        shadow_capture = {}
        shadow = check_paths([controls], root=controls, cache=False, _capture=shadow_capture)
        self.assertEqual(shadow.status, 1, shadow.to_dict())
        self.assertFalse(shadow_capture['graph'].analyzers[str(core)]._foundation_available('pyalamode'))
        self.assertEqual(self.source.read_text(), SOURCE)

    def test_check_build_do_not_execute_source_and_guards(self):
        sentinel = self.root/'executed'
        (self.root/'shell.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\n')
        for mode in ('off', 'exports', 'debug'):
            self.policy.write_text('[tool.pyalamode]\nbuilders=true\nboundary_guards="'+mode+'"\n'+('guarded_exports=["core:assemble"]\n' if mode != 'off' else ''))
            output = self.root/('built-'+mode)
            result = build_paths([self.source, self.root/"shell.py"], root=self.root, output=output)
            self.assertEqual(result.status, 0, result.to_dict())
            self.assertTrue(output.is_dir())
            self.assertFalse(sentinel.exists())
            if mode == 'debug':
                self.assertNotIn('VectorBuilder', {kind for row in result.debug_coverage for kind in row['parameters'].values()})

    def test_cli_json_status_and_no_output(self):
        self.policy.write_text('[tool.pyalamode]\nbuilders=false\n')
        completed = subprocess.run([sys.executable,'-m','pyalamode','build',str(self.root),'--root',str(self.root),'--output',str(self.root/'out'),'--json'],capture_output=True,text=True)
        self.assertEqual(completed.returncode, 1, completed.stderr)
        data = json.loads(completed.stdout)
        self.assertIsNone(data['output'])
        self.assertTrue(any(row['rule']=='PAL380' for file in data['files'] for row in file['diagnostics']))
        self.assertFalse((self.root/'out').exists())


class BuilderEvidenceTests(unittest.TestCase):
    def test_consumer_facade_writer_reports_actual_callee_and_retains_scalar(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            producer, site, consumer = (base/name for name in ('producer', 'site', 'consumer'))
            for path in (producer, site, consumer):
                path.mkdir()
            package = producer/'qbuilder'
            package.mkdir()
            (package/'__init__.py').write_text('# mode: fun\n')
            (package/'core.py').write_text(D06_SOURCE)
            (producer/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\nboundary_guards="off"\n'
                '[tool.pyalamode.distribution]\nschema=1\nname="checked-builder"\nversion="1.0.0"\n'
                'packages=["qbuilder"]\nexports=["qbuilder.core:make"]\n')
            wheel_path = base/'out/checked_builder-1.0.0-py3-none-any.whl'
            built = build_paths([producer], root=producer, artifact='wheel', output=wheel_path)
            self.assertEqual(built.status, 0, built.to_dict())
            wheel_bytes = wheel_path.read_bytes()
            with zipfile.ZipFile(wheel_path) as wheel:
                wheel.extractall(site)
            def installed_map():
                return {path.relative_to(site).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in site.rglob('*') if path.is_file()}
            installed_before = installed_map()
            (consumer/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n'
                '[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="checked-builder"\nversion="1.0.0"\npackages=["qbuilder"]\n')
            use = consumer/'use.py'
            use.write_text('from pyalamode import fun, Vector\nfrom qbuilder.core import make\n@fun\n'
                           'def total(source:Vector[int])->Vector[int]:\n    return make(source)\n')
            valid = consumer/'valid.py'
            valid.write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value+1\n')
            with patch.object(sys, 'path', [str(site), *sys.path]):
                def check(**kwargs):
                    return check_paths([consumer], root=consumer, **kwargs)
                cold, warm, fresh = check(), check(), check(cache=False)
                for result in (cold, warm, fresh):
                    self.assertEqual(result.status, 0, result.to_dict())
                    receipt = result.checked_dependencies[0]
                    self.assertEqual((receipt['input_status'], receipt['source_status'], receipt['complete'], receipt['verified']),
                                     (0, 0, True, True))
                    self.assertEqual([row['selector'] for row in receipt['exports']], ['qbuilder.core:make'])
                    for path in (use, valid):
                        self.assertEqual(next(file.contracts for file in result.results if file.path == str(path)),
                                         next(file.contracts for file in cold.results if file.path == str(path)))
                self.assertTrue(all(file.cache_hit for file in warm.results))
                prior = base/'accepted-output'
                successful_build = build_paths([consumer], root=consumer, output=prior)
                self.assertEqual(successful_build.status, 0, successful_build.to_dict())
                prior_bytes = {path.relative_to(prior).as_posix(): path.read_bytes() for path in prior.rglob('*') if path.is_file()}
                writer = consumer/'writer.py'
                writer_source = 'import pyalamode as pal\npal.vector_build = lambda callback: None\n'
                writer.write_text(writer_source)
                capture = {}
                try:
                    refused = check(_capture=capture)
                    refused_warm, no_cache = check(), check(cache=False)
                    for result in (refused, refused_warm, no_cache):
                        self.assertEqual(result.status, 1, result.to_dict())
                        self.assertEqual(result.tooling, [])
                        self.assertFalse(result.verified)
                        receipt = result.checked_dependencies[0]
                        self.assertEqual((receipt['admission'], receipt['input_status'], receipt['source_status'],
                                          receipt['complete'], receipt['verified'], receipt['exports']),
                                         ('current', 0, 1, True, False, []))
                        upstream = [row.dependency_context['upstream'] for file in result.results
                                    for row in file.diagnostics if row.rule == 'PAL371']
                        self.assertTrue(upstream, result.to_dict())
                        self.assertTrue(all(row == {'rule':'PAL240', 'selector':'qbuilder.core:make'} for row in upstream), upstream)
                        scalar = next(file for file in result.results if file.path == str(valid))
                        self.assertEqual(scalar.diagnostics, [])
                        self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
                        self.assertEqual(scalar.contracts, next(file.contracts for file in cold.results if file.path == str(valid)))
                    self.assertTrue(next(file for file in refused.results if file.path == str(valid)).cache_hit)
                    core = capture['graph'].modules['qbuilder.core'].result
                    self.assertNotIn('PAL120', [row.rule for row in core.diagnostics])
                    self.assertNotIn('PAL130', [row.rule for row in core.diagnostics])
                    target = [row.rule for row in core.diagnostics if (row.line, row.column) == (13, 12)]
                    self.assertIn('PAL240', target)
                    self.assertNotIn('PAL230', target)
                    output = base/'refused-output'
                    refused_build = build_paths([consumer], root=consumer, output=output)
                    self.assertEqual(refused_build.status, 1, refused_build.to_dict())
                    self.assertIsNone(refused_build.output)
                    self.assertFalse(output.exists())
                    self.assertEqual(prior_bytes, {path.relative_to(prior).as_posix(): path.read_bytes()
                                                  for path in prior.rglob('*') if path.is_file()})
                    self.assertEqual(installed_map(), installed_before)
                    self.assertEqual(wheel_path.read_bytes(), wheel_bytes)
                    self.assertEqual(writer.read_text(), writer_source)
                finally:
                    writer.unlink()
                restored = check()
                self.assertEqual(restored.status, 0, restored.to_dict())
                self.assertEqual([row['selector'] for row in restored.checked_dependencies[0]['exports']], ['qbuilder.core:make'])
                self.assertEqual(installed_map(), installed_before)
                for mutation in ('namespace=owner.__dict__\nnamespace["make"]=None\n', 'owner.__dict__.clear()\n'):
                    with self.subTest(installed_namespace=mutation):
                        self.assertEqual(check().status, 0)
                        writer.write_text('import qbuilder.core as owner\n'+mutation)
                        capture = {}
                        try:
                            refused, no_cache = check(_capture=capture), check(cache=False)
                            graph = capture['graph']
                            analyzer = graph.analyzers[str(writer)]
                            self.assertEqual(graph.reference(analyzer, ast.parse('owner.__dict__', mode='eval').body), 'module:qbuilder.core')
                            self.assertIn(('qbuilder.core', '*'), graph.replaced_foundations)
                            self.assertIn(graph.modules['qbuilder.core'].path+'::make', graph.replaced_functions)
                            for result in (refused, no_cache):
                                self.assertEqual(result.status, 1, result.to_dict())
                                self.assertEqual(result.tooling, [])
                                self.assertFalse(result.verified)
                                receipt = result.checked_dependencies[0]
                                self.assertEqual((receipt['admission'], receipt['input_status'], receipt['source_status'],
                                                  receipt['complete'], receipt['verified'], receipt['exports']),
                                                 ('current', 0, 1, True, False, []))
                                upstream = [row.dependency_context['upstream'] for file in result.results
                                            for row in file.diagnostics if row.rule == 'PAL371']
                                self.assertTrue(upstream, result.to_dict())
                                self.assertTrue(all(row and row['rule'] == 'PAL240' and row['selector'] in
                                    {'qbuilder.core:double', 'qbuilder.core:large', 'qbuilder.core:make', 'qbuilder.core:make.fill'}
                                    for row in upstream), upstream)
                                scalar = next(file for file in result.results if file.path == str(valid))
                                self.assertEqual(scalar.diagnostics, [])
                                self.assertTrue(scalar.contracts[0].source_evidence.startswith('checked'))
                                self.assertEqual(scalar.contracts, next(file.contracts for file in cold.results if file.path == str(valid)))
                            self.assertTrue(next(file for file in refused.results if file.path == str(valid)).cache_hit)
                            refused_build = build_paths([consumer], root=consumer, output=output)
                            self.assertEqual(refused_build.status, 1, refused_build.to_dict())
                            self.assertIsNone(refused_build.output)
                            self.assertFalse(output.exists())
                            self.assertEqual(installed_map(), installed_before)
                            self.assertEqual(wheel_path.read_bytes(), wheel_bytes)
                            self.assertEqual(prior_bytes, {path.relative_to(prior).as_posix(): path.read_bytes()
                                                          for path in prior.rglob('*') if path.is_file()})
                        finally:
                            writer.unlink()
                        restored = check()
                        self.assertEqual(restored.status, 0, restored.to_dict())
                        self.assertEqual([row['selector'] for row in restored.checked_dependencies[0]['exports']], ['qbuilder.core:make'])

    def test_current_consumer_policy_and_intrinsic_scope_relation(self):
        import base64
        import csv
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp).resolve();producer=base/'producer';site=base/'site';consumer=base/'consumer'
            for path in (producer,site,consumer):path.mkdir()
            (producer/'bulk').mkdir();(producer/'bulk/__init__.py').write_text('# mode: fun\n');(producer/'bulk/core.py').write_text(SOURCE)
            (producer/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n[tool.pyalamode.distribution]\nschema=1\nname="bulk"\nversion="1.0.0"\npackages=["bulk"]\nexports=["bulk.core:assemble"]\n')
            result=build_paths([producer],root=producer,artifact='wheel',output=base/'out/bulk-1.0.0-py3-none-any.whl')
            self.assertEqual(result.status,0,result.to_dict())
            with zipfile.ZipFile(result.output) as wheel:wheel.extractall(site)
            dependency='[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="bulk"\nversion="1.0.0"\npackages=["bulk"]\n'
            policy=consumer/'pyproject.toml';policy.write_text('[tool.pyalamode]\nbuilders=true\n'+dependency)
            (consumer/'use.py').write_text('from pyalamode import Vector, fun\nfrom bulk.core import assemble\n@fun\ndef use(values:Vector[int])->Vector[int]:\n    return assemble(values)\n')
            with patch.object(sys,'path',[str(site),*sys.path]):
                accepted=check_paths([consumer],root=consumer,cache=False)
                self.assertEqual(accepted.status,0,accepted.to_dict())
                self.assertEqual(accepted.checked_dependencies[0]['input_status'],0)
                policy.write_text(dependency)
                refused=check_paths([consumer],root=consumer,cache=False)
                self.assertEqual(refused.status,1,refused.to_dict())
                receipt=refused.checked_dependencies[0]
                self.assertEqual((receipt['input_status'],receipt['source_status']),(0,1))
                upstream=[row.dependency_context['upstream'] for file in refused.results for row in file.diagnostics if row.rule=='PAL371']
                self.assertTrue(any(row and row['rule']=='PAL380' for row in upstream),upstream)
                info=site/'bulk-1.0.0.dist-info';evidence=info/'pyalamode/evidence.json'
                original=json.loads(evidence.read_text())
                def replace(value):
                    value['sha256']=d.digest(value['payload']);evidence.write_bytes(d.canonical(value))
                    with (info/'RECORD').open('w',newline='') as stream:
                        writer=csv.writer(stream,lineterminator='\n')
                        for path in sorted(site.rglob('*')):
                            if path.is_file() and path!=info/'RECORD':
                                raw=path.read_bytes();writer.writerow([path.relative_to(site).as_posix(),'sha256='+base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip('='),str(len(raw))])
                        writer.writerow([info.name+'/RECORD','',''])
                different=copy.deepcopy(original);different['payload']['producer']['builder_version']='pyalamode.builders-future';replace(different)
                incompatible=check_paths([consumer],root=consumer,cache=False)
                self.assertEqual(incompatible.status,1,incompatible.to_dict())
                self.assertEqual(incompatible.checked_dependencies[0]['admission'],'incompatible')
                self.assertEqual(incompatible.checked_dependencies[0]['input_status'],1)
                self.assertIsNone(incompatible.checked_dependencies[0]['source_status'])
                self.assertTrue(any(row.rule=='PAL370' for file in incompatible.results for row in file.diagnostics))
                malformed=copy.deepcopy(original);malformed['payload']['exports'][0]['contract']['builder_scopes'][0]['callback_line']+=1;replace(malformed)
                corrupted=check_paths([consumer],root=consumer,cache=False)
                self.assertEqual(corrupted.status,2,corrupted.to_dict())
                self.assertTrue(any('builder_scopes' in row.reason for row in corrupted.tooling))

    def test_genuine_m11_history_retains_raw_ids_and_m10_predecessors(self):
        archive = json.loads((Path(__file__).parent/'fixtures/m12/legacy-m11.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            for name, raw in archive['files'].items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw.encode())
            raw = (root/'.pyalamode/baseline.json').read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), 'f42d456075893403b8b7875b9b18c3d434891dbbba017b8c52cd8ebb419dfe71')
            reference = m.load_reference(root,".pyalamode/baseline.json")
            self.assertEqual(reference['state']['schema'], 2)
            self.assertEqual(len(reference['state']['inputs']['product_artifacts']), 22)
            self.assertEqual(reference['record']['id'], 'f47887db0984005546d16cb8734a2a8e08e15625ec065aded5a96f9de88be3e3')
            _, state, report, _ = observe(root)
            self.assertEqual(state['schema'], 5)
            self.assertEqual(len(state['inputs']['product_artifacts']), 28)
            self.assertEqual(state['strict_status'], 1)
            self.assertEqual(len(report['comparison']['retained_findings']), 2)
            self.assertEqual(report['comparison']['new_findings'], [])
            with self.assertRaises(m.MigrationError):m.normalize_state(reference['state'])
            for name, text in archive['files'].items():self.assertEqual((root/name).read_bytes(),text.encode())
            for mutation in ('missing','extra','checker','hybrid'):
                bad=copy.deepcopy(reference['state'])
                if mutation=='missing':bad['inputs']['product_artifacts'].pop('checker.py')
                elif mutation=='extra':bad['inputs']['product_artifacts']['invented.py']='a'*64
                elif mutation=='checker':bad['checker']='invented'
                else:bad['policy']['builders']=True
                with self.subTest(mutation=mutation),self.assertRaises(m.MigrationError):m._state(bad,retained=True)

    def test_builders_policy_weakening_is_independent_of_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'core.py').write_text('from pyalamode import fun\n@fun\ndef same(value:int)->int:\n    return value\n')
            policy=root/'pyproject.toml';policy.write_text('[tool.pyalamode]\nbuilders=false\n')
            _, state, _, _=observe(root,bootstrap=True)
            m.write_baseline(root,state,owner='development',rationale='independent policy control',prepublish=lambda:None)
            policy.write_text('[tool.pyalamode]\nbuilders=true\n[tool.pyalamode.migration]\nschema=1\nreject_policy_weakening=true\n')
            _, current, report, _=observe(root)
            self.assertEqual(current['strict_status'],0)
            self.assertEqual(report['status'],1)
            self.assertEqual(report['comparison']['policy_weakening'][0]['reason'],'builders-enabled')
            self.assertIn('PAL367',[row['rule'] for row in report['gates']['diagnostics']])

    def test_current_wheel_closed_builder_rows_and_old_finite_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'bulk').mkdir();(root/'bulk/__init__.py').write_text('# mode: fun\n');(root/'bulk/core.py').write_text(SOURCE)
            (root/'pyproject.toml').write_text('[tool.pyalamode]\nbuilders=true\n[tool.pyalamode.distribution]\nschema=1\nname="bulk"\nversion="1.0.0"\npackages=["bulk"]\nexports=["bulk.core:assemble"]\n')
            output=root/'out/bulk-1.0.0-py3-none-any.whl'
            result=build_paths([root],root=root,artifact='wheel',output=output)
            self.assertEqual(result.status,0,result.to_dict())
            with zipfile.ZipFile(output) as wheel:data=json.loads(wheel.read('bulk-1.0.0.dist-info/pyalamode/evidence.json'))
            self.assertEqual(data['schema'],4)
            self.assertEqual(data['payload']['producer']['builder_version'],'pyalamode.builders-v1')
            self.assertEqual(len(data['payload']['producer']['product_artifacts']),28)
            d.validate_evidence(data)
            for mutate in ('row','scope','missing','hybrid','builder-type','builder-size'):
                bad=copy.deepcopy(data)
                if mutate=='row':bad['payload']['exports'][0]['contract']['operation_contracts'][0]['effects']=['State']
                elif mutate=='scope':bad['payload']['exports'][0]['contract']['builder_scopes'][0]['operations']=['append']
                elif mutate=='missing':bad['payload']['producer'].pop('builder_version')
                elif mutate=='hybrid':bad['schema']=1
                elif mutate=='builder-type':bad['payload']['producer']['builder_version']=True
                else:bad['payload']['producer']['builder_version']='x'*129
                bad['sha256']=d.digest(bad['payload'])
                with self.subTest(mutate=mutate),self.assertRaises(d.DistributionError):d.validate_evidence(bad)
            # An actual old profile requires old source contracts; never relabel a builder wheel.
            (root/'bulk/core.py').write_text('from pyalamode import fun\n@fun\ndef assemble(value:int)->int:\n    return value\n')
            plain=build_paths([root],root=root,artifact='wheel',output=root/'other/bulk-1.0.0-py3-none-any.whl')
            self.assertEqual(plain.status,0,plain.to_dict())
            with zipfile.ZipFile(plain.output) as wheel:old=json.loads(wheel.read('bulk-1.0.0.dist-info/pyalamode/evidence.json'))
            old['schema']=1;producer=old['payload']['producer'];producer.pop('builder_version');producer.pop('task_version');producer.pop('syntax_version');producer.pop('source_map_schema')
            # Genuine M11 evidence ships variants.py and has no tail_recursive contract field.
            artifacts=producer['product_artifacts'];artifacts['variants.py']=artifacts.pop('sums.py')
            producer['product_artifacts']={k:v for k,v in artifacts.items() if k in d.M11_PRODUCTS}
            for row in old['payload']['exports']:row['contract'].pop('builder_scopes');row['contract'].pop('task_scopes');row['contract'].pop('tail_recursive')
            for row in old['payload']['inputs']['sources'].values():
                row.pop('edition');row.pop('normalized_sha256')
            for row in old['payload']['modules']:
                for key in ('edition','normalized_sha256','translator','lowered_path','lowered_sha256','map_path','map_sha256'):row.pop(key)
            old['payload']['guards'].pop('source_maps')
            old['sha256']=d.digest(old['payload'])
            d.validate_evidence(old)
            d._export(old['payload']['exports'][0],historical=None)
            with self.assertRaises(d.DistributionError):d._export(old['payload']['exports'][0],historical=False)
            old['payload']['producer']['checker']='valid different historical label'
            old['sha256']=d.digest(old['payload'])
            d.validate_evidence(old)


if __name__ == '__main__':
    unittest.main()
