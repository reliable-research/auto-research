# Milestone Satisfaction without Prerequisite State: Checkpoint Bypass in Multi-Step Agent Verification — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run. All thresholds below are pre-registered decision rules, not observations.

---

## Step 0 — Core Asymmetry (升维)

**Invariant sentence:**
> "The observable signature a per-milestone verifier checks is a many-to-one projection of task history: many causal histories — including ones that never established the milestone's prerequisite state — map to the same passing signal, so satisfying a checkpoint is strictly weaker than establishing what that checkpoint certifies."

**判据 (deletion test).** Quote with the domain nouns deleted:
> "The observable signature a ___ checks is a many-to-one projection of ___: many ___ — including ones that never established the ___ — map to the same passing signal, so satisfying a ___ is strictly weaker than establishing what that ___ certifies."

With the nouns (verifier, task history, causal histories, prerequisite state, checkpoint) removed the sentence is empty — it asserts a specific non-injective relation between a *verifier's local signal* and the *causal state it certifies*. It is not a generic truth about projections (a projection can be injective; the claim is that *this* one is not, because prerequisite state is a causal-history property not recoverable from a local surface signal). It is not a bridge: it names no pair of literatures to connect; it states a property of one object (the checkpoint check). PASS.

---

## Step 2 — Archetype

**Primary archetype:** Empirical measurement of a failure mode of an existing paradigm — quantifying a rate that falsifies an implicit sufficiency assumption (consistent with digest N12 = `empirical`). Cache-grounded structural exemplars: `PLMCalibrationCloseLook2023` (background; controlled measurement of an assumed-sufficient claim) and `CodeReproducibilityGap2025` (method-twin; local-signal-vs-disjoint-oracle measurement). The previously named exemplar class (emergent-abilities-mirage, Gistify, lost-in-conversation) is **[UNVERIFIED — requires harvest]** — none of those works is in `discussion/reference_candidates.jsonl` — and is no longer load-bearing anywhere in this spec.
**Secondary archetype:** Instrumentation/dataset (CO1: the constructed prerequisite-DAG suite + independent oracle), in service of the measurement, not a headline benchmark release.

**What this changes downstream:**
- **(a) Abstract contribution slot:** a *measured checkpoint-bypass rate* (P(all milestones pass ∧ terminal oracle fails)) with per-strategy / per-topology / natural-incidence breakdowns — not a new verifier that "beats" prior graders.
- **(b) Intro logic:** "what becomes possible" — for the first time we can *quantify* whether independent per-milestone verification is a sufficient proxy for multi-step task success, rather than argue it qualitatively. Not "beat a number."
- **(c) Evidence standard:** leakage/measurement-error control + honest baselines, NOT a SOTA table. Specifically: (i) an oracle-audit false-inconsistency bound (A4), (ii) a B0 honest-trajectory control proving M2/M4 agree on legitimate completions, (iii) a B-alt strongest-checker control isolating structural locality from weak-implementation.

**Positioning against the verified reference cache (concede-and-differentiate, guidance.md Part 4 situation 6; added 2026-07-04).** The nearest verified neighbors, all `selected` records in `discussion/reference_candidates.jsonl` with digests on disk:
- **`CodeReproducibilityGap2025`** (method-twin) shows AI-generated code passing functional-correctness benchmarks still fails a separate, disjoint reproducibility oracle (clean-environment re-execution). **Conceded:** the local-signal-passes-but-disjoint-oracle-fails measurement pattern is shared. **Ours:** an explicit prerequisite DAG over milestones, *adversarially constructed* reorder/skip/inject trajectories (theirs are natural outputs only), milestone granularity rather than whole-program, and a strongest-checker attribution control (H5).
- **`RevealWeakestLink2024`** (method-twin, REVEAL) introduces step-level verification of reasoning chains because final-answer correctness masks invalid intermediate steps. **Conceded:** the local-vs-global verification-granularity gap is shared. **Ours:** the *inverse direction* — all local checks passing while the global terminal state is inconsistent — on stateful agent tasks with prerequisite structure, not linear text chains; and a measured rate under controlled bypass strategies rather than a verifier benchmark.
- **`MATPLogicalFlaws2025`** (method-twin) measures correct-final-answer-but-invalid-steps gaps using a disjoint theorem-prover oracle. **Conceded:** disjoint-oracle validation of a surface signal. **Ours:** agent state (filesystem/DB/tool state) rather than proof text; prerequisite-state causality (provenance) as the object; strategy/topology decomposition.
- **`RewardModelSelectionCrisis2025`** (method-twin; added 2026-07-05, Phase G finding — was `selected` in cache but uncited, a goal.md §7 gate violation) shows a Goodhart-style gap where standard reward-model ranking accuracy — a locally-assumed-sufficient proxy — fails to predict true downstream behavioral alignment under reward-guided decoding. **Conceded:** the same assumed-sufficient-checker-vs-true-outcome asymmetry, and both papers are instances of the Step-0 many-to-one-projection pattern. **Ours:** multi-step, multi-milestone agent trajectories with an explicit prerequisite DAG (theirs is single-turn, no dependency structure); adversarially constructed reorder/skip/inject traces (theirs are naturally sampled decoding outputs); a disjoint state-consistency oracle over task state rather than a downstream behavioral-alignment judgment.

The eight OpenReview works cited in digest N3 (TED, XENON, Gistify, StepORLM, LatentVeracity, WebArbiter, GTool, DiffTaskGraph) are **absent from this topic's cache**; per the 2026-07-04 fix they are demoted to [UNVERIFIED — requires harvest] in `digest.md`, and no positioning sentence in this spec depends on them. Their re-harvest remains the recorded Phase-B-blocking item.

---

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** No. The object is a single property (non-injectivity of the checkpoint→state map); we do not "connect verifier research to DAG research." The digest's related work (N3) supplies *ingredients* but the claim is about one measurable quantity.
- **Is the method mere Synthesis?** No. It constructs a controlled measurement instrument (prerequisite DAG + locality-scoped verifiers + disjoint terminal oracle) to measure a rate no cited work measures (N3 absence_comment).
- **Load-bearing verbs from integrate/unify/leverage family?** Checked and avoided. Load-bearing verbs are: *formalize, isolate, construct, measure, bound, gate*.
- **Abstract-opening rule:** mechanism/asymmetry first; forbidden "X is increasingly used… however… we introduce" template NOT used (see Abstract v0). PASS — no framing changes required.

---

## Step 5 — Formal Problem Definition

**Estimand** (guidance.md R1; revised 2026-07-04 — two populations, two distinct quantities, stated separately and never pooled):
- **Primary (headline): the natural checkpoint-bypass incidence** `ρ_nat := P_{τ∼D_nat}[Ω(τ)=0 | A(τ)=1]`, unit of analysis = one M2-complete rollout `τ` from the real-agent rollout distribution `D_nat`, reference population = rollouts a working per-milestone verification pipeline would score as complete, decision it feeds = whether deployed per-milestone verification can be trusted, without a separate terminal consistency check, as sufficient evidence of true multi-step task success. Tested by **H4 (headline hypothesis)**.
- **Secondary (constructibility): the constructed-suite bypass rate** `ρ_c := P_{τ∼D_c}[Ω(τ)=0 | A(τ)=1]` over the pre-registered constructed-trace distribution `D_c`. Because `D_c` is researcher-authored (M3 generates traces *designed* to pass the checkers), `ρ_c` is an existence/constructibility quantity: it characterizes *which strategies and topologies admit bypass* (H2, H3, H5), but its magnitude is a property of `D_c`, not of any deployed population, and is never reported as an incidence estimate. Gated by **H1 (constructibility gate)**.

**Notation.**
- Task `T = (Σ, V, E, Φ, Ω)`: `Σ` a state space; `V = {v_1..v_n}` milestones; `E ⊆ V×V` a prerequisite DAG; `Φ = {φ_k}` per-milestone verifiers; `Ω` a terminal oracle.
- Trajectory `τ = (a_1..a_m)`: an action sequence inducing a state path `σ_0 →…→ σ_m` in `Σ`. Terminal state `σ_τ := σ_m`.
- `φ_k : view_k(τ) → {0,1}` — verifier for `v_k`, whose input `view_k` is restricted to the *local* signal of `v_k` (no read access to other milestones' provenance). "All-pass": `A(τ) := ⋀_k φ_k(τ) = 1`.
- `Ω : σ_τ → {0,1}` — a total function of the terminal state comparing it to the canonical goal state `σ*_T`; `Ω(τ)=1` iff `σ_τ` is consistent with `σ*_T`. Disjoint code from every `φ_k`.
- `pre_k(τ)` — indicator that the *true* prerequisite state of `v_k` (established by executing all `E`-predecessors) holds in `τ`.
- **Bypass event** `B(τ) := A(τ)=1 ∧ Ω(τ)=0`. **Checkpoint-bypass rate** `ρ := P_{τ∼D}[Ω(τ)=0 | A(τ)=1]` over a pre-registered trajectory distribution `D` — instantiated separately as `ρ_c` on `D_c` (constructed) and `ρ_nat` on `D_nat` (real-agent rollouts); see Estimand. The two are never pooled.

**Adjective/verb → definition → measurement:**

| Load-bearing term (from N-Claims) | Formal definition | Measured by |
|---|---|---|
| "sufficient proxy" (Claim 1) | Per-milestone verification is *sufficient* iff `A(τ)=1 ⟹ Ω(τ)=1` for all `τ∈supp(D)`, i.e. `ρ=0`. | Estimate `ρ̂` with task-level cluster-bootstrap 95% CI (M5; Step 6 analysis-plan note). |
| "checkpoint bypass" | Event `B(τ)=A(τ)=1 ∧ Ω(τ)=0`. | Per-trajectory conjunction of M2 verdicts and M4 verdict. |
| "prerequisite state (not) holding" | `pre_k(τ)=0` for ≥1 `k` on the trajectory that yet passes `φ_k`. | Bypass-trace tag: which DAG edges the trace violates (M3). |
| "independent per-milestone verification" | Each `φ_k` depends only on `view_k(τ)`; `∂φ_k/∂provenance(v_{j≠k}) ≡ 0`. | Static scope restriction of verifier code (M2) + code audit (A2). |
| "most effective bypass strategy" (Claim 2) | `argmax_{s∈{reorder,skip,inject}} ρ_s`, `ρ_s := P[B(τ)|strategy=s]`. | Per-strategy rate (M5). |
| "structurally sound" (Claim 3) | A stepwise-verified signal is *sound on T* iff `ρ_T=0` under `Ω` as ground truth. | Same as sufficiency, per suite. |
| "terminal consistency oracle" | Total function `Ω` of `σ_τ` (hash-set / DB row-set / deterministic program output), disjoint from `Φ`. | M4; validated by audit (A4). |
| "natural incidence" | `ρ_nat := P[Ω(τ)=0 | A(τ)=1, τ∼real-agent rollouts]`. | RQ_INF_3 (M5). |

---

## Assumptions (A1..A6)

Each: statement · failure mode · detection · gate · consequence (guidance.md §3.2 template).

- **A1 — Canonical terminal state exists.** Every pilot/scale domain has an independently computable canonical goal state `σ*_T` making `Ω` a total function. *Fail:* domain has no well-defined terminal state (e.g. open-ended web tasks). *Detect:* reject any domain where two independent authors disagree on `σ*_T` for >5% of tasks. *Gate:* **PG-0**, pre-pilot domain-selection gate (checked before any task enters the pilot suite). *Consequence:* violating domain is dropped from the suite entirely — no H* is scored on it; does not block other conforming domains.
- **A2 — Oracle/verifier disjointness.** `Ω` shares no code/logic with any `φ_k`. *Fail:* shared helper causes correlated errors, hiding or faking bypass. *Detect:* static code-dependency audit (no shared imports/helpers between `Ω` and any `φ_k`) before any rate is computed. *Gate:* **PG-2**, walking-skeleton exit criterion (iii) (Step 9). *Consequence:* if violated, the entire run is invalid (same severity as a non-null B0 placebo, per goal.md §5 step 1) — fix the shared code and re-run from the walking skeleton; no H* may be scored in the interim.
- **A3 — M2 mirrors real grading.** The verifier types (file/existence, regex/substring, unit sub-test, tool-signature, DB-state, exact-match) faithfully represent deployed benchmark grading (checker-type list originally sourced from TED — **[UNVERIFIED — requires harvest]**; independently instantiated by the local per-call/per-milestone grading documented in cache records `MCPAgentBenchToolUse2026` (tool-selection/invocation-order sandbox grading) and `RLVRAtlassianToolUseAgents2026` (per-tool-call argument/signature checkers), so the assumption does not rest on the unverified citation). *Fail:* real graders richer (partial-credit, LLM-judge). *Detect:* report `ρ` per checker-type so readers map to their benchmark. *Gate:* no pilot gate — this is a construct-validity assumption checked by continuous reporting discipline (per-checker-type breakdown in every result table), not a pass/fail threshold. *Consequence:* does not block any H*; restricts the claim's scope — flagged as construct threat t1 and named explicitly in Limitations as bounding generalization to benchmarks whose grading matches these six checker types.
- **A4 — Oracle correctness bound.** M4's false-inconsistency rate (honest trajectory flagged inconsistent) is small. *Fail:* oracle bugs inflate `ρ`. *Detect:* manual stratified audit of 50–100 verdicts. *Gate:* **PG-1**, walking-skeleton exit criterion (ii) — **pilot gate: false-inconsistency rate must be ≤5%**. *Consequence:* if violated, the domain is dropped and `Ω` re-specified before any H1–H5 is scored on it (blocks, does not merely degrade).
- **A5 — Bypass traces are checker-valid.** Every constructed trace actually drives `A(τ)=1` (all `φ_k` pass). *Fail:* a "bypass" that never passed all checkers is not a bypass. *Detect:* assert `A(τ)=1` as a precondition for counting any trace toward `ρ`. *Gate:* design-time filter applied at trace-construction (every M3 trace generator run), not a separate pilot checkpoint — the strongest kind of detection per guidance.md §3.2 (enforced by construction, not by post-hoc audit). *Consequence:* non-conforming traces are excluded from the denominator and numerator of `ρ` entirely (never counted, never silently kept); if exclusions exceed 20% of generated traces for a strategy, that strategy's cell is flagged thin and its RQ pre-declared INCONCLUSIVE rather than scored.
- **A6 — Enough M2-complete real rollouts.** Real agents (RQ_INF_3) yield enough rollouts with `A(τ)=1` to estimate `ρ_nat`. *Fail:* too few complete rollouts → underpowered. *Detect:* require ≥200 M2-complete rollouts across agents before reporting `ρ_nat`. *Gate:* **PG-3**, pilot count gate, checked before H4 is scored. **Power statement (corrected 2026-07-04; arithmetic shown inline):** H4's decision rule is `ρ̂_nat ≥ 0.01` (i.e. ≥2 bypass events at n=200) with cluster-bootstrap 95% lower bound > 0. Power at the effect floor `ρ_nat = 0.02`: `P(X ≥ 2 | X ~ Bin(200, 0.02)) = 1 − 0.98^200 − 200·0.02·0.98^199 ≈ 1 − 0.0176 − 0.0718 ≈ 0.91 ≥ 0.9`. The prior spec set the decision threshold equal to the floor (`ρ̂ ≥ 0.02`, i.e. ≥4 events at n=200); that rule's power at the floor is `P(X ≥ 4 | Bin(200, 0.02)) ≈ 0.57`, and **no n achieves power 0.9 when threshold = true rate** (it converges to ~0.5) — the arithmetic error this revision fixes by decoupling the decision threshold (0.01) from the effect floor (0.02). These are per-rollout Bernoulli computations; the verdict-time interval is the task-level cluster bootstrap (see Step 6 analysis-plan note), so the ≥200 rollouts must span **≥20 distinct tasks** for the bootstrap to be estimable — re-derive during walking-skeleton scale-up and adjust n upward if task-level clustering inflates the variance. *Consequence:* if the 200-rollout floor is not met, H4 is **pre-declared INCONCLUSIVE** (never reported as a null result) and RQ_INF_3's finding is downgraded to descriptive-only, per guidance.md Part 4 situation 5.

---

## Step 6 — Pre-Registered Experiments

Sample-size / test choices reuse digest N8; hardened with binary thresholds. Family-wise error controlled by Holm–Bonferroni across H1–H4. H5 (B-alt structural-attribution, below) is a conditional follow-up test run only if H1 is non-null, and is Holm-corrected separately within its own single-comparison family (n=1), per guidance.md §3.1.

**Analysis-plan note — dependence structure (added 2026-07-04).** Trajectories are nested within tasks (≈5–15 traces per task share the DAG, verifier code, and oracle), so **no trajectory-level test below treats trajectories as i.i.d.**: rate CIs (H1, H4) use a task-level cluster bootstrap (resample tasks with replacement, 10,000 draws, percentile intervals); strategy contrasts (H2, H5) use cluster-robust (task-level) sandwich standard errors (equivalently, GEE binomial with exchangeable working correlation); the topology model (H3) is a mixed-effects logistic regression with a task random intercept. Every results table reports `n_tasks` alongside `n_trajectories`; the effective sample size is the number of tasks.

**Headline note (added 2026-07-04).** H4 (natural incidence, `ρ_nat`) is the **headline hypothesis**; H1 is a **constructibility gate** (a manipulation check that the pipeline can produce bypasses at all), expected to pass by construction — see RQ1 and the revised Estimand in Step 5.

### RQ1 (digest N8 RQ1) — Can milestones be satisfied without prerequisite state?
- **Assumption:** A1, A2, A4, A5.
- **Hypothesis H1 (constructibility gate — manipulation check, not a headline claim):** *H1 holds iff* the constructed-suite bypass rate `ρ̂_c ≥ 0.10` **and** its task-level cluster-bootstrap 95% lower bound `> 0.05`, over ≥300 constructed trajectories (20–40 pilot tasks × reorder/skip/inject × ~5 variants). **Role note (2026-07-04):** because M3's injection traces write the exact surface signature M2 checks, H1 is *expected to pass by construction*; a PASS is a manipulation check that licenses H2/H3/H5 and Claim 1's existence reading ("bypass is constructible"), and is never reported as evidence about deployed incidence (that is H4). A FAIL is therefore highly informative — see the fallback below and F-G1a.
- **Metric:** `ρ̂_c = (#{τ: A(τ)=1 ∧ Ω(τ)=0}) / (#{τ: A(τ)=1})`.
- **Verification:** task-level cluster bootstrap (10,000 resamples of tasks with replacement, percentile CI) in place of a naive exact-binomial/Wilson interval — trajectories are nested in tasks and are not independent (Step 6 analysis-plan note); report `n_tasks` alongside `n_trajectories` and per checker-type (A3). Holm slot 1.
- **Fallback:** If H1 fails, the paper's claim becomes: *"Under an explicit prerequisite DAG and standard-grading per-milestone verifiers, independent per-milestone verification is empirically sufficient on the constructed suite: checkpoint bypass occurs below a 10% rate (upper bound X%), bounding — rather than confirming — the sufficiency concern."*

### RQ_INF_1 (digest N8 RQ_INF_1) — Which strategy bypasses most?
- **Assumption:** A1, A5 (+ H1 non-null, else descriptive only).
- **Hypothesis H2:** *H2 holds iff* `ρ_inject` exceeds `max(ρ_reorder, ρ_skip)` by `≥10` percentage points, each pairwise two-proportion z-test `p<0.05` after Holm correction across the 3 pairs.
- **Metric:** per-strategy rates `ρ_reorder, ρ_skip, ρ_inject` (M5).
- **Verification:** three pairwise two-proportion tests with cluster-robust (task-level) standard errors — equivalently GEE binomial with strategy as predictor, exchangeable working correlation, sandwich SEs — Holm-corrected across the 3 pairs; report `n_tasks` per strategy cell; Holm slot 2.
- **Fallback:** If H2 fails, the paper's claim becomes: *"No single bypass strategy dominates; injection, reordering, and step-skipping defeat per-milestone verification at statistically comparable rates (all within Δ<10pp), indicating the vulnerability is generic to locality rather than specific to signal-forgery."*

### RQ_INF_2 (digest N8 RQ_INF_2) — Does topology modulate bypass?
- **Assumption:** A1, A5, and scale-up suite (≥200 tasks).
- **Hypothesis H3:** *H3 holds iff* in a **mixed-effects logistic regression** of `B(τ)` on prerequisite-chain depth and node in-degree **with a task-level random intercept** (trajectories are nested in tasks; Step 6 analysis-plan note), at least one fixed-effect coefficient has odds ratio `>1.2` per unit with Wald `p<0.05` (Holm across the two predictors).
- **Metric:** odds ratio per unit depth / per unit in-degree (M5).
- **Verification:** mixed-effects logistic regression (task random intercept), Wald tests on fixed effects, Holm across {depth, in-degree}; report `n_tasks` and per-cell trajectory counts; Holm slot 3.
- **Fallback:** If H3 fails, the paper's claim becomes: *"Checkpoint-bypass rate is insensitive to prerequisite-chain depth and node in-degree over the tested range; bypass is a flat structural property of per-milestone locality, not amplified by graph complexity."*

### RQ_INF_3 (digest N8 RQ_INF_3) — Do real agents bypass naturally?
- **Assumption:** A1, A2, A4, A6.
- **Hypothesis H4 (HEADLINE):** *H4 holds iff* natural incidence `ρ̂_nat ≥ 0.01` (at n=200 M2-complete rollouts: ≥2 bypass events) with task-level cluster-bootstrap 95% lower bound `> 0`, after subtracting audited oracle errors (A4), over ≥200 M2-complete real-agent rollouts spanning ≥20 distinct tasks (3–5 agents × ≥3 seeds); a two-proportion test with cluster-robust SE additionally reports `ρ_nat` vs `ρ_c` (expected direction `ρ_nat < ρ_c`, descriptive). **Effect floor:** `ρ_nat ≥ 0.02` — the smallest incidence that counts as deployment-relevant; the decision threshold `0.01` is deliberately set *below* the floor so the test has power ≥0.9 at the floor (A6's corrected computation: threshold = floor caps power at ~0.5 regardless of n). **Verdict edge cases (pre-declared):** `ρ̂_nat = 0` → FAIL (invoke the fallback); `0 < ρ̂_nat < 0.01` → INCONCLUSIVE-at-n, record the required n, never reported as null.
- **Metric:** `ρ_nat` (M5) + comparison to constructed rate `ρ_c`.
- **Verification:** task-level cluster-bootstrap CI (Step 6 analysis-plan note) + cluster-robust two-proportion test vs `ρ_c`; report `n_tasks` and rollouts-per-agent; Holm slot 4.
- **Fallback:** If H4 fails, the paper's claim becomes: *"Checkpoint bypass is a constructibility result, not an observed deployment behavior: real LLM agents rarely (<2%) produce all-milestones-pass-but-inconsistent rollouts unprompted; the risk is latent (adversarial/reward-hacking) rather than incidental."*

### Mandatory baselines

- **B0 "why do this at all" control — Honest valid trajectories.** For each task, valid topologically-ordered trajectories that genuinely execute every prerequisite. Expectation: `A=1` AND `Ω=1`, so bypass rate ≈ 0. *Justifies the problem:* proves M2 and M4 agree on legitimate completions, so any measured `ρ>0` on constructed traces is attributable to the bypass mechanism, not to baseline M2/M4 disagreement or oracle strictness. **Pre-registered check:** honest-trajectory bypass rate must be `<1%`; if not, M4 is miscalibrated (A4 violated) and the domain is dropped.
- **B-alt strongest-alternative-explanation control — Strongest milestone-scoped verifier.** *Rival explanation:* "bypass happens only because the `φ_k` are weak/lazy toy checks, not because per-milestone verification is structurally insufficient." Control: replace each `φ_k` with the *richest realistic local check* per checker-type (fullest DB-state comparison, strictest exact-match, deepest unit sub-test) — still milestone-scoped, still no cross-milestone provenance (locality preserved by construction), capability/compute-matched. Isolation test formalized as **Hypothesis H5** (guidance.md §3.1, all seven slots):
  - *H5 holds iff* on the injection-strategy traces, the strongest-checker bypass rate `ρ_inject^strong` remains `≥ 0.5 × ρ_inject^weak` (the standard-suite injection rate), two-proportion z-test for non-inferiority at `p<0.05`, run only over tasks where the standard-suite injection rate is itself non-zero (undefined ratio otherwise).
  - `applies_if`: [A1, A2, A5] (H1 non-null as a precondition — H5 is only meaningful once a weak-checker bypass exists to attribute).
  - `metric`: `ρ_inject^strong / ρ_inject^weak` (ratio of strongest-checker to standard-checker injection bypass rates).
  - `test`: one-sided two-proportion non-inferiority test with cluster-robust (task-level) standard errors — the strong- and weak-checker rates are computed on the same tasks, so pairing/clustering by task is mandatory (Step 6 analysis-plan note) — `H5` retained iff the ratio's cluster-robust lower bound clears 0.5.
  - `alpha`: 0.05 (single comparison, own family — see Step 6 preamble).
  - `effect_floor`: ratio `≥ 0.5` (bypass survives at least half-strength against the strongest realistic local checker anyone would deploy).
  - `aggregation`: single test, no cross-instrument vote (one suite, one strategy, one comparison).
  - **Fallback F5 (verbatim, pre-committed downgrade wording per guidance.md §3.3):** *If H5 fails* (i.e. `ρ_inject^strong < 0.5 × ρ_inject^weak`), the paper's claim becomes: *"The measured checkpoint-bypass rate is attributable, at least in part, to this study's specific checker implementations being weaker than the strongest realistic local check — against the richest checker per type, the injection bypass rate falls by more than half. The phenomenon this paper isolates is real on standard-strength graders (Claim 1 stands, downgraded) but the structural-locality mechanism claim (Claim 3's 'not implementation weakness' clause) does not survive; the practical recommendation narrows to 'strengthen milestone checkers' rather than 'per-milestone verification is inherently unsound regardless of checker strength.'"* If H5 *holds*, the original text stands: the cause is structural locality (the Step-0 non-injectivity), not implementation weakness. Injection traces (which forge the exact surface signal) are the sharp test since a stronger local check cannot see provenance.

### Global fallback F-G1 (re-pointed 2026-07-04 at the failable family) + combination rule FC-1

**F-G1 — trigger: the deployment-relevance family fails.** H4 FAILS (no measurable natural incidence) **and** H5 FAILS (bypass does not survive the strongest realistic local checker). H1 is excluded from the trigger because it is expected to pass by construction (Step 6 headline note) — a pivot keyed to H1 would never fire. Pivot: from *measured deployment risk* to *constructibility analysis + design caution*; the headline contribution flips from CO2 (the measured rate) to CO1+CO3 (the audit instrument and the disjoint-oracle pattern). **Pivoted abstract sentence (verbatim, pre-committed):** *"We show that per-milestone verification of multi-step agent tasks can be bypassed by construction — trajectories that pass every locality-scoped checkpoint while failing a disjoint terminal oracle are cheap to construct under an explicit prerequisite DAG — but we find no measurable natural incidence in real-agent rollouts (power ≥0.9 at a 2% floor), and the bypass largely does not survive the strongest realistic local checkers; we therefore deliver the constructed suite and the disjoint-oracle audit pattern as a design-time caution and audit tool, not as evidence of an active deployment failure."*

**FC-1 — pre-committed combination rule for the "H1 passes trivially, everything else fails" outcome.** If H1 PASSES and H3, H4, and H5 ALL FAIL, use this verbatim sentence and do not strengthen it at verdict time: *"Checkpoint bypass is a constructible artifact of milestone-locality that is not modulated by prerequisite-graph structure over the tested range, is not observed unprompted in real-agent rollouts at our power (floor 2%), and is substantially mitigated by stronger — still milestone-scoped — checkers; per-milestone verification therefore warrants a terminal consistency audit as a design caution, but our data do not support calling it an active or structurally irreparable deployment risk."* FC-1 subsumes the individual F3+F4+F5 sentences. For pairwise failures (any two of H3/H4/H5 fail), concatenate the individual F* sentences, weakest claim last; never invent new combination wording at verdict time.

**F-G1a — original all-zero case (retained as a sub-case).** If even constructed traces cannot bypass — `ρ̂_c` indistinguishable from 0 across all three strategies (H1 fails; H5/B-alt is moot because there is no non-zero weak-checker rate to attribute) — pivot from *measurement* to *refutation/negative-result*. **Pivoted abstract sentence:** *"We show that under an explicit prerequisite DAG and per-milestone verifiers drawn from standard agent-benchmark grading, independent per-milestone verification is empirically sufficient: constructed out-of-order, step-skipping, and state-injection trajectories cannot pass all checkpoints while failing a disjoint terminal oracle at any measurable rate, upper-bounding the checkpoint-bypass concern rather than confirming it."*

---

## Step 9 — Walking Skeleton

Minimal closed loop answering ONE binary question: *does at least one constructed trajectory pass all milestone checks while failing the terminal oracle, on a real domain, with a clean oracle?*

- **Arms (2):** (1) **B0 honest** valid trajectories; (2) **inject-bypass** traces (the sharpest strategy). Reorder/skip deferred.
- **Task set:** 10 hand-authored filesystem/coding DAG tasks, N≈5–7 milestones each, canonical terminal state = filesystem hash-set + deterministic program output.
- **Metrics (deterministic only):** `φ_k` = sandboxed assertions; `Ω` = hash-set/output equality. No LLM, no sampling noise.
- **Expected cost:** CPU/sandbox only, no GPU; ~10 tasks × 2 arms × ~5 variants ≈ 100 executions; wall-clock hours; ~8–12 annotator-hours to author.
- **Exit criterion (skeleton passed → scaling is config, not code):** (i) inject arm yields `≥1` trajectory with `A=1 ∧ Ω=0`; (ii) honest arm yields `0` such trajectories (bypass rate <1%, validates A4); (iii) A2 code-disjointness audit passes. If all three hold, moving to ≥300 trajectories, procedural generation (M1), 2–3 domains, and real-agent rollouts (RQ_INF_3) is a configuration/scale change — the loop (generate → verify → oracle → count) is unchanged.

---

## Claim–Evidence Map

| Abstract claim | Traces to | Status |
|---|---|---|
| Per-milestone verification is not a sufficient proxy (∃ bypass) — constructibility/existence reading only | H1 (RQ1, constructibility gate); Step-5 "sufficient proxy" def | needs-experiment; fallback-covered (H1 fallback / F-G1a) |
| State injection is the strongest single bypass strategy | H2 (RQ_INF_1) | needs-experiment; fallback-covered (H2 fallback) |
| Bypass rate rises with DAG depth / in-degree | H3 (RQ_INF_2) | needs-experiment; fallback-covered (H3 fallback) |
| Real agents bypass naturally at non-zero-but-lower incidence **(HEADLINE claim)** | H4 (RQ_INF_3, headline hypothesis) | needs-experiment; fallback-covered (H4 fallback; F-G1 if H5 also fails) |
| A disjoint terminal oracle is a viable soundness-audit pattern | Step-5 `Ω` def + A2/A4 + B0 control | supported-by-design (given A1–A4 gates pass) |
| The measured cause is structural locality, not weak checkers | H5 (B-alt control) | needs-experiment; fallback-covered (H5 fallback F5) |
| No corpus paper measures this rate (gap) | digest N3 absence_comment + Claim 4 (cache-grounded 2026-07-04: 150 triaged / 11 selected in `reference_candidates.jsonl`; nearest twins conceded in Step 2) | supported-by-design (verified-cache search; residual harvest of 8 demoted [UNVERIFIED] works still required before Phase B) |

---

## Abstract v0 (draft, mechanism-first) — DRAFT BEFORE RESULTS

A per-milestone verifier certifies a local surface signal, but the prerequisite state it is meant to certify is a property of causal history — and the map from history to signal is many-to-one: many histories that never established the prerequisite state produce the same passing signal, so satisfying a checkpoint is strictly weaker than establishing what it certifies. We formalize this gap and measure it. We construct multi-step agent tasks annotated with an explicit prerequisite DAG, equip each milestone with an independent verifier mirroring standard benchmark grading (file, DB-state, tool-signature, and exact-match checks), and define a separate terminal state-consistency oracle as ground truth. We isolate three bypass strategies — out-of-order completion, step-skipping, and direct state injection — and measure the checkpoint-bypass rate: trajectories passing every milestone check yet failing the oracle. Our headline estimand is the *natural incidence* of this event in rollouts of real LLM agents; constructed reorder/skip/inject traces serve as a constructibility gate and characterize which strategies and topologies admit bypass. We report rates by strategy and by graph topology with task-clustered intervals, bounding oracle error by manual audit. *(Pre-registered specification; no results yet.)*
