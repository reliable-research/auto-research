> Standalone discussion trace for T5.4, extracted verbatim from `pipeline.md`'s Seed brief through Cross-stage consistency check (Stages 1-6 of the `auto-research-discussion` critic/refiner loop). This is the complete round-by-round record — every draft, critique, decision, and refiner pass — that produced the confirmed stage outputs behind `paper_draft.md` and `experiment_design.md`. Nothing below is new; it was already produced and validated in the original run.

# Auto-Research-Discussion Run — T5.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T5.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries a formal problem definition, a Step-3 taste self-audit, and pre-registered experiments with fallback wording), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Any REVISE findings from `stage_review.md` are folded into the `paper_draft.*` files below before they were finalized — see `stage_review.md` for the fixes and the reasoning behind them.

## Seed brief

- **One-sentence description:** Measure whether a sequence of individually test-passing coding-agent patches, applied serially to the same repository, progressively erodes its architecture (cyclic dependencies, layering violations, coupling/complexity, duplication) beyond what the same task sequence would require under human-authored patches, and identify what predicts the erosion rate.
- **Apparent inputs:** a repository with a declared/inferable module architecture; a chronologically ordered sequence of realistic SWE tasks (SWE-bench Verified instances grouped by repo); one or more coding agents; the repository's pre-existing test suite plus per-task fail-to-pass tests as the sole acceptance gate; the task sequence's human-authored gold patches as a control arm.
- **Apparent outputs:** per-step architecture-metric trajectories; a within-arm erosion reading; an agent-vs-human (counterfactual-relative) erosion reading; factor attribution (agent configuration, task type, ordering, prior erosion state) and a patch-level mechanism profile (cross-layer imports, duplication, edit locality).
- **Closest research areas:** agentic SE evaluation substrate and its outcome-only test-gate paradigm (SWE-bench, SWE-Lancer); process-level/trajectory evaluation of agents (EnvConfigTrajEval, BOAD); longitudinal degradation modeling in adjacent LLM settings (Time-To-Inconsistency's survival framing, SimpleTIR's generation-distribution drift); classical human-driven architecture-erosion literature (Lehman 1980; Li et al. 2022; Sas et al. 2021).
- **In scope:** measuring architecture drift under agent-authored, test-gated, serial editing of real repositories, against a matched human counterfactual. **Out of scope:** proposing a new architecture-aware acceptance gate or agent training method; non-Python or non-import-graph architectures; live/production deployments.
- **Confidence: high.** As with a mature reverse-digest seed, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ challenge ↔ RQ ids) and already carrying its own asymmetry/taste self-check (`paper.md` Steps 0 and 3). Reconstruction risk is low; the risk instead is *redundancy* with `paper.md`'s own Steps 5/6, which is why stages 5/6 below are framed to add genuine schema-required content (falsifiable instrument-validity claims, explicit tier accounting) rather than re-deriving `paper.md`'s hypotheses verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a repository with a declared or inferable module architecture, and a chronologically ordered sequence of realistic development tasks applied serially to one persistent checkout by a coding agent — each patch admitted into that checkout only if it passes the task's designated tests — determine whether the repository's architecture (cyclic dependencies, layering violations, coupling/complexity, duplication) progressively deteriorates over the sequence, whether that deterioration exceeds what occurs when the identical task sequence is solved by the original human-authored patches, and, if so, what conditions and patch-level behaviors predict its rate.
- `input`: (1) a repository with a frozen, pre-declared import/layering contract; (2) a chronologically ordered sequence of T realistic tasks for that repository (issue-derived bug fixes and feature requests); (3) one or more coding agents (agent scaffold × backbone); (4) the repository's existing test suite plus each task's fail-to-pass tests, used as the sole functional-correctness gate; (5) the human-authored gold patches for the same task sequence, as a control arm.
- `output`: (1) per-step architecture-metric trajectories for every accepted patch; (2) an erosion-rate statistic per trajectory and arm; (3) an agent-vs-human erosion-rate contrast on the identical task sequence; (4) factor attribution (agent configuration, task type, ordering, prior erosion state) and a patch-level mechanism profile (cross-layer imports, duplication, edit locality) explaining the drift.
- `constraints`: ground truth for architectural state is defined solely as static-analysis metrics, not human-architect judgment; a patch is accepted into the sequence only if it passes the pre-existing test suite, i.e. the study specifically targets erosion that occurs *despite* per-step functional correctness; each trajectory is a single persistent checkout, so its steps cannot be parallelized within themselves.
- `objective`: "A positive erosion-rate finding is accepted only if the mixed-effects step×arm interaction term is Holm-corrected significant (p<0.05) for at least two of three primary structural metrics, with Cliff's δ ≥ 0.33 on a matched task-intersection contrast against the human-gold arm."
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 and `paper.md` Step 2 already settle this as a controlled longitudinal *measurement* against a counterfactual, not a proposed fix or new system.

**critique:**
- summary: The problem is concretely scoped and the four outputs are individually clear, but the objective smuggles in a stage-6-level statistical procedure, and the outputs quietly conflate two logically distinct claims that the seed material itself keeps separate.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "method_leak", comment: "Naming 'the mixed-effects step×arm interaction term,' 'Holm-corrected p<0.05,' and 'Cliff's δ ≥ 0.33' inside the problem-definition objective is a specific analysis-design commitment — that is later-stage content (stage 5/6), not a definition of what counts as a good solution at stage 1. Per the rubric, an artifact that names a specific statistical procedure as part of the problem is major regardless of how well-justified the procedure turns out to be. State the acceptance criterion in problem-definition terms — a reproducible statistical contrast against a matched counterfactual that clears a pre-registered, stated threshold — and push the specific test family to stage 6."}`
  - `{severity: major, field: "output", anti_pattern: "fields_misaligned (conflated outputs)", comment: "Outputs (2) and (3) as drafted read as one continuous claim ('deteriorates... whether that deterioration exceeds...'), but the seed material's own formal definitions (paper.md Step 5) keep these as two distinct, independently satisfiable properties: 'erosion (within arm)' — a positive trend for one arm alone — and 'agent-attributable erosion' — the excess of the agent arm's trend over the human-gold arm's trend on the same sequence. paper.md's own pre-committed Fallback F1 is written for exactly the case where the first holds without the second (drift present in both arms, statistically indistinguishable). Leaving the two outputs merged in stage 1 risks stage 4/6 treating one as a proxy for the other."}`
- decision: `move_to_refiner` (both flags are precision/formalization fixes using content already in the digest and paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A claim of agent-attributable erosion is accepted only if the observed deviation clears a pre-registered, stated threshold on a stated majority (not unanimity) of the primary structural-metric family, when the agent arm is contrasted against the matched human-gold counterfactual on the identical task sequence; the specific statistical procedure that operationalizes 'clears the threshold' is a stage-6 design decision, not a stage-1 commitment."
- `output` (refined): output (2) split explicitly into "(2a) a within-arm erosion reading per trajectory and arm — does this arm's own metric trajectory show a positive trend, independent of any other arm" and "(2b) a counterfactual-relative (agent-attributable) erosion reading — defined only relative to the matched human-gold arm on the identical task sequence, since a trajectory can show (2a) without (2b) (task-driven structural growth any correct implementation would also need) or (2b) without needing (2a) to be large in isolation." Output (3) is re-labeled as the *headline* contrast built from (2a) and (2b) together, not a third independent output.
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Repository state s₀; chronologically ordered task sequence T=(t₁,…,t_N) for one repo; editor policy π ∈ {agent config, human-gold}; patch pᵢ = π(tᵢ, sᵢ₋₁); gate G(pᵢ,sᵢ₋₁,tᵢ) ∈ {0,1}, admitting iff tᵢ's rebased fail-to-pass tests pass AND the regression suite passes; accepted state sᵢ = sᵢ₋₁ ⊕ pᵢ if G=1, else sᵢ=sᵢ₋₁ (after ≤k retries, task skipped and logged). Metric vector Φ(s) recorded at every accepted step. Within-arm erosion for arm π, metric m: a positive long-run trend of Φ_m(sᵢ) over i. Agent-attributable erosion: that trend, for the agent arm, exceeding the trend for the human-gold arm on the identical T. Determine which holds, at what rate, and predicted by which task/agent/patch-level factors."
- `changes_made`: removed the stage-6-level statistical procedure from `objective`; split the conflated erosion outputs into within-arm vs. counterfactual-relative readings; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Test suites are the dominant, often sole, automated acceptance gate for autonomous coding-agent patches, but test suites are constitutionally blind to dependency-direction, layering, and module-boundary structure — so whether repeated agent editing under this gate quietly accumulates architectural damage that no single-patch review would catch is a live, unanswered governance question for teams delegating multi-step software-engineering work to agents.
- `why_it_matters`: If a sequence of individually test-passing patches can nonetheless erode a repository's architecture faster than the equivalent human-authored work, then treating "the tests are green" as a proxy for "the codebase is healthy" is actively misleading, and teams scaling up agentic development on the strength of green CI have no visibility into a compounding maintainability cost until it manifests as a hard-to-reproduce bug or a stalled refactor months later. This matters specifically because the dominant evaluation paradigm for coding agents (SWE-bench-style benchmarks) defines correctness purely as test execution, and even work that criticizes unit-test grading as insufficient for full-system behavior replaces it with *stronger tests*, never a structural check — so the blind spot is not an oversight of any one benchmark, it is built into the entire evaluation paradigm the field currently uses to decide whether an agent is "good enough" to deploy.
- `who_cares`: Teams and organizations delegating multi-step software-engineering work to autonomous coding agents who currently rely on CI/test-suite status as their only automated signal of code health; SE researchers and benchmark designers deciding whether outcome-only correctness metrics (SWE-bench-style) are sufficient for agentic pipelines; builders of agent-orchestration systems (e.g., bandit-optimized multi-agent architectures) whose reward signals currently contain no architectural-quality term.
- `evidence`: `[SWE-bench, OpenReview:VTF8yNQM66]` defines patch correctness purely by fail-to-pass and regression test execution; `[SWE-Lancer, OpenReview:xZXhFg43EI]`'s own motivation argues unit tests "are insufficient for capturing full-system behavior," yet its remedy is stronger end-to-end tests, still an outcome-level per-task signal; `[BOAD, OpenReview:O6stE173BD]`'s own framing describes its optimization reward as "almost entirely deferred until the final patch outcome," with no architectural-quality term at all; Lehman's law of increasing complexity (`[Lehman, 1980]`) predicts drift absent explicit counter-work, under a human-driven cadence no test gate ever supplied — and no cited work has tested whether this transfers to automated, test-gated agent editing (digest N3's own absence note: no paper in the searched corpus measures architecture-metric drift across a serial sequence of agent-authored, test-gated patches).

**critique:**
- summary: The stakes for erosion existing (and being invisible to test gates) are well-argued and stake-specific, but the motivation only covers half of stage 1's confirmed outputs.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1's output (4) is a factor-and-mechanism profile — which conditions and which patch-level behaviors (cross-layer imports, duplication, edit locality) predict erosion rate — not merely whether erosion happens and how fast. why_it_matters motivates detecting erosion and its rate but never explains why mechanism-level attribution specifically matters, as opposed to stopping at a rate estimate. Without that, a reader could reasonably ask 'if I already know erosion is happening and roughly how fast, why do I need to know which patch behaviors carry it' — a real, unaddressed gap, since a rate estimate alone gives a team nothing to check on the *next* patch."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a rate estimate alone is not actionable at the point where it would matter: it tells a team that erosion is accumulating only after enough steps have passed to fit a trend, by which point the damage is already committed to the checkout. Knowing the concrete patch-level carriers — new cross-layer import edges, introduced duplication, low edit locality — is what would let a team turn a lagging, trajectory-level diagnosis into a leading, per-patch check (e.g., flag any patch that adds an import crossing a frozen layer boundary) without waiting for a longitudinal fit to confirm the problem after the fact. This is exactly why mechanism attribution, not just detection-and-rate, is one of stage 1's confirmed outputs rather than a nice-to-have."
- `changes_made`: added the leading-indicator/actionability argument for mechanism-level attribution, closing the partial-coverage gap.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_swebench` | Anon., SWE-bench (OpenReview:VTF8yNQM66) | false (defines patch correctness by test execution only; single-instance, not a sequence) | Defines correctness solely by fail-to-pass/regression execution and grades each instance independently from its own fixed base commit; measures no structural property of accepted patches and never observes what accumulates when many agent patches are applied *serially* to one persistent checkout. |
| `rw_coeditor` | Anon., Coeditor (OpenReview:ALVwQjZRS8) | false | Models multi-round edit *prediction* to assist a human within a single commit; does not measure the structural-quality trajectory of a repository under many autonomously accepted edits — its multi-round conditioning is an assistance mechanism, not a longitudinal quality measurement. |
| `rw_swelancer` | Anon., SWE-Lancer (OpenReview:xZXhFg43EI) | false | Its own motivation argues unit tests are insufficient, but the remedy (end-to-end tests plus economic payouts) is still an outcome-level, per-task acceptance signal; maintainability and architectural conformance of the accepted solution remain unmeasured, and tasks are graded in isolation, not as a cumulative sequence. |
| `rw_boad` | Anon., BOAD (OpenReview:O6stE173BD) | false | Optimizes agent architectures purely for issue-resolution success under a reward its own motivation describes as "almost entirely deferred until the final patch outcome"; contains no architectural-quality term, so discovered agents can maximize resolve rate while degrading repository structure — a blind spot the method cannot detect. |
| `rw_envconfigtraj` | Anon., EnvConfigTrajEval (OpenReview:Q8qgloDKUO) | false | Demonstrates outcome-only scoring conflates fundamentally different agent behaviors and builds process-level supervision — but only for a single environment-configuration episode; observes commands and diagnoses, not the evolving structural state of the code artifact across a longitudinal, multi-task sequence. |
| `rw_ttinconsistency` | Anon., Time-To-Inconsistency (OpenReview:88C7vSdn0t) | false (methodologically borrowed, not a runnable baseline) | Provides exactly the longitudinal statistical machinery this topic needs (survival events, censoring, turn-level hazards), but its degradation events are conversational inconsistencies in dialogue; it never instruments a persistent external artifact such as a repository, so whether artifact-state erosion follows comparable temporal dynamics is untested. |
| `rw_simpletir` | Anon., SimpleTIR (OpenReview:EplNy91Xqh) | false | Documents compounding multi-turn drift, but drift in the model's *generation distribution* during RL training, mitigated by trajectory filtering; does not study drift in the *persistent artifact* the agent edits, and its per-episode environments reset, so cumulative repository-state effects are outside its design. |
| `rw_lehman` | Lehman, 1980 | false | The laws of software evolution were derived from release-granularity observation of human-organizational development; they neither predict the cadence, mechanism, nor rate of complexity growth under autonomous agent editing with a test-only acceptance gate, and offer no per-patch measurement protocol. |
| `rw_li2022` | Li et al., 2022 | false | A systematic mapping of erosion causes/consequences/detection does not itself quantify erosion trajectories under automated agentic sequential editing, nor isolate erosion that occurs despite passing tests at every step; its own call for more empirical studies signals this gap remains open. |
| `rw_sas2021` | Sas et al., 2021 | false | The architectural-smell/source-change relation was established on ordinary human-authored OSS commit histories, not on a controlled, serially executed task sequence performed by an autonomous coding agent under a fixed test-passing gate; whether the same relation holds — or is amplified — for agent-generated edits is unknown. |

**critique:**
- summary: Every limitation is specific and problem-tied (not "scalability issues"-style vagueness), but one baseline label is drawn too conservatively given what the experiment design (`paper.md` Step 6, B-alt) actually does with it.
- comments:
  - `{severity: major, field: "specific_related_works[rw_swebench].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "SWE-bench's I/O framing is genuinely different from this paper's (per-instance-independent-from-base-commit vs. serial-and-cumulative) — marking it a straightforward baseline would risk implying SWE-bench's own reported resolve-rate numbers are being compared against, which they are not. But per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference,' and the current draft's blanket 'false' undersells this: paper.md's own single-shot control arm (B-alt) is exactly SWE-bench's per-instance-independent-of-history protocol, repurposed as the experimental arm that isolates whether serial accumulation itself amplifies erosion beyond the sum of per-patch damage. That's a legitimate, already-designed use of this work that the current draft's 'false, no note' loses."}`
- decision: `move_to_refiner` (this is a wording-precision fix, not a structural one — the protocol is still legitimately borrowable as a comparison arm).

### Refiner pass

- `rw_swebench.is_potential_baseline` set to `true`, with the accompanying note sharpened: "Not a baseline in the beat-a-number sense — SWE-bench's own reported resolve-rate numbers are not compared against. Its **per-instance, independent-of-accumulated-history protocol** is borrowed as the experimental *single-shot control arm* (solving each task from its original base commit with no accumulated agent history), isolating whether serial accumulation amplifies erosion beyond the sum of per-patch damage — independent of its published resolve-rate findings."
- `changes_made`: clarified SWE-bench's baseline role to avoid an implied resolve-rate comparison, while crediting the protocol reuse the experiment design already relies on.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — every limitation above is already the direct target of a stage-4/5 sub-problem and method (below), not a standalone claim this paper is separately committing to verify as its own research question. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4):

- **`sp_oracle_blindness`** — *description:* Determine when a test-passing patch nonetheless changes the repository's dependency/layering structure, despite the acceptance signal carrying zero structural information. *why_it_is_a_problem:* Test-based acceptance is the field's dominant gate, and even its critics only strengthen the test (never add a structural check) — if this gap isn't independently instrumented, erosion under passing patches remains invisible by construction, not just by oversight. *technical_challenge:* Architecture must be measured as an out-of-band static-analysis observable, defined and frozen independent of the test oracle, else any "erosion" claim risks circularity with the acceptance criterion itself. *source_limitation_ids:* `["lim_swebench_execonly", "lim_swelancer_outcomelevel", "lim_boad_rewardonly"]`.
- **`sp_counterfactual_definition`** — *description:* Define what counts as *agent-attributable* erosion, as distinct from structural growth any correct implementation of the same tasks would also require. *why_it_is_a_problem:* Raw metric worsening conflates legitimate necessary coupling growth (a feature genuinely needs a new cross-module call) with agent-specific degradation; without a counterfactual, any observed increase in complexity would misleadingly count as "erosion." *technical_challenge:* Requires a matched counterfactual trajectory (human-gold patches on the identical task sequence and ordering) whose own structural changes can be subtracted out — not solvable by a larger sample of agent-only runs. *source_limitation_ids:* `["lim_lehman_humancadence", "lim_li2022_nomeasurement", "lim_sas2021_humanonly"]`.
- **`sp_slow_drift_detection`** — *description:* Detect a genuine slow, compounding structural-drift signal across a long edit sequence when per-step metric changes are small relative to step-to-step variability. *why_it_is_a_problem:* If erosion is real, it likely accumulates through many individually negligible violations; a before/after snapshot would miss it, and naive pooled statistics ignore within-trajectory autocorrelation, risking both false negatives and pseudo-replication-inflated false positives. *technical_challenge:* Requires longitudinal, autocorrelation-aware statistics (per-step time series with trajectory-level random effects, plus a nonparametric trend check) rather than a two-point comparison. *source_limitation_ids:* `["lim_ttinconsistency_noartifact"]`.
- **`sp_attribution_under_cost`** — *description:* Attribute erosion rate to specific conditions (agent/backbone, task type, ordering, prior erosion state) and to concrete patch-level mechanisms (cross-layer imports, duplication, edit locality), under a combinatorial condition space where each additional condition costs a full, sequentially-dependent trajectory that cannot be parallelized within itself. *why_it_is_a_problem:* Without attribution, "erosion happens" is not actionable — a team needs to know what to change — but attribution studies are usually cheap to scale via more i.i.d. samples, whereas here each trajectory is expensive and cannot be split into independent replicates. *technical_challenge:* This is a design problem, not a bigger-sample problem — it requires a deliberately small, contrastive factorial plus within-trajectory mechanism features that extract attribution signal without requiring more trajectories. *source_limitation_ids:* `["__novel__"]` — no cited work addresses the combinatorial cost-vs-attribution tension; the closest candidates (EnvConfigTrajEval, SimpleTIR) address process-level/drift phenomena but not the cost-of-attribution problem itself.

**critique:**
- summary: Coverage checks out (solving all four would jointly deliver stage 1's confirmed outputs), but two sub-problems risk reading as the same underlying gap stated twice.
- comments:
  - `{severity: minor, field: "sp_oracle_blindness / sp_counterfactual_definition", anti_pattern: "overlap", comment: "Both can read as 'define what erosion even means' — one focused on detectability at a single step, the other on attribution across arms — but the descriptions don't make that distinction sharp enough. As drafted, a reader could reasonably ask why measuring Φ (sp_oracle_blindness) isn't already the whole story."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_oracle_blindness.technical_challenge` sharpened to end with: "...this is a **single-step, single-arm detectability** problem — can architectural change be observed at all, independent of test outcome and independent of any other arm."
- `sp_counterfactual_definition.technical_challenge` sharpened to end with: "...this is a **cross-arm, whole-trajectory attribution** problem distinct from detectability — a design that solves `sp_oracle_blindness` alone (just measuring Φ) would still misattribute legitimate feature-driven coupling growth as erosion without this sub-problem's counterfactual subtraction."
- `changes_made`: made the detectability-vs-attribution distinction explicit in both technical_challenge fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; 1 sourced from a mixed set of related-work limitations each, 1 `__novel__` with a stated decisive-component justification — a tight one-to-one correspondence with digest N5's four challenges C1–C4).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_blind_gate_and_metrics`** → targets `sp_oracle_blindness`. *proposed_approach:* Deliberately restrict the acceptance oracle to rebased fail-to-pass plus regression tests only (no linting, no import-structure checks), while independently running a static-analysis extractor (import-graph cycles, frozen import-linter layering contracts, architectural-smell detector, complexity/coupling metrics, duplication ratio) after every accepted step. *key_insight:* Because the gate can be shown, by a static scan of its own test files, to contain zero assertions over import-graph structure or module boundaries, any measured Φ change is by construction a case the oracle could not have seen — the isolation is definitional, not statistical. *hypotheses:* ["A static scan of every task's gate test files across the studied repositories finds zero assertions referencing import-graph structure, module boundaries, or layering — confirming the acceptance signal is structurally uninformative by construction, not merely in practice."]
- **`m_counterfactual_design`** → targets `sp_counterfactual_definition`. *proposed_approach:* Run the identical, chronologically ordered task sequence twice — once through the coding agent, once through the original human-authored gold patches — under identical rebasing/attrition rules, and define agent-attributable erosion strictly as the excess of the agent arm's structural trend over the human-gold arm's trend on the shared completed-task intersection. *key_insight:* Any structural growth a correct solution necessarily requires (a feature genuinely needing a new cross-module call) appears in both arms and cancels in the contrast; only the arm-to-arm difference is attributed to the agent. *hypotheses:* ["The agent arm's fixed-effect trend exceeds the human-gold arm's trend, for at least two of three primary structural metrics, by a pre-registered effect-size floor on the shared task-intersection contrast.", "Within-arm-only drift, without the counterfactual contrast, is not by itself sufficient evidence of agent-attributable erosion — demonstrated by at least one studied trajectory pair where within-arm drift is present in both arms at statistically indistinguishable rates."]
- **`m_longitudinal_drift_model`** → targets `sp_slow_drift_detection`. *proposed_approach:* Fit per-metric trajectories with trajectory-level random slopes/intercepts (mixed-effects), a per-trajectory nonparametric monotone-trend test, and a discrete-time survival model for time-to-first-new-violation with censoring for trajectories that never violate. *key_insight:* Random effects absorb step-to-step noise within a trajectory so a small compounding signal isn't swamped by patch-size variability, while the survival framing (adapted from turn-level hazard modeling of conversational degradation) converts "does it eventually erode" into a time-resolved, censoring-aware quantity instead of an endpoint check. *hypotheses:* ["Per-trajectory Mann-Kendall trend tests and the mixed-effects slope estimate agree in sign for at least 80% of trajectories exhibiting any drift — i.e., the two independent statistical readings of 'is this trajectory drifting' are not in tension."]
- **`m_attribution_and_mechanism`** → targets `sp_attribution_under_cost`. *proposed_approach:* Cross a small, deliberately contrastive factorial (agent configuration × task type × ordering, with seeds) with a per-patch feature profiler (cross-layer import edges, duplication delta, edit locality) computed for every accepted patch in both arms; regress per-step metric deltas on these patch features within trajectories, and regress trajectory-level erosion rate on the factorial conditions. *key_insight:* Attribution doesn't require more trajectories if some of the signal can be extracted *within* the trajectories already run — patch-level features supply a second, cheaper attribution channel that doesn't scale with the factorial's combinatorial cost. *hypotheses:* ["Removing the patch-level mechanism features (cross-layer imports, duplication delta, edit locality) from the within-trajectory delta regression drops its explained variance by at least half, demonstrating these three features are load-bearing carriers of the measured drift rather than incidental correlates.", "At least one of the four declared factors (agent configuration, task type, ordering, lagged prior-erosion state) attains a significant likelihood-ratio test against the null mixed model, net of the other three, demonstrating erosion rate is condition-dependent rather than uniform across the studied factorial."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold — but one method carries two headline claims and needs a one-line justification for why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_counterfactual_design.hypotheses", anti_pattern: null, comment: "The two hypotheses here (agent-excess-over-human, and within-arm-drift-insufficiency) are the paper's two most central claims about what counterfactual erosion even means. Worth stating explicitly why one design produces both, so this doesn't read as scope creep bundled into a single method."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_counterfactual_design.key_insight` extended: "...one experimental design — running both arms on the identical task sequence and fitting a single step×arm specification — yields two separately falsifiable estimands: the human-gold arm's own trend (tests whether the task sequence itself requires structural growth, independent of the agent) and the agent-vs-human interaction term (tests whether the agent adds excess erosion beyond that baseline requirement) — one instrument, two readouts, not two mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **6 hypotheses total** (1 + 2 + 1 + 2 across the four methods respectively — `m_counterfactual_design` and `m_attribution_and_mechanism` each carry two, per the refiner's one-instrument-two-estimands justification above), mixing instrument-validity claims (gate blindness, trend-test agreement) with the study's headline empirical predictions — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- SWE-bench Verified, repo-grouped chronological sequences (primary repos: django/django, sympy/sympy, astropy/astropy — the densest-coverage repositories per digest N6) — *justification:* real, chronologically dateable issue-derived tasks on Python repositories with declarable import-layer architectures, letting a serial sequence be constructed on a real development history rather than a synthetic one.
- (draft initially listed SWE-bench Lite with justification only "digest N8 lists it as a secondary dataset source" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Human-gold control (B0) — the actual developer PR patches applied serially under identical ordering, rebasing, and attrition rules; the necessary control for every agent-attributable-erosion claim.
- Single-shot control (B-alt, `rw_swebench`'s protocol reused per Stage 3) — the same agent, same backbone, same retry budget, solving each task from its original base commit with no accumulated history; rules out "erosion is just the sum of per-patch damage, not sequence-amplified."

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_gate_blindness_verified` | `sp_oracle_blindness` | "A static scan of every task's gate test files across the studied repositories finds zero assertions referencing import-graph structure, module boundaries, or layering — confirming the acceptance signal is structurally uninformative by construction, not merely in practice." |
| `rq_agent_excess_erosion` | `sp_counterfactual_definition` | "The agent arm's fixed-effect trend exceeds the human-gold arm's trend, for at least two of three primary structural metrics, by a pre-registered effect-size floor on the shared task-intersection contrast." |
| `rq_counterfactual_necessity` | `sp_counterfactual_definition` | "Within-arm-only drift, without the counterfactual contrast, is not by itself sufficient evidence of agent-attributable erosion — demonstrated by at least one studied trajectory pair where within-arm drift is present in both arms at statistically indistinguishable rates." |
| `rq_trend_test_agreement` | `sp_slow_drift_detection` | "Per-trajectory Mann-Kendall trend tests and the mixed-effects slope estimate agree in sign for at least 80% of trajectories exhibiting any drift — i.e., the two independent statistical readings of 'is this trajectory drifting' are not in tension." |
| `rq_mechanism_loadbearing` | `sp_attribution_under_cost` | "Removing the patch-level mechanism features (cross-layer imports, duplication delta, edit locality) from the within-trajectory delta regression drops its explained variance by at least half, demonstrating these three features are load-bearing carriers of the measured drift rather than incidental correlates." |
| `rq_factor_attribution` | `sp_attribution_under_cost` | "At least one of the four declared factors (agent configuration, task type, ordering, lagged prior-erosion state) attains a significant likelihood-ratio test against the null mixed model, net of the other three, demonstrating erosion rate is condition-dependent rather than uniform across the studied factorial." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E3 numbers and the walking-skeleton go/no-go gates as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason tied to a specific RQ.
- comments:
  - `{severity: major, field: "datasets[SWE-bench Lite]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest N8 lists it as a secondary dataset source' says nothing about which RQ needs it or why Verified alone doesn't suffice."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "SWE-bench Lite (secondary) — *justification:* used specifically to construct the second, permuted-order sequence needed for `rq_factor_attribution`'s ordering factor when a given repository's Verified-instance density is too thin to support two independent chronological orderings; without it, ordering could only be tested confounded with repository choice."
- `changes_made`: gave SWE-bench Lite's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the stage-1 critique specifically caught and removed a leaked statistical procedure from `objective`).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_oracle_blindness.source_limitation_ids`, `sp_counterfactual_definition.source_limitation_ids`, `sp_slow_drift_detection.source_limitation_ids` ∈ Stage 3 limitations ✓; `sp_attribution_under_cost.source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (per-step trajectories, within-arm reading, counterfactual-relative reading, factor+mechanism attribution) are each reachable: trajectories/within-arm via `sp_oracle_blindness`+`sp_slow_drift_detection`, counterfactual-relative reading via `sp_counterfactual_definition`, factor+mechanism attribution via `sp_attribution_under_cost` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs; recount: **6 Stage-5 hypotheses → 6 Stage-6 RQs**, one-to-one, verbatim.

**What was hardest:** the recurring tension was **not disagreement about facts** (the seed material — `digest.md`'s N5/N6/N8 plus `paper.md`'s Steps 5/6 — is unusually well-specified and already internally cross-referenced) but **scope discipline**: repeatedly checking whether a stage-5/6 hypothesis was quietly restating `paper.md`'s own already-finished Step 6 rather than adding something this schema's structure specifically demands (e.g., the gate-blindness static-scan claim and the trend-test-agreement claim are instrument-validity hypotheses that `paper.md`'s Assumptions table (A3, A6) gestures at as pre-registered checks but never states as falsifiable Stage-5-style hypotheses in their own right).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md` including its Phase A re-run section, `taste_audit.md`; no `design_review.md` exists). Every finding enumerated below with disposition. A prior attempt at this pass was interrupted before writing anything; this round verified its observation ("both stage-review fixes applied") and completed the remaining work.

| # | Source | Finding | Disposition |
|---|---|---|---|
| 1 | stage_review.md, Stage 2 REVISE | Related Work opening used Bridge-Opportunity-shaped "separate literatures... no work has yet connected the two" framing, contradicting the taste audit's 🟢 verdict | Verified already applied — instrument-gap framing naming SWE-bench and Sas et al. (2021) present in `paper_draft.md` (Intro ¶3 and Related Work opening) and `paper_draft.tex`; no residual "separate literatures" wording anywhere. No change needed. |
| 2 | stage_review.md, Stage 4 REVISE | RQ4's 80% sign-agreement target had no minimum qualifying-trajectory count; could silently collapse to a vacuous or underpowered set | Verified already applied — N ≥ 10 contingency with inconclusive-below-threshold reporting present in `paper_draft.md` (RQ4 Setup/Expected outcome/Falsification/Metrics), `paper_draft.tex`, and `experiment_design.md` (RQ4 sample-size rationale). No change needed. |
| 3 | stage_review.md, Phase A re-run item 1 | Digest self-verification resolve-count annotation stale (10/10) after N3 addition | Verified already applied in `digest.md` (11/11). No change needed. |
| 4 | stage_review.md, Phase A re-run item 2a | `reference_candidates.jsonl` in pre-canonical flat schema, no verdicts | Verified already applied — 159 records, all carrying a `verdict` field. No change needed. |
| 5 | stage_review.md, Phase A re-run item 2b | digest N3 citation keys unresolvable in cache | Verified already applied — 9 backfilled selected records logged; residual null-pdf limitation remains flagged (deferred to pre-Phase-E fetch, per the review's own disposition). No change needed. |
| 6 | stage_review.md, Phase A re-run item 2 (freshness bonus) | Method-twin arXiv:2607.01855 required concede-and-differentiate handling | Verified already applied — N3 work #11 and N4 limitation #11 present in `digest.md`. Per the review's own prescription ("fixed at source... never a silent related-work paragraph"), no `paper_draft.md` Related Work paragraph was added. No change needed. |
| 7 | stage_review.md, Phase A re-run item 5 | A6 missing inline gate label + consequence; no power assumption in ledger | Verified already applied — `paper.md` A6 carries `(S4, Step 9)` + consequence; A7 (power ≥ 0.8 against Cliff's δ ≥ 0.33, gate S6, INCONCLUSIVE-not-null) present and threaded into E1/E2 and Step 9. No change needed. |
| 8 | stage_review.md, Phase A re-run item 6 | Missing R1 estimand sentence; A2 instrument validation lacked full 5-step R2 sequence | Verified already applied — "Estimand (guidance.md R1)" sentence at top of `paper.md` Step 5; A2 rewritten with 2 raters, κ ≥ 0.7 AND ρ ≥ 0.4. No change needed. |
| 9 | taste_audit.md | Verdict 🟢 (no condition fired; scores 1/3/1); interpretation section is advisory only | No open findings — nothing to apply. |
| 10 | Cross-deliverable consistency check (this pass, task item 6) | `paper_draft.md`/`.tex` RQ2 said only "a pre-registered effect-size floor" while `experiment_design.md` and `paper.md` (A7/S6) pin Cliff's δ ≥ 0.33; RQ2's walking-skeleton go/no-go clause omitted the S6 power-projection gate added by the Phase A re-run | **Applied** — RQ2 Expected outcome now states the floor value (Cliff's δ ≥ 0.33 on per-trajectory slope pairs) and RQ2 Setup's walking-skeleton clause now includes the ≥ 0.8 power-projection gate, in both `paper_draft.md` and `paper_draft.tex`; PDF recompiled cleanly (12 pages). No hypothesis text touched. |

Cross-consistency verified after edits: 6 RQs in both `paper_draft.md` and `experiment_design.md`, one-to-one with the 6 verbatim Stage-5 target hypotheses (untouched); effect floor Cliff's δ ≥ 0.33, RQ4 margin 80% with N ≥ 10 contingency, RQ5 ≥ 50% variance-drop threshold, 54+6(+3) trajectory counts, and Holm correction consistent across `paper_draft.md`, `experiment_design.md`, and `paper.md`.
