# Agent package specification

## Purpose

The agent package is the unit of discovery, trust, routing, versioning, and evaluation in `adapted_research_arch`.

It is larger than a prompt and smaller than a service. It describes how one bounded decision-maker participates in a research stage without owning workflow state.

## Required layout

```text
agents/<agent-name>/
  agent.json          required machine-readable manifest
  AGENT.md            required operating instructions
  skills/             optional local skills
  prompts/            optional task templates
  evals/              optional evaluator definitions and fixtures
  tests/              optional package tests
  assets/             optional non-executable resources
```

Executable scripts must live under a declared skill, tool adapter, or test directory. Merely placing code in an agent package does not grant execution permission.

## Identity

Every package has a stable reverse-domain-style ID, semantic version, human-readable name, and maturity:

- `experimental`: interface may change; implicit routing disabled;
- `candidate`: package passes schema and fixture evaluation;
- `stable`: package passes required evaluator suites and compatibility checks;
- `deprecated`: remains loadable for pinned runs but is not selected for new runs.

The runtime identity is the tuple:

```text
agent ID + version + source root + manifest digest + instruction digest
```

Two packages with the same ID/version but different digests are a supply-chain conflict, not interchangeable versions.

## Capabilities

A capability is a stable verb-noun identifier such as:

- `research.frame_objective`;
- `literature.retrieve_papers`;
- `evidence.synthesize_claims`;
- `experiment.implement`;
- `experiment.execute`;
- `analysis.test_hypothesis`;
- `review.audit_integrity`;
- `publication.write_from_claims`.

Capabilities are routing keys, not permissions. An agent that can implement an experiment still needs a stage and policy grant to write or execute code.

## Typed inputs and outputs

The manifest references schema IDs. A stage may select an agent only when:

- all required input schemas are available from stage dependencies;
- produced schemas satisfy the stage contract;
- schema versions are compatible or an explicit converter exists.

Typical records include:

- `research.objective.v1`;
- `literature.query_plan.v1`;
- `evidence.record_set.v1`;
- `research.hypothesis_set.v1`;
- `experiment.plan.v1`;
- `experiment.result_set.v1`;
- `claim.candidate_set.v1`;
- `claim.promoted_set.v1`;
- `publication.section.v1`.

Prose may accompany a structured output, but it cannot replace a required record.

## Execution adapter

The first version supports three adapter types:

### Command

Launch an executable that reads one JSON request from standard input and returns one JSON result on standard output. Progress events use stderr JSONL or a side channel.

### Model

Invoke a configured model provider with the package instructions and tools. The runtime records provider, model, sampling configuration, context sources, and usage.

### Remote tool protocol

Invoke an MCP or equivalent remote capability. Connection identity, server version, tool schema, and approval annotations are pinned in the attempt.

An agent package may request one primary adapter and several tools. It cannot start undeclared adapters.

## Permission declaration

The package declares the maximum permissions it may request:

- filesystem read roots expressed as project-relative selectors;
- filesystem write selectors;
- network policy such as disabled, source retrieval, or explicit hosts;
- process execution requirement;
- scheduler, GPU, or container requirement;
- secrets by opaque handle name, never raw value;
- external write or publication capability.

The declaration is an upper bound. Effective permission is the intersection of package request, stage policy, project policy, environment capability, and approval grant.

## Risk

The package declares a default risk class from R0 to R5. A workflow may increase risk but cannot lower it below the package/tool requirement.

Implicit routing is permitted only for trusted packages at R0 or R1 unless project policy explicitly allows more.

## Evaluators

An agent may declare evaluator suites for:

- manifest and instruction conformance;
- output schema validity;
- fixture quality;
- citation precision and locator resolution;
- executable success and regression tests;
- safety and permission compliance;
- cost or latency budgets;
- domain-specific scientific validity.

The evaluated package cannot modify its evaluator, fixtures, or frozen evaluation dataset during the run.

## Budgets

Default budgets may cover:

- model tokens;
- wall time;
- tool calls;
- retrieved sources;
- candidate count;
- process CPU/memory;
- GPU time;
- estimated monetary cost.

Workflow and user limits may only reduce these defaults unless a new approval is granted.

## Discovery roots and precedence

Packages are discovered from:

1. built-in distribution roots;
2. user-configured roots;
3. project capability roots.

Precedence does not silently choose between conflicting stable IDs. The registry returns all origins and requires a pin or explicit policy. Existing runs always use the pinned origin and digests.

## Trust mechanism

Discovery performs only read-only parsing. To become trusted, a package must pass:

1. manifest schema validation;
2. path containment and symlink checks;
3. instruction/resource digest calculation;
4. static scan of declared executable content;
5. required package tests and fixture evaluators;
6. human or managed trust approval.

If any trusted file changes, the package moves to `changed` before another attempt can start.

## Routing

The router filters candidates by hard constraints first:

```text
capability
→ input/output compatibility
→ trust and maturity
→ environment availability
→ permission compatibility
→ budget feasibility
```

It then ranks remaining candidates by explicit project preference, scenario fit, and measured evaluator history. Model-generated preference may break a tie only when the choice is recorded and no frozen policy decides it.

## Invocation context

The agent receives a bounded request containing:

- project and run identifiers;
- stage and attempt identifiers;
- objective and stage instructions;
- typed dependency outputs;
- selected reviewed-memory excerpts with provenance;
- workspace and allowed roots;
- effective tool and permission descriptions;
- remaining budget;
- required output schemas and evaluators;
- explicit stop and escalation conditions.

It does not receive evaluation-only data, unrelated project memory, raw secrets, or unapproved capabilities.

## Output contract

The result contains:

- status: `completed`, `blocked`, `failed`, or `inconclusive`;
- produced typed records;
- artifact declarations;
- candidate claims and evidence references;
- observations proposed for memory;
- unresolved questions and limitations;
- usage and adapter metadata;
- optional request for a follow-up attempt or additional permission.

The runtime verifies all declared files and records. A `completed` status is only the agent's terminal state; the stage still proceeds to evaluation and promotion gates.

Artifact names must be safe relative names. `request.json`, `stdout.json`, `stderr.txt`, and `failure.txt` are reserved for runtime-owned attempt records.

## Hooks

Packages may declare lifecycle hooks only through trusted configuration. Supported early events are:

- `before_attempt`;
- `after_attempt`;
- `before_tool`;
- `after_tool`;
- `after_evaluation`.

Synchronous hooks may add validated context or deny an action. Asynchronous hooks may emit observations but cannot alter the active decision. Hook definitions are hash-trusted independently from the agent.

## Generated and optimized agents

An optimization workflow may produce a new package candidate. The output:

- receives a new version or experimental build identity;
- is stored under a candidate root;
- is marked `discovered` or `quarantined`;
- is evaluated against frozen fixtures and held-out tasks;
- cannot write to trusted roots;
- cannot approve or activate itself.

Promotion is a separate R5 action.

## Compatibility policy

The manifest format uses a major schema version. Unknown required fields or capabilities fail closed. Unknown optional metadata is preserved but ignored.

Stable agents support the current and previous minor protocol versions. Runs pin the resolved manifest representation so a later registry upgrade cannot reinterpret historical state.
