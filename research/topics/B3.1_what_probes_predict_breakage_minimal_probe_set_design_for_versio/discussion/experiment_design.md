# Experiment Design — B3.1: What Probes Predict Breakage?

> Standalone experiment-design spec, per `auto-research-discussion`'s "Final deliverables" item 2. Extracted from `pipeline.md`'s Stage 6 confirmed output (six mechanism-tier RQs, all traced to verbatim Stage 5 hypotheses) and `paper.md`'s Step 6 / Assumptions (A1–A7) numeric design targets, matching `paper_draft.md`'s Experiments section RQ-for-RQ. Nothing below is new content: every number, threshold, and test choice already appears in `pipeline.md` or `paper.md`. **Keep synchronized** — if `paper_draft.md`'s Experiments section is edited, mirror the change here, and vice versa.
>
> **Status.** Pre-registered specification only. No experiments have been run; there are no results to report. All figures below (`|P| ≥ 60`, `δ = 0.03`, `Δ_eq = 0.5 SD`, etc.) are pre-committed design targets, not observed outcomes.
>
> **Tier accounting (`pipeline.md` Stage 6 header, checked against `study_type = empirical`):** all 6 research questions below are **mechanism-tier** (one per Stage 5 hypothesis, verbatim). **Framing-tier: 0** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`. **Outcome-tier: 0** — `study_type = empirical` forbids "our procedure beats baseline X" framing; every baseline below is a sanity-check comparator, never a competitor to beat.

---

## Datasets

| dataset | contents | justification |
|---|---|---|
| **Open-weight version-pair corpus** | Successive checkpoints with immutably archived, redistributable weights (e.g. Llama-2→Llama-3, Qwen1.5→2→2.5, Mistral v0.1→v0.2→v0.3). Forms the corpus **backbone**. | Immutably archived checkpoints satisfy the reachability gate (`sp_retrospective_corpus`, A1) by construction — this stratum cannot itself become unreachable mid-study, so it anchors the corpus against survivorship bias. |
| **Dated closed-API snapshot pairs** | Dated snapshots (e.g. gpt-3.5-turbo-0301/0613/1106, gpt-4-0314/0613, dated Claude snapshots), treated as a secondary best-effort stratum. | Included specifically as the stratum whose reachability is **most at risk** of provider-side deprecation during the study — this is the precise condition RQ4 (`rq_corpus_attrition_bias`) tests, so the corpus needs real at-risk pairs, not only immutable ones, or RQ4 would have nothing to test against (Stage 6 refiner-pass fix). |
| **Probe item banks (one per family, ~100 items/family at pilot, ~1,500 total at scale)** | Capability: MMLU/GSM8K/BBH. Refusal-boundary: XSTest/OR-Bench. Format-preference: IFEval + a JSON-schema-compliance set. Calibration: MMLU-with-confidence / a semantic-calibration set. Safety-behavior: HarmBench/Sorry-Bench/OffTopicEval-style items. | Each item set is grounded in the specific related-work instrument it repurposes as a probe (`rw_refusalindex`, `rw_bcalibration`, `rw_offtopiceval`, `rw_prosafeprune`), so the battery is not an invented ad hoc set. |
| **Downstream-task suite (~20 real tasks at scale; 5 at pilot)** | Extraction-to-JSON, classification, RAG-answer, tool-call argument filling, moderation. | Spans tasks with different sensitivities (format-, calibration-, safety-sensitive) so that RQ3's (`rq_downstream_heterogeneity`) task-heterogeneity claim is actually testable rather than assumed — a homogeneous task suite could not distinguish the hypothesis from its null. |

**Unit of analysis and target n (`paper.md` Step 5 Notation, N8 analysis plan).** Cell = (pair `p`, task `t`). Target at scale: ≈20 pairs × ≈20 tasks ≈ 400 cells; pilot: ≈4 pairs × ≈10 tasks ≈ 40 cells. The corpus's actual power-driven target is `|P| ≥ 60` pairs (see Sample-size and power policy below) — larger than the N8 illustrative ≈20, corrected by the A6 power analysis.

## Baselines and placebo

**Baselines are sanity-check comparators, never outcome-tier competitors** — no RQ below is framed as "our procedure beats baseline X" (`study_type = empirical` forbids it).

- **Single-probe-family predictors** (each of the 5 families' drift alone) — the necessary comparator for any claim about which family dominates once all five are considered jointly (RQ1).
- **B0 — no-signal performance floor.** A constant base-rate breakage predictor using no probe features at all (predicts `E[B̄]`). This is a **floor to beat**, not a placebo — it cannot come out non-null by pipeline artifact. If the full battery (and every subset) fails to beat B0's AUC/Brier at α=0.05, no probe carries usable signal and the study's basic premise fails (routes to the global fallback F-G1 in `paper.md`).
- **B-alt — family-agnostic total-drift scalar.** Raw output-diff magnitude on the entire probe bank, ignoring family structure, at the same query budget as the five-family battery. Kills the rival explanation "probe drift predicts breakage only because both track how big the update was" — RQ1/axis-selectivity only means what it claims if the family-structured predictor beats this scalar.
- **EssenceBench-style item-subset compression baseline**, scoped to the capability family only (`rw_essencebench`, Stage 3's sharpened role — its own reported reconstruction-fidelity numbers are not compared against; only its subset-selection framing is borrowed as a within-family comparison arm).
- **Random/uniform drift-score baseline** — anchors the lower end of the comparison.
- **P0 — null-by-construction placebo, checked BEFORE any research question below is scored.** The family-drift feature vector `D(p)` and the breakage target `B̄(p)` are randomly permuted **across pairs** (destroying the pair-level correspondence while preserving both marginals), then the identical predictor and grouped-CV pipeline used for RQ1/RQ2 is re-fit on the shuffled data. Its predictive power must be null by construction: each family's shuffled coefficient CI must include 0, and the shuffled AUC's 95% CI must include 0.5, over ≥1,000 shuffles. **A non-null P0 = the pipeline measures an artifact (e.g. a CV grouping leak, or a per-pair nuisance like prompt length or decode temperature shared by `D` and `B̄`) = the run is invalid** — diagnose and re-run from the walking skeleton; never score any RQ "to see."

## Metrics (battery-wide)

Standardized regression coefficients and their bootstrap 95% CIs; partial correlations and variance-inflation factors (VIF); the ratio of cross-version drift to the within-version noise floor; Kendall rank correlation of the family ranking across paraphrase sets (**minimum** pairwise value across all paraphrase-set comparisons, not the mean); cross-validated AUC for the subset-ablation criterion; and a TOST equivalence-test statistic comparing drift magnitude between retained and attrited pairs against a ±0.5 SD margin.

## Sample-size and power policy (`paper.md` A6, shared across RQ1/RQ2/RQ5)

The central tests (RQ1, RQ2, RQ5) operate at the **pair level**, not the cell level — effective `n = |P|`, the number of version pairs, since all ≈400 (pair, task) cells collapse into one `B̄(p)` per pair before the joint regression, so cells within a pair are not independent replicates. By Fisher-z at two-sided α=0.05, power to detect a true `ρ = 0.30` (the RQ1 effect floor) is ≈0.25 at `|P|=20`, ≈0.47 at `|P|=40`, ≈0.65 at `|P|=60`, reaching 0.80 only at `|P|≈85`; the confirmatory paired-bootstrap test on `π_top − π_cap` (Holm-corrected across 10 family pairs) needs more pairs still. **Pre-committed policy:** at `|P| < 40`, RQ1 is **exploratory** (point estimates + CIs, no confirmatory verdict); at `40 ≤ |P| < 60`, the ranking is pre-declared **inconclusive**, never a fallback-triggering failure; the confirmatory PASS/FAIL verdict is scored only at `|P| ≥ 60` (power ≥0.65). The corpus target is therefore **`|P| ≥ 60`**, reached by adding more archived open-weight successions and dated-API strata (config, not code) — never by shrinking per-pair task coverage.

## Reported robustness checks and cost accounting (not gates; `paper.md` design-review additions, 2026-07-04)

- **Temporal-split forward validation (`paper.md` "Forward-validation robustness check").** The protocol's actual use is prospective ("run the minimal subset once per version bump"), but H1/H2 are estimated in-sample with random-pair grouped CV. Pre-registered robustness: fit the family ranking and `S*` on the chronologically *earlier* pairs, evaluate `AUC(S*)` and the ranking's Kendall τ on the *latest* held-out pairs; report forward `ΔAUC(S*)` and forward rank-stability alongside the in-sample numbers. **Reported robustness axis, not a gate** (with few pairs the temporal fold is thin); a large in-sample-vs-forward gap is disclosed as a limitation on the "run it prospectively" claim, never hidden.
- **Deterministic cost-accounting table (design-review "Missing RQs" item, reporting only — no new RQ, no design change).** Alongside all results, report queries, monetary cost (USD), and wall-clock time per version bump for the selected minimal subset `S*` versus a full downstream re-test, quantifying the audit-overhead saving the minimality argument rests on. Deterministic accounting, not a hypothesis test.
- **Probe-labeler validity (limitation, stated not tested).** The per-family probe instruments borrow cited single-axis constructions, and their judgment-based labels (e.g. "is this output a refusal?") do **not** receive the full R2 inter-rater validation plan reserved for the downstream `B(p,t)` classifier (κ ≥ 0.7, `paper.md` A3). Their label reliability is a stated assumption reported as a limitation, not a certified property — per the design review, left as a limitation to state.

---

## Research Question 1 — Which probe family's drift, if any, is the strongest predictor of downstream breakage once all five are considered jointly?

- **Tier:** mechanism.
- **Cross-reference:** `pipeline.md` Stage 6 `rq_axis_top_family` → `sp_axis_attribution`; formalized in `paper.md` as RQ1/**H1** (top-family half).
- **Target hypothesis (verbatim, Stage 5 `m_axis_ranking_regression`):** "The family with the highest bootstrap-median standardized coefficient in the joint regression will be refusal-boundary or safety-behavior, not capability, with the 95% CI on the top-family-minus-capability coefficient difference strictly above zero." (`paper.md` H1 adds the effect floor `π_top ≥ 0.30`, carried into Expected outcome below.)
- **Setup:** Pilot: 3–5 open-weight version pairs, ~500 probe items across the 5 families, ~10 downstream tasks. Scale-up: `|P| ≥ 60` pairs spanning open-weight and closed-API strata, ~1,500 probe items, ~20 downstream tasks. Joint regression `B̄ ~ Σ_f D_f`, bootstrap resampling (10,000 resamples) over version pairs for each coefficient's CI; pairwise coefficient differences via paired bootstrap.
- **Sample-size rationale:** See "Sample-size and power policy" above — floor is `|P| ≥ 60`, set by the Fisher-z power analysis for detecting `ρ = 0.30`, not chosen for convenience.
- **Statistical test:** Paired bootstrap at α = 0.05, Holm-corrected across the 10 family pairs; standardized coefficients `β_f` from `B̄ ~ Σ_f D_f` with VIF check.
- **Expected outcome:** At `|P| ≥ 60`: the family with the highest bootstrap-median standardized coefficient is refusal-boundary or safety-behavior, not capability, with `π_top ≥ 0.30`, and the 95% CI on the top-family-minus-capability coefficient difference lies strictly above zero. Falsified if capability's coefficient is largest, or if the top-family-over-capability CI includes zero (below `|P|=60`, a miss is inconclusive-for-power, not falsification). **Fallback (`paper.md` RQ1):** if `cap` ranks #1 → "raw-capability drift, not policy/format drift, dominates downstream breakage"; if no family reaches `π ≥ 0.30` → "no single axis is individually predictive; breakage is multivariate," handing the burden to the minimal-subset question (`paper.md` H2/RQ_INF_1, outside this run's 6-RQ scope — see note below).
- **Metrics:** Standardized regression coefficients per family with bootstrap 95% CIs; paired bootstrap difference between the top family and capability.

## Research Question 2 — Does at least one probe family carry statistically distinguishable predictive power at all?

- **Tier:** mechanism.
- **Cross-reference:** `pipeline.md` Stage 6 `rq_axis_top_family`'s companion RQ, `rq_any_family_signal` → `sp_axis_attribution`; embedded in `paper.md`'s H1 as the "any-signal" precondition.
- **Target hypothesis (verbatim, Stage 5 `m_axis_ranking_regression`):** "At least one family's standardized coefficient will have a 95% CI excluding zero — the joint regression will identify at least one family with non-null predictive power, rather than all five being statistically indistinguishable from a no-signal null."
- **Setup:** Same joint-regression fit as RQ1 (one shared instrument, two readouts — the ranking question and the existence-of-signal question); each family's coefficient CI checked individually against zero.
- **Sample-size rationale:** Identical to RQ1 — same fit, same `|P| ≥ 60` corpus, same pair-level effective n.
- **Statistical test:** Per-family coefficient CI vs. zero, Holm-corrected across the 5 families.
- **Expected outcome:** At least one family's coefficient has a 95% CI excluding zero. Falsified if every family's coefficient CI includes zero — which would also predict the B0 comparison shows no probe beating the base rate.
- **Metrics:** Per-family coefficient CIs; count of families excluding zero.

## Research Question 3 — Does downstream breakage vary meaningfully across tasks with different sensitivities, rather than uniformly across the downstream suite?

- **Tier:** mechanism.
- **Cross-reference:** `pipeline.md` Stage 6 `rq_downstream_heterogeneity` → `sp_downstream_breakage_construct`; formalized in `paper.md` as **RQ4/H4**.
- **Target hypothesis (verbatim, Stage 5 `m_downstream_functional_ground_truth`):** "The correlation between per-family drift and per-task breakage will differ meaningfully between at least two tasks with different sensitivities (e.g., a format-sensitive parsing task vs. a calibration-sensitive task), rather than being uniform across the downstream suite — demonstrating breakage is genuinely task-heterogeneous rather than driven by one axis-agnostic factor." (`paper.md` H4 sharpens "meaningfully" to a `≥0.15` absolute-Spearman-ρ floor, carried into Expected outcome below.)
- **Setup:** Per-task breakage `B(p,t)` computed for every (pair, task) cell before pooling; compare per-family drift-to-breakage correlation `ρ_f(t) = Spearman ρ(D_f(p), B(p,t))` across two pre-declared contrasts examined (not searched post hoc): (i) format-sensitive vs. calibration-sensitive task; (ii) safety-sensitive vs. capability-sensitive task.
- **Sample-size rationale:** Drawn from the same `|P|` corpus and the ≈20-task downstream suite (A5); restricted to 2 pre-registered contrasts specifically to avoid a post-hoc search over all task pairs, which would inflate false positives.
- **Statistical test:** Paired bootstrap over `P` (10,000 resamples) for the ρ-difference CI per contrast; Holm correction across the 2 contrasts.
- **Expected outcome:** For at least one of the two pre-declared contrasts, per-task correlations differ by ≥0.15 in absolute Spearman ρ, with the paired-bootstrap 95% CI on the difference excluding zero. Falsified if neither contrast clears the ≥0.15 bar — narrows Claim 4's scope rather than eliminating it (per `paper.md`'s A5 consequence).
- **Metrics:** Per-task drift-to-breakage correlation and its CI; comparison test between task pairs.

## Research Question 4 — Do version pairs lost to corpus attrition during the study differ systematically in drift magnitude from the pairs that remained reachable?

- **Tier:** mechanism.
- **Cross-reference:** `pipeline.md` Stage 6 `rq_corpus_attrition_bias` → `sp_retrospective_corpus`; formalized in `paper.md` as **RQ5/H5**.
- **Target hypothesis (verbatim, Stage 5 `m_corpus_construction_with_attrition_gate`):** "Pairs that include a closed-API snapshot which became unreachable during the study will not differ systematically in mean per-family drift magnitude from pairs that remained fully reachable throughout (two-sample test, α = 0.05) — ruling out systematic corpus-attrition bias in the retained sample." **Design-review refinement (`paper.md` H5, dated 2026-07-04):** the statistical test is reframed from a plain two-sample significance test to a **TOST equivalence test** against a pre-declared `Δ_eq = 0.5 SD` margin, because a non-significant plain test would rubber-stamp "unbiased" from an underpowered comparison rather than real evidence — the hypothesis's substance (no systematic attrition bias) is unchanged; only the test that certifies it changed.
- **Setup:** Track which dated closed-API snapshot pairs become unreachable over the study's duration; for each family, compute the standardized mean difference in `|D_f(p)|` between the attrited subset and the subset that remained reachable throughout.
- **Sample-size rationale:** Opportunistic, not a fixed target — determined by how many closed-API pairs actually become unreachable during the study window (A1). If the attrited stratum has too few pairs to power the TOST, RQ4 is reported **inconclusive** for that family (instrument/power failure, not a substantive null), and every headline ranking is reported both pooled and on the attrition-free open-weight-only subset as a robustness check.
- **Statistical test:** Two-one-sided-test (TOST) equivalence test per family against ±0.5 SD, α=0.05, Holm-corrected across the 5 families.
- **Expected outcome:** Equivalence established (both one-sided tests reject) for all 5 families. Falsified (per family) if the TOST rejects equivalence — that family's retained sample is attrition-biased; the claim narrows to a per-family caveat plus an attrition-free-subset robustness re-derivation, not a global invalidation.
- **Metrics:** Per-family standardized mean difference in `|D_f(p)|` between attrited and retained pairs; TOST statistic against ±0.5 SD, per family.

## Research Question 5 — Does a family's disentangled (partial) contribution to breakage prediction disagree in rank order with its raw correlation, revealing collinearity-driven misattribution?

- **Tier:** mechanism.
- **Cross-reference:** `pipeline.md` Stage 6 `rq_family_collinearity_partial` → `sp_family_collinearity`; formalized in `paper.md` as **RQ6/H6** (also `paper.md`'s R6 mechanism-analysis requirement).
- **Target hypothesis (verbatim, Stage 5 `m_partial_correlation_disentanglement`):** "For at least one of the five families, the raw pairwise correlation and the VIF-checked partial correlation will disagree in relative rank order by at least one position, demonstrating that family collinearity is non-negligible and that reporting raw correlations alone would misattribute predictive power."
- **Setup:** Compute each family's raw pairwise correlation with `B̄(p)` and its VIF-checked partial correlation net of the other four (same joint fit shared with RQ1/RQ2); compare the two rank orderings across all 5 families.
- **Sample-size rationale:** Shares RQ1's `|P| ≥ 60` corpus and joint fit. The VIF/partial-correlation check additionally needs **≥3 families in the design simultaneously** (A4) — the walking skeleton runs only 2 families (`ref`, `cap`) plus `fmt` specifically to pre-exercise this code path before scale-up.
- **Statistical test:** VIF check (must be `< 10` for partials to be trusted); rank comparison is deterministic given the fitted values, but each `β_f`'s bootstrap CI (shared with RQ1) determines whether a rank flip is distinguishable from noise.
- **Expected outcome:** At least one family's raw-correlation rank and partial-correlation rank disagree by ≥1 position. Falsified if raw and partial rankings agree exactly across all 5 families — reportable as "families are empirically near-orthogonal in this corpus," not a failed experiment. If VIF ≫ 10, ranks are not scored PASS/FAIL and attribution is downgraded to bundle-level.
- **Metrics:** Rank-order comparison between raw and partial correlation, per family; VIF values.

## Research Question 6 — Does cross-version drift exceed within-version noise and remain rank-stable across independently reworded paraphrase sets?

- **Tier:** mechanism.
- **Cross-reference:** `pipeline.md` Stage 6 `rq_noise_paraphrase_gate` → `sp_instrument_stability`; formalized in `paper.md` as **RQ_INF_2/H3**.
- **Target hypothesis (verbatim, Stage 5 `m_noise_and_paraphrase_gate`):** "At least 3 of the 5 probe families will show cross-version drift exceeding the within-version noise floor (one-sided permutation test, Holm-corrected across families, α = 0.05), and the resulting family predictive-power ranking will have Kendall τ ≥ 0.70 across at least 3 independent paraphrase sets."
- **Setup:** Estimate a within-version null distribution per family via ≥3 repeated re-decoded queries on the same version; test whether cross-version drift exceeds the 95th percentile of that null. Separately, recompute the full family ranking under ≥3 independently reworded paraphrase sets and compute Kendall τ for every pairwise comparison of paraphrase sets.
- **Sample-size rationale:** Requires ≥3 re-sampled decodings per item (to build the within-version null) and ≥3 independent paraphrase sets per probe item (to test rank-stability) — both are pre-declared minimums, not post-hoc choices; drawn from `paper.md` A2/A7 detection procedures.
- **Statistical test:** One-sided permutation test per family, α=0.05, Holm-corrected across families, for the noise-floor half; Kendall τ, reporting the **minimum** pairwise value across all paraphrase-set comparisons (not the mean, so one unstable pairing cannot be averaged away), for the rank-stability half.
- **Expected outcome:** ≥3 of 5 families show cross-version drift exceeding the within-version noise floor, and the resulting ranking has Kendall τ ≥ 0.70 across paraphrase sets. Falsified if fewer than 3 families clear the noise floor, or τ < 0.70 — either means RQ1/RQ2/RQ5's correlations are partly artifacts of decoding noise or probe-item phrasing. **Gating rule (`paper.md` "Fallback-combination rules"):** if fewer than 3 families survive this gate, RQ1's ranking is downgraded to "instrument-limited: only families {…} carry rank-stable drift" and the minimal-subset claim (H2, outside this run's 6-RQ scope) is suspended.
- **Metrics:** Drift-to-noise-floor ratio per family; Kendall τ of the family ranking across paraphrase sets.

---

## Note on scope: the minimal-subset hypothesis (H2 / RQ_INF_1)

`paper.md`'s own pre-existing Step 6 (predating this run's `pipeline.md` auto-research-discussion pass) also pre-registers **RQ_INF_1/H2** — "the minimal-sufficient family subset `S*` has `|S*| ≤ 2`" — via grouped 5-fold CV subset ablation (`ΔAUC(S*) = AUC(F) − AUC(S*)`, accept iff the 95% CI upper bound on `ΔAUC(S*) < δ = 0.03`). This is **not** one of the 6 RQs above because `pipeline.md`'s Stage 5/6 explicitly scoped itself to validating the *measurement instrument's properties* (noise floor, paraphrase stability, corpus attrition, family collinearity, task heterogeneity, axis attribution) rather than re-deriving `paper.md`'s own pre-existing headline hypotheses (H1/H2/H3) from scratch (see `pipeline.md`, Seed brief and Cross-stage consistency check). H2/RQ_INF_1 remains part of the paper's full pre-registered spec — see `paper.md` Step 6, "RQ_INF_1" — but is intentionally outside this standalone document's 6-RQ scope, which mirrors `pipeline.md` Stage 6's confirmed output and `paper_draft.md`'s Experiments section exactly.
