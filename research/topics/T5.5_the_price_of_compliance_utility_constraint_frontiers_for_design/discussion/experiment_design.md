# Experiment Design — The Price of Compliance (T5.5)

> Standalone protocol document, per `auto-research-discussion`'s Final-deliverables spec.
> Built from Stage 6's confirmed output in `pipeline.md` (§"Stage 6 — Experiment Design")
> and `paper.md`'s own Step 5/Step 6 pre-registered experiment content. Nothing below is
> invented beyond what those two sources already contain; sample-size and statistical-test
> detail not spelled out verbatim in the Stage 6 table is pulled from `paper.md`'s Step 5
> notation and Step 6 E1–E4 verification blocks, which the Stage 6 refiner pass explicitly
> designated as the source for this material ("reusing paper.md's already-designed E1–E4
> numbers as authored design targets, not fabricated results" — `pipeline.md` line 207).
> Status: **specification — no experiments have been run.** Every number below is a
> pre-registered design target, not a result.
>
> **Tier accounting** (checked against `study_type = empirical` in `pipeline.md` Stage 6):
> Mechanism-tier — 8 RQs, one per Stage 5 hypothesis, verbatim `target_hypotheses`.
> Framing-tier — 0 RQs (no Stage 3 limitation was flagged `verify_as_hypothesis`).
> Outcome-tier — 0 RQs (`empirical` study type forbids "our procedure beats baseline X"
> framing; all baselines below are sanity-check comparators and confound controls only).

## Datasets

- **BigCodeBench-Hard-style function-level suite** (≈150 tasks, executable unit-test
  oracles). *Justification:* cheap, high-n substrate for the pilot ladder sweep (`n = 150
  tasks × 5 samples = 750 attempts` per level/model/arm cell) that establishes the
  pass-rate/cost trend before scale-up budget is committed (`paper.md` Step 5 notation;
  E1 verification block).
- **SWE-bench Verified-style repository-level subset** (50 tasks, per-repository mapping
  of applicable catalog rules). *Justification:* required, not merely realistic, for the
  catalog fidelity/bindingness audit (RQ1) to apply to the catalog's repository-level
  rules at all — import-layering, dependency-direction, and dependency-injection rules
  have no multi-file structure to bind against on function-level BigCodeBench-Hard tasks,
  so without this suite the bindingness screen would silently exempt the architectural
  rule subset from ever being tested. Also lets RQ6 (breadth vs. strictness) and RQ7
  (mechanism share) be checked for generalization beyond function-level scope
  (`pipeline.md` Stage 6 refiner pass).
- **Contamination check** (carried from `paper_draft.md`'s Experimental Setup, not in
  the original Stage 6 table but consistent with it): per-task pass rates stratified by
  each task's public release date relative to each tested model's documented training
  cutoff where available; the dual-criterion shape test (RQ4/RQ5) is re-run excluding any
  task subset flagged as likely-memorized (near-ceiling Pass@1 at zero constraint
  strength across all tested models), and both analyses are reported if the verdict
  changes materially.

## Baselines (sanity-check comparators and confound controls — not outcome-tier competitors)

- **L0 / unconstrained arm (B0)** — anchors the utility ceiling and the CCS denominator
  for every hypothesis; doubles as the bindingness-screen control (rule is binding iff
  ≥5% of L0 generations violate it). If macro L0 violation rate < 5%, there is no
  compliance problem to price and the study halts at the walking skeleton.
- **Binary all-or-nothing enforcement arm** — the naive deployment policy the graded,
  multi-level sweep is compared against, to show the graded design adds information a
  single all-on run would not.
- **Length-matched placebo prompt (B-alt)** — semantically inert instructions,
  token-count-matched in position and formatting to the rendered rule set at each
  strength level; isolates instruction-load effects from constraint-content effects
  (RQ8). Rival explanation it rules out: degradation is caused by instruction load per
  se, not by what the constraints say.
- **External anchor (qualitative only)** — FollowBench's / RECAST's satisfaction-only
  degradation curves, compared qualitatively since their axes lack a pass-rate/cost
  dimension (per `lim_ifeval_followbench_no_utility_axis` / `lim_recast_autoif_construct_narrow`
  in `pipeline.md` Stage 3) and are not run under this paper's conditions.

---

## RQ1 — Catalog fidelity and bindingness

- **Tier:** Mechanism-tier (targets `sp_operationalization_validity`, method
  `m_bindingness_kappa_catalog`).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 150 & 198):** "No more than
  40% of the initial ~20-rule catalog will be dropped for κ < 0.8 or replaced for failing
  the bindingness screen, and — among whatever is dropped — drops will concentrate in
  rules targeting architectural/cohesion judgment calls rather than mechanical categories
  (naming, complexity thresholds), consistent with the harder-to-checkify categories
  being where fidelity risk actually lives rather than drops being randomly distributed
  across rule types."
- **Setup:** The initial ~20-rule catalog (import-layering/dependency-direction
  contracts, complexity/length ceilings, naming/visibility conventions, forbidden-API
  lists, dependency-injection mandates) is audited on a stratified 100-sample subset by
  2 human annotators labeling each flagged instance as genuine violation vs. checker
  artifact. Independently, any rule violated by <5% of unconstrained (L0) generations is
  screened as non-binding and replaced.
- **Sample-size rationale:** 100-sample stratified subset (`paper.md` Step 5 "valid
  checker" row) — the audit sample size fixed by the inter-rater-agreement design, not
  by the pilot/scale-up attempt budget.
- **Statistical test:** Cohen's κ per rule vs. 2 human annotators; pre-registered
  decision threshold κ ≥ 0.8 (rules below are dropped); bindingness screen is a
  pre-registered proportion threshold (<5% of L0 generations), not a significance test.
- **Expected outcome:** No more than 40% of the initial catalog is dropped or replaced
  overall, and the drops that do occur concentrate in architectural-intent categories
  rather than being spread uniformly across rule types.
- **Metrics:** Proportion of catalog dropped/replaced; category breakdown of drops
  (mechanical vs. architectural).

## RQ2 — Pilot trade-off magnitude

- **Tier:** Mechanism-tier (targets `sp_signal_variance`, method
  `m_matched_condition_power_model`).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 151 & 199):** "From L0 to
  L4 (pilot ladder, prompt-only arm), Pass@1(L4) ≤ Pass@1(L0) − 5 percentage points with
  mixed-effects strength coefficient OR < 0.90 per step (Holm-adjusted p < 0.05) AND
  cost-per-compliant-solved-task CCS(L4) ≥ 1.25 × CCS(L0), holding for ≥ 2 of 3 scale-up
  models."
- **Setup:** One mid-tier model, pilot ladder L0–L4 (cumulative rule packs, fixed
  strictness), prompt-only enforcement arm.
- **Sample-size rationale:** n = 150 tasks × 5 samples = 750 attempts per (level, model,
  arm) cell (`paper.md` E1 verification block) — fixed pilot budget, later checked for
  adequacy by RQ3's power analysis rather than assumed sufficient.
- **Statistical test:** Mixed-effects logistic regression of per-attempt pass on strength
  level (task-level random intercept); Cochran–Armitage trend test across levels;
  α = 0.05, Holm-corrected across models × arms.
- **Expected outcome:** Pass@1 at maximum pilot strength is ≥5pp below the unconstrained
  baseline with a significant negative strength coefficient, and CCS at maximum strength
  is ≥25% above the unconstrained baseline, holding for ≥2 of 3 scale-up models.
- **Metrics:** Pass@1, V, CP, CCS (Step 5 metrics group); mixed-effects strength
  coefficient and confidence interval; CCS ratio at max vs. zero strength.

## RQ3 — Power pre-commitment

- **Tier:** Mechanism-tier (targets `sp_signal_variance`, method
  `m_matched_condition_power_model` — second readout of the same fitted model as RQ2).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 151 & 200):** "If the
  pilot's observed effect size corresponds to less than 80% power for the 5pp pass-rate
  margin, the scale-up sample size per cell is pre-committed to increase according to the
  observed variance, rather than the pilot's null result being reported as evidence that
  compliance is 'approximately free.'"
- **Setup:** A post-pilot power analysis on the observed per-cell variance from RQ2's
  fitted mixed-effects model, run before any scale-up sample size is finalized.
- **Sample-size rationale:** No new sample — this RQ is a instrument-validity check
  computed on RQ2's pilot data (one fitted model, two readouts: the headline magnitude
  claim in RQ2 and the power-precommitment claim here, per the Stage 5 refiner's
  one-instrument-two-estimands justification, `pipeline.md` lines 165–166).
- **Statistical test:** Post-hoc power calculation for the pre-specified 5-percentage-point
  pass-rate margin, against the pre-specified 80% power threshold.
- **Expected outcome:** If observed power for the 5pp margin falls below 80%, the
  pre-committed sample-size enlargement rule fires for the scale-up rather than the
  pilot's result being reported as a null "graceful"/"free" finding. Any (model, level,
  arm) cell still below 80% power after the one-time enlargement is pre-declared
  **INCONCLUSIVE** for every hypothesis that reads it — excluded from PASS/FAIL
  aggregation numerators and denominators, never counted as a null result (`paper.md`
  A6 / gate PG-5).
- **Metrics:** Observed effect size and corresponding power for the 5pp margin; whether
  the enlargement rule fired.

## RQ4 — Knee existence

- **Tier:** Mechanism-tier (targets `sp_shape_detectability`, method
  `m_dual_criterion_breakpoint`).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 152 & 201):** "Under the
  checker-in-the-loop retry arm, a knee (both Davies p < 0.05 and ΔAIC > 4) exists for at
  least 2 of 3 scale-up models."
- **Setup:** Scale-up data (3 models, 3×3 breadth×strictness factorial grid, 3
  enforcement arms, + SWE-bench Verified suite), checker-in-the-loop retry arm. Linear
  and segmented (piecewise-linear) regressions of Pass@1 vs. strength are fit per model.
- **Sample-size rationale:** Scale-up factorial grid (3×3) × 3 models × 3 arms +
  SWE-bench suite (`paper.md` Step 9 walking-skeleton scale-up description); knee-location
  CI computed via 1,000 task-level bootstrap resamples (`paper.md` Step 5 "knee consistent
  across models" row).
- **Statistical test:** Davies test for a change point (p < 0.05) AND ΔAIC (linear −
  segmented) > 4, jointly required, plus `paper.md` H2's pre-registered effect floor:
  the segmented fit's post-breakpoint slope must be ≥ 2× its pre-breakpoint slope in
  absolute pp-per-level terms — a statistically detected breakpoint below this ratio is
  reported as **graceful-with-inflection**, not scored as a knee; knee location reported
  with 95% bootstrap CI.
- **Expected outcome:** A knee (both criteria jointly satisfied and the slope-ratio
  effect floor met) exists for a majority (≥2 of 3) of tested models under the retry
  arm, with overlapping knee-location confidence intervals across models exhibiting a
  knee.
- **Metrics:** Per-model knee-existence verdict; knee location σ* and bootstrap CI;
  cross-model interval overlap.

## RQ5 — Cross-axis shape agreement

- **Tier:** Mechanism-tier (targets `sp_shape_detectability`, method
  `m_dual_criterion_breakpoint` — same instrument as RQ4, second axis).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 152 & 202):** "The
  pass-rate-based and cost-based dual-criterion verdicts will agree (both graceful or
  both knee) for at least 2 of 3 models; where they disagree, the cell is reported as
  shape-discordant rather than one axis being treated as authoritative."
- **Setup:** The identical dual-criterion procedure from RQ4 applied independently to the
  log-CCS-vs-strength curve, per model × arm; verdict compared directly against RQ4's
  pass-rate-based verdict for the same cell.
- **Sample-size rationale:** Same scale-up dataset as RQ4 — no additional sampling; this
  RQ reuses RQ4's fitted curves on the cost axis.
- **Statistical test:** Davies test + ΔAIC dual criterion applied to log-CCS vs. strength,
  with the same ≥2× post-/pre-breakpoint slope-ratio effect floor as RQ4 (the identical
  dual-criterion-plus-slope-floor procedure, per `paper.md` H2c); direct
  agreement/disagreement comparison against the pass-rate verdict.
- **Expected outcome:** The two verdicts agree (both graceful or both knee) for ≥2 of 3
  models; disagreeing cells are reported as shape-discordant.
- **Metrics:** Cross-axis verdict agreement rate; identity and count of shape-discordant
  cells.

## RQ6 — Breadth vs. strictness

- **Tier:** Mechanism-tier (targets `sp_strength_dimensionality`, method
  `m_factorial_grid`).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 153 & 203):** "Breadth's
  main effect on pass-rate odds ratio (per level) will exceed strictness's main effect in
  magnitude at matched ladder position — i.e., adding more distinct rules costs more pass
  rate than tightening thresholds on already-active rules — in at least 2 of 3 models."
- **Setup:** Scale-up 3(breadth) × 3(strictness) factorial grid, σ = (b,s) ∈ {1,2,3} ×
  {1,2,3} plus σ₀ = L0; main effects and interaction read from the mixed-effects model.
- **Sample-size rationale:** Same scale-up factorial-grid budget as RQ4/RQ7 (3 models ×
  3×3 grid × arms); no separate sample beyond the scale-up allocation.
- **Statistical test:** Mixed-effects model with breadth and strictness as crossed
  factors; per-axis main-effect estimate and confidence interval, Holm-corrected across
  models.
- **Expected outcome:** Breadth's main effect exceeds strictness's main effect in
  magnitude for ≥2 of 3 tested models.
- **Metrics:** Per-axis main-effect estimate and CI; effect-size comparison between axes.

## RQ7 — Mechanism share

- **Tier:** Mechanism-tier (targets `sp_mechanism_attribution`, method
  `m_arm_interaction_decomposition`).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 154 & 204):** "The
  retry-arm log-cost slope will exceed 1.5× the prompt-only log-cost slope at the top
  strength tier (super-proportional retry cost), and the arm × strength interaction term
  will be significant (Holm-adjusted p < 0.05) with mechanism share MS ≥ 0.30 at that
  tier, in at least 2 of 3 models."
- **Setup:** Identical constraint grids run under all three enforcement arms (P/R/B) with
  disaggregated cost logging (prompt-overhead tokens, retry tokens, output-inflation
  tokens); mechanism share MS(σ) = [CCS_retry(σ) − CCS_prompt(σ)] / [CCS_retry(σ) −
  CCS(L0)], computed only for cells where the retry arm's cost premium over baseline
  exceeds a pre-specified floor (below-floor cells reported as mechanism-share
  undefined).
- **Sample-size rationale:** Same scale-up allocation as RQ4/RQ6 (3 models × factorial
  grid × 3 arms); cost is logged per attempt already collected for the pass-rate
  analyses, no additional sampling required.
- **Statistical test:** Two-way (arm × strength) mixed-effects model on log-cost;
  interaction-term significance test, Holm-corrected across models × arms.
- **Expected outcome:** At the top strength tier, retry-arm log-cost slope exceeds 1.5×
  the prompt-only slope, the interaction is significant, and mechanism share ≥0.30 in
  qualifying cells, for ≥2 of 3 models.
- **Metrics:** Arm × strength interaction estimate; mechanism-share statistic in
  qualifying cells; log-cost slope ratio (retry/prompt-only).

## RQ8 — Instruction-load control

- **Tier:** Mechanism-tier (targets `sp_instruction_load_confound`, method
  `m_length_matched_placebo`).
- **Target hypothesis (verbatim, Stage 5 / `pipeline.md` line 155 & 205):** "The
  constraint arm's strength effect on pass exceeds the length-matched placebo arm's
  strength effect by at least 3 percentage points at maximum strength (Holm-adjusted
  interaction test, p < 0.05); if this margin is not met, the observed frontier is
  re-scoped as an instruction-load effect, not a design-constraint-specific one."
- **Setup:** Within the prompt-only arm, the real constraint condition at each strength
  level is compared against a length-matched placebo condition (semantically inert
  instructions, token-count-matched in position and formatting to the rendered rule set).
- **Sample-size rationale:** Placebo arm added as a fourth condition at each pilot/scale-up
  strength level, matched in attempt count to the corresponding real-constraint cell (same
  750-attempt pilot budget structure as RQ2, extended to scale-up strength levels).
- **Statistical test:** Interaction test on the strength effect on pass rate between the
  real constraint arm and the placebo arm, Holm-adjusted p < 0.05.
- **Expected outcome:** The real constraint arm's strength effect on pass exceeds the
  placebo arm's strength effect by ≥3pp at maximum strength.
- **Metrics:** Interaction-term estimate and CI between the real and placebo arms.

---

## Further evaluation (descriptive rider, not a ninth RQ)

The pre-registered compliance-ceiling check (paper.md Claim 5 / H4) — whether residual
violation rate ever reaches exactly zero at an affordable strength level (CCS ≤ 2 ×
CCS(L0)) — is read directly off RQ4/RQ5's fitted curves with a 95% bootstrap CI on
min-V, requiring no new runs. Per the Stage 6 cross-stage consistency check
(`pipeline.md` "What was hardest"), this was deliberately **not** promoted to a ninth
standalone RQ: `paper.md` itself describes it as "attached to E2/E3 data... no new
runs" — a descriptive rider on the shape-detectability instrument's own output, not a
distinct decisive component the six-stage schema needs a dedicated slot for.
