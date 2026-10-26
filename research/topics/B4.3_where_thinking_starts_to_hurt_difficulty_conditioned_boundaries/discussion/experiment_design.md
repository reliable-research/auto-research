# Experiment Design — B4.3: Where Thinking Starts to Hurt

> Standalone protocol document, assembled per the `auto-research-discussion` skill's "Final deliverables" spec (item 2). Source: Stage 6's confirmed output in `discussion_trace.md` (the relocated `pipeline.md` trace) plus `../paper.md`'s own Step 6 ("Pre-Registered Experiments") and `paper_draft.md`'s assembled Experiments section, which is where several of Stage 6's protocol details (exact rollout counts, statistical-test names, sample-size targets) were carried forward and refined. **No content below was invented for this document** — every setup/statistical-test/metric detail is quoted or paraphrased from one of those three sources. This is meant to be runnable as a protocol without opening the paper draft; keep it synchronized with `paper_draft.md`/`.tex` if either is edited later.
>
> **Status:** specification only — no experiments have been run. All numbers are pre-registered design targets.
>
> **Tier accounting** (per Stage 6, checked against `study_type = empirical`): **6 mechanism-tier RQs** (RQ1–RQ6 below), one per Stage 5 hypothesis, each carrying its Stage 5 `target_hypotheses` text verbatim. **0 framing-tier RQs** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis` (see `discussion_trace.md` Stage 3 refiner note). **0 outcome-tier RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing; every baseline below is a sanity-check comparator that gives an informativeness/recovery claim a scale, never a competitor to beat. A 7th RQ (mechanism-analysis probe) is appended at the end as an **addendum**: it comes from `paper.md`'s own Step 6 "Mechanism analysis (M6)" and was later formalized as `RQ7` in `paper_draft.tex` during a post-hoc adversarial-review pass (`pipeline.md`'s Phase G), not from the original Stage 5/6 critic-refiner loop — it has no Stage 5 `target_hypotheses` entry, so its "target hypothesis" below is `paper.md`'s own pre-registered prediction text rather than a Stage-5-verbatim hypothesis. It is kept separate from the tier count above for that reason.

---

## Datasets

- **MATH-500** (native Level 1–5 difficulty tags; auto-gradable numeric answers) — pilot-stage domain; closed-form grading keeps the difficulty-triangulation and change-point machinery cheap to validate first.
- **GSM8K** — easy-stratum anchor, used to check that the lowest-difficulty end of the curve is not an artifact of MATH-500's own Level-1 items being unrepresentatively hard.
- **AIME 2024 / 2025** — hard-stratum anchor; used for curves only, not per-item statistics, given the small annual item count (~30/year), to probe whether the hardest strata are right-censored within the studied length grid.
- **GPQA-Diamond** (non-mathematical, multiple-choice domain) — stress-tests RQ4's and RQ5's held-out-**domain** claims outside math-heavy, free-response auto-grading, rather than only being observed post hoc within the math corpora above; if the cheap-signal predictor's advantage over the coarse-bin baseline evaporates outside math, that bounds the generality of the non-redundancy finding rather than falsifying it. (This justification replaced an earlier, provenance-only justification — "digest mentions non-math domain transfer" — flagged as too weak during Stage 6's critic round; see `discussion_trace.md`.)
- **A synthetic tunable-difficulty family** (e.g., Countdown or multi-digit arithmetic with a controlled operand count) — guarantees at least some strata where the tipping point is reachable at low budget, de-risking the possibility that every natural-benchmark stratum's curve is still rising at the largest studied length.

## Baselines

Sanity-check comparators only — this is a measurement study, and no research question here is framed as "our procedure beats baseline X." Each baseline gives an informativeness or recovery claim a scale.

- **Fixed thinking budgets at each grid length** (including an always-max-budget policy) — the no-stratification control. If the best fixed budget already sits within 1 percentage point of oracle-stop at matched cost, the boundary map has no allocation value, which is itself an informative outcome rather than a failed comparison.
- **Uniform budget forcing** (per Muennighoff et al., 2025, "s1"), applied identically across all difficulty strata — gives RQ3's difficulty-conditioning claim a concrete "one global budget" alternative to rule out.
- **A reimplemented DEER-style confidence-exit policy** — stopping when a trial answer's confidence crosses a threshold, with no difficulty stratification. Tests whether an existing, already-published training-free stopping rule already captures the tipping point implicitly, without ever localizing or reporting it. (Present in `paper.md`'s own Step-6 Verification for E3/RQ5 from the outset; it had dropped out of an intermediate draft of the assembled paper and was restored — see `pipeline.md`'s Phase G log, now folded into `paper_draft.md`.)
- **A reimplemented three-class prefill-difficulty probe** (per DiffAdapt / AdaptiveThinking) — the coarse-bin decoupling control for RQ4 and RQ5.
- **A position-controlled length-only null feature set** — the second decoupling control for RQ4, isolating trajectory content/order from mere trace-position priors.
- **Per-stratum oracle-stop** (computed in hindsight) — establishes the ceiling against which "substantial fraction recovered" (RQ5) is defined.

---

## RQ1 — Difficulty-proxy triangulation agreement

- **Tier:** mechanism.
- **Target sub-problem:** `sp_difficulty_proxy_validity`.
- **Target hypothesis (verbatim, from Stage 5 `m_difficulty_triangulation`):** "Quintile assignments from the primary model's low-budget solve rate will rank-correlate with dataset-native difficulty tags at Spearman ρ ≥ 0.4, and with a second model's low-budget solve rate at Spearman ρ ≥ 0.4; strata failing both checks will be reported as unreliable rather than used for downstream claims."
- **Setup:** For every tested (model × dataset) cell, compute Spearman rank correlation between the primary model's low-budget-solve-rate quintiles (solve rate over 8 rollouts truncated at 512 thinking tokens, per Stage 5's `m_difficulty_triangulation` proposed approach) and (a) the dataset's native difficulty tags where available, and (b) a second model's own low-budget solve-rate quintiles.
- **Sample-size rationale:** Not separately specified in the sources beyond the shared 8-rollout-per-item pool (at 512-token truncation) used to compute the solve-rate proxy itself (Stage 5 `m_difficulty_triangulation`); no distinct power target is stated for the correlation test.
- **Statistical test:** Spearman rank correlation, threshold ρ ≥ 0.4 on each of the two comparisons.
- **Expected outcome:** Both correlations reach ρ ≥ 0.4; strata that fail both checks are reported as unreliable and excluded from downstream tipping-point claims rather than silently retained.
- **Falsification condition:** Refuted if either correlation falls below 0.4 in a majority of tested cells — meaning the difficulty proxy is closer to a model-specific artifact than to a task-intrinsic quantity, undermining every downstream stratum-conditioned claim built on it.
- **Metrics:** Spearman ρ against native tags; Spearman ρ against a second model's solve rate; fraction of strata excluded as unreliable.

## RQ2 — Sign-flip existence

- **Tier:** mechanism.
- **Target sub-problem:** `sp_changepoint_power`.
- **Target hypothesis (verbatim, from Stage 5 `m_paired_changepoint_test`):** "In at least 2 of 5 difficulty quintiles, the accuracy-vs-length curve will show a statistically significant negative-slope region (peak-to-max contrast ≥3pp, Holm-corrected one-sided bootstrap p<0.05) that replicates in sign across at least 2 of the 3 length-control arms."
- **Setup:** Pilot stage: one model, MATH-500, 7 grid lengths (𝓛 = {256, 512, 1k, 2k, 4k, 8k, 16k}), 8 rollouts per (item, length). Scale-up: at least three models spanning scale, four datasets, 16 rollouts per cell. Grid lengths run under three length-control arms (truncation, forced continuation, natural stopping).
- **Sample-size rationale:** Pilot cells are sized to detect a 5-percentage-point accuracy drop between adjacent grid lengths at α = 0.05, power 0.8 (≥1,200 Bernoulli observations per (stratum, L) cell, per `paper.md` Assumption A6); an underpowered pilot result triggers a pre-committed enlargement in the scale-up rather than a null claim.
- **Statistical test:** Item-paired bootstrap (10,000 resamples, one-sided, Holm-corrected across 5 strata × 3 arms = 15 tests) on the forward accuracy difference between adjacent grid lengths.
- **Expected outcome:** In at least 2 of 5 difficulty quintiles, the peak-to-max accuracy contrast is significantly negative (≥3 percentage points, Holm-corrected p < 0.05).
- **Falsification condition:** Refuted if no quintile, dataset, or model shows a significant negative forward difference anywhere in the studied grid under any length-control arm — in which case the paper's own headline reframes from a boundary map to a well-powered null bounding where such a boundary cannot lie within practical budgets (the pre-committed Global Fallback F-G1).
- **Metrics:** Per-cell accuracy and its bootstrap confidence interval; peak-to-max contrast and its significance; count of quintiles with a detected flip.

## RQ3 — Difficulty-conditioned trend

- **Tier:** mechanism.
- **Target sub-problem:** `sp_changepoint_power`.
- **Target hypothesis (verbatim, from Stage 5 `m_paired_changepoint_test`):** "The localized tipping point will shift to longer lengths as stratum difficulty increases (Jonckheere-Terpstra trend test, p<0.05), with the hardest strata plausibly right-censored rather than reversing order."
- **Setup:** Among strata with a detected tipping point (RQ2), a Jonckheere-Terpstra trend test on the tipping point's length across ordered difficulty quintiles, with right-censored strata assigned maximum rank; the same test repeated on the synthetic tunable-difficulty family's difficulty parameter (≥5 synthetic difficulty levels, per `paper.md`'s E2 Verification).
- **Sample-size rationale:** Not separately specified beyond RQ2's per-cell rollout sizing, since the tipping points fed into this trend test are RQ2's outputs; 5 natural quintiles plus ≥5 synthetic difficulty levels are the stated stratum counts (`paper.md` E2 Verification).
- **Statistical test:** Jonckheere-Terpstra trend test on stratum-level tipping-point length; a reversal check runs the same test with the opposite alternative on the synthetic suite, which must not reject at p < 0.05.
- **Expected outcome:** The trend test rejects the null of no ordering (p < 0.05) on both natural and synthetic suites, with the tipping point increasing (or being right-censored) as difficulty increases, and no significant reversal between the two suites.
- **Falsification condition:** Refuted if the trend test finds no significant ordering (tipping point statistically indistinguishable from a single universal length threshold), or if the ordering reverses between natural and synthetic suites.
- **Metrics:** Per-stratum tipping-point length with bootstrap confidence interval; trend-test statistic and p-value; reversal check between natural and synthetic suites.

## RQ4 — Signal informativeness

- **Tier:** mechanism.
- **Target sub-problem:** `sp_signal_transfer_validity`.
- **Target hypothesis (verbatim, from Stage 5 `m_decoupled_cheap_signals`):** "At least one cheap feature family (entropy-trajectory or early-consistency) achieves AUROC ≥0.65 (95% CI excluding 0.5) for classifying whether marginal gain beyond the 256-token probe point is negative, on held-out strata — and this AUROC is not matched by the length-only null feature set."
- **Setup:** From the first 256 thinking tokens plus four truncated-answer probes (≤512 tokens each), compute entropy-trajectory and early-consistency features; fit a classifier of whether marginal gain beyond the probe point is negative; compare its AUROC against an identically-trained classifier fed only position-controlled length features, on held-out strata. No ground-truth correctness is used at prediction time.
- **Sample-size rationale:** Not separately specified beyond the shared held-out-strata split drawn from RQ2's rollout pool; AUROC confidence intervals are computed by stratified bootstrap over items (`paper.md` E1 Verification).
- **Statistical test:** AUROC with 95% confidence interval via stratified bootstrap over items; threshold is CI excluding 0.5.
- **Expected outcome:** At least one cheap feature family achieves AUROC ≥ 0.65 (95% CI excluding 0.5) on held-out strata, and this AUROC is not matched by the length-only null.
- **Falsification condition:** Refuted if no cheap feature family's AUROC confidence interval excludes 0.5, or if the length-only null achieves statistically indistinguishable AUROC — either would mean the apparent signal is a repackaging of trace length rather than genuine trajectory-level information.
- **Metrics:** Per-feature-family AUROC and its confidence interval; length-only null AUROC for comparison.

## RQ5 — Predictor non-redundancy

- **Tier:** mechanism.
- **Target sub-problem:** `sp_signal_transfer_validity`.
- **Target hypothesis (verbatim, from Stage 5 `m_decoupled_cheap_signals`, refiner-reframed to a non-redundancy claim):** "Stopping at the predicted tipping point recovers at least 50% of the oracle-minus-best-fixed-budget accuracy gap at matched mean token cost — a **non-redundancy** claim about the trajectory-level signal (it must exceed what the coarser 3-class prefill-probe baseline alone recovers), not a claim that this predictor is the best deployable stopping policy in any absolute sense."
- **Setup:** At matched mean token cost, compare accuracy of stopping at the predicted tipping point against the best single fixed budget, a reimplemented DEER-style confidence-exit policy, per-stratum oracle-stop, and a reimplemented three-class difficulty-bin classifier, on held-out strata and held-out task domains (including GPQA-Diamond). Predictor trained/evaluated under cross-stratum and cross-domain holdouts only; cross-model-family transfer is an explicitly declared out-of-scope limitation (Stage 5 scope note), not silently omitted.
- **Sample-size rationale:** Not separately specified beyond RQ2's cell sizing and the held-out split; Spearman ρ(L̂*, L*) at α = 0.01 is used as a predictor-quality gate (`paper.md` E3 metric) ahead of the recovery comparison.
- **Statistical test:** McNemar test on paired per-item correctness between predicted-stop and best fixed budget; oracle-gap recovery fraction comparison (descriptive) against the coarse-bin classifier; descriptive Pareto comparison against the DEER-style baseline.
- **Expected outcome:** All three conditions required (conjunctive, per `paper.md`'s H3 and the Phase G tightening of this RQ's Expected Outcome): (a) predicted-stop beats the best single fixed budget on paired per-item correctness, McNemar p < 0.05; (b) predicted-stop recovers at least 50% of the oracle-minus-best-fixed-budget accuracy gap at matched cost; (c) the recovered fraction exceeds what the coarser difficulty-bin classifier recovers under the same matched-cost comparison. A partial pass (e.g., (b)+(c) without (a)) is reported as such, not rounded up to a full pass.
- **Falsification condition:** Refuted if any of the three conditions fails, or (descriptively) if predicted-stop shows no better showing than the DEER-style confidence-exit policy at matched cost — in which case the trajectory-level signal is redundant with a much cheaper coarse decision or an already-published stopping rule, and the boundary map's practical value is diagnostic rather than actionable as a new stopping policy.
- **Metrics:** Oracle-gap recovery fraction for predicted-stop vs. coarse-bin classifier, at matched mean token cost; McNemar test statistic; descriptive Pareto comparison against the DEER-style confidence-exit policy.

## RQ6 — Cross-arm replication

- **Tier:** mechanism.
- **Target sub-problem:** `sp_intervention_emergence_confound`.
- **Target hypothesis (verbatim, from Stage 5 `m_triangulated_intervention_design`):** "The negative-slope region detected under the truncation arm will replicate in sign (though not necessarily magnitude) under the forced-continuation arm in a majority of quintiles where a flip is detected at all; single-arm-only detections will be reported separately as unconfirmed rather than folded into the headline claim."
- **Setup:** Among quintiles with a detected tipping point under the truncation arm (RQ2), check whether the forced-continuation arm detects a negative-slope region of the same sign; natural stopping is logged observationally for the same comparison where feasible.
- **Sample-size rationale:** Not separately specified beyond the shared three-arm rollout pool defined in RQ2 (same items, same length grid, same per-cell rollout counts, run once per arm).
- **Statistical test:** Cross-arm sign-agreement count/majority check among quintiles with a detected flip (not a separate significance test beyond RQ2's own Holm-corrected bootstrap, which already spans the 3 arms in its multiple-comparison correction).
- **Expected outcome:** The negative-slope region replicates in sign under the forced-continuation arm in a majority of quintiles where truncation detects a flip at all; single-arm-only detections are reported separately as unconfirmed.
- **Falsification condition:** Refuted if a majority of truncation-detected flips fail to replicate in sign under forced continuation — in which case the finding is better explained as an artifact of the truncation-and-forced-answer manipulation than as a property of the reasoning process, and no tipping-point claim from this design can be treated as confirmed.
- **Metrics:** Cross-arm sign-agreement rate among quintiles with a detected flip; count of confirmed vs. unconfirmed (single-arm-only) detections.

---

## Addendum: RQ7 — Mechanism probe (not one of the original Stage 6 RQs)

- **Tier:** mechanism (post-hoc addition — see note below; excluded from the "6 mechanism-tier RQs" count above).
- **Provenance:** Not part of the Stage 5/6 critic-refiner loop. Sourced from `paper.md`'s own Step 6 "Mechanism analysis (M6, added at Phase A re-run per guidance.md Part 6 item 8 / Part 2 A2's evidence standard)" — added because A2's evidence standard requires at least one mechanism analysis beyond the headline localization, explaining *why* the marginal return flips, not only *that* and *where*. Formalized as `RQ7` in `paper_draft.tex` during the Phase G adversarial-review pass (`pipeline.md`'s Phase Log), which found the Abstract's causal "overwrite" sentence had no traced experiment (an orphan claim) until this RQ was added.
- **Target claim (verbatim, from `paper.md`'s Step 6 M6 "Pre-registered prediction"):** "the correct→incorrect flip rate rises sharply past L\*_s relative to before it, and this rise co-occurs with elevated verification/backtracking step density (the mechanism guessed at in Step 0: continued reasoning overwrites an already-correct answer via a verification/backtracking step that itself introduces the error) — not merely a diffuse accuracy decay."
- **Setup:** Restricted to strata with a detected tipping point under RQ2, compare (i) correct→incorrect vs. incorrect→correct answer-flip rates, and (ii) verification/backtracking step density, in the grid-length window just before vs. just after L\*_s, using a paired bootstrap on the before/after contrast. A third measure — correlation between the entropy-trajectory slope feature (RQ4) and the sign of the answer flip at L\*_s — is also computed.
- **Sample-size rationale:** Not separately specified beyond the rollout pool already collected for strata with a detected tipping point (RQ2); no independent power calculation is stated for this probe in the sources.
- **Statistical test:** Paired bootstrap on the before/after contrast in flip rates, Holm-corrected across strata.
- **Expected outcome:** The correct→incorrect flip rate rises significantly after L\*_s relative to before it (p < 0.05), co-occurring with elevated verification/backtracking step density in the same window.
- **Falsification condition:** Refuted if correct→incorrect and incorrect→correct flip rates are statistically indistinguishable before vs. after L\*_s — the localized boundary from RQ2 remains real, but its mechanism is not verification-induced self-overwriting; the Introduction's causal "overwrite" story downgrades to a descriptive co-occurrence ("coincides with," not "is caused by"), and the paper reports the boundary without a mechanism claim.
- **Metrics:** Correct→incorrect and incorrect→correct flip rates before vs. after L\*_s, with bootstrap confidence intervals; verification/backtracking step density before vs. after L\*_s; correlation between entropy-trajectory slope and flip sign at L\*_s.

---

## Global fallback (applies across RQ2 + RQ3)

If the central hypothesis family (RQ2 AND RQ3) fails — no detectable sign flip, or no difficulty structure — the study's archetype pivots from *boundary map* to *well-powered refutation + censoring study* (still `empirical`), per `paper.md`'s pre-committed Global Fallback F-G1: "Across 3 model scales, 5 datasets, and three independent length manipulations totaling N rollouts, we find no difficulty-conditioned regime within practical budgets (≤16k tokens) where additional thinking reduces accuracy — implying that the overthinking premise motivating current stopping-rule and length-penalty methods is either an artifact of specific manipulations or lives beyond deployed budget ranges, and publishing the resulting censored boundary curves as the null landscape those methods must beat."

## Placebo check (applies to RQ2/RQ3/RQ6's shared change-point machinery)

Before any stratum's tipping point is trusted, the identical bootstrap and change-point procedure is run on a null-by-construction control: grid-length labels are randomly permuted within each item's rollout set (severing any true length-accuracy relationship while preserving the marginal accuracy distribution), and the same Holm-corrected test is applied. A non-null detection under this permutation would indicate a pipeline artifact (e.g., multiple-comparison leakage or a miscalibrated bootstrap) rather than a property of the reasoning process, and would block scoring of every downstream RQ until fixed. (Added to `paper_draft.tex`'s Methodology during the Phase G adversarial-review pass; not present in the original Stage 6 confirmed output, carried here for completeness since it directly gates RQ2/RQ3/RQ6's shared statistical machinery. As of the 2026-07-05 post-review revision pass, the same permutation-placebo language is also registered in `../paper.md`'s Mandatory Baselines section as B0's second, null-by-construction job, closing the Phase G to-do against the spec.)
