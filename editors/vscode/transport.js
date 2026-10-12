'use strict';
const {spawn} = require('node:child_process');
const {EventEmitter} = require('node:events');
const {TextDecoder} = require('node:util');
const path = require('node:path');
const fs = require('node:fs');
const {pathToFileURL} = require('node:url');
const MAX_HEADER = 8192, MAX_BODY = 8 * 1024 * 1024;
const HEX64 = /^[0-9a-f]{64}$/;
const META_KEYS = ['schema', 'target', 'pythonExecutable', 'pythonVersion', 'platform', 'root',
  'filesystemEncoding', 'filesystemErrors', 'languages', 'syntaxVersion', 'sourceMapSchema', 'formatProfile'];
const exactKeys = (value, keys) => value !== null && typeof value === 'object' && !Array.isArray(value) &&
  Object.keys(value).sort().join(',') === [...keys].sort().join(',');
const position = value => exactKeys(value, ['line', 'character']) &&
  Number.isSafeInteger(value.line) && value.line >= 0 && Number.isSafeInteger(value.character) && value.character >= 0;
const compare = (left, right) => left.line - right.line || left.character - right.character;
const validRange = value => exactKeys(value, ['start', 'end']) && position(value.start) &&
  position(value.end) && compare(value.start, value.end) <= 0;
const digest = value => typeof value === 'string' && HEX64.test(value);
const positive = value => Number.isSafeInteger(value) && value >= 1;
const relativePath = value => typeof value === 'string' && value.length > 0 && value.length <= 4096 &&
  !/[\\:\x00-\x1f\x7f-\x9f]/.test(value) && !value.split('/').some(part => !part || part === '.' || part === '..');
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);

function validateTextEdits(edits, text) {
  if (!Array.isArray(edits) || typeof text !== 'string') throw new Error('Invalid Pyalamode formatting edits');
  const lines = text.split(/\r\n|\r|\n/), boundary = point => {
    const line = lines[point.line];
    return line !== undefined && point.character <= line.length &&
      !(point.character > 0 && point.character < line.length &&
        /[\uD800-\uDBFF]/.test(line[point.character - 1]) && /[\uDC00-\uDFFF]/.test(line[point.character]));
  };
  for (const item of edits) {
    if (!exactKeys(item, ['range', 'newText']) || typeof item.newText !== 'string' ||
        !validRange(item.range) || !boundary(item.range.start) || !boundary(item.range.end))
      throw new Error('Invalid Pyalamode formatting edits');
  }
  const ordered = [...edits].sort((a, b) => compare(a.range.start, b.range.start) || compare(a.range.end, b.range.end));
  for (let i = 1; i < ordered.length; i++) {
    if (compare(ordered[i - 1].range.end, ordered[i].range.start) > 0 ||
        compare(ordered[i - 1].range.start, ordered[i].range.start) === 0)
      throw new Error('Overlapping Pyalamode formatting edits');
  }
  return edits;
}

function validateSourceLocation(result, snapshot) {
  const proof = result?.provenance;
  if (!exactKeys(result, ['schema', 'snapshot', 'freshness', 'location', 'provenance']) || result.schema !== 1 ||
      result.snapshot !== snapshot || !digest(snapshot) || typeof result.freshness !== 'string' ||
      !exactKeys(proof, ['schema', 'kind', 'status', 'verified', 'artifact', 'generated', 'authored', 'exact',
        'segments', 'snapshot', 'inputs', 'diagnostics']) || proof.schema !== 1 || proof.kind !== 'pyalamode-source-location' ||
      ![0, 1, 2].includes(proof.status) || !digest(proof.snapshot) || typeof proof.verified !== 'boolean' ||
      typeof proof.artifact !== 'string' || !path.isAbsolute(proof.artifact) ||
      !exactKeys(proof.generated, ['path', 'line', 'column', 'column_encoding', 'sha256']) ||
      !relativePath(proof.generated.path) || !proof.generated.path.endsWith('.py') || !positive(proof.generated.line) ||
      !positive(proof.generated.column) || proof.generated.column_encoding !== 'utf-8-bytes' || !digest(proof.generated.sha256) ||
      !exactKeys(proof.inputs, ['artifacts', 'evidence_sha256', 'product_artifacts']) || !object(proof.inputs.artifacts) ||
      !object(proof.inputs.product_artifacts) || !digest(proof.inputs.evidence_sha256) ||
      !Array.isArray(proof.segments) || !Array.isArray(proof.diagnostics)) throw new Error('Invalid Pyalamode source provenance');
  if (proof.status !== 0) {
    if (proof.verified || proof.authored !== null || proof.exact !== null || proof.segments.length || result.location !== null)
      throw new Error('Unverified Pyalamode source location');
    return result;
  }
  if (!proof.verified || typeof proof.exact !== 'boolean' || !proof.segments.every(index => Number.isSafeInteger(index) && index >= 0) ||
      !exactKeys(proof.authored, ['path', 'source_copy', 'line', 'column', 'end_line', 'end_column', 'column_encoding', 'sha256']) ||
      !relativePath(proof.authored.path) || !relativePath(proof.authored.source_copy) || !digest(proof.authored.sha256) ||
      ![proof.authored.line, proof.authored.column, proof.authored.end_line, proof.authored.end_column].every(positive) ||
      proof.authored.column_encoding !== 'utf-8-bytes' || proof.authored.end_line < proof.authored.line ||
      (proof.authored.end_line === proof.authored.line && proof.authored.end_column < proof.authored.column) ||
      !exactKeys(result.location, ['uri', 'range']) || typeof result.location.uri !== 'string' || !validRange(result.location.range))
    throw new Error('Invalid Pyalamode source location');
  return result;
}

function frame(message) {
  const body = Buffer.from(JSON.stringify(message), 'utf8');
  if (body.length > MAX_BODY) throw new Error('Pyalamode frame exceeds 8MiB');
  return Buffer.concat([Buffer.from(`Content-Length: ${body.length}\r\n\r\n`), body]);
}

class Frames {
  constructor(receive) { this.buffer = Buffer.alloc(0); this.length = null; this.receive = receive; }
  push(chunk) {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    for (;;) {
      if (this.length === null) {
        const end = this.buffer.indexOf('\r\n\r\n');
        if (end < 0) { if (this.buffer.length > MAX_HEADER) throw new Error('oversized header'); return; }
        if (end > MAX_HEADER || this.buffer.subarray(0, end).some(byte => byte > 127)) throw new Error('invalid header');
        const lines = this.buffer.subarray(0, end).toString('ascii').split('\r\n');
        let length = null;
        for (const line of lines) {
          const match = /^([^:]+):\s*(.*?)\s*$/.exec(line);
          if (!match) throw new Error('malformed header');
          const name = match[1].toLowerCase(), value = match[2];
          if (name === 'content-length') {
            if (length !== null || !/^(0|[1-9][0-9]*)$/.test(value)) throw new Error('invalid Content-Length');
            length = Number(value);
          } else if (name !== 'content-type' || !/^application\/(?:vscode-jsonrpc|json)(?:;\s*charset=utf-?8)?$/i.test(value)) throw new Error('unsupported header');
        }
        if (!Number.isSafeInteger(length) || length < 1 || length > MAX_BODY) throw new Error('invalid frame length');
        this.length = length; this.buffer = this.buffer.subarray(end + 4);
      }
      if (this.buffer.length < this.length) return;
      const bytes = this.buffer.subarray(0, this.length);
      this.buffer = this.buffer.subarray(this.length); this.length = null;
      const message = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(bytes));
      if (!message || Array.isArray(message) || message.jsonrpc !== '2.0') throw new Error('invalid JSON-RPC envelope');
      this.receive(message);
    }
  }
  finish() { if (this.length !== null || this.buffer.length) throw new Error('truncated server frame'); }
}

class Client extends EventEmitter {
  constructor(python, root, options = {}) {
    super();
    if (typeof python !== 'string' || !path.isAbsolute(python)) throw new Error('Configure an absolute pyalamode.pythonPath');
    fs.accessSync(python, fs.constants.X_OK);
    this.root = fs.realpathSync(root); this.python = python;
    this.pythonOwner = path.join(fs.realpathSync(path.dirname(python)), path.basename(python));
    this.args = ['-I', '-m', 'pyalamode.editor', '--stdio', '--root', this.root];
    this.pending = new Map(); this.abandoned = new Set(); this.next = 1;
    this.timeout = options.timeout || 30000; this.dead = false; this.stopping = false;
    this.child = spawn(python, this.args, {cwd: this.root, shell: false, stdio: ['pipe', 'pipe', 'pipe']});
    this.frames = new Frames(message => this.receive(message));
    this.child.stdout.on('data', chunk => { if (!this.dead) { try { this.frames.push(chunk); } catch (error) { this.fail(error); } } });
    this.child.stdout.on('end', () => { if (!this.stopping && !this.dead) { try { this.frames.finish(); } catch (error) { this.fail(error); } } });
    this.stderrBytes = 0;
    this.child.stderr.on('data', chunk => {
      const available = 65536 - this.stderrBytes;
      if (available <= 0) return;
      const selected = chunk.subarray(0, available); this.stderrBytes += selected.length;
      this.emit('log', selected.toString('utf8'));
      if (chunk.length > available) this.emit('log', '\nPyalamode stderr truncated at 64KiB\n');
    });
    this.child.on('error', error => this.fail(error));
    this.child.stdin.on('error', error => { if (!this.stopping) this.fail(error); });
    this.child.on('exit', (code, signal) => { this.emit('exit', {code, signal}); if (!this.stopping) this.fail(new Error(`Pyalamode server exited (${code}, ${signal})`)); });
  }
  send(message) {
    if (this.dead) throw new Error('Pyalamode server is unavailable');
    this.child.stdin.write(frame(message)); this.emit('wire', {direction: 'client', message});
  }
  notify(method, params) { this.send({jsonrpc: '2.0', method, params}); }
  request(method, params, token) {
    if (this.dead) return Promise.reject(new Error('Pyalamode server is unavailable'));
    if (this.pending.size >= 128) return Promise.reject(new Error('Too many pending Pyalamode requests'));
    if (token?.isCancellationRequested) return Promise.reject(new Error('Pyalamode request cancelled'));
    const id = this.next++;
    return new Promise((resolve, reject) => {
      const abandon = reason => {
        const entry = this.pending.get(id); if (!entry) return;
        this.pending.delete(id); this.abandoned.add(id);
        if (this.abandoned.size > 128) this.abandoned.delete(this.abandoned.values().next().value);
        entry.dispose(); reject(new Error(reason));
      };
      let subscription;
      const timer = setTimeout(() => abandon('Pyalamode request timed out; refresh required'), this.timeout);
      const dispose = () => { clearTimeout(timer); subscription?.dispose(); };
      this.pending.set(id, {resolve, reject, dispose});
      subscription = token?.onCancellationRequested(() => abandon('Pyalamode request cancelled'));
      try { this.send({jsonrpc: '2.0', id, method, params}); } catch (error) { this.pending.delete(id); dispose(); reject(error); }
    });
  }
  receive(message) {
    this.emit('wire', {direction: 'server', message});
    if (typeof message.method === 'string') {
      if (Object.hasOwn(message, 'id')) this.send({jsonrpc: '2.0', id: message.id, error: {code: -32601, message: 'Client method not supported'}});
      else this.emit('notification', message);
      return;
    }
    if (!Number.isSafeInteger(message.id) || Object.hasOwn(message, 'result') === Object.hasOwn(message, 'error')) throw new Error('invalid server response');
    if (this.abandoned.delete(message.id)) return;
    const entry = this.pending.get(message.id);
    if (!entry) throw new Error('unexpected server response id');
    if (Object.hasOwn(message, 'error')) {
      if (!message.error || !Number.isInteger(message.error.code) || typeof message.error.message !== 'string') throw new Error('invalid server error');
      this.pending.delete(message.id); entry.dispose();
      entry.reject(new Error(`${message.error.code}: ${message.error.message}`));
    } else { this.pending.delete(message.id); entry.dispose(); entry.resolve(message.result); }
  }
  fail(error) {
    if (this.dead) return; this.dead = true;
    for (const entry of this.pending.values()) { entry.dispose(); entry.reject(error); }
    this.pending.clear(); this.emit('failure', error); this.child.kill();
  }
  async initialize() {
    const result = await this.request('initialize', {rootUri: pathToFileURL(this.root).href, clientInfo: {name: 'pyalamode-local', version: '0.1.0'}});
    const caps = result?.capabilities, meta = caps?.experimental?.pyalamode;
    if (caps?.positionEncoding !== 'utf-16' || caps.textDocumentSync?.openClose !== true || caps.textDocumentSync?.change !== 1 || caps.textDocumentSync?.save?.includeText !== false || !['hoverProvider', 'definitionProvider', 'referencesProvider', 'documentSymbolProvider', 'codeActionProvider', 'documentFormattingProvider'].every(name => caps[name] === true) || result?.serverInfo?.name !== 'pyalamode' || typeof result.serverInfo.version !== 'string' || !result.serverInfo.version || !exactKeys(meta, META_KEYS) || meta.schema !== 2 || meta.root !== this.root || meta.pythonExecutable !== this.pythonOwner || meta.pythonVersion !== '3.13.1' || meta.target !== 'cpython-3.13.1' || !['darwin', 'linux'].includes(meta.platform) || meta.filesystemEncoding !== 'utf-8' || meta.filesystemErrors !== 'surrogateescape' || JSON.stringify(meta.languages) !== '["python","pyalamode"]' || meta.syntaxVersion !== 'pyalamode.syntax-v1' || meta.sourceMapSchema !== 1 || meta.formatProfile !== 'val-whitespace-v1') {
      const error = new Error('Incompatible Pyalamode server/runtime metadata'); this.fail(error); throw error;
    }
    this.provenance = {python: this.python, args: this.args, cwd: this.root, server: result};
    this.notify('initialized', {}); this.initialized = true; return result;
  }
  async stop() {
    if (this.stopping) return; this.stopping = true;
    if (!this.dead) {
      let timer;
      try { await Promise.race([this.request('shutdown', null), new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('shutdown timeout')), 2000); })]); this.notify('exit', null); } catch (_) {} finally { clearTimeout(timer); }
    }
    for (const entry of this.pending.values()) { entry.dispose(); entry.reject(new Error('Pyalamode server stopped')); }
    this.pending.clear(); this.dead = true; this.child.stdin.end();
    if (this.child.exitCode !== null || this.child.signalCode !== null) return;
    await new Promise(resolve => { const timer = setTimeout(() => { this.child.kill(); resolve(); }, 1000); this.child.once('exit', () => { clearTimeout(timer); resolve(); }); });
  }
}
module.exports = {Client, Frames, frame, MAX_HEADER, MAX_BODY, HEX64, exactKeys, validateTextEdits, validateSourceLocation};
