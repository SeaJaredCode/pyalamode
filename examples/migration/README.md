# Local migration walkthrough

Copy `core.py` and `pyproject.toml` into a fresh project directory, with Pyalamode installed in the supported CPython 3.13.1 environment. Run the following commands from that directory. The initial `total` function deliberately contains one reassignment finding; `doubled` is ordinary source.

```sh
pyalamode baseline --owner "project maintainer" --rationale "reviewed existing reassignment"
pyalamode regions
pyalamode ready
pyalamode check --audit
pyalamode convert function:core:total --preview
```

The baseline command returns 0 with an unverified write receipt and stores strict source status 1. Regions and readiness return 1 because the current strict source still fails. Audit returns 0 for the unchanged reviewed debt. The repair preview returns 0 and shows `result_2 = result + 100` followed by `return result_2`; source bytes remain unchanged. Review the diff and make those two edits yourself.

```sh
pyalamode check
pyalamode report --save
pyalamode convert function:core:doubled --preview
```

After that repair, check and report return 0. Report records the resolved finding and leaves the baseline unchanged. The adoption preview inserts the already available `@fun` marker before `doubled`, checks the complete overlay, and leaves the file unchanged. Apply the marker yourself after reviewing the candidate. `pyalamode ready` then has no remaining ordinary function candidate in this project. `total(300, 4)` still returns `1300` and `doubled(7)` returns `14` under ordinary Python.

An exact current export requirement can be added independently:

```toml
[tool.pyalamode]
required_exports = ["core:total", "core:doubled"]
```

Both exports must be selected and currently verified, even after a reviewed baseline replacement. A missing marker or failing body remains a current failure. `baseline --replace` needs a new explicit owner and rationale and records the valid predecessor; it cannot waive source or export failures. A saved report with debt returns command status 1 even though its nested write receipt is 0. JSON write commands use `{report, written}` to preserve those separate outcomes.

All views observe the full project, including ordinary analyzed writers; path arguments filter display. `.pyalamode` stores reviewed history and is excluded from source inventory. Existing exclusions also cover caches, virtual environments, build/dist directories, and the reserved `.pyalamode-build-` temporary build prefix. A user-chosen output directory outside those exclusions becomes source at the next observation. Readiness uses hypothetical selection to discover real direct/retained call edges; conversion checks actual markers and policy again without that hypothetical selector. Unknown dispatch and unsupported shapes remain review blockers. No command applies a source edit or grants trust. Human usefulness is **UNMEASURED**, with zero participants or attempts.
