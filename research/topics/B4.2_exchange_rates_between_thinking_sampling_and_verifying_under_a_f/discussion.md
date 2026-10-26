# Discussion — B4.2 思考-采样-验证的兑换率 / "Exchange Rates between Thinking, Sampling, and Verifying under a Fixed Dollar Budget"

> Auto-research-discussion document (6 stages, each with an internal critic→refine pass).
> Status: **KEEP-TOP**. Target: **ICLR 2027** (abstract **Sep 18, 2026**, paper **Sep 25, 2026**); the competitive pressure is acute — vendors are already publishing one slice of this analysis (Stage 2), so **ship before the crowd**.
> Sources: `README.md` (seed, [GIVEN]), `digest.md` (reverse digest; C1–C5 / M1–M5 / CO1–CO4 / RQ1, RQ_INF_1, RQ_INF_2, t1–t5 ids reused here), `paper.md` (pre-registered spec with formal estimand), `discussion/` (July working folder incl. `paper_draft.tex`, `experiment_design.md`).
> **Work-in-progress note:** a WIP archive exists at `topics/B4.2_exchange_rates_between_thinking_sampling_and_verifying_under_a_f.zip` (alongside the topic folder), and `discussion/` already contains a compiled `paper_draft.pdf` (July 4–5). This document consolidates the current plan on top of that material; it does not restart it.
> Tag conventions: **[VERIFY]** = channel-relayed number, must be independently verified and must never be cited in submitted text unverified; **[GIVEN]** = from the seed README.

---

## Stage 1 — Problem definition (precise estimand)

**Core question [GIVEN]:** Under a fixed dollar budget, what are the substitution rates among lengthening CoT ("thinking"), drawing more samples ("sampling"), and spending on a verifier ("verifying") across task families — and what does the efficient accuracy-per-dollar frontier look like?

**Estimand (v1, from `paper.md` Step 5).** For task family `F` and matched-cost budget bin `𝔅_k` under a frozen price sheet `P`: the **marginal rate of substitution** `MRS_ij = (∂Âcc/∂$_i)/(∂Âcc/∂$_j)` between levers `i, j ∈ {thinking L, sampling N, verifying V}`, estimated from the fitted accuracy surface `Âcc = f̂(L, N, V, c)` over a matched-cost grid in which **the verifier's own token cost is charged inside the same budget** — plus the per-family non-dominated (cost, accuracy) frontier with its allocation-mix composition `(s_think, s_sample, s_verify)`, and a cross-family stability verdict on frontier shape.

Three registered hypotheses (digest N9): **H1** exchange rates are budget-dependent, with an interior optimum for L; **H2** frontier shape is family-specific, ordered by verifiability (code > math > MCQ > open QA in verify-heaviness); **H3** interactions are non-additive (N×V positive, L×V negative).

**Critic:**
1. "Verifying" is one word for two different levers: *selection* (score N candidates, pick one) and *iterative verification* (check-then-revise). The grid instantiates only selection; the estimand should say so or reviewers will read "verifying" as covering revision loops it never measures.
2. `MRS` from finite differences on a fitted surface is fragile at frontier edges (few grid points, monotone-spline extrapolation); the estimand as stated implies a precision the grid may not support.
3. Dollar-denomination is the paper's identity, but a dollar is a price-sheet artifact (digest C5/t1). The estimand must pre-commit to what survives a price change: MRS *signs and orderings*, not MRS values.
4. The unit "accuracy" flattens task families with different metrics (pass@1-after-selection for code vs rubric score for open QA); cross-family shape comparison must be invariant to the per-family metric scale.

**Refined:**
- **Scope sentence (verbatim for the paper):** "Verifying" in this work = *post-hoc selection over N candidates by a priced judge*; sequential revise-with-feedback is out of scope and named as future work. Titles/claims use "verifier-based selection" where ambiguity could mislead.
- **Two-tier estimand:** Tier 1 (primary, price-robust) — the *ordering* of levers by marginal accuracy-per-dollar and the *sign pattern* of interactions, per (family, budget bin), required to survive a ±3× price-ratio perturbation (t1 mitigation). Tier 2 (secondary, dated) — numeric MRS values under the frozen Aug-2026 price sheet, published as a dated appendix table explicitly marked as pricing-regime-specific.
- MRS is reported only at interior frontier points with ≥ 3 neighboring grid cells; edge cells get qualitative dominance statements only.
- Cross-family comparison operates on the **allocation-mix composition** (a point on the simplex Δ², scale-free) rather than raw accuracy, exactly per `paper.md`'s Aitchison-distance permutation test — this is already metric-invariant; keep it.

---

## Stage 2 — Motivation (why now, binding constraint)

**Why now.**
1. **Vendors are publishing one slice of this analysis themselves.** Relayed vendor-chart numbers for GPT-5.6: reasoning-effort step **Xhi→Max: 53.6%→52.7% at +42% cost** (i.e., a *negative* marginal return on the thinking lever at the top end) **[VERIFY — channel-relayed; never cite unverified; locate the vendor's published chart/system card before any use]**; and multi-agent scaling **1→4→16 agents: +3.1pp then +1.11pp at ~6× cost** **[VERIFY — same status]**. If accurate, vendors are already publicizing *single-lever* cost curves — which makes the *cross-lever exchange rate* the obvious next question, and whoever publishes the 3-way analysis first owns the framing. This is the "ship before the crowd" pressure.
2. **The overthinking literature just made cost-aware evaluation mainstream** (arXiv:2604.10739 proposes cost-aware evaluation; 2507.14417 shows inverse scaling with thinking length; 2502.08235) — but it prices exactly one lever. The field has accepted the premise (accuracy must be cost-normalized) without the full consequence (all three levers priced in one budget, verifier cost included).
3. **Deployment reality:** every production agent stack today makes an implicit (L, N, V) allocation; none of its operators can answer "what does the next marginal dollar buy on each lever?" because no measured exchange rate exists.

**Binding constraint:** prior allocation analyses denominate budgets in FLOPs, tokens, or samples and treat the verifier as free (digest N4). The moment the verifier's own tokens are metered inside the constraint, the question changes from "does test-time scaling help" to "which lever do I fund" — and that question has no published answer.

**Critic:**
1. Both headline numbers are unverified relays; if they cannot be verified, motivation point 1 collapses to "vendors publish cost charts," which is weaker but still true. The doc needs the degraded version pre-written.
2. "Ship before the crowd" is a *strategy*, not a motivation; the paper text needs the scientific version (single-lever cost curves are uninterpretable for allocation decisions because levers interact — C2).
3. Point 3 asserts practitioner need without a single concrete workload; a reviewer can dismiss it as hand-waving.

**Refined:**
- **Degraded fallback for point 1 (pre-written):** "Vendor evaluations increasingly report accuracy against inference cost for *individual* levers (reasoning-effort tiers; agent-count scaling) [cite verified public charts only]. Single-lever curves cannot answer an allocation question: whether the marginal dollar should buy thinking, sampling, or verification depends on interactions no vendor chart measures." All relayed numbers stay in internal notes until verified against a public vendor artifact; the submission carries only verifiable citations.
- Scientific motivation foregrounded: because levers interact (H3), single-lever cost curves are not merely incomplete but *misleading* — e.g., the value of the Xhi→Max thinking step cannot be assessed without knowing what the same +42% spend buys as samples-plus-selection. **[VERIFY the 42% figure before even this illustrative use; otherwise use abstract placeholders.]**
- Concrete workload anchors (one per family): a math-tutoring API, a code-review bot with executable tests, a research-QA assistant — each with a per-query cost ceiling, each currently allocating by folklore.

---

## Stage 3 — Related work (positioning + boundary statements)

1. **Overthinking / thinking-length line** — **arXiv:2604.10739** (cost-aware evaluation for reasoning), **arXiv:2507.14417** (inverse scaling: longer thinking can hurt), **arXiv:2502.08235** (overthinking analysis) **[VERIFY exact scope of each at writing time — IDs supplied by the sweep; confirm 2502.08235's precise contribution before naming it]**; plus corpus twin [CoTLength, OpenReview:6QDFsYxtI1] (inverted-U theory). *Boundary:* this line establishes that the thinking lever has an interior optimum and that cost-normalization matters — **for one lever**. None trades thinking against sampling or verification, and none charges a verifier inside the budget. B4.2's delta is the 3-way substitution analysis under a single dollar constraint.
2. **Compute-optimal test-time scaling** — [SnellTTC, OpenReview:4FWAwZtd2n] (proposer–verifier allocation at matched FLOPs). *Boundary:* optimizes *strategy choice per prompt* under FLOPs; verifier cost unpriced; single task family; no dollar meter, no cross-family stability test.
3. **Repeated-sampling scaling** — [BrownMonkeys, arXiv:2407.21787] (coverage scales log-linearly in N). *Boundary:* coverage ≠ deliverable accuracy; the selector that converts coverage into accuracy is exactly the priced verifier we meter. We reuse their coverage framing and the oracle-selection upper bound.
4. **Sample-then-verify theory** — [VerifierFreeSuboptimal, OpenReview:beeNgQEfe2], [OTVerify, OpenReview:BBDhQJh6GB], [BestOfMajority, OpenReview:a6CVQpjbXq], [RerankingLaws, OpenReview:rhCgizNupi]. *Boundary:* bounds in H, n, coverage, ROC — verifier treated as an oracle-like resource with **no cost term**; cannot answer what a marginal dollar buys. These motivate our verifier-strength arms and the oracle band, and our measurement is the empirical complement their cost-free theory lacks.
5. **Two-lever allocation precedent** — [AsymVerify, OpenReview:hxL4Uf9tR3] (explore-vs-verify split for web agents). *Boundary:* the closest existing allocation study; two levers, one domain, cost in tool calls not dollars, no thinking-length axis. B4.2 generalizes to three levers × four families × one dollar meter.
6. **Step-level token budgeting** — [PlanAndBudget, OpenReview:ctspw4CqbS]. *Boundary:* allocates tokens *within* one reasoning episode; never across levers.
7. **Possible unswept adjacents [VERIFY - action item]:** any 2025–2026 "inference economics" or "cost-optimal test-time compute" measurement papers, hybrid parallel/sequential scaling studies, and vendor system cards with multi-lever charts. A targeted arXiv sweep for dollar-denominated allocation studies is a **week-1 blocking task** — this is the topic most likely to be scooped in-quarter, and the novelty statement must be re-checked against anything the sweep surfaces.

**Critic:**
1. The boundary statements are individually solid, but the *aggregate* landscape (items 1–6) makes the delta look like "we did the cross-product" — the related-work section must state why the cross-product is not incremental: pricing the verifier changes the *question type* (from scaling curves to substitution rates), and the empirical answer (H1–H3) is not derivable from any subset of priors.
2. Item 7 is the highest-stakes entry and currently has no owner/date.
3. The GPT-5.6 vendor charts (Stage 2), if verified, are themselves *related work* — vendor-published single-lever frontiers — and belong in this section, not only in motivation.

**Refined:**
- Add the anti-incremental paragraph: the union of priors yields three single-axis curves and one two-lever domain study; substitution rates are *joint* quantities — they live in the interaction terms (N×V, L×V) that no single-axis study can estimate even in principle. The measured sign pattern of those interactions is new information, not aggregation.
- Week-1 action item with gate: arXiv sweep (owner: paper lead, due with the pilot go/no-go). If a dollar-denominated 3-way study surfaces, pivot per pre-declared fallbacks: (a) cross-family stability + verifiability ordering as the headline (if the rival is single-family), or (b) the price-perturbation-robust ordering claim (if the rival uses one price sheet naively).
- Vendor charts, once verified, are cited in related work as "vendor-reported single-lever cost curves" — establishing both timeliness and the gap.

---

## Stage 4 — Sub-problems (each with the hard part named)

**SP1 — Cost commensuration (digest C1).** Map (L, N, V) onto one dollar unit: output tokens ≠ input tokens in price, samples multiply both, the verifier reads candidates (input) and emits judgments (output); open-weight models need a defensible GPU-hour-amortized price. **Hard part:** any single price sheet is contestable — the design must make headline claims *invariant* to the contestable part (dual reporting in normalized output-token equivalents + ±3× price-ratio sensitivity), or the whole paper is "one price sheet's opinion."

**SP2 — Lever interaction structure (C2).** Estimate exchange rates that are functions of the allocation itself (verifier worthless at N=1; longer candidates cost more to judge). **Hard part:** the grid must be dense enough to identify N×V and L×V interaction terms with confidence bands, under a combinatorial budget — grid design *is* power analysis here.

**SP3 — Controlling the thinking axis (t-mitigation in digest N6).** Enforce thinking-token caps L. **Hard part:** commercial APIs expose only coarse or hidden thinking budgets, so precise L-control exists only on open-weight models with s1-style budget forcing — the axis is most controllable exactly where pricing is least "real." Resolution: open-weight primary instrument, API partial replication on the (N, V) plane.

**SP4 — Stochastic realized cost under matched budgets (C4).** Models cannot be forced to emit exactly L tokens; realized cost varies per query. **Hard part:** "matched budget" must be an *empirical* property (matched-cost bins ±10% on realized cost, regression adjustment within bins) — naive nominal-setting comparison would systematically favor whichever lever under-spends its nominal budget.

**SP5 — Verifier-quality and grader confounds (t2, t5).** A weak verifier makes the verify lever look bad; the open-QA grader is itself verifier-like. **Hard part:** deconfounding requires a *band*, not a point: majority-vote floor (zero verifier dollars), cheap and strong verifier arms, and a zero-cost oracle-selection ceiling per grid point; open-QA graded by a judge model disjoint from all in-budget verifiers, with a human audit (κ ≥ 0.7 target).

**Critic:**
1. SP1–SP5 are well-formed but miss the *scheduling* sub-problem this topic actually dies of: the grid × families × models cross-product exceeds the 5-week window unless pruning is itself treated as a design problem.
2. SP3's resolution ("open-weight primary") has a consequence not flagged: the headline dollar numbers then rest on the *amortized GPU price*, the most contestable row of the price sheet — SP1 and SP3 interact.
3. No sub-problem owns the frontier-estimation statistics (spline fitting, elbow location, permutation test) — Stage 5 uses them, but nothing names the risk that frontier "shape" descriptors are estimator artifacts.

**Refined:**
- **Add SP6 — Grid economics:** pruning the (L × N × V × budget × family × model) cross-product to a runnable subset without destroying identifiability of the interaction terms. Mechanism: pilot token statistics → expected-cost pre-screen → keep only matched-cost-bin members (~35 configs/family in pilot); interaction identifiability checked by simulated-power analysis on pilot data *before* Stage-2 scale-up.
- SP1×SP3 interaction handled by hierarchy of claims: Tier-1 claims (orderings, signs) must hold under *both* the GPU-amortized price and a counterfactual "API-equivalent list price" for the same open-weight model (e.g., a hosted-inference provider's published rate **[VERIFY current hosted rates at freeze time]**); Tier-2 numerics carry the price sheet as metadata.
- Frontier-statistics risk folded into SP2 (renamed "interaction and frontier estimation"): elbow/shape descriptors reported with bootstrap distributions; any shape claim that does not survive spline-smoothing perturbation (t3 mitigation) is demoted from the abstract.

---

## Stage 5 — Methods (concrete design)

**M3 — Task suite (verifiability-ordered, per digest):**
- **Code** (executable checks): HumanEval+ and a contamination-controlled LiveCodeBench slice; graded by test execution (pass@1-after-selection).
- **Math** (exact match): MATH-500 + AIME 2024/2025 hard tail.
- **Graduate MCQ** (option match): GPQA-Diamond.
- **Open QA** (rubric): FRAMES (SimpleQA subset as alternate); LLM rubric judge disjoint from in-budget verifiers; 200-item double-human audit.
- Pilot: math + code, ~300 questions each; Stage 2: all four, ≥500 where the benchmark allows.

**The 3-way allocation grid (M2):**
- L ∈ {512, 1024, 2048, 4096} thinking-token caps via budget forcing (truncate thinking, force answer).
- N ∈ {1, 2, 4, 8, 16} samples at T=0.8.
- V ∈ {0 = majority vote (zero verifier dollars), cheap judge (small LLM, 0–100 scoring, best-of-N), strong judge (larger model / PRM-style)} + a **zero-cost oracle-selection arm** per grid point (upper bound; separates coverage from selection quality).
- Budget levels: 3–4 per family; configurations pre-screened by expected cost (pilot token statistics) into matched-cost bins (target ±10%), realized cost recorded per query.

**Dollar-cost accounting model (M1):**
- Per-call ledger: (input tokens, output tokens) from engine usage fields → dollars via a **price sheet frozen at experiment start** (dated, published as an artifact). Verifier calls metered identically (candidates = input, judgment = output).
- Open-weight pricing: primary = GPU-hour-amortized rate (utilization-measured, formula published); secondary = a hosted-provider list price for the same weights **[VERIFY at freeze]**.
- Dual reporting: all results also in normalized output-token-equivalent units; **±3× sensitivity perturbation** of (input:output, verifier:generator) price ratios; Tier-1 claims must survive the band.

**Frontier estimation (M5):**
- Per (family, budget bin): non-dominated set over (mean realized cost, accuracy); accuracy surface fit `Âcc = f̂(L, N, V, c)` (monotone spline / GAM with explicit N×V, L×V terms); MRS via local finite differences at interior frontier points only; elbow via max-curvature with bootstrap distribution.
- Cross-family stability: Aitchison distance between allocation-mix compositions of efficient sets at matched bins; permutation test (10,000 perms), Holm α=0.05; 10,000-resample cluster bootstrap over questions for all bands.
- Interaction tests (RQ_INF_2): likelihood-ratio tests on N×V and L×V terms.

**Models:** pilot = one open-weight reasoning model with controllable thinking (7–14B class, e.g., a Qwen/DeepSeek-R1-distill reasoning model **[VERIFY best current open-weight choice at freeze; field moves fast]**); Stage 2 adds one large open-weight (~70B class) and one commercial API model for a coarse (N, V)-plane partial replication (SP3).

**Critic:**
1. The grid has 4×5×3 = 60 nominal cells before budget binning; with the oracle arm, 4 budget levels, 2 pilot families, 300 questions, N up to 16 — the pilot's true call count needs restating from the July estimate (~1.7×10⁸ tokens) against *today's* 5-week window and actual GPU availability, or the plan is inherited wishful thinking.
2. Majority vote is undefined for open-ended code/QA outputs without an equivalence relation; "majority" needs an operationalization per family (exact-match clustering for math/MCQ; test-outcome clustering for code; embedding/judge clustering for open QA — the last leaks judge cost into the "zero-cost" arm).
3. Temperature is fixed at 0.8, but the sampling lever's value is temperature-dependent; a reviewer will ask whether the sampling axis is really the "sampling-at-an-arbitrary-T" axis.
4. The API partial replication charges real dollars for a *supporting* result; under deadline pressure it is the natural thing to cut, but the paper's "dollar realism" framing leans on having at least one list-priced model.

**Refined:**
- Compute restated in Stage 6 with an explicit GPU reservation blocker; pilot grid trimmed to matched-cost members only (~35 configs/family, as in `paper.md`), which caps pilot at ≈ 2 families × 300 q × 35 configs × (avg 6 samples) ≈ 1.3×10⁵ generations ≈ 1–2×10⁸ tokens — 1 node × ~4–6 days with vLLM batching at 7–14B. Confirmed runnable in the window.
- Majority-vote operationalization pre-registered per family: math/MCQ = exact-answer equivalence; code = passing-set equivalence on public tests (no judge cost); open QA = **no majority arm** (honest gap: V=0 for open QA is "first sample," which is itself informative — selection has no free proxy where verification is hard; this asymmetry is part of the finding, not a bug).
- Temperature: fixed T=0.8 for the main grid (registered as a scope condition), one-cell T ∈ {0.6, 1.0} robustness probe at the pilot's best allocation to bound sensitivity; full T-axis explicitly out of scope.
- API arm protected with a hard $2K sub-budget and run *early* (week 3, not last) on the coarse (N, V) grid at one budget level; if the sweep (Stage 3 item 7) reveals imminent competition, the API arm is the first thing traded for speed.

---

## Stage 6 — Experiment design (arms, scale, compute, go/no-go, milestones)

**Arms:**
| Arm | Content | Role |
|---|---|---|
| A0 Calibration | token-statistics pass; grader audit (200 open-QA items, 2 annotators); price-sheet freeze | feeds cost pre-screen; validates graders |
| A1 Pilot grid | 1 model (7–14B) × {math, code} × ~35 matched-cost configs × 300 q | H1 first estimate; go/no-go |
| A2 Full grid | + GPQA-Diamond, FRAMES; ≥500 q; denser bins; 3–4 budgets | H1, H2, H3 headline |
| A3 Scale/model robustness | large open-weight (~70B) on a reduced grid | Tier-1 ordering robustness |
| A4 API partial replication | commercial API, coarse (N, V) plane, 1 budget level, ≤$2K | dollar realism (first to cut) |
| A5 Baseline policies | single-sample floor, long-CoT-only, self-consistency-only, best-of-N+verifier, Best-of-Majority, difficulty-conditioned (Snell-style) — all at matched budgets | situates frontier vs named prior policies |

**Scale & compute estimate:**
- A1: ~1–2×10⁸ tokens ⇒ **~100–150 A100-hours** (vLLM, 7–14B) ≈ 1 node, 4–6 days.
- A2: 4 families × 500 q × ~60 configs ≈ 1–1.5×10⁹ tokens ⇒ **~700–1,000 A100-hours** ≈ one 8-GPU node, ~1.5 weeks batched.
- A3: reduced grid at 70B ⇒ **~300–400 A100-hours** (4-GPU tensor parallel).
- A4: ≤ **$2K** API. Annotation: ~15–20 hours (open-QA audit). Total: ~1,100–1,550 A100-hours + ≤$2K — "one dedicated node for the month," which must be **reserved by Aug 15** (named blocker).

**Pilot go/no-go (by Aug 27, 2026):** GO iff (i) matched-cost bins are populated (≥ 25 configs/family within ±10%); (ii) the pilot frontier is non-degenerate (≥ 3 distinct allocation mixes on the efficient set — if one lever dominates everywhere at all budgets, H1/H3 die, but **that is itself publishable** as "the exchange-rate question has a corner solution" provided the oracle arm shows selection headroom existed); (iii) verifier arms beat majority vote somewhere on the grid at matched cost (else the verifier instrument is too weak — swap verifier once, re-run the V-slice, else demote verifying to a two-arm paper). NO-GO ⇒ fallback venue path (below) with the pilot as a workshop paper.

**Milestone plan (working back from Sep 18 / Sep 25):**
- **Aug 13–17:** GPU reservation + API budget sign-off (blockers); price-sheet freeze; A0 token-statistics + grader audit start; adjacent-work arXiv sweep (Stage 3 item 7); attempt verification of the two vendor-chart numbers **[VERIFY]** — outcome decides which motivation variant (full vs degraded) the intro uses.
- **Aug 18–27:** A1 pilot; simulated-power check for interaction terms (SP6); **Aug 27 go/no-go**.
- **Aug 28–Sep 10:** A2 full grid (+ A5 baselines inside the same runs); A4 API arm early in this window; A3 as capacity allows.
- **Sep 10–16:** frontier/MRS/stability analysis; sensitivity band; figures; draft on `discussion/paper_draft.tex` skeleton (already compiled once — real head start).
- **Sep 16–18:** abstract freeze; **Sep 18 abstract**. Sep 19–25: full paper; A3 results may land in this week (abstract wording must not depend on A3); **Sep 25 paper**.

**Timeline verdict: feasible — the tightest of the two topics but genuinely runnable**, because the primary instrument is local open-weight inference (no vendor calendar dependency, unlike B3.3's prospective arm) and the July WIP (grid spec, formal estimand, draft skeleton, refs) removes most cold-start cost. Slack is ~4 days. **Explicit risk ranking:** (1) compute contention — if the node reservation fails, A3 drops and A2 falls to 2 budget levels × 4 families (still supports H1/H2; H3 loses power — flagged in the paper); (2) scooping — mitigated only by speed and by the pre-declared pivot claims (Stage 3); (3) verifier weakness (go/no-go iii). **Infeasibility flag:** if A1 has not started by **Aug 22** (compute or staffing), ICLR 2027 is not reachable with credible error bars; **fallback venue: ICML 2027** (abstract ~late Jan 2027) with the larger A2+A3 design as the base, and the pilot released as an arXiv preprint **immediately** anyway to establish priority against the crowd; secondary fallback: NeurIPS 2027, or the harness + cost-ledger as a D&B submission.

**Critic:**
1. The plan runs A5 baselines "inside the same runs" — true for allocation baselines that are grid points, but Snell-style difficulty-conditioned allocation needs a fitted difficulty predictor (validation split, extra passes); it is not a free grid point and could silently slip.
2. Publishing the pilot preprint "immediately" on NO-GO conflicts with ICLR anonymity if the team later submits substantially the same work — the priority-vs-anonymity tradeoff is real and undiscussed.
3. Go/no-go (ii) treats a corner solution as publishable, but the abstract deadline (Sep 18) precedes A2 completion (Sep 10) by days — the abstract must be written to survive either a rich frontier or a corner solution, and no wording strategy is given.
4. The two [VERIFY] vendor numbers appear in the milestone plan as a verification *task* but there is no stated rule for what happens on partial verification (e.g., the chart exists but numbers differ).

**Refined:**
- A5's difficulty-conditioned baseline is descoped to a *pilot-fitted, frozen* difficulty binning (Snell-style in spirit, fitted once on pilot data, no tuning in A2) and marked "approximate re-implementation"; if it threatens the critical path it is cut and the omission acknowledged — the frontier claims do not depend on it.
- Preprint policy: ICLR permits arXiv preprints (non-anonymity-violating under current policy **[VERIFY ICLR 2027 dual-submission/preprint policy when the CFP is out]**); the pilot preprint is posted under the *project* name on NO-GO only, and on GO the team posts nothing until after the abstract deadline to keep messaging aligned with the submission.
- Abstract wording strategy (pre-drafted both ways): frame the contribution as "the first dollar-denominated measurement of three-lever substitution, with the verifier priced inside the budget — we characterize when exchange rates are non-constant *and when they are not*"; both the rich-frontier and corner-solution outcomes instantiate this sentence truthfully. Numbers enter only the Sep 25 full paper.
- Partial-verification rule for vendor numbers: cite only what the public artifact itself shows, with the artifact as the citation; any residue of the relayed figures that the artifact does not confirm is discarded permanently (no "personal communication" citations).

---

*End of B4.2 discussion. Design ids (C1–C5, M1–M5, CO1–CO4, RQ1/RQ_INF_1/RQ_INF_2, t1–t5) interoperate with `digest.md` and `paper.md`; this document consolidates and re-schedules the July `discussion/` material (incl. the compiled `paper_draft.pdf` and the WIP zip at `topics/B4.2_...zip`) against the Sep 18/25, 2026 ICLR 2027 deadlines and the Aug-2026 competitive context.*
