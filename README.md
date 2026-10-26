# Auto Research

A local-first workspace combining a tested Python research controller, reusable research
skills, and a source archive of topic studies.

The controller owns run state, permissions, artifacts, claim promotion, reviewed memory,
and audit events. Agent packages supply command, model, or remote-tool adapters.
The ten built-in agents are deterministic fixtures. Producing scientific results requires
real providers, data, and external evaluators.

## Start

Python 3.11 or newer is required; the core has no third-party runtime dependencies.

```bash
python3 -m pip install -e .
ara init /tmp/my-research --name "My research"
ara --project /tmp/my-research workflows
ara --project /tmp/my-research run start literature-review \
  "Compare durable memory designs for research agents"
```

Use the returned run ID:

```bash
ara --project /tmp/my-research run status RUN_ID
ara --project /tmp/my-research run verify RUN_ID
ara doctor
```

The existing `ara` command and `adapted_research_arch` Python API remain compatible.

## Repository

| Path | Contents |
|---|---|
| [src/adapted_research_arch](src/adapted_research_arch) | Controller, CLI, protocol, agents, evidence, and memory |
| [tests](tests) | Conformance tests and sandbox regressions |
| [examples](examples), [schemas](schemas) | Agent packages and workflow contracts |
| [.claude/skills](.claude/skills) | Research discussion, digest, writing, and review skills |
| [.claude/commands](.claude/commands) | Topic-to-draft and review workflows |
| [research](research/README.md) | Historical topic portfolio, reviews, plans, paper sources, and references |
| [docs](docs/README.md) | Operation, architecture, protocol, and migration notes |

Topic studies are historical inputs and drafts. Their outcomes, venue windows, novelty
assessments, and archived numbers have not been revalidated by this merge. The archive is
not automatically loaded into runtime prompts.

## Verify

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The suite covers four workflows, recovery, trust, approvals, budgets, evidence,
memory isolation, tamper detection, and CLI/protocol interoperability.
See [conformance](docs/CONFORMANCE.md) for results and limits.

## Real adapters and containers

[The product guide](docs/PRODUCT_GUIDE.md) explains adapters and agent pins.
The optional image includes the runtime, Codex CLI, and Claude Code:

```bash
./scripts/docker-ara.sh build
./scripts/docker-ara.sh run --rm ara ara doctor
```

See [container operation](docs/CONTAINERS.md) for credentials and writable-auth behavior.

`ARA_OS_SANDBOX=auto` probes Bubblewrap before selecting it. Unavailable namespaces
use copied-workspace mode. Set `ARA_OS_SANDBOX=required` to require a working OS
boundary; copied workspaces alone do not confine untrusted code.

## Sources

Merged from [possible_autoresearch](https://github.com/skill-stability/possible_autoresearch)
and [imp_autoresesearch](https://github.com/skill-stability/imp_autoresesearch).
[Migration notes](docs/MIGRATION.md) record source revisions, exclusions, and compatibility.
The original repositories remain unchanged.
