'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vscode = require('vscode');
const {spawnSync} = require('node:child_process');
const {createHash} = require('node:crypto');
const failureRecord = error => error ? {name: error.name, message: error.message, code: error.code ?? null, stack: error.stack ?? null} : null;
function observation(name, fixtures) {
  if (!['trusted-host', 'restricted-host'].includes(name)) throw new Error('Unknown fixed observation case');
  const report = process.env.PYALAMODE_CLIENT_REPORT;
  if (typeof report !== 'string' || !path.isAbsolute(report)) throw new Error('Actual observations require a root-supplied absolute report path');
  const parent = fs.realpathSync(path.dirname(report)), workspace = fs.realpathSync(path.resolve(__dirname, '../../..'));
  const contained = (base, candidate) => { const value = path.relative(base, candidate); return value === '' || (!value.startsWith('..' + path.sep) && value !== '..' && !path.isAbsolute(value)); };
  if (contained(workspace, parent) || fixtures.some(root => contained(fs.realpathSync(root), parent)))
    throw new Error('Observation report must be outside source and fixture roots');
  const base = path.join(parent, path.basename(report) + '.observations');
  if (fs.existsSync(base)) {
    if (!fs.lstatSync(base).isDirectory() || fs.lstatSync(base).isSymbolicLink()) throw new Error('Invalid observation directory');
  } else fs.mkdirSync(base, {mode: 0o700});
  const directory = path.join(base, name); fs.mkdirSync(directory, {mode: 0o700});
  const write = (filename, value) => fs.writeFileSync(path.join(directory, filename), JSON.stringify(value, null, 2) + '\n', {flag: 'wx', mode: 0o600});
  write('intent.json', {schema: 1, case: name, report, directory, fixtures, fixtureOwnership: 'fresh isolated paths supplied or created by this fixed controller'});
  let sequence = 0;
  const streams = [], MAX_STREAM = 16 * 1024 * 1024;
  const streamSnapshot = close => streams.map(item => {
    if (close && !item.closed) {
      item.stream.removeListener('data', item.data); item.stream.removeListener('end', item.end);
      fs.closeSync(item.fd); item.closed = true;
    }
    const raw = fs.readFileSync(item.path);
    return {path: item.path, direction: item.direction, capture_start: item.captureStart, initial_prefix_unobservable: item.missingPrefix,
      observed_bytes: item.observed, retained_bytes: raw.length, sha256: createHash('sha256').update(raw).digest('hex'),
      byte_cap: MAX_STREAM, stream_end_observed: item.ended, capture_error: item.error,
      child_exit_code: item.client.child.exitCode, child_signal_code: item.client.child.signalCode,
      capture_closed: item.closed};
  });
  return {
    directory,
    transport(client, captureStart, missingPrefix) {
      const index = streams.length / 2 + 1;
      for (const [direction, stream] of [['stdout', client.child.stdout], ['stderr', client.child.stderr]]) {
        const filename = path.join(directory, 'transport-' + index + '-' + direction + '.bin');
        const item = {client, stream, direction, path: filename, fd: fs.openSync(filename, 'wx', 0o600),
          captureStart, missingPrefix, observed: 0, retained: 0, ended: false, closed: false, error: null};
        item.end = () => { item.ended = true; };
        item.data = chunk => {
          item.observed += chunk.length;
          try {
            const selected = chunk.subarray(0, Math.max(0, MAX_STREAM - item.retained));
            let offset = 0;
            while (offset < selected.length) { const count = fs.writeSync(item.fd, selected, offset, selected.length - offset); if (!count) throw new Error('Transport raw write made no progress'); offset += count; }
            item.retained += selected.length;
            if (selected.length !== chunk.length) throw new Error('Transport raw observation exceeded 16MiB byte cap');
          } catch (error) { if (!item.error) item.error = failureRecord(error); client.fail(error); }
        };
        streams.push(item); stream.on('data', item.data); stream.on('end', item.end);
      }
    },
    child(label, argv, cwd) {
      if (!/^[a-z][a-z0-9-]{0,63}$/.test(label) || !Array.isArray(argv) || argv.length < 1 || argv.length > 64 ||
          !argv.every(value => typeof value === 'string' && value.length <= 16384) || !path.isAbsolute(argv[0]) || !path.isAbsolute(cwd))
        throw new Error('Invalid fixed child invocation');
      const childDirectory = path.join(directory, String(++sequence).padStart(2, '0') + '-' + label);
      fs.mkdirSync(childDirectory, {mode: 0o700});
      const env = {...process.env}, intent = {schema: 1, label, argv, cwd, env, shell: false, timeout_ms: 60000, max_buffer_bytes: 16 * 1024 * 1024};
      fs.writeFileSync(path.join(childDirectory, 'intent.json'), JSON.stringify(intent, null, 2) + '\n', {flag: 'wx', mode: 0o600});
      let result, thrown;
      try { result = spawnSync(argv[0], argv.slice(1), {cwd, env, shell: false, stdio: ['ignore', 'pipe', 'pipe'], timeout: intent.timeout_ms, maxBuffer: intent.max_buffer_bytes}); }
      catch (error) { thrown = error; }
      const stdout = result?.stdout ?? Buffer.alloc(0), stderr = result?.stderr ?? Buffer.alloc(0);
      fs.writeFileSync(path.join(childDirectory, 'stdout.bin'), stdout, {flag: 'wx', mode: 0o600});
      fs.writeFileSync(path.join(childDirectory, 'stderr.bin'), stderr, {flag: 'wx', mode: 0o600});
      const identity = raw => ({byte_count: raw.length, sha256: createHash('sha256').update(raw).digest('hex')});
      const finish = {schema: 1, status: result?.status ?? null, signal: result?.signal ?? null, error: failureRecord(thrown || result?.error),
        stdout: identity(stdout), stderr: identity(stderr), stdout_was_null: !result || result.stdout === null,
        stderr_was_null: !result || result.stderr === null};
      fs.writeFileSync(path.join(childDirectory, 'finish.json'), JSON.stringify(finish, null, 2) + '\n', {flag: 'wx', mode: 0o600});
      if (thrown) throw thrown;
      if (result.error) throw result.error;
      if (result.status !== 0) throw new Error('Observed child failed: ' + label + ' (' + result.status + ', ' + result.signal + ')');
      return stdout.toString('utf8');
    },
    retain(value) { write('partial.json', {schema: 1, case: name, ...value, transports: streamSnapshot(false)}); },
    finish(value) {
      const transports = streamSnapshot(true), captureFailure = transports.some(item => item.capture_error);
      write('finish.json', {schema: 1, case: name, ...value, passed: value.passed && !captureFailure, transports});
      if (captureFailure && !value.error) throw new Error('Transport raw capture failed; retained observation is unverified');
    }
  };
}

async function eventually(probe, message) {
  const deadline = Date.now() + 5000;
  while (Date.now() < deadline) { const result = probe(); if (result) return result; await new Promise(resolve => setTimeout(resolve, 25)); }
  assert.fail(message);
}

let state = {}, running, observer;
async function restricted() {
  state = {mode: 'restricted-host', phase: 'preflight', trusted: vscode.workspace.isTrusted};
  assert.equal(vscode.workspace.isTrusted, false);
  const root = vscode.workspace.workspaceFolders[0].uri.fsPath, marker = path.join(root, 'unexpected-child');
  const launcher = path.join(root, 'must-not-launch');
  Object.assign(state, {root, marker, launcher, fixtureIntent: 'root-supplied fresh isolated restricted workspace/profile'});
  observer = observation('restricted-host', [root]);
  const quotedMarker = "'" + marker.replace(/'/g, "'\"'\"'") + "'";
  fs.writeFileSync(launcher, '#!/bin/sh\nprintf launched > ' + quotedMarker + '\nexit 1\n', {mode: 0o755});
  fs.writeFileSync(path.join(root, 'core.py'), '# mode: fun\ndef f()->int:return 1\n');
  fs.writeFileSync(path.join(root, 'dialect.pya'), '# mode: fun\ndef f()->int:\n    val answer = 1\n    return answer\n');
  await vscode.workspace.getConfiguration('pyalamode').update('pythonPath', launcher, vscode.ConfigurationTarget.Global);
  const extension = vscode.extensions.getExtension('pyalamode-local.pyalamode-local');
  state.extensionAvailable = Boolean(extension);
  assert.ok(extension); assert.equal(extension.packageJSON.capabilities.untrustedWorkspaces.supported, false);
  assert.deepEqual(extension.packageJSON.activationEvents, ['onLanguage:python', 'onLanguage:pyalamode']);
  await vscode.workspace.openTextDocument(vscode.Uri.file(path.join(root, 'core.py')));
  const dialect = await vscode.workspace.openTextDocument(vscode.Uri.file(path.join(root, 'dialect.pya')));
  assert.equal(dialect.languageId, 'pyalamode');
  await new Promise(resolve => setTimeout(resolve, 500));
  // The Development Host may load a development module despite its manifest
  // restriction. The client trust gate must still refuse every tool launch.
  assert.equal(extension.exports.client, undefined); assert.equal(fs.existsSync(marker), false);
  Object.assign(state, {phase: 'restriction-observed', extensionActive: extension.isActive, childSentinel: fs.existsSync(marker), dialectLanguage: dialect.languageId});
  await assert.rejects(extension.exports.ensure(), /trusted local workspace/);
  assert.equal(extension.exports.client, undefined); assert.equal(fs.existsSync(marker), false);
  state.phase = 'passed';
  if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify({vscode: vscode.version, node: process.version, trusted: false, configuredExecutable: launcher, extensionActive: extension.isActive, dialectLanguage: dialect.languageId, childSentinel: false, actual_api: true}, null, 2));
}
async function run() {
  state = {mode: 'trusted-host', phase: 'preflight'};
  assert.equal(vscode.env.remoteName, undefined); assert.equal(vscode.env.uiKind, vscode.UIKind.Desktop);
  const root = vscode.workspace.workspaceFolders[0].uri.fsPath;
  Object.assign(state, {root, fixtureIntent: 'root-supplied fresh isolated trusted workspace/profile'});
  observer = observation('trusted-host', [root]);
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
  const wire = []; state.wire = wire;
  const api = await extension.activate(); running = api;
  state.phase = 'activated';
  const ensuring = api.ensure(), initialClient = api.client;
  state.launch = initialClient ? {python: initialClient.python, args: initialClient.args, cwd: initialClient.root,
    pid: initialClient.child.pid ?? null} : null;
  if (initialClient) { initialClient.on('wire', row => wire.push(row)); observer.transport(initialClient, 'after activation exports returned, before awaiting ensure', true); }
  await ensuring;
  if (api.client !== initialClient) { api.client.on('wire', row => wire.push(row)); observer.transport(api.client, 'after awaited ensure returned new client', true); }
  Object.assign(state, {phase: 'ready', provenance: api.client.provenance});
  assert.equal(api.client.provenance.server.capabilities.experimental.pyalamode.schema, 2);
  assert.equal(api.client.provenance.server.capabilities.experimental.pyalamode.pythonVersion, '3.13.1');
  assert.equal(Object.keys(api.client.provenance.server.capabilities.experimental.pyalamode).length, 12);
  assert.deepEqual(api.client.provenance.server.capabilities.experimental.pyalamode.languages, ['python', 'pyalamode']);
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
  const built = JSON.parse(observer.child('compatible-build', [python, '-I', '-m', 'pyalamode', 'build', path.join(root, 'core.py'), '--root', root, '--output', artifact, '--json'], root));
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
  // The following writes/edits are explicit test-user actions in the isolated
  // fixture. The extension itself exposes no source or policy apply command.
  assert.equal(await unicodeDocument.save(), true);
  const dialectPolicy = '[tool.pyalamode]\nschema=1\nedition="pyalamode-v1-experimental"\n';
  fs.writeFileSync(path.join(root, 'pyproject.toml'), dialectPolicy);
  const dialectSource = '# mode: fun\r\n\r\ndef café() -> str:\r\n    val  result = "😀"  \r\n    "😀abcdefghi"; result = result + "café"\r\n    return result\r\n';
  const dialectUri = vscode.Uri.file(path.join(root, 'dialect.pya')), dialectCallerUri = vscode.Uri.file(path.join(root, 'dialect_caller.pya'));
  fs.writeFileSync(dialectUri.fsPath, dialectSource);
  const dialectDocument = await vscode.workspace.openTextDocument(dialectUri);
  await vscode.window.showTextDocument(dialectDocument);
  assert.equal(dialectDocument.languageId, 'pyalamode');
  assert.ok(extension.packageJSON.contributes.grammars.some(row => row.language === 'pyalamode' && row.scopeName === 'source.pyalamode'));
  const dialectReport = await vscode.commands.executeCommand('pyalamode.refresh');
  const dialectFindings = await eventually(() => {
    const rows = vscode.languages.getDiagnostics(dialectUri); return rows.some(row => row.code === 'PAL101') && rows;
  }, 'dialect UTF16 Problems diagnostic missing');
  const dialectRebinding = dialectFindings.find(row => row.code === 'PAL101');
  assert.equal(dialectRebinding.range.start.line, 4); assert.equal(dialectRebinding.range.start.character, 19);
  assert.ok(wire.some(row => row.direction === 'client' && row.message.method === 'textDocument/didOpen' &&
    row.message.params.textDocument.languageId === 'pyalamode' && row.message.params.textDocument.uri.endsWith('/dialect.pya')));
  const dialectHovers = await vscode.commands.executeCommand('vscode.executeHoverProvider', dialectUri, new vscode.Position(2, 5));
  assert.ok(dialectHovers.some(item => item.contents.some(content => String(content.value ?? content).includes('unverified'))));
  // This is an explicit test-user source edit after the original UTF16 finding.
  const dialectRepairSource = '# mode: fun\r\n\r\ndef café() -> str:\r\n    val  result = "😀"  \r\n    result = result + "café"\r\n    return result\r\n';
  const dialectStageVersion = dialectDocument.version, dialectStage = new vscode.WorkspaceEdit();
  dialectStage.replace(dialectUri, new vscode.Range(dialectDocument.positionAt(0), dialectDocument.positionAt(dialectDocument.getText().length)), dialectRepairSource);
  assert.equal(await vscode.workspace.applyEdit(dialectStage), true);
  const dialectRepairReport = await vscode.commands.executeCommand('pyalamode.refresh');
  assert.ok(dialectDocument.version > dialectStageVersion); assert.equal(dialectDocument.getText(), dialectRepairSource);
  assert.equal(dialectRepairReport.inputs.sources[fs.realpathSync(dialectUri.fsPath)].version, dialectDocument.version);
  const dialectRepairDiagnostic = dialectRepairReport.diagnostics.find(item => item.uri === dialectUri.toString() && item.code === 'PAL101');
  assert.ok(dialectRepairDiagnostic); assert.deepEqual(dialectRepairDiagnostic.range.start, {line: 4, character: 4});
  assert.equal(dialectRepairReport.report.status, 1); assert.equal(fs.readFileSync(dialectUri.fsPath, 'utf8'), dialectSource);
  const dialectActions = await vscode.commands.executeCommand('vscode.executeCodeActionProvider', dialectUri, new vscode.Range(4, 4, 4, 10));
  const dialectAction = dialectActions.find(item => item.command === 'pyalamode.preview' || item.command?.command === 'pyalamode.preview');
  assert.ok(dialectAction);
  const dialectCommand = typeof dialectAction.command === 'string' ? dialectAction : dialectAction.command;
  assert.equal(dialectCommand.arguments[0].version, dialectDocument.version); assert.equal(dialectCommand.arguments[0].snapshot, dialectRepairReport.snapshot);
  const dialectPreview = await vscode.commands.executeCommand(dialectCommand.command, ...dialectCommand.arguments);
  assert.equal(dialectPreview.before, dialectRepairSource); assert.notEqual(dialectPreview.after, dialectRepairSource);
  assert.equal(dialectDocument.getText(), dialectRepairSource); assert.equal(fs.readFileSync(dialectUri.fsPath, 'utf8'), dialectSource);
  assert.ok(dialectPreview.after.includes('    val result_2 = result + "café"\r\n')); assert.ok(dialectPreview.after.includes('    return result_2\r\n'));
  assert.equal(dialectPreview.status, 0); assert.deepEqual(dialectPreview.remainingDiagnostics, []);
  assert.ok(vscode.workspace.textDocuments.some(item => item.uri.scheme === 'pyalamode-view' && item.uri.path.endsWith('/proposed.pya') && item.getText() === dialectPreview.after));
  const dialectEdit = new vscode.WorkspaceEdit();
  dialectEdit.replace(dialectUri, new vscode.Range(dialectDocument.positionAt(0), dialectDocument.positionAt(dialectRepairSource.length)), dialectPreview.after);
  assert.equal(await vscode.workspace.applyEdit(dialectEdit), true);
  fs.writeFileSync(dialectCallerUri.fsPath, '# mode: fun\nfrom dialect import café\ndef call() -> str:\n    return café()\n');
  await vscode.workspace.openTextDocument(dialectCallerUri);
  assert.equal((await vscode.commands.executeCommand('pyalamode.refresh')).report.status, 0);
  const dialectDefinitions = await vscode.commands.executeCommand('vscode.executeDefinitionProvider', dialectCallerUri, new vscode.Position(3, 12));
  assert.ok(dialectDefinitions.some(item => (item.uri || item.targetUri).fsPath === dialectUri.fsPath));
  const dialectReferences = await vscode.commands.executeCommand('vscode.executeReferenceProvider', dialectUri, new vscode.Position(2, 5));
  assert.ok(dialectReferences.some(item => item.uri.fsPath === dialectCallerUri.fsPath));
  assert.equal(await vscode.commands.executeCommand(dialectCommand.command, ...dialectCommand.arguments), undefined);
  const dialectOptions = {tabSize: 4, insertSpaces: true}, beforeFormat = dialectDocument.getText(), formatVersion = dialectDocument.version;
  const dialectFormat = await vscode.commands.executeCommand('vscode.executeFormatDocumentProvider', dialectUri, dialectOptions);
  assert.ok(dialectFormat.length); assert.equal(dialectDocument.getText(), beforeFormat);
  assert.equal(fs.readFileSync(dialectUri.fsPath, 'utf8'), dialectSource);
  const guardedFormat = wire.filter(row => row.direction === 'client' && row.message.method === 'textDocument/formatting').at(-1).message.params;
  assert.equal(guardedFormat.pyalamode.version, formatVersion); assert.match(guardedFormat.pyalamode.snapshot, /^[0-9a-f]{64}$/);
  await assert.rejects(api.client.request('textDocument/formatting', {...guardedFormat,
    pyalamode: {version: formatVersion - 1, snapshot: guardedFormat.pyalamode.snapshot}}), /-32801/);
  // Let the real server produce nonempty edits, then change the buffer through
  // a test-user action before the provider receives that exact response.
  const originalRequest = api.client.request, versionBeforeRace = dialectDocument.version;
  let serverRaceEdits;
  api.client.request = async function(method, ...args) {
    const result = await originalRequest.call(this, method, ...args);
    if (method === 'textDocument/formatting' && serverRaceEdits === undefined) {
      serverRaceEdits = result;
      const userEdit = new vscode.WorkspaceEdit(); userEdit.insert(dialectUri, dialectDocument.positionAt(dialectDocument.getText().length), '# explicit test-user version change\r\n');
      assert.equal(await vscode.workspace.applyEdit(userEdit), true);
    }
    return result;
  };
  let withheld;
  try { withheld = await vscode.commands.executeCommand('vscode.executeFormatDocumentProvider', dialectUri, dialectOptions); }
  finally { api.client.request = originalRequest; }
  assert.ok(serverRaceEdits.length); assert.equal(withheld, undefined); assert.ok(dialectDocument.version > versionBeforeRace);
  const currentEdits = await vscode.commands.executeCommand('vscode.executeFormatDocumentProvider', dialectUri, dialectOptions);
  const explicitFormat = new vscode.WorkspaceEdit(); explicitFormat.set(dialectUri, currentEdits);
  assert.equal(await vscode.workspace.applyEdit(explicitFormat), true);
  const expectedFormat = dialectPreview.after.replace('val  result', 'val result').replace(/[\t ]+(?=\r?$)/gm, '') + '# explicit test-user version change\r\n';
  assert.equal(dialectDocument.getText(), expectedFormat);
  assert.equal(await vscode.commands.executeCommand('vscode.executeFormatDocumentProvider', dialectUri, dialectOptions), undefined);
  assert.equal(fs.readFileSync(path.join(root, 'pyproject.toml'), 'utf8'), dialectPolicy);
  assert.equal(await dialectDocument.save(), true);
  const mappedArtifact = path.join(root, 'build', 'mapped');
  const mappedBuild = JSON.parse(observer.child('mapped-build', [python, '-I', '-m', 'pyalamode', 'build', dialectUri.fsPath, '--root', root, '--output', mappedArtifact, '--json'], root));
  assert.equal(mappedBuild.status, 0);
  const generatedText = fs.readFileSync(path.join(mappedArtifact, 'dialect.py'), 'utf8');
  const generatedLine = generatedText.split(/\r\n|\r|\n/).findIndex(row => row.startsWith('def café(')); assert.ok(generatedLine >= 0);
  const mappedProject = await vscode.commands.executeCommand('pyalamode.refresh');
  const mapped = await vscode.commands.executeCommand('pyalamode.sourceLocation', {artifactUri: vscode.Uri.file(mappedArtifact).toString(),
    path: 'dialect.py', position: {line: generatedLine, character: 4}, snapshot: mappedProject.snapshot});
  assert.equal(mapped.provenance.status, 0); assert.equal(mapped.provenance.verified, true);
  assert.equal(mapped.location.uri, vscode.Uri.file(fs.realpathSync(dialectUri.fsPath)).toString());
  assert.equal(vscode.window.activeTextEditor.document.uri.fsPath, dialectUri.fsPath);
  assert.equal(vscode.window.activeTextEditor.selection.start.line, 2); assert.equal(vscode.window.activeTextEditor.selection.start.character, 4);
  assert.equal(dialectDocument.getText(), expectedFormat); assert.equal(fs.readFileSync(dialectUri.fsPath, 'utf8'), expectedFormat);
  state.dialect = {source: dialectSource, language: dialectDocument.languageId, report: dialectReport, diagnostic: dialectRebinding,
    hovers: dialectHovers, definitions: dialectDefinitions, references: dialectReferences, repairSource: dialectRepairSource, repairReport: dialectRepairReport, repairDiagnostic: dialectRepairDiagnostic, preview: dialectPreview,
    format: dialectFormat, guardedFormat, serverRaceEdits, withheld, expectedFormat, mappedBuild, mapped, sourceAutomaticallyEdited: false};
  const previous = api.client.child.pid;
  await vscode.commands.executeCommand('pyalamode.restart'); assert.notEqual(api.client.child.pid, previous);
  api.client.on('wire', row => wire.push(row)); observer.transport(api.client, 'after explicit restart returned; startup prefix unobservable', true);
  const bootstrapMarkers = ['workspace-bootstrap-sentinel', 'path-bootstrap-sentinel', 'startup-bootstrap-sentinel'];
  fs.mkdirSync(path.join(root, 'pyalamode')); fs.mkdirSync(path.join(root, 'bootstrap-poison'));
  fs.writeFileSync(path.join(root, 'pyalamode', '__init__.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, bootstrapMarkers[0]))}).write_text('workspace package executed')\n`);
  fs.writeFileSync(path.join(root, 'bootstrap-poison', 'sitecustomize.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, bootstrapMarkers[1]))}).write_text('startup import executed')\n`);
  const startup = path.join(root, 'bootstrap-poison', 'startup.py');
  fs.writeFileSync(startup, `from pathlib import Path\nPath(${JSON.stringify(path.join(root, bootstrapMarkers[2]))}).write_text('startup script executed')\n`);
  const original = {PYTHONPATH: process.env.PYTHONPATH, PYTHONSTARTUP: process.env.PYTHONSTARTUP};
  process.env.PYTHONPATH = path.join(root, 'bootstrap-poison'); process.env.PYTHONSTARTUP = startup;
  try { await vscode.commands.executeCommand('pyalamode.restart'); api.client.on('wire', row => wire.push(row)); observer.transport(api.client, 'after explicit poisoned-environment restart returned; startup prefix unobservable', true); await api.ensure(); }
  finally { for (const [key, value] of Object.entries(original)) { if (value === undefined) delete process.env[key]; else process.env[key] = value; } }
  assert.deepEqual(api.client.args, ['-I', '-m', 'pyalamode.editor', '--stdio', '--root', fs.realpathSync(root)]);
  for (const marker of bootstrapMarkers) assert.equal(fs.existsSync(path.join(root, marker)), false);
  assert.equal(fs.existsSync(path.join(root, 'sentinel')), false);
  const packet = {vscode: vscode.version, node: process.version, execPath: process.execPath, versions: process.versions, localDesktop: {remoteName: vscode.env.remoteName ?? null, uiKind: vscode.env.uiKind}, provenance: api.client.provenance, wire, source_before: bad, hovers: state.hovers, preview, repairedStatus: repaired.report.status, effect, guarded, unicodeRange: rebinding.range, dialect: state.dialect, bootstrapSentinels: Object.fromEntries(bootstrapMarkers.map(marker => [marker, false])), sentinel: false, actual_api: true};
  if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify(packet, null, 2));
  await api.dispose();
  state.phase = 'passed';
}
exports.run = async () => {
  let failure, cleanupError;
  try { if (process.env.PYALAMODE_CLIENT_RESTRICTED === '1') await restricted(); else await run(); }
  catch (error) {
    failure = error;
    if (observer) observer.retain({passed: false, error: failureRecord(error), state, fixtureRetained: true});
    if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify({...state, error: String(error), stack: error.stack}, null, 2));
    if (running) { try { await running.dispose(); } catch (closeError) { cleanupError = closeError; } }
    throw error;
  }
  finally {
    if (observer) observer.finish({passed: !failure, error: failureRecord(failure), cleanupError: failureRecord(cleanupError),
      state, fixtureRetained: true, cleanupIntent: 'host workspace/profile/evidence always retained under root-supplied isolated output'});
  }
};
