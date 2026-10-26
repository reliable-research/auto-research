# Experiment Design Spec — B4.6 (standalone protocol, Stage 6 confirmed output)

> Rendered from `discussion_trace.md` Stage 6, with the three `stage_review.md` fixes folded in (gate A1 first-hand confirmation; Tier-A wall-clock scope condition; latency descriptive readout in RQ1). Target hypotheses are **verbatim** from Stage 5 / Stage 3 — do not paraphrase them when executing. Every number below is an authored design target with a stated rationale, not a measured fact. Status: pre-registered; **no experiment has been run.** Date: 2026-08-15.

## Global design parameters (frozen before any measurement; hash the config)

- **Step typing.** A session is parsed into generation steps, non-verification tool steps, and verification steps with class K = {lint, type-check, unit, build, suite} and outcome ∈ {pass, fail, error}. A verification *target* is the pair (class, scope path); a **retry segment** is the contiguous step span from a failed verification of target f to the next verification attempt of the same target f (unterminated segments end at session end and are reported separately).
- **Attribution rules.** Conservative ρ_cons: verification execution seconds + verification feedback tokens injected into context (priced at their prefill/decode cost). Liberal ρ_lib: ρ_cons + all generation and tool cost inside retry segments. Both rules frozen before measurement; the estimand is the interval [ρ_cons, ρ_lib].
- **Cost model.** Two cache policies: Θ1 radix-tree prefix cache (SGLang-style, LRU node eviction) and Θ2 block-hash prefix cache (vLLM-style, block size 16). Three price vectors, frozen: P1 API-metered (per-token input/output with cached-input discount), P2 self-host GPU-hour amortized to tokens, P3 latency-weighted (P2 plus a per-second session-latency charge). Sensitivity grid = {P1,P2,P3} × {Θ1,Θ2}.
- **Session integrity filters.** Include sessions with recoverable per-step token accounting, ≥ 1 verification step, and a recorded terminal outcome; report the exclusion rate; excluded sessions never enter any headline n.
- **Instrument validation (walking-skeleton gates, all pass before scale-up):**
  - **A1 (substrate + novelty confirmation, upgraded per stage_review Stage-2 fix).** Re-verify the TraceLab corpus facts (~4,300 sessions, 430K tool calls, typed tool calls) against the actual release, **and read the TraceLab paper first-hand to confirm it reports no verification-attributed cost share, no retry attribution, and no cache-interaction analysis.** Pre-committed consequence: if any of the three exists, reposition per guidance.md situation 6 before trusting any measurement.
  - **A2 (step-type labeling).** Audit the automated step/class labeler on 200 randomly sampled tool calls against 2 independent human raters; require Cohen's κ ≥ 0.8 and adjacent-only confusion structure; a miss blocks scale-up.
  - **A3 (cost-model calibration).** Calibrate the replay simulator against real vLLM and SGLang runs on 20 replayed sessions; require simulated prefill-token counts within ±10% of measured; report calibration error alongside every cache result.
  - **A4 (kill-test).** Conservative-only ledger on 200 sessions: if the median conservative dollar share < 0.05, the premise is in danger — stop and re-examine before scaling (this is the one-day minimum-viable check).
- **Placebo B0 (checked before any hypothesis is scored).** Shuffle step-type labels within each session (preserving label counts); the attribution pipeline must then yield verification-attributed share ≈ its token share (ratio ≤ 1.1) and cache-invalidation ratio ≈ 1. A non-null placebo invalidates the run (guidance.md situation 1); no RQ is scored from an invalid run.
- **Tier partition (with the stage_review Stage-3 scope fix).** A reschedule π is **Tier A (replay-exact)** iff it preserves the agent-visible token sequence byte-for-byte; Δ$ is then exact *for the recorded sessions under the frozen cost model*. The deployment reading of Tier-A headroom additionally assumes no wall-clock-dependent agent behavior (step timeouts, latency-conditioned prompt content); the incidence of such constructs in the corpus is reported descriptively as a scope statement. Everything else is **Tier B (live)**: evaluated only by live re-execution under the non-inferiority certificate below.
- **Live arms.** SWE-bench Verified, 300 instances × 2 scaffolds (OpenHands; SWE-agent) × 3 seeds per arm, paired by (instance, seed) across arms. Non-inferiority on resolve rate: one-sided δ = 5pp at α = 0.05 via the paired discordant-pair (McNemar-style) construction; power ≥ 0.8 to certify when the true difference is 0 given discordance ≤ 0.15. A confidence bound straddling the margin is pre-declared **INCONCLUSIVE** — never a silent pass. (δ = 2pp at this n was computed to be undecidable and rejected in Stage-6 review.)
- **Speculation predictor.** Pass/fail predictor on pre-step observables (class, files touched, diff size since last same-class check, recent failure count, session phase, last lint status), trained on TraceLab only, frozen and hashed before any live run; held-out TraceLab AUC reported (target ≥ 0.75). The **oracle arm** is computed by replay over native live-run logs (an oracle never mispredicts, so its speculative continuations are outcome-identical by construction); the **frozen-predictor arm** requires live runs because mispredictions create rollback and divergent context.
- **Under-powered or gate-failing cells** are reported INCONCLUSIVE, never null, never dropped silently.

## Datasets

1. **TraceLab public traces** (arXiv:2606.30560) — the only public corpus at session granularity with typed tool calls; carries RQ1–RQ6 and predictor training. Corpus facts subject to gate A1.
2. **Self-run SWE-bench Verified sessions** (Jimenez et al., 2024; scaffolds: OpenHands, Wang et al. 2024; SWE-agent, Yang et al. 2024) — the only valid regime for Tier-B evaluation, and the cross-corpus half of RQ2.

## Baselines (sanity comparators — `study_type: empirical`; nothing is framed as a competitor to beat)

- The **native agent schedule** (recorded behavior) — the measured object and the reference condition for headroom.
- **Shuffled-step-type placebo** (B0) — validity control for the attribution pipeline.
- **Volume-matched neutral-filler re-rendering** — cache-side control isolating content churn from volume + position.

## Research questions

### RQ1 — What share of a session's serving cost is verification-induced? *(mechanism)*

- **Target hypothesis (H1, verbatim):** "On TraceLab sessions passing integrity filters, the median session's verification-induced dollar share has conservative bound at least 0.15 and liberal bound at least 0.30; the premise is falsified if even the liberal bound falls below 0.10."
- **Setup:** full ledger over all filtered TraceLab sessions; per-session [ρ_cons, ρ_lib] under P1/Θ1 (headline cell), decomposed into execution, feedback-token, retry-generation, and (from RQ3) cache-re-prefill components.
- **Sample-size rationale:** the corpus (~4,300 sessions) gives bootstrap CIs on median shares with half-widths well under 0.02 at 10,000 resamples; the binding constraint is corpus size, not power.
- **Statistical test:** 95% bootstrap CIs on median ρ_cons and ρ_lib; the H1 verdict compares CI bounds to the pre-registered floors.
- **Expected outcome:** median ρ_cons ≥ 0.15 and median ρ_lib ≥ 0.30.
- **Falsification condition:** refuted if the upper CI bound of median ρ_lib < 0.10 — verification would then not be a first-class cost object and the paper's premise fails openly (the certified small share becomes the reported finding, per the pre-committed pivot).
- **Metrics:** dollar-share interval (headline); component decomposition; **latency-share readout (descriptive, per the stage_review Stage-4 fix):** verification execution wall-time + attributable retry-generation time over session wall-time — reported alongside, not tested; headline verdicts are scoped to the dollar denomination.

### RQ2 — Are the headline verdicts artifacts of any single accounting choice? *(mechanism)*

- **Target hypothesis (H2, verbatim):** "Every headline verdict (H1's threshold verdict, H3's ratio verdict, H6's headroom verdict) is invariant across the three price vectors, both cache policies, and both corpora; falsified if any verdict flips under any grid cell."
- **Setup:** recompute RQ1, RQ3, RQ6 verdicts over the full {P1,P2,P3} × {Θ1,Θ2} grid and on the self-run SWE-bench corpus (identical ledger code).
- **Sample-size rationale:** grid recomputation reuses RQ1/RQ3/RQ6 samples; the SWE-bench arm has 1,800 native sessions (300 × 2 × 3), sufficient for verdict-level (not estimate-level) comparison.
- **Statistical test:** verdict-category comparison per cell; estimate differences reported with bootstrap CIs.
- **Expected outcome:** verdict categories unchanged in every cell; point estimates move, verdicts do not.
- **Falsification condition:** refuted if any headline verdict flips in any grid cell or on the second corpus — the affected claim is then downgraded to the accounting envelope in which it holds, per the pre-committed wording.
- **Metrics:** verdict matrix over the grid; per-cell estimates.

### RQ3 — Does verification output destroy disproportionate prefix-cache reuse? *(mechanism)*

- **Target hypothesis (H3, verbatim):** "Verification outputs account for a share of re-prefilled (invalidated) tokens at least 1.5 times their share of context tokens, under both cache policies; falsified if the ratio is at most 1.1 under either policy."
- **Setup:** replay each session's request sequence through Θ1 and Θ2; count re-prefilled tokens attributable to verification-output spans vs their context-token share; the volume-matched neutral-filler re-rendering supplies the null reference (its ratio should be ≈ 1 — this is also the cache-side placebo).
- **Sample-size rationale:** deterministic replay over the full corpus; CIs from session-level bootstrap.
- **Statistical test:** 95% bootstrap CI on the median invalidation ratio, per policy.
- **Expected outcome:** ratio ≥ 1.5 under both policies; filler control ≈ 1.
- **Falsification condition:** refuted if ratio ≤ 1.1 under either policy (verification content no worse than inert content of the same volume and position), or if the filler control deviates from 1 (attribution artifact — run invalid for this RQ).
- **Metrics:** invalidation ratio per policy; absolute re-prefill dollars; filler-control ratio.

### RQ4 — Is the cache damage format-driven or semantically necessary? *(mechanism)*

- **Target hypothesis (H4, verbatim):** "Canonicalizing volatile spans in verification output recovers at least half of the verification-attributable invalidation; falsified if recovery is below one quarter."
- **Setup:** re-render verification outputs with volatile spans (paths, timestamps, durations, truncation boundaries) canonicalized; replay under Θ1/Θ2; compare verification-attributable re-prefill against RQ3.
- **Sample-size rationale / test:** as RQ3 (deterministic replay, bootstrap CIs).
- **Expected outcome:** ≥ 50% of verification-attributable invalidation recovered — the churn is mostly format, i.e., removable without changing what the agent learns.
- **Falsification condition:** refuted if recovery < 25% — the damage would then be semantically necessary (genuinely new content each turn), and the "stabilize the renderer" implication is dropped in favor of the honest negative.
- **Metrics:** recovery fraction per policy; residual (semantic) invalidation share.

### RQ5 — Is the per-class cost–value frontier heterogeneous or degenerate? *(mechanism)*

- **Target hypothesis (H5, verbatim):** "Across verification classes, median execution cost spans at least a factor of 10 (lint to full suite) while stratified action-divergence spans at most a factor of 3 — that is, value per dollar differs by at least a factor of 3 across classes; falsified (degenerate frontier) if cost and stratified value are proportional within a factor of 1.5."
- **Setup:** per class: cost profile from the ledger; action-divergence and terminal-relevance estimated within pre-defined strata of (session phase, files touched, diff size since last same-class check). **Positivity gate (pre-registered):** a stratum enters only with ≥ 30 steps from ≥ 2 classes; if fewer than half of strata pass, the frontier is reported descriptive-only and H5 is scored INCONCLUSIVE.
- **Sample-size rationale:** 430K tool calls give expected thousands of verification steps per class; the gate, not the corpus, is the binding constraint and its pass rate is itself reported.
- **Statistical test:** stratum-weighted class contrasts with cluster-robust (per-session) bootstrap CIs.
- **Expected outcome:** cost span ≥ 10×, stratified value span ≤ 3×.
- **Falsification condition:** refuted if value per dollar is uniform within 1.5× across classes — granularity-aware scheduling would then be pointless and the finding is the degeneracy itself.
- **Metrics:** per-class cost and value profiles with stratum counts; positivity-gate pass rate.

### RQ6 — How much of the recorded bill is avoidable by agent-transparent rescheduling alone? *(mechanism)*

- **Target hypothesis (H6, verbatim):** "Tier-A rescheduling alone recovers at least 10% of the median session's total serving dollars at byte-identical outcomes; falsified if the recovered share is below 5%." (Coupling clause, verbatim from Stage 5: if H1 is falsified at the 0.10 level, H6 is scored against a re-based floor of half the measured liberal share, with the re-basing stated.)
- **Setup:** exact replay of Tier-A reschedules — batching verification executions, sandbox placement/prewarming, cache-aware scheduling of re-prefill, overlapping verification execution with same-turn decode — under the frozen cost model; grid-search within Tier A is legitimate (the probe may be as strong as possible; the estimand is the workload's avoidable share, not any policy's merit). Scope condition per the stage_review Stage-3 fix: exactness holds for recorded sessions under the frozen cost model; the deployment reading assumes no wall-clock-dependent agent behavior, whose incidence in the corpus is reported.
- **Sample-size rationale / test:** deterministic replay, full corpus; bootstrap CI on median recovered share.
- **Expected outcome:** recovered share ≥ 10% of total session dollars.
- **Falsification condition:** refuted if < 5% (< half the re-based floor under the coupling clause) — serving-side-only gains would then be marginal and the headroom story shifts to Tier B or fails.
- **Metrics:** recovered dollar share (median + distribution); breakdown by mechanism (batching / placement / cache-aware / overlap); wall-clock-dependence incidence.

### RQ7 — Is speculative continuation past predicted-pass verifications viable at realistic predictor quality? *(framing — from the Stage-3 `hypothesis_to_verify` on the nearest neighbor's limitation)*

- **Target hypothesis (verbatim, Stage 3):** "Speculative continuation past verifications predicted to pass yields net positive dollar savings on live coding-agent runs at non-inferior resolve rate; with an oracle pass/fail predictor the median saving is at least 15% of session serving dollars, and a frozen trace-trained predictor retains at least half of the oracle saving. The claim is falsified if oracle savings fall below 5% (speculation headroom absent regardless of predictor quality) or if the frozen predictor retains less than a quarter of oracle savings (headroom exists but is predictor-limited beyond practical reach)."
- **Setup:** oracle arm by replay over native live-run logs; frozen-predictor arm by live re-execution (rollback on misprediction: discard speculated tokens, charge them to the arm, resume from the verified state). Non-inferiority per the global certificate (δ = 5pp, paired, one-sided α = 0.05).
- **Sample-size rationale:** 300 × 2 × 3 = 1,800 paired runs per arm; power ≥ 0.8 for the non-inferiority certificate at discordance ≤ 0.15 (Stage-6 round-1 fix; δ = 2pp rejected as undecidable).
- **Statistical test:** paired discordant-pair non-inferiority test on resolve rate; bootstrap CIs on dollar savings.
- **Expected outcome:** oracle ≥ 15% median savings; frozen predictor ≥ half of oracle; resolve non-inferior.
- **Falsification condition:** as in the hypothesis (oracle < 5%, or frozen < quarter of oracle); resolve-rate non-inferiority failure caps the claim regardless of savings; straddling CI → INCONCLUSIVE.
- **Metrics:** oracle and realized dollar savings; predictor held-out AUC; misprediction/rollback cost share; paired resolve-rate difference with CI.
