# Experiment Design — B2.4: Failed or Infeasible? Calibrated Unsolvability Detection

> Standalone protocol document, per `auto-research-discussion`'s "Final deliverables" spec (SKILL.md). This renders Stage 6's confirmed output as something runnable without opening the paper.
>
> **Provenance.** The datasets/baselines list below is Stage 6's confirmed output from `pipeline.md` (§"Stage 6 — Experiment Design", refiner pass). The research-question structure below (RQ_INF_1/H1, RQ1a/H2, RQ1b/H3, RQ_INF_2/H4, five control arms, two global fallbacks) is `paper.md`'s **Step 6 — Pre-Registered Experiments**, which supersedes pipeline.md's original 6-RQ mechanism-tier table: per `pipeline.md`'s own Phase Log ("E/F (prose + LaTeX resync)"), the original Stage 6 table's single `B0`/`B-alt` pair and 6-RQ structure were revised, after a separate adversarial pass (`design_review.md`), into `paper.md`'s current `B0-p`/`B0-a`/`B-alt1`/`B-alt2`/`B-alt3` control arms and 4-RQ structure — and `paper_draft.md`'s Experiments section was resynced to match. Nothing below is invented: every hypothesis, setup number, statistical test, and metric is copied from `paper.md` Step 6 or `paper_draft.md`'s Experiments section (which itself splices `paper.md` verbatim).
> **Tier accounting** (per `pipeline.md` Stage 6, unchanged by the later revision): `study_type = empirical` ⇒ **mechanism-tier only**. Zero framing-tier RQs (no Stage 3 limitation was flagged `verify_as_hypothesis`). Zero outcome-tier RQs (`empirical` forbids "our procedure beats baseline X" framing) — every baseline/control arm below is a sanity-check comparator, never a competitor to beat.

## Datasets

| Dataset | Justification |
|---|---|
| **Spider 1.0** (Yu et al., 2018) | Single-database text-to-SQL scenarios with a closed-form schema-reachability check for the missing-resource mutation; pilot-stage domain, cheapest to build the oracle for. |
| **BFCL v3** (Berkeley Function Calling Leaderboard) | Has an existing irrelevance-detection split, the closest natural precedent for a removed-tool mutation; pilot-stage domain alongside Spider. |
| **BIRD** (Li et al., 2023) | Multi-table schemas with materially more complex reference queries than Spider's; lets `RQ1a`/H2 and `RQ1b`/H3 be tested under schema complexity closer to real deployments, checking that the directional bias and the design-vs-ceiling gap are not artifacts of Spider's comparatively simple single-database setting. (Refined during Stage 6's critic round — the draft justification, "digest lists it as a scale-up source," was rejected for not naming which RQ needs BIRD or why Spider alone wouldn't do.) |
| **τ-bench retail/airline** | Supports deleted-record and policy-contradiction mutations in a stateful, multi-turn tool-agent environment; scale-up domain. |
| **Terminal-Bench** | Supports non-existent-resource mutations in a command-line setting; scale-up domain. |

Domain admission is itself gated: **A6/PG-6** requires each domain to have script-checkable reference solutions, audited once at domain-selection time (before the pilot); a domain failing A6 is excluded from the pre-registered domain set entirely, never down-weighted or substituted ad hoc.

**Per-domain oracle bring-up milestone (scale-up scoping, per `design_review.md` F-7).** The walking skeleton's "scale-up is a config change" criterion is scoped to *within-domain* scaling only (more source tasks, operator instances, backbones, baseline adapters inside an already-admitted domain). Each *new* domain requires its own oracle backend and operator library — real engineering, not configuration — so every scale-up domain (BIRD, τ-bench, Terminal-Bench) must first pass a per-domain oracle bring-up milestone: PG-1, PG-2, and PG-5 cleared at 20-pair scale in that domain before any of its pairs may contribute to a headline table. A domain that has not cleared bring-up contributes nothing, rather than being scaled into on the strength of another domain's gates.

## Baselines — deployed attribution strategies (sanity-check comparators, not competitors to beat)

- **LLM-judge, all-at-once** (per Who&When).
- **LLM-judge, step-by-step** (per Who&When).
- **AgenTracer-style trained tracer**, label space extended to include `unsolvable`.
- **First-party self-report** (protocol adapted from capability self-assessment / KnowCapable).
- **Keyword/terminal-error heuristic** — floor baseline.

These five form the "full attribution battery" that H2/H3 quantify over.

**Baseline-availability pre-commitment (per `design_review.md` F-8).** The AgenTracer-style trained tracer is the one battery member with a reproducibility dependency: its counterfactual-replay supervision pipeline plus `unsolvable`-labeled training data, which may be drawn **only** from the same 30% pair-level held-in calibration split that B-alt1 and the trained leakage-probe reader use (never from the held-out 70% on which any headline number is computed). If the tracer cannot be reproduced within the pre-registered budget, the battery shrinks to 4 baselines with the reason stated in the paper, and every "≥3 of 5" vote rule becomes "≥3 of 4" (the H3 selection correction becomes best-of-4, CI level 1 − 0.05/4); the shrinkage is reported, never silent.

## Pre-registered control arms (mandatory)

Each control arm targets one specific rival explanation, not a number to beat.

- **B0-p — null-by-construction placebo** (checked *first*, before any RQ is scored). Two sham constructions, scored with the identical estimators used for every headline number: (i) **sham pairs** — a semantically inert mutation (rename an unused alias, reorder an environment listing) so both members remain solvable; (ii) **shuffled-label check** — permute oracle labels within domain and recompute every headline estimator. **Pre-committed null criterion:** "sham-pair gap's 95% pair-clustered bootstrap CI contains 0 **and** shuffled-label AUROC's 95% CI contains 0.5, per domain. Non-null ⇒ the pipeline measures an artifact ⇒ the run is invalid; no H1–H4 is scored."
- **B0-a — current-practice arm** (expected non-null; not the placebo gate). The label-space-restricted attributor, which can only emit `{success, agent_failure}`. Expected `FBR ≈ 1.0` on unsolvable members by construction — this is the argument for why the problem exists at all. "If B0-a's `FBR` is *not* near 1.0, the premise that current formulations force agent-blame is wrong and the whole framing is revisited." (Operationalized, per `paper_draft.md`'s control-arms section: "materially below 1.0" = the 95% CI excludes 0.95.)
- **B-alt1 — information-limit rival** (capability/budget-matched). An oracle-supervised trace probe — same backbone/compute as the strongest LLM-judge, but directly trained/calibrated on the oracle label — trained/calibrated on a 30% pair-level split (stratified by domain × operator type) and evaluated only on the held-out 70%. **Pre-committed three-branch rule:** held-out `AUROC < 0.60` ⇒ information-limited, rival wins; `AUROC ≥ 0.65` while deployed attributors stay below 0.65 ⇒ rival ruled out, gap is design-limited; `AUROC ∈ [0.60, 0.65)` or CI straddling both gates ⇒ mechanism verdict pre-declared **INCONCLUSIVE**, neither wording may be spliced.
- **B-alt2 — memorization/contamination rival** (budget-matched). Strongest LLM-judge baseline rerun on a surface-anonymized 20% subset of pairs per domain (schema/tool/entity/file names consistently renamed, semantics unchanged, `O` re-verified after renaming). **Pre-committed interpretation:** "if the anonymized-variant `FBR` shifts by ≥10 pp or unsolvable-score `AUROC` shifts by ≥0.10 (95% CI of the shift excluding 0) for a domain, the memorization rival wins there... No material shift ⇒ rival ruled out for that domain."
- **B-alt3 — base-rate prior-mismatch rival** (budget-matched). Strongest LLM-judge baseline rerun with one added prompt sentence disclosing the 50/50 unsolvability base rate. **Pre-committed downgrade wording:** "if disclosure closes ≥50% of that baseline's FBR−CoR gap... the observed over-blame is substantially a feasibility-prior miscalibration rather than a structural label-space limitation... If the gap survives disclosure, the structural-design reading stands."

## Assumption gates referenced below (PG-1..PG-6, from `paper.md` Assumptions A1–A6)

| Gate | Checks | Consequence if failed |
|---|---|---|
| PG-1 | A1 oracle soundness: 0 successes by strongest agent + bounded exhaustive/tool-search on every `t⁻` | Any succeeding `t⁻` dropped from all H1–H4 scoring immediately |
| PG-2 | A2 no surface leakage: text-only probe `AUROC_txt < 0.60` | Domain's FBR/CoR/AUROC withheld from headline tables until repaired and re-cleared |
| PG-3 | A3 agents genuinely attempt: `t⁺` success rate ∈ [0.15, 0.90] | Cell excluded from headline H1–H3 aggregation, reported separately as a floor/ceiling artifact |
| PG-4 | A4 baseline's label space admits `unsolvable`+confidence (harness schema check, pre-pilot) | Baseline retained only as the B0-a control; excluded from H2/H3 baseline-battery denominator |
| PG-5 | A5 matched-pair integrity: surface-statistics match (α=0.05) + ≥2-rater κ≥0.70 audit on 10% sample | Failing pair removed from the pool before H1–H4 scoring; systematically-failing operator repaired or retired |
| PG-6 | A6 verifier-equipped source exists (domain-selection-time, one-time) | Domain excluded from the pre-registered domain set entirely |

## Research Questions

### RQ_INF_1 (H1) — Does the phenomenon exist at material magnitude?

- **Tier:** mechanism-tier.
- **Target hypothesis (verbatim, `paper.md` Step 6):** "On the Stage-1 pilot (100 pairs, Spider + BFCL v3, 2 agents), the default LLM-judge attributor's `FBR ≥ 0.20` (effect floor) **and** the 95% pair-clustered bootstrap CI lower bound `> 0.05`."
- **Setup:** Stage-1 pilot: 100 pairs (Spider + BFCL v3), 2 agent backbones, the default LLM-judge attributor (all-at-once), untuned threshold. Assumptions checked: A1, A2, A3, A4, A6.
- **Sample-size rationale:** Single pre-registered baseline/pilot quantity, not a family — 100 pairs across the two pilot-stage domains is the Stage-1 scale fixed by the design (no family-wise correction needed since there is only one primary comparison at this stage).
- **Statistical test:** Cluster bootstrap over pairs, 10,000 resamples; report point estimate + 95% CI.
- **Alpha / aggregation:** α = 0.05 (one-sided, via the CI-lower-bound-> 0.05 criterion); no multiple-comparison correction (single primary baseline/pilot quantity — contrast with H2's Holm–Bonferroni across 5 baselines); no aggregation across baselines/domains at this stage (deferred to H2/H3).
- **Expected outcome:** `FBR ≥ 0.20`, with the 95% pair-clustered bootstrap CI lower bound exceeding 0.05.
- **Falsification condition:** If `FBR < 0.20` or CI overlaps 0.05 — retarget headline to "off-the-shelf LLM-judge attribution already separates unsolvable from agent-failure at rate X untuned; the open problem is the residual tail / the harder domains," per-domain/per-baseline reporting.
- **Metrics:** `FBR = P(ŷ=agent_failure | y=unsolvable)`, untuned default threshold, with 95% pair-clustered bootstrap CI.

### RQ1a (H2) — Directional bias: does over-blame persist across the deployed battery?

- **Tier:** mechanism-tier.
- **Target hypothesis (verbatim, `paper.md` Step 6):** "For **≥3 of the 5** attribution baselines, `FBR − CoR ≥ 0.10` (10 pp), Holm–Bonferroni-corrected across the 5 baselines at family-wise α = 0.05, two-proportion cluster-bootstrap test (resample at pair level)."
- **Setup:** Stage-2 run: 600 pairs (150/domain across 4 domains) × 3 agent backbones × the full 5-strategy attribution battery ⇒ ≥1,800 unsolvable decisions/baseline for the FBR class. Assumptions checked: A1–A5.
- **Sample-size rationale:** The CoR class conditions on *failed-solvable* instances only, whose count is agent-competence-dependent: under A3's allowed `t⁺` success range [0.15, 0.90], pooled failed-solvable n per baseline ranges from ≈180 (success = 0.90) to ≈1,530 (success = 0.15). Under a conservative p≈0.5 variance bound, one-sided power for the 10-pp FBR−CoR gap at α=0.05 exceeds 0.9 only when failed-solvable n ≳ 400 (`t⁺` success ≲ 0.78); at the A3 worst case (n≈180) power falls to ≈0.8 uncorrected and lower under Holm. **Pre-declared rule:** any baseline whose realized power for the 10-pp floor is < 0.8 after Holm correction has its H2 verdict pre-declared **INCONCLUSIVE** (never a null) and is excluded from the "≥3 of 5" vote denominator, with the exclusion stated; the same thin-cell rule applies per domain × agent-family × operator-type cell.
- **Statistical test:** Two-proportion cluster-bootstrap test (FBR vs. CoR, resampled at the pair level, 10,000 resamples) per strategy, Holm–Bonferroni corrected across the 5 strategies at family-wise α=0.05. Secondary: logistic regression of misattribution on {domain, operator-type, agent-family} fixed effects, to localize the bias (not itself a headline claim).
- **Expected outcome:** For ≥3 of the 5 (non-inconclusive) attribution strategies, `FBR` exceeds `CoR` by at least 10 percentage points after correction.
- **Falsification condition:** Refuted (bias absent) if fewer than 3 of 5 non-inconclusive strategies show the corrected 10-pp gap. Refuted in the **opposite direction** if ≥3 of 5 instead show `CoR − FBR ≥ 0.10` after correction — reported at full prominence: "attribution systems over-refuse rather than over-blame; the calibration-boundary result (RQ1b) becomes the finding of record with the recommended threshold adjustment reversed in sign."
- **Metrics:** `FBR`, `CoR`, and their difference per strategy, with cluster-bootstrap 95% (or 99% where H3's selection correction applies) CIs; realized power and realized n per strategy and per cell; `CoR` additionally reported stratified by the source task's difficulty tier alongside the pooled rate (removes the confound that FBR/CoR condition on asymmetric populations).

### RQ1b (H3) — Does a usable calibration boundary exist in every domain?

- **Tier:** mechanism-tier.
- **Target hypothesis (verbatim, `paper.md` Step 6):** "For **≥1** baseline in **each** of the ≥4 domains, `AUROC(c, 𝟙[y=unsolvable]) ≥ 0.65` with bootstrap CI lower bound `> 0.50`, and the risk–coverage curve is non-1:1 (AURC strictly below the coverage-proportional diagonal, CI-separated)."
- **Setup:** Same Stage-2 scale-up population as RQ1a (600 pairs, 4 domains, 3 agent backbones, 5-strategy battery).
- **Sample-size rationale:** "At least one baseline per domain" selects the best of 5 baselines within each domain, so per-baseline CIs use the Bonferroni-corrected level `1 − 0.05/5 = 99%` (preserving per-domain α=0.05 under selection); the AURC-vs-diagonal separation test uses the same corrected level. An H3 pass at the uncorrected 95% level that fails at 99% does not count.
- **Statistical test:** Bootstrap CI on AUROC at the 99%-corrected level; AURC-vs-diagonal separation test at the same corrected level. Secondary (pre-committed, resolving the digest N10-t2 promise per `design_review.md` F-11): a held-out-domain threshold-transfer analysis — the operating threshold selected on each set of n−1 domains is applied unchanged to the held-out domain and its realized risk/coverage is reported, with the result stated even if negative; not itself a headline claim and no hypothesis is attached to it.
- **Expected outcome:** For ≥1 strategy in each of the 4 domains, `AUROC ≥ 0.65` with 99%-level CI lower bound `> 0.50`, and AURC strictly below the coverage-proportional diagonal at the corrected level.
- **Falsification condition:** Refuted for a domain if no strategy clears the corrected bar. The spliced conclusion for a failing domain is conditional on B-alt1's three-branch rule, never asserted independently of it.
- **Metrics:** `AUROC` and `AURC` of the confidence score against the oracle label, 10-bin ECE, Unsolvability Refusal Index (Spearman `ρ(c, 𝟙[y=unsolvable])`) — all reported per domain at the corrected confidence level.

### RQ_INF_2 (H4) — Are the constructed pairs leak-free in every domain used for a headline number?

- **Tier:** mechanism-tier (instrument-validity / hard gate — checked before any RQ1a/RQ1b/RQ_INF_1 headline number is reported).
- **Target hypothesis (verbatim, `paper.md` Step 6):** "For **every** domain used in headline results, text-only probe `AUROC_txt < 0.60` after at most one operator-repair iteration, and pair members are not separable on length/token-overlap/perplexity at α=0.05."
- **Setup:** Assumptions checked: A2, A5. Two-reader leakage gate per domain: (i) the strongest attributor-battery backbone prompted text-only, (ii) a trained discriminator fit on the same 30% calibration split used by B-alt1, evaluated on held-out pairs. Both readers must first clear a positive-control power check (`AUROC ≥ 0.90` on deliberately leaky pairs) before their `<0.60` verdict on real pairs counts.
- **Sample-size rationale:** Human audit on a ≥2-independent-rater, κ≥0.70, 10% random sample per domain (shared with PG-5's matched-design-integrity check); the positive-control set size is whatever is needed to establish the 0.90 AUROC power bound before the gate is trusted on real pairs.
- **Statistical test:** Two-sample tests on surface length, token overlap, and instruction perplexity between pair members at α=0.05; inter-rater κ on the human-audit sample.
- **Expected outcome:** Every domain's text-only probe AUROC falls below 0.60 after at most one operator-repair iteration, and pair members are not statistically separable on surface statistics at α=0.05.
- **Falsification condition:** Refuted for a domain if its probe AUROC stays ≥0.60 after one repair iteration, or pair members are separable — that domain's headline rates are withheld and reported as a negative construct-validity finding (global fallback F-G1 applies at the paper level if H1 and H2 both fail; F-G2 applies if **every** domain fails H4).
- **Metrics:** Per-domain text-only probe AUROC (two readers); surface-statistic test p-values; human-audit κ on the 10% sample.

## Global fallbacks

- **F-G1 (archetype pivot).** If H1 fails (no material phenomenon) **and** H2 fails (no directional bias), pivot from measurement/empirical to benchmark/dataset archetype (requires H4 to pass, so the instrument itself is valid). Pivoted abstract: "We release a suite of matched solvable/unsolvable agent-task pairs with mechanically certified ground truth and a passing leakage audit across four domains... today's attribution systems already handle the injected cases, marking the residual hard fraction as the open target."
- **F-G2 (construct-validity pivot).** If H4 fails in **every** domain after the one permitted operator-repair iteration, F-G1 is barred (no valid instrument) and every FBR/CoR/AUROC number is unreportable — pivot to a construct-validity finding about leakage itself, licensed only because the probe passed its R2 positive-control power check. Pre-committed scope: repair budget is exactly one iteration per operator family; leakage prevalence reported per operator family × domain with the same CIs the headline rates would have used.

## Reporting protocol (R7)

No hyperparameter search is performed on the pre-registered thresholds (FBR/CoR floors, AUROC gates, α levels) — frozen before Stage-2 execution. One declared exception: each LLM-judge baseline's *prompt wording* is not search-free — the two established strategies (all-at-once, step-by-step) are each run with ≥3 paraphrased variants, variance across variants is reported, and the best variant per baseline is used for headline comparisons — a declared search over prompt wording only, never over statistical thresholds.
