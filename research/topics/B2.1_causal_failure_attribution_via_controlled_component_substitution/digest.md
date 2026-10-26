# Digest: Causal Failure Attribution via Controlled Component Substitution in Tool-Use Agents

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING, GROUNDED IN A REAL CORPUS.** No paper
> exists yet for this idea. This document projects an N0–N12 digest forward from a
> one-paragraph seed (topic code B2.1, label `[证据]`, parent topic "B2. 失败归因（plan /
> tool / execution）"). Every field is tagged inline:
> - **[GIVEN]** — verbatim/near-verbatim from the seed README (ground truth; never contradicted).
> - **[HYPOTHESIS]** — reasoned elaboration/prediction, grounded in the seed + real prior work
>   surfaced from the local corpus. Not a fact.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is done (authors, DOI, numbers,
>   artifacts). Never invented.
> - **[GROUNDED:corpus]** — the item is anchored to a real paper found in
>   `topics/corpus/ideas.jsonl` (OpenReview), cited with its real `paper_id` and URL.
>
> Do not read any [HYPOTHESIS] or [PLACEHOLDER] content below as a real finding.

---

## N0 Metadata

- **Title:** "Causal Failure Attribution via Controlled Component Substitution in Tool-Use Agents" **[GIVEN]** (seed title, verbatim)
- **Authors:** ["Anonymous"] **[PLACEHOLDER]** — paper does not exist; no authors to extract.
- **Abstract [HYPOTHESIS, drafted — NOT a real abstract]:**
  > "Tool-use LLM agents fail along long trajectories that interleave a plan, an executor, and
  > a set of tools/observations, but evaluation typically reports only aggregate task
  > success/failure and, when it does attribute blame, validates that blame against
  > human-annotated or single-culprit labels rather than a known causal ground truth. We ask:
  > when the executor is held fixed and the plan is substituted (or the plan is held fixed and
  > the tool is substituted), does the failure move with the substituted component — and can an
  > attribution method's blame assignment be *mechanically verified* against that substitution?
  > We construct a benchmark of tool-use agent trajectories with *injected, known faults*
  > (corrupted plan steps, broken tools, polluted observations), each carrying a mechanically
  > verifiable ground-truth failure-locus label produced by controlled component substitution.
  > We use this labeled corpus to measure the component-attribution accuracy of candidate
  > methods (LLM-judge post-hoc explanation, ablation/leave-one-out, intervention-based
  > do-then-verify) against ground truth, and argue the labeled fault corpus itself — a
  > 'Defects4J for agents' — is a primary contribution alongside the substitution protocol."
- **DOI:** null **[PLACEHOLDER]**
- **arXiv ID:** null **[PLACEHOLDER]**
- **Num pages:** null **[PLACEHOLDER]**
- **Research area:** "AI/ML" **[HYPOTHESIS]** — straddles AI/ML (LLM tool-use agents) and SE
  (fault-injection/benchmark methodology); classified AI/ML because the object of study is
  agent-pipeline behavior, not code-level software artifacts. All directly comparable prior
  work found in the corpus is filed under `domain=ml`.

**Status:** PARTIAL. **Absence comment:** `what_missing`: "No real title page exists — authors,
abstract, DOI, arXiv id, and page count are all unwritten because this is a pre-paper research
idea, not a digested document." `why_matters`: "Any downstream tool (se-paper-reviewer,
pengsida-paper-writer) that expects real bibliographic identity will be working from a
placeholder, not a citable source." `implication`: "Treat N0 purely as a working title/abstract
draft for planning purposes; re-run this digest for real once a paper is written."

---

## N1 Problem Formulation

- **Objective [HYPOTHESIS]:** "Diagnose which tool-use-agent pipeline component — the plan, the
  executor/tool, or the observation channel — is causally responsible for an observed task
  failure, by mechanically substituting one component at a time while holding the remaining
  components fixed at a known-good version, and validating any candidate attribution method's
  blame assignment against injected-fault ground-truth labels."
  - Kind of task: causal diagnosis / attribution-accuracy measurement + labeled-benchmark construction.
  - Domain: tool-use LLM agents (plan → executor → tool/observation pipelines).
  - Outcome shape: a released labeled fault-trajectory benchmark ("Defects4J for agents") plus a
    mechanically-verified accuracy report on failure-attribution methods.
- **Inputs [HYPOTHESIS]:**
  - A tool-use agent trajectory (plan, executor, tool set, observation trace) exhibiting a task failure.
  - A library of injectable faults with known ground-truth component labels (bad plan step,
    broken/replaced tool, polluted observation).
  - A candidate attribution method's blame assignment for a given failing trajectory.
- **Outputs [HYPOTHESIS]:**
  - A per-trajectory ground-truth failure-locus label (which single component was substituted/faulted).
  - A component-attribution-accuracy score per candidate method, overall and per fault category.
  - A released, labeled fault-trajectory benchmark.
- **Constraints [GIVEN]:** "Ground truth is obtained only by injecting a known fault (a bad
  plan step, a broken tool, or a polluted/contaminated observation) — this is what makes
  attribution accuracy measurable; the core question requires checking whether failure follows
  the specific component that was substituted (executor fixed / plan swapped, or plan fixed /
  tool swapped), i.e. attribution conclusions must be mechanically verifiable by re-running the
  substitution experiment." (paraphrased directly from the seed's 核心问题 and 最小实验)

**Status:** PARTIAL (as an inferred formulation) — **Source:** inferred/[HYPOTHESIS] for
inputs/outputs/objective, [GIVEN] for constraints. **Absence comment:** `what_missing`: "The
objective, inputs, and outputs are not quoted from a written Problem Formulation section — no such
section exists yet — they are reasoned elaborations of the seed's one-paragraph core question and
minimal experiment." `why_matters`: "A reader could mistake the precise-sounding
inputs/outputs/objective language for an author's own formalization rather than this digest's
extrapolation; only the `constraints` bullet is seed-verbatim." `implication`: "Re-verify N1
against a real Problem Formulation / Step-5 formalization once one is written; until then, treat
objective/inputs/outputs as a working formulation to be checked, not a citable fact — consistent
with `paper.md` Step 5's independently-derived formal notation, which N1 should be reconciled
against on the next full digest pass."

---

## N2 Motivation

**[HYPOTHESIS]** reconstructed from the parent-topic framing and grounded against the motivation
text of real corpus papers — no invented statistics, no numeric claims.

- Tool-use LLM agent pipelines routinely fail, but evaluation typically reports only aggregate
  task success/failure, not *which stage* (planning, tool selection/execution, or observation
  ingestion) is responsible; this is exactly the "coarse outcome-based metrics" gap that
  motivates process-level agent evaluation work such as `[AutoLibra, OpenReview:4BjGVZ7Bxn]`
  and the trajectory-level failure taxonomy in `[Terminal-Bench, OpenReview:a7Qa4CcHak]`.
  Without stage-level attribution, a practitioner cannot tell whether to invest in a better
  planner, a more robust executor/tool interface, or better observation handling. **[HYPOTHESIS]**
- A growing set of "failure attribution" methods for multi-agent/tool-use systems has been
  proposed (`[WhoAndWhen, OpenReview:GazlTYxZss]`, `[AgenTracer, OpenReview:l05DseqvuD]`), but
  their attributed cause is validated against *human-annotated* or *single-culprit* labels
  rather than a controlled causal ground truth — and `[DoVer, OpenReview:mrEK16Jy6h]` argues
  the single-culprit assumption is structurally weak, so a method can produce plausible but
  causally wrong blame. This is the gap the seed targets: attribution claims are rarely checked
  against a *known* injected cause. **[HYPOTHESIS]**
- Establishing whether "failure follows the substituted component" is even a valid premise is
  itself foundational: if swapping a good plan for a bad one (executor held fixed) does not
  reliably shift failure onto the plan, all blame-assignment research downstream of that
  assumption rests on shaky ground. Intervention-based debugging (`[DoVer,
  OpenReview:mrEK16Jy6h]`) and counterfactual label generation (`[AgenTracer,
  OpenReview:l05DseqvuD]`) already assume a version of this premise without measuring its
  reliability across a plan/tool/observation taxonomy. **[HYPOTHESIS]**

**Status:** PARTIAL. **Absence comment:** `what_missing`: "No written Introduction/Motivation
section exists to quote verbatim." `why_matters`: "Motivation claims here are reconstructed from
a topic-index entry plus the motivation text of real corpus papers, not argued in prose by
authors of this (non-existent) paper." `implication`: "Treat these bullets as plausible framing
to be validated/rewritten once an actual paper draft exists."

---

## N3 Related Works

**Corpus search performed** over `topics/corpus/ideas.jsonl` (11,683 OpenReview papers). Queries
run (semicolon-separated terms, title hits weighted 3×): (1) "failure attribution; multi-agent
system; blame assignment; who is responsible"; (2) "intervention; auto debugging; counterfactual;
causal; LLM agent"; (3) "agent benchmark; error localization; fault injection; trajectory; tool
use agent evaluation"; (4) "LLM agent failure; error analysis; debugging agent trajectories;
step-level"; (5) "LLM judge; evaluator reliability; critique; verify reasoning steps". Full
motivation+method text of the top hits was read directly. Entries below tagged
**[GROUNDED:corpus]** are real papers with real `paper_id`s; the single non-corpus entry is a
canonical SE benchmark the seed itself names, flagged explicitly.

- **[WhoAndWhen, OpenReview:GazlTYxZss]** **[GROUNDED:corpus]** — "Which Agent Causes Task
  Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems." Formalizes
  failure attribution as identifying *decisive errors* (agent–time pairs whose correction flips
  a failed trajectory to success), releases the **Who&When** dataset of failure logs with human
  annotations of the responsible agent and decisive step, and frames attribution as an
  LLM-as-a-Judge task with all-at-once / step-by-step / binary-search context strategies.
  url: https://openreview.net/forum?id=GazlTYxZss
- **[DoVer, OpenReview:mrEK16Jy6h]** **[GROUNDED:corpus]** — "DoVer: Intervention-Driven Auto
  Debugging for LLM Multi-Agent Systems." Treats failure attribution as a *testable causal
  hypothesis*: segment a session into planning-execution trials, generate a suspected
  agent/step hypothesis, synthesize a targeted edit at the orchestrator message layer, and
  replay from that point (rewind-edit-reexecute) to check whether the outcome changes; scores
  interventions as validated / partially validated / refuted / inconclusive by counterfactual
  outcome change and milestone progress. url: https://openreview.net/forum?id=mrEK16Jy6h
- **[AgenTracer, OpenReview:l05DseqvuD]** **[GROUNDED:corpus]** — "AgenTracer: Who Is Inducing
  Failure in the LLM Agentic Systems?" Generates high-fidelity attribution supervision by (a)
  counterfactual decisive-error discovery (replay with minimally-corrected steps) and (b)
  **programmatic fault injection from successful traces** — perturb an action, replay, and if the
  run now fails the injected step is the decisive error *by construction* — then trains a
  dedicated RL tracer with a multi-granular reward for agent and step attribution.
  url: https://openreview.net/forum?id=l05DseqvuD
- **[SelfEvolveBench, OpenReview:2H03gm4Rq6]** **[GROUNDED:corpus]** — "Towards Self-Evolving
  Agent Benchmarks: Validatable Agent Trajectory via Test-Time Exploration." Builds agent
  benchmarks from executable trajectories rather than textual mutation, and validates every task
  by *reproducibility* — replaying the recorded trajectory to confirm each action yields the same
  observation sequence before the task is accepted. url: https://openreview.net/forum?id=2H03gm4Rq6
- **[Terminal-Bench, OpenReview:a7Qa4CcHak]** **[GROUNDED:corpus]** — "Terminal-Bench:
  Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces." A containerized
  agent benchmark graded by final-state outcome tests, with a multi-stage audit/integrity
  pipeline (solvability validation, exploit-oriented inspection) and a trajectory-level failure
  taxonomy of *execution, coherence, and verification* errors adapted from MAST-style failure
  analysis. url: https://openreview.net/forum?id=a7Qa4CcHak
- **[AutoLibra, OpenReview:4BjGVZ7Bxn]** **[GROUNDED:corpus]** — "AutoLibra: Agent Metric
  Induction from Open-Ended Human Feedback." Argues coarse outcome metrics (task success/failure)
  fail to capture the intermediate decisions that cause success or failure; induces interpretable
  behavioral metrics from feedback grounded to specific trajectory segments and applies them via
  LLM-as-a-Judge. url: https://openreview.net/forum?id=4BjGVZ7Bxn
- **[CRM, OpenReview:4DJoBOQNd0]** **[GROUNDED:corpus]** — "Linking Process to Outcome:
  Conditional Reward Modeling for LLM Reasoning." Models a reasoning trajectory as a survival
  process to assign each step a reward reflecting its causal contribution to the final outcome,
  explicitly targeting the credit-assignment ambiguity that arises when step-level judgments are
  made independently of the full preceding trajectory. url: https://openreview.net/forum?id=4DJoBOQNd0
- **[FAPO, OpenReview:jhqqoimoWt]** **[GROUNDED:corpus]** — "Flawed-Aware Policy Optimization."
  Trains a generative reward model to detect "flawed-positive" rollouts (correct final answer,
  invalid intermediate reasoning) and to *predict the earliest erroneous step*, with a step-wise
  reward proportional to the distance from the gold error step — a concrete error-localization
  method that could be repurposed as an attribution baseline.
  url: https://openreview.net/forum?id=jhqqoimoWt
- **[Defects4J, Just et al. 2014]** **[NON-CORPUS — canonical SE benchmark, named by the seed]** —
  A database of real, isolated, reproducible Java bugs (each a buggy/fixed version pair with a
  triggering test), widely used as ground truth for fault-localization and program-repair
  evaluation. The seed explicitly frames its target artifact as "a Defects4J for agents." Cited
  from prior knowledge as canonical; verify the exact reference (ISSTA 2014) at write time.

**Status:** FOUND. **Absence comment:** null — 8 corpus entries plus 1 clearly-flagged canonical
non-corpus entry, all with an approach summary grounded in the paper's own motivation/method text.

---

## N4 Prior Limitations

**[HYPOTHESIS]** — inferred gaps between real N3 works and the seed's core question. Each cites the
exact N3 `citation_key` string it affects. `source` would be `extracted` in a real paper; here it
is inferred (no paper exists), so treat as a defensible reading of what the cited work
demonstrably does **not** cover.

- "Automated attribution methods validate blame against *human-annotated* or *single-culprit*
  labels, not against a known injected cause: Who&When's labels are manual and small-scale, and
  its LLM-judge is scored by agreement with those annotations rather than by whether the blamed
  component is *causally* responsible; DoVer itself argues the single-decisive-culprit assumption
  is structurally weak. Neither provides a labeled corpus whose ground truth is fixed *by
  construction* across a plan/tool/observation component taxonomy."
  **affects_works:** ["[WhoAndWhen, OpenReview:GazlTYxZss]", "[DoVer, OpenReview:mrEK16Jy6h]"]
  **limitation_type:** other (unvalidated attribution ground truth) **[HYPOTHESIS]**
- "AgenTracer already injects faults into successful traces to create decisive-step labels by
  construction — the closest real precedent — but its injection is aimed at *training a tracer*
  and targets a single perturbed action to produce a step label; it does not systematically
  vary faults across a taxonomy of plan-corruption / tool-breakage / observation-pollution
  component classes, nor does it measure whether failure *follows the substituted component*
  under a controlled hold-two-swap-one protocol, so it cannot report per-component-class
  attribution accuracy as a headline measurement."
  **affects_works:** ["[AgenTracer, OpenReview:l05DseqvuD]"]
  **limitation_type:** generalizability **[HYPOTHESIS]**
- "Agent-benchmark construction work validates task *solvability/reproducibility* (SelfEvolveBench
  replays trajectories to confirm reproducibility; Terminal-Bench grades final container state
  and tags failures as execution/coherence/verification) but its labels are outcome-based or
  coarse failure-*type* tags without a ground-truth causal *locus* fixed by injection — so these
  benchmarks give a common evaluation surface but not a labeled fault corpus against which
  attribution accuracy can be mechanically scored."
  **affects_works:** ["[SelfEvolveBench, OpenReview:2H03gm4Rq6]", "[Terminal-Bench, OpenReview:a7Qa4CcHak]"]
  **limitation_type:** other (no ground-truth causal locus) **[HYPOTHESIS]**
- "Step-level credit/error-localization methods for reasoning (AutoLibra's induced-metric
  LLM-judge, CRM's survival-based per-step credit, FAPO's earliest-erroneous-step predictor) can
  localize *a step*, but they assign credit via learned reward models or judges whose localization
  correctness is itself never validated against an injected known fault, and they operate on
  single-model reasoning steps rather than a multi-component agent pipeline where the fault may
  be a broken tool or a polluted observation rather than a bad token-level step."
  **affects_works:** ["[AutoLibra, OpenReview:4BjGVZ7Bxn]", "[CRM, OpenReview:4DJoBOQNd0]", "[FAPO, OpenReview:jhqqoimoWt]"]
  **limitation_type:** precision **[HYPOTHESIS]**
- "Defects4J supplies real-bug ground truth for fault localization, but only for single Java
  programs where the fault is a code statement recoverable by a triggering test; there is no
  analog whose 'fault' can be a semantic error in a natural-language plan step, a broken tool
  interface, or a polluted observation in a multi-step agent trajectory."
  **affects_works:** ["[Defects4J, Just et al. 2014]"]
  **limitation_type:** generalizability **[HYPOTHESIS]**

**grounding_check:** true — every limitation cites at least one N3 `citation_key` in the exact
N3 string form.

**Status:** PARTIAL (limitations are inferred, not author-claimed, since no paper exists).
**Absence comment:** `what_missing`: "These are not limitations the (non-existent) authors state;
they are inferred gaps between real found works and the seed's core question." `why_matters`: "A
reviewer should not treat these as citations of an actual related-work critique." `implication`:
"Re-derive N4 from a real related-work section once this paper is written; the corpus grounding
here (WhoAndWhen/DoVer/AgenTracer are directly on-target) makes these gaps far more defensible
than a generic SE-fault-localization analogy."

---

## N5 Challenges

**[HYPOTHESIS, tightly derived]** — problem-inherent obstacles implied by the core question, each
about the problem itself (not a named tool's weakness), passing the N4-vs-N5 test. Stable C-ids
retained from the prior digest.

- **C1:** Pipeline components in a tool-use agent are causally entangled — the plan conditions
  what the executor attempts, which conditions which tools are called and what observations come
  back — so a "which component looks anomalous" heuristic confuses correlation with the true
  causal locus of failure. **[HYPOTHESIS]**
- **C2:** Substituting one component while claiming to hold the others "fixed" can itself perturb
  downstream behavior (a new plan changes the instructions the executor receives even though the
  executor model is unchanged; agent stochasticity can flip an outcome independent of the swap),
  so the substitution protocol itself risks becoming a confound in measuring "does failure follow
  the substituted component." **[HYPOTHESIS]**
- **C3:** Building a fault library that spans plan/tool/observation categories with unambiguous
  ground-truth origin, at a scale sufficient to statistically evaluate attribution methods,
  requires injectable faults that are realistic enough to matter yet unambiguous enough to label —
  and injecting a fault does not guarantee the run actually fails *for that reason*. **[HYPOTHESIS]**
- **C4:** The observable failure symptom (final task failure) can be temporally and causally
  distant from an injected fault in a long, multi-step trajectory, so an attribution method must
  trace backward through many intermediate steps rather than compare a single input/output pair —
  and cascading effects can make a downstream component *appear* faulty. **[HYPOTHESIS]**

**conflation_check:** true — C1 (entanglement), C2 (substitution-as-confound + stochasticity), C3
(benchmark construction + inject≠cause), C4 (long-horizon causal distance) are distinct.

**Status:** PARTIAL. **Absence comment:** `what_missing`: "No paper text states these challenges;
they are derived from the seed's core question and the difficulties real corpus papers
(DoVer/AgenTracer) explicitly report — e.g. DoVer's 'structural ambiguity' and stochasticity
handling map onto C1/C2, AgenTracer's 'inject≠fail' concern onto C3." `why_matters`: "Weigh these
as predicted obstacles, not author-acknowledged difficulties." `implication`: "Use as the design
checklist for the eventual methodology section."

---

## N6 Methodology

**Overview [HYPOTHESIS]:** A fault-injection-based causal-attribution benchmark and protocol.
Construct a corpus of tool-use agent tasks; inject exactly one of three fault classes (corrupted
plan step, broken/replaced tool, polluted observation) at a time while holding the other two
pipeline components fixed at their known-good version; run the agent to obtain a failing
trajectory carrying a ground-truth component-level label; run each candidate attribution method
on the trajectory and score whether its blamed component matches the injected ground-truth label
— i.e. mechanical verification of attribution claims. The design borrows AgenTracer's "inject
into a successful trace → replay → label by construction" trick (`[AgenTracer,
OpenReview:l05DseqvuD]`) and DoVer's checkpointed rewind-edit-replay with multiple replays for
stochasticity (`[DoVer, OpenReview:mrEK16Jy6h]`), and validates every base task for
reproducibility before injection in the spirit of `[SelfEvolveBench, OpenReview:2H03gm4Rq6]`.

**Staged plan [HYPOTHESIS]:**
- **Stage 0 — Base-task reproducibility gate.** Take tasks from an existing agent benchmark
  (GAIA-style), run a fixed agent scaffold (e.g. MetaGPT / a plan-executor-tool loop), keep only
  tasks that (a) the agent solves and (b) replay reproducibly (SelfEvolveBench-style), to serve
  as known-good baselines for substitution.
- **Stage 1 — Pilot (the seed's minimal experiment).** On a small task set, inject each of the
  three fault classes and run the two substitution conditions from the seed (executor fixed / plan
  swapped; plan fixed / tool swapped). Confirm the premise (RQ1) and score a first attribution
  baseline (RQ_INF_1). Target O(hundreds) of labeled trajectories.
- **Stage 2 — Scale-up.** Expand across multiple task domains, agent frameworks, and LLM
  backbones; add the observation-pollution class at scale; release the labeled corpus and run the
  full baseline suite with statistical testing. Target O(thousands) of labeled trajectories.

**Key components:**
- **M1 — Fault Injection Library [HYPOTHESIS]:** Parameterized fault generators for three
  categories — *plan corruption* (delete/reorder/replace a plan step, inject an infeasible
  sub-goal), *tool breakage* (replace a tool with a stub returning error/empty/malformed output,
  or swap in a wrong-signature tool), *observation pollution* (inject noise/contradictory
  content/truncation into a returned observation). Each generator emits `(trajectory,
  injected_component, injected_step_index, fault_template_id)`. Granularity: per-step, single
  component per trajectory.
- **M2 — Controlled Substitution Harness [HYPOTHESIS]:** Checkpoints the known-good run, holds two
  of {plan, executor/tool, observation} fixed at their recorded good state, swaps in the faulty
  version of the third, and replays from the injection point forward (rewind-edit-reexecute).
  Runs *k* replays per trial (k≈3–5) to average over agent stochasticity. Instrument: an
  orchestrator-message-level edit layer (as in DoVer) so swaps preserve architectural generality.
- **M3 — Ground-Truth Labeling Protocol [HYPOTHESIS]:** Records the injected component as the gold
  failure-locus label, *conditioned on the run actually flipping from success to failure* (inject
  → replay → keep only if outcome flips, à la AgenTracer). This makes "inject ≠ cause" (C3)
  observable: an injected fault that does not flip the outcome is discarded, not mislabeled.
- **M4 — Attribution Method Suite [HYPOTHESIS]:** Candidate techniques applied uniformly to each
  labeled trajectory, mapped to real baselines: (a) LLM-judge post-hoc explanation with WhoAndWhen
  context strategies (all-at-once / step-by-step / binary-search); (b) ablation/leave-one-out
  blame (re-run with each component reset to good, observe which restores success); (c)
  intervention-based do-then-verify (DoVer-style hypothesis + counterfactual replay); (d) a
  step-level localizer repurposed from FAPO/CRM; (e) random/majority-class control.
- **M5 — Mechanical Verification Scorer [HYPOTHESIS]:** Computes component-attribution accuracy
  (predicted locus vs. ground-truth locus), a confusion matrix over {plan, tool, observation}, and
  per-fault-category accuracy; supports both single-component and multi-component blame (precision/
  recall) scoring.

**Challenge arguments:**
- C1 ← [M2]: "By perturbing exactly one of {plan, executor/tool, observation} per trial while
  holding the other two at their known-good state and replaying from the checkpoint, the harness
  isolates a single causal source, addressing the entanglement problem directly." **[HYPOTHESIS]**
- C2 ← [M2, M3]: "Running k replays per trial averages over agent stochasticity, and the
  outcome-flip condition (M3) anchors the ground-truth label to an observed causal effect rather
  than to the mere act of substitution, guarding against the substitution itself becoming an
  unaccounted confound." **[HYPOTHESIS]**
- C3 ← [M1, M3]: "A parameterized generator across three fault categories plus an
  inject→replay→keep-only-if-outcome-flips labeling protocol yields a benchmark whose labels are
  causally grounded by construction and whose scale is bounded only by compute, not by manual
  annotation." **[HYPOTHESIS]**
- C4 ← [M4, M5]: "Requiring each attribution method (M4) to process the full trajectory and
  scoring its blamed locus against the ground truth (M5) at least *measures* how methods handle
  long-horizon causal distance, exposing cascade-induced misattribution as low per-category
  accuracy." **[HYPOTHESIS]**

**Unaddressed challenges:** ["C4"] **[HYPOTHESIS]** — the harness *measures* whether methods handle
long-horizon causal distance (M4/M5) but does not itself *solve* it; a method that fails on
temporally distant faults simply scores low, which is a measurement outcome, not a challenge
resolved by the method design.

**Feasibility [HYPOTHESIS]:**
- **Order-of-magnitude effort.** Fault library ≈ 3 categories × ~5 fault templates × ~200 base
  tasks ≈ O(3,000) candidate labeled trajectories; with k≈4 replays per substitution trial plus
  base runs, ≈ O(10,000–30,000) agent runs total. On GAIA-style tasks with a GPT-4-class API
  backbone (~10–50 tool steps/run), per-run cost ≈ $0.10–0.50 → total API cost in the **low
  thousands of USD** (single-digit-$k), i.e. a small-lab budget. Human effort is minimal because
  ground truth is by construction; budget ≈ **15–25 annotator-hours** for a validation audit of a
  ~200-trajectory sample (do injected labels match a human's read of the failure cause?).
- **Biggest feasibility risk + mitigation.** The dominant risk is **C2 (substitution-as-confound
  + stochasticity)**: a swapped component may fail to reproduce the intended clean baseline, or
  agent stochasticity may flip outcomes independent of the swap, corrupting labels. Mitigation:
  fixed seeds / temperature-0 where possible, k-replay majority outcome, orchestrator-message-level
  edits (DoVer) rather than deep state edits, and the M3 outcome-flip filter that discards trials
  whose outcome does not move with the injected component.

**Status:** PARTIAL (hypothesized, but grounded in real methods). **Absence comment:**
`what_missing`: "No actual method section exists; M1–M5 are an extrapolation from a one-sentence
minimal experiment, with instruments borrowed from DoVer/AgenTracer/SelfEvolveBench."
`why_matters`: "Component names and the challenge-mapping are design guesses, not the eventual
authors' architecture." `implication`: "Use as a first-draft method skeleton grounded in the
closest real prior art, to be replaced once real design decisions are made."

---

## N7 Contributions

- **CO1** [dataset, is_testable=true, has_rq=true]: "A labeled fault-injection benchmark of
  tool-use agent trajectories with ground-truth plan/tool/observation failure-locus labels — a
  'Defects4J for agents' — whose labels are causally grounded by construction (inject → replay →
  keep only on outcome flip)." **[HYPOTHESIS]**
- **CO2** [conceptual_framework, is_testable=true, has_rq=true]: "A controlled
  component-substitution protocol (fix two pipeline components, swap the third, replay from
  checkpoint with k replays) for *mechanically validating* any failure-attribution method's
  accuracy against ground truth, rather than trusting unvalidated post-hoc explanations or
  human-agreement scores." **[HYPOTHESIS]**
- **CO3** [empirical_finding, is_testable=true, has_rq=true]: "An empirical measurement of how
  accurately existing/candidate attribution methods (LLM-judge, ablation, intervention-based,
  step-localizer) identify the true faulty component when that component is known by
  construction, reported per fault category." **[HYPOTHESIS]**

**Status:** PARTIAL (inferred from the minimal experiment, none author-asserted). **Absence
comment:** `what_missing`: "No contributions paragraph exists to quote." `why_matters`: "These
project what such a paper would claim, not a verified list." `implication`: "Revisit once an
intro contributions list is written."

---

## N8 Research Questions

- **RQ1 [GIVEN, near-verbatim restatement of the seed's 核心问题]:** "With the executor held
  fixed and the plan substituted, or with the plan held fixed and the tool substituted, does the
  observed failure track (move with) the substituted component?"
  - **rq_source:** explicit (given) | **evaluates_mechanisms:** ["M2", "M3"] |
    **addresses_challenges:** ["C1", "C2"] | **tests_contributions:** ["CO2"] |
    **answered_by_experiment:** "Run the substitution harness (M2) across the fault library (M1)
    with the M3 outcome-flip protocol; test whether the outcome-flip rate on trials where a given
    component was substituted exceeds the rate on control (no-op) substitutions."
- **RQ_INF_1 [HYPOTHESIS, inferred from the seed's 最小实验 — "归因结论可否被替换实验机械验证"]:**
  "Can existing/candidate failure-attribution methods be mechanically verified against injected
  ground-truth fault labels, and how accurate are they per fault category?"
  - **rq_source:** inferred | **evaluates_mechanisms:** ["M4", "M5"] | **addresses_challenges:**
    ["C3", "C4"] | **tests_contributions:** ["CO1", "CO3"] | **answered_by_experiment:** "Apply
    each M4 method to every labeled trajectory; compute component-attribution accuracy and the
    {plan,tool,observation} confusion matrix (M5) against ground truth."

**Datasets [HYPOTHESIS]:** {names: ["GAIA (base tool-use tasks for trajectory generation)",
"Who&When dataset (`[WhoAndWhen, OpenReview:GazlTYxZss]`) as a naturally-failing comparison set
with human labels", "The constructed injected-fault corpus (this work, CO1 — plan/tool/observation
labels)"]} — GAIA and Who&When are real, named, and genuinely fit (GAIA supplies realistic
tool-use tasks; Who&When supplies human-annotated failure logs to contrast construction-based
labels against).
**Baselines [HYPOTHESIS]:** {names: ["WhoAndWhen LLM-judge attribution (all-at-once / step-by-step
/ binary-search) `[WhoAndWhen, OpenReview:GazlTYxZss]`", "AgenTracer RL tracer `[AgenTracer,
OpenReview:l05DseqvuD]`", "DoVer intervention-based do-then-verify `[DoVer, OpenReview:mrEK16Jy6h]`",
"FAPO/CRM step-level error localizer `[FAPO, OpenReview:jhqqoimoWt]` / `[CRM, OpenReview:4DJoBOQNd0]`",
"Ablation/leave-one-out blame", "Random/majority-class control"]}
**Metrics [HYPOTHESIS]:** {names: ["Top-1 component-attribution accuracy = fraction of trajectories
whose blamed component equals the injected component", "Per-fault-category accuracy (plan vs. tool
vs. observation) with a 3×3 confusion matrix", "Precision/recall when multi-component blame is
allowed", "Outcome-flip rate (for RQ1): P(failure | component X substituted) vs. control"]}

**Analysis plan [HYPOTHESIS]:** Stage-1 pilot n ≈ 300 labeled trajectories (~100/fault class);
Stage-2 scale-up n ≈ 3,000. All inference is cluster-robust at the base-task level (trials
sharing a base task form one cluster — n ≈ 3,000 trials come from ~200 base tasks, so the
effective sample size is the cluster count; see paper.md's power statement). RQ1: two-proportion
comparison with cluster-robust variance (or a base-task cluster bootstrap) of the outcome-flip
rate under each substitution vs. the *class-matched* no-op control, significance α = 0.05,
expected direction = flip rate substantially above control for all three classes (premise holds).
RQ_INF_1: McNemar-style test on paired correct/incorrect attributions between each method and the
random/majority control, cluster-robust at the base-task level, α = 0.05 with Benjamini-Hochberg
correction across the method × fault-category grid; expected direction = every real method >
control, but with a **meaningful gap below the 100% ground-truth ceiling**, largest confusion
between plan-level and execution-level blame. Report 95% cluster-bootstrap CIs on all accuracies.

**Status:** PARTIAL. **Absence comment:** `what_missing`: "RQ1 restates the seed core question
(given); RQ_INF_1, datasets, baselines, metrics, and the analysis plan are inferred from a
one-sentence minimal experiment, though the named datasets/baselines are all real and on-target."
`why_matters`: "The specific baselines are illustrative-but-defensible, not binding."
`implication`: "Treat as an evaluation-design sketch to refine once experiment code exists."

---

## N9 Results — PLACEHOLDER, HYPOTHESIZED DIRECTION ONLY, NO REAL NUMBERS

**Do not treat any content below as a finding.** Numbers are never fabricated; only a falsifiable
predicted *direction* is stated per result, with `evidence_strength="missing"` and
`rq_answered=false` throughout.

- **RQ1 → result_text [PLACEHOLDER-HYPOTHESIZED DIRECTION]:** "Predicted: when the executor is
  held fixed and the plan is substituted for a faulty one (or the plan is held fixed and the tool
  substituted), the outcome-flip rate will be measurably above the no-op control for all three
  fault classes — but agreement will be strongest for tool-break faults (most directly observable
  as an execution error) and weakest for plan-corruption faults (effects propagate diffusely
  before manifesting as task failure)." **result_type:** quantitative (predicted).
  **evidence_strength:** missing. **rq_answered:** false.
  **FALSIFICATION CONDITION:** "Refuted if, across substitution trials, the outcome-flip rate is
  statistically indistinguishable from the no-op control regardless of which component was
  substituted — i.e. failure does NOT track the substituted component at better than control
  rates, refuting the seed premise that 'failure moves with the substituted component.'"
- **RQ_INF_1 → result_text [PLACEHOLDER-HYPOTHESIZED DIRECTION]:** "Predicted: LLM-judge and
  heuristic attribution methods will show mechanically-verified component-attribution accuracy
  substantially below the 100% ground-truth ceiling, with the largest confusion between plan-level
  and execution/tool-level blame; intervention-based do-then-verify (DoVer-style) and the trained
  tracer (AgenTracer-style) will outperform post-hoc LLM-judge, and all real methods will beat the
  random/majority control." **result_type:** quantitative (predicted). **evidence_strength:**
  missing. **rq_answered:** false.
  **FALSIFICATION CONDITION:** "Refuted if candidate attribution methods achieve accuracy
  statistically indistinguishable from the ground-truth ceiling (near-perfect match) across all
  three fault categories — that would show mechanical verification exposes no meaningful
  attribution-accuracy gap in current methods — OR if no real method exceeds the random/majority
  control, which would indicate the benchmark labels carry no learnable signal."

**Status:** NOT_FOUND (no experiment has been run). **Absence comment:** `what_missing`: "No real
results exist because the paper has not been written or the experiment run." `why_matters`: "A
reader must not mistake the predicted directions for actual findings — doing so would be exactly
the unverified causal claim this topic is designed to discourage." `implication`: "Re-run this
node from real output once the minimal experiment is executed; until then both results are open
hypotheses with the stated falsification conditions."

---

## N10 Threats

**[HYPOTHESIS]** anticipated limitations of this study type (no authors exist to have stated them;
standard threats for fault-injection/causal-attribution + benchmark designs). Categorized per the
schema enum.

- **t1** [construct]: "Injected faults (corrupted plan step / broken tool / polluted observation)
  may not represent the true distribution of naturally-occurring agent failures, so
  component-attribution accuracy measured on synthetic faults may not transfer to real-world
  attribution." **mitigation:** "Contrast injected-fault results against the naturally-failing,
  human-labeled Who&When set (`[WhoAndWhen, OpenReview:GazlTYxZss]`); report the gap explicitly."
  **[HYPOTHESIS]**
- **t2** [external]: "The task suite, agent scaffold, and fault taxonomy will be built around a few
  specific tool-use frameworks and LLM backbones, limiting generalization across architectures and
  models." **mitigation:** "Scale-up stage spans multiple frameworks (e.g. MetaGPT-style vs. a
  plain plan-executor loop) and ≥2 LLM backbones; report per-framework accuracy." **[HYPOTHESIS]**
- **t3** [internal]: "The substitution protocol assumes components can be cleanly swapped while
  holding others fixed; tight coupling (a plan format the executor expects) or agent stochasticity
  may make some swaps unrealistic or flip outcomes independent of the intended fault, confounding
  the label." **mitigation:** "k-replay majority outcome, temperature-0/fixed-seed runs,
  orchestrator-message-level edits, and the M3 outcome-flip filter discard confounded trials."
  **[HYPOTHESIS]**
- **t4** [conclusion]: "Component-attribution accuracy is compared across methods with limited
  sample sizes per fault category; without correction, multiple comparisons across the method ×
  category grid could yield spurious significance — and trials generated from a shared base task
  are dependent, so trial-level tests would overstate the effective n." **mitigation:**
  "Pre-registered analysis plan, McNemar-style tests on paired outcomes with cluster-robust
  inference at the base-task level, Benjamini-Hochberg correction, 95% cluster-bootstrap CIs (N8
  analysis plan)." **[HYPOTHESIS]**
- **t5** [scope]: "The taxonomy covers single-component faults (plan/tool/observation) and does not
  address compound failures where multiple components are simultaneously faulty, nor failures with
  no single locus (the distributed-responsibility case DoVer raises)." **mitigation:** "Explicitly
  scoped out; multi-component blame supported in scoring (M5) as a forward-looking extension."
  **[HYPOTHESIS]**

**Status:** NOT_FOUND (no author-written Threats section — paper unwritten). **Absence comment:**
`what_missing`: "There is no author-written limitations/threats section to extract." `why_matters`:
"The absence is expected for a pre-paper idea, but t1–t5 are worth pre-registering." `implication`:
"Replace with the authors' self-stated threats once a draft exists; do not cite t1–t5 as author
admissions."

---

## N11 Artifacts

**Status:** NOT_FOUND. **[PLACEHOLDER]** — nothing released; the paper does not exist.

- `artifacts`: []
- `has_code`: false
- `has_data`: false
- `has_model`: false

**Absence comment:** `what_missing`: "No code repository, dataset, model, or demo has been
released because no experiment has been run and no paper written." `why_matters`: "A reviewer
evaluating reproducibility/artifact availability should treat this as entirely unreleased, not
merely undocumented." `implication`: "Once the fault-injection library and benchmark (M1/M3, CO1)
are built, re-populate with real artifact entries — the labeled benchmark is expected to be the
primary artifact given the 'Defects4J for agents' framing."

---

## N12 Contribution Type

**Value:** `benchmark` **[HYPOTHESIS]**

**Rationale:** The seed explicitly frames the known-fault-labeled corpus itself as the primary
contribution — "这是给 agent 领域造一个'Defects4J'——已知故障标注库本身就是贡献" ("building a
Defects4J for the agent domain — the known-fault-labeled corpus itself is the contribution")
**[GIVEN]**. Per the N12 disambiguation hints ("We introduce benchmark X containing N tasks" →
`benchmark`; "We compared N methods on benchmark X" → `empirical`), what N9 validates is not a
general measurement study of an existing phenomenon but the construction and mechanical-verification
protocol (M1/M2/M3, CO1/CO2) of a new, reusable, ground-truth-labeled evaluation resource against
which attribution methods are then compared (CO3). The comparison (CO3) is a *demonstration* of the
resource's value — mirroring how `[Terminal-Bench, OpenReview:a7Qa4CcHak]` frames its empirical
section as a demonstration of a released resource rather than the headline — so the resource, not
the comparison, is the headline. Classification confirmed as `benchmark` (not `dataset`)
because the paired substitution *protocol* + labeled corpus form an evaluation harness for scoring
methods, not merely a static labeled dataset. **[HYPOTHESIS]**

**Status:** PARTIAL (classification reasoned from the seed's own framing, not read from a written
Contributions/Introduction section). **Absence comment:** `what_missing`: "No author-written
Introduction or Contributions section exists yet to state the contribution type directly; the
`benchmark` value is inferred from the seed's Chinese-language core question/minimal-experiment
text (quoted above, [GIVEN]) plus the N12 disambiguation heuristic applied to the hypothesized
N6/N7 design." `why_matters`: "A downstream reader should not treat `benchmark` as an
author-declared classification — it is this digest's best reading, and paper.md's independent
Step 2 archetype call (Resource/Benchmark, secondary Empirical) should be checked for agreement
before it is relied on." `implication`: "Confirmed: paper.md Step 2 independently arrives at the
same Resource/Benchmark-primary, Empirical-secondary classification, which corroborates this N12
value; re-derive from a real Introduction once written."

---

## Claims

- "Failure-attribution accuracy for tool-use agent pipelines can be mechanically validated by
  checking whether attributed blame matches the component that was actually substituted/faulted —
  with the ground-truth label anchored to an observed outcome flip — rather than trusting
  unvalidated post-hoc explanations or human-agreement scores." — evidence: argument, tied to
  CO2/M2/M3; contrasts `[WhoAndWhen, OpenReview:GazlTYxZss]` and `[DoVer, OpenReview:mrEK16Jy6h]`.
  **[HYPOTHESIS]**
- "A controlled-substitution protocol that holds two of three pipeline components fixed while
  swapping the third (with k-replay and an outcome-flip filter) isolates the causal source of
  failure, addressing the confound that naive attribution heuristics conflate correlation with
  true component-level responsibility." — evidence: argument, tied to C1/C2/M2. **[HYPOTHESIS]**
- "Current candidate attribution methods are predicted to show substantially lower accuracy on
  plan-level faults than on tool-level faults, because plan-corruption effects propagate more
  diffusely before manifesting as task failure." — evidence: prediction only, no experiment;
  falsifiable per N9's stated condition. **[PLACEHOLDER — hypothesized direction, no data]**
- "A labeled fault-injection benchmark whose ground truth is fixed by construction (inject →
  replay → keep on outcome flip) would constitute a reusable 'Defects4J-style' asset for the
  agent-failure-attribution community — extending the by-construction labeling of `[AgenTracer,
  OpenReview:l05DseqvuD]` from single-step decisive-error labels to a plan/tool/observation
  component taxonomy." — evidence: seed's own framing (N12) + AgenTracer precedent; contingent on
  the benchmark being built and released. **[PLACEHOLDER / HYPOTHESIS]**

---

## References

**[PLACEHOLDER for this paper's own bibliography]** — no bibliography exists; the paper has not
been written. The N3 works above are **real papers**: eight are from the local OpenReview corpus
(`topics/corpus/ideas.jsonl`), cited with their real `paper_id` and forum URL; one (Defects4J,
Just et al., ISSTA 2014) is a canonical SE benchmark named by the seed, flagged non-corpus and to
be verified at write time. They are grounding for this reverse digest, not a bibliography drawn
from an actual References section.
