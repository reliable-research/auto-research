# Auto Research

**Turn a research idea into a replayable, evidence-supported result.**

One controller owns the research loop: fix the question, register the hypotheses,
freeze a small experiment, measure, review the evidence, and write claims within
its scope. The same run ledger, artifact store, permission policy, and verifier
serve every stage.

## The research loop

| Stages | Commitment | Advancement check |
|---|---|---|
| S1–S2 | Worthwhile unknown; central question and scope | Sources and a frozen problem contract |
| S3–S4 | Falsifiable hypotheses and an implementable method | Competing explanations, interfaces, and review cards |
| S5 | Minimal experiment and decision protocol | Structured run plan frozen before execution |
| S6–S7 | Measurements, interpretation, and confirmation | Traceable raw records, recomputed summaries, and scope checks |
| S8 | Evidence-supported manuscript | Claims remain linked to accepted evidence |

The native `idea-to-paper` workflow pairs each of the eight stages with a separate
review, covering 48 stage-specific cards. Deterministic failures cannot be overridden
by a model's pass verdict. A frozen S2 question/scope or S5 protocol changes through a
new run, preserving the old record.

- `SIMULATED` produces a research plan with unmeasured result placeholders.
- `MEASURED` requires a trusted command executor at S6. Missing tools and errors
  remain invalid observations; real negative outcomes remain negative.

[Research-loop setup and contracts](docs/RESEARCH_LOOP.md) explains the adapters,
review records, measurement bridge, retries, and limits. The built-in fixture agents
remain useful for integration checks; they do not perform scientific research.

## Install and check

Python 3.11+; no third-party runtime dependencies.

```bash
python3 -m pip install -e .
ara doctor
ara workflows
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

After configuring the [research adapters](docs/RESEARCH_LOOP.md):

```bash
ara --project /path/to/project run start idea-to-paper \
  "Your research question" --evidence-mode SIMULATED \
  --agent-pin research.build_stage=research.builder \
  --agent-pin research.review_stage=research.reviewer \
  --agent-pin research.measure=research.measurement
```

The existing `ara` CLI, `adapted_research_arch` Python API, and four earlier workflows
remain available. [The product guide](docs/PRODUCT_GUIDE.md) covers initialization,
agent trust, approval, resumption, verification, and real model/remote-tool adapters.

## Repository

| Path | Purpose |
|---|---|
| [src/adapted_research_arch](src/adapted_research_arch) | One controller, ledger, policy, artifacts, claims, and memory |
| [research contracts](src/adapted_research_arch/research) | Stages, cards, evidence audit, runner, and six templates |
| [examples/agents](examples/agents) | Replaceable builder, reviewer, measurement, and retrieval packages |
| [tests](tests) | Runtime conformance and research-integrity checks |
| [.claude/skills](.claude/skills) | Optional research, digest, writing, and review methods |
| [research](research/README.md) | Historical portfolio and paper sources; not automatically loaded into prompts |
| [docs](docs/README.md) | Operation, architecture, contracts, and integration decisions |

Optional Docker tooling is described in [CONTAINERS.md](docs/CONTAINERS.md).
`ARA_OS_SANDBOX=required` requires a usable OS boundary; copied workspaces alone
provide operational isolation.

The [codeless integration](docs/CODELESS_INTEGRATION.md) records what was absorbed
and omitted. [Earlier migration notes](docs/MIGRATION.md) preserve the original source
snapshots. Historical research scores and novelty verdicts have not been revalidated.
