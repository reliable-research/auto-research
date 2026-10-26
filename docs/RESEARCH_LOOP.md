# One evidence-gated research loop

The central object is one research question with an explicit scope. `ResearchEngine`
is the sole execution and state authority. Builder and reviewer packages propose
artifacts and assessments; they cannot waive deterministic checks or rewrite the ledger.

## Commitments

S2 emits a `problemContract` with nonempty `researchQuestion`, `unit`, `scope`,
`primaryOutcome`, and `comparator` fields. S3–S8 return that same contract unchanged.
A changed question starts a revised run. This prevents a paper from silently solving
a different problem after seeing its results.

S5 emits `protocol`: a JSON object with optional `defaults` and nonempty `runs`.
Each run declares a unique `run_id`, argv `command`, finite positive `timeout_s`,
optional `inputs`, `group`, `label`, and workspace-relative `cwd`. It becomes frozen
when S5 and its review complete. S6 cannot change the argv, cohort, run order, group,
or timeout. Inputs, raw logs, exit status, timestamps, environment, and log digests
are recorded. All artifacts are bound to the native attempt and content-hashed store.

The user-selected `evidenceMode` is pinned in the `workflow/created` event. An
idempotent start cannot switch it. The default is `SIMULATED`: result quantities
remain `[TBD-MEASURE:id]`, and measured metric output is prohibited. In `MEASURED`,
S6 must use a trusted command package, raw logs must match their digests, and reported
summaries must recompute from the records. Missing tools and execution errors are
not negative results. Rates retain both all-run and valid-run denominators.

## Configure the three packages

First install the runtime into the Python environment used by the adapters, then:

```bash
research_project=/tmp/research-loop
ara init "$research_project" --name "Research loop"
cp -R examples/agents/research-builder "$research_project/agents/"
cp -R examples/agents/research-reviewer "$research_project/agents/"
cp -R examples/agents/research-measurement "$research_project/agents/"
```

Configure an existing native model bridge for the builder and reviewer using
`adapter.command` or `ARA_MODEL_BRIDGE`; see [PRODUCT_GUIDE.md](PRODUCT_GUIDE.md).
The bridge reads a native agent request on stdin and returns the native JSON output
envelope. The request contains only the current stage's six cards, selected template,
problem contract, relevant accepted stage records, and recent failure feedback.
Raw logs stay in the artifact store; providers fetch specific evidence when reviewing
it. S8 receives the accepted draft stages rather than reconstructing the method from memory.

The example model manifests use local/offline permissions and a zero monetary budget.
For a networked or paid provider, explicitly configure the package and project permission
and budget limits. Credentials remain the deployment adapter's responsibility; the
runtime does not search for or export private OAuth tokens.

After reviewing/configuring the packages, trust their digests:

```bash
ara --project "$research_project" agents trust research.builder
ara --project "$research_project" agents trust research.reviewer
ara --project "$research_project" agents trust research.measurement
ara --project "$research_project" run start idea-to-paper \
  "Your bounded research question" --evidence-mode SIMULATED \
  --agent-pin research.build_stage=research.builder \
  --agent-pin research.review_stage=research.reviewer \
  --agent-pin research.measure=research.measurement
```

Use `MEASURED` only when the frozen protocol's commands and inputs are available in
`project/workspace`. The supplied S6 package invokes
`python3 -m adapted_research_arch.research.bridge` inside the approved attempt.
It executes the structured S5 protocol, returns raw artifacts, and derives its summary.
The project's existing approval and budget controls still apply.

## Output contracts

A builder returns a `research.stage.v1` record:

```json
{
  "stage": "S2",
  "text": "Problem definition with source locations",
  "problemContract": {
    "researchQuestion": "Does the mechanism change the specified outcome?",
    "unit": "one task",
    "scope": "the declared task family and budget",
    "primaryOutcome": "the registered external outcome",
    "comparator": "the fixed baseline"
  }
}
```

S1 needs `stage` and `text`. S3–S8 copy the accepted problem contract. S5 additionally
supplies the structured protocol. The S6 command bridge supplies `measurementArtifact`
and `measurementSummary`. S8 supplies a paper artifact and `claimIds` matching the
promoted claims it receives. This record sits inside the usual native `records`
object with `status`, `summary`, `artifacts`, `claims`, `observations`, `metrics`, and
`usage`; see [AGENT_PACKAGE_SPEC.md](AGENT_PACKAGE_SPEC.md).

A reviewer returns a `research.review.v1` record naming the semantic stage and the
exact `reviewedAttemptId`. Its `cards` object must contain exactly that stage's six
IDs, each with `status`, `reason`, and `location`; `MET` and justified `N/A` may pass.
Unresolved cards or `BLOCKING` issues fail the stage even when `reviewDecision` says
`pass`. Builder and reviewer must be distinct trusted package IDs. This is role
separation, not a claim that two model outputs are statistically independent.

The full sequence is `s1`, `s1_review`, through `s8`, `s8_review`. The native verifier
checks the same immutable event chain and artifact hashes as other workflows.

## Refinement and boundaries

An evaluation failure preserves the attempt and stops advancement. Fix the provider,
input, or review-record defect before `ara run retry RUN_ID`; the new attempt receives
recent failure messages. An upstream scientific change uses a new run/thread and the
[T4 handoff template](../src/adapted_research_arch/research/assets/T4_ROLLBACK_AND_HANDOFF.md).
Accepted upstream artifacts are not silently mutated or automatically invalidated.
The other [T0–T5 templates](../src/adapted_research_arch/research/assets) remain packaged
reference material; the runtime records stage outputs rather than maintaining a second
set of mutable project-state files.

Text audits are heuristic checks for missing references, numeric assertions, and drift.
They do not prove the truth of arbitrary prose, novelty, statistics, or theory. The
measurement package is a trusted execution boundary; replacing it with a dishonest
command is not solved by JSON validation. New confirmation cohorts require an explicit
new protocol/run. Hosted model quality, citation validity, and scientific performance
are not established by the offline fixture tests.
