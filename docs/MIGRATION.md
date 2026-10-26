# Merge and cleanup

## Source snapshots

| Source | Pinned revision | Imported role |
|---|---|---|
| [possible_autoresearch](https://github.com/skill-stability/possible_autoresearch) | `97cdf786bad3141c8883c7639690da867a44ded5` | Research skills and topic portfolio |
| [imp_autoresesearch](https://github.com/skill-stability/imp_autoresesearch) | `7185f02cc00d46593173c5b1482762d33b254796` | Python runtime, tests, examples, and container tooling |

The destination starts from `fcaf6713f162cba68030292163b2088dc6fa62d3`.
This is a curated source-snapshot integration. The original repositories and their
histories are unchanged. Every retained or omitted source file is identified by its
original Git blob hash in [migration-manifest.json](migration-manifest.json).
Omitted material remains recoverable from the pinned source repositories.

## Retained content

- The complete active runtime and all original conformance tests, including command,
  model, and remote-tool adapters, policy, evidence, memory, and optimizer comparisons.
- Agent manifests, schemas, examples, Docker tooling, and nonredundant operating,
  architecture, protocol, and scenario documentation.
- Nine project-local research skills and two topic/review commands.
- The 45 B/T/H topic studies, four position-paper folders, and loop-R1 explorations,
  organized under `research/`. Seeds, specifications, reviews, experiment plans,
  reference catalogs, digests, Markdown/LaTeX paper sources, and translations remain.
- The current portion of the original `readme_draft.md`; the explicitly marked
  `=======before` historical duplicate section is omitted.

## Exclusions

The source snapshots contain 1,391 files. The integration retains
1,040 source files and excludes 351; excluded source
bytes total 46,459,729 (62.8% of the source size).
Counts describe file selection, not runtime speed or scientific performance.

| Excluded material | Reason |
|---|---|
| LaTeX build output and backup snapshots | Regenerable or superseded copies |
| PDFs, compressed paper bundles, and bitmap presentation exports | Keep editable research sources and SVG diagrams; link older exports to the source revision |
| Saved case runs, SQLite state, and copied workspaces | Bound to an external deployment; not reusable source or test fixtures |
| PDF report source, repeated executive summaries, and stale implementation plan | Covered by architecture, product, and conformance documentation |
| Old PDF-server deployment specification and source-specific standing instructions | Unrelated server paths and old project scope; current guidance is in `AGENTS.md` |
| Packaged skill archive | Duplicates the unpacked skill |
| Four corpus-calibration scripts | Hard-coded `/home/claude` paths and missing full original corpora; historical reports/catalogs remain with source links |
| Duplicate ignore rules and dependency-free lock stub | Consolidated ignore rules and existing Python packaging metadata |

Retired research topics remain as evidence and design notes. Retirement alone is not a
reason to delete their unique content. Links to omitted source artifacts point to their
pinned originals; SVG diagrams remain local.

## Integration changes

The `ara` CLI, `adapted_research_arch` import API, built-in agent IDs, and workflow IDs
remain compatible. Skills are instruction packages and are not automatically loaded as
runtime agents. Root documentation and command paths now describe the combined layout.

The imported runtime selected Bubblewrap whenever the executable was installed, even on
hosts where namespaces were prohibited. The merged runtime probes the exact sandbox
setup before executing an agent. Auto mode selects copied-workspace mode when the probe
fails; required mode still fails closed. A failed agent is never retried outside its
sandbox. Mount ordering also preserves workspaces located under `/tmp`. Diagnostics
report the usable backend rather than installation alone. Four regression tests cover
these paths, in addition to the original 28 tests.

Generated state, publication exports, backups, and credentials are ignored. CI runs the
conformance suite on Python 3.11 and 3.12. Archived research/calibration scores and cited
novelty findings have not been rerun or updated by this merge.

## Validation

- 32 conformance/regression tests pass, including all four workflows and the CLI/protocol path.
- The package wheel builds; an extracted-wheel literature-review run completes and verifies with all ten agent packages present.
- Runtime, test, skill-helper, and research-helper Python files compile; shell helpers pass syntax checks.
- The modified writing skill passes its frontmatter/structure validator.
- Imported file bytes were checked against the source Git blob hashes before documented adaptations.

The local environment cannot create Bubblewrap namespaces. Successful sandbox command
construction is covered by a controlled probe test; strict mode is tested to refuse an
unavailable boundary. Docker image execution requires Docker and authenticated model
CLIs and is not claimed as locally tested. Built-in agents remain deterministic fixtures.
