# Exchange Rates between Thinking, Sampling, and Verifying under a Fixed Dollar Budget — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All design ids (C1–C5, M1–M5, CO1–CO4, RQ1/RQ_INF_1/RQ_INF_2, t1–t5) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** A dollar spent on verification buys no accuracy by itself — it can only re-price dollars already spent on generation — whereas a thinking dollar and a sampling dollar buy accuracy directly; therefore the three levers are not symmetric currencies, and their exchange rates are necessarily functions of the allocation itself (of N, of L, of the budget level), not constants.

**判据 (deletion test).** Delete the domain nouns: "A ___ spent on ___ buys no ___ by itself — it can only re-price ___ already spent on ___ — whereas a ___ and a ___ buy ___ directly; therefore the exchange rates are functions of the allocation, not constants." The residue is empty: without *verification-as-selection-over-generated-candidates* the claim of derivative (second-order) value has no referent, and without *a shared dollar meter that charges the verifier's own tokens* (M1) the "same currency" premise is false. The sentence is not a bridge ("economics × LLM inference" is never asserted); it states a structural asymmetry — first-order vs. second-order levers inside one budget constraint — that the whole grid design (M2, M4) exists to measure. It directly generates RQ_INF_2 (verifier value must rise with N, since more candidates means more to re-price) and the C2 interaction structure.

## Step 2 — Archetype

**Primary:** `empirical` (measurement study) — per digest N12. **Secondary:** `technical_artifact` (the dollar-metered harness, CO4), strictly in support.

Downstream consequences:
- **(a) Abstract contribution slot:** a measured quantity — the accuracy-per-dollar Pareto frontier and the (non-)constancy of inter-lever exchange rates — not a new method and not a SOTA number.
- **(b) Intro logic:** "what becomes possible" = for the first time a practitioner can price a marginal dollar on each lever with the verifier's own cost inside the constraint; the intro must NOT promise to beat any baseline's accuracy, only to render an unmeasured trade-off measurable.
- **(c) Evidence standard for Results:** confidence-banded frontiers, pre-registered statistical tests, and survival of the price-perturbation sensitivity analysis (t1) — a directionally-correct anecdote or a single-price-sheet frontier does not meet the bar. Negative outcomes (constant exchange rates, universal frontier) are explicitly publishable under the fallbacks below.

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Check: the claim is not "econometrics and test-time scaling were never connected." It is that one measurable quantity (the verifier's own metered cost) has been left outside every prior budget constraint (N4.1–N4.6), making a specific asymmetry unmeasurable. **PASS.**
- **Is the method mere Synthesis?** Check: M1–M5 assemble existing components (budget forcing, best-of-N, majority vote), but the contribution is not the assembly — it is the measurement the assembly gates: matched-cost bins, MRS estimation, cross-family permutation test. The paper's claim survives replacing every component with an equivalent. **PASS** (empirical archetype makes synthesis-of-instruments legitimate; the finding, not the pipeline, is the contribution).
- **Load-bearing verbs:** *meter, price, gate (configurations into matched-cost bins), isolate (selection value from coverage via the oracle arm), measure, falsify*. No integrate/unify/leverage/combine in any claim. **PASS.**
- **Abstract-opening rule:** opens with the asymmetry (verification's derivative value inside a shared budget), not with "LLMs are increasingly used… however… we introduce". Enforced in Abstract v0 below. **PASS.**

No framing repair needed; the digest's framing already centers the cost-model absence (N4 limitation 2) rather than a bridge.

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1; added Phase A re-run, 2026-07-04 — Part 6 self-check item 1 previously had no explicit one-sentence estimand):** the marginal rate of substitution in accuracy-per-realized-dollar among the thinking-length (L), sample-count (N), and verifier-call (V) levers, estimated per (task family F, matched-cost budget bin 𝔅_k) cell from the fitted accuracy surface Âcc = f̂(L,N,V,c); the unit of analysis is one (family, budget-bin) cell, the reference population is the four task families × three budget levels under the frozen price sheet P, and the decision it feeds is a practitioner's choice of which lever to fund with the next marginal dollar at deployment.

**Notation.** Query q from task family F ∈ 𝔽 = {math, code, MCQ, openQA}. Allocation a = (L, N, V): thinking-token cap L, sample count N, verifier mode V ∈ {0 = majority vote, v_cheap, v_strong}. Frozen price sheet P = (p_in, p_out) per model, dollars per token (M1). Realized cost c(q, a) = Σ_{calls} (p_in·tok_in + p_out·tok_out), summed over generation **and** verifier calls. Budget levels B ∈ {B_1, B_2, B_3}; matched-cost bin 𝔅_k = {a : |E[c(·,a)] − B_k| ≤ 0.10·B_k}. Accuracy Acc_F(a) = mean over q∈F of grader output g_F(q, a) ∈ {0,1}. Dollar-share (mix) vector m(a) = (s_think, s_sample, s_verify) ∈ Δ², computed from metered token attribution: s_verify = verifier dollars / total dollars, s_think = marginal dollars of L beyond L_min at N=1 attribution, s_sample = remainder.

Load-bearing adjectives from digest Claims → computable definitions:

| adjective / verb | formal definition | measured by |
|---|---|---|
| **efficient / dominated** | a is efficient in (F, 𝔅_k) iff no a′∈𝔅_k has Acc_F(a′) ≥ Acc_F(a) and E[c] ≤ E[c(a)], one strict | non-dominated set over (mean realized cost, accuracy) per family × bin (M5) |
| **exchange rate (MRS_ij)** | MRS_ij(a) = (∂Âcc/∂$_i)/(∂Âcc/∂$_j) at a, from the fitted surface Âcc = f̂(L,N,V,c) | local finite differences on monotone-spline / GAM fit (M5) |
| **non-constant** (Claim 2) | ∃ lever pair (i,j), budgets k≠k′: MRS_ij(𝔅_k)/MRS_ij(𝔅_{k′}) ≥ 2 with disjoint 95% bootstrap CIs | H1b test |
| **frontier shape** | the tuple (mix composition {m(a): a efficient}, elbow = argmax curvature of spline fit, MRS signs) | M5 |
| **stable across families** (Claim 3) | Aitchison distance d_A between families' efficient-set mix compositions at matched 𝔅_k not significant under permutation test (10,000 perms, Holm α=0.05) | H2 test |
| **verifiability ordering** | fixed a priori: code (executable) > math (exact match) > MCQ (option match) > openQA (rubric) | design constant; used as the predicted rank order of s_verify |
| **verify-heavy / think-heavy** | family F is verify-heavier than F′ at 𝔅_k iff s_verify at F's max-accuracy efficient point exceeds F′'s by ≥ 0.10 (absolute share) | H2b criterion |
| **interior optimum** (of L) | ∃ L* ∉ {L_min, L_max}: Acc(L*,·) > Acc(L_min,·) + 0.02 and > Acc(L_max,·) + 0.02 at fixed (N,V,𝔅) | H1c criterion |
| **matched budget** | membership in 𝔅_k (±10%), with regression adjustment on realized c within bin | M2 + M5 |
| **accuracy-per-dollar** | Acc_F(a) / mean realized c(q,a) within 𝔅_k | M1 + grader |

Deleted adjectives: "largely orthogonal" (from digest N0 draft abstract) — not measurable as stated; replaced by the interaction tests of H3. "Cheaply-verifiable" — replaced by the fixed verifiability ordering above.

## Assumptions (A1..A7)

**Consequence column added Phase A re-run (2026-07-04)** — guidance.md §3.2 requires every A\* to fill five slots (assumption, failure_mode, detection, gate, **consequence**: "what happens to which H\* if it fails — degrade, restrict scope, or block"); the table previously carried only four (goal.md §3 item 5 / guidance.md Part 6 item 4).

| id | assumption | failure mode | detection (gate) | consequence (which H\* / scope) |
|---|---|---|---|---|
| A1 | Budget forcing controls L: the open-weight reasoning model respects the thinking cap and still emits a parseable answer | model ignores cap or degenerates when truncated | Skeleton gate: ≥95% of generations within L±10% and parseable; else swap model before any grid | **Blocks** all of E1/E2/E3 (H1a–H3b) — the L axis is undefined without a compliant model; per Part 4 situation 8, this is a pre-grid gate, not a post-hoc restriction. |
| A2 | Cost commensuration (C1): all three levers reduce to one dollar unit under a frozen price sheet, and conclusions are not artifacts of that sheet | rankings flip under plausible price perturbations | ±3× price-ratio sensitivity re-run (t1 mitigation); dual reporting in output-token equivalents (M1) | **Degrades** H1b/H3a/H3b (non-constancy and interaction claims) to price-sheet-conditional findings; Claim 7 (price-sheet robustness) becomes `fallback`-status rather than `held` if rankings flip. |
| A3 | Graders are valid: exact match (math/MCQ), test execution (code), rubric judge for openQA with human agreement κ ≥ 0.7 | rubric judge circular with the verifying lever (t5) | 200-item double-annotated audit; judge model ≠ in-budget verifier; openQA family excluded from claims failing the audit | **Restricts scope** of H2a/H2b (frontier-shape stability, verifiability ordering) to the three surviving families; does not block E1/E3, which do not depend on the openQA grader. |
| A4 | Headroom: base accuracy at B_1 floor lies in [0.15, 0.85] per family, so levers can move it | ceiling/floor saturation makes MRS unidentifiable | Skeleton pilot accuracy check; swap benchmark slice (e.g., MATH-500→AIME mix) if violated | **Blocks** MRS estimation (H1b) for the saturated family/budget cell only — that cell is reported `allocation-moot` (per the B0 exclusion rule below), other cells unaffected. |
| A5 | Matched-cost bins are populable: ≥8 grid configurations land in each 𝔅_k (C4) | realized-cost variance scatters configs outside ±10% bins | Pilot token-statistics run before the grid; widen to ±15% as a pre-declared amendment if <8 (logged) | **Degrades** power for H1a/H1b/H1c in the affected bin; per Part 6 item 9, a bin that still fails to populate after the ±15% amendment is pre-declared **INCONCLUSIVE** for that bin, never scored PASS/FAIL. |
| A6 | Verifiers discriminate above chance: cheap verifier AUC ≥ 0.60 against ground-truth labels on pilot candidates (t2) | verify axis measures a broken instrument, not the lever | Skeleton gate: AUC computed on pilot; if <0.60 replace cheap verifier before Stage 1 | **Blocks** E3 (H3a/H3b) and any verify-heavy reading of E1/E2 — an undiscriminating verifier makes the V axis measure noise, not the lever; gates before Stage 1, per Part 4 situation 8. |
| A7 | Sampling produces diversity: at T=0.8, N=16 yields ≥3 distinct final answers on ≥50% of pilot questions | degenerate pools make N and V axes collinear | Skeleton distinct-answer count; raise T or add nucleus perturbation if violated | **Blocks** identifiability of the N×V interaction (H3a) — collinear N/V axes make the interaction term inestimable; triggers the temperature/nucleus remedy before any grid point is scored. |

**Instrument validation (guidance.md R2; added Phase A re-run, Part 6 item 6):** two instruments in this table are LLM-judge-class and require the full 5-step R2 sequence, not only the acceptance threshold already named. (i) *Verifier (A6)*: ① grounded in the task's own gold labels (exact-match/test-execution ground truth, not a proxy); ② the cheap/strong verifier prompts are drafted and refined on the pilot's held-out candidate pool before Stage 1; ③ validated by AUC ≥ 0.60 against ground truth (already gated above); ④ confusion inspection — pilot false-accepts/false-rejects are inspected for whether errors cluster near the decision boundary (adjacent-difficulty candidates) rather than collapsing systematically onto one class; ⑤ frozen (hashed) before the Stage-1 grid runs, per M2's bin-freezing convention. (ii) *OpenQA rubric judge (A3)*: ① rubric criteria grounded in the benchmark's own published grading rubric (FRAMES/SimpleQA); ② refined on a calibration slice disjoint from the 200-item audit set, with named merge/split of rubric categories if two human raters disagree systematically on a category; ③ validated at κ ≥ 0.7 against two human raters (already gated above); ④ confusion inspection — disagreements audited for adjacency (partial-credit boundary cases) vs. systematic collapse, which would instead redirect openQA per Part 4 situation 7; ⑤ frozen before Stage-2 scale-up. Asserted validation numbers without this protocol are treated as absent per R2.

## Step 6 — Pre-Registered Experiments

Design constants (frozen at pre-registration, per M2/M3/M5 and the N8 analysis plan): grid L∈{512,1024,2048,4096}, N∈{1,2,4,8,16}, V∈{0, cheap, strong}; T=0.8; 3 budget levels; pilot ≥300 questions/family (math, code), Stage 2 ≥500/family (all four); paired bootstrap 10,000 resamples; permutation tests 10,000 perms; α=0.05 Holm–Bonferroni across family pairs and budget levels; oracle-verifier arm at every grid point (M4).

**Power / INCONCLUSIVE rule (guidance.md §3.4 R8, Part 6 item 9, Part 4 situation 5; added Phase A re-run — H1a/H1b/H1c/H2a/H2b/H3a/H3b previously had only binary PASS/FAIL wording with no under-powered branch):** n=300/family (pilot) is pre-registered to give power ≥0.8 for the 5pp reference contrast at Acc≈0.6 (per the E1 Verification note); this is re-checked empirically once pilot data lands. Any (family, budget-level) cell, or any specific lever-pair MRS/interaction test, whose *realized* n or bin population (post A5 gate) yields achieved power <0.8 for its own pre-registered effect floor is **pre-declared INCONCLUSIVE for that cell/test only** — never scored PASS, never scored FAIL, and never silently folded into an aggregate. INCONCLUSIVE cells are excluded from the "≥1 of 2 pilot families," "≥2 of 3 budget levels," and "≥2 of 6 family pairs" aggregation counts in H1a/H1b/H2a rather than counted against them. If the *central* test of an experiment (e.g., H1a's own pilot-family pair) is underpowered, Stage 2's n is raised to 500 (the pre-declared amendment already named in E1's Verification note) before that experiment is scored at all.

### E1 (RQ1) — Frontier shape and exchange rates on pilot families
- **Assumption:** A1, A2, A4, A5, A6, A7.
- **Hypothesis (binary):**
  - **H1a (mixed allocations matter):** On ≥1 of 2 pilot families and ≥2 of 3 budget levels, some mixed allocation (≥2 levers each holding ≥20% dollar share) beats the best single-lever arm in the same 𝔅_k by **≥3 accuracy pp**, Holm-corrected paired-bootstrap p < 0.05.
  - **H1b (non-constant exchange rates):** For ≥1 lever pair on ≥1 pilot family, MRS at B_1 vs B_3 differs by **factor ≥2** with disjoint 95% bootstrap CIs.
  - **H1c (interior thinking optimum):** On ≥1 pilot family, ∃ interior L* per the Step-5 definition (both margins ≥2 pp).
  - E1 **passes** iff H1a AND (H1b OR H1c).
- **Metric:** Acc_F(a); realized c(q,a); accuracy-per-dollar; MRS_ij (all as defined in Step 5, digest N8 metrics).
- **Verification:** full matched-cost grid (M2) with M1 metering; frontier extraction + GAM fit + finite-difference MRS with bootstrap CIs (M5); all six digest N8 baselines run in the same bins. n=300/family gives power 0.8 for a 5 pp paired contrast at Acc≈0.6 (digest analysis plan); the 3 pp criterion is therefore tested with the paired (not independent) bootstrap, which the pilot must show reaches power ≥0.8 or n is raised to 500 (pre-declared amendment).
- **Fallback F1 (pre-committed wording):** "Under a dollar-denominated budget that charges the verifier's own tokens, mixed think/sample/verify allocations buy no measurable accuracy over the best single-lever policy at matched cost, and exchange rates are budget-invariant constants: test-time compute levers are interchangeable currencies, so deployment policy reduces to picking one lever by engineering convenience — a cost-audited simplification of the allocation literature." (Covers H1a and H1b/H1c failure; the frontier and constant-rate table remain the deliverable, CO2 survives.)

### E2 (RQ_INF_1) — Cross-family stability of frontier shape
- **Assumption:** A1–A7 (A3 load-bearing for openQA).
- **Hypothesis (binary):**
  - **H2a (shape is family-specific):** The permutation test on Aitchison distance between efficient-set mix compositions rejects equality for **≥2 of 6 family pairs** at Holm-corrected α=0.05, at ≥2 of 3 budget levels.
  - **H2b (verifiability ordering):** s_verify at the max-accuracy efficient point satisfies code ≥ math ≥ MCQ ≥ openQA with **code − openQA ≥ 0.10** absolute dollar share, at ≥2 of 3 budget levels.
  - E2 **passes** iff H2a AND H2b.
- **Metric:** mix vector m(a); Aitchison distance d_A; frontier-shape stability statistic (digest N8).
- **Verification:** Stage-2 identical grid over 4 families × ≥500 questions, 3 models (small open-weight, large open-weight, one API model as partial replication only — N6 feasibility mitigation); permutation test 10,000 perms; Holm across the 6 pairs × 3 budgets; conclusion asserted only for effects surviving the ±3× price perturbation (A2).
- **Fallback F2 (pre-committed wording):** "The accuracy-per-dollar frontier's shape is invariant across verifiability classes: a single allocation policy, tuned on cheap-to-grade math, transfers to code, MCQ, and rubric-graded open QA at matched dollar budgets — evidence that efficient test-time allocation is a property of the compute levers, not the task family." (Digest Claim 3 explicitly pre-registers this negative as publishable.) If H2a passes but H2b fails (ordering contradicts verifiability), the fallback claim is: "frontier shape varies by family but is NOT predicted by verifiability class; we report the observed ordering and reject the verifiability account."

### E3 (RQ_INF_2) — Interaction structure of the verifier lever
- **Assumption:** A1, A5, A6, A7.
- **Hypothesis (binary):**
  - **H3a:** Likelihood-ratio test of the N×V interaction term in Âcc ~ f(L, N, V-mode, realized c) rejects the additive model at Holm-corrected p < 0.05 **with positive sign**, on ≥1 pilot family.
  - **H3b:** L×V term significant at Holm-corrected p < 0.05 **with negative sign**, same model.
  - E3 **passes** iff H3a (H3b reported either way; H3b alone does not rescue E3).
- **Metric:** interaction coefficients + LR statistics; realizable-vs-oracle selection gap at fixed (L,N) across V modes (M4).
- **Verification:** within-grid GLM/GAM with pre-specified terms; cheap vs. strong vs. majority-vote vs. oracle contrasts at fixed (L,N); paired bootstrap on coefficients. This is the direct test of the Step-0 asymmetry (derivative value of verification ⇒ value increasing in N).
- **Fallback F3 (pre-committed wording):** "Lever values are additively separable at deployment-relevant budgets: the marginal value of a verifier dollar is statistically flat in N and L within our grid, so exchange rates can be tabulated once per lever rather than per allocation — a two-parameter cost model suffices for budget planning." (Note: F3 contradicts the Step-0 asymmetry as a measurable effect at these budgets; if triggered, Step-0 is restated as a bounded claim — the asymmetry exists structurally but is below measurement resolution in [B_1, B_3] — and F-G1 is evaluated.)

### Mandatory controls

- **B0 — "why do this at all" control:** the **fixed-default floor** (L=512, N=1, V=0), leftover budget unspent, run at every budget level and family (= digest baseline "Single-sample short-CoT floor"). Pre-registered gate: every family × budget frontier must beat B0 by **≥5 pp accuracy** at matched or lower cost; any cell failing this is reported as "allocation is moot here" and excluded from exchange-rate claims. B0 is what shows a budget-allocation problem exists at all.
- **B-alt — strongest-alternative-explanation control:** the rival explanation for any verify-heavy result is **"it's just coverage plus free selection"** — more samples with majority vote, no paid verifier ([BrownMonkeys] coverage + self-consistency). Control: for every verify-heavy efficient point (L, N, V>0), run the **budget-matched majority-vote arm** (L, N′, 0) where N′ absorbs the verifier dollars (same 𝔅_k, ±10%). The verifier-lever claim (E3, and any verify-heavy reading of E1/E2) is asserted only where (L,N,V) beats (L,N′,0) with Holm-corrected paired-bootstrap p<0.05. The oracle arm (M4) additionally separates coverage from selection quality, capping what any verifier could have bought.

### Global fallback F-G1 — archetype pivot

If the central hypothesis family fails jointly (E1 fails AND E3 fails; frontier degenerate, rates constant, no interactions), the paper pivots from `empirical` finding to `benchmark/tool` (CO4 promoted to primary): the deliverable becomes the dollar-metered harness plus the first cost-audited null result. Pivoted abstract sentence, pre-committed: **"We release a dollar-metered test-time-compute harness that charges generation and verification in one budget, and use it to establish a cost-audited null: across math and code at three budget levels, thinking, sampling, and verifying trade at statistically constant exchange rates, so practitioners can allocate by convenience — and any future claim of allocation gains must beat this metered baseline."**

## Step 9 — Walking Skeleton

**One binary question:** *at matched dollar cost (±10%), do the three pure strategies produce distinguishable accuracy on one family — and does every instrument (cost meter, L-cap, bins, verifier, grader) behave?*

- **Arms (3):** (i) B0 floor (L=512, N=1, V=0); (ii) all-sampling: (L=512, N≈budget, V=0) majority vote; (iii) sample-then-verify: (L=512, N/2, cheap verifier scoring all candidates) — all targeted at one budget B_2.
- **Task set:** 50 MATH-500 questions (exact-match grader only; deterministic).
- **Metrics (deterministic only):** exact-match accuracy; M1-metered realized dollars per query; L-cap compliance rate; bin hit-rate; verifier AUC vs. ground truth; distinct-answer count at N=16 (checks A1, A5, A6, A7 in one run).
- **Cost:** 50 q × 3 arms × ≤10 total generations × ~4K tokens ≈ 6×10⁶ tokens ≈ 2–4 A100-hours on a 7–14B open-weight reasoning model with vLLM (≈ <$25 API-equivalent). Wall-clock: under one day including harness debugging.
- **Pass criterion (explicit):** all arms land within ±10% of B_2 realized cost; L-cap compliance ≥95%; verifier AUC ≥0.60; ≥50% of questions show ≥3 distinct answers at N=16; and any pairwise arm gap |ΔAcc| ≥ 5 pp is resolvable by the paired bootstrap at n=50 (sanity, not inference). **Skeleton passed ⇒ the full Stage-1 grid is a config change** (the grid file enumerates (L,N,V,B) tuples consumed by the same runner; no new code paths), **not a code change.** Any arm failing its gate blocks the grid and triggers the mapped A-id remedy.

## Reference-cache update note (Phase A re-run, 2026-07-04)

`discussion/reference_candidates.jsonl` was rebuilt into the canonical schema (goal.md §1) and re-selected against all 150 harvested candidates plus the 9 works `digest.md` N3 already cited from the OpenReview corpus. One new **method-twin** surfaced that N3's OpenReview-only corpus search had not seen: `ComputeAccuracy251224776` (arXiv:2512.24776, "Compute-Accuracy Pareto Frontiers for Open-Source Reasoning Large Language Models") maps an empirical FLOPs-only compute-accuracy Pareto frontier across 19 open-source reasoning models and finds a task-dependent saturation knee. Per guidance.md Part 4 situation 6 (concede-and-differentiate): **concede** the frontier-mapping/non-dominated-set methodology (M5) is not new relative to this work; **differentiate** on (a) the three-lever decomposition (L, N, V) vs. its single FLOPs axis, (b) the dollar meter charging the verifier's own cost vs. its architecture-only FLOPs accounting, and (c) matched-cost bins with bootstrap MRS vs. its post-hoc scatter-plot frontier. Claim 1 in the Claim–Evidence Map below is unaffected (the three-lever, dollar-denominated, verifier-cost-inclusive measurement remains absent from this new record too) — no repositioning of Claim 1 required, but `paper_draft.md`'s Related Work section (Phase E, not yet re-touched by this Phase A pass) must add one concede-and-differentiate sentence for this record before Phase G's `stale_claim_after_verdict`/uncited-twin check, per goal.md §7.

## Claim–Evidence Map

| # | claim (as the final abstract will state it) | trace | status |
|---|---|---|---|
| 1 | Prior budget constraints never charge the verifier's own cost; the three-lever dollar-denominated measurement is new | digest Claim 1, N3/N4 (corpus-grounded) | supported-by-design (re-verify vs. arXiv per N7 absence_comment before submission) |
| 2 | The three levers are metered in one dollar unit, verifier tokens included | M1 + Step-5 c(q,a) definition; A2 gate | supported-by-design |
| 3 | Exchange rates are non-constant: budget-dependent and interaction-bearing | H1b, H3a/H3b (digest Claim 2) | needs-experiment; fallback-covered (F1, F3) |
| 4 | Mixed allocations beat pure-lever policies at matched cost | H1a; gated by B0 and B-alt | needs-experiment; fallback-covered (F1) |
| 5 | Frontier shape is family-specific and ordered by verifiability | H2a + H2b (digest Claim 3) | needs-experiment; fallback-covered (F2, both branches) |
| 6 | Verifier value is derivative: increasing in N (Step-0 asymmetry made measurable) | H3a + B-alt control + oracle gap | needs-experiment; fallback-covered (F3 → bounded-claim restatement) |
| 7 | Conclusions are price-sheet-robust | A2 ±3× perturbation + token-unit dual report | supported-by-design (procedure), needs-experiment (outcome) |
| 8 | A reusable dollar-metered harness is released (CO4) | M1–M5 implementation + skeleton | supported-by-design; becomes primary under F-G1 |

No abstract claim exists outside this table; any new claim added later must be registered here with an H-id first.

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — written before any experiment; numbers pending; wording obeys Step 3]**
>
> A dollar spent on verification buys no accuracy by itself — it only re-prices dollars already spent on generation — yet no existing budget analysis charges the verifier's own cost against the budget it serves. We meter all three test-time levers — chain-of-thought length, sample count, and verifier calls — in one dollar unit, gate a 3D allocation grid into matched-cost bins at three budget levels, and measure the empirical exchange rates and accuracy-per-dollar Pareto frontier across task families spanning executable, exact-match, and rubric-graded verifiability. Budget-matched majority-vote and oracle-selection controls isolate what verification itself buys from what coverage buys for free. We test pre-registered hypotheses that exchange rates are non-constant (budget- and interaction-dependent) and that frontier shape follows the family's verifiability ordering, reporting confidence-banded frontiers and marginal rates of substitution either way.

(~128 words.)
