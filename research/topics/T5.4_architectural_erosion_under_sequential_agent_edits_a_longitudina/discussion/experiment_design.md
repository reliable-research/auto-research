# Experiment Design — T5.4 (standalone protocol)

> Extracted from `pipeline.md`'s confirmed Stage 6 output (research questions, tiers, target hypotheses verbatim from Stage 5) and `paper.md`'s Step 6 / Step 9 / Assumptions (A1–A7) design content. Nothing here is invented beyond those two sources — this document exists so the study can be executed without opening the paper. Status: **pre-registered design, no experiments run yet.**

## Tier accounting (study_type = empirical)

- **Mechanism-tier: 6 RQs** — one per Stage 5 hypothesis, matched verbatim.
- **Framing-tier: 0 RQs** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`; none manufactured to fill the tier.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The baselines below are sanity-check comparators only, never a competitor to beat.

## Datasets

- **SWE-bench Verified**, grouped by repository and ordered chronologically by issue creation date, restricted to the three densest-coverage repositories (django/django, sympy/sympy, astropy/astropy). *Justification:* real, chronologically dateable issue-derived tasks on Python repositories with declarable import-layer architectures, letting a serial task sequence be built on genuine development history rather than a synthetic one.
- **SWE-bench Lite (secondary)**. *Justification:* used specifically to construct the second, permuted-order sequence needed for `rq_factor_attribution`'s (RQ6) ordering factor when a given repository's Verified-instance density is too thin to support two independent chronological orderings; without it, ordering could only be tested confounded with repository choice. (This justification replaced an earlier draft that only cited "digest N8 lists it as a secondary source" — flagged as a `[major]` weak-justification issue in Stage 6 round 1 and fixed in the refiner pass.)

## Baselines (sanity-check comparators, not competitors to beat)

- **B0 — Human-gold control.** The actual developer PR patches applied serially under identical ordering, rebasing, and attrition rules as the agent arm. The necessary control for every agent-attributable-erosion claim: if agent trajectories do not separate from B0, there is no agent-specific problem, only task-driven structural growth.
- **B-alt — Single-shot control** (reuses `rw_swebench`'s protocol per Stage 3). The same agent, same pinned backbone, same retry budget (k=3), solving each task from its own original base commit with no accumulated history. Rules out "erosion is just the sum of per-patch damage, not sequence-amplified" — i.e., isolates whether accumulated history specifically compounds drift.

## Design constants (paper.md Step 6, hardened)

Scale-up = 3 repos (django, sympy, astropy) × 3 agent configs × 2 orderings × 3 seeds = 54 agent trajectories (~20 steps each) + 6 human-gold + 3 single-shot control trajectories (~1,080 step observations total). α = 0.05, Holm–Bonferroni correction within each hypothesis's declared test family. All longitudinal models are mixed-effects (`lme4`-style) with trajectory-level random slopes. Pilot stage (walking skeleton, Step 9): 1 repository (django) × 1 agent configuration × 1 ordering × 3 seeds, ~20 tasks, gated go/no-go on feasibility (S1–S6) before any scale-up spend.

---

## RQ1 — `rq_gate_blindness_verified`

- **Tier:** mechanism (targets `sp_oracle_blindness`)
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "A static scan of every task's gate test files across the studied repositories finds zero assertions referencing import-graph structure, module boundaries, or layering — confirming the acceptance signal is structurally uninformative by construction, not merely in practice."
- **Setup:** For every task's designated test files across the three primary repositories, statically scan for assertions that reference import structure, module membership, or declared layering, prior to any experimental run.
- **Sample-size rationale:** Exhaustive census, not a sampled statistical test — every gate test file for every task across all three primary repositories is scanned (per paper.md A3: "static scan of all gate tests per repo before runs"). No power calculation applies because this is a definitional/existence check, not an inferential contrast.
- **Statistical test:** None — a deterministic static-analysis scan (count of qualifying assertions found), not a hypothesis test.
- **Expected outcome:** Zero qualifying assertions are found across all scanned test files, confirming the acceptance signal is structurally uninformative by construction rather than merely in the studied instances.
- **Metrics:** Count of qualifying assertions found, by repository and by task.

## RQ2 — `rq_agent_excess_erosion`

- **Tier:** mechanism (targets `sp_counterfactual_definition`)
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "The agent arm's fixed-effect trend exceeds the human-gold arm's trend, for at least two of three primary structural metrics, by a pre-registered effect-size floor on the shared task-intersection contrast."
- **Setup:** Pilot: 1 repository (django) × 1 agent configuration × 1 ordering × 3 seeds, ~20 tasks, contrasted against the matched human-gold arm on the same sequence; go/no-go gated on walking-skeleton feasibility (minimum fraction of tasks surviving test-rebasing, bitwise-deterministic metric re-run). Scale-up: 3 repositories × 3 agent configurations × 2 orderings × 3 seeds (54 agent trajectories, ~20 steps each) contrasted against per-repository human-gold and single-shot control arms. Model: `Φ_m ~ step × arm + gold-patch-LOC + issue-age + (step | repo:seed)`, step×arm interaction as the estimand of interest.
- **Sample-size rationale:** 54 agent + 6 human-gold trajectories (~1,080 step observations) per paper.md A7. Per-condition cells in the factorial (3 agent configs × 3 repos × 2 orderings × 3 seeds ⇒ n=3 trajectories/cell before pooling) must be large enough for the per-factor analysis to be interpretable. Gate S6 (Step 9): before scale-up, a power calculation from the pilot's observed step-to-step metric variance must project ≥0.8 power to detect the pre-registered Cliff's δ ≥ 0.33 floor for the 3 primary metrics at n=54 vs n=6; if under-powered, the finding is pre-declared INCONCLUSIVE rather than a null result, and scale-up is deferred (more seeds, not more conditions).
- **Statistical test:** Mixed-effects LRT on the step×arm interaction term, Holm-corrected across the 3 primary metrics (cyclic dependencies, layering violations, duplication); Cliff's δ ≥ 0.33 on per-trajectory slope pairs (agent vs. human) required jointly with significance; per-trajectory Mann-Kendall τ as a nonparametric robustness cross-check; contrasts computed only on the task intersection completed by both arms.
- **Expected outcome:** For at least two of the three primary structural metrics, the step×arm interaction is positive and clears the pre-registered effect-size floor on the shared task-intersection contrast, indicating agent-attributable excess erosion beyond what the human-gold arm's own trend already accounts for. The single-shot control contrast is reported alongside this result: if excess erosion holds against the human-gold arm but serial and single-shot cumulative drift are statistically indistinguishable, the finding is reframed as "erosion is per-patch additive, not sequence-amplified."
- **Metrics:** Per-metric step×arm interaction estimate and confidence interval; per-trajectory Mann-Kendall trend statistic; seed-level dispersion.

## RQ3 — `rq_counterfactual_necessity`

- **Tier:** mechanism (targets `sp_counterfactual_definition`)
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Within-arm-only drift, without the counterfactual contrast, is not by itself sufficient evidence of agent-attributable erosion — demonstrated by at least one studied trajectory pair where within-arm drift is present in both arms at statistically indistinguishable rates."
- **Setup:** Among all studied trajectory pairs (agent arm and its matched human-gold counterfactual on the same task sequence, drawn from the same 54+6 trajectory pool as RQ2), identify pairs where both arms show a statistically significant within-arm trend, and compare the two arms' trend magnitudes directly.
- **Sample-size rationale:** This is an existence claim (≥1 qualifying pair), not a population-level powered test — it draws on the same 54 agent + 6 human-gold trajectory pool built for RQ2, requiring no separate sample.
- **Statistical test:** Per-pair trend-magnitude difference and its confidence interval, testing for statistical indistinguishability between arms among pairs that individually show significant within-arm drift.
- **Expected outcome:** At least one qualifying trajectory pair shows within-arm drift present in both the agent and human-gold arms at statistically indistinguishable rates, demonstrating that within-arm drift by itself does not imply agent-attributable erosion.
- **Metrics:** Count and identity of qualifying trajectory pairs; per-pair trend-magnitude difference and its confidence interval.

## RQ4 — `rq_trend_test_agreement`

- **Tier:** mechanism (targets `sp_slow_drift_detection`)
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Per-trajectory Mann-Kendall trend tests and the mixed-effects slope estimate agree in sign for at least 80% of trajectories exhibiting any drift — i.e., the two independent statistical readings of 'is this trajectory drifting' are not in tension."
- **Setup:** Among trajectories flagged by either the mixed-effects slope estimate or the per-trajectory Mann-Kendall test as showing any drift, compare the sign of the two readings.
- **Sample-size rationale:** The qualifying set is not fixed in advance by the scale-up's 54-trajectory total, since it is conditioned on trajectories showing *any* drift. At least 10 qualifying trajectories across the scale-up are required before this RQ is treated as adequately powered for the 80% target; if fewer qualify, the finding is reported descriptively (raw agreement count) rather than as a percentage, with the qualifying-set size stated alongside the result.
- **Statistical test:** Sign-agreement rate (descriptive proportion) between the mixed-effects slope sign and the Mann-Kendall trend sign among qualifying trajectories, conditional on the ≥10-trajectory power threshold.
- **Expected outcome:** The mixed-effects slope sign and the Mann-Kendall trend sign agree in at least 80% of qualifying trajectories, conditional on at least 10 trajectories qualifying.
- **Metrics:** Sign-agreement rate among qualifying trajectories; qualifying-set size, reported alongside every result from this RQ.

## RQ5 — `rq_mechanism_loadbearing`

- **Tier:** mechanism (targets `sp_attribution_under_cost`)
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Removing the patch-level mechanism features (cross-layer imports, duplication delta, edit locality) from the within-trajectory delta regression drops its explained variance by at least half, demonstrating these three features are load-bearing carriers of the measured drift rather than incidental correlates."
- **Setup:** Within each trajectory, regress per-step metric deltas on the three patch-level features (cross-layer import edges, duplication delta, edit locality) plus trajectory fixed effects; compare the explained variance of this model against an ablated model with the three features removed.
- **Sample-size rationale:** Per-step metric deltas within each of the 54 agent + 6 human-gold trajectories (~1,080 step observations per A7), with trajectory fixed effects absorbing between-trajectory variation.
- **Statistical test:** Nested-model comparison (full regression vs. ablated regression with the three features removed); explained-variance (R²) drop, threshold ≥50%.
- **Expected outcome:** Removing the three features from the regression drops explained variance by at least half, indicating the features are load-bearing carriers of the measured drift rather than incidental correlates of it.
- **Metrics:** Explained-variance ratio (full model vs. ablated model); per-feature regression coefficients and confidence intervals.

## RQ6 — `rq_factor_attribution`

- **Tier:** mechanism (targets `sp_attribution_under_cost`)
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "At least one of the four declared factors (agent configuration, task type, ordering, lagged prior-erosion state) attains a significant likelihood-ratio test against the null mixed model, net of the other three, demonstrating erosion rate is condition-dependent rather than uniform across the studied factorial."
- **Setup:** Regress trajectory-level erosion-rate estimates on the four declared factors (agent configuration, task type, ordering, lagged prior-erosion state) via likelihood-ratio tests against a null mixed model, each factor's effect assessed net of the other three.
- **Sample-size rationale:** Factorial cells: 3 agent configs × 3 repos × 2 orderings × 3 seeds ⇒ n=3 trajectories/cell before pooling (54 trajectories total, per paper.md A7); Gate S6 requires a pre-scale-up power projection (≥0.8) for the per-factor LRT to be interpretable, else the affected cell/family is pre-declared INCONCLUSIVE and named "untested, not ruled out" rather than reported as a null finding.
- **Statistical test:** Likelihood-ratio test per factor against the null mixed model, Holm-corrected across the 4-factor family; directional sign and marginal-R² contribution reported per significant factor.
- **Expected outcome:** At least one of the four factors attains a significant likelihood-ratio test net of the others, indicating erosion rate is condition-dependent rather than uniform across the studied factorial.
- **Metrics:** Per-factor likelihood-ratio statistic and marginal-R² contribution; directional sign of each significant factor.

---

**Keep synchronized with `paper_draft.md`'s Experiments section and `pipeline.md`'s Stage 6 record.** If a late edit changes the design in one, change it in the others.
