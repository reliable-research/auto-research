# Discussion Trace — B1.5 (Stage 1–6 critic/refiner record)

> Extracted verbatim from `pipeline.md` (previously inline there under the same headings). This is the complete round-by-round record of the `auto-research-discussion` six-stage run: every draft, every critique (comments + severities + resolution), every decision, every refiner pass, and the final cross-stage consistency check. It is the audit trail behind the confirmed stage outputs that fed `../paper.md` and `paper_draft.md`/`.tex`/`.pdf`. For the standalone, execution-ready Stage 6 spec, see `experiment_design.md`. For goal.md phase-gate tracking (Phase A–I), see `pipeline.md`.

# Auto-Research-Discussion Run — B1.5 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B1.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already runs its own asymmetry/taste self-check at Step 0/3), so genuine disagreement surfaced but never required re-proposing from scratch.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing combinatorial-test-design thread in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Given a fixed per-episode verification-call budget and three structurally distinct check flavors (uniform random spot-check, targeted invariance probe, hidden combinatorial test), determine which allocation policy minimizes the rate of undetected shortcuts taken by a pass-rate-optimizing coding agent.
- **Apparent inputs:** a fixed verification-call budget `B`; an attack-policy suite that implants shortcuts of known ground truth while passing the visible test set; a verification-flavor library with a common per-call cost meter; a coding-task suite with reference solutions.
- **Apparent outputs:** a per-(policy, budget) miss rate; the resulting miss-rate-vs-cost frontier over pure and mixed allocations; the identified best allocation at matched budget; its sensitivity to whether the agent can observe or infer the verifier's allocation policy.
- **Closest research areas:** AI-control-style budgeted oversight protocols (AIControl, ControlTax); reward-hacking / proxy-optimization mitigation (Inference-Time Reward Hacking, Correlated Proxies); classical inspection-game theory (Avenhaus et al.); adversarial test-suite generation (UTRL).
- **In scope:** comparing verification-allocation strategies against *implanted* shortcuts (known ground truth by construction) in coding tasks, under both allocation-blind and allocation-aware attackers. **Out of scope:** detecting *naturally emergent* shortcuts at scale (no affordable ground-truth oracle for those — digest N5/C4, threat t1); non-coding agent domains (web/tool-use/long-horizon SWE — threat t3); training new verifiers or optimizers.
- **Confidence: high.** As with a mature autoclaude seed, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that is already internally cross-referenced (N-node ↔ M-component ↔ RQ/H ids) and already carries its own asymmetry/bridge/synthesis self-audit (`paper.md` Step 0 and Step 3). Reconstruction risk is low; the risk instead is *redundancy* with `paper.md`'s own Steps 5/6/9 — stage 5/6 below are framed as validating the **measurement instrument's properties** (does the cost meter hold up, does the ground-truth substitution hold up, does the mixed-strategy story survive an adaptive attacker), not re-deriving `paper.md`'s hypotheses from a blank page.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed per-episode verification-call budget `B` and a pass-rate-optimizing coding agent that can implant shortcuts of known ground truth, determine which policy for allocating `B` calls across three structurally distinct check flavors — uniform random spot-checks, targeted invariance probes, and hidden combinatorial tests — minimizes the rate of undetected shortcuts, reported as a miss-rate-vs-cost frontier, under both allocation-blind and allocation-aware agent conditions.
- `input`: (1) a fixed budget `B` per episode; (2) an attack policy that optimizes apparent (visible-test) pass rate via implanted shortcuts with a known ground-truth label and machine-checkable witness; (3) a verification-flavor library (a held-out spot-check pool, an invariance-probe generator, a hidden combinatorial-test generator) metered under one common per-call cost rule; (4) a coding-task suite with reference solutions enabling ground-truth adjudication.
- `output`: (1) a per-(policy, budget) miss rate; (2) the miss-rate-vs-cost frontier for pure and mixed allocation policies; (3) the identified best allocation at each swept budget; (4) the sensitivity of that best allocation to whether the agent can observe or infer the verifier's allocation policy.
- `constraints`: ground truth (genuine vs. shortcut) must be independently determinable for every episode without spending the budget under study; every check must be cost-commensurable (one call = one execution + one comparison, held fixed across flavors); the agent's optimization pressure is held fixed while only the verifier's allocation varies.
- `objective`: An allocation-policy comparison is correct if it reports the ordering of policies' miss rates at matched budget, verified via task-clustered statistical tests, separately for the allocation-blind and allocation-aware conditions.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 settles this directly ("the seed's core question... and minimal experiment... both define the deliverable as a *comparative measurement* of existing verification-strategy types under adversarial pressure"), and `paper.md` Step 2 independently arrives at the same classification.

**critique:**
- summary: Strong, evidence-traceable draft — but the objective has a real evaluability gap around what "cost" means, and the summary quietly presupposes a single winner exists.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective says comparisons are decided 'at matched budget' but never states which cost meter that match is under. Digest N6/M2 defines cost as call count (1 call = 1 execution + 1 comparison), but paper.md's own Assumption A3 flags that this meter may not be fair across flavors in wall-clock/token terms, and pre-commits to re-indexing the frontier by wall-clock cost if the ratio exceeds 3x. An objective that doesn't name this contingency as first-class is not fully evaluable as written — a reader can't tell what the paper would report if the two cost meters disagreed."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'which policy... minimizes the rate' presupposes a single scalar winner, but digest N5/C2 states the three flavors have structurally incomparable detection profiles across attack families — so a pooled-only answer could obscure that different flavors dominate for different shortcut classes. Prefer phrasing that keeps per-attack-family reporting explicit rather than implying one number settles it."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest — no new content invented).

### Refiner pass

- `objective` (refined): "A comparison is accepted under the call-count cost meter (one call = one execution + one comparison) as the primary axis; if the realized per-call wall-clock/token cost ratio between any two flavors exceeds a pre-specified fairness bound, the frontier is re-indexed by wall-clock cost as the primary axis instead of resolved under call-count alone — this contingency is part of the objective, not an afterthought."
- `summary` (refined): "...determine which policy... minimizes the rate of undetected shortcuts — reported both pooled and broken out per attack family — as a miss-rate-vs-cost frontier..." (removes the single-scalar-winner presupposition).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation rather than inventing new symbols): "Task τ with reference r_τ; agent submits program s. Episode e=(τ,s,y_e,w_e), y_e∈{genuine,shortcut}, witness w_e known by construction. Flavors F={R,P,H}; allocation π∈Δ² (the flavor simplex) at budget B, integer-rounded; one call = one execution + one comparison. MR(π,B) = missed shortcut-episodes / shortcut-episodes. Determine argmin_π MR(π,B) (and the Pareto set over π) for each B∈{1,2,4,8,16}, under allocation-blind and allocation-aware attack conditions."
- `changes_made`: tightened the objective's cost-meter contingency; removed the summary's single-winner presupposition; added a formal_summary reusing paper.md's own notation.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Automated verifiers that gate agent code before it is merged, rewarded, or deployed operate under a fixed, small budget of verification calls; how that budget is *composed* across qualitatively different check flavors — not just its raw size — may be the dominant lever once exhaustive checking is off the table, and no existing work has directly compared these flavors under matched-budget adversarial pressure.
- `why_it_matters`: As LLM agents are delegated code-writing tasks gated by automated verifiers before their outputs are trusted, rewarded, or merged, exhaustive testing is not economically feasible, so real oversight pipelines already assume only a small fraction of outputs can be audited (AI-control protocols budget a "limited trusted labor" pool by design). If that limited budget is spent naively, a pass-rate-optimizing agent can concentrate shortcuts precisely where the budget does not reach. Existing quantitative treatments of this problem model the scarce verification resource as a single, homogeneous channel — an LM-monitor suspicion score plus an audit threshold — so they can quantify how *audit-budget size* trades off against safety, but structurally cannot ask whether *how the budget is composed* across qualitatively different check types (a random sample, a targeted invariance check, a hidden combinatorial test) changes the answer. Since practitioners must decide today how to split a fixed, non-negotiable inspection budget across check types in a CI or code-review pipeline, an answer to the composition question is directly actionable, not a theoretical curiosity.
- `who_cares`: Verifier/oversight-protocol designers deciding how to spend a fixed per-episode check budget; AI-control researchers whose current models treat oversight as a single monitoring channel; practitioners running code-agent pipelines gated by unit tests and hidden tests who must decide today how to split a fixed CI/audit budget across check types.
- `evidence`: `[ControlTax, OpenReview:BpyR6Wkl1c]`'s own motivation states that "practitioners lack a principled method to determine how monitoring accuracy, auditing budgets, and operational costs jointly determine the probability that a malicious action succeeds" — direct evidence that the *composition* question (not just the budget-size question) is unaddressed by the closest prior quantitative model. `[InfTimeRewardHacking, OpenReview:hSX7Dd8dxy]` documents that stronger optimization against an imperfect verifier produces a characteristic peak-and-collapse in true reward — evidence the strategic-exploitation failure mode this paper measures is real and already documented, just never from the defender's budget-composition side.

**critique:**
- summary: Real, stake-specific motivation with genuine citations — but coverage of stage 1's fourth output is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is the sensitivity of the best allocation to whether the agent can observe/infer the allocation policy — an allocation-blind vs. allocation-aware comparison, not just a one-time flavor ranking. why_it_matters motivates why the composition question matters in general, but never explains why checking robustness to an *allocation-aware* agent specifically matters, as opposed to just picking whichever flavor wins once and deploying it. A reader could reasonably ask 'why not just find the best flavor and be done' — that question is real and currently unaddressed here."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a one-time comparison of flavors against a naive, allocation-blind agent risks recommending a policy that only looks strong because it has never been probed: a deployed verifier is not a one-shot secret. A persistent CI check or code-review policy is reused across many episodes, and a patient attacker who observes enough outcomes can infer which calls are predictable and redistribute shortcuts accordingly — precisely the adaptive pressure that repeated exposure of a trusted-monitoring threshold would eventually create. An allocation recommendation that is never tested against an allocation-aware adversary answers a strictly easier question than the one a real, repeatedly-used verifier actually faces, and could reverse once that adversary is introduced."
- `changes_made`: added the allocation-awareness coverage argument tying directly to stage 1's fourth output.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (full motivation/method text read, per N3's own grounding procedure note). Per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list; the one non-corpus entry (the classical inspection-game survey) is explicitly marked as such, exactly as digest N3 marks it.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_aicontrol` | Anon., AI Control (OpenReview:KviM5k8pcP) | **true** (draft v1) | Routes among audit/defer/shutdown based on one LM-monitor suspicion signal over a whole deployment trajectory; treats the scarce verification resource as a single homogeneous channel, not a decomposable portfolio of check flavors. |
| `rw_controltax` | Anon., Control Tax (OpenReview:BpyR6Wkl1c) | **true** (draft v1) | Converts one monitor's ROC curve plus an audit budget into a compromise probability; the model is tied to one scalar suspiciousness signal and cannot express which *composition* of structurally distinct check types minimizes miss rate at fixed cost. |
| `rw_ctrlaltdeceit` | Anon., CTRL-ALT-DECEIT (OpenReview:XBMjXb6f4w) | false (LM-monitor transcript scoring, no bilateral check-flavor portfolio) | Scores agent transcripts/code with LM-based suspicion monitors under sandbagging/sabotage objectives; measures performance-stealth-detection trade-offs for one monitor design, not a composition of structurally distinct check operations. |
| `rw_calibratedstackelberg` | Anon., Calibrated Stackelberg Games (OpenReview:fHsBNNDroC) | false (abstract payoff-matrix theory, no instantiation) | Characterizes achievable principal utility against a calibrated-forecast-following agent at the level of abstract payoff matrices; gives no instantiation in which "inspection actions" are concrete verification operations, and no empirical miss-rate-vs-cost frontier. |
| `rw_inftimerewardhacking` | Anon., Inference-Time Reward Hacking (OpenReview:hSX7Dd8dxy) | false (modifies the optimizer, not the verifier) | Tunes optimization strength against a fixed, imperfect proxy to avoid a peak-and-collapse in true reward; holds the verifier itself fixed and does not allocate a budget of independent checks. |
| `rw_correlatedproxies` | Anon., Correlated Proxies (OpenReview:msEr27EejF) | false (regularizes occupancy divergence, not a check allocator) | Prevents hacking by regularizing the optimizer's occupancy divergence from a reference policy; a definition-level account of proxy validity, not a defender-side allocation policy over check flavors. |
| `rw_utrl` | Anon., UTRL (OpenReview:VqjNYF9nbP) | false (training-time test-generator, not an eval-time allocator) | Jointly trains a unit-test generator to discriminate against *sampled* imperfect programs drawn from the coder's natural error distribution, not against a strategic adversary that models the verifier and concentrates shortcuts where checks are absent; concerns training-time test generation, not an evaluation-time budget split. |
| `rw_inspectiongames` | Avenhaus, von Stengel & Zamir, Inspection Games (Handbook of Game Theory Vol. 3, 2002) — **non-corpus canonical entry, explicitly marked as such** | false (single homogeneous inspection technology) | Solves budget-constrained inspector-inspectee games with one homogeneous inspection technology against human/institutional inspectees; no account of check flavors with heterogeneous detection profiles against an autonomous pass-rate-optimizing agent, and no empirical instantiation in agentic code settings. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but two baseline labels need scrutiny together.
- comments:
  - `{severity: major, field: "specific_related_works[rw_aicontrol, rw_controltax].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Both works' own I/O framing is a long-horizon, whole-deployment audit/defer/shutdown protocol (AI Control) or a threshold-tuned single-signal compromise-probability model (Control Tax) — genuinely different from this paper's per-episode, matched-budget, multi-flavor comparison. Per the stage-3 rubric, an I/O-mismatched work is 'not a baseline — at best a method-side reference.' Marking both a straightforward comparable baseline risks implying this paper compares directly against either paper's own published safety numbers, which it does not — paper.md Step 6 only reproduces the *suspicion-score-triggered auditing protocol* at matched cost, not either paper's reported result."}`
- decision: `move_to_refiner` (a wording-precision fix — the *protocol* is still legitimately reusable as a comparison arm).

### Refiner pass

- `rw_aicontrol.is_potential_baseline` and `rw_controltax.is_potential_baseline` retained as `true`, but the field's note is sharpened: "Not a baseline in the beat-a-number sense — neither paper's own reported safety numbers are compared against. The single-channel **suspicion-score-triggered auditing protocol** they establish (AI Control's audit-threshold routing, Control Tax's ROC-based threshold optimization) is reproduced as one external comparison arm at matched call budget — borrowing the protocol structure, not either paper's published findings."
- `changes_made`: clarified both baselines' role to avoid an implied I/O-mismatched numeric comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is promoted to a stage-6 framing-tier RQ — the closest candidate (does the single-channel model's own threshold-optimization approach get beaten by a portfolio) is not a distinct framing check; it is already covered end-to-end as a mechanism-tier RQ in Stage 6 (the portfolio-vs-single-channel degradation comparison). Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4 — digest explicitly frames these as problem-inherent obstacles that hold for *any* solution attempt, independent of prior methods, `conflation_check: true` in the source; that framing is exactly the `__novel__` sentinel's intended use, so all four are sourced that way rather than forced onto a related-work limitation that doesn't actually fit):

- **`sp_allocation_exploitability`** — *description:* Design an allocation-comparison protocol whose conclusions are not falsified by an agent that infers the verifier's allocation policy and redistributes shortcuts into the resulting blind spot. *why_it_is_a_problem:* A fixed allocation recommendation is only actionable if it doesn't collapse the moment a persistent deployment leaks information about which calls are safe to target — the agent's shortcut distribution is a moving target under partial policy inference, not a fixed one. *technical_challenge:* Any deterministic (or frequently reused) allocation is exploitable in principle once the agent has observed enough outcomes to infer it; ruling this out requires explicitly modeling and testing an allocation-aware attacker, not just a static one. *source_limitation_ids:* `["__novel__"]`.
- **`sp_incomparable_detection_profiles`** — *description:* Compare three check flavors whose detection profiles cover disjoint, non-nested classes of shortcuts (sample-based, invariance-based, combinatorial) on a single axis. *why_it_is_a_problem:* Without a common yardstick, "flavor X is better" is meaningless — each flavor is structurally blind to whole classes of shortcuts the others catch, so the comparison is genuinely multi-objective, not a scalar ranking. *technical_challenge:* No flavor dominates across all shortcut classes; a fair comparison requires a cost-commensurable metering scheme across structurally different check operations before any ranking is even possible. *source_limitation_ids:* `["__novel__"]`.
- **`sp_budget_tradeoff`** — *description:* Characterize how a small, fixed number of verification calls forces an inescapable trade-off between broad coverage and targeted depth. *why_it_is_a_problem:* This trade-off is intrinsic to budget scarcity itself, not an artifact of any particular check design — even a perfect allocation policy cannot escape it, so any claim about "the best allocation" is only meaningful as one point on this trade-off, not a single number. *technical_challenge:* Every call spent on depth is a call not spent on breadth, and the shape of this trade-off (linear, concave, threshold-like) is not knowable in advance — it has to be measured as a swept frontier rather than assumed. *source_limitation_ids:* `["__novel__"]`.
- **`sp_groundtruth_under_budget`** — *description:* Obtain a ground-truth genuine-vs-shortcut label for every episode without spending the very exhaustive-checking budget the study is designed to avoid. *why_it_is_a_problem:* Miss rate is only measurable relative to a correct label, but by construction the budgeted verifier being studied cannot afford the exhaustive check that would produce that label directly. *technical_challenge:* Ground truth must be sourced from entirely outside the budgeted game (e.g., by construction at implantation time) rather than computed by the object of study itself, and this substitution has to be justified rather than assumed transparent for shortcuts an agent might discover unprompted. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all four would jointly deliver stage 1's four outputs), but two sub-problems risk reading as the same underlying issue.
- comments:
  - `{severity: minor, field: "sp_incomparable_detection_profiles / sp_budget_tradeoff", anti_pattern: "overlap", comment: "Both gesture at 'no single flavor/allocation wins everywhere,' which can read as one sub-problem stated twice. They are genuinely distinct — one is about *qualitative* incommensurability across shortcut classes (can flavor X's detections even be compared to flavor Y's at all), the other is about a *quantitative* resource trade-off (how much breadth you give up per unit of depth) — but the descriptions don't make that distinction explicit enough yet."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_incomparable_detection_profiles.technical_challenge` sharpened to end with: "...this is a **commensurability** problem — making structurally different detections comparable on one axis at all — distinct from how much of one you trade for the other."
- `sp_budget_tradeoff.technical_challenge` sharpened to end with: "...this is a **scarcity-allocation** problem distinct from commensurability — even after flavors are made comparable, a fixed budget still forces choosing how much of each to buy, and that trade-off's shape is what must be measured."
- `changes_made`: made the commensurability-vs-scarcity distinction explicit in both technical_challenge fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; all sourced `["__novel__"]`, each with a stated decisive-component justification reused from digest N5's own problem-inherent framing).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_adaptive_redistribution_test`** → targets `sp_allocation_exploitability`. *proposed_approach:* Run every allocation policy under two attack conditions — allocation-blind (the attack policy has no information about π) and allocation-aware (the attack policy conditions on the verifier's past check outcomes and/or a descriptor of π) — and compare each policy's miss-rate degradation (ΔMR) between the two conditions via a policy × condition interaction test; additionally reproduce the single-channel suspicion-score-triggered auditing protocol (Stage 3's sharpened baseline role) as one more policy in the same comparison. *key_insight:* A policy's ranking under a naive, allocation-blind attacker is not informative about deployment robustness unless it is also stress-tested against an attacker that can exploit exactly the predictability a fixed or deterministic allocation creates — mixed-strategy commitment is the standard game-theoretic defense against a best-responding opponent, so if it matters here it should show up as smaller ΔMR specifically for mixed/randomized policies. *hypotheses:* ["The best pure policy's miss-rate degradation (blind→aware) at B=4 exceeds the best mixed/randomized policy's degradation by at least 10 percentage points, via a policy × condition interaction term with task-clustered robust standard errors, p<0.05.", "The single-channel suspicion-score-triggered auditing baseline, reproduced at matched call budget, degrades from blind to aware by at least 10 percentage points more than the best flavor-portfolio policy, by the same interaction test, Holm-corrected jointly with the first hypothesis."]
- **`m_cost_commensurable_scoring`** → targets `sp_incomparable_detection_profiles`. *proposed_approach:* Meter every check flavor identically (one call = one sandboxed execution + one output comparison) and evaluate all three flavors against the same pool of implanted-shortcut episodes spanning three structurally distinct attack families (hard-coded special-casing, input-conditional backdoors, invariance-breaking implementations), producing one miss-rate number per (flavor, budget, attack-family) cell. *key_insight:* Detection profiles become comparable not by assuming a common currency but by constructing one: an identical cost meter plus a shared episode pool turns "flavor X is qualitatively different from flavor Y" into "flavor X and Y produce different numbers on the same axis," without pretending the flavors are otherwise interchangeable. *hypotheses:* ["At matched budget B∈{4,8}, both invariance probes and hidden combinatorial tests achieve a miss rate at least 10 percentage points lower than uniform random spot-checking against allocation-blind attacks, each contrast significant at p<0.05 (Holm-corrected) with task-level bootstrap 95% CI excluding 0."]
- **`m_simplex_frontier_sweep`** → targets `sp_budget_tradeoff`. *proposed_approach:* Parameterize an allocation policy as a point on the three-flavor simplex, sweep budget B over {1,2,4,8,16} and allocation over a 10%-grid of the simplex (plus the three pure vertices and an adaptive Thompson-sampling-style re-weighting policy), and report the resulting miss-rate-vs-budget curve and its trapezoidal AUC for every swept point. *key_insight:* The coverage-vs-depth trade-off is inherent to budget scarcity, so instead of assuming any single allocation is "correct," the trade-off can be turned into a measured Pareto frontier over the simplex — letting the data show whether an interior mixture buys anything over committing to one flavor, rather than asserting it does. *hypotheses:* ["Some evaluated mixed policy (an interior grid point or the adaptive policy) achieves a frontier AUC at least 0.05 lower (approximately 5 percentage points of mean miss rate over the swept budgets) than every pure vertex's AUC, with task-level bootstrap 95% CI on each mixture-vs-vertex difference excluding 0."]
- **`m_construction_oracle_with_novelty_control`** → targets `sp_groundtruth_under_budget`. *proposed_approach:* Implant shortcuts by construction (three attack families, each producing a machine-checkable witness — a trigger predicate or a violated invariance — known at generation time) so every episode carries ground truth without requiring the budgeted verifier itself to produce it; additionally run an "unstructured-novelty" control arm that draws checks from the same held-out input universes the targeted flavors use, but with the targeting logic (semantics-preserving transforms, covering-array structure) ablated, to isolate whether any targeted-flavor advantage comes from structure or merely from novelty relative to the visible tests. *key_insight:* Constructing ground truth by design only buys validity if the construction itself isn't silently doing the explanatory work — the novelty-ablated control is what lets "targeted flavors win" be attributed to their structure rather than to the trivial fact that they are held out at all. *hypotheses:* ["The targeted flavors' miss-rate advantage over uniform random spot-checking shrinks to under 5 percentage points and becomes statistically indistinguishable from zero (bootstrap CI including 0) when checks are drawn from the same held-out input universe with targeting structure ablated, at B=4."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but one method is carrying two headline claims and needs a one-line justification for why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_adaptive_redistribution_test.hypotheses", anti_pattern: null, comment: "Two hypotheses here (the mixed-vs-pure degradation gap, and the portfolio-vs-single-channel-baseline degradation gap) are two of the paper's most central claims, bundled into one method. Worth stating explicitly why one design produces both, so this doesn't read as scope creep folded into a single method entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_adaptive_redistribution_test.key_insight` extended: "...a single paired blind-vs-aware design produces two separately falsifiable readouts from one comparison: which policy (pure or mixed) degrades least under the interaction test (the first hypothesis) and whether the single-channel baseline specifically fares worse than the best portfolio (the second) — one instrument (the blind/aware interaction protocol), two readouts, not two mechanisms; the second hypothesis is Holm-corrected jointly with the first specifically because it reuses the same interaction test rather than introducing a separate one."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **5 hypotheses total** (2 + 1 + 1 + 1 across the four methods respectively — `m_adaptive_redistribution_test` carries two, per the refiner's one-instrument-two-readouts justification above), mixing instrument-validity claims (the novelty-ablation control) with the study's headline empirical predictions — a deliberate design choice for an `empirical` study_type, matching `paper.md`'s own five pre-registered hypotheses (H1, H2, H3, H3b, and the B-alt novelty control) almost verbatim, since the seed material had already worked out this exact hypothesis set.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 5 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check/comparator arms only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- APPS (competition-level programming problems) — *justification:* the implanted-backdoor substrate `[ControlTax, OpenReview:BpyR6Wkl1c]` and the AI-control line already use; pilot-stage domain.
- BigCodeBench (function-level tasks with rich argument structure) — *justification (draft v1, flagged below):* "digest mentions it's suited to combinatorial input generation."
- EvalPlus-extended HumanEval+/MBPP+ — *justification:* source of large held-out I/O pools needed for the random-spot-check flavor and the unstructured-novelty control arm.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Pure random-spot-check / invariance-probe / hidden-combinatorial-test vertices — the three necessary reference points every mixture is compared against.
- Single-channel suspicion-score-triggered auditing (reproducing the AI Control / Control Tax protocol at matched call budget, per Stage 3's sharpened baseline role) — the closest external comparator.
- No-verification floor (B=0, MR≡1 by construction) and visible-test-replay floor (all B calls re-executing draws from the visible test set, expected MR≈1) — sanity anchors, not competitors.
- Unstructured-novelty control (targeting logic ablated from the targeted flavors) — isolates structure from mere held-out novelty.

`research_questions` (5, all mechanism-tier — **draft v1 mislabels one as outcome-tier, flagged below**):

| rq_id | tier (draft v1) | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|---|
| `rq_flavor_advantage` | mechanism | `sp_incomparable_detection_profiles` | "At matched budget B∈{4,8}, both invariance probes and hidden combinatorial tests achieve a miss rate at least 10 percentage points lower than uniform random spot-checking against allocation-blind attacks, each contrast significant at p<0.05 (Holm-corrected) with task-level bootstrap 95% CI excluding 0." |
| `rq_mixture_dominance` | mechanism | `sp_budget_tradeoff` | "Some evaluated mixed policy (an interior grid point or the adaptive policy) achieves a frontier AUC at least 0.05 lower... than every pure vertex's AUC, with task-level bootstrap 95% CI on each mixture-vs-vertex difference excluding 0." |
| `rq_mixed_robustness` | mechanism | `sp_allocation_exploitability` | "The best pure policy's miss-rate degradation (blind→aware) at B=4 exceeds the best mixed/randomized policy's degradation by at least 10 percentage points, via a policy × condition interaction term with task-clustered robust standard errors, p<0.05." |
| `rq_portfolio_beats_baseline` | **outcome (draft v1)** | `sp_allocation_exploitability` | "The single-channel suspicion-score-triggered auditing baseline, reproduced at matched call budget, degrades from blind to aware by at least 10 percentage points more than the best flavor-portfolio policy, by the same interaction test, Holm-corrected jointly with the first hypothesis." |
| `rq_structure_vs_novelty` | mechanism | `sp_groundtruth_under_budget` | "The targeted flavors' miss-rate advantage... shrinks to under 5 percentage points and becomes statistically indistinguishable from zero... when checks are drawn from the same held-out input universe with targeting structure ablated, at B=4." |

**critique:**
- summary: Tier accounting is nearly clean, but one RQ's tier label and framing directly violate the `study_type=empirical` gate, and one dataset justification is a provenance note instead of a methodological reason.
- comments:
  - `{severity: major, field: "research_questions[rq_portfolio_beats_baseline].tier", anti_pattern: "tier_violation", comment: "This RQ is labeled `outcome` and its `rq_id`/description frame it as 'portfolio beats baseline' — exactly the forbidden 'our procedure beats baseline X' shape for a `study_type=empirical` paper (stages.md: 'outcome-tier RQs are forbidden... if one appears, that's a major flag'). The underlying hypothesis is actually about *differential degradation* under an allocation-aware attacker — an attribute of the procedure (how much detection power a portfolio retains vs. a single-channel design under adaptive pressure), not a beats-baseline claim. It must be relabeled mechanism-tier and reworded so the baseline appears as a comparator, not a competitor."}`
  - `{severity: minor, field: "datasets[BigCodeBench]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it's suited to...' is a provenance note, not a reason tied to a specific RQ. It should say which hypothesis needs BigCodeBench's argument-rich structure and why."}`
- decision: `move_to_refiner`.

### Refiner pass

- `rq_portfolio_beats_baseline` renamed `rq_baseline_degradation_comparison`, tier corrected to `mechanism`, `description` reworded: "How does detection-power retention under an allocation-aware agent compare between a flavor-portfolio policy and a single-channel auditing baseline, at matched cost?" — not "does portfolio X beat baseline Y." `target_hypotheses` field unchanged (still the verbatim hypothesis text; only the RQ's own framing/tier were the problem, not the hypothesis itself).
- `datasets` entry replaced: "BigCodeBench (function-level tasks with rich, multi-argument call signatures) — *justification:* `rq_flavor_advantage`'s hidden-combinatorial-test flavor needs tasks with enough independent input parameters for a pairwise (t=2) covering array to be non-trivial; APPS's single-issue I/O style under-stresses this flavor, so BigCodeBench is the scale-up domain that lets the combinatorial-test flavor's advantage (or lack of one) actually be tested rather than assumed."
- `changes_made`: fixed the tier-violation on the fourth RQ (relabel + reframe, hypothesis text untouched); gave BigCodeBench's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6** — 5 mechanism-tier RQs, 0 framing-tier, 0 outcome-tier.

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the cost-meter contingency in Stage 1's objective is a measurement rule, not a method choice; it was already present in the seed's own Assumption A3).
2. **ID stability** — no id renamed mid-run except the one disclosed Stage 6 refiner rename (`rq_portfolio_beats_baseline` → `rq_baseline_degradation_comparison`, logged above, not silent); `sp_*` / `m_*` stable stage-to-stage.
3. **Reference integrity** — all four Stage 4 `source_limitation_ids = ["__novel__"]` (consistent with digest N5's own problem-inherent framing) ✓; every Stage 5 `target_sub_problem_id` ∈ Stage 4 ✓ (one method per sub-problem, 4-for-4) ✓; every Stage 6 `target_hypotheses` is a **verbatim** match to a Stage 5 hypothesis ✓.
4. **Hypothesis-to-RQ recount (verbatim traceability check):** Stage 5 hypothesis count by method: `m_adaptive_redistribution_test`=2, `m_cost_commensurable_scoring`=1, `m_simplex_frontier_sweep`=1, `m_construction_oracle_with_novelty_control`=1 → **5 total**. Stage 6 RQ count: `rq_flavor_advantage`, `rq_mixture_dominance`, `rq_mixed_robustness`, `rq_baseline_degradation_comparison`, `rq_structure_vs_novelty` → **5 total**, each a 1:1 verbatim match to exactly one hypothesis, no duplicates, no orphans. Numbers match.
5. **Output coverage** — Stage 1's four outputs (per-policy miss rate, frontier, best-allocation id, awareness-sensitivity) are each reachable: miss rate/frontier via `sp_incomparable_detection_profiles` + `sp_budget_tradeoff` + `sp_groundtruth_under_budget` (measurability), best-allocation id via the simplex sweep, awareness-sensitivity via `sp_allocation_exploitability` — nothing promised in Stage 1 falls off the chain by Stage 6.
6. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs after the round-1 fix (the one draft-stage tier violation was caught and corrected, not left in).

**What was hardest:** unlike a stage with genuinely missing content, the recurring tension here was **a near-miss tier violation that would have been easy to wave through** — `rq_portfolio_beats_baseline`'s framing was a completely natural way to describe the comparison in plain English ("does the portfolio beat the baseline"), and it took an explicit re-check against the `study_type=empirical` gate (not just the rubric's generic "is this falsifiable" check) to catch that the *framing*, not the underlying hypothesis, was the problem. This is exactly the kind of mistake the tier-accounting recount is designed to catch before it reaches the paper draft.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup to a prior stage was required.

---

## Post-review revision round (2026-07-05)

> Scope: fold every still-OPEN finding from `stage_review.md`, `taste_audit.md`, and `design_review.md` into the three deliverables. Prior state: `design_review.md`'s 15 authorized fixes were already applied to `paper.md`/`digest.md` (2026-07-04), and `experiment_design.md` was assembled from the post-fix `paper.md` (so it already carried the manipulation check, placebo arm, winner's-curse guard, and 5-arm skeleton); the stale items were the draft-side propagation `design_review.md` itself deferred ("regenerating stale paper_draft.md/.tex") plus a few protocol details missing from `experiment_design.md`. A prior attempt at this round was interrupted before writing any of this section; no duplicate work was found, only the gaps below.

**Applied (source → finding → change → file):**

1. `design_review.md` F1 (unvalidated P/H instruments) → instrument-validation protocol propagated: full R2 bullet (soundness 100%, positive-control ≥90%, drop-not-patch, freeze, gate G5) added to `experiment_design.md` common design constants; condensed "Instrument validation" paragraph added to `paper_draft.md`/`.tex` Experimental Setup.
2. `design_review.md` F3 (attack-family-mix duality confound) → pre-registered {10/33/80}% reweighting sensitivity analysis with mix-stability wording: new section in `experiment_design.md`; new "Attack-family-mix sensitivity" paragraph in `paper_draft.md`/`.tex`.
3. `design_review.md` F4(i) (no null-by-construction placebo) → label-permutation placebo arm added to the draft's Baselines paragraph (`paper_draft.md`/`.tex`); already present in `experiment_design.md`.
4. `design_review.md` F4(ii)/A7 (genuine-episode source unspecified) → genuine-pool definition + 100-episode purity audit + 2% impurity consequence added to `experiment_design.md` common constants and the draft's Baselines paragraph (`paper_draft.md`/`.tex`).
5. `design_review.md` F5 (H3 failure ambiguous with weak awareness) → oracle-aware manipulation-check gate added to the draft's RQ3 Setup (`paper_draft.md`/`.tex`); `experiment_design.md` RQ3 falsification wording now explicitly licensed only when the check passes (CR-6 route otherwise).
6. `design_review.md` F6 (incomplete fallback algebra) → RQ1 falsification's "second-order lever" clause conditioned on CR-4 and wrong-direction rule added, in both `experiment_design.md` and `paper_draft.md`/`.tex`; CR-1…CR-7 outcome-combination rules added to `experiment_design.md` (verbatim-condensed from `paper.md`) and as an "Outcome-combination rules" paragraph in `paper_draft.md`/`.tex`; F-G1's INCONCLUSIVE-awareness variant added to `experiment_design.md`'s Global fallback.
7. `design_review.md` F7(i) (H2 winner's-curse) → RQ2 Setup's "single best-performing mixture" primary contrast replaced by the two pre-specified confirmatory candidates (uniform 1/3-mixture, adaptive policy; Holm over 2; grid exploratory) in `experiment_design.md` (leftover stale sentence) and `paper_draft.md`/`.tex`.
8. `design_review.md` F7(ii) (power ignores clustering) → DEFF = 1+(m̄−1)·ICC effective-n clause (ICC from pilot, no value asserted) added to both thin-cell rules (`experiment_design.md`, `paper_draft.md`/`.tex`).
9. `design_review.md` F9 (missing literatures; H3 quasi-known) → new "Metamorphic testing" Related Work thread and a security-games extension (Stackelberg allocation line; concede direction, contribute magnitude) added to `paper_draft.md`/`.tex`, each explicitly disclosing that its cache entry is [UNVERIFIED — requires harvest] and emitting **no citation key** (digest N3 discipline — no invented citations); RQ3 repositioning also added as a concession note in `experiment_design.md` and in the draft's RQ3 plain-language hypothesis.
10. `design_review.md` F10 (R6 double-count) — partial → per-episode coverage-overlap-with-witness-region metric added to `experiment_design.md`'s logged metrics as the distinct mechanism analysis (uses only already-logged data).
11. `design_review.md` F11(iii) (gates not nameable) → PG-A1/PG-A5/PG-A6/PG-A7 named pre-run gates section added to `experiment_design.md`.
12. `design_review.md` item-4/H4 propagation → draft RQ5 Setup now carries the E1-winner restriction, Holm over tested flavors, and the 5 pp effect floor (`paper_draft.md`/`.tex`); already present in `experiment_design.md`.
13. `stage_review.md` resume-pass open to-do #2 (Introduction first-mention citations) → `\citep{AIControl2024}`, `\citep{ControlTax2024}`, `\citep{AvenhausInspectionGames2002}`, `\citep{InfTimeRewardHacking2024}` added at first mention in Introduction paragraph 3 (`paper_draft.tex`; the `.md` mirror carries no citation markers anywhere by its own convention, so its prose is unchanged).

**Rejected / not applicable (with reasons):**

- `design_review.md` F10 derived minimax-π* analysis → deferred, per the reviewer's own disposition ("recommended but optional — requires Phase C data"); the draft-side half of F10 (overselling game framing) is moot — the draft's abstract/contributions already frame the work as measurement, not game theory.
- `design_review.md` F11(ii) budget-grid triple-writing → already satisfied: per-stage grids are frozen explicitly (pilot {1,2,4,8}; scale-up {1,2,4,8,16}) in `experiment_design.md` and the draft's RQ1 Setup; `paper.md`'s "{1,2,4,8(,16)}" denotes exactly that stage split.
- `stage_review.md` to-do #1 / `design_review.md` residual: fetch + digest the 6 remaining backfilled N3 keys → rejected as unactionable here: all are still-anonymous OpenReview submissions or a textbook with no jsonl-resolvable identity; forcing a guess risks misattribution (the 2 baseline-tagged keys were already resolved 2026-07-04).
- `stage_review.md` to-do #3 / Phase B walking skeleton and any results-dependent findings → rejected: no experiment compute in this environment; all gates remain pre-registered and ready.
- `taste_audit.md` → no action items (🟢 PASS in both the original audit and the 2026-07-04 re-audit).

**Cross-deliverable consistency after this round:** 5 RQs in `paper_draft.md` = 5 in `experiment_design.md`, all five target hypotheses byte-identical to the Stage-5 texts (untouched this round); effect floors match (10 pp for RQ1/RQ3/RQ4, 0.05 AUC for RQ2, 5 pp for RQ5); manipulation-check floor (10 pp at B=4) and skeleton signal gates (15 pp raw, G4/G6) consistent with `paper.md`; thin-cell/DEFF wording now identical in substance across both deliverables. `paper_draft.tex` recompiled: exit 0, 15 pages (up from 14), zero LaTeX errors, zero undefined citations.

### Deletion-audit addendum (2026-07-05)

A post-deletion audit recovered the three deleted review files from git HEAD and re-checked every actionable finding against the deliverables and this ledger. All stage-review findings (2 REVISE + Phase A items), all taste-audit items (none — 🟢), and design-review F1–F11 (including sub-parts) plus Missing-RQ items 1–4 and 8 verified as applied or explicitly dispositioned above. Three findings were absent AND undispositioned — `design_review.md` "Missing RQs / reviewer questions" items 5, 6, and 7 — and were applied now:

1. **MRQ-5 (budget×composition stability of the winner)** → pre-registered budget-stability check (RQ1 winner and RQ2 mixture-vs-vertex contrasts recomputed per swept budget, reanalysis-only; recommendation stated budget-unconditionally only if the same policy wins at every B, otherwise per-budget) — new "Budget-stability" section in `experiment_design.md`; new "Budget-stability of the recommendation" paragraph in `paper_draft.md`/`.tex`.
2. **MRQ-6 (ordering across attacker model families)** → per-attacker-backbone breakdown added as a pre-registered heterogeneity check to RQ1's Metrics (pooled ordering claimed model-general only if its direction replicates within every attacker backbone; otherwise reported pooled with per-backbone divergence disclosed) — `experiment_design.md` RQ1 metrics and `paper_draft.md`/`.tex` RQ1 metrics.
3. **MRQ-7 (why t=2 covering arrays)** → t=2 rationale (interaction-fault empirics; combinatorial growth of higher-strength arrays vs. the small swept budgets) plus a pre-registered exploratory t=3 sensitivity check on parameter-rich tasks — `experiment_design.md` common design constants (instrument-validation block) and the draft's "Instrument validation" paragraph (`paper_draft.md`/`.tex`).

Target hypotheses remained byte-identical (no hypothesis statement touched). `paper_draft.tex` recompiled after these edits: latexmk exit 0.
