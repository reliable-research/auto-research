> **✅ CURRENT — edited in place.** This spec carries all review corrections; there is no
> `.revised` sibling. The unedited original is upstream in
> `paper_autodiscussion/completed_jobs_dirs/<job>--<room>/experiment-spec.md`.

# Experiment Specification: Which Prover Teaches Software? Math-Proof vs. Program-Verification Post-Training Transfer

## Objective — what the experiment must establish (from the problem definition)

Build the code to measure **relative transfer** (not absolute theorem-proving strength) from two kinds of formal post-training — Lean mathematical-proof supervision vs. Dafny-style program-verification supervision — onto software capability, at small scale (0.6B–1.7B), from a **single shared checkpoint**, under **genuinely matched training budgets**.

The harness must:
1. Train several SFT arms (Lean, Dafny, matched non-formal control, curriculum variants, single-branch) from one shared checkpoint under a **shared Budget Ledger** that hard-matches four axes: sampled candidates `N`, checker-accepted trajectories `K`, loss-bearing tokens `T`, optimizer updates `S`.
2. Evaluate every arm on a **frozen Paired Evaluation Panel** spanning six outcome families: formal math + {code generation, execution reasoning, invariant inference, semantic equivalence, program repair}.
3. Produce a **branch-by-outcome transfer matrix** of paired win-minus-loss effects `W`, with a **predeclared math positive-control gate**: the Lean arm must beat the non-formal control on formal math before software-family results may be interpreted confirmatorily.
4. Answer whether a **math-proof→program-proof curriculum** beats either branch alone and whether the effect is **order-driven** (vs. Dafny→Lean / interleaved).

The deliverable is code + configs + analysis scripts. This spec does NOT require the agent to run training; it requires the agent to make the harness runnable and correct.

## Research Questions & Success Criteria — RQs with explicit, checkable success criteria

Let `W = P(arm_score > control_score) − P(arm_score < control_score)` (paired win-minus-loss), computed per-prompt as +1 win / −1 loss / 0 tie, then averaged. All CIs are **seed-cluster-robust** (few-cluster procedures; training seed is part of the estimand).

- **RQ1 — Budget normalization completeness.** Run all six arms under (a) normalization-complete and (b) equal-update-only scheduling, 8 seeds/arm/scheduler (**96 runs**). Success: max pairwise relative imbalance over `{N,K,T,S}` ≤ **0.01** for the normalized scheduler, AND normalized imbalance ≤ **20%** of the equal-update-only imbalance (joint one-sided bootstrap bound).
- **RQ2 — Replay-exposure robustness (training-time intervention; NOT post-hoc weighting).** Each of the six arms is trained **twice** — once under the `natural` replay regime and once under `flattened` — with 8 paired seeds, giving 12 training conditions and 96 runs, evaluated on the frozen **4,200-prompt** panel (700/family × 6). Success: for every arm and outcome family, the flattened-minus-natural contrast `mu_j(theta_flat) − mu_j(theta_natural)` falls inside the preregistered equivalence margin, with multiplicity-adjusted tests (clustered by prompt AND seed) passing. **Do not implement any post-hoc reweighting of a trained checkpoint's held-out outputs**: weights over training examples cannot change a frozen model's held-out behaviour, so a weighted-vs-unweighted comparison is identical by construction and its equivalence test cannot fail.
- **RQ3 — Math positive-control gate.** Lean vs. matched non-formal SFT, **12 paired seeds**, evaluated on **2,500** contamination-screened, dependency-disjoint Lean tasks. Success (GATE): point `W ≥ 0.10` AND one-sided 95% lower bound `> 0.05`. **If this fails, stop confirmatory analysis; label the matrix "diagnostic".**
- **RQ4 — Transfer matrix (conditional on RQ3).** Lean, Dafny, non-formal, 12 seeds, disjoint **4,000-prompt** panel (800/family × 5). Report per-family Dafny−control, Lean−control, Dafny−Lean, plus equal-weight aggregate Dafny−Lean. Success: aggregate Dafny−Lean `W ≥ 0.05` and significantly positive; every family-level contrast reported with sign + simultaneous interval.
- **RQ5 — Curriculum benefit vs. best comparator (conditional on RQ3).** Lean→Dafny, Lean-only, Dafny-only, non-formal, 12 seeds, disjoint **4,000-prompt** panel. Success: each of the three curriculum-minus-comparator contrasts `≥ 0.05` (so min `≥ 0.05`), every simultaneous lower bound `> 0`; per-family decomposition reported.
- **RQ6 — Order sensitivity (conditional on RQ3).** Lean→Dafny, Dafny→Lean, interleaved, 12 seeds, disjoint **9,000-prompt** panel (1,800/family × 5). Success: Lean→Dafny `W ≥ 0.03` vs. each alternative, both adjusted tests reject non-positive transfer; per-family breakdown reported.

## Methods to Implement — the components/algorithms to build (from method design)

### M1: Budget Ledger + budget-matched SFT trainer
- **Budget Ledger** (`BudgetLedger`): written once per training step from trainer's data loader + sampler state. Records per-arm cumulative and per-step: `N` sampled candidates, `K` unique validator-accepted trajectories, `T` loss-bearing tokens, `S` optimizer updates, and per-example replay counts + empirical replay probability `p_i = (selection count of example i) / (total selections)`.
- **Candidate sampling → checking → acceptance**: each arm samples `N` candidates, runs the arm's **checker** (Lean kernel / Dafny verifier / non-formal verified-response check), retains `K` checker-passing trajectories, **stratified** by (base-model success-propensity bin, length bin).
- **Deterministic packing & replay**: pack accepted trajectories to supply **exactly `T`** loss-bearing tokens over **exactly `S`** updates; replay (repeat) examples deterministically when accepted-token supply < T. Same **uninterrupted optimizer-state policy** across arms.
- **Budget intersection solver** (`solve_common_budget`): fix `(N,K,T,S)` at the largest common feasible intersection across arms, estimated on a disjoint **blinded pilot**. Checkers defined ex ante.
- Report **acceptance yield** (`K/N`) and **replay multiplicity** (mean replays/example) per arm.

### M2: Paired win-minus-loss estimator + gated confirmatory analysis
- `paired_W(arm_scores, control_scores)` → per-prompt {+1,−1,0}, mean over prompts; **equal benchmark weights within families**, equal family weights in aggregates.
- **Item-by-seed stratified bootstrap** for intervals; **seed-cluster-robust** few-cluster procedures (e.g., wild cluster bootstrap) for cross-run inference.
- **Gate controller** (`GateController`): computes RQ3 one-sided 95% lower bound; only if `> 0.05` does it unlock RQ4–RQ6 confirmatory endpoints. Otherwise emits `status="diagnostic"` and blocks confirmatory labels.
- **Flattened replay scheduler** (`flatten_replay`): cap each accepted trajectory's replay multiplicity at the arm's median, then **deterministically redistribute** the freed slots so total exposure is unchanged — round-robin over trajectories whose multiplicity is strictly below the cap, in canonical order (ascending current multiplicity, ties by trajectory id), repeating until all freed slots are placed or every trajectory reaches the cap; place any residual by continuing the same round-robin with the cap lifted by one, and record the residual count. The rule is performance-independent and seed-deterministic. Loss-bearing tokens, optimizer updates, sampled candidates, and accepted-trajectory totals must be **identical** to the `natural` regime — assert this in the ledger before training starts.
- **REMOVED — `hajek_reweight`.** An earlier version of this spec mandated Hájek stabilized inverse-replay weights (`w_i = p_bar / p_i`, truncated and normalized) "transported to the eval estimand by reweighting the arm's accepted-trajectory training distribution." **Do not implement it.** The weights index training examples while the estimand is a mean over held-out prompts of an already-frozen checkpoint; no channel connects them, so weighted and unweighted estimates coincide identically and the equivalence test cannot fail. Replay robustness is a property of the training pipeline and is testable only by changing what training sees (see `flatten_replay`).

### M3: Curriculum controller
- Arms: `Lean→Dafny`, `Dafny→Lean`, `interleaved(Lean+Dafny)` (minibatch-interleaved), plus segmented `Lean-only`, `Dafny-only`, `non-formal`.
- **Equal source quotas**: each half receives `T/2` tokens, `S/2` updates, `N/2` samples, `K/2` accepted trajectories; same uninterrupted optimizer-state policy. Reverse + interleaved hold source exposure fixed → contrasts isolate **ordering**, not mixture.

## Baselines to Implement — comparison methods and why each is included

1. **Matched non-formal SFT** — generic verified-response supervised control matching the full four-axis budget; the shared reference arm for the entire transfer matrix.
2. **Equal-update-only scheduling** — matches only `S`; used in RQ1 to demonstrate residual `N/K/T` imbalance.
3. **Shared checkpoint without post-training** (zero-exposure anchor) — detects trivial or sign-inverted transfer estimates.
4. **Single-branch arms** (Lean-only, Dafny-only) — identify whether curriculum effect requires both branches.
5. **Reverse + interleaved curricula** (Dafny→Lean, interleaved) — hold branch exposure fixed, isolate order sensitivity.

## Datasets — how to load or construct inputs (interfaces/format, not the data itself)

All datasets loaded through a common interface; the harness must not embed the data. Use **manifests** (JSON/YAML) recording source name, commit/release hash, extraction date, dedup parameters, and split assignment.

### Training pools (loader interfaces, not shipped data)
- `LeanProofPool` — Lean/mathlib theorem+proof items; each item exposes `statement`, `proof`, `imports/dependency graph`. Checked by Lean kernel.
- `DafnyVerificationPool` — program-verification items representing **states, transitions, contracts, invariants, frame conditions, verification conditions**; each exposes program text + spec. Checked by the Dafny verifier.
- `NonFormalSFTPool` — matched non-formal verified-response items with an ex-ante acceptance check.

Each pool implements:
```python
class TrainingPool(Protocol):
    def sample_candidates(self, n: int, rng) -> list[Candidate]: ...
    def check(self, cand: Candidate) -> CheckResult:  # pass/fail + metadata
    def strata(self, cand: Candidate) -> tuple[int, int]:  # (success_propensity_bin, length_bin)
```

### Evaluation panels (frozen, oracle-checked)
- **D1 Budget & Replay Ledger** — not external data; produced by the trainer (see M1). Sole input to RQ2 weights.
- **D2 Formal-Math Positive-Control Panel** — contamination-screened (normalized 13-gram fingerprint dedup against training pool + pretraining shards; whitespace/identifier canonicalized), **dependency-disjoint** (partition on Lean import graph so no eval theorem imports/is-imported-by any training theorem), exact-hash deduped. Pinned Lean/mathlib release tag in manifest. Oracle = Lean kernel proof acceptance.
- **D3 Paired Software-Family Panel** — 5 families, balanced; pinned versioned snapshots; exact-hash + MinHash (Jaccard ≥ 0.8) dedup within/across families; **every prompt carries an executable/verifiable oracle**.
- **D4 Curriculum-Order Panel** — frozen disjoint software-family splits with external oracles.

### Panel split/partition (frozen, version-pinned)
Implement `partition_panels(prompt_id, seed) -> panel ∈ {RQ4, RQ5, RQ6}` via a fixed hash-based function seeded once and frozen in the manifest, guaranteeing **disjointness across RQ4/RQ5/RQ6 panels**. Frozen split file records prompt IDs, family labels, oracle references; version-pinned so all arms/seeds see identical non-overlapping sets.

**Per-RQ panel sizes** (implement as config-driven samplers over D2/D3/D4):
- RQ2: 4,200 = 700 × {formal-math + 5 software families}.
- RQ3: 2,500 (formal math).
- RQ4: 4,000 = 800 × 5 software families.
- RQ5: 4,000 = 800 × 5 (disjoint from RQ4).
- RQ6: 9,000 = 1,800 × 5 (disjoint from RQ4, RQ5).

## Metrics — the measures to implement, with precise definitions / formulas

- **Paired win-minus-loss** `W`: per prompt `p`, `w_p = sign(score_arm(p) − score_control(p)) ∈ {+1,0,−1}`; `W = mean_p w_p`. Equal weights within family; equal-weight family aggregate = mean over 5 (or 6) family `W` values.
- **Budget imbalance** (RQ1): for quantity `Q ∈ {N,K,T,S}`, `imb_Q = max_{i,j} |Q_i − Q_j| / mean(Q_i, Q_j)`; overall = `max_Q imb_Q`; scheduler ratio = `imb_normalized / imb_equal_update_only`.
- **Replay-exposure sensitivity** (RQ2): per arm `a` and outcome family `j`, `Δ = mu_j(theta_a_flat) − mu_j(theta_a_natural)` computed from **two separately trained checkpoints**; success `|Δ|` within the preregistered equivalence margin; TOST-style simultaneous equivalence clustered by prompt and seed. **Not** a weighted-vs-unweighted re-analysis of one checkpoint — that comparison is identical by construction (see the REMOVED `hajek_reweight` note).
- **Acceptance yield** = `K/N`; **replay multiplicity** = mean per-example replay count.
- **Family-level contrasts** (RQ4): Dafny−control, Lean−control, Dafny−Lean per family; aggregate Dafny−Lean = equal-weight mean of 5 family Dafny−Lean values.
- **Curriculum vs. best comparator** (RQ5): three contrasts (Lean→Dafny minus {Lean-only, Dafny-only, non-formal}); score = **minimum** of the three; simultaneous seed-cluster lower bounds.
- **Order sensitivity** (RQ6): Lean→Dafny minus Dafny→Lean; Lean→Dafny minus interleaved; both aggregate + per-family.
- **Intervals**: item-by-seed stratified bootstrap; seed-cluster-robust (few-cluster) simultaneous CIs across families/contrasts (multiplicity-adjusted).

## Implementation Plan — ordered, concrete coding tasks the agent should perform

1. **Repo scaffold.** Create package `provers_transfer/` with modules: `ledger.py`, `pools.py`, `checkers.py`, `trainer.py`, `budget.py`, `curriculum.py`, `panels.py`, `metrics.py`, `stats.py`, `gate.py`, `analysis.py`, `config.py`. Add `configs/`, `scripts/`, `manifests/`, `tests/`.
2. **Config system** (`config.py`): dataclasses / YAML for arm definitions, `(N,K,T,S)`, seeds, scheduler mode (`normalization_complete` | `equal_update_only`), panel selection, decoding budget, dedup params. Add `configs/arms/*.yaml` for each arm and `configs/rq{1..6}.yaml`.
3. **Checkers** (`checkers.py`): pluggable `LeanChecker`, `DafnyChecker`, `NonFormalChecker`, each returning pass/fail + metadata. Define **ex ante** and pin tool versions. Stub external tool calls behind a `CheckerBackend` interface so the harness is testable without the tools installed.
4. **Training pools** (`pools.py`): implement `TrainingPool` protocol with candidate sampling, stratification bins (success-propensity × length), and dependency-graph accessors for Lean.
5. **Budget Ledger** (`ledger.py`): `BudgetLedger` with per-step append, per-example replay counts, `p_i`, `p_bar`, yield, replay multiplicity; serialize to Parquet/JSONL per run.
6. **Budget solver** (`budget.py`): `solve_common_budget(pilot_stats) -> (N,K,T,S)`; run on **disjoint blinded pilot**; deterministic packing + replay to hit exact `T`,`S`; both scheduler modes.
7. **Trainer** (`trainer.py`): budget-matched SFT loop from shared checkpoint; sampling→checking→stratified acceptance→packing→replay→updates; writes ledger each step; uninterrupted optimizer-state policy; supports single-branch and curriculum splits (`T/2,S/2,N/2,K/2` halves).
8. **Curriculum controller** (`curriculum.py`): `Lean→Dafny`, `Dafny→Lean`, `interleaved`; enforce equal source quotas; expose ordering as the only systematic difference.
9. **Panels** (`panels.py`): loaders for D2/D3/D4; contamination screen (13-gram normalized fingerprint), dependency-disjoint partition, exact-hash + MinHash dedup, `partition_panels` frozen split; oracle runners (execution / verifier / equivalence / repair-test).
10. **Metrics** (`metrics.py`): `paired_W`, budget imbalance, yield, replay multiplicity, family aggregation.
11. **Stats** (`stats.py`): item-by-seed stratified bootstrap; wild cluster bootstrap / few-cluster robust CIs; simultaneous multiplicity adjustment; TOST equivalence tests (RQ2); one-sided lower bounds (RQ3/RQ5/RQ6).
12. **Gate** (`gate.py`): `GateController` computing RQ3 bound and unlocking/blocking confirmatory endpoints; emits `diagnostic` label on failure.
13. **RQ drivers** (`scripts/run_rqN.py`, N=1..6): orchestrate arms×seeds, evaluate on the correct panel, compute metrics + intervals, check success criteria, write `results/rqN/`.
14. **Analysis + matrix report** (`analysis.py`, `scripts/build_transfer_matrix.py`): assemble branch-by-outcome `W` matrix with per-family signs/intervals; render Markdown/CSV report; **enforce the gate before printing confirmatory matrix**.
15. **Tests** (`tests/`): unit tests for `paired_W`, budget imbalance math, `flatten_replay` (cap respected, freed slots fully redistributed, per-arm exposure totals identical to `natural`, determinism under fixed seed), packing hits exact `T`/`S`, dedup/partition disjointness, gate blocking behavior; small synthetic end-to-end run with stubbed checkers/oracles.
16. **Reproducibility**: seed management (scheduling + training seeds), manifest hashing, run-config snapshotting.

## Ablations — variants to build as configurable switches, and what each isolates

- `scheduler_mode = normalization_complete | equal_update_only` — isolates value of full four-axis matching (RQ1).
- `replay_regime = natural | flattened` — isolates the replay-exposure confound (RQ2). This is a **training-time** switch selecting which scheduler builds the run; it is not a post-hoc analysis option, and both settings require their own training run.
- `curriculum_order = lean_dafny | dafny_lean | interleaved | lean_only | dafny_only | none` — isolates ordering vs. mixture vs. single-branch (RQ5/RQ6).
- `post_training = on | off` — zero-exposure anchor.
- `flatten_cap_quantile` — sensitivity of the flattening cap (median vs. 40th/60th percentile), re-trained per setting; this is a training-time ablation, not a re-analysis.
- `family_weighting = equal | native` — confirm equal-weight aggregation is what's reported.
- `bootstrap = item_by_seed | seed_cluster` — inference-procedure sensitivity.

## Expected Artifacts — the code modules, scripts, and config files that should exist when done

- Modules: `provers_transfer/{ledger,pools,checkers,trainer,budget,curriculum,panels,metrics,stats,gate,analysis,config}.py`.
- Scripts: `scripts/run_pilot.py`, `scripts/solve_budget.py`, `scripts/run_rq1.py … run_rq6.py`, `scripts/build_transfer_matrix.py`.
- Configs: `configs/arms/{lean,dafny,nonformal,lean_only,dafny_only,lean_dafny,dafny_lean,interleaved}.yaml`, `configs/rq1..rq6.yaml`, `configs/budget.yaml`.
- Manifests: `manifests/{formal_math_panel,software_panel,curriculum_panel,budget}.json` with source hashes, dedup params, frozen splits.
- Outputs: `results/rqN/` (per-run ledgers, per-prompt scores, contrasts, CIs), `results/transfer_matrix.{md,csv}`, `results/gate_status.json`.
- Tests: `tests/` unit + synthetic end-to-end.
- `README.md` documenting how to supply data/tools and run each RQ.

## Inputs You Must Provide (when you run) — external things the student must supply to actually run it later

- **Shared checkpoint**: one 0.6B–1.7B model checkpoint (path/weights) used as the identical init for every arm.
- **Lean toolchain + mathlib**: pinned Lean release + mathlib tag; working kernel for proof checking; Lean training corpus.
- **Dafny toolchain**: pinned Dafny verifier; program-verification corpus (states/transitions/contracts/invariants/frame conditions/VCs).
- **Non-formal SFT corpus** with an executable acceptance check.
- **Evaluation sources** for the 5 software families with **executable/verifiable oracles** (code exec sandbox, verifier, equivalence oracle, repair test suites) + the formal-math Lean eval panel.
- **Pretraining shards reference** (or fingerprints) for contamination screening.
- **Compute**: GPUs for ~96 runs (RQ1) + 12-seed arms (RQ3–RQ6); execution sandbox for oracles.
- **API keys / access** for any hosted checkers or model-serving, if applicable.
- **Dependencies**: Python env (numpy/scipy, bootstrap/cluster-robust stats, MinHash/datasketch, Parquet), Lean/Dafny binaries, sandbox runtime.

## Open Decisions / Assumptions — gaps left underspecified by the plan + the assumptions made

- **Base model / pretraining data identity** not specified → assume a single provided checkpoint with retrievable (or fingerprintable) pretraining shards; contamination screen degrades gracefully to training-pool-only if shards unavailable (record this in manifest).
- **Success-propensity & length strata bin counts** unspecified → assume quantile bins (e.g., 3×3); expose as config.
- **Decoding budget** (samples/temperature at eval) unspecified → fix a single shared decoding config across all arms; expose as config; record in manifests.
- **Tie definition** for `W` (score equality) unspecified per family → assume exact-oracle equality is a tie; document per-family oracle score type (binary pass/fail vs. graded).
- **Few-cluster robust procedure** choice unspecified → assume wild cluster bootstrap over training seeds; expose alternative.
- **Interleaving granularity** ("minibatch-interleaved") → assume alternating minibatches with equal per-half quotas; expose stride as config.
- **Pilot size / blinding** unspecified → assume a small disjoint pilot with arm labels masked to the budget solver; record pilot manifest.
- **Checker external-tool availability** → assume tools may be absent in dev; provide stub backends so tests and dry-runs pass without them, gated behind a `--real-checkers` flag.
- **Multiplicity adjustment family** (which contrasts share simultaneous control) → assume per-RQ family-wise control across that RQ's reported contrasts; document in `stats.py`.
