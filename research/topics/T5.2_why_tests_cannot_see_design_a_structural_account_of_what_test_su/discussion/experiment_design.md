# Experiment Design — T5.2 (standalone protocol)

> Rendered as a runnable protocol, per the `auto-research-discussion` skill's "Final deliverables" spec. Sourced entirely from Stage 6's confirmed output in `pipeline.md` ("## Stage 6 — Experiment Design") plus `paper.md`'s own Step 5/6 pre-registration (Notation, Assumptions A1–A6, design constants, E1–E3 verification methods) and `paper_draft.md`'s Experiments section, which already rendered this same Stage 6 output in prose. Nothing below is invented beyond those three sources; where two sources state a number differently, both numbers are given and the discrepancy is flagged rather than silently resolved.
>
> `study_type = empirical`. Tier accounting (from Stage 6): **9 mechanism-tier RQs**, one per Stage 5 hypothesis, verbatim. **0 framing-tier RQs** (no Stage 3 limitation was flagged `verify_as_hypothesis`). **0 outcome-tier RQs** (an empirical study forbids "our procedure beats baseline X" framing; B0/B-alt/augmentation below are confound-isolation and sanity-check comparators only).

## Datasets and Baselines

**Datasets** (confirmed Stage 6, post-refiner):
1. **Defects4J-derived Java subject projects** shipping Checkstyle + ArchUnit configurations. *Justification:* mature JUnit suites plus machine-readable naming/layering rules already in the project give ground truth without inventing a rule set from scratch; this is the primary pilot + scale-up corpus.
2. **A Python subset** with mature pytest suites and flake8/import-linter configurations. *Justification:* the cross-ecosystem arm required by `rq_category_structure`/`rq_split_half_reliability`'s generalization claim (Stage 4's `sp_generalization_scope`) — without a second ecosystem, "the finding generalizes beyond one language's tooling idioms" cannot be tested at all.
3. **A held-out set of ~3 additional systems** (mixed Java/Python, drawn *after* the primary corpus is fixed). *Justification (added in the Stage 6 refiner pass, replacing a rejected "general benchmark... more systems is better" filler entry):* reserved specifically as the pre-registered replication set for `rq_split_half_reliability`'s split-half check, so the reliability claim is tested on data not used to tune the operator catalog or checker thresholds, rather than only re-splitting the same fixed corpus post hoc.

Design constants that apply across all datasets/RQs (`paper.md` Step 6 preamble, pre-registered): pilot **n = 2 systems**; scale-up **n = 12 systems × 3 categories**; **≥ 150 admitted mutants/category/system** (Assumption A2); differential-corpus budget **N_diff ≥ 10,000** generated inputs per subject system (generator disjoint from `T`); **α = 0.05** with Holm correction within each hypothesis family; primary inference engine: mixed-effects logistic model `kill ~ mutant_type + category + (1|system)`. **Power statement** (`paper.md`): at the 150-admitted-mutant floor, a per-system two-proportion test has power ≥ 0.90 at α = 0.05 to detect the pre-registered effect floor `DMSR_c − FSR ≥ 0.25`. **Thin-cell rule**: any (category × system) cell ending below 150 admitted mutants is pre-declared **INCONCLUSIVE** for that cell — never scored as a null, never silently dropped — and excluded from any "≥ 9 of 12 systems" vote.

**Baselines** (confound-isolation and sanity-check comparators — never outcome-tier competitors to beat, consistent with `study_type = empirical`):
- **B0 — default functional mutation arm** (PIT/pitest, mutmut) on the identical unmodified suite. *Justification:* the necessary reference defining `FMS`/`FSR` for every `DMSR`-vs-`FSR` contrast; gates admission of every system via Assumption A1 (`FMS ≥ 0.40`).
- **B-alt — matched convention-neutral equivalent-mutant control** `N_c` (same operator family, same locality footprint, `EQ_B = 1`, `V = 0`). *Justification:* isolates whether kill probability responds to violation status specifically (design-specific) rather than to equivalence/undecidability per se (the generic equivalent-mutant effect) — the comparator `rq_design_specificity` is built on.
- **Augmentation arm** — a discrimination-optimized generated test set (UTRL-style, or a capability-matched substitute per Assumption A6's validity gate: must raise `FMS` by ≥ 10 points). *Justification:* the stronger-suite comparator for `rq_structural_vs_quantity` — distinguishing a structural (test-proof) blind spot from a quantity-limited one.

---

## RQ1 — `rq_equivalence_oracle_validity`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_oracle_independence`. **Target method:** `m_dual_oracle_admission`.
- **Target hypothesis (verbatim, Stage 5):** "Restricting to mutants surviving the audited equivalence-budget check yields an equivalence-oracle mislabel rate below 5% against a stratified human audit (n≥300), i.e. DMSR is not primarily an artifact of equivalence-oracle noise."
- **Setup:** Draw a stratified random sample of ≥ 300 admitted mutants across categories and systems; human auditors independently assess whether each is genuinely behavior-preserving; compare against the bounded differential-execution oracle's (`EQ_B`) certification (`paper_draft.md` RQ1 Setup; `paper.md` Step 5 "functionally equivalent" row).
- **Sample-size rationale:** n ≥ 300 stratified human audit sample, as stated verbatim in the Stage 5 hypothesis and reused unchanged in `paper_draft.md`'s RQ1. **Flag:** `paper.md`'s own Assumption A3 describes a narrower detection procedure — "manual audit of 100 randomly sampled *surviving* mutants" — for the same equivalence-oracle check. The Stage 5/6 hypothesis and `paper_draft.md` agree with each other on n ≥ 300 (the number carried forward here), but this leaves a residual n=100-vs-n≥300 mismatch against `paper.md`'s A3 text that the two source documents do not themselves reconcile.
- **Statistical test:** Proportion (mislabel-rate) estimate on the audit sample, evaluated against the pre-registered 5% threshold; per A3's gate, a mislabel rate ≥ 5% on any subject system triggers re-filtering to structurally-guaranteed operator subfamilies (pure renames, verified-commutative swaps, call-multiset-preserving relocations) and recomputation of DMSR for that system.
- **Expected outcome:** Equivalence-oracle mislabel rate against the human audit is below 5%.
- **Metrics:** Equivalence-oracle mislabel rate, overall and per category.

## RQ2 — `rq_violation_checker_precision`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_oracle_independence`. **Target method:** `m_dual_oracle_admission`.
- **Target hypothesis (verbatim, Stage 5):** "The violation checker achieves precision ≥0.90 against the same human audit per category, i.e. V(m)=1 meaningfully approximates human-judged convention violation rather than checker noise."
- **Setup:** Using the same stratified human-audit sample as RQ1, compare the machine-readable rule checker's (`V(m)`) violation verdict against human auditors' judgment, per category (`paper_draft.md` RQ2 Setup; `paper.md` Assumption A4's 5-step sequence: rules grounded in the project's own shipped config → thresholds drafted wide and refined on a held-out calibration subsample → validated against two independent human raters → confusion-structure inspection → checker frozen before scale-up).
- **Sample-size rationale:** n ≥ 300 stratified human audit across categories, two independent raters — matches `paper.md` A4 exactly (no cross-document discrepancy here, unlike RQ1).
- **Statistical test:** Precision estimate per category against the pre-registered 0.90 threshold; inter-rater reliability via Cohen's κ (must be ≥ 0.7, A4); confusion-structure inspection (disagreements must be adjacent-rule confusions, not a systematic collapse onto one category). Any category failing precision, κ, or the confusion-structure check is demoted to exploratory (A4 gate).
- **Expected outcome:** Checker precision is at least 0.90 in each category.
- **Metrics:** Violation-checker precision per category; inter-rater κ; confusion-matrix structure.

## RQ3 — `rq_nonlocal_yield`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_nonlocal_construction`. **Target method:** `m_nonlocal_operator_catalog`.
- **Target hypothesis (verbatim, Stage 5):** "The layering/cross-cutting operator family yields at least 50 dual-oracle-admitted mutants per subject system after filtering — the non-local category is constructible at usable yield, not merely a theoretical category."
- **Setup:** Apply the layering/cross-cutting operator family (relocates a call across a declared module boundary while preserving the call multiset) to each subject system and record the number of candidates that pass dual-oracle admission (`EQ_B=1, V=1`).
- **Sample-size rationale:** Threshold of ≥ 50 admitted mutants per subject system, evaluated across the 12-system scale-up corpus. This is a lower, feasibility-tier bar distinct from the ≥ 150/category/system power threshold (A2) used for the main statistical analyses (RQ5, RQ8) — an early constructibility checkpoint, not a conflicting number.
- **Statistical test:** Yield count (admitted/candidates) compared against the 50-mutant floor per system; a feasibility/threshold check, not an inferential test — consistent with A2's own "walking-skeleton yield metric... operators revised before scale-up if yield < 50% of candidates" treatment. Falsification is evaluated as yield falling below 50 in a majority of systems (`paper_draft.md` RQ3 Falsification condition).
- **Expected outcome:** At least 50 admitted mutants per subject system for this category.
- **Metrics:** Admitted-mutant count per system for the layering/cross-cutting category; admission yield rate (admitted/candidates).

## RQ4 — `rq_temporal_kill_extension`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_temporal_kill_semantics`. **Target method:** `m_extended_temporal_kill`.
- **Target hypothesis (verbatim, Stage 5):** "At least 50% of admitted temporal/ordering mutants have confirmed-identical final output (via the differential corpus) yet are flagged as convention-violating by the trace-order checker — a majority, not merely an existence instance, since kill-vs-violate independence for this category is exactly what is being measured, and a weaker existence claim would be true almost by construction."
- **Setup:** Among admitted temporal/ordering mutants, identify those with confirmed-identical final output under the differential corpus (`EQ_B=1`), and check how many are nonetheless flagged as convention-violating by the independent trace-order checker (`M4`'s extended kill criterion).
- **Sample-size rationale:** Computed as a within-`D_c` proportion over whichever temporal/ordering mutants are admitted under RQ5's ≥ 150/category/system target at scale-up (12 systems); no separate audit sample is needed since the check operates entirely on already-admitted mutants.
- **Statistical test:** One-sided proportion test against a 50% threshold. Note (round-1 critique, Stage 5): a bare existence claim ("at least one") was explicitly rejected as near-tautological and replaced with this rate-based version, since with any nontrivial admitted count a single instance is close to guaranteed.
- **Expected outcome:** At least 50% of admitted temporal/ordering mutants have confirmed-identical final output yet are flagged as violating by the trace-order checker.
- **Metrics:** Proportion of admitted temporal/ordering mutants with confirmed-identical final output that are flagged as violating.

## RQ5 — `rq_codifiable_scope_yield`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_groundtruth_scoping`. **Target method:** `m_scoped_codifiable_conventions`.
- **Target hypothesis (verbatim, Stage 5):** "Restricting to codifiable conventions still admits at least 150 mutants per category per system in at least 9 of 12 tested systems, i.e. the restriction is not so narrow that it starves the measurement of admitted cases."
- **Setup:** Across all three categories, count admitted mutants per category per system after the codifiable-convention scoping restriction (Checkstyle/ArchUnit/trace-rule representable conventions only) is applied.
- **Sample-size rationale:** ≥ 150 admitted mutants/category/system (Assumption A2's pre-registered floor), evaluated as a "≥ 9 of 12 systems" vote across the full 12-system scale-up corpus — the same vote structure and thin-cell/INCONCLUSIVE rule `paper.md`'s power statement applies to H1.
- **Statistical test:** Count/threshold check per (category × system) cell against the 150-mutant floor; a feasibility/vote check rather than a significance test. Cells below 150 are marked INCONCLUSIVE and excluded from the "≥ 9 of 12" vote rather than scored as failures.
- **Expected outcome:** At least 150 admitted mutants per category per system in at least 9 of 12 tested systems.
- **Metrics:** Admitted-mutant count per category per system; count of systems meeting vs. missing the 150-mutant floor.

## RQ6 — `rq_design_specificity`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_design_specificity`. **Target method:** `m_design_specificity_control`.
- **Target hypothesis (verbatim, Stage 5):** "The absolute difference in kill probability between the design-mutant set and its matched, convention-neutral control is below 0.05 per category."
- **Setup:** For each category, compare kill probability between the admitted design-mutant set `D_c` and its matched, convention-neutral control `N_c` (same operator family, same locality footprint, `V=0`), holding equivalence fixed. This is the same construct as `paper.md`'s B-alt pre-registered check: `|P(K_T=1|m∈D_c) − P(K_T=1|m∈N_c)| < 0.05` per category.
- **Sample-size rationale:** Same admitted-mutant sample as RQ5/E1/E2 (≥ 150/category/system across 12 systems), since `N_c` is matched pairwise to `D_c` by operator family and locality.
- **Statistical test:** Two-proportion (kill-probability) difference test between `D_c` and `N_c` per category, with bootstrap confidence intervals (10,000 resamples, system-level blocks, per `paper.md`'s E2 analogous verification method).
- **Expected outcome:** The absolute difference in kill probability between the two matched groups is below 0.05 per category. **Note on polarity** (flagged during `stage_review.md`'s review and folded into `paper_draft.md`): a *small* gap here is the outcome supporting a genuine, design-specific blind spot; a *large* gap would instead show the suite partially senses convention-violation via incidental structural coupling (quantified via `IKF_c`) — the reverse of "bigger gap, stronger finding."
- **Metrics:** Kill-probability difference between `D_c` and `N_c` per category, with confidence intervals; `IKF_c` decomposition if a gap is found.

## RQ7 — `rq_structural_vs_quantity`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_structural_vs_quantity`. **Target method:** `m_augmentation_arm`.
- **Target hypothesis (verbatim, Stage 5):** "For the non-local categories (layering/cross-cutting, temporal/ordering), the absolute DMSR reduction after a capability-matched augmentation (raising the functional mutation score by at least 10 points) is below 0.10, with no significant per-mutant kill change, across a majority of tested systems."
- **Setup:** For the non-local categories (LAY, TMP), augment each subject suite with a capability-matched, discrimination-optimized generated test set (validity gated by Assumption A6: must raise `FMS` by ≥ 10 points), and re-measure per-category DMSR before and after.
- **Sample-size rationale:** ≥ 4 subject systems (the explicit system-count threshold from `paper.md`'s H3), drawn from the 12-system scale-up corpus; augmentation validity gated by A6 before the comparison is treated as informative.
- **Statistical test:** Paired McNemar test per category per system on per-mutant kill verdicts before/after augmentation (`paper.md` E3 verification), Holm-corrected across categories; `ΔDMSR_c = DMSR_c(T) − DMSR_c(T∪T_gen)` computed alongside, conditional on the ΔFMS ≥ +0.10 arm-validity gate passing first.
- **Expected outcome:** The absolute survival-rate reduction after augmentation is below 0.10, with no statistically significant per-mutant kill change, across a majority of tested systems.
- **Metrics:** `ΔDMSR_c` per category/system; McNemar discordant-pair count/p-value; `ΔFMS` (augmentation-strength check).

## RQ8 — `rq_category_structure`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_generalization_scope`. **Target method:** `m_multi_system_category_design`.
- **Target hypothesis (verbatim, Stage 5):** "The category fixed effect in the mixed-effects model is significant at α=0.05, pooled across all tested systems."
- **Setup:** Fit the pre-registered mixed-effects logistic model `kill ~ mutant_type + category + (1|system)` across all 12 scale-up systems (Java + Python) and test the category term.
- **Sample-size rationale:** Full 12-system × 3-category scale-up corpus, ≥ 150 admitted mutants/category/system (A2). `paper.md`'s power statement ties this same 150-mutant floor to ≥ 0.90 power at α = 0.05 for the per-system contrast underlying H1, which draws on the identical admitted-mutant pool this category-effect test is estimated from.
- **Statistical test:** Likelihood-ratio test on the category fixed effect, α = 0.05 (`paper.md` E2 verification); pairwise per-category effect-size estimates with bootstrap confidence intervals (10,000 resamples, system-level blocks).
- **Expected outcome:** The category effect is statistically significant, pooled across all tested systems.
- **Metrics:** LRT statistic and p-value for the category fixed effect; per-category effect-size estimates with confidence intervals.

## RQ9 — `rq_split_half_reliability`

- **Tier:** mechanism-tier.
- **Target sub-problem:** `sp_generalization_scope`. **Target method:** `m_multi_system_category_design`.
- **Target hypothesis (verbatim, Stage 5):** "Per-category classifications computed from two disjoint random half-samples of systems agree in a majority of category comparisons."
- **Setup:** Split the tested systems into two disjoint random halves, recompute the per-category classification independently on each half using the identical fitted model structure, and compare agreement — including the held-out replication systems reserved specifically for this check.
- **Sample-size rationale:** Two disjoint random halves of the 12-system corpus (6 systems each), supplemented by the ~3-system held-out replication set added in the Stage 6 refiner pass specifically so this check is not run only by re-splitting the same fixed corpus post hoc.
- **Statistical test:** Split-half resampling — refit the same mixed-effects model on each disjoint half, compute per-category classification agreement rate across the two halves. A reliability/robustness check, not a null-hypothesis significance test; per `paper.md`'s framing, falsification is agreement falling at or below chance.
- **Expected outcome:** Per-category classifications computed from two disjoint random half-samples of systems agree in a majority of category comparisons.
- **Metrics:** Split-half classification agreement rate across category comparisons.

---

## Cross-references

- Datasets/baselines/RQ table origin: `pipeline.md` § "Stage 6 — Experiment Design" (draft_v1 + refiner pass).
- Target hypotheses origin (verbatim): `pipeline.md` § "Stage 5 — Method Design", "Confirmed Stage 5" (9 hypotheses across 7 methods).
- Design constants, power statement, thin-cell rule, Assumptions A1–A6, B0/B-alt/augmentation-arm definitions, E1–E3 verification methods: `paper.md` §§ "Step 5 — Formal Problem Definition", "Assumptions (A1..A6)", "Step 6 — Pre-Registered Experiments".
- Prose rendering of this same protocol (with placeholders for results): `paper_draft.md` § "Experiments".
