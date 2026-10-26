# Discussion Trace — B1.3: Milestone Satisfaction without Prerequisite State

> Extracted verbatim from `pipeline.md`'s Stage 1-6 transcript (this content previously lived inline in `pipeline.md`, before its Phase Log section was appended; moved here per the `auto-research-discussion` skill's "Final deliverables" spec so `pipeline.md` can stay a short phase-gate tracker). This is the complete round-by-round record — every draft, every critique with severities, every decision, every refiner pass — across all six stages, plus the final cross-stage consistency check. It fed the confirmed stage outputs that `paper.md` and `paper_draft.md`/`.tex`/`.pdf` were built from, and it is the audit trail for any "we considered X and rejected it in stage Y because Z" rebuttal material.

# Auto-Research-Discussion Run — B1.3 (autoclaude-style, repo-driven from digest.md + paper.md)

> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files — read `stage_review.md` for the reasoning behind those two fixes. (`pengsida-stage-reviewer` was added to the pipeline after this topic was first processed; this is a retrofit pass.)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B1.3**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (a full formal problem definition, pre-registered hypotheses with fallbacks, and its own taste self-audit already exist in `paper.md`), so genuine disagreement surfaced but didn't require re-proposing.

## Seed brief

- **One-sentence description:** Measure whether independent per-milestone verification in a multi-step agent task can be satisfied without the milestone's true prerequisite state ever holding — via out-of-order completion, step-skipping, or direct state injection — by comparing per-milestone verdicts against a disjoint terminal state-consistency oracle.
- **Apparent inputs:** a task spec `T=(Σ,V,E,Φ,Ω)` (state space, milestone set, prerequisite DAG, per-milestone verifiers, terminal oracle); candidate trajectories (honest topologically-valid ones and adversarially constructed reorder/skip/inject ones); for the natural-incidence question, real LLM-agent rollouts.
- **Apparent outputs:** per-milestone pass/fail verdicts; a terminal oracle verdict; the aggregate checkpoint-bypass rate, broken down by bypass strategy, graph topology, and (real-agent) natural incidence.
- **Closest research areas:** agent-benchmark verifier design and sufficiency (TED, WebArbiter); process/step reward model locality (StepORLM, LatentVeracity); prerequisite-DAG planning (XENON, GTool, DiffTaskGraph); benchmark shortcut-inflation findings (Gistify).
- **In scope:** measuring the existing independent-per-milestone-verification paradigm's bypass rate under an explicit prerequisite DAG, using both constructed adversarial trajectories and natural real-agent rollouts, on sandboxable domains with a computable canonical terminal state. **Out of scope:** proposing or training a new verifier design; open-ended domains with no well-defined terminal state; live/non-sandboxable deployments.
- **Confidence: high.** As with a mature reverse-digest seed, the "repo" here is itself a prior N0–N12 digest plus a pre-registered paper specification (`paper.md`) — already carrying its own formal problem definition (Step 5), pre-registered hypotheses with explicit fallbacks (Step 6), and its own asymmetry/taste self-check (Steps 0/2/3). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Step 5/6, which is why stages 5/6 below are framed as validating the **measurement instrument's own properties** (oracle validity, structural-vs-weak-checker attribution) — the assumptions `paper.md`'s A4 and B-alt control gesture at but never state as falsifiable stage-5-style hypotheses in their own right — not as re-deriving `paper.md`'s H1–H4 from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a multi-step agent task with an explicit prerequisite dependency graph over milestones, a set of per-milestone verifiers each scoped only to its own milestone's local signal (no read access to other milestones' provenance), and a separate terminal state-consistency oracle, determine whether a completion trajectory can pass every milestone verifier without ever establishing the prerequisite state each checkpoint is meant to certify — via out-of-order completion, step-skipping, or direct state injection — and measure the rate at which this occurs.
- `input`: (1) a task spec `T=(Σ,V,E,Φ,Ω)`: state space, milestone set, prerequisite DAG edges, per-milestone verifiers, terminal oracle; (2) candidate trajectories `τ` — both honest topologically-valid ones and adversarially constructed reorder/skip/inject ones; (3) for the natural-incidence question, real LLM-agent rollouts scored complete by the per-milestone verifiers.
- `output`: (1) per-milestone pass/fail verdicts (the all-pass indicator `A(τ)`); (2) the terminal oracle verdict `Ω(τ)`; (3) the checkpoint-bypass rate `ρ = P[A(τ)=1 ∧ Ω(τ)=0]`, broken down by bypass strategy, graph topology, and (for real rollouts) natural incidence.
- `constraints`: milestones must be independently, individually verifiable — verifiers have no read access to other milestones' provenance — for "bypass" to be well-defined; a canonical, independently-computable terminal state must exist so the oracle is a total function, disjoint in code from every per-milestone verifier.
- `objective`: a bypass-rate estimate is accepted as evidence about the verification paradigm only if the terminal oracle's own false-inconsistency rate, measured on honest trajectories, is bounded low.
- `study_type`: `empirical` — stated explicitly, not silently inferred: the seed's own core question ("中间里程碑 verifier 可否在不满足前置状态的情况下被逐个满足") and digest N12 already settle this as measurement/characterization of an existing verification paradigm's sufficiency, not a proposed fix.

**critique:**
- summary: Strong, evidence-traceable draft, but the objective has a real evaluability gap around what the measured rate actually certifies, and the output list is missing a field the objective itself depends on.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "'bounded low' names no threshold, and more importantly the objective doesn't state that any reported ρ is inherently a lower bound over a pre-registered sampling distribution, not a population-level or worst-case rate — digest C1/N10-t3 already flag this as a genuine, structural scope limit (a DAG over N milestones admits a super-linear number of reorderings/skip-patterns/injection points that no finite suite can exhaustively cover). Without stating this, a reader could read the objective as certifying 'the' bypass rate rather than a sampled lower-bound estimate, which is not what the design can support."}`
  - `{severity: minor, field: "output", anti_pattern: "fields_misaligned", comment: "The objective conditions acceptance on the oracle's false-inconsistency rate, but that rate isn't listed as one of the three outputs — a reader can't check the objective's own precondition without it being a first-class output."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A checkpoint-bypass rate is accepted as evidence about the verification paradigm's sufficiency only if (i) it is reported as a lower bound over a pre-registered trajectory-sampling distribution — never as an exhaustive or worst-case rate, since the bypass space is combinatorially large and only sampled — and (ii) the terminal oracle's own false-inconsistency rate, measured by manual audit of honest trajectories, does not exceed a pre-registered threshold; a rate measured against an oracle that fails this check is not reported as evidence of paradigm insufficiency."
- `output` (extended): added a fourth output — "(4) the oracle-audit false-inconsistency rate on honest trajectories, needed to interpret whether (3) reflects genuine paradigm insufficiency or oracle noise."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Task `T=(Σ,V,E,Φ,Ω)`. Trajectory `τ` induces terminal state `σ_τ`. Verifier `φ_k: view_k(τ)→{0,1}` for milestone `v_k`, scoped to local signal only; all-pass `A(τ):=⋀_k φ_k(τ)`. Oracle `Ω: σ_τ→{0,1}`, a total function comparing `σ_τ` to the canonical goal state `σ*_T`, disjoint in code from every `φ_k`. Bypass event `B(τ):=A(τ)=1 ∧ Ω(τ)=0`. Checkpoint-bypass rate `ρ:=P_{τ∼D}[B(τ)]` over a pre-registered trajectory distribution `D` — reported as a lower bound over `D`, not a population-level claim."
- `changes_made`: tightened `objective`'s evaluability conditions (threshold + lower-bound scope); added the oracle-audit rate as an explicit fourth output; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Independent per-milestone verification is the standard way multi-step agent benchmarks, reward signals, and deployment "task complete" judgments grade long-horizon tasks, but whether this local-checking paradigm is actually sufficient evidence of true task success — rather than something a trajectory can satisfy without ever establishing what each checkpoint is supposed to certify — has not been directly measured.
- `why_it_matters`: As multi-step agent benchmarks and RL reward shaping increasingly rely on per-milestone grading (file/state checks, unit sub-tests, tool-signature checks, DB-state comparisons) because directly verifying full end-to-end correctness is expensive, if a trajectory can satisfy every milestone checkpoint via reordering, skipping, or direct state injection without ever establishing the true prerequisite state, then scores, rewards, and completion judgments derived from this paradigm may systematically overstate real competence — the verifier itself becomes the attack surface, not the task. This is not hypothetical: prior work shows benchmark scores can be driven by shortcuts divorced from real capability (Gistify), and process/step reward models are already known to be locally consistent yet globally inconsistent (StepORLM). But no existing work directly quantifies how often this happens under an explicit prerequisite structure with an independent terminal ground truth — a corpus search across 11,683 papers found the ingredients but no direct measurement (digest N3 absence_comment).
- `who_cares`: Benchmark designers deciding whether per-milestone grading is a safe simplification; RL practitioners using milestone-based reward shaping for long-horizon agents; anyone treating "agent passed X of Y checkpoints" as evidence of real task completion.
- `evidence`: `[Gistify, OpenReview:nmdDgo4OXC]`'s own motivation argues SWE-bench/RepoBench-style evaluations can be passed via "memorized associations or retrieval shortcuts," so high scores don't imply deployment-ready ability; `[StepORLM, OpenReview:ZrgxU8WMmG]`'s own motivation argues process reward models "usually score steps independently," which is myopic because a step's correctness "often depends on later context"; `[WebArbiter, OpenReview:canA6Ef0RP]` shows checklist-based checkers reward "superficial compatibility." None of the three (nor any of the other five related works) measures a checkpoint-bypass rate under an explicit DAG with an independent terminal oracle — itself evidence the question is open.

**critique:**
- summary: Good stake-specific motivation with real citations, but coverage of stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1's output (3) is a bypass rate broken down by strategy, topology, and natural incidence — not one aggregate number. why_it_matters motivates why a bypass rate matters in general but never explains why the breakdown specifically matters, as opposed to a single headline 'bypass happens X% of the time' figure. A reader could reasonably ask 'why not just report one number and stop' — that's a real, unaddressed gap, and it's exactly the kind of distinction paper.md's own fallback structure (separate fallbacks for H1/H2/H3/H4) treats as carrying independent decision-relevance."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, collapsing this into one aggregate number would erase distinctions that are each independently decision-relevant: *which strategy* dominates tells a benchmark designer where to harden first (state-injection calls for provenance authentication; reordering/skipping call for execution-order checks — different fixes for different attack shapes); *whether topology modulates the rate* tells designers whether the risk grows with task complexity, i.e., whether deeper or more heavily-forked benchmarks are disproportionately exposed; and *natural incidence in real agents*, measured separately from the adversarially constructed rate, is what distinguishes a constructibility result (a latent, exploitable weakness) from an active measurement of unprompted misbehavior in today's deployed agents — the difference between 'this could be attacked' and 'this is already happening.' A single pooled rate would make exactly these operationally different conclusions indistinguishable from each other."
- `changes_made`: added the breakdown-matters argument, tying each of stage 1's promised breakdowns to a distinct, stated practical consequence.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation-id / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation_id (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_ted` | Anon., TED (OpenReview:fHsVNklKOc) | false (holistic LLM-judge over trajectories, not milestone-scoped) | `lim_ted_process_not_prerequisite` — documents the standard per-checkpoint grading mechanisms (DB-state, tool-signature, exact-match) and argues they under-measure interaction *process*, but its remedy is a holistic LLM-judge; it neither models an adversarial trajectory that satisfies each local checker without the prerequisite state, nor quantifies how often that happens. |
| `rw_xenon` | Anon., XENON (OpenReview:N22lDHYrXe) | false (planning aid, not an audit of verifier sufficiency) | `lim_xenon_gtool_planning_not_audit` — treats the prerequisite DAG as a planning aid to bootstrap/correct action ordering, but doesn't audit whether an independent milestone verifier can be satisfied while its graph prerequisites are unmet. |
| `rw_gtool` | Anon., GTool (OpenReview:bn47cqGQ7l) | false (same limitation as XENON) | `lim_xenon_gtool_planning_not_audit` (shared). |
| `rw_steporlm` | Anon., StepORLM (OpenReview:ZrgxU8WMmG) | **true** | `lim_steporlm_latentveracity_local_global` — correctly identifies step-wise verifiers are locally-scoped and can be globally inconsistent, but operates on linear reasoning/derivation chains graded against a final answer, with no explicit prerequisite DAG and no adversarial state injection; its proposed global signal is a learned LLM critic, not an independent state-consistency oracle used only as ground truth. |
| `rw_latentveracity` | Anon., LatentVeracity (OpenReview:eux1cp8GqC) | false | `lim_steporlm_latentveracity_local_global` (shared). |
| `rw_webarbiter` | Anon., WebArbiter (OpenReview:canA6Ef0RP) | false | `lim_webarbiter_gistify_better_checker_not_rate` — shows checklist/template checkers reward "superficial compatibility," but addresses this by proposing a better *checker* (a reasoning PRM), not by isolating and measuring the *rate* at which surface-satisfied per-milestone checks diverge from a separately-computed terminal ground truth. |
| `rw_gistify` | Anon., Gistify (OpenReview:nmdDgo4OXC) | false | `lim_webarbiter_gistify_better_checker_not_rate` (shared) — shows benchmark scores can be driven by shortcuts, addressed via a better *benchmark design* (execution-faithful compression), not a measured bypass rate. |
| `rw_difftaskgraph` | Anon., DiffTaskGraph (OpenReview:2HvgvB4aWq) | false | `lim_difftaskgraph_learned_not_oracle` — learns a prerequisite DAG and detects ordering mistakes, but its detection is a learned forecasting signal that presumes the learned graph is correct, not an independent oracle over task state; doesn't consider trajectories that spoof a milestone's surface signature without executing the prerequisite. |

**critique:**
- summary: Grounding is solid and every limitation is specific, not generic — but one baseline label needs scrutiny.
- comments:
  - `{severity: major, field: "specific_related_works[rw_steporlm].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "StepORLM's I/O framing is linear reasoning chains scored against a single final answer — genuinely different from this paper's multi-milestone DAG trajectories scored against a disjoint state oracle. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying StepORLM's own reported numbers are being compared against, which they are not and cannot be (different task, different ground truth)."}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — the *protocol* is still legitimately borrowable as a comparison arm).

### Refiner pass

- `rw_steporlm.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — StepORLM's own reported results are not compared against, and its task (linear chains, final-answer ground truth) is not this paper's task. Its **holistic post-hoc trajectory critique** is borrowed as a candidate *alternative verification-design arm* (does a single holistic check over the whole trajectory also miss what independent per-milestone verification misses, or does it catch it?) — a protocol structure to test in a natural extension, independent of StepORLM's own published results."
- `changes_made`: clarified StepORLM's baseline role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The closest candidate — "no corpus paper directly measures a checkpoint-bypass rate" (digest N3 absence_comment / Claim 4) — is a claim about corpus coverage already established by the search itself, not a framing-tier hypothesis this paper needs to re-verify experimentally, and it isn't a distinct check from this paper's own core measurement (already covered end-to-end as mechanism-tier RQs in Stage 6). Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus one genuinely novel decisive component):

- **`sp_combinatorial_coverage`** (C1) — *description:* Characterize the checkpoint-bypass rate from a finite, constructed trajectory sample despite a bypass space (reorderings × skip-patterns × injection points, over arbitrary DAG topologies) that grows super-linearly in the number of milestones. *why_it_is_a_problem:* any reported rate is only ever a sample from this space — presenting it as anything but an explicit lower bound would misrepresent what the design can support. *technical_challenge:* there is no way to exhaustively enumerate the bypass space for a nontrivial DAG, so the sampling procedure itself has to be structured (stratified by topology and strategy) rather than a convenience sample, or the direction of undercoverage can't even be characterized. *source_limitation_ids:* `["__novel__"]` — no cited work needs to solve this because none of them measures a bypass rate over a sampled adversarial-trajectory space in the first place.
- **`sp_verifier_locality`** (C2) — *description:* Establish, as an auditable property of the verifier implementation rather than an assumption, that per-milestone verifiers structurally cannot see whether a prior milestone's true prerequisite computation occurred versus merely its local success signal being present. *why_it_is_a_problem:* every claim in this paper rests on locality being a real, built-in property of the verifiers under test, not an incidental implementation gap that a slightly better local checker would close. *technical_challenge:* "locality" has to be operationalized as a checkable code-scope restriction (no read access to other milestones' provenance), not just asserted in prose. *source_limitation_ids:* `["lim_steporlm_latentveracity_local_global"]`.
- **`sp_provenance_authentication`** (C3) — *description:* Explain why direct state injection — writing a milestone's expected surface signature without executing the real operation — should be the bypass strategy hardest for a lightweight local checker to catch. *why_it_is_a_problem:* if injection isn't shown to specifically exploit provenance-blindness, "which strategy wins" is just an empirical curiosity rather than a diagnosis of *why* locality-scoped checking fails. *technical_challenge:* distinguishing "the prerequisite state was legitimately produced by executing prior steps" from "the state's observable surface signature was directly spoofed" requires authenticating causal history, which lightweight checkers (by construction, per C2) cannot do without becoming as expensive as full state tracing. *source_limitation_ids:* `["lim_webarbiter_gistify_better_checker_not_rate"]`.
- **`sp_oracle_validity`** (C4) — *description:* Establish that the terminal state-consistency oracle itself is trustworthy ground truth, not a second unverified measurement instrument whose own bugs could masquerade as bypasses. *why_it_is_a_problem:* an oracle that is as hard to specify correctly as the original task's success criterion could inflate (false inconsistencies) or hide (an overly lenient oracle) the very rate this paper reports. *technical_challenge:* validating an oracle requires an independent ground truth for the oracle's own verdicts (a manual audit), which is a separate measurement problem from validating the bypass rate itself. *source_limitation_ids:* `["lim_difftaskgraph_learned_not_oracle"]`.
- **`sp_structural_vs_weak_checker`** — *description:* Determine whether an observed bypass is caused by the structural fact that per-milestone verification is locality-scoped (sp_verifier_locality), or is merely an artifact of this study's own local checkers being weaker/lazier than what a careful benchmark designer would actually deploy. *why_it_is_a_problem:* without ruling out the weak-checker explanation, the paper's central claim ("independent per-milestone verification is structurally insufficient") is not distinguishable from the much weaker, uninteresting claim "this paper's toy checkers were easy to fool." *technical_challenge:* requires constructing the *strongest realistic* local checker per checker type — capability/compute-matched, but still milestone-scoped by construction — and showing the bypass survives against it, which is a different kind of evidence than simply reporting a rate against whatever checkers were built first. *source_limitation_ids:* `["__novel__"]` — this rival-explanation check is not raised by any cited work; it is a decisive component this paper's own design (`paper.md`'s B-alt control) requires to make its central claim defensible.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's objective); one pair of sub-problems risks reading as the same point twice.
- comments:
  - `{severity: minor, field: "sp_verifier_locality / sp_structural_vs_weak_checker", anti_pattern: "overlap", comment: "Both are, on a quick read, 'about locality causing bypass,' which can look like the same sub-problem stated twice. They are genuinely distinct — one establishes that locality is a real, auditable property of the verifiers (an existence/definitional problem), the other asks whether an *observed rate* is attributable to that structural property versus to this study's own checkers being unrepresentatively weak (an attribution/confound problem) — but the descriptions don't make the existence-vs-attribution distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_verifier_locality.technical_challenge` sharpened to end with: "...this is an **existence/definitional** problem — showing locality is a real, checkable property of the verifier code — not yet a claim about what causes any specific measured rate."
- `sp_structural_vs_weak_checker.technical_challenge` sharpened to end with: "...this is an **attribution** problem distinct from sp_verifier_locality's existence claim — even granting that verifiers are locality-scoped, a measured bypass rate could still be an artifact of this study's specific checker implementations being weak, and only a strongest-checker control can rule that out."
- `changes_made`: made the existence-vs-attribution distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 3 sourced from related-work limitations, 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_topology_stratified_sampling`** → targets `sp_combinatorial_coverage`. *proposed_approach:* Parameterize the task generator over graph-topology features (prerequisite-chain depth, node in-degree/branching factor) and generate bypass traces stratified across these topology bins and across all three bypass-strategy families (reorder/skip/inject), rather than an unstructured convenience sample; report the measured rate explicitly as a lower bound over the sampled distribution. *key_insight:* the combinatorial bypass space can't be exhaustively enumerated, but a stratified — not exhaustive — sample lets the rate be decomposed along exactly the structural axes (topology, strategy) that determine where bypass concentrates, turning "we can't cover everything" into "we can characterize where it concentrates." *hypotheses:* ["In a logistic regression of the bypass outcome on prerequisite-chain depth and node in-degree over the scale-up suite (≥200 tasks), at least one predictor will show an odds ratio > 1.2 per unit with Wald p<0.05 (Holm-corrected across the two predictors), indicating deeper or higher-fan-in prerequisite structure raises bypass odds."]
- **`m_locality_scoped_verifiers`** → targets `sp_verifier_locality`. *proposed_approach:* Implement each per-milestone verifier with a statically-audited scope restriction — reading only its own milestone's local signal, with no code path granting read access to other milestones' provenance — mirroring the checker types real benchmarks use (file/existence, regex/substring, unit sub-test, tool-signature, DB-state, exact-match), and measure the gap between the all-pass verdict and the disjoint terminal oracle as the direct operationalization of locality's consequence, applied to both constructed adversarial trajectories and natural real-agent rollouts. *key_insight:* locality isn't assumed or argued qualitatively — it's built into the verifier code as an auditable static property, so any measured gap is attributable to that scoping choice rather than an accidental implementation leak; and the same instrument, applied to two different trajectory distributions (adversarially constructed vs. natural agent rollouts), yields two separately falsifiable estimands from one measurement design. *hypotheses:* ["The measured aggregate checkpoint-bypass rate ρ̂ will be significantly greater than zero — ρ̂ ≥ 0.10 with Wilson 95% lower bound > 0.05 — over at least 300 constructed reorder/skip/inject trajectories on the pilot DAG suite (one-sided exact binomial test, p<0.05), demonstrating that independent per-milestone verification is not a sufficient proxy for true multi-step task success on this suite.", "Real LLM agents will naturally (non-adversarially) produce rollouts scored complete by every per-milestone verifier yet failing the terminal oracle at a non-zero but lower incidence than the constructed rate — natural incidence ρ̂_nat ≥ 0.02 with Wilson 95% lower bound > 0, over at least 200 verifier-complete real-agent rollouts, with a two-proportion test confirming ρ_nat < ρ_constructed."]
- **`m_injection_provenance_probe`** → targets `sp_provenance_authentication`. *proposed_approach:* Within the injection-strategy trace family, hold the milestone's local surface signature exactly fixed (touch the expected file, echo the expected pattern, insert the expected DB row) while never executing the real prerequisite operation, and compare the resulting per-strategy bypass rate against reordering and step-skipping. *key_insight:* injection is the sharpest test of provenance-blindness specifically because it forges the local success signal directly, unconstrained by needing an executable control-flow path the way reordering and skipping still are. *hypotheses:* ["The state-injection strategy's bypass rate will exceed both the reordering and step-skipping strategies' rates by at least 10 percentage points (pairwise two-proportion z-tests, Holm-corrected p<0.05 across the three pairs), because injection forges the milestone's local success signal directly without requiring an executable control-flow path."]
- **`m_strongest_checker_control`** → targets `sp_structural_vs_weak_checker`. *proposed_approach:* Replace each per-milestone verifier with the richest realistic local check per checker type (fullest DB-state comparison, strictest exact-match, deepest unit sub-test) — still milestone-scoped by construction, capability/compute-matched to the standard suite — and re-measure the injection-strategy bypass rate against this control. *key_insight:* if bypass survives even against the strongest local checker anyone would realistically deploy, the cause is the structural fact that the checker is milestone-scoped at all, not that this study's checkers happened to be lazy. *hypotheses:* ["Against the strongest-local-checker control (the richest realistic, still milestone-scoped, capability/compute-matched local check per checker type), the injection-strategy checkpoint-bypass rate remains at least half its value under the standard-strength checker suite — demonstrating that the measured bypass is attributable to structural locality rather than to lazy or weak checker implementations."]
- **`m_disjoint_oracle_with_audit`** → targets `sp_oracle_validity`. *proposed_approach:* Implement the terminal oracle as a total function of final task state (filesystem hash-set, DB row-set, or deterministic program output) sharing no code with any per-milestone verifier, and validate it via a manual stratified audit of a sample of oracle verdicts on honest, topologically-valid trajectories (which should uniformly pass both the verifiers and the oracle). *key_insight:* an oracle's trustworthiness is itself an empirical question, not a design assumption — the honest-trajectory audit is the one dataset where the "correct" answer is known independently of the oracle, making it the right instrument to bound the oracle's own error rate. *hypotheses:* ["A manual stratified audit of 50–100 oracle verdicts on honest (topologically-valid) trajectories will find a false-inconsistency rate of at most 5%, and the honest-trajectory bypass rate itself will be below 1% — establishing that the terminal oracle is disjoint-code-validated ground truth rather than a source of inflated bypass counts."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but one method is carrying two headline claims and needs a one-line justification for why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_locality_scoped_verifiers.hypotheses", anti_pattern: null, comment: "Two hypotheses here (the constructed-rate existence claim, and the natural-incidence claim) are two of the paper's four central empirical claims, bundled into one method. Worth stating explicitly why one mechanism produces both, so this doesn't read as scope creep."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_locality_scoped_verifiers.key_insight` extended: "...one measurement instrument — the locality-scoped verifier suite plus disjoint oracle — applied to two different trajectory distributions (adversarially constructed traces vs. natural real-agent rollouts) yields two separately falsifiable estimands: the constructed-rate hypothesis tests whether bypass is *possible at all* under adversarial construction, the natural-incidence hypothesis tests whether it *already occurs* unprompted — one instrument, two readouts, not two mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (2 + 1 + 1 + 1 + 1 across `m_locality_scoped_verifiers`, `m_topology_stratified_sampling`, `m_injection_provenance_probe`, `m_strongest_checker_control`, `m_disjoint_oracle_with_audit` respectively) — mixing the study's four headline empirical predictions (H1–H4 in `paper.md`'s own numbering) with two instrument-validity claims (`paper.md`'s A4 oracle-audit gate and B-alt structural-vs-weak-checker control, both present there as assumptions/baselines but never previously stated as falsifiable stage-5-style hypotheses in their own right) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The B0 and B-alt controls below are sanity-check / attribution comparators, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Constructed prerequisite-DAG agent task suite (pilot: ~20–40 hand-authored coding/filesystem tasks; scale-up: ~200–500 procedurally generated coding + tool-use + web-action tasks) — *justification:* the primary evaluation object; a canonical, independently-computable terminal state is required by A1, which the pilot's coding/filesystem domain (hash-set + program-output equality) satisfies cheaply.
- SWE-bench-style, τ-bench/τ²-bench, BFCL v3, ToolSandbox — *justification:* real task substrates whose grading practice (file/DB-state/tool-signature checks) this study's per-milestone verifiers are built to mirror, per A3.
- (draft initially listed "WebArena-style web-action tasks" with justification only "digest N8 lists it as a task substrate to adapt" — flagged below.)

`baselines` (sanity-check/attribution comparators, not outcome-tier competitors):
- B0 honest-trajectory control — topologically-valid trajectories that genuinely execute every prerequisite; expected `A=1 ∧ Ω=1` for all, i.e., bypass rate ≈0. Justifies that M2/M4 agree on legitimate completions, so any measured `ρ>0` on constructed traces is attributable to the bypass mechanism, not baseline verifier/oracle disagreement.
- B-alt strongest-local-checker control — richest realistic, still milestone-scoped, capability/compute-matched local check per checker type. Isolates structural locality from weak-implementation (feeds `m_strongest_checker_control`'s hypothesis directly).

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_bypass_exists` | `sp_verifier_locality` | "The measured aggregate checkpoint-bypass rate ρ̂ will be significantly greater than zero — ρ̂ ≥ 0.10 with Wilson 95% lower bound > 0.05 — over at least 300 constructed reorder/skip/inject trajectories on the pilot DAG suite (one-sided exact binomial test, p<0.05), demonstrating that independent per-milestone verification is not a sufficient proxy for true multi-step task success on this suite." |
| `rq_natural_incidence` | `sp_verifier_locality` | "Real LLM agents will naturally (non-adversarially) produce rollouts scored complete by every per-milestone verifier yet failing the terminal oracle at a non-zero but lower incidence than the constructed rate — natural incidence ρ̂_nat ≥ 0.02 with Wilson 95% lower bound > 0, over at least 200 verifier-complete real-agent rollouts, with a two-proportion test confirming ρ_nat < ρ_constructed." |
| `rq_topology_modulation` | `sp_combinatorial_coverage` | "In a logistic regression of the bypass outcome on prerequisite-chain depth and node in-degree over the scale-up suite (≥200 tasks), at least one predictor will show an odds ratio > 1.2 per unit with Wald p<0.05 (Holm-corrected across the two predictors), indicating deeper or higher-fan-in prerequisite structure raises bypass odds." |
| `rq_strategy_dominance` | `sp_provenance_authentication` | "The state-injection strategy's bypass rate will exceed both the reordering and step-skipping strategies' rates by at least 10 percentage points (pairwise two-proportion z-tests, Holm-corrected p<0.05 across the three pairs), because injection forges the milestone's local success signal directly without requiring an executable control-flow path." |
| `rq_structural_attribution` | `sp_structural_vs_weak_checker` | "Against the strongest-local-checker control (the richest realistic, still milestone-scoped, capability/compute-matched local check per checker type), the injection-strategy checkpoint-bypass rate remains at least half its value under the standard-strength checker suite — demonstrating that the measured bypass is attributable to structural locality rather than to lazy or weak checker implementations." |
| `rq_oracle_validity` | `sp_oracle_validity` | "A manual stratified audit of 50–100 oracle verdicts on honest (topologically-valid) trajectories will find a false-inconsistency rate of at most 5%, and the honest-trajectory bypass rate itself will be below 1% — establishing that the terminal oracle is disjoint-code-validated ground truth rather than a source of inflated bypass counts." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed H1–H4/A4/B-alt numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[WebArena-style]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest N8 lists it as a task substrate to adapt' is not a justification — it says nothing about which RQ needs this specific domain or why."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "WebArena-style web-action tasks — *justification:* used specifically to test whether `rq_topology_modulation`'s depth/in-degree finding generalizes to a domain whose per-milestone verifiers are DOM/page-state checks rather than the file/DB/tool-signature checks used in the coding and tool-use domains — stress-testing `sp_combinatorial_coverage`'s stratified design against a structurally different verifier population, not just re-observing the same domain twice."
- `changes_made`: gave the WebArena-style entry's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (verifier locality and provenance-authentication are described as properties/problems, not as "we build a locality-scoped verifier").
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` / `lim_*` stable stage-to-stage.
3. **Reference integrity** — `sp_verifier_locality.source_limitation_ids = ["lim_steporlm_latentveracity_local_global"]` ∈ Stage 3 ✓; `sp_provenance_authentication.source_limitation_ids = ["lim_webarbiter_gistify_better_checker_not_rate"]` ∈ Stage 3 ✓; `sp_oracle_validity.source_limitation_ids = ["lim_difftaskgraph_learned_not_oracle"]` ∈ Stage 3 ✓; `sp_combinatorial_coverage` and `sp_structural_vs_weak_checker` both correctly `["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (per-milestone verdicts, oracle verdict, bypass rate by strategy/topology/natural-incidence, oracle-audit rate) are each reachable: per-milestone/oracle verdicts and the constructed+natural bypass rate via `sp_verifier_locality` (`rq_bypass_exists`, `rq_natural_incidence`), the topology breakdown via `sp_combinatorial_coverage` (`rq_topology_modulation`), the strategy breakdown via `sp_provenance_authentication` (`rq_strategy_dominance`), and the oracle-audit rate via `sp_oracle_validity` (`rq_oracle_validity`) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.
6. **Recount check (the specific bug class the B5.5 run caught):** 5 sub-problems in Stage 4; 5 methods in Stage 5, one per sub-problem (1:1); 6 hypotheses across those 5 methods (2+1+1+1+1); 6 mechanism-tier RQs in Stage 6, one per hypothesis (1:1). 5 = 5 sub-problems↔methods ✓. 6 = 6 hypotheses↔RQs ✓. No off-by-one.

**What was hardest:** as with the mature-seed pattern, the recurring tension was **not disagreement about facts** (the digest and `paper.md` are unusually well-specified, down to exact thresholds) but **scope discipline** — repeatedly checking whether a stage-5/6 hypothesis was quietly restating `paper.md`'s own already-finished Step 6 rather than adding something this schema's structure specifically demands. The two instrument-validity hypotheses (`m_strongest_checker_control`'s structural-attribution claim and `m_disjoint_oracle_with_audit`'s audit-bound claim) are the clearest example: `paper.md`'s A4 and B-alt control already gesture at both, but neither was previously stated as an independently falsifiable stage-5-style hypothesis with its own threshold — that gap only became visible by walking the stages.md schema explicitly.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Revision pass over the review artifacts (`stage_review.md`, `taste_audit.md`, `design_review.md`, `pipeline.md` Phase Log). Every finding in those files was enumerated and statused; items already applied in earlier passes are not re-listed here — this section records only the findings that were still OPEN at the start of this pass, plus rejections with reasons. Past rounds above are untouched.

**Applied:**

1. `pipeline.md` Phase G `[moderate]` to-do 1 (also `stage_review.md` §Phase G) — the two `selected` adjacent cache records used in `paper.md` A3 were uncited in the draft's Experimental Setup → added `MCPAgentBenchToolUse2026` + `RLVRAtlassianToolUseAgents2026` citations to the Datasets paragraph ("tool-use benchmarks with database-state, tool-selection, and tool-signature grading") → `paper_draft.md` + `paper_draft.tex` (recompiled; both keys resolve in `paper_draft.bbl`).
2. `pipeline.md` Phase G `[moderate]` to-do 2 (also `stage_review.md` §Phase G) — background A2-archetype structural exemplar `PLMCalibrationCloseLook2023` (named in `paper.md` Step 2) was absent from the draft prose → added one evidence-shape sentence at the end of the Introduction's design-decisions paragraph naming the calibration study as the measurement-study mold → `paper_draft.md` + `paper_draft.tex`.
3. `design_review.md` §Missing-RQs 3 + `stage_review.md` Phase A item 6.9 follow-up ("RQ1–RQ3 sample sizes should also get an explicit power derivation before Phase B"; "per-cell power derivation for H3's topology bins" listed under design_review's "Not fixed here") → added a pre-registered per-cell power gate to RQ3 (simulation-based power ≥0.9 — matching A6's target — to detect OR 1.2 at realized cell counts, using pilot-observed intra-task correlation; under-powered cells pre-declared INCONCLUSIVE per A5's thin-cell rule) and an explicit power note to RQ1's sample-size rationale (coverage target, not power-derived; binding power lives in RQ2/RQ3) → `experiment_design.md`.
4. `design_review.md` §Missing-RQs 4 ("the design does not state the assumed completion rate" for the ≥200 M2-complete rollout floor) → added an explicit completion-yield assumption note to RQ2's sample-size rationale: total budget scales as 200/yield, no yield value is pre-registered, pilot must measure it, PG-3 blocks H4 scoring until the floor is met, and infeasible yield triggers PG-0 task re-selection rather than floor-lowering → `experiment_design.md`.
5. `design_review.md` §Missing-RQs 2 (per-checker-type sensitivity cannot be answered inferentially since A3 was demoted to a reporting discipline) → made the restriction explicit rather than silent: scope note on RQ1's per-checker-type metric in `experiment_design.md`, mirrored as one clause in the draft's Experimental Setup Metrics paragraph → `experiment_design.md` + `paper_draft.md` + `paper_draft.tex`.
6. Compile fix required by item 1: the auto-generated `refs.bib` title for `RLVRAtlassianToolUseAgents2026` contains U+2217 (∗), which pdflatex rejects once the key is cited; added `\DeclareUnicodeCharacter{2217}` to the preamble instead of hand-editing the script-generated bib → `paper_draft.tex`.

**Rejected as moot / out of scope (with reasons):**

7. `stage_review.md` Phase A item 2 / `design_review.md` F1 (reference-cache STOP: re-harvest the 8 phantom N3 works) — rejected for this pass: requires network/harvest capability this environment does not have; remains the honestly-logged Phase-B-blocking STOP in `pipeline.md`, unchanged.
8. `stage_review.md` Phase A item 6.10 (only 1 background archetype exemplar vs. the recommended 2–3) — rejected for this pass: same re-harvest dependency as item 7.
9. `design_review.md` §Missing-RQs 1 (mitigation/detectability RQ) — already applied earlier: the draft's "Further evaluation" paragraph names the cheaper partial-provenance-check alternative and pre-commits why it is out of scope (changes the object of study); no further edit needed.
10. `design_review.md` reliability-audit item 5 (H1–H4 in prose rather than the literal seven-slot template) — rejected: reviewer's own severity is "cosmetic gap"; the substance (all seven slots incl. verbatim fallbacks) is present in `paper.md`, which is the pre-registered design authority this pass must not restructure, and `experiment_design.md` must keep target hypotheses byte-identical rather than re-templated.
11. `pipeline.md` Phase G `[minor]` (overfull-hbox warnings from long inline `\texttt{}` paths) — rejected: cosmetic, zero content risk, explicitly ruled out of scope by the Phase G review itself.
12. `pipeline.md` open to-do 4 (run Phase B/C/D with real compute, re-splice E/F from `verdicts.json`) — rejected for this pass: no experiment compute in this environment; unchanged from the Phase Log's standing note.
13. `taste_audit.md` (initial + Phase H re-audit) — no findings to apply: both verdicts 🟢 with no reframe requested; this pass's added sentences are citation/scope-note edits at the same mechanism-specific altitude, introducing no bridge/synthesis language.

**Cross-deliverable consistency check (post-edit):** 6 RQs in both `experiment_design.md` and `paper_draft.md` (RQ1 gate / RQ2 headline / RQ3 topology / RQ4 strategy / RQ5 attribution / RQ6 oracle); effect floor `ρ_nat ≥ 0.02` with decision threshold 0.01 and power ≈0.91 at n=200 in both; RQ1 0.10/0.05 gate, RQ3 OR>1.2, RQ4 ≥10pp margin, RQ5 ≥0.5 retention, RQ6 ≤5%/<1% gates identical in both; task-clustered statistics (cluster bootstrap / cluster-robust SE / mixed-effects task intercept) named consistently in both. No mismatch found; no hypothesis text was altered.
