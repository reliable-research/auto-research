# Estimating Contamination from Generators You Have Never Seen: Robustness Limits of Distributional Estimators — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run. All ids (C1..C5, M1..M5, CO1..CO4, RQ1..RQ2, t1..t6) refer to digest.md nodes; nothing below contradicts the digest.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence.** A corpus's synthetic fraction is fixed at mixing time and is therefore *exactly* invariant to which generator wrote the synthetic text and to how heavily that text was later paraphrased — yet those two axes are precisely the ones along which every distributional estimator's decision statistic varies without bound, so estimator error is not noise but the structural price of reading a generator-invariant estimand off a generator-indexed statistic.

**判据 (deletion) test.** Domain nouns deleted:
> "A quantity is fixed at [Ø] time and is invariant to which [Ø] produced it and how it was [Ø]-ed, yet those are the axes along which every estimator's statistic varies without bound."

Without the domain nouns the clause "varies without bound while the estimand stays exactly fixed" has no referent: nothing forces an arbitrary quantity's estimator input to move unboundedly while its ground truth stays pinned. The sentence collapses to an empty template — it is NOT a valid generic statement. The load-bearing content is the *definitional* invariance of the controlled mixture ratio (C3) set against the *open-ended* variability of generators (C1) and paraphrase strength (C2). Passes: not a bridge, not a phenomenon restatement.

## Step 2 — Archetype

**Primary archetype:** Measurement / characterization study — map the *failure envelope* of an existing tool class (digest N12 = `empirical`). Deliverable is a degradation law, not a new estimator.
**Secondary archetype:** Falsification / negative-existence result (RQ2: does a generator-invariant feature exist?).

Downstream consequences:
- **(a) Abstract contribution slot:** a quantified degradation rate (LOGO gap, paraphrase slope) plus a feature-invariance verdict — CO1, CO2, CO3 — not a method that "beats" a baseline.
- **(b) Intro logic:** "what becomes measurable" — the first controlled, factorial characterization of *how fast* corpus-level estimators fail off-calibration and *whether* any signal survives — rather than "beat a number."
- **(c) Evidence standard:** effect sizes with generator-resampled bootstrap CIs and a pre-committed flatness test; a rigorous negative result for RQ2 counts as success (CO3), not failure.

## Step 3 — Taste self-audit

- **Bridge?** The opportunity is not "connect estimation and robustness." It is to measure a specific invariance-gap law (estimand fixed, statistic moves). PASS.
- **Synthesis?** The method reuses LOGO, paraphrase sweeps, and quantification correction (M1–M5). The non-synthetic core is the *estimand-invariance framing* + a factorial stress protocol that reads off a degradation *rate* and isolates the seen/unseen bit from generator difficulty. The contribution is the measurement, not the glue. PASS after centering the framing on the measured law.
- **Load-bearing verbs:** measure, isolate, gate, characterize, falsify — none from integrate/unify/leverage. PASS.
- **Abstract-opening rule:** v0 opens on the mechanism (invariant estimand vs generator-indexed statistic); the "X is increasingly used… however… we introduce" template is not used. PASS.

## Step 5 — Formal Problem Definition

**Estimand (R1, one sentence, added on Phase A re-check).** The quantity of interest is the absolute estimation error $\mathrm{AE}=|\hat r - r|$ of a corpus-level synthetic-fraction estimator, at the unit of analysis of one (test corpus, held-out generator, paraphrase-strength) cell, over the reference population of controlled human/synthetic mixtures built from the tested generator pool — feeding the decision of whether a distributional estimator's off-calibration reliability can be trusted for a training-corpus filtering/down-weighting policy (N2 motivation).

**Instrument validation (R2-lite, added on Phase A re-check — guidance.md Part 2 A2 evidence standard, Part 6 item 6).** The estimator suite's most instrument-like component is M3(a)'s supervised MGT classifier (the base classifier that classify-and-count and the quantification-corrected estimator both build on). Because ground truth here is objective-by-construction ($r$ is fixed at mixing time, not a subjective human judgment), the full 5-step R2 human-rater sequence does not apply verbatim; the applicable reduction is: ① the classifier is trained only on $G_{\text{cal}}$'s documents (never on $g^\ast$'s, by the LOGO design itself — this is what M1 already enforces); ② its held-out **in-distribution** accuracy (on a calibration-set validation split, disjoint from any LOGO test fold) must clear a pre-declared floor of AUROC $\ge 0.90$ before it is used in any LOGO comparison — an in-distribution accuracy below this floor means the base classifier itself is the bottleneck, not the LOGO gap, and the estimator is dropped from the suite rather than reported as "robust" or "fragile" on a broken base; ③ this floor is checked once per generator pool (frozen before the LOGO evaluation runs, mirroring R2⑤'s freeze-before-scale discipline) and is itself computed inside the walking skeleton (gate: PG-3b) so a failing base classifier is caught before any scale-up compute is spent.

**Notation.** Corpus $D$ of documents; true synthetic fraction $r\in[0,1]$ set by construction (M1). An estimator $\hat{E}$ maps $D\mapsto \hat{r}=\hat{E}(D)\in[0,1]$. Generators $g\in G$; calibration set $G_{\text{cal}}=G\setminus\{g^\ast\}$ for held-out $g^\ast$ (LOGO, M1). Paraphrase strength $k\in\{0,1,2,3\}$ (M2). Feature family $\phi$ with per-cell separability $\mathrm{AUROC}_{\phi}(g,k)$ (M5).

| Adjective/verb (from Claims) | Definition (computable) | Measured by |
|---|---|---|
| "degrade" | absolute error $\mathrm{AE}=\lvert \hat{r}-r\rvert$ increases | M4 |
| "faster under LOGO" | LOGO gap $\Delta_{\text{LOGO}}=\overline{\mathrm{AE}}_{\text{LOGO}}-\overline{\mathrm{AE}}_{\text{in-dist}}>0$ | M4 |
| "with paraphrase strength" | degradation slope $\beta_{\text{para}}=\partial\,\overline{\mathrm{AE}}/\partial k$ | M4 |
| "corrected degrades more slowly" | $\Delta_{\text{LOGO}}^{\text{corr}} < \Delta_{\text{LOGO}}^{\text{naive}}$ | M3, M4 |
| "does not close the gap" | $\Delta_{\text{LOGO}}^{\text{corr}}>0$ (sig.) | M4 |
| "generator-invariant feature" | $\mathrm{Var}_{(g,k)}[\mathrm{AUROC}_\phi]$ not sig. $>0$ AND $\min_{g,k}\mathrm{AUROC}_\phi \ge 0.70$ | M5 |
| "separable" | $\mathrm{AUROC}_\phi(g,k)\ge 0.70$ | M5 |
| "bias" | signed $E[\hat{r}]-r$ | M4 |

Every load-bearing adjective now maps to an equation over observables. None deleted.

## Assumptions (A1..A6)

> Each assumption below fills all five guidance.md §3.2 slots: assumption, failure_mode, detection, **gate**, **consequence**. `gate: PG-j` means checked inside the walking skeleton (Step 9) before scale-up; `gate: Phase C` means it requires the full scaled grid (≥3 generator families, full mixture/paraphrase sweep) and cannot be checked in the 3-generator pilot.

- **A1 (ground-truth validity).** Controlled binary mixture ratio = true contamination fraction (N1 constraint; C3). *Fails if* real contamination is co-authored/post-edited, not per-document-labelable (t2). *Detected by* a partial-post-editing robustness column (paraphrase applied to a fraction of each doc); if estimator ranking flips there, external validity is bounded and reported. **Gate:** Phase C (the partial-post-editing column is a scale-up addition, not part of the 3-generator walking skeleton). **Consequence:** if it fails, every H1/H2/H3 verdict is scope-restricted to "clean binary mixtures" and Claim 1 (Claim–Evidence Map) is downgraded to a bounded-envelope statement, not blocked outright — degrade, not block.
- **A2 (paraphrase on-manifold).** Paraphrase preserves meaning and does not push text off-manifold (M2; feasibility risk N6). *Fails if* heavy $k$ produces degenerate text that spuriously inflates error. *Detected by* the embedding-cosine fidelity gate (M2); results stratified by fidelity band; $k=0$ control always present. **Gate:** PG-2, checked inside the walking skeleton (the pilot already uses $k\in\{0,2\}$ with the fidelity gate live). **Consequence:** if it fails for some $(g,k)$ cells, those cells are excluded from the paraphrase-slope estimate for H1(ii)/H3 (not silently pooled), and the degradation-slope claim narrows to fidelity-passing cells only.
- **A3 (LOGO is truly OOD).** Held-out $g^\ast$ is structurally distinct from $G_{\text{cal}}$, not a resample of a seen generator (C1; t4). *Fails if* same-family artifacts leak. *Detected by* random intercept per generator *family* and CIs that resample generators, not just documents. **Gate:** Phase C (the pilot's 3-generator pool is too small to fit a per-family random intercept with any power; this check requires the scaled ≥3-family, 10–15-generator pool). **Consequence:** if it fails, H1(i) attribution is downgraded per the B-alt downgrade wording — degradation is reattributed to generator difficulty, not unseen-ness — and the RQ1 "unseen-ness" claim (not the raw LOGO-gap claim) is what falls.
- **A4 (pool diversity).** $G$ spans ≥3 families / multiple decoding configs so a degradation *rate* is estimable (t1). *Fails if* pool too homogeneous (LOGO gap ≈ 0 for a trivial reason). *Detected by* per-generator $\Delta_{\text{LOGO}}$ spread reported before pooling. **Gate:** Phase C (pool composition is a scale-up design choice; the pilot's 3 generators are a fixed, non-representative convenience set by construction). **Consequence:** if it fails, the degradation-rate estimate is reported as pool-specific only (t1's mitigation) and CO1/CO2 are scoped to the tested families rather than generalized — degrade, not block.
- **A5 (power).** ≥1000 docs per (generator, $k$, $r$) cell make a 0.03 AE difference detectable (N8 analysis plan). *Fails if* cells underfilled. *Detected by* the walking-skeleton pilot's realized CI width. **Gate:** PG-5, checked inside the walking skeleton (the pilot's ~1000-doc-per-cell target is sized to give an early read on realized CI width before the full grid is built). **Consequence:** per guidance.md Part 4 situation 5 / goal.md §8, any cell that fails this check is pre-declared **INCONCLUSIVE**, never scored as null and never silently dropped from the reported cell count; if the *central* RQ1 test cell is underpowered, the claim narrows to the powered cells only (situation 5's "narrow the claim" branch), not stopped outright.
- **A6 (clean human base).** Human side is genuinely human, not pre-contaminated. *Fails if* base corpus already contains AI text. *Detected by* a $k=0$ self-consistency check: estimators should return $\hat r\approx 0$ on the pure-human base. **Gate:** PG-6, checked inside the walking skeleton (this is the B0-adjacent placebo-style check the skeleton's pass criterion already requires, criterion (c)). **Consequence:** if it fails (non-null on pure-human base), this is a placebo-style non-null result — per goal.md §5 step 1 / Part 4 situation 1, the run is invalid, every H* is blocked from scoring, and the pipeline returns to diagnosing the human-base corpus before any re-run.

## Step 5b — Method-twin update (Phase A re-check, guidance.md Part 4 situation 6)

`discussion/reference_candidates.jsonl`'s 150-candidate harvest surfaced one genuine new method-twin, absent from the original OpenReview corpus search behind digest.md N3: **[Gumbel-Max-Watermark-Proportions, arXiv:2607.00224]**, *Sample Complexities of Estimating Gumbel–Max Watermark Proportions with and without Reduction to Pivotal Statistics* (now digest.md N3 item 10 / N4 item 7). **Concede:** it targets the identical estimand this paper does — a mixing proportion $\varepsilon$ of machine-generated text in an observed sample — with provably near-optimal sample complexity, which is more rigorous on the *estimator* dimension than anything in M3. **Differentiate:** its estimators are sample-efficient only under a cooperative watermarking assumption (a known pseudorandom scheme); it reports no result for a generator absent from that scheme and no paraphrase-attack condition, so it does not touch this paper's actual question (does *any* distributional estimator remain reliable when the generator is uncooperative and structurally unseen, and under paraphrase). This paper's contribution is positioned as the uncooperative/unseen-generator complement to that estimator theory, not a replacement for it — Threats (t1-class) should note that a watermark-cooperative regime is explicitly out of scope. **Repositioning is limited to `paper.md`/`digest.md` in this Phase A pass**; `paper_draft.md`/`.tex` (already compiled ahead of this cache upgrade) still need the same concede-and-differentiate paragraph added at the next Phase E pass (recorded in `discussion/stage_review.md`).

## Step 6 — Pre-Registered Experiments

### RQ1 — degradation rate under LOGO + paraphrase (N8 RQ1; CO1, CO2)
- **Assumption:** A1, A2, A3, A4, A5.
- **Hypothesis H1 (binary):** In the mixed-effects fit, (i) the regime coefficient $\Delta_{\text{LOGO}}\ge 0.05$ absolute error AND significantly $>0$; AND (ii) the paraphrase slope $\beta_{\text{para}}\ge 0.02$ per level AND significantly $>0$. **Both clauses must hold.**
- **Metric:** $\mathrm{AE}=\lvert\hat r-r\rvert$; $\Delta_{\text{LOGO}}=\overline{\mathrm{AE}}_{\text{LOGO}}-\overline{\mathrm{AE}}_{\text{in-dist}}$; $\beta_{\text{para}}=\partial\overline{\mathrm{AE}}/\partial k$ (N8 metrics).
- **Verification:** Linear mixed-effects model, fixed effects {regime (in-dist vs LOGO), $k$}, random intercept per generator family; 95% CIs via nonparametric bootstrap resampling *generators* (≥1000 resamples); α=0.05 Holm-corrected across the estimator suite (N8 analysis plan, hardened to resample generators per t4).
- **Fallback:** H1 fails on (i) only → claim "corpus-level estimators are unexpectedly robust to unseen generators once quantification-corrected; the dominant failure axis is paraphrase, not generator novelty." Fails on (ii) only → claim "paraphrase up to $k=3$ does not measurably degrade distributional estimation; generator novelty is the sole robustness axis." Both fail → route to F-G1.
- **Power pre-declaration (added on Phase A re-check — guidance.md Part 6 item 9 / goal.md §8, Part 4 situation 5):** any (generator, $k$, $r$) cell realizing fewer than the A5 floor of ~1000 documents, or a bootstrap CI on that cell's AE wider than 0.03 (the effect floor itself), is pre-declared **INCONCLUSIVE** for that cell before H1 is scored — never reported as a null/negative result and never silently excluded from the denominator of "how many cells were tested." If the central regime-coefficient test (H1(i)) itself draws on an underpowered majority of cells, H1 is not scored PASS/FAIL at all; the claim narrows to the powered subset and the gap in coverage is reported explicitly (situation 5's "narrow the claim" branch).

### RQ1-supp — quantification correction (Claim 3; CO1)
- **Assumption:** A5 (+ A1–A3).
- **Hypothesis H3 (binary):** $\Delta_{\text{LOGO}}^{\text{corr}} \le 0.70\cdot\Delta_{\text{LOGO}}^{\text{naive}}$ (correction cuts the gap by ≥30%) AND $\Delta_{\text{LOGO}}^{\text{corr}}>0$ significantly (gap not closed).
- **Metric:** paired $\Delta_{\text{LOGO}}$ for corrected vs naive classify-and-count (M3).
- **Verification:** paired bootstrap over generators on the gap difference; Holm within the suite.
- **Fallback:** Correction closes the gap ($\Delta_{\text{LOGO}}^{\text{corr}}$ not sig. $>0$) → stronger positive claim: "prior-shift quantification correction fully recovers LOGO robustness." No ≥30% reduction → claim "the LOGO gap is not primarily aggregate-proportion bias (C5); it is base per-instance classifier error."

### RQ2 — generator-invariant feature (N8 RQ2; CO3)
- **Assumption:** A2, A3, A4.
- **Hypothesis H2 (binary, negative predicted):** For every candidate feature $\phi$ tested, $\mathrm{Var}_{(g,k)}[\mathrm{AUROC}_\phi]$ is significantly $>0$ OR $\min_{g,k}\mathrm{AUROC}_\phi<0.70$ — i.e., **no** feature is generator-invariant.
- **Metric:** $\mathrm{AUROC}_\phi(g,k)$ per LOGO×$k$ cell; its cross-cell variance (N8 metrics).
- **Verification:** variance-components / Levene-style flatness test (H0: cross-cell variance = 0) per feature; α=0.05 Holm-corrected across features. A feature "passes invariance" only if it fails to reject H0 AND clears the 0.70 floor across all cells.
- **Fallback (publishable negative result):** H2 confirmed → CO3 negative branch: "no generator-invariant feature exists among {perplexity/log-likelihood, stylometric n-gram/burstiness, embedding-direction} — robust off-calibration estimation is empirically obstructed." Some feature passes → CO3 positive branch: report it as a candidate generator-invariant signature and characterize its AUROC floor.

### Mandatory baselines
- **B0 "why do this at all" — text-blind constant estimator.** Always outputs the calibration-set prior ratio $\bar r_{\text{cal}}$, ignoring the corpus. Justifies the problem: if real distributional estimators do not beat B0 *in-distribution* (lower AE at α=0.05), there is no working estimator whose degradation is worth measuring. **Gate:** proceed only if the best estimator's in-dist AE $<$ B0 AE by ≥0.05.
- **B-alt strongest-alternative-explanation — capability-matched seen/unseen swap.** Rival explanation: LOGO degradation arises because $g^\ast$'s text is *intrinsically harder to detect*, not because it is *unseen*. Control arm: evaluate the identical held-out documents from $g^\ast$ under two calibration regimes — $g^\ast$ **included** in $G_{\text{cal}}$ (seen) vs **excluded** (LOGO) — with pool size, budget, and $k$ matched. The seen−unseen AE difference isolates the pure OOD (unseen) effect with generator difficulty held constant. If this difference is not significant, degradation is difficulty, not novelty, and H1 attribution must be revised.

### Global fallback F-G1 (archetype pivot)
If the central hypothesis family fails (H1 both clauses fail AND B-alt shows no unseen effect), pivot from *degradation-law* to *positive-existence*:
> "Corpus-level contamination estimation is generator-robust: quantification-corrected distributional estimators recover the synthetic fraction within 0.05 absolute error even for wholly unseen generators and paraphrase up to $k=3$, and we identify the invariant statistic that underwrites this robustness."

## Step 9 — Walking Skeleton

Minimal closed loop answering ONE binary question: *does LOGO error measurably exceed in-distribution error for at least one real estimator, while estimators work when calibrated?*
- **Arms (2):** (1) naive classify-and-count; (2) quantification-corrected classify-and-count (M3). B0 (text-blind constant) computed for free as reference.
- **Smallest task set:** 3 generators (2 in $G_{\text{cal}}$, 1 held out), 1 domain (news/web prose), 1 mixture ratio $r=0.2$, $k\in\{0,2\}$; ~1000 docs per cell (A5).
- **Deterministic metrics only:** $\mathrm{AE}=\lvert\hat r-r\rvert$, $\Delta_{\text{LOGO}}$, and the A6 pure-human check ($\hat r\approx0$).
- **Expected cost:** ~2k synthetic docs + paraphrase for $k=2$ (~2k calls) + reused human base; single 7–13B open generator/paraphraser ≈ low tens of GPU-hours; estimator eval CPU-light. Wall-clock ~1–2 days.
- **Skeleton-passed criterion (scaling = config change):** PASS iff (a) best estimator in-dist AE $<$ B0 AE by ≥0.05 (B0 gate), AND (b) $\Delta_{\text{LOGO}}>0$ for ≥1 arm on the single held-out generator, AND (c) A6 check holds. On PASS, scaling to the full grid (12 generators × 5 ratios × 4 $k$ × 4 estimators, N6 Stage 2) is a manifest/config change to M1–M4, not new code.

## Claim–Evidence Map

| Abstract claim | Traces to | Status |
|---|---|---|
| Estimand is generator-invariant; estimators are generator-indexed | Step 0 + Step 5 defs | supported-by-design |
| Corpus estimators degrade under LOGO | H1(i), $\Delta_{\text{LOGO}}$ | needs-experiment |
| Error rises with paraphrase strength | H1(ii), $\beta_{\text{para}}$ | needs-experiment |
| Correction slows but does not close the gap | H3 | needs-experiment; fallback-covered |
| Degradation is unseen-ness, not difficulty | B-alt | needs-experiment |
| No generator-invariant feature exists (or one does) | H2 | needs-experiment; fallback-covered (both branches publishable) |
| Estimators beat a text-blind baseline in-distribution | B0 gate | needs-experiment |
| Findings pool-specific, may not generalize | A4, t1 | supported-by-design (scoped) |

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS)

The synthetic fraction of a corpus is fixed at mixing time and is exactly invariant to which generator produced the text and how heavily it was paraphrased — yet those two axes are where every distributional (corpus-level, ratio-based) contamination estimator's decision statistic varies without bound. We isolate and measure the resulting error. Using controlled human/synthetic mixtures at known ratios, we run leave-one-generator-out cross-validation crossed with a paraphrase-strength sweep and read off the estimation-error curves for classify-and-count, quantification-corrected, pooled zero-shot, and distribution-matching estimators. A capability-matched seen/unseen swap separates true unseen-generator degradation from mere per-generator difficulty. We further test, per statistical feature, whether human/synthetic separability stays flat across generators and paraphrase strength — falsifying or confirming a generator-invariant contamination signature. We report a degradation law and a pre-committed feature-invariance verdict; a negative result is a deliverable. (Draft — no experiments run.)
