'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {EventEmitter} = require('node:events');
const {spawnSync} = require('node:child_process');
const {createHash} = require('node:crypto');
const {pathToFileURL} = require('node:url');
const {Client, Frames, frame, MAX_BODY, validateTextEdits, validateSourceLocation} = require('../transport');
const failureRecord = error => error ? {name: error.name, message: error.message, code: error.code ?? null, stack: error.stack ?? null} : null;
function observation(name, fixtures) {
  if (!['server-overlays', 'isolated-bootstrap', 'dialect'].includes(name)) throw new Error('Unknown fixed observation case');
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
    retain(value) {
      const transports = streamSnapshot(false), captureFailure = transports.some(item => item.capture_error);
      write('partial.json', {schema: 1, case: name, ...value, passed: value.passed && !captureFailure, transports});
      return captureFailure;
    },
    finish(value) {
      const transports = streamSnapshot(true), captureFailure = transports.some(item => item.capture_error);
      write('finish.json', {schema: 1, case: name, ...value, passed: value.passed && !captureFailure, transports});
      if (captureFailure && !value.error) throw new Error('Transport raw capture failed; retained observation is unverified');
    }
  };
}

function handshake() {
  return {serverInfo: {name: 'pyalamode', version: 'experimental-syntax-14.0'}, capabilities: {
    positionEncoding: 'utf-16', textDocumentSync: {openClose: true, change: 1, save: {includeText: false}},
    hoverProvider: true, definitionProvider: true, referencesProvider: true, documentSymbolProvider: true,
    codeActionProvider: true, documentFormattingProvider: true, experimental: {pyalamode: {
      schema: 2, target: 'cpython-3.13.1', pythonExecutable: '/configured/python', pythonVersion: '3.13.1',
      platform: 'darwin', root: '/fixture', filesystemEncoding: 'utf-8', filesystemErrors: 'surrogateescape',
      languages: ['python', 'pyalamode'], syntaxVersion: 'pyalamode.syntax-v1', sourceMapSchema: 1, formatProfile: 'val-whitespace-v1'
    }}
  }};
}

function sourceLocation(snapshot, uri) {
  return {schema: 1, snapshot, freshness: 'current', location: {uri, range: {
    start: {line: 3, character: 4}, end: {line: 3, character: 14}
  }}, provenance: {schema: 1, kind: 'pyalamode-source-location', status: 0, verified: true,
    artifact: '/fixture/build/mapped', generated: {path: 'dialect.py', line: 4, column: 5, column_encoding: 'utf-8-bytes', sha256: 'c'.repeat(64)},
    authored: {path: 'dialect.pya', source_copy: '.pyalamode/sources/dialect.pya', line: 4, column: 5,
      end_line: 4, end_column: 15, column_encoding: 'utf-8-bytes', sha256: 'd'.repeat(64)}, exact: true,
    segments: [2], snapshot: 'e'.repeat(64), inputs: {artifacts: {}, evidence_sha256: 'f'.repeat(64), product_artifacts: {}}, diagnostics: []}};
}

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
  for (const change of [
    value => { value.capabilities.positionEncoding = 'utf-8'; },
    value => { value.capabilities.experimental.pyalamode.root = '/outside'; },
    value => { value.capabilities.experimental.pyalamode.pythonVersion = [3, 12, 0]; },
    value => { value.capabilities.experimental.pyalamode.pythonExecutable = '/other/python'; },
    value => { value.capabilities.codeActionProvider = false; },
    value => { value.capabilities.documentFormattingProvider = false; },
    value => { value.capabilities.experimental.pyalamode.schema = 1; },
    value => { value.capabilities.experimental.pyalamode.pythonVersion = [3, 13, 1]; },
    value => { value.capabilities.experimental.pyalamode.languages.reverse(); },
    value => { value.capabilities.experimental.pyalamode.syntaxVersion = 'future'; },
    value => { value.capabilities.experimental.pyalamode.sourceMapSchema = 2; },
    value => { value.capabilities.experimental.pyalamode.formatProfile = 'future'; },
    value => { value.capabilities.experimental.pyalamode.unknown = true; },
    value => { delete value.capabilities.experimental.pyalamode.languages; }
  ]) {
    const value = handshake(); change(value);
    const client = Object.create(Client.prototype); EventEmitter.call(client);
    let notified = 0, killed = 0;
    Object.assign(client, {root: '/fixture', python: '/configured/python', pending: new Map(), dead: false, child: {kill() { killed++; }}, request: async () => value, notify() { notified++; }});
    client.pythonOwner = '/configured/python';
    await assert.rejects(client.initialize(), /Incompatible/);
    assert.equal(client.dead, true); assert.equal(client.initialized, undefined); assert.equal(notified, 0); assert.equal(killed, 1);
  }
  for (const advertised of ['/configured/python', '/physical/other/python', '/physical/configured/python3', '/native/base/python']) {
    const value = handshake(); value.capabilities.experimental.pyalamode.pythonExecutable = advertised;
    const client = Object.create(Client.prototype); EventEmitter.call(client);
    let notified = 0, killed = 0;
    Object.assign(client, {root: '/fixture', python: '/configured/python', pythonOwner: '/physical/configured/python',
      pending: new Map(), dead: false, child: {kill() { killed++; }}, request: async () => value, notify() { notified++; }});
    await assert.rejects(client.initialize(), /Incompatible/);
    assert.equal(client.dead, true); assert.equal(client.initialized, undefined); assert.equal(notified, 0); assert.equal(killed, 1);
  }
});

test('exact metadata2 accepts both languages and retains literal native interpreter provenance', async () => {
  const client = Object.create(Client.prototype); EventEmitter.call(client);
  const messages = [], value = handshake();
  Object.assign(client, {root: '/fixture', python: '/configured/python', args: ['-I', '-m', 'pyalamode.editor'],
    request: async () => value, notify(method, params) { messages.push({method, params}); }});
  client.pythonOwner = '/configured/python';
  assert.equal(await client.initialize(), value);
  assert.equal(client.initialized, true); assert.deepEqual(messages, [{method: 'initialized', params: {}}]);
  assert.equal(Object.keys(value.capabilities.experimental.pyalamode).length, 12);
  assert.equal(client.provenance.python, '/configured/python');
  const physical = Object.create(Client.prototype); EventEmitter.call(physical);
  const advertised = handshake(), initialized = [];
  advertised.capabilities.experimental.pyalamode.pythonExecutable = '/physical/configured/python';
  Object.assign(physical, {root: '/fixture', python: '/configured/python', pythonOwner: '/physical/configured/python',
    args: ['-I', '-m', 'pyalamode.editor'], request: async () => advertised,
    notify(method, params) { initialized.push({method, params}); }});
  assert.equal(await physical.initialize(), advertised);
  assert.deepEqual(initialized, [{method: 'initialized', params: {}}]);
  assert.equal(physical.provenance.python, '/configured/python');
  assert.equal(physical.provenance.server.capabilities.experimental.pyalamode.pythonExecutable, '/physical/configured/python');
});

test('dialect language activation grammar and exact six packaged source files are declared', () => {
  const root = path.resolve(__dirname, '..'), metadata = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
  assert.deepEqual(metadata.activationEvents, ['onLanguage:python', 'onLanguage:pyalamode']);
  assert.deepEqual(metadata.contributes.languages, [{id: 'pyalamode', aliases: ['Pyalamode'], extensions: ['.pya'], configuration: './language-configuration.json'}]);
  assert.deepEqual(metadata.contributes.grammars, [{language: 'pyalamode', scopeName: 'source.pyalamode', path: './syntaxes/pyalamode.tmLanguage.json'}]);
  assert.equal(metadata.capabilities.untrustedWorkspaces.supported, false);
  assert.ok(metadata.contributes.commands.some(row => row.command === 'pyalamode.sourceLocation'));
  const grammar = JSON.parse(fs.readFileSync(path.join(root, 'syntaxes/pyalamode.tmLanguage.json'), 'utf8'));
  assert.equal(grammar.scopeName, 'source.pyalamode');
  assert.ok(grammar.patterns.some(row => row.name === 'storage.type.val.pyalamode' && row.match === '\\bval\\b'));
  assert.ok(grammar.patterns.some(row => row.name === 'entity.name.type.pyalamode'));
  assert.deepEqual(JSON.parse(fs.readFileSync(path.join(root, 'language-configuration.json'), 'utf8')).comments, {lineComment: '#'});
  const packager = fs.readFileSync(path.join(root, 'package_vsix.py'), 'utf8');
  assert.match(packager, /PAYLOAD = \("package.json", "extension.js", "transport.js", "README.md",\n\s+"language-configuration.json", "syntaxes\/pyalamode.tmLanguage.json"\)/);
});

test('format edit validation preserves UTF16 astral boundaries and refuses overlaps and malformed rows', () => {
  const text = 'val café = "😀"  \r\n', edits = [{range: {start: {line: 0, character: 15}, end: {line: 0, character: 17}}, newText: ''}];
  assert.equal(validateTextEdits(edits, text), edits);
  assert.deepEqual(validateTextEdits([], text), []);
  for (const value of [
    [{range: {start: {line: 0, character: 13}, end: {line: 0, character: 14}}, newText: ''}],
    [{range: {start: {line: 1, character: 1}, end: {line: 1, character: 1}}, newText: ''}],
    [{...edits[0], extra: true}], [{...edits[0], newText: null}], [edits[0], edits[0]],
    [{range: {start: {line: -1, character: 0}, end: {line: 0, character: 0}}, newText: ''}]
  ]) assert.throws(() => validateTextEdits(value, text), /formatting edits/);
});

test('mapped source navigation accepts verified relation and keeps stale artifact refusal explicit', () => {
  const snapshot = 'a'.repeat(64), value = sourceLocation(snapshot, 'file:///fixture/dialect.pya');
  assert.equal(validateSourceLocation(value, snapshot), value);
  const stale = structuredClone(value);
  Object.assign(stale.provenance, {status: 1, verified: false, authored: null, exact: null, segments: []}); stale.location = null;
  assert.equal(validateSourceLocation(stale, snapshot), stale);
  for (const change of [
    row => { row.snapshot = 'b'.repeat(64); }, row => { row.extra = true; },
    row => { row.provenance.verified = false; }, row => { row.location.range.start.character = -1; },
    row => { row.provenance.segments = [true]; }, row => { row.provenance.status = 3; }
  ]) { const row = structuredClone(value); change(row); assert.throws(() => validateSourceLocation(row, snapshot)); }
  const invented = structuredClone(stale); invented.location = value.location;
  assert.throws(() => validateSourceLocation(invented, snapshot), /Unverified/);
});

test('actual client adapters guard dialect versions, select both file languages and never apply source edits', async () => {
  const Module = require('node:module'), originalLoad = Module._load;
  const extensionPath = require.resolve('../extension'), previous = require.cache[extensionPath];
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-adapter-')));
  const text = '# mode: fun\n\ndef café() -> str:\n    val title = "😀"  \n    return title\n';
  fs.writeFileSync(path.join(root, 'dialect.pya'), text); fs.writeFileSync(path.join(root, 'core.py'), '# mode: fun\ndef f()->int:return 1\n');
  fs.mkdirSync(path.join(root, 'build', 'mapped'), {recursive: true}); fs.writeFileSync(path.join(root, 'build', 'mapped', 'dialect.py'), '# generated fixture bytes\n');
  class Uri {
    constructor(value) { const parsed = new URL(value); this.value = value; this.scheme = parsed.protocol.slice(0, -1); this.authority = parsed.host; this.path = decodeURIComponent(parsed.pathname); this.fsPath = this.path; }
    toString() { return this.value; }
    static file(name) { return new Uri(pathToFileURL(name).href); }
    static parse(value) { return new Uri(value); }
    static from(value) { return new Uri(value.scheme + '://' + value.path); }
  }
  const document = {uri: Uri.file(path.join(root, 'dialect.pya')), languageId: 'pyalamode', version: 1, isUntitled: false, isClosed: false, getText() { return text; }};
  const compatible = {...document, uri: Uri.file(path.join(root, 'core.py')), languageId: 'python'};
  const mismatch = {...document, languageId: 'python'};
  const providers = {}, selectors = {}, commands = new Map(), messages = [], shown = [], errors = [], snapshot = 'a'.repeat(64);
  const disposable = () => ({dispose() {}});
  let contentProvider, formatHook;
  class FakeClient extends EventEmitter {
    constructor(python, ownedRoot) { super(); this.python = python; this.root = ownedRoot; this.dead = false; this.provenance = {python}; }
    async initialize() { this.initialized = true; return {}; }
    notify(method, params) { messages.push({method, params}); }
    async request(method, params) {
      messages.push({method, params});
      if (method === 'pyalamode/project') return {snapshot};
      if (method === 'textDocument/formatting') {
        if (formatHook) await formatHook();
        return [{range: {start: {line: 3, character: 20}, end: {line: 3, character: 22}}, newText: ''}];
      }
      if (method === 'pyalamode/sourceLocation') return sourceLocation(snapshot, document.uri.toString());
      throw new Error('Unexpected mock request ' + method);
    }
    async stop() { this.dead = true; }
    fail(error) { this.dead = true; this.emit('failure', error); }
  }
  const vscode = {
    Uri, UIKind: {Desktop: 1}, env: {uiKind: 1, remoteName: undefined},
    Range: class { constructor(a, b, c, d) { this.start = {line: a, character: b}; this.end = {line: c, character: d}; } },
    TextEdit: class { constructor(range, newText) { this.range = range; this.newText = newText; } },
    workspace: {isTrusted: true, workspaceFolders: [{uri: Uri.file(root)}], textDocuments: [document, compatible, mismatch],
      getConfiguration() { return {get() { return '/configured/python'; }}; },
      registerTextDocumentContentProvider(_scheme, provider) { contentProvider = provider; return disposable(); },
      async openTextDocument(uri) { return uri.scheme === 'file' ? document : {uri, getText() { return contentProvider.provideTextDocumentContent(uri); }}; },
      applyEdit() { assert.fail('Client automatically applied an edit'); }},
    window: {createOutputChannel() { return {append() {}, appendLine() {}, dispose() {}}; },
      showErrorMessage(message) { errors.push(message); }, async showTextDocument(doc, options) { shown.push({doc, options}); }},
    languages: {createDiagnosticCollection() { return {clear() {}, delete() {}, dispose() {}, set() {}}; }},
    commands: {registerCommand(name, fn) { commands.set(name, fn); return disposable(); }}
  };
  for (const name of ['Hover', 'Definition', 'Reference', 'DocumentSymbol', 'CodeActions', 'DocumentFormattingEdit'])
    vscode.languages['register' + name + 'Provider'] = (selector, provider) => { providers[name] = provider; selectors[name] = selector; return disposable(); };
  for (const name of ['OpenTextDocument', 'ChangeTextDocument', 'SaveTextDocument', 'CloseTextDocument', 'ChangeConfiguration', 'ChangeWorkspaceFolders'])
    vscode.workspace['onDid' + name] = () => disposable();
  let api;
  try {
    delete require.cache[extensionPath];
    Module._load = function(request, parent, isMain) {
      if (parent?.filename === extensionPath && request === 'vscode') return vscode;
      if (parent?.filename === extensionPath && request === './transport') return {...require('../transport'), Client: FakeClient};
      return originalLoad.call(this, request, parent, isMain);
    };
    const extension = require('../extension'); Module._load = originalLoad;
    api = extension.activate({subscriptions: []}); await api.ensure();
    assert.deepEqual(selectors.Hover, [{language: 'python', scheme: 'file'}, {language: 'pyalamode', scheme: 'file'}]);
    assert.deepEqual(selectors.DocumentFormattingEdit, {language: 'pyalamode', scheme: 'file'});
    const opens = messages.filter(row => row.method === 'textDocument/didOpen');
    assert.deepEqual(opens.map(row => row.params.textDocument.languageId), ['pyalamode', 'python']);
    const provider = providers.DocumentFormattingEdit, options = {tabSize: 4, insertSpaces: true};
    const edits = await provider.provideDocumentFormattingEdits(document, options);
    assert.equal(edits.length, 1); assert.equal(edits[0].newText, '');
    assert.deepEqual(messages.find(row => row.method === 'textDocument/formatting').params,
      {textDocument: {uri: document.uri.toString()}, options, pyalamode: {version: 1, snapshot}});
    assert.equal(document.getText(), text); assert.equal(fs.readFileSync(document.uri.fsPath, 'utf8'), text);
    formatHook = async () => { document.version++; };
    assert.deepEqual(await provider.provideDocumentFormattingEdits(document, options), []);
    document.version = 1; formatHook = async () => { throw new Error('-32801: stale formatting input'); };
    assert.equal(await provider.provideDocumentFormattingEdits(document, options), undefined);
    assert.ok(errors.some(message => message.includes('-32801')));
    const located = await commands.get('pyalamode.sourceLocation')({artifactUri: Uri.file(path.join(root, 'build', 'mapped')).toString(),
      path: 'dialect.py', position: {line: 3, character: 4}, snapshot});
    assert.equal(located.provenance.verified, true); assert.equal(shown.at(-1).doc, document);
    assert.equal(shown.at(-1).options.selection.start.character, 4);
    assert.equal(fs.readFileSync(document.uri.fsPath, 'utf8'), text);
    assert.equal(await commands.get('pyalamode.sourceLocation')({artifactUri: Uri.file(path.join(root, 'build', 'mapped')).toString(),
      path: '../dialect.py', position: {line: 0, character: 0}, snapshot}), undefined);
    assert.ok(errors.some(message => message.includes('exact current mapped source')));
  } finally {
    Module._load = originalLoad; if (api) await api.dispose(); delete require.cache[extensionPath];
    if (previous) require.cache[extensionPath] = previous;
    fs.rmSync(root, {recursive: true, force: true});
  }
});

test('actual exported Node transport uses real Python server and source overlays', {skip: !process.env.PYALAMODE_CLIENT_PYTHON}, async () => {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-')));
  const journal = observation('server-overlays', [root]);
  const clean = '# mode: fun\n\ndef add(value: int) -> int:\n    return value + 1\n';
  const bad = '# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n';
  const python = process.env.PYALAMODE_CLIENT_PYTHON, wire = [], notifications = [], failures = [];
  let client, failure;
  try {
  fs.writeFileSync(path.join(root, 'core.py'), clean);
  fs.writeFileSync(path.join(root, 'bad.py'), bad);
  fs.writeFileSync(path.join(root, 'effect.py'), 'from pyalamode import effects, Clock, ClockCapability\n@effects(Clock)\ndef stamp(clock:ClockCapability)->int:return clock.now_ns()\n');
  fs.writeFileSync(path.join(root, 'sentinel_source.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, 'sentinel'))}).write_text('evaluated')\ndef ordinary(value: Path(${JSON.stringify(path.join(root, 'annotation-sentinel'))}).write_text('annotation') = Path(${JSON.stringify(path.join(root, 'default-sentinel'))}).write_text('default')):\n    return value\n`);
  client = new Client(python, root);
  journal.transport(client, 'synchronous constructor return before initialize request', false);
  client.on('wire', message => wire.push(message)); client.on('notification', message => notifications.push(message)); client.on('failure', error => failures.push(error.message));
  const uri = pathToFileURL(path.join(root, 'bad.py')).href;
    await client.initialize();
    assert.equal(client.provenance.python, python); assert.deepEqual(client.args, ['-I', '-m', 'pyalamode.editor', '--stdio', '--root', root]);
    assert.equal(client.provenance.server.capabilities.experimental.pyalamode.pythonExecutable, client.pythonOwner);
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
    const identity = JSON.parse(journal.child('integration-snapshot', [python, '-I', '-c', 'import json,sys;from pyalamode.integration_contracts import integration_snapshot;print(json.dumps(next(row for row in integration_snapshot(root=sys.argv[1])["catalog"] if row["identity"].endswith("sha256_digest"))))', root], root));
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
  } catch (error) { failure = error; throw error; }
  finally {
    let cleanupError;
    try { await client?.stop(); if (!failure) { assert.equal(client.dead, true); assert.equal(client.pending.size, 0); } }
    catch (error) { cleanupError = error; }
    const partial = {passed: !failure && !cleanupError, error: failureRecord(failure || cleanupError), cleanupError: failureRecord(cleanupError),
      wire, notifications, failures, provenance: client?.provenance ?? null, fixtureRetained: Boolean(failure || cleanupError),
      cleanupIntent: 'remove only this freshly created fixture on full success; retain failed fixture'};
    if (journal.retain(partial) && !cleanupError) cleanupError = new Error('Transport raw capture failed; fixture retained');
    if (!failure && !cleanupError) { try { fs.rmSync(root, {recursive: true, force: true}); } catch (error) { cleanupError = error; } }
    journal.finish({...partial, passed: !failure && !cleanupError, error: failureRecord(failure || cleanupError),
      cleanupError: failureRecord(cleanupError), fixtureRetained: fs.existsSync(root)});
    if (!failure && cleanupError) throw cleanupError;
  }
});

test('actual isolated child bootstrap never imports workspace or PYTHONPATH/startup poison', {skip: !process.env.PYALAMODE_CLIENT_PYTHON}, async () => {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-bootstrap-')));
  const poison = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-startup-')));
  const journal = observation('isolated-bootstrap', [root, poison]), wire = [];
  let client, failure;
  const markers = ['workspace-sentinel', 'path-sentinel', 'startup-sentinel'];
  try {
  fs.mkdirSync(path.join(root, 'pyalamode'));
  fs.writeFileSync(path.join(root, 'pyalamode', '__init__.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, markers[0]))}).write_text('workspace package executed')\n`);
  fs.writeFileSync(path.join(poison, 'sitecustomize.py'), `from pathlib import Path\nPath(${JSON.stringify(path.join(root, markers[1]))}).write_text('startup import executed')\n`);
  const startup = path.join(poison, 'startup.py');
  fs.writeFileSync(startup, `from pathlib import Path\nPath(${JSON.stringify(path.join(root, markers[2]))}).write_text('startup script executed')\n`);
  fs.writeFileSync(path.join(root, 'core.py'), '# mode: fun\ndef f()->int:return 1\n');
  const original = {PYTHONPATH: process.env.PYTHONPATH, PYTHONSTARTUP: process.env.PYTHONSTARTUP};
  process.env.PYTHONPATH = poison; process.env.PYTHONSTARTUP = startup;
  try { client = new Client(process.env.PYALAMODE_CLIENT_PYTHON, root); }
  finally { for (const [key, value] of Object.entries(original)) { if (value === undefined) delete process.env[key]; else process.env[key] = value; } }
  journal.transport(client, 'synchronous constructor/environment restore before initialize request', false);
  client.on('wire', row => wire.push(row));
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
  } catch (error) { failure = error; throw error; }
  finally {
    let cleanupError;
    try { await client?.stop(); } catch (error) { cleanupError = error; }
    const partial = {passed: !failure && !cleanupError, error: failureRecord(failure || cleanupError), cleanupError: failureRecord(cleanupError),
      wire, provenance: client?.provenance ?? null, inheritedPoison: {PYTHONPATH: poison, PYTHONSTARTUP: path.join(poison, 'startup.py')},
      fixtureRetained: Boolean(failure || cleanupError), cleanupIntent: 'remove only these fresh fixture roots on full success; retain failed fixtures'};
    if (journal.retain(partial) && !cleanupError) cleanupError = new Error('Transport raw capture failed; fixtures retained');
    if (!failure && !cleanupError) {
      try { fs.rmSync(root, {recursive: true, force: true}); fs.rmSync(poison, {recursive: true, force: true}); } catch (error) { cleanupError = error; }
    }
    journal.finish({...partial, passed: !failure && !cleanupError, error: failureRecord(failure || cleanupError),
      cleanupError: failureRecord(cleanupError), fixtureRetained: fs.existsSync(root) || fs.existsSync(poison)});
    if (!failure && cleanupError) throw cleanupError;
  }
});

test('real server dialect UTF16 navigation preview formatting and artifact source relation stay version-bound', {skip: !process.env.PYALAMODE_CLIENT_PYTHON}, async () => {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'pyalamode-client-dialect-'))), python = process.env.PYALAMODE_CLIENT_PYTHON;
  const journal = observation('dialect', [root]), wire = [], failures = [];
  let client, failure;
  const bad = '# mode: fun\r\n\r\ndef café() -> str:\r\n    val  result = "😀"  \r\n    "😀abcdefghi"; result = result + "café"\r\n    return result\r\n';
  const caller = '# mode: fun\nfrom dialect import café\ndef call() -> str:\n    return café()\n';
  try {
  fs.writeFileSync(path.join(root, 'dialect.pya'), bad);
  fs.writeFileSync(path.join(root, 'pyproject.toml'), '[tool.pyalamode]\nschema=1\nedition="pyalamode-v1-experimental"\n');
  const uri = pathToFileURL(path.join(root, 'dialect.pya')).href, callUri = pathToFileURL(path.join(root, 'caller.pya')).href;
  client = new Client(python, root);
  journal.transport(client, 'synchronous constructor return before initialize request', false);
  client.on('wire', row => wire.push(row)); client.on('failure', error => failures.push(error.message));
    const initialized = await client.initialize();
    assert.equal(initialized.capabilities.experimental.pyalamode.pythonVersion, '3.13.1');
    assert.deepEqual(initialized.capabilities.experimental.pyalamode.languages, ['python', 'pyalamode']);
    client.notify('textDocument/didOpen', {textDocument: {uri, languageId: 'pyalamode', version: 1, text: bad}});
    const before = await client.request('pyalamode/project', {}), diagnostic = before.diagnostics.find(item => item.uri === uri && item.code === 'PAL101');
    assert.ok(diagnostic); assert.equal(diagnostic.range.start.line, 4); assert.equal(diagnostic.range.start.character, 19);
    assert.equal(diagnostic.data.version, 1);
    const hovered = await client.request('textDocument/hover', {textDocument: {uri}, position: {line: 2, character: 5}});
    assert.ok(JSON.stringify(hovered).includes('unverified'));
    // This is an explicit test-user source edit after the original UTF16 finding.
    const repairSource = '# mode: fun\r\n\r\ndef café() -> str:\r\n    val  result = "😀"  \r\n    result = result + "café"\r\n    return result\r\n';
    client.notify('textDocument/didChange', {textDocument: {uri, version: 2}, contentChanges: [{text: repairSource}]});
    const repairReport = await client.request('pyalamode/project', {}), repairDiagnostic = repairReport.diagnostics.find(item => item.uri === uri && item.code === 'PAL101');
    assert.ok(repairDiagnostic); assert.equal(repairDiagnostic.data.version, 2);
    assert.deepEqual(repairDiagnostic.range.start, {line: 4, character: 4}); assert.equal(repairReport.report.status, 1);
    const params = {uri, version: 2, snapshot: repairReport.snapshot, diagnosticIndex: repairDiagnostic.data.diagnosticIndex};
    const preview = await client.request('pyalamode/preview', params);
    assert.equal(preview.before, repairSource); assert.notEqual(preview.after, repairSource); assert.equal(fs.readFileSync(path.join(root, 'dialect.pya'), 'utf8'), bad);
    assert.ok(preview.after.includes('    val result_2 = result + "café"\r\n')); assert.ok(preview.after.includes('    return result_2\r\n'));
    assert.equal(preview.status, 0); assert.deepEqual(preview.remainingDiagnostics, []);
    client.notify('textDocument/didChange', {textDocument: {uri, version: 3}, contentChanges: [{text: preview.after}]});
    fs.writeFileSync(path.join(root, 'caller.pya'), caller);
    const repaired = await client.request('pyalamode/project', {}); assert.equal(repaired.report.status, 0);
    const definitions = await client.request('textDocument/definition', {textDocument: {uri: callUri}, position: {line: 3, character: 12}});
    assert.ok(definitions.some(row => row.uri === uri && row.range.start.line === 2 && row.range.start.character === 4));
    const references = await client.request('textDocument/references', {textDocument: {uri}, position: {line: 2, character: 5}, context: {includeDeclaration: true}});
    assert.ok(references.some(row => row.uri === callUri));
    const formatParams = {textDocument: {uri}, options: {tabSize: 4, insertSpaces: true}, pyalamode: {version: 3, snapshot: repaired.snapshot}};
    const edits = validateTextEdits(await client.request('textDocument/formatting', formatParams), preview.after);
    assert.ok(edits.length); assert.equal(fs.readFileSync(path.join(root, 'dialect.pya'), 'utf8'), bad);
    await assert.rejects(client.request('textDocument/formatting', {...formatParams, pyalamode: {version: 1, snapshot: repaired.snapshot}}), /-32801/);
    await assert.rejects(client.request('textDocument/formatting', {...formatParams, pyalamode: {version: 3, snapshot: '0'.repeat(64)}}), /-32801/);
    await assert.rejects(client.request('textDocument/formatting', {...formatParams, options: {tabSize: 0, insertSpaces: true}}), /-32602/);
    await assert.rejects(client.request('pyalamode/preview', params), /-32801/);
    const formatted = preview.after.replace('val  result', 'val result').replace(/[\t ]+(?=\r?$)/gm, '');
    client.notify('textDocument/didChange', {textDocument: {uri, version: 4}, contentChanges: [{text: formatted}]});
    const after = await client.request('pyalamode/project', {}); assert.equal(after.report.status, 0);
    assert.deepEqual(await client.request('textDocument/formatting', {...formatParams, pyalamode: {version: 4, snapshot: after.snapshot}}), []);
    fs.writeFileSync(path.join(root, 'dialect.pya'), formatted);
    client.notify('textDocument/didSave', {textDocument: {uri}});
    const artifact = path.join(root, 'build', 'mapped');
    const built = JSON.parse(journal.child('mapped-build', [python, '-I', '-m', 'pyalamode', 'build', path.join(root, 'dialect.pya'), '--root', root, '--output', artifact, '--json'], root));
    assert.equal(built.status, 0);
    const current = await client.request('pyalamode/project', {});
    const generated = fs.readFileSync(path.join(artifact, 'dialect.py'), 'utf8');
    const line = generated.split(/\r\n|\r|\n/).findIndex(row => row.startsWith('def café(')); assert.ok(line >= 0);
    const located = validateSourceLocation(await client.request('pyalamode/sourceLocation', {artifactUri: pathToFileURL(artifact).href,
      path: 'dialect.py', position: {line, character: 4}, snapshot: current.snapshot}), current.snapshot);
    assert.equal(located.provenance.status, 0); assert.equal(located.provenance.verified, true);
    assert.equal(located.location.uri, uri); assert.equal(located.location.range.start.line, 2);
    assert.equal(located.location.range.start.character, 4); assert.equal(fs.readFileSync(path.join(root, 'dialect.pya'), 'utf8'), formatted);
    assert.deepEqual(failures, []);
    if (process.env.PYALAMODE_CLIENT_REPORT) {
      const reportPath = process.env.PYALAMODE_CLIENT_REPORT, previous = fs.existsSync(reportPath) ? JSON.parse(fs.readFileSync(reportPath, 'utf8')) : {};
      fs.writeFileSync(reportPath, JSON.stringify({...previous, dialect: {provenance: client.provenance, wire, diagnostic, hovered, definitions,
        references, repairSource, repairReport, repairDiagnostic, preview, repaired, edits, formatted, after, built, located, sourceAutomaticallyEdited: false}}, null, 2));
    }
  } catch (error) { failure = error; throw error; }
  finally {
    let cleanupError;
    try { await client?.stop(); } catch (error) { cleanupError = error; }
    const partial = {passed: !failure && !cleanupError, error: failureRecord(failure || cleanupError), cleanupError: failureRecord(cleanupError),
      wire, failures, provenance: client?.provenance ?? null, fixtureRetained: Boolean(failure || cleanupError),
      cleanupIntent: 'remove only this fresh fixture on full success; retain failed fixture/artifact bytes'};
    if (journal.retain(partial) && !cleanupError) cleanupError = new Error('Transport raw capture failed; fixture retained');
    if (!failure && !cleanupError) { try { fs.rmSync(root, {recursive: true, force: true}); } catch (error) { cleanupError = error; } }
    journal.finish({...partial, passed: !failure && !cleanupError, error: failureRecord(failure || cleanupError),
      cleanupError: failureRecord(cleanupError), fixtureRetained: fs.existsSync(root)});
    if (!failure && cleanupError) throw cleanupError;
  }
});
