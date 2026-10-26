# Scenarios and initial agent collection

## Scenario design rule

Scenarios share one runtime but select different stages. Every scenario still preserves:

- pinned agents and providers;
- typed inputs and outputs;
- artifact hashes;
- evidence-linked claims;
- explicit impact and approval boundaries;
- external evaluation;
- resumability and negative outcomes.

## Initial agents

### research-planner

**Capability:** Frame an objective, identify ambiguity, select a workflow profile, and propose measurable completion criteria.

**Mechanism:** Converts user intent and project state into a typed objective, constraints, risks, evaluator plan, and scenario choice. It cannot alter policy or approve execution.

### perspective-scout

**Capability:** Discover missing viewpoints and questions.

**Mechanism:** Uses STORM-style related-work orientation and simulated expert perspectives to produce a query plan. Its questions are planning artifacts, not claims.

### paper-retriever

**Capability:** Retrieve, parse, rerank, and locate scientific evidence.

**Mechanism:** Uses PaperQA-style document identities, passage indexes, follow-up queries, and reranking. It emits evidence records with exact locators.

### evidence-synthesizer

**Capability:** Produce candidate findings from evidence records.

**Mechanism:** Groups supporting and contradicting passages, distinguishes consensus from uncertainty, and emits structured candidate claims. It cannot promote them.

### hypothesis-designer

**Capability:** Turn gaps into testable hypotheses and falsification criteria.

**Mechanism:** Produces multiple candidate hypotheses, checks literature novelty, identifies measurements and controls, and passes only bounded plans to experiment design.

### experiment-engineer

**Capability:** Implement, launch, monitor, and recover experiments.

**Mechanism:** Builds a baseline first, writes code in an isolated workspace, runs local/container/SLURM jobs, captures logs and checkpoints, and reports execution facts separately from interpretation.

### data-analyst

**Capability:** Test hypotheses using captured data.

**Mechanism:** Executes declared statistical or analytical procedures, records assumptions and uncertainty, and binds every result value to a producing artifact.

### reproduction-engineer

**Capability:** Convert a paper into a tested implementation.

**Mechanism:** Creates an implementation specification before code, resolves equations and interfaces, generates and executes the implementation, then compares it under reference-free and reference-based criteria.

### integrity-reviewer

**Capability:** Audit evidence, logic, contamination, and presentation.

**Mechanism:** Runs deterministic provenance and policy checks first, then independently challenges surviving claims. It can reject or request revision but cannot manufacture replacement evidence.

### evidence-writer

**Capability:** Produce readable reports and manuscripts.

**Mechanism:** Consumes promoted claims and verified artifacts by default, renders limitations and negative results, and records reverse links from visible statements to evidence.

## Literature review workflow

```text
frame objective
  → discover perspectives
  → retrieve papers
  → resolve and rerank evidence
  → synthesize candidate claims
  → contradiction and citation audit
  → promote supported claims
  → write report
```

The workflow stops with `inconclusive` when sources are insufficient. It does not fill gaps from model memory.

## Data analysis workflow

```text
inspect data and provenance
  → define hypotheses and assumptions
  → establish baseline/descriptive analysis
  → execute tests or models
  → robustness and leakage checks
  → bind values to outputs
  → review claims
  → write findings
```

Code execution is R3. Claims that depend on unavailable columns, undocumented cleaning, or unresolved leakage cannot be promoted.

## Controlled code optimization workflow

```text
declare mutable targets and evaluator
  → freeze baseline
  → propose one hypothesis
  → mutate isolated candidate
  → execute fixed metrics and guards
  → retain/reject
  → repeat within budget
  → regression and held-out audit
  → explicit promotion
```

The simple linear loop is always present. Optional AIDE/GEPA search is an experimental arm under the same evaluator budget.

## Paper reproduction workflow

```text
ingest paper and supplemental material
  → extract claims, equations, and interfaces
  → write implementation specification
  → plan environment and tests
  → implement in isolated workspace
  → run examples and benchmark
  → compare with paper and optional reference code
  → record deviations and unsupported details
  → optionally package verified tools
```

Tool packaging follows Paper2Agent only after the reproduction evaluator passes.

## Empirical research workflow

```text
frame objective
  → literature and novelty review
  → hypothesis set
  → experiment design and controls
  → pilot gate
  → full execution
  → analysis, robustness, and ablation
  → claim promotion
  → independent integrity review
  → report or manuscript
```

The pilot gate protects budget and detects broken metrics. Failed promotion gates stop later expensive stages. A negative experimental result still proceeds to analysis and honest reporting when valid.

## Full research workflow

The full profile composes all relevant stages but remains declarative. It is not the default for small tasks.

It may include:

- perspective and literature breadth;
- claim/evidence graph construction;
- multiple hypotheses and optional best-first search;
- baseline, pilot, and full experiments;
- local, container, or SLURM execution;
- robustness, ablation, and contamination audits;
- adversarial review;
- report, manuscript, figure, or poster adapters.

## Workflow branching

Branches are explicit for:

- competing hypotheses;
- alternative implementations;
- debugging after execution failure;
- reviewer-requested revision;
- robustness or ablation arms.

Every branch records a parent stage/attempt and has isolated writable state. Merging combines typed outputs only after compatibility and evaluator checks.

## Agent routing examples

### Private literature review

Route `paper-retriever` to a local model and self-hosted search adapter. Network policy permits only configured literature hosts. The rest of the workflow remains unchanged.

### GPU experiment

Route `experiment-engineer` to Codex or another coding agent, grant a worktree and SLURM adapter, and pause for R3 approval with a declared GPU-hour limit.

### Formal-method experiment

Attach a formal verifier as the authoritative evaluator. Model-generated proof-state predictions remain diagnostic artifacts and cannot replace verifier results.

### Publication figure

After claim promotion, attach a PaperBanana-style figure agent. The integrity reviewer scores semantic fidelity separately from aesthetics and stores editable source or regeneration metadata.

## Negative and inconclusive outcomes

Every workflow can terminate validly with:

- supported positive findings;
- supported negative findings;
- mixed findings;
- inconclusive evidence;
- failed mechanism gate;
- saturated evaluation;
- floor evaluation;
- format or execution failure;
- blocked permissions or budget.

Only infrastructure or protocol failures are runtime errors. Scientific outcomes remain part of the report.
