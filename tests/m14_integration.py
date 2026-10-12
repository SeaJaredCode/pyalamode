"""Fixed M14 integration inputs; authored before any candidate observation.

These methods run only after root accepts the complete central/helper sources.
History decoding is data-only. No application fixture executes during checks.
"""
import base64
import contextlib
import copy
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
EDITION = 'pyalamode-v1-experimental'
POLICY = '[tool.pyalamode]\nschema=1\nedition="pyalamode-v1-experimental"\n'
SCALAR = '# mode: fun\ndef same(value: int) -> int:\n    return value + 1\n'
VECTOR = '# mode: fun\nfrom pyalamode import Vector\ndef make() -> Vector[int]:\n    val values: Vector[int] = [1, 2]\n    return values\n'
FIELDS = tuple('name path line parameters returns parameter_kinds enforcement behavior source_evidence trust failures freshness boundary_protection caller_obligations defaults captures dependencies callable_targets callable_defaults return_callable_targets definition_failures operations data_assertions callable_capture_evidence return_callable_evidence invoked_targets callable_dependencies callable_arguments callable_operations effect_bound required_effects effect_origins capability_parameters borrow_scopes failure_edges direct_failures patterns handlers operation_contracts callable_default_evidence external_assumptions builder_scopes task_scopes'.split())
FORMAT_KEYS = set('schema kind mode status source_status strict_status applied snapshot freshness inputs files diagnostics'.split())
FORMAT_FILE_KEYS = set('path version before_sha256 after_sha256 before after edits diff changed source_provenance'.split())
PROVENANCE_KEYS = set('schema owner selected_edition authored normalized translator map coordinate_space status'.split())


class M14Case(unittest.TestCase):
    """Shared source fixture support; no test methods or dynamic expectations."""
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.path = self.root / 'core.pya'
        self.policy(POLICY)

    def policy(self, text):
        (self.root / 'pyproject.toml').write_bytes(text.encode('utf-8'))

    def source(self, text, path=None):
        path = path or self.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if type(text) is bytes else text.encode('utf-8'))
        return path

    def check(self, text=None, *, cache=False, **kwargs):
        from pyalamode.project import check_paths
        if text is not None:
            self.source(text)
        return check_paths([self.root], root=self.root, cache=cache, **kwargs)

    def command(self, *args):
        from pyalamode.cli import main
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            status = main([*args, '--root', str(self.root), '--json'])
        return status, json.loads(stream.getvalue())

    def rules(self, result):
        return [d.rule for d in result.tooling] + [d.rule for f in result.results for d in f.diagnostics]

    def contract(self, result, name='make', path=None):
        matches = [asdict(c) for f in result.results for c in f.contracts
                   if c.name == name and (path is None or f.path == str(path))]
        self.assertEqual(len(matches), 1, result.to_dict())
        self.assertEqual(set(matches[0]), set(FIELDS))
        return matches[0]

    def checked(self, text=None):
        result = self.check(text)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertTrue(result.verified, result.to_dict())
        return result

    def refuse(self, text, status, rule):
        result = self.check(text)
        self.assertEqual(result.status, status, result.to_dict())
        self.assertIn(rule, self.rules(result))
        return result

    def format(self, mode='preview'):
        return self.command('format', str(self.path), '--' + mode)

    def rebuild_edits(self, before, edits):
        raw = before.encode('utf-8')
        for edit in reversed(edits):
            self.assertEqual(set(edit), {'start', 'end', 'replacement'})
            self.assertIs(type(edit['start']), int)
            self.assertIs(type(edit['end']), int)
            raw = raw[:edit['start']] + edit['replacement'].encode('utf-8') + raw[edit['end']:]
        return raw

    def normalized_contract(self, value, owners):
        """Only explicit typed path/target sites; all other nested values retained."""
        path_fields = {'path'}
        target_fields = {'target', 'targets', 'dependencies', 'callable_targets', 'callable_defaults',
                         'return_callable_targets', 'invoked_targets', 'callable_dependencies',
                         'callable_arguments', 'callback_targets'}
        def visit(item, key=None, inherited_target=False):
            target = inherited_target or key in target_fields
            if type(item) is dict:
                return {k: visit(v, k, target) for k, v in item.items()}
            if type(item) is list:
                return [visit(v, key, target) for v in item]
            if type(item) is str and (key in path_fields or target):
                for old, new in owners.items():
                    if item == old:
                        return new
                    if item.startswith(old + '::'):
                        return new + item[len(old):]
            return item
        return visit(copy.deepcopy(value))

    def repair(self, text):
        from pyalamode.migration_views import observe, convert_preview
        self.source(text)
        snapshot, state, _, _ = observe(self.root)
        return convert_preview(snapshot, state, 'function:core:make')

    def decoded_m13(self):
        raw = (REPO / 'tests/fixtures/m14/legacy-m13.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), 'fb75f89c9a515a22d2997ff878d39690153b9b77a360ae1ffb8cf60ec2fa780c')
        archive = json.loads(raw)
        blobs = {}
        for digest, row in archive['blobs'].items():
            value = row['data'].encode('utf-8') if row['encoding'] == 'utf-8-exact' else base64.b64decode(row['data'], validate=True)
            self.assertEqual((len(value), hashlib.sha256(value).hexdigest()), (row['bytes'], digest))
            blobs[digest] = value
        self.assertEqual((len(archive['files']), len(blobs)), (72, 58))
        return archive, blobs

    def comparison(self, before, after, **kwargs):
        from pyalamode.project import _contract_comparison
        value = _contract_comparison(before, after, **kwargs)
        self.assertEqual(set(value), {'matched', 'fields'})
        self.assertIs(type(value['matched']), bool)
        self.assertEqual([row['field'] for row in value['fields']], list(FIELDS))
        for row in value['fields']:
            self.assertEqual(set(row), {'field', 'before', 'after', 'matched', 'rule'})
            self.assertEqual(row['before'], before[row['field']])
            self.assertEqual(row['after'], after[row['field']])
            self.assertIs(type(row['matched']), bool)
        return value

    def assert_repair_relation(self, before, after, repair):
        """All43 actual fields; only fixed fixture binding/evidence changes."""
        self.assertEqual(set(before), set(FIELDS))
        self.assertEqual(set(after), set(FIELDS))
        expected = copy.deepcopy(before)
        first = {'line': 3, 'name': 'result', 'schema': 'int'}
        second = {'line': 4, 'name': 'result', 'schema': 'int'}
        if repair in {'PAL101-Assign', 'PAL101-AnnAssign'}:
            self.assertEqual(before['data_assertions'], [first, second] if repair == 'PAL101-Assign' else [first])
            expected['data_assertions'] = [first, {'line': 4, 'name': 'result_2', 'schema': 'int'}]
        else:
            self.assertEqual(repair, 'PAL250')
            self.assertEqual(before['data_assertions'], [])
            expected['data_assertions'] = [{'line': 4, 'name': 'updated_value', 'schema': 'Vector[int]'}]
        transitions = {
            'source_evidence': ('unverified: audit or failed selected gate', 'checked participating source'),
            'freshness': ('no successful checked claim', 'current for recorded inputs'),
            'behavior': ('unverified behavior; no certified effect bound', 'pure'),
        }
        self.assertEqual(before['effect_bound'], [])
        self.assertEqual(before['required_effects'], [])
        for field, (old, new) in transitions.items():
            self.assertEqual(before[field], old)
            expected[field] = new
        for field in FIELDS:
            self.assertEqual(after[field], expected[field], {'field': field, 'before': before[field], 'after': after[field]})


class SyntaxIntegrationTests(M14Case):
    def test_local_selection_and_whole_mode_axes(self):
        self.policy('[tool.pyalamode]\nschema=1\n')
        disabled = self.refuse(SCALAR, 1, 'PAL390')
        self.assertEqual(disabled.to_dict()['coverage']['eligible_functions'], 1)
        self.assertEqual(disabled.to_dict()['coverage']['eligible_modules'], 1)
        # Preparation refusals are already included in lowering's issue set.
        self.assertEqual(self.rules(disabled).count('PAL390'), 1)
        for audit in (False, True):
            for attempt in range(2):
                cached = self.check(cache=True, audit=audit)
                self.assertEqual(cached.status, 0 if audit else 1)
                self.assertFalse(cached.verified)
                primary = [d for file in cached.results for d in file.diagnostics if d.rule == 'PAL390']
                self.assertEqual([(d.line, d.column, d.end_line, d.end_column) for d in primary], [(1, 1, 1, 1)])
        self.policy(POLICY)
        self.checked(SCALAR)
        self.refuse(SCALAR.replace('# mode: fun\n', ''), 1, 'PAL390')
        missing = self.check()
        primary = [d for file in missing.results for d in file.diagnostics if d.rule == 'PAL390']
        self.assertEqual([(d.line, d.column, d.end_line, d.end_column) for d in primary], [(1, 1, 1, 1)])
        reserved = self.refuse(SCALAR.replace('return value + 1', 'return val + val'), 1, 'PAL392')
        occurrences = [d for file in reserved.results for d in file.diagnostics if d.rule == 'PAL392']
        self.assertEqual([(d.line, d.column, d.end_line, d.end_column) for d in occurrences], [(3, 12, 3, 15), (3, 18, 3, 21)])
        bad = self.refuse(b'# mode: fun\ndef broken(:\n', 2, 'PAL001')
        self.assertNotIn('PAL390', self.rules(bad))

    def test_ownership_collision_and_NFKC_axes(self):
        self.source(SCALAR, self.root / 'core.py')
        self.source(SCALAR)
        self.assertEqual(self.check().status, 2)
        self.path.unlink()
        self.source('# mode: fun\n', self.root / 'core/__init__.py')
        compatible = self.check()
        self.assertEqual(compatible.status, 0, compatible.to_dict())
        self.source('# mode: fun\n', self.root / 'core/__init__.pya')
        self.assertEqual(self.check().status, 2)
        for file in (self.root / 'core').iterdir():
            file.unlink()
        (self.root / 'core').rmdir()
        (self.root / 'core.py').unlink()
        for name in ('Core.pya', '\u212a.pya'):
            path = self.source(SCALAR, self.root / name)
            if name == 'Core.pya':
                self.source('# mode: fun\n', self.root / 'core/__init__.py')
            result = self.check()
            self.assertEqual(result.status, 2, result.to_dict())
            self.assertIn('PAL001', self.rules(result))
            path.unlink()
            if (self.root / 'core').exists():
                (self.root / 'core/__init__.py').unlink()
                (self.root / 'core').rmdir()
        self.refuse(SCALAR.replace('value + 1', '_pyalamode_syntax_Vector(value)'), 1, 'PAL392')

        # Direct entry ownership is checked before any authored bytes are read.
        from pyalamode.checker import analyze_file
        self.source(SCALAR)
        self.assertEqual(analyze_file(self.path, policy={"edition": EDITION}).status, 0)
        ordinary = self.source(SCALAR, self.root / 'ordinary.py')
        self.assertEqual(analyze_file(ordinary).status, 0)
        compatible_alias = self.root / 'ordinary-alias.py'
        compatible_alias.symlink_to(ordinary)
        self.assertEqual(analyze_file(compatible_alias).status, 0)
        real_directory = self.root / 'physical'
        real_directory.mkdir()
        real_dialect = self.source(SCALAR, real_directory / 'unit.pya')
        parent_alias = self.root / 'parent-alias'
        parent_alias.symlink_to(real_directory, target_is_directory=True)
        requests = []
        for alias_name, target in (('dialect-alias.pya', self.path),
                                   ('hidden-format.py', self.path),
                                   ('wrong-format.pya', ordinary)):
            alias = self.root / alias_name
            alias.symlink_to(target)
            requests.append(alias)
        requests.append(parent_alias / 'unit.pya')
        for request in requests:
            with self.subTest(physical_request=request.name):
                with patch.object(Path, 'read_bytes', side_effect=AssertionError('authored read before ownership refusal')):
                    refused = analyze_file(request, policy={"edition": EDITION})
                self.assertEqual(refused.status, 2, refused.to_dict())
                self.assertEqual([d.rule for d in refused.diagnostics], ['PAL001'])
                self.assertEqual(refused.diagnostics[0].path, str(request))
        self.assertEqual(real_dialect.read_bytes(), SCALAR.encode('utf-8'))

    def test_empty_annotation_exact_alias_qualified_quoted(self):
        sources = (
            ('from pyalamode import Vector', 'Vector[int]'),
            ('from pyalamode import Vector as V', 'V[int]'),
            ('import pyalamode as p', 'p.Vector[int]'),
            ('from pyalamode import Vector', '"Vector[int]"'),
            ('from pyalamode import Vector', 'Vector[tuple[int, str]]'),
        )
        for imports, annotation in sources:
            with self.subTest(annotation=annotation):
                text = '# mode: fun\n' + imports + '\ndef make() -> ' + annotation + ':\n    val values: ' + annotation + ' = []\n    return values\n'
                result = self.checked(text)
                self.assertEqual(self.contract(result)['returns'], 'Vector[tuple[int, str]]' if 'tuple' in annotation else 'Vector[int]')
        self.checked('# mode: fun\nfrom pyalamode import Map\ndef make() -> Map[str, int]:\n    val values: Map[str, int] = {}\n    return values\n')
        self.checked('# mode: fun\nfrom pyalamode import Vector, record\n@record\nclass Row:\n    value: int\nval rows: Vector[Row] = []\ndef make() -> Vector[Row]:\n    return rows\n')

        # The same established module identities admit ordinary explicit constructors.
        for imports, annotation, constructor in (
            ('from pyalamode import Vector, record', 'Vector[Row]', 'Vector[Row].of()'),
            ('from pyalamode import Vector as V, record', 'V[Row]', 'V[Row].of()'),
            ('import pyalamode as p\nfrom pyalamode import record', 'p.Vector[Row]', 'p.Vector[Row].of()'),
        ):
            with self.subTest(module_annotation=annotation):
                prefix = '# mode: fun\n' + imports + '\n@record\nclass Row:\n    value: int\n'
                suffix = 'def make() -> ' + annotation + ':\n    return rows\n'
                dialect = self.checked(prefix + 'val rows: ' + annotation + ' = []\n' + suffix)
                self.assertEqual(self.contract(dialect)['returns'], "Vector[Record['core:Row']]")
                self.path.unlink()
                ordinary = self.source(prefix + 'rows: ' + annotation + ' = ' + constructor + '\n' + suffix,
                                       self.root / 'core.py')
                compatible = self.checked()
                self.assertEqual(self.contract(compatible)['returns'], "Vector[Record['core:Row']]")
                ordinary.unlink()

    def test_empty_late_shadow_replaced_annotation_refusals(self):
        inputs = (
            "# mode: fun\nfrom pyalamode import Vector\ndef make() -> Vector[int]:\n    val values: 'Vector[\"int\"]' = []\n    return values\n",
            '# mode: fun\nfrom pyalamode import Vector\ndef make() -> Vector[int]:\n    val values: Vector[Unknown] = []\n    return values\n',
            '# mode: fun\nfrom pyalamode import Vector\ndef make() -> Vector[int]:\n    val Vector: int = 1\n    val values: Vector[int] = []\n    return values\n',
            '# mode: fun\nfrom pyalamode import Vector, record\nval rows: "Vector[Row]" = []\n@record\nclass Row:\n    value: int\ndef make() -> Vector[Row]:\n    return rows\n',
        )
        for source in inputs:
            with self.subTest(source=source):
                result = self.check(source)
                self.assertEqual(result.status, 1, result.to_dict())
                self.assertFalse(result.verified)
        # Removing only established bindings keeps later module names unavailable.
        self.path.unlink()
        ordinary = self.root / 'core.py'
        for source in (
            '# mode: fun\nfrom pyalamode import Vector, record\nrows: "Vector[Row]" = Vector[Row].of()\n@record\nclass Row:\n    value: int\ndef make() -> Vector[Row]:\n    return rows\n',
            '# mode: fun\nfrom pyalamode import record\n@record\nclass Row:\n    value: int\nrows: "Vector[Row]" = Vector[Row].of()\nfrom pyalamode import Vector\ndef make() -> Vector[Row]:\n    return rows\n',
        ):
            with self.subTest(compatible_late_binding=source):
                self.source(source, ordinary)
                result = self.check()
                self.assertEqual(result.status, 1, result.to_dict())
                self.assertFalse(result.verified)
        self.source('# mode: fun\nfrom pyalamode import Vector, record\n@record\nclass Row:\n    value: int\nrows: Vector[Row] = Vector[Row].of()\ndef make() -> Vector[Row]:\n    return rows\n', ordinary)
        self.source('import core\ncore.Row=print\n', self.root / 'writer.py')
        replaced = self.check()
        self.assertEqual(replaced.status, 1, replaced.to_dict())
        self.assertFalse(replaced.verified)
        self.assertIn('PAL130', self.rules(replaced))
        (self.root / 'writer.py').unlink()
        ordinary.unlink()
        self.source('import pyalamode\npyalamode.Vector=print\n', self.root / 'writer.py')
        self.assertEqual(self.check(VECTOR).status, 1)

    def test_complete_contract_counterparts(self):
        text = '''# mode: fun
from pyalamode import Vector, VectorBuilder, vector_build, effects, Task, TaskCapability, Clock, ClockCapability, task_map_with, borrow, Option, Some, Nothing
def defaulted(value:int, fee:int=2)->int:
    return value+fee
def captured(values:Vector[int], fee:int)->Vector[int]:
    def quote(value:int)->int:
        return value+fee
    return values.map(quote)
def assembled(values:Vector[int])->Vector[int]:
    def populate(builder:VectorBuilder[int])->None:
        builder.extend(values)
        return None
    return vector_build(populate)
@effects(Clock)
def stamp(clock:ClockCapability, value:int)->tuple[int,int]:
    return (value,clock.now_ns())
@effects(Task,Clock)
def scheduled(tasks:TaskCapability,clock:ClockCapability,values:Vector[int])->Vector[tuple[int,int]]:
    return task_map_with(tasks,clock,stamp,values)
@effects(Clock)
def now(clock:ClockCapability)->int:
    with borrow(clock) as view:
        return view.now_ns()
def safe(values:Vector[int])->int:
    try:
        val result:int=values[0]
    except IndexError:
        return 0
    return result
def choose(value:Option[int])->int:
    match value:
        case Some(item):
            return item
        case Nothing():
            return 0
'''
        self.policy(POLICY + 'tasks=true\nbuilders=true\n')
        self.source(text)
        counterpart = self.source(text.replace('val result:', 'result:'), self.root / 'counterpart.py')
        result = self.checked()
        left = {c.name: asdict(c) for f in result.results if f.path == str(self.path) for c in f.contracts}
        right = {c.name: asdict(c) for f in result.results if f.path == str(counterpart) for c in f.contracts}
        self.assertEqual(set(left), set(right))
        for name in left:
            self.assertEqual(set(left[name]), set(FIELDS))
            self.assertEqual(self.normalized_contract(left[name], {str(self.path): str(counterpart)}), right[name], name)
        self.assertTrue(left['defaulted']['defaults'])
        self.assertTrue(left['captured.quote']['captures'])
        for name, field in [('assembled', 'builder_scopes'), ('scheduled', 'task_scopes'), ('now', 'borrow_scopes'), ('safe', 'handlers'), ('choose', 'patterns')]:
            self.assertTrue(left[name][field], (name, field))
        self.assertEqual(left['scheduled']['required_effects'], ['Clock', 'Task'])
        self.assertTrue(left['scheduled']['failures'])
        self.assertTrue(all(row['trust'] and row['caller_obligations'] for row in left.values()))

    def test_public_authored_coordinates_and_private_cache(self):
        raw = '\ufeff"""astral \U0001f600 and separator \u2028"""\r\n# mode: fun\r\ndef make(value:int)->int:\r\n    val result:int=value\r\n    val result:int=result+1\r\n    return result\r\n'.encode('utf-8')
        self.source(raw)
        cold, warm, full = self.check(cache=True), self.check(cache=True), self.check(cache=False)
        self.assertEqual(cold.status, 1, cold.to_dict())
        for result in (cold, warm, full):
            finding = next(d for f in result.results for d in f.diagnostics if d.rule == 'PAL101')
            self.assertEqual((finding.line, finding.column), (5, 9))
            file = next(f for f in result.results if f.path == str(self.path))
            self.assertEqual(set(file.source_provenance), PROVENANCE_KEYS)
            self.assertEqual(file.source_provenance['authored']['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(file.source_provenance['coordinate_space'], 'authored-utf8')
        self.assertEqual([asdict(d) for d in cold.results[0].diagnostics], [asdict(d) for d in warm.results[0].diagnostics])
        self.assertEqual(self.contract(cold), self.contract(warm))
        self.assertEqual(self.contract(cold), self.contract(full))
        self.assertTrue(next(f for f in warm.results if f.path == str(self.path)).cache_hit)

        # Public checks must retain source authority even for checksum-valid payloads.
        from pyalamode import project

        def target(result):
            return next(f for f in result.results if f.path == str(self.path))

        def claim(file):
            value = copy.deepcopy(file.to_dict())
            value.pop('cache_hit')
            return value

        def assert_claims(result, reference):
            self.assertEqual(result.status, reference.status, result.to_dict())
            self.assertEqual(result.verified, reference.verified, result.to_dict())
            self.assertEqual({f.path: claim(f) for f in result.results},
                             {f.path: claim(f) for f in reference.results})
            self.assertEqual([asdict(d) for d in result.tooling],
                             [asdict(d) for d in reference.tooling])
            self.assertEqual(result.analysis_counts['fresh_body_files'],
                             sum(not f.cache_hit for f in result.results))
            self.assertEqual(result.analysis_counts['cached_body_files'],
                             sum(f.cache_hit for f in result.results))

        def store(envelope, cache_file):
            envelope = copy.deepcopy(envelope)
            encoded = json.dumps(envelope['payload'], sort_keys=True, separators=(',', ':'))
            envelope['checksum'] = hashlib.sha256(encoded.encode()).hexdigest()
            cache_file.write_text(json.dumps(envelope, sort_keys=True))
            written = json.loads(cache_file.read_bytes())
            self.assertEqual(written['checksum'], hashlib.sha256(json.dumps(
                written['payload'], sort_keys=True, separators=(',', ':')).encode()).hexdigest())

        helper = self.source(SCALAR.replace('def same(', 'def helper('),
                             self.root / 'cache_dependency.pya')
        scalar = SCALAR.replace('# mode: fun\n',
                                '# mode: fun\nfrom cache_dependency import helper\n')
        self.source(scalar)
        captured = {}
        reference = self.check(cache=False, _capture=captured)
        clean = self.check(cache=True)
        self.assertEqual(reference.status, 0, reference.to_dict())
        self.assertFalse(target(clean).cache_hit)
        assert_claims(clean, reference)
        warmed = self.check(cache=True)
        self.assertTrue(all(f.cache_hit for f in warmed.results))
        assert_claims(warmed, reference)
        cache_dir = self.root / '.pyalamode-cache'
        cache_file = cache_dir / (target(clean).fingerprint + '.json')
        genuine = json.loads(cache_file.read_bytes())
        self.assertEqual(set(genuine), {'payload', 'checksum'})
        self.assertEqual(set(genuine['payload']['contracts'][0]), set(FIELDS))
        self.assertEqual(genuine['payload']['contracts'][0]['returns'], 'int')
        self.assertTrue(genuine['payload']['contracts'][0]['trust'])
        self.assertIn(str(helper), genuine['payload']['dependencies'])
        for field in ('returns', 'effect_bound', 'trust', 'dependencies', 'source_provenance'):
            with self.subTest(cache_forgery=field):
                forged = copy.deepcopy(genuine)
                payload = forged['payload']
                if field == 'returns':
                    payload['contracts'][0]['returns'] = 'str'
                elif field == 'effect_bound':
                    payload['contracts'][0]['effect_bound'] = ['Clock']
                elif field == 'trust':
                    payload['contracts'][0]['trust'] = payload['contracts'][0]['trust'][1:]
                elif field == 'dependencies':
                    self.assertNotEqual(payload['dependencies'][str(helper)], '0' * 64)
                    payload['dependencies'][str(helper)] = '0' * 64
                else:
                    self.assertNotEqual(payload['source_provenance']['authored']['sha256'], '0' * 64)
                    payload['source_provenance']['authored']['sha256'] = '0' * 64
                self.assertEqual(set(payload), set(genuine['payload']))
                self.assertEqual(set(payload['contracts'][0]), set(FIELDS))
                store(forged, cache_file)
                checked = self.check(cache=True)
                self.assertFalse(target(checked).cache_hit)
                self.assertGreater(checked.analysis_counts['fresh_body_files'], 0)
                assert_claims(checked, reference)
                recovered = self.check(cache=True)
                self.assertTrue(target(recovered).cache_hit)
                assert_claims(recovered, reference)
        reordered = {key: genuine['payload'][key] for key in reversed(genuine['payload'])}
        cache_file.write_text(json.dumps({'checksum': genuine['checksum'], 'payload': reordered}))
        same = self.check(cache=True)
        self.assertTrue(target(same).cache_hit)
        assert_claims(same, reference)

        # Generic writes serialize data; they cannot establish a source derivation.
        forged_result = copy.deepcopy(captured['normalized_results'][str(self.path)])
        forged_result.contracts[0].returns = 'str'
        identities_before_write = project._SOURCE_CACHE_IDENTITIES.copy()
        project._cache_write(cache_dir, forged_result)
        self.assertEqual(project._SOURCE_CACHE_IDENTITIES, identities_before_write)
        bypass = self.check(cache=True)
        self.assertFalse(target(bypass).cache_hit)
        assert_claims(bypass, reference)
        self.assertTrue(target(self.check(cache=True)).cache_hit)

        # Unselected occupancy tests bounded eviction through real public checks.
        original_identities = project._SOURCE_CACHE_IDENTITIES
        try:
            project._SOURCE_CACHE_IDENTITIES = {
                (project.os.getpid(), f'{index:064x}',
                 str(self.root / 'not-selected' / str(index)), 'strict'): '0' * 64
                for index in range(4096)
            }
            self.assertFalse((self.root / 'not-selected').exists())
            evicted = self.check(cache=True)
            self.assertTrue(all(not f.cache_hit for f in evicted.results))
            assert_claims(evicted, reference)
            self.assertLessEqual(len(project._SOURCE_CACHE_IDENTITIES), 4096)
            recovered = self.check(cache=True)
            self.assertTrue(all(f.cache_hit for f in recovered.results))
            assert_claims(recovered, reference)
            published = project._SOURCE_CACHE_IDENTITIES
            published_values = published.copy()
            helper.write_text(SCALAR.replace('def same(', 'def helper(').replace('value + 1', 'value + 2'))
            changed_reference = self.check(cache=False)
            changed = self.check(cache=True)
            self.assertTrue(all(not f.cache_hit for f in changed.results))
            assert_claims(changed, changed_reference)
            self.assertIsNot(project._SOURCE_CACHE_IDENTITIES, published)
            self.assertEqual(published, published_values)
            self.assertLessEqual(len(project._SOURCE_CACHE_IDENTITIES), 4096)
        finally:
            helper.write_text(SCALAR.replace('def same(', 'def helper('))
            project._SOURCE_CACHE_IDENTITIES = original_identities

        # Separate CLI interpreters must rederive rather than trust persisted bytes.
        child = ('import sys\n'
                 'sys.path.insert(0, sys.argv[1])\n'
                 'from pyalamode.cli import main\n'
                 'raise SystemExit(main(["check", sys.argv[2], "--root", sys.argv[2], "--json"]))\n')
        for ordinal in range(2):
            with self.subTest(fresh_process=ordinal):
                completed = subprocess.run(
                    [sys.executable, '-I', '-B', '-X', 'utf8=' + str(sys.flags.utf8_mode),
                     '-c', child, str(REPO), str(self.root)],
                    cwd=REPO, capture_output=True, text=True, timeout=120)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                observed = json.loads(completed.stdout)
                self.assertEqual(observed['status'], reference.status)
                self.assertEqual(observed['verified'], reference.verified)
                self.assertTrue(all(not f['cache_hit'] for f in observed['files']))
                self.assertEqual(observed['analysis_counts']['fresh_body_files'], len(observed['files']))
                self.assertEqual(observed['analysis_counts']['cached_body_files'], 0)
                self.assertEqual({f['path']: {k: v for k, v in f.items() if k != 'cache_hit'}
                                  for f in observed['files']},
                                 {f.path: claim(f) for f in reference.results})
                self.assertEqual(observed['tooling'], [asdict(d) for d in reference.tooling])
        parent_reuse = self.check(cache=True)
        self.assertTrue(all(f.cache_hit for f in parent_reuse.results))
        assert_claims(parent_reuse, reference)

        # A success-shaped cache cannot erase a real mapped-source failure.
        helper.unlink()
        self.source(raw)
        failure_reference = self.check(cache=False)
        failure_cache = cache_dir / (target(failure_reference).fingerprint + '.json')
        failure_cache.unlink(missing_ok=True)
        failure = self.check(cache=True)
        self.assertFalse(target(failure).cache_hit)
        assert_claims(failure, failure_reference)
        forged = json.loads(failure_cache.read_bytes())
        forged['payload']['diagnostics'] = []
        forged['payload']['verified'] = True
        forged['payload']['status'] = 0
        for contract in forged['payload']['contracts']:
            contract['source_evidence'] = 'checked participating source'
            contract['freshness'] = 'current for recorded inputs'
            contract['behavior'] = 'pure'
        store(forged, failure_cache)
        refused = self.check(cache=True)
        self.assertFalse(target(refused).cache_hit)
        self.assertEqual(refused.status, 1)
        self.assertFalse(refused.verified)
        assert_claims(refused, failure_reference)
        finding = next(d for f in refused.results for d in f.diagnostics if d.rule == 'PAL101')
        self.assertEqual((finding.line, finding.column), (5, 9))
        self.assertFalse((self.root / 'built').exists())

    def test_translation_inputs_and_writer_cache_refusal(self):
        clean = self.check(VECTOR, cache=True)
        self.assertEqual(clean.status, 0, clean.to_dict())
        fingerprint = next(f for f in clean.results if f.path == str(self.path)).fingerprint
        self.source(VECTOR.replace('[1, 2]', '[1, 3]'))
        changed = self.check(cache=True)
        self.assertNotEqual(next(f for f in changed.results if f.path == str(self.path)).fingerprint, fingerprint)
        scalar = self.source(SCALAR, self.root / 'independent.py')
        before = self.check(cache=True)
        writer = self.root / 'writer.py'
        for text in ('import pyalamode.syntax as compiler\ncompiler.lower_source=print\n',
                     'import pyalamode.collections as backend\nbackend.Vector=print\n'):
            with self.subTest(writer=text):
                self.source(text, writer)
                refused = self.check(cache=True)
                self.assertEqual(refused.status, 1, refused.to_dict())
                self.assertEqual(self.contract(refused, 'same', scalar), self.contract(before, 'same', scalar))
                writer.unlink()
                self.assertEqual(self.check(cache=True).status, 0)
        self.policy('[tool.pyalamode]\nschema=1\n')
        self.assertIn('PAL390', self.rules(self.check(cache=True)))

    def test_format_full_parity_and_idempotence(self):
        raw = '\ufeff# mode: fun\r\ndef make(value:int)->int:\r\n    val    result:int=value+1  \r\n    return result\r\n'.encode('utf-8')
        self.source(raw)
        before = self.checked()
        status, preview = self.format()
        self.assertEqual(status, 1, preview)
        self.assertEqual(set(preview), FORMAT_KEYS)
        self.assertEqual((preview['source_status'], preview['strict_status'], preview['applied']), (0, 0, False))
        row = preview['files'][0]
        self.assertEqual(set(row), FORMAT_FILE_KEYS)
        self.assertEqual(self.rebuild_edits(row['before'], row['edits']), row['after'].encode('utf-8'))
        self.assertEqual(self.path.read_bytes(), raw)
        self.source(row['after'])
        after = self.checked()
        self.assertEqual(self.contract(before), self.contract(after))
        status, stable = self.format('check')
        self.assertEqual(status, 0, stable)
        self.assertEqual(stable['files'][0]['edits'], [])
        self.assertIsNone(stable['files'][0]['before'])
        self.assertIsNone(stable['files'][0]['after'])

    def test_format_refusal_stale_and_unnamed_compatible(self):
        from pyalamode.checker import analyze_source
        unnamed = analyze_source(SCALAR, path='<source>')
        self.assertIsNone(unnamed.source_provenance)
        for text in (VECTOR.replace('[1, 2]', '[]').replace('Vector[int] =', 'Unknown ='),
                     VECTOR.replace('[1, 2]', '[x for x in (1, 2)]'), b'\xff'):
            self.source(text)
            status, result = self.format()
            self.assertEqual(status, 2, result)
            self.assertFalse(result['applied'])
            self.assertTrue(all(row['after'] is None and not row['edits'] for row in result['files']))
        self.source(VECTOR.replace('val values', 'val    values'))
        from pyalamode import syntax
        original = syntax.format_source
        def changed(*args, **kwargs):
            value = original(*args, **kwargs)
            self.source(VECTOR + '\n# late input\n')
            return value
        with patch.object(syntax, 'format_source', changed):
            status, result = self.format()
        self.assertEqual(status, 2, result)
        self.assertFalse(result['applied'])

    def test_full_field_comparator_rejects_each_dimension(self):
        before = self.contract(self.checked(VECTOR))
        exact = self.comparison(before, copy.deepcopy(before))
        self.assertTrue(exact['matched'])
        for field in FIELDS:
            after = copy.deepcopy(before)
            value = after[field]
            if type(value) is dict:
                value['unapproved_changed_entry'] = 'changed'
            elif type(value) is list:
                value.append({'unapproved_changed_entry': 'changed'} if value and type(value[0]) is dict else 'changed')
            elif type(value) is int:
                after[field] = value + 1
            else:
                after[field] = 'changed'
            with self.subTest(field=field):
                comparison = self.comparison(before, after)
                self.assertFalse(comparison['matched'], comparison)
                self.assertFalse(next(row for row in comparison['fields'] if row['field'] == field)['matched'])
        self.assertEqual(before, self.contract(self.checked()))

    def test_repair_PAL101_Assign_and_AnnAssign_relation(self):
        for repair, binding in (('PAL101-Assign', 'val result=value+1\n    val result=result+1'),
                                ('PAL101-AnnAssign', 'val result:int=value+1\n    val result:int=result+1')):
            text = '# mode: fun\ndef make(value:int)->int:\n    ' + binding + '\n    return result\n'
            old = self.contract(self.check(text))
            proposal = self.repair(text)
            self.assertEqual(proposal['status'], 0, proposal)
            after = proposal['edits'][0]['after']
            self.assertIn('result_2=result+1' if repair == 'PAL101-Assign' else 'result_2:int=result+1', after.replace(' ', ''))
            self.assertIn('return result_2', after)
            self.assertEqual(self.path.read_text(), text)
            self.source(after)
            new = self.contract(self.checked())
            self.assertEqual(len(new['data_assertions']), 2)
            self.assertEqual([row['schema'] for row in new['data_assertions']], ['int', 'int'])
            self.assertEqual(old['source_evidence'], 'unverified: audit or failed selected gate')
            self.assertEqual(new['source_evidence'], 'checked participating source')
            self.assert_repair_relation(old, new, repair)

    def test_repair_PAL250_result_binding_relation(self):
        text = '# mode: fun\nfrom pyalamode import Vector\ndef make(values:Vector[int])->Vector[int]:\n    values.appended(1)\n    return values\n'
        old = self.contract(self.check(text))
        proposal = self.repair(text)
        self.assertEqual(proposal['status'], 0, proposal)
        after = proposal['edits'][0]['after']
        self.assertIn('val updated_value', after)
        self.assertIn('return values', after)
        self.source(after)
        new = self.contract(self.checked())
        self.assertEqual(len(new['data_assertions']), len(old['data_assertions']) + 1)
        self.assertEqual(new['data_assertions'][-1]['schema'], 'Vector[int]')
        self.assert_repair_relation(old, new, 'PAL250')

    def test_repair_unmatched_rows_and_promotion_refusals(self):
        cases = (
            '# mode: fun\ndef make(value:int)->int:\n    val result=value+1\n    val result="wrong"\n    return result\n',
            '# mode: fun\ndef make(value:int)->int:\n    val result=value+1\n    val alias=result\n    val result=result+1\n    return result\n',
            '# mode: fun\ndef make(value:int)->int:\n    val result=value+1\n    def capture()->int:\n        return result\n    val result=result+1\n    return capture()\n',
            '# mode: fun\ndef make(value:int)->int:\n    val result=value+1\n    val result=missing(value)\n    return result\n',
        )
        for text in cases:
            with self.subTest(text=text):
                proposal = self.repair(text)
                self.assertNotEqual(proposal['status'], 0, proposal)
                self.assertFalse(proposal['edits'])
                self.assertIsNone(proposal['candidate'])
                self.assertEqual(self.path.read_text(), text)

    def test_migration5_and_genuine1_through4_profiles(self):
        from pyalamode import migration as m
        from pyalamode.migration_views import observe
        self.source(SCALAR)
        _, state, _, _ = observe(self.root)
        self.assertEqual(state['schema'], 5)
        self.assertEqual(len(state), 26)
        self.assertEqual((state['syntax_version'], state['source_map_schema'], state['edition']), ('pyalamode.syntax-v1', 1, EDITION))
        archive, blobs = self.decoded_m13()
        row = next(row for row in archive['files'] if row['path'].endswith('/H05-state.json'))
        historical = json.loads(blobs[row['sha256']])
        self.assertEqual((historical['schema'], len(historical), len(historical['inputs']['product_artifacts'])), (4, 24, 26))
        self.assertNotIn('syntax_version', historical)
        m._state(historical, retained=True)
        counterfeit = copy.deepcopy(historical)
        counterfeit['syntax_version'] = 'pyalamode.syntax-v1'
        with self.assertRaises(m.MigrationError):
            m._state(counterfeit, retained=True)
        for relative, member, schema, count in (
                ('tests/fixtures/m11/legacy-m10.json', 'files', 1, 19),
                ('tests/fixtures/m12/legacy-m11.json', 'files', 2, 22),
                ('tests/fixtures/m13/legacy-m12.json', 'projects', 3, 24)):
            old = json.loads((REPO / relative).read_bytes())
            files = old[member]['H07'] if member == 'projects' else old[member]
            baseline = json.loads(files['.pyalamode/baseline.json'])['state']
            self.assertEqual((baseline['schema'], len(baseline['inputs']['product_artifacts'])), (schema, count))
            m._state(baseline, retained=True)
            bad = copy.deepcopy(baseline)
            bad['policy']['edition'] = EDITION
            with self.subTest(profile=schema), self.assertRaises(m.MigrationError):
                m._state(bad, retained=True)
        self.path.unlink()
        self.source(SCALAR, self.root / 'core.py')
        self.policy('[tool.pyalamode]\nschema=1\n')
        _, before, _, _ = observe(self.root)
        self.policy(POLICY)
        _, after, _, _ = observe(self.root)
        comparison = m.compare_states(before, after)
        self.assertTrue(comparison['policy_weakening'], comparison)
        self.assertIn('edition-experimental-enabled', json.dumps(comparison['policy_weakening']))

        # Local raw identity/selection/product relations, for both source formats.
        for captured in (state, before, after):
            validated = m._state(captured, retained=True)
            self.assertEqual(validated['edition'], captured['policy']['edition'])
            for path, source in captured['inputs']['sources'].items():
                provenance = source['source_provenance']
                self.assertEqual(source['origin'], 'disk')
                self.assertEqual(source['sha256'], source['disk_sha256'])
                self.assertEqual(source['sha256'], provenance['authored']['sha256'])
                self.assertEqual(path, provenance['owner']['authored_path'])
                self.assertEqual(provenance['selected_edition'], captured['edition'])
                if provenance['translator'] is not None:
                    self.assertEqual(provenance['translator']['files'],
                        {name: captured['inputs']['product_artifacts'][name] for name in ('source_maps.py', 'syntax.py')})
        from pyalamode.project import check_snapshot, load_policy
        from pyalamode.migration_views import capture_state, inventory
        for label, filename, text, status in (
                ('disabled-dialect', 'unit.pya', SCALAR, 1),
                ('malformed-python', 'unit.py', '# mode: fun\ndef broken(:\n', 2)):
            refusal_root = self.root / label
            refusal_root.mkdir()
            (refusal_root / 'pyproject.toml').write_bytes(b'[tool.pyalamode]\nschema=1\n')
            self.source(text, refusal_root / filename)
            refusal = check_snapshot([refusal_root], root=refusal_root, cache=False, _migration_history=False)
            self.assertEqual(refusal.result.status, status, refusal.result.to_dict())
            refusal_policy, error = load_policy(refusal_root)
            self.assertIsNone(error)
            refusal_state = capture_state(refusal, refusal_policy, inventory(refusal_root))
            m._state(refusal_state, retained=True)
            source = refusal_state['inputs']['sources'][filename]
            if status == 2:
                self.assertIsNone(source['source_provenance'])
            else:
                self.assertEqual(source['source_provenance']['selected_edition'], 'python-v1')
                self.assertEqual(source['source_provenance']['authored']['edition'], EDITION)
                self.assertEqual(source['source_provenance']['status'], 1)
        for suffix, selection, policy_text in (('.py', 'python-v1', '[tool.pyalamode]\nschema=1\n'),
                                                ('.pya', EDITION, POLICY)):
            overlay_root = self.root / ('overlay-python' if suffix == '.py' else 'overlay-dialect')
            overlay_root.mkdir()
            (overlay_root / 'pyproject.toml').write_bytes(policy_text.encode('utf-8'))
            path = self.source(SCALAR, overlay_root / ('unit' + suffix))
            overlay_text = SCALAR.replace('value + 1', 'value + 2')
            snapshot = check_snapshot([overlay_root], root=overlay_root, cache=False,
                overlays={str(path): {'text': overlay_text, 'version': 7}}, _migration_history=False)
            self.assertEqual(snapshot.result.status, 0, snapshot.result.to_dict())
            overlay_policy, error = load_policy(overlay_root)
            self.assertIsNone(error)
            overlay_state = capture_state(snapshot, overlay_policy, inventory(overlay_root))
            m._state(overlay_state, retained=True)
            self.assertEqual(overlay_state['edition'], selection)
            self.assertEqual(set(overlay_state['inputs']['sources']), {'unit' + suffix})
            source = overlay_state['inputs']['sources']['unit' + suffix]
            self.assertEqual((source['origin'], source['version']), ('overlay', 7))
            self.assertEqual(source['sha256'], hashlib.sha256(overlay_text.encode('utf-8')).hexdigest())
            self.assertEqual(source['disk_sha256'], hashlib.sha256(SCALAR.encode('utf-8')).hexdigest())
            self.assertNotEqual(source['sha256'], source['disk_sha256'])
            self.assertEqual(source['source_provenance']['authored']['sha256'], source['sha256'])
            self.assertEqual(source['source_provenance']['selected_edition'], selection)

        mutations = []
        def mutation(label):
            changed = copy.deepcopy(state)
            mutations.append((label, changed))
            return changed
        mutation('state-edition')['edition'] = 'python-v1'
        mutation('policy-edition')['policy']['edition'] = 'python-v1'
        mutation('source-raw-sha')['inputs']['sources']['core.pya']['sha256'] = '0' * 64
        raw_mismatch = mutation('provenance-raw-sha')['inputs']['sources']['core.pya']['source_provenance']
        raw_mismatch['authored']['sha256'] = '0' * 64
        raw_mismatch['map']['source_sha256'] = '0' * 64
        moved = mutation('provenance-owner-path')['inputs']['sources']['core.pya']['source_provenance']
        moved['owner'] = {'authored_path': 'other.pya', 'runtime_path': 'other.py', 'module': 'other'}
        moved['authored']['path'] = 'other.pya'
        moved['normalized']['path'] = 'other.py'
        mutation('source-selected-edition')['inputs']['sources']['core.pya']['source_provenance']['selected_edition'] = 'python-v1'
        for helper in ('syntax.py', 'source_maps.py'):
            mutation('translator-' + helper)['inputs']['sources']['core.pya']['source_provenance']['translator']['files'][helper] = '0' * 64
            mutation('recorded-product-' + helper)['inputs']['product_artifacts'][helper] = '0' * 64
        for label, changed in mutations:
            with self.subTest(local_provenance=label), self.assertRaises(m.MigrationError):
                m._state(changed, retained=True)
        self.assertEqual(m._state(state, retained=True)['inputs']['sources'], state['inputs']['sources'])


if __name__ == '__main__':
    unittest.main()
