# Discussion Trace — T5.5 (auto-research-discussion, Stages 1-6)

> Extracted verbatim from `pipeline.md`'s original Stage 1-6 transcript (the
> `auto-research-discussion` skill's own six-stage record: every draft version,
> every critique with severities and resolution, every refiner pass, and the final
> cross-stage consistency check). Moved here per the skill's updated Final-deliverables
> spec, which separates the discussion trace from `pipeline.md`'s goal.md phase-gate
> log. Nothing below has been re-run, re-worded, or re-derived — this is the same
> content that already fed `paper.md` and `paper_draft.*`.

# Auto-Research-Discussion Run — T5.5 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T5.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries Step 0 asymmetry, Step 2 archetype, Step 3 taste self-audit, Step 5 formal definitions, Step 6 pre-registered experiments with fallbacks, and a Claim–Evidence Map), so genuine disagreement surfaced but didn't require re-proposing from scratch.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Three REVISE findings from `stage_review.md` (a related-work coverage gap on architecture-conformance-checking tooling, an ill-conditioned mechanism-share metric in the Method, and a missing contamination/leakage check in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those three fixes. A nearest-neighbor sentence and per-RQ falsification conditions were built into the stage outputs and the assembled draft from the start (not left for `stage_review.md` to catch), so `stage_review.md` was deliberately pushed to find different, genuine issues rather than re-reporting those two.

## Seed brief

- **One-sentence description:** Measure how much enforcing machine-checkable design constraints on LLM coding agents degrades functional pass rate and inflates generation cost, and characterize whether the resulting compliance-utility frontier degrades gracefully or exhibits a sharp knee.
- **Apparent inputs:** executable coding-task suites (BigCodeBench-Hard, a SWE-bench Verified subset) with unit-test/fail-to-pass oracles; a κ-audited catalog of ~20 machine-checkable design rules parameterized by breadth × strictness; an enforcement-mechanism arm (prompt-only / checker-in-the-loop retry / binary all-on); a model.
- **Apparent outputs:** per-(task, strength, arm, model) attempt records (pass/fail, violation count, cost); aggregated per-cell pass rate, violation rate, and cost; a statistically tested shape verdict (graceful vs. knee) on the pass-rate-vs-strength and cost-vs-strength curves; a cost decomposition attributing price to mechanism vs. constraints.
- **Closest research areas:** constraint-following measurement (IFEval, FollowBench, RECAST, AutoIF); executable coding-agent benchmarks (SWE-bench, BigCodeBench-style suites); alignment-tax / Pareto-frontier characterization (NSPO, RMOD, FairFront); inference-time constrained decoding (SMC-Control); the single closest published template, one constraint dimension's cost (HiddenCost-Readability, ICSE 2026).
- **In scope:** measuring existing prompted/enforced LLM coding agents under a parametric constraint-strength sweep. **Out of scope:** training or fine-tuning a new agent or enforcement technique as the contribution; non-code constraint domains; constraint types with no executable/deterministic oracle.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest + pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste self-audit (paper.md Step 0/Step 3) and its own honest corpus-coverage report (digest N3). Reconstruction risk is low; the risk is *redundancy* with paper.md's own Step 5/Step 6, which is why stages 5/6 below are framed to add instrument-validity and confound-isolation structure the schema specifically demands (mechanism-share well-posedness, instruction-load confound, catalog-fidelity gate) rather than re-deriving paper.md's headline hypotheses verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given an LLM coding agent, a suite of coding tasks with executable pass/fail oracles, and a catalog of deterministic, machine-checkable design-constraint rules organized along a breadth (how many rules active) × strictness (per-rule threshold) strength axis, determine how task pass rate, residual constraint-violation rate, and generation cost jointly vary as constraint strength increases under a given enforcement mechanism, and characterize whether the resulting frontier degrades gracefully or exhibits a detectable knee.
- `input`: (1) a set of coding tasks each with an executable correctness oracle (unit tests / fail-to-pass tests); (2) a catalog of K deterministic design rules, each a decision procedure over static analysis of a candidate solution, addressable at strength σ = (breadth b, strictness s); (3) an enforcement arm a ∈ {prompt-only, checker-in-the-loop retry, binary all-on}; (4) a model m.
- `output`: (1) per-(task, σ, a, m, sample) attempt records: pass/fail, violated-rule count, generation cost; (2) aggregated per-cell pass rate, violation rate, and cost; (3) a statistically tested shape verdict — graceful vs. knee — for the pass-rate-vs-σ and cost-vs-σ relationships, per model × arm.
- `constraints`: design rules must be deterministic and machine-checkable — "violation" has to be an objectively computable output, not a judgment call, for the sweep to be well-defined at all; every attempt must terminate in a scored pass/fail outcome and a logged cost within a bounded interaction budget.
- `objective`: a shape verdict is accepted only if it is assessed jointly across both the pass-rate and the cost curves and reported separately per model (never pooled); if the two curves' shape verdicts disagree (e.g., pass-rate looks graceful while cost looks knee-shaped, or vice versa), that cell is reported as *shape-discordant* rather than resolved by picking one axis as authoritative.
- `study_type`: `empirical` — stated explicitly: digest N12 already settles this as a measurement/characterization study over *existing* coding agents ("the headline claim being a statistically tested shape verdict... over existing LLM coding agents, with... nothing new... trained"), not a proposed enforcement technique or agent being pitted against baselines to win.

**critique:**
- summary: Strong, evidence-traceable draft — but the objective silently assumes pass-rate shape and cost shape will always tell the same story, which the seed's own material explicitly denies.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "Digest N5's C2 states plainly that 'pass rate, violation rate, and cost need not vary monotonically or independently as constraint strength increases' — i.e., a knee in the cost curve and a knee in the pass-rate curve are not guaranteed to coincide. paper.md's own H2 tests 'Pass@1 (and log-CCS) vs. strength' as two separate fits per model×arm, but nowhere states what the paper concludes if pass-rate says 'graceful' while cost says 'knee' for the same cell. Without naming this as a first-class possibility, the objective is not fully evaluable — a reader can't tell what 'the frontier's shape' even means when its two defining axes disagree."}`
  - `{severity: minor, field: "constraints", anti_pattern: null, comment: "The determinism/machine-checkability constraint is real and load-bearing (it's what makes 'violation' measurable at all), but it's currently stated without saying *why* it's a constraint on the problem rather than an incidental method choice — worth one clause tying it to measurability, so a reader doesn't mistake it for a hidden method leak."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A shape verdict is accepted only if it is assessed jointly and independently across the pass-rate-vs-σ and cost-vs-σ relationships, reported separately per model × arm (never pooled). Where the two axes' verdicts agree, the cell is classified graceful or knee accordingly; where they disagree, the cell is reported as **shape-discordant** — a distinct, informative outcome in its own right, not an artifact to be resolved by an arbitrary tie-break or by treating one axis as automatically authoritative over the other."
- `constraints` (refined, one clause added): "...design rules must be deterministic and machine-checkable — because the sweep's entire measurement instrument depends on `violation` being an objectively computable output rather than a judgment call, any rule that cannot be checked this way cannot enter the catalog, independent of how well it captures real design intent (that fidelity risk is itself the subject of a later sub-problem, not resolved here)."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Task set T (function-level T_f, repository-level T_r). Rule catalog R = {r_1..r_K}, each r a deterministic decision procedure over static analysis of a candidate solution y. Strength σ = (b, s) ∈ breadth × strictness (ordinal ladder L in the pilot, factorial grid in the scale-up); active set R(σ) ⊆ R. Enforcement arm a ∈ {P, R, B}. Model m. Attempt = (task, σ, a, m, sample) ⇒ pass(y,t) ∈ {0,1}, violation count V(y,σ), cost c(attempt). Determine, per (m, a), whether pass(·)-vs-σ and cost(·)-vs-σ are each graceful or knee-shaped, and whether the two verdicts agree."
- `changes_made`: made cross-axis shape disagreement a first-class, named outcome instead of an unaddressed evaluability gap; tied the determinism constraint explicitly to measurability; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Enforcing design constraints on coding agents is routinely treated as a low-cost governance lever — "just add the architectural rules to the prompt or the linter" — but whether compliance is actually cheap, and whether its price scales at a predictable, near-linear rate, has never been directly measured for coding agents.
- `why_it_matters`: As organizations delegate production code generation to LLM agents, they increasingly want those agents to obey not just functional correctness but design-level constraints (layering rules, dependency direction, complexity ceilings, forbidden APIs). Mandating this is not free: every enforced rule draws on the same bounded generation process that functional correctness draws on (paper.md Step 0), so it is a candidate source of reduced pass rate and inflated cost. Adjacent evidence makes the worry concrete without yet answering it for this setting: instruction-following benchmarks document substantial degradation as the number of simultaneous constraints grows (FollowBench), and the safety-alignment literature has named the analogous phenomenon an "alignment tax" (NSPO) — but neither measures repository-level design constraints against an independent functional-correctness oracle, jointly with cost, for coding agents specifically.
- `who_cares`: Engineering teams deciding whether to enforce architectural conformance via LLM coding agents rather than a separate static-analysis gate; SE-tooling vendors pricing "design-aware" agent offerings; researchers deciding whether alignment-tax-style utility-compliance trade-offs, documented elsewhere, transfer to the coding-agent setting with its own cost accounting (tokens, retries, wall-clock).
- `evidence`: HiddenCost-Readability (ICSE 2026) shows that *one* semantically neutral constraint dimension (formatting) is nearly free — negligible Pass@1 change, ~24.5% token savings when removed — establishing that not all constraints are expensive, which makes the price of *semantically binding* design constraints (layering, dependency direction) an open empirical question rather than an assumed one. FollowBench's own reported degradation curves and RECAST's motivation ("constraint satisfaction... degrades substantially as constraints accumulate") are the nearest adjacent signal that compliance is *not* free in general. No corpus paper (digest N3, 11,683-paper search across 8 query angles) jointly sweeps design-constraint strength and measures a pass-rate × violation-rate × cost frontier for coding agents — itself evidence the specific question is open.

**critique:**
- summary: Good stake-specific motivation with real, non-fabricated evidence — but it justifies "does compliance cost something" while leaving unmotivated *why a shape verdict*, specifically, is the decision-relevant deliverable rather than a single average cost-per-constraint number.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a *shape* verdict (graceful vs. knee vs. shape-discordant) — a claim about the curve's geometry, not its average slope. why_it_matters motivates why compliance cost matters at all but never explains why a team would care about the difference between a graceful frontier and a knee-shaped one if both have the same average cost over the range they've already piloted. paper.md's own Step 0 gestures at this ('deployability is a function of where that knee sits, not of the average price') but that argument doesn't yet appear in the Stage-2 motivation itself — a reader could reasonably ask 'why not just measure the average price per rule and extrapolate,' and nothing here answers that."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a team that measures only the *average* cost across a limited pilot range (say, L0–L2) cannot tell a graceful frontier from a knee-shaped one from that average alone — both can show the identical average slope over the piloted range while implying opposite deployment decisions past it: a graceful frontier means cost scales predictably as more rules are added, while a knee means the same additional rule that looked cheap at L2 becomes catastrophically expensive at L3. Extrapolating linearly from an average, rather than testing the curve's shape directly, is exactly the mistake that would make 'design-aware coding agents are affordable' a claim that quietly stops being true the moment real deployments push past whatever strength was piloted — which is precisely why the frontier's *shape*, not its average price, is the deliverable this problem is built to produce."
- `changes_made`: added the shape-vs-average argument, grounding it in paper.md Step 0's own asymmetry language rather than inventing new content.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (full motivation/method texts read, per N3's grounding procedure); no additional landscape papers are invented here to pad a `general_related_works` list, and no citation appears that isn't already grounded in digest N3.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_swebench` | Anon., SWE-bench (OpenReview:VTF8yNQM66) | false (task substrate, not a competing measurement) | `lim_swebench_no_constraint_axis`: Defines utility purely as fail-to-pass resolution; no design-constraint dimension, no violation-rate metric, cost outside scoring — cannot reveal what compliance costs. |
| `rw_recast` | Anon., RECAST (OpenReview:90tCp2KszA) | false (training objective, not measurement) | `lim_recast_autoif_construct_narrow` *(shared with AutoIF)*: Optimizes/measures satisfaction of *code-verifiable* NL constraints; reports satisfaction rates without jointly measuring pass-rate and cost price paid for enforcement; explicitly confined to code-verifiable constraint types (RECAST's own motivation), not repository-level design/architecture constraints. |
| `rw_autoif` | Anon., AutoIF (OpenReview:cRR0oDFEBC) | false | *(shares `lim_recast_autoif_construct_narrow` above)* |
| `rw_smccontrol` | Anon., SMC-Control (OpenReview:xoXn62FzD0) | false (inference-time mechanism, not a swept frontier) | `lim_smc_control_mechanism_cost`: Provides an enforcement mechanism whose compute grows with constraint difficulty ("neither token-local nor cheap," its own motivation) but evaluates constraint satisfaction/distributional fidelity, not a swept strength-vs-pass-rate-vs-cost frontier. |
| `rw_nspo` | Anon., NSPO (OpenReview:GFyVxtyMvq) | false | `lim_nspo_different_axis`: Documents/mitigates the utility tax of *one* constraint class (training-time safety alignment); doesn't parametrize constraint strength; trade-off axes (harmlessness vs. reasoning) aren't the inference-time design constraints of coding agents. |
| `rw_rmod` | Anon., RMOD (OpenReview:i0Nno5MgXt) | false | `lim_rmod_assumes_reward_models`: Treats the multi-objective trade-off as given (reward models per objective already exist) and solves decode-time weight selection; doesn't empirically map what the compliance-utility-cost frontier looks like for agentic coding. |
| `rw_fairfront` | Anon., FairFront (OpenReview:65oFEAP42P) | false (methodological precedent only) | `lim_fairfront_closed_form_only`: Computes exact Pareto fronts only under classification-style closed form (Bayes-optimal posteriors, concave utilities); open-ended code generation admits no such closed form — the frontier here must be measured empirically. |
| `rw_hiddencost_readability` | Pan, Sun, Zhang, Lo, Du, HiddenCost-Readability (ICSE 2026, arXiv 2508.13666) | **true** | `lim_hiddencost_single_neutral_dimension`: Measures token-cost/pass-rate impact of *one*, semantically neutral constraint (formatting), removable without changing program behavior; doesn't study semantically binding design constraints (layering, dependency, complexity) that can conflict with task solutions, nor any enforcement-strength sweep. |
| `rw_ifeval` | Zhou et al., IFEval (arXiv 2311.07911) | false | `lim_ifeval_followbench_no_utility_axis` *(shared with FollowBench)*: Measures constraint-satisfaction degradation as constraints accumulate on general instruction tasks, without an independent functional-correctness oracle — compliance can't be traded off against task utility, and cost isn't an evaluation axis. |
| `rw_followbench` | Jiang et al., FollowBench (ACL 2024) | **true** | *(shares `lim_ifeval_followbench_no_utility_axis` above)* |

**critique:**
- summary: Grounding is solid and every limitation is specific, traceable to a real citation's own text — but two baseline labels need scrutiny, for the same reason.
- comments:
  - `{severity: major, field: "specific_related_works[rw_hiddencost_readability, rw_followbench].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Both are marked straightforward baselines, but their I/O framing genuinely differs from this paper's: HiddenCost-Readability studies one semantically neutral, single-dimension constraint (formatting) with no repository-level design semantics and no strength sweep; FollowBench's constraint ladder is over NL instructions with no functional-correctness oracle at all. Per the stage-3 rubric, works with mismatched I/O are 'not a baseline — at best a method-side reference.' Marking them straightforward baselines risks implying their published numbers are being compared against, which they are not."}`
- decision: `move_to_refiner` (wording-precision fix — the borrowed *protocol structures* are still legitimately reusable as comparison arms/design templates).

### Refiner pass

- `rw_hiddencost_readability.is_potential_baseline` retained `true`, note sharpened: "Not a baseline in the beat-a-number sense — its own formatting-only numbers are not compared against. Its **paired-comparison significance-testing protocol** (McNemar / Mann-Whitney on pass-rate deltas at matched token budgets) is borrowed as the statistical-methodology template for this paper's own pass-rate comparisons, independent of its published formatting-specific findings."
- `rw_followbench.is_potential_baseline` retained `true`, note sharpened: "Not a baseline in the beat-a-number sense — different domain (NL instructions, no functional oracle) means its reported satisfaction curves are never compared against directly. Its **graded incremental-levels protocol structure** is the direct template this paper's L0–L4 ordinal ladder adapts, extended with an independent pass/fail oracle and a cost axis it doesn't have."
- `changes_made`: clarified both works' roles to avoid an implied I/O-mismatched comparison, while preserving the legitimate protocol-borrowing relationship.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is promoted to a stage-6 framing-tier RQ — the closest candidate (digest N3's own "no corpus paper does this jointly" observation) is a novelty/coverage claim about the *literature*, not a testable property of *this* paper's own procedure, so it doesn't fit the framing-tier's definition. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (6 sub-problems, from digest N5's C1–C4 plus two additional decisive components the schema's structure specifically demands):

- **`sp_operationalization_validity`** — *description:* Convert qualitative, natural-language design intent ("keep layers decoupled") into a deterministic, sweepable rule catalog without the catalog silently drifting from real design intent. *why_it_is_a_problem:* any measured violation rate is only as valid as the catalog's fidelity to actual design norms — an unfaithful catalog measures agreement with the checker, not with design intent, which would make every downstream frontier claim an artifact of catalog choice. *technical_challenge:* rules chosen for checkability may systematically over-represent trivially mechanical constraints (naming, complexity ceilings) while under-representing subtler architectural intent (cohesion, separation of concerns) that resists deterministic checking, and there is no ground truth "correct" catalog to calibrate against except human judgment itself — exactly what a deterministic checker exists to replace. *source_limitation_ids:* `["lim_recast_autoif_construct_narrow"]` — RECAST/AutoIF's own limitation (confined to code-verifiable constraint types) is precisely why moving to deeper, AST-level architectural rules is a harder, unaddressed operationalization problem.
- **`sp_signal_variance`** — *description:* Attribute an observed pass-rate/cost change across strength levels to constraint strength itself, rather than to ordinary LLM sampling variability. *why_it_is_a_problem:* without this, any observed trend — graceful or knee-shaped — is unfalsifiable, since a handful of noisy attempts can manufacture the appearance of either. *technical_challenge:* requires enough independent attempts per (level, model, arm) cell for a task-level random-effects model to detect a true strength-driven effect against sampling noise, with a power check run *before* committing scale-up budget, not assumed. *source_limitation_ids:* `["__novel__"]`.
- **`sp_shape_detectability`** — *description:* Determine, with enough sweep resolution, whether the pass-rate/cost-vs-strength relationship is smooth or contains a breakpoint, without assuming the functional form a priori. *why_it_is_a_problem:* retry loops can simultaneously depress pass rate and inflate cost (C2), so a coarse or mis-spaced sweep could manufacture a spurious knee from noise, or wash out a genuine one — and the shape claim is exactly what determines engineering feasibility (paper.md Step 0), so an under-resolved sweep undermines the paper's central deliverable. *technical_challenge:* breakpoint detection needs both enough distinct strength levels to localize a change point and a test that doesn't over-fit noise as a knee, and the "right" number/spacing of levels can't be chosen before a pilot signal exists. *source_limitation_ids:* `["__novel__"]`.
- **`sp_strength_dimensionality`** — *description:* Constraint "strength" has at least two logically separate axes — breadth (how many rules active) and strictness (each rule's threshold) — that a single ordinal ladder conflates into one number. *why_it_is_a_problem:* if breadth and strictness affect pass rate/cost differently, a one-dimensional sweep can't attribute degradation to either axis, so any "knee" found on the ladder is really a knee in some undefined combination of the two. *technical_challenge:* a full factorial sweep of both axes multiplies the number of cells combinatorially, so disentangling the axes competes directly against the sweep-budget constraint a measurement study of this kind must respect. *source_limitation_ids:* `["__novel__"]`.
- **`sp_mechanism_attribution`** — *description:* Separate how much of the measured cost and pass-rate loss comes from the enforcement mechanism itself (prompt overhead, checker-in-the-loop retry blowup) versus from the design constraints being enforced. *why_it_is_a_problem:* reporting a single-mechanism frontier risks the frontier being a property of the harness's chosen enforcement machinery rather than of the constraints — a different (or future, smarter) mechanism could shift it entirely, making any "compliance is expensive" claim an artifact of implementation choice. *technical_challenge:* under one mechanism, constraint content and mechanism overhead are perfectly confounded within a single run; isolating them requires identical constraint sets run under mechanically distinct enforcement arms, modeling the interaction with strength. *source_limitation_ids:* `["lim_smc_control_mechanism_cost"]` — SMC-Control's own motivation ("neither token-local nor cheap") is the direct precedent for why enforcement-mechanism cost must be isolated from constraint-content cost.
- **`sp_instruction_load_confound`** — *description:* Distinguish behavioral/cost change caused specifically by design-constraint *content* from change caused merely by the presence of more/longer instructions in the prompt, regardless of what they say. *why_it_is_a_problem:* every arm that renders active rules as prompt text necessarily lengthens the prompt as strength grows, so without a control, any observed pass-rate drop or cost rise could be a generic instruction-load effect (documented for unrelated constraint types by FollowBench) rather than something specific to design constraints — undercutting the entire "price of compliance" framing in favor of a "price of verbosity" one. *technical_challenge:* content and length are naturally correlated in the raw prompt-only arm; isolating them requires a control that matches token count while emptying semantic content, a manipulation distinct from any of the three enforcement arms already defined. *source_limitation_ids:* `["__novel__"]` — this is the paper.md B-alt placebo control's underlying confound (t2 in N10's threat list), not one of N5's C1–C4, but a decisive component the study's own mandatory-baselines section already treats as non-optional.

**critique:**
- summary: Coverage checks out (solving all six would jointly deliver Stage 1's shape-verdict objective across both curves and both strength axes); one pair of sub-problems risks reading as the same confound twice.
- comments:
  - `{severity: minor, field: "sp_mechanism_attribution / sp_instruction_load_confound", anti_pattern: "overlap", comment: "Both are 'isolate a confound' sub-problems and could read as the same one restated. They are genuinely distinct — one is about which *enforcement arm* (prompt vs. retry) causes cost, the other is about whether *any* arm's effect is really about constraint content vs. mere prompt length — but the descriptions don't make the axis of difference explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_mechanism_attribution.technical_challenge` sharpened to end with: "...this is a confound between **enforcement-arm choices** (prompt-only vs. retry vs. binary) at fixed constraint content — a mechanism-choice problem, not a content-vs-length one."
- `sp_instruction_load_confound.technical_challenge` sharpened to end with: "...this is a confound between **content and raw length within any single arm** — orthogonal to which enforcement arm is used, and unresolved even if mechanism attribution (above) is solved perfectly, since a fixed arm could still be reacting to length alone."
- `changes_made`: made the arm-choice-vs-content-length distinction explicit in both technical_challenge fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (6 sub-problems; 2 sourced from related-work limitations, 4 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_bindingness_kappa_catalog`** → targets `sp_operationalization_validity`. *proposed_approach:* Build a ~20-rule deterministic catalog (import-layering/dependency-direction contracts, complexity/length ceilings, naming/visibility conventions, forbidden-API lists, dependency-injection mandates), each a static-analysis check; audit checker verdicts against 2 human annotators' "genuine violation vs. checker artifact" judgment on a 100-sample stratified subset, dropping any rule with Cohen's κ < 0.8; separately screen for bindingness, replacing any rule violated by <5% of unconstrained (L0) generations. *key_insight:* fidelity to design intent can't be proven analytically, but it can be bounded empirically by requiring the checker's verdicts to agree with independent human judgment above a pre-registered threshold — turning an otherwise unverifiable "is this really design intent" question into a verifiable inter-rater-agreement one. *hypotheses:* ["No more than 40% of the initial ~20-rule catalog will be dropped for κ < 0.8 or replaced for failing the bindingness screen, and — among whatever is dropped — drops will concentrate in rules targeting architectural/cohesion judgment calls rather than mechanical categories (naming, complexity thresholds), consistent with the harder-to-checkify categories being where fidelity risk actually lives rather than drops being randomly distributed across rule types."]
- **`m_matched_condition_power_model`** → targets `sp_signal_variance`. *proposed_approach:* Run 750 attempts per (level, model, arm) cell in the pilot (150 tasks × 5 samples); fit a mixed-effects logistic regression of per-attempt pass on strength level with a task-level random intercept; trend-test via Cochran–Armitage across levels, α = 0.05, Holm-corrected across models/arms; run a post-pilot power check before committing scale-up budget. *key_insight:* modeling task-level variance explicitly — rather than treating attempts as independent or eyeballing aggregate pass rates — is what lets a genuine strength-driven trend survive individual tasks/samples behaving noisily, and checking power *before* scale-up (not after) prevents an underpowered null result from being reported as "graceful degradation." *hypotheses:* ["From L0 to L4 (pilot ladder, prompt-only arm), Pass@1(L4) ≤ Pass@1(L0) − 5 percentage points with mixed-effects strength coefficient OR < 0.90 per step (Holm-adjusted p < 0.05) AND cost-per-compliant-solved-task CCS(L4) ≥ 1.25 × CCS(L0), holding for ≥ 2 of 3 scale-up models.", "If the pilot's observed effect size corresponds to less than 80% power for the 5pp pass-rate margin, the scale-up sample size per cell is pre-committed to increase according to the observed variance, rather than the pilot's null result being reported as evidence that compliance is 'approximately free.'"]
- **`m_dual_criterion_breakpoint`** → targets `sp_shape_detectability`. *proposed_approach:* Fit both linear and segmented (piecewise-linear) regressions of pass rate and log-cost against strength, per model × arm; declare a knee only if the Davies test rejects linearity (p < 0.05) AND ΔAIC (linear − segmented) > 4 jointly favor the segmented fit; report knee location + 95% bootstrap CI (1,000 task-level resamples); compare the pass-rate-based and cost-based verdicts for agreement. *key_insight:* a single criterion can be tricked either by noise (Davies alone) or by overfitting model flexibility (AIC alone); requiring both to agree is exactly the dual-criterion design that prevents either failure mode from manufacturing a false-positive or false-negative knee — and running the identical dual-criterion procedure once on the pass-rate curve and once on the cost curve is what makes the cross-axis agreement check (Stage 1's `shape-discordant` outcome) a natural byproduct of the same instrument, not a second one. *hypotheses:* ["Under the checker-in-the-loop retry arm, a knee (both Davies p < 0.05 and ΔAIC > 4) exists for at least 2 of 3 scale-up models.", "The pass-rate-based and cost-based dual-criterion verdicts will agree (both graceful or both knee) for at least 2 of 3 models; where they disagree, the cell is reported as shape-discordant rather than one axis being treated as authoritative."]
- **`m_factorial_grid`** → targets `sp_strength_dimensionality`. *proposed_approach:* Pilot uses the ordinal ladder L0–L4 (cumulative rule packs, breadth and strictness confounded); scale-up replaces it with a 3(breadth) × 3(strictness) factorial grid, reading off each axis's main effect and their interaction from the mixed-effects model. *key_insight:* an ordinal ladder can detect *that* something degrades, but only a factorial design can attribute *how much* of the degradation is breadth versus strictness — the factorial structure is the only way to answer a genuinely two-dimensional question with a two-dimensional design, rather than a bigger one-dimensional one. *hypotheses:* ["Breadth's main effect on pass-rate odds ratio (per level) will exceed strictness's main effect in magnitude at matched ladder position — i.e., adding more distinct rules costs more pass rate than tightening thresholds on already-active rules — in at least 2 of 3 models."]
- **`m_arm_interaction_decomposition`** → targets `sp_mechanism_attribution`. *proposed_approach:* Run identical constraint grids under all three enforcement arms with disaggregated cost logging (prompt-overhead tokens, retry tokens, output-inflation tokens); fit a two-way (arm × strength) mixed-effects model on pass and on log-cost; compute mechanism share MS(σ) = [CCS_retry(σ) − CCS_prompt(σ)] / [CCS_retry(σ) − CCS(L0)]. *key_insight:* the same constraint content produces a different cost profile depending purely on how it's enforced, so holding content fixed while varying only the enforcement arm is the only way to assign cost to "mechanism" rather than "constraints" — the arm × strength interaction term is a formal test of exactly this, not just a descriptive comparison. *hypotheses:* ["The retry-arm log-cost slope will exceed 1.5× the prompt-only log-cost slope at the top strength tier (super-proportional retry cost), and the arm × strength interaction term will be significant (Holm-adjusted p < 0.05) with mechanism share MS ≥ 0.30 at that tier, in at least 2 of 3 models."]
- **`m_length_matched_placebo`** → targets `sp_instruction_load_confound`. *proposed_approach:* Add a fourth, length-matched placebo-prompt control at each strength level — semantically inert instructions token-count-matched (same position, same formatting) to the rendered rule set — and require the strength effect on pass in the real constraint arm to exceed the placebo arm's effect by a pre-specified margin before attributing any drop to constraint content. *key_insight:* the only way to separate "the model is worse at coding when given more instructions" from "the model is worse at coding specifically because those instructions are design constraints" is to hold instruction load constant while emptying its content — varying exactly one factor while fixing the other. *hypotheses:* ["The constraint arm's strength effect on pass exceeds the length-matched placebo arm's strength effect by at least 3 percentage points at maximum strength (Holm-adjusted interaction test, p < 0.05); if this margin is not met, the observed frontier is re-scoped as an instruction-load effect, not a design-constraint-specific one."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold — but two methods each carry two hypotheses, and only one of them justifies why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_matched_condition_power_model.hypotheses", anti_pattern: null, comment: "Two hypotheses here (the headline pass-rate/cost magnitude claim, and the power-precommitment claim) are doing different jobs — one is the paper's central empirical finding, the other is an instrument-validity safeguard against reporting an underpowered null as a real result. Worth stating explicitly why one fitted model produces both readouts, matching the justification already given for `m_dual_criterion_breakpoint`."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_matched_condition_power_model.key_insight` extended: "...the same mixed-effects fit that estimates the strength coefficient (testing the headline magnitude hypothesis) also yields the residual variance needed for a post-hoc power calculation (testing the precommitment hypothesis) — one fitted model, two readouts, exactly the same one-instrument-two-estimands structure already used for the dual-criterion breakpoint test above, not two separately motivated mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly, for consistency with the already-justified `m_dual_criterion_breakpoint`.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **8 hypotheses total** (1 + 2 + 2 + 1 + 1 + 1 across the six methods respectively — `m_matched_condition_power_model` and `m_dual_criterion_breakpoint` each carry two, per the refiner's one-instrument-two-estimands justification above), mixing instrument-validity claims with the study's headline empirical predictions — a deliberate design choice for an `empirical` study_type, explained in the Stage 6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type = empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure/agent beats baseline X" framing. Baselines below are sanity-check comparators and confound controls only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- BigCodeBench-Hard (~150 function-level tasks, executable unit tests) — *justification:* cheap, high-n pilot substrate; used to establish the pilot ladder's pass-rate/cost trend (`rq_pilot_tradeoff_magnitude`) before committing scale-up budget.
- (draft initially listed) SWE-bench Verified (50-task repository-level subset) — *justification:* "digest mentions it as the scale-up realism suite," flagged below.

`baselines` (sanity-check comparators and confound controls, not outcome-tier competitors):
- L0 / unconstrained arm — necessary control anchoring the utility ceiling and the bindingness/B0 gate.
- Binary all-or-nothing enforcement — the naive deployment policy the graded sweep is compared against, to show the graded design adds information a single all-on run wouldn't.
- Length-matched placebo prompt (`m_length_matched_placebo`) — isolates instruction-load from constraint-content effects.
- External anchor: FollowBench's / RECAST's satisfaction-only degradation curves, compared qualitatively (their axes lack pass-rate/cost, per `lim_ifeval_followbench_no_utility_axis` / `lim_recast_autoif_construct_narrow`).

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_catalog_fidelity` | `sp_operationalization_validity` | "No more than 40% of the initial ~20-rule catalog will be dropped for κ < 0.8 or replaced for failing the bindingness screen, and — among whatever is dropped — drops will concentrate in rules targeting architectural/cohesion judgment calls rather than mechanical categories (naming, complexity thresholds), consistent with the harder-to-checkify categories being where fidelity risk actually lives rather than drops being randomly distributed across rule types." |
| `rq_pilot_tradeoff_magnitude` | `sp_signal_variance` | "From L0 to L4 (pilot ladder, prompt-only arm), Pass@1(L4) ≤ Pass@1(L0) − 5 percentage points with mixed-effects strength coefficient OR < 0.90 per step (Holm-adjusted p < 0.05) AND cost-per-compliant-solved-task CCS(L4) ≥ 1.25 × CCS(L0), holding for ≥ 2 of 3 scale-up models." |
| `rq_power_precommitment` | `sp_signal_variance` | "If the pilot's observed effect size corresponds to less than 80% power for the 5pp pass-rate margin, the scale-up sample size per cell is pre-committed to increase according to the observed variance, rather than the pilot's null result being reported as evidence that compliance is 'approximately free.'" |
| `rq_knee_existence` | `sp_shape_detectability` | "Under the checker-in-the-loop retry arm, a knee (both Davies p < 0.05 and ΔAIC > 4) exists for at least 2 of 3 scale-up models." |
| `rq_cross_axis_shape_agreement` | `sp_shape_detectability` | "The pass-rate-based and cost-based dual-criterion verdicts will agree (both graceful or both knee) for at least 2 of 3 models; where they disagree, the cell is reported as shape-discordant rather than one axis being treated as authoritative." |
| `rq_breadth_vs_strictness` | `sp_strength_dimensionality` | "Breadth's main effect on pass-rate odds ratio (per level) will exceed strictness's main effect in magnitude at matched ladder position — i.e., adding more distinct rules costs more pass rate than tightening thresholds on already-active rules — in at least 2 of 3 models." |
| `rq_mechanism_share` | `sp_mechanism_attribution` | "The retry-arm log-cost slope will exceed 1.5× the prompt-only log-cost slope at the top strength tier (super-proportional retry cost), and the arm × strength interaction term will be significant (Holm-adjusted p < 0.05) with mechanism share MS ≥ 0.30 at that tier, in at least 2 of 3 models." |
| `rq_instruction_load_control` | `sp_instruction_load_confound` | "The constraint arm's strength effect on pass exceeds the length-matched placebo arm's strength effect by at least 3 percentage points at maximum strength (Holm-adjusted interaction test, p < 0.05); if this margin is not met, the observed frontier is re-scoped as an instruction-load effect, not a design-constraint-specific one." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing paper.md's already-designed E1–E4 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but the SWE-bench Verified dataset justification is a provenance note, not a reason tied to what it actually stresses.
- comments:
  - `{severity: major, field: "datasets[SWE-bench Verified]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'realism suite' doesn't say which RQ needs it or why BigCodeBench-Hard alone can't answer it. In fact there's a sharper, necessary reason: several catalog rules (import-layering, dependency-direction, dependency-injection mandates) are repository/multi-file constraints that literally cannot be violated on BigCodeBench-Hard's function-level tasks — there's no package structure for a layering rule to bind against. Without SWE-bench Verified, the bindingness screen in `rq_catalog_fidelity` would only ever be able to screen the mechanical, single-file rule subset, silently exempting the architectural rule subset from ever being tested for bindingness at all."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "SWE-bench Verified (50-task repository-level subset, per-repo applicable-rule mapping) — *justification:* required, not merely realistic, for `rq_catalog_fidelity`'s bindingness screen to apply to the catalog's repository-level rules at all (import-layering, dependency-direction, dependency-injection mandates have no multi-file structure to bind against on function-level BigCodeBench-Hard tasks); also lets `rq_breadth_vs_strictness` and `rq_mechanism_share` be tested for generalization beyond function-level scope."
- `changes_made`: gave SWE-bench Verified's inclusion a hypothesis-linked, structurally necessary reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no specific statistical test or algorithm (the Stage 1 refiner deliberately kept "breakpoint-existence criterion" abstract rather than naming Davies/ΔAIC, which only appear starting at Stage 5's `proposed_approach`).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` / `rw_*` / `lim_*` stable stage-to-stage.
3. **Reference integrity** — `sp_operationalization_validity.source_limitation_ids = ["lim_recast_autoif_construct_narrow"]` ∈ Stage 3 limitations ✓; `sp_mechanism_attribution.source_limitation_ids = ["lim_smc_control_mechanism_cost"]` ∈ Stage 3 ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓ (8 of 8).
4. **Output coverage** — Stage 1's three outputs (attempt records, aggregated per-cell metrics, shape verdict) are each reachable: attempt-level validity via `sp_operationalization_validity` + `sp_signal_variance`, aggregated metrics via `sp_strength_dimensionality` + `sp_mechanism_attribution` + `sp_instruction_load_confound`, shape verdict (incl. the Stage-1-refined shape-discordant outcome) via `sp_shape_detectability` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** as with the B5.5 exemplar, the recurring tension was **not disagreement about facts** — paper.md's own Steps 0/5/6 already settle most factual content — but **scope discipline**: repeatedly checking whether a Stage 5/6 hypothesis was quietly restating one of paper.md's already-finished H1–H4, versus adding something this schema's structure specifically demands that paper.md's own Assumptions section (A1–A7) only gestures at without stating as a standalone falsifiable hypothesis (e.g., the catalog-fidelity drop-concentration claim, and the cross-axis shape-agreement check, both of which paper.md's A1/A4 assumptions imply but never state as testable claims in their own right). One deliberate scope decision, made explicitly rather than silently: the compliance-ceiling rider (paper.md's Claim 5 / H4 — residual violation never reaching zero at affordable strength) was **not** promoted to its own sub-problem/method here, since paper.md itself describes it as "attached to E2/E3 data... no new runs" — a descriptive rider on the shape-detectability instrument's own output, not a distinct decisive component the six-stage schema needs a dedicated slot for. It is carried forward into the assembled Experiments section as part of `rq_knee_existence`'s reported metrics, not invented as a seventh sub-problem.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

> Scope: a revision pass over the review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists), checking every finding against the current deliverables and folding in whatever was still open. Historical rounds above are untouched.

**Findings already applied (verified in current deliverables, no change needed):**

1. `stage_review.md` Stage 2 REVISE (related-work coverage gap: architecture-conformance-checking literature) → verified present as the honestly-marked `[citation needed]` "note on coverage" paragraph in `paper_draft.md` Related Work (mirrored in `paper_draft.tex`) and named again in the Conclusion's limitations.
2. `stage_review.md` Stage 3 REVISE (ill-conditioned mechanism-share ratio) → verified present as the pre-specified-floor guard + **mechanism-share undefined** convention in `paper_draft.md` (Cross-Arm Cost Decomposition, RQ7) and `experiment_design.md` RQ7.
3. `stage_review.md` Stage 4 REVISE (missing contamination/leakage check) → verified present as the release-date-vs-training-cutoff stratification + pooled-vs-excluded shape-verdict comparison in `paper_draft.md` Experimental Setup and `experiment_design.md` Datasets.
4. `stage_review.md` Stage 5 REVISE (four-message Introduction paragraph) → verified: the nearest-neighbor paragraph and the "Several other adjacent lines of work…" survey paragraph are split, with the explicit topic sentence in place.
5. `stage_review.md` Phase A item 2 (reference-cache integrity) → verified: `reference_candidates.jsonl` holds 160 records, 20 `selected`, no `pending`, including all 10 digest-N3 citation keys.
6. `stage_review.md` Phase A items 5–6 as they target `paper.md` → verified in `paper.md`: Estimand paragraph (Step 5), H2 slope-ratio effect floor + graceful-with-inflection rule, H2c/F2c + shape-discordant Step 5 row, PG-1…PG-6 gate ids with *Consequence:* clauses, A1's full 5-step R2 detection, A6's INCONCLUSIVE rule.

**Findings that were still open — applied this round:**

7. `stage_review.md` Phase A item 5/6 propagation gap (cross-deliverable consistency): `paper.md`'s H2 slope-ratio effect floor (post-breakpoint slope ≥ 2× pre-breakpoint slope, else graceful-with-inflection) and A6's INCONCLUSIVE rule existed only in `paper.md`, not in the deliverables that operationalize them. → Effect floor added to `paper_draft.md` (Dual-Criterion Shape Test method; RQ4 Setup and Falsification condition) and `experiment_design.md` (RQ4 Statistical test + Expected outcome; RQ5 Statistical test, per H2c's identical dual-criterion-plus-slope-floor procedure). INCONCLUSIVE rule added to `paper_draft.md` (Task-Level Trend Model method; RQ3 Expected outcome) and `experiment_design.md` (RQ3 Expected outcome, citing A6/PG-5). Target hypotheses in `experiment_design.md` left byte-identical (the floor is stated in the test/setup fields, not by rewording any verbatim hypothesis). Mirrored into `paper_draft.tex`.
8. `taste_audit.md` §6 residual-risk recommendation ("worth the paper draft stating plainly which framing is primary") → one sentence added to `paper_draft.md` Introduction immediately after the contributions list, naming the shape verdict as the primary framing and the catalog/harness/suites as the secondary resource contribution and pre-committed fallback headline (F-G1). Mirrored into `paper_draft.tex`.
9. `stage_review.md` Phase A item 1 minor note (digest formatting: N5/N6/N7/N12 lacked the explicit `**Status:**` line the other nodes carry; reviewer left it "for a future digest revision") → applied in `../digest.md`: `**Status:** FOUND (…)` lines added to N5, N6, N7, N12 in N4's established FOUND-with-qualifier style, which keeps the digest's own V-02 self-verification list (non-FOUND = N0–N3, N8–N11) exactly true and invents no new epistemic claims.

**Rejected as moot:** none — every enumerated review finding was either already applied or applied this round.

**Recompile:** `latexmk -pdf` on `paper_draft.tex` succeeded (14 pages); `paper_draft.pdf` regenerated.

**Cross-deliverable consistency after this round:** 8 RQs in both `paper_draft.md` and `experiment_design.md`; margins aligned across both and `paper.md` (5pp pass-rate drop, CCS ≥ 1.25×, 3pp placebo margin, MS ≥ 0.30, 1.5× log-cost slope ratio, ≥2× knee slope-ratio effect floor, κ ≥ 0.8, 5% bindingness screen, 80% power / INCONCLUSIVE rule).
