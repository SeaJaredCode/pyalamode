"""Fixed dialect editor requests, complete previews and version-bound edits.

These server tests complement, rather than claim, root's real VS Code host gate.
"""
import ast
import copy
from dataclasses import asdict
import json
from pathlib import Path
from unittest.mock import patch

from m14_integration import M14Case, POLICY, VECTOR, SCALAR, FIELDS

META_KEYS = set('schema target pythonExecutable pythonVersion platform root filesystemEncoding filesystemErrors languages syntaxVersion sourceMapSchema formatProfile'.split())


class SyntaxEditorTests(M14Case):
    def session(self, text=SCALAR):
        from pyalamode.editor import EditorSession
        self.source(text)
        session = EditorSession(self.root)
        initialized = session.handle('initialize', {'rootUri': self.root.as_uri()})
        session.handle('textDocument/didOpen', {'textDocument': {'uri': self.path.as_uri(), 'languageId': 'pyalamode', 'version': 1, 'text': text}})
        return session, initialized

    def format_params(self, session, version=1):
        report = session.handle('pyalamode/project', {})
        return {'textDocument': {'uri': self.path.as_uri()}, 'options': {'tabSize': 4, 'insertSpaces': True},
                'pyalamode': {'version': version, 'snapshot': report['snapshot']}}

    def preview(self, session):
        report = session.handle('pyalamode/project', {})
        finding = next(row for row in report['diagnostics'] if row['code'] in {'PAL101', 'PAL250'})
        return session.handle('pyalamode/preview', {'uri': self.path.as_uri(), 'version': session.documents[str(self.path)]['version'],
            'snapshot': report['snapshot'], 'diagnosticIndex': finding['data']['diagnosticIndex']})

    def test_metadata2_language_and_closed_request_shapes(self):
        from pyalamode.editor import ProtocolError
        session, initialized = self.session()
        capabilities = initialized['capabilities']
        self.assertTrue(capabilities['documentFormattingProvider'])
        metadata = capabilities['experimental']['pyalamode']
        self.assertEqual(set(metadata), META_KEYS)
        self.assertEqual((metadata['schema'], metadata['languages'], metadata['syntaxVersion'], metadata['sourceMapSchema']),
                         (2, ['python', 'pyalamode'], 'pyalamode.syntax-v1', 1))
        self.assertEqual(metadata['pythonVersion'], '3.13.1')
        self.assertEqual(metadata['formatProfile'], 'val-whitespace-v1')
        params = self.format_params(session)
        for mutate in ('extra', 'missing', 'bool-version', 'tab-size'):
            changed = copy.deepcopy(params)
            if mutate == 'extra':
                changed['invented'] = True
            elif mutate == 'missing':
                changed.pop('pyalamode')
            elif mutate == 'bool-version':
                changed['pyalamode']['version'] = True
            else:
                changed['options']['tabSize'] = True
            with self.subTest(mutate=mutate), self.assertRaises(ProtocolError):
                session.handle('textDocument/formatting', changed)
        with self.assertRaises(ProtocolError):
            session.handle('textDocument/didOpen', {'textDocument': {'uri': self.path.as_uri(), 'languageId': 'python', 'version': 2, 'text': SCALAR}})
        foreign = self.root.parent / (self.root.name + '-foreign.pya')
        foreign.write_text(SCALAR)
        self.addCleanup(lambda: foreign.unlink(missing_ok=True))
        with self.assertRaises(ProtocolError):
            session.handle('textDocument/didOpen', {'textDocument': {'uri': foreign.as_uri(), 'languageId': 'pyalamode', 'version': 1, 'text': SCALAR}})

    def test_authored_UTF16_diagnostic_navigation_hover(self):
        text = '\ufeff"""\U0001f600 unicode \u2028 contents"""\r\n# mode: fun\r\ndef leaf(value:int)->int:\r\n    return value+1\r\ndef make(value:int)->int:\r\n    val result:int=leaf(value)\r\n    val result:int=result+1\r\n    return result\r\n'
        session, _ = self.session(text)
        report = session.handle('pyalamode/project', {})
        finding = next(row for row in report['diagnostics'] if row['code'] == 'PAL101')
        self.assertEqual(finding['range']['start'], {'line': 6, 'character': 8})
        authored = finding['data']['authored']
        self.assertEqual((authored['line'], authored['column'], authored['column_encoding']), (7, 9, 'utf-8-bytes'))
        locations = session.handle('textDocument/definition', {'textDocument': {'uri': self.path.as_uri()}, 'position': {'line': 5, 'character': 20}})
        self.assertTrue(any(row['uri'] == self.path.as_uri() and row['range']['start'] == {'line': 2, 'character': 4} for row in locations), locations)
        hover = session.handle('textDocument/hover', {'textDocument': {'uri': self.path.as_uri()}, 'position': {'line': 4, 'character': 5}})
        payload = json.loads(hover['contents']['value'].split('```json\n', 1)[1].split('\n```', 1)[0])
        self.assertEqual(set(payload['contract']), set(FIELDS))
        self.assertNotIn('_pyalamode_syntax_', hover['contents']['value'])
        self.source(b'\xff')
        session.handle('textDocument/didClose', {'textDocument': {'uri': self.path.as_uri()}})
        malformed = session.handle('pyalamode/project', {})
        self.assertEqual(malformed['report']['status'], 2)
        self.assertTrue(all(row['code'] == 'PAL001' for row in malformed['diagnostics']))
        self.assertFalse(malformed['regions'])

    def test_LSP_formatting_edits_and_source_axes(self):
        text = '\ufeff# mode: fun\r\ndef make(value:int)->int:\r\n    val    result:int=value+1  \r\n    return result\r\n'
        session, _ = self.session(text)
        before = session.handle('pyalamode/project', {})
        edits = session.handle('textDocument/formatting', self.format_params(session))
        self.assertTrue(edits)
        for row in edits:
            self.assertEqual(set(row), {'range', 'newText'})
            self.assertEqual(set(row['range']), {'start', 'end'})
        from pyalamode.editor import _offset
        after = text
        for row in reversed(edits):
            start, end = _offset(text, row['range']['start']), _offset(text, row['range']['end'])
            after = after[:start] + row['newText'] + after[end:]
        self.assertIn('val result', after)
        self.assertTrue(after.startswith('\ufeff'))
        self.assertEqual(self.path.read_text(), text.replace('\r\n', '\n'))
        session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 2}, 'contentChanges': [{'text': after}]})
        current = session.handle('pyalamode/project', {})
        before_contract = before['regions'][0]['contract']
        after_contract = current['regions'][0]['contract']
        self.assertEqual(set(before_contract), set(FIELDS))
        self.assertEqual(before_contract, after_contract)
        self.assertEqual(session.handle('textDocument/formatting', self.format_params(session, 2)), [])
        self.assertEqual(current['report']['status'], 0)

    def test_LSP_formatting_version_and_freshness_refusal(self):
        from pyalamode.editor import ProtocolError
        session, _ = self.session(VECTOR.replace('val values', 'val    values'))
        stale = self.format_params(session)
        session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 2}, 'contentChanges': [{'text': VECTOR}]})
        with self.assertRaises(ProtocolError) as caught:
            session.handle('textDocument/formatting', stale)
        self.assertEqual(caught.exception.code, -32801)
        refused = VECTOR.replace('[1, 2]', '[x for x in (1, 2)]')
        session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 3}, 'contentChanges': [{'text': refused}]})
        with self.assertRaises(ProtocolError) as caught:
            session.handle('textDocument/formatting', self.format_params(session, 3))
        self.assertEqual(caught.exception.code, -32602)
        session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 4}, 'contentChanges': [{'text': VECTOR.replace('val values', 'val    values')}]})
        params = self.format_params(session, 4)
        from pyalamode import syntax
        original = syntax.format_source
        def changed(*args, **kwargs):
            value = original(*args, **kwargs)
            self.policy(POLICY + 'tasks=true\n')
            return value
        with patch.object(syntax, 'format_source', changed), self.assertRaises(ProtocolError) as caught:
            session.handle('textDocument/formatting', params)
        self.assertEqual(caught.exception.code, -32801)
        self.assertEqual(self.path.read_text(), VECTOR.replace('val values', 'val    values'))

    def test_sourceLocation_owned_artifact_relation(self):
        from pyalamode.project import build_paths
        self.source(VECTOR)
        out = self.root / 'built'
        built = build_paths([self.root], root=self.root, output=out)
        self.assertEqual(built.status, 0, built.to_dict())
        session, _ = self.session(VECTOR)
        report = session.handle('pyalamode/project', {})
        tree = ast.parse((out / 'core.py').read_bytes())
        target = next(node for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id == 'values')
        params = {'artifactUri': out.as_uri(), 'path': 'core.py', 'position': {'line': target.lineno - 1, 'character': target.col_offset}, 'snapshot': report['snapshot']}
        value = session.handle('pyalamode/sourceLocation', params)
        self.assertEqual(set(value), {'schema', 'snapshot', 'freshness', 'location', 'provenance'})
        self.assertEqual(value['provenance']['status'], 0)
        self.assertEqual(value['location']['uri'], self.path.as_uri())
        self.assertEqual(value['location']['range']['start'], {'line': 3, 'character': 8})
        original = (out / 'core.py').read_bytes()
        (out / 'core.py').write_bytes(original + b'\n# stale artifact\n')
        stale = session.handle('pyalamode/sourceLocation', params)
        self.assertEqual(stale['provenance']['status'], 1)
        self.assertIsNone(stale['location'])
        (out / 'core.py').write_bytes(original)
        params['path'] = '../core.py'
        malformed = session.handle('pyalamode/sourceLocation', params)
        self.assertEqual(malformed['provenance']['status'], 2)
        self.assertIsNone(malformed['location'])
        from pyalamode.editor import ProtocolError
        params['path'] = 'core.py'
        (out / 'core.py').write_bytes(original + b'\n# stale artifact\n')
        params['snapshot'] = '0' * 64
        with self.assertRaises(ProtocolError) as caught:
            session.handle('pyalamode/sourceLocation', params)
        self.assertEqual(caught.exception.code, -32801)
        params['snapshot'] = report['snapshot']
        for mutation in ('authored-disk', 'policy', 'extra-source'):
            with self.subTest(mutation=mutation):
                if mutation == 'authored-disk':
                    self.source(VECTOR + '\n# authored drift\n')
                elif mutation == 'policy':
                    self.policy(POLICY + 'tasks=true\n')
                else:
                    self.source('# mode: off\n', out / 'extra.py')
                with self.assertRaises(ProtocolError) as caught:
                    session.handle('pyalamode/sourceLocation', params)
                self.assertEqual(caught.exception.code, -32801)
                self.source(VECTOR)
                self.policy(POLICY)
                (out / 'extra.py').unlink(missing_ok=True)
        (out / 'core.py').write_bytes(original)
        self.source(VECTOR + '\n# authored drift with valid artifact\n')
        with self.assertRaises(ProtocolError) as caught:
            session.handle('pyalamode/sourceLocation', params)
        self.assertEqual(caught.exception.code, -32801)
        self.source(VECTOR)
        (out / 'core.py').write_bytes(original + b'\n# stale artifact\n')
        session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 2},
            'contentChanges': [{'text': VECTOR + '\n# overlay drift\n'}]})
        with self.assertRaises(ProtocolError) as caught:
            session.handle('pyalamode/sourceLocation', params)
        self.assertEqual(caught.exception.code, -32801)

    def test_editor_repair_complete43_and_binding_rows(self):
        text = '# mode: fun\ndef make(value:int)->int:\n    val result:int=value+1\n    val result:int=result+1\n    return result\n'
        session, _ = self.session(text)
        report = session.handle('pyalamode/project', {})
        old = next(row['contract'] for row in report['regions'] if row['name'] == 'make')
        preview = self.preview(session)
        self.assertEqual(preview['status'], 0, preview)
        self.assertIn('val result_2', preview['after'])
        self.assertIn('return result_2', preview['after'])
        self.assertEqual(self.path.read_text(), text)
        session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 2}, 'contentChanges': [{'text': preview['after']}]})
        after = session.handle('pyalamode/project', {})
        new = next(row['contract'] for row in after['regions'] if row['name'] == 'make')
        self.assertEqual(set(old), set(FIELDS))
        self.assertEqual(set(new), set(FIELDS))
        self.assertEqual([row['schema'] for row in new['data_assertions']], ['int', 'int'])
        self.assertEqual([row['name'] for row in new['data_assertions']], ['result', 'result_2'])
        self.assert_repair_relation(old, new, 'PAL101-AnnAssign')
        self.assertEqual(old['source_evidence'], 'unverified: audit or failed selected gate')
        self.assertEqual(new['source_evidence'], 'checked participating source')

        # An existing typed ValBinding receives only the fresh target token.
        self.assertEqual(preview['edits'][0]['newText'], 'result_2')
        self.assertEqual(preview['after'], text.replace('val result:int=result+1', 'val result_2:int=result+1').replace('return result', 'return result_2'))
        from pyalamode.editor import EditorSession, ProtocolError, _offset
        cases = (
            ('bare-Assign',
             '# mode: fun\ndef f(value: int) -> int:\n    val result = value\n    result = result + 1\n    return result\n',
             '# mode: fun\ndef f(value: int) -> int:\n    val result = value\n    val result_2 = result + 1\n    return result_2\n',
             'PAL101-Assign', 'val result_2'),
            ('bare-AnnAssign',
             '# mode: fun\ndef f(value: int) -> int:\n    val result: int = value\n    result: int = result + 1\n    return result\n',
             '# mode: fun\ndef f(value: int) -> int:\n    val result: int = value\n    val result_2: int = result + 1\n    return result_2\n',
             'PAL101-AnnAssign', 'val result_2'),
            ('existing-untyped-ValBinding',
             '# mode: fun\ndef f(value: int) -> int:\n    val result = value\n    val result = result + 1\n    return result\n',
             '# mode: fun\ndef f(value: int) -> int:\n    val result = value\n    val result_2 = result + 1\n    return result_2\n',
             'PAL101-Assign', 'result_2'),
        )
        for label, sample, expected, repair, target_text in cases:
            with self.subTest(declaration=label):
                session, _ = self.session(sample)
                report = session.handle('pyalamode/project', {})
                self.assertEqual([row['code'] for row in report['diagnostics']], ['PAL101'])
                old = next(row['contract'] for row in report['regions'] if row['name'] == 'f')
                value = self.preview(session)
                self.assertEqual(value['before'], sample)
                self.assertEqual(value['after'], expected)
                self.assertEqual((value['status'], value['remainingDiagnostics']), (0, []))
                self.assertEqual([row['newText'] for row in value['edits']], [target_text, 'result_2'])
                edited = sample
                for row in reversed(value['edits']):
                    start, end = _offset(sample, row['range']['start']), _offset(sample, row['range']['end'])
                    edited = edited[:start] + row['newText'] + edited[end:]
                self.assertEqual(edited, expected)
                self.assertEqual(self.path.read_bytes(), sample.encode('utf-8'))
                session.handle('textDocument/didChange', {'textDocument': {'uri': self.path.as_uri(), 'version': 2}, 'contentChanges': [{'text': value['after']}]})
                current = session.handle('pyalamode/project', {})
                self.assertEqual((current['report']['status'], current['diagnostics']), (0, []))
                new = next(row['contract'] for row in current['regions'] if row['name'] == 'f')
                self.assert_repair_relation(old, new, repair)
                self.assertEqual(new['data_assertions'], [{'line': 3, 'name': 'result', 'schema': 'int'}, {'line': 4, 'name': 'result_2', 'schema': 'int'}])

        # A fresh val in a semicolon chain remains unsupported by the grammar.
        same_line = '# mode: fun\ndef f(value: str) -> str:\n    val result = "\U0001f600"\n    "\U0001f600abcdefghi"; result = result + "caf\u00e9"\n    return result\n'
        session, _ = self.session(same_line)
        report = session.handle('pyalamode/project', {})
        self.assertEqual([row['code'] for row in report['diagnostics']], ['PAL101'])
        self.assertEqual(report['diagnostics'][0]['range']['start'], {'line': 3, 'character': 19})
        with self.assertRaises(ProtocolError) as caught:
            self.preview(session)
        self.assertEqual(caught.exception.code, -32602)
        self.assertEqual(str(caught.exception), 'candidate does not pass the complete current strict project gate')
        self.assertEqual(self.path.read_bytes(), same_line.encode('utf-8'))

        # The compatible .py target keeps the original rename-only bytes.
        self.path.unlink()
        ordinary = self.root / 'ordinary.py'
        ordinary_before = '# mode: fun\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n'
        ordinary_after = '# mode: fun\ndef f(value: int) -> int:\n    result = value\n    result_2 = result + 1\n    return result_2\n'
        self.source(ordinary_before, ordinary)
        session = EditorSession(self.root)
        session.handle('initialize', {'rootUri': self.root.as_uri()})
        session.handle('textDocument/didOpen', {'textDocument': {'uri': ordinary.as_uri(), 'languageId': 'python', 'version': 1, 'text': ordinary_before}})
        report = session.handle('pyalamode/project', {})
        self.assertEqual([row['code'] for row in report['diagnostics']], ['PAL101'])
        old = next(row['contract'] for row in report['regions'] if row['name'] == 'f')
        finding = report['diagnostics'][0]
        value = session.handle('pyalamode/preview', {'uri': ordinary.as_uri(), 'version': 1, 'snapshot': report['snapshot'], 'diagnosticIndex': finding['data']['diagnosticIndex']})
        self.assertEqual((value['before'], value['after'], value['status'], value['remainingDiagnostics']), (ordinary_before, ordinary_after, 0, []))
        self.assertEqual([row['newText'] for row in value['edits']], ['result_2', 'result_2'])
        self.assertNotIn('val ', value['after'])
        self.assertEqual(ordinary.read_bytes(), ordinary_before.encode('utf-8'))
        session.handle('textDocument/didChange', {'textDocument': {'uri': ordinary.as_uri(), 'version': 2}, 'contentChanges': [{'text': value['after']}]})
        current = session.handle('pyalamode/project', {})
        self.assertEqual((current['report']['status'], current['diagnostics']), (0, []))
        new = next(row['contract'] for row in current['regions'] if row['name'] == 'f')
        self.assert_repair_relation(old, new, 'PAL101-Assign')
