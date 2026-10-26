# Discussion Trace — B7.2 (auto-research-discussion, Stages 1–6)

> Mode: **autoclaude** (self-play — Claude plays proposer, critic, and refiner; the "repo" is a single immature seed, `../README.md`, sourced from `trend_scan_2026-08.md` §2.4 + the 2026-08-13 occupancy sweep). There is **no** `digest.md` and **no** `paper.md` for this topic — the seed is deliberately thin, so the formal problem definition, assumptions, and RQs-with-fallbacks below are derived from scratch during the stages rather than lifted from a pre-registered spec. Round cap: 5/stage (none hit). Each stage ran proposer v1 → one genuine critic round (a real, evidence-grounded major/minor, per `autoclaude_mode.md`'s anti-sycophancy rules) → one refiner pass → confirmed output.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on confirmed Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. `pipeline.md` holds the phase/gate log. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work; missing per-RQ falsification conditions in Experiments) are folded into the `paper_draft.*` files.
>
> **Defensive-security framing (held throughout):** this is a measurement study of how long adversarial content *persists* under benign memory-management policies, built to inform defenses. No stage produces an attack recipe; injected poison is instantiated only from **already-published** attacks used as a fixed treatment, and every hypothesis is about the *persistence estimand and the policies that govern it*, never about improving an attack.

## Seed brief (reconstructed from `../README.md` + `trend_scan_2026-08.md`)

- **One-sentence description:** Treat each injected poisoned claim in a long-lived LLM-agent memory as the subject of a survival analysis, and measure — as a censoring-aware neutralization *rate/half-life*, not a fixed-checkpoint binary — how long its behavioral influence persists under continuous benign traffic and utility-driven memory-management dynamics (summarization, consolidation/reflection, eviction/TTL, deduplication).
- **Apparent inputs:** a memory-augmented agent; a fixed library of published poisoning attacks used as a treatment; a (memory-policy × defense) grid; a long benign interaction stream; intermittent mechanical acceptance probes.
- **Apparent outputs:** a censoring-aware survival function / hazard curve per (policy × defense) cell; a poison half-life estimate with confidence interval; a per-cell persistence classification.
- **Closest research areas:** agent memory poisoning persistence (MemSecBench 2607.27080; Injection-Execution Dissociation 2605.08442; State Contamination / laundering 2605.16746); agent-memory defenses (A-MemGuard 2510.02373; MemLineage 2605.14421; Forensic Trajectory Signatures 2606.30566); memory-management / forgetting (From Recall to Forgetting 2604.20006; control-plane forgetting 2606.15903; MemGPT 2310.08560; Generative-Agents reflection 2304.03442); survival analysis (Kaplan–Meier 1958; Cox 1972).
- **In scope:** measuring persistence of already-published poison under manipulated memory policies in a sandbox. **Out of scope:** designing new attacks; new defenses (defenses enter only as fixed treatments); multi-agent contagion dynamics (named as a fallback angle in the README, deferred).
- **Confidence: medium-high.** The seed names a sharp falsifiable core hypothesis (utility-improving consolidation *lengthens* half-life via laundering) and a minimal experiment, but leaves the estimand, the event definition, the confound structure, and the RQ set unspecified — those are constructed below.
- **Falsifiable core hypothesis (from the seed, carried as the study's spine):** aggressive, utility-improving memory management **increases** poison half-life rather than decreasing it, because laundering (2605.16746) converts a detectable poisoned claim into a detector-invisible but behaviorally-active one — so the "Forget"/repair stage that a checkpoint benchmark scores as mitigation is, under realistic policies, a persistence-*amplifying* stage. If half-life is invariant to memory policy, the hypothesis is cleanly falsified.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a memory-augmented LLM agent whose long-lived memory has been seeded at time zero with a set of poisoned claims by a published attack, and given a memory-management policy (summarization, consolidation/reflection, eviction/TTL, deduplication) that governs how that memory evolves under a continuous stream of benign interactions, determine how long each poisoned claim continues to influence the agent's behavior — expressed as a neutralization time, a survival/hazard curve over interaction time, and a half-life — and how that persistence depends on the memory policy and any layered defense.
- `input`: (1) a memory-augmented agent with a configurable memory-management policy; (2) a set of *n* poisoned claims injected at *t*=0 via a fixed, published attack; (3) a benign interaction stream of bounded length *T*; (4) an optional published defense; (5) an intermittent probe schedule.
- `output`: (1) per poisoned claim, a neutralization time (possibly censored); (2) per (policy × defense) cell, a survival function *S(t)* and hazard *h(t)* over interaction time; (3) a half-life *t₁/₂* with a confidence interval; (4) a per-cell persistence classification.
- `constraints`: the injected attack and the benign stream are fixed across policy conditions so the policy is the only manipulated factor; every probe is a mechanical, deterministic decision (no subjective judgment); the agent runs in a sandbox with no live-deployment side effects.
- `objective`: a persistence estimate is correct if it recovers the true neutralization-time distribution of the poisoned claims under the given cell.
- `study_type`: `empirical` — stated explicitly: the seed's core question ("测其中和时间 … 输出 censoring-aware 半衰期估计量与 per-cell hazard 曲线") and its `[证据]` label settle this as a measurement/characterization study, not a proposed fix.

**critique:**
- summary: Strong, evidence-traceable draft, but the objective has a genuine evaluability gap and one output term is ambiguous in exactly the case the seed's own hypothesis turns on.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "'Neutralization' is undefined between two things that the seed's own laundering hypothesis (2605.16746) says diverge: literal removal of the claim from the store, and the end of the claim's behavioral influence. A censoring-aware estimator built on 'is the literal string still present?' would score a laundered claim as neutralized while it is still steering behavior — the exact failure the study exists to expose. A success criterion that does not fix which of these is the event of interest is not evaluable, and picking literal presence silently would build the conclusion's opposite into the instrument."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "'A half-life t₁/₂' presupposes S(t) crosses 0.5 within the horizon T. For cells where the poison persists in the majority of subjects at T, the half-life is undefined (right-censored), not zero and not missing. The output list should name censored/undefined-half-life cells as a first-class result, or the most important cells (the ones where policy amplifies persistence) fall off the table."}`
- decision: `move_to_refiner` (both are formalize-level fixes; the event-definition fix is content the seed's own hypothesis already forces).

### Refiner pass

- `objective` (refined): "A persistence estimate is accepted only if its event of interest is **durable loss of behavioral adoption** — the agent's action or answer ceases to be steered by the poisoned claim, as decided by a validated mechanical acceptance probe, and stays unsteered through the remaining probes — with the claim's *literal detectability* tracked as a separate covariate rather than as the event. A cell whose survival function does not reach 0.5 within the horizon is reported as **half-life ≥ T (right-censored)**, never dropped and never coerced to a point value."
- `summary` (refined): "…determine how long each poisoned claim continues to **steer the agent's behavior** (behavioral adoption, distinct from whether the claim's literal text remains retrievable)…"
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Agent memory *M_t* evolving over benign interaction time *t*=0…*T* under policy π and optional defense *d*. At *t*=0 a published attack injects poisoned claims *P*={*p₁*,…,*pₙ*}. For each *pᵢ*, an acceptance probe *a(pᵢ, t)* ∈ {adopted, not-adopted} decides behavioral adoption; the event time τᵢ = first *t* after which *a(pᵢ,·)* is durably not-adopted (right-censored at *T* if no such *t*). Estimand: the survival function *S_{π,d}(t)*=P(τ>t), the hazard *h_{π,d}(t)*, and the half-life *t₁/₂*=inf{*t*:*S(t)*≤0.5}. A separate literal-presence indicator *ℓ(pᵢ,t)* tracks detectability; the cell {ℓ=absent, a=adopted} is the laundering signature."
- `changes_made`: fixed the event definition to behavioral adoption; separated literal detectability as a covariate; pre-committed censored-half-life reporting; added formal_summary.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Memory-management policies are deployed to make long-lived agents more useful — summarization to fit context, consolidation/reflection to distill experience, eviction/TTL and deduplication to control store growth — and are tacitly assumed to also let benign traffic wash adversarial content out of memory over time. Whether they neutralize a poisoned claim, leave it untouched, or actively prolong its behavioral influence has never been measured as a rate.
- `why_it_matters`: Operators increasingly rely on "it will get summarized/consolidated away" as an implicit, free mitigation for memory poisoning, and repair benchmarks report persistence as a single post-repair binary (present/absent). But if a utility-improving policy *lengthens* the time a poisoned claim keeps steering behavior — because summarization can preserve a claim's influence in a form a content detector no longer flags (laundering) — then the policy chosen for utility is silently a security liability, and the checkpoint labeled "repair" is an amplification step. A defender who cannot see a neutralization *rate* cannot tell "this policy cleans poison slowly" from "this policy launders poison and locks it in," and will mis-provision defenses accordingly.
- `who_cares`: operators deploying long-lived agents who treat memory management as de facto hygiene; builders of memory-poisoning defenses deciding whether they must run continuously or can rely on eventual washout; benchmark authors reporting persistence as a fixed checkpoint; standards bodies (memory poisoning is a catalogued agent risk).
- `evidence`: MemSecBench (2607.27080) reports high post-checkpoint persistence but as a Write–Execute–Forget binary, with no neutralization time; State Contamination (2605.16746) demonstrates the single-pathway mechanism by which adversarial content survives summarization in a detector-invisible form; Injection-Execution Dissociation (2605.08442) shows injection and execution are decoupled across 21 models, i.e. literal presence and behavioral effect already come apart. None estimates a hazard curve or treats the memory policy as a manipulated variable.

**critique:**
- summary: Stake-specific, real citations, correct target — but coverage of Stage 1's outputs is incomplete in a way that matters.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 promises a hazard *curve* h(t) — a time-path — as a first-class output, not just a scalar half-life. why_it_matters motivates the half-life number and the on/off-mitigation question, but never says why the *shape* of the hazard over time matters. A reader can fairly ask 'why not just report the fraction still poisoned at horizon T?' — and the honest answer is exactly the motivation's crux: a policy that launders at a discrete consolidation event produces a hazard that spikes benignly then collapses (neutralization stalls) — a non-monotone/non-constant hazard that is invisible to any single endpoint and is what distinguishes slow-cleaning from lock-in. That argument is present in the method intent but missing from the motivation, so the time-path output is currently unmotivated."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "…critically, this is a claim about the *time-path*, not an endpoint: a policy that launders poison at a discrete consolidation/summarization event produces a hazard that stalls after that event — neutralization effectively stops — which a single end-of-horizon 'fraction still poisoned' number cannot distinguish from a policy that is simply cleaning slowly but monotonically. The defender's decision (run a defense continuously vs. rely on washout) depends on *which* of those two shapes is true, and only a hazard curve over interaction time, not a checkpoint, can tell them apart."
- `changes_made`: added the time-path/hazard-shape coverage argument tying the curve output to a concrete defender decision.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All works below were promoted to the **specific (deep) tier**: each was read at the problem-definition + claimed-contribution + I/O level (metadata and abstracts fetched and verified via the arXiv API — see `pipeline.md` freshness/verification log). No landscape-only padding papers are invented; the `general_related_works` tier is kept minimal and honest.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_memsecbench` | Chen et al., MemSecBench (2607.27080) | **true (as a comparator, not a number to beat)** | Reports persistence as a fixed Write–Execute–Forget **checkpoint binary** (present/absent), scored on literal/detector presence; no neutralization time, no hazard, and the memory policy is a fixed part of the benchmark rather than a manipulated variable. |
| `rw_injexec` | Leong, Injection-Execution Dissociation (2605.08442) | false (short-horizon mechanistic eval) | Shows injection and execution are decoupled across 6 defenses × 21 models, i.e. literal presence ≠ behavioral effect — but over short horizons and without a persistence-over-time estimand or a policy-as-treatment axis. |
| `rw_statecontam` | Wang et al., State Contamination (2605.16746) | false (single-pathway mechanism) | Demonstrates *that* adversarial content can survive summarization in a detector-invisible form (the laundering mechanism), but as a single-pathway existence result, not a cross-policy quantified rate; does not measure how the persistence hazard scales with policy aggressiveness. |
| `rw_amemguard` | Wei et al., A-MemGuard (2510.02373) | false (defense treatment) | A proactive memory defense; enters this study only as a fixed defense *treatment* on the grid, not evaluated on its own leaderboard terms; its own evaluation is not longitudinal-hazard-based. |
| `rw_memlineage` | Ouyang & Hou, MemLineage (2605.14421) | false (defense treatment) | Lineage-guided enforcement for agent memory; likewise a fixed defense treatment; provenance enforcement is orthogonal to whether a laundered claim's *behavioral* influence decays. |
| `rw_forensic` | Leong, Forensic Trajectory Signatures (2606.30566) | false (detection treatment) | Detects poisoning from trajectory signatures — a detector whose visibility is exactly what laundering evades; used as a defense/detection treatment and as the literal-presence covariate's natural instrument. |
| `rw_mempoison` | Devarangadi Sunil et al., Memory Poisoning Attack and Defense (2601.05504) | false (attack + defense source) | Provides an attack used as a fixed injection treatment and a paired defense; studies attack/defense efficacy, not a censoring-aware persistence rate under varying memory policies. |
| `rw_recall2forget` | From Recall to Forgetting (2604.20006) | **true (benign-stream source + benign-forgetting reference)** | Benchmarks *benign* long-term memory retention/forgetting; supplies realistic long benign streams, but measures benign recall utility, never adversarial-content persistence. |
| `rw_controlplane` | Control-Plane Placement Shapes Forgetting (2606.15903) | false (memory-config source) | Shows benign forgetting depends on where the memory control plane sits across 13 configurations; supplies the policy/configuration axis but does not touch adversarial persistence. |

**critique:**
- summary: Grounding is solid and every limitation is specific, but the nearest-neighbor's baseline label misdescribes the relationship and risks an I/O mismatch.
- comments:
  - `{severity: major, field: "specific_related_works[rw_memsecbench].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "MemSecBench's I/O is a fixed-checkpoint **binary persistence rate**, not a time-to-event; its 84.2%-persistence number is a probability at one observation time, not a survival curve. Marking it a straightforward baseline implies we compare our numbers against its number, which is a category error — you cannot beat a hazard curve against a binary. The honest relationship is that MemSecBench's checkpoint is the **degenerate single-observation-time special case** of the continuous estimand here (evaluate S(t) at one t and threshold it). Calling it a baseline hides that subsumption and invites the reviewer question 'isn't this just MemSecBench with more timepoints?' — which must be answered head-on, not filed under baselines."}`
- decision: `move_to_refiner` (a role/framing precision fix; MemSecBench remains the nearest neighbor and its *protocol* is still legitimately reused as the checkpoint comparison arm).

### Refiner pass

- `rw_memsecbench.is_potential_baseline` retained as `true`, but the role note is sharpened: "Not a baseline in the beat-a-number sense — MemSecBench's reported persistence rate is not compared against. Its Write–Execute–Forget **checkpoint protocol** is reused as a *comparison arm* (a single-observation-time evaluation) to demonstrate empirically that thresholding one checkpoint mis-estimates the continuous survival curve; the relationship is subsumption, and the paper's positioning concedes this explicitly."
- `changes_made`: reframed MemSecBench's role from competitor to subsumed special case + comparison arm; this becomes the explicit nearest-neighbor delta in Related Work.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The closest candidate for a framing-tier RQ — "does thresholding a single checkpoint actually mis-estimate the continuous curve" — is not a distinct external-literature hypothesis but a direct consequence of this paper's own estimand, already covered end-to-end as a mechanism-tier RQ in Stage 6 (RQ1). Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems):

- **`sp_censored_estimand`** — *description:* Recover a neutralization-time distribution (survival function, hazard, half-life) from observations that are right-censored (poison persists at horizon *T*) and interval-censored (neutralization falls between two intermittent probes). *why_it_is_a_problem:* the field reports persistence as a fixed-checkpoint binary, which discards censoring and cannot express a rate or a half-life at all; without a censoring-aware estimand there is no time axis to put policy effects on. *technical_challenge:* the event is observed only through a discrete probe schedule and a finite horizon, so the estimator must handle both censoring types and still deliver a half-life with a usable confidence interval. *source_limitation_ids:* `["lim_memsecbench_checkpoint"]`.
- **`sp_behavioral_outcome`** — *description:* Define the neutralization *event* as durable loss of behavioral adoption rather than literal removal, so that a laundered claim (detector-invisible but still steering behavior) is scored as *alive*, not neutralized. *why_it_is_a_problem:* literal presence and behavioral effect are already known to decouple (2605.08442), and laundering (2605.16746) is precisely the regime where they diverge; an event definition based on detectability builds the wrong answer into the instrument. *technical_challenge:* behavioral adoption must be read out from the agent's actions without a subjective judge, and separated cleanly from the literal-presence covariate that a detector reports. *source_limitation_ids:* `["lim_injexec_decoupling", "lim_statecontam_singlepath"]`.
- **`sp_policy_confound`** — *description:* Isolate the causal effect of memory-policy aggressiveness on the persistence hazard from the benign-traffic composition, content salience, and exposure changes that co-vary with policy. *why_it_is_a_problem:* memory policies are chosen for utility and change what the agent sees and stores; a raw correlation between "aggressive policy" and "longer persistence" could be salience/exposure, not laundering. *technical_challenge:* aggressive policies compress the same benign stream differently, so holding the input stream fixed does not by itself hold *exposure to corrective evidence* fixed — the confound survives a naive matched-stream design. *source_limitation_ids:* `["__novel__"]`.
- **`sp_probe_validity`** — *description:* Guarantee the acceptance probe is a reliable, reproducible measurement of behavioral adoption across many probe points and many claims. *why_it_is_a_problem:* an unreliable probe injects measurement noise that is indistinguishable from real hazard, so the survival curve would measure the probe, not the poison. *technical_challenge:* the probe must be mechanical (its ground truth a task outcome, not a rater's opinion) yet still validated against human judgment, and stable enough that its error is far below the effect floor. *source_limitation_ids:* `["__novel__"]`.
- **`sp_competing_risks`** — *description:* Separate the two distinct ways a poisoned claim can stop being adopted — content-neutralization (correction/overwrite of the claim) versus structural eviction (TTL/dedup removing the memory slot regardless of content) — and make hazard curves comparable across cells with different traffic volumes. *why_it_is_a_problem:* a half-life that lumps "evicted by TTL" together with "corrected" is uninterpretable, and the laundering hypothesis is specifically about the *content-neutralization* hazard, not the structural one. *technical_challenge:* the two exit causes are competing risks whose naive Kaplan–Meier treatment biases each other, and the interaction-time axis must be normalized so a high-traffic cell is not spuriously "faster." *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five jointly delivers Stage 1's four outputs), but two sub-problems risk reading as the same problem twice.
- comments:
  - `{severity: minor, field: "sp_behavioral_outcome / sp_probe_validity", anti_pattern: "overlap", comment: "Both bottom out in 'the acceptance probe,' so they can read as one sub-problem split in two. They are genuinely distinct — one is a *construct-definition* problem (what quantity is the event: behavioral adoption, not literal presence), the other a *measurement-reliability* problem (is our reading of that quantity trustworthy across thousands of probe points) — but the descriptions don't make the construct-vs-reliability split explicit, and a reader could reasonably ask why they aren't merged."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_behavioral_outcome.technical_challenge` sharpened to end with: "…this is a **construct-validity** problem — choosing *which quantity* is the event so laundering is scored as persistence — logically prior to, and separate from, whether that quantity is measured reliably."
- `sp_probe_validity.technical_challenge` sharpened to end with: "…this is a **measurement-reliability** problem distinct from the construct choice: even a perfectly-chosen behavioral-adoption event is worthless if the probe reads it with error comparable to the effect floor; the fix is a validation protocol (rater agreement, confusion structure), not a redefinition of the event."
- `changes_made`: made the construct-vs-reliability distinction explicit in both technical_challenge fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations, 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_survival_estimator`** → targets `sp_censored_estimand`. *proposed_approach:* Treat each poisoned claim as a survival subject; from the interval-censored probe sequence and the horizon *T*, estimate the survival function with a Kaplan–Meier / Turnbull interval-censoring estimator and the hazard with a Nelson–Aalen estimator; report the half-life as the median survival time with a bootstrap CI, and cells whose *S(t)* never crosses 0.5 as half-life ≥ *T*. *key_insight:* re-reading "present at checkpoint *t*?" as repeated interval-censored observations of one subject recovers the full *S(t)*/*h(t)*, which a fixed-checkpoint binary structurally cannot; the checkpoint is just *S(t)* evaluated at one *t* and thresholded. *hypotheses:* ["For at least 80% of tested (policy × defense) cells the interval-censored estimator returns a half-life whose 95% CI half-width is below 0.15·T, and the hazard is statistically non-constant (rejects the constant-hazard/exponential null at α=0.05) in at least half of tested cells — establishing that persistence has a time structure a single checkpoint cannot summarize."]
- **`m_behavioral_probe`** → targets `sp_behavioral_outcome`. *proposed_approach:* Score neutralization by a mechanical acceptance probe — a task whose correct output flips iff the poisoned claim is behaviorally adopted — and record, in parallel, a literal-presence indicator from a content detector; define the *laundering cell* as {literal-absent, behaviorally-adopted}. *key_insight:* separating behavioral adoption from literal detectability is exactly what makes laundering *observable* as its own measurable state; a single content-match metric conflates the two and cannot see it. *hypotheses:* ["The fraction of adopted-but-literally-absent claims (the laundering cell) is strictly greater than zero and increases with memory-policy aggressiveness, and the policy→persistence effect is carried by this cell rather than by increased literal retention."]
- **`m_policy_treatment`** → targets `sp_policy_confound`. *proposed_approach:* Make memory-policy aggressiveness the manipulated treatment; replay the *identical* injected claims and benign stream across policy levels (matched design) and fit a Cox proportional-hazards model with policy level as the covariate, estimating the hazard ratio for aggressive-vs-minimal policy; pair it with a matched-salience benign *tracer* claim as a placebo. *key_insight:* replaying identical traffic and claims across policy levels converts the utility–persistence confound into a within-subject contrast, and the benign tracer absorbs any residual salience/exposure effect. *hypotheses:* ["Poison half-life is monotonically non-decreasing in memory-policy aggressiveness, with a Cox hazard ratio for aggressive-vs-minimal policy ≤ 0.7 (|log HR| ≥ 0.36, Holm-corrected p<0.05) under the behavioral-adoption event.", "The matched-salience benign tracer shows no policy-dependent persistence effect (its aggressive-vs-minimal hazard-ratio CI contains 1), so the poison effect is specific to adversarial content, not to generic retention of salient content."]
- **`m_probe_validation`** → targets `sp_probe_validity`. *proposed_approach:* Pre-register the probe as a deterministic decision rule and validate it against ≥2 independent human raters on a held-out probe set, requiring Cohen's κ ≥ 0.7 and an adjacent-only confusion structure, audited on 50 probes in the pilot and 300 pre-scale-up. *key_insight:* anchoring the event's ground truth in a mechanical task outcome (not a subjective judgment) is what gives a reproducible, low-error event definition whose noise sits well below the effect floor. *hypotheses:* ["The mechanical acceptance probe agrees with human adjudication at Cohen's κ ≥ 0.7 on the held-out set, with disagreements confined to adjacent/borderline cases rather than a systematic misread of one adoption type."]
- **`m_competing_risks`** → targets `sp_competing_risks`. *proposed_approach:* Model content-neutralization and structural-eviction as competing risks via cause-specific hazards and cumulative incidence functions; normalize the time axis to interaction turns so cells with different traffic volume are comparable; test split-half reliability of the per-cell classification. *key_insight:* a half-life that lumps TTL eviction with content correction is uninterpretable, and the laundering claim is specifically that aggressive policy lowers the *content-neutralization* cause-specific hazard while leaving the structural one unchanged — a prediction only a competing-risks decomposition can check. *hypotheses:* ["Content-neutralization and structural-eviction cause-specific hazards are separately estimable, and the aggressive-policy effect appears in the content-neutralization hazard specifically (not the structural one); the per-cell persistence classification agrees across two disjoint random half-samples of injected claims in at least 80% of cells."]

**critique:**
- summary: Every method has a real mechanism and every hypothesis is falsifiable with a threshold — but the central method's confound argument has a hole the key_insight glosses over.
- comments:
  - `{severity: major, field: "m_policy_treatment.key_insight", anti_pattern: "mismatch (confound not actually isolated)", comment: "'Replaying identical traffic across policy levels holds composition fixed' is true at the *input*, but an aggressive summarization policy compresses that identical stream, so the agent's *exposure* to corrective benign evidence differs across policy levels even though the input stream is byte-identical. That means the matched-stream design alone does NOT isolate laundering from mere reduced-exposure-to-correction: a claim could persist longer under aggressive policy simply because the agent saw less of the traffic that would have overwritten it, with no laundering involved. The key_insight asserts isolation the design doesn't deliver. The benign tracer is currently framed as a nice-to-have placebo, but it is actually the load-bearing control that closes this hole — if reduced exposure were the mechanism, the matched-salience benign tracer would ALSO persist longer under aggressive policy; its invariance is what pins the effect on adversarial-content laundering specifically. That has to be stated as the isolating argument, not tucked into a second hypothesis."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_policy_treatment.key_insight` extended: "…the matched-stream contrast alone leaves one confound open — aggressive summarization compresses the identical stream, so *exposure to corrective evidence* also drops, which could lengthen persistence with no laundering at all. The matched-salience benign tracer is therefore not a decorative placebo but the load-bearing control that closes exactly this gap: if reduced exposure were the mechanism, the benign tracer would persist longer under aggressive policy too; its invariance under the same policy contrast is what isolates the effect on *adversarial-content laundering* specifically. The two hypotheses are thus one identification argument — the poison hazard ratio is only interpretable as laundering conditional on the tracer's hazard ratio being null."
- `changes_made`: promoted the benign tracer from placebo to the explicit isolating control; tied the placebo hypothesis to the causal reading of the central hypothesis.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **7 hypotheses total** (1+1+2+1+2 across the five methods respectively — `m_policy_treatment` and `m_competing_risks` each carry two). Mixes instrument-validity claims (estimand recoverability, probe validity, split-half reliability) with the study's headline empirical predictions (the policy→persistence reversal and its laundering mechanism) — a deliberate design for an `empirical` study_type, accounted for in the Stage-6 tier header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators only (the fixed-checkpoint protocol, an append-only no-management control, and the benign tracer), never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Benign interaction streams from *From Recall to Forgetting* (2604.20006) — *justification (v1):* provides long-term personalized interaction streams. *(flagged below.)*
- Memory system configurations from *Control-Plane Placement Shapes Forgetting* (2606.15903) — *justification:* supplies the 13-configuration policy/placement axis that instantiates the minimal/moderate/aggressive policy levels.
- Attack + defense treatments from MemSecBench (2607.27080), Memory Poisoning Attack and Defense (2601.05504), and State Contamination (2605.16746) — *justification:* fixed, already-published injection treatments so no new attack is created; span single-fact, procedural, and summarization-surviving (laundering-prone) poison types.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- The MemSecBench Write–Execute–Forget **checkpoint** protocol — a single-observation-time evaluation, to show empirically that one checkpoint mis-estimates the continuous survival curve.
- An **append-only / no-management** control policy — the null memory policy against which "aggressiveness" is defined.
- The **matched-salience benign tracer** — the placebo whose persistence must be policy-invariant.

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_estimand_recovery` | `sp_censored_estimand` | "For at least 80% of tested (policy × defense) cells the interval-censored estimator returns a half-life whose 95% CI half-width is below 0.15·T, and the hazard is statistically non-constant (rejects the constant-hazard/exponential null at α=0.05) in at least half of tested cells — establishing that persistence has a time structure a single checkpoint cannot summarize." |
| `rq_policy_reversal` | `sp_policy_confound` | "Poison half-life is monotonically non-decreasing in memory-policy aggressiveness, with a Cox hazard ratio for aggressive-vs-minimal policy ≤ 0.7 (|log HR| ≥ 0.36, Holm-corrected p<0.05) under the behavioral-adoption event." |
| `rq_placebo_specificity` | `sp_policy_confound` | "The matched-salience benign tracer shows no policy-dependent persistence effect (its aggressive-vs-minimal hazard-ratio CI contains 1), so the poison effect is specific to adversarial content, not to generic retention of salient content." |
| `rq_laundering_mechanism` | `sp_behavioral_outcome` | "The fraction of adopted-but-literally-absent claims (the laundering cell) is strictly greater than zero and increases with memory-policy aggressiveness, and the policy→persistence effect is carried by this cell rather than by increased literal retention." |
| `rq_forget_reclassification` | `sp_competing_risks` | "Content-neutralization and structural-eviction cause-specific hazards are separately estimable, and the aggressive-policy effect appears in the content-neutralization hazard specifically (not the structural one); the per-cell persistence classification agrees across two disjoint random half-samples of injected claims in at least 80% of cells." |
| `rq_probe_validity` | `sp_probe_validity` | "The mechanical acceptance probe agrees with human adjudication at Cohen's κ ≥ 0.7 on the held-out set, with disagreements confined to adjacent/borderline cases rather than a systematic misread of one adoption type." |

*(Note: the draft table initially listed only 6 rows — the second `m_competing_risks` hypothesis and the `m_policy_treatment` placebo hypothesis were both folded awkwardly. Corrected in the refiner pass to 7 one-to-one rows; see below.)*

**critique:**
- summary: Tier accounting is clean and every listed RQ traces to a verbatim hypothesis, but one dataset justification is a provenance note rather than a reason, and the RQ count does not match the 7 confirmed hypotheses one-to-one.
- comments:
  - `{severity: major, field: "datasets[recall2forget]", anti_pattern: "weak justification", comment: "'Provides long-term personalized interaction streams' says nothing about which RQ needs it or why *this* stream. The real reason is specific and load-bearing: the central hazard-ratio RQ (rq_policy_reversal) and its placebo (rq_placebo_specificity) need streams long enough that the right-censoring fraction at horizon T is small enough for the Kaplan–Meier median (half-life) CI to actually close; a short stream leaves most subjects censored and the central Cox HR underpowered. State that, or the dataset choice reads as convenience."}`
  - `{severity: major, field: "research_questions", anti_pattern: "uncovered_hypothesis", comment: "Stage 5 confirmed 7 hypotheses (m_policy_treatment and m_competing_risks each carry two), but the table has 6 rows — the second competing-risks hypothesis (cause-specific separability of content-neutralization vs structural-eviction, the Forget-as-amplification test) and the split-half reliability clause are jammed into one row, and one hypothesis is effectively uncovered. Split into 7 one-to-one mechanism-tier RQs."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets[recall2forget]` justification replaced: "supplies benign streams long enough that the right-censoring fraction at horizon *T* stays low enough for the Kaplan–Meier half-life CI to close and the central Cox hazard-ratio (rq_policy_reversal) to reach its pre-registered power; short streams would leave most subjects censored and underpower the headline contrast."
- `research_questions` expanded to **7** one-to-one rows: the competing-risks hypothesis was split into `rq_forget_reclassification` (cause-specific separability + the aggressive-policy effect landing in the content-neutralization hazard specifically — the Forget-as-amplification test) and `rq_split_half_reliability` (the ≥80% split-half classification-agreement clause). Final verbatim mapping:

| rq_id | target_hypotheses (verbatim, one per row) |
|---|---|
| `rq_estimand_recovery` | (m_survival_estimator H) |
| `rq_policy_reversal` | (m_policy_treatment H-a — the central reversal) |
| `rq_placebo_specificity` | (m_policy_treatment H-b — benign tracer null) |
| `rq_laundering_mechanism` | (m_behavioral_probe H — laundering cell rises with aggressiveness) |
| `rq_forget_reclassification` | (m_competing_risks H-a — cause-specific separability; aggressive effect in content-neutralization hazard) |
| `rq_split_half_reliability` | (m_competing_risks H-b — ≥80% split-half classification agreement) |
| `rq_probe_validity` | (m_probe_validation H — κ ≥ 0.7, adjacent-only confusions) |

- `changes_made`: gave the benign-stream dataset a hypothesis-linked reason; split the two-clause competing-risks row into two RQs so all 7 hypotheses are covered one-to-one.
- `declined_to_fix`: none.

**Confirmed Stage 6** — 7 mechanism-tier RQs, 0 outcome-tier (empirical gating satisfied).

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem`/`technical_challenge` name no technique (survival estimators, Cox, competing-risks first appear in Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_censored_estimand.source_limitation_ids = ["lim_memsecbench_checkpoint"]` ∈ Stage 3; `sp_behavioral_outcome.source_limitation_ids = ["lim_injexec_decoupling","lim_statecontam_singlepath"]` ∈ Stage 3; the other three sub-problems `["__novel__"]` with decisive-component justifications; every Stage-5 `target_sub_problem_id` ∈ Stage 4; every Stage-6 `target_hypotheses` is a **verbatim** match to a Stage-5 hypothesis ✓.
4. **Hypothesis ↔ RQ recount (literal):** Stage 5 confirmed **7** hypotheses — m_survival_estimator (1), m_behavioral_probe (1), m_policy_treatment (2), m_probe_validation (1), m_competing_risks (2) = 1+1+2+1+2 = **7**. Stage 6 confirmed **7** mechanism-tier RQs, one per hypothesis, verbatim. **7 = 7 ✓.** Framing-tier: 0 (none flagged). Outcome-tier: 0 (empirical). Total RQs = 7.
5. **Output coverage** — Stage 1's four outputs each reachable: neutralization time + survival/hazard curve via `sp_censored_estimand`+`sp_behavioral_outcome`; half-life with CI via `sp_censored_estimand` (+ `sp_policy_confound` for the policy contrast); per-cell classification via `sp_competing_risks` (+ `sp_probe_validity` for its reliability). Nothing promised in Stage 1 falls off the chain by Stage 6.
6. **`study_type` consistency** — `empirical` throughout; Stage 6 emits 0 outcome-tier RQs, correctly.

**What was hardest:** the recurring tension was **construct discipline around the event definition** — repeatedly having to prevent "neutralization" from silently collapsing back onto literal presence (the easy, detectable thing) when the whole study turns on it being behavioral adoption (the thing laundering keeps alive). Stage 1's event-definition major, Stage 4's construct-vs-reliability split, and Stage 5's exposure-confound major are three faces of the same discipline: the laundering hypothesis is only measurable if every downstream instrument refuses to equate "gone from the store" with "no longer steering behavior."

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass each = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.
