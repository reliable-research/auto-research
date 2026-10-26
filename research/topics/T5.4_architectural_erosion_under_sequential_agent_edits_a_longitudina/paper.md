# Architectural Erosion under Sequential Agent Edits: A Longitudinal Measurement — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run. All thresholds below are pre-registered; none is a result.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** The test-gated acceptance oracle is *memoryless and structure-blind* — it projects each patch onto per-step input–output behavior and discards its dependency-structure content — while architectural state is a *cumulative, structural* variable that changes only through exactly the patches the oracle admits; the gate therefore cannot, even in principle, bound the drift of the one quantity that compounds across the sequence.

**判据 (deletion test).** Delete the domain nouns (test oracle, patch, dependency structure, architecture): "The ___ is memoryless and ___-blind — it projects each ___ onto per-step ___ and discards its ___ content — while ___ state is cumulative and changes only through admitted ___s." Without the nouns the sentence has no truth value: nothing identifies *which* projection loses *which* accumulating quantity. It does not survive as a valid generic claim ("A and B were never connected" would), so this is an invariant statement about the oracle, not a bridge. The invariant is checkable: the gate function G (Step 5) is computable without ever reading the import graph — that is a property of the object, not of two literatures.

## Step 2 — Archetype

**Primary:** `empirical` (digest N12), sub-genre *controlled longitudinal comparison* — a measurement of a phenomenon against a counterfactual arm, not a system, benchmark, or method. **Secondary:** `tool` (CO4, explicitly subordinate — the harness exists to make the measurement replicable).

Downstream consequences:
- **(a) Abstract contribution slot:** a quantified phenomenon — the agent−human erosion-rate difference and its patch-level mechanism profile — never "we propose a framework/benchmark".
- **(b) Intro logic:** "what becomes possible" = erosion under agent editing becomes a *decidable, per-step-measurable* quantity with a defensible counterfactual; the intro argues the measurement was previously undefined (C2: erosion only exists relative to a counterfactual), not that we beat a number.
- **(c) Evidence standard for results:** pre-registered statistical contrasts (mixed-effects step×arm interactions, Holm-corrected, with effect sizes and per-repo breakdowns), 3-seed dispersion, and publishable-either-way criteria — not best-case demos or leaderboard deltas. A precise null is a valid result under this archetype (see F-G1).

## Step 3 — Taste self-audit

| Check | Verdict | Action |
|---|---|---|
| Is the opportunity a Bridge? | **Risk found.** Digest Claim 4 ("fills a documented gap between two literatures") is bridge-shaped. | Demoted: gap-filling is *positioning* (related-work paragraph), never the contribution. The contribution is the Step-0 invariant made measurable (H1–H3). |
| Is the method mere Synthesis? | **Risk found.** M1+M2+M3 could read as "SWE-bench + static analysis + mixed models glued together". | Reframed: the load-bearing design element is the *deliberately architecture-blind gate* (M5) crossed with the *human-gold counterfactual* (M4) — a controlled isolation of "admitted-yet-eroding" patches. The components are instrumentation for that isolation, not the idea. |
| Load-bearing verbs from integrate/unify/leverage family? | **Pass after rewrite.** | Verbs fixed to: *gate* (M5), *isolate* (M4 counterfactual), *measure* (M2/M3), *attribute* (M6). |
| Abstract-opening rule | Enforced in Abstract v0: opens with the oracle asymmetry (mechanism-first); the "X is increasingly used… however… we introduce" template is not used. | — |

**Corrected framing (idea skeleton):** *We isolate and measure a structural blind spot of the test-gated acceptance oracle: because G is invariant to dependency structure, serial acceptance can monotonically transport a repository along architecture-degrading trajectories; we measure that transport rate against the human counterfactual and attribute it to patch-level mechanisms.*

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The quantity: the per-metric slope difference Δβ_m between an agent-editor arm and a human-gold-editor arm of architecture-conformance metrics Φ_m over step index, on chronologically ordered, repository-grouped SWE-bench-Verified task sequences; the unit of analysis: one accepted-patch step within one trajectory (repo × arm × seed); the reference population: Python OSS repositories with an importable, declarable layered structure and dense SWE-bench Verified chronological task coverage (django/sympy/astropy at pilot scale); the decision it feeds: whether a test-gated acceptance oracle is a sufficient guardrail against architectural decay under serial agentic editing, or whether architecture-conformance gating must be added alongside it.

**Notation.** Repository state s₀; task sequence T = (t₁,…,t_N) (chronologically ordered SWE-bench Verified instances of one repo); editor policy π ∈ {agent configs, human-gold}; patch pᵢ = π(tᵢ, sᵢ₋₁); gate G(pᵢ, sᵢ₋₁, tᵢ) ∈ {0,1} = 1 iff tᵢ's rebased fail-to-pass tests pass ∧ regression suite passes (M5); accepted state sᵢ = sᵢ₋₁ ⊕ pᵢ if G=1, else sᵢ = sᵢ₋₁ (after ≤k=3 retries, task skipped and logged). Metric vector Φ(s) ∈ ℝ⁶ (M2): Φ₁ cyclic-dependency count (#modules in import-graph SCCs of size>1, grimp/pydeps); Φ₂ layering-violation count (violations of import-linter contracts frozen before any run); Φ₃ architectural-smell count (cyclic/hub-like/unstable, Arcan-style); Φ₄ propagation cost (MacCormack); Φ₅ maintainability index / cyclomatic complexity (radon); Φ₆ duplication % (jscpd). **Primary metrics** = {Φ₁, Φ₂, Φ₆}; Φ₃–Φ₅ secondary.

**Adjective/verb → definition → measurement:**

| Term in claims | Formal definition | Measured by |
|---|---|---|
| *test-passing* | G(p,s,t)=1 | SWE-bench harness execution (M5) |
| *architecture-blind* (gate) | G computable from test outcomes alone; ∀ structure-only rewrites p→p′ with identical test behavior, G(p)=G(p′); operationally: 0 assertions over import structure in the gate's test set | static scan of gate test files for import-graph assertions (A3 check) |
| *erosion* (within arm) | β_m > 0, where β_m = fixed-effect slope of Φ_m over step index i in `Φ_m ~ i + (i | repo:seed)` | mixed-effects fit (M3a) + per-trajectory Mann-Kendall τ (M3 check) |
| *progressive / cumulative* | Mann-Kendall trend significant per trajectory (monotone drift, not a one-step jump) | M3a nonparametric check |
| *agent-attributable erosion* (C2) | Δβ_m = β_m(agent) − β_m(human-gold) > 0, i.e. the step×arm interaction in `Φ_m ~ i × arm + covariates + (i | repo:seed)` | M3/M4 contrast on the task intersection completed by both arms (threat t2 rule) |
| *faster* | Δβ_m significant (Holm) ∧ Cliff's δ on per-trajectory slopes ≥ 0.33 | H1 procedure |
| *erosion rate* | (β_m per metric; plus discrete-time hazard of first new Φ₂ violation, censored) | M3a slopes; M3b survival model |
| *predicts* (a factor) | likelihood-ratio test of the factor's fixed effect, Holm-corrected p<0.05, ∧ marginal-R² gain ≥ 0.15 | H2 procedure |
| *mechanism* (patch-level) | regression coefficient of an M6 feature on per-step ΔΦ within trajectories | H3 procedure |
| *edit locality* | mean pairwise import-graph shortest-path distance among modules touched by p (lower = more local) | M6 profiler |
| *cross-layer import edge* | new import edge whose endpoints lie in different frozen import-linter layers | M6 profiler |

Deleted adjectives (no computable referent, removed from all claims): "silently", "hidden", "corrode" (replaced by defined *erosion*).

## Assumptions (A1..A6)

| ID | Assumption | Failure mode | Detection / gate |
|---|---|---|---|
| A1 | **Sequence constructibility:** ≥60% of a repo's chronologically ordered Verified tasks survive test-rebasing onto the agent-evolved checkout (digest N6 feasibility). | Merge conflicts/moved code make later tasks inapplicable; trajectories too short. | Walking-skeleton gate S1 (Step 9). Pre-committed fallback: curated synthetic 20-task sequence on one layered OSS app (digest N6 fallback path). |
| A2 | **Construct validity:** Φ is an acceptable proxy for architectural health (seed constraint: 真值 = 静态分析度量). | Metric-flat yet expert-judged-eroded snapshots (threat t1). | Full R2 instrument-validation sequence (guidance.md §R2), not a single-rater check: ① Φ's six sub-metrics are grounded in cited external construct definitions (cyclic-dependency/hub/unstable smells per Arcan's published taxonomy; layering per each repo's own documented package structure) before any snapshot is rated; ② the expert rating rubric is drafted wide and refined on a 15-snapshot held-out calibration set (named merge/split of rating categories logged before scale); ③ **two independent blinded expert raters** (not one) each rank all 60 sampled snapshots by perceived architectural health; require inter-rater agreement κ ≥ 0.7 on the coarse ordinal bins, **and** Spearman ρ ≥ 0.4 between the metric ranking and the raters' consensus (majority) ranking; ④ inspect the disagreement structure — rater-vs-rater and rater-vs-metric disagreements must be adjacent-rank, not systematic collapse (e.g. one rater flatly ignoring layering violations); ⑤ freeze the rubric and the 60-snapshot sample before any H1–H3 test is run. **Acceptance threshold:** κ ≥ 0.7 AND ρ ≥ 0.4 both required; if κ < 0.7 (raters don't agree with each other), the property is under-defined and claims scope to "metric-defined erosion" verbatim in title/abstract without asserting expert-judged construct validity; if κ ≥ 0.7 but ρ < 0.4 (raters agree with each other but not with Φ), Φ itself is the mis-specified element and the same scoping applies. |
| A3 | **Gate blindness:** the acceptance test set contains no import-structure assertions. | Some repo tests assert module layout, partially gating architecture. | Static scan of all gate tests per repo before runs; offending tests documented and excluded from the *blindness claim* (not from the gate). |
| A4 | **Sufficient acceptance:** each agent arm accepts ≥50% of surviving tasks (≥10 accepted steps of ~20), else slopes are underpowered (threat t4). | Weak agent/backbone stalls the sequence. | Skeleton gate S2; fallback: swap in a stronger pinned backbone before scale-up (config change). |
| A5 | **Control-arm feasibility:** human-gold patches apply serially in the same order with the same rebasing rules. | Gold patches conflict after reordering. | Skeleton arm 2; identical attrition rules for all arms (threat t2); primary contrasts restricted to the completed-task intersection. |
| A6 | **Metric determinism:** Φ(s) is a pure function of the snapshot (zero variance across re-runs). | Nondeterministic analyzers corrupt slopes. | Gate **S4 (Step 9)**: run M2 twice per snapshot; require bitwise-identical outputs. **Consequence if it fails:** treated as a placebo-arm-style invalidity per guidance.md Part 4 situation 1 — a nonzero re-run difference means the pipeline, not the repository, is the source of apparent drift, so H1–H3 are not scored from that run; the offending analyzer is pinned to a fixed version/seed or replaced before any re-run, and the skeleton (not the scale-up) is where this is caught. |
| A7 | **Adequate statistical power:** the scale-up's 54 agent + 6 human-gold trajectories (~1,080 step observations) detect a step×arm interaction of the pre-registered effect floor (Cliff's δ ≥ 0.33) at power ≥ 0.8 for the 3 primary metrics; per-condition cells in E2's factorial (3 agents × 3 repos × 2 orderings × 3 seeds ⇒ n=3 trajectories/cell before pooling) are large enough for the per-factor LRT to be interpretable. | Thin cells (e.g. a single agent config × repo combination with only 3 trajectories) yield a non-significant LRT that is indistinguishable from a true null, silently deflating H2/H3 into false "no factor matters" conclusions. | **Gate S6 (Step 9):** before scale-up, run a power calculation from the pilot's 1-agent/1-seed trajectory's observed step-to-step metric variance, projecting the minimum detectable Cliff's δ at n=54 vs n=6 trajectories and at each E2 cell's n=3; require projected power ≥ 0.8 for the H1 primary-metric family. **Consequence if under-powered:** any cell/family below the 0.8 target is **pre-declared INCONCLUSIVE** (guidance.md Part 4 situation 5), never reported as a null result — for H1 (the central, adequately-resourced test) this blocks scale-up until the design is adjusted (more seeds, not more conditions, per situation 10); for H2's per-factor cells this narrows H2's claim to only the powered factors, with underpowered factors named explicitly as "untested, not ruled out" rather than silently absent. |

## Step 6 — Pre-Registered Experiments

Design constants (digest N8 analysis plan, hardened): scale-up = 3 repos (django, sympy, astropy) × 3 agent configs × 2 orderings × 3 seeds = 54 agent trajectories (~20 steps) + 6 human-gold + 3 single-shot control trajectories; α = 0.05, Holm–Bonferroni within each hypothesis's declared test family; all models `lme4`-style mixed-effects with trajectory-level random slopes.

### E1 — Erosion vs the human counterfactual (RQ1 → H1)
- **Assumption:** A1–A7 (all; this is the central experiment).
- **Hypothesis H1 (binary):** In `Φ_m ~ step × arm + gold-patch-LOC + issue-age + (step | repo:seed)`, the step×arm interaction is positive with Holm-corrected p < 0.05 for **≥ 2 of the 3 primary metrics** {Φ₁ cyclic deps, Φ₂ layering violations, Φ₆ duplication}, **and** Cliff's δ on per-trajectory slope pairs (agent vs human) ≥ 0.33 for those same metrics. Both conjuncts required; else H1 fails.
- **Metric:** Δβ_m (Step 5) per primary metric; per-trajectory Mann-Kendall τ as the nonparametric robustness check (digest N8).
- **Verification:** mixed-effects LRT on the interaction term; Holm across the 3 primary metrics (secondary Φ₃–Φ₅ reported descriptively, outside the family); contrasts computed only on the task intersection completed by both arms (t2); n = 54 agent + 6 gold trajectories, ~1,080 step observations; seed-level dispersion reported (t5).
- **Fallback F1 (pre-committed wording):** If the agent−human contrast fails but within-agent-arm drift holds (Mann-Kendall significant, β_m > 0, ≥2/3 primary metrics): *"Test-gated serial editing erodes metric-defined architecture at a rate statistically indistinguishable from the human-gold counterfactual: erosion is task-driven, not agent-specific, and the test gate's structural blindness is equally permissive for both editors."* If no drift in any arm → F-G1.

### E2 — Factor attribution (RQ_INF_1 → H2)
- **Assumption:** A1, A4, A5, A7 (per-cell power); meaningful only if E1 finds drift in at least one arm.
- **Hypothesis H2 (binary):** At least one factor in the declared set {agent config, task type (bugfix/feature), ordering, lagged prior-erosion state} attains a Holm-corrected LRT p < 0.05 (family = 4 factors) **and** adds marginal-R² ≥ 0.15 for the erosion-rate outcome. Directional sub-prediction (reported, not gating): lagged erosion state is positive (compounding).
- **Metric:** per-trajectory β_m and survival hazard (M3b: discrete-time model of first new Φ₂ violation, censored trajectories retained) regressed on factors (M4 design).
- **Verification:** LRT per factor against the null mixed model; 54 trajectories; agent×backbone not fully crossed — attribution stated at configuration granularity only (digest unaddressed C4, kept as an explicit scope limit).
- **Fallback F2 (pre-committed wording):** *"Within the studied factorial, erosion rate is condition-invariant: no agent configuration, task type, ordering, or prior-state signal separates from seed noise (all Holm-corrected LRT p ≥ 0.05), yielding a single pooled erosion-rate estimate as the field's first quantitative baseline."*

### E3 — Patch-level mechanisms (RQ_INF_2 → H3)
- **Assumption:** A1, A5, A6.
- **Hypothesis H3 (binary):** (i) Paired Wilcoxon (agent vs human patch for the same task, ≥ 60 matched pairs/repo) is Holm-significant (family = 3 features) with rank-biserial r ≥ 0.3 for **≥ 2 of 3** M6 features {cross-layer import edges, duplication delta, edit locality (agent lower)}; **and** (ii) within-trajectory regression of per-step ΔΦ on the 3 features achieves R² ≥ 0.25 with ≥ 1 Holm-significant coefficient.
- **Metric:** M6 feature vector per accepted patch; per-step ΔΦ_m deltas (M2).
- **Verification:** paired nonparametric tests on the matched-task intersection; delta regression with trajectory fixed effects; features and pairing rule frozen before any run.
- **Fallback F3 (pre-committed wording):** *"Erosion, where present, enters diffusely: agent and human patches are indistinguishable on the three hypothesized structural features (all Holm-corrected p ≥ 0.05 or r < 0.3), so per-patch structural profiling cannot serve as an early-warning gate, and drift prediction requires trajectory-level state."*

### Mandatory baselines

- **B0 — "why do this at all" control: the human-gold serial arm** (M4a). The actual developer PR patches applied serially under identical ordering, rebasing, and attrition rules. This is the no-agent-mechanism arm: if agent trajectories do not separate from B0, there is no agent-specific problem — only Lehman-style task-driven structural growth, which C2 says is not erosion. Every headline claim is a contrast against B0, never a raw agent-arm trend.
- **B-alt — strongest-alternative-explanation control: the single-shot agent arm.** **Rival explanation:** "agent patches are *individually* structurally sloppy — the drift is just the sum of per-patch damage, and the *sequence* (persistent history, compounding context) contributes nothing." Control: the same agent, same pinned backbone, same retry budget k=3 (budget/capability-matched), solving each task from its original base commit with no accumulated history; compare Σᵢ ΔΦ(single-shot patches) against the serial trajectory's cumulative ΔΦ. **Binary criterion:** the sequence effect is confirmed iff serial cumulative drift exceeds the single-shot sum with Holm-corrected p < 0.05 (paired per task-intersection, per primary metric, ≥2/3 metrics); otherwise the pre-committed claim is *"erosion is per-patch additive: sequence history does not amplify it,"* which reframes mitigation from trajectory monitoring to per-patch gating.

### Global fallback F-G1 (archetype pivot)

If the central family fails entirely — H1 fails **and** no arm shows within-arm drift (all primary-metric Mann-Kendall trends non-significant across ≥ 80% of trajectories) — pivot from *empirical phenomenon characterization* to *empirical null + measurement protocol* (tool contribution CO4 promoted to co-primary). Pre-committed pivoted abstract sentence: *"Across 54 pre-registered longitudinal trajectories, individually test-passing coding-agent patch sequences do not measurably erode Python repository architecture over 20-step horizons — a bounded null that contradicts the naive extrapolation of Lehman's law to agentic editing, delivered with an open harness that makes the erosion question routinely re-measurable at longer horizons and for new agents."*

## Step 9 — Walking Skeleton

**Binary question:** *Can a ≥6-accepted-step serial agent trajectory be constructed on real chronologically ordered tasks, with a valid human-gold twin, such that the deterministic metric pipeline yields a per-step Φ series?* (Feasibility, not the science — H1 is not tested here.)

- **Arms (2):** (1) OpenHands + one pinned frontier backbone, serial, 1 seed; (2) human-gold patches, same order. No B-alt, no factorial.
- **Task set:** the 10 chronologically earliest django/django SWE-bench Verified instances (densest coverage repo, digest N6).
- **Metrics:** deterministic only — Φ₁ (grimp SCC count), Φ₂ (import-linter violations against contracts frozen from django's documented package layout), Φ₆ (jscpd %). No models, no statistics, no LLM judging.
- **Cost:** ≤ $80 API + ~4 h agent wall-clock + ~1 h static analysis; ≈ 1.5 person-days.
- **Pass criteria (all binary, all mapped to assumptions):** S1 ≥ 6/10 tasks survive test-rebasing (A1); S2 ≥ 5 surviving tasks accepted by the gate within k=3 retries (A4); S3 gold arm applies with the same rules (A5); S4 M2 re-run on each snapshot is bitwise identical (A6); S5 the two arms' cumulative |ΔΦ| differ by a nonzero amount on ≥ 1 metric (signal existence, not significance); **S6** the pilot's observed step-to-step metric variance, projected to n=54/n=6/n=3-per-cell, yields ≥ 0.8 power to detect the pre-registered Cliff's δ ≥ 0.33 floor for the 3 primary metrics (A7) — else scale-up is deferred and the design is adjusted (more seeds per condition, not more conditions, per guidance.md Part 4 situation 10) before any scale spend.
- **"Passed → scaling is config":** scale-up touches only a config file (repo list, agent list, ordering permutation, seed count) and the stats notebook; if any code beyond config must change to scale, the skeleton has not passed. If S1 fails → A1 fallback (synthetic sequence) before any scale-up spend.

## Claim–Evidence Map

| # | Abstract-bound claim (digest Claims §) | Trace | Status |
|---|---|---|---|
| 1 | Test-passing agent patches, applied serially, erode metric-defined architecture faster than human-gold patches on the same sequence (Claim 1) | H1 (E1), defs *erosion/faster/agent-attributable* | needs-experiment; fallback-covered (F1, F-G1) |
| 2 | Erosion rate is predicted by identifiable factors, incl. compounding prior state (Claim 2a) | H2 (E2) | needs-experiment; fallback-covered (F2) |
| 3 | Erosion enters through cross-layer imports, duplication, low edit locality (Claim 2b) | H3 (E3), M6 defs | needs-experiment; fallback-covered (F3) |
| 4 | The test gate is architecture-blind (Claim 3, weakened to its checkable core) | Step-5 *architecture-blind* definition + A3 scan | supported-by-design (a definitional property, verified by static scan, no experiment) |
| 5 | Sequence history amplifies erosion beyond per-patch damage | B-alt criterion | needs-experiment; fallback-covered (B-alt null wording) |
| 6 | The protocol yields a replicable, deterministic longitudinal measurement (CO1/CO4) | Skeleton S1–S5 + A6 + released harness | supported-by-design once skeleton passes |

Dropped from the abstract: digest Claim 4 (literature-gap bridge — positioning only, per Step 3) and any oracle-policy recommendation stronger than what Claim 3's checkable core supports.

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; every number pending)

> A test-gated acceptance oracle is memoryless and structure-blind: it projects each patch onto per-step test behavior and discards dependency structure, yet architectural state changes only through the patches it admits. We isolate the consequence: serial acceptance can transport a repository along architecture-degrading trajectories that no step of the gate can see. We measure this transport on chronologically ordered SWE-bench Verified task sequences executed on persistent checkouts, accepting each agent patch solely by fail-to-pass and regression tests, and tracking six static-analysis metric families after every accepted step. A human-gold counterfactual arm on identical sequences isolates agent-attributable erosion from task-required structural change; a budget-matched single-shot arm separates sequence compounding from per-patch damage; patch-level profiling (cross-layer imports, duplication, edit locality) attributes the drift mechanism. [Results pending: pre-registered slope contrasts, factor attribution, mechanism regressions.]

(~130 words; opens with the invariant; verbs: gate, isolate, measure, attribute.)
