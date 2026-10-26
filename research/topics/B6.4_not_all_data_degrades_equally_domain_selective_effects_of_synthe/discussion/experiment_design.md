# Experiment Design — B6.4: Domain-Selective Effects of Synthetic Contamination

> Standalone protocol document rendered from Stage 6's confirmed output (`pipeline.md`, "Stage 6 — Experiment Design") and `paper.md`'s Step 6 (Pre-Registered Experiments). This is the document to execute from directly — it should not require opening `paper_draft.md`. Keep synchronized with `paper_draft.md`'s Experiments section (same RQs, same setups, same expected outcomes) per `references/paper_assembly.md`'s synchronization rule; if either changes, update both.

**Study type:** `empirical` (a controlled measurement, not a new-system contribution). **Tier accounting** (checked against `study_type=empirical` per Stage 6): **5 mechanism-tier RQs**, one per Stage 5 hypothesis, verbatim target hypotheses; **0 framing-tier RQs** (no Stage 3 limitation was flagged `verify_as_hypothesis`); **0 outcome-tier RQs** (`study_type=empirical` forbids "our procedure beats baseline X" framing — the two candidate baselines from Stage 3 are demoted to sanity-check, mitigation-characterization arms, never competitors).

---

## Datasets

Four domain-partitioned continued-pretraining shards, held byte-identical across all cells except the one manipulated cell (Stage 1 `constraints`):

| Domain | Shard | Justification |
|---|---|---|
| Code | The Stack (permissive-license Python/Java subset) | Public, license-clean, large enough for the token budgets in the staged plan; links to an execution-based capability metric (HumanEval pass rate). |
| Mathematics | OpenWebMath | Public math text at the needed scale; natural link to GSM8K-style exact-match evaluation. |
| Prose | FineWeb-Edu | Public, high-quality prose at scale; natural link to LAMBADA/WikiText evaluation. |
| Dialogue | OASST1 + UltraChat | Public multi-turn dialogue data at the needed scale; natural link to MT-Bench evaluation. **Contingent on a pre-registered audit**: since UltraChat is itself LLM-generated, a synthetic-text classifier is passed over the pooled shard before any contamination run to estimate its existing synthetic base rate. If that rate exceeds 20%, UltraChat is dropped in favor of OASST1 plus a human-only forum corpus, as a pre-committed design amendment (not a post-hoc fix), before the dialogue domain enters the ratio sweep. This guards `RQ1`/`RQ2` against a ceiling-effect confound that would otherwise make dialogue look artificially tolerant. |

## Baselines (sanity-check comparators, not outcome-tier competitors)

This is a measurement study — no research question is framed as "our procedure beats baseline X."

- **Clean control** (0% contamination, shared across domains per seed) — necessary reference for every contaminated cell.
- **Global-uniform contamination arm** — the same total synthetic-token budget spread proportionally across all four shards. The "why do this at all" control: if concentrated single-domain injection is statistically indistinguishable from proportionally-spread injection (bootstrap 95% CI of the difference includes 0 in all domains), the domain axis adds nothing and the problem this paper studies does not exist.
- **Degeneracy-matched real-text arm** and **second-generator arm** — used directly by RQ5 and RQ4 respectively (see below).
- **Mitigation-characterization arms (optional, sanity-check only)** — an entropy-maximizing selection heuristic (EntropyCollapse-style) and an importance-weighted synthetic-training heuristic (SynthWeighting-style). Per Stage 3's refiner pass, these are explicitly *not* baselines in the beat-a-number sense; they characterize how much of any measured damage an existing generic mitigation already recovers, without any RQ claiming this paper's protocol "beats" either.

## Sample size and compute budget (shared across RQs, from `paper.md` Step 6 design constants)

- **Walking skeleton (feasibility gate, run before committing to the full design):** 3 arms — clean control, code@100%, prose@100% — 1 seed each, 1.1B model, 0.5B-token continued pretraining, one generator; deterministic metrics only (execution-based pass rate, last-word accuracy, held-out validation loss — no LLM judge). Expected cost ≈ 20–25 A100-hours (≈1 day on a 4-GPU node). If no domain shows a measurable, domain-localized delta at full contamination, the full grid is not run.
- **Pilot grid:** 4 domains × r ∈ {25%, 100%} + shared clean control, 3 seeds → 27 runs, 1.1B model, 0.5B tokens per run. 3 seeds per cell sets the pooled-seed SD used to calibrate effect-size floors against the walking skeleton's own detectability criterion (2× pooled seed SD).
- **Full grid (Stage 2):** r ∈ {0, 10, 25, 50, 100}%, second generator, base (1.1B) scale.
- **Scale-up:** 3B-scale replication at the two extreme ratios only, r ∈ {0, 100}% — per Stage 5's `m_staged_dose_response_and_scale_check` rationale: "the actionable claim only requires the ranking, not the exact magnitudes, to transfer across scale — concentrating scarce large-scale compute on the two most informative ratio extremes is sufficient to test that one claim."
- **Statistical defaults throughout:** α = 0.05, Holm–Bonferroni correction over the 4 domain-matched primary metrics; bootstrap = 10,000 resamples over seeds × evaluation items.

---

## RQ1 — Is contamination damage domain-selective at all?

- **Tier:** Mechanism
- **Target hypothesis (verbatim, Stage 5/Stage 6 `rq_domain_selectivity_interaction`):** "The domain × ratio interaction term in the dual-normalized mixed-effects model is significant at Holm-corrected α = 0.05."
- **Setup:** Fit the dual-normalized mixed-effects model (`normalized delta ~ domain × ratio + (1 | seed)`) on the pilot and scale-up grids; test the domain × ratio interaction term via a likelihood-ratio test against a no-interaction model, Holm-corrected across the four domain-matched primary metrics, α = 0.05. `paper.md`'s fuller H1 specification additionally requires this significance test to co-occur with (a) ≥1 pairwise slope difference `β_d − β_d′` whose bootstrap 95% CI excludes 0, and (b) a native-unit effect-size floor of ≥0.10 (≥10 percentage points of normalized capability delta at r=100%, matching the walking skeleton's own detectability threshold of 2× pooled seed SD) — significance alone does not pass without the magnitude floor.
- **Sample-size rationale:** Full pilot grid (27 runs, 3 seeds/cell) plus the Stage-2 full ratio grid (r ∈ {0,10,25,50,100}%); 3 seeds per cell is what sets the pooled-seed SD used to calibrate the 0.10 effect floor against the walking skeleton's pass criterion (iv).
- **Statistical test:** Likelihood-ratio test (full vs. no-interaction mixed-effects model), Holm-corrected across 4 domain-matched primary metrics, α = 0.05; pairwise slope-difference contrasts via 10,000-resample bootstrap CIs over seeds × eval items.
- **Expected outcome:** The interaction term is significant, indicating that damage is not a domain-uniform tax. **Falsification:** if non-significant after Holm correction, the reportable finding reframes to: within the tested regime, synthetic contamination behaves as a domain-uniform capability tax, bounding every cross-domain slope difference below the observed upper confidence limit (Fallback FB1) — a result that would simplify, not complicate, existing global-mixing-ratio theory.
- **Metrics:** Interaction-term likelihood-ratio statistic and Holm-corrected p-value; per-domain slopes β_d and their pairwise bootstrap confidence intervals.

## RQ2 — Is the domain ordering consistent with correctness strictness?

- **Tier:** Mechanism
- **Target hypothesis (verbatim, Stage 5/Stage 6 `rq_strictness_directional_ranking`):** "The pre-registered contrast (mean slope of code and mathematics) − (mean slope of prose and dialogue) is positive with a one-sided bootstrap 95% CI excluding zero, and the same sign holds under both the benchmark-metric and validation-loss normalizations."
- **Setup:** Conditional on RQ1, test the pre-registered contrast (mean slope of code and mathematics) minus (mean slope of prose and dialogue) via a one-sided bootstrap 95% confidence interval, checked independently under the benchmark-metric and validation-loss normalizations. `paper.md`'s H2 additionally requires the contrast's point estimate to clear an effect floor of ≥0.05 (≥5 percentage points of Δ per unit ratio) under both normalizations.
- **Sample-size rationale:** Same pilot + full grid as RQ1 (27-run pilot, 3 seeds/cell); dual normalization (benchmark-metric and validation-loss) is computed on the same runs, not a separate sample.
- **Statistical test:** One-sided bootstrap test (10,000 resamples) of the strict-vs-tolerant slope contrast; dual-normalization concordance check (same sign required under both).
- **Expected outcome:** The contrast is positive and its CI excludes zero under both normalizations, indicating domains with mechanically verifiable correctness structure are more fragile to contamination. **Falsification:** if the CI includes zero under either normalization, or the sign is negative, the correctness-strictness account of *which* domains are more fragile is wrong even if RQ1's domain-selectivity finding still holds (Fallback FB2) — the paper then reports the observed ranking with CIs as an open empirical finding without the strictness explanation.
- **Metrics:** Sign and 95% bootstrap confidence interval of the strict-versus-tolerant slope contrast under both normalizations.

## RQ3 — Does dose-response scale sensibly, and does the ranking transfer across model scale?

- **Tier:** Mechanism
- **Target hypothesis (verbatim, Stage 5/Stage 6 `rq_dose_response_scale_stability`):** "Within each domain, the normalized capability delta is non-decreasing in contamination ratio (Spearman ρ ≥ 0) in at least three of four domains, and the ranking of per-domain slopes computed at the two tested model scales agrees at Kendall's τ ≥ 0.66."
- **Setup:** Fit per-domain OLS slopes and quadratic terms across the full ratio grid at base (1.1B) scale; replicate the two most extreme ratios (0%, 100%) at a second, larger (3B) model scale; compare the domain rankings at the two scales via Kendall's τ. Per `paper.md`'s H3, this decomposes into: (i) β_d > 0 with 95% CI excluding 0 **and** β_d ≥ effect floor 0.05 in ≥3 of 4 domains; (ii) per-domain quadratic-term LRT, reported descriptively (either linear or threshold-shaped dose-response is informative, not itself gating); (iii) 1.1B-scale and 3B extreme-ratio rankings agree at Kendall's τ ≥ 0.66. H3 is scored PASS iff (i) **and** (iii) both hold.
- **Sample-size rationale:** Full ratio grid (r ∈ {0,10,25,50,100}%) at 1.1B scale, 3 seeds/cell, for the dose-response fit; 3B-scale replication restricted to the two extreme ratios only (compute-conservation rationale above) — this is the deliberate design choice that makes the 3B leg affordable while still answering the one claim (rank-transfer, not magnitude-transfer) that matters.
- **Statistical test:** Per-domain OLS regression plus likelihood-ratio test (linear vs. quadratic dose-response); Kendall's τ on the r=100% domain orderings at both scales.
- **Expected outcome:** Normalized delta is non-decreasing in ratio in ≥3 of 4 domains, and the domain ranking agrees across scales at Kendall's τ ≥ 0.66 (at most one adjacent transposition among four domains). **Falsification:** if dose-response is flat or non-monotonic in a way that breaks the ranking's ordering, or cross-scale τ falls below 0.66, the ranking is reported as **scale-conditional** (Fallback FB3) — it holds at the smaller tested scale but reorders at the larger one, meaning curation priorities from small-scale proxy studies would not transfer.
- **Metrics:** Per-domain slope and quadratic-term estimates; cross-scale Kendall's τ on the extreme-ratio ranking.

## RQ4 — Does the ranking replicate under a second, independently-sourced contamination generator?

- **Tier:** Mechanism
- **Target hypothesis (verbatim, Stage 5/Stage 6 `rq_generator_robustness`):** "The per-domain slope ranking obtained under the two independently-sourced contamination generators agrees at Kendall's τ ≥ 0.66 (at most one adjacent transposition among the four domains)."
- **Setup:** Repeat the full single-domain contamination sweep with a second generator from a different model family and quality tier, holding the injection protocol fixed; compute Kendall's τ between the two generators' resulting per-domain slope rankings.
- **Sample-size rationale:** Second-generator sweep uses the same full grid and seed count as the primary generator's Stage-2 grid, so the two generator-wise rankings are computed from matched-size samples; τ is computed on 4 items (domains) per generator, with a bootstrap CI over seeds × evaluation items to characterize its sampling uncertainty at that small item count.
- **Statistical test:** Exact Kendall's τ on 4 ranked items; bootstrap confidence interval on τ over seeds × items reported alongside.
- **Expected outcome:** τ between the two generators' rankings is ≥ 0.66. **Falsification:** if τ falls below 0.66, per-domain contamination vulnerability is reported as **generator-conditional** (Fallback FB4) — rankings from any single generator are unreliable on their own, making cross-generator replication a mandatory protocol step rather than an optional robustness check, and the measurement protocol itself (rather than any specific ranking) becomes the paper's most defensible contribution.
- **Metrics:** Kendall's τ between generator-wise rankings, with bootstrap confidence interval over seeds and evaluation items.

## RQ5 — Does damage in the synthetic arm exceed a degeneracy-matched real-text control?

- **Tier:** Mechanism
- **Target hypothesis (verbatim, Stage 5/Stage 6 `rq_syntheticness_vs_degeneracy`):** "At full contamination, the synthetic arm's capability damage significantly exceeds the degeneracy-matched real-text arm's damage in at least half of the tested domains, including the single most vulnerable domain identified by the cross-domain ranking, one-sided bootstrap p < 0.05 after Holm correction."
- **Setup:** At full (100%) contamination, compare the synthetic arm's capability damage against the degeneracy-matched real-text arm (real documents subsampled to match the synthetic arm's measured repetition and type-token-ratio profile at equal token replacement) via a paired one-sided bootstrap test per domain, Holm-corrected across the four domains. `paper.md`'s H5 additionally requires the point estimate to clear an effect floor of ≥0.03 (≥3 percentage points of normalized capability delta beyond the degeneracy-matched control) in ≥2 of 4 domains, including the top-ranked domain from RQ2. This is a **partial, not total, identification**: the matched arm equates *measured* surface degeneracy between arms, so it cannot rule out latent, unmeasured quality defects as a residual confound with syntheticness.
- **Sample-size rationale:** Degeneracy-matched arm run at r=100% only (the ratio at which the syntheticness-vs-degeneracy contrast is sharpest), same 3-seed structure as the primary contaminated cells, across all four domains, Holm-corrected for the resulting 4 comparisons.
- **Statistical test:** Paired one-sided bootstrap test per domain (10,000 resamples), Holm-corrected across the four domains.
- **Expected outcome:** The synthetic arm shows significantly more damage than the degeneracy-matched arm in ≥half of the tested domains, including the single most vulnerable domain from RQ2. **Falsification:** if the degeneracy-matched arm degrades as much as the synthetic arm across the tested domains, contamination damage in this regime is explained by **surface degeneracy rather than syntheticness specifically** (Fallback FB5) — a budget-relevant result in its own right, since cheap degeneracy detectors would then recover most of the protection expensive synthetic-text classifiers would otherwise provide.
- **Metrics:** Paired one-sided bootstrap p-values per domain (Holm-corrected); effect size of the synthetic-versus-degeneracy-matched contrast.

---

## Mechanism check (non-gating, explanatory — not a sixth RQ)

Per `paper.md`'s M7 and Stage 6's tier accounting (exactly 5 mechanism-tier RQs, none manufactured beyond the five Stage 5 hypotheses), this analysis is explanatory support for RQ1/RQ2, not a sixth pass/fail gate.

- **Setup:** For the code and mathematics shards, execute each injected synthetic document's associated tests (or a reference solution's tests, where available) and record the fraction verifiably incorrect despite passing surface fluency; for mathematics, resolve each synthetic worked solution's final answer against a symbolic/numeric checker. Prose and dialogue have no analogous mechanical checker by construction and are recorded as "not computable," not assumed null.
- **Statistical test:** Spearman ρ between per-domain verifiable-error rate (where computable) and the fitted slopes β_d across seeds and ratios, reported descriptively — not aggregated into the RQ1/RQ2 Holm correction.
- **Expected outcome:** Verifiable-error rate correlates positively with β_d. A null or negative correlation would not overturn RQ1/RQ2 if those pass on their own pre-registered criteria, but would flag that the correctness-strictness *mechanism* account is unsupported even where the *ranking* holds — the two are recorded as separable findings.
- **Metrics:** Spearman ρ (per-domain verifiable-error rate vs. β_d); fraction verifiably incorrect per domain.

---

## Global fallback (if the central hypothesis family fails)

If RQ1 fails (H1 false) or the walking skeleton's pass criterion is not met: pivot from an *empirical ranking* study to an *empirical bound + protocol artifact* study. Pre-committed pivoted framing (`paper.md` fallback F-G1): "Using a token-accounted single-domain contamination protocol with degeneracy-matched and cross-generator controls, we show that synthetic contamination up to 100% of any single domain shard acts as a domain-uniform capability tax at the 1–3B scale — bounding cross-domain vulnerability differences below δ* and licensing domain-agnostic filtering thresholds."
