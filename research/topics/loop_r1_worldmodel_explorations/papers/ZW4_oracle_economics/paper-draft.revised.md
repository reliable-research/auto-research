> **✅ CURRENT MANUSCRIPT.** Revised from `paper-draft.md`; see the revision log at the end
> and `../MAJORS.md` for every major and where it was fixed.

# Cost-Aware Phase Diagrams for Proof and Execution Oracles in Code Reinforcement Learning

## Abstract

Proof supervision is increasingly used to improve code reinforcement learning because formal arguments can cover many executions, yet this efficiency claim matters only if verifier costs are included in the training budget. Existing studies report capability or rollout reductions without jointly accounting for solver CPU time, GPU use, heavy-tailed obligation latency, and timeouts; consequently, they cannot determine when proof-based feedback is cheaper than test or execution feedback. We propose a preregistered, controlled comparison of test-outcome, execution-process, binary-proof, structured-proof, and hybrid oracles across program families, specification sources and quality tiers, and candidate-generation budgets. A shared evaluation contract holds generation and verification conditions fixed, while an append-only event ledger attributes per-call resources and preserves censored latency and timeout behavior. Cross-fitted attainable-capability envelopes then identify oracle winners and crossover points under matched model compute and price-parameterized end-to-end cost, with bootstrap uncertainty and GPU-to-CPU price sensitivity. The study is staged so that the measurement instrument is validated before any factorial is attempted: a first phase builds and audits the ledger against synthetic heavy-tailed latencies and existing training runs without launching new ones, a gate requires accurate per-call attribution and a censoring-aware latency model that beats a mean-latency baseline, and only then are phase diagrams computed over measured cells, with unmeasured cells reported as unobserved rather than interpolated. Evaluation uses the Controlled Multi-Oracle Factorial Benchmark, Blinded Specification-Defect Validation Set, and Metered Oracle Execution and Stall Traces. Source-only quality labels, naive job-wall-time accounting, and a mean-latency stall model serve as measurement baselines. Capability is measured by held-out test-suite pass rate under a fixed sampling protocol.

## Introduction

Reinforcement learning for code generation increasingly relies on executable feedback to distinguish functionally correct programs from plausible but defective ones. Such feedback ranges from test outcomes and intermediate execution traces to binary verification decisions, structured proof diagnostics, and hybrid combinations. Proof supervision is especially attractive because a proof can cover broad classes of executions without repeatedly sampling concrete inputs. This apparent reduction in oracle calls, however, does not establish lower training cost: difficult proof obligations can consume substantial CPU time, exhibit highly variable latency, or reach fixed time limits. The relative efficiency of supervision signals may therefore depend on program structure, specification quality, candidate-generation budget, and the prices of GPU and CPU resources.

Two observations make the uncertainty decision-relevant rather than merely acknowledged. First, the field's most-cited compute anchor for verifier-driven RL does not report the quantity it is used for: Re:Form gives GPU counts and wall-clock in separate columns for its subset-reward configuration — 16 A800-SXM4-80G GPUs for approximately 11 hours at 0.5B, and 16 GPUs for approximately 25 hours at 1.5B — and states no GPU-hours figure anywhere. The widely-quoted ~176 and ~400 GPU-hours are arithmetic performed on those columns by later readers, ours included, and the accompanying 40-epoch detail attaches only to the 3B run. Second, the solver-side cost is *unbounded within an order of magnitude by anything published*. The nearest published measurement — a one-off per-training-step wall-clock table for a cached Lean verifier inside an RLVR paper (Chen et al. [[2026](https://arxiv.org/abs/2604.25419)]) — covers a single oracle with no latency distributions and no capability-per-cost normalization, so no systematic, cost-normalized capability comparison across oracle types exists, and nothing bounds the Dafny arm here: a 200,000-candidate structured-verification-condition arm instrumented over five obligation categories implies roughly one million SMT or assertion-batch evaluations, which at a mean batch time of 0.2 s is about 56 CPU-hours and at 2.0 s is about 556. Both are plausible for Dafny, whose own documentation warns that individual assertions can become unexpectedly hard, time out, or vary widely in solver cost. A tenfold swing in the denominator of an efficiency claim, arising from a parameter nobody reports, is what this study exists to eliminate.

Yet the central efficiency claim has not been measured under audited end-to-end budgets. Existing work predominantly reports capability or sample efficiency while excluding some cost of producing the reward signal. Execution-based approaches include CodeRL (Hung Le et al.. CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning), RLEF (Jonas Gehring et al.. RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING), and ExecVerify (Lingxiao Tang et al.. ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning). Process-oriented methods such as StepCodeReasoner (Hao Wang et al.. StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning) and ORPS (Zhuohao Yu et al.. Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation) enrich runtime feedback, but do not compare test, execution-process, proof, and hybrid oracles under matched model-compute and end-to-end-cost constraints.

Formal-verification research demonstrates that machine-checkable feedback can guide generation, refinement, and reinforcement learning. Representative systems include AlphaVerus (Pranjal Aggarwal et al.. AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement), Re:Form (Chuanhao Yan et al.. Re:Form — Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny), LORIS (Tianchi Li et al.. Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors), and FVEL (Xiaohan Lin et al.. FVEL: Interactive Formal Verification Environment with Large Language Models via Theorem Proving). These systems establish the utility of verifier feedback but treat verification principally as a correctness mechanism rather than a priced oracle. Consequently, they do not reveal whether fewer proof-based evaluations compensate for solver CPU consumption, long-tailed latency, and timeouts. Answering this question requires a harness that normalizes heterogeneous oracle calls without changing sampling conditions or verifier effort across arms; call-level accounting that separates consumed resources from wall-clock stalls while retaining censored timeouts; and uncertainty-aware crossover estimation over a high-dimensional grid of program families, specification conditions, budgets, and hardware-price ratios.

The proposed study makes this comparison tractable by treating every supervision mechanism as an adapter to a shared oracle-evaluation contract. Preregistered blocks will hold checkpoints, candidate counts, decoding limits, update schedules, seeds, solver configurations, and resource caps constant, leaving reward information and its intrinsic evaluation cost as the systematic differences between arms. An append-only event ledger will record process-tree CPU time, reserved GPU time, wall latency, obligation identity, retries, caching, parallelism, termination causes, and timeout caps for every call. These observations will support a symbolic end-to-end cost model, \(C=H_{\mathrm{gpu}}p_{\mathrm{gpu}}+H_{\mathrm{cpu}}p_{\mathrm{cpu}}\), without imputing unobserved completion times beyond a timeout. Cross-fitted attainable-capability envelopes will then identify oracle winners and crossover regions under equal model compute and equal end-to-end cost, while bootstrap uncertainty will distinguish supported winners from ambiguous cells.

The evaluation will use the Controlled Multi-Oracle Factorial Benchmark, the Blinded Specification-Defect Validation Set, and Metered Oracle Execution and Stall Traces. It will span straight-line code, linear loops, nonlinear arithmetic, arrays and aliasing, and recursion; human-authored and model-generated specifications of preregistered quality; and candidate-generation budgets of approximately 50k, 200k, and 500k per arm. Source-only quality labels, naive job-wall-time accounting, and a mean-latency stall model will serve as measurement baselines. The resulting analyses will compare oracle capability under both budget definitions, report complete latency and timeout distributions, locate supported crossover regions, and assess whether equal-cost orderings persist when the GPU-to-CPU price ratio changes threefold.

## Contributions

- We introduce a controlled multi-oracle benchmark that isolates supervision choice by fixing generation, verification, and resource conditions across test, execution-process, binary-proof, structured-proof, and hybrid oracles.
- We develop per-obligation event-sourced accounting that attributes GPU and CPU consumption while preserving latency tails, timeout mass, concurrency, and censoring.
- We propose uncertainty-aware attainable-capability envelopes for constructing equal-model-compute and equal-end-to-end-cost phase diagrams and estimating oracle crossovers.
- We evaluate the robustness of oracle orderings across program families, specification conditions, candidate budgets, and GPU-to-CPU price ratios.

## Problem Definition

## Formal Problem Definition

Let \(\mathcal{O}=\{o_{\mathrm{test}},o_{\mathrm{exec}},o_{\mathrm{bin}},o_{\mathrm{{struct}}},o_{\mathrm{hybrid}}\}\) denote the test-outcome, execution-process, binary-proof, structured-proof, and hybrid oracles. Let \(\mathcal{F}\) contain the program families—straight-line code, linear loops, nonlinear arithmetic, arrays and aliasing, and recursion—and let \(\mathcal{S}\) contain human-authored fixed and model-generated specification conditions. Candidate-generation budgets belong to \(\mathcal{N}\), comprising the planned scales of approximately \(50{,}000\), \(200{,}000\), and \(500{,}000\) generations per arm. An experimental configuration is \(x=(o,f,s,n)\in\mathcal{O}\times\mathcal{F}\times\mathcal{S}\times\mathcal{N}\).

Each instrumented run \(r\) of configuration \(x\) produces a record
\[
R_r=\left(q_r,H_r^{\mathrm{gpu}},H_r^{\mathrm{cpu}},\{A_{rj}\}_{j\in\mathcal{J}_r}\right),
\]
where \(q_r\in[0,1]\) is capability, defined as the held-out test-suite pass rate under a fixed sampling protocol; \(H_r^{\mathrm{gpu}}\) and \(H_r^{\mathrm{cpu}}\) are total GPU- and CPU-hours; and \(\mathcal{J}_r\) indexes every oracle call. Each call record is
\[
A_{rj}=(\ell_{rj},\tau_{rj},h_{rj}^{\mathrm{cpu}},h_{rj}^{\mathrm{gpu}},\kappa_{rj}),
\]
where \(\ell_{rj}\) is observed latency, \(\tau_{rj}\in\{0,1\}\) indicates a timeout, \(h_{rj}^{\mathrm{cpu}}\) and \(h_{rj}^{\mathrm{gpu}}\) are call-level resource usages, and \(\kappa_{rj}\) identifies the associated proof or execution obligation. All obligations will be evaluated under prespecified time and resource limits that remain fixed across comparable arms. Timeout observations will be retained explicitly rather than discarded or represented solely through mean latency.

For nonnegative GPU and CPU prices \(p_{\mathrm{gpu}}\) and \(p_{\mathrm{cpu}}\), the end-to-end cost of run \(r\) is
\[
C_r(p_{\mathrm{gpu}},p_{\mathrm{cpu}})
  =H_r^{\mathrm{gpu}}p_{\mathrm{gpu}}
  +H_r^{\mathrm{cpu}}p_{\mathrm{cpu}}.
\]
The resource totals include model generation, execution, solving, verification, and other measured harness activity. The prices will remain free variables, with a dated price sheet defining a reference pair \((p_{\mathrm{gpu}}^0,p_{\mathrm{cpu}}^0)\). Let \(\widehat Q(o,f,s,n)\) and \(\widehat C(o,f,s,n;p_{\mathrm{gpu}},p_{\mathrm{cpu}})\) denote the capability and cost estimates computed from the observed runs of configuration \((o,f,s,n)\).

Under an equal model-compute budget \(n\), the selected oracle for program family \(f\) and specification condition \(s\) is
\[
D_{\mathrm{model}}(f,s,n)
  =\operatorname*{arg\,max}_{o\in\mathcal{O}}
    \widehat Q(o,f,s,n),
\]
where every oracle uses the same model, candidate-generation budget, and sampling protocol. Measured model-side resource usage will also be reported to verify budget comparability.

For an end-to-end cost budget \(B\ge 0\), the best observed capability attainable by oracle \(o\) is
\[
Q_o^{*}(f,s,B;p_{\mathrm{gpu}},p_{\mathrm{cpu}})
=\max_{\substack{n\in\mathcal{N}:\\
\widehat C(o,f,s,n;p_{\mathrm{gpu}},p_{\mathrm{cpu}})\le B}}
\widehat Q(o,f,s,n),
\]
and the equal-cost phase diagram is
\[
D_{\mathrm{cost}}(f,s,B;p_{\mathrm{gpu}},p_{\mathrm{cpu}})
=\operatorname*{arg\,max}_{o\in\mathcal{O}}
Q_o^{*}(f,s,B;p_{\mathrm{gpu}},p_{\mathrm{cpu}}).
\]
Ties will be preserved as sets rather than resolved arbitrarily. A crossover is a budget boundary at which either phase diagram changes its maximizing oracle; because \(\mathcal{N}\) is discrete, unsupported crossovers will be reported as intervals between adjacent observed budgets. Disagreement regions are tuples \((f,s,B)\) for which \(D_{\mathrm{model}}\) and \(D_{\mathrm{cost}}\) yield different oracle orderings.

For each relevant \((o,f,s,n)\), the evaluation will report the complete empirical distribution of call latencies \(\ell_{rj}\), the timeout mass \(\Pr(\tau_{rj}=1)\), and distributions conditional on obligation type \(\kappa_{rj}\). Cost robustness will be assessed through the price ratio
\[
\rho=\frac{p_{\mathrm{gpu}}}{p_{\mathrm{cpu}}},
\]
including threefold perturbations of the reference ratio \(\rho_0=p_{\mathrm{gpu}}^0/p_{\mathrm{cpu}}^0\). The ordering is price-robust for a given \((f,s,B)\) only if \(D_{\mathrm{cost}}\) remains unchanged over the evaluated values of \(\rho\). Planning estimates will determine experimental provisioning only; all phase diagrams, crossovers, and orderings will be derived from measured capability and resource usage.

## Challenges

The problem is difficult because the maximizing oracle may vary across the product space \(\mathcal{F}\times\mathcal{S}\times\mathcal{N}\), while \(\widehat Q\) must reflect held-out capability rather than presumed oracle correctness. Moreover, the number of calls \(|\mathcal{J}_r|\) is not a sufficient proxy for \(C_r\): solver and verifier latencies \(\ell_{rj}\) may be heavy-tailed, timeout-censored, and CPU-intensive, so two configurations with fewer calls can still have different or greater end-to-end costs. These heterogeneous resource profiles make the feasible set in \(Q_o^{*}\) dependent on both \(B\) and \(\rho\), allowing \(D_{\mathrm{model}}\) and \(D_{\mathrm{cost}}\) to disagree or change under price perturbations. Fair comparison further requires identical obligation-level limits across comparable arms, even when oracle types generate obligations of different complexity, and complete accounting of \(\tau_{rj}\) rather than mean-only latency summaries. Finally, the finite budget set \(\mathcal{N}\) permits direct identification only of observed phase assignments and crossover intervals, requiring the study to distinguish empirical measurements from unsupported interpolation or planning assumptions.

## Method Overview

The framework will take program tasks, specifications of controlled provenance and quality, candidate-generation budgets, and matched model checkpoints as input. It will compare test, execution-trace, binary-proof, structured-proof, and hybrid reward oracles under identical sampling and resource constraints, producing held-out capability estimates, complete resource and latency measurements, and uncertainty-aware maps of the best-performing oracle across experimental regimes.

Each candidate will be evaluated through a shared Oracle Evaluation Contract that normalizes heterogeneous oracle calls while preserving their intrinsic computational costs. The resulting rewards will drive matched training runs, while call-level observations will populate a resource ledger. These capability and cost records will subsequently define attainable performance envelopes under equal model compute and equal end-to-end cost, from which oracle winners and crossover regions will be estimated.

The Controlled Multi-Oracle Benchmark will organize preregistered experimental blocks across program family, specification source, specification quality, and candidate budget. Its purpose is to isolate supervision choice from differences in task coverage, sampling conditions, verifier effort, and resource limits, thereby supporting attribution of observed capability differences to the oracle. Controlled specification defects and held-out assessments will establish quality tiers independently of training outcomes.

The Oracle Evaluation Contract and event-sourced resource ledger will provide a common measurement boundary for all oracle types. This module will address incomplete cost attribution and heavy-tailed verification behavior by retaining observed GPU and CPU consumption, wall latency, retries, termination causes, and timeout censoring for every obligation. End-to-end cost will be derived from observed resource usage under symbolic GPU and CPU prices, while latency and timeout distributions will remain explicit rather than being reduced to averages.

The Budget-Sensitive Phase-Diagram Analysis will construct cross-fitted attainable-capability envelopes within each benchmark regime using validation-selected checkpoints and held-out evaluation. It will address the possibility that global rankings conceal regime-specific winners or change when verifier costs are included by comparing equal-model-compute and equal-end-to-end-cost budgets. Bootstrap uncertainty, ambiguous-winner regions, envelope intersections, and GPU-to-CPU price sensitivity will characterize the stability and location of oracle crossovers.

## Methodology

## Controlled Multi-Oracle Benchmark

Comparing heterogeneous reward oracles requires a benchmark that holds sampling conditions and verifier effort constant across test-based, execution-based, proof-based, and hybrid supervision. Otherwise, observed differences may reflect unequal candidate generation or resource limits rather than the supervision mechanism itself.

The central design principle is to block every non-oracle factor and derive rewards from frozen task artifacts. Under this design, the information supplied by each oracle and the intrinsic cost of obtaining that information constitute the only systematic differences between experimental arms.

We will construct preregistered factorial blocks over program family, specification source, specification-quality tier, and candidate-generation budget. Specification quality will be defined before training by introducing controlled defects and calibrating the resulting tiers against two independent criteria: defect-detection performance on held-out semantic mutants and blind expert ratings. This calibration will establish quality as an observed property of the specification rather than a label inferred solely from its source.

All oracle arms will begin from matched model checkpoints and use identical candidate counts, decoding limits, update schedules, random seeds, and sampling procedures. Oracle-specific evaluation will be mediated by a shared Oracle Evaluation Contract. The contract will define a common input task packet, candidate representation, reward interface, termination protocol, and audit schema. Oracle adapters will translate this interface into test outcomes, execution traces, binary proof judgments, structured proof feedback, or hybrid rewards.

Task packets, tests, specifications, proof obligations, and other evaluation artifacts will be frozen before an experimental block begins. Solver versions, solver configurations, timeout thresholds, memory limits, concurrency settings, and other resource caps will likewise remain fixed across arms. The harness will record the effective configuration of every call, enabling audits for deviations in generation settings or verifier limits. This matched protocol permits differences in held-out capability and resource consumption to be attributed to the selected oracle rather than to uncontrolled variation in sampling or evaluation conditions.

## Complete Resource-Cost Measurement

End-to-end oracle cost cannot be inferred reliably from rollout counts or aggregate job duration because proof and execution workloads may exhibit retries, parallelism, caching, wall-clock stalls, and censored timeouts. The measurement system must therefore attribute resource consumption at the level of individual obligations while preserving latency tails and incomplete calls.

Per-obligation event sourcing provides the required separation between consumed compute and elapsed time. Unlike mean latency or job-level accounting, an append-only event record retains the censoring and termination information needed to analyze heavy-tailed oracle behavior.

Every Oracle Evaluation Contract call will pass through an instrumentation layer that writes to an append-only resource ledger. Each record will identify the task and obligation, oracle type, attempt, cache status, retry relationship, degree of parallelism, timeout cap, termination cause, and relevant configuration. Measurements will include process-tree CPU time, reserved GPU time, wall-clock latency, and the timing boundaries required to distinguish oracle execution from queuing or other stalls. Retries and cache accesses will remain explicit events rather than being merged into a single aggregate call.

Observed GPU and CPU hours will be summed directly from ledger records. For GPU and CPU unit prices \(p_g\) and \(p_c\), respectively, end-to-end compute cost will be calculated as

\[
C(p_g,p_c)=p_g H_{\mathrm{gpu}}+p_c H_{\mathrm{cpu}},
\]

where \(H_{\mathrm{gpu}}\) and \(H_{\mathrm{cpu}}\) denote measured resource hours. Equivalently, after normalizing by the CPU price, cost can be parameterized by the GPU-to-CPU price ratio \(r=p_g/p_c\). Retaining symbolic prices allows the same measurements to support alternative pricing regimes without rerunning the benchmark.

Latency will be reported as stratified empirical distributions rather than collapsed into a mean. Completed calls and timed-out calls will be distinguished explicitly, with timeout mass reported for each experimental regime. Kaplan–Meier estimates will be restricted to the identifiable region preceding the timeout cap, and no post-timeout completion times will be imputed. Tail bounds will accompany the observed latency distributions where censoring prevents point identification. Ledger totals will also be reconciled against independent device-level and process-tree meters to assess attribution accuracy.

## Budget-Sensitive Phase Diagrams

Oracle rankings may change across program families, specification conditions, candidate budgets, and compute prices, while noisy capability measurements and heavy-tailed evaluation costs can make apparent crossovers unstable. The analysis must therefore distinguish equal-model-compute comparisons from equal-end-to-end-cost comparisons and quantify uncertainty in both winners and crossover locations.

Attainable-capability envelopes make these comparisons interpretable without assuming that learning trajectories are monotone. A larger budget can always reuse a checkpoint available at a smaller budget, so the best attainable capability is monotone in budget even when individual training runs are not.

For each program-family, specification-source, quality-tier, and candidate-budget cell, we will construct a separate attainable-capability envelope for every oracle. Checkpoints will be selected using validation data and evaluated only on held-out tasks. Cross-fitting will separate checkpoint selection from capability estimation, reducing selection bias while preserving the ability to compare multiple checkpoints from each training trajectory.

Two eligibility rules will define the envelopes. Under equal model compute, a checkpoint will be eligible when its observed GPU usage satisfies \(H_{\mathrm{gpu}}\leq B\). Under equal end-to-end cost, eligibility will require \(C(r)\leq B\), where cost is derived from the resource ledger and \(r\) is the GPU-to-CPU price ratio. At each budget \(B\), an oracle’s envelope will retain the held-out capability of the best eligible checkpoint.

Uncertainty will be estimated by cluster-bootstrapping both tasks and training seeds. For each bootstrap replicate and factorial cell, envelopes, winners, and envelope intersections will be recomputed jointly. An oracle will be declared the winner only when its bootstrap probability of being best is at least \(0.8\); cells failing this criterion will be marked ambiguous rather than assigned a potentially unstable ranking.

Price sensitivity will be evaluated at three price ratios only — the reference ratio \(r_0\), \(r_0/3\), and \(3r_0\). **There is no interpolation grid on either axis.** An earlier version of this paragraph added "a log-spaced interpolation grid", which contradicts the commitment made below that unmeasured cells are reported as unobserved and never interpolated; it also conflated the **price-ratio** axis with the **candidate-budget** axis, which are separate and must not be crossed into a single grid. Equal-cost envelopes will be reconstructed at each of the three ratios from the same observed GPU and CPU measurements. Where the winner changes between two adjacent **measured** budgets, the crossover is reported as that bracketing interval, and the bootstrap summarizes uncertainty over which interval brackets it — not over a point location. The resulting phase diagrams will show where oracle rankings differ between budget definitions, where price changes alter the preferred oracle, and where the available evidence does not support a unique winner.

## Experiments

## Experimental Setup

The evaluation will use three complementary datasets. The **Controlled Multi-Oracle Factorial Benchmark** crosses all preregistered program families, specification sources, specification-quality tiers, and candidate-generation budgets on shared task seeds. It is selected to test resource equivalence and budget-dependent oracle ordering under controlled conditions. The **Blinded Specification-Defect Validation Set** contains held-out defect challenges that are unavailable during quality-tier assignment. This separation enables a non-circular assessment of whether the tiers predict independently observed defect detectability. The **Metered Oracle Execution and Stall Traces** retain per-call GPU and CPU consumption, concurrency, complete latency observations, timeout indicators, and training-step stalls. These traces support attribution and tail-latency analyses, including proof-heavy regimes in which naive accounting may be unreliable.

Three diagnostic baselines will be evaluated. **Source-Only Quality Labels** represent quality using specification provenance alone and test whether the preregistered tiers contain information beyond source. **Naive Job-Wall-Time Accounting** attributes resource consumption from total job duration and therefore provides a control for errors caused by idle periods, concurrency, and overlapping GPU and CPU work. **Mean-Latency Stall Model** summarizes oracle latency with its mean and tests whether scalar summaries omit operationally significant tail and timeout behavior. These baselines are measurement sanity checks rather than general effectiveness baselines.

**The study is staged, and the stages differ by roughly two orders of magnitude in cost. This is deliberate: the measurement instrument is the contribution, and it is validated before any factorial is attempted.**

**Phase 1 — instrument construction and validation (RQ1–RQ4). No new training runs.** The ledger, the Oracle Evaluation Contract, and the envelope machinery are exercised against (i) synthetic task and specification generators with mock oracle latencies drawn from configurable heavy-tailed distributions, and (ii) *the training runs of the companion experiments in this research program*, which already execute proof-oracle and execution-oracle arms on a shared Dafny corpus **and whose specifications require an append-only per-oracle-call resource ledger** — wall latency, solver CPU, GPU time, termination cause, timeout cap, retries and cache status per call. That requirement was added to those studies precisely so this phase is possible; without it there is nothing to instrument and Phase 1 silently becomes a new-training-runs study. Phase 1 therefore consumes instrumentation overhead rather than training compute. Its scale is modest and self-contained: resource equivalence over 100 independent seeds per oracle arm; specification-quality validation on \(N=\max(300,60\text{ per program family})\) balanced specifications; 1,000 instrumented jobs per oracle across low, medium, and high concurrency; and 10,000 oracle calls plus 5,000 integrated training steps per proof-based regime under fixed timeout and resource caps, split evenly between baseline fitting and held-out evaluation.

**Gate.** Phase 2 proceeds only if Phase 1 establishes that per-call attribution is accurate (RQ3) and that the censoring-aware latency model beats the mean-latency baseline (RQ4). If the ledger cannot attribute resources correctly, no phase diagram computed from it is trustworthy, and the honest deliverable is the negative measurement result.

**Phase 2 — phase diagrams over the companion arms (RQ5–RQ6).** Restricted to the oracle arms, program families, and budgets the companion experiments actually run. This yields a phase diagram over a **small number of measured cells**, not a saturated grid: crossovers are reported as intervals between adjacent observed budgets, and cells that were not run are reported as unobserved rather than interpolated.

**Phase 3 — saturated factorial (aspirational; scope it to available compute before committing).** The full design crosses five oracles × five program families × two specification sources × three candidate budgets. At candidate budgets of 50k/200k/500k per arm this is on the order of several hundred training runs and is **not claimed as executable within this paper**. Where the text below quantifies a saturated design — "at least 120 cells with 20,000 paired held-out task-seed outcomes per cell and oracle" — that figure describes Phase 3 and must be read as an upper bound on ambition, not a commitment. Any cell count actually reported will be the cell count actually measured.

End-to-end cost will be computed from observed resource consumption as

\[
C = H_{\mathrm{gpu}}p_{\mathrm{gpu}} + H_{\mathrm{cpu}}p_{\mathrm{cpu}},
\]

where \(H_{\mathrm{gpu}}\) and \(H_{\mathrm{cpu}}\) are metered GPU and CPU hours and \(p_{\mathrm{gpu}}\) and \(p_{\mathrm{cpu}}\) are their respective prices. Equal-cost analyses will use the preregistered reference GPU-to-CPU price ratio \(r_0\), followed by sensitivity analyses at \(r_0/3\) and \(3r_0\). Winner probabilities and uncertainty intervals will be estimated through paired or family-stratified bootstrap procedures as appropriate. Primary metrics comprise resource-equivalence differences, quality-score correlations, meter-reconciliation errors, empirical latency and stall distributions, capability at matched budgets, winner probabilities, crossover coordinates, and winner-retention rates. Source labels, job wall time, and mean latency will be used only in their designated diagnostic comparisons.

The experiments address the following research questions:

1. **RQ1:** Does the benchmark maintain equivalent candidate-generation compute across oracle arms without configuration or resource-cap violations?
2. **RQ2:** Do preregistered specification-quality tiers measure independently observed defect detectability rather than merely encoding specification source?
3. **RQ3:** Does per-call ledger accounting accurately attribute GPU and CPU consumption under heterogeneous oracle workloads?
4. **RQ4:** Do complete latency and timeout distributions reveal proof-oracle stalls that mean-latency accounting misses?
5. **RQ5:** How often do equal-model-compute and equal-end-to-end-cost constraints select different oracles, and where do winner crossovers occur?
6. **RQ6:** Is equal-cost oracle ordering robust to a threefold change in the GPU-to-CPU price ratio?

## RQ1: Candidate-Generation Resource Equivalence

RQ1 tests whether oracle arms receive equivalent candidate-generation compute. The underlying challenge is to span all required program families, specification conditions, and generation budgets while preventing differences in sampling configuration or resource allocation from confounding comparisons among oracles.

For every program-family × specification-quality × generation-budget block, each oracle arm will be executed on 100 independent seeds. Models, prompts, sampling parameters, hardware, and resource caps will remain fixed within a block. Candidate counts, generated-token totals, and metered GPU hours will be compared using simultaneous equivalence intervals. Launch configurations and resource-limit events will also be audited. This analysis does not use an effectiveness baseline; its control is the direct within-block comparison of oracle arms under identical generation settings. Auditing configuration and cap events provides an ablation-like diagnostic that distinguishes resource imbalance from execution-policy violations.

A positive result would require every simultaneous arm-difference interval to lie within \(\pm1\%\), with no configuration or resource-cap deviations. Such an outcome would support the hypothesis that observed downstream differences are not attributable to unequal candidate-generation resources.

Evaluation metrics are:

- Relative range and pairwise differences in candidate count.
- Relative range and pairwise differences in generated tokens.
- Relative range and pairwise differences in metered GPU hours.
- Configuration-deviation count.
- Resource-cap-deviation count.

## RQ2: Independent Validity of Specification-Quality Tiers

RQ2 tests whether preregistered quality tiers predict defect detectability on unseen challenges. In plain terms, the experiment asks whether the tiers measure specification quality itself or merely restate where a specification originated.

The analysis will use \(N=\max(300,60\text{ per program family})\) specifications balanced across source and tier. Tiers will be assigned before a disjoint, blinded defect challenge set is revealed. Held-out defect-detection scores will then be correlated with tier ranks. The Source-Only Quality Labels baseline will be evaluated on the same specifications. Family-stratified bootstrap inference will estimate both the tier-score correlation and its improvement over the source-only correlation. Comparing tier ranks against source-only labels constitutes the principal ablation of the tier representation.

A positive result would place the lower 95% confidence bound for the tier-score Spearman correlation at or above 0.8 and the lower bound for its improvement over source-only labels at or above 0.2. This would support the hypothesis that the tiers capture independently observable differences in defect detectability beyond specification provenance.

Evaluation metrics are:

- Spearman correlation between quality tier and held-out defect-detection score.
- Correlation difference relative to Source-Only Quality Labels.
- Family-stratified bootstrap confidence intervals.

## RQ3: Accuracy of Per-Call Resource Attribution

RQ3 tests whether per-call ledger accounting can recover GPU and CPU consumption under heterogeneous workloads. The practical challenge is to attribute resources correctly when jobs contain idle intervals, concurrent calls, or overlapping GPU and CPU activity.

For each oracle, 1,000 instrumented jobs will be collected, balanced across benchmark strata and low, medium, and high concurrency. Ledger-attributed GPU hours will be reconciled against independent device telemetry, while attributed CPU hours will be reconciled against operating-system process-tree meters. The same jobs will then be recomputed using Naive Job-Wall-Time Accounting. Results will be stratified by oracle, concurrency level, and accounting method. Replacing ledger attribution with wall-time attribution provides the principal accounting ablation.

A positive result would require the GPU- and CPU-hour reconciliation intervals for ledger accounting to fall wholly within \(\pm1\%\). In addition, at least one oracle should exhibit a lower 95% confidence bound above 5% absolute error under wall-time accounting. This pattern would support the hypothesis that per-call accounting remains accurate under concurrency and overlap, whereas wall time can materially misattribute resources.

Evaluation metrics are:

- Absolute GPU-hour reconciliation error.
- Relative GPU-hour reconciliation error.
- Absolute CPU-hour reconciliation error.
- Relative CPU-hour reconciliation error.
- Errors stratified by oracle, concurrency level, and accounting method.

## RQ4: Tail Latency, Timeouts, and Training-Step Stalls

RQ4 tests whether full latency and timeout distributions reveal proof-oracle stalls that a mean-latency model misses. The challenge is that rare slow calls and timeouts may dominate training-step delays even when average call latency appears acceptable.

For each proof-based regime, the experiment will record 10,000 oracle calls and 5,000 integrated training steps under fixed timeout and resource caps. Completed-call latencies and timeout indicators will be retained separately. The traces will be divided equally: the Mean-Latency Stall Model will be fitted on one half, and its training-step stall predictions will be evaluated on the held-out half. Empirical latency distributions, timeout mass, and p95 step stalls will be compared with the baseline predictions. Replacing the complete distribution with its mean is the principal ablation.

A positive result would occur if at least one proof-based regime has either a completed-call p99 latency at least ten times its median or a timeout probability of at least 5%, and the mean-based model underpredicts empirical p95 training-step stall by at least 25%. This would support the hypothesis that operational risk is concentrated in tails or timeouts and cannot be represented adequately by mean latency alone.

Evaluation metrics are:

- Full empirical latency cumulative distribution.
- Median completed-call latency.
- p99 completed-call latency.
- Timeout probability.
- Empirical p95 training-step stall.
- Relative underprediction by the Mean-Latency Stall Model.

## RQ5: Budget-Dependent Oracle Ordering and Crossovers

RQ5 tests whether equal-model-compute and equal-end-to-end-cost constraints yield different oracle selections and locates the budgets at which winners change. The challenge is that an oracle favored under matched GPU consumption may not remain preferable after CPU usage and resource prices are included.

In Phase 2 this analysis runs over the cells the companion experiments actually execute — a small number of measured program-family × specification-source × budget combinations, not a saturated grid. (The saturated Phase 3 design would reach at least 120 cells with 20,000 paired held-out task-seed outcomes per cell and oracle; that scale is aspirational and is not claimed here.) **Unmeasured cells are reported as unobserved, never interpolated, and the reported cell count is always the measured cell count.** Equal-GPU and equal-cost frontiers will be constructed from observed capability and resource measurements. Equal-cost values will use \(C=H_{\mathrm{gpu}}p_{\mathrm{gpu}}+H_{\mathrm{cpu}}p_{\mathrm{cpu}}\) at \(r_0\). Paired bootstrap resampling will estimate the probability that each oracle is best. For adjacent budget intervals in which the winner changes, the crossover is reported as **that interval**, not as a point. Bisection would require evaluating capability at budgets between the measured ones, which is the interpolation this study rules out; with a discrete budget grid the defensible object is a bracketing interval, and narrowing it requires measuring more budgets rather than modelling between them. Comparing equal-GPU and equal-cost frontiers is the principal budget-definition ablation.

A positive result would show that a non-trivial fraction of **measured** cells have different qualifying winners under the two constraints — preregistered at 10% for the saturated Phase 3 design, but reported in Phase 2 as a count out of the cells actually run, since a proportion over a handful of cells is not a meaningful rate. With few cells, a single disagreement is reported as an existence proof that the two budget definitions can diverge, which is itself the claim of interest, and not as a rate. In each such comparison, the selected winner should have \(P(\mathrm{best})\geq0.8\) and a held-out capability advantage of at least two percentage points over the runner-up under the corresponding budget. This would support the hypothesis that oracle ordering depends materially on whether the budget accounts only for model compute or for total measured cost.

Evaluation metrics are:

- Capability at matched budgets.
- Bootstrap \(P(\mathrm{best})\).
- Winner–runner-up capability difference.
- Fraction of cells with different equal-GPU and equal-cost winners.
- Budget coordinates of crossover points.
- Cost coordinates of crossover points.

## RQ6: Robustness to GPU-to-CPU Price Ratios

RQ6 tests whether equal-cost oracle ordering remains stable when the GPU-to-CPU price ratio changes threefold in either direction. The challenge is to determine whether conclusions drawn at the reference ratio reflect robust resource-performance trade-offs or depend narrowly on a particular pricing assumption.

Using the same measured cells as RQ5, every observed resource-performance point will be repriced at \(r_0/3\), \(r_0\), and \(3r_0\). Equal-cost frontiers and paired-bootstrap winner probabilities will be reconstructed independently at each ratio. Retention will be evaluated only for cells with \(P(\mathrm{best})\geq0.8\) at \(r_0\). **Because Phase 2 measures few cells, this analysis is expected to be underpowered and must be reported as such**; the saturated Phase 3 design would require at least 80 qualifying cells before a robustness claim is made. Reporting an underpowered price-sensitivity result honestly is preferable to withholding it, since the direction of any observed instability is itself informative. Repricing the same measured points isolates price sensitivity without changing observed resource use or capability.

A positive result would require at least 75% of eligible cells to retain the same equal-cost winner at both \(r_0/3\) and \(3r_0\), with \(P(\mathrm{best})\geq0.8\) at each ratio. This would support the hypothesis that most confidently selected oracles remain preferable across substantial changes in relative GPU and CPU prices.

Evaluation metrics are:

- Equal-cost winner at each price ratio.
- Bootstrap \(P(\mathrm{best})\) at each price ratio.
- Joint winner-retention indicator.
- Fraction of eligible cells retaining the same winner.
- Price-ratio crossover locations.

## Related Work

**Which prior systems supply this study's experimental arms.** A measurement study needs concrete
training pipelines to instantiate its oracles. Each of the five oracles is therefore anchored to a
published recipe where one exists, and declared study-defined where none does:

| Oracle | Anchoring prior work |
|---|---|
| Test outcome | Le et al. \[2022\] (CodeRL), unit-test-derived functional feedback in its canonical form |
| Execution process | Tang et al. \[2026\] (ExecVerify), with Wang et al. \[2026\] (StepCodeReasoner) as an independent second instantiation of the same design |
| Binary proof | Yan et al. \[2025\] (Re:Form) and Tan \[2026\], both verifier-acceptance rewards over Dafny |
| Structured proof | The Haladir Team \[2026\] (RLFR) as the scalar proof-obligation precursor — a shaped reward equal to the proportion of obligations discharged — together with the typed verification-condition implementation developed in the companion study |
| Hybrid | **Study-defined.** No published system combines proof and execution rewards in a single code-RL objective; the closest precedent is proof-plus-counterexample supervision in semantic-equivalence self-play, which we cite as motivation rather than as a recipe |

**Re:Form anchors the binary-proof arm only.** Its "subset reward" is easily mistaken for structured
verification-condition feedback and is not: it checks whether a generated specification is stronger
than the ground-truth specification, which is a property of the *specification* rather than a
decomposition of the proof obligations discharged for a candidate program. Treating it as a
structured-proof recipe would mis-attribute the arm and would make the binary-versus-structured
contrast — the contrast this study exists to price — incoherent.

These are adopted as arm-supplying baselines rather than as points of comparison, and reproducing
them faithfully is a precondition for the comparison to mean anything. In particular, ExecVerify's
two-stage structure must be preserved — Stage I mixes the white-box term with a terminal
input/output term at α = 0.5, and Stage II switches to unit-test pass fraction — since a purely
stepwise execution arm would be a straw man. RLFR is unrefereed, is no longer available at its
original URL, and releases no implementation details, so the structured-proof precursor is
reproduced as a **formula-faithful arm under our harness**, not as an exact reproduction, and that
limitation is reported with the result.

**Three cost-aware neighbors bound the claim.** Orlanski et al. [[2025](https://arxiv.org/abs/2506.10056)]
map an accuracy-versus-throughput frontier for code *verifiers* — the closest published statement
that verification has a compute price and the choice among verifiers is a frontier — but in a
test-time generate-then-rank setting: no RL training, no proof oracles, no solver CPU accounting,
and no price model. It is the test-time analogue of this study's training-time question. Mitsuhashi
et al. [[2026](https://arxiv.org/abs/2605.25252)] quantify compute–supervision tradeoffs in RLVR by
varying verifier quality against rollout compute with the verifier priced at zero — direct published
evidence for the premise that the field treats oracle cost as free, cited as motivation rather than
as a competitor. JURY-RL (Chen et al. [[2026](https://arxiv.org/abs/2604.25419)]) reports
per-training-step wall-clock for its cached Lean verifier inside an RLVR paper — a one-off table for
a single oracle, with no capability-per-cost normalization, no latency distributions, and no price
parameterization. It confirms the gap while forbidding any claim that verifier wall-clock is never
measured inside RL training; what remains unoccupied is the systematic, cost-normalized capability
comparison across oracle types that this study runs.

Each subsection below therefore states, for its works, the paper-specific efficiency claim this study
would test, not merely that the work omits cost accounting.

## Execution-Grounded Supervision for Code Generation

Execution-grounded learning uses test outcomes, runtime traces, and iterative feedback to improve code synthesis. Le et al. [[2022](https://arxiv.org/abs/2207.01780)] train an actor–critic architecture with unit-test feedback, whereas Gehring et al. [[2025](https://proceedings.mlr.press/v267/gehring25a.html)] teach models to exploit execution feedback across successive synthesis attempts and Jain et al. [[2025](https://arxiv.org/abs/2502.20380)] formulate multi-turn generation using single-step rewards. Yu et al. [[2024](https://arxiv.org/abs/2412.15118)] combine execution profiling, self-critique, and tree-structured search to integrate process and outcome supervision. Wang et al. [[2026](https://arxiv.org/abs/2605.11922)] supervise anchored intermediate runtime states through bi-level reinforcement learning, while Tang et al. [[2026](https://arxiv.org/abs/2603.11226)] derive white-box rewards from control flow and variable states before transferring execution reasoning to code generation. Each carries a specific efficiency claim this study can price. Gehring et al. report reaching prior state of the art on CodeContests with a single rollout against five solutions from 100 samples, and with a budget of three samples against AlphaCode's 1,000 — an order-of-magnitude *sample* reduction whose end-to-end cost is unknown, because samples and oracle calls are not the same currency. Tang et al. report a 5.9% relative pass@1 gain (a cross-benchmark average of 53.9 to 57.1, i.e. 3.2 percentage points) over a pure unit-test-GRPO baseline on the same backbone, obtained by adding white-box supervision whose per-call cost is never separated from generation cost. The shared limitation is that these approaches assess capability or *sample* efficiency while treating reward computation as effectively unpriced, leaving test, trace, proof, and hybrid supervision incomparable under matched model-compute and end-to-end cost budgets.

## Verifier-Guided Program Synthesis and Verification

Verifier-guided synthesis and verification couple language models with formal tools that validate, refine, or repair generated artifacts. Aggarwal et al. [[2024](https://arxiv.org/abs/2412.06176)] bootstrap verified code through cross-language translation and verifier-guided tree refinement, while Sun et al. [[2024](https://theory.stanford.edu/~barrett/pubs/SSP%2B24-abstract.html)] check consistency among implementations, documentation, and formal annotations. Wu et al. [[2024](https://arxiv.org/abs/2310.04870)] combine language-model-generated abstractions with automated reasoners, Kamath et al. [[2023](https://arxiv.org/abs/2311.07948)] use symbolic checking to validate generated loop invariants, and Li et al. [[2026](https://arxiv.org/abs/2605.17914)] formalize and check local reasoning steps to provide targeted refinement feedback. Yan et al. [[2025](https://arxiv.org/abs/2507.16331)] use curated Dafny data and verifier-guided reinforcement learning, Tan [[2026](https://arxiv.org/abs/2605.30914)] studies verifier rewards and recursive proof repair, and a recent hardware-synthesis system [[2025](https://arxiv.org/abs/2509.06239)] integrates verifier-driven prompt repair with downstream hardware generation. Miceli Barone and Nok [[2026](https://aclanthology.org/2026.findings-acl.1615/)] validate semantic-equivalence self-play using proofs and counterexamples, whereas Lin et al. [[2024](https://papers.neurips.cc/paper_files/paper/2024/hash/62c6d7893b13a13c659cb815852dd00d-Abstract-Datasets_and_Benchmarks_Track.html)] translate C verification tasks into interactive Isabelle proving. Again the claims are specific and priceable. Yan et al. frame verifier-driven RL as the *scalable* route to formal supervision — scalability being precisely a cost assertion — while reporting hardware and wall-clock in separate columns and no GPU-hours; Li et al. report token cost for their inference-time refinement loop but no solver CPU time, so the dominant term in a verifier-in-the-loop budget goes unmeasured; and Tan reports a verified-reward trajectory without the solver-side accounting that would say what that trajectory cost. The shared limitation is that formal verification is treated primarily as a correctness signal or generation endpoint rather than as a priced oracle whose latency, timeouts, and CPU consumption can be compared with execution-based supervision.

## Neural Formal Theorem Proving

Neural formal theorem proving uses proof-assistant feedback, reinforcement learning, and structured search to generate machine-checkable mathematical proofs. Hubert et al. [[2026](https://doi.org/10.1038/s41586-025-09833-y)] develop reinforcement-learning-based formal reasoning for Olympiad-level mathematics, while Dong et al. [[2024](https://arxiv.org/abs/2411.01829)] reward models for proposing and proving useful intermediate lemmas. Xin et al. [[2024](https://arxiv.org/abs/2408.08152)] combine proof-assistant feedback with Monte Carlo tree search, and Ren et al. [[2025](https://arxiv.org/abs/2504.21801)] use recursively generated subgoal decompositions to initialize reinforcement learning. Lin et al. [[2025](https://arxiv.org/abs/2508.03613)] integrate scaffolded data synthesis with verifier-guided self-correction, whereas Leang et al. [[2025](https://arxiv.org/abs/2502.13137)] use theorem provers to validate synthetic reasoning data and provide reinforcement-learning feedback. The shared limitation is that this literature optimizes proof success, decomposition, or data validity without determining when proof-based supervision is cost-efficient relative to test and execution oracles under comparable resource budgets.

## Conclusion

Determining whether proof supervision is economically preferable to execution-based feedback requires treating oracle evaluation as part of the learning system rather than as a free correctness check. The proposed framework integrates controlled oracle comparisons, call-level resource attribution, complete tail and timeout accounting, and uncertainty-aware capability envelopes to reveal how supervision value and evaluation cost interact across program structure, specification quality, generation scale, and hardware prices. Its central contribution is a budget-sensitive account of oracle choice: the preferred signal may depend on whether compute is matched at the model boundary or cost is matched across the complete GPU–CPU pipeline. The planned evaluation will establish where oracle rankings are stable, where they reverse, and where evidence is insufficient to select a winner, while quantifying the operational consequences of heavy-tailed verifier behavior. These findings should support more defensible efficiency claims and better-informed infrastructure decisions for code reinforcement learning. Future work should examine how alternative fixed timeout and resource-cap policies reshape crossover boundaries without compromising comparability. Longitudinal replication with updated price sheets, together with controlled analyses of caching and parallelism, could determine whether observed phase boundaries persist as deployment conditions change.

---

## Revision log (working note — remove before submission)

Revised from the AutoDiscussion output of room `7bcfe3ef` (twin; the original `2a72d422` died in a
related-work retry loop), which closed 6/6 with 5/6 clean and one unresolved major.

1. **Scope inflation corrected — the primary fix.** The generated draft committed to "at least 120
   cells and 20,000 paired held-out task-seed outcomes per cell and oracle," i.e. roughly 600 training
   runs at candidate budgets of 50k–500k per arm. The seed had specified the opposite: *"measurement-only
   instrumentation layered on the training runs of the companion experiments."* The study is now
   explicitly three-staged — Phase 1 instrument validation on synthetic latencies and the companion
   runs (no new training), a **gate** requiring accurate per-call attribution and a censoring-aware
   latency model that beats the mean-latency baseline, Phase 2 phase diagrams over the cells the
   companion experiments actually execute, and Phase 3 saturated factorial marked aspirational and
   explicitly not claimed. Unmeasured cells are reported as unobserved, never interpolated, and the
   reported cell count is always the measured cell count.
2. **Reinstated the two anchors that motivate the paper.** (a) Re:Form reports GPU counts and
   wall-clock separately (0.5B: 16 × A800-SXM4-80G for ~11 h; 1.5B: 16 × ~25 h) and states **no
   GPU-hours figure**, so the circulating ~176/~400 are downstream arithmetic and the 40-epoch detail
   attaches only to the 3B run. (b) The **tenfold swing**: ~1M SMT/assertion-batch evaluations for a
   200k-candidate structured-VC arm is ~56 CPU-hours at 0.2 s mean batch time and ~556 at 2.0 s. That
   swing is the paper's reason to exist and had been reduced to a generic "heavy tail" assertion.
3. **Resolved the related_work major.** The artifact marked all eight works `is_potential_baseline=false`,
   leaving no path from literature to experimental arms. Related Work now opens by naming which prior
   systems are *constitutive*: Yan et al. supplies the proof arms, Tang et al. the execution-process
   arm (with Wang et al. as an independent second instantiation), Tan a cross-check proof arm, Le et
   al. the test-outcome arm — plus the warning that ExecVerify's two-stage structure must be
   reproduced or the execution arm becomes a straw man.
4. **Replaced the circular limitations** flagged as a minor. Every subsection previously ended with a
   near-identical restatement of "they never measure oracle cost." Each now names the paper-specific
   efficiency claim this study would price: RLEF's order-of-magnitude *sample* reduction (3 samples vs
   100 and vs 1,000 on CodeContests), ExecVerify's 5.9% *relative* pass@1 gain (53.9→57.1, i.e. +3.2
   points — **not** 5.9 percentage points), Re:Form's scalability framing, LORIS's token-cost-only
   reporting.
5. **Underpowering stated rather than hidden.** RQ6's price-robustness analysis over few measured
   cells is now declared expected-underpowered, with the Phase 3 threshold (≥80 qualifying cells)
   named as the bar for an actual robustness claim.

6. **2026-08-23 round-10 (deer-flow academic-paper-review pass).** The round-8 scoop sweep ordered
   three cost-aware neighbors into the ledger, but they were never absorbed into this manuscript —
   the seed block was the only place they existed. Related Work now carries a "three cost-aware
   neighbors" paragraph distinguishing Orlanski et al. (arXiv:2506.10056, test-time verifier
   frontier), Mitsuhashi et al. (arXiv:2605.25252, verifier priced at zero — motivating evidence),
   and JURY-RL (Chen et al., arXiv:2604.25419, one-off Lean-verifier wall-clock table). The
   introduction's solver-cost universal is softened accordingly: JURY-RL *does* measure verifier
   wall-clock inside RL training, so the unoccupied claim is now stated as "no systematic,
   cost-normalized capability comparison across oracle types." All three ids re-verified against the
   arXiv export API in one batched request this pass. Found by `deerflow_review_2026-08-23.md` (W2).

## Outstanding, not fixed here

- **Citation formatting in the prose.** The introduction renders citations as `Hung Le et al.. CodeRL:
  …` with doubled periods and no venue or identifier, while Related Work uses correct linked form with
  real venues. Unify on the latter at bib time.
- **Proof2Silicon is credited to "(unknown authors)"** despite the seeded reference naming Jha, Wan &
  Chen; the pipeline drops author lists on some entries. Same defect produced "(unknown authors)" for
  Gao, Schulman & Hilton in the companion ZW2 package.
- **Venue corrections to apply at bib time**: RLEF is ICML 2025, PMLR 267:19034–19055 — cite the
  six-author camera-ready list, not arXiv v2's seven. ORPS must appear under its ICML title,
  *"Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation."* CodeRL is
  NeurIPS 2022 on a CodeT5 backbone.
