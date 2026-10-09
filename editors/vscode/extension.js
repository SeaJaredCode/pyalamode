'use strict';
const vscode = require('vscode');
const fs = require('node:fs');
const path = require('node:path');
const {Client} = require('./transport');
let active;

function activate(context) {
  const output = vscode.window.createOutputChannel('Pyalamode');
  const diagnostics = vscode.languages.createDiagnosticCollection('pyalamode');
  const content = new Map(), versions = new Map(), editorUris = new Map();
  let client, ready, serial = 0, disposed = false;
  const subscriptions = context.subscriptions;
  const range = item => new vscode.Range(item.start.line, item.start.character, item.end.line, item.end.character);
  const location = item => new vscode.Location(displayUri(vscode.Uri.parse(item.uri)), range(item.range));
  const rootFolder = () => {
    const folders = vscode.workspace.workspaceFolders || [];
    if (!vscode.workspace.isTrusted) throw new Error('Pyalamode requires a trusted local workspace');
    if (vscode.env.remoteName !== undefined || vscode.env.uiKind !== vscode.UIKind.Desktop) throw new Error('Pyalamode supports a local desktop extension host');
    if (folders.length !== 1 || folders[0].uri.scheme !== 'file') throw new Error('Pyalamode supports one local file workspace');
    return fs.realpathSync(folders[0].uri.fsPath);
  };
  const localUri = uri => {
    if (uri.scheme !== 'file' || uri.authority) throw new Error('Only local file URIs are supported');
    const canonical = fs.realpathSync(uri.fsPath), relative = path.relative(rootFolder(), canonical);
    if (relative.startsWith('..' + path.sep) || relative === '..' || path.isAbsolute(relative)) throw new Error('Location is outside the Pyalamode workspace');
    return vscode.Uri.file(canonical);
  };
  const displayUri = uri => {
    const canonical = localUri(uri), known = editorUris.get(canonical.toString());
    return known || vscode.Uri.file(path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, path.relative(rootFolder(), canonical.fsPath)));
  };
  const supported = document => document.languageId === 'python' && document.uri.scheme === 'file' && !document.isUntitled;
  const fail = error => { diagnostics.clear(); output.appendLine('Unverified: ' + error.message); vscode.window.showErrorMessage('Pyalamode: ' + error.message); };
  const virtual = (text, label) => {
    const uri = vscode.Uri.from({scheme: 'pyalamode-view', path: '/' + (++serial) + '/' + label});
    content.set(uri.toString(), text); return uri;
  };
  const openView = async (text, label) => vscode.window.showTextDocument(await vscode.workspace.openTextDocument(virtual(text, label)), {preview: true});
  const opened = document => {
    if (!supported(document)) return;
    let uri;
    try { uri = localUri(document.uri).toString(); } catch (_) { return; }
    const previous = editorUris.get(uri);
    if (previous && previous.toString() !== document.uri.toString()) throw new Error('Multiple open editor aliases for one canonical Python file are unsupported');
    if (versions.has(uri)) return;
    editorUris.set(uri, document.uri);
    client.notify('textDocument/didOpen', {textDocument: {uri, languageId: 'python', version: document.version, text: document.getText()}});
    versions.set(uri, document.version);
  };
  async function start() {
    if (disposed) throw new Error('Pyalamode client disposed');
    diagnostics.clear(); versions.clear(); editorUris.clear();
    if (client) await client.stop();
    if (disposed) throw new Error('Pyalamode client disposed');
    const root = rootFolder(), python = vscode.workspace.getConfiguration('pyalamode').get('pythonPath');
    const transport = new Client(python, root); client = transport;
    transport.on('log', text => { if (client === transport) output.append(text); });
    transport.on('failure', error => { if (client === transport) fail(error); });
    transport.on('notification', message => {
      if (client !== transport || disposed) return;
      if (message.method === 'window/logMessage') {
        const messageText = String(message.params?.message || 'server tooling notification');
        if (message.params?.type === 1) fail(new Error(messageText)); else output.appendLine(messageText);
        return;
      }
      if (message.method !== 'textDocument/publishDiagnostics') return;
      const params = message.params;
      try {
        const uri = displayUri(vscode.Uri.parse(params.uri)), current = versions.get(params.uri);
        if (current !== undefined && params.version !== current) return;
        const rows = params.diagnostics.map(item => {
          const diagnostic = new vscode.Diagnostic(range(item.range), item.message, item.severity === 2 ? vscode.DiagnosticSeverity.Warning : vscode.DiagnosticSeverity.Error);
          diagnostic.code = item.code; diagnostic.source = item.source; diagnostic.data = item.data;
          if (item.relatedInformation) diagnostic.relatedInformation = item.relatedInformation.map(related => new vscode.DiagnosticRelatedInformation(location(related.location), related.message));
          return diagnostic;
        });
        diagnostics.set(uri, rows);
      } catch (error) { fail(error); }
    });
    try {
      const initialized = await transport.initialize();
      output.appendLine(JSON.stringify(transport.provenance, null, 2));
      for (const document of vscode.workspace.textDocuments) opened(document);
      await transport.request('pyalamode/project', {});
      return initialized;
    } catch (error) { transport.fail(error); throw error; }
  }
  const restart = () => {
    const previous = ready;
    ready = (async () => { try { await previous; } catch (_) {} return start(); })();
    return ready;
  };
  const ensure = async () => { if (disposed) throw new Error('Pyalamode client disposed'); if (!ready) ready = start(); await ready; return client; };
  const query = async (method, document, extra, token) => {
    const transport = await ensure(), canonical = localUri(document.uri).toString();
    const version = document.version;
    const result = await transport.request(method, {textDocument: {uri: canonical}, ...extra}, token);
    if (document.version !== version || token?.isCancellationRequested) return null;
    return result;
  };
  const safe = fn => async (...args) => { try { return await fn(...args); } catch (error) { if (!/cancelled/.test(error.message)) fail(error); return undefined; } };
  subscriptions.push(output, diagnostics, vscode.workspace.registerTextDocumentContentProvider('pyalamode-view', {provideTextDocumentContent: uri => content.get(uri.toString()) || ''}));
  const selector = {language: 'python', scheme: 'file'};
  subscriptions.push(vscode.languages.registerHoverProvider(selector, {provideHover: safe(async (document, position, token) => {
    const value = await query('textDocument/hover', document, {position}, token); if (!value) return null;
    const text = typeof value.contents === 'string' ? value.contents : value.contents.value;
    const markdown = new vscode.MarkdownString(text); markdown.isTrusted = false; markdown.supportHtml = false;
    return new vscode.Hover(markdown, value.range ? range(value.range) : undefined);
  })}));
  subscriptions.push(vscode.languages.registerDefinitionProvider(selector, {provideDefinition: safe(async (document, position, token) => (await query('textDocument/definition', document, {position}, token) || []).map(item => { localUri(vscode.Uri.parse(item.uri)); return location(item); }))}));
  subscriptions.push(vscode.languages.registerReferenceProvider(selector, {provideReferences: safe(async (document, position, referenceContext, token) => (await query('textDocument/references', document, {position, context: referenceContext}, token) || []).map(item => { localUri(vscode.Uri.parse(item.uri)); return location(item); }))}));
  const symbol = item => {
    const result = new vscode.DocumentSymbol(item.name, item.detail || '', item.kind - 1, range(item.range), range(item.selectionRange));
    result.children = (item.children || []).map(symbol); return result;
  };
  subscriptions.push(vscode.languages.registerDocumentSymbolProvider(selector, {provideDocumentSymbols: safe(async (document, token) => (await query('textDocument/documentSymbol', document, {}, token) || []).map(symbol))}));
  subscriptions.push(vscode.languages.registerCodeActionsProvider(selector, {provideCodeActions: safe(async (document, requestedRange, actionContext, token) => {
    const values = await query('textDocument/codeAction', document, {range: {start: requestedRange.start, end: requestedRange.end}, context: {diagnostics: []}}, token);
    return (values || []).filter(item => item.command === 'pyalamode.preview' && Array.isArray(item.arguments) && item.arguments.length === 1);
  })}));
  subscriptions.push(vscode.workspace.onDidOpenTextDocument(document => { if (client?.initialized && !client.dead) { try { opened(document); } catch (error) { client.fail(error); } } }));
  subscriptions.push(vscode.workspace.onDidChangeTextDocument(event => {
    if (!client || client.dead || !supported(event.document) || !event.contentChanges.length) return;
    let uri; try { uri = localUri(event.document.uri).toString(); } catch (_) { return; }
    if (!versions.has(uri)) return;
    versions.set(uri, event.document.version); diagnostics.delete(event.document.uri);
    client.notify('textDocument/didChange', {textDocument: {uri, version: event.document.version}, contentChanges: [{text: event.document.getText()}]});
  }));
  subscriptions.push(vscode.workspace.onDidSaveTextDocument(document => {
    if (!client || client.dead || !supported(document)) return;
    let uri; try { uri = localUri(document.uri).toString(); } catch (_) { return; }
    if (versions.has(uri)) client.notify('textDocument/didSave', {textDocument: {uri}});
  }));
  subscriptions.push(vscode.workspace.onDidCloseTextDocument(document => {
    if (!client || client.dead || !supported(document)) return;
    let uri; try { uri = localUri(document.uri).toString(); } catch (_) { return; }
    if (!versions.delete(uri)) return;
    editorUris.delete(uri); diagnostics.delete(document.uri); client.notify('textDocument/didClose', {textDocument: {uri}});
  }));
  const command = (name, fn) => subscriptions.push(vscode.commands.registerCommand(name, safe(fn)));
  command('pyalamode.refresh', async () => { diagnostics.clear(); const transport = await ensure(); return transport.request('pyalamode/project', {}); });
  command('pyalamode.restart', restart);
  command('pyalamode.contracts', async () => { const report = await (await ensure()).request('pyalamode/project', {}); await openView(JSON.stringify(report, null, 2), 'contracts.json'); return report; });
  command('pyalamode.explain', async selected => {
    const text = typeof selected === 'string' ? selected : await vscode.window.showInputBox({prompt: 'Pyalamode rule or operation', value: 'PAL101'});
    if (!text) return;
    const result = await (await ensure()).request('pyalamode/explain', {symbol: text}); await openView(result.text + '\n\n' + JSON.stringify(result, null, 2), 'explanation.txt'); return result;
  });
  command('pyalamode.preview', async params => {
    if (!params || Object.keys(params).sort().join(',') !== 'diagnosticIndex,snapshot,uri,version') throw new Error('Select a current Pyalamode preview action');
    const uri = displayUri(vscode.Uri.parse(params.uri)), document = await vscode.workspace.openTextDocument(uri);
    if (document.version !== params.version) throw new Error('Preview is stale; refresh diagnostics');
    const result = await (await ensure()).request('pyalamode/preview', params);
    if (result.uri !== params.uri || result.version !== document.version || result.snapshot !== params.snapshot || result.before !== document.getText()) throw new Error('Preview source changed; refresh diagnostics');
    const before = virtual(result.before, 'before.py'), after = virtual(result.after, 'proposed.py');
    await vscode.commands.executeCommand('vscode.diff', before, after, result.title + ' — ' + uri.fsPath, {preview: true});
    output.appendLine('Preview only: ' + JSON.stringify({source: params.uri, status: result.status, remainingDiagnostics: result.remainingDiagnostics, limits: result.limits}));
    return result;
  });
  command('pyalamode.guardLocation', async params => {
    if (!params) {
      const artifact = await vscode.window.showOpenDialog({canSelectFolders: true, canSelectFiles: false, canSelectMany: false, openLabel: 'Select local guarded artifact'}); if (!artifact) return;
      const publicBoundary = await vscode.window.showInputBox({prompt: 'Exact public boundary (for example core:f)'}); if (!publicBoundary) return;
      const phase = await vscode.window.showQuickPick(['argument', 'return', 'local'], {placeHolder: 'Failure coverage phase'}); if (!phase) return;
      const name = phase === 'return' ? undefined : await vscode.window.showInputBox({prompt: 'Exact argument/local name'});
      const authoredLine = phase === 'local' ? Number(await vscode.window.showInputBox({prompt: 'Authored local line (one-based)'})) : undefined;
      params = {artifactUri: artifact[0].toString(), publicBoundary, phase, ...(name ? {name} : {}), ...(authoredLine ? {authoredLine} : {})};
    }
    localUri(vscode.Uri.parse(params.artifactUri));
    const result = await (await ensure()).request('pyalamode/guardLocation', params);
    const destination = displayUri(vscode.Uri.parse(result.location.uri));
    await vscode.window.showTextDocument(await vscode.workspace.openTextDocument(destination), {selection: range(result.location.range)});
    output.appendLine('Authored guard coverage: ' + JSON.stringify(result)); return result;
  });
  subscriptions.push(vscode.workspace.onDidChangeConfiguration(event => { if (event.affectsConfiguration('pyalamode.pythonPath')) { diagnostics.clear(); restart().catch(fail); } }));
  subscriptions.push(vscode.workspace.onDidChangeWorkspaceFolders(() => { diagnostics.clear(); restart().catch(fail); }));
  active = {ensure, diagnostics, get client() { return client; }, async dispose() { disposed = true; if (client) await client.stop(); content.clear(); versions.clear(); editorUris.clear(); }};
  if (vscode.workspace.isTrusted) ensure().catch(fail);
  return active;
}
async function deactivate() { if (active) await active.dispose(); active = undefined; }
module.exports = {activate, deactivate};
