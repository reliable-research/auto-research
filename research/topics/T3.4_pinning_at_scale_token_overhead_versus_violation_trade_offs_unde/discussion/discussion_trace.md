# Auto-Research-Discussion Run — T3.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T3.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (a full pre-registered spec already existed), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure whether and when the token overhead of exhaustively "pinning" (verbatim-repeating) a growing standing constraint set — from single digits to several hundred rules — begins to reduce an LLM agent's task success rate, and design a bounded-budget selective-pinning policy for which constraints to keep resident at each turn.
- **Apparent inputs:** a constraint pool of size *n* (each constraint carrying a verification procedure and a ground-truth applicability label), an agent task suite with programmatically checkable episodes, a fixed per-turn token budget, and a pinning policy (full / none / selective-*k*).
- **Apparent outputs:** constraint-violation rate, token overhead, and task success rate — each as a function of (*n*, policy, model) — plus a selective-pinning selection policy and its measured position on the resulting three-way trade-off surface.
- **Closest research areas:** multi-constraint instruction following (RECAST); standing-item retention under long-context distraction (PrefEval, ICF-Bench); agent context/history management (Sculptor, AgentFold); budget-constrained context compression (COMI); controlled cognitive-load benchmarking (CogniLoad); positional degradation in long context (Lost in the Middle).
- **In scope:** measuring existing prompted LLM agents' violation/overhead/success trade-off under a constraint-count sweep, and evaluating a family of selective-pinning policies as compared conditions inside that sweep. **Out of scope:** training or fine-tuning new agents/models; mid-episode constraint churn (constraints revoked, revised, or added after the episode starts — the ICF-Bench setting); multi-session persistence.
- **Confidence: high.** Unlike a typical autoclaude repo scan, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste self-check (`paper.md` Step 0/3). Reconstruction risk is low; the risk instead is *redundancy* with `paper.md`'s own Step 5/6, which is why stages 5/6 below are framed as validating the **measurement instrument's properties** (including one honestly hypothesis-free component), not re-deriving `paper.md`'s hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given an LLM agent maintaining a standing set of *n* constraints (*n* scaling from single digits to several hundred), each with a verification procedure, and a pinning policy governing which subset of the *n* constraints is kept resident in the agent's context at each turn under a fixed per-turn token budget, determine when the token cost of keeping all *n* constraints resident begins to reduce the agent's task success rate, and design a bounded-budget selection policy for which constraints to keep resident at each turn.
- `input`: (1) a constraint pool of size *n*, each constraint *c* carrying a verification procedure (programmatic checker or calibrated LLM judge) and, per (constraint, episode, turn), a ground-truth applicability label; (2) an agent task suite whose episodes terminate in a programmatically checkable end state; (3) a fixed per-turn token budget; (4) a pinning policy — full (all *n* verbatim every turn), none (stated once), or selective-*k* (a bounded *k*-token budget with a selector).
- `output`: (1) constraint-violation rate as a function of (*n*, policy, model); (2) token overhead — absolute and as a fraction of the prompt — as a function of (*n*, policy, model); (3) task success rate as a function of (*n*, policy, model); (4) a selective-pinning selection policy together with its measured position on the resulting three-way trade-off surface.
- `constraints`: violations must be attributable per (constraint, episode, turn) triple, not only at the episode level; constraint count *n* must be experimentally separable from raw prompt length and from applicability density (the fraction of the *n* constraints that actually bind in a given episode), or any observed count effect is confounded; episode success must resolve to a programmatic, not subjectively judged, end-state check.
- `objective`: "A characterization of the trade-off is accepted only if (a) it determines, via a pre-registered segmented-regression test with a stated significance threshold, whether task success under full pinning has a breakpoint as a function of *n*; and (b) any selective-pinning policy is judged only relative to a budget- and capability-matched floor (a random-*k* selector at the same token budget), not against full pinning's absolute cost."
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12's own classification ("the paper's spine is a controlled measurement study... exactly the shape of the empirical exemplars this digest imitates") and the seed's own core question ("何时反噬") settle this as a characterization study, not a proposed system pitched to beat a baseline.

**critique:**
- summary: Grounded and specific, but the objective has a real evaluability gap on both of its own clauses, and the summary's framing quietly presupposes the answer to part of what's being measured.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "Clause (a) states 'whether' a breakpoint exists but doesn't say what counts as a valid finding if none is detected up to the tested range — paper.md's own E1 fallback text explicitly pre-commits to reporting 'no detectable task-success knee... the cost of exhaustive pinning is economic, not behavioral' as a legitimate result, not a failed characterization. Clause (b) has the same gap in the other direction: it says selectors are judged against a floor, but never states that *no selector clearing the floor* is itself an accepted, reportable outcome (paper.md's own E2 fallback: 'no budgeted selector matched full pinning... full pinning is the only reliable policy below the knee'). As written, a reader could infer the objective is only satisfied by a favorable result in both directions, which is not what the underlying design actually commits to."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'determine when the token cost... begins to reduce... task success' presupposes a breakpoint exists before it has been measured — the same presupposition digest N9's own falsification condition for RQ1 explicitly guards against ('refuted if... full-pinning task success shows no statistically significant decline... i.e., pin everything is always at least as good'). Prefer 'whether, and if so when' over 'when'."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content the source material already states explicitly — no new content needed).

### Refiner pass

- `objective` (refined): "A characterization of the trade-off is accepted only if (a) it determines, via a pre-registered segmented-regression test with a stated significance threshold, whether task success under full pinning has a breakpoint as a function of *n* — reporting 'no detectable breakpoint up to the tested range' as a valid, non-null finding, not a failure to characterize; and (b) any selective-pinning policy is judged only relative to a budget- and capability-matched floor (a random-*k* selector at the same token budget) — with 'no selective policy clears the floor, so full pinning remains the only reliable option below the knee' being an equally valid, accepted finding as 'a selective policy clears the floor.'"
- `summary` (refined): "...determine **whether, and if so when,** the token cost of keeping all *n* constraints resident begins to reduce the agent's task success rate, and design a bounded-budget selection policy..." (removes the presupposition that a breakpoint necessarily exists).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation): "Episode *e* = (τ, C, π, m, s): task τ, constraint set *C* with |C| = *n*, pinning policy π ∈ {full, none, selective-*k*}, model *m*, seed *s*. Per turn *t*: applicability label app(c, e, t) ∈ {0,1}, detector verdict viol(c, e) ∈ {0,1} on applicable pairs. V(n, π, m) = violation rate, O(n, π, m) = overhead ratio, S(n, π, m) = task success. Determine whether logit(S) under π=full has a breakpoint in log *n*, and whether any π=selective-*k* achieves V within a stated non-inferiority margin of π=full at a fraction of O(full)."
- `changes_made`: tightened both clauses of the objective's evaluability condition (null results explicitly accepted in both directions); removed a presupposition from `summary`; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Pinning — repeating every standing constraint verbatim in every turn — is the default, lowest-effort engineering fix for making sure an LLM agent "sees" safety rules, user preferences, and policy constraints, but nothing establishes whether this practice continues to work as standing constraint sets scale from a handful of rules to the hundreds now typical of production deployments.
- `why_it_matters`: The token cost of verbatim repetition grows linearly with the rule count, while nothing guarantees the compliance benefit grows with it too — RECAST's own motivation documents that "even advanced models experience substantial performance degradation when multiple requirements are present," and AgentFold's motivation independently observes that append-only context "produces context saturation... where the few facts that matter are mixed with noise." Treating "pin everything" as a free safety default silently substitutes an assumption (more rules pinned ⇒ more rules obeyed) for a measured fact, and if that assumption breaks down past some scale, the choice that looks safest on paper is the one quietly costing the most task performance.
- `who_cares`: Practitioners deploying LLM agents with large standing policy/safety/preference sets (enterprise agent platforms, regulated-industry copilots) who currently pin by default; designers of context-management middleware deciding whether to build selective-retrieval layers for standing constraints, not just for task history; researchers extending context-compression techniques (validated for evidence/QA retrieval) into the normative-constraint setting, where dropping the wrong unit causes a rule violation rather than a wrong answer.
- `evidence`: `[RECAST, OpenReview:90tCp2KszA]`'s own motivation cites FollowBench-style findings that models degrade substantially as simultaneous-requirement count grows; `[AgentFold, OpenReview:IuZoTgsUws]`'s own motivation documents context saturation in append-only agent histories; `[COMI, OpenReview:OGDIXDfaN4]`'s own framing treats compression as "a constrained information-selection problem" but only for query-relevant evidence, never for normative content whose omission is a violation rather than a wrong answer — no corpus paper jointly measures violation rate, token overhead, and task success while sweeping the count of simultaneously active constraints (digest N4, six independent limitations), itself evidence the question is open.

**critique:**
- summary: Grounded, stake-specific, and cites real sources, but coverage of stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is a selective-pinning *policy*, not just a diagnostic reading. why_it_matters motivates why the trade-off exists and why it's costly, but never explains why a validated *selection policy* specifically matters, as opposed to a simpler fix: 'measure the knee n*, then just cap the standing rule count below it.' Without addressing that, a reader could reasonably ask 'why build a selector at all — why not just keep the rule count under the knee?' — a real, unaddressed gap, since the standing rule count in a production deployment (safety rules, compliance policy, per-customer preferences) accumulates independent of what any single agent task actually needs at a given step."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, telling a deployer 'just cap the constraint count below the knee' is not actionable when the standing rule count is not the deployer's free choice — safety rules, compliance policy, and per-customer preferences accumulate independently of what a single agent task needs at any one step, so the count itself cannot simply be shrunk. The live decision a deployer actually faces is not *how many* rules to have on the books, but *which bounded subset* needs to be resident in context at a given step — which is exactly the decision a validated selection policy operationalizes, and a diagnostic reading of the knee alone does not."
- `changes_made`: added the actionability argument covering the previously unmotivated selective-pinning-policy output.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / role / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_recast` | Anon., RECAST (OpenReview:90tCp2KszA) | false (trains new models; scales *satisfaction*, not representation cost) | Improves constraint satisfaction via training + verification rewards, but treats the constraint set as free to represent — never measures the token cost of carrying *n* constraints across a multi-turn trajectory, nor sweeps *n* into the hundreds. |
| `rw_prefeval` | Anon., PrefEval (OpenReview:QWunLKbBGF) | false (single-preference retention, not many-constraint) | Tests whether one preference per query survives a long distractor-filled conversation; never scales to simultaneously-active constraint counts, and reports compliance only — no token-overhead or task-success cost of any retention mitigation. |
| `rw_icfbench` | Anon., ICF-Bench (OpenReview:hcJywRYc3n) | false (tests forgetting one revoked item, not retaining many standing items) | Isolates whether a model can suppress one revoked/revised instruction; doesn't scale the count of simultaneously active standing constraints and reports no overhead measure. |
| `rw_sculptor` | Anon., Sculptor (OpenReview:HPeiH7da0Z) | false (curates task history, not standing rules) | Actively manages the task-history workspace (fragment, hide, restore) but treats the standing instruction/policy block as fixed; never reports constraint-violation rate as an outcome at all. |
| `rw_agentfold` | Anon., AgentFold (OpenReview:IuZoTgsUws) | false (folds accumulating history, not standing constraints) | Learns a folding policy over accumulating sub-trajectory history; doesn't touch which of hundreds of standing rules deserve context residence. |
| `rw_comi` | Anon., COMI (OpenReview:OGDIXDfaN4) | **true** | Scores and compresses context units by informational relevance to a query, validated for evidence/QA; unvalidated where "relevance" means rule-applicability to the current action and where compressing a rule's wording can destroy its enforceability. |
| `rw_cogniload` | Anon., CogniLoad (OpenReview:0Sex2H5Jnn) | **true** | Tunes distractor density and length as independently tunable load factors for factual/reasoning material, measuring answer accuracy only; no analogous sweep exists for the count of pinned normative constraints, jointly against violation/overhead/success. |
| `rw_lostinthemiddle` | Liu et al. (2024, TACL), Lost in the Middle (arXiv:2307.03172) | false (canonical positional-degradation anchor, not runnable) | Shows single retrieval targets can go unused when buried in long context; doesn't quantify compliance decay as the number of simultaneously binding items grows, nor the overhead of keeping them all resident. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but two `is_potential_baseline=true` labels are conflating two different kinds of "borrowing" into one flag.
- comments:
  - `{severity: major, field: "specific_related_works[rw_comi, rw_cogniload].is_potential_baseline", anti_pattern: "io_approach_mismatch (partial)", comment: "COMI and CogniLoad are marked true with no distinction, but they play structurally different roles here. COMI's marginal-information-gain scoring is literally implemented and run as one of the five selector variants inside this paper's own selective-pinning sweep — a genuine, evaluated comparison arm at matched token budgets. CogniLoad's own reported numbers are on a disjoint task domain (synthetic reasoning under tunable distractor/length/complexity) and are never run or compared against here at all — only its factorial *design principle* (decoupling load dimensions so degradation attributes to one factor) is borrowed as this paper's own experimental-design blueprint. Marking both `true` identically risks implying CogniLoad's published numbers are a comparator, which they are not — study_type=empirical forbids exactly this kind of 'beats baseline X' framing (stages.md tier-violation check), so this distinction needs to be explicit before it reaches stage 6's baseline list."}`
- decision: `move_to_refiner` (a wording/classification-precision fix — the underlying literature engagement doesn't change).

### Refiner pass

- `rw_comi.is_potential_baseline` retained `true`, note sharpened: "A genuine evaluated arm, not a borrowed idea only — COMI's marginal-gain selector is implemented and run as one of the five `M3` selector variants (the 'comi' arm) and its violation rate/overhead is directly measured at matched token budgets against the paper's other selectors."
- `rw_cogniload.is_potential_baseline` **changed to `false`**, note added: "Not a baseline in any sense — CogniLoad's own reported numbers are on an unrelated task domain (synthetic reasoning) and are never compared against. Only its factorial-design *principle* is reused as this paper's own experimental blueprint for the constraint-count sweep harness."
- `changes_made`: clarified COMI's role as a genuinely-run comparison arm; corrected CogniLoad's over-eager `true` flag to `false` since no CogniLoad number is ever compared against.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`rw_lostinthemiddle`'s limitation, "positional degradation doesn't quantify compliance decay as item count grows") is not a distinct framing check but restates this paper's own core question, already covered end-to-end as mechanism-tier RQs in Stage 6. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C5):

- **`sp_budget_vs_load`** — *description:* Determine when a per-turn token budget that is finite, faced against a standing constraint count that is in principle unbounded, actually overflows or crowds out task-content tokens. *why_it_is_a_problem:* Any claim about full pinning "backfiring" is only meaningful if the point of crowding-out is actually located and quantified, not assumed. *technical_challenge:* Nothing in the pinning practice itself imposes a ceiling on constraint count — the token cost scales linearly with *n* with no built-in circuit breaker, so the crowding-out point is an empirical fact to locate, not a design parameter to read off. *source_limitation_ids:* `["__novel__"]` — no cited work measures the representation cost of a growing constraint set at all (RECAST scales satisfaction, not cost).
- **`sp_interference_dilution`** — *description:* Determine whether pinning *more* constraints reduces compliance to *each* constraint even when every constraint still fits comfortably within the token budget. *why_it_is_a_problem:* If this mechanism is real, "the budget hasn't overflowed yet" is not the same as "nothing is being lost" — a distinct failure mode from the budget-overflow one above. *technical_challenge:* Any observed decline as *n* grows is naturally confounded with the fact that pinning more constraints also means a longer prompt — isolating an interference effect from a pure length effect requires a control that holds length fixed while varying only constraint content. *source_limitation_ids:* `["lim_sculptor_agentfold_history_not_rules", "lim_lostinthemiddle_single_target_only"]`.
- **`sp_dynamic_applicability`** — *description:* Determine which constraints actually bind at a given step, given that applicability is task- and state-dependent and must be re-decided every turn rather than computed once. *why_it_is_a_problem:* A selection policy that can't tell which constraints are currently relevant will either under-select (missing a binding rule) or over-select (defeating the point of a budget). *technical_challenge:* Applicability is a normative matching question ("does rule *r* bind action *a* in state *s*?"), not a semantic-similarity question, and no prior work validates whether the two coincide. *source_limitation_ids:* `["lim_comi_evidence_not_norms"]`.
- **`sp_multiobjective_frontier`** — *description:* Characterize the joint violation-rate / token-overhead / task-success surface without collapsing it to one scalar, since acceptable trade-offs differ by constraint class (a safety rule and a formatting preference do not price violations equally). *why_it_is_a_problem:* Forcing a single scalar objective would silently bake in a value judgement about which constraint classes matter more. *technical_challenge:* there is no principled way to pick weights across constraint classes from the data alone. *source_limitation_ids:* `["__novel__"]`.
- **`sp_detector_validity`** — *description:* Establish that measured violation-rate curves reflect actual agent behavior rather than the error of whatever automatic detector produced them. *why_it_is_a_problem:* At hundreds of constraints across multi-turn episodes, exhaustive human checking is infeasible, so every downstream curve is only as trustworthy as the detector — an unvalidated detector could manufacture or mask the very trade-off being characterized. *technical_challenge:* semantic (LLM-judged) constraints have no ground truth cheaper than human annotation, so detector error must be bounded empirically, not assumed away. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's outputs), but two sub-problems risk reading as the same underlying claim ("more constraints hurt") stated twice.
- comments:
  - `{severity: minor, field: "sp_budget_vs_load / sp_interference_dilution", anti_pattern: "overlap", comment: "Both are framed as 'adding constraints eventually hurts,' which can read as one sub-problem restated. They are genuinely distinct — one is an *economic* crowding-out problem (token budget physically runs out or starves task content), the other is an *attention-interference* problem (compliance to each rule degrades even while every rule still fits comfortably in the budget) — but the descriptions don't make that distinction explicit enough for a reader to see they're different failure mechanisms requiring different controls."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_budget_vs_load.technical_challenge` sharpened to end with: "...this is a **budget-capacity** problem — it is resolved (or not) purely by counting tokens against the ceiling, independent of whether compliance to any individual rule degrades."
- `sp_interference_dilution.technical_challenge` sharpened to end with: "...this is an **attention-interference** problem distinct from budget capacity — it can occur *before* the token budget is ever exhausted, so no amount of headroom in the budget rules it out; the fix is a length-matched control, not a bigger budget."
- `changes_made`: made the budget-capacity-vs-attention-interference distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations — one from two combined limitations, one from a single limitation — 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_overhead_instrumentation`** → targets `sp_budget_vs_load`. *proposed_approach:* Instrument the full-pinning condition directly: log tokenizer counts of the constraint block per turn (absolute and as a fraction of the prompt) alongside task success, across the full *n*-sweep; fit a segmented (piecewise-linear) regression of logit(task success) on log *n* and test for a breakpoint (Davies test). *key_insight:* the crowding-out point cannot be assumed or computed analytically — it has to be *located* empirically, and a segmented model is what turns "does it back­fire" into a falsifiable breakpoint claim with a confidence interval rather than an eyeballed trend. *hypotheses:* ["Under full pinning, task success as a function of constraint count n has a detectable breakpoint (segmented regression, Davies test p < 0.05, 95% bootstrap CI inside [25, 400]), with success at n=400 at least 10 percentage points below success at n=10 in at least 2 of 3 tested models.", "Violation rate at n=400 exceeds violation rate at n=10 by at least 3 percentage points (absolute) in at least 2 of 3 tested models under full pinning, even though every constraint remains resident in context at every turn."]
- **`m_deconfounded_sweep_harness`** → targets `sp_interference_dilution`. *proposed_approach:* Build a factorial harness in which constraint count *n*, applicability density (fraction of the *n* constraints that actually bind), and raw prompt length are independently controlled — specifically, a length-matched inert-padding arm that replaces constraints with same-length non-normative text, holding token count fixed while removing all normative content. *key_insight:* an interference effect and a pure-length effect make the *same prediction* (success declines as more text is pinned) unless something holds length fixed while varying only content — the padding control is the only way to separate them. *hypotheses:* ["Length-matched inert padding reproduces at most 50% of the full-pinning task-success decline observed at n=400 (statistically distinguishable at α=0.05), and at fixed n=100, high applicability density raises violation rate by at least 0.03 (absolute, p<0.05) relative to low density."]
- **`m_selective_pinning_family`** → targets `sp_dynamic_applicability`. *proposed_approach:* Under a fixed token budget *k*, implement and re-run five selectors every turn — random-*k* (floor), static top-*k* by pilot-measured violation frequency, embedding similarity, COMI-style marginal-gain scoring, and an LLM applicability classifier — each scored against the ground-truth applicability labels from the sweep harness. *key_insight:* the only way to test whether normative applicability reduces to semantic similarity is to build a selector that is deliberately *not* similarity-based (the applicability classifier) and compare it, at the same budget, against selectors that are. *hypotheses:* ["At n ≥ 100 with a selective-pinning budget of 25% of full pinning's constraint tokens, the best-performing selector achieves a violation rate non-inferior to full pinning within 0.02 absolute (one-sided 95% CI) while using at most 30% of full pinning's overhead.", "The applicability-classifier selector achieves a violation rate at least 0.03 (absolute) lower than the best similarity-based selector (embedding or marginal-gain) at n ≥ 100 (Holm-corrected)."]
- **`m_violation_detector`** → targets `sp_detector_validity`. *proposed_approach:* Route rule-based constraints to exact programmatic checkers and semantic constraints to an LLM judge, calibrated against a 300-episode human-annotated stratified sample (by *n*, policy, constraint class) before any curve is interpreted. *key_insight:* detector error is a confound on every downstream curve, not a separate side-question — gating on a pre-registered agreement threshold before reading any curve is what keeps a noisy detector from silently manufacturing or masking the very trade-off being characterized. *hypotheses:* ["The dual-mode violation detector reaches Cohen's κ ≥ 0.80 against human annotation on a 300-episode stratified sample, with programmatic checkers reaching at least 0.95 raw agreement, after at most one calibration iteration."]
- **`m_tradeoff_tracker`** → targets `sp_multiobjective_frontier`. *proposed_approach:* Log the full (*n*, policy, model, seed) → {violation rate, overhead ratio, task success} table and render it as a Pareto surface with per-constraint-class breakdowns, rather than collapsing to one weighted scalar. *key_insight:* forcing a single objective would bake in an arbitrary weighting across constraint classes that no data-driven procedure can justify; reporting the surface, not resolving it, is the honest characterization. *hypotheses:* **none** — see critique below.

**critique:**
- summary: Every other method has a real falsifiable hypothesis with a stated threshold, but `m_tradeoff_tracker` has zero — is that an oversight, or a legitimate design choice?
- comments:
  - `{severity: major, field: "m_tradeoff_tracker.hypotheses", anti_pattern: "possible unfalsifiable_hypothesis (by omission)", comment: "stages.md requires every method's hypotheses to be falsifiable claims — this method has none at all. Digest N6 itself already flags this honestly: `unaddressed_challenges: ['C4']`, with the explicit note that the trade-off-tracker argument 'describes the frontier, not resolving it,' supplying 'no principled decision rule for which frontier point a deployer should choose.' Before accepting a zero-hypothesis method, this needs to be confirmed as an intentional, disclosed design choice rather than a gap that quietly drops `sp_multiobjective_frontier`'s coverage at stage 6 — and if it's intentional, the paper draft needs to say so explicitly rather than let a reader assume an oversight."}`
- decision: `move_to_refiner` (this is a disclosure fix, not a redesign — inventing a hypothesis the source material doesn't support would violate the refiner's own conservatism rule).

### Refiner pass

- `m_tradeoff_tracker` **confirmed hypothesis-free by design**, with an explicit note added rather than a manufactured claim: "This component is deliberately descriptive, not hypothesis-bearing: digest N6 already discloses (`unaddressed_challenges: ['C4']`) that no principled decision rule exists for collapsing the three-axis surface to a single preferred operating point, and inventing a falsifiable claim here — e.g., a specific weighting across constraint classes — would manufacture content the source material explicitly declines to supply. Reporting the Pareto surface *is* this sub-problem's resolution under `study_type: empirical`: the contribution is the measured, non-collapsed characterization itself, not a claim about where the frontier's 'right' point sits. Consequently, `sp_multiobjective_frontier` is covered by a method at stage 5, but — uniquely among the five sub-problems — generates zero stage-6 research questions, and that is a correct, not a missing, count."
- `changes_made`: added the explicit disclosure note; no hypothesis invented.
- `declined_to_fix`: the major flag itself — confirmed as intentional rather than "fixed" by adding content.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (1 + 2 + 2 + 1 + 0 across the five methods respectively — `m_selective_pinning_family` carries two falsifiable claims from one experimental design, mirroring `m_overhead_instrumentation`'s own two-claim structure: one instrument, two separately falsifiable estimands each), and one method (`m_tradeoff_tracker`) that is deliberately, disclosedly hypothesis-free — a design choice explained above, not a gap.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 4 RQs**, jointly covering all 6 Stage 5 hypotheses (two RQs each cover a pair of hypotheses tested by one shared experimental setup, verbatim `target_hypotheses`; two RQs cover one hypothesis each). `m_tradeoff_tracker` contributes zero RQs, correctly, per its Stage 5 disclosure.
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check / floor comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- τ-bench (airline/retail policy-following tool-use tasks) — *justification:* real domain policies as constraint seeds, task success via database-state checks; the primary task suite for every RQ.
- IFEval / FollowBench — *justification:* rule-based constraint sources (verifiable instructions, multi-level constraint templates), scaled via RECAST-style mining to build the *n*-up-to-400 constraint pool that every RQ draws from.
- PrefEval — *justification:* semantic-constraint source and long-context distractor protocol, feeding the LLM-judged remainder of the constraint pool (≥30%) that RQ4 (detector validity) specifically needs to stress-test.
- (draft initially listed LMSYS-Chat-1M with justification "distractor conversation filler, as used by PrefEval" — flagged below.)

`baselines` (sanity-check/floor comparators, not outcome-tier competitors):
- Full pinning — the stress-tested default every other condition is compared against.
- No pinning (B0) — the necessary "why does this problem exist at all" control.
- Random-*k* selector at the same token budget — the capability-matched floor that any claim about applicability-aware selection must clear.
- Length-matched inert-padding arm — the rival-explanation control isolating count from raw length.

`research_questions` (4, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_full_pinning_knee` | `sp_budget_vs_load` | "Under full pinning, task success as a function of constraint count n has a detectable breakpoint (segmented regression, Davies test p < 0.05, 95% bootstrap CI inside [25, 400]), with success at n=400 at least 10 percentage points below success at n=10 in at least 2 of 3 tested models."; "Violation rate at n=400 exceeds violation rate at n=10 by at least 3 percentage points (absolute) in at least 2 of 3 tested models under full pinning, even though every constraint remains resident in context at every turn." |
| `rq_selective_pinning_viability` | `sp_dynamic_applicability` | "At n ≥ 100 with a selective-pinning budget of 25% of full pinning's constraint tokens, the best-performing selector achieves a violation rate non-inferior to full pinning within 0.02 absolute (one-sided 95% CI) while using at most 30% of full pinning's overhead."; "The applicability-classifier selector achieves a violation rate at least 0.03 (absolute) lower than the best similarity-based selector (embedding or marginal-gain) at n ≥ 100 (Holm-corrected)." |
| `rq_count_vs_length_density` | `sp_interference_dilution` | "Length-matched inert padding reproduces at most 50% of the full-pinning task-success decline observed at n=400 (statistically distinguishable at α=0.05), and at fixed n=100, high applicability density raises violation rate by at least 0.03 (absolute, p<0.05) relative to low density." |
| `rq_detector_validity` | `sp_detector_validity` | "The dual-mode violation detector reaches Cohen's κ ≥ 0.80 against human annotation on a 300-episode stratified sample, with programmatic checkers reaching at least 0.95 raw agreement, after at most one calibration iteration." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E4 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to verbatim hypotheses, but one dataset's justification doesn't tie to any of the four confirmed RQs.
- comments:
  - `{severity: major, field: "datasets[LMSYS-Chat-1M]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'as used by PrefEval' is a provenance note, not a hypothesis-linked reason — it says where the idea came from, not which RQ needs it. Checking against all four confirmed RQs: RQ2's count-vs-length control is a length-matched *inert-padding* arm, not realistic distractor conversation; none of the four RQs test whether irrelevant conversational history (as opposed to constraint count, prompt length, or applicability density) affects compliance. Unlike PrefEval's own setting — where a single preference must survive being buried inside a long, unrelated conversation — this paper's constraints are always pinned (deliberately resident, never buried), so the distractor-conversation mechanism PrefEval needs doesn't have a clear analogue in this design at all."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry for LMSYS-Chat-1M **dropped**, not re-justified: unlike Stage 3's GLEE-style situation in other topics where a weak justification can be tightened into a hypothesis-linked one, none of the four confirmed RQs actually needs a realistic-distractor-conversation dimension — inventing one to keep the dataset would add scope the confirmed hypotheses never asked for, which the refiner is explicitly not permitted to do. Noted instead as a **further-evaluation** item: a future extension that adds a distractor-conversation dimension (constraints buried in irrelevant dialogue history, not just pinned) would need its own RQ and is out of scope here.
- `changes_made`: removed a dataset with no hypothesis-linked justification rather than manufacturing one; documented the removal as a scope decision, not an oversight.
- `declined_to_fix`: none (this stage's fix was a subtraction, not an addition).

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_interference_dilution.source_limitation_ids = ["lim_sculptor_agentfold_history_not_rules", "lim_lostinthemiddle_single_target_only"]` ∈ Stage 3 ✓; `sp_dynamic_applicability.source_limitation_ids = ["lim_comi_evidence_not_norms"]` ∈ Stage 3 ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` entry is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (violation rate, overhead, task success, selective-pinning policy) are each reachable: violation rate/overhead/success via `sp_budget_vs_load` + `sp_interference_dilution` + `sp_multiobjective_frontier`'s Pareto reporting, gated throughout by `sp_detector_validity`; the selective-pinning policy via `sp_dynamic_applicability` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** the recurring tension was not disagreement about facts (the seed material — a full pre-registered `paper.md`, not just a digest — is unusually well-specified) but **honest disclosure discipline**: repeatedly having to decide whether a stage-5/6 gap (no hypothesis for `m_tradeoff_tracker`; a dataset with no hypothesis-linked reason) should be patched by inventing content, or disclosed as a genuine, bounded limitation. In both cases the refiner declined to invent and instead made the gap explicit — consistent with digest N6's own `unaddressed_challenges` flag and with the no-fabrication rule.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: fold every finding in `stage_review.md` and `taste_audit.md` into the final deliverables. A prior revision attempt was interrupted mid-run (after editing `paper_draft.md` but before mirroring to `paper_draft.tex` and before logging); this round completed the mirroring and the log entries — no finding was re-applied twice. Historical rounds above are unmodified.

| # | Source | Finding | Status / what changed | File(s) |
|---|---|---|---|---|
| 1 | `stage_review.md` Stage 2 REVISE | Related Work must name the nearest-neighbor prior work (RECAST = domain, CogniLoad = method) with an explicit delta | already applied (verified present in Related Work opening paragraph and Introduction) | `paper_draft.md`, `paper_draft.tex` |
| 2 | `stage_review.md` Stage 4 REVISE | Every RQ subsection needs an explicit **Falsification condition** line, drawn from `paper.md`'s pre-committed Fallback text | already applied (verified in all four RQ subsections) | `paper_draft.md`, `paper_draft.tex` |
| 3 | `stage_review.md` Phase A item 2 | 8 works cited by `digest.md` N3/N4 missing from the reference cache | already applied (158/158 records carry final verdicts) | `reference_candidates.jsonl` |
| 4 | `stage_review.md` Phase A item 5 / 6.4 | Assumption ledger A1–A6 lacked `Gate:` / `Consequence if false:` slots | already applied (verified in `paper.md` "## Assumptions") | `paper.md` |
| 5 | `stage_review.md` Phase A item 6.1 | No single estimand sentence (R1) in Step 5 | already applied (verified in `paper.md` Step 5) | `paper.md` |
| 6 | `stage_review.md` Phase A item 6.6 | M4 detector lacked full 5-step instrument-validation plan; E4 fallback must trigger per-class on systematic confusion-structure failure | applied in `paper.md` (prior pass); propagated into RQ4 Setup ("two human raters", confusion-structure inspection), Falsification condition (per-class withdrawal), and Metrics of the draft — `paper_draft.md` edit made by the interrupted prior attempt, **mirrored into `paper_draft.tex` this round**; already present in `experiment_design.md` RQ4 | `paper.md`, `paper_draft.md`, `paper_draft.tex`, `experiment_design.md` |
| 7 | `stage_review.md` Phase A item 6.7 | No single place named which confound each design constraint removes (R3) | already applied (Confound-accounting table, 6 rows, in `paper.md`); draft's Methodology "Insight" paragraphs already name each confound in prose — no further draft change needed | `paper.md` |
| 8 | `stage_review.md` Phase A item 6.9 | No pre-declared rule for under-powered cells (388-episode/arm INCONCLUSIVE floor) | applied in `paper.md` (prior pass); propagated into RQ1 Sample-size rationale of the draft by the interrupted prior attempt, **mirrored into `paper_draft.tex` this round**; already present in `experiment_design.md` (grid note + RQ1–RQ3) | `paper.md`, `paper_draft.md`, `paper_draft.tex`, `experiment_design.md` |
| 9 | `stage_review.md` Phase A item 6 (fix 6) | TOST and GEE previously used undefined | TOST expanded to "two-one-sided-tests (TOST) equivalence test" in RQ2 falsification condition (draft edit by prior attempt, **mirrored into `.tex` this round**); GEE expanded to "Generalized Estimating Equations (…)" in `experiment_design.md` RQ1 statistical test **this round**; `paper.md` already defined both | `paper_draft.md`, `paper_draft.tex`, `experiment_design.md` |
| 10 | `stage_review.md` Phase A item 2 follow-on / item 7 / "Deferred" | Freshness-sweep repositioning against 3 new method-twins (`2512.22087` CAT, `2512.23457` HiR, `2607.02255` AgenticSTS) | **rejected for this round — deliberately deferred by the review itself** to pre-Phase-E: guidance.md Part 4 situation 6 requires a considered concede-and-differentiate repositioning of `digest.md`/`paper.md` (reading the three papers), not a quick prose patch; remains tracked in `pipeline.md` | — (tracked, unchanged) |
| 11 | `taste_audit.md` | Verdict 🟢, all three conditions clean; sole soft note (boilerplate = 1: "production policy/safety/preference sets") explicitly judged acceptable by the audit itself | no action required — no finding rises to a change request | — |

**Recompile:** `latexmk -pdf` clean — `paper_draft.pdf` regenerated (12 pages) from the mirrored `.tex`.

**Cross-deliverable consistency check (this round):** 4 RQs in `paper_draft.md` = 4 RQs in `experiment_design.md` = 4 E-experiments in `paper.md` ✓; effect floors and margins match everywhere (10 pp success floor, 3 pp / 0.03 violation deltas, δ = 0.02 non-inferiority margin with ±0.02 TOST equivalence margin, 25% budget / 30% overhead cap, ≤ 50% padding-arm reproduction, κ ≥ 0.80, ≥ 0.95 programmatic agreement, 450 episodes/cell with 388/arm INCONCLUSIVE floor) ✓; `experiment_design.md`'s target hypotheses remain byte-identical to the Stage 5 = Stage 6 verbatim strings (H1/H1b/H2/H2b/H3/H4), numerically consistent with `paper.md`'s binary criteria ✓. One mismatch found and fixed: bare "GEE" in `experiment_design.md` (item 9 above).
