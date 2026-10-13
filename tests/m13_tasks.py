"""Focused source and exact metadata checks for the characterized task API.

Application fixtures are checked/built as source, never imported. Ordinary
runtime mechanics and independent literal observations have separate owners.
"""
import base64
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from pyalamode import distribution as d, migration as m
from pyalamode.cli import explain_symbol
from pyalamode.migration_views import observe
from pyalamode.model import CHECKER_VERSION, OPERATION_VERSION, foundation_identities
from pyalamode.project import build_paths, check_paths, load_policy
from pyalamode.task_contracts import (TASK_VERSION, operation_catalog,
                                     operation_contract, setup_catalog)


PREFIX = '''from pyalamode import (Vector, Task, TaskCapability, Clock, ClockCapability,
                       effects, fun, task_map, task_map_with, borrow)
'''
PURE = PREFIX + '''@fun
def double(value: int) -> int:
    return value * 2
@effects(Task)
def make(tasks: TaskCapability, values: Vector[int]) -> Vector[int]:
    return task_map(tasks, double, values)
'''
EXTERNAL = PREFIX + '''@effects(Clock)
def stamp(view: ClockCapability, value: int) -> tuple[int, int]:
    return (value, view.now_ns())
@effects(Task, Clock)
def make(tasks: TaskCapability, clock: ClockCapability,
         values: Vector[int]) -> Vector[tuple[int, int]]:
    return task_map_with(tasks, clock, stamp, values)
'''
SCOPE_KEYS = set('operation line end_line message_schema result_schema callback_schema callback_targets capability ordering cancellation failure lifetime'.split())


class TaskSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'core.py'
        self.policy = self.root / 'pyproject.toml'
        self.source.write_text(PURE)
        self.policy.write_text('[tool.pyalamode]\ntasks=true\n')

    def tearDown(self):
        self.temp.cleanup()

    def check(self, source=None, **kwargs):
        if source is not None:
            self.source.write_text(source)
        return check_paths([self.root], root=self.root, **kwargs)

    def contract(self, result, name='make'):
        return next(c for f in result.results for c in f.contracts if c.name == name)

    def refused(self, source, rule):
        result = self.check(source, cache=False)
        self.assertEqual(result.status, 1, result.to_dict())
        self.assertIn(rule, [x.rule for f in result.results for x in f.diagnostics])
        return result

    def test_default_off_and_explicit_false_refuse_at_operation_call(self):
        for text in ('[tool.pyalamode]\n', '[tool.pyalamode]\ntasks=false\n'):
            self.policy.write_text(text)
            result = self.check(cache=False)
            disabled = [x for f in result.results for x in f.diagnostics if x.rule == 'PAL382']
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertEqual([(x.line, x.column) for x in disabled], [(8, 12)])
            self.assertEqual(self.contract(result).task_scopes, [])

    def test_policy_requires_exact_boolean_and_retains_no_output(self):
        for value in ('1', '"true"', '[]'):
            self.policy.write_text('[tool.pyalamode]\ntasks=' + value + '\n')
            output = self.root / 'build'
            result = build_paths([self.root], root=self.root, output=output)
            self.assertEqual(result.status, 2, result.to_dict())
            self.assertFalse(output.exists())

    def test_task_declaration_does_not_require_invocation_permission(self):
        self.policy.write_text('[tool.pyalamode]\n')
        result = self.check(PREFIX + '@effects(Task)\ndef make(tasks:TaskCapability,value:int)->int:\n    return value\n', cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        contract = self.contract(result)
        self.assertEqual(contract.effect_bound, ['Task'])
        self.assertEqual(contract.required_effects, [])
        self.assertEqual(contract.capability_parameters['tasks']['operations'], ['task_map', 'task_map_with'])

    def test_plain_task_scope_has_closed_schema_and_callback_identity(self):
        result = self.check(cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        contract = self.contract(result)
        self.assertEqual(contract.required_effects, ['Task'])
        self.assertEqual(len(contract.task_scopes), 1)
        row = contract.task_scopes[0]
        self.assertEqual(set(row), SCOPE_KEYS)
        self.assertEqual((row['operation'], row['message_schema'], row['result_schema'], row['callback_schema'], row['capability']),
                         ('pyalamode.tasks.task_map', 'int', 'int', 'Callable[[int], int]', None))
        self.assertEqual(row['callback_targets'], [str(self.source) + '::double'])
        self.assertEqual((row['line'], row['end_line']), (8, 8))
        self.assertTrue(set(('RuntimeError', 'ValueError', 'RecursionError')) <= set(contract.failures))
        self.assertEqual(result.to_dict()['task_operation_version'], TASK_VERSION)
        self.assertEqual(len(result.to_dict()['task_catalog']), 2)

    def test_injected_external_family_and_scope_are_retained(self):
        result = self.check(EXTERNAL, cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        contract = self.contract(result)
        self.assertEqual(contract.required_effects, ['Clock', 'Task'])
        scope = contract.task_scopes[0]
        self.assertEqual(scope['capability'], 'ClockCapability')
        self.assertEqual(scope['callback_schema'], 'Effectful[[ClockCapability, int], tuple[int, int], Clock]')
        self.assertEqual(scope['callback_targets'], [str(self.source) + '::stamp'])

    def test_declared_callback_upper_bound_survives_empty_body(self):
        result = self.check(PURE.replace('@fun', '@effects(Clock)').replace('@effects(Task)\ndef make', '@effects(Task, Clock)\ndef make'), cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual(self.contract(result).required_effects, ['Clock', 'Task'])
        self.assertEqual(self.contract(result).task_scopes[0]['callback_schema'], 'Effectful[[int], int, Clock]')

    def test_missing_task_or_callback_effect_is_refused(self):
        self.refused(PURE.replace('@effects(Task)', '@fun'), 'PAL310')
        self.refused(PURE.replace('@fun', '@effects(Clock)'), 'PAL310')
        self.refused(EXTERNAL.replace('@effects(Task, Clock)', '@effects(Task)'), 'PAL310')

    def test_nested_stable_capture_is_admitted(self):
        source = PREFIX + '''@effects(Task)
def make(tasks:TaskCapability,values:Vector[int],fee:int)->Vector[int]:
    def quote(value:int)->int:
        return value+fee
    return task_map(tasks,quote,values)
'''
        result = self.check(source, cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual(self.contract(result).task_scopes[0]['callback_targets'], [str(self.source) + '::make.quote'])

    def test_mutable_and_capability_captures_are_refused(self):
        changing = PREFIX + '''fee=2
fee=3
@effects(Task)
def make(tasks:TaskCapability,values:Vector[int])->Vector[int]:
    def quote(value:int)->int:
        return value+fee
    return task_map(tasks,quote,values)
'''
        self.refused(changing, 'PAL240')
        capturing = EXTERNAL.replace('def stamp(view: ClockCapability, value: int)', 'def stamp(view: ClockCapability, value: int)')
        # Explicit external slots cannot be replaced by a captured provider.
        capturing = PREFIX + '''@effects(Task,Clock)
def make(tasks:TaskCapability,clock:ClockCapability,values:Vector[int])->Vector[int]:
    @effects(Clock)
    def stamp(value:int)->int:
        return clock.now_ns()+value
    return task_map(tasks,stamp,values)
'''
        self.refused(capturing, 'PAL320')

    def test_callback_data_and_signature_contract_refusals(self):
        cases = [PURE.replace('task_map(tasks, double, values)', 'task_map(tasks, double)'),
                 PURE.replace('task_map(tasks, double, values)', 'task_map(tasks, double, messages=values)'),
                 PURE.replace('task_map(tasks, double, values)', 'task_map(tasks, double, (1,2))'),
                 PURE.replace('def double(value: int)', 'def double(value: str)'),
                 PURE.replace('task_map(tasks, double, values)', 'task_map(values, double, values)')]
        for source in cases:
            with self.subTest(source=source):
                self.refused(source, 'PAL221')

    def test_external_slot_cannot_inject_task_or_omit_family_bound(self):
        self.refused(EXTERNAL.replace('task_map_with(tasks, clock, stamp, values)', 'task_map_with(tasks, tasks, stamp, values)'), 'PAL221')
        self.refused(EXTERNAL.replace('@effects(Clock)\ndef stamp', '@fun\ndef stamp'), 'PAL221')

    def test_task_capability_has_no_methods_or_data_aliases(self):
        self.refused(PURE.replace('task_map(tasks, double, values)', 'tasks.task_map(double, values)'), 'PAL230')
        self.refused(PURE.replace('    return task_map', '    other=tasks\n    return task_map'), 'PAL320')

    def test_ignored_completed_vector_is_refused(self):
        self.refused(PURE.replace('    return task_map(tasks, double, values)', '    task_map(tasks, double, values)\n    return values'), 'PAL250')

    def test_borrowed_task_provider_preserves_task_and_expiry(self):
        result = self.check(PURE.replace('    return task_map(tasks, double, values)', '    with borrow(tasks) as view:\n        completed=task_map(view,double,values)\n    return completed'), cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual(self.contract(result).borrow_scopes[0]['interface'], 'TaskCapability')
        self.refused(PURE.replace('    return task_map(tasks, double, values)', '    with borrow(tasks) as view:\n        completed=task_map(view,double,values)\n    return task_map(view,double,values)'), 'PAL221')

    def test_controlled_and_live_setup_are_observed_without_execution(self):
        source = PURE + 'from pyalamode import live_tasks,controlled_tasks\na=live_tasks(2,max_tasks=8)\nb=controlled_tasks((2,0,1),cancel_after=2)\n'
        result = self.check(source, cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        setups = [row for f in result.results for row in f.setup_observations]
        self.assertEqual([row['identity'] for row in setups], ['pyalamode.tasks.live_tasks', 'pyalamode.tasks.controlled_tasks'])
        self.assertTrue(all(row['version'] == TASK_VERSION for row in setups))

    def test_audit_registration_alias_invalidates_backend_and_restoration(self):
        self.source.write_text(PURE)
        clean = self.check(cache=True)
        self.assertEqual(clean.status, 0, clean.to_dict())
        shell = self.root / 'shell.py'
        shell.write_text('import sys\nregister=sys.addaudithook\ndef hook(event,args):pass\nregister(hook)\n')
        invalid = self.check(cache=True)
        self.assertEqual(invalid.status, 1, invalid.to_dict())
        self.assertIn('PAL240', [x.rule for f in invalid.results for x in f.diagnostics])
        shell.write_text('import sys\nregister=sys.addaudithook\n')
        restored = self.check(cache=True)
        self.assertEqual(restored.status, 0, restored.to_dict())
        self.assertEqual(self.contract(restored).task_scopes, self.contract(clean).task_scopes)

    def test_native_handle_writer_is_conservative(self):
        (self.root / 'shell.py').write_text('import _thread\nnamespace=_thread._ThreadHandle.__dict__\nnamespace.update({"join":None})\n')
        result = self.check(cache=False)
        self.assertEqual(result.status, 1, result.to_dict())
        self.assertIn('PAL240', [x.rule for f in result.results for x in f.diagnostics])

    def test_cold_full_and_partial_cache_preserve_task_scope(self):
        cold = self.check(cache=True)
        warm = self.check(cache=True)
        self.assertEqual(cold.status, 0, cold.to_dict())
        self.assertEqual(self.contract(cold).task_scopes, self.contract(warm).task_scopes)
        (self.root / 'ordinary.py').write_text('value=3\n')
        partial = self.check(cache=True)
        self.assertEqual(partial.status, 0, partial.to_dict())
        self.assertEqual(self.contract(cold).task_scopes, self.contract(partial).task_scopes)

    def test_task_namespace_writers_refuse_tasks_and_preserve_other_contracts(self):
        independent = self.root / 'independent.py'
        independent.write_text('''from pyalamode import fun,Vector,effects,Clock,ClockCapability
@fun
def same(value:int)->int:
    return value+1
@fun
def copied(values:Vector[int])->Vector[int]:
    return values.map(same)
@effects(Clock)
def now(clock:ClockCapability)->int:
    return clock.now_ns()
''')
        clean = self.check(cache=True)
        self.assertEqual(clean.status, 0, clean.to_dict())
        clean_file = next(f for f in clean.results if f.path == str(independent))
        warm = self.check(cache=True)
        self.assertTrue(next(f for f in warm.results if f.path == str(independent)).cache_hit)
        cases = (
            ('module', 'pyalamode.tasks', 'import pyalamode.tasks as backend\nbackend.task_map=print\n'),
            ('alias', 'pyalamode.tasks', 'import pyalamode.tasks as backend\nalias=backend\nalias.task_map=print\n'),
            ('dictionary', 'pyalamode.tasks', 'import pyalamode.tasks as backend\nnamespace=backend.__dict__\nnamespace.update({"task_map":print})\n'),
            ('globals', 'pyalamode.tasks', 'from pyalamode import task_map\nnamespace=task_map.__globals__\nnamespace["task_map"]=print\n'),
            ('setattr', 'pyalamode.tasks', 'import pyalamode.tasks as backend\nsetattr(backend,"task_map",print)\n'),
            ('catalog', 'pyalamode.task_contracts', 'import pyalamode.task_contracts as backend\nbackend.operation_contract=print\n'),
        )
        writer = self.root / 'writer.py'
        seen_namespaces = set()
        for label, namespace, source in cases:
            with self.subTest(writer=label):
                writer.write_text(source)
                try:
                    captured = {}
                    first = self.check(cache=True, _capture=captured)
                    self.assertEqual(first.status, 1, first.to_dict())
                    self.assertIn('PAL240', [d.rule for f in first.results for d in f.diagnostics])
                    self.assertIn(namespace + '.*', captured['graph'].task_dependency_replacements)
                    task_file = next(f for f in first.results if f.path == str(self.source))
                    if namespace not in seen_namespaces:
                        self.assertFalse(task_file.cache_hit)
                    seen_namespaces.add(namespace)
                    self.assertNotEqual(task_file.fingerprint, next(f for f in clean.results if f.path == str(self.source)).fingerprint)
                    self.assertIn(namespace + '.*.<task dependency>', task_file.binding_context)
                    self.assertIn('PAL240', [d.rule for d in task_file.diagnostics if (d.line, d.column) == (8, 12)])
                    self.assertNotIn('PAL230', [d.rule for d in task_file.diagnostics if (d.line, d.column) == (8, 12)])
                    second = self.check(cache=True)
                    self.assertEqual(second.status, 1, second.to_dict())
                    self.assertTrue(next(f for f in second.results if f.path == str(self.source)).cache_hit)
                    uncached = self.check(cache=False)
                    self.assertEqual(uncached.status, 1, uncached.to_dict())
                    self.assertIn('PAL240', [d.rule for f in uncached.results for d in f.diagnostics])
                    for checked in (first, second):
                        unchanged = next(f for f in checked.results if f.path == str(independent))
                        self.assertTrue(unchanged.cache_hit)
                        self.assertEqual(unchanged.fingerprint, clean_file.fingerprint)
                        self.assertEqual(unchanged.binding_context, clean_file.binding_context)
                        self.assertEqual(unchanged.status, 0)
                        self.assertEqual({c.name for c in unchanged.contracts}, {'same', 'copied', 'now'})
                        self.assertTrue(all(c.source_evidence.startswith('checked') for c in unchanged.contracts))
                        self.assertEqual(next(c for c in unchanged.contracts if c.name == 'now').required_effects, ['Clock'])
                finally:
                    writer.unlink()
                restored = self.check(cache=True)
                self.assertEqual(restored.status, 0, restored.to_dict())
                self.assertEqual(self.contract(restored).task_scopes, self.contract(clean).task_scopes)

    def test_source_check_and_build_do_not_execute_application(self):
        sentinel = self.root / 'executed'
        source = PURE + 'from pathlib import Path\nPath(' + repr(str(sentinel)) + ').write_text("bad")\n'
        checked = self.check(source, cache=False)
        self.assertEqual(checked.status, 0, checked.to_dict())
        built = build_paths([self.root], root=self.root, output=self.root / 'out')
        self.assertEqual(built.status, 0, built.to_dict())
        self.assertFalse(sentinel.exists())


class TaskMetadataTests(unittest.TestCase):
    def test_catalog_is_finite_detached_and_explainable(self):
        operations = operation_catalog()
        self.assertEqual(len(operations), 2)
        self.assertTrue(all(len(row) == 30 for row in operations))
        self.assertEqual(len(setup_catalog()), 2)
        operations[0]['effects'].append('invented')
        self.assertEqual(operation_contract('task_map')['effects'], ['Task', 'callback declared/conditional effect-bound union'])
        self.assertIsNone(operation_contract('task_map_async'))
        self.assertEqual(explain_symbol('tasks')['contract']['version'], TASK_VERSION)
        self.assertEqual(explain_symbol('live_tasks')['contract']['catalog'][0]['identity'], 'pyalamode.tasks.live_tasks')

    def test_current_identity_and_exact_foundation_inventory(self):
        self.assertEqual(CHECKER_VERSION, 'experimental-syntax-sums-14.1')
        self.assertTrue(OPERATION_VERSION.endswith('builder-task-syntax-union-ops-14.1'))
        identities = foundation_identities()
        self.assertEqual(len(identities), 28)
        self.assertIn('tasks.py', identities)
        self.assertIn('task_contracts.py', identities)

    def test_tasks_policy_weakening_is_separate_from_source_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'core.py').write_text('from pyalamode import fun\n@fun\ndef same(value:int)->int:\n    return value\n')
            policy = root / 'pyproject.toml'
            policy.write_text('[tool.pyalamode]\ntasks=false\n')
            _, state, _, _ = observe(root, bootstrap=True)
            m.write_baseline(root, state, owner='development', rationale='explicit task permission', prepublish=lambda: None)
            policy.write_text('[tool.pyalamode]\ntasks=true\n[tool.pyalamode.migration]\nschema=1\nreject_policy_weakening=true\n')
            _, current, report, _ = observe(root)
            self.assertEqual(current['schema'], 5)
            self.assertEqual(current['strict_status'], 0)
            self.assertEqual(report['status'], 1)
            self.assertEqual(report['comparison']['policy_weakening'][0]['reason'], 'tasks-enabled')
            self.assertIn('PAL367', [row['rule'] for row in report['gates']['diagnostics']])

    def test_current_wheel_has_task_profile_and_closed_scopes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'qtask').mkdir()
            (root / 'qtask/__init__.py').write_text('# mode: fun\n')
            (root / 'qtask/core.py').write_text('# mode: fun\n' + PURE)
            (root / 'pyproject.toml').write_text('[tool.pyalamode]\ntasks=true\n[tool.pyalamode.distribution]\nschema=1\nname="qtask"\nversion="1.0.0"\npackages=["qtask"]\nexports=["qtask.core:make"]\n')
            result = build_paths([root], root=root, artifact='wheel', output=root / 'out/qtask-1.0.0-py3-none-any.whl')
            self.assertEqual(result.status, 0, result.to_dict())
            with zipfile.ZipFile(result.output) as wheel:
                envelope = json.loads(wheel.read('qtask-1.0.0.dist-info/pyalamode/evidence.json'))
            self.assertEqual(envelope['schema'], 4)
            self.assertEqual(envelope['payload']['producer']['task_version'], TASK_VERSION)
            self.assertEqual(len(envelope['payload']['producer']['product_artifacts']), 28)
            d.validate_evidence(envelope)
            for change in ('scope', 'missing', 'extra', 'effect'):
                bad = copy.deepcopy(envelope)
                if change == 'scope': bad['payload']['exports'][0]['contract']['task_scopes'][0]['ordering'] = 'arbitrary deterministic threads'
                elif change == 'missing': bad['payload']['producer'].pop('task_version')
                elif change == 'extra': bad['payload']['exports'][0]['contract']['task_scopes'][0]['cancel'] = True
                else: bad['payload']['exports'][0]['contract']['required_effects'] = ['invented']
                bad['sha256'] = d.digest(bad['payload'])
                with self.subTest(change=change), self.assertRaises(d.DistributionError):
                    d.validate_evidence(bad)

    def test_installed_task_writer_refusal_preserves_scalar_receipt_and_cache(self):
        from pyalamode import project
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            site, consumer = base / 'site', base / 'consumer'
            site.mkdir()
            consumer.mkdir()
            producers = (
                ('qtask', 'checked-tasks', PURE + '\nraise AssertionError("Task producer application executed")\n', ['qtask.core:make', 'qtask.core:double']),
                ('qplain', 'checked-scalar', 'from pyalamode import fun\n@fun\ndef same(value:int)->int:\n    return value+1\nraise AssertionError("scalar producer application executed")\n', ['qplain.core:same']),
            )
            for package, name, source, exports in producers:
                root = base / name
                (root / package).mkdir(parents=True)
                (root / package / '__init__.py').write_text('# mode: fun\n')
                (root / package / 'core.py').write_text(source)
                (root / 'pyproject.toml').write_text('[tool.pyalamode]\ntasks=true\n[tool.pyalamode.distribution]\nschema=1\nname=' + json.dumps(name) + '\nversion="1.0.0"\npackages=' + json.dumps([package]) + '\nexports=' + json.dumps(exports) + '\n')
                wheel = base / 'wheels' / (name.replace('-', '_') + '-1.0.0-py3-none-any.whl')
                built = build_paths([root], root=root, artifact='wheel', output=wheel)
                self.assertEqual(built.status, 0, built.to_dict())
                with zipfile.ZipFile(wheel) as archive:
                    archive.extractall(site)
            installed_before = {p.relative_to(site).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in site.rglob('*') if p.is_file()}
            declarations = ''.join('[[tool.pyalamode.checked_dependencies]]\nschema=1\nname=' + json.dumps(name) + '\nversion="1.0.0"\npackages=' + json.dumps([package]) + '\n' for package, name, _, _ in producers)
            (consumer / 'pyproject.toml').write_text('[tool.pyalamode]\ntasks=true\n' + declarations)
            (consumer / 'use.py').write_text('from pyalamode import effects,Task,TaskCapability,Vector\nfrom qtask.core import make\n@effects(Task)\ndef total(tasks:TaskCapability,values:Vector[int])->Vector[int]:\n    return make(tasks,values)\n')
            (consumer / 'independent.py').write_text('from pyalamode import fun\nfrom qplain.core import same\n@fun\ndef independent(value:int)->int:\n    return same(value)\n')
            (consumer / 'ordinary.py').write_text('raise AssertionError("consumer application executed")\n')
            def run(**kwargs):
                captured = {}
                checked = check_paths([consumer], root=consumer, _capture=captured, **kwargs)
                return checked, captured
            def receipt(checked, name):
                return next(r for r in checked.checked_dependencies if r['declaration']['name'] == name)
            def installed(captured, module):
                path = captured['graph'].modules[module].path
                return next(f for f in captured['installed_results'] if f.path == path)
            with patch.object(sys, 'path', [str(site), *sys.path]):
                clean, clean_capture = run(cache=True)
                self.assertEqual(clean.status, 0, clean.to_dict())
                warm, warm_capture = run(cache=True)
                self.assertEqual(warm.status, 0, warm.to_dict())
                self.assertTrue(installed(warm_capture, 'qtask.core').cache_hit)
                self.assertTrue(installed(warm_capture, 'qplain.core').cache_hit)
                scalar_clean = installed(clean_capture, 'qplain.core')
                task_clean = installed(clean_capture, 'qtask.core')
                writer = consumer / 'writer.py'
                cases = (
                    ('backend', 'pyalamode.tasks', 'import pyalamode.tasks as task_backend\ntask_backend.task_map=print\n'),
                    ('catalog-alias', 'pyalamode.task_contracts', 'import pyalamode.task_contracts as catalog\nalias=catalog\nnamespace=alias.__dict__\nnamespace.update({"operation_contract":print})\n'),
                )
                for label, namespace, source in cases:
                    with self.subTest(writer=label):
                        writer.write_text(source)
                        private = []
                        original = project._intrinsic_distribution_graph
                        def intrinsic(*args):
                            graph, dependencies = original(*args)
                            private.append(graph)
                            return graph, dependencies
                        try:
                            with patch.object(project, '_intrinsic_distribution_graph', intrinsic):
                                first, first_capture = run(cache=True)
                            self.assertFalse(installed(first_capture, 'qtask.core').cache_hit)
                            self.assertNotEqual(installed(first_capture, 'qtask.core').fingerprint, task_clean.fingerprint)
                            self.assertIn(namespace + '.*.<task dependency>', installed(first_capture, 'qtask.core').binding_context)
                            self.assertIn(namespace + '.*', first_capture['graph'].task_dependency_replacements)
                            self.assertNotIn(str(writer), private[0].analyzers)
                            self.assertEqual(private[0].task_dependency_replacements, set())
                            self.assertEqual(private[0].modules['qtask.core'].result.status, 0)
                            second, second_capture = run(cache=True)
                            self.assertTrue(installed(second_capture, 'qtask.core').cache_hit)
                            (consumer / 'ordinary.py').write_text('raise AssertionError("changed consumer application executed")\n')
                            partial, partial_capture = run(cache=True)
                            self.assertTrue(installed(partial_capture, 'qtask.core').cache_hit)
                            uncached, uncached_capture = run(cache=False)
                            for checked, captured in ((first, first_capture), (second, second_capture), (partial, partial_capture), (uncached, uncached_capture)):
                                self.assertEqual(checked.status, 1, checked.to_dict())
                                self.assertEqual(checked.tooling, [])
                                self.assertFalse(checked.verified)
                                task = receipt(checked, 'checked-tasks')
                                self.assertEqual((task['admission'], task['input_status'], task['source_status'], task['complete'], task['verified'], task['exports']), ('current', 0, 1, True, False, []))
                                self.assertTrue(any(d.rule == 'PAL371' and d.dependency_context['upstream']['rule'] == 'PAL240' for f in checked.results for d in f.diagnostics), checked.to_dict())
                                scalar = receipt(checked, 'checked-scalar')
                                self.assertEqual((scalar['admission'], scalar['input_status'], scalar['source_status'], scalar['complete'], scalar['verified']), ('current', 0, 0, True, True))
                                self.assertEqual([e['selector'] for e in scalar['exports']], ['qplain.core:same'])
                                scalar_file = installed(captured, 'qplain.core')
                                self.assertEqual(scalar_file.fingerprint, scalar_clean.fingerprint)
                                self.assertEqual(scalar_file.binding_context, scalar_clean.binding_context)
                                if checked is not uncached:
                                    self.assertTrue(scalar_file.cache_hit)
                                independent = next(f for f in checked.results if f.path == str(consumer / 'independent.py'))
                                self.assertEqual(independent.status, 0)
                                self.assertTrue(all(c.source_evidence.startswith('checked') for c in independent.contracts))
                            out = base / ('refused-' + label)
                            refused = build_paths([consumer], root=consumer, output=out)
                            self.assertEqual(refused.status, 1, refused.to_dict())
                            self.assertIsNone(refused.output)
                            self.assertFalse(out.exists())
                        finally:
                            writer.unlink()
                        restored, restored_capture = run(cache=True)
                        self.assertEqual(restored.status, 0, restored.to_dict())
                        self.assertEqual(installed(restored_capture, 'qtask.core').fingerprint, task_clean.fingerprint)
                        self.assertEqual(receipt(restored, 'checked-tasks')['exports'], receipt(clean, 'checked-tasks')['exports'])
                        restored_make = next(c for c in installed(restored_capture, 'qtask.core').contracts if c.name == 'make')
                        clean_make = next(c for c in task_clean.contracts if c.name == 'make')
                        self.assertEqual(restored_make.task_scopes, clean_make.task_scopes)
            self.assertEqual({p.relative_to(site).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in site.rglob('*') if p.is_file()}, installed_before)

    def test_authentic_m12_history_is_retained_and_not_promoted(self):
        archive = json.loads((Path(__file__).parent / 'fixtures/m13/legacy-m12.json').read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            for name, raw in archive['projects']['H07'].items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw.encode())
            reference = m.load_reference(root, '.pyalamode/baseline.json')
            self.assertEqual(reference['record']['id'], 'be726acf992467eda1b663476d336cad5a82c79c6f30ba6593b04c607661c476')
            self.assertEqual(hashlib.sha256((root / '.pyalamode/baseline.json').read_bytes()).hexdigest(), '15bcdcf8e83299e501d68f386d5ceca09fe79e8d66c2b6e7b299a262178b08f0')
            self.assertEqual(reference['state']['schema'], 3)
            self.assertEqual(len(reference['state']['inputs']['product_artifacts']), 24)
            self.assertEqual(reference['state']['checker'], 'confined-builders-12.0')
            self.assertNotIn('tasks', reference['state']['policy'])
            _, state, report, _ = observe(root)
            self.assertEqual(state['schema'], 5)
            self.assertEqual(state['strict_status'], 1)
            self.assertEqual(len(report['comparison']['retained_findings']), 4)
            with self.assertRaises(m.MigrationError):
                m.normalize_state(reference['state'])
            for name, raw in archive['projects']['H07'].items():
                self.assertEqual((root / name).read_bytes(), raw.encode())
            bad = copy.deepcopy(reference['state'])
            bad['policy']['tasks'] = True
            with self.assertRaises(m.MigrationError):
                m._state(bad, retained=True)

    def test_authentic_m12_wheels_keep_old_finite_nested_schema(self):
        archive = json.loads((Path(__file__).parent / 'fixtures/m13/legacy-m12.json').read_bytes())
        for mode, encoded in archive['wheels'].items():
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'old.whl'
                raw = base64.b64decode(encoded, validate=True)
                path.write_bytes(raw)
                original = '/tmp/pyalamode-m13-review/history/wheels/' + mode + '/checked_builder-1.0.0-py3-none-any.whl'
                self.assertEqual(hashlib.sha256(raw).hexdigest(), archive['retained_map'][original]['sha256'])
                with zipfile.ZipFile(path) as wheel:
                    envelope = json.loads(wheel.read('checked_builder-1.0.0.dist-info/pyalamode/evidence.json'))
                self.assertEqual(envelope['schema'], 2)
                d.validate_evidence(envelope)
                self.assertNotIn('task_version', envelope['payload']['producer'])
                for mutate in ('task-field', 'task-effect', 'task-capability', 'task-rule'):
                    bad = copy.deepcopy(envelope)
                    contract = bad['payload']['exports'][0]['contract']
                    if mutate == 'task-field': contract['task_scopes'] = []
                    elif mutate == 'task-effect': contract['effect_bound'] = ['Task']
                    elif mutate == 'task-capability': contract['parameters'][next(iter(contract['parameters']))] = 'TaskCapability'
                    else: bad['payload']['modules'][0]['diagnostics'] = [{'rule': 'PAL382'}]
                    bad['sha256'] = d.digest(bad['payload'])
                    with self.subTest(mode=mode, mutate=mutate), self.assertRaises(d.DistributionError):
                        d.validate_evidence(bad)


if __name__ == '__main__':
    unittest.main()
