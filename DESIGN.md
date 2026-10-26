# Design: Adapted Research Architecture

## 1. Objective

Build a research-agent platform that has the extensibility of an agent collection and the operational discipline of Codex.

The platform should be good at several scenarios—literature review, data analysis, code optimization, paper reproduction, and empirical research—without pretending that one agent or one fixed pipeline is best for all of them.

The design separates two concerns:

1. **Research control plane:** owns durable state, workflow transitions, evidence, approvals, evaluation, memory, and audit.
2. **Agent collection:** supplies replaceable planners, retrievers, coders, analysts, reviewers, and writers.

An agent may propose work and execute granted tools. It cannot declare its own result valid, promote its own claim, silently enlarge its permissions, or mutate authoritative project memory directly.

## 2. Why Codex is the architectural inspiration

Codex demonstrates several useful platform properties:

- a core engine can be independent of CLI, TUI, IDE, or desktop clients;
- threads can start, resume, fork, interrupt, and stream typed events;
- tools, skills, hooks, plugins, providers, and clients connect through explicit interfaces;
- permission and approval state is scoped to the action and session rather than hidden in a prompt;
- command output, file changes, and model messages are typed items with lifecycle states;
- project instructions and capabilities are discovered from known roots;
- the runtime owns execution and policy while higher-level objectives remain external.

`adapted_research_arch` preserves those boundaries but introduces research-native objects. A Codex turn is too coarse to represent a scientific claim, an experiment candidate, a verifier decision, or a claim-promotion gate. Those become first-class records here.

## 3. Design principles

### 3.1 Agents are packages, not authorities

An agent package declares identity, capabilities, inputs, outputs, tools, default instructions, risk, and evaluators. The runtime resolves permissions and validates outputs.

### 3.2 Research truth comes from evidence and external evaluators

Model confidence is metadata. Promotion requires evidence locators and, when applicable, an executable evaluator, statistical test, formal verifier, or human decision.

### 3.3 One stage has one inspectable responsibility

Planning, retrieval, execution, evaluation, claim promotion, and writing are different transitions. Combining them in one opaque agent call makes failure attribution impossible.

### 3.4 The simplest credible control is mandatory

Following the lesson from `loopr1_worldmodel`, advanced search, reflection, learned ranking, or multi-agent debate must be compared with a matched simple control. Novel mechanisms are optional until they improve the external outcome.

### 3.5 State is event-driven and resumable

Every authoritative transition produces a typed event. Materialized SQLite views make reads efficient, but the append-only event stream and content-hashed artifacts remain the audit source.

### 3.6 Capability loading is selective

The runtime loads only agents and skills required by the selected workflow. A large catalog must not become one giant prompt.

### 3.7 Safety follows impact, not agent identity

The same agent may read papers without approval but require approval to launch a GPU job, modify source, access a new network host, or publish externally.

## 4. System architecture

```text
+------------------------------ Clients -------------------------------+
| CLI | TUI | IDE | Web | automation client                            |
+--------------------------------+-------------------------------------+
                                 | JSON-RPC/JSONL + streamed events
+--------------------------------v-------------------------------------+
| Research app server                                                  |
| handshake | schema version | subscriptions | backpressure | auth     |
+--------------------------------+-------------------------------------+
                                 |
+--------------------------------v-------------------------------------+
| Research control plane                                               |
| projects | threads | workflows | stages | attempts | gates | approvals|
+------------+-------------------+-------------------+------------------+
             |                   |                   |
     +-------v--------+  +-------v--------+  +-------v----------------+
     | Agent registry |  | Policy engine |  | Evidence and state      |
     | discovery      |  | permissions   |  | artifacts, claims,      |
     | trust/pinning  |  | budgets       |  | memory, events, metrics |
     | routing        |  | approvals     |  | evaluator records       |
     +-------+--------+  +-------+--------+  +-------+----------------+
             |                   |                   |
+------------v-------------------v-------------------v------------------+
| Execution plane                                                       |
| model/command adapters | MCP/tools | containers | worktrees | SLURM  |
| retrievers | local compute | formal and statistical evaluators       |
+------------------------------------------------------------------------+
```

### 4.1 Research app server

The server is the stable boundary between the core and clients. It uses bidirectional JSON-RPC-style messages over JSONL initially. WebSocket support can be added later without changing method semantics.

The server is responsible for:

- connection initialization and capability negotiation;
- schema-version reporting;
- project, thread, workflow, and run APIs;
- event subscriptions and replay;
- approval and structured-input requests;
- bounded queues, overload errors, and client retry hints;
- schema generation for client SDKs.

The server does not contain scientific planning logic.

### 4.2 Research control plane

The control plane interprets declarative workflows and owns stage transitions. It decides when an agent can run, what context it receives, which gate follows it, whether another attempt is allowed, and what state becomes durable.

It is the only component allowed to:

- mark a stage complete;
- promote a claim;
- accept a candidate as a new baseline;
- commit reviewed observations to project memory;
- declare a workflow complete, failed, stopped, or inconclusive.

### 4.3 Agent registry and router

The registry discovers agent packages from built-in, user, and project roots. It parses manifests, validates schemas, resolves trust and versions, and exposes a capability index.

The router uses explicit constraints rather than free-form role invention:

```text
required capability
  + input/output schema compatibility
  + scenario tags
  + provider/environment availability
  + risk and permission compatibility
  + budget limits
  + pinned preference or measured evaluator score
  → selected agent package
```

The selected package ID, version, source root, manifest hash, instruction hash, model/provider, and tool set are pinned into the attempt record. Hot reload affects future attempts only.

### 4.4 Policy engine

The policy engine combines:

- project trust;
- workflow stage risk;
- agent-declared permissions;
- tool capability annotations;
- user control mode;
- environment limits;
- remaining time and cost budgets.

The result is an effective permission profile, never broader than the intersection of those inputs.

### 4.5 Evidence and state stores

The first implementation uses ordinary files plus SQLite:

```text
project/
  research.yaml
  runs/<run-id>/
    manifest.json
    events.jsonl
    artifacts/
    attempts/
    candidates/
  memory/
    raw/
    reviewed/
  research.sqlite
```

Large artifacts remain files addressed by digest. SQLite stores indexed metadata, relationships, and materialized workflow state. This keeps projects inspectable and avoids requiring external infrastructure for a local run.

## 5. Core entities

| Entity | Purpose | Key invariant |
|---|---|---|
| Project | Durable research objective and roots | Owns policies, memory, and runs; never inferred from a chat session |
| Thread | Human/agent interaction history | May start, resume, fork, or interrupt without altering completed artifacts |
| Workflow run | One scenario execution | Pins workflow, agents, providers, permissions, and budgets |
| Stage | Declarative research transition | Has typed inputs, outputs, risk, gates, and dependencies |
| Attempt | One agent execution for a stage | Immutable after completion; retries create new attempts |
| Item | Streamed model/tool/file/approval event | Has started/completed/failed/declined lifecycle |
| Artifact | Content-addressed file or structured output | Digest and producing attempt are mandatory |
| Claim | Testable statement derived from evidence | Cannot be promoted without valid evidence references |
| Evidence reference | Locator into an artifact or external source | Source identity and exact locator are mandatory |
| Evaluation | External judgment of an artifact or candidate | Evaluator version and contract are pinned |
| Candidate | Isolated mutable research branch | Never overwrites the baseline before promotion |
| Observation | Memory record with provenance and confidence | Raw record is immutable; corrections use relations |
| Approval | Human or policy decision at an impact boundary | Scope and granted subset are explicit |

## 6. Agent collection design

An agent is a directory containing a manifest and instructions:

```text
agents/paper-retriever/
  agent.json
  AGENT.md
  skills/
  prompts/
  evals/
  tests/
  assets/
```

The manifest declares:

- stable ID, version, description, and maturity;
- capabilities and scenario tags;
- accepted and produced schema IDs;
- execution adapter and provider requirements;
- allowed tools and requested permissions;
- risk level and whether implicit routing is allowed;
- required evaluators and default budgets;
- instruction and asset digests for releases.

### 6.1 Agent, skill, tool, workflow, and evaluator are different

| Object | Meaning |
|---|---|
| Agent | Bounded decision-maker that consumes and produces typed stage data |
| Skill | On-demand method instructions and optional scripts loaded by an agent |
| Tool | Executable capability such as shell, retriever, Python, MCP, or scheduler |
| Workflow | Ordered or branching composition of stages, gates, and agents |
| Evaluator | Independent authority that judges an output or candidate |

Keeping these distinct prevents the collection from becoming a directory of overlapping prompts.

### 6.2 Trust states

Agent packages move through four states:

1. `discovered`: metadata can be listed, but code cannot run.
2. `trusted`: manifest and instruction hashes were approved; declared actions may run under policy.
3. `changed`: a previously trusted package changed and execution is blocked pending review.
4. `quarantined`: validation, security, or evaluator failures prevent routing.

Generated or self-improved agents always return to `discovered`; they never inherit the trust of their parent.

### 6.3 Composition rule

Each stage has one accountable primary agent. Optional helpers may retrieve, execute, or review, but they communicate through typed artifacts and events rather than unrestricted agent-to-agent chat.

This deliberately ignores role proliferation. A new agent role is justified only by a distinct capability, tool boundary, context policy, or evaluator.

## 7. Workflow mechanism

The stage state machine is:

```text
pending
  → ready
  → waiting_for_approval | running
  → evaluating
  → accepted | retryable | blocked | failed | inconclusive | stopped
```

A normal stage proceeds as follows:

1. Resolve completed dependencies and typed inputs.
2. Query relevant reviewed memory without mutating it.
3. Route or load the pinned agent package.
4. Resolve environment, budgets, permissions, and approvals.
5. Create an isolated attempt workspace.
6. Execute the agent and stream typed items.
7. Store outputs as content-addressed artifacts and candidate claims.
8. Run schema, evidence, scientific, and regression evaluators.
9. Apply the stage's promotion gate.
10. Commit accepted outputs and reviewed observations; otherwise preserve the failed attempt.

Retries never rewrite an attempt. Forking creates a new branch with an explicit parent.

## 8. Evidence and claim promotion

Claims move through explicit states:

```text
draft observation
  → evidence-linked claim
  → evaluator-supported claim
  → promoted project claim
  → superseded or contradicted claim
```

Required mechanism:

- the agent emits structured claims separately from prose;
- each claim contains one or more evidence references;
- internal artifacts use a digest plus locator such as JSON Pointer, table cell, line, metric key, or figure panel;
- external sources use persistent identity plus page, section, passage, or record locator;
- a validator resolves every locator before the stage can pass;
- scenario-specific evaluators determine whether resolution is enough or additional testing is required;
- a writer receives only promoted claims by default.

Numeric publication claims must resolve to the code/output record that produced the value, following `data-to-paper`. General claims use Claude Scholar-style promotion gates. ARIS-style independent review runs after deterministic checks, not instead of them.

## 9. Memory mechanism

Memory has two layers:

1. **Raw observation log:** immutable attempt-derived records with provenance.
2. **Reviewed project graph:** accepted observations and claims linked by typed support, contradiction, supersession, derivation, and relatedness edges.

Foreground agents can propose observations but cannot write reviewed memory. A consolidation stage:

- groups related raw observations;
- detects conflicting records;
- drafts relations and confidence changes;
- requests review when promotion would affect later workflows;
- leaves superseded information queryable.

Recurring patterns may generate skill proposals, but proposals are quarantined packages until schema validation, tests, security review, and human approval pass.

## 10. Controlled optimization

The default optimizer is deliberately minimal:

```text
one hypothesis
  → one isolated change
  → fixed evaluator
  → retain or reject
  → append event
```

This absorbs `autoresearch` and `codex-autoresearch` as the default control.

Optional search engines may be selected by workflow:

- AIDE-style typed draft/debug/improvement branches for executable ML;
- GEPA-style evaluator-trace reflection and Pareto retention for heterogeneous failures;
- AI-Scientist-v2-style best-first expansion for expensive scientific hypotheses;
- ADAS-style agent architecture search only in a quarantined experimental workflow.

Every advanced search must run against a matched linear or best-of-N control. Promotion uses external evaluation, not the optimizer's self-reported confidence.

## 11. Parallel execution

ClawTeam contributes the execution mechanism, not a permanent swarm topology.

The coordinator:

- creates one worktree or copied workspace per candidate;
- grants exclusive leases for GPUs, ports, datasets, and scheduler jobs;
- tracks heartbeat and cancellation state;
- receives artifacts through the event protocol;
- owns comparison and integration.

Workers do not share a writable candidate directory. Redis or multi-host messaging is deferred until local queues and SLURM adapters are insufficient.

## 12. Permissions and human control

### 12.1 Risk classes

| Risk | Examples | Default behavior |
|---|---|---|
| R0 inspect | Read project files, query reviewed memory | Automatic inside declared roots |
| R1 derive | Local parsing, non-mutating analysis | Automatic in sandbox |
| R2 mutate | Change code or generate candidate files | Isolated workspace; approval depends on mode |
| R3 execute | Run code, use GPU, submit scheduler job | Budget and environment approval required |
| R4 external | New network host, external write, data upload | Explicit approval and allow-list |
| R5 publish | Promote claim, release package, send manuscript | Explicit human approval |

### 12.2 Control modes

- `autopilot`: R0–R3 may run within preapproved budgets and roots; R4–R5 pause.
- `copilot`: R0–R1 automatic; R2–R3 pause at configured impact boundaries; R4–R5 always pause.
- `manual`: every stage requires approval.

Approvals grant only a subset of the requested permissions and have `item`, `stage`, or `run` scope. A grant cannot cross projects or silently survive a changed agent hash.

### 12.3 Evaluation firewall

Datasets and sources can be marked `train`, `development`, `evaluation`, or `publication_only`. The policy engine blocks evaluators from being exposed to proposal agents when a workflow declares a frozen evaluation contract.

This directly adapts the `loopr1_worldmodel` discipline: no prompt selection, hyperparameter tuning, memory retrieval, or skill evolution may consume evaluation-only rows.

## 13. Initial agent collection

The first collection should stay small:

| Agent | Primary responsibility | Main source inspiration |
|---|---|---|
| research-planner | Frame objective and select workflow | GPT Researcher, InternAgent |
| perspective-scout | Generate missing questions and viewpoints | STORM |
| paper-retriever | Retrieve and rerank scientific evidence | PaperQA |
| evidence-synthesizer | Build evidence-linked findings | PaperQA, data-to-paper |
| hypothesis-designer | Produce testable, falsifiable hypotheses | AI-Scientist-v2, AutoSci |
| experiment-engineer | Implement and launch bounded experiments | NanoResearch, MLE-agent |
| data-analyst | Execute analysis and record uncertainty | DATAGEN |
| reproduction-engineer | Interpret and reproduce papers | Paper2Code |
| integrity-reviewer | Challenge claims and verify provenance | ARIS, Claude Scholar |
| evidence-writer | Write only from promoted claims | data-to-paper |

Search strategies, tools, and skills are attached to these agents; they are not each turned into another conversational persona.

## 14. Deployment profiles

### Local single-user

- one app-server process;
- SQLite and files;
- local model or hosted provider adapter;
- process sandbox and Git worktrees;
- no external queue.

This is the reference implementation target.

### Private lab

- shared object store and PostgreSQL projections;
- local model endpoints;
- SLURM executor;
- project-scoped authentication and approval roles;
- evaluation datasets mounted read-only.

### Distributed service

- stateless app-server replicas;
- durable event broker;
- remote execution workers;
- artifact store and secret broker;
- centralized policy and audit.

This profile is deferred until the local contracts are proven.

## 15. Reliability and observability

The runtime records:

- queue, stage, agent, tool, and evaluator latency;
- token, compute, wall-time, and monetary budgets;
- attempt outcomes and retry causes;
- artifact and manifest digests;
- approval requests and granted subsets;
- evaluator versions and dataset partitions;
- saturation, floor, parser failure, and contamination indicators;
- negative and inconclusive outcomes.

Recovery uses idempotency keys for creates and launches. On restart, the controller reconstructs materialized state from events, checks artifact digests, reconciles still-running external jobs, and resumes only from a safe stage boundary.

## 16. Deliberate exclusions

The core does not initially include:

- a copied Codex runtime or UI;
- a mandatory 23-stage research pipeline;
- foundation-model training or reinforcement-learning infrastructure;
- an embedded crawler or vector database;
- a copied catalog of hundreds of skills;
- autonomous installation or activation of generated agents;
- a permanent multi-agent swarm;
- Redis or multi-host coordination;
- billing, marketplace, or cloud-account management;
- figure, poster, PowerPoint, or LaTeX rendering engines;
- autonomous external publishing.

These may be adapters or later products. Excluding them keeps the core's scientific invariants testable.

## 17. Architectural acceptance criteria

The architecture is successful when an implementation can demonstrate all of the following:

1. A workflow resumes after process failure without rerunning a completed stage.
2. A fork preserves parent provenance while isolating all writable state.
3. A changed agent package cannot run under its old trust decision.
4. An ungrounded or unresolved claim cannot be promoted.
5. A numeric result can be traced back to producing code and output.
6. Evaluation-only data cannot reach proposal, tuning, or memory contexts.
7. High-impact execution cannot start without the required approval and budget.
8. A failed evaluator leaves the attempt and artifacts inspectable.
9. A writer cannot silently consume draft claims as established results.
10. An advanced optimizer is compared with a matched simple control.
11. Negative, inconclusive, saturated, and floored outcomes remain first-class results.
12. CLI and another client can drive the same running project through the protocol.
