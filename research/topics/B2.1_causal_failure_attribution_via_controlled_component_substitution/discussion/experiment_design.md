# Experiment Design — B2.1: Causal Failure Attribution via Controlled Component Substitution

> Standalone protocol document, per the updated `auto-research-discussion` skill's three-artifact
> deliverable split. This is Stage 6's confirmed output (`discussion/discussion_trace.md` → "##
> Stage 6 — Experiment Design") rendered as a document runnable without opening the paper, with
> setup/sample-size/statistical-test detail carried in from `../paper.md`'s own pre-registered
> Step 6 (E1–E4, Assumptions A1–A6, Mandatory baselines, Power statement). Nothing below is
> invented — every number and procedure traces to `discussion_trace.md`'s Stage 5/6 or to
> `../paper.md`. Status: **specification — no experiments have been run; all numbers are
> pre-registered design targets, not results.**
>
> **Tier accounting (from Stage 6, checked against `study_type = empirical`):** mechanism-tier 7
> RQs (one per Stage 5 hypothesis, verbatim `target_hypotheses`); framing-tier 0 RQs (no Stage 3
> limitation was flagged `verify_as_hypothesis`); outcome-tier 0 RQs (`study_type = empirical`
> forbids "our procedure beats baseline X" framing — the candidate attribution methods are the
> population being characterized, not competitors this paper is trying to beat).
>
> Keep this file synchronized with `paper_draft.md`'s Experiments section and `../paper.md`'s Step
> 6 if either is edited later.

## Datasets

- **GAIA-style tool-use tasks** — supplies the base task pool from which reproducibly-succeeding
  runs are selected for injection; realistic multi-step tool-use scenarios are what makes the
  substitution protocol's findings relevant to deployed agents. Reproducibility gate (Assumption
  A1): ≥ 60 base tasks must succeed in ≥ 4 of k = 5 temperature-0 replays; yield < 30 tasks
  triggers one pre-registered scaffold redesign (Gate PG-1), then a single re-run of Stage 0 —
  persistent failure routes to the global fallback (F-G1).
- **Who&When** (naturally-failing, human-labeled multi-agent trajectories) — a naturally-failing,
  human-labeled comparison set; contrasts this paper's construction-based labels against
  human-annotated ones and directly addresses the threat that injected faults might not represent
  naturally-occurring failure distributions. Also supplies the LLM-judge's three context-strategy
  prompts (all-at-once / step-by-step / binary-search).
- **The constructed injected-fault corpus** (this work's own output of the fault injection library
  + outcome-flip certification gate) — the paper's own released artifact; every RQ below is
  computed over it. Released in versioned tiers keyed to scaffold and backbone
  (`corpus-v1-<scaffold>-<backbone-id>`), with at least one tier built on a pinned open-weights
  backbone so re-certification and intervention baselines remain runnable after any API model is
  retired.
- **Held-out/paraphrased subset** (contamination control, B-alt-2) — a held-out subset of ≥ 30 base
  tasks not present in the benchmark's public release, or task instances with surface-paraphrased
  wording that breaks exact-string memorization, scored separately in E2–E4 to rule out
  memorized-task-familiarity as an alternative explanation for post-hoc-judge accuracy.

## Baselines / comparators (sanity-check comparators, not outcome-tier competitors)

This is a benchmark-construction and measurement study (`study_type = empirical`): no research
question below is framed as "our procedure beats baseline X." The candidate attribution methods
are the population being characterized.

- **WhoAndWhen LLM-judge** — post-hoc explanation approach, applied under all three context
  strategies (all-at-once / step-by-step / binary-search); the standard post-hoc explanation
  approach being characterized.
- **Ablation / leave-one-out blame** — re-run with each component reset to its known-good state;
  observe which restoration flips the outcome back to success.
- **DoVer-style intervention do-then-verify** — the standard interventionist comparator.
- **FAPO/CRM-style step-level localizer** — repurposed from single-agent reasoning to this
  multi-component setting; tests whether a method built for a different granularity transfers.
- **AgenTracer RL tracer** — conditional inclusion only: runnable as an accuracy comparator only if
  its trained tracer's weights or prompts are publicly released (Assumption A6, Gate PG-6,
  one-trajectory smoke test); if not, it is retained purely as the design precedent for the
  outcome-flip labeling trick and dropped from the accuracy-comparison table with a stated
  availability note.
- **B0-a — class-matched no-op substitution arms + identity-replay arm** — `δ_∅^c` for each
  c ∈ {plan, tool, obs} (n ≥ 100 each), swapping component c for an equivalent good copy via the
  *same edit pathway* as that class's fault injection, plus a zero-tier identity-replay arm `δ_id`
  (n ≥ 100, no edit at all, same-checkpoint replay). Justifies RQ2's existence (if `δ_∅^c` flips
  outcomes as often as real faults, "failure tracks the component" is unmeasurable) and lets
  RQ3 disambiguate *why* a flip occurred — edit-pathway artifact vs. intrinsic stochasticity
  (Assumption A4 / Gate PG-4's tiered rule). Both generators validated by a 5-step
  instrument-validation protocol (guidance.md §3.4 R2) against ≥ 2 independent human raters on a
  50-swap calibration slice, requiring κ ≥ 0.7 and ≥ 95% swaps rated equivalent.
- **B0-b — surface-heuristic attributor** — blames the component hosting the last step before the
  first observable error signal, detected by a frozen deterministic rule set (tool-return
  status/error fields, empty/schema-invalid payloads, fixed exception-string patterns); no LLM
  call, no human judgment. Justifies RQ4's existence (if this trivial heuristic already matches
  ground truth at ≥ 0.90, single-fault attribution at this severity tier is symptom-reading and no
  method-ranking benchmark is needed there — routes to combination rule CR-1). Random and
  majority-class attributors are also reported alongside it. Validated the same 5-step way against
  ≥ 2 raters on a 50-trajectory calibration slice, κ ≥ 0.7 required.
- **B-alt — budget-matched post-hoc judge** — the compute-parity control isolating
  causal-intervention access from raw replay budget: the LLM-judge granted the same replay budget
  (k additional sampled trajectories of the same failing run, provided as text) and
  self-consistency voting, so total model-calls and observable evidence are matched to the
  intervention arm. Directly targets RQ5.

## Research Questions

Each RQ's *target hypothesis* below is quoted verbatim from Stage 5's confirmed hypotheses as
carried into Stage 6's `research_questions` table (`discussion_trace.md`, "## Stage 6 — Experiment
Design"); wording is not paraphrased. Setup/sample-size/statistical-test/expected-outcome/metrics
detail is carried in from `../paper.md`'s corresponding pre-registered experiment (E1–E4),
Assumptions (A1–A6), Mandatory baselines, and Power statement sections, and cross-checked against
`paper_draft.md`'s already-assembled Experiments section (RQ1–RQ7), which restates the same design
targets in reader-facing prose.

---

### RQ1 — `rq_label_audit_agreement`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_label_construction`.
- **Target hypothesis (verbatim, Stage 5 `m_fault_injection_library`):** "Human auditors will agree
  with the constructed ground-truth failure-locus label for at least 80% of a sampled 200-trajectory
  audit set, per fault category."
- **Setup.** A sample of 200 certified trajectories, balanced across the three fault categories, is
  shown to independent human raters without the injected-component label; raters identify which
  component they judge responsible. Per Assumption A5's 5-step instrument-validation sequence
  (Gate PG-5, pre-Stage-2 scale-up): (1) categories are already grounded in the pipeline's own
  architecture (plan/tool/obs = K, not an invented taxonomy); (2) the fault-template library is
  drafted wide and refined on a held-out calibration subset before the full audit sample is drawn;
  (3) validated against ≥ 2 independent human raters; (4) the confusion structure is inspected —
  disagreements must land on adjacent classes (e.g., tool/observation), not a systematic three-way
  collapse; (5) the taxonomy is frozen (hashed) before Stage-2 scale-up.
- **Sample-size rationale.** 200-trajectory audit sample, balanced across the three fault
  categories (Assumption A5).
- **Statistical test.** Two readouts, both pre-registered: (a) raw human-label agreement rate with
  the constructed label, overall and per fault category (the Stage-5 hypothesis's own 80% target);
  (b) Cohen's/Fleiss' κ between raters and against the constructed label — not raw percent
  agreement alone, which overstates chance-corrected agreement (Assumption A5) — required
  κ ≥ 0.7.
- **Expected outcome.** Human auditors agree with the constructed label for at least 80% of the
  sampled trajectories, per fault category, with κ ≥ 0.7 against the constructed label;
  disagreement below this threshold, or systematic (non-adjacent) confusion, in a given category
  triggers re-examination of that category's fault templates (re-taxonomization per guidance.md
  situation 7) before any further release.
- **Metrics.** Human-label agreement rate, overall and per fault category; Cohen's/Fleiss' κ.

---

### RQ2 — `rq_component_flip_tracking`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_causal_entanglement`.
- **Target hypothesis (verbatim, Stage 5 `m_substitution_harness`):** "For each of the three fault
  classes, the outcome-flip rate under substitution will exceed the matched no-op control's flip
  rate by at least 0.20 (absolute), each significant at α = 0.05 after correction across the three
  classes."
- **Setup.** For each of the three fault classes, at least 100 injection trials and at least 100
  class-matched no-op-substitution trials (`δ_∅^c`, via the same edit pathway as that class's
  injection) are run, plus at least 100 identity-replay trials (`δ_id`), each replayed k = 4 times
  from a checkpoint on a reproducibly-succeeding base run (Assumptions A1–A4).
- **Sample-size rationale.** n ≥ 100 injection + n ≥ 100 class-matched no-op trials per class gives
  > 0.9 power for the significance component at the design alternative (true gap 0.30 vs. base
  rate 0.10) under trial independence. Because the pass criterion is a conjunction (point-estimate
  gap ≥ 0.20 **and** significance), the pass probability at a true gap of exactly 0.20 is ≈ 0.5 by
  symmetry — the design is powered against the 0.30 design alternative, not the floor. Per-class
  power under base-task clustering is re-computed by cluster-bootstrap simulation on the
  walking-skeleton pilot before Stage-1 scoring, thresholds frozen first; a class whose simulated
  power < 0.8 is pre-declared INCONCLUSIVE, never scored as null.
- **Statistical test.** Two-proportion comparison of flip rate under `δ_c` vs. `δ_∅^c`, with
  cluster-robust inference at the base-task level (trials sharing a base task form one cluster;
  equivalently a cluster bootstrap of the rate difference resampling base tasks); one-sided,
  α = 0.05, Benjamini–Hochberg corrected across the 3 classes; 95% cluster-bootstrap CIs reported
  on all rates.
- **Expected outcome.** Each fault class's flip rate exceeds the no-op control's flip rate by at
  least 0.20 absolute, with the gap statistically significant after correction. A class that does
  not clear this margin is reported as *uncertified* rather than merged into the certified set
  (pre-committed pattern-neutral fallback wording in `../paper.md` E1) — consistent with the
  possibility that some fault types (plan-level corruption in particular) propagate too diffusely
  to certify at this replay depth, though a reversed pattern is reported at full prominence, not
  smoothed into the expected wording. If no class passes even after one pre-registered k↑ retry,
  the design routes to the global fallback F-G1.
- **Metrics.** Per-class outcome-flip rate and its gap over the no-op control, with 95%
  cluster-bootstrap CIs.

---

### RQ3 — `rq_noop_stochasticity_bound`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_substitution_confound`.
- **Target hypothesis (verbatim, Stage 5 `m_outcome_flip_gate`):** "The no-op control's own
  outcome-flip rate will remain at or below 0.10 under k = 4 replays at temperature 0, confirming
  that background stochasticity alone does not manufacture false-positive labels."
- **Setup.** The same class-matched no-op-substitution trials used in RQ2's control arm (`δ_∅^c`,
  n ≥ 100/class) are examined on their own, alongside the zero-tier identity-replay arm (`δ_id`,
  n ≥ 100, no edit at all, same-checkpoint replay) that lets Gate PG-4 disambiguate *why* a flip
  occurred.
- **Sample-size rationale.** Shares the n ≥ 100 per-class no-op trial count with RQ2; the
  walking-skeleton pilot (Step 9) checks a coarse version of this bound first (identity-replay
  flips ≤ 1 of survivors) before full-scale scoring.
- **Statistical test.** Flip rate estimated with a 95% bootstrap CI and compared against a
  pre-registered upper bound: `δ_∅^c` ≤ 0.10 per class, `δ_id` ≤ 0.05 for the identity tier
  (Assumption A4). Disambiguation rule (Gate PG-4, tiered): if `δ_id` passes but some `δ_∅^c`
  fails, the *edit pathway* is the artifact — a harness bug, fixed and the skeleton re-run, never
  scored as a finding; if `δ_id` itself fails, it indicates intrinsic stochasticity — one
  pre-registered k↑ retry (to k = 8), then routes to the global fallback F-G1.
- **Expected outcome.** The no-op control's flip rate remains at or below 0.10 (and the identity
  tier at or below 0.05); a rate above either bound indicates the substitution-and-replay procedure
  itself is chaotically sensitive (or the edit pathway itself disturbs outcomes), undermining every
  certified label built on top of it.
- **Metrics.** No-op control flip rate per class, with 95% bootstrap CI; identity-replay flip rate.

---

### RQ4 — `rq_floor_beat`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_causal_distance`.
- **Target hypothesis (verbatim, Stage 5 `m_attribution_battery`):** "Each non-trivial attribution
  method family will exceed the surface-heuristic floor's accuracy by at least 0.10 absolute on the
  certified corpus."
- **Setup.** Computed only over the certified tier established by RQ2's per-class flip-rate check;
  an uncertified fault class is excluded from this pool rather than silently included. Each
  non-trivial method (LLM-judge under 3 context strategies, ablation/leave-one-out, DoVer-style
  intervention, FAPO/CRM-style step-localizer) is scored against the B0-b surface-heuristic floor.
  H2 passes iff ≥ 3 of the runnable method families pass (all-but-one, ≥ 2 of 3, if Gate PG-6
  leaves only 3 runnable families; with ≤ 2 runnable families the result is pre-declared
  INCONCLUSIVE). If `Acc(B0-b) ≥ 0.90` on the certified tier, this RQ is instead scored under
  combination rule CR-1 (heuristic-ceiling branch).
- **Sample-size rationale.** Stage-1 target n ≈ 300 certified trajectories (~100/class); Stage-2
  n ≈ 3,000 (~1,000/class). Powered-cell rule: a per-class/per-method cell needs ≥ 80 certified
  trajectories as a *necessary* condition (≥ 0.8 power under independence for a 0.10 absolute
  accuracy gap via McNemar-style paired test at α = 0.05); the *binding* check is a
  cluster-bootstrap power simulation run on the walking-skeleton pilot's observed base-task
  clustering, thresholds frozen before Stage-1 scoring — a cell is powered iff simulated power
  ≥ 0.8. Any cell failing either check is pre-declared INCONCLUSIVE for that class — never scored
  as null, never silently dropped from the denominator.
- **Statistical test.** McNemar-style test on paired correct/incorrect outcomes vs. B0-b, with
  base-task-cluster-robust inference (cluster bootstrap of the paired accuracy difference
  resampling base tasks), α = 0.05 with Benjamini–Hochberg correction across the full
  method × fault-category grid.
- **Expected outcome.** Each non-trivial method family exceeds the floor's accuracy by at least
  0.10 absolute on the certified corpus. If `Acc(B0-b) < 0.90` and this margin is not cleared, the
  pre-committed negative finding is: "On causally certified labels, current attribution methods do
  not exceed a trivial surface heuristic... indicating those labels reward symptom-matching rather
  than causal localization" (`../paper.md` E2 fallback) — reported as-is, not softened.
- **Metrics.** Per-method accuracy and its gap over the floor, with 95% bootstrap CIs; full 3×3
  confusion matrices reported for every method regardless of outcome.

---

### RQ5 — `rq_compute_parity_control`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_causal_distance`.
- **Target hypothesis (verbatim, Stage 5 `m_attribution_battery`, second hypothesis):** "The
  accuracy advantage of intervention-based methods over post-hoc judges will narrow to below 0.10
  absolute once the judge is given an equal replay budget of passive resamples (the budget-matched
  control) — i.e., intervention access adds no attribution accuracy beyond an equal budget of
  passive resampling."
- **Setup.** Computed only over the certified tier. The B-alt budget-matched post-hoc judge
  variant (same replay budget of additional sampled resamples as the intervention arm, self-
  consistency voting, no intervention access) is compared against the standard DoVer-style
  intervention method.
- **Sample-size rationale.** Shares the certified-tier n with RQ4 (Stage-1 n ≈ 300, Stage-2
  n ≈ 3,000) and the same powered-cell rule (≥ 80 certified trajectories/cell necessary;
  cluster-bootstrap simulated power ≥ 0.8 binding).
- **Statistical test.** Paired bootstrap difference test on accuracy between the intervention-based
  method and its budget-matched judge counterpart, base-task-cluster-robust, Benjamini–Hochberg
  corrected alongside RQ4's method × fault-category grid.
- **Expected outcome.** The accuracy gap between the intervention-based method and the
  budget-matched judge narrows to below 0.10 absolute, indicating that at least part of any raw
  advantage for intervention-based methods reflects extra compute rather than causal-intervention
  access specifically. If it closes, the paper's claim about do-then-verify narrows to a
  compute-parity statement: "Intervention access adds no attribution accuracy beyond an equal
  budget of passive resamples" (`../paper.md` B-alt, pre-committed wording).
- **Metrics.** Accuracy gap between the intervention-based method and its budget-matched judge
  counterpart, with bootstrap CI.

---

### RQ6 — `rq_ceiling_gap`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_causal_distance`.
- **Target hypothesis (verbatim, Stage 5 `m_verification_scorer`):** "The best-performing
  attribution method's overall accuracy will not exceed 0.90, with a 95% bootstrap CI upper bound
  below 0.95."
- **Setup.** Computed only over the certified tier established by RQ2 — this RQ's setup explicitly
  states the dependency added in Stage 6's refiner pass: a fault class that fails certification is
  excluded from this RQ's accuracy pool rather than silently included. Requires RQ2 (E1) to have
  passed. The best-performing method's overall accuracy across certified fault classes is
  estimated; B0-b is excluded from the max and reported separately as the heuristic-sufficiency
  rate.
- **Sample-size rationale.** Stage-1 n ≈ 300, confirmed at Stage-2 n ≈ 3,000; same powered-cell
  rule as RQ4/RQ5.
- **Statistical test.** Cluster bootstrap CI (10,000 resamples, resampling base tasks rather than
  trials) on the best method's accuracy.
- **Expected outcome.** The best-performing method's accuracy does not exceed 0.90, with the CI's
  upper bound below 0.95 — a measurable gap remains below the by-construction ceiling of 1.0. If
  instead the ceiling is already reached, the pre-committed fallback reframes the certified tier as
  "a competence certificate rather than an open challenge" and releases a harder single-fault tier
  at ≤ 25% of the Stage-2 injection budget (`../paper.md` E3 fallback).
- **Metrics.** Best-method overall accuracy with 95% bootstrap CI; per-class accuracies; B0-b's
  heuristic-sufficiency rate reported separately.

---

### RQ7 — `rq_plan_tool_asymmetry`

- **Tier:** Mechanism-tier.
- **Target sub-problem:** `sp_causal_distance`.
- **Target hypothesis (verbatim, Stage 5 `m_verification_scorer`, second hypothesis):** "For the
  post-hoc judge family specifically, accuracy on plan-level faults will be at least 0.10 lower
  than on tool-level faults, reflecting the more diffuse causal propagation of plan-corruption
  effects."
- **Setup.** Computed only over the certified tier; requires RQ2 and RQ4 (E1–E2) to have passed.
  For the LLM-judge family, accuracy conditioned on plan-level faults is compared against accuracy
  conditioned on tool-level faults, on **severity-matched template pairs** (plan and tool templates
  at the same pre-registered severity level) to control for the possibility that certification
  selects different surviving severity distributions per class (severity confound, R3);
  `Acc(B0-b | ℓ = c)` is reported per class alongside as a difficulty proxy. If the gap vanishes
  under severity matching, the claim is downgraded to a severity effect: "The apparent plan-fault
  difficulty is carried by fault severity composition, not by fault class itself"
  (`../paper.md` E4, pre-committed wording).
- **Sample-size rationale.** Shares the certified-tier n and powered-cell rule with RQ4/RQ6.
- **Statistical test.** Class-conditional cluster-bootstrap difference test (resampling base
  tasks), Benjamini–Hochberg corrected alongside RQ4's method × fault-category grid.
- **Expected outcome.** The post-hoc judge family's accuracy on plan-level faults is at least 0.10
  lower than on tool-level faults, consistent with plan-corruption effects propagating more
  diffusely through the trajectory before manifesting as a visible failure. A significant
  **reversed** ordering is not folded into the null wording — it is reported at full prominence
  with the pre-committed sentence: "Plan-fault attribution is more accurate than tool-fault
  attribution for post-hoc judges — the opposite of the propagation-diffuseness prediction —
  indicating that error-signal salience, not causal distance, drives judge accuracy" (`../paper.md`
  CR-5).
- **Metrics.** Class-conditional accuracy gap (plan vs. tool) for the post-hoc judge family, with
  bootstrap CI; `Acc(B0-b | ℓ = c)` per class as a difficulty proxy.

---

## Cross-cutting notes carried from `../paper.md`'s Step 6 (apply to all RQs above)

- **Cluster-robust inference throughout.** All E1–E4/RQ1–RQ7 inference is cluster-robust at the
  base-task level (Stage 2 generates ~3,000 trials from only ~200 base tasks, so the effective
  sample size is the cluster count, not the trial count); every test uses cluster-robust variance
  or a cluster bootstrap resampling base tasks, and every CI is a cluster-bootstrap CI.
- **Contamination control (B-alt-2).** Because base tasks are drawn from a publicly released
  benchmark, RQ4–RQ7 are additionally scored on the held-out/paraphrased subset (≥ 30 tasks); a
  method whose accuracy falls ≥ 10 points below its full-corpus accuracy on that subset has its
  headline accuracy reported as memorization-assisted, with only the held-out accuracy treated as
  evidence of causal attribution ability.
- **Fallback-combination rules (CR-1–CR-5, pre-committed, never invented at verdict time).**
  CR-1 (heuristic-ceiling branch) supersedes RQ4/RQ6's individual fallback wording whenever
  `Acc(B0-b) ≥ 0.90`; CR-2 governs RQ4–RQ7 wording within the certified tier when RQ2 partially
  passes; CR-3/CR-4 govern the RQ4-fails/RQ6-fails-or-passes combinations; CR-5 governs any
  wrong-direction (reversed) result. The global fallback F-G1 (pivot to a negative-result
  measurement study) supersedes all CR rules and fires on: RQ2 failing on all classes even after
  one k↑ retry; the identity-tier bound (RQ3) failing even after one k↑ retry; or fewer than 30
  reproducibly-solved base tasks even after one scaffold redesign.
- **Release discipline.** The corpus is released in versioned tiers keyed to scaffold and backbone;
  post-hoc methods are evaluable from released trajectories alone, intervention-based methods
  require live checkpoint-replay and are certified per backbone.
