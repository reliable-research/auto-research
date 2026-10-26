# Auto-Research-Discussion Run — B2.5 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B2.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (its own `paper.md` already runs a Step 0 asymmetry check and a Step 3 taste self-audit), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Given an LLM-agent trajectory that fails because a tool call returned a semantically wrong but syntactically/schema-valid observation, measure whether existing failure-attribution methods (LLM-judge reviewers, trained tracers, runtime monitors) misattribute responsibility to the plan or execution layer instead of the tool layer — and, if so, in which direction and why.
- **Apparent inputs:** agent trajectories (task, actions, tool observations, outcome) from existing tool-use benchmarks (AgentDojo, GAIA) and human-annotated failure logs (Who&When); a schema-preserving semantic-corruption injector; a counterfactual-replay procedure that verifies which corruption is the decisive cause; existing attribution methods run unmodified.
- **Apparent outputs:** per-trajectory attributed layer/step per method; a misattribution rate against matched overt-error controls; a misattribution-direction distribution (plan vs. execution) conditioned on corruption type/locus/subtlety; whether a minimal trust-license prompt intervention changes the rate.
- **Closest research areas:** LLM-agent failure attribution (Who&When, AgenTracer, MAST); tool-channel corruption/security (ChatInject, MCP-SafetyBench); agent robustness under overt tool unreliability (ResiliBench); lightweight runtime oversight (SupervisorAgent).
- **In scope:** measuring existing attribution methods' behavior under a controlled, ground-truth-verified corruption of tool observations, plus a lightweight prompt-level mechanism probe. **Out of scope:** proposing and training a new attribution method that fixes the bias; corruptions carrying embedded instructions (that is prompt injection, a different literature — ChatInject/MCP-SafetyBench); live/non-sandboxable production deployments.
- **Confidence: high.** Like a completed reverse-digest, the "repo" here is `digest.md` + `paper.md` — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste check (`paper.md` Step 0/Step 3). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Step 5/6, which is why stages 5/6 below are framed as validating the **measurement instrument's properties** (does the corruption stay invisible, does the ground truth verify, does the mapping rubric hold up), not re-deriving `paper.md`'s hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given an LLM agent trajectory that fails because a tool call returned a semantically incorrect but syntactically/schema-valid observation, determine whether existing failure-attribution methods (LLM-judge trajectory reviewers, trained tracers, runtime monitors) misattribute the responsible layer away from the tool that produced the corrupted observation — and if so, in which direction and why.
- `input`: (1) an agent trajectory (task, sequence of action/observation pairs, outcome) drawn from existing tool-use agent benchmarks; (2) a corruption operator that mutates one tool observation's semantic content while preserving schema/parse validity; (3) a procedure that establishes the corrupted observation is the decisive cause of the failure; (4) a set of existing attribution methods, run unmodified over the trajectory.
- `output`: (1) each method's attributed responsible layer (plan/tool/execution) and step index; (2) a misattribution rate on tool-caused failures relative to matched overt-tool-error controls; (3) the direction of misattribution (toward plan vs. toward execution) among misattributed cases; (4) whether a minimal prompt-level trust-license intervention changes the rate.
- `constraints`: injected corruption must remain schema/parse-valid, since a format error is a different fault mode than the one under study; the corrupted observation must be verified via counterfactual replay as the decisive cause, not merely correlated with failure; genuine plan-failure trajectories with independently clean observations must be available as a false-positive control.
- `objective`: an attribution method's output on the corrupted set is scored as misattributed if its labeled responsible layer ≠ tool; a claim of "systematic misattribution" is accepted only if a method's misattribution rate on schema-valid semantic corruption significantly exceeds its rate on matched overt-error controls, not merely if it is high in isolation.
- `study_type`: `empirical` — stated explicitly: the seed's own core question ("归因方法是否系统性地把责任错记") and digest N12 already settle this as a measurement/characterization study of *existing* methods, not a proposed new attribution method.

**critique:**
- summary: Strong draft, evidence-traceable to the seed, but one field names a specific technique where the problem statement should stay method-agnostic, and the objective has a real evaluability gap around a fact the seed itself flags.
- comments:
  - `{severity: major, field: "constraints", anti_pattern: "method_leak", comment: "\"verified via counterfactual replay\" names a specific technique (borrowed from AgenTracer) rather than the property the problem setting actually requires. Stage 1 should state the required property — independent verification that the corruption is decisive, not merely correlated — without committing to *how* that verification is performed; the technique choice belongs in Stage 5."}`
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "Digest C4 and N10 t1 both flag that agent frameworks disagree on the plan/tool/execution boundary and that each attribution method's native output uses a different vocabulary. The objective as written doesn't say how a method's raw output gets mapped onto the shared three-layer ontology before scoring — without a stated, pre-committed mapping rule, 'misattributed' is not yet evaluable as written, since two different mapping choices could flip the same raw output's score."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest — no new content needed).

### Refiner pass

- `constraints` (refined): "...the corrupted observation must be independently verified as the decisive cause of failure — not merely correlated with it — via a ground-truth procedure external to (and blinded from) the methods under test; genuine plan-failure trajectories with independently verified clean observations must be available as a false-positive control."
- `objective` (refined): "A regime classification is accepted only if (a) a method's misattribution rate on schema-valid semantic corruption significantly exceeds its rate on matched overt-error controls, and (b) the mapping from each method's native output vocabulary to the shared {plan, tool, execution} ontology is fixed in advance of scoring, with its own inter-rater reliability reported and cleared before any misattribution number is treated as meaningful."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "A trajectory τ = (q, (a₁,o₁), …, (a_T,o_T)) pairs a task q with actions a_t and tool observations o_t, scored by a programmatic checker V(τ) ∈ {0,1}. A corruption operator μ maps o_t ↦ o′_t while preserving schema/parse validity. An attribution method A maps τ ↦ (ℓ̂, t̂), ℓ̂ ∈ {plan, tool, execution}, via a method-specific mapping rubric R_A fixed before scoring. Determine, for corrupted trajectories whose ground truth is ℓ=tool at the injection step, whether ℓ̂ ≠ tool at a rate exceeding the same method's error rate on matched overt-error controls."
- `changes_made`: removed the named technique from `constraints`; tightened `objective`'s evaluability condition to require a pre-committed mapping rubric with reported reliability; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Failure attribution for LLM agents is being industrialized as the mechanism that routes real debugging effort — retrain the planner, patch the tool, add a retry — but every attribution method proposed so far treats the trajectory log as trustworthy evidence, so if a tool's schema-valid output is simply wrong, nothing in the current pipeline is positioned to catch that the diagnosis itself may be misdirected.
- `why_it_matters`: As deployed multi-agent systems increasingly delegate the "which component broke" decision to an LLM-judge or trained tracer rather than a human reading logs, a bias that systematically shifts blame away from the tool layer means every downstream fix aimed at "the plan" or "the execution" step is aimed at the wrong target, while the actual defect — an agent architecture that treats well-formed tool output as ground truth — goes unaddressed and unmonitored. This is not hypothetical: the same trajectory log that constitutes the failure evidence is produced by the very tool call under suspicion, so any diagnostic procedure that reads the log at face value inherits the corruption into its own premises before it starts reasoning about whose fault the failure is.
- `who_cares`: Teams operationalizing Who&When/AgenTracer-style attribution to drive planner retraining, tool patching, or data curation; designers of runtime supervisor agents deciding whether "read the trace" is a sufficient diagnostic primitive; security and robustness researchers who have shown the tool-return channel is attackable (ChatInject, MCP-SafetyBench) or unreliable (ResiliBench) but never asked whether diagnosis correctly localizes the resulting failure.
- `evidence`: Who&When's own motivation states manual failure attribution is "prohibitively expensive and inconsistent" — the explicit reason automation is being industrialized; AgenTracer's motivation frames its tracer's output as "the missing interface between failure observation and system improvement," i.e., meant to directly drive a corrective action. Neither work's fault universe includes a schema-valid corrupted tool observation: AgenTracer's programmatic injection perturbs agent actions, not tool returns, and Who&When's decisive-error definition is exercised on naturally occurring agent mistakes. ChatInject and MCP-SafetyBench show the tool-return channel is an actively exploited surface but measure attack success, not attribution correctness. Automated methods trusted to drive real interventions, and a documented fault channel those methods have never been tested against, is itself evidence the question is open.

**critique:**
- summary: Good stake-specific motivation with real citations, but coverage of stage 1's outputs is incomplete — two of the four promised outputs are left unmotivated.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 promises four outputs: attributed layer/step, misattribution rate, misattribution direction, and the trust-license intervention result. why_it_matters argues for why a bias in general is costly, but never explains why direction (plan vs. execution) or the mechanism probe specifically matter, as opposed to a single 'attribution is unreliable here' number. Without that, a reader could reasonably ask why the paper doesn't just report one unreliability rate and stop — a real, unaddressed gap."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, the misattribution's direction and cause change what kind of fix is warranted: if blame skews toward the plan layer, a team retraining planners is chasing a target that was never broken, while a skew toward execution would misdirect retry- or execution-hardening effort instead — and whether the bias traces to a removable prompt-level trust assumption or a deeper counterfactual-reasoning limitation determines whether the fix is a one-line prompt change or requires new verification machinery entirely. A bare 'attribution is unreliable here' rate, without direction or mechanism, tells a team that something is wrong but not what to change."
- `changes_made`: added the direction-and-mechanism coverage argument.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level from full motivation/method records; no title-only landscape mentions are padded in here, per the no-fabrication rule.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / is_potential_baseline / limitation → sub-problem it will motivate):

| work_id | citation | is_potential_baseline | limitation |
|---|---|---|---|
| `rw_whowhen` | Who&When (OpenReview:GazlTYxZss) | **true** | Its LLM-judge attribution takes the trajectory log as faithful evidence and its decisive-error definition is exercised on naturally-occurring agent mistakes; it never controls the condition where the log's own tool observations are semantically corrupted yet well-formed. |
| `rw_agentracer` | AgenTracer (OpenReview:l05DseqvuD) | **true** | Its programmatic fault injection perturbs agent *actions*, not tool returns — a tracer trained on action-perturbation labels has never seen a trajectory whose decisive error is a lying observation. |
| `rw_breakingagentbackbones` | BreakingAgentBackbones (OpenReview:kga18ld70t) | false (different I/O — isolates single calls, not trajectories) | Motivates the attribution-confounding problem ("difficult to attribute failures to the backbone LLM rather than tool wrappers...") but resolves it by removing the trajectory entirely, not by testing whether trajectory-level attribution mislocalizes tool-caused corruption. |
| `rw_chatinject` | ChatInject (OpenReview:WVhgFSKniL) | false (I/O mismatch — attack success, not attribution correctness) | Measures whether an attack embedded in tool content succeeds, not whether any diagnosis correctly localizes it; its corruptions are instruction-bearing payloads, outside the pure semantic-data-corruption threat model here. |
| `rw_mcpsafetybench` | MCP-SafetyBench (OpenReview:7XYjeL46co) | false | Same mismatch as ChatInject — dual eval of task/attack success, no attribution-correctness measurement. |
| `rw_resilibench` | ResiliBench (OpenReview:KTZ56LG7jZ) | false (I/O mismatch — overt error signals, not silent corruption) | Models overt tool unreliability (timeouts, invalid input) that surfaces as a visible failure signal; doesn't model a schema-valid but wrong value, and evaluates workflow adaptation, not attribution. |
| `rw_supervisoragent` | SupervisorAgent (OpenReview:pzFhtpkabh) | false (different mechanism — LLM-free trigger, not LLM-judge) | Its trigger filter fires on explicit error occurrence, repetitive behavior, or excessive observation length — precisely the signals a schema-valid corruption does not emit; structurally blind to this fault mode. |
| `rw_mast` | MAST (arXiv:2503.13657) | false (taxonomy, not a runnable baseline) | Taxonomy is distilled from human annotation of naturally occurring traces; annotators themselves consume the trace as trustworthy evidence, with no mechanism to represent corrupted-observation-caused failures. |

**critique:**
- summary: Grounding is solid and every limitation is specific and problem-tied, but one baseline label needs the same scrutiny B5.5's exemplar run applied to a mismatched-I/O "baseline."
- comments:
  - `{severity: major, field: "specific_related_works[rw_agentracer].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "AgenTracer's I/O framing — a tracer trained on action-perturbation labels — genuinely differs from this paper's need (a tracer scored on observation-corrupted trajectories it was never trained for). Marking it a straightforward baseline risks implying its own reported decisive-step accuracy is what's being compared against, which it is not. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline in the beat-a-number sense — at best a method-side reference.'"}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — the trained-tracer architecture is still legitimately runnable as a comparison arm).

### Refiner pass

- `rw_agentracer.is_potential_baseline` retained as `true`, but its note is sharpened: "Not a baseline in the beat-a-number sense — AgenTracer's own reported decisive-step accuracy is not what's compared against. Its trained-tracer architecture (or released checkpoint) is borrowed as an out-of-distribution stress test: does a tracer trained only on action-perturbation labels generalize to observation-corruption, or fail silently on it — independent of its published in-distribution numbers."
- `changes_made`: clarified AgenTracer's baseline role to avoid an implied like-for-like comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is promoted to a stage-6 framing-tier RQ — the closest candidate (whether the tool-return channel is really unaddressed by security work) is a positioning claim already carried as a Related Work claim (digest Claim 1), not a distinct empirical check this paper commits to running itself. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest C1–C4 plus the ground-truth-construction problem digest M1/M2 are built to solve):

- **`sp_ground_truth_construction`** — *description:* Construct trajectories whose failure is verifiably caused by a corrupted tool observation, and only that, when no prior work provides such labeled data. *why_it_is_a_problem:* without a verified ground truth, "misattribution" has nothing but the injection event itself to be scored against. *technical_challenge:* a schema-valid semantic corruption must simultaneously alter behavior, preserve validity, and be confirmed as the decisive cause rather than an incidental correlate — no cited method already produces this triple. *source_limitation_ids:* `["lim_agentracer_action_not_observation"]` (AgenTracer's replay-verification logic is the closest attempt, but verifies action faults, not observation faults).
- **`sp_form_invisibility`** — *description:* Ensure the injected corruption's ground-truth label carries no exploitable surface signal (parse errors, exceptions, type mismatches) that a shortcut could key on instead of genuine diagnosis. *why_it_is_a_problem:* a surface-detectable corruption would only measure whether methods bother to validate, not whether they can diagnose a well-formed lie (digest C1). *technical_challenge:* invisibility requires multiple independent gates (schema re-validation, parser acceptance, plausibility screening), since any single check could leak a signal; no cited work needs this guarantee because none scores continuous attribution against a hidden corruption. *source_limitation_ids:* `["__novel__"]`.
- **`sp_evidential_circularity`** — *description:* Determine whether misattribution is caused by attribution methods' structural reliance on the trace as evidence — reading corrupted content and treating it as true — as opposed to some other cause. *why_it_is_a_problem:* without isolating this mechanism, "misattribution happens" is descriptive, not diagnostic, and doesn't say whether the fix is architectural or superficial (digest C2). *technical_challenge:* manipulating "how much a method trusts the trace" requires an intervention that changes trust without changing capability, and confirming it doesn't just paper over a different confound (e.g., general suspicion rather than tool-specific doubt). *source_limitation_ids:* `["__novel__"]`.
- **`sp_counterfactual_entanglement`** — *description:* Separate genuine plan/execution defects from behavior that is a reasonable response to a corrupted observation, when both look identical in the raw trace. *why_it_is_a_problem:* without this separation, misattribution to the plan layer might reflect a real methodological ambiguity (the plan really was locally defensible) rather than a diagnostic failure, overstating the bias (digest C3). *technical_challenge:* judging counterfactual reasonableness requires knowledge the attribution methods don't have — what would have happened under a correct observation — which only the experimenter's injected ground truth supplies. *source_limitation_ids:* `["__novel__"]`.
- **`sp_layer_ontology_mismatch`** — *description:* Score attribution outputs that use heterogeneous native vocabularies (agent names, free-text rationales, discrete monitor flags) against one shared plan/tool/execution ground-truth ontology. *why_it_is_a_problem:* without a consistent, pre-committed mapping, differences in "misattribution rate" across methods could be an artifact of mapping generosity rather than real diagnostic differences (digest C4). *technical_challenge:* agent frameworks disagree on where a tool-selection or retrieval-component fault belongs, so the mapping rubric is itself a nontrivial design object whose own reliability must be reported before it is trusted. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five plausibly delivers stage 1's outputs) and each `source_limitation_ids` resolves correctly, but two sub-problems risk reading as one problem stated twice.
- comments:
  - `{severity: minor, field: "sp_ground_truth_construction / sp_form_invisibility", anti_pattern: "overlap", comment: "Both concern properties of the same constructed corruption, which can read as the same sub-problem described twice. They are genuinely distinct — one is about the corruption being *causally decisive* (the injected thing actually flips the outcome), the other about it being *surface-undetectable* (no gate catches it regardless of whether it flips the outcome) — but the descriptions don't make the independence of these two properties explicit."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_ground_truth_construction.technical_challenge` sharpened to end with: "...this is a **causal-decisiveness** problem — confirming the corruption is what flipped the outcome — distinct from whether the corruption is detectable; a decisive-but-detectable corruption and an undetectable-but-incidental one are both possible and both wrong for this study, for different reasons."
- `sp_form_invisibility.technical_challenge` sharpened to end with: "...this is a **surface-stealth** problem independent of decisiveness — a corruption can pass every validity gate and still turn out to be incidental to the failure, which is exactly why this sub-problem and ground-truth construction must be solved and checked separately, not treated as one property."
- `changes_made`: made the decisiveness-vs-stealth distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 1 sourced from a related-work limitation, 4 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_schema_preserving_injector`** → targets `sp_form_invisibility`. *proposed_approach:* a typed mutation-operator library (numeric perturbation, entity substitution, boolean flip, list truncation/reorder, stale-value substitution) applied to one tool return per trajectory, gated by three automated checks — schema re-validation, native parser acceptance, and an LLM plausibility screen (using a model disjoint from any judge/agent backbone) confirming the corrupted value is not self-evidently absurd in context. *key_insight:* no single validity check can certify invisibility, since each tests a different thing (type structure vs. runtime parsing vs. contextual plausibility) — passing all three simultaneously is what makes a corruption both legal and undetectable by the shortcuts an attribution method might use instead of real diagnosis. *hypotheses:* ["At least 90% of corruptions that pass all three automated gates will also be judged 'plausible in context' by an independent human rater blind to which observations were corrupted, confirming the automated screen approximates human undetectability rather than being a weaker proxy for it."]
- **`m_counterfactual_replay_oracle`** → targets `sp_ground_truth_construction`. *proposed_approach:* pair each candidate corrupted trajectory with a twin replay that restores the original observation at the same step (same seed/temperature-0 where the framework allows); keep only trajectories where the corrupted run fails the task's programmatic checker and the twin succeeds. *key_insight:* causal decisiveness is a strictly different property from surface stealth (per Stage 4's sharpened distinction) — only the twin-replay pair rules out a corruption being undetectable yet incidental to the failure. *hypotheses:* ["The yield of decisive corruptions (twin-flip rate) among schema-gate-passing candidates is at least 20% when corruptions target fields the agent's subsequent step actually references (load-bearing fields), versus a substantially lower yield for corruptions on non-referenced fields — confirming load-bearing-field targeting, not corruption volume alone, drives verified yield."]
- **`m_blinded_trust_probe_harness`** → targets `sp_evidential_circularity`. *proposed_approach:* run every attribution method blinded to injection metadata over the corrupted set; for each LLM-judge baseline, additionally run a second variant whose prompt adds exactly one sentence licensing the judge to treat tool observations as possibly unreliable and requiring independent sanity-checking; compare misattribution rate within-method, paired, with and without the license. *key_insight:* if a one-sentence license to distrust evidence the method already has access to measurably changes its verdict, the bias is best explained by the method's structural default of treating trace content as ground truth (circularity), not a hard capability ceiling, since capability didn't change — only the license did. *hypotheses:* ["For at least 2 of 3 LLM-judge variants, adding the trust-license sentence significantly reduces the misattribution rate on the corrupted set (paired test) without a significant increase in false-positive tool-blaming on genuine plan-failure controls.", "The reduction from the trust license is partial, not complete, leaving a majority of the original misattribution rate intact, because knowing observations may lie does not by itself reveal which observation lies."]
- **`m_matched_control_design`** → targets `sp_counterfactual_entanglement`. *proposed_approach:* construct two matched control sets on the same tasks and step loci as the treatment set — overt tool errors (exceptions/timeouts/empty returns) sharing the tool-layer root cause but emitting a visible signal, and genuine plan-failure trajectories with independently verified clean observations — plus a same-mutation control that injects the identical wrong value into the agent's own action rather than the tool's observation. *key_insight:* the experimenter's replay-verified ground truth supplies exactly the counterfactual comparison no attribution method under test has access to, turning "the plan step looks defensible given what the agent saw" from an unfalsifiable excuse into a measured quantity. *hypotheses:* ["Misattribution rate on the semantic-corruption treatment set exceeds misattribution rate on the matched overt-error control by a large, method-general margin (the Δ-trust gap), while misattribution on the matched agent-side-fault control (same wrong value, different locus) stays low — showing the effect is specific to the tool-observation channel rather than to the general difficulty of spotting any subtly wrong value."]
- **`m_prereg_mapping_rubric`** → targets `sp_layer_ontology_mismatch`. *proposed_approach:* before any results are seen, write one mapping rubric per attribution method that deterministically converts its native output into the shared {plan, tool, execution} label; validate via dual annotation on a held-out sample and report inter-rater agreement (Cohen's κ) as a precondition for trusting any downstream number. *key_insight:* fixing the mapping before unblinding removes the experimenter's own opportunity to (even unconsciously) choose a generous or strict mapping after seeing which answer it would produce. *hypotheses:* ["The pre-registered mapping rubric achieves Cohen's κ ≥ 0.7 between two independent annotators across all five attribution methods' outputs, and excluding rubric-disputed trajectories from the main analysis does not change the direction (though it may change the magnitude) of the headline misattribution-rate comparison."]

**critique:**
- summary: Every method has a real mechanism and every hypothesis is falsifiable with a stated threshold, but a cross-stage check surfaces a genuine gap: the seed's own core question asks for both misattribution *rate* and *direction* ("错记率与错记方向"), and Stage 1's promised output (3) is the direction of misattribution — yet no method above states a falsifiable hypothesis about *direction*. `m_matched_control_design`'s hypothesis is entirely about the Δ-trust-gap magnitude and the agent-side-fault control; it never predicts which way misattribution skews.
- comments:
  - `{severity: major, field: "m_matched_control_design.hypotheses", anti_pattern: "uncovered_hypothesis (cross-stage output coverage)", comment: "Stage 1 output (3) — 'the direction of misattribution among misattributed cases' — traces most naturally to sp_counterfactual_entanglement / this method, since the matched-control cross-tabulation is exactly the data source a direction claim would use. As drafted, no method anywhere in Stage 5 makes a falsifiable claim about direction or its dependence on corruption type/locus/subtlety. If this isn't fixed here, Stage 6 will either have to manufacture an RQ with no source hypothesis (a paraphrased_target violation) or silently drop a promised Stage 1 output — worth catching now rather than at assembly."}`
- decision: `move_to_refiner` (the fix is additive to an existing method's hypothesis list, using data the method's own design already produces — not a new mechanism, so refiner-appropriate rather than requiring a re-propose).

### Refiner pass

- `m_matched_control_design.hypotheses` extended with a second hypothesis: "Among misattributed cases, blame skews toward the plan layer rather than the execution layer (exact binomial test against 0.5), and the skew strengthens for subtle, late-trajectory, numeric/stale-value corruptions relative to overt, early, boolean/structural ones (a corruption-type/locus/subtlety factor is a significant predictor of blame direction in a mixed-effects logistic model)."
- `m_matched_control_design.key_insight` extended: "...the same cross-tabulation that supports the Δ-trust-gap magnitude claim — which layer got blamed, for which corrupted trajectories, of which type/locus/subtlety — supports a second, separately falsifiable readout (the direction and its type-dependence) from one underlying dataset: one design, two non-redundant aggregations, not two mechanisms."
- `changes_made`: added the direction/type-dependence hypothesis and justified why it is a second readout of the same method rather than a new component.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **7 hypotheses total** (1 + 1 + 2 + 2 + 1 across the five methods respectively — `m_blinded_trust_probe_harness` and `m_matched_control_design` each carry two, per the refiner's one-instrument-two-estimands justifications above).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Comparators below are sanity-check floors only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- AgentDojo (Debenedetti et al., 2024) — *justification:* real tool-calling tasks (email/banking/travel/Slack) with programmatic checkers and structured, injectable tool returns; pilot-stage domain, cheapest to instrument the injector and replay oracle against.
- Who&When failure logs (from `[Who&When, OpenReview:GazlTYxZss]`) — *justification:* source of real, human-annotated genuine-plan-failure controls and one already-logged multi-agent framework, avoiding the circularity of self-labeling "genuine" plan failures from synthetic data alone.
- (draft initially listed GAIA with justification only "digest mentions it as a source of long-horizon load-bearing observations" — flagged below.)

`baselines/comparators` (sanity-check floors, not outcome-tier competitors):
- Constant "always-predict-plan" attributor — floors the comparison: any method whose accuracy on the corrupted set doesn't beat naive majority-guessing (plan being the digest's own predicted majority direction) isn't performing attribution on corrupted evidence at all.
- Overt-tool-error arm (identical tasks/loci, visible fault signal) — the necessary comparator for the Δ-trust gap.
- Matched agent-side-fault arm (same wrong value, injected into the agent's action instead of the tool's observation) — isolates whether the effect is specific to the tool-observation channel or just "subtly wrong values are hard to spot anywhere."

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_screen_undetectability` | `sp_form_invisibility` | "At least 90% of corruptions that pass all three automated gates will also be judged 'plausible in context' by an independent human rater blind to which observations were corrupted, confirming the automated screen approximates human undetectability rather than being a weaker proxy for it." |
| `rq_verified_yield` | `sp_ground_truth_construction` | "The yield of decisive corruptions (twin-flip rate) among schema-gate-passing candidates is at least 20% when corruptions target fields the agent's subsequent step actually references (load-bearing fields), versus a substantially lower yield for corruptions on non-referenced fields — confirming load-bearing-field targeting, not corruption volume alone, drives verified yield." |
| `rq_trust_license_reduces` | `sp_evidential_circularity` | "For at least 2 of 3 LLM-judge variants, adding the trust-license sentence significantly reduces the misattribution rate on the corrupted set (paired test) without a significant increase in false-positive tool-blaming on genuine plan-failure controls." |
| `rq_trust_license_partial` | `sp_evidential_circularity` | "The reduction from the trust license is partial, not complete, leaving a majority of the original misattribution rate intact, because knowing observations may lie does not by itself reveal which observation lies." |
| `rq_delta_trust_gap` | `sp_counterfactual_entanglement` | "Misattribution rate on the semantic-corruption treatment set exceeds misattribution rate on the matched overt-error control by a large, method-general margin (the Δ-trust gap), while misattribution on the matched agent-side-fault control (same wrong value, different locus) stays low — showing the effect is specific to the tool-observation channel rather than to the general difficulty of spotting any subtly wrong value." |
| `rq_direction_skew` | `sp_counterfactual_entanglement` | "Among misattributed cases, blame skews toward the plan layer rather than the execution layer (exact binomial test against 0.5), and the skew strengthens for subtle, late-trajectory, numeric/stale-value corruptions relative to overt, early, boolean/structural ones (a corruption-type/locus/subtlety factor is a significant predictor of blame direction in a mixed-effects logistic model)." |
| `rq_mapping_reliability` | `sp_layer_ontology_mismatch` | "The pre-registered mapping rubric achieves Cohen's κ ≥ 0.7 between two independent annotators across all five attribution methods' outputs, and excluding rubric-disputed trajectories from the main analysis does not change the direction (though it may change the magnitude) of the headline misattribution-rate comparison." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E3 and Walking-Skeleton numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[GAIA]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it' says nothing about which RQ needs it or why. GAIA differs from AgentDojo in a way that should be load-bearing (longer causal chains between an early observation and its downstream use) but the draft doesn't say so."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "GAIA (Mialon et al., 2023) — *justification:* long-horizon, multi-step tool-use tasks where a single early observation is load-bearing many steps later; used specifically to stress-test `rq_direction_skew`'s locus factor (early/mid/late injection tercile) and its type-dependence claim under longer causal chains than AgentDojo's shorter tasks provide, rather than being included only because the digest names it as a source."
- `changes_made`: gave GAIA's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the Stage 1 critic explicitly removed one that had crept into `constraints`).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_ground_truth_construction.source_limitation_ids = ["lim_agentracer_action_not_observation"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (attributed layer/step, misattribution rate, misattribution direction, trust-license result) are each reachable: layer/step via `sp_layer_ontology_mismatch`; rate via `sp_ground_truth_construction` + `sp_form_invisibility` + `sp_counterfactual_entanglement`'s Δ-trust gap; **direction** via `sp_counterfactual_entanglement`'s direction hypothesis (added at Stage 5's critic round — this is exactly the item that would have silently fallen off the chain without that catch); trust-license result via `sp_evidential_circularity`. Nothing promised in Stage 1 is unreachable by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** unlike a typical run where stages disagree on facts, this seed material is unusually well-specified (`paper.md` had already worked out the injector, replay oracle, and controls in detail), so the recurring tension was **scope discipline on the seed's own two-part core question** — "错记率与错记方向" (rate *and* direction). The rate half of that question is easy to cover with a Δ-trust-gap style comparator; the direction half is easy to silently drop because it isn't a separate mechanism, just a different aggregation of the same data — which is exactly what Stage 5's critic round caught and the refiner fixed by adding a second hypothesis to `m_matched_control_design` rather than inventing a sixth method.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup to a *prior, already-confirmed* stage was required (the Stage 5 fix was applied within Stage 5's own refiner pass, before that stage was confirmed).

---

## Post-review revision round (2026-07-05)

> Revision pass over the three review artifacts (`stage_review.md`, `taste_audit.md`, `design_review.md`), folding every still-open finding into the deliverables. This round **resumed an interrupted prior attempt** (killed mid-run by an API limit on 2026-07-05, ~01:35–02:02): that attempt had already applied the F-8 tier-accounting line, the F-4/H3 McNemar power band (RQ3), the detection-vs-attribution readout (RQ3 metrics), and the judge-capability axis (RQ5 setup) to `experiment_design.md`, and the RQ3 ≥5 pp / RQ5 10 pp+competence-bar wording to `paper_draft.md` — but left a dangling reference ("wrong-direction rule (ii) in the global fallbacks below") to rules that did not exist, no H4 body section, no suffix-length confound anywhere, no fraction aggregation rule, and none of the 2026-07-05 `.md` edits mirrored into `paper_draft.tex`. This round completed and repaired that work; no section or row was duplicated.

### Findings ledger (source review → finding → status → what changed, in which file)

**stage_review.md** (all findings were applied on 2026-07-04; verified still in place, no action this round):
- Stage 2 REVISE (nearest-neighbor sentence naming Who&When/AgenTracer) → **verified applied** — present in `paper_draft.md`/`.tex` Related Work opening.
- Stage 4 REVISE (Falsification condition line in all 7 RQ subsections) → **verified applied** — present in all 7 RQ subsections of `paper_draft.md`/`.tex`.
- Phase A fixes 1–5 (digest N12 absence_comment; 8 cache records; Estimand sentence; A1–A7 consequence column; confound-removal ledger) → **verified applied** in `digest.md`/`paper.md`/`reference_candidates.jsonl`.

**taste_audit.md**: 🟢 verdict in both the original audit (§1–6) and the Phase-H re-audit (§7); no action items — nothing to apply. This round's edits touch Experiments/protocol substance only (no Abstract/Method-Overview framing change), so goal.md §3 item 8's re-audit trigger does not fire.

**design_review.md**:
- F-1 (B0 not null-by-construction) → **already applied 2026-07-04** (paper.md B0-placebo, fixes 1–2; spliced into draft) — verified.
- F-2 (unvalidated plausibility screen) → **already applied 2026-07-04** (paper.md R2 instrument-validation section + gate G5, fix 7) — verified.
- F-3 (scale-up config-not-code) → **already applied 2026-07-04** (paper.md skeleton framework-reach + G6 narrowing rule, fixes 8–9) — verified; `experiment_design.md` RQ5 already cites the G6 gate.
- F-4, H2 half (E2 power) → **already applied 2026-07-04** (paper.md fix 5; RQ6 bands in both deliverables) — verified. F-4, H3 half (McNemar discordant-rate power) → **completed this round**: prior attempt had added the ≥72-discordant-pairs band to `experiment_design.md` RQ3; now mirrored into `paper_draft.md`/`.tex` RQ3 Setup.
- F-5(1) (F0 premise-collapse fallback) → **already applied 2026-07-04** (paper.md fix 3; premise-collapse branch in both deliverables) — verified. F-5(2) (F2b) → **already applied 2026-07-04** (paper.md fix 6) — verified.
- F-5(3) (significantly negative Δ uncovered) → **applied this round**: wrong-direction rule (i) added to `experiment_design.md` Global fallbacks; full-prominence wrong-direction sentence added to `paper_draft.md`/`.tex` RQ5 Falsification condition.
- F-5(4) (license-increases-misattribution uncovered) → **applied this round**: wrong-direction rule (ii) added to `experiment_design.md` Global fallbacks (repairing the prior attempt's dangling RQ3 cross-reference); wrong-direction sentence added to `paper_draft.md`/`.tex` RQ3 Falsification condition.
- F-6 (fault-to-manifestation-distance confound on the headline Δ) → **applied this round**: suffix-length stratification of Δ_A with pre-committed collapse interpretation added to `experiment_design.md` RQ5 (Statistical test + Metrics) and `paper_draft.md`/`.tex` RQ5 Setup; post-fault suffix length added as a fixed-effect covariate to the RQ6 mixed model in both deliverables (covariate control only — the verbatim H2/H2b hypotheses are untouched).
- F-7 (harvest recall / novelty certification) → **already resolved 2026-07-04** second pass: targeted freshness sweep on the core manipulated variable (found + digested Causal Agent Replay, screened out arXiv:2606.21409) plus PDF caching for the core records — see `pipeline.md` Phase-A-residual and freshness-sweep rows. No further action possible without network beyond what was done.
- F-8 (human-annotator arm has no registered hypothesis) → **completed this round**: prior attempt had added only the tier-accounting mention; the H4 descriptive-arm body section (stratified 10% subsample per digest M3, CI readout vs. best automated method and overt-error control, pre-committed wording for both directions, explicitly no pass/fail bar) now added to `experiment_design.md`; matching "Human-annotator reference arm" paragraph added to `paper_draft.md`/`.tex` Experimental Setup.
- F-9 (MAST asserted from memory, id_resolves false) → **already resolved 2026-07-04** second pass (MAST arXiv:2503.13657 PDF fetched, fully digested, flag cleared) — verified via `pipeline.md` Phase-A-residual row.
- F-10 (stale 7-RQ draft vs. revised paper.md) → **already resolved 2026-07-04** E/F pass (B0-placebo/F0/power-band splice; placeholders marked; pipeline row documents the pre-execution-scaffold status) — verified.
- F-11 (estimand sentence length) → **rejected — moot for the deliverables**: `paper_draft.md`'s Problem Definition already carries a tight one-sentence estimand anchor ("The object of study is whether … exceeding the same method's error rate on matched trajectories where the tool fault is overt rather than schema-valid."); F-11's cosmetic complaint targets `paper.md`'s ~95-word sentence, which is the binding spec (not a prose deliverable) and was explicitly marked cosmetic by the reviewer.
- Missing-RQs item 1 (humans fooled too?) → same as F-8, **completed this round**.
- Missing-RQs item 2 (judge-capability axis) → **completed this round**: prior attempt had added it to `experiment_design.md` RQ5 Setup; now mirrored into `paper_draft.md`/`.tex` RQ5 Setup.
- Missing-RQs item 3 (detection-vs-attribution decomposition) → **completed this round**: prior attempt had added the descriptive readout to `experiment_design.md` RQ3 Metrics; now mirrored into `paper_draft.md`/`.tex` RQ3 Metrics.
- Missing-RQs item 4 (screen-cutpoint sensitivity) → **applied this round** to `experiment_design.md` RQ1 (0.7/0.9 re-stratification clause, importing what `paper.md`'s instrument-validation step 5 already pre-registers — no new content invented).
- Missing-RQs item 5 (what would B0-null look like) → same as F-1, already applied — verified.
- Missing-RQs item 6 (Δ stratified by fault-to-manifestation distance) → same as F-6, **applied this round**.
- Failure-space walk, "pre-commit the majority rule as a fraction, not an absolute count" (A5-drop denominator) → **applied this round**: fraction-form aggregation rule added to `experiment_design.md` RQ5 and `paper_draft.md`/`.tex` RQ5 Expected outcome.
- Failure-space walk, "pre-declare the A3 evidence add-ons in F-G1" → **applied this round**: one-line add-on list (contamination analysis, headroom vs. constant-attributor floor, maintenance statement) appended to the F1/F-G1 rule in `experiment_design.md` Global fallbacks.

### Hygiene checks this round

- **Target hypotheses byte-identical to `paper.md`/Stage 5:** all seven `target_hypotheses` blocks in `experiment_design.md` untouched by this round's edits (verified — every edit landed in Setup/Statistical-test/Expected-outcome/Falsification/Metrics/global sections only).
- **`.md` ↔ `.tex` sync:** the two stale 2026-07-05 `.md`-only edits from the interrupted attempt (RQ3 "≥5 pp absolute" expected outcome; RQ5 "at least 10 pp" + overt-error competence-bar conditional) were mirrored into `paper_draft.tex` along with all of this round's new prose; `latexmk -pdf -interaction=nonstopmode -halt-on-error paper_draft.tex` exits 0, 14 pages, zero undefined-citation warnings.
- **Cross-deliverable consistency:** 7 RQs in both deliverables (+H4 descriptive arm in both, marked no-tier/no-bar in both); effect floors and margins match (RQ3 ≥5 pp / ≤3 pp FPR / ≥72 discordant pairs; RQ5 ≥10 pp / 40% competence bar / fraction majority rule; RQ6 π_plan 0.65 / 120–50 bands; RQ1 90%/60%; RQ2 20%/10%; RQ7 κ ≥ 0.7); no mismatch remains.
