# Component selection

## Selection rule

`adapted_research_arch` does not maximize the number of borrowed ideas. A component is absorbed only when it has:

1. an explicit state transition;
2. an evaluator or observable completion condition;
3. a boundary that can be implemented without importing an entire source product;
4. value in more than one research scenario, or unusually strong value in one important scenario;
5. compatibility with durable evidence, permissions, and audit state.

Components are classified as `core`, `optional`, `adapter`, `deferred`, or `ignored`.

## Core components

### Protocol runtime and clients

**Selected from:** Codex.

**Absorbed mechanism:** A protocol-facing engine owns durable threads and streams typed item lifecycles to replaceable clients. Start, resume, fork, interrupt, approval, and event subscription are protocol operations rather than UI behavior.

**Adaptation:** Replace conversational-only primitives with projects, workflow runs, stages, attempts, artifacts, claims, evaluations, and approvals. Keep UI independence, schema generation, bounded queues, capability negotiation, and sandboxed execution.

**Not absorbed:** The Codex source tree, product-specific authentication, realtime voice, cloud task APIs, editor implementation, and compatibility surfaces.

### Minimal controlled improvement

**Selected from:** `autoresearch` and `codex-autoresearch`.

**Absorbed mechanism:** One hypothesis produces one isolated change; a fixed evaluator compares it with a baseline; the controller retains or rejects it and records the decision append-only.

**Why it wins:** It is the strongest default because attribution is clear and it provides a matched control for more elaborate search.

**Added from pi-autoresearch:** Backpressure, confidence tracking, idea rotation, anti-thrashing, and explicit finalization are controller hooks, not a separate optimizer.

### Scientific evidence retrieval

**Selected from:** PaperQA.

**Absorbed mechanism:** Parse papers into metadata-linked passages, retrieve and rerank evidence, issue follow-up searches, and preserve exact document locators through answer generation.

**Why it wins:** It has the strongest paper-specific source and citation chain among the reviewed repositories.

**Added from STORM:** Perspective discovery runs before retrieval when breadth is important.

**Added from ChatPaper:** Lightweight summary, translation, and review utilities remain optional triage tools.

### Durable research memory

**Selected from:** AutoSci and EvoScientist.

**Absorbed mechanism:** AutoSci supplies a lifecycle-wide project knowledge graph. EvoScientist supplies immutable observations, supporting/contradicting/superseding relations, asynchronous consolidation, and reviewable skill proposals.

**Why this combination wins:** AutoSci has the broader scientific ontology; EvoScientist has the stronger mechanism for knowledge change.

**Added from DeepScientist:** One inspectable project workspace per research quest.

**Added from DeepCode:** Durable event and execution repositories with evidence-based completion.

### Real experiment execution

**Selected from:** NanoResearch.

**Absorbed mechanism:** Connect literature and planning to code, local or SLURM execution, checkpoints, log parsing, statistical analysis, ablations, figures, and manuscript evidence through resumable stage schemas.

**Why it wins:** It has the most complete artifact flow for actual long-running empirical jobs.

**Added from MLE-agent:** Baseline-first engineering and explicit error-to-debug transitions.

**Added from RD-Agent:** Scenario-specific evaluator interfaces.

### Parallel isolation

**Selected from:** ClawTeam.

**Absorbed mechanism:** A coordinator creates worktree-isolated workers, leases resources, tracks heartbeat and mailbox state, and owns integration.

**Why it wins:** It solves the operational problem—writable-state collision and resource ownership—rather than only assigning personas.

**Initial restriction:** Local process queues and scheduler adapters only. Redis and multi-host transport are deferred.

### Claim promotion and provenance

**Selected from:** `data-to-paper`, Claude Scholar, and ARIS.

**Absorbed mechanism:** Numeric claims point to producing code/output; general claims move from evidence records through a promotion gate; independent reviewers challenge already machine-validated artifacts.

**Why the combination wins:** No one source covers numeric traceability, general claim maturity, deterministic integrity checks, and adversarial review equally well.

### Declarative lifecycle governance

**Selected from:** AutoResearchClaw.

**Absorbed mechanism:** Stage contracts, intervention modes, resumability, cost guardrails, verified registries, and stop-on-gate-failure behavior.

**Important modification:** Its comprehensive 23-stage pipeline becomes one profile, not a mandatory global workflow. Smaller scenarios select only relevant stages.

## Optional components

### Multi-candidate search

**AIDE contribution:** Typed draft, debug, and improvement child transitions for executable ML.

**GEPA contribution:** Evaluator-trace reflection, complementary candidate merge, and Pareto retention.

**AI-Scientist-v2 contribution:** Best-first scientific hypothesis expansion and literature novelty checks.

**Selection rule:** The workflow may activate one of these engines only after declaring a budget and matched linear or best-of-N control.

### Broad and private research

**GPT Researcher contribution:** Broad retriever, scraper, provider, vector-store, and optional reviewer ecosystem.

**local-deep-research contribution:** Local strategy routing, privacy controls, self-hosted model/search integration, and source-bounded research.

**Adaptation:** Both are retriever/provider adapters. Neither owns claims, memory, or workflow state.

### Paper reproduction

**Paper2Code contribution:** Plan–analyze–generate with an explicit implementation specification and reference-free/reference-based evaluation.

**Paper2Agent contribution:** Convert a verified implementation into tested tools and an interactive agent.

**Required order:** Reproduce and evaluate first; operationalize second.

### Domain and engineering skills

**AI-Research-SKILLs contribution:** ML research lifecycle and engineering methods.

**scientific-agent-skills contribution:** Cross-domain scientific procedures.

**Adaptation:** Reuse the package format and selected methods, not the full catalogs. Every imported skill is version-pinned, scanned, tested when executable, and loaded on demand.

## Adapter-only components

### Model-trained research behavior

DeepResearch models may be high-quality agent providers. Continual pretraining and reinforcement-learning infrastructure are outside the platform. External evidence and workflow gates remain authoritative.

### User-facing scientific workspaces

K-Dense contributes ideas for project ownership, provider routing, provenance, notebook bridges, and cost accounting. Its desktop/web/server product is not embedded; future clients may implement those services over the protocol.

### Publication rendering

PaperBanana and Paper2Poster may attach as rendering agents after claims pass provenance gates. Figure generation, PowerPoint assembly, and style toolkits are not core runtime services.

### Coding execution

Codex is a preferred coding-agent provider because of its local execution, sandbox, approval, skill, and session capabilities. It remains behind an adapter; the research controller decides scientific promotion.

## Deferred components

### Agent architecture search

ADAS is valuable but high risk: it generates new executable agent architectures. It is deferred until agent manifests, trust transitions, sandboxing, evaluation suites, and quarantine are implemented. Generated agents can never self-promote.

### Cross-project autonomous publishing

AgentLaboratory's AgentRxiv idea is deferred. Externally shared autonomous artifacts need identity, licensing, contamination, trust, and compatibility policies that are larger than the local runtime.

### Distributed swarm transport

Peer-to-peer and Redis coordination are deferred until local worktrees, processes, and SLURM jobs demonstrate a real scaling bottleneck.

### Full application surfaces

Desktop UI, web dashboard, notebook product, marketplace, billing, subscriptions, and cloud-account management are deferred. The protocol keeps them possible without coupling them to the core.

## Ignored components

### Awesome collections as implementation sources

The four `awesome-*` repositories and other editorial lists are useful discovery inputs but provide no executable mechanism to absorb.

### Mandatory role swarms

Large sets of planner, editor, fact-checker, reviewer, reviser, visualizer, writer, and publisher personas are not copied as permanent agents. A role is introduced only for a distinct capability, tool boundary, context policy, or evaluator.

### Mandatory giant workflow

No task is forced through every literature, experiment, review, and publication stage. Scenario profiles preserve shared safety invariants while selecting the smallest adequate path.

### Self-reported success

An agent's confidence, critique, or completion message is never an authoritative evaluator.

### Silent self-modification

Generated skills, hooks, agents, prompts, and policies cannot install, trust, or activate themselves.

## Resulting component stack

The selected stack is therefore:

```text
Codex-inspired protocol and policy substrate
  + declarative research workflows
  + small versioned agent collection
  + PaperQA-style evidence retrieval
  + AutoSci/EvoScientist memory
  + NanoResearch execution adapters
  + ClawTeam isolation
  + data-to-paper/Claude Scholar/ARIS integrity
  + minimal retain/revert optimization
  + optional tree/Pareto search
```
