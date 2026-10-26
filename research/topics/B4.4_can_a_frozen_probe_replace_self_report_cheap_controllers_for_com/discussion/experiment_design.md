# Experiment Design — B4.4: Can a Frozen Probe Replace Self-Report? Cheap Controllers for Compute Allocation

> Standalone protocol document, per the `auto-research-discussion` skill's "Final deliverables" spec (deliverable 2: "stage 6's confirmed output rendered as a *standalone* document... the document the user actually executes from — it should be runnable as a protocol without opening the paper"). Assembled entirely from `pipeline.md`'s Stage 6 confirmed output (Cross-stage consistency check verified every `target_hypotheses` entry is a verbatim match to a Stage 5 hypothesis) and `paper.md`'s own Step 6 / Assumptions / Step 9 content, with setup/expected-outcome/falsification prose reused from the already-reviewed `paper_draft.md` Experiments section where it elaborates the same Stage 6 confirmed output one-to-one. Nothing below is invented beyond those three sources. Status: **specification — no experiments have been run.** All numbers are pre-registered design targets, not results.

**Study type:** empirical (measurement / controlled comparison — no new controller mechanism is proposed; see Stage 1 `study_type`). Per Stage 6's tier accounting: **6 mechanism-tier RQs, 0 framing-tier RQs, 0 outcome-tier RQs** (outcome-tier framing is disallowed under `study_type=empirical`; Random/all-cheap/all-expensive/Oracle below are sanity-check comparators, never competitors to beat).

---

## Datasets

| Dataset | Role | Justification |
|---|---|---|
| **GSM8K** | Stage 1 pilot benchmark | Exact-match numeric answers give programmatic scoring for free; targets `sp_label_free_ground_truth` (`rq_labelcost`) and anchors the H1/H2 budget grid. |
| **MMLU-Pro** | Stage 1 pilot benchmark | 10-option multiple choice; stresses the predictive-entropy training-free variant and gives a second Stage-1 domain for the BH-corrected H1/H2 tests. |
| **MATH-500** | Stage 2 held-out benchmark | Used specifically to test whether the probe's transfer gap (H3 / `rq_transfer`) is bounded, rather than only being observed post hoc on the two fixed Stage-1 corpora. |
| **GPQA-Diamond** | Stage 2 held-out benchmark | Same transfer-test role as MATH-500 — a second held-out domain for `rq_transfer`. |
| **BIG-Bench-Hard** | Stage 2 held-out benchmark | *(Refiner-fixed justification — the draft's original "a generic multi-task reasoning benchmark" was flagged `[major]` and replaced.)* A multi-task suite whose component tasks differ from GSM8K/MMLU-Pro in **task format**, not just topic, letting `rq_transfer` (H3) test whether the probe's transfer gap is driven by topic shift alone or by format shift as well, rather than treating "held-out benchmark" as one undifferentiated condition. |

A second backbone family (Llama-3.1) is evaluated alongside the second/third held-out benchmarks to give `rq_transfer` a cross-backbone transfer condition in addition to the cross-task one.

## Baselines

Sanity-check comparators only — **not** outcome-tier competitors this study is trying to beat (per `study_type=empirical`, no research question here is framed as "our procedure beats baseline X").

| Baseline | Role |
|---|---|
| **B0 — Random router** at matched budget | The necessary "why do this at all" control: if no real controller beats Random on AUCC (paired-bootstrap CI excluding 0), per-query signal is worthless and the whole comparison is void. |
| **All-cheap / all-expensive** fixed policies | Anchor the budget endpoints of every matched-budget curve. |
| **Oracle router** (routes to expensive tier iff cheap tier is wrong) | Anchors the upper bound on matched-budget accuracy. |
| **Logit/predictive-entropy router** (training-free, M1a) | One of the two training-free controllers under test (`rq_trainingfree_sufficiency`). |
| **Self-consistency router**, k=8 (training-free, M1b) | The other training-free controller under test; its own k−1-sample acquisition cost is charged in every comparison. |
| **Verbalized-confidence self-report router** (M3a) | One of the two self-report operationalizations; prompt-tuned on a dev split before evaluation. |
| **P(True)-style self-report router** (M3b, Kadavath et al. 2022 protocol) | The other self-report operationalization. *(Kadavath et al. 2022 is not a beat-a-number baseline — its elicitation protocol is adopted directly as this arm's construction; see Stage 3 refiner note.)* The **stronger** of M3a/M3b on the dev split is reported as the headline self-report baseline everywhere except `rq_selfreport_variant_loadbearing`, which deliberately uses each variant alone. |

---

## Research Questions

All six RQs below are **mechanism-tier**, each matching one Stage 5 hypothesis verbatim (per the Cross-stage consistency check: "every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓").

### RQ1 — `rq_labelcost` (targets `sp_label_free_ground_truth`)

**Target hypothesis (verbatim, Stage 5 `m_recycled_label_pipeline` / Stage 6 table):**
> "A probe trained solely on labels recycled from cached self-consistency samples reaches AUROC > 0.60 against cheap-tier correctness on held-out GSM8K queries — the minimum separability needed for the probe to be a non-trivial routing signal at all."

- **Setup.** Train the probe (logistic-regression head and 2-layer-MLP head) solely on labels recycled from cached k=8 self-consistency samples on a held-out, de-duplicated GSM8K training pool (~5,000 queries); compute AUROC against cheap-tier correctness on a held-out GSM8K dev split. This is also the Step 9 walking-skeleton gate ("Gate A4"): the study does not proceed past the skeleton if this threshold is not met.
- **Sample-size rationale.** ~5,000-query training pool, disjoint and de-duplicated from the evaluation set (Assumption A5); no additional annotation cost beyond what the self-consistency baseline already pays (probe supervision is a byproduct of the k cached cheap-tier samples).
- **Statistical test.** None specified beyond the raw threshold comparison: AUROC is checked directly against the 0.60 cutoff (no CI or significance test is defined for this gate in the confirmed sources — only the point threshold).
- **Expected outcome.** Probe AUROC exceeds 0.60 against cheap-tier correctness — the minimum separability needed for the probe to be a non-trivial routing signal at all.
- **Falsification condition.** Refuted if probe AUROC is at or below 0.60 on the GSM8K dev split, in which case the probe is not a viable controller and RQ2, RQ4–RQ6 cannot be meaningfully run (per Assumption A4's stated consequence: the study stops at the walking skeleton, and only RQ3/H2 — training-free sufficiency — remains answerable).
- **Metrics.** AUROC(probe signal, cheap-tier correctness) on held-out GSM8K queries.

### RQ2 — `rq_probe_vs_selfreport` (targets `sp_cost_commensurability`)

**Target hypothesis (verbatim, Stage 5 `m_dual_cost_metered_router` / Stage 6 table = paper.md Step 6 H1):**
> "On both Stage-1 benchmarks (GSM8K, MMLU-Pro), at all 5 pre-registered budget points, the probe is non-inferior to the strongest self-report variant (McNemar does not reject in self-report's favor, BH-corrected α=0.05) and strictly superior at ≥2 of the 5 points on each benchmark."

*(paper.md's Step 6 carries a Phase-A-revised, more rigorous restatement of this same hypothesis, adding an explicit non-inferiority margin and effect floor: "...non-inferior... AND the paired-bootstrap 95% CI on the accuracy gap does not exclude −1pp in self-report's favor... strictly superior (McNemar rejects in probe's favor, BH α=0.05, AND the paired-bootstrap 95% CI on the accuracy gap excludes 0 with a point estimate ≥1pp — the effect floor below which a 'win' is not counted) at ≥2 of the 5 points on each benchmark." This is the version actually executed below.)*

- **Assumptions.** A1 (scorable ground truth), A2 (offline-simulation exactness), A3 (cost commensurability), A4 (probe has non-trivial signal — gated by RQ1).
- **Setup.** For every tested (benchmark × budget) cell across GSM8K and MMLU-Pro at 5 pre-registered budget points (all-cheap +10%, 25%, 50%, 75%, 90% toward all-expensive), compute matched-budget accuracy for the probe and for the stronger self-report variant using the same cached outputs.
- **Sample-size rationale.** n = 2,000 paired evaluation queries per benchmark, sized for ≈80% power at a ≈3-percentage-point accuracy gap (10 cells = 5 budgets × 2 benchmarks). Any cell whose realized discordant-pair count after routing falls below 30 pairs is pre-declared **INCONCLUSIVE** (never null, never silently dropped) and excluded from both the non-inferiority and superiority tallies.
- **Statistical test.** Paired McNemar test on per-query correctness at each of the 10 budget×benchmark cells, Benjamini–Hochberg corrected across all 10; 10,000× paired-bootstrap 95% CI on the accuracy gap for the non-inferiority margin (must not exclude −1pp in self-report's favor) and the superiority effect floor (must exclude 0 with a point estimate ≥1pp).
- **Expected outcome.** The probe is non-inferior to the strongest self-report variant at all 10 cells, and strictly superior at ≥2 of the 5 budget points on each benchmark (both McNemar- and effect-floor-qualified, as defined above).
- **Falsification condition.** Refuted toward self-report if McNemar rejects in self-report's favor, BH-corrected, at a majority of the 10 cells. **Fallback if refuted:** the claim becomes a cost-crossover characterization — "self-report retains a matched-budget accuracy edge of X percentage points below budget B\*; the probe is the accuracy-per-dollar choice only above B\*" — a reportable frontier result, not a null outcome.
- **Metrics.** Matched-budget accuracy $\text{Acc}_\pi(\tau_\pi(B))$ and its McNemar test statistic per cell; accuracy-per-dollar; area under the cost–accuracy curve (AUCC).

### RQ3 — `rq_trainingfree_sufficiency` (targets `sp_cost_commensurability`)

**Target hypothesis (verbatim, Stage 5 `m_dual_cost_metered_router` / Stage 6 table = paper.md Step 6 H2):**
> "Neither training-free controller (logit/predictive entropy; self-consistency agreement, k=8) is equivalent to the best controller: TOST equivalence within ±2pp fails for each at ≥3 of 5 budget points on both benchmarks, and the probe's matched-budget accuracy exceeds each training-free controller by >2pp (paired-bootstrap 95% CI excluding 0) at ≥3 of 5 points once self-consistency's k−1 extra samples are charged."

- **Assumptions.** A1, A2, A3.
- **Setup.** For logit/predictive entropy and self-consistency agreement (k=8) separately, run a TOST equivalence test (±2 percentage points) against the best controller's matched-budget accuracy at each of the 10 (budget × benchmark) cells; separately test whether the probe's matched-budget accuracy exceeds each training-free controller by more than 2 percentage points once self-consistency's k−1 extra samples are charged.
- **Sample-size rationale.** Same n = 2,000 paired queries/benchmark as RQ2. Cells are pre-declared adequately powered for the ±2pp margin at this n by construction of the margin choice (TOST requires larger n than a difference test for the same margin — RQ2's H1 is therefore the best-powered of the three headline tests). Any cell whose realized discordant-pair count falls below 30 pairs (a sparse threshold sweep near the budget extremes) is pre-declared **INCONCLUSIVE** — neither equivalent nor non-equivalent — and excluded from the ≥3-of-5 tally.
- **Statistical test.** TOST equivalence test (±2pp), BH-corrected across cells; 10,000× paired-bootstrap 95% CI for the >2pp probe-vs-training-free margin.
- **Expected outcome.** Neither training-free controller passes the ±2pp TOST equivalence test against the best controller at ≥3 of 5 budget points on either benchmark, and the probe exceeds each training-free controller by >2pp at ≥3 of 5 points.
- **Falsification condition.** Refuted (training-free signals already suffice) if either training-free controller passes the ±2pp TOST equivalence test against the best controller at a majority of cells. **Fallback if refuted:** "training-free self-consistency already suffices — the probe's marginal value is ≤2pp and does not justify its training pipeline" — a negative-for-probe, positive-for-practice result that still answers the research question.
- **Metrics.** TOST equivalence bound crossing per cell; paired-bootstrap 95% CI on the probe-vs-training-free accuracy gap; matched-budget accuracy, accuracy-per-dollar, and signal AUROC.

### RQ4 — `rq_transfer` (targets `sp_transfer_specificity`)

**Target hypothesis (verbatim, Stage 5 `m_cross_distribution_probe_transfer` / Stage 6 table = paper.md Step 6 H3):**
> "A probe trained on one Stage-1 benchmark, evaluated on ≥2 of 3 held-out benchmarks, retains matched-budget accuracy ≥ the training-free self-consistency router at ≥3 of 5 budget points, with the cross-backbone (Llama-3.1) transfer gap larger than the cross-task transfer gap."

- **Assumptions.** A4 (probe has non-trivial signal — gated by RQ1), A5 (no train/eval leakage).
- **Setup.** Train the probe once on GSM8K's recycled labels; evaluate its unretrained routing quality on at least 2 of 3 held-out benchmarks (MATH-500, GPQA-Diamond, BIG-Bench-Hard) and on a second backbone family (Llama-3.1), comparing matched-budget accuracy against the training-free self-consistency router evaluated under the same held-out conditions.
- **Sample-size rationale.** Reuses the same n = 2,000 held-out benchmark queries as RQ2/RQ3. Any held-out benchmark whose routed-expensive-tier subset (the only queries whose transfer accuracy is informative) falls below n = 200 after matched-budget routing is pre-declared **INCONCLUSIVE** for that benchmark's contribution to the ≥2-of-3 tally — never silently dropped, never scored as a null transfer gap.
- **Statistical test.** Paired-bootstrap 95% CI on the transfer gap $\Delta_{\text{transfer}}$ per held-out benchmark; no post-hoc point selection (full curves reported).
- **Expected outcome.** The probe retains matched-budget accuracy at or above the training-free self-consistency router at ≥3 of 5 budget points on ≥2 of 3 held-out benchmarks, with the cross-backbone (Llama-3.1) transfer gap larger than the cross-task transfer gap.
- **Falsification condition.** Refuted if the probe drops below the training-free self-consistency router's matched-budget accuracy on held-out benchmarks at a majority of budget points. **Fallback if refuted:** the deployable recipe is characterized as per-backbone probe retraining on recycled samples (cost quantified), not a transferable probe.
- **Metrics.** $\Delta_{\text{transfer}} = \text{Acc}_{\text{probe,in-dist}} - \text{Acc}_{\text{probe,held-out}}$; matched-budget accuracy per held-out benchmark/backbone vs. the training-free self-consistency router.

### RQ5 — `rq_selfreport_variant_loadbearing` (targets `sp_selfreport_construct_validity`)

**Target hypothesis (verbatim, Stage 5 `m_dual_selfreport_operationalization` / Stage 6 table):**
> "Reporting only the weaker of the two self-report variants as the baseline would change the H1 non-inferiority/superiority verdict at ≥1 of the 5 pre-registered budget points relative to using the stronger variant — demonstrating that the dual-variant safeguard is load-bearing, not a redundant precaution."

- **Setup.** Recompute RQ2's (H1's) non-inferiority/superiority verdict twice — once using only the verbalized-confidence variant as the self-report baseline, once using only the P(True)-style variant — and compare each single-variant verdict against the dual-variant (stronger-reported) verdict at all 5 pre-registered budget points on both benchmarks.
- **Sample-size rationale.** Reuses RQ2's cached outputs and n = 2,000/benchmark; no new data collection, only a re-scoring of the same cells under alternative baseline choices.
- **Statistical test.** No independent significance test is specified beyond re-running RQ2's own McNemar/bootstrap decision rule under each single-variant substitution and comparing the resulting verdicts cell-by-cell (a verdict-agreement count, not a new inferential test).
- **Expected outcome.** At least one of the two single-variant verdicts differs from the dual-variant verdict at ≥1 of the 5 budget points on at least one benchmark, demonstrating the safeguard is load-bearing.
- **Falsification condition.** Refuted if both single-variant verdicts are identical to the dual-variant verdict at every budget point on both benchmarks — meaning the safeguard changes nothing and the simpler single-variant design would have sufficed.
- **Metrics.** Count and location of (budget × benchmark) cells whose verdict changes between single-variant and dual-variant self-report baselines.

### RQ6 — `rq_decisionquality_isolation` (targets `sp_decision_quality_vs_cost_mechanics`)

**Target hypothesis (verbatim, Stage 5 `m_costfree_decision_quality_isolation` / Stage 6 table):**
> "The probe's AUROC against cheap-tier correctness is not lower than the strongest self-report variant's AUROC; if the probe wins the matched-budget comparison (H1) while its AUROC is lower than self-report's, the win is attributable to signal cost alone, not decision quality, and is reported as such rather than as a decision-quality finding."

- **Setup.** Compute AUROC against cheap-tier correctness for the probe and the stronger self-report variant, with no cost accounting at all, on the same cached outputs used for RQ2; compare the sign of the AUROC gap against the sign of the matched-budget accuracy gap from RQ2 at each budget point. This is the "B-alt" strongest-alternative-explanation control (paper.md's rival-explanation baseline) computed as its own standalone research question.
- **Sample-size rationale.** Reuses the same cached signals and evaluation queries as RQ2 — no separate sample-size target beyond RQ2's n = 2,000/benchmark, since AUROC is computed on the same pool.
- **Statistical test.** No independent significance test specified beyond direct AUROC comparison and sign agreement with the RQ2 matched-budget gap (a directional/mechanistic check, not a hypothesis test with its own CI in the confirmed sources).
- **Expected outcome.** The probe's AUROC is not lower than self-report's AUROC, so any matched-budget advantage found in RQ2 agrees in direction with the budget-independent decision-quality ranking.
- **Falsification condition.** Refuted (mechanical-only win) if the probe wins the RQ2 matched-budget comparison at a given budget point while its AUROC is lower than self-report's at that same point — in which case the win is reported explicitly as an artifact of the probe's lower signal-acquisition cost, not evidence of better decisions.
- **Metrics.** AUROC(probe, cheap-tier correctness) vs. AUROC(self-report, cheap-tier correctness); sign agreement with the RQ2 matched-budget accuracy gap.

---

## Power and thin-cell pre-declaration (applies across RQ2–RQ4)

- **RQ2 (H1):** power ≈ 0.8 for a ~3pp gap at n = 2,000 paired queries/benchmark — the best-powered test, since it uses the full Stage-1 eval set at every budget point.
- **RQ3 (H2):** same n = 2,000/benchmark and TOST ±2pp margin; TOST requires larger n than a difference test for the same margin, so this test's power is lower than RQ2's by construction — cells are pre-declared adequately powered for the ±2pp margin at n = 2,000; any cell with fewer than 30 discordant pairs after routing is pre-declared INCONCLUSIVE and excluded from the ≥3-of-5 tally.
- **RQ4 (H3):** transfer evaluation reuses the same n = 2,000 held-out benchmark queries; any held-out benchmark whose routed-expensive-tier subset falls below n = 200 after matched-budget routing is pre-declared INCONCLUSIVE for that benchmark's contribution to the ≥2-of-3 tally.
- **General rule.** No thin cell (below its stated per-hypothesis floor) is ever reported as a PASS, a FAIL, or a null result — it is reported as INCONCLUSIVE with its realized n.

## Mandatory baselines detail

- **B0 ("why do this at all" control).** Random router at matched budget: if no real controller beats Random on AUCC with paired-bootstrap CI excluding 0, per-query signal is worthless and the whole comparison is void. All-cheap/all-expensive and the Oracle router anchor the endpoints.
- **B-alt (strongest-alternative-explanation control).** The rival explanation this control isolates: "the probe wins matched-budget comparisons only because its signal is cheaper (the budget-accounting mechanic), not because its decisions are better — and/or because self-report was strawmanned." Isolated two ways: (1) the self-report baseline uses both variants (verbalized 0–100, P(True)), prompt-tuned on a dev split, reporting the stronger as headline (= RQ5); (2) a budget-independent AUROC(signal, cheap-tier correctness) comparison that strips all cost accounting (= RQ6).

## Global fallback

If the central hypothesis family (RQ2 ∧ RQ3, i.e. H1 ∧ H2) collapses — the probe neither matches self-report nor beats training-free signals — the archetype pivots from empirical-comparison to instrument/benchmark: the paper's contribution becomes the precompute-then-simulate matched-budget harness itself, with the finding that no controller dominates the accuracy-per-dollar frontier and the ranking is signal-cost- and budget-regime-dependent.

## Walking skeleton (Step 9, minimal closed loop before scale-up)

Answers one binary question: does the probe reach non-inferiority to self-report at even a single matched budget point on one benchmark?

- **Arms (3).** Frozen probe (logistic head, last-layer prefill), strongest self-report (verbalized), Random router (B0).
- **Task set.** GSM8K, 500 eval queries + 1,000 train queries (probe labels recycled from k=8 cheap samples).
- **Backbone pair.** Qwen2.5-7B-Instruct (cheap) vs. Qwen2.5-72B-Instruct or GPT-4o-class (expensive).
- **Metrics (deterministic only).** Matched-budget accuracy at the single B=50% point; AUROC(probe, cheap correctness); realized dollar cost.
- **Gate A4.** Probe AUROC > 0.60 on GSM8K dev, else stop (this is RQ1 run at pilot scale).
- **Skeleton-passed criterion.** Probe matched-budget accuracy ≥ self-report − 1pp at B=50% AND all three arms run through one shared simulator producing a (Cost, Acc) point. Scaling to the full RQ1–RQ6 grid above is then a config change (add benchmarks/backbones/budget points/thresholds to loops), not a code change, since every threshold/budget point is an offline replay over the cache.
