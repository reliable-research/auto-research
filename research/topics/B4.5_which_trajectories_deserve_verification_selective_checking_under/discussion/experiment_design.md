# Experiment Design — B4.5: Which Trajectories Deserve Verification?

> Standalone protocol, executable without opening the paper. Assembled from Stage 6's confirmed output in `discussion_trace.md` (formerly `pipeline.md`'s "## Stage 6 — Experiment Design" section) and `../paper.md`'s Step 6 ("Pre-Registered Experiments") / Step 9 ("Walking Skeleton"), reconciled against the already-fixed Experiments section of `paper_draft.md` (which folded in the Phase-G adversarial-review fix that extended RQ3 with `paper.md`'s H2(i) budget-recovery criterion). Nothing below is invented — every number, threshold, and justification traces to one of those three sources. Study type: `empirical` (Stage 1, confirmed) — no outcome-tier "beats baseline X" claims; every baseline is a sanity check or a strongest-alternative-explanation control (Stage 6 tier accounting: 7 mechanism-tier RQs, 0 framing-tier, 0 outcome-tier).
>
> Keep this file synchronized with `paper_draft.md`'s Experiments section — if either is edited, edit both.

---

## 1. Datasets

| Dataset | Role | Justification |
|---|---|---|
| **GSM8K** (test split; fixed 500-instance subsample for the pilot) | Pilot math anchor | Grade-school math word problems with short, exactly-matchable final answers — the cheapest domain in which to compute an oracle verifier label, anchoring the pilot stage. |
| **MATH-500** (500 competition-math problems, difficulty levels 1–5) | Pilot math, second point | Harder math with a graded difficulty knob; used both to pre-screen model–dataset pairs into the non-degenerate accuracy band (30–70%) the allocation question requires, and as a second math-domain point for the domain-transfer test (RQ7). |
| **HumanEval+** (164 tasks, EvalPlus-extended test suites) | Scale-up, code, realistic verifier | Enables an execution-based realistic verifier with near-ground-truth reliability, stress-testing whether selective-allocation gains survive contact with a genuinely non-oracle verifier (RQ6). |
| **MBPP+** (378 tasks, EvalPlus variant) | Scale-up, second code dataset | A second, larger and structurally different code benchmark (basic programming tasks vs. HumanEval+'s interview-style problems) — needed specifically so RQ7's code-side transfer cell and RQ6's execution-verifier audit are not certified from a single code dataset's idiosyncrasies alone. (This justification replaced a weaker provenance-only note — "digest lists it as a second code dataset" — flagged `[major]` in Stage 6's critic round and fixed in the refiner pass.) |

**Shared design constants** (frozen before Stage 1, per `paper.md` Step 6 header): pilot = 2 models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct) × 2 datasets (GSM8K-500, MATH-500), N = 16 sampled trajectories per instance, budget grid b ∈ {0.05, 0.10, 0.25, 0.50}, 5 seeds on the primary configuration, oracle verifier. Scale-up stage adds HumanEval+, MBPP+, N = 64, execution/PRM verifiers, and the sequential-reallocation method (M5). "Config" = one model×dataset pair; the pilot has 4 configs, the scale-up stage adds more.

## 2. Baselines

All baselines below are **sanity-check comparators or strongest-alternative-explanation controls, never outcome-tier competitors** — this is a measurement study; no research question is framed as "our procedure beats baseline X" (Stage 6 tier accounting, confirmed).

| Baseline | Role | Justification |
|---|---|---|
| **Uniform-random verifier-call allocation** at matched budget | B0 — necessary control | The no-mechanism arm every hypothesis is tested against: if selective allocation cannot beat this, no allocation question exists. |
| **Full verification** (B = N × #instances) | Upper anchor / headroom gate | Source of the verification-headroom gate: full-verification accuracy must exceed no-verification accuracy by ≥ 0.05 on a config, or that config is reported as out-of-scope (pre-registered exclusion, counted against generality claims). |
| **No verification / self-consistency majority vote** (Wang et al. 2023) | Lower anchor | Fixed sample count, equal weight per sample, no verification step — consensus-wrong answers pass through unchecked, exactly the failure a small, well-aimed verifier budget could catch. |
| **Difficulty-conditioned instance-level allocation**, adapted from Compute-Optimal-TTS | B-alt (strongest-alternative-explanation control) | Rules out the rival explanation "selective gains are just instance-difficulty triage — any per-instance hardness estimate would do; per-trajectory uncertainty adds nothing." Allocate calls to instances ranked by base-model difficulty estimate, then verify random trajectories within; call-budget-matched and aggregator-matched against the trajectory-uncertainty policy. |
| **Confidence-threshold escalation**, adapted from Trust-or-Escalate | B-alt (strongest-alternative-explanation control) | Per-item threshold, ignoring global budget coupling — isolates the value of *global*, budget-coupled ranking over *per-item*, budget-blind thresholding (Stage 3's sharpened role for this work: not a direct results comparison against Trust-or-Escalate's own human-agreement guarantees, only its calibrated-threshold mechanism is borrowed). |

**Note on B-alt wiring (resolved 2026-07-05, post-review revision round):** `pipeline.md`'s Phase G log had flagged that both B-alt controls were declared in `paper.md`'s pre-registered design and named in the Baselines paragraph but **not wired into an explicit RQ comparison arm**. This is now closed by extending RQ3 with a part (iii) that carries `paper.md`'s own pre-registered comparison verbatim ("M2 instance-level policy vs. B-alt at b ∈ {.10, .25}, same families/corrections; if M2 does not beat difficulty-triage, the claim demotes from 'trajectory-uncertainty-guided' to 'difficulty-guided' allocation") — the option `pipeline.md` itself named ("extend RQ3 to a three-arm design"), chosen over a dedicated RQ8 because no Stage 5 hypothesis exists for B-alt and this file's target hypotheses must stay byte-identical to their sources. See RQ3 below.

## 3. Statistical framework

Per `paper.md` Step 6 header and the per-RQ "Verification" lines: signal discrimination is assessed via AUROC with DeLong confidence intervals; matched-budget accuracy comparisons use paired McNemar tests plus 10,000-resample paired bootstrap confidence intervals on identical frozen trajectory pools; multiple comparisons within each declared family (e.g., {4 configs × 3 signals} for AUROC, {4 configs} for a single matched-budget comparison) are corrected with Holm–Bonferroni; realism, transfer, and sequential claims are each their own declared Holm family. Sample size for the pilot is 500 instances per config, stated as "power adequate for a 2-point paired difference at base accuracy 30–70%" (`paper.md` E1).

---

## 4. Research questions

All 7 are **mechanism-tier**, one per Stage 5 hypothesis, each `target_hypothesis` reproduced verbatim from Stage 5 / Stage 6 of `discussion_trace.md`. Setup, expected outcome, falsification condition, and metrics are reconciled with `paper_draft.md`'s Experiments section (already-reviewed final wording, including the Phase-G fixes).

### RQ1 — Do any of the verifier-free signals actually discriminate correct from incorrect trajectories?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_proxy_validity` (Stage 4). **Target method:** `m_uncertainty_scorer` (Stage 5).
- **Target hypothesis (Stage 5, verbatim):** "At least one of the three verifier-free signals attains AUROC ≥ 0.65, with 95% DeLong CI lower bound > 0.55, against verifier-labeled trajectory correctness on at least 3 of 4 pilot model×dataset configurations."
- **Setup.** On a held-out audited sample per pilot model×dataset configuration, compute AUROC (with DeLong confidence intervals) for each of the three signals — mode share, normalized sequence log-likelihood, verbalized confidence — against verifier-determined correctness.
- **Sample-size rationale.** 500 instances per config (pilot: 4 configs); `paper.md` states this is "power adequate for a 2-point paired difference at base accuracy 30–70%," the same base rate range this signal-validity test operates within.
- **Statistical test.** Per-signal AUROC with DeLong 95% CI; family = {4 configs × 3 signals}, Holm–Bonferroni corrected.
- **Expected outcome.** At least one signal attains AUROC ≥ 0.65, with a 95% DeLong CI lower bound above 0.55, on at least 3 of 4 pilot configurations.
- **Falsification condition.** Refuted if every signal's AUROC CI lower bound falls at or below 0.55 (indistinguishable from chance) on a majority of configurations — meaning the proxy gap is effectively total and no signal-based allocation policy can be expected to beat blind spending.
- **Metrics.** Per-signal AUROC and DeLong CI, per configuration.

### RQ2 — Are the highest-value, confident-but-wrong trajectories the ones every signal ranks as least worth verifying?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_proxy_validity`. **Target method:** `m_uncertainty_scorer`.
- **Target hypothesis (Stage 5, verbatim):** "Confident-but-wrong instances — plurality-answer mode share ≥ 0.75 and incorrect — are systematically under-selected by every signal-ranked policy relative to chance: P(rank in top-B | confident-but-wrong) falls below B/(mN)."
- **Setup.** Among instances whose plurality answer has mode share ≥ 0.75 and is nonetheless incorrect, measure the rate at which each signal's ranking places them outside the top-B selected for verification, and compare against the chance rate B/(mN) — the selection rate a uniform-random size-B sample would be expected to produce for any subgroup.
- **Sample-size rationale.** Same pilot pool as RQ1 (500 instances/config, 4 configs); the confident-but-wrong subgroup is a subset of this pool, so no additional sampling is required — its size is a fallout of the pilot's own model×dataset accuracy distribution.
- **Statistical test.** No separate significance test is specified in the pre-registered design beyond the threshold comparison itself; falsification is a direct rate comparison against the chance rate B/(mN), per signal and configuration (this is stated plainly here rather than implying a test that neither `pipeline.md` nor `paper.md` specifies).
- **Expected outcome.** Confident-but-wrong instances are selected for verification at a rate below the chance rate, for every one of the three signals.
- **Falsification condition.** Refuted if confident-but-wrong instances are selected at or above the chance rate under any signal — meaning the structural blind spot does not manifest for that signal.
- **Metrics.** Confident-but-wrong under-selection rate versus chance rate B/(mN), per signal and configuration.

### RQ3 — Does uncertainty-guided allocation beat uniform-random allocation at matched budget, and does it recover the majority of the full-verification gain at a small fraction of calls?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_allocation_granularity` (Stage 4). **Target method:** `m_budget_constrained_policy` (Stage 5).
- **Target hypothesis, part (i) (Stage 5, verbatim):** "The best single-signal, most-uncertain-first allocation policy beats uniform-random allocation at matched budget b = 0.10 by at least 2.0 accuracy points, with Holm-corrected McNemar p < 0.05, on at least 3 of 4 pilot configurations."
- **Target hypothesis, part (ii) — extension (`paper.md` H2(i), verbatim, added at Phase G per `pipeline.md`'s Phase Log: "Claim 1 / paper.md H2(i) ... had no corresponding RQ — extended RQ3 with the paper.md-licensed criterion"):** "budget-recovery fraction R(0.25) ≥ 0.50 with 95% bootstrap CI lower bound > 0.25 (strictly better than spend-proportional recovery) on ≥ 3 of 4 configs."
- **Pre-registered comparison, part (iii) — B-alt wiring (`paper.md` § Mandatory baselines, verbatim, wired in at the 2026-07-05 post-review revision round to close `pipeline.md`'s Phase G open to-do):** "Pre-registered comparison: M2 instance-level policy vs. B-alt at b ∈ {.10,.25}, same families/corrections; if M2 does not beat difficulty-triage, the claim demotes from 'trajectory-uncertainty-guided' to 'difficulty-guided' allocation (wording committed here)." B-alt = difficulty-conditioned instance-level allocation adapted from Compute-Optimal-TTS (primary) and confidence-threshold escalation adapted from Trust-or-Escalate (secondary), both call-budget-matched and aggregator-matched (see §2 Baselines).
- **Setup.** At b = 0.10, compare the best single-signal, most-uncertain-first allocation policy against uniform-random allocation on identical frozen trajectory pools, with a paired significance test and multiple-comparison correction across configurations. Separately, at b = 0.25, compute the budget-recovery fraction R(0.25) for the same policy with a bootstrap CI, testing the headline claim (Claim 1) that selective allocation recovers most of the full-verification gain at a small fraction of the calls. Third, at b ∈ {0.10, 0.25}, compare the M2 instance-level uncertainty-guided policy against each of the two B-alt control arms (difficulty-triage; confidence-threshold escalation), call-budget-matched and aggregator-matched, on the same frozen pools with the same test families and corrections as (i).
- **Sample-size rationale.** Pilot: 500 instances/config, 4 configs (same power rationale as RQ1); curves for R(b) draw on 5 seeds on the primary configuration for seed-level dispersion (`paper.md` Step 6 header). Part (iii) reuses the same pools and configs — no additional sampling.
- **Statistical test.** (i) Holm-corrected paired McNemar test, family = {4 configs}. (ii) 10,000-resample paired bootstrap CI on R(0.25). (iii) Same paired McNemar + Holm machinery as (i), per `paper.md`'s "same families/corrections," one family per B-alt arm × budget grid {0.10, 0.25}.
- **Expected outcome.** (i) The best single-signal policy beats uniform-random allocation by ≥ 2.0 accuracy points, corrected p < 0.05, on ≥ 3 of 4 pilot configurations. (ii) R(0.25) ≥ 0.50, with a 95% bootstrap CI lower bound above 0.25, on ≥ 3 of 4 pilot configurations. (iii) The M2 instance-level policy beats difficulty-triage at b ∈ {0.10, 0.25} under the same corrected criterion, and likewise beats per-item confidence-threshold escalation at matched budget — establishing that the gain is attributable to per-trajectory uncertainty under global budget coupling, not to instance-difficulty triage or per-item thresholding alone.
- **Falsification condition.** (i) Refuted if the accuracy difference between the best signal-ranked policy and uniform-random allocation is not significantly positive on a majority of configurations. (ii) Refuted if R(0.25)'s CI lower bound falls at or below 0.25 on a majority of configurations — recovery would then be only proportional to spend (budget–accuracy curve statistically indistinguishable from the diagonal), so Claim 1's "recovers the majority of the gain" wording would not hold even where (i) does. (iii) Is an attribution test, not a refutation of the allocation gain itself: if M2 does not beat difficulty-triage, the claim demotes — per the wording committed in `paper.md` — from "trajectory-uncertainty-guided" to "difficulty-guided" allocation; if M2 does not beat confidence-threshold escalation, the value of *global* budget-coupled ranking over per-item, budget-blind thresholding is not demonstrated and the framing scopes down to per-item selection.
- **Metrics.** Matched-budget accuracy difference and its CI, per configuration; R(0.25) and its bootstrap CI, per configuration; matched-budget accuracy difference between M2 and each B-alt arm at b ∈ {0.10, 0.25}, per configuration.

### RQ4 — Does sequential reallocation close a meaningful share of the static policy's gap to hindsight-optimal allocation?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_allocation_granularity`. **Target method:** `m_budget_constrained_policy` (sequential variant, M5).
- **Target hypothesis (Stage 5, verbatim; = `paper.md` H3c):** "Sequential reallocation closes at least 20% of the static policy's accuracy gap to hindsight-optimal allocation at b ≤ 0.10, with bootstrap CI excluding 0, on at least 2 of 4 configurations."
- **Setup.** At a small budget fraction (b ≤ 0.10), compute the accuracy gap between the static ranking policy and a hindsight-optimal allocation (computable post hoc once all pools are fully labeled), and measure what share of that gap the sequential reallocation policy (M5) closes.
- **Sample-size rationale.** Pilot configs, oracle-stage pools are fully labeled (so the hindsight-optimal reference is exactly computable, not estimated); gap-closure fraction uses the same 5-seed dispersion as RQ3.
- **Statistical test.** Bootstrap CI on the gap-closure fraction, its own declared Holm family (sequential), per `paper.md`'s "three separate Holm families (realism / transfer / sequential)."
- **Expected outcome.** Sequential reallocation closes ≥ 20% of the static policy's gap to hindsight-optimal allocation, with bootstrap CI excluding 0, on ≥ 2 of 4 configurations.
- **Falsification condition.** Refuted if the sequential policy's gap-closure is statistically indistinguishable from zero on a majority of configurations — meaning the online/adaptive character of the allocation problem is not worth the added complexity at these budget levels.
- **Metrics.** Gap-closure fraction = (Acc_M5 − Acc_M2) / (Acc_hindsight − Acc_M2), and its bootstrap CI, per configuration.

### RQ5 — Does the elimination-aware aggregator add accuracy beyond the naive combination rule?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_aggregation` (Stage 4). **Target method:** `m_elimination_aggregator` (Stage 5).
- **Target hypothesis (Stage 5, verbatim; = `paper.md` H2b):** "The elimination-aware aggregator beats the naive rule (use the verified answer if any, else raw majority vote) by at least 1.0 accuracy point at b = 0.25, with a paired bootstrap CI excluding 0, on at least 3 of 4 configurations."
- **Setup.** At b = 0.25, compare the elimination-aware aggregator (removes verified-incorrect answers from contention, confidence-weighted vote over what remains, falls back to highest-confidence unverified answer if verification eliminates every observed candidate) against the naive rule on identical verified pools, isolating the aggregation step from the allocation policy.
- **Sample-size rationale.** Its own 4-config family at b = 0.25 (`paper.md` Step 6: "H2b tested in its own 4-config family").
- **Statistical test.** Paired bootstrap CI excluding 0, family = {4 configs}.
- **Expected outcome.** The elimination-aware aggregator beats the naive rule by ≥ 1.0 accuracy point, paired bootstrap CI excluding 0, on ≥ 3 of 4 configurations.
- **Falsification condition.** Refuted if the aggregator's accuracy advantage is statistically indistinguishable from zero on a majority of configurations — meaning exploiting verified-incorrect eliminations adds nothing measurable, and aggregation is not a separate design axis from allocation at these budgets.
- **Metrics.** Matched-budget accuracy difference between the two aggregation rules and its CI.

### RQ6 — Do allocation gains survive the move from an oracle verifier to realistic verifiers?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_domain_transfer` (Stage 4). **Target method:** `m_realism_and_transfer_controls` (Stage 5).
- **Target hypothesis (Stage 5, verbatim, H_F; ≈ `paper.md` H3a, which adds a code-execution-specific clause quoted below):** "Under execution (code) and process-reward-model (math) verifiers, the selective-allocation accuracy gain retains at least 50% of its oracle-verifier magnitude and remains statistically significant on at least 2 of 4 scale-up configurations."
  - **`paper.md` H3a elaboration (verbatim):** "...on code with execution verification (near-ground-truth), Δacc(0.25) > 0 with p < 0.05."
- **Setup.** Repeat the matched-budget selective-vs-uniform comparison under execution-based (code) and process-reward-model-based (math) verifiers, after each verifier passes the false-positive/false-negative audit gate (Stage 1's realistic-tier trust definition), and compare the resulting accuracy gain against its oracle-verifier magnitude.
- **Sample-size rationale.** Scale-up stage: N = 64, HumanEval+ + MBPP+ (code) and MATH-500 (math) added to the pilot's GSM8K/MATH-500 base, execution/PRM verifiers — "Stage-2 configs" / "scale-up configurations" per `paper.md`.
- **Statistical test.** Same paired McNemar + bootstrap machinery as RQ3; its own declared Holm family (realism), per `paper.md`'s three-family split (realism / transfer / sequential). A verifier-noise sensitivity sweep linking to ROC-n-reroll is reported descriptively, with no attached hypothesis.
- **Expected outcome.** The accuracy gain under realistic verifiers retains ≥ 50% of its oracle-verifier magnitude and remains statistically significant on ≥ 2 of 4 scale-up configurations.
- **Falsification condition.** Refuted if the gain falls below half its oracle-verifier magnitude, or loses significance, on a majority of scale-up configurations — especially damaging under the code-execution verifier specifically, since execution verifiers are close to ground truth and a collapse there cannot be blamed on verifier noise.
- **Metrics.** Realistic-verifier accuracy gain as a fraction of oracle-verifier accuracy gain, per configuration; accuracy-per-dollar logging (A6).

### RQ7 — Does a policy frozen on one task domain transfer to another?

- **Tier:** mechanism.
- **Target sub-problem:** `sp_domain_transfer`. **Target method:** `m_realism_and_transfer_controls`.
- **Target hypothesis (Stage 5, verbatim, H_G; = `paper.md` H3b):** "A policy frozen on one task domain beats uniform allocation on the other domain at b = 0.25, with corrected p < 0.05, in at least 3 of 4 transfer-direction × model cells."
- **Setup.** Freeze a policy's signal choice and ranking granularity exactly as selected on one task domain (math or code), and evaluate it unmodified, with no retuning, on the other domain, comparing against uniform-random allocation on that domain.
- **Sample-size rationale.** Scale-up stage configs (math: GSM8K/MATH-500; code: HumanEval+/MBPP+), evaluated across transfer-direction × model cells (2 directions × 2 models = 4 cells minimum, per the "3 of 4 transfer-direction × model cells" threshold).
- **Statistical test.** Same paired machinery as RQ3/RQ6; its own declared Holm family (transfer).
- **Expected outcome.** The frozen policy beats uniform allocation on the domain it was not tuned on, at b = 0.25 with corrected p < 0.05, in ≥ 3 of 4 transfer-direction × model cells.
- **Falsification condition.** Refuted if the frozen policy fails to beat uniform allocation on the untuned domain in a majority of transfer cells — meaning signal informativeness is domain-bound and a verification-budget policy would need re-fitting per domain rather than transferring.
- **Metrics.** Transferred-policy accuracy delta over uniform allocation, per transfer direction and model.

---

## 5. Global fallback (if the central hypothesis family {RQ1, RQ3} fails jointly)

Per `paper.md`'s Global fallback F-G1: if signals prove uninformative or placement irrelevant, the paper pivots from "measurement of a working policy" to "negative-result characterization with a mechanism" — RQ2's confident-but-wrong under-selection measurement becomes the headline finding rather than a supporting one. Pre-committed pivoted abstract sentence: "We show that the verifier-free signals available to aim a metered verifier budget are systematically blind to the highest-value targets — confident-but-wrong consensus pools — and that this blindness, which we quantify as the confident-but-wrong mass across four benchmarks and two model families, caps selective verification at the value of blind spending, a measured ceiling that any future allocation policy must break by importing information from outside the sampling distribution."

## 6. Walking skeleton (pre-registered, `paper.md` Step 9)

**One binary question:** on one frozen pool, does mode-share-ranked allocation beat uniform allocation at b = 0.25 under an oracle verifier?
- **Arms:** uniform-random @ b=0.25; mode-share most-uncertain-first @ b=0.25; full verification (anchor).
- **Task set:** GSM8K, fixed 100-instance subsample, Qwen2.5-7B-Instruct, N = 16, one seed, greedy M4 aggregation.
- **Pass criterion (all four):** parse rate ≥ 0.95; headroom H ≥ 0.05; mode-share AUROC ≥ 0.60; arm-2 − arm-1 ≥ +1.0 accuracy point. Passing means scaling to the full grid above is a config change, not a code change.
