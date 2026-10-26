# Experiment Design — B4.2: Exchange Rates between Thinking, Sampling, and Verifying under a Fixed Dollar Budget

> Standalone experiment-design spec, assembled from Stage 6's confirmed output in `pipeline.md` (Stage 6 — Experiment Design) and `paper.md`'s own Step 6 (Pre-Registered Experiments) / Step 5 (Formal Problem Definition) / Step 9 (Walking Skeleton). Nothing below is invented beyond those two sources; sample-size figures, statistical-test names, and tolerance thresholds are `paper.md`'s own pre-registered design constants. Status: **specification — no experiments have been run.** This document is meant to be executable as a protocol on its own, without opening the paper.
>
> **Tier accounting (per Stage 6, checked against `study_type = empirical`):** Mechanism-tier: 9 RQs, one per Stage 5 hypothesis (verbatim `target_hypotheses`). Framing-tier: 0 RQs (no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured). Outcome-tier: 0 RQs (`study_type = empirical` forbids "our procedure beats baseline X" framing — every baseline below is a sanity-check comparator or ceiling, never a competitor to beat).

## Design constants (frozen at pre-registration, per `paper.md` Step 6)

- **Grid:** thinking-token cap $L \in \{512, 1024, 2048, 4096\}$; sample count $N \in \{1,2,4,8,16\}$; verifier mode $V \in \{0 = \text{majority vote}, \text{cheap}, \text{strong}\}$; temperature $T=0.8$; 3 budget levels $B_1, B_2, B_3$; matched-cost bin tolerance $\pm 10\%$ of target budget (pre-declared widening amendment to $\pm 15\%$ if a bin fails to populate — logged, not silent).
- **Sample sizes:** pilot stage $n \geq 300$ questions/family (math, code); Stage-2 cross-family replication $n \geq 500$ questions/family (all four families). Pilot $n=300$/family is pre-registered to give power $\geq 0.8$ for a 5-percentage-point reference contrast at $\text{Acc} \approx 0.6$; this is re-checked empirically once pilot data lands, and any cell whose realized power falls below 0.8 is pre-declared **INCONCLUSIVE** for that cell/test only (never scored PASS/FAIL, never silently folded into an aggregate) until Stage-2's $n=500$ resolves it.
- **Statistical tests:** paired bootstrap, 10,000 resamples; permutation tests, 10,000 permutations; likelihood-ratio tests for interaction terms; Holm–Bonferroni correction at $\alpha = 0.05$ across family pairs and budget levels wherever multiple comparisons are made.
- **Oracle arm:** a zero-cost ground-truth selection arm is run at every grid point, per method `m_coverage_selection_decomposition`.

## Datasets (per Stage 6, confirmed)

| family | dataset(s) | verifiability class | justification |
|---|---|---|---|
| Math | MATH-500 | exact-match | Pilot family. Cheap and unambiguous grading makes it the right family to validate the cost meter and fit the first interaction surface before scaling up to the other three families. |
| Code | HumanEval+ / a LiveCodeBench slice | executable | The most verify-heavy family under the pre-registered verifiability ordering (code $\geq$ math $\geq$ MCQ $\geq$ open QA). Needed so the verifiability-stratified replication and the coverage/selection decomposition both have a family where the verifier lever plausibly has the most headroom to show anything at all. |
| MCQ | GPQA-Diamond | option match | An intermediate anchor on the verifiability ordering, needed so the ordering claim isn't just a two-point comparison between math and open QA. |
| Open QA | FRAMES / a SimpleQA subset | rubric-graded | The least verifiable family. Needed both to test whether the verifiability ordering holds at its weakest-signal end, and because it's the family where the coverage/selection confound is sharpest (the rubric judge is itself a verifier-like instrument). |

## Baselines (per Stage 6, confirmed — sanity-check comparators/ceilings, not outcome-tier competitors)

| baseline | justification |
|---|---|
| **Fixed floor allocation** ($L=512, N=1, V=0$) | The necessary "why bother allocating at all" gate. Every lever-value claim is reported relative to this floor; the allocation-moot exclusion rule from Stage 1's `objective` is defined against it — a $(family, budget)$ cell in which nothing beats this floor by a pre-specified margin ($\geq 5$ accuracy percentage points, per `paper.md`'s pre-registered B0 gate) at matched or lower cost is excluded from exchange-rate and frontier-shape claims and reported as **allocation-moot**, not silently dropped or scored as evidence of constancy. |
| **Budget-matched majority-vote control** (reallocates the verifier's dollars into more samples, same cost bin) | The specific control `m_coverage_selection_decomposition` needs — isolates whether a verify-heavy allocation's accuracy gain is attributable to verification or fully explained by the extra candidates the same dollars would have bought instead. |
| **Difficulty-conditioned compute-optimal allocator** (SnellTTC policy, re-priced in dollars) | This is the one prior allocator that already conditions its choice on an interaction-like signal (per-prompt difficulty), so comparing its FLOPs-native decision boundary against this paper's dollar-metered interaction surface (`rq_nv_interaction`, `rq_interaction_magnitude_ordering`) tests whether a difficulty-conditioned policy derived without a cost meter happens to land near the dollar-optimal frontier, or whether re-pricing reveals it was tuned for a different currency than the one that matters at deployment. |
| **Zero-cost ground-truth oracle selector** | The upper-bound arm for `m_coverage_selection_decomposition` — a sanity ceiling, not a competitor. Bounds what any verifier's realized selection quality could ever recover from the same candidate pool. |

---

## RQ1 — `rq_price_robustness`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_cost_commensuration`.
- **Target hypothesis (verbatim, Stage 5 `m_unified_cost_meter`):** "The frontier-shape ordering (which family is most verify-heavy) is preserved under a ±3x perturbation of the input/output and generator/verifier price ratios for at least the majority of tested (family × budget) cells — i.e., the meter's qualitative conclusions are not an artifact of one specific price sheet, even though absolute dollar magnitudes are."
- **Setup:** Recompute the frontier-shape ordering (which family is most verify-heavy at its max-accuracy efficient point) under a $\pm 3\times$ perturbation of the input/output token price ratio and the generator/verifier price ratio, holding everything else fixed, for every tested (family × budget) cell.
- **Sample-size rationale:** Uses the same pilot/Stage-2 grid as all other RQs (no separate sample); robustness is assessed by recomputing the ordering statistic under perturbation across all tested (family × budget) cells, so its power is inherited from the grid's own per-family $n$ (pilot $\geq 300$, Stage-2 $\geq 500$).
- **Statistical test:** Ordering-agreement rate across the perturbation band (majority-agreement threshold across tested cells); no separate hypothesis test beyond the pre-specified majority criterion.
- **Expected outcome:** The ordering is preserved under perturbation for at least the majority of tested cells. Falsified if the ordering changes for more than half of tested cells under the $\pm3\times$ perturbation — that would mean the frontier-shape finding is a price-sheet artifact rather than a structural property of the levers.
- **Metrics:** Ordering agreement rate across the perturbation band, per cell and pooled.

## RQ2 — `rq_nv_interaction`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_lever_interaction`.
- **Target hypothesis (verbatim, Stage 5 `m_interaction_surface_model`):** "The N×V interaction term is statistically significant (likelihood-ratio test, Holm-corrected) on at least one task family, meaning a verifier's exchange rate measured at one sample count N does not transfer unchanged to a different N."
- **Setup:** Fit the interaction-aware response surface (accuracy as a function of $L$, $N$, verifier mode, and realized cost, with explicit $N \times V$ and $L \times V$ interaction terms) on the pilot grid (MATH-500) and test the sample-count × verifier-mode interaction term against the additive model.
- **Sample-size rationale:** Pilot $n \geq 300$/family, pre-registered for power $\geq 0.8$ on a 5pp reference contrast at $\text{Acc}\approx0.6$; if achieved power for this specific interaction term falls short, the cell is pre-declared INCONCLUSIVE rather than scored, pending the Stage-2 $n=500$ replication.
- **Statistical test:** Likelihood-ratio test of the $N\times V$ interaction term against the additive (no-interaction) model, Holm-corrected across families and fairness references where applicable.
- **Expected outcome:** The interaction term is statistically significant on at least one task family, meaning a verifier's exchange rate measured at one sample count does not transfer unchanged to a different sample count. Falsified if the likelihood-ratio test finds no significant interaction on any tested family — that would mean the additive (constant-exchange-rate) model already suffices.
- **Metrics:** Interaction-term coefficient and its likelihood-ratio statistic, per family.

## RQ3 — `rq_interaction_magnitude_ordering`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_lever_interaction`.
- **Target hypothesis (verbatim, Stage 5 `m_interaction_surface_model`):** "The magnitude of the L×V interaction term is smaller than the N×V interaction term's magnitude in a majority of tested cells where both are significant — i.e., verifier value interacts more strongly with how many candidates it screens than with how long each candidate is."
- **Setup:** Among cells where both the $N\times V$ and $L\times V$ interaction terms (from RQ2's fitted surface) are significant, compare their fitted magnitudes.
- **Sample-size rationale:** Conditional on RQ2's grid and significance filter; no additional sampling beyond the shared pilot/Stage-2 grid, restricted to the subset of cells where both terms clear significance.
- **Statistical test:** Comparison of fitted interaction-term magnitudes (ratio) across qualifying cells; majority-of-cells criterion.
- **Expected outcome:** The sample-count interaction's magnitude exceeds the thinking-cap interaction's magnitude in a majority of qualifying cells. Falsified if the thinking-cap interaction's magnitude is equal to or exceeds the sample-count interaction's magnitude in a majority of qualifying cells.
- **Metrics:** Ratio of interaction-term magnitudes, per qualifying cell.

## RQ4 — `rq_crossfamily_shape`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_verifiability_heterogeneity`.
- **Target hypothesis (verbatim, Stage 5 `m_verifiability_stratified_replication`):** "The permutation test rejects cross-family equality of allocation-mix composition for at least 2 of 6 family pairs at Holm-corrected α=0.05."
- **Setup:** Run the identical matched-cost grid protocol across all four task families and compute a permutation test on Aitchison distance between each family pair's efficient-set allocation-mix composition at matched budget levels.
- **Sample-size rationale:** Stage-2 cross-family replication, $n \geq 500$ questions/family across all four families (larger than the $n=300$ pilot because this RQ needs simultaneous power across 6 family pairs × 3 budget levels after Holm correction).
- **Statistical test:** Permutation test, 10,000 permutations, on Aitchison distance between family-pair efficient-set allocation-mix compositions, Holm-corrected across the six family pairs and tested budget levels.
- **Expected outcome:** The test rejects cross-family equality for at least 2 of 6 family pairs at Holm-corrected $\alpha=0.05$. Falsified if no family pair shows a significant difference at any tested budget level — that would mean a single allocation policy transfers across verifiability regimes without adjustment.
- **Metrics:** Aitchison distance and permutation p-value, per family pair and budget level.

## RQ5 — `rq_verifiability_ordering`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_verifiability_heterogeneity`.
- **Target hypothesis (verbatim, Stage 5 `m_verifiability_stratified_replication`):** "The verify-heavy dollar share at each family's max-accuracy efficient point follows the pre-registered verifiability ordering (code ≥ math ≥ MCQ ≥ open QA), with the code-vs-open-QA gap ≥0.10 absolute dollar share."
- **Setup:** At each family's max-accuracy efficient point, compute the verifier's dollar share of total spend, and compare the four families against the pre-registered ordering (executable code $\geq$ exact-match math $\geq$ multiple-choice $\geq$ rubric-graded open QA).
- **Sample-size rationale:** Same Stage-2 cross-family grid as RQ4 ($n \geq 500$/family, all four families), since both RQs depend on the same efficient-set estimation per family.
- **Statistical test:** Ordering comparison against the pre-registered ranking, with a fixed absolute-gap threshold (0.10 dollar share) rather than a significance test; assessed at a majority of tested budget levels.
- **Expected outcome:** The ordering holds, with the code-versus-open-QA gap at least 0.10 absolute dollar share, at a majority of tested budget levels. Falsified if the observed ordering contradicts the pre-registered ordering, or the gap falls below 0.10 at every tested budget level.
- **Metrics:** Verifier dollar-share vector per family, per budget level.

## RQ6 — `rq_bin_population`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_stochastic_cost_matching`.
- **Target hypothesis (verbatim, Stage 5 `m_matched_cost_binning`):** "At least 8 grid configurations populate each matched-cost bin per family and budget level using the pre-specified ±10% tolerance, without needing the pre-declared ±15% widening amendment."
- **Setup:** Count the number of distinct grid configurations whose expected pilot cost (estimated from pilot token statistics) falls within the pre-specified $\pm 10\%$ tolerance band of each target budget level, per family and budget level.
- **Sample-size rationale:** Assessed on the pilot token-statistics run (pre-grid), before the main $n\geq300$/family pilot or $n\geq500$/family Stage-2 grid is executed — this is a design-validity check on the grid itself, not an accuracy comparison.
- **Statistical test:** Configuration count against a fixed threshold (8 configurations); no inferential test — a pre-declared, deterministic acceptance criterion, with the $\pm15\%$ widening amendment triggered (and logged) if the threshold is missed at $\pm10\%$.
- **Expected outcome:** At least 8 configurations populate every matched-cost bin under the $\pm10\%$ tolerance, without triggering the widening amendment. Falsified if any bin requires the amendment to reach 8 configurations.
- **Metrics:** Configuration count per bin, per family and budget level.

## RQ7 — `rq_adjustment_loadbearing`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_stochastic_cost_matching`.
- **Target hypothesis (verbatim, Stage 5 `m_matched_cost_binning`):** "Frontier confidence bands computed with realized-cost regression adjustment are narrower than bands computed from nominal-cost grouping alone, on a majority of tested bins — demonstrating the adjustment step is load-bearing, not cosmetic."
- **Setup:** Compute frontier confidence bands twice per family and budget level — once using the realized-cost regression adjustment, once using nominal-cost grouping alone — and compare band widths.
- **Sample-size rationale:** Uses the same matched-cost bins populated for RQ6, drawing on the pilot/Stage-2 grid's realized-cost data within each bin; no additional sampling.
- **Statistical test:** Comparison of bootstrap confidence-band widths (paired, 10,000 resamples) between the two adjustment methods, majority-of-bins criterion.
- **Expected outcome:** Bands with the realized-cost adjustment are narrower than bands from nominal grouping alone, on a majority of tested bins. Falsified if the two approaches yield equally wide (or the adjustment yields wider) bands on a majority of bins — that would mean nominal-cost grouping suffices.
- **Metrics:** Confidence-band width under each method, per bin.

## RQ8 — `rq_verifier_beats_coverage_control`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_selection_vs_coverage_confound`.
- **Target hypothesis (verbatim, Stage 5 `m_coverage_selection_decomposition`):** "The verifier-lever accuracy gain over its budget-matched majority-vote control is statistically significant (paired bootstrap, Holm-corrected p<0.05) for the strong-verifier condition on at least one task family — i.e., at least one measured 'verifier value' finding survives this control rather than being fully explained by reallocated coverage."
- **Setup:** For every verify-heavy point on the fitted frontier, compare its accuracy against the budget-matched majority-vote control (identical dollars reallocated into additional samples at zero verifier cost) at the same cost bin.
- **Sample-size rationale:** Uses the pilot ($n\geq300$/family) and Stage-2 ($n\geq500$/family) grids' verify-heavy efficient points and their matched majority-vote control arms, run at the same cost bin for a like-for-like paired comparison.
- **Statistical test:** Paired bootstrap, 10,000 resamples, Holm-corrected across families, comparing strong-verifier accuracy against the budget-matched majority-vote control.
- **Expected outcome:** The strong-verifier condition's accuracy gain over its control is statistically significant on at least one task family. Falsified if no task family shows a significant gain — that would mean every measured "verifier value" finding is fully explained by the extra candidates the same dollars would have bought instead.
- **Metrics:** Paired accuracy difference and bootstrap confidence interval, per family.

## RQ9 — `rq_oracle_gap_shrinks`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_selection_vs_coverage_confound`.
- **Target hypothesis (verbatim, Stage 5 `m_coverage_selection_decomposition`, post-refiner):** "The oracle-minus-strong-verifier accuracy gap at matched (L,N) shrinks — rather than staying flat or widening — as N increases on at least one task family, i.e., additional candidates make the verifier's realized selection quality converge toward the coverage ceiling rather than leaving a constant or growing amount of realizable accuracy on the table."
- **Setup:** At fixed thinking cap, compare the accuracy gap between the zero-cost ground-truth oracle selector and the strong verifier across increasing sample counts $N$, on each task family.
- **Sample-size rationale:** Uses the oracle arm run at every grid point (per `m_coverage_selection_decomposition`), across the same pilot/Stage-2 $N \in \{1,2,4,8,16\}$ sweep; the trend is assessed across this $N$ sweep rather than requiring separate sample-size justification.
- **Statistical test:** Trend comparison of the oracle-minus-verifier accuracy gap as a function of $N$ (monotonicity/direction check), per family; no single point-estimate significance test, since the hypothesis is about the gap's trajectory.
- **Expected outcome:** The gap shrinks — rather than staying flat or widening — as sample count increases, on at least one task family. Falsified if the gap stays flat or widens with sample count on every tested family — that would mean additional candidates do not help the verifier close in on the coverage ceiling.
- **Metrics:** Oracle-minus-verifier accuracy gap as a function of sample count, per family.

---

## Cross-check against Stage 6 tier accounting

All 9 RQs above are mechanism-tier, matching Stage 6's confirmed tier accounting (9 mechanism / 0 framing / 0 outcome). Every `target hypothesis` field above is copied verbatim from the Stage 5 confirmed hypothesis text as carried into Stage 6's `target_hypotheses` column in `pipeline.md` — no paraphrase. Setup/statistical-test/expected-outcome/metrics content is drawn from `paper_draft.md`'s Experiments section (RQ1–RQ9, same order and numbering as this document) and `paper.md`'s Step 6 design constants (grid, sample sizes, bootstrap/permutation parameters, Holm correction, INCONCLUSIVE rule); no new numbers or claims are introduced here beyond those two sources.

Keep this document synchronized with `paper_draft.md`'s Experiments section: a late edit to one should be mirrored in the other.
