> **✅ CURRENT — edited in place.** This spec carries all review corrections; there is no
> `.revised` sibling. The unedited original is upstream in
> `paper_autodiscussion/completed_jobs_dirs/<job>--<room>/experiment-spec.md`.

# Experiment Specification: The Oracle Economics of Code RL — A Cost-Normalized Phase Diagram of Execution vs. Proof Supervision

## Objective — what the experiment must establish (from the problem definition)

Build an instrumented code-RL harness and analysis pipeline that measures and compares **capability efficiency** of five reward oracles (test-outcome, execution-process, binary-proof, structured-proof, hybrid) under two distinct budget definitions:

- **Equal model-compute** (matched GPU hours `H_gpu`, matched candidate generations).
- **Equal end-to-end cost** `C = H_gpu·p_gpu + H_cpu·p_cpu` (symbolic, dated prices).

The system must produce **phase diagrams** naming the best oracle for each (program family × specification quality × candidate budget) cell under both budgets, expose **disagreements** between the two orderings, locate **crossovers**, report **complete latency/timeout distributions** (never mean-only), and test whether the equal-cost ordering **survives a 3× shift in the GPU:CPU price ratio**.

Hard constraints the implementation must respect (encode as invariants/asserts, not prose):
- Never equate "fewer executions" with "lower cost"; cost is always the measured `C`.
- Never omit solver CPU time; CPU hours are first-class ledger fields.
- Never summarize heavy-tailed latency by mean alone; always emit full CDF, median, p95, p99, timeout mass.
- Never silently raise verifier effort/limits for any arm; resource caps are frozen per-obligation and audited.
- Never treat planning estimates as measurements; all cost/latency numbers come from the ledger.
- Prices are free variables from a dated price sheet; no hard-coded dollar constants in analysis.

## Research Questions & Success Criteria — RQs with explicit, checkable success criteria

**RQ1 — Resource control / arm equivalence.**
Success: For every equal-model-compute block, simultaneous equivalence intervals for {candidate count, generated tokens, metered GPU hours} across all oracle arms lie within **±1%**; audit logs show **zero** config-deviation and **zero** resource-cap-deviation events. Checkable: `equivalence_report.pass == True`.

**RQ2 — Specification-quality validity.**
Success: Preregistered tier ranks have Spearman **ρ ≥ 0.8** (lower 95% bootstrap bound ≥ 0.8) with held-out defect-detection scores, and exceed source-only labels by **≥ 0.2** (lower bound ≥ 0.2). Checkable: `quality_validation.rho_lb >= 0.8 and quality_validation.delta_lb >= 0.2`.

**RQ3 — Ledger cost attribution accuracy.**
Success: Ledger GPU-hour and CPU-hour totals reconcile **within ±1%** of independent device/process-tree meters (interval wholly within ±1%); **≥ 1 oracle** shows wall-time accounting error with lower 95% bound **> 5%** absolute. Checkable: `reconciliation.ledger_within_1pct and reconciliation.walltime_fails_5pct_any_oracle`.

**RQ4 — Tail latency / timeout exposure.**
Success: For ≥ 1 proof-based regime, completed-call **p99/median ≥ 10** OR **timeout mass ≥ 5%**; AND its mean-latency model underpredicts empirical **p95 step stall by ≥ 25%**. Checkable: `tail_report.any_regime_meets_tail and tail_report.mean_model_underpredicts_p95_by_25pct`.

**RQ5 — Budget-dependent ordering / crossovers.**
Success **depends on phase**. *Phase 2 (what this study runs):* at least one **measured** cell shows different equal-GPU vs equal-cost winners, that winner carrying bootstrap **P(best) ≥ 0.8** and held-out advantage **≥ 2 pp** over the runner-up — an existence proof that the two budget definitions can diverge, which is the claim of interest. A fraction over a handful of cells is not a meaningful rate and must not be reported as one. *Phase 3 (saturated, aspirational):* **≥ 10%** of cells disagree. Checkable: `phase_report.disagreeing_cells >= 1` and `phase_report.measured_cells` reported alongside; `disagreement_fraction` emitted **only** when `measured_cells >= 30`.

**RQ6 — Price-ratio robustness.**
Success **depends on phase**, exactly as for RQ5. *Phase 2 (what this study runs):* the retention fraction is computed over the few measured eligible cells and reported **with the underpowered flag set** — the honest deliverable is the observed direction of any instability, not a robustness verdict. A Phase 2 run must NOT be treated as a failure for having fewer than 80 eligible cells; the `n_eligible >= 80` requirement belongs to Phase 3. *Phase 3 (aspirational):* among cells with P(best) ≥ 0.8 at `r0`, **≥ 75%** retain the same equal-cost winner at both `r0/3` and `3·r0` with P(best) ≥ 0.8, over **≥ 80 eligible cells**. Checkable: `robustness_report.underpowered == (robustness_report.n_eligible < 80)` in Phase 2; `robustness_report.retention_fraction >= 0.75 and robustness_report.n_eligible >= 80` in Phase 3.

## Methods to Implement — the components/algorithms to build (from method design)

### M1. Preregistered Factorial Blocking + Oracle Evaluation Contract (OEC)

> **Staging (read before implementing).** The saturated five-oracle × five-family × two-spec-source ×
> three-budget factorial described below is the **Phase 3 aspiration**, not what this study runs.
> **Phase 1** builds and audits the ledger and OEC against synthetic heavy-tailed latencies and the
> companion experiments' existing runs — **no new training runs**. A **gate** then requires accurate
> per-call attribution (RQ3) and a censoring-aware latency model that beats the mean-latency baseline
> (RQ4). **Phase 2** computes phase diagrams over only the cells the companion experiments actually
> execute. Implement Phase 1 first; do not provision the saturated grid without an explicit decision
> to fund it.
- **Factor axes** (config-driven enums): program family ∈ {straight_line, linear_loop, nonlinear_arith, arrays_aliasing, recursion}; spec source ∈ {human_fixed, model_generated}; quality tier ∈ {high, medium, low} defined by **controlled defect injection** (see M1a); candidate budget `r` ∈ {~50k, ~200k, ~500k}.
- **Matched-checkpoint runner**: all oracle arms start from the same checkpoint, identical candidate counts, decoding limits, update schedules, and seeds. Only the reward adapter differs.
- **Oracle Evaluation Contract**: a stable interface `OracleAdapter.evaluate(task_packet, candidate) -> RewardResult`. Adapters: `TestOutcomeOracle`, `ExecutionProcessOracle`, `BinaryProofOracle`, `StructuredProofOracle`, `HybridOracle`. Each wraps **frozen artifacts** (frozen test suites, frozen solver binaries, fixed solver flags, fixed resource caps). Adapters must not mutate caps at runtime.
- **M1a. Quality-tier construction**: inject calibrated specification defects (e.g., weakened preconditions, dropped conjuncts, off-by-one bounds, missing frame conditions) at controlled densities per tier. Calibrate tiers **before training** against (i) held-out semantic mutants and (ii) blind expert ratings; store the mapping in a preregistration file.

### M2. Event-Sourced Resource Ledger
- **Append-only ledger** capturing per OEC call: `obligation_id`, `oracle_type`, `cpu_seconds_process_tree`, `gpu_seconds_reserved`, `wall_latency_s`, `retries`, `cache_hit`, `parallelism_degree`, `termination_cause` ∈ {completed, timeout, error, killed}, `timeout_cap_s`, `resource_cap`, timestamps, `seed`, `cell_id`.
- **Cost function**: `C = sum(gpu_seconds)/3600·p_gpu + sum(cpu_seconds)/3600·p_cpu` with symbolic prices injected at analysis time.
- **Censoring-aware latency stats**: empirical CDF over **completed calls only**; Kaplan–Meier survival **only over the identifiable pre-cap region**; explicit **timeout mass**; tail bounds **without imputing** post-timeout completion times. Never fabricate completion times for timed-out calls.
- **Reconciliation meters**: independent GPU device telemetry sampler and OS process-tree CPU meter, compared to ledger sums.

### M3. Cross-Fitted Attainable-Capability Envelopes + Phase Diagram
- **Capability metric**: held-out test-suite pass rate under a fixed sampling protocol (see Metrics).
- **Envelope construction** per cell (family × source × quality × budget): checkpoint selection on validation data, evaluation on held-out tasks, **cluster bootstrap over tasks and seeds**. Retain best checkpoint satisfying `H_gpu ≤ B` (equal-GPU) or `C(r) ≤ B` (equal-cost). Envelopes are **monotone** in budget by construction (a larger budget may reuse any cheaper checkpoint) → enforce monotone non-decreasing envelope in code.
- **Price-ratio grid** (NOT a budget grid): evaluate cost orderings at GPU:CPU price ratios `r0/3, r0, 3·r0`. The separate **candidate-budget** axis is `{50k, 200k, 500k}` measured budgets. **Do NOT interpolate between measured budgets.** Report the envelope only at budgets actually run; a log-spaced interpolation grid would manufacture capability values that were never observed, and the manuscript commits to reporting unmeasured cells as unobserved.
- **Winner declaration**: winner only when bootstrap **P(best) ≥ 0.8**; else mark cell **ambiguous**.
- **Crossover estimation**: from envelope intersections at **measured budgets only**. Where the winner changes between two adjacent measured budgets, report that **bracketing interval** as the crossover. **Do NOT bisect** — bisection requires evaluating capability at budgets between the measured ones, which is the interpolation forbidden above. Narrowing a crossover means measuring more budgets, not modelling between them. Report the bootstrap distribution over which interval contains the crossover, not a point estimate.

## Baselines to Implement — comparison methods and why each is included

- **B1. Source-Only Quality Labels** — labels derived purely from spec provenance (human vs model). Purpose: RQ2 sanity check that tiers carry information *beyond* source. Not an effectiveness baseline.
- **B2. Naive Job-Wall-Time Accounting** — attributes cost using job wall-clock time instead of per-obligation metered hours. Purpose: RQ3 negative control; expected to fail (>5% error) under idle/concurrency/overlap.
- **B3. Mean-Latency Stall Model** — predicts training-step stall from mean completed latency only. Purpose: RQ4 negative control; expected to underpredict p95 stall in proof regimes.

## Datasets — how to load or construct inputs (interfaces/format, not the data itself)

**D1. Controlled Multi-Oracle Factorial Benchmark.**
- Interface: `load_task_packets(family, source, quality, seed) -> List[TaskPacket]`.
- `TaskPacket` schema: `task_id`, `program_family`, `spec_source`, `quality_tier`, `prompt`, `frozen_test_suite_ref`, `spec_artifact_ref`, `solver_config_ref`, `held_out_test_ref`, `seed`. Task seeds are **shared across oracle arms**.
- Provide a **synthetic generator** stub if real task corpus unavailable (record as assumption): parametric program templates per family + defect-injected specs.

**D2. Blinded Specification-Defect Validation Set.**
- Interface: `load_defect_challenges() -> List[DefectChallenge]` with `challenge_id`, `spec_ref`, `injected_defect_type`, `is_defective`, `family`. **Disjoint** from tier-assignment data; loaded only at RQ2 evaluation time (gate via a "sealed" flag). Balanced: N = max(300, 60 per family).

**D3. Metered Oracle Execution and Stall Traces.**
- Not loaded — **produced** by the harness. Interface: the ledger DB (append-only). Provide `load_ledger(filter) -> DataFrame` and `load_step_stalls(regime) -> DataFrame` (per integrated training-step stall).

All dataset loaders return typed records; the spec assumes **no real data ships** — implement loaders + synthetic fallbacks and mark data provisioning under "Inputs You Must Provide".

## Metrics — the measures to implement, with precise definitions / formulas

- **Capability** = held-out test-suite pass rate = (# held-out tests passed) / (# held-out tests), under a fixed sampling protocol (fixed k, temperature, max tokens); report pass@1 and pass@k as configured.
- **Cost** `C = (Σ gpu_seconds/3600)·p_gpu + (Σ cpu_seconds/3600)·p_cpu`.
- **Equivalence (RQ1)**: relative range `= (max−min)/mean` and all pairwise diffs for {candidate_count, generated_tokens, gpu_hours}; simultaneous equivalence intervals (e.g., Bonferroni/simultaneous CIs across arms) must lie within ±1%. Deviation counts from audit log.
- **Quality validity (RQ2)**: Spearman ρ(tier_rank, defect_detection_score); Δρ = ρ(tier) − ρ(source_only); family-stratified bootstrap 95% CIs (lower bounds).
- **Reconciliation (RQ3)**: `abs_err = |ledger − meter|`, `rel_err = abs_err/meter` for GPU and CPU hours, per oracle × concurrency × accounting method.
- **Latency/tail (RQ4)**: empirical CDF (completed calls); median, p95, p99; **p99/median ratio**; **timeout mass** = (#timeout)/(#calls); KM curve over pre-cap region; empirical **p95 training-step stall**; mean-baseline underprediction `= (emp_p95 − mean_pred_p95)/emp_p95`.
- **Phase/ordering (RQ5)**: capability at matched budget; **P(best)** = bootstrap fraction where oracle is top; winner−runner-up difference (pp); disagreement fraction across cells; crossover (budget, cost) coordinates.
- **Robustness (RQ6)**: winner and P(best) at r0/3, r0, 3·r0; joint retention indicator; retention fraction among eligible cells; price-ratio crossover locations.

## Implementation Plan — ordered, concrete coding tasks the agent should perform

1. **Repo scaffold**: package `oracle_econ/` with subpackages `harness/`, `oracles/`, `ledger/`, `data/`, `analysis/`, `configs/`, `scripts/`, `tests/`. Add `pyproject.toml`, pinned deps.
2. **Config system** (`configs/`): YAML for factor axes, seeds, resource caps, timeout caps, sampling protocol, **price-ratio grid** `{r0/3, r0, 3r0}` — these are GPU:CPU price ratios for the cost-sensitivity analysis, **not** candidate budgets; the candidate-budget axis is `{50k, 200k, 500k}` and the two must not be conflated (no log/interpolation grid on either — see M1), and `price_sheet.yaml` (dated `p_gpu`, `p_cpu`, `r0` ratio).
3. **Data layer** (`data/`): implement `TaskPacket`, `DefectChallenge` schemas + loaders + synthetic generators + sealed-set gating for D2.
4. **Ledger** (`ledger/`): append-only store (SQLite/Parquet); `LedgerWriter.record(event)`; `GpuMeter`, `ProcessTreeCpuMeter`; context manager `measured_call(obligation_id, oracle_type, caps)` that populates all fields including `termination_cause` and `timeout_cap_s`. Assert caps immutable per obligation.
5. **Oracle adapters** (`oracles/`): implement OEC interface + 5 adapters wrapping frozen artifacts and fixed solver configs. Route **every** call through `measured_call`. Enforce per-obligation resource/time caps; on cap breach set `termination_cause=timeout` and do **not** impute completion.
6. **RL harness** (`harness/`): matched-checkpoint runner producing candidates; identical decoding/update/seed across arms; audit logger emitting config-deviation and cap-deviation events. Integrate step-stall measurement (record per-step stall attributable to oracle latency).
7. **RQ1 analysis** (`analysis/equivalence.py`): compute simultaneous equivalence intervals + deviation counts → `equivalence_report`.
8. **RQ2 analysis** (`analysis/quality_validation.py`): Spearman + Δ vs source-only + family-stratified bootstrap → `quality_validation`.
9. **RQ3 analysis** (`analysis/reconciliation.py`): ledger vs meters vs wall-time, per oracle/concurrency → `reconciliation`.
10. **RQ4 analysis** (`analysis/tail_latency.py`): CDF, quantiles, timeout mass, KM (pre-cap), train/eval split for mean-latency baseline, stall underprediction → `tail_report`.
11. **Envelopes + phase diagram** (`analysis/envelopes.py`, `analysis/phase.py`): cross-fitted monotone envelopes evaluated ONLY at measured budgets, equal-GPU & equal-cost frontiers, cluster bootstrap `P(best)`, winner/ambiguous labeling, crossover **interval** identification (no bisection — see M3) → `phase_report`.
12. **RQ6 robustness** (`analysis/price_robustness.py`): reprice at r0/3, r0, 3r0; retention among eligible; underpower flag → `robustness_report`.
13. **Phase-diagram plotting** (`analysis/plots.py`): grid heatmaps of winners per budget; disagreement overlays; latency CDFs; KM curves; crossover maps.
14. **Orchestration scripts** (`scripts/`): `run_experiment.py`, `run_rq{1..6}.py`, `build_phase_diagram.py`, each reading configs and writing JSON reports + figures.
15. **Tests** (`tests/`): unit tests for ledger accuracy on synthetic workloads, monotone-envelope invariant, cost formula, censoring (no imputation), and each report's success-criterion computation.

## Ablations — variants to build as configurable switches, and what each isolates

- **`accounting_method` ∈ {ledger, wall_time}** — isolates attribution error (RQ3).
- **`latency_model` ∈ {empirical, mean_only}** — isolates tail loss (RQ4).
- **`quality_labeling` ∈ {tier, source_only}** — isolates quality information beyond provenance (RQ2).
- **`budget_definition` ∈ {equal_gpu, equal_cost}** — isolates ordering disagreement (RQ5).
- **`price_ratio` ∈ {r0/3, r0, 3r0}** — isolates price robustness (RQ6).
- **`oracle_type` ∈ {test, exec_process, binary_proof, structured_proof, hybrid}** — the primary treatment switch.
- **`candidate_budget` ∈ {50k, 200k, 500k}** — isolates budget-dependence. (The `interpolation_grid` switch is removed: crossovers are reported as intervals between adjacent measured budgets, so resolution is set by which budgets were run, not by an interpolation setting.)
- **`concurrency_level` ∈ {low, med, high}** — stresses ledger attribution under overlap.

## Expected Artifacts — the code modules, scripts, and config files that should exist when done

- Modules: `oracle_econ/{harness,oracles,ledger,data,analysis}/*.py` as enumerated above.
- Configs: `configs/factors.yaml`, `configs/caps.yaml`, `configs/sampling.yaml`, `configs/budgets.yaml`, `configs/price_sheet.yaml` (dated), `configs/preregistration.yaml` (tier mapping, RQ thresholds, N per RQ).
- Scripts: `scripts/run_experiment.py`, `scripts/run_rq1..rq6.py`, `scripts/build_phase_diagram.py`.
- Reports (JSON): `equivalence_report`, `quality_validation`, `reconciliation`, `tail_report`, `phase_report`, `robustness_report`.
- Figures: equal-GPU and equal-cost phase diagrams, disagreement overlay, latency CDFs + KM curves, crossover maps.
- Ledger store (Parquet/SQLite) + `load_ledger`/`load_step_stalls` accessors.
- `tests/` suite; `README` describing run order (only if requested — do not auto-create docs beyond required).

## Inputs You Must Provide (when you run) — external things the student must supply to actually run it later

- **Base model + RL training stack** (policy, optimizer, decoding) and matched checkpoints per cell.
- **Real task corpus** for the 5 program families with frozen test suites and held-out test suites (or accept synthetic generators).
- **Specifications**: human-authored fixed and model-generated specs, plus the calibration set (semantic mutants + blind expert ratings) for tier assignment.
- **Blinded defect-challenge set** (D2), sealed until RQ2.
- **Solvers/verifiers** (SMT/proof assistants) with fixed configs and frozen binaries; licenses if any.
- **Compute**: GPUs for generation/eval and CPUs for solvers, at the target candidate budgets (~50k/200k/500k per arm); telemetry access for GPU device meters.
- **Dated price sheet**: `p_gpu`, `p_cpu`, and baseline ratio `r0`.
- **Ground truth**: held-out test labels and defect labels.
- **Dependencies**: RL framework, bootstrap/stats libs, lifelines (or KM implementation), plotting libs, Parquet/SQLite drivers.

## Open Decisions / Assumptions — gaps left underspecified by the plan + the assumptions made

- **No real data/model ships**: implement synthetic task/spec generators and mock oracle latencies so the pipeline and all six reports are executable end-to-end; swap in real components later. (Assumption.)
- **Sampling protocol specifics** (k, temperature, max tokens for capability) are set in `configs/sampling.yaml`; default pass@1 with fixed k reported. (Assumption.)
- **Resource-cap values** (timeout_cap_s, memory, CPU cores per obligation) are placeholders in `configs/caps.yaml`, frozen per obligation and identical across arms. (Assumption.)
- **Defect taxonomy and per-tier injection densities** are assumed (weakened pre/postconditions, dropped conjuncts, off-by-one, missing frame conditions); calibrate against provided mutants/ratings. (Assumption.)
- **Bootstrap details**: cluster bootstrap over (task, seed); default 1000 resamples; P(best) threshold 0.8 and advantage 2 pp from preregistration. (Assumption where unspecified.)
- **Envelope monotonicity** enforced by taking the running max over measured budgets. **No interpolation between them.** A crossover is reported as the interval between the two adjacent measured budgets that bracket the winner change; a point estimate would require either additional measured budgets or an explicitly justified parametric model, and this study commits to neither. (Constraint, not assumption.)
- **KM implementation**: use a standard estimator restricted to the pre-cap region; timeouts treated as right-censored, never imputed. (Assumption consistent with constraints.)
- **"GPU-hour ≤ B" vs "H_gpu ≤ B"** treated as equivalent equal-model-compute constraint; budget `B` grid derived from candidate budgets. (Assumption.)
- **Step-stall attribution**: per training-step stall measured as wall time blocked awaiting oracle results; exact integration point depends on the RL loop and is left as a harness hook. (Assumption.)
