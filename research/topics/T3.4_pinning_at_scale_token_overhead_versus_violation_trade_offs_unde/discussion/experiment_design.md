# Experiment Design — T3.4: Pinning at Scale

> Standalone protocol document, per `auto-research-discussion`'s Final Deliverables spec. This is Stage 6's confirmed output (`pipeline.md`, "## Stage 6 — Experiment Design") rendered runnable on its own, cross-checked against `paper.md`'s Step 6 ("Pre-Registered Experiments," E1–E4) for the setup/statistical-test/expected-outcome detail Stage 6 carried forward from that pre-registered spec. Nothing below is invented beyond those two sources. Keep synchronized with `paper_draft.md`'s Experiments section and `discussion_trace.md` if either changes.
>
> **Study type:** `empirical` (Stage 1). No research question below is framed as "our procedure beats baseline X" — baselines are floor/sanity-check comparators only. **Tier accounting:** 4 mechanism-tier RQs (below), 0 framing-tier (no Stage 3 limitation was flagged `verify_as_hypothesis`), 0 outcome-tier (forbidden under `study_type=empirical`). A fifth Stage 5 method, `m_tradeoff_tracker` (targets sub-problem `sp_multiobjective_frontier`), is disclosed as deliberately hypothesis-free — it renders the full (n, policy, model) → {V, O, S} grid as a Pareto surface rather than resolving it to one scalar — and correctly contributes zero RQs here.

## Datasets

- **τ-bench** (airline/retail policy-following tool-use tasks) — the primary task suite for every RQ; real domain policies serve as constraint seeds, and task success is verified via database-state checks (a programmatic end-state check, satisfying Stage 1's constraint that success resolve to a non-subjective check).
- **IFEval / FollowBench** — rule-based constraint sources (verifiable instructions, multi-level constraint templates), scaled via RECAST-style mining to build the constraint pool up to *n* = 400 that every RQ draws from.
- **PrefEval** — semantic-constraint source and long-context distractor protocol, feeding the LLM-judged remainder of the constraint pool (≥ 30%) that RQ4 (detector validity) specifically needs to stress-test.

*(A candidate fourth dataset, LMSYS-Chat-1M, was dropped in Stage 6's refiner pass: its only offered justification was provenance — "as used by PrefEval" — not a link to any of the four confirmed RQs. None of the RQs tests whether irrelevant conversational history, as opposed to constraint count, prompt length, or applicability density, affects compliance; this design always keeps constraints pinned or selectively pinned, never merely buried in unstructured history. Logged as a further-evaluation item, not fabricated into scope here.)*

## Baselines

Sanity-check / floor comparators — never outcome-tier competitors to beat:

- **Full pinning** — the stress-tested default every other condition is compared against.
- **No pinning (B0)** — the "why does this problem exist at all" control: constraints stated once at *t* = 1, never repeated. Pre-registered check: V(300, none) ≥ V(5, none) + 0.05; if this fails, constraint retention is a non-problem and pinning of any kind needs no study. Also anchors the trade-off surface's zero-overhead corner.
- **Random-*k* selector at the same token budget** — the capability-matched floor that any claim about applicability-aware selection (RQ2/H2b) must clear.
- **Length-matched inert-padding arm** — the rival-explanation control isolating constraint count from raw prompt length (RQ3/H3): identical token count and position, no normative content.

Grid and analysis plan (Stage 6 note, carried from `paper.md` Step 6): *n* ∈ {4, 10, 25, 50, 100, 200, 400} × 6 policies × 3 models × 150 tasks × 3 seeds (450 episodes/cell; powered for a 10-percentage-point success difference at 0.8 power, α = 0.05). Family-wise correction: Holm–Bonferroni over the policy family at α = 0.05. Any cell falling below 388 episodes/arm after dropped-row exclusion is pre-declared INCONCLUSIVE for that cell rather than scored as a null result.

---

## RQ1 — `rq_full_pinning_knee` (Mechanism tier)

**Target sub-problem:** `sp_budget_vs_load`

**Target hypotheses (verbatim, Stage 5 = Stage 6):**
- H1: "Under full pinning, task success as a function of constraint count n has a detectable breakpoint (segmented regression, Davies test p < 0.05, 95% bootstrap CI inside [25, 400]), with success at n=400 at least 10 percentage points below success at n=10 in at least 2 of 3 tested models."
- H1b: "Violation rate at n=400 exceeds violation rate at n=10 by at least 3 percentage points (absolute) in at least 2 of 3 tested models under full pinning, even though every constraint remains resident in context at every turn."

**Setup:** Pilot stage: 2 backbones × 2 conditions (full pinning / no pinning) × 50 pairs × 20 episodes on the rule-based subset. Scale-up: the full 7-level constraint-count grid × 6 policies × 3 models × 150 tasks × 3 seeds (450 episodes/cell). Under π_full only for H1/H1b.

**Sample-size rationale:** 450 episodes/cell, sized to detect a 10-percentage-point success difference at 80% power, α = 0.05 (the pre-registered analysis-plan target); cells falling below 388 episodes/arm after exclusions are declared INCONCLUSIVE for that cell rather than scored.

**Statistical test:** Mixed-effects logistic regression of episode success on log *n* × policy with a task random effect; segmented (piecewise-linear) regression of logit(success) on log *n* with a Davies test for a breakpoint; violation rate compared via cluster-robust standard errors at the episode level. Degrades to cluster-robust GEE (Generalized Estimating Equations — population-averaged regression with a robust sandwich variance estimator clustered by task) if the mixed-effects model fails to converge (A5).

**Expected outcome:** A detectable breakpoint (Davies *p* < 0.05, 95% bootstrap CI inside [25, 400]) with success at *n* = 400 at least 10 points below success at *n* = 10 in ≥ 2 of 3 models (H1); violation rate at *n* = 400 exceeds violation rate at *n* = 10 by ≥ 3 points (absolute) in ≥ 2 of 3 models, despite full context residence (H1b — presence without compliance).

**Fallback (pre-committed):** "Across three model families, full pinning of up to 400 simultaneously active constraints produced no detectable task-success knee; within this range the cost of exhaustive pinning is economic, not behavioral — we report the measured overhead schedule and the violation floor it buys."

**Metrics:** Segmented-regression breakpoint location and 95% CI; per-cell success at *n* = 10 vs. *n* = 400; per-cell violation rate at *n* = 10 vs. *n* = 400; overhead ratio *O* logged in parallel (secondary correlation, not a headline test).

---

## RQ2 — `rq_selective_pinning_viability` (Mechanism tier)

**Target sub-problem:** `sp_dynamic_applicability`

**Target hypotheses (verbatim, Stage 5 = Stage 6):**
- H2: "At n ≥ 100 with a selective-pinning budget of 25% of full pinning's constraint tokens, the best-performing selector achieves a violation rate non-inferior to full pinning within 0.02 absolute (one-sided 95% CI) while using at most 30% of full pinning's overhead."
- H2b: "The applicability-classifier selector achieves a violation rate at least 0.03 (absolute) lower than the best similarity-based selector (embedding or marginal-gain) at n ≥ 100 (Holm-corrected)."

**Setup:** At constraint counts *n* ≥ 100, all five selectors (random-*k*, static top-*k* by pilot-measured violation frequency, embedding similarity, COMI-style marginal-gain, applicability classifier) are re-run every turn at a fixed token budget *k* = 25% of full pinning's constraint tokens at the matching *n*, each scored against ground-truth applicability labels from the sweep harness.

**Sample-size rationale:** Drawn from the same 450-episodes/cell grid as RQ1, restricted to the *n* ≥ 100 cells across the 3 models; same 388-episodes/arm INCONCLUSIVE threshold applies per cell.

**Statistical test:** Per-budget pairwise non-inferiority tests (one-sided 95% CI at margin δ = 0.02 for H2; TOST-style two-one-sided-tests framing for H2b's converse/equivalence direction); Holm–Bonferroni correction across the 5-selector family; selector token/latency cost counted inside *O*.

**Expected outcome:** The best-performing selector is non-inferior to full pinning within 0.02 absolute violation rate while using ≤ 30% of full pinning's overhead (H2); the applicability-classifier selector beats the best similarity-based selector (embedding or marginal-gain) by ≥ 0.03 absolute violation rate at *n* ≥ 100, Holm-corrected (H2b).

**Fallback H2 (pre-committed):** "No budgeted selector matched full pinning within 2pp violation rate at any tested budget: for normative content, unlike evidence (COMI's domain), bounded selection is not safe — full pinning is the only reliable policy below the knee, and above it the practitioner faces a genuine dilemma, which we quantify."

**Fallback H2b (pre-committed):** "Applicability-aware and similarity-based selection were equivalent within ±2pp (TOST, α=0.05): normative applicability is empirically reducible to semantic relevance for this pool, so cheap embedding selection suffices — a deployable simplification." (Equivalence margin pre-set: ±0.02.)

**Metrics:** Per-selector violation rate and overhead ratio at matched budgets; non-inferiority margin test result against full pinning; pairwise applicability-classifier-vs.-similarity contrast; selector recall@k against the M1 applicability labels (diagnostic, secondary).

---

## RQ3 — `rq_count_vs_length_density` (Mechanism tier)

**Target sub-problem:** `sp_interference_dilution`

**Target hypothesis (verbatim, Stage 5 = Stage 6):**
- H3: "Length-matched inert padding reproduces at most 50% of the full-pinning task-success decline observed at n=400 (statistically distinguishable at α=0.05), and at fixed n=100, high applicability density raises violation rate by at least 0.03 (absolute, p<0.05) relative to low density."

**Setup:** Two linked subgrids. (i) At *n* = 400, a length-matched inert-padding arm (identical token count and position, no normative content) is compared against the real-constraint full-pinning arm on task-success decline relative to *n* = 4. (ii) At fixed *n* = 100, applicability density is independently varied at three levels (holding *n* constant), and violation rate is compared across density levels. This experiment is the internal-validity gate for interpreting RQ1.

**Sample-size rationale:** Drawn from the same mixed-effects machinery and episode-count targets as RQ1 (450 episodes/cell, 388-episode INCONCLUSIVE floor), applied to the padding-arm and density-level cells specifically.

**Statistical test:** Difference-of-declines significance test between the real-constraint arm and the padding arm at α = 0.05; same mixed-effects logistic machinery as RQ1 applied within the density subgrid.

**Expected outcome:** Inert padding reproduces ≤ 50% of the full-pinning success decline at *n* = 400 (statistically distinguishable, α = 0.05); at fixed *n* = 100, high vs. low applicability density raises violation rate by ≥ 0.03 absolute (*p* < 0.05).

**Fallback (pre-committed):** "Inert padding reproduced the full decline: the 'hundreds of constraints' effect is a raw prompt-length effect, and constraint-count guidance collapses into existing long-context guidance — we report this deflationary result with the padding-equivalence evidence." If density shows no effect, it is dropped from the harness as a nuisance factor, stated explicitly rather than silently dropped.

**Metrics:** Task-success decline magnitude, real-constraint arm vs. padding arm, with a difference-of-declines significance test; violation rate by applicability-density level at fixed *n*.

---

## RQ4 — `rq_detector_validity` (Mechanism tier)

**Target sub-problem:** `sp_detector_validity`

**Target hypothesis (verbatim, Stage 5 = Stage 6):**
- H4: "The dual-mode violation detector reaches Cohen's κ ≥ 0.80 against human annotation on a 300-episode stratified sample, with programmatic checkers reaching at least 0.95 raw agreement, after at most one calibration iteration."

**Setup:** A 300-episode sample, stratified by constraint count (*n*), policy, and constraint class, is independently annotated by 2 human raters (~50 annotator-hours), disjoint from a held-out 50-episode calibration slice used to refine the LLM-judge rubric beforehand. This experiment tests Assumption A1 directly and must clear its bar before any Stage-1 curve (RQ1–RQ3) is interpreted.

**Sample-size rationale:** 300 episodes, stratified by *n* × policy × constraint class, per the digest's feasibility analysis (~50 annotator-hours); calibration performed on a disjoint 50-episode slice first so the 300-episode sample is a clean validation set, not a tuning set.

**Statistical test:** Cohen's κ (overall and per constraint class) between detector verdicts and human annotation, with bootstrap confidence interval; per-class confusion-rate inspection to confirm disagreements concentrate between adjacent/similar constraint sub-types rather than a systematic class collapse.

**Expected outcome:** Overall κ ≥ 0.80 vs. human annotation, with programmatic checkers reaching ≥ 0.95 raw agreement, after at most one calibration iteration.

**Fallback (pre-committed, from digest N9):** "Semantic-constraint curves are withdrawn; all headline claims (H1–H3) are re-stated on the programmatically-checkable subset (≥ 70% of pool by construction), and LLM-judged constraints are reported in an appendix with judge-error bars." E1–E3 thresholds apply unchanged to the subset. The same fallback applies per-class if the confusion-structure check finds a systematic (non-adjacent) collapse for a specific constraint sub-type, even when aggregate κ passes.

**Metrics:** Overall and per-constraint-class Cohen's κ with bootstrap CI; programmatic-checker raw agreement rate.

---

## Global fallback (F-G1)

If the central family {H1, H1b, H2} all fail (no knee, no compliance decay, no favorable selective trade-off), the archetype pivots from `empirical` (trade-off characterization) to `benchmark/resource`: the deliverable becomes the calibrated constraint-count sweep harness itself — the labeled 400-constraint pool with per-turn applicability ground truth, dual-mode verified, plus the measured cost schedule. Pivoted abstract sentence (pre-committed, `paper.md` Step 6): "We release a 400-constraint, applicability-labeled sweep harness with calibrated dual-mode violation detection, and show that across three model families full pinning is behaviorally robust to at least 400 simultaneous constraints — making the pin-versus-select decision, within this range, a pure cost calculation for which we provide the measured schedule."
