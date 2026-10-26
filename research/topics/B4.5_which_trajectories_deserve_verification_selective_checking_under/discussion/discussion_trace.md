# Discussion Trace — B4.5 (auto-research-discussion, autoclaude-style, repo-driven from digest.md + paper.md)

> This is the complete round-by-round record of the six-stage critic↔refiner loop: every draft version, every critique (comments + severities + resolution), every decision, every refiner pass, and the final cross-stage consistency check. Moved out of `pipeline.md` (which now carries only a pointer here plus the goal.md Phase Log) per the `auto-research-discussion` skill's "Final deliverables" spec — this file is artifact 3 of 3, alongside `paper_draft.md` and `experiment_design.md`. The confirmed outputs recorded here already fed `paper.md` and `paper_draft.md`/`.tex`/`.pdf`; nothing below was regenerated for this extraction — it is moved verbatim from `pipeline.md`.
>
> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B4.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already runs its own asymmetry/archetype/taste self-audit in Steps 0–3), so genuine disagreement surfaced but never required re-proposing from scratch.
>
> **Full pipeline order (updated):** this trace (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Given a fixed budget of calls to a *trusted* verifier and more sampled candidate trajectories than that budget can cover, determine which trajectories to verify — and how to combine verified with unverified evidence — to maximize accuracy per verifier call.
- **Apparent inputs:** N candidate trajectories per task instance (self-consistency samples, best-of-N candidates, or agent rollouts); per-trajectory verifier-free uncertainty signals computable before any verifier call; a fixed global verifier-call budget B < N × (number of instances).
- **Apparent outputs:** the verified subset (size ≤ B); a final per-instance answer combining verified and unverified evidence; budget–accuracy curves and accuracy-per-verifier-call comparisons against baselines.
- **Closest research areas:** test-time-compute allocation (Compute-Optimal-TTS, CaTS — budgets *generation*, not verification); verifier-imperfection theory (ROC-n-reroll, OT-Verify — assumes the verifier scores *every* candidate, studies verifier noise, not verifier scarcity); selective evaluation / cascade routing (Trust-or-Escalate, TRIM — budgets per-item or per-step, not per-trajectory-across-a-pool).
- **In scope:** measuring how a fixed verifier-call budget should be spent across an already-sampled trajectory pool, when the verifier is trusted (accurate when consulted) and only its call count is scarce. **Out of scope:** verifier *unreliability* itself (that is topic B1.5's mirror-image question); training new samplers or verifiers; fully online/streaming deployments with unknown horizon across future batches.
- **Confidence: high.** As with B5.5, the "repo" here is a prior reverse-digest (`digest.md`, N0–N12) plus a pre-registered spec (`paper.md`, Steps 0–9) that already cross-references its own C1–C4/M1–M5/RQ ids and already ran its own asymmetry/archetype/taste self-audit (paper.md Steps 0/2/3). Reconstruction risk is low. The risk is the same one B5.5 flagged: *redundancy* with paper.md's own Steps 5/6 — so stages 5/6 below are framed as validating the **measurement instrument's properties** (signal validity, aggregation value, transfer robustness), not re-deriving paper.md's H1–H3 from scratch, even though the concrete thresholds below deliberately reuse paper.md's own pre-registered numbers as authored design targets.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a pool of N candidate reasoning trajectories per task instance, sampled by an LLM (parallel chains-of-thought, best-of-N candidates, or agent rollouts), and a global budget B of calls to a verifier that is trusted to score any trajectory it is given correctly, select which ≤B trajectories across the evaluation batch to submit for verification, and combine the resulting verified outcomes with the unverified trajectories' own signals into one final answer per instance, so as to maximize accuracy per verifier call.
- `input`: (1) N trajectories per instance, each with a final answer and enough structure to compute verifier-free signals before any verifier call; (2) a fixed global budget B < N × (#instances); (3) a verifier that returns a correct/incorrect label for any trajectory it is given.
- `output`: (1) the verified subset (size ≤ B); (2) a final predicted answer per instance combining verified and unverified evidence; (3) budget–accuracy curves and accuracy-per-verifier-call readings against baseline allocations.
- `constraints`: the verifier is trusted — the scarce resource is the number of calls, not the verifier's reliability; every trajectory must terminate in a checkable final answer before allocation decisions are made.
- `objective`: an allocation policy is preferred if, at matched budget B, it achieves higher accuracy-per-verifier-call than uniform-random allocation, and it is judged non-vacuous only where full verification actually improves on no verification at all.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 already settles this as a measurement/characterization study (the built components are instruments in service of the measurement, not a new model, dataset, or system being pitted for SOTA).

**critique:**
- summary: A well-evidenced draft, but `constraints` quietly forecloses a distinction the seed material itself treats as load-bearing, and the trace from Stage-1 outputs to what "trusted" means is incomplete.
- comments:
  - `{severity: major, field: "constraints", anti_pattern: "fields_misaligned", comment: "'the verifier is trusted' is stated as a flat given, but paper.md's own Assumption A1 treats trust as something that must be *audited*, not assumed, once the oracle verifier is replaced by a realistic one (execution tests, a PRM) — A1's own failure mode is explicit: 'PRM threshold noisy → trusted premise void, topic collapses into B1.5.' A problem statement that bakes in 'the verifier is trusted' as an unconditional constraint is inconsistent with a paper that spends an entire experimental stage (Stage 2 / E3-H3a) checking whether that premise actually holds for realistic verifiers. The constraint needs to distinguish the oracle tier (trust exact by construction, used to isolate the allocation question) from the realistic tier (trust as an empirically audited precondition with a stated error tolerance)."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "Output (2) says the aggregation 'combines' verified and unverified evidence but doesn't yet signal that a verified-*incorrect* result is itself informative (it eliminates a candidate answer without naming the correct one) — worth flagging now so stage 2's motivation doesn't have to introduce this idea from nothing."}`
- decision: `move_to_refiner` (both flags are formalize-level: the two-tier trust distinction and the elimination-information point are already fully worked out in paper.md's Assumptions/N6-M4 — nothing new needs inventing).

### Refiner pass

- `constraints` (refined): "The verifier is *trusted* in one of two senses, and the problem statement covers both explicitly rather than picking one silently: (a) an **oracle** tier, in which trust is exact by construction (a ground-truth lookup), used to isolate the allocation question from verifier quality; and (b) a **realistic** tier, in which trust is an empirically audited precondition — a verifier (test execution, a process-reward-model score) whose false-positive and false-negative rates against held-out gold labels fall below a pre-stated tolerance — rather than an assumption taken on faith. Every trajectory must also terminate in a checkable final answer before allocation decisions are made."
- `output` (refined, item 2): "...a final predicted answer per instance, combining verified outcomes with unverified signal — critically, a verified-*incorrect* outcome eliminates a candidate answer from contention even though it does not reveal the correct one, so the combination step is a genuine aggregation problem, not a fallback-to-vote formality."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Instances x_1..x_m; per instance a pool T_i={τ_i1..τ_iN} of trajectories with final answers a(τ). Verifier V: τ ↦ {0,1}. Budget B < mN. Policy π selects S ⊆ ∪T_i, |S| ≤ B. Aggregator g maps (T_i, V restricted to S∩T_i, verifier-free signals) ↦ â_i. Objective: maximize (1/m)Σ 1[â_i correct] at fixed B, relative to uniform-random S and to full verification (S = ∪T_i)."
- `changes_made`: split the trust constraint into an oracle/realistic two-tier statement; sharpened the aggregation output to name the elimination property explicitly; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Test-time-scaling pipelines that sample many candidate trajectories per query increasingly pair the sampler with a verifier, but the literature that treats compute as an explicitly metered, allocable resource has only ever metered *generation* — never the calls to the verifier itself, which is often the more expensive step (sandboxed execution, a PRM pass, a strong-judge call).
- `why_it_matters`: Deployed pipelines currently pick one of two extremes — verify every candidate (expensive, sometimes prohibitively so at scale) or verify nothing (errors that all sampled trajectories agree on, wrongly, pass straight through). Compute-allocation work has already normalized treating *generation* as a metered resource: Compute-Optimal-TTS allocates search/revision hyperparameters by estimated difficulty, and CaTS uses calibrated confidence to decide how many samples to draw. Neither extends this accounting to the verifier side — in both, verifier/PRM scoring is bundled into "the strategy" rather than treated as its own scarce resource with its own allocation question, so a pipeline designer currently has no principled way to decide how many verifier calls a deployment needs or where to aim them.
- `who_cares`: Pipeline engineers deciding how many verifier calls (test executions, PRM scores, judge calls) a deployed reasoning system actually needs and where to spend them; researchers building an inference-time-economics account that currently has a generation-budget theory (Compute-Optimal-TTS, CaTS) and a verifier-*imperfection* theory (ROC-n-reroll, OT-Verify) but nothing for verifier-*scarcity* with a verifier that is otherwise trustworthy.
- `evidence`: `[Compute-Optimal-TTS, OpenReview:4FWAwZtd2n]`'s own motivation frames test-time compute as "expensive and increasingly central to deployment," arguing for difficulty-conditioned allocation — of generation-side hyperparameters only. `[CaTS, OpenReview:jrSc4RJXy1]`'s own corpus record states self-consistency "uses a fixed sample count for every query and assigns equal weight to all samples regardless of their likely reliability" — diagnosing exactly the fixed-and-unweighted failure mode on the generation side that has no verifier-side analogue anywhere in the corpus. `[TRIM, OpenReview:MoKrugWUfC]`'s own motivation argues that step-level, threshold-based intervention decisions "are insufficient because PRM scores are noisy and the value of intervention depends on trajectory-level context" — evidence that even token/step-level budgeting work already recognizes a value-of-intervention question, just never at the cross-trajectory, cross-instance grain this topic asks about.

**critique:**
- summary: Strong, citation-backed motivation, but it covers the *selection* half of Stage 1's outputs thoroughly and says almost nothing about why the *aggregation* output matters as its own claim.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1's refined output (2) makes a specific point: a verified-incorrect outcome eliminates a candidate answer without naming the correct one, so combining evidence is a real aggregation problem. `why_it_matters` as drafted only motivates the allocation question (which trajectories to check) and never explains why *how the verified and unverified evidence gets combined* is a claim worth making in its own right. A reader could reasonably ask: why not just report accuracy on the verified subset and ignore the rest? Without an answer, the aggregation output (and CO4 in the digest) reads as bookkeeping rather than a real design axis."}`
- decision: `move_to_refiner` (the fix uses content already present in digest N5/C4 and N6/M4 — no new argument needs to be invented).

### Refiner pass

- `why_it_matters` (extended): "...and this is not only a selection question: a policy that only ever reports accuracy on the verified fraction throws away information the budget already bought. A verified-incorrect trajectory does not reveal the right answer, but it does remove a wrong one from contention — and if that elimination is not exploited, some of the value the budget purchased is simply discarded at the aggregation step, independent of how well the trajectories were chosen for verification in the first place. Getting the allocation exactly right while aggregating naively would still leave real accuracy on the table, which is why aggregation has to be measured as its own design axis rather than assumed to be a formality once selection is solved."
- `changes_made`: added the aggregation-as-distinct-design-axis argument, tied to Stage 1's refined output (2).
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight corpus works plus the one non-corpus canonical citation below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (their own motivation/method text was read, per digest's grounding notice), so no landscape-only entries are padded in here.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_computeopttts` | Anon., Compute-Optimal-TTS (OpenReview:4FWAwZtd2n) | **true** (adapted control arm) | Allocates inference hyperparameters per prompt under a FLOPs budget by estimated difficulty; verifier/PRM scoring is bundled into the chosen strategy, never metered as its own resource — so it answers "how much to generate," not "which already-sampled trajectories to check." |
| `rw_cats` | Anon., CaTS (OpenReview:jrSc4RJXy1) | false (generation-side, no verifier call at all) | Uses calibrated cross-sample-agreement confidence to decide how many samples to draw (early stopping); never invokes an external verifier, so it has no allocation question over verifier calls to answer. |
| `rw_rocnreroll` | Anon., ROC-n-reroll (OpenReview:3Gy5mmyuxn) | false (theoretical anchor, not a runnable comparison arm) | Gives an exact ROC-curve theory of verifier *imperfection* for Best-of-N/Rejection Sampling — but assumes the verifier scores every candidate; the number of verifier calls is never a constraint, only verifier accuracy is the free variable. |
| `rw_otverify` | Anon., OT-Verify (OpenReview:BBDhQJh6GB) | false (theoretical anchor) | Unifies coverage, verifier-ROC accuracy, and algorithm design via optimal transport — same all-candidates-scored assumption as ROC-n-reroll; verifier-call scarcity is outside its object of study. |
| `rw_trustorescalate` | Anon., Trust-or-Escalate (OpenReview:UHPnqSTBPO) | **true** (adapted control arm) | Selective cascaded judge evaluation with calibrated per-item escalation thresholds and provable human-agreement guarantees — but each item is accepted/escalated independently against a fixed threshold, with no shared budget coupling multiple items compete for. |
| `rw_trim` | Anon., TRIM (OpenReview:MoKrugWUfC) | false (nearest neighbor, not a baseline in the beat-a-number sense) | Budgets a costly intervention (strong-model step regeneration) under an explicit strong-model token budget, guided by a noisy per-step PRM risk signal — but the unit of allocation is a reasoning step *inside one trajectory*, not a whole trajectory *across a cross-instance pool*. |
| `rw_safer` | Anon., SAFER (OpenReview:kJmLmOvwLC) | false (no trusted verifier invoked at all) | Calibrates a sampling budget and an uncertainty-filtering threshold entirely offline against admissibility labels; at test time, no external trusted verifier is consulted, so it cannot exploit even a small number of ground-truth-grade checks. |
| `rw_selfcapability` | Anon., Self-Capability (OpenReview:EO6WtJ0q6G) | false (measures the signal's existence, not a policy built on it) | Evaluates whether ex-ante confidence predicts task success and supports accept/decline decisions, reporting substantial miscalibration — but never constructs or evaluates an allocation policy that spends a budget based on such a signal. |
| `rw_wang2023` | Wang et al., 2023 (ICLR, arXiv:2203.11171) | **true** (lower-anchor baseline) | Self-consistency majority voting: a fixed sample count, equal weight for every sample, no verification step at all — consensus-wrong answers pass through unchecked, exactly the failure a small, well-aimed verifier budget could catch. |

**critique:**
- summary: Every limitation is specific and tied to this paper's own input/output framing, but one baseline label overstates what a mismatched-I/O work licenses.
- comments:
  - `{severity: major, field: "specific_related_works[rw_trustorescalate].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Trust-or-Escalate's own framing is a per-item accept/escalate decision calibrated for bounded disagreement-with-humans risk — there is no cross-item budget coupling, because each item's escalation decision is made independently of every other item's. Marking it an unqualified 'true' baseline risks implying its own reported human-agreement guarantees are the comparison target, which they are not. Per the stage-3 rubric, a work whose I/O framing doesn't match this paper's (single-item threshold vs. batch-level budget-constrained ranking) 'is not a baseline — at best a method-side reference,' unless the mismatch itself is exactly what's being tested."}`
- decision: `move_to_refiner` (this is a precision fix to the field's accompanying note, not a structural change — the calibrated-threshold *mechanism* is still legitimately borrowable as a control arm).

### Refiner pass

- `rw_trustorescalate.is_potential_baseline` retained as `true`, but its note is sharpened: "Not a baseline in the beat-a-number sense — Trust-or-Escalate's own reported human-agreement risk-control results are not compared against. Its **calibrated per-item threshold mechanism** is adapted as a control arm specifically to isolate the value of *global*, budget-coupled ranking over *per-item*, budget-blind thresholding: if a policy that ignores the shared budget does just as well, the global-coupling framing adds nothing."
- `changes_made`: clarified Trust-or-Escalate's baseline role to avoid implying a direct results comparison against a mismatched I/O framing.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is promoted to a framing-tier RQ in Stage 6 — the closest candidate (rw_trim's step-vs-trajectory grain mismatch) is not an independent claim to verify but *is* the sub-problem itself (`sp_allocation_granularity` below), already covered end-to-end as a mechanism-tier RQ. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4):

- **`sp_proxy_validity`** — *description:* Establish whether any verifier-free signal computed before a verifier call (mode share, sequence log-likelihood, verbalized confidence) actually carries information about the verifier's eventual correct/incorrect label. *why_it_is_a_problem:* if it carries none, no allocation policy — however cleverly designed — can ever beat spending the budget blindly, so this isn't optional groundwork, it's the central claim the rest of the paper is conditioned on. *technical_challenge:* validating the proxy requires verifier labels, which are exactly the scarce resource the paper is trying to conserve — resolved only by decoupling proxy validation onto a held-out audited sample rather than the deployed budget itself; and the proxy's errors are adversarially structured, since the highest-value verification targets (confident-but-wrong consensus pools) are exactly what agreement-based signals rank as least worth checking. *source_limitation_ids:* `["rw_wang2023"]` (self-consistency's fixed, unweighted, unverified voting is the concrete case this sub-problem generalizes past).
- **`sp_domain_transfer`** — *description:* Determine whether a given signal's correctness-information content, and any policy built on it, still holds when the task domain shifts (bounded-answer-space math vs. open-ended code). *why_it_is_a_problem:* a policy validated only in-domain could be silently uninformative, or even mis-ranked, elsewhere — a real risk given how different math and code answer spaces are. *technical_challenge:* domain transfer can't be checked by more in-domain data; it requires freezing a policy tuned on one domain and evaluating it, unmodified, on a domain it was never tuned on. *source_limitation_ids:* `["__novel__"]` — no N4 limitation addresses cross-domain signal transfer specifically; the closest, Self-Capability's confidence-miscalibration finding, is about whether the signal exists at all, not whether it survives a distribution shift.
- **`sp_allocation_granularity`** — *description:* Decide, under one shared global budget, how to trade "verify a second trajectory of an already-uncertain instance" against "verify the first trajectory of a different instance" — ideally adaptively rather than by a single static ranking pass. *why_it_is_a_problem:* with one budget shared across many instances and trajectories, allocation is not a per-item threshold problem; a policy that can't reason across instances and across time (as outcomes arrive) leaves value on the table. *technical_challenge:* this is fundamentally a combinatorial, and potentially online/sequential, resource-allocation problem — any static, one-shot ranking is only an approximation to the true sequential decision process. *source_limitation_ids:* `["rw_trim"]` (TRIM's own motivation states local, per-step threshold decisions are insufficient because value-of-intervention is context-dependent — the same argument this sub-problem makes one grain up, at the level of whole trajectories across a pool rather than steps within one trajectory).
- **`sp_aggregation`** — *description:* Combine sparse, ground-truth-grade verified outcomes with dense, noisy unverified signals into one final answer per instance, without discarding the information the budget bought. *why_it_is_a_problem:* a verified-incorrect result eliminates a wrong answer but does not reveal the right one — an aggregator that doesn't exploit that elimination (e.g., falling back to a raw, un-corrected vote) wastes real information regardless of how good the allocation policy was. *technical_challenge:* the aggregation rule must be robust to the case where verification eliminates every candidate answer observed so far, not just the common case where a verified-correct answer is found. *source_limitation_ids:* `["__novel__"]` — no N4 limitation addresses the aggregation step; it is a decisive component this paper's own decomposition surfaces, not a gap in any cited work's I/O framing.

**critique:**
- summary: Coverage checks out — solving all four jointly would deliver Stage 1's objective — but two sub-problems risk reading as the same underlying concern about "does the signal carry information."
- comments:
  - `{severity: minor, field: "sp_proxy_validity / sp_domain_transfer", anti_pattern: "overlap", comment: "Both are framed around whether a signal 'carries information' about correctness, which can read as the same sub-problem stated twice. They are genuinely distinct — one is about whether the signal has *any* information content at all, within one fixed distribution; the other is about whether that information content is *stable under a distribution shift* — but the current phrasing doesn't make that distinction explicit enough for a reader to see they're not redundant."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_proxy_validity.technical_challenge` sharpened to end with: "...this is a **within-distribution information-content** problem — does the signal correlate with correctness at all, holding the sampling distribution fixed — not a question about whether that correlation survives elsewhere."
- `sp_domain_transfer.technical_challenge` sharpened to end with: "...this is a **distribution-shift stability** problem, distinct from within-distribution validity: a signal can be highly informative on math and still carry zero transferable information to code, and no amount of additional math-domain evidence resolves that — only an explicit frozen-policy, cross-domain test does."
- `changes_made`: made the within-distribution-validity vs. cross-distribution-stability distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; 2 sourced from related-work limitations, 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_uncertainty_scorer`** → targets `sp_proxy_validity`. *proposed_approach:* Compute three verifier-free signals per trajectory before any verifier call — mode share (fraction of the instance's sampled final answers agreeing with this one), normalized sequence log-likelihood, and a one-shot verbalized confidence rating — then measure each signal's AUROC against verifier-labeled correctness on a held-out audited sample, and separately count how often confident-but-wrong instances (plurality mode share ≥ 0.75, incorrect) are ranked outside the top-B by every signal. *key_insight:* proxy validity can't be assumed, but it can be converted from a hidden premise into a first-class measured quantity — and the same computed rank data that yields an aggregate AUROC also yields a structural failure-mode count, without a second measurement pass. *hypotheses:* ["At least one of the three verifier-free signals attains AUROC ≥ 0.65, with 95% DeLong CI lower bound > 0.55, against verifier-labeled trajectory correctness on at least 3 of 4 pilot model×dataset configurations.", "Confident-but-wrong instances — plurality-answer mode share ≥ 0.75 and incorrect — are systematically under-selected by every signal-ranked policy relative to chance: P(rank in top-B | confident-but-wrong) falls below B/(mN)."]
- **`m_budget_constrained_policy`** → targets `sp_allocation_granularity`. *proposed_approach:* Rank trajectories (or instances, compared as two granularities) most-uncertain-first and submit the top B for verification; additionally run a sequential variant that spends calls one at a time, stopping and reallocating remaining calls away from any instance that already has a verified-correct trajectory. *key_insight:* a static ranking is only an approximation to the true sequential decision process; comparing it against a sequential policy's measured gap-closure toward a hindsight-optimal allocation (computable post hoc, since oracle-stage pools are fully labeled) quantifies exactly how much the online character of the allocation problem matters, rather than assuming it does. *hypotheses:* ["The best single-signal, most-uncertain-first allocation policy beats uniform-random allocation at matched budget b = 0.10 by at least 2.0 accuracy points, with Holm-corrected McNemar p < 0.05, on at least 3 of 4 pilot configurations.", "Sequential reallocation closes at least 20% of the static policy's accuracy gap to hindsight-optimal allocation at b ≤ 0.10, with bootstrap CI excluding 0, on at least 2 of 4 configurations."]
- **`m_elimination_aggregator`** → targets `sp_aggregation`. *proposed_approach:* If any verified-correct trajectory exists for an instance, output its answer; otherwise remove every verified-incorrect *answer* from the candidate set and take a confidence-weighted majority vote over what remains; if verification eliminates every observed candidate answer, fall back to the highest-confidence unverified answer and flag the instance. *key_insight:* a verified-incorrect outcome doesn't name the right answer, but discarding it anyway (as a naive "verified-answer-or-raw-vote" rule does) throws away exactly the elimination information the budget already paid for. *hypotheses:* ["The elimination-aware aggregator beats the naive rule (use the verified answer if any, else raw majority vote) by at least 1.0 accuracy point at b = 0.25, with a paired bootstrap CI excluding 0, on at least 3 of 4 configurations."]
- **`m_realism_and_transfer_controls`** → targets `sp_domain_transfer`. *proposed_approach:* Before using a realistic (non-oracle) verifier operationally, audit it against held-out gold labels and require false-positive/false-negative rates below a pre-stated tolerance; separately, freeze a policy (signal choice plus granularity) tuned on one task domain and evaluate it, unmodified, on the other domain. *key_insight:* neither "trust" for a realistic verifier nor "transfer" for a signal-based policy can be assumed from within-condition performance alone — the only way to check whether either premise survives a shift (verifier class, or task domain) is to freeze the thing being tested and re-evaluate it under the shift, without retuning. *hypotheses:* ["Under execution (code) and process-reward-model (math) verifiers, the selective-allocation accuracy gain retains at least 50% of its oracle-verifier magnitude and remains statistically significant on at least 2 of 4 scale-up configurations.", "A policy frozen on one task domain beats uniform allocation on the other domain at b = 0.25, with corrected p < 0.05, in at least 3 of 4 transfer-direction × model cells."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis states a concrete, falsifiable threshold — but one method bundles two claims that read as testing two different premises, and the draft doesn't yet justify why that's one method rather than two.
- comments:
  - `{severity: major, field: "m_realism_and_transfer_controls.hypotheses", anti_pattern: null, comment: "The two hypotheses here test what look like different things — verifier-class realism (does the gain survive oracle→execution/PRM) and task-domain transfer (does a frozen policy survive math↔code) are not obviously the same claim, and stapling them into one method risks reading as scope creep dressed as a single mechanism, the same concern B5.5's stage-5 critic raised about `m_matched_conditions`. Either split this into two methods, or state explicitly why one mechanism produces both readouts."}`
- decision: `move_to_refiner` (the shared mechanism is real and already implicit in the proposed_approach — this is a justification gap, not a design gap).

### Refiner pass

- `m_realism_and_transfer_controls.key_insight` extended: "...concretely, both hypotheses are read off the **same design move** applied along two orthogonal shift axes: freeze the thing under test exactly as tuned or exactly as specified, then re-evaluate it — without retuning — under a shift it was not built for. For H_F the shift is in verifier class (oracle → execution/PRM); for H_G the shift is in task domain (math ↔ code). One audit-then-freeze-then-retest principle, two shift axes, not two unrelated mechanisms stapled together."
- `changes_made`: justified the two-hypotheses-one-method structure by naming the shared freeze-and-retest mechanism explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **7 hypotheses total** (2 + 2 + 1 + 2 across the four methods respectively — `m_uncertainty_scorer`, `m_budget_constrained_policy`, and `m_realism_and_transfer_controls` each carry two, per the one-instrument/one-mechanism, multiple-readout justifications above), mixing instrument-validity claims (signal AUROC, aggregation value) with the study's headline empirical predictions (selective beats uniform, gains survive realism and transfer) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Every baseline below is a sanity-check comparator or a strongest-alternative-explanation control, never a competitor this paper claims to beat for its own sake.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GSM8K (test split; pilot uses a fixed 500-instance subsample) — *justification:* grade-school math word problems with short, exactly-matchable final answers; cheapest domain to compute an oracle verifier label for, so it anchors the pilot.
- MATH-500 (500-problem competition-math subset, difficulty levels 1–5) — *justification:* harder math with graded difficulty, used to pre-screen model–dataset pairs into the non-degenerate accuracy band (30–70%) the allocation question requires, and as a second math-domain point for the domain-transfer test.
- HumanEval+ (164 tasks, EvalPlus-extended test suites) — *justification:* enables an execution-based realistic verifier with near-ground-truth reliability, stress-testing whether selective-allocation gains survive contact with a genuinely non-oracle, non-PRM verifier.
- (draft initially listed MBPP+ with justification only "digest lists it as a second code dataset for the scale-up stage" — flagged below.)

`baselines` (sanity-check comparators and strongest-alternative-explanation controls, not outcome-tier competitors):
- Uniform-random verifier-call allocation at matched budget — the necessary control for every allocation claim; if selective allocation cannot beat this, no allocation question exists.
- Full verification (B = N × #instances) — the upper anchor, and the source of the verification-headroom gate (full-verification accuracy must exceed no-verification accuracy by ≥ 0.05, or the config is out of scope).
- No verification / self-consistency majority vote (`rw_wang2023`) — the lower anchor.
- Difficulty-conditioned instance-level allocation, adapted from `rw_computeopttts` — the strongest-alternative-explanation control: rules out "the gains are just difficulty triage, not trajectory-level uncertainty."
- Confidence-threshold escalation, adapted from `rw_trustorescalate` — isolates the value of global, budget-coupled ranking over per-item, budget-blind thresholding (per Stage 3's sharpened role for this work).

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_signal_auroc` | `sp_proxy_validity` | "At least one of the three verifier-free signals attains AUROC ≥ 0.65, with 95% DeLong CI lower bound > 0.55, against verifier-labeled trajectory correctness on at least 3 of 4 pilot model×dataset configurations." |
| `rq_cbw_underselection` | `sp_proxy_validity` | "Confident-but-wrong instances — plurality-answer mode share ≥ 0.75 and incorrect — are systematically under-selected by every signal-ranked policy relative to chance: P(rank in top-B \| confident-but-wrong) falls below B/(mN)." |
| `rq_selective_vs_uniform` | `sp_allocation_granularity` | "The best single-signal, most-uncertain-first allocation policy beats uniform-random allocation at matched budget b = 0.10 by at least 2.0 accuracy points, with Holm-corrected McNemar p < 0.05, on at least 3 of 4 pilot configurations." |
| `rq_sequential_gap_closure` | `sp_allocation_granularity` | "Sequential reallocation closes at least 20% of the static policy's accuracy gap to hindsight-optimal allocation at b ≤ 0.10, with bootstrap CI excluding 0, on at least 2 of 4 configurations." |
| `rq_aggregation_value` | `sp_aggregation` | "The elimination-aware aggregator beats the naive rule (use the verified answer if any, else raw majority vote) by at least 1.0 accuracy point at b = 0.25, with a paired bootstrap CI excluding 0, on at least 3 of 4 configurations." |
| `rq_verifier_realism` | `sp_domain_transfer` | "Under execution (code) and process-reward-model (math) verifiers, the selective-allocation accuracy gain retains at least 50% of its oracle-verifier magnitude and remains statistically significant on at least 2 of 4 scale-up configurations." |
| `rq_domain_transfer` | `sp_domain_transfer` | "A policy frozen on one task domain beats uniform allocation on the other domain at b = 0.25, with corrected p < 0.05, in at least 3 of 4 transfer-direction × model cells." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing paper.md's already pre-registered E1–E3/H1–H3 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a provenance note rather than a reason tied to a specific RQ.
- comments:
  - `{severity: major, field: "datasets[MBPP+]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest lists it as a second code dataset' says nothing about which RQ needs a second code dataset or why one isn't redundant with HumanEval+."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "MBPP+ (378 tasks, EvalPlus variant) — *justification:* a second, larger and structurally different code benchmark (basic programming tasks vs. HumanEval+'s interview-style problems), needed specifically so `rq_domain_transfer`'s code-side cell and `rq_verifier_realism`'s execution-verifier audit are not certified from a single code dataset's idiosyncrasies alone."
- `changes_made`: gave MBPP+'s inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_matters`/`why_it_is_a_problem` fields name no technique (mode share, AUROC, and the elimination rule are introduced only from Stage 5 onward).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_proxy_validity.source_limitation_ids = ["rw_wang2023"]` and `sp_allocation_granularity.source_limitation_ids = ["rw_trim"]` both ∈ Stage 3 limitations ✓; `sp_domain_transfer` and `sp_aggregation` correctly use `["__novel__"]` with stated decisive-component justifications ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` entry is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (verified subset, final combined answer, budget–accuracy comparisons) are each reachable: the verified subset and the comparisons via `sp_proxy_validity` + `sp_allocation_granularity`; the combined final answer via `sp_aggregation`; generalization of all of it via `sp_domain_transfer` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, with all baselines framed as sanity checks or strongest-alternative-explanation controls, never as competitors this paper claims to beat.

**What was hardest:** as with B5.5, the recurring tension was not disagreement about facts (paper.md's own Steps 0–9 are unusually well-specified and pre-audited) but **scope discipline** — repeatedly checking whether a Stage-5/6 hypothesis was quietly restating paper.md's own already-finished Step 6 rather than adding something this schema's structure specifically demands. The two-hypotheses-one-method question (Stage 5, `m_realism_and_transfer_controls`) was the sharpest instance: paper.md's own E3 already lists H3a/H3b/H3c as "three separable sub-claims" under one RQ without stating *why* they're separable-but-unified, which is exactly the gap this pipeline's critic/refiner loop exists to close.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Revision pass over the review artifacts (`stage_review.md`, `taste_audit.md`, `pipeline.md` Phase Log; no `design_review.md` exists for this topic). Every finding in those files was enumerated and its status checked against the current deliverables; past rounds above are untouched. Findings already applied in earlier passes are listed for the record; the one OPEN finding was applied this round.

**Already applied in earlier passes (verified present in current deliverables, no action needed):**
- `stage_review.md` Stage 2 REVISE → nearest-neighbor TRIM sentence → present as the opening paragraph of Related Work (`paper_draft.md`/`.tex`).
- `stage_review.md` Stage 4 REVISE → per-RQ falsification conditions → present in all 7 RQ subsections (`paper_draft.md`/`.tex`) and in `experiment_design.md`.
- `stage_review.md` Phase A items 2/5/6 → reference-cache backfill; A1–A6 Gate/Consequence clauses; R1 estimand + power-and-thin-cell rule → present in `reference_candidates.jsonl` and `../paper.md`.
- `pipeline.md` Phase G [major] → RQ3 extended with paper.md H2(i) budget-recovery criterion → present in RQ3 part (ii) in all three deliverables.
- `pipeline.md` Phase G [moderate] → APC(B)/R(b) formal definitions → present in the Problem Definition's formal setup.
- `pipeline.md` Phase G [minor] → RQ2 chance rate B/(mN) → present in RQ2's Setup.
- `taste_audit.md` → 🟢 both passes, no action items.

**Applied this round:**
- Source: `pipeline.md` Phase G [moderate], logged-not-fixed ("B-alt controls ... named in Baselines but not wired into any RQ's comparison arms") + `pipeline.md` "Open to-dos carried forward" item (1) + `experiment_design.md` §2's own "Note on B-alt wiring (open to-do)". Finding: the two strongest-alternative-explanation controls (difficulty-conditioned instance-level allocation adapted from Compute-Optimal-TTS; confidence-threshold escalation adapted from Trust-or-Escalate) had no explicit RQ comparison arm. What changed: RQ3 extended with a part (iii) carrying `paper.md` § Mandatory baselines' pre-registered comparison verbatim ("M2 instance-level policy vs. B-alt at b ∈ {.10,.25}, same families/corrections; if M2 does not beat difficulty-triage, the claim demotes from 'trajectory-uncertainty-guided' to 'difficulty-guided' allocation") — Setup, Expected outcome, Falsification condition (framed as an attribution test with the committed demotion wording, not a refutation of the allocation gain), and Metrics all extended; the §2 wiring note flipped from open to resolved-with-pointer. The extend-RQ3 option was chosen over a dedicated RQ8 because `pipeline.md` itself offered it and no Stage 5 hypothesis exists for B-alt (target hypotheses must stay byte-identical to their sources; nothing new was invented — every threshold and clause in part (iii) is quoted or directly derived from `paper.md`). Files: `experiment_design.md` (Baselines note + RQ3), `paper_draft.md` (RQ3 subsection), `paper_draft.tex` (RQ3 subsection, recompiled to `paper_draft.pdf`, exit 0, zero undefined citations).

**Rejected — moot:**
- `pipeline.md` "Open to-dos carried forward" item (2): 7 of 9 N3-cited works (OpenReview-only anonymous submissions) have lightweight stub digests instead of full N0–N12 digests. Rejected — blocked on an external dependency (no public PDF mirror exists for these submissions); already honestly logged in `pipeline.md` and `stage_review.md`, and not resolvable by editing any deliverable in this environment.
