# Auto-Research-Discussion Run — B2.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B2.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries its own asymmetry check, formal notation, assumptions A1–A6, and fallback-covered hypotheses), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order (this run):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. This ordering and the four-artifact layout mirror the completed exemplar at `topics/B5.5.../discussion/`. Any REVISE findings from `stage_review.md` are folded into the `paper_draft.*` files before finalization — see `stage_review.md` for the reasoning behind each fix.
>
> **Note on downstream currency (added when this trace was split out of `pipeline.md`):** this file is the historical record of how Stages 1–6 were argued and confirmed. Stage 6's table below (6 mechanism-tier RQs, a single `B0`/`B-alt` control pair) was the state of the design at the moment this loop closed. A later adversarial pass (`design_review.md`, documented in `pipeline.md`'s Phase Log) revised the control-arm design and RQ numbering into what `paper.md`'s Step 6 and `experiment_design.md` now specify (`B0-p`/`B0-a`/`B-alt1`/`B-alt2`/`B-alt3`, 4 headline RQs: RQ_INF_1/H1, RQ1a/H2, RQ1b/H3, RQ_INF_2/H4). This file is kept as-is — the audit trail of the original discussion — rather than edited to match; for the current, authoritative experiment design, see `experiment_design.md` and `paper.md` Step 6.

## Seed brief

- **One-sentence description:** Measure whether LLM agents and the failure-attribution systems built around them can distinguish "the agent failed" from "the task itself was never solvable," and characterize where the calibration boundary of appropriate abstention/refusal lies.
- **Apparent inputs:** a constructed task instance (instruction + environment) from a matched solvable/unsolvable pair; the agent's execution trace over that instance; an attribution system's classification of that trace, with a confidence score.
- **Apparent outputs:** a per-instance attribution label from `{success, agent_failure, unsolvable}`; a confidence/abstention score on the `unsolvable` judgment; aggregate directional misattribution rates and calibration/risk–coverage curves.
- **Closest research areas:** LLM-agent failure attribution (AgenTracer, WhoWhen, MAST); refusal/abstention calibration and selective prediction (RefusalIndex, TrustOrEscalate, RLCR); agent self-assessment and interactive ambiguity resolution (KnowCapable, SilenceIsGolden, EHR-ChatQA).
- **In scope:** measuring existing attribution pipelines (LLM-judge, trained tracer, first-party self-report) against a mechanically-certified paired benchmark. **Out of scope:** training a new attribution system to fix the bias (this is a measurement study, not a proposed cure); naturally-occurring (non-injected) unsolvability as the headline construct; live/non-sandboxable deployments.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already carries its own formal notation (Step 5's `t=(q,E)`, `μ`, `O(t)`, `π`, `A`), its own assumption ledger (A1–A6), and its own fallback-covered hypotheses (H1–H4, B0, B-alt). Reconstruction risk is low; as in B5.5, the risk is *redundancy* with `paper.md`'s own Steps 5/6/9 — stages 4–6 below are framed to add the structure this schema specifically demands (explicit sub-problem decomposition, method-level `key_insight` framing, verbatim hypothesis→RQ traceability) rather than re-deriving `paper.md`'s own already-finished design.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a task instance consisting of an instruction and an environment (a database schema, tool list, file system, or policy set), and given an attribution system that reads an agent's execution trace over that instance and must emit a judgment of what happened, determine whether that system (and the acting agent itself) can distinguish "the agent failed to solve a solvable task" from "the task admitted no solution at all," and characterize the confidence threshold at which declaring "unsolvable" is warranted.
- `input`: (1) a task instance `t = (q, E)` — instruction `q` plus environment `E` — drawn from a matched solvable/unsolvable pair; (2) the agent's execution trace over `t` (actions, tool calls, errors, terminal event) under a fixed step/token budget; (3) the attribution system's classification output over the task text and trace, with an attached confidence score on the `unsolvable` judgment.
- `output`: (1) a per-instance label from `{success, agent_failure, unsolvable}`; (2) a confidence/abstention score in `[0,1]` attached to the `unsolvable` judgment; (3) aggregate directional misattribution rates (unsolvable→agent_failure and the reverse) plus threshold-free calibration curves (risk–coverage, AUROC, ECE) computed against a ground-truth oracle never exposed to the agent or the attribution system.
- `constraints`: unsolvability of a given instance must be certifiable mechanically from the task/environment specification itself, never from human judgment or from the agent's own failure (the latter would make the ground truth circular); the oracle is used only at evaluation time.
- `objective`: a directional-bias claim (that misattribution is asymmetric) or a calibration claim (that a usable confidence threshold exists) is accepted only if it is measured against the mechanically-certified oracle label, with both directions of error reported, not just the one the study happens to find interesting.
- `study_type`: `empirical` — stated explicitly: digest N12 already settles this ("the seed frames the deliverable as a measurement... every projected N9 result validates a measured quantity"), and the core question ("能否区分agent失败与任务本不可解") is a characterization question, not a proposed fix being pitted against baselines.

**critique:**
- summary: The problem is concretely scoped and evidence-traceable, but `input`/`output` silently narrow "attribution system" to a third-party post-hoc reader, which conflicts with the seed's own methodology.
- comments:
  - `{severity: major, field: "input", anti_pattern: "fields_misaligned", comment: "`input` says 'the attribution system's classification output over the task text and trace' — phrasing that presumes a third-party reader consuming a *finished* trace after the fact. But digest N6's own M4 explicitly includes 'the acting agent's own terminal self-report (first-party refusal)' as one of the four attribution instantiations, and M3's harness note says agents may 'declare a task infeasible' as an in-run terminal action — i.e., self-report happens *during* the run, not after. As written, the problem statement's input/output framing doesn't obviously cover this case, which the paper's own method battery treats as co-equal to the third-party readers."}`
  - `{severity: minor, field: "objective", anti_pattern: null, comment: "'not just the one direction the study happens to find interesting' is doing useful anti-cherry-picking work but reads as informal — could be tightened to name the two directions explicitly by their metric names once those are defined, which the refiner can do for free alongside formalizing."}`
- decision: `move_to_refiner` (a formalize-level fix — generalizing the definition of 'attribution system' to be agnostic to first-party vs. third-party, using content already present in N6/M3 — not a redesign).

### Refiner pass

- `input`/`output` (refined): generalize "attribution system" to a function `A: (q, x) → (ŷ, c)` where `x` is the trace produced so far (which may already contain the agent's own terminal infeasibility declaration as one possible event within it) and `ŷ ∈ {success, agent_failure, unsolvable}`, `c ∈ [0,1]`. The one constraint on `A`, stated explicitly: **`A` never observes the oracle `O(t)`.** This covers a third-party reader scoring a completed trace and the acting agent's own first-party self-report as the same kind of object — a function from (task text, trace-so-far) to a labeled, confidence-scored judgment — differing only in *when* `A` is invoked (after termination vs. as part of termination), not in what problem it solves.
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation): "Task `t=(q,E)`; agent `π` produces trace `x=π(t)` under budget `B`; attribution system `A(q,x) → (ŷ,c)`, `ŷ∈{success, agent_failure, unsolvable}`, `c∈[0,1]`, with `A` never observing oracle `O(t)∈{solvable, unsolvable}`. Determine whether `ŷ` recovers `O(t)` and characterize the operating points of `c` at which declaring `ŷ=unsolvable` is warranted."
- `objective` (tightened): "...accepted only if reported with both `FBR = P(ŷ=agent_failure | O(t)=unsolvable)` and `CoR = P(ŷ=unsolvable | O(t)=solvable ∧ π did not succeed)` named explicitly, not just the direction the study happens to find interesting."
- `changes_made`: generalized `input`/`output` to cover first-party and third-party attribution under one definition; added `formal_summary`; named the two directional metrics in `objective`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Failure-attribution pipelines are built on the implicit assumption that every failed run contains a culpable agent decision; treating "the task was never solvable" as an admissible outcome, rather than an unmodeled edge case, changes what these pipelines can be trusted to tell a downstream consumer.
- `why_it_matters`: The strongest current attribution formulations define their output as the earliest agent-step whose counterfactual correction would flip failure to success (AgenTracer, WhoWhen) — a label space with no admissible "no one was at fault" outcome. When a task has no solution, these systems must still nominate a culprit, systematically over-blaming the agent, wasting debugging effort chasing a fix that cannot exist, and miscalibrating whatever retry/escalate/abandon policy consumes the label.
- `who_cares`: Teams operating agent-debugging/observability pipelines that consume attribution labels to decide whether to retry, escalate to a human, or abandon a task; benchmark designers who need to know whether "agent failed" in their own evals means what it claims to mean; researchers extending refusal-calibration methods (RefusalIndex, RLCR) to multi-step agent settings where the ground truth is task feasibility rather than answer correctness.
- `evidence`: AgenTracer's and WhoWhen's own problem definitions structurally exclude "unsolvable" from their label space (digest N4 limitation 1); RefusalIndex's own motivation demonstrates that naive refusal-frequency metrics can be gamed by refusing more without tracking the actual boundary — evidence that *a* calibration boundary needs independent verification, not just a higher refusal rate.

**critique:**
- summary: The stakes are concrete and stage-1-specific, but the motivation never explains why the answer has to be a *calibration boundary* (a swept threshold, a curve) rather than simply adding an "unsolvable" label to the classifier and calling the problem solved.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a *calibration/risk–coverage curve*, not just a corrected 3-way label. The current why_it_matters motivates why misattribution matters but never motivates why a swept threshold specifically is needed, as opposed to a single fixed 'is it unsolvable, yes/no' fix. A skeptical reader could ask: 'why not just retrain the classifier with an unsolvable category and be done?' Digest N5's C3 already has the answer (asymmetric costs: over-flagging lets agents cop out of solvable-but-hard tasks, under-flagging blames agents for impossible ones, and the right operating point differs by task family and by which downstream policy consumes the label) but that argument never made it into why_it_matters."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, the two error directions have asymmetric downstream costs that a single fixed cutoff cannot serve: an operating point tuned to minimize false blame on genuinely unsolvable tasks will let agents claim infeasibility on tasks that were merely hard, masking real incompetence as a principled refusal; an operating point tuned to minimize that cop-out risk will instead blame agents for tasks nobody could have solved. Because different downstream consumers of the label — an auto-retry loop, a human-escalation queue, an abandonment policy — tolerate these two error types differently, no single accuracy number can serve all of them; only a full calibration characterization (a threshold sweep reported as a risk–coverage curve) lets each consumer choose its own operating point, which is why the output has to be a curve and not a corrected label."
- `changes_made`: added the asymmetric-cost argument explaining why calibration (not merely relabeling) is the right kind of output.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each at the approach + limitation level (a real corpus search over 11,683 OpenReview papers plus two canonical non-corpus works), so no additional landscape papers are invented here to pad a `general_related_works` list.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / role / `is_potential_baseline` / limitation):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_agentracer` | AgenTracer (OpenReview:l05DseqvuD) | **true** (label space extended with `unsolvable`, run within this paper's harness) | Defines attribution as the earliest agent-step whose counterfactual correction flips failure to success — presupposes such a correction exists; no admissible "task itself infeasible" outcome. |
| `rw_whowhen` | WhoWhen (arXiv:2505.00212) | **true** (its two prompting strategies — all-at-once, step-by-step — reused as LLM-judge baselines) | Same counterfactual-correction presupposition; finds even strong LLM judges weak at step-level localization, but never tests instances where no step-level fix exists. |
| `rw_mast` | MAST (arXiv:2503.13657) | false (taxonomy, not a runnable pipeline) | Its failure taxonomy (specification, misalignment, verification) has no category for task-level infeasibility, and its manual annotation is small-scale by its own citing papers' account. |
| `rw_refusalindex` | RefusalIndex (OpenReview:9gJBhkLRat) | false (different setting: single-turn factual QA, not multi-step agent traces) | Calibrates refusal against the *model's own* error probability, a knowledge-boundary notion — never against an externally certified "no one could solve this" ground truth. |
| `rw_silenceisgolden` | SilenceIsGolden (OpenReview:PhUCxfS0yf) | false (trains a single generator, not a third-party attribution system) | Unanswerable labels are inherited from a benchmark (TimeQA), not injected via matched-pair construction; nothing measures whether a third-party reader watching *someone else's* trace can make the same call. |
| `rw_knowcapable` | KnowCapable (OpenReview:EO6WtJ0q6G) | **true** (its ex-ante self-assessment protocol adapted to a post-hoc first-party self-report instantiation) | Testbeds (BigCodeBench, SWE-bench) are all solvable in principle, so low predicted success conflates "solvable but beyond me" with "unsolvable for anyone" — the two are never dissociated by construction. |
| `rw_trustorescalate` | TrustOrEscalate (OpenReview:UHPnqSTBPO) | false (calibrates against human-judge agreement, not oracle feasibility) | Escalates uncertain cases to a stronger judge rather than declaring the item itself infeasible — a different action space than "certify unsolvable." |
| `rw_rlcr` | RLCR (OpenReview:ASQ649zdHm) | false (single-turn, answer-correctness reward) | Calibrates confidence against *answer correctness* on verifiable problems whose reward design contains no unsolvable-instance class. |
| `rw_ehrchatqa` | EHR-ChatQA (OpenReview:hLweUPBz7k) | false (interactive ambiguity-resolution, not feasibility certification) | Treats underspecification as *resolvable* via clarification; never requires the agent to certify infeasibility and stop, nor supplies construction-guaranteed infeasibility labels to score such a call against. |

**critique:**
- summary: Every limitation is specific and problem-tied (no generic "scalability issues" phrasing), but one entry's role needs sharpening before it's reused as a metric source in Stage 5.
- comments:
  - `{severity: major, field: "specific_related_works[rw_refusalindex]", anti_pattern: "io_approach_mismatch", comment: "rw_refusalindex is correctly marked `is_potential_baseline: false` — its setting (single-turn factual QA, ground truth = model's own error probability) doesn't match this paper's setting (multi-step agent traces, ground truth = externally certified task infeasibility). But digest N6's own M5 reuses RefusalIndex's exact statistical *construct* — a Spearman correlation between abstention confidence and a ground-truth correctness column — as this paper's own calibration metric, substituting oracle-certified unsolvability for model-own-error as that column. Leaving this unstated risks implying the original paper's reported correlations are being compared against, which they are not — the mismatch this critique flags for is_potential_baseline applies just as much to what gets silently reused as a metric."}`
- decision: `move_to_refiner` (a wording-precision fix — the metric-form borrowing is legitimate and already designed into N6/M5, it just needs to be stated explicitly here rather than left implicit).

### Refiner pass

- `rw_refusalindex.is_potential_baseline` retained as `false`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number or even the run-it-again sense — RefusalIndex's own reported correlations are never compared against, and its setting (single-turn QA, knowledge-boundary ground truth) doesn't transfer. Its **Spearman-correlation measurement construct** is borrowed as this paper's calibration metric (the Unsolvability Refusal Index), with oracle-certified task infeasibility substituted for model-own-error as the ground-truth column — a borrowed instrument, not a borrowed finding or a borrowed setting."
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`rw_agentracer`/`rw_whowhen`'s counterfactual-presupposition limitation) is not a distinct framing check but is already operationalized as the mandatory label-space-restricted control (`B0` in `paper.md`, folded into Stage 5's `m_matched_attribution_battery` below) rather than a separate research question. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*
- `changes_made`: clarified `rw_refusalindex`'s role as a borrowed measurement construct, not a borrowed baseline or finding.
- `declined_to_fix`: none.

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus one genuinely novel decisive component):

- **`sp_mechanical_certification`** — *description:* Establish, for a given task instance, whether it is solvable — using only the task/environment specification itself, before any agent acts and independent of any observed agent behavior. *why_it_is_a_problem:* the only other available certification sources are human judgment (subjective, expensive at scale) or the agent's own failure (circular — it would define "unsolvable" as "whatever the agent didn't solve," which is exactly the confound this paper exists to remove). *technical_challenge:* the certification procedure must generalize across heterogeneous environment types (a database schema, a tool list, a file system, a policy set) while remaining a script-level, non-agentic check. *source_limitation_ids:* `["__novel__"]` — no cited work constructs a mechanical, pre-agent solvability certification; the closest works (RefusalIndex, TrustOrEscalate) certify against a model's own error or a human judge's agreement, not against the task specification itself.
- **`sp_trace_discriminability`** — *description:* Determine whether the evidence available in an agent's execution trace (actions, tool errors, dead ends, terminal event) is sufficient for a reader to tell "a competent agent correctly exhausted a genuinely unsolvable task" from "an incompetent agent botched a solvable one." *why_it_is_a_problem:* both cases can produce superficially similar traces — repeated tool errors, unresolved exploration, no final answer — so the discrimination signal, if it exists at all, is subtle. *technical_challenge:* the signal (if present) is plausibly something like *systematic* absence of a required resource versus *recoverable* mistakes that were never recovered, but no existing attribution formulation is built to look for that distinction specifically. *source_limitation_ids:* `["lim_agentracer_whowhen_counterfactual"]`.
- **`sp_boundary_calibration`** — *description:* Characterize the confidence threshold at which declaring an instance "unsolvable" is warranted, as a function of the asymmetric costs of the two error directions. *why_it_is_a_problem:* a single fixed cutoff cannot be correct for every task family or every downstream consumer of the label, since over- and under-flagging trade off differently depending on who consumes the label. *technical_challenge:* this requires a confidence signal that carries real discrimination power (not just a post-hoc label), and a way of reporting the trade-off (a curve, not a single number) that a downstream policy designer could actually act on. *source_limitation_ids:* `["lim_refusalindex_wrong_groundtruth", "lim_trustorescalate_rlcr_wrong_groundtruth"]`.
- **`sp_leakage_free_construction`** — *description:* Ensure that the mutation used to construct an unsolvable instance changes only the solvability-determining fact, leaving no surface artifact (length, phrasing, a conspicuously missing tool) that would let a system "detect" unsolvability without any genuine feasibility reasoning. *why_it_is_a_problem:* if the construction leaks, every downstream misattribution-rate number is measuring artifact-detection rather than the phenomenon the paper claims to measure. *technical_challenge:* the audit must operate on the task text alone, stripped of trace and environment, to isolate exactly the failure mode it's checking for — and it must be a hard gate applied before any headline number, not a post-hoc caveat. *source_limitation_ids:* `["__novel__"]`.
- **`sp_design_vs_information_limit`** — *description:* Determine whether a high measured misattribution rate reflects a fixable deficiency in how existing attribution systems are built (label space, prompt, judge weakness), or an information-theoretic ceiling — the possibility that the trace itself contains no recoverable feasibility signal for *any* observer, however capable. *why_it_is_a_problem:* without ruling out the ceiling explanation, a high misattribution rate says nothing about whether attribution-system design is the right place to intervene; the entire premise that "existing systems could do better" needs its own check. *technical_challenge:* the only way to establish the ceiling is to build the best-case reader — one given privileged access to the ground truth during calibration — and see whether even it can extract more signal from the same trace than deployed, oracle-blind systems can. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver Stage 1's objective), but two sub-problems risk reading as the same underlying question about trace-level signal.
- comments:
  - `{severity: minor, field: "sp_trace_discriminability / sp_design_vs_information_limit", anti_pattern: "overlap", comment: "Both are framed around 'is there signal in the trace,' which can read as the same sub-problem stated twice. They are genuinely distinct — one asks whether *currently deployed* attribution systems can discriminate, the other asks whether *any conceivable observer* (an upper bound, not an existing system) could — but the descriptions don't make that existing-capability-vs-ceiling distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_trace_discriminability.technical_challenge` sharpened to end with: "...this is a **capability-of-deployed-systems** question — do the attributors that actually get built and shipped pick up on this signal — not a question about the theoretical limit of what the trace contains."
- `sp_design_vs_information_limit.technical_challenge` sharpened to end with: "...this is a **ceiling** question distinct from deployed-system capability — it asks what the best conceivable reader could extract given privileged calibration access, which is the only way to tell whether a poor result from deployed systems reflects a fixable design problem or an unfixable information limit."
- `changes_made`: made the deployed-capability-vs-ceiling distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from Stage 3 limitations, 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_mutation_oracle`** → targets `sp_mechanical_certification`. *proposed_approach:* Apply exactly one typed mutation (missing-resource, contradictory-constraint, or stale-reference) to a verifier-equipped source task, then certify the mutated member via a static script check that the mutated element is (a) required by the reference solution and (b) has no substitute — a schema-graph reachability check for SQL, tool-signature coverage for function-calling, an environment-state assertion for τ-bench/Terminal-Bench. *key_insight:* solvability is not an agent-behavior property but a property of the task specification itself, so it can be certified before any agent runs, if the certification checks both "required" and "no substitute" rather than either alone. *hypotheses:* ["Running the strongest available agent plus a bounded exhaustive/tool-search against every constructed-unsolvable instance will yield zero successes across all tested domains, confirming the oracle certifies genuine unsolvability rather than merely difficulty."]
- **`m_matched_attribution_battery`** → targets `sp_trace_discriminability`. *proposed_approach:* Run a fixed harness (identical budget, logging, and prompt scaffolding) over both members of each matched pair, scored by a battery of attribution instantiations: LLM-judge (all-at-once and step-by-step), a trained tracer with its label space extended to include `unsolvable`, first-party in-run self-report, and a keyword/terminal-error heuristic floor — plus a label-space-restricted control that can only emit `{success, agent_failure}`. *key_insight:* holding the harness fixed across the matched pair isolates "what the attributor reads out of the trace" as the thing under test, rather than confounding it with differences in how the trace was produced. *hypotheses:* ["The label-space-restricted control will show FBR ≈ 1.0 on unsolvable instances by construction, confirming that a formulation with no feasibility category structurally forces agent-blame.", "For a majority of the full attribution battery's members, FBR will exceed CoR by at least 10 percentage points, showing the over-blame bias persists even when an `unsolvable` label is available, not just when it's structurally absent."]
- **`m_oracle_ceiling_probe`** → targets `sp_design_vs_information_limit`. *proposed_approach:* Build a trace-reading probe calibrated directly on the oracle label, using the same backbone and compute budget as the strongest deployed attributor, then compare its held-out discrimination performance against the deployed (oracle-blind) attributors'. *key_insight:* the strongest rival explanation for a high misattribution rate is that the trace itself carries no recoverable feasibility signal for anyone — the only way to rule this out is to build the best-case reader and see whether privileged calibration access lets it do any better on the same evidence. *hypotheses:* ["The oracle-calibrated probe will exceed AUROC 0.65 discriminating unsolvable from solvable-failed traces on held-out instances, while deployed oracle-blind attributors remain below this ceiling, showing the gap is attributable to attribution-system design rather than an information-theoretic limit."]
- **`m_calibration_sweep`** → targets `sp_boundary_calibration`. *proposed_approach:* Sweep the confidence threshold on the `unsolvable` score and report risk–coverage curves, AURC, AUROC, 10-bin ECE, and a Refusal-Index-style Spearman correlation between confidence and oracle-certified unsolvability, per task family rather than pooled. *key_insight:* because over- and under-flagging costs differ by task family and by downstream consumer, only a full curve — not a single accuracy number — lets each consumer choose its own operating point. *hypotheses:* ["For at least one attribution baseline in each tested domain, the risk–coverage curve will show a non-trivial knee (AURC strictly below the coverage-proportional diagonal, CI-separated), indicating the unsolvable-confidence score carries real discrimination signal even where hard 3-way classification is imperfect."]
- **`m_leakage_audit`** → targets `sp_leakage_free_construction`. *proposed_approach:* Gate every domain's mutation operators through a pre-registered validity check before any headline number is reported: surface-statistics matching (length, token overlap, instruction perplexity) between pair members, a text-only probe (task text alone, no trace, no environment) attempting to predict solvability, and a human audit of a random 10% sample. *key_insight:* the only way a mutation could be gamed is by leaving a textual "tell," so the audit has to strip away trace and environment access entirely to isolate exactly that failure mode. *hypotheses:* ["Each domain's text-only probe AUROC will fall below the pre-registered 0.60 gate after at most one operator-repair iteration, and pair members will not be statistically separable on surface length/token-overlap/perplexity at α=0.05, validating that measured misattribution reflects feasibility reasoning rather than surface-artifact detection."]

**critique:**
- summary: Every method has a real mechanism and a stated falsifiable hypothesis, but one hypothesis (`m_oracle_ceiling_probe`) risks reading as trivially true given how it's currently worded, which would make it unfalsifiable in practice.
- comments:
  - `{severity: major, field: "m_oracle_ceiling_probe.hypotheses", anti_pattern: "unfalsifiable_hypothesis", comment: "As stated, 'the oracle-calibrated probe will exceed AUROC 0.65... while deployed attributors remain below' risks being true almost by construction: the probe is calibrated directly on the ground truth it's being asked to predict, so of course it should do better than an oracle-blind reader — this isn't yet a genuine empirical claim about trace-level signal, it's closer to a tautology about supervision. The hypothesis needs to state explicitly why exceeding 0.65 on *held-out* instances is not guaranteed by the calibration setup, and what result *would* actually be surprising (and falsify the design's premise)."}`
- decision: `move_to_refiner` (the underlying design in `paper.md`'s own B-alt control already reasons about this correctly — the fix is to make that reasoning explicit in the hypothesis wording, not to redesign the probe).

### Refiner pass

- `m_oracle_ceiling_probe.key_insight` extended: "...calibration on the oracle label only constrains what the probe learns on its *training* instances — it does not guarantee the resulting decision rule generalizes to held-out traces, since the trace may simply not encode the distinguishing signal at all (in which case even privileged supervision cannot lift held-out AUROC above chance). Exceeding 0.65 on held-out instances is therefore a genuine, falsifiable claim about the trace's information content, not an artifact of having seen the answer during calibration — and the informative failure mode is exactly the one worth stating up front: if the calibrated probe *also* cannot clear 0.65, that is the strongest possible evidence that the ceiling, not attribution-system design, is the binding constraint, since no amount of extra design effort could then close the gap either."
- `changes_made`: clarified why the probe's held-out performance is a genuine empirical test rather than a guaranteed outcome of its calibration procedure, and named the informative failure direction explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (1 + 2 + 1 + 1 + 1 across the five methods respectively — `m_matched_attribution_battery` carries two, per the same one-instrument-two-estimands pattern used for its label-space-restricted control and its full-battery bias claim), mixing instrument-validity claims (oracle soundness, leakage gate) with the study's headline empirical predictions (directional bias, calibration knee, design-vs-ceiling) — a deliberate mix for an `empirical` study_type, carried into the tier accounting below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured (the closest candidate is already operationalized as the `B0` control inside `rq_labelspace_control`, a mechanism-tier RQ, not a separate framing-tier one).
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. All baselines below are sanity-check comparators, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Spider 1.0 (Yu et al., 2018) — *justification:* real text-to-SQL scenarios with a closed-form schema-reachability check for the missing-resource mutation; pilot-stage domain, cheapest to build the oracle for.
- BFCL v3 (Berkeley Function Calling Leaderboard) — *justification:* has an existing irrelevance-detection split, the closest natural precedent for a removed-tool mutation; pilot-stage domain alongside Spider.
- τ-bench retail/airline — *justification:* supports deleted-record and policy-contradiction mutations in a stateful tool-agent environment; scale-up domain.
- Terminal-Bench — *justification:* supports non-existent-resource mutations in a command-line setting; scale-up domain.
- (draft initially listed BIRD with justification only "digest lists it as a text-to-SQL scale-up source" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Label-space-restricted attributor (`B0`) — the necessary control confirming the problem is structurally forced, not incidental.
- LLM-judge attribution, all-at-once and step-by-step (per WhoWhen) — the two established prompting strategies.
- AgenTracer-style trained tracer with label space extended to `unsolvable`.
- First-party self-report (protocol adapted from KnowCapable).
- Keyword/terminal-error heuristic — floor baseline.
- Oracle-calibrated ceiling probe (`B-alt`) — the strongest-alternative-explanation control, isolating design-limited from information-limited.

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_oracle_soundness` | `sp_mechanical_certification` | "Running the strongest available agent plus a bounded exhaustive/tool-search against every constructed-unsolvable instance will yield zero successes across all tested domains, confirming the oracle certifies genuine unsolvability rather than merely difficulty." |
| `rq_labelspace_control` | `sp_trace_discriminability` | "The label-space-restricted control will show FBR ≈ 1.0 on unsolvable instances by construction, confirming that a formulation with no feasibility category structurally forces agent-blame." |
| `rq_directional_bias` | `sp_trace_discriminability` | "For a majority of the full attribution battery's members, FBR will exceed CoR by at least 10 percentage points, showing the over-blame bias persists even when an `unsolvable` label is available, not just when it's structurally absent." |
| `rq_ceiling_vs_design` | `sp_design_vs_information_limit` | "The oracle-calibrated probe will exceed AUROC 0.65 discriminating unsolvable from solvable-failed traces on held-out instances, while deployed oracle-blind attributors remain below this ceiling, showing the gap is attributable to attribution-system design rather than an information-theoretic limit." |
| `rq_calibration_knee` | `sp_boundary_calibration` | "For at least one attribution baseline in each tested domain, the risk–coverage curve will show a non-trivial knee (AURC strictly below the coverage-proportional diagonal, CI-separated), indicating the unsolvable-confidence score carries real discrimination signal even where hard 3-way classification is imperfect." |
| `rq_leakage_gate` | `sp_leakage_free_construction` | "Each domain's text-only probe AUROC will fall below the pre-registered 0.60 gate after at most one operator-repair iteration, and pair members will not be statistically separable on surface length/token-overlap/perplexity at α=0.05, validating that measured misattribution reflects feasibility reasoning rather than surface-artifact detection." |

(setup/sample-size/statistical-test/expected-outcome/falsification/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 6/9 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[BIRD]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest lists it as a scale-up source' says nothing about which RQ needs BIRD or why Spider alone wouldn't do."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "BIRD (Li et al., 2023) — *justification:* multi-table schemas with materially more complex reference queries than Spider's; lets `rq_directional_bias` and `rq_ceiling_vs_design` be tested under schema complexity closer to real deployments, checking that the directional bias and the design-vs-ceiling gap are not artifacts of Spider's comparatively simple single-database setting."
- `changes_made`: gave BIRD's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem`/`technical_challenge` fields describe what must be true or what must be measured, never how (no mutation-operator or oracle-script details appear before Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*`/`m_*`/`rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_trace_discriminability.source_limitation_ids = ["lim_agentracer_whowhen_counterfactual"]` and `sp_boundary_calibration.source_limitation_ids = ["lim_refusalindex_wrong_groundtruth", "lim_trustorescalate_rlcr_wrong_groundtruth"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (3-way label, confidence score, aggregate rates/curves) are each reachable: the label via `sp_mechanical_certification` + `sp_trace_discriminability`, the confidence score via `sp_boundary_calibration`, the aggregate rates/curves via `m_matched_attribution_battery` + `m_calibration_sweep` — with `sp_leakage_free_construction` and `sp_design_vs_information_limit` guarding the validity of all three. Nothing promised in Stage 1 falls off the chain by Stage 6. Stage 3's remaining limitations not directly sourcing a sub-problem (MAST's small-scale/no-infeasibility-category gap, SilenceIsGolden's third-party-vs-first-party gap, EHR-ChatQA's resolvable-only framing) are covered indirectly — by the released paired benchmark itself (MAST), by Stage 1's unified first-/third-party attribution definition (SilenceIsGolden), and by the harness's allowed infeasibility-declaration action (EHR-ChatQA) — rather than each requiring its own sub-problem.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** as with the B5.5 run, the recurring tension was **not disagreement about facts** (`paper.md`'s own Step 5/6/9 are unusually well-specified) but **scope discipline against a subtler failure mode this seed introduces**: distinguishing a claim about *what deployed attribution systems currently do* (Stage 4/5's `sp_trace_discriminability`/`m_matched_attribution_battery`) from a claim about *what any observer could possibly do* (`sp_design_vs_information_limit`/`m_oracle_ceiling_probe`) — and, within the latter, catching that a naively-worded ceiling hypothesis is trivially true by construction unless the held-out-generalization argument is made explicit. Both required a real critic round rather than rubber-stamping the digest's own already-strong design.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: fold every remaining finding from `stage_review.md`, `taste_audit.md`, and `design_review.md` into the final deliverables. This round completes a prior attempt that was interrupted mid-run: that attempt had already applied four changes to `paper_draft.md` (and two of their four `.tex` mirrors) plus the matching `experiment_design.md` sections; this round finished the remaining `.tex` mirrors, the overfull-hbox fix, and the record-keeping below. Historical rounds above are untouched.

**Already applied before this round (verified present, no action needed):**

- `stage_review.md` Stage 2 REVISE → nearest-neighbor sentence naming AgenTracer/Who&When and the delta — present in `paper_draft.md` (Intro ¶3, Related Work opening) and `paper_draft.tex`.
- `stage_review.md` Stage 4 REVISE → explicit **Falsification condition** line per RQ subsection — present in both draft files (4 lines, matching the current 4-RQ structure).
- `stage_review.md` Phase A re-run items 2/5/6 (cache backfill, H1 alpha/aggregation, PG-1..PG-6 gates + consequences, R1 estimand, R3 confounds, κ≥0.70, thin-cell INCONCLUSIVE, R7 subsection) → fixed 2026-07-04 in `paper.md`/`digest.md`/`reference_candidates.jsonl`, logged in `pipeline.md`.
- `stage_review.md` Phase G [moderate] finding 1 → CoR-stratified-by-difficulty reporting + secondary logistic-regression localization restored to RQ1a Metrics in both draft files.
- `design_review.md` F-1–F-6, F-9 (+ digest mirrors) → fixes 1–15 applied 2026-07-04 directly to `paper.md`/`digest.md` (B0-p placebo, B-alt2 memorization arm, B-alt3 base-rate arm, R2 plans for probe+oracle, H3 Bonferroni correction, corrected CoR power arithmetic, wrong-direction H2 wording, F-G2 pivot, B-alt1 30/70 split + three-branch rule) — recorded in `design_review.md` § "Fixes applied".
- `design_review.md` F-7 (config-not-code re-scoping) → applied by the interrupted attempt: within-domain scoping sentence + per-domain oracle bring-up milestone (PG-1/PG-2/PG-5 at 20-pair scale) in `paper_draft.md` §Datasets, `paper_draft.tex` (already mirrored pre-interruption), and `experiment_design.md` §Datasets. The `paper.md` Step 9 pass-criterion re-scope itself remains flagged "pending an executor decision" per `design_review.md` — unchanged here by design.
- `design_review.md` F-8 (trained-tracer availability + split) → applied by the interrupted attempt: pre-committed availability clause (supervision only from the B-alt1 30% held-in split; battery shrinks to 4 with stated reason, vote rules become ≥3-of-4, selection correction best-of-4) in `paper_draft.md` §Baselines-and-control-arms, `paper_draft.tex` (already mirrored pre-interruption), and `experiment_design.md` §Baseline-availability pre-commitment.
- `design_review.md` F-11 (threshold-transfer promise) → applied by the interrupted attempt as a pre-committed secondary (non-headline) analysis in `experiment_design.md` RQ1b Statistical test and `paper_draft.md` RQ1b Metrics.
- `taste_audit.md` → 🟢 both passes, zero findings; nothing to apply.

**Applied in this round:**

1. `design_review.md` F-10 (concede-and-differentiate the infeasible-task-benchmark precedent family) → the `paper_draft.md` Related Work passage added by the interrupted attempt ("A further precedent family sits inside agent benchmarks themselves… it is this combination, not infeasible-task evaluation as such, that no prior work covers") **mirrored into `paper_draft.tex`** (§Related Work, agent-self-assessment paragraph).
2. `design_review.md` F-11 → the RQ1b held-out-domain threshold-transfer sentence **mirrored into `paper_draft.tex`** (RQ1b Metrics).
3. Draft-consistency repair → B0-p sentence's clarifying parenthetical "(a real gap or above-chance AUROC on an artifact that should carry no signal)", present in `paper_draft.md`, **mirrored into `paper_draft.tex`** (control-arms paragraph).
4. `stage_review.md` Phase G [minor] finding 6 (4 overfull hboxes) → `\emergencystretch=3em` added to the `paper_draft.tex` preamble; recompiled clean (exit 0, **0** Overfull warnings, 0 undefined citations, 0 LaTeX errors).
5. `design_review.md` § "Missing RQs / reviewer questions" item 4 (no human-discrimination anchor for AUROC 0.65; B-alt1 bounds the trained-machine ceiling only) → applied as a claim hedge, not a new protocol arm: Conclusion's limitation list extended from two to three in `paper_draft.md` and `paper_draft.tex`, naming the machine-vs-human-analyst ceiling gap and the human-anchoring extension explicitly. (A human-reader study arm would be a substantive design extension the review's fix list does not mandate; not invented here.)

**Rejected as moot (with reasons):**

- `design_review.md` F-12 [NOTE] bookkeeping items → no deliverable change: (a) `stage_review.md`'s "150 harvested + 9 backfilled … of which one merged" is arithmetically self-consistent with 158 records; (b) "Two REVISE-level findings (checklist items 2, 5, 6…)" counts two underlying gaps overlapping three checklist items, per its own parenthetical; (c) the qualitative-not-hash input-record shortfall is already honestly disclosed in `pipeline.md`; (d) N3-key vs cache-key resolution-not-equality is tolerated by the review's own wording. All four concern the audit-trail files themselves, which are historical records.
- `design_review.md` F-10 re-harvest sub-item (new harvest run over the infeasible-task-benchmark axis: WebArena-unachievable / OSWorld-infeasible etc.) → **not performed, logged as the remaining open to-do**: it requires a fresh harvest run outside this revision pass's scope; the 2026-07-04 freshness sweep (2 targeted searches, both hits read in full) found no method-twin on this axis, and the concede-and-differentiate paragraph plus the estimand-scoped novelty claim (no unhedged "first" claim remains in either draft — verified by grep) cover the prose-side fix the review asked for.
- `stage_review.md` Phase G [minor] finding 5 (7 bib entries missing author fields) → unchanged: author names were never captured at harvest (OpenReview bot-wall; ACL-slice stored title/venue/year only); already logged as `pipeline.md` open to-do 1, backfill before camera-ready. Environment-blocked, not fixable in this pass.

**Cross-deliverable consistency check (post-edit):** `paper_draft.md`, `paper_draft.tex`, and `experiment_design.md` agree on the 4-RQ structure (RQ_INF_1/H1, RQ1a/H2, RQ1b/H3, RQ_INF_2/H4), 5 control arms (B0-p, B0-a, B-alt1, B-alt2, B-alt3), 2 global fallbacks (F-G1, F-G2), and every pre-registered floor/margin (FBR ≥ 0.20 with CI-LB > 0.05; 10-pp FBR−CoR at Holm-corrected family-wise α = 0.05, ≥3-of-5 vote; AUROC ≥ 0.65 with CI-LB > 0.50 at the Bonferroni-corrected 99% level; probe gate < 0.60 with ≥ 0.90 positive-control power; realized-power 0.8 INCONCLUSIVE rule; failed-solvable n ∈ ≈[180, 1530], powered at n ≳ 400). `experiment_design.md`'s four target-hypothesis strings are byte-identical to `paper.md` Step 6's H1–H4. A full normalized sentence-level diff of `paper_draft.md` vs `paper_draft.tex` after the mirrors shows no remaining content divergence (all residual diffs are markdown-vs-LaTeX formatting).
