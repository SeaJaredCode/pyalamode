'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vscode = require('vscode');
const {execFileSync} = require('node:child_process');

async function eventually(probe, message) {
  const deadline = Date.now() + 5000;
  while (Date.now() < deadline) { const result = probe(); if (result) return result; await new Promise(resolve => setTimeout(resolve, 25)); }
  assert.fail(message);
}

let state = {}, running;
async function restricted() {
  assert.equal(vscode.workspace.isTrusted, false);
  const root = vscode.workspace.workspaceFolders[0].uri.fsPath, marker = path.join(root, 'unexpected-child');
  const launcher = path.join(root, 'must-not-launch');
  fs.writeFileSync(launcher, '#!/bin/sh\nprintf launched > ' + JSON.stringify(marker) + '\nexit 1\n', {mode: 0o755});
  fs.writeFileSync(path.join(root, 'core.py'), '# mode: fun\ndef f()->int:return 1\n');
  await vscode.workspace.getConfiguration('pyalamode').update('pythonPath', launcher, vscode.ConfigurationTarget.Global);
  const extension = vscode.extensions.getExtension('pyalamode-local.pyalamode-local');
  assert.ok(extension); assert.equal(extension.packageJSON.capabilities.untrustedWorkspaces.supported, false);
  await vscode.workspace.openTextDocument(vscode.Uri.file(path.join(root, 'core.py')));
  await new Promise(resolve => setTimeout(resolve, 500));
  // The Development Host may load a development module despite its manifest
  // restriction. The client trust gate must still refuse every tool launch.
  assert.equal(extension.exports.client, undefined); assert.equal(fs.existsSync(marker), false);
  await assert.rejects(extension.exports.ensure(), /trusted local workspace/);
  assert.equal(extension.exports.client, undefined); assert.equal(fs.existsSync(marker), false);
  if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify({vscode: vscode.version, node: process.version, trusted: false, configuredExecutable: launcher, extensionActive: extension.isActive, childSentinel: false, actual_api: true}, null, 2));
}
async function run() {
  assert.equal(vscode.env.remoteName, undefined); assert.equal(vscode.env.uiKind, vscode.UIKind.Desktop);
  const root = vscode.workspace.workspaceFolders[0].uri.fsPath;
  const python = process.env.PYALAMODE_CLIENT_PYTHON;
  assert.ok(path.isAbsolute(python));
  const clean = '# mode: fun\n\ndef add(value: int) -> int:\n    return value + 1\n';
  const caller = '# mode: fun\nfrom core import add as plus\n\ndef caller(value: int) -> int:\n    return plus(value)\n';
  const bad = '# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n';
  fs.writeFileSync(path.join(root, 'core.py'), clean);
  fs.writeFileSync(path.join(root, 'caller.py'), caller);
  fs.writeFileSync(path.join(root, 'bad.py'), bad);
  fs.writeFileSync(path.join(root, 'effect.py'), 'from pyalamode import effects, Clock, ClockCapability\n@effects(Clock)\ndef stamp(clock:ClockCapability)->int:return clock.now_ns()\n');
  fs.writeFileSync(path.join(root, 'pyproject.toml'), '[tool.pyalamode]\nboundary_guards="exports"\nguarded_exports=["core:add"]\n');
  fs.writeFileSync(path.join(root, 'sentinel_source.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, 'sentinel'))}).write_text('evaluated')\n`);
  await vscode.workspace.getConfiguration('pyalamode').update('pythonPath', python, vscode.ConfigurationTarget.Global);
  const extension = vscode.extensions.getExtension('pyalamode-local.pyalamode-local');
  assert.ok(extension);
  const api = await extension.activate(); await api.ensure();
  running = api;
  const wire = []; api.client.on('wire', row => wire.push(row));
  state = {root, wire, provenance: api.client.provenance};
  const uri = vscode.Uri.file(path.join(root, 'bad.py'));
  const canonicalUri = vscode.Uri.file(fs.realpathSync(uri.fsPath)).toString();
  const document = await vscode.workspace.openTextDocument(uri); await vscode.window.showTextDocument(document);
  state.document = {uri: document.uri.toString(), language: document.languageId, version: document.version};
  const report = await vscode.commands.executeCommand('pyalamode.refresh');
  assert.equal(report.schema, 1); assert.equal(report.report.status, 1);
  const findings = await eventually(() => {
    const current = vscode.languages.getDiagnostics(uri);
    return current.some(item => item.code === 'PAL101') && current;
  }, 'actual Problems collection never published PAL101');
  assert.ok(findings.some(item => item.code === 'PAL101'));
  assert.ok(wire.some(row => row.direction === 'client' && row.message.method === 'textDocument/didOpen' && row.message.params.textDocument.uri === canonicalUri));
  const hovers = await vscode.commands.executeCommand('vscode.executeHoverProvider', uri, new vscode.Position(2, 5));
  state.hovers = hovers.map(item => ({contents: item.contents.map(content => typeof content === 'string' ? content : content.value), range: item.range}));
  assert.ok(state.hovers.some(item => item.contents.some(content => content.includes('unverified'))));
  const symbols = await vscode.commands.executeCommand('vscode.executeDocumentSymbolProvider', uri);
  assert.ok(symbols.some(item => item.name === 'f'));
  const callUri = vscode.Uri.file(path.join(root, 'caller.py'));
  await vscode.workspace.openTextDocument(callUri);
  const definitions = await vscode.commands.executeCommand('vscode.executeDefinitionProvider', callUri, new vscode.Position(4, 12));
  assert.ok(definitions.some(item => (item.uri || item.targetUri).fsPath.endsWith('core.py')));
  const references = await vscode.commands.executeCommand('vscode.executeReferenceProvider', vscode.Uri.file(path.join(root, 'core.py')), new vscode.Position(2, 5));
  assert.ok(references.some(item => item.uri.fsPath.endsWith('caller.py')));
  const actions = await vscode.commands.executeCommand('vscode.executeCodeActionProvider', uri, new vscode.Range(4, 4, 4, 10));
  const action = actions.find(item => item.command === 'pyalamode.preview' || item.command?.command === 'pyalamode.preview');
  assert.ok(action);
  const command = typeof action.command === 'string' ? action : action.command;
  const preview = await vscode.commands.executeCommand(command.command, ...command.arguments);
  assert.equal(preview.before, bad); assert.notEqual(preview.after, bad);
  assert.equal(document.getText(), bad); assert.equal(fs.readFileSync(uri.fsPath, 'utf8'), bad);
  const beforeView = vscode.workspace.textDocuments.find(item => item.uri.scheme === 'pyalamode-view' && item.uri.path.endsWith('/before.py'));
  const afterView = vscode.workspace.textDocuments.find(item => item.uri.scheme === 'pyalamode-view' && item.uri.path.endsWith('/proposed.py'));
  assert.ok(beforeView); assert.ok(afterView); assert.equal(beforeView.getText(), bad); assert.equal(afterView.getText(), preview.after);
  // This is an explicit test-user edit to the authored document, not an
  // extension fix/apply operation. It exercises real didChange/version flow.
  const edit = new vscode.WorkspaceEdit(); edit.replace(uri, new vscode.Range(document.positionAt(0), document.positionAt(document.getText().length)), preview.after);
  assert.equal(await vscode.workspace.applyEdit(edit), true);
  const repaired = await vscode.commands.executeCommand('pyalamode.refresh');
  assert.equal(repaired.report.status, 0); assert.ok(repaired.freshness.includes('unsaved'));
  assert.ok(wire.some(row => row.direction === 'client' && row.message.method === 'textDocument/didChange' && row.message.params.textDocument.version === document.version));
  assert.equal(repaired.inputs.sources[fs.realpathSync(uri.fsPath)].version, document.version);
  assert.equal(fs.readFileSync(uri.fsPath, 'utf8'), bad);
  assert.equal(await vscode.commands.executeCommand(command.command, ...command.arguments), undefined);
  const contracts = await vscode.commands.executeCommand('pyalamode.contracts');
  assert.ok(contracts.regions.length); assert.ok(vscode.workspace.textDocuments.some(item => item.uri.scheme === 'pyalamode-view' && item.uri.path.endsWith('/contracts.json')));
  const effect = contracts.regions.find(item => item.name === 'stamp').contract;
  assert.deepEqual(effect.required_effects, ['Clock']); assert.ok(effect.effect_origins.Clock);
  for (const field of ['source_evidence', 'failures', 'trust', 'external_assumptions', 'caller_obligations', 'effect_bound']) assert.ok(Object.hasOwn(effect, field));
  const explained = await vscode.commands.executeCommand('pyalamode.explain', 'PAL101'); assert.ok(explained.text.includes('binding'));
  // An explicit test-user save enables a real current selected-guard build.
  assert.equal(await document.save(), true);
  await vscode.commands.executeCommand('pyalamode.refresh');
  const artifact = path.join(root, 'build', 'guarded');
  const built = JSON.parse(execFileSync(python, ['-I', '-m', 'pyalamode', 'build', path.join(root, 'core.py'), '--root', root, '--output', artifact, '--json'], {cwd: root, encoding: 'utf8'}));
  assert.equal(built.status, 0);
  const guarded = await vscode.commands.executeCommand('pyalamode.guardLocation', {artifactUri: vscode.Uri.file(artifact).toString(), publicBoundary: 'pyalamode_exports.core:add', phase: 'argument', name: 'value'});
  assert.equal(guarded.location.uri, vscode.Uri.file(fs.realpathSync(path.join(root, 'core.py'))).toString());
  assert.equal(guarded.location.range.start.line, 2);
  assert.equal(vscode.window.activeTextEditor.document.uri.fsPath, path.join(root, 'core.py'));
  assert.equal(vscode.window.activeTextEditor.selection.start.line, 2);
  const unicode = '# mode: fun\r\n\r\ndef café() -> str:\r\n    result = "😀"; result = "café"\r\n    return result\r\n';
  const unicodeUri = vscode.Uri.file(path.join(root, 'unicode.py')); fs.writeFileSync(unicodeUri.fsPath, unicode);
  const unicodeDocument = await vscode.workspace.openTextDocument(unicodeUri);
  await vscode.commands.executeCommand('pyalamode.refresh');
  const unicodeFindings = await eventually(() => {
    const rows = vscode.languages.getDiagnostics(unicodeUri); return rows.some(item => item.code === 'PAL101') && rows;
  }, 'astral/CRLF Problems diagnostic missing');
  const rebinding = unicodeFindings.find(item => item.code === 'PAL101');
  assert.equal(rebinding.range.start.line, 3); assert.equal(rebinding.range.start.character, unicodeDocument.lineAt(3).text.lastIndexOf('result'));
  const unicodeEdit = new vscode.WorkspaceEdit(); unicodeEdit.replace(unicodeUri, new vscode.Range(unicodeDocument.positionAt(0), unicodeDocument.positionAt(unicode.length)), '# mode: fun\r\n\r\ndef café() -> str:\r\n    return "café"\r\n');
  assert.equal(await vscode.workspace.applyEdit(unicodeEdit), true);
  assert.equal((await vscode.commands.executeCommand('pyalamode.refresh')).report.status, 0);
  const previous = api.client.child.pid;
  await vscode.commands.executeCommand('pyalamode.restart'); assert.notEqual(api.client.child.pid, previous);
  const bootstrapMarkers = ['workspace-bootstrap-sentinel', 'path-bootstrap-sentinel', 'startup-bootstrap-sentinel'];
  fs.mkdirSync(path.join(root, 'pyalamode')); fs.mkdirSync(path.join(root, 'bootstrap-poison'));
  fs.writeFileSync(path.join(root, 'pyalamode', '__init__.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, bootstrapMarkers[0]))}).write_text('workspace package executed')\n`);
  fs.writeFileSync(path.join(root, 'bootstrap-poison', 'sitecustomize.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, bootstrapMarkers[1]))}).write_text('startup import executed')\n`);
  const startup = path.join(root, 'bootstrap-poison', 'startup.py');
  fs.writeFileSync(startup, `from pathlib import Path\nPath(${JSON.stringify(path.join(root, bootstrapMarkers[2]))}).write_text('startup script executed')\n`);
  const original = {PYTHONPATH: process.env.PYTHONPATH, PYTHONSTARTUP: process.env.PYTHONSTARTUP};
  process.env.PYTHONPATH = path.join(root, 'bootstrap-poison'); process.env.PYTHONSTARTUP = startup;
  try { await vscode.commands.executeCommand('pyalamode.restart'); await api.ensure(); }
  finally { for (const [key, value] of Object.entries(original)) { if (value === undefined) delete process.env[key]; else process.env[key] = value; } }
  assert.deepEqual(api.client.args, ['-I', '-m', 'pyalamode.editor', '--stdio', '--root', fs.realpathSync(root)]);
  for (const marker of bootstrapMarkers) assert.equal(fs.existsSync(path.join(root, marker)), false);
  assert.equal(fs.existsSync(path.join(root, 'sentinel')), false);
  const packet = {vscode: vscode.version, node: process.version, execPath: process.execPath, versions: process.versions, localDesktop: {remoteName: vscode.env.remoteName ?? null, uiKind: vscode.env.uiKind}, provenance: api.client.provenance, wire, source_before: bad, hovers: state.hovers, preview, repairedStatus: repaired.report.status, effect, guarded, unicodeRange: rebinding.range, bootstrapSentinels: Object.fromEntries(bootstrapMarkers.map(marker => [marker, false])), sentinel: false, actual_api: true};
  if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify(packet, null, 2));
  await api.dispose();
}
exports.run = async () => {
  try { if (process.env.PYALAMODE_CLIENT_RESTRICTED === '1') await restricted(); else await run(); }
  catch (error) {
    if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify({...state, error: String(error), stack: error.stack}, null, 2));
    if (running) await running.dispose();
    throw error;
  }
};
