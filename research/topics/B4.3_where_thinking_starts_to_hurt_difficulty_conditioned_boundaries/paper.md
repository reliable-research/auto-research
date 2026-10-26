# Where Thinking Starts to Hurt: Difficulty-Conditioned Boundaries of Test-Time Compute — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1–C4, M1–M5, RQ1/RQ_INF_1/RQ_INF_2, CO1–CO3, t1–t5) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** *Marginal test-time reasoning compute has a difficulty-indexed sign: the same additional thinking token that buys correctness on a hard problem buys error on an easy one, because continued reasoning can overwrite an already-correct answer state — so the return curve does not flatten, it flips.*

**判据 (deletion test).** Delete the domain nouns (thinking token, correctness/answer state, problem difficulty): *"Marginal X has a Y-indexed sign: the same additional unit of X that buys gain on a high-Y instance buys loss on a low-Y one, because continued X can overwrite an already-achieved outcome."* This generic statement is **false**: for a generic resource, marginal returns diminish toward zero but do not turn negative — spending more money, more samples, or more training data on an "easy" instance wastes the surplus, it does not destroy the result already obtained. The sentence is only true where the resource is *the same generative process that produced the answer*, so that spending more of it can revise a correct output into a wrong one (digest N3: [WhenMoreIsLess], [Chen et al., 2024], [FirstImpression]). The domain nouns are load-bearing; the sentence is not a bridge.

## Step 2 — Archetype

**Primary: `empirical` (boundary-mapping measurement study)** — per digest N12: unmodified off-the-shelf reasoning models, a purpose-built measurement harness, a characterization finding as the headline (cf. "LLMs Get Lost in Multi-Turn Conversation", "Are Emergent Abilities a Mirage?"). **Secondary:** small analysis instrument (the cheap-signal tipping-point predictor, CO2) in service of the empirical claim — not a tool release.

Downstream consequences:
- **(a) Abstract contribution slot:** a *map* (per-stratum accuracy-vs-length curves with statistically localized sign-flip points, or explicit right-censoring — CO1), not a method that beats a number. CO2/CO3 appear as instruments quantifying the map's usability.
- **(b) Intro logic:** "what becomes possible" — the entire adaptive-reasoning literature (stopping rules, difficulty probes, length-penalty training; digest N4) *presupposes* a difficulty-conditioned boundary it never measures; publishing the boundary map makes budget-allocation decisions auditable against a measured landscape instead of an assumed one.
- **(c) Evidence standard for results:** statistically localized change points with bootstrap CIs, multiple-comparison correction, and agreement across independent length manipulations — NOT leaderboard deltas. A well-powered null (no flip anywhere in the studied regime) is itself a publishable boundary datum (see F-G1).

## Step 3 — Taste Self-Audit

| Check | Verdict | Note |
|---|---|---|
| Is the opportunity a Bridge ("A and B never connected")? | **PASS** | The opportunity is an unmeasured invariant (sign flip of marginal return) that existing work exploits without measuring (N4 limitations 2–4), not a connection between two fields. |
| Is the method mere Synthesis (glue existing parts)? | **PASS** | M2 (three-arm length-control harness) + M3 (paired-bootstrap slope-sign change-point estimator) constitute a measurement instrument built for this question; M4's prefill probe is deliberately included as a *baseline*, not as the method. |
| Load-bearing verbs from integrate/unify/leverage family? | **PASS** | Load-bearing verbs: *measure, stratify, localize, isolate (the sign flip from truncation artifacts), predict, censor*. |
| Abstract opening rule ("X is increasingly used… however… we introduce") | **ENFORCED** | Abstract v0 below opens with the mechanism/asymmetry; forbidden template avoided. |

No check failed; no framing repair needed.

## Step 4 — Method-Twins (concede-and-differentiate)

*Added at Phase A re-run (2026-07-04), per guidance.md Part 4 situation 6 and Part 5: a freshness-sweep-style harvest (`discussion/reference_candidates.jsonl` Task-1 upgrade) surfaced two close steering/intervention method-twins not previously in the cache. Per situation 6, this is a repositioning at source, not a silent Related-Work citation add.*

- **`ThinkingSpeedESEL` (representation steering of fast/slow reasoning) and `2512.24574` / CREST (attention-head steering that cuts tokens and raises accuracy)** both **concede**: an unmodified model's reasoning trajectory *can* be steered at test time without retraining, and both presuppose the same difficulty-dependent boundary this paper measures — CREST explicitly motivates itself with "overthinking, underthinking" (its own N2), the same asymmetry as this paper's Step 0.
- **What remains B4.3's own contribution**: neither CREST nor ThinkingSpeed *measures* the boundary in an unmodified model — both *intervene* on it (steer activations) and report the resulting accuracy/token deltas, which is exactly the intervention-vs-emergence confound already named in digest C4/N4 limitation 4. B4.3's three-arm design (truncation / forced continuation / natural stopping, none of which edits internal activations) reports the boundary's location and shape *before* any steering is applied, which is the input CREST/ThinkingSpeed's own steering decisions would need but do not measure. CO1 (the boundary map) is therefore upstream of, and unmeasured by, both method-twins; CO2/CO3 (the cheap pre-hoc predictor and its oracle-gap recovery) have no analog in either paper, which validate steering directions post hoc rather than predicting a tipping point pre hoc.
- **Action for Phase E**: Related Work must name both method-twins in the same nearest-neighbor paragraph as `[WhenMoreIsLess]`/`[Chen et al., 2024]` (per the existing `stage_review.md` Stage-2 fix), not as a separate late paragraph — three concede-and-differentiate threads (theory-only validation, aggregate-only documentation, intervention-without-measurement) rather than two.

## Step 5 — Formal Problem Definition

**Estimand.** The difficulty-conditioned tipping-point length L\*_s — the smallest thinking-token budget at which further reasoning yields a significantly negative marginal accuracy return — and its predictability from cheap pre-hoc signals; unit of analysis is one (item, rollout) pair aggregated to a (stratum, length-control-arm) cell; reference population is natural math/science benchmarks plus a synthetic tunable-difficulty family, evaluated on off-the-shelf reasoning LLMs at 1.5B–32B scale; the decision it feeds is whether test-time compute budgets should be allocated uniformly or conditioned on difficulty (R1, guidance.md Part 3.4).

**Notation.** Model f with controllable thinking budget; item x with gold label y; rollout at truncation length L ∈ 𝓛 = {256, 512, 1k, 2k, 4k, 8k, 16k}; correctness Z(x, L, r) ∈ {0,1} for rollout r; strata s ∈ {1..5} (difficulty quintiles).

| Load-bearing adjective/verb (from digest Claims) | Formal definition | Measured by |
|---|---|---|
| "difficulty" (of x) | d(x) = 1 − pass-rate over 8 rollouts truncated at 512 thinking tokens (M1); quintile binning gives s(x) | generation logs; cross-checked vs MATH native levels + second-model solve rate (Spearman ρ reported) |
| "accuracy at length L" | A_s(L) = mean over items in s, rollouts r of Z(x, L, r) | exact-match auto-grading |
| "marginal benefit turns negative" | Δ_s(L_k) = A_s(L_{k+1}) − A_s(L_k) < 0, significant by one-sided paired item-level bootstrap (10k resamples), Holm-corrected (M3) | bootstrap on paired per-item differences |
| "tipping point" | L\*_s = min{L_k ∈ 𝓛 : Δ_s(L_k) significantly negative}; **right-censored** if no such L_k ≤ 16k | M3 + bootstrap CI over L\*_s |
| "non-monotonic region" | ∃ L_peak < L_max with A_s(L_peak) − A_s(L_max) > 0, significant as above | same test on peak-vs-max contrast |
| "cheap" (signal) | computable from ≤256 thinking tokens + k=4 truncated-answer probes (≤512 tokens each) ⇒ ≤ (256 + 4·512)/16384 ≈ 14% of max budget; **no ground-truth labels** at inference | token accounting in harness logs |
| "predictable" (tipping point) | Spearman ρ(L̂\*, L\*) on held-out strata/domains; localization error e = \|log₂ L̂\* − log₂ L\*\| | M4 predictor evaluation |
| "substantial fraction of oracle tradeoff" | oracle-gap recovery G = (A(pred-stop) − A(best fixed)) / (A(oracle-stop) − A(best fixed)) at matched mean token cost | M5 protocol |
| "difficulty-conditioned" (boundary) | L\*_s non-constant in s: Jonckheere–Terpstra trend on L\*_s (censored strata handled as max-rank ties) | M3 outputs across strata |
| "informative" (feature) | AUROC of feature for classifying sign(marginal gain beyond probe point), CI excluding 0.5 | per-feature AUROC, held-out strata |

Deleted adjectives: "meaningful", "efficient" (subsumed by G and by token-savings-at-matched-accuracy, digest N8 metrics).

## Assumptions

*Every A\* below carries a `consequence` clause (added at Phase A re-run, 2026-07-04, per guidance.md §3.2's seven-slot template) stating what happens to which H\* if the assumption fails — degrade, restrict scope, or block — so failure isn't just detected but has a pre-committed downstream action.*

- **A1 — Length control is valid.** Truncation + end-of-thinking delimiter + forced "Final Answer:" yields parseable answers. *Failure mode:* format collapse at small L. *Detection:* walking-skeleton gate — parse rate ≥95% in every cell; below that, curves confound accuracy with parse failure. *Consequence:* block — the walking skeleton (Step 9) does not pass, so H1a/H1b/H2/H3 cannot be evaluated at all until A1 is restored (no partial scoring on a confounded cell).
- **A2 — The difficulty proxy is not circular noise.** Low-budget solve rate (M1) rank-correlates with dataset-native tags and a second model's solve rate. *Failure:* strata encode model idiosyncrasy (t2). *Detection:* pilot gate — Spearman ρ ≥ 0.4 vs MATH levels AND vs second-model rate; else switch primary stratification to native tags (pre-committed). *Consequence:* degrade — H1a/H2 are re-scored under the native-tag stratification instead of the solve-rate proxy (pre-committed substitute, not a new post-hoc choice); RQ_INF_1's difficulty-conditioning claim is downgraded to "conditioned on the tag-based proxy only" if the two stratifications disagree.
- **A3 — The studied grid can contain a flip for at least some strata.** *Failure:* curves still rising at 16k everywhere (digest N6 feasibility risk). *Detection:* Stage-0 pilot on easy/medium quintiles + synthetic family whose difficulty parameter guarantees low-L\* strata; failure everywhere triggers F-G1. *Consequence:* block-and-pivot — H1a (and transitively H2, H3, which require H1a holding on ≥2 strata) cannot be scored as designed; the paper's central hypothesis family is replaced wholesale by the Global fallback F-G1 (well-powered refutation + censoring study).
- **A4 — Per-token logprobs and probe generations are obtainable** (vLLM harness, M2/M4). *Failure:* serving stack drops logprobs. *Detection:* skeleton (logprob completeness check per rollout). *Consequence:* restrict scope — H1b and H3 (which need entropy-trajectory features and truncated-answer probes) are dropped from the studied model/serving combination; H1a and H2 (which only need graded final answers, not logprobs) remain evaluable on the affected rollouts.
- **A5 — Correctness is auto-gradable** (exact-match/numeric on MATH-500, GSM8K, AIME, GPQA-D, synthetic). *Failure:* grader mislabels reformatted answers. *Detection:* pilot — manual audit of 100 graded answers; grader error ≤2%. *Consequence:* degrade — grader error above 2% triggers a grading-rule patch (documented, not silently re-tuned) and re-audit before any H\* is scored; all four hypotheses depend on graded correctness, so an unresolved grader failure blocks all of E1–E3, not just one.
- **A6 — Cell-level power is achievable.** ≥1,200 Bernoulli observations per (stratum, L) cell detect a 5pp drop at α=0.05, power 0.8 (digest N8 analysis plan). *Failure:* budget cuts rollouts. *Detection:* pre-run token-cost accounting in skeleton; AIME excluded from per-item statistics (t4). *Consequence:* restrict scope — thin cells (e.g. AIME) are pre-declared INCONCLUSIVE for that cell only (never silently dropped or scored as null), per guidance.md Part 4 situation 5; H1a/H2/H3 are scored on the remaining adequately powered strata and the narrowed scope is stated in the headline, not buried in Limitations.

## Step 6 — Pre-Registered Experiments

### E1 (RQ1) — Does marginal return flip sign, and do cheap signals see it?

- **Assumption:** A1, A3, A4, A5, A6.
- **Hypothesis H1a (flip exists):** In ≥2 of 5 difficulty quintiles, A_s(L_peak) − A_s(L_max) ≥ **3pp** with Holm-corrected one-sided paired bootstrap p < 0.05, and the negative-slope region replicates (same sign, p < 0.05) in **≥2 of the 3 length-control arms** (truncation, forced continuation, natural stopping). Binary: yes/no.
- **Hypothesis H1b (signal informativeness):** At least one cheap feature family (entropy-trajectory OR early-consistency, M4) achieves **AUROC ≥ 0.65** (95% CI excluding 0.5) for classifying sign(marginal gain beyond the 256-token probe point), on held-out strata. Binary: yes/no.
- **Metric:** A_s(L); Δ_s(L_k); peak-vs-max contrast; per-feature AUROC (Step 5 definitions; digest N8 metrics).
- **Verification:** item-level clustered bootstrap, 10,000 resamples, one-sided, Holm correction across 5 strata × 3 arms (15 tests); pilot ≥100 items/quintile × 7 lengths × 8 rollouts, Stage 1 ≥16 rollouts/cell (digest N8 plan). AUROC CI by stratified bootstrap over items.
- **Fallback (pre-committed wording):** If H1a fails: *"Within 256–16k thinking tokens, we find no statistically detectable negative-return region in [model family]: test-time reasoning exhibits diminishing, never negative, returns — a well-powered null that removes the empirical footing of overthinking-motivated stopping rules in this regime."* (= digest N9 Result-1 falsification, promoted to headline; see F-G1.) If only H1b fails: *"The sign flip exists but is invisible to trajectory-level cheap signals; boundary exploitation requires difficulty-bin information"* (claim CO2 is dropped, CO1 retained).

### E2 (RQ_INF_1) — Is the tipping point difficulty-conditioned?

- **Assumption:** A2, A3, A6 (and H1a holding on ≥2 strata).
- **Hypothesis H2:** Jonckheere–Terpstra trend test on L\*_s across ordered quintiles rejects at **p < 0.05** with right-censored strata assigned max rank, AND the ordering replicates directionally (no significant reversal) on the synthetic tunable-difficulty family. Binary: yes/no.
- **Metric:** L\*_s per stratum with bootstrap CI; censoring indicator; trend statistic (digest N8).
- **Verification:** JT test on stratum-level L\*_s (5 natural quintiles; ≥5 synthetic difficulty levels); reversal check = JT on synthetic suite with opposite alternative must NOT reject at p < 0.05.
- **Fallback (pre-committed wording):** *"The sign-flip location is statistically indistinguishable from a single universal length threshold across difficulty strata — overthinking onset is a model-level constant, which simplifies deployment (one global budget cap suffices) but refutes difficulty-conditioned budget allocation as a premise."* (= digest N9 Result-2 falsification, reframed as an equally decision-relevant finding.)

### E3 (RQ_INF_2) — Does predicting the boundary pay at matched cost?

- **Assumption:** A1–A6 (and H1a; H1b failing routes to the E1 fallback first).
- **Hypothesis H3:** At matched mean token cost, predicted-stop (a) beats the best single fixed budget on paired per-item correctness, McNemar **p < 0.05**; (b) recovers oracle-gap fraction **G ≥ 0.5**; (c) achieves G strictly greater than the coarse 3-class prefill-probe baseline's G. All three required. Binary: yes/no.
- **Metric:** G (Step 5); token savings at matched accuracy (% thinking-token reduction vs always-max at ≤1pp accuracy drop) reported descriptively; Spearman ρ(L̂\*, L\*) at α=0.01 as the predictor-quality gate (digest N8).
- **Verification:** M5 protocol — Pareto comparison of predicted-stop vs {fixed budgets on 𝓛} vs per-stratum oracle vs DEER-style confidence exit vs prefill probe, all at matched mean cost; McNemar on Stage-1 held-out items; predictor trained/evaluated under cross-stratum and cross-domain holdouts only.
- **Fallback (pre-committed wording):** *"Trajectory-level cheap signals do not convert the boundary map into allocation gains beyond difficulty-bin membership: a 3-class pre-hoc probe already captures the exploitable structure, and the map's value is diagnostic (where budgets are wasted) rather than a new stopping policy."* (CO3 dropped; CO1 + the negative comparative result retained, per digest N9 Result-3 falsification.)

### Mechanism analysis (R6, added at Phase A re-run per guidance.md Part 6 item 8 / Part 2 A2's evidence standard)

*A2's evidence standard requires ≥1 mechanism analysis beyond the headline localization — explaining* why *the marginal return flips, not only* that *and* where *it flips (guidance.md R6). This was previously missing from Step 6; added here, budgeted alongside E1, not deferred to future work.*

- **M6 — Trace-content mechanism probe.** For items whose stratum shows a localized L\*_s (H1a-positive strata only), compare the reasoning trace content just before vs. just after L\*_s across rollouts: (i) self-correction rate (fraction of rollouts where the truncated-answer probe's answer changes between L_k and L_{k+1}), split by whether the change is correct→incorrect or incorrect→correct; (ii) verification/backtracking step density per 256-token window (keyword+structure heuristic, e.g. "wait", "let me check", re-derivation), before vs. after L\*_s; (iii) correlation between the entropy-trajectory slope (M4 feature) and the sign of the answer-flip at L\*_s. **Pre-registered prediction:** the correct→incorrect flip rate rises sharply past L\*_s relative to before it, and this rise co-occurs with elevated verification-step density (the mechanism guessed at in Step 0: continued reasoning overwrites an already-correct answer via a verification/backtracking step that itself introduces the error) — not merely a diffuse accuracy decay. **Falsification:** if correct→incorrect and incorrect→correct flip rates are statistically indistinguishable before vs. after L\*_s (paired bootstrap, α=0.05), the localized boundary is real (per H1a) but its mechanism is not verification-induced self-overwriting — Claim 1 (existence of the flip) survives, but the Step-0 asymmetry's causal story is downgraded to descriptive-only, and CO1 is reported without a mechanism claim.
- **Reporting:** one mechanism-analysis subsection per Stage-1 dataset family (natural + synthetic), with the flip-rate contrast reported as a plain-language magnitude gloss (R4) alongside the statistic.

### Mandatory baselines

- **B0 — "why do this at all" control: uniform fixed budgets, including always-max.** Every fixed L ∈ 𝓛 applied to all items (this includes uniform budget forcing per [Muennighoff et al., 2025 (s1)]). If the best fixed budget already sits within **1pp** of per-stratum oracle stopping at equal cost, the boundary map has no allocation value and the problem, as posed for deployment, does not exist — this arm is what makes E3's question non-vacuous, and its accuracy-vs-L aggregate curve is also the no-stratification control for E1 (a flip visible only after stratification is the phenomenon; a flip visible in the aggregate is old news per [Chen et al., 2024]).
  **B0's second job — null-by-construction placebo (guidance.md §3.3; added 2026-07-05, closing the Phase G to-do logged in `discussion/pipeline.md`):** before any hypothesis (H1a/H1b/H2/H3, M6) is scored, the identical item-paired bootstrap and change-point procedure (M3) is run on a placebo control in which grid-length labels are randomly permuted within each item's rollout set — severing any true length–accuracy relationship while preserving the marginal accuracy distribution — and the same Holm-corrected test is applied. A "significant" flip detected under this permutation indicates a pipeline artifact (e.g. multiple-comparison leakage or a miscalibrated bootstrap) rather than a property of the reasoning process, and blocks scoring of every downstream hypothesis until fixed (goal.md §8: B0 evaluated before any hypothesis; a non-null placebo invalidates the run).
- **B-alt — strongest-alternative-explanation control.** *Rival explanation:* "the cheap signals carry no trajectory-level information — any predictive success merely re-encodes (i) difficulty-bin membership and/or (ii) trace-position/length priors." Two budget-matched arms isolate this: (1) the **3-class prefill hidden-state probe** ([DiffAdapt] / [AdaptiveThinking] reimplementation, M4-iii) — same training data, same holdouts, strictly pre-hoc; (2) a **length-only null feature set** (position-controlled, digest t5) fed to the identical predictor architecture. H1b/H3 claims stand only over both. *Rival for E1's flip itself:* "degradation is a truncation-format artifact" (t1) — isolated by requiring arm agreement (≥2 of 3 manipulations, incl. forced continuation which involves no abrupt closing) inside H1a rather than as a separate arm.

### Global fallback F-G1

If the central hypothesis family (H1a AND H2) fails — no detectable sign flip, or no difficulty structure — the archetype pivots from *boundary map* to *well-powered refutation + censoring study* (still `empirical`). Pivoted abstract sentence, pre-committed: *"Across 3 model scales, 5 datasets, and three independent length manipulations totaling N rollouts, we find no difficulty-conditioned regime within practical budgets (≤16k tokens) where additional thinking reduces accuracy — implying that the overthinking premise motivating current stopping-rule and length-penalty methods is either an artifact of specific manipulations or lives beyond deployed budget ranges, and publishing the resulting censored boundary curves as the null landscape those methods must beat."*

## Step 9 — Walking Skeleton

**One binary question:** *Can the truncation harness produce valid, gradable, logprob-complete answers whose accuracy measurably moves with L on easy items?* (Gates A1, A4, A5 before any grid.)

- **Arms (2):** (i) truncation at L ∈ {512, 2k, 8k} with forced answer; (ii) natural stopping (unconstrained), as the format-artifact reference.
- **Task set:** 50 MATH-500 items — 25 Level 1–2, 25 Level 5 — one model (DeepSeek-R1-Distill-Qwen-7B), 4 rollouts per (item, L): 50×3×4 + 50×4 = 800 generations, prefix-shared (one 8k trace yields all truncation points; only forced-answer suffixes regenerated).
- **Deterministic metrics only:** parse rate per cell; logprob completeness rate; exact-match accuracy per (level-group, L); sign of A(easy, 512) − A(easy, 8k). No bootstrap, no predictor, no synthetic family.
- **Expected cost:** ≤ ~8×10⁶ generated tokens ≈ 4–10 A100-hours (or < $50 API-class); < 1 day wall-clock.
- **Pass criterion:** parse rate ≥ 95% AND logprob completeness ≥ 99% in every cell, AND accuracy varies with L on easy items by ≥ 5pp between some pair of lengths (direction not required at this stage). **Skeleton passed ⇒ Stage 0/1 are config changes only** (item counts, grid 𝓛, rollout count, model list, dataset list — all YAML), not code changes; the analysis code path (grading → curves) is already exercised end-to-end.

## Claim–Evidence Map

| Claim (digest Claims section) | Traces to | Status |
|---|---|---|
| Marginal benefit turns negative beyond a difficulty-dependent length | H1a + H2; Step-5 defs of Δ_s, L\*_s | needs-experiment (fallback-covered: E1/E2 fallbacks + F-G1) |
| No prior work publishes the boundary map the adaptive-reasoning literature presupposes | digest N4 limitations 2–4 (corpus-grounded) | supported-by-design (literature claim; no experiment needed) |
| Cheap pre-hoc signals predict the tipping point beyond length-only and difficulty-bin nulls | H1b + H3(c) + B-alt | needs-experiment (fallback-covered: E1b/E3 fallbacks) |
| Predictive stopping recovers a substantial fraction of the oracle tradeoff at lower cost | H3(a,b); Step-5 def of G | needs-experiment (fallback-covered: E3 fallback) |
| The tipping point is not a universal threshold (anti one-size-fits-all budgets) | H2 + B0 (aggregate vs stratified contrast) | needs-experiment (fallback-covered: E2 fallback) |
| The same generative process that produced a correct answer can overwrite it (Step-0 asymmetry's causal mechanism, echoed in Abstract v0) | M6 mechanism probe (added at Phase A re-run, guidance.md R6) | needs-experiment (fallback-covered: M6 falsification — if flip-rate contrast is not significant, this row downgrades to descriptive-only and the abstract's causal wording must drop to "coincides with" per the stale-claim gate, goal.md §8) |

Every abstract claim below maps to a row above; no orphan claims (row above added at Phase A re-run to close a gap: the Abstract's causal mechanism sentence had no traced experiment before M6 existed).

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; all outcomes pending E1–E3)

Marginal test-time reasoning compute has a difficulty-indexed sign: past a boundary length, the same process that produced a correct answer can overwrite it, so returns flip negative rather than merely flattening. Stopping rules, difficulty probes, and length-penalty training all presuppose this boundary; none has measured it. We measure it. Stratifying tasks by an operational difficulty proxy (low-budget solve rate crossed with native tags), we localize, per stratum and under three independent length manipulations, the point where the marginal accuracy return of thinking turns negative — with change-point statistics, censoring made explicit, and pre-registered criteria. We then isolate whether cheap pre-hoc signals (entropy trajectories within 256 thinking tokens, four truncated-answer probes) predict this boundary beyond difficulty-bin membership and length priors, and quantify the fraction of the oracle accuracy–cost tradeoff that predicted stopping recovers at matched token cost.
