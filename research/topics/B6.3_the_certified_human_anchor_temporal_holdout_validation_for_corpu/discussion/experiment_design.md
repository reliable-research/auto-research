# Experiment Design — B6.3: The Certified-Human Anchor

> Standalone execution protocol for Stage 6 (Experiment Design) of the `auto-research-discussion` run. Sourced verbatim/without invention from two places: (1) `pipeline.md`'s Stage 6 confirmed output (`discussion_trace.md` § "Stage 6 — Experiment Design" holds the full critic/refiner record behind it), which supplies RQ2–RQ7 and their `target_hypotheses`, each a verbatim quote of a Stage 5 method's hypothesis; and (2) `paper.md`'s own pre-registered Step 6 (E1/H1, assumptions A1–A6), which supplies RQ1 — added directly to `paper_draft.md` during the adversarial-review pass (`pipeline.md`'s Phase Log, Phase G) because Hypothesis H1/Claim 1 had no corresponding research question in the Stage 5/6 pipeline output. Setup/expected-outcome/metrics text below matches `paper_draft.md`'s Experiments section (itself assembled from these same two sources); nothing here is invented beyond what those sources already state.
>
> `study_type = empirical` throughout (Stage 1, confirmed). All 7 RQs below are **mechanism-tier**. Zero framing-tier RQs (no Stage 3 related-work limitation was flagged `verify_as_hypothesis`). Zero outcome-tier RQs (`empirical` forbids "our procedure beats baseline X" framing — the detector battery and the mixture prevalence estimator are instruments under measurement, not competitors).
>
> Keep this file synchronized with `paper_draft.md`'s Experiments section and with `paper.md`'s Step 6 — a later edit to any research question, setup, or expected outcome in either of those must be mirrored here.

## Common design parameters

Per genre: 8–12 year-buckets × ~3,000 documents per bucket (per-bucket target set by the power calculation below). K = 3 instance-level detector families — `[DetectGPT, OpenReview:UiAyIILXRd]`, `[Learn-to-Distance, OpenReview:2ZUPeEM3FH]`, `[Disrupt-and-Recover, OpenReview:FiMZSxo4DO]` — plus the mixture estimator `[MonitorAIScale, OpenReview:bX3J7ho18S]`. Significance level α = 0.05 with Bonferroni correction across the 3 detectors (per-test α = 0.0167). All decision thresholds τ_k are frozen once on a held-out 2021 calibration split, disjoint from every evaluation bucket, before any evaluation FPR is computed (Assumption A4 — no threshold leakage). Success-vote aggregation rule, applied throughout: an effect counts as replicated if it holds for **≥ 2 of the 3 detector families**.

## Datasets

- **arXiv abstracts, 2007–2022** (single continuously-archived source) — primary pilot source; hard timestamps satisfy the purity/leakage constraints directly and provide ≥ 8 pre-2018 years needed for the leakage-immune sub-range control (RQ2).
- **CC-News / dated news archive** — a scale-up genre with faster topical churn, used to stress-test whether the composition-matching procedure (RQ5) and the drift result generalize beyond formal academic prose.
- **Project Gutenberg** (dated by first publication) — extends the anchor's temporal depth well beyond what any recent corpus offers, testing whether the confidence-bound envelope (RQ7) genuinely narrows for very old buckets or merely reflects thinner samples.
- **Reddit / Pushshift comments** (post-date stratified) — an informal, high-topic-churn genre used as an additional composition-matching stress test and to diversify the genre coverage the validity envelope must eventually bound.
- **HC3 (Human-ChatGPT Comparison Corpus)** — supplies the AI-side reference needed to build a known-ground-truth mixed target corpus for the reference-age propagation test (RQ6), where the true AI fraction is known by construction.
- **RAID (Robust AI Detection benchmark)** — used exclusively as a pre-registered instrument-validity check: before any threshold is frozen on the calibration split, each instance-level detector is confirmed to reproduce its expected ROC behavior on RAID's known-clean human/AI samples. This underwrites Assumption A4 (no threshold leakage), which every mechanism-tier RQ below depends on; it is not itself a claim-bearing dataset for any RQ's result.

## Baselines (validity-gate / sanity-check comparators — not outcome-tier competitors)

This is a measurement study; no research question below is framed as "our procedure beats baseline X."

- **Anchor-as-asserted control (B0).** Current practice: assume the nominal calibrated false-positive rate (ν = 1%) holds uniformly across the whole pre-2022 span. The paper's premise only has stakes if this control is actually violated (i.e., if RQ1's part (ii) holds).
- **Year-shuffle placebo.** Permute year labels within a source and refit the drift model. The placebo slope must be null (CI covering 0), or the measurement pipeline itself is manufacturing an artifact — a hard validity gate on the instrument, not a hypothesis to be supported or refuted.
- **Composition-matched resampled arm** (= RQ5's own method, `m_composition_matching`). The load-bearing rival-explanation control against the composition confound, not a competitor to beat.

## Sample-size / power foundation (Assumption A6, applies to all RQs below unless noted)

n_y ≈ 3,000 docs/bucket: for nominal FPR ν = 1%, a two-proportion test detects an absolute FPR difference of 1 percentage point between the earliest and latest bucket with power ≥ 0.9 at α = 0.0167 (the Bonferroni-corrected per-test α). Pilot gate PG-2 requires the chosen source to supply ≥ 3,000 docs/year for ≥ 8 pre-2022 years before scale-up; buckets whose realized confidence-interval half-width exceeds 1 percentage point are pre-declared **inconclusive**, never null.

---

## RQ1

- **Tier:** mechanism.
- **Target sub-problem:** none in the Stage 4/5 pipeline schema — sourced directly from `paper.md`'s own pre-registered Step 6 (E1/H1), not from a Stage 5 method. Its absence from the original Stage 5/6 pipeline output was flagged as a `[major]` in the adversarial-review pass (`pipeline.md` Phase Log, Phase G) and fixed by splicing it into `paper_draft.md` as RQ1.
- **Target hypothesis (verbatim, `paper.md` Step 6, Hypothesis H1):** "(i) pooled anchor FPR is nonzero — the 95% Clopper–Pearson lower bound on FPR_k pooled over all pre-2022 buckets is > 0.25% for ≥ 2/3 detectors; AND (ii) the bound is not uniform in time — max_y UCB_0.95(FPR_k(y)) > 2ν = 2% for ≥ 2/3 detectors. H1 passes iff both (i) and (ii) hold."
- **Setup.** On the primary single-source pilot corpus (arXiv abstracts, ≈3,000 documents per year-bucket, thresholds frozen on the 2021 calibration split per Assumption A4), the pooled false-positive rate across all pre-2022 buckets is computed per detector family, together with its 95% Clopper–Pearson interval, and the per-bucket upper confidence bound on false-positive rate is computed for every year.
- **Sample-size rationale.** Assumption A6 / Pilot gate PG-2 (see "Common design parameters" above): ≥ 3,000 docs/bucket, ≥ 8 pre-2022 years.
- **Statistical test.** Exact binomial confidence intervals per bucket; pooled confidence interval via stratified bootstrap (10,000 resamples) to respect bucket structure. No trend test is needed for H1 (that is RQ2's role).
- **Expected outcome.** Both hold for at least 2 of the 3 detector families: (i) the pooled anchor false-positive rate is nonzero — its 95% Clopper–Pearson lower bound exceeds 0.25%; and (ii) the bound is not uniform in time — the maximum per-year upper confidence bound exceeds twice the nominal calibrated rate.
- **Metrics.** Pooled false-positive rate and its Clopper–Pearson interval per detector family; per-bucket upper confidence bound on false-positive rate; the validity envelope E_k(ε,δ) evaluated at the pre-registered tolerance.

## RQ2

- **Tier:** mechanism.
- **Target sub-problem:** `sp_confound_disentanglement`.
- **Target hypothesis (verbatim, Stage 5 method `m_disentanglement_controls` → Stage 6 `rq_pre_llm_subrange`):** "The FPR-vs-year slope remains significant and same-signed when the drift regression is restricted to years at or before 2018 (a sub-range immune to post-2022-adjacent leakage by construction), for at least 2 of the 3 tested detector families."
- **Setup.** Using the primary single-source pilot corpus (arXiv abstracts, ~3,000 documents per year-bucket, with detector thresholds frozen on a 2021 calibration split disjoint from all evaluation years), the drift regression is refit restricted to years at or before 2018 only, for each of three instance-level detector families.
- **Sample-size rationale.** Same A6/PG-2 foundation as RQ1; the ≤2018 sub-range restriction is exactly why PG-2 requires ≥ 8 pre-2022 years in the first place — without that floor there would be no leakage-immune sub-range large enough to refit the regression on.
- **Statistical test.** Mixed-effects logistic regression (flag ~ Δ + (1|source); with a single source in the pilot, this degenerates to plain logistic regression with cluster-robust standard errors by bucket), Bonferroni-corrected across detectors; Mann-Kendall trend test as nonparametric corroboration — both must agree in sign.
- **Expected outcome.** The slope remains significant and positive — the same sign as the full-range slope — for at least 2 of the 3 detector families when restricted to the leakage-immune sub-range.
- **Metrics.** Per-bucket false-positive rate and confidence interval restricted to the sub-range; regression slope and confidence interval on the restricted range.

## RQ3

- **Tier:** mechanism.
- **Target sub-problem:** `sp_confound_disentanglement`.
- **Target hypothesis (verbatim, Stage 5 method `m_disentanglement_controls` → Stage 6 `rq_synthetic_drift_injection`):** "Synthetic-drift injection — graded lexical/syntactic perturbation applied to a single fixed year's human sample — produces a monotone increase in flagged rate with perturbation intensity, for at least 2 of the 3 tested detector families, replicating the sign of the slope observed on real year-to-year data."
- **Setup.** A single fixed year's human sample (drawn from the 2021 arm) is perturbed at five graded intensities of lexical and syntactic change (synonym substitution rate, sentence-length jitter, punctuation-convention shifts), and each detector's flag rate is measured at each intensity level, using the same fixed sample across all intensities (a paired design), per Assumption/Method M5.
- **Sample-size rationale.** Not separately specified beyond the primary per-bucket size (A6, ≈3,000 docs); because the design is paired — the same fixed sample reused across all 5 intensity levels — variance is controlled by the paired design rather than by an independently calculated sample size.
- **Statistical test.** Mann-Kendall trend test on flag rate versus perturbation intensity (paper.md's H2b Verification), with paper.md H2b's pre-registered effect floor: the monotone increase must amount to at least 1 percentage point absolute between the lowest and highest perturbation intensity (significance without magnitude does not pass); sign must replicate the direction of the real year-to-year slope from RQ2.
- **Expected outcome.** Flag rate increases monotonically with perturbation intensity for at least 2 of the 3 detector families, replicating the sign of the slope observed on real year-to-year data, with an absolute flag-rate increase of at least 1 percentage point between the lowest and highest perturbation intensity (the H2b effect floor).
- **Metrics.** Flag rate at each perturbation intensity; trend statistic and significance on flag rate versus intensity.

## RQ4

- **Tier:** mechanism.
- **Target sub-problem:** `sp_purity_unverifiability`.
- **Target hypothesis (verbatim, Stage 5 method `m_purity_bounding` → Stage 6 `rq_purity_spotcheck`):** "A human-audited spot-check of the hard-timestamped anchor sources estimates a residual mislabeling/impurity rate below 1%, keeping the impurity contribution to the reported FPR bound smaller than the magnitude of any detected drift effect."
- **Setup.** A human-audited spot-check sample of roughly 1,000–2,000 documents, stratified across year buckets and sources, is reviewed for misdating, later heavy revision, translation, or ghostwriting. Per Assumption A1, this runs as an R2-validated instrument, not a pass-through metadata read: provenance categories are grounded in the archival source's own timestamp/version-history metadata; the rubric is drafted and refined on a ~100-doc pilot slice before the full spot-check; two independent human annotators label the same spot-check sample, with inter-rater agreement required at κ ≥ 0.7 before the impurity estimate is trusted; disagreement patterns are inspected for systematic collapse; the rubric and threshold are frozen before scaling to the full sample.
- **Sample-size rationale.** 1,000–2,000 documents (digest N6 feasibility), stratified across year buckets and sources — large enough to bound impurity below 1% with a usable confidence interval while remaining feasible as a human-audited task (Pilot gate PG-1).
- **Statistical test.** Exact binomial confidence interval on the annotator-flagged impurity rate; Cohen's κ ≥ 0.7 inter-annotator agreement gate, required before the impurity number is trusted (if κ < 0.7, the rubric is refined and re-validated before any impurity number is reported).
- **Expected outcome.** The estimated impurity rate stays below 1%, with its upper confidence bound smaller than the magnitude of any detected drift effect from RQ2/RQ3.
- **Metrics.** Annotator-flagged impurity rate and its confidence interval; inter-annotator agreement rate (κ).

## RQ5

- **Tier:** mechanism.
- **Target sub-problem:** `sp_composition_confound`.
- **Target hypothesis (verbatim, Stage 5 method `m_composition_matching` → Stage 6 `rq_composition_matched_survival`):** "The FPR-vs-year slope detected in the raw single-source arm survives — same sign, comparable magnitude, and still significant at the pre-registered threshold — in a composition-matched resampled arm that equalizes topic-cluster and document-length distribution across year buckets."
- **Setup.** Each year bucket in the primary single-source corpus is resampled to equalize topic-cluster and document-length distribution against a reference bucket, at matched per-bucket token budgets (Assumption A3), and the drift regression is refit on this composition-matched resample. This is also the B-alt strongest-alternative-explanation control from `paper.md` Step 6: H2 is attributed to stylistic drift only if the slope survives in both this matched arm and the ≤2018 sub-range (RQ2).
- **Sample-size rationale.** Same A6 per-bucket target (≈3,000 docs) applied after resampling to matched token budgets; matching is a within-bucket reweighting, not a reduction in nominal sample size.
- **Statistical test.** Same mixed-effects logistic regression + Mann-Kendall corroboration as RQ2, applied to the matched resample, Bonferroni-corrected across detectors at the pre-registered α = 0.0167 threshold.
- **Expected outcome.** The slope survives — same sign, comparable magnitude, still significant at the pre-registered threshold — in the composition-matched arm.
- **Metrics.** Matched-arm slope and confidence interval; a per-bucket composition-similarity diagnostic relative to the reference bucket.

## RQ6

- **Tier:** mechanism.
- **Target sub-problem:** `sp_bias_propagation`.
- **Target hypothesis (verbatim, Stage 5 method `m_reference_swap_estimator`, refiner-pass version → Stage 6 `rq_reference_swap_bias`):** "Swapping the human reference fed into the mixture-based prevalence estimator from a recent bucket to the most temporally distant tested bucket (temporal distance ≥ 8 years), with the target corpus held fixed, shifts the estimated AI-fraction by at least 2 percentage points in the positive (older-reference-inflates-AI-fraction) direction, significant under a paired permutation test at α = 0.05 across held-out targets of both known and unknown composition."
- **Setup.** A target corpus is held fixed — both a synthetic mixture of known AI-fraction built from anchor human text plus an AI-side reference (HC3) at a known mixing ratio, and a real post-2022 corpus of unknown ground truth — while the human reference bucket fed into the mixture-based prevalence estimator (MonitorAIScale) is swapped between the most recent tested bucket (2021) and the most temporally distant tested bucket (Δ ≥ 8 years). Depends on Assumption A5 (estimator reproducibility with a swapped human reference); if irreproducible, falls back to a re-implemented mixture estimator of the same family, declared as such.
- **Sample-size rationale.** Held-out target corpora of both known and unknown composition (per A5); permutation test uses 10,000 permutations over document-to-reference assignments to guard against small-sample variance in the paired shift estimate rather than relying on a large-n asymptotic approximation.
- **Statistical test.** Paired permutation test (10,000 permutations over document-to-reference assignments), α = 0.05; on the known-composition target, additionally report the shift against ground-truth mixing ratio (absolute bias, not just relative shift). Mann-Kendall monotonicity of b(y) in Δ reported as a secondary check.
- **Expected outcome.** The estimated AI-fraction shifts upward by at least 2 percentage points when the aged reference is substituted, holding the target fixed, significant under a paired permutation test.
- **Metrics.** The shift in estimated AI-fraction between reference-bucket conditions; permutation-test significance; on the known-composition target, the absolute bias against the true mixing ratio.

## RQ7

- **Tier:** mechanism.
- **Target sub-problem:** `sp_envelope_calibration`.
- **Target hypothesis (verbatim, Stage 5 method `m_confidence_bounded_envelope` → Stage 6 `rq_envelope_conservatism`):** "The validity envelope defined by requiring the upper confidence bound on FPR to stay within a pre-declared tolerance of the nominal calibrated rate is strictly narrower than the envelope obtained from a naive raw-significance-threshold construction, for at least one tested source/genre — demonstrating the confidence-bound construction is load-bearing, not equivalent to the naive one."
- **Setup.** On the same fitted drift curve (from RQ2/RQ5), the validity envelope is constructed two ways — a naive construction that draws the boundary at the first year the raw slope's p-value crosses significance, and a confidence-bound construction (M4: E_k(ε,δ), pre-registered ε = 1 pp, δ = 0.05, Clopper–Pearson upper bounds) that draws the boundary at the largest contiguous range whose upper confidence bound on false-positive rate stays within a pre-declared tolerance of the nominal calibrated rate — and the two boundaries are compared directly, per source/genre.
- **Sample-size rationale.** Same A6/PG-2 per-bucket foundation; this RQ is specifically designed to test whether the confidence-bound construction behaves differently from the naive one precisely where per-year sample sizes shrink for older buckets (widening confidence intervals) — the comparison is only meaningful given the multi-genre, multi-bucket scale-up described in "Common design parameters" above.
- **Statistical test.** Not a significance test in the RQ1–RQ6 sense — a direct structural comparison: the boundary year is computed under each of the two envelope definitions and the two boundary years are compared. The falsification criterion is whether the two constructions produce an identical boundary across all tested sources and genres (falsified) versus a divergent, narrower confidence-bound boundary in at least one case (supported).
- **Expected outcome.** The confidence-bound envelope is strictly narrower — draws the safe boundary at a more recent year — than the naive envelope, for at least one tested source or genre.
- **Metrics.** The boundary year under each construction, per source/genre; the gap, in years, between the two boundaries.
