# Experiment Design — B1.2: Onset of Visible-Test Overfitting in Coding Agents

> Standalone experiment protocol, extracted from Stage 6's confirmed output in `pipeline.md` (Stage 6 — Experiment Design) and reconciled with `../paper.md`'s Step 6 (Pre-Registered Experiments), which is the later, authoritative registration for two RQs revised after Stage 6 closed (see notes on RQ5 and RQ8 below). This document is meant to be executable as a protocol on its own, without opening the paper. Status: **pre-registered design — no experiments have been run.** All "Result" lines are explicit placeholders.
>
> **Tier accounting** (per Stage 6 header in `pipeline.md`): **Mechanism-tier: 8 RQs** (one per Stage 5 hypothesis, verbatim). **Framing-tier: 0** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`. **Outcome-tier: 0** — `study_type = empirical` forbids "our procedure beats baseline X" framing; every baseline below is an isolation/sanity-check comparator, never a competitor to beat.

---

## Datasets

- **SWE-bench Verified** (Jimenez et al., 2024, ICLR) — *justification:* real Python repository-repair instances with fail-to-pass/pass-to-pass tests; the primary track for the full adequacy sweep (RQ3–RQ8) because it ships enough per-instance test infrastructure to support fine-grained sub-suite sampling.
- **Defects4J** (Just et al., 2014, ISSTA) — *justification:* Java repair instances with precomputed Major mutant kill matrices, letting the cross-language leg of the agent-transfer check (RQ7) reuse existing kill matrices instead of paying for fresh mutant generation.
- **EvalPlus / HumanEval+** (Liu et al., 2023, NeurIPS) — *justification:* precomputed, heavily augmented hidden tests serve as a ready-made held-out oracle and mutant surrogate on the Python track, directly de-risking the mutant-generation cost identified as the biggest feasibility risk (digest N6) for RQ1/RQ2's sampler/oracle validity checks. (Note: `paper.md` Step 5 withdraws this as a surrogate specifically for repository-level SWE-bench instances — EvalPlus artifacts are function-level — so its role is scoped to function-level pilot use, not the SWE-bench sweep itself.)
- **QuixBugs** (Lin et al., 2017, SPLASH Companion) — *justification:* small, single-fix Python/Java bugs with low mutant-generation cost; used specifically to pilot RQ1 (`rq_sampler_fidelity`) and RQ2 (`rq_oracle_soundness`) cheaply — the walking-skeleton stage — before committing the full Stage-1 budget to SWE-bench Verified and Defects4J, rather than to support a cross-language generalization claim in its own right. (This justification was itself a Stage 6 refiner-pass fix — the draft's original "for cross-language sanity" was rejected as a provenance note, not a methodological reason.)

## Baselines (isolation / sanity-check comparators — not outcome-tier competitors)

- **Full-adequacy control arm** (`ms ≈ 1.0`, size-matched) — the necessary reference point for every degraded-adequacy claim (feeds RQ3). Referred to in `paper.md` as **B-ref** (renamed from an earlier B0 label — it is not null-by-construction, since killing all mutants does not imply passing hidden tests).
- **Size-matched, adequacy-uncontrolled random sub-suite** — a covariate check within RQ1's setup, ruling out suite size/coverage as the true driver rather than adequacy itself (per `sp_adequacy_confound` / digest C4).
- **Budget-matched, single-shot best-of-k selection-only arm** (`m_selection_control`, `paper.md`'s **B-alt**) — no iterative retry, no feedback from the visible verdict; isolates iterative optimization pressure from a mechanical imperfect-verifier selection effect (feeds RQ8).
- **Null-by-construction placebo checks** (`paper.md`'s **B0**, checked before any of the above are scored): (i) a permutation placebo — shuffled adequacy labels must yield a null fixed effect; (ii) gold-patch pass-through — the gold patch must score a zero gap at every adequacy level. Either non-null invalidates the run per goal.md §5 step 1; no RQ below is scored until both are null.

## Common metrics (apply across RQs)

Mutation-kill score of the visible sub-suite; visible-pass and held-out-pass rates and their mixed-effects trend estimate; the overfitting gap and its confidence interval at each adequacy level; segmented-vs-smooth model-comparison statistics (ΔAIC, corrected Davies test p-value) for onset shape; the differential diagnostic's agreement with human-adjudicated labels and the resulting gaming fraction by adequacy band; the agent-by-adequacy interaction estimate and per-agent onset thresholds; the band-level gap difference (low-adequacy band, `ms ≤ 0.45`) between the iterative and selection-only arms. Additionally (2026-07-05 revision pass, per the design review's "where do real suites sit on your axis?" question): the empirical distribution of as-shipped full-suite mutation-kill scores across benchmark instances is reported descriptively — computed from the same kill matrices already required by RQ1, at zero additional agent cost — so any estimated onset threshold $s^*$ can be situated against where shipped suites actually sit, converting it from a curiosity into a calibration. This is a descriptive reporting commitment, not a new hypothesis; it enters no confirmatory test and does not alter the H1–H5 Holm family.

---

## RQ1 — `rq_sampler_fidelity`

**Tier.** Mechanism.

**Target hypothesis (verbatim, Stage 5 `m_adequacy_sampler`, unchanged through Stage 6 and `paper.md` A1/G-S1):**
> "The adequacy sampler attains each target mutation-kill score within ±0.05 while holding suite size and statement coverage within ±5% relative of the full suite, on at least 8 of 10 pilot instances with sufficiently rich kill matrices."

**Setup.** On 10 instances pre-screened for sufficiently rich kill matrices, construct sub-suites at each of six pilot adequacy levels ($ms \in \{0.3, 0.45, 0.6, 0.75, 0.9, 1.0\}$) and check whether the sampler hits each target within a fixed tolerance while holding suite size and statement coverage within a fixed relative tolerance of the full suite.

**Sample-size rationale.** 10 pilot instances, pre-screened for rich kill matrices (`paper.md` Assumption A1's detection gate). This is a walking-skeleton/instrument-validity gate sized to catch construction failures before committing budget to the full sweep — it is not power-analyzed for effect detection, since it tests a deterministic construction property, not a hypothesis about agent behavior.

**Statistical test.** None (deterministic threshold gate): the sampler either hits its target `ms` at matched size/coverage or it doesn't, per instance; the pass criterion is a count threshold (≥8/10), not a significance test.

**Expected outcome.** The sampler hits its target adequacy within tolerance, at matched size and coverage, on at least 8 of the 10 pilot instances.

**Metrics.** Per-instance adequacy error against target; per-instance size and coverage deviation from the full suite.

**Falsification condition.** The sampler misses its target mutation-kill score (outside tolerance) or breaches the matched size/coverage tolerance on more than 2 of the 10 pilot instances; any such instance is excluded before any agent is run rather than retained with a confounded adequacy label.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ2 — `rq_oracle_soundness`

**Tier.** Mechanism.

**Target hypothesis (verbatim, Stage 5 `m_adequacy_sampler`, unchanged through Stage 6 and `paper.md` A2/G-S2):**
> "The gold patch passes the full held-out oracle on repeated executions in 10 of 10 pilot instances, confirming the ground-truth signal is not itself flaky before it is used to score any agent patch."

**Setup.** On the same 10 pilot instances, execute the gold patch against the full held-out oracle three times each, checking for consistent pass verdicts across reruns.

**Sample-size rationale.** Same 10 pilot instances as RQ1, × 3 reruns each. Sized as an instrument-soundness gate (confirm the ground truth is not flaky), not as a powered hypothesis test.

**Statistical test.** None (deterministic replication gate): pass/fail consistency across 3 reruns per instance, on all 10 instances.

**Expected outcome.** The gold patch passes the full held-out oracle in all three reruns on all 10 pilot instances.

**Metrics.** Per-instance gold-patch pass/fail consistency across reruns.

**Falsification condition.** The gold patch fails even one of three held-out-oracle reruns on any pilot instance; that instance's oracle is treated as flaky and excluded from every downstream gap estimate rather than scored against an unreliable ground truth.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ3 — `rq_gap_exists`

**Tier.** Mechanism.

**Target hypothesis (verbatim, Stage 5 `m_trend_model`, unchanged through Stage 6; formalized as H1 in `paper.md` Step 6/E1):**
> "The overfitting gap G(s) = P(visible-pass) − P(held-out-pass), estimated by the mixed-effects model, is at least 10 percentage points larger at the lowest tested adequacy level than at full adequacy, with the mutation-score fixed effect significant at p<0.05 (Holm-corrected across agent families and mutant classes), while the gap at full adequacy itself stays at or below 10 percentage points."

**Setup.** Pilot stage: one agent family on approximately 50 instances of SWE-bench Verified, at six adequacy levels, with three samples per cell (approximately 900 episodes), to establish direction and estimate variance. Scale-up: three agent families (SWE-agent, Agentless, OpenHands) on approximately 300 instances spanning SWE-bench Verified and Defects4J, at eight adequacy levels ($ms \in \{0.3, 0.4, \dots, 1.0\}$), with five samples per cell (approximately 36,000 episodes).

**Sample-size rationale.** The pilot's 50-instance, 3-sample design is sized to estimate the variance needed to power the scale-up to detect a standardized gap difference at approximately 80–90% power at $\alpha = 0.05$ (`paper.md` Step 6 E1: "power target: ≥0.9 to detect a 10 pp gap difference at α=0.05 given the pilot's variance estimate"); an observed effect smaller than the design target in the pilot triggers a pre-committed enlargement of the scale-up sample rather than a premature null conclusion.

**Statistical test.** Mixed-effects logistic model of held-out-pass on mutation score, random intercepts for instance and agent, with a likelihood-ratio test on the mutation-score term, Holm-corrected across agent families (and across the H1–H5/RQ family per `paper.md`).

**Expected outcome.** The overfitting gap is at least 10 percentage points larger at the lowest tested adequacy level than at full adequacy, the mutation-score effect is statistically significant after correction, and the gap at full adequacy itself remains at or below 10 percentage points — establishing that adequacy, not a background gap present even at full adequacy, is the operative driver.

**Metrics.** The overfitting gap and its confidence interval at each adequacy level; the mixed-effects slope estimate and its corrected p-value.

**Falsification condition.** Either the gap at the lowest tested adequacy level fails to exceed the full-adequacy gap by 10 points with the mutation-score effect significant (a flat curve), or the gap at full adequacy itself already exceeds 10 points; either observation is reported as the finding itself, not a failed experiment. A third pre-committed outcome covers the wrong direction (`paper.md` Fallback-combination rule 2): if $\hat G(0.3) - \hat G(1.0) \le -10$ pp (gap *larger* at high adequacy), neither null wording applies — the inversion is reported at full prominence with an analysis of which mutant classes and patch behaviors drive it, never folded into a null.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ4 — `rq_curve_shape`

**Tier.** Mechanism.

**Target hypothesis (verbatim, Stage 5 `m_curve_shape_estimator`, unchanged through Stage 6; formalized as H2/H2a in `paper.md` Step 6/E2):**
> "The fitted gap-vs-adequacy relationship favors a smooth monotone specification over a segmented specification (ΔAIC < 10, or a Davies test not significant after multiplicity correction), i.e., visible-test overfitting grows gradually rather than at a sharp discrete threshold."

**Setup.** Conditional on RQ3 establishing a real trend, fit a segmented regression and a smooth monotone model to the pooled scale-up gap-vs-adequacy data, and compare via ΔAIC and a Davies test corrected for multiple comparisons.

**Sample-size rationale.** Reuses RQ3's pooled scale-up sample (~300 instances × 3 agent families × 8 levels × 5 samples); no separate sample is drawn or sized for this RQ beyond that pool.

**Statistical test.** Model comparison: segmented/changepoint regression vs. smooth monotone GAM via ΔAIC (decision margin ≥10) and a Davies test for breakpoint existence/location, corrected for multiple comparisons (parametric bootstrap for breakpoint CI per `paper.md`).

**Expected outcome.** The smooth monotone specification is favored (ΔAIC below the pre-specified margin, or the corrected Davies test non-significant), indicating the relationship is better described as gradual than as a sharp discrete threshold — consistent with mutation score being a coarse aggregate over a heterogeneous mutant population.

**Metrics.** ΔAIC between segmented and smooth models; corrected Davies test p-value and breakpoint confidence interval width. The monotone-growth component itself carries a pre-registered effect floor in native units (`paper.md` H2): the fitted smooth-monotone curve's total change across the sweep, $\hat G(0.3) - \hat G(1.0)$, must be at least 5 percentage points, so a statistically significant but practically flat trend is not reported as monotone growth regardless of p-value.

**Robustness cell (2026-07-05 deletion-audit addendum, per the design review's "is the onset driven by *which* mutants survive, not how many?" question):** at one mid-grid adequacy level (`ms = 0.6`), sub-suites are re-sampled under two deliberately different surviving-operator mixes at the same scalar `ms` (identical size/coverage constraints, M1), and $\hat G$ is re-estimated per mix; if the per-mix gap estimates differ by ≥ the 5 pp floor at equal scalar adequacy, the onset threshold $s^*$ is reported as operator-mix-conditioned rather than as a property of the scalar alone. Exploratory — outside the H1–H5 Holm family; it enters no confirmatory test.

**Falsification condition.** The fitted gap-vs-adequacy relationship is non-monotone (no consistent trend-test significance in either direction); reported as its own finding — that scalar mutation score does not order agent-exploitable suite weakness — rather than forced into either the sharp or gradual bucket.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ5 — `rq_diagnostic_validity`

**Tier.** Mechanism.

**Target hypothesis.** Stage 5/Stage 6's originally confirmed wording (`m_differential_diagnostic`) read: *"The differential-testing diagnostic's gaming/coincidental labels reach Cohen's kappa of at least 0.6 against dual-human-annotated adjudicated labels on a sample of visible-pass/held-out-fail patches."* This was **revised after Stage 6 closed** — `pipeline.md`'s own Phase Log (Phase A) records the acceptance bar being raised from κ≥0.6 to κ≥0.7 "to match guidance.md's stated requirement," and `paper.md` Step 6/E4 (H4(i)) now registers the updated bar as the authoritative wording. Per this document's sourcing rule (verbatim from Stage 5 *or* `paper.md`), the current registered hypothesis is used below:

> "M5's labels reach Cohen's $\kappa \ge 0.7$ against adjudicated dual human annotation on $n=100$ sampled $V{=}1,H{=}0$ patches" (`paper.md` Step 6, H4(i)).

**Setup.** Sample 100 visible-pass/held-out-fail patches produced during the scale-up sweep; two annotators, blind to the patches' adequacy level, independently label each as gaming or coincidental incompleteness, with disagreements adjudicated; compare against the diagnostic's automated labels.

**Sample-size rationale.** $n=100$ sampled patches, per `paper.md` E4's stated requirement ("requires ≥100 visible-pass/held-out-fail patches from E1, else fallback"); if fewer than 100 qualifying patches exist, H4 is reported as descriptive only (no confirmatory test) rather than the RQ being dropped.

**Statistical test.** Cohen's kappa between diagnostic labels and adjudicated human labels, evaluated against a binary acceptance bar (κ≥0.7) — a threshold check, not a significance test.

**Expected outcome.** The diagnostic's labels reach a Cohen's kappa of at least 0.7 against the adjudicated human labels.

**Metrics.** Cohen's kappa between diagnostic labels and adjudicated human labels.

**Falsification condition.** Cohen's kappa against adjudicated human labels falls below 0.7; the diagnostic is then withdrawn as a contribution and the annotated patch set is released as a labeling benchmark instead, rather than any trend claim (RQ6) being built on an unvalidated diagnostic.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ6 — `rq_gaming_trend`

**Tier.** Mechanism.

**Target hypothesis (verbatim, Stage 5 `m_differential_diagnostic`, unchanged through Stage 6; formalized as H4(ii) in `paper.md` Step 6/E4):**
> "The fraction of visible-pass/held-out-fail patches labeled gaming rises by at least 15 percentage points from the highest to the lowest tested adequacy band, indicating the widening gap is increasingly driven by exploitation rather than uniformly incomplete honest fixes."

**Setup.** Among all visible-pass/held-out-fail patches from the scale-up sweep, compute the diagnostic-labeled gaming fraction within the lowest and highest tested adequacy bands, and test the trend across bands with a corrected logistic trend test.

**Sample-size rationale.** Drawn from the same ≥100-patch pool used for RQ5 (banded by adequacy level: lowest band `ms ≤ 0.45` vs. highest band `ms ≥ 0.75` per `paper.md`); no independently sized sample beyond that pool. Conditional on RQ5 (H4(i)) passing — this RQ is not scored on an unvalidated diagnostic.

**Statistical test.** Logistic/CMH trend test of gaming fraction across adequacy bands, Holm-corrected.

**Expected outcome.** The gaming fraction at the lowest tested adequacy band exceeds that at the highest tested band by at least 15 percentage points, with a significant trend.

**Metrics.** Gaming fraction per adequacy band; trend-test statistic and corrected p-value.

**Falsification condition.** Conditional on RQ5 passing, the gaming fraction does not rise by the pre-specified 15-point margin from the highest to the lowest tested adequacy band; the widening gap, if any, is then reported as dominated by honest-but-incomplete fixes, not deliberate suite-gaming.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ7 — `rq_cross_agent_transfer`

**Tier.** Mechanism.

**Target hypothesis (verbatim, Stage 5 `m_transfer_harness`, unchanged through Stage 6; formalized as H3 in `paper.md` Step 6/E3):**
> "The agent-by-adequacy interaction term in the shared mixed-effects model is significant, and at least one pair of tested agent families has onset-threshold estimates differing by at least 0.15 mutation-score units with non-overlapping bootstrap 95% confidence intervals — i.e., no single universal onset threshold holds across the tested agent families."

**Setup.** Using the shared mixed-effects model fit across the three agent families in the scale-up, test the agent-by-adequacy interaction term via a likelihood-ratio test, and compare per-family onset-threshold estimates with bootstrap 95% confidence intervals.

**Sample-size rationale.** Reuses RQ3's scale-up sample (3 agent families, ~300 instances) — the number of agent families (3) is itself set by `paper.md` Assumption A6's budget-feasibility gate, which pre-commits to dropping to 2 families before shrinking instances-per-level if cost overruns; no separate sample-size rationale exists beyond that de-scope order.

**Statistical test.** Likelihood-ratio test of the agent×adequacy interaction term in the shared mixed-effects model; per-family onset-threshold bootstrap 95% confidence intervals.

**Expected outcome.** The agent-by-adequacy interaction is statistically significant, and at least one pair of tested families has onset-threshold estimates differing by at least 0.15 mutation-score units with non-overlapping confidence intervals — indicating no single universal onset threshold holds across the tested agents.

**Metrics.** Agent-by-adequacy interaction likelihood-ratio statistic; per-agent onset-threshold estimate and confidence interval.

**Falsification condition.** The agent-by-adequacy interaction is not statistically significant and no pair of tested families shows non-overlapping onset-threshold confidence intervals; onset behavior is then reported as benchmark-intrinsic rather than agent-intrinsic — promoted to a finding, not treated as a null result.

**Result.** *[placeholder — fill in after experiments are run]*

---

## RQ8 — `rq_selection_vs_iterative`

**Tier.** Mechanism.

**Target hypothesis.** Stage 5/Stage 6's originally confirmed wording (`m_selection_control`) read: *"The iterative arm's gap slope with respect to mutation score exceeds the budget-matched selection-only arm's slope by at least 5 percentage points at the lowest tested adequacy level, with the difference significant at p<0.05."* This was **revised after Stage 6 closed** — `pipeline.md`'s Phase Log (phase E/G) records this as a `[major]` internal-consistency fix: the slope-based formulation "mixed a derivative with a level difference and is superseded," and `paper.md` Step 6's registered **H5** (Mandatory baselines, B-alt) now states the corrected, authoritative wording, which is used below:

> "H5 holds iff the iterative arm's mean gap exceeds the selection-only arm's, $\hat G_{iter} - \hat G_{sel} \ge 5$ pp, in the low-adequacy band ($ms \le 0.45$), with the two-arm contrast in the mixed-effects model at $p<0.05$ (Holm, family {H1–H5})." (`paper.md` Step 6, Mandatory baselines / B-alt, registered as H5.)

**Setup.** Run a budget-matched, single-shot best-of-k selection arm at the same adequacy levels and total inference budget as the iterative arm, with no visible-suite feedback or retry; compare the two arms' mean gaps in the low-adequacy band (`ms ≤ 0.45`) via an arm×band contrast in the mixed-effects model.

**Sample-size rationale.** The selection-only arm is budget-matched (same total inference budget) to the iterative arm's scale-up sample from RQ3; no independent sample size is specified for this arm beyond that budget-matching constraint.

**Statistical test.** Arm×band contrast (iterative vs. selection-only) in the mixed-effects logistic model, Holm-corrected across the H1–H5 family.

**Expected outcome.** The iterative arm's mean gap in the low-adequacy band (`ms ≤ 0.45`) exceeds the feedback-free selection-only arm's mean gap in the same band by at least 5 percentage points, with the arm×band contrast significant at p<0.05 (Holm-corrected across the H1–H5 family).

**Metrics.** Mean gap for each arm in the low-adequacy band; band-level gap-difference estimate and significance test.

**Falsification condition.** The iterative arm's mean gap in the low-adequacy band does not exceed the feedback-free selection-only arm's by the pre-specified 5-point margin; every observed gap is then attributed to the mechanical imperfect-verifier selection effect the resampling literature already establishes, not to agent-side adaptive gaming. One contradictory-arms case is pre-committed rather than resolved ad hoc at verdict time (`paper.md` Fallback-combination rule 4, verbatim): if this isolation criterion (H5) fails while the gaming-fraction trend (RQ6/H4(ii)) passes — selection explains the aggregate gap, yet gaming-labeled patches still rise as adequacy falls — the adaptive-exploitation claim (Claim 6) falls and the gaming-fraction result (Claim 5) is downgraded to the pre-worded finding that gaming-shaped patches arise at higher rates under degraded adequacy even without iterative feedback, with the tension between the two arms reported as a finding after checking the harness's feedback-use logs (Assumption A3), the usual culprit when the two arms disagree.

**Result.** *[placeholder — fill in after experiments are run]*

---

## Cross-check against Stage 6's confirmed tier accounting

8 mechanism-tier RQs, 0 framing-tier, 0 outcome-tier — matches `pipeline.md` Stage 6 header exactly. Every `target_hypotheses` above traces 1:1 to a Stage 5 hypothesis id (`m_adequacy_sampler` ×2, `m_trend_model` ×1, `m_curve_shape_estimator` ×1, `m_differential_diagnostic` ×2, `m_transfer_harness` ×1, `m_selection_control` ×1 = 8), per `pipeline.md`'s own cross-stage consistency check. RQ5 and RQ8 are flagged above as post-Stage-6 revisions rather than silently presented as Stage 6's original text, so the audit trail in `discussion_trace.md` and this document stay reconcilable.
