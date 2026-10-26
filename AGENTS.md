# Working in Auto Research

- Python 3.11+; the runtime is dependency-free. Preserve the `ara` CLI and
  `adapted_research_arch` import API.
- Validate runtime changes with
  `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Built-in agents are deterministic fixtures, not measured scientific capability.
  Keep real-adapter claims tied to their actual evaluator outputs.
- Keep runtime operation docs in `docs/` and topic materials in `research/`.
  See `docs/MIGRATION.md` for source revisions and provenance.
- Treat topic-root seeds as historical inputs. For new research, work in a topic's
  `discussion/` or a separate run/project; preserve existing evidence and dated logs.
- Do not fabricate results or citations. A retained proposal, historical score, or
  archived novelty verdict is not a new verification result.
- Keep generated state, credentials, PDFs, archives, and LaTeX build outputs out of Git.
  Use `ARA_OS_SANDBOX=required` where an OS boundary is required.
