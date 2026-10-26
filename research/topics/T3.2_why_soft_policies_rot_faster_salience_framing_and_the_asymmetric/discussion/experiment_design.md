# Experiment Design — T3.2: Salience, Framing, or Prior? Attributing the Asymmetric Decay of Soft and Hard In-Context Constraints

> Standalone protocol document, per the `auto-research-discussion` skill's "Final deliverables" spec (deliverable 2). Built from Stage 6's confirmed output in `pipeline.md` (see `discussion_trace.md` for the full Stage 6 critic/refiner round) and from `../paper.md`'s own Step 6 "Pre-Registered Experiments" section. Nothing below is invented beyond those two sources. Status: **specification — no experiments have been run; all numbers are pre-registered design targets, not results.** `study_type = empirical`; this document should be executable as a protocol without opening `paper_draft.md`. Keep synchronized with `paper_draft.md`'s Experiments section if either is edited later.

## Tier accounting

Checked against `study_type = empirical` (Stage 1's confirmed study type; forbids "our procedure beats baseline X" outcome-tier framing):

- **Mechanism-tier: 6 RQs** — one per Stage 5 hypothesis, matched one-to-one, verbatim (below).
- **Framing-tier: 0 RQs** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`; none manufactured to pad the count.
- **Outcome-tier: 0 RQs** — the baselines below are sanity-check comparators only, never a competitor to beat.

## Datasets

- **LMSYS-Chat-1M** — supplies the distractor-turn pool used to pad conversations to a realistic long horizon without hand-authoring filler. This is the same padding protocol PrefEval already validated for this purpose, reused here rather than invented fresh.
- **IFEval** — supplies rule-checkable instruction-constraint templates, needed for the rule-verifiable subset of the constraint-pair bank that both RQ2/RQ3's cleanest cells and the difficulty-artifact sanity check depend on. Graded judge-based verifiers alone would confound "soft decays faster" with "judge-scored constraints decay faster."
- **HEx-PHI and AdvBench** — standard, named hard-norm probe-request taxonomies, needed to instantiate the "hard" side of matched pairs with established harmful-instruction categories whose severity is already externally calibrated, rather than inventing ad hoc ones.

## Baselines

Sanity-check comparators, not outcome-tier competitors — this is a measurement study, and no RQ here is framed as "our procedure beats baseline X."

- **No-injection floor arm** — identical harness with the constraint statement never injected. Establishes that turn-1 adherence is caused by injection at all, so "decay" means regression toward a measured no-constraint floor, not toward zero from an undefined starting point. (Corresponds to `paper.md` Step 6's "B0" floor component.)
- **No-manipulation natural-wording replication arm** (standard wording, sys-head, repetition 1) — the first, necessary check of whether the reported ~8x-style premise gap even replicates in matched pairs, independent of any manipulated-factor claim below; tests Assumption A1 before anything else is asked of the design. (Corresponds to `paper.md` Step 6's "B0" replication component; must show `G > 1` or the global fallback F-G1 fires.)
- **Naive every-k-turn verbatim-restatement heuristic** — a mitigation practitioners already use informally with no theoretical grounding; checks whether the study's own repetition-factor findings are at least consistent with what ad hoc practice already does.
- **SinkTrack-style training-free context anchoring** (open-weights models only) — the one prior method in the related-work set that treats positional salience as *the* operative mechanism; an informative sanity comparator for whether a competing salience-only intervention produces a similar or different effect size than this design's own position/repetition manipulation.
- **B-alt — strongest-alternative-explanation control** (from `paper.md` Step 6's "Mandatory baselines," carried into this protocol since it is a named baseline in that source even though Stage 6's own draft did not restate it): the rival explanation that "soft rots faster" is really a difficulty/verifiability artifact — soft constraints are intrinsically harder to satisfy and scored by graded verifiers. Matched arm: restrict analysis to pairs with (i) rule-based binary verifiers on both sides, (ii) turn-1 adherence ≥ 0.95 for both types, (iii) no-injection floors within 10 points of each other. Pre-registered check: the subset gap `log G_subset` must lie within ±50% of the full-bank `log G`; if the gap vanishes in this subset, the difficulty-artifact explanation wins and the mechanism-attribution claims (RQ2–RQ4) are withdrawn in favor of the artifact finding.

## Execution order

`rq_reactivity_equivalence` (RQ6) must be evaluated first, on the calibration subsample, before `rq_factor_significance` (RQ2), `rq_manipulated_share` (RQ3), or `rq_boosted_closure` (RQ4) are treated as trustworthy. If the equivalence test fails (the interaction confidence interval extends outside [0.80, 1.25]), the three gated RQs must be rerun on the reactivity-free between-conversation design, or their scope explicitly narrowed, before any mechanism-attribution claim is reported. (Verbatim from Stage 6's refiner pass; also stated in `paper.md`'s Step 6 as "RUN FIRST — gates E1/E2.")

---

## RQ1 — `rq_pair_bank_survival`

- **Tier:** mechanism.
- **Target sub-problem:** `sp_matched_pair_construction`.
- **Target hypothesis (verbatim, Stage 5/Stage 6):** "At least 80% of constructed pairs will survive both the covariate-matching construction criteria and the turn-1 baseline-adherence audit (≤5-point difference) without requiring re-authoring."
- **Setup:** 5 matched pairs restricted to rule-verifiable constraints (no judge-based verifiers) are authored and audited on covariate-matching criteria (topic, length, verifier class) at construction time, then piloted on one open-weights instruct model for 30-turn conversations with probes every 5 turns across 5 seeds (75 conversations total), checking each pair's turn-1 baseline-adherence difference. The full pilot bank (20 pairs, both rule- and judge-based) repeats the same two-stage audit before entering the main factorial.
- **Sample-size rationale:** the 5-pair/75-conversation slice is the minimum-viable check needed to validate the audit procedure itself before committing to authoring the full 20-pair pilot bank; the full bank's 20-pair size is the Stage-1 pilot design constant shared with RQ2 (below), sized jointly for the pilot factorial's power target, not for this RQ's own audit in isolation.
- **Statistical test:** none (a pre-registered proportion threshold against an audit pass/fail criterion, not a hypothesis test); pair-survival rate is reported directly against the 80% threshold.
- **Expected outcome:** at least 80% of constructed pairs survive both the covariate-matching construction criteria and the turn-1 baseline-adherence audit (≤5-point difference) without requiring re-authoring.
- **Metrics:** pair-survival rate through each audit stage; distribution of turn-1 adherence differences among surviving pairs.

## RQ2 — `rq_factor_significance`

- **Tier:** mechanism.
- **Target sub-problem:** `sp_confound_orthogonalization`.
- **Target hypothesis (verbatim, Stage 5/Stage 6):** "At least one manipulated factor block (wording, position, or repetition) shows a statistically significant factor×type×turn interaction at Holm-Bonferroni-corrected α=0.05."
- **Setup:** Pilot stage: 2 models × 20 matched pairs × a 2×2×2×2 factorial (type: soft/hard × wording: advisory/imperative × position: system-head/mid-turn-10 × repetition: 1/3), 30-turn conversations with probes every 5 turns, 3 seeds per cell, ≈960 conversations per model (1,920 total, per-cell n=60). Scale-up: ≥6 models across ≥3 model families × 40 pairs × 3-level wording and position factors × repetition {1, 3, 5}, horizon extended to 100 turns on a fractional-factorial subsample.
- **Sample-size rationale:** the pilot's 20 pairs and ≈960 conversations per model (per-cell n=60) are sized for ≥80% power to detect an interaction hazard ratio of 1.5 at α=0.05, to be confirmed by simulation before launch (the simulation script is part of the pre-registration artifact); an underpowered pilot result triggers the pre-committed scale-up rather than a null claim. Per-cell power is checked individually, not only for the pooled design: any cell whose simulated power falls below 80% is marked `INCONCLUSIVE` before data collection, never reported as a null effect.
- **Statistical test:** likelihood-ratio tests on the mixed-effects discrete-time cloglog hazard model (`hazard ~ turn × type × wording × position × repetition + (1|pair) + (1|model)`) for each factor×type×turn interaction, Holm-Bonferroni corrected across the three mechanism-factor tests; robustness checks: Weibull refit, leave-one-pair-out, per-model subgroup fits.
- **Expected outcome:** at least one of wording, position, or repetition shows a statistically significant factor×type×turn interaction after Holm-Bonferroni correction.
- **Metrics:** per-factor interaction coefficients and corrected p-values; per-cell hazard ratios; soft/hard hazard ratio `G` with 95% CI.

## RQ3 — `rq_manipulated_share`

- **Tier:** mechanism.
- **Target sub-problem:** `sp_confound_orthogonalization`.
- **Target hypothesis (verbatim, Stage 5/Stage 6):** "The manipulated factor blocks (salience + framing) jointly absorb more than 50% of the type×turn gap coefficient's partial-R², rather than the majority of the gap surviving unexplained by any manipulated factor."
- **Setup:** dominance analysis / partial-R² decomposition of the type×turn coefficient `β_{τ×turn}` from the same fitted model as RQ2, comparing the combined share attributable to the wording, position, and repetition factor blocks against the share attributable to the prior-strength proxy covariates (RQ5).
- **Sample-size rationale:** uses the same fitted model and sample as RQ2 (no additional data collection); the decomposition's reliability inherits RQ2's per-cell power characterization.
- **Statistical test:** dominance-weight / partial-R² decomposition (a variance-attribution procedure, not a significance test in isolation) computed on the RQ2 model fit.
- **Expected outcome:** the manipulated factor blocks jointly absorb more than 50% of the type×turn coefficient's partial-R².
- **Metrics:** dominance-weight/partial-R² share per factor block and for the prior-proxy covariates.

## RQ4 — `rq_boosted_closure`

- **Tier:** mechanism.
- **Target sub-problem:** `sp_confound_orthogonalization`.
- **Target hypothesis (verbatim, Stage 5/Stage 6):** "The boosted-soft cell achieves gap closure κ_close ≥ 0.5 (bootstrap 95% CI lower bound > 0.25) while its half-life remains statistically distinguishable from the standard-hard cell (half-life-ratio CI excludes 1) — presentation narrows but does not eliminate the gap."
- **Setup:** within the same fitted model as RQ2/RQ3, a specific "boosted-soft" cell (imperative wording, system-head position, repetition five) is contrasted against the standard-soft and standard-hard cells; gap-closure fraction `κ_close = [log t½(boosted-soft) − log t½(std-soft)] / [log t½(std-hard) − log t½(std-soft)]` and half-life ratios are computed with 10,000-resample bootstrap confidence intervals at the conversation level.
- **Sample-size rationale:** uses the same fitted model and sample as RQ2 (no additional data collection beyond ensuring the boosted-soft cell is populated within the factorial grid); this is a single pre-registered contrast, so no multiple-comparison correction across cells is applied (only within the family of two directional falsification conditions below).
- **Statistical test:** planned single contrast within the fitted model; bootstrap CIs (10,000 resamples, conversation-level resampling); α=0.05 (no correction needed — one pre-registered contrast).
- **Expected outcome:** `κ_close ≥ 0.5` with a bootstrap 95% CI lower bound above 0.25, while the boosted-soft cell's half-life remains statistically distinguishable from the standard-hard cell's (half-life-ratio CI excludes 1).
- **Metrics:** `κ_close` with bootstrap CI; boosted-soft-versus-standard-hard half-life ratio with CI.

## RQ5 — `rq_prior_proxy_signal`

- **Tier:** mechanism.
- **Target sub-problem:** `sp_prior_proxy_triangulation`.
- **Target hypothesis (verbatim, Stage 5/Stage 6):** "The prior-strength proxies (no-injection compliance rate and base-vs-instruct compliance delta) have standard deviation greater than 0.1 and Spearman correlation greater than 0.3 with each other across constraints, indicating shared, non-degenerate signal rather than uninformative or contradictory readings."
- **Setup:** no-injection zero-shot compliance rate and base-versus-instruct compliance delta are measured across all constructed constraints on the open-weights model pair (a third proxy, per-token KL divergence on the constraint-violating continuation, is measured where weights are accessible and entered as a covariate but is not part of this RQ's own pass/fail criterion); their standard deviation and Spearman correlation with each other are computed.
- **Sample-size rationale:** measured across the full constructed constraint bank (the same pairs authored for RQ1/RQ2), not a separately sized sample — the proxy battery rides on the existing bank rather than requiring new data collection.
- **Statistical test:** standard-deviation computation and Spearman rank correlation between the two proxies across constraints.
- **Expected outcome:** standard deviation of the no-injection compliance rate exceeds 0.1, and its Spearman correlation with the base-versus-instruct delta exceeds 0.3.
- **Metrics:** standard deviation of each proxy; pairwise Spearman correlation between proxies.

## RQ6 — `rq_reactivity_equivalence`

- **Tier:** mechanism.
- **Target sub-problem:** `sp_reactivity_confound`.
- **Target hypothesis (verbatim, Stage 5/Stage 6):** "The 95% CI of the probing-regime × type interaction hazard ratio lies entirely within [0.80, 1.25] (equivalence bound), indicating probe reactivity — whatever its magnitude — does not differentially bias the soft/hard comparison the main design relies on."
- **Setup:** a calibration subsample (4 pilot-flagged cells × 2 constraint pairs × 6 probe turns × 10 seeds, ≈480 between-conversation runs) is probed exactly once per conversation at a randomly assigned turn and contrasted against matched within-conversation curves.
- **Sample-size rationale:** the ≈480-run calibration subsample size follows the feasibility budget for this arm (digest N6); it is deliberately smaller than the main factorial because each between-conversation run consumes one full conversation per single probe point, making it the most expensive design per data point in the study.
- **Statistical test:** two-one-sided-tests (TOST) equivalence procedure on the probing-regime × type interaction hazard ratio, with equivalence bounds [0.80, 1.25] and α=0.05.
- **Expected outcome:** the 95% CI of the probing-regime × type interaction hazard ratio lies entirely within [0.80, 1.25].
- **Metrics:** probing-regime × type interaction hazard ratio with 95% CI; TOST equivalence decision.
- **Note:** this RQ must be evaluated first — see "Execution order" above — since RQ2, RQ3, and RQ4 all rely on the within-conversation hazard estimates whose validity this RQ tests.

---

## Provenance note

Every setup/sample-size/statistical-test/metric above reuses `paper.md`'s already-designed E1 (RQ2/RQ3), E2 (RQ4), E3 (RQ6), and Step-9 walking-skeleton numbers (RQ1's 5-pair/75-conversation slice), plus Stage 6's confirmed datasets, baselines, and execution-order note from `pipeline.md` (full round-by-round derivation in `discussion_trace.md`). No new numbers, thresholds, or designs were introduced in assembling this document; B-alt is the one baseline present in `paper.md` Step 6 but not restated in Stage 6's own draft, included here for protocol completeness with that provenance flagged explicitly.
