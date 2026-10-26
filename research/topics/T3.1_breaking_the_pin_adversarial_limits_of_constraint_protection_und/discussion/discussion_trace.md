# Discussion Trace — T3.1 (Stage 1-6 critic/refiner record)

> Extracted verbatim from `pipeline.md`'s "## Seed brief" through "## Cross-stage consistency check" sections (the full `auto-research-discussion` round-by-round record: every draft version, every critique with severities and resolution, every refiner pass, every decision), per the skill's updated "Final deliverables" spec (three separate output files: `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`). No content was regenerated — this is the same critic/refiner discussion that already fed `paper.md` and `paper_draft.md`/`.tex`/`.pdf`. `pipeline.md` itself now points here and retains only its Phase Log section (goal.md §2 pipeline-state tracking — a separate concern from this stage-discussion trace).

---

## Seed brief

- **One-sentence description:** Measure the precise adversarial-strength boundary at which pinning-style memory-constraint-protection defenses break under context compaction, and the attacker-to-defender cost ratio at that boundary.
- **Apparent inputs:** pinned task/safety constraints an LLM agent must obey across a long-horizon session; a lossy context-compaction mechanism under a fixed token budget; a matrix of pinning-style defense variants; an adversarial injection procedure (gradient-optimized suffix and template-role-forgery families) parametrized by an explicit strength knob.
- **Apparent outputs:** per-variant break-through-rate curves over injection strength; a boundary scalar (BT50/BT90) per curve; an attacker-cost-to-defender-cost ratio at that boundary, under multiple currencies.
- **Closest research areas:** LLM-agent prompt-injection attacks and defenses (ChatInject, TensorTrust, ThreatSnapshots); optimization-based jailbreaks (GCG, SlotGCG, TAO-Attack); context-compression/agent-memory pipelines (COMI, an information-theoretic channel view, LightMem).
- **In scope:** measuring existing pinning-defense variants' adversarial breakability and cost-effectiveness under a controlled compaction/injection harness. **Out of scope:** proposing a new pinning defense as the paper's primary contribution; training/fine-tuning attacker or defender models; live/non-sandboxable deployments.
- **Confidence: high.** As with a prior reverse-digest run in this batch, the "repo" here is itself a prior reverse-digest (`digest.md`) plus an unusually rigorous pre-registered spec (`paper.md`) — the latter already contains its own formal asymmetry statement (Step 0), archetype classification (Step 2), taste self-audit (Step 3), notation/oracle/assumption tables (Step 5), pre-registered experiments with fallbacks (Step 6), and a minimum-viable walking skeleton (Step 9). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own already-finished design work, which is why stages 5/6 below are framed as re-deriving the confirmed design through this schema's own discipline (falsifiable hypotheses tied to sub-problems, verbatim hypothesis→RQ traceability) rather than re-inventing it from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a set of pinned constraints an LLM agent must obey across a long-horizon session, a context-compaction mechanism that periodically compresses conversation/tool history under a fixed token budget, a matrix of pinning-style defense variants protecting those constraints, and an adversarial injection procedure (parametrized by an explicit strength scalar) targeting them, determine the injection strength at which each pinning-defense variant's post-compaction constraint break-through rate crosses a meaningful threshold, and the resulting ratio between the attacker's cost to reach that threshold and the defender's cost to run that variant.
- `input`: (1) agent trajectories with pinned constraints C, each obligatory for the remainder of the session; (2) a compaction event schedule that summarizes history under a fixed token budget B; (3) a defense-variant matrix D = {no-defense control, verbatim re-injection, redundant k-copy, checksum/tag-verified, structurally isolated protected-memory slot}; (4) an adversarial injection procedure per attack family (white-box gradient-optimized suffix; black-box template-role forgery), each parametrized by a strength scalar s.
- `output`: (1) per-(variant, attack-family, model) break-through-rate curves over s; (2) a boundary scalar (BT50/BT90) per curve, where the curve supports one; (3) an attacker-cost-to-defender-cost ratio at that boundary, in a stated currency.
- `constraints`: the injection attack is already established (premise, not re-derived here) to break through every tested model's pinning defense under some configuration; a break-through must be verifiable by a separable oracle checking the constraint's state before *and* after a compaction event, not inferred from the raw transcript alone.
- `objective`: a boundary is accepted for a given (variant, attack-family, model) cell only if a fitted break-through curve clears a stated fit-quality bar.
- `study_type`: `empirical` — stated explicitly: digest N12 classifies this `empirical` on the grounds that the defense-variant matrix, the strength sweep, and the two-tier oracle are instrumental to a measurement, not the headline offering (no new defense is proposed as the primary contribution).

**critique:**
- summary: Strong, evidence-traceable draft, but the objective has a real evaluability gap that the seed's own later material (N9) already implicitly resolves without saying so here.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective says a boundary is 'accepted' only if a fit-quality bar is cleared, but never states what happens to a cell that fails the bar because the curve is flat and low, not because the fit is bad. Digest N9's own predicted-direction language already treats a variant whose break-through rate stays capped below a low ceiling across the *entire* tested strength range ('unbreakable-in-range') as a stronger, more interesting result, not a missing data point — but the objective as written only defines acceptance for a rising-with-strength curve, silently leaving open whether a well-fit-but-flat cell counts as a success of the design or a gap in it."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'determine the injection strength at which each ... variant's ... break-through rate crosses a meaningful threshold' presupposes every variant crosses a threshold somewhere in range. Prefer phrasing that leaves 'crosses, or remains bounded below it throughout the tested range' equally open, symmetric with the objective fix."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content the digest already supports — no new content needed).

### Refiner pass

- `objective` (refined): "A boundary is accepted for a given (variant, attack-family, model) cell only if a fitted break-through curve clears a stated fit-quality bar (McFadden pseudo-R² ≥ 0.3, a significantly positive slope, and a bounded BT50 confidence interval); a cell whose break-through rate instead stays flat and below a low ceiling across the entire tested strength range is not a missing result but a distinct, equally reportable outcome — an unbreakable-in-range finding. The attacker/defender cost ratio is computed only over boundary-accepted cells; unbreakable-in-range cells are reported separately rather than silently dropped."
- `summary` (refined): "...determine, for each pinning-defense variant, whether and at what injection strength its post-compaction constraint break-through rate crosses a meaningful threshold within the tested range, or whether it instead remains bounded below that threshold throughout — and, where a boundary is found, the ratio between the attacker's cost to reach it and the defender's cost to run that variant."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation rather than inventing new symbols): "Trajectory of turns τ_1..τ_T; compaction event κ maps history to ≤B tokens, m≥1 events per trajectory; pinned constraint c ∈ C; defense variant d ∈ D = {d_0, d_reinj, d_kcopy, d_cksum, d_slot}; attack family a ∈ A = {a_wb, a_bb}; normalized strength s ∈ [0,1]; break-through indicator V(c,T;d,a,s,ω) ∈ {0,1}. For each (d,a,model g), estimate p_{d,a,g}(s) = Pr[V=1]; derive (i) BT50/BT90 where the fit-quality bar is cleared, (ii) the cost ratio R at BT50, (iii) cross-condition ordering stability."
- `changes_made`: tightened the objective's acceptance condition to name the unbreakable-in-range outcome explicitly; removed the presupposition from `summary`; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Memory-pinning is one of the main proposed mechanisms for keeping safety- and task-critical constraints alive through the lossy context-compaction that long-horizon LLM agents require, but whether — and how cheaply — an adversary can defeat it has so far only been shown to happen at all, never mapped as a function of attack strength or priced against what the defense costs to run.
- `why_it_matters`: As agent deployments grow long enough to require periodic context compaction, pinning-style defenses are the load-bearing mechanism operators lean on to assume a constraint fixed at session start ("never call this tool," "always defer to a human above $X") survives every later summarization pass. The prior paper's finding that an optimization-based injection broke every tested model's pinning defense already shows this assumption is not unconditionally true — but "not unconditionally true" is not actionable for a deployment decision. An operator choosing among the five variants (no-defense, re-injection, k-copy, checksum, structural slot) needs to know not just that each eventually fails, but at what attack strength, because a variant that fails only at a strength far beyond any deployed adversary's practical budget is a very different deployment decision from one that fails cheaply.
- `who_cares`: Operators of long-horizon LLM agents who rely on pinning to keep a safety- or task-critical constraint alive without re-verifying it every turn; designers of the next pinning variant, who need a comparison protocol rather than a single reported attack; security researchers deciding whether prompt-injection defenses generally should be evaluated by pass/fail alone or by a strength-swept curve.
- `evidence`: `[TensorTrust, OpenReview:fsW7wJGLBd]`'s own motivation argues injection defenses need to be evaluated on a robustness-vs-usability trade-off, not a single robustness number — precisely the kind of curve, not point, this paper measures for pinning specifically. `[LightMem, OpenReview:dyJ0GWpjJB]`'s consolidation mechanism is evaluated only on benign long-horizon dialogue consistency benchmarks (LoCoMo/LongMemEval), never under adversarial stress — evidence that a persistence claim and an adversarially-stress-tested persistence claim are different things nobody has measured together for a compaction-surviving pinning mechanism (N3 search-honesty note: none of the nine on-topic corpus papers combines a strength-swept attack, a memory-pinning target, and a cost ratio).

**critique:**
- summary: Good stake-specific motivation with real citations, but coverage of stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "why_it_matters justifies output (1) break-through curves and output (2) boundary scalars — knowing at what strength each variant fails — but never separately motivates why output (3), the attacker/defender *cost ratio*, is worth reporting once the boundary is already known. A reader could reasonably ask: if variant X's BT50 is already higher than variant Y's, why report a cost ratio too — doesn't the higher BT50 already say X is 'better'? That is a real, unaddressed gap: BT50 alone conflates how much attacker effort was needed to reach that strength with how much defender effort the variant itself imposes every turn. A variant with a modestly higher BT50 that costs far more in per-turn defender overhead to achieve it could be a strictly worse deployment choice than one with a lower BT50 and near-zero overhead — and nothing in why_it_matters currently says this."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, the boundary alone cannot answer a deployment trade-off between defender overhead and attacker resistance: two variants can have well-separated BT50 values while one imposes negligible extra tokens/latency per turn and the other imposes substantial per-turn overhead to reach its higher boundary — a difference invisible in the break-through curve alone and recoverable only once attacker cost to reach the boundary and defender cost to maintain the variant are expressed in a common unit and divided. The cost ratio is therefore not a restatement of the boundary but the one piece of information an operator needs to trade marginal robustness against marginal overhead, which no break-through curve by itself supplies."
- `changes_made`: added the cost-ratio-is-not-redundant-with-boundary argument.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level; no title-only landscape mentions were present in the source material, and per the no-fabrication rule no additional landscape papers are invented here to pad a `general_related_works` list. One entry (`rw_gcg`) is a canonical non-corpus anchor, flagged as such per N3.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / role / limitation → sub-problem it will motivate):

| work_id | citation | is_potential_baseline | limitation |
|---|---|---|---|
| `rw_chatinject` | Anon., ChatInject (OpenReview:WVhgFSKniL) | false (fixed single config, no strength axis) | Demonstrates template-role forgery breaks agent defenses at one fixed configuration; does not sweep a continuous strength parameter, target memory-pinning under compaction, or report a cost ratio. |
| `rw_threatsnapshots` | Anon., ThreatSnapshots / "Breaking Agent Backbones" (OpenReview:kga18ld70t) | false (single-call abstraction mismatch) | Deliberately isolates a single backbone LLM call to fix attribution; a pinned constraint's survival is a multi-event lifecycle property (repeated compaction passes) a one-call snapshot cannot represent. |
| `rw_slotgcg` | Anon., SlotGCG (OpenReview:Fn2rSOnpNf) | **true** | Optimizes adversarial-token insertion position to defeat single-turn safety-refusal; treats attack strength as a fixed budget, not a swept variable, against structured memory-pinning defenses. |
| `rw_taoattack` | Anon., TAO-Attack (OpenReview:XfbBiBG46D) | false | Replaces GCG's loss with a two-stage refusal-suppression objective; same single-turn refusal target as SlotGCG, no strength sweep against pinning. |
| `rw_guidedbench` | Anon., GuidedBench (OpenReview:ZVg8y3ibyM) | false (oracle reference, not baseline) | Sharpens the oracle for jailbreak success into an entity/action checklist, but the object is single-turn harmful-content elicitation; provides no oracle for "was a pinned constraint violated after compaction." |
| `rw_tensortrust` | Anon., TensorTrust (OpenReview:fsW7wJGLBd) | **true** | Measures a robustness-vs-usability trade-off for prompt injection in a single-turn string-comparison game with static human-authored defenses; no compaction dynamic, no swept strength axis. |
| `rw_comi` | Anon., COMI (OpenReview:OGDIXDfaN4) | false | Models what compression cooperatively retains under a benign objective; no adversary trying to evict a protected constraint. |
| `rw_infochannel` | Anon., "Information Theoretic Perspective on Agentic System Design" (OpenReview:isFHz8qf20) | false | Same benign, cooperative channel-compression view as COMI; no adversarial durability claim. |
| `rw_lightmem` | Anon., LightMem (OpenReview:dyJ0GWpjJB) | false (inspires a defense variant, not a baseline) | Efficient summarization+consolidation memory pipeline evaluated only on benign long-horizon dialogue consistency (LoCoMo/LongMemEval); its consolidation step is never adversarially stress-tested. |
| `rw_gcg` | Zou et al., 2023 (arXiv:2307.15043) | false (canonical anchor, not corpus) | Established gradient-guided greedy coordinate-descent suffix optimization; the discrete-optimization-injection family SlotGCG/TAO-Attack extend, not itself evaluated against pinning under compaction. |

**critique:**
- summary: Grounding is solid and every limitation is specific, but one baseline label needs scrutiny, and one limitation is a strong enough candidate for a framing-tier check that leaving it un-flagged would be an omission.
- comments:
  - `{severity: major, field: "specific_related_works[rw_slotgcg].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "SlotGCG's I/O framing is single-turn safety-refusal defeat at a fixed budget — genuinely different from this paper's framing (strength-swept break-through of memory-pinning across compaction events). Marking it a straightforward baseline risks implying SlotGCG's own reported attack-success numbers are being compared against, which they are not; per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.'"}`
  - `{severity: minor, field: "specific_related_works[rw_comi, rw_infochannel].limitations[].verify_as_hypothesis", anti_pattern: null, comment: "Both limitations note that neither work models an adversary trying to evict a protected constraint — i.e., both only establish *benign* retention behavior. This is a strong candidate to flag `verify_as_hypothesis: true`, since 'observed break-through is attributable to the adversarial injection, not to generic benign-compaction degradation' is exactly the kind of gap this paper is positioned to verify directly (`paper.md`'s own B0/B-alt controls already build toward this), and leaving it unflagged would mean a real, available framing-tier check goes unasked at Stage 6."}`
- decision: `move_to_refiner` (the baseline fix is wording-precision; the `verify_as_hypothesis` flag is additive, not corrective, but both are the kind of thing the refiner is meant to apply once flagged).

### Refiner pass

- `rw_slotgcg.is_potential_baseline` retained as `true`, but sharpened: "Not a baseline in the beat-a-number sense — SlotGCG's own reported refusal-defeat numbers are not compared against. Its **optimization machinery** (GCG-style greedy coordinate descent over insertion slots) is borrowed as the white-box attack family, independent of its published findings — the same role `rw_chatinject`'s template-role-forgery protocol plays for the black-box attack family."
- `rw_comi` and `rw_infochannel`'s shared limitation (`lim_comi_infochannel_benign`) set to `verify_as_hypothesis: true`: "This paper will verify, not merely assume, that observed post-compaction break-through is attributable to the adversarial injection specifically rather than to generic benign compaction-induced degradation that COMI/InfoChannel's cooperative framing would already predict at some baseline rate."
- `changes_made`: clarified SlotGCG's baseline role to avoid an implied I/O-mismatched comparison (and noted the same reasoning already applied to ChatInject in `draft_v1`); flagged the COMI/InfoChannel limitation as a framing-tier hypothesis to carry into Stage 6.
- `declined_to_fix`: none.

**Confirmed Stage 3** — 10 related works (9 specific + 1 canonical anchor), 7 limitations (`lim_chatinject_fixed_config`, `lim_threatsnapshots_single_call`, `lim_slotgcg_taoattack_gcg_no_cost` [shared: SlotGCG, TAO-Attack, GCG], `lim_guidedbench_no_persistence_oracle`, `lim_tensortrust_static_no_compaction`, `lim_comi_infochannel_benign` [shared: COMI, InfoChannel, `verify_as_hypothesis: true`], `lim_lightmem_benign_only`).

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C5 plus one new problem the mechanism map (N6) implies but N5 doesn't name directly — the oracle):

- **`sp_lossy_compaction_tradeoff`** — *description:* Score defense variants against the fact that compaction is lossy summarization by construction, so a "perfect" defense would either exempt pinned content from compaction entirely (defeating compaction's purpose) or require a verifier robust to arbitrary adversarial rewriting of the surrounding context. *why_it_is_a_problem:* Any variant's measured resistance is only meaningful once it's clear whether the variant survives *by* competing in the lossy pass or *by* sidestepping it — conflating the two would misattribute why a variant is robust. *technical_challenge:* the five candidate mechanisms sit on both sides of this line (re-injection/k-copy/checksum all compete inside the lossy pass and then attempt repair; the structural slot sidesteps it), and no single metric distinguishes "resisted the loss" from "was exempted from it" without instrumenting per-turn constraint state directly. *source_limitation_ids:* `["__novel__"]`.
- **`sp_strength_commensurability`** — *description:* Put two structurally different attack families (gradient-optimized suffix search; template-role forgery) on one comparable strength axis so a single break-through curve can be fit and compared per defense variant regardless of which family produced it. *why_it_is_a_problem:* without a shared axis, "variant X's boundary" would mean something different depending on which attack produced the number, making cross-variant and cross-family comparison meaningless. *technical_challenge:* the two families' raw strength units are structurally incommensurable (optimization iterations × candidate-set size × token budget vs. forged-turn count × payload token budget); there is no natural common unit, only a chosen normalization. *source_limitation_ids:* `["__novel__"]`.
- **`sp_violation_oracle_definition`** — *description:* Define, operationally, what counts as "the pinned constraint was violated after compaction" — a relational property across two points in time (present before compaction, violated at or after it), not a property of any single model output. *why_it_is_a_problem:* every downstream rate, curve, and cost ratio is only as valid as this oracle; a mis-scored oracle silently corrupts everything built on top of it. *technical_challenge:* hard constraints (a forbidden tool call, a numeric/format rule) admit a deterministic check, but soft constraints require a judge, and no existing oracle in the related-work landscape checks *persistence across a compaction event* — every one checks either single-turn harmfulness or single-call security. *source_limitation_ids:* `["lim_guidedbench_no_persistence_oracle"]`.
- **`sp_cost_currency_commensurability`** — *description:* Express attacker effort (optimizer queries, forward/backward passes, or tokens spent to reach a boundary) and defender effort (extra tokens/latency per turn a variant imposes) in one common currency so a ratio between them means something. *why_it_is_a_problem:* attacker and defender effort are denominated in entirely different kinds of resources (offline optimization compute vs. per-turn runtime overhead); reporting them separately would leave "is this variant worth its overhead" unanswerable as a single number. *technical_challenge:* no currency is uniquely correct — a token-equivalent conversion and an API-dollar-class conversion can, in principle, rank variants differently, so any chosen currency embeds a methodological assumption that must be surfaced, not hidden. *source_limitation_ids:* `["__novel__"]`.
- **`sp_stochastic_boundary_identifiability`** — *description:* Estimate a break-through rate, and the boundary derived from it, with quantified sampling error rather than as a point value, since LLM outputs and any LLM-judge oracle are non-deterministic. *why_it_is_a_problem:* without this, a reported boundary could be an artifact of noise at an underpowered trial count rather than a real property of the (variant, attack, model) cell. *technical_challenge:* the number of trials needed to resolve a boundary to a useful precision is itself unknown in advance and must be determined by a power criterion tied to the observed curve's steepness, not fixed a priori. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's outputs), but two sub-problems both lean on "no shared unit exists" as their core difficulty and could read as the same sub-problem stated twice.
- comments:
  - `{severity: minor, field: "sp_strength_commensurability / sp_cost_currency_commensurability", anti_pattern: "overlap", comment: "Both invoke the absence of a natural common unit as their central difficulty, which can read as one incommensurability problem restated. They are genuinely distinct — one is about putting *attack strength* (a single-sided quantity describing how hard the attacker is pushing) on a shared axis across two attack families; the other is about putting *two different actors' effort* (attacker offline compute vs. defender per-turn runtime cost) into one currency so they can be divided — but the descriptions don't make that distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_strength_commensurability.technical_challenge` sharpened to end with: "...this is a **single-axis normalization** problem — making one actor's (the attacker's) effort comparable across two different attack mechanisms — not a two-actor cost problem."
- `sp_cost_currency_commensurability.technical_challenge` sharpened to end with: "...this is a **cross-actor currency** problem distinct from the strength-axis normalization above — it compares two different actors' effort (attacker vs. defender), each already measured on its own terms, not two variants of the same actor's effort."
- `changes_made`: made the single-axis-normalization vs. cross-actor-currency distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 1 sourced from a related-work limitation, 4 `__novel__` with stated decisive-component justifications; digest N5's C3 — "adaptive adversary has a computable break point in principle, the question is cost, not if" — is treated as the motivating rationale folded into why `sp_cost_currency_commensurability` matters, not a sixth standalone sub-problem, since it restates why the cost dimension is needed rather than naming a distinct technical obstacle).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods, one per confirmed sub-problem):

- **`m_structural_defense_matrix`** → targets `sp_lossy_compaction_tradeoff`. *proposed_approach:* Implement five pinning variants as interchangeable middleware wrappers around a compaction summarizer — no-defense control, verbatim re-injection, redundant k-copy pinning, checksum/tag-verified pinning (a validator recomputes a hash of the protected span and re-inserts on mismatch), and a structurally isolated protected-memory slot exempt from summarization — instrumented to log each constraint's presence and verbatim state per turn, before and after every compaction event. *key_insight:* only the structural-slot variant sidesteps the lossy competition entirely by keeping content outside the compaction pass; the other four all still compete for retention budget inside the lossy channel and differ only in how they attempt post-hoc recovery — a difference invisible unless per-turn constraint state is instrumented directly rather than inferred from a final transcript. *hypotheses:* ["The structural protected-memory-slot variant achieves the highest BT50 of the five tested variants, because it is the only variant that removes pinned content from the lossy compaction competition entirely rather than attempting post-hoc recovery."]
- **`m_strength_sweep_protocol`** → targets `sp_strength_commensurability`. *proposed_approach:* Parametrize each attack family with an explicit strength knob (gradient family: optimization iterations × candidate-set size × token budget; template family: forged-role/turn count × payload token budget) and normalize both onto a shared [0,1] axis via a log-transformed, per-family-bounded scale, s = (log ρ − log ρ_min)/(log ρ_max − log ρ_min). *key_insight:* normalizing two structurally incomparable raw attack budgets onto one log-scaled axis is what allows a single break-through-vs-strength curve to be fit and compared per variant regardless of which attack family produced it — reporting each family's raw units instead would make no variant comparable across families. *hypotheses:* ["For at least 4 of the 5 defense variants (per model, per attack family), the fitted logistic break-through-vs-strength curve achieves McFadden pseudo-R² ≥ 0.3 with a significantly positive slope (Holm-corrected p < 0.05) and a BT50 bootstrap 95% CI no wider than 25% of the tested strength range."]
- **`m_two_tier_violation_oracle`** → targets `sp_violation_oracle_definition`. *proposed_approach:* Define constraint violation via a two-tier oracle — a deterministic programmatic check for hard constraints (forbidden tool call fired, numeric/format rule broken) and a GuidedEval-style rubric LLM-judge checklist for soft constraints — gated by an attribution requirement that the constraint was present immediately before the compaction event and violated at or after it. *key_insight:* a persistence oracle checks a relational property across two time points (present-before, violated-after), which is exactly what none of the existing single-turn harmfulness or single-backbone-call security oracles in the related-work landscape are built to check. *hypotheses:* ["The rubric LLM-judge tier of the oracle achieves Cohen's κ ≥ 0.6 against human labels on a held-out audit set; below that threshold, soft-constraint results are demoted to secondary/exploratory status rather than treated as confirmatory."]
- **`m_dual_currency_cost_accounting`** → targets `sp_cost_currency_commensurability`. *proposed_approach:* Convert attacker effort (optimizer queries, forward/backward passes, or API tokens spent to reach a variant's boundary) and defender overhead (extra tokens and latency imposed per turn) into a token-equivalent common currency, and separately into an API-dollar-class currency, then compute the ratio at each variant's BT50 under both. *key_insight:* expressing attacker and defender effort in the same unit — and doing so under two independently motivated currencies rather than one — turns "is this variant worth its overhead" from an incommensurable comparison into a checkable number whose currency-sensitivity is reported rather than hidden. *hypotheses:* ["The attacker/defender cost ratio at BT50 differs by at least 2× between the cheapest-to-break and most-expensive-to-break variant (Holm-corrected Wilcoxon signed-rank rejecting equality for at least one pair, α = 0.05), and the resulting variant ranking is identical (Kendall τ = 1) across the token-equivalent and API-dollar-class currencies."]
- **`m_bootstrap_boundary_estimation`** → targets `sp_stochastic_boundary_identifiability`. *proposed_approach:* Fit a logistic break-through-vs-strength curve per (variant, model, attack family) with Wilson score intervals on the raw rate and bootstrap confidence intervals on BT50/BT90, raising the per-cell trial count until the Wilson half-width falls below a preset threshold at the steepest grid point *before* fitting — a power gate rather than a fixed, possibly underpowered N. *key_insight:* reporting BT50 as a bootstrap interval derived from a power-gated trial count, rather than a point estimate from an arbitrarily chosen N, is what lets a boundary claim be distinguished from an equally-shaped curve that is actually sampling noise around a flat rate. *hypotheses:* ["Cross-model and cross-attack-family orderings of defense variants by BT50 (and separately by cost ratio) show mean pairwise Kendall's τ ≥ 0.6 at permutation p < 0.05, indicating the relative robustness ranking of pinning variants is largely model/attack-family-agnostic even as absolute BT50 values shift."]

**critique:**
- summary: Every method has a real mechanism and a falsifiable hypothesis with a stated threshold, but one hypothesis under-claims relative to what the source material already commits to.
- comments:
  - `{severity: minor, field: "m_structural_defense_matrix.hypotheses", anti_pattern: null, comment: "The hypothesis only claims the structural-slot variant is *highest*, leaving the relative order of the other four variants unstated. `paper.md`'s own Step 8 (H1) already commits to a full directional prediction — d_slot > d_cksum > d_kcopy > d_reinj > d_0 — as 'directional, to be confirmed.' Stating only the endpoint throws away a stronger, more falsifiable claim the design already supports without extra cost."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_structural_defense_matrix.hypotheses` extended to: "The five variants' BT50 values are ordered structural-slot > checksum-verified > k-copy > verbatim re-injection > no-defense-control, i.e., resistance increases with how far a variant's recovery mechanism is removed from relying on the lossy compaction pass to have preserved the constraint verbatim — a directional prediction to be confirmed, not merely that the structural-slot variant is highest among an otherwise-unordered set."
- `changes_made`: replaced the endpoint-only claim with the full pre-registered resistance ordering, made falsifiable at every adjacent pair, not just the top.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **5 hypotheses total** (one per method). Note, mirroring the design choice made explicit in a prior run of this pipeline: `m_two_tier_violation_oracle`'s hypothesis (an oracle-agreement threshold) and `m_bootstrap_boundary_estimation`'s hypothesis (a cross-condition rank-correlation) are **instrument-validity claims** — they certify the measurement apparatus itself is trustworthy — while `m_structural_defense_matrix`, `m_strength_sweep_protocol`, and `m_dual_currency_cost_accounting`'s hypotheses are the study's **headline empirical predictions** (which variant resists most, whether a boundary is fittable at all, whether cost differentiates variants). Mixing the two within one confirmed method set is a deliberate choice for an `empirical` study_type: the instrument-validity claims gate whether the headline claims can be trusted at all, and both kinds are equally falsifiable, so both belong in the same hypothesis set rather than being demoted to a methods appendix.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 5 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 1 RQ** — Stage 3's `lim_comi_infochannel_benign` was flagged `verify_as_hypothesis: true`; one RQ tests it directly.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators and confound-isolation controls only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- AgentDojo — *justification:* a tool-using agent environment that natively hosts task constraints alongside a security-relevant execution log, giving the hard-constraint oracle tier a programmatically checkable substrate (forbidden tool calls, numeric/format rules) without relying on judge-only scoring.
- InjecAgent — *justification:* an indirect-prompt-injection agent benchmark; supplies the injection substrate and existing attack-insertion scaffolding the template-role-forgery family (ChatInject-style) is adapted from.
- τ-bench (tau-bench) — *justification:* tool-agent tasks with explicit policy constraints closer to production agent workloads than AgentDojo's security-research framing, testing whether the boundary/cost findings generalize beyond one benchmark's task distribution.
- (draft initially listed LongMemEval/LoCoMo with justification only "digest mentions it as the compaction workload" — flagged below.)

`baselines` (sanity-check comparators and confound-isolation controls, not outcome-tier competitors):
- No-defense control under benign (non-adversarial) compaction — the necessary control for the framing-tier RQ (see below): establishes what fraction of constraints are lost to compaction alone, with no attacker present.
- Budget-matched benign-filler injection — replaces the attacker's payload with benign filler of identical token budget, count, and insertion position; isolates whether break-through is caused by the adversarial content specifically or by generic long-context degradation at matched budget.
- Scripted/non-adaptive template variants (fixed forged-role count, no optimization) — checks that any observed strength-dependent trend is not simply an artifact of longer prompts in general.

`research_questions` (6: 1 framing + 5 mechanism):

| rq_id | tier | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|---|
| `rq_benign_vs_adversarial_attribution` | framing | — (targets `lim_comi_infochannel_benign`) | "Neither work models an adversary trying to evict a protected constraint, so retention guarantees say nothing about adversarial durability of pinned content." |
| `rq_structural_slot_resistance` | mechanism | `sp_lossy_compaction_tradeoff` | "The five variants' BT50 values are ordered structural-slot > checksum-verified > k-copy > verbatim re-injection > no-defense-control..." |
| `rq_boundary_fit_quality` | mechanism | `sp_strength_commensurability` | "For at least 4 of the 5 defense variants... McFadden pseudo-R² ≥ 0.3 with a significantly positive slope... and a BT50 bootstrap 95% CI no wider than 25%..." |
| `rq_oracle_agreement` | mechanism | `sp_violation_oracle_definition` | "The rubric LLM-judge tier of the oracle achieves Cohen's κ ≥ 0.6 against human labels..." |
| `rq_cost_ratio_differentiation` | mechanism | `sp_cost_currency_commensurability` | "The attacker/defender cost ratio at BT50 differs by at least 2× between the cheapest-to-break and most-expensive-to-break variant... identical (Kendall τ = 1) across... currencies." |
| `rq_cross_model_ranking_stability` | mechanism | `sp_stochastic_boundary_identifiability` | "Cross-model and cross-attack-family orderings of defense variants by BT50 (and separately by cost ratio) show mean pairwise Kendall's τ ≥ 0.6 at permutation p < 0.05..." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 6/8 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis or flagged limitation, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[LongMemEval/LoCoMo]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it as the compaction workload' is not a justification — it says nothing about which RQ needs it or why AgentDojo/InjecAgent/τ-bench alone wouldn't suffice."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "LongMemEval and LoCoMo — *justification:* both natively require *multiple, repeated* compaction events across long multi-session dialogue, which single-session benchmarks (AgentDojo, InjecAgent, τ-bench) do not force. `sp_stochastic_boundary_identifiability`'s cross-condition claim (`rq_cross_model_ranking_stability`) specifically needs a workload where a pinned constraint must re-survive *more than one* compaction event to be a meaningful test of the durability asymmetry this paper is built around — a single-compaction task cannot distinguish 'survived once' from 'reliably re-wins the retention competition every time.'"
- `changes_made`: gave LongMemEval/LoCoMo's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the five variant names appear only in Stage 5, as intended).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_violation_oracle_definition.source_limitation_ids = ["lim_guidedbench_no_persistence_oracle"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis (mechanism tier) or the Stage 3 `verify_as_hypothesis`-flagged limitation text (framing tier) ✓.
4. **Output coverage** — Stage 1's three outputs (break-through curves, boundary scalars, cost ratio) are each reachable: curves/boundary via `sp_strength_commensurability` + `sp_violation_oracle_definition` + `sp_stochastic_boundary_identifiability`; cost ratio via `sp_cost_currency_commensurability`; the structural differentiation among variants via `sp_lossy_compaction_tradeoff` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs and exactly 1 framing-tier RQ (traced to the one Stage-3 limitation flagged `verify_as_hypothesis`).

**What was hardest:** unlike a typical run, the recurring tension was not filling gaps in a thin seed but **resisting the temptation to just transcribe `paper.md`'s already-finished Step 5/6/8/9 verbatim** without re-deriving them through this schema's own discipline. The schema's demands surfaced two things `paper.md` had implicitly handled but never stated as a first-class check: (a) the cost-ratio-is-not-redundant-with-the-boundary argument (Stage 2), which `paper.md` assumes throughout but never argues for explicitly, and (b) the single-axis-normalization vs. cross-actor-currency distinction (Stage 4), which `paper.md`'s C2/C4 split already respects structurally but doesn't explain in prose. Both are now explicit in the confirmed outputs above rather than left implicit in the pre-registered spec.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

Revision pass over the review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists). Each review finding was checked against the current deliverables for status (applied / logged-resolved / OPEN); OPEN items were folded in below. This section is an append-only record — no prior round was rewritten.

- **stage_review.md → Stage 2 REVISE (nearest-neighbor sentence naming TensorTrust/LightMem)** — already applied in `paper_draft.md`/`.tex` (Related Work opening + Introduction). No change needed this pass.
- **stage_review.md → Stage 4 REVISE (Falsification condition line on all six RQ subsections)** — already applied in both `paper_draft.md` and `paper_draft.tex`. No change needed this pass.
- **stage_review.md → Phase-A item 2 (reference-cache integrity; residual risk flagged as OPEN "before Phase E is next touched")** — was OPEN. `paper_draft.md`/`.tex` Related Work + Introduction still cited the ten unverified keys (ChatInject, ThreatSnapshots, SlotGCG, TAO-Attack, GCG, GuidedBench, TensorTrust, COMI, InfoChannel/companion-channel view, LightMem) as citable sources, whereas `paper.md` Step 5 and `digest.md` N3 already carry a provenance caveat. **Applied:** mirrored the `paper.md` Step-5 caveat into a "Citation-provenance caveat (pending re-harvest)" note at the head of the Related Work section in **both** `paper_draft.md` and `paper_draft.tex`, marking the ten names as provisional attack/defense *mechanism* references pending a targeted re-harvest, not finally-verified citations and not numerical baselines. Re-harvest itself remains out of environment scope (none of the ten OpenReview IDs appear in the 150-candidate harvest); the caveat closes the `stale_claim_after_verdict` gate exposure for the draft prose.
- **stage_review.md → Phase-A item 6 (oracle R2 validation plan; κ raised 0.6→0.7)** — `paper.md` and `paper_draft.md` RQ3 already ran at κ ≥ 0.7 with the full 5-step R2 setup, but **`paper_draft.tex` RQ3 was still at κ ≥ 0.6 with the old short setup** — a `.md`/`.tex` desync. **Applied:** updated `paper_draft.tex` RQ3 Setup (full R2 grounding: spec-grounded categories, ~50-case calibration slice, ≥2-rater ~200-case audit, confusion-structure check), Expected outcome (κ ≥ 0.7, no systematic collapse), and Falsification condition (κ < 0.7 or systematic collapse even at κ ≥ 0.7) to match `paper_draft.md`. Recompiled `paper_draft.pdf` (13 pages, clean except cosmetic overfull-hbox warnings).
- **experiment_design.md RQ3 verbatim hypothesis retains κ ≥ 0.6** — rejected as a change target (not a defect): the Stage-5 target hypothesis is quoted byte-verbatim by design, with an explicit "Known open item" note directing execution at the operational κ ≥ 0.7 bar. Left untouched to preserve the verbatim-hypothesis contract.
- **taste_audit.md (🟢, no conditions fired)** — no findings to apply; verdict is a clean pass on all three checks. Nothing to fold in.

**Cross-deliverable consistency re-check (paper_draft.md ↔ experiment_design.md ↔ paper_draft.tex):** RQ count 6 (RQ0–RQ5) matches across all three; effect floors match — cost ratio ≥ 2× (RQ4), Kendall τ ≥ 0.6 (RQ5), McFadden pseudo-R² ≥ 0.3 with BT50 CI ≤ 25% of range (RQ2), benign break-through Wilson upper bound < 0.20 (RQ0), and the operational oracle bar κ ≥ 0.7 (RQ3) now agree in all three files after the `.tex` fix above.
