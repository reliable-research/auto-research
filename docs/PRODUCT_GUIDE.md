# Product guide

## What the product is

Version 0.1 is a local research controller. It runs typed workflows through replaceable agent packages and records enough state to resume, inspect, and verify the work. The controller—not an agent—owns approvals, artifacts, claim promotion, reviewed memory, and the event ledger.

The included agents are deterministic fixtures. They prove the complete runtime path without credentials or network access. A useful deployment replaces individual fixtures with command, model, or remote-tool bridge packages while keeping the same workflow contracts.

## Install

Use Python 3.11 or newer:

```bash
python3 -m pip install -e .
ara --help
```

No third-party runtime package is required. For an isolated installation, create a virtual environment before running `pip install`.

## First project and run

```bash
ara init /tmp/research-demo --name "Research demo"
ara --project /tmp/research-demo agents list
ara --project /tmp/research-demo workflows
ara --project /tmp/research-demo run start data-analysis \
  "Test whether the fixture has an inspectable numeric result"
```

The start command returns a `run_...` identifier. Use it to inspect the durable state:

```bash
ara --project /tmp/research-demo run status RUN_ID
ara --project /tmp/research-demo run events RUN_ID
ara --project /tmp/research-demo run verify RUN_ID
```

`run verify` checks the event hash chain, artifact hashes, terminal attempts, and one completion event per completed stage.

## Control modes and approvals

`autopilot` executes R0–R3 stages within project policy. `copilot` requires approval from R2 upward. `manual` requires every stage to be approved. R4 and R5 always require approval.

```bash
ara --project /tmp/research-demo run start literature-review \
  "Review evidence" --mode copilot
ara --project /tmp/research-demo run approve RUN_ID --stage audit
ara --project /tmp/research-demo run resume RUN_ID
```

An approval is bound to the run, stage or run scope, agent package digest, permission subset, and effective budget. Editing a project agent invalidates both trust and prior digest-bound approvals.

## Recovery and lifecycle

Every stage creates a new attempt. If the controller process ends while an attempt is running, `run resume` marks that attempt interrupted, preserves its files, skips stages with authoritative completion events, and creates a fresh attempt for the first incomplete stage.

```bash
ara --project /tmp/research-demo run pause RUN_ID
ara --project /tmp/research-demo run resume RUN_ID
ara --project /tmp/research-demo run stop RUN_ID
ara --project /tmp/research-demo run retry RUN_ID
```

A stopped run is terminal. Retry is accepted only for a failed or blocked run. Negative, inconclusive, saturated, and floored scientific outcomes are successful workflow completions, not transport errors.

## Project layout

```text
research.json                 project identity and maximum policy
.ara/state.sqlite             durable projections, trust, approvals, claims, memory
.ara/threads/<id>/            fork provenance and isolated writable thread state
agents/<package>/             project-local agent packages
workspace/                    source copied into each attempt
runs/<run>/events.jsonl       hash-linked authoritative run events
runs/<run>/stages/            terminal structured stage results
runs/<run>/attempts/          isolated attempt workspaces
runs/<run>/artifacts/         content-addressed artifact bytes
```

Do not edit run files after completion. Verification reports modified or missing artifacts and altered event records.

## Agent adapters

A package consists of `agent.json` and `AGENT.md`. The runtime validates its identity, capabilities, adapter, permissions, risk, evaluators, budgets, and routing policy, then hashes all trusted package files.

Command adapters receive one JSON request on standard input and return one JSON object on standard output. Model adapters use `adapter.command` or `ARA_MODEL_BRIDGE`. Remote-tool adapters use `adapter.command` or `ARA_REMOTE_TOOL_BRIDGE`. Bridges receive the same bounded request, including provider/tool configuration, effective permissions, effective budget, reviewed memory, typed dependencies, and required gates.

Project packages begin as `discovered`:

```bash
ara --project /tmp/research-demo agents trust my.agent
ara --project /tmp/research-demo agents disable my.agent
```

Trusted project agents that carry R2/R3 permissions are never selected implicitly. Pin
them to one stage, or to every stage with a capability, and the pin is recorded in the
hash-linked `workflow/created` event so resume and approval cannot silently route a
different package:

```bash
ara --project /tmp/research-demo run start code-optimization \
  "Evaluate the fixed product contract" \
  --agent-pin baseline=my.product-evaluator \
  --agent-pin evaluate=my.product-evaluator
```

A capability-wide form such as
`--agent-pin experiment.execute=my.product-evaluator` covers both stages; a
stage-specific pin takes precedence. Protocol clients pass the same mapping as
`agentPins` on `workflow/start`.

If any package file changes, its state becomes `changed` and implicit or explicit routing fails until the new digest is trusted.

## Evidence, claims, and memory

Agents emit candidate claims. Artifact evidence must include an artifact ID and a locator such as `json:/metric`, `line:12`, `bytes:0-32`, or `sha256`. Numeric claims additionally require resolved `numeric` evidence. The integrity-review stage must return `reviewDecision=pass`; only then can the controller promote evidence-linked claims.

Writers receive promoted claims and no candidate claims. Their report record must reverse-link exactly to the promoted claim IDs.

Agent observations enter memory as `proposed`. Only a separate review can make them retrievable. Evaluation and publication-only observations remain hidden from agent retrieval even after review. Dependency context is recursively redacted when marked with those data classes.

## Protocol client

Start the newline-delimited JSON server:

```bash
ara serve --project-root /tmp/research-demo
```

Then send one JSON object per line. Expanded for readability:

```json
{
  "id": 1,
  "method": "initialize",
  "params": {"protocolVersions": ["1.0"]}
}
{
  "id": 2,
  "method": "workflow/start",
  "params": {
    "workflowId": "literature-review",
    "objective": "Review evidence"
  }
}
```

Use `event/list` with `afterSequence` to replay events after a cursor. CLI and protocol calls share the same project files and engine.

## Safety boundary

The runtime intersects package permissions with project policy, enforces wall-time and declared tool/source/cost usage, copies the source workspace per attempt, and checks that the source copy origin did not change. When a sandbox probe confirms Bubblewrap is usable, network-disabled agents automatically run with a read-only host mount, private network namespace, temporary `/tmp`, and only the attempt workspace writable. Set `ARA_OS_SANDBOX=required` to fail closed if this boundary is unavailable, or `off` to disable automatic use.

Bubblewrap's read-only host mount is not confidentiality isolation, and it cannot enforce hostname allowlists. On hosts without Bubblewrap, copied-workspace mode is operational isolation rather than a security boundary. Run untrusted adapters inside a hardened container or virtual machine, and place allowed network access behind an enforcement proxy. `ara doctor` reports the active boundary. Secrets should be supplied to a bridge by opaque handle rather than stored in a package or project file.

## Verification

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall -q src/adapted_research_arch tests
```

The acceptance mapping is in [CONFORMANCE.md](CONFORMANCE.md). Scheduler execution, container orchestration, graphical clients, autonomous package generation, and external publication remain later adapters rather than hidden behavior in the core.
