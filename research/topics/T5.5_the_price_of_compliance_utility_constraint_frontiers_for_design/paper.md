# The Price of Compliance: Utility-Constraint Frontiers for Design-Aware Coding Agents — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All thresholds below are PRE-REGISTERED: chosen before any data collection; they may not
> be revised after seeing results. Digest ids (C1–C4, M1–M6, CO1–CO3, RQ1/RQ_INF_1/RQ_INF_2,
> t1–t5, Claims 1–5) are cited, not re-derived.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** In an LLM coding agent, design compliance and functional
correctness are produced by one and the same bounded generation process — every enforced
design rule consumes the exact prompt budget, sampling attempts, and solution-space slack
that unit-test passing draws on — so compliance is not purchased at a fixed exchange rate:
below the agent's constraint-carrying capacity it is nearly free, and beyond it each
additional rule depresses pass rate and inflates retry cost *simultaneously*, making
deployability a function of where that knee sits, not of the average price.

**判据 (deletion test).** Delete the domain nouns (coding agent, design rule, unit-test
pass rate, prompt budget, retry cost): *"In a system, two outputs are produced by one
bounded process, so adding requirements is cheap up to a capacity and expensive beyond
it."* — This residual is an empty truism: it makes no falsifiable prediction (any
monotone cost curve satisfies it) and is not even reliably true (independent-knob systems
trade at fixed rates with no knee). The falsifiable content — that the knee exists at
*measurable* constraint strength, that pass-rate loss and token cost are *coupled through
the same retry loop* (C2, C4), and that its location decides engineering feasibility
(Claim 2 / seed line 18) — exists only with the domain nouns restored. The sentence is
therefore an asymmetry claim, not a bridge.

## Step 2 — Archetype

**Primary: `empirical` (measurement study)** — consistent with digest N12: the headline
deliverable is a statistically tested shape verdict on the swept pass-rate ×
violation-rate × cost frontier (CO2), over *existing* agents; nothing new is trained.
**Secondary: `benchmark/resource`** — the seed's `[资源]` label; the κ-audited rule
catalog, sweep harness, and constraint-annotated suites (CO1, M1/M3/M6) are released, and
this secondary archetype is the pre-committed pivot target (F-G1 below).

Downstream consequences:
- **(a) Abstract contribution slot:** a measured, tested *shape verdict* (knee vs.
  graceful, with CI on knee location) plus a cost decomposition (CO3) — NOT a new agent,
  enforcement technique, or SOTA number.
- **(b) Intro logic:** "what becomes decidable" — before this measurement, no one can
  decide whether design-aware coding agents are engineering-feasible at meaningful
  constraint strength; the frontier makes that a lookup, not a bet. Not "we beat X".
- **(c) Evidence standard (results section):** pre-registered statistical tests
  (mixed-effects models, Davies test, ΔAIC, Holm correction, bootstrap CIs per digest
  N8), per-model per-arm reporting (never pooled, per C4), and both mandatory controls
  (B0, B-alt) present in every headline figure. Effect existence alone is insufficient;
  the hard-coded margins in Step 6 must be met.

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Check: the framing is not "constraint-following
  research (IFEval/FollowBench) and coding benchmarks (SWE-bench) were never connected,
  we connect them." The opportunity is an *unmeasured quantity with decision value*: the
  coupled degradation frontier (Step 0 asymmetry). Bridges connect; this measures an
  invariant of one process. **PASS.**
- **Is the method mere Synthesis?** Check: the harness does assemble existing pieces
  (BigCodeBench, SWE-bench Verified, linters). But the method's load-bearing moves are
  *isolation* moves, not assembly: the bindingness screen (kills inert rules, t5), the
  κ-audit gate (bounds construct risk, C1/t1), the factorial breadth × strictness grid
  (unconfounds C3), the multi-arm + placebo design (unconfounds mechanism from
  constraint, C4/t2). These are controls, i.e., measurement methodology. **PASS.**
- **Load-bearing verbs.** Audit of the framing's verbs: *sweep, measure, isolate,
  screen, audit, decompose, test (a shape), gate*. No load-bearing *integrate / unify /
  combine / leverage*. **PASS.**
- **Abstract-opening rule.** Abstract v0 (below) opens with the mechanism/asymmetry
  ("Design compliance and functional correctness draw on the same generation budget…"),
  not with "Coding agents are increasingly used… however… we introduce". The digest N0
  draft abstract *does* open with the forbidden template ("Coding agents are increasingly
  asked…"); it is superseded by Abstract v0 here. **FIXED at the skeleton level:** the
  first sentence now carries the Step-0 asymmetry, and the contribution sentence uses
  "measure/characterize/isolate", not "introduce a framework".

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The joint relationship between enforced design-constraint
strength σ = (breadth, strictness) and enforcement arm a, on one hand, and three outcomes
— task pass rate, residual constraint-violation rate, and cost-per-compliant-solved-task —
on the other, for existing LLM coding agents (one frontier API, one mid-tier API, one
open-weight model) evaluated on executable coding-task suites (BigCodeBench-Hard,
a SWE-bench Verified subset). Unit of analysis: one (task, σ, arm, model, sample) attempt.
Reference population: current LLM-based coding agents operating under machine-checkable
design-rule enforcement on Python-centric executable benchmarks. Decision it feeds:
whether, and at what constraint strength, enforcing a given design-rule catalog is
engineering-feasible to deploy, and which enforcement mechanism (prompt-only vs.
checker-in-the-loop retry vs. binary all-on) to prefer at that strength.

**Notation.** Task set T (function-level T_f, |T_f| ≈ 150 BigCodeBench-Hard;
repository-level T_r, |T_r| = 50 SWE-bench Verified subset; M6). Rule catalog
R = {r_1..r_K}, K ≈ 20, each r a deterministic decision procedure over an AST/static
analysis of solution y (M1/M3). Strength σ: pilot ordinal ladder L ∈ {0..4} (cumulative
packs); scale-up factorial σ = (b, s) ∈ {1,2,3} × {1,2,3} plus σ₀ = L0 (b = 0). Active
set R(σ) ⊆ R. Enforcement arm a ∈ {P (prompt-only), R (checker-in-loop retry, k ≤ 3),
B (binary all-on single shot)} (M2). Model m. Attempt = one (task, σ, a, m, sample) run;
5 samples per cell.

Every load-bearing adjective/verb in the Claims, made computable:

| Adjective / verb (Claims source) | Formal definition | Measured by |
|---|---|---|
| pass (utility) | `pass(y,t) = 1` iff y passes all of t's unit tests / fail-to-pass tests | executable oracles (M6); Pass@1 = mean over attempts per cell |
| violation rate (Claim 1) | `V(y,σ) = |{r ∈ R(σ): r(y)=viol}| / |R(σ)|`, macro-averaged over tasks | M3 checker suite (no LLM judge) |
| compliant-pass | `CP = Pr[pass(y,t)=1 ∧ V(y,σ)=0]` | joint oracle + checker |
| cost | `c(attempt) = (tok_in, tok_out, #retries, wallclock, USD)`; primary economic scalar `CCS(σ,a,m) = Σ USD / #compliant-passed tasks` | M4 API metadata, prices pinned to run date |
| **non-trivial** trade-off (Claim 1) | strength effect on pass: mixed-effects OR per ladder step < 0.90 with Holm-adj p < 0.05, AND absolute drop Pass@1(L4) ≤ Pass@1(L0) − 5pp | H1 procedure |
| **knee / cliff** vs. **graceful** (Claim 2) | knee exists iff Davies test p < 0.05 AND ΔAIC = AIC_linear − AIC_segmented > 4 for pass-rate-vs-σ (M5) AND the segmented fit's post-breakpoint slope magnitude is ≥ 2× its pre-breakpoint slope magnitude (effect floor — a statistically detected breakpoint below this ratio is reported as graceful-with-inflection, not a knee, per guidance.md §3.1's significance-without-magnitude rule); graceful iff the dual-criterion test fails or the slope-ratio floor is unmet | H2 procedure |
| knee **consistent across models** | 95% bootstrap CIs (1,000 task-level resamples) on knee location σ* overlap pairwise for all tested models | H2b |
| **shape-discordant** (Claim 2; closes the cross-axis objective pipeline.md's Stage 1 refiner committed to but this spec had not yet formalized) | the identical dual-criterion-plus-slope-floor test applied independently to cost-vs-σ (log-CCS) yields a different graceful/knee classification than the pass-rate-vs-σ test, for the same (model, arm) cell | H2c procedure — reported per cell as its own outcome, never resolved by treating one axis as authoritative |
| **binding** rule (t5) | rule r is binding iff ≥ 5% of L0 (unconstrained) generations violate r | walking skeleton + pilot screen; non-binding rules replaced pre-scale-up |
| **attributable to mechanism** (Claim 4) | mechanism share `MS(σ) = [CCS_R(σ) − CCS_P(σ)] / [CCS_R(σ) − CCS(L0)]`, plus arm × strength interaction term in two-way mixed model | H3 procedure; M4 decomposition (prompt-overhead vs. retry vs. output tokens) |
| **super-proportional** retry cost (Claim 4) | cost elasticity of retry arm w.r.t. σ exceeds 1: log-cost slope ratio retry/prompt-only > 1.5 at top strength tier | H3b |
| **affordable** strength / compliance **ceiling** (Claim 5) | strength σ is affordable iff CCS(σ) ≤ 2 × CCS(L0); ceiling exists iff min over affordable σ of V > 0 | H4 (digest N9.4 falsification, hardened) |
| **valid** checker (C1) | per-rule Cohen's κ ≥ 0.8 vs. 2 human annotators on 100-sample stratified audit; rules below gate are dropped | M3 audit protocol |

Deleted adjectives (no computable definition retained): "meaningful" (strength),
"realistic" (tasks) — replaced by the binding screen and the named benchmarks respectively.

## Assumptions (A1..A7)

Each assumption below now names an explicit gate id (PG-\*, per goal.md §4's "instrument
validation runs inside B as PG-\* gates") and an explicit consequence clause naming which
H\* it degrades/restricts/blocks, per guidance.md §3.2's five-slot template.

- **A1 (construct):** Machine-checkable rules are faithful proxies for design intent
  (C1). *Failure mode:* checkers flag artifacts, not violations. *Detection* (guidance.md
  R2, 5-step): ① rule templates grounded in named external conventions (import-linter,
  radon, ruff thresholds); ② catalog drafted wide, then refined on a held-out calibration
  subset of L0/L1 generations, with named merge/split/remove operations dropping rules
  that never fire or always fire before the main sweep; ③ M3 κ-audit against 2 human
  raters on a 100-sample stratified subset, any rule κ < 0.8 dropped; ④ confusion
  structure inspected — disagreements must cluster on ambiguous rule wording, not a
  systematic checker/human collapse; ⑤ catalog + thresholds frozen (hashed) before
  scale-up. *Gate:* **PG-2** (pilot, after the walking skeleton, before the scale-up
  commit); halt and re-scope the catalog if > 40% of rules drop at step ③. *Consequence:*
  failure degrades the construct validity of V (violation rate), which feeds H1's
  violation-rate reporting, H2/H2c's cost-vs-constraint attribution, and H3 — those
  hypotheses are restricted to the post-audit rule subset and never scored on dropped
  rules.
- **A2 (bindingness):** Catalog rules bind on benchmark tasks. *Failure mode:* rules
  never approached at L0 → inert sweep, flat frontier artifact (t5). *Detection:* walking
  skeleton measures L0 violation prevalence; rule replaced if < 5% L0 violation. *Gate:*
  **PG-1** (walking skeleton, Step 9 pass criterion (i); doubles as the B0 check).
  *Consequence:* an undetected failure would flatten the frontier artificially, producing
  a false "graceful" verdict on H1/H2/H2c — the bindingness screen blocks scale-up until
  this gate passes.
- **A3 (oracle):** Unit-test / fail-to-pass oracles measure utility validly. *Failure
  mode:* flaky tests inject noise. *Detection:* 3× deterministic re-execution of a 50-task
  sample; tasks with unstable verdicts excluded. *Gate:* **PG-3** (walking
  skeleton/pilot, before the main sweep). *Consequence:* unaddressed flakiness inflates
  variance and degrades power for H1/H2 (interacts with A6's gate below); excluded tasks
  shrink the reported n and are never silently backfilled.
- **A4 (separation):** Adjacent strength levels produce measurable metric separation.
  *Failure mode:* ladder too coarse/too fine → no signal. *Detection:* pilot go/no-go
  gate — see Step 9 criterion (ii); densify levels near any detected transition (t4
  mitigation). *Gate:* **PG-4** (walking skeleton, Step 9 pass criterion (ii)).
  *Consequence:* failure blocks H1/H2/H2c scoring outright — an unseparated ladder cannot
  license a shape verdict, so the skeleton does not pass and scale-up does not proceed.
- **A5 (cost accounting):** API token metadata + pinned published prices give stable USD.
  *Failure mode:* price changes / hidden caching mid-run. *Detection:* raw token logs kept;
  all analyses re-runnable in token units; prices pinned to run dates. *Gate:* continuous,
  logged per attempt — walking-skeleton criterion (iii) checks the logging schema itself;
  there is no single pre-scale gate because prices can move mid-run. *Consequence:* a
  detected price change degrades H1(ii)'s and H3's CCS-based criteria to token-unit-only
  reporting for the affected window; it does not block H1(i)/H2's pass-rate-only
  criteria.
- **A6 (power):** 750 attempts per (level, model, arm) cell suffice for the H1 margin.
  *Failure mode:* underpowered → false "graceful" verdict (t4). *Detection:* post-pilot
  power analysis on observed variance before committing scale-up budget; if power < 0.8
  for a 5pp drop, increase samples per task before scaling, once, within the
  pre-committed budget ceiling (digest N6 feasibility). *Gate:* **PG-5** (post-pilot,
  before the scale-up budget is committed). *Consequence:* if the one-time enlargement
  still leaves power < 0.8 for a given (model, level, arm) cell, that cell is
  pre-declared **INCONCLUSIVE** for every H\* that reads it — excluded from PASS/FAIL
  aggregation numerators and denominators, never counted as a null result, per
  guidance.md Part 6 item 9 and Part 4 situation 5.
- **A7 (stability):** Model behavior stable across the run window. *Failure mode:*
  silent model updates confound the sweep. *Detection:* pinned model versions; a 20-task
  L0 canary re-run at start/middle/end; > 3pp canary drift ⇒ flag and re-run affected
  cells. *Gate:* continuous (**PG-6**, checked at three fixed points: pilot start/mid/end,
  and scale-up start/mid/end if scale-up spans multiple sessions). *Consequence:* a
  flagged drift restricts the affected cells' H1–H3/H2c scoring to the pre-drift data, or
  triggers a re-run, before those cells count toward any aggregation vote.

## Step 6 — Pre-Registered Experiments

### E1 — RQ1: How much does compliance cost, and what does the frontier look like?

- **Assumption:** A1, A2, A3, A5, A6, A7.
- **Hypothesis H1 (binary):** From L0 to L4 (pilot ladder, prompt-only arm, per model):
  (i) Pass@1(L4) ≤ Pass@1(L0) − 5 percentage points, with mixed-effects logistic
  regression strength coefficient OR < 0.90 per step at Holm-adjusted p < 0.05; AND
  (ii) CCS(L4) ≥ 1.25 × CCS(L0). H1 holds iff (i) AND (ii) hold for ≥ 2 of 3 scale-up models.
- **Metric:** Pass@1, V, CP, CCS as defined in Step 5 (digest N8 metrics group).
- **Verification:** n = 150 tasks × 5 samples = 750 attempts per (level, model, arm)
  cell. Mixed-effects logistic regression of per-attempt pass on strength (task random
  intercept); Cochran–Armitage trend test across levels; α = 0.05, Holm-corrected across
  models × arms (digest RQ1 analysis plan, thresholds now fixed).
- **Fallback F1 (pre-committed wording):** "Within the swept regime (≤ 20 κ-audited,
  binding design rules on BigCodeBench-Hard/SWE-bench Verified), design compliance is
  approximately free for current coding agents: pass rate degrades < 5pp and cost per
  compliant-solved task rises < 25% even at maximum strength — removing the presumed
  economic barrier to design-aware deployment." (Publishable negative per digest N9.1.)

### E2 — RQ_INF_1: Knee or graceful?

- **Assumption:** A2, A4, A6 (+ E1 infrastructure).
- **Hypothesis H2 (binary):** On scale-up data, under the checker-in-loop retry arm, a
  knee exists — Davies test p < 0.05 AND ΔAIC > 4 favoring segmented over linear fit of
  Pass@1 vs. strength, AND the segmented fit's post-breakpoint slope is ≥ 2× the
  pre-breakpoint slope in absolute pp-per-level terms (effect floor, per guidance.md
  §3.1: a statistically detected breakpoint below this magnitude is reported as
  graceful-with-inflection, not scored as a knee) — for ≥ 2 of 3 models. **H2b
  (secondary, binary):** the 95% bootstrap CIs on knee location overlap pairwise across
  all models exhibiting a knee. **H2c (secondary, binary — formalizes the cross-axis
  check pipeline.md's Stage 1 refiner and taste_audit.md already assume but this spec had
  not yet pre-registered):** the identical dual-criterion-plus-slope-floor test applied
  independently to cost-vs-strength (log-CCS) yields the same graceful/knee
  classification as the pass-rate test, for ≥ 2 of 3 models; cells where the two
  classifications disagree are reported as **shape-discordant** — a distinct, informative
  outcome, never resolved by treating one axis as authoritative.
- **Metric:** knee location σ* + 95% CI (1,000 task-level bootstrap resamples); ΔAIC;
  Davies p; pre/post-breakpoint slope ratio (digest M5); cross-axis agreement rate and
  count of shape-discordant cells (H2c).
- **Verification:** Segmented vs. linear regression of Pass@1 (and log-CCS) on strength,
  per model × arm; Holm correction across the model × arm cells; dual criterion
  (Davies + ΔAIC) plus the slope-ratio effect floor required jointly, per threat t4; the
  two per-axis verdicts are then compared directly for H2c.
- **Fallback F2 (pre-committed wording):** "The compliance-utility frontier is graceful:
  pass-rate loss is statistically indistinguishable from linear in constraint strength
  across all models and arms (Davies p ≥ 0.05, ΔAIC ≤ 4, or a detected breakpoint with
  sub-2× slope steepening), so feasibility reduces to a per-rule unit price that teams
  can budget linearly — the 'cliff risk' motivating cautious partial adoption of design
  constraints is not supported." (Digest N9.2.)
- **Fallback F2c (pre-committed wording, H2c):** "The pass-rate and cost curves' shapes
  disagree (shape-discordant) in a majority of tested model × arm cells; no single
  'frontier shape' verdict can be reported per cell, and feasibility guidance must be
  given separately per axis (utility-shape vs. cost-shape) rather than as one combined
  shape claim."

### E3 — RQ_INF_2: Mechanism or constraints?

- **Assumption:** A1, A5, A7.
- **Hypothesis H3 (binary):** At the top strength tier (b=3, s=3): (i) V_retry ≤ 0.5 ×
  V_prompt-only (retry halves residual violations); AND (ii) arm × strength interaction
  in the two-way mixed-effects model on log-cost is significant at Holm-adjusted
  p < 0.05 with mechanism share MS ≥ 0.30; AND (iii) retry-arm log-cost slope ≥ 1.5 ×
  prompt-only slope (super-proportional). H3 holds iff (i)–(iii) hold for ≥ 2 of 3 models.
- **Metric:** V per arm; MS(σ); disaggregated cost components (prompt-overhead tokens,
  retry tokens, output-inflation tokens) per M4; CO3 decomposition.
- **Verification:** Identical constraint grids under arms P/R/B; two-way (arm × strength)
  mixed-effects models on pass and log-cost; α = 0.05 Holm-corrected (digest RQ_INF_2 plan).
- **Fallback F3 (pre-committed wording):** "The frontier is mechanism-invariant: the
  price of compliance is a property of the constraint set, not of the enforcement
  machinery (arm × strength interaction n.s., MS < 0.30), so practitioners may choose
  the cheapest enforcement mechanism without shifting the frontier." (Digest N9.3.)

### E4 — Claim 5 rider (compliance ceiling), attached to E2/E3 data

- **Assumption:** A1, A2. **Hypothesis H4 (binary):** at every affordable strength
  (CCS ≤ 2 × CCS(L0)), residual V > 0 in all model × arm cells. **Metric:** min V over
  affordable σ. **Verification:** descriptive with 95% bootstrap CI on min-V; no new runs.
  **Fallback F4:** "Full design compliance is achievable at ≤ 2× the unconstrained cost
  per solved task, at strength σ = …" (digest N9.4 falsification, stated as the positive).

### Mandatory baselines

- **B0 — "why do this at all" control: the L0 unconstrained arm.** Measures violation
  prevalence when nothing is enforced. If unconstrained agents already satisfy the
  catalog (macro L0 violation rate < 5%), there is no compliance problem to price and
  the study halts at the skeleton (this doubles as the A2 bindingness screen). B0 also
  anchors the utility ceiling and the CCS denominator for every hypothesis above.
- **B-alt — strongest-alternative-explanation control: length-matched placebo prompt.**
  *Rival explanation:* degradation is caused by instruction load per se — longer prompts
  and more in-context directives depress pass rate regardless of content (threat t2) —
  i.e., the frontier measures prompt length, not design constraints. *Control:* at each
  strength level, an arm receiving semantically inert instructions token-count-matched
  to the rendered rule set (same position, same formatting). Budget/capability-matched
  by construction. Pre-registered check: the strength effect on pass in the constraint
  arm must exceed the placebo arm's effect by ≥ 3pp at L4 (Holm-adj p < 0.05, interaction
  test); otherwise all H1/H2 claims are re-scoped to "instruction-load effects".

### Global fallback F-G1 (archetype pivot)

If the central hypothesis family {H1, H2, H3} all fail, pivot from `empirical` (shape
verdict) to `benchmark/resource` (the seed's `[资源]` label; CO1 becomes the headline).
Pivoted abstract sentence, pre-committed: "We release the first κ-audited,
bindingness-screened harness for sweeping machine-checkable design-constraint strength
in coding agents — with the calibration finding that, across three models and two
executable benchmarks, compliance was approximately free and mechanism-invariant in the
swept regime, establishing the measured baseline any future design-aware agent must beat."

## Step 9 — Walking Skeleton

**One binary question:** *Do design constraints bind and separate at all — i.e., does the
full pipeline (rules → enforcement → checker → oracle → cost log) produce measurable
daylight between no-constraints and max-constraints?*

- **Arms (2):** L0 (unconstrained) vs. L4 (all pilot rule packs, prompt-only). One model
  (mid-tier API, pinned version).
- **Task set:** 30 BigCodeBench-Hard tasks (stratified by L0 difficulty), 3 samples each
  → 180 generations total.
- **Metrics (deterministic only):** Pass@1, macro violation rate V (M3 checkers), input/
  output tokens. No statistics, no fitting, no human audit yet.
- **Cost:** ≈ 4–6 × 10⁵ tokens, < $10, < 4 hours wall-clock including harness debugging
  (within the digest's $30–150 pilot class with large margin).
- **Pass criterion (binary):** (i) macro L0 violation rate ≥ 5% (rules bind — A2/B0
  gate; individually non-binding rules listed for replacement), AND (ii) at least one of:
  Pass@1(L4) ≤ Pass@1(L0) − 3pp, V(L4) ≤ V(L0) − 10pp, or mean tokens/attempt at L4 ≥
  1.10 × L0. AND (iii) every attempt row logs all five cost fields with no nulls.
- **"Skeleton passed ⇒ scaling is a config change":** the pilot (150 tasks × 5 levels ×
  5 samples) and scale-up (3 models, 3×3 grid, 3 arms, + SWE-bench suite) must be
  launchable by editing the harness config (task list, level set, arm flag, model id)
  with zero new code paths except the SWE-bench repo-rule mapping (M6), which is data,
  not code. If any scale-up step requires new harness logic, the skeleton did not pass.

## Claim–Evidence Map

| Claim (digest Claims 1–5) | Traces to | Status |
|---|---|---|
| 1. Non-trivial, likely non-linear trade-off | H1 (margin defs, Step 5) + H2 | needs-experiment; fallback-covered (F1/F2) |
| 2. Frontier *shape* determines deployability | Step-0 asymmetry + H2/H2b; "knee/graceful/affordable" defs (Step 5) | needs-experiment; fallback-covered (F2 reframes as unit price) |
| 3. Gap: no prior joint strength-sweep frontier (corpus-checked) | digest N3 grounding procedure + honest coverage report | supported-by-design (corpus evidence; scoped "novelty-encouraging, not proving"; supplementary arXiv/DBLP search pre-committed per N3 absence_comment) |
| 4. Substantial cost attributable to mechanism | H3 + MS definition (Step 5) | needs-experiment; fallback-covered (F3) |
| 5. Nonzero compliance ceiling at affordable strength | H4 + "affordable/ceiling" defs | needs-experiment; fallback-covered (F4) |
| (Instrument claim, CO1) κ-audited, binding, open protocol | A1/A2 gates + M3 audit + skeleton criterion | supported-by-design (gates are the evidence) |

Every abstract claim below maps to a row above; no claim lacks an H-id or Step-5 definition.

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — BEFORE RESULTS; numbers are pre-registered criteria, not findings.]**
> Design compliance and functional correctness in an LLM coding agent draw on one bounded
> generation process, so enforcing architectural rules cannot trade utility at a fixed
> rate: cost and pass-rate loss are coupled through the same prompts and retries, and
> deployability hinges on where — not whether — that coupling bites. We measure this
> directly: a κ-audited catalog of ~20 machine-checkable design rules, screened for
> bindingness, is swept over breadth × strictness across executable benchmarks
> (BigCodeBench-Hard, SWE-bench Verified) under prompt-only, checker-in-the-loop, and
> placebo-matched enforcement arms, logging pass rate, residual violation rate, and cost
> per compliant-solved task. Segmented-regression tests with bootstrap CIs isolate
> whether the frontier degrades gracefully or exhibits a knee, and a cost decomposition
> separates mechanism-induced from constraint-induced price. The resulting frontier turns
> design-aware agent feasibility from a bet into a lookup.
