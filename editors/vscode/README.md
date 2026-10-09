# Pyalamode local VS Code client

This local desktop extension uses the installed Python checker server. It adds no npm runtime dependency, compiler or runtime purity registry. VS Code 1.139.1 on native macOS is the actual supported editor tested here; server/wire Linux testing is separate. Human repair usefulness is **UNMEASURED**.

Install Pyalamode into the supported CPython 3.13.1 virtual environment. In VS Code User settings set `pyalamode.pythonPath` to its absolute interpreter path, for example `/Volumes/Projects/pyalamode/.venv/bin/python`. Preserve the virtual environment path. Open one trusted local workspace containing existing Python files. The client starts that executable with `-I -m pyalamode.editor --stdio --root <workspace>`, without a shell; isolated startup excludes workspace import paths, user site and `PYTHON*` environment overrides. The installed environment must contain Pyalamode; relying on the workspace or `PYTHONPATH` to locate the tool is unsupported. Its Output channel records actual launch and server metadata. Missing configuration, unsupported targets and transport failures are visible unverified states.

For local development, run `code --extensionDevelopmentPath=/Volumes/Projects/pyalamode/editors/vscode /path/to/project`. For a finite installable package, run:

```sh
.venv/bin/python editors/vscode/package_vsix.py --output /tmp/pyalamode-local.vsix
code --install-extension /tmp/pyalamode-local.vsix
```

The installer command is an intentional local installation step. Automated verification always supplies temporary `--user-data-dir` and `--extensions-dir`; it never changes the normal user profile. No Marketplace publication is provided.

Problems show the same rule, authored range and first binding as the shared command engine. Hover and **Pyalamode: Inspect Project Contracts** retain exact inputs/results, source evidence, effects/origins, transitive external trust, failures, freshness, ordinary setup and selected guard coverage. Definitions and references cover actual checked declarations/direct calls; unsupported targets receive no guessed location. Unsaved overlays remain explicitly unsaved evidence, and closing restores disk analysis. **Refresh Diagnostics** obtains fresh policy/dependency/approval state; an earlier snapshot is not a live runtime certificate.

**Explain Rule or Operation** uses shared explanations. An eligible code action opens **Preview Proposed Repair** as read-only before/after documents. It leaves source/policy unchanged, shows limits and remaining diagnostics and rejects stale text. Edit the authored file yourself after reviewing semantics. No action adds effects, trust, ignored errors or changed failure behavior. **Open Authored Guard Boundary** accepts a local built artifact, exact public boundary and coverage phase/name; current validated evidence navigates to the original compatible source. It does not run the artifact or treat an arbitrary exception string as evidence. Translated source mapping remains a later milestone.

**Restart Local Server** resets the owned child and synchronizes open files. Restricted/remote/virtual/multi-root workspaces and untitled/new nonexisting files are unsupported. This client neither grants workspace trust nor approves external integrations.

`node --test editors/vscode/test/client.test.js` exercises bounded framing and the real server when `PYALAMODE_CLIENT_PYTHON` supplies an absolute supported interpreter. The actual installed Extension Development Host runner is `test/extension-host.cjs`; run it with `--extensionTestsPath` and isolated profile/workspace paths as recorded in `Docs/evidence/m09-client.md`. No operation performance interval or human usability result is implied by these checks.
