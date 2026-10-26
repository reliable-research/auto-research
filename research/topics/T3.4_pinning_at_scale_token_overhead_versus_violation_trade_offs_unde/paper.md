# Pinning at Scale: Token Overhead versus Violation Trade-offs under Hundreds of Constraints — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1–C5, M1–M5, CO1–CO4, RQ1/RQ_INF_1–3, t1–t5) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** In a context window, pinning purchases the *presence* of each constraint at a linear token price, but *compliance* with each constraint is paid out of a fixed attention budget that every co-resident constraint dilutes — so the mechanism that guarantees a rule is seen is, past some count, the same mechanism that reduces how well any rule is followed.

**判据 (deletion test).** Delete the domain nouns (pinning, constraint, context window, token, attention):
> "___ purchases the presence of each ___ at a linear ___ price, but compliance with each ___ is paid out of a fixed ___ budget that every co-resident ___ dilutes."

Without the nouns the sentence has no truth value — there is no generic claim left standing ("presence is bought in one currency, compliance paid in another, and the currencies scale oppositely" is only true *because* transformer context has linear token cost and sublinear per-item attention). It does not survive as a valid generic statement, so it is an asymmetry, not a bridge. Contrast the forbidden form: "context compression and constraint following were never connected; we connect them" — that survives noun deletion and is rejected.

## Step 2 — Archetype

- **Primary:** `empirical` (measurement study), per N12: the spine is a factorial constraint-count sweep that deconfounds count, length, and applicability density and locates a breakpoint (CO1, CO3). The selective-pinning policy (CO2) is a *compared condition*, not a proposed system.
- **Secondary:** `benchmark/resource` — N12's stated post-hoc hinge: if the labeled constraint pool + harness (CO4) becomes the headline deliverable, reclassify. This is also the F-G1 pivot target (below).

**Downstream consequences:**
- (a) *Abstract contribution slot:* a characterized trade-off surface and a located knee n\* with CI — a number-with-uncertainty, not a SOTA delta and not a new system.
- (b) *Intro logic:* "what becomes decidable" — deployers currently choose pin-everything by folklore; the paper makes the pin-vs-select decision a measured function of (n, budget, constraint class). Not "we beat baseline X".
- (c) *Evidence standard for results:* effect existence + localization must survive deconfounding controls (padding, density) and detector-validity gates (κ ≥ 0.8); a policy "winning" without the B-alt budget-matched control is inadmissible. Negative/flat results are reportable under pre-committed fallbacks — the design is falsification-first (N9).

## Step 3 — Taste Self-Audit

| Check | Verdict | Note |
|---|---|---|
| Is the opportunity a Bridge ("A meets B")? | **PASS** | The opportunity is an asymmetry internal to one mechanism (presence vs compliance under one attention budget), not a connection between two literatures. COMI/RECAST are instruments, not the other side of a bridge. |
| Is the method mere Synthesis (glue existing parts)? | **PASS (after check)** | Risk: M3 reuses COMI-style selection. Resolution: the method's spine is the *factorial measurement design* (M1: count ⊥ length ⊥ density) + calibrated detector (M4); selectors are stimuli inside that design. The contribution is the measured surface, not the glued selector. |
| Load-bearing verbs from integrate/unify/leverage family? | **PASS** | Load-bearing verbs: *measure, sweep, deconfound, locate, isolate, gate, calibrate*. "Leverage/integrate" appear nowhere in claims. |
| Abstract opening rule | **ENFORCED** | Abstract v0 (below) opens with the presence-vs-compliance mechanism; the "LLM agents are increasingly used… however… we introduce" template from digest N0's draft abstract is discarded and rewritten. |

No framing fix needed beyond discarding the N0 draft abstract's opening (which used the forbidden "increasingly deployed… we ask" template).

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The joint trade-off surface {V, O, S}(n, π, m) — violation rate, token-overhead ratio, and task success rate — as a function of standing-constraint count n under pinning policy π, at the unit of analysis of one episode (a single agent run on one task with one constraint set, one policy, one model, one seed); reference population = LLM agents executing checkable multi-step tasks under a fixed per-turn token budget with a standing constraint set drawn from the pool P; the decision it feeds is whether a deployer should pin every standing constraint verbatim or adopt a bounded selective-pinning policy once n crosses the located knee n\*.

**Notation.** Episode e = (τ, C, π, m, s): task τ from suite T, constraint set C with |C| = n drawn from pool P, pinning policy π, model m, seed s. Turns t = 1..T_e. Ground-truth applicability label app(c, e, t) ∈ {0,1} from the M1 manifest. Detector verdict viol(c, e) ∈ {0,1} on applicable pairs (M4). tok(·) = tokenizer count. Policies: π_full (all n verbatim/turn), π_none (once at t=1), π_k^σ (budget k tokens, selector σ ∈ {rand, freq, sim, comi, app} per M3).

**Core quantities.**
- **Violation rate** V(n, π, m) = Σ_e Σ_c viol(c,e) / Σ_e Σ_c 1[app(c,e,·)=1]  — per digest metrics (N8).
- **Overhead ratio** O(n, π, m) = mean_t [ tok(constraint block_t) / tok(prompt_t) ]; also absolute cumulative constraint tokens per episode; cache-adjusted effective cost reported alongside (t1).
- **Task success** S(n, π, m) = fraction of episodes passing the programmatic end-state check.
- **Knee** n\* = breakpoint of segmented regression of logit(S) on log n under π_full (M5), existence gated by Davies test p < 0.05, CI by bootstrap (1,000 resamples).

**Adjective/verb → definition → measurement:**

| Claim word (digest Claims 1–5) | Formal definition | Measured by |
|---|---|---|
| "backfires" / "measurably reduce" (Claim 1) | Post-breakpoint slope β₂ < 0 in segmented model, p < 0.05, AND S(400, full, m) ≤ S(10, full, m) − 0.10 | M5 on Stage-1 grid |
| "knee n\*" (Claims 1, 3) | Davies-test breakpoint with 95% bootstrap CI ⊂ [25, 400] | M5 |
| "presence does not guarantee compliance" (Claim 1) | V(400, full, m) − V(10, full, m) ≥ 0.03 despite all constraints in context | M4 counts |
| "approximately match" (Claim 2) | Non-inferiority: V(select) − V(full) ≤ δ = 0.02 absolute, one-sided 95% CI | TOST-style non-inferiority test (Two One-Sided Tests: reject non-inferiority's null only if the entire (1−2α) CI of the difference falls within [−δ, δ]) |
| "a fraction of its token overhead" (Claim 2) | O(select) ≤ 0.30 × O(full) at same (n, m) | M2 instrumentation |
| "applicability-aware" (Claim 2) | Selector σ = app: P(c selected \| app(c,e,t)=1) computed against manifest labels; recall@k reported | M1 labels + M3 logs |
| "not reducible to semantic similarity" (Claim 2) | V(app-selector) ≤ V(sim/comi) − 0.03 at n ≥ 100, Holm-corrected | H2b test |
| "distinct degradation dimension" (Claim 3) | Padding-arm decline ≤ 0.5 × constraint-arm decline in S at n=400, difference p < 0.05 | H3 test |
| "reliable detector" (implicit in all curves) | Cohen's κ ≥ 0.8 vs human labels on 300-episode stratified sample; programmatic checkers ≥ 0.95 raw agreement | H4 / M4 calibration |

Deleted adjectives: "silently", "gracefully", "enterprise-scale" (motivation-only, no computable referent — excluded from claims).

## Assumptions

- **A1 — Checkable violations.** Every pool constraint carries a verification procedure; ≥ 70% programmatic (rule-based), remainder LLM-judged (N6 feasibility; RECAST-style construction). *Failure mode:* judge unreliable → curves uninterpretable (C5, t1). *Detection:* H4 κ-gate before any curve is read; skeleton runs on programmatic subset only. *Gate:* checked at E4, before Stage-1 curves are interpreted (not a walking-skeleton PG — the skeleton deliberately excludes the LLM judge, deferring A1 to E4). *Consequence if false:* H1/H1b/H2/H2b/H3's semantic-constraint-inclusive curves are withdrawn per the E4 fallback; all four headline hypotheses are re-scored on the programmatically-checkable subset only (≥70% of pool by construction) — no H\* is blocked outright, but every curve's scope narrows.
- **A2 — Pool scalable with applicability labels.** IFEval/FollowBench/τ-bench-policy constraints scale to n=400 with authored per-turn applicability labels (M1). *Failure:* labels ambiguous or pool degenerate (duplicates). *Detection:* pool-construction gate — two annotators label applicability on 50 sampled (c, e, t) triples, agreement ≥ 0.9 required before Stage 0. *Gate:* PG-0, pre-Stage-0 (runs before the walking skeleton itself, since the skeleton consumes the labeled pool as input). *Consequence if false:* blocks all of H1–H4 — Stage 0 cannot start without a validated pool; the pool must be re-annotated (relabel ambiguous applicability triples or deduplicate) and PG-0 re-run before any episode is executed.
- **A3 — Task suite sensitivity.** Constraints actually bind and success is off ceiling/floor: Stage-0 must show S ∈ [0.25, 0.85] at n=5 and no-pinning violation rate ≥ 0.05 at n=300. *Failure:* constraints never binding → nothing to measure. *Detection:* Stage-0 go/no-go (digest N6: "redesign task suite before scaling"). *Gate:* PG-4, the walking skeleton's pass criterion (iv) (Step 9). *Consequence if false:* blocks H1/H1b/H2/H2b/H3 — the task suite is redesigned (constraints too easy or never binding) and PG-4 re-run before Stage-1 scale-up; no H\* is scored against an unbinding suite.
- **A4 — Token counts price cost.** Overhead measured in tokens is meaningful despite provider prompt caching (t1). *Failure:* caching makes pinned blocks near-free. *Detection:* report raw and cache-adjusted cost; if they diverge > 5×, the overhead axis is re-based on cache-adjusted cost and H1's overhead clause re-stated in it. *Gate:* Stage-1 analysis (not walking-skeleton-checked — the skeleton logs token counts but does not yet compare raw vs. cache-adjusted cost; this is a documented gap, not a silent one). *Consequence if false:* does not block H1/H1b/H3 (violation-rate and success claims are unaffected), but degrades/rescales O(·) reporting and H2's "fraction of overhead" clause, which is re-stated in cache-adjusted units.
- **A5 — Statistical model estimable.** Episodes cluster by task; mixed-effects logistic with task random effect converges at 450 episodes/cell (digest analysis plan). *Failure:* non-convergence/singular fits. *Detection:* skeleton fits the model on pilot data; pre-committed degradation path: cluster-robust GEE (Generalized Estimating Equations — a population-averaged regression with a robust sandwich variance estimator clustered by task, used in place of the mixed-effects model when the latter's random-effects fit fails to converge). *Gate:* PG-1, walking-skeleton pass criterion (i) (Step 9 — "100% of episodes yield all three metrics without manual intervention" includes a successful model fit on pilot data). *Consequence if false:* no H\* is blocked; every hypothesis test (H1, H1b, H2, H2b, H3) silently switches from mixed-effects logistic regression to the pre-committed cluster-robust GEE, and this substitution is reported alongside the results, not left implicit.
- **A6 — Context fits at n=400.** Full pinning at n=400 plus task content fits every tested model's window. *Failure:* overflow makes π_full undefined at large n. *Detection:* skeleton includes one n=300 full-pinning arm; if overflow, cap sweep at largest feasible n and report it as a finding (budget wall reached before attention wall). *Gate:* PG-2, walking-skeleton pass criterion (ii) (Step 9). *Consequence if false:* restricts the scope of H1/H1b/H3 — every n=400 threshold in their binary criteria (e.g. "S(400) ≤ S(10) − 0.10") is re-registered at the largest feasible n instead, and RQ1/RQ3's headline claims are bounded to the achieved range, not silently reported as if n=400 had been reached.

## Step 6 — Pre-Registered Experiments

Grid and analysis plan inherited from digest N6/N8: Stage-1 = n ∈ {4,10,25,50,100,200,400} × 6 policies × 3 models × 150 tasks × 3 seeds (450 episodes/cell; powered for 10pp success difference at 0.8 power, α=0.05). Family-wise correction: Holm–Bonferroni over the policy family at α=0.05. Primary hypotheses declared here; everything else is exploratory.

**Power / thin-cell rule (guidance.md Part 6 item 9, Part 4 situation 5):** 450 episodes/cell is the pre-registered target for 0.8 power at the 10pp effect floor. Any cell (n, policy, model) that ends below 388 episodes/arm (the minimum for the same power/floor per the digest's analysis plan) after dropped-row exclusion (R8) is pre-declared **INCONCLUSIVE for that cell**, never scored as a null result and never silently dropped from the reported grid — it is reported with its achieved n and flagged. If a *primary* hypothesis's required cells (e.g. H1's n=10 and n=400 full-pinning cells, ≥2 of 3 models) fall below this threshold, that hypothesis as a whole is pre-declared INCONCLUSIVE rather than scored PASS/FAIL, and the paper narrows its claim to the powered subset of models/cells.

### E1 (RQ1 — when does full pinning backfire?)
- **Assumption:** A1, A2, A3, A5, A6.
- **Hypothesis H1 (binary):** Under π_full, segmented regression of logit(S) on log n detects a breakpoint (Davies p < 0.05) with 95% bootstrap CI inside [25, 400], AND S(400) ≤ S(10) − 0.10 (absolute) in ≥ 2 of 3 models.
- **Hypothesis H1b (binary):** V(400, full) ≥ V(10, full) + 0.03 (absolute) in ≥ 2 of 3 models — presence without compliance.
- **Metric:** S and V as defined in Step 5; O logged for the E1-secondary correlation (overhead ratio vs S).
- **Verification:** mixed-effects logistic regression of episode success on log n × policy, task random effect; Davies test for breakpoint; bootstrap CI (1,000 resamples); violation rate with cluster-robust SEs at episode level (digest analysis plan, hardened with the numeric thresholds above).
- **Fallback (pre-committed wording):** "Across three model families, full pinning of up to 400 simultaneously active constraints produced no detectable task-success knee; within this range the cost of exhaustive pinning is economic, not behavioral — we report the measured overhead schedule and the violation floor it buys." (Feeds F-G1 if H2 also fails.)

### E2 (RQ_INF_1 — which selective policy, and is applicability ≠ similarity?)
- **Assumption:** A1, A2, A3, A5.
- **Hypothesis H2 (binary):** At n ≥ 100 with budget k = 25% of π_full's constraint tokens, the best M3 selector is non-inferior to π_full on violation rate within δ = 0.02 (one-sided 95% CI) while O(select) ≤ 0.30 × O(full).
- **Hypothesis H2b (binary):** The applicability-classifier selector (e) achieves V at least 0.03 (absolute) lower than the best of similarity selectors (c)/(d) at n ≥ 100, Holm-corrected p < 0.05.
- **Metric:** V, O per Step 5; selector recall@k against M1 applicability labels (diagnostic); cost-adjusted success (secondary).
- **Verification:** per-budget pairwise non-inferiority tests (TOST framing for H2b's converse); Holm–Bonferroni across the 5-selector family; selector token/latency cost counted inside O (M3 spec).
- **Fallback H2:** "No budgeted selector matched full pinning within 2pp violation rate at any tested budget: for normative content, unlike evidence (COMI's domain), bounded selection is not safe — full pinning is the only reliable policy below the knee, and above it the practitioner faces a genuine dilemma, which we quantify."
- **Fallback H2b:** "Applicability-aware and similarity-based selection were equivalent within ±2pp (TOST, α=0.05): normative applicability is empirically reducible to semantic relevance for this pool, so cheap embedding selection suffices — a deployable simplification." (Equivalence margin pre-set: ±0.02.)

### E3 (RQ_INF_2 — count vs length vs density)
- **Assumption:** A2, A3, A5.
- **Hypothesis H3 (binary):** Length-matched inert padding reproduces ≤ 50% of the full-pinning success decline at n=400 (Δ_pad ≤ 0.5 × Δ_constraint, difference significant at α=0.05), AND at fixed n=100, high vs low applicability density raises V by ≥ 0.03 (absolute, p < 0.05).
- **Metric:** ΔS between n=4 and n=400 arms per condition; V by density level.
- **Verification:** subgrid per digest RQ_INF_2 — (i) padding control replacing constraints with inert same-length text, (ii) density at 3 levels holding n fixed; same mixed-effects machinery; this experiment is the internal-validity gate for interpreting E1 (t2).
- **Fallback:** "Inert padding reproduced the full decline: the 'hundreds of constraints' effect is a raw prompt-length effect, and constraint-count guidance collapses into existing long-context guidance — we report this deflationary result with the padding-equivalence evidence." (If density has no effect: applicability density is dropped from the harness as a nuisance factor, stated explicitly.)

### E4 (RQ_INF_3 — detector validity)
- **Assumption:** A1 (this experiment *tests* A1).
- **Hypothesis H4 (binary):** Dual-mode detector reaches Cohen's κ ≥ 0.80 vs human annotation on the 300-episode stratified sample (stratified by n, policy, constraint class), with programmatic checkers ≥ 0.95 raw agreement, after at most one calibration iteration.
- **Metric:** κ overall and per constraint class; per-class confusion rates.
- **Verification:** ~50 annotator-hours (digest feasibility); annotation before Stage-1 curves are interpreted; κ computed with bootstrap CI.
- **Instrument validation plan (guidance.md R2, 5-step, applied to the M4 dual-mode detector):**
  1. *Ground*: rule-based checkers are grounded directly in each constraint's own external verification spec (IFEval's programmatic checkers; RECAST-style rule-mode constraints — exact word-count/keyword/structure predicates, not a de novo rubric); LLM-judge criteria for model-based (semantic) constraints are drafted from the same source constraints' natural-language definitions.
  2. *Draft wide, refine on held-out calibration set*: the LLM-judge prompt/rubric is piloted on a held-out 50-episode calibration slice (disjoint from the 300-episode validation sample) with named refinement operations — merge constraint sub-types whose judge decisions are indistinguishable, split any sub-type showing bimodal judge behavior, remove any constraint template the judge cannot parse — before the rubric is frozen.
  3. *Validate against human raters*: 2 independent human annotators label the 300-episode stratified sample (by n, policy, constraint class); acceptance bar Cohen's κ ≥ 0.80 overall, programmatic checkers ≥ 0.95 raw agreement (H4).
  4. *Inspect confusion structure*: per-class confusion rates (already in Metric) must show disagreements concentrated between adjacent/similar constraint sub-types, not a systematic collapse of one class into another — a systematic collapse invalidates that class's curve even if aggregate κ clears 0.80.
  5. *Freeze*: the rubric and judge prompt are frozen after at most one calibration iteration (step 2's held-out refinement); no further prompt edits after Stage-1 scale-up begins.
- **Fallback (pre-committed, from N9):** "Semantic-constraint curves are withdrawn; all headline claims (H1–H3) are re-stated on the programmatically-checkable subset (≥ 70% of pool by construction), and LLM-judged constraints are reported in an appendix with judge-error bars." E1–E3 thresholds apply unchanged to the subset. The same fallback applies per-class if step 4's confusion-structure check finds a systematic (non-adjacent) collapse for a specific constraint sub-type, even when aggregate κ passes.

### Mandatory baselines

- **B0 — "why do this at all" control: π_none (no pinning).** Constraints stated once at t=1, never repeated. Justifies the problem's existence: if V(n, none) does not rise with n (pre-registered check: V(300, none) ≥ V(5, none) + 0.05, tied to A3's go/no-go), then constraint retention is a non-problem and pinning of any kind needs no study. B0 also anchors the trade-off surface's zero-overhead corner.
- **B-alt — strongest-alternative-explanation controls (budget/capability-matched):**
  - *Rival explanation 1 (for the knee, E1/E3):* "degradation at large n is a generic long-prompt effect, not constraint load." Control: **length-matched inert-padding arm** — identical token count and position, no normative content. If padding reproduces the decline, the constraint framing adds nothing (H3's explicit test).
  - *Rival explanation 2 (for the selector, E2):* "any selection at budget k works; applicability-awareness adds nothing beyond the budget cut itself." Control: **random-k selector at identical token budget k** — capability-matched floor. H2b's claim is admissible only against this floor and the similarity selectors, all at the same k.

**Confound accounting (guidance.md R3 — every design constraint names the confound it removes):**

| Design constraint | Confound removed |
|---|---|
| Length-matched inert-padding arm (E3, B-alt rival 1) | Raw prompt-length effect — without it, a success decline at large n could be "more text" rather than "more constraints." |
| Applicability-density held fixed at 3 levels while n varies independently (M1 factorial design) | Density-count entanglement — without it, "more constraints" is confounded with "more *binding* constraints." |
| Random-k selector at identical token budget k (B-alt rival 2) | Budget-cut-alone effect — without it, any selector's win over full pinning could just be "using fewer tokens," not applicability-awareness. |
| Programmatic-checker-only replication of headline analyses (A1 mitigation, E4 fallback) | Detector-error confound — without it, a measured violation-rate curve could reflect judge noise rather than agent behavior. |
| Cache-adjusted cost reported alongside raw tokens (A4) | Provider-side prompt-caching confound — without it, "token overhead" could price a cost the deployer doesn't actually pay. |
| Task random effect + cluster-robust SEs in the mixed-effects model (A5, t4) | Within-task episode non-independence — without it, per-cell significance would be overstated by treating clustered episodes as i.i.d. |

### Global fallback F-G1

If the central family {H1, H1b, H2} all fail (no knee, no compliance decay, no favorable selective trade-off), pivot the archetype from `empirical` (trade-off characterization) to `benchmark/resource` (N12's named hinge): the deliverable becomes the calibrated constraint-count sweep harness — the labeled 400-constraint pool with per-turn applicability ground truth, dual-mode verified, plus the measured cost schedule. **Pivoted abstract sentence:** "We release a 400-constraint, applicability-labeled sweep harness with calibrated dual-mode violation detection, and show that across three model families full pinning is behaviorally robust to at least 400 simultaneous constraints — making the pin-versus-select decision, within this range, a pure cost calculation for which we provide the measured schedule."

## Step 9 — Walking Skeleton

**Binary question:** "Are all three metrics (V, O, S) jointly computable end-to-end, and does at least one of them move by ≥ 5pp between n=5 and n=300 under full pinning?"

- **Arms (3):** (1) π_full at n=5; (2) π_full at n=300; (3) π_none at n=300 (B0 sanity — checks A3's binding requirement).
- **Task set:** 30 tasks from the executable-checkable suite (τ-bench-style, programmatic end-state checks), 1 mid-tier model, 2 seeds → 180 episodes.
- **Metrics:** deterministic only — programmatic checkers for all constraints (rule-based pool subset), tokenizer counts, end-state success. No LLM judge in the skeleton (A1's judged remainder is deferred to E4).
- **Cost:** ≈ 180 episodes × 6 turns × 4k tokens ≈ 4.5M tokens; tens of USD; under one day wall-clock including harness debugging.
- **Pass criterion (all four, binary):** (i) 100% of episodes yield all three metrics without manual intervention; (ii) n=300 full-pinning prompts fit the model window (A6); (iii) |metric(arm1) − metric(arm2)| ≥ 0.05 for at least one of {V, S}; (iv) V(n=300, none) ≥ V(n=5→proxy, none baseline) + 0.05 or arm-3 violation rate ≥ 0.05 (A3). — **Skeleton passed ⇒ Stage-1 is a config change** (grid values, model list, seed count in the manifest), not a code change: the harness, checkers, logging schema, and analysis script are all exercised by the skeleton.
- **Fail action:** (iii) fails → task-suite redesign per Stage-0 go/no-go (constraints too easy / never binding); (ii) fails → cap n and re-register thresholds at the cap.

## Claim–Evidence Map

| Final-abstract claim (digest Claims) | Trace | Status |
|---|---|---|
| Full pinning backfires past a knee n\*; presence ≠ compliance (Claim 1) | H1, H1b; "backfire"/"knee" defs (Step 5) | needs-experiment; fallback-covered (E1 fallback) |
| Budgeted applicability-aware selection matches full pinning at a fraction of overhead; applicability ≠ similarity (Claim 2) | H2, H2b; "approximately match"/"fraction" defs | needs-experiment; fallback-covered (both directions pre-worded) |
| Constraint count is a distinct load dimension from raw length (Claim 3) | H3; B-alt padding control | needs-experiment; fallback-covered (deflationary wording) |
| Exact n\*, gap size, best selector unknown until run (Claim 4) | acknowledged as PLACEHOLDER; CIs from M5 | supported-by-design (the spec never states numbers pre-run) |
| No prior work jointly measures V × O × S under a swept count of active constraints (Claim 5) | N4 limitations 1–6, corpus-grounded | supported-by-design (positioning claim; no experiment needed, survives all fallbacks) |
| Detector-validity claim implicit in every curve | H4; κ definition | needs-experiment; fallback-covered (subset restatement) |
| Reusable labeled harness (CO4) | A2 gate + skeleton pass; F-G1 target | supported-by-design (exists iff study runs) |

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; no numbers below are real)

Pinning a constraint into an agent's context buys its *presence* at a linear token price, but *compliance* is paid from a fixed attention budget that every co-resident rule dilutes — so the practice that guarantees each rule is seen may, at scale, be what erodes adherence to all of them. We measure where this reversal occurs. Sweeping the number of simultaneously active constraints from 4 to 400 across three model families, we isolate constraint count from raw prompt length and from applicability density, and jointly track violation rate, token overhead, and task success under full pinning, no pinning, and budgeted selective pinning. We locate the knee at which full pinning stops being wasteful and starts being harmful, test whether normative applicability reduces to semantic similarity, and gate every curve behind a human-calibrated dual-mode violation detector (κ ≥ 0.8). *(Draft; results slots empty by design.)*
