# Experiment Design — B2.2: How Few Replays Suffice? Budget-Bounded Localization of Decisive Failures

> Standalone protocol, executable without opening the paper. Assembled from `pipeline.md`'s Stage 6 confirmed output (`discussion_trace.md`, "Stage 6 — Experiment Design") and `paper.md`'s Step 6 ("Pre-Registered Experiments"), which is the **sole binding registration of record** (`paper.md`, 2026-07-04 note). Nothing below is invented beyond those two sources; where they differ, `paper.md` governs and the divergence is noted explicitly per RQ. Keep this file synchronized with `paper.md` Step 6 and `paper_draft.md`'s Experiments section — if one changes, change all three.
>
> **Tier accounting** (per `pipeline.md` Stage 6, checked against `study_type = empirical`): **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis. **Framing-tier: 0** — no Stage 3 limitation was flagged `verify_as_hypothesis`. **Outcome-tier: 0** — `empirical` study type forbids "our procedure beats baseline X" framing; every baseline below is a sanity-check/isolation comparator, never a competitor to beat. Within the 7 mechanism-tier RQs, `paper.md`'s registration of record further splits them into **5 confirmatory** (RQ2, RQ4, RQ5, RQ6, RQ7 — scored PASS/FAIL/INCONCLUSIVE against H1–H4) and **2 descriptive** (RQ1, RQ3 — pre-registered analyses with expected outcomes and falsification conditions, but no independent PASS/FAIL verdict).

---

## Datasets

- **ALFWorld** (deterministic household-task simulator) — pilot-stage domain. Justification: full determinism lets replay reproducibility be gated at ≥95% (assumption A2) before any strategy comparison is trusted; used for the Step 9 walking skeleton (20 trajectories) and as one of the two scale-up domains.
- **GAIA cached-web subset** (tool-use tasks, snapshotted/cached web content for deterministic replay) — scale-up domain. Justification: introduces tool-layer failures with real, though cached, tool-call variability absent from ALFWorld's synthetic simulator, letting RQ6 (layer-crossing design) and RQ7 (structure vs. uniform and judge) be tested under a genuine tool-use environment rather than only a household-task simulator, and stressing whether the structured-replay advantage generalizes beyond one domain's step semantics. (This justification replaced an earlier draft's citation-only justification — "digest mentions it as a scale-up domain" — flagged as too weak in Stage 6's critic round and refined to the hypothesis-linked reason above.)
- **Who&When human-annotated failure logs** — the natural-failure evaluation slice, re-hosted in the replay harness where re-executable. Justification: exposes any gap between injected-fault and natural-failure localization accuracy (assumption A6); its plan/tool/execution layer labels require a validated relabeling instrument (assumption A8, gate PG-4, κ ≥ 0.7) since Who&When's own schema does not carry that label.

## Baselines (sanity-check / isolation comparators — never a competitor to beat)

- **Budget-matched uniform-random checkpoint sampling (B-alt / M5a)** — isolates whether any advantage comes from the *index structure* bisection/group testing exploit, or merely from having replay access and spending a budget at all. Rival explanation it rules out: "the savings come merely from spending replay budget, not from index structure."
- **Exhaustive per-step counterfactual scan (M5b)** — the accuracy ceiling, not a competitor to beat; follows current fault-injection-corpus practice (AgenTracer-style).
- **Zero-replay log-only LLM judge (B0a; Who&When-style, all-at-once + step-by-step, M5c)** — the no-mechanism, current-practice control: if it matches replay-based accuracy, the entire replay enterprise is unjustified. Above-chance-but-weak accuracy is expected and does not bear on run validity.
- **B0b null-by-construction placebo (run-validity gate, not a research-question comparator)** — (i) label-shuffle placebo: score every strategy against permuted ground-truth indices, must land inside the analytic chance band; (ii) sham-injection arm: apply the fault-injection machinery at a step whose corruption verifiably does not flip the outcome, replay-based strategies must read "no fault" and the judge's predicted index must be at chance. B0b non-null invalidates the entire run and is checked before any H\*.
- **DoVer-style hypothesis-then-verify (M5d)** — checks whether LLM-proposed hypotheses plus replay verification match a budget-blind structured search; reported descriptively, not confirmatorily. If M5d dominates any structured strategy at any pre-registered budget point, CO4's provisioning guidance switches to hybrid wording for that budget regime rather than recommending blind structure.

## Metrics (shared across RQs)

Exact-step localization accuracy; step accuracy at ±2-step tolerance; layer accuracy (plan/tool/execution); replay cost in **replay units** (resumed LLM calls, position-weighted: cost of one `replay(k)` = (n−k+1) resumed LLM calls), with probe count and measured API dollar cost logged as secondary axes; the monotonicity-violation rate of the empirical g(k) profile; normalized area under the accuracy-vs-log-budget curve over the shared budget grid B ∈ {2, 4, 8, 16, 32, 64, exhaustive}.

---

## RQ1 — Position-dependent replay-unit savings

- **Tier.** Mechanism-tier (Stage 6); **descriptive** per `paper.md`'s registration of record — the pre-registered cost-accounting analysis under assumption A7, reported alongside H1–H4 but carrying no independent PASS/FAIL verdict.
- **Target hypothesis (verbatim, Stage 5 `m_position_cost_accounting`).** "Billing replay cost in resumed-LLM-call units rather than raw probe count shows that structured strategies' cost advantage over exhaustive per-step scanning is largest specifically for late-decisive-step trajectories, where per-probe replay units are cheapest to begin with — i.e., the replay-unit savings are not uniform across where the decisive step falls."
- **Setup.** For every trajectory in the pilot and scale-up corpora, compute each strategy's total replay-unit cost (resumed LLM calls) and its exact-step accuracy, then stratify the ratio of structured-strategy cost to exhaustive-scan cost by the quartile of the trajectory in which the decisive step d falls (early/mid/late).
- **Sample-size rationale.** Rides on the same n=300 scale-up corpus used for RQ2/RQ7 (see below); as a descriptive stratification rather than a confirmatory test, no independent power calculation is pre-registered for it.
- **Statistical test.** None formal (descriptive stratification); reported alongside a rank-stability check of strategy ordering across the three cost-accounting axes (replay-unit, probe-count, dollar).
- **Expected outcome.** The replay-unit cost ratio (structured strategy / exhaustive scan) is smallest — savings largest — for late-decisive-step trajectories, where a suffix replay is cheapest to begin with; savings are smaller, though still present, for early-decisive-step trajectories.
- **Falsification condition.** Refuted if the cost ratio is uniform across where the decisive step falls (no quartile effect), or if a probe-count-based accounting would rank strategies differently from a replay-unit accounting — either would mean the position-dependent cost claim is not load-bearing and a simpler probe-count metric would have sufficed.
- **Metrics.** Replay-unit cost ratio by decisive-step-position quartile; rank stability of strategies across replay-unit, probe-count, and dollar-cost accounting.

## RQ2 — Bisection ceiling vs. exhaustive scan

- **Tier.** Mechanism-tier (Stage 6); **confirmatory** — tests `paper.md` **H1** (the sole binding registration; supersedes the Stage 5/Stage 6 `rq_bisection_ceiling` wording's monotone-subset restriction, per `paper.md`'s "Registration of record" note).
- **Target hypothesis (verbatim, `paper.md` H1).** "On the injected-fault corpus, bisection and/or group testing reach ≥90% of the exhaustive per-step scan's exact-step accuracy while consuming ≤25% of its replay-unit cost."
- **Setup.** Pilot stage: 2 backbones × 2 conditions (bisection, exhaustive scan) × ALFWorld, 60 trajectories (20 per layer). Scale-up: ≥4 backbones × 2 domains (ALFWorld, GAIA cached-web subset) × 300 trajectories. Scored on the **pooled** scale-up corpus (not restricted to a monotone-profile subset — that restriction, present in an earlier draft, is dropped per the registration of record).
- **Sample-size rationale.** n=300 scale-up trajectories, sized to give >80% power to detect a 10-percentage-point paired accuracy difference at α=0.05 assuming ~20% discordance (shared corpus-sizing rationale with RQ7, below).
- **Statistical test.** Paired McNemar's test on exact-step accuracy; Wilcoxon signed-rank on replay-unit cost; α=0.05, Holm–Bonferroni-corrected across backbones and domains.
- **Aggregation.** PASS requires the pooled effect *and* the same-direction effect (bisection within the stated accuracy/cost floor of exhaustive) in ≥3 of 4 environment×LLM-family strata; if an entire environment stratum is lost to the harness reproduction-rate gate (PG-2), the rule degrades to same-direction in 2 of 2 remaining strata and the claim's envelope narrows to the surviving environment.
- **Expected outcome.** On the pooled scale-up corpus, bisection reaches at least 90% of the exhaustive scan's exact-step accuracy while consuming at most 25% of its replay-unit cost.
- **Falsification condition.** Refuted if bisection needs a replay-unit budget at or above 50% of the exhaustive scan's to come within 5 accuracy points of it, on the pooled corpus.
- **Metrics.** Exact-step accuracy and 95% CI (pooled corpus); replay-unit cost ratio (bisection / exhaustive).

## RQ3 — Monotonicity-violation rate as predictor

- **Tier.** Mechanism-tier (Stage 6); **descriptive** per `paper.md`'s registration of record — the pre-registered mechanism analysis under assumptions A3/F1, informing how H1's fallback (F1) is worded if H1 fails, not independently PASS/FAIL-scored.
- **Target hypothesis (verbatim, Stage 5 `m_bisection_localizer`, second hypothesis).** "Trajectories whose empirical g(k) profile violates monotonicity show bisection's accuracy advantage over uniform sampling shrink to within 5 percentage points, demonstrating that the monotonicity-violation rate is the load-bearing predictor of where the bisection shortcut works."
- **Setup.** Compute the monotonicity-violation rate per trajectory from bisection's logged g(k) profile; stratify trajectories into violating vs. non-violating strata; compare bisection's accuracy advantage over budget-matched uniform sampling within each stratum.
- **Sample-size rationale.** Same n=300 scale-up corpus as RQ2; no independent power calculation pre-registered (descriptive stratified diagnostic, not a confirmatory test).
- **Statistical test.** Paired McNemar within each stratum (violating vs. non-violating), Holm-corrected across the two strata.
- **Expected outcome.** In the monotonicity-violating stratum, bisection's accuracy advantage over uniform sampling shrinks to within 5 percentage points; in the non-violating stratum, the advantage remains large (consistent with RQ2's expected margin).
- **Falsification condition.** Refuted if the advantage is statistically indistinguishable between the violating and non-violating strata — meaning the monotonicity-violation rate carries no predictive information about where bisection's shortcut holds.
- **Metrics.** Per-stratum accuracy advantage (bisection − uniform) and 95% CI; monotonicity-violation rate distribution.

## RQ4 — Vote-count stabilization (r sweep)

- **Tier.** Mechanism-tier (Stage 6); **confirmatory** — tests conjunct (i) of `paper.md` **H4**.
- **Target hypothesis (verbatim, Stage 5 `m_vote_denoising`).** "r=3 repeated replays per probe stabilize bisection's localization accuracy to within 3 percentage points of r=5, at sampling temperature approximately 0.7 — the marginal value of de-noising past r=3 is small."
- **Setup.** Run bisection with r ∈ {1, 3, 5} repeated replays per probe at sampling temperature ≈0.7 on the same trajectories; estimate the single-replay flip rate per trajectory.
- **Sample-size rationale.** Same n=300 scale-up corpus; assumption A5 (oracle noise bounded/de-noisable with small r) is checked inside this RQ itself at scale-up, not via a separate pilot gate, since votes only become a first-class variable at scale.
- **Statistical test.** Paired Wilcoxon signed-rank across r∈{1,3,5} pairwise comparisons; α=0.05 with Holm correction across H4's two conjuncts (per-conjunct α=0.025), and further Holm-corrected across the three pairwise r-comparisons within this conjunct.
- **Expected outcome.** r=3 stabilizes bisection's accuracy to within 3 percentage points of r=5, indicating diminishing returns to further de-noising beyond r=3.
- **Falsification condition.** Refuted if accuracy at r=1 is statistically indistinguishable from r=5 (oracle effectively deterministic — a scoping result per fallback F4(a), not a failure), or if the gap between r=3 and r=5 exceeds 3 points (more votes required than assumed).
- **Metrics.** Exact-step accuracy vs. r; single-replay flip rate per trajectory.

## RQ5 — Noise crossover: group testing vs. vote-multiplied bisection

- **Tier.** Mechanism-tier (Stage 6); **confirmatory** — tests conjunct (ii) of `paper.md` **H4**.
- **Target hypothesis (verbatim, Stage 5 `m_group_testing_crossover`, first hypothesis).** "There exists a single-replay flip rate (oracle noise level) above which group testing's accuracy-per-replay-unit exceeds vote-multiplied bisection's, demonstrating that redundancy is a more efficient de-noising mechanism than repeated bisection probes once oracle noise crosses that threshold."
- **Setup.** At a fixed group-testing partition design (contiguous), sweep the single-replay flip rate (via sampling temperature) and compare accuracy-per-replay-unit between group testing and vote-multiplied bisection (r chosen per RQ4) across the sweep.
- **Sample-size rationale.** Same n=300 scale-up corpus; the crossover point is located via a 95% bootstrap CI on the flip-rate axis rather than a separate sample-size calculation.
- **Statistical test.** Bootstrap CI (95%, 1,000 resamples) on the crossover flip rate, required to exclude "no crossover within the observed flip-rate range"; per-conjunct α=0.025 (Holm split of H4's α=0.05 across its two conjuncts).
- **p-axis support pre-condition.** Scorable only if observed per-trajectory flip rates actually span the ≥15% threshold region under the swept sampling temperatures (both environments were chosen for reproducibility/A2, so this is a live risk, not a formality); if unmet, this conjunct is pre-declared **INCONCLUSIVE (insufficient noise support)**, not FAIL.
- **Expected outcome.** A flip rate exists (expected near 15%) above which group testing's accuracy-per-replay-unit exceeds bisection's.
- **Falsification condition.** Refuted if flip rates do span the threshold region but no flip rate in that range shows group testing exceeding bisection's accuracy-per-replay-unit.
- **Metrics.** Accuracy-per-replay-unit vs. flip rate for both strategies; bootstrap CI on the crossover flip rate.

## RQ6 — Layer-crossing group design and per-layer structured advantage

- **Tier.** Mechanism-tier (Stage 6); **confirmatory** — tests `paper.md` **H3**, both conjuncts (layer-crossing-vs-contiguous margin on plan-layer faults, and per-layer structured-vs-uniform advantage).
- **Target hypothesis (verbatim, Stage 5 `m_group_testing_crossover`, second hypothesis).** "Layer-crossing group-testing partitions outperform contiguous-only partitions by at least 5 percentage points specifically on plan-layer decisive failures, because plan-layer failures are the ones most likely to manifest through a downstream tool or execution step rather than locally."
- **Setup.** At a fixed noise level, compare contiguous vs. explicitly layer-crossing group-testing partition designs on exact-step and layer accuracy, stratified by the decisive step's true layer. Balanced corpus construction (assumption A4) guarantees ≈90–100 trajectories per layer at n=300.
- **Sample-size rationale.** Per-layer power ≈65–70% at α=0.017 (Holm-corrected over 3 layers) to detect a 10-point paired accuracy difference at ~90–100 trajectories/layer and ~20% discordance — below the pooled n=300 check's >80% power; any layer falling under this power floor is pre-declared INCONCLUSIVE for that layer.
- **Statistical test.** Paired McNemar per layer, Holm-corrected across the three layers (α=0.017 per layer after correction); layer × design interaction via stratified analysis.
- **Aggregation.** Requiring all 3 layers to independently clear significance would mostly measure power (≈0.65³–0.70³≈0.27–0.34 even if true everywhere), so H3's first conjunct PASSes iff the ≥10-point advantage holds in ≥2 of the adequately-powered layers *and* no adequately-powered layer shows a significant reversal; if fewer than 2 layers are adequately powered, the first conjunct is INCONCLUSIVE. The second conjunct (layer-crossing margin on plan-layer faults) is scored separately; H3 PASSes only if both conjuncts PASS.
- **Expected outcome.** Layer-crossing partitions outperform contiguous partitions by ≥5 points on plan-layer decisive failures specifically, with little/no difference on tool- or execution-layer failures; independently, the ≥10-point structured-over-uniform advantage holds within each layer stratum.
- **Falsification condition.** Second conjunct refuted if layer-crossing shows no advantage on plan-layer failures, or an equal/larger advantage on tool/execution layers. First conjunct refuted (not merely INCONCLUSIVE) only if an adequately-powered layer shows a significant reversal (uniform > structured).
- **Metrics.** Per-layer exact-step and layer accuracy, contiguous vs. layer-crossing partitions.

## RQ7 — Structured strategies vs. budget-matched uniform sampling and zero-replay judge

- **Tier.** Mechanism-tier (Stage 6); **confirmatory** — tests `paper.md` **H2**.
- **Target hypothesis (verbatim, Stage 5 `m_budget_matched_baseline_suite`).** "At a replay budget of one-quarter the trajectory length, both bisection and group testing exceed budget-matched uniform sampling's exact-step accuracy by at least 15 percentage points, and the zero-replay log-only judge sits at least 20 percentage points below the best structured strategy — establishing that both index structure and replay access, not just budget spend, are doing real work."
- **Setup.** At a replay budget of one-quarter the trajectory length (B=n/4), compare bisection and group testing against budget-matched uniform sampling and the zero-replay log-only judge on exact-step accuracy. Full budget-grid curve (B∈{2,...,64,exhaustive}) reported descriptively at every grid point; only the B=n/4 point is confirmatory.
- **Sample-size rationale.** n=300 trajectories in the scale-up corpus, sized to give >80% power to detect a 10-percentage-point paired accuracy difference at α=0.05 assuming ~20% discordance.
- **Statistical test.** Paired McNemar per comparison (4 pairwise: bisection-vs-uniform, group-testing-vs-uniform, bisection-vs-judge, group-testing-vs-judge), Holm-corrected across the four comparisons.
- **Aggregation.** PASS scored on the pooled n=300 corpus at the single pre-registered budget B=n/4 and additionally requires the same-sign effect in ≥3 of 4 environment×LLM-family strata (same PG-2 stratum-loss rule as RQ2/H1).
- **Expected outcome.** Both bisection and group testing exceed budget-matched uniform sampling's exact-step accuracy by ≥15 percentage points, and the zero-replay judge sits ≥20 percentage points below the best structured strategy.
- **Falsification condition.** Refuted (structure adds nothing) if either structured strategy fails to beat budget-matched uniform sampling by a statistically significant margin; refuted (replay is pointless) if the zero-replay judge's accuracy is statistically indistinguishable from the best structured strategy's.
- **Metrics.** Exact-step accuracy per strategy at B=n/4, pairwise accuracy gaps and 95% CIs.

---

## Global fallbacks (apply across RQs, per `paper.md` Step 6)

- **F-G1** — IF the central hypothesis family (H1+H2, i.e. RQ2+RQ7) fails, pivot archetype from "measurement of a saving" to "negative-result diagnostic": quantify *when* structured replay cannot succeed, using trajectory features (monotonicity-violation rate, recovery probability, layer) as the predictor.
- **F-G2** — IF the natural-failure slice proves non-replayable (fewer than 30 re-hosted Who&When logs pass gates PG-1/PG-2) AND the injected corpus's monotonicity-violation rate is degenerate (~zero variance), pivot to measuring the replayability-censoring mechanism itself, reporting the injected-fault curves as an upper-bound protocol with unmeasured transfer to natural failures.
