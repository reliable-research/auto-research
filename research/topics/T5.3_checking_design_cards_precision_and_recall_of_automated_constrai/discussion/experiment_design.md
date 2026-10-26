# Experiment Design — T5.3: Checking Design Cards (Precision/Recall of Automated Constraint Verification)

> Standalone experiment protocol, assembled from Stage 6's confirmed output in `discussion_trace.md` (formerly part of `pipeline.md`) and `paper.md`'s Step 6 pre-registered experiment spec (E1–E3, mandatory baselines, walking skeleton). Status: **pre-registered design — no experiments have been run.** All thresholds below are design targets, not results. Nothing here is invented beyond what those two sources already specify; keep this file synchronized with `paper_draft.md`'s Experiments section if either is edited.

## Datasets

- **Constructed design-card corpus** — category-labeled across the five constraint categories (structural/architectural boundary, API-usage restriction, naming/style, security invariant, intent-level) and decomposed into item-level checkable predicates, following `rw_rlcfchecklists`'s checklist-decomposition template. *Justification:* the necessary substrate for `rq_category_stratified_reliability` and `rq_automatable_partition` — without category-labeled cards there is no unit to stratify results by.
- **Coding-agent patches seeded from real issue-to-pull-request tasks** (SWE-bench / SWE-bench Verified-style, `rw_swebench`) — ecologically real, not synthetic. *Justification:* supplies the realistic patches `rq_corpus_nontriviality_gate`'s non-obviousness pre-screen needs to be meaningful; a fully synthetic corpus would let violations be constructed as obvious by design, defeating the pre-screen's purpose.
- **Constructed violating-patch variants** — added per category only where real agent patches naturally yield too few violations to retain that category in the analysis. *Justification:* avoids conflating corpus scarcity with a null finding on constraint operationalizability (per `sp_corpus_nontriviality`'s technical challenge).
- **Overall corpus sizing (from `paper.md` E1 Verification):** ≥ 1,000 (card, patch) pairs total, ≥ 150 pairs per category, ≥ 30 adjudicated violations per category before that category is eligible for the main analysis (categories below this bar are forced to "inconclusive" regardless of point estimates — see `rq_corpus_nontriviality_gate` below).

## Baselines

Sanity-check / rival-explanation comparators, not outcome-tier competitors — this is a measurement study, and no RQ below claims "our verifier beats baseline X" as a headline contribution.

- **B0 — naive keyword/regex matcher.** No AST parsing, no LLM reasoning; matches card keywords/patterns against the raw diff text. *Role:* establishes the floor a verifier needs to clear to be worth building at all, and — more informatively — reveals which categories already need no further verifier research because B0 already reaches the human-agreement band there. Feeds `rq_verifier_beats_naive`.
- **B-alt — single-shot LLM judge.** No card decomposition, no category routing, no calibrated abstention; budget-matched in total token spend per pair to the full routed (hybrid) verifier. *Role:* isolates whether an observed category-level split reflects the constraints' intrinsic operationalizability or an artifact of the routing/decomposition mechanism. Feeds `rq_instrument_invariance`.
- **Calibrated selective-judge protocol (Trust-or-Escalate style) — secondary, non-gating comparator.** Reported descriptively per category alongside B0/B-alt, with no pass/fail criterion attached. *Role:* included because it is the nearest published calibrated-judge design, not because any RQ requires beating it (this was corrected during Stage 6's refiner pass, which moved it out of `datasets` — where it had been mislabeled — into this baselines section).

## Research Questions

All 8 RQs are **mechanism-tier** (one per Stage 5 hypothesis, verbatim). `study_type = empirical` forbids outcome-tier "beats baseline" claims as a headline result; 0 framing-tier RQs were emitted since no Stage 3 limitation was flagged `verify_as_hypothesis`.

### RQ1 — `rq_category_stratified_reliability` (targets `sp_operationalizability_spectrum`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "On the four structurally-defined categories (architectural boundary, API-usage restriction, naming/style, security invariant) jointly, the verifier reaches precision ≥ 0.85 and recall ≥ 0.80, with Wilson 95% CI lower bounds ≥ 0.75 for both."
- **Setup:** Across the four structurally-defined categories jointly, compute precision and recall against the adjudicated reference with Wilson 95% confidence intervals.
- **Sample-size rationale:** Sized so each category retains at least 30 adjudicated violations (per the corpus pre-screen gate, `rq_corpus_nontriviality_gate`), within the overall ≥1,000-pair / ≥150-per-category corpus — giving stable Wilson interval widths at the pre-registered thresholds.
- **Statistical test:** Wilson 95% confidence intervals on precision and recall.
- **Expected outcome:** Precision ≥ 0.85 and recall ≥ 0.80 on all four structural categories jointly, with Wilson 95% CI lower bounds ≥ 0.75 for both.
- **Metrics:** Per-category precision, recall, and their Wilson 95% confidence intervals.

### RQ2 — `rq_category_effect_significant` (targets `sp_operationalizability_spectrum`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "The intent-level category's F1 falls at least 0.15 below the minimum F1 among the four structural categories, and this category effect is statistically significant via a likelihood-ratio test on a logistic regression of per-pair verifier correctness on category, at α = 0.05."
- **Setup:** Fit a logistic regression of per-pair verifier correctness (correct/incorrect against the adjudicated reference) on category, with an agent covariate and card as a clustering unit for standard errors (per `paper.md` E1's H2 regression); compare the intent-level category's F1 to the minimum F1 among the four structural categories.
- **Sample-size rationale:** Same corpus as RQ1 (≥150 pairs / ≥30 violations per category); clustering by card in the regression accounts for non-independence of pairs sharing a card.
- **Statistical test:** Likelihood-ratio test on the category coefficient, α = 0.05.
- **Expected outcome:** Intent-level F1 falls at least 0.15 below the minimum structural-category F1, and the category effect is statistically significant.
- **Metrics:** Per-category F1; likelihood-ratio test statistic and p-value on the category coefficient.

### RQ3 — `rq_reference_usability` (targets `sp_reference_noise_ceiling`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "Fleiss' κ among the human reviewers is at least 0.4 in every constraint category, establishing the human–human reference as usable rather than assumed usable."
- **Setup:** Compute Fleiss' κ among the raw, pre-adjudication labels from the ≥3-reviewer panel, separately for each of the five categories.
- **Sample-size rationale:** r ≥ 3 independent reviewers per (card, patch) pair, over the ≥150-pairs-per-category corpus, for stable per-category κ estimates.
- **Statistical test:** Fleiss' κ (point-estimate threshold check against 0.4; no separate significance test specified in the source stages).
- **Expected outcome:** Fleiss' κ ≥ 0.4 in every category.
- **Metrics:** Per-category Fleiss' κ.
- **Note:** Any category failing this bar is reported as *reference-unstable* — any verifier comparison against it in RQ1/RQ2/RQ4 is treated as uninterpretable rather than as evidence about the verifier (per Stage 1's refined `objective`).

### RQ4 — `rq_automatable_partition` (targets `sp_reference_noise_ceiling`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "The verifier–human κ gap's 95% bootstrap CI (10,000 resamples, clustered by card) has an upper bound at or below 0.10 for at least two constraint categories, licensing an automatable classification for those categories, while the intent-level category's gap CI lower bound exceeds 0.10, licensing a human-required classification, with at most one category classified inconclusive."
- **Setup:** For each category with a usable reference (i.e., passing RQ3), compute the gap Δ_t = κ_H,t − κ_V,t between the human–human ceiling and verifier–human agreement, with a 95% bootstrap confidence interval.
- **Sample-size rationale:** Categories with fewer than 30 observed violations are forced to "inconclusive" regardless of the CI (per `paper.md` E2 Verification / `rq_corpus_nontriviality_gate`'s gate); 10,000 bootstrap resamples clustered by card.
- **Statistical test:** Bootstrap confidence interval (10,000 resamples, clustered by card); Holm correction applied across the 5 categories for the human-required tests.
- **Expected outcome:** At least two categories classified automatable (Δ_t CI upper bound ≤ 0.10), the intent-level category classified human-required (Δ_t CI lower bound > 0.10), and at most one category classified inconclusive.
- **Metrics:** Per-category Δ_t and its bootstrap confidence interval; resulting automatable/human-required/reference-unstable/inconclusive classification.

### RQ5 — `rq_instrument_invariance` (targets `sp_intent_vs_literal`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "A single-shot LLM judge with no card decomposition and no calibrated abstention (baseline B-alt), budget-matched in total token spend per pair to the full hybrid verifier, shows a per-category F1 pattern within 0.05 of the hybrid verifier's own per-category F1 pattern — i.e., the category-level split is attributable to the constraints' intrinsic operationalizability rather than to the routing/decomposition mechanism itself."
- **Setup:** Run the budget-matched single-shot judge (B-alt: no card decomposition, no routing, no abstention) on the same corpus, and compare its per-category F1 pattern to the full routed (hybrid) verifier's pattern.
- **Sample-size rationale:** Same corpus and per-category minimums as RQ1–RQ4.
- **Statistical test:** Threshold comparison of per-category F1 differences against a 0.05 tolerance (maximum absolute per-category difference); no additional significance test specified in the source stages.
- **Expected outcome:** The two verifiers' per-category F1 patterns agree within 0.05 on every category.
- **Metrics:** Per-category F1 for both verifier configurations; the maximum per-category absolute difference between them.

### RQ6 — `rq_verifier_beats_naive` (targets `sp_precision_recall_tradeoff`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim, unchanged by the Stage 6 refiner — only the RQ's description was reframed):** "The full hybrid verifier beats a naive keyword/regex matcher (baseline B0) on pooled paired violation/no-violation decisions (McNemar's test, α = 0.05, Holm-corrected across categories)."
- **Refined framing (non-tautological, per Stage 6 refiner pass):** the informative question is not whether the hybrid wins in aggregate (near-guaranteed and uninformative on its own), but for which specific categories B0 already reaches the human-agreement band (making further verifier engineering unnecessary there), and whether the full hybrid verifier improves on B0 on the remaining categories.
- **Setup:** Score B0 on the same corpus; compare its per-category agreement with the adjudicated reference against the human-agreement band established in RQ4; compare its paired decisions against the full verifier's via McNemar's test.
- **Sample-size rationale:** Same corpus as RQ1–RQ5.
- **Statistical test:** McNemar's test, α = 0.05, Holm-corrected across the five categories.
- **Expected outcome:** On any category where B0 already falls inside the human-agreement band, that category is reported as not requiring further verifier engineering; on the remaining categories, the full verifier's paired decisions improve on B0's at a statistically significant level.
- **Metrics:** Per-category agreement of B0 against the human-agreement band; McNemar's test statistic and Holm-corrected p-value per category.

### RQ7 — `rq_threshold_category_dependence` (targets `sp_precision_recall_tradeoff`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "No single confidence threshold clears a 0.85 precision floor simultaneously on all five constraint categories — the precision-maximizing operating threshold differs significantly across categories, demonstrating that operating points are not category-invariant."
- **Setup:** Compute a confidence-thresholded precision/recall operating curve per category; identify, per category, the lowest confidence threshold at which precision reaches 0.85.
- **Sample-size rationale:** Same corpus as RQ1–RQ6; per-category curves require the same ≥30-violation floor to be estimated reliably.
- **Statistical test:** Comparison of per-category threshold values against category-invariance (existence check: does any single threshold clear 0.85 precision on all five categories simultaneously); no additional formal significance test specified in the source stages.
- **Expected outcome:** No single confidence threshold clears a 0.85 precision floor simultaneously on all five categories.
- **Metrics:** Per-category precision/recall operating curves; per-category threshold at which precision first reaches 0.85.

### RQ8 — `rq_corpus_nontriviality_gate` (targets `sp_corpus_nontriviality`)

- **Tier:** mechanism.
- **Target hypothesis (verbatim):** "At least 20% of pairs surviving the human pre-screen in each constraint category have a median reviewer judgment time exceeding a pre-specified non-obviousness threshold, and at least 30 adjudicated violations are retained per category before that category enters the analysis; categories not meeting this bar are reported as inconclusive rather than folded into an aggregate."
- **Setup:** Among pairs surviving the human pre-screen, compute the share per category whose median reviewer judgment time exceeds the pre-specified non-obviousness threshold, and the retained adjudicated violation count per category.
- **Sample-size rationale:** This RQ *is* the corpus-sizing gate the other seven RQs depend on — the ≥30-violations-per-category and ≥20%-non-obvious-pairs bars are the pre-registered admission criteria for a category to enter RQ1–RQ7's analyses at all.
- **Statistical test:** Threshold/gate check against pre-registered bars (≥ 20% non-obvious share, ≥ 30 retained violations); descriptive gating criteria, not an inferential significance test.
- **Expected outcome:** At least 20% of surviving pairs per category are judged non-obvious, and at least 30 adjudicated violations are retained per category, before that category is included in RQ1–RQ7's analyses.
- **Metrics:** Per-category share of non-obvious pairs; per-category retained violation count.

## Mechanism analysis (supplementary — `paper.md` Step 6, E3)

Not a separate RQ (it explains *why* the RQ1–RQ8 pattern holds, rather than testing an independent falsifiable claim), but part of the same pre-registered protocol: on every verifier error the adjudicated panel disagrees with, a second independent coding pass (2 raters, disagreements adjudicated) classifies the error as (i) literal-vs-intent mismatch, (ii) structural/pattern-matching failure, or (iii) other. Budget: all errors on the two walking-skeleton categories (API, INTENT), plus a stratified sample of ≥20 errors per category at full scale. Reported as an error-taxonomy table (category × mechanism-type counts) alongside the RQ4 headline Δ_t numbers.

## Cross-reference note

All 8 target hypotheses above are verified verbatim matches to the Stage 5 confirmed-output hypotheses recorded in `discussion_trace.md`'s Stage 6 table and cross-stage consistency check (item 3: "every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓"), and to `paper_draft.md`'s Experiments section (RQ1–RQ8 expected-outcome/falsification-condition wording). If either `paper_draft.md` or this file is edited later, keep both synchronized per the skill's Final Deliverables spec.
