# Port, Prune, or Relearn: Measuring Per-Skill Value Change in Agent Skill Libraries Across Backbone Upgrades

> Assembled from the six confirmed stage outputs in `discussion_trace.md`, post-audit (`taste_audit.md`: 🟢) and post-review (`stage_review.md`: four REVISE findings applied). Status: **specification / paper draft — no experiments have been run.** All numbers below are pre-registered design targets with stated rationales, not results.

## Abstract

LLM agents accumulate skill libraries — verified, reusable procedures — to amortize exploration cost into lasting capability. Every one of those skills, however, was acquired under a specific backbone model whose failure modes it encodes, and every backbone upgrade silently invalidates that encoding: the staleness axes the field has measured are skill accumulation and environment change, and the model-generation axis has so far been measured only as functional transfer accuracy — never in value terms. We freeze libraries acquired under older backbones and replay identical, mechanically-verified task streams (MBPP+, SWE-bench, ALFWorld) under newer model generations, in paired arms — bare, full-library, token-matched placebo-library, and per-skill masked — to estimate each skill's signed change in marginal utility per token. A trace-signature decomposition separates three loss mechanisms demanding different upgrade actions: obsolescence, active interference, and cost drag. We pre-register tests of whether libraries can flip from asset to liability under a stronger backbone, whether per-skill value change is heterogeneous enough to make selective retirement worthwhile, whether functional portability predicts value retention, and whether thresholding the measured estimates recovers most of an oracle's cost–success frontier — turning the recurring port/prune/relearn decision from guesswork into accounting.

## Introduction

Skill libraries have become a standard mechanism by which LLM agents convert expensive exploration into reusable capability: an agent solves a task, distills the solution into a verified procedure — a code snippet, a workflow, an action macro — and retrieves it when similar tasks recur. The design assumption inherited from the line of work that popularized this pattern is that accumulated skills are a monotone asset: acquisition cost is paid once, and value accrues with every reuse. That assumption is priced into how these systems are built — libraries ship with agents, persist across sessions, and grow without retirement policies.

Yet a central fact about every skill in such a library goes unrecorded: it was acquired under a specific backbone model, and much of what it encodes is compensation for that backbone's particular weaknesses — a workaround for parsing errors the old model made, a scaffold for reasoning steps the old model could not take alone, a defensive check against a failure mode the old model exhibited. In short, every skill encodes the failure modes of the backbone that acquired it, but the library carries no record of which backbone that was. When the backbone is upgraded — which now happens at every major model release — that encoding is silently invalidated. If stale skills merely go unused, the loss is bounded: wasted acquisition investment plus retrieval overhead. If they actively mislead the stronger model, the library becomes worse than nothing, and the monotone-asset assumption fails in the direction that silently degrades deployed systems. The operator facing an upgrade must choose among porting everything, wiping and relearning, or pruning ad hoc — and currently has no measured basis for any of the three.

The nearest existing work approaches this gap from adjacent but distinct angles. The staleness-diagnostics line measures skill-library rot on axes that hold the backbone fixed: Library Drift shows ungoverned accumulation — unbounded skill growth without outcome-driven lifecycle management — dragging a coding agent below its own no-library baseline, and the contract-violation line detects when a skill functionally breaks as its environment (packages, services, APIs) evolves. Cross-model work reports the opposite slice: a snapshot transfer-accuracy number for skills moved between models, with no cost accounting and no retention decision attached. And the economics framing exists without measurement: a survey conceptualizes tokens as economic primitives of agent operation, but no per-skill payback or depreciation curve has been reported for any real library. No prior work replays a frozen library across real backbone generations and asks what each skill is now worth.

Turning this question into a measurement surfaces three confounds that a naive with/without comparison cannot separate. A library is not only content: it is thousands of prompt tokens (pure context load), and an altered action space (a stronger backbone may invoke skills more or less often than the one that built them), and any cross-backbone comparison is dominated by the capability difference between the models themselves. Each of these alone can produce the same observed gap as genuinely harmful content. A further difficulty is scale: skills act in combinations under retrieval gating, so the factorial experiment that would attribute value per skill is exponentially infeasible, and any tractable per-skill estimator must defend the conditions under which its contrasts identify a per-skill quantity at all.

Even a clean measurement is not yet a decision: which action is right depends on *why* a skill lost value. An obsolete skill — one the new backbone succeeds without — is a cost-accounting problem that tolerates lazy pruning. An interfering skill — invoked, and inducing failures the bare model avoids — demands urgent retirement even if rarely used. A cost-drag skill — same outcomes, more tokens — is a compression target. These three mechanisms produce identical library-level deltas, so a library-level A/B toggle at upgrade time cannot choose the right action; and if per-skill value change is heterogeneous, both corner policies can sit far from the achievable frontier simultaneously, never-retire keeping the harmful minority while full-relearn re-buys the still-valuable majority.

Our design turns each obstacle into a specific instrument. Backbone generation becomes a clean treatment variable by freezing everything else: the same library, task stream, retriever, prompts, and turn budgets are replayed under each backbone, with the asset-or-liability verdict always paired against the *same* backbone running bare, so model capability cancels. A token-matched placebo library — syntactically valid, retrievable, task-irrelevant — carries the context load without the content, serving as the measurement's null instrument; forced-use and free-use invocation regimes separate what the content does from how often the model chooses to use it. A leave-one-out utility ledger turns the infeasible factorial into one bounded paired contrast per skill on that skill's own activation set, with an explicit additivity check (pairwise interaction probing with a pre-set bound, and a pre-committed downgrade to cluster-granularity reporting if it fails). Mechanical trace signatures — computed from execution outcomes and token billing, with no judge model — classify each depreciated skill as obsolete, interfering, or cost drag. Finally, an oracle-normalized retention sweep asks the decision question as a property of the measurement itself: not whether some policy wins, but how much of the frontier available to an oracle that knows true post-upgrade values is recovered by thresholding our estimates, at a pre-registered matched-success operating point.

We evaluate this design across three mechanically-verified task streams — execution-checked function synthesis, repository-level issue resolution, and embodied household tasks — and at least three real public backbone upgrade pairs spanning two vendor families and one two-generation gap, with acquisition, reuse, and measurement costs all metered in tokens.

In summary, we contribute:
- A formalization of backbone generation as an independent staleness axis for agent skill libraries — previously measured only as functional transfer accuracy, never in value terms — with a per-skill estimand — the signed change in marginal utility per token between acquisition-time and post-upgrade backbones — that turns the port/prune/relearn decision into a measurable quantity.
- An identification design for that estimand: same-backbone paired contrasts that cancel capability differences, a token-matched placebo library that isolates context-load effects, invocation-regime controls that separate content from selection, and an interaction-probed leave-one-out ledger that makes per-skill attribution tractable and honest about when it is licensed.
- A mechanical three-way decomposition of skill value loss — obsolescence, interference, cost drag — computable from paired execution traces alone, each mechanism mapped to a different upgrade action.
- A pre-registered test suite covering the asset-to-liability flip, value-change heterogeneity, generation-distance dose response, estimate reliability, the dissociation between functional portability and economic value, and the decision-adequacy of the measured estimates against an oracle frontier — with falsification conditions and pre-committed fallback readings for each.

## Problem Definition

**Formal setup.** A skill library L = {σ_1, ..., σ_K} is acquired by a fixed agent harness running backbone M_0 over a task stream, where each skill σ_k is an inspectable text/code artifact with a retrieval key, and its acquisition ledger records the provenance backbone, the tokens spent acquiring it, and its validation record. Consider an upgrade pair (M_0, M_1), where M_1 is a newer public generation, and a fixed evaluation stream T = {τ_1, ..., τ_N} of tasks with mechanical verifiers. For an arm A ∈ {bare, L, L∖{σ_k}, placebo}, let y(τ, M, A) ∈ {0, 1} be the verifier outcome and c(τ, M, A) ≥ 0 the token cost of running task τ under backbone M with arm A, everything else held byte-identical. Skill σ_k's activation set T_k ⊆ T is the set of tasks on which the retriever selects it. Its marginal utility under M is u_k(M) = E_{τ∈T_k}[ y(τ, M, L) − y(τ, M, L∖{σ_k}) ], with cost companion γ_k(M) = E_{τ∈T_k}[ c(τ, M, L) − c(τ, M, L∖{σ_k}) ].

**Estimand.** The object of study is the signed per-skill value change Δu_k = u_k(M_1) − u_k(M_0) — and, for skills whose acquisition-time utility clears a positive floor, the retention ratio r_k = u_k(M_1) / u_k(M_0) — together with the library-level contrast E_τ[ y(τ, M_1, L) − y(τ, M_1, bare) ] and its cost analogue. In one sentence: the quantity is the change in each skill's task-success benefit per token of cost when the frozen library is replayed under a newer backbone generation than the one that acquired it; the unit of analysis is one (skill, upgrade pair); the reference population is skill libraries induced by current LLM agents on mechanically-verified task streams; and the decision it feeds is the per-skill port/prune/relearn choice at upgrade time.

**Why this is hard.** The library-level contrast confounds three causes — content, context load, and invocation propensity — that only additional arms can separate: the placebo arm holds load and retrieval mechanics while removing content, and the forced-use regime holds invocation while isolating content effects. The per-skill quantity u_k is defined through a leave-one-out contrast, which identifies a per-skill value only when cross-skill interactions are second-order; because skills compose and retrieval competes, this is an assumption to be probed, not asserted, and the reporting granularity must degrade honestly when it fails. The retention ratio r_k is undefined or unstable when u_k(M_0) is near zero, which forces an acquisition-value floor and leaves below-floor skills — including any whose harm concentrates there — outside the per-skill estimate's reach. And every estimate is computed from finite, stochastic replays on small activation sets, so stability across disjoint task splits must be demonstrated before any ranking built on the estimates can be trusted.

## Method Overview

The study is a single measurement pipeline with five cooperating instruments. A fixed acquisition loop produces frozen, ledgered libraries; a cross-backbone replay harness turns backbone generation into a controlled treatment and produces the library-level asset-or-liability verdict; a placebo library gives that verdict its null instrument; a leave-one-out ledger converts the same replays into per-skill value estimates with an explicit licensing check; a trace-signature decomposition explains measured losses mechanistically; and an oracle-normalized retention sweep converts the estimates into a decision-adequacy verdict. Each instrument exists to remove one named confound or answer one named sub-question, and all ground truth is mechanical throughout — execution outcomes and token billing, no judge models and no human labels.

The **cross-backbone frozen-library replay** harness replays identical streams under each backbone in paired bare and full-library arms, in both free-use and forced-use invocation regimes. The **token-matched placebo library** isolates what context load and retrieval mechanics contribute on their own. The **per-skill utility ledger** estimates each eligible skill's marginal utility by masking it on its own activation set, probes the additivity assumption that licenses the attribution, and joins the result to acquisition costs to yield amortized net value. The **mechanism decomposition** classifies each depreciated skill as obsolescence, interference, or cost drag from paired trace signatures. The **oracle-normalized retention sweep** ranks skills by estimated retained value, sweeps the retention threshold, and scores the result against an oracle frontier at a pre-registered operating point, with the corner policies — never-retire, full-relearn, no-library — reported as fixed reference points of the decision space.

## Methodology

### Cross-Backbone Frozen-Library Replay

**Challenge.** Any cross-backbone comparison is dominated by the capability difference between the models, and any with/without-library comparison under one backbone is entangled with the model's changed willingness to invoke skills.

**Insight.** Backbone generation is a clean treatment only if everything the model touches except the backbone is frozen, and capability cancels only if every verdict is a *same-backbone* paired contrast: the upgraded model with the library against the same upgraded model bare, on the same tasks and seeds.

**Method.** For each stream, a library is acquired once under M_0 by a fixed Voyager/Agent-Workflow-Memory-style acquisition loop (design target: 40–80 skills per stream), then frozen with per-skill acquisition ledgers. The evaluation stream is replayed under each backbone in paired arms — bare and full-library — with harness, retriever, prompts, and turn budgets byte-identical across arms except library content, under two invocation regimes: free-use (the model chooses) and forced-use (a retrieved skill must be attempted), whose difference isolates invocation propensity from content. The library-level verdict for an upgrade pair is the paired success and cost-per-solved-task contrast under M_1, with the same contrast under M_0 establishing the acquisition-time asset baseline.

### Token-Matched Placebo Library

**Challenge.** A library is also thousands of prompt tokens and a retrieval apparatus; a harm measured against the bare arm could be caused by load and mechanics rather than by what the skills say.

**Insight.** The placebo is the measurement's null instrument: it reproduces the load and mechanics while removing the content, so whatever harm it reproduces is attributable to load, and content-attributed harm is what remains after subtracting it — the causal reading of the library-level verdict is licensed jointly with the placebo result, not by the with/without contrast alone.

**Method.** The placebo library matches the real library in skill count, token-length distribution, and retrieval-key statistics, but its bodies are syntactically valid, executable, task-irrelevant procedures drawn from a disjoint domain. It is replayed under the identical harness and regimes. Pre-registered reading: a placebo reproducing less than half of the real library's measured harm supports the content attribution; a placebo reproducing half or more refutes it and reattributes the phenomenon to context mechanics.

### Per-Skill Utility Ledger

**Challenge.** Skills act in combinations under retrieval gating; the factorial experiment over all 2^K sublibraries that would attribute value per skill is infeasible, yet the upgrade decision is per-skill.

**Insight.** Masking one skill at a time on its own activation set collapses the factorial into K bounded paired contrasts — but this identifies a per-skill quantity only if cross-skill interactions are second-order, so the licensing assumption must be probed and the reporting granularity must degrade honestly if it fails.

**Method.** For each skill clearing an activation floor (design target: ≥20 retrievals on the stream), a sampled subset of its activation tasks (design target: 30 tasks × 3 seeds) is replayed with the library minus that skill — the retriever re-run without it, so a substitute may fire, which is the deployment-relevant counterfactual — paired against full-library runs on the same tasks and seeds. This yields u_k and γ_k per backbone, and joining the acquisition ledger yields amortized net value (cumulative reuse benefit minus acquisition cost) per skill per backbone. The additivity license is checked by a pairwise-interaction probe: pair-masking over the top-frequency skill pairs, with the interaction share of total attributed value bounded at 15%; if the bound is exceeded, utilities are reported at retrieval-cluster granularity instead of single-skill granularity, and all downstream per-skill claims are re-evaluated at that granularity — a pre-committed downgrade, not a post hoc choice.

### Mechanism Decomposition

**Challenge.** Obsolescence, interference, and cost drag produce identical library-level deltas but demand different upgrade actions, and contract-style functional checks are blind to two of the three — an obsolete or interfering skill can be perfectly contract-conformant.

**Insight.** The three mechanisms leave distinct, mechanically-checkable signatures in per-task *paired* traces — what the bare run did on exactly the tasks where the skill fired — so the decomposition needs no judge model and no human labels, only the same paired replays the ledger already buys.

**Method.** Each floor-eligible skill with negative or near-zero retained utility is classified from its paired traces: *obsolescence* — the bare arm succeeds on the skill's activation set at a rate at least matching the with-skill arm, and the skill's success delta is within the equivalence band (|u_k(M_1)| ≤ 0.02); *interference* — with-skill failures occur on tasks the bare arm solves, with the skill invoked in the failing trace; *cost drag* — success delta within the equivalence band with a positive token delta. Library-level net harm is then decomposed into additive shares attributable to each class by aggregating the classified skills' paired contributions.

### Oracle-Normalized Retention Sweep

**Challenge.** A measurement of per-skill value is only worth its token cost if it improves the recurring upgrade decision — but "our policy beats the alternatives" is a method-paper claim this measurement study neither makes nor needs.

**Insight.** Oracle-normalization converts the decision question into a property of the measurement: how much of the cost–success frontier available to an oracle that knows each skill's true post-upgrade value is recovered by a rule that reads only our estimates — evaluated at one pre-registered operating point, so the swept frontier cannot be mined for a favorable comparison after the fact.

**Method.** Skills are ranked by estimated retained value; sweeping the retention threshold traces a (total token cost, success rate) frontier, charging full re-acquisition cost for refreshed skills and metering all measurement cost. The oracle ranks by ground-truth value computed on a held-out task split disjoint from the estimation split. The pre-registered operating point is matched success: the cost comparison is taken where each policy's success rate is within ±1 percentage point of the never-retire corner's success rate. The corner policies — never-retire (full old library), full-relearn (fresh library acquired under M_1, acquisition charged), and no-library — are reported as fixed reference points of the decision space; full frontier curves are reported descriptively only.

## Experiments

### Experimental Setup

**Task streams.** MBPP+ (execution-verified function synthesis; the EvalPlus-hardened verifier set over the MBPP tasks) — the pilot substrate: cheapest per episode, densest skill activations, and closed-form mechanical verification. A SWE-bench Lite-style subset (repository-level issue resolution) — stresses whether depreciation behaves differently for heavyweight, workflow-like skills whose acquisition cost is largest. ALFWorld (embodied household tasks in text) — chosen for two hypothesis-linked reasons: it tests the phenomenon's generality beyond code, and its short, repetitive episode structure yields the highest per-skill activation counts of the three streams, making it the best-powered regime for the per-skill estimator and its reliability check. Acquisition, evaluation, and held-out (RQ7/RQ8) task partitions are disjoint by construction, with the partition assignment hashed and frozen before any run, so the acquisition-time asset baseline cannot be inflated by memorized acquisition tasks. Because the canonical subsets cannot fund disjoint partitions at the stated sizes — SWE-bench Lite has exactly 300 instances and ALFWorld's unseen evaluation split has 134 games — the partitions draw from the benchmarks' larger pools (the full SWE-bench instance set; ALFWorld's full game set), with the sourcing recorded per partition.

**Backbones.** Design target: at least two vendor families × two consecutive public generations each, plus at least one two-generation pair within one family (three upgrade pairs minimum; the topic card's examples — a GPT-4-class to GPT-5-class step, a sonnet-4 to opus-5 step — fix the pattern, with concrete generations pinned at run time). Backbone generation is the treatment; the same-backbone bare arm absorbs capability differences by construction.

**Reference arms** (this is a measurement study; no research question is framed as "our procedure beats baseline X"). Bare backbone — the paired control every verdict is computed against. Never-retire and full-relearn — the corner policies of the decision space, reported as fixed reference points. Token-matched placebo library — the null instrument. Oracle per-skill selection — the upper reference for decision adequacy.

**Sample-size and power targets (authored design parameters).** Library-level arms: 300 tasks × 5 seeds = 1,500 paired episodes per (stream × upgrade-pair × arm), sized to detect a 3-percentage-point paired success contrast at approximately 0.8 power under an assumed 12–15% discordance rate; if the pilot's observed discordance implies less than 0.8 power at the 2-point effect floor, a pre-committed enlargement to 8 seeds applies before any null is claimed, and cells still underpowered after enlargement are pre-declared INCONCLUSIVE — never reported as null and never dropped silently. Per-skill ledger: activation floor 20, with 30 sampled activation tasks × 3 seeds per eligible skill; skills below the floor are reported as unmeasured at skill granularity (they remain inside every library-level quantity). All success tests are paired (McNemar-style) at α = 0.05 with Holm correction across upgrade pairs; cost outcomes use paired bootstrap intervals. Because the 1,500 paired episodes are 300 tasks × 5 seeds, seed-level replications are clustered within tasks and the pairs are not independent; inference is therefore pre-registered as cluster-robust — McNemar-style statistics computed on task-level aggregates with a cluster bootstrap over tasks — the 0.8 power target is re-evaluated against the pilot's observed within-task correlation (the nominal-N calculation is optimistic whenever that correlation is positive), and the enlargement rule applies to the effective sample size, not the nominal episode count.

**Measurement budget (design arithmetic, not results).** The library-level design implies roughly five arm-regime combinations (bare, full-library free-use, full-library forced-use, placebo, and corner-policy reference runs) × 1,500 episodes under M_1 per (stream × upgrade-pair) cell, plus the M_0 baseline arms; the per-skill ledger adds up to 80 skills × 30 tasks × 3 seeds × 2 backbones, plus the pairwise-interaction probe. That totals ≈2–3 × 10^4 episodes per cell and low-10^5 episodes for the full three-stream × three-pair grid — dominated in token cost by the SWE-bench stream, whose per-episode footprint is orders of magnitude above MBPP+'s. This envelope is a pre-registered design parameter: any budget reduction found necessary at pilot time must itself be pre-registered with its power consequence computed (extending the pilot-gate rule above) — cells are shrunk explicitly or declared INCONCLUSIVE, never silently.

**Metrics.** Paired library-level success and cost-per-solved-task contrasts; per-skill marginal utility, cost companion, retention ratio, and amortized net value; mechanism-class shares of net harm; split-half rank agreement of per-skill estimates; oracle-frontier recovery fraction at the matched-success operating point.

**Research questions:**
1. RQ1 — Does the frozen library flip from asset to liability under an upgraded backbone?
2. RQ2 — Does per-skill value retention decline with generation distance?
3. RQ3 — Is the measured harm content-driven rather than context-load-driven?
4. RQ4 — Is per-skill value change heterogeneous enough to make selective retirement non-trivial?
5. RQ5 — Are per-skill retention estimates reliable across disjoint task splits?
6. RQ6 — What share of the harm is active interference rather than obsolescence or cost drag?
7. RQ7 — Do the measured estimates recover most of the oracle's decision frontier?
8. RQ8 — Does functional portability predict economic value retention?

#### RQ1: Does the frozen library flip from asset to liability under an upgraded backbone?

**Setup.** For every (stream × upgrade-pair) cell, the paired contrast between the full-library and bare arms under M_1, in the free-use regime, with the same contrast under M_0 confirming the library was an asset at acquisition time (a library that never helped its own backbone cannot depreciate; such cells are excluded from the flip test and reported).

**Expected outcome.** In at least one tested cell, the frozen library reduces the upgraded backbone's paired success rate by ≥2 percentage points or raises its token cost per solved task by ≥10%, Holm-corrected p < 0.05 — the asset-to-liability flip exists.

**Falsification condition.** Refuted if no cell shows the flip at the floors — in which case the pre-committed reading is reported at full prominence: within the tested envelope, depreciation is bounded by pure obsolescence and cost accounting, and porting a stale library is certified safe (a robustness result the field currently cannot state), with the retire decision reduced to cost-only pruning.

**Hypothesis (plain language).** Weak-backbone compensations can actively harm a stronger backbone, not merely become useless.

**Metrics.** Per-cell paired success delta with CI; cost-per-solved-task ratio; count of flip cells.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Does per-skill value retention decline with generation distance?

**Setup.** For the library acquired under M_0, compare the distribution of per-skill retention between the one-generation pair (M_0 → M_1) and the two-generation pair (M_0 → M_2) within the same vendor family, per stream; paired Wilcoxon over floor-eligible skills present in both comparisons.

**Expected outcome.** Median retention under the two-generation upgrade is lower than under the one-generation upgrade in the majority of tested streams.

**Falsification condition.** Refuted if median retention is flat or higher at the larger generation distance in most streams — which would indicate depreciation is a one-time porting shock rather than a cumulative generational process, changing the refresh-cadence implication.

**Hypothesis (plain language).** Depreciation is dose-responsive in generation distance, not a fixed porting cost.

**Metrics.** Per-stream median retention by generation distance; paired Wilcoxon p-values.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Is the measured harm content-driven rather than context-load-driven?

**Setup.** In every cell where RQ1's flip is observed, the placebo-library arm's paired deltas versus bare are compared against the real library's deltas.

**Expected outcome.** The placebo reproduces less than 50% of the real library's harm (both success and cost deltas) in every flip cell.

**Falsification condition.** Refuted if the placebo reproduces half or more of the harm in any flip cell — the pre-committed downgrade then reattributes that cell's phenomenon to context load and retrieval mechanics, and the content-specific claims are withdrawn for that cell while the practical porting warning stands.

**Hypothesis (plain language).** The harm comes from what stale skills say, not from how much space they occupy.

**Metrics.** Placebo-to-real harm ratio per flip cell.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Is per-skill value change heterogeneous enough to make selective retirement non-trivial?

**Setup.** The per-skill ledger's retention distribution over floor-eligible skills, per (stream × upgrade-pair) cell; granularity downgraded to retrieval clusters if the additivity probe's 15% bound fails (pre-committed).

**Expected outcome.** In the majority of cells, at least 20% of floor-eligible skills retain ≥50% of acquisition-time marginal utility while at least another 20% fall to zero or negative retained utility.

**Falsification condition.** Refuted if retention is near-homogeneous (either tail below 20%) in most cells — reported at full prominence as a finding that per-skill accounting is unnecessary: a single library-level decision then suffices at upgrade time, and the measurement's decision yield collapses to the RQ1 verdict.

**Hypothesis (plain language).** Upgrades split libraries into keepers and liabilities; neither corner policy can be right for both.

**Metrics.** Retention-distribution tail masses per cell; interaction share from the additivity probe.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Are per-skill retention estimates reliable across disjoint task splits?

**Setup.** Each eligible skill's activation-task sample is split into disjoint halves; retention estimated independently on each; rank agreement computed over floor-eligible skills per cell.

**Expected outcome.** Split-half Spearman ρ ≥ 0.6 in the majority of cells.

**Falsification condition.** Refuted if rank agreement falls below 0.6 in most cells — the estimates are then sampling artifacts at the bought budget, no downstream ranking (RQ7) is licensed, and the pre-committed remedy is raising the per-skill budget or coarsening to cluster granularity before any decision claim is made.

**Hypothesis (plain language).** A skill's post-upgrade value is a stable property of the (skill, backbone) pair, not replay noise.

**Metrics.** Per-cell split-half Spearman ρ; fraction of cells clearing 0.6.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: What share of the harm is active interference rather than obsolescence or cost drag?

**Setup.** Mechanism classification of every floor-eligible depreciated skill from paired trace signatures, in every flip cell; library-level net harm decomposed into class shares.

**Expected outcome.** Interference accounts for at least 25% of library-level net harm in at least one flip cell.

**Falsification condition.** Refuted if interference stays below 25% everywhere the flip occurs — depreciation would then be economically real but mechanically benign (obsolescence plus drag), and the urgent-retirement implication is withdrawn in favor of cost-only pruning.

**Hypothesis (plain language).** Part of a stale library does not just ride along uselessly — it actively misleads the stronger model.

**Metrics.** Class shares of net harm per flip cell; per-class skill counts.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Do the measured estimates recover most of the oracle's decision frontier?

**Setup.** Retention-threshold sweep ranked by estimated retained value; oracle ranked by ground-truth value on a held-out task split disjoint from the estimation split; evaluation only at the pre-registered matched-success operating point (each policy's success within ±1 percentage point of the never-retire corner); corner policies reported as reference points; Holm correction across upgrade pairs.

**Expected outcome.** Thresholding on the estimates recovers at least 80% of the oracle frontier's cost reduction relative to the never-retire corner, at the matched-success operating point, in the majority of cells.

**Falsification condition.** Refuted if recovery falls below 80% in most cells — the measurement is then reliable (RQ5) but decision-insufficient at the bought budget, and the pre-committed reading names the gap's source (estimate noise near the decision boundary, or harm concentrated in below-floor skills) rather than claiming adequacy.

**Hypothesis (plain language).** Reading only the measured per-skill values gets an operator most of the way to the best achievable upgrade decision.

**Metrics.** Oracle-recovery fraction at the operating point per cell; corner-policy reference values; descriptive frontier curves.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ8: Does functional portability predict economic value retention?

**Setup.** Functional portability is measured independently of the task stream: a skill ports functionally iff its standalone contract validation — execution and contract-conformant output on held-out validation inputs disjoint from the evaluation tasks — passes under M_1. Cross-tabulate {ports cleanly, fails} × {retains value, loses value} over floor-eligible skills, per cell.

**Expected outcome.** Among skills that port with preserved functional correctness, at least 30% nonetheless fall to zero or negative retained marginal utility under the upgraded backbone.

**Falsification condition.** Refuted if fewer than 30% of cleanly-porting skills lose their value — functional portability would then be an adequate cheap proxy for retention, the per-skill economic apparatus would be over-engineered for the decision, and the snapshot-transfer-accuracy convention of prior cross-model work would be vindicated as a retention signal.

**Hypothesis (plain language).** A skill can still run perfectly and be worth nothing — value lives in what the backbone cannot do without it, which is exactly what an upgrade changes.

**Metrics.** Portability-by-retention contingency tables; fraction of cleanly-porting skills with non-positive retained utility.

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, two natural extensions are explicitly out of scope here: cross-family porting (a library acquired under one vendor's model replayed under another vendor's — a different treatment than generational upgrade, confounding architecture with generation), and online retirement policies that interleave measurement with continued acquisition (which breaks the frozen-library identification this design depends on).

### Threats to Validity

**Construct validity.** The per-skill value construct is licensed by the leave-one-out contrast only under approximate additivity of skill effects; this assumption has an explicit detection (the pairwise-interaction probe with its 15% bound) and a pre-committed downgrade (cluster-granularity reporting) rather than silent reliance. The retention ratio is undefined near zero acquisition-time utility, hence the acquisition-value floor; consequently, skills below the activation or value floors are unmeasured at skill granularity, and any harm concentrated there is visible only in library-level quantities — a stated boundary of the estimand, tested indirectly by RQ7's adequacy verdict. Functional portability (RQ8) is deliberately measured on validation inputs disjoint from the task stream so its dissociation from value retention cannot be a bookkeeping artifact.

**Internal validity.** The causal reading of every library-level verdict rests on three controls: the same-backbone paired contrast (cancels model capability), the token-matched placebo (isolates context load and retrieval mechanics; checked by construction against the real library's token-length and key distributions), and the forced-use/free-use pair (separates content effects from invocation propensity). Prompt and harness equality across arms is enforced by byte-identical templates with an automated per-episode token-accounting assertion; a violation downgrades the causal reading of the affected cell rather than being absorbed. Acquisition randomness is controlled by freezing one library per (stream, M_0) and reporting its composition; the library is the measured object, not a sampled population of libraries — a scope statement, not a hidden generalization.

**External validity.** Findings are scoped to frozen libraries acquired by one fixed acquisition loop, replayed on three sandboxable, mechanically-verified task streams, across the tested vendor families and generation pairs; they are not asserted for continually-learning libraries, for cross-vendor porting, for streams without mechanical verifiers, or for backbone pairs outside the tested envelope. The generational natural experiment is public — every claim is re-runnable by anyone at the next release cycle, which is the study's replication path.

**Conclusion validity.** Success contrasts are paired with pre-registered floors and Holm correction across upgrade pairs; because seed-level replications are clustered within tasks, all paired inference is cluster-robust (task-level aggregates, cluster bootstrap over tasks) and power is assessed on effective — not nominal — sample sizes; power targets and the enlargement rule are stated in the setup, and cells underpowered after enlargement are pre-declared INCONCLUSIVE, never null. Estimate-level claims are gated by the split-half reliability check (RQ5) before any ranking claim (RQ7) is licensed, and the decision-adequacy verdict is evaluated only at the pre-registered matched-success operating point, eliminating post hoc operating-point selection from a swept frontier.

## Related Work

The closest prior work is the environment-axis staleness line — Library Drift above all — and the cross-model transfer study AFTER, and the delta is worth stating plainly before surveying the landscape: Library Drift already measures skill-library value decaying to and below the no-library baseline, but its treatment variable is ungoverned accumulation — unbounded skill growth without outcome-driven lifecycle management — with the backbone held fixed; AFTER already moves skills across models, but reports a snapshot functional-transfer accuracy with no cost accounting and no retention decision. Neither — nor any work we know of — replays a frozen library across real backbone generations and estimates what each skill is still worth.

**Skill-library agents and their evaluation convention.** Voyager established the acquisition loop this study reuses — solve, verify, distill, retrieve — and demonstrated compounding returns from an ever-growing library; Agent Workflow Memory induces reusable workflows from agent experience with the same economic logic. Both evaluate the library only under the backbone that acquired it, so the monotone-asset assumption is untested on the model axis by construction. The lifelong-learning line now extends the pattern: GSE evolves a coding-agent skill bank over an explicit Skill Relation Graph with cluster-based consolidation and replay-driven verification — field evidence that cross-skill interactions are first-order in practice, which is exactly the threat our additivity probe measures rather than assumes away — and ASPIRE compounds robot-programming experience into a skill library claimed to persist across tasks, settings, and embodiments; neither attaches an economic account of what any skill is worth under a newer backbone. The agent-memory taxonomy of CoALA situates such libraries as procedural memory, distinct from the declarative memory whose staleness is now separately studied — Memora's staleness-aware metric penalizes reliance on invalidated *facts* under world change, an axis deliberately different from the procedural-skill-under-model-change axis measured here.

**Staleness diagnostics on the accumulation and environment axes.** Library Drift shows unbounded skill accumulation — growth without outcome-driven lifecycle management — dragging a coding agent below its no-library baseline, with human curation recovering the gap: the clearest evidence that library value is not monotone, on an axis this study holds fixed. Its trace diagnostics also include per-skill contribution scores with attribution verdicts — the nearest prior neighbor to our utility ledger — computed as within-run heuristics under a single backbone; the ledger differs in being a causal masked contrast on each skill's own activation set, with a cost companion, a placebo null instrument, an explicitly probed additivity license, and cross-backbone differencing. The environment axis proper belongs to the contract-violation line (SkillGuard/DriftBench), which benchmarks functional skill degradation across 880 pairs as packages, services, and APIs evolve, and detects breakage proactively; its limitation for the upgrade decision is that contract conformance is neither necessary nor sufficient for value: an obsolete or interfering skill can pass every contract check, which is exactly the dissociation RQ8 tests. These works motivate rather than pre-empt the backbone axis: their own treatment variables never include the model generation.

**Maintenance, governance, and skill economics.** SkillOps operationalizes library maintenance as an ops pipeline, but its triggers are environment events — dependency bumps, API changes — not backbone releases, and although its health monitoring includes a utility dimension, that signal is not backbone-conditioned: nothing tells it what a skill is worth after a backbone swap, so it cannot rank retirement candidates at upgrade time, which is precisely the quantity this measurement supplies. SkillsVote attributes task outcomes to skill-guided execution, exploration, and environment signals and gates library updates on that evidence, and evaluates offline transfer of frozen libraries — attribution as a curation signal — but the signal is not a cost-amortized economic estimand, and no backbone upgrade triggers re-evaluation. Token Economics is a survey conceptualizing tokens as economic primitives of agent operation — production factors, exchange media, units of account — supplying the vocabulary this study borrows; it reports no per-skill payback or depreciation curve, and the step from framing to measured estimand is the gap it leaves open and this paper closes.

**Cross-model skill transfer.** AFTER evaluates procedural memory in an explicit cross-model generalization setting and reports 73.1% cross-model transfer accuracy for ported skills — the only prior measurement on the backbone axis — and it additionally observes, qualitatively, that some skills generalize broadly across tasks and models while others lose effectiveness under transfer: the closest existing statement of RQ4's heterogeneity hypothesis. But transfer accuracy is a functional-portability number — it says a skill still runs, not that the new backbone still needs it — carrying no acquisition-cost amortization, no marginal-benefit accounting, and no retention decision; and the heterogeneity observation is unquantified and unpriced, which is what RQ4's pre-registered tail test adds. Our framing-tier question (RQ8) takes this seriously as the strongest rival reading of the literature — if portability predicted retention, snapshot accuracy would suffice for the upgrade decision — and pre-registers the dissociation test rather than asserting it.

**Task substrates.** MBPP with the EvalPlus-hardened verifiers, SWE-bench, and ALFWorld supply the mechanically-verified streams; all three are established benchmarks whose verifiers (test execution, issue resolution checks, goal-state checks) provide the judge-free ground truth the entire measurement rests on.

## Conclusion

This work reframes a design assumption — that an agent's accumulated skills are a monotone asset — as a measurable compatibility question between a library and the backbone generations that succeed the one that built it. The central methodological wager is that the port/prune/relearn decision becomes tractable only at per-skill resolution with mechanism labels attached: library-level toggles cannot separate keepers from liabilities, and functional checks cannot see economic death. Whichever way the pre-registered tests resolve, the outcome is decision-relevant: a confirmed asset-to-liability flip with a substantial interference share would establish that skill libraries need versioned retirement the way code needs deprecation; a null flip within the tested envelope would certify porting as safe and reduce upgrades to cost-only pruning — a license the field currently lacks either way. Three limitations bound the claim from the outset and point forward: the measurement covers one acquisition loop and three sandboxable streams, leaving continually-learning libraries and unverifiable domains open; skills below the activation floor remain unmeasured at skill granularity, so adequacy for decisions about them is inferred only through the oracle-recovery test; and the additivity license, though probed and equipped with a pre-committed downgrade, marks the boundary where per-skill accounting itself stops being the right abstraction — finding the right granularity for skill-library economics when skills strongly compose is the natural next methodological target.

## References

> Mirror of `discussion/refs.bib` (the `.tex` build uses `\citep`/`\citet` keys resolving to that file). Citation policy for this topic (recorded in `pipeline.md`): the 2026 works below were first recorded from this repo's verified scan records, then re-verified against the live arXiv API — metadata repair 2026-08-15; content re-check plus two verified additions (GSE, ASPIRE) 2026-08-21. Works with no recorded name (arXiv:2607.10113, 2606.11435, 2606.09421) remain deliberately uncited.

- X. Zhang et al. Library Drift: Diagnosing and Fixing a Silent Failure Mode in Self-Evolving LLM Skill Libraries. arXiv:2605.19576, 2026.
- L. Fan et al. Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries. arXiv:2605.10990, 2026.
- H. Pu et al. SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems. arXiv:2605.13716, 2026.
- Y. Chen et al. Token Economics for LLM Agents: A Dual-View Study from Computing and Economics. arXiv:2605.09104, 2026.
- J. Belikova et al. Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation. arXiv:2606.23127, 2026.
- H. Liu et al. SkillsVote: Lifecycle Governance of Agent Skills from Collection, Recommendation to Evolution. arXiv:2605.18401, 2026.
- M. Nayem Uddin et al. From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents. arXiv:2604.20006, 2026.
- Yang, C., Tian, J., Wang, Z., Liu, X., Ye, M., Chen, J. Learning Globally Reusable Skills for Coding Agents. arXiv:2608.06153, 2026.
- Lu, R., Wu, Y., Kou, E., Fu, L., Xiao, W., Mandlekar, A., Xu, Y., Shi, G., Goldberg, K., Chen, A., Chowdhury, M., Zhu, Y., Fan, L., Wang, G. ASPIRE: Agentic Skills Discovery for Robotics. arXiv:2607.00272, 2026.
- Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., Anandkumar, A. Voyager: An Open-Ended Embodied Agent with Large Language Models. arXiv:2305.16291, 2023.
- Wang, Z. Z., Mao, J., Fried, D., Neubig, G. Agent Workflow Memory. arXiv:2409.07429, 2024.
- Sumers, T., Yao, S., Narasimhan, K., Griffiths, T. L. Cognitive Architectures for Language Agents. TMLR, 2024. (arXiv:2309.02427)
- Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., Sutton, C. Program Synthesis with Large Language Models. arXiv:2108.07732, 2021.
- Liu, J., Xia, C. S., Wang, Y., Zhang, L. Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation. NeurIPS, 2023. (arXiv:2305.01210)
- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR, 2024. (arXiv:2310.06770)
- Shridhar, M., Yuan, X., Côté, M.-A., Bisk, Y., Trischler, A., Hausknecht, M. ALFWorld: Aligning Text and Embodied Environments for Interactive Learning. ICLR, 2021. (arXiv:2010.03768)

---

## Pre-handoff checklist

- **Organization/navigation** — narrative flows problem → formal definition → apparatus → experiments → related work with no forward references to undefined terms; each Introduction paragraph opens with its single message (verified by the Stage-5 writing review's reverse-outline re-check).
- **Terminology discipline** — "marginal utility," "retention ratio," "activation set," "flip cell," "corner policies," "matched-success operating point," and the three mechanism names are each defined at first use and used consistently; no internal stage IDs (`sp_*`, `m_*`, `rq_*` beyond the RQ1–RQ8 section labels, `lim_*`, H-numbers) leak into prose — checked directly against `discussion_trace.md`.
- **Notation** — (L, σ_k, M_0, M_1, T, T_k, y, c, u_k, γ_k, Δu_k, r_k) defined once in Problem Definition and reused consistently; no worked numeric example is included since no numbers exist yet (fabricating one would violate the no-results rule).
- **RQ framing matches outcomes** — all 8 RQs are graded/quantitative (deltas, shares, rank correlations, recovery fractions), each answered in its own subsection with an explicit falsifiable expected outcome and an explicit falsification condition.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]`; only explicit `[placeholder — fill in after experiments are run]` markers in Result slots, per the convention that this is a pre-registered spec, not a report.
- **Artifact plan** — the replay harness, acquisition-ledgered libraries, placebo generator, and per-skill ledgers are the natural release artifacts; not yet built, so not claimed as available.

## Hand-off

This is a Markdown draft, not a finished paper — experiments have not run. Natural next steps: execute from `experiment_design.md` (the standalone protocol; the two documents are synchronized), then splice results into the placeholders; or return to the discussion pipeline if piloting breaks an assumption (the most likely candidates, in order: the additivity probe exceeding its 15% bound, the acquisition-time asset precondition failing on a stream, and the discordance rate implying an underpowered flip test at the 2-point floor).
