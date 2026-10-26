# Discussion Trace — B1.6 (auto-research-discussion, Stages 1–6)

> Mode: **autoclaude** (self-play; Claude plays proposer, critic, and refiner).
> Source seed: `../README.md` (topic card, Chinese frontmatter + asymmetry
> statement) + `../digest.md` (N0–N12 reverse-digest, 857 lines). There is **no
> pre-registered `paper.md`** for this topic — the seed is less mature than
> B5.5's was, so the critic rounds are run at full strength and the formal
> problem definition, assumptions, and RQ-with-fallback machinery are derived
> here during the stages, not deferred to a spec that does not exist.
>
> **Anti-sycophancy discipline (autoclaude_mode.md Rules 1–3):** every student
> claim traces to a seed locator (README line or digest N-node); the teacher may
> attack the interpretation only with counter-evidence from the same material;
> at least one substantive `[major]` fires per stage. No `ignore_and_submit`
> override exists in this mode — a stage does not close over an open `[major]`.
> Round cap 5/stage; none hit.
>
> **Pipeline order:** this file → `taste_audit.md` (idea-level check on Stage 2+5)
> → `stage_review.md` (pengsida PASS/REVISE/STOP per stage, plus a Writing-stage
> check on the first assembled draft) → `paper_draft.md`/`.tex`/`.pdf`. REVISE
> findings from `stage_review.md` are folded into the `paper_draft.*` files;
> read that file for the reasoning behind each applied fix.

## Seed brief (autoclaude extra)

- **One-sentence description:** Measure whether an install-time **publisher-trust
  gate** (not a bare name-existence check) inserted into a multi-step LLM-agent
  trajectory blocks squatted-malicious skill installs without the usability
  collapse that every recommendation-time defense in the base study suffers, and
  how the *timing* of interception governs downstream task/security outcome and
  recovery cost.
- **Apparent inputs:** a skill registry snapshot carrying per-publisher trust
  tiers; a multi-step agent-trajectory harness embedding a recommend-then-install
  decision; a squatting adversary seeded from confirmed hallucinated-name
  recurrence; a probe set of legitimate skills from unverified publishers.
- **Apparent outputs:** per-episode compromise/rejection/task labels; a
  detection-lag (step index of first catch); a (compromise-block-rate,
  legitimate-reject-rate) operating point; recovery cost.
- **Closest research areas:** LLM tool/skill-use hallucination and supply-chain
  security (HallucSkills, arXiv:2607.12340 — the method-twin); tool-use
  grounding and verification (ToolLLM, Self-RAG, Tool-Augmented Reward Modeling);
  multi-agent failure attribution (AgenTracer).
- **In scope:** measuring an install-time provenance intervention on
  prompted/in-context agents against a sandboxed downstream task. **Out of
  scope:** retraining the recommendation model; live uncontrolled registries;
  a live iteratively-adapting red-team adversary (only a single simulated
  retargeting sweep is contemplated, and even that is a scale-up stretch goal).
- **Confidence: high** on the phenomenon and gap (the base paper is read in full
  in digest N3/N4 and confirms phenomenon + attack + detection-failure +
  defense-collapse, and explicitly does *not* build an install-time gate);
  **medium** on the novelty margin of the specific mechanism (digest N2/N10/t1
  flag that a provenance gate is a direct reading of the base paper's own closing
  call for "verified recommendation pipelines" — the resolution, adopted below,
  is to make the *measured operating point and timing curve* the contribution,
  not the gate idea).

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed LLM agent operating a multi-step task trajectory that
  embeds one skill-recommend-then-install decision, and given a skill registry
  snapshot annotated with per-publisher trust tiers (verified / previously-seen /
  unknown), determine whether a gate that runs immediately before install and
  keys only on trust tier — together with how many steps that check is delayed —
  changes (a) the rate at which a squatted-malicious install is completed and
  executes, (b) the rate at which a legitimate skill from an unverified publisher
  is wrongly rejected, and (c) the downstream task success and post-block
  recovery cost, relative to running no gate.
- `input`: (1) a trust-tiered registry snapshot; (2) a multi-step trajectory
  harness with a recommend-then-install step inside a task with a real,
  checkable downstream outcome; (3) a gate mapping (recommended name, snapshot) →
  {allow, block, human-review}; (4) a squatting adversary seeded from the base
  paper's confirmed recurring-hallucinated-name set; (5) a probe set of real,
  useful skills from first-time/independent publishers.
- `output`: (1) per-episode labels (hallucinated? squatted vs absent? gate
  verdict? ground-truth task/security outcome); (2) detection-lag = step index of
  first catch (gate: at the decision step; gate-off: organic-failure step, or
  "uncaught"); (3) a (compromise-block-rate, legitimate-reject-rate) operating
  point; (4) recovery cost.
- `constraints`: the gate may use **only** non-LLM provenance metadata — the base
  paper's RQ3 confirms self-/cross-model auditing is coin-flip (51–53%), so any
  LLM "looks-real" judgment inside the gate inherits that failure; the squatting
  simulation must use the confirmed name-recurrence property (RQ2), not arbitrary
  malicious names; ground truth for "compromise" is a static pre-committed
  trust-tier snapshot plus sandbox execution state, never a model judgment.
- `objective` (draft): a good study reports a security/usability operating point
  that **beats or meaningfully differentiates from** the base paper's four
  recommendation-time defenses (best published point: 3.2% hallucination / ~16%
  recall via retrieval grounding), per model/harness cell.
- `study_type`: `empirical` — the seed's own framing (digest N12) is an
  intervention-effect measurement: the harness + gate are the *instrument*, the
  reported operating point and detection-timing-to-cost curve are the result.

**critique:**
- summary: Evidence-traceable to digest N1/N8, and the constraints are the
  strongest part (the provenance-only and recurrence-seeded constraints both
  trace to confirmed base-paper findings). But the `objective` contains an
  outcome-tier framing that directly conflicts with the declared `study_type`,
  and one output term presupposes its own result.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "tier/study_type conflict (leads to a Stage-6 tier_violation)", comment: "The objective says the study must produce an operating point that 'beats or meaningfully differentiates from' the four published defenses — a beats-baseline, outcome-tier framing. But study_type is empirical, and stages.md forbids any 'our procedure beats baseline X' framing for empirical studies (it forces a Stage-6 tier_violation). This is not a wording nit: it decides what Stage 6 is allowed to ask. The evidence that empirical is the intended classification, not technical, is in the digest itself — N8 states the four published points are 'used as published comparison points rather than re-run, since re-running them is not this topic's contribution.' A head-to-head competition would require re-running them under one harness. So the 'beats' verb is the defect, not the classification. Resolve by reframing the objective to a *measurement*: report where the install-time provenance gate's operating point lands on the shared (block-rate, legitimate-reject-rate) plane and how far the published recommendation-time points sit from it — positioning, not victory."}`
  - `{severity: minor, field: "output (1)/(3)", anti_pattern: "presupposed result", comment: "'compromise-block-rate' and calling gate-off outcomes 'successful compromise' presupposes that a squatted install absent the gate actually executes and causes harm — but whether a squatted skill, once installed, executes and is detectable in the sandbox is part of what is measured (digest N9/RQ1 predicts timing may matter less for task success than for security precisely because a silently-installed skill 'may not disrupt the visible task at all'). Prefer neutral phrasing: the rate at which a squatted install is *completed and executed*, measured from sandbox state, not assumed."}`
- decision: `move_to_refiner` (the major is a reframe using content already in
  digest N8/N12; the minor is a wording fix using digest N9 — neither needs new
  content).

### Refiner pass

- `objective` (refined, verbatim into the paper's Problem Definition):
  "A measurement is well-defined if it reports, per model/harness cell: the
  install-time provenance gate's operating point on the shared (compromise-block
  rate, legitimate-unverified-publisher reject rate) plane, the detection-lag-to-
  outcome relationship as the check is delayed, and the recovery cost — with the
  base paper's four published recommendation-time operating points placed on the
  *same* plane as fixed reference markers, not as competitors the gate is scored
  against. No arm is framed as 'winning'; the deliverable is where the
  install-time point sits relative to the published recommendation-time frontier
  and how timing moves it."
- `summary` (refined): replaced "a squatted-malicious install is completed and
  executes" (removes the presupposition that it *is* a compromise before it is
  measured); "wrongly rejected" retained (a legitimate skill from an unverified
  publisher is legitimate by construction of the probe set, so "wrongly" is
  licensed).
- `formal_summary` (added): "Trajectory $\tau = (x_1,\dots,x_L)$ with one
  recommend-then-install step $x_r$ that proposes skill name $n$ and, if
  installed, executes skill body $b$ from registry $R$. Registry snapshot
  $R = \{(n_k, p_k, \theta_k)\}$ pairs each published name $n_k$ with publisher
  $p_k$ and trust tier $\theta_k \in \{\mathrm{verified}, \mathrm{known},
  \mathrm{unknown}\}$. Gate $g_\delta : (n, R) \to \{\text{allow, block,
  review}\}$ fires $\delta$ steps after $x_r$ ($\delta=0$: immediate;
  $\delta=\infty$: never / gate-off). Adversary pre-registers a subset of the
  confirmed recurring hallucinated names $\mathcal{H}$ under $\theta=\mathrm{unknown}$.
  Measure, per cell, the map from $(g, \delta)$ to (compromise-completion rate on
  $\mathcal{H}$-squatted names, reject rate on a legitimate-unknown-publisher
  probe set $\mathcal{L}$, task success, recovery cost)."
- `changes_made`: reframed objective from beats-baseline to measurement-and-
  positioning; removed the presupposed-compromise wording; added formal_summary.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical` (the outcome-tier framing that
threatened it was removed, not the classification). This decision gates Stage 6
to **zero outcome-tier RQs**.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: A just-published security study establishes that LLM agents
  hallucinate skill names at scale, that the names recur predictably enough to be
  squatted, that no model can flag them better than chance, and that every one of
  its four recommendation-time defenses buys a lower hallucination rate only by
  destroying usefulness. Its own closing call is for "verified recommendation
  pipelines" it never builds. The unexamined question is whether moving the check
  one step later — to install time, keyed on publisher provenance rather than on
  what the model is allowed to say — escapes that usability collapse.
- `why_it_matters`: All four base-paper defenses share one structural property:
  they intervene on the recommendation distribution (retrieval-constrained
  generation, self-refinement, cross-model voting), which is exactly why they
  collapse recall — a real but training-atypical skill name looks identical to a
  hallucinated one to a filter operating on the model's output. An install-time
  provenance gate does not touch that distribution at all: it only asks whether
  the specific name about to be installed comes from a verified publisher, so a
  correctly-named real skill from an unverified publisher and a hallucinated name
  are separable signals. And a *bare existence* check cannot substitute, because
  the base paper's own threat model is squatting: an attacker who observes a
  recurring hallucinated name pre-registers it, at which point "the name exists in
  the registry" is true for the malicious skill. Treating existence as safety
  would wave the trap straight through.
- `who_cares`: builders of open skill/tool marketplaces deciding whether registry
  presence is sufficient install-time governance; agent-harness authors choosing
  what to check before auto-installing a recommended skill; security teams reasoning
  about the confirmed squatting attack precondition.
- `evidence`: the base paper's confirmed numbers (36.0–43.1% hallucination, every
  configuration affected; RQ2 name recurrence; RQ3 51–53% detection; RQ4 best
  defense 40.8%→3.2% hallucination at ~16% recall) and its verbatim closing
  position (registry-level name reservation + verified recommendation pipelines,
  neither built). The tool-use literature already grounds proposed *actions* in
  real executable resources (ToolLLM trains on executable APIs; Tool-Augmented
  Reward Modeling invokes real tools mid-evaluation) but assumes the tool set is
  fixed, known, and trustworthy — the exact assumption the base paper shows is
  false for open registries.

**critique:**
- summary: Stake-specific, real citations, the squatting correction is load-
  bearing and the "recommendation-distribution vs install-point" contrast is a
  genuine mechanism, not hype. But coverage of Stage 1's outputs is incomplete in
  the same way B5.5's first motivation was.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 promises a *detection-timing* output (output 2: the step index of first catch, and a timing-to-cost curve) — a claim about *when* in the trajectory the intervention lands, not just a final operating point. why_it_matters motivates the operating point (outputs 3/4) thoroughly but never says why per-step timing specifically matters, as opposed to a single post-hoc audit of the final state. A reader can fairly ask 'why not just check provenance once, at the end, and be done?' — and there is a real, unaddressed answer in digest N9/RQ1: unlike the base paper's pure-noise hallucinations (which stall the visible task and surface organically), a *successfully installed malicious skill can look like task success* and may never organically surface, so a single end-state audit cannot distinguish 'blocked before execution' from 'executed silently, task completed anyway.' When the gate fires therefore decides whether harm is caught at all and at what recovery cost. Without this, the timing output is unmotivated."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended, verbatim into the Introduction): "...and critically,
  *when* the check fires is not a tuning detail but a first-class outcome: unlike a
  hallucinated non-existent name (which stalls the task and surfaces organically,
  because the tool simply is not there), a squatted skill that installs and runs
  can complete the visible task while doing its damage silently — so a single
  post-hoc audit of the final state cannot tell 'blocked before execution' apart
  from 'executed silently, task succeeded anyway.' Only step-indexed interception
  distinguishes the two, and the number of steps between an untrusted install and
  its detection is exactly the recovery cost an operator pays. This is why the study
  measures a detection-lag-to-outcome curve, not just an endpoint."
- `changes_made`: added the timing-coverage argument tying output 2 to a concrete
  why-now stake.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works are **specific (deep) tier** — digest N3/N4 engaged each at the
approach + limitation level. One is the fully-read non-corpus method-twin
(arXiv:2607.12340); eight are `[GROUNDED:corpus]` OpenReview records whose
titles/URLs were re-verified directly against `topics/corpus/ideas.jsonl` during
Phase A (all eight `paper_id`s resolve; titles match the digest's characterizations).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing /
limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it motivates) |
|---|---|---|---|
| `rw_hallucskills` | HallucSkills (Yuan et al., arXiv:2607.12340) | reference-point only | Measures hallucination at the recommendation-event level; validates one end-to-end install path as a single PoC; no multi-step trajectory-outcome study, no detection-timing, no recovery-cost, no systematic false-positive study; all four defenses act at recommendation time. **Nearest neighbor.** |
| `rw_toolllm` | ToolLLM (OpenReview:dHng2O0Jjr) | false (fixed known API set) | Depth-first multi-path decisioning mitigates early-error propagation but on a fixed, known API set; never instruments *when* a wrong (let alone nonexistent) tool choice is made or how timing relates to recoverability. |
| `rw_funcmasking` | Robust Function-Calling via Function Masking (OpenReview:yVQcr4qjD6) | **true (drafted)** | Shows models shortcut on function *names*; trains the policy to abstain when no real function applies — but within a known, fixed function set, and it robustifies the *policy*, not an external install-time gate. |
| `rw_agentracer` | AgenTracer (OpenReview:l05DseqvuD) | false | Counterfactual-replay failure attribution is the closest precedent for "how an early error causally affects a later outcome," but it diagnoses a *completed* trajectory post hoc and is built for general role/step errors, not a live pre-install gate. |
| `rw_selfrag` | Self-RAG (OpenReview:hSyW5go0v8) | **true (drafted)** | Learned reflection tokens deciding on-demand external checking is conceptually the closest to a grounding gate, but it is for factual-claim retrieval/support in generation, and requires retraining the base model rather than being a drop-in check. |
| `rw_themis` | Tool-Augmented Reward Modeling (OpenReview:d94x0gWTUX) | false | A reward model invokes real tools before scoring, but assumes *its own* toolset is real by construction; never asks whether the *evaluated policy* proposed a nonexistent/untrusted tool. |
| `rw_selfevolve` | Self-Evolving Agent Benchmarks (OpenReview:2H03gm4Rq6) | false | Treats a reproducible test-time trajectory as validation for a new benchmark item — a trajectory-construction method, not a live install-time safety intervention. |
| `rw_genartist` | GenArtist (OpenReview:Ur00BNk1v2) | false | Tree-structured planning with per-node verification and backtracking is the closest "catch-early-and-recover" architecture, but verifies image-generation quality, not tool existence/provenance, and never measures backtracking cost as a function of detection earliness. |
| `rw_toolacemt` | ToolACE-MT (OpenReview:KznJt9Fhjc) | false | Its offline verification stage checks *synthesized training data* trajectories once, offline — not a live per-step gate on a deployed agent's real-time proposals. |

**critique:**
- summary: Grounding is solid, the nearest neighbor (HallucSkills) is named and
  confronted rather than buried, and every limitation is problem-tied (not
  "scalability issues"-style vagueness). But two baseline labels fail the I/O-match
  test.
- comments:
  - `{severity: major, field: "specific_related_works[rw_selfrag / rw_funcmasking].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Both are drafted as potential baselines, but neither's I/O maps onto this paper's intervention. Self-RAG requires *retraining the base model* to emit reflection tokens for *factual-claim* retrieval — its input is a generation task and its output is a re-trained policy, not a drop-in install-time verdict over a registry snapshot. Function Masking likewise robustifies the *policy* via a masked-name training set within a *known, fixed* function set — it never faces the existence/provenance question at all. Per the stage-3 rubric, a work whose I/O doesn't map is 'not a baseline — at best a method-side reference.' Marking either a baseline implies its reported numbers are compared against, which they cannot be (nothing here is re-trained). The genuine runnable comparators are only gate-off (no intervention) and a *bare-existence* control gate; the base paper's four published points are fixed reference markers on the plane (Stage 1's reframed objective), not re-run baselines."}`
  - `{severity: minor, field: "rw_agentracer", anti_pattern: null, comment: "AgenTracer is cited as the precedent the timing-instrumentation 'adapts,' but it attributes failure *after a full trajectory completes*. Borrowing it as a live pre-execution control risks conflating post-hoc attribution with online intervention. The delayed-gate control is really an original controlled-delay design; it borrows only the counterfactual logic (hold the trajectory fixed, vary when the check fires), not AgenTracer's offline tracer. Say that."}`
- decision: `move_to_refiner`.

### Refiner pass

- `rw_selfrag.is_potential_baseline` and `rw_funcmasking.is_potential_baseline`
  set to `false`; both `role` set to `related_for_context` with the sharpened
  note "closest existing *mechanism* for on-demand external checking / name-
  shortcut robustification, but requires retraining and does not face the
  provenance/existence question — a method-side reference, not a runnable
  comparator."
- `rw_agentracer` note sharpened: "the controlled-delay design here is original;
  it borrows AgenTracer's counterfactual logic (hold trajectory fixed, vary the
  intervention point) but not its offline, post-completion tracer."
- **Nearest-neighbor handling (guidance.md situation 6 — method-twin):**
  `rw_hallucskills` carries `threat_to_motivation: high` (it is the same problem
  area and proved the phenomenon/attack/detection-failure/defense-collapse).
  Handled by concede-and-differentiate, recorded verbatim for the Related Work
  opening: concede it establishes the phenomenon, the squatting attack precondition,
  the coin-flip detectability, the recommendation-time defense collapse, and a
  single install-path PoC; claim the distinct response variables (trajectory-
  embedded install-time interception; detection-timing-to-cost; false-positive
  rate on legitimate unverified publishers), the distinct intervention point
  (install/execution vs recommendation), and the distinct signal (publisher
  provenance vs name existence / name similarity).
- **Note on `verify_as_hypothesis`:** set `false` on every limitation — none is a
  distinct framing-tier check; the closest candidate (HallucSkills' deferred
  false-negative study) restates this paper's own core measurement, already
  covered as mechanism-tier RQs in Stage 6. Per stages.md, no framing-tier RQ is
  manufactured.
- `declined_to_fix`: none.

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (from digest N5's C1–C6; C5 held out as an explicit stretch goal):

- **`sp_squatting_ground_truth`** (C1) — *description:* Construct a registry and
  adversary in which "the name exists" is true for the malicious skill, so the
  measurement tests provenance, not existence. *why_it_is_a_problem:* the base
  paper's own threat model is squatting; any evaluation whose ground truth is
  name-existence would score the trap as safe by construction. *technical_challenge:*
  the snapshot must carry forgery-resistant publisher-trust tiers and registration
  recency, and the adversary must pre-register names drawn from the *confirmed
  recurring* hallucinated set, not arbitrary strings, to stay faithful to the
  demonstrated attack. *source_limitation_ids:* `["lim_hallucskills"]`.
- **`sp_provenance_only_gate`** (C2) — *description:* Decide install with zero LLM
  judgment anywhere in the verdict path. *why_it_is_a_problem:* the base paper's
  RQ3 confirms self-/cross-model auditing is coin-flip (51–53%); an LLM "looks-real"
  call inside the gate re-imports that exact failure. *technical_challenge:* the
  verdict must be a function of provenance metadata alone (publisher tier,
  registration age, cross-registry corroboration), which forces a hard choice about
  the middle case — an unknown-publisher skill with no other signal — that a
  legitimate first-time publisher also occupies. *source_limitation_ids:* `["__novel__"]`.
- **`sp_usability_cost`** (C3) — *description:* Measure how often the gate rejects a
  *legitimate* skill from an unverified publisher. *why_it_is_a_problem:* every
  base-paper defense collapsed usefulness (best case ~16% recall); if the gate does
  the same, it relocated the tradeoff instead of solving it. *technical_challenge:* a
  legitimate first-time publisher is indistinguishable from a squatter on provenance
  *alone* until trust accrues, so the false-reject rate is not obviously avoidable —
  it must be measured, against a probe set of real useful skills from independent
  publishers, and compared to the base paper's published ~84%/~55% recall-loss
  figures. *source_limitation_ids:* `["__novel__"]`.
- **`sp_timing_causal`** (C4) — *description:* Isolate the causal effect of *when*
  the check fires on the security outcome and recovery cost, holding task difficulty
  fixed. *why_it_is_a_problem:* the seed's core question is partly about interception
  timing; if timing is confounded with task difficulty, no timing claim is licensed.
  *technical_challenge:* the outcome is now security-relevant (was a squatted skill
  installed and did it execute in the sandbox), which — unlike a stalled task — may
  never organically surface, so a controlled-delay design is needed that varies only
  the intervention step. *source_limitation_ids:* `["lim_agentracer"]`.
- **`sp_config_heterogeneity`** (C6) — *description:* Prevent known cross-
  configuration variance from masking or inflating the gate's measured effect.
  *why_it_is_a_problem:* the base paper's hallucination rate already ranges 36.0–43.1%
  across configurations; a pooled number would be uninterpretable against its own
  per-configuration reporting. *technical_challenge:* every operating-point and
  timing statistic must be reported per model/harness cell and against the base
  paper's own per-defense numbers, never pooled. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out — solving all five jointly delivers Stage 1's four
  outputs (ground-truth + gate → operating point; usability-cost → the reject-rate
  axis; timing-causal → the detection-lag output; heterogeneity → per-cell
  reporting). But one pair reads as potentially the same sub-problem twice.
- comments:
  - `{severity: minor, field: "sp_squatting_ground_truth / sp_provenance_only_gate", anti_pattern: "overlap", comment: "Both bottom out in 'the gate's signal is provenance, not name existence,' and could read as one sub-problem stated twice. They are genuinely distinct — one is about *ground-truth and adversary construction* (making the evaluation faithful to squatting, an offline design property of the testbed), the other is a *design constraint on the deployed gate* (no LLM in the verdict path, an online property of the intervention) — but the descriptions don't make the offline-vs-online distinction explicit enough, so a reader could merge them."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_squatting_ground_truth.technical_challenge` sharpened to end: "...this is an
  *offline testbed-construction* property — the registry snapshot and the
  recurrence-seeded adversary must make squatting the ground truth *before any
  agent runs*; it says nothing about what the deployed gate is allowed to read."
- `sp_provenance_only_gate.technical_challenge` sharpened to end: "...this is an
  *online gate-design* constraint distinct from the offline ground-truth
  construction — even a perfectly squatting-faithful testbed would be undone by a
  gate that quietly consulted an LLM (or a name-similarity heuristic) at decision
  time, re-importing the coin-flip failure the testbed was built to expose."
- `changes_made`: made the offline-construction vs online-design distinction explicit.
- `declined_to_fix`: C5 (adversarial re-targeting) is deliberately not promoted to
  a sub-problem — it is a longer-horizon question the plan can only partially answer
  with a single simulated sweep (digest N6 `unaddressed_challenges: [C5]`), so it is
  carried as a scale-up stretch goal and named honestly as out of scope, not dressed
  as a solved decomposition item.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations,
3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_trust_registry`** → `sp_squatting_ground_truth`. *proposed_approach:* snapshot
  the registry per episode, annotating each published name with publisher trust tier
  (verified / known / unknown) and registration recency; a squatted malicious skill
  can satisfy "exists" but never "verified-or-known publisher." *key_insight:*
  existence and provenance are different predicates, and only the second survives
  the squatting threat model. *hypotheses:* ["A bare name-existence gate (allow iff
  the name resolves in the registry) blocks under 5% of squatted-malicious installs,
  because the attacker's whole move is to make the name resolve — establishing that
  existence-checking is not a defense against the base paper's own attack."]
- **`m_provenance_gate`** → `sp_provenance_only_gate`. *proposed_approach:* a pre-
  install check keyed purely on M1's provenance metadata, no LLM anywhere: verdict is
  allow (verified/known publisher), block (unknown publisher), or human-review
  (unknown publisher flagged for a human, the middle case a legitimate first-timer
  also lands in). *key_insight:* moving the check to the install step means it never
  touches the recommendation distribution, so it does not inherit the recall collapse
  the recommendation-time defenses suffer. *hypotheses:* ["The gate blocks at least
  90% of squatted-malicious installs using zero LLM calls, per model/harness cell.",
  "Removing the LLM from the verdict path costs nothing in block rate: an ablation
  that adds an LLM 'looks-real' judgment does not raise the block rate beyond the
  provenance-only gate's, consistent with the base paper's coin-flip RQ3."]
- **`m_trajectory_harness`** → substrate for `sp_timing_causal` and output delivery.
  *proposed_approach:* embed one recommend-then-install decision (from the base
  paper's two settings: standalone-LLM recommendation and agent-harness recommend-
  then-install) as one step inside a longer task with a real checkable outcome
  (executable multi-step tool-dependency tasks in the style of ToolLLM), with the
  outcome including a security dimension (was a squatted skill installed and did it
  execute) alongside task success. *key_insight:* only an embedded install step with
  a real downstream task can expose the difference between "blocked before execution"
  and "executed silently, task succeeded." *hypotheses:* ["Gate benefit (the block-rate
  gain over gate-off) is larger in the agent-harness recommend-then-install setting
  than in the standalone-LLM recommendation setting, because only the former has a
  real install/execution step to intercept."]
- **`m_recurrence_adversary`** → `sp_squatting_ground_truth`. *proposed_approach:*
  seed the simulated attacker's pre-registered names from the confirmed recurring
  hallucinated-name set (RQ2), not arbitrary strings, so the adversary is faithful
  to the demonstrated attack. *key_insight:* an attack that only works against
  arbitrary names would over- or under-state the gate's value; recurrence is what
  makes pre-registration cheap and the threat real. *hypotheses:* ["The compromise-
  completion rate under gate-off is materially above zero (≥ a pre-registered floor)
  on recurrence-seeded squatted names, confirming the attack path executes end-to-end
  in the harness, not just in the base paper's single PoC."]
- **`m_timing_control`** → `sp_timing_causal`. *proposed_approach:* record the step
  index at which an untrusted/squatted install is first caught — immediately by the
  gate (δ=0), never/late via organic failure (gate-off), or artificially delayed by
  k steps (delayed-gate) — holding the trajectory and task difficulty fixed and
  varying only when the check fires. *key_insight:* a controlled delay isolates
  timing's causal effect on a security outcome that would otherwise never organically
  surface. *hypotheses:* ["Compromise-execution rate and recovery cost worsen
  monotonically as the check is delayed across {immediate, delayed-k, never}, holding
  task difficulty fixed."]
- **`m_operating_point`** → `sp_usability_cost` + `sp_config_heterogeneity`.
  *proposed_approach:* per episode, record compromise blocked/occurred, task
  success/fail, recovery cost, and the legitimate-unverified-publisher reject rate on
  the probe set; report a single (block-rate, legitimate-reject-rate) operating point
  per cell, placed on the same plane as the base paper's four published points.
  *key_insight:* the usability cost is the reject rate on *real* skills, and it is the
  one number that decides whether the tradeoff was solved or merely relocated.
  *hypotheses:* ["The gate's legitimate-unverified-publisher reject rate is materially
  below the base paper's worst recommendation-time recall loss (~84% real-skill
  rejection), specifically below half of it (< 42 percentage points), because moving
  the intervention off the recommendation distribution does not penalize a correctly-
  named real skill for being training-atypical."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis
  is falsifiable with a stated threshold, and the placebo (`m_trust_registry`'s
  existence-gate hypothesis) is a genuine load-bearing control, not decoration. But
  one method's *block* branch smuggles in exactly the signal the study was built to
  discredit.
- comments:
  - `{severity: major, field: "m_provenance_gate.proposed_approach", anti_pattern: "mismatch (the mechanism contradicts its own sub-problem's constraint)", comment: "The draft's earlier framing (carried from digest N6 M2) let the *block* verdict fire when 'the name matches a documented hallucination-recurrence pattern.' That reintroduces a *name-based* signal into the gate's verdict path — precisely the shortcut Function Masking (OpenReview:yVQcr4qjD6) shows models over-rely on, and precisely what sp_provenance_only_gate forbids. If the gate blocks partly on 'this name looks like a known hallucination,' it is partly a name-similarity gate and inherits that brittleness, and worse, it confounds the clean claim that provenance *alone* suffices. The recurrence-seeded pattern belongs to the *adversary/ground-truth construction* (m_recurrence_adversary, offline), NOT to the deployed gate's inputs (online). Fix: the block decision keys on publisher tier (unknown/unverified) as the necessary and sufficient signal; the recurrence set is used only to build the attack and to *label* ground truth, never read by the gate at decision time. This keeps the provenance-only claim clean and keeps the two sub-problems (offline construction vs online design) genuinely separate."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_provenance_gate.proposed_approach` (corrected, verbatim into the Methodology):
  "The verdict is a function of provenance metadata *only*: allow iff the publisher
  is verified or previously-known; otherwise block (unknown publisher) or route to
  human-review (unknown publisher, an operator-configurable middle tier). The gate
  never reads the recommended name's *string* — no existence lookup as a safety
  signal, no similarity-to-known-hallucinations heuristic, no LLM judgment — so its
  block decisions cannot inherit either the name-shortcut brittleness or the
  coin-flip detectability the base paper documents. The confirmed recurring
  hallucinated-name set is consumed *only* by the offline adversary constructor and
  the ground-truth labeler, never by the online gate."
- `m_provenance_gate.hypotheses[1]` retained (the LLM-ablation now cleanly tests that
  adding a judgment the gate deliberately excludes does not help).
- `changes_made`: removed the name-based block branch; made provenance the sole gate
  input; documented the offline/online separation of the recurrence set.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **7 hypotheses total** (1 placebo/existence-gate,
2 on the provenance gate, 1 harness/setting-dependence, 1 attack-path-validity,
1 timing-monotonicity, 1 usability-cost) — mixing instrument-validity/control claims
with the study's headline empirical predictions, the expected mix for an `empirical`
study_type (per the Stage-6 header below).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`.
- **Outcome-tier: 0 RQs** — required by `study_type = empirical`. No RQ is framed as
  "the gate beats defense X"; the base paper's four published points are fixed
  reference markers on the operating-point plane (Stage 1's reframed objective),
  never competitors re-run and scored against. This is the direct downstream payoff
  of the Stage-1 study_type fix — had the "beats the four defenses" objective
  survived, RQ1 below would be a `tier_violation`.

### Round 1 (critic phase)

**draft_v1:**

`datasets` (the harness is novel; the *source material* is real and named):
- A novel multi-step recommend-then-install trajectory harness embedding decisions
  from the base paper's own two settings (standalone-LLM recommendation; agent-harness
  recommend-then-install). *justification:* only an embedded install step with a real
  downstream task exposes the blocked-before-execution vs executed-silently distinction
  the timing RQ needs.
- A trust-tiered skill registry — a real marketplace's publisher-verification API if
  one exposes trust tiers, else a constructed synthetic registry. *justification:*
  provides the provenance metadata the gate keys on; without trust tiers there is no
  gate to evaluate.
- A squatting-adversary simulator seeded from the confirmed recurring hallucinated-name
  set. *justification:* makes squatting the ground truth faithfully (offline), so the
  block-rate axis measures provenance-blocking, not existence-blocking.
- A held-out probe set of legitimate skills from unverified/independent publishers.
  *justification:* the only way to measure the usability-cost (false-reject) axis on
  *real* skills.

`baselines` (sanity-check comparators / reference markers, not competitors to beat):
- Gate-off (no intervention) — the necessary control for every gate-on claim.
- Bare-existence gate (allow iff the name resolves) — the placebo whose block rate on
  squatted names must be ~0, establishing existence ≠ provenance.
- Delayed-gate (the provenance check fired k steps late) — isolates timing.
- The base paper's four published operating points — placed on the plane as fixed
  reference markers, *not re-run* (re-running them is not this study's contribution).

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_operating_point` | `sp_usability_cost` | "The gate blocks at least 90% of squatted-malicious installs using zero LLM calls, per model/harness cell." |
| `rq_usability_cost` | `sp_usability_cost` | "The gate's legitimate-unverified-publisher reject rate is materially below the base paper's worst recommendation-time recall loss (~84% real-skill rejection), specifically below half of it (< 42 percentage points), because moving the intervention off the recommendation distribution does not penalize a correctly-named real skill for being training-atypical." |
| `rq_existence_placebo` | `sp_squatting_ground_truth` | "A bare name-existence gate (allow iff the name resolves in the registry) blocks under 5% of squatted-malicious installs, because the attacker's whole move is to make the name resolve — establishing that existence-checking is not a defense against the base paper's own attack." |
| `rq_attack_path` | `sp_squatting_ground_truth` | "The compromise-completion rate under gate-off is materially above zero (≥ a pre-registered floor) on recurrence-seeded squatted names, confirming the attack path executes end-to-end in the harness, not just in the base paper's single PoC." |
| `rq_provenance_only` | `sp_provenance_only_gate` | "Removing the LLM from the verdict path costs nothing in block rate: an ablation that adds an LLM 'looks-real' judgment does not raise the block rate beyond the provenance-only gate's, consistent with the base paper's coin-flip RQ3." |
| `rq_timing` | `sp_timing_causal` | "Compromise-execution rate and recovery cost worsen monotonically as the check is delayed across {immediate, delayed-k, never}, holding task difficulty fixed." |
| `rq_setting` | `sp_timing_causal` | "Gate benefit (the block-rate gain over gate-off) is larger in the agent-harness recommend-then-install setting than in the standalone-LLM recommendation setting, because only the former has a real install/execution step to intercept." |

**critique:**
- summary: Tier accounting is clean (0 outcome-tier, correct for empirical), every RQ
  traces to a verbatim Stage-5 hypothesis, and the existence-placebo RQ is a real
  falsification control. But two RQs point at the wrong `target_sub_problem_id`, and
  one design lacks a hard pre-run gate the digest itself demands.
- comments:
  - `{severity: major, field: "rq_operating_point.target_sub_problem_id", anti_pattern: "reference-integrity slip", comment: "rq_operating_point tests the *block-rate* hypothesis (m_provenance_gate) but is tagged to sp_usability_cost, which is the *reject-rate* axis. The block-rate hypothesis belongs to sp_provenance_only_gate (the gate design), and the reject-rate hypothesis belongs to sp_usability_cost. As drafted, sp_provenance_only_gate is targeted only by rq_provenance_only, and sp_usability_cost carries two RQs about different axes. Re-map: rq_operating_point → sp_provenance_only_gate; rq_usability_cost → sp_usability_cost. Cross-stage reference integrity (stages.md rule 3) requires every target_sub_problem_id to actually be the sub-problem the hypothesis addresses."}`
  - `{severity: major, field: "datasets / analysis plan", anti_pattern: "missing replication gate", comment: "The digest (N6 staged plan, N8 metrics) makes baseline-hallucination-rate replication a *hard gate*: 'a pilot that cannot reproduce the published rate cannot trust its own gate-effect estimates.' The draft's RQ set assumes the 36.0–43.1% hallucination rate transfers to this harness but never states the pre-run check that must pass before any arm is scored. Without it, a harness that elicits, say, 5% hallucination would make every squatting arm underpowered and every operating point incomparable to the published points. Add an explicit replication gate (reproduce a hallucination rate within the published range on ≥1 base-paper model/harness) as a walking-skeleton pass criterion, exactly analogous to a placebo arm — its failure reopens the harness, it is not a substantive result."}`
- decision: `move_to_refiner` (both are integrity/completeness fixes using content in
  digest N6/N8; no new content).

### Refiner pass

- `rq_operating_point.target_sub_problem_id` → `sp_provenance_only_gate`;
  `rq_usability_cost.target_sub_problem_id` → `sp_usability_cost` (unchanged, now the
  only RQ on that sub-problem). Reference integrity re-verified: every sub-problem now
  has ≥1 RQ; sp_squatting_ground_truth has 2 (placebo + attack-path),
  sp_provenance_only_gate has 2 (block-rate + LLM-ablation), sp_timing_causal has 2
  (timing + setting), sp_usability_cost has 1 (reject-rate).
- Added a **replication gate** to the setup (not a new RQ — a pre-run pass criterion,
  like a placebo): "Before any gate arm is scored, reproduce a skill-hallucination rate
  within the base paper's published 36.0–43.1% range on at least one of its own
  model/harness configurations, using its prompt-construction method as closely as
  feasible. Failure reopens the harness (guidance situation 8); it is never reported as
  a substantive null." Mirrored into the digest-consistency note.
- `changes_made`: re-mapped two target_sub_problem_ids; added the replication gate.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

Per SKILL.md's cross-stage rules and the task's explicit "literally recount
hypotheses vs RQs" instruction:

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem`
   fields name no technique (the gate first appears in Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable
   stage-to-stage.
3. **Reference integrity** —
   - Stage 4 `source_limitation_ids`: `sp_squatting_ground_truth = ["lim_hallucskills"]`
     ∈ Stage 3 ✓; `sp_timing_causal = ["lim_agentracer"]` ∈ Stage 3 ✓; the other three
     `["__novel__"]` ✓.
   - Stage 5 `target_sub_problem_id`: all six ∈ Stage 4 (`m_trajectory_harness` maps to
     `sp_timing_causal` as its substrate; the other five map one-to-one) ✓.
   - Stage 6 `target_hypotheses`: all seven are **verbatim** matches to Stage 5
     `methods[].hypotheses` ✓ (spot-checked all 7 against the Stage-5 confirmed text).
4. **Hypothesis vs RQ recount (explicit):** Stage 5 confirmed **7 hypotheses**
   (m_trust_registry 1, m_provenance_gate 2, m_trajectory_harness 1,
   m_recurrence_adversary 1, m_timing_control 1, m_operating_point 1). Stage 6 confirmed
   **7 RQs**, all mechanism-tier, **one per hypothesis, no orphan and no double-cover.**
   7 = 7. ✓
5. **Output coverage** — Stage 1's four outputs each reachable: operating point via
   rq_operating_point + rq_usability_cost; detection-lag via rq_timing; compromise/task
   labels via rq_attack_path + rq_existence_placebo + the harness; provenance-only
   integrity via rq_provenance_only; setting-dependence via rq_setting. Nothing promised
   in Stage 1 falls off the chain by Stage 6.
6. **`study_type` consistency** — `empirical` throughout; Stage 6 emits 0 outcome-tier
   RQs, which is only correct *because* the Stage-1 "beats the four defenses" objective
   was reframed to measurement in that stage's critic round. Had it survived, this
   recount would surface a tier_violation.

**What was hardest:** not factual disagreement (the base paper is read in full in the
digest) but two recurring scope disciplines — (i) keeping the *gate* (a genuinely
simple mechanism: check a publisher tier) from being sold as the contribution when the
contribution is the *measured operating point + timing curve*, which is what keeps the
study honestly empirical rather than a thin method paper (digest t1/N2 flag exactly
this), and (ii) keeping the recurrence-seeded name signal strictly on the *offline*
adversary/ground-truth side and out of the *online* gate's inputs — the Stage-5 major —
so the provenance-only claim stays clean.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6
refiner passes. No stage hit the round cap; no cross-stage backup was required.
Genuine `[major]` flags fired in Stages 1, 2, 3, 5, 6 (five of six stages);
Stage 4 fired a `[minor]` overlap flag. No stage closed over an open major.
