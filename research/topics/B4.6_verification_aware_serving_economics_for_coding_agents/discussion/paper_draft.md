# The Verification Tax: Measuring Verification-Induced Cost and Avoidable Spend in Coding-Agent Serving

> Assembled from the six confirmed stage outputs in `discussion_trace.md`, post-audit (`taste_audit.md`: 🟢) and post-review (`stage_review.md`: three stage-level REVISE fixes plus two Writing-stage fixes folded in). Status: **specification / paper draft — no experiments have been run.** All numbers below are pre-registered design targets with stated rationales, not results.

## Abstract

Coding agents interleave code generation with verification — lint passes, type checks, unit tests, builds, full test suites — and feed the results back into their context. The serving stacks that host them price generation precisely while treating verification as opaque tool time: its execution cost is unmetered against the same budget, its output's effect on prefix-cache reuse is uncounted, and the retry loops its failures trigger are indistinguishable from ordinary progress. Two workload characterizations of coding-agent serving now exist, and neither carries verification-step semantics; dollar-priced speculative execution has been proposed, but without real-trace grounding and without the verify decision as its scheduling object. We pre-register a trace-grounded measurement of the verification tax on public coding-agent traces: an interval-valued ledger that bounds the verification-induced share of session dollars between attribution rules with known-direction bias; a cache-counterfactual replay that attributes prefix-cache invalidation to verification content specifically; a per-class cost–value profile across lint, type-check, unit, build, and suite; and a two-tier headroom evaluation — exact replay for reschedules the agent cannot observe, live non-inferiority-gated runs for those it can — that measures how much of the recorded bill is avoidable at matched resolve rate. Every estimate carries a pre-registered falsification bar, including the bar under which verification is not a first-class cost at all.

## Introduction

Coding agents have become a serving workload in their own right. A single issue-resolution session runs an LLM through dozens of generation steps interleaved with tool calls, and platform-scale deployments now meter this traffic at the scale of trillions of tokens — enterprise inference-economics analyses and a production characterization spanning 3.2 million users exist precisely because operators are paying these bills (arXiv:2608.00101; arXiv:2607.13080). On the serving side, an equally mature line of systems work — paged KV memory (Kwon et al., 2023), radix-tree prefix caching (Zheng et al., 2023), prefill/decode disaggregation (Zhong et al., 2024; Qin et al., 2024), chunked-prefill scheduling (Agrawal et al., 2024) — optimizes the cost of serving these token streams, on the shared premise that reusing cached prefixes and scheduling prefill work well is where the money is.

Yet one structural feature of the coding-agent workload is invisible to both communities' cost models: a large class of its steps are verifications. A lint pass, a type check, a unit test, a build, a full suite run — each executes outside the model, returns output that is injected back into the prompt, and, on failure, triggers a repair loop whose generation cost is causally downstream of the verification event. Serving stacks price every generated token but treat these steps as opaque tool time: their execution is not metered against the same budget as the tokens they cause, their outputs' effect on prefix-cache reuse is not counted, and a retry loop is indistinguishable from forward progress. The agent-side literature is no better positioned: test-time-compute analyses meter thinking and sampling in FLOPs or tokens and treat checking as an afterthought (Brown et al., 2024; Snell et al., 2024), and the feedback loop itself — run the tests, read the failures, try again — has been standard since Reflexion (Shinn et al., 2023) and execution-based checking since pass@k (Chen et al., 2021), without anyone pricing what the loop costs the serving layer. No published number says what fraction of a coding-agent session's dollars is verification-induced, how much prefix-cache reuse verification output destroys, or how much of either is avoidable.

The nearest existing work brackets this gap without closing it. TraceLab (arXiv:2606.30560) released the first public trace corpus of coding-agent workloads — roughly 4,300 sessions and 430,000 tool calls, with test, build, and edit steps distinguishable — but characterizes the workload in aggregate, with no verification-attributed cost share, no retry attribution, and no cache-interaction analysis; a production-scale study of Copilot traffic (arXiv:2608.00101) shares the same silence and releases no traces. Cost-Aware Speculative Execution for LLM-Agent Workflows: An Integrated Five-Dimension Method (arXiv:2606.07846) is the closest methodological neighbor: it prices speculation in dollars, as we do, but is not grounded in real traces, does not treat the verify decision as its scheduling object, and does not model verification's cache damage. Queueing-theoretic scheduling for LLM inference and agents (Dai et al., 2025) already models Generate and Verify as distinct service classes — theoretical precedent that the distinction matters — but presumes exactly the per-class cost, value, and churn parameters that have never been measured. And the agent-aware caching cluster (KVFlow, Pan et al., 2025; Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving, arXiv:2605.05696, among at least five systems in three months) improves reuse for agent workloads while remaining blind to which step semantics destroy reuse in the first place.

Measuring the verification tax from observational traces is harder than counting labeled steps, and the difficulties are what shape our design. A retry loop's tokens are causally downstream of a failed verification yet interleaved with genuine progress, and the trace contains no counterfactual session without verification — so any point estimate of induced cost would be arbitrary. Cache invalidation is a joint effect of content churn, position, and volume under a specific cache policy — so raw hit-rate differences cannot say whether verification *content* is at fault. The information value of a verification class cannot be read off outcomes, because agents run cheap checks after edits and expensive suites at endpoints — a scheduling-habit confound that turns naive class comparisons into artifacts. And a rescheduling counterfactual is only as valid as its evaluation: replaying a recorded session under a schedule that changes what the agent would have seen answers nothing, which is precisely the trace-grounding weakness of the nearest neighbor.

This paper's design is built around a single claim: verification steps are priced by serving stacks as opaque tool time, yet they are the workload's most cost-heterogeneous, most cache-hostile, and most reschedulable step class — and both halves of that claim are measurable from public traces. Each difficulty above becomes a design choice. Attribution is interval-valued by construction: a conservative rule (direct execution and feedback tokens only) and a liberal rule (plus complete retry segments) have known-direction bias on each side, so the truth is bracketed without a counterfactual. Cache damage is attributed by counterfactual re-rendering: unlike agent behavior, cache behavior is a deterministic function of the token sequence under a fixed policy, so replaying volume-matched inert content and canonicalized verification output isolates churn from volume, position, and format — an intervention that is exact on the cache even though it would be invalid on the agent. Class value is estimated only within strata of pre-step context, behind a pre-registered positivity gate that downgrades the frontier to descriptive if agents' habits turn out too phase-locked to support comparison. And headroom is evaluated in two tiers split by an invariance predicate: reschedules that preserve the agent-visible token sequence byte-for-byte are evaluated by exact replay, with outcomes identical by construction; reschedules that change what the agent sees — speculatively continuing past a verification predicted to pass, and rolling back on failure — are evaluated only by live re-execution under a pre-registered non-inferiority margin on resolve rate.

We evaluate this design on the TraceLab public corpus and on self-run SWE-bench Verified sessions (Jimenez et al., 2024) under two open scaffolds (Yang et al., 2024; Wang et al., 2024), with a shuffled-label placebo gating the attribution pipeline and every headline verdict recomputed across three price vectors, two cache policies, and both corpora.

In summary, we contribute:

- A formalization of verification-induced serving cost as an interval-valued estimand — bounded between attribution rules with known-direction bias — together with a session-level ledger that computes it from public traces, in dollars and (descriptively) in latency.
- A cache-counterfactual replay method that attributes prefix-cache invalidation to verification content specifically, separating churn from volume, position, and format, and measuring how much of the damage is removable by canonicalizing volatile output spans.
- A per-class cost–value profile across lint, type-check, unit, build, and suite — the empirical parameters that existing Generate/Verify scheduling theory presumes — estimated behind an explicit positivity gate that reports, rather than hides, when agents' scheduling habits make the comparison unidentifiable.
- A two-tier headroom evaluation, split by an agent-visibility invariance predicate, that pre-registers how much of the recorded serving bill is avoidable at matched resolve rate: exactly, for reschedules the agent cannot observe; and under a live non-inferiority certificate, for speculative continuation past predicted-pass verifications.

## Problem Definition

**Formal setup.** A session $s = (x_1, \ldots, x_n)$ interleaves generation steps, non-verification tool steps, and verification steps; each verification step carries a class $k \in K$ — lint, type-check, unit, build, or suite — a scope (the file or module checked), and an outcome (pass / fail / error). A verification *target* is the pair (class, scope); a *retry segment* is the contiguous step span from a failed verification of target $f$ to the next verification attempt of the same target. A serving cost model $C_{p,\Theta}(s)$ maps the session's request sequence to dollars given a price vector $p$ (per input token, output token, cached-input token, and verification-execution second) and a prefix-cache policy $\Theta$, counting prefill (cache-miss) tokens, decode tokens, and execution time. The objects of study are four: (i) the verification-induced share $\rho(s) = [\rho_{\mathrm{cons}}(s), \rho_{\mathrm{lib}}(s)]$ of $C_{p,\Theta}(s)$, an interval under two fixed attribution rules; (ii) the verification-attributable share of invalidated (re-prefilled) cache tokens; (iii) per-class cost and information-value profiles over $K$; and (iv) the headroom $\Delta(\pi) = C_{p,\Theta}(s) - C_{p,\Theta}(\pi(s))$ over admissible reschedules $\pi$, partitioned by the invariance predicate $\iota(\pi)$ — "the agent-visible token sequence is preserved byte-for-byte" — and reported only at matched resolve rate: identically-matched by construction when $\iota$ holds, or certified by a pre-registered one-sided non-inferiority margin on live runs when it does not.

**Why this is hard.** The trace contains no counterfactual session without verification, so $\rho$ is unidentifiable pointwise: any single attribution rule embeds an arbitrary causal judgment about which retry tokens verification "caused." The two rules above are chosen so that each side's bias direction is known by construction — the conservative rule can only undercount (it ignores induced repairs entirely), the liberal rule can only overcount (it absorbs all in-segment progress) — making the interval, not either endpoint, the honest estimand. Cache invalidation compounds the problem: under a prefix cache, a token's cost depends on whether the tokens before it changed, so verification output that churns — volatile paths, timestamps, durations, truncation boundaries re-rendered between turns — can cost multiples of its own length, but only a counterfactual re-rendering under the same policy $\Theta$ can separate that churn from the volume and position any equally long content would occupy. The per-class profiles are confounded by scheduling habits — agents run lint after edits and the suite at endpoints, so class and context are entangled, and only within-stratum contrasts (with verified overlap) license even an ordering claim. Finally, $\Delta(\pi)$ is only measurable where its evaluation is valid: replay is exact precisely on the $\iota$-preserving subclass, and anything beyond it requires live re-execution — a partition the nearest prior work does not draw, and the reason its dollar-priced speculation results are not trace-grounded.

## Method Overview

The study is a single measurement pipeline with four cooperating instruments. Typed sessions enter; the **verification cost ledger** turns each into an interval-valued verification-induced dollar share, decomposed into execution, feedback-token, retry-generation, and cache-re-prefill components, and recomputes every verdict across price vectors, cache policies, and corpora. The **cache-counterfactual replay** runs the same sessions through two prefix-cache simulators against re-rendered variants — volume-matched inert filler, and canonicalized verification output — to attribute invalidation to verification content and to measure how much of it is mere format. The **per-class value profiler** pairs each class's ledger cost with stratified estimates of its information value (does the outcome change the agent's next action; does it move eventual resolution), behind a positivity gate. The **two-tier headroom evaluation** consumes all three: it partitions candidate reschedules by the agent-visibility invariance predicate, replays the invariant tier exactly against the ledger's cost model, and sends the visible tier — speculative continuation past predicted-pass verifications — to live runs under a non-inferiority certificate, with an oracle-predictor arm bounding what speculation could ever recover and a frozen trace-trained predictor measuring what it recovers realistically.

## Methodology

### Verification Cost Ledger

**Challenge.** Retry-loop generation is causally downstream of failed verification yet interleaved with genuine progress, and no counterfactual verification-free session exists in the trace — a point attribution would be arbitrary, and the field would be right to ignore it.

**Insight.** The decision the estimand feeds — is verification a first-class cost object? — does not need a point; it needs an interval whose endpoints have known-direction bias. Bounding replaces the counterfactual that does not exist.

**Method.** Each session is parsed into typed steps (step-type labeling audited against two independent human raters, Cohen's $\kappa \geq 0.8$, adjacent-only confusion required, before scale-up). Direct costs — verification execution seconds and feedback tokens injected into context — are computed exactly. Retry segments are delimited structurally by the (class, scope) target identity. The conservative share $\rho_{\mathrm{cons}}$ counts direct costs only; the liberal share $\rho_{\mathrm{lib}}$ adds all generation and tool cost inside retry segments; both are dollar-ized under three pre-registered price vectors (API-metered; self-host GPU-hour; latency-weighted) and both cache policies, on TraceLab and on self-run SWE-bench sessions with identical code. Latency shares are computed alongside and reported descriptively; headline verdicts are scoped to the dollar denomination. A shuffled-step-type placebo gates the pipeline: with labels randomly re-assigned within a session, the "verification-attributed" share must collapse to its token share, or the run is invalid before any hypothesis is scored.

### Cache-Counterfactual Replay

**Challenge.** Prefix-cache invalidation is a joint effect of content churn, position, and volume under a specific cache policy; a raw hit-rate deficit cannot say whether verification content is at fault.

**Insight.** Cache behavior, unlike agent behavior, is a deterministic function of the token sequence given a policy — so counterfactual re-rendering, invalid as an intervention on the agent, is exact as an intervention on the cache.

**Method.** Each session's request sequence is replayed through a radix-tree prefix-cache simulator (SGLang-style) and a block-hash simulator (vLLM-style), both calibrated against real engine runs on a session subsample (simulated prefill counts within $\pm 10\%$ of measured, reported alongside every cache result). Three renderings are replayed: the recorded session; a volume-matched inert-filler variant (same lengths, same positions — the null reference, which must show ratio $\approx 1$); and a canonicalized variant with volatile spans (paths, timestamps, durations, truncation boundaries) rewritten to stable forms. The first delta attributes invalidation to verification content; the second measures how much of that damage is format-driven — removable without changing anything the agent learns — versus semantically necessary.

### Per-Class Value Profiler

**Challenge.** Agents run cheap checks after edits and expensive suites at session endpoints, so verification class and step context are entangled; naive class comparisons measure scheduling habits, not information value.

**Insight.** Scheduling needs only the ordering of value per dollar across classes, and an ordering claim is licensed by within-stratum contrasts — provided overlap actually holds, which is checkable and must be checked.

**Method.** For each class, the ledger supplies the cost profile; two value proxies are estimated within pre-defined strata of session phase, files touched, and diff size since the last same-class check: action-divergence (the probability that the agent's next action differs between pass and fail outcomes) and terminal relevance (the shift in eventual-resolution probability associated with the outcome). A pre-registered positivity gate admits a stratum only with at least 30 steps from at least two classes; if fewer than half the strata pass, the frontier is reported as descriptive only and its hypothesis is scored inconclusive — the failure of overlap is itself a finding about how phase-locked agents' verification habits are.

### Two-Tier Headroom Evaluation

**Challenge.** A rescheduling counterfactual is only as valid as its evaluation: replaying a session under a schedule that changes what the agent would have seen is off-policy and answers nothing — the precise trace-grounding weakness of the nearest prior work.

**Insight.** The agent-visibility boundary converts one ill-posed off-policy problem into two well-posed ones: an exact simulation for reschedules the agent cannot observe, and a small live experiment for those it can — and the boundary, not simulator fidelity, is what makes each headroom claim valid.

**Method.** A reschedule is Tier A iff it preserves the agent-visible token sequence byte-for-byte: batching verification executions, sandbox placement and prewarming, cache-aware scheduling of re-prefill, overlapping verification execution with same-turn decode. Tier-A headroom is computed by exact replay under the frozen cost model; recorded outcomes are reused by construction. Its exactness is scoped explicitly: it holds for the recorded sessions under the stated cost model, and its deployment reading additionally assumes no wall-clock-dependent agent behavior (step timeouts, latency-conditioned prompts), whose incidence in the corpus is reported descriptively. Tier B breaks the invariance — its representative is speculative continuation past verifications predicted to pass, rolling back (and paying for) discarded tokens on misprediction — and is evaluated only by live SWE-bench re-execution, paired by instance and seed, under a one-sided 5-percentage-point non-inferiority margin on resolve rate. A pass/fail predictor over pre-step observables is trained on TraceLab only and frozen (hashed) before any live run; an oracle arm — computable by replay over native live-run logs, since an oracle never mispredicts — bounds achievable speculation headroom from above, so the frozen-predictor arm reads as a fraction of a measured ceiling rather than an isolated number.

## Experiments

### Experimental Setup

**Datasets.** TraceLab public traces (arXiv:2606.30560) — roughly 4,300 sessions and 430,000 tool calls with test/build/edit steps distinguishable; the only public corpus at session granularity with typed tool calls; carries the ledger, cache, frontier, and Tier-A analyses and the predictor's training split. Its corpus facts, and the absence of verification-attributed analysis in its paper, are confirmed first-hand as a blocking pre-measurement gate — with a pre-committed repositioning if the confirmation fails. Self-run SWE-bench Verified sessions (Jimenez et al., 2024) under two open scaffolds — OpenHands (Wang et al., 2024) and SWE-agent (Yang et al., 2024) — at 300 instances $\times$ 2 scaffolds $\times$ 3 seeds per arm: the only valid regime for agent-visible reschedules, and the second corpus for verdict stability.

**Cost model.** Two cache policies (radix-tree, block-hash), three price vectors (API-metered; self-host GPU-hour amortized; latency-weighted), all frozen and hashed before measurement; simulator calibration error reported with every cache result.

**Run provenance and study cost.** Every live arm pins a single backbone model checkpoint and a fixed decoding configuration (temperature, top-p, maximum steps) per scaffold, frozen and hashed together with the cost model before any run; scaffold versions are pinned by commit. The live arms are the study's dominant expense — at minimum two arms of 1,800 paired SWE-bench runs each, plus calibration subsamples — so the realized dollar spend per arm is reported alongside the savings estimates it prices, in the same price vectors: a study about serving dollars that did not disclose its own serving bill would fail its own standard.

**Baselines** (sanity comparators — this is a measurement study; nothing is framed as a competitor to beat). The native agent schedule is the measured object and the reference for all headroom. A shuffled-step-type placebo gates the attribution pipeline before any hypothesis is scored. A volume-matched inert-filler re-rendering is the cache-side null control.

**Metrics.** Interval dollar shares and their decomposition; latency shares (descriptive); invalidation ratios and canonicalization recovery; per-class cost and value profiles with stratum counts; Tier-A recovered share by mechanism; oracle and realized speculation savings with predictor AUC and rollback cost; paired resolve-rate differences with confidence bounds.

**Research questions:**
1. RQ1 — What share of a session's serving cost is verification-induced?
2. RQ2 — Are the headline verdicts artifacts of any single accounting choice?
3. RQ3 — Does verification output destroy disproportionate prefix-cache reuse?
4. RQ4 — Is the cache damage format-driven or semantically necessary?
5. RQ5 — Is the per-class cost–value frontier heterogeneous or degenerate?
6. RQ6 — How much of the recorded bill is avoidable by agent-transparent rescheduling alone?
7. RQ7 — Is speculative continuation viable at realistic predictor quality?

#### RQ1: What share of a session's serving cost is verification-induced?

**Setup.** Full ledger over all integrity-filtered TraceLab sessions; per-session conservative/liberal interval under the headline price-vector/cache-policy cell, with component decomposition. Sample size: the full corpus (~4,300 sessions); 95% bootstrap confidence intervals on median shares (10,000 resamples) have expected half-widths well under 0.02, so corpus size, not power, binds.

**Expected outcome.** Median conservative share at least 0.15 and median liberal share at least 0.30 — verification clears the pre-registered first-class-cost bar.

**Falsification condition.** Refuted if the upper confidence bound of the median liberal share falls below 0.10 — verification would then not be a first-class cost object, and the certified small share is reported as the finding under the pre-committed pivot, at full prominence.

**Hypothesis (plain language).** A session's verification-induced spending is large enough that serving stacks mislabeling it as opaque tool time are mispricing a first-order cost driver.

**Metrics.** Dollar-share interval (headline); execution / feedback-token / retry-generation / cache-re-prefill decomposition; latency share reported descriptively, with headline verdicts scoped to dollars.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Are the headline verdicts artifacts of any single accounting choice?

**Setup.** Recompute the RQ1, RQ3, and RQ6 verdicts over the full grid of three price vectors and two cache policies, and on the self-run SWE-bench corpus with identical ledger code (1,800 native sessions).

**Expected outcome.** Point estimates move; verdict categories do not — every headline verdict is invariant across the grid and both corpora.

**Falsification condition.** Refuted if any headline verdict flips in any grid cell or on the second corpus; the affected claim is then downgraded, with pre-committed wording, to the accounting envelope in which it holds.

**Hypothesis (plain language).** The paper's conclusions are properties of the workload, not artifacts of one price sheet, one cache policy, or one trace corpus.

**Metrics.** Verdict matrix over the grid; per-cell estimates with confidence intervals.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Does verification output destroy disproportionate prefix-cache reuse?

**Setup.** Deterministic replay of every session under both cache policies; re-prefilled tokens attributable to verification-output spans compared against those spans' share of context tokens; the volume-matched inert-filler rendering supplies the null reference and doubles as the cache-side placebo.

**Expected outcome.** Verification outputs account for a share of invalidated tokens at least 1.5 times their context-token share under both policies, while the filler control sits near 1.

**Falsification condition.** Refuted if the ratio is at most 1.1 under either policy — verification content would then be no worse for the cache than inert content of equal volume and position; and the RQ is invalidated (attribution artifact) if the filler control deviates materially from 1.

**Hypothesis (plain language).** Verification output is cache-hostile beyond its length: it churns, and churn under a prefix cache is what costs money.

**Metrics.** Invalidation ratio per policy; absolute re-prefill dollars; filler-control ratio; simulator calibration error.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Is the cache damage format-driven or semantically necessary?

**Setup.** Replay the canonicalized rendering (volatile spans — paths, timestamps, durations, truncation boundaries — rewritten to stable forms) under both policies; compare verification-attributable re-prefill against RQ3's.

**Expected outcome.** Canonicalization recovers at least half of the verification-attributable invalidation — most of the damage is format, removable without changing what the agent learns.

**Falsification condition.** Refuted if recovery falls below one quarter — the damage would then be semantically necessary, and the stabilize-the-renderer implication is dropped in favor of the honest negative.

**Hypothesis (plain language).** The cache damage is mostly an artifact of how verification output is rendered, not of what it says.

**Metrics.** Recovery fraction per policy; residual (semantic) invalidation share.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Is the per-class cost–value frontier heterogeneous or degenerate?

**Setup.** Per class: ledger cost profile; action-divergence and terminal relevance estimated within pre-defined strata of session phase, files touched, and diff size since the last same-class check, with cluster-robust (per-session) bootstrap intervals. The positivity gate (at least 30 steps from at least two classes per admitted stratum) is applied first; its pass rate is itself reported.

**Expected outcome.** Median execution cost spans at least a factor of 10 from lint to full suite while stratified action-divergence spans at most a factor of 3 — value per dollar differs by at least threefold across classes, so granularity-aware scheduling has something real to exploit.

**Falsification condition.** Refuted (degenerate frontier) if cost and stratified value are proportional within a factor of 1.5 across classes; scored inconclusive, with the frontier reported as descriptive only, if fewer than half the strata pass the positivity gate.

**Hypothesis (plain language).** The cheap checks buy disproportionate information per dollar; pooling all verification into one number hides the very structure a scheduler would use.

**Metrics.** Per-class cost and value profiles with stratum counts; positivity-gate pass rate.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: How much of the recorded bill is avoidable by agent-transparent rescheduling alone?

**Setup.** Exact replay of agent-transparent reschedules — batching verification executions, sandbox placement and prewarming, cache-aware scheduling of re-prefill, overlapping verification execution with same-turn decode — under the frozen cost model, searching freely within the invariant tier (the probe may be as strong as possible: the estimand is the workload's avoidable share, not any policy's merit). The wall-clock scope condition applies and the corpus incidence of timeout- or latency-conditioned agent constructs is reported alongside.

**Expected outcome.** At least 10% of the median session's total serving dollars is recovered at byte-identical outcomes.

**Falsification condition.** Refuted if the recovered share falls below 5%; and if RQ1 is itself refuted at the 0.10 level, this floor is re-based to half the measured liberal share, with the re-basing stated — so one bad constant cannot fail two questions for one reason.

**Hypothesis (plain language).** A meaningful slice of the verification tax is refundable without the agent ever noticing.

**Metrics.** Recovered dollar share (median and distribution); breakdown by mechanism; wall-clock-dependence incidence.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Is speculative continuation viable at realistic predictor quality?

**Setup.** Conditional on the live arms: oracle savings computed by replay over native live-run logs (an oracle never mispredicts, so its continuations are outcome-identical by construction); realized savings from live runs with the frozen, TraceLab-trained predictor, rollback tokens charged to the arm. Non-inferiority on resolve rate: paired by instance and seed, one-sided 5-percentage-point margin at $\alpha = 0.05$ via the discordant-pair construction — power at least 0.8 when the true difference is zero given discordance at most 0.15 (a 2-point margin at this sample size is undecidable and was rejected at design review). Sample size: 300 instances $\times$ 2 scaffolds $\times$ 3 seeds = 1,800 paired runs per arm.

**Expected outcome.** Oracle savings of at least 15% of session serving dollars; the frozen predictor retains at least half of the oracle saving; resolve rate non-inferior.

**Falsification condition.** Refuted if oracle savings fall below 5% (speculation headroom absent regardless of predictor quality) or if the frozen predictor retains less than a quarter of the oracle saving (headroom exists but is predictor-limited beyond practical reach); a non-inferiority failure on resolve rate caps the claim regardless of savings, and a straddling confidence bound is reported as inconclusive.

**Hypothesis (plain language).** Continuing past checks that will pass is worth real money only if pass/fail is predictable enough — and both the ceiling and the realizable fraction are measured, not assumed.

**Metrics.** Oracle and realized dollar savings; predictor held-out AUC; misprediction and rollback cost share; paired resolve-rate difference with confidence bound.

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, two natural extensions are pre-registered as out of scope: instrumented-scaffold experiments that randomize verification cadence directly (upgrading the frontier's ordering claim to a causal one), and an online scheduler that consumes the measured profiles in a production serving stack — the systems paper this measurement study is deliberately not.

### Threats to Validity

**Construct validity.** The verification-induced share is attribution-rule-dependent by construction; the design's answer is the interval with known-direction bias at each end, the shuffled-label placebo that any attribution artifact must fail, and the grid recomputation that catches accounting-choice artifacts. The value proxies (action-divergence, terminal relevance) are behavioral correlates, not causal effects; the ordering claim is licensed only within gated strata, and the pre-committed downgrade (descriptive frontier, inconclusive verdict) triggers if overlap fails.

**Internal validity.** Step-type labels are an instrument and are audited (two raters, $\kappa \geq 0.8$, adjacent-only confusion) before scale-up. The cache simulators are calibrated against real engines with a $\pm 10\%$ acceptance bar and reported error. Tier-A exactness holds for recorded sessions under the frozen cost model; its deployment reading assumes no wall-clock-dependent agent behavior, whose corpus incidence is reported rather than assumed away.

**External validity.** Findings are scoped to the corpora and scaffolds measured: TraceLab's session mix and two open SWE-bench scaffolds. The production study whose scale motivates the problem releases no traces, so transfer to proprietary deployments is argued only via the verdict-stability grid, not asserted. Several load-bearing neighbor characterizations were engaged at corpus-scan depth during design; their bibliographic metadata has since been verified against the arXiv export API, but metadata is not full text, so the pre-measurement gate still requires first-hand confirmation that TraceLab's paper indeed lacks verification-attributed analysis, with a pre-committed repositioning if that confirmation fails — the novelty position is checked, not presumed. The frozen pass/fail predictor is additionally trained on TraceLab and deployed on live SWE-bench sessions, a cross-corpus transfer whose degradation is itself measured (held-out AUC on both corpora) rather than assumed benign; a predictor-limited outcome is a pre-registered result of RQ7, not a failure of the design.

**Conclusion validity.** Every hypothesis carries a pre-registered floor and falsification direction; under-powered or gate-failing cells are reported inconclusive, never null, never silently dropped; the placebo is scored before any hypothesis; and the non-inferiority margin was widened at design review from an undecidable 2 points to a powered 5 points rather than left to fail quietly.

## Related Work

The closest prior work is Cost-Aware Speculative Execution for LLM-Agent Workflows: An Integrated Five-Dimension Method (arXiv:2606.07846), and the delta is worth stating plainly before surveying the landscape: it shares this paper's dollar-denominated objective for agent-serving decisions, but it is not grounded in real traces, does not make the verify decision itself the scheduling object, and does not model verification's damage to prefix-cache reuse — the three properties this design is built around. We concede the shared objective and claim the measurement: trace-grounded attribution, cache interaction, and a validity-partitioned headroom estimate.

**Coding-agent workload characterization.** TraceLab (arXiv:2606.30560) released the first public coding-agent trace corpus with typed tool calls and characterizes the workload for serving-system design; a production-scale study of Copilot traffic (arXiv:2608.00101) does the same at 3.2-million-user scale without releasing traces; enterprise inference-economics analyses (arXiv:2607.13080) evidence that operators meter exactly this spending. Per the occupancy analysis this project ran before committing, a third aggregate characterization has no room — and none of the three carries verification-step semantics: no verification-attributed cost share, no retry attribution, no cache-interaction analysis. That absent dimension, confirmed first-hand as a pre-measurement gate, is precisely this paper's estimand.

**Agent-aware serving and caching.** The serving canon — PagedAttention (Kwon et al., 2023), SGLang's radix-tree reuse (Zheng et al., 2023), disaggregated prefill/decode (Zhong et al., 2024), KV-cache-centric production serving (Qin et al., 2024), chunked-prefill scheduling (Agrawal et al., 2024) — establishes that prefix reuse and prefill scheduling are where serving money concentrates, which is exactly why invalidation is a first-order term in our ledger. On top of it, an agent-aware cluster (KVFlow, Pan et al., 2025; Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving, arXiv:2605.05696; and at least three further systems within three months) optimizes cache behavior using workflow structure — but treats step content generically, so none can say which step semantics destroy reuse. This paper measures the channel those systems would need: verification output as a churn source, and how much of its damage canonicalization removes.

**Verification in test-time compute and agent loops.** Execution-based checking has anchored code generation since pass@k (Chen et al., 2021); Reflexion (Shinn et al., 2023) made feed-the-failure-back the standard agent loop; repeated sampling (Brown et al., 2024) and compute-optimal test-time scaling (Snell et al., 2024) allocate generation compute with verification treated as free or afterthought, denominating budgets in FLOPs or tokens rather than serving dollars. SWE-bench (Jimenez et al., 2024) and the open scaffolds that attack it (SWE-agent, Yang et al., 2024; OpenHands, Wang et al., 2024) fix the task substrate and produce exactly the session shape studied here. None of this line prices the verification loop's serving-side cost — the quantity our ledger bounds.

**Scheduling theory and speculation.** Queueing-theoretic scheduling for LLM inference and AI agents (Dai et al., 2025) models Generate and Verify as distinct service classes and derives throughput-optimal policies — theoretical precedent that the distinction matters for scheduling — but presumes the per-class cost, value, and churn parameters this paper estimates; our profiles are the empirical side of that model. Token-level speculative decoding (Leviathan et al., 2023) is the intra-request ancestor of step-level speculative continuation, and SpecBox: Speculative Sandbox Scheduling for Efficient LLM Agent Serving (arXiv:2607.23933) supplies a sandbox-prewarming mechanism speculation would use — a mechanism without a policy or an economic objective, which is where the live, non-inferiority-gated speculation arms of this study sit.

## Conclusion

This work reframes a serving-stack blind spot as a measurable quantity with a falsification bar: verification — the step class serving systems price as opaque tool time — is either a first-class cost object with measurable cache damage and refundable headroom, or it is not, and the design commits in advance to reporting either answer. The methodological wager is that observational traces, which cannot support pointwise causal attribution, can still support decision-grade claims when every estimand is given the strongest evidence its identification actually licenses: intervals with known-direction bias where no counterfactual exists, exact counterfactuals where the system (a cache) is deterministic, gated ordering claims where confounding is checkable, and a validity partition that sends each rescheduling counterfactual to the only regime — replay or live — that can honestly evaluate it. Whichever way the headline numbers fall, the profiles this study pre-registers are the parameters that existing Generate/Verify scheduling theory presumes and that agent-aware caching systems would need to become semantics-aware. The design's weakest identification is named rather than hidden: the per-class value ordering rests on stratified observational contrasts behind a positivity gate, and upgrading it to a causal claim requires instrumented scaffolds that randomize verification cadence — the natural next experiment, alongside the online scheduler that would consume these measurements in production and that this measurement study deliberately declines to be.

## References

> Script-generated from `discussion/refs.bib` (from `reference_candidates.jsonl` via `gen_refs_bib.py`), then metadata-synced by hand: this list is the Markdown-readable mirror. All 21 entries have been verified against the arXiv export API (15 on 2026-08-15 at build time; the remaining six 2026 entries batch-resolved in the 2026-08-15 supervisor repair and re-verified live on 2026-08-21, with published titles and author lists replacing the earlier scan-recorded placeholders).

- Agrawal, A., Kedia, N., Panwar, A., Mohan, J., Kwatra, N., Gulavani, B. S., Tumanov, A., Ramjee, R. Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve. OSDI, 2024. (arXiv:2403.02310)
- Fareed, F. Cost-Aware Speculative Execution for LLM-Agent Workflows: An Integrated Five-Dimension Method. arXiv:2606.07846, 2026.
- Peng, S.-W., Lin, Y.-H., Lee, Y.-P. Inference Economics of Enterprise Coding Agents: A Case Study of Cloud vs. On-Premise LLMs. arXiv:2607.13080, 2026.
- Ma, B., Eitzinger, J., Köstler, H. Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving. arXiv:2605.05696, 2026.
- Liu, B., Qiu, H., Goiri, Í., Fonseca, R., Bianchini, R., Choukse, E. Agentic Coding in the Wild: Characterizing GitHub Copilot Traces at Production Scale. arXiv:2608.00101, 2026.
- Zhang, Y., Wo, T., Wang, J., Sun, X., Zhang, M., Yuan, C., Li, L., Hu, C., Zomaya, A. Y., Yang, R. SpecBox: Speculative Sandbox Scheduling for Efficient LLM Agent Serving. arXiv:2607.23933, 2026.
- Zhu, K., Jacob, M., Ma, C., Pan, Y., Wang, S., Krishnamurthy, A., Kasikci, B. TraceLab: Characterizing Coding Agent Workloads for LLM Serving. arXiv:2606.30560, 2026.
- Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V., Ré, C., Mirhoseini, A. Large Language Monkeys: Scaling Inference Compute with Repeated Sampling. arXiv:2407.21787, 2024.
- Chen, M., Tworek, J., Jun, H., et al. Evaluating Large Language Models Trained on Code. arXiv:2107.03374, 2021.
- Dai, J. G., Deng, T., Li, Y., Peng, T. Throughput-Optimal Scheduling Algorithms for LLM Inference and AI Agents. arXiv:2504.07347, 2025.
- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR, 2024. (arXiv:2310.06770)
- Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C. H., Gonzalez, J. E., Zhang, H., Stoica, I. Efficient Memory Management for Large Language Model Serving with PagedAttention. SOSP, 2023. (arXiv:2309.06180)
- Leviathan, Y., Kalman, M., Matias, Y. Fast Inference from Transformers via Speculative Decoding. ICML, 2023. (arXiv:2211.17192)
- Pan, Z., Patel, A., Hu, Z., Shen, Y., Guan, Y., Li, W.-L., Qin, L., Wang, Y., Ding, Y. KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows. arXiv:2507.07400, 2025.
- Qin, R., Li, Z., He, W., Zhang, M., Wu, Y., Zheng, W., Xu, X. Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving. arXiv:2407.00079, 2024.
- Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S. Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS, 2023. (arXiv:2303.11366)
- Snell, C., Lee, J., Xu, K., Kumar, A. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. arXiv:2408.03314, 2024.
- Wang, X., Li, B., Song, Y., et al. OpenHands: An Open Platform for AI Software Developers as Generalist Agents. arXiv:2407.16741, 2024.
- Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., Press, O. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS, 2024. (arXiv:2405.15793)
- Zheng, L., Yin, L., Xie, Z., et al. SGLang: Efficient Execution of Structured Language Model Programs. arXiv:2312.07104, 2023.
- Zhong, Y., Liu, S., Chen, J., Hu, J., Zhu, Y., Liu, X., Jin, X., Zhang, H. DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving. OSDI, 2024. (arXiv:2401.09670)

---

## Pre-handoff checklist

- **Organization/navigation** — problem → definition → apparatus → experiments → related work, no forward reference to undefined terms; "verification tax," "retry segment," "invariance predicate," "Tier A/Tier B" each defined at first use.
- **Terminology discipline** — no internal stage IDs (`sp_*`, `m_*`, `rq_*`, H-numbers) in prose; checked by grep.
- **Notation** — the formal setup defines $(s, K, \rho_{\mathrm{cons}}, \rho_{\mathrm{lib}}, C_{p,\Theta}, \Delta(\pi), \iota)$ and later sections reuse it; no worked numeric example, since no numbers exist yet.
- **RQ framing matches outcomes** — all 7 RQs are graded/quantitative, each with an explicit falsification condition; none binary yes/no.
- **No typesetting artifacts** — only the explicit `[placeholder — fill in after experiments are run]` markers in Results.
- **Artifact plan** — the ledger/replay harness, canonicalization rules, and per-session decomposition tables are the natural release artifacts; not yet built, so not claimed as available.

## Hand-off

This is a pre-registered specification, not a report — Phases B–D (walking skeleton, full-scale runs, verdict splice) have not run in this environment. Execute from `experiment_design.md` (the standalone protocol), not from this draft; if piloting fails a gate (the TraceLab first-hand confirmation, the labeling audit, the placebo, or the kill-test), that is a cross-stage event that re-opens the relevant stage rather than a number to absorb.
