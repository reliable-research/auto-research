# Experiment Design — T5.1: Mining the Unwritten Rules

> Standalone protocol document, per the `auto-research-discussion` skill's "Final deliverables" spec: this is the document to execute from without opening the paper. Built from Stage 6's confirmed output in `pipeline.md` (now moved to `discussion_trace.md`) and `paper.md`'s Step 5/Step 6 ("Pre-Registered Experiments"). All hypotheses below are copied verbatim from `paper.md`'s Step 6 (the more recent, Phase-A-fixed version, which added effect floors, a power/thin-cell rule, and a mechanism-analysis plan on top of the Stage 5/6 discussion's originally confirmed hypotheses — see `discussion_trace.md`'s Stage 5/6 sections for the pre-fix wording and `pipeline.md`'s Phase log for the fix history). Nothing below is invented; every setup/threshold/test comes from `paper.md` or `pipeline.md`. Status: specification — no experiments have been run; all numbers are pre-registered design targets.

---

## Estimands (R1, from paper.md Step 5)

(i) For the extraction family (RQ1–RQ3): the precision and recall of a mined implicit-design-constraint catalog against human-annotated review threads, unit of analysis = one catalog entry (precision) or one held-out thread (recall proxy), reference population = the 5 pilot repositories' review history, feeding the decision of whether automated catalog mining is trustworthy enough to apply at scale at all. (ii) For the compliance family (RQ4–RQ8): the category-wise rate at which test-passing patches violate the validated catalog, unit of analysis = one (patch, category) pair, reference population = test-passing SWE-bench-Verified agent patches (≥3 systems) and their matched human-gold patches in the same repos, feeding the decision of whether test-suite success is a sufficient certification signal for autonomously-opened agent PRs.

---

## Datasets

- **SWE-bench Verified** (500 human-validated repository-issue tasks) — supplies the pilot repositories (django, scikit-learn, sympy, matplotlib, sphinx), the issue set, and the matched human gold patch for every agent patch tested in RQ7/RQ8. This pairing is what makes a matched-pair comparison possible at all.
- **Public SWE-bench leaderboard submission patches** — the source of test-passing agent patches from at least three distinct agent systems, needed so RQ7/RQ8's violation distribution is not an artifact of one agent's idiosyncratic style.
- **PR review-history corpus** harvested from the five pilot repositories — the raw material RQ1–RQ4 mine and validate the catalog from; chosen to overlap exactly with the SWE-bench Verified repository set so the catalog and the patches judged against it come from the same projects' actual norms.

## Baselines

Sanity-check / necessity comparators, not outcome-tier competitors — this is a measurement study (`study_type: empirical`), and no research question here is framed as "our procedure beats baseline X."

- **Keyword/directive-pattern extractor** (regex over should/must/please/avoid/never plus code-element mentions) — necessity check for RQ2: if a naive lexical pattern-matcher already recovered as much as the LLM extractor, semantic understanding would not be doing real work in candidate identification.
- **Existing linter/architecture rule inventories** (ruff, pylint, import-linter) — coverage check for RQ3: establishes what fraction of the catalog is already formalized elsewhere, which is what "unwritten" has to mean operationally.
- **Catalog-free zero-shot LLM judge** (the RLAC-style per-output latent-rubric protocol, borrowed per the related-work stage's sharpened role — not a comparison against RLAC's own reported results) — ablation control for RQ5/RQ7/RQ8: isolates whether a stable, multi-thread-supported, mined catalog finds anything a same-model judge without that catalog would not already find on its own. **Null-result interpretation (pre-committed):** if catalog-guided and catalog-free judging materially agree on which patches violate which rules, that would *not* refute the orthogonality finding (RQ5 — test-passing still carries no compliance information either way; CO2/CO4 may still stand on the catalog-free judge's own numbers). It *would* refute the catalog's own specific contribution: the paper's real instrument would be "a capable LLM asked to look for problems," not the mined, multi-thread-supported catalog, and CO1/CO3 would downgrade to "not demonstrated."
- **Matched human gold patches (B0)** — the necessary reference distribution for RQ8's agent-vs-human comparison, and the "why do this at all" control: if human gold patches already violate the catalog at the same rate as agent patches, there is no agent-specific compliance gap to characterize.

---

## Research Questions

Tier accounting (checked against `study_type = empirical`): **8 RQs, all mechanism-tier** — one per Stage 5 hypothesis. Framing-tier: 0 (no Stage 3 limitation was flagged `verify_as_hypothesis`). Outcome-tier: 0 (`empirical` forbids "our procedure beats baseline X" framing; the keyword baseline and catalog-free judge are sanity-check/ablation comparators embedded inside mechanism-tier RQs, never a competitor to beat).

### RQ1 — Does the mined catalog clear a pre-registered precision bar against human annotation?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 RQ1(i)):** "On the 5 pilot repos, catalog-entry precision Wilson-95%-CI lower bound ≥ 0.60 on the n=300 dual-annotated sample."
- **Setup.** A stratified sample of 300 catalog entries from the pilot repositories is dual-annotated as genuine project constraints or spurious; recall is estimated by having annotators independently mine constraints from 100 held-out review threads and checking what fraction the pipeline recovered. Wilson 95% confidence intervals are computed on both proportions. A pilot gate (precision ≥ 0.5 on an n=100 candidate sample) must pass first before this full-scale measurement is run (A1/A2, gate PG-1/PG-2).
- **Sample-size rationale.** n=300 for the precision sample and n=100 held-out threads for the recall proxy are the pre-registered sizes (paper.md Step 6, digest N8 analysis plan) chosen to support a Wilson 95% CI tight enough to distinguish the ≥0.60 target from the ≤0.5 pilot-gate floor.
- **Statistical test.** Wilson 95% CI on precision and on the recall proxy; Cohen's kappa reported (not gated) for the underlying dual-annotation agreement.
- **Expected outcome.** Catalog-entry precision's Wilson 95% CI lower bound is at least 0.60.
- **Metrics.** Precision (Wilson 95% CI); recall proxy (Wilson 95% CI); Cohen's kappa for dual-annotation agreement.

### RQ2 — Does recognizing a constraint require semantic understanding, or does a naive lexical pattern already suffice?

- **Tier:** Mechanism (explicitly reframed at Stage 5 as a necessity check on the mechanism, not an outcome-tier competitive claim).
- **Target hypothesis (verbatim, paper.md Step 6 RQ1(ii), reframing carried from Stage 5's refiner pass):** "LLM extractor beats the keyword/directive baseline on paired thread-level detection, McNemar p<0.05 in the LLM-favoring direction, with a minimum paired-accuracy gap of ≥8 percentage points as the effect floor (significance without this floor does not satisfy (ii)) — tested as a necessity check on the mechanism (does recognizing a constraint require semantic understanding of what the comment and its diff hunk say, or does a naive lexical pattern already suffice), not as a claim that this paper's pipeline outperforms a rival system to be beaten."
- **Setup.** The LLM extractor and the keyword/directive-pattern baseline are run over the same change-inducing comments, and their thread-level constraint-detection outputs are compared via a paired McNemar's test, α = 0.05.
- **Sample-size rationale.** Drawn from the same change-inducing comment pool mined for the catalog (paper.md Step 6); paired design (same comments scored by both extractors) maximizes power per comment relative to an unpaired design.
- **Statistical test.** McNemar's test, α = 0.05, in the extractor-favoring direction, with an 8-percentage-point paired-accuracy gap as a co-required effect floor.
- **Expected outcome.** The LLM extractor achieves significantly higher paired thread-level detection accuracy than the keyword baseline, with the gap at or above the 8-point floor.
- **Metrics.** Paired thread-level detection accuracy; McNemar's test statistic and p-value; paired-accuracy gap in percentage points.

### RQ3 — Is the catalog's content genuinely absent from existing static-analysis tooling?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 RQ1(iii)):** "Linter-expressibility rate < 0.50 (i.e., a strict majority of entries are genuinely unwritten)."
- **Setup.** Each admitted catalog entry (support ≥ 3 threads) is checked for expressibility as an existing rule in ruff, pylint, or import-linter's rule inventories.
- **Sample-size rationale.** Applied to the full admitted catalog (all supp≥3 entries), not a sub-sample — expressibility is a deterministic per-entry check, not one requiring statistical sampling.
- **Statistical test.** None (deterministic rate computation); reported with the linter-expressibility rate as a point estimate.
- **Expected outcome.** Fewer than half of admitted entries are expressible in any of the three checked tools (linter-expressibility rate < 0.50).
- **Metrics.** Linter-expressibility rate = $\frac{1}{|K|}\sum_k \mathbb{1}[\text{lintmap}(k)\ne\varnothing]$.

### RQ4 — Does the compliance judge agree with blind human annotation closely enough to trust at scale?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 RQ2 judge-validity component, pipeline.md `rq_judge_validity`):** "The compliance judge reaches agreement of κ ≥ 0.6 with blind dual-human annotation on a 400 (patch, rule)-pair sample."
- **Setup.** A sample of 400 (patch, rule) pairs is independently labeled by the automated compliance judge and by two blind human annotators; agreement is computed as Cohen's kappa. This gate is pre-committed to block scaled labeling for RQ5, RQ7, and RQ8 if it fails.
- **Sample-size rationale.** n=400 (patch, rule) pairs is the pre-registered size (paper.md Step 6, digest N8/A4) chosen to estimate kappa with enough precision to distinguish κ≥0.6 from failure at the scale RQ5/RQ7/RQ8 require.
- **Statistical test.** Cohen's kappa (judge vs. human, pooled and per category), with κ ≥ 0.6 as the pre-registered gate threshold.
- **Threshold note (explicit decision, review-revision pass 2026-07-05).** The Phase A method-rigor audit (stage_review.md item 6, advisory) noted that the guidance recipe's instrument-validation bar is κ ≥ 0.7 while this gate pre-registers κ ≥ 0.6. Decision: κ ≥ 0.6 is retained — it falls in the Landis–Koch "substantial agreement" band and is the pre-registered value used consistently across `digest.md`, `paper.md`, the Stage 6 hypotheses, and `paper_draft.md/.tex`; raising it post-registration would break byte-identical hypothesis traceability. Recorded here as an explicit decision, not a silent default.
- **Expected outcome.** Judge-versus-human agreement reaches κ ≥ 0.6.
- **Metrics.** Cohen's kappa (pooled and per category).

### RQ5 — Do test-passing patches nonetheless carry validated constraint violations?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 RQ2 orthogonality component, pipeline.md `rq_orthogonality`):** "Among held-out test-passing patches, the validated judge confirms a nonzero rate of catalog-rule violations — demonstrating that passing every test carries no information about mined-constraint compliance."
- **Setup.** With judge validity established (RQ4), the validated judge is applied to a sample of held-out test-passing patches, and the rate of confirmed violations (judge output corroborated by human spot-check) is measured.
- **Sample-size rationale.** Drawn from the ~500 test-passing SWE-bench-Verified agent patches (paper.md Step 6 datasets) with human spot-check confirmation sized to the walking-skeleton confirmation protocol (Step 9: ~20 flagged violations confirmed).
- **Statistical test.** 95% CI on the confirmed violation rate; refuted if statistically indistinguishable from zero.
- **Expected outcome.** A nonzero rate of confirmed violations is found among test-passing patches.
- **Metrics.** Confirmed violation rate among test-passing patches, with 95% CI.

### RQ6 — Is category assignment reliable enough to support a category-wise comparison?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 / pipeline.md `rq_category_reliability`):** "Dual-annotator category labeling reaches a pre-registered Cohen's kappa threshold, with residual disagreement concentrated in entries routed to 'other' rather than spread uniformly across the three named categories."
- **Setup.** Two annotators independently assign a category (or "other") to every catalog entry; disagreements are adjudicated and Cohen's kappa is computed, together with the distribution of adjudicated "other" assignments.
- **Sample-size rationale.** Applied to the full admitted catalog per pilot repository (not sub-sampled), since category reliability must be established over the same entries the category-wise comparison (RQ7) will later use.
- **Statistical test.** Cohen's kappa against the pre-registered threshold; qualitative check that disagreement concentrates in "other" rather than spreading uniformly across the three named categories.
- **Expected outcome.** Category labeling reaches the pre-registered kappa threshold, with disagreement concentrated in "other."
- **Metrics.** Cohen's kappa (category assignment); fraction of entries adjudicated to "other."

### RQ7 — Is the category-wise violation distribution uniform or skewed?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 RQ2(i)+(ii), pipeline.md `rq_category_distribution`):** "The category-wise violation distribution is non-uniform (chi-square goodness-of-fit p<0.05) with Cramér's V ≥ 0.15 as the effect floor (significance alone does not satisfy (i)), with error-handling and architectural-convention violation rates exceeding the API-convention rate."
- **Setup.** Category-wise violation rates are computed across all tested test-passing patches and compared for uniformity via a chi-square goodness-of-fit test, α = 0.05, with a per-repository stratified sensitivity check since patches are not independent within a repository. Patches are stratified by repository × category × arm; any repository × category cell with fewer than 20 test-passing patches is pre-declared **inconclusive** for that stratum and excluded from the per-repo sensitivity table rather than silently pooled into a null. The pooled (non-stratified) test is the primary analysis only if at least 4 of the 5 pilot repositories clear the n ≥ 20-per-category threshold; otherwise the claim narrows to the repositories that clear it.
- **Sample-size rationale.** Drawn from the ~500 test-passing agent patches plus matched gold patches (paper.md Step 6 datasets); the n≥20-per-cell rule is the pre-registered power/thin-cell threshold (paper.md Step 6, guidance.md Part 6 item 9) protecting against a pooled test being dominated by one sparse repository×category cell.
- **Statistical test.** Chi-square goodness-of-fit, α = 0.05, with Cramér's V ≥ 0.15 as a co-required effect floor.
- **Expected outcome.** The distribution is non-uniform, with EH and ARCH violation rates each exceeding API's.
- **Metrics.** Per-category violation rate with Wilson 95% CI; chi-square statistic and p-value; Cramér's V.

### RQ8 — Do test-passing agent patches violate mined constraints more often than matched human gold patches?

- **Tier:** Mechanism.
- **Target hypothesis (verbatim, paper.md Step 6 RQ2(iii), pipeline.md `rq_agent_vs_human_gap`):** "Test-passing agent patches violate mined constraints at a higher rate than matched human gold patches in at least one category (McNemar p<0.05, Holm-Bonferroni corrected across the three categories), by at least 8 percentage points (matched-pair rate difference) in every category where (iii) is claimed to hold (the effect floor; a significant-but-<8-point gap is reported as 'detected but small,' not as satisfying (iii))."
- **Setup.** Category-wise violation rates for agent patches and their matched human gold patches are compared via a matched-pair McNemar's test per category, Holm-Bonferroni corrected across the three categories, α = 0.05. **Mechanism analysis (secondary, non-gating):** validated violations are additionally cross-tabulated against (a) agent-system identity — checking whether any excess concentrates in specific agent systems rather than spreading uniformly across the ≥3 systems sampled — and (b) patch size/files touched — checking whether violation likelihood scales with patch size, which would point to an exposure-opportunity confound rather than a genuine per-patch compliance gap.
- **Sample-size rationale.** Same ~500-patch matched-pair dataset as RQ7, subject to the same n≥20-per-repo×category-cell rule; B0 (matched human gold) is evaluated as the reference distribution before any hypothesis is scored (A5).
- **Statistical test.** Matched-pair McNemar's test per category, Holm-Bonferroni correction across 3 categories, α = 0.05, with an 8-percentage-point matched-pair gap as a co-required effect floor per category where the hypothesis is claimed to hold.
- **Expected outcome.** Agent violation rate exceeds the matched human-gold rate by at least 8 points in at least one category after correction.
- **Metrics.** Per-category agent-vs-human-gold matched-pair delta; McNemar statistic and Holm-Bonferroni-corrected p-value per category.

---

## Global fallback F-G1

If the central hypothesis family fails (extraction precision cannot clear 0.5 even after the pilot-gate prompt revision, OR judge validity κ<0.6 blocks all automated measurement), the study pivots archetype from *measurement* to *negative-result / methodological*: "We show that implicit design constraints in PR review history resist reliable automated extraction/judging at current LLM capability, quantify exactly where the pipeline breaks (candidate identification vs. deduplication vs. judging), and release the human-annotated corpus and failure taxonomy as the contribution." (paper.md Step 6.)
