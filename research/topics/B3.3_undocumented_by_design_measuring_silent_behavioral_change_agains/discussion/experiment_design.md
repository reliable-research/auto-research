# Experiment Design — B3.3: Undocumented by Design? Measuring Silent Behavioral Change against Vendor Changelogs

> Standalone protocol assembled from Stage 6's confirmed output in `pipeline.md` ("## Stage 6 — Experiment Design") and `paper.md`'s own Step 6 / Step 9 experiment-design content (Pre-Registered Experiments, Walking Skeleton, Claim–Evidence Map). Nothing below is invented beyond those two sources — this is the document to execute from without opening `paper_draft.md`. Status: **specification, no experiments run.** All numbers are pre-registered design targets, not results. Keep synchronized with `paper_draft.md`'s Experiments section if either is edited.
>
> **Tier accounting** (checked against `study_type = empirical`, per Stage 1): **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim). **Framing-tier: 0 RQs** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`; none manufactured. **Outcome-tier: 0 RQs** — `empirical` study type forbids "our procedure beats baseline X" framing; the two prior black-box detectors below are sanity-check comparators only, never competitors to beat.
>
> **Numbering crosswalk to `paper.md`'s H1–H3 pre-registration:** RQ1 ↔ H3(b) (A/A false-positive bound, gate PG-1); RQ2 ↔ H1 (silent-rate majority, cross-vendor vote rule); RQ3 ↔ H3(a) (alignment F1, gate PG-3); RQ4 ↔ H2 (category concentration). RQ5 and RQ6 carry no H-number — they are the pre-registered instrument-validity checks for boundary attribution (assumption A4, gate PG-4) and probe-coverage stability (assumption A5, gate PG-5).

---

## Datasets and probe sources

Each category is anchored to an independently published, externally-validated benchmark chosen for a purpose unrelated to this study, rather than invented after seeing which probes show silent changes — this is what makes `rq_category_concentration`'s eventual concentration finding non-circular (per `m_category_anchored_taxonomy`, Stage 5).

| Source | Category anchored | Justification |
|---|---|---|
| MMLU | Factual QA | Established, broad-coverage knowledge benchmark; category boundary fixed independently of any observed silent-change pattern. |
| GSM8K | Reasoning / math | Established math-reasoning benchmark, same independence property. |
| TruthfulQA | Hallucination / factual-accuracy failure modes | Established truthfulness benchmark. |
| XSTest | Safety / refusal — **over-refusal direction** | Probes the false-positive direction of a silent safety-behavior change (safe prompts wrongly refused). |
| AdvBench / HarmBench | Safety / refusal — **under-refusal direction** | Probes the false-negative direction (harmful prompts answered when they should be refused). Both XSTest and AdvBench/HarmBench are required jointly: a vendor could silently shift refusal behavior in either direction between versions (tightening refusal to reduce liability, or loosening it to reduce false-refusal complaints), and using only one source would leave the safety/refusal category blind to whichever direction it did not cover. |
| IFEval | Formatting / instruction-following | Established instruction-compliance benchmark. |
| BFCL | Tool / function-calling | Established function-calling benchmark. |
| Self-scraped vendor changelog / release-note corpus (OpenAI, Anthropic, Google API release notes) | — (documentation-of-record) | The text `m_entailment_alignment` aligns detected diffs against; not a probe source. |

**Probe suite scale.** Stage-0 pilot: ~200 probes across 5–6 categories (per `paper.md` Step 9 Walking Skeleton). Scale-up: ≥3 vendors × multiple transitions each, ~1.5k probes per vendor at full Stage 1 scale.

## Baselines (sanity-check comparators, not outcome-tier competitors)

`study_type = empirical` forbids "beats baseline X" framing (Stage 6 tier accounting); every baseline below exists to validate an instrument property, not to be beaten for a headline claim.

| Baseline | Role | Justification |
|---|---|---|
| Same-version (A/A) null control | Necessary control for every cross-version claim | Identical pipeline run on two same-version resamples; instantiates `m_calibrated_diff_detector`'s hypothesis directly — if the detector finds "diffs" here, it manufactures its own findings. |
| Naive keyword/string-match changelog aligner (B0) | Weak lower baseline for the entailment aligner | If a trivial string matcher already labels most diffs as documented, semantic alignment adds nothing and the problem is a lookup, not an inference — this justifies `m_entailment_alignment`'s existence. |
| Prior black-box change-detection tools: logprob-distribution two-sample tracker (`rw_logprobtracking`); rank-based model-substitution test (`rw_rankuniformity`) | Change-detection-only comparators | Run as sanity checks on this pipeline's added coverage (does a probe's diff also get flagged by a narrower prior detector), never as a documented/silent-rate or F1 number to beat — neither prior tool produces a documented/silent label or aligns to changelog text, so they are not I/O-matched baselines (per Stage 3 refiner note on `rw_chen2023`, `rw_logprobtracking`, `rw_rankuniformity`). |

---

## RQ1 (`rq_aa_control`) — Does the diff detector control false positives against a same-version null while still detecting cross-version change?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_signal_from_noise`.
- **Target hypothesis (verbatim, Stage 5 / `m_calibrated_diff_detector`):** "The same-version (A/A) null control will flag a same-version resample pair as containing a detected diff (D=1) at a rate at or below the nominal α=0.05, while the cross-version arm's count of detected diffs will exceed the A/A arm's false-diff count by at least 3×."
- **Setup.** Pilot stage: one vendor, one clean-boundary version transition, ~200 probes across 5–6 categories, $N=50$ samples per snapshot. The identical procedure is additionally run on a same-version (A/A) resample pair at equal sampling budget. Scale-up: ≥3 vendors × multiple transitions each.
- **Sample-size rationale.** $N=50$ samples/snapshot balances API cost against the resolution needed to estimate the same-version null distribution by within-version resampling; ~200 probes across 5–6 categories is the smallest task set that exercises every category at pilot scale (per `paper.md` Step 9 Walking Skeleton), sized to detect a ≥3× margin between cross-version and A/A false-diff counts, not to power a fine-grained per-category test (that is RQ4's job).
- **Statistical test.** Permutation/bootstrap two-sample test at $\alpha=0.05$, Holm–Bonferroni corrected across probes within a transition; effect-size floor $|\text{Cliff's }\delta| \ge 0.33$ required in addition to significance.
- **Expected outcome.** The A/A control flags detected diffs ($D=1$) at a rate at or below the nominal $\alpha=0.05$; the cross-version arm's detected-diff count exceeds the A/A arm's false-diff count by at least $3\times$.
- **Falsification / fallback.** Refuted if the A/A false-diff rate exceeds $\alpha$, or if the cross-version arm's detected-diff count does not exceed the A/A arm's by the pre-registered $3\times$ margin. Per the pre-registered fallback (Stage 6 / `paper.md` RQ1 Fallback F1's detector-side counterpart), an A/A false-diff rate exceeding $\alpha$ does not end the study: the effect-size floor is recalibrated upward to the smallest value restoring FPR $\le \alpha$, all rates are re-derived under the corrected floor, and the corrected floor is reported transparently alongside the original.
- **Metrics.** Detected-diff rate and count, cross-version vs. A/A; margin ratio between the two arms.

## RQ2 (`rq_silent_rate`) — What fraction of detected behavioral diffs have no matching changelog claim?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_prose_to_behavior_alignment`.
- **Target hypothesis (verbatim, Stage 5 / `m_entailment_alignment`, first of its two hypotheses):** "The overall silent-change rate ρ (fraction of detected diffs with no matching changelog claim) exceeds 0.50, with the bootstrap 95% CI lower bound also exceeding 0.50."
- **Setup.** For every probe flagged $D(p)=1$ in a transition, compute the documented/silent label via the entailment aligner against that transition's parsed changelog claims; aggregate into an overall rate $\rho$, reported per vendor rather than pooled.
- **Sample-size rationale.** Bootstrap CI requires $\geq 1000$ resamples for a stable 95% interval. Because $\rho$ is scored per vendor, the **cross-vendor vote rule** (`paper.md` Step 6 RQ1 aggregation) requires $\geq 3$ tested vendors for a PASS/FAIL verdict; a vendor contributing fewer than 20 detected diffs is excluded from the vote as underpowered (not counted as a "no"). At Stage-0 pilot scale with only one vendor tested, the hypothesis is not scored PASS/FAIL — it is reported **INCONCLUSIVE-pending-scale-up** until the $\geq 3$-vendor vote is available.
- **Statistical test.** Bootstrap 95% confidence interval on $\rho$ ($\geq 1000$ resamples); cross-vendor majority vote (PASS requires $\rho>0.50$ with CI lower bound $>0.50$ in $\geq 2$ of the $\geq 3$ tested vendors).
- **Expected outcome.** The cross-vendor vote passes: $\rho$ exceeds 0.50 with the bootstrap 95% CI lower bound also exceeding 0.50 in at least 2 of the $\geq 3$ tested vendors.
- **Falsification / fallback.** Refuted if the cross-vendor vote fails (fewer than 2 of $\geq 3$ vendors clear the threshold). Per the pre-committed Fallback F1, the claim then shifts from "silence is the default" to "silence is a material minority" — reporting the measured $\rho$ and its CI directly, per vendor — with the headline reframed around RQ4's existence-and-category-structure finding rather than majority prevalence.
- **Metrics.** Overall silent-change rate $\rho$ with bootstrap CI, per vendor.

## RQ3 (`rq_alignment_validity`) — Does automatic changelog alignment reproduce human documented/silent labels, and does it improve on a naive string-match floor?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_prose_to_behavior_alignment`.
- **Target hypothesis (verbatim, Stage 5 / `m_entailment_alignment`, second of its two hypotheses):** "M4's automatic documented/silent labeling achieves F1 ≥ 0.70 against a human-labeled subset, exceeding the naive string-match baseline's F1 by a nontrivial, pre-specified margin."
- **Setup.** A human-labeled subset of diff/claim pairs is adjudicated by two annotators with disagreement resolution. The entailment aligner's documented/silent labels are compared against this human-labeled subset via F1, and against the naive string-match aligner's F1 on the same subset.
- **Sample-size rationale.** $\geq 200$ diff/claim pairs, chosen so that Cohen's $\kappa$ and F1 estimates on the human-labeled subset are stable enough to support a $\geq 0.6$ validity threshold on $\kappa$ and a $\geq 0.70$ threshold on F1; two independent annotators plus adjudication is the minimum needed to compute inter-annotator agreement at all.
- **Statistical test.** F1 against a fixed 0.70 threshold; F1 comparison between entailment aligner and string-match baseline (nontrivial, pre-specified margin); Cohen's $\kappa$ required $\geq 0.6$ for the human labels themselves to be considered valid ground truth.
- **Expected outcome.** The entailment aligner achieves $F1 \geq 0.70$ against human labels, exceeding the string-match baseline's F1 by a pre-specified, nontrivial margin.
- **Falsification / fallback.** Refuted (alignment unreliable) if entailment-aligner F1 falls below 0.70; refuted (semantic matching unnecessary) if the string-match baseline's F1 is statistically indistinguishable from the entailment aligner's. Per the pre-registered Fallback F3, an F1 below 0.70 does not retract the method: the automatic aligner is downgraded from a headline instrument to a human-in-the-loop aid, and the silent-change rate is reported only on the human-labeled subset, with the automatic-pipeline claim explicitly relabeled "assistive."
- **Metrics.** F1 (entailment vs. human, string-match vs. human), Cohen's $\kappa$ on the human-labeled subset.

## RQ4 (`rq_category_concentration`) — Do silent changes concentrate in specific, externally-anchored behavior categories?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_category_construct_validity`.
- **Target hypothesis (verbatim, Stage 5 / `m_category_anchored_taxonomy`):** "ρ_c is non-uniform across the externally-anchored categories (chi-square rejects equality at α=0.05), with safety/refusal, formatting/instruction-following, and latency/cost each significantly exceeding factual-accuracy in pairwise, Holm-corrected proportion tests."
- **Setup.** Per-category silent-change rate $\rho_c$ is computed for each benchmark-anchored category; categories below the minimum-diff threshold are pooled and reported as underpowered rather than tested individually.
- **Sample-size rationale.** Minimum 20 detected diffs per category to enter the chi-square/pairwise tests — the same underpowered-exclusion threshold used for the cross-vendor vote in RQ2, applied here at the category level so a category with too few diffs cannot drive a spurious significance result.
- **Statistical test.** Chi-square homogeneity test of $\rho_c$ across categories at $\alpha=0.05$; Holm-corrected pairwise proportion tests for the three predicted orderings (safety/refusal, formatting/instruction-following, latency/cost each vs. factual-accuracy).
- **Expected outcome.** $\rho_c$ is non-uniform across categories (chi-square rejects equality at $\alpha=0.05$), with safety/refusal, formatting/instruction-following, and latency/cost each significantly exceeding factual-accuracy in the pairwise tests.
- **Falsification / fallback.** Refuted (pervasive, category-agnostic silence) if the homogeneity test does not reject uniformity — Fallback F2 then reports "silent change is pervasive and category-agnostic." Refuted in direction (different concentration pattern) if $\rho_c$ is non-uniform but the predicted ordering does not hold — in that case the observed concentration, whatever it is, is reported as the finding, since the taxonomy's value is in surfacing genuine structure, not confirming a specific predicted order.
- **Metrics.** Per-category $\rho_c$ with bootstrap CIs; chi-square statistic; pairwise proportion test results.

## RQ5 (`rq_boundary_validity`) — Does restricting headline claims to fingerprint-clean version boundaries matter for the reported rate?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_boundary_attribution`.
- **Target hypothesis (verbatim, Stage 5 / `m_boundary_fingerprinting`):** "Transitions flagged as clean-boundary by the fingerprint-discontinuity test show a significantly higher rate of detected diffs (D=1) than transitions without a discontinuity, and restricting the headline silent-change rate to clean-boundary transitions yields a materially different estimate than a naive pooled estimate that includes quarantined transitions."
- **Setup.** Continuous fingerprint logging (first-token top-k log-probability profile) classifies each candidate transition as clean (fingerprint discontinuity exceeds within-version variance) or quarantined (no clear discontinuity — undated or rolling changes). The detected-diff rate is compared between clean and quarantined transitions, and the headline silent-change rate computed on clean transitions only is compared against a naive estimate pooling all transitions including quarantined ones.
- **Sample-size rationale.** Requires enough candidate transitions across the vendor set to populate both a clean and a quarantined bucket with a nonzero detected-diff count in each; this is the one RQ whose power depends on naturally occurring vendor release-cadence variation rather than a chosen $N$, so it is evaluated opportunistically across whatever transitions the polling period yields, restricted at minimum to the one clean-boundary transition required by the Stage-0 pilot (`paper.md` Step 9).
- **Statistical test.** Proportion test comparing detected-diff rate between clean and quarantined transitions; comparison of clean-only vs. naive pooled silent-change rate for material (not just wider-uncertainty) difference.
- **Expected outcome.** Clean transitions show a significantly higher detected-diff rate than quarantined ones, and the clean-only headline rate differs materially from the naive pooled estimate.
- **Falsification condition.** Refuted if detected-diff rates are statistically indistinguishable between clean and quarantined transitions, or if the clean-only and naive pooled rates agree within noise — either would mean the fingerprint-based boundary check is not load-bearing and a simpler, calendar-based pairing would have sufficed.
- **Metrics.** Detected-diff rate by transition-cleanliness status; clean-only vs. pooled silent-change rate comparison.

## RQ6 (`rq_coverage_stability`) — Is the silent-change rate stable across independent random subsets of the probe suite?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_partial_identification`.
- **Target hypothesis (verbatim, Stage 5 / `m_coverage_stability_check`):** "Silent-change rate estimates computed from two disjoint random halves of the probe suite, within the same transition, agree within a pre-specified tolerance in a majority of tested (vendor × transition) cells."
- **Setup.** For each (vendor × transition) cell with sufficient detected diffs, the probe suite is split into two disjoint random halves and the silent-change rate is recomputed independently on each half; agreement between the two half-sample rates is compared against a pre-specified tolerance.
- **Sample-size rationale.** Needs enough (vendor × transition) cells with sufficient detected-diff counts that "a majority of tested cells" is a meaningful statement rather than a claim about one or two cells; this is checked at Stage 1 scale-up (≥3 vendors × multiple transitions), not inside the cheap pilot, because the probe-subset ablation needs the full Stage-1 suite to be meaningful (per `paper.md` Assumption A5 / Gate PG-5).
- **Statistical test.** Split-half rate agreement compared against a pre-specified tolerance; proportion of tested cells meeting that tolerance, required to exceed a majority (>50%).
- **Expected outcome.** The two half-sample rates agree within the pre-specified tolerance in a majority of tested cells.
- **Falsification condition.** Refuted if agreement falls below the majority threshold across tested cells — that would mean the reported rate is sensitive to which probes happened to be included, undermining its interpretation as a property of the vendor's disclosure practice rather than of an arbitrarily chosen probe list.
- **Metrics.** Split-half rate agreement rate across tested cells.

---

## Global fallback (all RQs)

If the central hypothesis family fails outright — RQ2's cross-vendor vote does not pass **and** RQ4's category rates turn out uniform (silent change is neither prevalent nor structured) — the contribution pivots from a measurement-finding paper to an instrument paper: the validated, error-characterized documentation-fidelity pipeline itself becomes the headline contribution, and the result is reframed as an accountability-relevant calibration finding (vendor changelogs for the tested systems are largely faithful), per `paper.md` Step 6 "Global fallback F-G1."

## Walking skeleton (smallest go/no-go before scale-up)

Per `paper.md` Step 9: on one vendor, one clean-boundary version transition, does the pipeline detect ≥1 statistically-genuine behavioral diff (D=1, $|\delta|\ge0.33$) with no matching changelog claim, while flagging ~0 diffs on a same-version A/A control? Three arms: (1) cross-version pipeline, (2) same-version A/A null control, (3) B0 string-match aligner on the same diffs. ~200 probes across 5–6 categories, $N=50$ samples/probe. Skeleton passes if the cross-version arm yields ≥1 silent diff, the A/A arm yields ≤ $\alpha\cdot$(#probes) false diffs, and the entailment threshold $\tau$ is set on a ≥20-pair dev slice. If passed, scaling to full Stage 1 (3 vendors × 4 transitions × ~1.5k probes) is a config change, not a new code path.
