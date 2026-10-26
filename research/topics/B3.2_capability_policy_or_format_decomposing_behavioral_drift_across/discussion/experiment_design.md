# Experiment Design — B3.2: Capability, Policy, or Format?

> Standalone protocol rendered from Stage 6's confirmed output in `pipeline.md` (§"Stage 6 — Experiment Design") and `paper.md`'s own Step 6 pre-registered experiments (E1/E2/E3, Assumptions A1–A8, Step 9 walking skeleton). Nothing below is invented beyond what those two sources already specify; this document exists so the study is executable without opening the paper. Keep synchronized with `paper_draft.md`'s Experiments section and with `paper.md` if either is edited.
>
> **Tier accounting (per Stage 6, checked against `study_type = empirical`):** Mechanism-tier: 6 RQs, one per Stage 5 hypothesis, matched verbatim. Framing-tier: 0 (no Stage 3 limitation was flagged `verify_as_hypothesis`). Outcome-tier: 0 (`study_type = empirical` forbids "beats baseline X" framing — baselines below are sanity-check / misattribution-demonstration comparators only).
>
> **Gating order (paper.md Step 6):** E3 (calibration / `rq_calibration_recovery` + `rq_leakage_bound`) must pass before E1 (`rq_noise_floor_stability` + `rq_axis_decomposition_finding`) or E2 (`rq_cross_vendor_structure`) results are interpreted; the null-pair placebo (B-alt) runs alongside E1.

## Datasets

| Dataset | Battery | Justification |
|---|---|---|
| GSM8K, MMLU-Pro, HumanEval | Capability | Objectively verifiable, format-robust-scorable tasks (execution / exact-match) that anchor the capability battery. |
| LiveCodeBench | Capability | Rolling-release design prevents a capability-battery item from having differential training-data exposure across the two versions of a pair, which would otherwise confound a measured capability-axis change with a contamination artifact uncorrelated with true capability — exactly the confound `rq_axis_decomposition_finding`'s capability-share estimate needs ruled out to be interpretable. |
| XSTest, OR-Bench-Hard-1K, SORRY-Bench | Policy | The three strata (safe-but-seemingly-unsafe / pseudo-harmful / genuinely harmful) let a refusal-rate change be read against a fixed ground-truth harmfulness reference. |
| IFEval | Format | Directly measures instructed-format adherence, complementing the near-ceiling-correct prompt pool used for the rest of the format battery. |

## Baselines

Sanity-check / misattribution-demonstration comparators only — never outcome-tier competitors (`study_type = empirical` forbids a "beats baseline X" framing):

- **Blended-delta audit** (the `[ChatGPTBehavior, arXiv:2307.09009]` design; = paper.md's **B0**) — one blended per-task delta per pair, no format-robust scoring, no noise floor, no decomposition. Run on the M6 format-only constructed control pairs. **Pre-registered demonstration:** reports a nonzero "performance change" (|delta| > its own bootstrap CI) on ≥2/3 format-only controls — i.e., standard audit practice misattributes pure format drift as capability/policy change — while this paper's pipeline correctly attributes those same pairs to format. If B0 does *not* misattribute, the problem's practical motivation is downgraded from "documented mechanism" to "hypothetical" (pre-committed).
- **Null-pair placebo** (the same snapshot queried twice, in disjoint interleaved windows; = paper.md's **B-alt**, "strongest-alternative-explanation control") — because it is the same model against itself, the pipeline must find no axis exceeding the noise floor; any positive "detection" is a pipeline artifact, not evidence of the phenomenon. **Pre-registered criterion:** on every null pair, all three axis shares are statistically indistinguishable from the noise floor (permutation p ≥ 0.01 after correction); ≥2 null-pair detections across 3 vendors invalidates E1's positive findings pending diagnosis.
- **Two-way ablation** (capability+policy decomposition with the format axis removed) — run on format-only control pairs to show the third (format) axis is load-bearing, not decorative. **Pre-registered criterion:** two-way recovery accuracy on format-only controls must be ≤1/3 (no correct label available to it) while three-way recovery passes the calibration gate (H3).

---

## RQ: `rq_orthogonality_precondition`

- **Tier:** Mechanism
- **Target sub-problem:** `sp_entangled_causes`
- **Target hypothesis (verbatim, Stage 5 `m_battery_design_and_calibration` / Stage 6 confirmed):** "On format-only constructed control pairs (identical weights, altered template only), the capability battery's per-item correctness delta and the policy battery's refusal-rate delta are each not significantly different from their own within-version noise floor."
- **Setup:** On format-only constructed control pairs (identical weights, only the system template altered), measure the capability battery's per-item correctness delta and the policy battery's refusal-rate delta, and compare each against its own within-version noise floor.
- **Sample-size rationale:** Drawn from the same pool of 3 format-axis control pairs used for `rq_calibration_recovery` (3 per axis × 3 axes = 9 total, per M6) — no separate sample is constructed; this RQ is a diagnostic precondition check on that same pool (per Stage 5's refiner note: "one instrument, two checks on it, not two mechanisms").
- **Statistical test:** Per-battery permutation test of the observed delta against the within-version noise floor, on the format-only control pairs.
- **Expected outcome:** Neither the capability battery's correctness delta nor the policy battery's refusal-rate delta is significantly different from its own within-version noise floor on these format-only pairs.
- **Metrics:** Per-battery permutation-test p-value against the within-version noise floor, on format-only control pairs.

## RQ: `rq_calibration_recovery`

- **Tier:** Mechanism
- **Target sub-problem:** `sp_entangled_causes`
- **Target hypothesis (verbatim, Stage 5 `m_battery_design_and_calibration` / Stage 6 confirmed):** "Across at least 9 constructed control pairs (3 per axis), the blind decomposition procedure recovers the true dominant axis in at least 8 of 9 cases, with mean leakage share below 0.15."
- **Setup:** Across at least 9 constructed control pairs (3 per axis — capability: base vs. domain-SFT; policy: base vs. safety-SFT; format: identical weights, altered system template), run the complete pipeline with pair identities withheld from the analysis code (analyst-blind), and compare the predicted dominant axis against the true one, alongside the mean estimated leakage share.
- **Sample-size rationale:** n = 9 (3 per axis, per M6) is the pre-registered minimum for the exact binomial test to distinguish an 8/9 recovery rate from the 1/3 chance baseline at a meaningful significance level (exact binomial vs. p₀ = 1/3 gives p ≈ 0.0009 at 8/9); per Assumption A8/gate PG-7, per-cell power is recomputed from the walking-skeleton pilot's observed per-item variance (n=400, k=3) before any scale-up, and the minimum n per cell is fixed at the pilot-recomputed value, never reduced to raise a headline count.
- **Statistical test:** Exact binomial test against chance = 1/3, α = 0.05, n = 9, one-sided; leakage share estimated via M4's cross-axis regression with 1,000-resample bootstrap CI.
- **Expected outcome:** The pipeline recovers the true dominant axis in at least 8 of 9 control pairs, with mean leakage share below 0.15.
- **Metrics:** Recovery accuracy `Acc` (exact binomial test against 1/3 chance); mean leakage share `λ` with bootstrap confidence interval.
- **Power/INCONCLUSIVE carve-out (A8/PG-7):** if the pilot-recomputed per-cell power for detecting λ<0.15 is <0.9 for a given axis's 3 control pairs, that axis's contribution to `Acc` is reported as INCONCLUSIVE rather than scored pass/fail, and the ≥8/9 bar is evaluated only over the powered axes with the reduced denominator stated explicitly.
- **Fallback (pre-committed wording, paper.md E3):** If 6–7/9: "The instrument is partially calibrated: dominant-axis recovery exceeds chance (x/9, p = …) but not the pre-registered bar; real-pair results are therefore reported as dominant-axis calls with widened uncertainty, and per-axis percentage shares are demoted to exploratory." If ≤5/9 or λ ≥ largest axis share: instrument invalid → global fallback F-G1 (archetype pivot to negative result / measurement critique).

## RQ: `rq_leakage_bound`

- **Tier:** Mechanism
- **Target sub-problem:** `sp_leakage_measurement`
- **Target hypothesis (verbatim, Stage 5 `m_leakage_regression` / Stage 6 confirmed):** "The estimated cross-axis leakage share, measured via regression of capability/policy deltas on the other axes' independently measured features across the constructed control pairs, averages below 0.15 — the same threshold the calibration gate requires for the decomposition to be considered valid."
- **Setup:** Regress each control pair's capability-battery and policy-battery deltas on the other axes' independently measured features (format features for capability; lexical/surface cues for policy), and report the explained-variance fraction as the leakage share for that pair.
- **Sample-size rationale:** Uses the same 9 constructed control pairs as `rq_calibration_recovery` — leakage is estimated as a per-pair quantity within that pool, not from an independently sized sample.
- **Statistical test:** Bootstrap CI (1,000 item resamples) on mean and per-pair leakage share; threshold comparison against the pre-registered 0.15 bound.
- **Expected outcome:** The estimated leakage share averages below 0.15 across the constructed control pairs.
- **Metrics:** Mean and per-pair leakage share `λ(P)`, with bootstrap confidence intervals.

## RQ: `rq_noise_floor_stability`

- **Tier:** Mechanism
- **Target sub-problem:** `sp_noise_vs_drift`
- **Target hypothesis (verbatim, Stage 5 `m_noise_floor_model` / Stage 6 confirmed):** "For every tested version pair, the fitted within-version noise floor is stable across interleaved query windows (early-half estimate within 20% of the late-half estimate)."
- **Setup:** For every tested version pair (control and real), query both versions in interleaved time windows; compare the within-version noise-floor estimate computed from the early half of the study window against the estimate from the late half.
- **Sample-size rationale:** k = 5 repeated samples per item per version at fixed decoding settings (per Notation, Step 5); Assumption A2's gate (PG-2) requires the k=3-subset noise estimate to fall within 20% of the full k=5 estimate before trusting the floor, escalating k if it does not.
- **Statistical test:** Ratio comparison of early-half vs. late-half noise-floor estimate against a 20% tolerance; Assumption A1's gate PG-1 flags a between-window variance exceeding 2× the within-window variance (test "t2" per digest).
- **Expected outcome:** The early-half and late-half noise-floor estimates agree within 20% for every tested pair.
- **Metrics:** Ratio of early-half to late-half noise-floor estimate σ²_w(P), per pair and per battery.

## RQ: `rq_axis_decomposition_finding`

- **Tier:** Mechanism
- **Target sub-problem:** `sp_noise_vs_drift`
- **Target hypothesis (verbatim, Stage 5 `m_noise_floor_model` / Stage 6 confirmed):** "In at least 4 of 6 tested real version pairs, at least 2 of the 3 axes' contributions significantly exceed the estimated noise floor, and the format axis's share is at least 10% of explained drift in at least 3 of 6 pairs."
- **Setup:** Gated by `rq_calibration_recovery` passing. Across at least 6 real version pairs, permutation-test each axis's contribution against its pair's noise floor, and report the format axis's share of explained drift for each pair. ~3,000 items × 2 versions × 5 repeats per pair.
- **Sample-size rationale:** ≥6 real pairs from ≥3 vendors (Assumption A6), each with ~3,000 probe items (scaled up from the walking-skeleton's 400-item pilot) × 2 versions × k=5 repeats. Per Assumption A8/gate PG-7, per-cell power (6 pairs × 3 axes = 18 cells) is recomputed from the pilot's observed per-item variance before the k=5 scale-up, targeting ≥0.9 power to detect the pre-registered effect floor (η²≥0.10 for format share, λ<0.15 for leakage) at α=0.01, Holm–Bonferroni-corrected; minimum n per cell is fixed at the pilot-recomputed value, never reduced.
- **Statistical test:** Permutation test of axis contribution against the noise floor (10,000 label permutations) per axis-pair cell, α = 0.01, Holm–Bonferroni correction across the 6×3=18-cell family; 1,000-resample bootstrap CIs on all shares.
- **Expected outcome:** In at least 4 of 6 real version pairs, at least 2 of the 3 axes' contributions significantly exceed the noise floor, and the format axis's share is at least 10% of explained drift in at least 3 of 6 pairs.
- **Metrics:** Axis share η²_a(P) with bootstrap CIs; leakage share λ(P); within-version noise floor σ²_w(P); per-pair, per-axis permutation-test p-value.
- **Power/INCONCLUSIVE carve-out (A8/PG-7):** any of the 18 axis-pair cells whose pilot-recomputed power is <0.9 is excluded from both the numerator and denominator of the "≥4 of 6" / "≥3 of 6" counts and reported separately as INCONCLUSIVE (never as a pass, fail, or silent drop).
- **Fallback (pre-committed wording, paper.md E1):** (i) If decomposition binds but η²_fmt < 0.10 everywhere: "Once scoring is made format-invariant, format drift contributes negligibly (<10%) to measured version-pair drift; the widely-feared format confound is a scoring artifact, not a behavioral axis — blended audits need format-robust extractors, not a third axis." (ii) If leakage + noise absorb the majority of drift in most pairs: decomposition fails to bind → global fallback F-G1.

## RQ: `rq_cross_vendor_structure`

- **Tier:** Mechanism
- **Target sub-problem:** `sp_cross_vendor_comparability`
- **Target hypothesis (verbatim, Stage 5 `m_cross_vendor_agreement_test` / Stage 6 confirmed):** "The rank-ordering of axis dominance across version pairs, grouped by vendor, agrees significantly more than chance (Kendall's W ≥ 0.60 against a permutation null, p<0.05) across at least 6 pairs from at least 3 vendors, and pairs do not cluster tightly by vendor identity on the axis-share simplex beyond what the permutation null would produce."
- **Setup:** Gated by `rq_calibration_recovery` passing and `rq_axis_decomposition_finding` binding. Across at least 6 real version pairs from at least 3 vendors, summarize each pair as a point on the three-way axis-share simplex; compute Kendall's W over each vendor's rank ordering of axis dominance; separately check whether pairs cluster by vendor identity on the simplex.
- **Sample-size rationale:** ≥6 pairs from ≥3 vendors (Assumption A6) is the pre-registered minimum for the rank-agreement test; the small-n caveat is itself pre-registered (per Verification below), and the result is reported as graded evidence rather than a binary claim given the limited pair/vendor count.
- **Statistical test:** Kendall's W over per-vendor rank orderings of axis dominance, tested against a 10,000-draw permutation null, α = 0.05; secondary consistency check via silhouette score of vendor-labeled clustering on the axis-share simplex, tested against the same label-permuted null.
- **Expected outcome:** Kendall's W is at least 0.60 with permutation p < 0.05, and pairs do not cluster tightly by vendor identity beyond the permuted-null expectation.
- **Metrics:** Kendall's W with permutation-null p-value; silhouette score of vendor-labeled clustering against the permuted-label null.
- **Power/INCONCLUSIVE carve-out (A8/PG-7, inherited):** per paper.md's A8 gate (underpowered cells "pre-declared INCONCLUSIVE for H1/H2/H3 scoring"), a pair whose dominant-axis call rests on a cell reported INCONCLUSIVE under PG-7 is itself reported as INCONCLUSIVE for this test — excluded from the rank-agreement computation and its refutation, never silently dropped.
- **Fallback (pre-committed wording, paper.md E2):** "Drift structure is vendor-idiosyncratic: axis-dominance orderings do not agree across vendors (W = …, p ≥ 0.05) and/or pairs cluster by vendor; longitudinal audits therefore cannot assume a shared cross-vendor taxonomy and must be calibrated per vendor." This is treated as a fully publishable answer either way, since the underlying question is two-sided by construction.

---

## Mechanism analysis (beyond the headline tests)

**M7 — Feature-level leakage attribution** (paper.md Step 6, "guidance.md R6"). For every pair whose leakage share λ(P) clears a reportability threshold (λ ≥ 0.05), rank the M3 surface features (length, markdown density, list-vs-prose rate, hedging frequency, JSON-schema compliance, refusal-boilerplate rate) by the standardized regression coefficient magnitude from M4's cross-axis regression. **Pre-registered reporting rule:** the top-2 features by coefficient magnitude are named per pair in the results table; if the top feature differs from markdown density/length in a majority of leaky pairs, Claim 3's mechanism narrows explicitly to "a specific non-length surface dimension" rather than "format" generically.

## Global fallback F-G1 — archetype pivot

If the central hypothesis family fails (`rq_calibration_recovery` ≤5/9, or `rq_axis_decomposition_finding`'s leakage+noise dominance), the paper pivots from `empirical finding` to `negative result / measurement critique`, keeping the same data. **Pivoted abstract sentence (pre-committed, paper.md Step 6):** "We show that capability/policy/format attribution of LLM version drift is not identifiable from black-box behavior at practical probe budgets: even on control pairs whose dominant change axis is known by construction, blind recovery fails (x/9), placing a measured lower bound on the entanglement that every published longitudinal audit implicitly claims to see through." All raw outputs, batteries, and control recipes still release; the calibration protocol itself remains the reusable contribution.
