"""Fixed M14 ordinary artifacts, passive evidence and ownership controls."""
import base64
import ast
import copy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
from unittest.mock import patch
import zipfile

from m14_integration import M14Case, REPO, POLICY, SCALAR, VECTOR, FIELDS

LOCATE_KEYS = set('schema kind status verified artifact generated authored exact segments snapshot inputs diagnostics'.split())
DIRECTORY_KEYS = set('owner edition authored normalized runtime authored_copy_path lowered_copy_path map_path map_sha256 runtime_map_path runtime_map_sha256 facades'.split())
MODULE_KEYS = set('module authored_path source_sha256 installed_path artifact_sha256 initialization setup_observations edition normalized_sha256 translator lowered_path lowered_sha256 map_path map_sha256'.split())
PRODUCER_KEYS = set('builder_version checker edition encoding_version integration_version operation_contract product_artifacts runtime_environment standard_version task_version syntax_version source_map_schema'.split())


class SyntaxDistributionTests(M14Case):
    def build_directory(self, mode='off', name='built'):
        from pyalamode.project import build_paths
        self.source(VECTOR)
        self.policy(POLICY + ('boundary_guards="' + mode + '"\nguarded_exports=["core:make"]\n' if mode != 'off' else ''))
        out = self.root / name
        result = build_paths([self.root], root=self.root, output=out)
        self.assertEqual(result.status, 0, result.to_dict())
        return out, json.loads((out / 'pyalamode-evidence.json').read_bytes())

    def locate(self, out, path, line, column):
        return self.command('locate', '--artifact', str(out), '--path', path,
                            '--line', str(line), '--column', str(column))

    def setup_wheel(self, source=None, mode='off', name='wheel'):
        from pyalamode.project import build_paths
        package = self.root / 'checked_syntax'
        package.mkdir(exist_ok=True)
        self.source('# mode: fun\n', package / '__init__.py')
        core = package / 'core.pya'
        self.source(source or VECTOR.replace('def make()', 'def quote()'), core)
        if self.path.exists():
            self.path.unlink()
        self.policy(POLICY + ('boundary_guards="' + mode + '"\nguarded_exports=["checked_syntax.core:quote"]\n' if mode != 'off' else '') +
                    '[tool.pyalamode.distribution]\nschema=1\nname="checked-syntax"\nversion="1.0.0"\npackages=["checked_syntax"]\nexports=["checked_syntax.core:quote"]\n')
        out = self.root.parent / (self.root.name + '-' + name) / 'checked_syntax-1.0.0-py3-none-any.whl'
        self.addCleanup(lambda: shutil.rmtree(out.parent, ignore_errors=True))
        result = build_paths([self.root], root=self.root, output=out, artifact='wheel')
        self.assertEqual(result.status, 0, result.to_dict())
        site = self.root.parent / (self.root.name + '-' + name + '-site')
        site.mkdir()
        self.addCleanup(lambda: shutil.rmtree(site, ignore_errors=True))
        with zipfile.ZipFile(out) as archive:
            archive.extractall(site)
        evidence = site / 'checked_syntax-1.0.0.dist-info/pyalamode/evidence.json'
        return out, site, evidence, json.loads(evidence.read_bytes())

    def consumer(self, site, source=None, *, tasks=False, cache=False, capture=None):
        from pyalamode.project import check_paths
        consumer = self.root.parent / (self.root.name + '-consumer')
        consumer.mkdir(exist_ok=True)
        self.addCleanup(lambda: shutil.rmtree(consumer, ignore_errors=True))
        (consumer / 'pyproject.toml').write_text('[tool.pyalamode]\nschema=1\n' + ('tasks=true\n' if tasks else '') +
            '[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="checked-syntax"\nversion="1.0.0"\npackages=["checked_syntax"]\n')
        (consumer / 'use.py').write_text(source or '# mode: fun\nfrom checked_syntax.core import quote\nfrom pyalamode import Vector\ndef make()->Vector[int]:\n    return quote()\n')
        with patch.object(sys, 'path', [str(site), *sys.path]):
            result = check_paths([consumer], root=consumer, cache=cache, _capture=capture)
        return consumer, result

    def rewrite_record(self, site):
        info = site / 'checked_syntax-1.0.0.dist-info'
        record = info / 'RECORD'
        members = {path.relative_to(site).as_posix(): path.read_bytes()
                   for path in site.rglob('*') if path.is_file() and path != record and '__pycache__' not in path.parts}
        with record.open('w', newline='') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            for name, raw in sorted(members.items()):
                writer.writerow([name, 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip('='), str(len(raw))])
            writer.writerow([info.name + '/RECORD', '', ''])

    def rewrite_envelope(self, site, path, value):
        from pyalamode import distribution as d
        value['sha256'] = d.digest(value['payload'])
        path.write_bytes(d.canonical(value))
        self.rewrite_record(site)

    def ordinary(self, site, body):
        environment = {'PATH': os.environ.get('PATH', ''), 'PYTHONPATH': str(site) + os.pathsep + str(REPO),
                       'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8', 'PYTHONHASHSEED': '0'}
        result = subprocess.run([sys.executable, '-B', '-c', body], cwd=site,
                                env=environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_directory_off_debug_facade_maps(self):
        for mode in ('off', 'exports', 'debug'):
            out, evidence = self.build_directory(mode, 'built-' + mode)
            artifact = evidence['syntax_artifacts']
            self.assertEqual(set(artifact), {'schema', 'translator', 'modules'})
            self.assertEqual(artifact['schema'], 1)
            self.assertEqual(set(artifact['translator']['files']), {'syntax.py', 'source_maps.py'})
            row = artifact['modules']['core']
            self.assertEqual(set(row), DIRECTORY_KEYS)
            self.assertEqual(row['owner'], {'authored_path': 'core.pya', 'runtime_path': 'core.py', 'module': 'core'})
            self.assertEqual((out / row['authored_copy_path']).read_bytes(), self.path.read_bytes())
            self.assertEqual(hashlib.sha256((out / row['map_path']).read_bytes()).hexdigest(), row['map_sha256'])
            self.assertEqual(hashlib.sha256((out / row['runtime_map_path']).read_bytes()).hexdigest(), row['runtime_map_sha256'])
            self.assertTrue((out / 'core.py').is_file())
            self.assertFalse((out / 'core.pya').exists())
            for facade in row['facades']:
                self.assertEqual(set(facade), {'path', 'map_path', 'map_sha256'})
                self.assertEqual(hashlib.sha256((out / facade['map_path']).read_bytes()).hexdigest(), facade['map_sha256'])
            self.assertEqual(self.path.read_text(), VECTOR)

    def test_locate_exact_anchor_EOF_and_ownership(self):
        from pyalamode.source_maps import position_at
        out, evidence = self.build_directory('debug')
        row = evidence['syntax_artifacts']['modules']['core']
        raw = (out / 'core.py').read_bytes()
        tree = ast.parse(raw)
        copied = next(node for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id == 'values')
        anchored = next(node for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == 'pyalamode.boundaries')
        for node, exact in [(copied, True), (anchored, False)]:
            status, location = self.locate(out, 'core.py', node.lineno, node.col_offset + 1)
            self.assertEqual(status, 0, location)
            self.assertEqual(set(location), LOCATE_KEYS)
            self.assertEqual(set(location['generated']), {'path', 'line', 'column', 'column_encoding', 'sha256'})
            self.assertEqual(set(location['authored']), {'path', 'source_copy', 'line', 'column', 'end_line', 'end_column', 'column_encoding', 'sha256'})
            self.assertEqual(set(location['inputs']), {'evidence_sha256', 'product_artifacts', 'artifacts'})
            self.assertEqual(location['exact'], exact)
            if exact:
                self.assertEqual((location['authored']['line'], location['authored']['column']), (4, 9))
        eof = position_at(raw, len(raw))
        status, location = self.locate(out, 'core.py', eof.line, eof.column)
        self.assertEqual(status, 0, location)
        self.assertEqual(location['authored']['path'], 'core.pya')
        self.assertEqual(self.locate(out, '../core.py', 1, 1)[0], 2)
        self.assertEqual(self.locate(out, 'core.py', 1, 0)[0], 2)
        if row['facades']:
            facade = row['facades'][0]['path']
            parent = str(Path(facade).parent / '__init__.py')
            self.assertEqual(self.locate(out, parent, 1, 1)[0], 2)

        # A compatible dependency keeps its declared decoder during regeneration.
        import builtins
        from pyalamode.project import build_paths, locate_source
        latin_root = self.root / 'latin-project'
        latin_root.mkdir()
        (latin_root / 'pyproject.toml').write_bytes(POLICY.encode('utf-8'))
        dependency = b'# coding: latin-1\n# mode: fun\nLABEL = "caf\xe9"\ndef extra(value: int) -> int:\n    return value + 1\n'
        (latin_root / 'foreign.py').write_bytes(dependency)
        authored = '# mode: fun\nfrom foreign import extra\ndef make(value:int)->int:\n    val result=extra(value)\n    return result\n'
        (latin_root / 'core.pya').write_bytes(authored.encode('utf-8'))
        latin_out = self.root / 'latin-built'
        original_import = builtins.__import__
        def no_authored_import(name, *args, **kwargs):
            if name in {'foreign', 'core'}:
                raise AssertionError('authored application import during build/locate')
            return original_import(name, *args, **kwargs)
        with patch.object(builtins, '__import__', side_effect=no_authored_import):
            built = build_paths([latin_root], root=latin_root, output=latin_out)
            self.assertEqual(built.status, 0, built.to_dict())
            generated = (latin_out / 'core.py').read_bytes()
            generated_tree = ast.parse(generated)
            target = next(node for node in ast.walk(generated_tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id == 'result')
            located = locate_source(artifact=latin_out, path='core.py', line=target.lineno,
                column=target.col_offset + 1, root=latin_root)
        self.assertEqual((located['status'], located['verified'], located['exact']), (0, True, True), located)
        self.assertEqual((located['authored']['path'], located['authored']['line'], located['authored']['column']), ('core.pya', 4, 9))
        self.assertEqual((latin_out / '.pyalamode/sources/foreign.py').read_bytes(), dependency)
        self.assertEqual((latin_root / 'core.pya').read_bytes(), authored.encode('utf-8'))

    def test_wheel4_shapes_RECORD_and_normal_import(self):
        out, site, _, envelope = self.setup_wheel(mode='debug')
        payload = envelope['payload']
        self.assertEqual(set(envelope), {'schema', 'kind', 'payload', 'sha256'})
        self.assertEqual(envelope['schema'], 4)
        self.assertEqual(len(payload), 9)
        self.assertEqual(set(payload['producer']), PRODUCER_KEYS)
        self.assertEqual(len(payload['producer']['product_artifacts']), 28)
        for module in payload['modules']:
            self.assertEqual(set(module), MODULE_KEYS)
        for row in payload['inputs']['sources'].values():
            self.assertEqual(set(row), {'sha256', 'module', 'ownership', 'shipped', 'participating', 'edition', 'normalized_sha256'})
        self.assertEqual(set(payload['guards']), {'mode', 'exports', 'debug', 'generated_files', 'source_maps'})
        for export in payload['exports']:
            self.assertEqual(set(export['contract']), set(FIELDS))
        with zipfile.ZipFile(out) as archive:
            names = set(archive.namelist())
            record = list(csv.reader(io.StringIO(archive.read('checked_syntax-1.0.0.dist-info/RECORD').decode())))
            self.assertEqual({row[0] for row in record}, names)
            for name, digest, size in record:
                if name.endswith('/RECORD'):
                    self.assertEqual((digest, size), ('', ''))
                else:
                    raw = archive.read(name)
                    self.assertEqual(digest, 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip('='))
                    self.assertEqual(int(size), len(raw))
        self.assertEqual(self.ordinary(site, 'from checked_syntax.core import quote\nprint(tuple(quote()))\n'), '(1, 2)\n')

    def test_default_python_receiver_dialect_dependency(self):
        _, site, _, _ = self.setup_wheel()
        consumer, result = self.consumer(site)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual(result.to_dict()['edition'], 'python-v1')
        self.assertNotIn('edition', (consumer / 'pyproject.toml').read_text())
        receipt = result.checked_dependencies[0]
        self.assertTrue(receipt['verified'])
        self.assertEqual((receipt['input_status'], receipt['source_status']), (0, 0))
        self.assertEqual(len(result.results), 1)
        self.assertEqual(len(receipt['exports'][0]['contract']), 43)

        # Migration binds only consumer-owned sources, not producer dialect rows.
        from pyalamode.migration_views import observe
        from pyalamode import migration as m
        with patch.object(sys, 'path', [str(site), *sys.path]):
            _, local_state, _, _ = observe(consumer)
        m._state(local_state, retained=True)
        self.assertEqual((local_state['edition'], local_state['policy']['edition']), ('python-v1', 'python-v1'))
        self.assertEqual(set(local_state['inputs']['sources']), {'use.py'})
        local = local_state['inputs']['sources']['use.py']['source_provenance']
        self.assertEqual((local['owner']['authored_path'], local['selected_edition']), ('use.py', 'python-v1'))
        self.assertIn('checked-syntax', local_state['inputs']['checked_dependencies'])

    def test_consumer_combined_writer_and_scalar_precision(self):
        source = '# mode: fun\nfrom pyalamode import Vector, Task, TaskCapability, effects, task_map\ndef cb(value:int)->int:\n    return value+1\n@effects(Task)\ndef quote(tasks:TaskCapability,values:Vector[int])->Vector[int]:\n    return task_map(tasks,cb,values)\n'
        self.policy(POLICY + 'tasks=true\n')
        # setup_wheel owns a complete producer policy; add Task permission there.
        from pyalamode.project import build_paths
        with patch.object(self, 'policy', lambda text: M14Case.policy(self, text.replace('edition="pyalamode-v1-experimental"\n', 'edition="pyalamode-v1-experimental"\ntasks=true\n'))):
            _, site, _, _ = self.setup_wheel(source)
        use = '# mode: fun\nfrom checked_syntax.core import quote\nfrom pyalamode import Vector, Task, TaskCapability, effects\n@effects(Task)\ndef make(tasks:TaskCapability,values:Vector[int])->Vector[int]:\n    return quote(tasks,values)\n'
        consumer, disabled = self.consumer(site, use, tasks=False)
        self.assertEqual(disabled.status, 1, disabled.to_dict())
        self.assertEqual((disabled.checked_dependencies[0]['input_status'], disabled.checked_dependencies[0]['source_status']), (0, 1))
        (consumer / 'independent.py').write_text(SCALAR)
        _, clean = self.consumer(site, use, tasks=True, cache=True)
        self.assertEqual(clean.status, 0, clean.to_dict())
        self.consumer(site, use, tasks=True, cache=True)
        writer = consumer / 'writer.py'
        for text in ('import pyalamode.tasks as backend\nbackend.task_map=print\n',
                     'import pyalamode.task_contracts as backend\nbackend.operation_contract=print\n'):
            writer.write_text(text)
            _, changed = self.consumer(site, use, tasks=True, cache=True)
            self.assertEqual(changed.status, 1, changed.to_dict())
            findings = [d for f in changed.results for d in f.diagnostics if d.rule == 'PAL371']
            self.assertTrue(findings, changed.to_dict())
            self.assertTrue(all(d.dependency_context['upstream']['rule'] == 'PAL240' for d in findings))
            self.assertEqual((changed.checked_dependencies[0]['input_status'], changed.checked_dependencies[0]['source_status']), (0, 1))
            self.assertEqual(self.contract(clean, 'same'), self.contract(changed, 'same'))
            writer.unlink()
        _, restored = self.consumer(site, use, tasks=True, cache=True)
        self.assertEqual(restored.status, 0, restored.to_dict())
        self.assertFalse((consumer / 'built').exists())

    def test_maps_and_roles_closed_bounds(self):
        from pyalamode import distribution as d
        _, site, evidence, envelope = self.setup_wheel()
        d.validate_evidence(envelope)
        module = next(row for row in envelope['payload']['modules'] if row['authored_path'].endswith('.pya'))
        map_path = site / module['map_path']
        original = map_path.read_bytes()
        map_path.write_bytes(original + b' ' * (33554433 - len(original)))
        _, result = self.consumer(site)
        self.assertEqual(result.status, 2, result.to_dict())
        map_path.write_bytes(original)
        bad = copy.deepcopy(envelope)
        bad['payload']['artifacts'][module['map_path']]['role'] = 'invented-map'
        bad['sha256'] = d.digest(bad['payload'])
        with self.assertRaises(d.DistributionError):
            d.validate_evidence(bad)
        runtime = site / module['installed_path']
        raw = runtime.read_bytes()
        runtime.write_bytes(b'x' * 8388609)
        try:
            self.assertEqual(self.consumer(site)[1].status, 2)
        finally:
            runtime.write_bytes(raw)
        self.assertEqual(self.consumer(site)[1].status, 0)
        self.assertEqual(evidence.read_bytes(), d.canonical(envelope))

    def test_passive_malformed_vs_stale_axes(self):
        from pyalamode import distribution as d
        _, site, evidence, envelope = self.setup_wheel()
        original = evidence.read_bytes()
        module = next(row for row in envelope['payload']['modules'] if row['authored_path'].endswith('.pya'))

        # Known versions and syntactically valid pins must also agree internally.
        d.validate_evidence(envelope)
        for helper in ('syntax.py', 'source_maps.py'):
            for axis in ('module-translator', 'producer-product'):
                inconsistent = copy.deepcopy(envelope)
                if axis == 'module-translator':
                    next(row for row in inconsistent['payload']['modules'] if row['authored_path'].endswith('.pya'))['translator']['files'][helper] = '0' * 64
                else:
                    inconsistent['payload']['producer']['product_artifacts'][helper] = '0' * 64
                inconsistent['sha256'] = d.digest(inconsistent['payload'])
                with self.subTest(translator_helper=helper, axis=axis), self.assertRaises(d.DistributionError):
                    d.validate_evidence(inconsistent)
        self.assertEqual(evidence.read_bytes(), original)
        runtime = site / module['installed_path']
        before = runtime.read_bytes()
        runtime.write_bytes(before + b'\n# stale ordinary artifact\n')
        _, stale = self.consumer(site)
        self.assertEqual(stale.status, 1, stale.to_dict())
        self.assertEqual(stale.checked_dependencies[0]['input_status'], 1)
        self.assertEqual(stale.checked_dependencies[0]['exports'], [])
        runtime.write_bytes(before)
        bad = copy.deepcopy(envelope)
        next(row for row in bad['payload']['modules'] if row['authored_path'].endswith('.pya'))['translator']['version'] = 'invented'
        self.rewrite_envelope(site, evidence, bad)
        _, malformed = self.consumer(site)
        self.assertEqual(malformed.status, 2, malformed.to_dict())
        self.assertFalse(malformed.checked_dependencies[0]['complete'])
        evidence.write_bytes(original)
        self.rewrite_record(site)
        self.assertEqual(self.consumer(site)[1].status, 0)
        map_path = site / module['map_path']
        map_before = map_path.read_bytes()
        value = json.loads(map_before)
        def install_map(value):
            map_path.write_bytes((json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode())
            changed = copy.deepcopy(envelope)
            sha = hashlib.sha256(map_path.read_bytes()).hexdigest()
            changed['payload']['artifacts'][module['map_path']].update(sha256=sha, size=map_path.stat().st_size)
            next(row for row in changed['payload']['modules'] if row['authored_path'].endswith('.pya'))['map_sha256'] = sha
            for row in changed['payload']['guards']['source_maps'].values():
                if row['path'] == module['map_path']:
                    row['sha256'] = sha
            self.rewrite_envelope(site, evidence, changed)
        # Shape/bytes valid, but deliberately different from exact regeneration.
        valid = copy.deepcopy(value)
        next(row for row in valid['segments'] if row['kind'] == 'copy')['kind'] = 'anchor'
        install_map(valid)
        _, nonderived = self.consumer(site)
        self.assertEqual(nonderived.status, 1, nonderived.to_dict())
        self.assertEqual(nonderived.checked_dependencies[0]['input_status'], 1)
        value['segments'][0]['generated_end'] += 1
        install_map(value)
        try:
            self.assertEqual(self.consumer(site)[1].status, 2)
        finally:
            map_path.write_bytes(map_before)
            evidence.write_bytes(original)
            self.rewrite_record(site)

    def test_genuine_wheels1_through3_unchanged(self):
        from pyalamode import distribution as d
        fixture_raw = (REPO / 'tests/fixtures/m14/legacy-m11-wheel.json').read_bytes()
        self.assertEqual(hashlib.sha256(fixture_raw).hexdigest(), '784a13ccd48ee6ee5b217b500e12fececb7056ff3c5a8565b92b7abb554eec26')
        historic = json.loads(fixture_raw)
        self.assertEqual(set(historic), {'schema', 'kind', 'original_path', 'retained_path', 'wheel', 'receipt'})
        wheel1 = base64.b64decode(historic['wheel']['data'], validate=True)
        self.assertEqual((len(wheel1), hashlib.sha256(wheel1).hexdigest()),
                         (67958, '272be9de20f15a186905c288fe0609b3a74f8d2a0aaa8c89c61deff58e1d118e'))
        raw_receipt = historic['receipt']['data'].encode('utf-8')
        self.assertEqual((len(raw_receipt), hashlib.sha256(raw_receipt).hexdigest()),
                         (historic['receipt']['bytes'], historic['receipt']['sha256']))
        receipt = json.loads(raw_receipt)
        self.assertEqual(receipt['original_path'], historic['original_path'])
        self.assertEqual(receipt['copy_path'], historic['retained_path'])
        archive2 = json.loads((REPO / 'tests/fixtures/m13/legacy-m12.json').read_bytes())
        genuine = [(wheel1, 1, 22)] + [(base64.b64decode(encoded, validate=True), 2, 24) for encoded in archive2['wheels'].values()]
        self.assertEqual(len(genuine), 4)
        for raw, schema, products in genuine:
            with zipfile.ZipFile(io.BytesIO(raw)) as wheel:
                name = next(name for name in wheel.namelist() if name.endswith('/pyalamode/evidence.json'))
                envelope = json.loads(wheel.read(name))
            self.assertEqual((envelope['schema'], len(envelope['payload']['producer']['product_artifacts'])), (schema, products))
            self.assertNotIn('syntax_version', envelope['payload']['producer'])
            d.validate_evidence(envelope)
        archive, blobs = self.decoded_m13()
        wheels = [row for row in archive['files'] if row['path'].endswith('.whl')]
        self.assertEqual(len(wheels), 3)
        for row in wheels:
            with zipfile.ZipFile(io.BytesIO(blobs[row['sha256']])) as wheel:
                name = next(name for name in wheel.namelist() if name.endswith('/pyalamode/evidence.json'))
                envelope = json.loads(wheel.read(name))
            self.assertEqual((envelope['schema'], len(envelope['payload']['producer']['product_artifacts'])), (3, 26))
            self.assertNotIn('syntax_version', envelope['payload']['producer'])
            d.validate_evidence(envelope)
            counterfeit = copy.deepcopy(envelope)
            counterfeit['payload']['producer']['syntax_version'] = 'pyalamode.syntax-v1'
            counterfeit['sha256'] = d.digest(counterfeit['payload'])
            with self.assertRaises(d.DistributionError):
                d.validate_evidence(counterfeit)

    def test_late_publication_inputs_and_original_hold(self):
        from pyalamode import project, syntax
        self.source(VECTOR)
        raw = self.path.read_bytes()
        original = syntax.lower_source
        out = self.root / 'refused'
        def changed(*args, **kwargs):
            value = original(*args, **kwargs)
            self.source(raw + b'\n# late raw mutation\n')
            return value
        with patch.object(syntax, 'lower_source', changed):
            result = project.build_paths([self.root], root=self.root, output=out)
        self.assertNotEqual(result.status, 0, result.to_dict())
        self.assertFalse(out.exists())
        self.source(raw)
        self.source('raise AssertionError("ordinary fixture executed during check")\n', self.root / 'sentinel.py')
        self.assertEqual(self.check().status, 0)
        self.assertEqual(self.path.read_bytes(), raw)
        _, site, _, envelope = self.setup_wheel(name='late-dependency')
        consumer, clean = self.consumer(site)
        self.assertEqual(clean.status, 0, clean.to_dict())
        module = next(row for row in envelope['payload']['modules'] if row['authored_path'].endswith('.pya'))
        runtime = site / module['installed_path']
        runtime_before = runtime.read_bytes()
        check_original = project.check_paths
        def late_dependency(*args, **kwargs):
            result = check_original(*args, **kwargs)
            runtime.write_bytes(runtime_before + b'\n# late dependency\n')
            return result
        refused = consumer / 'refused'
        try:
            with patch.object(sys, 'path', [str(site), *sys.path]), patch.object(project, 'check_paths', late_dependency):
                result = project.build_paths([consumer], root=consumer, output=refused)
            self.assertEqual(result.status, 1, result.to_dict())
            self.assertIn('PAL372', self.rules(result))
            self.assertFalse(refused.exists())
        finally:
            runtime.write_bytes(runtime_before)

    def test_actual_runtime_bytecode_opt0_1_2(self):
        from pyalamode import distribution as d
        _, site, _, envelope = self.setup_wheel()
        module = next(row for row in envelope['payload']['modules'] if row['authored_path'].endswith('.pya'))
        runtime = site / module['installed_path']
        for optimization in (0, 1, 2):
            py_compile.compile(str(runtime), doraise=True, optimize=optimization)
        _, current = self.consumer(site)
        self.assertEqual(current.status, 0, current.to_dict())
        observed = current.checked_dependencies[0]['observed']['caches']
        self.assertEqual(len(observed), 3)
        self.assertTrue(all('/__pycache__/core.' in name for name in observed))
        cache = next(runtime.parent.glob('__pycache__/core.*.pyc'))
        raw = cache.read_bytes()
        cache.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        try:
            self.assertEqual(self.consumer(site)[1].status, 2)
        finally:
            cache.write_bytes(raw)
        self.assertEqual(self.consumer(site)[1].status, 0)
        self.assertEqual(self.ordinary(site, 'from checked_syntax.core import quote\nprint(tuple(quote()))\n'), '(1, 2)\n')
