# Discussion Trace — B2.1 (auto-research-discussion, Stages 1-6)

> Extracted verbatim from `discussion/pipeline.md` (the "# Auto-Research-Discussion Run — B2.1" section through "## Cross-stage consistency check"), per the updated `auto-research-discussion` skill's three-artifact deliverable split. This is the complete round-by-round critic/refiner record across all six stages that fed `../paper.md` and `paper_draft.md`/`.tex`/`.pdf`. Not re-run, not re-derived — moved as-is. `pipeline.md` retains its Phase Log (goal.md phase-gate tracking) and now points here for the Stage 1-6 transcript; see `experiment_design.md` for Stage 6's confirmed output rendered as a standalone protocol.

# Auto-Research-Discussion Run — B2.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Step 0–9), both pre-existing reverse-digest artifacts for seed **B2.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (a full N0–N12 digest plus a pre-registered formal spec with assumptions, hypotheses, and fallback wording already exist), so genuine disagreement surfaced but never required re-proposing from scratch.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5, verdict 🟢) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing contamination/leakage control in the Resource-archetype Experiments stage, and a buried-message paragraph in the Introduction) are already folded into the `paper_draft.*` files — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Determine whether, in a tool-use agent's plan→executor→tool/observation pipeline, injecting exactly one known fault while holding the other two components fixed causes the observed task failure to track the substituted component — and whether a candidate failure-attribution method's blame assignment can be mechanically verified against that by-construction ground truth, rather than checked only against human agreement.
- **Apparent inputs:** a base task set with a fixed agent scaffold, restricted to tasks that succeed reproducibly under replay; a library of fault injectors spanning plan-step corruption, tool breakage, and observation pollution; a candidate attribution method's blame prediction for a given failing trajectory.
- **Apparent outputs:** a per-trial ground-truth failure-locus label (certified only on outcome flip against a no-op control); outcome-flip rates per fault class; a component-attribution-accuracy score and confusion matrix per candidate method; a released labeled fault-trajectory benchmark.
- **Closest research areas:** LLM multi-agent failure attribution (WhoAndWhen, AgenTracer, DoVer); agent-benchmark reproducibility methodology (SelfEvolveBench, Terminal-Bench); step-level credit assignment for single-agent reasoning (CRM, FAPO); classical software fault-localization benchmarking (Defects4J) as the contrast case where backward annotation from a deterministic triggering test *is* possible.
- **In scope:** measuring, on tool-use agent trajectories with a fixed scaffold, whether failure tracks a substituted component, and whether existing/candidate attribution methods' blame survives mechanical verification against that manufactured ground truth. **Out of scope:** designing a new attribution algorithm meant to beat the others (the benchmark and protocol are the contribution, not a new detector); compound/multi-component faults; non-sandboxable live deployments.
- **Confidence: high.** As with the B5.5 run, the "repo" here is itself a prior reverse-digest plus a pre-registered formal specification (`digest.md`'s N0–N12 plus `paper.md`'s Step 0–9), already internally cross-referenced (C-ids ↔ M-ids ↔ RQ/H-ids) and already carrying its own asymmetry and taste self-check (`paper.md` Step 0 and Step 3). Reconstruction risk is low. The risk is instead *redundancy* with `paper.md`'s own Step 5/6 — this run's stage 5/6 are framed to add instrument-validity claims that `paper.md`'s Assumptions (A4, A5, A6, B-alt) gesture at but never states as this schema's own falsifiable, RQ-traceable hypotheses.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a tool-use agent pipeline whose plan, executor, and tool/observation channel jointly produce a trajectory, and given the ability to inject exactly one known fault (a corrupted plan step, a broken tool, or a polluted observation) into an otherwise reproducibly-succeeding run while holding the other two components fixed at their known-good state and replaying, determine (a) whether the resulting task failure tracks the substituted component rather than the other two, and (b) whether a candidate attribution method's blamed component matches this by-construction ground-truth label — i.e., whether an attribution claim can be mechanically verified rather than merely checked against human agreement.
- `input`: (1) a base task set together with a fixed agent scaffold, restricted to tasks verified to succeed reproducibly under repeated replay; (2) a library of fault injectors spanning three component classes (plan-step corruption, tool breakage, observation pollution); (3) a candidate attribution method's predicted blame component for a given failing trajectory.
- `output`: (1) a per-trial ground-truth failure-locus label, accepted only when the task outcome flips from success to failure against a matched no-op-substitution control; (2) the outcome-flip rate for each fault class relative to that control; (3) a component-attribution-accuracy score, and a full plan/tool/observation confusion matrix, for each candidate attribution method against the ground-truth labels; (4) a released corpus of labeled fault trajectories.
- `constraints`: ground truth is obtainable only by injecting a known fault into a reproducibly-succeeding run and checking whether the outcome flips — it cannot be reconstructed after the fact from a naturally-occurring failure; exactly one of the three pipeline components is faulted per trial, with the other two held at their checkpointed known-good state; each trial is replayed k times to average over agent stochasticity before a label is accepted.
- `objective`: A ground-truth label is accepted only if the injected fault's outcome-flip rate exceeds the matched no-op control's flip rate; a candidate attribution method's blame is scored correct only when it matches that accepted label.
- `study_type`: `empirical` — stated explicitly, not silently inferred. Digest N1's objective language ("diagnose," "validate... against ground-truth labels") and N12's own contribution-type rationale ("Not a SOTA table; a low-accuracy result on all methods is a valid benchmark finding") both point away from `technical` framing: the contribution is the substitution protocol and the labeled corpus it manufactures, not a new attribution algorithm proposed to beat the others.

**critique:**
- summary: Strong, evidence-traceable draft, but the objective silently assumes the premise-validation step succeeds uniformly across all three fault classes, which the seed's own pre-registered fallback logic explicitly denies.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective, as written, applies a single pass/fail gate across all fault classes at once. But paper.md's own pre-committed E1 fallback wording ('failure tracks the substituted component for executable faults... but not for semantic plan corruption... certified for the executable subset only') plans explicitly for a case where the premise holds for some classes and not others. An objective that doesn't allow for per-class certification would force stage 6 into either declaring a single global pass/fail (contradicting the seed's own fallback) or silently picking one interpretation without saying so."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "Output (3) says 'a candidate attribution method's blamed component' (singular) but digest M5 explicitly supports multi-component blame with precision/recall scoring — worth stating both scoring modes exist rather than implying only single-label blame is possible."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/spec — no new content needed).

### Refiner pass

- `objective` (refined): "A pipeline component's ground-truth label is certified **class by class**: a fault class is accepted as certified only if its outcome-flip rate exceeds the matched no-op control's flip rate by a pre-specified margin, and a class that does not clear this margin is reported as *uncertified* rather than folded into a single global verdict. Within the certified classes only, a candidate attribution method's blame is scored correct when it matches the accepted ground-truth label — exact match for single-component blame, precision/recall when multi-component blame is permitted."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's notation): "Pipeline component slots K = {plan, tool, obs} around a fixed executor ε. Task t, scaffold A, run R(t) → (τ, y): trajectory τ, outcome y ∈ {succ, fail}. δ_c is a fault operator on component c ∈ K; δ_∅ is a no-op substitution. k independent replays from the injection checkpoint; flip(t, δ_c) = 1 iff the base run is majority-success and post-injection runs are majority-failure over k replays. Ground-truth label ℓ(τ) = c iff δ_c was applied and flip = 1, restricted to classes c whose FlipRate(δ_c) − FlipRate(δ_∅) clears the certification margin. Attribution method m: τ → ĉ ⊆ K (single- or multi-component)."
- `changes_made`: made the objective's certification criterion per-class rather than global; noted both single- and multi-component scoring modes exist; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: A wave of failure-attribution methods for multi-agent and tool-use systems has been proposed, but every one of them is validated against human-annotated or single-culprit blame labels rather than a known, injected causal ground truth — so a method can produce a plausible-looking blame assignment that is symptom-matching rather than causally correct, and no existing evaluation can currently tell the difference.
- `why_it_matters`: Practitioners debugging a failing agent pipeline need to know whether to fix the planner, the tool interface, or the observation handling — and they currently have no principled way to check whether an attribution tool's answer is trustworthy, because the tool's own validation set was itself labeled by human judgment or by a single-decisive-step heuristic, not by a controlled experiment. Establishing whether "failure follows the substituted component" is even a reliable premise is foundational, not incidental: intervention-based auto-debugging (DoVer) and counterfactual label generation (AgenTracer) already lean on a version of this premise without measuring its reliability across a plan/tool/observation taxonomy — so if the premise doesn't hold uniformly, every downstream attribution claim built on interventionist reasoning inherits an unverified assumption.
- `who_cares`: agent-system developers deciding where to invest debugging effort (planner vs. tool interface vs. observation handling); designers of the next generation of failure-attribution methods who need ground truth to validate against; researchers currently treating human-agreement or single-culprit labels as sufficient evidence that a new attribution method works.
- `evidence`: `[WhoAndWhen, OpenReview:GazlTYxZss]`'s own Who&When dataset is human-annotated, scored by LLM-judge agreement with those annotations; `[DoVer, OpenReview:mrEK16Jy6h]`'s own motivation argues the single-decisive-culprit assumption is structurally weak; `[AgenTracer, OpenReview:l05DseqvuD]` already injects faults into successful traces to manufacture labels by construction — the closest real precedent — but targets a single perturbed action for tracer training, not a controlled cross-component taxonomy; `[AutoLibra, OpenReview:4BjGVZ7Bxn]` and `[Terminal-Bench, OpenReview:a7Qa4CcHak]` both independently motivate the same "coarse outcome-based metrics" gap this seed targets.

**critique:**
- summary: Good, stake-specific motivation with real citations, but it motivates the attribution-accuracy question heavily while leaving one of stage 1's four confirmed outputs essentially unmotivated.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is a *released, reusable corpus* — not a one-off internal check. why_it_matters argues why validating attribution methods matters in general, but never explains why this needs to become a standing, released benchmark rather than a single internal experiment run once and discarded. Without that, a reader could reasonably ask 'why does this need to be a benchmark at all, rather than a one-time sanity check' — a real, unaddressed gap, especially since digest N12 itself treats the corpus (not the comparison) as the headline contribution."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...and because by-construction ground truth is expensive to manufacture — a reproducibility gate, multiple injection classes, k-replay certification, a human audit pass — but cheap to reuse once built, the value of solving this compounds specifically through release: every future attribution method, not only the ones evaluated here, can be checked against the same certified labels rather than each new method re-earning trust through its own bespoke human-agreement study. This is exactly the role a reusable, causally-grounded corpus is positioned to play for this community — the way Defects4J plays it for program-repair research, with the caveat (addressed later, not elided) that a natural-language agent fault is not a code-level bug with a deterministic triggering test, so the analogy motivates the *shape* of the artifact without importing its guarantees."
- `changes_made`: added the artifact-reuse/standing-resource argument, explicitly covering stage 1's fourth output and pre-empting the "why not a one-off check" objection.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — the digest's N3/N4 already engaged each one at the approach + limitation level (full motivation/method text read, not title-only). No landscape-only entries are padded in.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_whoandwhen` | Anon., WhoAndWhen (OpenReview:GazlTYxZss) | **true** | Blame is scored by LLM-judge agreement with human-annotated decisive-error labels — validated against human judgment, not a known injected cause. |
| `rw_dover` | Anon., DoVer (OpenReview:mrEK16Jy6h) | **true** | Its own motivation argues the single-decisive-culprit assumption is structurally weak, but it offers no standardized, causally-grounded corpus spanning a plan/tool/observation taxonomy against which *any* method's accuracy can be scored. |
| `rw_agentracer` | Anon., AgenTracer (OpenReview:l05DseqvuD) | true | Injects faults into successful traces to manufacture labels by construction — closest real precedent — but the injection targets a single perturbed action for tracer-training supervision, not a controlled hold-two-swap-one protocol across a fault-class taxonomy, so it reports no per-component-class attribution-accuracy measurement. |
| `rw_selfevolvebench` | Anon., SelfEvolveBench (OpenReview:2H03gm4Rq6) | false (validates reproducibility, not attribution) | Validates task solvability/reproducibility by replay, not a ground-truth causal fault locus. |
| `rw_terminalbench` | Anon., Terminal-Bench (OpenReview:a7Qa4CcHak) | false | Grades final container state and tags failures with a coarse execution/coherence/verification taxonomy — no causal locus fixed by injection. |
| `rw_autolibra` | Anon., AutoLibra (OpenReview:4BjGVZ7Bxn) | false | Induces interpretable behavioral metrics from human feedback; motivates the same coarse-outcome-metric gap but never validates step localization against an injected fault. |
| `rw_crm` | Anon., CRM (OpenReview:4DJoBOQNd0) | true | Assigns per-step causal-contribution reward via a survival model, but on single-model reasoning steps, not a multi-component agent pipeline where the fault may be a broken tool or polluted observation. |
| `rw_fapo` | Anon., FAPO (OpenReview:jhqqoimoWt) | true | Predicts the earliest erroneous step in a single rollout; same single-agent-reasoning scope limitation as CRM, no injected-fault validation. |
| `rw_defects4j` | Just et al., Defects4J (ISSTA 2014) | false (canonical anchor, not runnable baseline) | Supplies real-bug ground truth only for single-statement Java code faults with a deterministic triggering test; no analog exists for a semantic plan-step, tool-interface, or observation fault in a multi-step agent trajectory. |

**critique:**
- summary: Grounding and limitation specificity are solid, but one baseline label overstates practical availability without noting a real, pre-registered contingency.
- comments:
  - `{severity: major, field: "specific_related_works[rw_agentracer].is_potential_baseline", anti_pattern: "weak justification (fails the rubric's 'is this baseline candidate reasonable' check)", comment: "Marking AgenTracer flatly `true` implies it can always be run as an accuracy comparator. But paper.md's own Assumption A6 states it explicitly: 'AgenTracer used only if weights/prompts are public, else dropped with a stated note.' As drafted, the baseline entry doesn't carry that condition, so a downstream reader (or Stage 6) could treat it as unconditionally runnable, which the seed's own feasibility analysis already disclaims."}`
- decision: `move_to_refiner` (a wording-precision fix — AgenTracer's role as design precedent for M3's labeling trick is unaffected).

### Refiner pass

- `rw_agentracer.is_potential_baseline` retained `true`, but the field's accompanying note is sharpened: "Runnable as an accuracy comparator only if its trained tracer's weights or prompts are publicly released; if not, it is retained purely as the design precedent for the outcome-flip labeling trick (borrowed into this paper's ground-truth gate) and dropped from the accuracy-comparison table with a stated availability note — per the seed's own pre-registered contingency."
- `changes_made`: attached AgenTracer's conditional-availability caveat directly to its baseline entry instead of leaving it implicit.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The closest candidate — `rw_whoandwhen`/`rw_dover`'s shared limitation ("does failure track the substituted component, validated causally rather than by human agreement") — is not a distinct framing-tier check; it restates this paper's own core mechanism-tier question, already covered end-to-end by Stage 6's `rq_component_flip_tracking`. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4):

- **`sp_causal_entanglement`** — *description:* Determine which single pipeline component (plan, executor/tool, or observation) is the true causal source of an observed task failure, when the components are architecturally entangled — the plan conditions what the executor attempts, which conditions which tools are invoked and what observations return. *why_it_is_a_problem:* Any attribution method applied to a passively-observed failing trajectory risks confusing which component merely looks anomalous downstream with which component is actually responsible upstream — a problem that holds even with unlimited data, because the correlation between components is never broken by an intervention. *technical_challenge:* Correlational cues are not causal evidence on their own, since each entangled component's output is itself shaped by the components upstream of it; separating true cause from downstream symptom requires an intervention that breaks the entanglement, not a better classifier over the same passively-observed trajectory. *source_limitation_ids:* `["__novel__"]`.
- **`sp_substitution_confound`** — *description:* Ensure that the act of substituting one component while nominally holding the other two "fixed" does not itself introduce a new confound — a different plan wording can perturb the executor's behavior even though the executor's weights are unchanged, and ordinary agent stochasticity can flip an outcome independent of the injected fault. *why_it_is_a_problem:* If the substitution protocol itself is a source of unaccounted variance, an observed outcome flip cannot be attributed to the injected fault with confidence — the instrument meant to manufacture ground truth would be silently mislabeling noise as a causal effect. *technical_challenge:* There is no way to guarantee a swap is "clean" by construction alone; detecting whether the protocol itself contributes false positives requires a matched control that undergoes the identical replay procedure without any injected fault, compared against the treatment arms. *source_limitation_ids:* `["__novel__"]`.
- **`sp_label_construction`** — *description:* Build a fault-injection library spanning plan corruption, tool breakage, and observation pollution that is unambiguous enough to label with a single component, realistic enough to be informative, and scalable enough to support statistical comparison across attribution methods. *why_it_is_a_problem:* A benchmark whose faults are too synthetic, too ambiguous, or too small in scale would not support the comparison it exists to enable — no prior corpus scores a continuous cross-component failure-locus label at all. *technical_challenge:* Injecting a fault does not guarantee the run actually fails for that reason (inject ≠ cause), and a fault template can straddle categories (a polluted observation that also functionally breaks a tool) — both properties can only be verified empirically, not by design inspection alone. *source_limitation_ids:* `["lim_unvalidated_ground_truth", "lim_agentracer_narrow_scope", "lim_no_causal_locus", "lim_defects4j_domain_gap"]`.
- **`sp_causal_distance`** — *description:* Score how accurately a candidate attribution method identifies the true faulty component when the observable failure symptom may be temporally and causally distant from the injected fault, and cascading effects can make an innocent downstream component look faulty. *why_it_is_a_problem:* A method that performs well when fault and symptom are adjacent may fail once effects have propagated through several intervening steps — an aggregate accuracy number would hide exactly this failure mode. *technical_challenge:* No single statistic separates genuine causal reasoning about a distant fault from confident-sounding symptom-matching; distinguishing them requires comparing each method's blame against ground truth across trajectories where fault-to-symptom distance varies, not one overall accuracy number. *source_limitation_ids:* `["lim_steplevel_precision"]`.

**critique:**
- summary: Coverage checks out (jointly solving all four would deliver stage 1's four outputs); the two novel sub-problems risk reading as the same underlying concern twice.
- comments:
  - `{severity: minor, field: "sp_causal_entanglement / sp_substitution_confound", anti_pattern: "overlap", comment: "Both are about 'isolating the true cause,' which can read as one sub-problem stated twice. They are genuinely distinct — one is a property of the *observational data-generating process* (architectural correlation that holds even under infinite passively-collected data), the other a property of the *experimental protocol itself* (a possible artifact introduced by the act of measuring) — but the current phrasing doesn't make that distinction explicit enough to survive a skeptical read."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_causal_entanglement.technical_challenge` sharpened to end with: "...this is a property of the **data-generating process**: no amount of additional passive observation resolves it, because the entanglement is architectural, not a sampling artifact."
- `sp_substitution_confound.technical_challenge` sharpened to end with: "...this is a property of the **measurement protocol itself**, distinct from architectural entanglement — even a perfectly disentangled system could still yield a false-positive flip if the swap mechanism or agent stochasticity, not the injected fault, is what moved the outcome."
- `changes_made`: made the data-generating-process-vs-measurement-protocol distinction explicit in both technical_challenge fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; 2 sourced from related-work limitations — one, `sp_label_construction`, from four limitations jointly — 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_fault_injection_library`** → targets `sp_label_construction`. *proposed_approach:* A parameterized generator library across three fault categories (plan-step deletion/reorder/replacement, tool replacement with an error/empty/malformed stub, observation noise/contradiction/truncation injection), each emitting `(trajectory, injected_component, injected_step_index, fault_template_id)`. *key_insight:* Realism and label-unambiguity cannot be guaranteed analytically, but they can be turned into a checkable empirical audit rather than an assumed property of the generator design. *hypotheses:* ["Human auditors will agree with the constructed ground-truth failure-locus label for at least 80% of a sampled 200-trajectory audit set, per fault category."]
- **`m_substitution_harness`** → targets `sp_causal_entanglement`. *proposed_approach:* Checkpoint a reproducibly-succeeding run, hold two of {plan, executor/tool, observation} fixed at their recorded good state, swap in the faulty version of the third, and replay from the injection point (rewind-edit-reexecute) via an orchestrator-message-level edit layer. *key_insight:* Entanglement cannot be resolved by better post-hoc reasoning over the same trajectory; it can only be broken by an intervention that perturbs exactly one component while everything else replays from an identical checkpoint. *hypotheses:* ["For each of the three fault classes, the outcome-flip rate under substitution will exceed the matched no-op control's flip rate by at least 0.20 (absolute), each significant at α = 0.05 after correction across the three classes."]
- **`m_outcome_flip_gate`** → targets `sp_substitution_confound`. *proposed_approach:* Certify a ground-truth label only if the trajectory's outcome actually flips (majority success → majority failure over k replays) and only relative to a matched no-op-substitution control run through the identical replay procedure. *key_insight:* Anchoring the label to an *observed effect* rather than to the mere act of substitution is what prevents the swap mechanism or background stochasticity from being silently mislabeled as a causal effect. *hypotheses:* ["The no-op control's own outcome-flip rate will remain at or below 0.10 under k = 4 replays at temperature 0, confirming that background stochasticity alone does not manufacture false-positive labels."]
- **`m_attribution_battery`** → targets `sp_causal_distance`. *proposed_approach:* Apply every candidate attribution method (LLM-judge under WhoAndWhen's three context strategies, ablation/leave-one-out blame, DoVer-style intervention do-then-verify, a repurposed step-level localizer, and a random/majority-class control) uniformly to every certified trajectory, plus a budget-matched variant of the post-hoc judge that receives the same number of additional sampled resamples the intervention arm consumes in replay budget, without the ability to actually intervene. *key_insight:* Uniform application under matched compute accounting is what makes a method's apparent advantage attributable to genuine causal reasoning rather than to extra replay budget. *hypotheses:* ["Each non-trivial attribution method family will exceed the surface-heuristic floor's accuracy by at least 0.10 absolute on the certified corpus."]
- **`m_verification_scorer`** → targets `sp_causal_distance`. *proposed_approach:* Score every method's predicted component against the certified ground-truth label with exact-match top-1 accuracy and a full plan/tool/observation confusion matrix, computed overall and conditioned on fault class, with 95% bootstrap confidence intervals. *key_insight:* Reporting the full class-conditional confusion structure, not one pooled number, is what exposes cascade-induced misattribution specifically. *hypotheses:* ["The best-performing attribution method's overall accuracy will not exceed 0.90, with a 95% bootstrap CI upper bound below 0.95."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but `m_attribution_battery`'s design already supports a second, distinct falsifiable claim (the budget-matched compute-parity check) that isn't yet stated as its own hypothesis, and `m_verification_scorer` similarly under-states what its confusion-matrix output supports.
- comments:
  - `{severity: major, field: "m_attribution_battery.hypotheses", anti_pattern: "uncovered claim (the method's own proposed_approach describes a budget-matched control that the hypotheses list never tests)", comment: "proposed_approach explicitly builds a budget-matched judge variant specifically to separate causal-intervention access from raw compute — but the single listed hypothesis only tests whether real methods clear a trivial floor. The compute-parity claim this component was built for is left untested at the hypothesis level, which means it would fall off the chain by Stage 6 even though the mechanism to test it is already designed."}`
  - `{severity: minor, field: "m_verification_scorer.hypotheses", anti_pattern: null, comment: "The confusion matrix is reported 'conditioned on fault class' in proposed_approach, but the single hypothesis only makes a pooled ceiling-gap claim. Worth adding the class-conditional claim the design already supports (plan-level vs. tool-level accuracy) rather than leaving that comparison implicit."}`
- decision: `move_to_refiner` (both are additions the existing mechanism already supports, not redesigns).

### Refiner pass

- `m_attribution_battery.hypotheses` (extended, second hypothesis added): "The accuracy advantage of intervention-based methods over post-hoc judges will narrow to below 0.10 absolute once the judge is given an equal replay budget of passive resamples (the budget-matched control) — i.e., intervention access adds no attribution accuracy beyond an equal budget of passive resampling."
- `m_attribution_battery.key_insight` (extended): "...a single uniform application protocol — same trajectories, same certified labels, same compute accounting — yields two separately falsifiable estimands from one comparison: whether real methods clear a trivial floor at all (the benchmark has signal), and whether an apparent intervention advantage is explained by genuine causal reasoning or merely by extra compute — one battery, two readouts, not two mechanisms."
- `m_verification_scorer.hypotheses` (extended, second hypothesis added): "For the post-hoc judge family specifically, accuracy on plan-level faults will be at least 0.10 lower than on tool-level faults, reflecting the more diffuse causal propagation of plan-corruption effects."
- `m_verification_scorer.key_insight` (extended): "...the same scorer that produces one pooled ceiling-gap number also produces the class-conditional breakdown needed to test whether the shortfall concentrates in plan-level faults specifically — one scoring instrument, two readouts."
- `changes_made`: added one hypothesis each to `m_attribution_battery` and `m_verification_scorer`, with an explicit one-instrument-two-estimands justification for each, mirroring the load-bearing design each method's `proposed_approach` already specified.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **7 hypotheses total** (1 + 1 + 1 + 2 + 2 across the five methods respectively), matching the count of instrument-validity and headline empirical claims this benchmark-construction study needs — deliberate, per the stage-6 tier accounting below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. This paper proposes no new attribution algorithm; the candidate methods (LLM-judge, ablation, DoVer-style intervention, step-localizer) are the *population being characterized*, not competitors this paper is trying to beat. The floor/ceiling/budget-parity checks below are sanity checks on the measurement instrument itself ("does the procedure return a trivial answer on a trivial input"), which `stages.md` explicitly allows as mechanism-tier for empirical papers.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GAIA-style tool-use tasks — *justification:* supplies the base task pool from which reproducibly-succeeding runs are selected for injection; realistic multi-step tool-use scenarios are what makes the substitution protocol's findings relevant to deployed agents.
- Who&When (`[WhoAndWhen, OpenReview:GazlTYxZss]`) — *justification:* a naturally-failing, human-labeled comparison set; contrasts this paper's construction-based labels against human-annotated ones and directly addresses the threat that injected faults might not represent naturally-occurring failure distributions.
- The constructed injected-fault corpus (this work, `sp_label_construction`'s output) — *justification:* the paper's own released artifact; every RQ below is computed over it.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- WhoAndWhen LLM-judge (all-at-once / step-by-step / binary-search context strategies) — the standard post-hoc explanation approach being characterized.
- Ablation / leave-one-out blame — re-run with each component reset to its known-good state, observe which restores success.
- DoVer-style intervention do-then-verify — the standard interventionist comparator.
- FAPO/CRM-style step-level localizer, repurposed from single-agent reasoning to this multi-component setting.
- AgenTracer RL tracer — conditional on public weights/prompts (per Stage 3's sharpened role); dropped with a stated note otherwise.
- Random / majority-class control and the surface-heuristic floor (blame the component hosting the last step before the first observable error signal) — the trivial-answer checks.
- Budget-matched post-hoc judge — the compute-parity control isolating causal-intervention access from raw replay budget.

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_label_audit_agreement` | `sp_label_construction` | "Human auditors will agree with the constructed ground-truth failure-locus label for at least 80% of a sampled 200-trajectory audit set, per fault category." |
| `rq_component_flip_tracking` | `sp_causal_entanglement` | "For each of the three fault classes, the outcome-flip rate under substitution will exceed the matched no-op control's flip rate by at least 0.20 (absolute), each significant at α = 0.05 after correction across the three classes." |
| `rq_noop_stochasticity_bound` | `sp_substitution_confound` | "The no-op control's own outcome-flip rate will remain at or below 0.10 under k = 4 replays at temperature 0, confirming that background stochasticity alone does not manufacture false-positive labels." |
| `rq_floor_beat` | `sp_causal_distance` | "Each non-trivial attribution method family will exceed the surface-heuristic floor's accuracy by at least 0.10 absolute on the certified corpus." |
| `rq_compute_parity_control` | `sp_causal_distance` | "The accuracy advantage of intervention-based methods over post-hoc judges will narrow to below 0.10 absolute once the judge is given an equal replay budget of passive resamples (the budget-matched control) — i.e., intervention access adds no attribution accuracy beyond an equal budget of passive resampling." |
| `rq_ceiling_gap` | `sp_causal_distance` | "The best-performing attribution method's overall accuracy will not exceed 0.90, with a 95% bootstrap CI upper bound below 0.95." |
| `rq_plan_tool_asymmetry` | `sp_causal_distance` | "For the post-hoc judge family specifically, accuracy on plan-level faults will be at least 0.10 lower than on tool-level faults, reflecting the more diffuse causal propagation of plan-corruption effects." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already pre-registered E1–E4/A1–A6 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but two of the RQs are silently conditioned on a result that hasn't necessarily happened yet, and the draft doesn't say so.
- comments:
  - `{severity: major, field: "research_questions[rq_ceiling_gap, rq_plan_tool_asymmetry].setup", anti_pattern: "question_hypothesis_mismatch (implicit unstated precondition)", comment: "paper.md's own Assumptions section is explicit that E3/E4-equivalent claims are conditioned on E1 (rq_component_flip_tracking) having passed first — these RQs only make sense computed over the *certified* tier. As drafted, rq_ceiling_gap and rq_plan_tool_asymmetry don't state this dependency, so a reader could run them over an uncertified fault class (e.g., plan faults, if those fail certification) and get a number that looks meaningful but rests on ground truth this paper's own Stage 1 objective already said should be reported as uncertified, not silently included."}`
- decision: `move_to_refiner`.

### Refiner pass

- `rq_ceiling_gap.setup` and `rq_plan_tool_asymmetry.setup` (both amended): "Computed only over the certified tier established by `rq_component_flip_tracking`'s per-class flip-rate check; a fault class that fails certification is excluded from this RQ's accuracy pool rather than silently included, consistent with Stage 1's per-class certification objective."
- `changes_made`: made the certified-tier dependency explicit in both downstream RQs' setup fields, closing the gap between Stage 1's per-class objective (refined in Stage 1's own refiner pass) and Stage 6's accuracy-gap RQs.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the substitution harness, outcome-flip gate, and attribution battery only appear starting Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` / `lim_*` stable stage-to-stage (`rw_agentracer`'s baseline note was annotated, not renamed).
3. **Reference integrity** — `sp_label_construction.source_limitation_ids = ["lim_unvalidated_ground_truth", "lim_agentracer_narrow_scope", "lim_no_causal_locus", "lim_defects4j_domain_gap"]` ∈ Stage 3 ✓; `sp_causal_distance.source_limitation_ids = ["lim_steplevel_precision"]` ∈ Stage 3 ✓; `sp_causal_entanglement`/`sp_substitution_confound` = `["__novel__"]` with stated decisive-component justifications ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a **verbatim** match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (certified per-class ground-truth label, flip rate, method accuracy/confusion matrix, released corpus) are each reachable: the certified label via `sp_causal_entanglement` + `sp_substitution_confound` (→ `rq_component_flip_tracking`, `rq_noop_stochasticity_bound`), flip rate via the same pair, method accuracy/confusion matrix via `sp_causal_distance` (→ `rq_floor_beat`, `rq_compute_parity_control`, `rq_ceiling_gap`, `rq_plan_tool_asymmetry`), and the released corpus via `sp_label_construction` (→ `rq_label_audit_agreement`) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs and 0 framing-tier RQs.
6. **Hypothesis/RQ count recount** (explicit, per the exemplar's own caught off-by-one): Stage 5 hypotheses = `H_audit, H_flip, H_stoch, H_floor, H_budget, H_ceiling, H_asymmetry` = **7**. Stage 6 RQs = `rq_label_audit_agreement, rq_component_flip_tracking, rq_noop_stochasticity_bound, rq_floor_beat, rq_compute_parity_control, rq_ceiling_gap, rq_plan_tool_asymmetry` = **7**. 7 = 7 ✓ — one-to-one, no orphan hypothesis, no unsourced RQ.

**What was hardest:** as in the B5.5 run, the recurring tension was not disagreement about facts (the seed material — a full digest plus a pre-registered formal spec with assumptions and fallback wording — is unusually well-specified) but **scope discipline**: repeatedly checking whether a Stage 5/6 hypothesis was quietly restating `paper.md`'s already-finished Step 6 rather than adding something this schema's structure specifically demands. Two concrete instances: the no-op stochasticity bound (`paper.md`'s Assumption A4) and the budget-matched compute-parity check (`paper.md`'s "B-alt" control, described in prose but never numbered as its own hypothesis) both existed as assumptions/asides in the source spec and had to be *promoted* into this schema's own falsifiable, RQ-traceable hypotheses rather than left implicit.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Revision pass over the completed pipeline's review artifacts (`stage_review.md`, `taste_audit.md`,
> `design_review.md`). Historical rounds above are unchanged. A prior attempt at this same pass was
> interrupted mid-run (API limit) after it had already folded the `design_review.md`-driven spec
> updates into `paper_draft.md` and `experiment_design.md` but only partway into `paper_draft.tex`;
> this round completed the interrupted mirroring rather than redoing or duplicating it. Every
> finding across the three review files is listed below with its disposition.

**From `design_review.md` (adversarial design review, verdict NEEDS-REVISION):**

- F1–F13 and the 21-item "Fixes applied (2026-07-04)" batch → **already applied** to `paper.md` (19
  edits: class-matched `δ_∅^c` + identity tier `δ_id`, CR-1–CR-5 combination rules, cluster-robust
  inference + 0.30-alternative power statement, B-alt-2 contamination arm, B0-b frozen detector,
  severity-matched H4, budgeted harder tier, F-G1 trigger extension, versioning/longevity section)
  and `digest.md` (2 edits: N8, t4) by the design review's own fix pass — recorded in
  `design_review.md`, not re-applied here.
- Remaining item: *"paper_draft.md/.tex remain stale relative to paper.md edits"* → **applied
  (completed this round)**. The interrupted prior attempt had already propagated the spec updates
  into `paper_draft.md` (Problem Definition notation `δ_∅^c`/`δ_id`; Certification Gate two-tier
  control; Datasets versioned-tier release; Baselines frozen B0-b detector; Contamination-control
  paragraph; cluster-robust setups and the 0.30-alternative power statement in RQ2; two-tier RQ3;
  heuristic-ceiling branch in RQ4; cluster-robust RQ5; floor-excluded-from-max RQ6; severity-matched
  RQ7; third scaffold/backbone-specificity limitation in the Conclusion; bounded CO1 wording in
  contribution bullet 4) and into `experiment_design.md` (same content as RQ cards plus B0-a/B0-b/
  B-alt/B-alt-2 comparator specs and the CR-1–CR-5/F-G1 cross-cutting notes). This round completed
  the unfinished `.md`→`.tex` mirroring: RQ3 (class-matched arms + identity tier, 0.10/0.05 bounds,
  tier disambiguation), RQ4 (cluster-robust McNemar-style test + heuristic-ceiling branch), RQ5
  (cluster-robust paired test), RQ6 (cluster bootstrap resampling base tasks; B0-b excluded from
  the max; heuristic-sufficiency rate), RQ7 (cluster bootstrap + severity-matched pairs + downgrade
  and reversed-ordering wording), Conclusion (two → three limitations, adding scaffold/backbone-
  specific certification), and the pre-handoff checklist notation line (`δ_∅^c`, `δ_id`). Files:
  `paper_draft.tex` (this round); `paper_draft.md`/`experiment_design.md` (prior attempt, verified
  this round). Recompiled clean: exit 0, 14 pages, zero errors, zero unresolved citations.
- Remaining item: *"CO1's 'reusable asset' claim remains bounded to one scaffold"* → **applied**
  (prior attempt in `paper_draft.md` contribution bullet 4 + Conclusion; this round mirrored the
  Conclusion wording into `paper_draft.tex`). No multi-scaffold replication cell was added — that
  is a compute decision, so the claim wording was bounded instead, per the review's own either/or.
- Remaining item F2: *"digest + fetch-verify the 9 load-bearing reference records"* → **already
  resolved** by the "Reference-cache real-digest build — 2026-07-04 (second run)" (logged in
  `pipeline.md` Phase Log and `stage_review.md`): all 9 records now carry real
  `pdf_path`/`digest_path`/`id_resolves=true`; zero load-bearing records with null `digest_path`.
- Remaining item F8: *"PG-5 κ-gate disambiguation branch (κ_rr vs κ_rl)"* → **rejected — deferred
  by the review itself**: `design_review.md` explicitly declined to apply it ("deserves a human
  decision (it reclassifies a possible gate failure as a headline finding)"). Unilaterally changing
  A5/PG-5's pre-registered consequence semantics in `paper.md` is outside this revision pass's
  license; left open for a human decision before Phase B.
- Remaining item: *"Phase A should be re-run over the edited bundle"* → **already resolved in
  substance**: the post-edit runs logged in `pipeline.md` (reference-cache real-digest build,
  freshness sweep, Phases E–I on 2026-07-04) re-verified the previously-failed items (2: cache
  digests; 6: contamination control now in the binding spec as B-alt-2) against the edited bundle;
  the technical resume point remains Phase B, unchanged.

**From `stage_review.md`:**

- Stage 4 REVISE (missing contamination/leakage control) → **already applied** (contamination
  paragraph in `paper_draft.md`/`.tex`; later made binding in `paper.md` as B-alt-2 via
  design-review fix 13; carried in `experiment_design.md` Datasets + cross-cutting notes).
- Stage 5 REVISE (buried Introduction message) → **already applied** (topic-sentence-first
  Introduction paragraph 1, present in both `paper_draft.md` and `.tex`).
- Phase A checklist items 1/5/6 (absence comments, PRISM memory-citation removal, PG-1…PG-6 ids,
  R1 estimand, R2/A5 κ protocol, power/thin-cell rule) → **already applied** to
  `digest.md`/`paper.md` in the Phase A re-run.
- Phase F STOP (zero `\cite`/no refs.bib) → **already applied** (12 `\citep{}` calls,
  script-generated `refs.bib`, mirrored bracketed citations in `.md`).
- Phase G [moderate] (pipeline vocabulary leaking into the Concurrent-work paragraph) → **already
  applied** (rewritten in both `.md`/`.tex`); the three Phase G [minor] items required no fix.
- Phase G to-do (full statistical/benchmark-soundness/Claim–Code re-review; expand Conclusion
  Limitations into a fuller Threats-to-Validity section) → **rejected — moot for this pass**:
  explicitly conditioned on real `B_pilot/`/`results/` existing; no compute in this environment.
  Remains logged as the standing to-do for the real-results Phase G.

**From `taste_audit.md`:** verdict 🟢 in both the original audit and the 2026-07-04 Phase H
re-audit; no findings, no reframe requested → **nothing to apply**.

**Cross-deliverable consistency check (this round):** 7 RQs in `paper_draft.md` = 7 RQ cards in
`experiment_design.md` = 7 Stage-6 RQs above; all 7 target hypotheses in `experiment_design.md`
byte-identical to Stage 5/6's confirmed strings; effect floors/margins/bounds consistent across
`paper.md`, `paper_draft.md`/`.tex`, `experiment_design.md` (0.20 flip-rate margin powered at the
0.30 alternative; 0.10 no-op and 0.05 identity bounds; 0.10 floor/parity/asymmetry margins; 0.90
ceiling with CI upper bound < 0.95 and the `Acc(B0-b) ≥ 0.90` CR-1 branch; ≥ 30-task held-out
contamination subset with the 10-point flag; κ ≥ 0.7; ≥ 80-trajectory necessary cell floor with
cluster-bootstrap-simulated power ≥ 0.8 binding). One pre-existing, deliberate format divergence
left as-is: the `.md` names the three concurrent-work systems and uses bracketed author-year
citations, the `.tex` describes the same three anonymously with `\citep{}` keys — both are the
Phase G-approved wording for their respective formats.

### Deletion-audit addendum (2026-07-05)

An audit of the deleted review files (recovered from git HEAD: `stage_review.md`,
`taste_audit.md`, `design_review.md`) re-verified every disposition above against actual file
contents. All findings checked out as applied or explicitly dispositioned, with one gap: **F11's
first half** (design_review [NOTE]: "B-alt controls a rival for a claim that appears in no
hypothesis or claim-map row … either promote the intervention-vs-judge comparison to a
pre-registered (secondary) hypothesis with the existing downgrade wording as its fallback, or
delete the abstract clause"). Design-review fix 12 was explicitly "(F11 partial)" — it applied
only the Who&When label-space mapping — and the promote-or-delete half was neither applied to
`paper.md` (the abstract's budget-matched clause had no hypothesis or claim-map row there; by the
review's own staleness rule, RQ5 living only in `experiment_design.md`/`paper_draft.*` does not
discharge it for the binding spec) nor listed in the review's "Remaining" section nor
individually dispositioned in this ledger. **Applied now (promote branch, no invented content):**
`paper.md` B-alt now pre-registers the comparison as secondary hypothesis **H-sec**, quoting
verbatim the already-existing Stage-5 second hypothesis (= RQ5 `rq_compute_parity_control`'s
target hypothesis) with RQ5's existing test spec (certified tier, base-task-cluster-robust paired
bootstrap, BH alongside E2's grid, E2's powered-cell rule) and the existing pre-committed
compute-parity wording as its pass-outcome claim; a matching Claim–Evidence Map row was added for
the Abstract's budget-matched clause, and the map's footer updated to "H1–H4, H-sec, or a Step-5
definition". No `paper_draft.md`/`.tex` prose change was needed (RQ5 already present in both), so
no recompile was required.
