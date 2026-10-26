> Extracted verbatim from `pipeline.md` (the `auto-research-discussion` Stage 1-6 critic/refiner transcript that fed `paper.md`'s and `paper_draft.md`'s construction). Moved into its own file per the updated skill's "Final deliverables" spec -- see `pipeline.md`'s Phase Log for everything that happened after this trace (taste audit, stage review, bibliography wiring, compile), and `experiment_design.md` for Stage 6 rendered as a standalone protocol.

# Auto-Research-Discussion Run — B5.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B5.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (a full pre-registered spec with fallback clauses already exists), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure how much bargaining surplus a weak-capability LLM agent representing a principal loses to a strong-capability adversary as the capability gap widens, and test whether restricting the weak agent's action space to schema-validated structured offers (deleting its free-text channel) protects it.
- **Apparent inputs:** a capability ladder of LLMs playable as either the weak principal's representative or the strong adversary; bilateral multi-issue bargaining game instances with known private valuations and a closed-form Pareto frontier; an action-space condition (structured-offer-only vs. free-text) assigned to the weak agent.
- **Apparent outputs:** per-episode outcome and normalized surplus-loss reading against a computable fair reference; a surplus-loss-vs-capability-gap scaling estimate; a causal verdict on whether the action-space constraint changes surplus loss.
- **Closest research areas:** scalable-oversight scaling laws for weak-vs-strong adversarial games (`ScalingLawsOversight`); weak-to-strong generalization (`WeakToStrong`); AI-control protocol-level restriction of the untrusted/weak party (`AIControl`, `ControlTax`); Bayesian strategic persuasion (`StrategicPersuasion`); negotiation-dialogue foundations (Lewis et al. 2017 Deal-or-No-Deal; GLEE).
- **In scope:** measuring existing prompted LLM agents' bargaining behavior under a controlled, manipulated capability gradient plus an action-space intervention, in sandboxable bilateral bargaining with a computable reference split. **Out of scope:** training or fine-tuning new agents; many-to-many markets with partner choice; live/non-sandboxable deployments; repeated-relationship reputation effects (that's a different topic in this same parent group).
- **Confidence: high.** Unlike a typical autoclaude repo scan, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` N0–N12 + `paper.md` Steps 0–9) that already cross-references its own challenges (C1–C4), mechanisms (M1–M5), contributions (CO1–CO4), and research questions (RQ1, RQ2a/b, RQ_INF_3) — and already ran its own asymmetry/taste self-check at `paper.md` Step 0/3. Reconstruction risk is low; as with the B5.5 exemplar, the risk is *redundancy* with `paper.md`'s own Step 6, which is why stages 5/6 below are framed as validating the **measurement instrument's properties** (does the dual gap measure agree with itself, does the harness read zero at zero gap) alongside the paper's headline causal claims, not as re-deriving `paper.md`'s hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a weak-capability LLM agent negotiating on behalf of a principal against a strong-capability adversary in bilateral multi-issue bargaining, and given a manipulable constraint on the weak agent's action space (schema-validated structured offers vs. unrestricted free text), determine how the weak agent's surplus loss relative to a computable fair reference scales with the capability gap between the two agents, and whether the action-space constraint changes that loss.
- `input`: (1) a capability ladder of LLM agents, each playable as either the weak principal's representative or the strong adversary, with the capability gap between any directed pair quantified two ways — an exogenous general-capability score delta, and an endogenous negotiation-specific Elo fit from round-robin play; (2) bargaining game instances drawn from established game families, each with known private valuations, reservation values, and a closed-form Pareto frontier; (3) an action-space condition assigned to the weak agent: structured-offer-only (one schema-validated JSON object per turn, no natural-language field) or free-text (the same offer object plus an unrestricted message).
- `output`: (1) a per-episode outcome record (offers, messages, agreement/impasse, realized split); (2) a normalized surplus-loss reading for the weak side against a computable fair reference; (3) a surplus-loss-vs-capability-gap scaling estimate, per action-space condition; (4) a causal verdict on whether the action-space constraint changes the weak side's surplus loss relative to free text at matched capability gap, including whether it lets a lower tier substitute for a higher one, and — except for a bilateral both-constrained control cell that isolates the adversary's own channel — the constraint is applied to the weak side only.
- `constraints`: every game instance must admit a closed-form fair reference computable from its known parameters even though valuations are private during play; every episode must terminate in agreement or impasse within a bounded number of rounds.
- `objective`: a surplus-loss-vs-capability-gap scaling claim is accepted only if it holds under a computable fair reference and the weak agent's loss causally reduces when the action-space constraint is applied.
- `study_type`: `empirical` — stated explicitly: digest N12 classifies this as a controlled behavioral measurement study over already-trained LLMs, not a new system or theorem, and the seed's own core question ("剩余损失如何随能力差距缩放") is a characterization question, not a proposed fix being pitted against baselines.

**critique:**
- summary: Grounded and traceable to the digest, but the objective has a real evaluability gap, and one clause in `output` smuggles a stage-6 experimental-design detail into the problem statement.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "'causally reduces' names no threshold, significance level, or effect size — as written, any nonzero directional shift, however noisy, would satisfy the objective. Digest N8's own analysis plan already commits to a Holm-corrected α=0.05 and a stated point-estimate floor (≥0.05 normalized-loss units) for exactly this claim (paper.md RQ2a) — the objective should name that standard rather than leaving 'causally' undefined. Separately, paper.md's own A3 flags that the two gap measures (exogenous score delta, endogenous negotiation Elo) may disagree in sign — the objective is silent on what happens then, which is the same kind of reference-ambiguity gap the B5.5 run's critic caught in its own Stage 1."}`
  - `{severity: minor, field: "output", anti_pattern: "later_stage_content", comment: "The final clause of output (4) — 'except for a bilateral both-constrained control cell that isolates the adversary's own channel' — is a stage-6 baseline-design decision, not a problem-setting output. It should be cut from the problem definition and left for the experiment-design stage, where it already belongs (paper.md's B-alt control)."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content the digest/paper.md already supplies — no new content needed).

### Refiner pass

- `objective` (refined): "A surplus-loss-vs-capability-gap scaling claim is accepted only if it holds under a computable fair reference (primary: the Nash bargaining solution; checked for sign-agreement against an equal split and the Kalai–Smorodinsky point) **and** only if the two capability-gap measures agree on the sign of the scaling relationship — disagreement between the two measures is reported as evidence of a projection-dependent gap axis, not resolved by preferring one measure over the other. A causal verdict on the action-space constraint is accepted only at a pre-specified standard: a Holm-corrected significance level of α = 0.05 together with a point-estimate reduction in normalized surplus loss of at least 0.05 units at matched capability gap."
- `output` (refined): trimmed clause (4) to: "a causal verdict on whether the action-space constraint changes the weak side's surplus loss relative to free text at matched capability gap, including whether it lets a lower capability tier substitute for a higher one." (control-cell design detail removed — it belongs to Stage 6.)
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Directed model pair (w, s): w = weak principal's agent, s = strong adversary. Game instance g with private valuations, reservation values r_w, r_s, deadline T. Action-space condition c ∈ {structured, free} applied to w. Episode e yields outcome o_e = (agree?, realized split). Normalized surplus loss L = (u_ref − u_realized)/(u_ref − r_w), with impasse scored at L=1. Capability gap Δ_a (exogenous score delta) and Δ_b (endogenous negotiation Elo delta), both computed per directed pair. Determine dL/dΔ per condition c, and whether E[L | c=structured] < E[L | c=free] at matched Δ for the same (w,s)."
- `changes_made`: tightened `objective`'s evaluability condition with a stated threshold and an explicit disagreement-reporting rule; removed a stage-6 design detail from `output`; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: As LLM agents are increasingly delegated bilateral negotiation on a principal's behalf, a principal fielding a weaker or cheaper model may face a counterparty running a stronger one — and whether restricting the weak agent's own expressive channel protects it, the way protocol-level restriction already protects weak/trusted parties in AI-control settings, has never been measured for bargaining specifically.
- `why_it_matters`: Adjacent literatures already establish two separate facts that this problem sits between but that neither one, alone or combined, actually answers: scalable-oversight work shows weak-vs-strong adversarial interactions have systematic, capability-dependent failure rates measured by win/loss outcomes or supervision-label quality (never a continuous economic outcome); and AI-control work shows that restricting a party's protocol-level channel can protect a principal, but only ever by constraining the *strong, untrusted* side or the surrounding protocol — never by restricting the *weak* party's own channel as self-protection, and never in a bargaining setting with a surplus split to score. If the capability gap converts into surplus loss at a rate nobody has measured, and if a near-zero-cost self-restriction on the weak side turns out to help (or, just as informatively, turns out not to), that is directly actionable for anyone deploying a weaker agent against an unknown or stronger counterparty.
- `who_cares`: Principals who deploy cost- or latency-constrained (hence weaker) negotiation agents against unknown-capability counterparties; designers of agent-to-agent commerce protocols deciding whether to mandate structured-offer schemas as a default safety rail; researchers asking whether AI-control's "restrict the untrusted side" finding has an analogue when it's the *trusted, weak* side that gets restricted instead.
- `evidence`: `[ScalingLawsOversight, OpenReview:u1j6RqH8nM]` fits a scaling law linking general capability to win-rate in weak-vs-strong oversight games — establishing that capability-gap-dependent outcomes are real and fittable, but never in a bargaining setting with a surplus to lose; `[AIControl, OpenReview:KviM5k8pcP]` and `[ControlTax, OpenReview:BpyR6Wkl1c]` show that protocol-level restriction protects a weak/trusted principal against a strong/untrusted counterparty — but always by restricting the strong side or the audit protocol, never the weak side's own channel; `[StrategicPersuasion, OpenReview:aTCXvJKnkE]` operationalizes exactly the free-text rhetorical channel a structured-offer constraint would delete, but only for a fixed receiver, never varying receiver capability relative to sender. None of the three combines a controlled capability gradient, a continuous surplus-loss outcome, and a self-restriction test on the weak side (digest N4's affects_works mapping) — itself evidence the combination is open.

**critique:**
- summary: The motivation is evidence-grounded and each citation earns its place, but the `why_it_matters` argument risks reading as "these two literatures haven't been connected" rather than leading with the mechanism — and it doesn't yet explain why a *scaling* relationship, not a single yes/no exploitation check, is the thing worth measuring.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a scaling estimate — a claim about how loss varies with gap, not merely whether it is nonzero at one gap level. As drafted, why_it_matters argues the exploitation-exists question and the constraint-helps question, but never argues why the gap-dependence (the slope, not a point estimate) specifically matters for a deployment decision. Without that, a reader could ask 'why not just check whether the weak side loses surplus once, at whatever gap I happen to face' — which is a real, unaddressed gap, structurally identical to the one the B5.5 run's critic caught in its own Stage 2."}`
  - `{severity: minor, field: "summary", anti_pattern: "bridge-adjacent framing risk (flagged for the taste audit, not a stages.md anti-pattern by name)", comment: "'...the way protocol-level restriction already protects weak/trusted parties in AI-control settings...' is one edit away from a 'these two things haven't been connected, so let's connect them' framing. paper.md's own Step 3 self-audit already flagged this exact risk and corrected toward leading with the channel-gating mechanism rather than the AI-control analogy. Carry that correction into this stage's confirmed output rather than re-introducing the risk here."}`
- decision: `move_to_refiner` (both are wording/coverage fixes using content already in the digest and paper.md — no new evidence needed).

### Refiner pass

- `summary` (refined, mechanism-first per paper.md Step 3's correction): "The surplus a stronger negotiator extracts from a weaker one is not fixed by the capability gap alone but by how much of that gap can pass through the action-space channel the bargaining protocol leaves open to the weaker party — so narrowing that channel could in principle deny the stronger side the surface through which its advantage converts into surplus, without changing either agent's underlying capability. Whether this channel-gating actually holds for present-day LLM bargainers, and how large the effect is relative to the raw capability gap, has never been measured."
- `why_it_matters` (extended with the scaling-specific argument): "...critically, a single-gap-level audit cannot answer the deployment question that actually matters: at what capability gap does surplus loss become unacceptable, and does that threshold move if the weak side is restricted to structured offers? Only a scaling estimate — loss as a function of gap, per action-space condition — lets a principal set an operating threshold (e.g., 'deploy the cost-efficient tier only if the gap to the likely counterparty stays below X, or only if structured offers are mandated'); a one-off exploitation check at whatever gap happens to be tested cannot license that kind of decision rule."
- `changes_made`: reframed `summary` to open on the channel-gating mechanism rather than the AI-control analogy (removing the bridge-adjacent phrasing the critic flagged); added the scaling-vs-single-audit coverage argument to `why_it_matters`.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All items below are **specific (deep) tier** — digest N3/N4 already engaged each at the approach-plus-limitation level; two entries (`GLEE`, `DealOrNoDeal`) are canonical, non-corpus sources cited by a corpus paper's own motivation text, retained per digest N3's own disclosed confidence note.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation → sub-problem it will motivate / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (`lim_*`) |
|---|---|---|---|
| `rw_scalinglaws` | Anon., ScalingLawsOversight (OpenReview:u1j6RqH8nM) | **true** | `lim_no_continuous_economic_outcome` — scores weak-vs-strong adversarial games only by oversight win-rate/Elo, never a continuous economic outcome such as bargaining surplus against a computable reference. |
| `rw_weaktostrong` | Anon., WeakToStrong (OpenReview:ghNRg2mEgN) | false (training setting, not adversarial bargaining) | `lim_no_continuous_economic_outcome` (shared) — capability gap as a controlled variable, but measured via label-recovery in a finetuning pipeline, not an adversarial economic interaction. |
| `rw_glee` | Shapira et al., GLEE (arXiv:2410.05254) | false (dataset/game-family source, not a comparison target) | `lim_no_capability_gap_as_iv` — standardizes bargaining game configurations but evaluates whichever models are plugged in at whatever capability they happen to have; capability gap is not a controlled independent variable. |
| `rw_dond` | Lewis et al., Deal-or-No-Deal (arXiv:1706.05125) | false (canonical scenario/value-function source) | `lim_no_capability_gap_as_iv` (shared) — canonical multi-issue division task and self-play agents, same gap. |
| `rw_aicontrol` | Anon., AIControl (OpenReview:KviM5k8pcP) | false (different domain: safety monitoring, not bargaining) | `lim_wrong_side_restricted` — protects a weak/trusted principal by restricting the *strong, untrusted* side or the surrounding audit protocol, never the weak party's own channel as self-protection. |
| `rw_controltax` | Anon., ControlTax (OpenReview:BpyR6Wkl1c) | false | `lim_wrong_side_restricted` (shared) — prices the protective protocol's overhead but the restriction is still on the untrusted side. |
| `rw_stratpersuasion` | Anon., StrategicPersuasion (OpenReview:aTCXvJKnkE) | false (one-shot sender-receiver, no bargaining surplus) | `lim_fixed_receiver_no_defenses` — operationalizes the free-text persuasive channel but only for a fixed receiver; capability is never varied relative to sender, and the receiver has no structural defense to test. |
| `rw_aria` | Anon., ARIA (OpenReview:eumRwpgdMU) | false (training-time credit assignment, not deployment-time exploitability) | `lim_training_time_not_deployment_time` — treats the free-form action space as a training-time variance problem to compress away, never asks whether exposing it makes an already-capable agent exploitable, and never compares constrained vs. free-form action spaces under adversarial pressure. |
| `rw_competeai` | Anon., CompeteAI (OpenReview:wGtzp4ZT1n) | false (homogeneous-capability market, no reference split) | `lim_no_reference_split` — studies competition among roughly homogeneous-capability agents; capability asymmetry is neither controlled nor measured, and without a closed-form reference no per-interaction surplus loss is attributable to exploitation. |
| `rw_capa` | Anon., GreatModelsThinkAlike / CAPA (OpenReview:3Z827FtMNe) | false (judge/supervision setting, not bargaining) | `lim_pair_similarity_confound` — shows weak-to-strong outcomes are modulated by supervisor-student *functional similarity*, warning that a single-axis capability-gap study risks confounding gap with pair similarity — but only diagnoses this for judging/supervision, not adversarial bargaining. |

**critique:**
- summary: Every limitation is specific and traceable, and the table already distinguishes methodological precedent from domain fit — but one `is_potential_baseline: true` label needs the same scrutiny the B5.5 run's critic applied to SOTOPIA.
- comments:
  - `{severity: major, field: "specific_related_works[rw_scalinglaws].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "ScalingLawsOversight's I/O framing is oversight win-rate in a Guard-vs-Houdini game — genuinely different from this paper's I/O (a continuous bargaining-surplus split against a computable Pareto reference). Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying its own reported win-rate numbers are being compared against, which they are not; what's actually reused is its role-specific Elo-estimation *technique* (digest M1's citation of it), not its results."}`
- decision: `move_to_refiner` (a wording-precision fix on one field, not a structural one — the Elo-estimation technique is still legitimately reused).

### Refiner pass

- `rw_scalinglaws.is_potential_baseline` changed to `false`, with an added note: "Not a baseline in the beat-a-number sense — its own reported oversight win-rates are not compared against. Its **role-specific Elo-estimation technique** (fitting a scaling law from round-robin play) is borrowed as a *method precedent* for this paper's endogenous negotiation-Elo gap measure (M1), independent of its own domain or published findings."
- `changes_made`: corrected the baseline label and clarified the technique-vs-results distinction, mirroring the B5.5 SOTOPIA fix.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a distinct stage-6 framing-tier RQ — every candidate (e.g., `lim_pair_similarity_confound`) restates a facet of this paper's own core question (already covered end-to-end as mechanism-tier RQs in Stage 6, specifically the dual-gap-measure agreement check). Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3** (10 related works, 7 named limitations — `lim_no_continuous_economic_outcome` is used to motivate the overall Stage 1/2 gap rather than a single Stage 4 sub-problem, consistent with how the B5.5 run treated one of its own N4-equivalent items).

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4):

- **`sp_gap_construct`** — *description:* Define and measure a capability gap between two LLM agents that is meaningful enough to regress surplus loss against, given that capability is not a single scalar. *why_it_is_a_problem:* if the gap measure is arbitrary or confounded, any scaling claim is an artifact of the projection chosen rather than a fact about capability itself. *technical_challenge:* an exogenous general-capability delta and an endogenous negotiation-specific Elo can disagree on both magnitude and ordering for the same model pair, and functional similarity between two same-tier models can itself modulate outcomes independent of any capability difference — so "the gap" is not observationally unique. *source_limitation_ids:* `["lim_pair_similarity_confound", "lim_no_capability_gap_as_iv"]`.
- **`sp_reference_and_game_design`** — *description:* Build a bargaining environment complex enough to be non-trivial for LLM agents yet simple enough to admit a closed-form fair-reference split for every instance. *why_it_is_a_problem:* without a computable reference, an observed split cannot be scored as "lost surplus" at all — it is just a number. *technical_challenge:* the two design requirements (game complexity, reference computability) pull in different directions, and even a computable reference is a construct choice (Nash bargaining vs. equal split vs. Kalai–Smorodinsky) that could itself drive a conclusion. *source_limitation_ids:* `["lim_no_reference_split"]`.
- **`sp_net_effect_of_restriction`** — *description:* Determine whether restricting the weak agent's action space to structured offers only helps, hurts, or has no effect on its surplus loss. *why_it_is_a_problem:* restriction removes both the weak agent's exposure to rhetorical exploitation and its own legitimate self-defense moves (framing, stalling, commitment language), so the net sign is not decidable a priori — this is the seed's own central, explicitly counter-intuitive question. *technical_challenge:* isolating a genuine causal effect requires holding everything else fixed across conditions (adversary behavior, game instance, capability tier) while varying only the weak agent's channel — and a positive finding at one tier doesn't establish whether restriction can substitute for a full tier of capability, which is a distinct, harder comparison. *source_limitation_ids:* `["lim_wrong_side_restricted", "lim_training_time_not_deployment_time"]`.
- **`sp_channel_attribution`** — *description:* Attribute any observed surplus loss to substantive bargaining skill (offer timing, concession strategy, value inference) versus the strong adversary's rhetorical/persuasive tactics in free text. *why_it_is_a_problem:* a between-condition loss difference alone tells you the free-text channel matters in aggregate, but not how much of the *mechanism* is rhetorical exploitation versus better substantive play — which changes what kind of protective intervention would actually generalize. *technical_challenge:* transcripts alone cannot cleanly separate the two channels without independent instrumentation, since a stronger model plausibly out-negotiates on substance *and* out-persuades on rhetoric simultaneously in the same free-text turn. *source_limitation_ids:* `["lim_fixed_receiver_no_defenses"]`.

**critique:**
- summary: Coverage checks out (solving all four would jointly deliver stage 1's objective), and each sub-problem traces to a real limitation rather than the `__novel__` sentinel — but two sub-problems risk reading as the same underlying issue stated twice.
- comments:
  - `{severity: minor, field: "sp_net_effect_of_restriction / sp_channel_attribution", anti_pattern: "overlap", comment: "Both concern the free-text channel and could be read as one problem twice. They are genuinely distinct — one asks whether restriction changes the *outcome* (does loss go down), the other asks *why* any observed change happens (which channel does the loss flow through) — but the descriptions don't make that distinction sharp enough. A reviewer could ask why RQ2's causal contrast and RQ_INF_3's channel attribution aren't the same experiment."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_net_effect_of_restriction.technical_challenge` sharpened to end with: "...this is an **outcome-level causal** question — does the constraint change the number — answerable from the same-model and cross-tier contrasts alone, without needing to know *why*."
- `sp_channel_attribution.technical_challenge` sharpened to end with: "...this is a **mechanism-decomposition** question distinct from the outcome-level contrast above — even if restriction is confirmed to lower loss, that alone does not say whether it worked by deleting a rhetorical channel or by simplifying the weak agent's own decision process, and only a within-condition channel attribution (not the between-condition contrast) can distinguish those."
- `changes_made`: made the outcome-vs-mechanism distinction explicit in both `technical_challenge` fields, so the two sub-problems no longer read as one restated.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; all traced to real Stage 3 limitations, no `__novel__` sentinel needed — this seed's literature grounding is dense enough that every decisive component maps to a specific gap in a specific cited work).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_gap_quantification_and_scaling`** → targets `sp_gap_construct`. *proposed_approach:* Quantify the capability gap between every directed model pair two ways — an exogenous general-capability score delta (fixed before any bargaining) and an endogenous negotiation-specific Elo fit from round-robin free-text self-play, following the role-specific Elo-estimation technique of `rw_scalinglaws`; regress normalized surplus loss on each gap measure via a mixed-effects model with random intercepts for game instance and model pair. *key_insight:* neither gap measure alone is trustworthy, but reporting both and requiring sign-agreement turns the "which projection of capability" problem into an explicit, checkable robustness condition rather than a hidden modeling choice. *hypotheses:* ["In the free-text condition, normalized surplus loss for the weak agent increases with capability gap — a significantly positive mixed-effects slope (two-sided Wald p < 0.05) under both gap measures, with the same sign for both, and a monotone trend across gap levels (Spearman ρ > 0)."]
- **`m_bargaining_harness`** → targets `sp_reference_and_game_design`. *proposed_approach:* Instantiate a parameterized multi-issue alternating-offers environment from two established game families plus one synthetic suite, computing the Pareto frontier and three reference splits (Nash bargaining, equal split, Kalai–Smorodinsky) in closed form for every instance; run zero-gap self-play controls (weak-vs-weak, strong-vs-strong) as an existence check on the metric itself. *key_insight:* a metric that isn't validated against its own null condition can't be trusted at nonzero gap either — if surplus loss is already large when there is no capability gap to explain it, the metric (not the phenomenon) is what's broken. *hypotheses:* ["At zero capability gap (self-play), mean normalized surplus loss is close to zero (|E[L | Δ=0]| ≤ 0.05) under the primary Nash-bargaining reference — validating that the harness measures gap-driven exploitation rather than a mechanically biased game or an arbitrary reference choice."]
- **`m_structured_offer_constraint`** → targets `sp_net_effect_of_restriction`. *proposed_approach:* In the constrained condition, the weak agent's entire turn is a single schema-validated JSON object (accept/reject/counteroffer plus an allocation), with no natural-language field transmitted and up to two resamples on parse failure; compare against a matched free-text condition (the same offer object plus an unrestricted message) at the same capability gap, and separately compare a constrained weak agent at tier t against an unconstrained weak agent at tier t+1 facing the same adversary. *key_insight:* the constraint is a single, minimal deletion (removing one field from the weak agent's turn) rather than a new algorithm — which is exactly what makes its effect, if any, attributable to channel removal rather than to some more elaborate redesign. *hypotheses:* ["(H2a) Restricting the weak agent to structured offers produces lower normalized surplus loss than free text at matched capability gap for the same model pair (Holm-corrected p < 0.05, point-estimate reduction ≥ 0.05 units), with the reduction growing as the gap widens (positive condition×gap interaction).", "(H2b) A constrained weak agent at capability tier t incurs surplus loss no greater than an unconstrained weak agent at tier t+1 against the same adversary, for at least one adjacent tier pair (one-sided non-inferiority test, α = 0.05) — i.e., the constraint can substitute for at least one tier of capability."]
- **`m_channel_attribution`** → targets `sp_channel_attribution`. *proposed_approach:* Compare the mixed-effects gap slope between the free-text and structured conditions to compute how much of the slope the structured condition removes; separately, an LLM judge tags each adversary free-text message against a closed tactic taxonomy (anchoring, misrepresentation of value, false deadline/commitment, flattery/pressure), with 10% human double-coding (target Cohen's κ ≥ 0.7), and relates tactic incidence to per-episode loss; a both-constrained control cell (adversary also schema-restricted) provides a bilateral check on whether any residual gap-slope in the structured condition is substantive rather than rhetorical. *key_insight:* the between-condition slope removal gives a causal (if coarse) bound on the rhetorical channel's contribution, while the tactic-incidence correlation gives a finer-grained (but correlational) account of which specific tactics are doing the work — the two readings are deliberately kept at different evidence strengths rather than conflated into one number. *hypotheses:* ["(exploratory) The reduction in gap slope from free text to structured accounts for more than half of the free-text slope, and adversary tactic incidence correlates positively with per-episode surplus loss (p < 0.05) — indicating exploitation flows predominantly through the rhetorical channel rather than substantive offer strategy."]

**critique:**
- summary: Every method has a real, minimal mechanism (no goal-restatement — the structured-offer method in particular is a one-field deletion, not a new system), and every hypothesis states a threshold — but `m_structured_offer_constraint` carries two headline claims and needs the same one-line justification the B5.5 run required for its own two-hypothesis method.
- comments:
  - `{severity: minor, field: "m_structured_offer_constraint.hypotheses", anti_pattern: null, comment: "H2a (same-model contrast) and H2b (cross-tier substitution) are this paper's two most central claims, both riding on one method. Worth stating explicitly why this is one intervention with two readouts, not scope creep bundled into a single method entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_structured_offer_constraint.key_insight` extended: "...one intervention — deleting the weak agent's free-text field — produces two distinct, separately falsifiable estimands from the same factorial design: the within-model condition contrast (H2a, does restriction help the same model against the same adversary) and the cross-tier substitution contrast (H2b, can restriction close a capability-tier gap) — one intervention, two readouts, not two mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly, mirroring the B5.5 run's `m_matched_conditions` fix.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **5 hypotheses total** (1 + 1 + 2 + 1 across the four methods respectively), deliberately mixing instrument-validity claims (gap-measure sign-agreement, zero-gap near-null loss) with the study's headline causal claims (same-model contrast, cross-tier substitution) and one exploratory mechanism claim (channel attribution) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 5 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`; `m_structured_offer_constraint`'s two hypotheses each get their own RQ).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators only.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GLEE bargaining game configurations (Shapira et al., 2024) — *justification:* a parameterized economic-game benchmark; used as the primary game family because its parameterization gives direct, controlled sweeps over surplus size and valuation asymmetry, which the pilot (Stage 1 harness build-out) needs to compute closed-form references cheaply before scaling up.
- Deal-or-No-Deal multi-issue division scenarios (Lewis et al., 2017) — *justification:* real multi-issue value functions with private per-item valuations; used to test whether the surplus-loss scaling relationship (RQ2) generalizes beyond GLEE's parameterized configurations to a second, independently designed game family.
- (draft initially listed the synthetic divide-the-pie suite with justification only "generated, for controlled asymmetry" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Zero-gap self-play (weak-vs-weak, strong-vs-strong) — the existence check for the metric itself (RQ1 below).
- Scripted Boulware / linear-conceder opponents — a non-adaptive, memoryless capability floor; if the gap-loss trend appears even against a scripted opponent, "the strong adversary's capability specifically" is refuted in favor of generic concession-strength differences.
- Both-constrained control cell (adversary also schema-restricted) — isolates whether any residual structured-condition gap-slope is substantive rather than rhetorical (feeds RQ5's channel attribution).

`research_questions` (5, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_gap_validity` | `sp_reference_and_game_design` | "At zero capability gap (self-play), mean normalized surplus loss is close to zero (\|E[L \| Δ=0]\| ≤ 0.05) under the primary Nash-bargaining reference — validating that the harness measures gap-driven exploitation rather than a mechanically biased game or an arbitrary reference choice." |
| `rq_scaling` | `sp_gap_construct` | "In the free-text condition, normalized surplus loss for the weak agent increases with capability gap — a significantly positive mixed-effects slope (two-sided Wald p < 0.05) under both gap measures, with the same sign for both, and a monotone trend across gap levels (Spearman ρ > 0)." |
| `rq_same_model_contrast` | `sp_net_effect_of_restriction` | "(H2a) Restricting the weak agent to structured offers produces lower normalized surplus loss than free text at matched capability gap for the same model pair (Holm-corrected p < 0.05, point-estimate reduction ≥ 0.05 units), with the reduction growing as the gap widens (positive condition×gap interaction)." |
| `rq_cross_tier_substitution` | `sp_net_effect_of_restriction` | "(H2b) A constrained weak agent at capability tier t incurs surplus loss no greater than an unconstrained weak agent at tier t+1 against the same adversary, for at least one adjacent tier pair (one-sided non-inferiority test, α = 0.05) — i.e., the constraint can substitute for at least one tier of capability." |
| `rq_channel_attribution` | `sp_channel_attribution` | "(exploratory) The reduction in gap slope from free text to structured accounts for more than half of the free-text slope, and adversary tactic incidence correlates positively with per-episode surplus loss (p < 0.05) — indicating exploitation flows predominantly through the rhetorical channel rather than substantive offer strategy." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 6 numbers as authored design targets, not fabricated results — including its explicit per-RQ fallback clauses, which become the Falsification condition lines.)

**critique:**
- summary: Tier accounting is clean, every RQ traces to a verbatim hypothesis, and the baselines are each informative (none is a strawman) — but the synthetic dataset's justification is a provenance note rather than a reason tied to a specific RQ.
- comments:
  - `{severity: major, field: "datasets[synthetic divide-the-pie suite]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'generated, for controlled asymmetry' doesn't say which RQ needs controlled asymmetry or why a generated suite is required for it — this is the same gap the B5.5 run's critic caught on its GLEE entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "Synthetic 3-issue divide-the-pie suite (generated) — *justification:* lets valuation asymmetry be swept as a controlled, continuous parameter independent of whatever asymmetry distribution GLEE's or Deal-or-No-Deal's fixed scenario pools happen to contain; specifically needed to test whether `rq_scaling`'s gap-measure sign-agreement (or disagreement) concentrates at high-asymmetry instances as a designed sweep, rather than only being observed post hoc across two fixed corpora."
- `changes_made`: gave the synthetic suite's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_matters`/`why_it_is_a_problem` fields name no technique (the structured-offer *intervention* itself is correctly confined to Stage 5, appearing in Stage 1 only as a manipulated input variable, matching how the B5.5 run handled its own reputation-visibility toggle).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` / `lim_*` stable stage-to-stage (one label correction — `rw_scalinglaws.is_potential_baseline` — was a field-value fix, not an ID rename).
3. **Reference integrity** — every `source_limitation_ids` in Stage 4 ∈ Stage 3's `lim_*` set ✓ (`lim_no_continuous_economic_outcome` is the one Stage-3 limitation not tied to any single Stage-4 sub-problem; it is used instead to motivate the overall Stage 1/2 gap, exactly mirroring how the B5.5 run treated one of its own N4-equivalent items); every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` entry is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (episode record, surplus-loss reading, scaling estimate, causal verdict) are each reachable: the episode record and surplus-loss reading via `sp_reference_and_game_design` (the harness), the scaling estimate via `sp_gap_construct`, and the causal verdict via `sp_net_effect_of_restriction` (+ `sp_channel_attribution` for the mechanism behind it) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** as with the B5.5 run, the recurring tension was **not disagreement about facts** — the seed material (`paper.md`'s own Steps 0–9, including its pre-run fallback clauses) is unusually well-specified — but **scope discipline against the bridge-framing risk**: `paper.md`'s own Step 3 self-audit had already flagged that leaning on the AI-control analogy ("restriction protects the weak party, just like in AI control") risks a Bridge-Opportunity framing, and the Stage 2 critic round in this run independently re-derived the same concern before seeing that self-audit resolved, then applied the same channel-gating-first correction paper.md had already committed to. The second recurring tension was distinguishing outcome-level causal claims (does restriction change the number) from mechanism-level ones (why does it change), which produced the Stage 4 overlap flag between `sp_net_effect_of_restriction` and `sp_channel_attribution`.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: revision pass over all findings in `stage_review.md` and `taste_audit.md` (`design_review.md` does not exist for this topic). Every finding was re-verified against the current `paper_draft.md`/`.tex`, `experiment_design.md`, `paper.md`, `refs.bib`, and the compile log — not taken on faith from `pipeline.md`'s log. Result: **all 11 findings already applied; 0 open; nothing re-applied.** This section records the verification, per the revision-pass convention of appending rather than rewriting past rounds.

1. `stage_review.md` Stage 2 REVISE (missing nearest-neighbor sentence) → **already applied**: Related Work opens with the explicit nearest-neighbor sentence naming `AIControl` (phenomenon-closest), `ScalingLawsOversight` (method-closest), and `LanguageOfBargaining2023` (manipulated-variable-closest), each with a concede-and-differentiate delta — in `paper_draft.md` (Related Work ¶1) and `paper_draft.tex`.
2. `stage_review.md` Stage 4 REVISE (missing per-RQ falsification conditions) → **already applied**: all five RQ subsections carry an explicit **Falsification condition** line in `paper_draft.md`, `paper_draft.tex` (5 occurrences verified), and `experiment_design.md`.
3. `stage_review.md` Phase A item 2 (reference-cache integrity; `digest_path` for the 4 load-bearing back-filled N3 works) → **already applied**: logged RESOLVED in `pipeline.md` (pre-E/pre-G to-dos row) and independently re-verified in Phase G's pre-check against the actual digest files.
4. `stage_review.md` Phase A item 5 (H1 effect floor; H2b non-inferiority margin; A1–A6 explicit `consequence:` slots) → **already applied** in `paper.md` (H1 line 96 carries the ≥0.10-unit floor; H2b line 120 carries δ = 0.05; A-slots carry consequences, e.g. A5).
5. `stage_review.md` Phase A item 6 (R1 estimand sentence; 5-step R2 instrument validation; R3 confound ledger; thin-cell INCONCLUSIVE rule) → **already applied** in `paper.md`; the R2 sequence and thin-cell rule are mirrored in `experiment_design.md` (RQ5 Setup/Falsification; "Thin-cell rule" section) and the thin-cell rule in `paper_draft.md`/`.tex` Experimental Setup.
6. `stage_review.md` Phase A item 7 (add `LanguageOfBargaining2023` to draft Related Work; resolve arXiv:2601.04387 freshness flag) → **already applied**: Phase E row added the third nearest-neighbor; the freshness flag was resolved (2601.04387 confirmed not a method-twin) in the pre-E/pre-G RESOLVED row.
7. `stage_review.md` Phase G Item 1 (RQ2 missing ≥0.10 floor; RQ4 missing δ = 0.05 margin; thin-cell rule absent from prose; RQ3 missing B0-near-null caveat) → **already applied**: verified in `paper_draft.md` (RQ2/RQ4/Thin-cell/RQ3 note) and `paper_draft.tex` (lines 111, 140–142, 159, 166–168).
8. `stage_review.md` Phase G Item 2 (four `selected` cache entries absent from Related Work: `PrincipalLoyalty2606`, `Decepticon2512`, `TRAP2512`, `BEDA2512`) → **already applied**: all four are cited with accurate deltas in the strategic-communication and LLM-agent-economic-interaction paragraphs of both draft files.
9. `stage_review.md` Phase G Item 3 (central hypothesis stated in accomplished-fact voice in Abstract + first contribution bullet) → **already applied**: both now read "Our central claim, tested rather than assumed here…" / "…tested, not assumed, via the pre-registered contrasts below," in `.md` and `.tex`.
10. `stage_review.md` Phase G Item 4 [major] (zero `\cite`/`refs.bib` infrastructure) → **already applied** via the 2026-07-05 Phase F re-entry: `gen_refs_bib.py` script-generates `refs.bib` (18 entries from `selected` cache records); 21 `\citep` instances over 15 keys wired with `natbib`/`plainnat`; 15/15 bibitems resolve; compile log shows zero undefined citations.
11. `stage_review.md` Phase G artifact-sync note (`.tex`/`.pdf` mismatch pending Phase I) → **already applied**: Phase I recompile 2026-07-05 PASS (clean rebuild, 0 errors, 13 pages); `.tex` and `.pdf` timestamps match.
- `taste_audit.md` (both the original audit and the 2026-07-04 post-Phase-G re-audit) → **no action items**: 🟢 verdict twice, no REVISE/concern requiring a deliverable change.
- `design_review.md` → **does not exist** for this topic; nothing to enumerate.

**Cross-deliverable consistency check (performed this round, no mismatch found):** 5 RQs in both `experiment_design.md` and `paper_draft.md`; RQ1 gate |E[L|Δ=0]| ≤ 0.05 with ±0.02 estimation precision in both; RQ2 effect floor ≥ 0.10 normalized-loss units, d ≈ 0.4 at ~80% power in both; RQ3 reduction floor ≥ 0.05 units + Holm α = 0.05 + B0-near-null interpretive note in both; RQ4 non-inferiority margin δ = 0.05 in both; RQ5 >50% slope-removal ratio in both; thin-cell rule (<30 valid episodes/cell; >25% thin cells → test INCONCLUSIVE) in both. All five `target_hypothesis` fields in `experiment_design.md` verified verbatim against `paper.md` Step 6 (H1/H2a/H2b/H3) and `pipeline.md` Stage 5/6 (RQ1's `rq_gap_validity`) — text identical modulo markdown emphasis markup, no paraphrase. No file edits were needed; `paper_draft.tex` untouched this round, so no recompile was required (current `.pdf` is the Phase I 2026-07-05 build).
