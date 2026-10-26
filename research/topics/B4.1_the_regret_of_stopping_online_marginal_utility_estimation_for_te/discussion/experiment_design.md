# Experiment Design — B4.1: The Regret of Stopping

> Standalone protocol document, per the updated `auto-research-discussion` SKILL.md's three-artifact deliverable spec ("the document the user actually executes from — it should be runnable as a protocol without opening the paper"). Assembled from `pipeline.md`'s Stage 6 confirmed output (draft + critique + refiner pass, now moved to `discussion_trace.md`) and `paper.md`'s Step 5 (Formal Problem Definition / Assumptions A1–A8) and Step 6 (Pre-Registered Experiments E1–E3 + Mandatory baselines), reconciled with the already-reviewed `paper_draft.md` Experiments section (which folds in the Phase E/G fixes: RQ11, the 3× noise-floor multiplier, the Placebo-first ordering note). Nothing below is invented beyond those three sources. Keep this file synchronized with `paper_draft.md`'s Experiments section if either is edited later.

**Tier accounting (from `pipeline.md` Stage 6, unchanged):** Mechanism-tier: 10 RQs, one per Stage 5 hypothesis, verbatim `target_hypotheses`. Framing-tier: 0 RQs (the one candidate — Adaptive Thinking's pre-decoding limitation — is already covered end-to-end as a mechanism-tier RQ, so a separate framing-tier RQ would double-count evidence). Outcome-tier: 0 RQs (`study_type = empirical` forbids "beats baseline X" framing; the baselines below are sanity/rival-explanation checks, not competitors). **RQ11 is an addition made after Stage 6 closed** — added during the Phase Log's Phase E/G passes (see `pipeline.md`'s Phase Log) to restore `paper.md`'s own pre-registered H3c criterion, which had been dropped from the assembled draft's RQ list. It was not part of the Stage 6 table of 10 and so has no `rq_id` in the discussion trace, but its target hypothesis is a verbatim quote from `paper.md`'s Step 6 (H3c) — see RQ11 below.

---

## Datasets

(From `pipeline.md` Stage 6 confirmed `datasets`, reconciled with `paper_draft.md`'s Experimental Setup prose.)

- **GSM8K** (test split, exact-match numeric verifier) — *justification:* large, exact-match-verifiable arithmetic word problems; cheapest domain to pilot the instrument on (short traces, unambiguous grading).
- **MATH-500** (expression-equivalence verifier) — *justification:* harder, multi-step math; stresses whether regret/AUROC findings generalize beyond arithmetic-level difficulty.
- **AIME 2024 + 2025** (integer-answer verifier, combined ~60 items) — *justification:* competition-hard; small n, used descriptively only (excluded from hypothesis tests) to check the difficulty–regret relationship at the extreme tail without inflating false-discovery risk.
- **GPQA-Diamond** (multiple-choice verifier) — *justification:* tests whether findings generalize beyond math-flavored reasoning to a different verifier type (MC grading) and error profile.
- **LiveCodeBench** (unit-test-execution verifier; Stage-2 scale-up only) — *justification:* tests generalization to a domain where "reasoning-transition checkpoints" look structurally different (code blocks, not prose) from the math/QA domains.

**Corpus quality and contamination controls** (added during `paper_draft.md`'s Phase A/E fixes, required by this paper's secondary Resource archetype): a manual audit of 50 verifier decisions per benchmark checks the mechanical grader's own error rate; any benchmark showing more than 2% grading errors requires a fixed grader before that benchmark's pilot results are trusted. Each benchmark's known train/pretraining overlap status (where publicly documented) is reported alongside the released corpus, and any benchmark with disclosed contamination risk is flagged in the corpus metadata rather than silently pooled with uncontaminated benchmarks in aggregate statistics.

## Baselines

(From `pipeline.md` Stage 6 confirmed `baselines`, with the refiner pass's fix to the prefix-only allocator's justification, plus `paper.md`'s Mandatory-baselines numeric criteria.)

- **B0 — Fixed-budget stopping** (the necessary "is adaptivity worth anything at all" control). Non-adaptive stopping at every fixed checkpoint index / token budget, with the best per-benchmark fixed budget chosen on the dev split. *Pre-registered justification criterion (`paper.md` Step 6):* the best adaptive heuristic must beat the best dev-selected fixed budget by ≥ 20% relative mean regret (Holm-corrected p < 0.05) at the median λ on ≥ 2 pilot benchmarks — otherwise adaptivity itself is worthless on these tasks and the paper's framing reverts to the global pivot (F-G1).
- **Oracle t\*** — the upper bound every rule is measured against, regret 0 by construction.
- **Prefix-only allocator (B-alt)** — *justification (refiner-fixed wording):* a capacity-matched predictor using only pre-decoding and first-checkpoint features, trained identically to the full history-based estimator and evaluated at matched mean token expenditure. Rules out the specific rival explanation that any measured gain from mid-trajectory signals is really just an implicit re-derivation of a difficulty estimate already available before decoding began (the position `[Adaptive Thinking, OpenReview:2i6Rp0gCq6]`'s own framing implies); beating it is what licenses calling the estimator's gain a genuine use of *online*, mid-trajectory evidence. **Numeric criterion (`paper.md`):** full estimator beats the prefix-only allocator with Holm-corrected p < 0.05 and ≥ 10% relative NR reduction; otherwise the pre-committed wording is *"the value of stopping-rule adaptivity is exhausted by pre-decoding difficulty prediction; mid-trajectory signals add nothing measurable."*

**Placebo-first ordering (B0):** B0 is evaluated *before* any of RQ3–RQ10 are scored, not merely reported alongside them — if B0 is not beaten by the ≥20% relative-regret margin above, the paper's framing reverts to the global pivot (see `paper.md`'s F-G1) rather than proceeding to score RQ3–RQ10 as if adaptivity were already established.

## Common protocol (applies to every RQ unless an RQ states otherwise)

(Verbatim from `paper.md` Step 6 "Common protocol," hardened from digest N8's analysis plan.)

≥ 500 instances/benchmark where test sets allow (AIME ~60 items: descriptive only, excluded from hypothesis tests); all rules replayed on identical logged trajectories → exactly paired; two-sided Wilcoxon signed-rank on per-instance regret differences; Holm–Bonferroni over the ~15 rule pairs per (benchmark, λ) family; α = 0.05 after correction; 10,000-resample paired bootstrap for 95% CIs; thresholds τ calibrated on a held-out 20% dev split, all tests on the disjoint 80% eval split.

**Matched-set / dropped-row rule (`paper.md`, guidance.md §3.4 R8):** an instance is dropped from the entire (benchmark, λ) comparison set — for every rule, not just the one that failed — if the verifier cannot parse a probe answer at any logged checkpoint, if the model's trace truncates before the first checkpoint (no valid oracle can be reconstructed), or if a rule's replay cannot produce a stop decision from the logged signal interface (Assumption A6). Dropped instances are logged with a reason code; the headline n reported for every table is the post-drop n, and the drop rate per benchmark is reported alongside n. Any (benchmark, λ) or leave-one-out cell whose post-drop n falls below the Assumption A8 power-derived minimum is pre-declared INCONCLUSIVE, never silently pooled with adequately powered cells.

**General sample-size rationale (Assumption A8, `paper.md`):** pre-registered sample sizes target power ≥ 0.8 for the two-sided Wilcoxon signed-rank test to detect each hypothesis's stated effect floor (e.g., H1a's NR_λ ≥ 0.05 regret gap over the noise floor; H2b's ≥10% relative NR reduction) at α = 0.05 after Holm correction, calibrated from a 100-instance pilot subsample's observed regret variance. Any (benchmark, λ) or LOBO/LOMO cell whose achieved power falls below 0.8 is flagged before scoring and reported as INCONCLUSIVE rather than as a null result. Per-RQ sections below name any RQ-specific sample-size detail beyond this general rule.

---

## RQ1: Is the reconstructed oracle non-trivial?

- **Tier:** Mechanism-tier (instrument-validity check).
- **Target hypothesis (verbatim, Stage 5 `m_checkpoint_probing_instrument` → Stage 6 `rq_oracle_nontriviality`, `pipeline.md`):** "At a moderate exchange rate, the oracle stopping checkpoint falls strictly before the trajectory's final checkpoint on at least 20% of instances (the oracle is non-trivial, not degenerate to 'always continue to the end')." *(Corresponds to `paper.md` Assumption A5's skeleton gate.)*
- **Setup:** At a moderate exchange rate (the λ grid's midpoint), compute the fraction of pilot instances (GSM8K, MATH-500, GPQA-Diamond; single backbone) for which t*(x, λ) falls strictly before the trajectory's final checkpoint K.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark (pilot stage, single backbone); no RQ-specific sample size beyond the common protocol.
- **Statistical test:** No significance test named in the source material — this is a gate/threshold check (fraction ≥ 20% at the median λ) rather than a formal hypothesis test, consistent with its role as `paper.md` Assumption A5's skeleton gate. Fail routes to F-G1 (the global pivot), per Assumption A5's consequence column.
- **Expected outcome:** The oracle recommends stopping before the trajectory's end on at least 20% of instances at the median λ.
- **Falsification condition:** Refuted if the oracle recommends continuing to the final checkpoint on more than 80% of instances.
- **Metrics:** Fraction of instances with t* < K at the median λ.

## RQ2: Is the oracle reconstruction precise enough to license comparisons?

- **Tier:** Mechanism-tier (instrument-validity check).
- **Target hypothesis (verbatim, Stage 5 `m_checkpoint_probing_instrument` → Stage 6 `rq_noise_floor`, `pipeline.md`):** "The oracle-reconstruction noise floor, measured by comparing oracles built from two disjoint probe halves, is no more than one-third of the best heuristic rule's own measured regret at the median exchange rate (the oracle is precise enough to license comparisons against it)." *(Corresponds to `paper.md` Assumption A3's skeleton gate.)*
- **Setup:** Independently reconstruct t*(x, λ) from two disjoint halves of the same per-checkpoint probes (probes 1–4 build t*, probes 5–8 score it); compare the resulting split-half regret (the instrument's "self-regret") against the best heuristic rule's own measured regret at the median λ.
- **Sample-size rationale:** N=8 probes per checkpoint (Assumption A3); a pre-committed mitigation is an N=32 re-probe on 100 instances if the gate fails.
- **Statistical test:** No significance test named — a threshold ratio check (noise floor ≤ 1/3 of best heuristic's measured regret). Directly gates H1a (RQ3): if this gate fails, RQ3/H1a is blocked, not merely degraded, until N is raised (per Assumption A3's consequence column).
- **Expected outcome:** The split-half noise floor is no more than one-third of the best heuristic rule's measured regret at the median λ.
- **Falsification condition:** Refuted if the split-half noise floor equals or exceeds one-third of the best heuristic's measured regret.
- **Metrics:** Split-half regret (noise floor); ratio to the best heuristic's measured regret.

## RQ3: Do calibrated single-signal rules incur real, non-noise regret?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_decomposed_regret_attribution` → Stage 6 `rq_heuristic_regret_real`, `pipeline.md`):** "Every calibrated single-signal rule has mean regret significantly greater than zero and exceeding the instrument's noise floor, on at least two of three pilot benchmarks and at least five of seven exchange-rate values." *(= `paper.md` H1a, with the exact multiplier restored during the Phase G review fix: regret must exceed 3× the noise floor, not merely exceed it.)*
- **Setup:** Pilot stage: 2 backbones × 2 conditions (rule on vs. oracle) × the three pilot benchmarks × ~500 instances each. Scale-up: ≥3 model families × 5 benchmarks. Thresholds τ per rule calibrated on the held-out 20% dev split; all tests on the disjoint 80% eval split.
- **Sample-size rationale:** ≥500 instances per benchmark (AIME excluded from hypothesis tests, reported descriptively) are sized to detect a standardized regret effect at conventional power against the split-half noise floor established in RQ2; an observed effect below that threshold in the pilot triggers a pre-committed sample enlargement in the scale-up rather than a null claim.
- **Statistical test:** Two-sided Wilcoxon signed-rank test on per-instance regret, Holm–Bonferroni corrected across rule pairs and λ values, α = 0.05; regret must additionally exceed 3× the RQ2 split-half noise floor to count (`paper.md` H1a Verification).
- **Expected outcome:** Every calibrated single-signal rule has mean regret significantly greater than zero (NR_λ ≥ 0.05) and exceeding 3× the RQ2 split-half noise floor, on at least two of the three pilot benchmarks and at least five of seven tested λ values.
- **Falsification condition:** Refuted if any single-signal rule's regret fails to clear 3× the RQ2 noise floor across the majority of benchmarks and λ values — that rule is effectively ε-certified as oracle-level, feeding the F-G1 pivot wording.
- **Metrics:** Per-rule mean regret and 95% bootstrap CI; count of (benchmark, λ) cells clearing the noise floor.

## RQ4: Do online signals discriminate correctness above chance?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_decomposed_regret_attribution` → Stage 6 `rq_signal_informativeness`, `pipeline.md`):** "At least one of the three online signals achieves per-checkpoint discrimination of verifier correctness reliably above chance (AUROC ≥ 0.60) on every benchmark." *(= `paper.md` H1b.)*
- **Setup:** For each benchmark, compute each signal's (confidence, entropy, self-consistency vote share) per-checkpoint AUROC against the checkpoint's own verifier label, pooled across instances and checkpoints.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark; no RQ-specific sample size beyond the common protocol.
- **Statistical test:** Bootstrap 95% CI on AUROC (lower bound > 0.55 required); no separate p-value test is named beyond this CI criterion in the source material.
- **Expected outcome:** At least one signal achieves AUROC ≥ 0.60 (bootstrap 95% CI lower bound > 0.55) on every benchmark.
- **Falsification condition:** Refuted if every signal's AUROC is statistically indistinguishable from 0.5 on a benchmark.
- **Metrics:** Per-signal, per-benchmark AUROC with bootstrap CI.

## RQ5: Does self-consistency dominate confidence and entropy?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_decomposed_regret_attribution` → Stage 6 `rq_signal_ranking`, `pipeline.md`):** "The self-consistency vote-share rule has lower mean regret than both the confidence-threshold and entropy-threshold rules in at least 60% of tested (backbone × benchmark × λ) cells." *(= `paper.md` H2a, which additionally requires self-consistency to be significantly worse in ≤10% of cells.)*
- **Setup:** Pairwise comparison of mean regret between the self-consistency vote-share rule and each of the confidence-threshold and entropy-threshold rules, across all tested (backbone × benchmark × λ) cells (Stage 2: 3 models × 5 benchmarks × 7 λ).
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark at Stage-2 scale-up (3 model families × 5 benchmarks); no additional RQ-specific sample size named.
- **Statistical test:** Pairwise two-sided Wilcoxon signed-rank per cell, Holm–Bonferroni corrected across rule pairs (`paper.md` H2a Verification).
- **Expected outcome:** The self-consistency rule has significantly lower mean regret than both alternatives in at least 60% of tested cells, and is significantly worse in no more than 10%.
- **Falsification condition:** Refuted if self-consistency is dominated by confidence or entropy in the majority of cells, or if no consistent ranking emerges.
- **Metrics:** Per-cell win/loss/tie counts and Holm-corrected pairwise significance.

## RQ6: Does a learned combination of signal history reduce regret, and does it transfer?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_learned_history_estimator` → Stage 6 `rq_learned_estimator_gain`, `pipeline.md`):** "The learned estimator reduces mean normalized regret relative to the best single-signal rule by at least 10% relative, under both leave-one-benchmark-out and leave-one-model-out evaluation." *(= `paper.md` H2b, which specifies ≥3 of 5 held-out benchmarks and ≥2 of 3 held-out models.)*
- **Setup:** Train the learned history estimator on Stage-1 logged trajectories; evaluate mean normalized regret against the best single-signal rule under leave-one-benchmark-out (holding out each of 5 scale-up benchmarks in turn) and leave-one-model-out (holding out each of 3 model families in turn).
- **Sample-size rationale:** Transfer claims are backed only by LOBO/LOMO splits (digest t4 mitigation, `paper.md` H2b Verification); Assumption A7 gates whether Stage-2 scale-up (needed for LOBO/LOMO) is affordable at all — failure forces a pre-declared shrink-along-declared-axes response, narrowing which hypotheses remain adequately powered.
- **Statistical test:** Exactly paired Wilcoxon per cell, Holm-corrected over rule pairs; significance required on ≥3 of 5 held-out benchmarks and ≥2 of 3 held-out models (`paper.md` H2b Verification).
- **Expected outcome:** The learned estimator reduces mean normalized regret relative to the best single-signal rule by at least 10% relative, with Holm-corrected significance, on at least 3 of 5 held-out benchmarks and at least 2 of 3 held-out models.
- **Falsification condition:** Refuted if the learned estimator fails to significantly beat the best single-signal rule on a majority of held-out benchmarks or models.
- **Metrics:** Normalized-regret reduction ratio (learned vs. best single signal) with bootstrap CI, per held-out split.

## RQ7: Does the learned estimator's residual gap to the oracle grow with difficulty?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_learned_history_estimator` → Stage 6 `rq_residual_gap_difficulty`, `pipeline.md`):** "The learned estimator's residual normalized regret at the median exchange rate remains at least 0.10 on every benchmark (the oracle gap is not closed), and this residual grows with task difficulty." *(= `paper.md` H2c, which specifies Spearman ρ ≥ 0.5 on ≥3 of 5 benchmarks.)*
- **Setup:** Within each scale-up benchmark, bin instances into difficulty deciles by baseline pass rate; compute the learned estimator's normalized regret NR_λ at the median λ within each decile.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark at Stage-2 scale-up; decile binning requires the full benchmark sample, not a subsample.
- **Statistical test:** Spearman correlation between NR_λ and difficulty decile (threshold ρ ≥ 0.5 on ≥3 of 5 benchmarks); `paper.md`'s E2 Verification paragraph does not separately name a significance procedure for H2c beyond this correlation threshold.
- **Expected outcome:** The learned estimator's residual normalized regret at the median λ remains at least 0.10 on every benchmark, and Spearman correlation between NR_λ and difficulty decile is at least 0.5 on at least 3 of 5 benchmarks.
- **Falsification condition:** Refuted if the residual gap is flat or shrinking across difficulty deciles.
- **Metrics:** Per-decile normalized regret; Spearman ρ(NR_λ, difficulty decile).

## RQ8: Is the ranking of stopping rules stable across the exchange rate?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_lambda_sweep_and_ranking_stability` → Stage 6 `rq_ranking_stability`, `pipeline.md`):** "The ranking of stopping rules by mean regret is stable across adjacent λ grid points (mean Kendall's τ ≥ 0.6, no adjacent pair below 0.3)." *(= `paper.md` H3a.)*
- **Setup:** Recompute every rule's ranking by mean regret at each of 7 log-spaced λ grid points spanning roughly 0.01–3 accuracy points per 1K tokens; compute Kendall's τ between rule orderings at each pair of adjacent grid points, pooled per model.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark; the 7-point λ grid is fixed by Assumption/notation in `paper.md` Step 5, not independently sized.
- **Statistical test:** Kendall's τ with bootstrap CIs over instance resamples (`paper.md` H3a Verification).
- **Expected outcome:** Mean Kendall's τ between adjacent λ orderings is at least 0.6, with no adjacent pair falling below 0.3.
- **Falsification condition:** Refuted if rule rankings reorder substantially across the λ grid (low or near-zero Kendall's τ between adjacent values).
- **Metrics:** Kendall's τ per adjacent λ pair, with bootstrap CI over instance resamples.

## RQ9: Does the dominant failure mode shift from stopping early to stopping late as the exchange rate rises?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_lambda_sweep_and_ranking_stability` → Stage 6 `rq_failure_mode_shift`, `pipeline.md`):** "The fraction of total regret attributable to stopping too late (overthinking) increases monotonically with λ, shifting by at least 20 percentage points from the lowest to the highest tested value." *(= `paper.md` H3b, which specifies Spearman ρ ≥ 0.8.)*
- **Setup:** At each λ grid point, compute the fraction of total regret attributable to stopping too late (t_r > t*) for the best-performing heuristic rule and for the learned estimator.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark; computed over the same 7-point λ grid as RQ8.
- **Statistical test:** Spearman ρ exact permutation test over the grid (`paper.md` H3b Verification), threshold ρ ≥ 0.8.
- **Expected outcome:** The stop-too-late regret share increases with λ (Spearman ρ ≥ 0.8 over the grid), shifting by at least 20 percentage points from the lowest to the highest tested λ.
- **Falsification condition:** Refuted if the stop-too-early/stop-too-late mix does not shift with λ in the predicted direction.
- **Metrics:** Stop-too-late regret share per λ, per rule.

## RQ10: Does exploiting mid-trajectory signals add value beyond pre-decoding difficulty prediction?

- **Tier:** Mechanism-tier.
- **Target hypothesis (verbatim, Stage 5 `m_predecoding_control` → Stage 6 `rq_predecoding_control`, `pipeline.md`):** "The full history-based estimator beats the capacity-matched pre-decoding-only control by at least 10% relative normalized-regret reduction at matched token expenditure, with statistical significance." *(Tied to `paper.md`'s B-alt mandatory-baseline numeric criterion: Holm-corrected p < 0.05 and ≥10% relative NR reduction.)*
- **Setup:** Train a capacity-matched predictor restricted to pre-decoding and first-checkpoint features only; compare its normalized regret against the full learned history estimator at matched mean token expenditure, across all scale-up benchmarks and models.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark at Stage-2 scale-up; no additional RQ-specific sample size named.
- **Statistical test:** Holm-corrected significance test (Wilcoxon, per the Common protocol) at p < 0.05, on the ≥10% relative NR reduction criterion (`paper.md` B-alt).
- **Expected outcome:** The full history-based estimator beats the pre-decoding-only control by at least 10% relative normalized-regret reduction, with statistical significance, at matched token expenditure.
- **Falsification condition:** Refuted if the pre-decoding-only control matches or beats the full estimator at the same token expenditure — pre-committed wording: *"the value of stopping-rule adaptivity is exhausted by pre-decoding difficulty prediction; mid-trajectory signals add nothing measurable."*
- **Metrics:** Normalized-regret reduction (full estimator vs. pre-decoding-only control) at matched token expenditure, with bootstrap CI.

## RQ11: Does checkpoint discretization dominate the measured between-rule regret differences?

- **Tier:** Mechanism-tier (instrument-validity / construct-validity check). **Not part of the original Stage 6 table of 10** — added later (Phase Log's Phase E/G passes in `pipeline.md`) to restore `paper.md`'s own pre-registered H3c criterion, which the first-assembled `paper_draft.tex` had dropped despite it being flagged in the Claim–Evidence Map as "the construct-validity precondition every claim above depends on."
- **Target hypothesis (verbatim, `paper.md` Step 6, H3c):** "2× coarser checkpoint subsampling changes each rule's mean regret by less than 50% of the median between-rule regret gap at the same λ."
- **Setup:** Re-segment each pilot trajectory at 2× coarser checkpoint granularity (half as many transition markers retained) and recompute every rule's mean regret at the median λ; compare the resulting shift in mean regret per rule to the median between-rule regret gap measured at the original (finer) granularity.
- **Sample-size rationale:** Inherits the Common protocol's ≥500 instances/benchmark at the pilot stage; Assumption A4 additionally requires median checkpoint count K ≥ 8 from the skeleton log.
- **Statistical test:** Point comparison with bootstrap CI (`paper.md` H3c Verification) — no separate significance test beyond the CI-bounded threshold ratio.
- **Expected outcome:** The 2×-coarser-checkpoint regret shift is less than 50% of the median between-rule regret gap at the same λ, for every rule in the bank.
- **Falsification condition:** Refuted if coarsening checkpoints shifts any rule's mean regret by 50% or more of the between-rule gap — in that case, checkpoint granularity, not the rule's own signal quality, is the dominant driver of the regret differences reported in RQ3–RQ9, and every absolute regret number in this paper is demoted from an oracle-relative claim to an instrument-relative one.
- **Metrics:** Per-rule regret shift under 2× coarsening; ratio to the median between-rule regret gap at the original granularity, with bootstrap CI.

---

## Global fallback (F-G1)

(Verbatim from `paper.md` Step 6.) If the central hypothesis family (H1a/H1b jointly, i.e. RQ3/RQ4, or Assumption A5's nontriviality gate, i.e. RQ1) fails, the archetype pivots from *empirical measurement of regret headroom* to *instrument/dataset: a regret-certification benchmark*. Pre-committed pivoted abstract sentence: *"We release a checkpoint-level, verifier-labeled reasoning-trajectory corpus and an offline-replay regret evaluator that certifies any stopping rule's distance from the per-instance oracle, and use it to show that on today's verifiable reasoning benchmarks the stopping problem is either already ε-solved by simple agreement thresholds or unresolvable from logged online signals — settling, in either direction, what further stopping-rule research can buy."*
