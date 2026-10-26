# Experiment Design — B3.5: Do All Models Drift the Same Way?

> Standalone rendering of the confirmed **Stage 6 (Experiment Design)** output from `discussion_trace.md` (the `auto-research-discussion` run), cross-checked against `../paper.md`'s own Step 5 (Formal Problem Definition, Assumptions A1–A6) and Step 6 (Pre-Registered Experiments E1–E3, baseline arms B0/B-alt). Nothing here is invented beyond those two sources — where a field (e.g., a numeric sample size) is not specified in either source, that gap is stated explicitly rather than filled in. Status: **specification only — no experiments have been run; all numbers are pre-registered design targets.**
>
> **Tier accounting (study_type = empirical):** 8 mechanism-tier RQs (one per Stage 5 hypothesis, verbatim). 0 framing-tier RQs (no Stage 3 related-work limitation was flagged `verify_as_hypothesis`). 0 outcome-tier RQs (`study_type = empirical` forbids "beats baseline X" framing — the baselines below are sanity-check comparators, never competitors to beat).

---

## Datasets

| Dataset | Axis supplied | Justification |
|---|---|---|
| IFEval | capability-loaded: instruction/format compliance | Verifiable-constraint instruction/format-compliance prompts; supplies the capability-loaded axis needed by RQ2 and RQ3 (the K_cap vs. K_neu contrast and its residualized counterpart). |
| TruthfulQA + SimpleQA | capability-loaded: factuality | Held-fixed factual-QA slice; supplies the capability-loaded factuality axis for the same RQ2/RQ3 contrast. |
| Curated borderline-safety refusal set | capability-neutral: refusal | Supplies the capability-neutral refusal axis needed by RQ2 (raw K_cap-vs-K_neu contrast), RQ4 (alignment-scheme robustness), and RQ5 (axis robustness). |
| Anthropic sycophancy-eval-style opinion-flip probes | capability-neutral: sycophancy | Supplies the capability-neutral sycophancy axis for the same RQ2/RQ4/RQ5 set. |
| GlobalOpinionQA-style stance battery | capability-neutral: political/moral stance | Supplies the capability-neutral political/moral-stance axis for the same RQ2/RQ4/RQ5 set. |
| NoveltyBench / INFINITY-CHAT-style open-ended prompts | diversity computation (RQ6, RQ7) | The Vendi Score computation in RQ6 and RQ7 needs open-ended generations with a large possible-response space to make a diversity statistic meaningful; the closed-form, single-correct-answer axis prompts used for drift-vector correlation (IFEval, TruthfulQA/SimpleQA) would produce a degenerate, near-constant diversity index regardless of the true population spread, so a separate open-ended prompt set is required specifically for the two diversity RQs, not the six correlation RQs. (Refined during Stage 6's critic round — the original draft's justification, "digest mentions it for the diversity axis," was rejected as a provenance note rather than a methodological reason; this is the corrected version.) |

Note: `paper.md`'s Step 5 notation also names a `reasoning` axis inside K_cap (scored via "fixed multi-step items"), and its Instrument Validation Plan (①) lists all six axis-to-instrument anchors including reasoning. Neither the confirmed Stage 6 output in `discussion_trace.md` nor `paper_draft.md`'s Experimental Setup lists a named public dataset for the reasoning axis specifically — this gap is carried over from those sources as-is, not filled in here.

## Baselines

All three are **sanity-check comparators, not outcome-tier competitors** — this is a measurement study, and no RQ is framed as "our procedure beats baseline X."

| Baseline | Role | Justification |
|---|---|---|
| Permutation / shuffled-vendor-pairing exchangeability null | Necessary control for every correlation claim (RQ2 through RQ5) | Defines the null distribution a correlation must exceed to be called "significant" rather than an artifact of chance vendor pairing. |
| Single-vendor drift-only analysis (`B0-NoDrift` in `paper.md`) | Degenerate no-cross-vendor baseline; also the noise-floor instrument for RQ8 | Confirms the correlation machinery reduces to nothing informative when there is nothing to correlate against; re-probing each pinned snapshot twice (split-half + two-week test–retest) against itself is also how the noise floor ν that gates RQ8 is empirically measured. |
| CAPA / Artificial-Hivemind-style contemporaneous cross-model similarity check | Cross-check that same-time similarity is not silently substituted for drift-*direction* similarity | Borrowed as an instrument, not as a number to beat (Stage 3's refiner sharpened both `rw_capa` and `rw_hivemind`'s baseline role to this same-time comparator-arm framing, since their own I/O framing is single-snapshot and not directly comparable to this paper's longitudinal drift-correlation numbers). |

---

## Research Questions

All 8 RQs are **mechanism-tier**, each traced to exactly one Stage 5 method/hypothesis and one Stage 4 sub-problem (`target_sub_problem_id`).

### RQ1 — Do the automated axis scorers agree with human judgment?

- **Tier:** mechanism
- **Target sub-problem:** `sp_battery_construct_validity`
- **Target hypothesis (verbatim, Stage 5 `m_probe_battery`):** "Each automated axis scorer achieves inter-rater agreement κ ≥ 0.70 against human labels on a held-out validation subset of at least 500 items per axis; any axis that fails this bar is re-instrumented or dropped before the main analysis."
- **Setup:** For each of the six behavioral axes, score a held-out validation subset of at least 500 items with both the automated scorer and independent human annotators; compute Cohen's/Fleiss' κ per axis. This sits inside `paper.md`'s broader 5-step instrument-validation plan for the battery (M1): ground each axis in a pre-existing cited instrument, pilot on a calibration slice disjoint from the evaluation slice, validate against ≥2 independent human raters (this RQ), inspect confusion structure for any axis scoring κ < 0.9, and freeze the scorer/prompts/thresholds before Stage-2 data collection.
- **Sample-size rationale:** ~500 items per axis, chosen per `paper.md`'s feasibility accounting (digest N6) as the item count that keeps human annotation within a stated ~40–80 annotator-hour budget while still being large enough to estimate κ per axis reliably.
- **Statistical test:** Cohen's/Fleiss' κ inter-rater agreement coefficient against a fixed pre-registered threshold (κ ≥ 0.70); axes scoring κ < 0.9 additionally undergo confusion-structure inspection (a systematic one-directional disagreement pattern triggers re-instrumentation rather than a lowered threshold).
- **Expected outcome:** Every axis achieves κ ≥ 0.70 against human labels on its validation subset.
- **Metrics:** Per-axis inter-rater agreement (κ).

### RQ2 — Is raw cross-vendor drift correlation higher on capability-loaded axes than capability-neutral axes?

- **Tier:** mechanism
- **Target sub-problem:** `sp_capability_confound`
- **Target hypothesis (verbatim, Stage 5 `m_capability_residualization`):** "If observed cross-vendor drift correlation is driven by shared capability improvement rather than genuine homogenization, correlation on K_cap axes will be significantly higher than on K_neu axes."
- **Setup:** Compute mean pairwise cross-vendor drift correlation separately on the capability-loaded axis subset (K_cap) and the capability-neutral axis subset (K_neu), on unresidualized drift vectors, across all tested vendor pairs and both time-alignment schemes. This is the same instrument as RQ3 (`paper.md`'s E1 / `B-alt-RisingTide`): partitioning by axis membership and residualizing out the empirical mean drift direction are, per the Stage 5 refiner, "the same operation... applied at two granularities — one instrument, two falsifiable predictions."
- **Sample-size rationale:** `paper.md`'s E1 design target: 6 vendors × 4–6 versions × ~400 prompts × 5 samples/prompt ≈ 60k calls (digest N6 feasibility budget). Vendor count (n ≤ 6) is explicitly too small to bootstrap over vendors — CIs are instead computed by bootstrapping over prompts.
- **Statistical test:** Permutation test (shuffle vendor pairings and axis labels, ≥10,000 draws); Mantel test on the full pairwise correlation matrix; bootstrap-over-prompts confidence intervals; Benjamini–Hochberg correction across pairs and axes at q = 0.05.
- **Expected outcome:** Correlation on K_cap is significantly higher than on K_neu — the signature a purely capability-driven, no-shared-pipeline explanation predicts.
- **Metrics:** Mean pairwise Pearson/cosine drift correlation, K_cap vs. K_neu, with bootstrap CIs over prompts.

### RQ3 — Does residualizing out the shared capability-improvement direction attenuate cross-vendor drift correlation?

- **Tier:** mechanism
- **Target sub-problem:** `sp_capability_confound`
- **Target hypothesis (verbatim, Stage 5 `m_capability_residualization`):** "If observed correlation is driven by the shared capability-improvement direction, residualized drift correlation will be substantially attenuated relative to raw drift correlation; a homogenization claim requires it not be."
- **Setup:** Compute the empirical cross-vendor mean drift direction ḡ; project it out of each vendor's drift vector to obtain the residualized drift d̃; recompute mean pairwise cross-vendor correlation on d̃ and compare to the raw (unresidualized) correlation on the full vector. Same instrument as RQ2 — see that entry's note on the shared one-instrument-two-predictions structure.
- **Sample-size rationale:** Identical to RQ2 (same data collection pass: 6 vendors × 4–6 versions × ~400 prompts × 5 samples/prompt ≈ 60k calls).
- **Statistical test:** Same permutation/Mantel/bootstrap/BH machinery as RQ2, applied to raw vs. residualized correlation estimates and their ratio.
- **Expected outcome:** If raw correlation was driven by the shared capability direction, residualized correlation is substantially attenuated relative to raw correlation; a homogenization claim requires that it is not.
- **Metrics:** Raw vs. residualized correlation estimates and their ratio, with bootstrap CIs.

### RQ4 — Is the sign of cross-vendor drift correlation stable across two independent time-alignment conventions?

- **Tier:** mechanism
- **Target sub-problem:** `sp_time_alignment`
- **Target hypothesis (verbatim, Stage 5 `m_dual_alignment`):** "The sign of the mean pairwise cross-vendor drift correlation is identical under calendar-time and release-index alignment in the majority of tested vendor pairs."
- **Setup:** Compute the full cross-vendor correlation matrix under calendar-time-bin alignment and, separately, under release-index alignment, using identical estimator and permutation-null machinery in both cases; compare signs across the two schemes for every tested vendor pair. Corresponds to the first condition of `paper.md`'s H3 (E3).
- **Sample-size rationale:** Same Stage-2 config as RQ2/RQ3 — 6 vendors, 6 axes, ~400 prompts, 5 samples/prompt, ≥10k permutation draws (per `paper.md`'s Step 9: the walking-skeleton-to-Stage-2 transition is a config change, not new code paths).
- **Statistical test:** Same permutation machinery as RQ2/RQ3, run once per alignment scheme; agreement between schemes is assessed as a pre-registered sign match, not a new statistical test in its own right (avoids garden-of-forking-paths per `paper.md`'s E3 Verification note).
- **Expected outcome:** The sign of the correlation is identical under both alignment schemes for the majority of tested vendor pairs.
- **Metrics:** Per-pair correlation sign agreement rate across the two alignment schemes.

### RQ5 — Is cross-vendor drift correlation robust to removing the single most-correlated behavioral axis?

- **Tier:** mechanism
- **Target sub-problem:** `sp_dimensionality_weighting`
- **Target hypothesis (verbatim, Stage 5 `m_axis_robustness`):** "A significant aggregate cross-vendor drift correlation, if present, holds (is individually significant) on at least half of the tested behavioral axes, and remains significant after the single most-correlated axis is removed."
- **Setup:** Compute per-axis pairwise correlation across all six behavioral axes; identify the single axis contributing the largest correlation; recompute the aggregate correlation with that axis removed (leave-one-axis-out) and compare to the full-axis-set aggregate. Corresponds to the second and third conditions of `paper.md`'s H3 (E3): individually significant on ≥3 of 6 axes (BH q = 0.05), and significance surviving leave-one-axis-out.
- **Sample-size rationale:** Same Stage-2 config as RQ4 (6 vendors, 6 axes, ~400 prompts, 5 samples/prompt).
- **Statistical test:** Per-axis Benjamini–Hochberg-corrected significance testing (q = 0.05) via the same permutation machinery as RQ2–RQ4; leave-one-axis-out re-estimate of the aggregate correlation.
- **Expected outcome:** The aggregate correlation remains significant on a majority (at least 3 of 6) of individually-tested axes, and remains significant after the single most-correlated axis is removed.
- **Metrics:** Per-axis correlation significance count; leave-one-axis-out aggregate correlation and its change relative to the full-axis-set estimate.

### RQ6 — Does the primary (Vendi) cross-vendor diversity index show a declining trend?

- **Tier:** mechanism
- **Target sub-problem:** `sp_diversity_operationalization`
- **Target hypothesis (verbatim, Stage 5 `m_diversity_index`):** "The Theil–Sen slope of the primary (Vendi) diversity index is significantly negative over the studied window, with a total decline of at least 10% of the window-initial value."
- **Setup:** Compute the Vendi Score over vendors' per-axis behavioral profiles at each calendar time bin across the studied window, using the NoveltyBench/INFINITY-CHAT-style open-ended prompt set (see Datasets above); fit a Theil–Sen trend to the resulting time series; test the slope's sign by permuting time-bin labels. Corresponds to the first condition of `paper.md`'s H2 (E2).
- **Sample-size rationale:** Not separately quantified as a prompt count in either `discussion_trace.md`'s confirmed Stage 6 output or `paper.md` — both specify that the diversity computation needs its own open-ended prompt pool (rather than reusing the closed-form correlation-axis prompts) but do not state a numeric prompt count for it, unlike RQ2/RQ3's explicit ~400-prompt figure. This gap is reported rather than filled in.
- **Statistical test:** Theil–Sen regression on the D(τ) time series; slope-sign significance assessed by permuting time-bin labels (≥10,000 draws, per `paper.md`'s E2 Verification).
- **Expected outcome:** The Theil–Sen slope is significantly negative, with a total decline over the window of at least 10% of the window-initial index value.
- **Metrics:** Vendi Score time series; Theil–Sen slope and its permutation-based significance; percentage decline relative to window-initial value.

### RQ7 — Is the diversity trend's sign consistent across two independently constructed indices?

- **Tier:** mechanism
- **Target sub-problem:** `sp_diversity_operationalization`
- **Target hypothesis (verbatim, Stage 5 `m_diversity_index`):** "The sign of the diversity trend is consistent between the primary (Vendi) index and the secondary (mean pairwise CAPA-distance) index."
- **Setup:** Compute the secondary diversity index (mean pairwise CAPA-style functional distance across vendors) at the same calendar time bins as the primary Vendi index; fit a Theil–Sen trend to the secondary index; compare its sign to the primary index's trend sign. Corresponds to the second condition of `paper.md`'s H2 (E2): the primary index is pre-registered as Vendi specifically "to prevent index shopping."
- **Sample-size rationale:** Same underlying data and time bins as RQ6 (same open-ended prompt set, same calendar-bin structure); no separate prompt count is specified for the secondary index beyond reuse of RQ6's data.
- **Statistical test:** Theil–Sen trend fit to the secondary index; sign comparison against the primary index's trend, treated as a pre-registered sign match rather than a new significance test — the same "avoids garden-of-forking-paths" logic `paper.md` applies to RQ4's alignment-sign comparison.
- **Expected outcome:** The two indices' trend signs agree.
- **Metrics:** Sign agreement between the primary and secondary index trends.

### RQ8 — Does measured inter-version change exceed the empirically-measured noise floor?

- **Tier:** mechanism
- **Target sub-problem:** `sp_noise_floor`
- **Target hypothesis (verbatim, Stage 5 `m_noise_floor_gate`):** "At least two-thirds of true version-steps across the tested vendor panel exceed the empirically-measured noise floor ν — i.e., models measurably drift at all under this battery, which is a precondition for every other hypothesis in this study."
- **Setup:** Re-probe every pinned snapshot twice (split-half and two-week test–retest) to build the same-model score-delta distribution and derive the noise floor ν as its 95th percentile; compare every true version-step's drift-vector magnitude against ν across the tested vendor panel. This is `paper.md`'s `B0-NoDrift` baseline arm and its A4/PG-4 gate. `paper.md`'s Step 9 walking skeleton pilots this at reduced scale first: 3 open-weight vendor families (Llama, Qwen, Mistral — sidestepping closed-vendor snapshot-immutability risk) × 3 dated versions × ~150 prompts × 3 axes (refusal, instruction/format compliance, factuality only), greedy decoding (1 sample), for 2,700 local generations total, before the full Stage-2 panel is run.
- **Sample-size rationale:** Full-scale: every pinned snapshot in the tested vendor panel, re-probed twice. Pilot/skeleton scale (`paper.md` Step 9): 3 vendors × 3 versions × ~150 prompts, chosen to fit a ~10–20 A100-hour / ~$0 API-spend budget as a pass/fail gate before committing to the full multi-vendor API spend.
- **Statistical test:** No inferential significance test is specified — this is a fixed-threshold proportion gate: ν is defined as the empirical 95th percentile of the same-model re-probe delta distribution, and the pass criterion is a simple proportion comparison (≥2/3 of true version-steps must have ‖d_{v,t}‖ > ν). `paper.md` treats this as gate `PG-4`/assumption `A4`, not a hypothesis test with a p-value.
- **Expected outcome:** At least two-thirds of true version-steps exceed ν.
- **Metrics:** Proportion of version-steps with ‖d_{v,t}‖ > ν; the empirically-measured value of ν itself.

---

## Cross-references

- Full round-by-round derivation of these 8 RQs (draft → critique → refiner pass) is in `discussion_trace.md`, Stage 6 section.
- The paper's own narrative version of this same experiment design is in `paper_draft.md`'s "Experiments" section (RQ1–RQ8 subsections) — the two are kept in sync; this file adds sample-size rationale and statistical-test detail pulled from `../paper.md`'s Step 5/6 that the paper's prose section summarizes more briefly.
- One previously logged inconsistency, now **resolved** (2026-07-05 post-review revision round): `stage_review.md` → "Phase G — 2026-07-04" noted that `paper.md`'s H3 and `paper_draft.tex`'s RQ4 stated slightly different alignment-stability granularity (aggregate-ρ̄ sign vs. per-pair majority-sign). `paper.md`'s E3 now carries a "Granularity reconciliation note" recording that Stage 6 refined H3's first conjunct to the per-pair majority-sign form and declaring that form the operative binary criterion for scoring H3 — which is exactly the wording RQ4 above already uses verbatim. Whoever runs Phase B scores H3's first conjunct per-pair (> 50% of tested vendor pairs sign-stable), with the aggregate-ρ̄ sign match reported alongside as descriptive only.
