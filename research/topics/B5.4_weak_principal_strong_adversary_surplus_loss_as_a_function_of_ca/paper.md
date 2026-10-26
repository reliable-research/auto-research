# Weak Principal, Strong Adversary: Surplus Loss as a Function of Capability Gap — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run. All ids (C*, M*, CO*, RQ*, t*) resolve to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** The surplus a stronger negotiator extracts from a weaker one is not fixed by the capability gap but by how much of that gap can pass through the action-space channel the protocol leaves open to the weaker party — so structurally narrowing that channel can cut the extractable surplus *without* changing either agent's capability.

**判据 (deletion test):** Delete the domain nouns (surplus, negotiator, capability gap, action-space channel, protocol, party): *"The ___ a stronger ___ extracts from a weaker one is not fixed by the ___ but by how much of it can pass through the ___ the ___ leaves open — so narrowing ___ can cut the extractable ___ without changing ___."* The residue is empty/unparseable, not a valid generic statement. The claim is load-bearing on the specific proposition that **surplus extraction is channel-gated, not purely capability-gated** — this is the invariant, not a bridge between two literatures.

## Step 2 — Archetype

- **Primary archetype (consistent with N12 `empirical`):** controlled behavioral **measurement study** — a measured scaling relationship (surplus-loss vs. capability gap) plus a pre-registered factorial **causal contrast** (constraint-as-protection), over already-trained LLMs.
- **Secondary:** counter-intuitive-phenomenon ("束缚反而保护" / constraint-as-protection, seed line 19).

Downstream commitments:
- **(a) Abstract contribution slot:** a measured surplus-loss-vs-gap curve (slope+CI, CO1) AND a causal verdict on whether action-space constraint lowers a weak agent's surplus loss (CO2). Not a system, not a leaderboard.
- **(b) Intro logic:** "what becomes measurable" — for the first time we quantify *economic* exploitation under capability asymmetry against a closed-form reference split, and test a near-zero-cost deployment mitigation. Not "beat a number."
- **(c) Evidence standard:** pre-registered directional hypotheses each with a falsification condition, a controlled factorial, and budget/capability-matched controls; a claim survives only where its sign is invariant across both gap measures and all three reference splits (t1, t4).

## Step 3 — Taste self-audit

- **Bridge check:** The opportunity is a *phenomenon* (channel-gated surplus extraction, Step 0), not "connect oversight-scaling to economics." **Risk flagged:** the motivation (N2) must not lean on "no one connected weak-vs-strong oversight to bargaining"; it must lead with the mechanism. **Corrected framing:** intro opens on the channel-gating asymmetry and the deployment question it forces, citing oversight-scaling only as method precedent (Elo estimation, M1), not as the thing being bridged. **Pass after fix.**
- **Synthesis check:** the method is not "combine game X + metric Y." The novel isolable object is **M3, the action-space constraint applied to one side as a deployment-time intervention**, which no cited work operationalizes (N4). **Pass.**
- **Verb check:** load-bearing verbs are *measure, isolate, test, gate* — not from the integrate/unify/leverage family. **Pass.**
- **Abstract-opening rule:** obeyed in Abstract v0 (mechanism first; verbs = measure/test/isolate; no "X is increasingly used… however… we introduce").

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1):** the average normalized surplus loss `E[L]` retained by a weak
principal's LLM agent `w` (unit of analysis: one directed model-pair `(w,s)` × game-instance
× action-space-condition episode), as a function of the capability gap `Δ(w,s)` to a strong
adversary `s`, over the reference population of present-day LLMs playing bilateral
multi-issue bargaining under a computable reference split — feeding the deployment decision
of whether, and under what action-space condition, a principal may safely field a
cost-efficient (weaker) negotiation agent against an unknown-or-stronger counterparty.

Notation: weak agent `w` (principal's representative), strong adversary `s`. Directed model pair `(w,s)`. Game instance `g` with private integer valuations, reservation values `r_w, r_s`, deadline `T=10` rounds. Action-space condition `c ∈ {structured, free}` applied to `w` only (in primary cells). Episode `e`.

| Adjective/verb (from Claims) | Formal definition | How measured |
|---|---|---|
| **normalized surplus loss** `L` | `L = (u_ref − u_realized) / (u_ref − r_w)` for the weak side; impasse → `u_realized = r_w` ⇒ `L=1` | deterministic game engine; `u_ref` from Nash-bargaining split of `g` (M2, M4) |
| **capability gap** `Δ` | dual scalar: `Δ_a` = exogenous public general-capability score delta (Arena Elo / MMLU-Pro), fixed pre-play; `Δ_b` = endogenous negotiation Elo delta fit from round-robin play (M1) | precomputed table per directed pair; both reported |
| **constraint / structured** | `w`'s entire turn = one schema-validated JSON `{action, allocation}`; no NL field transmitted; ≤2 resamples on parse failure | constrained decoding + schema validator (M3) |
| **protects / constraint-as-protection** | `E[L | c=structured] < E[L | c=free]` at matched `Δ`, same `(w,s)` | RQ2a mixed-effects contrast (M5) |
| **substitute for capability** | `E[L | w=t, c=structured] ≤ E[L | w=t+1, c=free]` vs. same `s` (tier `t+1` stronger) | RQ2b cross-cell contrast (M5) |
| **rhetorical channel (share)** | fraction of the `Δ→L` slope removed when the free-text field is deleted: `(β_free − β_structured)/β_free` | between-condition slope difference (M5, RQ_INF_3) |
| **protocol-valid episode** | offers parseable AND terminates in agreement-or-impasse within `T` | engine flag per episode (Stage-1 gate) |

Any adjective without a row above is deleted from claims.

## Assumptions (A1..An)

*(Slots per guidance.md §3.2: assumption / failure_mode / detection / gate / consequence.
`consequence` added explicitly below at the 2026-07-04 Phase A re-run — guidance.md §3.2 and
Part 6 item 4 require it as its own slot, not left implicit in the detection text.)*

- **A1 — weak tiers can negotiate.** Weakest cell yields ≥80% protocol-valid episodes with nonzero surplus-loss spread. *Fails:* all-impasse degeneracy (floor effect) makes the curve unidentifiable (N6 feasibility risk). *Detected:* Stage-1 gate (walking skeleton); if failed, swap in a stronger "weak" tier before Stage 2 spend. *Consequence:* blocks H1/H2a/H2b/H3 outright — `L` is undefined at floor (all-impasse) cells, so no hypothesis in Step 6 can be scored until this gate passes; this is a pre-Stage-2 block, not a per-hypothesis degradation.
- **A2 — computable reference split.** Every game instance `g` admits a closed-form Pareto frontier + Nash/equal/KS points. *Fails:* `u_ref` undefined. *Detected:* harness unit test computes all three references for every generated instance; instance rejected if any is undefined (M2). *Consequence:* affected instances are dropped pre-analysis (excluded from every headline n, per goal.md R8), never scored with an undefined `L`; if drop rate exceeds 10% of generated instances, the harness itself (M2) is treated as broken and Stage 1 is re-run before any H* is evaluated.
- **A3 — gap is orderable.** `Δ_a` and `Δ_b` agree on pair ordering. *Fails:* opposite-signed slopes (C1 projection-dependence). *Detected:* both measures reported; disagreement is itself a reportable RQ1 outcome (not hidden). *Consequence:* directly fails H1's same-signed-slopes clause (Step 6), triggering H1's own fallback wording rather than a separate downgrade — the consequence is already load-bearing inside H1's binary criterion, not a side effect.
- **A4 — no condition leakage to adversary.** `s` reacts to `w` only through `w`'s channel, not through prompt-format cues signalling `c` (t2). *Fails:* confounded condition contrast. *Detected:* identical adversary system prompts, condition undisclosed, side/first-mover counterbalancing, both-constrained control cell. *Consequence:* if leakage is detected (adversary behavior differs by condition in the both-constrained control, where it should not), H2a and H2b are both downgraded to the B-alt "confounded, not causal" wording (Step 6 fallback discipline) rather than scored as passed.
- **A5 — reliable tactic tagging.** LLM-judge tactic labels reach Cohen's κ ≥ 0.7 vs. 10% human double-coding (t5). *Fails:* channel attribution biased to null. *Detected:* κ acceptance gate; RQ_INF_3 kept exploratory. *Consequence:* if κ < 0.7, RQ_INF_3's tactic-incidence correlational half is dropped from the paper entirely (not reported with a caveat) — only the between-condition slope-difference bound (which does not depend on tagging) survives.
- **A6 — stable model versions.** Pinned model versions over a fixed evaluation window (t2). *Fails:* mid-experiment provider updates. *Detected:* re-run anchor cells at window end; discard if drift shifts anchor-cell mean `L` by >0.05. *Consequence:* if drift exceeds the 0.05 threshold, every cell run before the drift is treated as a separate stratum (time-window fixed effect added to the mixed-effects model) rather than pooled, and if strata disagree in sign the paper reports the disagreement per Part 4 situation 9 rather than pooling silently.

**Cross-condition design-constraint / confound ledger (guidance.md R3 — each constraint
names the confound it removes):**
- Identical adversary system prompts + undisclosed condition (A4) removes the confound of
  *adversary reactivity to condition-disclosure* (the adversary playing differently merely
  because it can tell which condition it is in, rather than because of the weak agent's
  actual channel).
- Side/first-mover counterbalancing (A4) removes the confound of *positional advantage*
  (whichever party moves first or is anchored to a role systematically gaining surplus,
  independent of capability gap or condition).
- The both-constrained control cell (B-alt) removes the confound of *bilateral instrument
  bias* — it isolates whether a residual gap-slope in the structured condition is
  substantive (survives even when neither side has a rhetorical channel) rather than an
  artifact of the weak side alone losing a channel.
- Pinned model versions over a fixed window (A6) removes the confound of *temporal
  provider drift* (a model silently updated mid-experiment changing outcomes independent of
  the manipulated gap or condition).
- Zero-gap self-play controls (B0) remove the confound of *mechanically biased scoring* —
  they test whether `L` is an artifact of the harness/reference-split choice rather than of
  a genuine capability gap.

## Step 6 — Pre-Registered Experiments

**Thin-cell rule (guidance.md Part 4 situation 5 / Part 6 item 9):** any gap-level × condition
× game-family cell with fewer than 30 valid episodes (below the powered n=50 target) is
pre-declared **INCONCLUSIVE** for that cell — its data are reported but excluded from the
primary Wald/Holm tests below, and INCONCLUSIVE cells are never scored as null or dropped
silently. If the *central* test (H1's pooled slope, or H2a's pooled condition main effect)
is underpowered because more than 25% of its constituent cells are thin, the whole test is
labeled INCONCLUSIVE rather than reported as a null finding.

### RQ1 — surplus-loss scaling (CO1; M1,M2,M4; C1,C2)
- **Assumption:** A1, A2, A3.
- **Hypothesis H1 (binary):** In the free-text condition, the mixed-effects gap slope `β_Δ > 0` with two-sided Wald `p < 0.05` under **both** `Δ_a` and `Δ_b`, AND Spearman `ρ > 0` over gap levels (monotone), AND the two gap measures give **same-signed** slopes, **AND the effect floor**: the model-implied increase in `L` from the smallest to the largest tested gap level (`β_Δ × range(Δ)`) is **≥ 0.10 normalized-loss units** under each gap measure — a statistically significant but sub-0.10 slope is reported as "detected but below the pre-registered practical-significance floor," not as H1 passing.
- **Metric:** `L` (primary); slope `β_Δ` from `L ~ Δ + (1|g) + (1|pair)`.
- **Verification:** mixed-effects linear regression, random intercepts for game instance and model pair, clustered by pair; n=50 episodes/cell; 30 directed unequal pairs + 6 zero-gap self-play controls × 3 game families.
- **Fallback:** if H1 fails (flat/non-monotone, opposite-signed across measures, or below the 0.10-unit effect floor) → claim **"normalized surplus loss is not a monotone, practically-significant function of a scalar capability gap; the gap axis is projection-dependent (confirms C1),"** reported as a measurement-of-confound finding with the two divergent curves.

### RQ2a — same-model constraint contrast (CO2,CO4; M3,M5; C4) — *digest contrast (a)*
- **Assumption:** A1, A2, A4.
- **Hypothesis H2a (binary):** condition main effect is negative — `E[L|structured] < E[L|free]` for the **same** `(w,s)` — with Holm-corrected `p < 0.05`, AND point-estimate reduction in normalized loss `≥ 0.05` units, AND the condition×gap interaction is positive (protection grows with `Δ`).
- **Metric:** `L`; condition main effect + condition×gap interaction coefficients.
- **Verification:** 2(condition)×k(gap) mixed-effects factorial; two primary tests (main effect, interaction) with Holm correction, α=0.05; clustered by pair; n=50/cell (detects d≈0.4 at power 0.8 per gap level, N8 analysis plan).
- **Fallback:** if H2a fails (`E[L|structured] ≥ E[L|free]` or non-significant) → claim **"expressive freedom does not expose the weak agent; action-space restriction is neutral-to-harmful, refuting constraint-as-protection"** — a publishable negative that supports the default intuition.
- **Sharpened prediction from the human-bargaining method-twin (digest.md N3
  `[LanguageOfBargaining, ACL:2023.acl-long.735]`, added at the 2026-07-04 Phase A re-run):**
  Heddaya et al. (2023) find that the same structured-offer-vs-free-text manipulation, run
  between *symmetric-capability* human dyads, leaves the average agreed price unchanged
  (only process metrics — speed, agreement rate, price variance — differ). This predicts
  that H2a's condition main effect should be **near zero specifically at `Δ≈0`** (the B0
  zero-gap self-play cells) and should only emerge as the significant **condition×gap
  interaction** already in H2a's own criterion — i.e. a near-null B0 condition contrast is
  not evidence against H2a, it is the specific pattern this prior human-subjects result
  predicts and that H2a's interaction term is designed to detect.

### RQ2b — cross-tier substitution contrast (CO2,CO4; M3,M5; C4) — *digest contrast (b), the seed's literal question*
- **Assumption:** A1, A2, A4.
- **Hypothesis H2b (binary):** a constrained weak agent of tier `t` undercuts an **unconstrained** agent of the next-stronger tier `t+1` against the same adversary, within a pre-registered **non-inferiority margin δ = 0.05 normalized-loss units**: `E[L | w=t, structured] ≤ E[L | w=t+1, free] + 0.05`, one-sided non-inferiority test, α=0.05, for **at least one** adjacent tier pair. (Without this explicit margin, "≤" alone is a superiority test mislabeled as non-inferiority — guidance.md §3.1's effect-floor rule requires the floor be stated in native `L` units, matching H2a's own 0.05-unit convention.)
- **Metric:** `L`; cross-cell mean difference at matched adversary.
- **Verification:** cross-cell contrast read off the same gap×condition factorial; one-sided mixed-effects test per adjacent tier pair against the δ=0.05 margin, Holm-corrected across the tested adjacent pairs.
- **Fallback:** if H2b fails → claim **"constraint helps within a model but cannot compensate for one capability tier; capability remains the dominant lever and constraint is a second-order mitigation"** — bounds the deployment recommendation CO4.

### RQ_INF_3 — channel attribution (CO4; M3,M5; C3) — exploratory
- **Assumption:** A2, A4, A5.
- **Hypothesis H3 (binary, exploratory):** the between-condition slope difference removes **>50%** of the free-text gap slope, i.e. `(β_free − β_structured)/β_free > 0.5`, AND adversary tactic incidence correlates positively with per-episode `L` (`p < 0.05`).
- **Metric:** rhetorical-channel share (Step 5); tactic incidence per transcript (LLM-judge, κ≥0.7).
- **Instrument validation (guidance.md R2, full 5-step sequence — added at the 2026-07-04
  Phase A re-run; previously only step ③ was specified):**
  ① **Ground categories externally:** the four tactic labels (anchoring, misrepresentation
  of value, false deadline/commitment, flattery/pressure) are grounded in established
  negotiation-tactics taxonomies (integrative/distributive-bargaining "hardball tactics"
  literature, e.g. Lewicki et al.'s negotiation tactics inventory) and in this cache's own
  `[BEDA2512]` adversarial/alignment dialogue-act formalization and `[StrategicPersuasion,
  OpenReview:aTCXvJKnkE]`'s persuasion-move vocabulary — not invented ad hoc.
  ② **Draft wide, refine on a held-out calibration set:** draft an initial 8–10 label set
  from the above sources, pilot-tag a held-out sample of 100 transcripts from the Stage-1
  skeleton run, and merge/split/remove labels with named operations (e.g. merge near-
  synonymous tactics with pairwise tagging agreement > 0.9) down to the frozen 4-label set.
  ③ **Validate against ≥2 independent human raters:** 10% double-coded by two human raters
  on the held-out set, target Cohen's κ ≥ 0.7 (A5) — the acceptance threshold.
  ④ **Inspect confusion structure:** the confusion matrix between LLM-judge and human labels
  must show disagreements concentrated between adjacent/related tactics (e.g. anchoring vs.
  misrepresentation-of-value), not a systematic collapse onto one dominant label; a
  systematic-collapse pattern fails validation even if aggregate κ clears 0.7.
  ⑤ **Freeze before scale:** the label set, prompt, and confusion-structure check are hashed
  and frozen before any Stage-2 scale-up tagging begins.
- **Verification:** paired between-condition slope difference per gap level + logistic/Poisson model of `L` on tactic counts; α=0.05, **labeled exploratory, no confirmatory claim** (t4, t5).
- **Fallback:** if structured-condition slope ≈ free-text slope (channel share ≈ 0) → claim **"exploitation is substantive (offer/concession strategy), not rhetorical; any protection from constraint operates via decision-simplification, not channel-closure"** — revises the mechanism story behind CO4. If step ③ fails to reach κ≥0.7 even after one refinement pass (step ②), per guidance.md Part 4 situation 7: simplify to a coarser 2-label split (rhetorical vs. non-rhetorical) and re-validate once; if that also fails, RQ_INF_3 is dropped to "not measurable at acceptable reliability" rather than reported with an uncalibrated judge.

### Mandatory baselines
- **B0 — "why do this at all" control (zero-gap self-play + scripted floor).** Weak-vs-weak and strong-vs-strong self-play (Δ=0), plus a scripted time-dependent (Boulware/linear) conceder as a capability floor. **Justifies existence:** if `E[L] ≈ 0` at Δ=0, surplus loss is caused by the gap and not by a mechanically biased metric or game; if `E[L]` is large even at Δ=0, the metric is broken and the study is void. Pre-registered pass: `|E[L | Δ=0]| ≤ 0.05`.
- **B-alt — strongest-alternative-explanation control (both-constrained cell + capability-matched adversary).** **Rival explanation:** the strong adversary wins purely on *substance* (better offer/concession strategy, value inference) and/or the constraint merely reduces the weak model's own parse/coherence errors — i.e., free text is *not* an exploitation channel. **Isolation:** the both-constrained cell (both sides schema-only, no NL either way) removes the rhetorical channel bilaterally; if the `Δ→L` slope persists there at the free-text magnitude, exploitation is substantive (kills the rhetorical-channel story even if H2a holds); if it collapses, the channel account is supported.

### Global fallback F-G1
If the constraint-as-protection family fails outright (**both H2a and H2b refuted**), pivot archetype from "actionable mitigation" to pure "measurement/characterization": the headline becomes the surplus-loss-vs-gap scaling law (CO1/RQ1) plus a clean negative result.
> *Pivoted abstract sentence:* "We measure how much bargaining surplus a weak principal's agent loses per unit of capability gap to a strong adversary, and show — contrary to the constraint-as-protection conjecture — that restricting the weak agent's action space does not recover surplus, isolating model capability itself as the operative lever."

## Step 9 — Walking Skeleton

- **Binary question:** *Does a constrained weak agent incur lower normalized surplus loss `L` than a free-text weak agent, for one fixed `(w,s)` pair on one game family?*
- **Arms (2, +1 optional control):** `structured` weak, `free` weak; optional `both-constrained` cell.
- **Task set:** 1 weak tier, 1 fixed strong adversary, 1 game family (GLEE-style bargaining), 50 episodes/cell → 100–150 episodes.
- **Metrics (deterministic only):** `L`, agreement/impasse rate, protocol-valid rate. No LLM-judge in the skeleton.
- **Cost:** ~2–3M tokens, tens of dollars API, ~1 person-week incl. harness debugging (N6 feasibility, Stage 1).
- **Skeleton-passed criterion:** ≥80% protocol-valid episodes in the weakest cell (A1) AND nonzero `L` spread AND the constrained-vs-free contrast computes end-to-end. When passed, scaling to the full grid (6 models, 3 game families, 30 pairs, both-constrained + zero-gap controls, tactic tagging) is a **config change** — add entries to the model list, game list, and cell matrix — **not a code change.**

## Claim–Evidence Map

| Abstract claim | Traces to | Status |
|---|---|---|
| Surplus loss increases with capability gap | H1 / RQ1 | needs-experiment |
| At zero gap there is no surplus loss (metric valid) | B0 / Step 5 `L` | supported-by-design |
| Restricting the weak agent's action space lowers its surplus loss (same model) | H2a / RQ2a | needs-experiment; fallback-covered |
| Constraint can substitute for ≥1 capability tier | H2b / RQ2b | needs-experiment; fallback-covered |
| Most gap-dependent loss flows through the rhetorical channel | H3 / RQ_INF_3 | needs-experiment (exploratory); fallback-covered |
| Reusable bargaining harness w/ closed-form frontiers + 3 references | Step 5 defs / M2 (CO3) | supported-by-design |
| Deployment recommendation "constraint-as-protection" | H2a ∧ H2b (CO4) | fallback-covered (F-G1) |

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS)

> When a stronger LLM negotiates against a weaker one on a principal's behalf, how much surplus the stronger side extracts is gated not only by the capability gap but by the action-space channel the protocol leaves open to the weaker party — so narrowing that channel could deny the stronger side the surface through which its advantage converts into surplus, without changing either model. We measure this. Over multi-issue alternating-offers bargaining with closed-form Pareto frontiers and a Nash reference split, across two established game families and a capability ladder of LLMs, we estimate normalized surplus loss as a function of a dual capability-gap measure (exogenous score delta; endogenous negotiation Elo). We then test, causally, whether restricting the weak agent to schema-validated structured offers (no free text) lowers its loss versus free-form negotiation — and whether that constraint can substitute for a tier of capability. Zero-gap self-play and both-constrained controls isolate exploitation from incompetence. Every hypothesis is pre-registered with a falsification condition.
