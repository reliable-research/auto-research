# B4.2 Autodiscussion Draft Review — "Dollar-Matched Substitution Rates for Joint Reasoning, Sampling, and Costed Verification"

Reviewer: Claude (review + revision pass), 2026-08-14.
Package: `paper_autodiscussion/completed_jobs_dirs/ZB4.2 ...--8f5db066/` (research-report.md, experiment-spec.md, paper-draft.md).
Reference design: `topics/B4.2_.../discussion.md` (KEEP-TOP, ICLR 2027, abstract Sep 18 / paper Sep 25, 2026).

---

## 1. Architecture of the draft (~10 lines)

The draft is a **pre-registered measurement-framework paper** (all future tense, no results) with four method modules:
(1) **Unified Dollar Cost Accounting** — package-exclusive metering in reserved serving contexts; role- and resource-tagged quantity vectors; device-second primary pricing with token-tariff replacement basis; footprint ladders, serialization replay, rounding-slack audits.
(2) **Shared-Cost Substitution/Interaction Estimation** — blocked adaptive randomization; family-specific matched-cost bins (±10%, cross-fitted); four-cell "exchange rectangles"; semiparametric response surfaces; gain-per-dollar ratio `r(δ;p)` and stabilized cross-product `s(δ;p)` with precision gates.
(3) **Audit-Anchored Long-Form Factuality** — expert content census, two-phase probability sampling, directional-error correction, calibrated pseudo-outcomes for a **LongFact** family.
(4) **Price-Robust Repricing** — fixed-quantity repricing over a ±3× price-ratio region, branch-and-bound search for interior flips, full-range invariance vs feasible-set retention (≥0.8).
Evaluation: 16 RQs over HumanEval/MBPP, MATH/GSM8K, GPQA, LongFact + metering, semi-synthetic, expert-reference, and seeded-repricing suites; 8 comparator classes. The formal estimand (MRS, interactions, Tier-1 orderings/signs vs Tier-2 dated numerics) faithfully implements discussion.md Stage 1.

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|---|---|---|---|
| N1 | First **joint 3-way (L×N×V) exchange-rate/substitution measurement under one dollar budget with verifier cost charged in-budget** | Snell et al. 2408.03314 (proposer/verifier, FLOPs-matched); Singhi et al. 2504.01005 (solve-vs-verify, 2 levers, token-equivalent); **2026 neighbors the draft misses:** arXiv:2606.19808 *Think Again or Think Longer? Selective Verification for Budget-Aware Reasoning* (thinking-vs-verification budget, 2 levers); arXiv:2607.08665 *Resample or Reroute?* (budgeted marginal-correctness-per-unit-cost decision); arXiv:2510.06135 asymmetric verification cost-accuracy in deep search; arXiv:2606.19354 verification-granularity/compute efficiency; arXiv:2512.02008 TTS survey (hybrid seq/parallel) | Every **pair** (L-N, N-V, and now L-V via 2606.19808) has a 2024–2026 two-lever study, but none estimates the **three-way** substitution surface, none charges verifier tokens inside the same dollar meter, and none tests price-ratio robustness. Delta = joint interactions (N×V, L×V signs) + dollar denomination + cross-family stability. | **HOLDS, but narrowed.** Verified via 5 searches (2026-08-14). The claim must be rewritten from "these levers have not been varied jointly" to the precise "no three-way, verifier-priced, dollar-denominated joint estimate"; the 2606.19808 L-vs-V neighbor makes the current wording falsifiable. |
| N2 | **Fixed-quantity repricing / price-perturbation invariance** (orderings & signs must survive ±3× price-ratio region) | Erol et al. 2504.13359 Cost-of-Pass (dollar frontier over whole pipelines, single price sheet); arXiv:2511.23455 *Price of Progress* (inference price-performance trends); arXiv:2607.26828 cost-calibrated frontier utility. Nothing found that repricing-perturbs a frozen resource ledger to test conclusion survival. | Prior dollar work uses one dated price sheet; the survival-under-repricing methodology (full-range invariance vs ≥0.8 retention) appears novel as an evaluation device. | **HOLDS** (2-3 searches). Genuinely the draft's most defensible methodological contribution; keep, but simplify the certification machinery (see §5). |
| N3 | Audit-anchored long-form factuality estimator (census + directional-error correction) | SAFE/LongFact line; survey-sampling measurement-error literature | Real but belongs to a different paper; not in discussion.md scope | **OUT OF SCOPE** — scope inflation (see §3). |
| N4 | Package-exclusive device-second metering with footprint ladders/serialization replay | Cloud-metering practice; no direct academic twin | Novel-ish engineering, but not the topic's edge and it *weakens* dollar realism (reviewers price tokens, not reserved device-seconds) | **DEMOTE** to an appendix-level accounting variant. |

**Vendor-race check (explicit portfolio requirement):** the draft's Introduction contains **no vendor positioning at all** — no mention that vendors already publish single-lever cost curves. Public artifacts now exist: OpenAI's GPT-5.6 launch page and coverage show score-vs-cost/latency curves for reasoning-effort tiers and an "ultra" multi-agent mode (4 agents default, up to 16) — i.e., exactly the two single-lever slices discussion.md Stage 2 flagged. The specific relayed numbers (53.6%→52.7% @ +42%; +3.1pp/+1.11pp @ ~6×) remain **unverified** → per discussion.md the *degraded fallback* paragraph must be used, citing only what public charts qualitatively show. The draft fails the race-positioning requirement as written.

## 3. Consistency vs discussion.md — silent scope changes (all silent, none flagged)

1. **Task suite swapped.** discussion.md M3: HumanEval+ + LiveCodeBench (contamination-controlled), MATH-500 + AIME 24/25, GPQA-**Diamond**, **FRAMES** open QA (rubric judge + 200-item human audit). Draft: HumanEval + **MBPP**, MATH + **GSM8K** (saturated, weakens the hard-tail budget story), GPQA **main set**, and **LongFact long-form factuality** — an entirely new family dragging in method module (3), an expert-panel apparatus, and 7 of 16 RQs. This is the largest silent inflation.
2. **Sampling grid inflated:** N ∈ {1,…,16} every integer (draft) vs N ∈ {1,2,4,8,16} (discussion.md); with matched-cost pre-screening the doubling grid was the point of SP6 grid economics.
3. **Accounting unit swapped:** discussion.md M1 = per-call token ledger × frozen price sheet + GPU-hour-amortized rate + hosted list price. Draft = reserved device-seconds in package-exclusive serving with footprint ladders, serialization replay, rounding audits — different estimand, far heavier, and it silently drops the "hosted list price secondary" realism anchor to a footnote role.
4. **Staged plan deleted:** A0–A5 arms, pilot go/no-go (Aug 27 gates i–iii), milestone plan, compute budget (~1,100–1,550 A100-h + ≤$2K API), fallback-venue logic — all absent. The API partial-replication arm (A4) is reduced to "1,000 hosted-endpoint calls" for ledger reconciliation only.
5. **Motivation dropped:** vendor single-lever charts (even degraded version), overthinking/cost-aware-eval line (2604.10739, 2507.14417, 2502.08235), concrete workload anchors — none present; intro instead cites KV-cache/vLLM-fleet ops papers, which motivate serving efficiency, not lever allocation.
6. **Preserved faithfully (credit):** selection-only verifier scope sentence; oracle arm exempt from cost comparisons; ±10% bins on realized cost; Tier-1/Tier-2 claim hierarchy; ±3× price region; open-QA "no free majority" asymmetry is implicitly handled (majority undefined for long-form) but the *finding-not-bug* framing is lost.

## 4. Citation audit (load-bearing set)

| Citation | Claimed as | Status |
|---|---|---|
| Snell et al., arXiv:2408.03314 | compute-optimal TTS, proposer/verifier under FLOPs | **CONFIRMED** |
| Wu et al., arXiv:2408.00724 | inference scaling laws, model size vs strategy at fixed FLOPs | **CONFIRMED** |
| Liu et al., arXiv:2502.06703 | 1B-vs-405B compute-optimal TTS; policy/PRM/difficulty | **CONFIRMED** |
| Kexun Zhang et al., arXiv:2410.22480 | learned sample-compute allocation (OSCA) | **CONFIRMED** |
| Wang et al., arXiv:2203.11171 | self-consistency | **CONFIRMED** |
| Brown et al., arXiv:2407.21787 | Large Language Monkeys, coverage scaling | **CONFIRMED** |
| Lightman et al., arXiv:2305.20050 | process vs outcome supervision, best-of-N | **CONFIRMED** |
| Lunjun Zhang et al., arXiv:2408.15240 | Generative Verifiers | **CONFIRMED** |
| Setlur et al., arXiv:2502.12118 | verifier-based scaling advantages | **CONFIRMED** |
| Singhi et al., arXiv:2504.01005 | When To Solve, When To Verify | **CONFIRMED** |
| Muennighoff et al., arXiv:2501.19393 | s1, budget forcing | **CONFIRMED** |
| Aggarwal & Welleck, arXiv:2503.04697 | L1 length-controlled reasoning | **CONFIRMED** |
| Erol et al., arXiv:2504.13359 | Cost-of-Pass economic framework | **CONFIRMED** |
| Xingyu Chen et al., arXiv:2412.21187; Han et al., 2412.18547; Chen et al., 2403.02419; Zhao et al., 2502.01839 | overthinking / token budget / more-calls / sample-scrutinize | **CONFIRMED** (roles match) |
| Hao Chen et al., arXiv:2505.11730 | verification-frequency during search | **PLAUSIBLE-UNVERIFIED** — could not confirm title/authors in searches; verify before submission or drop. |
| arXiv:2604.08075 (vLLM fleet), 2605.18869 (MO-CAPO), 2412.19442 (KV-cache survey) | intro ops motivation | **CONFIRMED-BUT-MISALIGNED** — real papers (per research-report evidence quotes) used to motivate the wrong thing (serving capacity, not lever allocation); replace with the vendor-chart + overthinking motivation. |

Verdict consistent with sibling review: **zero confabulated citations found**; the problem is *missing* 2026 neighbors (2606.19808, 2607.08665, 2510.06135, 2606.19354, 2602.01070, 2512.02008), not fake ones. The related-work section also ends with a leftover scaffold line "> This section requires manual completion with proper citations." which must not ship.

## 5. Gap to implementation (ICLR clock: abstract Sep 18, paper Sep 25 — ~5 weeks)

The draft as specified is **not executable in the window**. Rough floor of its own numbers: RQ1 200 held-out packages × strata + 1,000 hosted calls; RQ2 **20,000** cap-constrained requests; RQ3 3,600 cost-only executions **per family**; RQ4 50 concurrent replays × 4 cells × ≥30 rectangles/family; RQ6/7 tens of thousands of simulation replications (cheap but engineering-heavy); RQ10–13 expert panels labeling **thousands** of claims with disjoint reference panels (recruiting alone exceeds the window); RQ14–16 branch-and-bound certification over a continuous price region with recomputed support at every price point. Discussion.md's costed plan (A1 ≈ 100–150 A100-h; A2 ≈ 700–1,000; A3 ≈ 300–400; ≤$2K API; node reserved by Aug 15; A1 must start by Aug 22) covers **only** the substitution grid — none of the metering/certification/factuality superstructure. The draft also contains zero scheduling logic: no pilot, no go/no-go, no descope order. Conclusion: publishable-in-window only after cutting modules (1)-heavy metering to a token ledger, module (3) entirely, and RQs 1–5/10–13/15–16 to appendix-level checks.

## 6. Verdict + top-3 fixes + inferred unresolved MAJORs

**Verdict: MAJOR REVISION.** The formal estimand, tiered claim hierarchy, matched-cost design, and repricing-survival idea are genuinely strong and should survive. But the draft has drifted from "the exchange-rate paper" into "the metering-and-measurement-theory paper": it is un-runnable before the deadline, silent about every scope change, blind to the vendor race it exists to win, and missing the 2026 two-lever neighbors that define its true delta.

**Inferred 3 unresolved MAJORs (consistent with room-closure state):**
- **MAJOR-1 (feasibility/scope):** the package-exclusive metering + expert-audited LongFact + 16-RQ certification program cannot be executed before Sep 25; no pilot/gate/descope structure survives from discussion.md.
- **MAJOR-2 (positioning/novelty):** no vendor-race framing and no 2025–2026 neighbors (esp. thinking-vs-verification and budget-aware-decision papers), so the stated novelty claim ("not varied jointly") is over-broad and vulnerable; the anti-incremental argument (interaction terms are joint quantities) is absent.
- **MAJOR-3 (silent scope divergence):** benchmark suite, N-grid, accounting unit, and family list all silently diverge from the pre-registered discussion.md design; a preregistration-style paper that silently edits its own preregistration is self-undermining.

**Top-3 fixes (applied in `paper-draft.revised.md`):**
1. **Re-scope to the discussion.md design:** restore HumanEval+/LiveCodeBench, MATH-500/AIME, GPQA-Diamond, FRAMES (rubric judge + 200-item audit, no expert-census apparatus); N ∈ {1,2,4,8,16}; token-ledger dollar accounting (GPU-amortized primary + hosted list-price secondary); restore arms A0–A5, pilot go/no-go, milestones, compute budget; demote device-second metering and heavy factuality machinery to future work / appendix.
2. **Reposition for the race:** degraded-fallback vendor paragraph (public single-lever cost curves: reasoning-effort tiers, multi-agent scaling) + anti-incremental paragraph + 2026 neighbors added to related work with explicit two-lever-vs-three-lever boundary statements.
3. **Keep and foreground the two real methodological novelties** — in-budget verifier pricing within matched-cost bins, and fixed-quantity repricing survival (full-range invariance vs ≥0.8 retention) — collapsing 16 RQs to 5 RQs mapped to H1–H3 + ledger validity + price robustness; add Figure 1 (architecture.svg).
