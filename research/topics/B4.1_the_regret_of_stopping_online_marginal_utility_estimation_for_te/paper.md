# The Regret of Stopping: Online Marginal-Utility Estimation for Test-Time Reasoning — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1.., M1.., CO.., RQ..) refer to digest.md. Nothing here contradicts the digest; where the digest gives a statistical plan (N8), this file hardens it into binary criteria with pre-committed fallbacks.

## Step 0 — Core Asymmetry (升维)

**The asymmetry:** *The utility-optimal moment to stop a reasoning trace is a functional of the trace's unobserved future — a future in which additional reasoning segments carry signed marginal utility, since overthinking can flip verifier-correct answers to incorrect — while every deployable stopping signal is a functional of the observed past; mechanical verifiability makes that future exhaustively reconstructable offline, so the information rent every online rule pays (its regret) is an exactly computable quantity, not an unbounded unknown.*

**判据 (deletion test).** Delete the domain nouns:

> "The optimal moment to stop a [___] is a functional of its unobserved future, in which continuing carries signed marginal utility; [___] makes that future reconstructable offline, so every online rule's regret is exactly computable."

Without the domain nouns the sentence is **false or empty** twice over: (a) in generic sequential sampling (e.g. i.i.d. majority voting, classic secretary/optimal-stopping settings) continuation has *weakly non-negative* information value — "signed marginal utility" is false without the LLM-overthinking phenomenon (C3; [CoTLength], [JET], [FirstImpression]); (b) "the future is reconstructable offline" is false in general decision problems — counterfactual continuations cannot be labeled — and becomes true only under the seed's `[GIVEN]` constraint of mechanically verifiable answers plus checkpoint probing (M1). The sentence collapses without its domain content, so it is an asymmetry, not a bridge.

## Step 2 — Archetype

**Primary: `empirical` (measurement study)** — consistent with digest N12: every headline result is a comparative measurement of *existing* stopping heuristics against a reconstructed oracle. **Secondary: `dataset/instrument`** — the logged-trajectory corpus (M5/CO4) and the regret evaluator (M2) are the reusable instrument, subordinate to the measurement (N12's tie-break).

Downstream consequences:

- **(a) Abstract contribution slot:** a *quantity* (regret curves of practical stopping rules vs. a per-instance oracle, decomposed and λ-swept) plus the instrument that makes it computable — NOT a new stopping method that "beats" prior rules.
- **(b) Intro logic:** "what becomes possible" — before this work the field cannot say how much achievable utility its stopping heuristics leave on the table (Claim 1, N4 items 1–3); after it, any rule (including future ones, via offline replay on the released corpus) can be scored in regret terms. The intro does NOT argue "our rule is better".
- **(c) Evidence standard for results:** exactly paired per-instance comparisons on identical logged trajectories, pre-registered tests with multiplicity correction, instrument-validity controls (probe faithfulness, oracle noise floor, discretization ablation). Effect *direction and decomposition* matter more than any single benchmark number; a clean negative (e.g. "no λ-independent ranking exists") is a publishable outcome by design (Claim 5).

## Step 3 — Taste Self-Audit

| Check | Verdict | Evidence |
|---|---|---|
| Is the opportunity a Bridge ("A and B never connected")? | **PASS (not a bridge)** | The claim is not "connect regret analysis to LLM stopping"; it is that a specific quantity (per-instance oracle regret) is *constructible* in this domain because of verifiability, and is currently unmeasured (N4). The deletion test above fails without domain content. |
| Is the method mere Synthesis (glue existing parts)? | **PASS** | M3 deliberately re-implements existing rules — but as *measured conditions inside an instrument*, not as the contribution. The contribution is the oracle construction + regret decomposition (M2) and the measurement (CO1, CO2). |
| Load-bearing verbs from integrate/unify/leverage family? | **PASS after one fix** | Draft verbs audited: "combine the signal history" (M6) is retained only as a *measured condition*; load-bearing verbs throughout are **reconstruct, measure, quantify, decompose, isolate, certify**. No "integrate/unify/leverage" in any claim. |
| Abstract-opening rule | **PASS** | Abstract v0 (below) opens with the mechanism/asymmetry ("The right moment to stop… depends on the future…"), not with "Test-time reasoning is increasingly used… however… we introduce". |

No framing surgery needed beyond the verb fix noted above; the idea skeleton (measurement of an information rent) already satisfies the rules.

## Step 5 — Formal Problem Definition

**Estimand (guidance.md §3.4 R1, added per Phase A checklist item 1/6):** the mean per-instance regret R_λ(r,x) of a stopping rule r relative to the per-instance oracle t\*(x,λ), for the population of mechanically-verifiable reasoning instances drawn from the benchmark suite (M4), at a swept accuracy–compute exchange rate λ; it feeds the decision of which online stopping signal — if any — a compute-constrained deployer should adopt at their own operating point.

**Setup.** Instance x with mechanical verifier v(·)∈{0,1}. A reasoning trace is segmented at reasoning-transition markers into checkpoints k = 1..K (M1). At each checkpoint: N probe answers drawn on a counterfactual branch; verifier applied to each.

**Notation.**
- â_k ∈ [0,1]: probe-estimated accuracy at checkpoint k (fraction of N=8 verifier-correct probes).
- c_k: cumulative token cost through checkpoint k (trace tokens; probe tokens excluded — probes are instrument overhead, not policy cost).
- λ: accuracy–compute exchange rate (accuracy points per 1K tokens), swept over a log-spaced 7-point grid, λ ∈ [0.01, 3] (M2).
- Utility of stopping at k: **U_λ(k) = â_k − λ·c_k**.
- Oracle checkpoint: **t\*(x, λ) = argmax_k U_λ(k)**.
- Rule r stops at t_r(x) using only signals observable at ≤ t_r.
- **Regret: R_λ(r, x) = U_λ(t\*) − U_λ(t_r) ≥ 0.** Reported as mean over instances.
- **Normalized regret: NR_λ(r) = mean R_λ(r,x) / mean [U_λ(t\*) − U_λ(K)]** (0 = oracle, 1 = as bad as never stopping early). Undefined cells (denominator < 0.005) are excluded and reported.

**Every load-bearing adjective/verb → computable quantity:**

| Term in claims | Formal definition | Measured how |
|---|---|---|
| "online" (estimable/rule) | decision at k is a function only of {signals at 1..k} | enforced by offline replay over logged prefixes (M2/M5) |
| "marginal utility" (of one more segment) | ΔU_λ(k) = U_λ(k+1) − U_λ(k); "signed" ⇔ Pr[ΔU_λ(k) < 0] > 0 | directly from logged â, c |
| "regret" | R_λ(r, x) above | M2 replay |
| "oracle" | t\*(x, λ) over the logged trajectory | M2 |
| "practical" (stopping rule) | member of rule bank M3: fixed-budget, confidence-τ (DEER-style), entropy-τ, vote-share-τ (CaTS-criticized family), answer-stability (TrimR-style); τ calibrated on dev split by min dev regret per λ | M3 |
| "informative" (signal) | per-checkpoint AUROC of signal vs. verifier label > 0.5 | N8 metric "stop-signal AUROC" |
| "decouple" (proxy from correctness) | regret mass attributable to checkpoints where signal crosses τ but v disagrees; localized via stop-too-early/late split | M2 decomposition |
| "overthinking" / "stop-too-late" | regret from instances with t_r > t\*; share S_late(λ) = Σ_{t_r>t\*} R / Σ R | M2 decomposition |
| "difficulty" | per-instance baseline pass rate decile (lower pass rate = harder) | M4 |
| "stable ranking" | Kendall's τ between rule orderings at adjacent λ grid points | RQ_INF_2 plan |
| "far from / close to oracle" | NR_λ thresholds fixed in H1/H2 below | Step 6 |

Deleted adjectives (no computable referent, removed from all claims): "principled", "practical headroom" as a standalone noun, "efficient".

**Confound ledger (guidance.md §3.4 R3, added per Phase A checklist item 6 / Part 6 item 7 — every design constraint must name the confound it removes):**
- Probes run on a counterfactual branch while the main trace continues unmodified (M1) removes the confound of the probe intervention itself altering the trajectory the rules are scored against — without this, "natural" stopping and "probed" stopping would be conflated.
- Every rule in M3/M6 is replayed on the identical logged trajectory per instance (M2) removes the confound of trajectory-sampling variance between rules — without exact pairing, a rule could appear to win or lose because it happened to be scored on an easier/harder resampled trace, not because of its stopping logic.
- Threshold calibration for M3/M6 is restricted to a held-out 20% dev split, with all statistical tests run only on the disjoint 80% eval split (Step 6 Common protocol) removes the confound of overfitting thresholds to the same instances used to score them — without this split, every rule's regret would be optimistically biased by construction.
- The split-half oracle reconstruction in A3 (probes 1–4 build t\*, probes 5–8 score it) removes the confound of using the same probe draws to both build and validate the oracle — without the split, the oracle's own reconstruction noise would be invisible in its self-regret.
- The prefix-only allocator control (B-alt) is capacity-matched and evaluated at matched mean token expenditure to the full estimator, removing the confound that a capacity or budget advantage — not genuine use of mid-trajectory evidence — explains any measured gain.

## Assumptions (A1–A8)

*Consequence column added per guidance.md §3.2 (Phase A checklist item 5): each assumption's failure must name which H\* it degrades, restricts, or blocks — not just how the failure would be detected.*

| Id | Assumption | Failure mode | Detection (gate) | Consequence |
|---|---|---|---|---|
| A1 | Verifiers (exact-match, MC grader, unit tests; M4) are ground truth. | Grader false negatives on equivalent expressions inflate regret uniformly. | Skeleton gate: manual audit of 50 verifier decisions per benchmark; >2% grading errors → fix grader before Stage 1. | Blocks all of H1a/H1b/H2a/H2b/H2c/H3a/H3b/H3c: every regret number is computed from verifier labels, so an unfixed grader biases the whole hypothesis family uniformly; the gate is a hard stop before Stage 1, not a per-hypothesis degrade. |
| A2 | Probe answers at checkpoint k ≈ what natural stopping at k would yield (digest t2). | Prompt-format confound biases â_k. | Skeleton gate: probe-vs-natural final-answer agreement at last checkpoint ≥ 90%; second probe phrasing shifts â_k by < 0.05 mean abs. | Degrades H1a/H1b and all downstream regret comparisons (H2a/H2b/H2c/H3a/H3b): a biased â_k shifts both the oracle t\* and every rule's measured stopping accuracy, so failure restricts scope to "regret under this probe protocol" rather than "regret under natural stopping" until re-validated with an alternate phrasing. |
| A3 | N=8 probes give â_k precise enough that oracle t\* is not noise-driven (digest t1). | Binomial noise (±0.17 1 s.e.) manufactures fake regret. | Split-half noise floor: oracle chosen on probes 1–4, scored on probes 5–8; its "self-regret" is the instrument noise floor. Gate: noise floor ≤ 1/3 of the best heuristic's measured regret at median λ. Plus N=32 re-probe on 100 instances (t1 mitigation). | Directly gates H1a, which explicitly requires regret to exceed 3× the noise floor to count; if the gate fails, H1a is blocked (not merely degraded) until N is raised, and every other H\* inherits the same unresolved oracle-precision doubt since they all condition on the same t\*. |
| A4 | Transition-marker segmentation yields K ≈ 10–30 checkpoints capturing decision-relevant resolution. | Too-coarse checkpoints dominate measured regret. | H3c discretization ablation (2× coarser); skeleton logs K distribution, gate: median K ≥ 8. | Directly gates H3c (instrument-validity check); if H3c fails because coarse checkpoints dominate, absolute regret numbers for H1a/H2a/H2b/H2c/H3b are demoted from oracle-relative claims to instrument-relative claims (paper.md's own H3c fallback), restricting scope rather than blocking outright. |
| A5 | The oracle is nontrivial: for a material fraction of instances, t\* < K at moderate λ. | If t\* = K almost always, "stopping" has no economics and B0 suffices. | Skeleton gate: t\* < K on ≥ 20% of instances at median λ. Fail → problem is vacuous on these tasks; triggers F-G1 reconsideration. | Blocks the entire H1–H3 family: if stopping has no measurable economics on these tasks, no regret comparison is meaningful regardless of which rule is tested, so failure routes straight to the F-G1 global pivot rather than degrading any single H\*. |
| A6 | Offline replay = deployment: rules consume only logged signals, so replayed regret equals deployed regret. | A rule needing unlogged state (e.g. KV internals) can't be replayed faithfully. | Design-enforced: rule bank M3/M6 restricted to logged-signal interface; documented in corpus schema (M5). | Restricts scope of M3/M6 by construction (design-enforced, not merely detected): any candidate rule needing unlogged state is excluded from the rule bank rather than admitted and mis-scored, so H2a/H2b/H2c are protected from this failure mode rather than degraded by it. |
| A7 | Probe-cost mitigations make Stage 2 affordable (N6 feasibility: K×N ≈ 160× naive multiplier). | Budget overrun kills Stage 2. | Pilot gate: N=4 vote share correlates > 0.95 with N=8 (digest N6 mitigation); prefix-KV reuse benchmarked in skeleton. | Blocks Stage-2 scale-up experiments only (H2a's cross-cell generalization, H2b's LOBO/LOMO transfer, H3a/H3b's multi-model λ-sweep): Stage-1 pilot hypotheses (H1a/H1b at N=8) are unaffected; failure forces the pre-declared shrink-along-declared-axes response (guidance.md Part 4 situation 10), narrowing which H\* remain adequately powered rather than invalidating the pilot. |
| A8 | The pre-registered sample sizes give adequate power: n≈500/benchmark (Stage 1) and the LOBO/LOMO splits (Stage 2) achieve power ≥ 0.8 for the two-sided Wilcoxon signed-rank test to detect each H\*'s stated effect floor (H1a's NR_λ ≥ 0.05 regret gap over the noise floor; H2b's ≥10% relative NR reduction) at α = 0.05 after Holm correction. | An under-powered cell yields a statistically non-significant result that gets misread as "no regret" / "no gain" rather than "inconclusive." | Pre-Stage-1 power calculation from a 100-instance pilot subsample's observed regret variance; any (benchmark, λ) or LOBO/LOMO cell whose achieved power falls below 0.8 for its effect floor is flagged before scoring. | Gates the scoring rule for every H\*, not just one: thin/under-powered cells are pre-declared INCONCLUSIVE (guidance.md Part 4 situation 5) and excluded from the vote-rule denominators (e.g. H1a's "≥5 of 7 λ values"), never scored as a null result — this is the general rule the AIME-descriptive-only carve-out in Step 6's Common protocol is one named instance of. |

## Step 6 — Pre-Registered Experiments

Common protocol (hardened from digest N8 analysis_plan): ≥ 500 instances/benchmark where test sets allow (AIME ~60 items: descriptive only, excluded from hypothesis tests); all rules replayed on identical logged trajectories → exactly paired; two-sided Wilcoxon signed-rank on per-instance regret differences; Holm–Bonferroni over the ~15 rule pairs per (benchmark, λ) family; α = 0.05 after correction; 10,000-resample paired bootstrap for 95% CIs; thresholds τ calibrated on a 20% dev split, all tests on the disjoint 80% eval split.

**Matched-set / dropped-row rule (guidance.md §3.4 R8, added per Phase A checklist item 6 / Part 6 item 9):** an instance is dropped from the entire (benchmark, λ) comparison set — for every rule, not just the one that failed — if the verifier cannot parse a probe answer at any logged checkpoint, if the model's trace truncates before the first checkpoint (no valid oracle can be reconstructed), or if a rule's replay cannot produce a stop decision from the logged signal interface (A6). Dropped instances are logged with a reason code; the headline n reported for every table is the post-drop n, never the pre-drop instance count, and the drop rate per benchmark is reported alongside n. Any (benchmark, λ) or leave-one-out cell whose post-drop n falls below the A8 power-derived minimum is pre-declared INCONCLUSIVE (A8), never silently pooled with adequately powered cells.

### E1 (RQ1 — is marginal utility online-estimable, and what is the heuristics' regret?)

- **Assumptions:** A1, A2, A3, A4, A5, A8.
- **Hypotheses (binary):**
  - **H1a (regret is real):** every calibrated single-signal rule in M3 has mean regret > 0 with Holm-corrected p < 0.05 AND normalized regret NR_λ ≥ 0.05, at ≥ 5 of 7 λ values, on ≥ 2 of 3 pilot benchmarks (GSM8K, MATH-500, GPQA-Diamond; model: DeepSeek-R1-Distill-Qwen-7B).
  - **H1b (signals are informative):** for each benchmark, at least one of {confidence, entropy, vote share} has pooled per-checkpoint AUROC ≥ 0.60 (bootstrap 95% CI lower bound > 0.55).
  - H1 passes iff H1a AND H1b — i.e. marginal utility is *partially but imperfectly* online-estimable (digest N9.Result1 direction).
- **Metric:** R_λ, NR_λ, stop-signal AUROC (formulas in Step 5; digest N8 metrics).
- **Verification:** Wilcoxon vs. zero per rule per (benchmark, λ), Holm-corrected within benchmark; H1a's regret must additionally exceed 3× the A3 split-half noise floor to count.
- **Fallback (pre-committed wording):**
  - If H1a fails (some heuristic is oracle-level): *"On mechanically verifiable reasoning tasks, [rule X] is ε-certified: its regret is statistically indistinguishable from the per-instance oracle across the exchange-rate grid — online stopping is effectively solved in this regime, and we release the instrument that certifies it."* (Feeds F-G1.)
  - If H1b fails (all AUROC < 0.60): *"No logged online signal carries usable information about the correctness trajectory; online marginal-utility estimation on these tasks is near-vacuous, and all practical stopping rules are unavoidably fixed-budget rules in disguise."* (Digest N9.Result1 falsification arm (b).)

### E2 (RQ_INF_1 — which signal wins; does a learned combination beat all single signals?)

- **Assumptions:** A1–A4, A6, A7, A8.
- **Hypotheses (binary):**
  - **H2a (signal ranking; digest Claim 2):** the vote-share (self-consistency) rule has lower mean regret than BOTH the confidence and entropy rules, with Holm-corrected p < 0.05, in ≥ 60% of benchmark×λ cells (Stage 2: 3 models × 5 benchmarks × 7 λ), and is significantly *worse* than either in ≤ 10% of cells.
  - **H2b (learned combination; CO3):** M6 (logistic + ≤2-layer MLP over signal history) reduces mean normalized regret vs. the best single-signal rule by ≥ 10% relative, Holm-corrected p < 0.05, under leave-one-benchmark-out, on ≥ 3 of 5 held-out benchmarks; AND under leave-one-model-out on ≥ 2 of 3 held-out models.
  - **H2c (residual gap; digest Claim 3):** M6's NR_λ at median λ remains ≥ 0.10 on every Stage-2 benchmark (the oracle gap is not closed), and Spearman ρ(NR, difficulty decile) ≥ 0.5 on ≥ 3 of 5 benchmarks.
- **Metric:** paired per-instance R_λ differences; NR_λ; frontier AUC (digest N8) as secondary, no hypothesis attached.
- **Verification:** exactly paired Wilcoxon per cell, Holm over rule pairs; transfer claims backed only by LOBO/LOMO splits (digest t4 mitigation).
- **Fallback (pre-committed wording):**
  - H2a fails: *"No single online signal dominates: the lowest-regret signal is task- and model-contingent, contradicting the folk ordering in which sample agreement beats internal confidence — practitioners cannot select a stopping signal without per-deployment calibration."*
  - H2b fails: *"The signal history is redundant: a learned combination of confidence, entropy, and agreement adds no measurable regret reduction over the best single threshold, so the binding constraint is the signals' shared blind spot (C2), not how they are combined."*
  - H2c fails (gap closed): merge into E1's ε-certification fallback.

### E3 (RQ_INF_2 — sensitivity to λ and to checkpoint granularity)

- **Assumptions:** A3, A4, A8.
- **Hypotheses (binary):**
  - **H3a (ranking stability; digest Claim 5):** mean Kendall's τ between the full rule ordering at adjacent λ grid points ≥ 0.6, and no adjacent pair has τ < 0.3, per model (pooled over benchmarks).
  - **H3b (failure-mode shift; digest Claim 4):** stop-too-late regret share S_late(λ) is increasing in λ with Spearman ρ ≥ 0.8 over the 7-point grid, and S_late(λ_max) − S_late(λ_min) ≥ 20 percentage points, for the best heuristic and for M6.
  - **H3c (instrument validity):** 2× coarser checkpoint subsampling changes each rule's mean regret by less than 50% of the median between-rule regret gap at the same λ.
- **Metric:** Kendall's τ across adjacent λ; S_late(λ) decomposition; regret delta under coarsening (digest N8 metrics).
- **Verification:** τ with bootstrap CIs over instance resamples; ρ exact permutation test over the grid; H3c is a point comparison with bootstrap CI.
- **Fallback (pre-committed wording):**
  - H3a fails: *"No λ-independent recommendation of any stopping rule is defensible: rule rankings reorder across plausible accuracy–compute exchange rates, so every published 'better stopping rule' claim is implicitly conditioned on an undisclosed λ."* (Digest Claim 5 names this the headline negative finding.)
  - H3b fails: the overthinking-economics claim (Claim 4) is dropped; the decomposition is reported descriptively with the wording *"the stop-early/stop-late mix is not governed by the exchange rate in the predicted direction."*
  - H3c fails: absolute regret numbers are demoted to instrument-relative statements; only within-granularity rule comparisons are claimed, and the corpus release documents the discretization sensitivity as a first-class caveat.

### Mandatory baselines

- **B0 — "why do this at all" control: the fixed-budget sweep.** Non-adaptive stopping at every fixed checkpoint index / token budget (digest N8 baselines, item 1), with the best per-benchmark fixed budget chosen on the dev split. **Pre-registered justification criterion:** the best adaptive heuristic must beat the best *dev-selected* fixed budget by ≥ 20% relative mean regret (Holm-corrected p < 0.05) at the median λ on ≥ 2 pilot benchmarks — otherwise adaptivity itself is worthless on these tasks and the paper's framing changes (see F-G1).
- **B-alt — strongest-alternative-explanation control: the prefix-only allocator.** **Rival explanation:** "adaptive rules win not because mid-trajectory evidence is informative, but because they implicitly adapt to per-instance *difficulty*, which is already predictable before decoding" (the [AdaptiveThinking, OpenReview:2i6Rp0gCq6] position; digest N4 item 6). **Control arm:** an M6-capacity-matched predictor restricted to pre-generation / checkpoint-1 features only (prompt-level signals + first-checkpoint readouts), trained on the same data, replayed on the same trajectories, evaluated at matched mean token expenditure. The claim "online mid-trajectory estimation matters" is licensed only if full M6 beats the prefix-only allocator with Holm-corrected p < 0.05 and ≥ 10% relative NR reduction; otherwise the pre-committed wording is *"the value of stopping-rule adaptivity is exhausted by pre-decoding difficulty prediction; mid-trajectory signals add nothing measurable."*

### Global fallback F-G1

If the central hypothesis family (H1a/H1b jointly, or A5's nontriviality gate) fails, the archetype pivots from *empirical measurement of regret headroom* to *instrument/dataset: a regret-certification benchmark*. Pivoted abstract sentence, pre-committed: *"We release a checkpoint-level, verifier-labeled reasoning-trajectory corpus and an offline-replay regret evaluator that certifies any stopping rule's distance from the per-instance oracle, and use it to show that on today's verifiable reasoning benchmarks the stopping problem is either already ε-solved by simple agreement thresholds or unresolvable from logged online signals — settling, in either direction, what further stopping-rule research can buy."*

## Step 9 — Walking Skeleton

**One binary question:** *does the instrument produce a nontrivial, noise-dominating oracle, and does one adaptive rule measurably sit between fixed-budget and oracle?*

- **Arms (3):** (1) B0 fixed-budget sweep; (2) vote-share threshold rule (dev-calibrated); (3) oracle t\* (upper bound, regret 0).
- **Task set (smallest):** 100 GSM8K + 100 MATH-500 instances, DeepSeek-R1-Distill-Qwen-7B only, N = 8 probes, full checkpoint logging (M1), single λ = 0.3 acc-pts/1K-tokens (grid midpoint) plus the two grid endpoints for the A5 check.
- **Deterministic metrics only:** mean R_λ per arm, NR_λ, split-half noise floor (A3), probe-vs-natural agreement (A2), K distribution (A4), fraction of instances with t\* < K (A5).
- **Expected cost:** 200 traces + ~200×20×8 = 32K short probes with prefix-KV reuse ≈ 10–25 A100-GPU-hours; wall-clock 1–2 days including grader audit (A1).
- **Pass criterion (explicit, all four):** (i) t\* < K on ≥ 20% of instances at λ = 0.3 [A5]; (ii) probe agreement ≥ 90% at final checkpoint [A2]; (iii) split-half noise floor ≤ 1/3 of the vote-share rule's measured regret [A3]; (iv) strict ordering mean-R(B0) > mean-R(vote-share) > 0 at λ = 0.3 on ≥ 1 of the 2 benchmarks.
- **"Passed" means scaling is a config change:** Stage 1 (3 benchmarks × 500) and Stage 2 (3 models × 5 benchmarks) reuse the identical logger, replay evaluator, and analysis code — only model endpoints, instance lists, and the λ grid expand. Any code change after the skeleton (other than new rule implementations in the M3/M6 bank behind the fixed logged-signal interface, per A6) voids and restarts the pre-registration clock for the affected experiment.

## Claim–Evidence Map

| Claim (abstract will assert) | Trace | Status |
|---|---|---|
| Regret vs. a per-instance oracle is exactly computable on verifiable tasks (the instrument exists) | Step 5 definitions; M1/M2; skeleton pass | supported-by-design (conditional on skeleton gates A1–A5) |
| The field currently lacks any such measurement (digest Claim 1) | N4 items 1–3, corpus-grounded | supported-by-design (literature claim, re-verify per digest N4 absence_comment) |
| Practical rules incur real, positive regret; signals informative but insufficient | H1a ∧ H1b | needs-experiment; fallback-covered (E1 fallbacks, F-G1) |
| Self-consistency is the lowest-regret single signal (digest Claim 2) | H2a | needs-experiment; fallback-covered |
| Learned history combination beats single signals; residual gap grows with difficulty (digest Claim 3, CO3) | H2b ∧ H2c; B-alt gate | needs-experiment; fallback-covered |
| Overthinking is a quantified economic loss shifting with λ (digest Claim 4) | H3b | needs-experiment; fallback-covered |
| Rule rankings are λ-stable, so λ-independent recommendations are defensible (digest Claim 5) | H3a | needs-experiment; fallback IS the alternative headline |
| Released corpus enables offline regret scoring of future rules (CO4) | M5; A6 design | supported-by-design |
| Checkpoint discretization does not dominate measured between-rule regret differences (construct-validity precondition every claim above depends on) | H3c | needs-experiment; fallback-covered (H3c fallback demotes the rows above from oracle-relative to instrument-relative claims if it fails) |

Every abstract claim above traces to an H-id or a Step-5 definition; no orphan claims. *(H3c added per Phase A checklist item 4 — it was the one H-id with a pre-committed fallback but no Claim–Evidence Map row, an orphan the checklist's "no orphans either way" rule catches.)*

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — BEFORE RESULTS. All quantitative statements are pre-registered hypotheses, not findings.]**
> The right moment to stop a reasoning trace depends on its future — where continuing has *signed* value, since further steps can overturn correct answers — yet every deployable stopping signal reads only the past. On mechanically verifiable tasks this future is reconstructable: we probe reasoning trajectories at transition checkpoints, verifier-label every probe, and reconstruct the per-instance oracle stopping point across a swept accuracy–compute exchange rate. This turns the regret of any online stopping rule — confidence, entropy, self-consistency, answer-stability, or learned — into an exactly computable, decomposable quantity: how much achievable utility a rule forfeits, and whether by stopping too early or too late. We measure this regret across models, benchmarks, and difficulty, isolate mid-trajectory evidence from pre-decoding difficulty adaptation, and release the checkpoint-level trajectory corpus so any future stopping rule can be scored by offline replay. (146 words)

