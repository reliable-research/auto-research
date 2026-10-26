# Experiment Design — B3.4: How Many Prompts Break per Upgrade?

> Standalone experiment-design spec, per `auto-research-discussion`'s "Final deliverables" #2. Assembled from Stage 6's confirmed output in `pipeline.md` ("## Stage 6 — Experiment Design") and `paper.md`'s Step 6 / `paper_draft.md`'s Experiments section. Nothing below is invented beyond what those two sources already specify — this document exists to be executable as a protocol without opening the paper. Status: **specification — no experiments have been run.** Keep synchronized with `paper_draft.md`'s Experiments section if either is edited later.

**Study type:** empirical (measurement/audit study — not a proposed method competing against baselines).

**Tier accounting (from Stage 6):** 7 mechanism-tier RQs (one per Stage 5 hypothesis, verbatim), 0 framing-tier RQs (no Stage 3 limitation was flagged `verify_as_hypothesis`), 0 outcome-tier RQs (`study_type = empirical` forbids "our procedure beats baseline X" framing; the cheap-signal comparison is a mechanism-tier identifiability check on the measurement itself, not an outcome claim).

---

## Datasets

- **SchemaStore** (schemastore.org) — real-world JSON schemas, sampled and stratified by nesting depth and constraint count. *Justification:* sources the schema-contract genre with a naturally occurring feature distribution.
- **JSONSchemaBench** — approximately 10,000 real-world JSON schemas. *Justification:* scales the schema-contract genre beyond SchemaStore's coverage, needed for RQ4's (fragility-predictor) statistical-power requirement.
- **IFEval** — programmatically verifiable instruction constraints. *Justification:* sources the format-convention contract genre with an established, machine-checkable rule set.
- **FollowBench** — multi-constraint instructions stratified by constraint count. *Justification:* sources contracts at the high end of the constraint-density range so that feature has enough variance in the library for its odds ratio to be estimable in RQ4 — SchemaStore/JSONSchemaBench schemas alone skew toward moderate constraint counts. (This justification was itself a Stage-6 critic finding: the original draft justified FollowBench only as "the benchmark RECAST builds on," which the critic flagged as not tied to any RQ; the refiner replaced it with the RQ4-linked reason above.)
- **WildChat-1M** — real user–LLM conversations, mined for production-style few-shot/structured-output templates. *Justification:* sources the few-shot-template contract genre from genuinely in-the-wild usage rather than authored examples.
- **Berkeley Function Calling Leaderboard (BFCL) v3** — function-calling structured-action contracts. *Justification:* extends contract coverage to the function-calling genre.
- **Model version chains:** dated OpenAI gpt-4o snapshots (secondary, closed-API arm); Llama 2 → 3 → 3.1 → 3.3; Qwen2 → Qwen2.5 → Qwen3 (primary, open-weight anchor lineages). *Justification:* open-weight lineages are permanently re-queryable and individually addressable by construction, so primary claims are anchored there; closed-API dated snapshots are addressability-bounded (can change silently or be deprecated) and are reported only as a secondary arm.

## Baselines

Sanity-check comparators, not outcome-tier competitors — no RQ here is framed as "our procedure beats baseline X."

- **Within-version split-half noise floor (B_null / B0)** — the necessary null every breakage claim in RQ3 is tested against. Computed by splitting each contract's 20 samples at a given version into two disjoint 10-sample halves and running the identical breakage computation between the halves as if they were two versions.
- **First-token top-k logprob detector (LogProbTracking-style)** — the cheap-signal comparator for RQ5; if it predicts breakage as well as the structural fragility model, the constructed contract library adds nothing beyond what cheap monitoring already gives.
- **Grammar-constrained decoding arm** (conceptual lineage: DiffusionCFG's decoding-time-guarantee concept, implemented via an autoregressive-compatible tool such as xgrammar/outlines on the open-weight chains, not DiffusionCFG's own implementation, since the anchor lineages here are autoregressive, not diffusion models) — the schema-tier mitigation upper bound for RQ6.
- **DSPy-style per-version prompt recompilation** — the mitigation baseline for RQ7.

---

## RQ1 — Validator ground truth

- **Tier:** mechanism
- **Target sub-problem:** `sp_ground_truth_definition`
- **Target hypothesis (verbatim, Stage 5 `m_validator_construction` / Stage 6 `rq_validator_agreement`):** "Validator-vs-hand-label agreement on a held-out calibration set of positive/negative example outputs is ≥0.95, across all three tiers."
- **Setup:** Before any measurement run, a held-out calibration set of hand-constructed positive and negative example outputs is scored by all three validator tiers (parse, schema, convention) and compared against the hand labels.
- **Sample-size rationale:** Not separately specified in the source material beyond the calibration-set construction described above.
- **Statistical test:** Threshold comparison against a pre-registered ≥0.95 agreement bar (no significance test specified — this is a calibration gate, not a hypothesis test).
- **Expected outcome:** Validator-vs-hand-label agreement is at least 0.95, across all three tiers.
- **Falsification condition:** Refuted if agreement on the calibration set falls below 0.95 on any tier — meaning the acceptance predicate does not track real downstream-parser behavior closely enough for downstream breakage numbers to be trusted, and the strict/lenient boundary needs recalibration before any other RQ's results are meaningful.
- **Metrics:** Per-tier and overall validator-vs-hand-label agreement rate.

## RQ2 — Version addressability

- **Tier:** mechanism
- **Target sub-problem:** `sp_version_attribution`
- **Target hypothesis (verbatim, Stage 5 `m_version_paired_harness` / Stage 6 `rq_addressability_canary`):** "Across the collection window, open-weight anchor lineages trigger zero canary-flagged re-collection events, while at least one closed-API dated-snapshot chain triggers at least one — i.e., the addressability risk this design anchors around on open-weight chains is not a hypothetical one."
- **Setup:** Across the full collection window, the first-token logprob canary probe is run beside every collection batch on both the open-weight anchor lineages and the closed-API dated-snapshot chains; the count of canary-flagged re-collection events is tallied per lineage type.
- **Sample-size rationale:** Not separately specified in the source material — the canary runs continuously alongside every collection batch across the full collection window, rather than on a separately sized sample.
- **Statistical test:** Threshold/count comparison (zero events on open-weight vs. at least one on closed-API) — no significance test specified.
- **Expected outcome:** Open-weight anchor lineages trigger zero canary-flagged re-collection events across the collection window, while at least one closed-API dated-snapshot chain triggers at least one.
- **Falsification condition:** Refuted if canary-flagged events occur equally often (or more often) on open-weight lineages than on closed-API chains — meaning the addressability risk this design anchors its primary claims around on open-weight lineages is not actually differentiating, and treating closed-API results as a secondary, addressability-bounded arm needs re-justifying.
- **Metrics:** Canary-flagged re-collection event count, per lineage type.

## RQ3 — Breakage exceeds noise floor

- **Tier:** mechanism
- **Target sub-problem:** `sp_noise_confound`
- **Target hypothesis (verbatim, Stage 5 `m_noise_floor_estimator` / Stage 6 `rq_breakage_exceeds_noise`):** "On the open-weight anchor lineages, for at least half of tested version transitions, B(v→v′) exceeds B_null by a BH-corrected paired-permutation test (α=0.05), the pooled point estimate ΔB is at least 3 percentage points, and strict-envelope contract types (schema, convention) show larger ΔB than few-shot template contracts."
- **Setup:** Pilot stage: 300 contracts (100 schema, 100 format-convention, 100 few-shot-template), one open-weight lineage with at least three pinned successive versions, n = 20 samples per (contract, version), temperature-0 primary arm. Scale-up: approximately 3,000 contracts across at least ten version transitions and three model families.
- **Sample-size rationale:** The pilot's 300 paired pass/fail observations per transition give a two-sided exact paired test over 0.9 power to separate B = 5% from B_null = 1% at α = 0.05; the scale-up's approximately 3,000 contracts across ten-plus transitions is sized for RQ4's fragility-model power requirement, not solely for RQ3.
- **Statistical test:** Two-sided paired-permutation test of B(v→v′) against B_null over contracts, per transition; Benjamini–Hochberg corrected across all (transition × contract-type) cells; α = 0.05.
- **Expected outcome:** For at least half of tested version transitions, B(v→v′) significantly exceeds B_null; the pooled point estimate ΔB is at least 3 percentage points; strict-envelope contract types (schema, convention) show larger ΔB than few-shot-template contracts, whose demonstrations redundantly anchor the output format.
- **Falsification condition:** Refuted if, across all tested transitions and contract types, B(v→v′) is statistically indistinguishable from B_null after correction — the central claim that upgrades measurably break contracts beyond noise would be false, and the paper's finding would instead be a noise-adjusted upper bound on breakage rather than a demonstrated effect.
- **Metrics:** B(v→v′), B_null, ΔB and its paired-test p-value, per contract type.

## RQ4 — Fragility predictors

- **Tier:** mechanism
- **Target sub-problem:** `sp_power_collinearity`
- **Target hypothesis (verbatim, Stage 5 `m_fragility_predictor_model` / Stage 6 `rq_fragility_predictors`):** "In the mixed-effects model, at least one of {schema nesting depth, constraint density} has an odds ratio ≥1.3 with 95% CI excluding 1 after BH correction; few-shot example count has an odds ratio <1; and leave-one-family-out predictive ROC-AUC is ≥0.65."
- **Setup:** Mixed-effects logistic regression of the per-contract breakage event on the pre-registered seven-feature vector (schema nesting depth, field count, required-field ratio, constraint count, few-shot example count, instruction token length, delimiter/casing rule count) plus contract type, with random intercepts for version transition and model family, fit over all scale-up breakage events. The contract library's stratified sampling design deliberately decorrelates depth from constraint count.
- **Sample-size rationale:** Approximately 3,000 contracts across at least ten version transitions gives at least 0.8 power to detect a per-feature odds ratio of 1.3, per the pre-registered analysis plan.
- **Statistical test:** Wald tests on each feature, Benjamini–Hochberg corrected; predictive AUC assessed under grouped 5-fold cross-validation (grouped by contract family so near-duplicates never straddle folds) and under a leave-one-model-family-out split.
- **Expected outcome:** At least one of {schema nesting depth, constraint density} has an odds ratio at least 1.3 with a 95% CI excluding 1 after correction; few-shot example count has an odds ratio below 1; leave-one-family-out predictive AUC is at least 0.65.
- **Falsification condition:** Refuted if no pre-registered feature attains a significant odds ratio after correction, or if grouped-CV or leave-one-family-out AUC is indistinguishable from 0.5 — meaning fragility is unpredictable from the proposed structural features, which would itself be an actionable negative result (regression testing cannot be prioritized by contract structure and must be treated as exhaustive).
- **Metrics:** Per-feature odds ratios with 95% CIs; grouped 5-fold and leave-one-family-out predictive AUC.

## RQ5 — Cheap-signal specificity

- **Tier:** mechanism
- **Target sub-problem:** `sp_causal_specificity`
- **Target hypothesis (verbatim, Stage 5 `m_cheap_signal_decorrelation` / Stage 6 `rq_cheap_signal_specificity`):** "The structural fragility model's breakage-prediction AUC exceeds the first-token logprob detector's AUC by a pre-registered margin of at least 0.10."
- **Setup:** The first-token logprob two-sample detector is run on the same (contract, version) pairs used to fit the RQ4 fragility model; its own breakage-prediction AUC is computed on the same held-out split and compared directly against the structural model's AUC.
- **Sample-size rationale:** Not separately specified — this RQ reuses the same (contract, version) pairs and held-out split assembled for RQ4.
- **Statistical test:** Direct AUC comparison against a pre-registered margin threshold (≥0.10 gap); no additional significance test specified.
- **Expected outcome:** The structural fragility model's breakage-prediction AUC exceeds the cheap logprob detector's AUC by a pre-registered margin of at least 0.10.
- **Falsification condition:** Refuted if the AUC gap is below 0.10, or negative — meaning breakage carries no detectable structure beyond what a near-free, contract-agnostic distribution-shift signal already predicts, which would undercut the practical case for building and maintaining the expensive contract library at all.
- **Metrics:** AUC gap between the structural model and the cheap detector, on identical held-out data.

## RQ6 — Mitigation: grammar-constrained decoding (schema tier)

- **Tier:** mechanism
- **Target sub-problem:** `sp_avoidable_vs_inherent`
- **Target hypothesis (verbatim, Stage 5 `m_mitigation_headroom_bound`, arm a / Stage 6 `rq_mitigation_schema_tier`):** "Grammar-constrained decoding removes at least 90% of schema-tier breakage."
- **Setup:** On the open-weight anchor lineages, the schema-contract subset is re-run under a grammar-constrained decoding arm and compared, tier by tier, against the unmitigated arm on identical contracts.
- **Sample-size rationale:** Not separately specified — reuses the schema-contract subset of the RQ3 scale-up library, paired against the unmitigated arm on identical contracts.
- **Statistical test:** Paired permutation test, tier by tier, against the unmitigated arm.
- **Expected outcome:** Grammar-constrained decoding removes at least 90% of schema-tier breakage, reflecting that it guarantees schema conformance essentially by construction, while convention-tier breakage on the same contracts remains largely untouched.
- **Falsification condition:** Refuted if the schema-tier breakage reduction is below 90%, or non-significant — meaning schema-tier breakage is not, in fact, dominated by failures a decoding-time guarantee can eliminate, undercutting the case for this mitigation as a near-complete fix for that tier.
- **Metrics:** Schema-tier B_mitigated versus B_unmitigated, paired over identical contracts.

## RQ7 — Mitigation: per-version prompt recompilation

- **Tier:** mechanism
- **Target sub-problem:** `sp_avoidable_vs_inherent`
- **Target hypothesis (verbatim, Stage 5 `m_mitigation_headroom_bound`, arm b / Stage 6 `rq_mitigation_recompilation`):** "Per-version prompt recompilation yields at least a 25% relative reduction in total B(v→v′), significant by a paired test on identical contracts (α=0.05)."
- **Setup:** On the open-weight anchor lineages, the full contract library is re-run with a per-version, declaratively recompiled prompt and compared against the unmitigated, frozen-prompt arm on identical contracts.
- **Sample-size rationale:** Not separately specified — reuses the full RQ3 scale-up library, paired against the unmitigated arm on identical contracts.
- **Statistical test:** Paired permutation test on total B(v→v′), α = 0.05.
- **Expected outcome:** Per-version prompt recompilation yields at least a 25% relative reduction in total B(v→v′), significant at α = 0.05.
- **Falsification condition:** Refuted if the relative reduction is below 25%, or non-significant — meaning re-optimizing the prompt per version does not meaningfully offset upgrade-induced breakage, and the residual breakage would need to be attributed to failure modes neither decoding-time guarantees nor prompt re-optimization reach.
- **Metrics:** Total B_mitigated versus B_unmitigated under recompilation, paired over identical contracts.

---

## Note on the two mitigation RQs sharing one sub-problem

RQ6 and RQ7 both target `sp_avoidable_vs_inherent` and both derive from the single Stage 5 method `m_mitigation_headroom_bound`, which was deliberately designed as **one method with two arms** rather than two competing methods (per the Stage 5 refiner pass in `pipeline.md`): grammar-constrained decoding and prompt recompilation are unrelated techniques, but they share the same evaluation instrument — a tier-decomposed, paired-against-unmitigated comparison protocol — answering the same underlying question (how much of the measured breakage is avoidable) rather than being independent, incomparable evaluations.

## Global fallback (from `paper.md` Step 6)

If the central hypothesis family fails (RQ3 null AND RQ4 null), the paper pivots archetype from measurement-of-a-fragility-phenomenon to robustness-audit/calibration null: "Contrary to the prevailing assumption that provider model upgrades silently break downstream structured-output contracts, we measure per-upgrade breakage across three model families and find it statistically indistinguishable from within-version sampling noise, establishing an empirical upper bound and reframing model-version regression testing as a low-priority engineering activity."
