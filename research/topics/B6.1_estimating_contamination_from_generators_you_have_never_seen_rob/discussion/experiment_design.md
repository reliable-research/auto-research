# Experiment Design — B6.1: Robustness Limits of Corpus-Level Contamination Estimators

> Standalone Stage 6 execution spec, extracted from `pipeline.md`'s confirmed Stage 6 output (`## Stage 6 — Experiment Design`, now moved to `discussion_trace.md`) and `paper.md`'s Step 6/Step 9/Assumptions, reconciled with the already-assembled `paper_draft.md` Experiments section. Nothing below is invented beyond what those three sources already specify. Status: **specification — no experiments have been run; all numbers are pre-registered design targets.** Keep this file synchronized with `paper_draft.md`'s Experiments section if either is edited later.

## Tier accounting (per `pipeline.md` Stage 6, `study_type = empirical`)

- **Mechanism-tier: 7 RQs** — one per Stage 5 hypothesis, each `target_hypotheses` a verbatim quote of that hypothesis.
- **Framing-tier: 0 RQs** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our estimator beats baseline X" framing. All baselines below are sanity-check comparators or confound-isolation arms, never a competitor to beat.

## Datasets

- **Human base corpus** (real news/web prose) — provides the non-synthetic reference side. Justification: gives the leave-one-generator-out (LOGO)/paraphrase grid a stable reference not itself produced by any pool generator, so the pure-human self-consistency check ($\hat r \approx 0$ at $k=0$) is meaningful rather than trivially satisfied.
- **Multi-generator machine-text collections** (MGTBench- and RAID-style) — provide the synthetic side and cross-check corpus. Justification: each already spans multiple generator families, which is exactly the kind of pool a leave-one-generator-out design needs to be non-trivial — a pool of near-identical generators would make every LOGO fold artificially easy.
- **Paraphrased variants of the synthetic portion** (DIPPER-style paraphraser) at strength levels $k \in \{0,1,2,3\}$ rewrite rounds — directly operationalizes the paraphrase-strength axis at a controllable, ordered granularity, gated by an embedding-cosine semantic-fidelity check (A2) so degenerate high-$k$ rewrites do not masquerade as a paraphrase effect.
- **HC3** (human/ChatGPT comparison corpus) — *justification (refined during Stage 6's refiner pass, replacing an earlier "auxiliary in-domain human/synthetic reference" note that named no specific RQ):* provides matched human-authored and model-authored responses to the *same* prompts, which is specifically what the A6 pure-human self-consistency check needs (the `m_logo_calibration` method's $k=0$, $g^*$-absent control: every estimator should return $\hat r \approx 0$ on a corpus built entirely from HC3's human side). Because HC3 is not drawn from the same web-scrape distribution as the news/web base corpus, a passing self-consistency check on it is evidence the estimators aren't just keying on domain-specific artifacts of one human source.

## Baselines

(Sanity-check / confound-isolation comparators — not outcome-tier competitors. No RQ in this study is framed as "our estimator beats baseline X.")

- **B0 — text-blind constant estimator** ("why do this at all" gate). Always returns the calibration-set's prior mixture ratio $\bar r_{\text{cal}}$, ignoring the corpus entirely. If no real distributional estimator beats B0 in-distribution (lower AE at α = 0.05, by ≥0.05), there is no working estimator whose off-calibration degradation is worth measuring in the first place. **Gate:** proceed only if the best estimator's in-distribution AE is below B0's AE by ≥0.05.
- **B-alt — capability-matched seen/unseen swap** (confound-isolation arm for RQ4 / `sp_novelty_vs_difficulty_confound`, not a competitor). Evaluates the identical held-out documents from a generator $g^*$ under two calibration regimes — $g^*$ included in $G_{\text{cal}}$ (seen) vs. excluded (LOGO/unseen) — holding pool size, compute budget, and paraphrase strength $k$ matched between the two runs. The seen-versus-unseen AE difference isolates the pure unseen-ness effect, purged of the confound that a held-out generator's text might simply be intrinsically harder to detect. (Note: `paper.md`'s source material labels this a "baseline," but the Stage 6 cross-stage consistency check in `discussion_trace.md` explicitly reclassifies it as a Stage-5 method with its own hypothesis, since it targets a distinct sub-problem rather than functioning as a beat-or-lose comparator.)
- **Naive classify-and-count vs. quantification-corrected classify-and-count** — a matched pair, not a beat-baseline comparison; the value lies in their *difference* (RQ3), not in which one wins.

## Shared design elements (apply across all 7 RQs)

**Metrics common to the suite.** Absolute estimation error $\mathrm{AE} = |\hat r - r|$ and its condition-level mean; the leave-one-generator-out gap $\Delta_{\text{LOGO}}$ (mean LOGO error minus mean in-distribution error); the paraphrase-strength degradation slope $\beta_{\text{para}} = \partial\,\overline{\mathrm{AE}}/\partial k$; the seen-versus-unseen error difference on matched documents; per-feature AUROC and its cross-cell variance. Every significance test is run per member of the tested estimator suite or feature family and Holm-corrected within that suite before any RQ is scored, so a single favorable cell cannot be reported without accounting for the number of comparisons made.

**Sample-size / power rationale (A5, shared floor).** Every (generator, paraphrase-strength $k$, mixture-ratio $r$) cell is pre-declared to need **≥1000 documents** to detect the 0.03 absolute-error effect floor. A cell realizing fewer documents, or whose bootstrap confidence interval on AE is wider than 0.03, is pre-declared **INCONCLUSIVE** before any hypothesis is scored on it — never reported as a null result and never silently dropped from the denominator of cells tested. If a central test (RQ1's regime coefficient, or RQ7's flatness-and-floor criterion) draws on an underpowered majority of its cells, that RQ is not scored PASS/FAIL at all; the claim narrows to the powered subset and the coverage gap is reported explicitly.

**Instrument validation (paper.md R2-lite, applies to every estimator built on the supervised MGT classifier).** The classifier is trained only on $G_{\text{cal}}$'s documents (never on $g^*$'s — enforced by the LOGO design itself), and its held-out in-distribution accuracy (on a calibration-set validation split disjoint from any LOGO test fold) must clear a pre-declared floor of AUROC ≥ 0.90 before use in any LOGO comparison. Below this floor, the base classifier is dropped from the suite rather than reported as "robust" or "fragile" on a broken base.

---

## RQ1 — Leave-one-generator-out gap

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_open_generator_space`.
- **Target hypothesis (verbatim, Stage 5 `m_logo_calibration`):** "Mean absolute estimation error under leave-one-generator-out validation will exceed mean absolute error under in-distribution validation by at least 0.05, significantly, for the majority of tested estimators."
- **Setup.** For every tested (estimator × generator family) cell, compute mean absolute error under in-distribution validation and under leave-one-generator-out validation, holding harness, scenario sampling, and paraphrase level ($k=0$) fixed between the two conditions.
- **Sample-size rationale.** Sized so a 0.05 absolute-error difference is detectable with a generator-resampled bootstrap; subject to the shared A5 ≥1000-docs-per-cell floor and INCONCLUSIVE pre-declaration above.
- **Statistical test.** Part of the joint linear mixed-effects fit (fixed effects: calibration regime {in-distribution, LOGO}, paraphrase strength $k$; random intercept per generator family); 95% CIs via nonparametric bootstrap resampling *generators* (≥1000 resamples), not documents; α = 0.05, Holm-corrected across the estimator suite.
- **Expected outcome.** Mean absolute error under LOGO validation exceeds mean absolute error under in-distribution validation by at least 0.05, significantly, for the majority of tested estimators.
- **Falsification condition.** Refuted if the LOGO gap is not significantly greater than zero, or falls short of 0.05, for the majority of tested estimators — meaning current estimator designs already generalize acceptably to structurally unseen generators without further correction.
- **Metrics.** Mean absolute error per condition; $\Delta_{\text{LOGO}} = \overline{\mathrm{AE}}_{\text{LOGO}} - \overline{\mathrm{AE}}_{\text{in-dist}}$ and its generator-resampled bootstrap confidence interval.

## RQ2 — Paraphrase-strength degradation slope

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_paraphrase_margin_instability`.
- **Target hypothesis (verbatim, Stage 5 `m_paraphrase_sweep`):** "Mean absolute estimation error increases monotonically with paraphrase strength $k$, with a slope significantly greater than zero."
- **Setup.** Within the in-distribution and LOGO conditions alike, compare mean absolute error across paraphrase levels $k \in \{0,1,2,3\}$ via a monotonicity-oriented regression of error on $k$.
- **Sample-size rationale.** Same A5 floor (≥1000 docs per generator × $k$ × $r$ cell) and INCONCLUSIVE pre-declaration; cells failing the floor are excluded from the slope estimate, not silently pooled (per assumption A2's fidelity-band stratification).
- **Statistical test.** Slope term $\beta_{\text{para}} = \partial\,\overline{\mathrm{AE}}/\partial k$ read from the same joint mixed-effects fit as RQ1 (or a standalone monotonicity regression on $k$), with significance assessed against zero; Holm-corrected across the estimator suite.
- **Expected outcome.** Mean absolute error increases monotonically with paraphrase strength $k$, with a slope significantly greater than zero.
- **Falsification condition.** Refuted if the estimated slope is not significantly positive, or if error is non-monotonic (e.g., peaks at an intermediate $k$ and declines) across the tested range — meaning paraphrase strength, as parameterized here, is not the degradation driver hypothesized.
- **Metrics.** Slope of mean absolute error on $k$, with confidence interval; per-level mean absolute error.

## RQ3 — Quantification-correction gap reduction

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_aggregation_bias`.
- **Target hypothesis (verbatim, Stage 5 `m_quantification_correction`):** "The corrected estimator's leave-one-generator-out gap will be smaller than the naive estimator's gap by at least 30%, but will remain significantly greater than zero — correction reduces, but does not eliminate, degradation."
- **Setup.** Compute $\Delta_{\text{LOGO}}$ separately for the naive classify-and-count estimator and the quantification-corrected estimator on identical test corpora.
- **Sample-size rationale.** Same shared A5 floor, applied per estimator arm; the paired design (identical test corpora for both arms) reduces variance relative to an unpaired comparison at the same per-cell document count.
- **Statistical test.** Paired bootstrap over generators on the gap difference $\Delta_{\text{LOGO}}^{\text{naive}} - \Delta_{\text{LOGO}}^{\text{corr}}$; Holm-corrected within the estimator suite.
- **Expected outcome.** The corrected estimator's LOGO gap is smaller than the naive estimator's gap by at least 30%, but remains significantly greater than zero.
- **Falsification condition.** Refuted toward "correction is not load-bearing" if the reduction in $\Delta_{\text{LOGO}}$ is below 30% or not statistically distinguishable from zero; refuted toward "correction fully resolves the gap" if the corrected estimator's $\Delta_{\text{LOGO}}$ is not significantly greater than zero.
- **Metrics.** Paired difference in $\Delta_{\text{LOGO}}$ between corrected and naive estimators, with bootstrap confidence interval.

## RQ4 — Unseen-ness vs. intrinsic difficulty

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_novelty_vs_difficulty_confound`.
- **Target hypothesis (verbatim, Stage 5 `m_capability_matched_swap`):** "The seen-versus-unseen absolute-error difference, computed on the identical held-out documents, will be significantly greater than zero — i.e., detectability of the specific generator alone does not explain the leave-one-generator-out gap."
- **Setup.** For a fixed set of documents from a given generator, compute absolute error twice under matched pool size, compute budget, and paraphrase strength — once with that generator included in calibration (seen), once excluded (unseen) — this is the B-alt baseline/confound-isolation arm described above.
- **Sample-size rationale.** Same shared A5 floor per generator; because the comparison is paired on identical documents, the design needs fewer independent generators than an unpaired cross-generator comparison would to achieve the same power.
- **Statistical test.** Paired test over documents within generator, comparing seen vs. unseen absolute error.
- **Expected outcome.** The seen-versus-unseen absolute-error difference on identical held-out documents is significantly greater than zero.
- **Falsification condition.** Refuted if the seen-versus-unseen difference is not statistically distinguishable from zero — meaning the LOGO gap observed in RQ1 is driven by which generators happen to be difficult, not by calibration status, undermining any claim that "unseen-ness" specifically is the cause. (Per assumption A3, this RQ's attribution claim also requires the held-out generator to be structurally distinct from $G_{\text{cal}}$, not a resample of a seen generator family — checked via a per-family random intercept, gated at Phase C scale.)
- **Metrics.** Paired seen-versus-unseen absolute-error difference, with confidence interval.

## RQ5 — Calibration-regime effect net of paraphrase strength

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_confounded_stress_factors`.
- **Target hypothesis (verbatim, Stage 5 `m_joint_stress_design`, first estimand):** "The calibration-regime coefficient remains significant after controlling for paraphrase strength in the joint fit."
- **Setup.** In the joint mixed-effects fit (absolute error regressed jointly on calibration regime and paraphrase strength, random intercept per generator family), read off the regime coefficient's significance after the paraphrase-strength term is included.
- **Sample-size rationale.** Requires the full factorial grid (all generators crossed with all $k$ levels) at the shared A5 per-cell floor, since the joint fit's power depends on cell coverage across both factors simultaneously, not just marginal totals.
- **Statistical test.** Joint linear mixed-effects specification with both calibration regime and paraphrase strength as fixed effects and a random intercept per generator family — one instrument, two separately falsifiable estimands (this RQ reads the regime estimand; RQ6 reads the paraphrase estimand from the same fit).
- **Expected outcome.** The calibration-regime coefficient remains significant in the joint fit.
- **Falsification condition.** Refuted if the regime coefficient is not significant once paraphrase strength is included jointly — meaning the apparent LOGO effect observed univariately in RQ1 is actually attributable to a paraphrase-strength imbalance between conditions, not to calibration regime itself.
- **Metrics.** Regime coefficient estimate, standard error, and significance from the joint fit.

## RQ6 — Paraphrase-strength effect net of calibration regime

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_confounded_stress_factors`.
- **Target hypothesis (verbatim, Stage 5 `m_joint_stress_design`, second estimand):** "The paraphrase-strength coefficient remains significant after controlling for calibration regime in the joint fit."
- **Setup.** In the same joint mixed-effects fit as RQ5, read off the paraphrase-strength coefficient's significance after the calibration-regime term is included.
- **Sample-size rationale.** Same full-factorial-grid requirement as RQ5 — both estimands are read from one fit, so the sample-size need is shared, not additive.
- **Statistical test.** Same joint linear mixed-effects specification as RQ5 (both coefficients estimated jointly in the same model rather than via two separately fit models, which could each misattribute variance to the wrong factor).
- **Expected outcome.** The paraphrase-strength coefficient remains significant in the joint fit.
- **Falsification condition.** Refuted if the paraphrase-strength coefficient is not significant once calibration regime is included jointly — meaning the apparent paraphrase effect observed univariately in RQ2 is actually attributable to an imbalance in which generators appear at which paraphrase level, not to paraphrase strength itself.
- **Metrics.** Paraphrase-strength coefficient estimate, standard error, and significance from the joint fit.

## RQ7 — Generator-invariant feature existence

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_feature_invariance_search`.
- **Target hypothesis (verbatim, Stage 5 `m_invariance_probe`):** "No candidate feature family will simultaneously pass the cross-cell flatness test and the 0.70 per-cell floor across all tested held-out-generator × paraphrase-strength cells — the negative branch will be the observed outcome, though a partial-invariance ranking across features remains reportable regardless."
- **Setup.** For each candidate feature family (reference-model log-likelihood/perplexity; stylometric n-gram and burstiness statistics; sentence-embedding directions), compute human/synthetic separability (AUROC) in every tested held-out-generator × paraphrase-strength cell.
- **Sample-size rationale.** Requires the full combinatorial evaluation grid (all held-out generators × all $k$ levels) at the shared A5 per-cell floor, since invariance is explicitly a worst-cell property — an underpowered cell cannot be excluded from consideration the way it can for an average-case claim.
- **Statistical test.** Pre-committed cross-cell flatness test (variance-components / Levene-style, $H_0$: cross-cell AUROC variance = 0) per feature, combined with an absolute floor (AUROC ≥ 0.70) required in every cell; α = 0.05, Holm-corrected across the feature families tested. A feature "passes invariance" only if it fails to reject $H_0$ AND clears the 0.70 floor across all cells.
- **Expected outcome.** No candidate feature family simultaneously passes the flatness test and the 0.70 floor across all tested cells — the negative branch is the observed outcome, though a partial-invariance ranking across features remains reportable.
- **Falsification condition.** Refuted (a generator-invariant feature exists) if some candidate feature passes both the flatness test and the 0.70 floor across every tested cell — supporting the positive branch: identification of a candidate generator-invariant signature, reported together with its AUROC floor.
- **Metrics.** Per-cell AUROC for each feature family; cross-cell variance and flatness-test p-value; minimum per-cell AUROC.

---

## Global fallback (archetype pivot)

If the central hypothesis family fails (RQ1 and RQ2 both fail AND RQ4's B-alt swap shows no significant unseen effect), the study pivots from a *degradation-law* framing to a *positive-existence* framing (per `paper.md` Step 6, "Global fallback F-G1"):

> "Corpus-level contamination estimation is generator-robust: quantification-corrected distributional estimators recover the synthetic fraction within 0.05 absolute error even for wholly unseen generators and paraphrase up to $k=3$, and we identify the invariant statistic that underwrites this robustness."

## Walking skeleton (minimal closed loop, per `paper.md` Step 9)

Before running the full grid, a walking skeleton answers one binary question: *does LOGO error measurably exceed in-distribution error for at least one real estimator, while estimators work when calibrated?*

- **Arms (2):** naive classify-and-count; quantification-corrected classify-and-count. B0 (text-blind constant) computed for free as reference.
- **Smallest task set:** 3 generators (2 in $G_{\text{cal}}$, 1 held out), 1 domain (news/web prose), 1 mixture ratio $r = 0.2$, $k \in \{0,2\}$; ~1000 docs per cell.
- **Deterministic metrics only:** $\mathrm{AE} = |\hat r - r|$, $\Delta_{\text{LOGO}}$, and the A6 pure-human check ($\hat r \approx 0$).
- **Pass criterion (scaling = config change):** PASS iff (a) best estimator's in-distribution AE is below B0's AE by ≥0.05, AND (b) $\Delta_{\text{LOGO}} > 0$ for ≥1 arm on the single held-out generator, AND (c) the A6 pure-human check holds. On PASS, scaling to the full grid (12 generators × 5 ratios × 4 $k$ levels × 4 estimators) is a manifest/config change, not new code.
