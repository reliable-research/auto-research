# Discussion Trace — B2.2 (auto-research-discussion, Stages 1-6)

> Extracted verbatim from `pipeline.md` (this content previously lived inline there). Full round-by-round critic/refiner record across all six stages for seed **B2.2** — see `pipeline.md`'s header note for run mode/provenance and its Phase Log for what happened downstream of this trace (taste audit, stage review, paper assembly, compile). See `experiment_design.md` for the standalone Stage 6 spec, and note the Stage 6 **SUPERSEDED NOTE** below: `paper.md` Step 6 is the sole binding pre-registration where its wording differs from the `rq_*` entries recorded here.

## Seed brief

- **One-sentence description:** Measure, under a fixed replay budget, how few targeted counterfactual replays suffice to localize the decisive failure step (and its plan/tool/execution layer) in a long, already-failed LLM-agent trajectory, and how much structured search (bisection over checkpoint indices, noise-tolerant group testing) saves relative to exhaustive per-step replay, uniform-random sampling, and zero-replay log-only LLM judging.
- **Apparent inputs:** a failed agent trajectory decomposed into discrete, checkpointable steps; a ground-truth decisive-failure location established either by programmatic fault injection (replay-verified) or human annotation; a replay oracle that re-executes a trajectory suffix from any checkpoint and returns the task's own pass/fail verdict; a fixed per-trajectory replay-unit budget.
- **Apparent outputs:** a predicted decisive step index and layer per (trajectory, strategy, budget) triple; per-strategy cost-accuracy curves and their summary statistics.
- **Closest research areas:** LLM-agent failure attribution (Who&When, AgenTracer, DoVer); step-level compute allocation and credit assignment (TRIM, AttnRL, iStar); fixed-budget best-arm identification theory (BAI-LD); classical delta debugging (Zeller & Hildebrandt, 2002).
- **In scope:** measuring/characterizing existing search-strategy behavior over a replay oracle for trajectories that have already failed. **Out of scope:** proposing a new localization algorithm; training a new attribution model; live, non-sandboxable deployments; multi-agent population-level dynamics.
- **Confidence: high.** As with a typical mature reverse-digest seed, the "repo" here is itself a prior digest + pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste check (`paper.md` Steps 0/2/3). Reconstruction risk is low; the risk instead is *redundancy* with `paper.md`'s own Step 6, which is why several stage-5/6 hypotheses below are framed as validating the **measurement instrument's own properties** (cost-accounting stability, monotonicity as a predictor, vote-count sufficiency) rather than re-deriving `paper.md`'s headline hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a long LLM-agent trajectory that has already failed, decomposed into discrete, checkpointable steps, and given a replay oracle that can re-execute any suffix of the trajectory from a checkpoint and return the task's own pass/fail verdict, determine — under a fixed budget of replay units — the fewest targeted replays needed to correctly identify the decisive failure step and its layer (plan, tool, or execution), and how much bisection over checkpoint indices and noise-tolerant group testing save relative to exhaustive per-step replay, uniform-random checkpoint sampling, and zero-replay log-only LLM judging.
- `input`: (1) a failed trajectory τ of n discrete steps with step-boundary checkpoints; (2) a ground-truth decisive step index and layer, established either by programmatic fault injection with replay verification or by human annotation; (3) a replay oracle that re-executes steps k..n from checkpoint k and returns the task verifier's pass/fail outcome; (4) a fixed per-trajectory replay-unit budget.
- `output`: (1) a predicted decisive step index and layer per (trajectory, strategy, budget) triple; (2) per-strategy cost-accuracy curves and their summary statistics.
- `constraints`: the trajectory must be decomposable into discrete, individually checkpointable and replayable steps; the replay oracle's pass/fail signal may be stochastic (repeated replays of the same checkpoint can disagree); replay cost is not a fixed per-probe unit but scales with how much of the trajectory suffix must be re-executed.
- `objective`: a strategy is scored by its accuracy (exact-step, tolerance, and layer) at a given replay-unit budget, compared across strategies at matched budgets.
- `study_type`: `empirical` — stated explicitly: the core question ("how few replays suffice") and digest N12 already settle this as a measurement/characterization study — "no new localization algorithm is claimed as the primary novelty (bisection and group testing are classical primitives being characterized)."

**critique:**
- summary: Strong, evidence-traceable draft, but the objective has a real evaluability gap and one framing choice presupposes something not yet established.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "'compared across strategies at matched budgets' does not say what counts as a replay unit. Bisection spends votes (repeated replays per probe) to de-noise; group testing spends redundancy instead. Whether a de-noised bisection probe and a redundant group-testing probe cost 'the same' depends entirely on the accounting choice — and digest N10/t5 and paper.md's A7 already flag that replay-unit cost may not track dollar/latency cost faithfully across accounting choices. Without naming the canonical unit up front, the headline 'how much do we save' claim is not fully evaluable as written — a different accounting axis (probe count vs. resumed-LLM-calls vs. dollar cost) could rank the same strategies differently."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'the decisive failure step' presupposes a single, well-defined culprit exists in every trajectory. That is true by construction for the fault-injected corpus (an outcome-flipping counterfactual, verified by replay) but is not guaranteed for naturally-occurring failures, which can be diffuse or multi-causal. Prefer stating 'decisive' as an explicit operational definition for the constructed corpus, with natural failures treated as a distinct, best-effort evaluation slice rather than assumed to share the same clean ground truth."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A strategy's accuracy (exact-step, ±2-step tolerance, and layer) is compared across strategies only at **matched replay-unit budgets**, where a replay unit is defined as one resumed LLM call and every probe — including repeated de-noising votes — is billed in this unit; probe count and measured dollar cost are reported as secondary accounting axes, and a strategy ranking is only reported as robust if it is stable across all three."
- `summary` (refined): "...determine — under a fixed budget of replay units, billed as resumed LLM calls — the fewest targeted replays needed to correctly identify **the decisive failure step (the earliest checkpoint whose replay outcome flips relative to the corrupted run)** and its layer..." (makes "decisive" an explicit outcome-flipping definition rather than an assumed single-culprit fact).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Trajectory τ = (s₁,...,s_n), step-boundary checkpoints c₁..c_n. `replay(k, seed)` re-executes s_k..s_n from c_k (prefix 1..k−1 fixed, served from cache) and returns the task verifier's outcome g(k) ∈ {0,1}. Decisive step d = earliest k such that `replay(k,·)` with the original action passes while the observed/injected corruption fails; layer ℓ(d) ∈ {plan, tool, execution}. Budget B = maximum replay units (resumed LLM calls, summed over all probes and de-noising votes) spendable per trajectory. Determine, for a family of localization strategies, the accuracy-vs-B curve for predicting (d, ℓ(d))."
- `changes_made`: named the canonical cost unit explicitly in `objective`; converted "decisive" from an assumed fact to an operational, outcome-flipping definition; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Counterfactual replay is the only causally verified way to attribute a long agent trajectory's failure to a specific step, but every replay re-invokes real LLM and tool calls, and current replay-based attribution systems spend that budget exhaustively — replaying one step at a time — without ever asking how few replays would have sufficed.
- `why_it_matters`: As agent trajectories grow longer, manual log inspection to find the failing step becomes prohibitively expensive and inconsistent, and the causally sound alternative — replay — is treated by existing systems purely as an offline labeling cost, spent one step at a time, i.e., linear in trajectory length. If a structured search over checkpoint indices can match that labeling accuracy in a logarithmic number of replays instead, causally verified attribution stops being an expensive offline process reserved for building training corpora and becomes cheap enough to run routinely inside an agent-development loop, every time a run fails.
- `who_cares`: Agent developers who currently either read logs manually (fast but causally unverified) or run exhaustive replay sweeps (verified but expensive) to debug a single failing run; teams building replay-based training corpora via fault-injection pipelines, who currently pay the full linear replay cost per labeled trajectory; researchers deciding whether classical bisection/group-testing search — whose textbook guarantees assume a cheap, deterministic, repeatable test — transfer to a stochastic, costly, position-dependent LLM replay oracle.
- `evidence`: `[Who&When, OpenReview:GazlTYxZss]`'s own motivation states that step-level attribution is "substantially worse" than agent-level attribution and that manual log inspection does not scale; `[AgenTracer, OpenReview:l05DseqvuD]`'s method replays "one step at a time" by construction, and no accuracy-vs-replay-budget tradeoff is characterized anywhere in its own presentation; `[DoVer, OpenReview:mrEK16Jy6h]`'s intervention-driven replay verifies whichever hypothesis an LLM proposes but runs no budget-optimal search over checkpoint indices at all.

**critique:**
- summary: Stake-specific motivation with real, traceable evidence, but coverage of stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (2) is a per-strategy *cost-accuracy curve* across an entire budget grid, not a single point estimate. why_it_matters argues that cheaper causal verification matters in general, but never explains why a full curve is needed as opposed to picking one 'good enough' budget and reporting a single number. A skeptical reader could reasonably ask: 'why not just recommend 16 replays and be done?' — that gap is real and currently unaddressed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, different teams and different failures warrant different budgets: a nightly CI run debugging a routine failure can afford only a handful of replays, while a rare production incident justifies a much larger sweep. A single recommended budget cannot serve both regimes — only a full cost-accuracy curve lets a team read off the accuracy it would get at *its own* budget, or the budget it would need for a target accuracy, which a one-shot point estimate cannot provide."
- `changes_made`: added the budget-heterogeneity argument for why the deliverable is a curve, not a point estimate.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (eight are real, corpus-grounded OpenReview papers; one, Zeller & Hildebrandt 2002, is the canonical delta-debugging reference, cited from memory as a real, verifiable IEEE TSE paper, not fabricated).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_whoandwhen` | Anon., Who&When (OpenReview:GazlTYxZss) | **true** (zero-replay judge, no-mechanism control) | Log-only attribution is causally unverified and empirically weak at step granularity; its binary-search variant searches the *log context* with an LLM judge — it never re-executes anything, so a wrong verdict costs zero replays but carries no counterfactual guarantee. |
| `rw_agentracer` | Anon., AgenTracer (OpenReview:l05DseqvuD) | **true** (exhaustive-scan accuracy ceiling) | Replays "one step at a time" for every failed trajectory — O(n) interventions, each requiring suffix re-execution — and never characterizes how few replays would have sufficed, nor any accuracy-vs-replay-budget tradeoff. |
| `rw_dover` | Anon., DoVer (OpenReview:mrEK16Jy6h) | **true** (hypothesis-then-verify comparator) | Replays from LLM-suggested intervention points and evaluates recovery, but runs no budget-optimal search over checkpoint indices and does not compare structured strategies at matched replay budgets — its evaluation targets recovery utility, not localization cost curves. |
| `rw_int` | Anon., InT (OpenReview:YAhTj2VgBw) | false (training-time use, reference-solution-dependent) | First-error localization requires a reference solution to compare against, available for math datasets but not open-ended agent tasks; its localization is judged by downstream training benefit, not localization accuracy under any query budget. |
| `rw_trim_attnrl_istar` *(shared limitation)* | TRIM (OpenReview:MoKrugWUfC), AttnRL (OpenReview:NCN8oUsiNf), iStar (OpenReview:ooROvpmxMV) | false | All three intervene *during* generation or training (per-step escalation, rollout-branch allocation, implicit step rewards from preference pairs) — none provides post-hoc localization of the decisive step in an already-failed, fixed, logged trajectory, nor cost-accuracy guarantees for that diagnostic task. |
| `rw_bailD` | Anon., BAI-LD (OpenReview:gYetLsNO8x) | false (theory, not a runnable comparator) | Analyzes fixed-budget best-arm identification over stateless arms with i.i.d. reward draws; does not model a sequence of causally ordered checkpoints with an approximately monotone query signal and position-dependent per-query cost, so its guarantees do not transfer directly to trajectory localization. |
| `rw_deltadebug` | Zeller & Hildebrandt, 2002 (IEEE TSE 28(2)) | false (canonical ancestor, cited from memory) | Classical delta debugging assumes a cheap, deterministic, arbitrarily repeatable pass/fail test; LLM-agent replay violates all three (real model/tool cost, stochastic outcomes, possible environment drift), so ddmin's minimality guarantees do not carry over unmodified. |

**critique:**
- summary: Grounding is solid and every limitation is specific, but one entry's role needs sharper justification before it can safely sit in Related Work.
- comments:
  - `{severity: major, field: "specific_related_works[rw_deltadebug]", anti_pattern: "incomplete framing (mined check, stage 3: 'Incremental engineering / integration of existing components')", comment: "Bisection over checkpoint indices closely resembles ddmin bisecting an input. Digest N12 states plainly that 'no new localization algorithm is claimed as the primary novelty' — but the draft never states *why* re-running classical bisection under a stochastic, costly, position-dependent oracle is a characterization worth publishing rather than a straightforward re-application of a 20-year-old technique. Without that sentence, a reviewer's first objection would be 'you just ran ddmin on agent logs' — the incremental-engineering kill-shot the mined checklist warns about."}`
- decision: `move_to_refiner` (a wording-precision fix — the limitation itself is accurate, but the paper's own stance toward it needs to be made explicit).

### Refiner pass

- `rw_deltadebug`'s limitation entry extended with an explicit framing note: "This paper does not propose bisection or group testing as new algorithms — digest N12 rules that out. The contribution is the *characterization*: how classical bisection/group-testing behave once every one of ddmin's three founding assumptions (cheap, deterministic, repeatable test) is violated by a real LLM replay oracle, and where (the monotonicity-violation rate) that characterization breaks down. ddmin remains the conceptual ancestor whose assumptions this paper explicitly tests, not a runnable baseline to beat."
- `changes_made`: added the explicit non-novelty framing to `rw_deltadebug`, preempting an incremental-engineering objection before it reaches Related Work prose.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is promoted to a framing-tier RQ in Stage 6 — the closest candidate (whether ddmin's assumptions actually transfer) restates this paper's own core question rather than being a distinct framing check, and is already covered end-to-end by the mechanism-tier RQs in Stage 6. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus N4's L2/L3):

- **`sp_position_dependent_cost`** — *description:* Account for replay cost fairly when the cost of a single probe is heterogeneous — replaying from an early checkpoint costs far more resumed LLM calls than replaying from a late one. *why_it_is_a_problem:* Any "savings" claim is only meaningful relative to a cost unit that reflects what a replay actually costs; a probe-count metric would silently misprice strategies that probe at different positions. *technical_challenge:* Position-dependent cost has to be billed per-invocation (resumed LLM calls), not assumed uniform, and different accounting choices (probe count vs. replay units vs. dollar cost) could rank the same strategies differently. *source_limitation_ids:* `["__novel__"]`.
- **`sp_signal_nonmonotonicity`** — *description:* Determine when the suffix-replay outcome signal is (and isn't) a clean step function of the checkpoint index, since bisection's entire logarithmic advantage depends on that structure. *why_it_is_a_problem:* If intermediate steps can partially recover from an earlier fault, the very invariant that makes bisection efficient can silently break, and a bisection search would converge to the wrong index with no warning. *technical_challenge:* Recovery probability makes the signal only *approximately* monotone; detecting and quantifying the violation requires measuring the empirical g(k) profile directly, not assuming it away. *source_limitation_ids:* `["__novel__"]`.
- **`sp_noisy_oracle_denoising`** — *description:* Decide how many repeated replays (votes) a probe needs before its pass/fail read is trustworthy, given that a single LLM replay is a stochastic Bernoulli draw. *why_it_is_a_problem:* Without de-noising, an oracle's own sampling noise is indistinguishable from a genuine signal, making any localization claim unfalsifiable. *technical_challenge:* More votes cost more replay units, so the number of votes is itself a budget trade-off, not a free correctness fix. *source_limitation_ids:* `["__novel__"]`.
- **`sp_cross_layer_attribution`** — *description:* Localize decisive failures that may span or manifest across the plan/tool/execution layer boundary, not just within one homogeneous layer of identical steps. *why_it_is_a_problem:* A search strategy that only ever partitions the index space by contiguous position may miss failures whose true cause and observable symptom sit in different layers. *technical_challenge:* Layer-crossing partitions must be defined over the whole step-index space, and it's not obvious a priori whether contiguous or layer-crossing group designs localize better, or for which layer. *source_limitation_ids:* `["__novel__"]`.
- **`sp_exhaustive_replay_uncharacterized`** — *description:* Establish, for the first time, an accuracy-vs-replay-budget characterization for counterfactual-replay-based failure attribution, since no existing replay-based system reports one. *why_it_is_a_problem:* Current systems either replay exhaustively (as an offline labeling cost) or replay only LLM-suggested hypotheses — neither asks how few replays a search strategy would need to match that accuracy. *technical_challenge:* Building this characterization requires ground truth verified independently of any one strategy (so the exhaustive scan and structured strategies can be compared on the same trajectories at matched budgets), which no cited system's evaluation currently provides. *source_limitation_ids:* `["lim_exhaustive_labeling", "lim_no_budget_search"]` *(referring to `rw_agentracer`'s and `rw_dover`'s limitations above).*

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver Stage 1's objective), but two sub-problems risk reading as the same underlying issue restated.
- comments:
  - `{severity: minor, field: "sp_signal_nonmonotonicity / sp_noisy_oracle_denoising", anti_pattern: "overlap", comment: "Both are framed as 'the replay signal isn't perfectly reliable,' which can read as the same sub-problem stated twice. They are genuinely distinct — one is a *structural* failure of the monotonicity invariant caused by intermediate recovery, the other is *sampling noise* in a single stochastic draw — but the current descriptions don't make that distinction explicit enough for a reader to see they need two different fixes."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_signal_nonmonotonicity.technical_challenge` sharpened to end with: "...this is a **systematic-bias** problem, not a sampling-noise problem — no number of repeated votes at a given checkpoint fixes it if recovery has genuinely broken the ordering; the fix, if any, is detecting and reporting the violation, not de-noising harder."
- `sp_noisy_oracle_denoising.technical_challenge` sharpened to end with: "...this is a **sampling-variance** problem distinct from the monotonicity-bias issue above — the underlying step function may be perfectly well-behaved, and a single stochastic replay can still misread it; the fix is redundancy (votes or group-testing overlap), not search-strategy redesign."
- `changes_made`: made the bias-vs-variance distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 1 sourced from two related-work limitations, 4 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_position_cost_accounting`** → targets `sp_position_dependent_cost`. *proposed_approach:* The checkpointed replay harness bills every replay in **replay units** (resumed LLM calls), logged per invocation, rather than treating "one probe" as a fixed-cost unit; probe count and measured dollar cost are logged in parallel as secondary axes. *key_insight:* A cost metric that ignores position would silently misprice any strategy that probes disproportionately early or late; billing per resumed call makes "savings" a claim about actual compute spent, not about how many search steps were taken. *hypotheses:* `["Billing replay cost in resumed-LLM-call units rather than raw probe count shows that structured strategies' cost advantage over exhaustive per-step scanning is largest specifically for late-decisive-step trajectories, where per-probe replay units are cheapest to begin with — i.e., the replay-unit savings are not uniform across where the decisive step falls."]`
- **`m_bisection_localizer`** → targets `sp_signal_nonmonotonicity`. *proposed_approach:* Binary search over checkpoint indices using the end-of-task suffix-replay predicate g(k); at each probe, the empirical g-profile is logged in full (not just the final answer), so the monotonicity-violation rate can be computed directly per trajectory. *key_insight:* The bisection invariant is only as good as the monotonicity assumption behind it; measuring the violation rate turns a silent failure mode into a reported, falsifiable diagnostic rather than an unstated risk. *hypotheses:* `["Bisection reaches at least 90% of the exhaustive per-step scan's exact-step localization accuracy while consuming at most 25% of its replay-unit cost, on trajectories whose empirical g(k) profile is monotone.", "Trajectories whose empirical g(k) profile violates monotonicity show bisection's accuracy advantage over uniform sampling shrink to within 5 percentage points, demonstrating that the monotonicity-violation rate is the load-bearing predictor of where the bisection shortcut works."]`
- **`m_vote_denoising`** → targets `sp_noisy_oracle_denoising`. *proposed_approach:* Each probe is de-noised by majority vote over r repeated replays, with r swept as an explicit experimental factor (r ∈ {1,3,5}) rather than fixed by assumption. *key_insight:* Treating vote count as a first-class budget parameter turns "is the oracle noisy enough to matter" from an assumption into a measured quantity. *hypotheses:* `["r=3 repeated replays per probe stabilize bisection's localization accuracy to within 3 percentage points of r=5, at sampling temperature approximately 0.7 — the marginal value of de-noising past r=3 is small."]`
- **`m_group_testing_crossover`** → targets `sp_cross_layer_attribution`. *proposed_approach:* Adaptive group testing partitions the step-index space (contiguous or layer-crossing designs), tests groups via multi-step interventions with built-in redundancy, and refines within the implicated group. *key_insight:* Redundancy across groups is the standard combinatorial mechanism for tolerating a noisy oracle, and defining partitions over the whole index space (not just contiguous runs) lets attribution cross layer boundaries the way bisection alone cannot. *hypotheses:* `["There exists a single-replay flip rate (oracle noise level) above which group testing's accuracy-per-replay-unit exceeds vote-multiplied bisection's, demonstrating that redundancy is a more efficient de-noising mechanism than repeated bisection probes once oracle noise crosses that threshold.", "Layer-crossing group-testing partitions outperform contiguous-only partitions by at least 5 percentage points specifically on plan-layer decisive failures, because plan-layer failures are the ones most likely to manifest through a downstream tool or execution step rather than locally."]`
- **`m_budget_matched_baseline_suite`** → targets `sp_exhaustive_replay_uncharacterized`. *proposed_approach:* Run the fault-injected corpus (balanced across layers, replay-verified ground truth) through all strategies — bisection, group testing, uniform sampling, exhaustive scan, zero-replay judge, and hypothesis-then-verify — on the same trajectories at the same budget grid, for the first head-to-head cost-accuracy comparison of its kind. *key_insight:* A characterization is only informative if every strategy is compared on identical trajectories and budgets; no cited system's own evaluation provides this shared comparison. *hypotheses:* `["At a replay budget of one-quarter the trajectory length, both bisection and group testing exceed budget-matched uniform sampling's exact-step accuracy by at least 15 percentage points, and the zero-replay log-only judge sits at least 20 percentage points below the best structured strategy — establishing that both index structure and replay access, not just budget spend, are doing real work."]`

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold, but one method carries two headline claims and needs a one-line justification for why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_group_testing_crossover.hypotheses", anti_pattern: null, comment: "The noise-crossover hypothesis and the layer-crossing-design hypothesis are two distinct, separately falsifiable claims bundled under one method. Worth stating explicitly why one mechanism produces both, so this doesn't read as scope creep folded into a single method entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_group_testing_crossover.key_insight` extended: "...the same group-testing mechanism — redundant, configurable-partition group tests — yields two separately falsifiable readouts from one design: sweeping the noise/flip-rate axis at a fixed (contiguous) partition tests the crossover-over-bisection hypothesis, and sweeping the partition design (contiguous vs. layer-crossing) at a fixed noise level tests the layer-crossing-design hypothesis. One instrument, two orthogonal readouts, not two mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **7 hypotheses total** (1 + 2 + 1 + 2 + 1 across the five methods respectively), mixing instrument-validity claims (cost accounting, vote sufficiency) with the study's headline empirical predictions (bisection ceiling, structured-vs-uniform-vs-judge) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

> **SUPERSEDED NOTE (2026-07-04, post adversarial design review — `discussion/design_review.md`):** `paper.md` Step 6 is the **sole binding pre-registration**. Where the seven `rq_*` wordings below (and their copies in `paper_draft.md`) differ materially from paper.md's H1–H4 — notably `rq_bisection_ceiling`'s monotone-subset restriction vs. H1's pooled criterion — **paper.md governs**; see paper.md Step 6's "Registration of record" for the explicit rq_*↔H\* mapping. `rq_monotonicity_predictor` and `rq_position_dependent_savings` are descriptive analyses (A3/F1 and A7 respectively), not confirmatory hypotheses. The Stage 6 record below is retained as discussion-loop history, not as a registration.

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check/isolation comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- ALFWorld (deterministic household-task simulator) — *justification:* fully deterministic re-execution, so replay reproducibility can be gated at ≥95% before any strategy comparison; pilot-stage domain.
- Who&When human-annotated failure logs — *justification:* the natural-failure evaluation slice, re-hosted in the replay harness where re-executable, exposing any gap between injected-fault and natural-failure localization accuracy.
- (draft initially listed GAIA cached-web subset with justification only "digest mentions it as a scale-up domain" — flagged below.)

`baselines` (sanity-check/isolation comparators, not outcome-tier competitors):
- Uniform-random checkpoint sampling, budget-matched — isolates whether any advantage comes from the *index structure* bisection/group testing use, or merely from having replay access and spending a budget at all.
- Exhaustive per-step counterfactual scan — the accuracy ceiling, not a competitor to beat.
- Zero-replay log-only LLM judge (Who&When-style) — the no-mechanism control: if it matches replay-based accuracy, the entire replay enterprise is unjustified.
- DoVer-style hypothesis-then-verify — checks whether LLM-proposed hypotheses plus verification match a budget-blind structured search.

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_position_dependent_savings` | `sp_position_dependent_cost` | "Billing replay cost in resumed-LLM-call units rather than raw probe count shows that structured strategies' cost advantage over exhaustive per-step scanning is largest specifically for late-decisive-step trajectories, where per-probe replay units are cheapest to begin with — i.e., the replay-unit savings are not uniform across where the decisive step falls." |
| `rq_bisection_ceiling` | `sp_signal_nonmonotonicity` | "Bisection reaches at least 90% of the exhaustive per-step scan's exact-step localization accuracy while consuming at most 25% of its replay-unit cost, on trajectories whose empirical g(k) profile is monotone." |
| `rq_monotonicity_predictor` | `sp_signal_nonmonotonicity` | "Trajectories whose empirical g(k) profile violates monotonicity show bisection's accuracy advantage over uniform sampling shrink to within 5 percentage points, demonstrating that the monotonicity-violation rate is the load-bearing predictor of where the bisection shortcut works." |
| `rq_vote_stabilization` | `sp_noisy_oracle_denoising` | "r=3 repeated replays per probe stabilize bisection's localization accuracy to within 3 percentage points of r=5, at sampling temperature approximately 0.7 — the marginal value of de-noising past r=3 is small." |
| `rq_noise_crossover` | `sp_cross_layer_attribution` | "There exists a single-replay flip rate (oracle noise level) above which group testing's accuracy-per-replay-unit exceeds vote-multiplied bisection's, demonstrating that redundancy is a more efficient de-noising mechanism than repeated bisection probes once oracle noise crosses that threshold." |
| `rq_layer_crossing_design` | `sp_cross_layer_attribution` | "Layer-crossing group-testing partitions outperform contiguous-only partitions by at least 5 percentage points specifically on plan-layer decisive failures, because plan-layer failures are the ones most likely to manifest through a downstream tool or execution step rather than locally." |
| `rq_structure_vs_uniform_and_judge` | `sp_exhaustive_replay_uncharacterized` | "At a replay budget of one-quarter the trajectory length, both bisection and group testing exceed budget-matched uniform sampling's exact-step accuracy by at least 15 percentage points, and the zero-replay log-only judge sits at least 20 percentage points below the best structured strategy — establishing that both index structure and replay access, not just budget spend, are doing real work." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed sample sizes, budget grid, and statistical tests as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[GAIA cached-web subset]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it as a scale-up domain' says nothing about which RQ needs it or why. ALFWorld is a deterministic simulator with no real tool-call variability — a dataset is needed that stresses the layer-crossing and structure-vs-uniform claims under genuine tool-use conditions, not just a second domain for its own sake."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "GAIA cached-web subset (tool-use tasks, cached/snapshotted web content for deterministic replay) — *justification:* introduces tool-layer failures with real (though cached) tool-call variability absent from ALFWorld's deterministic household simulator, letting `rq_layer_crossing_design` and `rq_structure_vs_uniform_and_judge` be tested under a genuine tool-use environment rather than only a synthetic simulator, and stressing whether the structured-replay advantage generalizes beyond one domain's step semantics."
- `changes_made`: gave GAIA's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (bisection/group testing first appear in Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_exhaustive_replay_uncharacterized.source_limitation_ids = ["lim_exhaustive_labeling", "lim_no_budget_search"]` ∈ Stage 3 limitations (`rw_agentracer`, `rw_dover`) ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's two outputs (predicted step/layer per strategy-budget, and per-strategy cost-accuracy curves) are each reachable: the predicted-label output via `sp_signal_nonmonotonicity` + `sp_cross_layer_attribution` + `sp_noisy_oracle_denoising`, the cost-accuracy curve via `sp_position_dependent_cost` + `sp_exhaustive_replay_uncharacterized` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, and every baseline is explicitly labeled a sanity-check/isolation comparator, never a "beat baseline X" claim.

**What was hardest:** as with a mature seed, the recurring tension was **not disagreement about facts** but **scope discipline and terminological precision** — repeatedly separating claims that sound alike (monotonicity-bias vs. oracle-variance; probe count vs. replay-unit cost) and making sure a stage-5/6 hypothesis added something the schema specifically demands (e.g., the position-dependent cost-accounting claim, which `paper.md`'s own Assumptions section (A7) gestures at as a risk but never states as a falsifiable hypothesis in its own right).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Revision pass over the review artifacts (`stage_review.md`, `taste_audit.md`, `design_review.md`). Every finding in those files was enumerated and its status checked against the current deliverables; historical rounds above are untouched. Findings already applied and logged in `pipeline.md` are listed summarily; only the residual items produced new edits.

**Already applied before this pass (verified present in the current deliverables, no action needed):**
- `stage_review.md` Stage 2 REVISE (nearest-neighbor sentence naming AgenTracer/DoVer) → present in `paper_draft.md`/`.tex` Related Work opening.
- `stage_review.md` Stage 4 REVISE (per-RQ falsification conditions) → present in all 7 RQ subsections of `paper_draft.md`/`.tex` and `experiment_design.md`.
- `stage_review.md` Phase A items 2, 5(a–c), 6.1, 6.9 (reference-cache grounding records; H1/H2/H4 Aggregation slots; A1–A7 gate/consequence columns; A8+PG-4 R2 mini-plan; Step 1 estimand; per-layer power statement) → all present in `paper.md`; the 5 load-bearing null-digest records were subsequently given real PDFs/digests in the 2026-07-04 resume run.
- `stage_review.md` Phase G Findings 1–4 (RQ2 monotone-subset registration drift; missing H1/H2/H3 aggregation rules; RQ1/RQ3 descriptive registration-status notes; RQ5 p-axis support pre-condition) → present in `paper_draft.md`/`.tex` and mirrored in `experiment_design.md`.
- `stage_review.md` Phase G Finding 5 (BAILD2025 venue/year metadata) → fixed in `reference_candidates.jsonl`/`refs.bib`.
- `design_review.md` F1–F4, F6–F9, F11, F12 → applied to `paper.md` per its own "Fixes applied (2026-07-04)" log (B0a/B0b split; R3 confound note + F-G2; registration of record; widened full-negation fallbacks with sub-cases; H3 ≥2-of-adequately-powered-layers rule; H4 α/Holm/p-axis pre-condition + mixed-conjunct rule; skeleton smoke arms; M5d reporting rule; PG-2 stratum-loss rule; Claim-map relabeling), and carried into `experiment_design.md` and (per Phase G) `paper_draft.*`.
- `design_review.md` F10 (method-twin digests + targeted sweep) → closed by the 2026-07-04 resume run (real PDFs/digests for WhoWhen2025, AgenTracer2025, DoVer2025, BAILD2025, ZellerHildebrandt2002; freshness sweep found and correctly classified CausalAgentReplay2606 as adjacent).
- `taste_audit.md` → 🟢 both in the initial audit and the §7 post-Phase-G re-audit; no open taste findings.

**Applied in this round (3 residual cross-deliverable gaps, all splices from `paper.md`'s registration wording — no new content invented):**
1. `design_review.md` F1 / `experiment_design.md` Baselines vs. `paper_draft.*` → the B0b null-by-construction placebo (label-shuffle + sham-injection run-validity gate) existed in `paper.md`'s Mandatory baselines and `experiment_design.md` but was absent from `paper_draft.md`/`.tex` entirely. Added a B0b sentence to the Experimental Setup Baselines paragraph in both files, quoting `paper.md`'s wording (chance-band requirement; sham arm must read "no fault"; non-null B0b = artifact = run invalid, scored before any H*).
2. `design_review.md` F7 (H4 α/multiplicity) → `paper.md` H4 and `experiment_design.md` RQ4/RQ5 carry the α=0.05 Holm split across H4's two conjuncts (per-conjunct α=0.025), but `paper_draft.*`'s RQ4/RQ5 Setups did not. Added the conjunct mapping (RQ4 = H4 conjunct (i), RQ5 = H4 conjunct (ii)) and the per-conjunct α=0.025 to both RQ Setups in `paper_draft.md` and `.tex`.
3. Same item, RQ5 CI spec → `paper_draft.*`'s RQ5 said only "a bootstrap confidence interval"; aligned to the registered "95% bootstrap CI (1,000 resamples), required to exclude 'no crossover within the observed flip-rate range'" in both files.

**Deferred / rejected (with reasons):**
- `stage_review.md` Phase G Finding 6 (refs.bib entries lack author fields) — rejected for this pass: the canonical `reference_candidates.jsonl` schema has no author field, several selected records (e.g. CausalAgentReplay2606, DoVer2025) have no author metadata cached anywhere locally, and fabricating author lists is prohibited; remains the logged schema-change to-do for the next Phase F touch (already recorded in `pipeline.md`'s resume point).
- `design_review.md` F2/F5 constructive halves (build the propensity-sampled fault mode; count natural-slice re-hosting feasibility) — rejected — blocked on pilot compute (Phase B); the prose halves are already applied (R3 confound note licenses Claim 1/7 as injected-corpus-only; F-G2 pre-commits the non-replayable-slice pivot; Claim 7/8 scope-bounded).
- `design_review.md` "Missing RQs / reviewer questions" items 1, 4, 5, 6 (length-scaling stratum; harness-overhead accounting; multi-fault probe; verifier-reliability assumption) — rejected — design_review's own triage classifies these as "reviewer-question backlog, optional pre-B additions" needing a human design decision; adding new registered criteria in a revision pass would violate `paper.md`'s "no criterion may exist in two materially different versions" rule. Note item 1 is partially moot: `paper_draft.*` makes no Θ(log n / n) scaling claim in the abstract and its "Further evaluation" paragraph explicitly scopes longer trajectories out.

**Cross-consistency verification (task item 6):** RQ count 7 (5 confirmatory + 2 descriptive) consistent across `paper_draft.md`, `experiment_design.md`, and `paper.md`'s rq_*↔H* map; effect floors/margins consistent (H1 90%/25%, falsified at ≥50%-for-within-5-pts; H2 15 pts vs. uniform, 20 pts vs. judge at B=n/4; H3 10 pts per layer + 5 pts layer-crossing at α=0.017, power 65–70%, ≥2-of-adequately-powered rule; H4 r=3-within-3-pts-of-r=5, p ≥ 15% crossover, per-conjunct α=0.025); target hypotheses in `experiment_design.md` remain byte-identical to their `paper.md`/Stage-5 sources (untouched by this pass). The only mismatches found were the three listed above, now fixed in `paper_draft.md`/`.tex`.
