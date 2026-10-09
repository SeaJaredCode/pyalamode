'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {EventEmitter} = require('node:events');
const {execFileSync} = require('node:child_process');
const {pathToFileURL} = require('node:url');
const {Client, Frames, frame, MAX_BODY} = require('../transport');

test('all split boundaries preserve UTF8 frame byte lengths and concatenated envelopes', () => {
  const value = {jsonrpc: '2.0', id: 7, result: 'café😀'};
  const raw = frame(value);
  for (let split = 0; split <= raw.length; split++) {
    const values = [], parser = new Frames(item => values.push(item));
    parser.push(raw.subarray(0, split)); parser.push(raw.subarray(split)); parser.finish();
    assert.deepEqual(values, [value]);
  }
  const values = [], parser = new Frames(item => values.push(item));
  parser.push(Buffer.concat([raw, frame({jsonrpc: '2.0', id: 8, error: {code: -32601, message: 'unsupported'}})]));
  assert.equal(values.length, 2); assert.equal(values[1].id, 8);
});

test('invalid headers/body/UTF8/JSON/envelope and truncated frames refuse', () => {
  for (const raw of [
    Buffer.from('Content-Length: -1\r\n\r\n'), Buffer.from(`Content-Length: ${MAX_BODY + 1}\r\n\r\n`),
    Buffer.from('Content-Length: 2\r\nContent-Length: 2\r\n\r\n{}'),
    Buffer.from('Content-Length: 2\r\nContent-Type: application/json; charset=latin1\r\n\r\n{}'),
    Buffer.from('Content-Length: 1\r\n\r\n{'), Buffer.from('Content-Length: 1\r\n\r\n\xff', 'latin1'),
    Buffer.from('Content-Length: 2\r\n\r\n[]'), Buffer.from('X'.repeat(8193))
  ]) assert.throws(() => new Frames(() => {}).push(raw));
  const parser = new Frames(() => {}); parser.push(Buffer.from('Content-Length: 2\r\n\r\n{'));
  assert.throws(() => parser.finish(), /truncated/);
});

test('malformed matching error rejects the pending promise instead of losing settlement', async () => {
  const client = Object.create(Client.prototype); EventEmitter.call(client);
  client.pending = new Map(); client.abandoned = new Set(); client.dead = false;
  let kills = 0, disposed = 0; client.child = {kill() { kills++; }};
  const pending = new Promise((resolve, reject) => client.pending.set(1, {resolve, reject, dispose() { disposed++; }}));
  try { client.receive({jsonrpc: '2.0', id: 1, error: {code: -1, message: null}}); } catch (error) { client.fail(error); }
  await assert.rejects(Promise.race([pending, new Promise((_, reject) => setTimeout(() => reject(new Error('settlement missing')), 50))]), /invalid server error/);
  assert.equal(client.pending.size, 0); assert.equal(kills, 1); assert.equal(disposed, 1);
});

test('RPC error and cancelled late response remain distinct from invalid unknown response', async () => {
  const client = Object.create(Client.prototype); EventEmitter.call(client);
  client.pending = new Map(); client.abandoned = new Set([4]); client.dead = false;
  const pending = new Promise((resolve, reject) => client.pending.set(1, {resolve, reject, dispose() {}}));
  client.receive({jsonrpc: '2.0', id: 1, error: {code: -32601, message: 'unsupported'}});
  await assert.rejects(pending, /-32601/);
  client.receive({jsonrpc: '2.0', id: 4, result: 'late'});
  assert.throws(() => client.receive({jsonrpc: '2.0', id: 999, result: null}), /unexpected/);
});

test('configured interpreter path is explicit and inaccessible executables fail', () => {
  assert.throws(() => new Client('python3', os.tmpdir()), /absolute/);
  assert.throws(() => new Client('/missing-pyalamode-interpreter', os.tmpdir()));
});

test('local cancellation, deadlines and pending bounds settle every admitted promise', async () => {
  const client = Object.create(Client.prototype); EventEmitter.call(client);
  Object.assign(client, {pending: new Map(), abandoned: new Set(), next: 1, timeout: 10, dead: false, send() {}});
  let cancel, disposed = 0;
  const cancelled = client.request('test/cancel', {}, {onCancellationRequested(callback) { cancel = callback; return {dispose() { disposed++; }}; }});
  cancel(); await assert.rejects(cancelled, /cancelled/);
  assert.equal(disposed, 1); assert.equal(client.pending.size, 0);
  client.receive({jsonrpc: '2.0', id: 1, result: 'late'});
  await assert.rejects(client.request('test/deadline', {}), /timed out/);
  assert.equal(client.pending.size, 0); assert.ok(client.abandoned.has(2));
  for (let id = 10; id < 138; id++) client.pending.set(id, {});
  await assert.rejects(client.request('test/bounded', {}), /Too many/);
  client.pending.clear();
  await assert.rejects(client.request('test/alreadycancelled', {}, {isCancellationRequested: true}), /cancelled/);
});

test('actual spawn errors and child exit reject pending transport requests', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-lifecycle-'));
  for (const executable of [root, process.execPath]) {
    const client = new Client(executable, root); const failures = [];
    client.on('failure', error => failures.push(error.message));
    await assert.rejects(client.request('initialize', {}));
    assert.equal(client.dead, true); assert.equal(client.pending.size, 0); assert.equal(failures.length, 1);
    await client.stop();
  }
  fs.rmSync(root, {recursive: true, force: true});
});

test('incompatible advertised runtime/protocol refuses before document synchronization', async () => {
  const handshake = {serverInfo: {name: 'pyalamode', version: 'editor-experience-9.0'}, capabilities: {positionEncoding: 'utf-16', textDocumentSync: {openClose: true, change: 1, save: {includeText: false}}, hoverProvider: true, definitionProvider: true, referencesProvider: true, documentSymbolProvider: true, codeActionProvider: true, experimental: {pyalamode: {schema: 1, target: 'cpython-3.13.1', pythonExecutable: '/configured/python', pythonVersion: [3, 13, 1], platform: 'darwin', root: '/fixture', filesystemEncoding: 'utf-8', filesystemErrors: 'surrogateescape'}}}};
  for (const change of [
    value => { value.capabilities.positionEncoding = 'utf-8'; },
    value => { value.capabilities.experimental.pyalamode.root = '/outside'; },
    value => { value.capabilities.experimental.pyalamode.pythonVersion = [3, 12, 0]; },
    value => { value.capabilities.experimental.pyalamode.pythonExecutable = '/other/python'; },
    value => { value.capabilities.codeActionProvider = false; }
  ]) {
    const value = structuredClone(handshake); change(value);
    const client = Object.create(Client.prototype); EventEmitter.call(client);
    let notified = 0, killed = 0;
    Object.assign(client, {root: '/fixture', python: '/configured/python', pending: new Map(), dead: false, child: {kill() { killed++; }}, request: async () => value, notify() { notified++; }});
    await assert.rejects(client.initialize(), /Incompatible/);
    assert.equal(client.dead, true); assert.equal(client.initialized, undefined); assert.equal(notified, 0); assert.equal(killed, 1);
  }
});

test('actual exported Node transport uses real Python server and source overlays', {skip: !process.env.PYALAMODE_CLIENT_PYTHON}, async () => {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-')));
  const clean = '# mode: fun\n\ndef add(value: int) -> int:\n    return value + 1\n';
  const bad = '# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n';
  fs.writeFileSync(path.join(root, 'core.py'), clean);
  fs.writeFileSync(path.join(root, 'bad.py'), bad);
  fs.writeFileSync(path.join(root, 'effect.py'), 'from pyalamode import effects, Clock, ClockCapability\n@effects(Clock)\ndef stamp(clock:ClockCapability)->int:return clock.now_ns()\n');
  fs.writeFileSync(path.join(root, 'sentinel_source.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, 'sentinel'))}).write_text('evaluated')\ndef ordinary(value: Path(${JSON.stringify(path.join(root, 'annotation-sentinel'))}).write_text('annotation') = Path(${JSON.stringify(path.join(root, 'default-sentinel'))}).write_text('default')):\n    return value\n`);
  const python = process.env.PYALAMODE_CLIENT_PYTHON, client = new Client(python, root);
  const wire = [], notifications = [], failures = [];
  client.on('wire', message => wire.push(message)); client.on('notification', message => notifications.push(message)); client.on('failure', error => failures.push(error.message));
  const uri = pathToFileURL(path.join(root, 'bad.py')).href;
  try {
    await client.initialize();
    assert.equal(client.provenance.python, python); assert.deepEqual(client.args, ['-I', '-m', 'pyalamode.editor', '--stdio', '--root', root]);
    client.notify('textDocument/didOpen', {textDocument: {uri, languageId: 'python', version: 1, text: bad}});
    const report = await client.request('pyalamode/project', {});
    assert.equal(report.schema, 1); assert.equal(report.report.status, 1);
    const diagnostic = report.diagnostics.find(item => item.uri === uri && item.code === 'PAL101');
    assert.ok(diagnostic); assert.equal(diagnostic.data.version, 1); assert.ok(diagnostic.data.authored.column_encoding);
    const hovered = await client.request('textDocument/hover', {textDocument: {uri}, position: {line: 2, character: 5}});
    assert.ok(JSON.stringify(hovered).includes('unverified'));
    const explanation = await client.request('pyalamode/explain', {symbol: 'PAL101'}); assert.ok(explanation.text.includes('binding'));
    const previewParams = {uri, version: 1, snapshot: report.snapshot, diagnosticIndex: diagnostic.data.diagnosticIndex};
    const preview = await client.request('pyalamode/preview', previewParams);
    assert.equal(preview.before, bad); assert.notEqual(preview.after, bad); assert.equal(fs.readFileSync(path.join(root, 'bad.py'), 'utf8'), bad);
    client.notify('textDocument/didChange', {textDocument: {uri, version: 2}, contentChanges: [{text: preview.after}]});
    const repaired = await client.request('pyalamode/project', {}); assert.equal(repaired.report.status, 0); assert.ok(repaired.freshness.includes('unsaved'));
    const effect = repaired.regions.find(item => item.name === 'stamp').contract;
    assert.deepEqual(effect.required_effects, ['Clock']); assert.ok(effect.effect_origins.Clock);
    await assert.rejects(client.request('pyalamode/preview', previewParams));
    await assert.rejects(client.request('unknown/method', {}));
    assert.equal((await client.request('pyalamode/project', {})).report.status, 0);
    client.notify('textDocument/didClose', {textDocument: {uri}});
    assert.equal((await client.request('pyalamode/project', {})).report.status, 1);
    fs.writeFileSync(path.join(root, 'bad.py'), preview.after);
    fs.writeFileSync(path.join(root, 'external.py'), 'from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef digest(data:bytes)->bytes:return sha256_digest(data)\n');
    const denied = await client.request('pyalamode/project', {});
    assert.equal(denied.report.status, 1); assert.ok(denied.diagnostics.some(item => item.code === 'PAL350'));
    const identity = JSON.parse(execFileSync(python, ['-I', '-c', 'import json,sys;from pyalamode.integration_contracts import integration_snapshot;print(json.dumps(next(row for row in integration_snapshot(root=sys.argv[1])["catalog"] if row["identity"].endswith("sha256_digest"))))', root], {cwd: root, encoding: 'utf8'}));
    const approval = {operation: identity.identity, contract_sha256: identity.contract_sha256, dependency_sha256: identity.dependency_sha256, owner: 'M9 local client fixture reviewer', rationale: 'explicitly reviewed bounded digest fixture', provenance: 'root-authorized M9 actual client verification fixture', expires_at: new Date(Date.now() + 1800000).toISOString().replace(/\.\d{3}Z$/, 'Z')};
    fs.writeFileSync(path.join(root, 'pyproject.toml'), '[tool.pyalamode]\nexternal_trust="approved"\n[[tool.pyalamode.integration_approvals]]\n' + Object.entries(approval).map(([key, value]) => key + '=' + JSON.stringify(value) + '\n').join(''));
    const approved = await client.request('pyalamode/project', {});
    assert.equal(approved.report.status, 0);
    const trusted = approved.regions.find(item => item.name === 'digest').contract;
    assert.equal(trusted.external_assumptions[0].admission, 'approved'); assert.equal(trusted.external_assumptions[0].approval.owner, approval.owner);
    assert.ok(trusted.trust.some(item => item.includes(identity.identity)));
    assert.ok(approved.report.files.find(item => item.path.endsWith('external.py')).setup_observations.length);
    for (const sentinel of ['sentinel', 'annotation-sentinel', 'default-sentinel']) assert.equal(fs.existsSync(path.join(root, sentinel)), false);
    assert.ok(notifications.length); assert.deepEqual(failures, []);
    if (process.env.PYALAMODE_CLIENT_REPORT) fs.writeFileSync(process.env.PYALAMODE_CLIENT_REPORT, JSON.stringify({node: process.version, execPath: process.execPath, platform: process.platform, provenance: client.provenance, wire, notifications, denied, approved, identity, approval, sentinel: false}, null, 2));
  } finally { await client.stop(); fs.rmSync(root, {recursive: true, force: true}); }
  assert.equal(client.dead, true); assert.equal(client.pending.size, 0);
});

test('actual isolated child bootstrap never imports workspace or PYTHONPATH/startup poison', {skip: !process.env.PYALAMODE_CLIENT_PYTHON}, async () => {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-bootstrap-')));
  const poison = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-startup-')));
  const markers = ['workspace-sentinel', 'path-sentinel', 'startup-sentinel'];
  fs.mkdirSync(path.join(root, 'pyalamode'));
  fs.writeFileSync(path.join(root, 'pyalamode', '__init__.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, markers[0]))}).write_text('workspace package executed')\n`);
  fs.writeFileSync(path.join(poison, 'sitecustomize.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, markers[1]))}).write_text('startup import executed')\n`);
  const startup = path.join(poison, 'startup.py');
  fs.writeFileSync(startup, `from pathlib import Path\nPath(${JSON.stringify(path.join(root, markers[2]))}).write_text('startup script executed')\n`);
  fs.writeFileSync(path.join(root, 'core.py'), '# mode: fun\ndef f()->int:return 1\n');
  const original = {PYTHONPATH: process.env.PYTHONPATH, PYTHONSTARTUP: process.env.PYTHONSTARTUP};
  process.env.PYTHONPATH = poison; process.env.PYTHONSTARTUP = startup;
  let client;
  try { client = new Client(process.env.PYALAMODE_CLIENT_PYTHON, root); }
  finally { for (const [key, value] of Object.entries(original)) { if (value === undefined) delete process.env[key]; else process.env[key] = value; } }
  const wire = []; client.on('wire', row => wire.push(row));
  try {
    await client.initialize();
    assert.deepEqual(client.args, ['-I', '-m', 'pyalamode.editor', '--stdio', '--root', root]);
    assert.equal(client.provenance.python, process.env.PYALAMODE_CLIENT_PYTHON);
    const project = await client.request('pyalamode/project', {});
    assert.equal(project.schema, 1); assert.ok(Object.keys(project.inputs.product_artifacts).some(name => name.endsWith('editor.py')));
    for (const marker of markers) assert.equal(fs.existsSync(path.join(root, marker)), false);
    if (process.env.PYALAMODE_CLIENT_REPORT) {
      const reportPath = process.env.PYALAMODE_CLIENT_REPORT;
      const previous = fs.existsSync(reportPath) ? JSON.parse(fs.readFileSync(reportPath, 'utf8')) : {};
      fs.writeFileSync(reportPath, JSON.stringify({...previous, bootstrap: {provenance: client.provenance, inheritedPoison: {PYTHONPATH: poison, PYTHONSTARTUP: startup}, wire, project, sentinels: Object.fromEntries(markers.map(marker => [marker, false]))}}, null, 2));
    }
  } finally { await client.stop(); fs.rmSync(root, {recursive: true, force: true}); fs.rmSync(poison, {recursive: true, force: true}); }
});
