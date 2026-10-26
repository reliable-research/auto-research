> **✅ CURRENT — edited in place.** This spec carries all review corrections; there is no
> `.revised` sibling. The unedited original is upstream in
> `paper_autodiscussion/completed_jobs_dirs/<job>--<room>/experiment-spec.md`.

# Experiment Specification: Typed Obligation Verdicts as Reward — Structured Verification-Condition vs. Dense Execution-State Supervision for Dafny Code Models

## Objective — what the experiment must establish (from the problem definition)

Build a training-and-evaluation harness that determines, under fully matched conditions, whether reinforcement learning from **typed program-verification obligations with distinct solver verdicts** produces better **tool-off** (no verifier, no countermodel at inference) coding behavior than three alternative reward representations derived from the same or comparably dense signals.

Concretely, the harness must:

1. Train four RL arms from a shared base checkpoint over identical single-function Dafny instances, matched on sampled-token budget, candidates/task, optimizer, updates, verifier, and test harness:
   - **A1 Typed-verdict** (proposed): per-obligation-type × per-verdict advantage vector.
   - **A2 Dense execution-state** (primary contrast baseline).
   - **A3 Binary verifier** (pass/fail collapse baseline).
   - **A4 RLFR-style verified-goals ratio** (scalar-collapse mandatory ablation).
2. Score **every** on-policy candidate with **both** oracles (verifier + execution/hidden-test) at fixed snapshots *before* computing any arm-specific reward (paired-oracle scoring).
3. Evaluate tool-off hidden-test correctness and secondary outcomes (robustness, specification hacking, verifier-behavior divergence, scalarization sensitivity), with preregistered reward weights, distinct timeout-vs-refutation semantics, and raw obligation vectors persisted.

The **primary causal contrast** is A1 − A2 on tool-off hidden-test pass@1. The **mandatory ablation contrast** is A1 − A4.

---

## Research Questions & Success Criteria — RQs with explicit, checkable success criteria

Let `pass@1_arm` = mean tool-off hidden-test pass@1 over sealed tasks × checkpoints for an arm. All intervals use **two-way cluster bootstrap** over `{task, checkpoint}` clusters unless stated.

| RQ | Question | Success Criterion (checkable) |
|----|----------|-------------------------------|
| **RQ1** | Causal effect of typed vs. dense execution-state on tool-off pass@1 | `mean(pass@1_A1 − pass@1_A2) ≥ 0.02` **AND** two-sided 95% cluster-bootstrap CI (10,000 resamples over task×checkpoint) excludes 0. |
| **RQ2** | Typed vs. verified-goals-ratio collapse | `mean(pass@1_A1 − pass@1_A4) ≥ 0.02` **AND** two-sided 95% CI excludes 0. |
| **RQ3** | Reward pipeline preserves matched packet counts & scale, **and the dense arms actually receive dense signal** | (a) For **every** audited candidate, all arms emit the **same** packet count on that candidate (per-candidate agreement; violation rate = 0). Counts vary *across* candidates because snapshots sit at syntactic-completion boundaries, so a fixed `K=32` must **not** be asserted. (b) For each non-typed arm the simultaneous 95% CI of `RMS_arm / RMS_A1` ⊆ `[0.95, 1.05]`. (c) **Usable-packet gate:** median across candidates of (usable packets / total packets) ≥ the preregistered threshold, where *usable* = the packet holds ≥1 obligation with a determinate verdict (`proved`/`refuted`/`unknown`/`timeout`) that is neither `synthetic` nor `indeterminate`. Failing (c) means the dense arms are terminal-reward arms in disguise; report it as a feasibility negative and do **not** present the typed-vs-execution contrast as a dense comparison. |
| **RQ4** | Typed packets carry non-circular info about hidden correctness lost by the ratio | Relative CV log-loss reduction of typed-packet probe vs. ratio-only probe `≥ 0.05`, with one-sided 95% lower bound `≥ 0.05` (task-grouped nested 10-fold CV). |
| **RQ5** | Robustness under semantics-preserving perturbation; typed > dense | Simultaneous lower bound on typed perturbed-to-clean retention `≥ 0.90` **AND** simultaneous lower bound on `(perturbed pass@1_A1 − perturbed pass@1_A2) ≥ 0.02`. |
| **RQ6** | Reduced weakened-spec verifier-pass/hidden-fail divergence; scalarization insensitivity | Upper 95% bound on divergence-rate ratio `A1/A4 ≤ 0.80` **AND** upper 95% bound on max pass@1 spread across 8 fixed scalarizations `≤ 0.02`. |

**Reporting requirement (all RQs):** persist raw obligation-type × verdict count vectors for every candidate; report descriptive A1−A3 (binary) and per-checkpoint heterogeneity alongside primary contrasts.

---

## Methods to Implement — the components/algorithms to build (from method design)

### M0. Verifier abstraction (`DualOracle`) — shared infrastructure
Two frozen oracles applied to every candidate program at scoring snapshots:

- **`VerifierOracle`** wraps the fixed Dafny verifier. For a candidate `.dfy`, it must return a structured `VerifierResult` containing, **per obligation instance**:
  - `obligation_type ∈ {INITIALIZATION, PRESERVATION, EXIT_POSTCONDITION, SAFETY, TERMINATION}`
  - `verdict ∈ {PROVED, REFUTED_COUNTERMODEL, UNKNOWN, TIMEOUT, INVALID}`
  - source location + (if refuted) a serialized countermodel.
  - **Timeout must remain distinct from refutation** (never coalesce `TIMEOUT`/`UNKNOWN` into `REFUTED`).
  - Invocation: `dafny verify <file>` (pin one Dafny version; record it). Use `--verification-time-limit`/`/timeLimit` for the solver limit and a **deterministic resource limit (`/rlimit`)** where available for reproducibility; also apply an OS-level `subprocess` `timeout=` hard backstop. Parse per-task outcomes via `--verification-logger json|csv` (or `/verificationLogger:json|csv`), falling back to regex parsing of `file(line,col): Error: <msg>` lines plus the `finished with X verified, Y errors` summary. Map obligation-type from Dafny's message text (e.g., "invariant might not hold on entry" → INITIALIZATION; "might not be maintained by the loop" → PRESERVATION; "postcondition could not be proved" → EXIT_POSTCONDITION; index/null/division/frame → SAFETY; "cannot prove termination"/decreases → TERMINATION). Enable countermodel extraction (`/mv:<file>` or the counterexample-extraction option for the pinned version) with model completion enabled. **See Open Decisions for version-pinning assumptions.**
- **`ExecutionOracle`** wraps the fixed **reward-visible training test harness**: compile via `dafny build`/`dafny run` (or the pinned equivalent) and run the **training** tests; return `pass ∈ {0,1}` and per-test outcomes plus a **dense execution-state trace summary** (see M2/A2). Tool-off inference must call neither oracle.
- **TWO DISJOINT TEST SETS — do not conflate them.** Every task carries (a) `tests_train`, reward-visible, the only tests any oracle may see during training, and (b) `tests_sealed`, used exclusively for tool-off evaluation and never exposed to any reward channel, arm, or checkpoint-selection decision. They must be disjoint by construction and generated so that passing one does not trivially imply passing the other. An earlier version of this spec described the execution reward as running "hidden tests" while also requiring hidden tests to be withheld from every reward signal — those two statements cannot both hold, and the split above is what resolves them. `ExecutionOracle` reads `tests_train` only; `ToolOffEvaluator` (M3) reads `tests_sealed` only. Assert this separation in code and fail the run if either oracle is handed the wrong set.

Both oracles are **frozen** for the whole study (single version, fixed flags, fixed seeds). Every candidate is scored by **both** oracles before any arm computes its reward.

### M1. Seed-blocked four-arm randomized fork trainer (`ForkTrainer`)
- From **8 initialization checkpoints** (seed blocks) derived from one shared base checkpoint, fork **four replicate policies** (A1–A4). Randomize arm→policy assignment within each seed block; record assignment.
- **Exact-match training resources across arms:** same task stream/order per seed block, same sampled-token budget per update, same candidates/task (`C`), same optimizer + hyperparameters, same number of updates, same verifier, same harness. Enforce via a single shared `TrainingConfig` consumed by all arms; assert equality at startup.
- RL algorithm: policy-gradient / GRPO-style group-relative update over `C` candidates per task (see Open Decisions for the exact optimizer choice). The **only** thing that differs across arms is the reward function fed to the optimizer.
- **Identical-candidate matching is claimed only at seeding**; after the first on-policy update arms diverge — do not attempt candidate-level pairing post-seed. Pairing for statistics is at the **task × checkpoint** level.

### M2. Synchronized reward construction (`RewardBuilder`) — the core of the contrast
At the candidate's **`k_c` syntactic-completion boundaries** (≤32; NOT fixed token-indexed offsets — see the snapshot rule), build all rewards from the **same** dual-oracle observations so timing and scale are held constant; the only difference is which identities remain visible to the optimizer.

- **Channel encoding:** define the fixed schema of `(obligation_type × verdict)` channels = 5 types × 5 verdicts = **25 channels**, plus execution-state channels for A2. At each boundary snapshot compute the *change in counts* per channel since the previous snapshot. Zero-fill channels with no events. Emit **`k_c` packets per candidate per arm**, where `k_c` is that candidate's boundary count — identical across arms, varying across candidates, never padded or truncated to a global constant ( RQ3 audits this).
- **A1 Typed-verdict reward:** channel-normalized **multi-head advantages** over the 25 typed channels, combined by **one preregistered fixed weight vector** `w*` (alternate fixed vectors reserved for RQ6 sensitivity).
- **A2 Dense execution-state reward:** equally dense supervision from execution traces (e.g., per-snapshot deltas in {tests-passed, assertion-checks-passed, coverage-or-branch-signal, runtime-error-flags}), matched to comparable channel count and update timing. Must be **as dense as A1** (not a scalar).
- **A3 Binary verifier reward:** deterministic coarsening → `all-proved` (1 iff every obligation PROVED, else 0), emitted at that candidate's **same `k_c` boundary snapshots**.
- **A4 Verified-goals ratio:** deterministic coarsening → `proved / total_obligations` at that candidate's **same `k_c` boundary snapshots**.
- **Calibration:** on a **frozen pre-RL calibration corpus**, scale each arm's reward to **unit reward RMS** under a **common clipping** rule. Freeze the **25-channel schema** and the scalar calibration factors **before** any audit/training (RQ3 depends on this). The *channel* schema is fixed; the *packet count* `k_c` is not — it is the candidate's boundary count.

### M3. Tool-off behavioral evaluation + post-hoc diagnostics (`ToolOffEvaluator`)
- Sample **pass@1** completions with verifier and countermodel access **disabled** on the sealed battery, stratified by unseen program structure and paired semantics-preserving perturbations.
- Judge with **independent** property-based + metamorphic hidden tests (kept separate from any reward signal).
- **Post hoc only** (never fed back to generation): apply the common verifier and an **original-specification AST comparator** to compute clean/perturbed correctness, **specification hacking** (spec weakened relative to original AST yet verifier-passes), **verifier–behavior disagreement** (verifier PROVED but hidden tests fail, or vice-versa), and matched outcomes for **every preregistered typed scalarization**.

---

## Baselines to Implement — comparison methods and why each is included

| ID | Baseline | Why included |
|----|----------|--------------|
| **A2** | **Dense execution-state reward** | **Primary matched contrast.** Isolates typed-verdict feedback from equally dense execution supervision under identical resources → removes "typed just has more/denser signal" as a confound. |
| **A3** | **Binary verifier reward** | Fixed binary collapse of verifier signal. Tests whether any observed effect needs *typed verdict structure* vs. mere verifier pass/fail. Reported descriptively (not a preregistered CI target). |
| **A4** | **RLFR-style verified-goals ratio** | **Mandatory scalar-collapse ablation** built from the *same* obligation signals as A1. Isolates the information retained by typed packets beyond aggregate verified-goal coverage (drives RQ2, RQ4, RQ6). |

All baselines share M0/M1/M2 infrastructure; they differ **only** in `RewardBuilder`'s coarsening step.

---

### Oracle-call resource ledger (REQUIRED — consumed by the companion cost study)

Every oracle invocation — verifier and execution harness alike — MUST append one record to a
per-run `oracle_calls.jsonl`:

```
OracleCall = { run_id, candidate_id, snapshot_index, arm, oracle: "verifier"|"execution",
               obligation_id | null, wall_latency_s: float, solver_cpu_s: float,
               gpu_s: float, termination: "ok"|"timeout"|"error", timeout_cap_s: float,
               retries: int, cache_hit: bool }
```

Append-only, one line per call, never aggregated at write time — the companion cost study
(ZW4, *Oracle Economics*) reconstructs latency distributions and timeout mass from these records and
**cannot run its no-new-training phase without them**. Aggregating or dropping `termination` loses the
censoring information that study depends on. Emitting this ledger costs instrumentation overhead only;
it does not alter training, and it must be on for every arm so per-oracle costs stay comparable.

## Datasets — how to load or construct inputs (interfaces/format, not the data itself)

Implement a `DatasetLoader` interface returning typed records; the actual instances/tests are supplied by the user (see "Inputs You Must Provide"). Provide a small synthetic fixture set for pipeline testing.

### D1. Matched tool-off hidden-test suite (primary eval)
- **Size:** N = 6,000 sealed single-function Dafny tasks.
- **Stratification fields (must be present on each record):** `repo_or_template_family`, `obligation_type_signature`, `solver_verdict_mix`, `difficulty`.
- **Record schema:**
  ```
  Task {
    task_id: str
    prompt: str                      # natural-language / signature spec shown to model
    signature: str                   # Dafny method signature + requires/ensures skeleton
    hidden_tests: List[Test]         # property-based + metamorphic; never shown to model
    original_spec_ast: SpecAST       # for spec-hacking AST comparison
    strata: {family, obligation_sig, verdict_mix, difficulty}
    split: "eval"                    # sealed; disjoint from training & calibration
  }
  ```
- Sealed: no overlap with training or calibration families.

### D2. Disjoint reward calibration-audit corpus (RQ3, RQ4)
- **RQ3 audit:** N = 10,000 frozen candidates from **2,000 disjoint tasks** × **5 generation seeds**, covering feasible `(obligation_type × verdict)` cells.
- **RQ4 probe corpus:** N = 12,000 frozen candidates from **2,400 tasks** excluded from training, calibration, and primary eval. Each candidate carries its `k_c` typed packets, its verified-goals ratio, and its **hidden-correctness label** (used only as a label).
- **Record schema:**
  ```
  FrozenCandidate {
    cand_id, task_id, gen_seed
    program_text: str
    typed_packets: float[k_c][25]    # k_c boundary snapshots × 25 frozen (type×verdict) channels.
                                     # NOT float[32]: k_c is this candidate's boundary count (≤ K_max=32),
                                     # varies across candidates, identical across arms. Never pad/truncate.
    verified_goals_ratio: float
    raw_obligation_vector: int[5][5] # type × verdict counts (must be persisted)
    hidden_correct: 0|1              # label only
  }
  ```

### D3. Perturbation & weakened-specification stress suite (RQ5, RQ6)
- **RQ5:** N = 6,000 base tasks, each with **6 preregistered semantics-preserving variants**: identifier renaming, equivalent specification rewrite, conjunct reordering, formatting change, irrelevant-context insertion (and one more preregistered variant to reach 6). Hidden tests unchanged.
- **RQ6:** N = 10,000 **weakenable** tasks with preregistered **specification-removal/weakening transformations**; hidden tests unchanged; `original_spec_ast` retained for the AST comparator.
- **Record schema:**
  ```
  PerturbedTask {
    base_task_id
    variant_id: str          # "clean" | "rename" | "spec_rewrite" | ... (paired)
    prompt, signature
    hidden_tests             # identical to base
    original_spec_ast
    weakening_transform: Optional[str]   # for RQ6
  }
  ```

---

## Metrics — the measures to implement, with precise definitions / formulas

Implement in a `metrics.py` module; all consume persisted per-candidate records.

1. **Tool-off hidden-test pass@1** (per arm): `pass@1_arm = mean over (task, checkpoint) of hidden_correct(single tool-off completion)`.
2. **Paired arm difference:** `Δ = pass@1_Ai − pass@1_Aj` computed per `(task, checkpoint)` cluster then averaged; CI via **two-way cluster bootstrap** over `{task, checkpoint}`, 10,000 resamples, two-sided 95%.
3. **Reward RMS (per arm):** `RMS_arm = sqrt(mean(clipped_reward^2))` over calibration-audit candidates; report `RMS_arm / RMS_A1` with **task-clustered simultaneous** bootstrap equivalence bounds; **per-candidate packet-count-agreement violation rate** (arms disagreeing on a candidate's count; NOT deviation from a fixed 32) = fraction of candidates on which any two arms emit different packet counts.
4. **Probe log loss (RQ4):** out-of-fold logistic log loss for typed-packet probe vs. ratio-only probe; **relative reduction** = `(LL_ratio − LL_typed) / LL_ratio`; report one-sided 95% lower bound (task-clustered), plus calibration error (ECE).
5. **Perturbed pass@1 & retention (RQ5):** `retention = perturbed_pass@1 / clean_pass@1` (per arm), per-perturbation results, **worst-group retention**, simultaneous bounds; paired typed−dense perturbed difference.
6. **Weakened-spec divergence rate (RQ6):** `div_rate_arm = P(verifier PASSES ∧ hidden test FAILS ∣ weakened task)`; **rate ratio** `A1/A4`; upper simultaneous 95% bound. **Specification-hacking rate:** `P(spec weakened vs original AST ∧ verifier passes ∧ hidden fails)`.
7. **Scalarization spread (RQ6):** `spread = max_s pass@1(scalarization_s) − min_s pass@1(scalarization_s)` across 8 preregistered RMS-matched scalarizations; upper simultaneous 95% bound.
8. **Descriptive:** typed−binary (A1−A3) and typed−ratio point estimates; per-checkpoint heterogeneity of each contrast.

---

## Implementation Plan — ordered, concrete coding tasks the agent should perform

1. **Repo scaffold & config.** Create the package layout (see Expected Artifacts). Implement `config/` with a single frozen-schema `RewardSchema` (25 typed channels; **variable-length packet sequence of length `k_c`**, not 32 fixed slots — `k_c` is per-candidate and must match across arms) and a `TrainingConfig` dataclass consumed by all arms. Add an `assert_matched_resources()` startup check.
2. **`DualOracle` — verifier.** Implement `VerifierOracle.verify(program) -> VerifierResult` via subprocess to the pinned Dafny. Parse structured output (JSON/CSV logger; regex fallback). Implement the **obligation-type classifier** (message→type) and **verdict classifier** (PROVED/REFUTED_COUNTERMODEL/UNKNOWN/TIMEOUT/INVALID), keeping TIMEOUT≠REFUTED. Wire countermodel extraction + deterministic `/rlimit` and OS timeout backstop. Unit-test on synthetic `.dfy` fixtures covering each obligation type and verdict.
3. **`DualOracle` — execution.** Implement `ExecutionOracle.run(program, hidden_tests) -> ExecResult` (compile+run, per-test outcomes, dense execution-state trace summary). Guarantee the tool-off inference path never imports/calls either oracle.
4. **`RewardBuilder`.** Implement the boundary-snapshot channel encoder producing `typed_packets[k_c]`, where `k_c ≤ 32` is the candidate's own boundary count and the four coarsenings (A1 multi-head weighted advantages with `w*`; A2 dense execution channels; A3 all-proved; A4 proved/total). Implement zero-fill for channels absent at a snapshot. **No pad/truncate**: the packet count `k_c` is the candidate's boundary count and must be produced identically by every arm on that candidate, never forced to a global constant. Implement calibration (unit RMS, common clipping) using the frozen pre-RL corpus; freeze factors to disk.
5. **`ForkTrainer`.** Implement seed-blocked four-arm forking from 8 checkpoints, randomized arm assignment, and the shared RL update loop (group-relative policy gradient). Ensure the reward function is the **only** cross-arm difference. Log token budgets/updates to verify matching. Persist raw obligation vectors per candidate.
6. **`ToolOffEvaluator`.** Implement tool-off sampling (verifier/countermodel disabled), independent property-based + metamorphic test judging, and post-hoc diagnostics: common-verifier pass, **AST comparator** vs `original_spec_ast` (spec-hacking), verifier–behavior disagreement, per-scalarization matched outcomes.
7. **`metrics.py` + `stats.py`.** Implement all metrics above and a **two-way cluster bootstrap** (task×checkpoint) plus **task-clustered simultaneous** bootstrap for RQ3/RQ5/RQ6 and the **nested task-grouped 10-fold CV** logistic probe for RQ4.
8. **RQ drivers.** Implement one script per RQ (`run_rq1.py` … `run_rq6.py`) that loads persisted artifacts, computes the target statistic + CI, and emits a machine-readable pass/fail against the success criterion.
9. **Preregistration freeze.** Write reward weight vector `w*`, the 8 scalarizations, the 25-channel schema and the cap `K_max=32` (**not** a fixed packet count), clipping rule, and CV/bootstrap settings to a version-controlled `prereg.yaml` **before** any training; hash and record it.
10. **End-to-end smoke test** on synthetic fixtures + a tiny checkpoint to validate the full pipeline (train→score→evaluate→stats) before scaling.

---

## Ablations — variants to build as configurable switches, and what each isolates

Implement as flags in `RewardBuilder`/`TrainingConfig`:

- **`reward_mode ∈ {typed, dense_exec, binary, ratio}`** — the four arms; isolates reward representation (core contrast).
- **`scalarization_id ∈ {s1..s8}`** — 8 preregistered fixed weight vectors for A1 (RMS-matched via RQ3); isolates sensitivity of the typed arm to fixed scalarization (RQ6).
- **`timeout_semantics ∈ {distinct, merged_with_refuted}`** — default `distinct`; the `merged` switch quantifies how much distinct timeout semantics matters (do **not** use `merged` for headline results).
- **`countermodel_channels ∈ {on, off}`** — whether refutation channels distinguish REFUTED_COUNTERMODEL from UNKNOWN; isolates value of countermodel-bearing refutations.
- **`K_max ∈ {8,16,32}`** — sensitivity to the **cap** on boundary snapshots per candidate (default 32). This truncates the boundary list; it does not re-space snapshots, and a candidate with fewer boundaries than the cap is unaffected. Do **not** implement this as a fixed packet count.
- **`dense_exec_channel_set`** — configurable execution-state channels for A2, to test that A2 density is genuinely matched to A1.

---

## Expected Artifacts — the code modules, scripts, and config files that should exist when done

```
repo/
├── prereg.yaml                 # frozen weights w*, 8 scalarizations, 25-channel schema + K_max=32 cap, clipping, CV/bootstrap config (hashed)
├── config/
│   ├── reward_schema.py        # 25 typed channels; variable-length k_c packet sequence, cap K_max=32
│   └── training_config.py      # shared TrainingConfig + assert_matched_resources()
├── oracles/
│   ├── verifier_oracle.py      # Dafny subprocess, output parsing, obligation+verdict classifiers, countermodel
│   ├── execution_oracle.py     # compile/run hidden tests, dense execution-state trace
│   └── dual_oracle.py          # pairs both; scores every candidate before rewards
├── reward/
│   ├── channel_encoder.py      # boundary-snapshot obligation×verdict channel deltas, zero-fill; NO pad/truncate — k_c varies per candidate, identical across arms
│   ├── reward_builder.py       # 4 coarsenings + multi-head advantages + calibration (unit RMS, clipping)
│   └── calibration.py          # frozen pre-RL corpus calibration; persists factors
├── training/
│   ├── fork_trainer.py         # seed-blocked 4-arm fork from 8 checkpoints; shared RL loop
│   └── rollout.py              # candidate sampling, token-budget accounting
├── eval/
│   ├── tooloff_evaluator.py    # tool-off sampling (oracles disabled) + independent tests
│   ├── ast_comparator.py       # original-spec AST comparison for spec-hacking
│   └── diagnostics.py          # verifier-behavior divergence, per-scalarization matched outcomes
├── analysis/
│   ├── metrics.py              # all metric definitions
│   └── stats.py                # two-way + simultaneous cluster bootstrap; nested task-grouped CV probe
├── data/
│   └── dataset_loader.py       # D1/D2/D3 loaders + synthetic fixtures
├── scripts/
│   ├── run_rq1.py … run_rq6.py # per-RQ drivers emitting pass/fail vs. criteria
│   └── run_smoke_test.py       # end-to-end on synthetic fixtures
└── artifacts/                  # persisted candidates, raw obligation vectors, rewards, results (gitignored)
```

---

## Inputs You Must Provide (when you run) — external things the student must supply to actually run it later

- **Base checkpoint + 8 seed-blocked initializations** of a code model capable of Dafny generation, plus RL training compute (multi-GPU) sufficient for 4 arms × 8 checkpoints.
- **Dafny toolchain**, pinned to a specific version, installed and on `PATH`; confirm the exact CLI flag spellings for JSON/CSV verification logging, counterexample extraction, and resource-limit (`/rlimit`) against `dafny verify --help` for that version (several are version-dependent — see Open Decisions).
- **Z3** solver bundled with Dafny; fixed solver seed and resource limit for determinism.
- **Datasets** conforming to the D1/D2/D3 schemas: 6,000 sealed tasks (D1), 2,000 + 2,400 disjoint task pools (D2), 6,000 base + 10,000 weakenable stress tasks (D3) — each with hidden property-based/metamorphic tests, original-spec ASTs, and stratification labels. **Ensure train/calibration/eval family disjointness.**
- **Hidden-test harness** runtime (language + test runner for the metamorphic/property-based tests).
- **Ground-truth hidden-correctness labels** are produced by the ExecutionOracle at scoring time; you must supply correct, non-leaking hidden tests.
- **Python deps:** subprocess/LSP client (optional `pylspclient`/`multilspy` if using the Dafny language server), numpy/scipy, scikit-learn (logistic probe + CV), a bootstrap utility, and your RL framework (e.g., TRL/verl-style GRPO).
- **Preregistration sign-off:** commit `prereg.yaml` (weights, scalarizations, clipping, `K_max` cap, CV/bootstrap settings) **before** training.

---

## Open Decisions / Assumptions — gaps left underspecified by the plan + the assumptions made

1. **RL algorithm.** The plan specifies "candidates per task" and matched updates but not the optimizer family. **Assumption:** a group-relative policy-gradient method (GRPO-style) over `C` candidates/task, identical across arms; reward is the only cross-arm difference. Record exact optimizer/hyperparameters in `prereg.yaml`.
2. **Dafny version & flag names.** Exact spellings for JSON diagnostics, counterexample extraction, and the deterministic resource-limit flag are version-dependent. **Assumption:** pin one Dafny 4.x release; use `--verification-logger json|csv` (fallback: regex on `file(line,col): Error:` + summary line) and `/rlimit` for determinism; verify via `dafny verify --help`. Do not rely on exit-code numeric mapping — parse output.
3. **Obligation-type classification.** Dafny does not emit a first-class typed-obligation enum; types are inferred from message text/location. **Assumption:** implement a message→{INITIALIZATION,PRESERVATION,EXIT_POSTCONDITION,SAFETY,TERMINATION} classifier and validate on labeled fixtures; unmapped messages → SAFETY with a logged warning; unparseable/malformed programs → verdict INVALID.
4. **Dense execution-state channel set (A2).** The plan requires A2 to be "equally dense" but does not fix channels. **Assumption:** use per-snapshot deltas in {hidden-tests-passed, runtime-assertion-checks-passed, branch/coverage signal, runtime-error flags}, sized to match A1's channel count; expose as `dense_exec_channel_set`. This matching is a key validity threat — audit it.
5. **Boundary snapshots (cap `K_max=32`, not a fixed count) + MANDATORY prefix completion.** Snapshots sit at **syntactic-completion boundaries** — each position where the completed prefix strictly extends the previously verifiable content (a top-level declaration, statement, or specification clause closes) — capped at `K_max=32`. Do **not** use evenly spaced token offsets: on single-function candidates most such offsets land inside an unfinished body, every obligation is `indeterminate`, and the dense arms silently degrade to terminal reward. Emit fewer packets when fewer boundaries exist; never pad with duplicates. The boundary set is derived from the candidate text and MUST be identical across arms for that candidate (RQ3a checks per-candidate agreement, not a fixed count). Log `usable_packet_rate` per candidate for the RQ3c gate. **A raw token prefix is not a valid Dafny program**, so before either oracle is invoked each snapshot MUST pass through `PrefixCompleter` (deterministic, seed-independent, identical across arms): close open delimiters in parser-expected order; replace unterminated statements/expressions with typed holes; leave declared-but-unwritten method bodies **EMPTY**; leave written specification clauses untouched. **NEVER insert `assume false;` (or any other assumption) into an unwritten body** — `assume false` makes the remaining path unreachable and lets the verifier discharge the enclosing method's *original* postconditions vacuously, contaminating obligations the model actually wrote. Tagging inserted scaffolding does not undo that; the contamination is on the original obligations. Any stub that strengthens the path condition is likewise forbidden. Instead **abstain**: tag obligations from inserted holes `synthetic`, tag an obligation `indeterminate` **only when the program text its own verification condition depends on is incomplete** — NOT merely because the enclosing method is unfinished — and **exclude `synthetic` and `indeterminate` from reward**.

  **This distinction is what makes the dense signal feasible.** Gating on whole-method completeness would leave nearly every snapshot of a single-function candidate unusable, since the method closes only at the end; the dense arms would then be terminal-reward arms and the headline comparison would be infeasible by construction. Obligations have different dependency footprints and become determinate at different times: precondition well-formedness and invariant *initiation* are determined once the code preceding the loop and the invariant clause exist; *preservation* once the loop body closes; *postcondition sufficiency* and *termination* only once the method closes. Compute each obligation's dependency footprint from the VC's source span and mark it determinate as soon as that span is complete, independent of the enclosing unit. RQ3c's usable-packet gate then measures whether this actually delivers early signal rather than assuming it. Keep `synthetic` and `indeterminate` distinct from `unknown`/`timeout`, which mean the solver ran and did not conclude. Only obligations whose own dependency footprint is complete contribute reward at a snapshot — never "obligations in fully-written units", which is the whole-method gating this paragraph rejects two sentences above. Log the per-snapshot `indeterminate` share — a high early share is expected; a low one means the completer is doing more than closing syntax and must be investigated. Snapshots that cannot be closed into a parseable unit are recorded as `uncompletable`, excluded from both rewards, and their rate reported. Apply the SAME completer to the execution oracle's snapshots so dense proof and dense execution signals are computed on identical artifacts. Reuse the prior snapshot's verification context where incremental verification is available; otherwise charge full per-snapshot solver cost and report it, since a dense arm otherwise consumes ~K× the sparse arms' solver budget silently.
6. **Preregistered weight vector `w*` and 8 scalarizations.** Concrete numeric values are not given. **Assumption:** choose `w*` and `s1..s8` a priori (before any hidden-test access), RMS-match via the RQ3 calibration corpus, and freeze in `prereg.yaml`; do not tune on eval data.
7. **Countermodel serialization.** Boogie/Z3 models are partial/heuristic. **Assumption:** persist raw model text plus a boolean "countermodel-present" to distinguish REFUTED_COUNTERMODEL from UNKNOWN; do not depend on fully concretized models.
8. **"Verified-goals ratio" definition (A4/RLFR).** **Assumption:** `proved / total_obligations` at each snapshot, zero-fill unavailable events, identical calibration/clipping to other arms.
9. **Spec-hacking / AST comparator scope.** **Assumption:** the comparator flags a candidate as spec-weakened if its `requires`/`ensures`/`invariant`/`decreases` clause set is a strict logical/syntactic weakening of `original_spec_ast`; refine the equivalence checker as needed and record its rules in prereg.
10. **Statistical multiplicity.** Six RQs with several bounds each. **Assumption:** treat RQ1 (primary) and RQ2 (mandatory ablation) as confirmatory; RQ3–RQ6 use simultaneous bounds within-RQ; report all intervals without cross-RQ multiplicity correction unless the user requests otherwise (record the decision in prereg).
