# Discussion Trace — B4.1 (Auto-Research-Discussion Run, Stages 1–6)

> Extracted verbatim from `pipeline.md` (which previously held this content inline) on 2026-07-05, per the updated `auto-research-discussion` SKILL.md's three-artifact deliverable spec. No content below was regenerated or altered from the original run — see `pipeline.md`'s Phase Log for post-Stage-6 pipeline history (Phases A, E–I) and `experiment_design.md` for the standalone Stage 6 spec.

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B4.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material is unusually mature (`paper.md` already contains a formal notation table, seven pre-registered binary hypotheses with pre-committed fallback wording, a walking skeleton with an explicit pass/fail gate, and its own Step-3 taste self-audit), so genuine disagreement surfaced at the level of evaluability gaps and instrument-validity framing, not at the level of missing content.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and a missing corpus-quality/verifier-audit paragraph in Experimental Setup, required by this paper's *secondary* Resource archetype) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure the *regret* — the accuracy-minus-compute utility gap — that practical online stopping rules (confidence-, entropy-, and self-consistency-based) incur relative to a per-instance oracle stopping policy reconstructed offline from a fully probed reasoning trajectory, on tasks whose answers can be mechanically verified.
- **Apparent inputs:** a step-wise reasoning trajectory segmented at reasoning-transition checkpoints; per-checkpoint online signals (confidence, entropy, self-consistency vote share); a mechanical verifier; an accuracy–compute exchange rate λ.
- **Apparent outputs:** a per-checkpoint stop/continue decision per rule; a λ-swept, difficulty-conditioned regret curve per rule; an estimated marginal utility of continuing at each checkpoint; a released corpus of verifier-labeled trajectories.
- **Closest research areas:** training-free test-time stopping/early-exit for LLM reasoning (DEER, TrimR); self-consistency/agreement-based adaptive sampling (CaTS, Best-of-∞); RL-trained overthinking suppression (JET); pre-decoding compute allocation (Adaptive Thinking, Snell et al. 2024 compute-optimal scaling); theoretical accounts of chain-of-thought length (CoTLength).
- **In scope:** measuring existing stopping heuristics' distance from an oracle on mechanically verifiable reasoning tasks; a learned combination of existing online signals evaluated the same way. **Out of scope:** open-ended tasks with no mechanical verifier; training or fine-tuning the underlying reasoning model itself; frontier-scale proprietary models beyond one API reasoning model.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`), already internally cross-referenced (N-node ↔ M-component ↔ H-id) and already carrying its own asymmetry/taste self-check (`paper.md` Steps 0/3). The risk is not under-specification but *redundancy* with `paper.md`'s own Step 6 hardening — Stage 5/6 below are framed to add genuinely new structure (instrument-validity hypotheses, an explicit sub-problem decomposition, and RQ-level falsification conditions) rather than re-deriving `paper.md`'s own binary criteria verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a reasoning trajectory for a mechanically-verifiable task instance, segmented into checkpoints, and given at each checkpoint a per-checkpoint accuracy estimate and a cumulative token cost, determine — for a bank of online stopping rules that decide when to stop using only signals available up to that point — the *regret*: how much accuracy-minus-compute utility each rule forfeits relative to the per-instance oracle stopping point, as a function of task difficulty and the accuracy–compute exchange rate λ.
- `input`: (1) a per-instance reasoning trajectory segmented into K checkpoints; (2) at each checkpoint, a per-checkpoint accuracy estimate and cumulative token cost; (3) a mechanical verifier; (4) a grid of accuracy–compute exchange rates λ; (5) a bank of candidate online stopping rules, each observing only signals at or before its stopping checkpoint.
- `output`: (1) a stop/continue decision per rule per checkpoint; (2) a per-instance, per-λ regret value for each rule relative to the oracle stopping point; (3) regret curves aggregated by task difficulty and by λ; (4) an estimate of the signed marginal utility of continuing at each checkpoint.
- `constraints`: the task must be mechanically verifiable so that a correctness label — and hence an oracle stopping point — exists for every checkpoint of every instance; the oracle is itself a reconstruction, not a directly observed ground truth, and its reconstruction may carry its own estimation noise.
- `objective`: a rule's regret is characterized only relative to the oracle at each tested λ value; a single-λ regret number does not, on its own, characterize a rule.
- `study_type`: `empirical` — stated explicitly, matching digest N12's own tie-break rationale ("a regret characterization of an existing phenomenon... the defining shape of an empirical study"), not silently inferred.

**critique:**
- summary: The draft is tightly evidence-traceable to `paper.md`'s Step 5 formal table, and the four-part output list is complete — but the objective has a real evaluability gap, and the summary quietly treats a constructed reference as unconditional ground truth.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective says regret must be checked at each λ, but never says what happens when the measured regret is smaller than the oracle-reconstruction's own noise. Digest assumption A3 states the oracle is built from only N=8 verifier-checked probes per checkpoint, carrying binomial noise 'up to ±0.17 (1 s.e.)' that 'propagates into both t* and measured regret' — so a regret number that is merely nonzero is not yet evidence of a rule's failure; it could be the instrument's own noise floor. As written, the objective has no way to rule that out, so two different rules' regret readings are not comparably evaluable."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'the per-instance oracle stopping point' reads as if the oracle were a directly observed ground truth. It is a *reconstruction* — built from a finite number of counterfactual probes — and per digest A3/A5 that reconstruction itself needs validating (is it non-trivial? is it precise?) before it can license any regret claim. Prefer language that keeps the oracle's own constructedness visible."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest — no new content needed).

### Refiner pass

- `objective` (refined): "A rule's regret at exchange rate λ is accepted as characterized only if it is measured against the reconstructed oracle at that λ **and** the measured regret significantly exceeds the instrument's own reconstruction-noise floor — established by comparing the oracle reconstructed from disjoint halves of the same checkpoint's probes. A regret value that cannot be distinguished from this noise floor is reported as *inconclusive*, not attributed to the rule."
- `summary` (refined): "...determine — for a bank of online stopping rules... — the regret each rule incurs relative to a **reconstructed reference stopping point** (the oracle), itself subject to its own quantifiable reconstruction noise, as a function of task difficulty and the accuracy–compute exchange rate λ."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Instance x, mechanical verifier v(·)∈{0,1}. Trajectory segmented into checkpoints k=1..K. At each checkpoint, a probe-estimated accuracy â_k∈[0,1] and cumulative cost c_k are available. Utility of stopping at k: U_λ(k) = â_k − λ·c_k. Oracle checkpoint t*(x,λ) = argmax_k U_λ(k). A rule r observing only signals at indices ≤ t_r stops at t_r(x); its regret is R_λ(r,x) = U_λ(t*) − U_λ(t_r) ≥ 0. Determine the distribution of R_λ(r,x) over instances, its dependence on task difficulty and λ, and whether it exceeds the noise floor of t* itself."
- `changes_made`: tightened `objective`'s evaluability condition to require exceeding a stated noise floor; rephrased `summary` to keep the oracle's constructedness explicit; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: A growing family of test-time stopping mechanisms for LLM reasoning — confidence-based early exit, verifier-based trimming, agreement-threshold adaptive sampling — is evaluated only by end accuracy and token savings, never by how far each one falls short of the best a deployer could achieve if the future were known; without that distance, nobody can say how much headroom is actually left to capture.
- `why_it_matters`: If a stopping rule's regret against the achievable frontier is unmeasured, a deployer who fixes a stopping policy has no way to tell a "nearly-optimal, not worth touching further" rule from a "leaves most of the achievable headroom on the table" rule — two situations that call for opposite next actions (ship it vs. keep iterating) but currently look identical from an accuracy/token-savings report alone.
- `who_cares`: Practitioners deploying test-time reasoning under a real inference budget (API cost ceiling or latency SLA) who must pick or tune a stopping rule; researchers proposing new stopping heuristics, who currently have no common yardstick for "how much better than rule X, relative to what's achievable"; downstream users of the released trajectory corpus who want to score a future rule without re-running any model.
- `evidence`: `[CaTS, OpenReview:jrSc4RJXy1]`'s own motivation concedes that agreement-threshold stopping criteria "are not direct estimates of correctness and may not transfer cleanly across tasks or models" — an acknowledged proxy problem with no quantified size; `[DEER, OpenReview:NpU7ZXafRi]` and `[TrimR, OpenReview:ofEkphaqg7]` both report accuracy and token-savings numbers for their exit rules but neither scores its rule against a per-instance oracle, so neither can say how much of the achievable accuracy–compute frontier its heuristic actually recovers.

**critique:**
- summary: Well-grounded and specific, but coverage of stage 1's outputs is incomplete in one respect that matters for this paper's central design choice.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a regret curve *as a function of λ*, not a single number. why_it_matters argues why regret matters at all, but never explains why a deployer needs the whole λ-swept, decomposed curve rather than one aggregate 'token savings at matched accuracy' figure — which is exactly what today's stopping-rule papers already report. Without that argument, a reader could reasonably ask 'why not just report one number at one operating point, like everyone else does,' and the draft has no answer."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a single aggregate number is not enough, because which rule looks best can flip with the deployer's own exchange rate: a lab with cheap, abundant compute (low λ) and a metered API consumer (high λ) can be handed the same set of accuracy/token-savings tables today and reasonably disagree about which rule to adopt, with neither report telling them whether that disagreement is expected or an artifact of an unrepresentative operating point. A λ-swept, difficulty-decomposed regret curve — rather than a single scalar — is what lets a deployer read off the answer at *their own* exchange rate and tells a rule designer whether a claimed improvement is a robust, exchange-rate-independent property of the rule or an accident of the one operating point it was measured at."
- `changes_made`: added the argument for why the λ-swept, decomposed measurement (not a scalar) is the necessary output form.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier**, following digest N3's own full-text-level engagement — except Snell et al. 2024, which digest N3 itself flags as `[HYPOTHESIS-CANONICAL: non-corpus]` (not retrieved from the local OpenReview corpus, lower confidence), so it is kept in `general_related_works` rather than the deep tier, per the no-overclaiming-confidence rule in `stages.md`.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_deer` | Anon., DEER (OpenReview:NpU7ZXafRi) | **true** | Exits on a single-trace confidence threshold at a transition checkpoint, scored by end accuracy and token savings; never scored against a per-instance oracle, so it cannot say how much achievable utility its threshold leaves unrecovered. |
| `rw_jet` | Anon., JET (OpenReview:2u5ZRzDyS0) | false (requires RL training access) | Trains the policy itself to stop via a length-reward; cannot be replayed offline to score a fixed black-box model's stopping behavior, and measures learned performance, not the regret of a given rule. |
| `rw_cats` | Anon., CaTS (OpenReview:jrSc4RJXy1) | false (requires distillation/fine-tuning) | Distills self-consistency agreement into a trained confidence head; its own motivation concedes the underlying agreement signal "may not transfer cleanly," but no analysis quantifies the residual regret of acting on that proxy relative to an oracle. |
| `rw_bestofinf` | Anon., Best-of-Infinity (OpenReview:3qiCnLf3jf) | false (I/O mismatch — parallel sampling, not sequential trace) | Characterizes only the *parallel* dimension (how many i.i.d. samples to draw for majority vote); its Bayes-factor stopping rule and its infinite-sample reference point both concern population agreement, not a single sequential trace's accuracy-per-compute oracle. |
| `rw_trimr` | Anon., TrimR (OpenReview:ofEkphaqg7) | **true** | Stops on consecutive-segment answer-stability; like DEER, evaluated by accuracy/token-savings only, with no oracle-relative regret reported. |
| `rw_adaptivethinking` | Anon., Adaptive Thinking (OpenReview:2i6Rp0gCq6) | **true**, but see refiner note | Predicts expected self-consistency from pre-decoding hidden state and allocates compute *before* generation begins; cannot exploit — or evaluate the value of — evidence that only appears mid-trajectory. |
| `rw_cotlength` | Anon., CoTLength (OpenReview:6QDFsYxtI1) | false (theoretical account, not an implementable rule) | Derives a population-level optimal chain length from an error-accumulation model; predicts the inverted-U shape but supplies no online, per-instance estimator and no evaluation of how far observable signals are from realizing that optimum. |
| `rw_safer` | Anon., SAFER (OpenReview:kJmLmOvwLC) | false (different problem: offline global budget, not online per-instance stopping) | Conformal risk-control calibrates one global sampling budget with abstention from a calibration set; does not estimate per-instance marginal utility online, and its exchangeability requirement doesn't hold for per-step reasoning signals. |
| `rw_firstimpression` | Anon., First Impression (OpenReview:2PP70tFY0S) | false (diagnostic, not a decision rule) | Shows a model's pre-reasoning "internal bias" causally triggers overthinking, but supplies no decision-theoretic account — it diagnoses a cause of poor stopping, not a stopping policy or its regret. |
| `rw_snell` *(general tier)* | Snell et al., 2024 (arXiv:2408.03314) | false (landscape/canonical; not retrieved from corpus) | Shows compute-optimal allocation across strategies depends on predicted difficulty; treated here as background for the pre-decoding-sufficiency rival explanation, not as a deep-engaged work. |

**critique:**
- summary: Grounding is solid and every deep-tier limitation is specific, but one baseline label overstates what a straightforward "beat this number" comparison would mean.
- comments:
  - `{severity: major, field: "specific_related_works[rw_adaptivethinking].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Adaptive Thinking's I/O framing is pre-decoding (a single allocation decision made before any token is generated) — genuinely different from this paper's per-checkpoint, mid-trajectory framing. Per the stage-3 rubric, an I/O-mismatched work is 'not a baseline — at best a method-side reference.' Marking it a plain baseline risks implying this paper compares against Adaptive Thinking's own reported numbers, which it does not; what's actually borrowed is the *rival explanation it implies* (pre-decoding difficulty prediction might already capture everything mid-trajectory signals would add)."}`
- decision: `move_to_refiner` (a wording-precision fix, not a structural one — the *rival-explanation control* built from this work is still legitimate and, per Stage 4/5 below, becomes its own sub-problem and method).

### Refiner pass

- `rw_adaptivethinking.is_potential_baseline` retained as `true`, but sharpened: "Not a baseline in the beat-a-number sense — Adaptive Thinking's own reported numbers are not compared against. Its **pre-decoding difficulty-prediction premise** is borrowed as the rival explanation for a dedicated control (a capacity-matched, pre-decoding-only predictor), isolating whether mid-trajectory signals add anything beyond what is already predictable before generation starts."
- `changes_made`: clarified Adaptive Thinking's role to avoid an implied I/O-mismatched head-to-head comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The closest candidate for a framing-tier RQ (`rw_adaptivethinking`'s limitation — "does pre-decoding difficulty prediction already capture what mid-trajectory signals would add?") is not left as an independent framing check; it is instead promoted directly into a dedicated sub-problem and method (Stage 4/5's `sp_predecoding_confound` / `m_predecoding_control`) with its own mechanism-tier hypothesis. Per `stages.md`'s "if nothing was flagged, emit zero framing-tier RQs — don't manufacture one," a redundant framing-tier RQ testing the same claim a mechanism-tier hypothesis already tests would double-count evidence rather than add coverage.

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus one sourced from a Stage-3 limitation):

- **`sp_oracle_construction`** — *description:* Make the per-instance oracle stopping point — a functional of the trajectory's unobserved future — into a computable quantity, and establish that the resulting reconstruction is both non-trivial and precise enough to trust. *why_it_is_a_problem:* every regret claim downstream is only as meaningful as the reference it's measured against; if the oracle is degenerate (always the last checkpoint) or too noisy to distinguish from any rule's regret, no comparison downstream is interpretable. *technical_challenge:* the oracle is defined over a genuinely unobserved counterfactual future, and any reconstruction of it from a finite number of probes carries its own sampling noise that must be measured, not assumed away. *source_limitation_ids:* `["__novel__"]` (derived directly from digest C1, not from any single related work's limitation — none of the cited rules attempts to reconstruct an oracle at all).
- **`sp_signal_reliability`** — *description:* Determine where and how much each online signal (confidence, entropy, self-consistency) decouples from actual verifier-checked correctness, rather than reporting only an aggregate regret number. *why_it_is_a_problem:* a single aggregate regret figure cannot distinguish "this signal is uniformly a little off" from "this signal is confidently wrong in a specific, concentrated way" — and only the latter is actionable. *technical_challenge:* decoupling has to be *localized* (by checkpoint, by direction of error) using the same logged data the regret figure comes from, not inferred from the aggregate alone. *source_limitation_ids:* `["__novel__"]` (digest C2, sharpened beyond any one cited work's limitation — DEER/TrimR/CaTS each use a different single signal but none localizes its own failure mode).
- **`sp_utility_nonstationarity`** — *description:* Build an estimator of the *signed* marginal utility of continuing, since continuing can have negative value (overthinking flips correct answers to incorrect), rather than relying on one global fixed threshold. *why_it_is_a_problem:* if marginal utility can be negative and non-monotone, no single threshold on any one signal can be optimal across tasks, difficulties, or trajectory positions — a structural limitation of every threshold-based rule in the literature. *technical_challenge:* the estimator has to combine a running signal history into a directional (continue-helps vs. continue-hurts) prediction, not just a stop/continue binary from the current checkpoint alone. *source_limitation_ids:* `["__novel__"]` (digest C3, grounded in `[CoTLength, OpenReview:6QDFsYxtI1]`'s inverted-U finding but not itself addressed by that or any other cited work).
- **`sp_exchange_rate_dependence`** — *description:* Determine whether conclusions about which stopping rule is best, and where regret concentrates, are stable across the accuracy–compute exchange rate λ, or whether they are an artifact of whichever λ happens to be reported. *why_it_is_a_problem:* λ is a free parameter of the evaluator, not of the phenomenon; if rule rankings reorder across plausible λ values, then no single reported comparison in the literature is defensible without disclosing its λ. *technical_challenge:* this is a **robustness-to-a-free-parameter** problem, distinct from constructing the oracle itself — even a perfectly reconstructed, noise-free oracle at one λ would say nothing about ranking stability across λ; that requires sweeping λ and measuring rank agreement directly. *source_limitation_ids:* `["__novel__"]` (digest C4).
- **`sp_predecoding_confound`** — *description:* Isolate whether an online rule's apparent value comes from genuinely exploiting mid-trajectory evidence, or merely from implicitly re-deriving a difficulty estimate that was already available before decoding began. *why_it_is_a_problem:* if pre-decoding difficulty prediction already captures everything a mid-trajectory rule adds, then "online marginal-utility estimation" during generation is not doing any real work beyond what a much cheaper pre-decoding predictor already does. *technical_challenge:* difficulty and mid-trajectory signal content are naturally correlated (harder instances also tend to produce noisier mid-trajectory signals), so isolating the two requires a capacity-matched control restricted to pre-decoding features alone, evaluated at matched token expenditure — not just a correlation check. *source_limitation_ids:* `["rw_adaptivethinking"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's objective and output list), but two sub-problems risk reading as the same underlying concern about the oracle.
- comments:
  - `{severity: minor, field: "sp_oracle_construction / sp_exchange_rate_dependence", anti_pattern: "overlap", comment: "Both sub-problems involve the λ-parameterized oracle t*(x,λ), which can read as one sub-problem stated twice. They are genuinely distinct — one is about whether the oracle can be *constructed and trusted at all* (an existence/precision problem), the other about whether *conclusions drawn from it* survive varying its one free parameter (a robustness/reporting problem) — but the descriptions don't make that distinction sharp enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_oracle_construction.technical_challenge` sharpened to end with: "...this is a **constructibility and precision** problem — can the reference be built at all, and is it precise enough to trust — independent of what λ value is later chosen."
- `sp_exchange_rate_dependence.technical_challenge` sharpened to end with: "...this is a **robustness-to-a-reporting-choice** problem distinct from whether the oracle can be built — even a flawlessly constructed, zero-noise oracle at a single λ says nothing about whether the resulting rule ranking would survive a different, equally defensible choice of λ; the fix is sweeping λ and measuring agreement, not building a better oracle."
- `changes_made`: made the constructibility-vs-robustness distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 4 `__novel__` with stated decisive-component justifications, 1 sourced from a Stage-3 limitation).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_checkpoint_probing_instrument`** → targets `sp_oracle_construction`. *proposed_approach:* Segment each trajectory at reasoning-transition checkpoints; at each checkpoint, branch N counterfactual probes to a trial answer, verifier-label each, and use the resulting per-checkpoint accuracy/cost estimates to reconstruct t*(x,λ) over a λ grid; independently reconstruct the oracle from two disjoint halves of the same probes to measure the reconstruction's own noise floor. *key_insight:* the oracle's unobservability is a fact about the future, not about the offline record — once the future has been probed and verifier-labeled after the fact, the "unobservable" oracle becomes an ordinary, checkable statistic, and the same split-half trick that estimates it can also certify how much to trust it. *hypotheses:* ["At a moderate exchange rate, the oracle stopping checkpoint falls strictly before the trajectory's final checkpoint on at least 20% of instances (the oracle is non-trivial, not degenerate to 'always continue to the end').", "The oracle-reconstruction noise floor, measured by comparing oracles built from two disjoint probe halves, is no more than one-third of the best heuristic rule's own measured regret at the median exchange rate (the oracle is precise enough to license comparisons against it)."]
- **`m_decomposed_regret_attribution`** → targets `sp_signal_reliability`. *proposed_approach:* Replay each candidate rule (fixed-budget, confidence-threshold, entropy-threshold, self-consistency-vote-share-threshold, answer-stability) over the same logged trajectories; compute each rule's regret and its per-checkpoint signal-vs-verifier-label AUROC; split total regret by the sign of (t_r − t*) into stop-too-early and stop-too-late mass. *key_insight:* aggregate regret conflates "the signal is uninformative" with "the signal is informative but mis-thresholded," and only the paired, per-checkpoint replay on identical trajectories can tell these apart, because it holds everything except the rule itself constant. *hypotheses:* ["Every calibrated single-signal rule has mean regret significantly greater than zero and exceeding the instrument's noise floor, on at least two of three pilot benchmarks and at least five of seven exchange-rate values.", "At least one of the three online signals achieves per-checkpoint discrimination of verifier correctness reliably above chance (AUROC ≥ 0.60) on every benchmark.", "The self-consistency vote-share rule has lower mean regret than both the confidence-threshold and entropy-threshold rules in at least 60% of tested (backbone × benchmark × λ) cells."]
- **`m_learned_history_estimator`** → targets `sp_utility_nonstationarity`. *proposed_approach:* Train a small predictor (logistic regression / shallow MLP) mapping the running signal history (current and recent confidence/entropy/vote-share, their deltas, cumulative cost) to a signed predicted continuation gain; stop when predicted gain ≤ 0; evaluate with leave-one-benchmark-out and leave-one-model-out splits. *key_insight:* a single global threshold on one signal cannot track a quantity (marginal utility) that changes sign within a trajectory, but a predictor conditioned on the *trend* of the signal history can — the fix targets non-stationarity directly rather than picking a better fixed threshold. *hypotheses:* ["The learned estimator reduces mean normalized regret relative to the best single-signal rule by at least 10% relative, under both leave-one-benchmark-out and leave-one-model-out evaluation.", "The learned estimator's residual normalized regret at the median exchange rate remains at least 0.10 on every benchmark (the oracle gap is not closed), and this residual grows with task difficulty."]
- **`m_lambda_sweep_and_ranking_stability`** → targets `sp_exchange_rate_dependence`. *proposed_approach:* Recompute every rule's regret and ranking at each of 7 log-spaced λ grid points; measure Kendall's τ between rule orderings at adjacent λ values; track the stop-too-early/stop-too-late mass split as a function of λ. *key_insight:* ranking stability across λ is not implied by any single-λ result, however precise — it is a distinct empirical question about the *shape* of the regret surface in λ, answerable only by actually varying λ and measuring rank agreement, not by inspecting one slice of it. *hypotheses:* ["The ranking of stopping rules by mean regret is stable across adjacent λ grid points (mean Kendall's τ ≥ 0.6, no adjacent pair below 0.3).", "The fraction of total regret attributable to stopping too late (overthinking) increases monotonically with λ, shifting by at least 20 percentage points from the lowest to the highest tested value."]
- **`m_predecoding_control`** → targets `sp_predecoding_confound`. *proposed_approach:* Train a capacity-matched predictor restricted to pre-decoding and first-checkpoint features only (no later mid-trajectory signals); compare it against the full history-based estimator at matched mean token expenditure. *key_insight:* pre-decoding difficulty is a static, per-instance property fixed before generation starts, but how a trajectory actually unfolds is not fully determined by that static estimate — an instance predicted "hard" can resolve quickly, and one predicted "easy" can drift into unproductive continuation — so a fair test of whether mid-trajectory signals add real value is not a correlation check but a capacity-matched horse race against the best a pre-decoding-only predictor can do. *hypotheses:* ["The full history-based estimator beats the capacity-matched pre-decoding-only control by at least 10% relative normalized-regret reduction at matched token expenditure, with statistical significance."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis names a threshold, but one method's key_insight doesn't yet explain *why* mid-trajectory signals should beat a pre-decoding-only predictor — it currently just describes the comparison, not the reason to expect an asymmetric result.
- comments:
  - `{severity: minor, field: "m_predecoding_control.key_insight", anti_pattern: "weak_key_insight", comment: "As drafted, the key_insight mostly restates the approach (a matched control isolates mid-trajectory value) rather than explaining why mid-trajectory signals would carry information a pre-decoding predictor lacks. The fix is one sentence naming the actual mechanism: realized trajectory behavior can diverge from predicted difficulty in both directions, and only a signal that reads the trajectory as it unfolds can catch that divergence."}`
  - `{severity: minor, field: "m_checkpoint_probing_instrument.hypotheses", anti_pattern: null, comment: "Two hypotheses here (non-triviality, noise floor) are both instrument-validity claims rather than substantive findings about stopping rules. Worth stating explicitly why one instrument produces both, so this doesn't read as two unrelated checks bundled under one method."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_predecoding_control.key_insight` (already largely present in the draft, sharpened to lead with the mechanism rather than the comparison): "Pre-decoding difficulty is a static, per-instance estimate fixed before generation starts; realized trajectory behavior can diverge from it in both directions — a predicted-hard instance can resolve quickly, a predicted-easy one can drift into unproductive continuation — and only a signal that reads the trajectory as it actually unfolds can catch that divergence. The capacity-matched control is what turns 'mid-trajectory signals add value' from an assumption into a falsifiable comparison against the best a static predictor can do."
- `m_checkpoint_probing_instrument.key_insight` extended: "...both hypotheses are read off the same split-half reconstruction procedure applied to the same logged probes: whether the oracle is needed at all (non-triviality) and whether it is precise enough to trust once built (noise floor) — one instrument, two validity readouts, not two separate mechanisms."
- `changes_made`: sharpened the predecoding-control mechanism explanation; justified the two-hypotheses-one-method structure for the probing instrument.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **10 hypotheses total** (2 + 3 + 2 + 2 + 1 across the five methods respectively), mixing instrument-validity claims (non-triviality, noise floor) with the study's substantive empirical predictions (regret magnitude, signal ranking, learned-estimator gain, λ-stability, pre-decoding control) — a deliberate design choice for an `empirical` study_type, matching digest N8/`paper.md`'s own H1a–H3c + B-alt structure rather than re-deriving a smaller or larger set from scratch.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 10 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`), following the stage-6 default of one RQ per hypothesis (not bundled), matching the granularity `paper.md`'s own H-id table already uses.
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; the one candidate (`rw_adaptivethinking`'s pre-decoding limitation) is already covered end-to-end as a mechanism-tier RQ via `sp_predecoding_confound`/`m_predecoding_control`, so a separate framing-tier RQ would double-count the same evidence rather than add coverage — none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The fixed-budget and prefix-only-control comparisons below are necessary sanity/rival-explanation checks, never a competitor this paper claims to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GSM8K (test split) — *justification:* large, exact-match-verifiable arithmetic word problems; cheapest domain to pilot the instrument on (short traces, unambiguous grading).
- MATH-500 — *justification:* harder, multi-step math with an expression-equivalence verifier; stresses whether regret/AUROC findings generalize beyond arithmetic-level difficulty.
- AIME 2024 + 2025 — *justification:* integer-answer, competition-hard; small n (~60 combined), used descriptively only (excluded from hypothesis tests) to check the difficulty-regret relationship at the extreme tail without inflating false-discovery risk.
- GPQA-Diamond — *justification:* multiple-choice science QA; tests whether findings generalize beyond math-flavored reasoning to a different verifier type (MC grading) and error profile.
- LiveCodeBench (Stage-2 scale-up only) — *justification:* unit-test-execution verifier; tests generalization to a domain where "reasoning-transition checkpoints" look structurally different (code blocks, not prose) from the math/QA domains.

`baselines` (sanity-check / rival-explanation comparators, not outcome-tier competitors):
- Fixed-budget stopping (dev-selected best fixed checkpoint/token budget) — the necessary "is adaptivity worth anything at all" control.
- Oracle t* (regret 0 by construction) — the upper bound every rule is measured against.
- Prefix-only allocator (draft initially justified only as "similar to what Adaptive Thinking does" — flagged below).

`research_questions` (10, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_oracle_nontriviality` | `sp_oracle_construction` | "At a moderate exchange rate, the oracle stopping checkpoint falls strictly before the trajectory's final checkpoint on at least 20% of instances (the oracle is non-trivial, not degenerate to 'always continue to the end')." |
| `rq_noise_floor` | `sp_oracle_construction` | "The oracle-reconstruction noise floor, measured by comparing oracles built from two disjoint probe halves, is no more than one-third of the best heuristic rule's own measured regret at the median exchange rate (the oracle is precise enough to license comparisons against it)." |
| `rq_heuristic_regret_real` | `sp_signal_reliability` | "Every calibrated single-signal rule has mean regret significantly greater than zero and exceeding the instrument's noise floor, on at least two of three pilot benchmarks and at least five of seven exchange-rate values." |
| `rq_signal_informativeness` | `sp_signal_reliability` | "At least one of the three online signals achieves per-checkpoint discrimination of verifier correctness reliably above chance (AUROC ≥ 0.60) on every benchmark." |
| `rq_signal_ranking` | `sp_signal_reliability` | "The self-consistency vote-share rule has lower mean regret than both the confidence-threshold and entropy-threshold rules in at least 60% of tested (backbone × benchmark × λ) cells." |
| `rq_learned_estimator_gain` | `sp_utility_nonstationarity` | "The learned estimator reduces mean normalized regret relative to the best single-signal rule by at least 10% relative, under both leave-one-benchmark-out and leave-one-model-out evaluation." |
| `rq_residual_gap_difficulty` | `sp_utility_nonstationarity` | "The learned estimator's residual normalized regret at the median exchange rate remains at least 0.10 on every benchmark (the oracle gap is not closed), and this residual grows with task difficulty." |
| `rq_ranking_stability` | `sp_exchange_rate_dependence` | "The ranking of stopping rules by mean regret is stable across adjacent λ grid points (mean Kendall's τ ≥ 0.6, no adjacent pair below 0.3)." |
| `rq_failure_mode_shift` | `sp_exchange_rate_dependence` | "The fraction of total regret attributable to stopping too late (overthinking) increases monotonically with λ, shifting by at least 20 percentage points from the lowest to the highest tested value." |
| `rq_predecoding_control` | `sp_predecoding_confound` | "The full history-based estimator beats the capacity-matched pre-decoding-only control by at least 10% relative normalized-regret reduction at matched token expenditure, with statistical significance." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E3 + B-alt numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one baseline's justification is a provenance note instead of a reason tied to what it rules out.
- comments:
  - `{severity: major, field: "baselines[prefix-only allocator]", anti_pattern: "weak justification (fails the rubric's 'justification for why this comparator actually stresses the hypothesis')", comment: "'similar to what Adaptive Thinking does' says where the idea came from, not why beating it would mean anything. It needs to name the specific rival explanation it rules out — that adaptive value is exhausted by pre-decoding difficulty prediction — and the capacity/budget-matching condition that makes the comparison fair."}`
- decision: `move_to_refiner`.

### Refiner pass

- `baselines` entry replaced: "Prefix-only allocator — *justification:* a capacity-matched predictor using only pre-decoding and first-checkpoint features, trained identically to the full history-based estimator and evaluated at matched mean token expenditure. Rules out the specific rival explanation that any measured gain from mid-trajectory signals is really just an implicit re-derivation of a difficulty estimate already available before decoding began (the position `[Adaptive Thinking, OpenReview:2i6Rp0gCq6]`'s own framing implies); beating it is what licenses calling the estimator's gain a genuine use of *online*, mid-trajectory evidence."
- `changes_made`: gave the prefix-only allocator's inclusion a rival-explanation-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_matters`/`why_it_is_a_problem` fields name no technique (probing, thresholds, and the learned estimator appear starting only at Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_predecoding_confound.source_limitation_ids = ["rw_adaptivethinking"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (stop/continue decisions, per-instance/per-λ regret, difficulty/λ-aggregated regret curves, signed marginal-utility estimate) are each reachable: decisions/regret via `sp_oracle_construction`+`sp_signal_reliability`, difficulty/λ-curves via `sp_exchange_rate_dependence`, signed marginal utility via `sp_utility_nonstationarity` (+ `sp_predecoding_confound` for its causal-attribution reliability) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs and 10 mechanism-tier RQs, one per hypothesis (recount: 2+3+2+2+1 = 10 hypotheses in Stage 5 ⇔ 10 RQs in Stage 6 ✓).

**What was hardest:** unlike a typical under-specified seed, the recurring tension here was *not* finding real content — `paper.md` had already authored almost every hypothesis, threshold, and fallback — but making sure this schema's own structure (sub-problem decomposition, method-to-hypothesis traceability, RQ tiering) added genuinely new value rather than mechanically re-transcribing `paper.md`'s Step 6 table. The two places genuine new structure emerged: (a) explicitly separating "can the oracle be built and trusted" (`sp_oracle_construction`) from "do conclusions survive varying λ" (`sp_exchange_rate_dependence`) — two problems `paper.md` treats adjacently but doesn't explicitly distinguish; and (b) promoting the Adaptive-Thinking rival explanation from a related-work aside into its own named sub-problem/method pair (`sp_predecoding_confound`/`m_predecoding_control`), rather than leaving the B-alt control as an appendix-style "mandatory baseline" note the way `paper.md` does.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Revision pass over every finding in `stage_review.md` (Stage 1–5 review, Phase A checklist, Phase G adversarial review) and `taste_audit.md` (no `design_review.md` exists in this topic). Each finding was re-verified against the *current* deliverables rather than trusted from the log. Historical rounds above are untouched.

| # | Source | Finding | Status / action |
|---|---|---|---|
| 1 | stage_review.md Stage 2 (REVISE) | Missing nearest-neighbor sentence naming DEER/TrimR + delta at the head of Related Work | **Already applied** — verified present in `paper_draft.md` (Related Work opening paragraph) and `paper_draft.tex`; no change |
| 2 | stage_review.md Stage 4 (REVISE) | Verifier-grading audit (50 decisions/benchmark, >2% gate) + contamination check missing from Experimental Setup (secondary Resource archetype) | **Already applied** — verified in `paper_draft.md` ("Corpus quality and contamination controls"), `paper_draft.tex`, and mirrored in `experiment_design.md` Datasets section; no change |
| 3 | stage_review.md Phase A item 1 | digest.md N12 lacked `status`/`absence_comment` | **Already applied** — verified in `../digest.md` N12 (status: PARTIAL + 3-part absence_comment); no change |
| 4 | stage_review.md Phase A item 2 | Reference cache in ad hoc schema, all `pending`; N3 works absent from cache | **Already applied** — `reference_candidates.jsonl` in canonical schema, 160 records, 20 selected / 140 rejected, 0 pending; no change |
| 5 | stage_review.md Phase A item 4 | H3c orphaned from Claim–Evidence Map | **Already applied** — verified H3c row in `../paper.md` Claim–Evidence Map; no change |
| 6 | stage_review.md Phase A item 5 | A\* table missing `Consequence` column; no power assumption | **Already applied** — verified Consequence column on A1–A8 and new A8 power assumption in `../paper.md`; mirrored as the "General sample-size rationale (Assumption A8)" block in `experiment_design.md`; no change |
| 7 | stage_review.md Phase A item 6 | Missing estimand sentence (R1), confound ledger (R3), dropped-row rule (R8) | **Already applied** — verified all three in `../paper.md` (Estimand line, Confound ledger, Matched-set/dropped-row rule); dropped-row rule mirrored in `experiment_design.md` Common protocol; no change |
| 8 | stage_review.md Phase G [major] | H3c/RQ11 absent from the draft's RQ list | **Already applied** — RQ11 verified in `paper_draft.md` (RQ list item 11 + full subsection), `paper_draft.tex`, and `experiment_design.md` (verbatim H3c criterion: 2× coarser subsampling < 50% of median between-rule gap); no change |
| 9 | stage_review.md Phase G [major] | B0 placebo-first ordering + ≥20% justification criterion never stated as a checkable gate | **Already applied** — "Placebo-first ordering (B0)" paragraph verified in `paper_draft.md`, `paper_draft.tex`, and `experiment_design.md` Baselines; no change |
| 10 | stage_review.md Phase G [moderate] | RQ3 watered down H1a's "3× the noise floor" to "exceeding the noise floor" | **Already applied** — 3× multiplier verified in Expected Outcome + Falsification Condition of RQ3 in all three deliverables; no change |
| 11 | stage_review.md Phase G [moderate] | `Chen2023Close`/`FirstImpression2607` uncited at the exact claims they ground | **Already applied** — both citations verified at the "four distinct obstacles" paragraph sentences in `paper_draft.md`/`.tex`; no change |
| 12 | stage_review.md Phase G [minor] | `SAFER2607` had no Related Work paragraph | **Already applied** — "Offline global budget calibration" paragraph verified in `paper_draft.md`/`.tex`; no change |
| 13 | stage_review.md Phase G (hard gate) | `paper_draft.tex` had zero `\cite` commands, no `refs.bib` | **Already applied** — `build_refs_bib.py` + `refs.bib` (20 entries) exist; 11 distinct `\citep` keys resolve in the compiled PDF per the Phase I log; no change |
| 14 | stage_review.md Phase G (open to-do) / pipeline.md residual | `CaTS2607`/`AdaptiveThinking2607` lack a fetched PDF/full digest (OpenReview bot wall) | **Rejected — still environment-blocked.** Re-attempted 2026-07-05: `openreview.net/pdf?id=2i6Rp0gCq6` returns HTTP 403 (challenge page). Citations continue to rest on the corpus proposal record + public abstract, as logged. Requires an unblocked network, not a prose edit |
| 15 | taste_audit.md (both passes) | Verdict 🟢, no conditions fired, no action items | **No action required** — audit is confirmatory; re-checked that no edit in this pass touched the Abstract or Method Overview (no edits were made at all) |

**Cross-deliverable consistency check (this pass):** `paper_draft.md` and `experiment_design.md` both carry 11 RQs (RQ1–RQ11) in the same order with matching expected outcomes and falsification conditions; effect floors and margins agree across both files and `paper.md` (NR_λ ≥ 0.05 and 3× noise floor for RQ3/H1a; AUROC ≥ 0.60 / CI lower bound > 0.55 for RQ4/H1b; 60%/10% cell shares for RQ5/H2a; ≥10% relative on ≥3/5 benchmarks and ≥2/3 models for RQ6/H2b; residual ≥ 0.10 and ρ ≥ 0.5 on ≥3/5 for RQ7/H2c; τ ≥ 0.6 / no pair < 0.3 for RQ8/H3a; ρ ≥ 0.8 and ≥20 pp for RQ9/H3b; ≥10% at matched expenditure for RQ10/B-alt; <50% of median between-rule gap for RQ11/H3c; B0 gate ≥20% relative mean regret on ≥2 pilot benchmarks). Target hypotheses in `experiment_design.md` remain verbatim quotes; none were paraphrased. **No inconsistency found; no file content changed in this pass beyond this trace section and the pipeline Phase Log row.**
