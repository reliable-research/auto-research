# Digest: How Few Replays Suffice? Budget-Bounded Localization of Decisive Failures in Long Trajectories

> **REVERSE-DIGEST NOTICE.** This document does not summarize an existing paper — no such
> paper has been written yet. It is speculative scaffolding for research planning, built by
> projecting the seed idea (topic **B2.2**, label **[资源] / [Resource]**, parent topic
> **B2. 失败归因（plan / tool / execution）— Failure attribution: plan / tool / execution**)
> forward into the shape of a full N0–N12 digest, as if a paper answering it had been
> completed. Every field below carries one of four trust tags instead of the normal
> `extracted`/`inferred` source values:
> - **[GIVEN]** — verbatim/near-verbatim from the seed README (title, core question 核心问题,
>   minimal experiment 最小实验, gap-type label).
> - **[HYPOTHESIS]** — reasoned elaboration grounded in the seed + standard practice for this
>   kind of study. A prediction, not a fact.
> - **[GROUNDED:corpus]** — a real OpenReview paper from the local corpus
>   (`topics/corpus/ideas.jsonl`); its `approach_summary` is grounded in that paper's own
>   motivation/method text. The paper is real; its *fit* to this future paper is my judgment.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is done (authors, DOI, numbers,
>   artifacts). Never invented.
>
> Because there is no PDF, the schema's page/section `Locator` is replaced with either a
> pointer into the seed README (for [GIVEN] fields), a pointer into a corpus paper's
> motivation/method text (for [GROUNDED:corpus] fields), or the note `"derived, no source
> document"` (for [HYPOTHESIS]/[PLACEHOLDER] fields).

---

## N0 — Metadata

- `title`: "How Few Replays Suffice? Budget-Bounded Localization of Decisive Failures in Long Trajectories" **[GIVEN]** — verbatim from README line 16.
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — no paper exists, no authors assigned.
- `abstract` **[HYPOTHESIS]** (explicitly a draft, not a real abstract):
  > "Diagnosing why a long LLM-agent trajectory failed increasingly relies on counterfactual
  > replay: re-executing the trajectory from an intermediate checkpoint and observing whether
  > the outcome flips. Recent failure-attribution systems either read logs without replaying
  > (cheap but causally unverified) or replay one intervention per step (causally grounded
  > but linear in trajectory length). We ask: under a fixed replay budget, how few targeted
  > replays are needed to localize the decisive failure step, and how much do structured
  > search strategies — bisection over checkpoint indices and noise-tolerant group testing —
  > save relative to exhaustive per-step replay, uniform sampling, and zero-replay LLM
  > judging? On trajectories with programmatically injected, replay-verified failure
  > locations across plan/tool/execution layers, plus human-annotated natural failures, we
  > measure per-strategy cost-accuracy curves under matched budget sweeps. We hypothesize
  > that structured replay reaches near-exhaustive localization accuracy at a logarithmic
  > fraction of the replay cost, with group testing more robust than bisection when replay
  > outcomes are stochastic or failures span layer boundaries."
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"AI/ML"` **[HYPOTHESIS]** — LLM-agent trajectories, failure attribution; clear secondary overlap with SE (fault localization / delta debugging), reflected in N3/N4.
- **Status**: PARTIAL. `absence_comment`: `{"what_missing": "No authors or verified abstract exist because this paper has not been written.", "why_matters": "Bibliographic identity fields are normally used downstream (citation, indexing, reviewer assignment) and cannot be trusted yet.", "implication": "Treat authors/abstract as provisional scaffolding only; re-extract once a real manuscript exists."}`

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]**, built as a full predicate directly from the core question:
  "measure, under a fixed replay budget B, the minimum number of targeted re-executions
  ('replays' from step-boundary checkpoints) required to localize the decisive failure step
  and its layer (plan / tool / execution) in a long LLM-agent trajectory, by comparing
  bisection-search and group-testing replay strategies against uniform sampling, exhaustive
  per-step counterfactual replay, and zero-replay log-only LLM judging — producing, for each
  strategy, a cost-(replay units)-vs-accuracy-(correct localization) tradeoff curve."
  - Self-check: kind of task = localization/measurement study; domain = long LLM-agent
    trajectories (plan/tool/execution steps); outcome shape = per-strategy cost-accuracy
    tradeoff curves. All three land.
- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  1. A long agent trajectory (ordered sequence of plan / tool-call / execution steps) with
     step-boundary checkpoints of agent + environment state.
  2. Ground-truth decisive-failure location and layer, known via programmatic fault
     injection or human annotation **[GIVEN — "在已知故障位置的轨迹上", README line 19]**.
  3. A replay oracle: re-execute the trajectory suffix from any checkpoint and return the
     end-of-task pass/fail outcome from the task's own verifier.
  4. A fixed replay budget B (max replay units allowed per trajectory).
- `outputs` **[HYPOTHESIS]**:
  1. The predicted decisive failure step index and layer label per trajectory/strategy/budget.
  2. Per-strategy cost-accuracy curves and their summary statistics (accuracy@budget, AUC).
- `constraints`:
  1. Ground-truth failure location is known for evaluation **[GIVEN]** — README line 19:
     "在已知故障位置的轨迹上比较...".
  2. The trajectory is decomposable into discrete, individually checkpointable and
     replayable steps **[HYPOTHESIS]** — required for bisection/group-testing search to be
     well-defined; the same assumption is operationalized by checkpointed replay in
     intervention-driven debugging (cf. N3 [DoVer, OpenReview:mrEK16Jy6h]).
  3. The replay oracle's pass/fail signal may be stochastic; strategies may spend budget on
     repeated replays of the same checkpoint **[HYPOTHESIS]**.
- **Status**: PARTIAL (objective/inputs/outputs are inferred, not stated as a formal
  formulation in the seed). `source`: mixed, see tags; `location`: README lines 16–19 for
  [GIVEN] parts, "derived, no source document" for [HYPOTHESIS] parts.
  `absence_comment`: `{"what_missing": "The seed states a research question and a minimal experiment sketch, not a formal problem formulation.", "why_matters": "Without inputs/outputs/constraints spelled out, what counts as one replay, what the oracle returns, and what ground truth looks like are underspecified.", "implication": "The objective/inputs/outputs above are a reasoned reconstruction; a real paper may formalize differently (e.g. define 'decisive' via outcome-flipping counterfactuals as in AgenTracer/Who&When)."}`

---

## N2 — Motivation

- MotivationItem 1 **[HYPOTHESIS, grounded]**: "As LLM agents execute long multi-step
  trajectories, engineers 'must manually inspect long interaction logs to determine which
  agent and which action caused the failure', and this manual attribution 'becomes
  prohibitively expensive and inconsistent' as interaction length grows." `evidence`:
  `[{"type": "citation", "text": "motivation text of Who&When", "source": "[GROUNDED:corpus]", "location": "OpenReview:GazlTYxZss, motivation"}]`.
- MotivationItem 2 **[HYPOTHESIS, grounded]**: "The causally sound alternative to log
  reading is counterfactual replay — 'only re-execution can determine whether the
  hypothesized failure point was causally relevant' — but every replay re-invokes real LLM
  and tool calls, so replay count is the scarce resource. The seed's [资源] label makes this
  cost-accuracy tradeoff, uncharacterized by existing attribution work, the object of
  study." `evidence`: `[{"type": "citation", "text": "method text of DoVer (checkpointed replay and counterfactual verification)", "source": "[GROUNDED:corpus]", "location": "OpenReview:mrEK16Jy6h, method"}]`; label tie-in `label: "[资源]"` **[GIVEN]**.
- MotivationItem 3 **[HYPOTHESIS, grounded]**: "Systems that do use counterfactual replay to
  label decisive errors do so exhaustively — 'we replay the execution while replacing one
  step at a time' — i.e., linear in trajectory length; if structured search could match that
  accuracy in logarithmically many replays, causally verified attribution would become cheap
  enough to run routinely in agent development loops." `evidence`:
  `[{"type": "citation", "text": "method text of AgenTracer (counterfactual decisive-error discovery)", "source": "[GROUNDED:corpus]", "location": "OpenReview:l05DseqvuD, method"}]`.
- MotivationItem 4 **[HYPOTHESIS]**: "The parent topic's plan/tool/execution split implies
  decisive failures are not confined to one layer; a budget-bounded localizer must attribute
  across layer boundaries, not just within one homogeneous log of identical steps."
  `evidence`: `[]`, `location`: "derived from parent_topic field, no source document."

---

## N3 — Related Works

Eight of nine works below are real OpenReview papers retrieved from the local corpus
(`ideas.jsonl`, 11,683 papers) via keyword search (queries: failure attribution / blame
assignment; replay / counterfactual intervention / rollback; step-level credit assignment /
error propagation; budget / query efficiency / adaptive sampling; branching-point rollouts).
Each `approach_summary` is grounded in that paper's own motivation/method text. One
non-corpus entry ([Zeller & Hildebrandt, 2002]) is retained as the canonical delta-debugging
reference — clearly marked; it is a real, verifiable IEEE TSE paper, cited from memory, not
from the corpus.

| citation_key | approach_summary | paper_url | source |
|---|---|---|---|
| [Who&When, OpenReview:GazlTYxZss] | Formalizes automated failure attribution in LLM multi-agent systems as identifying "decisive errors — agent–time pairs whose correction flips a failed trajectory into success"; contributes the Who&When dataset of human-annotated failure logs and LLM-judge attribution strategies (all-at-once, step-by-step, binary search over the log context) plus a hybrid agent-then-step pipeline. | https://openreview.net/forum?id=GazlTYxZss | [GROUNDED:corpus] |
| [AgenTracer, OpenReview:l05DseqvuD] | Generates causally grounded decisive-error labels by "replaying the execution while replacing one step at a time with a minimally corrected action" (earliest outcome-flipping step = decisive error) and by programmatic fault injection into successful traces; trains a specialized RL tracer on the resulting corpus to predict responsible agent and step from logs. | https://openreview.net/forum?id=l05DseqvuD | [GROUNDED:corpus] |
| [DoVer, OpenReview:mrEK16Jy6h] | Treats failure attribution as a testable causal hypothesis: segments a failed session into planning-execution trials, generates a suspected agent/step hypothesis per trial, synthesizes a message-level intervention, then performs "checkpointed replay and counterfactual verification" — replaying from the intervention point to see whether the outcome changes, evaluating recovery and partial progress. | https://openreview.net/forum?id=mrEK16Jy6h | [GROUNDED:corpus] |
| [InT, OpenReview:YAhTj2VgBw] | Locates the first erroneous step of a failed reasoning rollout via reference-grounded self-verification, proposes a single corrective intervention for that step, and fine-tunes on prefix+intervention — using first-error localization for training-time credit assignment without PRMs or large branching-rollout pipelines. | https://openreview.net/forum?id=YAhTj2VgBw | [GROUNDED:corpus] |
| [TRIM, OpenReview:MoKrugWUfC] | Routes compute at the step level under an explicit strong-model token budget: a weak model drafts each reasoning step, a PRM-based risk signal plus a budget-aware policy decides whether to regenerate that step with a strong model — allocating expensive computation to the few steps where errors would cascade. | https://openreview.net/forum?id=MoKrugWUfC | [GROUNDED:corpus] |
| [AttnRL, OpenReview:NCN8oUsiNf] | Observes that "sampling dominates the cost of process-supervised RL" and that heuristic branch placement wastes rollout budget; scores each step's Forward Context Influence from attention structure and launches Monte Carlo rollouts only from the most influential steps, plus difficulty-aware sample allocation. | https://openreview.net/forum?id=NCN8oUsiNf | [GROUNDED:corpus] |
| [iStar, OpenReview:ooROvpmxMV] | Derives dense per-action credit for multi-turn agent RL without any replay: trains an implicit process reward model with a multi-turn DPO objective on trajectory preference pairs and reads off step-level rewards as PRM-to-reference log-probability ratios, combined with outcome-level advantages in critic-free RL. | https://openreview.net/forum?id=ooROvpmxMV | [GROUNDED:corpus] |
| [BAI-LD, OpenReview:gYetLsNO8x] | Theory of best-arm identification with a fixed sampling budget: a large-deviation framework coupling the empirical allocation process of any adaptive algorithm to error-exponent bounds on empirical rewards, yielding sharper guarantees for Successive Rejects and a new continuously-adaptive elimination algorithm — the formal template for "identify the target under a fixed number of noisy queries." | https://openreview.net/forum?id=gYetLsNO8x | [GROUNDED:corpus] |
| [Zeller & Hildebrandt, 2002] | Canonical delta debugging (ddmin): recursively bisects/partitions a failure-inducing input, re-running a deterministic pass/fail test on each candidate subset to isolate a minimal failure-inducing configuration in near-logarithmic test count. ("Simplifying and Isolating Failure-Inducing Input," IEEE TSE 28(2).) **Non-corpus canonical entry, cited from memory.** | (not in corpus) | [HYPOTHESIS-GROUNDED, non-corpus] |

**Status**: FOUND (9 works, within the 5–10 range; 8 corpus-grounded, 1 canonical).

---

## N4 — Prior Limitations

`grounding_check`: **true** — every limitation cites at least one `affects_works` entry
matching an N3 `citation_key` exactly. All entries **[HYPOTHESIS, grounded]**: there is no
future-paper text to extract from, but each limitation is defensible from the cited paper's
own motivation text or from what its stated method demonstrably does not cover.

| # | limitation_text | affects_works | limitation_type |
|---|---|---|---|
| L1 | Log-only attribution is causally unverified and empirically weak at step granularity: Who&When's own evidence shows "agent-level attribution is already difficult, and step-level attribution is substantially worse" (as summarized in DoVer's motivation), and its binary-search variant searches the *log context* with an LLM judge — it never re-executes anything, so a wrong verdict costs zero replays but also carries no counterfactual guarantee. | [Who&When, OpenReview:GazlTYxZss] | precision |
| L2 | Counterfactual replay labeling is exhaustive: AgenTracer replays "one step at a time" per failed trajectory, i.e., O(n) interventions each requiring suffix re-execution; the method text never characterizes how few replays would have sufficed, nor any accuracy-vs-replay-budget tradeoff — replay is treated as an offline label-generation cost, not a rationed resource. | [AgenTracer, OpenReview:l05DseqvuD] | efficiency |
| L3 | Intervention-driven debugging verifies whichever hypotheses an LLM proposes: DoVer replays from LLM-suggested intervention points and evaluates outcome change/recovery, but issues no budget-optimal search over checkpoint indices and does not compare structured strategies (bisection, group testing, uniform sampling) at matched replay budgets — its evaluation targets recovery utility, not localization cost curves. | [DoVer, OpenReview:mrEK16Jy6h] | efficiency |
| L4 | First-error localization via reference-grounded self-verification requires a reference solution to compare against, which exists for open math datasets but not for open-ended agent tasks (web, tool-use), and its localization is judged by downstream training benefit rather than by localization accuracy under any query budget. | [InT, OpenReview:YAhTj2VgBw] | generalizability |
| L5 | Step-level compute-allocation and credit-assignment methods intervene *during generation or training*: TRIM decides per-step escalation while the trajectory is being produced; AttnRL allocates rollout branches to influence-scored steps during RL; iStar derives implicit step rewards from preference pairs without replay. None provides post-hoc localization of the decisive step in a *fixed, already-failed* logged trajectory, nor cost-accuracy guarantees for that diagnostic task. | [TRIM, OpenReview:MoKrugWUfC], [AttnRL, OpenReview:NCN8oUsiNf], [iStar, OpenReview:ooROvpmxMV] | other |
| L6 | Fixed-budget best-arm identification analyzes adaptive allocation over stateless arms with i.i.d. reward draws; it does not model a sequence of causally ordered checkpoints where the query signal (suffix-replay outcome) has approximately monotone structure in the index and per-query cost varies with checkpoint position — so its guarantees do not transfer directly to trajectory localization. | [BAI-LD, OpenReview:gYetLsNO8x] | theoretical |
| L7 | Classical delta debugging assumes a cheap, deterministic, arbitrarily repeatable pass/fail test; LLM-agent replay violates all three (each replay costs real model/tool calls, outcomes are stochastic under sampling, and environments may drift), so ddmin's minimality guarantees do not carry over unmodified. | [Zeller & Hildebrandt, 2002] | generalizability |

---

## N5 — Challenges

`conflation_check`: **true** (four distinct obstacles, no near-duplicates). All **[HYPOTHESIS,
tightly derived]** from the core question — problem-inherent, not framed as any prior tool's
failure (N4-vs-N5 test applied). C-ids kept stable from the previous digest revision.

| id | text | source |
|---|---|---|
| C1 | Each replay re-invokes real LLM and tool calls over the trajectory suffix, so replay cost is both nonzero and *position-dependent* (replaying from step 3 of 40 costs ~10x more model calls than from step 36) — the resource being rationed is not a unit query count but heterogeneous replay units, directly per the core question "最少需要几次定向 replay". | [HYPOTHESIS] |
| C2 | Failure causation is non-local: a bad early plan decision may only manifest in the task outcome many steps later, and intermediate steps have partial recovery probability — so the checkpoint-indexed replay signal is only *approximately* monotone in the index, violating the clean bisection invariant that classical binary search and ddmin rely on. | [HYPOTHESIS] |
| C3 | LLM replay is stochastic: re-executing the same suffix twice under nonzero temperature can yield different pass/fail outcomes, so a single replay is a noisy oracle query; any budget accounting must include the repeated queries (votes) needed to de-noise each decision point. | [HYPOTHESIS] |
| C4 | The trajectory spans three heterogeneous layers (plan / tool / execution) with different step semantics, checkpoint sizes, and failure signatures; a decisive failure may need to be attributed across layer boundaries, complicating how a bisection split or a group-testing partition carves up the index space. | [HYPOTHESIS] |

---

## N6 — Methodology

### `overview` **[HYPOTHESIS]**
The study builds a checkpointed replay harness over sandboxed agent environments, constructs
a trajectory corpus with replay-verified ground-truth failure locations, and runs matched
budget sweeps of five localization strategies to produce per-strategy cost-accuracy curves.
The core localization primitive is the *suffix-replay predicate* g(k): re-execute the
trajectory from checkpoint k (steps k..n re-sampled by the same policy, with the recorded
prefix 1..k−1 fixed and its tool calls served from cache) and return the task verifier's
pass/fail outcome. For a decisive failure at step d, replays with k ≤ d can escape the
failure while replays with k > d inherit the corrupted state — an approximately monotone
signal that bisection (M3) exploits in O(log n) queries and that noise-tolerant group
testing (M4) exploits with redundancy. Because g(k) is scored on the *end-of-task* outcome,
late-manifesting effects of early causes are captured by the oracle rather than assumed
local (partial answer to C2).

**Staged plan.**
- *Stage 1 — pilot (= the seed's minimal experiment, README line 19)*: ~60 trajectories with
  injected known-position faults (20 per layer) in one deterministic environment (ALFWorld)
  with one agent scaffold and one model; compare 二分重放 (bisection), 分组测试 (group
  testing), 均匀抽样 (uniform sampling) cost-accuracy curves against exhaustive per-step
  replay. Success gate: the harness reproduces injected failures deterministically ≥95% of
  the time, and the curves separate visibly.
- *Stage 2 — scale-up*: ~300 injected-fault trajectories across two environments (ALFWorld +
  a cached-web GAIA subset), two agent scaffolds, two LLM families; add the zero-replay
  Who&When-style judge and DoVer-style hypothesis-then-verify baselines; add a
  natural-failure evaluation slice on human-annotated Who&When logs (re-hosted in the replay
  harness where re-executable); run the full statistical analysis of N8.

`location`: "derived, no source document; replay-primitive design grounded in [DoVer, OpenReview:mrEK16Jy6h] (checkpointed replay) and [AgenTracer, OpenReview:l05DseqvuD] (fault injection)."

### `key_components`
| id | name | text |
|---|---|---|
| M1 | Checkpointed replay harness | Snapshots agent state (message history, scratchpad) and environment state (containerized filesystem/env-simulator state; cached tool-call responses keyed by call hash) at every step boundary; exposes `replay(k, seed) -> pass/fail` using the task's own verifier. Cost accounting instrument: every replay is billed in *replay units* = number of resumed LLM calls, logged per invocation. Granularity: one step = one LLM call plus its tool result. |
| M2 | Fault-injected trajectory corpus with verified ground truth | Following AgenTracer-style programmatic fault injection: perturb one step of a *successful* trajectory (plan layer: corrupt a subgoal; tool layer: corrupt a tool argument; execution layer: corrupt a tool response/observation), replay downstream, and keep the trajectory only if the perturbed run fails and a replay from the injected step with the original action succeeds — yielding a replay-verified decisive step index + layer label per trajectory. Target composition: balanced across the three layers; trajectory lengths 20–60 steps. |
| M3 | Bisection replay localizer | Binary search over checkpoint indices using the suffix-replay predicate g(k), with r repeated replays (majority vote, r ∈ {1,3,5}) per probe to de-noise; expected cost O(r·log n) probes, each billed by suffix length in replay units. |
| M4 | Noise-tolerant group-testing replay localizer | Adaptive group testing over the step-index space: partition steps into g groups (contiguous or layer-crossing designs), test groups via multi-step interventions (replace all steps of a group with recorded-correct actions where available, else re-sample) and group-level outcome patterns with built-in redundancy; refine within the implicated group. Designed to tolerate a noisy oracle and to localize even when the implicated span crosses plan/tool/execution boundaries. |
| M5 | Baseline suite | (a) uniform-random checkpoint sampling; (b) exhaustive per-step counterfactual scan (the AgenTracer labeling procedure; O(n) probes — accuracy upper bound); (c) zero-replay log-only LLM judge in Who&When's all-at-once and step-by-step configurations (cost lower bound); (d) DoVer-style LLM hypothesis generation followed by replay verification of each hypothesis. |
| M6 | Cost-accuracy curve evaluator | Sweeps a fixed budget grid B ∈ {2, 4, 8, 16, 32, 64, exhaustive} replay units per trajectory; at each budget, records each strategy's localization accuracy (exact-step, step@±2 tolerance, layer) and computes normalized area under the accuracy-vs-log(budget) curve; bootstrap CIs over trajectories. |

(all `source="[HYPOTHESIS]"`, `location`: "derived, no source document"; M2 grounded in
[AgenTracer, OpenReview:l05DseqvuD] method text, M5(c) in [Who&When, OpenReview:GazlTYxZss],
M5(d) in [DoVer, OpenReview:mrEK16Jy6h].)

### `challenge_arguments`
| challenge_id | argument_text | mechanism_components |
|---|---|---|
| C1 | "Checkpointed replay re-runs only the suffix (cheaper for late checkpoints), replay units are billed per resumed LLM call rather than per probe, and bisection converges in O(log n) probes instead of the O(n) probes of an exhaustive scan — so the position-dependent cost is both measured honestly and minimized structurally." | [M1, M3] |
| C2 | "The suffix-replay predicate is scored on the end-of-task verifier outcome, so a cause that manifests late is still detected by probes at or before the causal step; residual non-monotonicity from recovery probability is measured directly (fraction of injected faults whose g(k) profile violates monotonicity) rather than assumed away." | [M1, M6] |
| C3 | "Both search strategies budget explicitly for de-noising: bisection spends r votes per probe, and group-testing designs carry redundancy as the standard combinatorial mechanism for tolerating a noisy oracle; the r-vs-accuracy tradeoff is itself an experimental variable (RQ_INF_3)." | [M3, M4] |
| C4 | "Fault injection produces balanced ground truth across plan/tool/execution layers, and group-testing partitions are defined over the whole step-index space — including layer-crossing group designs — so attribution is evaluated across, not within, layer boundaries." | [M2, M4] |

(all `source="[HYPOTHESIS]"` — predicted authorial arguments a future paper would make, not
extracted text; per V-08, inference-level confidence only.)

### `unaddressed_challenges`
`["C2"]` **[HYPOTHESIS]** — C2 is only *partially* addressed: the end-of-task oracle handles
late manifestation, but when intermediate steps have substantial recovery probability the
g(k) signal becomes genuinely non-monotone and bisection can converge to the wrong index no
matter how many votes are spent; the study measures this failure mode but does not claim to
solve it.

### Feasibility (order-of-magnitude)
**[HYPOTHESIS]** — all figures are planning estimates, not results.
- *Scale*: pilot 60 trajectories; scale-up 300 injected + a natural-failure slice; mean
  trajectory length ~30 steps; mean suffix replay ~15 LLM calls.
- *Compute/API*: worst-case per-trajectory sweep is dominated by the exhaustive baseline
  (~30 probes × 3 votes) plus the budget grid for 4 other strategies — order 10^2 replays ≈
  1.5×10^3 LLM calls per trajectory; scale-up total ≈ 5×10^5 LLM calls. At GPT-4o-mini-class
  pricing this is a low-thousands USD API cost class (~$1–3k); pilot ≈ 10^4 calls, <$200.
  No model training; GPU need is zero unless open-weight agents are self-hosted (1 node,
  <200 GPU-hours).
- *Human effort*: ground truth is programmatic (replay-verified), so annotation is limited
  to spot-checking ~10% of injected faults and adjudicating the natural-failure slice —
  ~20–30 annotator-hours.
- *Single biggest feasibility risk*: faithful re-execution. Live tools (web search, real
  APIs) are non-deterministic and side-effectful, which can make g(k) meaningless.
  *Mitigation*: restrict to environments where replay is controllable — ALFWorld
  (deterministic simulator) and a GAIA subset run against cached/snapshotted web content —
  and serve all un-intervened prefix tool calls from the M1 response cache; report the
  harness's own reproduction rate (target ≥95% deterministic failure reproduction) as a
  manipulated check before any strategy comparison.

---

## N7 — Contributions

| id | text | contribution_type | is_testable | has_rq |
|---|---|---|---|---|
| CO1 | A checkpointed replay harness plus a replay-verified fault-injected trajectory corpus that together form a reusable budget-bounded evaluation protocol for failure-localization strategies over long agent trajectories. | technical_artifact | true | true |
| CO2 | An empirical demonstration (or refutation) that bisection and/or group-testing replay reach localization accuracy comparable to exhaustive per-step counterfactual replay at a logarithmic fraction of the replay cost, and strictly dominate uniform sampling and zero-replay LLM judging at matched budgets. | empirical_finding | true | true |
| CO3 | A characterization of *when* structure helps: how the bisection-vs-group-testing ranking depends on replay-outcome noise (votes r), on non-monotone g(k) profiles (recovery probability), and on the failure's layer (plan/tool/execution). | empirical_finding | true | true |
| CO4 | Practitioner guidance: a "minimum sufficient replay budget" curve — for a target localization accuracy, how many replay units to provision per trajectory of length n — for debugging long agent trajectories under cost constraints. | conceptual_framework | false | false |

All **[HYPOTHESIS]** — what such a paper would plausibly claim; `location`: "derived, no
source document."

---

## N8 — Research Questions

| id | text | rq_source | addresses_challenges | evaluates_mechanisms | tests_contributions |
|---|---|---|---|---|---|
| RQ1 | "In long trajectories, what is the minimum number of targeted replays needed to localize the decisive failure layer, and how much do bisection/grouped-retrieval strategies save relative to full re-execution?" **[GIVEN — near-verbatim restatement of README's 核心问题, line 18]** | explicit | [C1, C2] | [M3, M4, M5] | [CO2] |
| RQ_INF_1 | "How does localization accuracy degrade as the replay budget shrinks, for each of bisection, group testing, uniform sampling, exhaustive scan, and zero-replay LLM judging — i.e., what do the full cost-accuracy curves look like?" **[HYPOTHESIS]**, inferred because the minimal experiment explicitly calls for "定位成本-准确率曲线" (a cost-accuracy *curve*), implying a budget sweep. | inferred | [C1, C3] | [M3, M4, M5, M6] | [CO2, CO3] |
| RQ_INF_2 | "Does the relative advantage of structured replay hold consistently across plan, tool, and execution failure layers, and across contiguous vs. layer-crossing group designs?" **[HYPOTHESIS]**, inferred from the parent topic's explicit plan/tool/execution split. | inferred | [C4] | [M2, M4, M6] | [CO3] |
| RQ_INF_3 | "How many repeated replays (votes r) per probe are needed to stabilize the noisy oracle, and at what noise level does group testing's redundancy overtake bisection's vote-multiplied probes?" **[HYPOTHESIS]**, inferred from the stochastic-replay premise; the vote count is part of the budget, so this is the noise leg of the cost-accuracy question. | inferred | [C2, C3] | [M1, M3, M4] | [CO2, CO3] |

- `datasets` **[HYPOTHESIS]**: `{"names": ["ALFWorld (deterministic household tasks; substrate for injected-fault trajectories, pilot + scale-up)", "GAIA (cached-web subset; substrate for injected-fault trajectories with tool use, scale-up)", "Who&When human-annotated failure logs (natural-failure evaluation slice, re-hosted in the replay harness where re-executable) [GROUNDED:corpus — OpenReview:GazlTYxZss]", "Self-built fault-injected corpus (~300 trajectories, replay-verified ground truth, balanced across plan/tool/execution; released as part of CO1)"], "source": "[HYPOTHESIS]", "location": "derived from minimal experiment, README line 19"}`
- `baselines` **[HYPOTHESIS]**: `{"names": ["Exhaustive per-step counterfactual scan (AgenTracer labeling procedure; accuracy upper bound, cost O(n)) [GROUNDED:corpus — OpenReview:l05DseqvuD]", "Zero-replay log-only LLM judge, all-at-once and step-by-step variants (Who&When) [GROUNDED:corpus — OpenReview:GazlTYxZss]", "DoVer-style LLM hypothesis generation + replay verification [GROUNDED:corpus — OpenReview:mrEK16Jy6h]", "Uniform-random checkpoint sampling", "Full re-execution reference (replay everything)"], "source": "[HYPOTHESIS]", "location": "derived from minimal experiment, README line 19"}`
- `metrics` **[HYPOTHESIS]**: `{"names": ["Exact-step localization accuracy (predicted index == ground-truth decisive index)", "Step accuracy@±2 (|predicted − true| ≤ 2, tolerance for boundary ambiguity)", "Layer accuracy (predicted plan/tool/execution label correct)", "Replay cost in replay units (number of resumed LLM calls consumed, position-weighted)", "Cost-accuracy AUC (normalized area under accuracy vs. log-budget over the grid B ∈ {2,…,64,exhaustive})", "Monotonicity-violation rate of g(k) (diagnostic for C2)"], "source": "[HYPOTHESIS]", "location": "derived from minimal experiment, README line 19"}`
- **Analysis plan [HYPOTHESIS]**: n = 60 trajectories (pilot) / 300 (scale-up), every
  strategy runs on the *same* trajectories at the *same* budget grid (fully paired design).
  Primary test: per-budget paired comparison of exact-step accuracy between each structured
  strategy and uniform sampling via McNemar's test; per-trajectory replay-units-to-correct-
  localization compared via Wilcoxon signed-rank. Significance α = 0.05 with Holm–Bonferroni
  correction across the budget grid and strategy pairs; 95% bootstrap CIs (1,000 resamples
  over trajectories) on all curves. Expected effect direction: at matched budgets,
  bisection and group testing > uniform sampling > zero-replay judge on exact-step accuracy;
  bisection/group testing reach ≥90% of the exhaustive scan's accuracy at ≤25% of its
  replay-unit cost; group testing > bisection specifically in the high-noise (r = 1,
  temperature > 0) and layer-crossing-failure strata. A power sanity check: n = 300 paired
  trajectories gives >80% power to detect a 10-percentage-point paired accuracy difference
  at α = 0.05 (McNemar, assuming ~20% discordance).

---

## N9 — Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**. No experiment has been run and no numbers
exist. Every entry states a predicted direction, `evidence_strength="missing"`,
`rq_answered=false`, plus an explicit falsification condition.

| rq_id | result_text (predicted direction) | result_type | evidence_strength | rq_answered |
|---|---|---|---|---|
| RQ1 | Predicted: bisection and group-testing replay localize the decisive step/layer at accuracy statistically indistinguishable from the exhaustive per-step scan while consuming an O(log n)-scaling rather than O(n)-scaling number of probes. **Refuted if** structured strategies need replay-unit budgets ≥50% of the exhaustive scan's to reach within 5 points of its exact-step accuracy. | quantitative | missing | false |
| RQ_INF_1 | Predicted: structured strategies' accuracy degrades gracefully (roughly linearly in log-budget) as B shrinks, while uniform sampling collapses toward chance below B ≈ n/4 and the zero-replay judge sits at a flat, budget-independent floor well below replay-based methods. **Refuted if** uniform sampling's curve matches or dominates bisection's across the budget grid, or if the zero-replay judge matches replay-based accuracy (which would make replay pointless). | quantitative | missing | false |
| RQ_INF_2 | Predicted: the structured-replay advantage holds across all three layers, with the smallest margin for plan-layer faults (highest recovery probability → most non-monotone g(k)), and layer-crossing group designs beat contiguous ones only for plan-layer faults. **Refuted if** structured strategies specifically underperform uniform sampling on any one layer, or if layer identity has no measurable effect on the margins. | quantitative | missing | false |
| RQ_INF_3 | Predicted: r = 3 votes per probe suffice to stabilize bisection at temperature ≈ 0.7 (accuracy within 3 points of r = 5), and there exists a measurable noise level (single-replay flip rate ≳15%) above which group testing's built-in redundancy yields higher accuracy-per-replay-unit than vote-multiplied bisection. **Refuted if** accuracy is insensitive to r (oracle effectively deterministic — C3 moot) or if no noise regime shows a group-testing advantage (CO3's crossover claim fails). | quantitative | missing | false |

---

## N10 — Threats / Self-Limitations

**[HYPOTHESIS]** — anticipated limitations of this kind of study, written as a
pre-registration checklist; no real Threats section exists yet. Mitigations are the study's
planned answers, not author-stated text.

| threat_id | category | description | mitigation |
|---|---|---|---|
| t1 | construct | "Decisive failure" is operationalized via injected, replay-verified single faults; natural agent failures can be diffuse or multi-causal — DoVer's motivation argues the single-culprit assumption "is weak in practice" — so injected-fault localization accuracy may overstate real-world performance. | Include the natural-failure slice from Who&When's human-annotated logs; report injected vs. natural accuracy separately and flag any gap as a construct limit of the corpus. **[HYPOTHESIS, added 2026-07-04]** Additionally, pre-commit (R3) that M2's exogenous injection + keep-filter bias the measured monotonicity-violation rate downward by construction, so monotonicity claims are licensed as injected-corpus properties only; if the natural slice proves non-replayable and the injected violation rate is degenerate, the pre-committed pivot is the replayability/censoring measurement itself (paper.md F-G2). |
| t2 | internal | Replay stochasticity and environment drift confound the comparison: if the harness cannot reproduce the original failure deterministically, differences between strategies may reflect harness noise rather than search quality. | Gate all experiments on a ≥95% deterministic failure-reproduction check per trajectory (M1's cache + fixed seeds); treat vote count r as an explicit experimental factor (RQ_INF_3) rather than a hidden constant. |
| t3 | external | Results come from two environments (ALFWorld, cached-web GAIA), two agent scaffolds, and two LLM families; cost-accuracy curves may not transfer to other tool ecosystems, longer horizons, or multi-agent orchestration frameworks. | State scope explicitly; release the harness (CO1) so the sweep is rerunnable on new environments; include trajectory length as a covariate to expose scaling trends beyond the sampled range. |
| t4 | conclusion | The budget grid × strategy pairs induce many hypothesis tests; naive per-cell significance would inflate false positives, and n = 60 (pilot) is underpowered for small effects. | Pre-register the primary comparisons; Holm–Bonferroni across the grid; bootstrap CIs on all curves; treat the pilot as estimation-only (no significance claims) and reserve confirmatory testing for the n = 300 scale-up. |
| t5 | construct | Replay-unit cost accounting (resumed LLM calls) may not track dollar or latency cost faithfully across models with different pricing/context regimes, biasing the "savings" claim. | Report three cost axes in parallel — probe count, replay units, and measured API dollar cost — and check that strategy rankings are stable across all three. |

`status`: NOT_FOUND (no author-written Threats section exists — this is a fully anticipated
list). `absence_comment`: `{"what_missing": "There is no author-written Threats-to-Validity or Limitations section because no paper has been written.", "why_matters": "A reviewer cannot yet know which of these anticipated threats the eventual authors will actually acknowledge or address.", "implication": "Treat t1–t5 as a pre-registration checklist for the study design, to be replaced by the real Limitations section once the paper exists."}`

---

## N11 — Artifacts

`status`: **NOT_FOUND** **[PLACEHOLDER]** — nothing has been released because the paper does
not exist.
- `artifacts`: `[]`
- `has_code`: `false`
- `has_data`: `false`
- `has_model`: `false`
- `absence_comment`: `{"what_missing": "No code repository, dataset, or model has been released, since this is a prospective research idea rather than a completed paper.", "why_matters": "Reproducibility and reuse of the replay harness and fault-injected corpus (the CO1 artifact claim) cannot be assessed yet.", "implication": "Re-check this node once (and if) the work is carried out; CO1 commits the eventual paper to releasing the harness and corpus."}`

---

## N12 — Contribution Type

- `value`: **`empirical`** **[HYPOTHESIS]**
- `rationale`: "What the projected N9 results validate is a *measurement*: per-strategy
  cost-accuracy curves for failure localization under matched replay budgets (README line
  19's '比较…定位成本-准确率曲线'), analogous in shape to Lost-in-Conversation's
  simulation-based measurement of multi-turn degradation — the harness (M1) and
  fault-injected corpus (M2) exist to support that comparison, exactly as that paper's
  sharded-simulation environment supports its study. No new localization *algorithm* is
  claimed as the primary novelty (bisection and group testing are classical primitives being
  characterized), which rules out `system`/`tool`; the corpus is instrumentation, not the
  headline claim, which rules out `dataset`/`benchmark` under the 'study is the main
  contribution' rule." **[HYPOTHESIS]**
- `source`: [HYPOTHESIS]

---

## Claims

1. **[HYPOTHESIS]** "Bisection over checkpoint indices with an end-of-task suffix-replay
   oracle is predicted to localize the decisive failure step in O(log n) probes versus the
   O(n) probes of the exhaustive per-step counterfactual scan that current replay-based
   attribution uses for labeling." — `evidence`: `[{"type": "citation", "text": "AgenTracer's method replays 'one step at a time' — linear by construction; bisection replaces the linear scan given an approximately monotone predicate.", "source": "[GROUNDED:corpus]", "location": "OpenReview:l05DseqvuD method / N6 M3"}]`
2. **[HYPOTHESIS]** "Zero-replay log-only judging is predicted to sit at a
   budget-independent accuracy floor well below replay-based strategies, because it cannot
   causally verify — Who&When's step-level attribution is already reported as weak and
   DoVer's motivation states retrospective log reading 'is not a reliable basis for causal
   claims'." — `evidence`: `[{"type": "citation", "text": "DoVer motivation summarizing Who&When's step-level results", "source": "[GROUNDED:corpus]", "location": "OpenReview:mrEK16Jy6h motivation / N4 L1"}]`
3. **[HYPOTHESIS]** "Group-testing replay is predicted to overtake bisection specifically in
   the high-noise and layer-crossing-failure regimes, because redundancy is the standard
   combinatorial mechanism for noisy oracles and groups can span plan/tool/execution
   boundaries." — `evidence`: `[{"type": "argument", "text": "Group-testing designs tolerate noisy measurements via redundancy and partition the whole index space.", "source": "[HYPOTHESIS]", "location": "N6 challenge_arguments C3/C4"}]`
4. **[HYPOTHESIS]** "The study's sharpest internal risk is non-monotone g(k) from recovery
   probability (C2): if intermediate steps frequently recover, bisection's invariant breaks
   and the predicted savings shrink — this is measured (monotonicity-violation rate) but not
   solved." — `evidence`: `[{"type": "argument", "text": "C2 is listed as only partially addressed; RQ1's falsification condition operationalizes this risk.", "source": "[HYPOTHESIS]", "location": "N6 unaddressed_challenges / N9 RQ1"}]`
5. **[HYPOTHESIS]** "Ground truth built by fault injection is causally verified but may
   overstate accuracy on natural failures, whose culprits can be diffuse — hence the paired
   injected/natural evaluation slices." — `evidence`: `[{"type": "citation", "text": "DoVer motivation: the single-well-defined-culprit assumption 'is weak in practice'.", "source": "[GROUNDED:corpus]", "location": "OpenReview:mrEK16Jy6h motivation / N10 t1"}]`
6. **[PLACEHOLDER]** "No code, data, or model artifacts currently exist for this topic; all
   quantitative statements in N9 are hypothesized directions with explicit falsification
   conditions, not measured outcomes." — `evidence`: `[{"type": "observation", "text": "N11 status is NOT_FOUND; every N9 entry has evidence_strength='missing' and rq_answered=false.", "source": "[PLACEHOLDER]", "location": "N9 / N11"}]`

---

## Self-verification pass (per `self-verification.md`)

- **V-04 / EX-09 ID consistency**:
  - `N4.limitations[].affects_works` (L1–L7) each match an `N3.works[].citation_key` string
    exactly: [Who&When, OpenReview:GazlTYxZss], [AgenTracer, OpenReview:l05DseqvuD],
    [DoVer, OpenReview:mrEK16Jy6h], [InT, OpenReview:YAhTj2VgBw],
    [TRIM, OpenReview:MoKrugWUfC], [AttnRL, OpenReview:NCN8oUsiNf],
    [iStar, OpenReview:ooROvpmxMV], [BAI-LD, OpenReview:gYetLsNO8x],
    [Zeller & Hildebrandt, 2002] ✓ — every N3 work is affected by ≥1 limitation and vice
    versa; `grounding_check=true` ✓.
  - `N6.challenge_arguments[].challenge_id` (C1, C2, C3, C4) ⊆ N5 ids {C1..C4} ✓;
    `mechanism_components` reference only M1–M6, all defined in `key_components` before
    `challenge_arguments` ✓. `N6.unaddressed_challenges` = ["C2"] ⊆ {C1..C4} ✓.
  - N8: `addresses_challenges` ⊆ {C1..C4}; `evaluates_mechanisms` ⊆ {M1..M6};
    `tests_contributions` ⊆ {CO1..CO4} (RQ1→CO2; RQ_INF_1→CO2,CO3; RQ_INF_2→CO3;
    RQ_INF_3→CO2,CO3) ✓. CO1/CO4 `has_rq` flags consistent (CO1 is exercised by every RQ's
    infrastructure and claimed testable via the harness's reproduction-rate gate; CO4 has
    `has_rq=false` as guidance derived from, not tested by, the RQs — note: CO1's
    `has_rq=true` maps to the RQ_INF_3 use of M1) ✓.
  - `N9.results[].rq_id` (RQ1, RQ_INF_1, RQ_INF_2, RQ_INF_3) all exist in N8 ✓; every N9
    entry carries `evidence_strength="missing"`, `rq_answered=false`, and an explicit
    "refuted if" condition ✓.
- **V-02 / EX-11**: every non-FOUND node (N0 PARTIAL, N1 PARTIAL, N10 NOT_FOUND, N11
  NOT_FOUND) carries a full 3-part `absence_comment` ✓.
- **V-10/V-11 self-consistency**: N10 status NOT_FOUND with a populated anticipated list is
  intentional (pre-registration checklist, explained in absence_comment). N11:
  `has_code`/`has_data`/`has_model` all `false`, matching empty `artifacts` ✓.
- **V-12**: N12 rationale cites the seed's concrete minimal-experiment framing and an
  exemplar-anchored analogy rather than being circular ✓.
- **V-08**: All N6 `challenge_arguments`, the feasibility estimates, the N8 analysis plan,
  and all N9 directions are explicitly inference-level ([HYPOTHESIS]/[PLACEHOLDER]), never
  presented with extracted-level confidence; corpus-grounded statements are tagged
  [GROUNDED:corpus] with OpenReview ids ✓.
- **No fabricated numbers**: the only numbers outside [GIVEN] text are explicitly-flagged
  planning estimates (feasibility, power check) or falsification thresholds, none presented
  as results ✓.
- Every node N0–N12 present, plus Claims ✓.
