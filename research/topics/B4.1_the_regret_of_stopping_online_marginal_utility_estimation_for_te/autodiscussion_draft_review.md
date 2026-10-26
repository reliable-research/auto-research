# B4.1 Autodiscussion Draft Review — The Regret of Stopping

**Reviewed:** 2026-08-15. Package `ZB4.1 ... --67b8c4da` (research-report.md, experiment-spec.md, paper-draft.md) vs `discussion.md` / `README.md`.
**Verification channel:** WebSearch not used (quota risk); all citation checks done via WebFetch of the arXiv API (`export.arxiv.org/api/query`) — a narrower sweep than a full web search; one targeted twin-search (`stopping+regret+reasoning+oracle`) returned zero hits.

---

## 1. Architecture of the draft (~10 lines)

The draft (retitled "Uncertainty-Calibrated Hindsight Oracles for Replayable Per-Instance Regret Analysis of Reasoning Stopping Rules") is a **pure measurement-framework paper** with three modules:

1. **Uncertainty-validated hindsight oracle** — checkpoint evidence bundles from matched stop-and-answer probes; paired block bootstrap preserving cross-checkpoint dependence; simultaneous max-t (sup-t) utility bands; split-conformal calibration against disjoint high-budget audit probes, yielding a confidence *set* over the utility-maximizing checkpoint t*(λ) rather than a plug-in argmax.
2. **Attributed per-instance regret** — for each rule's causal stop τ, regret is computed inside every calibrated oracle draw b as U_b(t*_b) − U_b(τ), with early/late/tie components assigned per draw so the decomposition is additive by construction and direction becomes a soft probability.
3. **Replayable rule-scoring corpus** — content-addressed records split into a causal namespace (policy-visible) and a sealed namespace (verifier evidence, oracle draws), a sandboxed sequential API with one irrevocable STOP, SHA-256 manifests, schema taint checks, randomized hindsight canaries.

The experiment section evaluates only the instrument itself (six RQs: band coverage, oracle-set inclusion, decomposition exhaustiveness, direction calibration, bit-exact replay, canary leakage) on **synthetic/stress corpora**, and states explicitly: *"It will not compare candidate rules for effectiveness."*

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|---------------|-------|--------|
| C1 | Uncertainty-validated hindsight oracle: simultaneous bands + conformal confidence sets over t*(λ), correcting max-of-noisy-means selection bias | ThinkBrake (2510.00546) uses a plug-in oracle-stopping headroom number (+8% acc, −72% tokens) with no uncertainty; Dong et al. (2606.30852) calibrate risk but never construct an oracle reference; discussion.md itself only had the cruder N=32 re-probe bias bound | Real and genuinely stronger than the design doc — the oracle-as-uncertain-object treatment answers Stage-1 critic hole (1) properly | **Keep** (a strength to preserve) |
| C2 | Per-instance oracle-relative regret with additive early/late/tie decomposition across a cost-weight grid | **arXiv:2604.10739** (Zhou et al., Apr 2026, "When More Thinking Hurts") — verified today: cost-aware evaluation of diminishing/negative marginal utility, difficulty-dependent optimal length, but **aggregate only, no per-instance oracle regret, no decomposition** | Delta survives — the single largest external risk flagged in discussion.md Stage 3 resolves **positively**. But the draft never cites 2604.10739 at all, so the delta is never established on paper | **Keep + must cite and carve explicitly** |
| C3 | Content-addressed sealed replay corpus with causal API, taint checks, canaries | No stopping-rule paper ships one; generic ML eval-infra ideas (frozen logs, leakage canaries) exist elsewhere | Modest; right-sized as the [资源] deliverable, not a headline | **Keep, demoted below the empirical findings** |
| C4 | (Implicit) "The framework audits its own correctness; it does not compare rules" | — | This is not a delta, it is an abdication of the topic's estimand (README seed: 各停止策略相对 oracle 的遗憾是多少 — *what regret does each rule incur*) | **Reject / invert** |
| C5 | Distinctness within the wave: not another adaptive-stopping method (DEER/ThinkBrake/Certaindex/JET territory), not B4.2's exchange-rate estimand, not B4.5's verifier-allocation axis | B4.2 consumes λ machinery; B4.5 meters verification | The draft is on the correct side of these lines but never states the boundaries | **Add explicit boundary sentences** |

## 3. Consistency vs discussion.md — silent scope changes

The sibling failure signature (**zero confabulated citations, silent scope inflation, missed 2026 neighbors**) is reproduced almost exactly:

- **S1 (scope inversion, the big one).** discussion.md commits to an *empirical pilot*: 1 model (DeepSeek-R1-Distill-Qwen-7B) × 3 benchmarks (GSM8K, MATH-500, GPQA-Diamond) × ~500 instances, K≈20 checkpoints × N=8 probes, calibrated rule zoo, regret curves, difficulty deciles, learned-estimator condition, ~1 node-week. The draft deletes all of it: datasets become synthetic stress corpora; the rule zoo becomes six toy reference rules (first/last/fixed/threshold/patience/budget) used only for reproducibility tests; the seed's core question is unanswered *by design*.
- **S2 (λ grid).** Log-spaced 7-point grid in interpretable units (~0.01–3 accuracy-points/1K tokens) → arbitrary {0, 0.05, …, 1.00} in "normalized-utility units", including λ=0 where the late/tie structure degenerates (continuation is free, so stop-late regret at the max-accuracy checkpoint is 0 by construction).
- **S3 (compute inflation).** Oracle audits "until … 50,000 rollouts have been reached" per instance × 600 instances is up to 3×10^7 rollouts — ~2 orders of magnitude beyond discussion.md's entire ~2.4×10^5-probe pilot budget. All week-1/2/3 go/no-go gates, the dry run, the Aug-24 fallback trigger, and the power-based gate vanish.
- **S4 (instrument-validity protocol).** The N=32 re-probe bias bound, the true-termination mid-trajectory validity subsample (SP1's two-pronged protocol), the branch-isolation invariant, and the probes-charged/probes-excluded dual cost accounting are all dropped or replaced by ungrounded "high-budget audit probes".
- **S5 (SP4 dropped).** The online marginal-utility estimator (the constructive half of the seed question, 边际收益能否被在线估计) and per-checkpoint signal-AUROC analysis are gone.
- **S6 (required related-work moves dropped).** No "relation to optimal stopping theory" paragraph (hindsight/competitive-analysis regret vs no-regret learning — a definitional fight the discussion explicitly predicted); no calibration literature; no B4.2/B4.5 boundary statements.
- **S7 (missed motivation spine + critical adjacent).** 2505.17813 (Hassid — shorter chains win), 2502.08235 (Cuadron — agentic overthinking), 2503.16419 (survey), and above all **2604.10739** are absent, although discussion.md names each as mandatory-to-engage.
- **Faithful parts (credit where due):** per-logged-trajectory paired replay, oracle-not-ground-truth constraint, early/late decomposition, replayable-corpus deliverable, and threshold-calibration-as-policy-class are all implemented, several more rigorously than specified.

## 4. Citation audit (all load-bearing citations, arXiv-API-verified 2026-08-15)

| Citation in draft | Verified id | Status |
|---|---|---|
| Muennighof et al., s1 | 2501.19393 | ✓ real; **author misspelled — "Muennighoff"** |
| Aggarwal & Welleck, L1 | 2503.04697 | ✓ |
| Snell et al., test-time compute | 2408.03314 | ✓ |
| Guo et al., DeepSeek-R1 | 2501.12948 | ✓ (well-known) |
| Yang et al., Dynamic Early Exit (DEER) | 2504.15895 | ✓ |
| Song et al., ThinkBrake | 2510.00546 | ✓ |
| Fu et al., Certaindex | 2412.20993 | ✓ |
| Fu et al., Deep Think with Confidence | 2508.15260 | ✓ |
| Li et al., ESC | 2401.10480 | ✓ |
| Aggarwal et al., Adaptive-Consistency | 2305.11860 | ✓ |
| Wan et al., RASC | 2408.17017 | ✓ |
| CGES "(unknown authors)" | 2511.02603 | ✓ real; **first author is Ehsan Aghazadeh — placeholder must be fixed** |
| Dong et al., When Does Learning to Stop Help? | 2606.30852 | ✓ real (June 2026) — the draft's closest 2026 neighbor, correctly engaged |
| Chen et al., overthinking 2+3 | 2412.21187 | ✓ |
| Wang et al., underthinking | 2501.18585 | ✓ |
| Lightman et al., Let's Verify | 2305.20050 | ✓ |

**Zero confabulated citations.** Two mechanical fixes (misspelling, unknown-author placeholder), one leftover scaffold line ("This section requires manual completion with proper citations"), and one critical **omission**: 2604.10739, plus the 2505.17813 / 2502.08235 / 2503.16419 motivation spine.

## 5. Gap to implementation

- experiment-spec.md opens with leftover assistant preamble ("I'll analyze this research plan…") — a generation artifact that must not ship.
- The spec is a competent blueprint for the *instrument's unit tests* (stats core, corpus format, canary classifiers) but contains **no model, no benchmark, no verifier implementation, no decoding/probe harness, no KV-branching plan, no cost model beyond a config placeholder** — everything needed to answer the research question is deferred to "Inputs You Must Provide."
- The 50k-rollouts-per-instance audit criterion is infeasible at pilot budget; nothing replaces discussion.md's dry-run gates or the power-based week-2 gate.
- Net: as specified, a coding agent would deliver a well-tested library that has never touched an LLM trajectory. The distance from spec to a submittable empirical paper is essentially the entire Stage-5/6 plan of discussion.md.

## 6. Verdict and top-3 fixes

**Verdict: MAJOR REVISION (accept the machinery, reject the framing).** The statistical treatment of the oracle is genuinely better than the design doc's, but the draft silently pivoted from "measure the regret of stopping rules" to "validate a measurement instrument on synthetic data," inverting the topic's estimand, deleting the empirical pilot, and missing the mandatory 2026 neighbors.

**Inferred unresolved major (room closed with 1):** the scope question itself — whether the paper may ship as instrument-validation-only or must contain the empirical rule-regret study. The thrice-repeated disclaimer "will not compare candidate rules for effectiveness" against a title promising "Regret Analysis of Reasoning Stopping Rules" reads as the residue of that unresolved argument, closed in favor of the framework-purist side. This revision overturns it.

1. **Restore the empirical study as the headline.** 1 model × 3 benchmarks pilot; calibrated rule zoo (fixed-budget, DEER-style confidence, entropy ×2 pre-registered variants, vote-share, TrimR-style stability, learned estimator ×2 architectures); regret curves over λ with early/late decomposition by difficulty decile; headroom ("X% of achievable utility unclaimed") as the headline number. Demote RQ1–RQ6 to an instrument-validation section with realistic audit budgets (N=32 re-probe on a subsample, not 50k rollouts).
2. **Restore the economics and gates of discussion.md.** Interpretable log-spaced λ grid (accuracy-points/1K tokens, no λ=0 headline), dual probe-cost accounting, two-pronged intervention-validity protocol (terminal agreement + true-termination subsample), branch-isolation invariant, week-1/2 go/no-go gates and the pivot framing for a near-zero-regret outcome.
3. **Rebuild related work.** Cite and carve against 2604.10739 (verified: aggregate cost-aware, no per-instance oracle — delta stated positively); add 2505.17813 / 2502.08235 / 2503.16419 as the motivation spine; keep Dong et al. 2606.30852 as closest neighbor; add the optimal-stopping-theory positioning paragraph (hindsight/prophet-style regret, not no-regret learning) and one-sentence boundaries vs B4.2 (exchange rates consume λ machinery) and B4.5 (meters verification, we meter thinking). Fix Muennighoff and the CGES author placeholder; delete scaffold lines.
