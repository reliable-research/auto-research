# deerflow_review — ZW4_oracle_economics

- **Skills used**: `.claude/skills/academic-paper-review/SKILL.md` (review procedure + output template) and `.claude/skills/deep-research/SKILL.md` (literature-context web-research methodology)
- **Review date**: 2026-08-23
- **Reviewer**: deer-flow academic-paper-review skill (Claude agent)
- **Files reviewed**: `paper-draft.revised.md` (current manuscript, read in full including revision log), `experiment-spec.md` (current spec, read in full), `seed.md` (context only)
- **Review mode**: pre-registration-style draft with no collected results — "Statistical Rigor" assesses the *planned* analysis; "Reproducibility" rates spec completeness. Findings-only; no package files edited.

## Search log

Every web query run for the literature-context phase, with hit/empty status:

| # | Query | Status |
|---|-------|--------|
| 1 | `cost-normalized comparison reward oracles code reinforcement learning 2026` | HIT — surfaced arXiv:2509.21882 (Hidden Costs and Measurement Gaps of RLVR); other hits tangential |
| 2 | `compute cost of verification vs execution vs LLM judge rewards RLVR training 2026` | HIT — surfaced JURY-RL (arXiv:2604.25419, cache-amortized verifier wall-clock), arXiv:2602.01523 (Relative-Budget Theory for RLVR), Modal verifier-model roundup |
| 3 | `verifier compute cost accounting reinforcement learning verifiable rewards GPU CPU hours` | HIT — surfaced "The Verification Tax" (airealist.ai) and several RLVR reward-cost papers reporting overhead percentages |
| 4 | `Dafny SMT solver verification time heavy tail timeout wall-clock cost training loop LLM` | HIT — Dafny Verification Optimization docs (resource count vs wall-clock), DafnyPro (POPL 2026), Dissect-and-Restore; confirms Dafny-cost-variability premise, no direct heavy-tail training-loop measurement found |
| 5 | `"phase diagram" compute budget crossover oracle capability envelope pareto frontier LLM training cost comparison` | HIT — method-twin sweep: Capability Frontier (arXiv:2606.26836), Shadow Price of Reasoning (arXiv:2606.03092), LLM cascade decision theory (arXiv:2605.06350); all inference-time, none an RL-training oracle phase diagram |
| 6 | `censored latency Kaplan-Meier timeout measurement solver benchmarking methodology` | HIT — general KM/censoring methodology (network-latency censoring literature); confirms the manuscript's non-informative-censoring caveat is a live threat, no solver-specific twin found |
| 7 | `"verifier is free" assumption criticism reward computation cost ignored RL code generation limitations` | HIT — verifier-free RL papers (arXiv:2605.09920, RLPR), criticisms of verifier design cost; nothing pricing oracle CPU into a training budget |
| 8 | `proof supervision vs test rewards code RL cost August 2026` | HIT (noisy) — ReCode (arXiv:2508.05170), awesome-RLVR list; most results off-topic (query pulled coupon-code spam), no scooping work found |

WebFetch deep-reads (3): arXiv:2509.21882 abstract page; airealist.ai "The Verification Tax"; arXiv:2506.10056 (Pareto Optimal Code Generation) abstract page.

**arXiv id verification**: one batched request `id_list=2506.10056,2509.21882,2604.25419,2605.25252,2507.16331,2602.01523,2603.11226,2605.17914` — all 8 resolved with matching titles. No citation debt.

---

# Paper Review: Cost-Aware Phase Diagrams for Proof and Execution Oracles in Code Reinforcement Learning

## Paper Metadata
- **Authors**: Not stated in manuscript (AutoDiscussion-generated draft, room `7bcfe3ef`, revised by project maintainer)
- **Venue**: Unsubmitted pre-registration-style draft (loop_r1 research-program family, package ZW4)
- **Year**: 2026
- **Domain**: Machine learning for code / reinforcement learning with verifiable rewards / empirical measurement methodology
- **Paper Type**: Pre-registered empirical measurement study (registered-report style; no collected results)

## Executive Summary

The paper attacks a real and, per this review's literature sweep, still-unoccupied gap: no published work compares test, execution-process, binary-proof, structured-proof, and hybrid reward oracles for code RL under an end-to-end cost budget that charges solver CPU time alongside GPU time. The claimed field-wide blind spot is corroborated from multiple independent directions — the position paper "Hidden Costs and Measurement Gaps of RLVR" (arXiv:2509.21882) documents budget-mismatch confounds without pricing oracles; industry analysis ("The Verification Tax") documents CPU-side verification as the actual pacing constraint of code-RL training (e.g., ~41,000 sandbox executions per training step; DeepCoder's 32 H100s gated by 1k+ sandbox executions/minute) with no systematic accounting; and the closest academic neighbor, Pareto Optimal Code Generation (arXiv:2506.10056), prices verifier throughput only at test time, not in RL training, and includes no proof oracles. The manuscript's two motivating anchors — Re:Form reporting no GPU-hours figure anywhere while ~176/~400 GPU-h circulate as if reported, and a tenfold (~56 vs ~556 CPU-h) swing in the solver-side denominator of a 200k-candidate structured-proof arm depending on an unreported mean batch time — are concrete, checkable, and effective.

The proposal's distinctive virtue is epistemic discipline: a three-phase staging in which the measurement instrument (append-only per-call resource ledger, Oracle Evaluation Contract, censoring-aware latency modeling) is validated before any phase diagram is computed, a hard gate between phases, crossovers reported as bracketing intervals between measured budgets with interpolation explicitly banned, and declared underpowering for the price-robustness analysis. The experiment spec is unusually complete, down to machine-checkable success predicates per RQ.

The main shortfalls are: (1) the deliverable the title and abstract promise — phase diagrams — is, in the actually-claimed Phase 2, a handful of cells inherited from companion experiments the paper does not control, so the honest expected output is an existence proof plus a validated instrument, and the framing has not fully caught up with that demotion; (2) the Related Work has not absorbed the three neighbors the project's own 2026-08-23 scoop sweep ordered added (Pareto Optimal Code Generation, arXiv:2605.25252, JURY-RL), one of which (JURY-RL's cache-amortized verifier wall-clock reporting) directly constrains how strongly the "nobody accounts" framing may be stated; (3) the Phase-1→Phase-2 gate conflates instrument validity with a contingent property of the world (heavy-tailed latency), so a well-behaved oracle workload could block the study for the wrong reason; and (4) the capability estimand — held-out test-suite pass rate — is the same currency the test-outcome oracle trains on, an alignment confound between evaluation and one treatment arm that the manuscript never discusses. Overall this is a valuable, honest, well-specified measurement proposal whose principal risks are dependency and framing, not soundness.

## Summary of Contributions

1. A controlled multi-oracle benchmark that isolates supervision choice by freezing generation, verification, and resource conditions across five reward-oracle types (Contributions, Methodology §Controlled Multi-Oracle Benchmark).
2. Per-obligation event-sourced resource accounting that attributes GPU/CPU consumption while preserving latency tails, timeout mass, concurrency, and censoring (Methodology §Complete Resource-Cost Measurement; spec M2).
3. Uncertainty-aware attainable-capability envelopes yielding equal-model-compute and equal-end-to-end-cost phase diagrams with interval-valued crossovers (Methodology §Budget-Sensitive Phase Diagrams; spec M3).
4. Robustness evaluation of oracle orderings across program families, specification conditions, candidate budgets, and a 3× GPU:CPU price-ratio perturbation (RQ5–RQ6).

## Claims Ledger

```
Claim 1: The field's efficiency claims for proof supervision exclude oracle-side cost; no prior
         work compares oracles under audited end-to-end budgets.
Evidence: Related Work per-paper efficiency-claim analysis (Intro ¶3-4; §Execution-Grounded,
         §Verifier-Guided); externally corroborated by this review's searches #1-#3, #7.
Strength: Strong — but must be softened to "no systematic, cost-normalized capability comparison
         across oracle types" per JURY-RL's one-off wall-clock table (seed's own 8th-pass
         instruction, not yet executed in the manuscript).

Claim 2: Re:Form reports no GPU-hours figure; circulating ~176/~400 GPU-h are third-party
         arithmetic on separate GPU-count and wall-clock columns.
Evidence: Introduction ¶2; revision log item 2; consistent with seed's resolved [VERIFY].
Strength: Strong (checkable against arXiv:2507.16331, verified to exist; the specific table
         reading was not independently re-verified by this review).

Claim 3: The solver-side cost of a 200k-candidate structured-VC arm is unbounded within an order
         of magnitude by anything published (~56 vs ~556 CPU-h at 0.2 s vs 2.0 s mean batch time).
Evidence: Introduction ¶2 — explicit arithmetic, labeled a planning estimate, replacement by
         measurement declared the study's purpose.
Strength: Moderate — arithmetic is transparent; the 0.2–2.0 s bracket is asserted as "plausible
         for Dafny" from documentation, not from any measured distribution.

Claim 4: The benchmark design permits attributing capability/cost differences to oracle choice.
Evidence: Blocking design (frozen artifacts, matched checkpoints, identical caps), RQ1
         equivalence check at ±1%.
Strength: Moderate — design is sound in principle; attribution inherits whatever the companion
         experiments actually froze, and the capability metric itself is not oracle-neutral (W4).

Claim 5: Per-call ledger accounting is accurate (±1%) where wall-time accounting materially
         misattributes (>5% for ≥1 oracle); full latency distributions reveal stalls mean-latency
         models miss (≥25% p95 underprediction).
Evidence: RQ3/RQ4 designs with independent meter reconciliation and train/held-out split.
Strength: Moderate — preregistered, falsifiable, well-instrumented; outcomes contingent.

Claim 6: Equal-model-compute and equal-cost budgets can select different oracles, and orderings
         may not survive a 3× price-ratio shift.
Evidence: RQ5/RQ6 designs; Phase 2 explicitly reframed as existence proof over few measured
         cells; RQ6 declared expected-underpowered.
Strength: Weak-to-Moderate as an empirical claim (honestly flagged); Strong as a formal
         possibility (the cost model makes divergence generic whenever H_cpu/H_gpu differs
         across arms).
```

## Strengths

### S1: Unusual pre-registration honesty — staging, gate, and anti-interpolation discipline
The three-phase structure (Experiments §Setup, Phases 1–3; spec M1 staging note) explicitly demotes the saturated 5×5×2×3 factorial to an aspirational Phase 3 "not claimed as executable within this paper," gates Phase 2 on instrument validation (RQ3/RQ4), reports crossovers only as bracketing intervals between measured budgets with bisection explicitly forbidden (RQ5; spec M3), and declares RQ6 expected-underpowered with the ≥80-cell bar named as Phase-3-only (RQ6; spec RQ6). The spec even distinguishes phase-dependent success criteria so a Phase-2 run cannot be misjudged by Phase-3 thresholds. This is markedly better epistemic hygiene than the field norm and directly practices the measurement discipline the paper preaches.

### S2: The gap is real, and the estimand is the right one
This review's independent literature sweep (searches #1–#3, #5, #7) confirms that no published work prices solver CPU into a training-time, cost-normalized, multi-oracle capability comparison. The nearest neighbors all miss on at least one load-bearing axis: Pareto Optimal Code Generation (arXiv:2506.10056) is test-time generate-then-rank with no proof oracles; JURY-RL (arXiv:2604.25419) reports one verifier's cache-amortized wall-clock, single oracle, no normalization; arXiv:2605.25252 varies verifier *quality* with the verifier priced at zero; arXiv:2509.21882 is a position paper on budget-matching confounds without oracle pricing; "The Verification Tax" is industry analysis without controlled comparison. The symbolic cost model C = H_gpu·p_gpu + H_cpu·p_cpu with a dated price sheet and 3× ratio sensitivity (Problem Definition; spec Metrics) is a clean, durable estimand that decouples the scientific claim (ordering robustness) from perishable dollar figures.

### S3: Related Work does constitutive anchoring, not just citation
The oracle-to-recipe table (Related Work, opening) names which published system supplies each experimental arm, declares the hybrid arm study-defined, warns that ExecVerify's two-stage structure (Stage I α=0.5 mixed reward, Stage II test-pass fraction) must be reproduced to avoid a straw-man execution arm, disambiguates Re:Form's subset reward from structured verification-condition feedback (a genuinely easy mis-attribution that would incoherate the binary-vs-structured contrast), and flags RLFR's unrefereed, formula-faithful-only status. Each related-work subsection states the specific priceable efficiency claim of its papers (e.g., RLEF's 3-samples-vs-1,000 sample reduction; ExecVerify's +3.2 pp correctly distinguished from "5.9%") rather than a boilerplate "they don't measure cost." This is reviewer-proof positioning work.

### S4: Censoring-aware latency treatment is methodologically correct
Timeouts are retained as first-class censored observations; the empirical CDF is over completed calls only; Kaplan–Meier is restricted to the identifiable pre-cap region; post-timeout completion times are never imputed; timeout mass is reported separately (Methodology §Complete Resource-Cost Measurement; spec M2). This is the correct survival-analysis treatment, and the spec encodes it as testable invariants ("Never fabricate completion times for timed-out calls") rather than prose.

## Weaknesses

### W1: The claimed deliverable depends on artifacts the paper does not control, and the framing has not caught up with the demotion
Phase 1 explicitly requires that the companion experiments (ZW1/ZW2) implement the append-only per-call ledger "added to those studies precisely so this phase is possible; without it there is nothing to instrument" (Experiments, Phase 1). Phase 2's cells are "the oracle arms, program families, and budgets the companion experiments actually run." This is a single point of failure: if companion instrumentation lands partially (wall latency but not process-tree CPU, say), RQ3 cannot be evaluated as specified, and the entire chain to RQ5/RQ6 stalls. Meanwhile the title ("Cost-Aware Phase Diagrams…"), abstract, and Contributions still foreground the phase diagrams and crossover estimation — the Phase-3 payoff — while the honestly-expected Phase-2 output is a validated instrument plus, at best, a one-cell existence proof of budget-definition divergence. **Fix**: state in the abstract that the primary claimed deliverable is the validated measurement instrument and that phase diagrams over the measured cells are the secondary deliverable; add a contingency paragraph specifying the minimum companion-ledger fields without which the study degrades to synthetic-only Phase 1, and what is still publishable in that case.

### W2: Related Work omits the neighbors the project's own scoop sweep ordered added
The seed's 2026-08-23 8th-pass note identifies three works that "must be cited and distinguished": Pareto Optimal Code Generation (arXiv:2506.10056) as the test-time analogue of the training-time question; Quantifying Empirical Compute-Supervision Tradeoffs in RLVR (arXiv:2605.25252) as motivating evidence of the verifier-priced-at-zero practice; and JURY-RL (arXiv:2604.25419), whose per-step verifier wall-clock table with cache amortization falsifies any "nobody even measures verifier wall-clock inside RL training" phrasing. None of the three appears in `paper-draft.revised.md`. The abstract's "Existing studies report capability or rollout reductions without jointly accounting for solver CPU time…" is defensible as written ("jointly" carries it), but Introduction ¶2's "the solver-side cost is not merely unmeasured but unbounded within an order of magnitude by anything published" is exactly the phrasing JURY-RL constrains — JURY-RL publishes solver-side per-step wall-clock, so "unmeasured" needs the ordered softening to "no systematic, cost-normalized comparison across oracle types." This review's own sweep additionally surfaced arXiv:2509.21882 (Position: Hidden Costs and Measurement Gaps of RLVR), which shares the paper's budget-matching thesis at the evaluation level and should be cited as independent motivation, and arXiv:2602.01523 (Relative-Budget Theory for RLVR) as a theory-side neighbor. **Fix**: add all five with one-line distinctions; re-audit the introduction's universally-quantified sentences against JURY-RL.

### W3: The Phase-1→Phase-2 gate conflates instrument validity with a contingent world-property
The gate requires (a) accurate per-call attribution (RQ3) and (b) "a censoring-aware latency model that beats a mean-latency baseline" (RQ4) (Experiments §Gate; spec M1 staging). Condition (a) is a genuine instrument-validity check. Condition (b) is not: whether the censoring-aware model beats the mean-latency baseline by ≥25% p95-stall underprediction depends on whether the observed proof-oracle workload *actually has* heavy tails or ≥5% timeout mass. If the companion runs' obligations happen to be well-conditioned (short, low-variance solves), RQ4's success criterion fails and Phase 2 is blocked — even though the ledger is accurate and phase diagrams computed from it would be perfectly trustworthy, and even though "proof oracles are not heavy-tailed here" would itself be a publishable finding that *supports* proof supervision's economics. The falsification section of the research program anticipates symmetric outcomes; the gate does not. **Fix**: split RQ4 into an instrument criterion (the censoring-aware estimator recovers known synthetic tail/timeout structure within stated error — testable on Phase 1's configurable synthetic latencies regardless of real-world tails) and a world-hypothesis (real proof regimes exhibit tails/timeouts); gate Phase 2 only on the instrument criteria (RQ3 + synthetic-recovery RQ4′).

### W4: The capability estimand is not oracle-neutral
Capability is "held-out test-suite pass rate under a fixed sampling protocol" (Problem Definition; spec Metrics). The test-outcome oracle trains directly on the currency the evaluation pays in; proof oracles train on specification satisfaction and are then graded on tests. If held-out tests and training tests are drawn from the same generative distribution (same frozen suites per task packet, disjoint splits), the test arm enjoys an objective–metric alignment advantage independent of any true capability difference; conversely, if specifications capture behavior the test distribution undersamples (the paper's own argument for proofs — "sampled tests are weak evidence" on large input spaces, seed §Predicted structure), test-based evaluation systematically underestimates proof-arm capability exactly where proof supervision should win. Either direction biases the phase diagram's winner map, and the manuscript never discusses it. **Fix**: report a secondary capability metric per cell — e.g., verifier-checked correctness against held-out *specifications*, or pass rate on adversarially/mutation-generated test augmentations disjoint from both arms' training signals — and report winner maps under both metrics; at minimum add this to threats/limitations with a directional analysis.

### W5: The hybrid arm is declared study-defined but never designed
The hybrid oracle appears as a co-equal member of 𝒪 in the formal problem definition and all six RQs, yet the only statement of its content anywhere in manuscript or spec is "Study-defined. No published system combines proof and execution rewards in a single code-RL objective" (Related Work table) and an adapter name `HybridOracle` (spec M1). No combination rule, weighting, scheduling, or cost-attribution split is given — although hybrid is precisely the arm whose cost profile (paying both solver CPU *and* execution CPU) makes it the most interesting cell of the phase diagram and the most sensitive to design choices. An arbitrary α could manufacture or erase crossovers. **Fix**: preregister the hybrid design (e.g., mirror ExecVerify's staged mixing with the structured-proof term substituted, α fixed in `configs/preregistration.yaml`), plus one ablation on the mixing weight, before any Phase-2 hybrid cell is interpreted.

### W6: Several preregistered thresholds are demanding-by-fiat with no power analysis
RQ2 requires the *lower 95% bound* of the tier–score Spearman correlation to be ≥0.8 and the improvement lower bound ≥0.2 — an extremely high bar for N = max(300, 60/family) with family stratification; RQ1's ±1% simultaneous equivalence across three quantities and all arm pairs may be unattainable purely from run-to-run GPU-hour measurement noise even under a correct harness; the 0.8 P(best) and 2 pp advantage thresholds are asserted from preregistration without justification. No power calculations appear anywhere. Failing RQ2's bar would ambiguate the entire specification-quality axis of the phase diagram. **Fix**: add a brief power/design-analysis appendix (simulate the bootstrap under plausible effect sizes and measurement noise); if ±1% or ρ≥0.8 are infeasible at planned N, revise the preregistration *now*, before data — that is what preregistration is for.

## Methodology Assessment

| Criterion | Rating (1-5) | Assessment |
|-----------|:---:|------------|
| Soundness | 4 | Blocking design, frozen artifacts, censoring-aware statistics, and monotone envelopes are all correct; docked for the gate's instrument/world conflation (W3) and the undiscussed evaluation-alignment confound (W4). |
| Novelty | 4 | The cost-normalized multi-oracle training-time comparison with solver CPU charged in is unoccupied per this review's sweep; components (Pareto/attainable envelopes, KM, preregistration) are individually standard, and test-time neighbors (arXiv:2506.10056) exist. Contribution is a measurement discipline, honestly billed as such. |
| Reproducibility | 4 | The spec is exceptionally complete: typed schemas, machine-checkable success predicates per RQ, config layout, invariants-as-asserts, ablation switches, and an explicit "Inputs You Must Provide" list. Docked because the pivotal inputs (companion runs, matched checkpoints, real corpus, hybrid design) do not ship, and sampling-protocol specifics are deferred to assumptions. |
| Experimental Design | 3 | Strong controls and diagnostic baselines (B1–B3 as negative controls is well-conceived), but Phase 2's cell count is inherited and possibly tiny, the hybrid arm is undesigned (W5), and the primary metric structurally favors one treatment arm (W4). |
| Statistical Rigor (planned) | 4 | Cluster bootstrap over tasks×seeds, simultaneous equivalence intervals, family stratification, censoring without imputation, explicit ambiguity labeling, and phase-dependent criteria are all rigorous; docked for absent power analysis and by-fiat thresholds (W6). |
| Scalability | 3 | Phase 1–2 costs are modest and honestly scoped (instrumentation overhead only); but the design the paper's question ultimately requires (Phase 3, ~hundreds of training runs at 50k–500k candidates/arm) is admitted to be beyond the study, so the method demonstrates the instrument more than it can answer the full question. |

## Questions for the Authors

1. Under equal model-compute, is GPU time that is *reserved but idle* during proof-oracle stalls charged to H_gpu? If yes, proof arms consume budget without generating candidates and the "equal candidate count" and "H_gpu ≤ B" constraints interact; if no, the equal-cost analysis under-prices stalls on reserved hardware. The ledger records `gpu_seconds_reserved` — state explicitly which analyses use reserved vs active GPU time.
2. What is the minimum set of companion-ledger fields without which Phase 1(ii) is infeasible, and what is the publication plan if the companion runs land without them (synthetic-only Phase 1)?
3. How will the hybrid oracle combine proof and execution rewards (rule, weights, schedule), and how is its per-call cost decomposed between solver CPU and execution CPU in the ledger?
4. If Phase 1 shows the real proof workloads are *not* heavy-tailed (RQ4's world-condition fails while attribution is accurate), does the gate block Phase 2? If so, why is a benign-tail finding — which would itself bear on the paper's thesis — grounds for not drawing the phase diagram?
5. The capability metric is held-out test pass rate; how do you rule out that winner maps merely reflect objective–metric alignment with the test-outcome arm rather than capability (W4)? Will a spec-checked secondary metric be reported?
6. RQ2 demands a lower 95% bound of ρ ≥ 0.8 at N = 300; what effect size and noise model make this attainable? Was any power simulation run before fixing the ±1% (RQ1) and 0.8/0.2 (RQ2) thresholds?

## Minor Issues

- Duplicate/stacked headings: "## Problem Definition" immediately followed by "## Formal Problem Definition"; "## Method Overview" then "## Methodology"; "## Experiments" then "## Experimental Setup" — collapse each pair.
- Introduction citation format renders as `Hung Le et al.. CodeRL: …` (doubled periods, no venue/id) while Related Work uses linked form — already logged in "Outstanding, not fixed here"; unify at bib time as planned.
- Notation collisions: the Problem Definition uses ρ = p_gpu/p_cpu while Methodology uses r = p_g/p_c for the same ratio; worse, spec M1 uses `r` for the *candidate budget* ("candidate budget `r` ∈ {~50k, …}") and `r0` for the price ratio in the same document — given that budget/price-ratio conflation is precisely the bug revision-log item and M3 warn against, rename the budget variable (e.g., `n`, matching the manuscript's 𝒩).
- The manuscript's Related Work cites "a recent hardware-synthesis system [[2025](https://arxiv.org/abs/2509.06239)]" with no name or authors — this is presumably Proof2Silicon, flagged in "Outstanding" as missing its authors (Jha, Wan & Chen); resolve before submission (id not included in this review's verification batch — carried as the manuscript's own outstanding item).
- Seed's 8th-pass cosmetic note says Re:Form v4's arXiv title now reads "Reducing Human **Priors**"; the arXiv export API today returns v4 titled "Reducing Human **Annotations**…". Re-check that note before executing the camera-ready sync it orders — the correction may be inverted.
- Revision log and "Outstanding, not fixed here" sections remain in the manuscript body — correctly marked "remove before submission"; ensure they are stripped, as they name internal room ids and companion-package defects.
- Abstract sentence "a first phase builds and audits the ledger against synthetic heavy-tailed latencies and existing training runs without launching new ones" is the abstract's only hint of staging; given W1, one more sentence naming the gate would make the abstract self-consistent with the demoted scope.
- Spec RQ5 emits `disagreement_fraction` only when `measured_cells >= 30`, but manuscript RQ5 preregisters the 10% fraction "for the saturated Phase 3 design" — harmonize the 30-cell spec threshold with the manuscript's phase language so neither is read as the other's contradiction.

## Literature Positioning

The manuscript's positioning against its three named literatures (execution-grounded supervision, verifier-guided synthesis, neural theorem proving) is strong and unusually specific — each subsection names the paper-specific priceable efficiency claim rather than a generic omission, and the constitutive-baseline table is exemplary (S3). The positioning is, however, one revision behind the project's own intelligence: the three neighbors identified in the 2026-08-23 scoop sweep (Pareto Optimal Code Generation, arXiv:2506.10056 — the test-time analogue; arXiv:2605.25252 — verifier-quality-vs-compute with verifier priced at zero; JURY-RL, arXiv:2604.25419 — one-off verifier wall-clock inside RLVR) are absent, and JURY-RL specifically forces a softening of the introduction's "unmeasured" universal (W2). This review's independent sweep adds two more that should be cited: **Position: The Hidden Costs and Measurement Gaps of RLVR** (arXiv:2509.21882), which independently argues that RLVR gains are overstated when budgets are unmatched — the same thesis one level up, and free supporting motivation; and **A Relative-Budget Theory for RLVR** (arXiv:2602.01523) as a theoretical treatment of budget allocation in RLVR. Industry evidence ("The Verification Tax": verification CPU as the pacing constraint, ~41k sandbox executions/step, 20,000–80,000× CPU-demand scaling moving from math to code RL) could be cited as practitioner corroboration that the CPU term the paper prices is operationally first-order. No scooping work was found: the specific claim — training-time, cost-normalized, five-oracle comparison with solver CPU charged into a symbolic-price budget, with censoring-preserved latency accounting — remains unoccupied as of 2026-08-23.

## Recommendations

**Overall Assessment**: Weak Accept — as a pre-registered measurement-study protocol (registered-report Stage 1 analogue). The gap is real and externally corroborated, the instrument design is sound and falsifiable, and the scope honesty is exemplary; the dependency risk (W1), stale related work (W2), gate design flaw (W3), and metric-alignment confound (W4) all need fixing before the protocol is frozen, but all are fixable without new data.

**Confidence**: Medium — the review verified the literature gap independently through 8 searches and 3 full fetches and read both current documents in full; it could not verify the companion experiments' specs (whose ledger requirements the study's feasibility rests on), the Re:Form table reading, or the RLFR precursor (reported by the manuscript itself as no longer available at its original URL).

**Contribution Level**: Moderate — a measurement discipline plus an instrument, honestly billed as "cheap to claim because it is layered instrumentation rather than a new training method" (seed); it would rise to Significant if Phase 2 yields even one supported budget-definition divergence, and the constrained Phase-2 cell count is what caps it today.

### Actionable Suggestions for Improvement
1. **Repair the gate (W3)**: split RQ4 into an instrument-recovery criterion evaluated on Phase 1's configurable synthetic latencies (the estimator recovers known tail/timeout structure within stated error) and a world-hypothesis about real proof regimes; gate Phase 2 only on RQ3 + the synthetic-recovery criterion, and preregister "benign tails" as a reportable supporting finding for proof-oracle economics rather than a study-blocking failure.
2. **Neutralize the capability metric (W4)**: add a preregistered secondary capability metric decoupled from both training signals — spec-checked correctness on held-out specifications and/or mutation-augmented test suites generated after training-arm freezing — and commit to reporting winner maps under both metrics with disagreements flagged, plus a threats paragraph on objective–metric alignment.
3. **Sync Related Work and soften the universal (W2)**: add arXiv:2506.10056, 2605.25252, 2604.25419, 2509.21882, and 2602.01523 with one-line distinctions; replace "not merely unmeasured but unbounded…by anything published" with the seed-ordered "no systematic, cost-normalized capability comparison across oracle types," keeping the tenfold-swing arithmetic (which survives the softening intact).
4. **Preregister the hybrid arm (W5)** — combination rule, fixed mixing weight, cost decomposition, and one mixing-weight ablation — before any hybrid cell is run or interpreted.
5. **Add a power/design appendix (W6)** simulating RQ1's ±1% equivalence and RQ2's ρ-lower-bound ≥ 0.8 under plausible noise, revising thresholds now if unattainable; and add the W1 contingency statement (minimum companion-ledger fields; synthetic-only fallback deliverable) plus an abstract sentence making the instrument the primary claimed contribution.

---

*Review limitations disclosed*: this is a pre-registration review; no results exist to audit. The companion experiments' specs (ZW1/ZW2) were not read — the feasibility of Phase 1(ii) is taken from this manuscript's own description. The Re:Form Table 2 reading and the Dafny-documentation characterization were checked for existence/plausibility but not line-verified against the source PDFs. Search coverage is bounded by 8 queries and 3 full fetches on 2026-08-23.
